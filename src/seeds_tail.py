"""The seed lottery's tail in n (static, Part A) and island merging at I = 4 (Part B).
Spec specs/2026-10-05-seeds-tail.md; predictions predictions/2026-10-05-seeds-tail.md.

Part A evaluates the modal language once at the largest cutoff (moat_static_big's packed evaluator) and takes every
smaller cutoff as a sub-block: canonical-function ids are created in enumeration order, so the functions of L_n are a
prefix of those of L_nmax (checked), and a pair's play depends only on the pair and its arguments (checked against a
direct modal.build at n = 9).  Masses are kept per canonical function and per length shell, in three units
(raw: shell s has mass 1/(2 s^2); infinite-normalized: raw / (pi^2/12); cutoff-normalized: raw / retained(n)).

    python3 src/seeds_tail.py static [nmax]       # Part A -> runs/seeds-tail-static.json
    python3 src/seeds_tail.py check               # Part B kernel equals seeds_in_n._run draw for draw
    python3 src/seeds_tail.py run [--procs 3]     # Part B -> runs/seeds-tail-rows.json
    python3 src/seeds_tail.py report              # runs/seeds-tail.md and runs/seeds-tail.json
"""
import argparse, json, math, os, sys, time
from collections import defaultdict
import numpy as np
from numba import njit, prange, set_num_threads
sys.path.insert(0, os.path.dirname(__file__))
import modal as M
import moat_static_big as MB
from chain import fixation

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
STATIC = os.path.join(RUNS, 'seeds-tail-static.json')
W = 0.3
Z_INF = math.pi ** 2 / 12


# ------------------------------------------------------------------ Part A kernels
@njit(parallel=True, cache=True)
def _suck_sub(V, K):
    out = np.zeros(K, np.bool_)
    for i in prange(K):
        for j in range(K):
            if V[i, j] == 1 and V[j, i] == 0:
                out[i] = True
                break
    return out


@njit(parallel=True, cache=True)
def _fakers(V, K, E, mu):
    """isf[q]: q defects on some establisher x in E that cooperates with q.  fm[e]: faker mass of E[e]."""
    isf = np.zeros(K, np.bool_)
    for q in prange(K):
        for e in range(E.shape[0]):
            x = E[e]
            if V[x, q] == 1 and V[q, x] == 0:
                isf[q] = True
                break
    fm = np.zeros(E.shape[0])
    for e in prange(E.shape[0]):
        x = E[e]; s = 0.0
        for q in range(K):
            if V[x, q] == 1 and V[q, x] == 0:
                s += mu[q]
        fm[e] = s
    return isf, fm


@njit(parallel=True, cache=True)
def _hash_sub(V, K, w1, w2):
    hr = np.zeros(K, np.uint64); hc = np.zeros(K, np.uint64)
    for x in prange(K):
        a = np.uint64(0); b = np.uint64(0)
        for y in range(K):
            if V[x, y]:
                a += w1[y]
            if V[y, x]:
                b += w2[y]
        hr[x] = a; hc[x] = b
    return hr, hc


@njit(cache=True)
def _same_sub(V, K, a, b):
    for y in range(K):
        if V[a, y] != V[b, y] or V[y, a] != V[y, b]:
            return False
    return True


@njit(cache=True)
def _coseed(V, draws, is_est):
    """Per seed (row of draws): A = some establisher present; K_pf = members that are fakers of a present establisher;
    K_pf_est = those of them that are themselves establishers."""
    S, N = draws.shape
    A = np.zeros(S, np.bool_); kpf = np.zeros(S, np.int64); kpe = np.zeros(S, np.int64)
    est = np.zeros(N, np.int64)
    for s in range(S):
        ne = 0
        for t in range(N):
            c = draws[s, t]
            if is_est[c]:
                dup = False
                for u in range(ne):
                    if est[u] == c:
                        dup = True; break
                if not dup:
                    est[ne] = c; ne += 1
        if ne == 0:
            continue
        A[s] = True
        for t in range(N):
            q = draws[s, t]
            for u in range(ne):
                x = est[u]
                if V[x, q] == 1 and V[q, x] == 0:
                    kpf[s] += 1
                    if is_est[q]: kpe[s] += 1
                    break
    return A, kpf, kpe


