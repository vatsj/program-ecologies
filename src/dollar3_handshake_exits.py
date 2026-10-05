"""Exit decomposition and bridges of hand-built handshake triples (two or
three conditional programs), against their constant counterparts.

    python3 src/dollar3_handshake_exits.py
Writes runs/dollar3/handshake_exits.json.
"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import json, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import dollar3 as D
from dollar3_run import build_chain, bridge_analysis, ROOT

TRIPLES = {
    'fair-pair handshake 12 (slot 3 (ALL,1/3))': ['if(BOX(2=(1,1/2)),(2,1/2),(ALL,1/3))', 'if(BOX(1=(2,1/2)),(1,1/2),(ALL,1/3))', '(ALL,1/3)'],
    'fair-pair constants 12 (slot 3 (ALL,1/3))': ['(2,1/2)', '(1,1/2)', '(ALL,1/3)'],
    'cyclic grand handshake 1<-2<-3<-1': ['if(BOX(2=(ALL,1/3)),(ALL,1/3),(ALL,2/3))', 'if(BOX(3=(ALL,1/3)),(ALL,1/3),(ALL,2/3))', 'if(BOX(1=(ALL,1/3)),(ALL,1/3),(ALL,2/3))'],
    'grand: two readers of each other + constant': ['if(BOX(2=(ALL,1/3)),(ALL,1/3),(ALL,2/3))', 'if(BOX(1=(ALL,1/3)),(ALL,1/3),(ALL,2/3))', '(ALL,1/3)'],
    'grand constants': ['(ALL,1/3)', '(ALL,1/3)', '(ALL,1/3)'],
}


def main():
    out = {}
    for arm in ('weak', 'modalPA', 'modal'):
        ch, S = build_chain(arm, 1000, 0.3, 1e-9, 10)
        for name, progs in TRIPLES.items():
            cl = []
            for s, txt in enumerate(progs):
                x = [x for x in range(S.K) if S.src(s, x) == txt][0]
                cl.append(int(ch.cls[s, x]))
            code = ch.code(*cl)
            # outcome of the triple
            hist = np.empty((2, 3), np.int64); val = np.empty(3, np.int64); u = np.empty(3, np.int64)
            t = D.enc_into(ch.ia, *ch.A, ch.reps[0, cl[0]], ch.reps[1, cl[1]], ch.reps[2, cl[2]], hist, val, u)
            ba = bridge_analysis(ch, code, examples=True)
            out['%s|%s' % (arm, name)] = dict(outcome=D.OUT_NAMES[t], pay=(u / 6).round(3).tolist(), **ba)
            print(arm, name, D.OUT_NAMES[t], {k: '%.2e' % v for k, v in ba['exit_rates'].items()}, 'bridge %.2e n %d' % (ba['bridge_mass'], ba['n_bridges']), flush=True)
    json.dump(out, open(os.path.join(ROOT, 'runs', 'dollar3', 'handshake_exits.json'), 'w'), indent=1, default=float)


if __name__ == '__main__':
    main()
