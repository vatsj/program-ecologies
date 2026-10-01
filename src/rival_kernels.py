"""Kernels for the rival-networks experiment (predictions/2026-10-01-rival-networks.md).

All on a general regular graph given as a neighbour array nb (N x deg), death-birth
updating: a uniformly random site dies; its neighbours compete to fill it with weight
exp(w * mean payoff over their own neighbours).  This is the update of
src/graph_rates.py and src/lattice.py.  A generation is N deaths.

  _invade_fix   per-mutant hitting probability of N/2 (ε-free), and for the lineages that
                reach N/2, whether they then fix, are lost, or are undecided by a cap.
  _domain       domain competition without mutation from a given two-type configuration:
                first passage of type A's count to 3N/4 or N/4, then to fixation;
                A's count and the number of A-B edges at checkpoints.
  _abm          finite-ε death-birth with mutation drawn from μ over all K classes;
                per-record statistics over edges and sites (approach rates only).
"""
import numpy as np
from abm import njit


@njit(cache=True)
def _payoff(U, grid, nb, v):
    deg = nb.shape[1]; s = 0.0; cv = grid[v]
    for b in range(deg):
        s += U[cv, grid[nb[v, b]]]
    return s / deg


@njit(cache=True)
def _db_event(U, grid, nb, w, wts):
    """One death-birth event; returns (site, old, new)."""
    N, deg = nb.shape
    s = np.random.randint(N)
    m = -1e300
    for a in range(deg):
        wts[a] = _payoff(U, grid, nb, nb[s, a])
        if wts[a] > m: m = wts[a]
    tot = 0.0
    for a in range(deg):
        wts[a] = np.exp(w * (wts[a] - m)); tot += wts[a]
    u = np.random.random() * tot; acc = 0.0; win = deg - 1
    for a in range(deg):
        acc += wts[a]
        if u <= acc:
            win = a; break
    old = grid[s]; new = grid[nb[s, win]]
    grid[s] = new
    return s, old, new


@njit(cache=True)
def _invade_fix(U, nb, w, trials, cap_gens, cont_gens, cont_max, seed):
    """U is the 2x2 block, index 0 = resident, 1 = mutant.  Returns
    (half, lost, undecided, fixed_after, lost_after, undecided_after); the
    continuation to fixation is run for at most cont_max of the half-successes."""
    np.random.seed(seed)
    N, deg = nb.shape
    wts = np.empty(deg)
    half = 0; lost = 0; und = 0; fx = 0; la = 0; ua = 0
    grid = np.zeros(N, np.int64)
    for tr in range(trials):
        grid[:] = 0
        grid[np.random.randint(N)] = 1
        cnt = 1; ev = 0; out = -1
        while ev < cap_gens * N:
            s, old, new = _db_event(U, grid, nb, w, wts)
            cnt += new - old
            ev += 1
            if cnt == 0:
                out = 0; break
            if 2 * cnt >= N:
                out = 1; break
        if out == 0:
            lost += 1
        elif out == -1:
            und += 1
        else:
            half += 1
            if cont_gens > 0 and fx + la + ua < cont_max:
                ev = 0; o2 = -1
                while ev < cont_gens * N:
                    s, old, new = _db_event(U, grid, nb, w, wts)
                    cnt += new - old
                    ev += 1
                    if cnt == N:
                        o2 = 1; break
                    if cnt == 0:
                        o2 = 0; break
                if o2 == 1: fx += 1
                elif o2 == 0: la += 1
                else: ua += 1
    return half, lost, und, fx, la, ua


@njit(cache=True)
def _cross_edges(grid, nb, a, b):
    N, deg = nb.shape; e = 0
    for v in range(N):
        if grid[v] == a:
            for k in range(deg):
                if grid[nb[v, k]] == b: e += 1
    return e


@njit(cache=True)
def _domain(U, nb, w, init, cap_gens, cont_gens, every, nrec, seed, lo, hi):
    """U 2x2, type 1 = A.  From init (0/1 array), run until A's count reaches hi (+1)
    or lo (-1), else 0 at cap (lo = N/4, hi = 3N/4 for the half split); then continue to fixation of either type (cont_gens cap).
    Returns (first, t_first, fix, t_fix, rec_cnt[nrec], rec_cross[nrec]); rec_* sampled
    every `every` generations from t = 0 (rec_cross = A-B edges), -1 after the run ends."""
    np.random.seed(seed)
    N, deg = nb.shape
    wts = np.empty(deg)
    grid = init.copy()
    cnt = 0
    for v in range(N): cnt += grid[v]
    rec_cnt = -np.ones(nrec); rec_cross = -np.ones(nrec)
    first = 0; t_first = -1.0; fix = 0; t_fix = -1.0
    total = (cap_gens + cont_gens) * N
    r = 0
    for ev in range(total + 1):
        if ev % (every * N) == 0 and r < nrec:
            rec_cnt[r] = cnt; rec_cross[r] = _cross_edges(grid, nb, 1, 0); r += 1
        if first == 0 and ev >= cap_gens * N:
            break
        s, old, new = _db_event(U, grid, nb, w, wts)
        cnt += new - old
        if first == 0:
            if cnt >= hi:
                first = 1; t_first = (ev + 1) / N
            elif cnt <= lo:
                first = -1; t_first = (ev + 1) / N
        if cnt == N:
            fix = 1; t_fix = (ev + 1) / N; break
        if cnt == 0:
            fix = -1; t_fix = (ev + 1) / N; break
        if first != 0 and ev - t_first * N >= cont_gens * N:
            break
    return first, t_first, fix, t_fix, rec_cnt, rec_cross


