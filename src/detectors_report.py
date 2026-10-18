"""Report for legitimate detectors: Part A tables, B/C removals with cause labels, sucker exposure, grudges, verdict
inputs.  python3 src/detectors_report.py  -> runs/detectors.md (tables) and runs/detectors.json (summary)."""
import gzip
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'detectors')
I_CC, I_LAB, I_DET, I_PBN, I_SUCK, I_EXM, I_EXT, I_EDGE, I_EDGE2, I_MARK, I_GLEN, I_NT, I_MAJ = range(13)
LABN = {0: 'unheld', 1: 'DET', 2: 'PBN', 3: 'open', 4: 'ident', 5: 'other'}


def cp(k, n, a=0.05):
    from scipy.stats import beta
    lo = beta.ppf(a / 2, k, n - k + 1) if k > 0 else 0.0
    hi = beta.ppf(1 - a / 2, k + 1, n - k) if k < n else 1.0
    return float(lo), float(hi)


def load(name):
    p = os.path.join(OUT, name)
    return json.load(gzip.open(p)) if os.path.exists(p) else []


# ------------------------------------------------------------------------------------------------ Part A
def part_a(rows):
    out = {}
    for r in rows:
        if r['variant'] != 'first': continue
        k = (r['N'], r['arm'], r['pred'])
        out.setdefault(k, []).append(r['first'] == 'established')
    pooled = {}
    for (N, arm, pred), v in out.items():
        pooled.setdefault((N, arm), []).extend(v)
    tab = {}
    for (N, arm), v in sorted(pooled.items()):
        k, n = int(sum(v)), len(v)
        tab['%d_%s' % (N, arm)] = dict(N=N, arm=arm, est=k, n=n, p=k / n, ci=cp(k, n))
    per = {'%d_%s_%s' % k: dict(est=int(sum(v)), n=len(v)) for k, v in sorted(out.items())}
    sec = {}
    for r in rows:
        if r['variant'] == 'first': continue
        k = '%s_%s' % (r['arm'], r['variant'])
        d = sec.setdefault(k, dict(first_lost=0, first_est=0, second_est=0, second_n=0))
        if r['first'] == 'lost':
            d['first_lost'] += 1
            d['second_n'] += 1
            d['second_est'] += int(r['second'] == 'established')
        elif r['first'] == 'established':
            d['first_est'] += 1
    for k, d in sec.items():
        d['p_second'] = d['second_est'] / max(1, d['second_n'])
        d['ci'] = cp(d['second_est'], d['second_n']) if d['second_n'] else None
    # grudges written, marked fraction, live encounters
    gst = {}
    for r in rows:
        if r['variant'] != 'first': continue
        k = '%d_%s' % (r['N'], r['arm'])
        d = gst.setdefault(k, dict(writes=[], marked=[], live=[], t=[]))
        d['writes'].append(r['writes_first']); d['marked'].append(r['marked_after_first'])
        d['live'].append(r['live_first']); d['t'].append(r['first_t'])
    gsum = {k: dict(writes=float(np.mean(d['writes'])), marked=float(np.mean(d['marked'])),
                    live=float(np.mean(d['live'])), t=float(np.mean(d['t']))) for k, d in gst.items()}
    return dict(pooled=tab, per_pred=per, second=sec, grudges=gsum)


# ------------------------------------------------------------------------------------------------ removals
def series(r):
    """Population-level series per checkpoint: g, det, pbn share, mean cc, max exploiter share, edge, edge_noTP,
    sucker share."""
    out = []
    for g, isl in r['recs']:
        a = np.array(isl, float)
        e = a[:, I_EDGE]; e2 = a[:, I_EDGE2]
        w = ~np.isnan(e)
        out.append([g, a[:, I_DET].mean(), a[:, I_PBN].mean(), a[:, I_CC].mean(), a[:, I_EXM].max(),
                    float(e[w].mean()) if w.any() else np.nan, float(e2[w].mean()) if w.any() else np.nan,
                    a[:, I_SUCK].mean()])
    return np.array(out)


