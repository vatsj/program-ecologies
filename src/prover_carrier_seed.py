"""Prover-carrier seed at b = 0 (specs/2026-10-05-prover-carrier-seed.md).

An invasion/establishment experiment at finite sizes on the proof-carrying contracts kernel (src/contracts_abm.py).
The kernel below is contracts_abm._run with extra counters and lineage tracking; the random-number call sequence is
unchanged, so a job built with contracts_abm.init_state and the same seeds reproduces a published run exactly.

Transition rules (spec, stated).  A birth copies the parent's source and contract.  With probability eps the child's
source is redrawn from mu; with s = 0 the inherited contract is kept iff valid for the new source, else dropped (no
contract is ever created by search).  A swap (probability sigma) copies a payoff-weighted donor's contract iff valid for
the child's source.  Counted per run: mutations, mutations of carriers, contracts kept / lost by invalid inheritance /
created (s > 0 only), swaps accepted (by recipient's previous contract, so onto non-carriers separately), same,
rejected, donor without contract.  A generation is I*N births.

Seeds.  'mix': the population is drawn iid from mu, then exactly round(f0 * N) slots per island (chosen uniformly) are
replaced by carriers whose sources are drawn from the establisher classes (self-cooperate and defect on D in the free
game, 118 sources at n = 8) in proportion to mu, each carrying its own signature.  'fb': the same with every carrier
FairBot.  'mu': contracts_abm's mu-drawn seed (each agent carries its own signature with probability f0).  ctl = 'off'
keeps the same source multiset and placement with the contracts removed.  The initial population depends on (seed, f0,
N, I, rep) only, not on b, sigma or ctl, so cells are paired.

Lineage.  Every agent carries the index of its founder (the initial slot it descends from, through births) and of its
contract's founder (the initial slot whose contract it carries, through inheritance or swaps; -1 if none).

    python3 src/prover_carrier_seed.py time
    python3 src/prover_carrier_seed.py run --set main [--procs 3]
    python3 src/prover_carrier_seed.py report
"""
import argparse, json, os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from abm import njit
import contracts_abm as A

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
W = 0.3
OUT = os.path.join(RUNS, 'prover_carrier_seed_rows.json')


def establishers(d, b='inf'):
    z = np.load(os.path.join(RUNS, 'contracts_types.npz'))
    v = z['val_inf']
    K = d['K']; iD = d['iD']
    return np.array([p for p in range(K) if v[p, p] == 1 and v[p, iD] == 0], np.int64)


