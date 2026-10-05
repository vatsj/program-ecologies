"""Certify the cut minima that k_at_n8.py's sharing table left as brackets (cut search aborted at 300k expansions),
with a larger expansion cap (specs/2026-10-05-k-at-n8.md, lemma sharing).

    python3 src/k_at_n8_certify.py [cap]
Writes runs/k-at-n8/certify.json.
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
import gl_proofs as G
import k_at_n8 as KN


def main(cap):
    d = json.load(open(os.path.join(KN.RUNS, 'k-at-n8-sharing.json')))
    out = []
    for r in d['rows']:
        for nm in ('C0', 'C1'):
            m = r[nm]
            if m is None or m['cut']['certified']: continue
            th = G.Theory(); x = th.prog(r['x']); y = th.prog(r['y']); orc = G.Oracle(th)
            R = dict(G.roots_for(th, x, y))
            at = [(frozenset(), frozenset([f])) for f, _, _, _ in G.atom_formulas(th, x, y)]
            cuts = G.cut_closure(th, [R['C0'], R['C1']] + at)          # the same cut set as the sharing table
            S = (frozenset(R[nm][0]), frozenset(R[nm][1]))
            ms = G.MinSearch(th, orc, cap=cap, cuts=cuts)
            t = time.time()
            res = ms.minimize(S, max_size=m['nocut']['size'] - 1)
            row = dict(x=r['x'], y=r['y'], root=nm, nocut=m['nocut']['size'], old_lb=m['cut'].get('lb'), t=time.time() - t)
            if res is None:
                row['result'] = 'non-theorem?'
            elif res['certified']:
                dm = ms.dag_sizes(S)
                row.update(cut=res['c'], certified=True, exact=dm['exact'], subs=dm['subsumption'])
            else:
                # no derivation below the cut-free size within max_size, or aborted
                lb = res['lb']
                row.update(certified=lb >= m['nocut']['size'], lb=lb, cut=[m['nocut']['size'], m['nocut']['loeb']] if lb >= m['nocut']['size'] else None)
            out.append(row)
            print(row, flush=True)
            json.dump(out, open(os.path.join(KN.KDIR, 'certify.json'), 'w'), indent=1)


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000)
