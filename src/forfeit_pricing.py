"""Charging forfeits like failed reads, exact (uncapped, shared-fuel) simulators, and the security fallback.

Spec specs/2026-10-26-forfeit-pricing.md (with the RS's addendum); hand derivations notes/forfeit-pricing.md section 1;
predictions predictions/2026-10-26-forfeit-pricing.md.  Imports the merged pricing and confirmation code and edits none of it.

Rules (notes 1.0): A (merged: P per capped read timeout; an uncapped read's failure is a forfeit and free), A_f (P per
distinct failure event: capped timeouts plus the forfeit, one charge for an uncapped read that exhausts the root), A_m (the
charge of A_f; a forfeit yields the forfeiter's security strategy instead of the game's forfeit outcome).

Arms (notes 1.2): 'none' (the merged catalogue), 'X' (exact simulators, half of the counterpart's template mass), 'sham' (the same
split, the second half a behaviourally identical capped simulator).

    python3 src/forfeit_pricing.py lt <game> <spec> [<spec> ...]       specs 'RULE[+X|+S]@LEVEL' (RULE in A, Af, Am), one process
    python3 src/forfeit_pricing.py pd <level> [--first 300 --runs 40]  one PD cell (rule A_f), one process

Fresh run indices only: L_T runs 300-339, PD reps 300-339.  LOTTERY objects at fixed geometry, never pi.
"""
import copy
import gzip
import json
import os
import pickle
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault('NUMBA_NUM_THREADS', '1')
import lt_tape as T
import lt_tape_games as G
import lt_tape_run as R
import rps as RP
import pricing_rules as P
import pricing_rules_lt as PL
from lt_tape import con, nat, L2, TP, EQ, IF, ME, THEM, TO_, plug, decompose, initial, EMPTY_STORE, store_get, store_put, nat as _nat
from lt_tape import innermost_tid, is_value, contract, VALUE_TAGS, ACTIONS, INF

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'runs', 'forfeit_pricing')
CACHE = os.path.join(OUT, '_cache')              # untracked numeric caches (never committed)
FRESH_LT = list(range(300, 340))
FRESH_PD = list(range(300, 340))
STORED_LT = list(range(0, 80)) + list(range(100, 140))
STORED_PD = list(range(0, 40)) + list(range(200, 240))
LEVELS = (0.03, 0.1, 0.3, 1.0, 10.0)
K0 = R.K0
RUN_, RUNX_ = P.RUN_, 4
UNC_MARGIN = 16                                  # a read whose fuel is within this of the root's whole fuel is uncapped
RESP_RPS = 11                                    # steps that cannot be spent on the read: 2 beta + RUN + close + let + 6 ladder
RESP_INSP = 9                                    # 2 beta + RUN + close + let + 4 ladder


# ----------------------------------------------------------------------------------------------------------------
# terms
# ----------------------------------------------------------------------------------------------------------------
OMEGA = ('app', ('lam', ('app', ('v', 0), ('v', 0))), ('lam', ('app', ('v', 0), ('v', 0))))   # loops until the root's fuel runs out


def _ladder_rps(v):
    return IF(EQ(v, con('R')), con('P'), IF(EQ(v, con('P')), con('S'), IF(EQ(v, con('S')), con('R'), OMEGA)))


def simx_rps(K, resp=RESP_RPS):
    """SIMX: play what beats the simulated action; no default (the failed read loops: a forfeit by running out)."""
    return L2(G.let(('run', nat(K - resp), THEM, ME), _ladder_rps(('v', 0))))


def simx_insp_I(K, resp=RESP_INSP):
    """SIMX_I: inspect iff the simulated inspectee cheats (K); comply (C) -> N; a failed read forfeits."""
    return L2(G.let(('run', nat(K - resp), THEM, ME), IF(EQ(('v', 0), con('K')), con('I'), IF(EQ(('v', 0), con('C')), con('N'), OMEGA))))


def simx_insp_E(K, resp=RESP_INSP):
    """SIMX_E: cheat iff the simulated inspector does not inspect: I -> C, N -> K; a failed read forfeits."""
    return L2(G.let(('run', nat(K - resp), THEM, ME), IF(EQ(('v', 0), con('I')), con('C'), IF(EQ(('v', 0), con('N')), con('K'), OMEGA))))


def _ubody():
    return IF(EQ(TP(0), nat(0)), con('R'), IF(EQ(TP(0), nat(1)), con('P'), con('S')))


