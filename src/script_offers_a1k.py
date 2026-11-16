"""Queue 80: are arm A1's (world S, canonical script carriers) and arm K's (world K, queue 79's skeleton carriers) tables identical on
the programs their laws use (the 59 base programs' constants, exploiters, bullies, F, R, and the canonical carriers matched by role)?
Compares action codes, failed reads and forfeits on every triple of the matched supports.

    python3 src/script_offers_a1k.py OUT.json
"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import script_offers_dyn as D

if __name__ == '__main__':
    S, K = D.tabs('S'), D.tabs('K')
    base = list(range(59))
    pairs = [(n + '.canon', n + '.canon') for n in ('Ocn', 'Ocp', 'Rcn', 'Rcp', 'FcSnoy', 'FcSpoy', 'Bcn', 'Bcp')]
    sidx = base + [S.names.index(a) for a, b in pairs]
    kidx = base + [K.names.index(b) for a, b in pairs]
    ix_s, ix_k = np.ix_(sidx, sidx, sidx), np.ix_(kidx, kidx, kidx)
    out = dict(triples=len(sidx) ** 3,
               code_diff=int((S.code[ix_s] != K.code[ix_k]).sum()),
               nto_diff=int((S.nto[ix_s] != K.nto[ix_k]).sum()),
               fo_diff=int((S.fo[ix_s] != K.fo[ix_k]).sum()),
               steps_equal=int((S.steps[ix_s] == K.steps[ix_k]).sum()))
    json.dump(out, open(sys.argv[1], 'w'), indent=1)
    print(out)
