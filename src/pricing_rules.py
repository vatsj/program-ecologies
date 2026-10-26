"""What compute should cost: three pricing rules across three games (spec specs/2026-10-25-pricing-rules.md; notes
notes/pricing-rules.md; predictions predictions/2026-10-25-pricing-rules.md).

This module is the L_T part: an instrumented copy of the exact engine of src/lt_tape.py that records, for every leaf of
the decision tree of a play, the *forest of read calls* (simulations, proofs, enumerations, certificate checks) with their
steps, nesting, keys and time-outs.  The totals of the instrumented run equal Engine.dist exactly (a test).  From the
forest the rules of the spec are charges:

  F    c * S                                    every step
  A    P_fail * |T|                              each timed-out read call (root steps and finishing reads free)
  FA   c * (S - sum_{t in T*} s(t) + K |T*|)     every step, a topmost timed-out call charged c K in place of its subtree
  B    c * (root steps + own steps of the calls whose key is not cached); keys cached at first execution (island ledger)
  TOLL tau * (number of read calls)              a constant toll per read call (control)

T = timed-out calls, T* the topmost of them, s(t) the steps of call t including nested calls, K the root fuel cap.
A *call* = the RUN step, the steps executed while its frame is open, and the closing step (a primitive read: its charge).
Nothing under src/ is edited: this module subclasses lt_tape.Engine and copies the small-step loop it must instrument.
"""
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lt_tape as T
from lt_tape import (VALUE_TAGS, TO_, ACTIONS, EMPTY_STORE, initial, is_value, contract, decompose, plug, innermost_tid,
                     store_get, store_put, nat, POISON, INF)

RUN_, PROVE_, PRP_, CHK_ = 0, 1, 2, 3
KIND_NAMES = ('run', 'prove', 'prp', 'chk')


# ----------------------------------------------------------------------------------------------------------------
# decompose with the cause of a frame closing
# ----------------------------------------------------------------------------------------------------------------
def decompose_l(t):
    """lt_tape.decompose plus a 4th component: the cause when the step closes a simulation frame
    ('value' | 'fuel' | 'stuck'), else None."""
    ctx = []
    while True:
        tag = t[0]
        if tag in VALUE_TAGS: return ctx, 'value', t, None
        if tag == 'v': return ctx, 'stuck', None, None
        if tag == 'sim':
            k, tid, inner = t[1], t[2], t[3]
            if is_value(inner): return ctx, 'det', inner, 'value'
            if k <= 0: return ctx, 'det', TO_, 'fuel'
            ictx, ikind, ipay, icause = decompose_l(inner)
            if ikind == 'stuck': return ctx, 'det', TO_, 'stuck'
            ctx.append(('sim', k, tid))
            ctx.extend(ictx)
            return ctx, ikind, ipay, icause
        if tag == 'if':
            if not is_value(t[1]):
                ctx.append(('hole', t, 1)); t = t[1]; continue
            out = contract(t)
            if out is T.STUCK: return ctx, 'stuck', None, None
            if out is T.POISON_READ: return ctx, 'poison', None, None
            return ctx, 'det', out, None
        start = 2 if tag == 'mk' else 1
        for i in range(start, len(t)):
            if not is_value(t[i]):
                ctx.append(('hole', t, i)); t = t[i]; break
        else:
            if tag == 'pair': return ctx, 'value', t, None
            out = contract(t)
            if out is T.STUCK: return ctx, 'stuck', None, None
            if out is T.POISON_READ: return ctx, 'poison', None, None
            if out[0] in T.MARKERS:
                return ctx, 'redex', out, None
            return ctx, 'det', out, None
        continue


# ----------------------------------------------------------------------------------------------------------------
# the ledger state of one path through the tape tree
# ----------------------------------------------------------------------------------------------------------------
class Led:
    """Open frames [tid, cid, steps, prog] outermost first, closed calls (cid, parent, kind, keyid, steps, to, cause)."""
    __slots__ = ('frames', 'calls', 'ncall')

    def __init__(self):
        self.frames = []; self.calls = []; self.ncall = 0

    def copy(self):
        o = Led()
        o.frames = [list(f) for f in self.frames]
        o.calls = list(self.calls)
        o.ncall = self.ncall
        return o

    def add(self, n, upto=None):
        fr = self.frames if upto is None else self.frames[:upto]
        for f in fr: f[2] += n


