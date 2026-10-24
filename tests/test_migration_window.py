"""Tests for the migration-window experiment (spec specs/2026-10-24-migration-window.md, required tests): the
generated kernels reproduce the originals and the stored runs draw for draw at mN = 0 and mN = 1 (baseline, U-gKR(0.99),
gV), the target statistic on hand-built archipelagos, the independent-component reference formula, the passage-time
helpers, the control starts.

    python3 -m pytest tests/test_migration_window.py -q
"""
import itertools, json, os, sys
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import numpy as np
import stable_sets as SS
import farsighted_refusal as F
import farsighted_refusal_run as FR
import migration_window as MW

ROOT = SS.ROOT


def _stored(rel):
    return json.load(open(os.path.join(ROOT, rel)))['runs']


# ------------------------------------------------------------------ reference formula
def test_reference_formula():
    def enum(C):
        n = 0
        for t in itertools.product(range(3), repeat=C):
            n += len(set(t)) == 3
        return n / 3 ** C
    for C in (1, 2, 3, 4, 5, 8):
        assert abs(MW.p_all_three(C) - enum(C)) < 1e-12
    assert MW.p_all_three(1) == 0 and abs(MW.p_all_three(2)) < 1e-15
    assert abs(MW.p_all_three(4) - 4 / 9) < 1e-12
    assert abs(MW.p_all_three(8) - 0.8834) < 1e-3


# ------------------------------------------------------------------ the target statistic on hand-built archipelagos
def _find(cat_name, k=0):
    ids = [z for z in range(MW.NOUT) if MW.OLAB[z] == cat_name]
    return ids[k]


def _arch(outcomes, purity=1.0):
    """one-generation archipelago from a list of outcome ids; encounter mass `purity` on the outcome."""
    modal = np.array([outcomes], np.int8)
    eff = np.array([[purity if MW.CATMAP[o] <= 2 else 0.0 for o in outcomes]], np.float32)
    fair = np.array([[purity if MW.CATMAP[o] == 0 else 0.0 for o in outcomes]], np.float32)
    return modal, eff, fair


def test_target_handbuilt():
    F0, F1, F2 = MW.V
    U = _find('U'); W = _find('W'); Dd = _find('D'); Gc = _find('G')
    base = [F0] * 21 + [F1] * 21 + [F2] * 22
    s = MW.target_series(*_arch(base))
    assert s['ts'][0] and s['tv'][0] and s['hps'][0] and s['hpv'][0] and s['nm'][0] == 3
    # one wasteful island: neither target
    s = MW.target_series(*_arch(base[:-1] + [W]))
    assert not s['ts'][0] and not s['tv'][0] and s['waste'][0] == 1
    s = MW.target_series(*_arch(base[:-1] + [Dd]))
    assert not s['ts'][0] and not s['tv'][0]
    # one unequal island, all three fair pairs still present: stated target holds, V* does not
    s = MW.target_series(*_arch(base[:-1] + [U]))
    assert s['ts'][0] and not s['tv'][0] and s['nm'][0] == 3
    s = MW.target_series(*_arch(base[:-1] + [Gc]))
    assert s['ts'][0] and not s['tv'][0]
    # a fair pair missing: neither holds, even if every island is efficient
    s = MW.target_series(*_arch([F0] * 32 + [F1] * 31 + [U]))
    assert not s['ts'][0] and not s['tv'][0] and s['nm'][0] == 2
    s = MW.target_series(*_arch([F0] * 32 + [F1] * 32))
    assert not s['ts'][0] and not s['tv'][0]
    # the only copy of a fair pair replaced by an unequal pair
    s = MW.target_series(*_arch([F0] * 32 + [F1] * 31 + [U]))
    assert s['nm'][0] == 2
    # high purity: modal efficient but only 0.9 of the mass efficient everywhere
    s = MW.target_series(*_arch(base, purity=0.9))
    assert s['ts'][0] and s['tv'][0] and not s['hps'][0] and not s['hpv'][0]


def test_passage_helpers():
    a = np.array([0, 1, 1, 0, 1, 1, 1, 1, 0, 0], bool)
    assert MW.first_window(a, L=3) == 4
    assert MW.first_window(a, L=3, start=5) == 5
    assert MW.first_window(a, L=5) == -1
    assert MW.first_window(np.ones(3, bool), L=5) == -1
    assert MW.episodes(a) == [(1, 2), (4, 4)]


def test_analyse_passage_and_episodes():
    """a scripted archipelago: waste until g = 40, three members until g = 300, then one member everywhere."""
    F0, F1, F2 = MW.V
    W = _find('W')
    G = 400; I = 6
    modal = np.zeros((G + 1, I), np.int8)
    modal[:] = np.array([F0, F0, F1, F1, F2, F2])
    modal[:40, 0] = W
    modal[300:] = F0
    effm = np.where(MW.CATMAP[modal] <= 2, 1.0, 0.0).astype(np.float32)
    fairm = np.where(MW.CATMAP[modal] == 0, 1.0, 0.0).astype(np.float32)
    cls = modal.astype(np.int16)
    meta = dict(status=[4], stop=[G], nmig=0, nev=0)
    rec, _ = MW.analyse(dict(modal=modal, effm=effm, fairm=fairm, cls=cls), [(0, I)], meta, G)
    assert rec['t_clear'] == 40
    assert rec['g_est'] == 0                       # three members present at generation 0 (island 0 is wasteful, but
    # F0 is on island 1)
    assert rec['t_lost'] == 300
    assert rec['ep_ts']['first'] == 40 and rec['ep_ts']['cum'] == 260 and rec['ep_ts']['n'] == 1
    assert rec['ep_tv']['first'] == 40
    assert rec['last_waste'] == 39
    assert rec['snap']['0']['W'] == 1


