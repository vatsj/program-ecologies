"""Does a co-seeded faker stop establishment?  The spoiler half of "almost all seeds".
Spec specs/2026-10-05-spoiler-conditioned.md; predictions predictions/2026-10-05-spoiler-conditioned.md.

Modal arm, PD, w = 0.3, eps = 0, iid seeds from the length prior at cutoff n in {6, 9, 12}, single islands (I = 1, no
migration), horizon 1e5 generations, the seeds_in_n kernel (`_run` with I = 1, m = 0: stops when the island is
locally frozen, i.e. every present class pairwise payoff-identical).

Class data: the modal language is evaluated once at n = 12 (moat_static_big's packed evaluator, as seeds_tail Part A);
n = 6 and 9 are sub-blocks, classes merged within L_n by identical row and column (checked against modal.build(9)).
Only the class-level 0/1 play matrix V (V[a, b] = 1 iff a cooperates with b) is kept; payoffs U = PD[V, V^T] are built
per island on the seed's support (no mutation, no migration: an island never leaves its seed's support).

    python3 src/spoiler_conditioned.py build            # class data -> cache/spoiler-n{6,9,12}.npz
    python3 src/spoiler_conditioned.py tables           # payoff tables, pairs -> runs/spoiler-conditioned-tables.json
    python3 src/spoiler_conditioned.py check            # local kernel equals seeds_in_n._run (n = 6, full class set)
    python3 src/spoiler_conditioned.py time             # timing batch (separate salt, outcomes not used)
    python3 src/spoiler_conditioned.py run [--procs 3]  # natural + forced -> runs/spoiler-conditioned-rows-*.json
    python3 src/spoiler_conditioned.py report           # runs/spoiler-conditioned.md and .json
"""
import argparse, json, math, os, sys, time
from collections import defaultdict
import numpy as np
from numba import njit
sys.path.insert(0, os.path.dirname(__file__))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
CACHE = os.path.join(ROOT, 'cache')
TABLES = os.path.join(RUNS, 'spoiler-conditioned-tables.json')
W = 0.3
NS = (6, 9, 12)
GENS = 100000
EVERY = 20
PDP = np.array([[-1.0, 1.0], [-2.0, 0.0]])       # pay[a][b], level order (D, C), as modal.PD
MU_TARGET = 1e-4
NPAIRS = 6


# ------------------------------------------------------------------ class data
def build_main(a):
    from numba import set_num_threads
    import modal as M
    import moat_static_big as MB
    set_num_threads(3)
    os.makedirs(CACHE, exist_ok=True)
    nmax = 12
    t0 = time.time()
    L = MB.CountedLanguage(nmax)
    nat, ak, al, af, aa, tt = L.arrays()
    nlev = int(al.max()) + 1
    T, nf = MB._traces(nat, ak, al, af, aa, tt, 200, nlev)
    if nf < 0:
        raise RuntimeError('did not stabilize')
    MB._to_stable(T, nf); V = T
    print('evaluated n=12: %d canons, %.0fs' % (V.shape[0], time.time() - t0), flush=True)
    cnt = L.size_counts(); a_s = L.a
    Kmax = V.shape[0]
    w_prog = np.array([0.0] + [1.0 / (2.0 * a_s[s] * s * s) for s in range(1, nmax + 1)])
    mshell = np.zeros((Kmax, nmax + 1))
    for s in range(1, nmax + 1):
        for c, m in cnt[s].items():
            mshell[c, s] += m * w_prog[s]
    first = np.full(Kmax, nmax + 1)
    for s in range(nmax, 0, -1):
        for c in cnt[s]:
            first[c] = s
    import seeds_tail as ST
    rng_w = np.random.default_rng(12345)
    w1 = rng_w.integers(1, 2**63, Kmax, dtype=np.uint64); w2 = rng_w.integers(1, 2**63, Kmax, dtype=np.uint64)
    for n in NS:
        K = int((first <= n).sum())
        assert (first[:K] <= n).all()
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
        cls.sort(key=lambda t: -t[2])           # as modal.ModalProvider: descending class mass
        reps = np.array([t[0] for t in cls], np.int64)
        mu = np.array([t[2] for t in cls]); mu = mu / mu.sum()
        Vc = np.ascontiguousarray(V[np.ix_(reps, reps)]).astype(np.uint8)
        names = np.array([L.rep[r] for r in reps])
        np.savez(os.path.join(CACHE, 'spoiler-n%d.npz' % n), V=Vc, mu=mu, names=names, nmem=np.array([len(t[1]) for t in cls]))
        print('n=%d: %d canons, %d classes, saved (%.0fs)' % (n, K, len(cls), time.time() - t0), flush=True)
        del Vc
    del V, T
    # check n = 6 and 9 against modal.build
    import seeds_in_n as SN
    for n in (6, 9):
        d = SN.data(n); c = cdata(n)
        same_names = sorted(d['names']) == sorted(c['names'])
        perm = [c['names'].index(x) for x in d['names']]
        Vb = c['V'][np.ix_(perm, perm)]
        Ub = PDP[Vb, Vb.T]
        print('check n=%d: classes %d vs %d, names equal %s, max |dmu| %.2e, U equal %s' % (
            n, len(d['names']), len(c['names']), same_names, np.abs(d['mu'] - c['mu'][perm]).max(), np.array_equal(Ub, d['U'])), flush=True)


