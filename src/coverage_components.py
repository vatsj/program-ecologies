"""Coverage components: which part of the full certificate lists carries the fair wage's regrowth
(notes/coverage-components.md; spec specs/2026-10-15-coverage-components.md).

Imports the parents' machinery (`sog_full`, `sog_full_kern`, `sog_full_run`, `founding_legibility`,
`founding_legibility_kern`) unchanged and adds:
  * the static classification of every H-list script (notes §1.0 items 2-4): canon, (a) untravelled, (b) second paths,
    (c) identity-true, (d) gate copies, with the joint flags (S3-static, S-opp-static, identity-true, live,
    probe-reachable, set covered by the default root);
  * masks (notes §1.0 items 5-7): a granted and a barred set per (run tree, set) -- full, empty, minus, plus, pairs,
    count-matched complement controls, and mediation withholdings;
  * `MaskEvaluator` (production on top of the grant: a set is attempted until the program has produced a script for
    it; held and barred results write nothing) and `MaskRun` (founders hold the grant; lack bits and production rows by
    the mask's rule; the mark kernel when production runs);
  * the run's extra statistics (notes §1.0 item 8): trajectory, held scripts by class and provenance, regrowth nucleus,
    pivotal granted scripts, the timing log.
"""
import os
import sys
import json
import time
import itertools
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sog_full as F
import sog_full_kern as KN
import sog_full_run as R
import founding_legibility as FL
import founding_legibility_kern as FK

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'runs', 'coverage_components')
KI = 10 ** 12
LABELS = ('canon', 'a', 'b', 'c', 'd')
COMPS = ('a', 'b', 'c', 'd')


# ----------------------------------------------------------------------------------------------------------------
# 1. The static classification (notes §1.0 items 2-4)
# ----------------------------------------------------------------------------------------------------------------
def feasible_w(al):
    """A worker root is possible: the boss is not certified both =1/2 and <=1/4; the other worker is not certified both
    to strike and to work (soundness)."""
    if al.get(('B', F.A_EQ12)) and al.get(('B', F.A_LE14)): return False
    if al.get(('O', F.A_STRIKE)) and al.get(('O', F.A_WORK)): return False
    return True


def feasible_id_b(al):
    """A boss identity triple is possible: N1 and N2 together force EQW, and EQW with one of them forces the other."""
    n1, n2, ew = bool(al.get(F.N1, False)), bool(al.get(F.N2, False)), bool(al.get(F.EQW, False))
    if n1 and n2 and not ew: return False
    if ew and (n1 != n2): return False
    return True


def feasible_b(al):
    if not feasible_id_b(al): return False
    for j in (1, 2):
        for s in (0, 1):
            if al.get(('P', j, s, F.A_STRIKE)) and al.get(('P', j, s, F.A_WORK)): return False
            if al.get(('E', 'N%d' % j)) and al.get(('P', j, s, F.A_WORK)): return False
    return True


# The complement controls' inclusion probabilities (notes §1.x): per role and component X, min(1, V_X / P_X) with V_X
# the mean number of X scripts and P_X the mean number of non-canonical non-X scripts per founder of replicates 0-19
# (computed by coverage_components_run.control_q; a test re-derives them).
CONTROL_Q = {'W': {'a': 0.256033, 'b': 1.0, 'c': 0.013078, 'd': 0.203464},
             'B': {'a': 0.608903, 'b': 1.0, 'c': 0.002997, 'd': 0.0}}

PROBE_VIEWS = ({F.A_GE14: 'F', F.A_EQ12: 'F', F.A_LE14: 'T'},      # the boss view at a pay(0) probe root
               {F.A_GE14: 'T', F.A_EQ12: 'F', F.A_LE14: 'T'})      # at a pay(1/4) probe root


def _idv(al):
    return lambda nm: bool(al.get(('E', nm), False))


def _probe_reachable(t, A, s):
    for view in PROBE_VIEWS:
        for oS, oW, eq in itertools.product('TF', 'TF', (True, False)):
            if oS == 'T' and oW == 'T': continue
            bv = (lambda view, oS, oW: (lambda at: view[at[1]] if at[0] == 'B' else
                                        (oS if at[1] == F.A_STRIKE else oW)))(view, oS, oW)
            try:
                u, _ = F.sym_check(t, 'W', A, s, (lambda e: (lambda nm: e))(eq), bv)
            except Exception:
                u = None
            if u is not None: return True
    return False


