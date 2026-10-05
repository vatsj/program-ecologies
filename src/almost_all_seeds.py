"""Almost all seeds?  Persistence without mutation along N >> I and I >> N
(specs/2026-10-04-almost-all-seeds.md; predictions/2026-10-04-almost-all-seeds.md).

Object 1 (static): the replicator from x0 = mu on each arm's full class payoff
matrix, under several priors; persistence (max growth rate over every class at
the endpoint), perturbation and tolerance checks, and a basin line toward
uniform.

Object 2 (dynamic): eps = 0 islands, iid seeding from mu (each slot iid from the
class masses of the length prior), complete island graph, w = 0.3, mN = 1, with
certified / metastable / unresolved stopping (see the predictions file).

Controls: mN = 0 islands; two-type single-migrant fixation assays (exact and
Monte Carlo).

    python3 src/almost_all_seeds.py static
    python3 src/almost_all_seeds.py assays
    python3 src/almost_all_seeds.py islands [--arms modal W0 L6R] [--only N,I,mN ...]
    python3 src/almost_all_seeds.py report
Writes runs/almost-all-seeds.md / .json (and runs/almost-all-seeds-islands.json).
"""
import argparse, json, os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from abm import njit
from chain import replicator, fixation

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
W = 0.3
_ARM = {}


# ------------------------------------------------------------------ arms
def arm_data(arm, n=6):
    """names, U, PCC, cnt (K x (n+1)) program counts by size, mu (length prior)."""
    key = (arm, n)
    if key in _ARM:
        return _ARM[key]
    if arm == 'modal':
        import modal as M
        L, val, worlds, prov = M.build(n)
        K = len(prov.names)
        cnt = np.zeros((K, n + 1))
        for k, mem in enumerate(prov.members):
            for s in range(1, n + 1):
                for c in mem:
                    cnt[k, s] += L.cnt_by_size[s].get(c, 0)
        d = dict(names=list(prov.names), U=np.ascontiguousarray(prov.Ufull, dtype=float), PCC=np.ascontiguousarray(prov.PCC, dtype=float),
                 cnt=cnt, mu=np.array([c[2] for c in prov.classes]), R='BOX(THEM(ME))')
    elif arm == 'W0':
        import matched_control as MC
        U, PCC, prov, lang, nprog = MC.build('W0', n)
        K = U.shape[0]
        cnt = np.zeros((K, n + 1))
        for k, c in enumerate(prov.classes):
            for p in c[1]:
                cnt[k, lang.size[p]] += 1
        d = dict(names=[lang.src(c[0]) for c in prov.classes], U=np.ascontiguousarray(U, dtype=float), PCC=np.ascontiguousarray(PCC, dtype=float),
                 cnt=cnt, mu=np.array([c[2] for c in prov.classes]), R='THEM(^C)')
    elif arm == 'L6R':
        assert n == 6
        from game import Game
        from abm import load_or_evaluate
        game = Game.load(os.path.join(ROOT, 'games', 'pd.yaml'))
        L, ids, reps, members, mu, Uc, PCC, PEX, names, div = load_or_evaluate(game, 6, verbose=False)
        K = len(reps)
        cnt = np.zeros((K, n + 1))
        for k, mem in enumerate(members):
            for a in mem:
                cnt[k, L.size[ids[a]]] += 1
        d = dict(names=list(names), U=np.ascontiguousarray(Uc, dtype=float), PCC=np.ascontiguousarray(PCC, dtype=float),
                 cnt=cnt, mu=np.asarray(mu, float), R='THEM(^C)')
    else:
        raise ValueError(arm)
    d['mu'] = d['mu'] / d['mu'].sum()
    nm = d['names']
    d['iR'] = nm.index(d['R']); d['iD'] = nm.index('D'); d['iC'] = nm.index('C')
    U = d['U']; iR = d['iR']
    d['fakers'] = [q for q in range(len(nm)) if U[q, iR] > U[iR, iR] + 1e-9]
    # cooperative family: self P(C,C) >= 0.95, not ALLC, and unexploitable (no class earns more against it than it earns against itself)
    d['coop'] = [k for k in range(len(nm)) if d['PCC'][k, k] >= 0.95 and k != d['iC']]
    d['coop_unfakeable'] = [k for k in d['coop'] if U[:, k].max() <= U[k, k] + 1e-9]
    _ARM[key] = d
    return d


def priors(d):
    """Class masses under each listed prior, each normalized to 1."""
    cnt = d['cnt']; n = cnt.shape[1] - 1
    s = np.arange(n + 1, dtype=float); a = cnt.sum(0)
    out = {}
    with np.errstate(divide='ignore', invalid='ignore'):
        per_len = np.where(a > 0, 1.0 / (np.maximum(a, 1) * 2 * np.maximum(s, 1) ** 2), 0.0)     # length prior, per program
    def norm(v): return v / v.sum()
    out['length'] = norm(cnt @ per_len)
    for b in (2, 4, 8):
        out['base %d' % b] = norm(cnt @ np.where(s > 0, float(b) ** (-s), 0.0))
    for beta in (0.5, 2.0):
        out['temper %g' % beta] = norm(cnt @ (per_len ** beta))
    out['uniform-programs'] = norm(cnt.sum(1))
    out['uniform-classes'] = np.full(cnt.shape[0], 1.0 / cnt.shape[0])
    return out


