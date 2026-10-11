"""Report for the identity-and-tags experiment: runs/identity-tags.md and runs/identity-tags.json.

    python3 src/identity_tags_report.py
"""
import json, math, os, sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'identity_tags')


def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'), float('nan'))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def fmt(x, d=4):
    if x is None: return '–'
    if isinstance(x, (int, np.integer)): return str(int(x))
    if x == 0: return '0'
    if abs(x) < 10 ** -(d - 1) or abs(x) >= 10 ** 5: return '%.2e' % x
    return ('%.' + str(d) + 'g') % x


def load(fn):
    p = os.path.join(OUT, fn)
    return json.load(open(p)) if os.path.exists(p) else None


CELL_ORDER = ['L', 'L_N200', 'L_I256', 'U', 'T1a', 'T1b', 'T1c', 'T2', 'T3', 'abl_identity', 'abl_tags', 'abl_cbq']
CELL_DESC = {'L': 'L (100, 64)', 'L_N200': 'L (200, 64)', 'L_I256': 'L (100, 256)', 'U': 'U (100, 64)',
             'T1a': 'T1a: M on EQ', 'T1b': 'T1b: M/10 on ten EQ spellings', 'T1c': 'T1c: M/10 on ten CB spellings, family removed',
             'T2': 'T2: M on TC1¹', 'T3': 'T3: M on XC', 'abl_identity': 'ablation: identity only',
             'abl_tags': 'ablation: tags only', 'abl_cbq': 'ablation: ⌜CB⌝ only'}


def summarize_cell(rows):
    n = len(rows)
    I = rows[0]['I']; N = rows[0]['N']
    pairs = I * (I - 1) / 2
    out = dict(n=n, N=N, I=I)
    for tag in ('h2000', 'end'):
        oc = Counter(r[tag]['outcome'] for r in rows)
        out[tag] = dict(outcomes=dict(oc), universal_open=oc.get('universal-open', 0), universal_other=oc.get('universal-other', 0),
                        patchwork=oc.get('patchwork', 0), failed=oc.get('failed', 0), unresolved=oc.get('unresolved', 0),
                        clique_wins=sum(1 for r in rows if r[tag]['clique_win']),
                        separated=sum(1 for r in rows if r[tag]['separated']),
                        cross_pcc=float(np.mean([r[tag]['cross_pcc'] for r in rows])),
                        cross_holders=float(np.mean([r[tag]['cross_holders'] for r in rows])),
                        island_pcc=float(np.mean([r[tag]['island_pcc'] for r in rows])),
                        occupancy=float(np.mean([r[tag]['occupancy'] for r in rows])),
                        wilson_universal_open=wilson(oc.get('universal-open', 0), n))
    out['E3'] = dict(Counter(r['E3'] for r in rows))
    eg = [r['establish_gen'] for r in rows if r['establish_gen'] >= 0]
    ag = [r['all_established_gen'] for r in rows if r['all_established_gen'] >= 0]
    out['establish_gen_median'] = float(np.median(eg)) if eg else None
    out['all_established_gen_median'] = float(np.median(ag)) if ag else None
    out['n_all_established'] = len(ag)
    ever = [r for r in rows if r['first_sep'] >= 0]
    out['ever_separated'] = len(ever)
    p = len(ever) / n
    out['h_sep_per_pair'] = (-math.log(1 - p) / pairs) if p < 1 else float('inf')
    sep_gen = sum(r['n_sep_checks'] * 10 for r in rows)
    out['resolution_events'] = sum(r['n_resolutions'] for r in rows)
    out['separated_run_generations'] = sep_gen
    out['h_res_per_run_gen'] = out['resolution_events'] / sep_gen if sep_gen else None
    flips = sum(r['n_flips'] for r in rows); exp = sum(r['sep_island_checks'] * 10 for r in rows)
    out['flips'] = flips; out['flip_rate_per_island_gen'] = flips / exp if exp else None
    out['first_sep_median'] = float(np.median([r['first_sep'] for r in ever])) if ever else None
    sep2000 = [r for r in rows if r['h2000']['separated']]
    out['separated_at_2000'] = len(sep2000)
    out['separated_2000_resolved_by_end'] = sum(1 for r in sep2000 if not r['end']['separated'])
    out['separated_2000_end_outcomes'] = dict(Counter(r['end']['outcome'] for r in sep2000))
    # patchwork naming
    pw = Counter()
    for r in rows:
        if r['h2000']['outcome'] == 'patchwork':
            pw[' / '.join(sorted(k for k in r['h2000']['labels']))] += 1
    out['patchwork_labels_2000'] = dict(pw)
    lab2000 = Counter(); labend = Counter()
    for r in rows:
        lab2000.update(r['h2000']['labels']); labend.update(r['end']['labels'])
    out['island_labels_2000'] = {k: v / (n * I) for k, v in lab2000.items()}
    out['island_labels_end'] = {k: v / (n * I) for k, v in labend.items()}
    hold = Counter()
    for r in rows:
        for h, c in r['end']['holders']: hold[h] += c
    out['top_holders_end'] = hold.most_common(6)
    # tracked groups
    tr = {}
    for g in rows[0]['track']:
        rs = [r['track'][g] for r in rows]
        seeded = [x['seeded'] for x in rs]
        ext = [x.get('extinct_gen', -1) for x in rs if x.get('seeded', 0) > 0]
        tr[g] = dict(runs_seeded=sum(1 for s in seeded if s > 0), mean_seeded=float(np.mean(seeded)),
                     extinct=sum(1 for e in ext if e >= 0), median_extinction=float(np.median([e for e in ext if e >= 0])) if any(e >= 0 for e in ext) else None,
                     ever_held_island=sum(1 for x in rs if x.get('max_islands', 0) > 0),
                     alive_at_first_sep=sum(1 for x in rs if x.get('alive_at_first_sep')),
                     alive_at_first_sep_n=sum(1 for x in rs if x.get('alive_at_first_sep') is not None))
    out['track'] = tr
    # pooling
    pc = {}
    for tag in ('h2000', 'end'):
        dec = [r['pooling'][tag] for r in rows if r.get('pooling') and r['pooling'][tag]['decided']]
        bs = sum(1 for d in dec if d['best_seed_won'])
        be = [d['best_est_won'] for d in dec if d['best_est_won'] is not None]
        pc[tag] = dict(decided=len(dec), best_seed_won=bs, best_est_won=sum(be), best_est_n=len(be))
    pc['n_sets_median'] = float(np.median([r['pooling']['n_sets'] for r in rows if r.get('pooling')]))
    pc['incomplete'] = sum(1 for r in rows if r.get('pooling') and not r['pooling']['complete'])
    out['pooling'] = pc
    # seeded label counts (pooling by raw counts)
    slc = defaultdict(list)
    for r in rows:
        for k, v in r['seeded_label_counts'].items(): slc[k].append(v)
    out['seeded_counts_mean'] = {k: float(np.sum(v) / n) for k, v in slc.items()}
    out['time_s_mean'] = float(np.mean([r['time_s'] for r in rows]))
    out['K_present_mean'] = float(np.mean([r['K_present'] for r in rows]))
    return out

