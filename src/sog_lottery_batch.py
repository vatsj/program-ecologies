"""Run the seed-lottery cells of src/sog_lottery.py in the spec's priority order (3 worker processes).

    python3 src/sog_lottery_batch.py [CELL ...]
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
import sog_lottery as S

ORDER = ['CC-main', 'RR-main', 'fact-hi-hostile', 'fact-hi-mostly', 'fact-lo-hostile', 'fact-lo-mostly', 'fact-lo-diverse',
         'sweep-0.06', 'sweep-0.24', 'noQ-CC', 'CC-N400', 'CC-I64', 'CC-mN0', 'CC-mN1', 'CC-pool', 'CC-cont', 'CC-c0.1',
         'RR-c0.1', 'RR-N400', 'noQ-RR']

if __name__ == '__main__':
    cells = sys.argv[1:] or ORDER
    for c in cells:
        if os.path.exists(os.path.join(S.OUT, '%s.json' % c)):
            print(c, 'exists, skipped', flush=True)
            continue
        t = time.time()
        S.run_cell(c, 3)
        print(c, 'done %.0fs' % (time.time() - t), flush=True)
