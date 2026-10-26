"""Drivers for the encounter-contracts experiment (spec specs/2026-10-25-encounter-contracts.md; notes notes/encounter-contracts.md).

    python3 src/encounter_contracts_run.py pool ARM NU I ROUNDS REP START [MN]   # island archipelago, migrants at mN per slot per generation
    python3 src/encounter_contracts_run.py within ARM NU I GENS REP              # no-migrant long runs (the strict-limit object)
    python3 src/encounter_contracts_run.py paired ARM NU REP N_EVENTS            # paired migrant / no-migrant branches (kappa, alpha)
    python3 src/encounter_contracts_run.py oracle ARM NU REP                     # exhaustive contract-stability oracle on a pool dump
One job per process.  Scratch dumps (npz) go outside the repository (EC_SCRATCH); small summaries (json) to runs/encounter_contracts/.

Arms: '0' (nu = 0), 'R', 'NR', 'BR', 'BRx', 'B', 'S', 'Slow', 'C', 'R16', and, on the hooked grammar, 'H', 'Htop', 'Hinert'.
"""
import json, os, sys, time, zlib, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from numba import njit
import encounter_contracts as EC
import many_islands as MI

ROOT = EC.ROOT
OUT = os.path.join(ROOT, 'runs', 'encounter_contracts')
SCRATCH = os.environ.get('EC_SCRATCH', os.path.join('/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad', 'ec_dumps'))
os.makedirs(OUT, exist_ok=True)
os.makedirs(SCRATCH, exist_ok=True)
N0 = EC.N0
NOUT = EC.NOUT
RELAX = 2000                                   # generations of founding relaxation (genesis on, no migrants) before event 0
CHECKPOINTS = (1, 3, 10, 30, 100, 300, 1000)

_ARMS = {}


def crc(s):
    return zlib.crc32(s.encode()) & 0x7fffffff


def arm_cfg(name, nu, N=N0):
    """(hooked grammar?, make_P kwargs)"""
    kw = dict(N=N, nu=nu)
    hooked = False
    if name == '0':
        kw['nu'] = 0.0
    elif name == 'R':
        pass
    elif name == 'NR':
        kw['acc'] = EC.ACC_NR
    elif name == 'BR':
        kw['acc'] = EC.ACC_BR
    elif name == 'BRx':
        kw['acc'] = EC.ACC_BR; kw['exe'] = EC.EXE_BR
    elif name == 'B':
        kw['bcast'] = 9
    elif name in ('S', 'Slow'):
        kw['filt'] = 0
    elif name == 'C':
        kw['copy'] = 0.5
    elif name == 'R16':
        kw['cap'] = 16
    elif name == 'H':
        kw['hook'] = EC.HOOK_H; hooked = True
    elif name == 'Htop':
        kw['hook'] = EC.HOOK_TOP; hooked = True
    elif name == 'Hinert':
        kw['nu'] = 0.0; hooked = True
    elif name == 'Rh':                         # R on the hooked grammar (every program wrapped at the top: = Htop without the hooks' special role)
        kw['hook'] = EC.HOOK_TOP; hooked = True
    else:
        raise ValueError(name)
    return hooked, kw


def get_arm(hooked):
    key = 'H' if hooked else 'L'
    if key not in _ARMS:
        _ARMS[key] = EC.CArm(hooked=hooked)
    return _ARMS[key]


def make_runner(name, nu, N=N0, nu_override=None):
    hooked, kw = arm_cfg(name, nu, N)
    if nu_override is not None:
        kw['nu'] = nu_override
    arm = get_arm(hooked)
    return EC.Runner(arm, EC.make_P(**kw)), hooked