def rho_D(N):
    """Single-copy fixation of an establisher (C/C 0, D/D -1 against D) on an all-D island of N."""
    return float(fixation(0.0, -1.0, -1.0, -1.0, N, W, N))


def static_main(a):
    nmax = a.nmax
    set_num_threads(3)
    t0 = time.time()
    L = MB.CountedLanguage(nmax)
    t_enum = time.time() - t0
    nat, ak, al, af, aa, tt = L.arrays()
    nlev = int(al.max()) + 1
    T, nf = MB._traces(nat, ak, al, af, aa, tt, 200, nlev)
    if nf < 0:
        raise RuntimeError('did not stabilize')
    MB._to_stable(T, nf); V = T
    t_eval = time.time() - t0
    Kmax = V.shape[0]
    print('n=%d: %d canonical functions, enumeration %.0fs, evaluation %.0fs (stable at world %d)' % (nmax, Kmax, t_enum, t_eval, nf), flush=True)
    cnt = L.size_counts()
    a_s = L.a
    w_prog = np.array([0.0] + [1.0 / (2.0 * a_s[s] * s * s) for s in range(1, nmax + 1)])
    mshell = np.zeros((Kmax, nmax + 1))                # raw mass per canon per shell
    for s in range(1, nmax + 1):
        for c, m in cnt[s].items():
            mshell[c, s] += m * w_prog[s]
    assert abs(mshell[:, 1:].sum(0) - np.array([1 / (2 * s * s) for s in range(1, nmax + 1)])).max() < 1e-12
    # K_n: canons that have a program of size <= n; check prefix property
    first = np.full(Kmax, nmax + 1)
    for s in range(nmax, 0, -1):
        for c in cnt[s]:
            first[c] = s
    Kn = {}
    for n in range(1, nmax + 1):
        k = int((first <= n).sum())
        assert (first[:k] <= n).all() and (first[k:] > n).all(), 'canon ids are not a prefix at n = %d' % n
        Kn[n] = k
    iC = L.op('C'); iD = L.op('D')
    iFB = L.op((0, 0, M.TM)); iFB1 = L.op((0, 1, M.TM))
    assert L.rep[iFB] == 'BOX(THEM(ME))' and L.rep[iFB1] == 'BOX1(THEM(ME))'
    selfc = np.array([V[c, c] == 1 for c in range(Kmax)])
    allc_row = None
    out = dict(nmax=nmax, canon=Kmax, worlds=int(nf), t_enum=t_enum, t_eval=t_eval, Z_inf=Z_INF, rows=[], items=[],
               reclass=[], rho={str(N): rho_D(N) for N in (100, 400, 1600)})
    prev = None
    rng_w = np.random.default_rng(12345)
    w1 = rng_w.integers(1, 2**63, Kmax, dtype=np.uint64); w2 = rng_w.integers(1, 2**63, Kmax, dtype=np.uint64)
    for n in range(a.nmin, nmax + 1):
        tn = time.time()
        K = Kn[n]
        raw = mshell[:K, 1:n + 1].sum(1)            # raw mass per canon at cutoff n
        retained = sum(1 / (2 * s * s) for s in range(1, n + 1))
        omitted = Z_INF - retained
        # ALLC: row all ones within L_n
        allc = np.array([V[c, :K].all() for c in range(K)])
        est = selfc[:K] & (V[:K, iD] == 0) & ~allc
        suck = _suck_sub(V, K)
        coop = selfc[:K] & ~allc
        core = coop & ~suck
        E = np.nonzero(est)[0].astype(np.int64)
        isf, fm = _fakers(V, K, E, raw)
        # behavioural classes (as modal.ModalProvider): identical row and column within L_n
        hr, hc = _hash_sub(V, K, w1, w2)
        groups = defaultdict(list)
        for c in range(K):
            groups[(int(hr[c]), int(hc[c]))].append(c)
        cls = []
        for mem in groups.values():
            rep = min(mem, key=lambda c: (L.bits_canon[c], c))
            for c in mem:
                assert c == rep or _same_sub(V, K, rep, c), 'hash collision'
            cls.append((rep, mem))
        ncls = len(cls)
        rep_of = {}
        for rep, mem in cls:
            for c in mem: rep_of[c] = rep
        def ncl(mask):
            return len({rep_of[c] for c in np.nonzero(mask)[0]})
        sh_est = mshell[:K][est].sum(0)[1:n + 1]
        sh_pf = mshell[:K][isf].sum(0)[1:n + 1]
        sh_core = mshell[:K][core].sum(0)[1:n + 1]
        sh_coop = mshell[:K][coop].sum(0)[1:n + 1]
        shellmass = np.array([1 / (2 * s * s) for s in range(1, n + 1)])
        mu_est = float(raw[est].sum()); mu_pf = float(raw[isf].sum()); mu_core = float(raw[core].sum())
        mu_fk_est = float(raw[est & suck].sum())
        row = dict(n=n, canon=K, classes=ncls, retained=retained, omitted=omitted,
                   n_est_classes=ncl(est), n_pf_classes=ncl(isf), n_core_classes=ncl(core), n_coop_classes=ncl(coop),
                   raw=dict(est=mu_est, pf=mu_pf, core=mu_core, coop=float(raw[coop].sum()), est_fakeable=mu_fk_est,
                            est_core=float(raw[est & core].sum()), FB=float(raw[iFB]), FB1=float(raw[iFB1]),
                            ALLC=float(raw[allc].sum()), D_class=float(raw[[c for c in range(K) if rep_of[c] == rep_of[iD]]].sum()),
                            pf_est=float(raw[isf & est].sum())),
                   shell_est=sh_est.tolist(), shell_pf=sh_pf.tolist(), shell_core=sh_core.tolist(), shell_coop=sh_coop.tolist(),
                   f_est=(sh_est / shellmass).tolist(), f_pf=(sh_pf / shellmass).tolist(), f_core=(sh_core / shellmass).tolist(),
                   FB_unfakeable=bool(not suck[iFB]), FB1_unfakeable=bool(not suck[iFB1]),
                   FB_invaders=[L.rep[q] for q in range(K) if V[iFB, q] == 1 and V[q, iFB] == 0][:10],
                   FB1_invaders=[L.rep[q] for q in range(K) if V[iFB1, q] == 1 and V[q, iFB1] == 0][:10])
        row['r'] = mu_pf / mu_est
        for u, z in (('inf', Z_INF), ('cut', retained)):
            row[u] = {k: v / z for k, v in row['raw'].items()}
        row['bound_est_inf'] = (mu_est + omitted) / Z_INF
        # establishment-weighted mass
        row['est_weighted'] = {str(N): dict(raw=mu_est * out['rho'][str(N)], cut=mu_est / retained * out['rho'][str(N)]) for N in (100, 400, 1600)}
        # item 4: establisher classes with raw mass >= 1e-4
        items = []
        for rep, mem in cls:
            if not est[rep]:
                continue
            m = float(raw[mem].sum())
            if m < 1e-4:
                continue
            e = int(np.searchsorted(E, rep))
            items.append(dict(name=L.rep[rep], mu_raw=m, mu_cut=m / retained, rho100=out['rho']['100'],
                              faker_mass_raw=float(fm[e]), faker_mass_cut=float(fm[e]) / retained,
                              core=bool(core[rep]), n_members=len(mem),
                              top_fakers=sorted({L.rep[rep_of[q]] for q in range(K) if V[rep, q] == 1 and V[q, rep] == 0},
                                                key=lambda s: len(s))[:4]))
        items.sort(key=lambda r: -r['mu_raw'])
        row['items'] = items
        row['max_faker_mass_cut'] = float(fm.max() / retained) if len(fm) else 0.0
        # mu-weighted exposure: expected (cutoff-normalized) faker mass facing a mu-random establisher
        row['exposure_cut'] = float((raw[E] * fm).sum() / raw[E].sum() / retained)
        # faker union restricted to establishers with raw class mass >= 1e-4 (the main establishers)
        main = np.array([c for c in E if raw[[m for m in groups[(int(hr[c]), int(hc[c]))]]].sum() >= 1e-4], np.int64)
        isf_main, _ = _fakers(V, K, main, raw)
        row['pf_main_cut'] = float(raw[isf_main].sum() / retained)
        row['n_main_est_canon'] = int(len(main))
        # reclassification from n - 1
        if prev is not None:
            Kp = prev['K']
            old = np.arange(Kp)
            rawp = mshell[:Kp, 1:n].sum(1)
            rc = dict(n=n, est_switch=int((est[:Kp] != prev['est']).sum()),
                      core_to_fakeable_raw=float(rawp[prev['core'] & ~core[:Kp]].sum()),
                      core_to_fakeable=[L.rep[c] for c in old[prev['core'] & ~core[:Kp]]][:8],
                      new_pf_old_syntax_raw=float(rawp[isf[:Kp] & ~prev['isf']].sum()),
                      pf_lost=int((prev['isf'] & ~isf[:Kp]).sum()),
                      d_est_new_shell_raw=float(sh_est[n - 1]), d_pf_new_shell_raw=float(sh_pf[n - 1]),
                      d_core_new_shell_raw=float(sh_core[n - 1]))
            rc['d_est_raw'] = mu_est - prev['mu_est']; rc['d_pf_raw'] = mu_pf - prev['mu_pf']; rc['d_core_raw'] = mu_core - prev['mu_core']
            out['reclass'].append(rc)
        prev = dict(K=K, est=est.copy(), core=core.copy(), isf=isf.copy(), mu_est=mu_est, mu_pf=mu_pf, mu_core=mu_core)
        # item 5: co-seeding, 1e5 iid seeds of N = 100 from the cutoff-normalized prior
        p = raw / raw.sum()
        rng = np.random.default_rng([20261005, n])
        Acnt = 0; kp = []; kpe = []
        for chunk in range(10):
            draws = rng.choice(K, size=(10000, 100), p=p).astype(np.int64)
            A_, k_, ke_ = _coseed(V, draws, est)
            Acnt += int(A_.sum()); kp.append(k_[A_]); kpe.append(ke_[A_])
        kp = np.concatenate(kp); kpe = np.concatenate(kpe)
        row['coseed'] = dict(seeds=100000, N=100, P_A=Acnt / 1e5, E_kpf_A=float(kp.mean()), se_E=float(kp.std() / math.sqrt(len(kp))),
                             P_kpf_A=float((kp > 0).mean()), se_P=float(math.sqrt((kp > 0).mean() * (1 - (kp > 0).mean()) / len(kp))),
                             E_kpe_A=float(kpe.mean()), naive_N_mupf=100 * mu_pf / retained)
        row['t'] = time.time() - tn
        out['rows'].append(row)
        print('n=%d K=%d classes=%d | mu_est raw %.5f cut %.5f inf %.5f | mu_pf cut %.5f r %.3f | core cut %.5f | FB unf %s FB1 unf %s | '
              'P(A) %.3f E[Kpf|A] %.3f P(Kpf>0|A) %.3f | %.0fs' % (
                  n, K, ncls, mu_est, row['cut']['est'], row['inf']['est'], row['cut']['pf'], row['r'], row['cut']['core'],
                  row['FB_unfakeable'], row['FB1_unfakeable'], row['coseed']['P_A'], row['coseed']['E_kpf_A'],
                  row['coseed']['P_kpf_A'], row['t']), flush=True)
        json.dump(out, open(a.out, 'w'), indent=1)
    # direct check at n = 9 against modal.build: masses of establishers, fakers, core (cutoff-normalized)
    if a.check9 and nmax > 9:
        import almost_all_seeds as AS
        d = AS.arm_data('modal', 9); U = d['U']; nm = d['names']; mu = d['mu']
        iDc = d['iD']
        estc = [k for k in d['coop'] if U[k, iDc] == -1]
        r9 = [r for r in out['rows'] if r['n'] == 9][0]
        chk = dict(classes=len(nm), mu_est=float(mu[estc].sum()), mu_core=float(mu[d['coop_unfakeable']].sum()),
                   mu_pf=float(mu[[q for q in range(len(nm)) if any(U[q, x] > U[x, x] + 1e-9 for x in estc)]].sum()))
        out['check9'] = dict(direct=chk, subblock=dict(classes=r9['classes'], mu_est=r9['cut']['est'], mu_core=r9['cut']['core'], mu_pf=r9['cut']['pf']))
        print('check n=9 direct', chk, 'sub-block', out['check9']['subblock'], flush=True)
        json.dump(out, open(a.out, 'w'), indent=1)
    print('total %.0fs' % (time.time() - t0))



