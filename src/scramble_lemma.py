"""The scramble lemma and Claim A (spec specs/2026-10-05-scramble-lemma.md; predictions
predictions/2026-10-05-scramble-lemma.md; proofs notes/scramble-lemma.md).

    python3 src/spoiler_conditioned.py build      # class cache (n = 6, 9, 12), ~70 s
    python3 src/scramble_lemma.py static          # Claim A exhaustively at n = 6, 9, 12; examples by conj4's evaluator
    python3 src/scramble_lemma.py logs            # per-faker payoff tables along recorded scrambles (spoiler logs)
    python3 src/scramble_lemma.py neutral [--procs 3]   # neutral-lineage control
    python3 src/scramble_lemma.py report          # runs/scramble-lemma.{md,json}
"""
import argparse, gzip, json, math, os, sys, time
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import spoiler_conditioned as SC

ROOT = SC.ROOT; RUNS = SC.RUNS
OUT_JSON = os.path.join(RUNS, 'scramble-lemma.json')
PFAM = ['BOX(THEM(ME))', 'BOX1(THEM(ME))', 'BOX(THEM(THEM))', 'BOX1(THEM(THEM))', 'BOX(THEM(^C))', 'BOX1(THEM(^C))']


def _load():
    try:
        return json.load(open(OUT_JSON))
    except FileNotFoundError:
        return {}


def _save(key, val):
    res = _load(); res[key] = val
    json.dump(res, open(OUT_JSON, 'w'), indent=1)


def static_main(a):
    out = {}
    for n in SC.NS:
        d = SC.cdata(n); V = d['V']; mu = d['mu']; nm = d['names']; iC = d['iC']; iD = d['iD']; est = d['est']
        rows = {}
        for xs in PFAM:
            x = nm.index(xs)
            fk = SC.fakers_of(d, x)
            ne = [int(q) for q in fk if not est[q]]
            es = [int(q) for q in fk if est[q]]
            bad = [nm[q] for q in ne if V[q, iD] == 0 and V[q, iC] == 0]       # Claim A counterexamples
            typ = defaultdict(lambda: [0, 0.0])
            for q in ne:
                t = ('coopD' if V[q, iD] else '') + ('+' if V[q, iD] and V[q, iC] else '') + ('coopALLC' if V[q, iC] else '')
                typ[t][0] += 1; typ[t][1] += float(mu[q])
            rows[xs] = dict(x_is_est=bool(est[x]), mu_x=float(mu[x]), n_fakers=len(fk), mass_fakers=float(mu[fk].sum()),
                            n_nonest=len(ne), mass_nonest=float(mu[ne].sum()) if ne else 0.0,
                            n_est_fakers=len(es), mass_est_fakers=float(mu[es].sum()) if es else 0.0,
                            counterexamples=bad, nonest_types={k: dict(classes=v[0], mass=v[1]) for k, v in typ.items()},
                            all_fakers_selfC=bool(all(V[q, q] for q in fk)),
                            all_fakers_coopALLC=bool(all(V[q, iC] for q in fk)),
                            heaviest_nonest=[(nm[q], float(mu[q]), int(V[q, iD]), int(V[q, iC]), int(V[q, q]))
                                             for q in sorted(ne, key=lambda q: -mu[q])[:5]],
                            heaviest_est=[(nm[q], float(mu[q])) for q in sorted(es, key=lambda q: -mu[q])[:5]])
            print('n=%2d %-18s est %d mu %.2e | fakers %5d (%.2e) | non-est %5d (%.2e) types %s | est-fakers %4d (%.2e)'
                  ' | counterex %d | selfC %s coopALLC %s' % (
                      n, xs, est[x], mu[x], len(fk), rows[xs]['mass_fakers'], len(ne), rows[xs]['mass_nonest'],
                      {k: v[0] for k, v in typ.items()}, len(es), rows[xs]['mass_est_fakers'], len(bad),
                      rows[xs]['all_fakers_selfC'], rows[xs]['all_fakers_coopALLC']), flush=True)
        out[str(n)] = dict(classes=d['K'], P=rows)
    import conj4 as C4
    ex = {}
    d12 = SC.cdata(12)
    for qs in ('and(BOX(THEM(THEM)),not(BOX(THEM(^C))))', 'and(BOX(THEM(THEM)),BOXD1(THEM(^C)))',
               'BOX1(THEM(^not(BOX(THEM(ME)))))', 'and(BOX(THEM(THEM)),BOXD1(THEM(^D)))',
               'not(BOX(THEM(ME)))', 'BOX(THEM(^D))', 'or(BOXD1(THEM(ME)),BOX(THEM(^D)))'):
        q = C4.parse(qs); r = {}
        for xs in ('BOX(THEM(THEM))', 'BOX1(THEM(THEM))'):
            x = C4.parse(xs)
            r[xs] = dict(q_vs_x=C4.stable(q, x), x_vs_q=C4.stable(x, q))
        r['q_vs_q'] = C4.stable(q, q); r['q_vs_D'] = C4.stable(q, ('D',)); r['q_vs_C'] = C4.stable(q, ('C',))
        r['establisher'] = bool(r['q_vs_q'] == 1 and r['q_vs_D'] == 0)
        r['class_name_in_cache_n12'] = qs in d12['names']
        ex[qs] = r
        print(qs, r, flush=True)
    out['examples_conj4'] = ex
    _save('static', out)


