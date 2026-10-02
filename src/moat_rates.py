"""Static single-edge rates and a local estimate for predictions/2026-10-02-drift-closure.md.

For each variant (free arm, prior boost, D fringe, CD fringe) and N: entry rho(x | all-D) for key programs;
exits from key worlds per mutation event, split strict / neutral / other with top destinations; and a local
estimate of P(C,C): the chain restricted to all-D plus the self-cooperating monomorphic states within two
transitions of it, every other destination lumped into all-D.  Only Chain.expand on single states is used.

    python3 src/moat_rates.py
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import fringe as F
from chain import Chain

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS = [('FB', F.FB), ('FB1', F.FB1), ('PB', F.PB), ('P*', F.PSTAR), ('BTT', F.BTT), ('ALLC', 'C')]


def exits(ch, prov, key):
    U = prov.Ufull; names = prov.names
    a = ch.states[key][0][0]; uaa = U[a, a]
    ex = dict(strict=0.0, neutral=0.0, other=0.0); dest = {}
    for b, v in ch.trans.get(key, {}).items():
        if b == key: continue
        for q, mw in ch.trans_mut[(key, b)].items():
            if U[q, a] > uaa + 1e-12: t = 'strict'
            elif max(abs(U[q, a] - uaa), abs(U[a, q] - uaa), abs(U[q, q] - uaa)) < 1e-12: t = 'neutral'
            else: t = 'other'
            ex[t] += mw; dest[names[q]] = dest.get(names[q], 0.0) + mw
    ex['total'] = sum(ex.values())
    ex['top'] = sorted(dest.items(), key=lambda kv: -kv[1])[:3]
    return ex


def local_estimate(ch, prov, depth=2):
    P = prov.PCC; names = prov.names
    iD = names.index('D')
    kD = ch.mono(iD); ch.expand(kD)
    coop = lambda k: ch.states[k][2] == 'mono' and P[ch.states[k][0][0], ch.states[k][0][0]] == 1
    S = [kD]; frontier = [kD]
    for _ in range(depth):
        nxt = []
        for k in frontier:
            for b, v in ch.trans[k].items():
                if b not in S and coop(b) and v > 1e-14:
                    ch.expand(b); S.append(b); nxt.append(b)
        frontier = nxt
    idx = {k: i for i, k in enumerate(S)}
    M = np.zeros((len(S), len(S)))
    for k in S:
        for b, v in ch.trans[k].items():
            M[idx[k], idx.get(b, 0)] += v
    A = M.T - np.eye(len(S)); A[-1, :] = 1.0
    rhs = np.zeros(len(S)); rhs[-1] = 1.0
    pi = np.linalg.solve(A, rhs)
    return float(1 - pi[0]), len(S)


def rates(n, N, delta=0.0, kind='D', boost=None):
    L, prov = F.build_variant(n, delta, kind, boost)
    names = prov.names
    ch = Chain(prov, N=N, w=0.3, verbose=False, eager_poly=False)
    out = dict(n=n, N=N, delta=delta, kind=kind, boost=boost)
    iD = names.index('D'); kD = ch.mono(iD); ch.expand(kD)
    for lab, s in KEYS:
        if s not in names: continue
        q = names.index(s); k = ch.mono(q); ch.expand(k)
        out['enter_' + lab] = float(sum(r for (a, b, qq), (r, ks, tk) in ch.edge_rho.items() if a == kD and qq == q))
        e = exits(ch, prov, k)
        out['exit_' + lab] = e
    out['local'], out['local_states'] = local_estimate(ch, prov)
    return out


def main():
    rows = []
    variants = [(0.0, 'D', None), (0.0, 'D', (F.PB, F.FB)), (1e-3, 'D', None), (1e-2, 'D', None), (1e-3, 'CD', None), (1e-2, 'CD', None)]
    for n in (6, 8):
        for delta, kind, boost in variants:
            if boost is not None and n < 8: continue
            for N in (100, 1000, 10000, 30000, 100000):
                r = rates(n, N, delta, kind, boost); rows.append(r)
                tag = 'n=%d δ=%g %s%s N=%d' % (n, delta, kind, ' boost PB' if boost else '', N)
                s = '; '.join('%s in %.2e out %.2e (s %.1e n %.1e o %.1e) -> %s' % (
                    lab, r.get('enter_' + lab, 0), r['exit_' + lab]['total'], r['exit_' + lab]['strict'], r['exit_' + lab]['neutral'],
                    r['exit_' + lab]['other'], ','.join('%s:%.1e' % t for t in r['exit_' + lab]['top'][:2]))
                    for lab, _ in KEYS if 'exit_' + lab in r)
                print('%s | local P(C,C) %.4f (%d states) | %s' % (tag, r['local'], r['local_states'], s), flush=True)
    json.dump(rows, open(os.path.join(ROOT, 'runs', 'drift_closure_rates.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
