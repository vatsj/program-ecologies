"""Report for the encounter-contracts experiment: reads runs/encounter_contracts/*.json and writes runs/encounter-contracts.md and .json.

    python3 src/encounter_contracts_report.py
"""
import glob, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import encounter_contracts as EC

ROOT = EC.ROOT
D = os.path.join(ROOT, 'runs', 'encounter_contracts')
NOUT = EC.NOUT

ST_ATT_S, ST_ACC_S, ST_BLK_S = EC.ST_ATT_S, EC.ST_ACC_S, EC.ST_BLK_S
CATS = ['F', 'U', 'G', 'W', 'D', 'M', 'none']


def load_cells():
    cells = {}
    for f in sorted(glob.glob(os.path.join(D, 'pool_*.json'))):
        r = json.load(open(f))
        r['_file'] = os.path.basename(f)
        cells[os.path.basename(f)[:-5]] = r
    return cells


def load_kind(prefix):
    out = {}
    for f in sorted(glob.glob(os.path.join(D, prefix + '_*.json'))):
        out[os.path.basename(f)[:-5]] = json.load(open(f))
    return out


def wilson(k, n, z=1.96):
    if n == 0:
        return (float('nan'), float('nan'))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def cp(res, r):
    for c in res['checkpoints']:
        if c['round'] == r:
            return c
    return None


def shares(c, kind='settled'):
    h = c[kind]
    n = c['n_settled'] if kind == 'settled' else c['I']
    n = max(n, 1)
    return {k: v / n for k, v in h.items()}


def fmt(x, d=3):
    if x is None or (isinstance(x, float) and (math.isnan(x))):
        return 'n/a'
    return ('%.' + str(d) + 'f') % x


def cell_name(r):
    return '%s nu=%g I=%d %s%s%s' % (r['arm'], r['nu'], r['I'], r['start'], '' if r['mN'] == 1e-3 else ' mN=%g' % r['mN'],
                                     '' if r['N'] == 100 else ' N=%d' % r['N'])
