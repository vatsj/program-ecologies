"""Driver for the prudent-openness cells (predictions/2026-10-11-prudent-openness.md).

    python3 src/prudent_openness_run.py static                       # families, paths, seed payoffs, tilt masses
    python3 src/prudent_openness_run.py validate [--workers 3]       # notes §1.13 (before any counted cell)
    python3 src/prudent_openness_run.py lottery --cells P1 P2 ... [--N 100 --I 64] [--out main]
    python3 src/prudent_openness_run.py chain --N 1000 10000 [--twins 1]

Raw outputs go to runs/prudent_openness/ (json; no npz committed).
"""
import argparse, json, math, os, sys, time
from collections import Counter, defaultdict
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import identity_tags as IT
import identity_tags_run as R
import prudent_openness as PO_

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'prudent_openness')
os.makedirs(OUT, exist_ok=True)
SALT = 20261010            # the identity run's streams (paired seeds, notes §1.8)
CK = np.array(PO_.CKPTS, np.int64)
NF = len(PO_.FAMS)


# ------------------------------------------------------------------ kernel
def _kernel():
    from numba import njit
    from almost_all_seeds import _sample_parent, _island_cc

    @njit(cache=True)
    def closure(U, selfc, glob, K, res_ids, nres, inZ, queue):
        for k in range(K): inZ[k] = False
        qn = 0; qh = 0
        for t in range(nres):
            r = res_ids[t]
            if not inZ[r]:
                inZ[r] = True; queue[qn] = r; qn += 1
        while qh < qn:
            z = queue[qh]; qh += 1
            uzz = U[z, z]
            for q in range(K):
                if glob[q] > 0 and not inZ[q] and U[q, z] >= uzz - 1e-9:
                    inZ[q] = True; queue[qn] = q; qn += 1
        ns = 0
        for t in range(qn):
            if selfc[queue[t]]: ns += 1
        if ns == qn: return 1
        if ns == 0: return 0
        return -1

    @njit(cache=True)
    def majority(counts, pres, npres, i):
        best = -1; bc = -1
        for t in range(npres[i]):
            k = pres[i, t]
            if counts[i, k] > bc or (counts[i, k] == bc and k < best):
                bc = counts[i, k]; best = k
        return best

    @njit(cache=True)
    def run(U, PCC, init, N, w, m, gens, every, seed, selfc, famask, NF, ck, track):
        """The identity run's kernel (same random stream) without the 2,000 stop; family counts per island at every
        event; first zero (event) and first hold (check grid) per island and family; snapshots at the checkpoints."""
        np.random.seed(seed)
        I, K = init.shape
        counts = init.copy()
        paysum = np.zeros((I, K))
        pres = np.zeros((I, K), np.int64); npres = np.zeros(I, np.int64); pos = -np.ones((I, K), np.int64)
        fam = np.zeros((I, NF), np.int64)
        for i in range(I):
            for k in range(K):
                if counts[i, k] > 0:
                    pres[i, npres[i]] = k; pos[i, k] = npres[i]; npres[i] += 1
                    for f in range(NF):
                        if (famask[k] >> f) & 1: fam[i, f] += counts[i, k]
            for t in range(npres[i]):
                j = pres[i, t]
                for t2 in range(npres[i]):
                    k = pres[i, t2]
                    paysum[i, j] += counts[i, k] * U[j, k]
        fam0 = fam.copy()
        zg = -np.ones((I, NF), np.int64); fh = -np.ones((I, NF), np.int64)
        glob = np.zeros(K, np.int64)
        res_ids = np.empty(K, np.int64); inZ = np.zeros(K, np.bool_); queue = np.empty(K, np.int64)
        isl_cc = np.zeros(I); maj = np.zeros(I, np.int64); prevmaj = -np.ones(I, np.int64)
        e3_gen = -1; e3_out = -1
        estab = -1; all_estab = -1
        snap_estab = np.zeros(K, np.int64)
        first_sep = -1; n_sep_chk = 0; n_res_events = 0; was_sep = False
        n_flips = 0; sep_isl_chk = 0
        frozen_gen = -1
        nt = track.shape[0]
        track_ext = -np.ones(nt, np.int64); track_maxisl = np.zeros(nt, np.int64)
        track_alive_at_sep = np.zeros(nt, np.bool_)
        nck = ck.shape[0]
        snap = np.zeros((nck, I, K), np.int64)
        snap_sep = np.zeros(nck, np.bool_)
        nextck = 0
        g_end = gens
        for g in range(gens):
            for e in range(I * N):
                i = np.random.randint(I)
                src = i
                if m > 0.0 and I > 1 and np.random.random() < m:
                    src = np.random.randint(I - 1)
                    if src >= i: src += 1
                child = _sample_parent(counts, paysum, U, pres, npres, src, N, w)
                u = np.random.randint(N); acc = 0; victim = pres[i, 0]
                for t in range(npres[i]):
                    k = pres[i, t]; acc += counts[i, k]
                    if u < acc:
                        victim = k; break
                if victim == child:
                    continue
                counts[i, victim] -= 1
                fv = famask[victim]; fc = famask[child]
                for f in range(NF):
                    if (fv >> f) & 1:
                        fam[i, f] -= 1
                        if fam[i, f] == 0 and zg[i, f] < 0: zg[i, f] = g
                    if (fc >> f) & 1:
                        fam[i, f] += 1
                if counts[i, victim] == 0:
                    p = pos[i, victim]; last = pres[i, npres[i] - 1]
                    pres[i, p] = last; pos[i, last] = p; pos[i, victim] = -1; npres[i] -= 1
                new = counts[i, child] == 0
                if new:
                    pres[i, npres[i]] = child; pos[i, child] = npres[i]; npres[i] += 1
                counts[i, child] += 1
                for t in range(npres[i]):
                    j = pres[i, t]
                    if new and j == child:
                        continue
                    paysum[i, j] += U[j, child] - U[j, victim]
                if new:
                    v = 0.0
                    for t in range(npres[i]):
                        k = pres[i, t]
                        v += counts[i, k] * U[child, k]
                    paysum[i, child] = v
            gg = g + 1
            if gg % every == 0 or gg == gens:
                for k in range(K): glob[k] = 0
                for i in range(I):
                    for t in range(npres[i]):
                        glob[pres[i, t]] += counts[i, pres[i, t]]
                    cc, pay = _island_cc(counts, PCC, U, pres, npres, paysum, i, N)
                    isl_cc[i] = cc
                    if estab < 0 and cc >= 0.9: estab = gg
                    maj[i] = majority(counts, pres, npres, i)
                allheld = True
                for i in range(I):
                    h = selfc[maj[i]] and isl_cc[i] >= 0.5
                    if not h: allheld = False
                    if h:
                        fm = famask[maj[i]]
                        for f in range(NF):
                            if (fm >> f) & 1 and fh[i, f] < 0: fh[i, f] = gg
                if all_estab < 0 and allheld:
                    all_estab = gg
                    for k in range(K): snap_estab[k] = glob[k]
                sep = False
                for i in range(I):
                    if not (selfc[maj[i]] and isl_cc[i] >= 0.5): continue
                    for j in range(i + 1, I):
                        if not (selfc[maj[j]] and isl_cc[j] >= 0.5): continue
                        a = maj[i]; b = maj[j]
                        if a != b and PCC[a, b] == 0.0 and U[a, b] < -0.5 and U[b, a] < -0.5:
                            sep = True; break
                    if sep: break
                if sep:
                    n_sep_chk += 1
                    if first_sep < 0:
                        first_sep = gg
                        for t in range(nt):
                            track_alive_at_sep[t] = glob[track[t]] > 0
                    for i in range(I):
                        if prevmaj[i] >= 0 and maj[i] != prevmaj[i]:
                            a = prevmaj[i]; b = maj[i]
                            if U[a, b] < -0.5 and U[b, a] < -0.5: n_flips += 1
                    sep_isl_chk += I
                elif was_sep:
                    n_res_events += 1
                was_sep = sep
                for i in range(I): prevmaj[i] = maj[i]
                for t in range(nt):
                    k = track[t]
                    if glob[k] == 0 and track_ext[t] < 0: track_ext[t] = gg
                    h = 0
                    for i in range(I):
                        if maj[i] == k and isl_cc[i] >= 0.9: h += 1
                    if h > track_maxisl[t]: track_maxisl[t] = h
                if e3_gen < 0:
                    npg = 0; only = -1
                    for k in range(K):
                        if glob[k] > 0:
                            npg += 1; only = k
                    if npg == 1 and not selfc[only]:
                        e3_gen = gg; e3_out = 0
                    else:
                        allres = True; allco = True
                        for i in range(I):
                            for t in range(npres[i]): res_ids[t] = pres[i, t]
                            st_ = closure(U, selfc, glob, K, res_ids, npres[i], inZ, queue)
                            if st_ < 0:
                                allres = False; break
                            if st_ == 0: allco = False
                        if allres:
                            e3_gen = gg; e3_out = 1 if allco else 0
                npg = 0
                for k in range(K):
                    if glob[k] > 0:
                        res_ids[npg] = k; npg += 1
                frozen = False
                if npg <= 400:
                    u0 = U[res_ids[0], res_ids[0]]
                    frozen = True
                    for x in range(npg):
                        for y in range(npg):
                            if abs(U[res_ids[x], res_ids[y]] - u0) > 1e-9:
                                frozen = False; break
                        if not frozen: break
                while nextck < nck and ck[nextck] == gg:
                    snap_sep[nextck] = sep
                    for i in range(I):
                        for k in range(K): snap[nextck, i, k] = counts[i, k]
                    nextck += 1
                if frozen:
                    frozen_gen = gg
                    while nextck < nck:
                        snap_sep[nextck] = sep
                        for i in range(I):
                            for k in range(K): snap[nextck, i, k] = counts[i, k]
                        nextck += 1
                    g_end = gg
                    break
        return (e3_gen, e3_out, estab, all_estab, snap_estab, first_sep, n_sep_chk, n_res_events, n_flips, sep_isl_chk,
                frozen_gen, g_end, track_ext, track_maxisl, track_alive_at_sep, snap, snap_sep, fam0, zg, fh)
    return run


