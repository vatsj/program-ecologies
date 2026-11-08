"""Queue 76 (spec specs/2026-11-08-bully-resistance.md): bully-resistant readers in arm T.

The catalogue is T+ (queue 75: arm T's 27 programs, Trojan bullies Bn Bp, junk Jf Jr) plus

  prudent readers P  (8):  P<dir><fb><to>   strict probe (an inconclusive probe read counts as refuse)
  lenient probe  Q   (4):  Q<dir>z<to>      the probe variant: an inconclusive probe read counts as accept (fallback z only)
  openers        O   (8):  O<first><fb><to>

Prudent reader (reading partner j = next for dir n, previous for dir p; k the third slot): accept j iff the cooperation read says
j names me at 1/2 (T's convention `to`: y accepts a timed-out read, n does not) AND a second read of j, with the third slot
replaced by the constant that names j at 1/3, does NOT show j naming k at 2/3 (and, strict, is not inconclusive).  Accept = name j
at 1/2; else the fallback (o: the other slot at 1/2; z: null).  dir n: the probe replaces the `run` argument p by the quoted
constant C3 (k names its previous = j at 1/3); the exploit answer is code 2.  dir p: the probe replaces the capk argument n by the
quoted constant C0 (k names its next = j at 1/3); the exploit answer is code 5.

Opener O: read both others in the actual triple (a = what next names, b = what prev names).  If next names prev at 2/3 (a = 2) and
prev names next at 1/3 (b = 3), name prev at 1/2 (code 4); if prev names next at 2/3 (b = 5) and next names prev at 1/3 (a = 0),
name next at 1/2 (code 1); otherwise act as the two-partner reader D<first><fb><to> using the two values already read.

Nothing existing is edited.  The first 31 programs are exactly T+'s (V2).
"""
import os, sys, hashlib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lt_code as L
import churn_primary_t as CT
import tplus as TP

KS = CT.KS
SIMN = CT.SIMN
SIMP = CT.SIMP
Q3 = 'Q3CONST'      # symbol for the quoted constant program C3 (names its previous at 1/3), inlined by the compiler hook
Q0 = 'Q0CONST'
# a constant program (lambda (me n p) c) is the closed term lam lam lam (nat c)
for _nm, _c in ((Q3, 3), (Q0, 0)):
    L.CONST_SYMS[_nm] = ('quote', ('lam', ('lam', ('lam', ('nat', _c)))))

PROBEN = '(capk %d (run %d n %s) me)' % (KS, KS, Q3)
PROBEP = '(capk %d (run %d p me) %s)' % (KS, KS, Q0)


def _acc(var, dirn, to):
    t = 'eq %s %d' % (var, 4 if dirn == 'n' else 1)
    return '(or (%s) (eq %s TO))' % (t, var) if to == 'y' else '(%s)' % t


def src_prudent(dirn, fb, to, lenient=False):
    sim = SIMN if dirn == 'n' else SIMP
    probe = PROBEN if dirn == 'n' else PROBEP
    go = 1 if dirn == 'n' else 4
    other = 4 if dirn == 'n' else 1
    ex = 2 if dirn == 'n' else 5
    f = {'o': other, 'z': CT.NULL}[fb]
    bad = '(eq q %d)' % ex if lenient else '(or (eq q %d) (eq q TO))' % ex
    return '(lambda (me n p) (let ((r %s)) (if %s (let ((q %s)) (if %s %d %d)) %d)))' % (
        sim, _acc('r', dirn, to), probe, bad, f, go, f)


def src_opener(first, fb, to):
    g1 = 1 if first == 'n' else 4
    g2 = 4 if first == 'n' else 1
    f = {'f': g1, 'z': CT.NULL}[fb]
    # a = what next names (SIMN), b = what prev names (SIMP)
    va, vb = ('a', 'b') if first == 'n' else ('b', 'a')
    d1, d2 = ('n', 'p') if first == 'n' else ('p', 'n')
    dpart = '(if %s %d (if %s %d %d))' % (_acc(va, d1, to), g1, _acc(vb, d2, to), g2, f)
    return ('(lambda (me n p) (let ((a %s)) (let ((b %s)) (if (and (eq a 2) (eq b 3)) 4 (if (and (eq b 5) (eq a 0)) 1 %s)))))'
            % (SIMN, SIMP, dpart))


NAMES_P = ['P%s%s%s' % (d, fb, to) for d in 'np' for fb in 'oz' for to in 'yn']
NAMES_Q = ['Q%sz%s' % (d, to) for d in 'np' for to in 'yn']
NAMES_O = ['O%s%s%s' % (f, fb, to) for f in 'np' for fb in 'fz' for to in 'yn']
SRC_P = [src_prudent(n[1], n[2], n[3]) for n in NAMES_P]
SRC_Q = [src_prudent(n[1], n[2], n[3], True) for n in NAMES_Q]
SRC_O = [src_opener(n[1], n[2], n[3]) for n in NAMES_O]
NAMES_NEW = NAMES_P + NAMES_Q + NAMES_O
FAM_NEW = ['prudent'] * 8 + ['prudent_a'] * 4 + ['opener'] * 8
SRC_NEW = SRC_P + SRC_Q + SRC_O
NBR = TP.NPLUS + len(NAMES_NEW)           # 51

FAMB = ['c_third', 'c_half', 'c_two3', 'c_grand', 'single', 'two', 'exploit', 'bully', 'junk', 'prudent', 'prudent_a', 'opener']


def library_br():
    out = list(TP.library_plus())
    for n, f, s in zip(NAMES_NEW, FAM_NEW, SRC_NEW):
        out.append((n, f, s))
    return out


class CatalogueBR(TP.Catalogue):
    def __init__(self):
        lib = library_br()
        self.names = [x[0] for x in lib]
        self.fam = [x[1] for x in lib]
        self.terms = [CT._prog(x[2]) for x in lib]
        self.K = len(lib)
        self.idx = {n: i for i, n in enumerate(self.names)}


class TabsBR(TP.TabsPlus):
    """Execution tables of the 51 programs and the joint tables (as TabsPlus)."""

    def __init__(self, cache_dir=None):
        self.cat = CatalogueBR()
        self.names = self.cat.names
        self.fam = self.cat.fam
        self.K = self.cat.K
        key = hashlib.md5(('|'.join(self.names) + str(CT.KS) + str(CT.KR) + '|'.join(TP.SRC_EXTRA) + '|'.join(SRC_NEW) + 'br1').encode()).hexdigest()[:12]
        path = None
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)
            path = os.path.join(cache_dir, 'br_%s.npz' % key)
        if path and os.path.exists(path):
            z = np.load(path)
            self.code, self.steps, self.nto, self.fo = z['code'], z['steps'], z['nto'], z['fo']
        else:
            self.code, self.steps, self.nto, self.fo = L.run_big(self.cat.build_tables)
            if path:
                tmp = path + '.%d.tmp.npz' % os.getpid()
                np.savez(tmp, code=self.code, steps=self.steps, nto=self.nto, fo=self.fo)
                os.replace(tmp, path)
        self._joint()
