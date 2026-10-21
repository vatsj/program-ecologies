"""Tests for the coalition-proof auctions run (src/auctions.py; notes/coalition-proof-auctions.md).

The note's decimal examples are scaled by 10 (integer reports): values (2, .5, .5) -> (20, 5, 5), etc.
"""
import os
import sys
import itertools

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import auctions as A

AM41 = A.Auction(A.FAMILIES['AM'], 41)


def pay(rule, b, auc=AM41):
    k = auc.encode(b)
    return auc.payments(rule)[k], auc.win[k]


# ---------------------------------------------------------------- winner determination and the tie rule
def test_tie_more_winners_then_lowest_index():
    # P = AB at 20 against A + B = 20: more winners wins the tie
    p, w = pay('vcg', (20, 10, 10))
    assert list(w) == [0, 1, 1]
    # P above the sum wins
    p, w = pay('vcg', (21, 10, 10))
    assert list(w) == [1, 0, 0]
    # substitutes: bidders 0 and 1 both on A with equal reports: the lower index wins
    sub = A.Auction(A.FAMILIES['subs'], 11)
    k = sub.encode((5, 5, 3, 7))
    assert list(sub.win[k]) == [1, 0, 0, 1]
    # a zero report wins a free item by the more-winners rule
    k = sub.encode((0, 0, 0, 0))
    assert list(sub.win[k]) == [1, 0, 1, 0]


def test_am_vcg_closed_forms():
    rng = np.random.default_rng(1)
    for _ in range(400):
        bP, bA, bB = rng.integers(0, 41, 3)
        p, w = pay('vcg', (bP, bA, bB))
        if bP > bA + bB:
            assert list(w) == [1, 0, 0] and p[0] == bA + bB and p[1] == p[2] == 0
        else:
            assert list(w) == [0, 1, 1]
            assert p[1] == max(bP, bB) - bB and p[2] == max(bP, bA) - bA and p[0] == 0


# ---------------------------------------------------------------- the Ausubel-Milgrom numbers (note section 2, scaled by 10)
def test_ausubel_milgrom_losers_overbid():
    # values (2, .5, .5): VCG gives P the package at price 1; losers' overbid to 2 zeroes both prices
    p, w = pay('vcg', (20, 5, 5))
    assert list(w) == [1, 0, 0] and p[0] == 10
    p, w = pay('vcg', (20, 20, 20))
    assert list(w) == [0, 1, 1] and p[1] == p[2] == 0
    net = [5 - p[1], 5 - p[2]]
    assert net == [5, 5]                                   # +0.5 each under VCG
    p, w = pay('surcharge', (20, 20, 20))
    assert p[1] + p[2] >= 20 - 1e-9
    assert [5 - p[1], 5 - p[2]] == [-5, -5]                # -0.5 each under the surcharge


def test_ausubel_milgrom_threshold_and_shading():
    p, w = pay('vcg', (20, 15, 15))
    assert p[1] == p[2] == 5                               # 0.5 each
    p, w = pay('surcharge', (20, 15, 15))
    assert p[1] == p[2] == 10                              # 1, 1
    p, w = pay('surcharge', (20, 12, 15))                  # bidder 2 shades to 1.2
    assert p[1] == 8.5 and p[2] == 11.5                    # 0.85 / 1.15
    assert (15 - p[1]) - (15 - 10) == 1.5                  # a gain of 0.15 for the shader
    assert (15 - p[2]) - (15 - 10) == -1.5                 # taken from bidder 3


# ---------------------------------------------------------------- the surcharge rule
def _core_ok(auc, k):
    """brute-force core check of the surcharge payments at profile k over all bidder sets S."""
    n = auc.n
    p = auc.payments('surcharge')[k]
    win = auc.win[k]; b = auc.B[k]
    for S in range(1, 1 << n):
        lhs = sum(b[i] * win[i] - p[i] for i in range(n) if S >> i & 1)
        if lhs > auc.W[k] - auc.Wex[S][k] + 1e-9:
            return False
    return all(p[i] <= b[i] + 1e-9 for i in range(n) if win[i]) and (p >= -1e-9).all()


def test_surcharge_in_core_and_zero_iff_vcg_in_core():
    for fam in ('AM', 'subs', 'twopk', 'AMplus'):
        auc = A.Auction(A.FAMILIES[fam], 7)
        pv = auc.payments('vcg'); ps = auc.payments('surcharge')
        n = auc.n
        for k in range(0, auc.M, 1 if auc.M < 3000 else 7):
            assert _core_ok(auc, k), (fam, auc.B[k])
            # VCG in the core iff the surcharge is zero
            win = auc.win[k]; b = auc.B[k]
            vcg_core = all(sum(b[i] * win[i] - pv[k, i] for i in range(n) if S >> i & 1) <= auc.W[k] - auc.Wex[S][k] + 1e-9
                           for S in range(1, 1 << n))
            assert vcg_core == (np.abs(ps[k] - pv[k]).sum() < 1e-9), (fam, b)


def test_surcharge_matches_generic_lp_qp():
    rng = np.random.default_rng(5)
    for fam in ('AM', 'subs', 'twopk', 'AMplus'):
        auc = A.Auction(A.FAMILIES[fam], 9)
        ps = auc.payments('surcharge')
        for k in rng.choice(auc.M, 60, replace=False):
            g = A.surcharge_generic(auc.B[k], auc.pk, auc)
            assert np.abs(g - ps[k]).max() < 1e-4, (fam, auc.B[k], g, ps[k])