# ====================================================================== island summaries
@njit(cache=True)
def summary(A, C1, C2, ST, P, N, out):
    """out[0:3] mean stage-2 payoff per slot (sixths), out[3] total, out[4:4+NOUT] encounter distribution over outcomes (stage 2),
    out[4+NOUT:4+2*NOUT] the same for the override-free stage-1 play, out[4+2*NOUT] the share of encounters in which a contract
    fires (stage-2 profile differs from stage 1)."""
    cnt = ST[0]; tprog = ST[1]; pres = ST[6]; npres = ST[7]
    VECt = A[9]; PAYi = A[8]
    N3 = float(N) ** 3
    for i in range(out.shape[0]):
        out[i] = 0.0
    for i0 in range(npres[0]):
        a = pres[0, i0]
        for i1 in range(npres[1]):
            b = pres[1, i1]
            for i2 in range(npres[2]):
                c = pres[2, i2]
                code = EC.tcode(A, C1, C2, ST, P, a, b, c)
                p1 = EC.stage1(A, C1, tprog[0, a], tprog[1, b], tprog[2, c])
                w = cnt[0, a] * cnt[1, b] * cnt[2, c] / N3
                for s in range(3):
                    out[s] += w * PAYi[code, s]
                out[3] += w * (PAYi[code, 0] + PAYi[code, 1] + PAYi[code, 2])
                out[4 + VECt[code]] += w
                out[4 + NOUT + VECt[p1]] += w
                if code != p1:
                    out[4 + 2 * NOUT] += w


MV = np.array(MI.V, np.int64)
OUTCOME_VEC = np.array([list(x) for x in MI.X], np.float64)           # payoffs of the 20 realizable outcomes (units of g)


def pareto_dominated(u, g=6.0):
    """is the island's expected payoff vector u (sixths) Pareto-dominated by some realizable outcome?"""
    X = OUTCOME_VEC
    ge = (X >= u - 1e-9).all(axis=1)
    gt = (X > u + 1e-9).any(axis=1)
    return bool((ge & gt).any())


def class_label(c):
    if c < 0:
        return 'none'
    if c < NOUT:
        return MI.OLAB[c]
    return 'member-mixed' if c == NOUT else 'other'


def pool_stats(R, pool):
    """per-checkpoint statistics of the pool: instantaneous and settled class histograms, categories, V* shares, payoffs."""
    A = R.A; arm = R.arm
    arm.clear_c2()
    I = len(pool)
    cur = np.zeros(I, np.int64); sett = np.zeros(I, np.int64)
    out = np.zeros(5 + 2 * NOUT)
    pay = np.zeros((I, 4)); dom = np.zeros(I, bool)
    fire = np.zeros(I); s1fair = np.zeros(I); s2fair = np.zeros(I)
    hk = arm.hk
    hooked_prog = np.array([[hk[s, x].max() >= 0 for x in range(arm.K)] for s in range(3)]) if arm.hooked else None
    hshare = np.zeros(I)
    ntypes = np.zeros(I, np.int64)
    for i, isl in enumerate(pool):
        ST = isl.ST
        cur[i] = ST[11][EC.MI_CLS]; sett[i] = ST[11][EC.MI_SETTLED]
        ntypes[i] = ST[7].sum()
        if i % 64 == 0:
            arm.clear_c2()
        summary(A, arm.c1, arm.c2, ST, R.P, int(R.P[EC.P_N]), out)
        pay[i, :3] = out[:3]; pay[i, 3] = out[3]
        dom[i] = pareto_dominated(out[:3])
        fire[i] = out[4 + 2 * NOUT]
        if hooked_prog is not None:
            cnt_, tprog_, pres_, npres_ = ST[0], ST[1], ST[6], ST[7]
            tot = 0.0
            for s_ in range(3):
                for j in range(npres_[s_]):
                    t_ = pres_[s_, j]
                    if hooked_prog[s_, tprog_[s_, t_]]:
                        tot += cnt_[s_, t_]
            hshare[i] = tot / (3.0 * int(R.P[EC.P_N]))
        s2fair[i] = out[4 + MV].sum(); s1fair[i] = out[4 + NOUT + MV].sum()
    return cur, sett, pay, dom, ntypes, (fire, s1fair, s2fair, hshare if hooked_prog is not None else None)


def cat_counts(cls):
    """histogram of categories F0 F1 F2 U G W D mixed/other none from class ids."""
    h = dict(F0=0, F1=0, F2=0, U=0, G=0, W=0, D=0, mixed=0, none=0)
    for c in cls:
        if c < 0:
            h['none'] += 1
        elif c < NOUT:
            cat = int(MI.CATMAP[c])
            if cat == 0:
                h['F%d' % MI.V.index(c)] += 1
            else:
                h[['F', 'U', 'G', 'W', 'D'][cat]] += 1
        else:
            h['mixed'] += 1
    return h


