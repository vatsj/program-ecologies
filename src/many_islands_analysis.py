"""Analysis helpers for the many-islands experiment: the exact one-migrant kernel at class level (injection
statistics), per-recipient hazards, the fair-to-fair block, the class-level ODE, the two-migrant probes and the
cryptic-drift experiment.  Importable without side effects; the report is many_islands_report.py.
"""
import os, sys, json, math, time, zlib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from numba import njit
import many_islands as MI
import many_islands_run as MR


# ====================================================================== per-recipient hazards (exact)
@njit(cache=True)
def rec_hazard(C, PAYt, VECt, pool, rec_idx, don_idx, N, w, out, fair_mask):
    """For each recipient (rows of rec_idx) and its donors (don_idx[n, :]): the mean over donors and the three slots of
    the exact probability per event that the recipient (a) changes any program (fixation), (b) changes outcome class,
    (c) moves to a fair-pair outcome (from a non-fair one), (d) leaves a fair pair for another outcome, (e) moves from
    one fair pair to another.  out[n, 0..4]."""
    m = don_idx.shape[1]
    for n in range(rec_idx.shape[0]):
        i = rec_idx[n]
        ci = jl(C, pool[i, 0], pool[i, 1], pool[i, 2])
        old = VECt[ci]
        a = 0.0; b = 0.0; c = 0.0; d = 0.0; e = 0.0
        for t in range(m):
            j = don_idx[n, t]
            for s in range(3):
                x = pool[j, s]
                if x == pool[i, s]:
                    continue
                if s == 0:
                    cx = jl(C, x, pool[i, 1], pool[i, 2])
                elif s == 1:
                    cx = jl(C, pool[i, 0], x, pool[i, 2])
                else:
                    cx = jl(C, pool[i, 0], pool[i, 1], x)
                pf = MI.pfix(PAYt[cx, s] - PAYt[ci, s], float(N), w)
                nw = VECt[cx]
                a += pf
                if nw != old:
                    b += pf
                    if fair_mask[nw] and not fair_mask[old]:
                        c += pf
                    if fair_mask[old] and not fair_mask[nw]:
                        d += pf
                    if fair_mask[old] and fair_mask[nw]:
                        e += pf
        norm = 3.0 * m
        out[n, 0] = a / norm; out[n, 1] = b / norm; out[n, 2] = c / norm; out[n, 3] = d / norm; out[n, 4] = e / norm
    return 0


from many_islands import jl


FAIR = np.zeros(MI.NOUT, np.bool_)
FAIR[MI.V] = True


def pool_outcomes(arm, pool):
    ctx = arm.ctx()
    return np.array([MI.VEC[int(MI.jl(ctx, *map(np.int64, t)))] for t in pool], np.int64)


def class_shares(oc):
    return np.bincount(oc, minlength=MI.NOUT) / max(len(oc), 1)


def exact_class_kernel(arm, pool, rng, per_class=2000, m_don=20):
    """K[a, b, c] over outcome classes a, b, c, estimated by exact one-event probabilities on stratified samples:
    recipients up to per_class per class a, m_don donors per recipient and donor class b.  Also returns the pair counts
    and the per-slot fixation / class-change sums, the shares x of the pool and the per-recipient hazards."""
    arm.maybe_flush(0.5)
    ctx = arm.ctx()
    oc = pool_outcomes(arm, pool)
    x = class_shares(oc)
    by = {c: np.nonzero(oc == c)[0] for c in range(MI.NOUT)}
    out = np.zeros((MI.NOUT, MI.NOUT, MI.NOUT)); npair = np.zeros((MI.NOUT, MI.NOUT)); outslot = np.zeros((MI.NOUT, 3, 2))
    for a in range(MI.NOUT):
        if len(by[a]) == 0:
            continue
        rec = by[a] if len(by[a]) <= per_class else rng.choice(by[a], per_class, replace=False)
        for b in range(MI.NOUT):
            if len(by[b]) == 0:
                continue
            don = rng.choice(by[b], (len(rec), m_don))
            r_ = np.repeat(rec, m_don).astype(np.int64); d_ = don.reshape(-1).astype(np.int64)
            keep = r_ != d_
            MI.exact_rates(ctx, MI.PAY, MI.VEC, pool, r_[keep], d_[keep], MI.N0, MI.W, out, npair, outslot)
    return normalize_K(out, npair), npair, x, oc, outslot, out


def normalize_K(out, npair):
    K = np.zeros_like(out)
    for a in range(MI.NOUT):
        for b in range(MI.NOUT):
            if npair[a, b] > 0:
                K[a, b] = out[a, b] / npair[a, b]
            else:
                K[a, b, a] = 1.0                  # an unobserved cell: stay (it carries no mass)
    return K


