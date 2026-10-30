"""Sections, verdict scoring and main of the arm-T islands report (see many_islands_t_report.py for the loaders)."""
import os, sys, json, math
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import many_islands_t as M
from many_islands_t_common import NPOOL, parse_cell, tabs
from many_islands_t_report import (R, mean_ci, fmt, wilson, rec_at, table, vstar_end, TCRIT2, ROOT)
import many_islands_t_run as RN


# ====================================================================== sections
def sec_validation(r):
    r.add('## 0. Validations (before any counted cell)\n')
    rows = []
    for nm in ('tables', 'charge', 'ode', 'kernel', 'founding', 'arch', 'dslcmp'):
        v = r.get('V:' + nm)
        rows.append((nm, 'not run' if v is None else ('pass' if v.get('pass') else 'FAIL'), '' if v is None else '%.0f s' % v.get('wall', 0)))
    r.add(table(rows, ['validation', 'result', 'wall']))
    r.js['validation'] = {nm: r.get('V:' + nm) for nm in ('tables', 'charge', 'ode', 'kernel', 'founding', 'arch', 'dslcmp')}
    t = r.get('V:tables')
    if t:
        r.add('\nTables: mismatches against the stored arm-T tables, code %d, steps %d, joint %d, stored make_J %d (step-price path, max |diff| %.1e); forfeits in all 3 x 19,683 root evaluations: %d; failed-read histogram over the same %s; '
              'maximum failed reads in a root: constants %d, S and X %d, D %d; failed reads in a triple whose root cannot reach a read cycle: %d of %d; rotation-equivariance violations (gross payoff, failed reads, forfeits, steps, class, excluded slot, kernel tensor): %d.' % (
                  t['code_mismatch'], t['steps_mismatch'], t['joint_mismatch'], t['stored_make_J_mismatch'], t['step_price_max_abs_diff'], t['forfeits_total'],
                  t['nto_hist'], t['nto_const_max'], t['nto_single_exploit_max'], t['nto_two_max'], t['cycle_violations'], t['cycle_checked'], t['equiv_total_violations']))
        r.add('\nHand-built triples (notes 1.2), all matching the hand prediction: ' + '; '.join('(%s) failed reads %s, net payoffs at 0.1 %s, steps %s' % (
            ','.join(x['triple']), x['nto'], [round(z, 2) for z in x['net_at_0_1']], x['steps']) for x in t['hand_rows']))
    k = r.get('V:kernel')
    if k:
        r.add('\nKernel against simulated relaxation (P_fail %s; %d draws; draws from the post-anneal law and from the ODE at 10^3 events; forfeit stratum: %s):\n' % (k['P'], k['draws'], k['forfeit_stratum']))
        r.add(table([(x['stratum'], x['n'], x.get('fixed'), '%.3f' % x['expected'] if 'expected' in x else '', '%.2f' % x['z'] if 'z' in x else '',
                      '[%.4f, %.4f]' % tuple(x['wilson']) if 'wilson' in x else '', '%.4f' % x['mean_pfix'] if 'mean_pfix' in x else '', x.get('ok'))
                     for x in k['rows']], ['stratum', 'n', 'fixed', 'expected', 'z', 'Wilson 95%', 'mean P_fix', 'ok']))
    a = r.get('V:arch')
    if a:
        r.add('\nODE against the archipelago at I = 4,096 (20 worlds), V* share at 10^3 events per island:\n')
        r.add(table([(x['P'], '%.4f' % x['ode_vstar_1e3'], '%.4f' % x['worlds_mean'], '%.4f' % x['worlds_sd'], '%.4f' % x['diff'], x['ok']) for x in a['rows']],
                    ['P_fail', 'ODE', 'worlds mean', 'worlds sd', 'difference', 'within 0.02']))
    f = r.get('V:founding')
    if f:
        r.add('\nFounding at main, P_fail 0, against the stored churn T-main at mN = 0: V* %.4f (pool t-half-width %.4f) against stored %.4f [%.4f, %.4f]; mean total payoff of the settled triples %.4f (the stored "eff" is %.4f, defined on the locally closed states and not comparable). %s' % (
            f['mine_vstar'], f['mine_vstar_halfwidth'], f['stored_vstar'][0], f['stored_vstar'][1], f['stored_vstar'][2], f['mine_eff'], f['stored_eff'][0], f['note']))
    r.add('')


def sec_founding(r, cells):
    r.add('## 1. Founding and post-anneal law per cell (3 pools of 16,384 islands)\n')
    rows = []
    js = {}
    for c in cells:
        ps = [r.get('P:%s:%d' % (c, p)) for p in range(NPOOL)]
        ps = [p for p in ps if p]
        if not ps:
            continue
        sh = np.array([p['shares'] for p in ps])
        rd = np.array([p['readers'] for p in ps]).mean(axis=1)
        row = [c, '%d' % sum(p['settled'] for p in ps), '%d/%d/%d/%d' % (sum(p['capped'] for p in ps), sum(p['late'] for p in ps), sum(p['mixed'] for p in ps), sum(p['drifting'] for p in ps))]
        for k in range(5):
            row.append(fmt(*mean_ci(sh[:, k]), nd=3))
        row.append(fmt(*mean_ci(rd), nd=3))
        row.append('%d' % int(np.mean([p['support'] for p in ps])))
        row.append('%.0f' % np.mean([p['mean_gen'] for p in ps]))
        rows.append(row)
        js[c] = dict(shares=sh.tolist(), readers=rd.tolist(), support=[p['support'] for p in ps])
    r.add(table(rows, ['cell (dose|P_fail|A)', 'settled', 'capped/late/mixed/drifting', 'F', 'U', 'G', 'W', 'D', 'reader marginal', 'distinct triples per pool', 'mean gens']))
    r.js['founding'] = js
    r.add('')


def traj_row(jobs):
    out = []
    for T in (0.0, 10.0, 100.0, 1e3, 1e4, 1e5):
        v = [rec_at(j['recs'], T)['shares'][0] for j in jobs if rec_at(j['recs'], T) is not None]
        out.append(float(np.mean(v)) if v else None)
    return out


