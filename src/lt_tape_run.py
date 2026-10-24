"""Tables, island statistics and lotteries for the private-tape experiment (run one cell per process).

    python3 src/lt_tape_run.py <game> <arm> <c> <cell> [K] [renorm] [m]

game in {rps, insp}; arm in the arms of lt_tape_games; c in {0, c0} given as '0' or 'c0' (or a float); cell in CELLS.
Output: runs/lt_tape/<game>_<arm>_c<c>_<cell>[_K<K>][_renorm][_m4].json (island-mean statistics at the checkpoints per run).
"""
import gzip
import json
import math
import os
import sys
import time

import numpy as np
from numba import njit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault('NUMBA_NUM_THREADS', '1')
import lt_tape as T
import lt_tape_games as G
import rps as RP
import mixed2 as M2

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'runs', 'lt_tape')
K0 = 10000                       # fuel cap (notes/lt-tape.md section 2.1)
C0 = 0.12 / K0                   # price calibrated so that exhausting K0 costs 0.12
CELLS = {
    'primary': dict(N=100, I=64, runs=40),
    'size': dict(N=400, I=16, runs=20),
}
CPS = np.array([500, 1000, 1500, 2000, 4000], np.int64)
UNI4 = np.array([1 / 3, 1 / 3, 1 / 3, 0.0])


# ----------------------------------------------------------------------------------------------------------------
class Tables:
    """Everything static about one (game, arm, K, c, renorm, m) cell."""

    def __init__(self, game, arm, K, c, renorm=False, m=3, seed_prover=None):
        self.game, self.arm, self.K, self.c, self.renorm, self.m = game, arm, K, c, renorm, m
        r = 3 if game == 'rps' else 2
        self.r = r
        if game == 'rps':
            tpls = G.catalogue_rps(K, m)
        else:
            tpls = list(G.catalogue_insp(K, m))
        self.tpls = tpls
        self.names = [[t.name for t in lst] for lst in tpls]
        full_terms, _ = G.arm_terms(game, tpls, 'full')
        self.sizes = [np.array([T.size(x) for x in lst]) for lst in full_terms]
        terms, keep = G.arm_terms(game, tpls, arm, renorm)
        self.terms = terms
        self.keep = [np.array(k, bool) for k in keep]
        self.disabled = [np.array([G.arm_disabled(game, arm, t) for t in lst]) for lst in tpls]
        self.fam = [np.array([('const' if self.disabled[ro][i] else t.family) for i, t in enumerate(lst)])
                    for ro, lst in enumerate(tpls)]
        self.prover = T.TProver(r, limit=3 * max(K, 2 * K0))
        self.engine = T.Engine(self.prover, K=K, r=r, m=m)
        t0 = time.time()
        if game == 'rps':
            self.Gt, self.S, self.RT, self.FU = G.rps_tables(terms[0], self.engine)
            self.Ug, self.U = G.rps_payoffs(self.Gt, self.S, c)
        else:
            (self.G0, self.G1, self.S0, self.S1, self.RT0, self.RT1, self.FU0, self.FU1) = G.insp_tables(terms[0], terms[1], self.engine)
            self.UAg, self.UBg, self.UA, self.UB = G.insp_payoffs(self.G0, self.G1, self.S0, self.S1, c)
        self.t_tables = time.time() - t0
        self.engine_stats = dict(self.engine.stats); self.n_searches = len(self.prover.cache)

    # prior --------------------------------------------------------------------------------------------------------
    def founders(self, cell, run, N, I):
        """Founder counts per role (paired across arms: the sizes are the full arm's; a renormalized arm draws from its own mask)."""
        out = []
        for ro in range(len(self.tpls)):
            seed = RP.run_seed('founders|%s|%d' % (cell, ro), run)
            out.append(G.draw_founders(self.sizes[ro], self.keep[ro], I, N, seed))
        return out


