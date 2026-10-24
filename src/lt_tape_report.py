"""Report for the private-tape experiment: runs/lt-tape.md and runs/lt-tape.json from runs/lt_tape/*.json.gz.

Every statistic is labelled with its object: LOTTERY = the epsilon = 0 seed lottery at the stated (N, I), read at generation 2,000
(4,000 beside it), island means then run means with run-clustered 95% bootstrap intervals (4,000 resamples of runs); CHAIN = the
epsilon -> 0 diagnostic; STATIC = exact tables.
"""
import glob
import gzip
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lt_tape_run as RUN
import lt_tape_games as G
import lt_tape as T

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'runs', 'lt_tape')
_cache = {}


def load(name):
    if name in _cache: return _cache[name]
    p = os.path.join(OUT, name + '.json.gz')
    if not os.path.exists(p):
        _cache[name] = None; return None
    d = json.load(gzip.open(p, 'rt'))
    _cache[name] = d
    return d


def boot(vals, B=4000, seed=20261024):
    v = np.asarray(vals, float)
    v = v[~np.isnan(v)]
    if len(v) == 0: return (float('nan'),) * 3
    idx = np.random.default_rng(seed).integers(len(v), size=(B, len(v)))
    m = v[idx].mean(1)
    return float(v.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def fmt(t, d=3):
    if t is None: return 'n/a'
    if isinstance(t, tuple):
        if np.isnan(t[0]): return 'n/a'
        return '%.*f [%.*f, %.*f]' % (d, t[0], d, t[1], d, t[2])
    return '%.*f' % (d, t)


def rv(name, key, g='2000'):
    d = load(name)
    if d is None: return np.array([])
    return np.array([r['stats'][g].get(key, np.nan) for r in d['recs']], float)


def stat(name, key, g='2000'):
    v = rv(name, key, g)
    return boot(v) if len(v) else None


def paired(nameA, nameB, key, g='2000'):
    a = rv(nameA, key, g); b = rv(nameB, key, g)
    if len(a) == 0 or len(b) == 0 or len(a) != len(b): return None
    return boot(a - b)


def cn(game, arm, c, cell='primary', K=None, renorm=False, m=3, sampled=False):
    cv = RUN.C0 if c == 'c0' else (0.0 if c in ('0', 0) else float(c))
    return RUN.cell_name(game, arm, cv, cell, K or RUN.K0, renorm, m, sampled)


def resolved(name):
    d = load(name)
    return boot([r['resolved'] for r in d['recs']]) if d else None


def island_vals(name, key, g='isl2000'):
    """Pooled island-level values over runs (list per run of arrays)."""
    d = load(name)
    return [np.array(r[g][key], float) for r in d['recs']] if d else []


def md_table(header, rows):
    out = ['| ' + ' | '.join(header) + ' |', '|' + '|'.join(['---'] * len(header)) + '|']
    for r in rows: out.append('| ' + ' | '.join(str(x) for x in r) + ' |')
    return '\n'.join(out) + '\n'


def lottery_rows(game, arms, keys, labels, cs=('0', 'c0'), cell='primary', g='2000', renorm=False, **kw):
    rows = []
    for arm in arms:
        for c in cs:
            n = cn(game, arm, c, cell, renorm=renorm, **kw)
            if load(n) is None: continue
            row = ['%s%s' % (arm, ' (renorm)' if renorm else ''), 'free' if c == '0' else 'c0']
            for k in keys:
                row.append(fmt(stat(n, k, g)))
            row.append(fmt(resolved(n), 2))
            rows.append(row)
    return md_table(['arm', 'price'] + labels + ['resolved'], rows)
