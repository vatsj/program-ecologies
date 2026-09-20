"""Unfakeable enterers: programs p in the weak-arm family L_n with
  (i)   u(p, D) >= u(D, D)                     can enter all-D
  (ii)  u(p, p) >  u(D, D)                     cooperates with itself
  (iii) no q in L_n invades all-p from rare:   for every q != p either
        u(q,p) < u(p,p), or u(q,p) = u(p,p) and u(q,q) <= u(p,q)   unfakeable
Candidates satisfying (i) and (ii) are tested for (iii) shortest first, with a
cheap prefilter against the probe set L_6.  Extra programs (given as source
strings) are tested against the same family.
"""
import argparse, os, sys, time, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from dsl import Language
from game import Game
from evaluate import evaluate, pair_keys, keys_of
from chain import fixation
from reference import Reference

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOL = 1e-7


def payoffs_vs(L, g, ids, p, tol=1e-11):
    """u(q,p), u(p,q), u(q,q) for all q in ids."""
    ids = np.asarray(ids)
    keys = np.union1d(pair_keys(L, ids, [p], g.role), keys_of(L.count, ids, ids, 0))
    res = evaluate(L, g, keys, tol=tol)
    P = np.full(len(ids), p)
    return res.payoff(ids, P), res.payoff(P, ids), res.payoff(ids, ids)


def invaders(L, g, ids, p, upp):
    uqp, upq, uqq = payoffs_vs(L, g, ids, p)
    first = uqp > upp + TOL
    second = (np.abs(uqp - upp) <= TOL) & (uqq > upq + TOL)
    inv = (first | second) & (ids != p)
    return ids[inv], uqp[inv], upq[inv], uqq[inv], first[inv]