# ------------------------------------------------------------------ Object 1
def endpoint(d, x0, atol=1e-5, ext_tol=1e-9, close=True):
    """Replicator endpoint.  The integrator prunes shares below ext_tol, but in
    the true flow positive coordinates stay positive, so a pruned class with a
    positive growth rate at the endpoint would come back.  close=True re-injects
    every positive-growth class at 1e-6 and re-integrates until no class has a
    positive growth rate (at most 30 rounds); 'first' keeps the first endpoint."""
    e = _endpoint(d, x0, atol, ext_tol)
    if not close:
        return e
    first = dict(pcc=e['pcc'], max_growth=e['max_growth'], positive=list(e['positive']), support=dict(e['support']))
    rounds = []
    for it in range(30):
        if not e['positive']:
            break
        x1 = e['x'].copy(); x1[e['pos_idx']] += 1e-6; x1 /= x1.sum()
        added = list(e['positive'])
        e = _endpoint(d, x1, atol, ext_tol)
        rounds.append((added[:4], e['pcc']))
    e['first'] = first; e['rounds'] = rounds
    return e


def _endpoint(d, x0, atol, ext_tol):
    U, PCC = d['U'], d['PCC']
    x, status, traj, peak = replicator(U, x0, atol=atol, ext_tol=ext_tol)
    fit = U @ x; fbar = float(x @ fit); g = fit - fbar
    pcc = float(x @ PCC @ x); pay = fbar
    surv = np.nonzero(x >= 1e-6)[0]
    pos = np.nonzero(g > 1e-9)[0]
    neutral = [int(q) for q in np.nonzero(np.abs(g) <= 1e-9)[0] if x[q] < 1e-6]
    return dict(x=x, status=status, pcc=pcc, pay=pay, support={d['names'][k]: float(x[k]) for k in surv},
                max_growth=float(g.max()), argmax=[d['names'][q] for q in np.nonzero(g >= g.max() - 1e-12)[0]][:6],
                positive=[d['names'][q] for q in pos], pos_idx=pos, neutral=neutral, resid=float(np.abs(g[x > 0]).max()))


def extinction_order(d, x0, dt=0.02, T=4000.0, thr=1e-6):
    """Fixed-step exponential-Euler integration of the replicator (no pruning)
    from x0: the first times at which ALLC and D fall below thr, and the time
    the cooperative family first holds 0.99."""
    U = d['U']; x = np.asarray(x0, float).copy()
    tC = tD = t99 = None; t = 0.0
    coop = np.zeros(len(x), bool); coop[d['coop']] = True
    while t < T:
        f = U @ x; fb = x @ f
        x = x * np.exp(dt * (f - fb)); x /= x.sum(); t += dt
        if tC is None and x[d['iC']] < thr: tC = t
        if tD is None and x[d['iD']] < thr: tD = t
        if t99 is None and x[coop].sum() >= 0.99: t99 = t
        if tC is not None and tD is not None and t99 is not None:
            break
    return dict(t_C=tC, t_D=tD, t_coop99=t99, C_first=(tC is not None and (tD is None or tC < tD)))


def flow_check(d, x0, dt=0.02, T=20000.0, marks=(100, 300, 1000, 3000, 10000, 20000)):
    """Fixed-step exponential-Euler replicator from x0 with no pruning (only
    floating-point underflow): P(C,C) at the marked times, the final classes
    above 1e-6 and the final max growth rate.  A check on the closed endpoints
    (writes runs/almost-all-seeds-flow.txt via 'flowcheck')."""
    U = d['U']; x = np.asarray(x0, float).copy(); t = 0.0; out = []; mi = 0
    while t < T:
        f = U @ x; fb = x @ f
        x = x * np.exp(dt * (f - fb)); x /= x.sum(); t += dt
        if mi < len(marks) and t >= marks[mi]:
            out.append((marks[mi], float(x @ d['PCC'] @ x))); mi += 1
    top = sorted([(d['names'][k], float(x[k])) for k in range(len(x)) if x[k] > 1e-6], key=lambda kv: -kv[1])[:4]
    g = U @ x - x @ U @ x
    return out, top, float(g.max())


def character(e):
    return 'eff' if e['pcc'] >= 0.95 else ('def' if e['pcc'] <= 0.05 else 'mid')


