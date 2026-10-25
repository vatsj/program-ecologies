"""Islands to infinity before time (spec specs/2026-10-25-many-islands.md; notes notes/many-islands.md; predictions
predictions/2026-10-25-many-islands.md).

Rare-migration jump chain on settled islands of three-player majority division (dollar3), with annealed mutation
before migration and the number of islands taken large before time.

Structure (notes 1.2).  A settled island is a program triple.  One migrant into slot s meets two monomorphic other
slots, so slot s is a two-type Moran process with constant fitness ratio exp(w * dpay); the island-state chain is
exactly Markov on triples with the closed-form kernel `pfix`.  The pieces:

  - `Arm`: a program catalogue (canonical functions of the dollar3 DSL, an evaluator, seed laws per slot).
  - joint-code cache: an open-addressing hash of (x0, x1, x2) -> joint code, filled on demand by the stored
    evaluator (`dollar3.enc_into`), so no K^3 table is built.
  - `island_run`: the stored island kernel (`stable_sets.kern`, I = 1, m = 0) re-expressed with the lazy joint
    cache, a monomorphic stopping rule and annealed arrivals; with no arrivals it consumes random numbers in the
    stored kernel's order (checked draw for draw in tests/test_many_islands.py).
  - `chain_run`: the pool Monte Carlo of the jump chain (donor / slot / recipient uniform; exact Moran fixation).
  - exact kernel and ODE helpers (injection statistics, class-level equation).

Importable without side effects; the drivers are in many_islands_run.py.
"""
import os, sys
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from numba import njit
import dollar3 as D
import stable_sets as SS
import dominance_contracts_run as DR

ROOT = SS.ROOT
W = SS.W
N0 = 100
T = DR.tables()
X = T.R
NOUT = len(X)
PAY = np.ascontiguousarray(T.PAY)                 # (729, 3) dollar units
VEC = np.ascontiguousarray(T.VEC)                 # (729,) outcome id
ISMEM = np.ascontiguousarray(T.ISMEM)
TOT = np.ascontiguousarray(T.TOT)
V = sorted(SS.symmetric_set(X, 6))                # outcome ids of the three fair pairs
CATLAB = ['F', 'U', 'G', 'W', 'D']


def _cat(k):
    c = T.cat[k]
    if c == 'fair': return 0
    if c == 'unequal': return 1
    if c.startswith('grand'): return 2 if sum(X[k]) == 6 else 3
    if c == 'wasteful': return 3
    return 4


CATMAP = np.array([_cat(k) for k in range(NOUT)], np.int8)
# the slot not in the pair (-1 if none) of each outcome
EXCL = np.full(NOUT, -1, np.int64)
for _k, _x in enumerate(X):
    _z = [i for i in range(3) if _x[i] == 0]
    if len(_z) == 1 and sum(_x) > 0:
        EXCL[_k] = _z[0]
OLAB = []
for _k in range(NOUT):
    _c = int(CATMAP[_k])
    OLAB.append(('F%d' % V.index(_k)) if _c == 0 else T.labels[_k])
VIDX = np.full(NOUT, -1, np.int64)
for _i, _v in enumerate(V):
    VIDX[_v] = _i


