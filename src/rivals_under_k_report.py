"""Report for rivals under K: runs/rivals-under-k.md and runs/rivals-under-k.json.
Spec specs/2026-10-05-rivals-under-k.md; predictions predictions/2026-10-05-rivals-under-k.md."""
import json, math, os, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import rivals_under_k as RK
from rival_islands_report import wilson, poisson_ci, km

RUNS = RK.RUNS
OUT_MD = os.path.join(RUNS, 'rivals-under-k.md')
OUT_JS = os.path.join(RUNS, 'rivals-under-k.json')
MARKS = (100, 1000, 10000, 100000, 300000)
ARMLAB = {'free': 'free', 'K16': 'K b = 16', 'K4': 'K b = 4', 'K54': 'K b = 54'}


def ci(k, n):
    if n == 0: return '–'
    lo, hi = wilson(k, n)
    return '%d/%d = %.4f [%.4f, %.4f]' % (k, n, k / n, lo, hi)


def cis(k, n):
    if n == 0: return '–'
    lo, hi = wilson(k, n)
    return '%.2f [%.2f, %.2f]' % (k / n, lo, hi)


def e(x, d=2):
    if x is None or (isinstance(x, float) and math.isnan(x)): return '–'
    if x == 0: return '0'
    return ('%.' + str(d - 1) + 'e') % x if (abs(x) < 1e-2 or abs(x) >= 1e4) else ('%.' + str(d + 1) + 'g') % x


def upper0(n):
    """One-sided 95% upper bound on a binomial rate with 0 events in n runs (exact: 1 - 0.05^(1/n) ~ 3/n)."""
    return 1 - 0.05 ** (1 / n)


def upper_k(k, n):
    """One-sided 95% upper bound (Clopper-Pearson) on a binomial rate with k events in n."""
    from scipy.stats import beta
    return float(beta.ppf(0.95, k + 1, n - k)) if k < n else 1.0


# ------------------------------------------------------------------ natural cells
def nat_stats(rs):
    n = len(rs)
    st = dict(n=n, arm=rs[0]['arm'], mN=rs[0]['mN'])
    st['status'] = dict(Counter(r['status'] for r in rs))
    st['ever'] = sum(r['first_sep'] >= 0 for r in rs)
    st['end'] = sum(r['n_sep_end'] > 0 for r in rs)
    st['end_ci'] = list(wilson(st['end'], n)); st['end_upper95'] = upper_k(st['end'], n)
    st['ever_ci'] = list(wilson(st['ever'], n))
    kinds_end = Counter(); kinds_ever = Counter(); rivals_end = Counter(); rivals_ever = Counter()
    bl_end = 0; bl_ever = 0; pst_end = 0
    sep_rows = []
    for r in rs:
        if r['first_sep'] < 0 and r['n_sep_end'] == 0: continue
        S = r.get('seps', [])
        first = [s for s in S if s['when'] == 'first']
        endS = [s for s in S if s['when'] == 'end']
        if first:
            s = first[0]; kinds_ever[s['kind']] += 1
            if s['kind'] == 'A-rival':
                rivals_ever[s['rival']] += 1; bl_ever += s['rival_bridgeless']
        if r['n_sep_end'] > 0 and endS:
            s = endS[0]; kinds_end[s['kind']] += 1
            if s['kind'] == 'A-rival':
                rivals_end[s['rival']] += 1; bl_end += s['rival_bridgeless']; pst_end += s['rival_pstar']
        sep_rows.append(dict(rep=r['rep'], first=r['first_sep'], end=r['n_sep_end'] > 0, status=r['status'],
                             stop=r['stop_gen'], sep=r['sep'], pcc=r['pcc'], cf=r['cf_cross_pcc'],
                             seps=[dict((k, v) for k, v in s.items() if k not in ('rival_sources',)) for s in S]))
    st['kinds_ever'] = dict(kinds_ever); st['kinds_end'] = dict(kinds_end)
    st['rivals_ever'] = dict(rivals_ever); st['rivals_end'] = dict(rivals_end)
    st['bridgeless_end'] = bl_end; st['bridgeless_ever'] = bl_ever; st['pstar_end'] = pst_end
    # resolution of ever-separated runs: duration from first separation to resolution, censored at the stop
    ev = [r for r in rs if r['sep']['ever']]
    dur = [(r['sep']['resolved_at'] - r['sep']['first']) if not r['sep']['sep_at_end'] else (r['stop_gen'] - r['sep']['first'])
           for r in ev]
    evt = [not r['sep']['sep_at_end'] for r in ev]
    st['resolved'] = int(sum(evt)); st['censored'] = int(len(evt) - sum(evt))
    st['km'] = km(dur, evt, MARKS) if ev else {}
    st['dur_resolved_median'] = float(np.median([d_ for d_, x in zip(dur, evt) if x])) if sum(evt) else float('nan')
    st['episodes'] = dict(Counter(r['sep']['n_episodes'] for r in ev))
    # bridge fate among ever-separated A-rivalries
    fate = Counter()
    for r in ev:
        f = [s for s in r.get('seps', []) if s['when'] == 'first']
        if not f: continue
        s = f[0]
        key = ('bridged' if s['n_bridge_classes'] > 0 else 'no bridge in support') + (
            '' if s['n_bridge_classes'] == 0 else (', bridge alive' if s['bridge_alive_end'] else ', bridge dead')) + (
            ', separated at end' if r['sep']['sep_at_end'] else ', resolved')
        fate[key] += 1
    st['bridge_fate'] = dict(fate)
    st['pcc'] = float(np.mean([r['pcc'] for r in rs])); st['pcc_min'] = float(np.min([r['pcc'] for r in rs]))
    st['eff'] = sum(r['pcc'] >= 0.95 for r in rs); st['eff_ci'] = list(wilson(st['eff'], n))
    st['alld'] = sum(r['pcc'] < 0.05 for r in rs)
    sr = [r for r in rs if r['n_sep_end'] > 0]
    st['cf_sep'] = float(np.mean([r['cf_cross_pcc'] for r in sr])) if sr else float('nan')
    st['pcc_sep'] = float(np.mean([r['pcc'] for r in sr])) if sr else float('nan')
    st['cf_all'] = float(np.mean([r['cf_cross_pcc'] for r in rs]))
    st['n_est'] = float(np.mean([r['n_est'] for r in rs]))
    st['hours'] = sum(r['time_s'] for r in rs) / 3600
    st['sep_rows'] = sep_rows
    return st