def capped_clone_rps(k=101):
    """Behaviourally identical to SIM100u (same play law, same timeouts against the catalogue; fuel 101 instead of 100)."""
    return L2(G.let(('run', nat(k), THEM, ME), G.beat_case(('v', 0), _ubody())))


def capped_clone_I(k=101):
    return L2(IF(EQ(('run', nat(k), THEM, ME), con('K')), con('I'), con('N')))


def capped_clone_E(k=101):
    return L2(IF(EQ(('run', nat(k), THEM, ME), con('I')), con('C'), con('K')))


def build_check_originals(K):
    """The reconstructions of the capped counterparts equal the catalogue's terms at fuel 100 (asserted in the tests)."""
    return dict(rps=capped_clone_rps(100), I=capped_clone_I(100), E=capped_clone_E(100))


# counterpart name per game and role, exact twin name, sham twin name
TWINS = dict(rps=[(0, 'SIM100u', 'SIMX', 'SIM100u~')],
             insp=[(0, 'SI100n', 'SIMX_I', 'SI100n~'), (1, 'SE100k', 'SIMX_E', 'SE100k~')])


def _extend(game, cats, K):
    lists = [list(x) for x in cats]
    mk = {'SIMX': lambda v: simx_rps(K), 'SIMX_I': lambda v: simx_insp_I(K), 'SIMX_E': lambda v: simx_insp_E(K),
          'SIM100u~': lambda v: capped_clone_rps(), 'SI100n~': lambda v: capped_clone_I(), 'SE100k~': lambda v: capped_clone_E()}
    for (ro, cp, xn, sn) in TWINS[game]:
        for nm in (xn, sn):
            lists[ro].append(G.Template(nm, ro, 'sim', False, mk[nm], dict(twin_of=cp)))
    return lists


# ----------------------------------------------------------------------------------------------------------------
# the instrumented engine with uncapped reads
# ----------------------------------------------------------------------------------------------------------------
class LedX(P.Led):
    __slots__ = ('tape_unc',)

    def __init__(self):
        super().__init__()
        self.tape_unc = False

    def copy(self):
        o = LedX()
        o.frames = [list(f) for f in self.frames]
        o.calls = list(self.calls)
        o.ncall = self.ncall
        o.tape_unc = self.tape_unc
        return o