# ------------------------------------------------------------------ Part B: I = 4 merging pilot
import seeds_in_n as SN
import almost_all_seeds as AS
from multiprocessing import Pool

ROWS = os.path.join(RUNS, 'seeds-tail-rows.json')
GENS = 100000
CATS = ('establisher', 'probe-faker', 'D', 'ALLC', 'other self-cooperator', 'other')


@njit(cache=True)
def _snap(counts, pres, npres, i, out):
    for r in range(6):
        out[i, r, 0] = -1; out[i, r, 1] = 0
    for t in range(npres[i]):
        k = pres[i, t]; c = counts[i, k]
        r = 5
        if c > out[i, 5, 1]:
            while r > 0 and c > out[i, r - 1, 1]:
                out[i, r, 0] = out[i, r - 1, 0]; out[i, r, 1] = out[i, r - 1, 1]; r -= 1
            out[i, r, 0] = k; out[i, r, 1] = c


_KERNEL = None


def kernel():
    """seeds_in_n._run with event counters that draw no random numbers (checked by `check`)."""
    global _KERNEL
    if _KERNEL is not None:
        return _KERNEL
    import inspect
    src = inspect.getsource(SN._run.py_func).replace('@njit(cache=True)\n', '')
    reps = [
        ('def _run(U, PCC, init, N, w, m, gens, every, seed, iC, coopmask, coremask, T0):',
         'def _run(U, PCC, init, N, w, m, gens, every, seed, iC, coopmask, coremask, T0, cat, ev_mig, ev_intro, first_strong, first_cert_isl, snap_strong, snap_cert):'),
        ("            if victim == child:\n                continue\n",
         "            if src != i:\n                wdw = 0 if first_cert < 0 else 1\n                ev_mig[wdw, cat[child], strong[i]] += 1\n"
         "                if counts[i, child] == 0:\n                    ev_intro[wdw, cat[child], strong[i]] += 1\n"
         "            if victim == child:\n                continue\n"),
        ("                if fz and allco:\n                    ncert += 1\n",
         "                if fz and allco:\n                    if first_cert_isl[i] < 0:\n                        first_cert_isl[i] = g + 1\n"
         "                        _snap(counts, pres, npres, i, snap_cert)\n                    ncert += 1\n"),
        ("                if 10 * co >= 9 * N:\n                    strong[i] = 1\n",
         "                if 10 * co >= 9 * N:\n                    if first_strong[i] < 0:\n                        first_strong[i] = g + 1\n"
         "                        _snap(counts, pres, npres, i, snap_strong)\n                    strong[i] = 1\n"),
    ]
    for a_, b_ in reps:
        assert src.count(a_) == 1, a_
        src = src.replace(a_, b_)
    ns = dict(vars(SN)); ns['_snap'] = _snap
    exec(compile(src, 'seeds_tail_kernel', 'exec'), ns)
    _KERNEL = njit(cache=False)(ns['_run'])
    return _KERNEL


