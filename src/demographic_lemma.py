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
            fg = S / (N - kg) if kg > 0 else 0.0
            if ghost >= 0:
                wt[ghost] = fg
            Fbar = (S + kg * fg) / N
            # ---- instrumentation (state before the event), only up to tau
            if st_tau == 0 or mode == 0:
                dtp = _xs_exp(xs) / N
                for i in range(nt):
                    c = track[i]; kc = counts[c]
                    if c == ghost:
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
            if st_tau == 0:
                if counts[child] > kmax[child]: kmax[child] = counts[child]
                for i in range(nt):
                    c = track[i]
                    if c == child:
                        if hit1[i] < 0 and counts[c] >= K1: hit1[i] = g + (e + 1.0) / N
                        if hit2[i] < 0 and counts[c] >= K2: hit2[i] = g + (e + 1.0) / N
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


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('cmd'); ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--reps', type=int, default=0); ap.add_argument('--only', default=None)
    a = ap.parse_args()
    dict(static=static_main, test=test_main, timing=timing_main, forced=forced_main, dsea=dsea_main,
         lottery=lottery_main)[a.cmd](a)