# ------------------------------------------------------------------ cells
PART1 = ['L', 'P1', 'P2', 'P3', 'P4', "P4'", 'P5', 'P1p', 'P2n', 'P3p', 'P4p', 'P4n', 'P5p']
SCAN_A = ['scanA_%d' % i for i in range(8)]
SCAN_B = ['scanB_%d' % i for i in range(8)]
_S = {}


def _static():
    if 'po' not in _S:
        po = PO_.PO()
        _S['po'] = po
        _S['run'] = _kernel()
        _S['priors'] = {}
        track = {'XB': po.xb, 'CBP': po.cbp, 'CB': po.cb, 'EQ': po.eq, 'XC': po.xc}
        _S['track'] = track
    return _S['po']


def prior_of(cell):
    po = _static()
    base = cell.split('@')[0]
    p = _S['priors'].get(base)
    if p is None:
        p = po.class_prior(base)
        _S['priors'][base] = p
    return p


def parse_cell(cell):
    """'<prior cell>' or '<prior cell>@N,I'."""
    if '@' in cell:
        b, ni = cell.split('@')
        N, I = (int(x) for x in ni.split(','))
        return b, N, I
    return cell, 100, 64


def island_view(counts, PCC, N):
    I = counts.shape[0]
    cc = np.zeros(I); maj = np.zeros(I, np.int64)
    for i in range(I):
        c = counts[i].astype(float)
        nz = np.nonzero(c)[0]
        tot = c[nz] @ PCC[np.ix_(nz, nz)] @ c[nz] - (c[nz] * np.diag(PCC)[nz]).sum()
        cc[i] = tot / (N * (N - 1))
        # majority: largest count, ties to the smallest local index (as the kernel)
        best = -1; bc = -1
        for k in nz:
            if counts[i, k] > bc:
                bc = counts[i, k]; best = k
        maj[i] = best
    return cc, maj


