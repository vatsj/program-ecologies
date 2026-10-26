"""Report for the failure-pricing confirmation: runs/failure-pricing-confirm.md and .json from runs/failure_pricing_confirm/.

LOTTERY objects at fixed geometry (RPS, inspection: N = 100 per role, I = 64, mN = 1, 40 fresh runs 100-139, generation 2,000, plus
(400, 16); PD: world K, S-nonself, (100, 64), 40 fresh reps 200-239, up to 10,000 generations), never pi.  Scores and the
classification: notes/failure-pricing-confirm.md section 1, predictions/2026-10-25-failure-pricing-confirm.md.
Intervals: run-clustered bootstrap (4,000 resamples) for means, Wilson for run counts.
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

ROOT = F.ROOT
OUT = F.OUT
OLD = os.path.join(ROOT, 'runs', 'pricing_rules')
LEVELS = [0.03, 0.1, 0.3, 1.0, 10.0]
_c = {}


def load(path):
    if path not in _c:
        _c[path] = json.load(gzip.open(path, 'rt')) if os.path.exists(path) else None
    return _c[path]


def lt_cell(game, rule, level, cell='primary'):
    return load(os.path.join(OUT, '%s_%s_%g_%s.json.gz' % (game, rule, level, cell)))


def pd_cell(rule, level):
    return load(os.path.join(OUT, 'pd_%s_%g.json.gz' % (rule, level)))


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


# ---------------------------------------------------------------------------------------------------------------- summaries
def runv(d, key, g='2000'):
    return np.array([r['stats'][g][key] for r in d['recs']], float)


def summ_rps(d):
    if d is None: return None
    e_prog = runv(d, 'e_prog'); eg = runv(d, 'e_gross'); fo = runv(d, 'forfeit'); mix = runv(d, 'mix')
    prr = np.array([r['ext']['modal_share']['PRR'] for r in d['recs']], float)
    mixst, a, b = F.rps_by_mixing(eg, fo)
    net = F.status_le(F.boot(e_prog), F.TH['rps'])
    return dict(e_prog=F.boot(e_prog), e_gross=F.boot(eg), forfeit=F.boot(fo), mix=F.boot(mix), prr=F.boot(prr),
                net=net, mixing=mixst, mixing_parts=(a, b), status=F.worst(net, mixst), n=len(e_prog),
                U=F.boot(runv(d, 'sh_U')), sim=F.boot(runv(d, 'fam_sim')), to=F.boot(runv(d, 'to_play')),
                runs=dict(e_prog=e_prog, e_gross=eg, forfeit=fo, prr=prr))


def summ_insp(d):
    if d is None: return None
    eg = np.array([np.mean(r['ext']['isl_eff_gross']) for r in d['recs']], float)
    en = np.array([np.mean(r['ext']['isl_eff_net']) for r in d['recs']], float)
    c0 = runv(d, 'u0g') - runv(d, 'u0'); c1 = runv(d, 'u1g') - runv(d, 'u1')
    return dict(gross=F.boot(eg), net=F.boot(en), s_gross=F.status_ge(F.boot(eg), F.TH['insp']), status=F.status_ge(F.boot(en), F.TH['insp']),
                charge0=F.boot(c0), charge1=F.boot(c1), u0g=F.boot(runv(d, 'u0g')), u1g=F.boot(runv(d, 'u1g')),
                to=F.boot(runv(d, 'to_play')), p_insp=F.boot(runv(d, 'p_insp')), q_cheat=F.boot(runv(d, 'q_cheat')),
                n=len(eg), runs=dict(gross=eg, net=en))


def summ_pd(d, cap=F.TH['pd_charge']):
    if d is None: return None
    recs = d['recs']
    c = F.pd_counts(recs, cap)
    ch = np.array([F.pd_flags(r)['charge'] for r in recs], float)
    scr = np.array([r['ltrace_stats']['scr_charge'] for r in recs], float) if 'ltrace_stats' in recs[0] else np.full(len(recs), np.nan)
    cum = np.array([r['ltrace_stats']['cum_charge'] for r in recs], float) if 'ltrace_stats' in recs[0] else np.full(len(recs), np.nan)
    pcc = np.array([r['final'].get('pcc', np.nan) for r in recs], float)
    return dict(c=c, status=c['sC'], end_charge=F.boot(ch), scr_charge=F.boot(scr), cum_charge=F.boot(cum), pcc=F.boot(pcc),
                n_over_tight=int(np.sum(ch >= F.TH['pd_charge_tight'] - F.TOL)), n_over_cap=int(np.sum(ch > cap + F.TOL)),
                frozen=F.boot([1.0 if r['frozen_at'] >= 0 else 0.0 for r in recs]), gen=F.boot([r['last_gen'] for r in recs]),
                wall=F.boot([r.get('wall', np.nan) for r in recs]), max_charge=float(np.nanmax(ch)),
                ndist=F.boot([len(set(r['holders'])) if r.get('holders') else np.nan for r in recs]),
                chg=F.boot([r.get('n_changes_after500', np.nan) for r in recs]),
                runs=dict(A=np.array([F.pd_flags(r)['A'] for r in recs], float), B=np.array([F.pd_flags(r)['B'] for r in recs], float),
                          C=np.array([F.pd_flags(r)['C'] for r in recs], float), ch=ch, scr=scr, reps=[r['rep'] for r in recs]))


def level_summ(game, level, cell='primary'):
    rule = 'Z' if level == 0.0 else 'A'
    if game == 'rps': return summ_rps(lt_cell('rps', rule, level, cell))
    if game == 'insp': return summ_insp(lt_cell('insp', rule, level, cell))
    return summ_pd(pd_cell(rule, level))


def games_at(rps_lv, insp_lv, pd_lv, cell='primary'):
    s = dict(rps=level_summ('rps', rps_lv, cell), insp=level_summ('insp', insp_lv, cell))
    if cell == 'primary': s['pd'] = level_summ('pd', pd_lv)
    return s


def joint(s):
    sts = [s[g]['status'] if s.get(g) else 'incomplete' for g in (('rps', 'insp', 'pd') if 'pd' in s else ('rps', 'insp'))]
    return F.classify(sts), sts


# ---------------------------------------------------------------------------------------------------------------- stored rows
def retro():
    rows_rps = []; rows_pd = []; rows_insp = []
    for p in sorted(glob.glob(os.path.join(OLD, 'rps_*_primary.json.gz'))):
        d = load(p)
        if d['meta']['rule'] not in ('F', 'FA', 'Bw', 'B', 'Bo', 'A', 'Z', 'Zs', 'Fs', 'T', 'Bws', 'Bl'): continue
        eg = runv(d, 'e_gross'); fo = runv(d, 'forfeit'); mix = runv(d, 'mix'); ep = runv(d, 'e_prog')
        st, a, b = F.rps_by_mixing(eg, fo)
        net = F.status_le(F.boot(ep), F.TH['rps'])
        rows_rps.append((d['meta']['rule'], d['meta']['level'], fmt(F.boot(ep)), net, fmt(F.boot(eg)), fmt(F.boot(fo)), fmt(F.boot(mix)), st,
                         'yes' if (net == 'met' and st != 'met') else ''))
    for p in sorted(glob.glob(os.path.join(OLD, 'insp_*_primary.json.gz'))):
        d = load(p)
        eff = runv(d, 'isl_efficient')
        c0 = runv(d, 'u0g') - runv(d, 'u0'); c1 = runv(d, 'u1g') - runv(d, 'u1')
        rows_insp.append((d['meta']['rule'], d['meta']['level'], fmt(F.boot(eff)), F.status_ge(F.boot(eff), F.TH['insp']), fmt(F.boot(c0), 4),
                          fmt(F.boot(c1), 4), 'unavailable (island counts not stored)'))
    for p in sorted(glob.glob(os.path.join(OLD, 'pd_*_wk_Snon_100_64.json.gz'))):
        d = load(p)
        recs = list(d['recs'])
        if not recs or 'ledger' not in recs[0]: continue
        rule, lv = d['meta']['rule'], d['meta']['level']
        ext = load(p.replace('.json.gz', '_ext.json.gz'))
        pooled = ''
        if ext is not None:
            c2 = F.pd_counts(recs + list(ext['recs']))
            pooled = '%d/%d C=%d (%s)' % (c2['B'], c2['n'], c2['C'], c2['sC'])
        c = F.pd_counts(recs)
        ch = np.array([F.pd_flags(r)['charge'] for r in recs], float)
        rows_pd.append((rule, lv, fc(c['A'], c['n']), fc(c['B'], c['n']), fc(c['C'], c['n']), c['sC'], '%.4g' % np.nanmean(ch), c['late'], c['censored'], pooled))
    return rows_rps, rows_insp, rows_pd


# ---------------------------------------------------------------------------------------------------------------- verdicts
def pdiff_pd(s, z, key='B'):
    ra = dict(zip(s['runs']['reps'], s['runs'][key])); rz = dict(zip(z['runs']['reps'], z['runs'][key]))
    reps = sorted(set(ra) & set(rz))
    return F.boot_paired([ra[r] for r in reps], [rz[r] for r in reps])


def excludes0(t): return t[1] > 0 or t[2] < 0


def build():
    R = dict(levels={}, big={}, verdicts=[], classification={})
    z = games_at(0.0, 0.0, 0.0)
    R['zero'] = z
    for lv in LEVELS:
        R['levels'][lv] = games_at(lv, lv, lv)
    R['As'] = games_at(0.2, 0.5, 0.3)
    R['big'] = dict(Z=games_at(0.0, 0.0, 0.0, 'size') if True else None, A=games_at(0.1, 0.1, 0.1, 'size'))
    return R


def verdict_rows(R):
    V = []
    L = R['levels']; z = R['zero']
    a1 = L[0.1]
    ok = lambda s, g: s.get(g) is not None

    def add(i, v, d): V.append((i, v, d))

    if all(ok(a1, g) for g in ('rps', 'insp', 'pd')):
        rs, isn, pds = a1['rps']['status'], a1['insp']['status'], a1['pd']['status']
        pt = a1['pd']['c']['wC'][0]
        if rs == 'met' and isn == 'met' and pds in ('met', 'undetermined') and pt >= 0.75: v = 'held'
        elif 'failed' not in (rs, isn, pds) and pt >= 0.75: v = 'partial'
        else: v = 'failed'
        add('1', v, 'RPS %s (net %s, mixing %s), inspection net %s (%s), PD (C) %s %s' % (rs, a1['rps']['net'], a1['rps']['mixing'], isn,
            fmt(a1['insp']['net']), pds, fc(a1['pd']['c']['C'], a1['pd']['c']['n'])))
        add('1c (gpt-6.1-sol)', 'held' if isn == 'undetermined' else 'failed', 'inspection net at A 0.1: %s %s; gross %s %s' % (isn, fmt(a1['insp']['net']), a1['insp']['s_gross'], fmt(a1['insp']['gross'])))
    # 2
    b = R['big']
    if b['A'].get('insp') and b['Z'].get('insp'):
        ia = b['A']['insp']; iz = b['Z']['insp']
        c1 = ia['status'] == 'met' or (ia['status'] == 'undetermined' and ia['net'][0] >= 0.60)
        c2 = ia['net'][0] >= iz['net'][0] - 0.10 - 1e-9
        add('2', 'held' if c1 and c2 else ('partial' if c1 or c2 else 'failed'),
            'A 0.1 net %s %s; zero price %s; clause1 %s clause2 %s; gross A %s' % (ia['status'], fmt(ia['net']), fmt(iz['net']), c1, c2, fmt(ia['gross'])))
    # 3
    d3 = {}
    if ok(L[0.03], 'rps'):
        s = L[0.03]['rps']['status']; d3['3a'] = 'held' if s == 'failed' else ('partial' if s == 'undetermined' else 'failed')
    if ok(L[0.3], 'rps'):
        s = L[0.3]['rps']['mixing']; d3['3b'] = 'held' if s == 'met' else ('partial' if s == 'undetermined' else 'failed')
    nf = [(lv, g) for lv in (0.03, 0.1, 0.3) for g in ('insp', 'pd') if ok(L[lv], g) and L[lv][g]['status'] == 'failed']
    d3['3c'] = 'held' if not nf else 'failed'
    vs = list(d3.values())
    add('3', 'held' if all(x == 'held' for x in vs) else ('failed' if 'failed' in vs else 'partial'),
        '3a RPS at 0.03: %s (%s); 3b RPS mixing at 0.3: %s (%s, e_gross %s, forfeit %s); 3c failed insp/PD levels: %s' % (
            d3.get('3a'), L[0.03]['rps']['status'] if ok(L[0.03], 'rps') else '', d3.get('3b'), L[0.3]['rps']['mixing'] if ok(L[0.3], 'rps') else '',
            fmt(L[0.3]['rps']['e_gross']) if ok(L[0.3], 'rps') else '', fmt(L[0.3]['rps']['forfeit']) if ok(L[0.3], 'rps') else '', nf))
    if ok(L[0.3], 'rps'):
        add('3c (gemini-4-argon)', 'held' if L[0.3]['rps']['mixing'] != 'met' else 'failed', 'by mixing at 0.3: %s, parts %s' % (L[0.3]['rps']['mixing'], L[0.3]['rps']['mixing_parts']))
    # 4
    if ok(a1, 'rps') and ok(L[1.0], 'rps') and ok(L[10.0], 'rps'):
        cl = [a1['rps']['mixing'] == 'met', a1['rps']['prr'][0] >= 0.8, L[1.0]['rps']['mixing'] == 'failed', L[10.0]['rps']['mixing'] == 'failed']
        nbad = cl.count(False)
        bad_hard = [i for i, x in enumerate(cl) if not x and [a1['rps']['mixing'], None, L[1.0]['rps']['mixing'], L[10.0]['rps']['mixing']][i] == 'failed']
        v = 'held' if nbad == 0 else ('partial' if nbad == 1 else 'failed')
        add('4', v, 'mixing met at 0.1: %s; PRR modal share %s; failed at 1 (%s) and at 10 (%s)' % (a1['rps']['mixing'], fmt(a1['rps']['prr']), L[1.0]['rps']['mixing'], L[10.0]['rps']['mixing']))
    # 5
    d5 = {}
    det = []
    viol = 0; worstgap = 0
    nrun_over = 0
    for lv in LEVELS:
        if ok(L[lv], 'pd'):
            c = L[lv]['pd']['c']
            gap = c['B'] - c['C']; worstgap = max(worstgap, gap)
            nrun_over += L[lv]['pd']['n_over_tight']
            det.append('%g: A %d B %d C %d' % (lv, c['A'], c['B'], c['C']))
    d5['5a'] = worstgap <= 2
    d5['5b'] = nrun_over == 0
    fst = None
    p = os.path.join(OLD, 'pd_F_0.01_wk_Snon_100_64.json.gz')
    if os.path.exists(p):
        fcnt = F.pd_counts(load(p)['recs'])
        fst = fcnt
        d5['5c'] = fcnt['sC'] != 'met' and fcnt['C'] == 0
    allv = list(d5.values())
    if allv and all(allv): v = 'held'
    elif d5.get('5a') and d5.get('5c') and nrun_over <= 2: v = 'partial'
    else: v = 'failed'
    add('5', v, '; '.join(det) + '; max B-C gap %d; priced runs with end-state charge >= 0.03: %d; F 1e-2 stored (C) %s' % (worstgap, nrun_over, None if fst is None else fc(fst['C'], fst['n'])))
    zz = z.get('pd')
    pdif = {}
    if zz is not None:
        for lv in LEVELS:
            if ok(L[lv], 'pd'): pdif[lv] = pdiff_pd(L[lv]['pd'], zz, 'B')
    R['pd_paired_B'] = pdif
    exc = [lv for lv, t in pdif.items() if excludes0(t)]
    add('5c (gpt-6.1-sol)', 'held' if (d5['5b'] and exc) else 'failed', 'end-state charges tiny: %s; levels whose paired persistent-UO difference excludes 0: %s; %s' % (d5['5b'], exc, {lv: fmt(t) for lv, t in pdif.items()}))
    # E1
    if ok(a1, 'insp'):
        gap = a1['insp']['gross'][0] - a1['insp']['net'][0]
        add('E1', 'held' if gap <= 0.05 + 1e-9 else 'failed', 'gross %s net %s gap %.3f' % (fmt(a1['insp']['gross']), fmt(a1['insp']['net']), gap))
    # E2
    if ok(a1, 'pd') and ok(L[10.0], 'pd'):
        s01 = a1['pd']['scr_charge'][0]; s10 = L[10.0]['pd']['scr_charge'][0]
        ratio = s10 / s01 if s01 > 0 else float('inf')
        add('E2', 'held' if (s01 < 0.03 and ratio < 100) else 'failed', 'scramble charge/play A0.1 %s, A10 %s, ratio %.1f' % (fmt(a1['pd']['scr_charge'], 5), fmt(L[10.0]['pd']['scr_charge'], 5), ratio))
    # E3
    d3_ = []
    for lv in [0.0] + LEVELS:
        s = z.get('pd') if lv == 0.0 else L[lv].get('pd')
        if s: d3_.append((lv, s['c']['A'], s['c']['B']))
    add('E3', 'held' if all(abs(a - b_) <= 2 for _, a, b_ in d3_) else 'failed', 'levels (A snapshot, B persistent): %s' % d3_)
    # E4
    e4 = {lv: pdif[lv] for lv in (0.03, 0.1, 0.3) if lv in pdif}
    add('E4', 'held' if e4 and all((not excludes0(t)) and abs(t[0]) <= 0.15 for t in e4.values()) else 'failed', {lv: fmt(t) for lv, t in e4.items()})
    # E5
    if ok(L[0.03], 'rps'):
        x = L[0.03]['rps']['prr'][0]
        add('E5', 'held' if 0.55 <= x <= 0.85 else 'failed', 'PRR modal share at 0.03: %s' % fmt(L[0.03]['rps']['prr']))
    # E6
    As = R['As']
    if As.get('rps') and As.get('insp') and ok(L[0.3], 'insp') and ok(L[1.0], 'insp'):
        lo = min(L[0.3]['insp']['net'][0], L[1.0]['insp']['net'][0]) - 0.05; hi = max(L[0.3]['insp']['net'][0], L[1.0]['insp']['net'][0]) + 0.05
        c1 = As['rps']['mixing'] == 'met'; c2 = As['insp']['net'][0] >= 0.60 and lo <= As['insp']['net'][0] <= hi
        add('E6', 'held' if c1 and c2 else 'failed', 'A_s RPS 0.2 mixing %s; insp 0.5 net %s (fresh 0.3: %s, 1: %s)' % (As['rps']['mixing'], fmt(As['insp']['net']), fmt(L[0.3]['insp']['net']), fmt(L[1.0]['insp']['net'])))
    # E7
    if b['A'].get('rps') and b['Z'].get('rps'):
        c1 = b['A']['rps']['mixing'] == 'met'; c2 = b['Z']['rps']['mixing'] == 'failed'
        add('E7', 'held' if c1 and c2 else 'failed', 'size A 0.1 RPS mixing %s (e_gross %s, forfeit %s); zero price mixing %s (e_gross %s)' % (
            b['A']['rps']['mixing'], fmt(b['A']['rps']['e_gross']), fmt(b['A']['rps']['forfeit']), b['Z']['rps']['mixing'], fmt(b['Z']['rps']['e_gross'])))
    # E8
    dd = load(os.path.join(OUT, 'rps_A_0.1_primary.json.gz')); di = load(os.path.join(OUT, 'insp_A_0.1_primary.json.gz'))
    if dd and di:
        def nest_share(d, g='2000'):
            tt = np.array([r['ext']['to'][g]['top'] + r['ext']['to'][g]['nested'] for r in d['recs']]); nn = np.array([r['ext']['to'][g]['nested'] for r in d['recs']])
            return float(nn.sum() / tt.sum()) if tt.sum() > 0 else 0.0
        sr, si = nest_share(dd), nest_share(di)
        add('E8', 'held' if sr <= 0.10 and si <= 0.10 else 'failed', 'nested share of counted timeouts at generation 2,000: RPS %.4f, inspection %.4f' % (sr, si))
    # E9, classification
    if all(ok(a1, g) for g in ('rps', 'insp', 'pd')):
        lab, sts = joint(a1)
        R['classification']['primary'] = dict(label=lab, statuses=sts)
        add('E9', 'held' if lab == 'unresolved' and 31 <= a1['pd']['c']['C'] <= 37 else 'failed', 'label %s; statuses (rps, insp, pd) %s; PD (C) %d/40' % (lab, sts, a1['pd']['c']['C']))
    if b['A'].get('rps') and b['A'].get('insp'):
        lab, sts = joint(b['A'])
        R['classification']['size'] = dict(label=lab, statuses=sts)
    # E10
    ok10 = True; det10 = []
    for lv in (1.0, 10.0):
        if ok(L[lv], 'pd') and ok(L[lv], 'insp'):
            pdp = L[lv]['pd']['c']['wC'][0]
            c = pdp >= 0.70 and L[lv]['insp']['status'] == 'met'
            ok10 &= c; det10.append('%g: PD C %s, insp net %s %s' % (lv, fc(L[lv]['pd']['c']['C'], 40), L[lv]['insp']['status'], fmt(L[lv]['insp']['net'])))
    add('E10', 'held' if ok10 else 'failed', '; '.join(det10))
    return V


# ---------------------------------------------------------------------------------------------------------------- tables
def band_table(R):
    rows = []
    cols = [('Z (0)', R['zero'])] + [('A %g' % lv, R['levels'][lv]) for lv in LEVELS] + [('A_s (0.2/0.5/0.3)', R['As'])]
    for name, s in cols:
        r, i, p = s.get('rps'), s.get('insp'), s.get('pd')
        lab, sts = joint(s) if all(s.get(g) for g in ('rps', 'insp', 'pd')) else ('incomplete', [])
        rows.append((name,
                     fmt(r['e_prog']) + ' ' + r['net'] if r else 'n/a', fmt(r['e_gross']) if r else '', fmt(r['forfeit']) if r else '',
                     r['mixing'] if r else '', fmt(r['prr'], 2) if r else '', r['status'] if r else '',
                     fmt(i['gross']) if i else '', fmt(i['net']) if i else '', i['status'] if i else '',
                     fc(p['c']['B'], p['c']['n']) if p else '', fc(p['c']['C'], p['c']['n']) if p else '', p['status'] if p else '', lab))
    return table(['cell', 'RPS e_prog (net)', 'RPS e_gross', 'RPS forfeits', 'by mixing', 'PRR modal share', 'RPS', 'insp gross eff', 'insp net eff', 'insp',
                  'PD (B) persistent', 'PD (C) cost-incl.', 'PD', 'classification'], rows)


def pd_detail(R):
    rows = []
    for name, s in [('Z (0)', R['zero'])] + [('A %g' % lv, R['levels'][lv]) for lv in LEVELS]:
        p = s.get('pd')
        if not p: continue
        c = p['c']
        rows.append((name, fc(c['A'], c['n']), fc(c['B'], c['n']), fc(c['C'], c['n']), c['late'], c['censored'], fmt(p['frozen'], 2), fmt(p['gen'], 0), fmt(p['pcc']),
                     fmt(p['end_charge'], 5), '%.4f' % p['max_charge'], fmt(p['scr_charge'], 5), fmt(p['cum_charge'], 6), p['n_over_tight'], fmt(p['ndist'], 1), fmt(p['chg'], 0), fmt(p['wall'], 0)))
    return table(['cell', '(A) snapshot UO', '(B) persistent UO', '(C) cost-inclusive', 'late', 'censored', 'frozen', 'generations', 'P(C,C)', 'end-state charge/play',
                  'max run', 'scramble charge/play (g<=200)', 'cumulative charge/play', 'runs >= 0.03', 'distinct holders', 'holder changes after 500', 'wall s/run'], rows)


def pd_stakes(R):
    rows = []
    for lv in LEVELS:
        p = R['levels'][lv].get('pd')
        if not p: continue
        rows.append(('A %g' % lv, '%.3g' % p['end_charge'][0], '%.3g' % (p['end_charge'][0] / 3), '%.3g' % p['scr_charge'][0], '%.3g' % (p['scr_charge'][0] / 3), '%.3g' % p['cum_charge'][0]))
    return table(['cell', 'end-state charge', 'in range units', 'scramble charge', 'in range units', 'cumulative'], rows)


def lt_detail(R, game):
    rows = []
    for name, s in [('Z (0)', R['zero'])] + [('A %g' % lv, R['levels'][lv]) for lv in LEVELS]:
        x = s.get(game)
        if not x: continue
        if game == 'rps':
            rows.append((name, fmt(x['U']), fmt(x['sim']), fmt(x['mix']), fmt(x['to']), fmt(x['prr'], 2)))
        else:
            rows.append((name, fmt(x['charge0'], 4), fmt(x['charge1'], 4), fmt(x['u0g']), fmt(x['u1g']), fmt(x['to'], 4), fmt(x['p_insp'], 3), fmt(x['q_cheat'], 3)))
    if game == 'rps':
        return table(['cell', 'U share', 'simulators', 'individual mixing', 'timeouts/play', 'PRR modal share'], rows)
    return table(['cell', 'inspector charge', 'inspectee charge', 'inspector game payoff', 'inspectee game payoff', 'timeouts/play', 'P(inspect)', 'P(cheat)'], rows)


def paired_lt(R):
    rows = []
    z = R['zero']
    for lv in LEVELS:
        s = R['levels'][lv]
        if s.get('rps') and z.get('rps'):
            for k in ('e_gross', 'forfeit', 'prr'):
                t = F.boot_paired(s['rps']['runs'][k], z['rps']['runs'][k])
                rows.append(('RPS', 'A %g' % lv, k, fmt(t)))
        if s.get('insp') and z.get('insp'):
            for k in ('gross', 'net'):
                t = F.boot_paired(s['insp']['runs'][k], z['insp']['runs'][k])
                rows.append(('inspection', 'A %g' % lv, 'efficient fraction (%s)' % k, fmt(t)))
        if s.get('pd') and z.get('pd'):
            for k in ('B', 'C'):
                t = pdiff_pd(s['pd'], z['pd'], k)
                rows.append(('PD', 'A %g' % lv, 'proportion (%s)' % k, fmt(t)))
    return table(['game', 'cell', 'statistic', 'price minus zero, paired (95%)'], rows)


def timeouts_tables(R):
    out = ''
    rows = []
    for game in ('rps', 'insp'):
        for name, rule, lv in [('Z', 'Z', 0.0)] + [('A %g' % l, 'A', l) for l in LEVELS]:
            d = lt_cell(game, rule, lv)
            if not d: continue
            for g in ('500', '2000'):
                v = {k: np.mean([r['ext']['to'][g][k] for r in d['recs']]) for k in ('play', 'top', 'nested', 'opp')}
                tot = v['top'] + v['nested']
                rows.append((game, name, g, '%.4f' % v['play'], '%.4f' % v['top'], '%.5f' % v['nested'], '%.4f' % v['opp'], '%.3f' % (v['nested'] / tot if tot > 0 else 0.0)))
    out += table(['game', 'cell', 'generation', 'timed-out calls/play', 'topmost', 'nested inside a timed-out call', 'issued from the opponent\'s code', 'nested share'], rows)
    # by programme
    rows = []
    for game in ('rps', 'insp'):
        for name, rule, lv in [('Z', 'Z', 0.0), ('A 0.1', 'A', 0.1), ('A 1', 'A', 1.0)]:
            d = lt_cell(game, rule, lv)
            if not d: continue
            nm = d['meta']['names']
            for g in ('500', '2000'):
                if game == 'rps':
                    v = np.mean([r['ext']['to'][g]['by_prog'] for r in d['recs']], 0)
                    top = np.argsort(-v)[:4]
                    rows.append((game, name, g, 'role 0', ', '.join('%s %.4f' % (nm[0][i], v[i]) for i in top if v[i] > 0)))
                else:
                    for ro in (0, 1):
                        v = np.mean([r['ext']['to'][g]['by_prog%d' % ro] for r in d['recs']], 0)
                        top = np.argsort(-v)[:4]
                        rows.append((game, name, g, 'inspector' if ro == 0 else 'inspectee', ', '.join('%s %.4f' % (nm[ro][i], v[i]) for i in top if v[i] > 0)))
    out += '\n' + table(['game', 'cell', 'generation', 'role', 'top programmes by timed-out calls/play contributed (share-weighted)'], rows)
    return out


def support_tables():
    rows = []
    for game in ('rps', 'insp'):
        for name, rule, lv in [('Z', 'Z', 0.0)] + [('A %g' % l, 'A', l) for l in LEVELS]:
            d = lt_cell(game, rule, lv)
            if not d: continue
            nm = d['meta']['names']
            tr = {k: np.mean([r['ext']['transitions'][k]['modal'] for r in d['recs']]) for k in ('500-1000', '1000-1500', '1500-2000', '2000-4000')}
            ts = {k: np.mean([r['ext']['transitions'][k]['support'] for r in d['recs']]) for k in ('1500-2000', '2000-4000')}
            import collections
            cnt = collections.Counter()
            nsup = []
            if game == 'rps':
                for r in d['recs']:
                    for x in r['ext']['dom']['2000']: cnt[nm[0][x]] += 1
                    nsup += [len(s) for s in r['ext']['support2000']]
            else:
                for r in d['recs']:
                    for a, b in zip(*r['ext']['dom']['2000']): cnt[nm[0][a] + '/' + nm[1][b]] += 1
                    nsup += [len(s0) + len(s1) for s0, s1 in zip(*r['ext']['support2000'])]
            tot = sum(cnt.values())
            rows.append((game, name, ' '.join('%s %.2f' % (k, v / tot) for k, v in cnt.most_common(4)), '%.2f' % np.mean(nsup),
                         '/'.join('%.2f' % tr[k] for k in ('500-1000', '1000-1500', '1500-2000', '2000-4000')), '%.2f / %.2f' % (ts['1500-2000'], ts['2000-4000'])))
    return table(['game', 'cell', 'modal programme(s), share of islands', 'mean support size (>= 5%)', 'modal changed: 500-1000 / 1000-1500 / 1500-2000 / 2000-4000', 'support changed: 1500-2000 / 2000-4000'], rows)


def big_table(R):
    rows = []
    for name, s in (('Z (0)', R['big']['Z']), ('A 0.1', R['big']['A'])):
        r, i = s.get('rps'), s.get('insp')
        if not r or not i: continue
        rows.append((name, fmt(r['e_prog']) + ' ' + r['net'], fmt(r['e_gross']), fmt(r['forfeit']), r['mixing'], r['status'], fmt(i['gross']), fmt(i['net']), i['status']))
    return table(['(400, 16), 40 runs', 'RPS e_prog (net)', 'e_gross', 'forfeits', 'by mixing', 'RPS', 'insp gross', 'insp net', 'insp'], rows)



DISCLOSURES = """
## Deviations, retries, cuts and censoring (disclosed)

