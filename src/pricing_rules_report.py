"""Report for the pricing-rules experiment: runs/pricing-rules.md and runs/pricing-rules.json from runs/pricing_rules/*.json.gz.

Objects: LOTTERY = the epsilon = 0 seed lottery at the stated geometry (RPS and inspection read at generation 2,000; the PD at the end
of the run, at most 10,000); STATIC = exact tables of the instrumented engine.  Intervals: run-clustered bootstrap (4,000
resamples) for means, Wilson for the PD proportion.  Targets and scoring: predictions/2026-10-25-pricing-rules.md.
"""
import glob
import gzip
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'runs', 'pricing_rules')

TH = dict(rps=0.10, insp=0.60, pd=0.70)
RULE_LEVELS = dict(F=[1e-5, 1e-4, 1e-3, 1e-2], FA=[1e-5, 1e-4, 1e-3, 1e-2], B=[1e-5, 1e-4, 1e-3, 1e-2], A=[0.01, 0.1, 1.0, 10.0])
_cache = {}


def load(path):
    if path in _cache: return _cache[path]
    d = json.load(gzip.open(path, 'rt')) if os.path.exists(path) else None
    _cache[path] = d
    return d


def cell(game, rule, level, cell='primary'):
    if game == 'pd':
        return load(os.path.join(OUT, 'pd_%s_%g_%s.json.gz' % (rule, level, 'wk_Snon_100_64' if cell == 'primary' else 'wk_Snon_200_64')))
    return load(os.path.join(OUT, '%s_%s_%g_%s.json.gz' % (game, rule, level, cell)))


