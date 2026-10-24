"""The PD under the pricing rules: the play-step model and the priced payoff (notes/pricing-rules.md §2).

The stored carrier-lottery kernel (src/provenance.py, annealed_kern.py) has no play-step table: its payoffs are outcomes
(A, selfa) of units' decision trees over checks whose values (CHC, CHD, UVt) are tabulated.  This module evaluates the same
decision trees (at most two atoms, depth <= 2 for all 4,162 run trees) on the same tables and charges each atom evaluation
the cost of its check call, by outcome:

    twelve classes (CLASS_NAMES): the checked unit has no list (nolist); a check of distinct quotes true / false (dist_T,
    dist_F); of a unit against its own quote (same_T / same_F); a unit against itself (self_T / self_F, atoms (them,them) and
    (me,me)); against the constant quotes ^C / ^D (vsC_*, vsD_*); a check that reaches its cap (TO, V + 6 = 250,006); plus
    the root's own steps (base).  The first model used medians of the stored records; `pricing_rules_pd_validate.py` fits the
    class costs by non-negative least squares on executed plays and reports the held-out error

and a production act (S-nonself, the only rule in the cell) the stored medians COSTS[3] (produce C), COSTS[4] (produce D),
COSTS[5] (cap).  The rules' per-play charges (steps S, time-out calls n, the steps of those calls, calls m):

    rule 0 zero; 1 F: c (S + SP); 2 A: P (n + n'); 3 F+A: c ((S - s_to + K n) + (SP - sp_to + K n')); 4 B steady state: c * root
    steps (reads and production acts amortized to zero at the type level); 5 toll: tau (m + acts)

with K = 10**6 (the encounter budget).  All of this is a pair-level function of the two types, so it enters the Moran
fitness (a type's mean payoff against its island) through `pay_net`.  Zero price returns the stored payoff exactly.
"""
import os
import sys

import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import provenance as PV
import lt_genes_pop as GP

R_SNON = PV.R_SNON
KPD = 1.0e6
# cost classes (see CLASS_NAMES): the median-based first model; replaced by the executable calibration when present
CST_DEFAULT = np.array([101.0, 15815.0, 15815.0, 9513.0, 9513.0, 9513.0, 9513.0, 2415.0, 2415.0, 245.0, 245.0, 250006.0, 4.0])
RULE_CODE = {'Z': 0, 'F': 1, 'A': 2, 'FA': 3, 'B': 4, 'T': 5}


def build_dt(cat):
    """Decision-tree arrays of the run trees: DTy[t] (0 leaf C, 1 leaf D, 2 tree), DR[t] the root atom (kind, a, q),
    BTy[t, b] the branch (0 C, 1 D, 2 sub-atom) for b = 0 (atom true) / 1 (false), BA[t, b] the sub-atom, BL[t, b] the sub-atom's
    leaves (true, false) as 1 = C, 0 = D."""
    T = cat.T
    DTy = np.zeros(T, np.int64); DR = np.zeros((T, 3), np.int64)
    BTy = np.zeros((T, 2), np.int64); BA = np.zeros((T, 2, 3), np.int64); BL = np.zeros((T, 2, 2), np.int64)
    for t, dt in enumerate(cat.tau_dt):
        if isinstance(dt, str):
            DTy[t] = 0 if dt == 'C' else 1
            continue
        DTy[t] = 2
        DR[t] = GP.atom_box_kind(dt[0])
        for b in range(2):
            node = dt[1 + b]
            if isinstance(node, str):
                BTy[t, b] = 0 if node == 'C' else 1
            else:
                BTy[t, b] = 2
                BA[t, b] = GP.atom_box_kind(node[0])
                for q in range(2):
                    leaf = node[1 + q]
                    assert isinstance(leaf, str), 'tree deeper than 2'
                    BL[t, b, q] = 1 if leaf == 'C' else 0
    return DTy, DR, BTy, BA, BL