def test_surcharge_minimal_revenue():
    from scipy.optimize import linprog
    auc = A.Auction(A.FAMILIES['twopk'], 8)
    ps = auc.payments('surcharge')
    rng = np.random.default_rng(2)
    for k in rng.choice(auc.M, 40, replace=False):
        win = [i for i in range(auc.n) if auc.win[k, i]]
        if not win:
            continue
        b = auc.B[k].astype(float)
        rows, rhs = [], []
        for S in range(1, 1 << auc.n):
            sw = [i for i in win if S >> i & 1]
            if sw:
                rows.append([1.0 if i in sw else 0.0 for i in win])
                rhs.append(sum(b[i] for i in sw) - (auc.W[k] - auc.Wex[S][k]))
        res = linprog(np.ones(len(win)), A_ub=-np.array(rows), b_ub=-np.array(rhs), bounds=[(0, b[i]) for i in win], method='highs')
        assert abs(ps[k].sum() - res.fun) < 1e-7


# ---------------------------------------------------------------- 2XL (note section 8)
def test_twoxl_leader_values():
    vh, vl = A.twoxl_leader_values(100, 60, 200, 'weak')   # v = (10, 6) on a 0.1 grid
    assert (vh, vl) == (69, 50)                            # 6.9 and 5.0
    # equal values: the 50-50 split is the only nonempty case (sum of the leader values = v)
    a, b = A.twoxl_leader_values(80, 80, 200, 'weak')
    assert a == b


# ---------------------------------------------------------------- the notion kernel against a plain-python reference
def _ref_gain(auc, rule, v, S, Rd):
    win, pay_ = auc.tables(rule)
    n, R = auc.n, auc.R
    C = [i for i in range(n) if i not in S]

    def pf(prof, i):
        k = auc.encode(prof)
        return v[i] * int(win[k, i]) - pay_[k, i]

    out = {}
    truth = sum(pf(tuple(v), i) for i in S)
    totals = {0: [], 1: [], 2: [], 3: [], 4: []}
    best = {k: -1e18 for k in range(5)}
    for dS in itertools.product(range(Rd), repeat=len(S)):
        if all(dS[s] == v[S[s]] for s in range(len(S))):
            continue

        def prof(r):
            p = list(v)
            for s, i in enumerate(S):
                p[i] = dS[s]
            for j, i in enumerate(C):
                p[i] = r[j]
            return tuple(p)

        def closure(weak):
            start = tuple(v[i] for i in C)
            seen = {start}; queue = [start]; ne = []
            while queue:
                r = queue.pop()
                is_ne = True
                for j, i in enumerate(C):
                    vals = []
                    for bb in range(R):
                        r2 = list(r); r2[j] = bb
                        vals.append(pf(prof(r2), i))
                    m = max(vals)
                    if vals[r[j]] < m - 1e-9:
                        is_ne = False
                    for bb in range(R):
                        if vals[bb] >= m - 1e-9 and (vals[r[j]] < m - 1e-9 or (weak and bb != r[j])):
                            r2 = list(r); r2[j] = bb; r2 = tuple(r2)
                            if r2 not in seen:
                                seen.add(r2); queue.append(r2)
                if is_ne:
                    ne.append(r)
            return ne

        def stot(r):
            return sum(pf(prof(r), i) for i in S)

        def closest(ne):
            return min(ne, key=lambda r: (sum(abs(r[j] - v[C[j]]) for j in range(len(C))), sum(r[j] * R ** j for j in range(len(C)))))

        ns, nw = closure(False), closure(True)
        allr = list(itertools.product(range(R), repeat=len(C)))
        ctot = {r: sum(pf(prof(r), i) for i in C) for r in allr}
        mx = max(ctot.values())
        n2 = [r for r in allr if ctot[r] >= mx - 1e-9]
        vals = {}
        if ns:
            vals[0] = stot(closest(ns)); vals[2] = min(stot(r) for r in ns)
        if nw:
            vals[1] = min(stot(r) for r in nw)
        vals[3] = stot(closest(n2)); vals[4] = min(stot(r) for r in n2)
        for k, x in vals.items():
            best[k] = max(best[k], x - truth)
    return best


def test_kernel_matches_reference():
    G = 3
    for fam, rule in (('AM', 'vcg'), ('AM', 'surcharge'), ('subs', 'vcg')):
        auc = A.Auction(A.FAMILIES[fam], 5 if fam == 'subs' else 7)
        if fam == 'subs':
            mask = np.zeros(G ** 4, bool); mask[::9] = True
        else:
            mask = None
        res = A.analyze(auc, rule, G, mask=mask)
        insts = res['insts']
        pick = np.nonzero(mask)[0] if mask is not None else range(len(insts))
        for q in list(pick)[:12]:
            v = tuple(int(x) for x in insts[q])
            for si, S in enumerate(res['SS']):
                ref = _ref_gain(auc, rule, v, S, auc.R)
                for k in range(5):
                    assert abs(res['gain'][k, q, si] - ref[k]) < 1e-7, (fam, rule, v, S, k, res['gain'][k, q, si], ref[k])


def test_substitutes_vcg_in_core_and_robust():
    auc = A.Auction(A.FAMILIES['subs'], 7)
    G = 3
    inc, sur, _ = A.vcg_in_core(auc, G)
    assert inc.all()
