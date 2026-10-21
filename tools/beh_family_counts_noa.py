import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import hooks_beh as HB
for L in (7, 8):
    t = time.time()
    F = HB.Family(('c', 'd'), L=L)
    print('noA L', L, 'classes', len(F.classes), 'constants', len(F.constants), '%.1fs' % (time.time() - t), flush=True)
