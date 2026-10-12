"""Report for the gene arm: runs/gene-arm.md and runs/gene-arm.json from runs/gene_arm/*.json (the verdicts section
is runs/gene_arm/verdicts.md, written by hand after reading the tables, and appended)."""
import json, os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'runs', 'gene_arm')


def load(name):
    f = os.path.join(D, name)
    return json.load(open(f)) if os.path.exists(f) else None


def f(x, d=3):
    if x is None:
        return '–'
    if isinstance(x, str):
        return x
    if x != 0 and (abs(x) < 10 ** -d or abs(x) >= 1e5):
        return '%.1e' % x
    return ('%.' + str(d) + 'f') % x


ARMS = ['base-CC', 'base-RC', 'base-RR', 'G-all', 'G-all-RC', 'G-cred', 'G-cred-ctl', 'G-cred-whole', 'G-cred-whole-ctl',
        'G-asym', 'G-asym-ctl', 'G-recip', 'G-recip-ctl', 'random']


def cells():
    out = {}
    for p in glob.glob(os.path.join(D, 'cell_*.json')):
        d = json.load(open(p))
        out[(d['arm'], d['kernel'], d['prior'], int(d['N']))] = d
    return out


def main():
    L = []
    J = {}
    st = load('static.json'); guard = load('guard.json')
    C = cells()
    L.append('# The gene arm: run report (2026-10-11)\n')
    L.append('Spec `specs/2026-10-11-gene-arm.md`; notes `notes/gene-arm.md`; predictions `predictions/2026-10-11-gene-arm.md`; code '
             '`src/gene_arm.py`, `src/gene_arm_run.py`, `src/gene_arm_report.py`, `tests/test_gene_arm.py`. Raw outputs in `runs/gene_arm/` '
             '(cell_*.json, static.json, chicken.json, lottery_*.json, coalition.json; tables_*.npz not committed).\n')
    L.append('**Scale guard.** At cap 2 the boss slot has ≥ %d behavioural classes (worker ≥ %d) > 3,000, so the SOG cells run at **cap 1** '
             '(136 worker and 1,323 boss programs), a different experiment from the spec\'s ≤ 2-gene arm; chicken at cap 2 (68 programs per role).\n'
             % (guard['boss_classes_lower_bound'], guard['worker_classes_lower_bound']))
    # static
    L.append('## Static\n')
    L.append('**Arms (cap 1):**\n')
    L.append('| arm | rule | genes W / B | programs B / W | classes B / W | refined units B / W | prior mass kept B / W (length; uniform) |')
    L.append('|---|---|---|---|---|---|---|')
    for a, r in st['arms'].items():
        L.append('| %s | %s | %d / %d | %d / %d | %d / %d | %d / %d | %s / %s; %s / %s |' % (
            a, r['rule'], r['genes_w'], r['genes_b'], r['programs_b'], r['programs_w'], r['classes_b'], r['classes_w'], r['refined_b'], r['refined_w'],
            f(r['mass_kept_length']['boss']), f(r['mass_kept_length']['worker']), f(r['mass_kept_uniform']['boss']), f(r['mass_kept_uniform']['worker'])))
    L.append('')
    L.append('**The override filter (G-cred) against the frozen reference catalogue (all cap-1 programs, CC):** admitted = %s; %s. '
             'No vacuous admission. Admitted-only iteration: %s, changes %s. Random removal keeps W: %s; B: %s.\n' % (
                 ', '.join('`%s`' % g for g in st['filter_summary']['worker_admitted']),
                 ', '.join('`%s`' % g for g in st['filter_summary']['boss_admitted']),
                 st['admitted_only']['status'], st['admitted_only']['changed_vs_frozen'] or 'none',
                 ', '.join(st['random_removal']['worker']), ', '.join(st['random_removal']['boss'])))
    L.append('| named gene | admitted | firing encounters | failing | heaviest failing witness (boss \\| W1 \\| W2: play; override vs alternatives) |')
    L.append('|---|---|---|---|---|')
    for k, v in st['named_gene_verdicts'].items():
        w = v.get('witness_fail')
        ws = ('%s \\| %s \\| %s: %s; %s vs %s' % (w['boss'], w['W1'], w['W2'], w['play'], w['u_override'], w.get('u_alt', w.get('u_alts')))) if w else '–'
        L.append('| %s %s | %s | %d | %d | %s |' % (k, v['name'], v['admitted'], v['fired'], v['failed'], ws))
    L.append('')
    L.append('**Encoding invariance** (fraction of reference encounter mass, length prior, on which the two encodings play differently):\n')
    L.append('| pair | CC | RR |')
    L.append('|---|---|---|')
    for k, v in st['encoding_invariance'].items():
        g = lambda r: f(r.get('diff_mass', r.get('diff_mass_W1')))
        L.append('| %s | %s | %s |' % (k, g(v['CC']), g(v['RR'])))
    L.append('\nOverride-filter verdicts: gene encodings fail, base encodings are unfiltered (admitted) — invariance fails for every named gene '
             'under G-cred and G-recip; under G-cred-whole both encodings are rationalized identically.\n')
    L.append('**Named states** (play under the arm; gene-stable strict / weak; Nash; Pareto-dominated):\n')
    arms5 = ['G-all', 'G-cred', 'G-cred-whole', 'G-asym', 'G-recip']
    L.append('| state | ' + ' | '.join(arms5) + ' | Nash (CC) | dominated |')
    L.append('|---|' + '---|' * (len(arms5) + 2))
    for k, v in st['named_states'].items():
        cellsx = []
        for a in arms5:
            r = v['arms'][a]
            cellsx.append('%s %s/%s' % (r['play'], 'S' if r['gene_stable'] else 'U', 'S' if r['weak_gene_stable'] else 'U'))
        L.append('| %s = %s | %s | %s | %s |' % (k, v['state'], ' | '.join(cellsx), v['arms']['G-all']['nash'], v['arms']['G-all']['pareto_dominated']))
    L.append('')
    L.append('**All program triples (cap 1): gene-stable triples by arm** (strict; weak = no admissible gene weakly improves its carrier and strictly improves someone):\n')
    L.append('| arm | version | triples | gene-stable | stable ∧ Nash | stable ∧ ¬Nash | Nash ∧ ¬stable | stable ∧ Pareto-dominated (prior mass) | stable by wage 0 / ¼ / ½ |')
    L.append('|---|---|---|---|---|---|---|---|---|')
    for a, v in st['gene_stable_scan'].items():
        for ver in ('strict', 'weak'):
            r = v[ver]
            L.append('| %s | %s | %d | %d | %d | %d | %d | %d (%s) | %d / %d / %d |' % (
                a, ver, r['triples'], r['stable'], r['stable_nash'], r['stable_not_nash'], r['nash_not_stable'], r['stable_dominated'],
                f(r['stable_dominated_mass']), r['stable_by_wage']['0'], r['stable_by_wage']['1/4'], r['stable_by_wage']['1/2']))
    L.append('')
    gr = st['gene_stable_scan']['G-recip']
    L.append('**G-recip: gene-stable Pareto-dominated states and the admissible genes that would leave them** (strict version, heaviest by prior):\n')
    for e in gr['strict']['dominated_examples'][:4]:
        L.append('- %s (play %s, mass %s): %s' % (e['state'], e['play'], f(e['mass']),
                                                   '; '.join('%s %s Δ=%s → %s' % tuple(x) for x in e['leaving_genes']) or 'none'))
    L.append('- weak version: %d triples, e.g. %s (no single admissible gene weakly improves its carrier and strictly improves anyone)' % (
        gr['weak']['stable_dominated'], '; '.join('%s (%s)' % (e['state'], e['play']) for e in gr['weak']['dominated_examples'][:2])))
    L.append('- Pareto-efficient states G-recip still admits as gene-stable: zero wage with everyone working (Z) and the fair and ¼ plays held '
             'by committed bases (F, F_u, I, F*): the filter cannot choose among the frontier\'s wages.\n')
    L.append('**SG on hand states** (targeted proposals; kind):\n')
    for k, v in st['sg_hand'].items():
        L.append('- %s: ' % k + '; '.join('%s: %s' % (s, ', '.join('%s %s' % (p['gene'], p['kind']) for p in ps)) for s, ps in v.items()))
    L.append('')
    # chain
    L.append('## Chain (ε → 0; cap 1; c = 0.5)\n')
    L.append('Fair = wage ½ with both working and no realized whack; ¼ = intermediate; split = one striker. "cut" = unexplored outflow / total '
             'outflow; "fair corr." = first-order cut-corrected fair share (dropped fair exits added to the fair escape) where the cut exceeds 2%.\n')
    for prior in ('uniform', 'length'):
        L.append('**%s prior** (N = 10³ → 10⁴):\n' % prior)
        L.append('| arm | kernel | fair | ¼ | zero | strike | split | worker payoff | boss | states | cut | fair corr. | strict-NE seeds |')
        L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        for a in ARMS:
            for k in ('prior', 'SG', 'local'):
                r3, r4 = C.get((a, k, prior, 1000)), C.get((a, k, prior, 10000))
                if not r3 and not r4:
                    continue
                g = lambda r, key: f(r['summary'][key]) if r else '–'
                L.append('| %s | %s | %s → %s | %s → %s | %s → %s | %s → %s | %s → %s | %s | %s | %s / %s | %s / %s | %s | %s |' % (
                    a, k, g(r3, 'fair'), g(r4, 'fair'), g(r3, 'intermediate'), g(r4, 'intermediate'), g(r3, 'zero wage'), g(r4, 'zero wage'),
                    g(r3, 'strike'), g(r4, 'strike'), g(r3, 'scab split'), g(r4, 'scab split'),
                    f(r4['payoffs']['W1']) if r4 else '–', f(r4['payoffs']['boss']) if r4 else '–',
                    r3['states'] if r3 else '–', r4['states'] if r4 else '–', f(r3['cut_total_rel']) if r3 else '–', f(r4['cut_total_rel']) if r4 else '–',
                    f(r4.get('fair_cut_corrected')) if r4 else '–', r4['strict_ne'] if r4 else '–'))
        L.append('')
    # support and transitions for key cells
    L.append('### Support, transitions and decisive edges (N = 10⁴)\n')
    for key in [(a, 'prior', p, 10000) for p in ('uniform', 'length') for a in ('G-all', 'G-cred', 'G-cred-whole', 'G-asym', 'G-recip', 'G-cred-ctl', 'base-CC', 'base-RC')]:
        r = C.get(key)
        if not r:
            continue
        L.append('**%s, %s prior** (99%% of π on %d states; implemented whack %s; strike-whacker bases %s; probe bosses %s):\n' % (
            key[0], key[2], r['support_size_99'], {k: f(v) for k, v in r['implemented_whack'].items()}, f(r['strike_whacker_base']), f(r['probe_boss'])))
        for s in r['support'][:6]:
            L.append('- π %s: %s → %s [%s]%s%s' % (f(s['pi'], 4), s['state'], s['play'], s['summary'],
                                                   '' if s['gene_stable'] else ' gene-unstable via %s %s (Δ %s)' % (s['gene_witness']['slot'], s['gene_witness']['gene'], f(s['gene_witness']['du'])),
                                                   ' Pareto-dominated' if s['pareto_dominated'] else ''))
        for t in r['transitions'][:3]:
            L.append('  - exits of %s (π %s): total %s per event; %s; top: %s' % (
                t['state'], f(t['pi'], 4), f(t['exit_total']), ', '.join('%s %s' % (k, f(v)) for k, v in t['by_kind'].items()),
                '; '.join('%s %s Δ=%s NΔ=%s → %s (%s) %s' % (e['slot'], e['kind'], f(e['delta']), f(e['N_delta'], 1), e['to_play'], e['to_summary'], f(e['rate'])) for e in t['top'][:3])))
        L.append('')
    # execution
    L.append('## Execution rates of threat-type genes and commitments (prior kernel; the RS\'s second addition)\n')
    L.append('| cell | threat | carrier mass | on-path execution rate | cost / execution | carriers\' mean payoff | non-carriers\' |')
    L.append('|---|---|---|---|---|---|---|')
    for key in [(a, 'prior', p, 10000) for p in ('uniform', 'length') for a in ('base-CC', 'base-RC', 'G-all', 'G-cred', 'G-recip')]:
        r = C.get(key)
        if not r: continue
        for th, v in r['execution'].items():
            L.append('| %s/%s | %s | %s | %s | %s | %s | %s |' % (key[0], key[2], th, f(v['carrier_mass']), f(v['execution_rate'], 4), f(v['cost_per_execution']),
                                                                   f(v['carrier_mean_payoff']), f(v['noncarrier_mean_payoff'])))
    L.append('')
    # device
    L.append('## The proof device on the chain\'s support (99% of π)\n')
    L.append('| cell | gene-stable mass | weak | Pareto-dominated | dominated ∧ stable | Nash | heaviest dominated ∧ stable |')
    L.append('|---|---|---|---|---|---|---|')
    for key in sorted(C):
        r = C[key]
        if key[1] != 'prior' or key[3] != 10000: continue
        d = r['device']
        L.append('| %s/%s | %s | %s | %s | %s | %s | %s |' % (key[0], key[2], f(d['stable']), f(d['weak']), f(d['dominated']), f(d['dominated_stable']), f(d['nash']),
                                                    '; '.join('%s (%s, π %s)' % (e['state'], e['play'], f(e['pi'], 4)) for e in d['dominated_stable_examples'][:1])))
    L.append('')
    # SG diag
    L.append('## SG and the uniform-local kernel: targeted proposals at the top states (N = 10⁴)\n')
    for key in sorted(C):
        r = C[key]
        if key[1] == 'prior' or key[3] != 10000: continue
        sd = r.get('sg_diag', [])
        L.append('- %s/%s/%s: strict proposals at the 8 top states %s; strict whack proposals %s; conservative whack proposals %s' % (
            key[0], key[1], key[2], [x['strict'] for x in sd], sum(len(x['strict_whack']) for x in sd), sum(len(x['conservative_whack']) for x in sd)))
    L.append('')
    co = load('coalition.json')
    if co:
        L.append('## Coalition kernel (labelled cell)\n')
        for k, v in co.items():
            if not v.get('coalition'):
                L.append('- %s: no two-worker coalition leads to a strict boss move to a higher wage with both working' % k); continue
            L.append('- %s: coalition %s (μ-product %s), pair play %s, boss response %s; %s' % (
                k, ' + '.join(v['coalition']), f(v['mu_product']), v['pair_play'], v['boss_response'],
                '; '.join('N=%s: ρ₂ %s (N²ρ₂ %s), sequential ρ %s then %s' % (n[1:], f(v[n]['rho2']), f(v[n]['rho2_times_N2']), f(v[n]['rho_first']), f(v[n]['rho_second']))
                          for n in ('N100', 'N1000') if n in v)))
        L.append('')
    # lottery
    L.append('## Lottery (ε = 0; (N, I) = (100, 64), mN = 1, 40 runs, length-prior seeds, CC)\n')
    L.append('| arm | runs closed | fair islands | ¼ | zero | strike | split | strike-whacker share at closure | whacks / encounter (trajectory) | strikes at s > 0 / encounter | at s = 0 |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|')
    for a in ('G-all', 'G-cred', 'G-asym', 'G-recip'):
        d = load('lottery_%s.json' % a)
        if not d: continue
        from collections import Counter
        lab = Counter(l for r in d['runs'] for l in r['label']); n = sum(lab.values())
        g = lambda k: f(lab.get(k, 0) / n)
        tr = lambda k: f(np.mean([r['trajectory'][k] for r in d['runs']]), 4)
        L.append('| %s | %d/%d | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            a, sum(r['status'] == 1 for r in d['runs']), len(d['runs']), g(0), g(1), g(2), g(3), g(4),
            f(np.mean([r['strike_whacker_share_final'] for r in d['runs']])), tr('whacks_per_encounter'), tr('strikes_pos_wage_per_encounter'), tr('strikes_zero_wage_per_encounter')))
    L.append('')
    sg = load('lottery_sg.json')
    if sg:
        L.append('**SG innovation in the lottery (a different object: finite-ε innovation, %s)**:\n' % sg['params'])
        L.append('| cell | fair (end) | ¼ (end) | zero (end) | fair (2nd half) | ¼ (2nd half) | zero (2nd half) | innovations / run |')
        L.append('|---|---|---|---|---|---|---|---|')
        for k, v in sg['summary'].items():
            L.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (k, f(v['fair_end']), f(v['quarter_end']), f(v['zero_end']), f(v['fair_2nd']), f(v['quarter_2nd']), f(v['zero_2nd']), f(v['innovations'], 0)))
        L.append('')
    ch = load('chicken.json')
    if ch:
        L.append('## Fixed-role chicken (cap 2)\n')
        L.append('Filter: ' + '; '.join('%s %s (fired %d, failed %d)' % (v['name'], 'admitted' if v['admitted'] else 'removed', v['fired'], v['failed']) for v in ch['filter'].values()) + '.\n')
        L.append('Named states: ' + '; '.join('%s: %s' % (k, ', '.join('%s %s' % (a, 'stable' if r['gene_stable'] else 'unstable %s' % r['witness'][:1]) for a, r in v.items())) for k, v in ch['named_states'].items()) + '.\n')
        L.append('Encoding: (St,1)+firm plays as (St,0) everywhere: %s.\n' % ch['encoding_firm']['play_identical'])
        L.append('| cell | R1 | R2 | crash | dove | units | top state | top exits |')
        L.append('|---|---|---|---|---|---|---|---|')
        for k, v in ch['cells'].items():
            if k.startswith('lottery'): continue
            s = v['summary']
            L.append('| %s | %s | %s | %s | %s | %d | %s (%s) | %s |' % (k, f(s['R1']), f(s['R2']), f(s['crash']), f(s['dove']), v['K'], v['support'][0]['state'], f(v['support'][0]['pi']),
                                                               '; '.join('%s Δ=%s → %s' % (f(e['rate']), f(e['delta']), e['label']) for e in v['top_exits'][:2])))
        L.append('')
        L.append('| lottery cell | per-island establishment (R1 or R2) | run sd | role-1 share | patchwork runs |')
        L.append('|---|---|---|---|---|')
        for k, v in ch['cells'].items():
            if not k.startswith('lottery'): continue
            L.append('| %s | %s | %s | %s | %s |' % (k, f(v['per_island_establishment']), f(v['est_run_sd']), f(v['role1_share']), f(v['patchwork_runs'])))
        L.append('')
    ver = os.path.join(D, 'verdicts.md')
    if os.path.exists(ver):
        L.append(open(ver).read())
    open(os.path.join(ROOT, 'runs', 'gene-arm.md'), 'w').write('\n'.join(L) + '\n')
    J['cells'] = {'%s/%s/%s/%d' % k: {kk: v[kk] for kk in ('summary', 'wage', 'payoffs', 'states', 'cut_total_rel', 'device', 'execution', 'KcB', 'KcW', 'KuB', 'KuW', 'strict_ne') if kk in v}
                  | {'support': v['support'][:6], 'fair_cut_corrected': v.get('fair_cut_corrected')} for k, v in C.items()}
    J['static'] = {k: st[k] for k in ('arms', 'filter_summary', 'admitted_only', 'encoding_invariance', 'named_states', 'gene_stable_scan', 'named_gene_verdicts')}
    J['guard'] = guard
    for k in ('coalition', 'lottery_sg'):
        J[k] = load(k + '.json')
    if ch:
        J['chicken'] = {k: ch[k] for k in ('filter', 'named_states', 'cells', 'encoding_firm')}
    J['lottery'] = {}
    for a in ('G-all', 'G-cred', 'G-asym', 'G-recip'):
        d = load('lottery_%s.json' % a)
        if d:
            J['lottery'][a] = [{k: r[k] for k in ('run', 'status', 'stop_gen', 'label_counts', 'strike_whacker_share_final', 'trajectory')} for r in d['runs']]
    json.dump(J, open(os.path.join(ROOT, 'runs', 'gene-arm.json'), 'w'), indent=1, default=str)
    print('wrote runs/gene-arm.md, runs/gene-arm.json')


if __name__ == '__main__':
    main()
