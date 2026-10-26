"""Forfeit pricing: payoffs under the three forfeit conventions, arms, statistics, and the cell runner (notes/forfeit-pricing.md).

    python3 src/forfeit_pricing_run.py lt <game> <spec> [<spec> ...]       specs 'RULE[+X|+S]@LEVEL' (RULE in A, Af, Am), one process
    python3 src/forfeit_pricing_run.py build <game>                        build and cache the numeric tables

Imports src/forfeit_pricing.py (engine, tables) and the merged pricing and confirmation code; edits none of it.
Fresh run indices only (L_T runs 300-339).  LOTTERY objects at fixed geometry, never pi.
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
import lt_tape_games as G
import lt_tape_run as R
import rps as RP
import pricing_rules_lt as PL
import failure_pricing_confirm as F
import forfeit_pricing as FP
from forfeit_pricing import BaseX, TWINS, OUT, FRESH_LT


# ----------------------------------------------------------------------------------------------------------------
# game payoffs under the forfeit conventions
# ----------------------------------------------------------------------------------------------------------------
def rps_u4(mode):
    """4x4 payoff of (R, P, S, forfeit): 'stored' (a forfeiter loses 1 against any action, the opponent gains 1, both forfeit 0) or
    'm' (the forfeiter is a uniform draw: expectation 0 against anything, the opponent gains nothing)."""
    u = np.zeros((4, 4))
    for a, na in enumerate('RPS'):
        for b, nb in enumerate('RPS'):
            u[a, b] = G.RPS.u(na, nb)
    if mode == 'stored':
        for a in range(3):
            u[a, 3] = 1.0; u[3, a] = -1.0
    return u


def rps_game_payoffs(Gt, mode):
    return np.einsum('xya,yxb,ab->xy', Gt, Gt, rps_u4(mode))


def insp_V(mode):
    """(V0, V1) over x in (I, N, forfeit), y in (C, K, forfeit).  'stored': the stored convention (a forfeiter plays its worst action
    against the realized one).  'm': a forfeiting inspector plays I and a forfeiting inspectee plays C (their pure security
    actions); both forfeit: (I, C)."""
    V0, V1 = G.insp_payoff_tensors()
    if mode == 'stored': return V0, V1
    P0, P1 = G.INSP.P0, G.INSP.P1
    V0 = V0.copy(); V1 = V1.copy()
    for y in range(2):
        V0[2, y] = P0[0, y]; V1[2, y] = P1[0, y]
    for x in range(2):
        V0[x, 2] = P0[x, 0]; V1[x, 2] = P1[x, 0]
    V0[2, 2] = P0[0, 0]; V1[2, 2] = P1[0, 0]
    return V0, V1


def insp_game_payoffs(G0, G1, mode):
    V0, V1 = insp_V(mode)
    UAg = np.einsum('abx,bay,xy->ab', G0, G1, V0)
    UBg = np.einsum('abx,bay,xy->ba', G0, G1, V1)
    return UAg, UBg


def parse_spec(s):
    """'Af+X@0.1' -> (rule, arm, level)."""
    head, lv = s.split('@')
    rule, arm = head, 'none'
    if '+' in head:
        rule, a = head.split('+'); arm = {'X': 'X', 'S': 'sham'}[a]
    assert rule in ('A', 'Af', 'Am')
    return rule, arm, float(lv)


def spec_name(game, rule, arm, level, cell='primary'):
    return '%s_%s%s_%g_%s' % (game, rule, {'none': '', 'X': '+X', 'sham': '+S'}[arm], level, cell)


def seed_label(rule, arm, level):
    return '%s@%g%s' % (rule, level, {'none': '', 'X': '+X', 'sham': '+S'}[arm])


def founders_arm(base, game, cell, run, N, I, arm):
    """Standard founders of the merged catalogue (price- and rule-independent, so every arm and rule of a run starts from the same
    draw), padded to the extended catalogue; under 'X' / 'sham' each founder of a counterpart template becomes its twin with
    probability 1/2 (an independent fair coin per founder)."""
    tb = base.tb
    out = []
    for ro in range(len(tb.names)):
        nb = base.n_base[ro]
        seed = RP.run_seed('founders|%s|%d' % (cell, ro), run)
        ib = G.draw_founders(tb.sizes[ro][:nb], np.ones(nb, bool), I, N, seed)
        init = np.zeros((I, len(tb.names[ro])), np.int64)
        init[:, :nb] = ib
        if arm != 'none':
            for (r_, cp, xn, sn) in TWINS[game]:
                if r_ != ro: continue
                ci = tb.names[ro].index(cp); ti = tb.names[ro].index(xn if arm == 'X' else sn)
                rng = np.random.default_rng(RP.run_seed('xsplit|%s|%d|%s' % (cell, ro, cp), run))
                moved = rng.binomial(init[:, ci], 0.5)
                init[:, ci] -= moved; init[:, ti] += moved
        out.append(init)
    return out


def arm_keep(base, game, arm):
    tb = base.tb
    keeps = []
    for ro in range(len(tb.names)):
        k = np.zeros(len(tb.names[ro]), bool); k[:base.n_base[ro]] = True
        for (r_, cp, xn, sn) in TWINS[game]:
            if r_ != ro: continue
            if arm == 'X': k[tb.names[ro].index(xn)] = True
            if arm == 'sham': k[tb.names[ro].index(sn)] = True
        keeps.append(k)
    return keeps


def make_view(base, rule, level, arm, no_forfeit=False):
    """A copy of the tables whose payoffs are those of the rule at the level for the arm: game payoffs (stored forfeit convention
    or the security replacement) minus the rule's expected charge; the exploiter set (keep) restricted to the programmes of the arm;
    founders drawn by `founders_arm`.  no_forfeit zeroes the forfeit term of the charge (the validation of A_f against A)."""
    tb = copy.copy(base.tb)
    game = base.game
    tb.keep = arm_keep(base, game, arm)
    tb.rule, tb.level, tb.arm_tag = rule, level, arm
    mode = 'm' if rule == 'Am' else 'stored'
    if game == 'rps':
        a = base.arrays
        ev = a['ev_A'] if (rule == 'A' or no_forfeit) else a['ev_Af']
        ch = level * ev
        tb.Ug = rps_game_payoffs(tb.Gt, mode)
        tb.U = tb.Ug - ch
        tb.CH = ch
        u3 = rps_u4('stored')[:3, :3]
        Gt = tb.Gt
        tb.NUM = np.einsum('xya,yxb,ab->xy', Gt[:, :, :3], Gt[:, :, :3], u3)
        tb.DEN = Gt[:, :, :3].sum(-1) * Gt[:, :, :3].sum(-1).T
    else:
        a0, a1 = base.arr0, base.arr1
        e0 = a0['ev_A'] if (rule == 'A' or no_forfeit) else a0['ev_Af']
        e1 = a1['ev_A'] if (rule == 'A' or no_forfeit) else a1['ev_Af']
        tb.CH0, tb.CH1 = level * e0, level * e1
        tb.UAg, tb.UBg = insp_game_payoffs(tb.G0, tb.G1, mode)
        tb.UA, tb.UB = tb.UAg - tb.CH0, tb.UBg - tb.CH1
    tb.founders = lambda cell, run, N, I: founders_arm(base, game, cell, run, N, I, arm)
    return tb


# ----------------------------------------------------------------------------------------------------------------
# statistics
# ----------------------------------------------------------------------------------------------------------------
def e_comp_islands(tb, counts, N):
    """Exploitability on completed plays: for each exploiter x of the arm, sum_y X_y NUM[x, y] / sum_y X_y DEN[x, y] (undefined where
    no completed play), maximum over the defined exploiters; NaN on an island with none (never zero)."""
    X = counts / float(N)
    num = X @ tb.NUM.T; den = X @ tb.DEN.T
    ok = (den > 1e-12) & tb.keep[0][None, :]
    val = np.where(ok, num / np.where(ok, den, 1.0), -np.inf)
    m = val.max(1)
    return np.where(ok.any(1), m, np.nan)


def _nm(x):
    x = np.asarray(x, float)
    return float(np.nanmean(x)) if np.isfinite(x).any() else float('nan')


def rps_record(base, tb, full, N, I, run, wall, tag):
    names = tb.names[0]
    named, _ = R.named_idx(tb)
    idx = {n: i for i, n in enumerate(names)}
    a = base.arrays
    rec = dict(run=run, wall=wall, tag=tag, stats={}, ext={})
    lvl = tb.level
    coin_idx = [idx['U']] + [i for i, n in enumerate(names) if n.startswith('B_') or n.startswith('CB_')]
    for g in (2000, 4000):
        c = full[g]
        st = R.rps_island_stats(c, N, tb, named)
        s = {k: round(_nm(v), 6) for k, v in st.items()}
        X = c / float(N)
        ec = e_comp_islands(tb, c, N)
        s['e_comp'] = round(_nm(ec), 6); s['e_comp_undef'] = int(np.isnan(ec).sum())
        s['to_play'] = round(float(np.einsum('ia,ab,ib->i', X, a['n_to'], X).mean()), 6)
        s['uto_play'] = round(float(np.einsum('ia,ab,ib->i', X, a['n_uto'], X).mean()), 6)
        s['forf_play'] = round(float(np.einsum('ia,ab,ib->i', X, a['forf'], X).mean()), 6)
        s['charge_play'] = round(float(np.einsum('ia,ab,ib->i', X, tb.CH, X).mean()), 6)
        for nm in ('SIMX', 'SIM100u', 'SIM100u~', 'U', 'PRR', 'PB', 'CRR'):
            s['mass_' + nm] = round(float(X[:, idx[nm]].mean()), 6)
            s['present_' + nm] = round(float((c[:, idx[nm]] > 0).mean()), 6)
        s['coin_mass'] = round(float(X[:, coin_idx].sum(1).mean()), 6)
        rec['stats'][str(g)] = s
    c = full[2000]
    st = R.rps_island_stats(c, N, tb, named)
    ec = e_comp_islands(tb, c, N)
    for k in ('e_gross', 'e_prog', 'forfeit', 'mix'):
        rec['ext']['isl_' + k] = [round(float(x), 5) for x in st[k]]
    rec['ext']['isl_e_comp'] = [None if np.isnan(x) else round(float(x), 5) for x in ec]
    dom = {}; sup = {}
    for g in R.CPS:
        g = int(g)
        cg = full[g]
        dom[str(g)] = cg.argmax(1).tolist()
        sup[str(g)] = [np.nonzero(row / float(N) >= 0.05)[0].tolist() for row in cg]
    rec['ext']['dom'] = dom
    rec['ext']['support2000'] = sup['2000']
    gl = [int(g) for g in R.CPS]
    rec['ext']['transitions'] = {'%d-%d' % (p, q): dict(modal=float(np.mean([dom[str(p)][i] != dom[str(q)][i] for i in range(I)])),
                                                         support=float(np.mean([sup[str(p)][i] != sup[str(q)][i] for i in range(I)])))
                                 for p, q in zip(gl[:-1], gl[1:])}
    rec['ext']['modal_share'] = {k: float(np.mean([names[d] == k for d in dom['2000']])) for k in set(names[d] for d in dom['2000'])}
    rec['ext']['modal_share_4000'] = {k: float(np.mean([names[d] == k for d in dom['4000']])) for k in set(names[d] for d in dom['4000'])}
    X = c / float(N)
    rec['ext']['forf_by_prog'] = [round(float(v), 6) for v in (X * np.einsum('ab,ib->ia', a['forf'], X)).mean(0)]
    rec['ext']['to_by_prog'] = [round(float(v), 6) for v in (X * np.einsum('ab,ib->ia', a['n_to'], X)).mean(0)]
    ix = idx['SIMX']; xm = X[:, ix]
    wx = xm.sum()
    if wx > 0:
        fam = tb.fam[0]
        rec['ext']['simx_plays'] = dict(weight=float(wx),
                                        finished=float((xm * (X @ a['unc_fin'][ix])).sum() / wx),
                                        forfeit=float((xm * (X @ a['forf'][ix])).sum() / wx),
                                        tape=float((xm * (X @ a['unc_tape'][ix])).sum() / wx),
                                        forfeit_by_family={f: float((xm * (X[:, fam == f] @ a['forf'][ix][fam == f])).sum() / wx)
                                                           for f in G.FAMILIES})
    else:
        rec['ext']['simx_plays'] = dict(weight=0.0)
    rec['ext']['x_counts'] = {nm: [int(v) for v in c[:, idx[nm]]] for nm in ('SIMX', 'SIM100u', 'SIM100u~')}
    return rec


def insp_record(base, tb, full, N, I, run, wall, tag):
    n0, n1 = tb.names
    named0, named1 = R.named_idx(tb)
    i0 = {n: i for i, n in enumerate(n0)}; i1 = {n: i for i, n in enumerate(n1)}
    a0, a1 = base.arr0, base.arr1
    rec = dict(run=run, wall=wall, tag=tag, stats={}, ext={})
    for g in (2000, 4000):
        c0, c1 = full[g]
        st = R.insp_island_stats(c0, c1, N, tb, named0, named1)
        s = {k: (round(float(np.nanmean(v)), 6) if np.isfinite(v).any() else float('nan')) for k, v in st.items()}
        m = F.insp_island_means(tb, c0, c1, N)
        for k in ('eff_gross', 'eff_net', 'u0', 'u1', 'u0g', 'u1g'):
            s['n_' + k] = round(float(np.mean(m[k])), 6)
        X0 = c0 / float(N); X1 = c1 / float(N)
        s['to0'] = round(float(np.einsum('ia,ib,ab->i', X0, X1, a0['n_to']).mean()), 6)
        s['to1'] = round(float(np.einsum('ib,ia,ba->i', X1, X0, a1['n_to']).mean()), 6)
        s['forf0'] = round(float(np.einsum('ia,ib,ab->i', X0, X1, a0['forf']).mean()), 6)
        s['forf1'] = round(float(np.einsum('ib,ia,ba->i', X1, X0, a1['forf']).mean()), 6)
        s['charge0'] = round(float(np.einsum('ia,ib,ab->i', X0, X1, tb.CH0).mean()), 6)
        s['charge1'] = round(float(np.einsum('ib,ia,ba->i', X1, X0, tb.CH1).mean()), 6)
        for nm in ('SIMX_I', 'SI100n', 'SI100n~'):
            s['mass0_' + nm] = round(float(X0[:, i0[nm]].mean()), 6); s['present0_' + nm] = round(float((c0[:, i0[nm]] > 0).mean()), 6)
        for nm in ('SIMX_E', 'SE100k', 'SE100k~'):
            s['mass1_' + nm] = round(float(X1[:, i1[nm]].mean()), 6); s['present1_' + nm] = round(float((c1[:, i1[nm]] > 0).mean()), 6)
        rec['stats'][str(g)] = s
    c0, c1 = full[2000]
    m = F.insp_island_means(tb, c0, c1, N)
    for k in ('u0g', 'u1g', 'u0', 'u1', 'eff_gross', 'eff_net'):
        rec['ext']['isl_' + k] = [round(float(x), 5) for x in m[k]]
    dom = {}; sup = {}
    for g in R.CPS:
        g = int(g)
        d0, d1 = full[g]
        dom[str(g)] = [d0.argmax(1).tolist(), d1.argmax(1).tolist()]
        sup[str(g)] = [[np.nonzero(r / float(N) >= 0.05)[0].tolist() for r in d0], [np.nonzero(r / float(N) >= 0.05)[0].tolist() for r in d1]]
    rec['ext']['dom'] = dom
    gl = [int(g) for g in R.CPS]
    rec['ext']['transitions'] = {'%d-%d' % (p, q): dict(
        modal=float(np.mean([(dom[str(p)][0][i], dom[str(p)][1][i]) != (dom[str(q)][0][i], dom[str(q)][1][i]) for i in range(I)])),
        support=float(np.mean([(sup[str(p)][0][i], sup[str(p)][1][i]) != (sup[str(q)][0][i], sup[str(q)][1][i]) for i in range(I)])))
        for p, q in zip(gl[:-1], gl[1:])}
    rec['ext']['modal0'] = {k: float(np.mean([n0[d] == k for d in dom['2000'][0]])) for k in set(n0[d] for d in dom['2000'][0])}
    rec['ext']['modal1'] = {k: float(np.mean([n1[d] == k for d in dom['2000'][1]])) for k in set(n1[d] for d in dom['2000'][1])}
    X0 = c0 / float(N); X1 = c1 / float(N)
    rec['ext']['forf0_by_prog'] = [round(float(v), 6) for v in (X0 * (X1 @ a0['forf'].T)).mean(0)]
    rec['ext']['forf1_by_prog'] = [round(float(v), 6) for v in (X1 * (X0 @ a1['forf'].T)).mean(0)]
    for nm, X, Y, arr, ix in (('simx_I', X0, X1, a0, i0['SIMX_I']), ('simx_E', X1, X0, a1, i1['SIMX_E'])):
        xm = X[:, ix]; wx = xm.sum()
        if wx > 0:
            rec['ext'][nm + '_plays'] = dict(weight=float(wx), finished=float((xm * (Y @ arr['unc_fin'][ix])).sum() / wx),
                                             forfeit=float((xm * (Y @ arr['forf'][ix])).sum() / wx),
                                             tape=float((xm * (Y @ arr['unc_tape'][ix])).sum() / wx))
        else:
            rec['ext'][nm + '_plays'] = dict(weight=0.0)
    return rec


# ----------------------------------------------------------------------------------------------------------------
# cell runner
# ----------------------------------------------------------------------------------------------------------------
def lt_cell(base, rule, arm, level, cell='primary', runs=FRESH_LT, out_dir=OUT, label=None, no_forfeit=False, no_write=False, quiet=False,
            keep_full=False, tag=''):
    game = base.game
    tb = make_view(base, rule, level, arm, no_forfeit=no_forfeit)
    cfg = R.CELLS[cell]
    N, I = cfg['N'], cfg['I']
    lab = label if label is not None else (PL.seed_label('A', level) if (rule == 'A' and arm == 'none') else seed_label(rule, arm, level))
    name = spec_name(game, rule, arm, level, cell) + tag
    recs = []
    for r in runs:
        t1 = time.time()
        if game == 'rps':
            full, ex = PL.lottery_rps_exact(tb, cell, r, N, I, lab)
            rec = rps_record(base, tb, full, N, I, r, time.time() - t1, name)
        else:
            full, ex = PL.lottery_insp_exact(tb, cell, r, N, I, lab)
            rec = insp_record(base, tb, full, N, I, r, time.time() - t1, name)
        if keep_full: rec['full'] = full
        recs.append(rec)
        if not quiet: print('%s run %d wall %.1f' % (name, r, time.time() - t1), flush=True)
    meta = dict(name=name, game=game, rule=rule, arm=arm, level=level, cell=cell, K=base.K, N=N, I=I, runs=list(runs), names=tb.names,
                fam=[f.tolist() for f in tb.fam], mismatch=base.mismatch, label=lab, n_base=base.n_base)
    if not no_write:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, name + '.json.gz')
        with gzip.open(path + '.tmp', 'wt') as f:
            json.dump(dict(meta=meta, recs=recs), f)
        os.replace(path + '.tmp', path)
    return dict(meta=meta, recs=recs)


def main(argv):
    mode = argv[0]
    if mode == 'lt':
        game = argv[1]
        tag = ''; runs = FRESH_LT
        if '--ext' in argv:          # supplementary runs (fresh indices 340-419), files tagged _ext
            i = argv.index('--ext'); runs = list(range(int(argv[i + 1]), int(argv[i + 2]))); tag = '_ext'
            argv = argv[:i] + argv[i + 3:]
        base = BaseX(game)
        print('tables ready', game, 'mismatch', base.mismatch, 'build %.0fs' % base.t_build, flush=True)
        for s in argv[2:]:
            rule, arm, level = parse_spec(s)
            path = os.path.join(OUT, spec_name(game, rule, arm, level) + tag + '.json.gz')
            if os.path.exists(path):
                print('skip', path); continue
            lt_cell(base, rule, arm, level, runs=runs, tag=tag)
    elif mode == 'build':
        BaseX(argv[1])
    else:
        raise SystemExit('mode?')


if __name__ == '__main__':
    main(sys.argv[1:])
