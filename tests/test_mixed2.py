"""Tests for src/mixed2.py: the hand tables of notes/mixed2.md section 1 (typed in here literally), an independent
exact-rational reference evaluator (recursion over the expression tree with explicit best-response formulas, no
tensors), the posterior in Endgame II's `cr`, the fresh card in simulation, the price at c = 0, the bounded-`cr`
audit, canonical enumeration counts, the chain and the lottery kernel on toy games."""
import os, sys, math, itertools
from fractions import Fraction as Fr
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import mixed2 as M

TOL = 1e-9
_cache = {}


def built(game, arm, n, D=12, workmode=0):
    key = (game, arm, n, D, workmode)
    if key not in _cache:
        L = M.Lang2(game, arm, n)
        _cache[key] = (L, M.evaluate(L, D, workmode=workmode))
    return _cache[key]


# ------------------------------------------------------------------ the independent reference evaluator
class Ref:
    """Exact rational evaluator written from the semantics of notes/mixed2.md section 1.0 by recursion over the node arrays."""

    def __init__(self, L):
        self.L = L
        self.game = L.game
        self.wts = (Fr(1, 3), Fr(2, 3)) if L.game == 'end' else (Fr(1), Fr(0))
        self.memo = {}
        self.cmemo = {}

    # ---- action distributions
    def G(self, r, a, b, d):
        """value of program node a (context r) against program node b (other role) with d levels left: [[x0,x1,F] for card W, L]."""
        key = (r, a, b, d)
        if key not in self.memo:
            self.memo[key] = self.ev(r, a, a, b, d)
        return self.memo[key]

    def ev(self, r, e, a, b, d):
        L = self.L
        o = L.op[e]
        if o == M.OP_C0:
            return [[Fr(1), Fr(0), Fr(0)]] * 2
        if o == M.OP_C1:
            return [[Fr(0), Fr(1), Fr(0)]] * 2
        if o == M.OP_X:
            return [[Fr(1, 2), Fr(1, 2), Fr(0)]] * 2
        if o == M.OP_COIN:
            u = self.ev(r, L.A[e], a, b, d); v = self.ev(r, L.B[e], a, b, d)
            return [[(u[c][j] + v[c][j]) / 2 for j in range(3)] for c in range(2)]
        if o == M.OP_CARD:
            u = self.ev(r, L.A[e], a, b, d); v = self.ev(r, L.B[e], a, b, d)
            return [u[0], v[1]]
        if o == M.OP_APP:
            if d == 0:
                return [[Fr(0), Fr(0), Fr(1)]] * 2
            arg = a if L.K[e] == M.APP_ME else int(L.B[e])
            return self.G(1 - r, b, arg, d - 1)
        if o == M.OP_IF:
            q = self.ev(r, L.C[e], a, b, d)
            p0 = self.wts[0] * q[0][0] + self.wts[1] * q[1][0]
            p1 = self.wts[0] * q[0][1] + self.wts[1] * q[1][1]
            pf = self.wts[0] * q[0][2] + self.wts[1] * q[1][2]
            u = self.ev(r, L.A[e], a, b, d); v = self.ev(r, L.B[e], a, b, d)
            out = [[p0 * u[c][j] + p1 * v[c][j] for j in range(3)] for c in range(2)]
            for c in range(2):
                out[c][2] += pf
            return out
        if o in (M.OP_CR, M.OP_SR, M.OP_SRK):
            t = int(L.typ[e])
            ch = self.ev(r, L.A[e], a, b, d)
            m = {(cc, y): self.wts[cc] * ch[cc][y] for cc in range(2) for y in range(2)}
            pf = self.wts[0] * ch[0][2] + self.wts[1] * ch[1][2]
            z = 1 - pf
            if z == 0:
                return [[Fr(0), Fr(0), Fr(1)]] * 2
            if o == M.OP_CR:
                res = []
                for oc in range(2):
                    p0 = self.cr_resp(t, oc, m, z)
                    res.append([z * p0, z * (1 - p0), pf])
                return res
            if o == M.OP_SR:
                res = []
                for oc in range(2):
                    acc = Fr(0)
                    for (cc, y), mm in m.items():
                        acc += mm * self.sr_resp(t, oc, cc, y)
                    res.append([acc, z - acc, pf])
                return res
            k = int(L.K[e])                     # sr_k, inspection
            q = (m[(0, 1)] + m[(1, 1)]) / z
            res = []
            for oc in range(2):
                acc = Fr(0)
                for nn in range(k + 1):
                    pm = math.comb(k, nn) * q ** nn * (1 - q) ** (k - nn)
                    f1 = Fr(nn, k)
                    acc += pm * self.srk_resp(t, f1)
                zk = z ** k
                res.append([zk * acc, zk * (1 - acc), 1 - zk])
            return res
        raise ValueError(o)

    def cr_resp(self, t, oc, m, z):
        """probability of own action 0 for the exact best response, ties by the own coin (explicit formulas)."""
        if self.game == 'insp':
            if t == 0:                               # inspector: inspect iff cheat prob > 1/4
                q = (m[(0, 1)] + m[(1, 1)]) / z
                d = 4 * q - 1
            else:                                    # inspectee: comply iff inspection prob > 1/4
                p = (m[(0, 0)] + m[(1, 0)]) / z
                d = 4 * p - 1
        else:
            if t == 1:                               # II: call iff 4 m_LB - 2 m_WB > 0 (action 0 = CALL)
                d = (4 * m[(1, 0)] - 2 * m[(0, 0)]) / z
            else:                                    # I with card oc: action 0 = BET
                q = (m[(0, 0)] + m[(1, 0)]) / z
                d = 2 * q if oc == 0 else 2 - 4 * q
        return Fr(1) if d > 0 else (Fr(1, 2) if d == 0 else Fr(0))

    def sr_resp(self, t, oc, cc, y):
        if self.game == 'insp':
            if t == 0:
                return Fr(1) if y == 1 else Fr(0)            # sampled cheat -> inspect
            return Fr(1) if y == 0 else Fr(0)                # sampled inspection -> comply
        if t == 1:
            if y == 1:
                return Fr(1, 2)                              # sampled check
            return Fr(0) if cc == 0 else Fr(1)               # sampled bet by a winner -> FOLD (action 1), by a loser -> CALL
        # I with card oc against a sampled II action y (0 = CALL)
        if y == 0:
            return Fr(1) if oc == 0 else Fr(0)               # CALL: winner bets, loser checks
        return Fr(1, 2) if oc == 0 else Fr(1)                # FOLD: winner indifferent, loser bets

    def srk_resp(self, t, f1):
        # frequency of opponent action 1 among k draws
        if t == 0:
            d = 4 * f1 - 1
        else:
            d = 4 * (1 - f1) - 1
        return Fr(1) if d > 0 else (Fr(1, 2) if d == 0 else Fr(0))

    # ---- payoffs with forfeits
    def payoff(self, a, b, d):
        """(U0, U1) game payoffs of role-0 program node a against role-1 program node b."""
        g = M.GAMES[self.game]
        P0 = [[[Fr(int(g['Pay0'][c, x, y])) for y in range(2)] for x in range(2)] for c in range(2)]
        P1 = [[[Fr(int(g['Pay1'][c, x, y])) for y in range(2)] for x in range(2)] for c in range(2)]
        g0 = self.G(0, a, b, d); g1 = self.G(1, b, a, d)[0]
        u0 = u1 = Fr(0)
        for c in range(2):
            wc = self.wts[c]
            if wc == 0:
                continue
            for x in range(3):
                for y in range(3):
                    pr = wc * g0[c][x] * g1[y]
                    if pr == 0:
                        continue
                    if x < 2 and y < 2:
                        u0 += pr * P0[c][x][y]; u1 += pr * P1[c][x][y]
                    elif x == 2 and y < 2:               # role 0 forfeits: its worst action against y
                        col = [P0[c][xx][y] for xx in range(2)]
                        mn = min(col); tied = [xx for xx in range(2) if col[xx] == mn]
                        u0 += pr * mn; u1 += pr * sum(P1[c][xx][y] for xx in tied) / len(tied)
                    elif x < 2 and y == 2:               # role 1 forfeits
                        row = [P1[c][x][yy] for yy in range(2)]
                        mn = min(row); tied = [yy for yy in range(2) if row[yy] == mn]
                        u1 += pr * mn; u0 += pr * sum(P0[c][x][yy] for yy in tied) / len(tied)
                    else:
                        u0 += pr * min(P0[cc][xx][yy] for cc in range(2) for xx in range(2) for yy in range(2))
                        u1 += pr * min(P1[cc][xx][yy] for cc in range(2) for xx in range(2) for yy in range(2))
        return u0, u1

    # ---- serial depth costs
    def cost(self, r, a, b, d, mode='E'):
        key = (r, a, b, d, mode)
        if key not in self.cmemo:
            self.cmemo[key] = self.cexp(r, a, a, b, d, mode)
        return self.cmemo[key]

    def cexp(self, r, e, a, b, d, mode):
        L = self.L
        o = L.op[e]
        if o in (M.OP_C0, M.OP_C1, M.OP_X):
            return Fr(0)
        if o == M.OP_COIN:
            u = self.cexp(r, L.A[e], a, b, d, mode); v = self.cexp(r, L.B[e], a, b, d, mode)
            return (u + v) / 2 if mode == 'E' else max(u, v)
        if o == M.OP_CARD:
            u = self.cexp(r, L.A[e], a, b, d, mode); v = self.cexp(r, L.B[e], a, b, d, mode)
            return self.wts[0] * u + self.wts[1] * v if mode == 'E' else max(u, v)
        if o == M.OP_APP:
            if d == 0:
                return Fr(0)
            arg = a if L.K[e] == M.APP_ME else int(L.B[e])
            return 1 + self.cost(1 - r, b, arg, d - 1, mode)
        if o == M.OP_IF:
            q = self.ev(r, L.C[e], a, b, d)
            p0 = self.wts[0] * q[0][0] + self.wts[1] * q[1][0]
            p1 = self.wts[0] * q[0][1] + self.wts[1] * q[1][1]
            cq = self.cexp(r, L.C[e], a, b, d, mode)
            cu = self.cexp(r, L.A[e], a, b, d, mode); cv = self.cexp(r, L.B[e], a, b, d, mode)
            return cq + (p0 * cu + p1 * cv if mode == 'E' else max(cu, cv))
        if o == M.OP_CR:
            return self.cexp(r, L.A[e], a, b, d, 'M')
        if o in (M.OP_SR, M.OP_SRK):
            cc = self.cexp(r, L.A[e], a, b, d, mode)
            return cc if o == M.OP_SR else int(L.K[e]) * cc
        raise ValueError(o)


