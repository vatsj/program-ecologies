"""Driver for legitimate detectors (predictions/2026-10-17-legitimate-detectors.md, notes/detectors.md).

    python3 src/detectors_run.py gate                       # the soundness gate (term level), go/no-go
    python3 src/detectors_run.py static [--workers 3]      # world K: the milestone-5 closure under the keyed reading
    python3 src/detectors_run.py ext [--workers 3]         # K: executed production of new keys, OSV/SPO, sets
    python3 src/detectors_run.py grudge [--workers 3]      # the grudge pair tables W, AG1, AG2
    python3 src/detectors_run.py validate                  # reproduction of stored runs; kernel checks
    python3 src/detectors_run.py cells --part A|B|C ...    # the cells
Raw arrays go to runs/detectors/ (npy/pkl, not committed); summaries to json.
"""
import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import detectors as DT

OUT = DT.OUT


def log(*a):
    print(*a, flush=True)


def _js(x):
    if isinstance(x, dict): return {str(k): _js(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [_js(v) for v in x]
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, (np.floating,)): return float(x)
    if isinstance(x, (np.bool_,)): return bool(x)
    return x


def cmd_gate(a):
    rep = DT.gate(n_sample=a.n, log=log)
    json.dump(_js(rep), open(os.path.join(ROOTRUNS, 'detectors-gate.json'), 'w'), indent=1)
    log('GATE: %s (bad: %s; unexpected: %s; %.0fs)' % ('GO' if rep['go'] else 'NO-GO', rep['bad'], rep['unexpected'],
                                                      rep['time_s']))


ROOTRUNS = os.path.join(DT.ROOT, 'runs')
KDIR = os.path.join(OUT, 'K')


def cmd_static(a):
    """World K: milestone 5's unit closure and tables, every check under the keyed reading (notes §1.3)."""
    from multiprocessing import Pool
    import lt_genes_pop as GP
    t0 = time.time()
    DT.install_library('key')
    DT.set_world('K')
    sync = os.path.join(KDIR, 'sync')
    os.makedirs(sync, exist_ok=True)
    U = GP.Universe(DT.K, DT.PCAP, verbose=True)
    with Pool(min(3, a.workers), initializer=DT._winit_K, initargs=(DT.K, DT.PCAP, sync)) as pool:
        Tb = GP.Tables(U, pool, verbose=True, sync_dir=sync)
        cl = GP.Closure(Tb, verbose=True)
        rounds = cl.run()
        log('closure converged after %d rounds: units %d, scripts %d, checks %d (%.0fs check time), total %.0fs' % (
            rounds, len(U.units), len(U.scripts), Tb.n_checks, Tb.t_checks, time.time() - t0))
        st = GP.finalize(cl, verbose=True)
    st['time_s'] = time.time() - t0
    GP.save_static(st, U, Tb, cl, os.path.join(KDIR, 'static'))
    log('static K done (%.0fs)' % (time.time() - t0))


_EXW = {}


def _exinit_K(units, scripts):
    import lt_genes_pop as GP
    sys.setrecursionlimit(1000000)
    DT.install_library('key')
    DT.set_world('K')
    U = GP.Universe(DT.K, DT.PCAP)
    U.scripts = list(scripts); U.sid = {k: i for i, k in enumerate(U.scripts)}
    U.units = list(units); U.uid = {k: i for i, k in enumerate(U.units)}
    _EXW['U'] = U


def _exec_prod_job_K(items):
    """Term-executed productions in world K (the Key library; keyed terms): outcome per memo key."""
    import lt_code as L
    import lt_genes as G
    U = _EXW['U']
    out = []
    for tag, key, u, v, rel in items:
        if len(L.CACHE) > 200000: L.CACHE.clear()
        xt = DT.key_term_K(U, U.units[u], 'H')
        if v is None: yt = L.PROG_D
        elif rel == 's': yt = xt
        else: yt = DT.key_term_K(U, U.units[v], 'C' if rel == 'w' else 'H')
        s, n, oc = G.produce_term(xt, yt, 'C' if tag == 'C' else 'D', DT.V, DT.K, DT.PCAP, DT.K)
        out.append((tag, key, oc, n))
    return out


def cmd_ext(a):
    """World K: executed production outcomes (new memo keys executed; keys shared with L reuse the stored outcome,
    a random sample re-executed as a check), OSV/SPO placeholders (used only by S-k windows and counters), sets."""
    from multiprocessing import Pool
    import lt_genes_pop as GP
    import provenance_run as PR
    t0 = time.time()
    st, meta = GP.load_static(os.path.join(KDIR, 'static'))
    exL = json.load(open(os.path.join(PR.OUT, 'prod_exec.json')))
    dL = {(tag, tuple(key)): oc for tag, key, oc in exL}
    keys = [('C', k) for k in meta['prodC']] + [('D', k) for k in meta['prodD']]
    new = [(tag, k) for tag, k in keys if (tag, tuple(k)) not in dL]
    old = [(tag, k) for tag, k in keys if (tag, tuple(k)) in dL]
    rng = np.random.default_rng(20261017)
    samp = [old[i] for i in rng.choice(len(old), size=min(a.nsample, len(old)), replace=False)]
    log('K memo keys %d: shared with L %d, new %d; re-executing %d shared' % (len(keys), len(old), len(new), len(samp)))
    items = []
    for tag, k in new + samp:
        u, v, rel = meta['prod_rep'][(tag, k)]
        items.append((tag, k, int(u), None if v is None else int(v), rel))
    res = []
    nw = min(3, a.workers)
    with Pool(nw, initializer=_exinit_K, initargs=(meta['units'], meta['scripts'])) as pool:
        for out in pool.imap_unordered(_exec_prod_job_K, [items[i::nw * 4] for i in range(nw * 4)]):
            res.extend(out)
    newset = set((tag, tuple(k)) for tag, k in new)
    kset = set((t_, tuple(k_)) for t_, k_ in keys)
    ex = [[tag, list(kk), oc] for (tag, kk), oc in dL.items() if (tag, kk) in kset]
    agree = 0; checked = 0; disagree = []
    for tag, k, oc, n in res:
        kt = (tag, tuple(k))
        if kt in newset:
            ex.append([tag, list(k), oc])
        else:
            checked += 1
            ref = dL[kt]
            to = lambda o: o in ('capTO', 'fuelTO')
            if to(ref) == to(oc): agree += 1
            else: disagree.append([tag, list(k), ref, oc])
    json.dump(ex, open(os.path.join(KDIR, 'prod_exec.json'), 'w'))
    T = st['PRODC'].shape[0]; ns = len(meta['scripts'])
    np.save(os.path.join(KDIR, 'OSV.npy'), np.full((T, ns, 64), -1, np.int8))
    np.save(os.path.join(KDIR, 'SPO.npy'), np.zeros((T, ns), bool))
    old_out = PR.OUT
    PR.OUT = KDIR
    try:
        PR.cmd_sets(argparse.Namespace(which='ext'))
    finally:
        PR.OUT = old_out
    rep = dict(keys=len(keys), shared=len(old), new=len(new),
               new_cap_timeouts=sum(1 for tag, k, oc, n in res if (tag, tuple(k)) in newset and oc in ('capTO', 'fuelTO')),
               shared_rechecked=checked, shared_timeout_agree=agree, shared_disagree=disagree[:20], time_s=time.time() - t0)
    json.dump(_js(rep), open(os.path.join(KDIR, 'ext.json'), 'w'), indent=1)
    log(json.dumps(_js(rep)))


def cmd_grudge(a):
    """The grudge pair tables over world K's writer units: W (validity of Key_v[δ_w] at (w, v)), AG1 (both actions with
    w's grudge against v), AG2 (writer pairs with grudges both ways), PW (the prewritten oracle), wdel (δ script id),
    plus a sham audit."""
    from multiprocessing import Pool
    import lt_genes_pop as GP
    t0 = time.time()
    st, meta = GP.load_static(os.path.join(KDIR, 'static'))
    units, scripts = meta['units'], meta['scripts']
    cat, names = DT.catalogue()
    eff = set(DT.eff_trees(cat))
    O = np.asarray(st['O'])
    writers = []
    wdel = []
    for u in O.tolist():
        t, cs, ds = units[u]
        if t not in eff: continue
        hy = [s for s in ds if DT.has_hyp(scripts[s][1])]
        if hy:
            writers.append(u); wdel.append(hy[0])
    nW = len(writers)
    n = len(units)
    log('eff trees %d; writer units %d (of %d reachable); reachable units %d' % (len(eff), nW, len(O), len(O)))
    widx = -np.ones(n, np.int64)
    widx[writers] = np.arange(nW)
    W = np.zeros((nW, n), np.int8)
    AG1 = -np.ones((nW, n), np.int8)
    AG2 = -np.ones((nW, nW), np.int8)
    jobs = []
    chunk = 400
    Ol = O.tolist()
    for w in writers:
        for i in range(0, len(Ol), chunk):
            jobs.append((w, Ol[i:i + chunk]))
    nw = min(3, a.workers)
    done = 0
    with Pool(nw, initializer=DT._ginit, initargs=(units, scripts)) as pool:
        for out in pool.imap_unordered(DT._grudge_job, jobs):
            for w, v, Wv, code in out:
                W[widx[w], v] = Wv; AG1[widx[w], v] = code
            done += 1
            if done % 200 == 0: log('  AG1 jobs %d / %d (%.0fs)' % (done, len(jobs), time.time() - t0))
        jobs2 = [(w1, writers) for w1 in writers]
        for out in pool.imap_unordered(DT._grudge2_job, jobs2):
            for w1, w2, code in out:
                AG2[widx[w1], widx[w2]] = code
        log('  AG2 done (%.0fs)' % (time.time() - t0))
        rng = np.random.default_rng(7)
        sj = [(int(rng.choice(writers)), [int(x) for x in rng.choice(O, 50)]) for _ in range(20)]
        sham_bad = 0; sham_n = 0
        A = np.asarray(st['A'])
        for out in pool.imap_unordered(DT._sham_job, sj):
            for w, v, code in out:
                sham_n += 1
                if code != int(A[w, v]) + 2 * int(A[v, w]): sham_bad += 1
    A = np.asarray(st['A'])
    PW = np.zeros((nW, n), np.int8)
    for iw, w in enumerate(writers):
        PW[iw] = (W[iw] == 1) & (A[w, :] == 1) & (A[:, w] == 0)
    np.savez(os.path.join(KDIR, 'grudge.npz'), writers=np.array(writers), wdel=np.array(wdel), widx=widx, W=W,
             AG1=AG1, AG2=AG2, PW=PW)
    # summary: grudge effects on play
    chg = 0; tot = 0
    for iw, w in enumerate(writers):
        m = W[iw, O] == 1
        tot += int(m.sum())
        base = A[w, O].astype(int) + 2 * A[O, w].astype(int)
        chg += int(((AG1[iw, O] != base) & m).sum())
    rep = dict(eff_trees=len(eff), writers=nW, reachable=len(O), W_true=int(W.sum()), W_pairs_changed=chg,
               W_pairs=tot, AG1_unknown=int((AG1[:, O] < 0).sum()), AG2_unknown=int((AG2 < 0).sum()),
               sham_audit=dict(n=sham_n, differing=sham_bad), time_s=time.time() - t0)
    json.dump(_js(rep), open(os.path.join(KDIR, 'grudge.json'), 'w'), indent=1)
    log(json.dumps(_js(rep)))


# ================================================================================================================
# Populations
# ================================================================================================================
SALT_DT = 20261017
GMODE = {'K0': 0, 'KG': 1, 'KGh': 2, 'KGs': 3, 'KGp': 4, 'L': 0}
LAB = {'unheld': 0, 'DET': 1, 'PBN': 2, 'open': 3, 'ident': 4, 'other': 5}
REC = ['cc', 'label', 'det', 'pbn', 'sucker', 'expl_max', 'expl_tot', 'edge', 'edge_noTP', 'det_marked', 'glen',
       'n_types', 'majsp']


def island_record(R, i, cc_i):
    """Per-island checkpoint record (notes §1.5 quantities)."""
    import detectors_kern as KG
    Wd = R.W
    n = int(R.npres[i]); N = R.N
    ks = R.pres[i, :n].copy(); c = R.counts[i, ks].astype(float)
    kb = R.gbase[ks]; u = R.tunit[kb]; s = R.tsp[kb]
    M = KG.gacts_matrix(i, R.pres, R.npres, R.gbase, R.gg, R.GS, R.GN, R.tunit, R.tsp, R.A, R.selfa, R.widx, R.AG1,
                        R.AG2, R.PW, R.gmode).astype(np.int64)
    pay = KG.PAYM[M, M.T].astype(float)
    selfp = np.diag(pay)
    f = (pay @ c - selfp) / (N - 1)
    det = Wd['DET'][s]; pbn = Wd['PBN'][s]; suck = Wd['sucker'][u] == 1
    # majority quote
    qkey = u * 100000 + s
    uq, inv = np.unique(qkey, return_inverse=True)
    qc = np.bincount(inv, weights=c)
    q = int(np.argmax(qc))
    mi = int(np.nonzero(inv == q)[0][0])
    held = M[mi, mi] == 1 and cc_i >= 0.5
    if not held: lab = 0
    elif det[mi]: lab = 1
    elif pbn[mi]: lab = 2
    elif Wd['ident'][u[mi]]: lab = 4
    elif Wd['openu'][u[mi]]: lab = 3
    else: lab = 5
    modal = int(np.argmax(c))
    ex = (M[modal, :] == 1) & (M[:, modal] == 0)
    ex_max = float(c[ex].max() / N) if ex.any() else 0.0
    ex_tot = float(c[ex].sum() / N)
    edge = edge2 = np.nan
    if det.any() and pbn.any():
        wf = lambda m, fv: float((fv[m] * c[m]).sum() / c[m].sum())
        edge = wf(pbn, f) - wf(det, f)
        mm = det | pbn
        cm = c * mm
        f2 = (pay @ cm - selfp * mm) / max(1.0, cm.sum() - 1)
        edge2 = wf(pbn, f2) - wf(det, f2)
    gl = R.GN[R.gg[ks]]
    detn = c[det].sum()
    marked = float(c[det & (gl > 0)].sum() / detn) if detn > 0 else np.nan
    wr = R.widx[u] >= 0
    glen = float((gl[wr] * c[wr]).sum() / c[wr].sum()) if wr.any() else 0.0
    return [float(cc_i), lab, float(c[det].sum() / N), float(c[pbn].sum() / N), float(c[suck].sum() / N), ex_max,
            ex_tot, edge, edge2, marked, glen, n, int(s[mi])]


def fission_founders(kind, rep, Wd, T=12800):
    """B1 (50/50 DET/PBN), B2 (natural shares over DET ∪ PBN), or L (Pangaea's list: identical to its F cells)."""
    import pangaea as PG
    mu = Wd['mu']
    if kind == 'L':
        lst, _ = PG.founder_list(T, rep, 'L', Wd['LS'])
        perm = PG.permutation(T, rep)
        return PG.partition(lst, 100, T // 100, perm)
    rng = np.random.default_rng([T, rep, SALT_DT, {'B1': 1, 'B2': 2}[kind]])
    det = np.nonzero(Wd['DET'])[0]; pbn = np.nonzero(Wd['PBN'])[0]
    if kind == 'B1':
        a = rng.choice(det, size=T // 2, p=mu[det] / mu[det].sum())
        b = rng.choice(pbn, size=T // 2, p=mu[pbn] / mu[pbn].sum())
        lst = np.concatenate([a, b])
    else:
        both = np.concatenate([det, pbn])
        lst = rng.choice(both, size=T, p=mu[both] / mu[both].sum())
    perm = rng.permutation(T)
    return lst[perm].reshape(T // 100, 100)


def cell_spec(cell):
    """cell = '<geom>_<arm>_<sched>': geom in B1, B2, Cff, Cis, Ref; arm in L, K0, KG, KGh, KGs; sched e0, t1, t3."""
    geom, arm, sch = cell.split('_')
    K = {'e0': 0, 't1': 1, 't3': 3}[sch]
    w = 'L' if arm == 'L' else 'K'
    return geom, arm, K, w


def ff_job(job):
    """One fission-fusion (B, Cff, Ref) or island (Cis) run."""
    import detectors as DTm
    import provenance as PV
    import provenance_run as PR
    import pangaea as PG
    import annealed as AN
    import realizable_scaling as RS
    cell, rep, horizon = job
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    geom, arm, Ksch, w = cell_spec(cell)
    Wd = DTm.world(w)
    LS = Wd['LS']
    if geom == 'Cis':
        N, I = 200, 64
        rng = np.random.default_rng([N, I, rep, PR.SALT])
        sp = rng.choice(len(LS['mu']), size=(I, N), p=LS['mu'])
        rule = np.full((I, N), PV.R_SNON, np.int64)
        unit = LS['Eu'][LS['tau'][sp]]
        seed = PR.kernel_seed(N, I, rep)
        mN = RS.mN_cal(N)
        epsg = AN.schedule('ann', N, Ksch) if Ksch else None
        merge_at = 0
    else:
        N, I = 100, 128
        sp = fission_founders('L' if geom in ('Cff', 'Ref') else geom, rep, Wd)
        rule = np.full((I, N), PV.R_SNON, np.int64)
        unit = LS['Eu'][LS['tau'][sp]]
        if geom == 'Ref':
            import removing_rivals as RR
            kPB = Wd['names'].index(RR.PB_SP)
            pos = RR.donor_positions(N, I, rep)
            for i in range(I):
                sp[i, pos[i]] = kPB; rule[i, pos[i]] = PV.R_H; unit[i, pos[i]] = Wd['Hu'][Wd['tau'][kPB]]
        seed = PG.kernel_seed_pg(N, I, rep)
        mN = 1.0
        merge_at = 200
        epsg = None
        if Ksch:
            Tm = N * I
            en = AN.eps_n_annealed(Tm, AN.arrivals_A(Ksch))
            epsg = (en / Tm).astype(np.float64)
    R = DTm.DRun(w, sp, rule, unit, seed, r=100, mN=mN, gmode=GMODE[arm], gcap=3, epsg=epsg, pairmode=1)
    recs = []
    snaps_g = []
    gens_done = 0
    g = 0
    every = 10
    while g < horizon:
        R.advance(every)
        g = R.g
        if merge_at and g == merge_at:
            R.merge(PG.kernel_seed_pg(R.N * R.I, 1, rep) ^ 0x5DEECE66D)
        if g <= 1000 or g % 50 == 0:
            cc = R.island_stats()
            recs.append((g, [island_record(R, i, cc[i]) for i in range(R.I)]))
    cc = R.island_stats()
    fin = [island_record(R, i, cc[i]) for i in range(R.I)]
    # universal-open (provenance's): every island held, holders pairwise mutual, every holder open
    maj = R.maj_k.copy()
    held = [R.acts(int(k), int(k))[0] == 1 and cc[i] >= 0.5 for i, k in enumerate(maj)]
    mutual = all(R.acts(int(maj[i]), int(maj[j])) == (1, 1) for i in range(R.I) for j in range(i + 1, R.I))
    openh = all(bool(Wd['openu'][R.tunit[R.gbase[int(k)]]]) for k in maj)
    uo = bool(all(held) and mutual and openh)
    nl = int(R.nglog[0])
    glog = R.glog[:nl].copy()
    # grudge-write summary by (writer class, target class)
    wcls = lambda s: 'DET' if Wd['DET'][s] else ('PBN' if Wd['PBN'][s] else ('suck' if Wd['sucker'][Wd['nat'][s]] else 'other'))
    pairs = {}
    for row in glog.tolist():
        k = wcls(row[2]) + '>' + wcls(row[4]) + (':boot' if row[7] == 0 else ':cert')
        pairs[k] = pairs.get(k, 0) + 1
    na = int(R.narr[0])
    arr_sp = R.arr[:na, 2]
    arr_cls = {}
    for s in arr_sp.tolist():
        k = wcls(s); arr_cls[k] = arr_cls.get(k, 0) + 1
    import detectors_kern as KG
    out = dict(cell=cell, rep=rep, world=w, arm=arm, K=Ksch, horizon=horizon, last_gen=R.g,
               recs=[(gg_, np.round(np.array(r_, float), 5).tolist()) for gg_, r_ in recs],
               final=np.round(np.array(fin, float), 5).tolist(), uo=uo, held=int(sum(held)), mutual=bool(mutual),
               gctr=dict(zip(['write', 'evict', 'adopt', 'live_enc', 'sucker_enc', 'enc', 'selfskip', 'nowriter',
                              'wfail', 'skip_isl', 'recomp', 'dirty', 'boot', 'pred_marked', 'pred_unmarked', 'spare'],
                             R.gctr.tolist())),
               write_pairs=pairs, n_writes_logged=nl, glog_sample=glog[:2000].tolist(),
               isl_sucker_gen=R.isl_sucker_gen.tolist(), arrivals=na, arrivals_cls=arr_cls,
               n_base_types=int(R.ntv[0]), n_grudge_types=int(R.ngt[0]), n_lists=int(R.ngv[0]),
               ctr=R.ctr.sum(0).tolist(), time_s=time.time() - t0)
    return out


def a_job(job):
    """Part A: one predator arrival on an island of the canonical detector (world K)."""
    import detectors as DTm
    import provenance as PV
    N, ps, arm, rep, variant, gcap = job
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    Wd = DTm.world('K')
    names = Wd['names']
    kd = names.index(DTm.DET_SP)
    ud = int(Wd['nat'][kd])
    sp = np.full((1, N), kd, np.int64); rule = np.full((1, N), PV.R_SNON, np.int64); unit = np.full((1, N), ud, np.int64)
    seed = int((rep * 1000003 + N * 10007 + ps * 101 + GMODE[arm] * 7 + {'first': 0, 'exact': 1, 'syn': 2}[variant] * 13
                + gcap * 17 + SALT_DT) % (2 ** 62))
    rng = np.random.default_rng([seed % (2 ** 31), 5])
    R = DTm.DRun('K', sp, rule, unit, seed, r=100, mN=0.0, gmode=GMODE[arm], gcap=gcap)

    def inject(s):
        import detectors_kern as KG
        j = int(rng.integers(N))
        kb, nt = PV.make_type(R.d, R.tunit, R.trule, R.tsp, R.tanc, int(R.ntv[0]), int(Wd['spE'][s]), PV.R_SNON, s, 0)
        R.ntv[0] = nt
        k = KG.gmake(R.gdict2, R.gbase, R.gg, R.ngt, kb, 0, R.freel, R.nfree)
        old = R.slots[0, j]
        R.slots[0, j] = k
        KG.gchange(0, old, k, R.counts, R.paysum, R.pres, R.npres, R.pos, R.gbase, R.gg, R.GS, R.GN, R.tunit, R.tsp,
                   R.A, R.selfa, R.widx, R.AG1, R.AG2, R.PW, R.gmode, R.gdirty, R.gcount, R.gdict2, R.freel, R.nfree)
        R.spcount[0, R.tsp[R.gbase[old]]] -= 1; R.spcount[0, s] += 1
        bo = R.gbase[old]
        R.uns[0] += (0 if PV.is_settled(kb, R.tunit, R.trule, R.tset, R.LS['st']['BLC'], R.LS['st']['BLD'], R.LS['PD'],
                                        R.LS['st']['utau'], R.LS['FUT']) else 1) - \
            (0 if PV.is_settled(bo, R.tunit, R.trule, R.tset, R.LS['st']['BLC'], R.LS['st']['BLD'], R.LS['PD'],
                                R.LS['st']['utau'], R.LS['FUT']) else 1)
        R.rulecount[PV.R_SNON] += 0
        PV.plog_open(0, j, kb, R.tunit, R.trule, R.LS['st']['BLC'], R.plog)

    def run_until(s, gmax=1000):
        maxc = 1; gstart = R.g
        while True:
            R.advance(1)
            cnt = int(R.spcount[0, s])
            maxc = max(maxc, cnt)
            if cnt >= N // 2: return 'established', R.g - gstart, maxc
            if cnt == 0: return 'lost', R.g - gstart, maxc
            if R.g - gstart >= gmax: return 'censored', R.g - gstart, maxc

    def marked(s):
        ks = R.pres[0, :R.npres[0]]
        c = R.counts[0, ks]
        isd = R.tsp[R.gbase[ks]] == kd
        hold = np.array([s in R.glist(k) for k in ks])
        return float(c[isd & hold].sum() / max(1, c[isd].sum()))
    R.advance(2)                                         # settle the residents (no-op: they are at their natural unit)
    out = dict(N=N, pred=names[ps], pred_sp=int(ps), arm=arm, rep=rep, variant=variant, gcap=gcap)
    inject(ps)
    res, dur, mx = run_until(ps)
    out.update(first=res, first_t=dur, first_max=mx, marked_after_first=marked(ps),
               writes_first=int(R.gctr[0]), live_first=int(R.gctr[3]))
    if variant != 'first':
        if res == 'lost':
            s2 = ps
            if variant == 'syn':
                t = int(Wd['tau'][ps])
                cand = [j for j in Wd['LS']['cat'].members[t] if j != ps]
                s2 = int(cand[rep % len(cand)])
            out['second_sp'] = names[s2]
            inject(s2)
            res2, dur2, mx2 = run_until(s2)
            out.update(second=res2, second_t=dur2, second_max=mx2, marked_after_second=marked(s2))
        else:
            out.update(second=None)
    out.update(gctr=R.gctr.tolist(), time_s=time.time() - t0)
    return out


def run_pool(fn, jobs, path, workers, key=None):
    import gzip
    from multiprocessing import Pool
    rows = json.load(gzip.open(path)) if os.path.exists(path) else []
    done = {jkey(r) for r in rows}
    todo = [j for j in jobs if jkey(j) not in done]
    log('%s: %d jobs, %d done, %d to run on %d workers' % (os.path.basename(path), len(jobs), len(done), len(todo), workers))
    if not todo: return rows
    t0 = time.time()
    last = time.time()
    with Pool(workers, maxtasksperchild=8) as pool:
        for r in pool.imap_unordered(fn, todo):
            rows.append(_js(r))
            log('  %s (%.0fs; total %.0fs)' % (short(r), r['time_s'], time.time() - t0))
            if time.time() - last > 120:
                json.dump(rows, gzip.open(path + '.tmp', 'wt')); os.replace(path + '.tmp', path); last = time.time()
    json.dump(rows, gzip.open(path + '.tmp', 'wt')); os.replace(path + '.tmp', path)
    return rows


def jkey(j):
    if isinstance(j, dict): return (j.get('cell'), j.get('rep')) if 'cell' in j else (j['N'], j['pred_sp'], j['arm'], j['rep'], j['variant'], j['gcap'])
    if len(j) == 3: return (j[0], j[1])
    return (j[0], j[1], j[2], j[3], j[4], j[5])


def short(r):
    if 'cell' in r:
        f = r['final']
        return '%s rep %d: last %d, final islands %d, det %.3f pbn %.3f writes %d types %d' % (
            r['cell'], r['rep'], r['last_gen'], len(f), sum(x[2] for x in f) / len(f), sum(x[3] for x in f) / len(f),
            r['gctr']['write'], r['n_grudge_types'])
    return 'A N=%d %s %s rep %d %s: %s %s' % (r['N'], r['pred'], r['arm'], r['rep'], r['variant'], r['first'],
                                             r.get('second'))


def _val_job(job):
    """Reproduction of a stored run with the grudge kernel at gmode 0 in world L (draw for draw)."""
    import detectors as DTm
    import provenance as PV
    import provenance_run as PR
    import pangaea as PG
    import realizable_scaling as RS
    import annealed as AN
    import gzip
    kind, rep, gmax = job
    t0 = time.time()
    Wd = DTm.world('L')
    LS = Wd['LS']
    bad = []
    if kind == 'scal':
        rows = [r for r in json.load(gzip.open(os.path.join(DT.ROOT, 'runs/realizable_scaling/lottery_main.json.gz')))
                if r['cell'] == 'rs_Snon_200_64_cal' and r['rep'] == rep]
        ref = {t[0]: t for t in rows[0]['trace']}
        N, I = 200, 64
        rng = np.random.default_rng([N, I, rep, PR.SALT])
        sp = rng.choice(len(LS['mu']), size=(I, N), p=LS['mu'])
        R = DTm.DRun('L', sp, np.full((I, N), PV.R_SNON, np.int64), LS['Eu'][LS['tau'][sp]], PR.kernel_seed(N, I, rep),
                     r=100, mN=RS.mN_cal(N))
        n = 0
        while R.g < gmax:
            R.advance(10)
            if R.g in ref:
                cc = R.island_stats()
                t = ref[R.g]
                n += 1
                if abs(float(cc.mean()) - t[1]) > 1e-9 or int(R.ntv[0]) != t[7]:
                    bad.append((R.g, float(cc.mean()), t[1], int(R.ntv[0]), t[7]))
    elif kind == 'ff':
        rows = [r for r in json.load(gzip.open(os.path.join(DT.ROOT, 'runs/pangaea/lottery_F.json.gz')))
                if r['cell'] == 'pg_L_100_128_r100_ff200' and r['rep'] == rep]
        ref = {t['g']: t for t in rows[0]['trace']}
        N, I = 100, 128
        sp = fission_founders('L', rep, Wd)
        R = DTm.DRun('L', sp, np.full((I, N), PV.R_SNON, np.int64), LS['Eu'][LS['tau'][sp]],
                     PG.kernel_seed_pg(N, I, rep), r=100, mN=1.0)
        n = 0
        while R.g < gmax:
            R.advance(10)
            if R.g == 200:
                R.merge(PG.kernel_seed_pg(R.N * R.I, 1, rep) ^ 0x5DEECE66D)
            if R.g in ref:
                cc = R.island_stats()
                t = ref[R.g]
                ntp = int(sum(int(R.npres[i]) for i in range(R.I))) if R.I == 1 else \
                    int(len(np.nonzero(R.counts[:, :R.ngt[0]].sum(0))[0]))
                n += 1
                if abs(float(cc.mean()) - t['pcc']) > 1e-4 or ntp != t['nt']:
                    bad.append((R.g, float(cc.mean()), t['pcc'], ntp, t['nt']))
    else:
        rows = [r for r in json.load(gzip.open(os.path.join(DT.ROOT, 'runs/annealed/cells_main.json.gz')))
                if r['cell'] == 'an_i_200' and r['rep'] == rep]
        snaps = rows[0]['snaps']
        N, I = 200, 8
        rng = np.random.default_rng([N, I, rep, PR.SALT])
        sp = rng.choice(len(LS['mu']), size=(I, N), p=LS['mu'])
        R = DTm.DRun('L', sp, np.full((I, N), PV.R_SNON, np.int64), LS['Eu'][LS['tau'][sp]], PR.kernel_seed(N, I, rep),
                     r=100, mN=RS.mN_cal(N), epsg=AN.schedule('ann', N, 3), pairmode=1)
        n = 0
        while R.g < gmax:
            R.advance(10)
            if str(R.g) in snaps:
                s = snaps[str(R.g)]
                R.island_stats()
                hs = [int(R.tsp[R.gbase[k]]) for k in R.maj_k]
                n += 1
                if int(R.ntv[0]) != s['n_types'] or hs != s['holder_sp']:
                    bad.append((R.g, int(R.ntv[0]), s['n_types'], hs, s['holder_sp']))
    return dict(kind=kind, rep=rep, compared=n, bad=bad, time_s=time.time() - t0)


B_CELLS = ['B1_K0_e0', 'B1_KG_e0', 'B1_K0_t1', 'B1_KG_t1', 'B1_K0_t3', 'B1_KG_t3',
           'B2_K0_e0', 'B2_KG_e0', 'B2_K0_t1', 'B2_KG_t1']
C_CELLS = ['Cff_L_e0', 'Cff_K0_e0', 'Cff_KG_e0', 'Cff_K0_t1', 'Cff_KG_t1', 'Cff_KGh_e0', 'Cff_KGs_e0',
           'Cis_L_e0', 'Cis_K0_e0', 'Cis_KG_e0', 'Cis_K0_t1', 'Cis_KG_t1']
REF_CELLS = ['Ref_KG_e0']
A_ARMS = ['K0', 'KG', 'KGh', 'KGs', 'KGp']


def a_jobs(preds, reps=100):
    jobs = []
    for N in (200, 800):
        for arm in A_ARMS:
            for ps in preds:
                for rep in range(reps):
                    jobs.append((N, ps, arm, rep, 'first', 3))
    for arm in ('KG', 'KGh'):
        for variant in ('exact', 'syn'):
            for rep in range(reps):
                jobs.append((200, preds[0], arm, rep, variant, 3))
    for arm in ('K0', 'KG', 'KGh'):
        for rep in range(50):
            jobs.append((3200, preds[0], arm, rep, 'first', 3))
    return jobs


def top_predators(k=3):
    import detectors as DTm
    import removing_rivals as RR
    import provenance as PV
    Wd = DTm.world('K')
    LS = Wd['LS']
    kd = Wd['names'].index(DTm.DET_SP)
    pt = DTm.with_rr(LS, RR.predator_table, int(Wd['nat'][kd]), kd, PV.R_SNON, [Wd['uFB'], Wd['uPB']], LS)
    order = np.argsort(-LS['mu'] * pt['is_pred'])[:k]
    return [int(s) for s in order if pt['is_pred'][s]], pt


def cmd_cells(a):
    nw = min(3, a.workers)
    if a.part == 'A':
        preds, pt = top_predators()
        log('top predators: %s (mass %.4f)' % ([DT.world('K')['names'][s] for s in preds], pt['mass']))
        jobs = a_jobs(preds, a.reps)
        if a.limit: jobs = jobs[:a.limit]
        run_pool(a_job, jobs, os.path.join(OUT, 'cells_A%s.json.gz' % a.tag), nw)
        return
    cells = {'B': B_CELLS, 'C': C_CELLS, 'R': REF_CELLS}[a.part] if not a.cells else a.cells
    jobs = [(c, rep, a.horizon) for rep in range(a.rep0, a.rep0 + a.reps) for c in cells]
    run_pool(ff_job, jobs, os.path.join(OUT, 'cells_%s%s.json.gz' % (a.part, a.tag)), nw)


def cmd_statics(a):
    """Notes §2 statics: the canonical detector in L and K, DET and PBN, predators, writers."""
    import detectors as DTm
    import removing_rivals as RR
    import provenance as PV
    out = {}
    for w in ('L', 'K'):
        Wd = DTm.world(w)
        LS = Wd['LS']; A = Wd['A']; sa = Wd['sa']; names = Wd['names']; mu = Wd['mu']; tau = Wd['tau']; Hu = Wd['Hu']
        kd = names.index(DTm.DET_SP)
        ud = int(Wd['nat'][kd])
        units = LS['meta']['units']; scripts = LS['meta']['scripts']
        refs = {'C': Wd['uC'], 'D': Wd['uD'], 'FairBot': Wd['uFB'], 'PrudentBot': Wd['uPB'],
                'anti-punisher': int(Hu[tau[names.index('if(CHK(them,^D,D),D,C)')]])}
        O = np.asarray(LS['st']['O'])
        t, cs, ds = units[ud]
        det = dict(unit=ud, C=[DTm.C.show_script(scripts[s][1]) for s in cs], D=[DTm.C.show_script(scripts[s][1]) for s in ds],
                   self=int(sa[ud]), twin=int(A[ud, ud]), coop_with=int((A[ud, O] == 1).sum()), of=len(O),
                   vs={k: [int(A[ud, v]), int(A[v, ud])] for k, v in refs.items()}, in_T=bool(Wd['T'][ud]))
        pt = DTm.with_rr(LS, RR.predator_table, ud, kd, PV.R_SNON, [Wd['uFB'], Wd['uPB']], LS)
        det['pred_mass'] = pt['mass']; det['pred_n'] = pt['n_sp']; det['pred_top'] = pt['top']
        det['pred_constants'] = pt['constants']
        # exploiters (any program it cooperates with that defects against it), including self-cooperators
        ph = pt['phen']
        ex = (A[ud, ph] == 1) & (A[ph, ud] == 0)
        det['exploiter_mass'] = float(mu[ex].sum())
        out[w] = dict(detector=det, DET=dict(n=int(Wd['DET'].sum()), mass=float(mu[Wd['DET']].sum()),
                                             top=[(names[s], float(mu[s])) for s in np.argsort(-mu * Wd['DET'])[:12]]),
                      PBN=dict(n=int(Wd['PBN'].sum()), mass=float(mu[Wd['PBN']].sum())),
                      effsp=dict(n=int(Wd['effsp'].sum()), mass=float(mu[Wd['effsp']].sum())),
                      T_units=int(Wd['T'].sum()), units=len(units), reachable=len(O),
                      sucker_mass=float(mu[Wd['sucker'][Wd['nat']] == 1].sum()),
                      writers=int(len(Wd['writers'])))
        # DET members' relations to PrudentBot-H / FairBot-H at natural units
        dn = Wd['nat'][Wd['DET']]
        out[w]['DET_mutual_PB'] = float(((A[dn, Wd['uPB']] == 1) & (A[Wd['uPB'], dn] == 1)).mean()) if len(dn) else None
        out[w]['DET_mutual_FB'] = float(((A[dn, Wd['uFB']] == 1) & (A[Wd['uFB'], dn] == 1)).mean()) if len(dn) else None
        log(w, json.dumps(_js(out[w]))[:3000])
    json.dump(_js(out), open(os.path.join(ROOTRUNS, 'detectors-static.json'), 'w'), indent=1)


def cmd_audit(a):
    """The two-bit reduction against explicit terms: individuals' actual spellings (bodies of their own spelling) and
    full grudge lists, host replay, against the kernel's actions; pairs with a live grudge bit after a B1 KG run."""
    import detectors as DTm
    import provenance as PV
    import pangaea as PG
    import lt_genes as G
    import lt_genes_pop as GP
    import carrier_populations as CP
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    Wd = DTm.world('K')
    LS = Wd['LS']; cat = LS['cat']; meta = LS['meta']
    U = GP.Universe(DTm.K, DTm.PCAP)
    U.scripts = list(meta['scripts']); U.units = list(meta['units'])
    out = dict(pairs=0, agree=0, disagree=[])
    rng = np.random.default_rng(11)
    for cell, rep, gens in (('B1_KG_e0', 0, 250), ('Cff_KG_e0', 0, 250)):
        geom, arm, Ksch, w = cell_spec(cell)
        sp = fission_founders('L' if geom == 'Cff' else geom, rep, Wd)
        R = DTm.DRun('K', sp, np.full(sp.shape, PV.R_SNON, np.int64), LS['Eu'][LS['tau'][sp]],
                     PG.kernel_seed_pg(100, 128, rep), r=100, mN=1.0, gmode=1)
        while R.g < gens:
            R.advance(10)
            if R.g == 200: R.merge(PG.kernel_seed_pg(12800, 1, rep) ^ 0x5DEECE66D)
        ks = np.nonzero(R.counts[:, :R.ngt[0]].sum(0))[0]
        live = []
        for k in ks:
            if not R.glist(int(k)): continue
            for s in R.glist(int(k)):
                js = [j for j in ks if R.tsp[R.gbase[j]] == s]
                for j in js[:2]: live.append((int(k), int(j)))
        rng.shuffle(live)
        bodies = {}

        def term(k):
            kb = R.gbase[k]; s = int(R.tsp[kb]); u = int(R.tunit[kb])
            if s not in bodies:
                bodies[s] = G.marked_body(CP.body_term(cat.sexprs[cat.spell[s]['i']], DTm.V, DTm.K), 'H')
            t, cs, ds = U.units[u]
            dl = [U.scripts[i][1] for i in ds]
            hyp = [x for x in dl if DTm.has_hyp(x)]
            dl = [DTm.keyed(x, DTm.KEY_D) if DTm.has_hyp(x) else x for x in dl]
            for g2 in R.glist(k):
                if g2 not in bodies:
                    bodies[g2] = G.marked_body(CP.body_term(cat.sexprs[cat.spell[g2]['i']], DTm.V, DTm.K), 'H')
                dl.append(DTm.keyed(hyp[0], L_canon(bodies[g2])))
            return DTm.C.carrier(bodies[s], G.canon_list([U.scripts[i][1] for i in cs], dl))
        import lt_code as L
        L_canon = L.canon_term
        h = CP.IdealCheck()
        UVt = np.asarray(LS['st']['UVt'])
        for k, j in live[:a.n]:
            h.clear()
            tk, tj = term(k), term(j)
            uk, uj = int(R.tunit[R.gbase[k]]), int(R.tunit[R.gbase[j]])
            akj, ajk, _ = DTm._pair_acts(U, h, uk, U.units[uk][0], tk, uj, U.units[uj][0], tj, UVt)
            kk = tuple(int(x) for x in R.acts(k, j))
            out['pairs'] += 1
            if (int(akj), int(ajk)) == kk: out['agree'] += 1
            else: out['disagree'].append([cell, k, j, [int(akj), int(ajk)], list(kk), R.glist(k), R.glist(j)])
        log('%s: %d live pairs audited so far, %d agree' % (cell, out['pairs'], out['agree']))
    out['time_s'] = time.time() - t0
    json.dump(_js(out), open(os.path.join(OUT, 'audit.json'), 'w'), indent=1)
    log(json.dumps(_js(out))[:2000])


def cmd_validate(a):
    from multiprocessing import Pool
    jobs = [('scal', 0, 1000), ('scal', 1, 1000), ('ff', 0, 1000), ('ff', 1, 1000), ('ann', 0, 1000), ('ann', 1, 1000)]
    out = []
    with Pool(min(3, a.workers)) as pool:
        for r in pool.imap_unordered(_val_job, jobs):
            log('validate %s rep %d: %d checkpoints compared, %d differ (%.0fs)' % (r['kind'], r['rep'], r['compared'],
                                                                                   len(r['bad']), r['time_s']))
            out.append(r)
    json.dump(_js(out), open(os.path.join(OUT, 'validate.json'), 'w'), indent=1)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('gate'); s.add_argument('--n', type=int, default=240)
    s = sub.add_parser('static'); s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('ext'); s.add_argument('--workers', type=int, default=3); s.add_argument('--nsample', type=int, default=60)
    s = sub.add_parser('grudge'); s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('validate'); s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('statics')
    s = sub.add_parser('audit'); s.add_argument('--n', type=int, default=150)
    s = sub.add_parser('cells'); s.add_argument('--part', required=True); s.add_argument('--workers', type=int, default=3)
    s.add_argument('--reps', type=int, default=20); s.add_argument('--rep0', type=int, default=0)
    s.add_argument('--horizon', type=int, default=10000); s.add_argument('--cells', nargs='*')
    s.add_argument('--tag', default=''); s.add_argument('--limit', type=int, default=0)
    a = ap.parse_args()
    {'gate': cmd_gate, 'static': cmd_static, 'ext': cmd_ext, 'grudge': cmd_grudge, 'validate': cmd_validate,
     'cells': cmd_cells, 'statics': cmd_statics, 'audit': cmd_audit}[a.cmd](a)


if __name__ == '__main__':
    main()
