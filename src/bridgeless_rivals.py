"""Bridge-less rivals: their prior mass in n, and mediation before loss at N >= 200.
Spec specs/2026-10-05-bridgeless-rivals.md (reviewed, reviews/2026-10-05-bridgeless-rivals-gpt-6.1-sol.md);
predictions predictions/2026-10-05-bridgeless-rivals.md.

Static screening.  The modal language is evaluated once at the largest feasible cutoff (moat_static_big's packed
evaluator, one byte per canonical pair, as seeds_tail Part A); smaller cutoffs are sub-blocks (canonical ids are a
prefix).  n = 15 does not fit: 374,074 canonical functions, 140 GB at one byte per pair; n = 14 (126,370; 16 GB) does
not fit either.  The largest cutoff is n = 13 (51,234 canonical functions, 2.6 GB).  Classes are merged within L_n by
identical row and column, as modal.ModalProvider; masses per class in cut units (normalized within the cutoff), raw
units (the infinite length prior, shell s has mass 1/(2 s^2)) and inf units (raw / (pi^2/12)).

Definitions (spec, [after review]).  A = {FairBot = BOX(THEM(ME)), BOX1(THEM(ME))}.
  establisher        self-cooperates, defects on D, not ALLC.  cooperative class: self-cooperates, not ALLC.
  rival of A         an establisher that mutually defects with some member of A (primary; as rival_islands' static);
                     "full rival": mutually defects with both members.
  pairwise bridge    of (A, R): a cooperative class, not in A, that mutually cooperates with both members of A and with R.
  safe bridge        a pairwise bridge that is an establisher.
  bridge mass        total cut mass of the pairwise bridges; heaviest bridge; safe bridge mass.
  tau                sensitivity threshold on the heaviest bridge (cut units): R is bridge-less at tau iff its heaviest
                     bridge has mass <= tau (tau = 0: literally no bridge).  tau in {0, 1e-5, 1e-4, 1e-3}.
  prey of R          a class that cooperates with R while R defects on it; reported among A's network (cooperative
                     classes mutually cooperating with both members of A) and among the union of all rivals' bridges.
  mediator           a cooperative class, not a pairwise bridge, that is neutral or better against FairBot,
                     BOX1(THEM(ME)) and R in pairwise one-migrant fixation at N = 200 (rho(M into all-X) >= 1/N).  With
                     both classes self-cooperating, rho depends only on the pair's outcome, so "neutral or better" is
                     "X cooperates with M"; FairBot's pair is unfakeable, so a mediator mutually cooperates with A and
                     fakes R (R cooperates with it, it defects on R): a two-step path R -> M ~ A.
  connectivity       shortest path from R to A (either member) in the mutual-cooperation graph over establishers.

    python3 src/bridgeless_rivals.py classes        # evaluate n = 13, class data for n = 9, 12, 13 -> cache/
    python3 src/bridgeless_rivals.py static         # screening -> runs/bridgeless-rivals-static.json
"""
import argparse, gzip, json, math, os, sys, time
from collections import Counter, defaultdict, deque
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
CACHE = os.path.join(ROOT, 'cache')
STATIC = os.path.join(RUNS, 'bridgeless-rivals-static.json')
W = 0.3
NMAX = 13
NS = (9, 12, 13)
Z_INF = math.pi ** 2 / 12
TAUS = (0.0, 1e-5, 1e-4, 1e-3)
PDP = np.array([[-1.0, 1.0], [-2.0, 0.0]])       # pay[a][b], level order (D, C), as modal.PD
FB, FB1 = 'BOX(THEM(ME))', 'BOX1(THEM(ME))'
PROBE, PROBE1 = 'BOX(THEM(^C))', 'BOX1(THEM(^C))'


def retained(n):
    return sum(1 / (2 * s * s) for s in range(1, n + 1))