def static_cell(job):
    arm, n = job
    d = arm_data(arm, n)
    names = d['names']; K = len(names)
    rows = []
    for pname, x0 in priors(d).items():
        t = time.time()
        e = endpoint(d, x0)
        r = dict(arm=arm, n=n, prior=pname, classes=K, status=e['status'], pcc=e['pcc'], pay=e['pay'],
                 support=sorted(e['support'].items(), key=lambda kv: -kv[1])[:8], n_support=len(e['support']),
                 max_growth=e['max_growth'], argmax=e['argmax'], positive=e['positive'][:8], n_positive=len(e['positive']),
                 n_neutral=len(e['neutral']), neutral=[names[q] for q in e['neutral']][:10], resid=e['resid'],
                 persistent=len(e['positive']) == 0, first=e['first'], closure_rounds=e['rounds'],
                 mu_R=float(x0[d['iR']]), mu_C=float(x0[d['iC']]), mu_D=float(x0[d['iD']]),
                 mu_coop=float(x0[d['coop']].sum()), mu_coop_unfakeable=float(x0[d['coop_unfakeable']].sum()), mu_fakers=float(x0[d['fakers']].sum()))
        # tolerance variants
        tol = {}
        for lab, kw in (('atol 1e-4', dict(atol=1e-4)), ('atol 1e-6', dict(atol=1e-6)), ('ext 1e-8', dict(ext_tol=1e-8)), ('ext 1e-10', dict(ext_tol=1e-10))):
            e2 = endpoint(d, x0, **kw)
            tol[lab] = dict(pcc=e2['pcc'], max_growth=e2['max_growth'], resid=e2['resid'], same=abs(e2['pcc'] - e['pcc']) < 1e-3)
        r['tolerance'] = tol
        if pname == 'length':
            r['extinction_order'] = extinction_order(d, x0)
        # perturbations (only meaningful when neutral classes exist)
        pert = []
        neu = list(e['neutral'])
        if d['iC'] in neu:
            neu.remove(d['iC']); neu = [d['iC']] + neu
        for q in neu[:40]:
            x1 = e['x'].copy(); x1[q] += 1e-2; x1 /= x1.sum()
            e2 = endpoint(d, x1)
            pert.append((names[q], e2['pcc'], abs(e2['pcc'] - e['pcc']) < 1e-3 and character(e2) == character(e)))
        if neu:
            x1 = e['x'].copy(); x1[neu] += 1e-2 / len(neu); x1 /= x1.sum()
            e2 = endpoint(d, x1)
            pert.append(('all neutral', e2['pcc'], abs(e2['pcc'] - e['pcc']) < 1e-3 and character(e2) == character(e)))
        rng = np.random.default_rng(7)
        for j in range(5):
            qs = rng.choice(K, size=3, replace=False)
            x1 = e['x'].copy(); x1[qs] += 1e-2 / 3; x1 /= x1.sum()
            e2 = endpoint(d, x1)
            pert.append(('mix ' + ','.join(names[q] for q in qs), e2['pcc'], abs(e2['pcc'] - e['pcc']) < 1e-3 and character(e2) == character(e)))
        r['perturb'] = pert
        r['perturb_recovered'] = int(sum(p[2] for p in pert)); r['perturb_n'] = len(pert)
        r['perturb_fail'] = [(p[0], p[1]) for p in pert if not p[2]][:6]
        r['time_s'] = time.time() - t
        rows.append(r)
    # basin lines (length prior)
    pr = priors(d)
    for uname, uni in (('classes', pr['uniform-classes']), ('programs', pr['uniform-programs'])):
        line = []
        for t in (0, 0.25, 0.5, 0.75, 1.0):
            e = endpoint(d, (1 - t) * pr['length'] + t * uni)
            line.append((t, e['pcc'], len(e['positive'])))
        rows.append(dict(arm=arm, n=n, basin_toward=uname, line=line,
                         t_max_eff=max([t for t, p, _ in line if p >= 0.95], default=None),
                         all_eff_upto=max([t for t in (0, 0.25, 0.5, 0.75, 1.0) if all(p >= 0.95 for tt, p, _ in line if tt <= t)], default=None)))
    return rows


# ------------------------------------------------------------------ Object 2
@njit(cache=True)
def _sample_parent(counts, paysum, U, pres, npres, isl, N, w):
    m = -1e300
    for t in range(npres[isl]):
        k = pres[isl, t]
        f = (paysum[isl, k] - U[k, k]) / (N - 1)
        if f > m: m = f
    tot = 0.0
    for t in range(npres[isl]):
        k = pres[isl, t]
        f = (paysum[isl, k] - U[k, k]) / (N - 1)
        tot += counts[isl, k] * np.exp(w * (f - m))
    u = np.random.random() * tot; acc = 0.0
    for t in range(npres[isl]):
        k = pres[isl, t]
        f = (paysum[isl, k] - U[k, k]) / (N - 1)
        acc += counts[isl, k] * np.exp(w * (f - m))
        if u <= acc:
            return k
    return pres[isl, npres[isl] - 1]


@njit(cache=True)
def _island_cc(counts, PCC, U, pres, npres, paysum, i, N):
    cc = 0.0; pay = 0.0
    for t in range(npres[i]):
        a = pres[i, t]
        pay += counts[i, a] * (paysum[i, a] - U[a, a]) / (N - 1)
        for t2 in range(npres[i]):
            b = pres[i, t2]
            nn = counts[i, a] * counts[i, b] if a != b else counts[i, a] * (counts[i, a] - 1)
            cc += nn * PCC[a, b]
    return cc / (N * (N - 1)), pay / N


