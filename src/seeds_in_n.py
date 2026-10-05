"""Almost all seeds: cutoff sensitivity in n (specs/2026-10-05-seeds-in-n.md;
predictions/2026-10-05-seeds-in-n.md).

The eps = 0 island lottery of src/almost_all_seeds.py (complete island graph,
w = 0.3, mN = 1, iid seeding from the length prior, the same certification),
for the modal arm at cutoffs n = 6, 7, 8, 9.  The kernel `_run` below is
almost_all_seeds._run with additions that do not change the random stream
(checked by `python3 src/seeds_in_n.py check`):
  - T0: migration off for generations g < T0 (nucleation-then-spread control);
  - exact island-level and global ALLC extinction times (in the birth loop);
  - the global class counts at global ALLC extinction;
  - for every lost cooperative island, its composition at the last check at
    which it was >= 90% cooperative (top 6 classes and the number present),
    so the loss mechanism can be reconstructed from the payoff table;
  - the first generation with a certified cooperative island (every present
    class cooperative, pairwise payoff-identical) and a certified core island
    (the same with every present class unfakeable), and island counts at T0.

    python3 src/seeds_in_n.py static      # the prior-mass table
    python3 src/seeds_in_n.py check       # kernel equals almost_all_seeds._run with T0 = 0
    python3 src/seeds_in_n.py time        # one run at n = 9, (1600, 4)
    python3 src/seeds_in_n.py run [--procs 3] [--only n,N,I,mN,T0 ...]
    python3 src/seeds_in_n.py report
Writes runs/seeds-in-n-rows.json (raw), runs/seeds-in-n.json and runs/seeds-in-n.md.
"""
import argparse, json, os, sys, time, collections
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import almost_all_seeds as AS
from abm import njit
from chain import fixation

ROOT = AS.ROOT
RUNS = AS.RUNS
W = AS.W
NS = (6, 7, 8, 9)
GENS = 100000                 # common generation budget, every cell (predeclared)
CAP_S = 7200                  # administrative cap per cell, seconds (projected)
ROWS = os.path.join(RUNS, 'seeds-in-n-rows.json')
MAXLOSS = 2000


def cells():
    """(n, N, I, mN, T0, reps)."""
    out = []
    for n in NS:
        for N, I, reps in ((100, 4, 20), (400, 4, 20), (1600, 4, 40), (100, 64, 20), (100, 256, 40), (400, 16, 20)):
            out.append((n, N, I, 1.0, 0, reps))
        for N in (100, 400, 1600):
            out.append((n, N, 4, 0.0, 0, 100))
    for n in (6, 9):
        out.append((n, 100, 64, 1.0, 2000, 40))
    return out


_D = {}


def data(n):
    if n in _D:
        return _D[n]
    d = dict(AS.arm_data('modal', n))
    K = len(d['names'])
    d['coopmask'] = np.zeros(K, np.bool_); d['coopmask'][d['coop']] = True
    d['coremask'] = np.zeros(K, np.bool_); d['coremask'][d['coop_unfakeable']] = True
    d['fakeable'] = [k for k in d['coop'] if k not in d['coop_unfakeable']]
    _D[n] = d
    return d


# ------------------------------------------------------------------ kernel
@njit(cache=True)
def _locally_frozen(counts, U, pres, npres, i):
    lo = 1e300; hi = -1e300
    for t in range(npres[i]):
        a = pres[i, t]
        for t2 in range(npres[i]):
            b = pres[i, t2]
            if U[a, b] < lo: lo = U[a, b]
            if U[a, b] > hi: hi = U[a, b]
    return hi - lo < 1e-12


