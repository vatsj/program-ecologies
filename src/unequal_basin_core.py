"""Core of the unequal-basin experiment (spec specs/2026-10-31-unequal-basin.md; notes notes/unequal-basin.md).

Extends the DSL machinery of many_islands.py with a divergence mask, so that the compute charge A_f (P_fail dollars
per divergent slot per encounter) can be applied in the weak evaluator:

  - `weak2`: the weak evaluator of dollar3._weak_into, additionally returning the mask of slots that stay bottom at the
    least fixed point (those play the null action (ALL, 2/3) = local action 8, and are charged).
  - the extended joint code  code2 = code + 729 * mask  (mask bit s = slot s divergent), at most 5832 values;
    PAY2[code2, s] = PAY[code, s] - P_fail * bit_s;   VEC2[code2] = VEC[code].
  - `island_run2`, `pool_build`: copies of many_islands.island_run / many_islands_run.build_pool over code2.  With
    P_fail = 0 they consume random numbers in the same order as the stored ones and give the same pools (tested).
  - helpers for supports, the S3 action on programs, and the lumping signature.

Nothing existing is edited.  Importable without side effects.
"""
import os, sys, math, time, zlib
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from numba import njit
import dollar3 as D
import many_islands as MI

ROOT = MI.ROOT
N0 = MI.N0
W = MI.W
SCR = os.environ.get('UB_SCRATCH', '/private/tmp/claude-501/-Users-jstav-code-program-ecologies/'
                     'eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/ub')
POOLS = os.path.join(SCR, 'pools')
OUTD = os.path.join(ROOT, 'runs', 'unequal_basin')
NCODE = 729
NMASK = 8


# ====================================================================== the weak evaluator with the divergence mask
@njit(cache=True)
def weak2(nat, atL, atJ, atA, tab, x0, x1, x2, val):
    """as dollar3._weak_into; returns the divergence mask (bit s: slot s still bottom at the fixed point); val gets the
    played actions (bottom replaced by 8)."""
    xs = (x0, x1, x2)
    new = np.empty(3, np.int64)
    for s in range(3):
        val[s] = -1
    for it in range(16):
        same = True
        for s in range(3):
            x = xs[s]
            k = nat[s, x]
            if k == 0:
                nv = tab[s, x, 0]
            else:
                idx = 0
                bot = False
                for t in range(k):
                    v = val[atJ[s, x, t]] if it > 0 else -1
                    if v < 0:
                        bot = True
                        break
                    if v == atA[s, x, t]:
                        idx |= 1 << t
                nv = -1 if bot else tab[s, x, idx]
            new[s] = nv
        for s in range(3):
            if new[s] != val[s]:
                same = False
            val[s] = new[s]
        if same and it > 0:
            break
    mask = 0
    for s in range(3):
        if val[s] < 0:
            val[s] = 8
            mask |= 1 << s
    return mask


@njit(cache=True)
def enc2(armi, nat, atL, atJ, atA, tab, PARTNER, x0, x1, x2, hist, val):
    """extended joint code of the encounter (x0, x1, x2): code + 729 * divergence mask; -1 if the modal evaluator did
    not converge (checked on the whole support)."""
    if armi == 0:
        D._modal_into(nat, atL, atJ, atA, tab, x0, x1, x2, hist, val)
        if val[0] == -9:
            return -1
        return val[0] * 81 + val[1] * 9 + val[2]
    m = weak2(nat, atL, atJ, atA, tab, x0, x1, x2, val)
    return val[0] * 81 + val[1] * 9 + val[2] + 729 * m


@njit(cache=True)
def jl2(C, x0, x1, x2):
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
            code = enc2(armi, nat, atL, atJ, atA, tab, PARTNER, x0, x1, x2, hist, val)
            if meta[0] * 10 < ((np.int64(1) << bits) * 7):
                keys[p] = key
                vals[p] = code
                meta[0] += 1
            return code
        p = (p + 1) & mask


def joint2(arm, x0, x1, x2):
    return int(jl2(arm.ctx(), np.int64(x0), np.int64(x1), np.int64(x2)))


def tables2(pfail):
    """PAY2 (5832, 3), VEC2 (5832,) for a per-divergent-slot charge pfail (dollars)."""
    PAY2 = np.zeros((NCODE * NMASK, 3))
    VEC2 = np.zeros(NCODE * NMASK, np.int64)
    for m in range(NMASK):
        PAY2[m * NCODE:(m + 1) * NCODE] = MI.PAY
        for s in range(3):
            if (m >> s) & 1:
                PAY2[m * NCODE:(m + 1) * NCODE, s] -= pfail
        VEC2[m * NCODE:(m + 1) * NCODE] = MI.VEC
    return np.ascontiguousarray(PAY2), VEC2


