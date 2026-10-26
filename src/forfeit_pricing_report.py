"""Report for the forfeit-pricing run: summaries, classification, the verdicts of predictions/2026-10-26-forfeit-pricing.md, and the
tables.  Writes runs/forfeit-pricing.md and runs/forfeit-pricing.json.

    python3 src/forfeit_pricing_report.py
"""
import glob
import gzip
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import failure_pricing_confirm as F
import forfeit_pricing as FP
import forfeit_pricing_run as FR

ROOT = FP.ROOT
OUT = FP.OUT
LEVELS = list(FP.LEVELS)
_c = {}
MARGIN = 0.05


def load(path):
    if path not in _c:
        _c[path] = json.load(gzip.open(path, 'rt')) if os.path.exists(path) else None
    return _c[path]


def cell(game, spec):
    rule, arm, level = FR.parse_spec(spec)
    return load(os.path.join(OUT, FR.spec_name(game, rule, arm, level) + '.json.gz'))


def pdcell(level):
    return load(os.path.join(OUT, 'pd_Af_%g.json.gz' % level))


def fmt(t, d=3):
    if t is None or (isinstance(t, (tuple, list)) and np.isnan(t[0])): return 'n/a'
    return '%.*f [%.*f, %.*f]' % (d, t[0], d, t[1], d, t[2])


def fc(k, n):
    t = F.wilson(k, n)
    return '%d/%d = %.3f [%.3f, %.3f]' % (k, n, t[0], t[1], t[2])


