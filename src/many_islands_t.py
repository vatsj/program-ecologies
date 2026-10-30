"""The stable-set target in the Turing-complete arm under islands -> infinity before time (spec
specs/2026-10-29-many-islands-t.md; notes notes/many-islands-t.md; predictions predictions/2026-10-29-many-islands-t.md).

Arm T of churn_primary_t (27 programs per slot, L_T^code) in the exact island-to-infinity object of many_islands:
a settled island is a program triple (27^3 = 19,683 states); one migrant into slot s meets two monomorphic other slots,
so the event is a two-type constant-fitness Moran process with the closed-form fixation probability; the mean-field
(I -> infinity) dynamics is an exact ODE on the triple simplex, the finite-I dynamics an event-driven jump chain.

Pieces: tables (payoff, failed-read counts, forfeits per triple and slot, from executing L_T^code), charge A_f,
founding / annealing island simulator on a dense table, exact kernel tensor PF, the ODE (explicit adaptive and
backward Euler), the Jacobian on the rotation-non-invariant sectors, the finite-world chain.  Importable without side
effects; drivers in many_islands_t_run.py, report in many_islands_t_report.py.  Nothing existing is edited.
"""
import os, sys, math, time, hashlib
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from numba import njit
import lt_code as L
import churn_primary_t as CT
import many_islands as MI

ROOT = os.path.dirname(HERE)
SCR = os.environ.get('MIT_SCRATCH', '/private/tmp/claude-501/-Users-jstav-code-program-ecologies/'
                     'eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/mit')
NP = 27                      # programs per slot (the library; the 4 stub twins of churn_primary_t are excluded)
NT = NP ** 3
N0 = 100
W = MI.W                     # 0.3, acts on payoffs in dollars (stable_sets.Tables: PAY = outcome / 6)
PAY = MI.PAY
VEC = MI.VEC
NOUT = MI.NOUT
CATMAP = MI.CATMAP           # 0 F, 1 U, 2 G, 3 W, 4 D
EXCL = MI.EXCL
VIDX = MI.VIDX
NCLS = 5
CLS = ['F', 'U', 'G', 'W', 'D']
PAIRNAME = ['F0', 'F1', 'F2']

DOSES = ('0', 'lo', 'main', 'hi')


# ====================================================================== tables with failed-read counts
_COUNT = [0]


def _enter_sim_counted_factory(orig):
    def counted(k, thunk, key=None):
        r = orig(k, thunk, key)
        if isinstance(r, str) and r == 'TO':
            _COUNT[0] += 1
        return r
    return counted


from contextlib import contextmanager


@contextmanager
def counting():
    """install the failed-read counter around lt_code.enter_sim for the duration of the block (no edit of lt_code)."""
    orig = L.enter_sim
    L.enter_sim = _enter_sim_counted_factory(orig)
    try:
        yield
    finally:
        L.enter_sim = orig


def f_eval_counted(cat, a, b, c):
    """root evaluation of program a with next = b, prev = c: (cyclic action code 0-8, steps, failed reads, forfeit).
    A failed read is an `enter_sim` frame that closes on TO (nested frames closed by an enclosing expiry are not
    counted: the enclosing frame is the one that returns TO); a forfeit is a root that runs out of fuel, gets stuck
    or returns a non-number (it plays the timeout action 8)."""
    _COUNT[0] = 0
    v, st = L.evaluate(cat.init3(cat.terms[a], cat.terms[b], cat.terms[c]), CT.KR)
    ok = isinstance(v, int) and not isinstance(v, bool) and 0 <= v <= 8
    return (int(v) if ok else CT.NULL), int(st), int(_COUNT[0]), (0 if ok else 1)


def _build_counted(cat):
    code = np.empty((NP, NP, NP), np.int8)
    steps = np.empty((NP, NP, NP), np.int16)
    nto = np.empty((NP, NP, NP), np.int8)
    fo = np.empty((NP, NP, NP), np.int8)
    with counting():
        for p in range(NP):
            if cat.fam[p] == 'const':
                c, s, n, f = f_eval_counted(cat, p, 0, 0)
                code[p] = c; steps[p] = s; nto[p] = n; fo[p] = f
                continue
            for n_ in range(NP):
                for v_ in range(NP):
                    c, s, n, f = f_eval_counted(cat, p, n_, v_)
                    code[p, n_, v_] = c; steps[p, n_, v_] = s; nto[p, n_, v_] = n; fo[p, n_, v_] = f
    return code, steps, nto, fo