@njit(cache=True)
def _run(U, PCC, init, N, w, m, gens, every, seed, iC, coopmask, coremask, T0):
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
    loss_log = np.zeros((MAXLOSS, 6), np.int64); nloss = 0     # (gen, island, largest class after, ALLC globally extinct, classes present at snapshot)
    loss_snap = np.zeros((MAXLOSS, 6, 2), np.int64)            # top-6 (class, count) at the last strong check
    snap = np.zeros((I, 6, 2), np.int64); snap_np = np.zeros(I, np.int64); snap_g = np.zeros(I, np.int64)
    glob = np.zeros(K, np.int64)
    # exact ALLC extinction times
    tC_first = -np.ones(I); tC_last = -np.ones(I); C_reent = np.zeros(I, np.int64)
    gC = 0
    for i in range(I): gC += counts[i, iC]
    tC_glob = -1.0
    core_glob = np.zeros(K, np.int64)
    for i in range(I):
        if counts[i, iC] == 0:
            tC_first[i] = 0.0; tC_last[i] = 0.0
    if gC == 0:
        tC_glob = 0.0
        for i in range(I):
            for k in range(K): core_glob[k] += counts[i, k]
    first_cert = -1; first_cert_core = -1
    atT0 = np.zeros(4, np.int64)        # at g = T0: certified coop, certified core, frozen non-cooperative, not frozen
    status = 0; stop_gen = gens
    s = 0
    IN = I * N
    for g in range(gens):
        for e in range(IN):
            i = np.random.randint(I)
            src = i
            if m > 0.0 and I > 1 and g >= T0 and np.random.random() < m:
                src = np.random.randint(I - 1)
                if src >= i: src += 1
            child = AS._sample_parent(counts, paysum, U, pres, npres, src, N, w)
            u = np.random.randint(N); acc = 0; victim = pres[i, 0]
            for t in range(npres[i]):
                k = pres[i, t]; acc += counts[i, k]
                if u < acc:
                    victim = k; break
            if victim == child:
                continue
            counts[i, victim] -= 1
            if victim == iC:
                gC -= 1
                if counts[i, iC] == 0:
                    tt = g + e / IN
                    if tC_first[i] < 0: tC_first[i] = tt
                    tC_last[i] = tt
                if gC == 0 and tC_glob < 0:
                    tC_glob = g + e / IN
                    for i2 in range(I):
                        for t in range(npres[i2]):
                            core_glob[pres[i2, t]] += counts[i2, pres[i2, t]]
            if counts[i, victim] == 0:
                p = pos[i, victim]; last = pres[i, npres[i] - 1]
                pres[i, p] = last; pos[i, last] = p; pos[i, victim] = -1; npres[i] -= 1
            new = counts[i, child] == 0
            if new:
                pres[i, npres[i]] = child; pos[i, child] = npres[i]; npres[i] += 1
                if child == iC and tC_first[i] >= 0:
                    C_reent[i] += 1
            counts[i, child] += 1
            if child == iC:
                gC += 1
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
            ncert = 0; ncore = 0; nfz = 0
            for i in range(I):
                for t in range(npres[i]):
                    glob[pres[i, t]] += counts[i, pres[i, t]]
                cc, pay = AS._island_cc(counts, PCC, U, pres, npres, paysum, i, N)
                cc_tot += cc
                if first_noC[i] < 0 and counts[i, iC] == 0:
                    first_noC[i] = g + 1
                co = 0; allco = True; allcore = True
                for t in range(npres[i]):
                    if coopmask[pres[i, t]]: co += counts[i, pres[i, t]]
                    else: allco = False
                    if not coremask[pres[i, t]]: allcore = False
                fz = _locally_frozen(counts, U, pres, npres, i)
                if fz and allco:
                    ncert += 1
                    if allcore: ncore += 1
                elif fz:
                    nfz += 1
                if strong[i] == 1 and 2 * co < N:
                    if ext_C >= 0: lost_after += 1
                    else: lost_before += 1
                    if nloss < MAXLOSS:
                        big = pres[i, 0]
                        for t in range(npres[i]):
                            if counts[i, pres[i, t]] > counts[i, big]: big = pres[i, t]
                        loss_log[nloss, 0] = g + 1; loss_log[nloss, 1] = i; loss_log[nloss, 2] = big; loss_log[nloss, 3] = 1 if ext_C >= 0 else 0
                        loss_log[nloss, 4] = snap_np[i]; loss_log[nloss, 5] = snap_g[i]
                        for r in range(6):
                            loss_snap[nloss, r, 0] = snap[i, r, 0]; loss_snap[nloss, r, 1] = snap[i, r, 1]
                        nloss += 1
                if 10 * co >= 9 * N:
                    strong[i] = 1
                    # snapshot: top 6 classes by count
                    for r in range(6):
                        snap[i, r, 0] = -1; snap[i, r, 1] = 0
                    for t in range(npres[i]):
                        k = pres[i, t]; c = counts[i, k]
                        r = 5
                        if c > snap[i, 5, 1]:
                            while r > 0 and c > snap[i, r - 1, 1]:
                                snap[i, r, 0] = snap[i, r - 1, 0]; snap[i, r, 1] = snap[i, r - 1, 1]; r -= 1
                            snap[i, r, 0] = k; snap[i, r, 1] = c
                    snap_np[i] = npres[i]; snap_g[i] = g + 1
                elif 2 * co < N: strong[i] = 0
            if first_cert < 0 and ncert > 0: first_cert = g + 1
            if first_cert_core < 0 and ncore > 0: first_cert_core = g + 1
            if T0 > 0 and g + 1 == T0:
                atT0[0] = ncert; atT0[1] = ncore; atT0[2] = nfz; atT0[3] = I - ncert - nfz
            if ext_C < 0 and glob[iC] == 0:
                ext_C = g + 1
            if s < nsamp:
                tr_cc[s] = cc_tot / I
                npz = 0
                for k in range(K):
                    if glob[k] > 0: npz += 1
                tr_np[s] = npz
                s += 1
            # stopping (as almost_all_seeds._run)
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
                    if not _locally_frozen(counts, U, pres, npres, i):
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
        isl_cc[i], isl_pay[i] = AS._island_cc(counts, PCC, U, pres, npres, paysum, i, N)
    return (status, stop_gen, counts, isl_cc, isl_pay, first_noC, ext_C, lost_before, lost_after, tr_cc[:s], tr_np[:s],
            loss_log[:nloss], loss_snap[:nloss], tC_first, tC_last, C_reent, tC_glob, core_glob, first_cert, first_cert_core, atT0)