def checkpoint_record(R, pool, rnd, wall):
    cur, sett, pay, dom, ntypes, fs = pool_stats(R, pool)
    fire, s1fair, s2fair, hshare = fs
    I = len(pool)
    rec = dict(round=rnd, wall=wall, I=I)
    rec['cur'] = cat_counts(cur)
    rec['settled'] = cat_counts(sett)
    ok = sett >= 0
    rec['n_settled'] = int(ok.sum())
    rec['cur_hist'] = np.bincount(np.clip(cur, 0, NOUT + 1), minlength=NOUT + 2).tolist()
    rec['settled_hist'] = np.bincount(np.clip(sett[ok], 0, NOUT + 1), minlength=NOUT + 2).tolist()
    rec['mean_total_sixths'] = float(pay[:, 3].mean())
    rec['mean_pay_sixths'] = pay[:, :3].mean(axis=0).tolist()
    rec['pareto_dominated_share'] = float(dom.mean())
    rec['ntypes_mean'] = float(ntypes.mean()); rec['ntypes_max'] = int(ntypes.max())
    if hshare is not None:
        rec['hooked_share'] = float(hshare.mean())
    # on islands whose settled class is a fair pair: how much of the fair play is override-dependent (stage 2 fair, stage 1 not)
    fair_s = np.array([(0 <= c < NOUT and int(MI.CATMAP[c]) == 0) for c in sett])
    if fair_s.any():
        rec['fair_islands'] = dict(n=int(fair_s.sum()), mean_firing_mass=float(fire[fair_s].mean()),
                                   stage1_fair_mass=float(s1fair[fair_s].mean()), stage2_fair_mass=float(s2fair[fair_s].mean()),
                                   share_override_dependent=float((s1fair[fair_s] < 0.5).mean()))
    h = rec['cur']
    rec['vstar_cur'] = (h['F0'] + h['F1'] + h['F2']) / I
    hs = rec['settled']
    n = max(ok.sum(), 1)
    rec['vstar_settled'] = (hs['F0'] + hs['F1'] + hs['F2']) / n
    rec['WD_cur'] = (h['W'] + h['D']) / I
    rec['WD_settled'] = (hs['W'] + hs['D']) / n
    return rec


# ====================================================================== founding
def found_island(R, group, N, rep, i, relax=RELAX, tag=''):
    arm = R.arm
    rng = np.random.default_rng(crc('ec-found|%s|%d|%d|%d' % (group, N, rep, i)))
    init = np.stack([rng.multinomial(N, arm.laws[s]) for s in range(3)]).astype(np.int64)
    isl = R.init_island(init)
    seed = crc('ec-kern|%s|%d|%d|%d|%s' % (group, N, rep, i, tag))
    R.run(isl, relax, seed, 0.0, island_id=-1 - i)
    return isl


def aggregate_events(rows, N, agg):
    """rows: list of tracked-bundle records (island, formed_gen, smask, cat, p, f0..f2, max0..2, life0..2, simult, alive, setcat,
    copied, endgen, gain0..2) -> running aggregates by (|S|, category)."""
    if not rows:
        return
    a = np.array(rows)
    smask = a[:, 2].astype(int); cat = a[:, 3].astype(int)
    k = (smask & 1) + ((smask >> 1) & 1) + ((smask >> 2) & 1)
    mx = a[:, 8:11]; life = a[:, 11:14]
    mem = np.stack([(smask >> s) & 1 for s in range(3)], axis=1).astype(bool)
    both = np.all(np.where(mem, mx * 2 > N, True), axis=1)            # each signer's half exceeds half its slot at some time
    simult = a[:, 14] > 0.5
    gains = a[:, 19:22]
    # coordination class at formation: some half underdominant alone (gain < 0), else independently non-negative
    coord = np.any(np.where(mem, gains < -1e-9, False), axis=1)
    anypos = np.any(np.where(mem, gains > 1e-9, False), axis=1)
    copied = a[:, 17] > 0.5
    for kk in (1, 2, 3):
        for c in range(7):
            m = (k == kk) & (cat == c)
            if not m.any():
                continue
            key = '%d|%d' % (kk, c)
            d = agg.setdefault(key, dict(n=0, both=0, simult=0, coord=0, anypos=0, copied=0, alive_end=0, life_sum=np.zeros(3), life_n=0, lifes=[],
                                         both_coord=0, both_free=0, coord_alive=0))
            d['n'] += int(m.sum()); d['both'] += int(both[m].sum()); d['simult'] += int(simult[m].sum())
            d['coord'] += int(coord[m].sum()); d['anypos'] += int(anypos[m].sum()); d['copied'] += int(copied[m].sum())
            d['both_coord'] += int((both[m] & coord[m]).sum()); d['both_free'] += int((both[m] & ~coord[m]).sum())
            d['alive_end'] += int((a[m, 15] > 0.5).sum())
            # lifetime of the signer halves (generations), kept as a bounded sample
            if len(d['lifes']) < 20000:
                d['lifes'].extend(np.where(mem[m], life[m], np.nan).tolist()[:max(0, 20000 - len(d['lifes']))])