_DB = {}


def bdata(n=6):
    if n in _DB:
        return _DB[n]
    d = SN.data(n)
    U = d['U']; nm = d['names']; K = len(nm); iD = d['iD']
    est = [k for k in d['coop'] if U[k, iD] == -1]
    fk = [q for q in range(K) if any(U[q, x] > U[x, x] + 1e-9 for x in est)]
    cat = np.full(K, 5, np.int64)
    for k in d['coop']: cat[k] = 4
    for k in fk: cat[k] = 1
    cat[d['iC']] = 3; cat[iD] = 2
    for k in est: cat[k] = 0
    d = dict(d); d['est'] = est; d['estmask'] = np.zeros(K, bool); d['estmask'][est] = True; d['cat'] = cat; d['fk'] = fk
    _DB[n] = d
    return d


def cells():
    """(n, N, I, mN, reps)."""
    return [(6, 400, 4, 0.1, 60), (6, 400, 4, 1.0, 60), (6, 400, 4, 10.0, 60), (6, 400, 4, 0.0, 100), (6, 1600, 1, 0.0, 240)]


def seed_of(N, I, mN, rep):
    """Fresh salt (20261005): no earlier seeds run is replayed."""
    return [N, I, int(round(mN * 10)), rep, 20261005], 1000003 * rep + 11 * N + 5 * I + int(round(mN * 1000)) + 20261005