def cross_pcc(counts, PCC, N, sel=None, pairs=None):
    """Mean over ordered island pairs (i != j) of x_i' PCC x_j (x = composition / N).  sel: class mask (restrict
    individuals); pairs: island mask (restrict to pairs of selected islands)."""
    cf = counts.astype(float)
    if sel is not None:
        cf = cf * sel[None, :]
    isl = np.arange(cf.shape[0]) if pairs is None else np.nonzero(pairs)[0]
    if len(isl) < 2:
        return None
    cf = cf[isl]
    g = cf.sum(0)
    tot = g @ PCC @ g - float(((cf @ PCC) * cf).sum())
    if sel is None:
        den = N * N * len(isl) * (len(isl) - 1)
    else:
        n = cf.sum(1)
        den = n.sum() ** 2 - (n ** 2).sum()
        if den <= 0:
            return None
    return float(tot / den)


def lottery_job(job):
    cell, rep, gens = job
    po = _static()
    st = po.st
    base, N, I = parse_cell(cell)
    pri = prior_of(base)
    rng = np.random.default_rng([N, I, rep, SALT])
    init_full = np.zeros((I, st.nc), np.int64)
    for i in range(I):
        init_full[i] = rng.multinomial(N, pri)
    present = np.nonzero(init_full.sum(0))[0]
    K = len(present)
    loc = {int(c): j for j, c in enumerate(present)}
    U = np.ascontiguousarray(st.U[np.ix_(present, present)])
    PCC = np.ascontiguousarray(st.PCC[np.ix_(present, present)])
    selfc = st.selfc[present].astype(np.bool_)
    famask = po.famask[present].astype(np.int64)
    init = np.ascontiguousarray(init_full[:, present])
    trk = _S['track']
    tr_names = [n for n in trk if trk[n] in loc]
    track = np.array([loc[trk[n]] for n in tr_names], np.int64) if tr_names else np.zeros(0, np.int64)
    t0 = time.time()
    res = _S['run'](U, PCC, init, N, 0.3, 1.0 / N, gens, 10, 7919 * rep + 13 * N + I, selfc, famask, NF, CK, track)
    (e3_gen, e3_out, estab, all_estab, snap_estab, first_sep, n_sep_chk, n_res, n_flips, sep_isl_chk, frozen_gen,
     g_end, track_ext, track_maxisl, track_alive_sep, snap, snap_sep, fam0, zg, fh) = res
    out = dict(cell=cell, rep=rep, N=N, I=I, K_present=K, gens=gens, g_end=int(g_end), time_s=time.time() - t0,
               E3=('success' if e3_out == 1 else 'fail') if e3_gen >= 0 else 'censored', E3_gen=int(e3_gen),
               establish_gen=int(estab), all_established_gen=int(all_estab), first_sep=int(first_sep),
               n_sep_checks=int(n_sep_chk), n_resolutions=int(n_res), n_flips=int(n_flips),
               sep_island_checks=int(sep_isl_chk), frozen_gen=int(frozen_gen))
    out.update(checkpoint_stats(po, present, snap, snap_sep, e3_gen, e3_out, N))
    # stages
    held_fam = out.pop('_held_fam')                       # (nck, I, NF)
    stages = {}
    for b, f in enumerate(PO_.FAMS):
        stages[f] = PO_.stage_stats(fam0[:, b], zg[:, b], fh[:, b], held_fam[:, :, b])
    out['stages'] = stages
    # logger consistency against the snapshots (notes §1.13 item 4)
    bits = ((famask[:, None] >> np.arange(NF)[None, :]) & 1).astype(np.int64)      # K x NF
    c0_ok = bool((init @ bits == fam0).all())
    fh_ok = True; zg_ok = True
    for t, T in enumerate(PO_.CKPTS):
        if T > g_end and frozen_gen < 0:
            continue
        Tq = min(T, g_end)
        hf = held_fam[t]
        if ((hf) & ((fh < 0) | (fh > Tq))).any(): fh_ok = False
        fc = snap[t] @ bits
        if ((fc == 0) & (fam0 > 0) & ((zg < 0) | (zg >= Tq))).any(): zg_ok = False
    out['consistency'] = dict(c0=c0_ok, first_hold=fh_ok, first_zero=zg_ok)
    out['track'] = {n: dict(seeded=int(init_full[:, trk[n]].sum()), ext=int(track_ext[j]), max_isl=int(track_maxisl[j]),
                            alive_at_first_sep=bool(track_alive_sep[j]) if first_sep >= 0 else None)
                    for j, n in enumerate(tr_names)}
    for n in trk:
        if n not in out['track']:
            out['track'][n] = dict(seeded=0)
    # pooling check (the identity run's): at 2,000 and 10,000
    lab = po.lab
    pc = {}
    for t, T in enumerate(PO_.CKPTS):
        if T not in (2000, 10000):
            continue
        o = out['ck'][str(T)]
        pc[str(T)] = R.pooling_check(st, init_full, present, snap_estab, {'all_established_gen': out['all_established_gen'],
                                     'h2000': dict(holders_g=o['holders_g'], outcome=o['outcome']),
                                     'end': dict(holders_g=o['holders_g'], outcome=o['outcome'])}, lab)
    out['pooling'] = {T: (dict(decided=v['h2000']['decided'], best_seed_won=v['h2000']['best_seed_won'],
                               best_est_won=v['h2000']['best_est_won'], n_sets=v['n_sets']) if v else None)
                      for T, v in pc.items()}
    out['seeded'] = {f: int(fam0[:, b].sum()) for b, f in enumerate(PO_.FAMS)}
    out['seeded_identity_classes'] = int(sum(1 for c in present if po.lab[c] == 'identity'))
    return out


