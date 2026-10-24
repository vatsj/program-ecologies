"""The soundness test (prediction 1; run before any counted cell): writes runs/lt_tape/soundness.json."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lt_tape_audit as A

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K0 = 10000

if __name__ == '__main__':
    out = {}
    t0 = time.time()
    for game in ('insp', 'rps'):
        for arm in ('full', 'prand'):
            out['%s_%s' % (game, arm)] = A.pair_soundness(game, K0, arm=arm)
            print(game, arm, {k: v for k, v in out['%s_%s' % (game, arm)].items() if k not in ('bad', 'play_disagree_examples')},
                  round(time.time() - t0), flush=True)
    out['adaptive_and_certificates'] = A.run_all(K=3000)
    print('adaptive', out['adaptive_and_certificates']['adaptive'], round(time.time() - t0), flush=True)
    os.makedirs(os.path.join(ROOT, 'runs', 'lt_tape'), exist_ok=True)
    with open(os.path.join(ROOT, 'runs', 'lt_tape', 'soundness.json'), 'w') as f:
        json.dump(out, f, indent=1, default=str)