def job(j):
    n, N, I, mN, rep, gens = j
    d = bdata(n); run = kernel()
    U, PCC, mu = d['U'], d['PCC'], d['mu']
    K = len(mu); nm = d['names']
    rs, ss = seed_of(N, I, mN, rep)
    rng = np.random.default_rng(rs)
    init = np.zeros((I, K), np.int64)
    for i in range(I):
        init[i] = rng.multinomial(N, mu)
    ev_mig = np.zeros((2, 6, 2), np.int64); ev_intro = np.zeros((2, 6, 2), np.int64)
    fs = -np.ones(I, np.int64); fc = -np.ones(I, np.int64)
    ss_ = -np.ones((I, 6, 2), np.int64); sc_ = -np.ones((I, 6, 2), np.int64)
    t = time.time()
    out = run(U, PCC, init, N, W, mN / N, gens, 20, ss, d['iC'], d['coopmask'], d['coremask'], 0,
              d['cat'], ev_mig, ev_intro, fs, fc, ss_, sc_)
    (st, sg, counts, isl_cc, isl_pay, first_noC, ext_C, lb, la, tr_cc, tr_np, loss_log, loss_snap,
     tC_first, tC_last, C_reent, tC_glob, core_glob, first_cert, first_cert_core, atT0) = out
    glob = counts.sum(0)
    cc = float(isl_cc.mean()); pay = float(isl_pay.mean())

    def named(sn, i):
        return [(nm[int(c)], int(k)) for c, k in sn[i] if c >= 0]

    def origin(sn, i):
        """Largest cooperative class in the snapshot: in the island's own seed (local) or not (import)."""
        for c, k in sn[i]:
            if c >= 0 and d['coopmask'][c]:
                return 'local' if init[i, c] > 0 else 'import'
        return None
    losses = []
    for x, sn in zip(loss_log, loss_snap):
        r = SN.mechanism(d, sn[:, 0], sn[:, 1], int(x[4]), int(x[2]))
        r.update(gen=int(x[0]), island=int(x[1]), after_allc=int(x[3]), snapshot_gen=int(x[5]))
        losses.append(r)
    holders = []
    for i in range(I):
        nz = np.nonzero(counts[i])[0]
        holders.append(nm[int(nz[np.argmax(counts[i, nz])])])
    resolved = st in (1, 2, 3, 5)
    isl_out = [AS.outcome(c, p) for c, p in zip(isl_cc, isl_pay)]
    if mN > 0:
        outc = AS.outcome(cc, pay) if st in (1, 2, 3) else ('unresolved' if st == 4 else None)
    else:
        outc = ('efficient' if all(o == 'efficient' for o in isl_out) else 'not all efficient') if st == 5 else 'unresolved'
    fc0 = int(np.argmin(np.where(fc >= 0, fc, 1 << 60))) if (fc >= 0).any() else -1
    r = dict(n=n, N=N, I=I, mN=mN, rep=rep, gens=gens, status=AS.STATUS.get(int(st), str(st)), stop_gen=int(sg), pcc=cc, pay=pay,
             outcome=outc, isl_out=isl_out, isl_cc=[round(float(c), 4) for c in isl_cc],
             final={nm[k]: int(v) for k, v in enumerate(glob) if v > 0}, holders=holders,
             isl_final=[{nm[k]: int(counts[i, k]) for k in np.nonzero(counts[i])[0]} for i in range(I)],
             first_cert=int(first_cert), first_strong=fs.tolist(), first_cert_isl=fc.tolist(),
             snap_strong=[named(ss_, i) for i in range(I)], snap_cert=[named(sc_, i) for i in range(I)],
             origin_strong=[origin(ss_, i) for i in range(I)], origin_cert=[origin(sc_, i) for i in range(I)],
             founder=(named(sc_, fc0)[0][0] if fc0 >= 0 and named(sc_, fc0) else None), founder_island=fc0,
             ev_mig=ev_mig.tolist(), ev_intro=ev_intro.tolist(),
             seed_n_est=[int(init[i, d['est']].sum()) for i in range(I)], seed_n_core=[int(init[i, d['coop_unfakeable']].sum()) for i in range(I)],
             seed_n_fk=[int(init[i, d['fk']].sum()) for i in range(I)],
             tC_glob=float(tC_glob), lost_before=int(lb), lost_after=int(la), losses=losses, time_s=time.time() - t)
    return r


