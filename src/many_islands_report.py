"""Report for the many-islands experiment: reads the per-job json files in runs/many_islands/ and writes
runs/many-islands.md and runs/many-islands.json.  Importable without side effects.

    python3 src/many_islands_report.py
"""
import os, sys, json, math, glob
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import many_islands as MI
import many_islands_run as MR
from many_islands_analysis import tint

OUT = MR.OUT
ROOT = MR.ROOT
ARMS = ('L', 'M', 'R')
AS = (0, 50, 150)
ARMNAME = {'L': 'L (weak)', 'M': 'modalPA', 'R': 'readers', 'Rw': 'readers (weak)'}
V = list(MI.V)
SHOW_CP = (1, 10, 100, 300, 1000, 3000, 10000, 100000, 1000000)


def jload(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def cells():
    out = []
    for arm in ('L', 'M', 'R', 'Rw'):
        for A in AS:
            if glob.glob(os.path.join(OUT, 'chain_%s_A%d_p[0-9].json' % (arm, A))):
                out.append((arm, A))
    return out


def fmt(v, d=3):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return 'nan'
    return ('%.' + str(d) + 'f') % v


def interval(v, d=3):
    m, lo, hi = tint(v)
    if math.isnan(lo):
        return fmt(m, d)
    return '%s [%s, %s]' % (fmt(m, d), fmt(lo, d), fmt(hi, d))


def wilson(k, n, z=1.96):
    return MR.wilson(k, n, z)


# ====================================================================== statistics of one histogram
def shares(h):
    h = np.asarray(h, float)
    return h / max(h.sum(), 1.0)


def pair_shares(h):
    return shares(h)[V]


def vstar(h):
    return float(pair_shares(h).sum())


def coverage(h, thr=1e-3):
    return bool((pair_shares(h) > thr).all())


def max_pair_fraction(h):
    p = pair_shares(h)
    return float(p.max() / max(p.sum(), 1e-12))


def break_time(cps, hist, vmin=0.5, frac=0.6):
    """first checkpoint (events per island) at which the V* share is at least vmin and the largest pair holds at least
    frac of it; nan if never."""
    for c, h in zip(cps, hist):
        if vstar(h) >= vmin and max_pair_fraction(h) >= frac:
            return float(c)
    return float('nan')


def first_loss_events(first_loss, I):
    fl = [v for v in first_loss if v >= 0]
    return float(min(fl)) / I if fl else float('nan')


def lowdim(h):
    s = shares(h)
    cat = MI.CATMAP
    return dict(Vstar=float(s[V].sum()), U=float(s[cat == 1].sum()), G=float(s[cat == 2].sum()), W=float(s[cat == 3].sum()),
                D=float(s[cat == 4].sum()), eff=float(sum(s[k] for k in range(MI.NOUT) if MI.TOT[k] > 0.999)),
                pairs=[float(x) for x in s[V]], minpair=float(s[V].min()), maxfrac=max_pair_fraction(h))


def km_median(times, observed):
    """Kaplan-Meier median; times with observed flag (False = right-censored at that time)."""
    t = np.asarray(times, float); e = np.asarray(observed, bool)
    o = np.argsort(t, kind='stable')
    t = t[o]; e = e[o]
    n = len(t); S = 1.0
    for i in range(n):
        if e[i]:
            S *= 1.0 - 1.0 / (n - i)
            if S <= 0.5:
                return float(t[i])
    return float('nan')


def at(cps, hist, cp):
    return hist[cps.index(cp)] if cp in cps else None


# ====================================================================== per-cell summary
def load_cell(arm, A):
    c = dict(arm=arm, A=A)
    c['chains'] = [jload(f) for f in sorted(glob.glob(os.path.join(OUT, 'chain_%s_A%d_p[0-9].json' % (arm, A))))]
    c['post'] = jload(os.path.join(OUT, 'post_%s_A%d.json' % (arm, A)))
    c['union'] = jload(os.path.join(OUT, 'union_%s_A%d.json' % (arm, A)))
    c['ia'] = jload(os.path.join(OUT, 'ia_%s_A%d.json' % (arm, A)))
    c['comp'] = jload(os.path.join(OUT, 'comp_%s_A%d.json' % (arm, A)))
    c['sym'] = jload(os.path.join(OUT, 'sym_%s_A%d_sym.json' % (arm, A)))
    c['rs'] = {os.path.basename(f)[len('rs_%s_A%d_' % (arm, A)):-5]: jload(f)
               for f in sorted(glob.glob(os.path.join(OUT, 'rs_%s_A%d_*.json' % (arm, A))))}
    c['pools'] = [jload(f) for f in sorted(glob.glob(os.path.join(OUT, 'pool_%s_A%d_p[0-9].json' % (arm, A))))]
    return c


def traj_over_pools(chs, key):
    out = {}
    for cp in SHOW_CP:
        vals = [c['summary'][c['cps'].index(cp)][key] for c in chs if cp in c['cps']]
        if vals:
            out[cp] = tint(vals)
    return out


def cell_summary(cell):
    chs = cell['chains']
    S = dict(arm=cell['arm'], A=cell['A'], npools=len(chs), I=chs[0]['I'], capped=[c['capped'] for c in chs])
    S['post'] = {k: tint([c['summary0'][k] for c in chs]) for k in ('Vstar', 'F0', 'F1', 'F2', 'U', 'G', 'W', 'D', 'eff', 'meanTOT')}
    S['traj'] = {k: traj_over_pools(chs, k) for k in ('Vstar', 'U', 'G', 'W', 'D', 'eff', 'meanTOT')}
    cov = {}
    for cp in SHOW_CP:
        hs = [c['hist'][c['cps'].index(cp)] for c in chs if cp in c['cps']]
        if hs:
            cov[cp] = dict(min_pair=float(np.mean([pair_shares(h).min() for h in hs])), covered=int(sum(coverage(h) for h in hs)),
                           pools=len(hs), maxfrac=[max_pair_fraction(h) for h in hs])
    S['cov'] = cov
    S['break'] = [break_time(c['cps'], c['hist']) for c in chs]
    S['first_loss'] = [first_loss_events(c['first_loss'], c['I']) for c in chs]
    S['x1000'] = S['traj']['Vstar'].get(1000)
    S['x1e4'] = S['traj']['Vstar'].get(10000)
    S['xinf'] = S['traj']['Vstar'].get(100000)
    S['xinf_converged'] = bool(S['xinf'] and S['x1e4'] and abs(S['xinf'][0] - S['x1e4'][0]) < 0.02)
    S['div'] = {cp: [float(np.mean([c['div'][c['cps'].index(cp)][q] for c in chs if cp in c['cps']])) for q in range(6)]
                for cp in (1, 1000, 10000, 100000) if all(cp in c['cps'] for c in chs)}
    # excluded-slot drift along the path: fixations that replaced the excluded program, class unchanged / changed, over slot visits
    dr = np.zeros((MI.NOUT, 3))
    for c in chs:
        d = np.array(c['drift'])
        dr += d[:7].sum(axis=0)                    # intervals up to 1000 events per island
    S['drift_to1000'] = dict(excl_visits=float(dr[:, 2].sum()), same_class=float(dr[:, 0].sum()), changed=float(dr[:, 1].sum()))
    # path flows between fair pairs (event counts in the intervals up to 1000 events per island)
    pk = {}
    for c in chs:
        for (i, a, b, cc, n) in c['pathK']:
            if c['cps'][i] <= 1000 and a != cc:
                key = (MI.CATLAB[MI.CATMAP[a]] + ('%d' % V.index(a) if a in V else ''), MI.CATLAB[MI.CATMAP[cc]] + ('%d' % V.index(cc) if cc in V else ''))
                pk[key] = pk.get(key, 0) + n
    S['path_flows_to1000'] = {'%s>%s' % k: v for k, v in sorted(pk.items(), key=lambda kv: -kv[1])[:20]}
    # symmetric manifold
    sy = cell['sym']
    if sy:
        S['sym'] = {cp: lowdim(sy['hist'][sy['cps'].index(cp)]) for cp in SHOW_CP if cp in sy['cps']}
        S['sym_meta'] = dict(n_reps=sy['n_reps'], cap=sy['cps'][-1], wall=sy['wall'])
    # pool-size ladder
    un = cell['union']
    if un:
        S['union'] = {k: dict(I=v['I'], traj={cp: lowdim(v['hist'][v['cps'].index(cp)]) for cp in SHOW_CP if cp in v['cps']},
                              brk=break_time(v['cps'], v['hist'])) for k, v in un.items()}
    # giant resampled pools and tilts
    S['rs'] = {}
    for tag, r in cell['rs'].items():
        S['rs'][tag] = dict(M=r['M'], sym=r['sym'], tilt=r['tilt'], source=r['source'],
                            traj={cp: lowdim(r['hist'][r['cps'].index(cp)]) for cp in SHOW_CP if cp in r['cps']},
                            brk=break_time(r['cps'], r['hist']), imbalance=[(c, max_pair_fraction(h)) for c, h in zip(r['cps'], r['hist'])
                                                                           if 300 <= c <= 30000], wall=r['wall'])
    # (2a)
    ia = cell['ia']
    if ia:
        S['ia'] = ia_summary(ia, S)
    cp_ = cell['comp']
    if cp_:
        S['comp'] = comp_summary(cp_)
    S['post_full'] = cell['post']
    return S


def ia_summary(ia, S):
    out = {}
    pool_v = {cp: S['traj']['Vstar'][cp][0] for cp in S['traj']['Vstar']}
    for I in sorted({r['I'] for r in ia}):
        rs = [r for r in ia if r['I'] == I]
        cps = rs[0]['cps']
        cap = cps[-1]
        d = dict(runs=len(rs), cap=cap)
        d['V'] = {cp: float(np.mean([vstar(r['hist'][cps.index(cp)]) for r in rs])) for cp in SHOW_CP if cp in cps}
        d['V_sd'] = {cp: float(np.std([vstar(r['hist'][cps.index(cp)]) for r in rs], ddof=1)) for cp in SHOW_CP if cp in cps}
        d['cov1000'] = [int(sum(coverage(r['hist'][cps.index(1000)]) for r in rs)), len(rs)]
        fl = [first_loss_events(r['first_loss'], I) for r in rs]
        obs = [not math.isnan(v) for v in fl]
        times = [v if o else float(cap) for v, o in zip(fl, obs)]
        d['first_loss'] = dict(times=fl, observed=int(sum(obs)), km_median=km_median(times, obs))
        bt = [break_time(cps, r['hist']) for r in rs]
        bo = [not math.isnan(v) for v in bt]
        bts = [v if o else float(cap) for v, o in zip(bt, bo)]
        d['break'] = dict(times=bt, observed=int(sum(bo)), km_median=km_median(bts, bo))
        d['dev_from_pool'] = {cp: abs(d['V'][cp] - pool_v[cp]) for cp in d['V'] if cp in pool_v}
        out[I] = d
    return out


def comp_summary(comp):
    out = {}
    base = {r['run']: r for r in comp if r['C'] == 1}
    for C in sorted({r['C'] for r in comp}):
        rs = [r for r in comp if r['C'] == C]
        cps = rs[0]['cps']
        d = dict(runs=len(rs))
        d['V'] = {cp: float(np.mean([vstar(r['hist'][cps.index(cp)]) for r in rs])) for cp in SHOW_CP if cp in cps}
        d['diff_vs_C1'] = {}
        for cp in SHOW_CP:
            if cp in cps:
                dif = [vstar(r['hist'][cps.index(cp)]) - vstar(base[r['run']]['hist'][cps.index(cp)]) for r in rs]
                d['diff_vs_C1'][cp] = [float(np.mean(dif)), float(np.std(dif, ddof=1) / math.sqrt(len(dif))) if len(dif) > 1 else float('nan')]
        d['cov'] = {cp: [int(sum(coverage(r['hist'][cps.index(cp)]) for r in rs)), len(rs)] for cp in SHOW_CP if cp in cps}
        d['U'] = {cp: float(np.mean([lowdim(r['hist'][cps.index(cp)])['U'] for r in rs])) for cp in SHOW_CP if cp in cps}
        d['G'] = {cp: float(np.mean([lowdim(r['hist'][cps.index(cp)])['G'] for r in rs])) for cp in SHOW_CP if cp in cps}
        out[C] = d
    return out


# ====================================================================== markdown
def md_table(header, rows):
    out = ['| ' + ' | '.join(header) + ' |', '|' + '|'.join(['---'] * len(header)) + '|']
    for r in rows:
        out.append('| ' + ' | '.join(str(x) for x in r) + ' |')
    return out


def key(arm, A):
    return '%s A=%d' % (arm, A)


def build(write=True):
    cs = cells()
    R = {}
    for arm, A in cs:
        R[key(arm, A)] = cell_summary(load_cell(arm, A))
    md = ['# Many islands: islands to infinity before time, rare migration, annealed mutation (report)', '']
    md += ['Spec `specs/2026-10-25-many-islands.md`; predictions `predictions/2026-10-25-many-islands.md`; notes `notes/many-islands.md`.', '']
    md += ['## 1. Post-annealing law of the settled islands (pool means [t interval over pools])', '']
    rows = []
    for k, S in R.items():
        p = S['post']
        rows.append([k, S['npools'], S['I'], sum(S['capped']), interval([p['Vstar'][0]], 3) if False else '%s' % interval_t(p['Vstar']),
                     interval_t(p['U']), interval_t(p['G']), interval_t(p['W']), interval_t(p['D']), interval_t(p['eff']),
                     fmt(p['meanTOT'][0], 4)])
    md += md_table(['cell', 'pools', 'islands/pool', 'capped', 'V*', 'U', 'G', 'W', 'D', 'efficient (total 1)', 'mean total'], rows)
    md += ['', '## 2. Pool Monte Carlo of the jump chain (V* share, pool means), by events per island', '']
    cps_show = [c for c in SHOW_CP]
    rows = []
    for k, S in R.items():
        rows.append([k] + [fmt(S['traj']['Vstar'][c][0], 3) if c in S['traj']['Vstar'] else '' for c in cps_show])
    md += md_table(['cell'] + [str(c) for c in cps_show], rows)
    md += ['', 'Wasteful + disagreement share:', '']
    rows = []
    for k, S in R.items():
        rows.append([k] + [fmt(S['traj']['W'][c][0] + S['traj']['D'][c][0], 4) if c in S['traj']['W'] else '' for c in cps_show])
    md += md_table(['cell'] + [str(c) for c in cps_show], rows)
    md += ['', 'Unequal share:', '']
    rows = []
    for k, S in R.items():
        rows.append([k] + [fmt(S['traj']['U'][c][0], 3) if c in S['traj']['U'] else '' for c in cps_show])
    md += md_table(['cell'] + [str(c) for c in cps_show], rows)
    md += ['', 'Coverage: pools (of n) with all three fair pairs above 10^-3, and mean smallest pair share:', '']
    rows = []
    for k, S in R.items():
        rows.append([k] + ['%d/%d, %s' % (S['cov'][c]['covered'], S['cov'][c]['pools'], fmt(S['cov'][c]['min_pair'], 3)) if c in S['cov'] else '' for c in cps_show])
    md += md_table(['cell'] + [str(c) for c in cps_show], rows)
    md += ['', 'Largest pair as a fraction of V* (per pool) at 10,000 and 100,000 events per island; break time (first checkpoint with V* >= 0.5 and largest pair >= 0.6 of V*); first fair-pair loss (events per island):', '']
    rows = []
    for k, S in R.items():
        mf = lambda cp: ', '.join(fmt(x, 2) for x in S['cov'].get(cp, {}).get('maxfrac', []))
        rows.append([k, mf(10000), mf(100000), ', '.join(fmt(x, 0) for x in S['break']), ', '.join(fmt(x, 0) for x in S['first_loss'])])
    md += md_table(['cell', 'maxfrac @1e4', 'maxfrac @1e5', 'break', 'first loss'], rows)
    md += ['', 'Program diversity (mean distinct programs per slot, pool 0..): at 1, 1,000, 10,000, 100,000 events per island:', '']
    rows = []
    for k, S in R.items():
        rows.append([k] + [', '.join(fmt(x, 0) for x in S['div'].get(cp, [])[:3]) for cp in (1, 1000, 10000, 100000)])
    md += md_table(['cell', '1', '1000', '10000', '100000'], rows)
    # symmetric manifold
    md += ['', '## 3. The S3-symmetric mean-field chain (orbit Monte Carlo): V*, largest/smallest pair, G, by events per island', '']
    rows = []
    for k, S in R.items():
        if 'sym' in S:
            for cp in SHOW_CP:
                if cp in S['sym']:
                    s = S['sym'][cp]
                    rows.append([k, cp, fmt(s['Vstar'], 4), ', '.join(fmt(x, 4) for x in s['pairs']), fmt(s['U'], 4), fmt(s['G'], 4), fmt(s['W'] + s['D'], 4)])
    md += md_table(['cell', 'events/island', 'V*', 'pairs', 'U', 'G', 'W+D'], rows)
    # ladder
    md += ['', '## 4. Pool-size ladder and giant resampled pools (V*, break time)', '']
    rows = []
    for k, S in R.items():
        for lab, u in S.get('union', {}).items():
            rows.append([k, lab, u['I'], ', '.join('%s:%s' % (cp, fmt(u['traj'][cp]['Vstar'], 3)) for cp in (100, 1000, 3000, 10000) if cp in u['traj']), fmt(u['brk'], 0)])
        for tag, u in S.get('rs', {}).items():
            rows.append([k, 'rs:' + tag, u['M'], ', '.join('%s:%s' % (cp, fmt(u['traj'][cp]['Vstar'], 3)) for cp in (100, 1000, 3000, 10000) if cp in u['traj']), fmt(u['brk'], 0)])
    md += md_table(['cell', 'pool', 'islands', 'V* at 100, 1000, 3000, 10000', 'break time'], rows)
    # ia
    md += ['', '## 5. (2a) Event-driven archipelagos: V* (run mean) at 1,000 events/island, coverage at 1,000, first loss and break (KM median, events/island)', '']
    rows = []
    for k, S in R.items():
        for I, d in S.get('ia', {}).items():
            rows.append([k, I, d['cap'], fmt(d['V'].get(1000), 3), fmt(d['V_sd'].get(1000), 3), '%d/%d' % tuple(d['cov1000']),
                         '%d/%d, %s' % (d['first_loss']['observed'], d['runs'], fmt(d['first_loss']['km_median'], 0)),
                         '%d/%d, %s' % (d['break']['observed'], d['runs'], fmt(d['break']['km_median'], 0)),
                         fmt(d['dev_from_pool'].get(1000), 3)])
    md += md_table(['cell', 'I', 'cap', 'V*@1000', 'sd', 'covered@1000', 'first loss (observed, KM median)', 'break (observed, KM median)', '|V*-pool|@1000'], rows)
    # components
    md += ['', '## 6. (1) Disconnected components, I = 1,024: V* difference from one component (run mean, se) and coverage across components', '']
    rows = []
    for k, S in R.items():
        for C, d in S.get('comp', {}).items():
            rows.append([k, C, ', '.join('%s:%s' % (cp, fmt(d['V'][cp], 3)) for cp in (1000, 10000, 100000) if cp in d['V']),
                         ', '.join('%s:%s' % (cp, fmt(d['diff_vs_C1'][cp][0], 3)) for cp in (1000, 10000, 100000) if cp in d['diff_vs_C1']),
                         ', '.join('%s:%d/%d' % (cp, d['cov'][cp][0], d['cov'][cp][1]) for cp in (1000, 10000, 100000) if cp in d['cov']),
                         ', '.join('%s:%s' % (cp, fmt(d['U'][cp], 3)) for cp in (10000, 100000) if cp in d['U'])])
    md += md_table(['cell', 'C', 'V*', 'V* - V*(C=1)', 'covered runs', 'U'], rows)
    # post analyses
    md += ['', '## 7. Kernel statistics (exact one-migrant kernel on the post-anneal pools)', '']
    for k, S in R.items():
        P = S.get('post_full')
        if not P:
            continue
        md += ['### %s' % k, '']
        fb = P['fair_block']
        md += ['Antisymmetric net flows between fair pairs (shares per event, mean [t interval over pools]): D01 %s, D02 %s, D12 %s; mean fair-to-fair flow %s.' % (
            interval_t(fb['D'][0], 9), interval_t(fb['D'][1], 9), interval_t(fb['D'][2], 9), fmt(float(np.mean(fb['flow_mean'])), 9)), '']
        md += ['Category rates per event (exit, to V*): ' + '; '.join('%s: %s, %s' % (g, interval_t(v['exit'], 6), interval_t(v['toF'], 6)) for g, v in P['cat_rates'].items()), '']
        md += ['Heterogeneity of per-recipient exit probability within category (pool 0): ' + '; '.join(
            '%s: mean %s, CV %s, share with zero exit %s' % (g, fmt(v['mean_exit'], 6), fmt(v['cv_exit'], 2), fmt(v['frac_zero_exit'], 3)) for g, v in P['heterogeneity'].items()), '']
        md += ['Routes (rate per event of a recipient of the category, by the role of the migrant\'s slot): ' + '; '.join(
            '%s %s' % (a, fmt(v, 6)) for a, v in sorted(P['routes'].items(), key=lambda kv: -kv[1])[:14]), '']
        md += ['Cryptic drift (paired hazard before/after a neutral substitution of the excluded program): ' + '; '.join(
            '%s: n=%d, to-V* ratio %s, change ratio %s' % (g, v['n'], fmt(v['ratio_toF'], 2), fmt(v['ratio_change'], 2)) for g, v in P['cryptic'].items()), '']
        md += ['ODE (class level) V* at 1e3, 1e4, 1e5: ' + ', '.join(fmt(np.interp(np.log(t), np.log(np.maximum(P['ode']['t'], 1e-9)), P['ode']['V']), 3) for t in (1e3, 1e4, 1e5)) +
               '; mass error %s, min x %s' % (fmt(P['ode']['mass_err'], 12), fmt(P['ode']['min_x'], 12)), '']
        tm = P['two_migrant']
        rows = []
        for cell_, v in tm.items():
            if v['n']:
                n = v['n']
                rows.append([cell_, n, fmt(v['single_change'] / n, 5), fmt(v['seq_change'] / n, 5), fmt(v['ov_change'] / n, 5), fmt(v['single_toF'] / n, 5),
                             fmt(v['seq_toF'] / n, 5), fmt(v['ov_toF'] / n, 5), v['ov_capped']])
        md += ['Two-migrant probe (recipient group > donor group; per tuple: single migrant, two in sequence, two overlapping; change of class and move to V*):', '']
        md += md_table(['cell', 'n', 'single chg', 'seq chg', 'overlap chg', 'single toV*', 'seq toV*', 'overlap toV*', 'capped'], rows)
        inj = P.get('injection_at_checkpoints', {})
        if inj:
            md += ['', 'Injection statistics on triples sampled during migration (exit / to-V* per event by group):']
            for ck, v in inj.items():
                md += ['- %s: shares %s; ' % (ck, {a: round(b, 4) for a, b in v['shares'].items()}) + '; '.join(
                    '%s exit %s toV* %s' % (g, fmt(x['exit'], 6), fmt(x['toF'], 6)) for g, x in v['by_group'].items())]
        md += ['']
    md += ['Excluded-slot drift along the path (events up to 1,000 per island, all pools): fixations replacing the excluded program per visit of the excluded slot:', '']
    rows = [[k, int(S['drift_to1000']['excl_visits']), int(S['drift_to1000']['same_class']), int(S['drift_to1000']['changed'])] for k, S in R.items()]
    md += md_table(['cell', 'excluded-slot events', 'fixed, class unchanged', 'fixed, class changed'], rows)
    md += ['', 'Largest class-changing path flows up to 1,000 events per island (counts, all pools):', '']
    for k, S in R.items():
        md += ['- %s: ' % k + ', '.join('%s %d' % (a, v) for a, v in list(S['path_flows_to1000'].items())[:10])]
    out = '\n'.join(md) + '\n'
    if write:
        with open(os.path.join(ROOT, 'runs', 'many-islands.md'), 'w') as f:
            f.write(out)
        with open(os.path.join(ROOT, 'runs', 'many-islands.json'), 'w') as f:
            json.dump(R, f, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
    return R, out


def interval_t(t, d=3):
    m, lo, hi = t
    if lo is None or (isinstance(lo, float) and math.isnan(lo)):
        return fmt(m, d)
    return '%s [%s, %s]' % (fmt(m, d), fmt(lo, d), fmt(hi, d))


if __name__ == '__main__':
    R, out = build()
    print(out[:3000])
