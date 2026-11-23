"""Queue 81, stage 0: the tiered fixation lemma (PROOFS P10) against simulation.

Spec specs/2026-11-23-tiered-best-response.md (stage 0, amendments); predictions
predictions/2026-11-23-tiered-best-response.md (RE 1, RE 2).

One focal slot (Moran, N individuals, fitness 1 - w + w * expected payoff, w = 0.3): residents p earn u = 1 against
everything except where stated; a variant p' earns the same against the natives (Delta_0 = 0) and 1 + Delta against a
tester q.  So f = 1 for the resident and sigma = (w / f) * m * T * Delta = w * m * T * Delta.

0a (assumption A by construction).  At every birth event in the focal slot each of the i variants independently met a
tester with probability eps = m T / N (Binomial(i, eps) testers met), so the variants' total weight is
i + w * Delta * Binomial(i, eps).  The event process is simulated as its embedded jump chain (only events that change
i are drawn; the per-state up/down probabilities are summed exactly over the binomial), which has the same fixation law.
Compared with (i) P10's finite-N formula rho = (1 - 1/r)/(1 - r^-N), r = 1 + w eps Delta, (ii) the exact value for
the realized event process (birth-death product formula), (iii) the asymptote sigma / (1 - e^-sigma).

0b (real testers).  A partner slot of N natives (fitness 1) receives testers: at each birth event in the partner slot,
with probability m / N the newborn is an arriving tester instead of a copy of its parent (m arrivals per generation).
A tester's fitness is r_q (relative to natives) when it meets a resident and r_q + delta when it meets a variant; its
expected fitness is r_q + delta * i / N.  The focal slot's variants have fitness 1 + w * Delta * j / N (j testers in
the partner slot).  Events alternate at random between the two slots (one generation = N events per slot).  The partner
slot is burned in for BURN generations with no variant, then one variant is placed; a replicate ends when the variant
fixes, is lost, or the testers reach half of the partner slot (tester establishes).  N rho counts only fixation.
T (mean copy-generations of one arrival's lineage until extinction or N/2) is computed exactly for a single arrival
in the all-resident environment (birth-death sojourn, constant fitness r_q), and checked by Little's law in a long
resident-only run of the partner slot with immigration.

    python3 src/tbr_stage0.py a [--reps 100000]
    python3 src/tbr_stage0.py b [--reps 20000]
"""
import argparse, json, math, os, sys, time
import numpy as np
from numba import njit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'tbr_rows')
W = 0.3
SIGMAS = (-3.0, -2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0, 3.0)
NS = (100, 400)
BURN = 20


def asym(s):
    return 1.0 if abs(s) < 1e-12 else s / (1.0 - math.exp(-s))


def p10_rho(N, r):
    if abs(r - 1.0) < 1e-15:
        return 1.0 / N
    return (1.0 - 1.0 / r) / (1.0 - r ** (-N))


def bd_fix(pu, pd):
    """fixation from 1 copy of a birth-death chain on 0..N with up/down probabilities pu[i], pd[i] (i = 1..N-1)."""
    N = len(pu)
    # sum_{k=0}^{N-1} prod_{i=1}^{k} gamma_i, gamma_i = pd_i / pu_i
    s = 1.0; prod = 1.0
    for k in range(1, N):
        if k >= len(pu) or pu[k] <= 0:
            break
        prod *= pd[k] / pu[k]
        s += prod
    return 1.0 / s


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


# ------------------------------------------------------------------ 0a
def updown_a(N, eps, delta):
    """per-event up/down probabilities at i variants, summed exactly over Binomial(i, eps) testers met."""
    from scipy.stats import binom
    pu = np.zeros(N + 1); pd = np.zeros(N + 1)
    for i in range(1, N):
        b = np.arange(i + 1); pb = binom.pmf(b, i, eps)
        wv = i + W * delta * b
        tot = wv + (N - i)
        pu[i] = float((pb * wv / tot).sum()) * (N - i) / N
        pd[i] = float((pb * (N - i) / tot).sum()) * i / N
    return pu, pd


