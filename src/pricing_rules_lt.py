"""The L_T games (RPS and inspection) under the pricing rules: static ledger tables, priced views of the stored tables, and
the lotteries (exact-expectation kernel for F, A, F+A, B-warm, toll; sampled-encounter kernel with island ledgers for B-cold
and the matched bridges).  One cell per process:

    python3 src/pricing_rules_lt.py <game> <rule> <level> <cell> [--runs n] [--kernel exact|sampled]

game in {rps, insp}; rule in {Z (zero price), F, A, FA, B (cold cache, sampled), Bw (warm cache, exact), T (toll)}, and the
bridges Fs/As/FAs/Zs (same rule through the sampled kernel); level = c, P_fail or tau; cell in {primary, size}.
Rows: runs/pricing_rules/<game>_<rule>_<level>_<cell>.json.gz
"""
import copy
import gzip
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault('NUMBA_NUM_THREADS', '1')
import lt_tape as T
import lt_tape_games as G
import lt_tape_run as R
import rps as RP
import mixed2 as M2
import pricing_rules as P

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'runs', 'pricing_rules')
K0 = R.K0
CELLS = R.CELLS
CPS = R.CPS
RULES = ('Z', 'F', 'A', 'FA', 'B', 'Bw', 'Bws', 'Bo', 'Bl', 'T', 'Zs', 'Fs', 'As', 'FAs')
SAMPLED = ('B', 'Bws', 'Bo', 'Bl', 'Zs', 'Fs', 'As', 'FAs')
KEEP_KEYS = None            # all keys of the stored record are small enough once the island lists are dropped


# ----------------------------------------------------------------------------------------------------------------
# static ledger tables
# ----------------------------------------------------------------------------------------------------------------
class Base:
    """The stored tables of one game (c = 0) plus the instrumented ledger of every ordered pair of the catalogue."""

    def __init__(self, game, K=K0, arm='full'):
        self.game = game; self.K = K
        self.tb = R.Tables(game, arm, K, 0.0)
        tb = self.tb
        r = tb.r
        self.eng = P.LedgerEngine(tb.prover, K, r, 3)
        self.recs = {}
        if game == 'rps':
            terms = tb.terms[0]; n = len(terms)
            self.n = n
            self.arrays = self._arrays(terms, terms)
            self._check(terms, terms, tb.S, None)
        else:
            t0, t1 = tb.terms
            self.n0, self.n1 = len(t0), len(t1)
            self.arr0 = self._arrays(t0, t1)              # [inspector a, inspectee b]: the inspector's play
            arr1 = self._arrays(t1, t0)                  # [inspectee b, inspector a]: the inspectee's play
            self.arr1 = arr1
            self._check(t0, t1, tb.S0, tb.S1)

    def _arrays(self, xs, ys):
        nx, ny = len(xs), len(ys)
        keys = ('S', 'n_to', 'fa', 'ncall', 'root_own', 'n_top', 'fuel')
        out = {k: np.zeros((nx, ny)) for k in keys}
        for i, x in enumerate(xs):
            for j, y in enumerate(ys):
                rec = self.eng.ledger(x, y)
                ex = P.pair_expectations(rec, self.K)
                for k in keys: out[k][i, j] = ex[k]
        return out

    def _check(self, xs, ys, S_a, S_b):
        """The instrumented totals reproduce the stored engine's steps and distributions exactly."""
        tb = self.tb
        bad = 0
        for i, x in enumerate(xs):
            for j, y in enumerate(ys):
                d = tb.engine.dist(x, y); l = self.eng.ledger(x, y)
                if d['dist'] != l['dist'] or d['steps'] != l['steps'] or d['fuel'] != l['fuel']: bad += 1
                if S_b is not None:
                    d2 = tb.engine.dist(y, x); l2 = self.eng.ledger(y, x)
                    if d2['dist'] != l2['dist'] or d2['steps'] != l2['steps'] or d2['fuel'] != l2['fuel']: bad += 1
        self.mismatch = bad

    # charges ------------------------------------------------------------------------------------------------------
    @staticmethod
    def charge(arr, rule, level, K):
        """Expected charge matrix (same shape as the arrays) of a rule at a level.  Z: 0; F: c S; A: P n_to; FA: c fa;
        Bw (warm cache): c root_own; T: tau ncall."""
        if rule in ('Z', 'Zs'): return np.zeros_like(arr['S'])
        if rule in ('F', 'Fs'): return level * arr['S']
        if rule in ('A', 'As'): return level * arr['n_to']
        if rule in ('FA', 'FAs'): return level * arr['fa']
        if rule in ('Bw', 'Bws', 'B', 'Bo', 'Bl'): return level * arr['root_own']
        if rule == 'T': return level * arr['ncall']
        raise ValueError(rule)

    def view(self, rule, level):
        """A copy of the stored tables whose payoffs are net of the rule's charge (B in the sampled kernel is shown by its
        warm-cache steady state in the statistics tables: the net payoffs used for exploitability)."""
        tb = copy.copy(self.tb)
        eff = 'Bw' if rule in ('B', 'Bws', 'Bo', 'Bl') else rule
        if self.game == 'rps':
            ch = self.charge(self.arrays, eff, level, self.K)
            tb.U = tb.Ug - ch
            tb.CH = ch
        else:
            ch0 = self.charge(self.arr0, eff, level, self.K)
            ch1 = self.charge(self.arr1, eff, level, self.K)
            tb.UA = tb.UAg - ch0
            tb.UB = tb.UBg - ch1
            tb.CH0, tb.CH1 = ch0, ch1
        tb.rule, tb.level = rule, level
        return tb