def fr(x):
    return float(x)


# ------------------------------------------------------------------ the hand tables of notes/mixed2.md (typed literally)
INSP_ROWS = ['I', 'N', 'X', 'P14', 'P516', 'P38', 'RI', 'CRI']
INSP_COLS = ['C', 'K', 'X', 'CRC', 'RC']
F_ = Fr
INSP_TABLE = {
    'I': [(-1, 0), (-1, -3), (-1, F_(-3, 2)), (-1, 0), (-1, 0)],
    'N': [(0, 0), (-4, 1), (-2, F_(1, 2)), (-4, 1), (-4, 1)],
    'X': [(F_(-1, 2), 0), (F_(-5, 2), -1), (F_(-3, 2), F_(-1, 2)), (F_(-1, 2), 0), (F_(-3, 2), F_(-1, 2))],
    'P14': [(F_(-1, 4), 0), (F_(-13, 4), 0), (F_(-7, 4), 0), (F_(-7, 4), 0), (F_(-5, 2), 0)],
    'P516': [(F_(-5, 16), 0), (F_(-49, 16), F_(-1, 4)), (F_(-27, 16), F_(-1, 8)), (F_(-5, 16), 0), (F_(-141, 64), F_(-11, 64))],
    'P38': [(F_(-3, 8), 0), (F_(-23, 8), F_(-1, 2)), (F_(-13, 8), F_(-1, 4)), (F_(-3, 8), 0), (F_(-31, 16), F_(-5, 16))],
    'RI': [(0, 0), (-1, -3), (F_(-3, 2), F_(-1, 2)), (-4, -3), (-4, -3)],
    'CRI': [(0, 0), (-1, -3), (-1, F_(-3, 2)), (-4, -3), (-4, -3)],
}
END_ROWS = ['BET', 'CHECK', 'XI', 'HON', 'EQ', 'EXP', 'CRI']
END_COLS = ['CALL', 'FOLD', 'X', 'CRII', 'RII', 'SRII']
END_TABLE = {   # payoff to I (II receives the negative except in a mutual forfeit)
    'BET': [-1, 1, 0, -1, -1, F_(-1, 3)],
    'CHECK': [F_(-1, 3)] * 6,
    'XI': [F_(-2, 3), F_(1, 3), F_(-1, 6), F_(-2, 3), F_(-1, 6), F_(-1, 4)],
    'HON': [F_(1, 3), F_(-1, 3), 0, F_(-1, 3), F_(-1, 9), F_(-1, 9)],
    'EQ': [0] * 6,
    'EXP': [F_(1, 3), 1, 0, None, None, None],           # the reader columns: see test_exp_against_readers (erratum)
    'CRI': [F_(1, 3), 1, 0, -3, -3, -3],
}


