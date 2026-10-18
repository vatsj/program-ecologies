"""Tests for the per-root run (notes/per-root.md §1.0): R1 never attempts a set with a script valid at the root; R2
writes exactly the shadowed alternative; R0 reproduces S3 draw for draw; the mark is list-invariant and safe; the
order of operations under repeated failure, append, eviction and return to an earlier root; the lackable bits; the
kernel against the Python encounter path."""
import os
import sys
import itertools

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import sog_full as F
import sog_full_run as R
import sog_full_kern as KN
import lt_cert as C
import founding_legibility as FL
import founding_legibility_kern as FK
import coverage_components as CC
import per_root as PR
import per_root_kern as PK

R.load_costc()
G = R.grammar('id')
SMALL = dict(I=4, N=30)
GENS = 60
_if, _A, _L = F._if, F._A, F._L
ALTPROG = _if(_A(('O', F.A_WORK)), _L('W'), _if(_A(('B', F.A_EQ12)), _L('W'), _L('S')))   # O:W ? W : (B1/2 ? W : S)


def wpid(ev, x, inv=None):
    sp = G.roles['W']['spellings'].index(x)
    tk = int(G.roles['W']['tau'][sp])
    return ev.reg.get('W', sp, inv if inv is not None else F.empty_inv('W'))


def bpid(ev, x, inv=None):
    sp = G.roles['B']['spellings'].index(x)
    return ev.reg.get('B', sp, inv if inv is not None else F.empty_inv('B'))


ROOTS_W = [(bex, oex) for bex in itertools.product('TF', repeat=3) for oex in itertools.product('TF', repeat=2)
           if not (oex == ('T', 'T')) and not (bex[1] == 'T' and bex[2] == 'T')]


# ---------------------------------------------------------------- PROD3A
def test_prod3a_primary_is_prod3_and_alt_in_H():
    """On every worker run tree and root (EQ = F): PROD3A's primary is PROD3's script, its visit log extends PROD3's,
    and the alternative is an H script valid where the hypothesised co-worker box is false."""
    W = G.roles['W']
    n_alt = 0
    for tk, t in enumerate(W['dts']):
        _, per = G.hlist('W', tk)
        ats = [a for a in F.dt_atoms(t) if a[0] != 'E']
        for A in F.WORKER_Q:
            for bits in itertools.product('TF', repeat=len(ats)):
                val = dict(zip(ats, bits))
                bv = lambda a: val[a]
                idv = lambda nm: False
                l0, l1 = [], []
                s0, c0 = F.sym_prod3(t, 'W', A, idv, bv, l0)
                s1, a1, c1 = PR.sym_prod3_alt(t, 'W', A, idv, bv, l1)
                assert s0 == s1
                if 'altbr' not in [e[0] for e in l1]:
                    assert l0 == l1 and a1 is None          # no Hyp choice closed: PROD3A is PROD3 step for step
                    continue
                if a1 is None:
                    continue                                # the F branch was run (and charged) and failed
                n_alt += 1
                assert a1 in per[A] and a1 != s1
                assert 'altbr' in [e[0] for e in l1]
                # the alternative is a script about the same set, valid at some root with a co-worker box false
                ok = False
                for bits2 in itertools.product('TF', repeat=len(ats)):
                    v2 = dict(zip(ats, bits2))
                    u, _ = F.sym_check(t, 'W', A, a1, idv, lambda a: v2[a])
                    if u is not None and any(a[0] == 'O' and v2[a] == 'F' for a in ats):
                        ok = True; break
                assert ok
    assert n_alt > 100


def test_named_alternative():
    """O:W ? W : (B1/2 ? W : S): [C] is Hyp on O:W; its alternative is 'O:W false, B1/2 true' (RunNeg O:W, Run B1/2)."""
    t = F.dt(ALTPROG)
    A = ('C',)
    bv = lambda a: 'T' if a == ('B', F.A_EQ12) else 'F'
    s, alt, calls = PR.sym_prod3_alt(t, 'W', A, lambda nm: False, bv)
    assert s is not None and alt is not None
    alpha = {('O', F.A_WORK): False, ('B', F.A_EQ12): True}
    h, _ = F.sym_produce(t, 'W', A, alpha, lambda nm: False)
    assert alt == h
    # valid where the co-worker is not certified to work and the boss is certified =1/2; invalid otherwise
    u, _ = F.sym_check(t, 'W', A, alt, lambda nm: False, lambda a: 'F' if a[0] == 'O' else 'T')
    assert u == []
    u, _ = F.sym_check(t, 'W', A, alt, lambda nm: False, lambda a: 'T')
    assert u is None


