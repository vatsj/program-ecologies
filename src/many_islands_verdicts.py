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
        pts = [(int(I), ia[I]['first_loss']['km_median']) for I in Is if not nanf(ia[I]['first_loss']['km_median']) and ia[I]['first_loss']['km_median'] > 0]
        bpts = [(int(I), ia[I]['break']['km_median']) for I in Is if not nanf(ia[I]['break']['km_median']) and ia[I]['break']['km_median'] > 0]
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
        # sol's counter-prediction: size dependence of efficiency in the L and M arms
        big = []
        for k, S in R.items():
            if not S.get('comp') or not (k.startswith('L ') or k.startswith('M ')):
                continue
            for C, d in S['comp'].items():
                if int(C) == 1:
                    continue
                for cp in (1000, 10000, 100000):
                    df = d['diff_vs_C1'].get(cp)
                    if df and not nanf(df[1]) and abs(df[0]) - 1.96 * df[1] > 0.05:
                        big.append('%s C=%s @%d: %.3f' % (k, C, cp, df[0]))
        add('7c', 'counter (gpt-6.1-sol): efficiency depends on component size in L / M (some |V* difference| > 0.05, interval excluding 0.05)',
            'held' if big else 'failed', '; '.join(big[:12]) or 'none')
        out = 'held' if (dmax <= 0.05 and (not covs or min(covs) >= 0.9)) else 'failed'
        add('7', 'components agree with one component on V* within 0.05; coverage across components >= 0.9 from C=16 (spec checkpoints)', out, 'max |diff| at 1000 over cells: %.3f; ' % dmax + '; '.join(det))
    return rows


def rate_ratio(a, b):
    return a / b if b else float('nan')


