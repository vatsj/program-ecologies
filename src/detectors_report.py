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
    if det_rm and not pbn_rm: winner = 'PBN'
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


def main():
    A = load('cells_A.json.gz')
    B = load('cells_B.json.gz')
    Cr = load('cells_C.json.gz') + load('cells_R.json.gz')
    rep = dict(A=part_a(A) if A else None, B=cell_summary(B) if B else None, C=cell_summary(Cr) if Cr else None)
    json.dump(rep, open(os.path.join(ROOT, 'runs', 'detectors.json'), 'w'), indent=1, default=float)
    print(json.dumps(rep, indent=1, default=float)[:20000])


if __name__ == '__main__':
    main()