def sec_ode(r, cells):
    r.add('## 2. The exact ODE: V* share by cell and start (symmetrized trajectories; mean over the 3 pools)\n')
    r.add('Time is migrant events per island. `conv` = pools meeting criterion (a); `V*(end)` is the value at the last time computed (mean +- t half-width over pools), `end` its time; `min pool` the lowest pool.\n')
    rows = []
    js = {}
    for c in cells:
        dose, P, A = parse_cell(c)
        for st in ('nat', 'fair', 'uneq', 'wd'):
            jobs = r.ode_pools(c, P, st)
            if not jobs:
                continue
            tr = traj_row(jobs)
            ends = vstar_end(jobs)
            conv = sum(1 for j in jobs if j['status'] == 'converged')
            sh = np.array([j['final_shares'] for j in jobs]).mean(axis=0)
            rows.append([c, st, '%d/%d' % (conv, len(jobs))] + ['%.4f' % x if x is not None else '' for x in tr] + [fmt(*mean_ci(ends), nd=4), '%.4f' % min(ends),
                         '%.1e' % np.mean([j['t_end'] for j in jobs]), '%.4f' % sh[1], '%.4f' % sh[2], '%.1e' % max(j['resid_end'] for j in jobs)])
            full = {}
            for T_ in (0.0, 10.0, 100.0, 1e3, 1e4, 1e5):
                rr = [rec_at(j['recs'], T_) for j in jobs]
                rr = [x for x in rr if x is not None]
                full['%g' % T_] = dict(shares=np.mean([x['shares'] for x in rr], axis=0).tolist(), pairs=np.mean([x['pairs'] for x in rr], axis=0).tolist(),
                                       readers=np.mean([x['readers'] for x in rr], axis=0).tolist())
            full['end'] = dict(t=float(np.mean([j['t_end'] for j in jobs])), shares=np.mean([j['final_shares'] for j in jobs], axis=0).tolist(),
                               pairs=np.mean([j['final_pairs'] for j in jobs], axis=0).tolist(), readers=np.mean([j['final_readers'] for j in jobs], axis=0).tolist())
            js['%s|%s' % (c, st)] = dict(pools=[dict(status=j['status'], t_end=j['t_end'], shares_end=j['final_shares'], pairs_end=j['final_pairs'], readers_end=j['final_readers'],
                                                    resid=j['resid_end'], tilt=j.get('tilt')) for j in jobs], vstar_traj=tr, trajectory_mean_over_pools=full)
    r.add(table(rows, ['cell', 'start', 'conv', 'V*(0)', 'V*(10)', 'V*(10^2)', 'V*(10^3)', 'V*(10^4)', 'V*(10^5)', 'V*(end)', 'min pool', 'end', 'U(end)', 'G(end)', 'max resid']))
    r.js['ode'] = js
    r.add('')
    # unavailable tilts
    na = []
    for c in cells:
        dose, P, A = parse_cell(c)
        for st in ('fair', 'uneq', 'wd'):
            for p in range(NPOOL):
                j = r.ode(c, P, st, p)
                if j is not None and not j.get('available', True):
                    na.append('%s %s pool %d' % (c, st, p))
    if na:
        r.add('Tilted starts unavailable (the tilted class has no mass in the symmetrized post-anneal law): ' + '; '.join(na) + '.\n')
    tol = []
    for c in cells:
        dose, P, A = parse_cell(c)
        j = r.ode(c, P, 'nat', 0)
        if j and 'tolcheck' in j:
            tol.append((c, j['tolcheck']['max_share_diff_at_1e4'], j['tolcheck']['max_share_diff_end'], j['tolcheck']['t_end']))
    if tol:
        r.add('Solver check (natural start, pool 0; explicit rtol 1e-8 against 1e-10, backward Euler 8 against 16 steps per decade): max difference of any class share.\n')
        r.add(table([(c, '%.1e' % a, '%.1e' % b, '%.1e' % t) for c, a, b, t in tol], ['cell', 'at 10^4 (tolerance 10^-8 vs 10^-10)', 'at end (BE 8 vs 16 per decade)', 'end']))
        r.add('')


def sec_classes(r):
    r.add('## 3. Class trajectories, main dose, A = 0 (symmetrized natural start, mean over pools)\n')
    for c in ('main|0|0', 'main|0.1|0', 'main|0.03|0'):
        dose, P, A = parse_cell(c)
        jobs = r.ode_pools(c, P, 'nat')
        if not jobs:
            continue
        rows = []
        for T in (0.0, 10.0, 100.0, 1e3, 1e4, 1e5):
            sh = np.mean([rec_at(j['recs'], T)['shares'] for j in jobs], axis=0)
            pr = np.mean([rec_at(j['recs'], T)['pairs'] for j in jobs], axis=0)
            rd = np.mean([rec_at(j['recs'], T)['readers'] for j in jobs], axis=0)
            rows.append(['%g' % T] + ['%.4f' % x for x in sh] + ['%.4f' % x for x in pr] + ['%.4f' % rd.mean()])
        e = np.mean([j['final_shares'] for j in jobs], axis=0)
        pe = np.mean([j['final_pairs'] for j in jobs], axis=0)
        re_ = np.mean([j['final_readers'] for j in jobs], axis=0)
        rows.append(['end %.1e' % np.mean([j['t_end'] for j in jobs])] + ['%.4f' % x for x in e] + ['%.4f' % x for x in pe] + ['%.4f' % re_.mean()])
        r.add('**%s**\n' % c)
        r.add(table(rows, ['events', 'F', 'U', 'G', 'W', 'D', 'pair a', 'pair b', 'pair c', 'reader marginal']))
        r.add('')


def sec_readers(r, cells):
    r.add('## 4. Reader marginal along the trajectories (slot-mean of the marginal mass on reader programs; mean over pools)\n')
    rows = []
    for c in cells:
        dose, P, A = parse_cell(c)
        if dose == '0':
            continue
        for st in ('nat', 'uneq'):
            jobs = r.ode_pools(c, P, st)
            if not jobs:
                continue
            row = [c, st]
            for T in (0.0, 10.0, 100.0, 1e3, 1e4, 1e5):
                v = [np.mean(rec_at(j['recs'], T)['readers']) for j in jobs if rec_at(j['recs'], T) is not None]
                row.append('%.4f' % np.mean(v) if v else '')
            row.append('%.4f' % np.mean([np.mean(j['final_readers']) for j in jobs]))
            rows.append(row)
    r.add(table(rows, ['cell', 'start', '0', '10', '10^2', '10^3', '10^4', '10^5', 'end']))
    r.add('')