def finalize_agg(agg):
    out = {}
    for key, d in agg.items():
        L = np.array(d['lifes']) if d['lifes'] else np.zeros((0, 3))
        out[key] = dict(n=d['n'], n_both_fix=d['both'], n_both_coord=d['both_coord'], n_both_free=d['both_free'], n_coord=d['coord'],
                        frac_both_fix=d['both'] / d['n'], frac_simult=d['simult'] / d['n'], frac_coord=d['coord'] / d['n'],
                        frac_anypos=d['anypos'] / d['n'], frac_copied=d['copied'] / d['n'], frac_alive_2000=d['alive_end'] / d['n'],
                        life_median=[float(np.nanmedian(L[:, s])) if np.isfinite(L[:, s]).any() else None for s in range(3)],
                        life_mean=[float(np.nanmean(L[:, s])) if np.isfinite(L[:, s]).any() else None for s in range(3)])
    return out


# ====================================================================== the pool (islands with rare migration)
def donor_individual(rng, isl, s):
    ST = isl.ST
    cnt, tprog, tn, tkey, tfil, tbun, pres, npres = ST[:8]
    n = int(npres[s])
    ts = pres[s, :n]
    w = cnt[s, ts].astype(float)
    if n == 1:
        t = int(ts[0])
    else:
        t = int(rng.choice(ts, p=w / w.sum()))
    ent = [(int(tkey[s, t, e]), int(tfil[s, t, e]), int(tbun[s, t, e])) for e in range(int(tn[s, t]))]
    return int(tprog[s, t]), ent