def recipient_hazards(arm, pool, oc, rng, per_class=2000, m_don=40):
    """per-recipient exact hazards with donors uniform from the whole pool: dict class -> array (n, 5)."""
    ctx = arm.ctx()
    res = {}
    for a in range(MI.NOUT):
        idx = np.nonzero(oc == a)[0]
        if len(idx) == 0:
            continue
        rec = idx if len(idx) <= per_class else rng.choice(idx, per_class, replace=False)
        don = rng.integers(0, len(pool), (len(rec), m_don)).astype(np.int64)
        out = np.zeros((len(rec), 5))
        rec_hazard(ctx, MI.PAY, MI.VEC, pool, rec.astype(np.int64), don, MI.N0, MI.W, out, FAIR)
        res[a] = out
    return res


def fair_block(K, x):
    """flows (shares per event) between the three fair pairs: flow[p, q] = x_p * sum_b x_b K[p, b, q]; the antisymmetric
    part D_pq = flow[p, q] - flow[q, p]."""
    V = MI.V
    flow = np.zeros((3, 3))
    for i, p in enumerate(V):
        for j, q in enumerate(V):
            if i != j:
                flow[i, j] = x[p] * np.einsum('b,b->', x, K[p, :, q])
    D = flow - flow.T
    return flow, D


# ====================================================================== two-migrant probes
def event_dist(arm, tr, s, x):
    """(p, new triple) as event_prob."""
    return MI.event_prob(arm, tr, s, x)


def sequential_dist(arm, a, d, s1, s2):
    """exact distribution over outcome classes after two single-migrant events from the same donor triple d into slots s1
    then s2 (full relaxation between): dict class -> prob."""
    out = {}
    p1, a1 = MI.event_prob(arm, a, s1, d[s1])
    for (st, w1) in ((a, 1.0 - p1), (a1, p1)):
        if w1 <= 0:
            continue
        p2, st2 = MI.event_prob(arm, st, s2, d[s2])
        for (fin, w2) in ((st, 1.0 - p2), (st2, p2)):
            if w2 <= 0:
                continue
            c = MI.outcome_of(arm, fin)
            out[c] = out.get(c, 0.0) + w1 * w2
    return out


def overlap_sim(arm, a, d, s1, s2, seed, N=MI.N0):
    """simulate two simultaneous migrants (donor's programs in slots s1, s2) into the settled island a; returns
    (status, triple or None, outcome class or None)."""
    init = np.zeros((3, arm.K), np.int64)
    for t in range(3):
        init[t, a[t]] = N
    init[s1, a[s1]] -= 1; init[s1, d[s1]] += 1
    init[s2, a[s2]] -= 1; init[s2, d[s2]] += 1
    st, g, counts, na = MI.island_run(arm.ctx(), arm.lc(32), MI.PAY, init, N, MI.W, seed, 20000, np.empty(0), arm.cum, True)
    if st != 0:
        return 1, None, None
    tr = MI.triple_of(counts)
    return 0, tr, MI.outcome_of(arm, tr)


def two_migrant_probe(arm, pool, oc, rng, n_per_cell=200, seed0=0):
    """For each recipient group g_a and donor group g_b in {F, U, G, W, D}: n_per_cell tuples (recipient, donor, ordered
    distinct slots); exact sequential distribution and simulated overlap.  Group of a class = CATMAP.  Reports, per cell,
    P(class changes) and P(new class is F) for single (first migrant only, exact), sequential and overlap."""
    arm.maybe_flush(0.5)
    cat = MI.CATMAP[oc]
    res = {}
    for ga in range(5):
        ia = np.nonzero(cat == ga)[0]
        if len(ia) == 0:
            continue
        for gb in range(5):
            ib = np.nonzero(cat == gb)[0]
            if len(ib) == 0:
                continue
            acc = dict(n=0, single_change=0.0, single_toF=0.0, seq_change=0.0, seq_toF=0.0, ov_change=0, ov_toF=0, ov_capped=0)
            for k in range(n_per_cell):
                i = int(rng.choice(ia)); j = int(rng.choice(ib))
                if i == j:
                    continue
                s1, s2 = (int(v) for v in rng.permutation(3)[:2])
                a = tuple(int(v) for v in pool[i]); d = tuple(int(v) for v in pool[j])
                c0 = int(oc[i])
                # single migrant (the first only)
                p1, a1 = MI.event_prob(arm, a, s1, d[s1])
                c1 = MI.outcome_of(arm, a1) if p1 > 0 else c0
                acc['single_change'] += p1 * (c1 != c0)
                acc['single_toF'] += p1 * (FAIR[c1] and not FAIR[c0])
                dist = sequential_dist(arm, a, d, s1, s2)
                acc['seq_change'] += sum(v for c, v in dist.items() if c != c0)
                acc['seq_toF'] += sum(v for c, v in dist.items() if FAIR[c] and not FAIR[c0])
                st, tr, c = overlap_sim(arm, a, d, s1, s2, seed0 + 7919 * (ga * 5 + gb) + k)
                if st:
                    acc['ov_capped'] += 1
                else:
                    acc['ov_change'] += (c != c0)
                    acc['ov_toF'] += bool(FAIR[c] and not FAIR[c0])
                acc['n'] += 1
            res['%s>%s' % (MI.CATLAB[ga], MI.CATLAB[gb])] = acc
    return res


