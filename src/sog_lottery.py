"""The social organization game under the seed lottery (spec specs/2026-10-06-social-organization-lottery.md,
reviewed in reviews/2026-10-06-social-organization-lottery-gpt-6.1-sol.md; predictions in
predictions/2026-10-06-social-organization-lottery.md).

The game, grammar, prior and evaluators are the union run's (src/union.py, quorum arm, boss n = 6, workers n = 10,
level 0) and the enforcement run's (src/union_enforcement.py: arms CC / RR, the replacement pool).  Classes are
re-lumped under each evaluator (exact behavioural lumping, as union_enforcement_run.run_part_c), class masses are
sums of the frozen function masses.

Seed lottery.  eps = 0.  I islands, three slot populations of N per island (boss, W1, W2).  Iid seeds per slot from
the slot's seed distribution (default: the length prior; the factorial reweights it).  Dynamics per slot: the island
Moran birth-death of src/rival_islands.py: a birth event picks an (island, slot) unit uniformly; with probability
m = mN / N the parent comes from a uniformly chosen other island's same slot; the parent is drawn on the source
island with weight count * exp(w * f), f the expected payoff of the class against the source island's other two
slot populations (one member of each per encounter, uniform draws: the expectation of the spec's "matched once with
a uniformly drawn individual of each other slot"); the victim is uniform in the recipient unit.  w = 0.3.  A
generation is 3 I N births.  Exact event skipping as in rival_islands: a birth in a monomorphic unit without a
migrant changes nothing; the number of such births before the next possibly-effective one is geometric.

Stopping (spec, [after review]).  mN > 0: the run stops when closure is verified against the globally surviving
classes of every slot: for every slot, all globally present classes give the same realized play key (a1, a2, whack1,
whack2, wage paid if anyone works) against every combination of globally present classes of the other two slots.
Then every encounter anywhere has one play, no neutral transition can change play against a surviving class, and at
eps = 0 nothing can change a payoff again.  mN = 0: every island locally closed in the same sense.  Otherwise the run
is horizon-censored.

    python3 src/sog_lottery.py classes             # build the class caches (runs/sog_lottery/*.npz, not committed)
    python3 src/sog_lottery.py static              # static tables -> runs/sog-lottery-static.{md,json}
    python3 src/sog_lottery.py validate            # kernel validation against src/union_abm.py
    python3 src/sog_lottery.py run --cell NAME [--procs 3]
    python3 src/sog_lottery.py report
"""
import argparse, json, math, os, sys, time
from collections import Counter, defaultdict
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from numba import njit
import union as U
import union_enforcement as E

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
OUT = os.path.join(RUNS, 'sog_lottery')
W = 0.3
GENS = 100000


# ------------------------------------------------------------------ classes
_BASE = {}


def base(arm='quorum'):
    if arm not in _BASE:
        d = U.build(arm=arm)
        _BASE[arm] = d
    return _BASE[arm]


def class_data(enf='CC', pool=0, c=0.5, arm='quorum', tie='whack'):
    """Behavioural classes under the evaluator (enf, pool, c, tie) for the worker grammar `arm`.
    Returns dict with Jc (KcB, KcW, KcW) int8, tagc, massB, massW (normalized length prior), repB, repW,
    named indices and class traits."""
    os.makedirs(OUT, exist_ok=True)
    rb, rw = E.ARMS[enf]
    key = '%s_%s' % (arm, enf) + (('_pool%d_c%g' % (pool, c)) if rb or rw else '')
    f = os.path.join(OUT, 'classes_%s.npz' % key)
    d = base(arm)
    P = d['P']
    if os.path.exists(f):
        z = np.load(f)
        C = {k: z[k] for k in z.files}
        for k in ('KcW', 'KcB'):
            C[k] = int(C[k])
    else:
        if rb or rw:
            J = E.tensor_e(*P.arrays(), U.TT, P.KB, P.KW, P.tag.astype(np.int64), rb, rw, pool, c, E.TIES[tie])
        else:
            J = U.tensor(*P.arrays(), U.TT, P.KB, P.KW)
        C = U.classes(d, J=J)
        C.pop('J')
        np.savez(f, **C)
    C['key'] = key
    C['nmw'] = {k: (int(C['cw'][v]) if v is not None else None) for k, v in U.named(P).items()}
    C['nmb'] = {k: int(C['cb'][v]) for k, v in U.named_boss(P).items()}
    C['srcW'] = [P.src_w(int(C['repW'][x])) for x in range(C['KcW'])]
    C['srcB'] = [P.src_b(int(C['repB'][b])) for b in range(C['KcB'])]
    # constant (non-conditional) classes: the representative has no atoms
    C['constW'] = np.array([len(d['P'].fw[int(C['repW'][x])][0]) == 0 for x in range(C['KcW'])])
    C['constB'] = np.array([len(d['P'].fb[int(C['repB'][b])][0]) == 0 for b in range(C['KcB'])])
    traits(C)
    return C


def key_of(j, t1, t2):
    """Realized play key: (a1, a2, whacked1, whacked2, wage paid if anyone works else 3)."""
    b, a1, a2 = j // 4, (j // 2) % 2, j % 2
    si, h = b // 3, b % 3
    w1 = int((h == 0 and a1 == 1) or (h == 2 and t1 == 1))
    w2 = int((h == 0 and a2 == 1) or (h == 2 and t2 == 1))
    sp = si if (a1 == 0 or a2 == 0) else 3
    return (((a1 * 2 + a2) * 2 + w1) * 2 + w2) * 4 + sp


KEYT = np.zeros((36, 2, 2), np.int64)
for _j in range(36):
    for _t1 in range(2):
        for _t2 in range(2):
            KEYT[_j, _t1, _t2] = key_of(_j, _t1, _t2)


