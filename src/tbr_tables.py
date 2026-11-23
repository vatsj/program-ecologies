"""Queue 81: tables and registered verdicts from runs/tbr/agg.json and the stage 0 / 1b rows.

Writes runs/tbr/tables.md (included in the report) and runs/tiered-best-response.json (verdicts and tables).
"""
import glob, json, math, os, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOL = 1e-9


def f(x, d=3):
    if x is None:
        return '–'
    if isinstance(x, (list, tuple)):
        if x[0] is None:
            return '–'
        if x[1] is None:
            return ('%.' + str(d) + 'f') % x[0]
        return ('%.' + str(d) + 'f [%.' + str(d) + 'f, %.' + str(d) + 'f]') % tuple(x)
    return ('%.' + str(d) + 'f') % x


def boot_mean(v, rng, B=2000):
    v = np.asarray(v, float)
    if len(v) == 0:
        return [None, None, None]
    bs = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(B)]
    return [float(v.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]


def label(k):
    a, exp, N, lam, mN = k
    if a == 'P':
        return 'P %s mN=%g' % (exp, mN)
    return '%s N=%d Λ=%g mN=%g' % (a, N, lam, mN)


def main():
    rng = np.random.default_rng(8181)
    agg = json.load(open(os.path.join(ROOT, 'runs', 'tbr', 'agg.json')))['cells']
    L = []
    J = dict(tables={}, verdicts={})
    S1 = [k for k, e in agg.items() if (e['key'][0] in 'TM' and e['key'][3] == 100 and e['key'][4] == 1) or
          (e['key'][0] == 'P' and abs(e['key'][4] - 1.091) < 1e-3)]
    order = sorted(agg, key=lambda k: (agg[k]['key'][0], agg[k]['key'][1], agg[k]['key'][2] or 0,
                                       agg[k]['key'][3] if agg[k]['key'][3] is not None else -1, agg[k]['key'][4]))

    # ---------------- joint (unconditional) table
    L.append('### Unconditional joint table at the horizon (every cell)\n')
    L.append('| cell | worlds | diverse | settled islands (≥0.8 / ≥0.95) | settled with E ≠ {p} | vacuous: E = {p} / arrival / T | native regret > 0 (majority / composition) | E_comp = E | repro |')
    L.append('|---|---|---|---|---|---|---|---|---|')
    for k in order:
        e = agg[k]; c = e['counts']
        rp = [x for x in e['repro'] if x is not None]
        L.append('| %s | %d | %s (%d) | %s / %s | %s | %d / %d / %d | %s / %s | %s | %s |' % (
            label(e['key']), c['worlds'], f(c['diverse'], 2), c['n_diverse'], f(c['settled08'], 2), f(c['settled095'], 2),
            f(c['nonemptyE'], 2), c['vacE'], c['vacA'], c['vacT'], f(c['natpos'], 3), f(c.get('natpos_comp'), 3),
            f(c.get('Ecomp_eq_E'), 3), ('%d/%d' % (sum(rp), len(rp))) if rp else 'n/a'))
    J['tables']['joint'] = {label(agg[k]['key']): agg[k]['counts'] for k in order}

    # ---------------- migrant tier tables
    def migtab(title, wk, which, ctls):
        L.append('\n### %s\n' % title)
        hdr = '| cell | runs with cases | cases | residents zero | residents mean | ' + ' | '.join(
            '%s zero | %s mean | %s excess' % (c, c, c) for c in ctls) + ' | empty (%s) |' % '/'.join(ctls)
        L.append(hdr)
        L.append('|' + '---|' * (5 + 3 * len(ctls) + 1))
        for k in order:
            e = agg[k]; b = e.get(wk)
            if b is None:
                continue
            b = b[which]
            if b['n_cases'] == 0:
                continue
            row = '| %s | %d/%d | %d | %s | %s | ' % (label(e['key']), b['n_runs_with_cases'], b['n_runs'], b['n_cases'],
                                                    f(b['res_zero']), f(b['res_mean']))
            row += ' | '.join('%s | %s | %s' % (f(b.get(c + '_zero')), f(b.get(c + '_mean')), f(b.get(c + '_excess')))
                              for c in ctls)
            row += ' | %s |' % '/'.join(str(b.get(c + '_empty', '–')) for c in ctls)
            L.append(row)
    migtab('Migrant tier, diverse worlds, settled islands, residents with zero native regret, T-weighted (σ units; primary)',
           'mig_diverse', 'T', ('pm', 'ar', 'fd'))
    migtab('Migrant tier, diverse worlds, arrival-weighted (payoff units)', 'mig_diverse', 'A', ('pm', 'ar', 'fd'))
    migtab('Migrant tier, diverse worlds, all residents (native regret not required), T-weighted', 'mig_diverse_allres', 'T', ('pm',))
    migtab('Migrant tier, diverse worlds, islands settled at ≥ 0.95, T-weighted', 'mig_diverse_095', 'T', ('pm',))
    migtab('Migrant tier, consensus worlds (non-vacuous cases only), T-weighted', 'mig_consensus', 'T', ('pm', 'ar', 'fd'))

    # ---------------- RE 3 and RE 4 (pooled over stage-1 cells of arms with >= 100 cases)
    def pooled(cells, wk, ctl_key):
        """pool cases over cells by re-weighting each cell's pooled shares by its case count (point estimate) and a
        conservative interval: the case-weighted mean of the cells' interval endpoints."""
        num = den = 0.0; lo = hi = 0.0
        for k in cells:
            b = agg[k][wk]['T']
            ex = b.get(ctl_key)
            if ex is None or ex[0] is None:
                continue
            n = b['n_cases']
            num += n * ex[0]; den += n
            lo += n * (ex[1] if ex[1] is not None else ex[0]); hi += n * (ex[2] if ex[2] is not None else ex[0])
        return (num / den, lo / den, hi / den, int(den)) if den else (None, None, None, 0)
    arms_ok = []
    per_arm = {}
    for a in ('T', 'M', 'P'):
        cells = [k for k in S1 if agg[k]['key'][0] == a]
        n = sum(agg[k]['mig_diverse']['T']['n_cases'] for k in cells)
        per_arm[a] = dict(cells=cells, n=n, pm=pooled(cells, 'mig_diverse', 'pm_excess'),
                          sup=pooled(cells, 'mig_diverse', 'ar_excess' if a != 'P' else 'fd_excess'),
                          fd=pooled(cells, 'mig_diverse', 'fd_excess'))
        if n >= 100:
            arms_ok.append(a)
    allc = [k for a in arms_ok for k in per_arm[a]['cells']]
    pm = pooled(allc, 'mig_diverse', 'pm_excess')
    # supply: arrival control in T/M, founder in P
    num = den = 0.0
    for a in arms_ok:
        x = per_arm[a]['sup']
        if x[0] is not None:
            num += x[3] * x[0]; den += x[3]
    sup = num / den if den else None
    L.append('\n### RE 3 / RE 4 pools (stage 1, diverse worlds, settled, zero native regret, T-weighted)\n')
    L.append('| arm | non-vacuous cases | excess over prior-matched | excess over supply control | excess over founder control |')
    L.append('|---|---|---|---|---|')
    for a in ('T', 'M', 'P'):
        x = per_arm[a]
        L.append('| %s | %d | %s | %s | %s |' % (a, x['n'], f(x['pm'][:3]), f(x['sup'][:3]), f(x['fd'][:3])))
    L.append('| pooled (%s) | %d | %s | %s | |' % ('+'.join(arms_ok), pm[3], f(pm[:3]), f(sup)))
    re3 = 'inconclusive' if pm[3] < 100 else ('holds' if pm[0] >= 0.15 else ('falsified' if pm[0] < 0.05 else 'fails, falsifier not fired'))
    if pm[0] is None or sup is None:
        re4 = 'inconclusive'
    elif sup < 0.5 * pm[0]:
        re4 = 'holds'
    elif sup >= pm[0]:
        re4 = 'falsified'
    else:
        re4 = 'fails, falsifier not fired'
    J['verdicts']['RE3'] = dict(verdict=re3, excess_pm=pm[:3], n=pm[3], arms=arms_ok, per_arm={a: per_arm[a]['pm'] for a in per_arm})
    J['verdicts']['RE4'] = dict(verdict=re4, excess_supply=sup, excess_pm=pm[0], per_arm={a: per_arm[a]['sup'] for a in per_arm})

    # ---------------- stage 2: dose and time tables
    L.append('\n### Stage 2 (N = 200): doses, paired founders; diverse worlds, settled, zero native regret, T-weighted\n')
    L.append('| arm | Λ | mN | worlds diverse 25% / 100% | settled 100% | E ≠ {p} | cases 25% / 50% / 100% | residents zero 25% | 50% | 100% | prior-matched zero 100% | residents mean σ-regret 100% |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
    dose = {}
    for k in order:
        e = agg[k]; a, exp, N, lam, mN = e['key']
        if a in 'TM' and N != 200:
            continue
        if a == 'P' and exp != 'dense':
            continue
        b25 = e['mig_diverse_25']['T']; b50 = (e.get('mig_diverse_50') or {}).get('T'); b100 = e['mig_diverse']['T']
        L.append('| %s | %s | %g | %s / %s | %s | %s | %d / %s / %d | %s | %s | %s | %s | %s |' % (
            a, '–' if lam is None else '%g' % lam, mN, f(e['counts25']['diverse'], 2), f(e['counts']['diverse'], 2),
            f(e['counts']['settled08'], 2), f(e['counts']['nonemptyE'], 2), b25['n_cases'],
            b50['n_cases'] if b50 else '–', b100['n_cases'], f(b25['res_zero']), f(b50['res_zero']) if b50 else '–',
            f(b100['res_zero']), f(b100['pm_zero']), f(b100['res_mean'])))
        dose[(a, lam, mN)] = b100
    # RE 5: mN = 1 vs 0.1 at Lambda = 100 (P: 1.091 vs 0.1)
    re5 = {}
    for a in ('T', 'M', 'P'):
        lam = None if a == 'P' else 100
        hi = dose.get((a, lam, 1.091 if a == 'P' else 1)); lo = dose.get((a, lam, 0.1))
        if hi is None or lo is None or hi['n_cases'] == 0 or lo['n_cases'] == 0:
            re5[a] = None; continue
        re5[a] = dict(hi=hi['res_zero'][0], lo=lo['res_zero'][0], n_hi=hi['n_cases'], n_lo=lo['n_cases'],
                      diff=hi['res_zero'][0] - lo['res_zero'][0])
    tested = {a: v for a, v in re5.items() if v is not None}
    ncase = sum(v['n_hi'] + v['n_lo'] for v in tested.values())
    if not tested or ncase < 100:
        v5 = 'inconclusive' if tested else 'not tested'
    elif all(v['diff'] >= 0.05 for v in tested.values()):
        v5 = 'holds'
    elif all(v['diff'] < 0 for v in tested.values()):
        v5 = 'falsified'
    else:
        v5 = 'fails, falsifier not fired'
    J['verdicts']['RE5'] = dict(verdict=v5, per_arm=re5)

    # RE 6: diverse share, arm T at mN = 1 (stage 1, each N) and mN = 10; arm P dense at its boundary
    t1 = {agg[k]['key'][2]: agg[k]['counts']['diverse'] for k in S1 if agg[k]['key'][0] == 'T'}
    t10 = [agg[k]['counts']['diverse'] for k in agg if agg[k]['key'][0] == 'T' and agg[k]['key'][4] == 10]
    t1_200 = t1.get(200)
    pd = [agg[k]['counts']['diverse'] for k in S1 if agg[k]['key'][0] == 'P' and agg[k]['key'][1] == 'dense']
    if any(v >= 0.5 for v in t1.values()):
        v6 = 'falsified'
    elif all(v < 0.5 for v in t1.values()) and (not t10 or t10[0] < (t1_200 if t1_200 is not None else 1)) and pd and pd[0] > 0.5:
        v6 = 'holds'
    else:
        v6 = 'fails, falsifier not fired'
    J['verdicts']['RE6'] = dict(verdict=v6, T_mN1=t1, T_mN10=t10, P_dense=pd)

    # RE 7: prior tier in consensus worlds at Lambda = 100 (stage 1 cells, T and M)
    L.append('\n### Prior tier (tier 3 inside tier 2), consensus worlds, settled, zero native regret\n')
    L.append('| cell | weighting | cases | residents zero (in tier) | prior-matched zero | excess | residents zero (unconditional) | residents mean | prior-matched mean |')
    L.append('|---|---|---|---|---|---|---|---|---|')
    num = den = 0.0; lo_ = hi_ = 0.0
    for k in order:
        e = agg[k]
        if e['key'][0] == 'P' or 'prior_consensus' not in e:
            continue
        for w in ('T', 'A'):
            b = e['prior_consensus'][w]
            if b['n_cases'] == 0:
                continue
            L.append('| %s | %s | %d | %s | %s | %s | %s | %s | %s |' % (label(e['key']), w, b['n_cases'], f(b['res_zero']),
                     f(b['pm_zero']), f(b['excess']), f(b['res_zero_unc']), f(b['res_mean']), f(b['pm_mean'])))
            if w == 'T' and k in S1 and b['excess'][0] is not None:
                num += b['n_cases'] * b['excess'][0]; den += b['n_cases']
                lo_ += b['n_cases'] * (b['excess'][1] if b['excess'][1] is not None else b['excess'][0])
                hi_ += b['n_cases'] * (b['excess'][2] if b['excess'][2] is not None else b['excess'][0])
    ex7 = num / den if den else None
    if den < 100:
        v7 = 'inconclusive'
    elif abs(ex7) <= 0.05:
        v7 = 'holds'
    elif ex7 >= 0.15:
        v7 = 'falsified'
    else:
        v7 = 'fails, falsifier not fired'
    J['verdicts']['RE7'] = dict(verdict=v7, excess=[ex7, lo_ / den if den else None, hi_ / den if den else None], n=int(den),
                                arr_late={label(agg[k]['key']): agg[k].get('arr_late') for k in order if agg[k]['key'][0] != 'P'})
    L.append('\nShare of tail arrivals after 50% of the horizon (60 N): ' + ', '.join(
        '%s %s' % (label(agg[k]['key']), f(agg[k].get('arr_late'), 4)) for k in order
        if agg[k]['key'][0] != 'P' and agg[k]['key'][3] in (100, 1000) and agg[k]['key'][4] == 1))

    # RE 8: paired change 25% -> 100%, pooled over arms (stage 1 cells)
    diffs = []
    per = {}
    for k in S1:
        d = agg[k]['time_diffs']
        diffs += d
        per[label(agg[k]['key'])] = boot_mean(d, rng) + [len(d)]
    b8 = boot_mean(diffs, rng)
    if len(diffs) == 0:
        v8 = 'not tested'
    elif b8[0] > 0 and b8[1] > 0:
        v8 = 'falsified'
    elif b8[0] <= 0:
        v8 = 'holds'
    else:
        v8 = 'fails, falsifier not fired'
    J['verdicts']['RE8'] = dict(verdict=v8, change=b8, n_runs=len(diffs), per_cell=per)
    L.append('\n### RE 8: paired change in residents\' mean T-regret (σ units), 25% → 100%, runs diverse at both\n')
    L.append('| cell | runs | mean change [95%] |')
    L.append('|---|---|---|')
    for kk, v in per.items():
        L.append('| %s | %d | %s |' % (kk, v[3], f(v[:3])))
    L.append('| pooled | %d | %s |' % (len(diffs), f(b8)))

    # RE 9: routes
    L.append('\n### RE 9: routes of zero-regret residents (settled, non-vacuous, zero native regret), stage 1\n')
    L.append('| arm | residents | (c) taken over | (a) replaced an equivalent | (b) held | (u) other | origin of (c) holders |')
    L.append('|---|---|---|---|---|---|---|')
    v9 = {}
    for a in ('T', 'M', 'P'):
        cnt = {}; org = {}
        for k in S1:
            if agg[k]['key'][0] != a:
                continue
            for r, n in agg[k]['routes']['counts'].items():
                cnt[r] = cnt.get(r, 0) + n
            for r, n in agg[k]['routes']['c_origin'].items():
                org[r] = org.get(r, 0) + n
        n = sum(cnt.values())
        sh = {r: cnt.get(r, 0) / n for r in 'cabu'} if n else {}
        v9[a] = dict(n=n, shares=sh, origin=org)
        L.append('| %s | %d | %s | %s | %s | %s | %s |' % (a, n, *(f(sh.get(r), 3) if n else '–' for r in 'cabu'),
                                                      ', '.join('%s %d' % x for x in sorted(org.items()))))
    nall = sum(v['n'] for v in v9.values())
    if nall < 100:
        r9 = 'inconclusive'
    elif any(v['n'] and v['shares']['a'] >= 0.5 for v in v9.values()):
        r9 = 'falsified'
    elif all(v['shares'].get('a', 0) < 0.25 for v in v9.values() if v['n']):
        r9 = 'holds'
    else:
        r9 = 'fails, falsifier not fired'
    J['verdicts']['RE9'] = dict(verdict=r9, per_arm=v9)

    # ---------------- stage 0
    s0a = [json.loads(l) for l in open(os.path.join(ROOT, 'runs', 'tbr_rows', 'stage0a.jsonl'))]
    s0b = [json.loads(l) for l in open(os.path.join(ROOT, 'runs', 'tbr_rows', 'stage0b.jsonl'))]
    L.append('\n### Stage 0a: N·ρ (10⁵ replicates) against P10\n')
    L.append('| N | σ | N·ρ [95%] | P10 finite-N | exact (event process) | σ/(1 − e^−σ) | P10 in interval |')
    L.append('|---|---|---|---|---|---|---|')
    for r in s0a:
        L.append('| %d | %g | %.3f [%.3f, %.3f] | %.3f | %.3f | %.3f | %s |' % (r['N'], r['sigma'], r['Nrho'], r['Nrho_lo'],
                 r['Nrho_hi'], r['Nrho_p10'], r['Nrho_exact_process'], r['Nrho_asym'], 'yes' if r['p10_in_ci'] else 'no'))
    nin = sum(r['p10_in_ci'] for r in s0a)
    J['verdicts']['RE1'] = dict(verdict='holds' if nin >= 16 else ('falsified' if nin < 14 else 'fails, falsifier not fired'),
                                contained=nin, of=len(s0a))
    L.append('\n### Stage 0b: real testers (2·10⁴ replicates; T exact; sign and error against σ/(1 − e^−σ))\n')
    L.append('| case | N | σ | N·ρ [95%] | asymptote | rel. error | tester established | T exact / Little | σ by Little |')
    L.append('|---|---|---|---|---|---|---|---|---|')
    wrong = []; off = []
    for r in s0b:
        L.append('| %s | %d | %g | %.3f [%.3f, %.3f] | %.3f | %+.2f | %d | %.1f / %.1f | %+.2f |' % (
            r['case'], r['N'], r['sigma'], r['Nrho'], r['Nrho_lo'], r['Nrho_hi'], r['Nrho_asym'], r['rel_err'],
            r['tester_est'], r['T'], r['T_little'], r['sigma_little']))
        if r['case'] in ('rq0.7', 'rq0.9', 'neutral') and abs(r['sigma']) >= 0.5:
            if (r['sigma'] > 0 and r['Nrho'] <= 1) or (r['sigma'] < 0 and r['Nrho'] >= 1):
                wrong.append((r['case'], r['N'], r['sigma'], r['Nrho']))
        if r['case'] in ('rq0.7', 'rq0.9', 'neutral') and abs(r['rel_err']) > 0.40:
            off.append((r['case'], r['N'], r['sigma'], round(r['rel_err'], 2)))
    J['verdicts']['RE2'] = dict(verdict='falsified' if (wrong or off) else 'holds', wrong_sign=wrong, off40=off)

    # ---------------- stage 1b
    for arm in ('T', 'M', 'P'):
        p = os.path.join(ROOT, 'runs', 'tbr_rows', 'stage1b_%s.jsonl' % arm)
        if not os.path.exists(p):
            continue
        rows = [json.loads(l) for l in open(p)]
        L.append('\n### Stage 1b, arm %s: frozen natives, real migrant lineages (N = 200)\n' % arm)
        L.append('| profile (occurrences) | slot | variant class (size) | resident? | σ (P10) | N·ρ [95%] | σ/(1 − e^−σ) | tester est. |')
        L.append('|---|---|---|---|---|---|---|---|')
        agree = 0; tot = 0
        for r in rows:
            L.append('| %s (%d) | %s | %s (%d) | %s | %+.3f | %.3f [%.3f, %.3f] | %.3f | %d |' % (
                r['profile'], r['occ'], r.get('j', 0), r['variant'], r['cls_size'], 'yes' if r['is_resident'] else '',
                r['sigma'], r['Nrho'], r['Nrho_lo'], r['Nrho_hi'], r['Nrho_asym'], r['tester_est']))
            if abs(r['sigma']) >= 0.5:
                tot += 1
                agree += (r['sigma'] > 0) == (r['Nrho'] > 1)
        L.append('\nSign agreement where |σ| ≥ 0.5: %d of %d.' % (agree, tot))
        J['tables']['stage1b_' + arm] = rows

    J['tables']['cells'] = agg
    open(os.path.join(ROOT, 'runs', 'tbr', 'tables.md'), 'w').write('\n'.join(L) + '\n')
    json.dump(J, open(os.path.join(ROOT, 'runs', 'tiered-best-response.json'), 'w'), indent=1, default=float)
    for k, v in J['verdicts'].items():
        print(k, v['verdict'])


if __name__ == '__main__':
    main()