def sec_raw(r, cells):
    r.add('## 5. Raw (unsymmetrized) pool laws: the sampling tilt the knife-edge amplifies\n')
    rows = []
    js = {}
    for c in cells:
        dose, P, A = parse_cell(c)
        jobs = r.ode_pools(c, P, 'nat', raw=True)
        for j in jobs:
            pr0 = rec_at(j['recs'], 0.0)['pairs']
            tilt0 = (max(pr0) - min(pr0)) / max(sum(pr0), 1e-12)
            fin = j['final_pairs']
            fs = sum(fin)
            r4 = rec_at(j['recs'], 1e4)
            rows.append([c, j['pool'], '%.4f' % tilt0, ('%.4f' % r4['shares'][0]) if r4 else '', '%.4f' % fs, ', '.join('%.3f' % (x / max(fs, 1e-12)) for x in fin), '%.1e' % j['t_end'], j['status']])
        js[c] = [dict(pool=j['pool'], pairs_end=j['final_pairs'], t_end=j['t_end'], shares_end=j['final_shares']) for j in jobs]
    r.add(table(rows, ['cell', 'pool', 'initial pair imbalance (max - min)/F', 'V*(10^4)', 'V*(end)', 'shares of V* on pairs a, b, c at the end', 'end', 'status']))
    r.js['raw'] = js
    r.add('')


def sec_jac(r, cells):
    r.add('## 6. The symmetric limit: Jacobian on the rotation-non-invariant sector, controlled perturbations\n')
    rows = []
    js = {}
    for c in cells:
        dose, P, A = parse_cell(c)
        j = r.get('J:%s:%s:0' % (c, P))
        if not j:
            continue
        sp = j['spectrum']
        top = sp['noninv_top'][0]
        arn = j.get('arnoldi_full')
        rows.append([c, j['ode_status'], '%.1e' % j['ode_t_end'], sp['support'], '%.0e' % sp['thr'], '%.3e' % sp['noninv_max'], sp['noninv_count_pos'], '%.2e' % sp['noninv_min'],
                     ' / '.join('%.2f' % z for z in top['class_l1']), '%.1e' % sp['leak_rate'],
                     ('%.3e%s' % (arn[0][0], '' if j.get('arnoldi_converged') else ' (unconverged)')) if isinstance(arn, list) and arn else str(arn)[:30]])
        js[c] = dict(lam=sp['noninv_max'], npos=sp['noninv_count_pos'], top=top, inv_top=sp['inv_top'][:3], leak=sp['leak_rate'], arnoldi=arn, support=sp['support'], thr=sp['thr'],
                     sensitivity=j['support_sensitivity'])
    r.add(table(rows, ['cell', 'limit status', 'limit t', 'support S', 'thr', 'largest Re (non-invariant)', '# Re > 0', 'smallest Re', 'leading eigenvector L1 by class F/U/G/W/D', 'leak rate out of S', 'full-space Arnoldi lead']))
    r.add('')
    r.add('Controlled symmetry-breaking perturbations (relative amplitude eps in the largest entry; unprojected equation; growth rate of the non-invariant norm fitted over [3 N0, 0.05]):\n')
    prow = []
    for c in cells:
        dose, P, A = parse_cell(c)
        j = r.get('J:%s:%s:0' % (c, P))
        if not j:
            continue
        for p in j['perturbations']:
            prow.append([c, p['kind'], '%g' % p['eps'], '%.2e' % p['N0'], '%.3e' % p['lam_jac'],
                         ('%.3e' % p['rate_fit']) if p['rate_fit'] is not None else (('early %.2e' % p['rate_early']) if p.get('rate_early') is not None else 'n/a'), '%.1e' % p['T_end'], '%.3f' % p['Ns'][-1]])
    r.add(table(prow, ['cell', 'direction', 'eps', 'N0', 'lambda (Jacobian)', 'fitted growth rate', 'T', 'N(T)']))
    r.js['jacobian'] = js
    r.add('')


def world_stats(w):
    I = w['I']
    rows = w['worlds']
    n = len(rows)
    fin = [np.array(x['pairs'])[-1] for x in rows]
    fair = [f.sum() / I for f in fin]
    keep3 = [bool((f / I >= 0.05).all()) for f in fin]
    cons99 = [bool(fs >= 0.99) for fs in fair]
    single = [bool(fs >= 0.99 and f.max() / max(f.sum(), 1) >= 0.95) for f, fs in zip(fin, fair)]
    first = []
    for x in rows:
        fl = [v for v in x['first_loss'] if v > 0]
        first.append(min(fl) / I if fl else None)
    dom = [int(np.argmax(f)) if s else None for f, s in zip(fin, single)]
    cps = w['cps']
    hist = [np.array(x['hist']) / I for x in rows]
    uneq = [bool(h[-1][1] >= 0.99) for h in hist]
    collapse = []
    for h in hist:
        F = h[:, 0]
        pk = int(np.argmax(F >= 0.9)) if (F >= 0.9).any() else None
        t = None
        if pk is not None and F[-1] < 0.5:
            for ci in range(pk, len(F)):
                if F[ci] < 0.5:
                    t = cps[ci]
                    break
        collapse.append(t)
    return dict(n=n, keep3=sum(keep3), cons99=sum(cons99), single=sum(single), fair_mean=float(np.mean(fair)), first=first, dom=dom, fin=[f.tolist() for f in fin],
                uneq=sum(uneq), collapse=collapse)


