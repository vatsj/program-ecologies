"""Re-run the priced Exp 1 cells that the polish bug could reach (every
c = 1e-3 cell; costs at c >= 1e-2 are multiples of c, so no payoff gap falls
below the 1e-3 polish threshold) with the fixed chain (commit a49a007), and
compare with runs/priced_limN.json.

    python3 src/priced_recheck.py
Writes runs/priced_recheck.md/json.
"""
import json, os, sys
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from priced_limN import cell

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    old = {(r['n'], r['pricing'], r['c'], r['N']): r for r in json.load(open(os.path.join(ROOT, 'runs', 'priced_limN.json')))
           if r['exp'] == 'exp1'}
    free = {(k[0], k[3]): r['pcc'] for k, r in old.items() if k[2] == 0}
    J = sorted([('exp1', n, c, 0, N, 'per', p) for (n, p, c, N) in old if c == 1e-3], key=lambda j: (-j[1], -j[4]))
    rows = []
    with Pool(3) as pool:
        for r in pool.imap_unordered(cell, J):
            rows.append(r); print(r['n'], r['pricing'], r['N'], '%.4f' % r['pcc'], flush=True)
    rows.sort(key=lambda r: (r['n'], r['pricing'], r['N']))
    L = ['# Priced arm, c = 1e-3 cells re-run with the fixed chain (a49a007)', '',
         '| n | pricing | N | P(C,C) before | after | free arm (c = 0) | polymorphic π before / after | FairBot exits strict / neutral (after) | support (after, top 3) |',
         '|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        o = old[(r['n'], r['pricing'], r['c'], r['N'])]
        L.append('| %d | %s | %d | %.4f | %.4f | %.4f | %.1e / %.1e | %.2e / %.2e | %s |' % (
            r['n'], r['pricing'], r['N'], o['pcc'], r['pcc'], free[(r['n'], r['N'])], o['poly'], r['poly'],
            r['fb_exit_strict'], r['fb_exit_neutral'], '; '.join('%s %.3f' % sp for sp in r['support'][:3])))
    json.dump(rows, open(os.path.join(ROOT, 'runs', 'priced_recheck.json'), 'w'), indent=1, default=str)
    open(os.path.join(ROOT, 'runs', 'priced_recheck.md'), 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))


if __name__ == '__main__':
    main()