# ====================================================================== arms
class Arm:
    """name: 'L' (weak evaluator, length prior), 'M' (modalPA evaluator, same law), 'R' (E-min main catalogue under the
    modalPA evaluator: flexible readers at about 9%), 'Rw' (the same catalogue under the weak evaluator)."""

    def __init__(self, name):
        self.name = name
        if name in ('L', 'M'):
            S, mu = SS.arm_data('weak')
            self.S = S
            self.armi = D.ARM['weak' if name == 'L' else 'modalPA']
            self.laws = np.array([SS.seed_law('L', s) for s in range(3)])
            self.cat = None
        elif name in ('R', 'Rw'):
            import churn_primary as CP
            cat = CP.get_cat('Emin-main-m' if name == 'R' else 'Emin-main-w')
            self.cat = cat
            self.S = cat.S
            self.armi = cat.armi
            self.laws = np.array([cat.law(s) for s in range(3)])
        else:
            raise ValueError(name)
        self.K = self.laws.shape[1]
        self.cum = np.cumsum(self.laws, axis=1)
        self.cum /= self.cum[:, -1:]
        S = self.S
        self.arrs = (np.ascontiguousarray(S.nat), np.ascontiguousarray(S.atL), np.ascontiguousarray(S.atJ),
                     np.ascontiguousarray(S.atA), np.ascontiguousarray(S.tab), np.ascontiguousarray(D.PARTNER))
        self.cache = None

    def new_cache(self, bits=24):
        cap = 1 << bits
        self.cache = dict(keys=np.zeros(cap, np.uint32), vals=np.zeros(cap, np.int16), meta=np.zeros(2, np.int64),
                          bits=bits)
        return self.cache

    def ctx(self):
        if self.cache is None:
            self.new_cache()
        c = self.cache
        scratch = (np.zeros((2, 3), np.int64), np.zeros(3, np.int64), np.zeros(3, np.int64))
        return (c['keys'], c['vals'], c['meta'], np.int64(self.armi), self.arrs[0], self.arrs[1], self.arrs[2],
                self.arrs[3], self.arrs[4], self.arrs[5], np.int64(self.K), np.int64(c['bits']), scratch[0],
                scratch[1], scratch[2])

    def lc(self, L=32):
        """the island-local dense cache over local program ids (persistent, reset by island_run); L local ids per
        slot (programs beyond fall back on the global hash)."""
        if getattr(self, '_lc', None) is None:
            self._lc = {}
        if L not in self._lc:
            self._lc[L] = (np.full((3, self.K), -1, np.int32), np.full(L ** 3, -1, np.int16),
                           np.zeros(min(L ** 3, 1 << 22), np.int64), np.zeros(1, np.int64), np.int64(L))
        return self._lc[L]

    def maybe_flush(self, frac=0.5):
        c = self.cache
        if c is not None and c['meta'][0] > frac * (1 << c['bits']):
            c['keys'][:] = 0; c['vals'][:] = 0; c['meta'][:] = 0
            c['meta'][1] += 1                      # flush counter

    def joint(self, x0, x1, x2):
        return int(_jl_py(self.ctx(), x0, x1, x2))

    def name_of(self, s, x):
        return self.S.src(s, x) if x < len(self.S.fs) else self.cat.S.src(s, x)


def permute_support(arm, sigma):
    """perm[s][x] = index in slot sigma[s] of the image of slot s's program x, for the programs x with positive seed
    mass in slot s (-1 elsewhere): `Slots.permute` restricted to the support, since the readers' catalogue holds
    absolute forms that are meaningful only in their own slot."""
    S = arm.S
    out = []
    for s in range(3):
        ts = sigma[s]
        m = -np.ones(arm.K, np.int64)
        for x, f in enumerate(S.fs):
            if arm.laws[s][x] <= 0:
                continue
            atoms, tab = f
            img_atoms = []
            for (L, jr, al) in atoms:
                j = D.others(s)[jr]; tj = sigma[j]
                p = D.partner_abs(j, al); tp = D.ALL if p == D.ALL else sigma[p]
                img_atoms.append((L, D.others(ts).index(tj), D.local_of(tj, tp, al % 3)))
            img_tab = []
            for l in tab:
                p = D.partner_abs(s, l); tp = D.ALL if p == D.ALL else sigma[p]
                img_tab.append(D.local_of(ts, tp, l % 3))
            g = D.Lang._reduce(img_atoms, img_tab)
            m[x] = S.index[ts][g]
        out.append(m)
    return out


# ====================================================================== joint-code cache (njit)
@njit(cache=True)
def jl(C, x0, x1, x2):
    keys, vals, meta, armi, nat, atL, atJ, atA, tab, PARTNER, K, bits, hist, val, u = C
    key = np.uint32(((x0 * K + x1) * K + x2) + 1)
    h = (np.uint64(key) * np.uint64(0x9E3779B97F4A7C15)) >> np.uint64(64 - bits)
    mask = (np.int64(1) << bits) - 1
    p = np.int64(h)
    while True:
        kk = keys[p]
        if kk == key:
            return np.int64(vals[p])
        if kk == 0:
            D.enc_into(armi, nat, atL, atJ, atA, tab, PARTNER, x0, x1, x2, hist, val, u)
            code = val[0] * 81 + val[1] * 9 + val[2]
            if meta[0] * 10 < ((np.int64(1) << bits) * 7):       # never fill the table (probing must terminate)
                keys[p] = key; vals[p] = code; meta[0] += 1
            return code
        p = (p + 1) & mask