def table(head, rows):
    out = ['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)]
    for r in rows: out.append('| ' + ' | '.join(str(x) for x in r) + ' |')
    return '\n'.join(out) + '\n'


def sp(lv, rule='Af', arm=''):
    return '%s%s@%g' % (rule, arm, lv)


# ---------------------------------------------------------------------------------------------------------------- summaries
def rv(d, key, g='2000'):
    return np.array([r['stats'][g][key] for r in d['recs']], float)


def modal(d, name, role=None):
    if role is None: return np.array([r['ext']['modal_share'].get(name, 0.0) for r in d['recs']], float)
    return np.array([r['ext']['modal%d' % role].get(name, 0.0) for r in d['recs']], float)


def summ_rps(d, g='2000'):
    if d is None: return None
    eg = rv(d, 'e_gross', g); ep = rv(d, 'e_prog', g); fo = rv(d, 'forfeit', g)
    ec = rv(d, 'e_comp', g)
    mixst, a, b = F.rps_by_mixing(eg, fo)
    net = F.status_le(F.boot(ep), F.TH['rps'])
    s = dict(e_prog=F.boot(ep), e_gross=F.boot(eg), forfeit=F.boot(fo), e_comp=F.boot(ec), e_comp_undef=int(rv(d, 'e_comp_undef', g).sum()),
             mix=F.boot(rv(d, 'mix', g)), net=net, mixing=mixst, mixing_parts=(a, b), status=F.worst(net, mixst), n=len(eg),
             charge_play=F.boot(rv(d, 'charge_play', g)), to_play=F.boot(rv(d, 'to_play', g)), forf_play=F.boot(rv(d, 'forf_play', g)),
             coin_mass=F.boot(rv(d, 'coin_mass', g)),
             runs=dict(e_gross=eg, e_prog=ep, forfeit=fo, e_comp=ec))
    for nm in ('SIMX', 'SIM100u', 'SIM100u~', 'U', 'PRR', 'PB', 'CRR'):
        s['mass_' + nm] = F.boot(rv(d, 'mass_' + nm, g)); s['present_' + nm] = F.boot(rv(d, 'present_' + nm, g))
    key = 'modal_share' if g == '2000' else 'modal_share_4000'
    for nm in ('SIMX', 'SIM100u', 'SIM100u~', 'U', 'PRR', 'PB', 'CRR'):
        v = np.array([r['ext'][key].get(nm, 0.0) for r in d['recs']], float)
        s['modal_' + nm] = F.boot(v); s['runs']['modal_' + nm] = v
    s['runs']['mass_SIMX'] = rv(d, 'mass_SIMX', g)
    s['runs']['coin_mass'] = rv(d, 'coin_mass', g)
    s['runs']['mass_PB'] = rv(d, 'mass_PB', g); s['runs']['mass_U'] = rv(d, 'mass_U', g); s['runs']['mass_PRR'] = rv(d, 'mass_PRR', g)
    tr = np.mean([r['ext']['transitions']['1500-2000']['modal'] for r in d['recs']])
    s['trans_modal_1500_2000'] = float(tr)
    s['trans_modal_2000_4000'] = float(np.mean([r['ext']['transitions']['2000-4000']['modal'] for r in d['recs']]))
    s['trans_support_2000_4000'] = float(np.mean([r['ext']['transitions']['2000-4000']['support'] for r in d['recs']]))
    return s


def summ_insp(d, g='2000'):
    if d is None: return None
    en = np.array([np.mean(r['ext']['isl_eff_net']) for r in d['recs']], float) if g == '2000' else rv(d, 'n_eff_net', g)
    eg = np.array([np.mean(r['ext']['isl_eff_gross']) for r in d['recs']], float) if g == '2000' else rv(d, 'n_eff_gross', g)
    s = dict(net=F.boot(en), gross=F.boot(eg), status=F.status_ge(F.boot(en), F.TH['insp']), n=len(en),
             to0=F.boot(rv(d, 'to0', g)), to1=F.boot(rv(d, 'to1', g)), forf0=F.boot(rv(d, 'forf0', g)), forf1=F.boot(rv(d, 'forf1', g)),
             charge0=F.boot(rv(d, 'charge0', g)), charge1=F.boot(rv(d, 'charge1', g)),
             u0g=F.boot(rv(d, 'n_u0g', g)), u1g=F.boot(rv(d, 'n_u1g', g)), runs=dict(net=en, gross=eg))
    for nm in ('SIMX_I', 'SI100n', 'SI100n~'):
        s['mass0_' + nm] = F.boot(rv(d, 'mass0_' + nm, g)); s['present0_' + nm] = F.boot(rv(d, 'present0_' + nm, g))
        v = np.array([r['ext']['modal0'].get(nm, 0.0) for r in d['recs']], float) if g == '2000' else None
        if v is not None: s['modal0_' + nm] = F.boot(v); s['runs']['modal0_' + nm] = v
    for nm in ('SIMX_E', 'SE100k', 'SE100k~'):
        s['mass1_' + nm] = F.boot(rv(d, 'mass1_' + nm, g)); s['present1_' + nm] = F.boot(rv(d, 'present1_' + nm, g))
        v = np.array([r['ext']['modal1'].get(nm, 0.0) for r in d['recs']], float) if g == '2000' else None
        if v is not None: s['modal1_' + nm] = F.boot(v); s['runs']['modal1_' + nm] = v
    s['runs']['mass0_SIMX_I'] = rv(d, 'mass0_SIMX_I', g); s['runs']['mass0_SI100n'] = rv(d, 'mass0_SI100n', g)
    return s


def summ_pd(d, cap=F.TH['pd_charge']):
    if d is None: return None
    recs = d['recs']
    c = F.pd_counts(recs, cap)
    ch = np.array([F.pd_flags(r)['charge'] for r in recs], float)
    ffe = [r.get('ffe', {}) for r in recs]
    return dict(c=c, status=c['sC'], end_charge=F.boot(ch), max_charge=float(np.nanmax(ch)),
                frozen=F.boot([1.0 if r['frozen_at'] >= 0 else 0.0 for r in recs]), gen=F.boot([r['last_gen'] for r in recs]),
                max_steps=float(np.nanmax([f.get('max_steps', np.nan) for f in ffe])),
                forfeit_weight=float(np.nansum([f.get('forfeit_weight', np.nan) for f in ffe])),
                n_forfeit_runs=int(sum(1 for f in ffe if f.get('forfeit_weight', 0) > 0)), n=len(recs))


def paired(a, b):
    """Paired difference a - b over run indices (the cells share run indices and order)."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    return a - b


def tost(diff, margin=MARGIN, B=4000, seed=20261026):
    """Equivalence of a paired mean difference at the margin: the 90% bootstrap interval inside (-margin, margin) is 'equivalent'; 'different' when the 95%
    interval excludes [-margin, margin] entirely (lower > margin or upper < -margin); else 'unresolved'."""
    d = np.asarray(diff, float); d = d[~np.isnan(d)]
    if len(d) == 0: return dict(mean=np.nan, ci95=(np.nan, np.nan), ci90=(np.nan, np.nan), verdict='n/a')
    idx = np.random.default_rng(seed).integers(len(d), size=(B, len(d)))
    m = d[idx].mean(1)
    ci95 = (float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))); ci90 = (float(np.percentile(m, 5)), float(np.percentile(m, 95)))
    if ci90[0] > -margin and ci90[1] < margin: v = 'equivalent'
    elif ci95[0] > margin or ci95[1] < -margin: v = 'different'
    else: v = 'unresolved'
    return dict(mean=float(d.mean()), ci95=ci95, ci90=ci90, verdict=v)


# ---------------------------------------------------------------------------------------------------------------- classification
CONF_PD = {}


def conf_pd_status(level):
    """PD status carried from the confirmation run's A at the same level (the rule's forfeit charge is zero there)."""
    if level not in CONF_PD:
        d = json.load(open(os.path.join(ROOT, 'runs', 'failure-pricing-confirm.json')))
        for k, v in d['levels'].items():
            CONF_PD[float(k)] = (v['pd']['status'], v['pd']['c']['C'])
    return CONF_PD[level]


def classify_cell(game_stat_rps, game_stat_insp, pd_status):
    sts = [game_stat_rps, game_stat_insp, pd_status]
    return F.classify(sts), sts


def build():
    R = dict(rps={}, insp={}, pd={})
    specs = {}
    for game in ('rps', 'insp'):
        for rule in ('A', 'Af', 'Am'):
            for arm in ('', '+X', '+S'):
                for lv in LEVELS:
                    s = '%s%s@%g' % (rule, arm, lv)
                    d = cell(game, s)
                    if d is None: continue
                    R[game][s] = summ_rps(d) if game == 'rps' else summ_insp(d)
    for lv in (0.1, 1.0):
        d = pdcell(lv)
        if d is not None: R['pd']['Af@%g' % lv] = summ_pd(d)
    return R


def pooled_insp(R, lv):
    """Inspection without X has identical tables under A, A_f and A_m (the merged catalogue has no forfeits): the cells differ only by the
    dynamics seed.  The pooled estimate averages the available rules within each run index (the founders are shared) and bootstraps the runs."""
    arrs = [R['insp']['%s@%g' % (r, lv)]['runs']['net'] for r in ('A', 'Af', 'Am') if '%s@%g' % (r, lv) in R['insp']]
    if not arrs: return None
    m = np.mean(arrs, axis=0)
    t = F.boot(m)
    return dict(net=t, status=F.status_ge(t, F.TH['insp']), n_rules=len(arrs))


def pd_for(R, lv):
    """(status, label) of the PD at a level: this run's A_f cell where run, else carried from the confirmation run's A."""
    k = 'Af@%g' % lv
    if k in R['pd']: return R['pd'][k]['status'], 'this run'
    return conf_pd_status(lv)[0], 'carried from the confirmation run'


# ---------------------------------------------------------------------------------------------------------------- static tables
def static_tables(R):
    out = {}
    b = FP.BaseX('rps')
    names = b.tb.names[0]
    n = b.n_base[0]
    ix = {k: i for i, k in enumerate(names)}
    s, c, t = ix['SIMX'], ix['SIM100u'], ix['SIM100u~']
    Ug = FR.rps_game_payoffs(b.tb.Gt, 'stored'); Um = FR.rps_game_payoffs(b.tb.Gt, 'm')
    rows = []
    for j in range(n):
        o = names[j]
        agree = float((b.tb.Gt[j, s, :3] ** 2).sum()) if b.tb.Gt[j, s, 3] == 0 else float('nan')
        row = dict(opp=o, simx=dict(g=Ug[s, j], gm=Um[s, j], to=b.arrays['n_to'][s, j], forf=b.arrays['forf'][s, j]),
                   cap=dict(g=Ug[c, j], gm=Um[c, j], to=b.arrays['n_to'][c, j], forf=b.arrays['forf'][c, j]),
                   sham=dict(g=Ug[t, j], to=b.arrays['n_to'][t, j]),
                   opp_vs_simx=dict(g=Ug[j, s], to=b.arrays['n_to'][j, s], forf=b.arrays['forf'][j, s]), agree=agree)
        rows.append(row)
    out['rps'] = rows
    # SIMX against SIMX and the exact simulator's net rows at each level and rule
    bi = FP.BaseX('insp')
    n0, n1 = bi.tb.names
    i0 = {k: i for i, k in enumerate(n0)}; i1 = {k: i for i, k in enumerate(n1)}
    UAg, UBg = FR.insp_game_payoffs(bi.tb.G0, bi.tb.G1, 'stored')
    UAm, UBm = FR.insp_game_payoffs(bi.tb.G0, bi.tb.G1, 'm')
    rows0 = []
    for j in range(bi.n_base[1]):
        o = n1[j]
        sx, cp = i0['SIMX_I'], i0['SI100n']
        rows0.append(dict(opp=o, simx=dict(g=UAg[sx, j], gm=UAm[sx, j], to=bi.arr0['n_to'][sx, j], forf=bi.arr0['forf'][sx, j]),
                          cap=dict(g=UAg[cp, j], gm=UAm[cp, j], to=bi.arr0['n_to'][cp, j], forf=bi.arr0['forf'][cp, j])))
    out['insp0'] = rows0
    rows1 = []
    for j in range(bi.n_base[0]):
        o = n0[j]
        sx, cp = i1['SIMX_E'], i1['SE100k']
        rows1.append(dict(opp=o, simx=dict(g=UBg[sx, j], gm=UBm[sx, j], to=bi.arr1['n_to'][sx, j], forf=bi.arr1['forf'][sx, j]),
                          cap=dict(g=UBg[cp, j], gm=UBm[cp, j], to=bi.arr1['n_to'][cp, j], forf=bi.arr1['forf'][cp, j])))
    out['insp1'] = rows1
    return out


# ---------------------------------------------------------------------------------------------------------------- verdicts
def verdicts(R, ST):
    V = []

    def add(key, verdict, detail): V.append(dict(id=key, verdict=verdict, detail=detail))
    g = R['rps']; gi = R['insp']
    # 1
    a3, a1 = g.get('Af@0.3'), g.get('Af@1')
    if a3 and a1:
        if a3['mixing'] == 'met' and a1['mixing'] == 'met': v = 'held'
        elif a3['mixing'] == 'met' and a1['mixing'] == 'undetermined': v = 'partial'
        else: v = 'failed'
        add('1', v, 'by mixing at A_f 0.3: %s (e_gross %s, forfeit %s); at 1: %s (e_gross %s, forfeit %s)' % (
            a3['mixing'], fmt(a3['e_gross']), fmt(a3['forfeit']), a1['mixing'], fmt(a1['e_gross']), fmt(a1['forfeit'])))
    # 2
    det = []; ok = True; anyd = False; stat_ok = True; stat_fail = False
    for lv in (0.03, 0.1):
        f = g.get('Af@%g' % lv); a = g.get('A@%g' % lv); fi = gi.get('Af@%g' % lv); ai = gi.get('A@%g' % lv)
        if not (f and a and fi and ai): continue
        for key in ('e_gross', 'forfeit', 'e_prog'):
            t = tost(paired(f['runs'][key], a['runs'][key]))
            det.append('%g RPS %s: %s' % (lv, key, '%s mean %.4f 90%% [%.4f, %.4f]' % (t['verdict'], t['mean'], t['ci90'][0], t['ci90'][1])))
            ok &= t['verdict'] == 'equivalent'; anyd |= t['verdict'] == 'different'
        t = tost(paired(fi['runs']['net'], ai['runs']['net']))
        det.append('%g insp net: %s mean %.4f 90%% [%.4f, %.4f]' % (lv, t['verdict'], t['mean'], t['ci90'][0], t['ci90'][1]))
        ok &= t['verdict'] == 'equivalent'; anyd |= t['verdict'] == 'different'
        stat_ok &= (f['mixing'] == 'met')
        stat_fail |= (f['mixing'] == 'failed') or (fi['status'] == 'failed')
        if lv == 0.1: stat_ok &= (fi['status'] == 'met')
    if det:
        v = 'held' if (ok and stat_ok) else ('partial' if (not anyd and not stat_fail) else 'failed')
        add('2', v, '; '.join(det) + '; statuses ok: %s' % stat_ok)
    # 3
    a10 = g.get('Af@10')
    if a10:
        up = a10['forfeit'][2]
        if up <= 0.05 and a10['mixing'] != 'failed': v = 'held'
        elif a10['forfeit'][0] <= 0.05 and a10['mixing'] != 'failed': v = 'partial'
        else: v = 'failed'
        add('3', v, 'A_f 10: by mixing %s, forfeit %s, e_gross %s' % (a10['mixing'], fmt(a10['forfeit']), fmt(a10['e_gross'])))
    # 4
    shares = {}
    for lv in LEVELS:
        x = g.get('Af+X@%g' % lv)
        if x: shares[lv] = x['modal_SIMX']
    if shares:
        v = 'held' if all(s[0] < 0.05 for s in shares.values()) else 'failed'
        add('4', v, 'SIMX modal share under A_f + X: ' + '; '.join('%g: %s' % (lv, fmt(s)) for lv, s in shares.items()))
    # 5
    det5 = []; a_ok = True; any_lv = False
    for lv in LEVELS:
        x = gi.get('Af+X@%g' % lv); n = gi.get('Af@%g' % lv)
        if not (x and n): continue
        d = float(np.mean(paired(x['runs']['net'], n['runs']['net'])))
        det5.append('%g: net with X %.3f, without %.3f, diff %+.3f' % (lv, x['net'][0], n['net'][0], d))
        a_ok &= abs(d) <= 0.10; any_lv = True
    x01 = gi.get('Af+X@0.1')
    if any_lv and x01:
        share = x01['modal0_SIMX_I']
        b_ok = share[0] >= 0.1
        v = 'held' if (a_ok and b_ok) else ('partial' if (a_ok or b_ok) else 'failed')
        # counter-predictions
        s01 = gi.get('Af+S@0.1')
        cap_better = 0.0
        for r0 in ST['insp0']:
            d = (r0['simx']['g'] - 0.1 * (r0['simx']['to'] + r0['simx']['forf'])) - (r0['cap']['g'] - 0.1 * (r0['cap']['to'] + r0['cap']['forf']))
            cap_better = max(cap_better, d)
        counter_g = (not b_ok) and cap_better <= 0.05
        sup = None
        if s01 is not None:
            sh_clone = s01.get('modal0_SI100n~', (0, 0, 0))[0]
            sup = abs(share[0] - sh_clone) > 0.03
        add('5', v, '; '.join(det5) + '; SIMX_I modal share at 0.1: %s; max paired static advantage of SIMX_I over SI100n against an inspectee class at P=0.1 (A_f): %+.3f' % (fmt(share), cap_better))
        add('5c-gemini', 'held' if counter_g else 'failed', 'modal share < 0.1: %s; no class where SIMX_I beats SI100n by more than 0.05: %s' % (not b_ok, cap_better <= 0.05))
        if sup is not None:
            add('5c-gpt', 'supported' if sup else 'not supported', 'modal share SIMX_I (A_f+X) %.3f against its counterpart-clone share in the sham cell %.3f' % (share[0], sh_clone))
    # 6
    det6 = []; ok6 = True; counter6 = False; any6 = False
    for lv, ref in ((0.1, 37), (1.0, 36)):
        p = R['pd'].get('Af@%g' % lv)
        if not p: continue
        any6 = True
        k = p['c']['C']
        det6.append('%g: C %s, status %s (confirmation A: %d/40), max steps %.0f, forfeit runs %d' % (lv, fc(k, p['n']), p['status'], ref, p['max_steps'], p['n_forfeit_runs']))
        ok6 &= (p['status'] == 'met' and abs(k - ref) <= 6)
        counter6 |= abs(k - ref) > 3
    if any6:
        add('6', 'held' if ok6 else 'failed', '; '.join(det6))
        add('6c-gpt', 'held' if counter6 else 'failed', 'a count more than 3 from the confirmation run at some level: %s' % counter6)
    # 9
    det9 = []; allnox = True; allx = True
    for lv in (0.1, 0.3, 1.0, 10.0):
        m = g.get('Am@%g' % lv); mx = g.get('Am+X@%g' % lv)
        if m:
            det9.append('%g no-X %s' % (lv, fmt(m['forfeit']))); allnox &= m['forfeit'][0] < 0.05
        if mx:
            det9.append('%g X %s' % (lv, fmt(mx['forfeit']))); allx &= mx['forfeit'][0] < 0.05
    if det9:
        v = 'held' if (allnox and allx) else ('partial' if (allnox or allx) else 'failed')
        add('9', v, 'fallback share A_m: ' + '; '.join(det9))
        m1 = g.get('Am@0.1'); mx1 = g.get('Am+X@0.1')
        c9 = any(s is not None and s['forfeit'][0] >= 0.05 for s in (m1, mx1))
        add('9c-gpt', 'held' if c9 else 'failed', 'fallback share >= 0.05 at 0.1 in some arm: %s' % c9)
    # 10
    det10 = []; st_eq = True; ec_ok = True; ec_part = 0; stat_diff = 0
    for lv in LEVELS:
        for arm in ('', '+X'):
            a = g.get('Am%s@%g' % (arm, lv)); f = g.get('Af%s@%g' % (arm, lv))
            if not (a and f): continue
            if a['mixing'] != f['mixing']: st_eq = False; stat_diff += 1
            ea, ef = a['e_comp'][0], f['e_comp'][0]
            d = abs(ea - ef) if not (np.isnan(ea) or np.isnan(ef)) else None
            det10.append('%g%s: by mixing %s/%s, e_comp %.4f/%.4f' % (lv, arm, a['mixing'], f['mixing'], ea, ef))
            if d is not None and d > 0.05: ec_ok = False; ec_part += 1
    for lv in (0.1, 1.0):
        a = gi.get('Am@%g' % lv); f = gi.get('Af@%g' % lv)
        if a and f:
            det10.append('insp %g: %s/%s' % (lv, a['status'], f['status']))
            if a['status'] != f['status']: st_eq = False; stat_diff += 1
    if det10:
        if st_eq and ec_ok: v = 'held'
        elif (st_eq and ec_part <= 1) or stat_diff <= 1: v = 'partial'
        else: v = 'failed'
        add('10', v, '; '.join(det10))
        add('10c-gpt', 'held' if not st_eq else 'failed', 'some status differs: %s' % (not st_eq))
    # 11
    a_ = g.get('Am+X@0.1'); f_ = g.get('Af+X@0.1')
    if a_ and f_:
        ma, mf = a_['mass_SIMX'][0], f_['mass_SIMX'][0]
        ratio = ma / mf if mf > 0 else float('nan')
        v = 'held' if (mf > 0 and ratio >= 2) else ('held' if (mf == 0 and ma > 0) else 'failed')
        ra = a_['runs']['mass_SIMX']; rf = f_['runs']['mass_SIMX']
        idx = np.random.default_rng(20261026).integers(len(ra), size=(4000, len(ra)))
        with np.errstate(divide='ignore', invalid='ignore'):
            rat = ra[idx].mean(1) / rf[idx].mean(1)
        rat = rat[np.isfinite(rat)]
        ci = (float(np.percentile(rat, 2.5)), float(np.percentile(rat, 97.5))) if len(rat) else (np.nan, np.nan)
        add('11', v, 'SIMX mass at 0.1: A_m %.5f, A_f %.5f, ratio %.2f, 95%% interval of the ratio of paired means [%.2f, %.2f]' % (ma, mf, ratio, ci[0], ci[1]))
        add('11c-gemini', 'held' if (len(rat) and ci[0] <= 1 <= ci[1]) else 'failed', 'the interval of the ratio contains 1: %s (A_f mass %.5f, A_m mass %.5f, founder mass 0.00095: %s)' % (len(rat) > 0 and ci[0] <= 1 <= ci[1], mf, ma, 'A_m above the founder floor, A_f below it' if (ma > 0.00095 and mf < 0.00095) else 'both near the floor'))
    return V


def eng_verdicts(R, ST):
    V = []

    def add(key, verdict, detail): V.append(dict(id=key, verdict=verdict, detail=detail))
    g = R['rps']; gi = R['insp']
    # E1
    det = []; ok = True
    for lv in (1.0, 10.0):
        f = g.get('Af@%g' % lv); a = g.get('A@%g' % lv)
        if f and a:
            det.append('%g: PB modal A_f %s, A %s' % (lv, fmt(f['modal_PB']), fmt(a['modal_PB'])))
            ok &= (f['modal_PB'][0] <= 0.05)
            if lv == 1.0: ok &= (a['modal_PB'][0] >= 0.4)
    if det: add('E1', 'held' if ok else 'failed', '; '.join(det))
    # E2
    det = []; ok = True
    for lv in (1.0, 10.0):
        f = g.get('Af@%g' % lv)
        if f:
            det.append('%g: U modal %s, PRR modal %s' % (lv, fmt(f['modal_U']), fmt(f['modal_PRR'])))
            ok &= (f['modal_U'][0] >= 0.6 and f['modal_PRR'][0] < 0.15)
    if det: add('E2', 'held' if ok else 'failed', '; '.join(det))
    # E3
    det = []; ok = True
    for lv, allowed in ((0.03, ('met', 'undetermined')), (0.1, ('met', 'undetermined')), (0.3, ('undetermined',)), (1.0, ('failed',)), (10.0, ('failed',))):
        a = g.get('A@%g' % lv)
        if a:
            det.append('%g: %s' % (lv, a['mixing']))
            if lv in (0.03, 0.1): ok &= a['mixing'] in allowed
            elif lv == 0.3: ok &= a['mixing'] in ('undetermined', 'met', 'failed') and a['mixing'] != 'met' or a['mixing'] == 'undetermined'
            else: ok &= a['mixing'] == 'failed'
    if det: add('E3', 'held' if ok else 'failed', 'concurrent A by mixing: ' + '; '.join(det))
    # E4
    det = []; ok = True
    for lv in (0.03, 0.1):
        for rule in ('A', 'Af'):
            s = g.get('%s@%g' % (rule, lv))
            if s: det.append('%s %g: %.5f' % (rule, lv, s['forfeit'][0])); ok &= s['forfeit'][0] < 0.002
    if det: add('E4', 'held' if ok else 'failed', '; '.join(det))
    # E5
    det = []; ok = True
    for lv in LEVELS:
        for rule in ('Af', 'Am', 'A'):
            s = g.get('%s+X@%g' % (rule, lv))
            if s:
                det.append('%s %g: mass %.5f present %.3f' % (rule, lv, s['mass_SIMX'][0], s['present_SIMX'][0]))
                ok &= (s['mass_SIMX'][0] < 0.002)
                if lv >= 0.1: ok &= (s['present_SIMX'][0] < 0.10)
    if det: add('E5', 'held' if ok else 'failed', '; '.join(det))
    # E6
    det = []; ok = True
    for lv in (0.1, 1.0):
        for rule in ('Af', 'A'):
            x = gi.get('%s+X@%g' % (rule, lv)); n = gi.get('%s@%g' % (rule, lv))
            if x and n:
                d = float(np.mean(paired(x['runs']['net'], n['runs']['net'])))
                det.append('%s %g: diff %+.3f, mass SIMX_I %.5f vs SI100n %.5f' % (rule, lv, d, x['mass0_SIMX_I'][0], x['mass0_SI100n'][0]))
                ok &= abs(d) <= 0.10 and x['mass0_SIMX_I'][0] < x['mass0_SI100n'][0]
    if det: add('E6', 'held' if ok else 'failed', '; '.join(det))
    # E7
    det = []; ok = True
    for lv in (0.1, 1.0):
        s = g.get('Af+S@%g' % lv); n = g.get('Af@%g' % lv); si = gi.get('Af+S@%g' % lv); ni = gi.get('Af@%g' % lv)
        if s and n:
            for key in ('e_gross', 'forfeit'):
                d = float(np.mean(paired(s['runs'][key], n['runs'][key]))); det.append('%g RPS %s %+.4f' % (lv, key, d)); ok &= abs(d) <= 0.05
        if si and ni:
            d = float(np.mean(paired(si['runs']['net'], ni['runs']['net']))); det.append('%g insp net %+.4f' % (lv, d)); ok &= abs(d) <= 0.05
    if det: add('E7', 'held' if ok else 'failed', '; '.join(det))
    # E8
    det = []; ok = True
    for lv in (0.1, 1.0):
        c = {r: gi.get('%s@%g' % (r, lv)) for r in ('A', 'Af', 'Am')}
        if all(c.values()):
            pairs = [('A', 'Af'), ('A', 'Am'), ('Af', 'Am')]
            for a, b in pairs:
                d = float(np.mean(paired(c[a]['runs']['net'], c[b]['runs']['net'])))
                det.append('%g %s-%s %+.4f' % (lv, a, b, d)); ok &= abs(d) <= 0.06
    if det: add('E8', 'held' if ok else 'failed', '; '.join(det))
    # E9
    det = []; ok = True
    for lv in LEVELS:
        a = g.get('Am@%g' % lv); f = g.get('Af@%g' % lv)
        if a and f:
            d1 = abs(a['e_comp'][0] - f['e_comp'][0]); d2 = abs(a['forfeit'][0] - f['forfeit'][0])
            det.append('%g: e_comp %.4f, fallback %.4f' % (lv, d1, d2)); ok &= (d1 <= 0.02 and d2 <= 0.02)
    if det: add('E9', 'held' if ok else 'failed', 'A_m against A_f without X: ' + '; '.join(det))
    # E10
    det = []; ok = True
    for lv in (0.1, 1.0):
        p = R['pd'].get('Af@%g' % lv)
        if p:
            det.append('%g: C %d/%d, forfeit runs %d, max steps %.0f' % (lv, p['c']['C'], p['n'], p['n_forfeit_runs'], p['max_steps']))
            ok &= (34 <= p['c']['C'] <= 40 and p['n_forfeit_runs'] == 0)
    if det: add('E10', 'held' if ok else 'failed', '; '.join(det))
    # E12
    det = []; ok = True
    for lv in (1.0, 10.0):
        a = g.get('Am@%g' % lv); f = g.get('Af@%g' % lv)
        if a and f:
            d1 = abs(a['coin_mass'][0] - f['coin_mass'][0]); d2 = a['forfeit'][0] - f['forfeit'][0]
            det.append('%g: coin mass A_m %.3f A_f %.3f, fallback excess %+.4f' % (lv, a['coin_mass'][0], f['coin_mass'][0], d2)); ok &= (d1 <= 0.10 and d2 <= 0.02)
    if det: add('E12', 'held' if ok else 'failed', '; '.join(det))
    return V


# ---------------------------------------------------------------------------------------------------------------- tables
def band_table(R):
    g = R['rps']; gi = R['insp']
    rows = []
    for lv in LEVELS:
        for rule, arm in (('A', ''), ('Af', ''), ('Af', '+X'), ('Am', ''), ('Am', '+X'), ('Af', '+S'), ('A', '+X')):
            k = '%s%s@%g' % (rule, arm, lv)
            s = g.get(k); si = gi.get(k)
            if s is None and si is None: continue
            pds, pdl = pd_for(R, lv)
            cl = F.classify([s['status'] if s else 'incomplete', si['status'] if si else 'incomplete', pds]) if (arm == '' and s and si) else '-'
            rows.append([k, fmt(s['e_prog']) if s else '-', fmt(s['e_gross']) if s else '-', fmt(s['e_comp']) if s else '-',
                         fmt(s['forfeit']) if s else '-', s['mixing'] if s else '-', ('%.2f' % s['modal_PRR'][0]) if s else '-',
                         ('%.2f' % s['modal_U'][0]) if s else '-', ('%.2f' % s['modal_PB'][0]) if s else '-',
                         ('%.3f' % s['modal_SIMX'][0]) if s else '-', fmt(si['net']) if si else '-', si['status'] if si else '-',
                         pds if arm == '' and rule != 'Am' else '-', cl])
    return table(['cell', 'RPS e_prog (net)', 'e_gross (policy)', 'e_comp (completed)', 'forfeit / fallback share', 'by mixing', 'PRR modal', 'U modal', 'PB modal',
                  'SIMX modal', 'insp net eff', 'insp', 'PD (this run or carried)', 'classification'], rows)


def exact_table(R):
    g = R['rps']
    rows = []
    for k in sorted(g, key=lambda s: (float(s.split('@')[1]), s)):
        if '+X' not in k and '+S' not in k: continue
        s = g[k]
        rows.append([k, '%.5f' % s['mass_SIMX'][0], '%.5f' % s['mass_SIM100u'][0], '%.5f' % s['mass_SIM100u~'][0], '%.3f' % s['present_SIMX'][0],
                     '%.3f' % s['modal_SIMX'][0], '%.3f' % s['modal_SIM100u~'][0], '%.3f' % s['modal_SIM100u'][0]])
    t1 = table(['cell', 'mass SIMX', 'mass SIM100u', 'mass SIM100u~', 'islands with SIMX present', 'SIMX modal', 'SIM100u~ modal', 'SIM100u modal'], rows)
    gi = R['insp']
    rows = []
    for k in sorted(gi, key=lambda s: (float(s.split('@')[1]), s)):
        if '+X' not in k and '+S' not in k: continue
        s = gi[k]
        rows.append([k, '%.5f' % s['mass0_SIMX_I'][0], '%.5f' % s['mass0_SI100n'][0], '%.5f' % s['mass0_SI100n~'][0], '%.3f' % s['present0_SIMX_I'][0],
                     '%.3f' % s['modal0_SIMX_I'][0], '%.5f' % s['mass1_SIMX_E'][0], '%.5f' % s['mass1_SE100k'][0], '%.3f' % s['present1_SIMX_E'][0],
                     '%.3f' % s['modal1_SIMX_E'][0]])
    t2 = table(['cell', 'mass SIMX_I', 'mass SI100n', 'mass SI100n~', 'SIMX_I present', 'SIMX_I modal', 'mass SIMX_E', 'mass SE100k', 'SIMX_E present', 'SIMX_E modal'], rows)
    return t1, t2


def plays_table():
    """The exact simulators' plays and forfeits by opponent family, pooled over the cells' runs (weighted by SIMX mass)."""
    rows = []
    for spec in sorted([os.path.basename(p) for p in glob.glob(os.path.join(OUT, 'rps_*+X_*.json.gz'))]):
        d = load(os.path.join(OUT, spec))
        W = 0.0; fin = fo = tp = 0.0; fam = {}
        for r in d['recs']:
            sp_ = r['ext']['simx_plays']
            w = sp_['weight']
            if w <= 0: continue
            W += w; fin += w * sp_['finished']; fo += w * sp_['forfeit']; tp += w * sp_['tape']
            for k, v in sp_['forfeit_by_family'].items(): fam[k] = fam.get(k, 0.0) + w * v
        if W > 0:
            rows.append([spec.replace('.json.gz', ''), '%.4f' % W, '%.3f' % (fin / W), '%.3f' % (fo / W), '%.3f' % (tp / W),
                         ', '.join('%s %.3f' % (k, v / W) for k, v in fam.items() if v > 0) or '-'])
        else:
            rows.append([spec.replace('.json.gz', ''), '0', '-', '-', '-', '-'])
    return table(['cell', 'SIMX weight (sum of island masses)', 'plays: exact read finished', 'forfeit (read ran out)', 'a private tape inside the read', 'forfeit by opponent family'], rows)


def conditional_rps():
    """Islands that were founded with at least one exact simulator (or its twin, in the sham cells): how often is it present at 2,000, modal, and its mass
    against the founders' mass (recomputed from the deterministic founders of each run).  Pooled over the runs of each cell."""
    b = FP.BaseX('rps')
    names = b.tb.names[0]
    ix = {k: i for i, k in enumerate(names)}
    rows = []
    for path in sorted(glob.glob(os.path.join(OUT, 'rps_*+[XS]_*_primary.json.gz'))):
        d = load(path)
        arm = d['meta']['arm']
        twin = 'SIMX' if arm == 'X' else 'SIM100u~'
        nf = pres = mod = 0; fm = em = 0.0; cnt = 0
        for r in d['recs']:
            init = FR.founders_arm(b, 'rps', 'primary', r['run'], 100, 64, arm)[0][:, ix[twin]]
            fin = np.array(r['ext']['x_counts'][twin])
            dom = np.array(r['ext']['dom']['2000'])
            f = init > 0
            nf += int(f.sum()); pres += int((fin[f] > 0).sum()); mod += int((dom[f] == ix[twin]).sum())
            fm += float(init[f].sum()) / 100.0; em += float(fin[f].sum()) / 100.0
        rows.append([os.path.basename(path).replace('.json.gz', ''), twin, nf, '%.3f' % (pres / nf) if nf else '-', '%.3f' % (mod / nf) if nf else '-',
                     '%.3f' % (fm / nf) if nf else '-', '%.3f' % (em / nf) if nf else '-'])
    return table(['cell', 'twin', 'islands founded with it', 'present at 2,000', 'modal at 2,000', 'mean founder mass (founded islands)', 'mean mass at 2,000'], rows)