def seed_label(rule, level):
    """The dynamics-seed price label: the stored one ('%g' of c) for F and Z, a rule tag otherwise."""
    if rule == 'Z': return '0'
    if rule == 'F': return '%g' % level
    return '%s@%g' % (rule, level)


def dyn_seed(tb, cell, run, label):
    return RP.run_seed('dynamics|%s|%s|%s|%s|%d|%s' % (cell, tb.game, tb.arm, label, tb.K, tb.renorm), run)


# ----------------------------------------------------------------------------------------------------------------
# lotteries (exact kernel)
# ----------------------------------------------------------------------------------------------------------------
def lottery_rps_exact(tb, cell, run, N, I, label, mN=1.0):
    init, = tb.founders(cell, run, N, I)
    idx = np.nonzero(init.sum(0) > 0)[0]
    init_l = np.ascontiguousarray(init[:, idx])
    Ul = np.ascontiguousarray(tb.U[np.ix_(idx, idx)])
    seed_d = dyn_seed(tb, cell, run, label)
    out, nalive, homo, nwin = RP.lottery_kernel(Ul, init_l, N, RP.W, mN / N, seed_d, CPS, 1500, 2000, 10)
    full = {}
    for ci, g in enumerate(CPS):
        f = np.zeros((I, len(tb.names[0])), np.int64); f[:, idx] = out[ci]; full[int(g)] = f
    return full, dict(nalive_window=float(np.mean(nalive / max(nwin, 1))), homo_window=float(np.mean(homo / max(nwin, 1))))


def lottery_insp_exact(tb, cell, run, N, I, label, mN=1.0):
    init0, init1 = tb.founders(cell, run, N, I)
    i0 = np.nonzero(init0.sum(0) > 0)[0]; i1 = np.nonzero(init1.sum(0) > 0)[0]
    UA = np.ascontiguousarray(tb.UA[np.ix_(i0, i1)]); UB = np.ascontiguousarray(tb.UB[np.ix_(i1, i0)])
    seed_d = dyn_seed(tb, cell, run, label)
    o0, o1 = M2.lottery2(UA, UB, np.ascontiguousarray(init0[:, i0]), np.ascontiguousarray(init1[:, i1]), N, M2.W, mN / N, seed_d, CPS)
    full = {}
    for ci, g in enumerate(CPS):
        f0 = np.zeros((I, len(tb.names[0])), np.int64); f0[:, i0] = o0[ci]
        f1 = np.zeros((I, len(tb.names[1])), np.int64); f1[:, i1] = o1[ci]
        full[int(g)] = (f0, f1)
    return full, {}


# ----------------------------------------------------------------------------------------------------------------
# extra statistics (timeouts, charges)
# ----------------------------------------------------------------------------------------------------------------
def extra_stats_rps(base, counts, N):
    X = counts / float(N)
    nto = np.einsum('ia,ab,ib->i', X, base.arrays['n_to'], X)
    ncall = np.einsum('ia,ab,ib->i', X, base.arrays['ncall'], X)
    sim = np.array([f == 'sim' for f in base.tb.fam[0]])
    return dict(to_play=nto, calls_play=ncall)


def extra_stats_insp(base, c0, c1, N):
    X0 = c0 / float(N); X1 = c1 / float(N)
    to0 = np.einsum('ia,ib,ab->i', X0, X1, base.arr0['n_to']); to1 = np.einsum('ib,ia,ba->i', X1, X0, base.arr1['n_to'])
    nc0 = np.einsum('ia,ib,ab->i', X0, X1, base.arr0['ncall']); nc1 = np.einsum('ib,ia,ba->i', X1, X0, base.arr1['ncall'])
    return dict(to0=to0, to1=to1, calls0=nc0, calls1=nc1, to_play=0.5 * (to0 + to1), calls_play=0.5 * (nc0 + nc1))