# ----------------------------------------------------------------------------------------------------------------
def rps_island_stats(counts, N, tb, named):
    X = counts / float(N)
    Dpop = np.einsum('ib,xbk->ixk', X, tb.Gt)
    Q = np.einsum('ix,ixk->ik', X, Dpop)
    tv = 0.5 * np.abs(Dpop - UNI4).sum(-1)
    mix = (X * (tv <= 0.05)).sum(1)
    UxN = X @ tb.U.T; UxG = X @ tb.Ug.T
    ex = tb.keep[0]
    e_prog = np.where(ex[None, :], UxN, -1e9).max(1)
    e_gross = np.where(ex[None, :], UxG, -1e9).max(1)
    best_ind = np.where(ex[:, None], tb.U, -1e9).max(0)
    best_ind_g = np.where(ex[:, None], tb.Ug, -1e9).max(0)
    e_indiv = (X * best_ind[None, :]).sum(1); e_indiv_g = (X * best_ind_g[None, :]).sum(1)
    fam = tb.fam[0]
    out = dict(forfeit=Q[:, 3], mix=mix, e_prog=e_prog, e_gross=e_gross, e_indiv=e_indiv, e_indiv_g=e_indiv_g,
               net_payoff=np.einsum('ia,ab,ib->i', X, tb.U, X), cost=np.einsum('ia,ab,ib->i', X, tb.Ug - tb.U, X),
               homo=(X ** 2).sum(1), nclass=(counts > 0).sum(1).astype(float), steps=np.einsum('ia,ab,ib->i', X, tb.S, X))
    for f in G.FAMILIES:
        out['fam_' + f] = X[:, fam == f].sum(1)
    out['fam_disabled'] = X[:, tb.disabled[0]].sum(1)
    for k, i in named.items():
        out['sh_' + k] = X[:, i]
    mixers = np.array([n in ('U',) or n.startswith('B_') or n.startswith('CB_') for n in tb.names[0]]) & ~tb.disabled[0]
    out['tape_mixers'] = X[:, mixers].sum(1)
    out['freqR'] = Q[:, 0]; out['freqP'] = Q[:, 1]; out['freqS'] = Q[:, 2]
    return out


def _div(a, b):
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(b > 1e-12, a / np.maximum(b, 1e-300), np.nan)


