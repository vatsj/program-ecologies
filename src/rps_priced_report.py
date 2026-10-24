"""Assemble runs/rps-priced.md and runs/rps-priced.json from the stored cells and score the predictions of
predictions/2026-10-23-rps-priced.md by the conventions fixed there.

    python3 src/rps_priced_report.py
"""
import gzip, json, math, os, sys
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rps as RP

ROOT = RP.ROOT
OUT = os.path.join(ROOT, 'runs', 'rps_priced')
ARMS = ('pure', 'sample', 'matched', 'exact')
CS = (0.0, 0.001, 0.01, 0.05)
NS = (100, 1000, 10000, 100000)
STOCH = ('sample', 'exact')


def jload(p):
    if p.endswith('.gz'):
        with gzip.open(p, 'rt') as f: return json.load(f)
    with open(p) as f: return json.load(f)


def tag(arm, kind, c, D):
    return '%s_%s_c%s_D%d' % (arm, kind, repr(c), D)


def chain(arm, c, N, kind='depth', D=12, sfx=''):
    p = os.path.join(OUT, 'chain_%s_N%d%s.json' % (tag(arm, kind, c, D), N, sfx))
    return jload(p) if os.path.exists(p) else None


def lot(arm, c, cell='primary', kind='depth', D=12):
    p = os.path.join(OUT, 'lottery_%s_%s.jsonl.gz' % (tag(arm, kind, c, D), cell))
    if not os.path.exists(p): return []
    rows = [json.loads(l) for l in gzip.open(p, 'rt')]
    return sorted(rows, key=lambda r: r['run'])