NCLS = 12
(C_N0, C_D_T, C_D_F, C_S_T, C_S_F, C_Q_T, C_Q_F, C_VC_T, C_VC_F, C_VD_T, C_VD_F, C_TO) = range(12)
C_BASE = 12
CLASS_NAMES = ['nolist', 'dist_T', 'dist_F', 'same_T', 'same_F', 'self_T', 'self_F', 'vsC_T', 'vsC_F', 'vsD_T', 'vsD_F', 'TO', 'base']


@njit(cache=True)
def _has(ai, x, BLC, BLD):
    return BLC[x, 0] >= 0 if ai == 0 else BLD[x, 0] >= 0


@njit(cache=True)
def atom_eval(kind, ai, qi, u, v, same, BLC, BLD, CHC, CHD, UVt):
    """(value 0/1, cost class, timed out 0/1) of one atom of u's tree against v (u, v units; same = same quote)."""
    if kind == 0 or kind == 1:
        if same:
            if not _has(ai, u, BLC, BLD): return 0, C_N0, 0
            x = UVt[u, ai]
            if x == 2: return 0, C_TO, 1
            return (1, C_S_T, 0) if x == 1 else (0, C_S_F, 0)
        if kind == 0:
            chk = v; tgt = u
        else:
            chk = u; tgt = v
        if not _has(ai, chk, BLC, BLD): return 0, C_N0, 0
        x = CHC[chk, tgt] if ai == 0 else CHD[chk, tgt]
        if x == 2: return 0, C_TO, 1
        return (1, C_D_T, 0) if x == 1 else (0, C_D_F, 0)
    sub = v if (kind == 2 or kind == 4) else u
    if kind == 2 or kind == 3:
        idx = ai
    else:
        idx = 2 + 2 * qi + ai
    x = UVt[sub, idx]
    if not _has(ai, sub, BLC, BLD): return (1 if x == 1 else 0), C_N0, 0
    if x == 2: return 0, C_TO, 1
    if kind == 2 or kind == 3:
        return (1, C_Q_T, 0) if x == 1 else (0, C_Q_F, 0)
    if qi == 0:
        return (1, C_VC_T, 0) if x == 1 else (0, C_VC_F, 0)
    return (1, C_VD_T, 0) if x == 1 else (0, C_VD_F, 0)


@njit(cache=True)
def play_classes(u, v, same, utau, DTy, DR, BTy, BA, BL, BLC, BLD, CHC, CHD, UVt):
    """(action 1 = C, first atom class or -1, second atom class or -1, first timed out, second timed out)."""
    t = utau[u]
    if DTy[t] == 0: return 1, -1, -1, 0, 0
    if DTy[t] == 1: return 0, -1, -1, 0, 0
    val, c1, to1 = atom_eval(DR[t, 0], DR[t, 1], DR[t, 2], u, v, same, BLC, BLD, CHC, CHD, UVt)
    b = 0 if val == 1 else 1
    ty = BTy[t, b]
    if ty == 2:
        val2, c2, to2 = atom_eval(BA[t, b, 0], BA[t, b, 1], BA[t, b, 2], u, v, same, BLC, BLD, CHC, CHD, UVt)
        act = BL[t, b, 0] if val2 == 1 else BL[t, b, 1]
        return act, c1, c2, to1, to2
    return (1 if ty == 0 else 0), c1, -1, to1, 0


@njit(cache=True)
def play_ledger(u, v, same, utau, DTy, DR, BTy, BA, BL, BLC, BLD, CHC, CHD, UVt, CST):
    """(action 1 = C, steps, timed-out calls, steps of those calls, calls) of u's play against v."""
    act, c1, c2, to1, to2 = play_classes(u, v, same, utau, DTy, DR, BTy, BA, BL, BLC, BLD, CHC, CHD, UVt)
    S = CST[C_BASE]; nto = 0; tos = 0.0; ncall = 0
    if c1 >= 0:
        S += CST[c1]; ncall += 1
        if to1 == 1: nto += 1; tos += CST[c1]
    if c2 >= 0:
        S += CST[c2]; ncall += 1
        if to2 == 1: nto += 1; tos += CST[c2]
    return act, S, nto, tos, ncall