def paired(a, b, key):
    """McNemar-style paired comparison of a boolean statistic over common reps."""
    A = {r['rep']: r for r in a}; B = {r['rep']: r for r in b}
    common = sorted(set(A) & set(B))
    x = [(key(A[k]), key(B[k])) for k in common]
    return dict(n=len(common), both=sum(1 for p, q in x if p and q), a_only=sum(1 for p, q in x if p and not q),
                b_only=sum(1 for p, q in x if q and not p))


# ------------------------------------------------------------------ forced cells
def qstat(rows, ref, key='n_loc_est', B=2000):
    rr = {r['rep']: r for r in ref}
    a = np.array([(r[key], rr[r['rep']][key]) for r in rows if r['rep'] in rr], float)
    if len(a) == 0 or a[:, 1].sum() == 0: return float('nan'), (float('nan'), float('nan')), a
    q = a[:, 0].sum() / a[:, 1].sum()
    rng = np.random.default_rng(11); bs = []
    for _ in range(B):
        ix = rng.integers(0, len(a), len(a))
        if a[ix, 1].sum() > 0: bs.append(a[ix, 0].sum() / a[ix, 1].sum())
    return float(q), (float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))), a,


def dq_paired(rows_a, ref_a, rows_b, ref_b, key='n_loc_est', B=2000):
    """q(a) - q(b), bootstrap over reps common to both (paired seeds)."""
    ra = {r['rep']: r for r in rows_a}; fa = {r['rep']: r for r in ref_a}
    rb = {r['rep']: r for r in rows_b}; fb = {r['rep']: r for r in ref_b}
    common = sorted(set(ra) & set(fa) & set(rb) & set(fb))
    if not common: return float('nan'), (float('nan'), float('nan'))
    M = np.array([(ra[k][key], fa[k][key], rb[k][key], fb[k][key]) for k in common], float)
    f = lambda m: m[:, 0].sum() / m[:, 1].sum() - m[:, 2].sum() / m[:, 3].sum()
    d0 = f(M); rng = np.random.default_rng(13); bs = []
    for _ in range(B):
        ix = rng.integers(0, len(M), len(M))
        if M[ix, 1].sum() > 0 and M[ix, 3].sum() > 0: bs.append(f(M[ix]))
    return float(d0), (float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)))


