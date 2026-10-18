"""Tests for hooks, Part W (src/hooks_w.py, src/hooks_w_kern.py, src/hooks_w_run.py).

The primitive's semantics, the conflict rule, equal node cost, fills checked (soundness: no fill lets a program
exploit a sound prover), inert = default-resolved, and the baseline reproducing stored runs."""
import os, sys, json
import numpy as np
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import hooks_w as H
import modal as M

ROOT = os.path.join(os.path.dirname(__file__), '..')
ALL = np.ones((4, 4), np.bool_)
NONE_ACTIVE = np.zeros((4, 4), np.bool_)


@pytest.fixture(scope='module')
def hk():
    return H.Lang(6, hooks=True)


@pytest.fixture(scope='module')
def pl():
    return H.Lang(6, hooks=False)


def spec(fills, tags, active=ALL, recency=0, ctx=-1):
    f = np.zeros(4, np.int64); f[:len(fills)] = fills
    return H.spec_of(f, len(fills), tags, active, recency, ctx)


def play(L, bx, sx, by, sy):
    """x vs y with each player's spec the same in every context (no history fills involved)."""
    a, b, _, _ = H.eval_match(*L.arrays(), L.iC, L.iD, bx, sx, sx, sx, by, sy, sy, sy)
    return a, b


def base(L, name):
    return L.names.index(name)


# ------------------------------------------------------------------ the primitive
def test_plain_grammar_and_evaluator_match_modal(pl):
    L0 = M.ModalLanguage(6)
    assert pl.L.n_programs == L0.n_programs == 1020
    val, _ = M.evaluate(L0)
    for i, cx in enumerate(pl.base):
        for j, cy in enumerate(pl.base):
            a, b = play(pl, i, 0, j, 0)
            assert a == val[cx, cy] and b == val[cy, cx]


def test_hook_defaults_and_fills(hk):
    hC, hD = base(hk, 'HOOK(0,C)'), base(hk, 'HOOK(0,D)')
    D, FB = hk.bD, hk.FB
    # defaults: HOOK(t, C) is ALLC, HOOK(t, D) is DefectBot
    assert play(hk, hC, 0, D, 0) == (1, 0)
    assert play(hk, hD, 0, FB, 0) == (0, 0)
    assert play(hk, hC, 0, FB, 0) == (1, 1)
    # a none-scope fill overrides the default
    sD = spec([H.fcode(0, 0, H.NONE, H.SEEDED, 0)], 1)
    sC = spec([H.fcode(1, 0, H.NONE, H.SEEDED, 0)], 1)
    assert play(hk, hC, sD, FB, 0) == (0, 0)
    assert play(hk, hD, sC, D, 0) == (1, 0)
    # a fill on a tag the program does not carry never applies
    assert spec([H.fcode(0, 1, H.NONE, H.SEEDED, 0)], 1) == 0
    # inert fills: the program plays its defaults
    assert spec([H.fcode(0, 0, H.NONE, H.SEEDED, 0)], 1, active=NONE_ACTIVE) == 0


def test_behaviour_key_reads_the_partner_class(hk):
    hC = base(hk, 'HOOK(0,C)')
    # DefectBot's class as read by anyone: never provably cooperates -> beta = 0; ALLC: beta = 7
    s0 = spec([H.fcode(0, 0, H.BEH, H.SEEDED, 0)], 1)          # defect against beta = 0
    assert play(hk, hC, s0, hk.bD, 0) == (0, 0)
    assert play(hk, hC, s0, hk.bC, 0) == (1, 1)
    s7 = spec([H.fcode(0, 0, H.BEH, H.SEEDED, 7)], 1)          # defect against beta = 7 (ALLC)
    assert play(hk, hC, s7, hk.bC, 0) == (0, 1)
    assert play(hk, hC, s7, hk.bD, 0) == (1, 0)


def test_history_key_applies_only_to_that_lineage(hk):
    hD = base(hk, 'HOOK(0,D)')
    f = np.zeros(4, np.int64); f[0] = H.fcode(1, 0, H.HIST, H.WRITTEN, 42)
    s_none = H.spec_of(f, 1, 1, ALL, 0, -1)
    s_42 = H.spec_of(f, 1, 1, ALL, 0, 42)
    s_7 = H.spec_of(f, 1, 1, ALL, 0, 7)
    assert s_none == 0 and s_7 == 0 and s_42 != 0
    # two HOOK(0, D) programs with mutual history C fills keyed on each other cooperate; as strangers they defect
    a, b, _, _ = H.eval_match(*hk.arrays(), hk.iC, hk.iD, hD, 0, s_42, 0, hD, 0, s_42, 0)
    assert (a, b) == (1, 1)
    assert play(hk, hD, s_none, hD, s_none) == (0, 0)


# ------------------------------------------------------------------ the conflict rule
def _value(sp, t, beta):
    m = (sp >> (16 * t)) & 0xFFFF
    return (m >> beta) & 1, (m >> (8 + beta)) & 1      # (applies, value)