def test_inspection_hand_table():
    L, ev = built('insp', 'exact', 8)
    for rn in INSP_ROWS:
        a = M.prog_of(L, 0, M.NAMED_INSP[0][rn])
        for j, cn in enumerate(INSP_COLS):
            b = M.prog_of(L, 1, M.NAMED_INSP[1][cn])
            h0, h1 = INSP_TABLE[rn][j]
            assert abs(ev['U0'][a, b] - float(h0)) < TOL, (rn, cn, ev['U0'][a, b], h0)
            assert abs(ev['U1'][b, a] - float(h1)) < TOL, (rn, cn, ev['U1'][b, a], h1)


def test_endgame_hand_table():
    L, ev = built('end', 'exact', 7)
    for rn in END_ROWS:
        a = M.prog_of(L, 0, M.NAMED_END[0][rn])
        for j, cn in enumerate(END_COLS):
            h = END_TABLE[rn][j]
            if h is None:
                continue
            b = M.prog_of(L, 1, M.NAMED_END[1][cn]) if cn != 'SRII' else None
            if cn == 'SRII':
                continue                                     # sr is not in the exact arm; tested in the matched arm below
            assert abs(ev['U0'][a, b] - float(h)) < TOL, (rn, cn, ev['U0'][a, b], h)
            mutual = (h == -3 and rn == 'CRI')
            exp1 = -3.0 if mutual else -float(h)
            assert abs(ev['U1'][b, a] - exp1) < TOL, (rn, cn)