def forced_stats(rs, ref):
    n = len(rs)
    st = dict(n=n, arm=rs[0]['arm'], mN=rs[0]['mN'], exp=rs[0]['exp'], forced=rs[0]['forced'])
    st['status'] = dict(Counter(r['status'] for r in rs))
    if 'lineage_alive_end' in rs[0]:
        st['coop_est_runs'] = sum(r['coop_est_lineage'] > 0 for r in rs)
        st['coop_est_islands'] = sum(r['coop_est_lineage'] for r in rs)
        st['coop_hold_end_runs'] = sum(r['coop_hold_end_lineage'] > 0 for r in rs)
        st['coop_hold_end_islands_mean'] = float(np.mean([r['coop_hold_end_lineage'] for r in rs]))
        st['alive_end'] = sum(r['lineage_alive_end'] for r in rs)
        st['alive_ci'] = list(wilson(st['alive_end'], n))
        ext = [r['lineage_ext_gen'] for r in rs]
        st['ext_median'] = float(np.median([x if x >= 0 else np.inf for x in ext]))
        st['ext_q'] = [float(np.percentile([x if x >= 0 else 1e9 for x in ext], q)) for q in (25, 50, 75, 90)]
        st['lineage_max_mean'] = float(np.mean([r['lineage_max'] for r in rs]))
        st['lineage_held_max_mean'] = float(np.mean([r['lineage_held_max'] for r in rs]))
        st['lineage_held_end_mean'] = float(np.mean([r['lineage_held_end'] for r in rs]))
        st['founders'] = int(np.mean([r['founders'] for r in rs]))
        st['forced_cls'] = rs[0]['forced_cls']
    st['sep_end'] = sum(r['n_sep_end'] > 0 for r in rs); st['sep_ever'] = sum(r['first_sep'] >= 0 for r in rs)
    st['pcc'] = float(np.mean([r['pcc'] for r in rs])); st['pcc_min'] = float(np.min([r['pcc'] for r in rs]))
    st['eff'] = sum(r['pcc'] >= 0.95 for r in rs)
    sr = [r for r in rs if r['n_sep_end'] > 0]
    st['cf_sep'] = float(np.mean([r['cf_cross_pcc'] for r in sr])) if sr else float('nan')
    st['n_est'] = float(np.mean([r['n_est'] for r in rs]))
    if ref:
        q, qci, a = qstat(rs, ref)[:3]
        st['q_est'] = [q, qci[0], qci[1], len(a)]
    st['hours'] = sum(r['time_s'] for r in rs) / 3600
    return st


def pos_stats(rs):
    n = len(rs)
    st = dict(n=n, arm=rs[0]['arm'], mN=rs[0]['mN'], forced=rs[0]['forced'])
    st['rival_est'] = sum(r['rival_est'] for r in rs)
    st['ever_sep'] = sum(r['ever_sep_tag'] for r in rs)
    st['sep_end'] = sum(r['sep_end_tag'] for r in rs)
    st['both_end'] = sum(r['both_end'] for r in rs)
    st['gen_sep_end'] = sum(r['n_sep_end'] > 0 for r in rs)
    st['losses'] = sum(r['loss_t'] >= 0 for r in rs)
    st['loss_A'] = sum(r['loss_net'] == 1 for r in rs); st['loss_R'] = sum(r['loss_net'] == 2 for r in rs)
    T = sum(r['expo'] for r in rs); st['expo'] = T
    lo, hi = poisson_ci(st['losses'])
    st['hazard'] = [st['losses'] / T if T else float('nan'), lo / T if T else float('nan'), hi / T if T else float('nan')]
    st['hazard_upper0'] = 3 / T if T else float('nan')
    inv = Counter()
    for r in rs:
        for k, v in r['inv'].items(): inv[k] += v
    st['inv'] = dict(inv)
    est = [r for r in rs if r['rival_est']]
    st['med_den'] = len(est); st['med'] = sum(r['med_before_end'] for r in est)
    st['b_alive_end'] = sum(r['bridge_alive_end'] for r in rs)
    st['bseed_isl'] = float(np.mean([r['bridge_seed_islands'] for r in rs]))
    st['held_end'] = {t: float(np.mean([r['held_end'][t] for r in rs])) for t in ('0', '1', '2', '3')}
    st['pcc'] = float(np.mean([r['pcc'] for r in rs])); st['pcc_min'] = float(np.min([r['pcc'] for r in rs]))
    sepd = [r for r in rs if r['ever_sep_tag']]
    tl = [r['loss_t'] if r['loss_t'] >= 0 else r['stop_gen'] for r in sepd]
    evs = [r['loss_t'] >= 0 for r in sepd]
    st['km'] = km(tl, evs, MARKS) if sepd else {}
    st['t_loss_med'] = float(np.median([r['loss_t'] for r in rs if r['loss_t'] >= 0])) if st['losses'] else float('nan')
    # separation at end split by bridge fate
    st['sep_end_bridge_dead'] = sum(r['sep_end_tag'] and not r['bridge_alive_end'] for r in rs)
    st['sep_end_bridge_alive'] = sum(r['sep_end_tag'] and r['bridge_alive_end'] for r in rs)
    st['status'] = dict(Counter(r['status'] for r in rs))
    st['hours'] = sum(r['time_s'] for r in rs) / 3600
    return st