def xcheck_main(a):
    """Independent evaluator: every faker q of every member of P at n = 12, and every q with V[x, q] = 1 for x in P,
    re-evaluated by conj4.play on (x, q), (q, x), (q, q), (q, D), (q, C); compared with the cache."""
    import conj4 as C4
    d = SC.cdata(12); V = d['V']; nm = d['names']; iC = d['iC']; iD = d['iD']
    t0 = time.time()
    res = {}
    Dp, Cp = ('D',), ('C',)
    for xs in PFAM:
        x = nm.index(xs); xp = C4.parse(xs)
        qs = np.nonzero(V[x, :] == 1)[0]          # everything x cooperates with (superset of its fakers)
        dis = 0; checked = 0; claimA_fail = 0
        for q in qs:
            qp = C4.parse(nm[q])
            vals = (C4.stable(xp, qp), C4.stable(qp, xp), C4.stable(qp, qp), C4.stable(qp, Dp), C4.stable(qp, Cp))
            ref = (V[x, q], V[q, x], V[q, q], V[q, iD], V[q, iC])
            checked += 1
            if tuple(int(v) for v in vals) != tuple(int(v) for v in ref):
                dis += 1
            faker = vals[0] == 1 and vals[1] == 0
            est = vals[2] == 1 and vals[3] == 0
            if faker and not est and vals[3] == 0 and vals[4] == 0:
                claimA_fail += 1
        res[xs] = dict(cooperated_with=int(checked), disagreements=dis, claimA_failures_conj4=claimA_fail)
        print(xs, res[xs], '%.0fs' % (time.time() - t0), flush=True)
    _save('xcheck_conj4_n12', res)


# ------------------------------------------------------------------ instrumented kernel
from numba import njit
NCATX = 7          # spoiler categories + 6 = ghost
TMAX = 2000        # generations: bounded stopping time tau = tau_A ^ TMAX ^ (local freeze)
CW = (1 - math.exp(-SC.W * 3)) / (SC.W * 3)
CW2 = (math.exp(SC.W * 3) - 1) / (SC.W * 3)


