"""Scores the registered predictions of predictions/2026-10-25-many-islands.md against the report data (the dict R built by
many_islands_report.build).  Every rule is the one written in the predictions file before the counted cells."""
import os, sys, json, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import many_islands as MI
import many_islands_report as RP


def g(R, arm, A):
    return R.get('%s A=%d' % (arm, A))


def nanf(x):
    return x is None or (isinstance(x, float) and math.isnan(x))


def slope_loglog(xs, ys):
    xs = np.log(np.asarray(xs, float)); ys = np.log(np.asarray(ys, float))
    if len(xs) < 2:
        return float('nan'), float('nan'), float('nan')
    A_ = np.vstack([xs, np.ones_like(xs)]).T
    sol, res, rk, sv = np.linalg.lstsq(A_, ys, rcond=None)
    return float(sol[0]), float('nan'), float('nan')


def boot_slope(xs, ys, rng, n=2000):
    xs = np.asarray(xs, float); ys = np.asarray(ys, float)
    out = []
    for _ in range(n):
        idx = rng.integers(0, len(xs), len(xs))
        if len(set(xs[idx])) < 2:
            continue
        out.append(slope_loglog(xs[idx], ys[idx])[0])
    return float(np.quantile(out, 0.025)), float(np.quantile(out, 0.975))