def test_most_specific_scope_wins():
    fills = [H.fcode(1, 0, H.BEH, H.SEEDED, 3),           # oldest: behaviour, key 3, C
             H.fcode(0, 0, H.HIST, H.SEEDED, 5),          # history keyed 5, D
             H.fcode(1, 0, H.ROLE, H.SEEDED, 0),          # role, C
             H.fcode(0, 0, H.NONE, H.SEEDED, 0)]          # newest: none, D
    sp_stranger = spec(fills, 1, ctx=-1)
    sp_5 = spec(fills, 1, ctx=5)
    assert _value(sp_stranger, 0, 3) == (1, 1)           # behaviour beats everything at its key
    assert _value(sp_stranger, 0, 0) == (1, 1)           # role beats none (role is C, none is D)
    assert _value(sp_5, 0, 0) == (1, 0)                  # history beats role
    assert _value(sp_5, 0, 3) == (1, 1)                  # behaviour beats history
    # ties by recency within a scope
    two_none = [H.fcode(1, 0, H.NONE, H.SEEDED, 0), H.fcode(0, 0, H.NONE, H.SEEDED, 0)]
    assert _value(spec(two_none, 1), 0, 0) == (1, 0)


def test_recency_only_ablation():
    fills = [H.fcode(1, 0, H.BEH, H.SEEDED, 3), H.fcode(0, 0, H.NONE, H.SEEDED, 0)]
    assert _value(spec(fills, 1, recency=0), 0, 3) == (1, 1)
    assert _value(spec(fills, 1, recency=1), 0, 3) == (1, 0)      # the newer none fill wins


def test_write_fill_in_place_and_fifo():
    out = np.zeros(4, np.int64)
    f = np.array([H.fcode(1, 0, H.HIST, H.WRITTEN, 9), H.fcode(0, 0, H.NONE, H.SEEDED, 0), 0, 0], np.int64)
    n, ev, inp = H.write_fill(f, 2, H.fcode(0, 0, H.HIST, H.WRITTEN, 9), out)      # same (tag, scope, key)
    assert (n, ev, inp) == (2, 0, 1)
    assert out[0] == f[1] and out[1] == H.fcode(0, 0, H.HIST, H.WRITTEN, 9)
    full = np.array([H.fcode(1, 0, H.HIST, H.WRITTEN, k) for k in (1, 2, 3, 4)], np.int64)
    n, ev, inp = H.write_fill(full, 4, H.fcode(1, 0, H.HIST, H.WRITTEN, 5), out)
    assert (n, ev, inp) == (4, 1, 0)
    assert list(out) == [full[1], full[2], full[3], H.fcode(1, 0, H.HIST, H.WRITTEN, 5)]


# ------------------------------------------------------------------ equal node cost
def test_equal_node_cost(hk):
    L = hk.L
    assert L.a[1] == 6                                   # C, D and four one-node hook leaves
    m = {nm: hk.mu[base(hk, nm)] for nm in ('C', 'D', 'HOOK(0,C)', 'HOOK(0,D)', 'HOOK(1,C)', 'HOOK(1,D)')}
    # every hook leaf has the same mass whatever its tag or default (and so whatever scope later fills it)
    assert np.allclose([m['HOOK(0,C)'], m['HOOK(0,D)'], m['HOOK(1,C)'], m['HOOK(1,D)']], m['HOOK(0,C)'])
    # same node cost as a constant: mass differs from C only through the canonical function's other spellings
    assert m['HOOK(0,C)'] <= m['C']


# ------------------------------------------------------------------ fills are checked (soundness by construction)
def test_inert_equals_default_resolved(hk):
    rng = np.random.default_rng(0)
    for _ in range(3000):
        i, j = rng.integers(len(hk.base), size=2)
        a = play(hk, i, 0, j, 0)
        b = play(hk, hk.b_restrict[i], 0, hk.b_restrict[j], 0)
        assert a == b


def test_no_fill_exploits_a_sound_prover(hk):
    """Lemma 0 survives hooks: against FairBot and BOX1(THEM(ME)) no filled program gets (D, C)."""
    rng = np.random.default_rng(1)
    provers = [hk.FB, base(hk, 'BOX1(THEM(ME))')]
    hooked = [i for i in range(len(hk.base)) if hk.b_tags[i]]
    for _ in range(4000):
        x = hooked[rng.integers(len(hooked))]
        tags = [t for t in (0, 1) if (hk.b_tags[x] >> t) & 1]
        fl = []
        for _k in range(rng.integers(1, 5)):
            sc = int(rng.integers(4))
            key = 0 if sc < 2 else int(rng.integers(8))
            if sc == H.HIST:
                key = 5
            fl.append(H.fcode(int(rng.integers(2)), tags[rng.integers(len(tags))], sc, H.SEEDED, key))
        f = np.zeros(4, np.int64); f[:len(fl)] = fl
        s0 = H.spec_of(f, len(fl), hk.b_tags[x], ALL, 0, -1)
        s5 = H.spec_of(f, len(fl), hk.b_tags[x], ALL, 0, 5)      # the prover descends from founder 5
        for p in provers:
            a, b, _, _ = H.eval_match(*hk.arrays(), hk.iC, hk.iD, x, s0, s5, s0, p, 0, 0, 0)
            assert not (a == 0 and b == 1)


# ------------------------------------------------------------------ the baseline reproduces stored runs
@pytest.mark.skipif(not os.path.exists(os.path.join(ROOT, 'runs', 'almost-all-seeds-islands.json')), reason='stored rows')
def test_baseline_reproduces_stored_rows():
    import hooks_w_run as R
    out = R.validate(2)
    assert all(r['equal'] for r in out)