def run_pool(armname, nu, I, rounds, rep, start='post', mN=1e-3, N=N0, nu_override=None, checkpoints=CHECKPOINTS, name=None, dump_at=(),
             log=None, extra=None):
    R, hooked = make_runner(armname, nu, N, nu_override)
    group = 'H' if hooked else 'L'
    t0 = time.time()
    # founding library
    lib_n = I if start == 'post' else 2 * I
    lib = []
    for i in range(lib_n):
        lib.append(found_island(R, group, N, rep, i, tag=armname))
        if log and i % 128 == 127:
            print('%s: founded %d/%d, %.0f s' % (name, i + 1, lib_n, time.time() - t0), file=log, flush=True)
    rng = np.random.default_rng(crc('ec-pool|%s|%g|%d|%s|%g' % (armname, nu, rep, start, mN)))
    if start != 'post':
        cur = np.array([isl.ST[11][EC.MI_CLS] for isl in lib])
        cat = np.array([int(MI.CATMAP[c]) if 0 <= c < NOUT else 9 for c in cur])
        w = np.ones(len(lib))
        if start == 'tiltF0':
            w[cur == MI.V[0]] = 6.0
        elif start == 'tiltU':
            w[cat == 1] = 6.0
        elif start == 'tiltD':
            w[(cat == 3) | (cat == 4)] = 6.0
        idx = rng.choice(len(lib), size=I, replace=True, p=w / w.sum())
        pool = [lib[j].copy() for j in idx]
    else:
        pool = lib
    del lib
    Hr = max(1, int(round(1.0 / (3.0 * mN))))               # generations per round: one migrant per island on average
    lam = 3.0 * mN * Hr
    recs = [checkpoint_record(R, pool, 0, time.time() - t0)]
    orc0 = oracle_summary(R, pool)
    abs_g = float(RELAX)
    agg = {}
    cev_all = []
    ev_buf = []
    cps = sorted(set(checkpoints))
    next_cp = 0
    dumped = {}
    R.stat[:] = 0
    R.statf[:] = 0
    stat_cp = []
    for r in range(1, rounds + 1):
        order = rng.permutation(I)
        for i in order:
            isl = pool[i]
            n = rng.poisson(lam)
            xrows = []
            if n:
                times = np.sort(rng.random(n)) * Hr
                for tt in times:
                    j = int(rng.integers(I - 1))
                    if j >= i: j += 1
                    s = int(rng.integers(3))
                    prog, ent = donor_individual(rng, pool[j], s)
                    xrows.append(R.xrow(tt, 1, slot=s, prog=prog, entries=ent))
            seed = crc('ec-run|%s|%g|%d|%s|%d|%d' % (armname, nu, rep, start, r, int(i)))
            R.run(isl, Hr, seed, abs_g, xrows=xrows, island_id=int(i))
            if R.events:
                ev_buf.extend(R.events); R.events = []
            if R.cevents:
                cev_all.extend(R.cevents); R.cevents = []
        abs_g += Hr
        if len(ev_buf) > 20000:
            aggregate_events(ev_buf, N, agg); ev_buf = []
        if next_cp < len(cps) and r == cps[next_cp]:
            next_cp += 1
            rec = checkpoint_record(R, pool, r, time.time() - t0)
            rec['genesis_stat'] = R.stat.tolist(); rec['genesis_statf'] = R.statf.tolist()
            recs.append(rec)
            if log:
                print('%s: round %d: V* settled %.3f cur %.3f WD %.3f  wall %.0f s' % (name, r, rec['vstar_settled'], rec['vstar_cur'], rec['WD_cur'], time.time() - t0), file=log, flush=True)
        if r in dump_at:
            dump_pool(pool, name, r)
    aggregate_events(ev_buf, N, agg)
    cev = np.array(cev_all) if cev_all else np.zeros((0, 9))
    np.save(os.path.join(SCRATCH, '%s_cev.npy' % name), cev)
    res = dict(arm=armname, nu=nu, I=I, rounds=rounds, rep=rep, start=start, mN=mN, N=N, round_gens=Hr, relax=RELAX, hooked=hooked,
               checkpoints=recs, bundles=finalize_agg(agg), wall=time.time() - t0,
               cev_summary=cev_summary(cev, I), genesis_stat=R.stat.tolist(), genesis_statf=R.statf.tolist(),
               oracle_round0=orc0, oracle_final=oracle_summary(R, pool))
    if extra:
        res.update(extra)
    return res, pool, R


def oracle_summary(R, pool, maxprod=64):
    """exhaustive contract-stability oracle on every island of the pool, by the island's current class category: the exact
    acceptance probability per genesis draw by |S| (frequency-weighted over the present type triples), the share of islands with no
    improving contract at all (contract-stable), and the number skipped (too many type triples)."""
    cats = {}
    for isl in pool:
        c = int(isl.ST[11][EC.MI_CLS])
        if c < 0: key = 'none'
        elif c < NOUT:
            k = int(MI.CATMAP[c]); key = 'F' if k == 0 else ['F', 'U', 'G', 'W', 'D'][k]
        else: key = 'M'
        out = EC.acceptance_profile(R, isl, maxprod)
        d = cats.setdefault(key, dict(n=0, skipped=0, stable=0, mass=np.zeros(3), counts=np.zeros(3)))
        d['n'] += 1
        if out[7] > 0.5:
            d['skipped'] += 1
            continue
        d['mass'] += out[:3]; d['counts'] += out[3:6]
        if out[3:6].sum() == 0:
            d['stable'] += 1
    res = {}
    for k, d in cats.items():
        m = max(d['n'] - d['skipped'], 1)
        res[k] = dict(n=d['n'], skipped=d['skipped'], contract_stable_share=d['stable'] / m,
                      mean_accept_prob_by_S=(d['mass'] / m).tolist(), mean_accept_prob=float(d['mass'].sum() / m),
                      mean_improving_proposals_by_S=(d['counts'] / m).tolist())
    return res