def sec_worlds(r):
    r.add('## 7. Finite worlds (20 worlds per cell and I, to 10^5 events per island)\n')
    rows = []
    js = {}
    chi = {}
    for c, suffix in [(c, sfx) for sfx in ('', ':uneq') for c in ('main|0.1|0', 'main|0|0', '0|0|0')]:
        for I in RN.WORLD_I:
            w = r.get('W:%s:%d%s' % (c, I, suffix))
            if not w:
                continue
            s = world_stats(w)
            c_lab = c + (' (unequal tilt)' if suffix else '')
            fl = [x for x in s['first'] if x is not None]
            med = ('%.0f' % np.median(fl)) if fl else 'never'
            lo, hi = wilson(s['cons99'], s['n'])
            rows.append([c_lab, I, s['n'], '%.4f' % s['fair_mean'], '%d (%.2f-%.2f)' % (s['cons99'], lo, hi), s['single'], s['keep3'], '%d / %d' % (len(fl), s['n']), med,
                         ', '.join(str(sum(1 for d in s['dom'] if d == q)) for q in range(3)), s['uneq'], sum(1 for t in s['collapse'] if t is not None)])
            js['%s|%d%s' % (c, I, suffix)] = dict(cons99=s['cons99'], single=s['single'], keep3=s['keep3'], fair_mean=s['fair_mean'], first=s['first'], dom=s['dom'], fin=s['fin'], uneq=s['uneq'], collapse=s['collapse'])
            for d in s['dom']:
                if d is not None and not suffix:
                    chi.setdefault(c, [0, 0, 0])[d] += 1
    r.add(table(rows, ['cell', 'I', 'worlds', 'mean fair share at 10^5', '>= 0.99 on fair pairs (Wilson)', 'single-pair worlds', 'all three pairs >= 0.05', 'worlds that lost a pair', 'median events/island to first loss', 'end pair counts (a, b, c)', 'worlds ending >= 0.99 unequal', 'fair consensus (>= 0.9) then collapse below 0.5']))
    r.add('')
    from scipy.stats import chi2 as C2
    lines = []
    tot = np.zeros(3)
    for c, v in chi.items():
        v = np.array(v, float)
        tot += v
        if v.sum() > 0:
            x2 = float(((v - v.sum() / 3) ** 2 / (v.sum() / 3)).sum())
            lines.append('%s: counts %s, chi2 %.2f, p %.3f' % (c, v.astype(int).tolist(), x2, 1 - C2.cdf(x2, 2)))
    if tot.sum() > 0:
        x2 = float(((tot - tot.sum() / 3) ** 2 / (tot.sum() / 3)).sum())
        lines.append('all cells: counts %s, chi2 %.2f, p %.3f' % (tot.astype(int).tolist(), x2, 1 - C2.cdf(x2, 2)))
        js['equal_likelihood'] = dict(by_cell=chi, total=tot.tolist(), chi2=x2, p=float(1 - C2.cdf(x2, 2)))
    r.add('End pair among single-pair worlds (pair indices in the order of V; equal in law by the equivariance of the whole implementation): ' + '; '.join(lines))
    r.js['worlds'] = js
    r.add('')


def sec_worldsx(r):
    r.add('### 7b. Long finite worlds (20 worlds each): does a fair consensus last?\n')
    rows = []
    js = {}
    for c in ('main|0.1|0', 'main|0|0', '0|0|0'):
        for (I, T) in ((64, 10 ** 7), (256, 3 * 10 ** 6), (1024, 10 ** 6)):
            w = r.get('WX:%s:%d:%d' % (c, I, T))
            if not w:
                continue
            s = world_stats(w)
            cps = w['cps']
            # fair share of the worlds at selected times
            hist = [np.array(x['hist']) / I for x in w['worlds']]
            sel = [t for t in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7) if t in cps]
            fs = [float(np.mean([h[cps.index(t), 0] for h in hist])) for t in sel]
            cl = [t for t in s['collapse'] if t is not None]
            rows.append([c, I, T, s['n'], ', '.join('%g: %.3f' % (t, f) for t, f in zip(sel, fs)), s['cons99'], s['uneq'], len(cl), ('%.0f' % np.median(cl)) if cl else 'none',
                         s['single'], s['keep3']])
            js['%s|%d' % (c, I)] = dict(T=T, cons99=s['cons99'], uneq=s['uneq'], collapse=s['collapse'], fair_by_time=dict(zip([str(t) for t in sel], fs)))
    r.add(table(rows, ['cell', 'I', 'to (events/island)', 'worlds', 'mean fair share at (events/island)', '>= 0.99 on fair pairs at end', '>= 0.99 unequal at end', 'worlds with a fair consensus that collapsed',
                       'median collapse checkpoint', 'single-pair worlds at end', 'all three pairs >= 0.05 at end']))
    r.js['worldsx'] = js
    r.add('')


def sec_limit(r):
    r.add('## 6b. What the symmetric limit is made of (natural start, pool 0)\n')
    import many_islands_t_ode as O
    from many_islands_t_common import xstar_path
    T = r.tabs
    js = {}
    for c in ('0|0|0', 'lo|0|0', 'main|0|0', 'main|0.1|0', 'main|0.03|0', 'hi|0|0', 'hi|0.1|0'):
        dose, P, A = parse_cell(c)
        pth = xstar_path(c, P, 'nat', 0)
        if not os.path.exists(pth):
            continue
        x = np.load(pth)
        idx = np.argsort(-x)[:8]
        nr = T.is_reader[O._TR].sum(axis=1)
        mass_by_readers = [float(x[nr == k].sum()) for k in range(4)]
        fam_mass = {}
        for k, f in enumerate(['const', 'single', 'two', 'exploit']):
            fam_mass[f] = float(np.mean([(marg_f(x, T, s, f)) for s in range(3)]))
        top = [(float(x[t]), [T.names[a] for a in O._TR[t]], M.CLS[T.CL.ravel()[t]]) for t in idx]
        r.add('**%s**: triples with mass above 1e-9: %d; mass by number of readers in the triple (0/1/2/3): %s; slot-mean program-family mass: %s; top triples: %s\n' % (
            c, int((x > 1e-9).sum()), ', '.join('%.4f' % m for m in mass_by_readers), ', '.join('%s %.4f' % (k, v) for k, v in fam_mass.items()),
            '; '.join('%.4f (%s)' % (m, ' '.join(n)) for m, n, cl in top)))
        js[c] = dict(support=int((x > 1e-9).sum()), mass_by_readers=mass_by_readers, fam_mass=fam_mass, top=top)
    r.js['limit_composition'] = js
    r.add('')


def marg_f(x, T, s, fam):
    import many_islands_t_ode as O
    q = O.marginals(x)[s]
    return float(sum(q[i] for i in range(M.NP) if T.fam[i] == fam))


