"""T+ : arm T's 27-program library plus Trojan bullies and junk programs written in L_T^code (queue 75, spec
specs/2026-11-08-length-prior-t.md).  Nothing existing is edited.

Programs 0-26 are churn_primary_t.library()[:27] (the prior's library), then
  27 Bn   Trojan bully reading the next slot:  if next names me at 1/3 (code 3) name it at 2/3 (code 2), else name prev at 1/2 (code 4)
  28 Bp   the same reading prev:               if prev names me at 1/3 (code 0) name it at 2/3 (code 5), else name next at 1/2 (code 1)
  29 Jf   junk, forfeit:                       returns 99 (not a code) -> plays 8 and is charged one forfeit
  30 Jr   junk, one failed read:               a read with cap 0 always fails (charged one failed read), then plays code 8
The bully is the DSL's Trojan bully ("if partner j names me at 1/3, name j at 2/3, else name k at 1/2",
majority_tail.dsl_family_data) in the arm-T frame, one program per direction (the cyclic frame identifies the two
non-self slots with next / prev).  The execution tables are built from lt_code with the A_f counters of
many_islands_t (failed reads = enter_sim frames closing on TO, forfeit = non-code root value).
"""
import os, sys, hashlib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lt_code as L
import churn_primary_t as CT

NLIB = 27
NAMES_EXTRA = ['Bn', 'Bp', 'Jf', 'Jr']
FAM_EXTRA = ['bully', 'bully', 'junk_f', 'junk_r']
NPLUS = NLIB + len(NAMES_EXTRA)          # 31 (the same length as the stored T catalogue with its four stubs)


def src_bully(dirn):
    if dirn == 'n':
        return '(lambda (me n p) (let ((r %s)) (if (eq r 3) 2 4)))' % CT.SIMN
    return '(lambda (me n p) (let ((r %s)) (if (eq r 0) 5 1)))' % CT.SIMP


SRC_EXTRA = [src_bully('n'), src_bully('p'), '(lambda (me n p) 99)',
             '(lambda (me n p) (let ((r (capk 0 (lambda (x) x) me))) 8))']


def library_plus():
    """[(name, family, source)] of the 31 programs of T+."""
    lib = CT.library()[:NLIB]
    out = list(lib)
    for n, f, s in zip(NAMES_EXTRA, FAM_EXTRA, SRC_EXTRA):
        out.append((n, f, s))
    return out


# ---- counting of failed reads (enter_sim frames closing on TO), installed once
_COUNT = [0]
_orig_enter_sim = L.enter_sim


def _counted_enter_sim(k, thunk, key=None):
    r = _orig_enter_sim(k, thunk, key)
    if isinstance(r, str) and r == 'TO':
        _COUNT[0] += 1
    return r


def install_counter():
    if L.enter_sim is not _counted_enter_sim:
        L.enter_sim = _counted_enter_sim


install_counter()


def init3(p, x, y):
    return ('app', ('app', ('app', p, ('quote', p)), ('quote', x)), ('quote', y))


def f_eval(prog, b, c, fuel=CT.KR):
    """root evaluation of the closed program term `prog` with next = b, prev = c: (code 0-8, steps, failed reads,
    forfeit, raw value)."""
    _COUNT[0] = 0
    v, st = L.evaluate(init3(prog, b, c), fuel)
    ok = isinstance(v, int) and not isinstance(v, bool) and 0 <= v <= 8
    return (int(v) if ok else CT.NULL), int(st), int(_COUNT[0]), (0 if ok else 1), v


class Catalogue:
    def __init__(self):
        lib = library_plus()
        self.names = [x[0] for x in lib]
        self.fam = [x[1] for x in lib]
        self.terms = [CT._prog(x[2]) for x in lib]
        self.K = len(lib)
        self.idx = {n: i for i, n in enumerate(self.names)}

    def build_tables(self):
        K = self.K
        code = np.empty((K, K, K), np.int8); steps = np.empty((K, K, K), np.int16)
        nto = np.empty((K, K, K), np.int8); fo = np.empty((K, K, K), np.int8)
        for p in range(K):
            if self.fam[p] in ('const', 'junk_f', 'junk_r'):
                c, s, n, f, _ = f_eval(self.terms[p], self.terms[0], self.terms[0])
                code[p] = c; steps[p] = s; nto[p] = n; fo[p] = f
                continue
            for n_ in range(K):
                for v_ in range(K):
                    c, s, n, f, _ = f_eval(self.terms[p], self.terms[n_], self.terms[v_])
                    code[p, n_, v_] = c; steps[p, n_, v_] = s; nto[p, n_, v_] = n; fo[p, n_, v_] = f
        return code, steps, nto, fo


class TabsPlus:
    """Execution tables of the 31 programs (code[p, n, v], steps, nto, fo for program p with next n, prev v) and the
    joint tables over triples (a in slot 0, b in slot 1, c in slot 2); the dollar3 translation is the one of
    many_islands_t.Tabs._joint."""

    def __init__(self, cache_dir=None):
        self.cat = Catalogue()
        self.names = self.cat.names
        self.fam = self.cat.fam
        self.K = self.cat.K
        key = hashlib.md5(('|'.join(self.names) + str(CT.KS) + str(CT.KR) + '|'.join(SRC_EXTRA) + 'tplus1').encode()).hexdigest()[:12]
        path = None
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)
            path = os.path.join(cache_dir, 'tplus_%s.npz' % key)
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

    def _joint(self):
        import many_islands as MI
        self.VEC, self.PAYD = MI.VEC, MI.PAY
        c0 = self.code.astype(np.int64)
        c1 = self.code.transpose(2, 0, 1).astype(np.int64)
        c2 = self.code.transpose(1, 2, 0).astype(np.int64)
        pi, d = c1 // 3, c1 % 3
        l1 = np.where(pi < 2, 3 * (1 - pi) + d, c1)
        self.JT = (c0 * 81 + l1 * 9 + c2).astype(np.int64)

        def st3(x):
            return np.stack([x.astype(np.int32), x.transpose(2, 0, 1).astype(np.int32),
                             x.transpose(1, 2, 0).astype(np.int32)], axis=-1)
        self.ST, self.NTO, self.FO = st3(self.steps), st3(self.nto), st3(self.fo)
        self.GROSS = self.PAYD[self.JT]

    def payoff(self, p_read, p_forf=None):
        if p_forf is None:
            p_forf = p_read
        return self.GROSS - p_read * self.NTO - p_forf * self.FO

    def charged_tables(self, pfail, T):
        """(J, PAY, VEC, ISMEM, TOT) at the A_f charge: J holds type ids of (outcome code, the three net payoffs)."""
        K = self.K
        net = self.payoff(pfail, pfail)
        key = np.concatenate([self.JT[..., None].astype(np.float64), np.round(net, 12)], axis=-1).reshape(-1, 4)
        uk, inv = np.unique(key, axis=0, return_inverse=True)
        PAY = uk[:, 1:4].copy()
        VEC = T.VEC[uk[:, 0].astype(np.int64)]
        J = inv.reshape(K, K, K).astype(np.int32)
        return J, PAY, VEC.astype(np.int64), T.ISMEM, T.TOT