def main():
    st = load('static_n7.json'); an = load('static_analysis.json'); va = load('validate.json')
    lot = load('lottery_main.json') or []
    ch = load('chain.json') or []
    by = defaultdict(list)
    for r in lot: by[r['cell']].append(r)
    cells = {c: summarize_cell(by[c]) for c in CELL_ORDER + EXTRA if by.get(c)}
    for c, s in cells.items():
        rs = by[c]
        s['cooccur'] = {tag: dict(exclusive_and_open=sum(1 for r in rs if 'exclusive' in r[tag]['labels'] and 'open' in r[tag]['labels']),
                                  any_exclusive=sum(1 for r in rs if 'exclusive' in r[tag]['labels']),
                                  any_tag_club=sum(1 for r in rs if any(k.startswith('tag') for k in r[tag]['labels'])),
                                  identity_and_open=sum(1 for r in rs if 'identity' in r[tag]['labels'] and 'open' in r[tag]['labels']),
                                  identity_majority=sum(1 for r in rs if r[tag]['labels'].get('identity', 0) > r['I'] / 2))
                        for tag in ('h2000', 'end')}
    js = dict(static=st, analysis=an, validate=va, lottery=cells, chain=ch, diag=load('diag.json'))
    return js, cells


EXTRA = ['X_noclique', 'X_noallc']
CELL_DESC.update({'X_noclique': 'extra: identity cliques removed', 'X_noallc': 'extra: unconditional cooperators removed'})


