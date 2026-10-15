"""Legibility at founding in the fully realizable social organization game (notes/founding-legibility.md).

Imports the parent's machinery (`sog_full`, `sog_full_kern`, `sog_full_run`) unchanged and adds:
  * the founding pass (L1, notes §1.0 item 2): one frozen empty-list snapshot, each founder alone runs S-nonself_3
    production on M = 10 random non-self cross-role triples of its island's founders, under the ordinary cap and fuel;
  * `FLRun`, the parent's `Run` with founders' lists given (L1), with the mark kernel (L2), or with the founding
    lists delivered at a later check (L1-withheld, by surgery with the kernel's own `replace`);
  * the extra statistics of notes §1.0 item 7 (worker-slot composition, manipulation checks).
"""
import os
import sys
import json
import time
from collections import defaultdict

import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sog_full as F
import sog_full_kern as KN
import sog_full_run as R
import founding_legibility_kern as FK

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'runs', 'founding_legibility')
M_FOUND = 10
K6, K3, KI = 10 ** 6, 3 * 10 ** 6, 10 ** 12
WITHHOLD_GEN = 10

CELLS = {
    # natural founding (the parent's rule); N6 replicates rerun for validation and the new statistics
    'N6': dict(arm='eq', K=K6),
    'N3': dict(arm='eq', K=K3),
    'Ni': dict(arm='eq', K=KI),
    # L1, legible founders
    'L1_6': dict(arm='eq', K=K6, found='L1'),
    'L1_3': dict(arm='eq', K=K3, found='L1'),             # L3
    'L1_i': dict(arm='eq', K=KI, found='L1'),
    'L1W_3': dict(arm='eq', K=K3, found='W'),             # withheld until generation 10
    'L1sham_3': dict(arm='sham', K=K3, found='L1'),
    'L1_3_N200': dict(arm='eq', K=K3, found='L1', N=200),
    # L2, the mark (safe key), and L1 + L2
    'L2_6': dict(arm='eq', K=K6, mark=1),
    'L1L2_6': dict(arm='eq', K=K6, found='L1', mark=1),
    # the added diagnostic: H + eq on the ideal table (the maximal founding list)
    'Heq_i': dict(arm='eq', K=KI, mode='H'),
}


def cell_cfg(name):
    c = dict(CELLS[name])
    c.setdefault('mode', 'S'); c.setdefault('N', 100); c.setdefault('I', 64); c.setdefault('mN', 1.0)
    c['name'] = name
    return c


# ----------------------------------------------------------------------------------------------------------------
# the founding pass
# ----------------------------------------------------------------------------------------------------------------
@njit(cache=True)
def prod_one(s, bb, xx, yy, T, PT, BLACK, WLACK, LIVE_EQ, K, P, VPLUS, PW_, ctr, miss, oi, oc, apply_stats):
    """The production of the participant in slot s alone at the composed encounter (bb, xx, yy): its new type, or
    -1 on a table miss.  The parent's kernel routines, so the computation is an encounter's."""
    if not KN.chain(bb, xx, yy, T, oi, oc, miss):
        return -1
    if s == 0:
        if BLACK[T[24][bb]] == 0:
            return bb
        return KN.prod_boss(bb, oi, oc, PT, K, P, VPLUS, PW_, ctr, miss, apply_stats)
    x = xx if s == 1 else yy
    if WLACK[T[2][x]] == 0:
        return x
    return KN.prod_worker(x, s, oi, oc, PT, LIVE_EQ, K, P, VPLUS, PW_, ctr, miss, apply_stats)