_CLS = {}


def classify(g, role, tk):
    """{A: [row per H-list index]}; a row is a dict with the label and the joint flags (notes §1.0 item 4)."""
    key = (id(g), role, tk)
    r = _CLS.get(key)
    if r is not None: return r
    t = g.roles[role]['dts'][tk]
    _, per = g.hlist(role, tk)
    ats = F.dt_atoms(t)
    ids = [a for a in ats if a[0] == 'E']
    feas = feasible_w if role == 'W' else feasible_b
    out = {}
    for A in F.FAM[role]:
        H = per[A]
        gen = defaultdict(list)
        for bits in itertools.product([True, False], repeat=len(ats)):
            al = dict(zip(ats, bits))
            alpha = {a: v for a, v in al.items() if a[0] != 'E'}
            s, _ = F.sym_produce(t, role, A, alpha, _idv(al))
            if s is not None: gen[s].append(al)
        S3, Sopp = set(), set()
        for bits in itertools.product([True, False], repeat=len(ats)):
            al = dict(zip(ats, bits))
            bv = (lambda al: (lambda a: 'T' if al[a] else 'F'))(al)
            sc, _ = F.sym_prod3(t, role, A, _idv(al), bv)
            if sc is None: continue
            if role == 'W':
                Sopp.add(sc)
                if not al.get(F.EQ_W, False): S3.add(sc)
            else:
                if feasible_id_b(al):
                    S3.add(sc); Sopp.add(sc)
        sc0, _ = F.sym_prod3(t, role, A, lambda nm: False, lambda a: 'F')
        assert sc0 is None or sc0 in S3
        assert S3 <= set(H) and Sopp <= set(H)
        rows = []
        for i, s in enumerate(H):
            als = gen[s]
            r_ = dict(i=i, canon=(s == sc0), S3=(s in S3), Sopp=(s in Sopp),
                      idT=all(any(al[a] for a in ids) for al in als), live=any(feas(al) for al in als),
                      cov=(sc0 is not None))
            r_['probe'] = _probe_reachable(t, A, s) if role == 'W' else None
            r_['label'] = label(r_)
            rows.append(r_)
        out[A] = rows
    _CLS[key] = out
    return out


def label(r):
    """Priority (d) > (c) > {(a), (b)}; canon is the remainder (notes §1.0 item 4)."""
    if r['canon']: return 'canon'
    if (not r['S3']) and r['Sopp']: return 'd'
    if (not r['S3']) and r['idT']: return 'c'
    if not r['cov']: return 'a'
    return 'b'


def labels_of(g, role, tk):
    """Per set (family order): tuple of labels over the H list."""
    c = classify(g, role, tk)
    return tuple(tuple(r['label'] for r in c[A]) for A in F.FAM[role])