def cev_summary(cev, I):
    """transition counts of settled-class changes by (old category, new category) and attribution proxies."""
    if len(cev) == 0:
        return dict(n=0)
    old = cev[:, 2].astype(int); new = cev[:, 3].astype(int)
    t = cev[:, 1]; lm = cev[:, 4]; la = cev[:, 5]; since = cev[:, 6]
    def cat(c):
        if c < 0: return 'none'
        if c < NOUT:
            k = int(MI.CATMAP[c]); return ['F', 'U', 'G', 'W', 'D'][k]
        return 'M'
    def pair(c):
        if 0 <= c < NOUT and int(MI.CATMAP[c]) == 0:
            return MI.V.index(c)
        return -1
    trans = {}
    pt = {}
    for o, n_, tt, m, a, sc in zip(old, new, t, lm, la, since):
        k = '%s>%s' % (cat(o), cat(n_))
        d = trans.setdefault(k, dict(n=0, migrant_window=0, fresh_contract=0))
        d['n'] += 1
        tc = sc                                             # time the class started (the change itself, 500 generations before settling)
        if 0 <= tc - m <= 1500:
            d['migrant_window'] += 1
        if a > m and 0 <= tc - a <= 3000:
            d['fresh_contract'] += 1
        po, pn = pair(o), pair(n_)
        if po >= 0 and pn >= 0:
            pt['F%d>F%d' % (po, pn)] = pt.get('F%d>F%d' % (po, pn), 0) + 1
    return dict(n=int(len(cev)), trans=trans, fair_pair_trans=pt)


def dump_pool(pool, name, rnd):
    arrs = {}
    for k, nm in enumerate(('cnt', 'tprog', 'tn', 'tkey', 'tfil', 'tbun', 'pres', 'npres', 'pos', 'ser', 'F', 'mi', 'mf')):
        arrs[nm] = np.stack([isl.ST[k] for isl in pool])
    arrs['trk'] = np.stack([isl.trk for isl in pool])
    np.savez_compressed(os.path.join(SCRATCH, '%s_r%d.npz' % (name, rnd)), **arrs)


def load_pool(path):
    z = np.load(path)
    names = ('cnt', 'tprog', 'tn', 'tkey', 'tfil', 'tbun', 'pres', 'npres', 'pos', 'ser', 'F', 'mi', 'mf')
    arrs = {nm: z[nm] for nm in names}
    trk = z['trk']
    I = arrs['cnt'].shape[0]
    pool = []
    for i in range(I):
        ST = tuple(np.ascontiguousarray(arrs[nm][i]) for nm in names)
        pool.append(EC.Island(ST, np.ascontiguousarray(trk[i])))
    return pool


# ====================================================================== within-island long runs (no migrants)
def run_within(armname, nu, I, gens, rep, N=N0, chunk=20000, log=None, name='within'):
    R, hooked = make_runner(armname, nu, N)
    group = 'H' if hooked else 'L'
    t0 = time.time()
    per = []
    trans = {}
    agg = {}
    statf_tot = np.zeros(EC.STF_LEN)
    stat_tot = np.zeros(EC.ST_LEN, np.int64)
    for i in range(I):
        isl = found_island(R, group, N, rep, i, tag=armname)
        R.statf[:] = 0
        stat_before = R.stat.copy()
        R.cevents = []
        g = float(RELAX)
        n_ch = 0
        while g < RELAX + gens:
            R.run(isl, chunk, crc('ec-within|%s|%g|%d|%d|%d' % (armname, nu, rep, i, int(g))), g, island_id=i)
            g += chunk
        gen_c = R.statf[:7].copy(); gen_sc = R.statf[7:14].copy()
        statf_tot += R.statf
        stat_tot += R.stat - stat_before
        cev = np.array(R.cevents) if R.cevents else np.zeros((0, 9))
        per.append(dict(i=i, gen_cur=gen_c.tolist(), gen_settled=gen_sc.tolist(), n_changes=int(len(cev)), final=int(isl.ST[11][EC.MI_SETTLED])))
        for row in cev:
            o, n_ = int(row[2]), int(row[3])
            def lab(c):
                if c < 0: return 'none'
                if c < NOUT:
                    k_ = int(MI.CATMAP[c])
                    return ('F%d' % MI.V.index(c)) if k_ == 0 else ['F', 'U', 'G', 'W', 'D'][k_]
                return 'M'
            k = '%s>%s' % (lab(o), lab(n_))
            trans[k] = trans.get(k, 0) + 1
        if R.events:
            aggregate_events(R.events, N, agg); R.events = []
        if log and i % 20 == 19:
            print('%s: island %d/%d %.0f s' % (name, i + 1, I, time.time() - t0), file=log, flush=True)
    gc = np.array([p['gen_cur'] for p in per]); gs = np.array([p['gen_settled'] for p in per])
    res = dict(arm=armname, nu=nu, I=I, gens=gens, rep=rep, N=N, wall=time.time() - t0,
               gen_cur_total=gc.sum(axis=0).tolist(), gen_settled_total=gs.sum(axis=0).tolist(),
               changes_total=int(sum(p['n_changes'] for p in per)), transitions=trans, bundles=finalize_agg(agg),
               genesis_stat=stat_tot.tolist(), genesis_statf=statf_tot.tolist(), per_island=per)
    return res


