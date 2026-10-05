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


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('cmd'); ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--reps', type=int, default=0)
    a = ap.parse_args()
    dict(static=static_main)[a.cmd](a)