class Tabs:
    """Execution tables of the 27-program library: code[p, n, v], steps, nto (failed reads), fo (forfeit) of program p
    with next = n, prev = v; and the derived joint tables over triples (a, b, c) in slots (0, 1, 2)."""

    def __init__(self, cache_dir=None):
        self.cat = CT.TCat()
        self.names = self.cat.names[:NP]
        self.fam = self.cat.fam[:NP]
        self.is_reader = self.cat.is_reader[:NP].copy()
        cache_dir = cache_dir or os.path.join(SCR, 'cache')
        key = hashlib.md5(('|'.join(self.names) + str(CT.KS) + str(CT.KR) + 'counted1').encode()).hexdigest()[:12]
        path = os.path.join(cache_dir, 'tabs_%s.npz' % key)
        if os.path.exists(path):
            z = np.load(path)
            self.code, self.steps, self.nto, self.fo = z['code'], z['steps'], z['nto'], z['fo']
        else:
            self.code, self.steps, self.nto, self.fo = L.run_big(_build_counted, self.cat)
            os.makedirs(cache_dir, exist_ok=True)
            np.savez(path, code=self.code, steps=self.steps, nto=self.nto, fo=self.fo)
        self._joint()

    def _joint(self):
        """JT[a, b, c] joint action code (the dollar3 translation of churn_primary_t.TCat.joint_codes) and the per-slot
        arrays ST (steps), NTO (failed reads), FO (forfeits) with shape (27, 27, 27, 3)."""
        c0 = self.code.astype(np.int64)
        c1 = self.code.transpose(2, 0, 1).astype(np.int64)
        c2 = self.code.transpose(1, 2, 0).astype(np.int64)
        pi, d = c1 // 3, c1 % 3
        l1 = np.where(pi < 2, 3 * (1 - pi) + d, c1)
        self.JT = (c0 * 81 + l1 * 9 + c2).astype(np.int64)

        def st3(x):
            return np.stack([x.astype(np.int32), x.transpose(2, 0, 1).astype(np.int32), x.transpose(1, 2, 0).astype(np.int32)], axis=-1)
        self.ST, self.NTO, self.FO = st3(self.steps), st3(self.nto), st3(self.fo)
        self.OUT = VEC[self.JT]                        # outcome id of each triple
        self.CL = CATMAP[self.OUT].astype(np.int8)     # class 0..4
        self.PAIR = VIDX[self.OUT]                     # fair pair index (0..2) or -1
        self.GROSS = PAY[self.JT]                      # (27, 27, 27, 3) dollars

    def payoff(self, p_read, p_forf=None):
        """net payoff table (27,27,27,3) in dollars: gross - P_read * failed reads - P_forf * forfeit (A_f: p_forf = p_read)."""
        if p_forf is None:
            p_forf = p_read
        return self.GROSS - p_read * self.NTO - p_forf * self.FO


def seed_law(tabs, dose):
    """the seed law over the 27 programs (every slot): 'main' / 'lo' / 'hi' from churn_primary_t.FAMILY_WEIGHT, '0' the
    constants only (the readers' mass moved to the constants proportionally), 'ab:<name>' the main law with a reader
    family removed and its mass moved to the constants proportionally."""
    cat = tabs.cat
    if dose == '0':
        w = np.zeros(NP)
        ids = [i for i in range(NP) if tabs.fam[i] == 'const']
        w[ids] = 1.0 / len(ids)
        return w
    if dose.startswith('ab:'):
        w = cat.law('main')[:NP].copy()
        kind = dose[3:]
        if kind == 'So':
            rm = [i for i in range(NP) if tabs.fam[i] == 'single' and tabs.names[i][2] == 'o']
        elif kind == 'Sz':
            rm = [i for i in range(NP) if tabs.fam[i] == 'single' and tabs.names[i][2] == 'z']
        elif kind == 'D':
            rm = [i for i in range(NP) if tabs.fam[i] == 'two']
        elif kind == 'X':
            rm = [i for i in range(NP) if tabs.fam[i] == 'exploit']
        else:
            raise ValueError(dose)
        mass = w[rm].sum(); w[rm] = 0.0
        cs = [i for i in range(NP) if tabs.fam[i] == 'const']
        w[cs] += mass * w[cs] / w[cs].sum()
        return w / w.sum()
    w = cat.law(dose)[:NP].copy()
    return w / w.sum()


# ====================================================================== the exact kernel
@njit(cache=True)
def pfix(dpay, N, w):
    """fixation probability of one migrant in a two-type Moran process with constant payoff advantage dpay (dollars)
    (the stored closed form; many_islands.pfix)."""
    a = w * dpay
    if abs(a) < 1e-12:
        return 1.0 / N
    if a > 0:
        return (1.0 - math.exp(-a)) / (1.0 - math.exp(-a * N))
    b = -a
    return (1.0 - math.exp(-b)) * math.exp(-b * (N - 1.0)) / (1.0 - math.exp(-b * N))


