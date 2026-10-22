"""Tests for the prudence run (notes/prudence.md §1.9).  Tests needing the untracked cached tables skip when absent."""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAVE_CACHE = os.path.exists(os.path.join(ROOT, 'runs', 'provenance', 'static', 'meta.pkl')) and \
    os.path.exists(os.path.join(ROOT, 'runs', 'detectors', 'K', 'static', 'meta.pkl')) and \
    os.path.exists(os.path.join(ROOT, 'runs', 'world_k', 'cells_C.json.gz'))
needs_cache = pytest.mark.skipif(not HAVE_CACHE, reason='cached tables absent')


def test_schedule_integrates_to_A():
    import prudence as P
    for A in (52, 156):
        lam = P.lam(A)
        assert abs(lam.sum() - A * P.NTOT / 100.0) < 1e-9            # delivered total = 128 A exactly
        eps = P.schedule(A)
        assert len(eps) == P.MERGE + P.TAIL
        assert (eps[:P.MERGE] == 0).all()
        assert abs((eps[P.MERGE:] * P.NTOT).sum() - A * P.NTOT / 100.0) < 1e-9
        assert (np.diff(eps[P.MERGE:]) < 0).all()                    # monotone annealing
    assert (P.schedule(0) == 0).all()
    # the annealing shape: 0.55 of the delivered total within the first 1,000 generations
    lam = P.lam(52)
    assert abs(lam[:1000].sum() / lam.sum() - 0.5501) < 1e-3
    # the delivered fraction of the infinite-horizon integral at 10,000 is >= 0.9 (amendment 2.1)
    w = P.arrival_weights()
    inf = P.T0 * 1.0                                                  # integral of (1 + t/t0)^-2 over [0, inf)
    assert w.sum() / inf >= 0.9


@needs_cache
def test_sd_set_and_depleted_prior():
    import world_k as WK
    import prudence as P
    sd = {}
    for w in P.WORLDS:
        LS = WK.use_world(w)
        S = P.sets(LS)
        sd[w] = S['SD'].copy()
        assert not (S['SD'] & S['Qsp']).any()                        # the former TwinD family is not removed
        cum = P.depleted_cumL(LS)
        inc = np.diff(np.concatenate([[0.0], cum]))
        assert (inc[S['SD']] == 0).all()
        assert np.allclose(inc[~S['SD']], LS['mu'][~S['SD']])
        assert abs(cum[-1] - (1 - LS['mu'][S['SD']].sum())) < 1e-12
        # a depleted draw never lands on a removed spelling (u = 0 and u = 1 included)
        for u in np.linspace(0, 1 - 1e-12, 4001):
            s = int(np.searchsorted(cum, u * cum[-1], side='right'))
            assert not S['SD'][s]
    assert (sd['L'] == sd['K']).all()                                # the same syntactic set in both worlds
    assert 4000 < sd['L'].sum() < 5000


@needs_cache
def test_target_sets_frozen_and_world_specific():
    import world_k as WK
    import prudence as P
    n = {}
    for w in P.WORLDS:
        LS = WK.use_world(w)
        S = P.sets(LS)
        n[w] = int(S['T'].sum())
        assert S['T'][S['uPB']]                                      # PrudentBot-H is in its own network
        assert not S['T'][S['dH']] and not S['T'][S['cH']]           # DefectBot-H and CooperateBot-H are not
        assert S['guard'][S['uPB']] and not S['guard'][S['cbH']]     # PrudentBot is guarded, FairBot is not
    assert n['L'] == 235                                             # the removing-rivals target
    assert n['K'] > n['L']                                           # certified suckers pass the K guard


@needs_cache
def test_arrival_kernel_equals_pangaea_kernel_at_eps0_and_lineage_and_pairing():
    import world_k as WK
    import pangaea as PG
    import prudence as P
    rep = 990
    LS = WK.use_world('L')
    # the Pangaea kernel alone
    R0 = PG.PGRun(P.FF_CELL, rep)
    while R0.g < P.MERGE: R0.advance(10)
    R0.merge(PG.kernel_seed_pg(R0.N * R0.I, 1, rep) ^ 0x5DEECE66D)
    R0.advance(40)
    # the prudence run at A = 0
    R1 = P.PruRun(rep, 'A0')
    while R1.g < P.MERGE: R1.advance(10)
    R1.do_merge()
    R1.advance(40)
    assert R1.g == R0.g == P.MERGE + 40
    assert (R1.slots == R0.slots).all() and (R1.counts[:, :R1.ntv[0]] == R0.counts[:, :R0.ntv[0]]).all()
    assert int(R1.ntv[0]) == int(R0.ntv[0])
    # arrivals: lineage conservation, uniqueness and the nested/paired streams
    out = {}
    for arm in ('A52', 'A156'):
        R = P.PruRun(rep, arm)
        while R.g < P.MERGE: R.advance(10)
        R.do_merge()
        R.advance(40)
        n = int(R.nfr[0])
        assert n == int(R.rcount[0]) == int(R.nlin[0]) > 100
        lids = R.fr[:n, 4]
        assert len(set(lids.tolist())) == n and lids.min() == 1 and lids.max() == n
        lin = R.lin[0]
        assert lin.max() <= n and ((lin > 0).sum() <= n)             # arrival-descended individuals <= arrivals so far
        assert R.counts[0, :R.ntv[0]].sum() == R.N
        # every arrival record's first column is a generation in the tail so far
        assert (R.fr[:n, 0] >= P.MERGE).all() and (R.fr[:n, 0] < R.g).all()
        out[arm] = (n, R.fr[:n, 2].copy())
    n52, sp52 = out['A52']; n156, sp156 = out['A156']
    assert 0.25 < n52 / n156 < 0.42                                  # about 1/3, binomial noise only
    assert (sp52 == sp156[:n52]).all()                               # the same founder sequence in the same order
    # the world changes nothing about the arriving spellings (K shares founders and fseed)
    LSK = WK.use_world('K')
    RK = P.PruRun(rep, 'A52')
    while RK.g < P.MERGE: RK.advance(10)
    RK.do_merge()
    RK.advance(40)
    nk = int(RK.nfr[0])
    m = min(nk, n52)
    assert (RK.fr[:m, 2] == sp52[:m]).all()
    WK.use_world('L')


@needs_cache
def test_a0_reproduces_stored_fission_fusion_row():
    import gzip
    import json
    import world_k as WK
    import pangaea as PG
    import prudence as P
    import prudence_run as PRUN
    rows = json.load(gzip.open(os.path.join(ROOT, 'runs/world_k/cells_C.json.gz')))
    rep = 0
    for w in P.WORLDS:
        LS = WK.use_world(w)
        st = [r for r in rows if r['cell'] == P.FF_CELL and r['world'] == w and r['rep'] == rep][0]
        ref = {t['g']: t for t in st['trace']}
        R = P.PruRun(rep, 'A0')
        n = 0
        while R.g < 400:
            R.advance(10)
            if R.g == P.MERGE: R.do_merge()
            dec = PG.decompose(R, R.island_stats(), closure=False)
            if R.g in ref:
                s = ref[R.g]
                n += 1
                assert (PRUN.r5(dec['pcc']), PRUN.r5(dec['M']), PRUN.r5(dec['target']), int(dec['n_types'])) == \
                    (s['pcc'], s['M'], s['target'], s['nt']), (w, R.g)
        assert n >= 35