@njit(cache=True)
def _sim_jump(pu, pd, N, reps, seed):
    np.random.seed(seed)
    fix = 0
    for r in range(reps):
        i = 1
        while 0 < i < N:
            if np.random.random() * (pu[i] + pd[i]) < pu[i]:
                i += 1
            else:
                i -= 1
        if i == N:
            fix += 1
    return fix


def stage_a(reps):
    rows = []
    for N in NS:
        for s in SIGMAS:
            delta = 1.0 if s >= 0 else -1.0
            eps = abs(s) / (W * N)                       # sigma = w * (eps N) * Delta, f = 1
            t0 = time.time()
            pu, pd = updown_a(N, eps, delta)
            seed = 7000 + N + int(round(10 * (s + 5)))
            k = int(_sim_jump(pu, pd, N, reps, seed))
            lo, hi = wilson(k, reps)
            r = 1.0 + W * eps * delta
            rho_p10 = p10_rho(N, r)
            rho_ex = bd_fix(pu[:N], pd[:N])
            rows.append(dict(stage='0a', N=N, sigma=s, eps=eps, delta=delta, reps=reps, fix=k, Nrho=N * k / reps,
                             Nrho_lo=N * lo, Nrho_hi=N * hi, Nrho_p10=N * rho_p10, Nrho_exact_process=N * rho_ex,
                             Nrho_asym=asym(s), p10_in_ci=bool(lo <= rho_p10 <= hi), exact_in_ci=bool(lo <= rho_ex <= hi),
                             rel_err_asym=(N * k / reps) / asym(s) - 1.0, wall=round(time.time() - t0, 2)))
            print(json.dumps(rows[-1]), flush=True)
    return rows


# ------------------------------------------------------------------ 0b
def sojourn_T(N, r):
    """exact mean copy-generations of one arrival (constant relative fitness r against natives) until extinction or
    reaching ceil(N/2) copies, and the establishment probability.  Moran in one slot: N events per generation."""
    M = (N + 1) // 2 if N % 2 else N // 2          # absorbing at M = N/2 copies
    # states 1..M-1 transient
    n = M - 1
    up = np.zeros(n); dn = np.zeros(n)
    for t in range(n):
        j = t + 1
        tot = r * j + (N - j)
        up[t] = r * j / tot * (N - j) / N
        dn[t] = (N - j) / tot * j / N
    # expected number of events at each state from start 1: solve (I - P) x = e_1 restricted (Green's function row)
    A = np.zeros((n, n))
    for t in range(n):
        A[t, t] = up[t] + dn[t]            # leaving probability (self-loops cancel)
        if t + 1 < n:
            A[t, t + 1] = -up[t]
        if t - 1 >= 0:
            A[t, t - 1] = -dn[t]
    # visits v solve v^T (D - P_off) = e_1^T in "leave-count" form: expected number of events spent at state = G[0, t]
    G = np.linalg.solve(A.T, np.eye(n)[0])     # v_t = expected events at state t from start 1
    copygen = float(sum(G[t] * (t + 1) for t in range(n)) / N)
    # establishment probability (hit M before 0)
    g = dn / up
    pr = np.concatenate([[1.0], np.cumprod(g)])
    pest = float(1.0 / pr.sum())
    return copygen, pest