# ------------------------------------------------------------------ class data
def classes_main(a):
    from numba import set_num_threads
    import moat_static_big as MB
    import seeds_tail as ST
    set_num_threads(a.threads)
    os.makedirs(CACHE, exist_ok=True)
    t0 = time.time()
    L = MB.CountedLanguage(NMAX)
    nat, ak, al, af, aa, tt = L.arrays()
    nlev = int(al.max()) + 1
    T, nf = MB._traces(nat, ak, al, af, aa, tt, 200, nlev)
    if nf < 0:
        raise RuntimeError('did not stabilize')
    MB._to_stable(T, nf); V = T
    Kmax = V.shape[0]
    print('evaluated n=%d: %d canons, stable at world %d, %.0fs' % (NMAX, Kmax, nf, time.time() - t0), flush=True)
    cnt = L.size_counts(); a_s = L.a
    w_prog = np.array([0.0] + [1.0 / (2.0 * a_s[s] * s * s) for s in range(1, NMAX + 1)])
    mshell = np.zeros((Kmax, NMAX + 1))
    for s in range(1, NMAX + 1):
        for c, m in cnt[s].items():
            mshell[c, s] += m * w_prog[s]
    first = np.full(Kmax, NMAX + 1)
    for s in range(NMAX, 0, -1):
        for c in cnt[s]:
            first[c] = s
    rng_w = np.random.default_rng(12345)
    w1 = rng_w.integers(1, 2**63, Kmax, dtype=np.uint64); w2 = rng_w.integers(1, 2**63, Kmax, dtype=np.uint64)
    for n in NS:
        K = int((first <= n).sum())
        assert (first[:K] <= n).all() and (first[K:] > n).all()
        raw = mshell[:K, 1:n + 1].sum(1)
        hr, hc = ST._hash_sub(V, K, w1, w2)
        groups = defaultdict(list)
        for c in range(K):
            groups[(int(hr[c]), int(hc[c]))].append(c)
        cls = []
        for mem in groups.values():
            rep = min(mem, key=lambda c: (L.bits_canon[c], c))
            for c in mem:
                assert c == rep or ST._same_sub(V, K, rep, c), 'hash collision'
            cls.append((rep, mem, float(raw[mem].sum())))
        cls.sort(key=lambda t: -t[2])
        reps = np.array([t[0] for t in cls], np.int64)
        rawc = np.array([t[2] for t in cls])
        cls_of = np.full(K, -1, np.int64)
        for j, t in enumerate(cls):
            cls_of[np.array(t[1], np.int64)] = j
        Vc = np.ascontiguousarray(V[np.ix_(reps, reps)]).astype(np.uint8)
        names = np.array([L.rep[r] for r in reps])
        np.save(os.path.join(CACHE, 'bridgeless-V%d.npy' % n), Vc)
        np.savez(os.path.join(CACHE, 'bridgeless-meta%d.npz' % n), raw=rawc, names=names, reps=reps, cls_of=cls_of,
                 nmem=np.array([len(t[1]) for t in cls]), retained=retained(n), K=K)
        print('n=%d: %d canons, %d classes, retained %.6f, raw total %.6f (%.0fs)' % (
            n, K, len(cls), retained(n), rawc.sum(), time.time() - t0), flush=True)
        del Vc


_D = {}


def cdata(n):
    if n in _D:
        return _D[n]
    V = np.load(os.path.join(CACHE, 'bridgeless-V%d.npy' % n), mmap_mode='r')
    z = np.load(os.path.join(CACHE, 'bridgeless-meta%d.npz' % n))
    names = [str(x) for x in z['names']]
    raw = z['raw']
    selfc = np.array(np.diagonal(V)).astype(bool)
    iC = names.index('C'); iD = names.index('D')
    allc = np.array([bool(np.asarray(V[k]).all()) for k in range(len(names))])
    vD = np.asarray(V[:, iD]).astype(bool)
    d = dict(n=n, V=V, raw=raw, mu=raw / raw.sum(), names=names, idx={x: i for i, x in enumerate(names)},
             reps=z['reps'], cls_of=z['cls_of'], retained=float(z['retained']), selfc=selfc, iC=iC, iD=iD,
             allc=allc, est=selfc & ~vD & ~allc, coop=selfc & ~allc)
    _D[n] = d
    return d


# ------------------------------------------------------------------ static screening
def fix1(N, uqq, uqa, uaq, uaa, k=1):
    """P(k copies of q fix against resident a): Moran birth-death, parent ~ count * exp(w * mean payoff, self
    excluded), victim uniform (rival_islands.fix_k)."""
    import rival_islands as R
    return R.fix_k(N, W, k, uqq, uqa, uaq, uaa)


def rho_case(N):
    """One-migrant fixation of a self-cooperator q into an all-x island of another self-cooperator, by outcome
    (q's play, x's play) against each other."""
    out = {}
    for vq in (0, 1):
        for vx in (0, 1):
            out[(vq, vx)] = fix1(N, 0.0, PDP[vq, vx], PDP[vx, vq], 0.0)
    return out