def insp_island_stats(c0, c1, N, tb, named0, named1):
    X0 = c0 / float(N); X1 = c1 / float(N)
    out = {}
    UAx = X1 @ tb.UA.T; UBx = X0 @ tb.UB.T
    UAgx = X1 @ tb.UAg.T; UBgx = X0 @ tb.UBg.T
    out['u0g'] = (X0 * UAgx).sum(1); out['u1g'] = (X1 * UBgx).sum(1)
    out['u0'] = (X0 * UAx).sum(1); out['u1'] = (X1 * UBx).sum(1)
    k0, k1 = tb.keep
    out['e0'] = np.where(k0[None, :], UAx, -1e9).max(1); out['e1'] = np.where(k1[None, :], UBx, -1e9).max(1)
    d0 = X1 @ (1 - tb.G0[:, :, 2]).T; d1 = X0 @ (1 - tb.G1[:, :, 2]).T
    p0 = _div(X1 @ tb.G0[:, :, 0].T, d0); q1 = _div(X0 @ tb.G1[:, :, 1].T, d1)
    w0 = np.where(np.isnan(p0), 0.0, X0); w1 = np.where(np.isnan(q1), 0.0, X1)
    out['p_insp'] = _div((w0 * np.nan_to_num(p0)).sum(1), w0.sum(1)); out['q_cheat'] = _div((w1 * np.nan_to_num(q1)).sum(1), w1.sum(1))
    p0n = np.nan_to_num(p0, nan=0.5); q1n = np.nan_to_num(q1, nan=0.5)
    out['mix0'] = (X0 * ((p0n > 0.02) & (p0n < 0.98))).sum(1); out['mix1'] = (X1 * ((q1n > 0.02) & (q1n < 0.98))).sum(1)
    out['m_above'] = (X0 * (p0n > 0.25 + 5e-3)).sum(1); out['m_at'] = (X0 * (np.abs(p0n - 0.25) <= 5e-3)).sum(1)
    out['m_below'] = (X0 * (p0n < 0.25 - 5e-3)).sum(1)
    out['q_comply'] = (X1 * (q1n <= 0.02)).sum(1); out['q_cheater'] = (X1 * (q1n >= 0.98)).sum(1)
    pn = np.nan_to_num(out['p_insp'], nan=0.5); qn = np.nan_to_num(out['q_cheat'], nan=0.5)
    out['isl_efficient'] = ((out['u0g'] >= -0.05) & (out['u1g'] >= -0.05)).astype(float)
    out['isl_commit_comply'] = ((pn > 0.25 + 5e-3) & (qn < 0.1)).astype(float)
    out['isl_commit'] = (pn > 0.25 + 5e-3).astype(float)
    out['f0'] = (X0 * (X1 @ tb.FU0.T)).sum(1); out['f1'] = (X1 * (X0 @ tb.FU1.T)).sum(1)
    out['forfeit0'] = (X0 * (X1 @ tb.G0[:, :, 2].T)).sum(1); out['forfeit1'] = (X1 * (X0 @ tb.G1[:, :, 2].T)).sum(1)
    out['homo0'] = (X0 ** 2).sum(1); out['homo1'] = (X1 ** 2).sum(1)
    out['nclass0'] = (c0 > 0).sum(1).astype(float); out['nclass1'] = (c1 > 0).sum(1).astype(float)
    for ro, X in ((0, X0), (1, X1)):
        fam = tb.fam[ro]
        for f in G.FAMILIES:
            out['fam%d_%s' % (ro, f)] = X[:, fam == f].sum(1)
        out['fam%d_disabled' % ro] = X[:, tb.disabled[ro]].sum(1)
    for k, i in named0.items(): out['sh0_' + k] = X0[:, i]
    for k, i in named1.items(): out['sh1_' + k] = X1[:, i]
    # route steps (population-weighted mean steps per encounter) and encounter weights where the route is used
    for ri, rn in enumerate(T.ROUTES):
        out['rs0_' + rn] = np.einsum('ia,ib,ab->i', X0, X1, tb.RT0[:, :, ri])
        out['rs1_' + rn] = np.einsum('ib,ia,ba->i', X1, X0, tb.RT1[:, :, ri])
        out['ru0_' + rn] = np.einsum('ia,ib,ab->i', X0, X1, (tb.RT0[:, :, ri] > 0).astype(float))
        out['ru1_' + rn] = np.einsum('ib,ia,ba->i', X1, X0, (tb.RT1[:, :, ri] > 0).astype(float))
    out['steps0'] = np.einsum('ia,ib,ab->i', X0, X1, tb.S0); out['steps1'] = np.einsum('ib,ia,ba->i', X1, X0, tb.S1)
    # shares by route among the readers of the arm
    names0, names1 = tb.names
    cm0 = np.array([n.startswith('CARR') for n in names0]) & ~tb.disabled[0]
    out['carrier_share0'] = X0[:, cm0].sum(1)
    com = (np.array([n.startswith('CARR') or n.startswith('M') for n in names0]) & ~tb.disabled[0]) & (
        np.array([tb.tpls[0][i].meta.get('p', 0) > 0.25 for i in range(len(names0))]))
    out['committed_mass'] = X0[:, com].sum(1)
    out['committed_carrier_mass'] = X0[:, com & cm0].sum(1)
    return out


def named_idx(tb):
    n0 = tb.names[0]
    if tb.game == 'rps':
        return {k: n0.index(k) for k in ('U', 'SIM20R', 'SIM100R', 'SIM100u', 'PB', 'PRR', 'CRR', 'R0', 'P0', 'S0', 'H0', 'H1', 'H2')}, None
    n1 = tb.names[1]
    return ({k: n0.index(k) for k in ('I0', 'N0', 'RI', 'RIM', 'M4', 'CARR3', 'M3', 'M2', 'CARR2', 'M5', 'CARR4', 'SI100n', 'HI0')},
            {k: n1.index(k) for k in ('C0', 'K0', 'PR3', 'CR3', 'PCR3', 'PE', 'PEC', 'PR2', 'PR4', 'CR2', 'CR4', 'SE100k', 'Mc4')})


def support(counts, N, thr=0.05):
    return (counts / float(N)) >= thr