def main():
    stat = json.load(open(RK.STATIC))
    calib = json.load(open(RK.CALIB))
    out = dict(static=dict((k, v) for k, v in stat.items() if k not in ('screen_single',)), calib=calib)
    nat = RK.load('nat') + RK.load('nat4')
    cells = defaultdict(list)
    for r in nat:
        cells[(r['arm'], r['mN'])].append(r)
    out['nat'] = {('%s|%g' % k): nat_stats(v) for k, v in sorted(cells.items())}
    B = calib['mN_boundary']
    # paired comparisons at the common mN and at the calibrated values
    if ('free', B['free']) in cells and ('K16', B['free']) in cells:
        out['paired_common'] = dict(
            end=paired(cells[('K16', B['free'])], cells[('free', B['free'])], lambda r: r['n_sep_end'] > 0),
            ever=paired(cells[('K16', B['free'])], cells[('free', B['free'])], lambda r: r['first_sep'] >= 0),
            eff=paired(cells[('K16', B['free'])], cells[('free', B['free'])], lambda r: r['pcc'] >= 0.95))
    pos = RK.load('pos')
    if pos: out['pos'] = pos_stats(pos)
    pst = RK.load('pstar'); pst0 = RK.load('pstar', True)
    fc = {}
    for r in pst:
        fc.setdefault((r['exp'], r['arm']), []).append(r)
    rf = {}
    for r in pst0:
        rf.setdefault((r['exp'], r['arm']), []).append(r)
    out['forced'] = {}
    for k, v in sorted(fc.items()):
        out['forced']['%s|%s' % k] = forced_stats(v, rf.get(k))
    # q_est contrasts (paired seeds)
    for arm in ('K16', 'free'):
        if ('pstar', arm) in fc and ('iid', arm) in fc and ('pstar', arm) in rf and ('iid', arm) in rf:
            out['forced']['pstar|%s' % arm]['dq_vs_iid'] = dq_paired(fc[('pstar', arm)], rf[('pstar', arm)], fc[('iid', arm)], rf[('iid', arm)])
    if ('dctl', 'K16') in fc and ('dctl', 'K16') in rf:
        out['forced']['dctl|K16']['dq_vs_iid'] = dq_paired(fc[('dctl', 'K16')], rf[('dctl', 'K16')], fc[('iid', 'K16')], rf[('iid', 'K16')])
        if ('pstar', 'K16') in fc:
            out['forced']['pstar|K16']['dq_vs_dctl'] = dq_paired(fc[('pstar', 'K16')], rf[('pstar', 'K16')], fc[('dctl', 'K16')], rf[('dctl', 'K16')])
            out['forced']['pstar|K16']['alive_paired_vs_dctl'] = paired(fc[('pstar', 'K16')], fc[('dctl', 'K16')], lambda r: r['lineage_alive_end'])
    cont = RK.load('cont')
    if cont:
        out['cont'] = [dict(arm=r['arm'], mN=r['mN'], rep=r['rep'], status=r['status'], stop=r['stop_gen'], sep_end=r['n_sep_end'],
                            matches=r['matches_1e5'], pairs=r['sep_end_pairs'], sep=r['sep'], hours=r['time_s'] / 3600) for r in cont]
    json.dump(out, open(OUT_JS, 'w'), indent=1, default=str)
    write_md(out, stat, calib)
    print('wrote', OUT_MD, OUT_JS)