# ---------------------------------------------------------------- R1, R2 at the Python level
def test_r1_never_attempts_a_valid_set():
    ev = PR.evaluator('R1', PR.KI)
    rng = np.random.default_rng(3)
    W = G.roles['W']
    n_checked = 0
    for _ in range(300):
        sp = int(rng.integers(len(W['spellings'])))
        tk = int(W['tau'][sp])
        _, per = G.hlist('W', tk)
        inv = tuple(tuple(sorted(rng.choice(len(per[A]), size=min(len(per[A]), int(rng.integers(0, 3))),
                                            replace=False).tolist())) for A in F.WORKER_Q)
        x = ev.reg.get('W', sp, inv)
        bex, oex = ROOTS_W[int(rng.integers(len(ROOTS_W)))]
        ctx = ev.worker_ctx(x, 1, bex, oex, False)
        cc = [1000] * 5
        npid, recs = ev.part(x, ctx, cc, 1000)
        attempted = {r[1] for r in recs if r[0] == 'prod'}
        for si, c in enumerate(ctx):
            if c[0] == 1:
                assert si not in attempted
                n_checked += 1
            else:
                assert si in attempted
            if c[0] == 1:
                t = W['dts'][tk]
                ents = [sc for A2, sc in ev.reg[x].entries if A2 == F.WORKER_Q[si]]
                assert any(F.sym_check(t, 'W', F.WORKER_Q[si], sc, lambda nm: False,
                                       lambda a: bex[F.BOSS_Q.index(a[1])] if a[0] == 'B' else
                                       (oex[0] if a[1] == F.A_WORK else oex[1]))[0] is not None for sc in ents)
    assert n_checked > 20


def test_r2_writes_alternative_first():
    ev = PR.evaluator('R2', PR.KI)
    x = wpid(ev, ALTPROG)
    bex, oex = ('F', 'T', 'F'), ('F', 'F')
    ctx = ev.worker_ctx(x, 1, bex, oex, False)
    npid, recs = ev.part(x, ctx, [10] * 5, 1000)
    t = F.dt(ALTPROG)
    s, alt, _ = PR.sym_prod3_alt(t, 'W', ('C',), lambda nm: False, lambda a: bex[F.BOSS_Q.index(a[1])]
                                 if a[0] == 'B' else (oex[0] if a[1] == F.A_WORK else oex[1]))
    _, per = G.hlist('W', ev.reg[x].tk)
    assert ev.reg[npid].inv[0] == (per[('C',)].index(alt), per[('C',)].index(s))
    # R1 writes only the primary
    ev1 = PR.evaluator('R1', PR.KI)
    x1 = wpid(ev1, ALTPROG)
    n1, _ = ev1.part(x1, ev1.worker_ctx(x1, 1, bex, oex, False), [10] * 5, 1000)
    assert ev1.reg[n1].inv[0] == (per[('C',)].index(s),)
    # R0 + alternatives writes the bundle once
    ev0 = PR.evaluator('R0alt', PR.KI)
    x0 = wpid(ev0, ALTPROG)
    n0, _ = ev0.part(x0, ev0.worker_ctx(x0, 1, bex, oex, False), [10] * 5, 1000)
    assert ev0.reg[n0].inv[0] == (per[('C',)].index(alt), per[('C',)].index(s))


def test_return_to_earlier_root_and_eviction():
    """D*-like boss: R2 writes per root, validates on return; R3 (k = 2) evicts by CLOCK, FIFO by age."""
    for rule in ('R2', 'R3k2', 'R3k2f'):
        ev = PR.evaluator(rule, PR.KI)
        b = bpid(ev, F.NAMED_B['D*'])
        pi, ii = ev.boss_reads(b)
        codes = []
        for vals in itertools.product('TF', repeat=len(pi)):
            code = ['F'] * 8 + [False, False, False]
            for p, v in zip(pi, vals): code[p] = v
            codes.append(tuple(code))
        cur = b
        seen = []
        for k in range(3):
            for code in codes:
                ctx = ev.boss_ctx(cur, code)
                nxt, recs = ev.part(cur, ctx, [10] * 8, 1000)
                # a set valid at the root is never attempted
                att = {r[1] for r in recs if r[0] == 'prod'}
                for si, c in enumerate(ctx):
                    if c[0] == 1: assert si not in att
                seen.append(tuple(len(z) for z in ev.reg[nxt].inv))
                cur = nxt
        pr = ev.reg[cur]
        if rule == 'R2':
            # every root's script is held after one sweep: the second and third sweeps write nothing
            assert seen[len(codes) - 1] == seen[-1]
            for code in codes:
                ctx = ev.boss_ctx(cur, code)
                for c in ctx:
                    assert c[0] != 0 or c[4] < 0          # invalid only where PROD3 finds nothing
        else:
            assert max(len(z) for z in pr.aux) <= 2
            for z in pr.aux:
                assert all(b_[0] >= 1 for b_ in z)