# ----------------------------------------------------------------------------------------------------------------
def lottery_rps(tb, cell, run, N, I, mN=1.0):
    init, = tb.founders(cell, run, N, I)
    idx = np.nonzero(init.sum(0) > 0)[0]
    init_l = np.ascontiguousarray(init[:, idx])
    Ul = np.ascontiguousarray(tb.U[np.ix_(idx, idx)])
    seed_d = RP.run_seed('dynamics|%s|%s|%s|%g|%d|%s' % (cell, tb.game, tb.arm, tb.c, tb.K, tb.renorm), run)
    out, nalive, homo, nwin = RP.lottery_kernel(Ul, init_l, N, RP.W, mN / N, seed_d, CPS, 1500, 2000, 10)
    full = {}
    for ci, g in enumerate(CPS):
        f = np.zeros((I, len(tb.names[0])), np.int64); f[:, idx] = out[ci]; full[int(g)] = f
    return full, dict(nalive_window=float(np.mean(nalive / max(nwin, 1))), homo_window=float(np.mean(homo / max(nwin, 1))))


def lottery_insp(tb, cell, run, N, I, mN=1.0):
    init0, init1 = tb.founders(cell, run, N, I)
    i0 = np.nonzero(init0.sum(0) > 0)[0]; i1 = np.nonzero(init1.sum(0) > 0)[0]
    UA = np.ascontiguousarray(tb.UA[np.ix_(i0, i1)]); UB = np.ascontiguousarray(tb.UB[np.ix_(i1, i0)])
    seed_d = RP.run_seed('dynamics|%s|%s|%s|%g|%d|%s' % (cell, tb.game, tb.arm, tb.c, tb.K, tb.renorm), run)
    o0, o1 = M2.lottery2(UA, UB, np.ascontiguousarray(init0[:, i0]), np.ascontiguousarray(init1[:, i1]), N, M2.W, mN / N, seed_d, CPS)
    full = {}
    for ci, g in enumerate(CPS):
        f0 = np.zeros((I, len(tb.names[0])), np.int64); f0[:, i0] = o0[ci]
        f1 = np.zeros((I, len(tb.names[1])), np.int64); f1[:, i1] = o1[ci]
        full[int(g)] = (f0, f1)
    return full, {}


@njit(cache=True)
def _cum_pick(cum, u):
    lo = 0; hi = len(cum) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if cum[mid] > u: hi = mid
        else: lo = mid + 1
    return lo


@njit(cache=True)
def lottery2_sampled(G0, G1, V0, V1, S0, S1, c, init0, init1, N, w, m, seed, cps, nenc):
    """eps = 0 islands, two populations per island, SAMPLED encounters: each generation every individual plays nenc encounters
    against uniformly drawn members of the other population of its island (realized actions drawn from the exact class-level
    distributions G0 (n0, n1, 3), G1 (n1, n0, 3); payoff = game payoff of the realized profile minus c times the expected steps);
    then 2 I N replacement events with parent probability proportional to exp(w * the individual's sampled mean payoff) (migration
    with probability m from a uniformly chosen other island), victims uniform.  Individual-level state."""
    np.random.seed(seed)
    I, n0 = init0.shape
    n1 = init1.shape[1]
    cls0 = np.zeros((I, N), np.int64); cls1 = np.zeros((I, N), np.int64)
    for i in range(I):
        k = 0
        for a in range(n0):
            for t in range(init0[i, a]):
                cls0[i, k] = a; k += 1
        k = 0
        for b in range(n1):
            for t in range(init1[i, b]):
                cls1[i, k] = b; k += 1
    fit0 = np.zeros((I, N)); fit1 = np.zeros((I, N))
    out0 = np.zeros((len(cps), I, n0), np.int64); out1 = np.zeros((len(cps), I, n1), np.int64)
    ci = 0
    gens = cps[len(cps) - 1]
    cum = np.zeros(N)
    for g in range(gens):
        for i in range(I):
            for j in range(N):
                s = 0.0
                for e in range(nenc):
                    o = np.random.randint(N)
                    a = cls0[i, j]; b = cls1[i, o]
                    u = np.random.random(); x = 0
                    acc = G0[a, b, 0]
                    if u >= acc:
                        acc += G0[a, b, 1]; x = 1
                        if u >= acc: x = 2
                    u = np.random.random(); y = 0
                    acc = G1[b, a, 0]
                    if u >= acc:
                        acc += G1[b, a, 1]; y = 1
                        if u >= acc: y = 2
                    s += V0[x, y] - c * S0[a, b]
                fit0[i, j] = s / nenc
            for j in range(N):
                s = 0.0
                for e in range(nenc):
                    o = np.random.randint(N)
                    b = cls1[i, j]; a = cls0[i, o]
                    u = np.random.random(); x = 0
                    acc = G0[a, b, 0]
                    if u >= acc:
                        acc += G0[a, b, 1]; x = 1
                        if u >= acc: x = 2
                    u = np.random.random(); y = 0
                    acc = G1[b, a, 0]
                    if u >= acc:
                        acc += G1[b, a, 1]; y = 1
                        if u >= acc: y = 2
                    s += V1[x, y] - c * S1[b, a]
                fit1[i, j] = s / nenc
        for e in range(2 * I * N):
            i = np.random.randint(I); p = np.random.randint(2)
            src = i
            if m > 0.0 and np.random.random() < m:
                src = np.random.randint(I - 1)
                if src >= i: src += 1
            mx = -1e300
            for j in range(N):
                f = fit0[src, j] if p == 0 else fit1[src, j]
                if f > mx: mx = f
            tot = 0.0
            for j in range(N):
                f = fit0[src, j] if p == 0 else fit1[src, j]
                tot += np.exp(w * (f - mx)); cum[j] = tot
            par = _cum_pick(cum, np.random.random() * tot)
            vic = np.random.randint(N)
            if p == 0:
                cls0[i, vic] = cls0[src, par]; fit0[i, vic] = fit0[src, par]
            else:
                cls1[i, vic] = cls1[src, par]; fit1[i, vic] = fit1[src, par]
        gg = g + 1
        while ci < len(cps) and gg == cps[ci]:
            for i in range(I):
                for j in range(N):
                    out0[ci, i, cls0[i, j]] += 1; out1[ci, i, cls1[i, j]] += 1
            ci += 1
    return out0, out1