def test_endgame_srii_column_matched_arm():
    L, ev = built('end', 'matched', 7)
    for rn in ['BET', 'CHECK', 'XI', 'HON', 'EQ', 'CRI']:
        a = M.prog_of(L, 0, M.NAMED_END[0][rn]) if rn != 'CRI' else M.prog_of(L, 0, ('sr', M.APPME))
        b = M.prog_of(L, 1, ('sr', M.APPME))
        if rn == 'CRI':
            continue                                         # sr-I reading sr-II: mutual forfeit, covered by the reference test
        h = END_TABLE[rn][5]
        assert abs(ev['U0'][a, b] - float(h)) < TOL, (rn, ev['U0'][a, b], h)


def test_exp_against_readers_erratum():
    """notes/mixed2.md 1.2 said EXP against the reader columns is a mutual forfeit (-3); it is not: the winner branch of
    `card BET cr(THEM(ME))` does not read, so only the loser slice loops.  Hand recursion (notes section 2): against CRII,
    U_I = 473/2187."""
    L, ev = built('end', 'exact', 7)
    a = M.prog_of(L, 0, M.NAMED_END[0]['EXP'])
    b = M.prog_of(L, 1, M.NAMED_END[1]['CRII'])
    assert abs(ev['U0'][a, b] - 473 / 2187) < TOL
    G0 = ev['G0'][a, b]; G1 = ev['G1'][b, a]
    assert abs(G0[0] - 1) < TOL and abs(G0[3 + 1] - 665 / 729) < TOL and abs(G0[3 + 2] - 64 / 729) < TOL
    assert abs(G1[0] - 665 / 729) < TOL and abs(G1[2] - 64 / 729) < TOL


def test_nash_and_identities():
    # inspectee with cheat probability 1/4 (coin C X): every inspector earns -1; inspector with p = 1/4 gives the inspectee 0
    L, ev = built('insp', 'exact', 8)
    b = M.prog_of(L, 1, ('coin', 'c0', 'x'))
    for nm in ('I', 'N', 'X', 'P14', 'P38'):
        a = M.prog_of(L, 0, M.NAMED_INSP[0][nm])
        assert abs(ev['U0'][a, b] + 1) < TOL
    a = M.prog_of(L, 0, M.NAMED_INSP[0]['P14'])
    for nm in ('C', 'K', 'X'):
        assert abs(ev['U1'][M.prog_of(L, 1, M.NAMED_INSP[1][nm]), a]) < TOL
    # commitment: the visible p > 1/4 gives the inspector -p against C; the coin tie at 1/4 gives -7/4 against CRC
    a14 = M.prog_of(L, 0, M.NAMED_INSP[0]['P14']); crc = M.prog_of(L, 1, M.NAMED_INSP[1]['CRC'])
    assert abs(ev['U0'][a14, crc] + 7 / 4) < TOL


def test_dyadic_grid_blind_arm():
    L = M.Lang2('insp', 'blind', 8)
    ev = M.evaluate(L, 12)
    # p of each program: inspect probability against any inspectee (non-reading)
    p = ev['G0'][:, 0, 0]
    ps = sorted(set(np.round(p, 12)))
    assert len(ps) == 17
    above = [x for x in ps if x > 0.25 + 1e-9]
    assert abs(above[0] - 5 / 16) < 1e-12
    # sizes: 3/8 at size 5, 5/16 at size 7
    sz = L.size[L.progs[0]]
    assert sz[np.abs(p - 3 / 8) < 1e-12].min() == 5
    assert sz[np.abs(p - 5 / 16) < 1e-12].min() == 7
    assert sz[np.abs(p - 1 / 4) < 1e-12].min() == 3


def test_endgame_equilibrium_formulas_and_minimax():
    L, ev = built('end', 'exact', 7)
    # U_I(w, l, q) = -1/3 + 2/3 w q + 4/3 l (1 - 2 q); equilibrium (1, 1/4, 1/2), value 0
    f = lambda w, l, q: -1 / 3 + 2 / 3 * w * q + 4 / 3 * l * (1 - 2 * q)
    assert abs(f(1, 0.25, 0.5)) < 1e-15
    assert abs(f(1, 0.25, 0.0)) < 1e-15 and abs(f(1, 0.25, 1.0)) < 1e-15
    # the paper's value 2aP(2a+2b)/(2a+b) - a at a = 1, b = 2, P = 1/3 is 0; bluff b/(2a+b) P/(1-P) = 1/4
    assert abs(2 * 1 * (1 / 3) * (2 + 4) / (2 + 2) - 1) < 1e-15 and abs((2 / 4) * (1 / 3) / (2 / 3) - 0.25) < 1e-15
    eq = M.prog_of(L, 0, M.NAMED_END[0]['EQ']); eq7 = M.prog_of(L, 0, M.NAMED_END[0]['EQ7'])
    x2 = M.prog_of(L, 1, 'x')
    assert np.abs(ev['U0'][eq]).max() < TOL                       # EQ earns exactly 0 against every II program
    assert np.abs(ev['U0'][eq7]).max() < TOL
    assert ev['U1'][x2].min() > -TOL                              # II's coin never loses against any I program
    chk = M.prog_of(L, 0, 'c1'); xi = M.prog_of(L, 0, 'x'); bet = M.prog_of(L, 0, 'c0'); hon = M.prog_of(L, 0, ('card', 'c0', 'c1'))
    assert abs(ev['U1'][x2, chk] - 1 / 3) < TOL and abs(ev['U1'][x2, xi] - 1 / 6) < TOL
    assert abs(ev['U1'][x2, bet]) < TOL and abs(ev['U1'][x2, hon]) < TOL
    # equality exactly when the winner always bets (w = 1): U1[X, a] = (1 - w)/3 for non-reading a
    nonread = ~L.has_app[0]
    w = ev['G0'][:, 0, 0]
    assert np.abs((1 - w)[nonread] / 3 - ev['U1'][x2][nonread]).max() < TOL