@njit(cache=True)
def _run(init_t, init_l, I, N, w, m, eps, s, sigma, uniform, gens, every, seed,
         tsrc, tcon, pc, U, PCC, type_of, valid, own_type, mu_cdf, cls, iC, cC, cFB, anti, NC, K, lottery, thin,
         init_anc, init_canc):
    np.random.seed(seed)
    NP = U.shape[0]
    NA = I * N
    NT = tsrc.shape[0]
    UT = np.ascontiguousarray(U.T)
    Udiag = np.zeros(NP)
    for k in range(NP): Udiag[k] = U[k, k]
    agent_t = init_t.copy(); agent_l = init_l.copy()
    anc = init_anc.copy(); canc = init_canc.copy()
    cnt = np.zeros((I, NP), np.int64)
    pres = np.zeros((I, NP), np.int64); npres = np.zeros(I, np.int64); pos = -np.ones((I, NP), np.int64)
    paysum = np.zeros((I, NP))
    cnt_con = np.zeros(NC + 1, np.int64); cnt_lab = np.zeros(NC + 1, np.int64); cnt_src = np.zeros(K, np.int64)
    cnt_type = np.zeros(NT, np.int64)
    for a in range(NA):
        i = a // N; k = pc[agent_t[a]]
        if cnt[i, k] == 0:
            pres[i, npres[i]] = k; pos[i, k] = npres[i]; npres[i] += 1
        cnt[i, k] += 1
        cnt_con[tcon[agent_t[a]] + 1] += 1; cnt_lab[agent_l[a] + 1] += 1; cnt_src[tsrc[agent_t[a]]] += 1
        cnt_type[agent_t[a]] += 1
    for i in range(I):
        for t1 in range(npres[i]):
            j = pres[i, t1]
            for t2 in range(npres[i]):
                k = pres[i, t2]
                paysum[i, j] += cnt[i, k] * U[j, k]
    nsamp = gens // every
    half = nsamp // 2
    acc = np.zeros(14)   # pcc, carrier, coop mass, src-ALLC load, con-ALLC load, anti, FB-con share, max con share, -, -, -, n, carrier-cond pcc, n(carrier-cond)
    con_share = np.zeros(NC); src_share = np.zeros(K)
    # transitions: 0 mutations, 1 mutations of carriers, 2 kept (valid), 3 lost (invalid), 4 created (s), 5 mutation of non-carrier stays none
    trn = np.zeros(6, np.int64)
    sw = np.zeros(4, np.int64)          # accepted (changed), same, rejected, donor none
    sw_onto_none = 0                    # accepted swaps onto a recipient with no contract
    sw_cross = 0                        # accepted swaps whose donor's contract founder differs from the recipient's founder
    carr_g = np.zeros(gens, np.int32)
    ntr = nsamp // thin + 1
    tr = np.zeros((ntr, 4)); ntrace = 0          # gen, pcc, carrier, carrier-cond pcc
    status = 0; stop_gen = gens; s_idx = 0
    reach = np.zeros(NP, np.bool_)
    ncar = NA - cnt_con[0]
    gdone = 0
    for g in range(gens):
        for e in range(NA):
            i = np.random.randint(I)
            victim = i * N + np.random.randint(N)
            srci = i
            if m > 0.0 and I > 1 and np.random.random() < m:
                srci = np.random.randint(I - 1)
                if srci >= i: srci += 1
            par = A_sample(agent_t, pc, paysum, Udiag, srci, N, w, False)
            t = agent_t[par]; p = tsrc[t]; c = tcon[t]; lab = agent_l[par]
            an = anc[par]; ca = canc[par]
            if eps > 0.0 and np.random.random() < eps:
                p = A_pick(mu_cdf)
                trn[0] += 1
                if c >= 0: trn[1] += 1
                if np.random.random() < s:
                    if c != cls[p]: trn[4] += 1
                    c = cls[p]; lab = cls[p]; ca = victim
                else:
                    if c >= 0 and valid[p, c] == 0:
                        c = -1; ca = -1; trn[3] += 1
                    elif c >= 0:
                        trn[2] += 1
                    else:
                        trn[5] += 1
            if sigma > 0.0 and np.random.random() < sigma:
                dn = A_sample(agent_t, pc, paysum, Udiag, i, N, w, uniform)
                cd = tcon[agent_t[dn]]
                if cd < 0:
                    sw[3] += 1
                elif cd == c:
                    sw[1] += 1
                elif valid[p, cd] == 1:
                    sw[0] += 1
                    if c < 0: sw_onto_none += 1
                    if canc[dn] != an: sw_cross += 1
                    c = cd; ca = canc[dn]
                else:
                    sw[2] += 1
            if sigma > 0.0 and np.random.random() < sigma:
                dn = A_sample(agent_t, pc, paysum, Udiag, i, N, w, uniform)
                ld = agent_l[dn]
                if ld >= 0:
                    lab = ld
            nt = type_of[p, c + 1]
            ot = agent_t[victim]
            ol = agent_l[victim]
            agent_l[victim] = lab
            anc[victim] = an; canc[victim] = ca
            cnt_lab[ol + 1] -= 1; cnt_lab[lab + 1] += 1
            if nt == ot:
                continue
            agent_t[victim] = nt
            if tcon[ot] < 0 and c >= 0: ncar += 1
            if tcon[ot] >= 0 and c < 0: ncar -= 1
            cnt_con[tcon[ot] + 1] -= 1; cnt_con[c + 1] += 1
            cnt_src[tsrc[ot]] -= 1; cnt_src[p] += 1
            cnt_type[ot] -= 1; cnt_type[nt] += 1
            ko = pc[ot]; kn = pc[nt]
            if ko == kn:
                continue
            cnt[i, ko] -= 1
            if cnt[i, ko] == 0:
                q = pos[i, ko]; lastk = pres[i, npres[i] - 1]
                pres[i, q] = lastk; pos[i, lastk] = q; pos[i, ko] = -1; npres[i] -= 1
            new = cnt[i, kn] == 0
            if new:
                pres[i, npres[i]] = kn; pos[i, kn] = npres[i]; npres[i] += 1
            cnt[i, kn] += 1
            for t1 in range(npres[i]):
                j = pres[i, t1]
                if new and j == kn:
                    continue
                paysum[i, j] += UT[kn, j] - UT[ko, j]
            if new:
                v = 0.0
                for t1 in range(npres[i]):
                    k = pres[i, t1]
                    v += cnt[i, k] * U[kn, k]
                paysum[i, kn] = v
        carr_g[g] = ncar
        gdone = g + 1
        if (g + 1) % every == 0:
            pcc_tot = 0.0; coop = 0
            for i in range(I):
                cc = 0.0
                for t1 in range(npres[i]):
                    a1 = pres[i, t1]
                    if PCC[a1, a1] == 1.0: coop += cnt[i, a1]
                    for t2 in range(npres[i]):
                        b1 = pres[i, t2]
                        nn = cnt[i, a1] * cnt[i, b1] if a1 != b1 else cnt[i, a1] * (cnt[i, a1] - 1)
                        cc += nn * PCC[a1, b1]
                pcc_tot += cc / (N * (N - 1))
            pcc = pcc_tot / I
            carriers = NA - cnt_con[0]
            # carrier-conditional P(C,C) (pooled over islands; exact for I = 1)
            ccc = -1.0
            if carriers >= 2:
                num = 0.0
                for t1 in range(K, NT):
                    n1 = cnt_type[t1]
                    if n1 == 0: continue
                    for t2 in range(K, NT):
                        n2 = cnt_type[t2]
                        if n2 == 0: continue
                        nn = n1 * n2 if t1 != t2 else n1 * (n1 - 1)
                        num += nn * PCC[pc[t1], pc[t2]]
                ccc = num / (carriers * (carriers - 1.0))
            topc = -1; topn = 0
            for cc_ in range(NC):
                if cnt_con[cc_ + 1] > topn:
                    topn = cnt_con[cc_ + 1]; topc = cc_
            if s_idx % thin == 0 and ntrace < ntr:
                tr[ntrace, 0] = g + 1; tr[ntrace, 1] = pcc; tr[ntrace, 2] = carriers / NA; tr[ntrace, 3] = ccc
                ntrace += 1
            if s_idx >= half:
                acc[0] += pcc; acc[1] += carriers / NA; acc[2] += coop / NA
                if coop > 0:
                    acc[3] += cnt_src[iC] / coop; acc[4] += cnt_con[cC + 1] / coop
                an_ = 0
                for p in range(K):
                    if anti[p]: an_ += cnt_src[p]
                acc[5] += an_ / NA
                if carriers > 0:
                    acc[6] += cnt_con[cFB + 1] / carriers; acc[7] += topn / carriers
                    for cc_ in range(NC):
                        if cnt_con[cc_ + 1] > 0: con_share[cc_] += cnt_con[cc_ + 1] / carriers
                if ccc >= 0:
                    acc[12] += ccc; acc[13] += 1
                acc[11] += 1
                for p in range(K):
                    if cnt_src[p] > 0: src_share[p] += cnt_src[p] / NA
            s_idx += 1
            if lottery:
                for k in range(NP): reach[k] = False
                for t1 in range(NT):
                    if cnt_type[t1] > 0:
                        reach[pc[t1]] = True
                if sigma > 0.0:
                    for p in range(K):
                        if cnt_src[p] == 0: continue
                        for cc_ in range(NC):
                            if cnt_con[cc_ + 1] > 0 and valid[p, cc_] == 1:
                                reach[pc[type_of[p, cc_ + 1]]] = True
                lo = 1e300; hi = -1e300
                for a1 in range(NP):
                    if not reach[a1]: continue
                    for b1 in range(NP):
                        if not reach[b1]: continue
                        if U[a1, b1] < lo: lo = U[a1, b1]
                        if U[a1, b1] > hi: hi = U[a1, b1]
                if hi - lo < 1e-12:
                    status = 1; stop_gen = g + 1
                    break
    if lottery and status == 0:
        mono = True
        for i in range(I):
            if npres[i] != 1: mono = False
        status = 3 if mono else 4
    isl_cc = np.zeros(I)
    for i in range(I):
        cc = 0.0
        for t1 in range(npres[i]):
            a1 = pres[i, t1]
            for t2 in range(npres[i]):
                b1 = pres[i, t2]
                nn = cnt[i, a1] * cnt[i, b1] if a1 != b1 else cnt[i, a1] * (cnt[i, a1] - 1)
                cc += nn * PCC[a1, b1]
        isl_cc[i] = cc / (N * (N - 1))
    return (acc, con_share, src_share, trn, sw, sw_onto_none, sw_cross, carr_g[:gdone], tr[:ntrace], status, stop_gen,
            isl_cc, cnt_con, cnt_src, cnt_type, agent_t, anc, canc)


