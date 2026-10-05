"""Post-hoc analysis of saved union chains: the fair states (support, exits,
exit slope over N) and the boss "wage fakers" that defeat the union's wage check.

    python3 src/union_post.py --arm quorum --c 0.5
"""
import argparse, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import union as U
from union_chain import UChain
from union_run import load, exits, describe, state_info, OUT


def fair_analysis(arm, c, N, top=12):
    d, C, nmw, nmb = load(arm)
    z = np.load(os.path.join(OUT, '%s_c%g_N%d_chain.npz' % (arm, c, N)))
    ch = UChain(C, c, N, arm=arm, verbose=False)
    codes, lpi = z['codes'], z['lpi']; pi = np.exp(lpi)
    summ = np.array([state_info(int(t))['summ'] for t in z['typ']])
    fair = np.nonzero(summ == 0)[0]
    order = fair[np.argsort(-pi[fair])]
    pf = pi[fair].sum()
    rows = []
    for k in order[:top]:
        ex, tot = exits(ch, int(codes[k]), top=4)
        rows.append(dict(pi=float(pi[k]), share_of_fair=float(pi[k] / pf), state=describe(d, C, *ch.decode(int(codes[k]))), exit_by_kind=tot,
                         top=[dict(p=e['prob'], kind=e['kind'], slot=['B', 'W1', 'W2'][e['slot']],
                                   mutant=(d['P'].src_b(C['repB'][e['cls']]) if e['slot'] == 0 else d['P'].src_w(C['repW'][e['cls']])), to=e['summ_to'])
                              for e in ex]))
    # exit rate out of the fair summary, by kind of the first move: pi-weighted
    src, dst, pr = z['src'], z['dst_idx'], z['pr']
    f = np.exp(lpi[src] + pr)
    leave = (summ[src] == 0) & (summ[dst] != 0)
    return dict(arm=arm, c=c, N=N, fair_mass=float(pf), fair_exit_rate=float(f[leave].sum() / pf) if pf > 0 else None, top=rows)


def wage_fakers(arm='quorum', c=0.5):
    """Boss programs that pay < 1/2 against a union pair (and against a militant pair), with the pair working."""
    d, C, nmw, nmb = load(arm)
    out = {}
    for name in ('union', 'militant', "union' (BOX(OTHER=strike))"):
        x = nmw.get(name)
        if x is None: continue
        L = []
        for b in range(C['KcB']):
            j = int(C['Jc'][b, x, x]); bb, a1, a2 = j // 4, (j // 2) % 2, j % 2
            if bb // 3 < 2 and a1 == 0 and a2 == 0:
                L.append(dict(boss=d['P'].src_b(C['repB'][b]), play=U.joint_name(j), mass=float(C['massB'][b])))
        out[name] = dict(n=len(L), mass=float(sum(e['mass'] for e in L)), examples=sorted(L, key=lambda e: -e['mass'])[:6])
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--arm', default='quorum')
    ap.add_argument('--c', type=float, default=0.5)
    a = ap.parse_args()
    res = dict(fakers=wage_fakers(a.arm, a.c), fair={})
    for N in (100, 1000, 10000):
        f = os.path.join(OUT, '%s_c%g_N%d_chain.npz' % (a.arm, a.c, N))
        if os.path.exists(f):
            res['fair'][str(N)] = fair_analysis(a.arm, a.c, N)
    rates = [(int(k), v['fair_exit_rate']) for k, v in res['fair'].items() if v['fair_exit_rate']]
    if len(rates) >= 2:
        x = np.log([r[0] for r in rates]); y = np.log([r[1] for r in rates])
        res['fair_exit_slope'] = float(np.polyfit(x, y, 1)[0])
    json.dump(res, open(os.path.join(OUT, 'post_%s_c%g.json' % (a.arm, a.c)), 'w'), indent=1, default=float)
    print(json.dumps(res['fakers'], indent=1))
    for N, v in res['fair'].items():
        print('N', N, 'fair mass %.4f exit rate %.3e' % (v['fair_mass'], v['fair_exit_rate'] or 0))
        for r in v['top'][:8]:
            print('  %.2e (%.2f of fair) %s' % (r['pi'], r['share_of_fair'], r['state']), {k: '%.1e' % q for k, q in r['exit_by_kind'].items()})
            for e in r['top'][:3]:
                print('       %.1e %s %s %s -> %s' % (e['p'], e['kind'], e['slot'], e['mutant'], e['to']))
    print('fair exit slope', res.get('fair_exit_slope'))
