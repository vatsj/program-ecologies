"""Launch gate of specs/2026-10-21-behavioural-hooks.md: the named members' pairwise outcome table by the generalized solver
(hooks_beh.eval_match_beh, stabilized evaluation on finite linear GL frames) against an independent pure-Python Kripke
reference (hooks_beh.ref_match) and against the RE's hand derivation in the spec.  Prints the table and the verdict."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import numpy as np
import hooks_beh as HB

box = lambda f: ('box', f)
REF = {'FairBot': ('D', [(box('a'), 1)]), 'TrustingBot': ('C', [(box(('not', 'a')), 0)]),
       'PrudentBot': ('D', [(('and', box('a'), box(('not', 'd'))), 1)]), 'GodelPredator': ('C', [(box('a'), 0)]),
       'CooperateBot': ('C', []), 'DefectBot': ('D', [])}
# the RE's hand derivation (spec "Launch gate"): (x, y) -> (x's action, y's action)
HAND = {('FairBot', 'TrustingBot'): 'DC', ('GodelPredator', 'GodelPredator'): 'CC', ('FairBot', 'GodelPredator'): 'DC',
        ('PrudentBot', 'CooperateBot'): 'DC', ('PrudentBot', 'TrustingBot'): 'DC', ('PrudentBot', 'FairBot'): 'CC'}


def table(B):
    N = HB.named_programs(B)
    names = list(N)
    solver = {}; ref = {}
    for x in names:
        for y in names:
            bx, sx = N[x]; by, sy = N[y]
            ax, ay, rs = B.play(bx, sx, by, sy)
            solver[(x, y)] = 'CD'[1 - ax] + 'CD'[1 - ay]
            rx, ry = HB.ref_match(REF[x], REF[y])
            ref[(x, y)] = 'CD'[1 - rx[-1]] + 'CD'[1 - ry[-1]]
            assert rx[-6:] == [rx[-1]] * 6 and ry[-6:] == [ry[-1]] * 6, (x, y, rx, ry)
    return names, solver, ref


def main():
    B = HB.Beh()
    names, solver, ref = table(B)
    print('solver table (row x plays, column y plays; first letter = row program):')
    print('%-14s' % '', *['%-8s' % n[:7] for n in names])
    for x in names:
        print('%-14s' % x, *['%-8s' % solver[(x, y)] for y in names])
    print('solver vs independent reference: %d mismatches' % sum(solver[k] != ref[k] for k in solver))
    print('hand derivation vs solver:')
    ok = True
    for (x, y), h in HAND.items():
        s = solver[(x, y)]
        ok &= (s == h)
        print('  %-14s vs %-14s hand %s solver %s %s' % (x, y, h, s, 'ok' if s == h else 'DISAGREES'))
        rx, ry = HB.ref_match(REF[x], REF[y], 8)
        print('      worlds 0-7: %s: %s   %s: %s' % (x, ''.join('CD'[1 - v] for v in rx), y, ''.join('CD'[1 - v] for v in ry)))
    print('GATE', 'PASSED' if ok else 'FAILED')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
