"""Part A of the coalition-proof auctions run: the one-round notion on small package auctions (static, exhaustive).

    python3 src/auctions_static.py main            # all four families x (vcg, surcharge) -> runs/auctions/static_<fam>.json
    python3 src/auctions_static.py bw              # first-price leader values, the Bernheim-Whinston comparison and the R2 core (AM)
    python3 src/auctions_static.py wide            # sensitivity: responders on 0..4G, deviators on 0..2G (AM)
    python3 src/auctions_static.py ring            # grand ring per family and rule

Spec specs/2026-10-21-coalition-proof-auctions.md; predictions predictions/2026-10-21-coalition-proof-auctions.md.
"""
import json, math, os, sys, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auctions as A

G = 10
R = 2 * G + 1
OUT = os.path.join(A.ROOT, 'runs', 'auctions')
SEED = 20261021
SUB = 3000
EPS = 1e-9


def _json(o):
    if isinstance(o, dict): return {str(k): _json(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_json(v) for v in o]
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, np.ndarray): return _json(o.tolist())
    if isinstance(o, float) and not math.isfinite(o): return None
    return o


def save(name, obj):
    os.makedirs(OUT, exist_ok=True)
    json.dump(_json(obj), open(os.path.join(OUT, name), 'w'), indent=1)


def family_mask(fam):
    """instance mask: all instances (AM) or a fixed-seed subsample of SUB instances."""
    n = len(A.FAMILIES[fam])
    NI = G ** n
    if NI <= SUB:
        return np.ones(NI, bool)
    rng = np.random.default_rng(SEED)
    m = np.zeros(NI, bool)
    m[rng.choice(NI, SUB, replace=False)] = True
    return m


def coalition_class(sm, winmask, size):
    if size == 1:
        return 'singleton'
    if sm & ~winmask == 0:
        return 'winners'
    if sm & winmask == 0:
        return 'losers'
    return 'mixed'


def summarize(fam, rule, auc, res, ti, mask):
    """robust fractions and break classification per variant; deterred-only shares."""
    gain = res['gain']; SS = res['SS']
    sel = np.nonzero(mask)[0]
    nI = len(sel)
    out = dict(family=fam, rule=rule, n_instances=int(nI), variants={})
    wm = ti['winmask'][sel]
    smask = [sum(1 << i for i in S) for S in SS]
    brk_all = {}
    for k, name in enumerate(A.VARIANTS):
        brk = gain[k][sel] > EPS                          # (nI, nS)
        brk_all[k] = brk
        anyb = brk.any(1)
        v = dict(robust_frac=float(1 - anyb.mean()), n_robust=int((~anyb).sum()),
                 unresolved_instances=float((res['unres'][k][sel] > 0).any(1).mean()),
                 mean_max_gain=float(np.where(anyb, gain[k][sel].max(1), 0).mean()))
        cls = {c: np.zeros(nI, bool) for c in ('singleton', 'losers', 'winners', 'mixed')}
        pair_counts = {c: 0 for c in cls}
        for si, S in enumerate(SS):
            for q in range(nI):
                if brk[q, si]:
                    c = coalition_class(smask[si], int(wm[q]), len(S))
                    cls[c][q] = True; pair_counts[c] += 1
        v['instances_with_break_by_class'] = {c: float(cls[c].mean()) for c in cls}
        v['break_events_by_class'] = pair_counts
        v['broken_only_by_singleton'] = float((cls['singleton'] & ~(cls['losers'] | cls['winners'] | cls['mixed'])).mean())
        v['broken_only_by_multi'] = float(((~cls['singleton']) & (cls['losers'] | cls['winners'] | cls['mixed'])).mean())
        v['by_coalition'] = {','.join(str(i + 1) for i in S): float(brk[:, si].mean()) for si, S in enumerate(SS)}
        out['variants'][name] = v
    # deterrence by spite: strict break not weak break
    det = {}
    for lab, ks, kw in (('R1', 0, 1), ('R1_literal', 0, 2), ('R2', 3, 4)):
        bs, bw = brk_all[ks], brk_all[kw]
        inst_s = bs.any(1); inst_w = bw.any(1)
        det[lab] = dict(strict_broken_instances=int(inst_s.sum()),
                        deterred_only_instances=int((inst_s & ~inst_w).sum()),
                        share_instances=float((inst_s & ~inst_w).sum() / max(1, inst_s.sum())),
                        strict_break_events=int(bs.sum()), deterred_only_events=int((bs & ~bw).sum()),
                        share_events=float((bs & ~bw).sum() / max(1, bs.sum())),
                        weak_not_strict_events=int((bw & ~bs).sum()))
    out['spite'] = det
    return out