def checkpoint_stats(po, present, snap, snap_sep, e3_gen, e3_out, N):
    st = po.st
    gl = present
    U = st.U[np.ix_(present, present)]; PCC = st.PCC[np.ix_(present, present)]
    selfc = st.selfc[present]
    mutCB = po.mut[po.cb][present]
    famask = po.famask[present]
    readers = po.readers[present]
    lab = po.lab
    inFP = (famask >> 0) & 1
    ck = {}
    nck = len(PO_.CKPTS)
    I = snap.shape[1]
    held_fam = np.zeros((nck, I, NF), bool)
    for t, T in enumerate(PO_.CKPTS):
        cnt = snap[t]
        cc, maj = island_view(cnt, PCC, N)
        held = np.array([bool(selfc[m_]) and cc[i] >= 0.5 for i, m_ in enumerate(maj)])
        for b in range(NF):
            held_fam[t, :, b] = held & (((famask[maj] >> b) & 1) == 1)
        hm = PCC[np.ix_(maj, maj)]
        cross_holders = float((hm.sum() - np.trace(hm)) / (I * (I - 1)))
        occ = float(np.mean([mutCB[m_] or gl[m_] == po.cb for m_ in maj]))
        if e3_out == 0 and 0 <= e3_gen <= T:
            oc = 'failed'
        elif any(not selfc[m_] for m_ in maj):
            oc = 'failed' if 0 <= e3_gen <= T else 'unresolved'
        elif held.all() and cross_holders >= 1.0 - 1e-12:
            oc = 'universal-open' if occ == 1.0 else 'universal-other'
        elif held.all():
            oc = 'patchwork'
        else:
            oc = 'unresolved'
        hfp = held_fam[t, :, 0]
        holders_g = sorted({int(gl[m_]) for m_ in maj})
        d = dict(outcome=oc, separated=bool(snap_sep[t]), n_held=int(held.sum()), cross_holders=cross_holders,
                 cross_pcc=cross_pcc(cnt, PCC, N), cross_readers=cross_pcc(cnt, PCC, N, sel=readers.astype(float)),
                 cross_FP_islands=cross_pcc(cnt, PCC, N, pairs=hfp), island_pcc=float(cc.mean()), occupancy=occ,
                 univ={f: bool(held_fam[t, :, b].all()) for b, f in enumerate(PO_.FAMS)},
                 held={f: int(held_fam[t, :, b].sum()) for b, f in enumerate(PO_.FAMS)},
                 held_XB=int(sum(1 for i, m_ in enumerate(maj) if held[i] and gl[m_] == po.xb)),
                 labels=dict(Counter(str(lab[gl[m_]]) if st.est[gl[m_]] else ('nonest:' + ('selfc' if st.selfc[gl[m_]] else 'D')) for m_ in maj)),
                 holders_g=holders_g[:64], holders=Counter(st.names[gl[m_]] for m_ in maj).most_common(5))
        ck[str(T)] = d
    return dict(ck=ck, _held_fam=held_fam)


def cmd_lottery(a):
    path = os.path.join(OUT, 'lottery_%s.json' % a.out)
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {(r['cell'], r['rep']) for r in rows}
    cells = []
    for c in a.cells:
        cells.append(c if (a.N, a.I) == (100, 64) else '%s@%d,%d' % (c, a.N, a.I))
    jobs = [(c, rep, a.gens) for c in cells for rep in range(a.runs) if (c, rep) not in done]
    nw = max(1, min(a.workers, 3))
    print('lottery jobs', len(jobs), 'workers', nw, flush=True)
    with Pool(nw) as pool:
        for k, r in enumerate(pool.imap_unordered(lottery_job, jobs, chunksize=1)):
            rows.append(r)
            if k % 10 == 9 or k == len(jobs) - 1:
                json.dump(rows, open(path, 'w'), default=str)
            c2 = r['ck']['2000']; c10 = r['ck']['10000']
            print('%s rep %d: 2000 %s cross %.3f | 10000 %s cross %.3f FPuniv %s | id isl %d | %s (%.0fs, K=%d, end %d)' % (
                r['cell'], r['rep'], c2['outcome'], c2['cross_pcc'], c10['outcome'], c10['cross_pcc'], c10['univ']['FP'],
                c10['held']['identity'], c10['holders'][:2], r['time_s'], r['K_present'], r['g_end']), flush=True)
    json.dump(rows, open(path, 'w'), default=str)