@njit(cache=True)
def _run(U, PCC, init, N, w, m, gens, every, seed, iC, coopmask):
    """Complete island graph, eps = 0.  status: 1 outcome-frozen, 2 separated
    (monomorphic, all cross migrants strictly disadvantaged), 3 metastable
    (monomorphic at horizon), 4 unresolved, 5 every island locally frozen (m = 0)."""
    np.random.seed(seed)
    I, K = init.shape
    counts = init.copy()
    paysum = np.zeros((I, K))
    pres = np.zeros((I, K), np.int64); npres = np.zeros(I, np.int64); pos = -np.ones((I, K), np.int64)
    for i in range(I):
        for k in range(K):
            if counts[i, k] > 0:
                pres[i, npres[i]] = k; pos[i, k] = npres[i]; npres[i] += 1
        for t in range(npres[i]):
            j = pres[i, t]
            for t2 in range(npres[i]):
                k = pres[i, t2]
                paysum[i, j] += counts[i, k] * U[j, k]
    nsamp = gens // every
    tr_cc = np.zeros(nsamp); tr_np = np.zeros(nsamp, np.int64)
    first_noC = -np.ones(I, np.int64)
    ext_C = -1
    strong = np.zeros(I, np.int64)
    lost_before = 0; lost_after = 0
    loss_log = np.zeros((400, 4), np.int64); nloss = 0     # (gen, island, largest class after, ALLC globally extinct)
    glob = np.zeros(K, np.int64)
    status = 0; stop_gen = gens
    s = 0
    for g in range(gens):
        for e in range(I * N):
            i = np.random.randint(I)
            src = i
            if m > 0.0 and I > 1 and np.random.random() < m:
                src = np.random.randint(I - 1)
                if src >= i: src += 1
            child = _sample_parent(counts, paysum, U, pres, npres, src, N, w)
            u = np.random.randint(N); acc = 0; victim = pres[i, 0]
            for t in range(npres[i]):
                k = pres[i, t]; acc += counts[i, k]
                if u < acc:
                    victim = k; break
            if victim == child:
                continue
            counts[i, victim] -= 1
            if counts[i, victim] == 0:
                p = pos[i, victim]; last = pres[i, npres[i] - 1]
                pres[i, p] = last; pos[i, last] = p; pos[i, victim] = -1; npres[i] -= 1
            new = counts[i, child] == 0
            if new:
                pres[i, npres[i]] = child; pos[i, child] = npres[i]; npres[i] += 1
            counts[i, child] += 1
            for t in range(npres[i]):
                j = pres[i, t]
                if new and j == child:
                    continue
                paysum[i, j] += U[j, child] - U[j, victim]
            if new:
                v = 0.0
                for t in range(npres[i]):
                    k = pres[i, t]
                    v += counts[i, k] * U[child, k]
                paysum[i, child] = v
        if (g + 1) % every == 0:
            for k in range(K): glob[k] = 0
            cc_tot = 0.0
            for i in range(I):
                for t in range(npres[i]):
                    glob[pres[i, t]] += counts[i, pres[i, t]]
                cc, pay = _island_cc(counts, PCC, U, pres, npres, paysum, i, N)
                cc_tot += cc
                if first_noC[i] < 0 and counts[i, iC] == 0:
                    first_noC[i] = g + 1
                co = 0
                for t in range(npres[i]):
                    if coopmask[pres[i, t]]: co += counts[i, pres[i, t]]
                if strong[i] == 1 and 2 * co < N:
                    if ext_C >= 0: lost_after += 1
                    else: lost_before += 1
                    if nloss < 400:
                        big = pres[i, 0]
                        for t in range(npres[i]):
                            if counts[i, pres[i, t]] > counts[i, big]: big = pres[i, t]
                        loss_log[nloss, 0] = g + 1; loss_log[nloss, 1] = i; loss_log[nloss, 2] = big; loss_log[nloss, 3] = 1 if ext_C >= 0 else 0
                        nloss += 1
                if 10 * co >= 9 * N: strong[i] = 1
                elif 2 * co < N: strong[i] = 0
            if ext_C < 0 and glob[iC] == 0:
                ext_C = g + 1
            if s < nsamp:
                tr_cc[s] = cc_tot / I
                npz = 0
                for k in range(K):
                    if glob[k] > 0: npz += 1
                tr_np[s] = npz
                s += 1
            # stopping
            if m > 0.0:
                lo = 1e300; hi = -1e300
                for a in range(K):
                    if glob[a] == 0: continue
                    for b in range(K):
                        if glob[b] == 0: continue
                        if U[a, b] < lo: lo = U[a, b]
                        if U[a, b] > hi: hi = U[a, b]
                if hi - lo < 1e-12:
                    status = 1; stop_gen = g + 1; break
                mono = True
                for i in range(I):
                    if npres[i] != 1:
                        mono = False; break
                if mono:
                    sep = True
                    for i in range(I):
                        a = pres[i, 0]
                        for j in range(I):
                            q = pres[j, 0]
                            if q != a and not (U[q, a] < U[a, a] - 1e-12):
                                sep = False
                    if sep:
                        status = 2; stop_gen = g + 1; break
            else:
                allf = True
                for i in range(I):
                    lo = 1e300; hi = -1e300
                    for t in range(npres[i]):
                        a = pres[i, t]
                        for t2 in range(npres[i]):
                            b = pres[i, t2]
                            if U[a, b] < lo: lo = U[a, b]
                            if U[a, b] > hi: hi = U[a, b]
                    if hi - lo >= 1e-12:
                        allf = False; break
                if allf:
                    status = 5; stop_gen = g + 1; break
    if status == 0:
        mono = True
        for i in range(I):
            if npres[i] != 1: mono = False
        status = 3 if mono else 4
    isl_cc = np.zeros(I); isl_pay = np.zeros(I)
    for i in range(I):
        isl_cc[i], isl_pay[i] = _island_cc(counts, PCC, U, pres, npres, paysum, i, N)
    return status, stop_gen, counts, isl_cc, isl_pay, first_noC, ext_C, lost_before, lost_after, tr_cc[:s], tr_np[:s], loss_log[:nloss]


STATUS = {1: 'certified-frozen', 2: 'certified-separated', 3: 'metastable', 4: 'unresolved', 5: 'local-frozen'}


def outcome(cc, pay):
    if cc >= 0.95: return 'efficient'
    if cc <= 0.05 and abs(pay + 1) <= 0.05: return 'defecting'
    return 'other'