_C = {}


def cdata(n):
    """Class data at cutoff n: V (uint8), mu, names, iC, iD, est (establisher mask), and helpers."""
    if n in _C:
        return _C[n]
    z = np.load(os.path.join(CACHE, 'spoiler-n%d.npz' % n), mmap_mode='r')
    V = np.asarray(z['V']); mu = np.asarray(z['mu']); names = [str(x) for x in z['names']]
    K = len(names)
    iC = names.index('C'); iD = names.index('D')
    selfc = np.diagonal(V).astype(bool)
    allc = V.all(1).astype(bool)
    est = selfc & (V[:, iD] == 0) & ~allc            # establisher: self-cooperates, defects on D
    assert allc[iC] and not est[iD]
    d = dict(n=n, V=V, mu=mu, names=names, K=K, iC=iC, iD=iD, est=est, selfc=selfc, allc=allc)
    _C[n] = d
    return d


def fakers_of(d, x):
    """q fakes x: q defects on x while x cooperates with q (so U[q, x] = 1 > 0 = U[x, x] for an establisher x)."""
    V = d['V']
    return np.nonzero((V[x, :] == 1) & (V[:, x] == 0))[0]


def d_profile(d, q):
    """The faker's play against D, from the 2x2 game {q, D}: f_q - f_D = x (U[q,q] - U[D,q]) + (1 - x)(U[q,D] - U[D,D])."""
    V = d['V']; iD = d['iD']
    uqq = PDP[V[q, q], V[q, q]]; uqD = PDP[V[q, iD], V[iD, q]]; uDq = PDP[V[iD, q], V[q, iD]]; uDD = -1.0
    a1 = uqq - uDq; a0 = uqD - uDD
    if a1 == 0 and a0 == 0: return 'neutral'
    if a1 <= 0 and a0 <= 0: return 'disadvantaged'
    if a1 >= 0 and a0 >= 0: return 'advantaged'
    return 'mixed'


def table4(d, t, q):
    V = d['V']; ids = [t, q, d['iD'], d['iC']]
    return [[float(PDP[V[a, b], V[b, a]]) for b in ids] for a in ids]


def pair_list(n):
    """Every (target, faker) pair with mu(target) >= MU_TARGET (target an establisher), heaviest by mu(t) mu(q) first."""
    d = cdata(n); mu = d['mu']; nm = d['names']; V = d['V']
    out = []
    for t in np.nonzero(d['est'] & (mu >= MU_TARGET))[0]:
        for q in fakers_of(d, t):
            out.append(dict(target=nm[t], faker=nm[q], t=int(t), q=int(q), mu_t=float(mu[t]), mu_q=float(mu[q]),
                            weight=float(mu[t] * mu[q]), faker_vs_D=d_profile(d, q), faker_is_est=bool(d['est'][q]),
                            faker_vs_ALLC='D' if V[q, d['iC']] == 0 else 'C', faker_selfC=bool(V[q, q]),
                            target_vs_faker_of_others=None, table=table4(d, t, q)))
    out.sort(key=lambda r: -r['weight'])
    return out