# ------------------------------------------------------------------ static
def cmd_static(a):
    po = _static()
    st = po.st
    A = po.A
    out = dict(M=po.M, m_L=po.m_L, n_cliques=len(po.cliques), n_cliques_with_CBP=int(sum(1 for c in po.cliques if po.cbp in c)))
    nm = {'CBP': po.cbp, 'CB': po.cb, 'Cc': po.cc, 'D': st.iD, 'EQ': po.eq, 'XC': po.xc, 'XB': po.xb}
    out['hand_table'] = {r: ''.join('C' if A[nm[r], nm[c]] == 1 else 'D' for c in ['Cc', 'D', 'CB', 'EQ', 'XC', 'CBP'])
                         for r in ['Cc', 'D', 'CB', 'EQ', 'XC', 'CBP']}
    mu = po.muL
    out['CBP'] = dict(cls=po.cbp, name=st.names[po.cbp], n_spell=int(st.n_spell[po.cbp]), mass=float(mu[po.cbp]),
                      n_inv=po.ninv(po.cbp), spellings=[st.cat.name(int(k)) for k in np.nonzero(st.cos == po.cbp)[0]])
    sg = np.array([IT.s_guarded(st.cat.dt_list[int(st.cat.sp_dt[int(st.crep[c])])]) for c in range(po.nc)])
    ninv = np.array([po.ninv(c) for c in range(po.nc)])

    def fam(c):
        c = np.asarray(c, np.int64)
        return dict(n=int(len(c)), n_spell=int(st.n_spell[c].sum()), mass=float(mu[c].sum()),
                    labels=dict(Counter(str(po.lab[x]) for x in c)), n_sguarded=int(sg[c].sum()),
                    mass_sguarded=float(mu[c[sg[c]]].sum()), n_exploited=int((ninv[c] > 0).sum()),
                    mass_exploited=float(mu[c[ninv[c] > 0]].sum()),
                    heaviest=[(st.names[x], float(mu[x])) for x in sorted(c, key=lambda x: -mu[x])[:8]])
    out['FP'] = fam(po.FP); out['core'] = fam(po.core); out['nice'] = fam(po.nice); out['FX'] = fam(po.FX)
    out['CB_in_FP'] = bool(po.cb in po.FP)
    ms = sorted([float(mu[c].sum()) for c in po.cliques if po.cbp in c], reverse=True)
    out['FP_runner_up'] = ms[1] if len(ms) > 1 else None
    FCB = st.F_CB()
    op_pr = np.nonzero((po.lab == 'open') & (A[:, po.cc] == 0))[0]
    sg_pr = np.nonzero(st.est & sg & (A[:, po.cc] == 0))[0]
    out['overlaps'] = {k: dict(n=int(len(S)), mass=float(mu[S].sum()), n_in_FP=int(len(set(S) & set(po.FP.tolist()))),
                               mass_in_FP=float(mu[sorted(set(S) & set(po.FP.tolist()))].sum()))
                       for k, S in [('F_CB', np.array(FCB)), ('N(CB)+', po.NCB), ('P_open(open & refuse Cc)', op_pr),
                                    ('P_open(S-guarded est. refusing Cc)', sg_pr), ('F_X', po.FX)]}
    out['P_open_sguarded_labels'] = dict(Counter(str(po.lab[x]) for x in sg_pr))
    comps = st.families()['comps']
    cc_ = [c for c in comps if po.cbp in c][0]
    out['component_CBP'] = dict(n=len(cc_), mass=float(mu[cc_].sum()), contains_XC=bool(po.xc in cc_), contains_EQ=bool(po.eq in cc_))
    out['exclusive_label_equals_FX'] = bool(set(np.nonzero(po.lab == 'exclusive')[0].tolist()) == set(po.FX.tolist()))
    p = po.paths()
    out['paths'] = dict(n_direct=p['n_direct'], direct_FX_members=[st.names[x] for x in p['direct_FX_members']],
                        n_mid=p['n_mid'], mass_mid=p['mass_mid'], n_len3_pairs=p['n_len3_pairs'],
                        cbp_xc_bridges=[(st.names[x], float(mu[x]), int(ninv[x])) for x in p['cbp_xc_bridges']])
    out['XB'] = dict(name=st.names[po.xb], mass=float(mu[po.xb]), n_inv=int(ninv[po.xb]), in_FX=bool(po.xb in po.FX),
                     mutual_with=[n for n, k in st.named.items() if po.mut[po.xb, k]] + (['CBP'] if po.mut[po.xb, po.cbp] else []),
                     n_FP_nbrs=int(po.mut[po.xb, po.FP].sum()), n_core_nbrs=int(po.mut[po.xb, po.core].sum()))
    out['allc'] = dict(n=int(len(po.allc)), mass=float(mu[po.allc].sum()),
                       CB_coop_mass=float(mu[po.allc[A[po.cb, po.allc] == 1]].sum()),
                       CBP_coop=[(st.names[x], float(mu[x])) for x in po.allc if A[po.cbp, x] == 1])
    out['readers'] = dict(n=int(po.readers.sum()), mass=float(mu[po.readers].sum()))
    # cells: masses, copies, seed payoffs
    cells = {}
    for c in PART1 + SCAN_A + SCAN_B:
        pr = po.class_prior(c)
        f = po.seed_payoff(pr)
        bm = po.block_masses(pr)
        wf = lambda S: float((pr[S] * f[S]).sum() / max(pr[S].sum(), 1e-300)) if pr[S].sum() > 0 else None
        cells[c] = dict(masses=bm, copies={k: 6400 * v for k, v in bm.items()},
                        f=dict(CBP=float(f[po.cbp]), CB=float(f[po.cb]), EQ=float(f[po.eq]), XC=float(f[po.xc]), D=float(f[st.iD]),
                               FP=wf(po.FP), core=wf(po.core), nice=wf(po.nice), CBset=wf(po.CBset), identity=wf(po.ident)))
    out['cells'] = cells
    json.dump(out, open(os.path.join(OUT, 'static.json'), 'w'), indent=1, default=str)
    print(json.dumps({k: out[k] for k in ('M', 'm_L', 'hand_table', 'CBP', 'CB_in_FP', 'paths', 'XB')}, indent=1, default=str))
    for c in PART1:
        print(c, {k: round(v, 5) for k, v in cells[c]['masses'].items()}, {k: (round(v, 3) if v is not None else None) for k, v in cells[c]['f'].items()})


