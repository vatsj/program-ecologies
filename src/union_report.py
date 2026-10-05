"""Collect runs/union/*.json into runs/union.json and the tables of runs/union.md
(the prose of runs/union.md is written by hand around the tables printed here).

    python3 src/union_report.py > runs/union/tables.md
"""
import glob, json, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'runs', 'union')
SUMM = ['fair', 'intermediate', 'zero wage', 'strike', 'scab split', 'repression:strike', 'repression:source']


def f3(v):
    if v is None: return '–'
    if v == 0: return '0'
    if abs(v) < 1e-3: return '%.0e' % v
    return '%.3f' % v


def chain_tables(cells):
    L = ['## Chain: π by disjoint summary (fair / intermediate / zero wage / strike / scab split / repression:strike / repression:source)', '',
         '| arm | c | N | ' + ' | '.join(SUMM) + ' | efficiency | boss | worker | states | outcome cut |', '|' + '---|' * (len(SUMM) + 8)]
    for o in cells:
        L.append('| %s | %g | %g | %s | %.3f | %.3f | %.4f | %d | %.1e |' % (o['arm'], o['c'], o['N'], ' | '.join(f3(o['summary'][k]) for k in SUMM),
                 o['efficiency'], o['mean_payoff']['boss'], o['mean_payoff']['W1'], o['states'], o['rel_cut_change']))
    L += ['', '## Chain: wage and whack-policy distributions, conditional-program mass', '',
          '| arm | c | N | s = 0 / 1/4 / 1/2 | policy strike / none / source | mass with a conditional (boss / worker) | militant present | union or union′ present | tagged worker present |',
          '|---|---|---|---|---|---|---|---|---|']
    for o in cells:
        wd, hd, nm = o['wage_dist'], o['whack_policy_dist'], o['named_worker_presence']
        L.append('| %s | %g | %g | %s / %s / %s | %s / %s / %s | %s (%s / %s) | %s | %s | %s |' % (
            o['arm'], o['c'], o['N'], f3(wd['0']), f3(wd['1/4']), f3(wd['1/2']), f3(hd['strike']), f3(hd['none']), f3(hd['source']),
            f3(o['mass_with_conditional']), f3(o['mass_conditional_boss']), f3(o['mass_conditional_worker']), f3(nm.get('militant')),
            f3(nm.get('union', 0) + nm.get("union' (BOX(OTHER=strike))", 0)), f3(o['mass_tagged_worker_present'])))
    L += ['', '## Chain: dwell per visit (mutation events) and lumped relaxation time', '',
          '| arm | c | N | ' + ' | '.join(SUMM) + ' | relaxation |', '|' + '---|' * (len(SUMM) + 4)]
    for o in cells:
        L.append('| %s | %g | %g | %s | %.3g |' % (o['arm'], o['c'], o['N'], ' | '.join(('%.3g' % o['dwell_events'][k]) if o['dwell_events'][k] else '–' for k in SUMM),
                 o['lumped_relaxation_events']))
    L += ['', '## Chain: the drift race (π-weighted flow per mutation event)', '',
          '| arm | c | N | union or union′ into a worker slot | tagged class into a worker slot | source targeting into the boss slot | of which from states with a tagged worker | strike targeting into the boss slot |',
          '|---|---|---|---|---|---|---|---|']
    for o in cells:
        dr = o['drift']
        L.append('| %s | %g | %g | %.2e | %.2e | %.2e | %.2e | %.2e |' % (o['arm'], o['c'], o['N'], dr['union_like_into_worker_slot'], dr['tagged_into_worker_slot'],
                 dr['source_targeting_into_boss_slot'], dr['source_targeting_into_boss_from_tagged_states'], dr['strike_targeting_into_boss_slot']))
    return L


def main():
    cells = []
    for f in sorted(glob.glob(os.path.join(D, '*_c*_N*.json'))):
        o = json.load(open(f))
        cells.append(o)
    order = {'quorum': 0, 'noquorum': 1, 'blind': 2}
    cells.sort(key=lambda o: (order[o['arm']], o['c'], o['N']))
    L = chain_tables(cells)
    print('\n'.join(L))
    allj = dict(chain=cells, static=json.load(open(os.path.join(D, 'static.json'))),
                abm=[json.load(open(f)) for f in sorted(glob.glob(os.path.join(D, 'abm_*.json')))],
                islands=[json.load(open(f)) for f in sorted(glob.glob(os.path.join(D, 'islands_*.json')))])
    for o in allj['chain']:
        o.pop('rounds', None)
    json.dump(allj, open(os.path.join(ROOT, 'runs', 'union.json'), 'w'), indent=1, default=float)


if __name__ == '__main__':
    main()
