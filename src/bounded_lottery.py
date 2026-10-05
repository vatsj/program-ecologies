"""eps = 0 seeding lottery for the semantic legibility gate (specs/2026-10-04-bounded-provers.md, items 3 and 6).

Islands as in src/almost_all_seeds.py (complete graph, w = 0.3, horizon 1e5 generations, the same stopping rules),
n = 6.  Seeding iid from the length prior at the level of canonical functions, then mapped to each arm's behavioural
classes, so a given (cell, rep) starts from the same programs at every b (paired seeds).  The island kernel is
almost_all_seeds._run, patched at load time to also return the global class counts at ALLC's global extinction.

    python3 src/bounded_lottery.py [--workers 3]
Writes runs/bounded-provers-lottery.json.
"""
import os, sys, json, time, inspect, argparse
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import almost_all_seeds as AS
from abm import njit
from bounded import build_arm, lang, BUDGETS, INF, ROOT

OUT = os.path.join(ROOT, 'runs', 'bounded-provers-lottery.json')
CELLS = [(100, 4, 1.0), (400, 4, 1.0), (1600, 4, 1.0), (100, 64, 1.0), (100, 256, 1.0), (100, 64, 0.0), (400, 4, 0.0)]
GENS = 100000
MARGIN = 0.15


def _patched_run():
    src = inspect.getsource(AS._run.py_func)
    src = src.replace('@njit(cache=True)\n', '')
    for old, new in (('    ext_C = -1\n', '    ext_C = -1\n    core_glob = np.zeros(K, np.int64)\n'),
                     ('                ext_C = g + 1\n', '                ext_C = g + 1\n                for kk in range(K):\n                    core_glob[kk] = glob[kk]\n'),
                     ('loss_log[:nloss]\n', 'loss_log[:nloss], core_glob\n')):
        assert src.count(old) == 1, old
        src = src.replace(old, new)
    ns = dict(AS.__dict__)
    exec(compile(src, 'patched_run', 'exec'), ns)
    return njit(cache=False)(ns['_run'])


_RUN = None
_DATA = {}


def arm_data(kind, b):
    key = (kind, b)
    if key in _DATA:
        return _DATA[key]
    a = build_arm(6, kind, b); prov = a['prov']
    names = list(prov.names)
    U = np.ascontiguousarray(prov.Ufull, dtype=float); PCC = np.ascontiguousarray(prov.PCC, dtype=float)
    K = len(names)
    L = lang(6)
    cls = np.zeros(len(L.funcs), np.int64)
    for k, mem in enumerate(prov.members):
        for c in mem: cls[c] = k
    iC, iD = names.index('C'), names.index('D')
    coop = [k for k in range(K) if PCC[k, k] >= 0.95 and k != iC]
    unf = [k for k in coop if U[:, k].max() <= U[k, k] + 1e-9]
    d = dict(names=names, U=U, PCC=PCC, cls=cls, iC=iC, iD=iD, coop=coop, coop_unfakeable=unf,
             fakers_of_FB=[q for q in range(K) if U[q, names.index('BOX(THEM(ME))')] > U[names.index('BOX(THEM(ME))'), names.index('BOX(THEM(ME))')] + 1e-9])
    _DATA[key] = d
    return d


