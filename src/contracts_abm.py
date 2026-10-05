"""Proof-carrying contracts v1: agent-based runs (finite eps, well-mixed) and the eps = 0 seeding lottery on islands.
Finite-size mechanism results, not limits (swapping is a second operator outside the eps->0 chain).

Agents carry (source, contract) = a type of src/contracts.py, plus a behaviourally inert neutral label.  A birth: a
uniformly random agent of island i dies; the parent is drawn from island i (or, with probability m, from a uniformly
random other island) with probability proportional to exp(w * fitness) (rejection sampling; fitness = mean payoff
against the other N - 1 agents of the parent's island).  With probability eps the child's source is redrawn from mu;
its contract is then, with probability s, the source's own signature, else the parent's contract if valid for the new
source, else none; the label follows the same rule without a validity filter.  Then with probability sigma a donor is
drawn on island i (payoff-weighted or uniform) and its contract copied if valid for the child's source; independently,
with probability sigma, a label donor is drawn the same way and its label copied.

    python3 src/contracts_abm.py grid [--procs 3]
    python3 src/contracts_abm.py lottery [--procs 3]
    python3 src/contracts_abm.py report
"""
import argparse, json, os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from abm import njit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
PD = np.array([[-1.0, 1.0], [-2.0, 0.0]])
W = 0.3
FMAX = 1.0                       # largest PD payoff: rejection bound for exp(w * f)
_D = {}


def data(b):
    """Type tables at gate b ('inf', '4', '2')."""
    if b in _D:
        return _D[b]
    z = np.load(os.path.join(RUNS, 'contracts_types.npz'))
    st = json.load(open(os.path.join(RUNS, 'contracts_static.json')))
    names = st['names']; cname = st['cname']
    tsrc, tcon, mu, cls, valid = z['tsrc'], z['tcon'], z['mu'], z['cls'], z['valid']
    val = z['val_' + b] if b != '0' else np.load(os.path.join(RUNS, 'contracts_types_b0.npz'))['val_0']
    U = PD[val.astype(int), val.T.astype(int)]
    key = {}; pc = np.zeros(len(U), np.int64)
    for t in range(len(U)):
        pc[t] = key.setdefault((U[t].tobytes(), U[:, t].tobytes()), len(key))
    NP = len(key)
    rep = np.zeros(NP, np.int64)
    for t in range(len(U) - 1, -1, -1):
        rep[pc[t]] = t
    Uc = np.ascontiguousarray(U[np.ix_(rep, rep)])
    PCC = np.ascontiguousarray((val * val.T)[np.ix_(rep, rep)].astype(np.float64))
    K = len(mu); NC = valid.shape[1]
    type_of = -np.ones((K, NC + 1), np.int64)          # column 0 = none, c + 1 = contract c
    for t in range(len(tsrc)):
        type_of[tsrc[t], tcon[t] + 1] = t
    iC = names.index('C'); iD = names.index('D'); iFB = names.index('BOX(THEM(ME))')
    PS = 'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))'
    # anti-provers (RS-b): a BOX/BOX1(THEM(ME)) atom whose truth makes the action D
    import modal as M
    L = M.ModalLanguage(8)
    nat, ak, al, af, aa, tt = L.arrays()
    anti = np.zeros(K, np.bool_)
    for p in range(K):
        for j in range(nat[p]):
            if ak[p, j] == 0 and af[p, j] == 0:
                if all(((int(tt[p]) >> i) & 1) == 0 for i in range(1 << nat[p]) if (i >> j) & 1):
                    anti[p] = True
    d = dict(names=names, cname=cname, tsrc=tsrc, tcon=tcon, mu=mu, cls=cls, valid=valid.astype(np.int8), pc=pc, NP=NP,
             U=Uc, PCC=PCC, type_of=type_of, K=K, NC=NC, iC=iC, iD=iD, iFB=iFB,
             cC=int(cls[iC]), cD=int(cls[iD]), cFB=int(cls[iFB]), cPS=int(cls[names.index(PS)]), anti=anti,
             mu_cdf=np.cumsum(mu / mu.sum()), own_type=np.array([type_of[p, cls[p] + 1] for p in range(K)], np.int64),
             selfcoop_con=np.array([int(st_S) for st_S in np.diag(z['S'])], np.int64))
    _D[b] = d
    return d