def boot(vals, B=4000, seed=20261025):
    v = np.asarray(vals, float); v = v[~np.isnan(v)]
    if len(v) == 0: return (float('nan'),) * 3
    idx = np.random.default_rng(seed).integers(len(v), size=(B, len(v)))
    m = v[idx].mean(1)
    return float(v.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'),) * 3
    p = k / n
    den = 1 + z * z / n
    ctr = (p + z * z / (2 * n)) / den
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return float(p), float(max(0, ctr - half)), float(min(1, ctr + half))


def fmt(t, d=3):
    if t is None or (isinstance(t, tuple) and np.isnan(t[0])): return 'n/a'
    return '%.*f [%.*f, %.*f]' % (d, t[0], d, t[1], d, t[2])


def runstat(d, key, g='2000'):
    return np.array([r['stats'][g].get(key, np.nan) for r in d['recs']], float)


def pdstat(d, key):
    out = []
    for r in d['recs']:
        if key == 'uo': out.append(1.0 if r['final'].get('universal_open') else 0.0)
        elif key == 'pcc': out.append(r['final'].get('pcc', np.nan))
        elif key == 'steps': out.append(r['ledger'][0] if r.get('ledger') else np.nan)
        elif key == 'to': out.append(r['ledger'][2] if r.get('ledger') else np.nan)
        elif key == 'charge': out.append(r['ledger'][3] if r.get('ledger') else np.nan)
        elif key == 'prodsteps': out.append(r['ledger'][1] if r.get('ledger') else np.nan)
        elif key == 'frozen': out.append(1.0 if r['frozen_at'] >= 0 else 0.0)
        elif key == 'gen': out.append(r['last_gen'])
        elif key == 'wall': out.append(r['wall'])
    return np.array(out, float)


def target(game, d):
    """(estimate triple, status) of the game's target in cell d."""
    if d is None: return None, 'not run'
    if game == 'rps':
        t = boot(runstat(d, 'e_prog'))
        st = 'met' if t[2] <= TH['rps'] else ('failed' if t[1] > TH['rps'] else 'undetermined')
    elif game == 'insp':
        t = boot(runstat(d, 'isl_efficient'))
        st = 'met' if t[1] >= TH['insp'] else ('failed' if t[2] < TH['insp'] else 'undetermined')
    else:
        v = pdstat(d, 'uo')
        t = wilson(int(v.sum()), len(v))
        st = 'met' if t[1] >= TH['pd'] else ('failed' if t[2] < TH['pd'] else 'undetermined')
    return t, st


def triple(rule, level, cl='primary'):
    out = {}
    for g in ('rps', 'insp', 'pd'):
        out[g] = target(g, cell(g, rule, level, cl))
    return out


def joint(tr):
    sts = [tr[g][1] for g in ('rps', 'insp', 'pd')]
    if any(s == 'not run' for s in sts): return 'incomplete'
    if all(s == 'met' for s in sts): return 'MET'
    if any(s == 'failed' for s in sts): return 'failed'
    return 'undetermined'


def levels_present(rule):
    return [lv for lv in RULE_LEVELS[rule] if any(cell(g, rule, lv) is not None for g in ('rps', 'insp', 'pd'))]


# ---------------------------------------------------------------------------------------------------------------- statics
def statics():
    import pricing_rules_lt as L
    import numpy as np
    out = {}
    cgrid = [10 ** (x / 8.0) for x in range(-48, -7)]          # 1e-6 .. 1e-1
    pgrid = [10 ** (x / 8.0) for x in range(-24, 17)]          # 1e-3 .. 1e2
    b = L.Base('rps'); K = b.K
    names = b.tb.names[0]; u = names.index('U')
    Ug = b.tb.Ug
    rows = []
    for rule, grid in (('F', cgrid), ('FA', cgrid), ('Bw', cgrid), ('A', pgrid), ('T', pgrid)):
        for lv in grid:
            ch = b.charge(b.arrays, rule, lv, K)
            Un = Ug - ch
            gain = Un[:, u] - Un[u, u]
            gain[u] = -1
            rows.append(dict(rule=rule, level=lv, invaders=int((gain > 1e-9).sum()), max_gain=float(gain.max()),
                             who=[names[i] for i in np.nonzero(gain > 1e-9)[0].tolist()][:6]))
    out['rps_U_invasion'] = rows
    b2 = L.Base('insp'); K = b2.K
    n0, n1 = b2.n0, b2.n1
    eff = [(a, c) for a in range(n0) for c in range(n1) if b2.tb.UAg[a, c] >= -0.05 and b2.tb.UBg[c, a] >= -0.05]
    rows = []
    for rule, grid in (('F', cgrid), ('FA', cgrid), ('Bw', cgrid), ('A', pgrid), ('T', pgrid)):
        for lv in grid:
            ch0 = b2.charge(b2.arr0, rule, lv, K); ch1 = b2.charge(b2.arr1, rule, lv, K)
            UA = b2.tb.UAg - ch0; UB = b2.tb.UBg - ch1
            ok = 0
            for (a, c) in eff:
                inv0 = (UA[:, c] > UA[a, c] + 1e-9).any(); inv1 = (UB[:, a] > UB[c, a] + 1e-9).any()
                if not inv0 and not inv1: ok += 1
            rows.append(dict(rule=rule, level=lv, eff_pairs=len(eff), proof=ok))
    out['insp_efficient_pairs'] = rows
    return out, b, b2


def flips(rows, key, good):
    """Level intervals (by rule) where good(row) holds, merged on the grid."""
    res = {}
    for rule in sorted(set(r['rule'] for r in rows)):
        rr = [r for r in rows if r['rule'] == rule]
        ivs = []; cur = None
        for r in rr:
            if good(r):
                if cur is None: cur = [r['level'], r['level']]
                else: cur[1] = r['level']
            else:
                if cur is not None: ivs.append(cur); cur = None
        if cur is not None: ivs.append(cur)
        res[rule] = ivs
    return res


# ---------------------------------------------------------------------------------------------------------------- tables
def stat_row(game, d):
    if d is None: return None
    if game == 'rps':
        keys = ['e_prog', 'e_gross', 'sh_U', 'fam_sim', 'forfeit', 'mix', 'to_play', 'steps', 'cost', 'net_payoff']
        return {k: boot(runstat(d, k)) for k in keys} | {'resolved': boot([r['resolved'] for r in d['recs']])}
    if game == 'insp':
        keys = ['isl_efficient', 'isl_commit_comply', 'p_insp', 'q_cheat', 'u0g', 'u1g', 'fam0_sim', 'sh1_C0', 'to_play', 'steps0', 'steps1']
        r = {k: boot(runstat(d, k)) for k in keys}
        r['charge0'] = boot(runstat(d, 'u0g') - runstat(d, 'u0')); r['charge1'] = boot(runstat(d, 'u1g') - runstat(d, 'u1'))
        r['resolved'] = boot([x['resolved'] for x in d['recs']])
        return r
    v = pdstat(d, 'uo')
    return dict(uo=wilson(int(v.sum()), len(v)), pcc=boot(pdstat(d, 'pcc')), steps=boot(pdstat(d, 'steps')), to=boot(pdstat(d, 'to')),
                charge=boot(pdstat(d, 'charge')), frozen=boot(pdstat(d, 'frozen')), gen=boot(pdstat(d, 'gen')), wall=boot(pdstat(d, 'wall')))


def build():
    R = {}
    ref = {}
    for g in ('rps', 'insp'):
        ref[g] = dict(Z=target(g, cell(g, 'Z', 0.0)), Zs=target(g, cell(g, 'Zs', 0.0)))
    ref['pd'] = dict(Z=target('pd', cell('pd', 'Z', 0.0)))
    R['reference'] = ref
    R['bands'] = {}
    for rule in ('F', 'FA', 'B', 'A'):
        R['bands'][rule] = {lv: triple(rule, lv) for lv in RULE_LEVELS[rule]}
    R['bands_Bw'] = {lv: triple('Bw', lv) for lv in RULE_LEVELS['F']} if False else None
    return R


def md_triple_table(R, rule):
    lines = ['| level | RPS e_prog (net) | RPS | inspection efficient | insp | PD universal-open | PD | joint |', '|---|---|---|---|---|---|---|---|']
    for lv in RULE_LEVELS[rule]:
        tr = R['bands'][rule][lv]
        if all(tr[g][1] == 'not run' for g in tr): continue
        lines.append('| %g | %s | %s | %s | %s | %s | %s | %s |' % (lv, fmt(tr['rps'][0]), tr['rps'][1], fmt(tr['insp'][0]), tr['insp'][1],
                                                                   fmt(tr['pd'][0]), tr['pd'][1], joint(tr)))
    return '\n'.join(lines)


def band_summary(R):
    out = {}
    for rule in ('F', 'FA', 'B', 'A'):
        lv = RULE_LEVELS[rule]
        stat = {l: joint(R['bands'][rule][l]) for l in lv}
        met = [l for l in lv if stat[l] == 'MET']
        poss = [l for l in lv if stat[l] in ('MET', 'undetermined')]
        adj = any(stat[lv[i]] == 'MET' and stat[lv[i + 1]] == 'MET' for i in range(len(lv) - 1))
        out[rule] = dict(status=stat, met=met, possible=poss, adjacent_met=adj)
    return out


def get(game, rule, level, cl='primary'):
    return cell(game, rule, level, cl)


def share_u(rule, level, cl='primary'):
    d = get('rps', rule, level, cl)
    return None if d is None else boot(runstat(d, 'sh_U'))


def verdicts(R, S):
    V = []
    def add(name, verdict, detail): V.append((name, verdict, detail))
    # 1
    bad = []; allmet = []; unk = []
    for lv in RULE_LEVELS['F']:
        tr = R['bands']['F'][lv]
        if all(tr[g][1] == 'not run' for g in tr): continue
        sts = [tr[g][1] for g in tr]
        if any(x == 'failed' for x in sts): bad.append(lv)
        elif all(x == 'met' for x in sts): allmet.append(lv)
        else: unk.append(lv)
    v1 = 'failed' if allmet else ('held' if not unk else 'undetermined')
    add('1 F has no joint band', v1, 'levels with a failed game: %s; all three met: %s; undetermined or incomplete: %s' % (bad, allmet, unk))
    # 2
    st = S['A']['status']
    lv = RULE_LEVELS['A']
    adj = S['A']['adjacent_met']
    possible_pairs = [(lv[i], lv[i + 1]) for i in range(3) if st[lv[i]] not in ('failed', 'incomplete') and st[lv[i + 1]] not in ('failed', 'incomplete')]
    v2 = 'held' if adj else ('failed' if not possible_pairs and all(st[l] != 'incomplete' for l in lv) else 'undetermined')
    add('2 A has a joint band', v2, 'status by level %s; adjacent pair met: %s; adjacent pairs still possible: %s' % (st, adj, possible_pairs))
    # 3
    su = {l: share_u('A', l) for l in RULE_LEVELS['A']}
    s01 = su.get(0.1)
    if s01 is None: v3 = 'not scored'
    else:
        hi = [su[l] for l in (0.1, 1.0, 10.0) if su.get(l) is not None]
        v3 = 'held' if all(x[0] >= 0.5 for x in hi) and s01[1] > 0.5 else ('failed' if s01[2] < 0.5 else 'partial')
    tp = {}
    for l in (0.1, 1.0):
        d = get('rps', 'A', l); d0 = get('rps', 'Z', 0.0)
        if d and d0: tp[l] = (boot(runstat(d, 'to_play')), boot(runstat(d0, 'to_play')))
    add('3 A: U wins at P_fail >= 0.1', v3, 'share of U by P_fail: %s; timeouts per play (A vs zero): %s' % (
        {l: fmt(x) for l, x in su.items() if x}, {l: (fmt(a), fmt(b)) for l, (a, b) in tp.items()}))
    cp = []
    for l in (0.1, 1.0, 10.0):
        t = R['bands']['A'].get(l, {}).get('rps')
        d = get('rps', 'A', l); d0 = get('rps', 'Z', 0.0)
        if t and d and d0 and t[1] != 'not run':
            half = boot(runstat(d, 'to_play'))[0] <= 0.5 * boot(runstat(d0, 'to_play'))[0]
            cp.append((l, t[1], bool(half)))
    add('3c (gpt-6.1-sol) finishing readers keep RPS off target', 'held' if any(st_ != 'met' and half for (_, st_, half) in cp) else ('failed' if cp else 'not scored'), str(cp))
    # 4
    d = get('pd', 'B', 1e-3)
    pdB = target('pd', d)
    diffs = {}
    for c in (1e-5, 1e-4, 1e-3, 1e-2):
        b_ = share_u('B', c); f_ = share_u('F', c)
        if b_ and f_: diffs[c] = b_[0] - f_[0]
    v4 = 'not scored' if d is None or not diffs else ('held' if pdB[1] == 'met' and all(x <= 0.1 for x in diffs.values()) else ('failed' if any(x > 0.1 for x in diffs.values()) else 'partial'))
    add('4 B helps the PD, hurts the coin', v4, 'PD B at 1e-3: %s %s; U share B - F by c: %s' % (fmt(pdB[0]), pdB[1], {c: round(x, 3) for c, x in diffs.items()}))
    add('4c (gpt-6.1-sol) ordering fails by > 0.1 either way', ('held' if any(abs(x) > 0.1 for x in diffs.values()) else 'failed') if diffs else 'not scored',
        'differences: %s' % {c: round(x, 3) for c, x in diffs.items()})
    # 5
    def lowest_met(rule):
        for l in RULE_LEVELS[rule]:
            t = R['bands'][rule][l]['rps']
            if t[1] == 'met': return l
        return None
    lf, lfa = lowest_met('F'), lowest_met('FA')
    pdfa = R['bands']['FA'][1e-3]['pd'][1]
    v5 = 'failed' if S['FA']['met'] else ('held' if (lfa is not None and (lf is None or lfa < lf)) and pdfa == 'failed' else 'partial')
    add('5 F+A against F', v5, 'lowest panel c meeting RPS: F %s, F+A %s; PD under F+A at 1e-3: %s; F+A joint band: %s' % (lf, lfa, pdfa, S['FA']['met'] or 'none'))
    # engineer's predictions
    s3 = share_u('F', 1e-3); s4 = share_u('F', 1e-4)
    add('E1 stored RPS dose reproduced', 'not scored' if not (s3 and s4) else ('held' if s3[0] >= 0.5 and s4[0] < 0.5 else 'failed'), 'U share F: 1e-3 %s, 1e-4 %s' % (fmt(s3), fmt(s4)))
    pdF = {c: target('pd', get('pd', 'F', c)) for c in (1e-4, 1e-3)}
    add('E2 PD under F fails by arithmetic', 'not scored' if any(v[0] is None for v in pdF.values()) else ('held' if all(v[0][0] < 0.35 for v in pdF.values()) else 'failed'),
        '; '.join('c=%g: %s' % (c, fmt(v[0])) for c, v in pdF.items()))
    z = target('pd', get('pd', 'Z', 0.0))
    pdA = {p: target('pd', get('pd', 'A', p)) for p in (0.01, 0.1, 1.0, 10.0)}
    pdA = {p: v for p, v in pdA.items() if v[0] is not None}
    add('E3 PD under A is the zero-price PD', 'not scored' if z[0] is None or not pdA else ('held' if all(abs(v[0][0] - z[0][0]) <= 0.15 for v in pdA.values()) else 'failed'),
        'zero %s; A: %s' % (fmt(z[0]), {p: fmt(v[0]) for p, v in pdA.items()}))
    iA = {p: target('insp', get('insp', 'A', p)) for p in (0.01, 0.1, 1.0, 10.0)}
    iA = {p: v for p, v in iA.items() if v[0] is not None}
    add('E4 inspection under A stays >= 0.6', 'not scored' if not iA else ('held' if all(v[0][0] >= 0.6 for v in iA.values()) else 'failed'),
        {p: fmt(v[0]) + ' ' + v[1] for p, v in iA.items()})
    diffsw = {}
    for c in (1e-5, 1e-4, 1e-3, 1e-2):
        b_ = get('rps', 'B', c); w_ = get('rps', 'Bw', c)
        if b_ and w_:
            diffsw[c] = (boot(runstat(b_, 'e_prog'))[0] - boot(runstat(w_, 'e_prog'))[0], boot(runstat(b_, 'sh_U'))[0] - boot(runstat(w_, 'sh_U'))[0])
    add('E5 warm and cold cache within 0.1', 'not scored' if not diffsw else ('held' if all(abs(a) < 0.1 and abs(b) < 0.1 for a, b in diffsw.values()) else 'failed'),
        'e_prog and U-share differences (B cold - B warm): %s' % {c: (round(a, 3), round(b, 3)) for c, (a, b) in diffsw.items()})
    wid = {r: len(S[r]['possible']) for r in S}
    add('E6 headline: F none; A widest possible band, two adjacent met; FA and B narrower', 'held' if (not S['F']['met'] and S['A']['adjacent_met'] and len(S['A']['possible']) >= 3 and
         len(S['A']['possible']) > max(len(S['B']['possible']), len(S['FA']['possible']))) else ('failed' if (not S['A']['adjacent_met'] and all(s != 'undetermined' for s in S['A']['status'].values())) or len(S['A']['possible']) < len(S['B']['possible']) else 'partial'),
        'possible-band widths %s; met %s' % (wid, {r: S[r]['met'] for r in S}))
    tA = {}
    for t in (0.1, 1.0):
        di = get('insp', 'T', t); dr = get('rps', 'T', t)
        if di: tA[('insp', t)] = fmt(target('insp', di)[0])
        if dr: tA[('rps', t)] = fmt(target('rps', dr)[0])
    ti = target('insp', get('insp', 'T', 1.0))
    add('E7 toll tau = 1 breaks inspection', 'not scored' if ti[0] is None else ('held' if ti[0][0] < 0.6 else 'failed'), str(tA))
    pdFA = target('pd', get('pd', 'FA', 1e-3)); pdF3 = target('pd', get('pd', 'F', 1e-3))
    add('E8 F+A binds the PD at least as hard as F', 'not scored' if pdFA[0] is None or pdF3[0] is None else ('failed' if (pdFA[1] == 'met' and pdF3[1] == 'failed') else 'held'),
        'PD c=1e-3: F %s, F+A %s' % (fmt(pdF3[0]), fmt(pdFA[0])))
    return V


def cells_for(game):
    pref = {'rps': 'rps_', 'insp': 'insp_', 'pd': 'pd_'}[game]
    seen = []
    for f in sorted(glob.glob(os.path.join(OUT, pref + '*_primary.json.gz')) + glob.glob(os.path.join(OUT, pref + '*_wk_Snon_100_64.json.gz'))):
        b = os.path.basename(f)[len(pref):].replace('.json.gz', '')
        parts = b.split('_')
        rule, lv = parts[0], float(parts[1])
        seen.append((rule, lv))
    order = {'Z': 0, 'Zs': 1, 'F': 2, 'Fs': 3, 'A': 4, 'As': 5, 'FA': 6, 'FAs': 7, 'Bw': 8, 'B': 9, 'T': 10}
    return sorted(set(seen), key=lambda x: (order.get(x[0], 99), x[1]))


def DETAIL(R):
    out = []
    out += ['## RPS detail (LOTTERY, generation 2,000; run means with 95% intervals)', '',
            '| cell | e_prog (net) | e_gross | U share | simulators | forfeits | individual mixing | timeouts/play | steps/play | charge/play | resolved |', '|---|---|---|---|---|---|---|---|---|---|---|']
    for rule, lv in cells_for('rps'):
        d = cell('rps', rule, lv)
        if d is None: continue
        r = stat_row('rps', d)
        out.append('| %s %g | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (rule, lv, fmt(r['e_prog']), fmt(r['e_gross']), fmt(r['sh_U']), fmt(r['fam_sim']), fmt(r['forfeit']),
                                                                        fmt(r['mix']), fmt(r['to_play']), fmt(r['steps'], 1), fmt(r['cost'], 4), fmt(r['resolved'], 2)))
    out += ['', '## Inspection detail (LOTTERY, generation 2,000)', '',
            '| cell | efficient islands | committed+compliant | P(inspect) | P(cheat) | simulating inspectors | C0 share | inspector game payoff | inspectee game payoff | timeouts/play | charge inspector | charge inspectee | resolved |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for rule, lv in cells_for('insp'):
        d = cell('insp', rule, lv)
        if d is None: continue
        r = stat_row('insp', d)
        out.append('| %s %g | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (rule, lv, fmt(r['isl_efficient']), fmt(r['isl_commit_comply']), fmt(r['p_insp']), fmt(r['q_cheat']),
                                                                                  fmt(r['fam0_sim']), fmt(r['sh1_C0']), fmt(r['u0g']), fmt(r['u1g']), fmt(r['to_play']), fmt(r['charge0'], 4), fmt(r['charge1'], 4), fmt(r['resolved'], 2)))
    out += ['', '## PD detail (LOTTERY, world K, S-nonself, (100, 64), 20 runs)', '',
            '| cell | universal-open runs | P(C,C) | final steps/play | production steps/play | timeouts/play | charge/play | frozen runs | generations | wall s/run |', '|---|---|---|---|---|---|---|---|---|---|']
    for rule, lv in cells_for('pd'):
        d = cell('pd', rule, lv)
        if d is None: continue
        r = stat_row('pd', d)
        out.append('| %s %g | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (rule, lv, fmt(r['uo']), fmt(r['pcc']), fmt(r['steps'], 0), fmt(boot(pdstat(d, 'prodsteps')), 0), fmt(r['to'], 4),
                                                                      fmt(r['charge'], 4), fmt(r['frozen'], 2), fmt(r['gen'], 0), fmt(r['wall'], 0)))
    return '\n'.join(out)