# ====================================================================== the island kernel over code2 (copy of island_run)
@njit(cache=True)
def codl2(C, LC, s, k, p, q):
    loc, Jl, touched, tc, L = LC
    if s == 0:
        a = k; b = p; c = q
    elif s == 1:
        a = p; b = k; c = q
    else:
        a = p; b = q; c = k
    la = loc[0, a]; lb = loc[1, b]; lc = loc[2, c]
    if la < 0 or lb < 0 or lc < 0:
        return jl2(C, a, b, c)
    idx = (la * L + lb) * L + lc
    v = np.int64(Jl[idx])
    if v >= 0:
        return v
    v = jl2(C, a, b, c)
    if tc[0] < touched.shape[0]:
        Jl[idx] = np.int16(v); touched[tc[0]] = idx; tc[0] += 1
    return v


@njit(cache=True)
def _fit2(C, LC, PAYt, counts, pres, npres, s, k):
    o1, o2 = MI._others(s)
    v = 0.0
    for t1 in range(npres[o1]):
        p = pres[o1, t1]
        for t2 in range(npres[o2]):
            q = pres[o2, t2]
            v += counts[o1, p] * counts[o2, q] * PAYt[codl2(C, LC, s, k, p, q), s]
    return v


@njit(cache=True)
def _replace2(C, LC, nloc, assigned, PAYt, counts, pres, npres, pos, F, act, apos, nact, s, child, victim):
    MI._assign(LC, nloc, assigned, s, child)
    counts[s, victim] -= 1
    if counts[s, victim] == 0:
        p = pos[s, victim]; last = pres[s, npres[s] - 1]
        pres[s, p] = last; pos[s, last] = p; pos[s, victim] = -1; npres[s] -= 1
    new = counts[s, child] == 0
    if new:
        pres[s, npres[s]] = child; pos[s, child] = npres[s]; npres[s] += 1
    counts[s, child] += 1
    o1, o2 = MI._others(s)
    for sa in (o1, o2):
        sb = o1 + o2 - sa
        for ta in range(npres[sa]):
            k = pres[sa, ta]
            v = 0.0
            for tb in range(npres[sb]):
                q = pres[sb, tb]
                if s < sb:
                    v += counts[sb, q] * (PAYt[codl2(C, LC, sa, k, child, q), sa] - PAYt[codl2(C, LC, sa, k, victim, q), sa])
                else:
                    v += counts[sb, q] * (PAYt[codl2(C, LC, sa, k, q, child), sa] - PAYt[codl2(C, LC, sa, k, q, victim), sa])
            F[sa, k] += v
    if new:
        F[s, child] = _fit2(C, LC, PAYt, counts, pres, npres, s, child)
    return MI._setact(s, npres[s] > 1, act, apos, nact)


@njit(cache=True)
def island_run2(C, LC, PAYt, init, N, w, seed, H, arr_t, cum, mono_stop):
    """many_islands.island_run over the extended code and PAY2 (same control flow, same random-number order)."""
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
                MI._assign(LC, nloc, assigned, s, k)
    for s in range(3):
        for t in range(npres[s]):
            k = pres[s, t]
            F[s, k] = _fit2(C, LC, PAYt, counts, pres, npres, s, k)
    NU = 3
    act = np.arange(NU); apos = np.arange(NU); nact = 0
    for u in range(NU):
        if npres[u] > 1:
            nact = MI._setact(u, True, act, apos, nact)
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
                    nact = _replace2(C, LC, nloc, assigned, PAYt, counts, pres, npres, pos, F, act, apos, nact, s, y, victim)
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
        child = MI._parent(F, counts, pres, npres, s, N2, w)
        r = np.random.randint(N); acc = 0; victim = pres[s, 0]
        for t in range(npres[s]):
            k = pres[s, t]; acc += counts[s, k]
            if r < acc:
                victim = k; break
        if victim == child:
            continue
        nact = _replace2(C, LC, nloc, assigned, PAYt, counts, pres, npres, pos, F, act, apos, nact, s, child, victim)
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


def crc(s):
    return zlib.crc32(s.encode()) & 0x7fffffff


def group_of(arm):
    return 'LM' if arm in ('L', 'M') else 'R'


