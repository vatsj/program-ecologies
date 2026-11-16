"""Queue 80: build and cache the S1 check table and the execution tables.

    python3 src/script_offers_tables.py s1                       # runs/script_offers/s1_table.json (catalogue + forgers, S0 run per entry)
    python3 src/script_offers_tables.py build S S1 [forg]        # world S, machine S1, at (KR', cap')   -> runs/_cache/sco_*.npz
    python3 src/script_offers_tables.py build S S0 [forg]        # the same in S0 (V3)
    python3 src/script_offers_tables.py build K C1               # world K (queue 79's CHK, C1) at (KR', cap')
"""
import os, sys, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import lt_code as L
import script_offers as S
import script_offers_cat as SC

CACHE = os.path.join(ROOT, 'runs', '_cache')
S1PATH = os.path.join(ROOT, 'runs', 'script_offers', 's1_table.json')


def make_s1():
    cat = SC.Cat('S', forg=True)
    rows = []
    for i in range(cat.K):
        for c in range(1, 6):
            v, cost = S.core_s0(cat.terms[i], c)
            rows.append([cat.names[i], c, v if v in ('T', 'F') else 'BOT', int(cost)])
    os.makedirs(os.path.dirname(S1PATH), exist_ok=True)
    json.dump(dict(KCHK=S.KCHK, CAPP=S.CAPP, KRP=S.KRP, rows=rows), open(S1PATH, 'w'))
    return rows


def load_s1(cat=None):
    """{(canon, code): (value, cost)} for the S1 machine (requires names to match the current catalogue + forgers)."""
    d = json.load(open(S1PATH))
    assert (d['KCHK'], d['CAPP'], d['KRP']) == (S.KCHK, S.CAPP, S.KRP)
    cat = cat or SC.Cat('S', forg=True)
    out = {}
    for nm, c, v, cost in d['rows']:
        out[(L.canon_term(cat.terms[cat.idx[nm]]), c)] = (v, cost)
    return out


def chk_matrix(cat):
    """CHK[i, c] = 1 if chk(program i, code c) = T (codes 1..5 -> columns 0..4), from the S1 table file."""
    d = json.load(open(S1PATH))
    M = np.zeros((cat.K, 5), np.int8)
    cost = np.zeros((cat.K, 5), np.int64)
    for nm, c, v, cs in d['rows']:
        if nm in cat.idx:
            M[cat.idx[nm], c - 1] = 1 if v == 'T' else 0
            cost[cat.idx[nm], c - 1] = cs
    return M, cost


def table_path(world, machine, forg, fuel=None, cap=None):
    cat = SC.Cat(world, cap, forg)
    fuel = fuel or 3 * (cap or S.CAPP)
    return os.path.join(CACHE, 'sco_%s_%s_%s.npz' % (world, machine, cat.key(machine, fuel, 'f%d' % forg))), cat


def get_tables(world, machine, forg=False, workers=None, cap=None, fuel=None, log=print):
    path, cat = table_path(world, machine, forg, fuel, cap)
    if os.path.exists(path):
        z = np.load(path)
        return cat, z['code'], z['steps'], z['nto'], z['fo']
    workers = workers or int(os.environ.get('DAYTONA_CPUS', 3))
    s1 = load_s1() if world == 'S' else {}
    t0 = time.time()
    cat, code, steps, nto, fo = SC.build_tables(world, machine=machine, cap=cap, fuel=fuel, forg=forg, workers=workers, s1tab=s1,
                                                regress=True, log=log)
    log('built %s %s forg=%s in %.0fs' % (world, machine, forg, time.time() - t0))
    os.makedirs(CACHE, exist_ok=True)
    tmp = path + '.%d.tmp.npz' % os.getpid()
    np.savez_compressed(tmp, code=code, steps=steps, nto=nto, fo=fo)
    os.replace(tmp, path)
    return cat, code, steps, nto, fo


if __name__ == '__main__':
    if sys.argv[1] == 's1':
        r = make_s1()
        print(len(r), 'worst', max(x[3] for x in r))
    elif sys.argv[1] == 'build':
        world, machine = sys.argv[2], sys.argv[3]
        forg = len(sys.argv) > 4 and sys.argv[4] == 'forg'
        get_tables(world, machine, forg)