def test_cr_posterior():
    L, ev = built('end', 'exact', 7)
    crii = M.prog_of(L, 1, M.NAMED_END[1]['CRII'])
    call = lambda spec: ev['G1'][crii, M.prog_of(L, 0, spec)][0]
    eq = M.NAMED_END[0]['EQ']
    assert abs(call(eq) - 0.5) < TOL                                              # indifferent at (1, 1/4): the tie coin
    assert abs(call(('card', 'c0', ('coin', 'x', ('coin', 'c1', 'x')))) - 1) < TOL     # l = 3/8, 4l > w: call
    assert abs(call(('card', 'c0', ('coin', 'c1', ('coin', 'c1', 'x')))) - 0) < TOL     # l = 1/8, 4l < w: fold
    assert abs(call('c1') - 0.5) < TOL                                           # I never bets: payoff-indifferent, own coin
    assert abs(call('c0') - 1) < TOL                                             # always bets: posterior 2/3 bluff, call
    assert abs(call(('card', 'c0', 'c1')) - 0) < TOL                              # honest bettor: fold


def test_fresh_card_in_simulation():
    """II reads I with a card independent of the real one: RII calls with probability P(sampled I bets) = w/3 + 2l/3, and
    SRII (a draw of card and action) with 1/2 + l/3 - w/6, both different from reading the real card."""
    L, ev = built('end', 'exact', 7)
    rii = M.prog_of(L, 1, M.NAMED_END[1]['RII'])
    for spec, w, l in ((M.NAMED_END[0]['HON'], 1, 0), (M.NAMED_END[0]['EQ'], 1, 0.25), ('c0', 1, 1), ('x', .5, .5)):
        assert abs(ev['G1'][rii, M.prog_of(L, 0, spec)][0] - (w / 3 + 2 * l / 3)) < TOL
    L2, ev2 = built('end', 'matched', 7)
    srii = M.prog_of(L2, 1, ('sr', M.APPME))
    for spec, w, l in ((M.NAMED_END[0]['HON'], 1, 0), (M.NAMED_END[0]['EQ'], 1, 0.25), ('c0', 1, 1), ('x', .5, .5)):
        assert abs(ev2['G1'][srii, M.prog_of(L2, 0, spec)][0] - (0.5 + l / 3 - w / 6)) < TOL
    # EQ's bluff rate is read card-free: against EQ the mean call rate of RII is 1/2
    assert abs(ev['G1'][rii, M.prog_of(L, 0, M.NAMED_END[0]['EQ'])][0] - 0.5) < TOL


def test_price_at_c0_and_depths():
    L, ev = built('insp', 'exact', 8)
    arms, _, _ = M.build_arm('insp', 'exact', 8, prices=(0.0, 0.01))
    A0, A1 = arms[0.0], arms[0.01]
    assert np.abs(A0.UA - A0.UAg).max() < 1e-12 and np.abs(A0.UB - A0.UBg).max() < 1e-12
    ri = M.prog_of(L, 0, M.NAMED_INSP[0]['RI']); cri = M.prog_of(L, 0, M.NAMED_INSP[0]['CRI'])
    rc = M.prog_of(L, 1, M.NAMED_INSP[1]['RC']); crc = M.prog_of(L, 1, M.NAMED_INSP[1]['CRC'])
    c_, k_ = M.prog_of(L, 1, 'c0'), M.prog_of(L, 1, 'c1')
    for r_ in (ri, cri):
        for nr in (c_, k_):
            assert ev['E0'][r_, nr] == 1.0
        for rd in (rc, crc):
            assert ev['E0'][r_, rd] == 12.0 and ev['E1'][rd, r_] == 12.0
    i_, n_ = M.prog_of(L, 0, 'c0'), M.prog_of(L, 0, 'c1')
    for rd in (rc, crc):
        assert ev['E1'][rd, i_] == 1.0 and ev['E1'][rd, n_] == 1.0
    assert ev['E0'][i_].max() == 0.0 and ev['E1'][c_].max() == 0.0
    # priced payoff: RC against I at c = 0.01 is 0 - 0.01
    assert abs((ev['U1'][rc, i_] - 0.01 * ev['E1'][rc, i_]) + 0.01) < 1e-12
    # Endgame: EXP pays 2/3 of a level against a non-reader (winner branch does not read), CRI pays 1, mutual readers 12
    Le, eve = built('end', 'exact', 7)
    exp_ = M.prog_of(Le, 0, M.NAMED_END[0]['EXP']); cri_e = M.prog_of(Le, 0, M.NAMED_END[0]['CRI'])
    x_ = M.prog_of(Le, 1, 'x'); crii = M.prog_of(Le, 1, M.NAMED_END[1]['CRII'])
    assert abs(eve['E0'][exp_, x_] - 2 / 3) < TOL and eve['E0'][cri_e, x_] == 1.0
    assert eve['E0'][cri_e, crii] == 12.0 and eve['E1'][crii, cri_e] == 12.0
    # sr_k pays k levels against a non-reader
    Lk, evk = built('insp', 'sr4', 8)
    srk4 = M.prog_of(Lk, 1, ('srk', M.APPME))
    assert evk['E1'][srk4, M.prog_of(Lk, 0, 'c0')] == 4.0
    Lk, evk = built('insp', 'sr16', 8)
    assert evk['E1'][M.prog_of(Lk, 1, ('srk', M.APPME)), M.prog_of(Lk, 0, 'c1')] == 16.0


