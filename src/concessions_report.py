"""Markdown for the concessions run (runs/concessions.md) from runs/concessions-static.json, runs/concessions/*.json.

    python3 src/concessions_report.py named      # the named-program block for the predictions file
    python3 src/concessions_report.py all        # runs/concessions.md and runs/concessions.json
"""
import os, sys, json, glob
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
OUT = os.path.join(RUNS, 'concessions')

SHORTW = {'scab': 'scab', 'T0 (strike iff s = 0)': 'T0', 'T1 = militant (strike iff s <= 1/4)': 'T1', 'always strike': 'strike',
          'union': 'union', 'militant- (strike iff not BOX(s = 1/2))': 'mil-', 'T0- (strike iff not BOX(s in {1/4,1/2}))': 'T0-'}


def f(x, d=3):
    if x is None:
        return '–'
    if isinstance(x, str):
        return x
    if x != 0 and abs(x) < 10 ** (-d):
        return '%.1e' % x
    return ('%.' + str(d) + 'f') % x


def short_boss(k):
    return k.split(' = ')[0].split(' (')[0] if ' = ' in k or ' (' in k else k


def named_block(S, key='named_table_CC'):
    T = S[key]
    L = []
    L.append('**Named workers** (union-run grammar, level-0 boxes about the current encounter):\n')
    for k, v in T['worker_src'].items():
        L.append('- %s: `%s`' % (k, v))
    L.append('\n**Named bosses** (`W_j(^(s,none))` = worker j\'s play against the quoted constant boss (s, none) beside the current other worker):\n')
    for k, v in T['boss_src'].items():
        L.append('- %s: `%s`' % (k, v))
    L.append('\n**What the probes read** (quoted self-pair play, executed / recommended; fv = first world from which the strike probe fails, 127 = never):\n')
    L.append('| worker pair | vs (0,none) | vs (1/4,none) | fv strike@0 L0 / L1 | fv strike@1/4 L0 / L1 |')
    L.append('|---|---|---|---|---|')
    for k, v in T['quoted'].items():
        a, b = v['vs (0,none)'], v['vs (1/4,none)']
        L.append('| %s | %s / %s | %s / %s | %d / %d | %d / %d |' % (SHORTW[k], a['executed'], a['recommended'], b['executed'], b['recommended'],
                                                                 a['fv_strike_L0'], a['fv_strike_L1'], b['fv_strike_L0'], b['fv_strike_L1']))
    ws = T['workers']
    L.append('\n**Play and payoffs (boss, W1, W2) of every named boss against every named worker self-pair** (%s):\n' % key.split('_')[-1])
    L.append('| boss | ' + ' | '.join(SHORTW[w] for w in ws) + ' |')
    L.append('|---' * (len(ws) + 1) + '|')
    rows = {(r['boss'], r['W1'], r['W2']): r for r in T['rows']}
    for b in T['bosses']:
        cells = []
        for w in ws:
            r = rows[(b, w, w)]
            cells.append('%s (%s)' % (r['play'], ', '.join('%g' % v for v in r['pay'])))
        L.append('| %s | %s |' % (short_boss(b), ' | '.join(cells)))
    L.append('\n**Mixed pairs** (W1, W2) for the bosses that read W1 (probe, current-encounter and faker bosses):\n')
    mixed = [('T1 = militant (strike iff s <= 1/4)', 'scab'), ('scab', 'T1 = militant (strike iff s <= 1/4)'),
             ('T1 = militant (strike iff s <= 1/4)', 'T0 (strike iff s = 0)'), ('T0 (strike iff s = 0)', 'T1 = militant (strike iff s <= 1/4)'),
             ('T1 = militant (strike iff s <= 1/4)', 'always strike'), ('always strike', 'scab'), ('scab', 'always strike'),
             ('militant- (strike iff not BOX(s = 1/2))', 'scab')]
    L.append('| boss | ' + ' | '.join('%s, %s' % (SHORTW[a], SHORTW[b]) for a, b in mixed) + ' |')
    L.append('|---' * (len(mixed) + 1) + '|')
    for b in T['bosses']:
        if b.startswith('('):
            continue
        cells = []
        for a, c in mixed:
            r = rows[(b, a, c)]
            cells.append('%s (%s)' % (r['play'], ', '.join('%g' % v for v in r['pay'])))
        L.append('| %s | %s |' % (short_boss(b), ' | '.join(cells)))
    return '\n'.join(L)


