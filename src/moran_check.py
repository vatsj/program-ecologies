"""Moran check: finite-N simulation vs the chain's pi, per selection intensity w.

For each (arm, game, n, N, w): the chain's pi by majority type and the Moran
process's occupancy by majority type (fitness 1 + w * payoff in both), at
mutation rates eps with eps*N in {0.1, 1}.  Prints a markdown table.
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from dsl import Language
from game import Game
from chain import Chain
from moran import simulate, chain_occupancy
import run

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check(arm, game_name, n, N, ws=(0.01, 0.1, 1.0), epss=(0.001, 0.01), steps=4_000_000, seed=1, top=4):
    game = Game.load(os.path.join(ROOT, 'games', game_name + '.yaml'))
    L = Language(arm, n, role=game.role)
    prov, div = run.get_provider(L, game, arm, n, True, 'square', False)
    reps = [c[0] for c in prov.classes]; mu = np.array([c[2] for c in prov.classes]); U = prov.U(reps)
    lines = ['### %s arm, %s, n=%d, N=%d' % (arm, game_name, n, N), '',
             '| w | eps | type | chain pi (majority) | Moran (majority) | Moran (present) |', '|---|---|---|---|---|---|']
    for w in ws:
        ch = Chain(prov, N=N, w=w).explore()
        occ_c, maj_c = chain_occupancy(ch, prov)
        for eps in epss:
            t = time.time()
            occ_m, maj_m = simulate(U, mu, N, eps, steps, w=w, seed=seed)
            present = {}
            for sup, v in occ_m.items():
                for k in sup:
                    present[k] = present.get(k, 0) + v
            keys = sorted(set(maj_c) | set(maj_m), key=lambda k: -(maj_c.get(k, 0) + maj_m.get(k, 0)))[:top]
            for k in keys:
                lines.append('| %g | %g | `%s` | %.3f | %.3f | %.3f |' % (w, eps, L.src(reps[k]), maj_c.get(k, 0), maj_m.get(k, 0), present.get(k, 0)))
    return '\n'.join(lines)


if __name__ == '__main__':
    out = []
    for arm, game, n, N in [('strong', 'pd', 6, 100), ('weak', 'pd', 6, 100)]:
        out.append(check(arm, game, n, N))
        print(out[-1], flush=True)
    with open(os.path.join(ROOT, 'runs', 'moran_check.md'), 'w') as f:
        f.write('\n\n'.join(out) + '\n')