# ----------------------------------------------------------------------------------------------------------------
# 2. Masks (notes §1.0 items 5-7)
# ----------------------------------------------------------------------------------------------------------------
class Mask:
    """kind: 'full' | 'empty' | 'minus' | 'plus' | 'randplus' | 'randminus'.  comps: the component letters (for
    'plus' / 'minus' the union; for the random kinds the component whose count is matched).  withhold: a set of
    (role, tk, set index, script index) removed from the grant (mediation replays)."""

    def __init__(self, name, kind, comps=(), seed=0, withhold=()):
        self.name, self.kind, self.comps, self.seed = name, kind, tuple(comps), seed
        self.withhold = frozenset(withhold)
        self._c = {}
        self.g = None

    def bind(self, g):
        self.g = g
        return self

    def _rand(self, role, tk, labs):
        """The complement control's draw for run tree tk (notes §1.x, replacing §1.0 item 7's per-program stratum):
        of the n non-canonical scripts not in X, k = floor(q n) + Bernoulli(q n - floor(q n)) are taken uniformly
        without replacement, q = CONTROL_Q[role][X] the ratio of X's volume to the complement's volume per founder
        (replicates 0-19), capped at 1.  Returns a set of (si, idx)."""
        X = self.comps[0]
        q = CONTROL_Q[role][X]
        pool = [(si, i) for si, ls in enumerate(labs) for i, l in enumerate(ls) if l not in ('canon', X)]
        if q <= 0 or not pool: return set()
        rng = np.random.default_rng([self.seed, 1 if role == 'B' else 0, tk, 20261015])
        x = q * len(pool)
        k = int(np.floor(x)) + (1 if rng.random() < x - np.floor(x) else 0)
        pick = rng.choice(len(pool), size=min(k, len(pool)), replace=False)
        return set(pool[int(z)] for z in pick)

    def sets(self, role, tk):
        """(granted, barred): tuples over the family of frozensets of H-list indices."""
        key = (role, tk)
        r = self._c.get(key)
        if r is not None: return r
        labs = labels_of(self.g, role, tk)
        nfam = len(labs)
        G = [set() for _ in range(nfam)]; X = [set() for _ in range(nfam)]
        if self.kind == 'full':
            for si, ls in enumerate(labs): G[si] = set(range(len(ls)))
        elif self.kind == 'empty':
            pass
        elif self.kind == 'plus':
            for si, ls in enumerate(labs): G[si] = {i for i, l in enumerate(ls) if l in self.comps}
        elif self.kind == 'minus':
            for si, ls in enumerate(labs):
                X[si] = {i for i, l in enumerate(ls) if l in self.comps}
                G[si] = set(range(len(ls))) - X[si]
        elif self.kind in ('randplus', 'randminus'):
            d = self._rand(role, tk, labs)
            for si, ls in enumerate(labs):
                sel = {i for (s2, i) in d if s2 == si}
                if self.kind == 'randplus':
                    G[si] = sel
                else:
                    X[si] = sel; G[si] = set(range(len(ls))) - sel
        else:
            raise ValueError(self.kind)
        for (r_, t_, si, i) in self.withhold:
            if r_ == role and t_ == tk: G[si].discard(i)
        r = (tuple(frozenset(z) for z in G), tuple(frozenset(z) for z in X))
        self._c[key] = r
        return r

    def grant_inv(self, role, tk):
        G, _ = self.sets(role, tk)
        return tuple(tuple(sorted(z)) for z in G)

    def describe(self):
        return dict(name=self.name, kind=self.kind, comps=list(self.comps), seed=self.seed,
                    withhold=sorted(list(w) for w in self.withhold))


def mask_for(cell):
    """The mask of a cell name (notes §1.0 item 6)."""
    if cell == 'Hfull': return Mask(cell, 'full')
    if cell == 'S3': return Mask(cell, 'empty')
    if cell.startswith('minus_'): return Mask(cell, 'minus', cell[6:])
    if cell.startswith('plus_'): return Mask(cell, 'plus', cell[5:])
    if cell.startswith('rplus_'): return Mask(cell, 'randplus', cell[6:], seed=1000 + ord(cell[6]))
    if cell.startswith('rminus_'): return Mask(cell, 'randminus', cell[7:], seed=2000 + ord(cell[7]))
    raise ValueError(cell)


def production_on(mask):
    """Minus and full cells are pure grants (Lemma P) and run with production off (H mode)."""
    return mask.kind in ('empty', 'plus', 'randplus')