def charge_table(R):
    g = R['rps']
    rows = []
    for lv in LEVELS:
        for rule in ('A', 'Af', 'Am'):
            for arm in ('', '+X'):
                s = g.get('%s%s@%g' % (rule, arm, lv))
                if not s: continue
                rows.append(['%s%s@%g' % (rule, arm, lv), fmt(s['to_play'], 4), fmt(s['forf_play'], 4), fmt(s['charge_play'], 4)])
    return table(['cell', 'timed-out capped reads per play', 'forfeits per play', 'charge per play'], rows)


def static_table(ST):
    rows = []
    for r in ST['rps']:
        s, c = r['simx'], r['cap']
        rows.append([r['opp'], '%+.3f' % s['g'], '%.0f' % s['to'], '%.0f' % s['forf'], '%+.3f' % c['g'], '%.0f' % c['to'], '%+.3f' % (r['opp_vs_simx']['g']),
                     '%+.3f / %+.3f' % (s['g'] - 0.1 * (s['to'] + s['forf']) - (c['g'] - 0.1 * (c['to'] + c['forf'])), s['g'] - 1.0 * (s['to'] + s['forf']) - (c['g'] - 1.0 * (c['to'] + c['forf']))),
                     '%+.3f' % (s['gm'] - 0.1 * (s['to'] + s['forf'])), ('%.3f' % r['agree']) if not np.isnan(r['agree']) else 'forfeit'])
    t = table(['opponent', 'SIMX gross (A, A_f)', 'timeouts', 'forfeit', 'SIM100u gross', 'timeouts', 'opponent gross vs SIMX', 'SIMX - SIM100u net (A_f) at 0.1 / 1', 'SIMX net A_m at 0.1',
               'predictability of the opponent (agreement of two draws)'], rows)
    out = [t]
    for key, label, a, b in (('insp0', 'SIMX_I against SI100n (inspector payoffs, by inspectee class)', 'SIMX_I', 'SI100n'),
                              ('insp1', 'SIMX_E against SE100k (inspectee payoffs, by inspector class)', 'SIMX_E', 'SE100k')):
        rows = []
        for r in ST[key]:
            s, c = r['simx'], r['cap']
            rows.append([r['opp'], '%+.3f' % s['g'], '%.0f' % s['to'], '%.0f' % s['forf'], '%+.3f' % c['g'], '%.0f' % c['to'], '%.0f' % c['forf'],
                         '%+.3f / %+.3f' % (s['g'] - 0.1 * (s['to'] + s['forf']) - (c['g'] - 0.1 * (c['to'] + c['forf'])), s['g'] - 1.0 * (s['to'] + s['forf']) - (c['g'] - 1.0 * (c['to'] + c['forf']))),
                         '%+.3f' % (s['gm'] - 0.1 * (s['to'] + s['forf']))])
        out.append('\n**%s**\n\n' % label + table(['opponent', a + ' gross (A, A_f)', 'timeouts', 'forfeit', b + ' gross', 'timeouts', 'forfeit', 'net (A_f) difference at 0.1 / 1', a + ' net A_m at 0.1'], rows))
    return '\n'.join(out)