def screen(n, refs, rhoN=200):
    """Rivals of the reference pair `refs` (two class names) at cutoff n with bridges, prey, mediators, connectivity."""
    d = cdata(n)
    V = np.asarray(d['V']).astype(bool)
    K = V.shape[0]
    mu = d['mu']; raw = d['raw']; nm = d['names']
    a0, a1 = d['idx'][refs[0]], d['idx'][refs[1]]
    coop, est = d['coop'], d['est']
    MC = lambda x: V[x, :] & V[:, x]
    MD = lambda x: ~V[x, :] & ~V[:, x]
    notA = np.ones(K, bool); notA[[a0, a1]] = False
    netA = coop & MC(a0) & MC(a1)
    md0, md1 = MD(a0), MD(a1)
    riv = est & (md0 | md1)
    full = est & md0 & md1
    R_ = np.nonzero(riv)[0]
    R_ = R_[np.argsort(-mu[R_])]
    rc = rho_case(rhoN); inv = 1.0 / rhoN
    # multi-source BFS from A over the mutual-cooperation graph among establishers (and A)
    E = np.nonzero(est | ~notA)[0]
    pos = -np.ones(K, np.int64); pos[E] = np.arange(len(E))
    adj = V[np.ix_(E, E)] & V[np.ix_(E, E)].T
    dist = -np.ones(len(E), np.int64)
    dq = deque()
    for s in (a0, a1):
        dist[pos[s]] = 0; dq.append(pos[s])
    while dq:
        u = dq.popleft()
        for v in np.nonzero(adj[u] & (dist < 0))[0]:
            dist[v] = dist[u] + 1; dq.append(v)
    rows = []
    union_br = np.zeros(K, bool)
    for r in R_:
        mcr = MC(r)
        br = netA & mcr & notA
        union_br |= br
        safe = br & est
        bi = np.nonzero(br)[0]
        hb = int(bi[np.argmax(mu[bi])]) if len(bi) else -1
        si = np.nonzero(safe)[0]
        hs = int(si[np.argmax(mu[si])]) if len(si) else -1
        prey = V[:, r] & ~V[r, :]                     # x cooperates with R, R defects on x
        # mediators: cooperative, not a bridge, not in A, and each of a0, a1, r cooperates with it (rho >= 1/N)
        medm = coop & notA & ~br & V[a0, :] & V[a1, :] & V[r, :]
        medm[r] = False
        mi = np.nonzero(medm)[0]
        # rho check (all classes self-cooperate): rho(M into all-X) by the outcome pair (V[M, X], V[X, M])
        ok = all(rc[(int(V[m, x]), int(V[x, m]))] >= inv * (1 - 1e-9) for m in mi[:50] for x in (a0, a1, r))
        assert ok
        rows.append(dict(name=nm[r], mu=float(mu[r]), raw=float(raw[r]), full=bool(full[r]),
                         md=[bool(md0[r]), bool(md1[r])],
                         n_bridges=int(br.sum()), bridge_mass=float(mu[br].sum()), bridge_raw=float(raw[br].sum()),
                         heaviest_bridge=nm[hb] if hb >= 0 else None, heaviest_bridge_mu=float(mu[hb]) if hb >= 0 else 0.0,
                         n_safe=int(safe.sum()), safe_mass=float(mu[safe].sum()),
                         heaviest_safe=nm[hs] if hs >= 0 else None, heaviest_safe_mu=float(mu[hs]) if hs >= 0 else 0.0,
                         prey_netA_mass=float(mu[prey & netA].sum()), n_prey_netA=int((prey & netA).sum()),
                         prey_netA_top=[(nm[x], float(mu[x])) for x in sorted(np.nonzero(prey & netA)[0], key=lambda x: -mu[x])[:3]],
                         n_mediators=int(len(mi)), mediator_mass=float(mu[mi].sum()),
                         mediator_est_mass=float(mu[mi[est[mi]]].sum()) if len(mi) else 0.0,
                         mediator_top=[(nm[x], float(mu[x])) for x in sorted(mi, key=lambda x: -mu[x])[:3]],
                         path_len=int(dist[pos[r]]) if dist[pos[r]] >= 0 else None,
                         rho_R_into=[rc[(int(V[r, x]), int(V[x, r]))] for x in (a0, a1)],
                         rho_into_R=[rc[(int(V[x, r]), int(V[r, x]))] for x in (a0, a1)],
                         rep_canon=int(d['reps'][r]), cls=int(r)))
    # prey among the union of all rivals' bridges (bridges of other rivals that R eats)
    for row in rows:
        r = row['cls']
        prey = V[:, r] & ~V[r, :]
        row['prey_bridges_mass'] = float(mu[prey & union_br].sum())
        row['prey_bridges_top'] = [(nm[x], float(mu[x])) for x in sorted(np.nonzero(prey & union_br)[0], key=lambda x: -mu[x])[:3]]
    tot = float(mu[R_].sum())
    agg = {}
    for tau in TAUS:
        for key, col in (('heaviest', 'heaviest_bridge_mu'), ('total', 'bridge_mass'), ('safe', 'heaviest_safe_mu')):
            bl = [r for r in rows if r[col] <= tau]
            mbl = float(sum(r['mu'] for r in bl)); mbr = tot - mbl
            agg['%s|%g' % (key, tau)] = dict(n_bridgeless=len(bl), n_bridged=len(rows) - len(bl),
                                             bridgeless_mu=mbl, bridged_mu=mbr, frac=mbl / tot if tot else None,
                                             ratio=mbl / mbr if mbr > 0 else None,
                                             bridgeless_raw=float(sum(r['raw'] for r in bl)))
    out = dict(n=n, refs=list(refs), K=K, n_canon=int(len(d['cls_of'])), retained=d['retained'],
               omitted=Z_INF - d['retained'], n_rivals=len(rows), n_full=int(full.sum()), rival_mu=tot,
               rival_raw=float(raw[R_].sum()), rival_inf=float(raw[R_].sum() / Z_INF),
               est_mu=float(mu[est].sum()), netA_mu=float(mu[netA].sum()), union_bridge_mu=float(mu[union_br].sum()),
               connected=int(sum(1 for r in rows if r['path_len'] is not None)),
               path_hist=dict(Counter(str(r['path_len']) for r in rows)),
               rho=dict(('%d%d' % k, v) for k, v in rc.items()), agg=agg, rivals=rows)
    return out


