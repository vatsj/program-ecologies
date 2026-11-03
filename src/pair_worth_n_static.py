"""Static supply numbers (spec Design 1; notes/pair-worth-n.md).  Run: python3 src/pair_worth_n_static.py

For each arm, exact evaluation of every triple of the slot catalogue (one program per slot) on the modal chain, accumulating the
seed-law weight of triples that play a grand coalition (any feasible sum), a grand-efficient coalition, and a core-proper
outcome, separately for each pattern of named / constant members, so that any dose delta follows by
P(delta) = sum_pat (1 - delta)^(#const) delta^(#named) S[pat].  Then: expected number of grand-playing individual triples on
one island (N^3 P), all-named triples, same-split T for B*, B, G, F."""
import json, math, os, sys, time
import numpy as np
from numba import njit
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pair_worth as PW
import pair_worth_n as PN

OUTP = os.path.join(PW.ROOT, 'runs', 'pair_worth_n')
NS = (100, 200, 400, 800)
DELTAS = (0.0125, 0.025, 0.05, 0.15, 0.5)


@njit(cache=True)
def class_sums(LN, ATP, ATA, ATL, ATS, OA, DF, OUT, K, named, wq, GR, EF, CO):
    S = np.zeros((8, 3))
    hist = np.empty((2, 3), np.int64); val = np.empty(3, np.int64)
    bad = 0
    for a in range(K):
        for b in range(K):
            wab = wq[0, a] * wq[1, b]
            if wab == 0.0:
                continue
            for c in range(K):
                w = wab * wq[2, c]
                if w == 0.0:
                    continue
                if not PW.eval_dl(LN, ATP, ATA, ATL, ATS, OA, DF, a, b, c, hist, val):
                    bad += 1
                    continue
                o = OUT[val[0], val[1], val[2]]
                pat = named[0, a] + 2 * named[1, b] + 4 * named[2, c]
                S[pat, 0] += w * GR[o]; S[pat, 1] += w * EF[o]; S[pat, 2] += w * CO[o]
    return S, bad


def member_weights(arm, menu):
    """(named flag, weight within type) per catalogue member id; constants 1/nact, named by the family's law."""
    G = menu.G
    n = G.nact
    K = menu.total
    named = np.zeros(K, np.int64); w = np.zeros(K)
    w[:n] = 1.0 / n
    for fi, f in enumerate(menu.fams):
        off = menu.off[fi]
        for r in range(menu.size[fi]):
            named[off + r] = 1
            if f.kind in PN.F_KINDS:
                s = r // n
                M = 25 if f.kind == 'F4' else 28
                w[off + r] = (7 - s) / M / n
            else:
                w[off + r] = 1.0 / menu.size[fi]
    return named, w


def arm_static(arm):
    G = PW.get_game('pw13')
    CLA, CLB = G.class_tables()
    GR = (G.KIND == 1).astype(np.float64)
    EF = (CLB == 1).astype(np.float64)
    CO = (CLA == 1).astype(np.float64)
    menu = PN.arm_menu_n(arm, 0.05)
    K = menu.total
    U = [np.arange(K, dtype=np.int64) for _ in range(3)]
    t = PW.ProgTable(menu, U)
    named, w = member_weights(arm, menu)
    nm = np.stack([named] * 3); wq = np.stack([w] * 3)
    t0 = time.time()
    S, bad = class_sums(*t.arrs(), G.OUT, K, nm, wq, GR, EF, CO)
    assert bad == 0
    return menu, S, time.time() - t0


def P_of(S, delta, col):
    tot = 0.0
    for pat in range(8):
        npn = bin(pat).count('1')
        tot += (1 - delta) ** (3 - npn) * delta ** npn * S[pat, col]
    return tot


def P_named_all(S, delta, col):
    return delta ** 3 * S[7, col]


def T_closed(arm, delta, N):
    """same-split / feasible-support count of one island at founding (closed form where one exists)."""
    if arm == 'CBs':
        n = delta * N / 28; return 28 * n ** 3
    if arm == 'CB':
        n = delta * N / 19; return 19 * n ** 3
    if arm == 'CG':
        n = delta * N / 28; return 28 * n ** 3
    return None


def main():
    os.makedirs(OUTP, exist_ok=True)
    out = dict(note='P_* = probability that a triple of founder draws (one per slot) plays: grand (any feasible sum), '
                    'grand efficient, core proper; counts = N^3 P (individual triples on one island); named3 = all three named; '
                    'T = closed-form same-split count (B*, B, G: arms of the spec) ; S[pat] = unit-weight sums by pattern '
                    '(bit s set: slot s named)', arms={})
    for arm in ('C', 'CG', 'CF', 'CFm', 'CF4', 'CB', 'CBs'):
        menu, S, wall = arm_static(arm)
        rec = dict(catalogue_per_slot=menu.total, eval_wall_s=round(wall, 1), S=S.tolist(), delta={})
        for d in DELTAS:
            r = {}
            for col, nm in enumerate(('grand_any', 'grand_eff', 'core')):
                p = P_of(S, d, col); pn = P_named_all(S, d, col)
                r['P_' + nm] = p
                r['P_named3_' + nm] = pn
                r['counts_' + nm] = {str(N): N ** 3 * p for N in NS}
                r['counts_named3_' + nm] = {str(N): N ** 3 * pn for N in NS}
            r['T_closed'] = {str(N): T_closed(arm, d, N) for N in NS}
            rec['delta'][str(d)] = r
        out['arms'][arm] = rec
        r5 = rec['delta']['0.05']
        print('%-4s catalogue %4d  eval %.0fs  delta .05: P(grand any) %.4e  P(grand eff) %.4e  P(core) %.4e  | named3: any %.3e eff %.3e | '
              'N^3 P(eff) at N=100,200,400,800: %s | T %s' % (
                  arm, menu.total, wall, r5['P_grand_any'], r5['P_grand_eff'], r5['P_core'], r5['P_named3_grand_any'], r5['P_named3_grand_eff'],
                  ['%.3g' % r5['counts_grand_eff'][str(N)] for N in NS], ['%.3g' % x if x is not None else '-' for x in r5['T_closed'].values()]), flush=True)
    # inoculation arms: fixed supply
    out['inoculation'] = {'CBk1': dict(copies_per_slot=1, same_split_triples_per_island=1, compatible_support_every_island=True),
                          'CBk4': dict(copies_per_slot=4, same_split_triples_per_island=64, compatible_support_every_island=True)}
    # F feasibility: probability three F's drawn from the marginal are feasible, and efficient (sum = 6)
    w = np.array([(7 - s) / 28.0 for s in range(7)])
    feas = 0.0; eff = 0.0
    for a in range(7):
        for b in range(7):
            for c in range(7):
                p = w[a] * w[b] * w[c]
                if a + b + c <= 6: feas += p
                if a + b + c == 6: eff += p
    out['F_three_feasible'] = dict(P_feasible=feas, P_efficient=eff, note='three independent F shares from the (7-s)/28 marginal')
    print('three-F feasible %.4f efficient %.4f' % (feas, eff))
    with open(os.path.join(OUTP, 'static.json'), 'w') as f:
        json.dump(out, f, indent=1)


if __name__ == '__main__':
    main()