def _jl_py(C, x0, x1, x2):
    return jl(C, np.int64(x0), np.int64(x1), np.int64(x2))


@njit(cache=True)
def cod(C, s, k, p, q):
    """joint code with focal program k in slot s, (p, q) the other two slots' programs in increasing slot order."""
    if s == 0:
        return jl(C, k, p, q)
    if s == 1:
        return jl(C, p, k, q)
    return jl(C, p, q, k)


@njit(cache=True)
def codl(C, LC, s, k, p, q):
    """as cod, through the island-local dense table (local program ids), falling back on the global hash."""
    loc, Jl, touched, tc, L = LC
    if s == 0:
        a = k; b = p; c = q
    elif s == 1:
        a = p; b = k; c = q
    else:
        a = p; b = q; c = k
    la = loc[0, a]; lb = loc[1, b]; lc = loc[2, c]
    if la < 0 or lb < 0 or lc < 0:
        return jl(C, a, b, c)
    idx = (la * L + lb) * L + lc
    v = np.int64(Jl[idx])
    if v >= 0:
        return v
    v = jl(C, a, b, c)
    if tc[0] < touched.shape[0]:
        Jl[idx] = np.int16(v); touched[tc[0]] = idx; tc[0] += 1
    return v


@njit(cache=True)
def _assign(LC, nloc, assigned, s, k):
    loc = LC[0]; L = LC[4]
    if loc[s, k] < 0 and nloc[s] < L:
        loc[s, k] = nloc[s]; assigned[s, nloc[s]] = k; nloc[s] += 1


# ====================================================================== Moran fixation
@njit(cache=True)
def pfix(dpay, N, w):
    """fixation probability of one migrant in a two-type Moran process (parent proportional to count * exp(w pay),
    victim uniform) with constant payoff advantage dpay (dollar units)."""
    a = w * dpay
    if abs(a) < 1e-12:
        return 1.0 / N
    if a > 0:
        # (1 - e^{-a}) / (1 - e^{-aN})
        return (1.0 - math.exp(-a)) / (1.0 - math.exp(-a * N))
    # a < 0, b = -a: (e^b - 1) / (e^{bN} - 1) = (1 - e^{-b}) e^{-b (N - 1)} / (1 - e^{-b N})
    b = -a
    return (1.0 - math.exp(-b)) * math.exp(-b * (N - 1.0)) / (1.0 - math.exp(-b * N))


PFT = np.array([pfix(d / 6.0, float(N0), W) for d in range(-4, 5)])      # fixation probability by payoff change in sixths


def pfix_py(dpay, N=N0, w=W):
    return pfix(float(dpay), float(N), float(w))


# ====================================================================== the island kernel
@njit(cache=True)
def _setact(u, a, act, apos, nact):
    p = apos[u]
    if a and p >= nact:
        j = act[nact]; act[nact] = u; act[p] = j; apos[u] = nact; apos[j] = p; nact += 1
    elif (not a) and p < nact:
        nact -= 1; j = act[nact]; act[nact] = u; act[p] = j; apos[u] = nact; apos[j] = p
    return nact


@njit(cache=True)
def _others(s):
    if s == 0:
        return 1, 2
    if s == 1:
        return 0, 2
    return 0, 1


@njit(cache=True)
def _fit(C, LC, PAYt, counts, pres, npres, s, k):
    o1, o2 = _others(s)
    v = 0.0
    for t1 in range(npres[o1]):
        p = pres[o1, t1]
        for t2 in range(npres[o2]):
            q = pres[o2, t2]
            v += counts[o1, p] * counts[o2, q] * PAYt[codl(C, LC, s, k, p, q), s]
    return v