# ====================================================================== cryptic drift: neutral substitution of the excluded slot
def cryptic_drift(arm, pool, oc, rng, groups=(0, 1, 3), per_group=1500, m_don=40):
    """For recipients on an excluded-slot outcome (fair, unequal, wasteful pairs): the exact hazard per event (donors
    uniform from the pool) before and after one neutral substitution of the excluded slot's program (a program drawn from
    a random island's same slot, accepted only if the outcome class is unchanged).  Paired."""
    arm.maybe_flush(0.5)
    ctx = arm.ctx()
    cat = MI.CATMAP[oc]
    res = {}
    for g in groups:
        idx = np.nonzero((cat == g) & (MI.EXCL[oc] >= 0))[0]
        if len(idx) == 0:
            continue
        rec = rng.choice(idx, min(per_group, len(idx)), replace=False)
        newpool = []
        keep = []
        for i in rec:
            e = int(MI.EXCL[oc[i]])
            for _ in range(30):
                x = int(pool[rng.integers(len(pool)), e])
                tr = list(pool[i]); tr[e] = x
                if x != pool[i, e] and MI.outcome_of(arm, tuple(tr)) == oc[i]:
                    newpool.append(tr); keep.append(i); break
        if not keep:
            continue
        keep = np.array(keep, np.int64)
        # evaluate hazards: the recipients are rows of `pool` for 'before' and of a copy with the replaced triples for 'after'
        P2 = pool.copy()
        for i, tr in zip(keep, newpool):
            P2[i] = tr
        don = rng.integers(0, len(pool), (len(keep), m_don)).astype(np.int64)
        before = np.zeros((len(keep), 5)); after = np.zeros((len(keep), 5))
        rec_hazard(ctx, MI.PAY, MI.VEC, pool, keep, don, MI.N0, MI.W, before, FAIR)
        rec_hazard(ctx, MI.PAY, MI.VEC, P2, keep, don, MI.N0, MI.W, after, FAIR)
        res[MI.CATLAB[g]] = dict(n=int(len(keep)), before=before.mean(0).tolist(), after=after.mean(0).tolist(),
                                 ratio_toF=float(after[:, 2].mean() / max(before[:, 2].mean(), 1e-300)),
                                 ratio_change=float(after[:, 1].mean() / max(before[:, 1].mean(), 1e-300)))
    return res


# ====================================================================== the post-processing job for one (arm, A)
TQ = {1: 12.71, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571}      # 0.975 t quantiles, df = n - 1 for n = 2..6 pools


def tint(vals):
    v = np.asarray(vals, float)
    n = len(v)
    if n < 2:
        return [float(v.mean()), float('nan'), float('nan')]
    h = TQ.get(n - 1, 2.0) * v.std(ddof=1) / math.sqrt(n)
    return [float(v.mean()), float(v.mean() - h), float(v.mean() + h)]