A_sample = A._sample
A_pick = A._pick


def init_seed(d, est, seed, N, I, f0, rng):
    """Carrier seed: iid mu, then exactly round(f0 * N) carriers per island at uniformly chosen slots."""
    K = d['K']; NA = N * I
    src = rng.choice(K, size=NA, p=d['mu'] / d['mu'].sum())
    k = int(round(f0 * N))
    car = np.zeros(NA, bool)
    for i in range(I):
        sl = rng.choice(N, size=k, replace=False) + i * N
        car[sl] = True
    nc = int(car.sum())
    if seed == 'mix':
        pe = d['mu'][est] / d['mu'][est].sum()
        src[car] = est[rng.choice(len(est), size=nc, p=pe)]
    elif seed == 'fb':
        src[car] = d['iFB']
    return src, car


def build_job_state(job):
    d = A.data(job['b'])
    if job['seed'] == 'mu':
        # contracts_abm's mu-drawn seed with contracts_abm's rng key, so published runs reproduce exactly
        rng = np.random.default_rng([int(1e6 * job['f0']) + 7, int(10 * job['sigma']), int(job.get('s', 0)), job['N'], job['I'], job['rep'],
                                     1, {'inf': 0, '4': 4, '2': 2, '0': 100}[job['b']], 0])
        it, il = A.init_state(d, 'mu', job['N'], job['I'], job['f0'], rng)
        src = d['tsrc'][it]; car = d['tcon'][it] >= 0
    else:
        est = establishers(d)
        rng = np.random.default_rng([['mix', 'fb'].index(job['seed']) + 11, int(round(1e5 * job['f0'])), job['N'], job['I'], job['rep'], 20251005])
        src, car = init_seed(d, est, job['seed'], job['N'], job['I'], job['f0'], rng)
    if job.get('k') is not None:
        pass
    if job.get('ctl') == 'off':
        car = np.zeros_like(car)
    it = np.where(car, d['own_type'][src], d['type_of'][src, 0]).astype(np.int64)
    il = np.where(car, d['cls'][src], -1).astype(np.int64)
    seed = int(rng.integers(1 << 30))
    return d, it, il, seed, src, car