@njit(cache=True)
def _scramble(U, init, N, w, seed, iC, iD, q, ghost, cat, tmax, every, cw, Cw):
    """seeds_in_n._run (I = 1, m = 0) up to the first ALLC extinction, with the same RNG calls in the same order,
    plus a 'ghost' class (index `ghost`, or -1 for none) whose payoffs are q's but whose fitness per copy is pinned to the
    mean fitness of the non-ghost population (so its relative fitness r = f/F_bar - 1 is exactly 0).
    Tracks, for class q, Lam = -sum log(1 + r/N) and the integrals of B1-B3, all in generations, up to tau."""
    np.random.seed(seed)
    K = init.shape[0]
    counts = init.copy()
    paysum = np.zeros(K)
    pres = np.zeros(K, np.int64); npres = 0; pos = -np.ones(K, np.int64)
    for k in range(K):
        if counts[k] > 0:
            pres[npres] = k; pos[k] = npres; npres += 1
    for t in range(npres):
        j = pres[t]
        for t2 in range(npres):
            k = pres[t2]
            paysum[j] += counts[k] * U[j, k]
    Lam = 0.0; J1 = 0.0; Jpay = 0.0; Jb2 = 0.0; Jpos = 0.0; Jneg = 0.0; IA = 0.0; ID = 0.0
    dev = np.zeros(NCATX)            # integral of x_j (pi_j - pi_q) by category of j
    xint = np.zeros(NCATX)           # integral of x_cat
    tau = -1.0; status = 0
    fw = np.zeros(K)
    stop = False
    for g in range(tmax):
        for e in range(N):
            # ---- instrumentation on the state before the event
            mx = -1e300
            for t in range(npres):
                k = pres[t]
                if k == ghost: continue
                f = (paysum[k] - U[k, k]) / (N - 1)
                if f > mx: mx = f
            S = 0.0; kg = 0
            for t in range(npres):
                k = pres[t]
                if k == ghost:
                    kg = counts[k]; continue
                fw[k] = math.exp(w * ((paysum[k] - U[k, k]) / (N - 1) - mx))
                S += counts[k] * fw[k]
            fg = S / (N - kg) if kg > 0 else 0.0
            Fbar = (S + kg * fg) / N
            if counts[q] > 0:
                piq = (paysum[q] - U[q, q]) / (N - 1)
            else:
                v = 0.0
                for t in range(npres):
                    k = pres[t]; v += counts[k] * U[q, k]
                piq = v / (N - 1)
            fq = math.exp(w * (piq - mx))
            r = fq / Fbar - 1.0
            Lam -= math.log(1.0 + r / N)
            J1 += (1.0 - fq / Fbar) / N
            pibar = 0.0
            for t in range(npres):
                k = pres[t]
                if k == ghost:
                    pk = mx + math.log(fg) / w        # the ghost's effective log-fitness / w
                else:
                    pk = (paysum[k] - U[k, k]) / (N - 1)
                pibar += counts[k] * pk / N
                dev[cat[k]] += counts[k] * (pk - piq) / N / N
                xint[cat[k]] += counts[k] / N / N
            dlt = pibar - piq
            Jpay += w * dlt / N
            if dlt > 0:
                Jb2 += w * cw * dlt / N; Jpos += dlt / N
            else:
                Jb2 += w * Cw * dlt / N; Jneg -= dlt / N
            IA += counts[iC] / N / N; ID += counts[iD] / N / N
            # ---- the event, exactly as seeds_in_n._run with I = 1, m = 0
            np.random.randint(1)
            # _sample_parent (almost_all_seeds), with the ghost's weight pinned
            m2 = -1e300
            for t in range(npres):
                k = pres[t]
                if k == ghost: continue
                f = (paysum[k] - U[k, k]) / (N - 1)
                if f > m2: m2 = f
            tot = 0.0
            for t in range(npres):
                k = pres[t]
                if k == ghost:
                    tot += counts[k] * fg
                else:
                    f = (paysum[k] - U[k, k]) / (N - 1)
                    tot += counts[k] * np.exp(w * (f - m2))
            u = np.random.random() * tot; acc = 0.0
            child = pres[npres - 1]
            for t in range(npres):
                k = pres[t]
                if k == ghost:
                    acc += counts[k] * fg
                else:
                    f = (paysum[k] - U[k, k]) / (N - 1)
                    acc += counts[k] * np.exp(w * (f - m2))
                if u <= acc:
                    child = k; break
            uu = np.random.randint(N); acc2 = 0; victim = pres[0]
            for t in range(npres):
                k = pres[t]; acc2 += counts[k]
                if uu < acc2:
                    victim = k; break
            if victim == child:
                continue
            counts[victim] -= 1
            if counts[victim] == 0:
                p = pos[victim]; last = pres[npres - 1]
                pres[p] = last; pos[last] = p; pos[victim] = -1; npres -= 1
            new = counts[child] == 0
            if new:
                pres[npres] = child; pos[child] = npres; npres += 1
            counts[child] += 1
            for t in range(npres):
                j = pres[t]
                if new and j == child:
                    continue
                paysum[j] += U[j, child] - U[j, victim]
            if new:
                v = 0.0
                for t in range(npres):
                    k = pres[t]
                    v += counts[k] * U[child, k]
                paysum[child] = v
            if victim == iC and counts[iC] == 0:
                tau = g + e / N; status = 1; stop = True; break
        if stop: break
        if (g + 1) % every == 0:
            lo = 1e300; hi = -1e300
            for t in range(npres):
                a = pres[t]
                for t2 in range(npres):
                    b = pres[t2]
                    if U[a, b] < lo: lo = U[a, b]
                    if U[a, b] > hi: hi = U[a, b]
            if hi - lo < 1e-12:
                tau = g + 1.0; status = 2; break       # locally frozen with ALLC present
    if status == 0:
        tau = float(tmax); status = 3                 # censored at TMAX
    return status, tau, counts, Lam, J1, Jpay, Jb2, Jpos, Jneg, IA, ID, dev, xint