def label_window(S, t0i, t1i, loser):
    """Labels for a removal of `loser` ('DET' or 'PBN') over checkpoints t0i..t1i (indices into S)."""
    W = S[t0i:t1i + 1]
    labs = []
    if W[0, 3] < 0.95: labs.append('inefficiency')
    if np.nanmax(W[:, 4]) >= 0.3: labs.append('predation')
    sgn = 1.0 if loser == 'DET' else -1.0          # edge = f_PBN - f_DET
    e = sgn * W[:, 5]; e2 = sgn * W[:, 6]
    if np.isfinite(e).any():
        me, me2 = np.nanmean(e), np.nanmean(e2)
        if me > 0 and (me - me2) > 0 and me2 <= 0: labs.append('prudence premium')
    win_share = W[0, 2] if loser == 'DET' else W[0, 1]
    los_share = W[0, 1] if loser == 'DET' else W[0, 2]
    if not labs and win_share > los_share: labs.append('abundance')
    if not labs: labs.append('unresolved')
    return labs


PREC = ['inefficiency', 'predation', 'prudence premium', 'abundance', 'unresolved']


def removals(r):
    """Network removals (extinction of DET or PBN spellings) with labels; winner."""
    S = series(r)
    out = {}
    gs = S[:, 0]
    for net, col in (('DET', 1), ('PBN', 2)):
        x = S[:, col]
        if x[0] <= 0 or x[-1] > 0:
            out[net] = None
            continue
        zero = np.nonzero(x > 0)[0]
        tb = int(zero[-1] + 1)                       # first checkpoint of the final zero run
        t0 = int(np.searchsorted(gs, gs[tb] - 500))
        labs = label_window(S, t0, tb, net)
        head = [l for l in PREC if l in labs][0]
        out[net] = dict(g=float(gs[tb]), labels=labs, head=head,
                        sucker_share_window=float(np.nanmean(S[t0:tb + 1, 7])))
    det_rm, pbn_rm = out['DET'], out['PBN']
    if S[0, 1] <= 0 and not pbn_rm: winner = 'DET gone by 10'     # never seeded or extinct before the first checkpoint
    elif S[0, 2] <= 0 and not det_rm: winner = 'PBN gone by 10'
    elif det_rm and not pbn_rm: winner = 'PBN'
    elif pbn_rm and not det_rm: winner = 'DET'
    elif det_rm and pbn_rm: winner = 'both removed'
    else: winner = 'coexistence'
    return dict(removals=out, winner=winner, det_final=float(S[-1, 1]), pbn_final=float(S[-1, 2]),
                det_peak=float(S[:, 1].max()), pbn_peak=float(S[:, 2].max()), det_at_200=float(S[gs <= 200][-1, 1]),
                pbn_at_200=float(S[gs <= 200][-1, 2]), det_0=float(S[0, 1]), pbn_0=float(S[0, 2]),
                pcc_final=float(S[-1, 3]))


def island_events(r):
    """Island-level holder changes away from DET or PBN (I > 1 phases): (from, to, labels)."""
    recs = r['recs']
    ev = []
    if not recs: return ev
    nI = len(recs[0][1])
    gs = [g for g, isl in recs]
    for i in range(nI):
        lab = [int(isl[i][I_LAB]) if i < len(isl) else -1 for g, isl in recs]
        for t in range(1, len(recs)):
            if len(recs[t][1]) != nI: break
            prev, cur = lab[t - 1], lab[t]
            if prev in (1, 2) and cur != prev:
                # stays out for >= 25 generations
                ok = True
                for t2 in range(t, len(recs)):
                    if len(recs[t2][1]) != nI: break
                    if gs[t2] - gs[t] >= 25: break
                    if lab[t2] == prev: ok = False; break
                if not ok: continue
                w0 = recs[t - 1][1][i]; w1 = recs[t][1][i]
                labs = []
                if w0[I_CC] < 0.95: labs.append('inefficiency')
                if max(w0[I_EXM], w1[I_EXM]) >= 0.3: labs.append('predation')
                e = w0[I_EDGE]; e2 = w0[I_EDGE2]
                if e is not None and np.isfinite(e):
                    sg = 1 if prev == 1 else -1
                    if sg * e > 0 and sg * (e - e2) > 0 and sg * e2 <= 0: labs.append('prudence premium')
                if not labs: labs.append('abundance' if cur in (1, 2, 3) else 'unresolved')
                ev.append(dict(island=i, g=gs[t], frm=LABN[prev], to=LABN.get(cur, '?'), labels=labs,
                               head=[l for l in PREC if l in labs][0]))
    return ev