def test_bounded_cr_audit():
    L, ev = built('end', 'exact', 7)
    a = M.prog_of(L, 0, M.NAMED_END[0]['EXP']); b = M.prog_of(L, 1, M.NAMED_END[1]['CRII'])
    # CRII (role 1) reads EXP's distribution on D - 1 levels; EXP's actual one differs (hand recursion: the loser slice bets with
    # probability 211/243 at level 11 and 0 at level 12), so the bounded read is not the actual distribution
    assert abs(ev['prevG0'][a, b][3] - 211 / 243) < TOL and abs(ev['G0'][a, b][3]) < TOL
    assert np.abs(ev['prevG0'][a, b] - ev['G0'][a, b]).max() > 1e-6
    x = M.prog_of(L, 1, 'x')
    assert np.abs(ev['prevG1'][x, a] - ev['G1'][x, a]).max() < TOL        # a non-reader: the read equals the actual
    arms, _, _ = M.build_arm('end', 'exact', 7, prices=(0.0,))
    A = arms[0.0]
    assert A.Dcr1[int(A.cls_of[1][b]), int(A.cls_of[0][a])] == 1.0 and A.Dcr0.sum() >= 0


def test_reference_agreement_all_pairs_small_depth():
    for game, arm, n in (('insp', 'exact', 8), ('insp', 'sr4', 8), ('end', 'exact', 7), ('end', 'matched', 7)):
        for D in (3, 12):
            L, ev = built(game, arm, n, D=D)
            ref = Ref(L)
            rng = np.random.default_rng(5 + D)
            pairs = [(int(rng.integers(L.S0)), int(rng.integers(L.S1))) for _ in range(6 if D == 12 else 30)]
            # guarded, cap-boundary and reader pairs
            rd0 = np.nonzero(L.has_app[0])[0]; rd1 = np.nonzero(L.has_app[1])[0]
            pairs += [(int(rng.choice(rd0)), int(rng.choice(rd1))) for _ in range(6 if D == 12 else 25)]
            for a, b in pairs:
                na, nb = L.progs[0][a], L.progs[1][b]
                g0 = ref.G(0, na, nb, D); g1 = ref.G(1, nb, na, D)
                u0, u1 = ref.payoff(na, nb, D)
                W0 = ev['G0'].shape[2]
                for c in range(2 if W0 == 6 else 1):
                    for j in range(3):
                        assert abs(float(g0[c][j]) - ev['G0'][a, b, 3 * c + j]) < 1e-9, (game, arm, D, L.src(na), L.src(nb), c, j)
                for j in range(3):
                    assert abs(float(g1[0][j]) - ev['G1'][b, a, j]) < 1e-9, (game, arm, D, L.src(na), L.src(nb), j)
                assert abs(float(u0) - ev['U0'][a, b]) < 1e-9, (game, arm, D, L.src(na), L.src(nb), float(u0), ev['U0'][a, b])
                assert abs(float(u1) - ev['U1'][b, a]) < 1e-9, (game, arm, D, L.src(na), L.src(nb))
                assert abs(float(ref.cost(0, na, nb, D)) - ev['E0'][a, b]) < 1e-9, (game, arm, D, L.src(na), L.src(nb))
                assert abs(float(ref.cost(1, nb, na, D)) - ev['E1'][b, a]) < 1e-9, (game, arm, D, L.src(na), L.src(nb))


def test_work_mode_at_least_depth():
    L, ev = built('insp', 'exact', 8, D=8)
    L2, evw = built('insp', 'exact', 8, D=8, workmode=1)
    assert (evw['E0'] >= ev['E0'] - 1e-12).all() and (evw['E1'] >= ev['E1'] - 1e-12).all()
    assert evw['E0'].max() > ev['E0'].max()


