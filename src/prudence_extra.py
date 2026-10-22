"""Extra tables for the prudence run (post-hoc reads of the same rows; declared in runs/prudence.md as such).

    python3 src/prudence_extra.py [--rows ...] [--out runs/prudence-extra.json]
"""
import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import prudence_report as RP

ROOT = RP.ROOT


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rows', nargs='+', default=[os.path.join(ROOT, 'runs/prudence/cells_main.json.gz'),
                                                  os.path.join(ROOT, 'runs/prudence/cells_ext.json.gz')])
    ap.add_argument('--out', default=os.path.join(ROOT, 'runs', 'prudence-extra.json'))
    a = ap.parse_args()
    d = RP.load(a.rows)
    out = {}
    lines = []
    for (w, arm) in sorted(d):
        rs = [d[(w, arm)][k] for k in sorted(d[(w, arm)])]
        n = len(rs)
        # identity after the merge's first 50 generations; at the merge
        id_merge = [r['comp']['light']['ident'] for r in rs]
        id_post = [max([t['ident'] for t in r['trace'] if t['g'] >= 250] or [0.0]) for r in rs]
        Q_post = [max([t['Q'] for t in r['trace'] if t['g'] >= 250] or [0.0]) for r in rs]
        # time-averaged standing shares over the tail (trapezoid on the trace, g <= 10200)
        def tavg(key):
            v = []
            for r in rs:
                g = np.array([t['g'] for t in r['trace']], float); x = np.array([t[key] for t in r['trace']], float)
                m = g <= 10200
                v.append(float(np.trapz(x[m], g[m]) / (g[m][-1] - g[m][0])) if m.sum() > 1 else 0.0)
            return float(np.mean(v))
        # realized selection advantage where defined (both prudent and unguarded present), over the first 2,000 tail generations
        sel, frac_def = [], []
        for r in rs:
            tr = [t for t in r['trace'] if t['g'] <= 2200]
            vals = [t['sel_adv'] for t in tr if t['sel_adv'] is not None]
            frac_def.append(len(vals) / max(1, len(tr)))
            if vals: sel.append(float(np.mean(vals)))
        # change of the prudent share from the merge to the tail's end
        dg = [RP.endpoint(r, RP.TAIL_T)['prud'] - r['comp']['light']['prud'] for r in rs if RP.endpoint(r, RP.TAIL_T)]
        # failures to be universal-open or target at the tail's end
        fail = []
        for r in rs:
            e = RP.endpoint(r, RP.TAIL_T)
            if e and (e['lost'] or not e['uo']):
                fail.append(dict(rep=r['rep'], pcc=e['pcc'], M=e['M'], T=e['T'], status=e['status'], h_sp=e['h_sp']))
        # not on target at the tail's end: the plurality
        offt = []
        for r in rs:
            e = RP.endpoint(r, RP.TAIL_T)
            if e and e['T'] is not None and e['T'] < 0.95:
                offt.append(dict(rep=r['rep'], T=round(e['T'], 3), off=round(e['off'], 3), prud=round(e['prud'], 3)))
        o = dict(n=n, ident_merge_mean=float(np.mean(id_merge)), ident_merge_ge05=int(sum(1 for x in id_merge if x >= 0.05)),
                 ident_post_max=float(max(id_post)), ident_post_ge05=int(sum(1 for x in id_post if x >= 0.05)),
                 Q_post_max=float(max(Q_post)),
                 suck_c_tavg=tavg('suck_c'), suck_u_tavg=tavg('suck_u'), prud_tavg=tavg('prud'), off_tavg=tavg('off'),
                 sel_adv_mean_2000=(float(np.mean(sel)) if sel else None), sel_adv_defined_frac=float(np.mean(frac_def)),
                 d_prud_merge_to_tailend=float(np.mean(dg)), fail=fail, not_on_target=offt)
        out['%s:%s' % (w, arm)] = o
        lines.append((w, arm, n, round(o['ident_merge_mean'], 4), o['ident_merge_ge05'], round(o['ident_post_max'], 4), o['ident_post_ge05'],
                      round(o['suck_c_tavg'], 4), round(o['suck_u_tavg'], 4),
                      None if o['sel_adv_mean_2000'] is None else round(o['sel_adv_mean_2000'], 5), round(o['sel_adv_defined_frac'], 2),
                      round(o['d_prud_merge_to_tailend'], 3), len(fail), len(offt)))
    json.dump(out, open(a.out, 'w'), indent=1)
    print('world arm n ident_merge_mean ident_merge>=.05 ident_post_max ident_post>=.05 suck_c_tavg suck_u_tavg sel_adv(0-2000) defined d_prud(merge->end) failures not_on_target')
    for l in lines: print(*l)


if __name__ == '__main__':
    main()