def cell_summary(rows):
    out = {}
    for r in rows:
        c = r['cell']
        d = out.setdefault(c, dict(n=0, winners={}, rem={}, det_final=[], pbn_final=[], uo=0, writes=[], boot=[],
                                   evict=[], adopt=[], sucker_enc=[], sucker_isl=[], arrivals=[], arr_cls={},
                                   isl_ev={}, det_extinct=0, glen=[], pcc=[], write_pairs={}, det_200=[], time=[]))
        rm = removals(r)
        d['n'] += 1
        d['winners'][rm['winner']] = d['winners'].get(rm['winner'], 0) + 1
        for net, x in rm['removals'].items():
            if x:
                key = '%s:%s' % (net, x['head'])
                d['rem'][key] = d['rem'].get(key, 0) + 1
                if net == 'DET': d['det_extinct'] += 1
        d['det_final'].append(rm['det_final']); d['pbn_final'].append(rm['pbn_final']); d['det_200'].append(rm['det_at_200'])
        d['uo'] += int(r.get('uo', False))
        g = r['gctr']
        d['writes'].append(g['write']); d['boot'].append(g['boot']); d['evict'].append(g['evict']); d['adopt'].append(g['adopt'])
        d['sucker_enc'].append(g['sucker_enc']); d['sucker_isl'].append(r['isl_sucker_gen'][0])
        d['arrivals'].append(r['arrivals'])
        for k, v in r['arrivals_cls'].items(): d['arr_cls'][k] = d['arr_cls'].get(k, 0) + v
        for e in island_events(r):
            key = '%s>%s:%s' % (e['frm'], e['to'], e['head'])
            d['isl_ev'][key] = d['isl_ev'].get(key, 0) + 1
        fin = np.array(r['final'], float)
        d['glen'].append(float(np.nanmean(fin[:, I_GLEN]))); d['pcc'].append(float(fin[:, I_CC].mean()))
        for k, v in r['write_pairs'].items(): d['write_pairs'][k] = d['write_pairs'].get(k, 0) + v
        d['time'].append(r['time_s'])
    summ = {}
    for c, d in out.items():
        summ[c] = dict(n=d['n'], winners=d['winners'], removals=d['rem'], det_extinct=d['det_extinct'],
                       det_final_median=float(np.median(d['det_final'])), pbn_final_median=float(np.median(d['pbn_final'])),
                       det_at_200_median=float(np.median(d['det_200'])), uo=d['uo'],
                       writes_mean=float(np.mean(d['writes'])), boot_share=float(np.sum(d['boot']) / max(1, np.sum(d['writes']))),
                       evict_mean=float(np.mean(d['evict'])), adopt_mean=float(np.mean(d['adopt'])),
                       sucker_enc_mean=float(np.mean(d['sucker_enc'])), sucker_isl_gen_mean=float(np.mean(d['sucker_isl'])),
                       arrivals_mean=float(np.mean(d['arrivals'])), arrivals_cls=d['arr_cls'], island_events=d['isl_ev'],
                       glen_final_mean=float(np.nanmean(d['glen'])) if d['glen'] else None,
                       pcc_final_mean=float(np.mean(d['pcc'])), write_pairs=d['write_pairs'],
                       time_mean=float(np.mean(d['time'])))
    return summ