@njit(cache=True)
def _build_pf(PT, N, w, PF):
    """PF[s, a0, a1, a2, y] = fixation probability of a slot-s migrant y into the settled triple (a0, a1, a2); 0 if y is
    the resident."""
    n = PT.shape[0]
    for a0 in range(n):
        for a1 in range(n):
            for a2 in range(n):
                for y in range(n):
                    # slot 0
                    if y != a0:
                        PF[0, a0, a1, a2, y] = pfix(PT[y, a1, a2, 0] - PT[a0, a1, a2, 0], N, w)
                    else:
                        PF[0, a0, a1, a2, y] = 0.0
                    if y != a1:
                        PF[1, a0, a1, a2, y] = pfix(PT[a0, y, a2, 1] - PT[a0, a1, a2, 1], N, w)
                    else:
                        PF[1, a0, a1, a2, y] = 0.0
                    if y != a2:
                        PF[2, a0, a1, a2, y] = pfix(PT[a0, a1, y, 2] - PT[a0, a1, a2, 2], N, w)
                    else:
                        PF[2, a0, a1, a2, y] = 0.0


def make_pf(PT, N=N0, w=W):
    PF = np.zeros((3, NP, NP, NP, NP))
    _build_pf(np.ascontiguousarray(PT), float(N), float(w), PF)
    return PF


# ====================================================================== island simulator on a dense table
@njit(cache=True)
def _pay(PT, s, k, p, q):
    if s == 0:
        return PT[k, p, q, 0]
    if s == 1:
        return PT[p, k, q, 1]
    return PT[p, q, k, 2]


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
def _fit(PT, counts, pres, npres, s, k):
    o1, o2 = _others(s)
    v = 0.0
    for t1 in range(npres[o1]):
        p = pres[o1, t1]
        for t2 in range(npres[o2]):
            q = pres[o2, t2]
            v += counts[o1, p] * counts[o2, q] * _pay(PT, s, k, p, q)
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
def _replace(PT, counts, pres, npres, pos, F, act, apos, nact, s, child, victim):
    """one birth-death replacement in slot s (victim -> child, victim != child): the stored kernel's update."""
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
                    v += counts[sb, q] * (_pay(PT, sa, k, child, q) - _pay(PT, sa, k, victim, q))
                else:
                    v += counts[sb, q] * (_pay(PT, sa, k, q, child) - _pay(PT, sa, k, q, victim))
            F[sa, k] += v
    if new:
        F[s, child] = _fit(PT, counts, pres, npres, s, child)
    return _setact(s, npres[s] > 1, act, apos, nact)


@njit(cache=True)
def island_run_t(PT, init, N, w, seed, H, arr_t, cum, mono_stop):
    """One island, three slot populations, no migration (many_islands.island_run on a dense payoff table PT[a, b, c, s]).
    init (3, K) counts; H the cap in generations (a generation is 3N slot-events); arr_t sorted arrival times in
    generations (annealed prior arrivals: slot uniform, program from cum[slot], victim a uniform resident).  Stops when
    every slot is monomorphic and no arrival is pending (mono_stop) or at H.  Returns (status, generation, counts,
    narr): status 0 settled, 1 capped at H."""
    np.random.seed(seed)
    K = init.shape[1]
    counts = init.copy()
    pres = np.zeros((3, K), np.int64); npres = np.zeros(3, np.int64); pos = -np.ones((3, K), np.int64)
    F = np.zeros((3, K))
    for s in range(3):
        for k in range(K):
            if counts[s, k] > 0:
                pres[s, npres[s]] = k; pos[s, k] = npres[s]; npres[s] += 1
    for s in range(3):
        for t in range(npres[s]):
            k = pres[s, t]
            F[s, k] = _fit(PT, counts, pres, npres, s, k)
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
                    nact = _replace(PT, counts, pres, npres, pos, F, act, apos, nact, s, y, victim)
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
        nact = _replace(PT, counts, pres, npres, pos, F, act, apos, nact, s, child, victim)
        if mono_stop and nact == 0 and narr >= na:
            status = 0
            break
    return status, g, counts, narr


def triple_of(counts):
    out = []
    for s in range(3):
        nz = np.nonzero(counts[s])[0]
        if len(nz) != 1:
            return None
        out.append(int(nz[0]))
    return tuple(out)


def arrival_times(rng, A, t1=200.0, t0=500.0):
    return MI.arrival_times(rng, A, t1, t0)


def build_island(PT, law, cum, rng, seed, A=0, N=N0, cap=20000, t1=200.0, t0=500.0):
    """founding multinomial(N, law) per slot, Poisson(A) annealed arrivals, relaxation to monomorphism (cap generations
    after the last arrival).  Returns dict(status, gen, triple, narr, counts_if_unsettled)."""
    init = np.stack([rng.multinomial(N, law) for _ in range(3)]).astype(np.int64)
    arr = arrival_times(rng, A, t1, t0)
    H = int((arr[-1] if len(arr) else 0.0)) + cap + 2
    status, g, counts, narr = island_run_t(PT, init, N, W, int(seed) % (2 ** 31), H, arr, cum, True)
    tr = triple_of(counts) if status == 0 else None
    return dict(status=int(status), gen=int(g), triple=tr, narr=int(narr), counts=counts if status else None)


def cum_of(law):
    c = np.cumsum(law)
    c = c / c[-1]
    return np.ascontiguousarray(np.stack([c, c, c]))