def nearby_K():
    p = os.path.join(OUT, 'static_K.json')
    if not os.path.exists(p): return 'not run\n'
    d = json.load(open(p))
    Ks = sorted(d, key=int)
    rows = []
    # compare law and events across budgets
    def sig(r):
        return (tuple(sorted((k, round(v, 6)) for k, v in r['dist'].items())), round(r['forf'], 6), round(r['n_to'], 6), round(r['n_uto'], 6))
    for sect in ('rps', 'insp0', 'insp1'):
        names = d[Ks[0]][sect].keys()
        for nm in names:
            sigs = []
            for K in Ks:
                e = d[K][sect].get(nm)
                if e is None: sigs.append(None); continue
                sigs.append(sig(e['x']))
            same = all(s == sigs[0] for s in sigs)
            e0 = d[Ks[0]][sect][nm]['x']
            rows.append([sect, nm, 'same' if same else 'DIFFERS', '%s' % e0['dist'], 'forf %.0f, capped TO %.0f' % (e0['forf'], e0['n_to']),
                         '; '.join('K%s: %.0f steps' % (K, d[K][sect][nm]['x']['steps']) for K in Ks if nm in d[K][sect])])
    return table(['pair set', 'opponent', 'law and events across K', 'play law (first K)', 'events', 'steps'], rows)


