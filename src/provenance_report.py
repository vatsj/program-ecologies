"""Summaries for runs/provenance.md and runs/provenance.json (predictions/2026-10-12-provenance.md).

    python3 src/provenance_report.py [--files main extra size] > runs/provenance/report.txt
"""
import argparse
import json
import math
import os
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import provenance as PV

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'provenance')
EB = PV.EBINS


def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'), float('nan'))
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def mcnemar_exact(b, c):
    n = b + c
    if n == 0: return 1.0
    k = min(b, c)
    p = sum(math.comb(n, i) for i in range(0, k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def boot_ci(x, nb=10000, seed=1):
    x = np.asarray(x, float)
    if len(x) == 0: return (float('nan'), float('nan'))
    rng = np.random.default_rng(seed)
    m = rng.choice(x, size=(nb, len(x)), replace=True).mean(1)
    return (float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975)))


def snap_at(r, g):
    """The snapshot at generation g: recorded, or the final state of a run that froze (one global type) or was never
    extended (universal with E3 decided by the horizon); None for an extension censored before g."""
    s = r['snaps'].get(str(g))
    if s is not None: return s
    if r.get('frozen_at', -1) > 0 and g >= r['last_gen']: return r['final']
    if g > r['gens'] and r['horizon'] <= r['gens']: return r['snaps'].get(str(r['gens'])) or r['final']
    return None


def censored_at(rows, g):
    return sum(1 for r in rows if snap_at(r, g) is None)


