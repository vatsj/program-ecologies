"""Does the size-7 level-PA key family contain a prudent program (D against CooperateBot and DefectBot, C against FairBot and
against a copy of itself) as a one-fill program, for either default?"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import numpy as np
import hooks_beh as HB
import hooks_w2 as H

B = HB.Beh()
KT = B.KT
N = HB.named_programs(B)
panel = ['CooperateBot', 'DefectBot', 'FairBot']
for dname, base, act in (('HOOK(0,D) + (key -> C)', B.base('HOOK(0,D)'), 1), ('HOOK(0,C) + (key -> D)', B.base('HOOK(0,C)'), 0)):
    hits = []
    for k in KT.keys:
        if k['family'] == 'legacy' and k['id'] < 8:
            continue
        sp = B.spec([H.fcode(act, 0, H.BEH, H.SEEDED, k['id'])], 1)
        s = ''.join('CD'[1 - B.play(base, sp, *N[q])[0]] for q in panel) + 'CD'[1 - B.play(base, sp, base, sp)[0]]
        if s == 'DDCC':
            hits.append(k['name'])
    print(dname, ': keys with signature (CooperateBot D, DefectBot D, FairBot C, copy of itself C):', len(hits), hits[:10])
# the same with the d-clause read one level up, by the pure-Python reference (box1 ignores world 0)
