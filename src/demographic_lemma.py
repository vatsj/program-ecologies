"""The demographic lemma, the factorized spoiler bound, and the establishment formula.
Spec specs/2026-10-05-demographic-lemma.md; predictions predictions/2026-10-05-demographic-lemma.md;
proofs notes/demographic-lemma.md.  Extends src/scramble_lemma.py (class cache, forced pairs, kernel conventions).

    python3 src/demographic_lemma.py static              # exact u_k, diffusion u_1, Lemma D event-clock bounds, model p(N)
    python3 src/demographic_lemma.py test                # kernel self-checks
    python3 src/demographic_lemma.py forced [--procs 3]  # Tasks 1-2: ghost (fixed t) + co-seeded target/faker founders
    python3 src/demographic_lemma.py dsea [--procs 3]    # Task 3(b): u_k from an all-D island
    python3 src/demographic_lemma.py lottery [--procs 3] # Task 3(c)-(e): iid lottery with per-founder tags
    python3 src/demographic_lemma.py report              # runs/demographic-lemma.{md,json}
"""
import argparse, gzip, json, math, os, sys, time
import numpy as np
from math import erf, sqrt, pi
sys.path.insert(0, os.path.dirname(__file__))
import spoiler_conditioned as SC
import scramble_lemma as SL

ROOT = SC.ROOT; RUNS = SC.RUNS
W = SC.W
C_SLOPE = W * 1.0          # c = w (R - P), R = 0, P = -1
OUT_JSON = os.path.join(RUNS, 'demographic-lemma.json')
NS_N = (100, 400, 1600)


def _load():
    try:
        return json.load(open(OUT_JSON))
    except FileNotFoundError:
        return {}


def _save(key, val):
    res = _load(); res[key] = val
    json.dump(res, open(OUT_JSON, 'w'), indent=1)


# ------------------------------------------------------------------ exact two-type fixation (prover vs D)
def log_gamma_prover_vs_D(N, w=W):
    """log of gamma_j = f_D(j) / f_q(j) for j = 1..N-1 copies of a prover q in a sea of D, with the kernel's
    self-excluded payoffs: pi_q(j) = ((j-1) R + (N-j) P)/(N-1), pi_D(j) = (j P + (N-j-1) P)/(N-1) = P.
    Birth-death Moran (parent by fitness, victim uniform): P(j -> j+1)/P(j -> j-1) = f_q(j)/f_D(j) exactly."""
    j = np.arange(1, N)
    return -w * (j - 1) / (N - 1)          # log(f_D/f_q) = w (pi_D - pi_q) = -w (j-1)/(N-1)


def u_exact(N, ks, w=W):
    """Exact fixation probability from k copies: u_k = sum_{i<k} prod_{j<=i} gamma_j / sum_{i<N} prod_{j<=i} gamma_j."""
    lg = log_gamma_prover_vs_D(N, w)
    cs = np.concatenate([[0.0], np.cumsum(lg)])        # cs[i] = sum_{j<=i} log gamma_j, i = 0..N-1
    m = cs.max()
    e = np.exp(cs - m)
    S = np.cumsum(e)                                    # S[k-1] = sum_{i<k}
    tot = S[-1]
    ks = np.asarray(ks)
    return S[np.clip(ks, 1, N) - 1] / tot * (ks > 0)


def u_all(N, w=W):
    """u_k for k = 0..N."""
    return np.concatenate([[0.0], u_exact(N, np.arange(1, N + 1), w)])


def u1_diffusion(N, c=C_SLOPE, erfcorr=True):
    """Diffusion with drift M(x) = c x^2 (1 - x) and variance V(x) = 2 x (1 - x)/N per generation (Moran birth-death):
    u'' = -N c x u', u(x) = erf(x sqrt(Nc/2)) / erf(sqrt(Nc/2)); u_1 = u(1/N)."""
    a = sqrt(N * c / 2)
    return erf(a / N) / (erf(a) if erfcorr else 1.0)


def u_diffusion(x, N, c=C_SLOPE):
    a = sqrt(N * c / 2)
    return erf(x * a) / erf(a)


# ------------------------------------------------------------------ Lemma D, event-clock bound
def lemmaD_event_bound(N, T, k0=1, K=None):
    """S(NT) <= inf_{t <= T} [1 - (1 - 1/(1 + dmin t))^k0] / P(Poisson(N t) <= N T)   (notes 1.4)."""
    from scipy.stats import poisson
    dmin = 1.0 if K is None else 1 - (K - 1) / N
    best = (1.0, T)
    for t in np.linspace(0.3 * T, T, 701):
        num = 1 - (1 - 1 / (1 + dmin * t)) ** k0
        den = poisson.cdf(N * T, N * t)
        v = num / den
        if v < best[0]:
            best = (v, float(t))
    return dict(bound=float(best[0]), t_star=best[1], poisson_bound_at_T=float(1 - (1 - 1 / (1 + dmin * T)) ** k0), dmin=dmin)


# ------------------------------------------------------------------ scramble model (mean field) for the curvature loss
def curvature_loss(xA0=0.466, xD0=0.466, w=W, dt=1e-3, xstop=None, N=None, remainder='none'):
    """Mean-field scramble in {ALLC, D, prover} with the prover rare: integrate r = f_e/Fbar - 1 for a payoff-neutral
    ALLC-cooperating establisher while ALLC decays (replicator flow of the kernel: dx_j/dt = x_j (f_j/Fbar - 1)).
    remainder='none': only ALLC and D (renormalized).  Returns R = int r dt up to x_A = 1/N (or xstop) and the time."""
    xA, xD = xA0 / (xA0 + xD0), xD0 / (xA0 + xD0)
    if xstop is None:
        xstop = 1.0 / N
    R = 0.0; t = 0.0
    while xA > xstop and t < 1e4:
        pA = -2 * xD; pD = xA - xD; pe = -xD                    # ALLC: S vs D, R vs ALLC; D: P vs D, T vs ALLC
        fA, fD, fe = math.exp(w * pA), math.exp(w * pD), math.exp(w * pe)
        Fb = xA * fA + xD * fD
        R += (fe / Fb - 1) * dt
        dA = xA * (fA / Fb - 1)
        xA += dA * dt; xD = 1 - xA
        t += dt
    return R, t


