"""Three players and coalition coins against the alpha- and beta-cores (static).
notes/2026-11-23-three-players-coins.md.  Game G3: slots 0, 1 play N/X/Y (0/1/2), slot 2 plays L/R (0/1)."""
import sys, os, json, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from abm import njit
from scipy.optimize import linprog


def pay(a0, a1, a2):
    if a0 == 0 and a1 == 0: return (1.0, 1.0, 1.0)
    if a0 == 1 and a1 == 1: return (2.0, 2.0, 0.0) if a2 == 0 else (2.0, 0.0, 0.0)
    if a0 == 2 and a1 == 2: return (0.0, 2.0, 0.0) if a2 == 0 else (2.0, 2.0, 0.0)
    return (0.0, 0.0, 0.0)


def part1(grid=201):
    """Pair {0,1} against player 2, baseline (1,1).  Correlated pair mixtures over the 9 joint actions."""
    J = list(itertools.product(range(3), range(3)))
    UL = np.array([pay(a, b, 0)[:2] for a, b in J]); UR = np.array([pay(a, b, 1)[:2] for a, b in J])
    # alpha: max_sigma min over (b in L,R; i in 0,1) of u_i - 1  (LP)
    c = np.zeros(10); c[-1] = -1
    A = []; 
    for U in (UL, UR):
        for i in (0, 1):
            A.append(np.append(-U[:, i], 1.0))
    r = linprog(c, A_ub=np.array(A), b_ub=np.zeros(4), A_eq=[np.append(np.ones(9), 0)], b_eq=[1], bounds=[(0, 1)] * 9 + [(None, None)])
    alpha_val = r.x[-1] - 1            # best guaranteed min gain of the pair with a shared coin
    # beta: for each p = P(L), max_sigma min_i u_i - 1
    worst = 1e9; worst_p = None
    for p in np.linspace(0, 1, grid):
        U = p * UL + (1 - p) * UR
        A = [np.append(-U[:, i], 1.0) for i in (0, 1)]
        r = linprog(c, A_ub=np.array(A), b_ub=np.zeros(2), A_eq=[np.append(np.ones(9), 0)], b_eq=[1], bounds=[(0, 1)] * 9 + [(None, None)])
        g = r.x[-1] - 1
        if g < worst: worst, worst_p = g, float(p)
    # pure
    pure_alpha = max(min(min(pay(a, b, t)[0], pay(a, b, t)[1]) for t in (0, 1)) for a, b in J) - 1
    pure_beta = min(max(min(pay(a, b, t)[0], pay(a, b, t)[1]) for a, b in J) for t in (0, 1)) - 1
    return {'pair_alpha_gain_shared_coin': float(alpha_val), 'pair_beta_gain_shared_coin_min_over_p': float(worst), 'at_p': worst_p,
            'pair_alpha_gain_pure': float(pure_alpha), 'pair_beta_gain_pure': float(pure_beta)}


def part2():
    out = {}
    acts = [range(3), range(3), range(2)]
    for i in range(3):
        oth = [j for j in range(3) if j != i]
        comp = list(itertools.product(acts[oth[0]], acts[oth[1]]))
        def u(ai, b):
            prof = [0, 0, 0]; prof[i] = ai; prof[oth[0]] = b[0]; prof[oth[1]] = b[1]
            return pay(*prof)[i]
        M = np.array([[u(ai, b) for b in comp] for ai in acts[i]])          # rows: i's actions
        k, m = M.shape
        # maxmin: max v s.t. sigma^T M >= v
        r1 = linprog(np.append(np.zeros(k), -1), A_ub=np.hstack([-M.T, np.ones((m, 1))]), b_ub=np.zeros(m),
                     A_eq=[np.append(np.ones(k), 0)], b_eq=[1], bounds=[(0, 1)] * k + [(None, None)])
        r2 = linprog(np.append(np.zeros(m), 1), A_ub=np.hstack([M, -np.ones((k, 1))]), b_ub=np.zeros(k),
                     A_eq=[np.append(np.ones(m), 0)], b_eq=[1], bounds=[(0, 1)] * m + [(None, None)])
        out['player%d' % (i + 1)] = {'maxmin': float(r1.x[-1]), 'minmax_correlated': float(r2.x[-1])}
    return out