def post_job(arm_name, A, npools=5, probe_n=200):
    t0 = time.time()
    arm = MI.Arm(arm_name); arm.new_cache(24)
    rng = np.random.default_rng(MR.crc('mi-post|%s|%d' % (arm_name, A)))
    pools = []
    for k in range(npools):
        if os.path.exists(MR.pool_path(arm_name, A, k)):
            pools.append(MR.load_pool(arm_name, A, k))
    res = dict(arm=arm_name, A=A, npools=len(pools))
    shares = []; Ks = []; flows = []; Ds = []; outs = []; npairs = []
    for k, (tr, info) in enumerate(pools):
        K, npair, x, oc, outslot, out = exact_class_kernel(arm, tr, rng)
        shares.append(x); Ks.append(K); outs.append(out); npairs.append(npair)
        fl, D = fair_block(K, x)
        flows.append(fl); Ds.append(D)
        if k == 0:
            res['capped_pool0'] = info['capped']
    shares = np.array(shares)
    xm = shares.mean(0)
    res['post_shares'] = {MI.OLAB[c]: tint(shares[:, c]) for c in range(MI.NOUT) if xm[c] > 0}
    res['post_summary'] = [MR.summarize_hist(np.round(sh * 1e6).astype(np.int64)) for sh in shares]
    Dm = np.array([[D[0, 1], D[0, 2], D[1, 2]] for D in Ds])               # antisymmetric entries D01, D02, D12
    Fm = np.array([[fl[i, j] for i in range(3) for j in range(3) if i != j] for fl in flows])
    res['fair_block'] = dict(D=[tint(Dm[:, q]) for q in range(3)], flow_mean=Fm.mean(0).tolist(),
                             D_over_flow=[float(abs(Dm[:, q].mean()) / max(Fm.mean(), 1e-300)) for q in range(3)])
    # pooled kernel and the class-level ODE
    out = sum(outs); npair = sum(npairs)
    Kp = normalize_K(out, npair)
    ts, Xt = MI.ode_integrate(Kp, xm / xm.sum(), 1e5, 70)
    res['ode'] = dict(t=ts.tolist(), V=Xt[:, MI.V].sum(1).tolist(),
                      cat={MI.CATLAB[c]: Xt[:, MI.CATMAP == c].sum(1).tolist() for c in range(5)},
                      pair=[Xt[:, v].tolist() for v in MI.V], mass_err=float(np.abs(Xt.sum(1) - 1).max()), min_x=float(Xt.min()))
    # per-recipient hazards (pool 0): heterogeneity within classes
    tr0 = pools[0][0]
    oc0 = pool_outcomes(arm, tr0)
    hz = recipient_hazards(arm, tr0, oc0, rng)
    cats = MI.CATMAP
    het = {}
    for g in range(5):
        v = np.concatenate([hz[c][:, 1] for c in hz if cats[c] == g]) if any(cats[c] == g for c in hz) else np.zeros(0)
        vf = np.concatenate([hz[c][:, 2] for c in hz if cats[c] == g]) if any(cats[c] == g for c in hz) else np.zeros(0)
        if len(v):
            het[MI.CATLAB[g]] = dict(n=int(len(v)), mean_exit=float(v.mean()), sd_exit=float(v.std()),
                                     cv_exit=float(v.std() / max(v.mean(), 1e-300)), mean_toF=float(vf.mean()),
                                     frac_zero_exit=float((v < 1e-12).mean()), q90_exit=float(np.quantile(v, 0.9)),
                                     q50_exit=float(np.quantile(v, 0.5)))
    res['heterogeneity'] = het
    res['hazard_by_class'] = {MI.OLAB[c]: dict(n=int(len(hz[c])), mean=hz[c].mean(0).tolist()) for c in hz}
    res['cryptic'] = cryptic_drift(arm, tr0, oc0, rng)
    # injection statistics repeated on triples sampled during migration (dumps at 10, 100, 1000 events per island)
    dp = os.path.join(MR.OUT, 'dump_%s_A%d.npz' % (arm_name, A))
    inj = {}
    if os.path.exists(dp):
        z = np.load(dp)
        for key in z.files:
            P = z[key].astype(np.int64)
            Kd, npd, xd, ocd, osd, outd = exact_class_kernel(arm, P, rng, per_class=1000, m_don=20)
            hzd = recipient_hazards(arm, P, ocd, rng, per_class=1000, m_don=20)
            rows = {}
            for g in range(5):
                parts = [hzd[c] for c in hzd if cats[c] == g]
                if parts:
                    v = np.concatenate(parts)
                    rows[MI.CATLAB[g]] = dict(n=int(len(v)), exit=float(v[:, 1].mean()), toF=float(v[:, 2].mean()),
                                              cv=float(v[:, 1].std() / max(v[:, 1].mean(), 1e-300)))
            fl_, D_ = fair_block(Kd, xd)
            inj[key] = dict(shares={MI.CATLAB[c]: float(xd[cats == c].sum()) for c in range(5)}, by_group=rows,
                            D=[float(D_[0, 1]), float(D_[0, 2]), float(D_[1, 2])], flow=float(fl_[~np.eye(3, dtype=bool)].mean()))
    res['injection_at_checkpoints'] = inj
    res['two_migrant'] = two_migrant_probe(arm, tr0, oc0, rng, n_per_cell=probe_n, seed0=MR.crc('mi-2m|%s|%d' % (arm_name, A)) % 10 ** 6)
    res['wall'] = time.time() - t0
    with open(os.path.join(MR.OUT, 'post_%s_A%d.json' % (arm_name, A)), 'w') as f:
        json.dump(res, f)
    return res


if __name__ == '__main__':
    r = post_job(sys.argv[1], int(sys.argv[2]), npools=int(sys.argv[3]) if len(sys.argv) > 3 else 5)
    print(json.dumps({k: r[k] for k in ('arm', 'A', 'npools', 'wall')}))
