"""Strong Nash in the provability arm against the alpha- and beta-cores (static).
notes/2026-11-23-case3-static.md; PROOFS P6-P9.  Actions C = 1, D = 0."""
import sys, os, json, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import provability as P
import dollar3 as D3

GAMES = {  # (a1, a2) -> (u1, u2)
    'PD': {(1, 1): (0, 0), (1, 0): (-2, 1), (0, 1): (1, -2), (0, 0): (-1, -1)},
    'MP': {(1, 1): (1, -1), (0, 0): (1, -1), (1, 0): (-1, 1), (0, 1): (-1, 1)},
    'Q':  {(1, 1): (1, 1), (1, 0): (0, 2), (0, 1): (0, 0), (0, 0): (1, 0)},
}
NAME = {(1, 1): 'CC', (1, 0): 'CD', (0, 1): 'DC', (0, 0): 'DD'}
OUT = list(NAME)


def cores(g):
    a_core, b_core = [], []
    for a in OUT:
        ua = g[a]
        pareto = any(g[x][0] > ua[0] and g[x][1] > ua[1] for x in OUT)
        # player 1 moves a1, player 2 moves a2
        al1 = any(all(g[(x, b)][0] > ua[0] for b in (0, 1)) for x in (0, 1))
        al2 = any(all(g[(b, x)][1] > ua[1] for b in (0, 1)) for x in (0, 1))
        be1 = all(any(g[(x, b)][0] > ua[0] for x in (0, 1)) for b in (0, 1))
        be2 = all(any(g[(b, x)][1] > ua[1] for x in (0, 1)) for b in (0, 1))
        if not (pareto or al1 or al2): a_core.append(NAME[a])
        if not (pareto or be1 or be2): b_core.append(NAME[a])
    return a_core, b_core


def analyse(n, kinds):
    L = P.ModalLanguage(n, kinds)
    val, _ = P.evaluate(L)
    v = val.astype(int); K = v.shape[0]
    mu = np.asarray(L.mu_canon, float); mu = mu / mu.sum()
    mine, theirs = v, v.T          # mine[i, j] = i's action against j; theirs[i, j] = j's action against i
    # reach[j][x][y]: some deviator plays x while resident j plays y
    reach = np.zeros((K, 2, 2), bool)
    for x in (0, 1):
        for y in (0, 1):
            reach[:, x, y] = ((mine == x) & (theirs == y)).any(axis=0)  # over deviators i against resident j
    reachable = {(x, y) for x in (0, 1) for y in (0, 1) if ((mine == x) & (theirs == y)).any()}
    res = {'n': n, 'K': K, 'reachable_outcomes': sorted(NAME[o] for o in reachable)}
    a1, a2 = mine, theirs          # profile (i, j): player 1 = i plays mine[i, j]; player 2 = j plays mine[j, i] = theirs[i, j]
    for gname, g in GAMES.items():
        u1 = np.zeros((2, 2)); u2 = np.zeros((2, 2))
        for (x, y), (p, q) in g.items(): u1[x, y] = p; u2[x, y] = q
        U1 = u1[a1, a2]; U2 = u2[a1, a2]
        # player 1 deviates against resident j: outcomes (x, y) in reach[j]; best u1
        best1 = np.full(K, -1e9); best2 = np.full(K, -1e9)
        for x in (0, 1):
            for y in (0, 1):
                best1 = np.where(reach[:, x, y], np.maximum(best1, u1[x, y]), best1)   # resident = player 2 = j
                best2 = np.where(reach[:, x, y], np.maximum(best2, u2[y, x]), best2)   # resident = player 1 = i
        dev1 = best1[None, :] > U1 + 1e-12
        dev2 = best2[:, None] > U2 + 1e-12
        pair = np.zeros((K, K), bool)
        for (x, y) in reachable:
            pair |= (u1[x, y] > U1 + 1e-12) & (u2[x, y] > U2 + 1e-12)
        sne = ~(dev1 | dev2 | pair)
        outs = {}
        for o in OUT:
            m = sne & (a1 == o[0]) & (a2 == o[1])
            if m.any():
                ii, jj = np.argwhere(m)[0]
                outs[NAME[o]] = {'profiles': int(m.sum()), 'example': [L.rep[ii], L.rep[jj]]}
        ac, bc = cores(g)
        res[gname] = {'alpha_core': ac, 'beta_core': bc, 'sne_outcomes': outs,
                      'sne_profiles': int(sne.sum())}
    # who reads whom
    match = (mine == theirs)
    res['universal_mirrors'] = [L.rep[i] for i in np.where(match.all(axis=1))[0]]
    res['universal_antimirrors'] = [L.rep[i] for i in np.where((~match).all(axis=1))[0]]
    can_match = match.any(axis=0); can_mis = (~match).any(axis=0)      # over deviators, per resident (column)
    both = can_match & can_mis
    res['R_mass'] = float(mu[both].sum()); res['R_count'] = int(both.sum())
    res['no_matcher'] = [L.rep[j] for j in np.where(~can_match)[0]][:8]
    res['no_mismatcher'] = [L.rep[j] for j in np.where(~can_mis)[0]][:8]
    # mirror quality: prior mass of opponents whose actual action each program matches
    mq = (match * mu[None, :]).sum(axis=1)
    top = np.argsort(-mq)[:3]
    res['best_mirrors'] = [[L.rep[i], round(float(mq[i]), 4)] for i in top]
    low = np.argsort(mq)[:3]
    res['best_antimirrors'] = [[L.rep[i], round(float(1 - mq[i]), 4)] for i in low]
    # exposure: never exploited (no opponent plays D against my C)
    expl = ((mine == 1) & (theirs == 0)).any(axis=1)
    unex = ~expl & (mine == 1).any(axis=1)          # cooperates with someone, never exploited
    res['unexploited_cooperators'] = int(unex.sum())
    res['unexploited_mass'] = float(mu[unex].sum())
    fb = [i for i, s in enumerate(L.rep) if s.replace(' ', '') == 'BOX(THEM(ME))']
    res['fairbot_unexploited'] = bool(fb and unex[fb[0]])
    res['fairbot_src_found'] = bool(fb)
    return res