def static_md(S):
    L = []
    L.append('### Languages (mass-preserving substitution)\n')
    L.append('| arm | grammar functions (n = 11) | included functions | boss classes | worker classes | boss mass included | merged by fingerprint | null (novel two-atom policies) | probe functions dropped (ref) | merge check failures |')
    L.append('|---|---|---|---|---|---|---|---|---|---|')
    for arm, I in S['languages'].items():
        L.append('| %s | %d | %d | %d | %d | %.4f | %.4f (%d) | %.4f (%d policies) | %.4f | %d / %d |' % (
            arm, I['grammar_functions'], I['included_functions'], I['KcB'], I['KcW'], I['boss_mass_included_functions'], I['boss_mass_merged'],
            I['merged_functions'], I['boss_mass_null'], I['novel_policies'], I['ref_probe_mass_dropped'], I['merge_verify_failures'], I['merge_verified']))
    L.append('')
    L.append('### Prior masses of the named classes\n')
    m = S['masses']
    keys = list(m['P01']['bosses'])
    L.append('| boss class | P01 | P0 | sham | ref |')
    L.append('|---|---|---|---|---|')
    for k in keys:
        if k.startswith('D*_'):
            continue
        L.append('| %s | %s |' % (short_boss(k), ' | '.join(f(m[a]['bosses'].get(k), 2) if m[a]['bosses'].get(k) is not None else '–' for a in ('P01', 'P0', 'sham', 'ref'))))
    L.append('| D* family (8 variants, each) | %s | – | – | – |' % f(m['P01']['bosses']['D*_1 L00'], 2))
    L.append('| all constants | %s |' % ' | '.join(f(m[a]['boss_constants'], 3) for a in ('P01', 'P0', 'sham', 'ref')))
    L.append('| all probe classes | %s |' % ' | '.join(f(m[a]['boss_probe_classes'], 3) for a in ('P01', 'P0', 'sham', 'ref')))
    L.append('\nWorker masses (all arms): ' + ', '.join('%s %s' % (SHORTW[k], f(v, 2)) for k, v in m['P01']['workers'].items()) + '.\n')
    return '\n'.join(L)


def states_md(S, arm):
    L = []
    L.append('| state | play | payoffs | strict B (mass; p/event at 10⁴) | neutral B | neutral W1 | neutral W2 | strict W | top move at N = 10⁴ | best excluded boss (gain; mass) |')
    L.append('|---|---|---|---|---|---|---|---|---|---|')
    for k, v in S['named_states'][arm].items():
        a = v['by_slot_kind']
        nB = a['B']['neutral-keep']['mass'] + a['B']['neutral-change']['mass']
        nW1 = a['W1']['neutral-keep']['mass'] + a['W1']['neutral-change']['mass']
        nW2 = a['W2']['neutral-keep']['mass'] + a['W2']['neutral-change']['mass']
        sW = a['W1']['strict']['mass'] + a['W2']['strict']['mass']
        t = v['top'][0]
        ea = S['excluded_audit'][arm][k]
        L.append('| %s | %s | %s | %s; %s | %s | %s | %s | %s | %s %s (%s, Δ %+g) | %s; %s |' % (
            k, v['play'], ', '.join('%g' % x for x in v['pay']), f(a['B']['strict']['mass'], 4), f(a['B']['strict']['p_N10000'], 2),
            f(nB, 3), f(nW1, 4), f(nW2, 3), f(sW, 4), t['slot'], '`%s`' % t['mutant'], t['kind'], t['du'],
            ('%+g' % ea['best_null']['gain']) if ea['best_null']['gain'] > 0 else 'none', f(ea['null_strict_mass'], 4)))
    return '\n'.join(L)


if __name__ == '__main__':
    S = json.load(open(os.path.join(RUNS, 'concessions-static.json')))
    if sys.argv[1] == 'named':
        print(named_block(S))
        print()
        print(static_md(S))
        for arm in ('P01', 'P0'):
            print('\n#### Named states, %s (CC, c = 0.5)\n' % arm)
            print(states_md(S, arm))