def spite_margins(auc, rule, res, ti, mask, nmax=400):
    """for instances broken under R1/T-strict but robust under R1/T-weak: the margin of the spiteful responder (bid distance
    below the smallest winning bid), at the strict-gain-maximizing coalition and deviation."""
    gain = res['gain']; SS = res['SS']; insts = res['insts']
    win, pay = auc.tables(rule)
    n, Rr = auc.n, auc.R
    sel = np.nonzero(mask)[0]
    ev = np.argwhere((gain[0][sel] > EPS) & ~(gain[1][sel] > EPS))      # (instance row, coalition) break events deterred only by spite
    rng = np.random.default_rng(SEED)
    if len(ev) > nmax:
        ev = ev[rng.choice(len(ev), nmax, replace=False)]
    cand = ev
    margins = []; cannot = 0; nspite = 0
    for row, si in cand:
        q = sel[row]; S = SS[si]
        ds_code = int(res['arg'][0, q, si])
        Rd_ = res['Rd']
        dS = [(ds_code // Rd_ ** s) % Rd_ for s in range(len(S))]
        vals = insts[q]
        rs, Cl = A.response_set(auc, rule, S, vals, dS, 'strict')
        rw, _ = A.response_set(auc, rule, S, vals, dS, 'weak')
        if not rs or not rw:
            continue
        # S's totals
        def stot(r):
            idx = sum(dS[s] * int(auc.base[S[s]]) for s in range(len(S))) + sum(r[j] * int(auc.base[Cl[j]]) for j in range(len(Cl)))
            return sum(int(vals[i]) * int(win[idx, i]) - pay[idx, i] for i in S)
        r0 = min(rs, key=lambda r: (sum(abs(r[j] - int(vals[Cl[j]])) for j in range(len(Cl))), sum(r[j] * Rr ** j for j in range(len(Cl)))))
        rstar = min(rw, key=stot)
        for j in range(len(Cl)):
            if rstar[j] != r0[j]:
                nspite += 1
                idx = sum(dS[s] * int(auc.base[S[s]]) for s in range(len(S))) + sum(rstar[t] * int(auc.base[Cl[t]]) for t in range(len(Cl)))
                wb = None
                for b in range(Rr):
                    idb = idx + (b - rstar[j]) * int(auc.base[Cl[j]])
                    if win[idb, Cl[j]]:
                        wb = b; break
                if wb is None:
                    cannot += 1
                else:
                    margins.append(wb - rstar[j])
    m = np.array(margins) if margins else np.array([0])
    return dict(n_sampled=int(len(cand)), n_spiters=nspite, cannot_win=cannot, n_margins=len(margins),
                margin_mean=float(m.mean()), margin_median=float(np.median(m)), margin_min=int(m.min()), margin_max=int(m.max()),
                share_margin_le0=float((m <= 0).mean()) if margins else None)


def core_stats(auc, G):
    inc, sur, d = A.vcg_in_core(auc, G)
    return inc, sur


def family_report(fam, rules=('vcg', 'surcharge'), Rd=None, tag='', with_spite=True):
    t0 = time.time()
    pk = A.FAMILIES[fam]
    Rr = R if Rd is None else 2 * G * 2 + 1
    auc = A.Auction(pk, Rr)
    mask = family_mask(fam)
    n = len(pk)
    out = dict(family=fam, packages=list(pk), G=G, R=Rr, Rd=(Rd or Rr), n_instances_total=int(G ** n), n_instances_evaluated=int(mask.sum()),
               subsample_seed=SEED if mask.sum() < G ** n else None, rules={})
    sel = np.nonzero(mask)[0]
    inc, sur = core_stats(auc, G)
    out['P_vcg_in_core'] = float(inc[sel].mean()); out['mean_surcharge_total'] = float(sur[sel].mean())
    out['mean_surcharge_when_positive'] = float(sur[sel][sur[sel] > 1e-9].mean()) if (sur[sel] > 1e-9).any() else 0.0
    out['share_positive_surcharge'] = float((sur[sel] > 1e-9).mean())
    for rule in ('vcg', 'surcharge', 'fp'):
        ti = A.truth_info(auc, rule, G)
        out.setdefault('revenue_at_truth', {})[rule] = float(ti['revenue'][sel].mean())
        out.setdefault('bidder_welfare_at_truth', {})[rule] = float(ti['u'].sum(1)[sel].mean())
    out['efficient_welfare'] = float(A.truth_info(auc, 'vcg', G)['welfare'][sel].mean())
    for rule in rules:
        t1 = time.time()
        res = A.analyze(auc, rule, G, mask=mask, Rd=(R if Rd is not None else None))
        ti = A.truth_info(auc, rule, G)
        summ = summarize(fam, rule, auc, res, ti, mask)
        summ['seconds'] = time.time() - t1
        summ['nmulti_by_coalition'] = {','.join(str(i + 1) for i in S): [int(res['nmulti'][k, si]) for k in range(A.NV)] for si, S in enumerate(res['SS'])}
        summ['maxset_by_coalition'] = {','.join(str(i + 1) for i in S): [int(res['maxset'][k, si]) for k in range(A.NV)] for si, S in enumerate(res['SS'])}
        summ['unresolved_events'] = {A.VARIANTS[k]: int((res['unres'][k][sel] > 0).sum()) for k in range(A.NV)}
        if fam == 'AM' and rule == 'vcg':
            # prediction 2 mismatch
            insts = res['insts'][sel]
            pred = insts[:, 0] > np.minimum(insts[:, 1], insts[:, 2])
            brk = (res['gain'][0][sel] > EPS).any(1)
            summ['pred2_mismatch'] = int((brk != pred).sum())
            summ['pred2_fail_only_where_vP_gt_min'] = bool(((~pred) & brk).sum() == 0)
        if fam == 'AM' and rule == 'surcharge':
            insts = res['insts'][sel]
            pos = sur[sel] > 1e-9
            brk = (res['gain'][0][sel] > EPS)
            SS = res['SS']
            # singleton break on positive-surcharge instances; losers-collusion (the pair {A,B}) never profits
            single_idx = [si for si, S in enumerate(SS) if len(S) == 1]
            ab = SS.index((1, 2))
            summ['pred3'] = dict(positive_surcharge_instances=int(pos.sum()),
                                 singleton_break_on_positive=float(brk[pos][:, single_idx].any(1).mean()),
                                 pair_AB_break_overall=float(brk[:, ab].mean()),
                                 pair_AB_break_on_positive=float(brk[pos][:, ab].mean()),
                                 truthful_winners_among_AB_when_positive=float(((ti['winmask'][sel][pos] & 6) == 6).mean()))
        if with_spite and fam == 'AM':
            summ['spite_margin'] = spite_margins(auc, rule, res, ti, mask)
        out['rules'][rule] = summ
        if fam in ('AM',):
            np.savez_compressed(os.path.join(OUT, 'tmp_%s_%s%s.npz' % (fam, rule, tag)), gain=res['gain'].astype(np.float32), unres=res['unres'].astype(np.int32))
    out['seconds'] = time.time() - t0
    return out


def ring_report(fam, auc, mask):
    sel = np.nonzero(mask)[0]
    insts = A.all_instances(auc.n, G)[sel]
    out = {}
    for rule in ('vcg', 'surcharge', 'fp'):
        best, rev, wel, eff, arg = A.ring(auc, rule, G, insts)
        ti = A.truth_info(auc, rule, G)
        tb = ti['u'].sum(1)[sel]; tr = ti['revenue'][sel]
        gain = best - tb
        ring_eff = np.abs(wel - eff) < 1e-9
        out[rule] = dict(mean_truthful_bidder_total=float(tb.mean()), mean_ring_total=float(best.mean()), mean_gain=float(gain.mean()),
                         mean_revenue_at_truth=float(tr.mean()), mean_revenue_at_ring=float(rev.mean()),
                         gain_over_truthful_revenue=float(gain.sum() / max(tr.sum(), 1e-9)),
                         share_efficient_at_ring=float(ring_eff.mean()), share_zero_payment_efficient=float((ring_eff & (rev < 1e-9)).mean()),
                         share_ring_gain_equals_revenue_at_truth=float((np.abs(gain - tr) < 1e-9).mean()),
                         max_gain_minus_revenue=float((gain - tr).max()))
    return out


# ------------------------------------------------------------------ Bernheim-Whinston comparison (first-price, AM)
def integer_core(auc, q_idx, G):
    """integer points of the true-value core (bidder payoffs u, revenue >= 0) and its Pareto-maximal subset."""
    n = auc.n
    SSall = [S for S in range(1, 1 << n)]
    cS = {S: int(auc.W[q_idx] - auc.Wex[S][q_idx]) for S in SSall}
    grid = np.stack(np.meshgrid(*[np.arange(G + 1)] * n, indexing='ij'), -1).reshape(-1, n)
    ok = np.ones(len(grid), bool)
    for S in SSall:
        tot = sum(grid[:, i] for i in range(n) if S >> i & 1)
        ok &= tot <= cS[S]
    core = grid[ok]
    cset = set(map(tuple, core.tolist()))
    pareto = []
    for u in core:
        mx = True
        for i in range(n):
            u2 = list(u); u2[i] += 1
            if tuple(u2) in cset:
                mx = False; break
        if mx:
            pareto.append(u)
    return core, np.array(pareto)


def bw_report(fam='AM'):
    t0 = time.time()
    auc = A.Auction(A.FAMILIES[fam], R)
    n = auc.n
    mask = np.ones(G ** n, bool)
    res = A.analyze(auc, 'fp', G, mask=mask)
    win, pay = auc.tables('fp')
    insts = res['insts']
    SS = res['SS']
    vcg_ti = A.truth_info(auc, 'vcg', G)
    out = dict(family=fam, rule='fp', n_instances=int(len(insts)), unresolved_events={A.VARIANTS[k]: int((res['unres'][k] > 0).sum()) for k in range(A.NV)},
               variants={})
    for k, name in ((0, 'R1_strict'), (1, 'R1_weak'), (3, 'R2_strict'), (4, 'R2_weak')):
        nonempty = 0; n_all_within1 = 0; n_some_within1 = 0; dists_max = []; dists_min = []; sizes = []
        revs = []; bws = []; vrev = []; vbw = []; n_nonempty_core_bad = 0; n_in_core = 0; n_vec = 0
        for q in range(len(insts)):
            v = insts[q]
            tidx = int(v @ auc.base)
            wstar = int(auc.W[tidx])
            welf = (win.astype(np.int64) * v).sum(1)
            u = v * win - pay
            okm = np.abs(welf - wstar) < 1e-9
            for si, S in enumerate(SS):
                tot = u[:, list(S)].sum(1)
                okm &= tot >= res['lead'][k, q, si] - 1e-9
            if not okm.any():
                continue
            nonempty += 1
            U = np.unique(u[okm].astype(np.int64), axis=0)
            sizes.append(len(U))
            core, par = integer_core(auc, tidx, G)
            dm = np.array([np.abs(par - uu).max(1).min() for uu in U])
            dists_max.append(dm.max()); dists_min.append(dm.min())
            n_all_within1 += int(dm.max() <= 1); n_some_within1 += int(dm.min() <= 1)
            cs = set(map(tuple, core.tolist()))
            n_vec += len(U); n_in_core += sum(tuple(uu) in cs for uu in U)
            revs.append(pay[okm].sum(1).mean()); bws.append(u[okm].sum(1).mean())
            vrev.append(vcg_ti['revenue'][q]); vbw.append(vcg_ti['u'][q].sum())
        ne = max(1, nonempty)
        out['variants'][name] = dict(nonempty=nonempty, nonempty_frac=nonempty / len(insts),
                                     all_within_1_tick=n_all_within1 / ne, some_within_1_tick=n_some_within1 / ne,
                                     n_all_within_1=n_all_within1, n_some_within_1=n_some_within1,
                                     mean_max_dist=float(np.mean(dists_max)) if dists_max else None, mean_min_dist=float(np.mean(dists_min)) if dists_min else None,
                                     mean_set_size=float(np.mean(sizes)) if sizes else None,
                                     share_vectors_in_true_core=n_in_core / max(1, n_vec),
                                     mean_revenue_in_set=float(np.mean(revs)) if revs else None, mean_bidder_welfare_in_set=float(np.mean(bws)) if bws else None,
                                     mean_vcg_revenue_same_instances=float(np.mean(vrev)) if vrev else None,
                                     mean_vcg_bidder_welfare_same_instances=float(np.mean(vbw)) if vbw else None)
    out['seconds'] = time.time() - t0
    return out


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'main'
    os.makedirs(OUT, exist_ok=True)
    if cmd == 'main':
        fams = sys.argv[2:] or ['AM', 'AMplus', 'subs', 'twopk']
        for fam in fams:
            r = family_report(fam)
            save('static_%s.json' % fam, r)
            print(fam, 'done in %.0fs' % r['seconds'], flush=True)
    elif cmd == 'bw':
        r = bw_report('AM')
        save('static_bw_AM.json', r)
        print('bw done in %.0fs' % r['seconds'])
    elif cmd == 'wide':
        r = family_report('AM', Rd=R, tag='_wide', with_spite=True)
        save('static_wide_AM.json', r)
        print('wide done in %.0fs' % r['seconds'])
    elif cmd == 'ring':
        out = {}
        for fam in A.FAMILIES:
            auc = A.Auction(A.FAMILIES[fam], R)
            out[fam] = ring_report(fam, auc, family_mask(fam))
            print(fam, 'ring done', flush=True)
        save('static_ring.json', out)


if __name__ == '__main__':
    main()