def supp_inspection():
    """Supplementary inspection runs (indices 340-419, files tagged _ext) pooled with the registered 300-339: 120 runs per cell.  The run-level
    efficient fraction is nearly binary (the 64 islands with migration mostly end in one state), so 40 runs cannot resolve differences of 0.1-0.2."""
    rows = []; out = {}
    for lv in (0.03, 0.1, 0.3, 1.0, 10.0):
        vals = {}
        for arm in ('', '+X', '+S'):
            name = FR.spec_name('insp', 'Af', {'': 'none', '+X': 'X', '+S': 'sham'}[arm], lv)
            a = load(os.path.join(OUT, name + '.json.gz')); b = load(os.path.join(OUT, name + '_ext.json.gz'))
            if a is None or b is None: continue
            recs = a['recs'] + b['recs']
            vals[arm] = dict(net=np.array([np.mean(r['ext']['isl_eff_net']) for r in recs], float),
                             mass=np.array([r['stats']['2000']['mass0_SIMX_I'] for r in recs], float),
                             massc=np.array([r['stats']['2000']['mass0_SI100n'] for r in recs], float),
                             massS=np.array([r['stats']['2000']['mass0_SI100n~'] for r in recs], float))
        if '' not in vals: continue
        row = ['%g' % lv, fmt(F.boot(vals['']['net'])) + ' ' + F.status_ge(F.boot(vals['']['net']), 0.60)]
        out[lv] = dict(none=F.boot(vals['']['net']))
        for arm, lab in (('+X', 'X'), ('+S', 'sham')):
            if arm in vals:
                d = vals[arm]['net'] - vals['']['net']
                row.append(fmt(F.boot(vals[arm]['net'])) + ' ' + F.status_ge(F.boot(vals[arm]['net']), 0.60)); row.append(fmt(F.boot(d)))
                out[lv][lab] = F.boot(vals[arm]['net']); out[lv][lab + '-none'] = F.boot(d)
            else:
                row += ['-', '-']
        if '+X' in vals and '+S' in vals:
            d = vals['+X']['net'] - vals['+S']['net']; row.append(fmt(F.boot(d))); out[lv]['X-sham'] = F.boot(d)
        else: row.append('-')
        row.append('%.3f / %.3f' % (vals['+X']['mass'].mean(), vals['+X']['massc'].mean()) if '+X' in vals else '-')
        rows.append(row)
    return table(['level', 'A_f no X (120 runs)', 'A_f + X', 'X - none (paired)', 'A_f + sham', 'sham - none (paired)', 'X - sham (paired)', 'mass SIMX_I / SI100n in the X cell'], rows), out


