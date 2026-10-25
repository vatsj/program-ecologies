"""Arm T of the churn-in-the-primary-object experiment (spec specs/2026-10-25-churn-primary.md; notes/churn-primary.md
section 1.2.3 and 1.4): three-player majority division played by programs of L_T^code (src/lt_code.py, imported, not
edited) that read each other by capped simulation.

Frame.  A program is a closed term  lam me. lam n. lam p. body  and is run as  p(<p>)(<next>)(<prev>)  where next is
slot s+1 and prev slot s-1 (mod 3).  Its value is an action code 0-8 = 3*partner + demand, partner 0 = next, 1 = prev,
2 = ALL, demand 0, 1, 2 = 1/3, 1/2, 2/3, relative to the program's own slot.  Reading the next slot is
SIMN = capk k (run k n p) me; reading the previous slot is SIMP = capk k (run k p me) n.  A value that is not a
natural number 0-8, a root evaluation that runs out of fuel and a stuck term all play the timeout action (ALL, 2/3)
(code 8).  The joint table translates cyclic codes into the game's slot-relative action indices (a swap of the two
partner codes in slot 1) and reads the outcome from dollar3.

Frozen settings: simulation cap KS = 400 steps, root fuel KR = 1,200 steps.
"""
import os, sys, hashlib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lt_code as L

KS = 400
KR = 1200
COMP = L.SxCompiler()
SIMN = '(capk %d (run %d n p) me)' % (KS, KS)
SIMP = '(capk %d (run %d p me) n)' % (KS, KS)
C0_PRICE = 1.2e-4           # c0 = 0.12 / K0 with K0 = 10^3 (the dearest finishing encounter is 821 steps)
NULL = 8


def _prog(src):
    return COMP.expr(L.sx_parse(src)[0], [])


def _acc(dirn, to):
    t = 'eq r 4' if dirn == 'n' else 'eq r 1'
    return '(or (%s) (eq r TO))' % t if to == 'y' else '(%s)' % t


def src_const(a):
    return '(lambda (me n p) %d)' % a


def src_single(dirn, fb, to):
    """read one partner; accept -> name it at 1/2; else fallback o (the other slot at 1/2), z (null), q (the partner anyway)"""
    sim = SIMN if dirn == 'n' else SIMP
    go = 1 if dirn == 'n' else 4
    other = 4 if dirn == 'n' else 1
    f = {'o': other, 'z': NULL, 'q': go}[fb]
    return '(lambda (me n p) (let ((r %s)) (if %s %d %d)))' % (sim, _acc(dirn, to), go, f)


def src_two(first, fb, to):
    """read the first partner, then the second; fallback f (name the first at 1/2) or z (null)"""
    s1, s2 = (SIMN, SIMP) if first == 'n' else (SIMP, SIMN)
    d2 = 'p' if first == 'n' else 'n'
    g1 = 1 if first == 'n' else 4
    g2 = 4 if first == 'n' else 1
    f = {'f': g1, 'z': NULL}[fb]
    return '(lambda (me n p) (let ((r %s)) (if %s %d (let ((r %s)) (if %s %d %d)))))' % (
        s1, _acc(first, to), g1, s2, _acc(d2, to), g2, f)


def src_exploit(dirn):
    sim = SIMN if dirn == 'n' else SIMP
    if dirn == 'n':
        return '(lambda (me n p) (let ((r %s)) (if (eq r 3) 2 (if (eq r 4) 1 8))))' % sim
    return '(lambda (me n p) (let ((r %s)) (if (eq r 0) 5 (if (eq r 1) 4 8))))' % sim


FAMILY_WEIGHT = {  # dose -> family -> total weight (notes 1.4)
    'main': {'const': 0.900, 'single': 0.060, 'two': 0.030, 'exploit': 0.010},
    'lo': {'const': 0.900, 'single': 0.087, 'two': 0.003, 'exploit': 0.010},
    'hi': {'const': 0.830, 'single': 0.060, 'two': 0.100, 'exploit': 0.010},
}


def library():
    """list of (name, family, source).  The first 27 entries are the prior's library; the rest (family 'stub', weight
    zero) are the fallback-disabled twins used only by the probe."""
    out = []
    for a in range(9):
        out.append(('C%d' % a, 'const', src_const(a)))
    for dirn in 'np':
        for fb in 'oz':
            for to in 'yn':
                out.append(('S%s%s%s' % (dirn, fb, to), 'single', src_single(dirn, fb, to)))
    for first in 'np':
        for fb in 'fz':
            for to in 'yn':
                out.append(('D%s%s%s' % (first, fb, to), 'two', src_two(first, fb, to)))
    for dirn in 'np':
        out.append(('X%s' % dirn, 'exploit', src_exploit(dirn)))
    for dirn in 'np':
        for to in 'yn':
            out.append(('S%sq%s' % (dirn, to), 'stub', src_single(dirn, 'q', to)))
    return out


