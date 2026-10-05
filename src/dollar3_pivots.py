"""Directed flows between coalition states by role, from saved chains.

For every pair-to-pair transition: which slot moved (the excluded slot, the
member that stays = pivot, or the member that leaves), and the pivot's share
before and after.  Also flows between outcome types (grand, fair, unfair,
wasteful, disagreement), so that net currents between types are visible.

    python3 src/dollar3_pivots.py
Writes runs/dollar3/pivots.json.
"""
import glob, json, os
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = ['grand', 'fair', 'unfair', 'wasteful', 'X']


def analyse(path):
    f = np.load(path)
    codes, lpi, pay, typ = f['codes'], f['lpi'], f['pay'], f['typ']
    src, dst, pr = f['src'], f['dst_idx'], f['pr']
    keep = src != dst
    src, dst, pr = src[keep], dst[keep], pr[keep]
    fl = np.exp(lpi[src] + pr)
    M = np.zeros((5, 5))
    np.add.at(M, (typ[src], typ[dst]), fl)
    np.fill_diagonal(M, 0)
    net = M - M.T
    pairs = np.nonzero(np.isin(typ[src], [1, 2, 3]) & np.isin(typ[dst], [1, 2, 3]) & (pay[src] != pay[dst]).any(1))[0]
    a = pay[src[pairs]]; b = pay[dst[pairs]]
    ma = a > 0; mb = b > 0
    same = (ma == mb).all(1)
    both = ma & mb
    piv = np.argmax(both, axis=1)
    rows = np.arange(len(pairs))
    pa = a[rows, piv]; pb = b[rows, piv]
    roles = {}
    for k in np.unique(np.stack([same, pa, pb], 1), axis=0):
        sel = (same == k[0]) & (pa == k[1]) & (pb == k[2])
        if k[0]:
            key = 'same pair (share of first common member %s -> %s)' % (round(k[1] / 6, 3), round(k[2] / 6, 3))
        else:
            key = 'pivot %s -> %s' % (round(k[1] / 6, 3), round(k[2] / 6, 3))
        roles[key] = roles.get(key, 0.0) + float(fl[pairs[sel]].sum())
    pi = np.exp(lpi)
    return dict(type_flow={'%s>%s' % (T[i], T[j]): float(M[i, j]) for i in range(5) for j in range(5) if i != j and M[i, j] > 0},
                net_type_current={'%s>%s' % (T[i], T[j]): float(net[i, j]) for i in range(5) for j in range(5) if net[i, j] > 1e-300},
                pair_moves=dict(sorted(roles.items(), key=lambda kv: -kv[1])),
                mass={T[t]: float(pi[typ == t].sum()) for t in range(5)})


def main():
    out = {}
    for p in sorted(glob.glob(os.path.join(ROOT, 'runs', 'dollar3', '*_chain.npz'))):
        name = os.path.basename(p)[:-10]
        out[name] = analyse(p)
        print(name, {k: '%.2e' % v for k, v in list(out[name]['pair_moves'].items())[:4]})
        print('   net', {k: '%.2e' % v for k, v in out[name]['net_type_current'].items()})
    json.dump(out, open(os.path.join(ROOT, 'runs', 'dollar3', 'pivots.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