def seed_of(N, I, mN, rep, T0):
    """Paired across n: the same RNG seeds at every cutoff (the multinomial draw differs)."""
    return [N, I, int(mN * 10), rep, T0, 2026105], 100003 * rep + 7 * N + I + int(mN * 1000) + 3 * T0 + 4242


def mechanism(d, snapc, snapn, snp, q):
    """Classify a loss from the payoff table.  snapc/snapn: top classes and counts at the last
    strong check (-1 padded); snp: classes present then; q: largest class after the loss."""
    U = d['U']; nm = d['names']
    res = [(int(c), int(k)) for c, k in zip(snapc, snapn) if c >= 0 and c != q]
    held = max(res, key=lambda x: x[1])[0] if res else -1
    q_in = q in [int(c) for c in snapc if c >= 0]
    n_res = snp - (1 if q_in else 0)
    if held < 0:
        return dict(held=None, mech='unknown')
    a = held
    if n_res == 1:
        if U[q, a] > U[a, a] + 1e-9: mech = 'strict invasion of a monomorphic island'
        elif abs(U[q, a] - U[a, a]) <= 1e-9: mech = 'neutral replacement'
        else: mech = 'fixation against selection'
    else:
        mech = 'displacement from a mixed island'
    return dict(held=nm[a], held_core=bool(d['coremask'][a]), held_coop=bool(d['coopmask'][a]), taker=nm[q],
                mech=mech, n_residents=int(n_res), allc_in_snapshot=bool(d['iC'] in [int(c) for c in snapc]),
                q_strictly_beats_held=bool(U[q, a] > U[a, a] + 1e-9),
                snapshot=[(nm[int(c)], int(k)) for c, k in zip(snapc, snapn) if c >= 0])