def write_md(out, stat, calib):
    L = []
    w = L.append
    w('# Rivals under the bounded prover K: does incompleteness remove the bridge-less obstruction? (`src/rivals_under_k.py`)')
    w('')
    w('Spec `specs/2026-10-05-rivals-under-k.md` (reviewed by gpt-6.1-sol); predictions `predictions/2026-10-05-rivals-under-k.md`. '
      'Modal language L_8 (610 canonical sources) under the free box (GL+Def table) and under K at global budget b (guard at the '
      "reader's own budget; `runs/k-at-n8/kval_n8_b*.npy`). PD, w = 0.3, ε = 0, iid length-prior seeds at n = 8 drawn at source "
      'level and lumped by each arm\'s classes (paired seeds across arms), complete island graph, N = 200, I = 64, generation = I·N '
      'births, horizon 10⁵ (continuation 3·10⁵). **Finite-cutoff (n = 8), finite-horizon evidence about the bridge-less obstruction '
      "relative to FairBot's pair; not a large-population or large-cutoff conclusion; incompatible non-A networks beyond the static "
      'graph, longer bridge paths and larger cutoffs are untested here.** Intervals: Wilson 95% over runs (runs are the independent '
      'units); one-sided 95% upper bounds Clopper–Pearson (≈ 3/n at zero events); hazards exact Poisson, 3/exposure at zero losses; '
      'resolution times right-censored (Kaplan–Meier); q_est by run bootstrap over paired seeds.')
    w('')
    WR = out.get('what_ran')
    if WR:
        w('**What ran.** ' + WR); w('')
    # ---------------- static
    w('## 1. Static screening (n = 8; free, K b = 16, and K b = 4, 54 for budget sensitivity)')
    w('')
    fr = stat['free_reproduction']
    w('**Checks.** Free reproduction: the class table built from the GL+Def table equals `modal.build(8)` (the n = 8 free table '
      '`seeds_in_n` uses): %d classes, names %s, payoffs %s, max |Δμ| %s. Lumping validity (behavioural class = identical directed '
      'row and column; checked exhaustively, every arm): ' % (fr['n_classes_here'], 'equal' if fr['names_equal'] else 'DIFFER',
                                                            'equal' if fr.get('U_equal') else 'DIFFER', e(fr.get('mu_maxdiff'))))
    s = []
    for arm in RK.ARMS:
        lc = stat['lumping'][arm]
        s.append('%s %d classes, %d member violations, mass error %s, seed-draw max |z| %.1f, %d sources tested, mismatches %s' % (
            ARMLAB[arm], lc['n_classes'], lc['members_bad'], e(lc['mass_err']), lc['seed_moment_max_z'], lc['sources_tested'],
            lc['mismatches'] or 0))
    w('; '.join(s) + '. The establisher, rival and direct-bridge tests (existence and mass) were compared between lumped and '
      'source-level tables on **all 610 sources** (the spec\'s 1,000-source sample exceeds the language).')
    w('')
    w('| arm | classes | establishers (μ cut) | rivals (full / half) | rival μ cut [raw] | direct-bridge-less: n, share of rival μ [raw μ] | hard share | no mediator path ≤ 3 (establisher / cooperative graph) | A-faked share | P\\* family share | fixation at N = 200: zero / < 10⁻¹² / positive | at N = 400 |')
    w('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for arm in ('free', 'K16', 'K54', 'K4'):
        S = stat['screen'][arm]; g = S['agg']
        w('| %s | %d | %d (%.4f) | %d (%d / %d) | %s [%s] | %d, **%.3f** [%s] | %.3f | %.3f / %.3f | %.3f | %.3f | %d / %d / %d | %d / %d / %d |' % (
            ARMLAB[arm], S['K'], S['est_n'], S['est_mu'], S['n_rivals'], S['n_full'], S['n_rivals'] - S['n_full'],
            e(S['rival_mu']), e(S['rival_raw']), g['direct_bridgeless']['n'], g['direct_bridgeless']['share'] or 0,
            e(g['direct_bridgeless']['raw']), g['hard_bridgeless']['share'] or 0, g['no_mediator_path']['share'] or 0,
            g['no_mediator_path_coop']['share'] or 0, g['A_faked']['share'] or 0, g['pstar_family']['share'] or 0,
            g['fix200_zero']['n'], g['fix200_below']['n'], g['fix200_positive']['n'],
            g['fix400_zero']['n'], g['fix400_below']['n'], g['fix400_positive']['n']))
    w('')
    w('Rivals of A = {FairBot, `BOX1(THEM(ME))`} (cut μ; bridges = cooperative classes mutually cooperating with FairBot, '
      '`BOX1(THEM(ME))` and R; path = shortest path to A in the establisher mutual-cooperation graph):')
    w('')
    w('| arm | rival | μ | full | P\\* family | direct bridges (μ, heaviest) | mediators | A-faked | path | ρ(R→A_j), ρ(A_j→R) at N = 200 |')
    w('|---|---|---|---|---|---|---|---|---|---|')
    for arm in ('free', 'K16', 'K54', 'K4'):
        for r in stat['screen'][arm]['rivals']:
            w('| %s | `%s` | %s | %s | %s | %d (%s, `%s`) | %d | %s | %s | %s |' % (
                ARMLAB[arm], r['name'], e(r['mu']), 'yes' if r['full'] else 'half', 'yes' if r['pstar_family'] else '',
                r['n_bridges'], e(r['bridge_mass']), r['heaviest_bridge'] or '–', r['n_mediators'], 'yes' if r['A_faked'] else '',
                r['path_est'], ', '.join(e(x) for x in r['fix']['200']['rho'])))
    w('')
    w('**Compatibility / bridge graph** (nodes: establishers and A; edges: mutual cooperation):')
    w('')
    w('| arm | nodes | components (largest) | A\'s component μ / establisher μ | FairBot and `BOX1(THEM(ME))` connected | path length to A: count | by μ | mutually-defecting establisher pairs (n, μ²-mass) |')
    w('|---|---|---|---|---|---|---|---|')
    for arm in ('free', 'K16', 'K54', 'K4'):
        G = stat['screen'][arm]['graph_est']; md = stat['screen'][arm]['md_pairs']
        w('| %s | %d | %d (%s) | %.4f / %.4f | %s | %s | %s | %d, %s |' % (
            ARMLAB[arm], G['nodes'], G['components'], ', '.join(map(str, G['largest'][:4])), G['A_component_mu'], G['est_mu'],
            'yes' if G['A_connected_to_each_other'] else '**no**',
            ', '.join('%s: %d' % (k, v) for k, v in sorted(G['path_hist_count'].items(), key=lambda t: int(t[0]))),
            ', '.join('%s: %s' % (k, e(v)) for k, v in sorted(G['path_hist_mu'].items(), key=lambda t: int(t[0]))),
            md['n'], e(md['mass'])))
    w('')
    w('(path −1 = not connected to A.) **New rivals under K by source identity** (a canonical source that is a rival of A under '
      'K\'s table and not under the free table):')
    w('')
    w('| arm | new rivals: n, cut μ (bridge-less μ) | lost (rival under free, not under K): n, cut μ | kept |')
    w('|---|---|---|---|')
    for arm, v in stat['new_rivals'].items():
        w('| %s | %d, %s (%s) | %d, %s | %d |' % (ARMLAB[arm], v['new']['n'], e(v['new']['cut']), e(v['new']['bridgeless_cut']),
                                               v['lost']['n'], e(v['lost']['cut']), v['kept']['n']))
    w('')
    lost = stat['new_rivals']['K16']['lost']['items']
    w('Lost at b = 16 (sources): ' + ', '.join('`%s` (%s)' % (x['src'], e(x['cut'])) for x in lost) + '. New at b = 4: ' +
      ', '.join('`%s` (%s)' % (x['src'], e(x['cut'])) for x in stat['new_rivals']['K4']['new']['items'][:10]) + ', …')
    w('')
    w('**P\\* under each table** (`and(BOX1(THEM(ME)),not(BOX(THEM(ME))))`):')
    w('')
    w('| arm | class | self-play | vs FairBot (P\\*, FB) | vs `BOX1(THEM(ME))` | row = D\'s row | column ≠ D\'s in | prey μ not D\'s (establishers: n, μ) | D\'s prey not P\\*\'s μ |')
    w('|---|---|---|---|---|---|---|---|---|')
    for arm in ('free', 'K16', 'K54', 'K4'):
        p = stat['pstar'][arm]
        w('| %s | `%s` (%d members) | %s | %s | %s | %s | %d classes | %s (%d, %s) | %s |' % (
            ARMLAB[arm], p['cls'], p['n_members'], 'C' if p['self'] else 'D', ''.join('CD'[1 - x] for x in p['vs_FB']),
            ''.join('CD'[1 - x] for x in p['vs_FB1']), 'yes' if p['row_equals_D_row'] else 'no', p['col_differs_from_D'],
            e(p['prey_not_D_mu']), p['prey_est_n'], e(p['prey_est_mu']), e(p['D_prey_not_pstar_mu'])))
    w('')
    w('**b = 4 supplement** (A is split there): rivals of each member alone.')
    w('')
    w('| arm | reference | rivals | rival μ | direct-bridge-less share | hard share |')
    w('|---|---|---|---|---|---|')
    for k, v in stat.get('screen_single', {}).items():
        arm, ref = k.split('|')
        g = v['agg']
        w('| %s | `%s` | %d | %s | %.3f | %.3f |' % (ARMLAB[arm], ref, v['n_rivals'], e(v['rival_mu']),
                                                g['direct_bridgeless']['share'] or 0, g['hard_bridgeless']['share'] or 0))
    w('')
    # ---------------- calibration
    w('## 2. Calibration (m = 0, N = 200, I = 16, 120 runs per table)')
    w('')
    w('| table | T_nuc (median, 95% bootstrap) | per-island nucleation p | boundary mN = 0.3·N/T_nuc | quartiles |')
    w('|---|---|---|---|---|')
    for arm in ('free', 'K16', 'K4'):
        if arm not in calib['T_nuc']: continue
        dd = calib['dist'][arm]
        w('| %s | %.0f [%.0f, %.0f] | %.3f (%d / %d) | %.3f | %.0f / %.0f / %.0f |' % (
            ARMLAB[arm], calib['T_nuc'][arm], dd['median_ci'][0], dd['median_ci'][1], calib['p'][arm], calib['n_nuc'][arm][0],
            calib['n_nuc'][arm][1], calib['mN_boundary'][arm], dd['25'], dd['50'], dd['75']))
    w('')
    w('Checks are every 5 generations, so T_nuc is resolved to 5. The dimensionless coordinate x = mN·T_nuc/N for each natural cell '
      'is in the next table.')
    w('')
    # ---------------- natural
    w('## 3. (a) Natural runs, matched (N = 200, I = 64, horizon 10⁵)')
    w('')
    w('| table | mN | x = mN·T_nuc/N | runs | ever separated [95%] | **separated at the horizon** [95%] (one-sided 95% upper) | A-rival / non-A at the horizon | direct-bridge-less among horizon separations | island P(C,C) mean (min) | run-level efficient [95%] | cf cross P(C,C), separated runs | worker-hours |')
    w('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for k, st in out['nat'].items():
        arm, mN = k.split('|'); mN = float(mN)
        T = calib['T_nuc'][arm]
        w('| %s | %.3f | %.3f | %d | %s | **%s** (%s) | %d / %d | %d | %.4f (%.3f) | %s | %s | %.2f |' % (
            ARMLAB[arm], mN, mN * T / 200, st['n'], cis(st['ever'], st['n']), ci(st['end'], st['n']), e(st['end_upper95']),
            st['kinds_end'].get('A-rival', 0), st['end'] - st['kinds_end'].get('A-rival', 0), st['bridgeless_end'],
            st['pcc'], st['pcc_min'], cis(st['eff'], st['n']), e(st['cf_sep']), st['hours']))
    w('')
    if 'paired_common' in out:
        pc = out['paired_common']
        w('**Paired at the common mN** (same source-level seeds in both tables): horizon separation K only %d, free only %d, both %d; '
          'ever separated K only %d, free only %d, both %d; run-level efficient K only %d, free only %d (of %d paired runs).' % (
              pc['end']['a_only'], pc['end']['b_only'], pc['end']['both'], pc['ever']['a_only'], pc['ever']['b_only'],
              pc['ever']['both'], pc['eff']['a_only'], pc['eff']['b_only'], pc['eff']['n']))
        w('')
    w('Separations by rival (first separation of each ever-separated run; at the horizon):')
    w('')
    w('| table | mN | ever: kinds | ever: A-rivals | horizon: A-rivals | bridge fate (first separation) | resolved / censored | KM P(still separated) at 10² / 10³ / 10⁴ / 10⁵ after first separation | median time to resolution | episodes |')
    w('|---|---|---|---|---|---|---|---|---|---|')
    for k, st in out['nat'].items():
        arm, mN = k.split('|')
        w('| %s | %s | %s | %s | %s | %s | %d / %d | %s | %s | %s |' % (
            ARMLAB[arm], mN, st['kinds_ever'] or '–', ', '.join('`%s` %d' % kv for kv in st['rivals_ever'].items()) or '–',
            ', '.join('`%s` %d' % kv for kv in st['rivals_end'].items()) or '–', st['bridge_fate'] or '–', st['resolved'], st['censored'],
            ' / '.join('%.2f' % st['km'].get(m, float('nan')) for m in MARKS[:4]) if st['km'] else '–',
            e(st['dur_resolved_median']), st['episodes'] or '–'))
    w('')
    w('Per-separation tracking (every run ever separated; "first" = first separation, "end" = at the horizon; bridges = cooperative '
      'classes in the support mutually cooperating with both holders; A-bridges = the spec\'s pairwise bridges of (A, R)):')
    w('')
    w('| table | mN | rep | first sep gen | resolved at (−1: separated at the horizon) | when | pair | kind | rival bridge-less | bridge classes | bridge copies / islands at seeding | A-bridge copies at seeding | bridge alive at end | mediations (first gen) | islands held a / b |')
    w('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for k, st in out['nat'].items():
        arm, mN = k.split('|')
        for sr in st['sep_rows']:
            for s in sr['seps']:
                w('| %s | %s | %d | %d | %d | %s | `%s` / `%s` | %s | %s | %d | %d / %d | %s | %s | %d (%d) | %d / %d |' % (
                    ARMLAB[arm], mN, sr['rep'], sr['sep']['first'], sr['sep']['resolved_at'], s['when'], s['a'], s['b'], s['kind'],
                    s.get('rival_bridgeless', '–'), s['n_bridge_classes'], s['bridge_seed'], s['bridge_seed_islands'],
                    s.get('A_bridge_seed', '–'), s['bridge_alive_end'], s['mediations'], s['t_first_med'], s['held_a'], s['held_b']))
    w('')
    # ---------------- positive control
    if 'pos' in out:
        p = out['pos']
        w('## 4. (b) Positive control: the heaviest bridged rival of A under K b = 16, forced densely')
        w('')
        w('Rival `%s` (a half-rival: mutual defection with `BOX1(THEM(ME))`, mutual cooperation with FairBot), one copy per island '
          'replacing a uniformly chosen seed; kernel tags for (`BOX1(THEM(ME))`, R): 1 = A\'s network, 2 = R\'s, 3 = bridge. mN = %.3f.' % (p['forced'], p['mN']))
        w('')
        w('| runs | rival established | ever separated | **horizon separated** [95%] | separated with bridge dead / alive | losses (A / R) / exposure, hazard [95%] | R-island losses 2>1 / 2>3 / 2>0 | **mediation-before-loss** [95%] | bridge alive at end | island P(C,C) (min) | KM after separation at 10³ / 10⁴ / 10⁵ |')
        w('|---|---|---|---|---|---|---|---|---|---|---|')
        w('| %d | %s | %s | **%s** | %d / %d | %d (%d / %d) / %s, %s [%s, %s] | %d / %d / %d | **%s** | %d | %.4f (%.3f) | %s |' % (
            p['n'], cis(p['rival_est'], p['n']), cis(p['ever_sep'], p['n']), cis(p['sep_end'], p['n']), p['sep_end_bridge_dead'],
            p['sep_end_bridge_alive'], p['losses'], p['loss_A'], p['loss_R'], e(p['expo']), e(p['hazard'][0]), e(p['hazard'][1]),
            e(p['hazard'][2]), p['inv'].get('2>1', 0), p['inv'].get('2>3', 0), p['inv'].get('2>0', 0), cis(p['med'], p['med_den']),
            p['b_alive_end'], p['pcc'], p['pcc_min'], ' / '.join('%.2f' % p['km'].get(m, float('nan')) for m in (1000, 10000, 100000))))
        w('')
    # ---------------- forced P*
    if out.get('forced'):
        w('## 5. (c) Forced P\\* with the inert-defector control (one founder per island, replacing a uniformly chosen seed)')
        w('')
        w('The forced founders are followed as a lineage (a duplicate column of their class, tagged; tags have no dynamic effect). '
          '**Cooperative establishment** = an island certified cooperative whose holder is the lineage; **lineage survival** = the '
          'lineage present at the horizon in any state. q_est = local establishments / the paired m = 0 reference (same initial states).')
        w('')
        w('| cell | table | mN | runs | cooperative establishment: runs (islands) | holder at the end, certified: runs | **lineage alive at the horizon** [95%] | lineage extinction gen quartiles 25/50/75/90 | max copies (mean) | max islands held (mean) | q_est [95%] | Δq_est vs iid [95%] | Δq_est vs D control | horizon separated | island P(C,C) (min) |')
        w('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        for k, st in out['forced'].items():
            exp, arm = k.split('|')
            lab = {'pstar': 'forced P\\*', 'dctl': 'forced D (inert control)', 'iid': 'iid control'}[exp]
            q = st.get('q_est', [float('nan')] * 3)
            dqi = st.get('dq_vs_iid'); dqd = st.get('dq_vs_dctl')
            if 'alive_end' in st:
                w('| %s | %s | %.3f | %d | %d (%d) | %d | **%s** | %s | %.1f | %.1f | %.2f [%.2f, %.2f] | %s | %s | %s | %.4f (%.3f) |' % (
                    lab, ARMLAB[arm], st['mN'], st['n'], st['coop_est_runs'], st['coop_est_islands'], st['coop_hold_end_runs'],
                    cis(st['alive_end'], st['n']), ' / '.join(e(x) if x < 1e8 else 'alive' for x in st['ext_q']),
                    st['lineage_max_mean'], st['lineage_held_max_mean'], q[0], q[1], q[2],
                    ('%+.3f [%+.3f, %+.3f]' % (dqi[0], dqi[1][0], dqi[1][1])) if dqi else '–',
                    ('%+.3f [%+.3f, %+.3f]' % (dqd[0], dqd[1][0], dqd[1][1])) if dqd else '–',
                    cis(st['sep_end'], st['n']), st['pcc'], st['pcc_min']))
            else:
                w('| %s | %s | %.3f | %d | – | – | – | – | – | – | %.2f [%.2f, %.2f] | – | – | %s | %.4f (%.3f) |' % (
                    lab, ARMLAB[arm], st['mN'], st['n'], q[0], q[1], q[2], cis(st['sep_end'], st['n']), st['pcc'], st['pcc_min']))
        w('')
        ap = out['forced'].get('pstar|K16', {}).get('alive_paired_vs_dctl')
        if ap:
            w('Paired (same seeds and founder islands): P\\* alive and D dead %d, D alive and P\\* dead %d, both alive %d, of %d.' % (
                ap['a_only'], ap['b_only'], ap['both'], ap['n']))
            w('')
    # ---------------- continuation
    if out.get('cont'):
        w('## 6. (e) Continuation of every separated, unresolved natural run to 3·10⁵ generations')
        w('')
        w('Same initial state and kernel stream with a longer check schedule (identical up to 10⁵); "matches" = the 10⁵ check row '
          'equals the original run\'s final row.')
        w('')
        w('| table | mN | rep | matches | status at 3·10⁵ | separated at 3·10⁵ | pairs | worker-hours |')
        w('|---|---|---|---|---|---|---|---|')
        for c in out['cont']:
            w('| %s | %.3f | %d | %s | %s | %d | %s | %.2f |' % (ARMLAB[c['arm']], c['mN'], c['rep'], c['matches'], c['status'],
                                                         c['sep_end'], '; '.join('`%s` / `%s`' % tuple(p) for p in c['pairs'][:2]), c['hours']))
        w('')
    V = out.get('verdicts_md')
    if V:
        w(V)
    open(OUT_MD, 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