def lottery_state(job):
    """Exactly k prover carriers (establishers in proportion to mu) per island, at uniformly chosen slots."""
    d = A.data(job['b'])
    est = establishers(d)
    N, I, k = job['N'], job['I'], job['k']
    rng = np.random.default_rng([31, N, I, k, job['rep'], 20251005])
    K = d['K']
    src = rng.choice(K, size=N * I, p=d['mu'] / d['mu'].sum())
    car = np.zeros(N * I, bool)
    pe = d['mu'][est] / d['mu'][est].sum()
    for i in range(I):
        sl = rng.choice(N, size=k, replace=False) + i * N
        car[sl] = True
        src[sl] = est[rng.choice(len(est), size=k, p=pe)]
    if job.get('ctl') == 'off':
        car = np.zeros_like(car)
    it = np.where(car, d['own_type'][src], d['type_of'][src, 0]).astype(np.int64)
    il = np.where(car, d['cls'][src], -1).astype(np.int64)
    seed = int(rng.integers(1 << 30))
    return d, it, il, seed, src, car


def run_job(job):
    lottery = bool(job['lottery'])
    if job.get('k') is not None:
        d, it, il, seed, src0, car0 = lottery_state(job)
    else:
        d, it, il, seed, src0, car0 = build_job_state(job)
    N, I = job['N'], job['I']
    NA = N * I
    anc0 = np.arange(NA, dtype=np.int64)
    canc0 = np.where(car0, np.arange(NA), -1).astype(np.int64)
    every = 20 if not lottery else 5
    thin = 25 if not lottery else 20
    t0 = time.time()
    out = _run(it, il, I, N, W, job.get('mN', 0.0) / N, job['eps'], float(job.get('s', 0)), float(job['sigma']), False,
               job['gens'], every, seed, d['tsrc'], d['tcon'], d['pc'], d['U'], d['PCC'], d['type_of'], d['valid'], d['own_type'],
               d['mu_cdf'], d['cls'], d['iC'], d['cC'], d['cFB'], d['anti'], d['NC'], d['K'], lottery, thin, anc0, canc0)
    (acc, con_share, src_share, trn, sw, sw_none, sw_cross, carr_g, tr, status, stop_gen, isl_cc, cnt_con, cnt_src, cnt_type,
     agent_t, anc, canc) = out
    r = dict(job)
    r['time_s'] = time.time() - t0
    nm = d['names']; cn = d['cname']; tsrc = d['tsrc']; tcon = d['tcon']
    n = max(acc[11], 1)
    k0 = int(car0.sum())
    r['k0'] = k0
    r['seed_sources'] = {nm[p]: int(v) for p, v in zip(*np.unique(src0[car0], return_counts=True))} if k0 else {}
    # carrier trajectory
    cg = carr_g.astype(np.int64)
    G = len(cg)
    ext = np.nonzero(cg == 0)[0]
    r['carrier_ext_gen'] = int(ext[0] + 1) if len(ext) and k0 > 0 else None
    def first_ge(fr):
        h = np.nonzero(cg >= fr * NA)[0]
        return int(h[0] + 1) if len(h) else None
    r['t10'] = first_ge(0.1); r['t50'] = first_ge(0.5)
    r['carrier_min_500'] = int(cg[:500].min()) if G else None
    r['carrier_at'] = {str(gg): int(cg[gg - 1]) for gg in (10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000) if gg <= G}
    r['growth_200'] = float(np.log(max(cg[199], 0.5) / k0) / 200) if G >= 200 and k0 > 0 else None
    r['carrier_traj'] = cg[:1000:10].tolist() + cg[1000::200].tolist()
    r['trace'] = tr.tolist()
    r['transitions'] = dict(mutations=int(trn[0]), mut_of_carriers=int(trn[1]), kept_valid=int(trn[2]), lost_invalid=int(trn[3]),
                            created=int(trn[4]), noncarrier_stays_none=int(trn[5]))
    r['swaps'] = dict(accepted=int(sw[0]), same=int(sw[1]), rejected=int(sw[2]), donor_none=int(sw[3]), accepted_onto_none=int(sw_none),
                      accepted_cross_lineage=int(sw_cross))
    births = NA * (stop_gen if lottery else G)
    r['births'] = int(births)
    # final population: lineage ancestry of the final carriers
    fc = tcon[agent_t] >= 0
    r['final_carrier'] = float(fc.mean())
    if fc.any():
        fa = anc[fc]; ca = canc[fc]
        r['final_carriers_founders'] = int(len(np.unique(fa)))
        r['final_carriers_from_seed_carrier_founder'] = float(car0[fa].mean())
        r['final_carriers_contract_from_other_lineage'] = float((ca != fa).mean())
        r['final_carriers_founder_source'] = {nm[p]: int(v) for p, v in zip(*np.unique(src0[fa], return_counts=True))}
        r['final_carriers_contract_founder_n'] = int(len(np.unique(ca)))
    r['final_contracts'] = {(cn[c - 1] if c > 0 else 'none'): int(v) for c, v in enumerate(cnt_con) if v > 0 and v >= 0.005 * NA}
    r['final_sources'] = {nm[p]: int(v) for p, v in enumerate(cnt_src) if v > 0 and v >= 0.005 * NA}
    if not lottery:
        cs = con_share / n; ss = src_share / n
        r.update(pcc=acc[0] / n, carrier=acc[1] / n, coop_mass=acc[2] / n, src_allc_load=acc[3] / n, con_allc_load=acc[4] / n,
                 anti_share=acc[5] / n, fb_con_share=acc[6] / n, max_con_share=acc[7] / n,
                 carrier_pcc=acc[12] / acc[13] if acc[13] > 0 else None,
                 top_contracts=[(cn[c], float(cs[c])) for c in np.argsort(-cs)[:8] if cs[c] > 0],
                 top_sources=[(nm[p], float(ss[p])) for p in np.argsort(-ss)[:10] if ss[p] > 0])
    else:
        st = {1: 'frozen', 3: 'metastable', 4: 'unresolved'}.get(int(status), 'running')
        pcc = float(isl_cc.mean())
        r.update(status=st, stop_gen=int(stop_gen), pcc=pcc,
                 outcome=('efficient' if pcc >= 0.95 else ('defecting' if pcc <= 0.05 else 'other')) if st != 'unresolved' else 'unresolved',
                 isl_cc=isl_cc.tolist() if I <= 64 else None)
        if I > 1 and k0:
            # placement: carriers' sources per island at seeding
            r['placement'] = [sorted(nm[p] for p in src0[i * N:(i + 1) * N][car0[i * N:(i + 1) * N]]) for i in range(I)] if I <= 4 else \
                [len(set(src0[i * N:(i + 1) * N][car0[i * N:(i + 1) * N]])) for i in range(I)]
    return r