def lottery_insp_sampled(tb, cell, run, N, I, mN=1.0, nenc=10):
    init0, init1 = tb.founders(cell, run, N, I)
    i0 = np.nonzero(init0.sum(0) > 0)[0]; i1 = np.nonzero(init1.sum(0) > 0)[0]
    V0, V1 = G.insp_payoff_tensors()
    G0 = np.ascontiguousarray(tb.G0[np.ix_(i0, i1)]); G1 = np.ascontiguousarray(tb.G1[np.ix_(i1, i0)])
    S0 = np.ascontiguousarray(tb.S0[np.ix_(i0, i1)]); S1 = np.ascontiguousarray(tb.S1[np.ix_(i1, i0)])
    seed_d = RP.run_seed('sampled|%s|%s|%g|%d' % (cell, tb.arm, tb.c, tb.K), run)
    o0, o1 = lottery2_sampled(G0, G1, V0, V1, S0, S1, float(tb.c), np.ascontiguousarray(init0[:, i0]), np.ascontiguousarray(init1[:, i1]),
                              N, M2.W, mN / N, seed_d, CPS, nenc)
    full = {}
    for ci, g in enumerate(CPS):
        f0 = np.zeros((I, len(tb.names[0])), np.int64); f0[:, i0] = o0[ci]
        f1 = np.zeros((I, len(tb.names[1])), np.int64); f1[:, i1] = o1[ci]
        full[int(g)] = (f0, f1)
    return full, {}