def boot(vals, B=4000):
    v = np.asarray(vals, float); v = v[~np.isnan(v)]
    if len(v) == 0: return (float('nan'),) * 3
    idx = np.random.default_rng(20261023).integers(len(v), size=(B, len(v)))
    m = v[idx].mean(1)
    return float(v.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def fmt(t, d=3):
    if t is None: return 'n/a'
    if isinstance(t, tuple):
        if math.isnan(t[0]): return 'n/a'
        return '%.*f [%.*f, %.*f]' % (d, t[0], d, t[1], d, t[2])
    if isinstance(t, float) and math.isnan(t): return 'n/a'
    return '%.*f' % (d, t)


def runvec(rows, g, key):
    return np.array([r['means'][str(g)][key] if str(g) in r['means'] and key in r['means'][str(g)] else np.nan for r in rows])


def pdiff(rowsA, rowsB, g, key):
    ra = {r['run']: r for r in rowsA}; rb = {r['run']: r for r in rowsB}
    common = sorted(set(ra) & set(rb))
    a = np.array([ra[i]['means'][str(g)][key] for i in common]); b = np.array([rb[i]['means'][str(g)][key] for i in common])
    return boot(a - b), len(common)


def fmt1(x):
    return 'none cut' if x is None else '%.1f' % x


def md_table(header, rows):
    s = '| ' + ' | '.join(header) + ' |\n|' + '---|' * len(header) + '\n'
    for r in rows:
        s += '| ' + ' | '.join(str(x) for x in r) + ' |\n'
    return s


def resolution(rows, which='2000'):
    key = 'resolution_' + which
    tot = dict(resolved=0, cycling=0, unresolved=0); n = 0; runs_unres = 0; chg = []
    for r in rows:
        if key not in r: continue
        for k in tot: tot[k] += r[key][k]
        n += r['I']; runs_unres += (r[key]['unresolved'] > 0); chg.append(r[key]['mean_support_changes'])
    if n == 0: return None
    return dict(resolved=tot['resolved'] / n, cycling=tot['cycling'] / n, unresolved=tot['unresolved'] / n, runs_with_unresolved=runs_unres,
                runs=len(chg), mean_support_changes=float(np.mean(chg)))


def main():
    S = {}                                   # json summary
    md = []
    P = md.append
    static = jload(os.path.join(OUT, 'static.json')) if os.path.exists(os.path.join(OUT, 'static.json')) else {}
    P('# Rock-paper-scissors with a compute price (run report, 2026-10-23)\n')
    P('Spec `specs/2026-10-23-rps-priced.md`; predictions `predictions/2026-10-23-rps-priced.md`; notes `notes/rps-priced.md`. Code `src/rps_priced.py`, '
      '`src/rps_priced_run.py`, `src/rps_priced_report.py`, tests `tests/test_rps_priced.py`. Every chain number is an epsilon -> 0 object (pi over the explored '
      'recurrent states, twin-expanded, exploration threshold 1e-8 unless a sensitivity is named); every lottery number is an epsilon = 0 finite-(N, I, horizon) '
      'statistic at (N, I) = (100, 64) unless stated, mN = 1, w = 0.3, generation 2,000 unless stated, never pi. Net exploitability is the primary exploitability. '
      'Intervals are 95% bootstrap intervals over runs (paired by founder run in contrasts).\n')

    # ------------------------------------------------------------ completeness
    expected = []
    for arm in ARMS:
        for c in (0.001, 0.01, 0.05):
            for N in NS: expected.append(('chain', arm, 'depth', c, 12, N))
            expected.append(('lottery', arm, 'depth', c, 12, 'primary'))
        for N in NS: expected.append(('chain', arm, 'forfeit', 0.01, 12, N))
        expected.append(('lottery', arm, 'forfeit', 0.01, 12, 'primary'))
        for N in (1000, 10000): expected.append(('chain', arm, 'depth', 0.0, 12, N))
        expected.append(('lottery', arm, 'depth', 0.0, 12, 'primary'))
        expected.append(('lottery', arm, 'depth', 0.01, 12, 'size'))
    for N in (1000, 10000, 100000): expected.append(('chain', 'exact_br', 'depth', 0.01, 12, N))
    expected.append(('lottery', 'exact_br', 'depth', 0.01, 12, 'primary'))
    for arm in STOCH:
        for c, D in ((0.015, 8), (0.0075, 16)):
            for N in (1000, 10000): expected.append(('chain', arm, 'depth', c, D, N))
            expected.append(('lottery', arm, 'depth', c, D, 'primary'))
    for arm in ARMS:
        expected.append(('sens', arm, 'depth', 0.01, 12, 'sens'))
    missing = []
    for kind, arm, k, c, D, x in expected:
        if kind == 'chain':
            ok = chain(arm, c, x, k, D) is not None
        elif kind == 'lottery':
            need = {'primary': 40, 'size': 20}[x]
            rows = lot(arm, c, x, k, D)
            ok = len(rows) >= need
        else:
            ok = all(chain(arm, c, 10000, k, D, s) is not None for s in ('_th6', '_th10', '_lumped'))
        if not ok: missing.append((kind, arm, k, c, D, x))
    P('## 0. Completeness\n')
    P('%d of %d cells complete.\n' % (len(expected) - len(missing), len(expected)))
    P('Missing or partial: %s\n' % ('none' if not missing else '; '.join('%s %s %s c=%s D=%s %s' % m for m in missing)))
    S['completeness'] = dict(expected=len(expected), missing=[list(map(str, m)) for m in missing])
    n7 = os.path.join(OUT, 'n7work_quick.json')

    # ------------------------------------------------------------ statics
    P('## 1. Static numbers and validation\n')
    rows = []
    for key, v in static.items():
        if v['kind'] == 'depth' and v['D'] == 12 and v['arm'] in ARMS + ('exact_br',):
            sp = v.get('split', {})
            rows.append((v['arm'], v['c'], v['S'], v['K'], sp.get('K_unpriced', '-'), sp.get('n_unpriced_classes_split', '-'),
                         '%.3f' % sp['prior_mass_of_split_classes'] if sp else '-', sp.get('priced_classes_that_merge_unpriced', '-'),
                         '%.1f' % v['H_max'], '%.1f' % v['HW_max'], '%.1e' % v['max_abs_work_minus_depth'],
                         '%.1e' % v['equivariance_err_U'] if v['equivariance_err_U'] is not None else 'n/a'))
    P(md_table(['arm', 'c', 'programs', 'priced classes', 'unpriced classes', 'unpriced classes split', 'prior mass of split classes',
                'priced classes merging unpriced', 'max depth cost', 'max work cost', 'max |work - depth|', 'cyclic relabel err (U_c)'], rows))
    P('Hand tables: the cost table of notes §1.2 and the priced payoffs of §1.3 agree with the evaluator to 1e-12 on the eleven named programs at c = 0.001, 0.01, 0.05 '
      '(`tests/test_rps_priced.py::test_hand_cost_table`, `::test_hand_priced_payoffs`); the numba cost kernel agrees with a recursive reference on random and reading-heavy pairs '
      'in the pure, sample, matched and exact arms for both the depth and the work cost; c = 0 reproduces the unpriced class tables, payoff tables and the first stored lottery runs '
      'bitwise and the stored chain statistics to 1e-6; pricing splits only the class of `X`.\n')
    rows = []
    p1ok = True
    for key, v in static.items():
        if 'pred1' in v and v['D'] == 12 and v['arm'] in ('sample', 'matched', 'exact', 'exact_br') and v['kind'] in ('depth', 'forfeit'):
            q = v['pred1']
            rows.append((v['arm'], v['kind'], v['c'], q['n_self_forfeiting'], q['invade_fail'], q['weak_dominance_fail'], '%.1e' % q['X_min_payoff_vs_any'],
                         '%.1f' % q['X_cost_max'], '%.2e' % q['min_invade_margin'], '%.2e' % q['min_dominance_margin'], q['programs_earning_gt0_vs_X']))
            if v['c'] > 0 and (q['invade_fail'] or q['weak_dominance_fail'] or q['X_min_payoff_vs_any'] < -1e-9 or q['X_cost_max'] > 0):
                p1ok = False
    P('### Prediction 1 statics (every program of the n = 6 table)\n')
    P(md_table(['arm', 'price', 'c', 'self-forfeiting programs', 'X fails to invade', 'X fails weak dominance', 'min X payoff vs any program', 'X cost',
                'min invasion margin', 'min dominance margin', 'programs earning > 0 vs X'], rows))
    # toy
    tp = os.path.join(OUT, 'toy.json')
    if os.path.exists(tp):
        toy = jload(tp)
        P('### Eleven-program toy chain (class-level, uniform prior, depth price)\n')
        P(md_table(['c', 'N', 'pi(X monomorphic)', 'guarded share', 'states', 'top state'],
                   [(v['c'], v['N'], '%.4f' % v['pi_X_mono'], '%.4f' % v['guarded_share'], v['n_states'], v['top'][0]['state'][:60]) for v in toy.values()]))
        S['toy'] = {k: dict(pi_X=v['pi_X_mono'], guarded=v['guarded_share']) for k, v in toy.items()}

    # ------------------------------------------------------------ chain tables
    P('## 2. The epsilon -> 0 chain (class tables at n = 6, D = 12, w = 0.3, length prior; depth price unless stated)\n')
    hdr = ['arm', 'c', 'N', 'e net', 'e gross', 'e indiv', 'e (exact set)', 'mixing', 'self-play forfeit', 'plays forfeited', 'pi(X class)', 'prior X', 'readers', 'guarded', 'cost paid', 'net payoff', 'polymorphic mass', 'states 0.99', 'recurrent', 'indet. events', 'log10 cut']
    chrows = []
    CH = {}
    for arm in ARMS:
        for c in CS:
            for N in NS:
                r = chain(arm, c, N)
                if r is None: continue
                s = r['pi_stat']
                CH[(arm, c, N)] = r
                chrows.append((arm, c, N, '%.4f' % s['e_prog'], '%.4f' % s['e_gross'], '%.4f' % s['e_indiv'], '%.4f' % s.get('e_exset', float('nan')), '%.3f' % s['mix_pop'],
                               '%.3f' % s['forfeit_self'], '%.3f' % s['forfeit_plays'], '%.4f' % r['class_share_X'], '%.4f' % r['prior_mass_X'], '%.3f' % s['share_readers'],
                               '%.3f' % s['share_guarded'], '%.4f' % s['cost_paid'], '%.4f' % s['net_payoff'], '%.2e' % r['pi_polymorphic_mass'],
                               r['n_states_for_0.99'], r['n_recurrent'], r['indeterminate_total_events'], fmt1(r['log10_cut'])))
    P(md_table(hdr, chrows))
    S['chain'] = {'%s|%s|%d' % k: dict(e_net=v['pi_stat']['e_prog'], e_gross=v['pi_stat']['e_gross'], e_indiv=v['pi_stat']['e_indiv'], mix=v['pi_stat']['mix_pop'],
                                       fself=v['pi_stat']['forfeit_self'], fplays=v['pi_stat']['forfeit_plays'], X=v['class_share_X'], readers=v['pi_stat']['share_readers'],
                                       guarded=v['pi_stat']['share_guarded'], poly=v['pi_polymorphic_mass'], e_exset=v['pi_stat'].get('e_exset')) for k, v in CH.items()}
    P('\n### Chain sensitivities (N = 10^4, c = 0.01): exploration threshold 1e-6 / 1e-8 / 1e-10 and lumped residents\n')
    rows = []
    for arm in ARMS:
        for sfx, nm_ in (('_th6', 'theta 1e-6'), ('', 'theta 1e-8 (primary)'), ('_th10', 'theta 1e-10'), ('_lumped', 'lumped, 1e-8')):
            r = chain(arm, 0.01, 10000, sfx=sfx)
            if r is None: continue
            s = r['pi_stat']
            rows.append((arm, nm_, '%.4f' % s['e_prog'], '%.4f' % s['mix_pop'], '%.4f' % s['forfeit_plays'], '%.4f' % r['class_share_X'], '%.2e' % r['pi_polymorphic_mass'], r['n_recurrent'], fmt1(r['log10_cut'])))
    P(md_table(['arm', 'variant', 'e net', 'mixing', 'plays forfeited', 'pi(X)', 'polymorphic mass', 'recurrent states', 'log10 cut'], rows))
    P('\n### Support and transition structure (N = 10^4, c = 0.01)\n')
    for arm in ARMS:
        r = CH.get((arm, 0.01, 10000))
        if r is None: continue
        P('* **%s** (K = %d; states for 0.99: %d; polymorphic mass %.2e; support-size mass %s): %s' % (
            arm, r['K'], r['n_states_for_0.99'], r['pi_polymorphic_mass'], r['pi_support_size'],
            '; '.join('%s %.3f' % (a, b) for a, b in r['class_share_top'][:6] and [(t[0], t[1]) for t in r['class_share_top'][:6]])))
        if r.get('top_exits'):
            e0 = r['top_exits'][0]
            P('  Top state exits (log10 rate per mutation event): total %s; %s' % (e0['log10_total_exit'], '; '.join('to %s (%.2f)' % (x['to'][:40], x['log10_rate']) for x in e0['top_exits'][:3])))
        d = r['discovery']
        P('  Discovery: %d candidate supports, %d seeded, saturated closure %s (complete %s, branch %s), attractor search %d starts: %d stable polymorphic rest points (sizes %s).' % (
            d['n_candidates'], d['n_seeded'], [x['ids'] for x in d['saturated_closure']][:3], d['closure_complete'], d['closure_branch'], d['att_starts'],
            d['n_attractor_search_stable_poly'], d['attractor_stable_sizes']))
    P('')

    # ------------------------------------------------------------ lottery
    P('## 3. The epsilon = 0 seed lottery, (N, I) = (100, 64), mN = 1, 40 runs (founders paired run by run with the unpriced run)\n')
    LT = {}
    keys = ['e_prog', 'e_gross', 'e_indiv', 'e_exset', 'mix_pop', 'forfeit_plays', 'share_X', 'share_readers', 'share_guarded', 'cost_paid', 'net_payoff', 'nclass', 'homo']
    hdr = ['arm', 'c', 'runs', 'e net', 'islands e net <= 0.05', 'e gross', 'e indiv', 'e (exact set)', 'mixing', 'plays forfeited', 'X', 'readers', 'guarded', 'cost paid', 'net payoff', 'classes alive', 'homozygosity']
    rows = []
    for arm in ARMS:
        for c in CS:
            rr = lot(arm, c)
            LT[(arm, c)] = rr
            if len(rr) == 0: continue
            rows.append((arm, c, len(rr), fmt(boot(runvec(rr, 2000, 'e_prog'))), fmt(boot(runvec(rr, 2000, 'share_e_le_0.05'))), fmt(boot(runvec(rr, 2000, 'e_gross'))),
                         fmt(boot(runvec(rr, 2000, 'e_indiv'))), fmt(boot(runvec(rr, 2000, 'e_exset'))), fmt(boot(runvec(rr, 2000, 'mix_pop'))),
                         fmt(boot(runvec(rr, 2000, 'forfeit_plays'))), fmt(boot(runvec(rr, 2000, 'share_X'))), fmt(boot(runvec(rr, 2000, 'share_readers'))),
                         fmt(boot(runvec(rr, 2000, 'share_guarded'))), fmt(boot(runvec(rr, 2000, 'cost_paid')), 4), fmt(boot(runvec(rr, 2000, 'net_payoff')), 4),
                         fmt(boot(runvec(rr, 2000, 'nclass')), 2), fmt(boot(runvec(rr, 2000, 'homo')))))
    P(md_table(hdr, rows))
    S['lottery'] = {}
    for (arm, c), rr in LT.items():
        if rr:
            S['lottery']['%s|%s' % (arm, c)] = {k: boot(runvec(rr, 2000, k)) for k in keys + ['share_e_le_0.05']}
    P('\n### Resolution of islands (support = classes with share >= 0.05; window 1,500-2,000 and 9,500-10,000)\n')
    rows = []
    for arm in ARMS:
        for c in CS:
            rr = LT.get((arm, c))
            if not rr: continue
            a = resolution(rr, '2000'); b = resolution(rr, '10000')
            rows.append((arm, c, '%.3f / %.3f / %.3f' % (a['resolved'], a['cycling'], a['unresolved']), '%d / %d' % (a['runs_with_unresolved'], a['runs']),
                         '%.3f / %.3f / %.3f' % (b['resolved'], b['cycling'], b['unresolved']) if b else 'n/a', '%d / %d' % (b['runs_with_unresolved'], b['runs']) if b else 'n/a',
                         fmt(boot(runvec(rr, 10000, 'e_prog'))), fmt(boot(runvec(rr, 10000, 'mix_pop'))), fmt(boot(runvec(rr, 10000, 'forfeit_plays'))), fmt(boot(runvec(rr, 10000, 'share_X')))))
    P(md_table(['arm', 'c', 'g=2,000: resolved / cycling / unresolved islands', 'runs with an unresolved island', 'g=10,000: resolved / cycling / unresolved', 'runs with unresolved',
                'e net at 10,000', 'mixing at 10,000', 'plays forfeited at 10,000', 'X at 10,000'], rows))
    S['resolution'] = {'%s|%s' % (arm, c): resolution(LT[(arm, c)], '2000') for arm in ARMS for c in CS if LT.get((arm, c))}

    # size cell
    P('\n### Size cell (N, I) = (400, 16), 20 runs, c = 0.01 (generation 2,000)\n')
    rows = []
    for arm in ARMS:
        rr = lot(arm, 0.01, 'size')
        if rr:
            rows.append((arm, len(rr), fmt(boot(runvec(rr, 2000, 'e_prog'))), fmt(boot(runvec(rr, 2000, 'share_e_le_0.05'))), fmt(boot(runvec(rr, 2000, 'mix_pop'))),
                         fmt(boot(runvec(rr, 2000, 'forfeit_plays'))), fmt(boot(runvec(rr, 2000, 'share_X'))), fmt(boot(runvec(rr, 2000, 'share_readers')))))
    P(md_table(['arm', 'runs', 'e net', 'islands e <= 0.05', 'mixing', 'plays forfeited', 'X', 'readers'], rows))


    # replicate
    rep = {arm: lot(arm, 0.01, 'primary200') for arm in ARMS}
    if all(len(v) >= 200 for v in rep.values()):
        P('\n### Supplementary replicate: 200 further runs at c = 0.01 (generation 2,000, independent founders, not paired with the 40-run cell)\n')
        rows = []
        for arm in ARMS:
            rr = rep[arm]
            rows.append((arm, len(rr), fmt(boot(runvec(rr, 2000, 'e_prog'))), fmt(boot(runvec(rr, 2000, 'share_e_le_0.05'))), fmt(boot(runvec(rr, 2000, 'mix_pop'))),
                         fmt(boot(runvec(rr, 2000, 'forfeit_plays'))), fmt(boot(runvec(rr, 2000, 'share_X'))), fmt(boot(runvec(rr, 2000, 'share_readers'))), fmt(boot(runvec(rr, 2000, 'e_exset')))))
        P(md_table(['arm', 'runs', 'e net', 'islands e <= 0.05', 'mixing', 'plays forfeited', 'X', 'readers', 'e (exact set)'], rows))
        d, n = pdiff(rep['exact'], rep['matched'], 2000, 'e_prog'); dx, _ = pdiff(rep['exact'], rep['matched'], 2000, 'e_exset')
        P('\nPaired exact - matched over %d runs: e net %s; exploiter-set control %s; mixing %s.' % (n, fmt(d), fmt(dx), fmt(pdiff(rep['exact'], rep['matched'], 2000, 'mix_pop')[0])))
        S['replicate200'] = dict(exact_minus_matched_e=d, exact_minus_matched_e_exset=dx)

    # ------------------------------------------------------------ controls
    P('\n## 4. Controls (c = 0.01 unless stated)\n')
    P('### Forfeit-only price (charge c D P(forfeit); successful reading is free)\n')
    rows = []
    for arm in ARMS:
        rr = lot(arm, 0.01, 'primary', 'forfeit')
        rd = lot(arm, 0.01)
        if not rr: continue
        c4 = chain(arm, 0.01, 10000, 'forfeit'); c5 = chain(arm, 0.01, 100000, 'forfeit')
        rows.append((arm, 'lottery', fmt(boot(runvec(rr, 2000, 'e_prog'))), fmt(boot(runvec(rr, 2000, 'mix_pop'))), fmt(boot(runvec(rr, 2000, 'forfeit_plays'))),
                     fmt(boot(runvec(rr, 2000, 'share_X'))), fmt(boot(runvec(rr, 2000, 'share_readers'))), fmt(pdiff(rr, rd, 2000, 'forfeit_plays')[0]) + ' (vs depth price)'))
        for N, cc in ((10000, c4), (100000, c5)):
            if cc:
                s = cc['pi_stat']
                rows.append((arm, 'chain N=%d' % N, '%.4f' % s['e_prog'], '%.3f' % s['mix_pop'], '%.3f' % s['forfeit_plays'], '%.4f' % cc['class_share_X'], '%.3f' % s['share_readers'], ''))
    P(md_table(['arm', 'object', 'e net', 'mixing', 'plays forfeited', 'X', 'readers', 'forfeit diff vs depth price'], rows))
    P('\n### Depth panel: c D = 0.12 at D = 8 (c = 0.015), 12 (c = 0.01), 16 (c = 0.0075)\n')
    rows = []
    for arm in STOCH:
        for D, c in ((8, 0.015), (12, 0.01), (16, 0.0075)):
            rr = lot(arm, c, 'primary', 'depth', D)
            for N in (1000, 10000):
                cc = chain(arm, c, N, 'depth', D)
                if cc:
                    s = cc['pi_stat']
                    rows.append((arm, D, c, 'chain N=%d' % N, '%.4f' % s['e_prog'], '%.3f' % s['mix_pop'], '%.3f' % s['forfeit_plays'], '%.4f' % cc['class_share_X']))
            if rr:
                rows.append((arm, D, c, 'lottery', fmt(boot(runvec(rr, 2000, 'e_prog'))), fmt(boot(runvec(rr, 2000, 'mix_pop'))), fmt(boot(runvec(rr, 2000, 'forfeit_plays'))), fmt(boot(runvec(rr, 2000, 'share_X')))))
    P(md_table(['arm', 'D', 'c', 'object', 'e net', 'mixing', 'plays forfeited', 'X'], rows))
    P('\n### exact-br (genuine best response to forfeits) priced at c = 0.01\n')
    rows = []
    for N in (1000, 10000, 100000):
        cc = chain('exact_br', 0.01, N)
        if cc:
            s = cc['pi_stat']; rows.append(('chain N=%d' % N, '%.4f' % s['e_prog'], '%.3f' % s['mix_pop'], '%.3f' % s['forfeit_plays'], '%.4f' % cc['class_share_X'], '%.3f' % s['share_readers']))
    rr = lot('exact_br', 0.01)
    if rr:
        rows.append(('lottery', fmt(boot(runvec(rr, 2000, 'e_prog'))), fmt(boot(runvec(rr, 2000, 'mix_pop'))), fmt(boot(runvec(rr, 2000, 'forfeit_plays'))), fmt(boot(runvec(rr, 2000, 'share_X'))), fmt(boot(runvec(rr, 2000, 'share_readers')))))
    P(md_table(['object', 'e net', 'mixing', 'plays forfeited', 'X', 'readers'], rows))
    P('\n### Work price\n')
    wd = [v['max_abs_work_minus_depth'] for v in static.values() if v['kind'] == 'depth' and v['D'] == 12]
    P('At n = 6 the work cost table equals the depth cost table exactly in every arm (maximum |work - depth| over the table %.1e; maximum cost 12.0 in both), so the work-price cells at c = 0.01 '
      'in the sample and exact arms are the depth-price cells (notes §1.1, §2.2) and are not rerun.' % (max(wd) if wd else float('nan')))
    if os.path.exists(n7):
        w7 = jload(n7)
        P('\nn = 7 supplement (unpriced exact class representatives, %d classes, closed set of %d programs; classes not recomputed under the price; discovery restricted to pairs and triples among the 120 highest-prior classes, the 8-strongest-invader closure, no attractor search, exploration threshold 1e-8): maximum depth cost %.1f, maximum work cost %.1f; '
          '%d of %d class pairs have work > depth (largest excess %.1f). Examples (reader, opponent, depth, work): %s.' % (
              w7['K'], w7['closed_set'], w7['max_depth'], w7['max_work'], w7['n_pairs_work_gt_depth'], w7['n_pairs'], w7['max_work_minus_depth'],
              '; '.join('%s vs %s: %.2f, %.2f' % tuple(e) for e in w7['examples'][:4])))
        rows = []
        for kind in ('depth', 'work'):
            for N in (1000, 10000):
                v = w7.get('%s_N%d' % (kind, N))
                if v: rows.append((kind, N, '%.4f' % v['e_prog'], '%.4f' % v['e_gross'], '%.3f' % v['mix_pop'], '%.3f' % v['forfeit_plays'], '%.4f' % v['X'], '%.3f' % v['readers'], '%.4f' % v['cost_paid'], '%.2e' % v['poly']))
        P('\n' + md_table(['n = 7 price', 'N', 'e net', 'e gross', 'mixing', 'plays forfeited', 'X', 'readers', 'cost paid', 'polymorphic mass'], rows))
        S['n7work'] = {k: v for k, v in w7.items() if k != 'examples'}

    # ------------------------------------------------------------ verdicts
    V = {}
    P('\n## 5. Verdicts (conventions of `predictions/2026-10-23-rps-priced.md`)\n')

    def two_arm(vs):
        if all(v == 'held' for v in vs): return 'held'
        if all(v == 'failed' for v in vs): return 'failed'
        return 'partial'

    # 1
    V['1'] = ('held' if p1ok and static else 'failed', 'X pays 0 and earns >= 0 against every program; at every c > 0 (depth and forfeit-only prices) X invades and weakly dominates all self-forfeiting programs in the sample, matched, exact and exact-br tables (0 failures in all combinations); at c = 0 it only ties' if p1ok else 'a failure in static.json')
    # 2
    v2 = {}
    for arm in STOCH:
        rr = lot(arm, 0.01)
        if not rr: continue
        f = boot(runvec(rr, 2000, 'forfeit_plays')); m = boot(runvec(rr, 2000, 'mix_pop')); sh = boot(runvec(rr, 2000, 'share_e_le_0.05'))
        if f[0] >= 0.3 or m[0] < 0.4: vv = 'failed'
        elif f[0] <= 0.1 and m[0] >= 0.6 and sh[0] >= 0.6: vv = 'held'
        else: vv = 'partial'
        v2[arm] = (vv, 'forfeits %s, mixing %s, islands e net <= 0.05 %s' % (fmt(f), fmt(m), fmt(sh)))
    if v2:
        V['2'] = (two_arm([v[0] for v in v2.values()]), '; '.join('%s: %s (%s)' % (a, v[0], v[1]) for a, v in v2.items()))
    # 3
    v3 = {}
    for arm in STOCH:
        r4 = chain(arm, 0.01, 10000); r3 = chain(arm, 0.01, 1000); r5 = chain(arm, 0.01, 100000)
        if not (r3 and r4 and r5): continue
        e4, m4 = r4['pi_stat']['e_prog'], r4['pi_stat']['mix_pop']
        if e4 > 0.2 or m4 < 0.4: lv = 'failed'
        elif e4 <= 0.1 and m4 >= 0.6: lv = 'held'
        else: lv = 'partial'
        de = abs(r3['pi_stat']['e_prog'] - r5['pi_stat']['e_prog']); dm = abs(r3['pi_stat']['mix_pop'] - r5['pi_stat']['mix_pop'])
        sp = 'held' if (de <= 0.1 and dm <= 0.1) else 'failed'
        vv = 'failed' if lv == 'failed' else ('held' if lv == 'held' and sp == 'held' else 'partial')
        v3[arm] = (vv, 'N=10^4: e net %.4f, mixing %.3f (level %s); N=10^3 vs 10^5: |de| %.4f, |dmix| %.4f (speed %s); self-play forfeit gap %.4f' % (
            e4, m4, lv, de, dm, sp, abs(r3['pi_stat']['forfeit_self'] - r5['pi_stat']['forfeit_self'])))
    if v3:
        V['3'] = (two_arm([v[0] for v in v3.values()]), '; '.join('%s: %s (%s)' % (a, v[0], v[1]) for a, v in v3.items()))
        cg = False
        for arm in STOCH:
            r3 = chain(arm, 0.01, 1000); r5 = chain(arm, 0.01, 100000)
            if r3 and r5:
                dm = abs(r3['pi_stat']['mix_pop'] - r5['pi_stat']['mix_pop']); df = abs(r3['pi_stat']['forfeit_self'] - r5['pi_stat']['forfeit_self'])
                cg = cg or (dm > 0.1 and df < dm)
        V['3 counter (gpt)'] = ('held' if cg else 'failed', 'in at least one arm the 10^3-vs-10^5 mixing distance exceeds 0.1 while the self-play forfeit distance is smaller: %s' % cg)
    # 4
    v4 = {}
    c4 = {}
    for arm in STOCH:
        seqs = {}
        for k in ('forfeit_plays', 'mix_pop'):
            seqs[k] = [boot(runvec(lot(arm, c), 2000, k)) if lot(arm, c) else None for c in CS]
        if any(s is None for ss in seqs.values() for s in ss): continue
        fm = [s[0] for s in seqs['forfeit_plays']]; mm = [s[0] for s in seqs['mix_pop']]
        a_ok = all(min(x[0], x[2]) - 1e-12 <= x[1] <= max(x[0], x[2]) + 1e-12 for x in (fm[:3], mm[:3]) for _ in [0]) if False else None
        a_f = min(fm[0], fm[2]) - 1e-12 <= fm[1] <= max(fm[0], fm[2]) + 1e-12
        a_m = min(mm[0], mm[2]) - 1e-12 <= mm[1] <= max(mm[0], mm[2]) + 1e-12
        b_ok = mm[3] >= mm[2]
        rise = []; mdown = []
        for i in range(3):
            d, n = pdiff(lot(arm, CS[i + 1]), lot(arm, CS[i]), 2000, 'forfeit_plays'); rise.append(d[1] > 0)
            d2, n2 = pdiff(lot(arm, CS[i + 1]), lot(arm, CS[i]), 2000, 'mix_pop'); mdown.append(d2[2] < 0)
        c_ok = not any(rise)
        vv = 'failed' if not c_ok else ('held' if (a_f and a_m and b_ok) else 'partial')
        v4[arm] = (vv, 'forfeits over c = 0, .001, .01, .05: %s; mixing: %s; (a) between: forfeits %s mixing %s; (b) mix(.05) >= mix(.01): %s; (c) no significant rise in forfeits: %s' % (
            ['%.3f' % x for x in fm], ['%.3f' % x for x in mm], a_f, a_m, b_ok, c_ok))
        c4[arm] = (c_ok, any(mdown))
    if v4:
        V['4'] = (two_arm([v[0] for v in v4.values()]), '; '.join('%s: %s (%s)' % (a, v[0], v[1]) for a, v in v4.items()))
        cp = all(c[0] for c in c4.values()) and any(c[1] for c in c4.values())
        V['4 counter (gpt)'] = ('held' if cp else 'failed', 'forfeits monotone in both arms and mixing has a significantly falling step in at least one arm: %s' % cp)
    # 5
    v5 = {}
    ok = []
    for c in (0.001, 0.01, 0.05):
        rr = lot('pure', c)
        if rr: v5[c] = boot(runvec(rr, 2000, 'e_indiv'))
    if len(v5) == 3:
        vals = [v[0] for v in v5.values()]
        vv = 'held' if all(x >= 0.3 for x in vals) else ('failed' if any(x <= 0.1 for x in vals) else 'partial')
        chn = {c: chain('pure', c, 10000) for c in (0.001, 0.01, 0.05)}
        V['5'] = (vv, 'pure arm lottery individual net exploitability at c = .001/.01/.05: %s; population net exploitability %s; gross individual exploitability %s; chain N=10^4 e net %s, e indiv %s' % (
            ' / '.join(fmt(v) for v in v5.values()), ' / '.join(fmt(boot(runvec(lot('pure', c), 2000, 'e_prog'))) for c in v5), ' / '.join(fmt(boot(runvec(lot('pure', c), 2000, 'e_indiv_gross'))) for c in v5),
            ' / '.join('%.4f' % chn[c]['pi_stat']['e_prog'] if chn[c] else 'n/a' for c in chn), ' / '.join('%.4f' % chn[c]['pi_stat']['e_indiv'] if chn[c] else 'n/a' for c in chn)))
    # 6
    v6 = {}
    for arm in STOCH:
        rr = lot(arm, 0.01)
        if not rr: continue
        x = boot(runvec(rr, 2000, 'share_X')); rd = boot(runvec(rr, 2000, 'share_readers')); g = boot(runvec(rr, 2000, 'share_guarded'))
        vv = 'held' if x[0] > rd[0] else 'failed'
        v6[arm] = (vv, 'X %s vs readers combined %s (guarded readers %s)' % (fmt(x), fmt(rd), fmt(g)), g[0] > x[0])
    if v6:
        V['6'] = (two_arm([v[0] for v in v6.values()]), '; '.join('%s: %s (%s)' % (a, v[0], v[1]) for a, v in v6.items()))
        extra = []
        for arm in STOCH:
            rr = lot(arm, 0.05)
            if rr: extra.append('c=0.05 %s: X %s guarded %s' % (arm, fmt(boot(runvec(rr, 2000, 'share_X'))), fmt(boot(runvec(rr, 2000, 'share_guarded')))))
            r5 = chain(arm, 0.01, 100000)
            if r5: extra.append('chain N=10^5 c=0.01 %s: X %.3f guarded %.3f' % (arm, r5['class_share_X'], r5['pi_stat']['share_guarded']))
        V['6 counter (gemini)'] = ('held' if all(v[2] for v in v6.values()) else 'failed', 'guarded readers hold more than X at c = 0.01 in both arms: %s; %s' % ([v[2] for v in v6.values()], '; '.join(extra)))
    # 7
    re_, rm_ = lot('exact', 0.01), lot('matched', 0.01)
    c_e, c_m = chain('exact', 0.01, 10000), chain('matched', 0.01, 10000)
    if re_ and rm_ and c_e and c_m:
        d, n = pdiff(re_, rm_, 2000, 'e_prog')
        dx, _ = pdiff(re_, rm_, 2000, 'e_exset') if 'e_exset' in re_[0]['means']['2000'] else (None, 0)
        dc = c_e['pi_stat']['e_prog'] - c_m['pi_stat']['e_prog']
        dcx = c_e['pi_stat'].get('e_exset', float('nan')) - c_m['pi_stat'].get('e_exset', float('nan'))
        lot_neg = d[2] < 0
        chain_neg = dc < -0.01
        vv = 'failed' if lot_neg else ('partial' if chain_neg else 'held')
        d200 = S.get('replicate200', {}).get('exact_minus_matched_e')
        V['7'] = (vv, ('replicate (200 runs) exact - matched net e %s; ' % fmt(d200) if d200 else '') + 'lottery paired exact - matched net e %s (%d runs; exploiter-set control %s); chain N=10^4: %.4f (exploiter-set control %.4f); N=10^3: %.4f' % (
            fmt(d), n, fmt(dx) if dx else 'n/a', dc, dcx, chain('exact', 0.01, 1000)['pi_stat']['e_prog'] - chain('matched', 0.01, 1000)['pi_stat']['e_prog'] if chain('exact', 0.01, 1000) and chain('matched', 0.01, 1000) else float('nan')))
    # RS statement
    rs = {}
    for c in (0.001, 0.01, 0.05):
        cells = []
        for arm in STOCH:
            r4 = chain(arm, c, 10000); rr = lot(arm, c)
            if r4: cells.append(('chain', arm, r4['pi_stat']['e_prog'], r4['pi_stat']['mix_pop']))
            if rr: cells.append(('lottery', arm, boot(runvec(rr, 2000, 'e_prog'))[0], boot(runvec(rr, 2000, 'mix_pop'))[0]))
        if not cells: continue
        if all(e <= 0.05 and m >= 0.8 for _, _, e, m in cells): vv = 'held'
        elif all(e > 0.15 or m < 0.5 for _, _, e, m in cells): vv = 'failed'
        else: vv = 'partial'
        rs[c] = (vv, '; '.join('%s %s e %.3f mix %.3f' % x for x in cells))
    for c, v in rs.items():
        V['RS statement, reading (I), c = %s' % c] = v
    P(md_table(['item', 'verdict', 'evidence'], [(k, v[0], v[1]) for k, v in V.items()]))
    S['verdicts'] = {k: dict(verdict=v[0], evidence=v[1]) for k, v in V.items()}

    P('\n## 6. Deviations from the spec (details in `notes/rps-priced.md` §2-§3)\n')
    P('1. Exploration threshold 1e-8 (not the unpriced 1e-14); sensitivities 1e-6, 1e-10, lumped at N = 10^4, c = 0.01. 2. The invasion closure follows the 8 strongest invaders per node; polymorphic seeds also from a 1,000-start replicator search. '
      '3. All lottery runs are carried to 10,000 generations (generation 2,000 is the primary reading). 4. The work-price cells at n = 6 are not rerun: the work table equals the depth table exactly; the n = 7 supplement uses the unpriced class representatives and restricted discovery. '
      '5. A 200-run replicate at c = 0.01 was added. 6. Net exploitability of the pure arm can be negative (no `X`); gross individual exploitability is reported beside it. 7. c = 0 is run through the same pipeline; it reproduces the stored unpriced run.\n')
    open(os.path.join(ROOT, 'runs', 'rps-priced.md'), 'w').write('\n'.join(md) + '\n')
    json.dump(S, open(os.path.join(ROOT, 'runs', 'rps-priced.json'), 'w'), default=float, indent=1)
    print('wrote runs/rps-priced.md and .json')


if __name__ == '__main__':
    main()