def part3(grid=401):
    """Player 3 mixes 1/2-1/2.  Independent pair mixing (r, s over N/X/Y each) vs a shared coin."""
    U = np.array([[0.5 * np.array(pay(a, b, 0)[:2]) + 0.5 * np.array(pay(a, b, 1)[:2]) for b in range(3)] for a in range(3)])  # [a][b][i]
    best = -1e9
    g = np.linspace(0, 1, 81)
    for x1 in g:
        for y1 in g:
            if x1 + y1 > 1 + 1e-12: continue
            r = np.array([1 - x1 - y1, x1, y1])
            for x2 in g:
                for y2 in g:
                    if x2 + y2 > 1 + 1e-12: continue
                    s = np.array([1 - x2 - y2, x2, y2])
                    v = np.einsum('a,b,abi->i', r, s, U)
                    best = max(best, min(v) - 1)
    q = np.linspace(0, 1, grid)                      # shared coin: q on XX, 1-q on YY
    shared = max(min(q_ * U[1, 1, 0] + (1 - q_) * U[2, 2, 0], q_ * U[1, 1, 1] + (1 - q_) * U[2, 2, 1]) - 1 for q_ in q)
    return {'independent_best_min_gain': float(best), 'shared_coin_best_min_gain': float(shared)}


# ---------------------------------------------------------------- three-player sound-reading arm
NACT = (3, 3, 2)


def atoms_of(s):
    out = []
    for Lv in (0, 1):
        for j in range(3):
            if j == s: continue
            for x in range(NACT[j]): out.append((Lv, j, x))
    return out


def programs(s, max_atoms):
    """Rows [shape, A, B, l0, l1, l2]; atoms as indices into atoms_of(s)."""
    na = len(atoms_of(s)); k = NACT[s]; P = []
    for l in range(k): P.append((0, 0, 0, l, 0, 0))
    for a in range(na):
        for l0 in range(k):
            for l1 in range(k):
                if l0 != l1: P.append((1, a, 0, l0, l1, 0))
    if max_atoms >= 2:
        for a in range(na):
            for b in range(na):
                if a == b: continue
                for l0 in range(k):
                    for l1 in range(k):
                        if l0 == l1: continue
                        for l2 in range(k):
                            P.append((2, a, b, l0, l1, l2)); P.append((3, a, b, l2, l0, l1))
    return np.array(P, np.int64)


def atom_arrays():
    AL = np.zeros((3, 12), np.int64); AJ = np.zeros((3, 12), np.int64); AX = np.zeros((3, 12), np.int64)
    for s in range(3):
        for i, (Lv, j, x) in enumerate(atoms_of(s)): AL[s, i], AJ[s, i], AX[s, i] = Lv, j, x
    return AL, AJ, AX


@njit(cache=True)
def _act(p, s, AL, AJ, AX, ok0, ok1):
    sh = p[0]
    if sh == 0: return p[3]
    a = p[1]
    ta = ok0[AJ[s, a], AX[s, a]] if AL[s, a] == 0 else ok1[AJ[s, a], AX[s, a]]
    if sh == 1: return p[3] if ta else p[4]
    b = p[2]
    tb = ok0[AJ[s, b], AX[s, b]] if AL[s, b] == 0 else ok1[AJ[s, b], AX[s, b]]
    if sh == 2:
        if ta: return p[3] if tb else p[4]
        return p[5]
    if ta: return p[3]
    return p[4] if tb else p[5]


@njit(cache=True)
def play(p0, p1, p2, AL, AJ, AX):
    ok0 = np.ones((3, 3), np.bool_); ok1 = np.ones((3, 3), np.bool_)
    a0 = a1 = a2 = 0
    for n in range(24):
        a0 = _act(p0, 0, AL, AJ, AX, ok0, ok1); a1 = _act(p1, 1, AL, AJ, AX, ok0, ok1); a2 = _act(p2, 2, AL, AJ, AX, ok0, ok1)
        for x in range(3):
            if a0 != x: ok0[0, x] = False
            if a1 != x: ok0[1, x] = False
            if a2 != x: ok0[2, x] = False
            if n >= 1:
                if a0 != x: ok1[0, x] = False
                if a1 != x: ok1[1, x] = False
                if a2 != x: ok1[2, x] = False
    return a0, a1, a2