class TCat:
    """The arm-T catalogue: names, families, terms, the execution tables (action code and steps, per ordered triple
    (program, next, prev)) and the joint tables."""
    kind = 'lt'

    def __init__(self, cache_dir=None):
        lib = library()
        self.names = [x[0] for x in lib]
        self.fam = [x[1] for x in lib]
        self.terms = [_prog(x[2]) for x in lib]
        self.K = len(lib)
        self.idx = {n: i for i, n in enumerate(self.names)}
        self.is_reader = np.array([f in ('single', 'two', 'exploit', 'stub') for f in self.fam])
        self._tab = None
        self.cache_dir = cache_dir
        self._types = {}

    # ---- execution
    @staticmethod
    def init3(p, x, y):
        return ('app', ('app', ('app', p, ('quote', p)), ('quote', x)), ('quote', y))

    def f_eval(self, a, b, c):
        """cyclic action code (0-8, timeouts mapped to 8), steps, raw value of program a with next = b, prev = c."""
        v, st = L.evaluate(self.init3(self.terms[a], self.terms[b], self.terms[c]), KR)
        ok = isinstance(v, int) and not isinstance(v, bool) and 0 <= v <= 8
        return (int(v) if ok else NULL), int(st), v

    def _build(self):
        K = self.K
        code = np.empty((K, K, K), np.int8); steps = np.empty((K, K, K), np.int16)
        for p in range(K):
            if self.fam[p] == 'const':
                c, s, _ = self.f_eval(p, 0, 0)
                code[p] = c; steps[p] = s
                continue
            for n in range(K):
                for v in range(K):
                    c, s, _ = self.f_eval(p, n, v)
                    code[p, n, v] = c; steps[p, n, v] = s
        return code, steps

    def tables(self):
        if self._tab is not None:
            return self._tab
        key = hashlib.md5(('|'.join(self.names) + str(KS) + str(KR) + repr([t for t in self.terms])).encode()).hexdigest()[:12]
        path = None
        if self.cache_dir:
            path = os.path.join(self.cache_dir, 'tcat_%s.npz' % key)
            if os.path.exists(path):
                z = np.load(path)
                self._tab = (z['code'], z['steps'])
                return self._tab
        code, steps = L.run_big(self._build)
        if path:
            os.makedirs(self.cache_dir, exist_ok=True)
            np.savez(path, code=code, steps=steps)
        self._tab = (code, steps)
        return self._tab

    # ---- the joint tables
    def joint_codes(self):
        """JT[a, b, c] = dollar3 joint action code (a in slot 0, b in slot 1, c in slot 2) and ST[a, b, c, s] steps."""
        code, steps = self.tables()
        c0 = code.astype(np.int64)
        c1 = code.transpose(2, 0, 1).astype(np.int64)
        c2 = code.transpose(1, 2, 0).astype(np.int64)
        pi, d = c1 // 3, c1 % 3
        l1 = np.where(pi < 2, 3 * (1 - pi) + d, c1)
        JT = (c0 * 81 + l1 * 9 + c2).astype(np.int32)
        ST = np.stack([steps.astype(np.int32), steps.transpose(2, 0, 1).astype(np.int32),
                       steps.transpose(1, 2, 0).astype(np.int32)], axis=-1)
        return JT, ST

    def make_J(self, U, price, PAY, VEC):
        """J (padded local tables) and the payoff / outcome lookups: price 0 -> the standard code tables; price > 0 ->
        type ids (code, steps of the three programs) with PAYT = PAY - price * steps."""
        JT, ST = self.joint_codes()
        Kmax = max(len(u) for u in U)
        Up = [np.concatenate([u, np.full(Kmax - len(u), u[0])]).astype(np.int64) for u in U]
        ix = np.ix_(Up[0], Up[1], Up[2])
        J = JT[ix]
        if price == 0:
            return J.astype(np.int32), PAY, VEC
        Sx = ST[ix]
        key = (J.astype(np.int64) * 2048 + Sx[..., 0]) * 2048 + Sx[..., 1]
        key = key * 2048 + Sx[..., 2]
        uk, inv = np.unique(key.ravel(), return_inverse=True)
        s2 = (uk % 2048); s1 = (uk // 2048) % 2048; s0 = (uk // 2048 ** 2) % 2048; code = (uk // 2048 ** 3)
        PAYT = PAY[code].copy()
        PAYT[:, 0] -= price * s0; PAYT[:, 1] -= price * s1; PAYT[:, 2] -= price * s2
        VECT = VEC[code]
        return inv.reshape(J.shape).astype(np.int32), PAYT, VECT.astype(np.int64)

    # ---- priors
    def law(self, dose):
        w = np.zeros(self.K)
        if dose.startswith('ab'):
            # ablations (addendum 2): one reader family alone at weight 0.03, the rest constants
            pick = {'abS': [i for i, n in enumerate(self.names) if self.fam[i] == 'single' and n[2] == 'o'],
                    'abZ': [i for i, n in enumerate(self.names) if self.fam[i] == 'single' and n[2] == 'z'],
                    'abD': [i for i, f in enumerate(self.fam) if f == 'two']}[dose]
            cs = [i for i, f in enumerate(self.fam) if f == 'const']
            for i in cs:
                w[i] = 0.97 / len(cs)
            for i in pick:
                w[i] = 0.03 / len(pick)
            return w
        fw = FAMILY_WEIGHT[dose]
        for fam, tot in fw.items():
            ids = [i for i, f in enumerate(self.fam) if f == fam]
            for i in ids:
                w[i] = tot / len(ids)
        return w

    def label(self, x):
        return self.names[x]