def replay_job(job):
    """Matched counterfactual replay (notes §1.5, §2.5 item 8): rerun (cell, rep) with the same seeds to g0, apply the
    surgery, continue to g1; returns the network shares at g1 for the replay and the original."""
    sys.path.insert(0, os.path.join(ROOT, 'src'))
    import detectors as DTm
    import detectors_run as DR
    import provenance as PV
    import pangaea as PG
    import annealed as AN
    import provenance_run as PR
    import realizable_scaling as RS
    import time
    cell, rep, g0, g1, kind = job
    t0 = time.time()
    geom, arm, Ksch, w = DR.cell_spec(cell)
    Wd = DTm.world(w)
    LS = Wd['LS']
    if geom == 'Cis':
        N, I = 200, 64
        rng = np.random.default_rng([N, I, rep, PR.SALT])
        sp = rng.choice(len(LS['mu']), size=(I, N), p=LS['mu'])
        rule = np.full((I, N), PV.R_SNON, np.int64); unit = LS['Eu'][LS['tau'][sp]]
        seed = PR.kernel_seed(N, I, rep); mN = RS.mN_cal(N)
        epsg = AN.schedule('ann', N, Ksch) if Ksch else None
        merge_at = 0
    else:
        N, I = 100, 128
        sp = DR.fission_founders('L' if geom in ('Cff', 'Ref') else geom, rep, Wd)
        rule = np.full((I, N), PV.R_SNON, np.int64); unit = LS['Eu'][LS['tau'][sp]]
        if geom == 'Ref':
            import removing_rivals as RR
            kPB = Wd['names'].index(RR.PB_SP)
            pos = RR.donor_positions(N, I, rep)
            for i in range(I):
                sp[i, pos[i]] = kPB; rule[i, pos[i]] = PV.R_H; unit[i, pos[i]] = Wd['Hu'][Wd['tau'][kPB]]
        seed = PG.kernel_seed_pg(N, I, rep); mN = 1.0; merge_at = 200
        epsg = None
        if Ksch:
            en = AN.eps_n_annealed(N * I, AN.arrivals_A(Ksch)); epsg = (en / (N * I)).astype(np.float64)
    R = DTm.DRun(w, sp, rule, unit, seed, r=100, mN=mN, gmode=DR.GMODE[arm], gcap=3, epsg=epsg, pairmode=1)

    def adv_to(gt):
        while R.g < gt:
            R.advance(10)
            if merge_at and R.g == merge_at:
                R.merge(PG.kernel_seed_pg(R.N * R.I, 1, rep) ^ 0x5DEECE66D)

    def shares():
        ks = np.nonzero(R.gcount[:R.ngt[0]])[0]
        s = R.tsp[R.gbase[ks]]; c = R.gcount[ks]
        tot = c.sum()
        return float(c[Wd['DET'][s]].sum() / tot), float(c[Wd['PBN'][s]].sum() / tot)
    adv_to(g0)
    before = shares()
    if kind == 'nosucker':
        kD = Wd['names'].index('D')
        newk = R.make_type(Wd['uD'], PV.R_H, kD)
        n = R.replace_where(lambda k: Wd['sucker'][R.tunit[R.gbase[k]]] == 1, lambda k: newk)
    else:
        n = 0
        for i in range(R.I):
            R.island_stats()
        ks = np.nonzero(R.gcount[:R.ngt[0]])[0]
        modal = int(ks[np.argmax(R.gcount[ks])])
        n = R.replace_where(lambda k: R.acts(modal, k) == (1, 0), lambda k: modal)
    adv_to(g1)
    return dict(cell=cell, rep=rep, g0=g0, g1=g1, kind=kind, replaced=int(n), before=before, after=shares(),
                time_s=time.time() - t0)