def spellings(game, n, arm='exact'):
    """independent raw spelling counts by size (a recurrence over sorts, no canonicalisation)."""
    card = game == 'end'
    A = {(r, t): [0] * (n + 1) for r in (0, 1) for t in (0, 1)}
    app = {r: [0] * (n + 1) for r in (0, 1)}
    for s in range(1, n + 1):
        for r in (0, 1):
            if s == 3:
                app[r][s] = 1
            elif s >= 4:
                app[r][s] = A[(r, r)][s - 3]
        for r in (0, 1):
            for t in (0, 1):
                c = 0
                if s == 1:
                    c += 3
                if s >= 2:
                    if arm == 'exact':
                        c += A[(r, 1 - t)][s - 1]
                    for i in range(1, s - 1):
                        c += A[(r, t)][i] * A[(r, t)][s - 1 - i]
                        if card and r == 0 and t == 0:
                            c += A[(r, t)][i] * A[(r, t)][s - 1 - i]
                    for q in range(3, s - 2):
                        for a in range(1, s - q - 1):
                            b = s - 1 - q - a
                            if b >= 1:
                                c += 2 * app[r][q] * A[(r, t)][a] * A[(r, t)][b]
                A[(r, t)][s] = c
        for r in (0, 1):
            A[(r, 1 - r)][s] += app[r][s]
    return A


def test_enumeration_multiplicities():
    for game, n in (('insp', 8), ('end', 7)):
        L = M.Lang2(game, 'exact', n)
        A = spellings(game, n)
        for r in (0, 1):
            for s in range(1, n + 1):
                assert L.a_size[r][s] == A[(r, r)][s], (game, r, s, L.a_size[r][s], A[(r, r)][s])
        for r in (0, 1):
            assert abs(L.mu[r].sum() - 1) < 1e-12
    # canonical counts
    assert M.Lang2('insp', 'exact', 8).S0 == 2150 and M.Lang2('end', 'exact', 7).S0 == 3938 and M.Lang2('end', 'exact', 7).S1 == 713


def test_matched_isomorphic_to_exact():
    """sr replaces cr node for node: same enumeration order, same multiplicities, hence the same prior spelling mass."""
    Le = M.Lang2('insp', 'exact', 8); Lm = M.Lang2('insp', 'matched', 8)
    assert Le.S == Lm.S and (Le.mult == Lm.mult).all() and (Le.size == Lm.size).all()
    assert np.abs(Le.mu[0] - Lm.mu[0]).max() < 1e-15
    cr_e = Le.has_cr[0]; sr_m = Lm.has_sr[0]
    assert (cr_e == sr_m).all()
    assert abs(Le.mu[0][cr_e].sum() - Lm.mu[0][sr_m].sum()) < 1e-15


def test_sr_equals_if_in_inspection():
    """a one-draw best response is the conditional program: sr(THEM(ME)) behaves as `if THEM(ME) = I then C else K` for the
    inspectee and as RI for the inspector, against every opposing program."""
    L, ev = built('insp', 'matched', 8)
    sr1 = M.prog_of(L, 1, ('sr', M.APPME)); rc = M.prog_of(L, 1, M.NAMED_INSP[1]['RC'])
    sr0 = M.prog_of(L, 0, ('sr', M.APPME)); ri = M.prog_of(L, 0, M.NAMED_INSP[0]['RI'])
    assert np.abs(ev['U1'][sr1] - ev['U1'][rc]).max() < TOL and np.abs(ev['U0'][:, sr1] - ev['U0'][:, rc]).max() < TOL
    assert np.abs(ev['U0'][sr0] - ev['U0'][ri]).max() < TOL


def test_srk_binomial_inspection():
    L, ev = built('insp', 'sr4', 8)
    s4 = M.prog_of(L, 1, ('srk', M.APPME))
    for nm, p in (('I', 1), ('N', 0), ('X', .5), ('P14', .25), ('P38', .375)):
        a = M.prog_of(L, 0, M.NAMED_INSP[0][nm])
        # comply iff the sampled inspection frequency exceeds 1/4 (ties by coin): P(comply)
        pm = lambda n: math.comb(4, n) * p ** n * (1 - p) ** (4 - n)
        comply = sum(pm(n) for n in range(5) if n / 4 > 0.25) + 0.5 * pm(1)
        assert abs(ev['G1'][s4, a][0] - comply) < TOL, nm


# ------------------------------------------------------------------ toy chain and lottery kernel
class Toy:
    pass


def toy_arm(UA, UB, m0, m1):
    A = Toy()
    A.UA, A.UB = np.array(UA, float), np.array(UB, float)
    A.mass = [np.array(m0, float), np.array(m1, float)]
    A.K = [A.UA.shape[0], A.UA.shape[1]]
    return A


