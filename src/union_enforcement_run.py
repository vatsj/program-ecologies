"""Runner for the enforcement experiment (specs/2026-10-05-enforcement.md).

    python3 src/union_enforcement_run.py partA
    python3 src/union_enforcement_run.py partB          # reduced chains, 3 workers
    python3 src/union_enforcement_run.py audit          # full-language tensors: stabilization, strikes at s > 0
    python3 src/union_enforcement_run.py partC --arm RC --pool 1 --c 0.5 --N 1000
Writes runs/enforcement/*.json.
"""
import argparse, json, os, sys, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import union as U
import union_enforcement as E

OUT = E.OUT


def run_part_a(args):
    os.makedirs(OUT, exist_ok=True)
    res = {}
    for lev in ((0, 1), (0,)):
        t = time.time()
        res['levels_%s' % ''.join(map(str, lev))] = E.part_a(levels=lev)
        print('part A levels', lev, '%.0fs' % (time.time() - t), flush=True)
    json.dump(res, open(os.path.join(OUT, 'part_a.json'), 'w'), indent=1, default=float)


_BASE = None


def _cell(key):
    global _BASE
    if _BASE is None:
        _BASE = E.make_base()
    arm, pool, c, tie, prior, N = key
    return key, E.reduced_cell(_BASE, arm, pool, c, tie, prior, N)


def run_part_b(args):
    from multiprocessing import Pool
    os.makedirs(OUT, exist_ok=True)
    E.make_base()                      # build the class cache once
    keys = [(arm, pool, c, tie, prior, N) for arm in E.ARMS for pool in (0, 1) for c in (0.1, 0.5) for tie in ('whack', 'nowhack')
            for prior in ('uniform', 'mu') for N in (100, 1000)]
    with Pool(args.workers) as p:
        res = dict(p.map(_cell, keys))
    out = {'%s|pool%d|c%g|%s|%s|N%d' % k: v for k, v in res.items()}
    base = E.make_base()
    static = {}
    for arm in E.ARMS:
        for pool in (0, 1):
            for c in (0.1, 0.5):
                static['%s|pool%d|c%g' % (arm, pool, c)] = E.reduced_static(base, arm, pool, c, 'whack')
    json.dump(dict(cells=out, static=static,
                   masses=dict(boss={base[2][i]: float(base[5][i]) for i in range(9)}, worker=dict(zip(E.NAMED_W, map(float, base[6]))))),
              open(os.path.join(OUT, 'part_b.json'), 'w'), indent=1, default=float)
    print('part B: %d cells' % len(out))


def run_audit(args):
    """Full-language tensors in every (arm, pool, c, tie): every encounter stabilizes;
    implemented strikes at s > 0 under rational workers (S1)."""
    d, C, nmw, nmb = E.load_base()
    P = d['P']; TAG = P.tag.astype(np.int64)
    out = {}
    for arm, (rb, rw) in E.ARMS.items():
        for pool in (0, 1):
            for c in (0.1, 0.5):
                for tie in ('whack', 'nowhack'):
                    if not pool and tie == 'nowhack':
                        continue
                    t = time.time()
                    J = E.tensor_e(*P.arrays(), U.TT, P.KB, P.KW, TAG, rb, rw, pool, c, E.TIES[tie])
                    b = J // 4; si = b // 3; a1 = (J // 2) % 2; a2 = J % 2
                    out['%s|pool%d|c%g|%s' % (arm, pool, c, tie)] = dict(
                        unstable=int((J < 0).sum()), encounters=int(J.size),
                        strikes_at_positive_wage=int((((a1 == 1) | (a2 == 1)) & (si > 0) & (J >= 0)).sum()),
                        strikes_total=int((((a1 == 1) | (a2 == 1)) & (J >= 0)).sum()),
                        source_targeting_implemented=int(((b % 3) == 2).sum()))
                    print(arm, pool, c, tie, out['%s|pool%d|c%g|%s' % (arm, pool, c, tie)], '%.0fs' % (time.time() - t), flush=True)
    json.dump(out, open(os.path.join(OUT, 'audit_full.json'), 'w'), indent=1)


def run_part_c(args):
    """Full chain in one (arm, pool) cell: classes re-lumped under the modified
    evaluator, class masses = sums of the frozen function masses."""
    from union_chain import UChain
    from union_run import analyse, seeds
    t = time.time()
    d, C0, nmw_f, nmb_f = E.load_base()
    P = d['P']; TAG = P.tag.astype(np.int64)
    rb, rw = E.ARMS[args.arm]
    tag = '%s_pool%d_c%g_N%d_%s' % (args.arm, args.pool, args.c, args.N, args.tie)
    J = E.tensor_e(*P.arrays(), U.TT, P.KB, P.KW, TAG, rb, rw, args.pool, args.c, E.TIES[args.tie])
    C = U.classes(d, J=J); C.pop('J')
    nmw = {k: (int(C['cw'][v]) if v is not None else None) for k, v in nmw_f.items()}
    nmb = {k: int(C['cb'][v]) for k, v in nmb_f.items()}
    print('classes: boss %d worker %d (%.0fs)' % (C['KcB'], C['KcW'], time.time() - t), flush=True)
    ch = UChain(C, args.c, args.N, w=0.3, theta=args.theta, arm='quorum', verbose=True)
    PAY, REP = E.payoff_table_e(args.c, args.pool)
    ch.PAY = PAY
    ch.explore_hybrid(seeds(ch, nmw, nmb))
    a = argparse.Namespace(arm=tag, c=args.c, N=args.N, w=0.3, theta=args.theta)
    out = analyse(ch, d, C, nmw, nmb, a)
    # enforcement statistics on the explored chain
    typ = ch.typ; pi = ch.pi
    j = typ // 4; t1 = (typ // 2) % 2; t2 = typ % 2
    b = j // 4; h = b % 3; a1 = (j // 2) % 2; a2 = j % 2
    striker = (a1 == 1) | (a2 == 1)
    wst = ((h == 0) & striker) | ((h == 2) & (((a1 == 1) & (t1 == 1)) | ((a2 == 1) & (t2 == 1))))
    out['strike_incidence'] = float(pi[striker].sum())
    out['repression_given_strike'] = float(pi[wst].sum() / pi[striker].sum()) if pi[striker].sum() > 0 else None
    sur = np.array([E.surplus(int(j[k]), int(t1[k]), int(t2[k]), PAY, REP) for k in range(len(j))])
    out['total_surplus'] = float(pi @ sur)
    out['class_counts'] = dict(boss=int(C['KcB']), worker=int(C['KcW']))
    out['tie'] = args.tie; out['pool'] = args.pool; out['enf_arm'] = args.arm
    out['time_s'] = time.time() - t
    json.dump(out, open(os.path.join(OUT, 'partC_%s.json' % tag), 'w'), indent=1, default=float)
    print(json.dumps({k: out[k] for k in ('states', 'rel_cut_change', 'summary', 'efficiency', 'total_surplus', 'mean_payoff',
                                          'strike_incidence', 'repression_given_strike', 'time_s')}, indent=1, default=float))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['partA', 'partB', 'audit', 'partC'])
    ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--arm', default='RC')
    ap.add_argument('--pool', type=int, default=1)
    ap.add_argument('--c', type=float, default=0.5)
    ap.add_argument('--N', type=float, default=1000)
    ap.add_argument('--tie', default='whack')
    ap.add_argument('--theta', type=float, default=1e-9)
    a = ap.parse_args()
    {'partA': run_part_a, 'partB': run_part_b, 'audit': run_audit, 'partC': run_part_c}[a.what](a)