def decompose_now(R, Wd):
    """Post-hoc mechanism decomposition (labelled post hoc): the DET and PBN members' mean fitness split by partner class
    (DET, PBN, third parties), pooled over islands (each type's fitness against its own island), and the DET-PBN pair
    relations (who exploits whom, mutual, feud)."""
    sys.path.insert(0, os.path.join(ROOT, 'src'))
    import detectors_kern as KG
    acc = {c: {p: 0.0 for p in ('DET', 'PBN', 'TP')} for c in ('DET', 'PBN')}
    cnt = {'DET': 0.0, 'PBN': 0.0}
    pr = dict(P_exploits_D=0.0, D_exploits_P=0.0, mutual=0.0, feud=0.0, n=0.0)
    for i in range(R.I):
        n = int(R.npres[i]); N = R.N
        ks = R.pres[i, :n].copy(); c = R.counts[i, ks].astype(float)
        s = R.tsp[R.gbase[ks]]
        M = KG.gacts_matrix(i, R.pres, R.npres, R.gbase, R.gg, R.GS, R.GN, R.tunit, R.tsp, R.A, R.selfa, R.widx, R.AG1,
                            R.AG2, R.PW, R.gmode).astype(np.int64)
        pay = KG.PAYM[M, M.T].astype(float)
        det = Wd['DET'][s]; pbn = Wd['PBN'][s]; tp = ~(det | pbn)
        for cls, mk in (('DET', det), ('PBN', pbn)):
            if not mk.any(): continue
            for pname, pm in (('DET', det), ('PBN', pbn), ('TP', tp)):
                cc = c * pm
                v = (pay[:, :] @ cc - np.diag(pay) * pm) / (N - 1)
                acc[cls][pname] += float((v[mk] * c[mk]).sum())
            cnt[cls] += float(c[mk].sum())
        if det.any() and pbn.any():
            di = np.nonzero(det)[0]; pi = np.nonzero(pbn)[0]
            for a in di:
                for b in pi:
                    w = c[a] * c[b]
                    x, y = M[a, b], M[b, a]
                    pr['n'] += w
                    if x == 1 and y == 0: pr['P_exploits_D'] += w
                    elif x == 0 and y == 1: pr['D_exploits_P'] += w
                    elif x == 1 and y == 1: pr['mutual'] += w
                    else: pr['feud'] += w
    out = dict(g=int(R.g), det=cnt['DET'] / (R.I * R.N), pbn=cnt['PBN'] / (R.I * R.N))
    for cls in ('DET', 'PBN'):
        for p in ('DET', 'PBN', 'TP'):
            out['%s_from_%s' % (cls, p)] = acc[cls][p] / cnt[cls] if cnt[cls] else None
    for k in ('P_exploits_D', 'D_exploits_P', 'mutual', 'feud'):
        out[k] = pr[k] / pr['n'] if pr['n'] else None
    return out


def mech_job(job):
    """Rerun (cell, rep) and decompose at the listed generations (post hoc)."""
    sys.path.insert(0, os.path.join(ROOT, 'src'))
    import detectors as DTm
    import detectors_run as DR
    import time
    cell, rep, gens = job
    t0 = time.time()
    R, merge_at, Wd = setup(cell, rep)
    out = []
    for gt in gens:
        while R.g < gt:
            R.advance(10)
            if merge_at and R.g == merge_at:
                import pangaea as PG
                R.merge(PG.kernel_seed_pg(R.N * R.I, 1, rep) ^ 0x5DEECE66D)
        out.append(decompose_now(R, Wd))
    return dict(cell=cell, rep=rep, decomp=out, time_s=time.time() - t0)