def cell_summary(rows, g=2000):
    I = rows[0]['I']
    out = {}
    cens = censored_at(rows, g)
    rows = [r for r in rows if snap_at(r, g) is not None]
    n = len(rows)
    out['censored'] = cens
    sn = [snap_at(r, g) for r in rows]
    uo = sum(1 for s in sn if s['universal_open'])
    out['runs'] = n
    out['established'] = sum(1 for r in rows if 0 <= r['establish_gen'] <= g)
    out['E3'] = dict(success=sum(1 for r in rows if r['E3'] == 'success' and r['E3_gen'] <= g),
                     fail=sum(1 for r in rows if r['E3'] == 'fail' and r['E3_gen'] <= g))
    out['E3']['censored'] = n - out['E3']['success'] - out['E3']['fail']
    out['outcome'] = {k: sum(1 for s in sn if s['outcome'] == k) for k in ('universal', 'patchwork', 'unheld')}
    out['universal_open'] = uo
    out['universal_open_wilson'] = wilson(uo, n)
    out['pcc'] = float(np.mean([s['pcc'] for s in sn]))
    out['identity_islands'] = float(np.mean([s['identity_islands'] / I for s in sn]))
    out['spo_islands'] = float(np.mean([s['spo_islands'] / I for s in sn]))
    out['open_islands'] = float(np.mean([s['open_islands'] / I for s in sn]))
    out['cross_pcc'] = float(np.mean([s['cross_pcc'] for s in sn]))
    out['runs_with_identity_island'] = sum(1 for s in sn if s['identity_islands'] > 0)
    pers = [r['persistence'] for r in rows if r['persistence'] is not None]
    out['persistence'] = float(np.mean(pers)) if pers else None
    est = sorted(r['establish_gen'] if r['establish_gen'] >= 0 else 10 ** 9 for r in rows)
    out['establish_median'] = est[n // 2] if est[n // 2] < 10 ** 9 else None
    fin = [r['establish_gen'] for r in rows if r['establish_gen'] >= 0]
    out['establish_mean_established'] = float(np.mean(fin)) if fin else None
    inst = np.array([s['inst'] for s in sn]).sum(0)          # rule x (C, SPO, search, host)
    out['spo_fraction_held'] = float(inst[:, 1].sum() / max(1, inst[:, 0].sum()))
    out['search_fraction_held'] = float(inst[:, 2].sum() / max(1, inst[:, 0].sum()))
    out['spo_instances_by_rule'] = {PV.RULE_NAMES[k]: int(inst[k, 1]) for k in range(PV.NRULE) if inst[k, 1] > 0}
    ctr = np.array([r['ctr'] for r in rows]).sum(0)
    out['spo_produced'] = int(ctr[:, PV.C_SPO_PROD].sum()); out['spo_copied'] = int(ctr[:, PV.C_SPO_COPY].sum())
    out['spo_by_nonself_production'] = int(ctr[:, PV.C_NONSELF_SPO].sum())
    out['ident_entries'] = int(ctr[:, PV.C_IDENT_ENTRY].sum()); out['spo_unit_entries'] = int(ctr[:, PV.C_SPOU_ENTRY].sum())
    out['n_quotes'] = float(np.mean([s['n_quotes'] for s in sn])); out['n_spellings'] = float(np.mean([s['n_spellings'] for s in sn]))
    rc = np.array([s['rule_coop'] for s in sn]).sum(0); ra = np.array([s['rule_all'] for s in sn]).sum(0)
    out['rule_coop'] = {PV.RULE_NAMES[k]: float(rc[k] / max(1, rc.sum())) for k in range(PV.NRULE) if ra[k] > 0}
    out['rule_all'] = {PV.RULE_NAMES[k]: float(ra[k] / max(1, ra.sum())) for k in range(PV.NRULE) if ra[k] > 0}
    out['group_ever_held'] = [sum(1 for r in rows if r['group_max'][z] > 0) for z in range(3)]
    out['seeded_Q_per_run'] = float(np.mean([r['seeded_Q'] for r in rows]))
    out['seeded_only_self_per_run'] = float(np.mean([r['seeded_only_self'] for r in rows]))
    out['time_s_mean'] = float(np.mean([r['time_s'] for r in rows]))
    return out


def costs(rows):
    """Per rule: per-match modelled production steps, attempts, successes, cap timeouts, waits and acquisitions."""
    ctr = np.array([r['ctr'] for r in rows]).sum(0)
    steps = np.array([r['steps_rule'] for r in rows]).sum(0)
    enc = np.array([r['enc_exp'] for r in rows]).sum(0)
    encf = np.array([r.get('enc_futile', [0] * PV.NRULE) for r in rows]).sum(0)
    hw = np.array([r['hist_wait'] for r in rows]).sum(0)          # rule, cap, kind(4), bins
    ha = np.array([r['hist_acq'] for r in rows]).sum(0)           # rule, cap, bins
    hs = np.array([r['hist_steps'] for r in rows]).sum(0)         # rule, bins
    hc = np.array([r['hist_cens'] for r in rows]).sum(0)          # rule, cap, how(2), bins
    npd = np.array([r['nprod'] for r in rows]).sum(0)             # rule, cap, (acq, death, horizon, mono)
    out = {}
    b20 = int(np.searchsorted(EB, 20))                            # bins >= 20 encounters
    for k in range(PV.NRULE):
        if enc[k] <= 0: continue
        c = ctr[k]
        d = dict(per_match_steps=float(steps[k] / enc[k]), enc_exp=float(enc[k]), futile_enc=float(encf[k]),
                 futile_share=float(encf[k] / enc[k]), C_attempts=int(c[PV.C_CATT]),
                 C_ok=int(c[PV.C_COK]), C_capTO=int(c[PV.C_CTO]), C_none=int(c[PV.C_CNONE]),
                 capTO_share=float(c[PV.C_CTO] / max(1, c[PV.C_CATT])), D_attempts=int(c[PV.C_DATT]),
                 AC=int(c[PV.C_AC]), AC_ok=int(c[PV.C_ACOK]), skip_self=int(c[PV.C_SKIPSELF]),
                 delay_skip=int(c[PV.C_DELAY_SKIP]),
                 windows=dict(closed_k=int(c[PV.C_WIN_K]), closed_deadline=int(c[PV.C_WIN_DL]),
                              safeguard=int(c[PV.C_WIN_SAFE]), fallback=int(c[PV.C_WIN_FALLBACK]),
                              strict_cleared=int(c[PV.C_WIN_STRICTCLR]), cleared_no_admissible=int(c[PV.C_WIN_EMPTYCLR]),
                              candidates=int(c[PV.C_CAND]), spo_kept_safeguard=int(c[PV.C_SAFE_SPO]),
                              spo_kept_fallback=int(c[PV.C_FALL_SPO])),
                 gate=dict(lookups=int(c[PV.C_GATE]), hits=int(c[PV.C_HIT]), misses=int(c[PV.C_MISS]),
                           gate_T=int(c[PV.C_GATE_T]), gate_TO=int(c[PV.C_GATE_TO]), stores=int(c[PV.C_STORE]),
                           hit_timeout=int(c[PV.C_HIT_TO]), hit_rejected=int(c[PV.C_HIT_REJ]),
                           invalidations=int(c[PV.C_INVAL]), overflow=int(c[PV.C_OVERFLOW]),
                           appends=int(c[PV.C_GATE_APPEND])))
        prods = {}
        for cap in (0, 1):
            acq = int(npd[k, cap, 0]); death = int(npd[k, cap, 1]); hor = int(npd[k, cap, 2]); mono = int(npd[k, cap, 3])
            tot = acq + death + hor
            if tot == 0: continue
            # waits: attempted (kind 0) and never attempted (kind 2, a lower bound)
            wa = hw[k, cap, 0]; wn = hw[k, cap, 2]
            ge20 = int(wa[b20:].sum() + wn[b20:].sum())
            wam = hw[k, cap, 1]; wnm = hw[k, cap, 3]
            ge20m = int(wam[b20:].sum() + wnm[b20:].sum())
            acq_h = ha[k, cap]
            cum = np.cumsum(acq_h)
            med_bin = int(np.searchsorted(cum, (cum[-1] + 1) // 2)) if cum[-1] > 0 else None
            prods['capable' if cap else 'incapable'] = dict(
                producers=tot, acquired=acq, censored_death=death, never_by_horizon=hor,
                never_by_horizon_share=float(hor / tot), wait_ge20=ge20, wait_ge20_share=float(ge20 / tot),
                near_monoclonal=mono, wait_ge20_mono=ge20m, wait_ge20_mono_share=float(ge20m / mono) if mono else None,
                acq_enc_median_bin=None if med_bin is None else [int(EB[med_bin]), int(EB[med_bin + 1])],
                acq_enc_hist=acq_h.tolist(), wait_hist=wa.tolist())
        d['producers'] = prods
        cs = np.cumsum(hs[k])
        if cs[-1] > 0:
            mb = int(np.searchsorted(cs, (cs[-1] + 1) // 2))
            d['acq_steps_median'] = float(10 ** (2 + (mb + 0.5) / 10))
            d['acq_steps_hist'] = hs[k].tolist()
        out[PV.RULE_NAMES[k]] = d
    return out


def paired(A, B, g=2000):
    """Paired contrast A - B on universal-open (discordant pairs, exact McNemar) and identity islands."""
    ra = {r['rep']: r for r in A}; rb = {r['rep']: r for r in B}
    reps = sorted(set(ra) & set(rb))
    I = A[0]['I']
    ua = np.array([bool((snap_at(ra[k], g) or ra[k]['final'])['universal_open']) for k in reps])
    ub = np.array([bool((snap_at(rb[k], g) or rb[k]['final'])['universal_open']) for k in reps])
    ia = np.array([(snap_at(ra[k], g) or ra[k]['final'])['identity_islands'] / I for k in reps])
    ib = np.array([(snap_at(rb[k], g) or rb[k]['final'])['identity_islands'] / I for k in reps])
    b = int((ua & ~ub).sum()); c = int((~ua & ub).sum())
    du = ua.astype(float) - ub.astype(float)
    di = ia - ib
    return dict(n=len(reps), A_univ=int(ua.sum()), B_univ=int(ub.sum()), discordant_A_only=b, discordant_B_only=c,
                mcnemar_p=mcnemar_exact(b, c), univ_diff_runs=int(ua.sum() - ub.sum()), univ_diff_mean=float(du.mean()),
                univ_diff_ci=boot_ci(du), ident_diff_mean=float(di.mean()), ident_diff_ci=boot_ci(di))


def rule_composition(rows, gens=(50, 200, 1000, 2000)):
    """Mixed cell: rule shares among cooperative individuals on held islands at establishment and checkpoints, full
    rule frequencies beside them, and the strata by holder run tree."""
    out = {}
    est = [r['est_snap'] for r in rows if r.get('est_snap')]
    def agg(sns, key):
        v = np.array([s[key] for s in sns]).sum(0)
        return [float(x) for x in v / max(1, v.sum())]
    out['establishment'] = dict(coop=agg(est, 'rule_coop'), all=agg(est, 'rule_all'), runs=len(est))
    for g in gens:
        sns = [snap_at(r, g) for r in rows]
        sns = [s for s in sns if s]
        out[str(g)] = dict(coop=agg(sns, 'rule_coop'), all=agg(sns, 'rule_all'), runs=len(sns))
    strat = defaultdict(lambda: np.zeros(PV.NRULE))
    for r in rows:
        s = snap_at(r, 2000) or r['final']
        for name, v in s['strat_tree']:
            strat[name] += np.array(v)
    top = sorted(strat.items(), key=lambda z: -z[1].sum())[:15]
    out['strata_tree_2000'] = [(n, [float(x) for x in v / v.sum()], float(v.sum())) for n, v in top]
    strat = defaultdict(lambda: np.zeros(PV.NRULE))
    for r in rows:
        s = snap_at(r, 2000) or r['final']
        for name, v in s['strat_sp']:
            strat[name] += np.array(v)
    top = sorted(strat.items(), key=lambda z: -z[1].sum())[:15]
    out['strata_spelling_2000'] = [(n, [float(x) for x in v / v.sum()], float(v.sum())) for n, v in top]
    return out


def stages(rows, g=2000):
    """Arrival -> establishment -> persistence -> spread, for identity units, SPO-only units and open units."""
    I = rows[0]['I']
    ctr = np.array([r['ctr'] for r in rows]).sum(0)
    res = {}
    for z, (name, key, entry) in enumerate((('identity', 'identity_islands', PV.C_IDENT_ENTRY),
                                            ('spo', 'spo_islands', PV.C_SPOU_ENTRY), ('open', 'open_islands', None))):
        held_end = [((snap_at(r, g) or r['final'])[key]) for r in rows]
        arrivals = int(ctr[:, entry].sum()) if entry is not None else None
        res[name] = dict(entries=arrivals, runs_ever_held=sum(1 for r in rows if r['group_max'][z] > 0),
                         runs_held_at_end=sum(1 for h in held_end if h > 0), islands_at_end=int(sum(held_end)),
                         islands_per_entry=(float(sum(held_end) / arrivals) if arrivals else None),
                         first_gen_median=(float(np.median([r['group_first'][z] for r in rows if r['group_first'][z] >= 0]))
                                           if any(r['group_first'][z] >= 0 for r in rows) else None),
                         max_islands_mean=float(np.mean([r['group_max'][z] for r in rows])))
    res['seeded_Q_per_run'] = float(np.mean([r['seeded_Q'] for r in rows]))
    res['seeded_only_self_per_run'] = float(np.mean([r['seeded_only_self'] for r in rows]))
    return res


def holders(rows, g=2000, top=10):
    c = defaultdict(int)
    for r in rows:
        s = snap_at(r, g) or r['final']
        for name, n in s['holders']:
            c[name] += n
    return sorted(c.items(), key=lambda z: -z[1])[:top]


def pad_row(r):
    """Rows written before the diagnostic rule was added have 10 rule rows; pad every per-rule array to NRULE."""
    R = PV.NRULE

    def pad(x, depth=0):
        x = np.asarray(x)
        if x.shape[0] >= R: return x.tolist()
        z = np.zeros((R - x.shape[0],) + x.shape[1:], x.dtype)
        return np.concatenate([x, z]).tolist()
    for key in ('ctr', 'steps_rule', 'enc_exp', 'enc_futile', 'hist_wait', 'hist_acq', 'hist_steps', 'hist_cens', 'nprod'):
        if key in r: r[key] = pad(r[key])
    sns = list(r['snaps'].values()) + [r['final']] + ([r['est_snap']] if r.get('est_snap') else [])
    for s in sns:
        for key in ('rule_all', 'rule_coop', 'inst'):
            s[key] = pad(s[key])
        s['strat_tree'] = [(n, pad(v)) for n, v in s['strat_tree']]
        s['strat_sp'] = [(n, pad(v)) for n, v in s['strat_sp']]
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--files', nargs='+', default=['main'])
    a = ap.parse_args()
    rows = []
    for f in a.files:
        p = os.path.join(OUT, 'lottery_%s.json' % f)
        if os.path.exists(p):
            rows += [pad_row(r) for r in json.load(open(p))]
    by = defaultdict(list)
    for r in rows:
        by[r['cell']].append(r)
    for c in by: by[c].sort(key=lambda r: r['rep'])
    rep = dict(cells={}, costs={}, stages={}, holders={}, contrasts={}, composition={})
    for c, rs in by.items():
        rep['cells'][c] = cell_summary(rs)
        if max(r['horizon'] for r in rs) > 2000:
            rep['cells'][c + '@10000'] = cell_summary(rs, g=10000)
            rep['cells'][c + '@10000']['extended_runs'] = sum(1 for r in rs if r['horizon'] > 2000)
        rep['costs'][c] = costs(rs)
        rep['stages'][c] = stages(rs)
        rep['holders'][c] = holders(rs)
    pairs = [('a', 'Snon', 'Sself'), ('b', 'Snon', 'Sdel'), ('c', 'Snon', 'Cdonor'), ('', 'ablation', 'Snon'),
             ('', 'S2', 'Sself'), ('', 'S3', 'Sself'), ('', 'S3', 'Snon'), ('', 'S2', 'Snon'), ('', 'S3strict', 'Snon'),
             ('', 'S3strict', 'Sself'), ('', 'Sdel', 'Sself'), ('', 'CSnon', 'Snon'), ('', 'mixed', 'Sself'),
             ('', 'mixed', 'Snon'), ('', 'Sgate', 'Sself'), ('', 'Sgate', 'Snon'), ('', 'H', 'Snon'),
             ('', 'Cdonor', 'H'), ('', 'Snon_N200', 'Sself_N200'), ('', 'Snon_I128', 'Sself_I128'),
             ('', 'Snon_N200', 'Cdonor_N200'), ('', 'Snon_I128', 'Cdonor_I128'),
             ('diag', 'S2own', 'S2'), ('diag', 'S2time', 'S2'), ('diag', 'SselfDF', 'Sself'), ('diag', 'S2time', 'SselfDF'),
             ('diag', 'S2time', 'Sself')]
    for tag, A, B in pairs:
        if A in by and B in by:
            rep['contrasts']['%s%s - %s' % ('(%s) ' % tag if tag else '', A, B)] = paired(by[A], by[B])
    if 'mixed' in by:
        rep['composition']['mixed'] = rule_composition(by['mixed'])
    json.dump(rep, open(os.path.join(ROOT, 'runs', 'provenance.json'), 'w'), indent=1, default=float)
    # text tables
    print('| cell | runs | E3 s/f/c | univ/patch/unheld | universal-open [Wilson] | island P(C,C) | identity islands | SPO islands | cross P(C,C) | SPO held frac | estab median | time s |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for c, s in rep['cells'].items():
        w = s['universal_open_wilson']
        print('| %s | %d | %d/%d/%d | %d/%d/%d | %d [%.2f, %.2f] | %.3f | %.3f | %.3f | %.3f | %.4f | %s | %.0f |' % (
            c, s['runs'], s['E3']['success'], s['E3']['fail'], s['E3']['censored'], s['outcome']['universal'],
            s['outcome']['patchwork'], s['outcome']['unheld'], s['universal_open'], w[0], w[1], s['pcc'],
            s['identity_islands'], s['spo_islands'], s['cross_pcc'], s['spo_fraction_held'], s['establish_median'],
            s['time_s_mean']))
    print()
    print('| cell | identity: entries, runs ever held, runs held at end, islands at end, per entry | SPO-only: entries, ever, end, islands, per entry | open: ever, end, islands | seeded Q / only-self per run |')
    print('|---|---|---|---|---|')
    for c, s in rep['stages'].items():
        a, b, o = s['identity'], s['spo'], s['open']
        f = lambda x: '-' if x is None else '%.3f' % x
        print('| %s | %s, %d, %d, %d, %s | %s, %d, %d, %d, %s | %d, %d, %d | %.1f / %.1f |' % (
            c, a['entries'], a['runs_ever_held'], a['runs_held_at_end'], a['islands_at_end'], f(a['islands_per_entry']),
            b['entries'], b['runs_ever_held'], b['runs_held_at_end'], b['islands_at_end'], f(b['islands_per_entry']),
            o['runs_ever_held'], o['runs_held_at_end'], o['islands_at_end'], s['seeded_Q_per_run'], s['seeded_only_self_per_run']))
    print()
    for c, cr in rep['costs'].items():
        for rule, d in cr.items():
            cap = d.get('producers', {}).get('capable', {})
            print('%-12s %-15s per-match executed %.0f, futile share %.3f, C attempts %d ok %d capTO %.4f, acq median steps %s, capable producers %s acquired %s died %s at-horizon %s wait>=20 %.4f (near-mono %s: %s)' % (
                c, rule, d['per_match_steps'], d['futile_share'], d['C_attempts'], d['C_ok'], d['capTO_share'],
                '%.0f' % d['acq_steps_median'] if 'acq_steps_median' in d else '-', cap.get('producers'),
                cap.get('acquired'), cap.get('censored_death'), cap.get('never_by_horizon'), cap.get('wait_ge20_share', 0),
                cap.get('near_monoclonal'), cap.get('wait_ge20_mono_share')))
    print()
    for k, v in rep['contrasts'].items():
        print('%-34s n %d univ %d vs %d (A-only %d, B-only %d, p %.3g; diff %+.3f [%.3f, %.3f]) ident diff %+.3f [%.3f, %.3f]' % (
            k, v['n'], v['A_univ'], v['B_univ'], v['discordant_A_only'], v['discordant_B_only'], v['mcnemar_p'],
            v['univ_diff_mean'], v['univ_diff_ci'][0], v['univ_diff_ci'][1], v['ident_diff_mean'],
            v['ident_diff_ci'][0], v['ident_diff_ci'][1]))


if __name__ == '__main__':
    main()