def key(r):
    return (r['n'], r['N'], r['I'], r['mN'], r['rep'])


def warm():
    kernel(); bdata(6)


def check_main(a):
    """The event kernel reproduces seeds_in_n._run draw for draw (T0 = 0)."""
    d = bdata(6); K = len(d['mu']); run = kernel()
    ok = True
    for N, I, mN in ((400, 4, 0.1), (400, 4, 10.0), (400, 4, 0.0), (1600, 1, 0.0), (100, 4, 1.0)):
        for rep in range(3):
            rng = np.random.default_rng([N, I, rep, 99])
            init = np.array([rng.multinomial(N, d['mu']) for _ in range(I)], np.int64)
            A = SN._run(d['U'], d['PCC'], init, N, W, mN / N, 20000, 20, 31 + rep, d['iC'], d['coopmask'], d['coremask'], 0)
            B = run(d['U'], d['PCC'], init, N, W, mN / N, 20000, 20, 31 + rep, d['iC'], d['coopmask'], d['coremask'], 0, d['cat'],
                    np.zeros((2, 6, 2), np.int64), np.zeros((2, 6, 2), np.int64), -np.ones(I, np.int64), -np.ones(I, np.int64),
                    -np.ones((I, 6, 2), np.int64), -np.ones((I, 6, 2), np.int64))
            same = all(np.array_equal(np.asarray(x), np.asarray(y)) for x, y in zip(A, B))
            ok &= same
            print(N, I, mN, rep, 'same' if same else 'DIFFERENT', A[0], A[1], flush=True)
    print('ALL SAME' if ok else 'MISMATCH')