def setup(cell, rep):
    """The run object of (cell, rep) exactly as detectors_run.ff_job builds it (same seeds and founders)."""
    sys.path.insert(0, os.path.join(ROOT, 'src'))
    import detectors as DTm
    import detectors_run as DR
    import provenance as PV
    import pangaea as PG
    import annealed as AN
    import provenance_run as PR
    import realizable_scaling as RS
    geom, arm, Ksch, w = DR.cell_spec(cell)
    Wd = DTm.world(w)
    LS = Wd['LS']
    if geom == 'Cis':
        N, I = 200, 64
        rng = np.random.default_rng([N, I, rep, PR.SALT])
        sp = rng.choice(len(LS['mu']), size=(I, N), p=LS['mu'])
        rule = np.full((I, N), PV.R_SNON, np.int64); unit = LS['Eu'][LS['tau'][sp]]
        seed = PR.kernel_seed(N, I, rep); mN = RS.mN_cal(N)
        epsg = AN.schedule('ann', N, Ksch) if Ksch else None
        merge_at = 0
    else:
        N, I = 100, 128
        sp = DR.fission_founders('L' if geom in ('Cff', 'Ref') else geom, rep, Wd)
        rule = np.full((I, N), PV.R_SNON, np.int64); unit = LS['Eu'][LS['tau'][sp]]
        if geom == 'Ref':
            import removing_rivals as RR
            kPB = Wd['names'].index(RR.PB_SP)
            pos = RR.donor_positions(N, I, rep)
            for i in range(I):
                sp[i, pos[i]] = kPB; rule[i, pos[i]] = PV.R_H; unit[i, pos[i]] = Wd['Hu'][Wd['tau'][kPB]]
        seed = PG.kernel_seed_pg(N, I, rep); mN = 1.0; merge_at = 200
        epsg = None
        if Ksch:
            en = AN.eps_n_annealed(N * I, AN.arrivals_A(Ksch)); epsg = (en / (N * I)).astype(np.float64)
    R = DTm.DRun(w, sp, rule, unit, seed, r=100, mN=mN, gmode=DR.GMODE[arm], gcap=3, epsg=epsg, pairmode=1)
    return R, merge_at, Wd


def all_labels(rows):
    """Every label (overlap allowed) of every network removal, per cell."""
    out = {}
    for r in rows:
        rm = removals(r)
        for net, x in rm['removals'].items():
            if not x: continue
            for l in x['labels']:
                k = (r['cell'], net, l)
                out[k] = out.get(k, 0) + 1
    return {'%s|%s|%s' % k: v for k, v in sorted(out.items())}


def per_run(rows):
    return [dict(cell=r['cell'], rep=r['rep'], uo=r.get('uo'), **{k: v for k, v in removals(r).items()
                                                                 if k != 'removals'},
                 removals=removals(r)['removals'], writes=r['gctr']['write'], boot=r['gctr']['boot'],
                 sucker_enc=r['gctr']['sucker_enc'], arrivals=r['arrivals'], arrivals_cls=r['arrivals_cls'])
            for r in rows]


def md(rep):
    L = ['# Legitimate detectors: run tables (generated by src/detectors_report.py)', '']
    if rep['A']:
        L += ['## Part A: predator establishment per arrival (pooled over the top three K predators)', '',
              '| N | arm | established / runs | p [95%] |', '|---|---|---|---|']
        for k, v in rep['A']['pooled'].items():
            L.append('| %d | %s | %d / %d | %.3f [%.3f, %.3f] |' % (v['N'], v['arm'], v['est'], v['n'], v['p'], v['ci'][0], v['ci'][1]))
        L += ['', '| second arrival (N = 200) | first lost | second established / n |', '|---|---|---|']
        for k, v in sorted(rep['A']['second'].items()):
            L.append('| %s | %d | %d / %d |' % (k, v['first_lost'], v['second_est'], v['second_n']))
        L += ['', '| N_arm | mean writes per arrival | marked share at the end | generations |', '|---|---|---|---|']
        for k, v in sorted(rep['A']['grudges'].items()):
            L.append('| %s | %.1f | %.2f | %.1f |' % (k, v['writes'], v['marked'], v['t']))
        L.append('')
    for part in ('B', 'C'):
        S = rep[part]
        if not S: continue
        L += ['## Part %s' % part, '', '| cell | n | winners | removals (headline) | DET at 200 / 10,000 (median) | universal-open | '
              'writes (boot share) | sucker enc. | arrivals |', '|---|---|---|---|---|---|---|---|---|']
        for c, v in sorted(S.items()):
            L.append('| %s | %d | %s | %s | %.3f / %.3f | %d | %.0f (%.2f) | %.0f | %.0f |' % (
                c, v['n'], ', '.join('%s %d' % kv for kv in sorted(v['winners'].items())),
                ', '.join('%s %d' % kv for kv in sorted(v['removals'].items())) or '–', v['det_at_200_median'],
                v['det_final_median'], v['uo'], v['writes_mean'], v['boot_share'], v['sucker_enc_mean'],
                v['arrivals_mean']))
        L.append('')
        L += ['Island-level holder changes away from DET or PBN (headline label):', '']
        for c, v in sorted(S.items()):
            if v['island_events']:
                L.append('- %s: %s' % (c, ', '.join('%s %d' % kv for kv in sorted(v['island_events'].items()))))
        L.append('')
    return '\n'.join(L)