def track(stat, lo, hi):
    """Rivals at cutoff lo (by representative canon) followed to cutoff hi: class splits and bridge gains."""
    dlo, dhi = cdata(lo), cdata(hi)
    S_lo = {r['cls']: r for r in stat[lo]['rivals']}
    S_hi = {r['cls']: r for r in stat[hi]['rivals']}
    out = []
    for c, r in S_lo.items():
        mem = np.nonzero(dlo['cls_of'] == c)[0]
        tgt = sorted(set(int(x) for x in dhi['cls_of'][mem]))
        rh = [S_hi.get(t) for t in tgt]
        assert all(x is not None for x in rh), 'rival status is per canon and cutoff-invariant'
        out.append(dict(name=r['name'], mu_lo=r['mu'], split=len(tgt), hb_lo=r['heaviest_bridge_mu'],
                        hb_hi=max(x['heaviest_bridge_mu'] for x in rh), bm_lo=r['bridge_mass'],
                        bm_hi=max(x['bridge_mass'] for x in rh),
                        gained=bool(r['n_bridges'] == 0 and min(x['n_bridges'] for x in rh) > 0),
                        gained_any=bool(r['n_bridges'] == 0 and max(x['n_bridges'] for x in rh) > 0),
                        hi_names=[x['name'] for x in rh][:4],
                        new_bridges=[x['heaviest_bridge'] for x in rh][:4]))
    return out


def static_main(a):
    t0 = time.time()
    res = dict(ns=list(NS), taus=list(TAUS), note_n15='n = 15: 374,074 canonical functions (140 GB at one byte per '
               'pair); n = 14: 126,370 (16 GB); neither fits. Largest cutoff n = 13 (51,234 canonical functions).')
    for refs, key in (((FB, FB1), 'A'), ((PROBE, PROBE1), 'probe')):
        st = {}
        for n in NS:
            st[n] = screen(n, refs)
            g = st[n]['agg']
            print('[%s] n=%d: %d classes, %d rivals (%d full), rival mu %.3g raw %.3g; bridgeless frac tau=0 %.3f, '
                  'tau=1e-4 %.3f; path %s (%.0fs)' % (key, n, st[n]['K'], st[n]['n_rivals'], st[n]['n_full'],
                  st[n]['rival_mu'], st[n]['rival_raw'], g['heaviest|0']['frac'] or 0, g['heaviest|0.0001']['frac'] or 0,
                  st[n]['path_hist'], time.time() - t0), flush=True)
        tr = {'%d-%d' % (lo, hi): track(st, lo, hi) for lo, hi in ((9, 12), (12, 13), (9, 13))}
        res[key] = dict(stat={str(n): st[n] for n in NS}, track=tr)
    json.dump(res, open(STATIC, 'w'), indent=1)
    print('saved %s (%.0fs)' % (STATIC, time.time() - t0))