def majority():
    blocked = 0; total = 0; unblocked = []
    acts = range(9)
    pays = {}
    for a in itertools.product(acts, acts, acts):
        u, _ = D3.outcome(D3.PARTNER, *a); pays[a] = tuple(int(x) for x in u)
    for a, ua in pays.items():
        total += 1; ok = False
        for S in ((0, 1), (0, 2), (1, 2)):
            t = ({0, 1, 2} - set(S)).pop()
            for xs in itertools.product(acts, acts):
                good = True
                for b in acts:
                    prof = [0, 0, 0]; prof[S[0]] = xs[0]; prof[S[1]] = xs[1]; prof[t] = b
                    u = pays[tuple(prof)]
                    if not (u[S[0]] > ua[S[0]] and u[S[1]] > ua[S[1]]): good = False; break
                if good: ok = True; break
            if ok: break
        if ok: blocked += 1
        else: unblocked.append([list(a), list(ua)])
    return {'profiles': total, 'alpha_blocked_by_a_pair_of_constants': blocked, 'unblocked': unblocked[:5]}


if __name__ == '__main__':
    out = {'full': [], 'pa_only': []}
    for n in (5, 6, 7, 8, 9):
        out['full'].append(analyse(n, ((0, 0), (1, 0), (0, 1), (1, 1))))
        out['pa_only'].append(analyse(n, ((0, 0), (1, 0))))
    out['majority'] = majority()
    os.makedirs('runs', exist_ok=True)
    json.dump(out, open('runs/case3-static.json', 'w'), indent=1)
    for arm in ('full', 'pa_only'):
        print('==', arm)
        for r in out[arm]:
            print('n', r['n'], 'K', r['K'], 'reach', r['reachable_outcomes'])
            for g in GAMES:
                print('  ', g, 'alpha', r[g]['alpha_core'], 'beta', r[g]['beta_core'], 'SNE',
                      {k: v['profiles'] for k, v in r[g]['sne_outcomes'].items()})
            print('   mirrors', r['universal_mirrors'][:3], 'anti', r['universal_antimirrors'][:3], 'R mass', round(r['R_mass'], 4),
                  'R count', r['R_count'], 'no matcher', r['no_matcher'][:3], 'no mismatcher', r['no_mismatcher'][:3])
            print('   best mirrors', r['best_mirrors'], 'best anti', r['best_antimirrors'])
            print('   unexploited cooperators', r['unexploited_cooperators'], round(r['unexploited_mass'], 4), 'FairBot', r['fairbot_unexploited'], r['fairbot_src_found'])
    print('majority', out['majority'])