_KC = {}


def _setup(n):
    if n not in _KC:
        _KC[n] = SC.cdata(n)
    return _KC[n]


def run_local(d, init_full, N, seed, q, cat_full, ghost_k=0):
    """One island on the seed's support plus ALLC, D and q.  ghost_k > 0: ghost_k copies of a ghost class appended
    (payoffs of q, fitness pinned to the mean), taken from init_full's q entry."""
    sup = np.union1d(np.nonzero(init_full)[0], [d['iC'], d['iD'], q]).astype(np.int64)
    # keep class order = cdata order (as SC.simulate), so the RNG stream matches the spoiler kernel
    V = d['V'][np.ix_(sup, sup)].astype(np.int64)
    U = PDP_[V, V.T]
    loc = {int(g): j for j, g in enumerate(sup)}
    init = init_full[sup].astype(np.int64)
    cat = cat_full[sup].astype(np.int64)
    ghost = -1
    if ghost_k > 0:
        K = len(sup)
        U2 = np.zeros((K + 1, K + 1)); U2[:K, :K] = U
        qi = loc[q]
        U2[K, :K] = U[qi, :]; U2[:K, K] = U[:, qi]; U2[K, K] = U[qi, qi]
        U = U2
        init = np.append(init, ghost_k); init[qi] -= ghost_k
        cat = np.append(cat, 6)
        ghost = K
    U = np.ascontiguousarray(U)
    out = _scramble(U, init, N, SC.W, seed, loc[d['iC']], loc[d['iD']], loc[q], ghost, cat, TMAX, SC.EVERY, CW, CW2)
    st, tau, counts, Lam, J1, Jpay, Jb2, Jpos, Jneg, IA, ID, dev, xint = out
    cnt = {int(sup[j]): int(counts[j]) for j in range(len(sup)) if counts[j] > 0}
    return dict(status=int(st), tau=round(float(tau), 3), kq=int(counts[loc[q]]), kg=int(counts[ghost]) if ghost >= 0 else -1,
                Lam=float(Lam), J1=float(J1), Jpay=float(Jpay), Jb2=float(Jb2), Jpos=float(Jpos), Jneg=float(Jneg),
                IA=float(IA), ID=float(ID), dev=[float(x) for x in dev], xint=[float(x) for x in xint], final=cnt)


PDP_ = SC.PDP
DOSES = {100: (1, 3), 400: (1, 3, 10)}
NBG = 1000


def frc_setup(n, N, pi, rep, salt=SC.SALT_FRC):
    """The spoiler run's forced background and treatment-(b) insertion, rebuilt with the same RNG calls."""
    d = _setup(n); mu = d['mu']
    P = SC.forced_pairs(n)[pi]
    t, q = P['t'], P['q']
    rng = np.random.default_rng([n, N, pi, rep, salt])
    bg = rng.multinomial(N, mu).astype(np.int64)
    slots = np.repeat(np.arange(d['K']), bg)
    perm = rng.permutation(N)
    ss = 1000003 * rep + 7 * N + 13 * n + 101 * pi + salt % 100000
    cat = np.full(d['K'], 5, np.int64)
    cat[d['est']] = 4; cat[d['iC']] = 3; cat[d['iD']] = 2; cat[q] = 1; cat[t] = 0
    return d, P, t, q, bg, slots, perm, ss, cat


