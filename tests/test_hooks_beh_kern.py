"""Tests of the behavioural-hooks kernel and runner (src/hooks_beh_kern.py, src/hooks_beh_run.py): write semantics, the
conditional key draw, sham matching, seeding, class logging, short runs of every write mode, and the reproduction of the stored
hooks_w2 `open-max` rows with the legacy keys."""
import os, sys, json, gzip
import numpy as np
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import hooks_w2 as H
import hooks_beh as HB
import hooks_beh_kern as K
import hooks_beh_run as R


@pytest.fixture(scope='module')
def S():
    return R.setup()


def test_wfill_inplace_ignores_flags_and_origin():
    f = np.zeros(4, np.int64)
    a = H.fcode(1, 0, H.BEH, H.WRITTEN, 100 | (1 << 12))
    out = np.zeros(4, np.int64)
    nf, ev, inpl, rej = K.wfill(f, 0, a, out, 0)
    assert (nf, ev, inpl, rej) == (1, 0, 0, 0)
    f = out.copy()
    b = H.fcode(0, 0, H.BEH, H.COPIED, 100 | (2 << 12) | (1 << 14))          # same (tag, scope, key id): replaces in place
    nf, ev, inpl, rej = K.wfill(f, 1, b, out, 0)
    assert (nf, ev, inpl, rej) == (1, 0, 1, 0) and out[0] == b
    c = H.fcode(1, 0, H.BEH, H.WRITTEN, 101)                                    # another key id: appended
    f = out.copy()
    nf, ev, inpl, rej = K.wfill(f, 1, c, out, 0)
    assert nf == 2 and inpl == 0


def test_wfill_eviction_and_noevict():
    f = np.array([H.fcode(1, 0, H.BEH, H.WRITTEN, k) for k in (20, 21, 22, 23)], np.int64)
    new = H.fcode(1, 0, H.BEH, H.WRITTEN, 24)
    out = np.zeros(4, np.int64)
    nf, ev, inpl, rej = K.wfill(f, 4, new, out, 0)
    assert (nf, ev, rej) == (4, 1, 0) and out[0] == f[1] and out[3] == new               # FIFO
    nf, ev, inpl, rej = K.wfill(f, 4, new, out, 1)
    assert (nf, ev, rej) == (4, 0, 1) and list(out) == list(f)                              # rejected, list unchanged
    same = H.fcode(0, 0, H.BEH, H.WRITTEN, 22)
    nf, ev, inpl, rej = K.wfill(f, 4, same, out, 1)
    assert (inpl, rej) == (1, 0)                                                           # an in-place update is not an insertion


def test_hostile_keys_are_the_named_ones(S):
    KT = S.KT
    assert KT.keys[int(S.hostile[0])]['form'] == ('box', ('not', 'a'))
    assert KT.keys[int(S.hostile[1])]['form'] == ('box', 'a')
    assert S.prior_full[int(S.hostile[0])] > 0


def test_base_defaults_and_single_hook(S):
    names = S.Lx.names
    i = names.index('HOOK(0,C)'); j = names.index('HOOK(0,D)')
    assert S.b_def[i, 0] == 1 and S.b_def[j, 0] == 0 and S.b_def[i, 1] == -1
    assert S.b_multi[i] == 0 and S.b_multi[j] == 0
    k = [n for n in range(len(names)) if 'HOOK(0,C)' in names[n] and 'HOOK(0,D)' in names[n]]
    assert k and all(S.b_multi[x] == 1 for x in k[:20])


def test_conditional_draw_only_true_keys(S):
    """_draw returns a key whose truth is 1 and never a zero-prior key; frequencies follow the prior."""
    B = S.B; N = S.N
    ax, ay, (row, _) = B.play(*N['FairBot'], *N['FairBot'], full=True)
    tvrow = np.array([HB.key_true(k, S.KT.key_prog, row) for k in range(len(S.KT.keys))])
    assert tvrow[S.k_fair]                                         # box a is true of a cooperating FairBot partner
    np.random.seed(0)
    draws = [K._draw(tvrow, S.prior_full, False, -1, -1, 1.0) for _ in range(3000)]
    assert all(d >= 0 and tvrow[d] and S.prior_full[d] > 0 for d in draws)
    w = S.prior_full * tvrow
    p = w[S.k_fair] / w.sum()
    assert abs(np.mean([d == S.k_fair for d in draws]) - p) < 0.04
    hb = [K._draw(tvrow, S.prior_full, True, int(S.hostile[0]), int(S.hostile[1]), 10.0) for _ in range(3000)]
    assert np.mean([d == S.k_fair for d in hb]) > np.mean([d == S.k_fair for d in draws])    # box a is hostile-boosted


