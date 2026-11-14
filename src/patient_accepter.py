"""Queue 78 (spec specs/2026-11-14-patient-accepters.md): the patient accepter R in arm T.

The catalogue is queue 76's (bully_resist.py: T+ , P, Q, O, F2; 55 programs) plus four patient accepters, appended last (K = 59):

  R<d><to>  reads partner d (d = n: the next slot, d = p: the previous slot) and treats the OTHER partner as its current one.
            If the read partner names me at 1/2, name it at 1/2; otherwise name the current partner at 1/3.
              Rnn / Rny:  (let ((r SIMN)) (if ACC 1 3))   reads next (acceptance: next names its prev = me at 1/2, code 4);
                          default code 3 = (prev, 1/3), on path the constant C3
              Rpn / Rpy:  (let ((r SIMP)) (if ACC 4 0))   reads prev (acceptance: prev names its next = me at 1/2, code 1);
                          default code 0 = (next, 1/3), on path the constant C0
            to = n: a timed-out read is no offer; to = y: a timed-out read counts as an offer (T's convention `to`).
            In a bully-held unequal island the victim's current partner is the bully and the read slot is the excluded one, so the
            matched orientation for a victim in slot v with the bully in slot v-1 (its prev) is Rn*, with the bully in v+1 it is Rp*.
            Under R1 the body is `(if (eq readn 4) 1 3)`: 6 nodes.

Nothing existing is edited.  The first 55 programs are exactly queue 76's (V2).
"""
import os, sys, hashlib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lt_code as L
import churn_primary_t as CT
import tplus as TP
import bully_resist as BR


def src_accepter(dirn, to):
    sim = CT.SIMN if dirn == 'n' else CT.SIMP
    go = 1 if dirn == 'n' else 4                 # name the read partner at 1/2
    dflt = 3 if dirn == 'n' else 0               # name the current (unread) partner at 1/3
    return '(lambda (me n p) (let ((r %s)) (if %s %d %d)))' % (sim, CT._acc(dirn, to), go, dflt)


NAMES_R = ['R%s%s' % (d, to) for d in 'np' for to in 'ny']          # Rnn, Rny, Rpn, Rpy
SRC_R = [src_accepter(n[1], n[2]) for n in NAMES_R]
FAM_R = ['accepter'] * 4
NPA = BR.NBR + len(NAMES_R)                                         # 59
DEFAULT_CONST = {'Rnn': 'C3', 'Rny': 'C3', 'Rpn': 'C0', 'Rpy': 'C0'}   # the 1/3 constant each R replaces on path
FAMP = BR.FAMB + ['accepter']


def library_pa():
    out = list(BR.library_br())
    for n, f, s in zip(NAMES_R, FAM_R, SRC_R):
        out.append((n, f, s))
    return out


class CataloguePA(TP.Catalogue):
    def __init__(self):
        lib = library_pa()
        self.names = [x[0] for x in lib]
        self.fam = [x[1] for x in lib]
        self.terms = [CT._prog(x[2]) for x in lib]
        self.K = len(lib)
        self.idx = {n: i for i, n in enumerate(self.names)}

    def build_rows(self, rows):
        """execution tables of the programs in `rows` against every (next, prev) of the catalogue."""
        K = self.K
        out = {}
        for p in rows:
            code = np.empty((K, K), np.int8); steps = np.empty((K, K), np.int16)
            nto = np.empty((K, K), np.int8); fo = np.empty((K, K), np.int8)
            if self.fam[p] in ('const', 'junk_f', 'junk_r'):
                c, s, n, f, _ = TP.f_eval(self.terms[p], self.terms[0], self.terms[0])
                code[:] = c; steps[:] = s; nto[:] = n; fo[:] = f
            else:
                for n_ in range(K):
                    for v_ in range(K):
                        c, s, n, f, _ = TP.f_eval(self.terms[p], self.terms[n_], self.terms[v_])
                        code[n_, v_] = c; steps[n_, v_] = s; nto[n_, v_] = n; fo[n_, v_] = f
            out[p] = (code, steps, nto, fo)
        return out


def _rows_job(rows):
    TP.install_counter()
    cat = CataloguePA()
    return L.run_big(cat.build_rows, rows)


def build_tables_parallel(workers=3):
    cat = CataloguePA()
    K = cat.K
    order = [p for p in range(K) if cat.fam[p] not in ('const', 'junk_f', 'junk_r')][::-1] + \
            [p for p in range(K) if cat.fam[p] in ('const', 'junk_f', 'junk_r')]
    chunks = [order[i::workers * 4] for i in range(workers * 4)]
    code = np.empty((K, K, K), np.int8); steps = np.empty((K, K, K), np.int16)
    nto = np.empty((K, K, K), np.int8); fo = np.empty((K, K, K), np.int8)
    if workers > 1:
        import multiprocessing as mp
        with mp.get_context('fork').Pool(workers) as pool:
            parts = pool.map(_rows_job, chunks, chunksize=1)
    else:
        parts = [_rows_job(c) for c in chunks]
    for d in parts:
        for p, (c, s, n, f) in d.items():
            code[p] = c; steps[p] = s; nto[p] = n; fo[p] = f
    return code, steps, nto, fo


class TabsPA(TP.TabsPlus):
    """Execution tables of the 59 programs and the joint tables (as TabsPlus)."""

    def __init__(self, cache_dir=None, workers=None):
        self.cat = CataloguePA()
        self.names = self.cat.names
        self.fam = self.cat.fam
        self.K = self.cat.K
        key = hashlib.md5(('|'.join(self.names) + str(CT.KS) + str(CT.KR) + '|'.join(TP.SRC_EXTRA) + '|'.join(BR.SRC_NEW)
                           + '|'.join(SRC_R) + 'pa1').encode()).hexdigest()[:12]
        path = None
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)
            path = os.path.join(cache_dir, 'pa_%s.npz' % key)
        if path and os.path.exists(path):
            z = np.load(path)
            self.code, self.steps, self.nto, self.fo = z['code'], z['steps'], z['nto'], z['fo']
        else:
            nw = workers or int(os.environ.get('DAYTONA_CPUS', min(3, os.cpu_count() or 1)))
            self.code, self.steps, self.nto, self.fo = build_tables_parallel(nw)
            if path:
                tmp = path + '.%d.tmp.npz' % os.getpid()
                np.savez(tmp, code=self.code, steps=self.steps, nto=self.nto, fo=self.fo)
                os.replace(tmp, path)
        self._joint()


def read_value(tabs_or_cat, me_term, dirn, b_term, c_term):
    """the raw value of the patient accepter's read (code, 'TO', or other) when the program `me_term` (whose quote is `me`) runs with
    next = b, prev = c: the read SIMN / SIMP evaluated inside the same frame as R itself."""
    sim = CT.SIMN if dirn == 'n' else CT.SIMP
    rd = CT._prog('(lambda (me n p) %s)' % sim)
    t = ('app', ('app', ('app', rd, ('quote', me_term)), ('quote', b_term)), ('quote', c_term))
    TP._COUNT[0] = 0
    v, st = L.evaluate(t, CT.KR)
    return v, int(st), int(TP._COUNT[0])