def sec_charge(r, cells):
    r.add('## 8. The charge: effect on founding and on the limit\n')
    rows = []
    for c in ('main|0|0', 'main|0.03|0', 'main|0.1|0'):
        ps = [r.get('P:%s:%d' % (c, p)) for p in range(NPOOL)]
        ps = [p for p in ps if p]
        if ps:
            rows.append([c, fmt(*mean_ci([p['shares'][0] for p in ps]), nd=4), fmt(*mean_ci([np.mean(p['readers']) for p in ps]), nd=4)])
    r.add(table(rows, ['founding cell', 'post-anneal V*', 'post-anneal reader marginal']))
    r.add('')
    r.add('Founding law x migration charge crossed (dose main, A = 0; symmetrized starts, mean over pools):\n')
    rows = []
    for pf in ('0', '0.1'):
        for pm in (0.0, 0.1):
            c = 'main|%s|0' % pf
            for st in ('nat', 'uneq'):
                jobs = r.ode_pools(c, pm, st)
                if jobs:
                    tr = traj_row(jobs)
                    rows.append([pf, pm, st, '%d/%d' % (sum(j['status'] == 'converged' for j in jobs), len(jobs)), '%.4f' % tr[3], '%.4f' % tr[5], fmt(*mean_ci(vstar_end(jobs)), nd=4),
                                 '%.4f' % np.mean([np.mean(j['final_readers']) for j in jobs])])
    r.add(table(rows, ['founding P_fail', 'migration P_fail', 'start', 'conv', 'V*(10^3)', 'V*(10^5)', 'V*(end)', 'reader marginal (end)']))
    r.add('')
    T = r.tabs
    d1 = float(np.abs(T.payoff(0.1, 0.0) - T.payoff(0.1, 0.1)).max())
    d2 = float(np.abs(T.payoff(0.0, 0.1) - T.payoff(0.0, 0.0)).max())
    r.add('Controls of question 5. The table has no forfeit event, so (i) failed reads charged without the forfeit charge (rule A) are the same payoff table as A_f (max |A - A_f| = %.1e) and (ii) forfeits charged without failed reads are the P_fail = 0 table (max difference %.1e); the two ODE controls are therefore identical to the cells already run (no separate trajectory).\n' % (d1, d2))
    r.js['charge_controls'] = dict(A_vs_Af=d1, forfeit_only_vs_zero=d2)
    r.add('Failed reads and timeouts by program family, per play (laws: independent-slot founding law, symmetrized post-anneal law, the natural-start limit):\n')
    rows = []
    for c in ('main|0.1|0', 'hi|0.1|0'):
        dose, P, A = parse_cell(c)
        x = r.get('X:%s:%s' % (c, P))
        if not x:
            continue
        for law, key in (('founding', 'charges_founding'), ('post-anneal', 'charges_post'), ('limit', 'charges_limit')):
            ch = x.get(key)
            if not ch:
                continue
            for f, v in ch['by_family'].items():
                if v['failed_reads_per_play'] is None:
                    continue
                rows.append([c, law, f, '%.4f' % v['mass'], '%.4f' % v['failed_reads_per_play'], '%.4f' % v['share_plays_with_timeout'], '%.1f' % v['steps_per_play'], '%.5f' % v['forfeits_per_play']])
            rows.append([c, law, 'all triples', '', '%.4f' % ch['mean_failed_reads_per_play'], '%.4f of encounters have a failed read in some slot' % ch['share_triples_with_timeout'], '', ''])
    r.add(table(rows, ['cell', 'law', 'program family', 'mass', 'failed reads / play', 'share of plays with one', 'steps / play', 'forfeits / play']))
    r.add('')


def sec_rates(r, cells):
    r.add('## 9. What carries conversion: per-event rates into V* by migrant family, fair-to-fair rates\n')
    r.add('Per event, per island of the recipient class, at the post-anneal symmetrized law (mean of the pools) and at the limit when it exists. Families: constants, single readers, two-partner readers, exploiting readers.\n')
    rows = []
    js = {}
    for c in ('main|0|0', 'main|0.1|0', 'hi|0|0', 'hi|0.1|0', 'lo|0|0', '0|0|0'):
        dose, P, A = parse_cell(c)
        x = r.get('X:%s:%s' % (c, P))
        if not x:
            continue
        for key, lab in (('conv_post', 'post-anneal'), ('conv_limit', 'limit')):
            cv = x.get(key)
            if not cv:
                continue
            for cl, v in cv.items():
                if v is None or cl == 'F':
                    continue
                if lab == 'limit' and v['mass'] < 1e-9:
                    continue                      # the class is empty at the limit (rates would divide by ~0)
                rows.append([c, lab, cl, '%.4f' % v['mass'], '%.4f' % v['to_F_total']] + ['%.4f' % v['to_F_by_family'][f] for f in ('const', 'single', 'two', 'exploit')] + ['%.4f' % v['any_fix_total']])
        js[c] = {k: x.get(k) for k in ('conv_post', 'conv_limit', 'ka_post', 'ka_limit', 'class_rates_post')}
    r.add(table(rows, ['cell', 'law', 'recipient class', 'class mass', 'rate to V* (all)', 'by const', 'by single', 'by two', 'by exploit', 'rate of any fixation']))
    r.add('')
    r.add('Per migrant: the same post-anneal rates divided by the family\'s share of the donors\' slot marginals (the rate a migrant of that family converts a recipient of the class into V*):\n')
    rows = []
    for c in ('main|0|0', 'main|0.1|0', 'hi|0|0', 'hi|0.1|0', 'lo|0|0'):
        dose, P, A = parse_cell(c)
        x = r.get('X:%s:%s' % (c, P))
        if not x or not x.get('conv_post'):
            continue
        fm = {f: x['charges_post']['by_family'][f]['mass'] for f in ('const', 'single', 'two', 'exploit')}
        for cl, v in x['conv_post'].items():
            if v is None or cl in ('F', 'G'):
                continue
            rows.append([c, cl] + ['%.4f' % (v['to_F_by_family'][f] / fm[f]) if fm[f] > 0 else '' for f in ('const', 'single', 'two', 'exploit')] + ['%.3f' % (fm['single'] / max(fm['const'], 1e-12) * 0 + 0) if False else ''])
    r.add(table([row[:6] for row in rows], ['cell', 'recipient class', 'per const migrant', 'per single-reader migrant', 'per two-partner migrant', 'per exploiting migrant']))
    r.add('')
    rows = []
    for c in ('main|0|0', 'main|0.1|0', 'hi|0|0', 'hi|0.1|0', 'lo|0|0'):
        dose, P, A = parse_cell(c)
        x = r.get('X:%s:%s' % (c, P))
        if not x:
            continue
        for key, lab in (('ka_post', 'post-anneal'), ('ka_limit', 'limit')):
            ka = x.get(key)
            if not ka:
                continue
            rows.append([c, lab] + ['%.3e' % ka['kappa_by_offset'][str(o)] for o in (0, 1, 2)] + ['%.3e' % ka['alpha_by_offset'][str(o)] for o in (0, 1, 2)] + ['%.3e' % ka['leave_by_offset'][str(o)] for o in (0, 1, 2)])
    r.add('kappa(a, b) = probability per event that a recipient on pair a hit by a donor on pair b ends on b; alpha = ends on the third pair; leave = ends outside V*; averaged over ordered pairs with the same cyclic offset of the excluded slots (offset 0: the same pair):\n')
    r.add(table(rows, ['cell', 'law', 'kappa o0', 'kappa o1', 'kappa o2', 'alpha o0', 'alpha o1', 'alpha o2', 'leave o0', 'leave o1', 'leave o2']))
    r.js['rates'] = js
    r.add('')


