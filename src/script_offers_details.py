"""Queue 80: occupancy, scramble and charge details of selected step-2 cells (markdown to stdout and step2_details.json).

    python3 src/script_offers_details.py OUTDIR
"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import script_offers_report as R

BULLY = ('s_bully', 'k_bully')
SHORT = {'s_open': 'Oc', 's_acc': 'Rc', 's_firm': 'Fc', 's_bully': 'Bc', 's_open+': 'Oc+', 's_acc+': 'Rc+', 's_firm+': 'Fc+',
         's_prud+': 'Pc+', 's_openR+': 'OcR+', 's_accR+': 'RcR+', 'k_open': 'Oc', 'k_acc': 'Rc', 'k_firm': 'Fc', 'k_bully': 'Bc',
         'bully': 'B', 'single': 'F', 'two': 'F', 'exploit': 'X', 'accepter': 'R'}


def short(f):
    return SHORT.get(f, f)


if __name__ == '__main__':
    out = sys.argv[1]
    rows = R.load('runs/sco_rows/*/rows_*.jsonl')
    rows = {k: v for k, v in rows.items() if v['series'] not in ('pilot', 'v1')}
    agg = R.aggregate(rows)
    res = {}
    L = []
    cells = [(a, 3.0, ph, 200, d) for a, ph in (('A2', 0.0), ('A2', 0.5), ('A4', 0.5), ('A5', 0.5), ('K2', 0.5), ('K', 0.5), ('A3', 1.0), ('A4', 1.0))
             for d in (0.03, 0.003)]
    L.append('| cell (β 3, N 200) | fair islands | paired slots: family (share) | Bc share paired / excluded | Bc partners | islands with Bc / B on ⅔ | unequal holders |')
    L.append('|---|---|---|---|---|---|---|')
    for k in cells:
        e = agg.get(k + (None,))
        if not e:
            continue
        pair = {}
        sp = {}
        for kk, n in e['hold'].items():
            role, fam, s = kk.split('|')
            if role == 'pair':
                pair[short(fam)] = pair.get(short(fam), 0) + n
                if s != '-':
                    sp[s] = sp.get(s, 0) + n
        tot = sum(pair.values())
        top = sorted(pair.items(), key=lambda x: -x[1])[:5]
        unq = {}
        nrun = e['n']
        partners = {short(p): n for p, n in e['bc_pair_partner'].items()}
        r = dict(cell=k, pair_slots=tot, pair_fams={a: n for a, n in pair.items()}, spellings_in_pairs=sp, bc_pair=e['bc_pair_share'],
                 bc_excl=e['bc_excl_share'], bc_partners=partners, bc_on_23=e['bc_on_23_share'], sb_on_23=e['sb_on_23_share'], vstar=e['vstar'],
                 same_class=e['same_class'], charges=e['charges'])
        res['|'.join(map(str, k))] = r
        L.append('| %s φ%g δ%g (V* %.2f) | %d of %d | %s | %s / %s | %s | %.3f / %.3f | |' % (
            k[0], k[2], k[4], e['vstar'], tot // 2, 64 * nrun, ', '.join('%s %.2f' % (a, n / tot) for a, n in top) if tot else '–',
            e['bc_pair_share'], e['bc_excl_share'], ', '.join('%s %d' % (a, n) for a, n in sorted(partners.items(), key=lambda x: -x[1])[:4]),
            e['bc_on_23_share'], e['sb_on_23_share']))
    # scramble and charges per arm (mean over every N = 200 cell)
    sc = {}
    for k, e in agg.items():
        if k[3] == 200 and k[5] is None:
            s = sc.setdefault(k[0], [[], []])
            s[0].append(e['same_class']); s[1].append(e['charges'])
    L.append('')
    L.append('| arm | 30N-to-120N class agreement (mean over cells) | mean read + forfeit charge per slot at 120N |')
    L.append('|---|---|---|')
    for a, (x, y) in sorted(sc.items()):
        L.append('| %s | %.3f | %.4f |' % (a, float(np.mean(x)), float(np.mean(y))))
        res['scramble_' + a] = [float(np.mean(x)), float(np.mean(y))]
    # spellings in pairs (A2, beta 3, phi 1/2, pooled over delta)
    spool = {}
    for d in R.DELTAS:
        e = agg.get(('A2', 3.0, 0.5, 200, d, None))
        for kk, n in e['hold'].items():
            role, fam, s = kk.split('|')
            if role == 'pair' and s != '-':
                spool[s] = spool.get(s, 0) + n
    t = sum(spool.values())
    L.append('')
    L.append('A2 (β 3, φ ½, pooled over δ): paired fair-island slots held by carriers, by spelling: ' +
             ', '.join('%s %.3f' % (s, n / t) for s, n in sorted(spool.items())))
    res['A2_spelling_shares'] = {s: n / t for s, n in spool.items()}
    json.dump(res, open(os.path.join(out, 'step2_details.json'), 'w'), indent=1, default=str)
    print('\n'.join(L))