def tables_main(a):
    res = {}
    for n in NS:
        d = cdata(n); mu = d['mu']; nm = d['names']
        pl = pair_list(n)
        tg = sorted({r['t'] for r in pl} | set(np.nonzero(d['est'] & (mu >= MU_TARGET))[0].tolist()), key=lambda t: -mu[t])
        # the faker's play against D over all fakers of these targets, by count and mass
        fk = {}
        for r in pl: fk[r['q']] = r['faker_vs_D']
        prof = defaultdict(lambda: [0, 0.0])
        for q, c in fk.items():
            prof[c][0] += 1; prof[c][1] += float(mu[q])
        # forced pairs: heaviest NPAIRS among those where the faker exploits the target (U[q,t] > U[t,t]; true by construction)
        forced = pl[:NPAIRS]
        res[str(n)] = dict(n=n, classes=d['K'], mu_est=float(mu[d['est']].sum()), n_targets=len(tg),
                           targets=[dict(name=nm[t], mu=float(mu[t]), n_fakers=int(len(fakers_of(d, t))),
                                         faker_mass=float(mu[fakers_of(d, t)].sum())) for t in tg],
                           n_pairs=len(pl), faker_profile={k: dict(classes=v[0], mass=v[1]) for k, v in prof.items()},
                           pairs=pl[:60], forced=forced,
                           pair_mass_by_profile={c: float(sum(r['weight'] for r in pl if r['faker_vs_D'] == c)) for c in ('disadvantaged', 'neutral', 'advantaged', 'mixed')})
        print('n=%d: %d targets (mu >= 1e-4), %d pairs; faker profiles %s' % (n, len(tg), len(pl), dict(prof)), flush=True)
        for r in pl[:12]:
            print('   %-28s <- %-34s w %.2e  mu_q %.4f  vsD %-13s est %s  vsALLC %s' % (r['target'], r['faker'], r['weight'], r['mu_q'], r['faker_vs_D'], r['faker_is_est'], r['faker_vs_ALLC']), flush=True)
    json.dump(res, open(TABLES, 'w'), indent=1)



# ------------------------------------------------------------------ kernel (seeds_in_n._run, single island, with logs)
_KERNEL = None
NCAT = 6
CATS = ('target', 'faker', 'D', 'ALLC', 'other establisher', 'other')


def kernel():
    """seeds_in_n._run with three logs that draw no random numbers (checked by `check`): the generation of every class's
    extinction (ext_t), the category counts at the island's first ALLC extinction (catC, taken just after the ALLC death,
    before the replacing birth), and the category counts every `every` generations (flog)."""
    global _KERNEL
    if _KERNEL is not None:
        return _KERNEL
    import inspect
    import seeds_in_n as SN
    src = inspect.getsource(SN._run.py_func).replace('@njit(cache=True)\n', '')
    reps = [
        ('def _run(U, PCC, init, N, w, m, gens, every, seed, iC, coopmask, coremask, T0):',
         'def _run(U, PCC, init, N, w, m, gens, every, seed, iC, coopmask, coremask, T0, cat, flog, ext_t, catC):'),
        ("            if counts[i, victim] == 0:\n                p = pos[i, victim]",
         "            if counts[i, victim] == 0:\n                ext_t[victim] = g + e / IN\n                p = pos[i, victim]"),
        ("                    if tC_first[i] < 0: tC_first[i] = tt\n",
         "                    if tC_first[i] < 0:\n                        tC_first[i] = tt\n"
         "                        for t9 in range(npres[i]):\n                            catC[cat[pres[i, t9]]] += counts[i, pres[i, t9]]\n"),
        ("                tr_cc[s] = cc_tot / I\n",
         "                tr_cc[s] = cc_tot / I\n                for t9 in range(npres[0]):\n                    flog[s, cat[pres[0, t9]]] += counts[0, pres[0, t9]]\n"),
    ]
    for a_, b_ in reps:
        assert src.count(a_) == 1, a_
        src = src.replace(a_, b_)
    ns = dict(vars(SN))
    exec(compile(src, 'spoiler_kernel', 'exec'), ns)
    _KERNEL = njit(cache=False)(ns['_run'])
    return _KERNEL


STATUS = {1: 'certified-frozen', 2: 'certified-separated', 3: 'metastable', 4: 'unresolved', 5: 'local-frozen'}


