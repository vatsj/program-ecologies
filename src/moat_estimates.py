"""Static local estimates for every planned cell of predictions/2026-10-02-drift-closure.md.

The chain restricted to all-D plus every monomorphic state within `depth` transitions of it (Chain.expand on
single states only; edges to states outside the set are lumped into all-D).  Reports P(C,C), and the cooperative
mass split into: the FairBot family (self-cooperating, cooperates with FairBot, cooperates with ALLC), the
prudent family (cooperates with FairBot, defects on ALLC), the rival family (self-cooperating, defects on
FairBot), and ALLC.

    python3 src/moat_estimates.py [--depth 3]
"""
import json, os, sys, argparse, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import fringe as F
from chain import Chain

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = (100, 1000, 10000, 30000, 100000)


def cells():
    J = []
    for n in (6, 8):
        for N in NS:
            J.append(('free', n, 0.0, 'D', N))
            for kind in ('D', 'CD'):
                for d in (1e-3, 1e-2):
                    J.append((kind, n, d, kind, N))
            J.append(('mu', n, 1e-2, 'mu', N))
            if n == 8:
                J.append(('boostPB', n, 0.0, 'D', N))
                J.append(('addP12b', n, 0.0, 'D', N))
                J.append(('addP12bsib', n, 0.0, 'D', N))
            if n == 6:
                J.append(('Dpath', n, 10.0 / N, 'D', N))     # delta_N = 10 / N: w delta N = 3
    return J


def family(P, names, q):
    iC, iFB = names.index('C'), names.index(F.FB)
    if q == iC: return 'ALLC'
    if P[q, q] != 1: return None
    if P[q, iFB] != 1: return 'rival'
    return 'FBfam' if P[q, iC] == 1 else 'prudent'


def local(job, depth=3):
    arm, n, delta, kind, N = job
    boost = (F.PB, F.FB) if arm == 'boostPB' else None
    extra = (F.P12B,) if arm == 'addP12b' else ((F.P12B,) + tuple(F.P12B_SIBS) if arm == 'addP12bsib' else ())
    L, prov = F.build_variant(n, delta, kind, boost, extra)
    P = prov.PCC; names = prov.names
    ch = Chain(prov, N=N, w=0.3, verbose=False, eager_poly=False)
    kD = ch.mono(names.index('D'))
    S = [kD]; seen = {kD}; frontier = [kD]
    for _ in range(depth):
        nxt = []
        for k in frontier:
            ch.expand(k)
            for b, v in ch.trans[k].items():
                if b not in seen and v > 1e-15 and ch.states[b][2] == 'mono':
                    seen.add(b); S.append(b); nxt.append(b)
        frontier = nxt
    for k in frontier: ch.expand(k)
    idx = {k: i for i, k in enumerate(S)}
    M = np.zeros((len(S), len(S)))
    for k in S:
        for b, v in ch.trans[k].items():
            M[idx[k], idx.get(b, 0)] += v
    # stationary distribution by GTH (stable for near-closed classes)
    A = M.copy(); m = len(S)
    for k in range(m - 1, 0, -1):
        s = A[k, :k].sum()
        A[:k, k] /= s if s > 0 else 1.0
        A[:k, :k] += np.outer(A[:k, k], A[k, :k])
    pi = np.zeros(m); pi[0] = 1.0
    for k in range(1, m):
        pi[k] = pi[:k] @ A[:k, k]
    pi /= pi.sum()
    out = dict(arm=arm, n=n, delta=delta, kind=kind, N=N, states=m)
    fam = dict(FBfam=0.0, prudent=0.0, rival=0.0, ALLC=0.0, other=0.0)
    pcc = 0.0
    tops = []
    for k, p in zip(S, pi):
        q = ch.states[k][0][0]
        f = family(P, names, q)
        if f is None:
            fam['other'] += p if q != names.index('D') else 0.0
        else:
            fam[f] += p; pcc += p
        tops.append((p, names[q]))
    coopv = np.array([family(P, names, ch.states[k][0][0]) is not None for k in S])
    cm = float(pi[coopv].sum())
    net_exit = float(pi[coopv] @ M[np.ix_(coopv, ~coopv)].sum(axis=1)) / cm if cm > 0 else float('nan')
    out.update(pcc=pcc, pi_D=float(pi[0]), net_exit=net_exit, **fam)
    out['top'] = [(nm, float(p)) for p, nm in sorted(tops, reverse=True)[:6]]
    return out


def only(arms):
    return [j for j in cells() if j[0] in arms]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--workers', type=int, default=3); ap.add_argument('--arms', default='')
    ap.add_argument('--out', default='drift_closure_estimates.json'); a = ap.parse_args()
    J = cells() if not a.arms else only(a.arms.split(',')); rows = []
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(local, J):
            rows.append(r)
            print('%-8s n=%d δ=%-8.3g N=%-6d P(C,C) %.4f D %.4f | FBfam %.4f prudent %.4f rival %.4f ALLC %.1e | %s' % (
                r['arm'], r['n'], r['delta'], r['N'], r['pcc'], r['pi_D'], r['FBfam'], r['prudent'], r['rival'], r['ALLC'],
                '; '.join('%s %.3f' % t for t in r['top'][1:4])), flush=True)
    rows.sort(key=lambda r: (r['arm'], r['n'], r['delta'] if r['arm'] != 'Dpath' else 0, r['N']))
    json.dump(rows, open(os.path.join(ROOT, 'runs', a.out), 'w'), indent=1)


if __name__ == '__main__':
    main()
