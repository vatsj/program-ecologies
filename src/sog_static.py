"""Static acceptable outcomes of the social organization game in program space
(notes/2026-11-15-sog-static.md).  Boss picks a wage s in {0,1/4,1/2} and whom to
whack; each worker works or strikes.  Payoffs as in union.py without tags or pool:
worker s*work - L*whacked, boss sum over working (1-s) - c*whacks.

Deviation without response: the others' programs stay as written, so their reply to
a rewrite is whatever their text says.  Two brackets on what a coalition S can get:
  alpha: S blocks iff some a_S strictly improves every member against every reply
         (deviators are constants; the outsiders' text may punish as it likes);
  beta:  S blocks iff against every reply some a_S strictly improves every member
         (deviators read and move last).
Outcomes unblocked under beta are supportable however the reading regress resolves.
"""
import itertools, sys
from fractions import Fraction as F
W = [F(0), F(1, 4), F(1, 2)]
BOSS = [(s, w1, w2) for s in W for w1 in (0, 1) for w2 in (0, 1)]   # wage, whack W1, whack W2
WORK = [0, 1]                                                        # 0 work, 1 strike
ACT = [BOSS, WORK, WORK]

def pay(b, a1, a2, c, L=1):
    s, h1, h2 = b
    boss = sum((1 - s) for a in (a1, a2) if a == 0) - c * (h1 + h2)
    return (boss, (s if a1 == 0 else 0) - L * h1, (s if a2 == 0 else 0) - L * h2)

def cores(c, weak=False):
    prof = list(itertools.product(*ACT))
    U = {p: pay(*p, c) for p in prof}
    coal = [S for r in (1, 2, 3) for S in itertools.combinations(range(3), r)]
    def better(q, p, S):
        if weak:
            return all(U[q][i] >= U[p][i] for i in S) and any(U[q][i] > U[p][i] for i in S)
        return all(U[q][i] > U[p][i] for i in S)
    def mk(aS, aO, S, O):
        x = [None] * 3
        for i, a in zip(S, aS): x[i] = a
        for i, a in zip(O, aO): x[i] = a
        return tuple(x)
    out = {'alpha': [], 'beta': []}
    for p in prof:
        ab = bb = False
        for S in coal:
            O = [i for i in range(3) if i not in S]
            AS = list(itertools.product(*[ACT[i] for i in S])); AO = list(itertools.product(*[ACT[i] for i in O]))
            if any(all(better(mk(a, o, S, O), p, S) for o in AO) for a in AS): ab = True
            if all(any(better(mk(a, o, S, O), p, S) for a in AS) for o in AO): bb = True
        if not ab: out['alpha'].append(p)
        if not bb: out['beta'].append(p)
    return out, U

def name(p):
    (s, h1, h2), a1, a2 = p
    return 's=%s %s%s whack=%d%d' % (s, 'WS'[a1], 'WS'[a2], h1, h2)

if __name__ == '__main__':
    for c in (F(1, 10), F(1, 2), F(3, 2)):
        for weak in (False, True):
            o, U = cores(c, weak)
            print('c=%s %s: alpha %d, beta %d' % (c, 'weak' if weak else 'strict', len(o['alpha']), len(o['beta'])))
            for p in o['alpha']:
                print('   %-22s pay=%s%s' % (name(p), tuple(str(x) for x in U[p]), '' if p in o['beta'] else '   (alpha only)'))
