"""Mass on states with two or three conditional programs (handshakes) and the
top such states, from saved chains.

    python3 src/dollar3_handshakes.py <arm> <N> [tag]
Appends to runs/dollar3/handshakes.json.
"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import json, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import dollar3 as D
from dollar3_run import build_chain, describe, ROOT


def main():
    arm, N = sys.argv[1], int(sys.argv[2]); tag = sys.argv[3] if len(sys.argv) > 3 else ''
    f = np.load(os.path.join(ROOT, 'runs', 'dollar3', '%s_N%d%s_chain.npz' % (arm, N, tag)))
    ch, S = build_chain(arm, N, 0.3, 1e-9, 10)
    codes, pi, typ = f['codes'], np.exp(f['lpi']), f['typ']
    K = ch.Kc
    c = np.stack([codes // (K * K), (codes // K) % K, codes % K], 1)
    ncond = sum((S.nat[s, ch.reps[s, c[:, s]]] > 0).astype(int) for s in range(3))
    out = dict(arm=arm, N=N, mass_by_conditional_count={int(k): float(pi[ncond == k].sum()) for k in range(4)},
               states_by_conditional_count={int(k): int((ncond == k).sum()) for k in range(4)})
    idx = np.nonzero(ncond >= 2)[0]
    out['top_multi_conditional'] = [dict(pi=float(pi[k]), state=describe(ch, codes[k]), type=D.OUT_NAMES[typ[k]]) for k in idx[np.argsort(-pi[idx])][:10]]
    path = os.path.join(ROOT, 'runs', 'dollar3', 'handshakes.json')
    allr = json.load(open(path)) if os.path.exists(path) else {}
    allr['%s_N%d%s' % (arm, N, tag)] = out
    json.dump(allr, open(path, 'w'), indent=1)
    print(json.dumps(out, indent=1)[:2500])


if __name__ == '__main__':
    main()
