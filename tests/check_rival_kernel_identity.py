"""Draw-for-draw identity of the k = 1 path of rival_islands._kern against the pre-propagule kernel
(src/rival_islands.py at commit ca3cc7f, read from git).  Usage: python3 tests/check_rival_kernel_identity.py"""
import importlib.util, os, subprocess, sys, tempfile
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'src')
sys.path.insert(0, SRC)
import rival_islands as R

old = subprocess.run(['git', 'show', 'ca3cc7f:src/rival_islands.py'], cwd=os.path.join(HERE, '..'),
                     capture_output=True, text=True, check=True).stdout
tmp = os.path.join(SRC, '_rival_islands_ca3cc7f.py')
open(tmp, 'w').write(old.replace('@njit(cache=True)', '@njit'))
try:
    spec = importlib.util.spec_from_file_location('rival_old', tmp)
    O = importlib.util.module_from_spec(spec); spec.loader.exec_module(O)
finally:
    os.remove(tmp)

d = R.cls(9)
bad = 0; n = 0
for preset, pair in (('AB', 0), ('AB', 2), ('iid', None), ('halfAB', 0)):
    for N, I, mN, gens in ((100, 16, 1.0, 3000), (100, 8, 0.1, 3000), (50, 4, 3.0, 2000)):
        for rep in range(4):
            rng = np.random.default_rng([7, rep, N, I])
            init, pre, A, B = R.build_init(d, N, I, pair, preset, rng)
            sup, U, PCC, coop, tag = R.restrict(d, init, A, B)
            K = len(sup); rr = np.random.default_rng(rep); r1 = rr.random(K); r2 = rr.random(K)
            iDl = int(np.searchsorted(sup, d['iD'])) if d['iD'] in set(sup.tolist()) else -1
            li = np.ascontiguousarray(init[:, sup]); ch = R.checks_schedule(gens); seed = 1000 + rep
            a = O._kern(U, PCC, coop, tag, li, N, R.W, mN / N, seed, ch, True, iDl, r1, r2, pre)
            b = R._kern(U, PCC, coop, tag, li, N, R.W, mN / N, seed, ch, True, iDl, r1, r2, pre, 1)
            ok = True
            for k, (x, y) in enumerate(zip(a, b[:28])):
                if k == 5:
                    y = y[:, :12]
                if not np.array_equal(np.asarray(x), np.asarray(y)):
                    ok = False; print('MISMATCH', preset, pair, N, I, mN, rep, 'output', k)
            n += 1; bad += (not ok)
print('%d / %d runs identical draw for draw' % (n - bad, n))
