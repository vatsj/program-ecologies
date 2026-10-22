"""Follow-up to the launch gate (tools/beh_gate.py): which programs of the form HOOK(0, D) + (key -> C) in the size-7 level-PA
key family are FairBot-like, which are prudent (exploit CooperateBot, cooperate with FairBot and with themselves), and the
named table when PrudentBot's d-clause is read one level up (box1: ignores world 0), by the pure-Python reference."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import numpy as np
import hooks_beh as HB
import hooks_w2 as H
from collections import Counter

B = HB.Beh()
KT = B.KT
N = HB.named_programs(B)
hd = B.base('HOOK(0,D)')
panel = ['CooperateBot', 'DefectBot', 'FairBot', 'TrustingBot', 'GodelPredator']
sig = {}
for k in KT.keys:
    if k['family'] == 'legacy' and k['id'] < 8:
        continue
    sp = B.spec([H.fcode(1, 0, H.BEH, H.SEEDED, k['id'])], 1)
    s = ''
    for q in panel:
        ax, ay, _ = B.play(hd, sp, *N[q])
        s += 'CD'[1 - ax]
    ax, ay, _ = B.play(hd, sp, hd, sp)
    s += 'CD'[1 - ax]
    sig[k['id']] = s
fb = ''
for q in panel:
    fb += 'CD'[1 - B.play(*N['FairBot'], *N[q])[0]]
fb += 'CD'[1 - B.play(*N['FairBot'], *N['FairBot'])[0]]
print('signature order: vs', panel, 'and vs a copy of itself')
print('FairBot signature', fb)
c = Counter(sig.values())
print('distinct signatures among the %d keys (key -> C on HOOK(0,D)):' % len(sig))
for s, n in c.most_common():
    ex = [KT.keys[i]['name'] for i, v in sig.items() if v == s][:3]
    print('  %s  %4d keys, e.g. %s' % (s, n, ex))
# prudent signature: exploit CooperateBot (D), D vs DefectBot, cooperate with FairBot (C), cooperate with itself (C)
pr = [i for i, s in sig.items() if s[0] == 'D' and s[2] == 'C' and s[5] == 'C']
print('keys that exploit CooperateBot, cooperate with FairBot and with themselves:', len(pr), [KT.keys[i]['name'] for i in pr[:10]])
fbl = [i for i, s in sig.items() if s == fb]
print('keys with FairBot\'s signature:', len(fbl))
prior = KT.prior_full
print('prior mass of FairBot-signature keys (full family):', round(float(sum(prior[i] for i in fbl)), 4),
      ' of prudent-signature keys:', round(float(sum(prior[i] for i in pr)), 4))
