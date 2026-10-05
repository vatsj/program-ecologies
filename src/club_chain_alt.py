"""Extra diagnostic (not predicted): the chain at n = 8 on a smaller fixed point, K' = K_max without the four
member-exploiting members `and(CLUB(THEM),not(BOX...))` and the four BOXD-guarded ones, which is also a fixed point
(every subset of the full-set limit K* at n = 8 is one, runs/club_lattice.json).  Shows how much of the within-K outcome the selection of the fixed
point decides.

    python3 src/club_chain_alt.py      # writes runs/club_chain_alt.json
"""
import json, os, sys
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import club_chain as CC

ROOT = CC.ROOT


def main():
    km = [r for r in json.load(open(os.path.join(ROOT, 'runs', 'club_maximal.json'))) if r['n'] == 8 and r['mode'] == 'full'][0]['K_max_members']
    alt = [s for s in km if 'not(' not in s and 'BOXD' not in s]
    print('K\' =', alt, flush=True)
    K = {(8, 'alt'): alt}
    J = [('club', 8, N, 'alt') for N in (100, 1000, 10000)]
    rows = []
    with Pool(2, initializer=CC._init, initargs=(K,)) as pool:
        for r in pool.imap_unordered(CC.cell, J):
            rows.append(r)
            print('alt n=8 N=%d: P(C,C) %.4f pi(K) %.6f top %s %.3f; support %s; hit %.3g' % (r['N'], r['pcc'], r['pi_K'], r['top_K'], r['pi_top_K'],
                  r['support'][:3], r['hit_K']), flush=True)
    rows.sort(key=lambda r: r['N'])
    json.dump(dict(K_alt=alt, rows=rows), open(os.path.join(ROOT, 'runs', 'club_chain_alt.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