def simulate(d, init_full, N, seed, cat_full, gens=GENS, keep_log=True):
    """One island from the class-count vector init_full (length K).  Works on the seed's support plus ALLC and D (zero
    counts do not enter `pres`, so the random stream is that of the full-class kernel)."""
    run = kernel()
    sup = np.nonzero(init_full)[0]
    sup = np.union1d(sup, [d['iC'], d['iD']]).astype(np.int64)
    V = d['V'][np.ix_(sup, sup)].astype(np.int64)
    U = np.ascontiguousarray(PDP[V, V.T]); PCC = np.ascontiguousarray((V * V.T).astype(float))
    loc = {int(g): j for j, g in enumerate(sup)}
    iC = loc[d['iC']]
    init = init_full[sup][None, :].astype(np.int64)
    coop = np.ascontiguousarray(d['selfc'][sup] & ~d['allc'][sup]); core = np.zeros(len(sup), np.bool_)
    cat = np.ascontiguousarray(cat_full[sup].astype(np.int64))
    flog = np.zeros((gens // EVERY, NCAT), np.int64); ext_t = -np.ones(len(sup)); catC = np.zeros(NCAT, np.int64)
    out = run(U, PCC, init, N, W, 0.0, gens, EVERY, seed, iC, coop, core, 0, cat, flog, ext_t, catC)
    (st, sg, counts, isl_cc, isl_pay, first_noC, ext_C, lb, la, tr_cc, tr_np, loss_log, loss_snap,
     tC_first, tC_last, C_reent, tC_glob, core_glob, first_cert, first_cert_core, atT0) = out
    c = counts[0]
    fin = np.nonzero(c)[0]
    Vf = V[np.ix_(fin, fin)]
    cat0 = np.zeros(NCAT, np.int64)
    for j in np.nonzero(init[0])[0]: cat0[cat[j]] += init[0, j]
    if init[0, iC] == 0: catC = cat0.copy()
    nrow = len(tr_cc)
    res = dict(status=STATUS[int(st)], resolved=int(st) in (1, 2, 3, 5), stop_gen=int(sg), pcc=float(isl_cc[0]),
               final={int(sup[j]): int(c[j]) for j in fin}, coop_fix=bool(Vf.all()), efficient=bool(isl_cc[0] >= 0.95),
               tC=float(tC_first[0]), catC=catC.tolist(), cat0=cat0.tolist(),
               ext={int(sup[j]): round(float(ext_t[j]), 2) for j in range(len(sup)) if ext_t[j] >= 0})
    if keep_log:
        res['flog'] = [cat0.tolist()] + flog[:min(nrow, 500)].tolist()
    return res


def check_main(a):
    """The logging kernel on the seed's support reproduces seeds_in_n._run on the full n = 6 and n = 9 class sets."""
    import seeds_in_n as SN
    ok = True
    for n in (6, 9):
        dd = SN.data(n); c = cdata(n)
        perm = np.array([c['names'].index(x) for x in dd['names']])      # SN index -> cdata index
        for N in (100, 400):
            for rep in range(4):
                rng = np.random.default_rng([n, N, rep, 777])
                init = rng.multinomial(N, dd['mu'])[None, :].astype(np.int64)
                A = SN._run(dd['U'], dd['PCC'], init, N, W, 0.0, GENS, EVERY, 91 + rep, dd['iC'], dd['coopmask'], dd['coremask'], 0)
                full = np.zeros(c['K'], np.int64); full[perm] = init[0]
                # the local kernel orders classes by cdata index; SN orders by its own index.  Identical streams need the
                # same order, so compare on SN's own ordering by permuting cdata into SN order:
                cc = dict(c); cc['V'] = c['V'][np.ix_(perm, perm)]; cc['selfc'] = c['selfc'][perm]; cc['allc'] = c['allc'][perm]
                cc['iC'] = dd['iC']; cc['iD'] = dd['iD']
                B = simulate(cc, init[0], N, 91 + rep, np.zeros(len(perm), np.int64), keep_log=False)
                finA = {int(k): int(v) for k, v in enumerate(A[2][0]) if v > 0}
                same = A[1] == B['stop_gen'] and finA == B['final'] and abs(A[3][0] - B['pcc']) < 1e-12
                ok &= same
                print(n, N, rep, 'same' if same else 'DIFFERENT', STATUS[int(A[0])], A[1], B['stop_gen'], flush=True)
    print('ALL SAME' if ok else 'MISMATCH')


# ------------------------------------------------------------------ jobs
SALT_NAT = 20261006
SALT_FRC = 20261007
SALT_TIME = 99
NNAT = 4000
NBG = 1000
NS_N = (100, 400)
DOSES = {400: (1, 3, 10), 100: (1, 3)}
TREAT = ('a', 'b', 'c', 'cD', 'd')      # c: k extra copies of the target's own class; cD: k extra copies of D


def nat_seed(n, N, rep, salt):
    return [n, N, rep, salt], 1000003 * rep + 7 * N + 13 * n + salt % 100000


def nat_job(j):
    n, N, rep, salt = j
    d = cdata(n); mu = d['mu']; V = d['V']; est = d['est']; nm = d['names']
    rs, ss = nat_seed(n, N, rep, salt)
    rng = np.random.default_rng(rs)
    init = rng.multinomial(N, mu).astype(np.int64)
    sup = np.nonzero(init)[0]
    E = sup[est[sup]]
    pairs = []
    if len(E):
        F = (V[np.ix_(E, sup)] == 1) & (V[np.ix_(sup, E)].T == 0)
        for a_, b_ in zip(*np.nonzero(F)):
            pairs.append((int(E[a_]), int(sup[b_])))
    fk = sorted({q for _, q in pairs})
    fne = [q for q in fk if not est[q]]; fe = [q for q in fk if est[q]]
    if not len(E): cell = 'noA'
    elif not pairs: cell = 'i'
    elif fne and not fe: cell = 'ii'
    elif fe and not fne: cell = 'iii'
    else: cell = 'iv'
    targets = [int(x) for x in E] if cell == 'i' else sorted({x for x, _ in pairs})
    cat = np.full(d['K'], 5, np.int64)
    cat[E] = 4; cat[d['iC']] = 3; cat[d['iD']] = 2
    cat[fk] = 1; cat[targets] = 0
    t0 = time.time()
    r = simulate(d, init, N, ss, cat, keep_log=len(E) > 0)
    fin = r['final']
    tracked = set(targets) | set(fk) | {d['iC'], d['iD']}
    big = max(fin, key=lambda k: fin[k])
    out = dict(kind='nat', n=n, N=N, rep=rep, salt=salt, cell=cell,
               est={nm[x]: int(init[x]) for x in E}, n_est=int(init[E].sum()),
               pairs=[(nm[x], nm[q], int(init[x]), int(init[q]), d_profile(d, q), bool(est[q])) for x, q in pairs],
               targets={nm[x]: int(init[x]) for x in targets}, n_fk=int(init[fk].sum()) if fk else 0,
               n_fk_nonest=int(init[fne].sum()) if fne else 0, n_fk_est=int(init[fe].sum()) if fe else 0,
               fk_profiles=sorted({d_profile(d, q) for q in fne}),
               status=r['status'], resolved=r['resolved'], stop_gen=r['stop_gen'], pcc=r['pcc'],
               coop_fix=r['coop_fix'], efficient=r['efficient'],
               target_surv=any(x in fin for x in targets), est_surv=any(bool(est[k]) for k in fin), faker_surv=any(q in fin for q in fk),
               nonest_faker_surv=any(q in fin for q in fne),
               winner=nm[big], winner_cat=CATS[cat[big]], final_support=len(fin),
               final_top=sorted(((nm[k], v) for k, v in fin.items()), key=lambda t: -t[1])[:6],
               tC=r['tC'], catC=r['catC'], cat0=r['cat0'],
               ext=sorted(((nm[k], t) for k, t in r['ext'].items() if k in tracked), key=lambda t: t[1]),
               flog=r.get('flog'), time_s=time.time() - t0)
    return out


_P = {}


def forced_pairs(n):
    """The NPAIRS heaviest pairs, then the predeclared supplement S (an establisher-faker pair, the same at every n)."""
    if n not in _P:
        T = json.load(open(TABLES))[str(n)]
        S = [r for r in T['pairs'] if (r['target'], r['faker']) == SUPP]
        assert len(S) == 1
        _P[n] = T['forced'] + S
    return _P[n]


SUPP = ('not(BOXD(THEM(^C)))', 'BOX(THEM(ME))')


def frc_job(j):
    """One background, every treatment and dose, common random numbers."""
    n, N, pi, rep, salt = j
    d = cdata(n); mu = d['mu']; nm = d['names']; est = d['est']
    P = forced_pairs(n)[pi]
    t, q = P['t'], P['q']
    rng = np.random.default_rng([n, N, pi, rep, salt])
    bg = rng.multinomial(N, mu).astype(np.int64)
    slots = np.repeat(np.arange(d['K']), bg)
    perm = rng.permutation(N)
    ss = 1000003 * rep + 7 * N + 13 * n + 101 * pi + salt % 100000
    cat = np.full(d['K'], 5, np.int64)
    cat[d['est']] = 4; cat[d['iC']] = 3; cat[d['iD']] = 2; cat[q] = 1; cat[t] = 0
    sup = np.nonzero(bg)[0]
    E = sup[est[sup]]
    res = dict(kind='frc', n=n, N=N, pair=pi, rep=rep, salt=salt, bg_t=int(bg[t]), bg_q=int(bg[q]), bg_A=bool(len(E)),
               bg_n_est=int(bg[E].sum()), out={})
    t0 = time.time()
    for k in DOSES[N]:
        first = slots[perm[:k]]; second = slots[perm[10:10 + k]]
        for tr in TREAT:
            init = bg.copy()
            if tr in ('a', 'b', 'c', 'cD'):
                np.subtract.at(init, first, 1); init[t] += k
            if tr in ('b', 'c', 'cD'):
                np.subtract.at(init, second, 1); init[{'b': q, 'c': t, 'cD': d['iD']}[tr]] += k
            if tr == 'd':
                np.subtract.at(init, first, 1); init[q] += k
            assert init.sum() == N and init.min() >= 0
            r = simulate(d, init, N, ss, cat, keep_log=(tr == 'b'))
            fin = r['final']; big = max(fin, key=lambda c: fin[c])
            rec = [int(r['resolved']), int(t in fin), int(q in fin), int(r['coop_fix']), int(r['efficient']),
                   CATS[cat[big]], nm[big], round(r['pcc'], 4), r['stop_gen'], round(r['tC'], 2), r['catC'],
                   round(r['ext'].get(t, -1.0), 2), round(r['ext'].get(q, -1.0), 2)]
            if tr == 'b':
                rec.append(r['flog'][:12])
            res['out']['%s%d' % (tr, k)] = rec
    res['time_s'] = time.time() - t0
    return res


FRC_FIELDS = ['resolved', 'target_surv', 'faker_surv', 'coop_fix', 'efficient', 'winner_cat', 'winner', 'pcc', 'stop_gen',
              'tC', 'catC', 'ext_target', 'ext_faker', 'flog']


def warm():
    kernel()
    for n in NS: cdata(n)


def time_main(a):
    warm()
    for n in NS:
        for N in NS_N:
            t0 = time.time()
            rows = [nat_job((n, N, rep, SALT_TIME)) for rep in range(40)]
            tn = (time.time() - t0) / 40
            t0 = time.time()
            fr = [frc_job((n, N, pi, rep, SALT_TIME)) for pi in (0, 2) for rep in range(4)]
            tf = (time.time() - t0) / 8
            print('n=%d N=%d: natural %.3fs/island (max %.2f), forced %.3fs/background (%d runs)' % (
                n, N, tn, max(r['time_s'] for r in rows), tf, len(fr[0]['out'])), flush=True)


ROWS_NAT = os.path.join(RUNS, 'spoiler-conditioned-rows-nat.json.gz')
ROWS_FRC = os.path.join(RUNS, 'spoiler-conditioned-rows-frc.json.gz')


def _job(j):
    return nat_job(j[1:]) if j[0] == 'nat' else frc_job(j[1:])


def run_main(a):
    import gzip
    from multiprocessing import Pool
    jobs = []
    if a.only in (None, 'nat'):
        jobs += [('nat', n, N, rep, SALT_NAT) for n in NS for N in NS_N for rep in range(NNAT)]
    if a.only in (None, 'frc'):
        jobs += [('frc', n, N, pi, rep, SALT_FRC) for n in NS for N in NS_N for pi in range(NPAIRS + 1) for rep in range(NBG)]
    print('%d jobs' % len(jobs), flush=True)
    nat, frc = [], []
    t0 = time.time()
    with Pool(a.procs, initializer=warm) as pool:
        for i, r in enumerate(pool.imap_unordered(_job, jobs, chunksize=20)):
            (nat if r['kind'] == 'nat' else frc).append(r)
            if (i + 1) % 2000 == 0:
                print('%d / %d done, %.0fs' % (i + 1, len(jobs), time.time() - t0), flush=True)
            if time.time() - t0 > 2 * 3600:
                print('ADMINISTRATIVE CENSORING at %d / %d jobs' % (i + 1, len(jobs)), flush=True)
                pool.terminate(); break
    for rows, path in ((nat, ROWS_NAT), (frc, ROWS_FRC)):
        if rows:
            rows.sort(key=lambda r: (r['n'], r['N'], r.get('pair', -1), r['rep']))
            with gzip.open(path, 'wt') as f:
                json.dump(rows, f)
    print('done: %d natural, %d forced backgrounds, %.0fs' % (len(nat), len(frc), time.time() - t0), flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['build', 'tables', 'check', 'time', 'run', 'report'])
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--only', default=None)
    a = ap.parse_args()
    {'build': build_main, 'tables': tables_main, 'check': check_main, 'time': time_main, 'run': run_main}[a.what](a)