# ------------------------------------------------------------------ enriched lottery (dynamics)
# Kernel: rival_islands._kern unchanged (exact skipping, lumping, ancestry labels, strong-holder log), n = 9 class data
# (rival_islands.cls(9)), modal arm, PD, w = 0.3, eps = 0, complete island graph, generation = I*N births.
# Network tags for a forced rival R: the kernel's tags for the pair (BOX1(THEM(ME)), R): 1 = A's network (mutually
# cooperates with BOX1(THEM(ME)) and not with R), 2 = R's network, 3 = mutual cooperator with both (bridge), 0 = other.
SALT = 20261007
GENS = 100000
EXPS = ('dense', 'sparse', 'nobridge', 'iid', 'nat', 'scale', 'time')
FORCED = os.path.join(RUNS, 'bridgeless-rivals-forced.json')    # the six forced rivals, chosen from the static screening


def forced():
    return json.load(open(FORCED))


def boundary():
    import island_path as IP
    return IP.boundary()


def seeds(N, I, rep, rival, preset, exp, mN, gens):
    """Initial state depends only on (N, I, rep, rival, preset): the m = 0 reference shares it."""
    import zlib
    rh = 0 if rival is None else zlib.crc32(rival.encode()) % 100003
    pc = ('iid', 'dense', 'sparse', 'nobridge').index(preset)
    rs = [SALT, N, I, rep, rh, pc]
    ss = (1000003 * rep + 7919 * EXPS.index(exp) + 104729 * pc + 13 * N + 17 * I + int(round(mN * 1000)) + 31 * rh
          + 101 * (gens // 1000) + SALT) % (2 ** 31 - 1)
    return rs, ss


def pair_bridges9(d, R):
    """Classes removed in the bridge-removed cell: the static pairwise bridges of (A, R) (mutual cooperators with
    FairBot, BOX1(THEM(ME)) and R) together with the kernel's tag-3 classes (mutual cooperators with BOX1(THEM(ME))
    and R), cooperative, not in A."""
    import rival_islands as R_
    V = np.asarray(d['V']).astype(bool)
    a0, a1 = d['idx'][FB], d['idx'][FB1]
    MC = lambda x: V[x, :] & V[:, x]
    br = d['coop'] & ((MC(a0) & MC(a1) & MC(R)) | (MC(a_ref(d, R)) & MC(R)))
    br[[a0, a1]] = False
    return br


def a_ref(d, R):
    """The member of A the kernel's tags are taken against: BOX1(THEM(ME)) if R mutually defects with it, else FairBot."""
    a0, a1 = d['idx'][FB], d['idx'][FB1]
    V = d['V']
    return a1 if (V[R, a1] == 0 and V[a1, R] == 0) else a0


def build_init(d, N, I, rival, preset, rng):
    K = len(d['mu'])
    mu = d['mu']
    R = None if rival is None else d['idx'][rival]
    removed = 0.0
    if preset == 'nobridge':
        br = pair_bridges9(d, R)
        removed = float(mu[br].sum())
        mu = mu.copy(); mu[br] = 0.0; mu = mu / mu.sum()
    init = np.zeros((I, K), np.int64)
    for i in range(I):
        forced_here = preset in ('dense', 'nobridge') or (preset == 'sparse' and i < I // 4)
        if forced_here:
            init[i] = rng.multinomial(N - 1, mu); init[i, R] += 1
        else:
            init[i] = rng.multinomial(N, mu)
    return init, np.zeros(I, np.int64), R, removed


def tr_trace(trace, col, gmax):
    return [(int(g), int(v)) for g, v in zip(trace[:, 0], trace[:, col]) if g <= gmax]


def job(j):
    import rival_islands as R_
    import island_path as IP
    exp, N, I, mN, rep, gens, rival, preset = j
    d = R_.cls(9); nm = d['names']
    rs, ss = seeds(N, I, rep, rival, preset, exp, mN, gens)
    rng = np.random.default_rng(rs)
    init, pre, Rc, removed = build_init(d, N, I, rival, preset, rng)
    A1 = a_ref(d, Rc) if Rc is not None else None
    t0 = time.time()
    sup, U, PCC, coop, tag = R_.restrict(d, init, A1, Rc)
    li = np.ascontiguousarray(init[:, sup]); K = len(sup)
    rr = np.random.default_rng(ss); r1 = rr.random(K); r2 = rr.random(K)
    iDl = int(np.searchsorted(sup, d['iD'])) if d['iD'] in set(sup.tolist()) else -1
    o = R_._kern(U, PCC, coop, tag, li, N, W, mN / N, ss, R_.checks_schedule(gens), True, iDl, r1, r2, pre, 1)
    (st, sg, counts, isl_cc, isl_pay, trace, t_ext, held_zero, parent, t_est, e_arr, e_arrC, e_arrD, e_imm, e_hold, e_hloc,
     t90, a90, imm90, h90, hl90, arr_all, loss_log, nloss, first_sep, sep_a, sep_b, nsepchk, tr_log, ntr, mig_ct) = o
    G = lambda x: nm[int(sup[x])] if x >= 0 else None
    root = np.arange(K)
    for x in range(K):
        r_ = x
        while parent[r_] != r_: r_ = parent[r_]
        root[x] = r_
    glob = counts.sum(0)
    hold = np.array([R_.holder(counts[i]) for i in range(I)])
    htag = tag[hold]
    estd = t_est >= 0
    loc_est = estd & (e_hloc >= 0.5)
    loc_end = loc_est & (root[np.maximum(e_hold, 0)] == hold)
    x = glob / glob.sum(); pr = np.nonzero(x)[0]
    cf = float(x[pr] @ PCC[np.ix_(pr, pr)] @ x[pr])
    cert_end = isl_cc >= 0.95
    r = dict(exp=exp, N=N, I=I, mN=mN, rep=rep, gens=gens, rival=rival, preset=preset, removed=removed,
             status=R_.STATUS[int(st)], stop_gen=int(sg), pcc=float(isl_cc.mean()), cf_cross_pcc=cf,
             isl_eff=int(cert_end.sum()), n_est=int(estd.sum()), n_loc_est=int(loc_est.sum()), n_loc_end=int(loc_end.sum()),
             n_support=int(K), time_s=0.0)
    # generic separation (any two certified holders mutually defecting), ever (kernel) and at the end
    hc = sorted({int(h) for i, h in enumerate(hold) if cert_end[i] and coop[h]})
    sep_end = [(a, b) for ai, a in enumerate(hc) for b in hc[ai + 1:] if U[a, b] == -1 and U[b, a] == -1]
    r['first_sep'] = int(first_sep); r['n_sep_end'] = len(sep_end)
    r['first_sep_pair'] = (G(sep_a), G(sep_b)) if first_sep >= 0 else None
    r['sep_end_pairs'] = [(G(a), G(b)) for a, b in sep_end[:6]]
    # tagged analysis (forced rival present)
    if Rc is not None:
        held = {t: trace[:, 3 + (t - 1)] for t in (1, 2)}       # holder-rule islands per check
        heldc = {t: trace[:, 5 + (t - 1)] for t in (1, 2)}      # certified
        g = trace[:, 0]
        ev = np.nonzero((heldc[1] >= 1) & (heldc[2] >= 1))[0]
        r['ever_sep_tag'] = bool(len(ev) > 0)
        r['t_sep_tag'] = int(g[ev[0]]) if len(ev) else -1
        e2 = np.nonzero(heldc[2] >= 1)[0]
        r['rival_est'] = bool(len(e2) > 0)
        r['t_rival_est'] = int(g[e2[0]]) if len(e2) else -1
        # loss: after both networks have held a certified island, the first check at which one holds no island
        loss_t = -1; loss_net = 0
        if len(ev):
            after = np.arange(ev[0], len(g))
            z1 = after[held[1][after] == 0]; z2 = after[held[2][after] == 0]
            c1 = int(g[z1[0]]) if len(z1) else -1; c2 = int(g[z2[0]]) if len(z2) else -1
            cands = [(c, k) for c, k in ((c1, 1), (c2, 2)) if c >= 0]
            if cands:
                loss_t, loss_net = min(cands)
        r['loss_t'] = loss_t; r['loss_net'] = loss_net
        tend = loss_t if loss_t >= 0 else float(sg)
        r['expo'] = IP.integ(trace, 3, 4, tend)
        r['sep_end_tag'] = bool(((htag == 1) & cert_end).any() and ((htag == 2) & cert_end).any())
        r['both_end'] = bool((htag == 1).any() and (htag == 2).any())
        r['held_end'] = {str(t): int((htag == t).sum()) for t in range(4)}
        # establishment per island by tag and ancestry (at the island's first certification)
        etag = np.array([tag[h] if h >= 0 else -1 for h in e_hold])
        r['est_by_tag'] = {str(t): [int((estd & (etag == t) & (e_hloc >= 0.5)).sum()), int((estd & (etag == t) & (e_hloc < 0.5)).sum())]
                           for t in range(4)}
        r['est_rival_cls_local'] = int((estd & (e_hloc >= 0.5) & (e_hold >= 0) & (root[np.maximum(e_hold, 0)] == int(np.searchsorted(sup, Rc)))).sum())
        # bridge founders: tag-3 copies in the seed
        b3 = tag == 3
        r['bridge_seed_islands'] = int((li[:, b3].sum(1) > 0).sum()); r['bridge_seed_copies'] = int(li[:, b3].sum())
        r['bridge_seed_classes'] = int((li[:, b3].sum(0) > 0).sum())
        r['bridge_classes_mass'] = float(d['mu'][sup[b3]].sum())
        # strong-holder transitions by tag: invasions, mediation (2>3) and losses of rival islands
        inv = Counter(); med_t = []; nuc = Counter(); rival_losses = []
        for g_, i_, a_, b_ in tr_log:
            if a_ < 0:
                nuc[int(tag[b_])] += 1; continue
            ta, tb = int(tag[a_]), int(tag[b_])
            if ta != tb:
                inv['%d>%d' % (ta, tb)] += 1
                if ta == 2:
                    rival_losses.append((int(g_), tb))
                if ta == 2 and tb == 3:
                    med_t.append(int(g_))
        r['inv'] = dict(inv); r['first_strong'] = {str(t): v for t, v in nuc.items()}
        r['n_med'] = len(med_t); r['t_med'] = med_t[0] if med_t else -1
        lim = loss_t if loss_t >= 0 else int(sg)
        r['med_before_end'] = bool(any(t <= lim for t in med_t))
        rl = [x for x in rival_losses if x[0] <= lim]
        r['last_rival_loss'] = rl[-1][1] if rl else None
        r['bridge_est'] = int((estd & (etag == 3)).sum())
        r['bridge_held_end'] = int((htag == 3).sum())
        r['bridge_alive_end'] = bool(glob[b3].sum() > 0)
        r['t_ext'] = [float(v) for v in t_ext]
        gi = sorted(set(int(np.searchsorted(g, v)) for v in np.unique(np.round(np.logspace(1, math.log10(max(gens, 10)), 41)))))
        gi = [q for q in gi if q < len(trace)]
        r['trace'] = trace[gi][:, [0, 3, 4, 12, 7, 9]].round(3).tolist()
    # natural runs: classify every separation (first and at the end) by the static rival type and bridge fate
    if exp == 'nat' and (first_sep >= 0 or sep_end):
        S = [('first', root[sep_a], root[sep_b])] if first_sep >= 0 else []
        S += [('end', a, b) for a, b in sep_end[:3]]
        V9 = np.asarray(d['V']).astype(bool)
        a1g = d['idx'][FB1]; a0g = d['idx'][FB]
        out = []
        for kind, a, b in S:
            ga, gb = int(sup[a]), int(sup[b])
            inA = [bool(V9[x, a1g] and V9[a1g, x] and V9[x, a0g] and V9[a0g, x]) for x in (ga, gb)]
            mcab = V9[sup][:, ga] & V9[ga, sup] & V9[sup][:, gb] & V9[gb, sup] & coop
            brl = np.nonzero(mcab)[0]
            br_seed = int(li[:, brl].sum()) if len(brl) else 0
            br_isl = int((li[:, brl].sum(1) > 0).sum()) if len(brl) else 0
            br_end = int(np.isin(hold, brl).sum()) if len(brl) else 0
            br_alive = bool(glob[brl].sum() > 0) if len(brl) else False
            med = 0
            for g_, i_, a_, b_ in tr_log:
                if a_ >= 0 and b_ in set(brl.tolist()) and root[a_] in (a, b):
                    med += 1
            out.append(dict(kind=kind, a=G(a), b=G(b), inA=inA, n_bridge_classes=int(len(brl)), bridge_seed=br_seed,
                            bridge_seed_islands=br_isl, bridge_held_end=br_end, bridge_alive_end=br_alive, mediations=med,
                            held_a=int((hold == a).sum()), held_b=int((hold == b).sum())))
        r['seps'] = out
    r['time_s'] = time.time() - t0
    return r


def cells(exp):
    """(exp, N, I, mN, reps, gens, rival, preset)."""
    B = boundary(); out = []
    if exp in ('dense', 'sparse'):
        for rv in forced()['six']:
            out.append((exp, 200, 64, B[200], 100, GENS, rv, exp))
    elif exp == 'nobridge':
        out.append((exp, 200, 64, B[200], 100, GENS, forced()['bridged'][0], 'nobridge'))
    elif exp == 'iid':
        out.append((exp, 200, 64, B[200], 100, GENS, None, 'iid'))
    elif exp == 'nat':
        out.append((exp, 200, 64, B[200], 3000, GENS, None, 'iid'))
    elif exp == 'scale':
        f = forced()
        for rv in (f['bridgeless'][0], f['bridged'][0]):
            out.append((exp, 400, 64, B[400], 40, GENS, rv, 'dense'))
            out.append((exp, 200, 256, B[200], 40, GENS, rv, 'dense'))
            out.append((exp, 200, 64, B[200], 40, 300000, rv, 'dense'))
    return out


def ref_cells(exp):
    """m = 0 references with the same initial states (for q)."""
    if exp in ('nat', 'scale'):
        return []
    return [(e, N, I, 0.0, reps, GENS, rv, pre) for e, N, I, mN, reps, gens, rv, pre in cells(exp)]


def rows_path(exp, ref=False):
    return os.path.join(RUNS, 'bridgeless-rivals-rows-%s%s.json.gz' % (exp, '-m0' if ref else ''))


def load(exp, ref=False):
    p = rows_path(exp, ref)
    return json.load(gzip.open(p, 'rt')) if os.path.exists(p) else []


def save(exp, rows, ref=False):
    def conv(o):
        if isinstance(o, np.integer): return int(o)
        if isinstance(o, np.floating): return float(o)
        if isinstance(o, np.ndarray): return o.tolist()
        raise TypeError(type(o))
    tmp = rows_path(exp, ref) + '.tmp'
    with gzip.open(tmp, 'wt') as f:
        json.dump(rows, f, default=conv)
    os.replace(tmp, rows_path(exp, ref))


def ckey(r):
    return (r['exp'], r['N'], r['I'], r['mN'], r['gens'], r['rival'], r['preset'])


def warm():
    import rival_islands as R_
    R_.cls(9)
    job(('time', 20, 4, 1.0, 0, 50, forced()['six'][0], 'dense'))


def run_main(a):
    from multiprocessing import Pool
    for ref in ((False, True) if a.ref else (False,)):
        exp = a.exp
        rows = load(exp, ref)
        done = Counter(ckey(r) for r in rows)
        jobs = []
        for c in (ref_cells(exp) if ref else cells(exp)):
            e, N, I, mN, reps, gens, rv, pre = c
            if a.rival and rv != a.rival:
                continue
            key = (e, N, I, mN, gens, rv, pre)
            for rep in range(done[key], min(reps, a.maxreps)):
                jobs.append((e, N, I, mN, rep, gens, rv, pre))
        jobs.sort(key=lambda j: (j[4], -j[1] * j[2]))         # rep-major: every cell advances together
        print('%s%s: %d jobs' % (exp, ' (m = 0 refs)' if ref else '', len(jobs)), flush=True)
        t0 = time.time()
        with Pool(a.procs, initializer=warm) as pool:
            for r in pool.imap_unordered(job, jobs):
                rows.append(r)
                print('%s N=%d I=%d mN=%g %s %s rep %d: %s gen %d pcc %.3f sep_end %s loss %s/%s med %s (%.1fs; %.0fs total)' % (
                    r['exp'], r['N'], r['I'], r['mN'], (r['rival'] or '-')[:40], r['preset'], r['rep'], r['status'], r['stop_gen'],
                    r['pcc'], r.get('sep_end_tag', r['n_sep_end']), r.get('loss_t'), r.get('loss_net'), r.get('n_med'),
                    r['time_s'], time.time() - t0), flush=True)
                if len(rows) % 25 == 0:
                    save(exp, rows, ref)
        save(exp, rows, ref)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['classes', 'static', 'run', 'timing'])
    ap.add_argument('--threads', type=int, default=3)
    ap.add_argument('--exp', default='dense')
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--maxreps', type=int, default=10 ** 9)
    ap.add_argument('--ref', action='store_true')
    ap.add_argument('--rival', default=None)
    a = ap.parse_args()
    if a.what == 'classes':
        classes_main(a)
    elif a.what == 'static':
        static_main(a)
    elif a.what == 'run':
        run_main(a)