def lemma_job(j):
    """One forced background: treatment (b) with k inserted fakers, and the matched neutral control (k inserted ghosts
    in the same slots, same seed, same stopping rule), for every dose."""
    n, N, pi, rep = j
    d, P, t, q, bg, slots, perm, ss, cat = frc_setup(n, N, pi, rep)
    out = dict(n=n, N=N, pair=pi, rep=rep, bg_q=int(bg[q]), bg_t=int(bg[t]), xA0=float(bg[d['iC']] / N),
               xD0=float(bg[d['iD']] / N), runs={})
    for k in DOSES[N]:
        first = slots[perm[:k]]; second = slots[perm[10:10 + k]]
        init = bg.copy()
        np.subtract.at(init, first, 1); init[t] += k
        np.subtract.at(init, second, 1); init[q] += k
        xA = init[d['iC']] / N; xD = init[d['iD']] / N
        rf = run_local(d, init, N, ss, q, cat)
        rg = run_local(d, init, N, ss, q, cat, ghost_k=k)
        for r in (rf, rg):
            r['kt'] = int(r['final'].get(t, 0)); del r['final']
        out['runs'][str(k)] = dict(k0q=int(init[q]), xA=float(xA), xD=float(xD), faker=rf, ghost=rg)
    return out


def check_main(a):
    """The instrumented kernel reproduces the spoiler run's treatment (b) draw for draw up to tC: compare tC and the
    target's and faker's extinction times with the recorded rows (forced, first backgrounds of each cell)."""
    rows = json.load(gzip.open(SC.ROWS_FRC, 'rt'))
    by = {(r['n'], r['N'], r['pair'], r['rep']): r for r in rows}
    ok = 0; bad = 0; skipped = 0
    for n in SC.NS:
        for N in (100, 400):
            for pi in range(7):
                for rep in range(3):
                    r = by[(n, N, pi, rep)]
                    d, P, t, q, bg, slots, perm, ss, cat = frc_setup(n, N, pi, rep)
                    k = 1
                    first = slots[perm[:k]]; second = slots[perm[10:10 + k]]
                    init = bg.copy(); np.subtract.at(init, first, 1); init[t] += k
                    np.subtract.at(init, second, 1); init[q] += k
                    rf = run_local(d, init, N, ss, q, cat)
                    rec = r['out']['b1']
                    tC = rec[9]
                    if rf['status'] != 1 or tC < 0:
                        skipped += 1; continue
                    same = abs(round(rf['tau'], 2) - tC) < 0.011
                    # faker alive at tC per the record: its extinction time is -1 (never) or > tC
                    alive_rec = rec[12] < 0 or rec[12] > tC
                    same &= (rf['kq'] > 0) == alive_rec
                    ok += same; bad += (not same)
                    if not same:
                        print('DIFF', n, N, pi, rep, rf['tau'], tC, rf['kq'], rec[12])
    print('same %d, different %d, skipped (frozen/censored or no ALLC) %d' % (ok, bad, skipped))
    _save('check_kernel', dict(same=ok, different=bad, skipped=skipped))


ROWS = os.path.join(RUNS, 'scramble-lemma-rows.json.gz')


def _warm():
    for n in SC.NS: _setup(n)


def run_main(a):
    from multiprocessing import Pool
    nb = a.nbg
    jobs = [(n, N, pi, rep) for n in SC.NS for N in (100, 400) for pi in range(7) for rep in range(nb)]
    print('%d jobs' % len(jobs), flush=True)
    rows = []; t0 = time.time()
    with Pool(a.procs, initializer=_warm) as pool:
        for i, r in enumerate(pool.imap_unordered(lemma_job, jobs, chunksize=10)):
            rows.append(r)
            if (i + 1) % 5000 == 0:
                print('%d / %d, %.0fs' % (i + 1, len(jobs), time.time() - t0), flush=True)
    rows.sort(key=lambda r: (r['n'], r['N'], r['pair'], r['rep']))
    if a.nbg >= 100:
        with gzip.open(ROWS, 'wt') as f:
            json.dump(rows, f)
    print('done %d in %.0fs' % (len(rows), time.time() - t0), flush=True)


def _wilson(k, n, z=1.96):
    if n == 0: return (float('nan'),) * 3
    p = k / n; den = 1 + z * z / n; c = (p + z * z / (2 * n)) / den; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return p, max(0.0, c - h), min(1.0, c + h)