@njit(cache=True)
def match_counts(P3, Q0, Q1, AL, AJ, AX):
    """For each resident p3: number of (q0, q1) with outcome (X,X,L) or (Y,Y,R); and per pair the residents matched."""
    n3 = P3.shape[0]; cnt = np.zeros(n3, np.int64); per = np.zeros((Q0.shape[0], Q1.shape[0]), np.int64)
    for k in range(n3):
        for i in range(Q0.shape[0]):
            for j in range(Q1.shape[0]):
                a0, a1, a2 = play(Q0[i], Q1[j], P3[k], AL, AJ, AX)
                if (a0 == 1 and a1 == 1 and a2 == 0) or (a0 == 2 and a1 == 2 and a2 == 1):
                    cnt[k] += 1; per[i, j] += 1
    return cnt, per


@njit(cache=True)
def any_match(p3, Q0, Q1, AL, AJ, AX):
    for i in range(Q0.shape[0]):
        for j in range(Q1.shape[0]):
            a0, a1, a2 = play(Q0[i], Q1[j], p3, AL, AJ, AX)
            if (a0 == 1 and a1 == 1 and a2 == 0) or (a0 == 2 and a1 == 2 and a2 == 1): return i, j
    return -1, -1


def show(s, p):
    at = atoms_of(s); nm = [['N', 'X', 'Y'], ['N', 'X', 'Y'], ['L', 'R']]
    def A(i):
        Lv, j, x = at[i]; return 'BOX%s(%d=%s)' % ('1' if Lv else '', j + 1, nm[j][x])
    l = lambda v: nm[s][v]
    sh = p[0]
    if sh == 0: return l(p[3])
    if sh == 1: return 'if(%s,%s,%s)' % (A(p[1]), l(p[3]), l(p[4]))
    if sh == 2: return 'if(%s,if(%s,%s,%s),%s)' % (A(p[1]), A(p[2]), l(p[3]), l(p[4]), l(p[5]))
    return 'if(%s,%s,if(%s,%s,%s))' % (A(p[1]), l(p[3]), A(p[2]), l(p[4]), l(p[5]))


def part4():
    AL, AJ, AX = atom_arrays()
    P3 = programs(2, 2); Q0s = programs(0, 1); Q1s = programs(1, 1); Q0b = programs(0, 2); Q1b = programs(1, 2)
    cN = np.array((0, 0, 0, 0, 0, 0), np.int64)
    res = np.array([play(cN, cN, p, AL, AJ, AX)[2] == 0 for p in P3])
    R3 = P3[res]
    cnt, per = match_counts(R3, Q0s, Q1s, AL, AJ, AX)
    surv = np.where(cnt == 0)[0]
    out = {'player3_programs': int(len(P3)), 'residents_playing_L_at_status_quo': int(len(R3)),
           'deviator_programs_1atom': int(len(Q0s)), 'deviator_programs_2atoms': int(len(Q0b)),
           'residents_unmatched_by_1atom_pairs': int(len(surv)),
           'universal_matching_pairs_1atom': int((per == len(R3)).sum()),
           'best_pair_share_of_residents_matched': float(per.max() / len(R3))}
    i, j = np.unravel_index(per.argmax(), per.shape)
    out['best_pair'] = [show(0, Q0s[i]), show(1, Q1s[j])]
    hard = np.argsort(cnt)[:5]
    out['hardest_residents'] = [[show(2, R3[k]), int(cnt[k])] for k in hard]
    still = []
    for k in surv:
        a, b = any_match(R3[k], Q0b, Q1s, AL, AJ, AX)
        if a < 0: a, b = any_match(R3[k], Q0s, Q1b, AL, AJ, AX)
        if a < 0: a, b = any_match(R3[k], Q0b, Q1b, AL, AJ, AX)
        if a < 0: still.append(show(2, R3[k]))
    out['residents_unmatched_by_2atom_pairs'] = len(still); out['unmatched_examples'] = still[:10]
    return out


if __name__ == '__main__':
    out = {'part1': part1(), 'part2': part2(), 'part3': part3(), 'part4': part4()}
    json.dump(out, open('runs/three-coins-static.json', 'w'), indent=1)
    print(json.dumps(out, indent=1))
