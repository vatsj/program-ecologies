"""Static numbers for predictions/2026-10-02-dollar-partitions.md, computed
before any chain or island run.

  python3 src/dollar_static.py > runs/dollar_static.md

(1) Replicator basins over constant demands (Skyrms's comparison), uniform
    starting points on the simplex.
(2) Efficient conventions in the language: classes whose self-play is
    efficient, their partition, prior mass and class size.
(3) Pairwise contests between conventions: mismatch payoffs, the crossing
    frequency (risk dominance) and Moran fixation of one mutant at N = 100,
    1,000 and 10,000, w = 0.3.
"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import dollar as D
from chain import replicator, fixation

W = 0.3


def basins(U, n=4000, seed=1):
    """Fraction of uniform simplex starts reaching each rest point (by rounded support)."""
    rng = np.random.default_rng(seed)
    K = U.shape[0]
    out = {}
    for _ in range(n):
        x0 = rng.dirichlet(np.ones(K))
        x, st, _, _ = replicator(U, x0, rest_tol=1e-9, ext_tol=1e-7)
        key = tuple(np.round(x, 2)) if st == 'rest' else ('cycle',)
        out[key] = out.get(key, 0) + 1
    return {k: v / n for k, v in sorted(out.items(), key=lambda kv: -kv[1])}


def crossing(U, a, b):
    """Frequency of b at which b and a earn the same in an {a, b} population (None if no interior crossing)."""
    # f_b(x) = x U[b,b] + (1-x) U[b,a]; f_a(x) = x U[a,b] + (1-x) U[a,a]
    den = (U[b, b] - U[b, a]) - (U[a, b] - U[a, a])
    if abs(den) < 1e-12:
        return None
    x = (U[a, a] - U[b, a]) / den
    return float(x) if 0 < x < 1 else None


def rho(U, q, a, N, w=W):
    return float(fixation(U[q, q], U[q, a], U[a, q], U[a, a], N, w, N))


def main():
    lines = ['# Static numbers: divide the dollar (predictions/2026-10-02-dollar-partitions.md)', '']
    res = {}
    # (1) constants only
    for name in ('dollar3', 'dollar5'):
        g = D.load_game(name, role=False)
        v = g.values
        Uc = g.pay[0]
        b = basins(Uc)
        lines += ['## Replicator basins over the constant demands %s (no ROLE), 4,000 uniform starts' % list(np.round(v, 3)), '']
        for k, f in list(b.items())[:8]:
            lines.append('- %s: %.3f' % (dict(zip(g.actions, k)) if k[0] != 'cycle' else 'cycle', f))
        res['basins_' + name] = {str(k): f for k, f in b.items()}
        lines.append('')
    # (2)-(3) language-level numbers for every evaluated cell
    for name, n, role in CELLS:
        path = os.path.join(D.ROOT, 'runs', 'dollar_eval_%s_n%d%s.npz' % (name, n, '' if role else '_norole'))
        if not os.path.exists(path):
            lines += ['## %s n=%d ROLE=%s: not evaluated yet' % (name, n, role), '']
            continue
        lines += cell_numbers(name, n, role, res)
    print('\n'.join(lines))
    json.dump(res, open(os.path.join(D.ROOT, 'runs', 'dollar_static.json'), 'w'), indent=1, default=str)


CELLS = [('dollar3', 5, False), ('dollar3', 5, True), ('dollar3', 6, False), ('dollar5', 5, False), ('dollar5', 5, True)]


def cell_numbers(name, n, role, res):
    E = D.load_or_evaluate(name, n, role=role, verbose=False)
    g, U, JA, names, mu, sizes = E['game'], E['U'], E['JA'], E['names'], E['mu'], E['sizes']
    K = len(U)
    tag = '%s_n%d_%s' % (name, n, 'role' if role else 'norole')
    out = ['## %s, n = %d, ROLE %s: %d programs, %d classes, divergent pairs %.4f' % (name, n, 'on' if role else 'off', len(E['ids']), K, E['div']), '']
    oc = [D.state_outcomes(JA, g, np.eye(K)[c] * 100) for c in range(K)]
    eff = [c for c in range(K) if oc[c]['dwl'] < 1e-9]
    out.append('Classes whose self-play is efficient (monomorphic conventions): %d, prior mass %.4f.' % (len(eff), mu[eff].sum()))
    out += ['', '| class | partition (self-play) | mu | programs | reads opponent |', '|---|---|---|---|---|']
    reads = D.conditions_on_demand(E['L'], E['ids'], E['members'])
    bypart = {}
    for c in eff:
        part = [k for k, v in oc[c].items() if k not in ('dwl', 'ineff', 'clash') and v > 1 - 1e-9][0]
        bypart.setdefault(part, []).append(c)
        out.append('| `%s` | %s | %.4f | %d | %s |' % (names[c], part, mu[c], sizes[c], 'yes' if reads[c] else 'no'))
    out += ['', 'Prior mass by partition: ' + ', '.join('%s %.4f' % (p, mu[cs].sum()) for p, cs in bypart.items()), '']
    out.append('Program-weighted (seeding) mass by partition: ' + ', '.join('%s %.4f' % (p, sizes[cs].sum() / sizes.sum()) for p, cs in bypart.items()))
    res[tag] = dict(n_prog=len(E['ids']), K=K, eff=[names[c] for c in eff], mu_part={p: float(mu[cs].sum()) for p, cs in bypart.items()},
                    size_part={p: float(sizes[cs].sum() / sizes.sum()) for p, cs in bypart.items()})
    # pairwise contests among the top conventions (up to 4 by mu)
    top = sorted(eff, key=lambda c: -mu[c])[:4]
    out += ['', 'Pairwise contests (row q invades column a): payoff of q against a / a against q, crossing frequency of q, '
            'Moran fixation of one q at N = 100 / 1,000 / 10,000 (w = 0.3; neutral 1/N).', '',
            '| q | a | u(q,a) / u(a,q) | crossing | rho N=100 | rho N=1000 | rho N=10000 |', '|---|---|---|---|---|---|---|']
    pw = {}
    for q in top:
        for a in top:
            if q == a:
                continue
            cr = crossing(U, a, q)
            r = [rho(U, q, a, N) for N in (100, 1000, 10000)]
            pw['%s|%s' % (names[q], names[a])] = dict(cross=cr, rho=r)
            out.append('| `%s` | `%s` | %.3f / %.3f | %s | %.3g | %.3g | %.3g |' % (names[q], names[a], U[q, a], U[a, q], '%.3f' % cr if cr else '-', *r))
    res[tag]['pairwise'] = pw
    # best direct invader of each convention (largest rho at N = 100 and 1000, over all classes)
    out += ['', 'Strongest single-mutant invaders of each convention (by mu * rho, N = 100 and 1,000):', '']
    for a in top:
        for N in (100, 1000):
            sc = []
            for q in range(K):
                if q != a:
                    sc.append((mu[q] * rho(U, q, a, N), q))
            sc.sort(reverse=True)
            tot = sum(s for s, _ in sc)
            out.append('- `%s`, N = %d: total exit mu*rho %.3g; top %s' % (names[a], N, tot, ', '.join('`%s` %.2g (rho %.2g)' % (names[q], s, s / mu[q]) for s, q in sc[:4])))
    # single-island replicator from the program-uniform composition and from random program-uniform draws of size 100
    x0 = sizes / sizes.sum()
    x, st, _, _ = replicator(U, x0, rest_tol=1e-10, ext_tol=1e-8)
    o = D.state_outcomes(JA, g, x * 1e6)
    out += ['', 'Replicator from the program-uniform composition (one well-mixed island, deterministic): rest %s; outcome %s.' % (
        ', '.join('`%s` %.3f' % (names[c], x[c]) for c in np.argsort(-x)[:4] if x[c] > 1e-3),
        ', '.join('%s %.3f' % (k, v) for k, v in o.items() if v > 1e-3))]
    rng = np.random.default_rng(5)
    agg = {}
    for t in range(400):
        cnt = rng.multinomial(100, x0)
        xs, st, _, _ = replicator(U, cnt / 100.0, rest_tol=1e-10, ext_tol=1e-8)
        o = D.state_outcomes(JA, g, xs * 1e6)
        key = max((k for k in o if k not in ('dwl',)), key=lambda k: o[k])
        key = key if o[key] > 0.99 else 'mixed:' + '+'.join(sorted(k for k in o if k != 'dwl' and o[k] > 0.05))
        agg[key] = agg.get(key, 0) + 1
    out.append('Replicator from 400 multinomial(100) draws of that composition: ' + ', '.join('%s %.3f' % (k, v / 400) for k, v in sorted(agg.items(), key=lambda kv: -kv[1])) + '.')
    res[tag]['island_basins'] = {k: v / 400 for k, v in agg.items()}
    out.append('')
    return out


if __name__ == '__main__':
    main()