def island_job(job):
    arm, N, I, mN, rep, gens = job
    d = arm_data(arm, 6)
    U, PCC, mu = d['U'], d['PCC'], d['mu']
    K = len(mu)
    rng = np.random.default_rng([['modal', 'W0', 'L6R'].index(arm), N, I, int(mN * 10), rep])
    init = np.zeros((I, K), np.int64)
    for i in range(I):
        init[i] = rng.multinomial(N, mu)
    coopmask = np.zeros(K, np.bool_); coopmask[d['coop']] = True
    t = time.time()
    st, sg, counts, isl_cc, isl_pay, first_noC, ext_C, lb, la, tr_cc, tr_np, loss_log = _run(
        U, PCC, init, N, W, mN / N, gens, 20, 100003 * rep + 7 * N + I + ['modal', 'W0', 'L6R'].index(arm) * 13 + int(mN * 1000), d['iC'], coopmask)
    names = d['names']
    glob = counts.sum(0)
    cc = float(isl_cc.mean()); pay = float(isl_pay.mean())
    r = dict(arm=arm, N=N, I=I, mN=mN, rep=rep, gens=gens, status=STATUS[st], stop_gen=int(sg), pcc=cc, pay=pay,
             outcome=outcome(cc, pay) if st in (1, 2, 3) else ('unresolved' if st == 4 else None),
             final={names[k]: int(v) for k, v in enumerate(glob) if v > 0},
             islands=[{names[k]: int(counts[i, k]) for k in np.nonzero(counts[i])[0]} for i in range(I)] if I <= 16 else None,
             n_island_classes=len({tuple(np.nonzero(counts[i])[0]) for i in range(I)}),
             isl_cc=isl_cc.tolist() if mN == 0 else None, isl_out=[outcome(c, p) for c, p in zip(isl_cc, isl_pay)] if mN == 0 else None,
             first_noC_median=float(np.median(first_noC[first_noC >= 0])) if (first_noC >= 0).any() else -1,
             first_noC_max=int(first_noC.max()) if (first_noC >= 0).all() else -1,
             ext_C=int(ext_C), lost_before=int(lb), lost_after=int(la),
             seed_has_R=int((init[:, d['iR']] > 0).sum()), seed_has_coopU=int((init[:, d['coop_unfakeable']].sum(1) > 0).sum()),
             seed_has_faker=int((init[:, d['fakers']].sum(1) > 0).sum()),
             loss_log=[(int(a), int(b), names[c], int(e)) for a, b, c, e in loss_log],
             trace_cc=tr_cc[::50].tolist(), time_s=time.time() - t)
    if st == 2:
        S = sorted({int(np.nonzero(counts[i])[0][0]) for i in range(I)})
        r['max_rho_sep'] = max(fixation(U[q, q], U[q, a], U[a, q], U[a, a], N, W, N) for q in S for a in S if q != a)
    return r


def cells():
    out = []
    for N in (100, 400, 1600, 6400):
        out.append((N, 4, 1.0, 40 if N in (100, 6400) else 20))
    for I in (16, 64, 256):
        out.append((100, I, 1.0, 40 if I == 256 else 20))
    for N, I in ((200, 8), (400, 16), (800, 32)):
        out.append((N, I, 1.0, 20))
    out += [(400, 4, 0.0, 20), (100, 64, 0.0, 20)]
    return out


def islands_main(a):
    path = os.path.join(RUNS, 'almost-all-seeds-islands.json')
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {(r['arm'], r['N'], r['I'], r['mN'], r['rep']) for r in rows}
    hz = json.load(open(a.horizons)) if a.horizons else {}
    jobs = []
    for arm in a.arms:
        for N, I, mN, reps in cells():
            if a.only and '%d,%d,%g' % (N, I, mN) not in a.only:
                continue
            gens = hz.get('%s,%d,%d,%g' % (arm, N, I, mN), a.gens)
            for rep in range(a.reps if a.reps else reps):
                if (arm, N, I, mN, rep) not in done:
                    jobs.append((arm, N, I, mN, rep, gens))
    jobs.sort(key=lambda j: -j[1] * j[2])
    for arm in a.arms:
        d = arm_data(arm, 6)
        # warm the numba cache once
        _run(d['U'], d['PCC'], np.full((2, len(d['mu'])), 1, np.int64), len(d['mu']), W, 0.01, 1, 1, 0, d['iC'], np.zeros(len(d['mu']), np.bool_))
    print('%d jobs' % len(jobs), flush=True)
    with Pool(a.procs) as pool:
        for r in pool.imap_unordered(island_job, jobs):
            rows.append(r)
            print('%s N=%d I=%d mN=%g rep %d: %s %s gen %d P(C,C) %.3f (%.0fs)' % (r['arm'], r['N'], r['I'], r['mN'], r['rep'], r['status'], r['outcome'],
                  r['stop_gen'], r['pcc'], r['time_s']), flush=True)
            json.dump(rows, open(path, 'w'))


# ------------------------------------------------------------------ assays
@njit(cache=True)
def _assay(uqq, uqa, uaq, uaa, N, w, reps, seed):
    np.random.seed(seed)
    fix = 0
    for r in range(reps):
        k = 1
        while 0 < k < N:
            fq = ((k - 1) * uqq + (N - k) * uqa) / (N - 1)
            fa = (k * uaq + (N - k - 1) * uaa) / (N - 1)
            p = 1.0 / (1.0 + np.exp(w * (fa - fq)))
            if np.random.random() < p: k += 1
            else: k -= 1
        if k == N: fix += 1
    return fix


def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 1.0)
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def assay_job(job):
    arm, q, a, N, reps = job
    d = arm_data(arm, 6); U = d['U']; nm = d['names']
    iq, ia = nm.index(q), nm.index(a)
    t = time.time()
    k = _assay(U[iq, iq], U[iq, ia], U[ia, iq], U[ia, ia], N, W, reps, 17 + N + 1000 * ['modal', 'W0', 'L6R'].index(arm) + 7 * iq + 3 * ia)
    return dict(arm=arm, q=q, a=a, N=N, reps=reps, fix=int(k), rho_mc=k / reps, ci=wilson(k, reps),
                rho_exact=float(fixation(U[iq, iq], U[iq, ia], U[ia, iq], U[ia, ia], N, W, N)), time_s=time.time() - t)


