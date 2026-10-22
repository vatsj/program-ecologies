"""The gate's named table when PrudentBot's d-clause is read one level up ('box1', ignores world 0), by the pure-Python
reference (the registry evaluator is level-PA only)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import hooks_beh as HB

box = lambda f: ('box', f)
box1 = lambda f: ('box1', f)
REF = {'FairBot': ('D', [(box('a'), 1)]), 'TrustingBot': ('C', [(box(('not', 'a')), 0)]),
       'PrudentBot(box1 d)': ('D', [(('and', box('a'), box1(('not', 'd'))), 1)]), 'GodelPredator': ('C', [(box('a'), 0)]),
       'CooperateBot': ('C', []), 'DefectBot': ('D', [])}
names = list(REF)
print('%-20s' % '', *['%-8s' % n[:7] for n in names])
for x in names:
    row = []
    for y in names:
        rx, ry = HB.ref_match(REF[x], REF[y])
        assert rx[-6:] == [rx[-1]] * 6 and ry[-6:] == [ry[-1]] * 6
        row.append('CD'[1 - rx[-1]] + 'CD'[1 - ry[-1]])
    print('%-20s' % x, *['%-8s' % r for r in row])
rx, ry = HB.ref_match(REF['PrudentBot(box1 d)'], REF['FairBot'], 8)
print('PrudentBot(box1 d) vs FairBot, worlds 0-7:', ''.join('CD'[1 - v] for v in rx), ''.join('CD'[1 - v] for v in ry))
