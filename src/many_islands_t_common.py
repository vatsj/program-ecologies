"""Shared helpers of the arm-T islands experiment: paths, cells, the cached tables and kernels, pool loading."""
import os, sys
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import many_islands_t as M
import many_islands_t_ode as O

SCR = M.SCR
OUT = os.path.join(SCR, 'out')
POOLS = os.path.join(SCR, 'pools')
XSTAR = os.path.join(SCR, 'xstar')
NPOOL = 3
NISL = 16384
DOSEID = {'0': 0, 'lo': 1, 'main': 2, 'hi': 3, 'ab-So': 4, 'ab-D': 5, 'ab-X': 6, 'ab-Sz': 7}

_CACHE = {}


def parse_cell(c):
    dose, P, A = c.split('|')
    return dose, float(P), int(A)


def cname(c):
    return c.replace('|', '_').replace(':', '-')


def job_name(j):
    return j.replace(':', '__').replace('|', '_')


def result_path(j):
    return os.path.join(OUT, job_name(j) + '.json')


def tabs():
    if 'tabs' not in _CACHE:
        _CACHE['tabs'] = M.Tabs()
    return _CACHE['tabs']


def get_pf(P):
    k = ('pf', float(P))
    if k not in _CACHE:
        _CACHE[k] = M.make_pf(tabs().payoff(float(P)))
    return _CACHE[k]


def pool_path(cell, pool):
    return os.path.join(POOLS, '%s__%d.npz' % (cname(cell), pool))


def load_pool(cell, pool):
    z = np.load(pool_path(cell, pool))
    return z['hist'].astype(np.float64)


def xstar_path(cell, pm, start, pool, raw=False):
    return os.path.join(XSTAR, job_name('O:%s:%s:%s:%d%s' % (cell, pm, start, pool, ':raw' if raw else '')) + '.npy')


def ode_result(cell, pm, start, pool, raw=False):
    import json
    p = result_path('O:%s:%s:%s:%d%s' % (cell, pm, start, pool, ':raw' if raw else ''))
    return json.load(open(p)) if os.path.exists(p) else None