def test_sham_groups_match_size_and_applicability(S):
    KT = S.KT
    for k in KT.full_ids[:300]:
        grp = S.sham_list[S.sham_off[k]:S.sham_off[k + 1]]
        assert k in grp
        assert all(KT.keys[g]['size'] == KT.keys[k]['size'] and S.applic[g] == S.applic[k] for g in grp)


def test_legacy_seeding_equals_hooks_w2_founders(S):
    import hooks_w2_run as W2R
    c = R.CELLS['open-max']
    b1, f1 = R.founders(S, 3, 600, c)
    class M:
        mu = S.mu; b_tags = S.Lx.b_tags
    b2, f2 = W2R.founders(3, 600, M, None, False)
    assert list(b1) == list(b2) and f1 == f2


def test_behavioural_seeding_replaces_only_behaviour_keys(S):
    import hooks_w2_run as W2R
    c = R.CELLS['beh-max']
    b1, f1 = R.founders(S, 3, 600, c)
    b0, f0 = R.founders(S, 3, 600, R.CELLS['open-max'])
    assert list(b1) == list(b0)
    nb = 0
    for x, y in zip(f1, f0):
        assert len(x) == len(y)
        for fx, fy in zip(x, y):
            assert H.f_scope(fx) == H.f_scope(fy) and H.f_tag(fx) == H.f_tag(fy) and H.f_action(fx) == H.f_action(fy)
            if H.f_scope(fx) == H.BEH:
                nb += 1
                assert 10 <= H.f_key(fx) < len(S.KT.keys) and S.prior_full[H.f_key(fx)] > 0
            else:
                assert fx == fy
    assert nb > 100


def test_hostile_seeding_boost_changes_the_joint(S):
    n = 2000
    for cell in ('beh-max', 'beh-max-hostile'):
        pass
    b0, f0 = R.founders(S, 5, n, R.CELLS['beh-max'])
    b1, f1 = R.founders(S, 5, n, R.CELLS['beh-max-hostile'])
    h0, c0 = R.hostile_founded(S, b0, f0, 100, n // 100)
    h1, c1 = R.hostile_founded(S, b1, f1, 100, n // 100)
    assert c1.sum() > c0.sum()


def _tiny(name, **kw):
    c = dict(R.CELLS[name]); c.update(kw)
    R.CELLS['tiny-' + name] = c
    return 'tiny-' + name


@pytest.mark.parametrize('cell', ['beh-max', 'beh-max-noA', 'beh-max-hostile', 'beh-written-only', 'M5-sham', 'M-grudge-only',
                                  'M3d-thanks-noevict', 'M3a-thanks-noinherit', 'M4-late'])
def test_short_runs_every_mode(cell):
    name = _tiny(cell, N=20, I=4, gens=12, **({'log': 1} if cell == 'beh-max' else {}))
    row = R.run_one(name, 0)
    assert row['overflow'] == 0 and row['state_overflow'] == 0
    assert row['counters'][0] > 0
    if cell in ('beh-max', 'beh-max-noA', 'beh-max-hostile', 'beh-written-only', 'M5-sham'):
        assert row['counters'][17] > 0                              # behavioural writes happened
    if cell == 'M3d-thanks-noevict':
        assert row['counters'][4] == 0                              # no eviction ever
    if cell == 'M4-late':
        assert row['counters'][23] > 0 and row['counters'][1] + row['counters'][2] == 0     # no write inside generations 0-50
    if cell == 'beh-max':
        conv = np.array(row['conv'])
        assert conv[4].sum() > 0                                    # births logged
        assert sum(sum(r) for t in row['ts'] if t['cls'] for r in t['cls']) > 0


def test_class_logging_counts_individuals():
    name = _tiny('beh-max', N=20, I=4, gens=10, log=1)
    row = R.run_one(name, 1)
    for t in row['ts']:
        if t['cls'] is not None:
            assert np.array(t['cls']).sum() == 80                  # every individual has one class
            assert np.array(t['tab']).sum() == 80


def test_open_max_reproduces_stored_rows_short():
    """The legacy-keys cell (ancestry flags off, same law) reproduces the stored hooks_w2 rows draw for draw (island P(C,C),
    present types and held fills at every stored generation up to the run length)."""
    out = R.validate(1, gens=25)
    r = out[0]
    assert r['records_equal']['isl_pcc'] and r['records_equal']['types'] and r['records_equal']['held']
    assert r['records_equal']['n_checked'] >= 3