def sec_ablation(r):
    r.add('## 10. Ablations at the main dose (a reader family removed from the seed; its mass moved to the constants)\n')
    rows = []
    js = {}
    for tag, lab in (('main', 'none (main)'), ('ab-So', 'switchers S..o.. removed (4 programs)'), ('ab-D', 'two-partner readers removed (8)'), ('ab-X', 'exploiting readers removed (2)')):
        for P in ('0', '0.1'):
            c = ('main|%s|0' % P) if tag == 'main' else ('%s|%s|0' % (tag, P))
            jobs = r.ode_pools(c, float(P), 'nat')
            ps = [r.get('P:%s:%d' % (c, p)) for p in range(NPOOL)]
            ps = [p for p in ps if p]
            if not jobs:
                continue
            tr = traj_row(jobs)
            rows.append([lab, P, '%d/%d' % (sum(j['status'] == 'converged' for j in jobs), len(jobs)), fmt(*mean_ci([p['shares'][0] for p in ps]), nd=4) if ps else '', '%.4f' % tr[3], '%.4f' % tr[4], '%.4f' % tr[5],
                         fmt(*mean_ci(vstar_end(jobs)), nd=5), '%.5f' % np.mean([j['final_shares'][2] for j in jobs]), '%.4f' % np.mean([np.mean(j['final_readers']) for j in jobs])])
            js['%s|%s' % (tag, P)] = dict(vstar_end=vstar_end(jobs), traj=tr)
    r.add(table(rows, ['removed', 'P_fail', 'conv', 'founding V*', 'V*(10^3)', 'V*(10^4)', 'V*(10^5)', 'V*(end)', 'G(end)', 'reader marginal (end)']))
    r.js['ablations'] = js
    r.add('')


def sec_dsl(r):
    v = r.get('V:dslcmp')
    r.add('## 11. Arm T at P_fail 0 against the DSL readers arm R: where the tables differ (a description; fuel decides whether a fallback runs, so no difference is attributed to the timeout action)\n')
    if not v:
        return
    rows = []
    for ev in ('modal', 'weak'):
        for k, s in v[ev]['stats'].items():
            rows.append([ev, k, s['n'], s['differ'], '%.3f' % (s['differ'] / max(s['n'], 1)), s['class_differ'], json.dumps(s['by_flag'])])
    r.add(table(rows, ['DSL evaluator', 'triple type', 'triples', 'outcome differs', 'share', 'class differs', 'by the timeout flags (y accepts a timed-out read, n does not) of the T readers in the triple']))
    ex = []
    for ev in ('modal', 'weak'):
        for k, s in v[ev]['stats'].items():
            for e in s['examples'][:3]:
                ex.append('%s / %s: (%s, %s, %s) T -> %s, DSL -> %s' % (ev, k, e[0], e[1], e[2], e[3], e[4]))
    r.add('\nExamples: ' + '; '.join(ex))
    r.add('')


