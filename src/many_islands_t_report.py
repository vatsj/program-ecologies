"""Aggregate the per-job records of the arm-T islands experiment into runs/many-islands-t.md, runs/many-islands-t.json and
runs/many_islands_t/*.json (small files), and score the registered predictions (predictions/2026-10-29-many-islands-t.md).

    python3 src/many_islands_t_report.py [--out runs]
"""
import os, sys, json, glob, math
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import many_islands_t as M
from many_islands_t_common import OUT, NPOOL, parse_cell, cname

ROOT = M.ROOT
CLS = M.CLS
TCRIT2 = 4.303          # t quantile, 2 degrees of freedom (3 pools)


def load_all():
    recs = {}
    for f in glob.glob(os.path.join(OUT, '*.json')):
        try:
            r = json.load(open(f))
        except Exception:
            continue
        if 'job' in r:
            recs[r['job']] = r
    return recs


def mean_ci(v):
    v = np.asarray(v, float)
    if len(v) == 0:
        return None, None
    m = float(v.mean())
    if len(v) < 2:
        return m, None
    return m, float(TCRIT2 * v.std(ddof=1) / math.sqrt(len(v))) if len(v) == 3 else float(2.0 * v.std(ddof=1) / math.sqrt(len(v)))


def fmt(m, h, nd=4):
    if m is None:
        return 'n/a'
    if h is None:
        return ('%.' + str(nd) + 'f') % m
    return ('%.' + str(nd) + 'f ± %.' + str(nd) + 'f') % (m, h)


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def rec_at(recs, t):
    best = None
    for r in recs:
        if abs(r['t'] - t) <= 1e-9 * max(1.0, t):
            return r
    return best


def traj_stats(job_recs, key='shares'):
    """per time in the common checkpoint set: list over pools of the vector."""
    out = {}
    for T in (0.0, 10.0, 100.0, 1e3, 1e4, 1e5):
        out[T] = [rec_at(j['recs'], T)[key] for j in job_recs if rec_at(j['recs'], T) is not None]
    return out


class R:
    def __init__(self):
        self.recs = load_all()
        self.md = []
        self.js = {}

    def get(self, job):
        return self.recs.get(job)

    def ode(self, cell, pm, start, pool, raw=False):
        return self.get('O:%s:%s:%s:%d%s' % (cell, float(pm), start, pool, ':raw' if raw else ''))

    def ode_pools(self, cell, pm, start, raw=False):
        out = []
        for p in range(NPOOL):
            r = self.ode(cell, pm, start, p, raw)
            if r is not None and r.get('available', True):
                out.append(r)
        return out

    def add(self, s=''):
        self.md.append(s)


def vstar_end(rs):
    return [r['final_shares'][0] for r in rs]


def table(rows, header):
    lines = ['| ' + ' | '.join(header) + ' |', '|' + '|'.join(['---'] * len(header)) + '|']
    for r in rows:
        lines.append('| ' + ' | '.join(str(c) for c in r) + ' |')
    return '\n'.join(lines)