def traits(C):
    """Class traits used for lineages and shares.
    Boss: strike-whacker = realizes a whack on a constant striker in some encounter with workers from
    {scab, always strike}^2; source-whacker = realizes a whack in some encounter with workers from
    {scab, always strike, militant, union}^2 and is not a strike-whacker; fair boss = offers s = 1/2 to (scab, scab).
    Worker: striker = the constant always-strike class; militant, union, scab = the named classes;
    conditional = non-constant class."""
    Jc = C['Jc']; tg = C['tagc']
    nm = C['nmw']
    sc, st = nm['scab'], nm['always strike']
    core = [sc, st]
    ext = [v for v in (sc, st, nm['militant'], nm['union']) if v is not None]
    KB = C['KcB']
    sw = np.zeros(KB, bool); anyw = np.zeros(KB, bool); fair = np.zeros(KB, bool); zerob = np.zeros(KB, bool)
    for b in range(KB):
        for x in ext:
            for y in ext:
                j = int(Jc[b, x, y]); h = (j // 4) % 3; a1 = (j // 2) % 2; a2 = j % 2
                wk = (h == 0 and (a1 or a2)) or (h == 2 and (tg[x] or tg[y]))
                if wk:
                    anyw[b] = True
                    if x in core and y in core and h == 0:
                        sw[b] = True
        j = int(Jc[b, sc, sc])
        fair[b] = (j // 4) // 3 == 2
        zerob[b] = (j // 4) // 3 == 0
    C['bt_strikewhack'] = sw
    C['bt_anywhack'] = anyw
    C['bt_fair'] = fair
    C['bt_zero'] = zerob
    KW = C['KcW']
    def one(i):
        v = np.zeros(KW, bool)
        if i is not None:
            v[i] = True
        return v
    C['wt_striker'] = one(st)
    C['wt_scab'] = one(sc)
    C['wt_militant'] = one(nm['militant'])
    C['wt_union'] = one(nm['union'])
    C['wt_cond'] = ~C['constW']
    C['bt_cond'] = ~C['constB']
    return C


BOSS_LINEAGES = ['strike-whacker', 'any-whacker', 'fair boss', 'conditional boss']
WORK_LINEAGES = ['striker', 'militant', 'union', 'conditional worker', 'scab']


def lineage_masks(C):
    LB = np.stack([C['bt_strikewhack'], C['bt_anywhack'], C['bt_fair'], C['bt_cond']]).astype(np.int64)
    LW = np.stack([C['wt_striker'], C['wt_militant'], C['wt_union'], C['wt_cond'], C['wt_scab']]).astype(np.int64)
    return LB, LW


# ------------------------------------------------------------------ per-joint-code tables
NST = 36
ST_NAMES = (['sum:' + s for s in U.SUMM] + ['ww:%s:%s' % (w, p) for w in U.WNAME for p in ('both work', 'one strikes', 'both strike')]
            + ['pol:' + h for h in U.HNAME] + ['pay:boss', 'pay:W1', 'pay:W2', 'production', 'whacks', 'strikers', 'surplus', 'replaced']
            + ['b:' + x for x in BOSS_LINEAGES] + ['w:' + x for x in WORK_LINEAGES])
assert len(ST_NAMES) == NST


def code_tables(c, pool):
    """T[j, t1, t2, :27]: per-encounter contributions to the island statistics (first 27 of ST_NAMES)."""
    PAY, REP = E.payoff_table_e(c, pool)
    T = np.zeros((36, 2, 2, 27))
    for j in range(36):
        b, a1, a2 = j // 4, (j // 2) % 2, j % 2
        si, h = b // 3, b % 3
        for t1 in range(2):
            for t2 in range(2):
                r = T[j, t1, t2]
                r[U.summary(j, t1, t2)] = 1
                r[7 + 3 * si + (a1 + a2)] = 1
                r[16 + h] = 1
                r[19:22] = PAY[j, t1, t2]
                r[22] = (1 - a1) + (1 - a2)
                wk = int((h == 0 and a1) or (h == 2 and t1)) + int((h == 0 and a2) or (h == 2 and t2))
                r[23] = wk
                r[24] = a1 + a2
                r[25] = E.surplus(j, t1, t2, PAY, REP)
                r[26] = REP[j, t1, t2]
    return PAY, T


# ------------------------------------------------------------------ kernel
@njit(cache=True)
def _pay(Jc, tagc, PAY, s, k, p, q):
    """payoff to slot s's class k against the other two slots' classes p, q (in slot order)."""
    if s == 0:
        b = k; x = p; y = q
    elif s == 1:
        b = p; x = k; y = q
    else:
        b = p; x = q; y = k
    return PAY[Jc[b, x, y], tagc[x], tagc[y], s]


@njit(cache=True)
def _others(s):
    if s == 0:
        return 1, 2
    if s == 1:
        return 0, 2
    return 0, 1


@njit(cache=True)
def _fit_full(Jc, tagc, PAY, counts, pres, npres, i, s, k):
    o1, o2 = _others(s)
    v = 0.0
    for t1 in range(npres[i, o1]):
        p = pres[i, o1, t1]
        for t2 in range(npres[i, o2]):
            q = pres[i, o2, t2]
            v += counts[i, o1, p] * counts[i, o2, q] * _pay(Jc, tagc, PAY, s, k, p, q)
    return v


@njit(cache=True)
def _parent(F, counts, pres, npres, i, s, N2, w):
    m = -1e300
    for t in range(npres[i, s]):
        k = pres[i, s, t]
        f = F[i, s, k] / N2
        if f > m: m = f
    tot = 0.0
    for t in range(npres[i, s]):
        k = pres[i, s, t]
        tot += counts[i, s, k] * np.exp(w * (F[i, s, k] / N2 - m))
    u = np.random.random() * tot; acc = 0.0
    for t in range(npres[i, s]):
        k = pres[i, s, t]
        acc += counts[i, s, k] * np.exp(w * (F[i, s, k] / N2 - m))
        if u <= acc:
            return k
    return pres[i, s, npres[i, s] - 1]


@njit(cache=True)
def _island_stats(Jc, tagc, T, LB, LW, counts, pres, npres, i, N, out):
    """out[:NST] <- expected per-encounter statistics on island i (uniform draw of one member per slot)."""
    for z in range(out.shape[0]):
        out[z] = 0.0
    N3 = float(N) * N * N
    for ta in range(npres[i, 0]):
        b = pres[i, 0, ta]
        for tb in range(npres[i, 1]):
            x = pres[i, 1, tb]
            for tc in range(npres[i, 2]):
                y = pres[i, 2, tc]
                p = counts[i, 0, b] * counts[i, 1, x] * counts[i, 2, y] / N3
                j = Jc[b, x, y]
                for z in range(27):
                    out[z] += p * T[j, tagc[x], tagc[y], z]
    for ta in range(npres[i, 0]):
        b = pres[i, 0, ta]
        for z in range(LB.shape[0]):
            if LB[z, b]:
                out[27 + z] += counts[i, 0, b] / N
    for s in (1, 2):
        for ta in range(npres[i, s]):
            x = pres[i, s, ta]
            for z in range(LW.shape[0]):
                if LW[z, x]:
                    out[27 + LB.shape[0] + z] += counts[i, s, x] / (2.0 * N)


@njit(cache=True)
def _closed(Jc, tagc, KEYT, cls0, n0, cls1, n1, cls2, n2):
    """Play identity: in every slot, all listed classes give the same play key against every combination of the
    other slots' listed classes."""
    for tb in range(n1):
        x = cls1[tb]
        for tc in range(n2):
            y = cls2[tc]
            k0 = KEYT[Jc[cls0[0], x, y], tagc[x], tagc[y]]
            for ta in range(1, n0):
                if KEYT[Jc[cls0[ta], x, y], tagc[x], tagc[y]] != k0:
                    return False
    for ta in range(n0):
        b = cls0[ta]
        for tc in range(n2):
            y = cls2[tc]
            k0 = KEYT[Jc[b, cls1[0], y], tagc[cls1[0]], tagc[y]]
            for tb in range(1, n1):
                x = cls1[tb]
                if KEYT[Jc[b, x, y], tagc[x], tagc[y]] != k0:
                    return False
        for tb in range(n1):
            x = cls1[tb]
            k0 = KEYT[Jc[b, x, cls2[0]], tagc[x], tagc[cls2[0]]]
            for tc in range(1, n2):
                y = cls2[tc]
                if KEYT[Jc[b, x, y], tagc[x], tagc[y]] != k0:
                    return False
    return True


@njit(cache=True)
def _setact(u, a, act, apos, nact):
    p = apos[u]
    if a and p >= nact:
        j = act[nact]; act[nact] = u; act[p] = j; apos[u] = nact; apos[j] = p; nact += 1
    elif (not a) and p < nact:
        nact -= 1; j = act[nact]; act[nact] = u; act[p] = j; apos[u] = nact; apos[j] = p
    return nact


@njit(cache=True)
def kern(Jc, tagc, PAY, T, KEYT, LB, LW, init, N, w, m, seed, checks, tsmax, half):
    """init[i, s, k]: initial counts.  checks: generation schedule (increasing, last = horizon).
    Returns status (1 globally closed, 5 every island locally closed (m = 0), 4 horizon-censored), stop generation,
    final counts, the per-island statistics at every check (nchk, I, NST), the time series of (striker share,
    strike-whacker share, any-whacker share) per island for generations <= tsmax, cumulative (whacks, strikers)
    per island, the time integral of the statistics over generations > half, lineage extinction generations
    (global, -1 = alive at stop), the number of migrant births and the number of checks done."""
    np.random.seed(seed)
    I = init.shape[0]; K = init.shape[2]
    counts = init.copy()
    pres = np.zeros((I, 3, K), np.int64); npres = np.zeros((I, 3), np.int64); pos = -np.ones((I, 3, K), np.int64)
    glob = np.zeros((3, K), np.int64)
    F = np.zeros((I, 3, K))
    for i in range(I):
        for s in range(3):
            for k in range(K):
                if counts[i, s, k] > 0:
                    pres[i, s, npres[i, s]] = k; pos[i, s, k] = npres[i, s]; npres[i, s] += 1
                    glob[s, k] += counts[i, s, k]
    for i in range(I):
        for s in range(3):
            for t in range(npres[i, s]):
                k = pres[i, s, t]
                F[i, s, k] = _fit_full(Jc, tagc, PAY, counts, pres, npres, i, s, k)
    NU = 3 * I
    act = np.arange(NU); apos = np.arange(NU); nact = 0
    for u in range(NU):
        if npres[u // 3, u % 3] > 1:
            nact = _setact(u, True, act, apos, nact)
    nchk = len(checks)
    stats = np.zeros((nchk, I, NST))
    ts = np.zeros((tsmax + 1, I, 3))
    cum = np.zeros((I, 2)); integ = np.zeros((I, NST))
    nlb = LB.shape[0]; nlw = LW.shape[0]
    ext = -np.ones(nlb + nlw, np.int64)
    tmp = np.zeros(NST)
    N2 = float(N) * N
    UN = NU * N
    total = checks[nchk - 1] * UN
    mm = m if I > 1 else 0.0
    b = 0
    ci = 0
    nextchk = checks[0] * UN
    status = 4; stop_gen = checks[nchk - 1]
    nmig = 0
    lastg = 0
    for i in range(I):
        _island_stats(Jc, tagc, T, LB, LW, counts, pres, npres, i, N, tmp)
        ts[0, i, 0] = tmp[27 + nlb + 0]; ts[0, i, 1] = tmp[27 + 0]; ts[0, i, 2] = tmp[27 + 1]
    for z in range(nlb):
        tot = 0
        for k in range(K):
            if LB[z, k]: tot += glob[0, k]
        if tot == 0: ext[z] = 0
    for z in range(nlw):
        tot = 0
        for k in range(K):
            if LW[z, k]: tot += glob[1, k] + glob[2, k]
        if tot == 0: ext[nlb + z] = 0
    cls0 = np.zeros(K, np.int64); cls1 = np.zeros(K, np.int64); cls2 = np.zeros(K, np.int64)
    while True:
        pa = (nact + (NU - nact) * mm) / NU
        if pa <= 0.0:
            G = total + 1
        elif pa >= 1.0:
            G = 0
        else:
            uu = np.random.random()
            G = int(np.log(1.0 - uu) / np.log(1.0 - pa))
        if b + G >= nextchk:
            b = nextchk
            g = checks[ci]
            dt = g - lastg
            for i in range(I):
                _island_stats(Jc, tagc, T, LB, LW, counts, pres, npres, i, N, tmp)
                for z in range(NST):
                    stats[ci, i, z] = tmp[z]
                cum[i, 0] += dt * tmp[23]; cum[i, 1] += dt * tmp[24]
                if g > half:
                    dth = g - max(lastg, half)
                    for z in range(NST):
                        integ[i, z] += dth * tmp[z]
                if g <= tsmax:
                    ts[g, i, 0] = tmp[27 + nlb + 0]; ts[g, i, 1] = tmp[27 + 0]; ts[g, i, 2] = tmp[27 + 1]
            for z in range(nlb):
                if ext[z] < 0:
                    tot = 0
                    for k in range(K):
                        if LB[z, k]: tot += glob[0, k]
                    if tot == 0: ext[z] = g
            for z in range(nlw):
                if ext[nlb + z] < 0:
                    tot = 0
                    for k in range(K):
                        if LW[z, k]: tot += glob[1, k] + glob[2, k]
                    if tot == 0: ext[nlb + z] = g
            lastg = g
            ci += 1
            if mm > 0.0:
                n0 = 0; n1 = 0; n2 = 0
                for k in range(K):
                    if glob[0, k] > 0:
                        cls0[n0] = k; n0 += 1
                    if glob[1, k] > 0:
                        cls1[n1] = k; n1 += 1
                    if glob[2, k] > 0:
                        cls2[n2] = k; n2 += 1
                if _closed(Jc, tagc, KEYT, cls0, n0, cls1, n1, cls2, n2):
                    status = 1; stop_gen = g; break
            else:
                allc = True
                for i in range(I):
                    if not _closed(Jc, tagc, KEYT, pres[i, 0], npres[i, 0], pres[i, 1], npres[i, 1], pres[i, 2], npres[i, 2]):
                        allc = False; break
                if allc:
                    status = 5; stop_gen = g; break
            if ci >= nchk:
                break
            nextchk = checks[ci] * UN
            continue
        # one possibly-effective birth
        b = b + G + 1
        if np.random.random() * pa * NU < nact:
            u = act[np.random.randint(nact)]
            mig = mm > 0.0 and np.random.random() < mm
        else:
            u = act[nact + np.random.randint(NU - nact)]
            mig = True
        i = u // 3; s = u % 3
        src = i
        if mig:
            src = np.random.randint(I - 1)
            if src >= i: src += 1
            nmig += 1
        child = _parent(F, counts, pres, npres, src, s, N2, w)
        r = np.random.randint(N); acc = 0; victim = pres[i, s, 0]
        for t in range(npres[i, s]):
            k = pres[i, s, t]; acc += counts[i, s, k]
            if r < acc:
                victim = k; break
        if victim == child:
            continue
        counts[i, s, victim] -= 1; glob[s, victim] -= 1
        if counts[i, s, victim] == 0:
            p = pos[i, s, victim]; last = pres[i, s, npres[i, s] - 1]
            pres[i, s, p] = last; pos[i, s, last] = p; pos[i, s, victim] = -1; npres[i, s] -= 1
        new = counts[i, s, child] == 0
        if new:
            pres[i, s, npres[i, s]] = child; pos[i, s, child] = npres[i, s]; npres[i, s] += 1
        counts[i, s, child] += 1; glob[s, child] += 1
        # update the other two slots' fitness sums (slot s's own sums do not depend on slot s)
        o1, o2 = _others(s)
        for sa in (o1, o2):
            sb = o1 + o2 - sa
            for ta in range(npres[i, sa]):
                k = pres[i, sa, ta]
                v = 0.0
                for tb in range(npres[i, sb]):
                    q = pres[i, sb, tb]
                    if s < sb:
                        v += counts[i, sb, q] * (_pay(Jc, tagc, PAY, sa, k, child, q) - _pay(Jc, tagc, PAY, sa, k, victim, q))
                    else:
                        v += counts[i, sb, q] * (_pay(Jc, tagc, PAY, sa, k, q, child) - _pay(Jc, tagc, PAY, sa, k, q, victim))
                F[i, sa, k] += v
        if new:
            F[i, s, child] = _fit_full(Jc, tagc, PAY, counts, pres, npres, i, s, child)
        nact = _setact(u, npres[i, s] > 1, act, apos, nact)
    return status, stop_gen, counts, stats[:ci], ts, cum, integ, ext, nmig, ci


# ------------------------------------------------------------------ the single-worker variant (secondary cell)
def single_data(c=0.5):
    """Boss + one worker.  Boss grammar: the union boss grammar with only the W1 atoms (BOX(W1 = work/strike));
    worker grammar: the union worker grammar without OTHER and QUORUM atoms (it reads only the boss), each with its
    own length prior at the union cutoffs (boss n = 6, worker n = 10).  Implemented on the three-slot kernel with a
    phantom W2 slot frozen at the scab on every island: no boss or worker atom reads W2, so the boss-W1 play does not
    depend on it, and the payoff table counts only W1 (u_B = (1 - s)[W1 works] - c [W1 whacked]; u_W2 = 0)."""
    f = os.path.join(OUT, 'classes_single.npz')
    LB = U.RoleLang(6, [(0, k) for k in (0, 1)], U.NB)
    fb, mb, cb, sb = LB.canon()
    LW = U.RoleLang(10, [(0, k) for k in range(12)], U.NW)
    fw, mw, cw, sw = LW.canon()
    P = U.Programs(fb, fw)
    ph = P.index_w[((), (0,))]
    if os.path.exists(f):
        z = np.load(f); J1 = z['J1']
    else:
        Bs = np.arange(P.KB, dtype=np.int64); Ws = np.arange(P.KW, dtype=np.int64)
        J1 = np.empty((P.KB, P.KW), np.int8)
        flag = np.ones((2, U.TT.shape[0]), np.bool_)
        for b in range(P.KB):
            for x in range(P.KW):
                J1[b, x] = U.encounter(*P.arrays(), U.TT, b, x, ph, flag)
        np.savez(f, J1=J1)
    assert (J1 >= 0).all()
    # lumping
    kw = {}; cwi = np.empty(P.KW, np.int64)
    for x in range(P.KW):
        cwi[x] = kw.setdefault(J1[:, x].tobytes(), len(kw))
    kb = {}; cbi = np.empty(P.KB, np.int64)
    for b in range(P.KB):
        cbi[b] = kb.setdefault(J1[b].tobytes(), len(kb))
    mw_ = mw / mw.sum(); mb_ = mb / mb.sum()
    KcW, KcB = len(kw), len(kb)
    massW = np.bincount(cwi, weights=mw_, minlength=KcW); massB = np.bincount(cbi, weights=mb_, minlength=KcB)
    repW = np.full(KcW, -1, np.int64); repB = np.full(KcB, -1, np.int64)
    for x in np.argsort(-mw_, kind='stable'):
        if repW[cwi[x]] < 0: repW[cwi[x]] = x
    for b in np.argsort(-mb_, kind='stable'):
        if repB[cbi[b]] < 0: repB[cbi[b]] = b
    J1c = J1[repB][:, repW]
    Jc = np.ascontiguousarray(np.repeat(J1c[:, :, None], KcW, axis=2))
    C = dict(Jc=Jc, tagc=np.zeros(KcW, np.int64), KcB=KcB, KcW=KcW, massB=massB, massW=massW, repB=repB, repW=repW, key='single')
    C['srcW'] = [P.src_w(int(repW[x])) for x in range(KcW)]
    C['srcB'] = [P.src_b(int(repB[b])) for b in range(KcB)]
    C['constW'] = np.array([len(fw[int(repW[x])][0]) == 0 for x in range(KcW)])
    C['constB'] = np.array([len(fb[int(repB[b])][0]) == 0 for b in range(KcB)])
    C['nmw'] = {'scab': int(cwi[ph]), 'always strike': int(cwi[P.index_w[((), (1,))]]),
                'militant': int(cwi[P.index_w[(((0, 2),), (0, 1))]]), 'union': None}
    C['nmb'] = {U.bname(b): int(cbi[P.index_b[((), (b,))]]) for b in range(U.NB)}
    C['phantom'] = int(cwi[ph])
    traits(C)
    # payoff and statistic tables counting W1 only
    PAY = np.zeros((36, 2, 2, 3)); T = np.zeros((36, 2, 2, 27))
    for j in range(36):
        b, a1 = j // 4, (j // 2) % 2
        si, h = b // 3, b % 3
        s = WAGES_[si]
        wk = int(h == 0 and a1 == 1)
        uB = (1 - s) * (1 - a1) - c * wk
        u1 = s * (1 - a1) - 1.0 * wk
        for t1 in range(2):
            for t2 in range(2):
                PAY[j, t1, t2] = (uB, u1, 0.0)
                r = T[j, t1, t2]
                r[U.summary(4 * b + 2 * a1, 0, 0)] = 1
                r[7 + 3 * si + a1] = 1
                r[16 + h] = 1
                r[19:22] = PAY[j, t1, t2]
                r[22] = 1 - a1; r[23] = wk; r[24] = a1; r[25] = uB + u1; r[26] = 0
    return C, PAY, T


WAGES_ = U.WAGES


# ------------------------------------------------------------------ seeds and cells
def checks_schedule(gens):
    c = list(range(1, min(gens, 2000) + 1)) + list(range(2025, min(gens, 10000) + 1, 25)) + \
        list(range(10100, gens + 1, 100))
    if not c or c[-1] != gens:
        c.append(gens)
    return np.array(c, np.int64)


def seed_dists(C, striker=None, boss='diverse', swap=None):
    """Seed distributions (pB, pW) over classes.  striker: constant-striker mass with the conditional-worker mass
    held at the prior's and the scab taking the rest (None = the prior).  boss: 'diverse' (the prior), 'hostile'
    (the committed strike-targeting boss at s = 0 only), 'mostly' (0.9 of it and 0.1 of the non-whacking boss at
    s = 0)."""
    pW = C['massW'].copy()
    nm = C['nmw']
    if striker is not None:
        cond = pW[~C['constW']].sum()
        others_const = [k for k in np.where(C['constW'])[0] if k not in (nm['scab'], nm['always strike'])]
        assert not others_const
        pW[nm['always strike']] = striker
        pW[nm['scab']] = 1.0 - striker - cond
    if swap is not None:
        # extra (not preregistered): move the constant striker's prior mass onto a wage-conditional striker
        if swap == 'militant':
            k = nm['militant']
        else:                      # 'refuser': strike iff provably s = 0, the heaviest such class
            Jc = C['Jc']; sc = nm['scab']
            def resp(x):
                return tuple((int(Jc[C['nmb']['(%s,none)' % s_], x, sc]) // 2) % 2 for s_ in ('0', '1/4', '1/2'))
            cands = [x for x in range(C['KcW']) if resp(x) == (1, 0, 0)]
            k = max(cands, key=lambda x: C['massW'][x])
        pW[k] += pW[nm['always strike']]; pW[nm['always strike']] = 0.0
    pB = C['massB'].copy()
    if boss == 'hostile':
        pB[:] = 0; pB[C['nmb']['(0,strike)']] = 1.0
    elif boss == 'mostly':
        pB[:] = 0; pB[C['nmb']['(0,strike)']] = 0.9; pB[C['nmb']['(0,none)']] = 0.1
    return pB / pB.sum(), pW / pW.sum()


def init_counts(rng, I, N, pB, pW):
    K = max(len(pB), len(pW))
    init = np.zeros((I, 3, K), np.int64)
    for i in range(I):
        init[i, 0, :len(pB)] = rng.multinomial(N, pB)
        init[i, 1, :len(pW)] = rng.multinomial(N, pW)
        init[i, 2, :len(pW)] = rng.multinomial(N, pW)
    return init


BASE_CELL = dict(enf='CC', pool=0, c=0.5, arm='quorum', N=100, I=16, mN=0.1, striker=None, boss='diverse', gens=GENS, runs=40)


def _cell(**kw):
    d = dict(BASE_CELL); d.update(kw); return d


# The factorial's (high, diverse) cell and the sweep's 0.48 cell are CC-main; the sweep's 0.12 cell is fact-lo-diverse.
CELLS = {
    'CC-main': _cell(),
    'RR-main': _cell(enf='RR'),
    'fact-hi-hostile': _cell(boss='hostile'),
    'fact-hi-mostly': _cell(boss='mostly'),
    'fact-lo-hostile': _cell(striker=0.12, boss='hostile'),
    'fact-lo-mostly': _cell(striker=0.12, boss='mostly'),
    'fact-lo-diverse': _cell(striker=0.12),
    'sweep-0.06': _cell(striker=0.06),
    'sweep-0.24': _cell(striker=0.24),
    'noQ-CC': _cell(arm='noquorum'),
    'CC-N400': _cell(N=400),
    'CC-I64': _cell(I=64),
    'CC-mN0': _cell(mN=0.0),
    'CC-mN1': _cell(mN=1.0),
    'CC-pool': _cell(pool=1),
    'CC-cont': _cell(gens=300000),
    'CC-c0.1': _cell(c=0.1),
    'RR-c0.1': _cell(enf='RR', c=0.1),
    'RR-N400': _cell(enf='RR', N=400),
    'noQ-RR': _cell(enf='RR', arm='noquorum'),
    # extras added after the first results (not preregistered; no verdict rests on them): the rare non-zero-wage
    # outcomes of the main cells at 400 runs, and the single-worker cell is separate (sog_single)
    'xref-CC': _cell(swap='refuser'),
    'xmil-CC': _cell(swap='militant'),
    'xref-mostly': _cell(swap='refuser', boss='mostly'),
    'xmil-mostly': _cell(swap='militant', boss='mostly'),
    'xref-hostile': _cell(swap='refuser', boss='hostile'),
    'CC-I64-cont': _cell(I=64, gens=300000),
    'single-CC': _cell(single=True),
    'single-CC-x400': _cell(single=True, runs=400),
    'CC-main-x400': _cell(runs=400),
    'RR-main-x400': _cell(enf='RR', runs=400),
    'noQ-CC-x400': _cell(arm='noquorum', runs=400),
}
SALT = 20261006


# ------------------------------------------------------------------ validation against src/union_abm.py
def _val_job(args):
    which, rep, gens_rec = args
    import union_abm as A
    C = class_data('CC', 0, 0.5, 'quorum')
    PAY, T = code_tables(0.5, 0)
    LB, LW = lineage_masks(C)
    nb, nw = C['nmb'], C['nmw']
    trip = [(nb['(0,strike)'], nw['always strike'], nw['scab']), (nb['(1/2,none)'], nw['scab'], nw['scab']),
            (nb['(0,none)'], nw['always strike'], nw['always strike']), (nb['(1/4,source)'], nw['union'], nw['militant'])]
    I, N, mN = 4, 20, 0.5
    out = []
    if which == 'abm':
        SUMM, WAGE, WHK = A.tables()
        Km = max(C['KcB'], C['KcW']); cdfs = np.ones((3, Km))
        init = np.array(trip, np.int64)
        for g in gens_rec:
            r_sum, r_sw, r_pay, r_dom, ov = A.run(np.ascontiguousarray(C['Jc']), C['tagc'].astype(np.int64), PAY, SUMM, WAGE, WHK, cdfs,
                                                  init, I, N, W, 0.0, mN, np.zeros(3), g, g, 1000 * rep + g)
            out.append(np.concatenate([r_sum[-1], r_pay[-1]], axis=1))
    else:
        K = max(C['KcB'], C['KcW'])
        init = np.zeros((I, 3, K), np.int64)
        for i, t in enumerate(trip):
            for s in range(3):
                init[i, s, t[s]] = N
        for g in gens_rec:
            r = kern(np.ascontiguousarray(C['Jc']), C['tagc'].astype(np.int64), PAY, T, KEYT, LB, LW, init, N, W, mN / N,
                     7919 * rep + g, np.array([g], np.int64), 0, g)
            st = r[3][-1]
            out.append(np.concatenate([st[:, :7], st[:, 19:22]], axis=1))
    return np.array(out)


def validate(reps=600, procs=3):
    """Same small cell, same initial islands, independent random streams: compare island-level means of the
    summary distribution and payoffs at two times (two-sample z per statistic)."""
    from multiprocessing import Pool
    gens_rec = (15, 150)
    with Pool(procs) as p:
        A_ = np.array(p.map(_val_job, [('abm', r, gens_rec) for r in range(reps)]))
        K_ = np.array(p.map(_val_job, [('kern', r, gens_rec) for r in range(reps)]))
    res = {}
    zs = []
    for gi, g in enumerate(gens_rec):
        a = A_[:, gi]; k = K_[:, gi]
        ma, mk = a.mean(0), k.mean(0)
        se = np.sqrt(a.var(0, ddof=1) / reps + k.var(0, ddof=1) / reps) + 1e-12
        z = (ma - mk) / se
        ok = se > 1e-9
        zs.extend(np.abs(z[ok]).tolist())
        res[str(g)] = dict(abm=ma.round(4).tolist(), kern=mk.round(4).tolist(), z=np.where(ok, z, 0).round(2).tolist())
    zs = np.array(zs)
    res['n_stats'] = int(len(zs)); res['max_abs_z'] = float(zs.max()); res['frac_abs_z_gt_2'] = float((zs > 2).mean())
    res['frac_abs_z_gt_3'] = float((zs > 3).mean())
    res['cols'] = U.SUMM + ['pay:boss', 'pay:W1', 'pay:W2']
    res['cell'] = dict(I=4, N=20, mN=0.5, w=W, c=0.5, reps=reps, islands='(0,strike)|striker|scab; (1/2,none)|scab|scab; '
                       '(0,none)|striker|striker; (1/4,source)|union|militant')
    return res


# ------------------------------------------------------------------ static tables
def payoff_rows(pool=0):
    rows = []
    PAYs = {c: E.payoff_table_e(c, pool) for c in (0.5, 0.1)}
    for j in range(36):
        b, a1, a2 = j // 4, (j // 2) % 2, j % 2
        si, h = b // 3, b % 3
        tags = [(0, 0)] if h != 2 else [(0, 0), (0, 1), (1, 0), (1, 1)]
        for t1, t2 in tags:
            P5, R5 = PAYs[0.5]; P1, _ = PAYs[0.1]
            nwk = int((h == 0 and a1) or (h == 2 and t1)) + int((h == 0 and a2) or (h == 2 and t2))
            rows.append(dict(s=U.WNAME[si], h=U.HNAME[h], a1='WS'[a1], a2='WS'[a2], tags='%d%d' % (t1, t2),
                             uB_c05=float(P5[j, t1, t2, 0]), uB_c01=float(P1[j, t1, t2, 0]), u1=float(P5[j, t1, t2, 1]),
                             u2=float(P5[j, t1, t2, 2]), production=(1 - a1) + (1 - a2) + (int(R5[j, t1, t2]) if pool else 0),
                             whacks=nwk, loss_workers=float(nwk), cost_boss_c05=0.5 * nwk, cost_boss_c01=0.1 * nwk,
                             summary=U.SUMM[U.summary(j, t1, t2)]))
    return rows


def slot_payoffs(C, PAY, pB, pW):
    """Expected payoff of every boss class against the worker seed (iid W1, W2), and of every worker class (in W1)
    against the boss seed and the W2 seed."""
    Jc = C['Jc'].astype(np.int64); tg = C['tagc'].astype(np.int64)
    PB = PAY[Jc, tg[None, :, None], tg[None, None, :], 0]
    P1 = PAY[Jc, tg[None, :, None], tg[None, None, :], 1]
    KB, KW = C['KcB'], C['KcW']
    fB = (PB.reshape(KB * KW, KW) @ pW).reshape(KB, KW) @ pW
    fW = pB @ (P1.reshape(KB * KW, KW) @ pW).reshape(KB, KW)
    return fB, fW, PB, P1


def replicator(C, PAY, T, pB, pW, gens=(0, 10, 25, 50, 100, 200, 500), w=W):
    """Deterministic per-generation map x' = x e^{w f} / <e^{w f}> in each slot simultaneously (infinite-N mean of
    the Moran kernel), from the seed composition."""
    Jc = C['Jc'].astype(np.int64); tg = C['tagc'].astype(np.int64)
    KB, KW = C['KcB'], C['KcW']
    code = (Jc * 4 + tg[None, :, None] * 2 + tg[None, None, :]).astype(np.uint8).ravel()
    P = [PAY[Jc, tg[None, :, None], tg[None, None, :], s].astype(np.float64) for s in range(3)]
    T2 = T.reshape(144, 27)
    xb, x1, x2 = pB.copy(), pW.copy(), pW.copy()
    out = {}
    LB, LW = lineage_masks(C)
    for g in range(max(gens) + 1):
        if g in gens:
            W3 = (xb[:, None, None] * x1[None, :, None] * x2[None, None, :]).ravel()
            st = np.bincount(code, weights=W3, minlength=144) @ T2
            rec = {ST_NAMES[z]: float(st[z]) for z in range(27)}
            for z, nmz in enumerate(BOSS_LINEAGES):
                rec['b:' + nmz] = float(xb[LB[z].astype(bool)].sum())
            for z, nmz in enumerate(WORK_LINEAGES):
                rec['w:' + nmz] = float(0.5 * (x1[LW[z].astype(bool)].sum() + x2[LW[z].astype(bool)].sum()))
            out[g] = rec
        fb = (P[0].reshape(KB * KW, KW) @ x2).reshape(KB, KW) @ x1
        f1 = xb @ (P[1].reshape(KB * KW, KW) @ x2).reshape(KB, KW)
        f2 = x1 @ (xb @ P[2].reshape(KB, KW * KW)).reshape(KW, KW)
        xb = xb * np.exp(w * (fb - fb.max())); xb /= xb.sum()
        x1 = x1 * np.exp(w * (f1 - f1.max())); x1 /= x1.sum()
        x2 = x2 * np.exp(w * (f2 - f2.max())); x2 /= x2.sum()
    return out


STATIC_SETS = [('CC-main', dict()), ('fact-lo-diverse', dict(striker=0.12)), ('sweep-0.06', dict(striker=0.06)),
               ('sweep-0.24', dict(striker=0.24)), ('fact-hi-mostly', dict(boss='mostly')), ('fact-lo-mostly', dict(striker=0.12, boss='mostly')),
               ('fact-hi-hostile', dict(boss='hostile')), ('fact-lo-hostile', dict(striker=0.12, boss='hostile'))]


def static(out_json, out_md):
    res = {}
    L = []
    L.append('# Static tables: the social organization game under the seed lottery\n')
    L.append('Generated by `python3 src/sog_lottery.py static` (spec `specs/2026-10-06-social-organization-lottery.md`).\n')
    # 1. payoff table
    rows = payoff_rows(0); rows_p = payoff_rows(1)
    res['payoff_table'] = rows; res['payoff_table_pool'] = rows_p
    L.append('## 1. Payoff table (one encounter; L = 1; tags matter only under source targeting)\n')
    L.append('u_B = (1 - s) x #working - c x #whacks; a working worker gets s, a striker 0, a whacked worker loses L = 1; '
             'production = #working; enforcement loss = c x #whacks (boss) + L x #whacks (workers). With the pool a whacked '
             'striker is replaced by an outside scab: the boss gains 1 - s per replaced striker and the outside scab earns s.\n')
    L.append('| s | h | W1 | W2 | tags | u_B (c=0.5) | u_B (c=0.1) | u_W1 | u_W2 | production | whacks | loss: workers | loss: boss c=0.5 / 0.1 | summary | u_B pool c=0.5 |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for r, rp in zip(rows, rows_p):
        L.append('| %s | %s | %s | %s | %s | %.2f | %.2f | %.2f | %.2f | %d | %d | %.1f | %.2f / %.2f | %s | %.2f |' % (
            r['s'], r['h'], r['a1'], r['a2'], r['tags'], r['uB_c05'], r['uB_c01'], r['u1'], r['u2'], r['production'],
            r['whacks'], r['loss_workers'], r['cost_boss_c05'], r['cost_boss_c01'], r['summary'], rp['uB_c05']))
    L.append('')
    # 2-4. per arm and seed set
    arms = [('CC', 0, 0.5, 'quorum'), ('CC', 0, 0.1, 'quorum'), ('CC', 1, 0.5, 'quorum'), ('RR', 0, 0.5, 'quorum'), ('CC', 0, 0.5, 'noquorum')]
    for enf, pool, c, arm in arms:
        C = class_data(enf, pool, c, arm)
        PAY, T = code_tables(c, pool)
        akey = '%s pool=%d c=%g %s' % (enf, pool, c, arm)
        res[akey] = {}
        L.append('## Arm %s (boss classes %d, worker classes %d)\n' % (akey, C['KcB'], C['KcW']))
        sets = STATIC_SETS if (enf, pool, c, arm) == ('CC', 0, 0.5, 'quorum') else STATIC_SETS[:1]
        for sname, kw in sets:
            pB, pW = seed_dists(C, **kw)
            fB, fW, PB, P1 = slot_payoffs(C, PAY, pB, pW)
            nb, nw = C['nmb'], C['nmw']
            r = {}
            r['boss_const'] = {k: float(fB[v]) for k, v in nb.items()}
            diff = {}
            for si, sn in enumerate(U.WNAME):
                bn = lambda h: '(%s,%s)' % (sn, h)
                if enf == 'CC':
                    diff['s=%s strike-none' % sn] = float(fB[nb[bn('strike')]] - fB[nb[bn('none')]])
                    diff['s=%s source-none' % sn] = float(fB[nb[bn('source')]] - fB[nb[bn('none')]])
            r['whack_minus_nonwhack'] = diff
            r['boss_all'] = [dict(cls=int(b), src=C['srcB'][b], mass=float(C['massB'][b]), seed=float(pB[b]), pay=float(fB[b]),
                                  strikewhack=bool(C['bt_strikewhack'][b]), anywhack=bool(C['bt_anywhack'][b])) for b in range(C['KcB'])]
            r['worker_all'] = [dict(cls=int(x), src=C['srcW'][x], mass=float(C['massW'][x]), seed=float(pW[x]), pay=float(fW[x]),
                                    tag=int(C['tagc'][x])) for x in range(C['KcW'])]
            r['worker_named'] = {k: (float(fW[v]) if v is not None else None) for k, v in nw.items()}
            mB = float(pB @ fB); mW = float(pW @ fW)
            r['mean_boss'] = mB; r['mean_worker'] = mW
            r['replicator'] = replicator(C, PAY, T, pB, pW)
            res[akey][sname] = r
            L.append('### Seed %s\n' % sname)
            L.append('Mean boss payoff against the seed %.3f; mean worker payoff %.3f.\n' % (mB, mW))
            L.append('Constant bosses against the iid worker seed: ' + ', '.join('%s %.3f' % (k, v) for k, v in r['boss_const'].items()) + '.\n')
            if diff:
                L.append('Whacking minus non-whacking at identical wage: ' + ', '.join('%s %+.3f' % (k, v) for k, v in diff.items()) + '.\n')
            L.append('Named workers against the boss seed (W2 iid from the worker seed): ' +
                     ', '.join('%s %.3f' % (k, v) for k, v in r['worker_named'].items() if v is not None) + '.\n')
            # conditional bosses: best and worst, and the strike-whacker / non-whacker split
            sw = C['bt_strikewhack']; aw = C['bt_anywhack']
            def wavg(mask):
                m = pB[mask].sum() if pB[mask].sum() > 0 else C['massB'][mask].sum()
                ww = pB[mask] if pB[mask].sum() > 0 else C['massB'][mask]
                return float((ww * fB[mask]).sum() / ww.sum()) if ww.sum() > 0 else float('nan')
            L.append('Seed-weighted mean payoff: strike-whackers %.3f (seed mass %.3f), other whackers %.3f (%.3f), non-whackers %.3f (%.3f).\n' % (
                wavg(sw), pB[sw].sum(), wavg(aw & ~sw), pB[aw & ~sw].sum(), wavg(~aw), pB[~aw].sum()))
            ordB = np.argsort(-fB)
            L.append('Top 5 boss classes by payoff against the seed: ' + '; '.join('`%s` %.3f (prior %.1e)' % (C['srcB'][b], fB[b], C['massB'][b]) for b in ordB[:5]) + '.\n')
            ordW = np.argsort(-fW)
            L.append('Top 5 worker classes: ' + '; '.join('`%s` %.3f (prior %.1e)' % (C['srcW'][x], fW[x], C['massW'][x]) for x in ordW[:5]) +
                     '. Bottom 3: ' + '; '.join('`%s` %.3f' % (C['srcW'][x], fW[x]) for x in ordW[-3:]) + '.\n')
            rep = r['replicator']
            cols = ['b:strike-whacker', 'b:any-whacker', 'b:fair boss', 'w:striker', 'w:scab', 'w:conditional worker',
                    'sum:fair', 'sum:intermediate', 'sum:zero wage', 'sum:strike', 'sum:scab split', 'sum:repression:strike', 'pay:boss', 'pay:W1']
            L.append('Replicator (deterministic per-generation map of the Moran kernel, w = 0.3) from the seed:\n')
            L.append('| gen | ' + ' | '.join(cols) + ' |')
            L.append('|---|' + '---|' * len(cols))
            for g, rec in rep.items():
                L.append('| %d | ' % g + ' | '.join('%.3f' % rec[cc] for cc in cols) + ' |')
            L.append('')
    json.dump(res, open(out_json, 'w'), indent=0, default=float)
    open(out_md, 'w').write('\n'.join(L) + '\n')
    return res


# ------------------------------------------------------------------ runs
TS_REC = (0, 5, 10, 25, 50, 100, 200, 500)
_CD = {}


def _cdata(p):
    key = (p['enf'], p['pool'] if p['enf'] != 'CC' else 0, p['c'] if p['enf'] != 'CC' else 0.5, p['arm'])
    if key not in _CD:
        _CD[key] = class_data(p['enf'], p['pool'] if p['enf'] != 'CC' else 0, p['c'], p['arm'])
    return _CD[key]


def run_seed(name, r):
    """Seed per (cell, run); the continuation reuses the main cell's seeds (its first 10^5 generations are the main
    cell's runs, since checks consume no random numbers)."""
    import zlib
    base_name = {'CC-cont': 'CC-main', 'CC-I64-cont': 'CC-I64'}.get(name, name)
    return (SALT + 1009 * (zlib.crc32(base_name.encode()) % 1000003) + r) % (2 ** 31)


def _comp_payoff(C, PAY, comp, s, k):
    """payoff of class k in slot s against an island composition comp = (dict per slot class->count)."""
    o1, o2 = {0: (1, 2), 1: (0, 2), 2: (0, 1)}[s]
    n1 = sum(comp[o1].values()); n2 = sum(comp[o2].values())
    v = 0.0
    for p_, a in comp[o1].items():
        for q_, bq in comp[o2].items():
            if s == 0:
                b, x, y = k, p_, q_
            elif s == 1:
                b, x, y = p_, k, q_
            else:
                b, x, y = p_, q_, k
            v += a * bq * PAY[int(C['Jc'][b, x, y]), int(C['tagc'][x]), int(C['tagc'][y]), s]
    return v / (n1 * n2)


def run_job(args):
    name, r = args
    p = CELLS[name]
    if p.get('single'):
        C, PAY, T = single_data(p['c'])
    else:
        C = _cdata(p)
        PAY, T = code_tables(p['c'], p['pool'])
    LB, LW = lineage_masks(C)
    pB, pW = seed_dists(C, p['striker'], p['boss'], p.get('swap'))
    seed = run_seed(name, r)
    rng = np.random.default_rng(seed)
    I, N, gens = p['I'], p['N'], p['gens']
    init = init_counts(rng, I, N, pB, pW)
    if p.get('single'):
        init[:, 2, :] = 0; init[:, 2, C['phantom']] = N
    chk = checks_schedule(gens)
    t0 = time.time()
    status, stop, counts, stats, ts, cum, integ, ext, nmig, ci = kern(
        np.ascontiguousarray(C['Jc']), C['tagc'].astype(np.int64), PAY, T, KEYT, LB, LW, init, N, W, p['mN'] / N,
        seed % (2 ** 31), chk, 500, gens // 2)
    wall = time.time() - t0
    if stop < ts.shape[0] - 1:
        ts[stop + 1:] = ts[stop]          # closed: the composition is recorded as frozen at the stop
    fin = stats[-1]
    H = gens; half = gens // 2
    rem = H - stop
    cumH = cum + rem * fin[:, [23, 24]]
    integH = integ + (H - max(stop, half)) * fin
    tavg = integH / (H - half)
    comp = []
    for i in range(I):
        comp.append([{int(k): int(counts[i, s, k]) for k in np.nonzero(counts[i, s])[0]} for s in range(3)])
    maj = [tuple(max(comp[i][s], key=comp[i][s].get) for s in range(3)) for i in range(I)]
    # reciprocal invasion payoffs between distinct terminal island play states (majority triples with distinct play)
    play = [int(KEYT[int(C['Jc'][m[0], m[1], m[2]]), int(C['tagc'][m[1]]), int(C['tagc'][m[2]])]) for m in maj]
    groups = {}
    for i in range(I):
        groups.setdefault(play[i], i)
    inv = []
    gl = sorted(groups.items())
    for ga, ia in gl:
        for gb, ib in gl:
            if ga == gb:
                continue
            row = []
            for s in range(3):
                res_mean = sum(cnt * _comp_payoff(C, PAY, comp[ia], s, k) for k, cnt in comp[ia][s].items()) / N
                row.append(_comp_payoff(C, PAY, comp[ia], s, maj[ib][s]) - res_mean)
            inv.append(dict(recipient=ia, donor=ib, d=[round(v, 4) for v in row]))
    lab = [int(np.argmax(fin[i, :7])) for i in range(I)]
    wage = [int(np.argmax([fin[i, 7 + 3 * w_:10 + 3 * w_].sum() for w_ in range(3)])) for i in range(I)]
    tsr = {str(g): ts[g].round(4).tolist() for g in TS_REC if g < ts.shape[0]}
    sw = ts[:, :, 1]
    dec100 = (sw[0] - sw[:101].min(0)).round(4).tolist()
    dec100_end = (sw[0] - sw[100]).round(4).tolist()
    rec = dict(cell=name, run=r, seed=seed, status=int(status), stop_gen=int(stop), nmig=int(nmig), wall=wall,
               final=fin.round(5).tolist(), label=lab, wage=wage, cum_whacks=cumH[:, 0].round(3).tolist(),
               cum_strikers=cumH[:, 1].round(3).tolist(), tavg=tavg.round(5).tolist(),
               ext={nm_: int(ext[z]) for z, nm_ in enumerate(['b:' + x for x in BOSS_LINEAGES] + ['w:' + x for x in WORK_LINEAGES])},
               ts=tsr, sw_decline100_min=dec100, sw_decline100_end=dec100_end,
               comp=[[sorted(cs.items()) for cs in ci_] for ci_ in comp], majority=[list(m) for m in maj],
               majority_src=[[C['srcB'][m[0]], C['srcW'][m[1]], C['srcW'][m[2]]] for m in maj], invasion=inv)
    return rec, ts.astype(np.float32)


def run_cell(name, procs=3):
    from multiprocessing import Pool
    p = CELLS[name]
    single_data(p["c"]) if p.get("single") else _cdata(p)       # build the class cache before forking
    t = time.time()
    jobs = [(name, r) for r in range(p['runs'])]
    with Pool(procs) as pool_:
        res = pool_.map(run_job, jobs, chunksize=1)
    recs = [x[0] for x in res]
    TS = np.stack([x[1] for x in res])
    json.dump(dict(cell=name, params=p, runs=recs, wall=time.time() - t), open(os.path.join(OUT, '%s.json' % name), 'w'))
    np.savez_compressed(os.path.join(OUT, 'ts_%s.npz' % name), ts=TS)
    st = Counter(r_['status'] for r_ in recs)
    labs = Counter(U.SUMM[l] for r_ in recs for l in r_['label'])
    print(name, 'status', dict(st), 'labels', dict(labs), 'wall %.0fs' % (time.time() - t), flush=True)


# ------------------------------------------------------------------ report
IDX = {n_: z for z, n_ in enumerate(ST_NAMES)}


def _ci(v):
    v = np.asarray(v, float)
    m = float(v.mean())
    se = float(v.std(ddof=1) / np.sqrt(len(v))) if len(v) > 1 else 0.0
    return m, 1.96 * se


def cell_summary(d):
    p = d['params']; runs = d['runs']
    R = len(runs); I = p['I']
    out = dict(params=p, runs=R)
    fin = np.array([r['final'] for r in runs])                  # (R, I, NST)
    lab = np.array([r['label'] for r in runs])                  # (R, I)
    out['status'] = dict(Counter(STATUS.get(r['status'], str(r['status'])) for r in runs))
    out['stop_gen'] = dict(median=float(np.median([r['stop_gen'] for r in runs])), max=int(max(r['stop_gen'] for r in runs)),
                           min=int(min(r['stop_gen'] for r in runs)))
    closed = np.array([r['status'] in (1, 5) for r in runs])
    def frac(mask_ri, sub=None):
        f = mask_ri.mean(1)
        if sub is not None:
            f = f[sub]
        if len(f) == 0:
            return None
        m, h = _ci(f)
        return dict(mean=round(m, 4), ci=round(h, 4))
    out['labels'] = {U.SUMM[k]: frac(lab == k) for k in range(7)}
    out['labels_closed_runs'] = {U.SUMM[k]: frac(lab == k, closed) for k in range(7)} if closed.any() else None
    out['labels_censored_runs'] = {U.SUMM[k]: frac(lab == k, ~closed) for k in range(7)} if (~closed).any() else None
    out['label_mass'] = {U.SUMM[k]: round(float(fin[:, :, k].mean()), 4) for k in range(7)}
    prod = fin[:, :, IDX['production']]
    wages = np.array([r['wage'] for r in runs])
    haswage = prod >= 0.05
    out['island_wage'] = {U.WNAME[w]: frac((wages == w) & haswage) for w in range(3)}
    out['island_wage']['none (production < 0.05)'] = frac(~haswage)
    sw = fin[:, :, IDX['b:strike-whacker']]; aw = fin[:, :, IDX['b:any-whacker']]
    fb = fin[:, :, IDX['b:fair boss']]; st = fin[:, :, IDX['w:striker']]
    wh = fin[:, :, IDX['whacks']]
    out['strike_whacker'] = dict(mean_share=round(float(sw.mean()), 4), present=frac(sw > 0), majority=frac(sw >= 0.5))
    out['any_whacker'] = dict(mean_share=round(float(aw.mean()), 4), present=frac(aw > 0), majority=frac(aw >= 0.5))
    out['realized_repression'] = frac(wh > 1e-3)
    out['realized_repression_label'] = frac((lab == 5) | (lab == 6))
    out['fair_boss_present'] = frac(fb > 0)
    out['strikers_surviving'] = frac(st > 0)
    out['scab_convergence'] = frac((lab == 2) & (st == 0))
    out['nonwhackers_establish'] = frac(sw < 0.5)
    dmin = np.array([r['sw_decline100_min'] for r in runs]); dend = np.array([r['sw_decline100_end'] for r in runs])
    out['early_decline'] = dict(ge03_min=frac(dmin >= 0.3), lt01_min=frac(dmin < 0.1), ge03_end=frac(dend >= 0.3),
                                lt01_end=frac(dend < 0.1), mean_min=round(float(dmin.mean()), 4), mean_end=round(float(dend.mean()), 4))
    ts = {g: np.array([r['ts'][g] for r in runs if g in r['ts']]) for g in runs[0]['ts']}
    out['ts_mean'] = {g: dict(striker=round(float(v[:, :, 0].mean()), 4), strike_whacker=round(float(v[:, :, 1].mean()), 4),
                              any_whacker=round(float(v[:, :, 2].mean()), 4)) for g, v in ts.items()}
    pay = fin[:, :, 19:21] if p.get("single") else fin[:, :, 19:22]
    out['payoff_vector'] = [round(float(x), 4) for x in pay.mean((0, 1))]
    out['production'] = round(float(prod.mean()), 4)
    out['whacks_per_encounter'] = round(float(wh.mean()), 5)
    out['surplus'] = round(float(fin[:, :, IDX['surplus']].mean()), 4)
    cw = np.array([r['cum_whacks'] for r in runs]); cs = np.array([r['cum_strikers'] for r in runs])
    out['cum_whack_cost_per_island'] = round(float(p['c'] * cw.mean()), 3)
    out['cum_worker_loss_per_island'] = round(float(cw.mean()), 3)
    out['cum_production_lost_per_island'] = round(float(cs.mean()), 3)
    # lineages
    lin = {}
    for k in runs[0]['ext']:
        e = np.array([r['ext'][k] for r in runs])
        alive = e < 0
        lin[k] = dict(alive_frac=round(float(alive.mean()), 3),
                      median_ext=(float(np.median(e[~alive])) if (~alive).any() else None),
                      max_ext=(int(e[~alive].max()) if (~alive).any() else None))
    out['lineages'] = lin
    # patchworks
    pw = []; pwl = []
    for r_, rr in enumerate(runs):
        ws = set(int(wages[r_, i]) for i in range(I) if haswage[r_, i])
        pw.append(len(ws) >= 2)
        ls = set(int(lab[r_, i]) for i in range(I) if lab[r_, i] in (0, 1, 2))
        pwl.append(len(ls) >= 2)
    out['patchwork_wage'] = round(float(np.mean(pw)), 4)
    out['patchwork_label'] = round(float(np.mean(pwl)), 4)
    out['distinct_play_states_mean'] = round(float(np.mean([len(set(map(tuple, r['majority']))) for r in runs])), 3)
    inv_n = 0; inv_pos = 0; inv_res = 0; inv_neu = 0
    for rr in runs:
        for e in rr['invasion']:
            inv_n += 1
            mx = max(e['d'])
            if mx > 1e-9: inv_pos += 1
            elif mx < -1e-9: inv_res += 1
            else: inv_neu += 1
    out['invasion_pairs'] = dict(n=inv_n, invadable=inv_pos, resistant=inv_res, neutral=inv_neu)
    # distribution
    tot = pay.sum(2)
    elig = tot > 1e-9
    with np.errstate(invalid='ignore', divide='ignore'):
        mins = np.where(elig, pay.min(2) / np.where(elig, tot, 1), np.nan)
    out['distribution'] = dict(eligible=round(float(elig.mean()), 4),
                               min_share_mean=(round(float(np.nanmean(mins)), 4) if elig.any() else None),
                               three_role_threshold=(round(float((mins[elig] >= 1 / 6 - 1e-12).mean()), 4) if elig.any() else None))
    tav = np.array([r['tavg'] for r in runs])[:, :, 19:(21 if p.get('single') else 22)]
    ttot = tav.sum(2, keepdims=True)
    with np.errstate(invalid='ignore', divide='ignore'):
        sh = np.where(ttot > 1e-9, tav / ttot, np.nan)
    out['time_avg_shares'] = [round(float(np.nanmean(sh[:, :, s])), 4) for s in range(tav.shape[2])]
    out['time_avg_payoffs'] = [round(float(tav[:, :, s].mean()), 4) for s in range(tav.shape[2])]
    out['wall_s'] = round(float(d.get('wall', 0)), 1)
    return out


STATUS = {1: 'closed', 5: 'local-closed (mN = 0)', 4: 'censored'}

CHAIN = {  # control (i): the union / enforcement runs' eps->0 chain (pi), nearest cell
    'CC c=0.5': 'chain (union run, N = 10²): fair 0.005, intermediate 0.022, zero wage 0.46, strike 0.13, scab split 0.38',
    'CC c=0.1': 'chain (union run, N = 10²): fair 0.005, intermediate 0.021, zero wage 0.49, strike 0.12, scab split 0.36-0.38',
    'RR c=0.5': 'chain (enforcement run, N = 10²): fair 0.004, intermediate 0.754, zero wage 0.21',
    'CC pool c=0.5': 'chain (enforcement run, N = 10³): fair 3e-5, intermediate 0.002, zero wage 0.986',
}


def report():
    cells = [c for c in CELLS if os.path.exists(os.path.join(OUT, '%s.json' % c))]
    S_ = {}
    for c in cells:
        S_[c] = cell_summary(json.load(open(os.path.join(OUT, '%s.json' % c))))
    json.dump(dict(cells=S_, chain_controls=CHAIN), open(os.path.join(RUNS, 'social-organization-lottery.json'), 'w'), indent=1)
    L = ['# The social organization game under the seed lottery: runs\n',
         'Spec `specs/2026-10-06-social-organization-lottery.md`; predictions `predictions/2026-10-06-social-organization-lottery.md`; '
         'code `src/sog_lottery.py`; static tables `runs/sog-lottery-static.md`; per-run records `runs/sog_lottery/<cell>.json`; '
         'summaries `runs/social-organization-lottery.json`. eps = 0, w = 0.3, 40 runs per cell; intervals are run-level 95% '
         '(mean ± 1.96 SE). Island fractions read at the closure stop or at the horizon (censored).\n']
    def f(x):
        if x is None: return '—'
        if isinstance(x, dict): return '%.3f ± %.3f' % (x['mean'], x['ci'])
        return '%.3f' % x
    def vec(v):
        return '(' + ', '.join('%.3f' % x for x in v) + ')'

    def pcell(c):
        p = S_[c]['params']
        return '%s c=%g%s N=%d I=%d mN=%g p_s=%s boss=%s %s gens=%d' % (p['enf'], p['c'], ' pool' if p['pool'] else '', p['N'], p['I'], p['mN'],
                                                                      'prior' if p['striker'] is None else p['striker'], p['boss'], p['arm'], p['gens'])
    L.append('## Cells\n')
    L.append('| cell | parameters | status | stop gen (median / max) | wall s |')
    L.append('|---|---|---|---|---|')
    for c in cells:
        s = S_[c]
        L.append('| %s | %s | %s | %.0f / %d | %.0f |' % (c, pcell(c), ', '.join('%s %d' % kv for kv in s['status'].items()),
                                                         s['stop_gen']['median'], s['stop_gen']['max'], s['wall_s']))
    L.append('\n## Island labels at stop/horizon (fraction of islands)\n')
    L.append('| cell | fair | intermediate | zero wage | strike | scab split | repression:strike | repression:source |')
    L.append('|---|---|---|---|---|---|---|---|')
    for c in cells:
        L.append('| %s | ' % c + ' | '.join(f(S_[c]['labels'][k]) for k in U.SUMM) + ' |')
    L.append('\n## Raw payoff vectors, production, enforcement (island means at stop/horizon), and distribution\n')
    L.append('| cell | payoffs (boss, W1, W2) | production | whacks / encounter | surplus | cum. whack cost / island | cum. worker loss / island | cum. production lost to strikes / island | eligible | min share | three-role threshold | time-avg shares (B, W1, W2) |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for c in cells:
        s = S_[c]; dd = s['distribution']
        L.append('| %s | %s | %.3f | %.4f | %.3f | %.2f | %.2f | %.1f | %.3f | %s | %s | %s |' % (
            c, vec(s['payoff_vector']), s['production'], s['whacks_per_encounter'], s['surplus'], s['cum_whack_cost_per_island'],
            s['cum_worker_loss_per_island'], s['cum_production_lost_per_island'], dd['eligible'],
            f(dd['min_share_mean']), f(dd['three_role_threshold']), vec(s['time_avg_shares'])))
    L.append('\n## Whackers, strikers, establishment\n')
    L.append('| cell | strike-whacker share | s-w present | s-w majority | any-whacker present | realized repression (whacks > 1e-3) | strikers surviving | scab convergence | non-whackers establish (s-w < 0.5) | early decline ≥ 0.3 (min / end) | early decline < 0.1 (min / end) |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|')
    for c in cells:
        s = S_[c]; e = s['early_decline']
        L.append('| %s | %.3f | %s | %s | %s | %s | %s | %s | %s | %s / %s | %s / %s |' % (
            c, s['strike_whacker']['mean_share'], f(s['strike_whacker']['present']), f(s['strike_whacker']['majority']),
            f(s['any_whacker']['present']), f(s['realized_repression']), f(s['strikers_surviving']), f(s['scab_convergence']),
            f(s['nonwhackers_establish']), f(e['ge03_min']), f(e['ge03_end']), f(e['lt01_min']), f(e['lt01_end'])))
    L.append('\n## Time series (first 500 generations; island means of the striker, strike-whacker and any-whacker shares)\n')
    gl = list(S_[cells[0]]['ts_mean'].keys())
    L.append('| cell | ' + ' | '.join('g=%s' % g for g in gl) + ' |')
    L.append('|---|' + '---|' * len(gl))
    for c in cells:
        L.append('| %s | ' % c + ' | '.join('%.2f / %.2f / %.2f' % (v['striker'], v['strike_whacker'], v['any_whacker'])
                                            for v in S_[c]['ts_mean'].values()) + ' |')
    L.append('\n## Lineage extinction (global; fraction of runs alive at stop/horizon, median extinction generation)\n')
    ln = list(S_[cells[0]]['lineages'].keys())
    L.append('| cell | ' + ' | '.join(ln) + ' |')
    L.append('|---|' + '---|' * len(ln))
    for c in cells:
        L.append('| %s | ' % c + ' | '.join('%.2f / %s' % (v['alive_frac'], ('%.0f' % v['median_ext']) if v['median_ext'] is not None else '—')
                                            for v in S_[c]['lineages'].values()) + ' |')
    L.append('\n## Patchworks and reciprocal invasion between terminal island states\n')
    L.append('| cell | runs with ≥ 2 island wages | runs with ≥ 2 wage labels | distinct majority triples / run | invasion pairs (n / invadable / resistant / neutral) | island wage 0 / 1/4 / 1/2 / none |')
    L.append('|---|---|---|---|---|---|')
    for c in cells:
        s = S_[c]; iv = s['invasion_pairs']; iw = s['island_wage']
        L.append('| %s | %.3f | %.3f | %.2f | %d / %d / %d / %d | %s / %s / %s / %s |' % (
            c, s['patchwork_wage'], s['patchwork_label'], s['distinct_play_states_mean'], iv['n'], iv['invadable'], iv['resistant'], iv['neutral'],
            f(iw['0']), f(iw['1/4']), f(iw['1/2']), f(iw['none (production < 0.05)'])))
    L.append('\n## Chain controls (ε→0 π of the union and enforcement runs)\n')
    for k, v in CHAIN.items():
        L.append('- %s: %s' % (k, v))
    open(os.path.join(RUNS, 'social-organization-lottery.md'), 'w').write('\n'.join(L) + '\n')
    return S_


# ------------------------------------------------------------------ CLI
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('what')
    ap.add_argument('--cell', default=None)
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--reps', type=int, default=600)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    if a.what == 'classes':
        for args in [('CC', 0, 0.5, 'quorum'), ('RR', 0, 0.5, 'quorum'), ('RR', 0, 0.1, 'quorum'), ('CC', 0, 0.5, 'noquorum'),
                     ('RR', 0, 0.5, 'noquorum')]:
            t = time.time(); C = class_data(*args)
            print(args, C['KcB'], C['KcW'], '%.0fs' % (time.time() - t), flush=True)
    elif a.what == 'static':
        static(os.path.join(RUNS, 'sog-lottery-static.json'), os.path.join(RUNS, 'sog-lottery-static.md'))
    elif a.what == 'validate':
        r = validate(a.reps, a.procs)
        json.dump(r, open(os.path.join(RUNS, 'sog-lottery-validate.json'), 'w'), indent=1)
        print(json.dumps({k: r[k] for k in ('n_stats', 'max_abs_z', 'frac_abs_z_gt_2', 'frac_abs_z_gt_3')}))
    elif a.what == 'run':
        run_cell(a.cell, a.procs)
    elif a.what == 'report':
        report()


if __name__ == '__main__':
    main()
