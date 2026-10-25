"""Report for the many-islands experiment: reads the per-job json files in runs/many_islands/ and writes
runs/many-islands.md and runs/many-islands.json.  Importable without side effects.

    python3 src/many_islands_report.py
"""
import os, sys, json, math, glob
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import many_islands as MI
import many_islands_run as MR
from many_islands_analysis import tint

OUT = MR.OUT
ARMS = ('L', 'M', 'R')
AS = (0, 50, 150)
ARMNAME = {'L': 'L (weak)', 'M': 'modalPA', 'R': 'readers', 'Rw': 'readers (weak)'}
CP_ALL = list(MR.CHECKPOINTS) + list(MR.EXT)


def jload(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def cells():
    out = []
    for arm in ('L', 'M', 'R', 'Rw'):
        for A in AS:
            if glob.glob(os.path.join(OUT, 'chain_%s_A%d_p*.json' % (arm, A))):
                out.append((arm, A))
    return out


def chains(arm, A):
    fs = sorted(glob.glob(os.path.join(OUT, 'chain_%s_A%d_p*.json' % (arm, A))))
    return [jload(f) for f in fs]


def km_median(times, events):
    """Kaplan-Meier median of right-censored times (events 1 = observed); nan if the curve stays above 0.5."""
    t = np.asarray(times, float); e = np.asarray(events, int)
    order = np.argsort(t)
    t = t[order]; e = e[order]
    n = len(t); S = 1.0
    for i in range(n):
        if e[i]:
            S *= 1.0 - 1.0 / (n - i)
            if S <= 0.5:
                return float(t[i])
    return float('nan')


def pool_curve(chs, key):
    """per-pool arrays of a summary key over the checkpoints: (npools, ncp)."""
    return np.array([[s[key] for s in c['summary']] for c in chs])


def fmt(v, d=3):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return 'nan'
    return ('%.' + str(d) + 'f') % v


def interval(v, d=3):
    m, lo, hi = tint(v)
    if math.isnan(lo):
        return fmt(m, d)
    return '%s [%s, %s]' % (fmt(m, d), fmt(lo, d), fmt(hi, d))