@njit(cache=True)
def _sim_b(N, w, Delta, m, rq, dq, reps, burn, seed, maxev):
    np.random.seed(seed)
    out = np.zeros(4, np.int64)          # fixed, lost, tester established, truncated
    pm = m / N
    half = N // 2
    for r in range(reps):
        j = 0
        # burn-in of the partner slot with an all-resident focal slot (i = 0)
        nb = burn * N
        for e in range(nb):
            # partner event: parent by fitness (natives 1, testers rq), victim uniform; immigration
            if np.random.random() < pm:
                child = 1
            else:
                wq = rq * j; tot = wq + (N - j)
                child = 1 if np.random.random() * tot < wq else 0
            vic = 1 if np.random.random() * N < j else 0
            j += child - vic
            if j >= half:
                j = 0                    # an established tester before the variant arrives: restart the burn-in tail
        i = 1
        ev = 0
        res = 3
        while True:
            ev += 1
            if ev > maxev:
                res = 3; break
            if np.random.random() < 0.5:
                # focal event
                fv = 1.0 + w * Delta * j / N
                wv = fv * i; tot = wv + (N - i)
                child = 1 if np.random.random() * tot < wv else 0
                vic = 1 if np.random.random() * N < i else 0
                i += child - vic
                if i == 0:
                    res = 1; break
                if i == N:
                    res = 0; break
            else:
                if np.random.random() < pm:
                    child = 1
                else:
                    fq = rq + dq * i / N
                    wq = fq * j; tot = wq + (N - j)
                    child = 1 if np.random.random() * tot < wq else 0
                vic = 1 if np.random.random() * N < j else 0
                j += child - vic
                if j >= half:
                    res = 2; break
        out[res] += 1
    return out


@njit(cache=True)
def _little(N, m, rq, gens, seed):
    """resident-only partner slot with immigration: total tester copy-generations and arrivals (Little's law), and
    establishment events (the count is reset to 0 after one)."""
    np.random.seed(seed)
    pm = m / N; half = N // 2
    j = 0; area = 0.0; arr = 0; est = 0
    for e in range(gens * N):
        if np.random.random() < pm:
            child = 1; arr += 1
        else:
            wq = rq * j; tot = wq + (N - j)
            child = 1 if np.random.random() * tot < wq else 0
        vic = 1 if np.random.random() * N < j else 0
        j += child - vic
        area += j
        if j >= half:
            est += 1; j = 0
    return area / N, arr, est


CASES = [('rq0.7', 0.7, 0.0), ('rq0.9', 0.9, 0.0), ('neutral', 1.0, 0.0),
         ('rq0.9_better', 0.9, 0.1), ('rq0.9_worse', 0.9, -0.1)]
PRIMARY = ('rq0.7', 'rq0.9', 'neutral')


def stage_b(reps):
    rows = []
    for N in NS:
        for cname, rq, dq in CASES:
            T, pest = sojourn_T(N, rq)
            for s in SIGMAS:
                delta = 0.0 if s == 0 else (1.0 if s > 0 else -1.0)
                m = (abs(s) if s != 0 else 1.0) / (W * T)          # sigma = w m T Delta (f = 1)
                t0 = time.time()
                seed = 91000 + N * 7 + int(round(10 * (s + 5))) * 13 + CASES.index((cname, rq, dq)) * 1000
                o = _sim_b(N, W, delta, m, rq, dq, reps, BURN, seed, 200 * N * N)
                area, arr, est = _little(N, m, rq, 4000 if N == 100 else 2000, seed + 1)
                T_little = area / max(arr, 1)
                k = int(o[0]); n = int(o.sum())
                lo, hi = wilson(k, n)
                sig_little = W * m * T_little * delta
                rows.append(dict(stage='0b', case=cname, rq=rq, dq=dq, N=N, sigma=s, m=m, delta=delta, T=T, p_est=pest,
                                 T_little=T_little, est_little=int(est), arr_little=int(arr), sigma_little=sig_little,
                                 reps=n, fixed=k, lost=int(o[1]), tester_est=int(o[2]), truncated=int(o[3]),
                                 Nrho=N * k / n, Nrho_lo=N * lo, Nrho_hi=N * hi, Nrho_asym=asym(s),
                                 Nrho_p10=N * p10_rho(N, 1.0 + s / N), rel_err=(N * k / n) / asym(s) - 1.0,
                                 wall=round(time.time() - t0, 2)))
                print(json.dumps(rows[-1]), flush=True)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['a', 'b'])
    ap.add_argument('--reps', type=int, default=None)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    if a.what == 'a':
        rows = stage_a(a.reps or 100000)
    else:
        rows = stage_b(a.reps or 20000)
    with open(os.path.join(OUT, 'stage0%s.jsonl' % a.what), 'w') as f:
        for r in rows:
            f.write(json.dumps(r) + '\n')


if __name__ == '__main__':
    main()