# ------------------------------------------------------------------ validation (notes §1.13)
def cmd_validate(a):
    import lt_code as L
    import lt_cert as Cc
    po = _static()
    st = po.st
    cat = st.cat
    out = {}
    # 1. hand table by whole plays and against the class table
    names = {'Cc': ('C',), 'D': ('D',), 'CB': IT.CB_X, 'EQ': IT.EQ_X, 'XC': IT.XC_X, 'CBP': PO_.CBP_X}
    hand = {'Cc': 'CCCCCC', 'D': 'DDDDDD', 'CB': 'CDCDDC', 'EQ': 'DDDCDD', 'XC': 'DDDDCD', 'CBP': 'DDCDDC'}
    order = ['Cc', 'D', 'CB', 'EQ', 'XC', 'CBP']
    terms = {n: cat.term(cat.spelling_of(x, 0)) for n, x in names.items()}
    plays = {}
    for r in order:
        s = ''
        for c in order:
            L.CACHE.clear()
            s += L.play(terms[r], terms[c], cat.K)[0]
        plays[r] = s
    tab = {r: ''.join('C' if st.A[st.class_of(names[r], 0), st.class_of(names[c], 0)] == 1 else 'D' for c in order) for r in order}
    out['hand_table'] = dict(hand=hand, plays=plays, table=tab, ok=bool(plays == hand == tab))
    print('hand table ok', out['hand_table']['ok'], flush=True)
    chk = R.CP.Checker('ideal', cat.V, cat.K)
    vals = {}
    for desc, t, m, aa in [('chk_D(CB,qC)', terms['CB'], L.PROG_C, 'D'), ('chk_D(CBP,qCB)', terms['CBP'], cat.cb_term, 'D'),
                           ('chk_C(XC,CBP)', terms['XC'], terms['CBP'], 'C'), ('chk_C(CBP,CB)', terms['CBP'], terms['CB'], 'C'),
                           ('chk_C(CB,CBP)', terms['CB'], terms['CBP'], 'C'), ('chk_D(Cc,qC)', terms['Cc'], L.PROG_C, 'D'),
                           ('chk_D(CBP,qC)', terms['CBP'], L.PROG_C, 'D')]:
        vals[desc] = chk(0, t, m, aa)[0]
    out['checks'] = vals
    print(vals, flush=True)
    # 2. families
    out['families'] = dict(FP=len(po.FP), FP_mass=float(po.muL[po.FP].sum()), core=len(po.core), core_mass=float(po.muL[po.core].sum()),
                           nice=len(po.nice), FX=len(po.FX), XB_in_FX=bool(po.xb in po.FX), CB_in_FP=bool(po.cb in po.FP),
                           ident_FP_disjoint=bool(not (set(po.ident.tolist()) & set(po.FP.tolist()))))
    print(out['families'], flush=True)
    # 3. seed laws
    laws = {}
    M = po.M
    targets = {'P1': [('FP', M)], 'P2': [('CBset', M)], 'P3': [('FP', M), ('identity', 0.0)], 'P4': [('FP', M)],
               "P4'": [('CBset', M)], 'P5': [('FP', M / 2), ('EQten', M / 2)], 'P1p': [('core', M), ('nice', 0.0)],
               'P2n': [('nice', M), ('core', 0.0)], 'P3p': [('core', M), ('nice', 0.0), ('identity', 0.0)],
               'P4p': [('core', M), ('nice', 0.0)], 'P4n': [('nice', M), ('core', 0.0)], 'P5p': [('core', M / 2), ('EQten', M / 2), ('nice', 0.0)]}
    rng = np.random.default_rng(5)
    for c, tg in targets.items():
        pr = po.class_prior(c)
        bm = po.block_masses(pr)
        err = max(abs(bm[g] - v) for g, v in tg)
        if c in ('P4', "P4'", 'P4p', 'P4n'):
            err = max(err, bm['allc'])
        # the rest proportional to L
        blk = np.zeros(po.nc, bool)
        for g, v in tg:
            blk[po.groups[g]] = True
        if c in ('P2', "P4'"):
            blk[po.NCB] = True
        if c in ('P4', "P4'", 'P4p', 'P4n'):
            blk[po.allc] = True
        if c in ('P5', 'P5p'):
            blk[po.EQten] = True
        rest = ~blk & (pr > 0)
        ratio = pr[rest] / po.muL[rest]
        draws = rng.multinomial(200000, pr)
        emp = {g: float(draws[po.groups[g]].sum() / 200000) for g, _ in tg}
        laws[c] = dict(err=float(err), rest_ratio_spread=float(ratio.max() / ratio.min() - 1) if rest.any() else 0.0, empirical=emp,
                       target={g: v for g, v in tg})
    # P2 = T1c, scan points
    laws['P2_eq_T1c'] = float(np.abs(st.mass(po.cell_weights('P2')) - st.class_prior('T1c')).max())
    laws['scanA_6_eq_L'] = float(np.abs(st.mass(po.cell_weights('scanA_6')) - st.class_prior('L')).max())
    laws['scanA_0_eq_noclique'] = float(np.abs(st.mass(po.cell_weights('scanA_0')) - st.class_prior('noclique')).max())
    scan = {}
    for c in SCAN_A + SCAN_B:
        pr = po.class_prior(c)
        i = int(c.split('_')[1])
        m = PO_.SCAN_M[i] if PO_.SCAN_M[i] is not None else po.m_L
        scan[c] = dict(m=m, ident=float(pr[po.ident].sum()), FP=float(pr[po.FP].sum()))
    laws['scan'] = scan
    out['laws'] = laws
    print(json.dumps({k: v for k, v in laws.items() if k != 'scan'}, indent=0, default=str)[:3000], flush=True)
    # 5. reproduction of the identity run (L and T1c = P2 at 2,000 and at its end for continued runs; no-clique at 2,000)
    ref = json.load(open(os.path.join(R.OUT, 'lottery_main.json')))
    refd = {(r['cell'], r['rep']): r for r in ref}
    jobs = [(c, rep, 10000) for c in ('L', 'P2', 'scanA_0') for rep in range(a.reps)]
    mine = {}
    with Pool(max(1, min(a.workers, 3))) as pool:
        for r in pool.imap_unordered(lottery_job, jobs, chunksize=1):
            mine[(r['cell'], r['rep'])] = r
    rep_out = []
    for (c, rep), r in sorted(mine.items()):
        rc = {'L': 'L', 'P2': 'T1c', 'scanA_0': 'X_noclique'}[c]
        q = refd.get((rc, rep))
        if q is None: continue
        a2 = (r['ck']['2000']['outcome'], round(r['ck']['2000']['cross_pcc'], 9))
        b2 = (q['h2000']['outcome'], round(q['h2000']['cross_pcc'], 9))
        e = None
        if q['end']['gen'] == 10000:
            e = (r['ck']['10000']['outcome'] == q['end']['outcome'] and abs(r['ck']['10000']['cross_pcc'] - q['end']['cross_pcc']) < 1e-9)
        rep_out.append(dict(cell=c, rep=rep, at2000=bool(a2 == b2), mine=a2, ref=b2, at10000=e))
    out['reproduction'] = dict(n=len(rep_out), n_ok_2000=sum(x['at2000'] for x in rep_out),
                               n_end_checked=sum(1 for x in rep_out if x['at10000'] is not None),
                               n_end_ok=sum(1 for x in rep_out if x['at10000']), rows=rep_out)
    print('reproduction', {k: v for k, v in out['reproduction'].items() if k != 'rows'}, flush=True)
    # 4. stage logger on a real run against a recount from its snapshots
    r = mine[('L', 0)]
    ok = True
    for f in PO_.FAMS:
        s = r['stages'][f]
        for T in PO_.CKPTS:
            if s[T]['held'] != r['ck'][str(T)]['held'][f]: ok = False
    out['stage_vs_snapshot'] = ok
    # 6. crossing on constructed curves
    ms = [0, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3, 9e-3, 2e-2]
    f = [0.8, 0.75, 0.7, 0.6, 0.4, 0.2, 0.1, 0.0]
    mstar, fl = PO_.crossing(ms, f)
    exp = math.exp(math.log(1e-3) + (0.1 / 0.2) * (math.log(2e-3) - math.log(1e-3)))
    out['crossing_test'] = dict(mstar=mstar, expected=exp, ok=bool(abs(mstar - exp) < 1e-12 and fl == 'ok'))
    json.dump(out, open(os.path.join(OUT, 'validate.json'), 'w'), indent=1, default=str)
    print('stage_vs_snapshot', ok, 'crossing', out['crossing_test'], flush=True)