class Producer:
    """Calls prod_one on a run's tables, filling table misses through the run's own fill methods."""

    def __init__(self, run):
        self.run = run
        self.oi = np.zeros(10, np.int64); self.oc = np.zeros(15, np.int64); self.miss = np.zeros(8, np.int64)
        self.dummy = np.zeros(KN.NCTR, np.int64)
        self.live_eq = 1 if 'EQ' in run.ev.live else 0
        self.refresh()

    def refresh(self):
        r = self.run
        self.T, self.PT = r.T(), R.Run.PT(r)

    def __call__(self, s, b, x, y, ctr):
        r = self.run
        ev = r.ev
        while True:
            A = r.A
            v = prod_one(s, b, x, y, self.T, self.PT, A['BLACK'], A['WLACK'], self.live_eq, ev.K, ev.P, F.VPLUS,
                         F.PROD_W, self.dummy, self.miss, self.oi, self.oc, False)
            if v >= 0:
                break
            if self.miss[0] == 8:
                r.grow_pairs()
            else:
                r.fill_miss(self.miss.copy())
            self.refresh()
        A = r.A
        v2 = prod_one(s, b, x, y, self.T, self.PT, A['BLACK'], A['WLACK'], self.live_eq, ev.K, ev.P, F.VPLUS,
                      F.PROD_W, ctr, self.miss, self.oi, self.oc, True)
        assert v2 == v
        return v

    def chain(self, b, x, y):
        r = self.run
        while not KN.chain(b, x, y, self.T, self.oi, self.oc, self.miss):
            if self.miss[0] == 8:
                r.grow_pairs()
            else:
                r.fill_miss(self.miss.copy())
            self.refresh()
        return self.oi.copy(), self.oc.copy()


def empty_types(run):
    """Type ids of the founders with empty lists: (3, I, N) array."""
    ev = run.ev
    out = np.zeros((3,) + run.founders[0].shape, np.int64)
    cache = {}
    for s, arr in enumerate(run.founders):
        role = 'B' if s == 0 else 'W'
        for i in range(arr.shape[0]):
            for k in range(arr.shape[1]):
                sp = int(arr[i, k])
                key = (s, sp)
                if key not in cache:
                    cache[key] = run.type_id(role, ev.reg.get(role, sp, F.empty_inv(role)))
                out[s, i, k] = cache[key]
    return out


def founding_pass(run, M=M_FOUND, trace=None):
    """L1 (notes §1.0 item 2).  Returns (types (3, I, N) after the pass, stats).  trace: a list to which every
    triple is appended as (slot, island, founder, m, b, x, y, type before, type after)."""
    ev = run.ev
    I, N = run.I, run.N
    sp = [np.asarray(a) for a in run.founders]
    et = empty_types(run)
    ft = et.copy()
    rng = np.random.default_rng([run.rep, N, I, 20261014, 1])
    pr = Producer(run)
    ctr = np.zeros(KN.NCTR, np.int64)
    steps = np.zeros((3, I, N), np.int64)
    ntrip = np.zeros((3, I, N), np.int64)
    late_acq = 0          # worker founders acquiring a script after their first triple (S13)
    t0 = time.time()
    for i in range(I):
        for s in range(3):
            o1, o2 = KN.others(s)
            for k in range(N):
                t = int(et[s, i, k])
                if s > 0:
                    other = 2 if s == 1 else 1
                    cand = np.nonzero(sp[other][i] != sp[s][i, k])[0]
                for m in range(M):
                    if s == 0:
                        b = t; x = int(et[1, i, rng.integers(N)]); y = int(et[2, i, rng.integers(N)])
                    else:
                        if len(cand) == 0:
                            break
                        bb = int(et[0, i, rng.integers(N)])
                        oo = int(et[other, i, cand[rng.integers(len(cand))]])
                        if s == 1:
                            b, x, y = bb, t, oo
                        else:
                            b, x, y = bb, oo, t
                    before = ctr[17] + ctr[18]
                    nt = pr(s, b, x, y, ctr)
                    if trace is not None:
                        trace.append((s, i, k, m, b, x, y, t, int(nt)))
                    steps[s, i, k] += ctr[17] + ctr[18] - before
                    ntrip[s, i, k] += 1
                    if nt != t and s > 0 and m > 0:
                        late_acq += 1
                    t = int(nt)
                ft[s, i, k] = t
    st = dict(time=time.time() - t0, ctr=ctr[:19].tolist(), late_worker_acquisitions=int(late_acq),
              no_triple_workers=int((ntrip[1:] == 0).sum()))
    for s in range(3):
        st['steps_s%d' % s] = dict(median=float(np.median(steps[s])), mean=float(steps[s].mean()),
                                   q90=float(np.quantile(steps[s], 0.9)), max=int(steps[s].max()))
    st['steps_per_island_mean'] = float(steps.sum(axis=(0, 2)).mean())
    st['coverage'] = coverage(run, ft)
    return ft, st


