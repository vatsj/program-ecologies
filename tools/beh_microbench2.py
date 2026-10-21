import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import numpy as np
from numba import njit
import hooks_beh as HB
import hooks_w2 as H


@njit
def loop(LA, KA, iC, iD, bx, sx, by, sy, n):
    rs = np.zeros((2, KA[1].shape[0]), np.bool_)
    s = 0
    for i in range(n):
        ax, ay, _, _ = HB.eval_match_beh(LA[0], LA[1], LA[2], LA[3], LA[4], LA[5], LA[6], LA[7], LA[8], LA[9], LA[10], LA[11],
                                         iC, iD, KA[0], KA[1], KA[2], KA[3], False, bx, sx, sx, sx, by, sy, sy, sy, rs)
        s += ax + ay
    return s


B = HB.Beh()
N = HB.named_programs(B)
L = B.Lx
for a, b in (('PrudentBot', 'FairBot'), ('FairBot', 'FairBot'), ('TrustingBot', 'GodelPredator')):
    loop(B.LA, B.KT.arrays(), L.iC, L.iD, N[a][0], N[a][1], N[b][0], N[b][1], 2)
    t = time.time()
    loop(B.LA, B.KT.arrays(), L.iC, L.iD, N[a][0], N[a][1], N[b][0], N[b][1], 20000)
    print(a, b, '%.2f us per eval' % ((time.time() - t) / 20000 * 1e6))
# a typical hooked pair with random bases
rng = np.random.default_rng(0)
hooked = [i for i in range(len(L.base)) if L.b_tags[i] > 0]
tot = 0; t = time.time(); n = 0
for _ in range(50):
    bx = int(rng.choice(hooked)); by = int(rng.choice(hooked))
    loop(B.LA, B.KT.arrays(), L.iC, L.iD, bx, 0, by, 0, 400); n += 400
print('random hooked bases, no fills: %.2f us per eval' % ((time.time() - t) / n * 1e6))
