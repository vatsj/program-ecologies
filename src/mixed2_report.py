"""Report for the two-role mixed-action experiment: reads runs/mixed2/ and writes runs/mixed2.md and runs/mixed2.json with the
verdict of every prediction of predictions/2026-10-23-two-role-mixed.md under the scoring conventions fixed there.

    python3 src/mixed2_report.py
"""
import gzip, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs', 'mixed2')
BOOT = 4000
rng = np.random.default_rng(20261023)


def jload(path):
    if path.endswith('.gz'):
        with gzip.open(path, 'rt') as f: return json.load(f)
    with open(path) as f: return json.load(f)


def exists(*parts):
    return os.path.exists(os.path.join(RUNS, *parts))


# ------------------------------------------------------------------ lottery access
_lot = {}


def lot(game, arm, c, cell='primary'):
    """lottery cell (price irrelevant for the blind arm: its c = 0 file serves both prices); None if missing."""
    if arm == 'blind':
        c = 0.0
    key = (game, arm, c, cell)
    if key not in _lot:
        p = 'lot_%s_%s_c%g_%s.json.gz' % (game, arm, c, cell)
        _lot[key] = jload(os.path.join(RUNS, p)) if exists(p) else None
    return _lot[key]


def vals(L, key, g=2000):
    out = []
    for r in L['runs']:
        v = r['stats'].get(str(g), {}).get(key)
        out.append(np.nan if v is None else float(v))
    return np.array(out)


def win(L, key, lo=1500, hi=2000):
    out = []
    for r in L['runs']:
        gs = [g for g in r['cps'] if lo <= g <= hi]
        v = [r['stats'][str(g)].get(key) for g in gs]
        v = [x for x in v if x is not None]
        out.append(float(np.mean(v)) if v else np.nan)
    return np.array(out)


def boot(x, B=BOOT):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return (np.nan, np.nan, np.nan)
    idx = rng.integers(0, len(x), size=(B, len(x)))
    m = x[idx].mean(1)
    return (float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5)))


def pdiff(a, b):
    n = min(len(a), len(b))
    return boot(np.asarray(a[:n], float) - np.asarray(b[:n], float))


def fmt(t, d=3):
    if t is None or (isinstance(t, float) and not np.isfinite(t)):
        return 'n/a'
    if isinstance(t, tuple):
        return '%.*f [%.*f, %.*f]' % (d, t[0], d, t[1], d, t[2])
    return '%.*f' % (d, t)


def cell_ok(*Ls):
    return all(L is not None and len(L['runs']) >= 1 for L in Ls)


# ------------------------------------------------------------------ chain access
def chain(game, arm, c):
    if arm == 'blind':
        c = 0.0
    p = 'chain_%s_%s_c%g.json' % (game, arm, c)
    return jload(os.path.join(RUNS, p)) if exists(p) else None
