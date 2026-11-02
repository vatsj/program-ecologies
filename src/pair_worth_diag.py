"""Diagnostic: what are the majority programs of the final consensus state?  (G1/3 and G5/6, mN = 1, Lambda = 0.)
python3 src/pair_worth_diag.py  -> runs/pair_worth/diag.json"""
import json, os, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pair_worth as PW
import pair_worth_run as PR


def describe(menu, G, s, m):
    fi, si, c = menu.decode(int(m))
    if fi < 0:
        return 'const %s' % G.aname(s, c)
    f = menu.fams[fi]
    return '%s sigma=%s c=%s' % (f.kind, f.sigmas[si], G.aname(s, c) if c >= 0 else '-')


def diag(gname, arm, delta, runs=range(20), mN=1.0):
    G, CLA, CLB = PR.game_tables(gname)
    out = []
    kinds = collections.Counter()
    for r in runs:
        prep = PR.prepare(gname, arm, r, 100, delta, [0.0])
        o = PR.run_kernel(prep, 0.0, mN)
        counts = o['counts']; U = prep['U']; menu = prep['menu']
        modal = o['modal'][o['stop']]
        cls = CLB[modal.astype(np.int64)]
        # island 0 majority programs
        maj = [int(np.argmax(counts[0, s])) for s in range(3)]
        desc = [describe(menu, G, s, U[s][maj[s]]) for s in range(3)]
        fam = tuple('B' if d.startswith('B') else ('K' if d.startswith('K') else ('const' if d.startswith('const') else d.split()[0])) for d in desc)
        kinds[(int(cls[0]), fam)] += 1
        out.append(dict(run=r, cls=int(cls[0]), outcome=str(G.outs[int(modal[0])]), programs=desc))
    return dict(game=gname, arm=arm, delta=delta, mN=mN, runs=out, summary={'%d|%s' % k: v for k, v in kinds.items()})


def main():
    res = []
    for g, arm, d in (('pw13', 'CBs', 0.05), ('pw13', 'CB', 0.05), ('pw13', 'CBe', 0.05), ('pw13', 'C', 0.05), ('pw56', 'CB', 0.05), ('pw56', 'CBK', 0.05)):
        r = diag(g, arm, d)
        res.append(r)
        print(g, arm, d, r['summary'], flush=True)
    json.dump(res, open(os.path.join(PW.ROOT, 'runs', 'pair_worth', 'diag.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