class LedgerEngineX(P.LedgerEngine):
    """pricing_rules.LedgerEngine with reads classified as capped or uncapped (fuel within UNC_MARGIN of the root's K) and a flag
    for a private-tape read inside an open uncapped frame.  A copy of the instrumented loop; nothing else differs."""

    def explore_l(self, t, store, used, w, emit, led, root):
        K = self.K
        th = self.th
        while True:
            ctx, kind, pay, cause = P.decompose_l(t)
            if kind == 'value':
                out = t[1] if (t[0] == 'con' and t[1] in ACTIONS) else 'BOT'
                emit(w, out, used, led, 'value' if out != 'BOT' else 'other-value'); return
            if kind == 'stuck':
                emit(w, 'BOT', used, led, 'stuck'); return
            if kind == 'poison':
                emit(w, 'POISON', used, led, 'poison'); return
            if used >= K:
                emit(w, 'BOT', used, led, 'K'); return
            tids = [fr[2] for fr in ctx if fr[0] == 'sim']
            nopen = len(tids)
            if kind == 'det':
                t = plug(ctx, pay); used += 1
                led.add(1, nopen)
                if len(led.frames) > nopen:                                  # a frame closes on this step
                    f = led.frames[nopen]
                    f[2] += 1
                    to = cause != 'value'
                    if cause == 'stuck': self.nstuck += 1
                    parent = led.frames[nopen - 1][1] if nopen > 0 else -1
                    led.calls.append((f[1], parent, RUNX_ if f[6] else RUN_, f[4], f[2], to, cause))
                    del led.frames[nopen:]
                continue
            tag = pay[0]
            if tag == 'RUN':
                ctr, digs = store
                tid = ctr + 1
                term = ('sim', pay[1], tid, ('app', ('app', pay[2][1], pay[2]), pay[3]))
                t = plug(ctx, term); used += 1; store = (tid, digs)
                led.add(1, nopen)
                issuer = led.frames[nopen - 1][3] if nopen > 0 else root
                kid = self.key(issuer, pay[2][1])
                parent = led.frames[nopen - 1][1] if nopen > 0 else -1
                cid = led.ncall; led.ncall += 1
                led.frames.append([tid, cid, 1, pay[2][1], kid, parent, pay[1] >= K - UNC_MARGIN])
                continue
            if tag == 'TAPE':
                i = pay[1]
                tid = innermost_tid(ctx)
                d = store_get(store, (tid, i))
                used += 1
                led.add(1, nopen)
                if any(f[6] for f in led.frames[:nopen]): led.tape_unc = True
                if d is not None:
                    t = plug(ctx, _nat(d)); continue
                for d in range(self.r):
                    self.explore_l(plug(ctx, _nat(d)), store_put(store, (tid, i), d), used, w / self.r, emit, led.copy(), root)
                return
            kcode = None
            capped = False
            if tag == 'PROVE':
                psi = th.from_fv(pay[2])
                q = self.prover.query(psi, pay[1])
                self.stats['prove'] += 1
                W = q['W'] if q['complete'] else INF
                res = T.T_ if q['found'] else T.F_
                cost = W; kcode = P.PROVE_
                rkey = ('prove', pay[1], pay[2])
            elif tag == 'HQ':
                cost = T.qnodes(pay[2]); res = _nat(T.hash_value(pay[2], pay[1]))
            elif tag == 'PRP':
                ok, cost = self.do_prp(pay[1], pay[2], pay[3], pay[4], pay[5])
                capped = self._cap_flag
                res = T.T_ if ok else T.F_; kcode = P.PRP_
                rkey = ('prp', pay[1], pay[3], pay[4], pay[5])
            else:
                ok, cost = self.do_chk(pay[1], pay[2], pay[3], pay[4])
                res = T.T_ if ok else T.F_; kcode = P.CHK_
                rkey = ('chk', pay[2], pay[3], pay[4])
            G_ = K - used
            fuels = [fr[1] for fr in ctx if fr[0] == 'sim']
            counters = [G_] + fuels
            exceeded = [i for i, v in enumerate(counters) if v < cost]
            if not exceeded:
                t = plug(ctx, res, dec=cost); used += cost
                led.add(cost, nopen)
                if kcode is not None:
                    issuer = led.frames[nopen - 1][3] if nopen > 0 else root
                    kid = self.key(issuer, rkey)
                    parent = led.frames[nopen - 1][1] if nopen > 0 else -1
                    cid = led.ncall; led.ncall += 1
                    led.calls.append((cid, parent, kcode, kid, cost, bool(capped), 'cap' if capped else None))
                continue
            mv = min(counters[i] for i in exceeded)
            i0 = min(i for i in exceeded if counters[i] == mv)
            if i0 == 0:
                emit(w, 'BOT', K, led, 'K-search'); return
            led.add(mv + 1, i0)
            f = led.frames[i0 - 1]
            parent = led.frames[i0 - 2][1] if i0 >= 2 else -1
            led.calls.append((f[1], parent, RUNX_ if f[6] else RUN_, f[4], f[2], True, 'cap'))
            del led.frames[i0 - 1:]
            nsim = 0; cut = None
            for j, fr in enumerate(ctx):
                if fr[0] == 'sim':
                    nsim += 1
                    if nsim == i0: cut = j; break
            t = plug(ctx[:cut], TO_, dec=mv + 1); used += mv + 1

    def ledger(self, x, y):
        key = (x, y)
        r = self.lcache.get(key)
        if r is not None: return r
        acc = {}; leaves = []; steps = [0]; fuel = [0]
        from fractions import Fraction
        steps = [Fraction(0)]; fuel = [Fraction(0)]

        def emit(w, out, used, led, reason):
            acc[out] = acc.get(out, Fraction(0)) + w
            steps[0] += w * used
            if reason in ('K', 'K-search'): fuel[0] += w
            leaves.append((w, out, used, tuple(sorted(led.calls)), reason, bool(led.tape_unc)))

        self.explore_l(initial(x, y), EMPTY_STORE, 0, Fraction(1), emit, LedX(), x)
        r = dict(dist=acc, steps=steps[0], fuel=fuel[0], leaves=leaves)
        self.lcache[key] = r
        return r


