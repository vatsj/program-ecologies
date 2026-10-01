"""Exp D of predictions/2026-10-01-price-scaling-path.md: the priced modal arm
(atoms pricing) along joint paths c_N = c0 * (N / 1000)^(-alpha) in the eps->0
chain.

    python3 src/scaling_path.py [workers]
Writes runs/scaling_path.md/json.
"""
import json, os, sys
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import modal as M
from chain import fixation
from priced_limN import cell

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = (100, 1000, 10000, 30000, 100000, 300000)
PATHS = [(6, 1e-2, 0.25), (6, 1e-2, 0.5), (6, 1e-2, 0.6), (6, 1e-2, 0.75), (6, 1e-2, 1.0), (6, 1e-2, 1.5),
         (6, 1e-3, 0.5), (6, 1e-1, 0.5), (6, 3e-2, 0.25), (8, 1e-2, 0.5)]
W = 0.3


def rates(n, c, N):
    """Two-edge diagnostics: mutation-weighted entry into all-D of every
    self-cooperating class, sum mu_q rho(q | D), and the ALLC exit
    mu(C) rho(C | FairBot)."""
    _, _, _, prov = M.build_priced(n, c, pricing='atoms')
    U, P, nm = prov.Ufull, prov.PCC, prov.names
    mu = np.array([t[2] for t in prov.classes])
    D, C, F = nm.index('D'), nm.index('C'), nm.index('BOX(THEM(ME))')
    rho = lambda q, a: fixation(U[q, q], U[q, a], U[a, q], U[a, a], N, W, N)
    entry = sum(mu[q] * rho(q, D) for q in range(len(nm)) if P[q, q] == 1 and q != C)
    return dict(entry_family=float(entry), entry_fb=float(mu[F] * rho(F, D)), exit_allc=float(mu[C] * rho(C, F)))


def job(spec):
    n, c0, alpha, N = spec
    c = c0 * (N / 1000.0) ** (-alpha) if c0 > 0 else 0.0
    r = cell(('pathD', n, c, 0, N, 'per', 'atoms'))
    r.update(c0=c0, alpha=alpha, **rates(n, c, N))
    return r


def jobs():
    J = [(n, c0, a, N) for n, c0, a in PATHS for N in NS if not (c0 == 3e-2 and N > 100000)]
    J = sorted(J, key=lambda j: (-j[3], -j[0]))
    return [(6, 0.0, 0.0, N) for N in (100000, 300000)] + J   # free-arm extension first


def main(workers=3):
    rows = []
    with Pool(workers) as pool:
        for r in pool.imap_unordered(job, jobs()):
            rows.append(r)
            print('n=%d c0=%g alpha=%g N=%d c=%.3g: P(C,C) %.4f pi(D) %.4f pi(FB) %.4f poly %.1e FB exit strict %.2e neutral %.2e (%.0fs)' % (
                r['n'], r['c0'], r['alpha'], r['N'], r['c'], r['pcc'], r['pi_D'], r['pi_FB'], r['poly'],
                r['fb_exit_strict'], r['fb_exit_neutral'], r['time_s']), flush=True)
            json.dump(rows, open(os.path.join(ROOT, 'runs', 'scaling_path.json'), 'w'), indent=1, default=str)
    rows.sort(key=lambda r: (r['n'], r['c0'], r['alpha'], r['N']))
    L = ['# Price scaling paths c_N = c0 (N/1000)^-alpha: eps->0 chain, atoms pricing, PD, w = 0.3', '',
         '| n | c0 | alpha | N | c | P(C,C) | π(all-D) | π(all-FairBot) | π(all-ALLC) | polymorphic π | cut flow | near-closed | FairBot exits: strict / neutral | Σμρ entry (family / FairBot) | ALLC exit μρ | terminal | support (top 4) |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        L.append('| %d | %g | %g | %d | %.3g | %.4f | %.4f | %.4f | %.4f | %.1e | %.1e | %d | %.2e / %.2e | %.2e / %.2e | %.2e | %d | %s |' % (
            r['n'], r['c0'], r['alpha'], r['N'], r['c'], r['pcc'], r['pi_D'], r['pi_FB'], r['pi_C'], r['poly'], r['cut_flow'], r['near_closed'],
            r['fb_exit_strict'], r['fb_exit_neutral'], r.get('entry_family', 0), r.get('entry_fb', 0), r.get('exit_allc', 0), r['n_terminal'], '; '.join('%s %.3f' % sp for sp in r['support'][:4])))
    open(os.path.join(ROOT, 'runs', 'scaling_path.md'), 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