# ====================================================================== paired migrant / no-migrant branches
def run_paired(armname, nu, dump, n_kappa, n_general, window=1500, seed0=0, N=N0, log=None, name='paired', abs_g0=None):
    """From a pool dump: for each event a recipient island, a donor island (for the kappa/alpha set, a fair-pair recipient of pair a and
    a donor from a different fair pair b), a slot and a donor individual; run the recipient for `window` generations with and without
    the migrant on the same seed (common random numbers) and record the class at the end of both branches."""
    R, hooked = make_runner(armname, nu, N)
    pool = load_pool(dump)
    I = len(pool)
    cls = np.array([isl.ST[11][EC.MI_CLS] for isl in pool])
    idx_by_pair = [np.nonzero(cls == MI.V[k])[0] for k in range(3)]
    rng = np.random.default_rng(crc('ec-paired|%s|%g|%d' % (armname, nu, seed0)))
    t0 = time.time()
    recs = []
    base_g = float(abs_g0 if abs_g0 is not None else max(isl.ST[12][EC.MF_LASTTOUCH] for isl in pool))
    for e in range(n_kappa + n_general):
        general = e >= n_kappa
        if not general:
            ok = [k for k in range(3) if len(idx_by_pair[k]) > 0]
            a = int(rng.choice(ok))
            others = [k for k in ok if k != a]
            if not others:
                continue
            b = int(rng.choice(others))
            i = int(rng.choice(idx_by_pair[a])); j = int(rng.choice(idx_by_pair[b]))
        else:
            i = int(rng.integers(I)); j = int(rng.integers(I - 1))
            if j >= i: j += 1
            a = -1; b = -1
        s = int(rng.integers(3))
        prog, ent = donor_individual(rng, pool[j], s)
        tm = float(rng.random() * 100.0)
        sd = crc('ec-paired-run|%s|%g|%d|%d' % (armname, nu, seed0, e))
        A_ = pool[i].copy(); B_ = pool[i].copy()
        R.run(A_, window, sd, base_g, island_id=i)
        R.run(B_, window, sd, base_g, xrows=[R.xrow(tm, 1, slot=s, prog=prog, entries=ent)], island_id=i)
        R.events = []; R.cevents = []
        mfA = A_.ST[12]; mfB = B_.ST[12]
        recs.append((i, j, a, b, int(cls[i]), int(cls[j]), s, int(A_.ST[11][EC.MI_CLS]), int(B_.ST[11][EC.MI_CLS]),
                     float(base_g + window - mfA[EC.MF_CLSSINCE]), float(base_g + window - mfB[EC.MF_CLSSINCE]), int(general)))
        if log and e % 2000 == 1999:
            print('%s: %d events %.0f s' % (name, e + 1, time.time() - t0), file=log, flush=True)
    return np.array(recs), time.time() - t0