def job(j):
    global _RUN
    if _RUN is None:
        _RUN = _patched_run()
    kind, b, N, I, mN, rep = j
    d = arm_data(kind, b); L = lang(6)
    mu = L.mu_canon / L.mu_canon.sum()
    rng = np.random.default_rng([N, I, int(mN * 10), rep, 2026104])
    K = len(d['names'])
    init = np.zeros((I, K), np.int64)
    for i in range(I):
        cnt = rng.multinomial(N, mu)
        np.add.at(init[i], d['cls'], cnt)
    coopmask = np.zeros(K, np.bool_); coopmask[d['coop']] = True
    t = time.time()
    res = _RUN(d['U'], d['PCC'], init, N, AS.W, mN / N, GENS, 20, 100003 * rep + 7 * N + I + int(mN * 1000) + 99991, d['iC'], coopmask)
    st, sg, counts, isl_cc, isl_pay, first_noC, ext_C, lb, la, tr_cc, tr_np, loss_log, core_glob = res
    glob = counts.sum(0)
    cc = float(isl_cc.mean()); pay = float(isl_pay.mean())
    names = d['names']
    r = dict(kind=kind, b=b, N=N, I=I, mN=mN, rep=rep, status=AS.STATUS[st], stop_gen=int(sg), pcc=cc, pay=pay,
             outcome=AS.outcome(cc, pay) if st in (1, 2, 3) else ('unresolved' if st == 4 else None),
             final={names[k]: int(v) for k, v in enumerate(glob) if v > 0},
             isl_out=[AS.outcome(c, p) for c, p in zip(isl_cc, isl_pay)] if mN == 0 else None,
             ext_C=int(ext_C), lost_before=int(lb), lost_after=int(la),
             seed_core=int(init[:, d['coop']].sum()), seed_core_unf=int(init[:, d['coop_unfakeable']].sum()),
             core_at_extC=int(core_glob[d['coop']].sum()) if ext_C >= 0 else None,
             core_unf_at_extC=int(core_glob[d['coop_unfakeable']].sum()) if ext_C >= 0 else None,
             loss_log=[(int(a), int(bb), names[c], int(e)) for a, bb, c, e in loss_log][:40],
             time_s=time.time() - t)
    return r


def arms():
    return [('global', b) for b in BUDGETS] + [('random', b) for b in (1, 2, 3, 4)]


def key(r):
    return (r['kind'], str(r['b']), r['N'], r['I'], r['mN'], r['rep'])


def paired(rows, kind, b, cell):
    """Paired difference in efficient indicator, (kind, b) minus (global, inf), over reps present in both."""
    N, I, mN = cell
    A = {r['rep']: r for r in rows if r['kind'] == kind and str(r['b']) == str(b) and (r['N'], r['I'], r['mN']) == cell}
    B = {r['rep']: r for r in rows if r['kind'] == 'global' and str(r['b']) == str(INF) and (r['N'], r['I'], r['mN']) == cell}
    reps = sorted(set(A) & set(B))
    reps = [k for k in reps if A[k]['outcome'] not in ('unresolved', None) and B[k]['outcome'] not in ('unresolved', None)]
    if not reps:
        return None
    dlt = np.array([(A[k]['outcome'] == 'efficient') - (B[k]['outcome'] == 'efficient') for k in reps], float)
    rng = np.random.default_rng(7)
    bs = rng.choice(dlt, (10000, len(dlt))).mean(1)
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return dict(n=len(reps), diff=float(dlt.mean()), lo=float(lo), hi=float(hi),
                equivalent=bool(lo >= -MARGIN and hi <= MARGIN), inside_margin=bool(abs(dlt.mean()) <= MARGIN))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--workers', type=int, default=3)
    a = ap.parse_args()
    rows = json.load(open(OUT)) if os.path.exists(OUT) else []
    done = {key(r) for r in rows}

    def run(J):
        J = [j for j in J if (j[0], str(j[1]), j[2], j[3], j[4], j[5]) not in done]
        J.sort(key=lambda j: -j[2] * j[3])
        print('%d jobs' % len(J), flush=True)
        with Pool(a.workers) as pool:
            for r in pool.imap_unordered(job, J, chunksize=4):
                rows.append(r); done.add(key(r))
                if len(rows) % 50 == 0:
                    json.dump(rows, open(OUT, 'w'), default=str)
                    print('%d rows' % len(rows), flush=True)
        json.dump(rows, open(OUT, 'w'), default=str)
    # round 1: 20 reps everywhere
    run([(k, b, N, I, mN, rep) for k, b in arms() for N, I, mN in CELLS for rep in range(20)])
    # round 2: adaptive replication to 40 where the paired difference is inside the margin but its interval is not
    ext = []
    for k, b in arms():
        if (k, b) == ('global', INF): continue
        for cell in CELLS:
            if cell[2] == 0.0: continue
            p = paired(rows, k, b, cell)
            if p and p['inside_margin'] and not p['equivalent']:
                ext.append((k, b, cell))
    print('adaptive cells:', ext, flush=True)
    J = []
    for k, b, (N, I, mN) in ext:
        for rep in range(20, 40):
            J.append((k, b, N, I, mN, rep)); J.append(('global', INF, N, I, mN, rep))
    J = list(dict.fromkeys(J))
    run(J)


if __name__ == '__main__':
    main()
