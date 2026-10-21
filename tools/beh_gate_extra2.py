"""Prudent classes: one-fill programs HOOK(0, d) + (key -> action) whose signature is prudent (D against CooperateBot and
DefectBot, C against FairBot and against a copy of itself), and those with the named PrudentBot's full panel signature, for
the level-PA family (box only) and the family with box1 admitted; counts of key classes and prior mass, per family."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import numpy as np
import hooks_beh as HB
import hooks_w2 as H

PANEL = ['CooperateBot', 'DefectBot', 'FairBot', 'TrustingBot', 'GodelPredator']


def signatures(B):
    N = HB.named_programs(B)
    out = {}
    for dname, base, act in (('D-default (key -> C)', B.base('HOOK(0,D)'), 1), ('C-default (key -> D)', B.base('HOOK(0,C)'), 0)):
        sig = {}
        for k in B.KT.keys:
            if k['family'] == 'legacy' and k['id'] < 8:
                continue
            sp = B.spec([H.fcode(act, 0, H.BEH, H.SEEDED, k['id'])], 1)
            s = ''.join('CD'[1 - B.play(base, sp, *N[q])[0]] for q in PANEL) + 'CD'[1 - B.play(base, sp, base, sp)[0]]
            sig[k['id']] = s
        out[dname] = sig
    pb = ''.join('CD'[1 - B.play(*N['PrudentBot'], *N[q])[0]] for q in PANEL) + 'CD'[1 - B.play(*N['PrudentBot'], *N['PrudentBot'])[0]]
    fb = ''.join('CD'[1 - B.play(*N['FairBot'], *N[q])[0]] for q in PANEL) + 'CD'[1 - B.play(*N['FairBot'], *N['FairBot'])[0]]
    return out, pb, fb


def report(label, B):
    KT = B.KT
    sigs, pb, fb = signatures(B)
    print('== %s: %d keys (%d full-family classes, %d a-free classes, 10 legacy)' % (label, len(KT.keys), len(KT.full_ids), len(KT.noa_ids)))
    print('PrudentBot signature (vs CooperateBot, DefectBot, FairBot, TrustingBot, GodelPredator, copy):', pb, ' FairBot:', fb)
    for dname, sig in sigs.items():
        for fam, ids, prior in (('full', KT.full_ids, KT.prior_full), ('a-free', KT.noa_ids, KT.prior_noa)):
            prud = [i for i in ids if sig[i][0] == 'D' and sig[i][1] == 'D' and sig[i][2] == 'C' and sig[i][5] == 'C']
            pbs = [i for i in ids if sig[i] == pb]
            fbs = [i for i in ids if sig[i] == fb]
            print('  %-22s %-7s prudent (D,D,C,.,.,C): %4d classes, prior mass %.4f | PrudentBot signature: %4d, %.4f | FairBot signature: %4d, %.4f'
                  % (dname, fam, len(prud), sum(prior[i] for i in prud), len(pbs), sum(prior[i] for i in pbs), len(fbs), sum(prior[i] for i in fbs)))
            if fam == 'full' and prud:
                print('      shortest prudent:', sorted([(KT.keys[i]['size'], KT.keys[i]['name']) for i in prud])[:6])


if __name__ == '__main__':
    report('level PA only (box)', HB.Beh(level1=False))
    report('box and box1', HB.Beh(level1=True))