* **Nothing was cut; nothing crashed; no retries.** All registered cells ran: PD at the zero price and A at 0.03, 0.1, 0.3, 1, 10 (40 fresh reps each, 200-239); RPS and inspection at (100, 64) at the zero price and A at 0.03, 0.1, 0.3, 1, 10 and the stakes-normalized points (RPS 0.2, inspection 0.5), 40 fresh runs (100-139); RPS and inspection at (400, 16): zero price and A 0.1, 40 runs (100-139). The batch log (`runs/failure_pricing_confirm_batch.log`) shows no retry. Two workers throughout (a many-islands process was alive).
* **Caches** were copied from the pricing-rules engineer's worktree (`agent-a2a0df6470309b1aa`), not from the main checkout, which has none; untracked, never committed. The sha256 digests of every cache file and of the `static` directories are identical before and after the run. The code digests differ only by the report module, added after the pre-run digest.
* **The PD stakes-normalized point is the A 0.3 cell** (range 3, 0.1 x 3 = 0.3): no separate run (notes 1.4).
* **Censoring.** A PD run that has not frozen by generation 10,000 is censored (16-19 of 40 per cell); all are kept and scored by the persistence rule (an unfrozen run counts if universal-open at the end and the last indicator change is at least 500 generations earlier). The persistent count equals the snapshot count in every priced cell; at the zero price one run is late (36 snapshot, 35 persistent).
* **Scramble charge** uses the right-endpoint rule (notes 1.2b); the PD has only primitive reads (check or production caps, at most 2 per play, no nesting), so its timeouts are reported by stage only and not by programme or depth. Nested timed-out calls (inside another timed-out call) are exactly 0 in every RPS and inspection cell; a timed-out call issued from the opponent's code inside a simulation occurs (zero price 0.014-0.025 per play, at most 0.011 under A 0.03 and 0 from A 0.1).
* **Inspection net by island is unavailable for the stored rows**; the retrospective table gives gross fractions and the stored role charges.
* **The verdict logic was fixed in the predictions file before any counted cell**; the classification (confirmed iff all three games are met) uses the worst of each game's components. The exploratory sample is not pooled with the fresh runs anywhere in the headline.
"""

def main():
    R = build()
    V = verdict_rows(R)
    md = ['# Confirming failure pricing as the default compute charge (run report, 2026-10-25)\n']
    md.append('Spec `specs/2026-10-25-failure-pricing-confirmation.md`; notes `notes/failure-pricing-confirm.md`; predictions `predictions/2026-10-25-failure-pricing-confirm.md`. '
              'LOTTERY objects at fixed geometry, fresh run indices only (RPS and inspection runs 100-139 at (100, 64) and (400, 16); PD reps 200-239, world K, S-nonself, (100, 64), up to 10,000 generations). '
              'Never pi; conclusions restricted to the tested geometries, grammars, caps and world K. Intervals: run-clustered bootstrap for means, Wilson for run counts.\n')
    cl = R['classification']
    md.append('## Headline\n')
    if 'primary' in cl:
        md.append('**Default (A at P_fail = 0.1) at (100, 64): %s** (statuses RPS / inspection / PD: %s). ' % (cl['primary']['label'].upper(), cl['primary']['statuses']))
    if 'size' in cl:
        md.append('At (400, 16), RPS and inspection: **%s** (%s).\n' % (cl['size']['label'], cl['size']['statuses']))
    md.append('\n## Band table, fresh runs, (100, 64)\n')
    md.append(band_table(R))
    md.append('\nPD (B) persistent universal-open; (C) persistent with end-state charge per play <= 0.3 (0.1 of the range 3); threshold 0.70 by Wilson. Insp net: net-of-charge efficient islands >= 0.60.\n')
    md.append('\n## Verdicts\n')
    md.append(table(['#', 'verdict', 'detail'], [(i, '**%s**' % v, str(d)) for i, v, d in V]))
    md.append('\n## PD detail\n')
    md.append(pd_detail(R))
    md.append('\nCharge in stakes (range 3):\n\n' + pd_stakes(R))
    md.append('\n## RPS detail\n' + lt_detail(R, 'rps'))
    md.append('\n## Inspection detail\n' + lt_detail(R, 'insp'))
    md.append('\n## Larger geometry (400, 16)\n' + big_table(R))
    md.append('\n## Paired price-minus-zero differences (matched fresh founder sets)\n' + paired_lt(R))
    md.append('\n## Timed-out calls: by depth and stage, then by programme\n' + timeouts_tables(R))
    md.append('\n## Support and transitions\n' + support_tables())
    rr, ri, rp = retro()
    md.append('\n## Retrospective: the new scores on the stored rows of "What compute should cost" (exploratory runs, not fresh)\n')
    md.append('RPS by mixing (stored e_gross and forfeit run values):\n\n' + table(['rule', 'level', 'e_prog (net)', 'net', 'e_gross', 'forfeits', 'individual mixing', 'by mixing', 'net met but not by mixing'], rr))
    md.append('\nPD persistent and cost-inclusive (registered rows; pooled with the supplementary rows where present):\n\n' + table(['rule', 'level', '(A) snapshot', '(B) persistent', '(C) cost-inclusive', 'status (C)', 'mean end-state charge', 'late', 'censored', 'pooled B / C'], rp))
    md.append('\nInspection: gross efficient fraction and the stored role charges; the island-level net score is unavailable for stored rows:\n\n' + table(['rule', 'level', 'efficient (gross)', 'status', 'inspector charge', 'inspectee charge', 'net'], ri))
    md.append(DISCLOSURES)
    hp = os.path.join(OUT, 'provenance_hashes.json')
    if os.path.exists(hp):
        h = json.load(open(hp))
        md.append('\n## Provenance\n')
        same = h.get('pre', {}).get('caches') == h.get('post', {}).get('caches') if 'post' in h else None
        md.append('Cache digests pre and post run identical: %s (`runs/failure_pricing_confirm/provenance_hashes.json`).\n' % same)
    open(os.path.join(ROOT, 'runs', 'failure-pricing-confirm.md'), 'w').write('\n'.join(md))

    def clean(o):
        if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items() if k != 'runs'}
        if isinstance(o, (list, tuple)): return [clean(v) for v in o]
        if isinstance(o, (np.floating, np.integer)): return o.item()
        if isinstance(o, np.ndarray): return o.tolist()
        return o
    json.dump(dict(verdicts=[dict(id=i, verdict=v, detail=str(d)) for i, v, d in V], classification=cl, levels=clean(R['levels']), zero=clean(R['zero']),
                   As=clean(R['As']), big=clean(R['big'])), open(os.path.join(ROOT, 'runs', 'failure-pricing-confirm.json'), 'w'), indent=1, default=str)
    print('\n'.join(md)[:6000])


if __name__ == '__main__':
    main()