def main(n, extras, out_path, N_list=(10, 100), ws=(0.01, 0.1, 1.0), max_full=400):
    g = Game.load(os.path.join(ROOT, 'games', 'pd.yaml'))
    t0 = time.time()
    L = Language('weak', n)
    ids = L.ids()
    extra_ids = [L.parse(s) for s in extras]
    D = L.parse('D')
    print('L_%d: %d programs (%.0fs)' % (n, len(ids), time.time() - t0), flush=True)
    # (i), (ii) for the family and the extras
    allp = np.concatenate([ids, np.array(extra_ids, np.int64)])
    keys = np.union1d(pair_keys(L, allp, [D], g.role), keys_of(L.count, allp, allp, 0))
    res = evaluate(L, g, keys, tol=1e-11)
    upD = res.payoff(allp, np.full(len(allp), D)); upp = res.payoff(allp, allp); uDD = float(res.payoff(D, D))
    uDp = res.payoff(np.full(len(allp), D), allp)
    c1 = upD >= uDD - TOL; c2 = upp > uDD + TOL
    print('(i) %d, (ii) %d, both %d of %d (%.0fs)' % (c1[:len(ids)].sum(), c2[:len(ids)].sum(), (c1 & c2)[:len(ids)].sum(), len(ids), time.time() - t0), flush=True)
    cand = ids[(c1 & c2)[:len(ids)]]
    # behavioural dedup of candidates by (u(p,D), u(p,p), u(D,p)) is not sound; order by bits only
    cand = cand[np.argsort(L.bits[cand], kind='stable')]
    probe = L.ids(min(6, n))
    results = []
    winner = None
    tested_full = 0
    for p in cand:
        p = int(p); u_pp = float(upp[np.searchsorted(allp, p)])
        inv_p, *_ = invaders(L, g, probe, p, u_pp)
        if len(inv_p):
            continue
        tested_full += 1
        inv, uqp, upq, uqq, first = invaders(L, g, ids, p, u_pp)
        if len(inv) == 0:
            winner = p
            break
        if tested_full >= max_full:
            print('stopped after %d full tests' % tested_full, flush=True)
            break
    report = {'n': n, 'n_programs': int(len(ids)), 'n_cand': int(len(cand)), 'full_tests': tested_full,
              'winner': None, 'extras': []}
    lines = ['# Unfakeable enterers, weak arm L_%d (%d programs)' % (n, len(ids)), '',
             'Conditions: (i) u(p,D) >= u(D,D) = %.3g; (ii) u(p,p) > u(D,D); (iii) no q in L_%d invades all-p from rare.' % (uDD, n),
             'Candidates satisfying (i) and (ii): %d; full (iii) tests after the L_6 prefilter: %d.' % (len(cand), tested_full), '']

    counts = L.growth_rate(upto=max(n, max([int(L.size[e]) for e in extra_ids] + [n])))[1]

    def bits_of(p):
        if p < L.n_enum:
            return float(L.bits[p])
        sz = int(L.size[p])
        return float(np.log2(counts[sz]) + 2 * np.log2(sz) + 1)   # same code, count from the recursion

    def describe(p, label):
        k = np.searchsorted(allp, p)
        rows = ['## %s: `%s` (%d nodes, %.2f bits)' % (label, L.src(p), L.size[p], bits_of(p)),
                '', 'u(p,D) = %.4g (u(D,D) = %.4g), u(p,p) = %.4g, u(D,p) = %.4g' % (upD[k], uDD, upp[k], uDp[k])]
        inv, uqp, upq, uqq, first = invaders(L, g, ids, p, float(upp[k]))
        ok3 = len(inv) == 0
        rows.append('(i) %s, (ii) %s, (iii) %s' % (c1[k], c2[k], ok3))
        if not ok3:
            order = np.argsort(L.bits[inv])[:6]
            rows.append('invaders (shortest): ' + '; '.join('`%s` u(q,p)=%.3g u(q,q)=%.3g u(p,q)=%.3g%s' % (
                L.src(q), uqp[i], uqq[i], upq[i], '' if first[i] else ' (2nd order)') for i, q in zip(order, inv[order])))
        rows.append('')
        rows.append('| N | w | rho(p | all-D) |'); rows.append('|---|---|---|')
        rhos = {}
        for N in N_list:
            for w in ws:
                r = fixation(float(upp[k]), float(upD[k]), float(uDp[k]), uDD, N, w, N)
                rhos['%d,%g' % (N, w)] = r
                rows.append('| %d | %g | %.3e |' % (N, w, r))
        rows.append('')
        return rows, dict(src=L.src(p), nodes=int(L.size[p]), bits=bits_of(p), uPD=float(upD[k]), uPP=float(upp[k]), uDP=float(uDp[k]),
                          i=bool(c1[k]), ii=bool(c2[k]), iii=ok3, invaders=[L.src(q) for q in inv[np.argsort(L.bits[inv])[:6]]], rho=rhos)

    if winner is not None:
        rows, d = describe(winner, 'Winner (shortest program satisfying all three)')
        lines += rows; report['winner'] = d
        # spot-check (iii) with the reference evaluator against three named programs
        R = Reference(L)
        lines.append('Reference-evaluator spot check of (iii) (budget 200):'); lines.append('')
        lines.append('| q | P(q plays C vs p) | P(p plays C vs q) | u(q,p) | u(p,p) | u(q,q) | u(p,q) |'); lines.append('|---|---|---|---|---|---|---|')
        for s in ['THEM(^D)', 'THEM(^C)', 'or(X,THEM(ME))']:
            q = L.parse(s)
            vq = R.value(q, winner, 0, 200); vp = R.value(winner, q, 0, 200); vqq = R.value(q, q, 0, 200); vpp = R.value(winner, winner, 0, 200)
            V = lambda v: float((lambda p: (p[0].copy(), p[1]))(v)[0][1] + v[1] * (g.minimax[0] == 1))   # P(C) with floor mass on the minimax level
            uqp = g.payoff(V(vq), V(vp)); upq = g.payoff(V(vp), V(vq)); uqq = g.payoff(V(vqq), V(vqq)); u_pp = g.payoff(V(vpp), V(vpp))
            lines.append('| `%s` | %.4g | %.4g | %.4g | %.4g | %.4g | %.4g |' % (s, V(vq), V(vp), uqp, u_pp, uqq, upq))
        lines.append('')
    else:
        lines.append('## No program in L_%d satisfies all three.' % n); lines.append('')
        # shortest satisfying any two
        two = {}
        two['(i)+(ii)'] = int(cand[0]) if len(cand) else None
        # (i)+(iii) and (ii)+(iii): scan shortest programs satisfying the pair, test (iii) with the prefilter then fully
        for label, mask in [('(i)+(iii)', c1[:len(ids)] & ~c2[:len(ids)]), ('(ii)+(iii)', c2[:len(ids)] & ~c1[:len(ids)])]:
            pool = ids[mask]; pool = pool[np.argsort(L.bits[pool], kind='stable')]
            found = None; tests = 0
            for p in pool:
                p = int(p); u_pp = float(upp[np.searchsorted(allp, p)])
                if len(invaders(L, g, probe, p, u_pp)[0]): continue
                tests += 1
                if len(invaders(L, g, ids, p, u_pp)[0]) == 0:
                    found = p; break
                if tests >= 50: break
            two[label] = found
        for label, p in two.items():
            if p is None:
                lines.append('- %s: none found' % label); continue
            rows, d = describe(p, 'Shortest satisfying %s' % label)
            lines += rows; report.setdefault('two', {})[label] = d
    for s, p in zip(extras, extra_ids):
        rows, d = describe(p, 'Extra program')
        lines += rows; report['extras'].append(d)
    lines.append('Wall time %.0fs.' % (time.time() - t0))
    with open(out_path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    with open(out_path.replace('.md', '.json'), 'w') as f:
        json.dump(report, f, indent=1)
    print('\n'.join(lines), flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=9)
    ap.add_argument('--extra', nargs='*', default=['or(and(and(X,X),THEM(^C)),THEM(ME))'])
    a = ap.parse_args()
    main(a.n, a.extra, os.path.join(ROOT, 'runs', 'enterers_n%d.md' % a.n))