def larger():
    out = ['', '## Larger geometry (levels that met all three at the primary geometry)', '', '| cell | RPS (400, 16) | inspection (400, 16) | PD (200, 64) |', '|---|---|---|---|']
    p = os.path.join(OUT, 'big_levels.json')
    levels = json.load(open(p)) if os.path.exists(p) else []
    for (rule, lv) in levels:
        tr = triple(rule, lv, 'size')
        tr['pd'] = target('pd', cell('pd', rule, lv, 'big'))
        out.append('| %s %g | %s %s | %s %s | %s %s |' % (rule, lv, fmt(tr['rps'][0]), tr['rps'][1], fmt(tr['insp'][0]), tr['insp'][1], fmt(tr['pd'][0]), tr['pd'][1]))
    if not levels: out.append('| none | | | |')
    return '\n'.join(out)


def statics_md():
    st, b, b2 = statics()
    out = ['', '## Statics (exact tables; where invasions flip between the panel points)', '']
    fl = flips(st['rps_U_invasion'], 'invaders', lambda r: r['invaders'] == 0)
    out += ['RPS: levels at which a monomorphic `U` population is invaded by no program (net payoffs), by rule:', '']
    for rule, ivs in fl.items():
        out.append('* %s: %s' % (rule, ', '.join('[%.2g, %.2g]' % tuple(iv) for iv in ivs) or 'no level on the grid'))
    allg = {r: len([x for x in st['rps_U_invasion'] if x['rule'] == r]) for r in fl}
    fl2 = flips(st['insp_efficient_pairs'], 'proof', lambda r: r['proof'] == r['eff_pairs'])
    fl3 = flips(st['insp_efficient_pairs'], 'proof', lambda r: r['proof'] > 0)
    out += ['', 'Inspection: efficient resident pairs (both roles at game payoff >= -0.05): %d. Levels at which every one resists invasion by any single mutant of either role:' % st['insp_efficient_pairs'][0]['eff_pairs'], '']
    for rule, ivs in fl2.items():
        out.append('* %s: %s; at least one resistant pair: %s' % (rule, ', '.join('[%.2g, %.2g]' % tuple(iv) for iv in ivs) or 'none', ', '.join('[%.2g, %.2g]' % tuple(iv) for iv in fl3[rule]) or 'none'))
    return '\n'.join(out), st


