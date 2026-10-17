"""A per-root production rule for the fully realizable social organization game (notes/per-root.md; spec
specs/2026-10-16-per-root-production.md).

Imports the parents' machinery (`sog_full`, `sog_full_kern`, `sog_full_run`, `founding_legibility`,
`founding_legibility_kern`, `coverage_components`) unchanged and adds:
  * `sym_prod3_alt`: PROD3A, PROD3 that also writes the shadowed F-branch alternative of the first succeeding Hyp-first
    choice point (notes §1.0 item 6), with the parent's visit log for the cost model;
  * the rules R0, R0+alternatives, R1, R2, R3 (k bundles per set, CLOCK-LRU or FIFO) as an evaluator
    (`PREvaluator`): root validation with its charge, the attempt, the new class after use / production / eviction,
    the lackable bits, and a Python encounter path mirroring the kernel (for sampled encounters, traces and tests);
  * `PRRun`: the parent's Run on the generated kernel `per_root_kern` (lazy new-class table, list-free mark);
  * the run's statistics (notes §1.0 items 10-11) and the cell job.
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
import lt_cert as C
import coverage_components as CC
import per_root_kern as PK

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'runs', 'per_root')
KI, K3, K6 = 10 ** 12, 3 * 10 ** 6, 10 ** 6
DISPATCH_LOOKUP = 60          # root-keyed dispatch: a decision tree over the root's six values (notes §1.0 item 7)
ALT_CORR = {'W': 0.0}         # PROD3A's own-step correction per alternative attempt (set by the audit, notes §1.x)

RULES = {
    'R0': dict(perroot=False, alt=False, cap=None, evict=None),
    'R0alt': dict(perroot=False, alt=True, cap=None, evict=None),
    'R1': dict(perroot=True, alt=False, cap=None, evict=None),
    'R2': dict(perroot=True, alt=True, cap=None, evict=None),
    'R3k2': dict(perroot=True, alt=True, cap=2, evict='clock'),
    'R3k3': dict(perroot=True, alt=True, cap=3, evict='clock'),
    'R3k2f': dict(perroot=True, alt=True, cap=2, evict='fifo'),
    # labelled mechanism diagnostics (predictions addendum): one role under R2, the other under R0's lack rule
    'R2w': dict(perroot=True, alt=True, cap=None, evict=None, r0role='B'),
    'R2b': dict(perroot=True, alt=False, cap=None, evict=None, r0role='W'),
}


class Rule:
    def __init__(self, name, dispatch=False):
        d = RULES[name]
        self.name = name
        self.perroot, self.alt, self.cap, self.evict = d['perroot'], d['alt'], d['cap'], d['evict']
        self.usebits = self.cap is not None and self.evict == 'clock'
        self.dispatch = dispatch
        self.r0role = d.get('r0role')

    def key(self):
        return (self.name, self.dispatch)


# ----------------------------------------------------------------------------------------------------------------
# 1. PROD3A symbolically (notes §1.0 item 6)
# ----------------------------------------------------------------------------------------------------------------
def sym_prod3_alt(t, role, A, idv, boxval, log=None):
    """PROD3 with the shadowed alternative: (primary | None, alternative | None, calls).  The primary and its visit
    events are exactly sym_prod3's; at the first Hyp-first choice point whose Hyp branch closes, the F branch is also
    run (its events logged after an 'altbr' marker; it does not call the hypothesised box).  An enclosing ChkR takes
    its first subtree's alternative if any, else its second's; a choice point whose F branch fails passes on the
    alternative found inside its Hyp subtree."""
    Aset_ = set(A)
    calls = []

    def lg(*e):
        if log is not None: log.append(e)

    def ptac(al, Lf, Rf, c):
        if c > 63:
            lg('bound'); return None, c + 1, None
        c1 = c + 1
        if F.BOTS in Lf or F.TOPS in Rf or any(x in Rf and x[0] in ('pre', 'call', 'box') for x in Lf):
            lg('ax', Lf, Rf, len(al)); return C.node(C.AX, 0), c1, None
        for jj, b in enumerate(Rf):
            if b[0] == 'box' and al.get(b[1]) is True:
                lg('pos', Lf, Rf, len(al), jj)
                return C.node(C.HYP if F.hypable(role, b[1]) else C.RUN, jj), c1, None
        for jj, b in enumerate(Lf):
            if b[0] == 'box' and al.get(b[1]) is False:
                lg('neg', Lf, Rf, len(al), jj); return C.node(C.RUNNEG, jj), c1, None
        for jj, x in enumerate(Rf):
            if x[0] not in ('pre', 'call'): continue
            if x[0] == 'pre':
                s = F.sym_evstar(t, x[1], Aset_, idv)
                if log is not None:
                    pth = x[1]
                    while True:
                        y = F.node_at(t, pth)
                        if isinstance(y, tuple) and y[0][0] == 'E':
                            pth = pth + (idv(y[0][1]),); continue
                        break
                    lg('ev', Lf, Rf, len(al), jj, x[1], None if isinstance(y, tuple) else F.LEAFVAL.get(y, y))
                q, cc, a = ptac(al, Lf, C.fadd(s, C.fdel(x, Rf)), c1)
                if q is None: return None, cc, None
                return C.node(C.EVS, jj, q), cc, (None if a is None else C.node(C.EVS, jj, a))
            path = x[1]
            nd = F.node_at(t, path)
            B = ('box', nd[0])
            Rx = C.fdel(x, Rf)
            v = al.get(nd[0])
            lg('ck', Lf, Rf, len(al), jj, path, v is None, F.hypable(role, nd[0]))

            def branch(al2, cc):
                q1, cc1, a1 = ptac(al2, C.fadd(B, Lf), C.fadd(('pre', path + (True,)), Rx), cc)
                if q1 is None:
                    lg('br1fail'); return None, cc1, None
                q2, cc2, a2 = ptac(al2, Lf, C.fadd(B, C.fadd(('pre', path + (False,)), Rx)), cc1)
                if q2 is None:
                    lg('br2fail'); return None, cc2, None
                lg('brok')
                alt = None
                if a1 is not None: alt = C.node(C.CHKR, jj, a1, q2)
                elif a2 is not None: alt = C.node(C.CHKR, jj, q1, a2)
                return C.node(C.CHKR, jj, q1, q2), cc2, alt
            if v is None:
                if F.hypable(role, nd[0]):
                    al2 = dict(al); al2[nd[0]] = True
                    q, cc, a = branch(al2, c1)
                    if q is not None:
                        lg('altbr')
                        al3 = dict(al); al3[nd[0]] = False
                        qf, _, _ = branch(al3, c1)
                        return q, cc, (qf if qf is not None else a)
                    bv = boxval(nd[0]); calls.append((nd[0], bv))
                    lg('call', bv)
                    if bv == 'T':
                        lg('hypdead'); return None, c1, None
                    al2 = dict(al); al2[nd[0]] = False
                    lg('retry')
                    return branch(al2, c1)
                bv = boxval(nd[0]); calls.append((nd[0], bv))
                lg('call', bv)
                al2 = dict(al); al2[nd[0]] = (bv == 'T')
                return branch(al2, c1)
            return branch(al, c1)
        lg('noatom', Lf, Rf, len(al))
        return None, c1, None
    q, _, a = ptac({}, (), (('pre', ()),), 0)
    return q, a, calls


def split_log(log):
    """(events before the first 'altbr', the alternative branch's events): the primary's own log and the extra."""
    out, alt, inalt = [], [], False
    # the alternative's events are those logged between an 'altbr' marker and the return of that choice point; the
    # primary's events are the rest.  Since the F branch runs after the Hyp branch has closed and returns directly,
    # its events are exactly the events after 'altbr' up to the next event emitted by an enclosing frame.  For the
    # cost model both are visit events at the same per-event rates, so the split is reported, not used for charging.
    for e in log:
        if e[0] == 'altbr':
            inalt = True; continue
        (alt if inalt else out).append(e)
    return out, alt


# ----------------------------------------------------------------------------------------------------------------
# 2. Programs with bundle structure (R3) and the evaluator
# ----------------------------------------------------------------------------------------------------------------
class PRProg(F.Prog):
    __slots__ = ('aux',)


class PRRegistry(F.Registry):
    """The parent's registry with an optional bundle structure per program (R3): aux = per set, a tuple of
    (bundle length, use bit) in list order; None for uncapped rules."""

    def __init__(self, grammar, capped):
        super().__init__(grammar)
        self.capped = capped

    def get(self, role, sp, inv, aux=None):
        if self.capped:
            if aux is None:
                aux = tuple(tuple((1, 0) for _ in idx) for idx in inv)
        else:
            aux = None
        key = (role, sp, inv, aux)
        pid = self.index.get(key)
        if pid is None:
            pid = len(self.progs)
            p = PRProg(self.g, role, sp, inv, pid)
            p.aux = aux
            self.progs.append(p)
            self.index[key] = pid
        return pid


def bundle_of(aux_si, pos):
    """Index of the bundle holding flat position pos of a set's list."""
    s = 0
    for b, (ln, _) in enumerate(aux_si):
        if pos < s + ln: return b
        s += ln
    raise IndexError(pos)


class PREvaluator(F.Evaluator):
    """The parent's Evaluator under a production rule (notes §1.0 items 3-7)."""

    def __init__(self, gram, arm, K, rule):
        super().__init__(gram, arm, 'S', K=K)
        self.rule = rule
        self.reg = PRRegistry(gram, rule.cap is not None)
        if rule.dispatch:
            self.ae = DispatchAbsEval4(self.reg, self.cm, self.live)
        else:
            self.ae = F.AbsEval4(self.reg, self.cm, self.live)
        self._ctx = {}
        self._lk = {}
        self._new = {}
        self.ideal = K >= KI

    # ---- classes
    def canon(self, pid):
        c = self._canon.get(pid)
        if c is None:
            pr = self.reg[pid]
            r = self.g.roles[pr.role]
            if pr.isT1:
                c = pid
            else:
                ms = r['members'][pr.tk]
                csp = ms[0]
                if pr.role == 'W' and csp == self.g.t1_spelling:
                    csp = ms[1] if len(ms) > 1 else csp
                c = self.reg.get(pr.role, csp, pr.inv, pr.aux)
            self._canon[pid] = c
        return c

    # ---- validation at a root (notes §1.0 item 3)
    def validate(self, pr, t, role, A, idv, bv, cid, tab, dlist):
        """(val, own steps, call mask, flat position of the valid entry within the set's list): val -1 for an empty
        list, 1 valid, 0 invalid.  Linear checking (the parent's vone cost); dispatch charges the selected entry only."""
        ents = pr.entries
        if not any(A2 == A for A2, _ in ents):
            return -1, 0, 0, -1
        steps = 0; att = 0; used = None; scanned = len(ents); calls = set(); pos = -1
        per_entry = []
        for i, (A2, sc) in enumerate(ents):
            if A2 != A: continue
            att += 1
            r, cl, nodes_ = F.sym_check_trace(t, role, A, sc, idv, bv)
            st = sum(F.node_steps(t, role, A, rec, tab, dlist) for rec in nodes_)
            per_entry.append((st, set(cid(a) for a, v in cl)))
            steps += st
            calls |= per_entry[-1][1]
            if r is not None:
                used = r; scanned = i + 1; pos = att - 1
                break
        if self.rule.dispatch and used is not None:
            # dispatch reads the root's boxes (the calls the scan makes) and traverses the selected entry only
            st, cl = per_entry[-1]
            steps = st + F.vone_steps(role, pr.lc, 1, 1, True, len(ents)) + DISPATCH_LOOKUP
        else:
            steps += F.vone_steps(role, pr.lc, scanned, att, used is not None, len(ents))
        return (1 if used is not None else 0), int(steps), sum(1 << c for c in calls), pos

    def attempt(self, t, role, A, idv, bv, cid, tab, dlist, per):
        """(primary index | -1, alternative index | -1, own steps, call mask) of one PROD3 / PROD3A attempt."""
        log = []
        if self.rule.alt and role == 'W':
            sc, sa, calls = sym_prod3_alt(t, role, A, idv, bv, log)
        else:
            sc, calls = F.sym_prod3(t, role, A, idv, bv, log)
            sa = None
        base, f = F.prod_features(log, tab, dlist, A, role)
        own = F.prod_steps(role, base, f, sc is not None)
        if sa is not None:
            own += int(round(ALT_CORR.get(role, 0.0)))
        idx = per[A].index(sc) if sc is not None else -1
        ai = per[A].index(sa) if sa is not None else -1
        return idx, ai, own, sum(1 << c for c in set(cid(a) for a, v in calls))

    def worker_ctx(self, x, j, bex, oex, rel):
        """Per set (family order): (val, vown, vmask, vpos, idx, alt, own, mask) at the worker's root."""
        x = self.canon(x)
        key = ('W', x, j, bex, oex, rel)
        r = self._ctx.get(key)
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
        out = []
        for si, A in enumerate(F.WORKER_Q):
            out.append(self._set_ctx(pr, t, 'W', A, idv, bv, cid, tab, dlist, per))
        r = tuple(out)
        self._ctx[key] = r
        return r

    def boss_ctx(self, b, code):
        b = self.canon(b)
        pi, ii = self.boss_reads(b)
        key = ('B', b, tuple(code[i] for i in pi), tuple(code[i] for i in ii))
        r = self._ctx.get(key)
        if r is not None: return r
        pr = self.reg[b]
        t = self.g.roles['B']['dts'][pr.tk]
        idv = self.ae.idv_boss(code)
        vals = dict(zip(F.PROBE_ATOMS, code[:8]))
        ik = F.ident_key('B', t, idv)
        tab, dcl = self.cm.ft_table('B', pr.sp, 0, ik)
        dlist = (pr.dc[0] - dcl[0], pr.dc[2] - dcl[2])
        _, per = self.g.hlist('B', pr.tk)
        bv = lambda at: vals[at]
        cid = lambda at: F.PROBE_ATOMS.index(at)
        out = []
        for si, A in enumerate(F.BOSS_Q):
            out.append(self._set_ctx(pr, t, 'B', A, idv, bv, cid, tab, dlist, per))
        r = tuple(out)
        self._ctx[key] = r
        return r

    def _set_ctx(self, pr, t, role, A, idv, bv, cid, tab, dlist, per):
        rule = self.rule
        if rule.r0role == role:
            # this role keeps R0's lack rule: a held set is never attempted and costs nothing (read as valid, uncharged)
            has = any(A2 == A for A2, _ in pr.entries)
            if has:
                return (1, 0, 0, -1, -1, -1, 0, 0)
            idx, ai, own, mask = self.attempt(t, role, A, idv, bv, cid, tab, dlist, per)
            return (-1, 0, 0, -1, idx, ai, own, mask)
        if rule.perroot:
            val, vown, vmask, vpos = self.validate(pr, t, role, A, idv, bv, cid, tab, dlist)
        else:
            has = any(A2 == A for A2, _ in pr.entries)
            val, vown, vmask, vpos = (0 if has else -1), 0, 0, -1
        # the attempt is computed whenever it can run: every set under a per-root rule (a validation timeout makes a
        # valid set lacking, and the mark must only ever record a true NONE), the empty sets under R0's lack rule
        need = (val == -1) or rule.perroot
        if need:
            idx, ai, own, mask = self.attempt(t, role, A, idv, bv, cid, tab, dlist, per)
        else:
            idx, ai, own, mask = -1, -1, 0, 0
        return (val, vown, vmask, vpos, idx, ai, own, mask)

    # ---- the new program after an encounter's outcomes
    def apply(self, pid, ctx, states):
        """states per set: 0 nothing, 1 used (validated; CLOCK sets the bundle's bit), 2 produced (bundle appended,
        then eviction under a cap).  Returns the new pid (same class structure, the program's own spelling)."""
        rule = self.rule
        pr = self.reg[pid]
        key = (pid, ctx, tuple(states))
        r = self._new.get(key)
        if r is not None: return r
        inv = [list(z) for z in pr.inv]
        aux = [[list(b) for b in z] for z in pr.aux] if pr.aux is not None else None
        for si, s in enumerate(states):
            val, vown, vmask, vpos, idx, ai, own, mask = ctx[si]
            if s == 1:
                if rule.usebits and vpos >= 0:
                    b = bundle_of(aux[si], vpos)
                    aux[si][b][1] = 1
            elif s == 2:
                if idx < 0: continue
                bundle = ([ai] if (ai >= 0 and ai != idx) else []) + [idx]
                new = [z for z in bundle if z not in inv[si]]
                if not new: continue
                if not rule.perroot:
                    assert not inv[si]
                if rule.cap is not None and len(aux[si]) >= rule.cap:
                    if rule.evict == 'fifo':
                        victim = 0
                    else:
                        victim = None
                        for b in range(len(aux[si])):
                            if aux[si][b][1] == 0:
                                victim = b; break
                            aux[si][b][1] = 0
                        if victim is None: victim = 0
                    st = sum(aux[si][b][0] for b in range(victim))
                    del inv[si][st:st + aux[si][victim][0]]
                    del aux[si][victim]
                    new = [z for z in bundle if z not in inv[si]]
                inv[si] += new
                if aux is not None:
                    aux[si].append([len(new), 0])
        auxt = tuple(tuple(tuple(b) for b in z) for z in aux) if aux is not None else None
        r = self.reg.get(pr.role, pr.sp, tuple(tuple(z) for z in inv), auxt)
        self._new[key] = r
        return r

    # ---- lackable bits (notes §1.0 item 8)
    def lackable(self, cpid):
        """Bits of the sets a production at some root may attempt or (CLOCK) use: R0-type, the empty sets; per-root at
        the ideal table without use bits, the sets for which some root (box values T/F; identity values a producing
        root can have) leaves no entry valid or makes the scan call a box (a timed-out box then times the validation
        out); otherwise every set."""
        rule = self.rule
        pr = self.reg[cpid]
        n = len(F.FAM[pr.role])
        if not rule.perroot:
            return sum(1 << i for i, x in enumerate(pr.inv) if not x)
        if rule.usebits or not self.ideal:
            return (1 << n) - 1
        key = (pr.role, pr.tk, pr.inv)
        r = self._lk.get(key)
        if r is not None: return r
        t = self.g.roles[pr.role]['dts'][pr.tk]
        ats = [a for a in F.dt_atoms(t) if a[0] != 'E']
        if pr.role == 'W':
            idvs = [lambda nm: False]
        else:
            idvs = [(lambda d: (lambda nm: d.get(nm, False)))(dict(zip(('N1', 'N2', 'EQW'), c)))
                    for c in F.BOSS_ID_COMBOS]
        bits = 0
        for si, A in enumerate(F.FAM[pr.role]):
            ents = [sc for A2, sc in pr.entries if A2 == A]
            if not ents:
                bits |= 1 << si; continue
            lk = False
            for idv in idvs:
                for vb in itertools.product('TF', repeat=len(ats)):
                    val = dict(zip(ats, vb))
                    called = []

                    def bv(at):
                        called.append(at); return val[at]
                    ok = False
                    for sc in ents:
                        u, _ = F.sym_check(t, pr.role, A, sc, idv, bv)
                        if u is not None:
                            ok = True; break
                    if called or not ok:
                        lk = True; break
                if lk: break
            if lk: bits |= 1 << si
        self._lk[key] = bits
        return bits

    # ---- the Python encounter path (mirrors the kernel without the mark)
    def part(self, pid, ctx, call_costs, play_steps):
        """One participant's validation and attempts in its residual fuel: (new pid, records).  Records:
        ('val', si, outcome, req, charged) and ('prod', si, outcome, req, charged, alt written)."""
        rule = self.rule
        rem = self.K - play_steps
        V = self.K // 4
        recs = []
        states = [0] * len(ctx)
        lack = []
        stopped = False
        for si, (val, vown, vmask, vpos, idx, ai, own, mask) in enumerate(ctx):
            if val < 0:
                lack.append(si); continue
            if not rule.perroot: continue
            req = vown + sum(call_costs[c] for c in range(len(call_costs)) if (vmask >> c) & 1)
            if rem <= 0:
                recs.append(('val', si, 'valfuel', req, 0)); stopped = True; break
            if req > V + F.VPLUS:
                ch = V + F.TO_CHARGE
                if ch > rem:
                    recs.append(('val', si, 'valfuel', req, rem)); rem = 0; stopped = True; break
                rem -= ch
                recs.append(('val', si, 'valTO', req, ch)); lack.append(si); continue
            if req > rem:
                recs.append(('val', si, 'valfuel', req, rem)); rem = 0; stopped = True; break
            rem -= req
            if val == 1:
                recs.append(('val', si, 'valid', req, req))
                if rule.usebits: states[si] = 1
            else:
                recs.append(('val', si, 'invalid', req, req)); lack.append(si)
        if stopped: lack = []
        for si in lack:
            val, vown, vmask, vpos, idx, ai, own, mask = ctx[si]
            req = own + sum(call_costs[c] for c in range(len(call_costs)) if (mask >> c) & 1)
            if rem <= 0:
                recs.append(('prod', si, 'fuelTO', req, 0, False)); continue
            if req - F.PROD_W > self.P + F.VPLUS:
                ch = self.P + F.VPLUS + F.PROD_W
                if ch > rem:
                    recs.append(('prod', si, 'fuelTO', req, rem, False)); rem = 0; continue
                rem -= ch
                recs.append(('prod', si, 'capTO', req, ch, False)); continue
            if req > rem:
                recs.append(('prod', si, 'fuelTO', req, rem, False)); rem = 0; continue
            rem -= req
            if idx < 0:
                recs.append(('prod', si, 'none', req, req, False)); continue
            states[si] = 2
            recs.append(('prod', si, 'found', req, req, ai >= 0))
        newpid = self.apply(pid, ctx, tuple(states))
        for k, r in enumerate(recs):
            if r[0] == 'prod' and r[2] == 'found':
                if self.reg[newpid].inv[r[1]] == self.reg[pid].inv[r[1]] and newpid == pid:
                    recs[k] = r[:2] + ('dup',) + r[3:]
        return newpid, recs

    def productions(self, b, x, y, tr=None, gate=True):
        """The encounter's productions [(pid, new pid, records)]; R0 is the parent's S-nonself_3 exactly.  Records are
        flattened to the parent's (si, outcome, req, charged) for the parent's summary, validation included."""
        if self.rule.name == 'R0' and not self.rule.dispatch:
            return super().productions(b, x, y, tr, gate)
        out = []
        for pid, npid, recs in self.productions_full(b, x, y, tr, gate):
            if recs and recs[0] == ('refused',):
                out.append((pid, npid, recs)); continue
            out.append((pid, npid, [(r[1], r[2], r[3], r[4]) for r in recs]))
        return out

    def productions_full(self, b, x, y, tr=None, gate=True):
        tr = tr or self.triple(b, x, y)
        out = []
        ctx = self.boss_ctx(b, tr['code'])
        nb, rec = self.part(b, ctx, list(tr['pcost']), tr['steps'][0])
        out.append((b, nb, rec))
        for jj, pid, oc, od in ((1, x, 2, 3), (2, y, 0, 1)):
            if tr['rel'] and gate:
                out.append((pid, pid, [('refused',)])); continue
            oex = (tr['wex'][oc], tr['wex'][od])
            ctx = self.worker_ctx(pid, jj, tr['bex'], oex, bool(tr['rel']))
            cc = list(tr['bchg']) + [tr['wchg'][oc], tr['wchg'][od]]
            np_, rec = self.part(pid, ctx, cc, tr['steps'][jj])
            out.append((pid, np_, rec))
        return out


class DispatchAbsEval4(F.AbsEval4):
    """The checker with root-keyed dispatch (notes §1.0 item 7): the same values (the selected entry is the first
    valid one in list order), own steps charged as the selected entry alone plus the lookup when an entry is valid at
    the root, the linear scan otherwise; nested calls as the scan's (dispatch must read the root's boxes)."""

    def _vone(self, key):
        enc, j, A = key
        n = self.nvec(enc)
        pid, idv, slot = self.subject(key)
        pr = self.reg[pid]
        role = pr.role
        t = self.reg.g.roles[role]['dts'][pr.tk]
        ik = F.ident_key(role, t, idv)
        tkey = ('D', pid, slot, A, ik)
        VT_ = self.vtrie
        node = VT_.get(tkey)
        nested = []
        if node is not None:
            path_ok = True
            while node[0] == 'q':
                atom = node[1]
                bk = self.boxkey(key, atom)
                v = self.check(bk)
                nested.append(bk)
                nxt = node[2].get(v)
                if nxt is None:
                    path_ok = False; break
                node = nxt
            if path_ok:
                used, steps = node[1], node[2]
                res = None if used is None else [self.boxkey(key, a) for a in used]
                return res, self._vcost(key, n, steps, nested)
            nested = []
        tab, dcl = self.cm.ft_table(role, pr.sp, slot, ik)
        dlist = (pr.dc[0] - dcl[0], pr.dc[2] - dcl[2])
        seq = []

        def boxval(atom):
            bk = self.boxkey(key, atom)
            v = self.check(bk)
            nested.append(bk)
            seq.append((atom, v))
            return v
        steps = 0; att = 0; used = None; scanned = len(pr.entries)
        last_st = 0; last_nc = 0
        for i, (A2, sc) in enumerate(pr.entries):
            if A2 != A: continue
            att += 1
            n0 = len(nested)
            r, calls, nodes_ = F.sym_check_trace(t, role, A, sc, idv, boxval)
            st = sum(F.node_steps(t, role, A, rec, tab, dlist) for rec in nodes_)
            steps += st
            last_st = st; last_nc = len(nested) - n0
            if r is not None:
                used = list(r); scanned = i + 1
                break
        if used is not None:
            steps = last_st + F.vone_steps(role, pr.lc, 1, 1, True, len(pr.entries)) + DISPATCH_LOOKUP
            ncalls = last_nc
        else:
            steps += F.vone_steps(role, pr.lc, scanned, att, False, len(pr.entries))
            ncalls = None
        leaf = ('r', None if used is None else tuple(used), steps, ncalls)
        if not seq:
            VT_[tkey] = leaf
        else:
            root = VT_.get(tkey)
            if root is None or root[0] != 'q':
                root = ('q', seq[0][0], {})
                VT_[tkey] = root
            nd = root
            for q, (atom, v) in enumerate(seq):
                assert nd[1] == atom
                if q + 1 < len(seq):
                    nx = nd[2].get(v)
                    if nx is None:
                        nx = ('q', seq[q + 1][0], {})
                        nd[2][v] = nx
                    nd = nx
                else:
                    nd[2][v] = leaf
        res = None if used is None else [self.boxkey(key, a) for a in used]
        return res, self._vcost(key, n, steps, nested)


def build_vt_dispatch(ev, cpid, slot, A, eqval):
    """The parent's build_vt with dispatch charging: the trie's queries stay the linear scan's (dispatch reads the
    root's boxes, and the values do not change); the leaf's own steps are the selected entry's plus the lookup."""
    pr = ev.reg[cpid]
    t = ev.g.roles['W']['dts'][pr.tk]
    idv = lambda nm: eqval if nm == 'EQ' else False
    ik = F.ident_key('W', t, idv)
    tab, dcl = ev.cm.ft_table('W', pr.sp, slot, ik)
    dlist = (pr.dc[0] - dcl[0], pr.dc[2] - dcl[2])
    ats = [a for a in F.dt_atoms(t) if a[0] != 'E']
    root = None
    for bits in itertools.product((True, False), repeat=len(ats)):
        val = dict(zip(ats, bits))
        seq = []

        def boxval(atom):
            v = 'T' if val[atom] else 'F'
            seq.append((F.VT_ATOM[atom], 1 if val[atom] else 0))
            return v
        steps = 0; att = 0; used = None; scanned = len(pr.entries); last = 0
        for i, (A2, sc) in enumerate(pr.entries):
            if A2 != A: continue
            att += 1
            r, calls, nodes_ = F.sym_check_trace(t, 'W', A, sc, idv, boxval)
            st = sum(F.node_steps(t, 'W', A, rec, tab, dlist) for rec in nodes_)
            steps += st; last = st
            if r is not None:
                used = list(r); scanned = i + 1; break
        if used is not None:
            steps = last + F.vone_steps('W', pr.lc, 1, 1, True, len(pr.entries)) + DISPATCH_LOOKUP
        else:
            steps += F.vone_steps('W', pr.lc, scanned, att, False, len(pr.entries))
        leaf = ('r', used is not None, tuple(F.VT_ATOM[a] for a in (used or ())), steps)
        if not seq:
            if root is None: root = leaf
            continue
        if root is None: root = ('q', seq[0][0], {})
        nd = root
        for q, (a, v) in enumerate(seq):
            assert nd[0] == 'q' and nd[1] == a
            if q + 1 < len(seq):
                nx = nd[2].get(v)
                if nx is None:
                    nx = ('q', seq[q + 1][0], {}); nd[2][v] = nx
                nd = nx
            else:
                if v in nd[2]: assert nd[2][v] == leaf, (nd[2][v], leaf)
                nd[2][v] = leaf
    return root


# ----------------------------------------------------------------------------------------------------------------
# 3. The run on the generated kernel
# ----------------------------------------------------------------------------------------------------------------
QB_NAMES = ('QB_VAL', 'QB_VOWN', 'QB_VMASK', 'QB_IDX', 'QB_ALT', 'QB_OWN', 'QB_MASK')
QW_NAMES = ('QW_VAL', 'QW_VOWN', 'QW_VMASK', 'QW_IDX', 'QW_ALT', 'QW_OWN', 'QW_MASK')


class PRRun(R.Run):
    """The parent's Run under a rule, on per_root_kern.K3 (mark always present; mode 1 skips marked attempts)."""

    def __init__(self, ev, cfg, rep, mark_mode=1, stride=500, barred=None):
        self.st_ = PK.new_state(mark_mode, stride, logcap=60000)
        self.qrows = {'B': [], 'W': []}
        self.barred = barred or {}
        cfg = dict(cfg, share=False)
        super().__init__(ev, cfg, rep)
        A = self.A
        for nm in QB_NAMES + QW_NAMES:
            A.make(nm, (3,) if nm.startswith('QB') else (2,), np.int64, 4096, -1 if nm in ('QB_IDX', 'QB_ALT', 'QW_IDX', 'QW_ALT') else 0)
        A.make('QB_NEW', (27,), np.int64, 4096, -1)
        A.make('QW_NEW', (9,), np.int64, 4096, -1)
        self.nq = {'B': 0, 'W': 0}
        r = ev.rule
        self.RV = np.array([1 if r.perroot else 0, 1 if r.usebits else 0, F.TO_CHARGE], np.int64)

    # lackable bits
    def class_id(self, role, cpid):
        n0 = len(self.bcls)
        c = super().class_id(role, cpid)
        if role == 'B' and c >= n0:
            self.A['BLACK'][c] = self.ev.lackable(self.bcls[c]) if self.mode_S else 0
        return c

    def register_wclass(self, c, cpid):
        super().register_wclass(c, cpid)
        self.A['WLACK'][c] = self.ev.lackable(cpid) if self.mode_S else 0

    def fill_type(self, role, sp, c):
        cpid = (self.bcls if role == 'B' else self.wcls)[c]
        pr = self.ev.reg[cpid]
        self.type_id(role, self.ev.reg.get(role, sp, pr.inv, pr.aux))
        self.fills['type' + role] += 1

    def _newq(self, role):
        r = self.nq[role]; self.nq[role] = r + 1
        names = (QB_NAMES + ('QB_NEW',)) if role == 'B' else (QW_NAMES + ('QW_NEW',))
        for nm in names:
            self.A.ensure(nm, r + 1)
        return r

    def _bar(self, role, tk, ctx):
        """Mediation replays: barred (role, run tree) -> {(set, script)}: a barred primary or alternative is not
        written (the attempt still runs and is charged)."""
        bars = self.barred.get((role, tk))
        if not bars: return ctx
        out = []
        for si, c in enumerate(ctx):
            val, vown, vmask, vpos, idx, ai, own, mask = c
            if (si, ai) in bars: ai = -1
            if (si, idx) in bars: idx = -1; ai = -1
            out.append((val, vown, vmask, vpos, idx, ai, own, mask))
        return tuple(out)

    def _fillq(self, role, row, ctx, cls, cpid):
        A = self.A
        P_ = 'QB_' if role == 'B' else 'QW_'
        for a, (val, vown, vmask, vpos, idx, ai, own, mask) in enumerate(ctx):
            A[P_ + 'VAL'][row, a] = val; A[P_ + 'VOWN'][row, a] = vown; A[P_ + 'VMASK'][row, a] = vmask
            A[P_ + 'IDX'][row, a] = idx; A[P_ + 'ALT'][row, a] = ai; A[P_ + 'OWN'][row, a] = own
            A[P_ + 'MASK'][row, a] = mask
        A[P_ + 'NEW'][row, :] = -1
        A[P_ + 'NEW'][row, 0] = cls
        self.qrows[role].append((cpid, ctx))

    def fill_pb(self, b, ri, code):
        ev = self.ev
        cb = int(self.A['BCLS'][b])
        cpid = self.bcls[cb]
        ctx = self._bar('B', ev.reg[cpid].tk, ev.boss_ctx(cpid, R.decode_code(code)))
        row = self._newq('B')
        self._fillq('B', row, ctx, cb, cpid)
        self.A['PBI'][cb, ri] = row
        self.fills['pb'] += 1

    def fill_pw(self, x, j, bex, oex, rel):
        ev = self.ev
        cx = int(self.A['WCLS'][x])
        cpid = self.wcls[cx]
        oexv = (R.VSTR[oex % 3], R.VSTR[oex // 3])
        ctx = self._bar('W', ev.reg[cpid].tk, ev.worker_ctx(cpid, j, R.bexvals(bex), oexv, bool(rel)))
        row = self._newq('W')
        self._fillq('W', row, ctx, cx, cpid)
        key = ((((cx * 2 + (j - 1)) * 27 + bex) * 9 + oex) * 2 + rel)
        self.PWD[key] = row
        self.fills['pw'] += 1

    def fill_new(self, role01, row, code):
        role = 'B' if role01 == 0 else 'W'
        cpid, ctx = self.qrows[role][row]
        n = len(ctx)
        states = tuple((code // 3 ** a) % 3 for a in range(n))
        npid = self.ev.apply(cpid, ctx, states)
        c = self.class_id(role, self.ev.canon(npid))
        self.A['QB_NEW' if role == 'B' else 'QW_NEW'][row, code] = c
        self.fills['new' + role] += 1

    def fill_miss(self, m):
        kind = int(m[0])
        if kind == KN.MISS_PB:
            t0 = time.time(); self.fill_pb(int(m[1]), int(m[2]), int(m[3])); self.t_fill += time.time() - t0
        elif kind == KN.MISS_PW:
            t0 = time.time(); self.fill_pw(int(m[1]), int(m[2]), int(m[3]), int(m[4]), int(m[5]))
            self.t_fill += time.time() - t0
        elif kind == PK.MISS_NEW:
            t0 = time.time(); self.fill_new(int(m[1]), int(m[2]), int(m[3])); self.t_fill += time.time() - t0
        else:
            super().fill_miss(m)

    def batch_filled(self, key):
        k = key[0]
        A = self.A
        if k == PK.MISS_NEW:
            return A['QB_NEW' if key[1] == 0 else 'QW_NEW'][key[2], key[3]] >= 0
        return super().batch_filled(key)

    def PT(self):
        A = self.A
        MARK, MK, LOG, PC, SC = self.st_
        return super().PT() + (MARK, MK, LOG, PC, SC, self.RV) + tuple(A[nm] for nm in QB_NAMES + ('QB_NEW',)) \
            + tuple(A[nm] for nm in QW_NAMES + ('QW_NEW',))

    def run(self, gens):
        checks = np.arange(R.CHECK_EVERY, gens + 1, R.CHECK_EVERY, dtype=np.int64)
        nchk = len(checks)
        I, N = self.I, self.N
        if self.snap is None:
            self.snap = (np.zeros((nchk + 1, I, 3, N + 1), np.int32), np.zeros((nchk + 1, I, 3, N + 1), np.int32),
                         np.zeros((nchk + 1, I, 3), np.int32))
            st, sc, sn = self.snap
            for i in range(I):
                for s in range(3):
                    sn[0, i, s] = self.npres[i, s]
                    for t in range(self.npres[i, s]):
                        k = self.pres[i, s, t]; st[0, i, s, t] = k; sc[0, i, s, t] = self.counts[i, s, k]
        else:
            st, sc, sn = self.snap
            add = nchk + 1 - st.shape[0]
            if add > 0:
                self.snap = (np.concatenate([st, np.zeros((add,) + st.shape[1:], np.int32)]),
                             np.concatenate([sc, np.zeros((add,) + sc.shape[1:], np.int32)]),
                             np.concatenate([sn, np.zeros((add,) + sn.shape[1:], np.int32)]))
        self.checks = checks
        cfg = self.cfg
        m = cfg['mN'] / N
        r_enc = N / 3.0 * cfg.get("r_mult", 1.0)
        live_eq = 1 if 'EQ' in self.ev.live else 0
        t0 = time.time()
        while True:
            A = self.A
            stv, scv, snv = self.snap
            status = PK.K3.run_kernel(self.st, self.seed, I, N, 0.3, m, r_enc, self.checks, self.ev.K, self.ev.P,
                                      live_eq, self.mode_S, self.qmax, F.PROD_W,
                                      self.counts, self.pres, self.npres, self.pos, self.F, self.act, self.apos,
                                      self.quiet, self.nqlist, self.nqpos, self.T(), self.PT(), A['WACT'], A['TAG'],
                                      A['BLACK'], A['WLACK'], self.JQ, R.PAYF, self.ctr, self.miss, stv, scv, snv,
                                      self.maxiter, self.mbuf)
            if status == 0:
                break
            if status == 5:
                continue
            if status == 4:
                self.fill_batch()
                continue
            if status == 2:
                self.nmiss += 1
                self.fill_miss(self.miss.copy())
                continue
            raise RuntimeError('kernel status %d' % status)
        self.t_run += time.time() - t0
        return self


_EVC = {}


def evaluator(rule_name, K=KI, dispatch=False, arm='eq'):
    key = (rule_name, K, dispatch, arm)
    ev = _EVC.get(key)
    if ev is None:
        R.load_costc()
        ev = PREvaluator(R.grammar(F.ARMS[arm][0]), arm, K, Rule(rule_name, dispatch))
        _EVC[key] = ev
    return ev


def make_run(rule_name, rep, N=100, I=64, mN=1.0, K=KI, dispatch=False, mark_mode=1, barred=None):
    if dispatch:
        F.build_vt = build_vt_dispatch          # process-local: the dispatch variant's checker cost (notes §1.0 item 7)
    ev = evaluator(rule_name, K, dispatch)
    cfg = dict(name=rule_name, arm='eq', mode='S', N=N, I=I, mN=mN, K=K)
    return PRRun(ev, cfg, rep, mark_mode=mark_mode, barred=barred)


# ----------------------------------------------------------------------------------------------------------------
# 4. Statistics (notes §1.0 items 10-11)
# ----------------------------------------------------------------------------------------------------------------
TRAJ_GENS = (0, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000)
_S3S = {}


def s3_static(g, role, tk):
    """Per set: the H indices in S3^static (what PROD3 can write at some root; coverage_components.classify)."""
    key = (role, tk)
    r = _S3S.get(key)
    if r is None:
        cls = CC.classify(g, role, tk)
        r = tuple(frozenset(row['i'] for row in cls[A] if row['S3']) for A in F.FAM[role])
        _S3S[key] = r
    return r


def prov_class(g, role, tk, si, pos, idx):
    """'first' (position 0, primary-producible), 'perroot' (primary-producible, a later position), 'alt' (only
    PROD3A's alternative writes it) -- notes §1.0 item 10."""
    if idx not in s3_static(g, role, tk)[si]:
        return 'alt'
    return 'first' if pos == 0 else 'perroot'


def type_classes(ev, pid, cache):
    r = cache.get(pid)
    if r is None:
        pr = ev.reg[pid]
        r = set()
        for si, idxs in enumerate(pr.inv):
            for pos, ix in enumerate(idxs):
                r.add(prov_class(ev.g, pr.role, pr.tk, si, pos, ix))
        cache[pid] = r
    return r


def held_stats(run, ci, cache):
    """Per role: mean scripts per set (individual-weighted) and the share of individuals holding each class."""
    ev = run.ev
    out = {}
    for role, slots, tl in (('B', (0,), run.btypes), ('W', (1, 2), run.wtypes)):
        nset = len(F.FAM[role])
        tot = np.zeros(nset); n = 0.0
        cnt = defaultdict(float)
        for i in range(run.I):
            for s in slots:
                t, c = R.snap_comp(run, ci, i, s)
                for tt, cc in zip(t, c):
                    pid = tl[int(tt)]
                    pr = ev.reg[pid]
                    tot += np.array([len(z) for z in pr.inv]) * cc
                    n += cc
                    for k in type_classes(ev, pid, cache):
                        cnt[k] += cc
        out[role] = dict(scripts_per_set=(tot / max(n, 1)).round(4).tolist(),
                         holding={k: round(v / max(n, 1), 5) for k, v in sorted(cnt.items())})
    return out


def acquisition(run, RS, cache):
    """First check (generation) at which some individual holds a 'perroot' / 'alt' script, per role."""
    ev = run.ev
    first = {}
    for ci in range(RS.nck):
        for role, slots, tl in (('B', (0,), run.btypes), ('W', (1, 2), run.wtypes)):
            for i in range(run.I):
                for s in slots:
                    t, c = R.snap_comp(run, ci, i, s)
                    for tt in t:
                        for k in type_classes(ev, tl[int(tt)], cache):
                            if k in ('perroot', 'alt') and (role + ':' + k) not in first:
                                first[role + ':' + k] = ci * R.CHECK_EVERY
        if len(first) == 4: break
    return first


def fair_bosses(run, RS, gens):
    """Per listed generation: islands with a present boss type that pays 1/2 to the island's modal worker pair."""
    ev = run.ev
    out = {}
    for gg in gens:
        if gg > (RS.nck - 1) * R.CHECK_EVERY: continue
        ci = RS.at_gen(gg)
        n = 0
        for i in range(run.I):
            xt, yt = R.modal_type(run, ci, i, 1), R.modal_type(run, ci, i, 2)
            if xt < 0 or yt < 0: continue
            t, c = R.snap_comp(run, ci, i, 0)
            for tt in t:
                tr = ev.triple(run.btypes[int(tt)], run.wtypes[xt], run.wtypes[yt])
                if tr['boss'] // 3 == 2:
                    n += 1; break
        out[str(gg)] = n
    return out


def wage_states(RS, start_gen=20):
    """Island states per check (0 zero wage, 1 quarter, 2 half but not fair, 3 fair): occupancy over checks from
    start_gen, transition counts between consecutive checks, run-level losses and regrowths, first-fair times."""
    c0 = start_gen // R.CHECK_EVERY
    S = np.where(RS.fair, 3, RS.wage)
    occ = [float((S[c0:] == k).mean()) for k in range(4)]
    tr = np.zeros((4, 4), np.int64)
    for c in range(max(c0, 1), RS.nck):
        np.add.at(tr, (S[c - 1], S[c]), 1)
    fs = RS.fair.mean(axis=1)
    losses = regrowths = 0
    state = 'hi' if fs[c0] >= 0.5 else ('lo' if fs[c0] <= 0.1 else 'mid')
    for c in range(c0 + 1, RS.nck):
        if state != 'lo' and fs[c] <= 0.1:
            if state == 'hi': losses += 1
            state = 'lo'
        elif state != 'hi' and fs[c] >= 0.5:
            if state == 'lo': regrowths += 1
            state = 'hi'
    anyfair = np.nonzero(RS.fair[1:].any(axis=1))[0]
    after = [int(c) for c in np.nonzero(fs >= 0.5)[0] if c >= c0]
    return dict(occupancy=occ, transitions=tr.tolist(), losses=losses, regrowths=regrowths,
                first_fair_gen=int((anyfair[0] + 1) * R.CHECK_EVERY) if len(anyfair) else None,
                first_half_after20=after[0] * R.CHECK_EVERY if after else None,
                mean_0_end=float(fs.mean()), mean_2000_end=float(fs[RS.at_gen(2000):].mean()))


def _drop(ev, pid, si, ix):
    pr = ev.reg[pid]
    inv = tuple(tuple(z for z in idxs if not (q == si and z == ix)) for q, idxs in enumerate(pr.inv))
    return ev.reg.get(pr.role, pr.sp, inv)


def nuclei(run, RS, max_islands=3):
    """Regrowth (CC's definition): each nucleus's first fair encounter and its pivotal scripts (removing the script
    from every member of the triple that shares the holder's run tree and holds it makes the play unfair), with
    provenance class, CC label and list position."""
    ev = run.ev
    g = ev.g
    fs = RS.fair.mean(axis=1)
    c20, c200 = 20 // R.CHECK_EVERY, min(200 // R.CHECK_EVERY, RS.nck - 1)
    out = dict(final=float(fs[-1]), min_20_200=float(fs[c20:c200 + 1].min()),
               regrows=bool(fs[-1] >= 0.5 and fs[c20:c200 + 1].min() <= 0.1), nuclei=[])
    if not out['regrows']:
        return out
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
        ft = CC.fair_triples(run, ev, st, i)
        if not ft:
            out['nuclei'].append(dict(island=i, gen=st * R.CHECK_EVERY, note='no fair triple among the 400 most frequent'))
            continue
        w, bp, xp, yp = ft[0]
        trip = [bp, xp, yp]
        mem = []
        for s, p in enumerate(trip):
            pr = ev.reg[p]
            labs = CC.labels_of(g, pr.role, pr.tk)
            mem.append(dict(slot=s, spelling=F.show(g.roles[pr.role]['spellings'][pr.sp]),
                            tree=F.show_dt(g.roles[pr.role]['dts'][pr.tk]),
                            holder=R.holder_class(run, ev, p, {}) if pr.role == 'W' else None,
                            inv=[[[ix, labs[si][ix], prov_class(g, pr.role, pr.tk, si, pos, ix)]
                                  for pos, ix in enumerate(idxs)] for si, idxs in enumerate(pr.inv)]))
        piv = []
        for s, p in enumerate(trip):
            pr = ev.reg[p]
            labs = CC.labels_of(g, pr.role, pr.tk)
            for si, idxs in enumerate(pr.inv):
                for pos, ix in enumerate(idxs):
                    t2 = list(trip)
                    for s2 in range(3):
                        q = ev.reg[trip[s2]]
                        if q.role == pr.role and q.tk == pr.tk and ix in q.inv[si]:
                            t2[s2] = _drop(ev, trip[s2], si, ix)
                    if not R.fair_play(ev.triple(*t2)):
                        piv.append(dict(slot=s, set=si, idx=ix, pos=pos, label=labs[si][ix],
                                        prov=prov_class(g, pr.role, pr.tk, si, pos, ix), role=pr.role, tk=int(pr.tk)))
        out['nuclei'].append(dict(island=i, gen=st * R.CHECK_EVERY, weight=w, members=mem, pivotal=piv))
    return out


def cost_log(run):
    """Quantiles of the encounter cost relative to play from the kernel's stride sample (notes §1.0 item 10)."""
    MARK, MK, LOG, PC, SC = run.st_
    n = int(MK[4])
    if n == 0:
        return dict(n=0)
    L = LOG[:n].astype(float)
    gen = L[:, 0] / (3.0 * run.I * run.N)
    play = L[:, 1:4].sum(1); val = L[:, 4:7].sum(1); prod = L[:, 7:10].sum(1)
    out = dict(n=n)
    for tag, m in (('all', np.ones(n, bool)), ('after50', gen >= 50), ('before50', gen < 50)):
        if m.sum() == 0: continue
        r = (play[m] + val[m] + prod[m]) / np.maximum(play[m], 1)
        out[tag] = dict(n=int(m.sum()), median=float(np.median(r)), p90=float(np.percentile(r, 90)),
                        p99=float(np.percentile(r, 99)), mean=float(r.mean()),
                        cumulative=float((play[m] + val[m] + prod[m]).sum() / max(play[m].sum(), 1)),
                        val_share_nonplay=float(val[m].sum() / max((val[m] + prod[m]).sum(), 1)),
                        play_median=float(np.median(play[m])), max_gen=float(gen[m].max()))
    return out


PC_NAMES = ('valid', 'invalid', 'valTO', 'valfuel', 'attempts', 'found', 'none', 'capTO', 'fuelTO', 'marked',
            'marked_steps', 'val_steps', 'prod_steps', 'found_alt', 'class_changes', 'examined')


def kernel_counters(run):
    MARK, MK, LOG, PC, SC = run.st_
    return dict(boss={k: int(PC[q]) for q, k in enumerate(PC_NAMES)},
                worker={k: int(PC[32 + q]) for q, k in enumerate(PC_NAMES)},
                mark=dict(skipped=int(MK[5]), skipped_steps=int(MK[6]), sensitive=int(MK[7]), bound=int(MK[8]),
                          recorded=int(MK[9]), examined=int(MK[10])),
                executed_encounters=int(run.ctr[0]), log_rows=int(MK[4]))


def prod_log(summ):
    out = {}
    for gen, d in summ['encounters'].items():
        c = defaultdict(int)
        for row in d['rows']:
            for o in row[3]:
                c[o] += 1
        out[str(gen)] = dict(c)
    return out


# ----------------------------------------------------------------------------------------------------------------
# 5. The cell job
# ----------------------------------------------------------------------------------------------------------------
CELLS = {
    # ideal table
    'R0_i': dict(rule='R0', K=KI), 'R0alt_i': dict(rule='R0alt', K=KI), 'R1_i': dict(rule='R1', K=KI),
    'R2_i': dict(rule='R2', K=KI), 'R3k2_i': dict(rule='R3k2', K=KI), 'R3k3_i': dict(rule='R3k3', K=KI),
    'R3k2f_i': dict(rule='R3k2f', K=KI),
    # executed
    'R0_3': dict(rule='R0', K=K3), 'R2_3': dict(rule='R2', K=K3), 'R2d_3': dict(rule='R2', K=K3, dispatch=True),
    'R0_6': dict(rule='R0', K=K6), 'R2_6': dict(rule='R2', K=K6),
    'R3k2_3': dict(rule='R3k2', K=K3), 'R3k2_6': dict(rule='R3k2', K=K6),
    'R3k3_3': dict(rule='R3k3', K=K3), 'R3k3_6': dict(rule='R3k3', K=K6),
    'R3k2f_3': dict(rule='R3k2f', K=K3), 'R3k2f_6': dict(rule='R3k2f', K=K6),
    'R2w_i': dict(rule='R2w', K=KI), 'R2b_i': dict(rule='R2b', K=KI),
    'Hfull_3': dict(rule='H', K=K3), 'Hfull_6': dict(rule='H', K=K6), 'Hfull_i': dict(rule='H', K=KI),
    # the (200, 64) panel
    'R2_i_N200': dict(rule='R2', K=KI, N=200),
}


def cell_job(args):
    """args = (cell, rep, extend_to[, barred list, tag]): one run, written to runs/per_root/cell_<tag>/rep_<rep>.json.
    extend_to: 10000 (default) or 20000.  barred: [(role, tk, set, script)] never written (mediation replays)."""
    cell, rep, extend_to = args[:3]
    barred = args[3] if len(args) > 3 else None
    tag = args[4] if len(args) > 4 else cell
    d = os.path.join(OUT, 'cell_' + tag)
    f = os.path.join(d, 'rep_%03d.json' % rep)
    if os.path.exists(f):
        return tag, rep, dict(skipped=0.0)
    R.load_costc()
    cfg = CELLS[cell]
    N = cfg.get('N', 100)
    t0 = time.time()
    if cfg['rule'] == 'H':
        run = CC.make_run(CC.mask_for('Hfull'), rep, N=N, K=cfg['K'])
        run.st_ = None
    else:
        bars = None
        if barred:
            bars = defaultdict(set)
            for role, tk, si, ix in barred:
                bars[(role, tk)].add((si, ix))
        run = make_run(cfg['rule'], rep, N=N, K=cfg['K'], dispatch=cfg.get('dispatch', False), barred=bars)
    run.prefill()
    t1 = time.time()
    run.run(R.HORIZON)
    t2 = time.time()
    sham = R.evaluator_k('sham', 'S', KI)
    summ, RS = R.summarize(run, ev_sham=sham, horizon=R.HORIZON)
    pr = dict(cfg=dict(cfg, cell=cell, barred=barred))
    cache = {}
    if run.st_ is not None:
        pr['held_2000'] = held_stats(run, RS.at_gen(R.HORIZON), cache)
        pr['kernel_2000'] = kernel_counters(run)
        pr['cost_2000'] = cost_log(run)
        pr['prod_log'] = prod_log(summ)
    t3 = time.time()
    out = dict(cell=tag, rep=rep, summary=summ, pr=pr, time=dict(setup=t1 - t0, run=t2 - t1, summary=t3 - t2))
    run.run(extend_to)
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
    if extend_to > R.EXTEND:
        c1 = RS.at_gen(R.EXTEND)
        out['summary_ext']['at_10000'] = dict(persistence=float(RS.fair[c1].mean()),
                                              wage=[float((RS.wage[c1] == w).mean()) for w in range(3)])
    fs = RS.fair.mean(axis=1)
    pr['traj'] = {str(gg): float(fs[min(gg // R.CHECK_EVERY, ci)]) for gg in TRAJ_GENS if gg <= extend_to}
    pr['wage_states'] = wage_states(RS)
    pr['nuclei'] = nuclei(run, RS)
    pr['fair_bosses'] = fair_bosses(run, RS, (0, 10, 20, 30, 50, 100, 200, 500, 1000, 2000, 5000, 10000))
    if run.st_ is not None:
        pr['held_end'] = held_stats(run, ci, cache)
        pr['held_200'] = held_stats(run, RS.at_gen(200), cache)
        pr['acquisition'] = acquisition(run, RS, cache)
        pr['kernel_end'] = kernel_counters(run)
        pr['cost_end'] = cost_log(run)
        pr['ntypes'] = (len(run.btypes), len(run.wtypes))
    pr['t_fill'] = run.t_fill
    out['time']['ext'] = time.time() - t3
    os.makedirs(d, exist_ok=True)
    tmp = f + '.tmp%d' % os.getpid()
    json.dump(out, open(tmp, 'w'), default=str)
    os.replace(tmp, f)
    return tag, rep, out['time']


# ----------------------------------------------------------------------------------------------------------------
# 6. PROD3A as code (the realizability audit, notes §1.0 item 12): appended to K3' in the audit process only
# ----------------------------------------------------------------------------------------------------------------
PROD3A_SRC = r"""
; ---------------- PROD3A: PROD3 that also writes the shadowed F-branch alternative ----------------
; qtac returns (node-or-NONE . (count . alternative-or-NONE)); PCORE3A returns (primary-or-NONE . alternative-or-NONE)
(def PROD3A (arg) (capk (fst arg) PCORE3A (snd arg)))
(def PCORE3A (ad)
  (let ((r (snd ad)) (enc (fst r)) (j (fst (snd r))) (A (fst (snd (snd r)))) (K (snd (snd (snd r))))
        (cx (pair (pair 8 (pair ID_CHK3 ad)) ad))
        (res (qtac cx 0 0 (pair (mkatom (mkconf4 enc j) K A 0) 0) 0)))
    (pair (fst res) (snd (snd res)))))
(def qfail (c) (pair NONE (pair c NONE)))
(def qtac (cx al L R c)
  (if (lt 63 c) (qfail (add c 1))
    (let ((c1 (add c 1)))
      (if (caxiom L R) (pair (mknd 0 0 0) (pair c1 NONE))
        (let ((h (ptpos cx al R 0)))
          (if (not (eq h NONE)) (pair (mknd (fst h) (snd h) 0) (pair c1 NONE))
            (let ((g (ptneg al L 0)))
              (if (not (eq g NONE)) (pair (mknd 2 g 0) (pair c1 NONE))
                (qatom cx al L R R 0 c1)))))))))
(def qwrap (j a) (if (eq a NONE) NONE (mknd 26 j (pair a 0))))
(def qatom (cx al L R l j c)
  (if (eq l 0) (qfail c)
    (let ((x (fst l)))
      (if (not (eq (fst x) 6)) (qatom cx al L R (snd l) (add j 1) c)
        (let ((p (snd x)) (conf (fst p)) (f (fst (snd p))) (a (fst (snd (snd p)))) (m (snd (snd (snd p))))
              (r (cstep conf)))
          (if (and (lt 0 f) (eq (fst r) 2))
              (let ((q (qtac cx al L (fadd (evfrom3 r f a m) (fdel x R)) c)))
                (if (eq (fst q) NONE) q
                  (pair (mknd 26 j (pair (fst q) 0)) (pair (fst (snd q)) (qwrap j (snd (snd q)))))))
              (let ((s (chkstate3 conf f a)))
                (if (eq s 0) (qfail c)
                  (qchk cx al L (fdel x R) j s c)))))))))
(def qchk (cx al L Rx j s c)
  (let ((B (fst s)) (v (alook B al)))
    (if (eq v 2)
      (if (phypable cx B)
          (let ((q (qbranch cx (pair (pair B 1) al) L Rx j s c)))
            (if (not (eq (fst q) NONE))
                (let ((qf (qbranch cx (pair (pair B 0) al) L Rx j s c)))
                  (pair (fst q) (pair (fst (snd q)) (if (eq (fst qf) NONE) (snd (snd q)) (fst qf)))))
                (if (eq (tcheck3 B) T) (qfail c)
                    (qbranch cx (pair (pair B 0) al) L Rx j s c))))
          (qbranch cx (pair (pair B (if (eq (tcheck3 B) T) 1 0)) al) L Rx j s c))
      (qbranch cx al L Rx j s c))))
(def qbranch (cx al L Rx j s c)
  (let ((B (fst s)) (q1 (qtac cx al (fadd B L) (fadd (fst (snd s)) Rx) c)))
    (if (eq (fst q1) NONE) q1
      (let ((q2 (qtac cx al L (fadd B (fadd (snd (snd s)) Rx)) (fst (snd q1)))))
        (if (eq (fst q2) NONE) q2
          (pair (mknd 25 j (pair (fst q1) (pair (fst q2) 0)))
                (pair (fst (snd q2))
                      (if (not (eq (snd (snd q1)) NONE)) (mknd 25 j (pair (snd (snd q1)) (pair (fst q2) 0)))
                        (if (not (eq (snd (snd q2)) NONE)) (mknd 25 j (pair (fst q1) (pair (snd (snd q2)) 0)))
                          NONE)))))))))
; ---------------- validation as code: the program's own root validation (vone4 on its own box) ----------------
(def SELFVAL (ad) (vone4 (pair ID_CHK3 ad)))
"""


def build_audit_library():
    """K3' plus PROD3A_SRC (appended: every existing index is unchanged).  Rebuilds lt_code's global library in this
    process; call only in the audit process."""
    import lt_code as L
    assert F.ISWRAP_OLD in C.CERT_SRC
    comp = L.SxCompiler()
    for k, v in L.LIB_CONSTS.items(): comp.consts[k] = v
    for k, v in C.CERT_CONSTS.items(): comp.consts[k] = v
    for k, v in F.CERT4_CONSTS.items(): comp.consts[k] = v
    comp.load(L.LIBRARY_SRC)
    comp.load(C.CERT_SRC.replace(F.ISWRAP_OLD, F.ISWRAP_NEW))
    comp.load(F.CERT4_SRC)
    n_old = len(comp.order)
    comp.load(PROD3A_SRC)
    for nm in C.WRAP_NAMES + ['CHK3', 'CHK3N']: comp.consts['ID_' + nm] = comp.order.index(nm)
    comp.consts['NLIB'] = len(comp.order)
    old_index = dict(L.LIBIDX)
    terms = comp.build(0)
    for nm, i in old_index.items():
        assert comp.index[nm] == i, nm
    L.LIB[:] = terms
    L.LIBNAME.clear(); L.LIBNAME.update({i: n for i, n in enumerate(comp.order)})
    L.LIBIDX.clear(); L.LIBIDX.update(comp.index)
    L._compiled.clear()
    L.LIBCODE[:] = [L.compile_term(t[1]) for t in terms]
    L.CACHE.clear()
    for nm, kind in (('vone4', 'vone'), ('cchk3', 'node')):        # re-install the parent's step probes
        F._ORIG.pop(nm, None)
        F._wrap_lib(nm, kind)
    return comp, n_old


def term_prod3a(enc, j, A, Pcap=F.V_MAIN, V=F.V_MAIN, K=F.K_MAIN, fuel=None):
    """PROD3A by the term at the producer's own box: (primary data | None, alternative data | None, steps, outcome)."""
    import lt_code as L
    arg = F.P(F.N(Pcap), F.mk_arg4(V, enc, j, A, K))
    tm = ('app', ('lib', L.LIBIDX['PROD3A']), arg)
    v, n = L.run_big(L.evaluate, tm, fuel if fuel is not None else 10 ** 9)
    if v == 'BOT': return None, None, n, 'fuelTO'
    if v == 'TO': return None, None, n, 'capTO'
    NONE = L.LIB_CONSTS['NONE']
    d = F._rt_data(v)
    prim, alt = d
    if prim == NONE: return None, None, n, 'none'
    return prim, (None if alt == NONE else alt), n, 'found'