def txt(path, default=''):
    p = os.path.join(OUT, path)
    return open(p).read() if os.path.exists(p) else default


def main():
    R = build()
    ST = static_tables(R)
    V = verdicts(R, ST); E = eng_verdicts(R, ST)
    head = ['# Forfeit pricing, exact simulators and the security fallback (run report, 2026-10-26)', '',
            'Spec `specs/2026-10-26-forfeit-pricing.md`; notes `notes/forfeit-pricing.md`; predictions `predictions/2026-10-26-forfeit-pricing.md`. LOTTERY objects at fixed geometry '
            '(N, I) = (100, 64), generation 2,000 (4,000 secondary), fresh run indices only (L_T runs 300-339, PD reps 300-339), world K. Never pi; finite-size mechanism test, no '
            'large-population or limit claim. Intervals: run-clustered percentile bootstrap (means), Wilson (PD counts); equivalence: 90% bootstrap interval inside +-0.05 (two one-sided tests).', '']
    out = head
    out.append('## Cells present\n')
    cells = []
    for game in ('rps', 'insp'):
        cells.append('%s: %s' % (game, ', '.join(sorted(R[game], key=lambda s: (float(s.split('@')[1]), s)))))
    cells.append('pd: %s' % ', '.join(sorted(R['pd'])))
    out.append('\n'.join('- ' + c for c in cells) + '\n')
    out.append('## Band table (RPS, inspection, PD; (100, 64))\n')
    out.append(band_table(R))
    out.append('PD statuses at 0.03, 0.3 and 10 are carried from the confirmation run (the PD has no forfeits, `ffe` recorder); inspection is run under every rule.\n')
    out.append('## Classification of A_f at each level\n')
    rows = []
    for lv in LEVELS:
        s = R['rps'].get('Af@%g' % lv); si = R['insp'].get('Af@%g' % lv)
        if not (s and si): continue
        pds, pdl = pd_for(R, lv)
        cl, sts = classify_cell(s['status'], si['status'], pds)
        pi = pooled_insp(R, lv)
        cl2 = F.classify([s['status'], pi['status'], pds]) if pi else '-'
        rows.append(['%g' % lv, s['net'], s['mixing'], si['status'] + ' ' + fmt(si['net']), '%s (%s)' % (pds, pdl), cl,
                     ('%s %s (%d rules)' % (pi['status'], fmt(pi['net']), pi['n_rules'])) if pi else '-', cl2])
    out.append(table(['level', 'RPS net', 'RPS by mixing', 'inspection (the A_f cell)', 'PD', 'A_f classification (registered: the cell)', 'inspection pooled over rules with identical tables', 'classification with the pooled inspection'], rows))
    rows = []
    for lv in LEVELS:
        s = R['rps'].get('A@%g' % lv); si = R['insp'].get('A@%g' % lv)
        if not (s and si): continue
        pds, pdl = pd_for(R, lv)
        cl, sts = classify_cell(s['status'], si['status'], pds)
        rows.append(['%g' % lv, s['net'], s['mixing'], si['status'], '%s (%s)' % (pds, pdl), cl])
    out.append('Concurrent A (forfeits free, fresh runs 300-339):\n\n' + table(['level', 'RPS net', 'RPS by mixing', 'inspection', 'PD', 'A classification'], rows))
    rows = []
    for lv in LEVELS:
        for arm in ('', '+X'):
            s = R['rps'].get('Am%s@%g' % (arm, lv))
            if s: rows.append(['Am%s@%g' % (arm, lv), s['net'], s['mixing'], fmt(s['forfeit']), fmt(s['e_comp'])])
    out.append('A_m (RPS only for the full set; inspection is reported in the band table):\n\n' + table(['cell', 'RPS net', 'by mixing', 'fallback share', 'e_comp'], rows))
    out.append('## Verdicts (predictions/2026-10-26-forfeit-pricing.md)\n')
    out.append(table(['#', 'verdict', 'detail'], [[v['id'], '**%s**' % v['verdict'], v['detail']] for v in V]))
    out.append('Engineer\'s predictions:\n\n' + table(['#', 'verdict', 'detail'], [[v['id'], '**%s**' % v['verdict'], v['detail']] for v in E]))
    out.append('## Exact simulators: mass, presence, modal share (RPS)\n')
    t1, t2 = exact_table(R)
    out.append(t1)
    out.append('Inspection:\n\n' + t2)
    out.append('The exact simulator\'s plays (SIMX holders, RPS): finished / forfeit / private tape inside the read, and the forfeit by opponent family:\n\n' + plays_table())
    out.append('Conditional on being founded (RPS; the exact simulator against its sham twin where the cell has one):\n\n' + conditional_rps())
    st_, supp = supp_inspection()
    out.append('## Supplementary inspection runs (indices 340-419 pooled with 300-339, 120 runs per cell)\n')
    out.append(st_)
    out.append('## Charge per play, split into timed-out capped reads and forfeits (RPS)\n')
    out.append(charge_table(R))
    out.append('## Static paired payoffs: exact against capped simulators, by opponent class\n')
    out.append(static_table(ST))
    out.append('## Recursive reader pairs at nearby fuel budgets (K = 9,000 / 10,000 / 11,000)\n')
    out.append(nearby_K())
    out.append('## Support and transitions (RPS, share of islands whose modal programme changed)\n')
    rows = []
    for k in sorted(R['rps'], key=lambda s: (float(s.split('@')[1]), s)):
        s = R['rps'][k]
        rows.append([k, '%.3f' % s['trans_modal_1500_2000'], '%.3f' % s['trans_modal_2000_4000'], '%.3f' % s['trans_support_2000_4000']])
    out.append(table(['cell', 'modal changes 1500-2000', '2000-4000', 'support changes 2000-4000'], rows))
    out.append('## Secondary: generation 4,000 (RPS by mixing, inspection net)\n')
    rows = []
    for k in sorted(R['rps'], key=lambda s: (float(s.split('@')[1]), s)):
        d = cell('rps', k); s4 = summ_rps(d, '4000')
        ki = R['insp'].get(k)
        i4 = summ_insp(cell('insp', k), '4000') if ki else None
        rows.append([k, s4['mixing'], fmt(s4['e_gross']), fmt(s4['forfeit']), (i4['status'] + ' ' + fmt(i4['net'])) if i4 else '-'])
    out.append(table(['cell', 'RPS by mixing (4000)', 'e_gross', 'forfeit share', 'insp net (4000)'], rows))
    out.append('## PD (A_f; the recorder of maximum encounter steps)\n')
    rows = []
    for k, p in sorted(R['pd'].items()):
        rows.append([k, fc(p['c']['C'], p['n']), p['status'], p['c']['censored'], '%.5f' % p['max_charge'], '%.0f' % p['max_steps'], p['n_forfeit_runs'], '%.3g' % p['forfeit_weight']])
    out.append(table(['cell', 'cost-inclusive count (C)', 'status', 'censored runs', 'max end-state charge/play', 'max encounter steps', 'runs with a forfeit', 'forfeit weight'], rows))
    out.append('## Deviations, crashes, retries, cuts\n')
    out.append(txt('deviations.md', '(none recorded yet)\n'))
    open(os.path.join(ROOT, 'runs', 'forfeit-pricing.md'), 'w').write('\n'.join(out))

    def clean(o):
        if isinstance(o, dict): return {k: clean(v) for k, v in o.items() if k != 'runs'}
        if isinstance(o, (list, tuple)): return [clean(x) for x in o]
        if isinstance(o, (np.floating, np.integer)): return float(o)
        return o
    json.dump(dict(verdicts=V, eng_verdicts=E, supplementary_inspection=clean(supp), summaries=clean(R)), open(os.path.join(ROOT, 'runs', 'forfeit-pricing.json'), 'w'), indent=1, default=str)
    print('written; verdicts:', [(v['id'], v['verdict']) for v in V], [(v['id'], v['verdict']) for v in E])


if __name__ == '__main__':
    main()