def main():
    R = build()
    S = band_summary(R)
    R['summary'] = {k: {kk: (vv if kk != 'status' else {str(a): b for a, b in vv.items()}) for kk, vv in v.items()} for k, v in S.items()}
    V = verdicts(R, S)
    R['verdicts'] = V
    lines = ['# What compute should cost: three pricing rules across three games (run report, 2026-10-25)', '',
             'Spec `specs/2026-10-25-pricing-rules.md`; hand table `notes/pricing-rules.md` §1; choices and deviations §2; predictions '
             '`predictions/2026-10-25-pricing-rules.md`. LOTTERY objects at fixed geometry (RPS, inspection: N = 100 per role, I = 64, '
             'mN = 1, 40 runs, generation 2,000, K = 10⁴; PD: world K, S-nonself, (100, 64), 20 runs, up to 10,000 generations, K = 10⁶ per '
             'encounter). Never π; a fixed-geometry comparison, not evidence about large populations. Targets: RPS net exploitability e_prog '
             '≤ 0.10; inspection efficient islands ≥ 0.60; PD universal-open runs ≥ 0.70. met / failed / undetermined by 95% run-level '
             'intervals.', '']
    lines += ['## Reference (zero price)', '', '| game | exact kernel | sampled kernel (bridge) |', '|---|---|---|']
    for g in ('rps', 'insp'):
        lines.append('| %s | %s %s | %s %s |' % (g, fmt(R['reference'][g]['Z'][0]), R['reference'][g]['Z'][1], fmt(R['reference'][g]['Zs'][0]), R['reference'][g]['Zs'][1]))
    lines.append('| pd | %s %s | – |' % (fmt(R['reference']['pd']['Z'][0]), R['reference']['pd']['Z'][1]))
    lines += ['', '## Joint-band table', '']
    for rule in ('F', 'A', 'FA', 'B'):
        lines += ['### Rule %s' % rule, '', md_triple_table(R, rule), '',
                  'Joint band (all three met): %s; possible band (no game failed): %s; adjacent pair met: %s' % (
                      S[rule]['met'] or 'none', S[rule]['possible'] or 'none', S[rule]['adjacent_met']), '']
    lines += ['## Verdicts', '', '| # | verdict | detail |', '|---|---|---|']
    for n, v, d in V: lines.append('| %s | **%s** | %s |' % (n, v, d))
    lines += ['', DETAIL(R), larger()]
    if '--nostatics' not in sys.argv:
        sm, st = statics_md()
        lines.append(sm)
        R['statics'] = st
    open(os.path.join(ROOT, 'runs', 'pricing-rules.md'), 'w').write('\n'.join(lines))
    json.dump(R, open(os.path.join(ROOT, 'runs', 'pricing-rules.json'), 'w'), default=lambda o: str(o), indent=1)
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