def verdicts(R, validate_json=None, pool_walls=None):
    rows = []

    def add(pid, claim, outcome, detail):
        rows.append(dict(id=pid, claim=claim, outcome=outcome, detail=detail))

    # ---- P1: fair block antisymmetric part
    det = []; held = True; undecided = False
    for arm in ('L', 'M', 'R'):
        for A in (0, 150):
            S = g(R, arm, A)
            if not S or not S.get('post_full'):
                continue
            D = S['post_full']['fair_block']['D']
            inside = [(d[1] <= 0 <= d[2]) if not nanf(d[1]) else None for d in D]
            if any(v is None for v in inside):
                undecided = True
            elif not all(inside):
                held = False
            det.append('%s A=%d: %s' % (arm, A, ', '.join('%.2e [%.2e, %.2e]' % tuple(d) for d in D)))
    add('1', 'antisymmetric fair-to-fair net flows are zero within their intervals (L, M, R)',
        'held' if held and not undecided else ('partial (intervals undefined)' if held else 'failed'), '; '.join(det))
    # ---- P2: coverage in the limit
    det = []; sym_ok = True; pools_x1000 = True; pools_inf = True; anysym = False
    for k, S in R.items():
        c1000 = S['cov'].get(1000); cinf = S['cov'].get(100000)
        s_last = None
        if 'sym' in S:
            anysym = True
            last = max(S['sym'].keys())
            s_last = S['sym'][last]
            if min(s_last['pairs']) <= 1e-3:
                sym_ok = False
        if c1000 and c1000['covered'] < c1000['pools']:
            pools_x1000 = False
        if cinf and cinf['covered'] < cinf['pools']:
            pools_inf = False
        det.append('%s: pools covered at 1e3 %s, at 1e5 %s; symmetric chain smallest pair at %s: %s' % (
            k, '%d/%d' % (c1000['covered'], c1000['pools']) if c1000 else '-', '%d/%d' % (cinf['covered'], cinf['pools']) if cinf else '-',
            max(S['sym'].keys()) if 'sym' in S else '-', '%.4f' % min(s_last['pairs']) if s_last else '-'))
    if anysym and sym_ok and pools_x1000 and not pools_inf:
        out = 'partial: holds on the symmetric manifold and at the spec checkpoints; fails in every finite pool by 10^5 events per island (symmetry breaking)'
    elif anysym and sym_ok and pools_x1000 and pools_inf:
        out = 'held'
    else:
        out = 'failed'
    add('2', 'all three fair pairs keep positive shares in (2b), every arm', out, '; '.join(det))
    # ---- P3
    S = g(R, 'L', 0)
    if S:
        x1, xi = S['x1000'], S['xinf']
        out = 'held at the spec horizon, failed at long times' if (x1[0] < 0.6 and xi and xi[0] >= 0.9) else ('held' if x1[0] < 0.6 and (not xi or xi[0] < 0.6) else ('failed' if x1[0] >= 0.9 or (xi and xi[0] >= 0.9) else 'partial'))
        add('3', 'L, A=0: V* share stays below 0.6 (failed if >= 0.9)', out,
            'x1000 %.3f, x1e4 %.3f, xinf(1e5) %.3f (converged: %s)' % (x1[0], S['x1e4'][0], xi[0] if xi else float('nan'), S['xinf_converged']))
    # ---- P4
    S0, S1 = g(R, 'L', 0), g(R, 'L', 150)
    if S0 and S1:
        d = S1['post']['Vstar'][0] - S0['post']['Vstar'][0]
        xi = S1['xinf'][0] if S1['xinf'] else float('nan')
        out = 'held' if (d >= 0.1 and xi < 0.9) else ('failed' if (d < 0.0 or xi >= 0.9) else 'partial')
        add('4', 'L: A=150 raises the post-anneal V* by >= 0.1 over A=0, limit below 0.9', out,
            'post V* A=0 %.3f, A=150 %.3f (diff %.3f); x1000 %.3f / %.3f; xinf(A=150) %.3f' % (
                S0['post']['Vstar'][0], S1['post']['Vstar'][0], d, S0['x1000'][0], S1['x1000'][0], xi))
    # ---- P5
    SR_, SM_ = g(R, 'R', 150), g(R, 'M', 150)
    if SR_:
        x1, xi = SR_['x1000'][0], (SR_['xinf'][0] if SR_['xinf'] else float('nan'))
        covok = SR_['cov'].get(1000, {}).get('covered', 0) == SR_['cov'].get(1000, {}).get('pools', -1)
        out = 'held' if (x1 >= 0.9 and xi >= 0.9 and covok) else ('failed' if (x1 < 0.9 and (nanf(xi) or xi < 0.9)) else 'partial')
        add('5', 'readers, A=150: (2b) V* >= 0.9 with coverage', out, 'x1000 %.3f, xinf %.3f, coverage@1000 %s' % (x1, xi, covok))
        cout = 'held' if (x1 < 0.75 and (nanf(xi) or xi < 0.75)) else ('failed' if (x1 >= 0.75 and (not nanf(xi) and xi >= 0.75)) else 'partial')
        add('5c', 'counter (gemini-4-argon): V* stays below 0.75 with readers', cout, 'x1000 %.3f, xinf %.3f' % (x1, xi))
    # ---- P6
    slopes = {}
    for k, S in R.items():
        ia = S.get('ia')
        if not ia:
            continue
        Is = sorted(ia.keys(), key=lambda v: int(v))
        pts = [(int(I), ia[I]['first_loss']['km_median']) for I in Is if not nanf(ia[I]['first_loss']['km_median'])]
        bpts = [(int(I), ia[I]['break']['km_median']) for I in Is if not nanf(ia[I]['break']['km_median'])]
        cov = ia[Is[-1]]['cov1000']
        rec = dict(first_loss_pts=pts, break_pts=bpts, cov_largest=cov, I_largest=int(Is[-1]))
        if len(pts) >= 3:
            sl = slope_loglog([p[0] for p in pts], [p[1] for p in pts])[0]
            lo, hi = boot_slope([p[0] for p in pts], [p[1] for p in pts], np.random.default_rng(1))
            rec['slope'] = (sl, lo, hi)
        if len(bpts) >= 3:
            sl = slope_loglog([p[0] for p in bpts], [p[1] for p in bpts])[0]
            lo, hi = boot_slope([p[0] for p in bpts], [p[1] for p in bpts], np.random.default_rng(2))
            rec['break_slope'] = (sl, lo, hi)
        slopes[k] = rec
    if slopes:
        det = []
        outs = []
        for k, rec in slopes.items():
            c = rec['cov_largest']
            cl = (c[0] / c[1]) >= 0.9
            if 'slope' in rec:
                sl, lo, hi = rec['slope']
                lin = hi >= 0.8
                outs.append(lin and cl)
                det.append('%s: first-loss slope %.2f [%.2f, %.2f] over I=%s; break slope %s; coverage at I=%d @1000: %d/%d' % (
                    k, sl, lo, hi, [p[0] for p in rec['first_loss_pts']],
                    ('%.2f [%.2f, %.2f]' % rec['break_slope']) if 'break_slope' in rec else '-', rec['I_largest'], c[0], c[1]))
            else:
                outs.append(None)
                det.append('%s: first-loss median undefined for fewer than 3 sizes (censored); break points %s; coverage at I=%d @1000: %d/%d' % (
                    k, rec['break_pts'], rec['I_largest'], c[0], c[1]))
        if all(o is True for o in outs):
            out = 'held'
        elif any(o is False for o in outs):
            out = 'failed (sublinear growth in first-loss / break time with I)' if any('slope' in r for r in slopes.values()) else 'failed'
        else:
            out = 'partial (censored)'
        add('6', 'first loss of a fair pair grows at least linearly in I; coverage at I=4096 held in >= 0.9 of runs at 1000 events/island', out, ' | '.join(det))
    # ---- P7 and counter
    det = []; dmax = 0.0; covs = []
    for k, S in R.items():
        c = S.get('comp')
        if not c:
            continue
        for C, d in c.items():
            if int(C) == 1:
                continue
            df = d['diff_vs_C1'].get(1000)
            if df:
                dmax = max(dmax, abs(df[0]))
            cv = d['cov'].get(1000)
            if int(C) >= 16 and cv:
                covs.append(cv[0] / cv[1])
            det.append('%s C=%s: diff@1000 %s, diff@1e4 %s, coverage@1000 %s, @1e4 %s' % (
                k, C, '%.3f' % df[0] if df else '-', '%.3f' % d['diff_vs_C1'][10000][0] if 10000 in d['diff_vs_C1'] else '-',
                '%d/%d' % tuple(cv) if cv else '-', '%d/%d' % tuple(d['cov'][10000]) if 10000 in d['cov'] else '-'))
    if det:
        out = 'held' if (dmax <= 0.05 and (not covs or min(covs) >= 0.9)) else 'failed'
        add('7', 'components agree with one component on V* within 0.05; coverage across components >= 0.9 from C=16 (spec checkpoints)', out, '; '.join(det))
    return rows