def _percopy(qk, k):
    return 1 - (1 - qk) ** (1.0 / k) if 0 <= qk < 1 else 1.0


GRID = np.concatenate([[-np.inf], np.arange(0.0, 8.01, 0.1), [np.inf]])


def b1_bound(lam, k0):
    """Binned B1 bound on P(alive at tau): sum_i min(P(Lam in [a_i, a_i+1)), E[k0] e^{-a_i}); and the single-level
    bound inf_L [P(Lam < L) + E[k0] e^{-L}]."""
    lam = np.asarray(lam); Ek = float(np.mean(k0)); n = len(lam)
    tot = 0.0
    for lo, hi in zip(GRID[:-1], GRID[1:]):
        p = np.mean((lam >= lo) & (lam < hi))
        tot += min(p, Ek * math.exp(-lo)) if np.isfinite(lo) else p
    best = min(np.mean(lam < L) + Ek * math.exp(-L) for L in GRID[1:-1])
    return min(1.0, tot), min(1.0, best)


TYPES = {0: 'disadvantaged', 1: 'disadvantaged', 2: 'neutral', 3: 'neutral', 4: 'neutral', 5: 'neutral', 6: 'advantaged'}


def combined_main(a):
    """The combined per-island bound on the spoiler run's forced (b) islands (k = 1): P(target survives) >=
    rho~ - P(F)·h+, with rho~ = P(A)·P(surv | A, F^c), h = P(surv | A, F^c) - P(surv | A, F); P(F) bounded by B1
    (single-level, from this run's Lambda distribution) or measured.  Target survival = the spoiler's 'target_surv'."""
    frc = json.load(gzip.open(SC.ROWS_FRC, 'rt'))
    L = _load()['lemma']
    out = {}
    for N in (100, 400):
        for typ in ('disadvantaged', 'neutral', 'advantaged'):
            for n in SC.NS:
                R = [r for r in frc if r['N'] == N and r['n'] == n and TYPES[r['pair']] == typ]
                rec = [r['out']['b1'] for r in R]
                rec = [x for x in rec if x[9] >= 0]           # tC defined
                A = np.array([(x[11] < 0 or x[11] > x[9]) for x in rec]); F = np.array([(x[12] < 0 or x[12] > x[9]) for x in rec])
                S = np.array([bool(x[1]) for x in rec])
                pA = A.mean(); pS_AFc = S[A & ~F].mean(); pS_AF = S[A & F].mean() if (A & F).sum() else float('nan')
                h = pS_AFc - pS_AF if (A & F).sum() else pS_AFc
                rho = pA * pS_AFc
                PF_meas = F.mean()
                lem = L['%d/%s/k1/%d' % (N, typ, n)]
                PF_b1 = min(lem['bound_binned'], lem['bound_single'])
                out['%d/%s/%d' % (N, typ, n)] = dict(islands=len(rec), P_surv=float(S.mean()), P_A=float(pA),
                    P_surv_given_A_Fc=float(pS_AFc), P_surv_given_A_F=float(pS_AF), n_AF=int((A & F).sum()), h=float(h),
                    rho_tilde=float(rho), P_F_measured=float(PF_meas), P_F_B1=float(PF_b1),
                    bound_B1=float(rho - PF_b1 * max(h, 0)), bound_measuredF=float(rho - PF_meas * max(h, 0)))
                o = out['%d/%s/%d' % (N, typ, n)]
                print('%d %-13s n=%2d | P(surv) %.3f | rho~ %.3f (P(A) %.3f x %.3f) | h %.2f (n_AF %d) | P(F) meas %.3f B1 %.3f | bound B1 %.3f, meas-F %.3f' % (
                    N, typ, n, o['P_surv'], rho, pA, pS_AFc, h, o['n_AF'], PF_meas, PF_b1, o['bound_B1'], o['bound_measuredF']))
    _save('combined', out)