def test_chain_matches_dense_solution():
    rng = np.random.default_rng(3)
    K0, K1 = 4, 3
    UA = rng.normal(size=(K0, K1)); UB = rng.normal(size=(K1, K0))
    m0 = rng.random(K0); m0 /= m0.sum(); m1 = rng.random(K1); m1 /= m1.sum()
    A = toy_arm(UA, UB, m0, m1)
    N = 50
    ch = M.TwoPopChain(A, N)
    ch.explore([0, 5], log_theta=-400.0, max_states=K0 * K1)
    n = len(ch.states)
    assert n == K0 * K1
    # dense continuous-time generator and linear solve
    Q = np.zeros((n, n))
    for s in ch.states:
        a, b = divmod(s, K1)
        for q in range(K0):
            if q != a:
                Q[s, q * K1 + b] += 0.5 * m0[q] * math.exp(float(M.lrho(np.array([UA[q, b] - UA[a, b]]), N)[0]))
        for q in range(K1):
            if q != b:
                Q[s, a * K1 + q] += 0.5 * m1[q] * math.exp(float(M.lrho(np.array([UB[q, a] - UB[b, a]]), N)[0]))
    G = Q - np.diag(Q.sum(1))
    Aeq = np.vstack([G.T, np.ones(n)]); beq = np.zeros(n + 1); beq[-1] = 1
    pi = np.linalg.lstsq(Aeq, beq, rcond=None)[0]
    got = np.exp(ch.lpi - np.logaddexp.reduce(ch.lpi))
    order = [ch.states.index(s) for s in range(n)]
    assert np.abs(got[order] - pi).max() < 1e-9


def test_full_chain_solver_matches_explored():
    rng = np.random.default_rng(11)
    K0, K1 = 5, 4
    A = toy_arm(rng.normal(size=(K0, K1)), rng.normal(size=(K1, K0)), np.full(K0, 1 / K0), np.full(K1, 1 / K1))
    for N in (20, 400):
        ch = M.TwoPopChain(A, N)
        ch.explore(list(range(K0 * K1)), log_theta=-400.0, max_states=K0 * K1)
        ref = np.exp(ch.lpi - np.logaddexp.reduce(ch.lpi))[np.argsort(ch.states)]
        ch2 = M.TwoPopChain(A, N)
        lp = ch2.solve_full()
        assert np.abs(np.exp(lp) - ref).max() < 1e-10


def test_weak_graph_classes_matching_pennies():
    UA = np.array([[1, -1], [-1, 1]]); UB = np.array([[-1, 1], [1, -1]])     # matching pennies
    lab, classes = M.weak_graph_classes(UA, UB)
    assert len(classes) == 1 and classes[0]['kind'] == 'cycle' and classes[0]['size'] == 4
    UA = np.array([[2, 0], [0, 1]]); UB = np.array([[2, 0], [0, 1]])         # coordination: two rest points
    lab, classes = M.weak_graph_classes(UA, UB)
    assert sorted(c['kind'] for c in classes) == ['rest', 'rest']
    UA = np.array([[1, 1], [0, 0]]); UB = np.array([[0, 0], [0, 0]])          # ties: a drift set
    lab, classes = M.weak_graph_classes(UA, UB)
    assert [c['kind'] for c in classes] == ['drift']


def test_lottery_kernel_dominance_and_determinism():
    # class 0 of role 0 earns more against every role-1 class and class 1 of role 1 earns more: both populations converge
    UA = np.array([[1.0, 1.0], [0.0, 0.0]]); UB = np.array([[0.0, 0.0], [1.0, 1.0]])
    init0 = np.array([[50, 50]] * 4); init1 = np.array([[50, 50]] * 4)
    cps = np.array([5, 300], np.int64)
    o0, o1 = M.lottery2(UA, UB, init0, init1, 100, 0.3, 0.0, 7, cps)
    assert (o0.sum(2) == 100).all() and (o1.sum(2) == 100).all()
    assert (o0[1, :, 0] == 100).all() and (o1[1, :, 1] == 100).all()
    o0b, o1b = M.lottery2(UA, UB, init0, init1, 100, 0.3, 0.0, 7, cps)
    assert (o0 == o0b).all() and (o1 == o1b).all()


def test_island_stats_one_hot_matches_tables():
    arms, _, L = M.build_arm('insp', 'exact', 8, prices=(0.0,))
    A = arms[0.0]
    ia = int(A.cls_of[0][M.prog_of(L, 0, M.NAMED_INSP[0]['P38'])]); ib = int(A.cls_of[1][M.prog_of(L, 1, 'c0')])
    X0 = np.zeros((1, A.K[0])); X1 = np.zeros((1, A.K[1])); X0[0, ia] = 1; X1[0, ib] = 1
    st = M.island_stats(A, X0, X1)
    assert abs(st['u0'][0] + 3 / 8) < 1e-9 and abs(st['u1'][0]) < 1e-9
    assert abs(st['p_insp'][0] - 3 / 8) < 1e-9 and abs(st['q_cheat'][0]) < 1e-9
    assert abs(st['m_p38'][0] - 1) < 1e-12 and abs(st['m_above'][0] - 1) < 1e-12
    assert abs(st['J'][0].sum() - 1) < 1e-9


def test_one_role_reads_ablation_arms():
    ee = M.Lang2('insp', 'exact_ee', 8); bl = M.Lang2('insp', 'blind', 8); ex = M.Lang2('insp', 'exact', 8)
    assert ee.S0 == bl.S0 and not ee.has_app[0].any() and not ee.has_cr[0].any()          # inspectors blind
    assert ee.S1 == ex.S1 and (ee.has_cr[1] == ex.has_cr[1]).all()                          # inspectees as in the exact arm
    er = M.Lang2('insp', 'exact_er', 8)
    assert er.S1 == bl.S1 and er.S0 == ex.S0