def own_verdicts(R, val=None, rs_all=None):
    """E1-E15 (the RE's own, written after the notes' hand analysis) and the aggregate-stability classification."""
    rows = []

    def add(pid, claim, outcome, detail):
        rows.append(dict(id=pid, claim=claim, outcome=outcome, detail=detail))

    # E1
    if val:
        ev = val['event_formula']
        ok = all(v['inside'] for v in ev.values())
        add('E1', 'closed-form one-migrant kernel agrees with simulated relaxation (and kern draw for draw)', 'held' if ok else 'failed',
            '; '.join('%s: sim %.4f [%.4f, %.4f] vs formula %.4g' % (k, v['simulated'], v['ci'][0], v['ci'][1], v['formula']) for k, v in ev.items()))
    # E2
    S = g(R, 'L', 0)
    if S:
        x1 = S['x1000'][0]; u1 = S['traj']['U'][1000][0]; wd = S['traj']['W'][1000][0] + S['traj']['D'][1000][0]
        ok = 0.30 <= x1 <= 0.50 and u1 >= 0.40 and wd <= 0.03
        add('E2', 'L, A=0: V* at 1000 events in [0.30, 0.50], unequal >= 0.40, W+D <= 0.03', 'held' if ok else 'failed',
            'V* %.3f, U %.3f, W+D %.4f' % (x1, u1, wd))
    # E3
    hs = []
    for arm in ('L', 'M'):
        P = (g(R, arm, 0) or {}).get('post_full')
        if P:
            h = P['heterogeneity']
            ratio = h['W']['mean_exit'] / h['U']['mean_exit']
            hs.append((arm, ratio, h['U']['cv_exit'], h['F']['cv_exit']))
    if hs:
        ok = all(r >= 20 and cu >= 1 and cf >= 1 for _, r, cu, cf in hs)
        bad = all(r < 5 and cu < 0.5 and cf < 0.5 for _, r, cu, cf in hs)
        add('E3', 'exit hazard of U is >= 20x smaller than of W, and CV of per-recipient exit >= 1 for U and F (class chain not Markov)',
            'held' if ok else ('failed' if bad else 'partial'), '; '.join('%s: W/U hazard ratio %.1f, CV(U) %.2f, CV(F) %.2f' % h for h in hs))
    # E4
    S0, S1 = g(R, 'L', 0), g(R, 'L', 150)
    if S0 and S1:
        d = S1['post']['Vstar'][0] - S0['post']['Vstar'][0]
        add('E4', 'annealing lowers the post-anneal V* in L by at least 0.05 (against prediction 4)', 'held' if d <= -0.05 else 'failed',
            'post V* A=150 minus A=0: %.4f' % d)
    # E5
    SR_, SM_ = g(R, 'R', 150), g(R, 'M', 150)
    if SR_ and SM_:
        d = SR_['x1000'][0] - SM_['x1000'][0]
        add('E5', 'readers raise V* over modalPA by >= 0.1 at 1000 events, A=150, and stay below 0.9', 'held' if (d >= 0.1 and SR_['x1000'][0] < 0.9) else 'failed',
            'R %.3f, M %.3f, diff %.3f' % (SR_['x1000'][0], SM_['x1000'][0], d))
    # E6
    if S0 and S0['traj']['U'].get(100000):
        ug = S0['traj']['U'][100000][0] + S0['traj']['G'][100000][0]
        add('E6', 'L, A=0: U + G still >= 0.3 at 1e5 events per island', 'held' if ug >= 0.3 else 'failed', 'U+G %.4f (U %.4f, G %.4f)' % (
            ug, S0['traj']['U'][100000][0], S0['traj']['G'][100000][0]))
    # E7 / E8
    ia = (S0 or {}).get('ia')
    if ia:
        Is = [I for I in sorted(ia.keys(), key=int) if int(I) <= 256]
        pts = [(int(I), ia[I]['first_loss']['km_median']) for I in Is if not nanf(ia[I]['first_loss']['km_median']) and ia[I]['first_loss']['km_median'] > 0]
        bpts = [(int(I), ia[I]['break']['km_median']) for I in Is if not nanf(ia[I]['break']['km_median']) and ia[I]['break']['km_median'] > 0]
        det = 'first-loss medians %s; break medians %s' % (pts, bpts)
        cov256 = ia[256]['cov1000'] if 256 in ia else None
        use = bpts if len(bpts) >= 3 else pts
        if len(use) >= 3:
            sl = slope_loglog([p[0] for p in use], [p[1] for p in use])[0]
            ok = sl < 0.8 and (cov256 is None or cov256[0] == cov256[1])
            add('E7', 'at I <= 256 the first-loss / break time is not linear in I (slope < 0.8) and nothing is lost at 1000 events', 'held' if ok else 'failed',
                'slope %.2f over I=%s; coverage at 1000 for I=256: %s; %s' % (sl, [p[0] for p in use], cov256, det))
        else:
            add('E7', 'at I <= 256 the first-loss / break time is not linear in I', 'partial (too few observed medians)', det)
        devs = {I: ia[I]['dev_from_pool'].get(1000) for I in ia if int(I) >= 256}
        firstok = [int(I) for I in sorted(ia.keys(), key=int) if ia[I]['dev_from_pool'].get(1000) is not None and ia[I]['dev_from_pool'][1000] <= 0.05]
        add('E8', '(2a) V* within 0.05 of the pool value at 1000 events from I = 256 upward', 'held' if all(v is not None and v <= 0.05 for v in devs.values()) else 'failed',
            'deviations %s; sizes within 0.05: %s' % ({I: round(v, 4) for I, v in devs.items() if v is not None}, firstok))
    # E9
    det = []; ok9 = []
    for k, SS_ in R.items():
        P = SS_.get('post_full')
        if not P:
            continue
        tm = P['two_migrant']
        sh = {}
        for lab, nm in P['post_shares'].items():
            pass
        # donor weights: the shares of the five groups
        pg = SS_['post']
        w = {'F': pg['Vstar'][0], 'U': pg['U'][0], 'G': pg['G'][0], 'W': pg['W'][0], 'D': pg['D'][0]}
        seq = ov = 0.0
        for ga in ('U',):
            for gb, wb in w.items():
                c = tm.get('%s>%s' % (ga, gb))
                if c and c['n']:
                    seq += wb * c['seq_toF'] / c['n']; ov += wb * c['ov_toF'] / c['n']
        det.append('%s: U recipients to V*: sequential %.2e, overlapping %.2e' % (k, seq, ov))
        ok9.append(None if seq == 0 or ov == 0 else (ov / seq <= 5))
    if det:
        add('E9', 'overlapping two migrants convert U to V* within a factor 5 of two in sequence', 'held' if all(o is True for o in ok9) else ('partial/undetermined' if any(o is None for o in ok9) else 'failed'), '; '.join(det))
    # E10
    det = []; oks = []
    for k, SS_ in R.items():
        P = SS_.get('post_full')
        if P and 'U' in P['cryptic']:
            r = P['cryptic']['U']['ratio_toF']
            det.append('%s: U to-V* hazard ratio after/before %.2f' % (k, r))
            oks.append((k, r))
    if oks:
        lcell = [r for k, r in oks if k.startswith('L ') and k.endswith('A=0')]
        rcell = [r for k, r in oks if k.startswith('R ')]
        ok = bool(lcell) and 0.7 <= lcell[0] <= 1.4 and (not rcell or max(rcell) > 1.4)
        add('E10', 'cryptic drift: L ratio within [0.7, 1.4]; readers above 1.4', 'held' if ok else 'failed', '; '.join(det))
    # E11
    if val:
        c = val['cost']
        add('E11', 'one L A=0 island <= 0.3 s; annealed A=150 <= 3 s', 'held' if (c['L_A0_island_s'] <= 0.3 and c['L_A150_island_s'] <= 3) else 'failed',
            'L A=0 %.3f s, L A=150 %.3f s, R A=0 %.3f, R A=150 %.3f' % (c['L_A0_island_s'], c['L_A150_island_s'], c['R_A0_island_s'], c['R_A150_island_s']))
    # E12
    det = []; bad = False
    for k, SS_ in R.items():
        P = SS_.get('post_full')
        if P and 'mixed_states' in P:
            m = P['mixed_states']
            det.append('%s: mixed %d, drifting %d of %d' % (k, m['mixed'], m['drifting'], m['n']))
            if m['mixed_share'] > 0.005:
                bad = True
    if det:
        add('E12', 'mixed (polymorphic) islands are <= 0.001 of islands in every cell', 'failed' if bad else 'held', '; '.join(det))
    # E13 and the aggregate-stability classification
    agg = {}
    for k, SS_ in R.items():
        rs = SS_.get('rs', {})
        if not all(t in rs for t in ('rs', 'tiltF0', 'tiltU')):
            continue
        row = {}
        for t in ('rs', 'tiltF0', 'tiltU'):
            tr = rs[t]['traj']
            cp = 30000 if 30000 in tr else max(tr)
            sw = rs[t].get('switching', {}).get(cp)
            row[t] = dict(cp=cp, V=tr[cp]['Vstar'], U=tr[cp]['U'], WD=tr[cp]['W'] + tr[cp]['D'], G=tr[cp]['G'], pairs=tr[cp]['pairs'],
                          switching=sw[0] if sw else None)
        spread = max(max(row[t][q] for t in row) - min(row[t][q] for t in row) for q in ('V', 'U', 'WD', 'G'))
        converged = spread <= 0.02
        st = SS_.get('symtilt', {})
        symrow = {}
        if SS_.get('sym') and 'symtiltF' in st and 'symtiltU' in st:
            for t_, tr_ in (('sym', SS_['sym']), ('symtiltF', st['symtiltF']['traj']), ('symtiltU', st['symtiltU']['traj'])):
                cp_ = 30000 if 30000 in tr_ else max(tr_.keys())
                symrow[t_] = dict(cp=cp_, V=tr_[cp_]['Vstar'], U=tr_[cp_]['U'], WD=tr_[cp_]['W'] + tr_[cp_]['D'], G=tr_[cp_]['G'])
            sym_spread = max(max(symrow[t_][q] for t_ in symrow) - min(symrow[t_][q] for t_ in symrow) for q in ('V', 'U', 'WD', 'G'))
        else:
            sym_spread = None
        sw_last = row['rs']['switching']
        symsw = None
        if SS_.get('sym_switching'):
            lastcp = max(SS_['sym_switching'].keys())
            symsw = SS_['sym_switching'][lastcp][0]
        rate = sw_last if sw_last is not None else symsw
        rate_sym = symsw
        use = rate_sym if rate_sym is not None else rate
        converged_cls = (sym_spread is not None and sym_spread <= 0.02) if sym_spread is not None else converged
        sw_starts = []
        for t_, tr_ in (('sym', None), ('symtiltF', st.get('symtiltF')), ('symtiltU', st.get('symtiltU'))):
            if t_ == 'sym':
                if SS_.get('sym_switching'):
                    sw_starts.append(SS_['sym_switching'][30000 if 30000 in SS_['sym_switching'] else max(SS_['sym_switching'].keys())][0])
            elif tr_ and tr_.get('switching'):
                sw_starts.append(tr_['switching'][30000 if 30000 in tr_['switching'] else max(tr_['switching'].keys())][0])
        lo_sw = min(sw_starts) if sw_starts else use
        if lo_sw is None:
            cls = 'undetermined'
        elif converged_cls and lo_sw >= 1e-5:
            cls = 'unique dynamic equilibrium (shares converge to one vector from every start; islands keep switching)'
        elif converged_cls and lo_sw < 1e-6:
            cls = 'frozen (converged, no switching)'
        elif (not converged_cls) and lo_sw >= 1e-5:
            cls = 'several dynamic equilibria (shares converge within each basin and differ by start; islands keep switching)'
        elif (not converged_cls) and lo_sw < 1e-6:
            cls = 'neutral (start-dependent, no switching)'
        else:
            cls = 'slow / mixed'
        agg[k] = dict(sym_row=symrow, sym_spread=sym_spread, row=row, spread=spread, converged=converged, switching_pool_last=sw_last, switching_sym_last=symsw, classification=cls)
    if agg:
        det = '; '.join('%s: spread %.3f, switching(pool) %s, switching(sym) %s -> %s' % (
            k, v['spread'], ('%.1e' % v['switching_pool_last']) if v['switching_pool_last'] is not None else '-',
            ('%.1e' % v['switching_sym_last']) if v['switching_sym_last'] is not None else '-', v['classification']) for k, v in agg.items())
        l0 = agg.get('L A=0')
        ok = bool(l0 and l0['converged'] and l0['row']['tiltU']['V'] >= 0.95 and l0['classification'].startswith('frozen'))
        add('E13', 'aggregate stability: three starts agree within 0.02, tilt toward U ends at V* >= 0.95, final state frozen (L A=0)', 'held' if ok else 'failed', det)
    # E14
    S = g(R, 'L', 0)
    if S and S.get('sym'):
        last = max(S['sym'].keys())
        sl = S['sym'][last]
        spread = (max(sl['pairs']) - min(sl['pairs'])) / max(np.mean(sl['pairs']), 1e-12)
        brk = {}
        for k_, v in (S.get('union') or {}).items():
            brk['%d' % v['I']] = v['brk']
        for t_, v in S.get('rs', {}).items():
            if t_ == 'rs':
                brk['%d' % v['M']] = v['brk']
        for i_, b in enumerate(S['break']):
            brk['16384 (pool %d)' % i_] = b
        vals = [x for x in brk.values() if not nanf(x)]
        ok = sl['Vstar'] >= 0.99 and spread <= 0.05 and vals and min(vals) >= 3000 and max(vals) <= 30000 and max(vals) / min(vals) < 3
        add('E14', 'symmetric orbit chain (L, A=0): V* >= 0.99 and pairs equal within 5% at the last checkpoint; unsymmetrized pools break between 3e3 and 3e4, growth < 3x',
            'held' if ok else 'failed', 'sym at %d: V* %.4f, relative pair spread %.4f; break times %s' % (last, sl['Vstar'], spread, brk))
    # E15
    det = []; okk = True; cells15 = {}
    for k, SS_ in R.items():
        P = SS_.get('post_full')
        if P and P.get('ka'):
            ka = P['ka']
            kap, alp = ka['kappa_sym'], ka['alpha_sym']
            cells15[k] = (kap[0], alp[0])
            pos = (not nanf(alp[1])) and alp[1] > 0 and kap[1] > 0
            ratio = alp[0] / kap[0] if kap[0] else float('nan')
            det.append('%s: kappa %.2e, alpha %.2e (alpha interval %s 0), alpha/kappa %.3f' % (k, kap[0], alp[0], 'excludes' if pos else 'includes', ratio))
            if not pos:
                okk = False
            if (k.startswith('L ') or k.startswith('M ')) and not (0.05 <= ratio <= 0.5):
                okk = False
    for A in (0, 150):
        if ('R A=%d' % A) in cells15 and ('M A=%d' % A) in cells15:
            f = cells15['R A=%d' % A][0] / cells15['M A=%d' % A][0]
            det.append('readers/M kappa factor at A=%d: %.2f' % (A, f))
            if f < 3:
                okk = False
    if det:
        add('E15', 'alpha > 0 and kappa > 0 everywhere; alpha/kappa in [0.05, 0.5] in L and M; readers >= 3x kappa', 'held' if okk else 'failed', '; '.join(det))
    return rows, agg