# ------------------------------------------------------------------ job sets
F0S = (0.001, 0.003, 0.01, 0.03, 0.1)


def reps_for(f0):
    return 20 if f0 in (0.001, 0.003) else 5


def jobs_for(which, gens=100000):
    J = []
    if which in ('main', 'ctl_off', 'ctl_inf', 'twins', 'twins_ctl'):
        for seed in ('mix', 'fb'):
            for f0 in F0S:
                for sg in (0.0, 1.0):
                    for r in range(20 if which.startswith('twins') else reps_for(f0)):
                        base = dict(seed=seed, f0=f0, sigma=sg, N=6400, I=1, rep=r, s=0, mN=0.0)
                        if which == 'main':
                            J.append(dict(base, b='0', ctl='on', eps=1e-3, gens=gens, lottery=False, set='main'))
                        elif which == 'ctl_off' and sg == 0.0:
                            J.append(dict(base, b='0', ctl='off', eps=1e-3, gens=gens, lottery=False, set='ctl_off'))
                        elif which == 'ctl_inf' and sg == 0.0:
                            J.append(dict(base, b='inf', ctl='on', eps=1e-3, gens=gens, lottery=False, set='ctl_inf'))
                        elif which == 'twins':
                            J.append(dict(base, b='0', ctl='on', eps=0.0, gens=gens, lottery=True, set='twins'))
                        elif which == 'twins_ctl' and sg == 0.0:
                            J.append(dict(base, b='0', ctl='off', eps=0.0, gens=gens, lottery=True, set='twins_ctl'))
                            J.append(dict(base, b='inf', ctl='on', eps=0.0, gens=gens, lottery=True, set='twins_ctl'))
    if which == 'ctl_mu':
        for sg in (0.0, 1.0):
            for r in range(5):
                J.append(dict(seed='mu', f0=0.01, sigma=sg, N=6400, I=1, rep=r, s=0, mN=0.0, b='0', ctl='on', eps=1e-3, gens=gens,
                              lottery=False, set='ctl_mu'))
    if which == 'nsweep':
        for N in (1600, 25600):
            for sg in (0.0, 1.0):
                for r in range(5 if N == 1600 else 3):
                    J.append(dict(seed='mix', f0=0.01, sigma=sg, N=N, I=1, rep=r, s=0, mN=0.0, b='0', ctl='on', eps=1e-3, gens=gens,
                                  lottery=False, set='nsweep'))
    if which == 'nsweep_twins':
        for N in (1600, 25600):
            for sg in (0.0,):
                for r in range(20):
                    J.append(dict(seed='mix', f0=0.01, sigma=sg, N=N, I=1, rep=r, s=0, mN=0.0, b='0', ctl='on', eps=0.0, gens=gens,
                                  lottery=True, set='nsweep_twins'))
    if which == 'long':
        for f0 in (0.01, 0.1):
            for sg in (0.0, 1.0):
                for r in range(3):
                    J.append(dict(seed='mix', f0=f0, sigma=sg, N=6400, I=1, rep=r, s=0, mN=0.0, b='0', ctl='on', eps=1e-3, gens=100000,
                                  lottery=False, set='long'))
    if which == 'lottery':
        cells = [(100, 4, 0), (100, 4, 1), (100, 4, 3), (100, 4, 16), (100, 64, 0), (100, 64, 1), (100, 64, 3)]
        for sg in (0.0, 1.0):
            for (N, I, k) in cells:
                if k == 0 and sg == 1.0:
                    continue
                for r in range(40):
                    J.append(dict(seed='mix', k=k, f0=k / N, sigma=sg, N=N, I=I, rep=r, s=0, mN=1.0, b='0', ctl='on', eps=0.0,
                                  gens=gens, lottery=True, set='lottery'))
    return J