def job(j):
    n, N, I, mN, T0, rep, gens = j
    d = data(n)
    U, PCC, mu = d['U'], d['PCC'], d['mu']
    K = len(mu); nm = d['names']
    rs, ss = seed_of(N, I, mN, rep, T0)
    rng = np.random.default_rng(rs)
    init = np.zeros((I, K), np.int64)
    for i in range(I):
        init[i] = rng.multinomial(N, mu)
    t = time.time()
    (st, sg, counts, isl_cc, isl_pay, first_noC, ext_C, lb, la, tr_cc, tr_np, loss_log, loss_snap,
     tC_first, tC_last, C_reent, tC_glob, core_glob, first_cert, first_cert_core, atT0) = _run(
        U, PCC, init, N, W, mN / N, gens, 20, ss, d['iC'], d['coopmask'], d['coremask'], T0)
    glob = counts.sum(0)
    cc = float(isl_cc.mean()); pay = float(isl_pay.mean())
    core = d['coop_unfakeable']; coop = d['coop']
    holders = []
    for i in range(I):
        nz = np.nonzero(counts[i])[0]
        holders.append(nm[int(nz[np.argmax(counts[i, nz])])])
    losses = []
    for x, sn in zip(loss_log, loss_snap):
        r = mechanism(d, sn[:, 0], sn[:, 1], int(x[4]), int(x[2]))
        r.update(gen=int(x[0]), island=int(x[1]), after_allc=int(x[3]), snapshot_gen=int(x[5]))
        losses.append(r)
    r = dict(n=n, N=N, I=I, mN=mN, T0=T0, rep=rep, gens=gens, status=AS.STATUS[st], stop_gen=int(sg), pcc=cc, pay=pay,
             outcome=AS.outcome(cc, pay) if st in (1, 2, 3) else ('unresolved' if st == 4 else None),
             final={nm[k]: int(v) for k, v in enumerate(glob) if v > 0},
             holders=holders,
             isl_out=[AS.outcome(c, p) for c, p in zip(isl_cc, isl_pay)],
             isl_cc=[round(float(c), 4) for c in isl_cc] if mN == 0 else None,
             isl_final=[{nm[k]: int(counts[i, k]) for k in np.nonzero(counts[i])[0]} for i in range(I)] if (I <= 16 or mN == 0) else None,
             ext_C_check=int(ext_C), tC_glob=float(tC_glob), tC_first=[round(float(v), 2) for v in tC_first],
             tC_last=[round(float(v), 2) for v in tC_last], C_reentries=int(C_reent.sum()),
             lost_before=int(lb), lost_after=int(la), losses=losses,
             seed_core=[{nm[k]: int(init[i, k]) for k in core if init[i, k] > 0} for i in range(I)],
             seed_n_core=[int(init[i, core].sum()) for i in range(I)],
             seed_n_fakeable=[int(init[i, d['fakeable']].sum()) for i in range(I)],
             seed_n_C=[int(init[i, d['iC']]) for i in range(I)],
             core_at_extC=int(core_glob[core].sum()) if tC_glob >= 0 else None,
             coop_at_extC=int(core_glob[coop].sum()) if tC_glob >= 0 else None,
             core_at_extC_by={nm[k]: int(core_glob[k]) for k in coop if core_glob[k] > 0} if tC_glob >= 0 else None,
             first_cert=int(first_cert), first_cert_core=int(first_cert_core),
             at_T0=dict(cert_coop=int(atT0[0]), cert_core=int(atT0[1]), frozen_other=int(atT0[2]), not_frozen=int(atT0[3])) if T0 > 0 else None,
             trace_cc=[round(float(v), 4) for v in tr_cc[::5]], trace_np=[int(v) for v in tr_np[::5]],
             time_s=time.time() - t)
    if st == 4:
        pr = [k for k in range(K) if glob[k] > 0]
        r['unresolved_pairs'] = [(nm[a], nm[b]) for a in pr for b in pr if a < b and not (np.allclose(U[a, pr], U[b, pr]))][:20]
    return r