class LedgerEngine(T.Engine):
    """lt_tape.Engine with instrumented evaluation.  `ledger(x, y)` returns a dict: dist (as Engine.dist), steps (expected),
    fuel (forfeit probability), leaves [(weight, outcome, S, calls)], with calls a tuple of
    (cid, parent, kind, keyid, steps, timed_out, cause) in order of start.  Key ids index self.keys."""

    def __init__(self, prover, K, r, m, enum_cap_default=400):
        super().__init__(prover, K, r, m, enum_cap_default)
        self.keys = {}; self.key_list = []
        self.lcache = {}
        self._cap_flag = False
        self.nstuck = 0

    def key(self, issuer, read):
        k = (issuer, read)
        i = self.keys.get(k)
        if i is None:
            i = len(self.key_list); self.keys[k] = i; self.key_list.append(k)
        return i

    def do_prp(self, b, xq, yq, a, k):
        self._cap_flag = False
        self.stats['prp'] += 1
        if self.in_enum: return False, 1
        self.in_enum += 1
        try:
            try:
                leaves = self.leaves_of(xq[1], yq, cap=b)
            except T.EnumCap:
                self._cap_flag = True
                return False, b
        finally:
            self.in_enum -= 1
        charge = 1 + sum(1 + u for (_, _, u) in leaves)
        p = sum((w for (w, o, _) in leaves if o == a), Fraction(0))
        return p >= Fraction(k, self.den), charge

    # -- the instrumented loop -------------------------------------------------------------------------------------
    def explore_l(self, t, store, used, w, emit, led, root):
        K = self.K
        th = self.th
        while True:
            ctx, kind, pay, cause = decompose_l(t)
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
                    led.calls.append((f[1], parent, RUN_, f[4], f[2], to, cause))
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
                led.frames.append([tid, cid, 1, pay[2][1], kid, parent])
                continue
            if tag == 'TAPE':
                i = pay[1]
                tid = innermost_tid(ctx)
                d = store_get(store, (tid, i))
                used += 1
                led.add(1, nopen)
                if d is not None:
                    t = plug(ctx, nat(d)); continue
                for d in range(self.r):
                    self.explore_l(plug(ctx, nat(d)), store_put(store, (tid, i), d), used, w / self.r, emit, led.copy(), root)
                return
            # multi-step primitives
            kcode = None
            capped = False
            if tag == 'PROVE':
                psi = th.from_fv(pay[2])
                q = self.prover.query(psi, pay[1])
                self.stats['prove'] += 1
                W = q['W'] if q['complete'] else INF
                res = T.T_ if q['found'] else T.F_
                cost = W; kcode = PROVE_
                rkey = ('prove', pay[1], pay[2])
            elif tag == 'HQ':
                cost = T.qnodes(pay[2]); res = nat(T.hash_value(pay[2], pay[1]))
            elif tag == 'PRP':
                ok, cost = self.do_prp(pay[1], pay[2], pay[3], pay[4], pay[5])
                capped = self._cap_flag
                res = T.T_ if ok else T.F_; kcode = PRP_
                rkey = ('prp', pay[1], pay[3], pay[4], pay[5])
            else:
                ok, cost = self.do_chk(pay[1], pay[2], pay[3], pay[4])
                res = T.T_ if ok else T.F_; kcode = CHK_
                rkey = ('chk', pay[2], pay[3], pay[4])
            G = K - used
            fuels = [fr[1] for fr in ctx if fr[0] == 'sim']
            counters = [G] + fuels
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
            # frame i0 - 1 (0-based among open frames) times out; its enclosing frames pay the same steps
            led.add(mv + 1, i0)
            f = led.frames[i0 - 1]
            parent = led.frames[i0 - 2][1] if i0 >= 2 else -1
            led.calls.append((f[1], parent, RUN_, f[4], f[2], True, 'cap'))
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
        acc = {}; leaves = []; steps = [Fraction(0)]; fuel = [Fraction(0)]

        def emit(w, out, used, led, reason):
            acc[out] = acc.get(out, Fraction(0)) + w
            steps[0] += w * used
            if reason in ('K', 'K-search'): fuel[0] += w
            calls = tuple(sorted(led.calls))
            leaves.append((w, out, used, calls, reason))

        self.explore_l(initial(x, y), EMPTY_STORE, 0, Fraction(1), emit, Led(), x)
        r = dict(dist=acc, steps=steps[0], fuel=fuel[0], leaves=leaves)
        self.lcache[key] = r
        return r


# ----------------------------------------------------------------------------------------------------------------
# per-leaf accounting under each rule
# ----------------------------------------------------------------------------------------------------------------
def leaf_stats(S, calls):
    """(n_to, n_top, steps_top, n_calls, top_level_steps) of one leaf's call forest.  calls: (cid, parent, kind, key,
    steps, to, cause) in cid order."""
    to = {c[0]: c[5] for c in calls}
    parent = {c[0]: c[1] for c in calls}
    n_to = sum(1 for c in calls if c[5])
    n_top = 0; steps_top = 0
    for c in calls:
        if not c[5]: continue
        p = c[1]; nested = False
        while p != -1:
            if to.get(p, False): nested = True; break
            p = parent.get(p, -1)
        if not nested:
            n_top += 1; steps_top += c[4]
    top_level = sum(c[4] for c in calls if c[1] == -1)
    return n_to, n_top, steps_top, len(calls), top_level


def charges_F(S): return S
def charges_FA(S, n_top, steps_top, K): return S - steps_top + K * n_top


def b_charge(S, calls, cached):
    """The B charge in steps of one leaf given the island's cache (a set of key ids), updated in place: the root's own
    steps plus the own steps of every call that is not under a cached call; every executed (uncached, not-under-cached)
    call inserts its key.  Returns the charge."""
    children = {}
    for c in calls:
        children.setdefault(c[1], []).append(c)
    top = sum(c[4] for c in children.get(-1, []))
    charge = S - top
    free = set()
    for c in calls:                                   # cid order: parents before children
        cid, parent, kind, kid, st, to, cause = c
        if parent in free:
            free.add(cid); continue
        if kid in cached:
            free.add(cid); continue
        own = st - sum(ch[4] for ch in children.get(cid, []))
        charge += own
        cached.add(kid)
    return charge


def pair_expectations(rec, K):
    """Expected per-play quantities of a ledger record: S, n_to, FA steps, n_calls, root_own (the warm-cache B charge),
    n_top, n_to_prp (prp cap events), plus the forfeit probability."""
    S = n_to = fa = ncall = rown = ntop = 0.0
    for (w, out, used, calls, reason) in rec['leaves']:
        w = float(w)
        nto, ntop_, stop, nc, toplv = leaf_stats(used, calls)
        S += w * used; n_to += w * nto; ncall += w * nc; ntop += w * ntop_
        fa += w * (used - stop + K * ntop_)
        rown += w * (used - toplv)
    return dict(S=S, n_to=n_to, fa=fa, ncall=ncall, root_own=rown, n_top=ntop, fuel=float(rec['fuel']))