@njit(cache=True)
def _sample(agent_t, pc, paysum, Udiag, isl, N, w, uniform):
    """An agent index on island isl, drawn uniformly or proportional to exp(w * fitness) (rejection)."""
    base = isl * N
    while True:
        a = base + np.random.randint(N)
        if uniform:
            return a
        k = pc[agent_t[a]]
        f = (paysum[isl, k] - Udiag[k]) / (N - 1)
        if np.random.random() < np.exp(w * (f - 1.0)):
            return a


@njit(cache=True)
def _pick(cdf):
    u = np.random.random()
    lo = 0; hi = cdf.shape[0] - 1
    while lo < hi:
        m = (lo + hi) // 2
        if cdf[m] < u: lo = m + 1
        else: hi = m
    return lo


@njit(cache=True)
def _run(init_t, init_l, I, N, w, m, eps, s, sigma, uniform, gens, every, seed,
         tsrc, tcon, pc, U, PCC, type_of, valid, own_type, mu_cdf, cls, iC, cC, cFB, anti, NC, K, lottery, thin):
    np.random.seed(seed)
    NP = U.shape[0]
    NA = I * N
    UT = np.ascontiguousarray(U.T)
    Udiag = np.zeros(NP)
    for k in range(NP): Udiag[k] = U[k, k]
    agent_t = init_t.copy(); agent_l = init_l.copy()
    cnt = np.zeros((I, NP), np.int64)
    pres = np.zeros((I, NP), np.int64); npres = np.zeros(I, np.int64); pos = -np.ones((I, NP), np.int64)
    paysum = np.zeros((I, NP))
    cnt_con = np.zeros(NC + 1, np.int64); cnt_lab = np.zeros(NC + 1, np.int64); cnt_src = np.zeros(K, np.int64)
    cnt_type = np.zeros(tsrc.shape[0], np.int64)
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
    # accumulators (second half)
    acc = np.zeros(12)   # pcc, carrier, coop mass, src-ALLC load, con-ALLC load, anti share, FB-con share, max con share, FB-label share, max label share, labelled frac, n
    con_share = np.zeros(NC); lab_share = np.zeros(NC)
    src_share = np.zeros(K)
    dom_con_prev = -2; con_trans = np.zeros((NC + 2, NC + 2), np.int64)
    dom_pc_prev = -2; pc_trans = np.zeros((NP, NP), np.int64) if I == 1 else np.zeros((1, 1), np.int64)
    sw = np.zeros((4, NC + 1), np.int64)        # accepted (changed), accepted (same), rejected, donor without contract [col 0]
    sw2 = np.zeros((4, NC + 1), np.int64)       # second half
    routes = np.zeros((NC + 1, NC), np.int64)    # recipient's previous contract (+1) -> copied contract, accepted changes
    lsw = np.zeros(2, np.int64)
    ntr = nsamp // thin + 1
    tr = np.zeros((ntr, 6)); ntrace = 0          # pcc, carrier, FB-con share, top con, top con share, coop mass
    status = 0; stop_gen = gens; s_idx = 0
    reach = np.zeros(NP, np.bool_)
    for g in range(gens):
        second = 2 * (g // every) >= nsamp
        for e in range(NA):
            i = np.random.randint(I)
            victim = i * N + np.random.randint(N)
            srci = i
            if m > 0.0 and I > 1 and np.random.random() < m:
                srci = np.random.randint(I - 1)
                if srci >= i: srci += 1
            par = _sample(agent_t, pc, paysum, Udiag, srci, N, w, False)
            t = agent_t[par]; p = tsrc[t]; c = tcon[t]; lab = agent_l[par]
            if eps > 0.0 and np.random.random() < eps:
                p = _pick(mu_cdf)
                if np.random.random() < s:
                    c = cls[p]; lab = cls[p]
                else:
                    if c >= 0 and valid[p, c] == 0:
                        c = -1
            if sigma > 0.0 and np.random.random() < sigma:
                dn = _sample(agent_t, pc, paysum, Udiag, i, N, w, uniform)
                cd = tcon[agent_t[dn]]
                if cd < 0:
                    sw[3, 0] += 1
                    if second: sw2[3, 0] += 1
                elif cd == c:
                    sw[1, cd + 1] += 1
                    if second: sw2[1, cd + 1] += 1
                elif valid[p, cd] == 1:
                    sw[0, cd + 1] += 1; routes[c + 1, cd] += 1
                    if second: sw2[0, cd + 1] += 1
                    c = cd
                else:
                    sw[2, cd + 1] += 1
                    if second: sw2[2, cd + 1] += 1
            if sigma > 0.0 and np.random.random() < sigma:
                dn = _sample(agent_t, pc, paysum, Udiag, i, N, w, uniform)
                ld = agent_l[dn]
                if ld >= 0:
                    if ld != lab: lsw[0] += 1
                    lab = ld
                else:
                    lsw[1] += 1
            nt = type_of[p, c + 1]
            ot = agent_t[victim]
            ol = agent_l[victim]
            agent_l[victim] = lab
            cnt_lab[ol + 1] -= 1; cnt_lab[lab + 1] += 1
            if nt == ot:
                continue
            agent_t[victim] = nt
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
        if (g + 1) % every == 0:
            # sample
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
            labelled = NA - cnt_lab[0]
            topc = -1; topn = 0
            for cc_ in range(NC):
                if cnt_con[cc_ + 1] > topn:
                    topn = cnt_con[cc_ + 1]; topc = cc_
            topl = 0
            for cc_ in range(NC):
                if cnt_lab[cc_ + 1] > topl: topl = cnt_lab[cc_ + 1]
            if s_idx % thin == 0 and ntrace < ntr:
                tr[ntrace, 0] = pcc; tr[ntrace, 1] = carriers / NA
                tr[ntrace, 2] = cnt_con[cFB + 1] / carriers if carriers > 0 else np.nan
                tr[ntrace, 3] = topc; tr[ntrace, 4] = topn / carriers if carriers > 0 else np.nan
                tr[ntrace, 5] = coop / NA
                ntrace += 1
            if s_idx >= half:
                acc[0] += pcc; acc[1] += carriers / NA; acc[2] += coop / NA
                if coop > 0:
                    acc[3] += cnt_src[iC] / coop; acc[4] += cnt_con[cC + 1] / coop
                an = 0
                for p in range(K):
                    if anti[p]: an += cnt_src[p]
                acc[5] += an / NA
                if carriers > 0:
                    acc[6] += cnt_con[cFB + 1] / carriers; acc[7] += topn / carriers
                    for cc_ in range(NC):
                        if cnt_con[cc_ + 1] > 0: con_share[cc_] += cnt_con[cc_ + 1] / carriers
                if labelled > 0:
                    acc[8] += cnt_lab[cFB + 1] / labelled; acc[9] += topl / labelled
                    for cc_ in range(NC):
                        if cnt_lab[cc_ + 1] > 0: lab_share[cc_] += cnt_lab[cc_ + 1] / labelled
                acc[10] += labelled / NA
                acc[11] += 1
                for p in range(K):
                    if cnt_src[p] > 0: src_share[p] += cnt_src[p] / NA
            # dominant contract (> 1/2 of carriers, else -1 = none dominant; NC = no carriers)
            dc = -1
            if carriers == 0:
                dc = NC
            elif 2 * topn > carriers:
                dc = topc
            if dom_con_prev != -2 and dc != dom_con_prev:
                con_trans[dom_con_prev + 1, dc + 1] += 1
            dom_con_prev = dc
            if I == 1:
                dp = -1
                for t1 in range(npres[0]):
                    if 2 * cnt[0, pres[0, t1]] > N: dp = pres[0, t1]
                if dp >= 0:
                    if dom_pc_prev >= 0 and dp != dom_pc_prev:
                        pc_trans[dom_pc_prev, dp] += 1
                    dom_pc_prev = dp
            s_idx += 1
            # lottery stopping: every type reachable by swapping is pairwise payoff-identical
            if lottery:
                for k in range(NP): reach[k] = False
                nr = 0
                for t1 in range(tsrc.shape[0]):
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
    return (acc, con_share, lab_share, src_share, con_trans, pc_trans, sw, sw2, routes, lsw, tr[:ntrace],
            status, stop_gen, isl_cc, cnt_con, cnt_src, cnt_type)


def init_state(d, start, N, I, f0, rng):
    NA = N * I
    K = d['K']
    if start == 'alld':
        src = np.full(NA, d['iD'], np.int64)
        car = rng.random(NA) < f0
        src[car] = rng.choice(K, size=int(car.sum()), p=d['mu'] / d['mu'].sum())
    else:
        src = rng.choice(K, size=NA, p=d['mu'] / d['mu'].sum())
        car = rng.random(NA) < f0
    t = np.where(car, d['own_type'][src], d['type_of'][src, 0])
    lab = np.where(car, d['cls'][src], -1)
    return t.astype(np.int64), lab.astype(np.int64)


def run_job(job):
    """job: dict(b, s, f0, sigma, start, N, I, rep, gens, eps, uniform, lottery, mN, tag)"""
    d = data(job['b'])
    rng = np.random.default_rng([int(1e6 * job['f0']) + 7, int(10 * job['sigma']), int(job['s']), job['N'], job['I'], job['rep'],
                                 ['alld', 'mu'].index(job['start']), {'inf': 0, '4': 4, '2': 2, '0': 100}[job['b']], int(job['uniform'])])
    it, il = init_state(d, job['start'], job['N'], job['I'], job['f0'], rng)
    seed = int(rng.integers(1 << 30))
    t0 = time.time()
    every = 20 if not job['lottery'] else 5
    out = _run(it, il, job['I'], job['N'], W, job['mN'] / job['N'], job['eps'], float(job['s']), float(job['sigma']), bool(job['uniform']),
               job['gens'], every, seed, d['tsrc'], d['tcon'], d['pc'], d['U'], d['PCC'], d['type_of'], d['valid'], d['own_type'], d['mu_cdf'],
               d['cls'], d['iC'], d['cC'], d['cFB'], d['anti'], d['NC'], d['K'], bool(job['lottery']), 50 if not job['lottery'] else 20)
    (acc, con_share, lab_share, src_share, con_trans, pc_trans, sw, sw2, routes, lsw, tr, status, stop_gen, isl_cc, cnt_con, cnt_src, cnt_type) = out
    n = max(acc[11], 1)
    cn = d['cname']; nm = d['names']; NC = d['NC']
    r = dict(job)
    r['time_s'] = time.time() - t0
    if not job['lottery']:
        cs = con_share / n; ls = lab_share / n; ss = src_share / n
        r.update(pcc=acc[0] / n, carrier=acc[1] / n, coop_mass=acc[2] / n, src_allc_load=acc[3] / n, con_allc_load=acc[4] / n,
                 anti_share=acc[5] / n, fb_con_share=acc[6] / n, max_con_share=acc[7] / n, fb_label_share=acc[8] / n,
                 max_label_share=acc[9] / n, labelled=acc[10] / n,
                 ps_con_share=float(cs[d['cPS']]),
                 top_contracts=[(cn[c], float(cs[c])) for c in np.argsort(-cs)[:8] if cs[c] > 0],
                 top_labels=[(cn[c], float(ls[c])) for c in np.argsort(-ls)[:8] if ls[c] > 0],
                 top_sources=[(nm[p], float(ss[p])) for p in np.argsort(-ss)[:10] if ss[p] > 0],
                 con_trans=[('none-dominant' if a == 0 else ('no-carriers' if a == NC + 1 else cn[a - 1]), 'none-dominant' if b == 0 else ('no-carriers' if b == NC + 1 else cn[b - 1]), int(con_trans[a, b]))
                            for a, b in zip(*np.nonzero(con_trans))],
                 n_pc_trans=int(pc_trans.sum()),
                 swaps=dict(accepted=int(sw[0].sum()), same=int(sw[1].sum()), rejected=int(sw[2].sum()), donor_none=int(sw[3, 0]),
                            accepted_2nd=int(sw2[0].sum()), same_2nd=int(sw2[1].sum()), rejected_2nd=int(sw2[2].sum()), donor_none_2nd=int(sw2[3, 0]),
                            by_contract=[(cn[c - 1], int(sw[0, c]), int(sw[1, c]), int(sw[2, c])) for c in np.argsort(-(sw[0] + sw[1] + sw[2]))[:10] if (sw[0, c] + sw[1, c] + sw[2, c]) > 0 and c > 0],
                            routes=[('none' if a == 0 else cn[a - 1], cn[b], int(routes[a, b])) for a, b in sorted(zip(*np.nonzero(routes)), key=lambda ab: -routes[ab[0], ab[1]])[:12]],
                            label_changed=int(lsw[0]), label_donor_none=int(lsw[1])),
                 trace=tr.tolist())
    else:
        st = {1: 'frozen', 3: 'metastable', 4: 'unresolved'}.get(int(status), 'running')
        pcc = float(isl_cc.mean())
        r.update(status=st, stop_gen=int(stop_gen), pcc=pcc, outcome=('efficient' if pcc >= 0.95 else ('defecting' if pcc <= 0.05 else 'other')) if st != 'unresolved' else 'unresolved',
                 final_contracts={cn[c - 1] if c > 0 else 'none': int(v) for c, v in enumerate(cnt_con) if v > 0},
                 final_sources={nm[p]: int(v) for p, v in enumerate(cnt_src) if v > 0 and v >= 0.01 * job['N'] * job['I']},
                 swaps=dict(accepted=int(sw[0].sum()), same=int(sw[1].sum()), rejected=int(sw[2].sum()), donor_none=int(sw[3, 0])))
    return r


# ------------------------------------------------------------------ job lists
def grid_jobs(gens=100000, reps=3):
    jobs = []
    for b in ('2', '4', 'inf'):
        combos = [(0, 0.0, 0.0)] + [(0, f0, sg) for f0 in (0.01, 1.0) for sg in (0.0, 0.1, 1.0)] + \
                 [(1, f0, sg) for f0 in (0.0, 0.01, 1.0) for sg in (0.0, 0.1, 1.0)]
        for s, f0, sg in combos:
            for start in ('mu', 'alld'):
                for r in range(reps):
                    jobs.append(dict(b=b, s=s, f0=f0, sigma=sg, start=start, N=6400, I=1, rep=r, gens=gens, eps=1e-3, uniform=False,
                                     lottery=False, mN=0.0, tag='grid'))
        for s in (0, 1):
            for f0 in (0.01, 1.0):
                for r in range(reps):
                    jobs.append(dict(b=b, s=s, f0=f0, sigma=1.0, start='mu', N=6400, I=1, rep=r, gens=gens, eps=1e-3, uniform=True,
                                     lottery=False, mN=0.0, tag='uniform'))
    for N in (1600, 25600):
        for sg in (0.0, 1.0):
            for r in range(reps):
                jobs.append(dict(b='2', s=0, f0=0.01, sigma=sg, start='mu', N=N, I=1, rep=r, gens=gens, eps=1e-3, uniform=False,
                                 lottery=False, mN=0.0, tag='Npath'))
    return jobs


def lottery_jobs(gens=100000, reps=40):
    jobs = []
    for (N, I) in ((100, 4), (400, 4), (100, 64), (100, 256)):
        for b in ('2', 'inf'):
            confs = [(0.0, 0.0)] + [(f0, sg) for f0 in (0.01, 1.0) for sg in (0.0, 1.0)]
            for f0, sg in confs:
                for r in range(reps):
                    jobs.append(dict(b=b, s=0, f0=f0, sigma=sg, start='mu', N=N, I=I, rep=r, gens=gens, eps=0.0, uniform=False,
                                     lottery=True, mN=1.0, tag='lottery'))
    return jobs


def supp_jobs(gens=100000, reps=3):
    jobs = []
    combos = [(0, 0.0, 0.0)] + [(0, f0, sg) for f0 in (0.01, 1.0) for sg in (0.0, 1.0)] + [(1, f0, sg) for f0 in (0.0, 0.01, 1.0) for sg in (0.0, 1.0)]
    for s, f0, sg in combos:
        for r in range(reps):
            jobs.append(dict(b='0', s=s, f0=f0, sigma=sg, start='mu', N=6400, I=1, rep=r, gens=gens, eps=1e-3, uniform=False,
                             lottery=False, mN=0.0, tag='supp'))
    return jobs


def supplottery_jobs(gens=100000, reps=40):
    jobs = []
    for (N, I) in ((100, 4), (400, 4), (100, 64), (100, 256)):
        for f0, sg in [(0.0, 0.0)] + [(f0, sg) for f0 in (0.01, 1.0) for sg in (0.0, 1.0)]:
            for r in range(reps):
                jobs.append(dict(b='0', s=0, f0=f0, sigma=sg, start='mu', N=N, I=I, rep=r, gens=gens, eps=0.0, uniform=False,
                                 lottery=True, mN=1.0, tag='lottery'))
    return jobs


def _key(j):
    return tuple(j[k] for k in ('tag', 'b', 's', 'f0', 'sigma', 'start', 'N', 'I', 'rep', 'uniform'))


def main_run(kind, procs, gens, only=None):
    path = os.path.join(RUNS, 'contracts_%s.json' % kind)
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {_key(r) for r in rows}
    jobs = dict(grid=grid_jobs, lottery=lottery_jobs, supp=supp_jobs, supplottery=supplottery_jobs)[kind](gens)
    if only:
        jobs = [j for j in jobs if j['tag'] in only]
    jobs = [j for j in jobs if _key(j) not in done]
    jobs.sort(key=lambda j: (j['start'] == 'alld', -j['N'] * j['I']))
    for b in (('0',) if kind.startswith('supp') else ('inf', '4', '2')):
        data(b)
    print('%d jobs' % len(jobs), flush=True)
    with Pool(procs) as pool:
        for r in pool.imap_unordered(run_job, jobs):
            rows.append(r)
            if r['lottery']:
                print('lottery N=%d I=%d b=%s f0=%g sigma=%g rep %d: %s %s gen %d P(C,C) %.3f (%.0fs)' % (
                    r['N'], r['I'], r['b'], r['f0'], r['sigma'], r['rep'], r['status'], r['outcome'], r['stop_gen'], r['pcc'], r['time_s']), flush=True)
            else:
                print('%s b=%s s=%d f0=%g sigma=%g %s N=%d rep %d%s: P(C,C) %.3f carrier %.3f FBcon %.3f maxcon %.3f (%.0fs)' % (
                    r['tag'], r['b'], r['s'], r['f0'], r['sigma'], r['start'], r['N'], r['rep'], ' uniform' if r['uniform'] else '',
                    r['pcc'], r['carrier'], r['fb_con_share'], r['max_con_share'], r['time_s']), flush=True)
            json.dump(rows, open(path, 'w'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('kind', choices=['grid', 'lottery', 'supp', 'supplottery', 'test'])
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--gens', type=int, default=100000)
    ap.add_argument('--only', nargs='*')
    a = ap.parse_args()
    if a.kind == 'test':
        for b in ('2',):
            t = time.time()
            r = run_job(dict(b=b, s=0, f0=0.01, sigma=1.0, start='mu', N=6400, I=1, rep=0, gens=a.gens, eps=1e-3, uniform=False, lottery=False, mN=0.0, tag='test'))
            print({k: v for k, v in r.items() if k != 'trace'}, time.time() - t)
    else:
        main_run(a.kind, a.procs, a.gens, a.only)