def posthoc(workers=3):
    """After the cells: the mechanism decomposition on samples and the matched replays (both labelled post hoc /
    as notes §1.5 replays)."""
    from multiprocessing import Pool
    B = load('cells_B.json.gz'); Cr = load('cells_C.json.gz') + load('cells_R.json.gz')
    gens = [10, 50, 100, 190, 210, 300, 500, 1000, 2000, 5000]
    mjobs = [(c, rep, gens) for c in ('B1_K0_e0', 'B1_KG_e0', 'B2_K0_e0', 'B2_KG_e0', 'Cff_K0_e0', 'Cff_KG_e0',
                                       'Cff_L_e0') for rep in range(4)]
    rjobs = []
    seen = {}
    for r in B + Cr:
        rm = removals(r)
        for net, x in rm['removals'].items():
            if not x: continue
            g1 = int(x['g'])
            g0 = max(10, int(np.floor((g1 - 100) / 10.0) * 10))
            if g0 >= g1: continue
            for lab, kind in (('predation', 'nopred'), ('prudence premium', 'nosucker'), ('inefficiency', 'nosucker')):
                if lab in x['labels']:
                    k = (r['cell'], net, lab)
                    if seen.get(k, 0) >= 5: continue
                    seen[k] = seen.get(k, 0) + 1
                    rjobs.append((r['cell'], r['rep'], g0, g1 + 50, kind, net, lab))
    out_m, out_r = [], []
    with Pool(workers) as pool:
        for res in pool.imap_unordered(mech_job, mjobs):
            out_m.append(res); print('mech', res['cell'], res['rep'], round(res['time_s']), flush=True)
        json.dump(out_m, open(os.path.join(OUT, 'mech.json'), 'w'), default=float)
        for res in pool.imap_unordered(_replay_wrap, rjobs):
            out_r.append(res); print('replay', res['cell'], res['rep'], res['kind'], res['before'], res['after'], flush=True)
        json.dump(out_r, open(os.path.join(OUT, 'replays.json'), 'w'), default=float)


def _replay_wrap(job):
    cell, rep, g0, g1, kind, net, lab = job
    r = replay_job((cell, rep, g0, g1, kind))
    r.update(net=net, label=lab)
    return r


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'posthoc':
        posthoc()
        return
    A = load('cells_A.json.gz')
    B = load('cells_B.json.gz')
    Cr = load('cells_C.json.gz') + load('cells_R.json.gz')
    rep = dict(A=part_a(A) if A else None, B=cell_summary(B) if B else None, C=cell_summary(Cr) if Cr else None,
               labels_B=all_labels(B), labels_C=all_labels(Cr), runs_B=per_run(B), runs_C=per_run(Cr))
    for extra in ('mech.json', 'replays.json'):
        p = os.path.join(OUT, extra)
        if os.path.exists(p): rep[extra.split('.')[0]] = json.load(open(p))
    json.dump(rep, open(os.path.join(ROOT, 'runs', 'detectors.json'), 'w'), indent=1, default=float)
    open(os.path.join(OUT, 'tables.md'), 'w').write(md(rep))
    print(md(rep))


if __name__ == '__main__':
    main()
