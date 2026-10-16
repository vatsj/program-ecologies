"""Diagnostic (post hoc, not predicted): how target islands become identity islands under rain (B3).  Replays one run
deterministically and prints the composition of the first islands that turn identity, before and after the flip."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import provenance as PV
import removing_rivals as RR


def comp(R, i, S, names):
    ks = R.pres[i, :R.npres[i]]
    rows = []
    for k in ks.tolist():
        u = int(R.tunit[k])
        rows.append((int(R.counts[i, k]), names[int(R.tsp[k])], u, 'T' if S['T'][u] else ('ID' if S['ident'][u] else
                     ('open' if S['openu'][u] else '-')), int(S['sa'][u]), int(R.lin[i, np.nonzero(R.slots[i] == k)[0][0]] > 0)))
    rows.sort(key=lambda z: -z[0])
    return rows


def main(cell, rep, gmax, nshow):
    R = RR.RRRun(cell, rep)
    S = RR.static(R.LS); names = R.LS['names']
    hist = {}
    flipped = []
    idshare_prev = np.zeros(R.I)
    while R.g < gmax and len(flipped) < nshow:
        R.advance(5)
        cc = R.island_stats()
        h = RR.holders(R, cc) if False else None
        for i in range(R.I):
            ks = R.pres[i, :R.npres[i]]
            ids = float((R.counts[i, ks] * S['ident'][R.tunit[ks]]).sum()) / R.N
            hist.setdefault(i, []).append((R.g, round(ids, 3), round(float(cc[i]), 3)))
            if ids >= 0.5 and idshare_prev[i] < 0.5 and R.g > 500 and i not in [f[0] for f in flipped]:
                flipped.append((i, R.g))
                print('island %d crosses 0.5 identity share at g %d' % (i, R.g))
                print('  identity share / island pcc history (every 5 gens, last 40):', hist[i][-40:])
                print('  composition now:', comp(R, i, S, names)[:8])
            idshare_prev[i] = ids
    print('done at', R.g, 'flipped', flipped)


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