# ------------------------------------------------------------------ chain (Part 3, diagnostic)
def chain_cell(job):
    """The identity run's chain_cell on the support top-1,500 ∪ identity ∪ F_P, closed components removed (notes §1.12)."""
    from chain_log import LogChain, NEG
    from dollar_partitions import ClassProvider
    import carrier_populations_run as CPR
    from carrier_populations_report import leak_test
    N, log_theta, twins = job
    t0 = time.time()
    po = _static()
    st = po.st
    A = st.A.copy()
    mu0 = st.class_prior('L')
    lab0 = po.lab
    keep = np.array(sorted(set(np.argsort(-mu0)[:1500].tolist()) | set(po.ident.tolist()) | set(po.FP.tolist())))
    dropped = []
    while True:
        lt = leak_test(A[np.ix_(keep, keep)])
        cl = sorted({int(keep[i]) for c in lt['closed'] for i in c})
        if not cl: break
        dropped += cl
        ks = set(cl)
        keep = np.array([k for k in keep if k not in ks])
    Ak = A[np.ix_(keep, keep)]; mu = mu0[keep]; mu = mu / mu.sum(); names = [st.names[k] for k in keep]; lab = lab0[keep]
    U, PCC = R.CP.pay_matrix(Ak)
    nc = len(mu)
    iD = int(np.nonzero(keep == st.iD)[0][0])
    grp = {'core': set(po.core.tolist()), 'nice': set(po.nice.tolist()), 'FX': set(po.FX.tolist()), 'XB': {po.xb}, 'CBP': {po.cbp}}
    CH = CPR.fast_chain_class()
    ch = CH(ClassProvider(U, mu), N=N, w=0.3, Ufull=U if twins else None, twins=twins, theta=1.0, max_states=10 ** 9)
    ch.explore_log(extra_states=[], log_theta=log_theta, max_states=int(os.environ.get('PO_MAX_STATES', 4000)), verbose=False)
    keys_all, lpi_all, sinfo, out_un, rec = ch.solve_sparse()
    keys = [keys_all[i] for i in rec]
    pi = np.exp(lpi_all[rec])
    LA, _ = ch.log_matrix(keys)
    pcc = 0.0; piD = 0.0; coop = np.zeros(len(keys))
    for i, k in enumerate(keys):
        ids, x, kind = ch.states[k]; ids = list(ids); x = np.asarray(x)
        c = float(x @ PCC[np.ix_(ids, ids)] @ x); coop[i] = c; pcc += pi[i] * c
        if kind == 'mono' and ids[0] == iD: piD += pi[i]
    tot_flow = 0.0
    for i in range(len(keys)):
        row = LA[i].copy(); row[i] = NEG
        f = row[np.isfinite(row)]
        if len(f): tot_flow += pi[i] * float(np.exp(np.logaddexp.reduce(f)))
    cut = float(sum(float(np.exp(np.logaddexp.reduce([lpi_all[i] + lw for i, lw in lst]))) for k2, lst in out_un.items()))

    def desc(k):
        ids, x, kind = ch.states[k]
        return ' + '.join('%s:%.3f' % (names[i], xi) for i, xi in zip(ids, x))
    outside = np.setdiff1d(np.arange(st.nc), keep)
    order = np.argsort(-pi)
    support = []
    for i in order[:12]:
        if pi[i] < 1e-4: break
        k = keys[i]
        row = LA[i].copy(); row[i] = NEG
        fin = np.isfinite(row)
        lex = float(np.logaddexp.reduce(row[fin])) if fin.any() else NEG
        ex = []
        for j in np.argsort(-np.where(fin, row, -np.inf))[:3]:
            if not fin[j]: break
            muts = sorted(ch.lmut.get((k, keys[j]), {}).items(), key=lambda kv: -kv[1])[:2]
            ex.append(dict(to=desc(keys[j]), log10_rate=float(row[j] / math.log(10)), mutants=[(names[q], float(v / math.log(10))) for q, v in muts]))
        ids = list(ch.states[k][0]); x = np.asarray(ch.states[k][1])
        # closure check: classes outside the support invading this state neutrally or better
        gid = keep[ids]
        uxx = float(x @ st.U[np.ix_(gid, gid)] @ x)
        inv = outside[(st.U[np.ix_(outside, gid)] @ x) >= uxx - 1e-9]
        support.append(dict(state=desc(k), pi=float(pi[i]), coop=float(coop[i]), labels=[str(lab[q]) for q in ids],
                            groups=[[g for g, s in grp.items() if int(keep[q]) in s] for q in ids],
                            log10_exit=lex / math.log(10) if np.isfinite(lex) else None, exits=ex,
                            omitted_invaders=dict(n=int(len(inv)), mass_L=float(mu0[inv].sum()),
                                                  heaviest=[(st.names[q], float(mu0[q])) for q in sorted(inv, key=lambda q: -mu0[q])[:4]])))
    top = None
    ci = [i for i in order if coop[i] >= 0.95]
    if ci:
        i = ci[0]; k = keys[i]
        ids = list(ch.states[k][0])
        top = dict(state=desc(k), pi=float(pi[i]), groups=[[g for g, s in grp.items() if int(keep[q]) in s] for q in ids],
                   labels=[str(lab[q]) for q in ids])
    pi_lab = defaultdict(float); pi_grp = defaultdict(float)
    for i, k in enumerate(keys):
        ids, x, kind = ch.states[k]
        for q, xi in zip(ids, x):
            pi_lab[str(lab[q])] += pi[i] * xi
            for g, s in grp.items():
                if int(keep[q]) in s: pi_grp[g] += pi[i] * xi
    return dict(N=N, twins=bool(twins), log10_theta=log_theta / math.log(10), n_classes=nc, n_dropped=len(dropped),
                n_FP_in_support=int(len(set(keep.tolist()) & set(po.FP.tolist()))),
                n_expanded=len(keys_all), n_recurrent=len(keys), pcc=pcc, pi_D=piD, pi_coop=float(pi[coop >= 0.95].sum()),
                pi_by_label=dict(pi_lab), pi_by_group=dict(pi_grp), cut_rel=cut / tot_flow if tot_flow > 0 else None,
                support=support, top_coop=top, time_s=time.time() - t0)