def assays_main(a):
    jobs = []
    for arm in ('modal', 'W0'):
        R = arm_data(arm, 6)['R']
        for N in (100, 400, 1600):
            jobs.append((arm, R, 'D', N, {100: 20000, 400: 50000, 1600: 100000}[N]))
            jobs.append((arm, 'D', R, N, 20000))
            if arm == 'W0':           # the faker edge, both directions
                jobs.append((arm, 'THEM(^D)', R, N, 20000))
                jobs.append((arm, R, 'THEM(^D)', N, 20000))
    with Pool(a.procs) as pool:
        rows = pool.map(assay_job, jobs)
    for r in rows:
        print(r, flush=True)
    json.dump(rows, open(os.path.join(RUNS, 'almost-all-seeds-assays.json'), 'w'), indent=1, default=float)


def static_main(a):
    jobs = [(arm, n) for arm, n in a.static_cells]
    with Pool(a.procs) as pool:
        res = pool.map(static_cell, jobs)
    rows = [r for rr in res for r in rr]
    json.dump(rows, open(os.path.join(RUNS, 'almost-all-seeds-static.json'), 'w'), indent=1, default=float)
    for r in rows:
        if 'prior' in r:
            print('%s n=%d %-16s first: P(C,C) %.4f max growth %.2e %s | closed after %d rounds: P(C,C) %.4f persistent %s max growth %.2e (%s) n_neutral %d perturb %d/%d tol %s support %s' % (
                r['arm'], r['n'], r['prior'], r['first']['pcc'], r['first']['max_growth'], r['first']['positive'][:2], len(r['closure_rounds']),
                r['pcc'], r['persistent'], r['max_growth'], ','.join(r['argmax'][:2]), r['n_neutral'],
                r['perturb_recovered'], r['perturb_n'], all(v['same'] for v in r['tolerance'].values()), r['support'][:4]), flush=True)
        else:
            print(r, flush=True)


# ------------------------------------------------------------------ report
def _fmt_ci(k, n):
    lo, hi = wilson(k, n)
    return '%.2f [%.2f, %.2f]' % (k / n if n else 0, lo, hi)