# ------------------------------------------------------------------ founders and controls
def test_founders_prefix():
    a, _ = MW.founders('L1', 3, 128, 100)
    b, _ = MW.founders('L1', 3, 64, 100)
    c, _ = MW.founders('L1', 3, 16, 100)
    assert (a[:64] == b).all() and (a[:16] == c).all()


def test_controls_start_as_seeded():
    for kind, I in (('bal', 60), ('waste', 60)):
        init = MW.control_founders(kind, 'L1', 0, I, 100)
        loc, U = SS.compress(init)
        J = SS.joint_for('weak', U)
        out = MW.MK.kern_mw(J, MW.T.PAY, MW.T.VEC, MW.T.ISMEM, MW.T.TOT, loc, 100, SS.W, 0.0, 1, 2, 1,
                            np.zeros(0, np.int64), 100)
        modal = out[9][0]
        cats = MW.CATMAP[modal]
        if kind == 'bal':
            assert (cats == 0).all()
            assert sorted(np.bincount([MW.V.index(int(m)) for m in modal]).tolist()) == [20, 20, 20]
        else:
            assert (cats == 3).sum() == 15 and (cats == 0).sum() == 45
            assert sorted(np.bincount([MW.V.index(int(m)) for m in modal if MW.CATMAP[m] == 0]).tolist()) == [15, 15, 15]
        assert out[3][0].tolist() == modal.tolist()    # pure islands: the 0.95 class is the modal outcome


# ------------------------------------------------------------------ identity with the originals
def _small(sd, I=8, N=30, base='L1'):
    init, _ = MW.founders(base, sd, I, N)
    return init


def test_kern_identity_small():
    for mN in (0, 1):
        for sd in (0, 1):
            init = _small(sd)
            loc, U = SS.compress(init)
            J = SS.joint_for('weak', U)
            seed = 12345 + sd
            o = SS.kern(J, MW.T.PAY, MW.T.VEC, MW.T.ISMEM, MW.T.TOT, loc, 30, SS.W, mN / 30, seed, 400, 10,
                        np.zeros(0, np.int64), 2000000)
            n = MW.MK.kern_mw(J, MW.T.PAY, MW.T.VEC, MW.T.ISMEM, MW.T.TOT, loc, 30, SS.W, mN / 30, seed, 400, 10,
                              np.zeros(0, np.int64), 1000)
            assert o[0] == n[0] and o[1] == n[1] and o[8] == n[8] and o[7] == n[7]
            assert (o[3] == n[3]).all() and (o[2] == n[2]).all()
            # the added record is consistent with the original per-island classes: whenever the 0.95 class is an
            # outcome, it is the modal outcome
            cls = n[3]; modal = n[9]
            sel = cls < MW.NOUT
            assert (cls[sel] == modal[sel]).all()


def test_fkern_identity_small():
    for guards, g in ((['g0', 'gKR0.99'], 'gKR'), (['g0', 'gV'], 'gV')):
        for mN in (0, 1):
            init = _small(0)
            loc, U = SS.compress(init)
            st = F.Setup(loc, U, len(guards), assign=('bit', 1.0, 1), rng=None)
            ga = FR.guard_arrays(guards)
            seed = 777
            o = F.run_fkern(st, MW.T, 30, mN, seed, 300, np.zeros(0, np.int64), ga, nu=0.1, rec_every=50,
                            evcap=1000, cevcap=1000)
            n = MW.run_fkern_mw(st, 30, mN, seed, 300, np.zeros(0, np.int64), ga)
            assert o[0] == n['status'] and o[1] == n['stop'] and o[8] == n['nmig'] and o[7] == n['nev']
            assert (o[3] == n['cls']).all()
            assert [int(v) for v in o[11].sum(0)] == n['cnt']


# ------------------------------------------------------------------ the stored runs, draw for draw
def test_stored_baseline_mN0_and_mN1():
    for cell, mN, runs, H in (('L0', 0, (0, 1, 2), 10000), ('L1', 1, (0, 2), 10000)):
        stored = _stored('runs/stable_sets/%s.json' % cell)
        for r in runs:
            init, _ = MW.founders(cell, r, 64, 100)
            seed = MW.SR.run_seed(cell, r) % (2 ** 31)
            o = MW.run_comp('base', init, 100, mN, seed, H)
            s = stored[r]
            assert (o['status'], o['stop'], o['nmig'], o['nev']) == (s['status'], s['stop_gen'], s['nmig'], s['nev']), (cell, r)


def test_stored_guard_runs_mN1():
    for guard, cell in (('gKR', 'UKR99-1'), ('gV', 'R2r-1')):
        stored = _stored('runs/farsighted_refusal/%s.json' % cell)
        r = 0
        init, _ = MW.founders('L1', r, 64, 100)
        seed = MW.SR.run_seed('L1', r) % (2 ** 31)
        o = MW.run_comp(guard, init, 100, 1, seed, 10000)
        s = stored[r]
        assert (o['status'], o['stop'], o['nmig'], o['nev'], o['ncev']) == (s['status'], s['stop_gen'], s['nmig'], s['nev'], s['ncev']), cell