def cmd_chain(a):
    path = os.path.join(OUT, 'chain.json')
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {(r['N'], r['twins']) for r in rows}
    jobs = [(N, math.log(a.theta), bool(tw)) for tw in a.twins for N in a.N if (N, bool(tw)) not in done]
    with Pool(max(1, min(a.workers, 3, len(jobs)))) as pool:
        for r in pool.imap_unordered(chain_cell, jobs, chunksize=1):
            rows.append(r)
            json.dump(rows, open(path, 'w'), indent=1, default=str)
            print('N=%d twins=%s: P(C,C) %.4f pi(D) %.4f top %s groups %s (%.0fs)' % (r['N'], r['twins'], r['pcc'], r['pi_D'],
                  r['support'][0]['state'] if r['support'] else None, dict(r['pi_by_group']), r['time_s']), flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('static')
    s = sub.add_parser('validate'); s.add_argument('--workers', type=int, default=3); s.add_argument('--reps', type=int, default=40)
    s = sub.add_parser('lottery')
    s.add_argument('--cells', nargs='+', default=['L']); s.add_argument('--runs', type=int, default=40)
    s.add_argument('--gens', type=int, default=10000); s.add_argument('--N', type=int, default=100); s.add_argument('--I', type=int, default=64)
    s.add_argument('--out', default='main'); s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('chain')
    s.add_argument('--N', type=int, nargs='+', default=[1000, 10000]); s.add_argument('--theta', type=float, default=1e-8)
    s.add_argument('--twins', type=int, nargs='+', default=[1]); s.add_argument('--workers', type=int, default=3)
    a = ap.parse_args()
    {'static': cmd_static, 'validate': cmd_validate, 'lottery': cmd_lottery, 'chain': cmd_chain}[a.cmd](a)