def report_main(a):
    L = ['# Almost all seeds? Persistence without mutation along N >> I and I >> N (2026-10-04)', '',
         'Spec `specs/2026-10-04-almost-all-seeds.md`; predictions `predictions/2026-10-04-almost-all-seeds.md`; code `src/almost_all_seeds.py`. '
         'PD, w = 0.3. Raw rows: `runs/almost-all-seeds.json` (static, islands, assays).', '']
    st = json.load(open(os.path.join(RUNS, 'almost-all-seeds-static.json')))
    isl = json.load(open(os.path.join(RUNS, 'almost-all-seeds-islands.json')))
    ap_ = os.path.join(RUNS, 'almost-all-seeds-assays.json')
    asy = json.load(open(ap_)) if os.path.exists(ap_) else []
    # ---- Object 1
    L += ['## Object 1: replicator from x0 = prior', '',
          '"first" = the integrator\'s endpoint (`chain.replicator`, shares below 1e-9 pruned). "closed" = after re-injecting every class with positive '
          'growth rate at 1e-6 and re-integrating until none has (the true flow keeps positive coordinates positive). Persistence, neutral classes, '
          'perturbations and tolerance checks refer to the closed endpoint. Support = classes with share >= 1e-6.', '',
          '| arm | n | prior | first P(C,C) | first max growth (class) | rounds | closed P(C,C) | persistent | support size | top support | neutral extinct classes | perturbations recovered | tolerance x10 and /10 same | residual |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in st:
        if 'prior' not in r: continue
        f = r['first']
        L.append('| %s | %d | %s | %.4f | %.2g %s | %d | %.4f | %s | %d | %s | %d | %d/%d | %s | %.0e |' % (
            r['arm'], r['n'], r['prior'], f['pcc'], f['max_growth'], ('`%s`' % f['positive'][0]) if f['positive'] else '', len(r['closure_rounds']),
            r['pcc'], 'yes' if r['persistent'] else 'NO', r['n_support'], '; '.join('`%s` %.2f' % (k, v) for k, v in r['support'][:3]),
            r['n_neutral'], r['perturb_recovered'], r['perturb_n'], 'yes' if all(v['same'] for v in r['tolerance'].values()) else 'NO', r['resid']))
    L += ['', 'Extinction order under the length prior (fixed-step integration, no pruning; time to share < 1e-6):', '',
          '| arm | n | ALLC extinct at t | D extinct at t | cooperative family >= 0.99 at t | ALLC first |', '|---|---|---|---|---|---|']
    fm = lambda v: '%.1f' % v if v is not None else 'never (t <= 4000)'
    for r in st:
        if r.get('prior') == 'length':
            e = r['extinction_order']
            L.append('| %s | %d | %s | %s | %s | %s |' % (r['arm'], r['n'], fm(e['t_C']), fm(e['t_D']), fm(e['t_coop99']), e['C_first']))
    L += ['', 'Basin lines, x0 = (1 - t) * length prior + t * uniform (closed endpoints): P(C,C) at t = 0, 0.25, 0.5, 0.75, 1.', '',
          '| arm | n | uniform over | P(C,C) along t | largest t with every t\' <= t efficient |', '|---|---|---|---|---|']
    for r in st:
        if 'basin_toward' in r:
            L.append('| %s | %d | %s | %s | %s |' % (r['arm'], r['n'], r['basin_toward'], ' / '.join('%.2f' % p for t, p, _ in r['line']),
                                                    r['all_eff_upto'] if r['all_eff_upto'] is not None else 'none'))
    # ---- Object 2
    L += ['', '## Object 2: eps = 0 islands, iid seeding from mu', '',
          'Complete island graph, mN = 1 (one migrant per island per generation; a generation = I*N births), horizon 1e5 generations, checks every 20. '
          'Categories: CF = certified, outcome-frozen (all surviving classes pairwise payoff-identical); CS = certified, separated (islands monomorphic, every '
          'cross-island migrant strictly disadvantaged); MS = metastable (monomorphic at horizon, some neutral or advantaged migrant); UN = unresolved. '
          'Efficient = mean island P(C,C) >= 0.95 at stop. Eff fraction = efficient (CF/CS/MS) / runs, Wilson 95%. '
          'P(no R), P(no unfakeable coop), P(faker) are per-island seed probabilities from mu, times I.', '']
    for arm in ('modal', 'W0', 'L6R'):
        d = arm_data(arm, 6)
        muR = d['mu'][d['iR']]; muU = d['mu'][d['coop_unfakeable']].sum(); muF = d['mu'][d['fakers']].sum()
        L += ['### %s' % {'modal': 'Modal arm (n = 6, all box kinds)', 'W0': 'W0 (weak, no X, no `ROLE`, n = 6)', 'L6R': 'Weak L_6 with X and `ROLE`'}[arm], '',
              'mu(R = `%s`) = %.4f; mu(unfakeable cooperative family) = %.4f; mu(fakers of R) = %.4f.' % (d['R'], muR, muU, muF), '',
              '| N | I | mN | runs | CF / CS / MS / UN | efficient / defecting / other | eff fraction [95%] | mean final P(C,C) | median stop gen | P(no R) * I | P(no unfakeable coop) * I | P(faker) * I | islands seeded with R / faker | top frozen classes |',
              '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
        for N, I, mN, reps in cells():
            s = [r for r in isl if r['arm'] == arm and r['N'] == N and r['I'] == I and r['mN'] == mN]
            if not s: continue
            n = len(s)
            if mN == 0:
                cat = [sum(r['status'] == 'local-frozen' for r in s), 0, 0, sum(r['status'] == 'unresolved' for r in s)]
            else:
                cat = [sum(r['status'] == c for r in s) for c in ('certified-frozen', 'certified-separated', 'metastable', 'unresolved')]
            oc = [sum(r['outcome'] == o for r in s) for o in ('efficient', 'defecting', 'other')]
            agg = {}
            for r in s:
                tot = sum(r['final'].values())
                for k, v in r['final'].items(): agg[k] = agg.get(k, 0) + v / tot / n
            top = sorted(agg.items(), key=lambda kv: -kv[1])[:3]
            pnoR = (1 - muR) ** N; pnoU = (1 - muU) ** N; pF = 1 - (1 - muF) ** N
            L.append('| %d | %d | %g | %d | %d / %d / %d / %d | %d / %d / %d | %s | %.3f | %d | %.2g | %.2g | %.2g | %.2f / %.2f | %s |' % (
                N, I, mN, n, cat[0], cat[1], cat[2], cat[3], oc[0], oc[1], oc[2], _fmt_ci(oc[0], n) if mN > 0 else '(per island below)',
                np.mean([r['pcc'] for r in s]), np.median([r['stop_gen'] for r in s]), pnoR * I, pnoU * I, pF * I,
                np.mean([r['seed_has_R'] / I for r in s]), np.mean([r['seed_has_faker'] / I for r in s]),
                '; '.join('`%s` %.2f' % kv for kv in top)))
        un = [r for r in isl if r['arm'] == arm and r['status'] in ('unresolved', 'metastable')]
        if un:
            L += ['', 'Unresolved / metastable runs: ' + '; '.join('(N %d, I %d, mN %g, rep %d) %s P(C,C) %.2f: %s' % (
                r['N'], r['I'], r['mN'], r['rep'], r['status'], r['pcc'], ', '.join('`%s` %d' % kv for kv in sorted(r['final'].items(), key=lambda kv: -kv[1])[:4])) for r in un[:12])]
        sep = [r for r in isl if r['arm'] == arm and r['status'] == 'certified-separated']
        if sep:
            L += ['', 'Certified-separated runs: %d; largest disadvantaged-migrant fixation probability %.2g.' % (len(sep), max(r['max_rho_sep'] for r in sep))]
        ctl = []
        for N, I, mN, reps in cells():
            if mN != 0: continue
            s = [r for r in isl if r['arm'] == arm and r['N'] == N and r['I'] == I and r['mN'] == 0]
            if not s: continue
            outs = [o for r in s for o in r['isl_out']]
            ctl.append('(N %d, I %d) %d islands: efficient %s, defecting %.2f, other %.2f' % (
                N, I, len(outs), _fmt_ci(sum(o == 'efficient' for o in outs), len(outs)), np.mean([o == 'defecting' for o in outs]), np.mean([o == 'other' for o in outs])))
        if ctl:
            L += ['', 'No-migration control (mN = 0), per island: ' + '; '.join(ctl) + '.']
        if arm == 'modal':
            L += ['', 'Mechanism (modal, mN = 1): global ALLC extinction generation; cooperative islands (>= 90% in cooperative classes other than ALLC) '
                  'that fell below 50%, before / after global ALLC extinction.', '',
                  '| N | I | ALLC extinct: median / max gen | runs with ALLC never extinct | coop islands lost before / after |', '|---|---|---|---|---|']
            for N, I, mN, reps in cells():
                if mN == 0: continue
                s = [r for r in isl if r['arm'] == arm and r['N'] == N and r['I'] == I and r['mN'] == mN]
                if not s: continue
                ex = [r['ext_C'] for r in s if r['ext_C'] >= 0]
                L.append('| %d | %d | %s / %s | %d | %d / %d |' % (N, I, '%d' % np.median(ex) if ex else '-', '%d' % max(ex) if ex else '-',
                         sum(r['ext_C'] < 0 for r in s), sum(r['lost_before'] for r in s), sum(r['lost_after'] for r in s)))
            lp = os.path.join(RUNS, 'almost-all-seeds-losses.json')
            if os.path.exists(lp):
                import collections
                lo = json.load(open(lp)); c = collections.Counter((x[2], x[3]) for r in lo for x in r['loss_log'])
                L += ['', 'Who took those islands (the %d runs with losses re-run with a loss log, `runs/almost-all-seeds-losses.json`; %d of %d reproduced '
                      'exactly; all %d ended efficient): ' % (len(lo), sum(r['reproduced'] for r in lo), len(lo), sum(r['outcome'] == 'efficient' for r in lo)) +
                      ', '.join('`%s` %d (%s)' % (k[0], v, 'after ALLC extinct' if k[1] else 'before') for k, v in c.most_common()) +
                      '. These probe-fakers (D against everything but ALLC) exploit only the fakeable cooperative classes in the cooperative set '
                      '(`BOX(THEM(^C))`, `BOX1(THEM(^C))` and `not(...)` forms), not FairBot, `BOX(THEM(THEM))` or `BOX1(THEM(ME))`.']
        L.append('')
    if asy:
        L += ['## Control (b): single-migrant fixation assays (isolated island, two types)', '',
              '| arm | migrant -> resident | N | reps | fixations | rho Monte Carlo [95%] | rho exact |', '|---|---|---|---|---|---|---|']
        for r in asy:
            lo, hi = r['ci']
            L.append('| %s | `%s` -> all-`%s` | %d | %d | %d | %.2e [%.2e, %.2e] | %.3e |' % (r['arm'], r['q'], r['a'], r['N'], r['reps'], r['fix'], r['rho_mc'], lo, hi, r['rho_exact']))
        for arm in ('modal', 'W0'):
            s = [r for r in asy if r['arm'] == arm and r['a'] == 'D']
            if len(s) >= 2:
                x = np.log([r['N'] for r in s]); y1 = np.log([r['rho_exact'] for r in s])
                ym = [np.log(r['rho_mc']) for r in s if r['fix'] > 0]
                L += ['', '%s, R into all-D: slope of log rho on log N over N = 100, 400, 1600: exact %.3f%s.' % (arm, np.polyfit(x, y1, 1)[0],
                      (', Monte Carlo %.3f' % np.polyfit(x, ym, 1)[0]) if len(ym) == len(s) else '')]
    out = '\n'.join(L) + '\n'
    open(os.path.join(RUNS, 'almost-all-seeds.md'), 'w').write(out)
    json.dump(dict(static=st, islands=[{k: v for k, v in r.items() if k != 'trace_cc'} for r in isl], assays=asy),
              open(os.path.join(RUNS, 'almost-all-seeds.json'), 'w'), indent=0, default=float)
    print(out)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['static', 'islands', 'assays', 'time', 'report', 'flowcheck'])
    ap.add_argument('--arms', nargs='+', default=['modal', 'W0', 'L6R'])
    ap.add_argument('--only', nargs='*', default=None)
    ap.add_argument('--gens', type=int, default=100000)
    ap.add_argument('--reps', type=int, default=0)
    ap.add_argument('--horizons', default='')
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--static_cells', nargs='+', type=lambda s: (s.split(':')[0], int(s.split(':')[1])),
                    default=[('modal', 6), ('modal', 7), ('modal', 8), ('modal', 9), ('W0', 6), ('W0', 7), ('L6R', 6)])
    a = ap.parse_args()
    if a.what == 'static': static_main(a)
    elif a.what == 'islands': islands_main(a)
    elif a.what == 'assays': assays_main(a)
    elif a.what == 'report': report_main(a)
    elif a.what == 'flowcheck':          # weak arms, all priors, T = 2e4; modal n = 8 at three priors, T = 3e3
        for arm, n, pns, T in (('W0', 7, None, 2e4), ('W0', 6, None, 2e4), ('L6R', 6, None, 2e4), ('modal', 8, ('length', 'base 8', 'temper 2'), 3e3)):
            d = arm_data(arm, n)
            for pn, x0 in priors(d).items():
                if pns and pn not in pns: continue
                out, top, gm = flow_check(d, x0, T=T, marks=tuple(m for m in (100, 300, 1000, 3000, 10000, 20000) if m <= T))
                print(arm, n, pn, ' '.join('t%d:%.3f' % o for o in out), top, 'maxg %.1e' % gm, flush=True)
    elif a.what == 'time':
        for arm in a.arms:
            r = island_job((arm, 6400, 4, 1.0, 0, a.gens))
            print(arm, r['status'], r['outcome'], r['stop_gen'], '%.1fs' % r['time_s'], flush=True)