def report_main(a):
    rows = json.load(gzip.open(ROWS, 'rt'))
    out = {}
    lines = []
    for N in (100, 400):
        for typ in ('disadvantaged', 'neutral', 'advantaged'):
            for k in DOSES[N]:
                for nsel in ('pooled',) + tuple(SC.NS):
                    R = [r for r in rows if r['N'] == N and TYPES[r['pair']] == typ and (nsel == 'pooled' or r['n'] == nsel)]
                    R = [(r, r['runs'][str(k)]) for r in R]
                    RE = [(r, x) for r, x in R if x['xA'] >= 0.3 and x['xD'] >= 0.3]
                    f = [x['faker'] for _, x in RE]; g = [x['ghost'] for _, x in RE]
                    nE = len(RE)
                    st = np.array([y['status'] for y in f]); stg = np.array([y['status'] for y in g])
                    alive = np.array([y['kq'] > 0 for y in f]); galive = np.array([y['kg'] > 0 for y in g])
                    tal = np.array([y['kt'] > 0 for y in f])
                    k0 = np.array([x['k0q'] for _, x in RE])
                    lam = np.array([y['Lam'] for y in f])
                    kq = np.array([y['kq'] for y in f])
                    pf = _wilson(alive.sum(), nE); pg = _wilson(galive.sum(), nE)
                    clean = np.array([r['bg_q'] == 0 for r, _ in RE])      # no background copies of q: exactly k copies
                    pf0 = _wilson((alive & clean).sum(), clean.sum()); pg0 = _wilson((galive & clean).sum(), clean.sum())
                    lam0 = lam[clean]; bb0, bs0 = b1_bound(lam0, k0[clean])
                    pf_t = _wilson((alive & tal).sum(), tal.sum())
                    bb, bs = b1_bound(lam, k0)
                    mart = float(np.mean(kq * np.exp(lam)) / np.mean(k0))
                    mart_se = float(np.std(kq * np.exp(lam)) / math.sqrt(nE) / np.mean(k0))
                    sf = _percopy(pf[0], k); sg = _percopy(pg[0], k)
                    sel_share = (math.log(sg / sf) / -math.log(sf)) if 0 < sf < 1 and sg > 0 else float('nan')
                    tau = np.array([y['tau'] for y in f])
                    key = '%d/%s/k%d/%s' % (N, typ, k, nsel)
                    rec = dict(N=N, type=typ, k=k, n=nsel, islands=len(R), in_E=nE,
                               status_counts={str(s): int((st == s).sum()) for s in (1, 2, 3)},
                               ghost_status_counts={str(s): int((stg == s).sum()) for s in (1, 2, 3)},
                               faker_alive=pf, ghost_alive=pg, faker_alive_given_target=pf_t,
                               s_faker=sf, s_ghost=sg, s_faker_given_target=_percopy(pf_t[0], k) if tal.sum() else None,
                               ratio_ghost_over_faker=(pg[0] / pf[0]) if pf[0] > 0 else None, selection_share=sel_share,
                               bound_binned=bb, bound_single=bs, bound_over_measured=(bb / pf[0]) if pf[0] > 0 else None,
                               Ek0=float(k0.mean()), martingale_ratio=mart, martingale_se=mart_se,
                               Lam_quantiles=[float(np.quantile(lam, p)) for p in (0.05, 0.25, 0.5, 0.75, 0.95)],
                               Lam_mean=float(lam.mean()), P_Lam_le_0=float(np.mean(lam <= 0)),
                               tau_median=float(np.median(tau)), tau_quantiles=[float(np.quantile(tau, p)) for p in (0.1, 0.5, 0.9)],
                               neutral_theory_1_over_1ptau=float(np.mean(1.0 / (1.0 + tau))),
                               J1=float(np.mean([y['J1'] for y in f])), Jpay=float(np.mean([y['Jpay'] for y in f])),
                               Jb2=float(np.mean([y['Jb2'] for y in f])), Jpos=float(np.mean([y['Jpos'] for y in f])),
                               Jneg=float(np.mean([y['Jneg'] for y in f])),
                               IA=float(np.mean([y['IA'] for y in f])), ID=float(np.mean([y['ID'] for y in f])),
                               IA_q05=float(np.quantile([y['IA'] for y in f], 0.05)),
                               dev=[float(v) for v in np.mean([y['dev'] for y in f], 0)],
                               xint=[float(v) for v in np.mean([y['xint'] for y in f], 0)],
                               ghost_mart=float(np.mean([y['kg'] for y in g]) / k),
                               clean_n=int(clean.sum()), clean_faker_alive=pf0, clean_ghost_alive=pg0,
                               clean_s_faker=_percopy(pf0[0], k), clean_s_ghost=_percopy(pg0[0], k),
                               clean_ratio=(pg0[0] / pf0[0]) if pf0[0] > 0 else None,
                               clean_selection_share=(math.log(_percopy(pg0[0], k) / _percopy(pf0[0], k)) / -math.log(_percopy(pf0[0], k))) if 0 < pf0[0] < 1 else None,
                               clean_bound=min(bb0, bs0), clean_bound_over_measured=(min(bb0, bs0) / pf0[0]) if pf0[0] > 0 else None,
                               clean_Lam_median=float(np.median(lam0)))
                    out[key] = rec
                    if nsel == 'pooled':
                        print('   clean (bg_q = 0, %d): faker %.4f [%.4f, %.4f] ghost %.4f [%.4f, %.4f] ratio %.2f sel %.2f bound %.3f (%.1fx) Lam med %.2f' % (
                            rec['clean_n'], *pf0, *pg0, rec['clean_ratio'] or float('nan'), rec['clean_selection_share'] or float('nan'),
                            rec['clean_bound'], rec['clean_bound_over_measured'] or float('nan'), rec['clean_Lam_median']), flush=True)
                        print('%s E %d | faker %.4f ghost %.4f (ratio %.2f) | s_f %.4f s_g %.4f sel %.2f | bound %.4f (%.1fx) | Lam med %.2f P(Lam<=0) %.2f | mart %.3f+-%.3f | tau med %.1f 1/(1+tau) %.4f' % (
                            key, nE, pf[0], pg[0], rec['ratio_ghost_over_faker'] or float('nan'), sf, sg, sel_share, bb,
                            rec['bound_over_measured'] or float('nan'), rec['Lam_quantiles'][2], rec['P_Lam_le_0'], mart, mart_se,
                            rec['tau_median'], rec['neutral_theory_1_over_1ptau']), flush=True)
    _save('lemma', out)
    # per pair: the faker's static payoffs against target, itself, D, ALLC, and the scramble integrals (k = 1, in E)
    pp = {}
    for n in SC.NS:
        for pi in range(7):
            P = SC.forced_pairs(n)[pi]
            tb = P['table']           # rows/cols: target, faker, D, ALLC
            for N in (100, 400):
                R = [r['runs']['1'] for r in rows if r['n'] == n and r['N'] == N and r['pair'] == pi]
                R = [x for x in R if x['xA'] >= 0.3 and x['xD'] >= 0.3]
                f = [x['faker'] for x in R]
                pp['%d/%d/%d' % (n, N, pi)] = dict(
                    target=P['target'], faker=P['faker'], type=TYPES[pi],
                    faker_payoff_vs=dict(target=tb[1][0], itself=tb[1][1], D=tb[1][2], ALLC=tb[1][3]),
                    D_payoff_vs=dict(target=tb[2][0], faker=tb[2][1], D=tb[2][2], ALLC=tb[2][3]),
                    int_x=dict(zip(SC.CATS, [float(v) for v in np.mean([y['xint'] for y in f], 0)[:6]])),
                    int_dev=dict(zip(SC.CATS, [float(v) for v in np.mean([y['dev'] for y in f], 0)[:6]])),
                    Lam_mean=float(np.mean([y['Lam'] for y in f])), tau_median=float(np.median([y['tau'] for y in f])),
                    faker_alive=float(np.mean([y['kq'] > 0 for y in f])), ghost_alive=float(np.mean([x['ghost']['kg'] > 0 for x in R])))
    _save('pairs', pp)
    for key, v in pp.items():
        if key.split('/')[1] == '400':
            print(key, v['faker'], v['type'], 'pay', v['faker_payoff_vs'], 'int_x', {k: round(x, 2) for k, x in v['int_x'].items()},
                  'dev', {k: round(x, 3) for k, x in v['int_dev'].items()}, 'Lam %.2f alive %.3f ghost %.3f' % (v['Lam_mean'], v['faker_alive'], v['ghost_alive']))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('cmd'); ap.add_argument('--procs', type=int, default=3); ap.add_argument('--nbg', type=int, default=NBG)
    a = ap.parse_args()
    dict(static=static_main, xcheck=xcheck_main, check=check_main, run=run_main, report=report_main, combined=combined_main)[a.cmd](a)