def md(js, cells):
    st, an, va, dg = js['static'], js['analysis'], js['validate'], js.get('diag')
    o = []
    w = o.append
    w('# Run: identity and tags in the carrier grammar, the pooling test (2026-10-10)')
    w('')
    w('Spec `specs/2026-10-10-identity-and-tags.md`; review `reviews/2026-10-10-identity-and-tags-gpt-6.1-sol.md`; notes '
      '`notes/identity-tags.md`; predictions `predictions/2026-10-10-identity-and-tags.md` (with the endpoint revision); code '
      '`src/identity_tags.py`, `src/identity_tags_run.py`, `src/identity_tags_report.py`, `tests/test_identity_tags.py`; '
      'raw arrays in `runs/identity_tags/` (npz and pickles not committed). K = 10⁶, V = K/4, PD of the modal arm, w = 0.3. '
      'All lottery numbers are ε = 0, finite (N, I, horizon) evidence.')
    w('')
    w('## 1. Scale guard, costs, validation')
    w('')
    w('| spellings | run trees | τ′-units | lists | classes (singletons from split units) | unit-value checks | pair checks C / D (reduced keys) | TO C / D | total s (2 workers) |')
    w('|---|---|---|---|---|---|---|---|---|')
    w('| %d | %d | %d | %d | %d (%d from %d units) | %d | %d / %d | %d / %d | %.0f |' % (
        st['n_spellings'], st['n_dts'], st['n_units'], st['n_lists'], st['n_classes'], st['n_split_classes'], st['n_split_units'],
        st['unit_value_checks'], st['pair']['C']['keys'], st['pair']['D']['keys'], st['pair']['C']['TO'], st['pair']['D']['TO'], st['total_s']))
    w('')
    w("Classes exceed the spec's 2,500 trigger; the full grammar is computable, so no reduced grammar was run.")
    w('')
    ev = va['exec_vs_ideal']
    w('**Validation (notes §1.13):** hand table %d/%d cells by whole plays; Lemma T′/R sample %d pairs, %d mismatches; '
      'executable = ideal on %d classes (%d cells played whole), %d mismatches; soundness: %d + %d true checks, %d false atoms; '
      'milestone-2 lists changed by the extended probes: %d of %d; marker-reduced lists %d/%d direct productions equal; '
      'eq-clique spellings %d, classes %d (all singletons: %s); tags correct: %s.' % (
        va['hand_table']['n'] - va['hand_table']['mismatches'], va['hand_table']['n'], va['lemma_TR_sample']['n'], va['lemma_TR_sample']['mismatches'],
        ev['n_classes'], ev['n_cells'], ev['mismatches'], va['soundness_C']['n_true'], va['soundness_D']['n_true'],
        va['soundness_C']['false_atoms'] + va['soundness_D']['false_atoms'], va['m2_list_changes']['n_changed'], va['m2_list_changes']['n'],
        va['lists_marker_reduction']['n'] - va['lists_marker_reduction']['mismatches'], va['lists_marker_reduction']['n'],
        va['lumping']['eq_spellings'], va['lumping']['eq_classes'], va['lumping']['eq_singletons'], va['tags_ok']))
    w('')
    w('## 2. Static structure (L unless stated)')
    w('')
    m = an['mass']
    w('| prior | establishers | S-guarded est. | exploited est. | self-cooperators | unconditional C | D class |')
    w('|---|---|---|---|---|---|---|')
    for pr in ('L', 'U'):
        x = m[pr]
        w('| %s | %s | %s | %s | %s | %s | %s |' % (pr, fmt(x['est']), fmt(x['est_sguarded']), fmt(x['est_exploited']), fmt(x['selfc']), fmt(x['allc']), fmt(x['D'])))
    w('')
    w('Counts: %d classes; %d self-cooperators; %d establishers; %d unconditional cooperators.' % (an['n_classes'], an['n_selfc'], an['n_est'], an['n_allc']))
    w('')
    w('**Establisher classes by family label** (notes §1.10):')
    w('')
    w('| label | classes | mass L | mass U |')
    w('|---|---|---|---|')
    for k, v in sorted(an['labels'].items(), key=lambda kv: -kv[1]['mass_L']):
        if k == '-': continue
        w('| %s | %d | %s | %s |' % (k, v['n'], fmt(v['mass_L']), fmt(v['mass_U'])))
    w('')
    w('**Named classes:**')
    w('')
    w('| name | class representative | spellings in class | class mass L | spelling mass L | label | S-guarded | strict invaders |')
    w('|---|---|---|---|---|---|---|---|')
    for n, v in an['named'].items():
        w('| %s | `%s` | %d | %s | %s | %s | %s | %d |' % (n, v['name'], v['n_spellings'], fmt(v['mass_L']), fmt(an['spelling_mass'].get(n)),
                                                       v['label'], v['s_guarded'], v['n_strict_invaders']))
    w('')
    F = an['F_CB']; ic = an['identity_cliques']
    w('**Families.** %d maximal cliques of the establisher compatibility graph (complete enumeration, %.0f s); %d components (largest %d). '
      '**F_CB** (the heaviest maximal clique containing CB): %d classes, %d spellings, **M = %s**; CB lies in %d maximal cliques; '
      'N(CB) (establishers mutually cooperating with CB): %d classes, mass %s. Exact-identity cliques (maximal cliques of one single-spelling class): '
      '%d, total mass %s, heaviest %s (`%s`); **M / heaviest identity clique = %.0f**. The eq-clique run tree: %d spellings, mass %s, %d classes '
      "(CB's run tree: %d spellings, mass %s, %d classes)." % (
        an['cliques']['n'], an['cliques']['s'], an['cliques']['n_components'], an['cliques']['component_sizes'][0],
        F['size'], F['n_spellings'], fmt(F['M']), F['n_cliques_with_CB'], F['N_CB_size'], fmt(F['N_CB_mass']),
        ic['n_exact'], fmt(ic['mass_exact']), fmt(ic['max_mass']), ic['heaviest'][0][0], an['ratio_M_over_max_identity_clique'],
        an['eq_tree']['n_spellings'], fmt(an['eq_tree']['mass']), an['eq_tree']['n_classes'],
        an['cb_tree']['n_spellings'], fmt(an['cb_tree']['mass']), an['cb_tree']['n_classes']))
    w('')
    w('Heaviest pairwise-compatible sets (maximal cliques; near-duplicates differ in a few overlapping members):')
    w('')
    w('| mass L | classes | spellings | labels | contains CB | rival of F_CB | bridges with F_CB (non-exploitable) | heaviest members |')
    w('|---|---|---|---|---|---|---|---|')
    for t in an['top_cliques'][:14]:
        w('| %s | %d | %d | %s | %s | %s | %d (%d) | %s |' % (fmt(t['mass']), t['size'], t['n_spellings'], t['labels'], t['contains_CB'], t['rival_of_FCB'],
                                                      t['bridges_with_FCB'], t['bridges_nonexploitable'], ', '.join('`%s`' % h for h in t['heaviest'][:3])))
    w('')
    r = an['rivals_of_CB']
    w('**Rivals of CB** (establishers mutually defecting with CB): %d classes, mass %s, labels %s. Heaviest: %s.' % (
        r['n'], fmt(r['mass']), r['labels'], '; '.join('`%s` (%s, %s, S-guarded %s, %d invaders)' % (h[0], h[1], fmt(h[2]), h[3], h[4]) for h in r['heaviest'][:6])))
    w('')
    w('**Pairwise bridges** (self-cooperating classes mutually cooperating with both):')
    w('')
    w('| pair | bridges | mass L | establishers | non-exploitable | heaviest non-exploitable |')
    w('|---|---|---|---|---|---|')
    for k, v in an['pairwise_bridges'].items():
        w('| %s | %d | %s | %d | %d | %s |' % (k, v['n'], fmt(v['mass_L']), v['n_est'], v['n_nonexploitable'],
                                          ', '.join('`%s` %s' % (b[0], fmt(b[1])) for b in v['nonexploitable'][:3]) or '–'))
    w('')
    lk = an['leak']
    w('**Leak test:** %d self-cooperating classes in %d components (largest %d); **%d closed**, all identity cliques (labels %s), total mass %s; heaviest: %s.' % (
        lk['n_selfcoop'], lk['n_components'], lk['sizes'][0], lk['n_closed'], lk['closed_labels'], fmt(lk['closed_mass_L']),
        ', '.join('`%s` %s' % (c[0], fmt(c[1])) for c in lk['closed_heaviest'][:4])))
    w('')
    if dg:
        w('**Seed payoff** (expected payoff of a class against the iid seed, f = U·μ; the scramble diagnostic):')
        w('')
        w('| prior | unconditional C mass | EQ | CB | MC¹ | TC1¹ | XC | D | open (mass-weighted) | open prudent (refuse Cc): n, mass, f | identity (mass-weighted) | other |')
        w('|---|---|---|---|---|---|---|---|---|---|---|---|')
        for cell in ('L', 'U', 'T1a', 'T2', 'T3', 'identity', 'noclique', 'noallc'):
            if cell not in dg: continue
            d = dg[cell]; nmd = d['named']
            w('| %s | %s | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f | %d, %s, %.3f | %s | %s |' % (
                cell, fmt(d['allc_mass']), nmd['EQ'], nmd['CB'], nmd['MC^1'], nmd['TC1^1'], nmd['XC'], nmd['D'],
                d['open']['mean_f'], d['open_prudent']['n'], fmt(d['open_prudent']['mass']), d['open_prudent']['mean_f'],
                ('%.3f' % d['identity']['mean_f']) if 'identity' in d else '–', ('%.3f' % d['other']['mean_f']) if 'other' in d else '–'))
        w('')
    w('## 3. The ε = 0 lottery (mN = 1, 40 runs per cell; horizon 2,000, runs separated at 2,000 continued to 10,000)')
    w('')
    w('Outcomes on holders (predictions, endpoint revision). "Univ-open" = every island held and every pair of holders mutually cooperating, every holder mutually cooperating with CB.')
    w('')
    w('| cell | univ-open @2,000 [Wilson] | univ-other | patchwork | unresolved | failed | univ-open @10,000 | patchwork @10,000 | clique wins @2,000 / @10,000 | cross P(C,C) realized / holders @2,000 | @10,000 | island P(C,C) | open occupancy @2,000 / @10,000 |')
    w('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for c in CELL_ORDER + EXTRA:
        if c not in cells: continue
        s = cells[c]; h, e = s['h2000'], s['end']
        w('| %s | %d [%.2f, %.2f] | %d | %d | %d | %d | %d | %d | %d / %d | %.3f / %.3f | %.3f / %.3f | %.3f | %.2f / %.2f |' % (
            CELL_DESC.get(c, c), h['universal_open'], h['wilson_universal_open'][0], h['wilson_universal_open'][1], h['universal_other'], h['patchwork'],
            h['unresolved'], h['failed'], e['universal_open'], e['patchwork'], h['clique_wins'], e['clique_wins'], h['cross_pcc'], h['cross_holders'],
            e['cross_pcc'], e['cross_holders'], h['island_pcc'], h['occupancy'], e['occupancy']))
    w('')
    w('**Island shares by holder label** (fraction of all islands × runs):')
    w('')
    w('| cell | @2,000: open / identity / other / tag / exclusive | @10,000: open / identity / other / tag / exclusive | top holders @10,000 (island-runs) |')
    w('|---|---|---|---|')

    def sh(d):
        g = lambda k: d.get(k, 0.0)
        return '%.3f / %.3f / %.3f / %.3f / %.3f' % (g('open'), g('identity'), g('other'), g('tag1') + g('tag2'), g('exclusive'))
    for c in CELL_ORDER + EXTRA:
        if c not in cells: continue
        s = cells[c]
        w('| %s | %s | %s | %s |' % (CELL_DESC.get(c, c), sh(s['island_labels_2000']), sh(s['island_labels_end']),
                                     ', '.join('`%s` %d' % (a, b) for a, b in s['top_holders_end'][:3])))
    w('')
    w('**Separation, resolution and hazards:**')
    w('')
    w('| cell | ever separated | first separation (median gen) | h_sep per island pair | separated @2,000 | of those resolved by 10,000 | their outcome @10,000 | resolution events / separated run-gens | holder flips per island-gen (separated) |')
    w('|---|---|---|---|---|---|---|---|---|')
    for c in CELL_ORDER + EXTRA:
        if c not in cells: continue
        s = cells[c]
        w('| %s | %d | %s | %s | %d | %d | %s | %d / %d = %s | %s |' % (CELL_DESC.get(c, c), s['ever_separated'], fmt(s['first_sep_median']), fmt(s['h_sep_per_pair']),
                                                                    s['separated_at_2000'], s['separated_2000_resolved_by_end'], s['separated_2000_end_outcomes'],
                                                                    s['resolution_events'], s['separated_run_generations'], fmt(s['h_res_per_run_gen']), fmt(s['flip_rate_per_island_gen'])))
    w('')
    w('**Establishment and the pooling check** (a set *won* = universal with every holder in the set; decided = some set won):')
    w('')
    w('| cell | first island at P(C,C) ≥ 0.9 (median gen) | every island held (median gen; runs) | maximal cliques per run (median) | decided @2,000 / @10,000 | largest seeded set won @10,000 | largest established set won @10,000 |')
    w('|---|---|---|---|---|---|---|')
    for c in CELL_ORDER + EXTRA:
        if c not in cells: continue
        s = cells[c]; pc = s['pooling']
        w('| %s | %s | %s (%d) | %s | %d / %d | %d / %d | %d / %d |' % (CELL_DESC.get(c, c), fmt(s['establish_gen_median']), fmt(s['all_established_gen_median']),
                                                               s['n_all_established'], fmt(pc['n_sets_median']), pc['h2000']['decided'], pc['end']['decided'],
                                                               pc['end']['best_seed_won'], pc['end']['decided'], pc['end']['best_est_won'], pc['end']['best_est_n']))
    w('')
    w('**Tracked classes** (runs seeded / runs in which it ever held an island / runs in which it was extinct by the end; median extinction generation):')
    w('')
    groups = ['MC1', 'MC2', 'OF1', 'AF1', 'TC1^1', 'XC', "XC'", 'EQ', 'CB', 'TwinD']
    w('| cell | ' + ' | '.join(groups) + ' | marked carrier alive at first separation |')
    w('|---|' + '---|' * (len(groups) + 1))
    for c in CELL_ORDER + EXTRA:
        if c not in cells: continue
        tr = cells[c]['track']
        cellv = []
        for g in groups:
            x = tr.get(g)
            cellv.append('%d / %d / %d (%s)' % (x['runs_seeded'], x['ever_held_island'], x['extinct'], fmt(x['median_extinction'])) if x else '–')
        mc = tr.get('MC1')
        w('| %s | %s | %s |' % (CELL_DESC.get(c, c), ' | '.join(cellv), '%d / %d' % (mc['alive_at_first_sep'], mc['alive_at_first_sep_n']) if mc else '–'))
    w('')
    w('**Who is separated from whom** (runs with islands of both labels / with any island of the label, @2,000 → @10,000):')
    w('')
    w('| cell | identity & open | identity majority | exclusive & open | any exclusive island | any tag-club island |')
    w('|---|---|---|---|---|---|')
    for c in CELL_ORDER + EXTRA:
        if c not in cells: continue
        co = cells[c]['cooccur']; a_, b_ = co['h2000'], co['end']
        w('| %s | %d → %d | %d → %d | %d → %d | %d → %d | %d → %d |' % (CELL_DESC.get(c, c), a_['identity_and_open'], b_['identity_and_open'],
                                                                 a_['identity_majority'], b_['identity_majority'], a_['exclusive_and_open'], b_['exclusive_and_open'],
                                                                 a_['any_exclusive'], b_['any_exclusive'], a_['any_tag_club'], b_['any_tag_club']))
    w('')
    yl = load('yields.json')
    if yl:
        w('**Islands per seeded copy** (islands held at 2,000 / 10,000 per seeded copy of the label, all runs of the cell pooled; '
          'the pooling question by raw counts):')
        w('')
        w('| cell | open | identity | other | exclusive | identity copies seeded per run | open copies per run |')
        w('|---|---|---|---|---|---|---|')
        for c in CELL_ORDER + EXTRA:
            if c not in yl: continue
            y = yl[c]; ip = y['islands_per_seeded_copy']; sp = y['seeded_per_run']
            g = lambda k: '%.3f / %.3f' % tuple(ip[k]) if ip.get(k) and ip[k][0] is not None else '–'
            w('| %s | %s | %s | %s | %s | %.1f | %.1f |' % (CELL_DESC.get(c, c), g('open'), g('identity'), g('other'), g('exclusive'),
                                                         sp.get('identity', 0.0), sp.get('open', 0.0)))
        w('')
    ch = js.get('chain') or []
    if ch:
        w('## 4. The ε→0 chain (diagnostic)')
        w('')
        w('| label | N | P(C,C) | π(all-D) | π by label | top states (π, labels) | states | cut/flow | s |')
        w('|---|---|---|---|---|---|---|---|---|')
        for r in sorted(ch, key=lambda r: (r['label'], r['N'])):
            tops = '; '.join('`%s` %s %s' % (x['state'][:70], fmt(x['pi']), x['labels']) for x in r['support'][:4])
            w('| %s | %d | %.4f | %s | %s | %s | %d | %s | %.0f |' % (r['label'], r['N'], r['pcc'], fmt(r['pi_D']),
              {k: round(v, 4) for k, v in r['pi_by_label'].items() if v > 1e-3}, tops, r['n_recurrent'], fmt(r['cut_rel']), r['time_s']))
        w('')
    return o


def chain_summary(ch):
    out = {}
    for r in ch:
        top = r['support'][0] if r['support'] else None
        out[(r['label'], r['N'])] = dict(pcc=r['pcc'], top=top['state'] if top else None, top_pi=top['pi'] if top else None,
                                         top_labels=top['labels'] if top else None, pi_identity=r['pi_by_label'].get('identity', 0.0),
                                         pi_open=r['pi_by_label'].get('open', 0.0), pi_D=r['pi_D'])
    return out


def verdicts(js, cells):
    """The verdict table (scored by the conventions of the predictions file and its endpoint revision)."""
    ch = chain_summary(js.get('chain') or [])
    m10 = ch.get(('main', 10000)); n3 = ch.get(('noclosed', 1000)); n4 = ch.get(('noclosed', 10000))
    c7 = ('**held**: top state at N = 10⁴ `%s` (π %.3f, labels %s); π on identity cliques %.3f' % (m10['top'], m10['top_pi'], m10['top_labels'], m10['pi_identity'])
          if m10 and m10['top_labels'] and all(l == 'identity' for l in m10['top_labels']) else
          ('**failed**: top state `%s` (%s)' % (m10['top'], m10['top_labels']) if m10 else 'not run'))
    if n3 and n4 and 0 < n3['pcc'] < 1 and 0 < n4['pcc'] < 1:
        import math as _m
        slope = (_m.log(n4['pcc'] / (1 - n4['pcc'])) - _m.log(n3['pcc'] / (1 - n3['pcc']))) / _m.log(10)
        ctrl = 'no-clique control P(C,C) %.3f / %.3f at 10³ / 10⁴, odds slope %.2f, top state `%s` (%s)' % (n3['pcc'], n4['pcc'], slope, n4['top'], n4['top_labels'])
    else:
        slope = None
        ctrl = 'no-clique control: %s' % ({k: v['pcc'] for k, v in ch.items()} if ch else 'not run')
    L_ = cells['L']
    rows = [
        ('RE 1', 'clique cheap (within 4× of CB) but one class; F_CB ≥ 10× any clique',
         '**held** (EQ and CB spellings both 1.94·10⁻⁴; every eq spelling its own class; M = 0.031 = 162 × the heaviest identity clique; falsifier not fired). '
         'But the 322 identity cliques together weigh 0.009, and the heaviest pairwise-compatible set is a defection-detector set (0.034), not F_CB'),
        ('RE 2', 'open family universal on ≥ 0.7 at (100, 64); no clique win; largest established set wins ≥ 0.9 and beats raw counts',
         '**failed, falsifier fired** (universal-open %d/40 at 2,000, %d/40 at 10,000; the largest-established set won in %d of 40 runs because no set won the rest). '
         'No clique win (0) held; where a set won anywhere the largest-established set won 3/3 (L) and 29/29, 29/30, 32/33 (ablations, no-clique cell) against 0/3, 0/29, 1/30, 3/33 for raw counts' % (
             L_['h2000']['universal_open'], L_['end']['universal_open'], L_['pooling']['end']['best_est_won'])),
        ('RE 3', 'T1a clique wins 0.3–0.7; T1b and T1c carriers ≥ 0.8; T1b ≪ T1a',
         '**failed, falsifier fired**: clique wins 0/40 (T1a; 2/40 by 10,000), carriers win 0/40 (T1b) and 1/40 (T1c; 7/40 by 10,000); T1b ≥ T1a on wins (0 = 0), and on islands held by eq-cliques T1b 0.78 against T1a 0.82 at 2,000 '
         '(islands per seeded copy 0.197 against 0.204): incompatible spellings establish as well as one identity. T1b < T1a only later (0.72 against 0.91 at 10,000)'),
        ('RE 4', 'tag club rivals carriers; marked carrier resolves (≤ 0.2 separated where alive); no and-form resolution',
         '**falsifier fired as worded** (10/10 runs with a living marked carrier at the first separation were separated at 2,000), but the rivalry it addresses never formed: '
         'TC1¹ at mass M held an island in 33/40 runs and was extinct by the end in 39/40 (median generation 110), eaten by marked defectors; the separations are with identity cliques, which no bridge reaches. '
         'No resolution through the and-form (AF¹ never held an island)'),
        ('RE 5', 'XC bridge-less; ≥ 0.3 separated XC/carriers; none resolves by 10,000',
         '**falsifier fired**: bridge-less held (0 classes cooperate with CB and XC, by soundness); separated XC/open in 40/40 at 2,000 held; but the XC–open rivalry resolved by majority in 9 of 40 runs by 10,000 (open family lost, no bridge), XC holding 0.73 → 0.91 of islands'),
        ('RE 6', '(200, 64) and (100, 256) within 0.15 of (100, 64); separation hazard falling in N; resolution hazard rising in I',
         '**held as worded, vacuously** (universal 0/40 in all three; falsifier not fired); P(ever separated) = 1 in every cell so the per-pair hazard is saturated; the resolution clause **failed** '
         '(resolution events 4 at (100, 64), 0 at (100, 256), 0 at (200, 64)); N = 200 freezes the patchwork; I = 256 absorbs clique islands slowly (identity share 0.36 → 0.17) without resolving a run'),
        ('RE 7', 'chain absorbed by the eq-clique or TwinD at N = 10⁴', c7),
        ('S1', 'hand table by whole plays', '**held** (196/196)'),
        ('S2', 'Lemma T′/R: 0 mismatches on ≥ 2,000 pairs', '**held** (0/4,946; every n ≤ 4 pair and 1,500+ at n ≤ 5 in the tests)'),
        ('S3', '≤ 1% of milestone-2 lists change', '**held** (0/12,546)'),
        ('S4', 'classes > 2,500, full grammar computable in < 3 h', '**held** (3,974 classes, 20 min on 2 workers)'),
        ('S5', 'M in [0.005, 0.05]; heaviest identity clique EQ; identity total ≤ 0.01', '**held** (0.031; EQ 1.94·10⁻⁴; 0.0090)'),
        ('S6', 'detector rivals heavier than any identity clique', '**held** (`if(CHK(them,⌜C⌝,D),D,C)` 0.0047 mutually defects with CB; the heaviest set without CB 0.034 > M)'),
        ('S7', 'L: E3 ≥ 0.9; universal-open ≥ 0.5; separated ≤ 0.3; no clique win', '**failed, falsifier fired** (E3 40/40 and no clique win held; universal-open 0/40 < 0.3; separated 40/40)'),
        ('S8', 'largest established set beats largest seeded set by ≥ 0.1', '**held** on the decided runs (largest-established set won %d of %d, largest-seeded set %d of %d, pooled over all cells at 10,000; only 3 decided runs under L)' % (
            sum(s['pooling']['end']['best_est_won'] for s in cells.values()), sum(s['pooling']['end']['decided'] for s in cells.values()),
            sum(s['pooling']['end']['best_seed_won'] for s in cells.values()), sum(s['pooling']['end']['decided'] for s in cells.values()))),
        ('S9', 'T1a eq-clique holds every island in [0.2, 0.6] by 10,000; T1b ≤ 0.1; T1c universal ≥ 0.6', '**failed, falsifier fired** (T1a 2/40 < 0.1; T1b 0; T1c 7/40)'),
        ('S10', 'T2: club establishes ≥ 0.7; marked D takes its islands; marked carrier alive at first separation ≤ 0.3; club wins ≤ 0.1', '**held** (33/40; extinct 39/40; 10/40; 0)'),
        ('S11', 'T3: XC establishes ≥ 0.8; separated ≥ 0.3; ≥ 0.2 of separations resolve by majority by 10,000', '**held** (40/40; 40/40; the XC–open rivalry resolved in 9/40 = 0.23; run-level patchworks persist through identity cliques)'),
        ('S12', '(200, 64) within 0.15; (100, 256) lower by ≥ 0.1', 'first clause **held** (0 = 0); second **failed, number** (0 = 0; falsifier "higher" not fired)'),
        ('S13', 'U universal-open ≥ 0.4, clique wins ≤ 0.1; ablations within 0.2 of L', '**failed** (U 0/40, identity cliques hold 0.73 of islands, clique wins 0; tags-only 18/40 and ⌜CB⌝-only 22/40 against L 0/40); falsifier (clique wins > 0.2) not fired'),
        ('S14', 'chain absorbed by identity cliques, top EQ; no-clique control: open top state, P(C,C) [0.4, 0.95], slope [0.3, 0.7]',
         (c7 + '; ' + ctrl) if m10 else 'not run'),
    ]
    return rows


if __name__ == '__main__':
    js, cells = main()
    lines = md(js, cells)
    lines.append('## 6. Verdicts')
    lines.append('')
    lines.append('| # | prediction | outcome |')
    lines.append('|---|---|---|')
    for a_, b_, c_ in verdicts(js, cells):
        lines.append('| %s | %s | %s |' % (a_, b_, c_))
    lines.append('')
    extra = os.path.join(OUT, 'report_tail.md')
    if os.path.exists(extra):
        lines += open(extra).read().split('\n')
    open(os.path.join(ROOT, 'runs', 'identity-tags.md'), 'w').write('\n'.join(lines) + '\n')
    json.dump(js, open(os.path.join(ROOT, 'runs', 'identity-tags.json'), 'w'), indent=1, default=str)
    for c, s in cells.items():
        h = s['h2000']; e = s['end']
        print('%-14s n=%d univ-open %d other %d patch %d fail %d unres %d | sep2000 %d resolved-by-end %d | end univ-open %d patch %d | cross %.3f / %.3f clique wins %d' % (
            c, s['n'], h['universal_open'], h['universal_other'], h['patchwork'], h['failed'], h['unresolved'], s['separated_at_2000'],
            s['separated_2000_resolved_by_end'], e['universal_open'], e['patchwork'], h['cross_pcc'], e['cross_pcc'], h['clique_wins']))
