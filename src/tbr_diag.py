"""Queue 81 diagnostics (exploratory, not registered): in diverse worlds, do the competing majority profiles differ in
outcome (payoff vector) or only off path?  And which programs hold the islands.

    python3 src/tbr_diag.py > runs/tbr/diag.txt
"""
import glob, gzip, json, os, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    import tbr
    arms = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'runs', 'tbr_rows', 'tm', '*.json.gz'))):
        r = json.load(gzip.open(f, 'rt'))
        a = r['arm']
        if a not in arms:
            arms[a] = tbr.Tri(a)
        A = arms[a]
        key = (a, r['N'], r['lam'], r['mN'], 'S3' if r.get('supply') else 'main')
        for snap in ('100',):
            w = r['snaps'][snap]['world']
            cs = r['snaps'][snap]['cases']
            maj = {}
            for c in cs:
                maj.setdefault(c['i'], [0, 0, 0])[c['j']] = c['p']
            profs = Counter(tuple(v) for v in maj.values())
            pv = {}
            for p in profs:
                pv[p] = tuple(np.round(A.pay([p[0]], [p[1]], [p[2]])[0, 0, 0], 9))
            outs = Counter()
            for p, n in profs.items():
                outs[pv[p]] += n
            big_out = [o for o, n in outs.items() if n >= 0.05 * len(maj)]
            DIAG[key].append(dict(diverse=w['diverse'], n_out_big=len(big_out), n_prof=len(profs),
                                  top=[(list(p), n) for p, n in profs.most_common(3)]))
    for key in sorted(DIAG):
        rows = DIAG[key]
        div = [x for x in rows if x['diverse']]
        print('%s N=%d Lam=%g mN=%g %s: worlds %d, diverse in programs %d, of which diverse in outcomes %d' % (
            key[0], key[1], key[2], key[3], key[4], len(rows), len(div), sum(1 for x in div if x['n_out_big'] >= 2)))
    # names of arm T holders
    A = arms.get('T')
    if A is not None:
        hold = Counter()
        for f in glob.glob(os.path.join(ROOT, 'runs', 'tbr_rows', 'tm', 'T_*_100_1.json.gz')):     # stage 1 only
            r = json.load(gzip.open(f, 'rt'))
            for c in r['snaps']['100']['cases']:
                hold[(c['j'], A.names[c['p']])] += 1
        print('arm T holders (slot, program): islands', hold.most_common(12))


DIAG = defaultdict(list)
if __name__ == '__main__':
    main()
