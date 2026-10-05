"""Compile runs/dollar3/*.json into runs/three-player-dollar.md and .json.

    python3 src/dollar3_report.py
"""
import glob, json, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARMS = ['constants', 'weak', 'modalPA', 'modal']
NS = [100, 1000, 10000]
T = ['grand', 'fair pair', 'unfair pair', 'wasteful pair', 'disagreement']


def load():
    cells = {}
    for arm in ARMS:
        for N in NS:
            f = os.path.join(ROOT, 'runs', 'dollar3', '%s_N%d.json' % (arm, N))
            if os.path.exists(f):
                cells[(arm, N)] = json.load(open(f))
    extra = {}
    for f in glob.glob(os.path.join(ROOT, 'runs', 'dollar3', '*_N*_*.json')):
        if f.endswith('_chain.json'): continue
        extra[os.path.basename(f)[:-5]] = json.load(open(f))
    abm = json.load(open(os.path.join(ROOT, 'runs', 'dollar3', 'abm.json'))) if os.path.exists(os.path.join(ROOT, 'runs', 'dollar3', 'abm.json')) else None
    return cells, extra, abm


def fmt(x, d=4):
    return ('%.' + str(d) + 'f') % x if isinstance(x, (int, float)) and x == x else str(x)


def main():
    cells, extra, abm = load()
    L = ['# Three-player majority divide-the-dollar: runs (2026-10-04)', '',
         'Spec `specs/2026-10-04-three-player-dollar.md`; predictions `predictions/2026-10-04-three-player-dollar.md` '
         '(committed before any run). Code: `src/dollar3*.py`. Per-cell data: `runs/dollar3/<arm>_N<N>.json` '
         '(and `_chain.npz`: explored states, log π, kept edges).', '',
         'ε→0 chain over monomorphic triples of payoff classes, w = 0.3, exact constant-selection Moran fixation. '
         'n = 6 (one-atom conditionals). The chain is solved on an explored subset; "cut" is the π-weighted rate of '
         'transitions leaving it (folded into self-loops), relative to all transitions, and "outcome cut" the same for '
         'transitions that change the payoff vector. Method: constants = whole 729-state chain by GTH; others = '
         '"hybrid" (core by log-scaled GTH, ring eliminated by its stochastic complement).', '']
    L += ['## π by outcome type', '',
          '| arm | N | grand | fair pair | unfair pair | wasteful pair | disagreement | efficiency | E[max share] | P(some slot 0) | P(pair) | mass on states with a conditional | states | outcome cut |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for (arm, N), j in sorted(cells.items(), key=lambda kv: (ARMS.index(kv[0][0]), kv[0][1])):
        m = j['mass_by_type']
        L.append('| %s | %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %d | %s |' % (
            arm, N, *[fmt(m[t]) for t in T], fmt(j['efficiency']), fmt(j['E_max_share']), fmt(j['P_some_slot_zero']), fmt(j['P_pair']),
            fmt(j.get('mass_with_conditional', 0)), j['states'], ('%.1e' % j['rel_cut_change']) if j.get('rel_cut_change') == j.get('rel_cut_change') and 'rel_cut_change' in j else '—'))
    L += ['', '## Currents and dwell', '',
          'C is the net circulation P12→P13→P23→P12 (π-weighted, per mutation event); it must vanish by relabeling symmetry. '
          '"bids in" = pair-to-pair moves made by the excluded slot; "pivot" = by the member that stays; "dropped" = by the member that leaves. '
          'Dwell is per visit, in mutation events. Relaxation: the lumped 5-type chain (an estimate).', '',
          '| arm | N | C | pair→pair flow | bids in | pivot | dropped | entry X→G | entry X→pairs | dwell G | dwell pair | dwell X | relaxation | max rel. π asymmetry under relabeling (top 2000) |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for (arm, N), j in sorted(cells.items(), key=lambda kv: (ARMS.index(kv[0][0]), kv[0][1])):
        c = j['circulation']; r = j['pair_to_pair_by_mover']; e = j['entry_rate_from_X']; d = j['dwell_events']
        L.append('| %s | %d | %.1e | %.2e | %.2e | %.2e | %.2e | %.2e | %.2e | %.3g | %.3g | %.3g | %.3g | %.1e |' % (
            arm, N, c['C'], c['total_pair_to_pair'], r['excluded_bids_in'], r['pivot_switches'], r['dropped_slot_moves'],
            e['G'], e['P12'] + e['P13'] + e['P23'], d['G'], d['P12'], d['X'], j['lumped_relaxation_events'], j['relabel_pi_max_rel_diff_top2000']))
    for (arm, N), j in sorted(cells.items(), key=lambda kv: (ARMS.index(kv[0][0]), kv[0][1])):
        start = len(L)
        L += ['', '### %s, N = %d' % (arm, N), '']
        L.append('Support (top 8 of %d states):' % j['states']); L.append('')
        for s in j['support'][:8]:
            L.append('- %.4f `%s` (%s, payoffs %s)' % (s['pi'], s['state'], s['type'], s['pay']))
        if j.get('top_conditional'):
            L.append(''); L.append('Top states with a conditional program: ' + '; '.join('%.2e `%s` (%s)' % (c['pi'], c['state'], c['type']) for c in j['top_conditional'][:5]))
        L.append(''); L.append('Transitions out of the top states (probability per mutation event):'); L.append('')
        for t in j['transitions'][:4]:
            L.append('- `%s` (π %.4f): ' % (t['state'], t['pi']) + '; '.join('%.2e → `%s`' % (x['p'], x['to']) for x in t['top'][:3]))
        L.append(''); L.append('Efficient triples (top by π): exit decomposition by prior mass per mutation event; bridges; exit rates at this N.'); L.append('')
        L.append('| π | state | type | strict | neutral-change | neutral-keep | deleterious | bridge mass | n bridges | drift-closed (depth 2) | exit rate strict / neutral / deleterious | entry from X |')
        L.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
        for t in j['efficient_triples'][:8]:
            dd = t['decomposition']; er = t.get('exit_rates', dict(strict=float('nan'), neutral_change=float('nan'), neutral_keep=float('nan'), deleterious=float('nan')))
            L.append('| %.4f | `%s` | %s | %.2e | %.2e | %.2e | %.2e | %.2e | %d | %s | %.1e / %.1e / %.1e | %.1e |' % (
                t['pi'], t['state'], t['type'], dd['strict'], dd['neutral-change'], dd['neutral-keep'], dd['deleterious'], t['bridge_mass'], t['n_bridges'],
                t['drift_closed_depth2'], er['strict'], er['neutral_change'] + er['neutral_keep'], er['deleterious'], t['entry_rate_from_X']))
        ex = [t for t in j['efficient_triples'][:3] if t.get('bridge_examples')]
        for t in ex[:2]:
            b = t['bridge_examples'][0]
            L.append(''); L.append('Bridge example from `%s`: slot %d drifts to `%s` (μ %.1e), then slot %d `%s` (%s, ρ %.2e) gives payoffs %s.' % (
                t['state'], b['slot'], b['entrant'], b['mass'], b['then_slot'], b['then'], b['then_kind'], b['then_rho'], b['then_pay']))
        p1 = j['p1_sweep']
        L.append(''); L.append('P1 sweep: %d efficient states with π ≥ 1e-6 checked (π mass %.4f); drift-closed at depth 2: %d (mass %.2e)%s.' % (
            p1['checked'], p1['checked_mass'], len(p1['closed']), p1['closed_mass'], (': ' + '; '.join('`%s` %.1e' % (c['state'], c['pi']) for c in p1['closed'][:5])) if p1['closed'] else ''))
        if arm == 'weak':     # atoms are simulated, not proved
            L[start:] = [x.replace('BOX(', 'SIM(') for x in L[start:]]
    piv = os.path.join(ROOT, 'runs', 'dollar3', 'pivots.json')
    if os.path.exists(piv):
        pv = json.load(open(piv))
        L += ['', '## Pair-to-pair moves and net currents between outcome types', '',
              'Pair-to-pair moves that change payoffs, by the pivot\'s share before -> after (the pivot is the member that stays and switches partner; '
              'π-weighted flow per mutation event). Net current between outcome types: J(a->b) - J(b->a), positive entries only.', '']
        for k in sorted(pv):
            if 'ring' in k or 'theta' in k: continue
            r = pv[k]
            L.append('- `%s`: %s. Net: %s.' % (k[:-0] if False else k, ', '.join('%s %.2e' % kv for kv in list(r['pair_moves'].items())[:5]),
                     ', '.join('%s %.2e' % kv for kv in r['net_type_current'].items() if kv[1] > 1e-12)))
    hs = os.path.join(ROOT, 'runs', 'dollar3', 'handshake_exits.json')
    if os.path.exists(hs):
        h = json.load(open(hs))
        L += ['', '## Hand-built handshakes (N = 1000): do conditional pairs or grand coalitions leak less than constants?', '',
              '| arm | triple | outcome | strict | neutral keep | neutral change | deleterious | bridge mass | n bridges |', '|---|---|---|---|---|---|---|---|---|']
        for k, r in h.items():
            arm, name = k.split('|')
            e = r['exit_rates']
            L.append('| %s | %s | %s | %.2e | %.2e | %.2e | %.2e | %.2e | %d |' % (arm, name, r['outcome'], e['strict'], e['neutral_keep'], e['neutral_change'], e['deleterious'], r['bridge_mass'], r['n_bridges']))
    hm = os.path.join(ROOT, 'runs', 'dollar3', 'handshakes.json')
    if os.path.exists(hm):
        h = json.load(open(hm))
        L += ['']
        for k, r in h.items():
            L.append('- `%s`: π mass by number of conditional slots %s (states %s).' % (k, {a: round(b, 4) for a, b in r['mass_by_conditional_count'].items()}, r['states_by_conditional_count']))
    named = os.path.join(ROOT, 'runs', 'dollar3', 'named.json')
    if os.path.exists(named):
        nd = json.load(open(named))
        L += ['', '## Named efficient triples: exits, bridges, invasion tables', '',
              'Exit rates are probabilities per mutation event at that N (strict = mutant gains; neutral = mutant\'s payoff unchanged, outcome kept or changed; deleterious). '
              'Bridge mass: prior mass per mutation event of outcome-keeping neutral entrants after which a strict or outcome-changing neutral exit exists. '
              'Drift-closed (depth 2): no strict exit, no outcome-changing neutral exit, no bridge.', '',
              '| arm | N | triple | strict | neutral keep | neutral change | deleterious | bridge mass | n bridges | drift-closed |', '|---|---|---|---|---|---|---|---|---|---|']
        for k, r in nd.items():
            arm, N, name = k.split('|')
            e = r['exit_rates']
            L.append('| %s | %s | %s | %.2e | %.2e | %.2e | %.2e | %.2e | %d | %s |' % (arm, N, name, e['strict'], e['neutral_keep'], e['neutral_change'], e['deleterious'],
                                                                               r['bridge_mass'], r['n_bridges'], r['drift_closed_depth2']))
        for k, r in nd.items():
            if r.get('bridge_examples'):
                arm, N, name = k.split('|')
                b = r['bridge_examples'][0]
                line = '- %s, %s: slot %d drifts to `%s` (μ %.1e per slot), then slot %d plays `%s` (%s, ρ %.2e at N = 100), payoffs %s.' % (
                    arm, name, b['slot'], b['entrant'], b['mass'], b['then_slot'], b['then'], b['then_kind'], b['then_rho'], b['then_pay'])
                L.append(line.replace('BOX(', 'SIM(') if arm == 'weak' else line)
    if extra:
        L += ['', '## Method checks', '']
        for k, j in sorted(extra.items()):
            m = j['mass_by_type']
            L.append('- `%s` (%s, %d states): %s; E[max] %.4f; outcome cut %s' % (k, j.get('method', '?'), j['states'],
                     ', '.join('%s %.4f' % (t, m[t]) for t in T), j['E_max_share'], ('%.1e' % j['rel_cut_change']) if 'rel_cut_change' in j else '—'))
    if abm:
        L += ['', '## Agent-based runs (finite εN = 0.1 per slot per generation; approach rates, not π)', '',
              'N = 100 per slot, ε = 10⁻³ per birth, w = 0.3, 10⁵ generations, records every 10 generations. Dominant label: outcome of the triple of majority classes, or "mixed".', '',
              '| arm | start | seed | grand | fair | unfair | wasteful | disagreement | pair runs | mean interior pair dwell (gens) | pair→pair switches | first gen with P(pair) > 0.5 |',
              '|---|---|---|---|---|---|---|---|---|---|---|---|']
        for o in abm['jobs']:
            m = o['mean_outcome']
            L.append('| %s | %s | %d | %.3f | %.3f | %.3f | %.3f | %.3f | %d | %s | %d | %s |' % (o['arm'], o['start'], o['seed'], *[m[t] for t in T], o['n_pair_runs'],
                     ('%.0f' % o['mean_pair_dwell_interior']) if o['mean_pair_dwell_interior'] else '—', o['pair_to_pair_switches'], o['first_gen_pair_prob_above_half']))
        for arm in sorted({o['arm'] for o in abm['jobs']}):
            dw = [o['mean_pair_dwell_interior'] for o in abm['jobs'] if o['arm'] == arm and o['mean_pair_dwell_interior']]
            if dw:
                L.append(''); L.append('%s: mean interior pair dwell across seeds and starts %.0f generations (range %.0f–%.0f, %d runs).' % (arm, np.mean(dw), min(dw), max(dw), len(dw)))
    head = os.path.join(ROOT, 'runs', 'dollar3', 'verdicts.md')
    if os.path.exists(head):
        L = L[:2] + open(head).read().rstrip('\n').split('\n') + [''] + L[2:]
    open(os.path.join(ROOT, 'runs', 'three-player-dollar.md'), 'w').write('\n'.join(L) + '\n')
    out = dict(cells={'%s_N%d' % k: {kk: v[kk] for kk in v if kk not in ('rounds',)} for k, v in cells.items()}, checks=extra, abm=abm)
    json.dump(out, open(os.path.join(ROOT, 'runs', 'three-player-dollar.json'), 'w'), indent=1, default=float)
    print('\n'.join(L[:40]))


if __name__ == '__main__':
    main()
