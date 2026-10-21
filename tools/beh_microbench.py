import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import numpy as np
import hooks_beh as HB
import hooks_w2 as H

B = HB.Beh()
N = HB.named_programs(B)
B.play(*N['FairBot'], *N['PrudentBot'])
B.play(*N['FairBot'], *N['PrudentBot'], full=True)
for full in (False, True):
    t = time.time()
    for _ in range(300):
        B.play(*N['PrudentBot'], *N['FairBot'], full=full)
    print('full', full, '%.2f ms per call (python overhead included)' % ((time.time() - t) / 300 * 1000))
print('R', B.R, 'keys', len(B.KT.keys))