def test_clock_eviction_unit():
    ev = PR.evaluator('R3k2', PR.KI)
    b = bpid(ev, F.NAMED_B['D*'])
    pr = ev.reg[b]
    _, per = G.hlist('B', pr.tk)
    # build a program holding two bundles for set 2 (<=1/4), the first used (bit 1), the second not
    sc = per[F.BOSS_Q[2]]
    assert len(sc) == 2
    inv = ((), (), (0, 1))
    p = ev.reg.get('B', pr.sp, inv, ((), (), ((1, 1), (1, 0))))
    ctx = (( -1, 0, 0, -1, -1, -1, 0, 0),) * 2 + ((0, 0, 0, -1, 0, -1, 0, 0),)
    # producing a held script writes nothing
    q = ev.apply(p, ctx, (0, 0, 2))
    assert q == p
    # a fake new script index: use a 1-script H list of another set to check eviction order on set 2 (CLOCK keeps
    # the used bundle and evicts the unused one; FIFO evicts the oldest)
    aux = ((), (), ((1, 1), (1, 0)))
    vic = PR.bundle_of(aux[2], 1)
    assert vic == 1


# ---------------------------------------------------------------- the mark
def test_mark_key_list_free_and_safe():
    """PROD3's result for a set at a root does not depend on the program's own list (the mark's key omits it)."""
    for rule in ('R1', 'R2'):
        ev = PR.evaluator(rule, PR.KI)
        rng = np.random.default_rng(5)
        W = G.roles['W']
        for _ in range(200):
            sp = int(rng.integers(len(W['spellings'])))
            tk = int(W['tau'][sp])
            _, per = G.hlist('W', tk)
            invs = [F.empty_inv('W'), F.full_inv(G, 'W', tk),
                    tuple(tuple(range(min(1, len(per[A])))) for A in F.WORKER_Q)]
            bex, oex = ROOTS_W[int(rng.integers(len(ROOTS_W)))]
            res = set()
            for inv in invs:
                x = ev.reg.get('W', sp, inv)
                ctx = ev.worker_ctx(x, 1, bex, oex, False)
                res.add(tuple((c[4], c[5]) for c in ctx))
            assert len(res) == 1


def small_run(rule, rep, K=PR.KI, mark_mode=1):
    run = PR.make_run(rule, rep, K=K, mark_mode=mark_mode, **SMALL)
    run.prefill()
    run.run(GENS)
    return run


def comp(run):
    st, sc, sn = run.snap
    out = []
    for ci in range(st.shape[0]):
        row = []
        for i in range(run.I):
            for s in range(3):
                n = sn[ci, i, s]
                tl = run.btypes if s == 0 else run.wtypes
                row.append(sorted((run.ev.reg[tl[int(t)]].sp, run.ev.reg[tl[int(t)]].inv, int(c))
                                  for t, c in zip(st[ci, i, s, :n], sc[ci, i, s, :n])))
        out.append(row)
    return out


@pytest.mark.parametrize('rep', [0, 1])
def test_r0_reproduces_s3(rep):
    a = small_run('R0', rep)
    ev = R.evaluator_k('eq', 'S', PR.KI)
    b = FL.FLRun(ev, dict(name='x', arm='eq', mode='S', mN=1.0, K=PR.KI, **SMALL), rep, mark=FK.new_mark_state(1))
    b.prefill(); b.run(GENS)
    assert comp(a) == comp(b)
    assert a.ctr[0] == b.ctr[0]
    for k in (2, 7, 12, 13, 16):
        assert a.ctr[k] == b.ctr[k]
    # without any skip the attempts equal S3's (no mark in the parent's own kernel)
    c = small_run('R0', rep, mark_mode=0)
    p = R.Run(ev, dict(name='y', arm='eq', mode='S', mN=1.0, K=PR.KI, share=False, **SMALL), rep)
    p.prefill(); p.run(GENS)
    assert comp(c) == comp(p)
    assert [x for k, x in enumerate(c.ctr) if k != 14] == [x for k, x in enumerate(p.ctr) if k != 14]


