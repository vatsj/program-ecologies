"""Validation of the encounter-contracts engine before any counted cell (writes runs/encounter-contracts-validate.json).

  1. nu = 0 reproduces many_islands.island_run draw for draw (founders, and founders with annealed arrivals).
  2. The exhaustive oracle against the Monte Carlo acceptance frequency of the genesis draws on hand-built islands and on settled
     islands of the arm-0 pool.
  3. Arm 0 of this engine (continuous-time migrants, rounds) against the stored many-islands chain (closed-form events) at the
     spec's checkpoints: the increments of V* and the dominated shares.
Run after the arm-0 validation pool (pool_0_nu0_I1024_R1000_p0_post_m0.001.json and its dump) exists.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import encounter_contracts as EC
import encounter_contracts_run as ER
import many_islands as MI
import stable_sets as SS
import dollar3 as D

OUT = os.path.join(EC.ROOT, 'runs')


def parity(n_founders=12, n_arrivals=6):
    arm = ER.get_arm(False)
    R = EC.Runner(arm, EC.make_P(nu=0.0))
    marm = MI.Arm('L'); marm.new_cache(22)
    rng = np.random.default_rng(2024)
    same = 0
    for trial in range(n_founders):
        init = np.stack([rng.multinomial(100, arm.laws[s]) for s in range(3)]).astype(np.int64)
        seed = 9000 + trial
        st0, g0, c0, _ = MI.island_run(marm.ctx(), marm.lc(32), MI.PAY, init, 100, MI.W, seed, 20002, np.empty(0), marm.cum, True)
        isl = R.init_island(init)
        st, g = R.run(isl, 20002, seed, 0.0)
        same += int((st, g) == (st0, g0) and np.array_equal(isl.counts_by_program(arm.K), c0))
    same_arr = 0
    for trial in range(n_arrivals):
        init = np.stack([rng.multinomial(100, arm.laws[s]) for s in range(3)]).astype(np.int64)
        arr = MI.arrival_times(rng, 20)
        seed = 9500 + trial
        H = int(arr[-1]) + 5002
        st0, g0, c0, na0 = MI.island_run(marm.ctx(), marm.lc(64), MI.PAY, init, 100, MI.W, seed, H, arr, marm.cum, True)
        isl = R.init_island(init)
        st, g = R.run(isl, H, seed, 0.0, xrows=[R.xrow(t, 0) for t in arr])
        same_arr += int((st, g) == (st0, g0) and np.array_equal(isl.counts_by_program(arm.K), c0))
    return dict(founders=n_founders, identical=same, with_arrivals=n_arrivals, identical_with_arrivals=same_arr)


def oracle_vs_mc(dump, n_islands=12, n_draws=30000):
    R, hooked = ER.make_runner('R', 1.0)
    pool = ER.load_pool(dump)
    rng = np.random.default_rng(5)
    idx = rng.choice(len(pool), size=n_islands, replace=False)
    rows = []
    act = np.arange(3); apos = np.arange(3)
    np.random.seed(11)
    for i in idx:
        isl = pool[i]
        out = EC.acceptance_profile(R, isl)
        pexp = float(out[:3].sum())
        stat = np.zeros(EC.ST_LEN, np.int64)
        for _ in range(n_draws):
            ST = tuple(a.copy() for a in isl.ST)
            R.arm.clear_c2()
            EC.genesis_attempt(R.A, R.arm.c1, R.arm.c2, ST, R.P, act.copy(), apos.copy(), 0, 100, stat, isl.trk.copy(), 0.0, False)
        acc = int(stat[EC.ST_ACC_S:EC.ST_ACC_S + 3].sum())
        sd = (max(pexp, 1e-12) * (1 - pexp) / n_draws) ** 0.5
        rows.append(dict(island=int(i), cls=int(isl.ST[11][EC.MI_CLS]), oracle=pexp, mc=acc / n_draws, z=(acc / n_draws - pexp) / sd if sd > 0 else 0.0,
                         skipped=bool(out[7] > 0.5)))
    return rows


def arm0_vs_stored(poolfile):
    r = json.load(open(poolfile))
    d = json.load(open(os.path.join(EC.ROOT, 'runs', 'many-islands.json')))['L A=0']['traj']
    rows = []
    for rd in ('1', '10', '100', '300', '1000'):
        c = [c for c in r['checkpoints'] if c['round'] == int(rd)]
        if not c:
            continue
        c = c[0]
        n = max(c['n_settled'], 1)
        rows.append(dict(round=int(rd), vstar_engine=c['vstar_settled'], vstar_stored=d['Vstar'][rd][0],
                         vstar_stored_ci=[d['Vstar'][rd][1], d['Vstar'][rd][2]],
                         U_engine=c['settled']['U'] / n, U_stored=d['U'][rd][0], W_engine=c['settled']['W'] / n, W_stored=d['W'][rd][0],
                         D_engine=c['settled']['D'] / n, D_stored=d['D'][rd][0]))
    c0 = r['checkpoints'][0]
    rows0 = dict(vstar_round0_engine=c0['vstar_settled'], stored_post_anneal=json.load(open(os.path.join(EC.ROOT, 'runs', 'many-islands.json')))['L A=0']['post']['Vstar'][0])
    return rows, rows0


def main():
    pf = os.path.join(EC.ROOT, 'runs', 'encounter_contracts', 'pool_0_nu0_I1024_R1000_p0_post_m0.001.json')
    dump = os.path.join(ER.SCRATCH, 'pool_0_nu0_I1024_R1000_p0_post_m0.001_r1000.npz')
    res = dict(parity=parity(), oracle_vs_mc=oracle_vs_mc(dump))
    rows, rows0 = arm0_vs_stored(pf)
    res['arm0_vs_stored'] = rows
    res['arm0_round0'] = rows0
    with open(os.path.join(OUT, 'encounter-contracts-validate.json'), 'w') as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res, indent=1)[:3000])


if __name__ == '__main__':
    main()
