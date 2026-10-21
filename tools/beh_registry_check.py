"""Registry identity is by truth table at word length 5; check that no merged boxed subformulas differ at word length 6 and 7
(hash of the table, memo cleared between formulas)."""
import os, sys, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import hooks_beh as HB

KT = HB.KeyTable()
# all boxed subformulas occurring in any key (before registry dedupe): collect from key forms
boxes = {}


def walk(f):
    if isinstance(f, str):
        return
    if f[0] in ('box', 'box1'):
        boxes[f] = 1
    for g in f[1:]:
        walk(g)


for k in KT.keys:
    walk(k['form'])
print('distinct boxed subformulas (syntactic):', len(boxes), ' registry entries:', KT.R)
for L in (6, 7):
    ps = HB.PointSpace(3, L)
    groups = {}
    for f in boxes:
        tt5 = KT.ps.tt(f, HB.ATOMS).tobytes()
        ps.memo.clear()
        h = hashlib.md5(ps.tt(f, HB.ATOMS).tobytes()).hexdigest()
        groups.setdefault(tt5, set()).add(h)
    bad = sum(1 for v in groups.values() if len(v) > 1)
    print('word length', L, ': groups at length 5:', len(groups), ' groups split at this length:', bad, flush=True)