def paired_summary(recs, nboot=400, seed=0):
    """kappa / alpha with the matched no-migrant control and a cluster bootstrap over recipient islands."""
    rng = np.random.default_rng(seed)
    out = {}
    ev = recs[recs[:, 11] == 0]
    gen = recs[recs[:, 11] == 1]
    def rate(sel, kind, branch):
        a = sel[:, 2].astype(int); b = sel[:, 3].astype(int)
        c = 3 - a - b
        fin = sel[:, 7 + branch].astype(int)
        tgt = np.array([MI.V[x] for x in (b if kind == 'kappa' else c)])
        return (fin == tgt).astype(float)
    if len(ev):
        cl = ev[:, 0].astype(int)
        uniq = np.unique(cl)
        for kind in ('kappa', 'alpha'):
            rA = rate(ev, kind, 0); rB = rate(ev, kind, 1)
            d = rB - rA
            def agg(idx):
                m = np.isin(cl, idx)
                return d[m].mean() if m.any() else np.nan
            boots = []
            groups = {u: np.nonzero(cl == u)[0] for u in uniq}
            for _ in range(nboot):
                pick = rng.choice(uniq, size=len(uniq), replace=True)
                ii = np.concatenate([groups[u] for u in pick])
                boots.append(d[ii].mean())
            lo, hi = np.percentile(boots, [2.5, 97.5])
            # clustered upper bound of the migrant branch rate itself
            bm = []
            for _ in range(nboot):
                pick = rng.choice(uniq, size=len(uniq), replace=True)
                ii = np.concatenate([groups[u] for u in pick])
                bm.append(rB[ii].mean())
            out[kind] = dict(n=int(len(ev)), n_clusters=int(len(uniq)), migrant_branch=float(rB.mean()), control_branch=float(rA.mean()),
                             excess=float(d.mean()), excess_ci=[float(lo), float(hi)], migrant_branch_ci=[float(x) for x in np.percentile(bm, [2.5, 97.5])],
                             count_migrant=int(rB.sum()), count_control=int(rA.sum()))
    if len(gen):
        trans = {}
        for r in gen:
            def cat(c):
                c = int(c)
                if c < 0: return 'none'
                if c < NOUT: return ['F', 'U', 'G', 'W', 'D'][int(MI.CATMAP[c])]
                return 'M'
            k0 = cat(r[4])
            for br, col in (('control', 7), ('migrant', 8)):
                key = '%s|%s>%s' % (br, k0, cat(r[col]))
                trans[key] = trans.get(key, 0) + 1
        out['general'] = dict(n=int(len(gen)), transitions=trans)
    return out


def write_json(obj, path):
    with open(path, 'w') as f:
        json.dump(obj, f)


def main(argv):
    cmd = argv[1]
    log = sys.stderr
    if cmd == 'pool':
        arm, nu, I, rounds, rep, start = argv[2], float(argv[3]), int(argv[4]), int(argv[5]), int(argv[6]), argv[7]
        mN = float(argv[8]) if len(argv) > 8 else 1e-3
        Nn = int(argv[9]) if len(argv) > 9 else N0
        name = 'pool_%s_nu%g_I%d_R%d_p%d_%s_m%g%s' % (arm, nu, I, rounds, rep, start, mN, '' if Nn == N0 else '_N%d' % Nn)
        dump_at = tuple(int(x) for x in os.environ.get('EC_DUMP', '').split(',') if x)
        cps = tuple(int(x) for x in os.environ.get('EC_CPS', '').split(',') if x) or CHECKPOINTS
        res, pool, R = run_pool(arm, nu, I, rounds, rep, start, mN, N=Nn, name=name, dump_at=dump_at, log=log, checkpoints=cps)
        write_json(res, os.path.join(OUT, name + '.json'))
        print('done', name, res['wall'])
    elif cmd == 'within':
        arm, nu, I, gens, rep = argv[2], float(argv[3]), int(argv[4]), int(argv[5]), int(argv[6])
        name = 'within_%s_nu%g_I%d_G%d_p%d' % (arm, nu, I, gens, rep)
        res = run_within(arm, nu, I, gens, rep, log=log, name=name)
        write_json(res, os.path.join(OUT, name + '.json'))
        print('done', name, res['wall'])
    elif cmd == 'paired':
        arm, nu, dump, nk, ng, seed0 = argv[2], float(argv[3]), argv[4], int(argv[5]), int(argv[6]), int(argv[7])
        name = 'paired_%s_nu%g_%s_k%d_g%d_s%d' % (arm, nu, os.path.basename(dump).replace('.npz', ''), nk, ng, seed0)
        recs, wall = run_paired(arm, nu, dump, nk, ng, seed0=seed0, log=log, name=name)
        np.save(os.path.join(SCRATCH, name + '.npy'), recs)
        res = dict(arm=arm, nu=nu, dump=os.path.basename(dump), n_kappa=nk, n_general=ng, wall=wall, summary=paired_summary(recs))
        write_json(res, os.path.join(OUT, name + '.json'))
        print('done', name, wall)
    else:
        raise SystemExit('unknown command')


if __name__ == '__main__':
    main(sys.argv)