def coverage(run, types):
    """Share of founders holding a script, per role and per set."""
    ev = run.ev
    out = {}
    for s in range(3):
        role = 'B' if s == 0 else 'W'
        tl = run.btypes if s == 0 else run.wtypes
        fam = F.FAM[role]
        anyc = 0; per = np.zeros(len(fam))
        tt = types[s].ravel()
        for t in tt:
            inv = ev.reg[tl[int(t)]].inv
            anyc += any(len(z) for z in inv)
            per += np.array([len(z) > 0 for z in inv])
        out['slot%d' % s] = dict(any=anyc / len(tt), per_set=(per / len(tt)).tolist())
    return out


def founder_seq(run, types):
    """The (spelling, inventory) sequence in Run.__init__'s founder loop order (i, s, k)."""
    ev = run.ev
    seq = []
    for i in range(run.I):
        for s in range(3):
            tl = run.btypes if s == 0 else run.wtypes
            for k in range(run.N):
                pr = ev.reg[tl[int(types[s, i, k])]]
                seq.append((pr.sp, pr.inv))
    return seq


# ----------------------------------------------------------------------------------------------------------------
# the run
# ----------------------------------------------------------------------------------------------------------------
class FLRun(R.Run):
    """The parent's Run with (optionally) given founder lists and (optionally) the mark kernel."""

    def __init__(self, ev, cfg, rep, founder_seq=None, mark=None):
        self._fseq = founder_seq
        self._fpos = 0
        self.mark = mark
        super().__init__(ev, cfg, rep)
        if founder_seq is not None:
            assert self._fpos == len(founder_seq)

    def founder_inv(self, role, sp):
        if self._fseq is None:
            return super().founder_inv(role, sp)
        sp2, inv = self._fseq[self._fpos]
        self._fpos += 1
        assert sp2 == sp
        return inv

    def PT(self):
        pt = super().PT()
        return pt if self.mark is None else pt + tuple(self.mark)

    def run(self, gens):
        if self.mark is None:
            return super().run(gens)
        # the parent's Run.run with the mark kernel (founding_legibility_kern.K2.run_kernel)
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
            status = FK.K2.run_kernel(self.st, self.seed, I, N, 0.3, m, r_enc, self.checks, self.ev.K, self.ev.P,
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
        self.save_shared()
        return self


def evaluator(cfg):
    return R.evaluator_k(cfg['arm'], cfg['mode'], cfg['K'])


def make_run(cfg, rep):
    """Builds the run of a cell: the founding pass (L1, W) on a natural Run of the same seed whose tables are shared,
    then the cell's Run.  Returns (run, info)."""
    ev = evaluator(cfg)
    info = {}
    seq = None
    finv = None
    if cfg.get('found') in ('L1', 'W'):
        base = R.Run(ev, dict(cfg, mode='S'), rep)
        ft, st = founding_pass(base)
        info['founding'] = st
        if cfg['found'] == 'L1':
            seq = founder_seq(base, ft)
        else:
            finv = (base.founders, ft, base)
        base.save_shared()
    mark = FK.new_mark_state(1) if cfg.get('mark') else None
    run = FLRun(ev, cfg, rep, founder_seq=seq, mark=mark)
    if finv is not None:
        # the withheld lists: (spellings, founding types) as inventories, keyed for delivery by spelling
        spf, ft, base = finv
        pools = defaultdict(list); gpools = defaultdict(list)
        for s in range(3):
            tl = base.btypes if s == 0 else base.wtypes
            for i in range(run.I):
                for k in range(run.N):
                    inv = ev.reg[tl[int(ft[s, i, k])]].inv
                    pools[(i, s, int(spf[s][i, k]))].append(inv)
                    gpools[(s, int(spf[s][i, k]))].append(inv)
        run._withheld = (pools, gpools)
    return run, info


def deliver_withheld(run):
    """L1-withheld (notes §1.0 item 3): every present individual receives, for each set it lacks, the founding script
    of a founder of its spelling (pooled per island; lack rule).  Done with the kernel's own replace."""
    ev = run.ev
    pools, gpools = run._withheld
    rng = np.random.default_rng([run.rep, run.N, run.I, 20261014, 2])
    live_eq = 1 if 'EQ' in ev.live else 0
    oi = np.zeros(10, np.int64); oc = np.zeros(15, np.int64); miss = np.zeros(8, np.int64)
    scr = np.zeros((run.N + 2, run.N + 2), np.uint8)
    moved = 0; examined = 0
    for i in range(run.I):
        moves = []
        for s in range(3):
            role = 'B' if s == 0 else 'W'
            tl = run.btypes if s == 0 else run.wtypes
            pres = [(int(run.pres[i, s, t]), int(run.counts[i, s, run.pres[i, s, t]])) for t in range(run.npres[i, s])]
            for k, c in pres:
                pr = ev.reg[tl[k]]
                pool = pools.get((i, s, pr.sp)) or gpools.get((s, pr.sp))
                examined += c
                if not pool:
                    continue
                ch = rng.integers(len(pool), size=c)
                grp = defaultdict(int)
                for q in ch:
                    merged = tuple(a if len(a) else b for a, b in zip(pr.inv, pool[int(q)]))
                    grp[merged] += 1
                for merged, cnt in sorted(grp.items()):
                    if merged == pr.inv:
                        continue
                    nk = run.type_id(role, ev.reg.get(role, pr.sp, merged))
                    moves.append((s, k, nk, cnt))
        for s, k, nk, cnt in moves:
            for _ in range(cnt):
                newt = np.full(3, -1, np.int64)
                if run.counts[i, s, nk] == 0:
                    newt[s] = nk
                    while not KN.precheck_multi(i, newt, run.counts, run.pres, run.npres, run.T(), run.A['WACT'],
                                                run.A['TAG'], live_eq, oi, oc, miss, scr):
                        run.st[KN.ST_STATUS] = 0
                        KN.collect_precheck(i, newt, run.npres, run.pres, run.T(), run.mbuf, run.st)
                        if run.st[KN.ST_STATUS] == 0:
                            if miss[0] == 8: run.grow_pairs()
                            else: run.fill_miss(miss.copy())
                        else:
                            run.fill_batch()
                KN.replace(i, s, k, nk, run.counts, run.pres, run.npres, run.pos, run.F, run.JQ, R.PAYF, run.T(),
                           run.A['WACT'], run.A['TAG'], live_eq, oi, oc, miss, scr, 1)
                moved += 1
        KN.mark_dirty(i, run.quiet, run.nqlist, run.nqpos, run.st)
        for s in range(3):
            KN.setact(3 * i + s, run.npres[i, s] > 1, run.act, run.apos, run.st)
    # consistency: the incremental fitness equals a full recomputation
    err = 0.0
    for i in range(run.I):
        for s in range(3):
            for t in range(run.npres[i, s]):
                k = run.pres[i, s, t]
                v = KN.fit_full(i, s, k, run.counts, run.pres, run.npres, run.pos, run.JQ, R.PAYF)
                err = max(err, abs(v - run.F[i, s, k]))
    return dict(moved=moved, examined=examined, fitness_err=err)


# ----------------------------------------------------------------------------------------------------------------
# statistics (notes §1.0 item 7)
# ----------------------------------------------------------------------------------------------------------------
_CLS = {}


def wclass(ev, sp):
    """P§1.8's class by play of a worker spelling ('open', 'greenbeard', 'unconditional')."""
    key = (id(ev), sp)
    if key not in _CLS:
        g = ev.g
        pid = ev.reg.get('W', sp, F.full_inv(g, 'W', int(g.roles['W']['tau'][sp])))
        _CLS[key] = R.holder_class(None, ev, pid, {})
    return _CLS[key]


def snap_types(run, ci, i, s):
    t, c = R.snap_comp(run, ci, i, s)
    return t, c


def composition(run, ci):
    ev = run.ev
    tot = defaultdict(float); n = 0.0
    for i in range(run.I):
        for s in (1, 2):
            t, c = snap_types(run, ci, i, s)
            for tt, cc in zip(t, c):
                tot[wclass(ev, ev.reg[run.wtypes[int(tt)]].sp)] += cc
                n += cc
    return {k: v / n for k, v in tot.items()}


def militant_survival(run, ci):
    """Fraction of (island, open-militant spelling founded there) pairs whose spelling is present at check ci."""
    ev = run.ev
    _, sp1, sp2 = run.founders
    pairs = 0; alive = 0
    for i in range(run.I):
        fs = set(int(z) for z in sp1[i]) | set(int(z) for z in sp2[i])
        mil = [z for z in fs if wclass(ev, z) == 'open']
        present = set()
        for s in (1, 2):
            t, c = snap_types(run, ci, i, s)
            for tt in t:
                present.add(ev.reg[run.wtypes[int(tt)]].sp)
        pairs += len(mil); alive += sum(1 for z in mil if z in present)
    return alive / max(pairs, 1)


def gen0_stats(run, nsamp=300):
    """Manipulation checks (a), (b), (d) at generation 0 (called after prefill, before the run)."""
    ev = run.ev
    I, N = run.I, run.N
    out = {}
    # (a) coverage of the founders' lists
    types = np.zeros((3, I, N), np.int64)
    for i in range(I):
        for s in range(3):
            row = []
            for t in range(run.npres[i, s]):
                k = run.pres[i, s, t]
                row += [k] * int(run.counts[i, s, k])
            types[s, i] = row
    out['coverage'] = coverage(run, types)
    # (b) first-encounter decisions: an open-militant founder's strike probability in a uniform encounter (cube)
    st_num = 0.0; st_den = 0.0; wk_num = 0.0; wk_den = 0.0
    for i in range(I):
        n0, n1, n2 = run.npres[i]
        cb = run.counts[i, 0, run.pres[i, 0, :n0]].astype(float)
        c1 = run.counts[i, 1, run.pres[i, 1, :n1]].astype(float)
        c2 = run.counts[i, 2, run.pres[i, 2, :n2]].astype(float)
        J = run.JQ[i, :n0, :n1, :n2].astype(np.int64) // 4
        a1 = (J // 2) % 2; a2 = J % 2
        p1 = np.einsum('b,bpq,q->p', cb, a1, c2) / (N * N)
        p2 = np.einsum('b,bpq,p->q', cb, a2, c1) / (N * N)
        for s, cs, ps in ((1, c1, p1), (2, c2, p2)):
            for t in range(len(cs)):
                spx = ev.reg[run.wtypes[int(run.pres[i, s, t])]].sp
                wk_num += cs[t] * ps[t]; wk_den += cs[t]
                if wclass(ev, spx) == 'open':
                    st_num += cs[t] * ps[t]; st_den += cs[t]
    out['militant_strike_p'] = st_num / max(st_den, 1)
    out['worker_strike_p'] = wk_num / max(wk_den, 1)
    # (d) retention: a held script certifies its holder in a uniform generation-0 encounter
    rng = np.random.default_rng([run.rep, 20261014, 4])
    pr = Producer(run)
    held = np.zeros((3, 3)); cert = np.zeros((3, 3))
    for i in range(I):
        for _ in range(nsamp // 10):
            ks = []
            for s in range(3):
                n = run.npres[i, s]
                w = run.counts[i, s, run.pres[i, s, :n]].astype(float)
                ks.append(int(run.pres[i, s, rng.choice(n, p=w / w.sum())]))
            oi, oc = pr.chain(*ks)
            bp = ev.reg[run.btypes[ks[0]]]
            for A in range(3):
                if len(bp.inv[A]):
                    held[0, A] += 1; cert[0, A] += ((oi[3] // 3 ** A) % 3) == 1
            for j, base in ((1, 4), (2, 6)):
                wp = ev.reg[run.wtypes[ks[j]]]
                for A in range(2):
                    if len(wp.inv[A]):
                        held[j, A] += 1; cert[j, A] += oi[base + A] == 1
    out['retention'] = dict(held=held.tolist(), certified=cert.tolist(),
                            rate=[[float(cert[s, A] / held[s, A]) if held[s, A] else None for A in range(3)]
                                  for s in range(3)])
    return out


def later_stats(run, mark=None):
    out = {}
    for g in (0, 10, 50, 200):
        ci = g // R.CHECK_EVERY
        out['comp_%d' % g] = composition(run, ci)
        if g in (10, 50):
            out['militant_survival_%d' % g] = militant_survival(run, ci)
    if mark is not None:
        MARK, MK, LOG = mark
        n = int(MK[FK.MK_LOGN])
        lg = LOG[:n]
        out['mark'] = dict(MK=MK.tolist(), marks=len(MARK), log_n=n)
        if n:
            play = lg[:, 1].astype(float)
            out['mark']['executed'] = dict(
                median_play=float(np.median(play)),
                ratio_nomark=float(np.median(play + lg[:, 2]) / max(np.median(play), 1)),
                ratio_mark=float(np.median(play + lg[:, 3]) / max(np.median(play), 1)),
                mean_ratio_nomark=float((play + lg[:, 2]).sum() / max(play.sum(), 1)),
                mean_ratio_mark=float((play + lg[:, 3]).sum() / max(play.sum(), 1)))
    return out


def mark_cost_samples(run, gens=(0, 50, 200, 2000), n=300):
    """Population-sampled encounters (the parent's estimator, its own stream): play steps, production steps charged
    (every attempt, as in S_3), and production steps with every NONE attempt skipped (the mark's steady state)."""
    ev = run.ev
    rng = np.random.default_rng([run.rep, 20261014, 5])
    RS_n = int(run.st[KN.ST_CI]) + 1
    rows = []
    for g in gens:
        cj = min(g // R.CHECK_EVERY, RS_n - 1)
        for _ in range(n):
            i = int(rng.integers(run.I))
            ks = []
            for s in range(3):
                t, c = R.snap_comp(run, cj, i, s)
                ks.append(int(rng.choice(t, p=c / c.sum())))
            bp, xp, yp = run.btypes[ks[0]], run.wtypes[ks[1]], run.wtypes[ks[2]]
            tr = ev.triple(bp, xp, yp)
            play = sum(tr['steps'])
            pa = pn = 0
            for pid, npid, rec in ev.productions(bp, xp, yp, tr, gate=run.cfg.get('gate') != 'opp'):
                for r in rec:
                    if r[0] == 'refused': continue
                    pa += r[3]
                    if r[1] != 'none': pn += r[3]
            rows.append((g, int(play), int(pa), int(pn)))
    a = np.array(rows, float)
    out = dict(rows=rows)
    for lab, sel in (('all', np.ones(len(a), bool)), ('late', a[:, 0] >= 50)):
        b = a[sel]
        out[lab] = dict(median_play=float(np.median(b[:, 1])),
                        ratio_s3=float(np.median(b[:, 1] + b[:, 2]) / max(np.median(b[:, 1]), 1)),
                        ratio_mark_steady=float(np.median(b[:, 1] + b[:, 3]) / max(np.median(b[:, 1]), 1)))
    return out


def bare_source_replay(run, cis=(0, 1, 5), later=(1, 5, 20), per_ci=400, cap_pairs=40):
    """The amendment's replay (notes §1.0 item 4): NONE results recorded at sampled encounters at check ci, keyed on
    the bare-source key (own type, slot, set, the partners' spellings), replayed at later checks against partners of
    the same spellings with other lists present anywhere in the population (any island), the producer's own type
    unchanged.  A success is a production the bare-source mark would have suppressed."""
    ev = run.ev
    rng = np.random.default_rng([run.rep, 20261014, 6])
    RS_n = int(run.st[KN.ST_CI]) + 1
    fails = {}
    for ci in cis:
        if ci >= RS_n: continue
        for _ in range(per_ci):
            i = int(rng.integers(run.I))
            ks = []
            for s in range(3):
                t, c = R.snap_comp(run, ci, i, s)
                ks.append(int(rng.choice(t, p=c / c.sum())))
            pids = [run.btypes[ks[0]], run.wtypes[ks[1]], run.wtypes[ks[2]]]
            for s, (pid, npid, rec) in enumerate(ev.productions(*pids)):
                for r in rec:
                    if r[0] == 'refused' or r[1] != 'none': continue
                    o1, o2 = KN.others(s)
                    key = (s, pid, r[0], ev.reg[pids[o1]].sp, ev.reg[pids[o2]].sp)
                    fails.setdefault(key, (ci, pids[o1], pids[o2]))
    # every (slot, spelling) -> pids present at each later check, over all islands
    avail = {}
    for cj in later:
        if cj >= RS_n: continue
        dd = defaultdict(set)
        for i in range(run.I):
            for ss in range(3):
                t, c = R.snap_comp(run, cj, i, ss)
                tl = run.btypes if ss == 0 else run.wtypes
                for z in t:
                    q = tl[int(z)]
                    dd[(ss, ev.reg[q].sp)].add(q)
        avail[cj] = dd
    replays = 0; succ = 0; examples = []; keys_tested = 0; keys_succ = 0
    for key, (ci, p1, p2) in fails.items():
        s, pid, A, sp1, sp2 = key
        o1, o2 = KN.others(s)
        tested = False; hit = False
        for cj in later:
            if cj <= ci or cj not in avail: continue
            c1 = sorted(avail[cj].get((o1, sp1), ())); c2 = sorted(avail[cj].get((o2, sp2), ()))
            pairs = [(x, y) for x in c1 for y in c2 if (x, y) != (p1, p2)]
            if len(pairs) > cap_pairs:
                pairs = [pairs[int(z)] for z in rng.choice(len(pairs), cap_pairs, replace=False)]
            for x, y in pairs:
                trip = [None, None, None]; trip[s] = pid; trip[o1] = x; trip[o2] = y
                if s > 0 and ev.reg[trip[1]].sp == ev.reg[trip[2]].sp:
                    continue
                rec = ev.productions(*trip)[s][2]
                for r in rec:
                    if r[0] == A:
                        replays += 1; tested = True
                        if r[1] == 'found':
                            succ += 1; hit = True
                            if len(examples) < 8:
                                examples.append([cj * R.CHECK_EVERY, s, F.show(ev.g.roles['B' if s == 0 else 'W']['spellings'][ev.reg[pid].sp]), A])
        keys_tested += tested; keys_succ += hit
    return dict(failures_recorded=len(fails), keys_replayed=keys_tested, keys_with_success=keys_succ,
                replays=replays, suppressed_successes=succ, examples=examples)


def replay_job(rep, gens=200):
    """The replay on a natural S_3 + eq run of replicate rep run to `gens` generations."""
    R.load_costc()
    cfg = cell_cfg('N6')
    run, info = make_run(cfg, rep)
    run.prefill()
    run.run(gens)
    return bare_source_replay(run)


def cell_job(args):
    name, rep, extend = args
    d = os.path.join(OUT, 'cell_' + name)
    f = os.path.join(d, 'rep_%03d.json' % rep)
    if os.path.exists(f):
        return name, rep, dict(skipped=0.0)
    R.load_costc()
    cfg = cell_cfg(name)
    t0 = time.time()
    run, info = make_run(cfg, rep)
    run.prefill()
    t1 = time.time()
    g0 = gen0_stats(run) if cfg['mode'] == 'S' else None
    t1b = time.time()
    if cfg.get('found') == 'W':
        run.run(WITHHOLD_GEN)
        info['withheld'] = deliver_withheld(run)
    run.run(R.HORIZON)
    t2 = time.time()
    ev = run.ev
    sham = R.evaluator_k('sham', cfg['mode'], cfg['K']) if ev.g.gram == 'id' and cfg['arm'] != 'sham' else None
    summ, RS = R.summarize(run, ev_sham=sham, horizon=R.HORIZON)
    fl = later_stats(run, run.mark if isinstance(run, FLRun) else None)
    fl['gen0'] = g0
    fl.update(info)
    if cfg.get('mark') or (name == 'N6' and rep < 5):
        t2b = time.time()
        fl['mark_cost'] = mark_cost_samples(run)
        if name == 'N6':
            fl['replay'] = bare_source_replay(run)
        fl['t_extra'] = time.time() - t2b
    out = dict(cell=name, rep=rep, summary=summ, fl=fl,
               time=dict(setup=t1 - t0, gen0=t1b - t1, run=t2 - t1b, summary=time.time() - t2))
    if extend:
        t3 = time.time()
        run.run(R.EXTEND)
        RS = R.RunStats(run)
        ci = RS.nck - 1
        end = dict(gen=ci * R.CHECK_EVERY, persistence=float(RS.fair[ci].mean()),
                   wage=[float((RS.wage[ci] == w).mean()) for w in range(3)], prodeff=float(RS.prodeff[ci].mean()),
                   strike_any=float(np.mean([(k // 4) % 4 != 0 for k in RS.play[ci]])))
        out['summary_ext'] = dict(end=end, fair_t=RS.fair.mean(axis=1)[::10].tolist(),
                                  wage_t=[[float((RS.wage[c] == w).mean()) for w in range(3)]
                                          for c in range(0, RS.nck, 10)],
                                  ctr=run.ctr.tolist())
        if run.mark is not None:
            out['mark_ext'] = run.mark[1].tolist()
        out['time']['ext'] = time.time() - t3
    os.makedirs(d, exist_ok=True)
    tmp = f + '.tmp%d' % os.getpid()
    json.dump(out, open(tmp, 'w'), default=str)
    os.replace(tmp, f)
    ev.maybe_clear(0)
    return name, rep, out['time']
