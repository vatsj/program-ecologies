"""Family counts under level1 (box1 admitted) for several word lengths, to check the quotient is stable."""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import hooks_beh as HB
from collections import Counter

for atoms in (HB.ATOMS, ('c', 'd')):
    for L in (4, 5, 6):
        t = time.time()
        F = HB.Family(atoms, L=L)
        print(atoms, 'L', L, 'classes', len(F.classes), 'constants', len(F.constants), 'a(s)', [int(x) for x in F.a[2:]],
              dict(sorted(Counter(v['size'] for v in F.classes).items())), '%.1fs' % (time.time() - t), flush=True)