def key(r):
    return (r['n'], r['N'], r['I'], r['mN'], r['T0'], r['rep'])


def warm():
    d = data(6); K = len(d['mu'])
    _run(d['U'], d['PCC'], np.full((2, K), 1, np.int64), K, W, 0.01, 1, 1, 0, d['iC'], d['coopmask'], d['coremask'], 0)


def run_main(a):
    rows = json.load(open(ROWS)) if os.path.exists(ROWS) else []
    done = {key(r) for r in rows}
    jobs = []
    for n, N, I, mN, T0, reps in cells():
        if a.only and '%d,%d,%d,%g,%d' % (n, N, I, mN, T0) not in a.only:
            continue
        for rep in range(reps):
            if (n, N, I, mN, T0, rep) not in done:
                jobs.append((n, N, I, mN, T0, rep, a.gens))
    jobs.sort(key=lambda j: (-j[1] * j[2], -j[0]))
    warm()
    for n in NS: data(n)
    print('%d jobs' % len(jobs), flush=True)
    t0 = time.time()
    with Pool(a.procs, initializer=warm) as pool:
        for r in pool.imap_unordered(job, jobs):
            rows.append(r)
            print('n=%d N=%d I=%d mN=%g T0=%d rep %d: %s %s gen %d P(C,C) %.3f lost %d/%d (%.1fs; %.0fs total)' % (
                r['n'], r['N'], r['I'], r['mN'], r['T0'], r['rep'], r['status'], r['outcome'], r['stop_gen'], r['pcc'],
                r['lost_before'], r['lost_after'], r['time_s'], time.time() - t0), flush=True)
            if len(rows) % 25 == 0:
                json.dump(rows, open(ROWS, 'w'))
    json.dump(rows, open(ROWS, 'w'))


def check_main(a):
    """The kernel with T0 = 0 reproduces almost_all_seeds._run draw for draw."""
    for n, N, I in ((6, 100, 4), (6, 400, 4), (9, 100, 16), (8, 400, 4)):
        d = data(n); K = len(d['mu'])
        for rep in range(3):
            rng = np.random.default_rng([n, N, I, rep])
            init = np.array([rng.multinomial(N, d['mu']) for _ in range(I)], np.int64)
            A = AS._run(d['U'], d['PCC'], init, N, W, 1.0 / N, 20000, 20, 11 + rep, d['iC'], d['coopmask'])
            B = _run(d['U'], d['PCC'], init, N, W, 1.0 / N, 20000, 20, 11 + rep, d['iC'], d['coopmask'], d['coremask'], 0)
            same = A[0] == B[0] and A[1] == B[1] and np.array_equal(A[2], B[2]) and A[6] == B[6] and A[7] == B[7] and A[8] == B[8]
            print(n, N, I, rep, 'same' if same else 'DIFFERENT', A[0], A[1], B[0], B[1], 'ext_C check %d exact %.2f' % (B[6], B[16]),
                  'losses', len(B[11]), flush=True)


def static_rows():
    rows = []
    for n in NS:
        d = data(n); mu = d['mu']; nm = d['names']
        rows.append(dict(n=n, classes=len(nm), mu_C=float(mu[d['iC']]), mu_D=float(mu[d['iD']]), mu_coop=float(mu[d['coop']].sum()),
                         mu_core=float(mu[d['coop_unfakeable']].sum()), mu_FB=float(mu[nm.index('BOX(THEM(ME))')]),
                         mu_fakeable=float(mu[d['fakeable']].sum()), n_core=len(d['coop_unfakeable']), n_coop=len(d['coop']),
                         core=[(nm[k], float(mu[k])) for k in sorted(d['coop_unfakeable'], key=lambda k: -mu[k])]))
    return rows