@njit(cache=True)
def _parent(F, counts, pres, npres, s, N2, w):
    m = -1e300
    for t in range(npres[s]):
        k = pres[s, t]
        f = F[s, k] / N2
        if f > m: m = f
    tot = 0.0
    for t in range(npres[s]):
        k = pres[s, t]
        tot += counts[s, k] * np.exp(w * (F[s, k] / N2 - m))
    u = np.random.random() * tot; acc = 0.0
    for t in range(npres[s]):
        k = pres[s, t]
        acc += counts[s, k] * np.exp(w * (F[s, k] / N2 - m))
        if u <= acc:
            return k
    return pres[s, npres[s] - 1]


@njit(cache=True)
def _replace(C, LC, nloc, assigned, PAYt, counts, pres, npres, pos, F, act, apos, nact, s, child, victim):
    """one birth-death replacement in slot s (victim -> child, victim != child), the stored kernel's update."""
    _assign(LC, nloc, assigned, s, child)
    counts[s, victim] -= 1
    if counts[s, victim] == 0:
        p = pos[s, victim]; last = pres[s, npres[s] - 1]
        pres[s, p] = last; pos[s, last] = p; pos[s, victim] = -1; npres[s] -= 1
    new = counts[s, child] == 0
    if new:
        pres[s, npres[s]] = child; pos[s, child] = npres[s]; npres[s] += 1
    counts[s, child] += 1
    o1, o2 = _others(s)
    for sa in (o1, o2):
        sb = o1 + o2 - sa
        for ta in range(npres[sa]):
            k = pres[sa, ta]
            v = 0.0
            for tb in range(npres[sb]):
                q = pres[sb, tb]
                if s < sb:
                    v += counts[sb, q] * (PAYt[codl(C, LC, sa, k, child, q), sa] - PAYt[codl(C, LC, sa, k, victim, q), sa])
                else:
                    v += counts[sb, q] * (PAYt[codl(C, LC, sa, k, q, child), sa] - PAYt[codl(C, LC, sa, k, q, victim), sa])
            F[sa, k] += v
    if new:
        F[s, child] = _fit(C, LC, PAYt, counts, pres, npres, s, child)
    return _setact(s, npres[s] > 1, act, apos, nact)