# ====================================================================== verdicts
def verdicts(r):
    V = {}
    out = []

    def score(name, claim, status, detail):
        out.append((name, claim, status, detail))
        V[name] = dict(claim=claim, status=status, detail=detail)

    def ends(c, P, st):
        jobs = r.ode_pools(c, P, st)
        return jobs, vstar_end(jobs)

    def conv_all(jobs):
        return len(jobs) == NPOOL and all(j['status'] == 'converged' for j in jobs)

    # 1
    jobs, e = ends('main|0|0', 0.0, 'nat')
    if jobs:
        if not conv_all(jobs):
            proxy = [rec_at(j['recs'], 1e5)['shares'][0] for j in jobs]
            st = 'unscored' if min(proxy) >= 0.95 or True else 'unscored'
            score('P1', 'main, P_fail 0: V* >= 0.99 at convergence from the natural law [< 0.95]', 'unscored (unresolved; V* at the end %s)' % ', '.join('%.4f' % x for x in e), 'proxy (b) at 10^5: %s' % proxy)
        else:
            st = 'held' if min(e) >= 0.99 else ('failed' if min(e) < 0.95 else 'partial')
            score('P1', 'main, P_fail 0: V* >= 0.99 at convergence from the natural law [< 0.95]', st, 'V* at convergence %s (t = %s)' % (', '.join('%.5f' % x for x in e), ', '.join('%.0e' % j['t_end'] for j in jobs)))
    # 2
    res = []
    stat = 'held'
    for st_ in ('uneq', 'wd'):
        jobs, e = ends('main|0|0', 0.0, st_)
        if not jobs:
            res.append('%s unavailable' % st_)
            continue
        res.append('%s: %s (%s)' % (st_, ', '.join('%.5f' % x for x in e), 'converged' if conv_all(jobs) else 'unresolved'))
        if min(e) < 0.9:
            stat = 'failed'
        elif min(e) < 0.99 and stat == 'held':
            stat = 'partial'
        if not conv_all(jobs) and stat == 'held':
            stat = 'unscored'
    score('P2', 'main, P_fail 0: V* >= 0.99 from the unequal and the wasteful/disagreement tilts [any below 0.9]', stat, '; '.join(res))
    # 3
    res = []
    ok = True
    for P in (0.0, 0.1):
        c = '0|%s|0' % ('0' if P == 0.0 else '0.1')
        ju, eu = ends(c, P, 'uneq')
        jf, ef = ends(c, P, 'fair')
        if ju and jf:
            Uend = [j['final_shares'][1] for j in ju]
            res.append('P_fail %s: unequal tilt U(end) %s V* %s; fair tilt V*(end) %s' % (P, ', '.join('%.4f' % x for x in Uend), ', '.join('%.4f' % x for x in eu), ', '.join('%.4f' % x for x in ef)))
            ok &= (min(Uend) >= 0.9 and min(ef) >= 0.9)
            same = (np.mean(eu) > 0.5) == (np.mean(ef) > 0.5)
            if same:
                ok = False
    score('P3', 'dose 0: unequal tilt -> U >= 0.9, fair tilt -> V* >= 0.9 [both to the same class]', 'held' if ok else 'failed', '; '.join(res))
    # 4
    jj = r.get('J:main|0|0:0.0:0')
    j1 = r.get('J:main|0.1|0:0.1:0')
    lam0 = jj['spectrum']['noninv_max'] if jj else None
    lam1 = j1['spectrum']['noninv_max'] if j1 else None
    wk = r.get('W:main|0|0:1024')
    wk1 = r.get('W:main|0.1|0:1024')
    d4 = 'lambda(main, 0) = %s, lambda(main, 0.1) = %s' % (('%.3e' % lam0) if lam0 is not None else 'n/a', ('%.3e' % lam1) if lam1 is not None else 'n/a')
    a_ok = lam0 is not None and lam1 is not None and lam0 > 0 and lam1 > 0
    a_fail = lam0 is not None and lam1 is not None and (lam0 <= 0 or lam1 <= 0)
    wres = []
    fw_stat = 'unscored'
    c18 = 'unscored'
    for lab, w, lam in (('P0', wk, lam0), ('P0.1', wk1, lam1)):
        if w and lam is not None:
            s = world_stats(w)
            lnsq = math.log(math.sqrt(1024))
            scored = lam * 1e5 > lnsq
            wres.append('%s: lambda*1e5 = %.1f (ln sqrt I = %.2f, %s); worlds keeping all three pairs %d/20; worlds >= 0.99 on fair pairs %d/20; single-pair worlds %d/20' % (
                lab, lam * 1e5, lnsq, 'scored' if scored else 'unscored', s['keep3'], s['cons99'], s['single']))
            if scored:
                if s['keep3'] >= 10:
                    fw_stat = 'failed'
                elif s['keep3'] <= 2 and fw_stat != 'failed':
                    fw_stat = 'held'
                elif fw_stat != 'failed':
                    fw_stat = 'partial'
            if s['cons99'] < 15:
                c18 = 'failed'
            elif s['cons99'] >= 18 and c18 != 'failed':
                c18 = 'held'
            elif c18 != 'failed':
                c18 = 'partial'
    score('P4a', 'main: largest real part on the non-invariant subspace positive [<= 0]', 'held' if a_ok else ('failed' if a_fail else 'unscored'), d4)
    score('P4b', 'main, I = 1024: at most 2/20 worlds keep all three pairs >= 0.05 [>= 10/20] (scored only if lambda*1e5 > ln sqrt I)', fw_stat,
          '; '.join('%s: lambda*1e5 = %.1f vs ln sqrt I = %.2f; worlds keeping all three pairs %d/20' % (lab, lam * 1e5, math.log(math.sqrt(1024)), world_stats(w)['keep3'])
                    for lab, w, lam in (('P_fail 0', wk, lam0), ('P_fail 0.1', wk1, lam1)) if w and lam is not None))
    score('P4c', 'main, I = 1024: worlds with >= 0.99 of islands on fair pairs in >= 18/20 [fewer than 15]', c18,
          '; '.join('%s: %d/20 worlds >= 0.99 on fair pairs' % (lab, world_stats(w)['cons99']) for lab, w, lam in (('P_fail 0', wk, lam0), ('P_fail 0.1', wk1, lam1)) if w))
    # 5
    jobs, e = ends('main|0.1|0', 0.1, 'nat')
    ju, eu = ends('main|0.1|0', 0.1, 'uneq')
    if jobs:
        if not conv_all(jobs):
            st = 'unscored (unresolved)'
        else:
            st = 'held' if min(e) >= 0.95 else ('failed' if min(e) < 0.9 else 'partial')
        score('P5', 'main, P_fail 0.1: V* >= 0.95 at convergence from the natural law [< 0.9]', st,
              'natural %s; unequal tilt %s (gemini-4-argon counter-prediction: < 0.9 from the unequal tilt; gpt-6.1-sol: lower reader marginal, slower conversion)' % (
                  ', '.join('%.5f' % x for x in e), ', '.join('%.5f' % x for x in eu) if eu else 'n/a'))
    # 6
    base = ends('main|0|0', 0.0, 'nat')[1]
    so = ends('ab-So|0|0', 0.0, 'nat')[1]
    dd = ends('ab-D|0|0', 0.0, 'nat')[1]
    if base and so and dd:
        dso = np.mean(base) - np.mean(so)
        ddd = np.mean(base) - np.mean(dd)
        trb = traj_row(r.ode_pools('main|0|0', 0.0, 'nat'))
        trs = traj_row(r.ode_pools('ab-So|0|0', 0.0, 'nat'))
        trd = traj_row(r.ode_pools('ab-D|0|0', 0.0, 'nat'))
        if abs(dso - ddd) < 0.002:
            st = 'partial (the limits do not separate: both drops are 0; at finite time removing the switchers costs more)' if trs[3] < trd[3] else 'partial (the limits do not separate; at finite time the reverse)'
        else:
            st = 'held' if dso > ddd else 'failed'
        score('P6', 'removing switchers lowers the V* limit more than removing two-partner readers [reverse]', st,
              'limit drop: switchers %.5f, two-partner %.5f; V* at 10^3: main %.4f, -So %.4f, -D %.4f; at 10^4: %.4f, %.4f, %.4f' % (dso, ddd, trb[3], trs[3], trd[3], trb[4], trs[4], trd[4]))
    # E1..E3
    t = r.get('V:tables')
    if t:
        score('E1', 'zero forfeit events in the table', 'held' if t['forfeits_total'] == 0 else 'failed', 'forfeits %d' % t['forfeits_total'])
        score('E2', 'exact rotation equivariance', 'held' if t['equiv_total_violations'] == 0 else 'failed', 'violations %d' % t['equiv_total_violations'])
        score('E3', 'failed reads follow the reading graph (constants 0, S and X <= 1, D <= 2, only with a reachable cycle)',
              'held' if (t['nto_const_max'] == 0 and t['nto_single_exploit_max'] <= 1 and t['nto_two_max'] <= 2 and t['cycle_violations'] == 0) else 'failed',
              'max %d / %d / %d, violations %d' % (t['nto_const_max'], t['nto_single_exploit_max'], t['nto_two_max'], t['cycle_violations']))
    # E4
    a = [r.get('P:main|0|0:%d' % p) for p in range(NPOOL)]
    b = [r.get('P:main|0.1|0:%d' % p) for p in range(NPOOL)]
    if all(a) and all(b):
        ra = np.mean([np.mean(p['readers']) for p in a]); rb = np.mean([np.mean(p['readers']) for p in b])
        va = np.mean([p['shares'][0] for p in a]); vb = np.mean([p['shares'][0] for p in b])
        rel = abs(rb - ra) / ra
        st = 'held' if (rel < 0.10 and abs(vb - va) < 0.02) else ('failed' if (rel > 0.25 or abs(vb - va) > 0.02) else 'partial')
        score('E4', 'founding at 0.1 vs 0 changes the post-anneal reader marginal < 10% and V* < 0.02', st, 'reader marginal %.4f -> %.4f (relative %.3f), V* %.4f -> %.4f' % (ra, rb, rel, va, vb))
    # E5
    ps = [r.get('P:main|0|0:%d' % p) for p in range(NPOOL)]
    x = r.get('X:main|0|0:0.0')
    if all(ps):
        sup = [p['support'] for p in ps]
        un = x['support_union'] if x else None
        ok = all(1000 <= s <= 5000 for s in sup)
        bad = any(s < 500 or s > 8000 for s in sup)
        score('E5', 'support per 16,384-pool at main between 1,000 and 5,000 triples; union <= 2x pool', 'held' if (ok and (un is None or un <= 2 * max(sup))) else ('failed' if bad else 'partial'), 'per pool %s, union %s' % (sup, un))
    # E6
    vals = {}
    for P in ('0', '0.03', '0.1'):
        jobs = r.ode_pools('main|%s|0' % P, float(P), 'nat')
        if jobs:
            vals[P] = float(np.mean(vstar_end(jobs)))
    if len(vals) == 3:
        mono = vals['0.1'] <= vals['0.03'] + 0.01 and vals['0.03'] <= vals['0'] + 0.01
        non = (vals['0.1'] > vals['0.03'] + 0.02) or (vals['0.03'] > vals['0'] + 0.02)
        v3 = {P: traj_row(r.ode_pools('main|%s|0' % P, float(P), 'nat'))[3] for P in ('0', '0.03', '0.1')}
        score('E6', 'V*(0.1) <= V*(0.03) <= V*(0) +- 0.01 at main', 'held' if mono else ('failed' if non else 'partial'),
              'V* at the end: ' + ', '.join('%s: %.5f' % (k, v) for k, v in vals.items()) + ' (a vacuous test at the limit); V* at 10^3 events: ' + ', '.join('%s: %.4f' % (k, v) for k, v in v3.items()))
    # E7
    j0 = r.ode_pools('main|0|0', 0.0, 'nat'); j150 = r.ode_pools('main|0|150', 0.0, 'nat')
    if j0 and j150:
        d = abs(np.mean(vstar_end(j150)) - np.mean(vstar_end(j0)))
        t0_, t1_ = traj_row(j0), traj_row(j150)
        score('E7', 'A = 150 within 0.02 of A = 0 (P_fail 0)', 'held' if d < 0.02 else ('failed' if d > 0.05 else 'partial'),
              'V* at the end A=0 %.5f, A=150 %.5f, difference %.5f (vacuous at the limit); V* at 10^3 events %.4f and %.4f, at 10^4 %.4f and %.4f' % (np.mean(vstar_end(j0)), np.mean(vstar_end(j150)), d, t0_[3], t1_[3], t0_[4], t1_[4]))
    # E8
    dv = {}
    for dose in M.DOSES:
        jobs = r.ode_pools('%s|0|0' % dose, 0.0, 'nat')
        if jobs:
            dv[dose] = float(np.mean(vstar_end(jobs)))
    if len(dv) == 4:
        nondec = dv['lo'] >= dv['0'] - 0.01 and dv['hi'] >= dv['main'] - 0.01 and dv['main'] >= dv['0'] - 0.01
        dec = dv['hi'] < dv['main'] - 0.02
        d3 = {dose: traj_row(r.ode_pools('%s|0|0' % dose, 0.0, 'nat'))[3] for dose in M.DOSES}
        score('E8', 'V* limit non-decreasing in the dose at P_fail 0', 'held' if nondec else ('failed' if dec else 'partial'),
              ', '.join('%s: %.5f' % (k, v) for k, v in dv.items()) + ' (a vacuous test at the limit); V* at 10^3 events: ' + ', '.join('%s: %.4f' % (k, v) for k, v in d3.items()))
    # E9
    wj = r.js.get('worlds', {}).get('equal_likelihood')
    if wj:
        score('E9', 'end pairs equally likely (chi-square p >= 0.01)', 'held' if wj['p'] >= 0.01 else 'failed', 'counts %s, chi2 %.2f, p %.3f' % (wj['total'], wj['chi2'], wj['p']))
    r.js['verdicts'] = V
    return out