def leaf_events(calls, reason):
    """The failure events of one leaf (notes 1.0): (capped read timeouts, uncapped timeouts, forfeit 0/1, events under A,
    events under A_f/A_m).  An uncapped read that times out is the forfeit when the root forfeits (one charge) and is
    otherwise charged as a read timeout under every rule."""
    n_c = sum(1 for c in calls if c[5] and c[2] != RUNX_)
    n_u = sum(1 for c in calls if c[5] and c[2] == RUNX_)
    forf = 1 if reason in ('K', 'K-search') else 0
    surv = 0 if forf else n_u
    return n_c, n_u, forf, n_c + surv, n_c + forf + surv


def x_expectations(rec):
    """Per-pair expectations of a ledger record (x's own play): steps, capped timeouts, uncapped timeouts, forfeit probability,
    events under A and under A_f, calls, finished uncapped reads, tape reads inside an uncapped read, other-BOT probability."""
    out = dict(S=0.0, n_to=0.0, n_uto=0.0, forf=0.0, ev_A=0.0, ev_Af=0.0, ncall=0.0, unc_fin=0.0, unc_tape=0.0, bot_other=0.0)
    for (w, o, used, calls, reason, tape_unc) in rec['leaves']:
        w = float(w)
        n_c, n_u, forf, eA, eF = leaf_events(calls, reason)
        out['S'] += w * used; out['n_to'] += w * n_c; out['n_uto'] += w * n_u; out['forf'] += w * forf
        out['ev_A'] += w * eA; out['ev_Af'] += w * eF; out['ncall'] += w * len(calls)
        out['unc_fin'] += w * sum(1 for c in calls if c[2] == RUNX_ and not c[5])
        out['unc_tape'] += w * (1 if (tape_unc and any(c[2] == RUNX_ for c in calls)) else 0)
        if o == 'BOT' and not forf: out['bot_other'] += w
    return out


# ----------------------------------------------------------------------------------------------------------------
# tables with the exact simulators and their sham twins
# ----------------------------------------------------------------------------------------------------------------
ARR_KEYS = ('S', 'n_to', 'n_uto', 'forf', 'ev_A', 'ev_Af', 'ncall', 'unc_fin', 'unc_tape', 'bot_other')


class TablesX(R.Tables):
    """lt_tape_run.Tables of the full arm over the catalogue extended by the exact twins and the sham twins (appended, so the
    first n entries are the merged catalogue).  The numeric tables can be loaded from a cache; the catalogue is always rebuilt."""

    def __init__(self, game, K=K0):
        self.twin_game = game
        orig_r, orig_i = G.catalogue_rps, G.catalogue_insp
        G.catalogue_rps = lambda K_, m=3: _extend('rps', orig_r(K_, m), K_)
        G.catalogue_insp = lambda K_, m=3: _extend('insp', list(orig_i(K_, m)), K_)
        try:
            super().__init__(game, 'full', K, 0.0)
        finally:
            G.catalogue_rps, G.catalogue_insp = orig_r, orig_i


def _cache_path(game, K):
    return os.path.join(CACHE, 'base_%s_K%d.pkl' % (game, K))