@njit(cache=True)
def island_run(C, LC, PAYt, init, N, w, seed, H, arr_t, cum, mono_stop):
    """One island, three slot populations, no migration (the stored kernel with I = 1, m = 0).

    init (3, K) counts; H the cap in generations (a generation is 3N slot-events); arr_t sorted arrival times in
    generations (annealed prior arrivals: slot uniform, program from cum[slot], victim a uniform resident); the run
    stops when every slot is monomorphic and no arrival is pending (mono_stop) or at H.  Without arrivals the
    random-number order is the stored kernel's.  Returns (status, generation, counts, narr): status 0 settled
    (monomorphic), 1 capped at H."""
    np.random.seed(seed)
    K = init.shape[1]
    counts = init.copy()
    pres = np.zeros((3, K), np.int64); npres = np.zeros(3, np.int64); pos = -np.ones((3, K), np.int64)
    F = np.zeros((3, K))
    nloc = np.zeros(3, np.int64)
    assigned = np.zeros((3, LC[4]), np.int64)
    LC[3][0] = 0
    for s in range(3):
        for k in range(K):
            if counts[s, k] > 0:
                pres[s, npres[s]] = k; pos[s, k] = npres[s]; npres[s] += 1
                _assign(LC, nloc, assigned, s, k)
    for s in range(3):
        for t in range(npres[s]):
            k = pres[s, t]
            F[s, k] = _fit(C, LC, PAYt, counts, pres, npres, s, k)
    NU = 3
    act = np.arange(NU); apos = np.arange(NU); nact = 0
    for u in range(NU):
        if npres[u] > 1:
            nact = _setact(u, True, act, apos, nact)
    N2 = float(N) * N
    UN = NU * N
    b = 0.0
    g = 0
    nextchk = float(UN)
    total = float(H) * UN
    narr = 0
    na = arr_t.shape[0]
    status = 1
    while True:
        pa = nact / NU
        if pa <= 0.0:
            G = total + 1.0
        elif pa >= 1.0:
            G = 0.0
        else:
            uu = np.random.random()
            G = float(int(np.log(1.0 - uu) / np.log(1.0 - pa)))
        if narr < na:
            ba = arr_t[narr] * UN
            if nact == 0:
                # nothing happens until the arrival: jump to it
                if ba > b:
                    b = float(int(ba))
                    g = int(b // UN)
                    nextchk = float((g + 1) * UN)
                if g >= H:
                    break
                G = -1.0
            if G < 0.0 or ba <= min(b + G + 1.0, nextchk):
                if ba > b:
                    b = float(int(ba))
                # arrival
                s = np.random.randint(3)
                y = np.searchsorted(cum[s], np.random.random())
                if y >= K: y = K - 1
                r = np.random.randint(N); acc = 0; victim = pres[s, 0]
                for t in range(npres[s]):
                    k = pres[s, t]; acc += counts[s, k]
                    if r < acc:
                        victim = k; break
                narr += 1
                if victim != y:
                    nact = _replace(C, LC, nloc, assigned, PAYt, counts, pres, npres, pos, F, act, apos, nact, s, y, victim)
                continue
        elif nact == 0 and mono_stop:
            status = 0
            break
        if b + G >= nextchk:
            b = nextchk
            g += 1
            if g >= H:
                break
            nextchk = float((g + 1) * UN)
            continue
        b = b + G + 1.0
        if np.random.random() * pa * NU < nact:
            u = act[np.random.randint(nact)]
        else:
            u = act[nact + np.random.randint(NU - nact)]
        s = u
        child = _parent(F, counts, pres, npres, s, N2, w)
        r = np.random.randint(N); acc = 0; victim = pres[s, 0]
        for t in range(npres[s]):
            k = pres[s, t]; acc += counts[s, k]
            if r < acc:
                victim = k; break
        if victim == child:
            continue
        nact = _replace(C, LC, nloc, assigned, PAYt, counts, pres, npres, pos, F, act, apos, nact, s, child, victim)
        if mono_stop and nact == 0 and narr >= na:
            status = 0
            break
    for s in range(3):
        for l in range(nloc[s]):
            LC[0][s, assigned[s, l]] = -1
    for t in range(LC[3][0]):
        LC[1][LC[2][t]] = -1
    LC[3][0] = 0
    return status, g, counts, narr


# ====================================================================== settled-state helpers
def triple_of(counts):
    """the program triple of a monomorphic island (3, K counts), or None."""
    out = []
    for s in range(3):
        nz = np.nonzero(counts[s])[0]
        if len(nz) != 1:
            return None
        out.append(int(nz[0]))
    return tuple(out)


def outcome_of(arm, tr):
    return int(VEC[arm.joint(*tr)])


def classify_counts(arm, counts, N=N0):
    """the stored `_classify`: outcome with at least 0.95 of the encounter mass, 'member-mixed' (nout) if the fair pairs
    jointly carry >= 0.95, else 'other' (nout + 1).  Returns (class, efficiency)."""
    nz = [np.nonzero(counts[s])[0] for s in range(3)]
    dist = np.zeros(NOUT)
    N3 = float(N) ** 3
    for a in nz[0]:
        for b in nz[1]:
            for c in nz[2]:
                dist[VEC[arm.joint(a, b, c)]] += counts[0, a] * counts[1, b] * counts[2, c] / N3
    mx = dist.max(); arg = int(dist.argmax())
    mem = float(dist[ISMEM].sum()); eff = float((dist * TOT).sum())
    if mx >= 0.95:
        return arg, eff
    if mem >= 0.95:
        return NOUT, eff
    return NOUT + 1, eff


# ====================================================================== founding and annealing of one island
def arrival_times(rng, A, t1=200.0, t0=500.0):
    n = int(rng.poisson(A)) if A > 0 else 0
    u = np.sort(rng.random(n))
    return t1 + t0 * u / (1.0 - u)


def build_island(arm, rng, seed, A=0, N=N0, cap=20000, t1=200.0, t0=500.0, H=None):
    """one island: founding multinomial, Poisson(A) prior arrivals, relaxation to monomorphism.  Returns a dict with
    status (0 settled, 1 capped), the triple (or None), the final generation and the counts of arrivals delivered."""
    init = np.stack([rng.multinomial(N, arm.laws[s]) for s in range(3)]).astype(np.int64)
    arr = arrival_times(rng, A, t1, t0)
    if H is None:
        H = int((arr[-1] if len(arr) else 0.0)) + cap + 2
    ctx = arm.ctx()
    status, g, counts, narr = island_run(ctx, arm.lc(32 if A == 0 else 64), PAY, init, N, W, int(seed) % (2 ** 31), H, arr, arm.cum, True)
    tr = triple_of(counts) if status == 0 else None
    return dict(status=int(status), gen=int(g), triple=tr, narr=int(narr), counts=counts if status else None,
                last_arrival=float(arr[-1]) if len(arr) else 0.0)


# ====================================================================== the one-migrant kernel, exactly
def event_prob(arm, tr, s, x):
    """(fixation probability, new triple) for migrant program x into slot s of settled triple tr."""
    if x == tr[s]:
        return 0.0, tr
    o1, o2 = _others(s)
    ctx = arm.ctx()
    pr = PAY[int(jl(ctx, *map(np.int64, tr))), s]
    t2 = list(tr); t2[s] = x
    px = PAY[int(jl(ctx, *map(np.int64, t2))), s]
    return float(pfix(float(px - pr), float(N0), float(W))), tuple(t2)


# ====================================================================== the pool Monte Carlo of the jump chain
@njit(cache=True)
def chain_run(C, PAYt, VECt, EXCLt, pool, comp, events_total, cps, seed, N, w, hist, track_K, Kc, drift, first_loss,
              fair_ids):
    """Pool of settled islands pool (I, 3) program ids; I = n_components * comp.  One event: recipient uniform, donor
    uniform among the other islands of its component, slot uniform; the migrant fixes with the exact Moran
    probability.  cps: sorted checkpoint event counts (total events); hist[len(cps), NOUT] outcome counts recorded at
    each; Kc[len(cps), NOUT, NOUT, NOUT]: counts of (recipient class, donor class, new class) per event in the
    interval ending at that checkpoint (only when track_K); drift[len(cps), NOUT, 3]: [events that replaced the
    excluded slot's program without changing the class, replaced with class change, events with the excluded slot as
    the slot] per recipient outcome; first_loss[3]: event index of the first time the count of each fair pair hits
    zero (-1 if never).  Returns the number of events done and the pool (mutated)."""
    np.random.seed(seed)
    I = pool.shape[0]
    NOUTt = hist.shape[1]
    code = np.zeros(I, np.int64)
    oc = np.zeros(I, np.int64)
    cnt = np.zeros(NOUTt, np.int64)
    for i in range(I):
        code[i] = jl(C, pool[i, 0], pool[i, 1], pool[i, 2])
        oc[i] = VECt[code[i]]
        cnt[oc[i]] += 1
    for q in range(3):
        first_loss[q] = -1
        if cnt[fair_ids[q]] == 0:
            first_loss[q] = 0
    ncp = cps.shape[0]
    ci = 0
    e = 0
    # the Kc / drift interval index is the next checkpoint
    while ci < ncp:
        tgt = cps[ci]
        while e < tgt:
            i = np.random.randint(I)
            if comp < I:
                base = (i // comp) * comp
                j = base + np.random.randint(comp - 1)
                if j >= i: j += 1
            else:
                j = np.random.randint(I - 1)
                if j >= i: j += 1
            s = np.random.randint(3)
            x = pool[j, s]
            e += 1
            r = pool[i, s]
            ocj = oc[j]
            if x == r:
                if track_K:
                    Kc[ci, oc[i], ocj, oc[i]] += 1
                continue
            o1, o2 = _others(s)
            if s == 0:
                cx = jl(C, x, pool[i, 1], pool[i, 2])
            elif s == 1:
                cx = jl(C, pool[i, 0], x, pool[i, 2])
            else:
                cx = jl(C, pool[i, 0], pool[i, 1], x)
            d6 = int(round(6.0 * (PAYt[cx, s] - PAYt[code[i], s])))
            pf = PFT[d6 + 4] if (d6 >= -4 and d6 <= 4) else pfix(PAYt[cx, s] - PAYt[code[i], s], float(N), w)
            old = oc[i]
            ex = EXCLt[old]
            if ex >= 0 and s == ex:
                drift[ci, old, 2] += 1
            if pf > 1e-12 and np.random.random() < pf:
                pool[i, s] = x
                code[i] = cx
                nw = VECt[cx]
                if nw != old:
                    cnt[old] -= 1; cnt[nw] += 1
                    oc[i] = nw
                    for q in range(3):
                        if first_loss[q] < 0 and cnt[fair_ids[q]] == 0:
                            first_loss[q] = e
                    if ex >= 0 and s == ex:
                        drift[ci, old, 1] += 1
                else:
                    if ex >= 0 and s == ex:
                        drift[ci, old, 0] += 1
                if track_K:
                    Kc[ci, old, ocj, nw] += 1
            else:
                if track_K:
                    Kc[ci, old, ocj, old] += 1
        for z in range(NOUTt):
            hist[ci, z] = cnt[z]
        ci += 1
    return e


# ====================================================================== exact injection statistics
@njit(cache=True)
def exact_rates(C, PAYt, VECt, pool, rec_idx, don_idx, N, w, out, npair, outslot):
    """For each (recipient, donor) pair (rows of rec_idx, don_idx, equal length) and each slot (probability 1/3 each),
    the exact probability that the event changes the recipient's outcome class.  out[old, donor class, new] accumulates
    the pair's distribution over the new class (the 'stay' mass goes to new = old), npair[old, donor class] counts the
    pairs; outslot[old, slot, 0/1] accumulates, per slot, the probability that the event fixes and that it changes the
    class (summed over pairs)."""
    for n in range(rec_idx.shape[0]):
        i = rec_idx[n]; j = don_idx[n]
        ci = jl(C, pool[i, 0], pool[i, 1], pool[i, 2])
        old = VECt[ci]
        cj = jl(C, pool[j, 0], pool[j, 1], pool[j, 2])
        ocj = VECt[cj]
        ch = 0.0
        for s in range(3):
            x = pool[j, s]
            if x == pool[i, s]:
                continue
            if s == 0:
                cx = jl(C, x, pool[i, 1], pool[i, 2])
            elif s == 1:
                cx = jl(C, pool[i, 0], x, pool[i, 2])
            else:
                cx = jl(C, pool[i, 0], pool[i, 1], x)
            pf = pfix(PAYt[cx, s] - PAYt[ci, s], float(N), w)
            nw = VECt[cx]
            outslot[old, s, 0] += pf
            if nw != old:
                out[old, ocj, nw] += pf / 3.0
                ch += pf / 3.0
                outslot[old, s, 1] += pf
        out[old, ocj, old] += 1.0 - ch
        npair[old, ocj] += 1


# ====================================================================== class-level ODE
def ode_rates(K, x):
    """dx/dt for K[a, b, c] (prob. that a recipient of class a hit by a donor of class b becomes class c; rows over c sum
    to 1): inflow from other classes, outflow to other classes."""
    NC = K.shape[0]
    xb = x                                 # donor shares
    # flow[a, c] = sum_b x_b K[a, b, c]  (per unit of recipient share)
    flow = np.einsum('b,abc->ac', xb, K)
    off = flow.copy()
    np.fill_diagonal(off, 0.0)
    return x @ off - x * off.sum(axis=1)


def ode_integrate(K, x0, T_end, n_out=60):
    """integrate the class-level equation to T_end (events per island) with scipy's LSODA on a log time grid; returns
    times, trajectory (n_out, NC)."""
    from scipy.integrate import solve_ivp
    ts = np.unique(np.concatenate([[0.0], np.geomspace(1.0, T_end, n_out)]))
    sol = solve_ivp(lambda t, x: ode_rates(K, x), (0.0, T_end), x0, t_eval=ts, method='LSODA', rtol=1e-9, atol=1e-12)
    return sol.t, sol.y.T