def static_main(a):
    out = {}
    rows = []
    for N in (100, 400, 1600, 6400):
        u = u_all(N)
        u1 = float(u[1])
        r = dict(N=N, u1_exact=u1, u1_diff=u1_diffusion(N), u1_diff_noerf=u1_diffusion(N, erfcorr=False),
                 u1_naive=sqrt(2 * C_SLOPE / (pi * N)),
                 uk={str(k): float(u[k]) for k in (1, 2, 4, 8, 16, 32, 64)},
                 uk_indep={str(k): float(1 - (1 - u1) ** k) for k in (1, 2, 4, 8, 16, 32, 64)},
                 uk_linear={str(k): float(k * u1) for k in (1, 2, 4, 8, 16, 32, 64)},
                 u_diff_k={str(k): float(u_diffusion(k / N, N)) for k in (1, 2, 4, 8, 16, 32, 64)})
        R, tA = curvature_loss(N=N)
        r['curvature_R'] = R; r['curvature_factor'] = math.exp(R); r['mf_allc_ext_time'] = tA
        rows.append(r)
        print('N=%5d u1 exact %.5f diff(erf) %.5f naive %.5f ratio exact/diff %.3f | curvature e^R %.3f (mf tau %.1f)' % (
            N, u1, r['u1_diff'], r['u1_naive'], u1 / r['u1_diff'], math.exp(R), tA))
        print('        u_k exact  ', ' '.join('%.4f' % r['uk'][k] for k in r['uk']))
        print('        1-(1-u1)^k ', ' '.join('%.4f' % r['uk_indep'][k] for k in r['uk']))
        print('        k u1       ', ' '.join('%.4f' % r['uk_linear'][k] for k in r['uk']))
        print('        diffusion  ', ' '.join('%.4f' % r['u_diff_k'][k] for k in r['uk']))
    out['u'] = rows
    LD = {}
    for N in NS_N:
        for T in (5, 10, 20, 40):
            for K in (None, N // 20, N // 4):
                b = lemmaD_event_bound(N, T, 1, K)
                LD['%d/%d/%s' % (N, T, K)] = b
                print('Lemma D event clock N=%d T=%d K=%s: bound %.4f (t* %.2f), Poisson-clock 1/(1+dmin T) %.4f, ratio %.3f' % (
                    N, T, K, b['bound'], b['t_star'], b['poisson_bound_at_T'], b['bound'] / b['poisson_bound_at_T']))
    out['lemmaD_event_clock'] = LD
    _save('static', out)



# ------------------------------------------------------------------ instrumented kernel (extends scramble_lemma._scramble)
from numba import njit

NSNAP = 4


@njit(cache=True)
def _xs_exp(state):
    """Exp(1) draw from an inline xorshift64* generator (separate from np.random, so the event chain is unchanged)."""
    x = state[0]
    x ^= (x >> np.uint64(12)); x ^= (x << np.uint64(25)); x ^= (x >> np.uint64(27))
    state[0] = x
    z = (x * np.uint64(2685821657736338717)) >> np.uint64(11)
    u = (float(z) + 0.5) / 9007199254740992.0
    return -math.log(u)


@njit(cache=True)
def _frozen(U, pres, npres):
    lo = 1e300; hi = -1e300
    for t in range(npres):
        a = pres[t]
        for t2 in range(npres):
            b = pres[t2]
            if U[a, b] < lo: lo = U[a, b]
            if U[a, b] > hi: hi = U[a, b]
    return hi - lo < 1e-12


@njit(cache=True)
def _dl_run(U, init, N, w, seed, iC, ghost, track, snaps, K1, K2, tmax_tau, mode, stop_gen, horizon, every):
    """One island of the seeds_in_n kernel (I = 1, m = 0; same RNG calls in the same order when ghost < 0), with:
    - an optional ghost class (index `ghost`) whose fitness per copy is pinned to the mean fitness of the others;
    - tracked lineages (class indices in `track`): per event, a = f/Fbar, r = a - 1, d = 1 - a k/N;
      R and Phi = 1 + int d e^{-R} on the event clock (dt = 1/N) and on an independent Poisson clock (Exp(N) holding
      times from a separate generator); Lam = -sum log(1 + r/N) (the exact discrete martingale k e^{Lam});
      the size at fixed generations `snaps`, first hitting generations of K1 and K2, and the running max up to tau;
    - tau = first ALLC extinction (status 1) ^ local freeze with ALLC present (2) ^ tmax_tau generations (3);
    - mode 0: stop at max(tau, stop_gen) or earlier once tau is reached and every tracked lineage is extinct;
      mode 1: after tau, continue to local freeze (final status 5) or the horizon (6).
    Returns everything as arrays."""
    np.random.seed(seed)
    K = init.shape[0]
    nt = track.shape[0]
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
    xs = np.zeros(1, np.uint64); xs[0] = np.uint64(seed * 2654435761 + 88172645463325252) | np.uint64(1)
    R_e = np.zeros(nt); Phi_e = np.ones(nt); R_p = np.zeros(nt); Phi_p = np.ones(nt); Lam = np.zeros(nt)
    ksnap = -np.ones((nt, snaps.shape[0]), np.int64); phisnap = np.zeros((nt, snaps.shape[0]))
    hit1 = -np.ones(nt); hit2 = -np.ones(nt)
    kmax = counts.copy()               # running max per class up to tau
    k_tau = -np.ones(nt, np.int64); phiE_tau = np.zeros(nt); phiP_tau = np.zeros(nt); R_tau = np.zeros(nt); Lam_tau = np.zeros(nt)
    counts_tau = counts.copy()
    IA = 0.0; ID = 0.0
    tau = -1.0; st_tau = 0; st_fin = 0; gend = 0
    wt = np.zeros(K)
    isnap = 0
    rec = 0
    if counts[iC] == 0:
        tau = 0.0; st_tau = 1
        for i in range(nt):
            k_tau[i] = counts[track[i]]; phiE_tau[i] = 1.0; phiP_tau[i] = 1.0
        rec = 1
    done = False
    for g in range(horizon):
        for e in range(N):
            # ---- fitness weights (as almost_all_seeds._sample_parent: exp(w (pi - m)), m = max over non-ghost present)
            m = -1e300
            for t in range(npres):
                k = pres[t]
                if k == ghost: continue
                f = (paysum[k] - U[k, k]) / (N - 1)
                if f > m: m = f
            S = 0.0; kg = 0
            for t in range(npres):
                k = pres[t]
                if k == ghost:
                    kg = counts[k]; continue
                f = (paysum[k] - U[k, k]) / (N - 1)
                wt[k] = np.exp(w * (f - m))
                S += counts[k] * wt[k]
            if kg >= N:
                fg = 1.0                     # the ghost has fixed: every weight is the ghost's (degenerate, neutral)
            elif kg > 0:
                fg = S / (N - kg)
            else:
                fg = 0.0
            if ghost >= 0:
                wt[ghost] = fg
            Fbar = (S + kg * fg) / N
            # ---- instrumentation (state before the event), only up to tau
            if st_tau == 0 or mode == 0:
                dtp = _xs_exp(xs) / N
                for i in range(nt):
                    c = track[i]; kc = counts[c]
                    if c == ghost or kg >= N:
                        a = 1.0
                    else:
                        if kc > 0:
                            pc = (paysum[c] - U[c, c]) / (N - 1)
                        else:
                            v = 0.0
                            for t in range(npres):
                                k = pres[t]; v += counts[k] * U[c, k]
                            pc = v / (N - 1)
                        a = np.exp(w * (pc - m)) / Fbar
                    r = a - 1.0
                    d = 1.0 - a * kc / N
                    Phi_e[i] += d * math.exp(-R_e[i]) / N
                    R_e[i] += r / N
                    Phi_p[i] += d * math.exp(-R_p[i]) * dtp
                    R_p[i] += r * dtp
                    Lam[i] -= math.log(1.0 + r / N)
                if st_tau == 0:
                    IA += counts[iC] / N / N
            # ---- the event
            np.random.randint(1)
            tot = 0.0
            for t in range(npres):
                k = pres[t]
                tot += counts[k] * wt[k]
            u = np.random.random() * tot; acc = 0.0
            child = pres[npres - 1]
            for t in range(npres):
                k = pres[t]
                acc += counts[k] * wt[k]
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
            if st_tau == 0 or mode == 0:
                # running max and first hitting times: up to tau in mode 1, over the whole run in mode 0
                if counts[child] > kmax[child]: kmax[child] = counts[child]
                for i in range(nt):
                    c = track[i]
                    if c == child:
                        if hit1[i] < 0 and counts[c] >= K1: hit1[i] = g + (e + 1.0) / N
                        if hit2[i] < 0 and counts[c] >= K2: hit2[i] = g + (e + 1.0) / N
            if st_tau == 0:
                if victim == iC and counts[iC] == 0:
                    tau = g + (e + 1.0) / N; st_tau = 1
                    for k in range(K): counts_tau[k] = counts[k]
                    for i in range(nt):
                        k_tau[i] = counts[track[i]]; phiE_tau[i] = Phi_e[i]; phiP_tau[i] = Phi_p[i]; R_tau[i] = R_e[i]; Lam_tau[i] = Lam[i]
                    rec = 1
        # end of generation g
        if st_tau == 0 and (g + 1) >= tmax_tau:
            tau = float(g + 1); st_tau = 3
        if st_tau == 0 and (g + 1) % every == 0:
            if _frozen(U, pres, npres):
                tau = float(g + 1); st_tau = 2
        # snapshots at exact generation boundaries ((g + 1) N events)
        while isnap < snaps.shape[0] and snaps[isnap] <= g + 1:
            for i in range(nt):
                ksnap[i, isnap] = counts[track[i]]; phisnap[i, isnap] = Phi_e[i]
            isnap += 1
        if st_tau > 0 and rec == 0:
            # the state at tau for statuses 2 and 3 (defined at generation ends); status 1 is recorded at the event
            for k in range(K): counts_tau[k] = counts[k]
            for i in range(nt):
                k_tau[i] = counts[track[i]]; phiE_tau[i] = Phi_e[i]; phiP_tau[i] = Phi_p[i]; R_tau[i] = R_e[i]; Lam_tau[i] = Lam[i]
            rec = 1
        if mode == 0:
            if st_tau > 0 and g + 1 >= stop_gen:
                st_fin = 7; gend = g + 1; done = True
            elif st_tau > 0:
                alive = False
                for i in range(nt):
                    if counts[track[i]] > 0: alive = True
                if not alive:
                    st_fin = 8; gend = g + 1; done = True
        else:
            if st_tau > 0 and (g + 1) % every == 0 and _frozen(U, pres, npres):
                st_fin = 5; gend = g + 1; done = True
        if done:
            break
    if not done:
        st_fin = 6; gend = horizon
    # snapshots not reached (run ended early): the lineage state is final; fill with the final counts
    while isnap < snaps.shape[0]:
        for i in range(nt):
            ksnap[i, isnap] = counts[track[i]]; phisnap[i, isnap] = -1.0
        isnap += 1
    return (st_tau, tau, counts_tau, st_fin, gend, counts, kmax, IA,
            k_tau, phiE_tau, phiP_tau, R_tau, Lam_tau, ksnap, phisnap, hit1, hit2)


# ------------------------------------------------------------------ wrappers and jobs
SNAPS = np.array([5, 10, 20, 40], np.int64)
GENS = 100000
EVERY = 20
TMAX_TAU = 2000
SALT_FRC = 20261051
SALT_DSEA = 20261052
SALT_LOT = 20261053
PDP = SC.PDP


def run_island(U, init, N, seed, iC, ghost=-1, track=(), K1=None, K2=None, mode=1, stop_gen=0, horizon=GENS):
    U = np.ascontiguousarray(U, dtype=np.float64)
    tr = np.array(track, np.int64)
    K1 = max(2, N // 20) if K1 is None else K1
    K2 = max(2, N // 4) if K2 is None else K2
    out = _dl_run(U, np.ascontiguousarray(init, np.int64), N, W, seed, iC, ghost, tr, SNAPS, K1, K2, TMAX_TAU, mode,
                  stop_gen, horizon, EVERY)
    keys = ('st_tau', 'tau', 'counts_tau', 'st_fin', 'gend', 'counts', 'kmax', 'IA', 'k_tau', 'phiE_tau', 'phiP_tau',
            'R_tau', 'Lam_tau', 'ksnap', 'phisnap', 'hit1', 'hit2')
    return dict(zip(keys, out))


def _local(d, init_full, extra=()):
    """Local class set: support of init_full plus ALLC and D plus `extra`, in cdata order; returns sup, U, loc."""
    sup = np.union1d(np.nonzero(init_full)[0], [d['iC'], d['iD']] + list(extra)).astype(np.int64)
    V = d['V'][np.ix_(sup, sup)].astype(np.int64)
    U = PDP[V, V.T]
    loc = {int(g): j for j, g in enumerate(sup)}
    return sup, U, loc


def _dup(U, base_idx):
    """Append duplicate classes (payoff-identical copies of the local classes in base_idx) to U."""
    K = U.shape[0]
    ext = list(range(K)) + list(base_idx)
    return np.ascontiguousarray(U[np.ix_(ext, ext)])


TYPES = SL.TYPES
ALLOC = {0: 1500, 1: 1500, 2: 750, 3: 750, 4: 750, 5: 750, 6: 3000}     # backgrounds per pair per (n, N) at 3,000/type


def forced_job(j):
    """One background: (i) faker run with tagged target and faker founders, to tau then to local freeze;
    (ii) ghost run (faker founder -> ghost), to max(tau, 40 generations); common random numbers."""
    n, N, pi, rep = j
    d = SC.cdata(n); mu = d['mu']
    P = SC.forced_pairs(n)[pi]
    t, q = P['t'], P['q']
    rng = np.random.default_rng([n, N, pi, rep, SALT_FRC])
    bg = rng.multinomial(N, mu).astype(np.int64)
    slots = np.repeat(np.arange(d['K']), bg)
    perm = rng.permutation(N)
    seed = int(1000003 * rep + 7 * N + 13 * n + 101 * pi + SALT_FRC % 100000)
    init = bg.copy()
    init[slots[perm[0]]] -= 1
    init[slots[perm[10]]] -= 1
    sup, U, loc = _local(d, init, [t, q])
    K = len(sup)
    U2 = _dup(U, [loc[t], loc[q]])
    iT, iF = K, K + 1
    ini = np.concatenate([init[sup], [1, 1]]).astype(np.int64)
    xA = ini[loc[d['iC']]] / N; xD = ini[loc[d['iD']]] / N
    rf = run_island(U2, ini, N, seed, loc[d['iC']], -1, (iT, iF), mode=1, horizon=GENS)
    rg = run_island(U2, ini, N, seed, loc[d['iC']], iF, (iT, iF), mode=0, stop_gen=int(SNAPS[-1]), horizon=GENS)
    ct, cf = rf['counts_tau'], rf['counts']
    fin = np.nonzero(cf)[0]
    base = np.concatenate([sup, [t, q]])
    fb = base[fin]
    coop_fix = bool(np.all(d['V'][np.ix_(fb, fb)] == 1))
    out = dict(n=n, N=N, pair=pi, rep=rep, bg_t=int(bg[t]), bg_q=int(bg[q]), xA=float(xA), xD=float(xD),
               inE=bool(xA >= 0.3 and xD >= 0.3),
               f=dict(st_tau=int(rf['st_tau']), tau=round(float(rf['tau']), 3), IA=float(rf['IA']),
                      A=bool(ct[loc[t]] + ct[iT] > 0), Fc=bool(ct[loc[q]] + ct[iF] > 0), kT=int(ct[iT]), kF=int(ct[iF]),
                      kt_class=int(ct[loc[t]] + ct[iT]), kq_class=int(ct[loc[q]] + ct[iF]),
                      phiE=[float(x) for x in rf['phiE_tau']], phiP=[float(x) for x in rf['phiP_tau']],
                      R=[float(x) for x in rf['R_tau']], Lam=[float(x) for x in rf['Lam_tau']],
                      kmaxT=int(rf['kmax'][iT]), kmaxF=int(rf['kmax'][iF]),
                      hitT=[float(rf['hit1'][0]), float(rf['hit2'][0])], hitF=[float(rf['hit1'][1]), float(rf['hit2'][1])],
                      st_fin=int(rf['st_fin']), gend=int(rf['gend']),
                      S=bool(cf[loc[t]] + cf[iT] > 0), Sq=bool(cf[loc[q]] + cf[iF] > 0), coop_fix=coop_fix),
               g=dict(st_tau=int(rg['st_tau']), tau=round(float(rg['tau']), 3), kG_tau=int(rg['k_tau'][1]),
                      kT_tau=int(rg['k_tau'][0]), ksnap=[int(x) for x in rg['ksnap'][1]],
                      phisnap=[float(x) for x in rg['phisnap'][1]], phiE=float(rg['phiE_tau'][1]),
                      phiP=float(rg['phiP_tau'][1]), hit=[float(rg['hit1'][1]), float(rg['hit2'][1])],
                      kmax=int(rg['kmax'][iF]), st_fin=int(rg['st_fin'])))
    return out


def dsea_job(j):
    """reps runs of k prover copies (FairBot payoffs) in an all-D island of N; the seeds_in_n kernel, to local freeze."""
    N, k, block, reps = j
    U = np.array([[0.0, -1.0, 0.0], [-1.0, -1.0, 1.0], [0.0, -2.0, 0.0]])    # prover, D, ALLC (absent)
    fix = 0; ext = 0; other = 0; gens = []
    for r in range(reps):
        seed = int(SALT_DSEA % 100000 + 7919 * N + 104729 * k + 1000003 * (block * reps + r))
        ini = np.array([k, N - k, 0], np.int64)
        o = run_island(U, ini, N, seed, 2, -1, (), mode=1, horizon=GENS)
        c = o['counts']
        if c[0] == N:
            fix += 1; gens.append(int(o['gend']))
        elif c[0] == 0:
            ext += 1
        else:
            other += 1
    return dict(N=N, k=k, block=block, reps=reps, fix=fix, ext=ext, other=other, fix_gens=gens)


def lottery_job(j):
    """One iid island at cutoff n, every establisher founder its own tagged class; to tau, then to local freeze."""
    n, N, rep = j
    d = SC.cdata(n); mu = d['mu']; V = d['V']; est = d['est']
    rng = np.random.default_rng([n, N, rep, SALT_LOT])
    init = rng.multinomial(N, mu).astype(np.int64)
    seed = int(1000003 * rep + 7 * N + 13 * n + SALT_LOT % 100000)
    E = np.nonzero(init * est)[0]
    founders = []
    for e in E:
        founders += [int(e)] * int(init[e])
    init2 = init.copy(); init2[E] = 0
    sup, U, loc = _local(d, init2, [])
    K = len(sup)
    allb = np.concatenate([sup, np.array(founders, np.int64)]).astype(np.int64)
    Vl = V[np.ix_(allb, allb)].astype(np.int64)
    U2 = PDP[Vl, Vl.T]
    ini = np.concatenate([init2[sup], np.ones(len(founders), np.int64)]).astype(np.int64)
    t0 = time.time()
    o = run_island(U2, ini, N, seed, loc[d['iC']], -1, (), mode=1, horizon=GENS)
    ct, cf = o['counts_tau'], o['counts']
    fin = np.nonzero(cf)[0]; fb = allb[fin]
    coop_fix = bool(np.all(V[np.ix_(fb, fb)] == 1))
    cnt = cf[fin].astype(float); M = (V[np.ix_(fb, fb)] * V[np.ix_(fb, fb)].T).astype(float)
    pcc = float((cnt @ M @ cnt - (cnt * np.diag(M)).sum()) / (N * (N - 1)))
    fk = [(int(founders[i]), int(ct[K + i]), int(o['kmax'][K + i])) for i in range(len(founders))]
    other = {int(allb[c]): int(ct[c]) for c in range(K) if ct[c] > 0 and allb[c] not in (d['iC'], d['iD'])}
    fin_d = {}
    for c in fin:
        fin_d[int(allb[c])] = fin_d.get(int(allb[c]), 0) + int(cf[c])
    return dict(n=n, N=N, rep=rep, st_tau=int(o['st_tau']), tau=round(float(o['tau']), 3), IA=float(o['IA']),
                xA0=float(init[d['iC']] / N), xD0=float(init[d['iD']] / N), n_founders=len(founders),
                founders=fk, D_tau=int(ct[loc[d['iD']]]), C_tau=int(ct[loc[d['iC']]]), other_tau=other,
                st_fin=int(o['st_fin']), gend=int(o['gend']), coop_fix=coop_fix, pcc=pcc, final=fin_d,
                time_s=time.time() - t0)


def test_main(a):
    """(1) With no ghost and no tags the kernel reproduces seeds_in_n._run draw for draw (stop generation, final counts).
    (2) The D-sea kernel against the exact formula (u_1, N = 100).
    (3) Martingale identities on a few forced runs: E[k_tau e^{Lam}] = k0 exactly (event clock)."""
    import seeds_in_n as SN
    ok = True
    for n, N in ((6, 100), (6, 400), (9, 100)):
        dd = SN.data(n)
        for rep in range(4):
            rng = np.random.default_rng([n, N, rep, 4242])
            init = rng.multinomial(N, dd['mu'])[None, :].astype(np.int64)
            A = SN._run(dd['U'], dd['PCC'], init, N, W, 0.0, GENS, EVERY, 31 + rep, dd['iC'], dd['coopmask'],
                        dd['coremask'], 0)
            B = run_island(dd['U'], init[0], N, 31 + rep, dd['iC'], -1, (), mode=1, horizon=GENS)
            same = int(A[1]) == int(B['gend']) and np.array_equal(A[2][0], B['counts'])
            ok &= same
            print('identity n=%d N=%d rep %d: %s (stop %d vs %d)' % (n, N, rep, 'same' if same else 'DIFFERENT', A[1],
                  B['gend']), flush=True)
    print('IDENTITY', 'OK' if ok else 'FAILED', flush=True)
    r = dsea_job((100, 1, 999, 20000))
    p = r['fix'] / r['reps']; lo, hi = SL._wilson(r['fix'], r['reps'])[1:]
    print('D-sea N=100 k=1: %.4f [%.4f, %.4f] exact %.4f' % (p, lo, hi, u_exact(100, [1])[0]), flush=True)
    rows = [forced_job((9, 100, pi, rep)) for pi in (2, 0) for rep in range(300)]
    for who, ix in (('target', 0), ('faker', 1)):
        kk = np.array([r['f']['kT'] if ix == 0 else r['f']['kF'] for r in rows])
        lam = np.array([r['f']['Lam'][ix] for r in rows]); RE = np.array([r['f']['R'][ix] for r in rows])
        print('%s: E[k e^Lam] = %.3f +- %.3f ; E[k e^-R_event] = %.3f ; P(alive) = %.3f' % (
            who, np.mean(kk * np.exp(lam)), np.std(kk * np.exp(lam)) / np.sqrt(len(kk)), np.mean(kk * np.exp(-RE)),
            np.mean(kk > 0)), flush=True)


def timing_main(a):
    for N in (100, 400, 1600):
        t0 = time.time(); k = 0
        for pi in (0, 2, 6):
            for rep in range(a.reps or 6):
                forced_job((9, N, pi, 900000 + rep)); k += 1
        print('forced N=%d: %.3fs per background' % (N, (time.time() - t0) / k), flush=True)
    for N in (100, 400, 1600, 6400):
        t0 = time.time(); m = 4 if N < 6400 else 2
        rr = [lottery_job((9, N, 900000 + r)) for r in range(m)]
        print('lottery N=%d: %.2fs per island; outcomes %s' % (N, (time.time() - t0) / m, [r['coop_fix'] for r in rr]),
              flush=True)


FCOLS = ['n', 'N', 'pair', 'rep', 'bg_t', 'bg_q', 'inE', 'xA', 'xD', 'st_tau', 'tau', 'IA', 'A', 'Fc', 'kT', 'kF', 'kt_class',
         'kq_class', 'phiE_T', 'phiE_F', 'phiP_T', 'phiP_F', 'R_T', 'R_F', 'Lam_T', 'Lam_F', 'kmaxT', 'kmaxF', 'hitT1',
         'hitT2', 'hitF1', 'hitF2', 'st_fin', 'gend', 'S', 'Sq', 'coop_fix',
         'g_st_tau', 'g_tau', 'g_kG_tau', 'g_kT_tau', 'g_k5', 'g_k10', 'g_k20', 'g_k40', 'g_phi5', 'g_phi10', 'g_phi20',
         'g_phi40', 'g_phiE', 'g_phiP', 'g_hit1', 'g_hit2', 'g_kmax', 'g_st_fin']
NBG_TYPE = 10000         # backgrounds per (N, n, type): the spec's 3,000 (salt block 0) plus a declared 7,000 extension


def _flat(r):
    f, g = r['f'], r['g']
    return [r['n'], r['N'], r['pair'], r['rep'], r['bg_t'], r['bg_q'], r['inE'], r['xA'], r['xD'], f['st_tau'], f['tau'],
            f['IA'], f['A'], f['Fc'], f['kT'], f['kF'], f['kt_class'], f['kq_class'], f['phiE'][0], f['phiE'][1],
            f['phiP'][0], f['phiP'][1], f['R'][0], f['R'][1], f['Lam'][0], f['Lam'][1], f['kmaxT'], f['kmaxF'],
            f['hitT'][0], f['hitT'][1], f['hitF'][0], f['hitF'][1], f['st_fin'], f['gend'], f['S'], f['Sq'], f['coop_fix'],
            g['st_tau'], g['tau'], g['kG_tau'], g['kT_tau']] + g['ksnap'] + g['phisnap'] + [g['phiE'], g['phiP'],
            g['hit'][0], g['hit'][1], g['kmax'], g['st_fin']]


FROWS = os.path.join(RUNS, 'demographic-lemma-forced.npz')        # gitignored (runs/*.npz); aggregates go to the json
LROWS = os.path.join(RUNS, 'demographic-lemma-lottery.json.gz')
DROWS = os.path.join(RUNS, 'demographic-lemma-dsea.json')


def _forced_flat(j):
    return _flat(forced_job(j))


def _warm():
    for n in SC.NS:
        SC.cdata(n)


def forced_main(a):
    from multiprocessing import Pool
    scale = {pi: ALLOC[pi] * NBG_TYPE // 3000 for pi in ALLOC}
    jobs = [(n, N, pi, rep) for N in NS_N for n in SC.NS for pi in range(7) for rep in range(scale[pi])]
    print('%d forced backgrounds' % len(jobs), flush=True)
    t0 = time.time(); out = []
    with Pool(a.procs, initializer=_warm) as pool:
        for i, r in enumerate(pool.imap_unordered(_forced_flat, jobs, chunksize=50)):
            out.append(r)
            if (i + 1) % 20000 == 0:
                print('%d / %d, %.0fs' % (i + 1, len(jobs), time.time() - t0), flush=True)
    X = np.array(out, dtype=np.float64)
    X = X[np.lexsort((X[:, 3], X[:, 2], X[:, 0], X[:, 1]))]
    np.savez_compressed(FROWS, X=X, cols=np.array(FCOLS))
    print('done %d in %.0fs' % (len(out), time.time() - t0), flush=True)


DSEA_CELLS = [(100, 10000), (400, 10000), (1600, 10000), (6400, 4000)]
DSEA_K = (1, 2, 4, 8, 16)


def dsea_main(a):
    from multiprocessing import Pool
    jobs = []
    for N, reps in DSEA_CELLS:
        for k in DSEA_K:
            nb = 20
            for b in range(nb):
                jobs.append((N, k, b, reps // nb))
    t0 = time.time()
    with Pool(a.procs) as pool:
        rows = pool.map(dsea_job, jobs, chunksize=1)
    json.dump(rows, open(DROWS, 'w'))
    print('done %d blocks in %.0fs' % (len(rows), time.time() - t0), flush=True)


LOT_CELLS = [(100, 4000), (400, 4000), (1600, 4000), (6400, 1000), (25600, 400)]
LOT_N = 9


def lottery_main(a):
    from multiprocessing import Pool
    only = set(int(x) for x in a.only.split(',')) if a.only else None
    rows = []
    if os.path.exists(LROWS):
        rows = json.load(gzip.open(LROWS, 'rt'))
    done = {(r['N'], r['rep']) for r in rows}
    jobs = [(LOT_N, N, rep) for N, reps in LOT_CELLS for rep in range(reps)
            if (only is None or N in only) and (N, rep) not in done]
    jobs.sort(key=lambda j: -j[1])
    print('%d lottery islands' % len(jobs), flush=True)
    t0 = time.time()
    with Pool(a.procs, initializer=_warm) as pool:
        for i, r in enumerate(pool.imap_unordered(lottery_job, jobs, chunksize=4)):
            rows.append(r)
            if (i + 1) % 1000 == 0 or (r['N'] >= 6400 and (i + 1) % 50 == 0):
                print('%d / %d, %.0fs' % (i + 1, len(jobs), time.time() - t0), flush=True)
                with gzip.open(LROWS, 'wt') as f:
                    json.dump(rows, f)
    rows.sort(key=lambda r: (r['N'], r['rep']))
    with gzip.open(LROWS, 'wt') as f:
        json.dump(rows, f)
    print('done %d in %.0fs' % (len(jobs), time.time() - t0), flush=True)


# ------------------------------------------------------------------ analysis helpers
def wilson(k, n, z=1.96):
    return SL._wilson(int(k), int(n), z)


def boot_ci(fn, arrays, B=2000, seed=0, alpha=0.05):
    """Percentile bootstrap over rows (each array indexed by row)."""
    rng = np.random.default_rng(seed)
    n = len(arrays[0])
    if n == 0:
        return (float('nan'), float('nan'))
    vals = []
    for _ in range(B):
        ix = rng.integers(0, n, n)
        v = fn(*[x[ix] for x in arrays])
        if np.isfinite(v):
            vals.append(v)
    if not vals:
        return (float('nan'), float('nan'))
    return (float(np.quantile(vals, alpha / 2)), float(np.quantile(vals, 1 - alpha / 2)))


PHI_GRID = np.concatenate([np.arange(1.0, 10.0, 0.25), np.arange(10.0, 100.0, 1.0), np.geomspace(100.0, 1e8, 120)])


def lemmaDp_bound(phi, k0=1, upper=False):
    """Binned Lemma D' bound: P(alive at tau) <= sum_i min(P(Phi in [phi_i, phi_{i+1})), 1 - (1 - 1/phi_i)^k0).
    upper=True replaces each bin probability by its Wilson upper bound (conservative)."""
    phi = np.asarray(phi); n = len(phi)
    edges = np.concatenate([PHI_GRID, [np.inf]])
    cnt, _ = np.histogram(phi, bins=edges)
    tot = 0.0
    for i in range(len(PHI_GRID)):
        p = cnt[i] / n
        if upper and cnt[i] > 0:
            p = wilson(cnt[i], n)[2]
        tot += min(p, 1 - (1 - 1 / PHI_GRID[i]) ** k0)
    return min(1.0, tot)


def b1_bound(lam, k0=1):
    """B1 (notes/scramble-lemma.md): inf_L [P(Lam < L) + k0 e^{-L}] (event-clock exponential martingale)."""
    lam = np.asarray(lam)
    return float(min(1.0, min(np.mean(lam < L) + k0 * math.exp(-L) for L in np.arange(0.0, 8.0, 0.02))))


def r_env(tau, a, f, nb=10):
    """Shared-background part of the association: E[s_A(tau) s_F(tau)]/(E[s_A] E[s_F]) with tau in quantile bins."""
    qs = np.quantile(tau, np.linspace(0, 1, nb + 1)); qs[-1] += 1e-9
    b = np.clip(np.searchsorted(qs, tau, side='right') - 1, 0, nb - 1)
    sa = np.array([a[b == i].mean() if (b == i).any() else 0 for i in range(nb)])
    sf = np.array([f[b == i].mean() if (b == i).any() else 0 for i in range(nb)])
    w = np.array([(b == i).mean() for i in range(nb)])
    den = (w * sa).sum() * (w * sf).sum()
    return float((w * sa * sf).sum() / den) if den > 0 else float('nan')


def _ratio_r(a, f):
    pa = a.mean(); pf = f.mean()
    return (a & f).mean() / pa / pf if pa > 0 and pf > 0 else float('nan')


def load_forced():
    z = np.load(FROWS)
    X = z['X']; cols = [str(c) for c in z['cols']]
    return {c: X[:, i] for i, c in enumerate(cols)}


def _mf_path(xA0=0.466, xD0=0.466, w=W, dt=1e-3, T=200.0):
    """Mean-field R(t), Phi(t) = 1 + int e^{-R} for a payoff-neutral ALLC-cooperating establisher (curvature only)."""
    xA = xA0 / (xA0 + xD0); xD = 1 - xA
    ts = [0.0]; Rs = [0.0]; Ph = [1.0]
    R = 0.0; P = 1.0; t = 0.0
    while t < T:
        pA = -2 * xD; pD = xA - xD; pe = -xD
        fA, fD, fe = math.exp(w * pA), math.exp(w * pD), math.exp(w * pe)
        Fb = xA * fA + xD * fD
        P += math.exp(-R) * dt
        R += (fe / Fb - 1) * dt
        xA += xA * (fA / Fb - 1) * dt; xD = 1 - xA
        t += dt
        if abs(t - round(t, 1)) < dt / 2:
            ts.append(t); Rs.append(R); Ph.append(P)
    return np.array(ts), np.array(Rs), np.array(Ph)


def _fmt(p):
    return '%.4f [%.4f, %.4f]' % tuple(p)


def report_dsea(md, J):
    rows = json.load(open(DROWS))
    agg = {}
    for r in rows:
        a = agg.setdefault((r['N'], r['k']), [0, 0, 0, []])
        a[0] += r['fix']; a[1] += r['reps']; a[2] += r['other']; a[3] += r['fix_gens']
    out = {}
    md += ['## Task 3(a)-(b): escape from a D sea (u_k)', '',
           'Seeds_in_n kernel on {prover k, D N − k}, run to local freeze (no unresolved run). Exact = birth–death formula;',
           'diffusion = erf form; independent copies = 1 − (1 − u₁)^k.', '',
           '| N | k | runs | measured u_k [95%] | exact | diffusion | 1 − (1 − u₁)^k | k·u₁ | exact in interval | median fixation gen |',
           '|---|---|---|---|---|---|---|---|---|---|']
    nin = 0; ncell = 0
    for (N, k), (f, n, o, g) in sorted(agg.items()):
        ue = float(u_exact(N, [k])[0]); u1 = float(u_exact(N, [1])[0])
        p = wilson(f, n)
        ud = float(u_diffusion(k / N, N))
        inside = p[1] <= ue <= p[2]
        nin += inside; ncell += 1
        out['%d/%d' % (N, k)] = dict(runs=n, fix=f, other=o, u=p, exact=ue, diffusion=ud, indep=1 - (1 - u1) ** k,
                                     linear=k * u1, exact_inside=bool(inside), median_fix_gen=float(np.median(g)) if g else None)
        md.append('| %d | %d | %d | %s | %.4f | %.4f | %.4f | %.4f | %s | %s |' % (
            N, k, n, _fmt(p), ue, ud, 1 - (1 - u1) ** k, k * u1, 'yes' if inside else 'NO',
            '%.0f' % np.median(g) if g else '–'))
    md += ['', 'Exact value inside the 95%% interval in %d of %d cells. u₁ measured/diffusion: %s.' % (
        nin, ncell, ', '.join('%.3f (N = %d)' % (out['%d/1' % N]['u'][0] / out['%d/1' % N]['diffusion'], N)
                              for N in (100, 400, 1600, 6400))), '']
    J['dsea'] = out


def report_ghost(md, J, F):
    E = F['inE'] > 0
    out = {}
    md += ['## Task 1: Lemma D against the ghost (fitness pinned to the mean), fixed time and stopped', '',
           'Ghost runs: the faker founder of every forced background replaced by a ghost (plays as the faker, fitness =',
           'population mean, so r ≡ 0 and d = 1 − k/N exactly), common random numbers with the faker run, all 7 pairs and',
           '3 cutoffs pooled (the ghost\'s survival does not depend on its payoffs except through others), in E.',
           'Bound = event-clock Lemma D (notes §1.4) for the process killed at K; "killed alive" = alive at t and K not hit by t.', '',
           '| N | t | backgrounds | alive (unkilled) | ratio to 1/(1+t) | killed at N/20: alive | bound | killed at N/4: alive | bound | P(hit N/4 by t) | k₀/K (N/4) |',
           '|---|---|---|---|---|---|---|---|---|---|---|']
    for N in NS_N:
        m = E & (F['N'] == N)
        n = int(m.sum())
        for i, t in enumerate(SNAPS):
            k = F['g_k%d' % t][m]
            h1 = F['g_hit1'][m]; h2 = F['g_hit2'][m]
            al = k > 0
            kill1 = al & ((h1 < 0) | (h1 > t)); kill2 = al & ((h2 < 0) | (h2 > t))
            hit2 = (h2 >= 0) & (h2 <= t)
            p = wilson(al.sum(), n); p1 = wilson(kill1.sum(), n); p2 = wilson(kill2.sum(), n); ph = wilson(hit2.sum(), n)
            b1 = lemmaD_event_bound(N, int(t), 1, N // 20)['bound']; b2 = lemmaD_event_bound(N, int(t), 1, N // 4)['bound']
            rec = dict(n=n, alive=p, ratio_1_over_1pt=p[0] * (1 + t), ratio_ci=(p[1] * (1 + t), p[2] * (1 + t)),
                       killed_N20=p1, bound_N20=b1, killed_N4=p2, bound_N4=b2, hit_N4=ph, k0_over_K=4.0 / N,
                       exceeds_N20=bool(p1[1] > b1), exceeds_N4=bool(p2[1] > b2))
            out['%d/%d' % (N, t)] = rec
            md.append('| %d | %d | %d | %s | %.3f [%.3f, %.3f] | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f |' % (
                N, t, n, _fmt(p), rec['ratio_1_over_1pt'], *rec['ratio_ci'], p1[0], b1, p2[0], b2, ph[0], 4.0 / N))
    md += ['', '**Stopped version** (ghost alive at its own run\'s τ = ALLC extinction ∧ freeze ∧ 2,000 generations), by stopping',
           'reason; Lemma D′ bound from the measured Φ_τ (Poisson clock, binned); lower-tail decomposition',
           'inf_t₁ [Lemma D(t₁, K = N/4) + P(hit N/4 by t₁) + P(τ < t₁)] with the measured lower tail of τ.', '',
           '| N | reason | islands | ghost alive at τ | median τ | E[1/(1+τ)] | Lemma D′ bound | lower-tail bound |',
           '|---|---|---|---|---|---|---|---|']
    for N in NS_N:
        m = E & (F['N'] == N)
        tau = F['g_tau'][m]; al = F['g_kG_tau'][m] > 0; st = F['g_st_tau'][m]; phi = F['g_phiP'][m]
        for lab, sel in (('all', np.ones(len(st), bool)), ('ALLC extinct', st == 1), ('frozen', st == 2), ('cap', st == 3)):
            if sel.sum() == 0:
                md.append('| %d | %s | 0 | – | – | – | – | – |' % (N, lab)); continue
            p = wilson(al[sel].sum(), sel.sum())
            bD = lemmaDp_bound(phi[sel])
            best = 1.0
            for t1 in np.arange(1.0, 40.0, 0.5):
                b = 1 / (1 + (1 - (N // 4 - 1) / N) * t1) + 4.0 / N + np.mean(tau[sel] < t1)
                best = min(best, b)
            out['stopped/%d/%s' % (N, lab)] = dict(n=int(sel.sum()), alive=p, tau_median=float(np.median(tau[sel])),
                                                   E_inv=float(np.mean(1 / (1 + tau[sel]))), lemmaDp=bD, lowertail=best)
            md.append('| %d | %s | %d | %s | %.1f | %.4f | %.4f | %.4f |' % (N, lab, sel.sum(), _fmt(p), np.median(tau[sel]),
                      np.mean(1 / (1 + tau[sel])), bD, best))
    md.append('')
    J['ghost'] = out


TYPE_OF = {0: 'disadvantaged', 1: 'disadvantaged', 2: 'neutral', 3: 'neutral', 4: 'neutral', 5: 'neutral', 6: 'advantaged'}
TYPE_LIST = ('disadvantaged', 'neutral', 'advantaged')


def _typemask(F, typ):
    return np.isin(F['pair'], [p for p, t in TYPE_OF.items() if t == typ])


def report_forced(md, J, F):
    """Task 2 (r_q, Lemma D' on fakers, combined bound) and the target founder's E[k_tau] (Task 3c, RE 4)."""
    E = F['inE'] > 0
    out = {}
    md += ['## Task 2: per-founder dependence r_q, Lemma D′ on faker founders, and the combined bound', '',
           'Forced backgrounds (one tagged target founder, one tagged faker founder; scramble-lemma pairs), in E.',
           'A = target class alive at τ; F_j = the tagged faker founder alive at τ; r = P(F_j | A)/P(F_j) (bootstrap 95%);',
           'r_env = the τ-binned shared-background value; Lemma D′ = binned bound on P(F_j) from the measured Φ_τ (Poisson',
           'clock); B1 = the exponential-martingale bound of the scramble lemma, for comparison; ghost = P(ghost alive at τ).', '']
    hdr = ('| N | type | n | bgs | stop 1/2/3 | P(A) | P(F_j) | joint events | r [95%] | r_env | Lemma D′ (×) | B1 | ghost |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    md += list(hdr)
    for N in NS_N:
        for typ in TYPE_LIST:
            for nsel in SC.NS + ('pooled',):
                m = E & (F['N'] == N) & _typemask(F, typ)
                if nsel != 'pooled':
                    m &= F['n'] == nsel
                A = F['A'][m] > 0; Fj = F['kF'][m] > 0; tau = F['tau'][m]
                st = F['st_tau'][m]
                n = int(m.sum())
                r = _ratio_r(A, Fj)
                ci = boot_ci(_ratio_r, [A, Fj], B=1000, seed=N + len(typ) + (0 if nsel == 'pooled' else nsel))
                re = r_env(tau, A.astype(float), Fj.astype(float))
                bD = lemmaDp_bound(F['phiP_F'][m]); bDc = lemmaDp_bound(F['phiP_F'][m], upper=True)
                bB1 = b1_bound(F['Lam_F'][m])
                gh = (F['g_kG_tau'][m] > 0).mean()
                blk = m & (F['rep'] < np.vectorize(lambda p: ALLOC[int(p)])(F['pair']))
                A3 = F['A'][blk] > 0; F3 = F['kF'][blk] > 0
                rec = dict(n=n, stop={str(s): int((st == s).sum()) for s in (1, 2, 3)}, PA=wilson(A.sum(), n),
                           PF=wilson(Fj.sum(), n), joint=int((A & Fj).sum()), r=r, r_ci=ci, r_env=re,
                           r_3000=_ratio_r(A3, F3), n_3000=int(blk.sum()), joint_3000=int((A3 & F3).sum()),
                           lemmaDp=bD, lemmaDp_cons=bDc, B1=bB1, ghost=float(gh),
                           tau_median=float(np.median(tau)), tau_cv=float(np.std(tau) / np.mean(tau)),
                           martingale_F=float(np.mean(F['kF'][m] * np.exp(F['Lam_F'][m]))),
                           martingale_T=float(np.mean(F['kT'][m] * np.exp(F['Lam_T'][m]))))
                out['%d/%s/%s' % (N, typ, nsel)] = rec
                md.append('| %d | %s | %s | %d | %s | %.3f | %.4f | %d | %.2f [%.2f, %.2f] | %.3f | %.4f (%.2f×) | %s | %.4f |' % (
                    N, typ, nsel, n, '/'.join(str(rec['stop'][s]) for s in '123'), rec['PA'][0], rec['PF'][0], rec['joint'],
                    r, ci[0], ci[1], re, bD, bD / rec['PF'][0] if rec['PF'][0] > 0 else float('nan'),
                    '%.3f' % bB1, gh))
    md.append('')
    J['r'] = out
    # ---- the combined bound
    md += ['### The combined per-island bound (confidence-qualified empirical bound, not a theorem)', '',
           'P(Est | E) ≥ ρ̃·[1 − E[K_q]·q̄·r·h^rel] (notes §3.1). Est = target class in the final support (faker runs, to',
           'local freeze); F = faker class alive at τ (for h); E[K_q] = 1 + mean bg_q; q̄ = Lemma D′ bound on the founder;',
           'point = all at estimates; cons = ρ̃ lower 95%, q̄ with Wilson-upper bins, r and h^rel upper 95%. "old" = the',
           'scramble lemma\'s form ρ̃ − P(F)·h⁺ with P(F) measured (its best case). P(Est) measured for comparison.', '',
           '| N | type | n | P(Est) | ρ̃ | h^rel | E[K_q] | q̄ (D′) | r | bound (point) | bound (cons) | old (measured P(F)) |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|']
    CB = {}
    for N in NS_N:
        for typ in TYPE_LIST:
            for nsel in SC.NS + ('pooled',):
                m = E & (F['N'] == N) & _typemask(F, typ)
                if nsel != 'pooled':
                    m &= F['n'] == nsel
                A = F['A'][m] > 0; Fc = F['Fc'][m] > 0; S = F['S'][m] > 0
                n = int(m.sum())
                pA = A.mean()
                pS_AFc = S[A & ~Fc].mean() if (A & ~Fc).any() else float('nan')
                pS_AF = S[A & Fc].mean() if (A & Fc).any() else float('nan')
                h = (pS_AFc - pS_AF) if (A & Fc).any() else 0.0
                hrel = max(h, 0) / pS_AFc if pS_AFc > 0 else float('nan')
                rho = pA * pS_AFc
                EK = 1 + F['bg_q'][m].mean()
                rr = out['%d/%s/%s' % (N, typ, nsel)]
                qb = rr['lemmaDp']; qbc = rr['lemmaDp_cons']
                r = rr['r']; rhi = rr['r_ci'][1]
                bp = rho * (1 - EK * qb * r * hrel)

                def _rho(a, s, fc):
                    sel = a & ~fc
                    return a.mean() * (s[sel].mean() if sel.any() else 0.0)

                def _hrel(a, s, fc):
                    s1 = s[a & ~fc]; s2 = s[a & fc]
                    if len(s1) == 0 or s1.mean() == 0: return float('nan')
                    return max((s1.mean() - (s2.mean() if len(s2) else s1.mean())), 0) / s1.mean()
                rlo = boot_ci(_rho, [A, S, Fc], B=500, seed=7 + N)[0]
                hhi = boot_ci(_hrel, [A, S, Fc], B=500, seed=9 + N)[1]
                bc = rlo * (1 - EK * qbc * rhi * hhi) if np.isfinite(hhi) else float('nan')
                old = rho - Fc.mean() * max(h, 0)
                rec = dict(n=n, P_Est=wilson(S.sum(), n), rho=rho, rho_lo=rlo, h=h, hrel=hrel, hrel_hi=hhi, EK=EK, qbar=qb,
                           qbar_cons=qbc, r=r, r_hi=rhi, bound_point=bp, bound_cons=bc, old_measuredF=old,
                           n_AF=int((A & Fc).sum()), P_Fc=float(Fc.mean()))
                CB['%d/%s/%s' % (N, typ, nsel)] = rec
                md.append('| %d | %s | %s | %.4f | %.4f | %.2f | %.2f | %.4f | %.2f | %.4f | %.4f | %.4f |' % (
                    N, typ, nsel, rec['P_Est'][0], rho, hrel, EK, qb, r, bp, bc, old))
    J['combined'] = CB
    md.append('')
    # ---- target founder: E[k_tau] per seeded copy (every target cooperates with ALLC)
    md += ['### Target founder: E[k_τ | E] per seeded copy (all forced targets cooperate with ALLC)', '',
           '| N | n | founders | P(alive at τ) | E[k_τ] [95%] | E[k_τ | alive] | e^{R_τ} mean | E[k e^{Λ}] (martingale) |',
           '|---|---|---|---|---|---|---|---|']
    KT = {}
    for N in NS_N:
        for nsel in SC.NS + ('pooled',):
            m = E & (F['N'] == N)
            if nsel != 'pooled':
                m &= F['n'] == nsel
            k = F['kT'][m]
            ci = boot_ci(lambda x: x.mean(), [k], B=1000, seed=N)
            rec = dict(n=int(m.sum()), alive=wilson((k > 0).sum(), m.sum()), Ek=float(k.mean()), Ek_ci=ci,
                       Ek_alive=float(k[k > 0].mean()) if (k > 0).any() else float('nan'),
                       eR=float(np.mean(np.exp(F['R_T'][m]))), mart=float(np.mean(k * np.exp(F['Lam_T'][m]))))
            KT['%d/%s' % (N, nsel)] = rec
            md.append('| %d | %s | %d | %.4f | %.3f [%.3f, %.3f] | %.1f | %.3f | %.3f |' % (
                N, nsel, rec['n'], rec['alive'][0], rec['Ek'], *ci, rec['Ek_alive'], rec['eR'], rec['mart']))
    J['target_ktau'] = KT
    md.append('')


def _block(d, classes_counts):
    """Largest mutually-cooperating block among establisher classes (greedy by count): returns the class set."""
    V = d['V']
    blk = []
    for c, _ in sorted(classes_counts.items(), key=lambda t: -t[1]):
        if all(V[c, b] == 1 and V[b, c] == 1 for b in blk):
            blk.append(c)
    return blk


def report_lottery(md, J, F):
    rows = json.load(gzip.open(LROWS, 'rt'))
    d = SC.cdata(LOT_N); V = d['V']; mu = d['mu']; iC = d['iC']; nm = d['names']
    mu_est = float(mu[d['est']].sum())
    ts, Rs, Ph = _mf_path()
    out = {}
    md += ['## Task 3(c)-(e): the iid lottery with per-founder tags (n = 9, I = 1, no migration)', '',
           'Every establisher founder is its own payoff-identical tagged class. Outcome = cooperative fixation (every final',
           'pair mutually cooperates); efficient = final P(C,C) ≥ 0.95. τ = ALLC extinction ∧ local freeze ∧ 2,000; final',
           'stop = local freeze (5) or the 10⁵ horizon (6). μ_est = %.4f (n = 9).' % mu_est, '',
           '| N | islands | coop. fixation [95%] | efficient | τ stop 1/2/3 | final 5/6 | median τ [10–90%] | founders/island |',
           '|---|---|---|---|---|---|---|---|']
    byN = {}
    for r in rows:
        byN.setdefault(r['N'], []).append(r)
    for N in sorted(byN):
        R = byN[N]
        n = len(R)
        cf = np.array([r['coop_fix'] for r in R]); ef = np.array([r['pcc'] >= 0.95 for r in R])
        st = np.array([r['st_tau'] for r in R]); sf = np.array([r['st_fin'] for r in R]); tau = np.array([r['tau'] for r in R])
        nf = np.array([r['n_founders'] for r in R])
        rec = dict(n=n, coop=wilson(cf.sum(), n), eff=wilson(ef.sum(), n), st_tau={str(s): int((st == s).sum()) for s in (1, 2, 3)},
                   st_fin={str(s): int((sf == s).sum()) for s in (5, 6)}, tau_q=[float(np.quantile(tau, p)) for p in (0.1, 0.5, 0.9)],
                   founders_mean=float(nf.mean()), coop_eq_eff=int((cf == ef).sum()))
        if N == 6400:
            cf200 = np.array([r['coop_fix'] for r in R if r['rep'] < 200])
            rec['coop_first200'] = wilson(cf200.sum(), len(cf200))
        if N == 1600:
            cf2k = np.array([r['coop_fix'] for r in R if r['rep'] < 2000])
            rec['coop_first2000'] = wilson(cf2k.sum(), len(cf2k))
        out[str(N)] = rec
        md.append('| %d | %d | %s | %.4f | %s | %s | %.1f [%.1f, %.1f] | %.1f |' % (
            N, n, _fmt(rec['coop']), rec['eff'][0], '/'.join(str(rec['st_tau'][s]) for s in '123'),
            '/'.join(str(rec['st_fin'][s]) for s in ('5', '6')), rec['tau_q'][1], rec['tau_q'][0], rec['tau_q'][2], rec['founders_mean']))
    md.append('')
    if '6400' in out:
        md.append('(6,400, 1): first 200 islands (the spec\'s cell) %s.' % _fmt(out['6400']['coop_first200']))
    if '1600' in out:
        md.append('(1,600, 1): first 2,000 islands (the spec\'s cell) %s.' % _fmt(out['1600']['coop_first2000']))
    md.append('')
    # ---- founders: E[k_tau] per seeded copy, split by ALLC cooperation
    md += ['### Establisher founders through the scramble (per seeded copy; islands in E, ALLC-extinction stops)', '',
           '| N | group | founders | P(alive at τ) | E[k_τ] [95%, islands resampled] | E[k_τ | alive] | P(max ≥ N/4 before τ) | E[u(k_τ)] / (u₁·E[k_τ]) |',
           '|---|---|---|---|---|---|---|---|']
    FK = {}
    for N in sorted(byN):
        R = [r for r in byN[N] if r['xA0'] >= 0.3 and r['xD0'] >= 0.3 and r['st_tau'] == 1]
        u = u_all(N)
        for grp in ('all', 'coopALLC', 'exploitALLC', 'BOX(THEM(ME))', 'BOX1(THEM(ME))', 'BOX(THEM(THEM))', 'BOX(THEM(^C))'):
            ks = []; isl = []; km = []
            for i, r in enumerate(R):
                for (c, k, kx) in r['founders']:
                    if grp == 'all' or (grp == 'coopALLC' and V[c, iC] == 1) or (grp == 'exploitALLC' and V[c, iC] == 0) or nm[c] == grp:
                        ks.append(k); isl.append(i); km.append(kx)
            if not ks:
                md.append('| %d | %s | 0 | – | – | – | – | – |' % (N, grp)); FK['%d/%s' % (N, grp)] = dict(n=0); continue
            ks = np.array(ks); isl = np.array(isl); km = np.array(km)
            # bootstrap over islands
            rng = np.random.default_rng(N)
            nI = len(R); sums = np.bincount(isl, weights=ks, minlength=nI); cnts = np.bincount(isl, minlength=nI)
            bs = []
            for _ in range(1000):
                ix = rng.integers(0, nI, nI)
                bs.append(sums[ix].sum() / max(cnts[ix].sum(), 1))
            ci = (float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975)))
            Ek = float(ks.mean())
            conc = float(u[np.minimum(ks, N)].mean() / (u[1] * Ek)) if Ek > 0 else float('nan')
            rec = dict(n=int(len(ks)), alive=wilson((ks > 0).sum(), len(ks)), Ek=Ek, Ek_ci=ci,
                       Ek_alive=float(ks[ks > 0].mean()) if (ks > 0).any() else float('nan'),
                       cap=float(np.mean(km >= N // 4)), concavity=conc)
            FK['%d/%s' % (N, grp)] = rec
            md.append('| %d | %s | %d | %.4f | %.3f [%.3f, %.3f] | %.1f | %.4f | %.3f |' % (
                N, grp, rec['n'], rec['alive'][0], Ek, *ci, rec['Ek_alive'], rec['cap'], conc))
    md.append('')
    J['founders'] = FK
    # ---- predictors
    md += ['### Predicting p(N)', '',
           '- **semi-empirical** (RE 3, spec (d)): each island\'s state at τ mapped through the exact two-type escape u_K of',
           '  the pooled count K of the largest mutually-cooperating establisher block (remainder treated as D); islands',
           '  frozen before ALLC extinction count at their (determined) outcome;',
           '- **independent founders after the scramble**: 1 − Π_j (1 − u_{k_j}) over the block\'s surviving founder lineages;',
           '- **p_corr** (closed-form compound model, S6): each island\'s founder count and τ, each founder alive with',
           '  probability 1/Φ(τ) and geometric with mean e^{R(τ)}Φ(τ) given alive (mean-field curvature path), pooled escape',
           '  u_K (40 Monte Carlo draws per island);',
           '- **naive** μ_est√(2cN/π); **independent-founder form** 1 − exp(−naive); **pooled-family form**',
           '  erf(μ_est√(Nc/2))/erf(√(Nc/2)).', '',
           '| N | measured | semi-empirical | ratio [95%] | indep. founders | p_corr | ratio | naive | 1 − e^{−naive} | pooled erf |',
           '|---|---|---|---|---|---|---|---|---|---|']
    PR = {}
    rng = np.random.default_rng(5)
    for N in sorted(byN):
        R = byN[N]; u = u_all(N)
        y = np.array([r['coop_fix'] for r in R], float)
        semi = np.zeros(len(R)); ind = np.zeros(len(R)); corr = np.zeros(len(R))
        for i, r in enumerate(R):
            if r['st_tau'] != 1:
                semi[i] = ind[i] = float(r['coop_fix'])
            else:
                cc = {}
                for (c, k, kx) in r['founders']:
                    if k > 0: cc[c] = cc.get(c, 0) + k
                blk = _block(d, cc) if cc else []
                Kb = sum(cc[c] for c in blk)
                semi[i] = u[min(Kb, N)]
                ind[i] = 1 - np.prod([1 - u[min(k, N)] for (c, k, kx) in r['founders'] if c in blk and k > 0])
            tau = r['tau']; M = r['n_founders']
            j = min(int(round(tau * 10)), len(ts) - 1)
            phi = Ph[j]; eR = math.exp(Rs[j])
            if M > 0:
                al = rng.binomial(M, 1 / phi, 40)
                Ks = np.array([rng.geometric(1 / max(eR * phi, 1.0), a).sum() if a > 0 else 0 for a in al])
                corr[i] = u[np.minimum(Ks, N)].mean()
        ps, pc, pi_ = semi.mean(), corr.mean(), ind.mean()
        rci = boot_ci(lambda a, b: a.mean() / b.mean(), [y, semi], B=1000, seed=N)
        naive = mu_est * math.sqrt(2 * C_SLOPE * N / math.pi)
        pooled = u_diffusion(mu_est, N)
        rec = dict(measured=float(y.mean()), semi=float(ps), ratio_semi=float(y.mean() / ps), ratio_semi_ci=rci,
                   indep_after=float(pi_), p_corr=float(pc), ratio_corr=float(y.mean() / pc), naive=naive,
                   indep_form=1 - math.exp(-naive), pooled_form=pooled,
                   calibration=[(float(lo), float(hi), int(((semi >= lo) & (semi < hi)).sum()),
                                 float(y[(semi >= lo) & (semi < hi)].mean()) if ((semi >= lo) & (semi < hi)).any() else None,
                                 float(semi[(semi >= lo) & (semi < hi)].mean()) if ((semi >= lo) & (semi < hi)).any() else None)
                                for lo, hi in ((0, 1e-9), (1e-9, 0.1), (0.1, 0.3), (0.3, 0.6), (0.6, 0.9), (0.9, 1.01))])
        PR[str(N)] = rec
        md.append('| %d | %.4f | %.4f | %.3f [%.3f, %.3f] | %.4f | %.4f | %.3f | %.4f | %.4f | %.4f |' % (
            N, rec['measured'], ps, rec['ratio_semi'], *rci, pi_, pc, rec['ratio_corr'], naive, 1 - math.exp(-naive), pooled))
    md.append('')
    md += ['Calibration of the semi-empirical predictor (islands binned by predicted u; measured rate | mean prediction):', '']
    for N in sorted(byN):
        md.append('- N = %d: ' % N + '; '.join('[%.2g, %.2g): %d islands, %s | %s' % (lo, hi, k, '%.3f' % m if m is not None else '–',
                                                                                     '%.3f' % p if p is not None else '–')
                                               for lo, hi, k, m, p in PR[str(N)]['calibration']))
    md.append('')
    # exponents over 100-1600
    Ns = [N for N in (100, 400, 1600) if str(N) in PR]
    if len(Ns) == 3:
        x = np.log(Ns)
        ex = {k: float(np.polyfit(x, np.log([PR[str(N)][k] for N in Ns]), 1)[0]) for k in ('measured', 'semi', 'p_corr', 'naive')}
        bs = []
        rngb = np.random.default_rng(11)
        Ys = {N: np.array([r['coop_fix'] for r in byN[N]], float) for N in Ns}
        for _ in range(1000):
            ps_ = [Ys[N][rngb.integers(0, len(Ys[N]), len(Ys[N]))].mean() for N in Ns]
            bs.append(np.polyfit(x, np.log(ps_), 1)[0])
        ex['measured_ci'] = (float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975)))
        PR['exponents'] = ex
        md.append('Fitted exponent of p over N = 100–1,600: measured %.3f [%.3f, %.3f]; semi-empirical %.3f; p_corr %.3f; naive %.3f.' % (
            ex['measured'], *ex['measured_ci'], ex['semi'], ex['p_corr'], ex['naive']))
        md.append('')
    J['lottery'] = out; J['predictors'] = PR


def report_extrap(md, J):
    """Extrapolated spoiler sum S_x(N) = N sum_type mu_type(x) qbar_type(N) r_type(N) h_type(N) for x in P (n = 12)."""
    d = SC.cdata(12); mu = d['mu']; nm = d['names']
    rr = J['r']; cb = J['combined']
    md += ['### Extrapolated spoiler sum for the members of P (natural seeding, n = 12)', '',
           'S_x(N) = N·Σ_type μ_type(x)·q̄_type(N)·r_type(N)·h^rel_type(N), with q̄ = Lemma D′ bound, r and h^rel measured',
           '(pooled over n) at N = 100, 400, 1,600 and extrapolated as power laws in N (r held at its N = 1,600 value if its',
           'fit is unstable). Non-positive h^rel counts as 0. FairBot\'s pair has no fakers, so S ≡ 0 (the sanity check).', '']
    fits = {}
    for typ in TYPE_LIST:
        Ns = np.array(NS_N, float)
        q = np.array([rr['%d/%s/pooled' % (N, typ)]['lemmaDp'] for N in NS_N])
        r = np.array([rr['%d/%s/pooled' % (N, typ)]['r'] for N in NS_N])
        h = np.array([max(cb['%d/%s/pooled' % (N, typ)]['hrel'], 1e-6) for N in NS_N])
        fq = np.polyfit(np.log(Ns), np.log(q), 1); fh = np.polyfit(np.log(Ns), np.log(h), 1)
        fits[typ] = dict(q=q.tolist(), r=r.tolist(), h=h.tolist(), q_slope=float(fq[0]), h_slope=float(fh[0]))
        fits[typ]['at'] = {}
        for N in (100, 400, 1600, 10000):
            qN = math.exp(np.polyval(fq, math.log(N))); hN = min(1.0, math.exp(np.polyval(fh, math.log(N))))
            fits[typ]['at'][str(N)] = dict(q=qN, h=hN, r=float(r[-1]))
    md.append('Fits: ' + '; '.join('%s q̄ ∝ N^%.2f, h^rel ∝ N^%.2f (h^rel = %s)' % (t, fits[t]['q_slope'], fits[t]['h_slope'],
                                                                                  '/'.join('%.2f' % v for v in fits[t]['h'])) for t in TYPE_LIST))
    md += ['', '| target x | μ fakers (disadv. / neutral / advant.) | S(100) | S(400) | S(1,600) | S(10⁴) extrapolated |', '|---|---|---|---|---|---|']
    out = {}
    for xs in SL.PFAM:
        x = nm.index(xs)
        fk = SC.fakers_of(d, x)
        mt = {t: 0.0 for t in TYPE_LIST}
        for q in fk:
            p = SC.d_profile(d, int(q))
            t = {'disadvantaged': 'disadvantaged', 'neutral': 'neutral', 'advantaged': 'advantaged'}.get(p, 'neutral')
            mt[t] += float(mu[q])
        S = {}
        for N in (100, 400, 1600, 10000):
            S[str(N)] = float(sum(N * mt[t] * fits[t]['at'][str(N)]['q'] * fits[t]['at'][str(N)]['r'] * fits[t]['at'][str(N)]['h']
                                  for t in TYPE_LIST))
        out[xs] = dict(mass=mt, S=S)
        md.append('| `%s` | %.4f / %.4f / %.4f | %.3f | %.3f | %.3f | %.3f |' % (
            xs, mt['disadvantaged'], mt['neutral'], mt['advantaged'], S['100'], S['400'], S['1600'], S['10000']))
    md.append('')
    J['extrapolation'] = dict(fits=fits, targets=out)


def report_main(a):
    J = _load()
    md = []
    if os.path.exists(DROWS):
        report_dsea(md, J)
    if os.path.exists(FROWS):
        F = load_forced()
        report_ghost(md, J, F)
        report_forced(md, J, F)
        report_extrap(md, J)
    else:
        F = None
    if os.path.exists(LROWS):
        report_lottery(md, J, F)
    json.dump(J, open(OUT_JSON, 'w'), indent=1, default=float)
    open(os.path.join(RUNS, 'demographic-lemma-tables.md'), 'w').write('\n'.join(md) + '\n')
    print('\n'.join(md))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('cmd'); ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--reps', type=int, default=0); ap.add_argument('--only', default=None)
    a = ap.parse_args()
    dict(static=static_main, test=test_main, timing=timing_main, forced=forced_main, dsea=dsea_main,
         lottery=lottery_main, report=report_main)[a.cmd](a)