def pool_file(arm, pfail, A, idx):
    tag = '%s_P%s_A%d_p%d' % (arm, ('%g' % pfail).replace('.', 'p'), A, idx)
    return os.path.join(POOLS, tag + '.npz'), os.path.join(OUTD, 'pool_' + tag + '.json')


def build_pool2(arm_name, pfail, A, idx, n_isl=16384, log=None, save=True):
    """n_isl independent islands.  The streams are those of many_islands_run.build_pool (founding and arrivals common to
    arms of one group and to every A, by island index; kernel seed the same function of (arm, A, idx, i)), so at pfail = 0 the
    pool equals the stored one and pfail = 0.1 is paired with it."""
    arm = MI.Arm(arm_name)
    arm.new_cache(24)
    PAY2, VEC2 = tables2(pfail)
    g = group_of(arm_name)
    triples = -np.ones((n_isl, 3), np.int16)
    status = np.zeros(n_isl, np.int8)
    gens = np.zeros(n_isl, np.int64)
    narr = np.zeros(n_isl, np.int32)
    t0 = time.time()
    capped = []
    mixed = []
    late = 0
    for i in range(n_isl):
        if i % 128 == 0:
            arm.maybe_flush(0.45)
        rf = np.random.default_rng(crc('mi-found|%s|%d|%d' % (g, idx, i)))
        ra = np.random.default_rng(crc('mi-arr|%s|%d|%d|%d' % (g, A, idx, i)))
        init = np.stack([rf.multinomial(MI.N0, arm.laws[s]) for s in range(3)]).astype(np.int64)
        arr = MI.arrival_times(ra, A)
        H = int(arr[-1] if len(arr) else 0.0) + 20002
        seed = crc('mi-kern|%s|%s|%d|%d|%d' % (arm_name, 'x', A, idx, i)) % (2 ** 31)
        st, gg, counts, na = island_run2(arm.ctx(), arm.lc(32 if A == 0 else 64), PAY2, init, MI.N0, MI.W, seed, H, arr,
                                         arm.cum, True)
        status[i] = st; gens[i] = gg; narr[i] = na
        if st != 0:
            st2, g2, counts2, _ = island_run2(arm.ctx(), arm.lc(32 if A == 0 else 64), PAY2, counts, MI.N0, MI.W, seed + 1,
                                              5000, np.empty(0), arm.cum, True)
            if st2 == 0:
                counts = counts2; st = 0; status[i] = 0; late += 1
            else:
                f1 = counts / MI.N0; f2 = counts2 / MI.N0
                lost = bool(((counts > 0) & (counts2 == 0)).any())
                band = bool((np.abs(f2 - f1) < 0.1).all()) and not lost
                status[i] = 2 if band else 3
                capped.append((i, 0, 0.0))
                if band:
                    for s_ in range(3):
                        for k_ in np.nonzero(counts2[s_])[0]:
                            mixed.append((i, s_, int(k_), int(counts2[s_, k_])))
        if st == 0:
            triples[i] = MI.triple_of(counts)
        if log and i % 1024 == 1023:
            print('%s P%g A%d p%d: %d islands, %.0f s, capped %d' % (arm_name, pfail, A, idx, i + 1, time.time() - t0, len(capped)),
                  file=log, flush=True)
    info = dict(arm=arm_name, pfail=pfail, A=A, idx=idx, n=n_isl, wall=time.time() - t0, capped=len(capped),
                n_mixed=int(len({m[0] for m in mixed})), n_drifting=int((status == 3).sum()), n_late=late,
                max_gen=int(gens.max()), flushes=int(arm.cache['meta'][1]))
    if save:
        os.makedirs(POOLS, exist_ok=True)
        os.makedirs(OUTD, exist_ok=True)
        pf, jf = pool_file(arm_name, pfail, A, idx)
        np.savez_compressed(pf, triples=triples, status=status, gens=gens, narr=narr,
                            mixed=np.array(mixed, dtype=np.int64).reshape(-1, 4))
        import json
        with open(jf, 'w') as f:
            json.dump(info, f)
    return info


def load_pool2(arm, pfail, A, idx):
    pf, _ = pool_file(arm, pfail, A, idx)
    z = np.load(pf)
    tr = z['triples'].astype(np.int64)
    ok = z['status'] == 0
    return tr[ok], dict(n=int(len(ok)), capped=int((~ok).sum()), mixed=z['mixed'])


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'pool':
        arm, pfail, A, idx = sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
        n = int(sys.argv[6]) if len(sys.argv) > 6 else 16384
        r = build_pool2(arm, pfail, A, idx, n, log=sys.stdout)
        print(r, flush=True)