# ----------------------------------------------------------------------------------------------------------------
def record(tb, full, N, extra, named, run, wall, tag):
    rec = dict(run=run, wall=wall, tag=tag, **extra, stats={})
    if tb.game == 'rps':
        for g in (2000, 4000):
            st = rps_island_stats(full[g], N, tb, named[0])
            rec['stats'][str(g)] = {k: round(float(np.nanmean(v)), 6) for k, v in st.items()}
        s1 = support(full[1500], N); s2 = support(full[2000], N)
        rec['resolved'] = float(np.mean((s1 == s2).all(1)))
        rec['dom2000'] = full[2000].argmax(1).tolist(); rec['dom4000'] = full[4000].argmax(1).tolist()
        # island-level category flags at 2000 and 4000 for the verdict statistics
        for g in (2000, 4000):
            st = rps_island_stats(full[g], N, tb, named[0])
            rec['isl%d' % g] = {k: np.round(v, 5).tolist() for k, v in st.items() if k in ('e_prog', 'e_indiv', 'forfeit', 'mix', 'fam_mixer', 'tape_mixers', 'sh_U')}
    else:
        for g in (2000, 4000):
            c0, c1 = full[g]
            st = insp_island_stats(c0, c1, N, tb, named[0], named[1])
            rec['stats'][str(g)] = {k: (round(float(np.nanmean(v)), 6) if np.isfinite(v).any() else float('nan')) for k, v in st.items()}
        a = np.concatenate([support(full[1500][0], N), support(full[1500][1], N)], 1)
        b = np.concatenate([support(full[2000][0], N), support(full[2000][1], N)], 1)
        rec['resolved'] = float(np.mean((a == b).all(1)))
        rec['dom2000'] = [full[2000][0].argmax(1).tolist(), full[2000][1].argmax(1).tolist()]
        rec['dom4000'] = [full[4000][0].argmax(1).tolist(), full[4000][1].argmax(1).tolist()]
        for g in (2000, 4000):
            st = insp_island_stats(full[g][0], full[g][1], N, tb, named[0], named[1])
            rec['isl%d' % g] = {k: np.round(np.nan_to_num(v, nan=-9.0), 5).tolist() for k, v in st.items()
                                if k in ('u0g', 'u1g', 'isl_efficient', 'isl_commit_comply', 'p_insp', 'q_cheat', 'e0', 'e1', 'sh0_RI', 'sh0_RIM',
                                         'sh1_C0', 'fam0_sim', 'fam0_prover', 'fam0_rim', 'carrier_share0', 'committed_mass',
                                         'committed_carrier_mass', 'm_above', 'fam1_enum', 'fam1_check', 'fam1_pcr', 'fam1_prover')}
    return rec


def cell_name(game, arm, c, cell, K, renorm, m, sampled=False):
    cs = 'cprice' if abs(c - C0) < 1e-12 else ('cfree' if c == 0 else 'c%g' % c)
    return '%s_%s_%s_%s%s%s%s%s' % (game, arm, cs, cell, '' if K == K0 else '_K%d' % K, '_renorm' if renorm else '',
                                   '_m%d' % m if m != 3 else '', '_sampled' if sampled else '')


def run_cell(game, arm, c, cell, K=K0, renorm=False, m=3, runs=None, sampled=False, nenc=10):
    tb = Tables(game, arm, K, c, renorm, m)
    named = named_idx(tb)
    cfg = CELLS[cell]
    N, I = cfg['N'], cfg['I']
    runs = runs if runs is not None else cfg['runs']
    name = cell_name(game, arm, c, cell, K, renorm, m, sampled)
    recs = []
    for r in range(runs):
        t0 = time.time()
        if game == 'rps': full, ex = lottery_rps(tb, cell, r, N, I)
        elif sampled: full, ex = lottery_insp_sampled(tb, cell, r, N, I, nenc=nenc)
        else: full, ex = lottery_insp(tb, cell, r, N, I)
        recs.append(record(tb, full, N, ex, named, r, time.time() - t0, name))
        print('%s run %d wall %.1f' % (name, r, time.time() - t0), flush=True)
    os.makedirs(OUT, exist_ok=True)
    meta = dict(name=name, game=game, arm=arm, c=c, K=K, renorm=renorm, m=m, N=N, I=I, runs=runs, sampled=sampled,
                names=tb.names, sizes=[s.tolist() for s in tb.sizes], disabled=[d.tolist() for d in tb.disabled],
                prior=[G.prior_masses(tb.sizes[ro], tb.keep[ro]).tolist() for ro in range(len(tb.sizes))],
                engine_stats=tb.engine_stats, searches=tb.n_searches, t_tables=tb.t_tables)
    with gzip.open(os.path.join(OUT, name + '.json.gz'), 'wt') as f:
        json.dump(dict(meta=meta, recs=recs), f)
    return name


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('game'); ap.add_argument('arm'); ap.add_argument('c'); ap.add_argument('cell')
    ap.add_argument('--K', type=int, default=K0); ap.add_argument('--renorm', action='store_true')
    ap.add_argument('--m', type=int, default=3); ap.add_argument('--runs', type=int, default=None)
    ap.add_argument('--sampled', action='store_true')
    a = ap.parse_args()
    c = C0 if a.c == 'c0' else float(a.c)
    run_cell(a.game, a.arm, c, a.cell, a.K, a.renorm, a.m, a.runs, a.sampled)