def make_record(base, tb, full, N, extra, named, run, wall, tag):
    """Island-mean statistics at generation 2,000 (and 4,000 where the kernel ran that far) plus the extra statistics."""
    gens = (2000, 4000) if 4000 in full else (2000,)
    rec = dict(run=run, wall=wall, tag=tag, **extra, stats={})
    if base.game == 'rps':
        for g in gens:
            st = R.rps_island_stats(full[g], N, tb, named[0])
            rec['stats'][str(g)] = {k: round(float(np.nanmean(v)), 6) for k, v in st.items()}
            ex = extra_stats_rps(base, full[g], N)
            rec['stats'][str(g)].update({k: round(float(np.mean(v)), 6) for k, v in ex.items()})
        s1 = R.support(full[1500], N); s2 = R.support(full[2000], N)
        rec['resolved'] = float(np.mean((s1 == s2).all(1)))
        for g in gens: rec['dom%d' % g] = full[g].argmax(1).tolist()
    else:
        for g in gens:
            c0, c1 = full[g]
            st = R.insp_island_stats(c0, c1, N, tb, named[0], named[1])
            rec['stats'][str(g)] = {k: (round(float(np.nanmean(v)), 6) if np.isfinite(v).any() else float('nan')) for k, v in st.items()}
            ex = extra_stats_insp(base, c0, c1, N)
            rec['stats'][str(g)].update({k: round(float(np.mean(v)), 6) for k, v in ex.items()})
        a = np.concatenate([R.support(full[1500][0], N), R.support(full[1500][1], N)], 1)
        b = np.concatenate([R.support(full[2000][0], N), R.support(full[2000][1], N)], 1)
        rec['resolved'] = float(np.mean((a == b).all(1)))
        for g in gens: rec['dom%d' % g] = [full[g][0].argmax(1).tolist(), full[g][1].argmax(1).tolist()]
    return rec


# ----------------------------------------------------------------------------------------------------------------
def cell_file(game, rule, level, cell, tag=None):
    return os.path.join(OUT, '%s_%s_%g_%s%s.json.gz' % (game, rule, level, cell, '' if tag is None else '_' + tag))


def run_cell(game, rule, level, cell, runs=None, base=None, first=0, tag=None):
    t0 = time.time()
    base = base or Base(game)
    tb = base.view(rule, level)
    named = R.named_idx(tb)
    cfg = CELLS[cell]
    N, I = cfg['N'], cfg['I']
    runs = runs if runs is not None else cfg['runs']
    label = seed_label(rule, level)
    name = '%s_%s_%g_%s' % (game, rule, level, cell)
    recs = []
    sampled = rule in SAMPLED
    if sampled:
        import pricing_rules_kern as KR
        sdata = KR.SampledData(base, rule, level)
    for r in range(first, first + runs):
        t1 = time.time()
        if sampled and rule in ('Bo', 'Bl'):
            import pricing_rules_kern_own as KO
            lab = label if rule == 'Bo' else seed_label('B', level)
            full, ex = KO.lottery_own(base, tb, sdata, rule, level, cell, r, N, I, lab)
        elif sampled:
            full, ex = KR.lottery_sampled(base, tb, sdata, rule, level, cell, r, N, I, label, warm=1 if rule == 'Bws' else 0)
        elif game == 'rps':
            full, ex = lottery_rps_exact(tb, cell, r, N, I, label)
        else:
            full, ex = lottery_insp_exact(tb, cell, r, N, I, label)
        recs.append(make_record(base, tb, full, N, ex, named, r, time.time() - t1, name))
        print('%s run %d wall %.1f' % (name, r, time.time() - t1), flush=True)
    os.makedirs(OUT, exist_ok=True)
    meta = dict(name=name, game=game, rule=rule, level=level, cell=cell, K=base.K, N=N, I=I, runs=runs, sampled=sampled,
                names=tb.names, fam=[f.tolist() for f in tb.fam], mismatch=base.mismatch, t_total=time.time() - t0,
                engine_stats=dict(base.tb.engine_stats))
    with gzip.open(cell_file(game, rule, level, cell, tag) + '.tmp', 'wt') as f:
        json.dump(dict(meta=meta, recs=recs), f)
    os.replace(cell_file(game, rule, level, cell, tag) + '.tmp', cell_file(game, rule, level, cell, tag))
    return name


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('game'); ap.add_argument('rule'); ap.add_argument('level', type=float); ap.add_argument('cell')
    ap.add_argument('--runs', type=int, default=None); ap.add_argument('--first', type=int, default=0); ap.add_argument('--tag', default=None)
    a = ap.parse_args()
    run_cell(a.game, a.rule, a.level, a.cell, a.runs, None, a.first, a.tag)
