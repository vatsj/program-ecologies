"""Per-mutant invasion rates on a general graph (the eps->0 object of a
structured population).  Death-birth Moran: a random site dies; its neighbours
compete to fill it with probability proportional to exp(w * mean payoff over
their own neighbours).  rho(mut | res): one mutant in an all-res population,
run until the mutant holds half the graph (success) or is extinct (failure);
trials undecided after cap_gens generations are reported separately.

Graphs: torus (degree 4), hypercube of dimension d (degree d, N = 2^d).
Well-mixed reference: Moran fixation to N/2 (chain.fixation with kstar = N/2).

    python3 src/graph_rates.py
"""
import json, os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from abm import njit
from chain import fixation

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def torus(side):
    N = side * side
    nb = np.empty((N, 4), np.int64)
    for s in range(N):
        x, y = s % side, s // side
        nb[s] = [y * side + (x + 1) % side, y * side + (x - 1) % side, ((y + 1) % side) * side + x, ((y - 1) % side) * side + x]
    return nb


def hypercube(d):
    N = 1 << d
    return np.array([[s ^ (1 << b) for b in range(d)] for s in range(N)], np.int64)


@njit(cache=True)
def _invade(U, nb, w, iRes, iMut, trials, cap_gens, seed):
    np.random.seed(seed)
    N, deg = nb.shape
    wts = np.empty(deg)
    succ = 0; fail = 0; undec = 0
    for tr in range(trials):
        grid = np.full(N, iRes, np.int64)
        grid[np.random.randint(N)] = iMut
        cnt = 1; ev = 0; out = -1
        while ev < cap_gens * N:
            s = np.random.randint(N)
            m = -1e300
            for a in range(deg):
                v = nb[s, a]; pay = 0.0
                for b in range(deg):
                    pay += U[grid[v], grid[nb[v, b]]]
                wts[a] = pay / deg
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
            if old == iMut: cnt -= 1
            if new == iMut: cnt += 1
            ev += 1
            if cnt == 0:
                out = 0; break
            if 2 * cnt >= N:
                out = 1; break
        if out == 1: succ += 1
        elif out == 0: fail += 1
        else: undec += 1
    return succ, fail, undec


def well_mixed(U, iRes, iMut, N, w):
    return fixation(U[iMut, iMut], U[iMut, iRes], U[iRes, iMut], U[iRes, iRes], N, w, N // 2)