def static_main(a):
    for r in static_rows():
        print('n=%d classes %d mu(ALLC) %.3f mu(D) %.3f mu(self-coop) %.4f mu(core) %.4f mu(FairBot) %.4f mu(fakeable) %.4f | core %d of %d: %s' % (
            r['n'], r['classes'], r['mu_C'], r['mu_D'], r['mu_coop'], r['mu_core'], r['mu_FB'], r['mu_fakeable'], r['n_core'], r['n_coop'],
            ', '.join('%s %.4f' % kv for kv in r['core'][:6])))


def time_main(a):
    warm()
    for rep in range(a.reps or 1):
        r = job((9, 1600, 4, 1.0, 0, rep, a.gens))
        print('n=9 (1600, 4) rep %d: %s %s gen %d, %.1fs' % (rep, r['status'], r['outcome'], r['stop_gen'], r['time_s']), flush=True)


def replay_main(a):
    """Birth-level replay of the one core-held island lost to D (n = 6, (100, 256), rep 17, island 189):
    the kernel is re-compiled with a log of every birth on that island from generation 140 (same draws)."""
    import inspect
    src = inspect.getsource(_run.py_func).replace('@njit(cache=True)\n', '')
    src = src.replace('def _run(U, PCC, init, N, w, m, gens, every, seed, iC, coopmask, coremask, T0):',
                      'def _run(U, PCC, init, N, w, m, gens, every, seed, iC, coopmask, coremask, T0, target, blog):\n    nb = 0')
    old = "            if victim == child:\n                continue\n"
    assert src.count(old) == 1
    src = src.replace(old, "            if i == target and g >= 140 and nb < blog.shape[0]:\n                blog[nb, 0] = g; blog[nb, 1] = src; blog[nb, 2] = child; blog[nb, 3] = victim; nb += 1\n" + old)
    ns = dict(globals()); exec(compile(src, 'replay', 'exec'), ns); run = njit(cache=False)(ns['_run'])
    d = data(6); nm = d['names']; iD = nm.index('D')
    rs, ss = seed_of(100, 256, 1.0, 17, 0)
    rng = np.random.default_rng(rs); init = np.array([rng.multinomial(100, d['mu']) for _ in range(256)], np.int64)
    blog = -np.ones((5000, 4), np.int64)
    out = run(d['U'], d['PCC'], init, 100, W, 0.01, 160, 10 ** 6, ss, d['iC'], d['coopmask'], d['coremask'], 0, 189, blog)
    b = blog[blog[:, 0] >= 0]
    for g in range(140, 160, 4):
        bb = b[(b[:, 0] >= g) & (b[:, 0] < g + 4)]
        print('gens %d-%d: births %d, local D-parent %d, D migrants %d, D victims %d' % (
            g, g + 3, len(bb), ((bb[:, 2] == iD) & (bb[:, 1] == 189)).sum(), ((bb[:, 2] == iD) & (bb[:, 1] != 189)).sum(), (bb[:, 3] == iD).sum()))
    mig = b[b[:, 1] != 189]
    print('total: %d births, %d migrant births of which %d D; final island %s' % (len(b), len(mig), (mig[:, 2] == iD).sum(),
          {nm[k]: int(out[2][189, k]) for k in np.nonzero(out[2][189])[0]}))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['static', 'check', 'time', 'run', 'report', 'replay'])
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--gens', type=int, default=GENS)
    ap.add_argument('--reps', type=int, default=0)
    ap.add_argument('--only', nargs='*', default=None)
    a = ap.parse_args()
    if a.what == 'static': static_main(a)
    elif a.what == 'check': check_main(a)
    elif a.what == 'time': time_main(a)
    elif a.what == 'run': run_main(a)
    elif a.what == 'replay': replay_main(a)
    elif a.what == 'report':
        import seeds_in_n_report as R
        R.main()
