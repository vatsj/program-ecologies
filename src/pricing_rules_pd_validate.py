"""Calibration and validation of the PD play-step model against executable plays (notes/pricing-rules.md §2).

The stored tables give a play's atom outcomes but no steps.  Here random ordered pairs of distinct units are drawn from the
types a zero-price lottery actually creates (a few runs advanced 300 generations), the model classifies each atom evaluation
(pricing_rules_pd_model.play_classes) and the actual run of the program against the other's quote is executed in the
executable L_T^code evaluator (lt_genes.play_side, K = 10**6).  A non-negative least-squares fit of the executed steps on the
class counts gives the cost of each class (the TO class is fixed at V + 6); a held-out sample reports the error of the fitted
model.  Writes runs/pricing_rules/pd_cost_calibration.json, which the model loads.

    python3 src/pricing_rules_pd_validate.py [n_fit] [n_hold]
"""
import json
import os
import sys
import time

import numpy as np
from scipy.optimize import nnls

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault('NUMBA_NUM_THREADS', '1')
import world_k as WK
import lt_genes as G
import lt_code as L
import lt_genes_pop as GP
import pricing_rules_pd_model as M
import pricing_rules_pd as PD

K = 10 ** 6
OUT = os.path.join(os.path.dirname(HERE), 'runs', 'pricing_rules')
CAL = os.path.join(OUT, 'pd_cost_calibration.json')


def build_universe(LS):
    meta = LS['meta']
    U = GP.Universe(K, K // 4)
    U.scripts = list(meta['scripts']); U.sid = {k: i for i, k in enumerate(U.scripts)}
    U.units = list(meta['units']); U.uid = {k: i for i, k in enumerate(U.units)}
    return U


def prog(U, u):
    t, cs, ds = U.units[u]
    return G.Prog('u', U.bodies[t], 'H', [U.scripts[i][1] for i in cs], [U.scripts[i][1] for i in ds])


def lottery_units(LS, reps=(0, 1, 2), gens=300):
    """Units that occur in zero-price lottery runs advanced `gens` generations (all types ever created)."""
    PD.CFG.update(rule='Z', level=0.0, cst=None)
    us = set()
    for rep in reps:
        R = PD.PricedRun('wk_Snon_100_64', rep, track=False)
        R.advance(gens)
        nt = int(R.ntv[0])
        us.update(np.unique(R.tunit[:nt]).tolist())
    return np.array(sorted(us))


def sample(n, units, seed, PX, p_same=0.15):
    """Ordered pairs of distinct units, and with probability p_same a unit against its own quote (same quote)."""
    utau, BLC, BLD, CHC, CHD, UVt, PRODC, PD_, KIND, NAT, DTy, DR, BTy, BA, BL, CST, COSTS, PAR = PX
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        u = int(units[rng.integers(len(units))])
        same = rng.random() < p_same
        v = u if same else int(units[rng.integers(len(units))])
        if u == v and not same: continue
        act, c1, c2, to1, to2 = M.play_classes(u, v, same, utau, DTy, DR, BTy, BA, BL, BLC, BLD, CHC, CHD, UVt)
        out.append((u, v, int(act), int(c1), int(c2), bool(same)))
    return out


def execute(U, pairs, tmax):
    t0 = time.time()
    rows = []
    for (u, v, act, c1, c2, same) in pairs:
        if time.time() - t0 > tmax: break
        if len(L.CACHE) > 200000: L.CACHE.clear()
        a, w, bot = G.play_side(prog(U, u), prog(U, v), K)
        rows.append(dict(u=u, v=v, same=same, act_model=act, c1=c1, c2=c2, exec=int(w), act_exec=a, bot=bool(bot)))
    return rows


def features(rows):
    X = np.zeros((len(rows), 13)); y = np.zeros(len(rows))
    for i, r in enumerate(rows):
        for c in (r['c1'], r['c2']):
            if c >= 0: X[i, c] += 1
        X[i, 12] = 1
        y[i] = r['exec']
    return X, y


def fit(rows):
    """NNLS on the class counts (columns of classes never seen keep the default); TO fixed at V + 6."""
    X, y = features(rows)
    X = X.copy(); to_col = X[:, M.C_TO].copy(); y = y - 250006.0 * to_col; X[:, M.C_TO] = 0
    # fixed: the root's own steps (4, the constants) and the nolist check (101, the stored gate0)
    y = y - 4.0 * X[:, M.C_BASE] - 101.0 * X[:, M.C_N0]
    X[:, M.C_BASE] = 0; X[:, M.C_N0] = 0
    seen = X.sum(0) > 0
    beta = M.CST_DEFAULT.copy()
    Xs = X[:, seen]
    b, _ = nnls(Xs, y)
    beta[seen] = b
    beta[M.C_TO] = 250006.0; beta[M.C_BASE] = 4.0; beta[M.C_N0] = 101.0
    return beta, seen


def summarize(rows, beta):
    X, y = features(rows)
    pred = X @ beta
    ok = (pred > 0) & (y > 0)
    lr = np.log10(y[ok] / pred[ok])
    return dict(n=len(rows), median_ratio=float(10 ** np.median(lr)), q10=float(10 ** np.quantile(lr, .1)), q90=float(10 ** np.quantile(lr, .9)),
                within_2x=float(np.mean(np.abs(lr) <= np.log10(2))), mean_pred=float(pred.mean()), mean_exec=float(y.mean()),
                action_agree=float(np.mean([(r['act_model'] == 1) == (r['act_exec'] == 'C') for r in rows])))


def run(n_fit=4000, n_hold=1500, seed=11, tmax=3600):
    sys.setrecursionlimit(1000000)
    LS = WK.use_world('K')
    U = build_universe(LS)
    units = lottery_units(LS)
    PX = M.make_px(LS, 'F', 1e-4, M.CST_DEFAULT)
    t0 = time.time()
    rows_fit = execute(U, sample(n_fit, units, seed, PX), tmax)
    rows_hold = execute(U, sample(n_hold, units, seed + 1, PX), tmax)
    beta, seen = fit(rows_fit)
    res = dict(units=int(len(units)), classes=M.CLASS_NAMES, beta=beta.tolist(), seen=seen.tolist(), default=M.CST_DEFAULT.tolist(),
               fit_default=summarize(rows_fit, M.CST_DEFAULT), fit_fitted=summarize(rows_fit, beta),
               hold_default=summarize(rows_hold, M.CST_DEFAULT), hold_fitted=summarize(rows_hold, beta),
               class_counts=np.bincount([c for r in rows_fit for c in (r['c1'], r['c2']) if c >= 0], minlength=12).tolist(),
               secs=time.time() - t0)
    os.makedirs(OUT, exist_ok=True)
    json.dump(res, open(CAL, 'w'), indent=1)
    print(json.dumps(res, indent=1))
    return res


if __name__ == '__main__':
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 4000, int(sys.argv[2]) if len(sys.argv) > 2 else 1500)
