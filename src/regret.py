"""Regret witnesses of population states.

For a mixture sigma over behavioural classes, r(q) = u(q, sigma) - u(sigma, sigma):
the large-N fitness advantage of a single q.  A state is no-regret iff
max_q r(q) <= 1e-9.  Writes runs/regret_witnesses.md.

    python3 src/regret.py
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from game import Game
from abm import load_or_evaluate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(game_name, norole=False):
    g = Game.load(os.path.join(ROOT, 'games', game_name + '.yaml'))
    if norole: g.role = False; g.nroles = 1
    _, _, _, _, _, U, PCC, _, names, _ = load_or_evaluate(g, 6, verbose=False)
    return U, PCC, names


def regret(U, names, mix, top=4):
    x = np.zeros(len(names))
    for k, v in mix.items(): x[names.index(k)] += v
    x /= x.sum()
    r = U @ x - x @ U @ x
    order = np.argsort(-r)
    return float(r[order[0]]), [(names[q], float(r[q])) for q in order[:top]], float(x @ U @ x)


def fmt(res):
    mx, top, pay = res
    return '%.3f | %.3f | %s' % (pay, mx, ', '.join('`%s` %.3f' % t for t in top if t[1] > 1e-9) or '—')


def main():
    L = ['# Regret witnesses (predictions in `predictions/2026-09-30-regret-witnesses.md`)', '',
         'r(q) = u(q, σ) − u(σ, σ); a state is no-regret iff max r ≤ 1e-9. Top witnesses with positive regret listed.', '',
         '| game | state | payoff u(σ,σ) | max regret | top witnesses |', '|---|---|---|---|---|']
    U, PCC, names = load('pd')
    for nm in ['D', 'THEM(^C)', 'X', 'ROLE']:
        L.append('| PD | all-`%s` | %s |' % (nm, fmt(regret(U, names, {nm: 1}))))
    L.append('| PD | all-`THEM(^C)`: regret of the shadow `C` | | %.3f | |' % (U[names.index('C'), names.index('THEM(^C)')] - U[names.index('THEM(^C)'), names.index('THEM(^C)')]))
    # frozen island runs
    rows = json.load(open(os.path.join(ROOT, 'runs', 'islands_pd.json')))
    iF = names.index('THEM(^D)')
    fams = {'coop': [], 'defect': [], 'other': []}
    for r in rows:
        fc = r['final_classes']
        mx, top, pay = regret(U, names, fc)
        kind = 'coop' if r['pcc_final'] > 1 - 1e-9 else ('defect' if r['pcc_final'] < 1e-9 and abs(r['pay_final'] + 1) < 1e-9 else 'other')
        tot = sum(fc.values())
        # share of sucker-cooperating defectors: classes that cooperate with ALLC-types, i.e. behave like THEM(^D) against the D family
        f = sum(v for k, v in fc.items() if U[names.index('not(THEM(^C))'), names.index(k)] > U[names.index('D'), names.index('D')] + 1e-9) / tot
        fams[kind].append((mx, top[0][0], f))
    for kind, lst in fams.items():
        mxs = np.array([m for m, _, _ in lst])
        wit = {}
        for m, w, _ in lst:
            if m > 1e-9: wit[w] = wit.get(w, 0) + 1
        extra = ''
        if kind == 'defect':
            zero = [f for m, _, f in lst if m <= 1e-9]; pos = [f for m, _, f in lst if m > 1e-9]
            extra = '; exploitable-by-`not(THEM(^C))` share: max %.2f in no-regret runs, min %.2f in positive-regret runs' % (max(zero) if zero else float('nan'), min(pos) if pos else float('nan'))
        L.append('| PD islands | frozen %s (%d runs) | | %d no-regret; max regret median %.3f, max %.3f | %s%s |' % (
            kind, len(lst), int((mxs <= 1e-9).sum()), np.median(mxs), mxs.max(), ', '.join('`%s` ×%d' % kv for kv in sorted(wit.items(), key=lambda kv: -kv[1])[:4]), extra))
    U, PCC, names = load('chicken')
    for nm in ['ROLE', 'not(ROLE)', 'THEM(^ROLE)', 'not(or(THEM(THEM),X))', 'not(or(THEM(ME),X))', 'THEM(ME)']:
        L.append('| Chicken+ROLE | all-`%s` | %s |' % (nm, fmt(regret(U, names, {nm: 1}))))
    U, PCC, names = load('chicken_norole', True)
    states = {'mixed-eq state: `not(THEM(ME))` 9/11 + Straight 2/11': {'not(THEM(ME))': 9, 'Straight': 2},
              'three-class cool state (0.659/0.195/0.146)': {'not(THEM(THEM))': 0.659, 'Straight': 0.195, 'not(THEM(^Straight))': 0.146},
              'two-class state `not(THEM(ME))` 0.627 + `not(or(X,THEM(ME)))` 0.372': {'not(THEM(ME))': 0.627, 'not(or(X,THEM(ME)))': 0.372},
              'all-`not(THEM(ME))` (frozen mutual Swerve)': {'not(THEM(ME))': 1}}
    for k, v in states.items():
        L.append('| Chicken no ROLE | %s | %s |' % (k, fmt(regret(U, names, v))))
    out = os.path.join(ROOT, 'runs', 'regret_witnesses.md')
    open(out, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))


if __name__ == '__main__':
    main()