class BaseX:
    """Numeric tables (action laws, steps, payoffs of the stored forfeit convention) and ledger arrays of the extended catalogue."""

    def __init__(self, game, K=K0, use_cache=True, check=True):
        self.game, self.K = game, K
        path = _cache_path(game, K)
        self.base_names = None
        if use_cache and os.path.exists(path):
            blob = pickle.load(open(path, 'rb'))
            self._build_shell(blob)
            return
        t0 = time.time()
        tb = TablesX(game, K)
        self.tb = tb
        r = tb.r
        eng = LedgerEngineX(tb.prover, K, r, 3)
        self.eng = eng
        recs = {}
        if game == 'rps':
            terms = tb.terms[0]
            self.arrays = self._arrays(eng, terms, terms)
            self.mismatch = self._check(eng, tb, terms, terms, both=False) if check else -1
            blob = dict(Gt=tb.Gt, S=tb.S, RT=tb.RT, FU=tb.FU, arrays=self.arrays, mismatch=self.mismatch)
        else:
            t0_, t1_ = tb.terms
            self.arr0 = self._arrays(eng, t0_, t1_)
            self.arr1 = self._arrays(eng, t1_, t0_)
            self.mismatch = self._check(eng, tb, t0_, t1_, both=True) if check else -1
            blob = dict(G0=tb.G0, G1=tb.G1, S0=tb.S0, S1=tb.S1, RT0=tb.RT0, RT1=tb.RT1, FU0=tb.FU0, FU1=tb.FU1,
                        arr0=self.arr0, arr1=self.arr1, mismatch=self.mismatch)
        blob['t_build'] = time.time() - t0
        self.t_build = blob['t_build']
        if use_cache:
            os.makedirs(CACHE, exist_ok=True)
            pickle.dump(blob, open(path + '.tmp', 'wb'))
            os.replace(path + '.tmp', path)
        self._fill(tb)

    def _build_shell(self, blob):
        """Rebuild the catalogue (cheap) and attach the cached numeric tables, without running the engine."""
        game, K = self.game, self.K
        tb = TablesX.__new__(TablesX)
        # run the cheap part of Tables.__init__ by calling it with a stub engine: replicate its catalogue steps
        orig_r, orig_i = G.catalogue_rps, G.catalogue_insp
        G.catalogue_rps = lambda K_, m=3: _extend('rps', orig_r(K_, m), K_)
        G.catalogue_insp = lambda K_, m=3: _extend('insp', list(orig_i(K_, m)), K_)
        try:
            r = 3 if game == 'rps' else 2
            tb.game, tb.arm, tb.K, tb.c, tb.renorm, tb.m = game, 'full', K, 0.0, False, 3
            tb.r = r
            tpls = G.catalogue_rps(K, 3) if game == 'rps' else list(G.catalogue_insp(K, 3))
        finally:
            G.catalogue_rps, G.catalogue_insp = orig_r, orig_i
        tb.tpls = tpls
        tb.names = [[t.name for t in lst] for lst in tpls]
        full_terms, _ = G.arm_terms(game, tpls, 'full')
        tb.sizes = [np.array([T.size(x) for x in lst]) for lst in full_terms]
        terms, keep = G.arm_terms(game, tpls, 'full', False)
        tb.terms = terms
        tb.keep = [np.array(k, bool) for k in keep]
        tb.disabled = [np.array([G.arm_disabled(game, 'full', t) for t in lst]) for lst in tpls]
        tb.fam = [np.array([('const' if tb.disabled[ro][i] else t.family) for i, t in enumerate(lst)]) for ro, lst in enumerate(tpls)]
        tb.engine_stats = {}; tb.n_searches = 0; tb.t_tables = 0.0
        if game == 'rps':
            tb.Gt, tb.S, tb.RT, tb.FU = blob['Gt'], blob['S'], blob['RT'], blob['FU']
            tb.Ug, tb.U = G.rps_payoffs(tb.Gt, tb.S, 0.0)
            self.arrays = blob['arrays']
        else:
            tb.G0, tb.G1, tb.S0, tb.S1, tb.RT0, tb.RT1, tb.FU0, tb.FU1 = (blob[k] for k in ('G0', 'G1', 'S0', 'S1', 'RT0', 'RT1', 'FU0', 'FU1'))
            tb.UAg, tb.UBg, tb.UA, tb.UB = G.insp_payoffs(tb.G0, tb.G1, tb.S0, tb.S1, 0.0)
            self.arr0, self.arr1 = blob['arr0'], blob['arr1']
        self.tb = tb
        self.mismatch = blob['mismatch']
        self.t_build = blob.get('t_build', float('nan'))
        self._fill(tb)

    def _fill(self, tb):
        n_base = {}
        for ro, lst in enumerate(tb.names):
            n_base[ro] = len([t for t in lst if not (t.endswith('~') or t.startswith('SIMX'))])
        self.n_base = n_base

    @staticmethod
    def _arrays(eng, xs, ys):
        nx, ny = len(xs), len(ys)
        out = {k: np.zeros((nx, ny)) for k in ARR_KEYS}
        for i, x in enumerate(xs):
            for j, y in enumerate(ys):
                ex = x_expectations(eng.ledger(x, y))
                for k in ARR_KEYS: out[k][i, j] = ex[k]
        return out

    @staticmethod
    def _check(eng, tb, xs, ys, both):
        """The instrumented totals reproduce the stored engine's distributions, steps and forfeit probabilities exactly."""
        bad = 0
        for i, x in enumerate(xs):
            for j, y in enumerate(ys):
                d = tb.engine.dist(x, y); l = eng.ledger(x, y)
                if d['dist'] != l['dist'] or d['steps'] != l['steps'] or d['fuel'] != l['fuel']: bad += 1
                if both:
                    d2 = tb.engine.dist(y, x); l2 = eng.ledger(y, x)
                    if d2['dist'] != l2['dist'] or d2['steps'] != l2['steps'] or d2['fuel'] != l2['fuel']: bad += 1
        return bad