@njit(cache=True)
def _abm(U, ACT, lab, nlab, mu_cdf, nb, w, eps, gens, every, init, seed, iFB, iPS, iC):
    """Finite-eps death-birth with mutation.  ACT[x, y] = 1 iff x plays C against y.
    lab[k] in 0..nlab-1 is the network label of class k.  Every `every` generations
    records (fractions are over directed neighbour pairs = edges counted twice):
      0 generation, 1 P(C,C), 2 mutual-defection (MD) edge fraction,
      3 MD edges between FB-net (lab 1) and P*-net (lab 2) sites,
      4 MD edges with at least one D-type (lab 0) end, 5 other MD edges,
      6 mean payoff deficit per edge, R - mean u (R = 0; includes compute costs),
      7 compute-cost part of that deficit,
      8 FB class share, 9 P* class share, 10 ALLC share, 11.. 11+nlab label shares,
      11+nlab / 12+nlab / 13+nlab: the front, sites not in P*-net with at least one P*-net
      neighbour: its ALLC count, FB-net count and total, each / N.
    Labels: 0 D-type, 1 FB-net, 2 P*-net, 3 exploitable (ALLC kin), 4 other-coop."""
    np.random.seed(seed)
    N, deg = nb.shape
    K = U.shape[0]
    grid = init.copy()
    wts = np.empty(deg)
    nr = gens // every
    rec = np.zeros((nr, 14 + nlab))
    base = np.array([[-1.0, 1.0], [-2.0, 0.0]])   # PD payoff, (D, C) order
    r = 0
    for g in range(1, gens + 1):
        for e in range(N):
            s = np.random.randint(N)
            m = -1e300
            for a in range(deg):
                wts[a] = _payoff(U, grid, nb, nb[s, a])
                if wts[a] > m: m = wts[a]
            tot = 0.0
            for a in range(deg):
                wts[a] = np.exp(w * (wts[a] - m)); tot += wts[a]
            u = np.random.random() * tot; acc = 0.0; win = deg - 1
            for a in range(deg):
                acc += wts[a]
                if u <= acc:
                    win = a; break
            if np.random.random() < eps:
                u = np.random.random(); child = K - 1
                for i in range(K):
                    if u <= mu_cdf[i]:
                        child = i; break
            else:
                child = grid[nb[s, win]]
            grid[s] = child
        if g % every == 0 and r < nr:
            cc = 0.0; md = 0.0; mdb = 0.0; mdd = 0.0; pay = 0.0; cost = 0.0
            ne = float(N * deg)
            for v in range(N):
                x = grid[v]
                for k in range(deg):
                    y = grid[nb[v, k]]
                    ax = ACT[x, y]; ay = ACT[y, x]
                    if ax == 1 and ay == 1:
                        cc += 1.0
                    if ax == 0 and ay == 0:
                        md += 1.0
                        lx = lab[x]; ly = lab[y]
                        if (lx == 1 and ly == 2) or (lx == 2 and ly == 1):
                            mdb += 1.0
                        elif lx == 0 or ly == 0:
                            mdd += 1.0
                    pay += U[x, y]
                    cost += base[ax, ay] - U[x, y]
            rec[r, 0] = g; rec[r, 1] = cc / ne; rec[r, 2] = md / ne; rec[r, 3] = mdb / ne
            rec[r, 4] = mdd / ne; rec[r, 5] = (md - mdb - mdd) / ne
            rec[r, 6] = -pay / ne; rec[r, 7] = cost / ne
            nfb = 0.0; nps = 0.0; nc = 0.0
            for v in range(N):
                x = grid[v]
                if x == iFB: nfb += 1.0
                if x == iPS: nps += 1.0
                if x == iC: nc += 1.0
                rec[r, 11 + lab[x]] += 1.0 / N
                if lab[x] != 2:
                    fr = False
                    for k in range(deg):
                        if lab[grid[nb[v, k]]] == 2:
                            fr = True; break
                    if fr:
                        rec[r, 13 + nlab] += 1.0 / N
                        if x == iC: rec[r, 11 + nlab] += 1.0 / N
                        if lab[x] == 1: rec[r, 12 + nlab] += 1.0 / N
            rec[r, 8] = nfb / N; rec[r, 9] = nps / N; rec[r, 10] = nc / N
            r += 1
    return rec, grid


@njit(cache=True)
def _front(U, nb, w, init, gens, every, track, seed):
    """No mutation, K types (U is K x K).  Runs `gens` generations from init and records the
    count of type `track` every `every` generations (column 0), the number of sites of
    each type (columns 1..K), and the front: for sites not of type `track` with at least one
    `track` neighbour, the count of each type (columns K+1..2K)."""
    np.random.seed(seed)
    N, deg = nb.shape
    K = U.shape[0]
    wts = np.empty(deg)
    grid = init.copy()
    nr = gens // every + 1
    rec = np.zeros((nr, 2 * K + 1))
    r = 0
    for g in range(0, gens + 1):
        if g > 0:
            for e in range(N):
                _db_event(U, grid, nb, w, wts)
        if g % every == 0 and r < nr:
            for v in range(N):
                rec[r, 1 + grid[v]] += 1
                if grid[v] != track:
                    for k in range(deg):
                        if grid[nb[v, k]] == track:
                            rec[r, 1 + K + grid[v]] += 1
                            break
            rec[r, 0] = rec[r, 1 + track]
            r += 1
    return rec