def run_main(a):
    rows = json.load(open(ROWS)) if os.path.exists(ROWS) else []
    done = {key(r) for r in rows}
    jobs = [(n, N, I, mN, rep, a.gens) for n, N, I, mN, reps in cells() for rep in range(reps) if (n, N, I, mN, rep) not in done]
    jobs.sort(key=lambda j: (-j[3], -j[1]))
    print('%d jobs' % len(jobs), flush=True)
    t0 = time.time()
    with Pool(a.procs, initializer=warm) as pool:
        for r in pool.imap_unordered(job, jobs):
            rows.append(r)
            print('N=%d I=%d mN=%g rep %d: %s %s gen %d P(C,C) %.3f first_cert %d (%.1fs; %.0fs total)' % (
                r['N'], r['I'], r['mN'], r['rep'], r['status'], r['outcome'], r['stop_gen'], r['pcc'], r['first_cert'],
                r['time_s'], time.time() - t0), flush=True)
            if len(rows) % 20 == 0:
                json.dump(rows, open(ROWS, 'w'))
    json.dump(rows, open(ROWS, 'w'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['static', 'check', 'run', 'report'])
    ap.add_argument('nmax', type=int, nargs='?', default=12)
    ap.add_argument('--nmin', type=int, default=6)
    ap.add_argument('--out', default=STATIC)
    ap.add_argument('--check9', type=int, default=1)
    ap.add_argument('--procs', type=int, default=3)
    a = ap.parse_args()
    ap_gens = GENS
    if a.what == 'static': static_main(a)
    elif a.what == 'check': check_main(a)
    elif a.what == 'run':
        a.gens = GENS
        run_main(a)
    elif a.what == 'report':
        import seeds_tail_report as R
        R.main()