def test_mark_is_a_cost_fix_at_the_ideal_table():
    """With the mark on and off (mode 0 records, never skips), R2's dynamics are identical; the mark skips attempts
    and no examined production is mark-sensitive."""
    a = small_run('R2', 0, mark_mode=1)
    b = small_run('R2', 0, mark_mode=0)
    assert comp(a) == comp(b)
    assert a.st_[1][5] > 0                   # attempts skipped
    assert a.st_[1][7] == 0 and b.st_[1][7] == 0
    # the Lemma-M bound (every completed NONE skipped) can differ even here: regress timeouts charge V = K/4, so fuel
    # can bind at K = 10^12; it is reported, not asserted


# ---------------------------------------------------------------- lackable bits and the kernel vs Python
@pytest.mark.parametrize('rule', ['R1', 'R2', 'R3k2'])
def test_kernel_matches_python(rule):
    run = small_run(rule, 0)
    ev = run.ev
    oi = np.zeros(10, np.int64); oc = np.zeros(15, np.int64); miss = np.zeros(8, np.int64)
    newt = np.full(3, -1, np.int64); ctr = np.zeros(KN.NCTR, np.int64)
    st, sc, sn = run.snap
    ci = st.shape[0] - 1
    rng = np.random.default_rng(1)
    n = 0
    for _ in range(150):
        i = int(rng.integers(run.I))
        tb = st[ci, i, 0, :sn[ci, i, 0]]; t1 = st[ci, i, 1, :sn[ci, i, 1]]; t2 = st[ci, i, 2, :sn[ci, i, 2]]
        if not (len(tb) and len(t1) and len(t2)): continue
        bb, xx, yy = int(rng.choice(tb)), int(rng.choice(t1)), int(rng.choice(t2))
        while True:
            A = run.A
            ok = PK.K3.productions(bb, xx, yy, run.T(), run.PT(), A['BLACK'], A['WLACK'], 1, ev.K, ev.P, F.VPLUS,
                                   F.PROD_W, ctr, miss, oi, oc, newt, False)
            if ok: break
            if miss[0] == 8: run.grow_pairs()
            else: run.fill_miss(miss.copy())
        kern = [run.btypes[newt[0]] if newt[0] >= 0 else run.btypes[bb],
                run.wtypes[newt[1]] if newt[1] >= 0 else run.wtypes[xx],
                run.wtypes[newt[2]] if newt[2] >= 0 else run.wtypes[yy]]
        prods = ev.productions_full(run.btypes[bb], run.wtypes[xx], run.wtypes[yy])
        py = [p[1] for p in prods]
        for s in range(3):
            # the kernel's new type is the Python path's new program up to spelling-canonical class
            assert ev.canon(kern[s]) == ev.canon(py[s]) or (ev.reg[kern[s]].inv == ev.reg[py[s]].inv
                                                             and ev.reg[kern[s]].aux == ev.reg[py[s]].aux)
        n += 1
    assert n > 50


def test_lackable_bits_exact():
    """A set whose lackable bit is 0 is attempted at no root and its list never changes (R1 and R2 at the ideal
    table)."""
    for rule in ('R1', 'R2'):
        ev = PR.evaluator(rule, PR.KI)
        rng = np.random.default_rng(9)
        W = G.roles['W']
        m = 0
        for _ in range(300):
            sp = int(rng.integers(len(W['spellings'])))
            tk = int(W['tau'][sp])
            x = ev.reg.get('W', sp, F.full_inv(G, 'W', tk))
            bits = ev.lackable(x)
            zero = [si for si in range(2) if not (bits >> si) & 1]
            if not zero: continue
            m += 1
            for bex, oex in ROOTS_W:
                ctx = ev.worker_ctx(x, 1, bex, oex, False)
                npid, recs = ev.part(x, ctx, [10] * 5, 1000)
                for si in zero:
                    assert not any(r[0] == 'prod' and r[1] == si for r in recs)
                    assert ev.reg[npid].inv[si] == ev.reg[x].inv[si]
        assert m > 10