# ----------------------------------------------------------------------------------------------------------------
# 3. The evaluator and the run under a mask
# ----------------------------------------------------------------------------------------------------------------
class MaskEvaluator(F.Evaluator):
    """The parent's Evaluator with production on top of the grant (notes §1.0 item 5): a set is attempted iff the
    program holds no script for it outside the grant; a result already held ('held') or barred ('barred') writes
    nothing (index None for the kernel); a found script is added to the set's list (union, H order)."""

    def __init__(self, gram, arm, prod_mode, K, mask):
        super().__init__(gram, arm, prod_mode, K=K)
        self.mask = mask.bind(self.g)
        self.kinds = {}

    def lacking(self, pr):
        G, _ = self.mask.sets(pr.role, pr.tk)
        return [not (set(pr.inv[si]) - G[si]) for si in range(len(pr.inv))]

    def gc(self, pr):
        """Per set: a granted script is held (an attempt there is one the literal lack rule would suppress)."""
        G, _ = self.mask.sets(pr.role, pr.tk)
        return [bool(set(pr.inv[si]) & G[si]) for si in range(len(pr.inv))]

    def _outcome(self, pr, si, idx):
        if idx is None: return None, 'none'
        _, X = self.mask.sets(pr.role, pr.tk)
        if idx in pr.inv[si]: return None, 'held'
        if idx in X[si]: return None, 'barred'
        return idx, 'found'

    def prod_boss(self, b, code):
        b = self.canon(b)
        pi, ii = self.boss_reads(b)
        key = ('B', b, tuple(code[i] for i in pi), tuple(code[i] for i in ii))
        r = self._prod.get(key)
        if r is not None: return r
        pr = self.reg[b]
        t = self.g.roles['B']['dts'][pr.tk]
        idv = self.ae.idv_boss(code)
        vals = dict(zip(F.PROBE_ATOMS, code[:8]))
        ik = F.ident_key('B', t, idv)
        tab, dcl = self.cm.ft_table('B', pr.sp, 0, ik)
        dlist = (pr.dc[0] - dcl[0], pr.dc[2] - dcl[2])
        _, per = self.g.hlist('B', pr.tk)
        lack = self.lacking(pr)
        out = []; kinds = []
        for si, A in enumerate(F.BOSS_Q):
            if not lack[si]: continue
            log = []
            sc, calls = F.sym_prod3(t, 'B', A, idv, lambda at: vals[at], log)
            base, f = F.prod_features(log, tab, dlist, A, 'B')
            own = F.prod_steps('B', base, f, sc is not None)
            idx, kind = self._outcome(pr, si, per[A].index(sc) if sc is not None else None)
            out.append((si, idx, own, tuple(F.PROBE_ATOMS.index(a) for a, v in calls)))
            kinds.append(kind)
        self._prod[key] = out
        self.kinds[key] = kinds
        return out

    def prod_worker(self, x, j, bex, oex, rel):
        x = self.canon(x)
        key = ('W', x, j, bex, oex, rel)
        r = self._prod.get(key)
        if r is not None: return r
        pr = self.reg[x]
        t = self.g.roles['W']['dts'][pr.tk]
        eqv = rel and 'EQ' in self.live
        idv = lambda nm: eqv if nm == 'EQ' else False
        ik = F.ident_key('W', t, idv)
        tab, dcl = self.cm.ft_table('W', pr.sp, j, ik)
        dlist = (pr.dc[0] - dcl[0], pr.dc[2] - dcl[2])
        _, per = self.g.hlist('W', pr.tk)

        def bv(at):
            if at[0] == 'B': return bex[F.BOSS_Q.index(at[1])]
            return oex[0] if at[1] == F.A_WORK else oex[1]

        def cid(at):
            if at[0] == 'B': return F.BOSS_Q.index(at[1])
            return 3 if at[1] == F.A_WORK else 4
        lack = self.lacking(pr)
        out = []; kinds = []
        for si, A in enumerate(F.WORKER_Q):
            if not lack[si]: continue
            log = []
            sc, calls = F.sym_prod3(t, 'W', A, idv, bv, log)
            base, f = F.prod_features(log, tab, dlist, A, 'W')
            own = F.prod_steps('W', base, f, sc is not None)
            idx, kind = self._outcome(pr, si, per[A].index(sc) if sc is not None else None)
            out.append((si, idx, own, tuple(cid(a) for a, v in calls)))
            kinds.append(kind)
        self._prod[key] = out
        self.kinds[key] = kinds
        return out

    def productions(self, b, x, y, tr=None, gate=True):
        """The parent's S-nonself_3 after the play, with outcome kinds ('found', 'none', 'held', 'barred'; suffix '*'
        for an attempt at a grant-covered set)."""
        tr = tr or self.triple(b, x, y)
        out = []
        cb = self.canon(b)
        att = self.prod_boss(b, tr['code'])
        pi, ii = self.boss_reads(cb)
        kk = ('B', cb, tuple(tr['code'][i] for i in pi), tuple(tr['code'][i] for i in ii))
        nb, rec = self.produce(b, att, list(tr['pcost']), tr['steps'][0], kinds=self.kinds.get(kk))
        out.append((b, nb, rec))
        for jj, pid, oc, od in ((1, x, 2, 3), (2, y, 0, 1)):
            if tr['rel'] and gate:
                out.append((pid, pid, [('refused',)])); continue
            oex = (tr['wex'][oc], tr['wex'][od])
            att = self.prod_worker(pid, jj, tr['bex'], oex, bool(tr['rel']))
            kk = ('W', self.canon(pid), jj, tr['bex'], oex, bool(tr['rel']))
            cc = list(tr['bchg']) + [tr['wchg'][oc], tr['wchg'][od]]
            np_, rec = self.produce(pid, att, cc, tr['steps'][jj], kinds=self.kinds.get(kk))
            out.append((pid, np_, rec))
        return out

    def produce(self, pid, attempts, call_costs, play_steps, refused=False, kinds=None):
        pr = self.reg[pid]
        if refused:
            return pid, [('refused',)]
        gcs = self.gc(pr)
        rem = self.K - play_steps
        inv = [list(z) for z in pr.inv]
        rec = []
        for q, (si, idx, own, calls) in enumerate(attempts):
            sfx = '*' if gcs[si] else ''
            req = own + sum(call_costs[c] for c in calls)
            if rem <= 0:
                rec.append((si, 'fuelTO' + sfx, req, 0)); continue
            if req - F.PROD_W > self.P + F.VPLUS:
                charged = self.P + F.VPLUS + F.PROD_W
                if charged > rem:
                    rec.append((si, 'fuelTO' + sfx, req, rem)); rem = 0; continue
                rem -= charged
                rec.append((si, 'capTO' + sfx, req, charged)); continue
            if req > rem:
                rec.append((si, 'fuelTO' + sfx, req, rem)); rem = 0; continue
            rem -= req
            if idx is None:
                k = kinds[q] if kinds is not None else 'none'
                rec.append((si, k + sfx, req, req)); continue
            inv[si] = sorted(set(inv[si]) | {idx})
            rec.append((si, 'found' + sfx, req, req))
        newpid = self.reg.get(pr.role, pr.sp, tuple(tuple(z) for z in inv))
        return newpid, rec