@njit(cache=True)
def prod_ledger(k, j, tunit, tsp, trule, utau, BLC, BLD, PRODC, PD, KIND, NAT, CHD, UVt, COSTS):
    """(steps, timed-out acts, steps of those acts, acts) of the S-nonself production of type k in an encounter with j."""
    if trule[k] != R_SNON: return 0.0, 0, 0.0, 0
    u = tunit[k]; v = tunit[j]
    SP = 0.0; nto = 0; tos = 0.0; nacts = 0
    if BLC[u, 0] < 0 and tsp[j] != tsp[k]:
        rel = PV.relation(k, j, tunit, tsp)
        t = utau[u]
        code = PV.c_code(u, v, rel, utau, KIND, NAT, CHD, UVt, BLC, BLD)
        sid = PRODC[t, code]
        nacts += 1
        if sid == -3:
            SP += COSTS[5]; nto += 1; tos += COSTS[5]
        else:
            SP += COSTS[3]
    if BLD[u, 0] < 0:
        nacts += 1
        if PD[u] == -3:
            SP += COSTS[5]; nto += 1; tos += COSTS[5]
        else:
            SP += COSTS[4]
    return SP, nto, tos, nacts


@njit(cache=True)
def charge_pair(k, j, tunit, tsp, trule, PX):
    """The rule's charge of type k in an encounter with type j (payoff units)."""
    utau, BLC, BLD, CHC, CHD, UVt, PRODC, PD, KIND, NAT, DTy, DR, BTy, BA, BL, CST, COSTS, PAR = PX
    rule = int(PAR[0])
    if rule == 0: return 0.0
    lev = PAR[1]; Kp = PAR[2]
    u = tunit[k]; v = tunit[j]
    same = (u == v) and (tsp[k] == tsp[j])
    act, S, nto, tos, ncall = play_ledger(u, v, same, utau, DTy, DR, BTy, BA, BL, BLC, BLD, CHC, CHD, UVt, CST)
    SP, nto2, tos2, nacts = prod_ledger(k, j, tunit, tsp, trule, utau, BLC, BLD, PRODC, PD, KIND, NAT, CHD, UVt, COSTS)
    if rule == 1: return lev * (S + SP)
    if rule == 2: return lev * (nto + nto2)
    if rule == 3: return lev * ((S - tos + Kp * nto) + (SP - tos2 + Kp * nto2))
    if rule == 4: return lev * CST[C_BASE]
    return lev * (ncall + nacts)


@njit(cache=True)
def pay_net(k, j, tunit, tsp, trule, A, selfa, PX):
    base = PV.pay(k, j, tunit, tsp, A, selfa)
    if PX[17][0] == 0.0: return base
    return base - charge_pair(k, j, tunit, tsp, trule, PX)


def load_cst(path=None):
    """The fitted class costs (runs/pricing_rules/pd_cost_calibration.json) if the calibration has been run, else the
    median-based defaults."""
    import json
    path = path or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'runs', 'pricing_rules',
                                'pd_cost_calibration.json')
    if os.path.exists(path):
        return np.array(json.load(open(path))['beta'], float)
    return CST_DEFAULT.copy()


def make_px(LS, rule, level, cst=None):
    """The tuple of tables `pay_net` reads (arrays only), for rule in RULE_CODE at a level."""
    st = LS['st']
    DTy, DR, BTy, BA, BL = LS.setdefault('_dt', build_dt(LS['cat']))
    cst = load_cst() if cst is None else np.asarray(cst, float)
    par = np.array([RULE_CODE[rule], float(level), KPD])
    return (np.asarray(st['utau']), np.asarray(st['BLC']), np.asarray(st['BLD']), st['CHC'], st['CHD'], np.asarray(st['UVt']),
            np.asarray(LS['PRODC']), np.asarray(LS['PD']), np.asarray(st['KIND']), np.asarray(st['NAT']),
            DTy, DR, BTy, BA, BL, cst, np.asarray(LS['COSTS'], float), par)