def key(j):
    return tuple(str(j.get(k)) for k in ('set', 'seed', 'b', 'ctl', 'f0', 'k', 'sigma', 'N', 'I', 'rep', 'eps'))


def main_run(sets, procs, gens, limit=None):
    rows = json.load(open(OUT)) if os.path.exists(OUT) else []
    done = {key(r) for r in rows}
    jobs = [j for s in sets for j in jobs_for(s, gens) if key(j) not in done]   # kept in the order of `sets`
    if limit: jobs = jobs[:limit]
    for b in ('0', 'inf'):
        A.data(b)
    print('%d jobs' % len(jobs), flush=True)
    with Pool(procs) as pool:
        for r in pool.imap_unordered(run_job, jobs):
            rows.append(r)
            if r['lottery']:
                print('%s %s b=%s %s f0=%g k=%s sig=%g N=%d I=%d rep %d: %s %s gen %d P(C,C) %.3f carriers %.3f (%.0fs)' % (
                    r['set'], r['seed'], r['b'], r['ctl'], r['f0'], r.get('k'), r['sigma'], r['N'], r['I'], r['rep'], r['status'], r['outcome'],
                    r['stop_gen'], r['pcc'], r['final_carrier'], r['time_s']), flush=True)
            else:
                print('%s %s b=%s %s f0=%g sig=%g N=%d rep %d: P(C,C) %.3f carrier %.3f ext %s t50 %s (%.0fs)' % (
                    r['set'], r['seed'], r['b'], r['ctl'], r['f0'], r['sigma'], r['N'], r['rep'], r['pcc'], r['carrier'],
                    r['carrier_ext_gen'], r['t50'], r['time_s']), flush=True)
            tmp = OUT + '.tmp'
            json.dump(rows, open(tmp, 'w')); os.replace(tmp, OUT)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('kind', choices=['time', 'run', 'repro'])
    ap.add_argument('--set', nargs='*', default=['main'])
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--gens', type=int, default=100000)
    ap.add_argument('--limit', type=int)
    a = ap.parse_args()
    if a.kind == 'time':
        for b in ('0', 'inf'):
            j = dict(seed='mix', f0=0.0, sigma=0.0, N=6400, I=1, rep=0, s=0, mN=0.0, b=b, ctl='on', eps=1e-3, gens=a.gens, lottery=False, set='time')
            t = time.time(); r = run_job(j)
            print(b, 'gens', a.gens, 'P(C,C) %.3f' % r['pcc'], '%.1fs' % (time.time() - t), flush=True)
    elif a.kind == 'repro':
        # same RNG sequence as contracts_abm: a mu-seed b = 0 job must give identical statistics through both kernels
        for sg in (0.0, 1.0):
            j = dict(seed='mu', f0=0.01, sigma=sg, N=6400, I=1, rep=0, s=0, mN=0.0, b='0', ctl='on', eps=1e-3, gens=a.gens, lottery=False, set='repro')
            r = run_job(j)
            r2 = A.run_job(dict(b='0', s=0, f0=0.01, sigma=sg, start='mu', N=6400, I=1, rep=0, gens=a.gens, eps=1e-3, uniform=False,
                                lottery=False, mN=0.0, tag='repro'))
            print(sg, 'new', r['pcc'], r['carrier'], r['swaps'], 'old', r2['pcc'], r2['carrier'], r2['swaps']['accepted'], r2['swaps']['rejected'], flush=True)
    else:
        main_run(a.set, a.procs, a.gens, a.limit)