def sec_verdicts(r):
    r.add('## 12. Verdicts against the registered predictions (predictions/2026-10-29-many-islands-t.md)\n')
    out = verdicts(r)
    r.add(table([(n, c, s, d) for n, c, s, d in out], ['prediction', 'claim [falsifier]', 'verdict', 'numbers']))
    r.add('')


def main():
    outdir = os.path.join(ROOT, 'runs')
    r = R()
    r.tabs = tabs()
    cells, abl = RN.cells_main(), RN.cells_ablation()
    r.add('# The stable-set target in the Turing-complete arm under islands to infinity before time (2026-10-29)\n')
    r.add('Spec `specs/2026-10-29-many-islands-t.md`, predictions `predictions/2026-10-29-many-islands-t.md`, notes `notes/many-islands-t.md`. Generated by `src/many_islands_t_report2.py` from the per-job records.\n')
    sec_validation(r)
    sec_founding(r, cells + abl)
    sec_ode(r, cells + abl)
    sec_classes(r)
    sec_readers(r, cells)
    sec_raw(r, cells)
    sec_jac(r, cells)
    sec_limit(r)
    sec_worlds(r)
    sec_worldsx(r)
    sec_charge(r, cells)
    sec_rates(r, cells)
    sec_ablation(r)
    sec_dsl(r)
    sec_verdicts(r)
    open(os.path.join(outdir, 'many-islands-t.md'), 'w').write('\n'.join(r.md) + '\n')
    json.dump(r.js, open(os.path.join(outdir, 'many-islands-t.json'), 'w'), default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
    os.makedirs(os.path.join(outdir, 'many_islands_t'), exist_ok=True)
    for k, v in r.js.items():
        if k in ('ode', 'raw', 'worlds', 'jacobian', 'rates', 'founding', 'ablations', 'verdicts', 'worldsx', 'limit_composition', 'charge_controls'):
            json.dump(v, open(os.path.join(outdir, 'many_islands_t', k + '.json'), 'w'), default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
    print('wrote runs/many-islands-t.md', len(r.md), 'blocks')


if __name__ == '__main__':
    main()