class MaskRun(FL.FLRun):
    """The parent's Run (via FLRun, for the mark kernel) under a mask: founders hold the grant; lack bits and
    production rows by the mask's rule."""

    def __init__(self, ev, cfg, rep, mark=None):
        self.mask = ev.mask
        super().__init__(ev, cfg, rep, founder_seq=None, mark=mark)

    def founder_inv(self, role, sp):
        tk = int(self.ev.g.roles[role]['tau'][sp])
        return self.mask.grant_inv(role, tk)

    def lackbits(self, cpid):
        if not self.mode_S: return 0
        pr = self.ev.reg[cpid]
        return sum(1 << si for si, l in enumerate(self.ev.lacking(pr)) if l)

    def class_id(self, role, cpid):
        n0 = len(self.bcls)
        c = super().class_id(role, cpid)
        if role == 'B' and c >= n0:
            self.A['BLACK'][c] = self.lackbits(self.bcls[c])
        return c

    def register_wclass(self, c, cpid):
        super().register_wclass(c, cpid)
        self.A['WLACK'][c] = self.lackbits(cpid)

    def _newinv(self, pr, att, pat):
        inv = [set(z) for z in pr.inv]
        for a, (si, idx, own, calls) in enumerate(att):
            if (pat >> a) & 1 and idx is not None:
                inv[si].add(idx)
        return tuple(tuple(sorted(z)) for z in inv)

    def fill_pb(self, b, ri, code):
        ev = self.ev
        A = self.A
        cb = int(A['BCLS'][b])
        cpid = self.bcls[cb]
        att = ev.prod_boss(cpid, R.decode_code(code))
        r = self.newrow('pb')
        A['PB_N'][r] = len(att)
        pr = ev.reg[cpid]
        for a, (si, idx, own, calls) in enumerate(att):
            A['PB_IDX'][r, a] = -1 if idx is None else idx
            A['PB_OWN'][r, a] = own
            A['PB_MASK'][r, a] = sum(1 << c for c in set(calls))
        for pat in range(1 << len(att)):
            A['PB_NEW'][r, pat] = self.class_id('B', ev.canon(ev.reg.get('B', pr.sp, self._newinv(pr, att, pat))))
        A['PBI'][cb, ri] = r
        self.fills['pb'] += 1

    def fill_pw(self, x, j, bex, oex, rel):
        ev = self.ev
        A = self.A
        cx = int(A['WCLS'][x])
        cpid = self.wcls[cx]
        oexv = (R.VSTR[oex % 3], R.VSTR[oex // 3])
        att = ev.prod_worker(cpid, j, R.bexvals(bex), oexv, bool(rel))
        r = self.newrow('pw')
        A['PW_N'][r] = len(att)
        pr = ev.reg[cpid]
        for a, (si, idx, own, calls) in enumerate(att):
            A['PW_IDX'][r, a] = -1 if idx is None else idx
            A['PW_OWN'][r, a] = own
            A['PW_MASK'][r, a] = sum(1 << c for c in set(calls))
        for pat in range(1 << len(att)):
            A['PW_NEW'][r, pat] = self.class_id('W', ev.canon(ev.reg.get('W', pr.sp, self._newinv(pr, att, pat))))
        key = ((((cx * 2 + (j - 1)) * 27 + bex) * 9 + oex) * 2 + rel)
        self.PWD[key] = r
        self.fills['pw'] += 1


_EVC = {}


def evaluator(mask, mode, K=KI, arm='eq'):
    """One MaskEvaluator per (mask, mode, K) per process; switching masks drops the previous one and its tables."""
    key = (mask.name, mask.kind, mask.comps, mask.seed, mask.withhold, mode, K, arm)
    ev = _EVC.get(key)
    if ev is None:
        for k, old in list(_EVC.items()):
            for sk in [s for s in R._SHARED if s[0] == id(old)]:
                del R._SHARED[sk]
            del _EVC[k]
        R.load_costc()
        ev = MaskEvaluator(R.grammar(F.ARMS[arm][0]), arm, mode, K, mask)
        _EVC[key] = ev
    return ev


def make_run(mask, rep, N=100, I=64, mN=1.0, K=KI, mark=True, mode=None):
    """The run of a cell: mode 'S' (production on, with the mark if mark) or 'H' (a pure grant)."""
    mode = mode or ('S' if production_on(mask) else 'H')
    ev = evaluator(mask, mode, K)
    cfg = dict(name=mask.name, arm='eq', mode=mode, N=N, I=I, mN=mN, K=K)
    mk = FK.new_mark_state(1) if (mode == 'S' and mark) else None
    return MaskRun(ev, cfg, rep, mark=mk)


# ----------------------------------------------------------------------------------------------------------------
# 4. Statistics (notes §1.0 item 8)
# ----------------------------------------------------------------------------------------------------------------
TRAJ_GENS = (0, 10, 20, 200, 2000, 10000)


def held_stats(run, ci):
    """Per role: the share of individuals holding >= 1 script of each class, split granted / produced."""
    ev = run.ev
    g = ev.g
    out = {}
    for role, slots, tl in (('B', (0,), run.btypes), ('W', (1, 2), run.wtypes)):
        cnt = defaultdict(float); n = 0.0
        for i in range(run.I):
            for s in slots:
                t, c = R.snap_comp(run, ci, i, s)
                for tt, cc in zip(t, c):
                    pr = ev.reg[tl[int(tt)]]
                    labs = labels_of(g, role, pr.tk)
                    G, _ = ev.mask.sets(role, pr.tk)
                    has = set()
                    for si, idxs in enumerate(pr.inv):
                        for ix in idxs:
                            prov = 'granted' if ix in G[si] else 'produced'
                            has.add(labs[si][ix] + ':' + prov); has.add(labs[si][ix])
                    for h in has: cnt[h] += cc
                    n += cc
        out[role] = {k: v / n for k, v in sorted(cnt.items())}
    return out


def fair_triples(run, ev, ci, i):
    """Present triples of island i at check ci that play fair, with their count products (descending)."""
    tb, cb = R.snap_comp(run, ci, i, 0); t1, c1 = R.snap_comp(run, ci, i, 1); t2, c2 = R.snap_comp(run, ci, i, 2)
    rows = []
    for b, nb in zip(tb, cb):
        for x, nx in zip(t1, c1):
            for y, ny in zip(t2, c2):
                rows.append((int(nb * nx * ny), int(b), int(x), int(y)))
    rows.sort(reverse=True)
    out = []
    for w, b, x, y in rows[:400]:
        bp, xp, yp = run.btypes[b], run.wtypes[x], run.wtypes[y]
        if R.fair_play(ev.triple(bp, xp, yp)):
            out.append((w, bp, xp, yp))
            if len(out) >= 1: break
    return out


def _minus(ev, pid, si, idx):
    pr = ev.reg[pid]
    inv = tuple(tuple(z for z in idxs if not (q == si and z == idx)) for q, idxs in enumerate(pr.inv))
    return ev.reg.get(pr.role, pr.sp, inv)


def _set_empty(reg, pr, si):
    inv = tuple(() if q == si else idxs for q, idxs in enumerate(pr.inv))
    return reg.get(pr.role, pr.sp, inv)


def timing(ev, plain, trip, slot, si, idx):
    """The timing log (notes §1.0 item 8): would S_3 write script idx for set si of the member in `slot` at this
    encounter ('here'), at the same triple after every member's productions ('next'), or not ('never')?"""
    pids = [plain.reg.get(ev.reg[p].role, ev.reg[p].sp, ev.reg[p].inv) for p in trip]
    pids[slot] = _set_empty(plain.reg, plain.reg[pids[slot]], si)
    for step in ('here', 'next'):
        prods = plain.productions(*pids)
        recs = prods[slot][2]
        if recs and recs[0][0] == 'refused':
            return 'never (gate)' if step == 'here' else 'never'
        newp = prods[slot][1]
        if idx in plain.reg[newp].inv[si]:
            return 'pre-populated, ' + step
        pids = [p[1] for p in prods]
        if plain.reg[pids[slot]].inv[si]:
            return 'never'          # S_3 wrote another script for the set: the lack rule keeps idx out
    return 'never'


def regrowth(run, RS, plain, max_islands=3):
    """Regrowth analysis at the endpoint (notes §1.0 item 8)."""
    ev = run.ev
    g = ev.g
    nck = RS.nck
    fs = RS.fair.mean(axis=1)
    c20, c200 = 20 // R.CHECK_EVERY, min(200 // R.CHECK_EVERY, nck - 1)
    out = dict(final=float(fs[-1]), min_20_200=float(fs[c20:c200 + 1].min()),
               regrows=bool(fs[-1] >= 0.5 and fs[c20:c200 + 1].min() <= 0.1), nuclei=[])
    starts = []
    for i in range(run.I):
        f = RS.fair[:, i]
        if not f[-1]: continue
        nf = np.nonzero(~f)[0]
        st = int(nf[-1]) + 1 if len(nf) else 0
        if st * R.CHECK_EVERY >= 20:
            starts.append((st, i))
    starts.sort()
    out['n_regrown_islands'] = len(starts)
    for st, i in starts[:max_islands]:
        ft = fair_triples(run, ev, st, i)
        if not ft:
            out['nuclei'].append(dict(island=i, gen=st * R.CHECK_EVERY, note='no fair triple among the 400 most frequent'))
            continue
        w, bp, xp, yp = ft[0]
        trip = [bp, xp, yp]
        mem = []
        for s, p in enumerate(trip):
            pr = ev.reg[p]
            role = pr.role
            labs = labels_of(g, role, pr.tk)
            G, _ = ev.mask.sets(role, pr.tk)
            inv = []
            for si, idxs in enumerate(pr.inv):
                inv.append([[ix, labs[si][ix], 'granted' if ix in G[si] else 'produced'] for ix in idxs])
            hc = R.holder_class(run, ev, p, {}) if role == 'W' else None
            mem.append(dict(slot=s, spelling=F.show(g.roles[role]['spellings'][pr.sp]),
                            tree=F.show_dt(g.roles[role]['dts'][pr.tk]), holder=hc, inv=inv))
        piv = []
        for s, p in enumerate(trip):
            pr = ev.reg[p]
            labs = labels_of(g, pr.role, pr.tk)
            G, _ = ev.mask.sets(pr.role, pr.tk)
            for si, idxs in enumerate(pr.inv):
                for ix in idxs:
                    t2 = list(trip); t2[s] = _minus(ev, p, si, ix)
                    if not R.fair_play(ev.triple(*t2)):
                        granted = ix in G[si]
                        row = dict(slot=s, set=si, idx=ix, label=labs[si][ix],
                                   prov='granted' if granted else 'produced', tk=pr.tk, role=pr.role,
                                   S3=classify(g, pr.role, pr.tk)[F.FAM[pr.role][si]][ix]['S3'])
                        if granted:
                            row['timing'] = timing(ev, plain, trip, s, si, ix)
                        piv.append(row)
        out['nuclei'].append(dict(island=i, gen=st * R.CHECK_EVERY, weight=w, members=mem, pivotal=piv))
    return out


def prod_log(summ):
    """Outcome counts of the attempts on the population-sampled encounters of the parent's summary."""
    out = {}
    for gen, d in summ['encounters'].items():
        c = defaultdict(int)
        for row in d['rows']:
            for o in row[3]:
                c[o] += 1
        out[str(gen)] = dict(c)
    return out


def cell_job(args):
    """args = (cell, rep, extend[, withhold-json, tag]): one run, written to runs/coverage_components/cell_<cell>."""
    cell, rep, extend = args[:3]
    withhold = args[3] if len(args) > 3 else None
    tag = args[4] if len(args) > 4 else cell
    d = os.path.join(OUT, 'cell_' + tag)
    f = os.path.join(d, 'rep_%03d.json' % rep)
    if os.path.exists(f):
        return tag, rep, dict(skipped=0.0)
    R.load_costc()
    nomark = cell.endswith('_nomark')
    smode = cell.endswith('_Smode')          # a minus or full cell forced to run with production on (Lemma P check)
    base = cell[:-7] if nomark else (cell[:-6] if smode else cell)
    mask = mask_for(base)
    if nomark or smode:
        mask = Mask(cell, mask.kind, mask.comps, mask.seed)
    if withhold:
        mask = Mask(tag, mask.kind, mask.comps, mask.seed, withhold=[tuple(w) for w in withhold])
    t0 = time.time()
    run = make_run(mask, rep, mark=not nomark, mode='S' if smode else None)
    ev = run.ev
    run.prefill()
    t1 = time.time()
    run.run(R.HORIZON)
    t2 = time.time()
    sham = R.evaluator_k('sham', 'S', KI)
    summ, RS = R.summarize(run, ev_sham=sham, horizon=R.HORIZON)
    cc = dict(mask=mask.describe(), mode=run.cfg['mode'],
              held_2000=held_stats(run, RS.at_gen(R.HORIZON)), prod_log=prod_log(summ))
    t3 = time.time()
    out = dict(cell=tag, rep=rep, summary=summ, cc=cc, time=dict(setup=t1 - t0, run=t2 - t1, summary=t3 - t2))
    if extend:
        run.run(R.EXTEND)
        RS = R.RunStats(run)
        ci = RS.nck - 1
        end = dict(gen=ci * R.CHECK_EVERY, persistence=float(RS.fair[ci].mean()),
                   wage=[float((RS.wage[ci] == w).mean()) for w in range(3)], prodeff=float(RS.prodeff[ci].mean()),
                   strike_any=float(np.mean([(k // 4) % 4 != 0 for k in RS.play[ci]])))
        out['summary_ext'] = dict(end=end, fair_t=RS.fair.mean(axis=1)[::10].tolist(),
                                  wage_t=[[float((RS.wage[c] == w).mean()) for w in range(3)]
                                          for c in range(0, RS.nck, 10)],
                                  ctr=run.ctr.tolist(),
                                  fair_mask_end=int(sum(1 << i for i in range(run.I) if RS.fair[ci, i])))
        fs = RS.fair.mean(axis=1)
        cc['traj'] = {str(gg): float(fs[min(gg // R.CHECK_EVERY, ci)]) for gg in TRAJ_GENS}
        cc['held_10000'] = held_stats(run, ci)
        plain = R.evaluator_k('eq', 'S', KI)
        cc['regrowth'] = regrowth(run, RS, plain)
        if run.mark is not None:
            out['mark_ext'] = run.mark[1].tolist()
        out['time']['ext'] = time.time() - t3
    os.makedirs(d, exist_ok=True)
    tmp = f + '.tmp%d' % os.getpid()
    json.dump(out, open(tmp, 'w'), default=str)
    os.replace(tmp, f)
    ev.maybe_clear(0)
    return tag, rep, out['time']
