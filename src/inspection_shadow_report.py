"""Report for the inspection-shadow experiment: reads runs/inspection_shadow/*, scores the predictions of
predictions/2026-10-24-inspection-shadow.md under the conventions fixed there, writes runs/inspection-shadow.md and .json.

    python3 src/inspection_shadow_report.py

Chain numbers are eps -> 0 whole-space objects; lottery numbers are eps = 0 finite-(N, I, horizon) statistics (with the declared rain
in the rain cells).  Run-clustered 95% intervals: 4,000 bootstrap resamples of runs (paired contrasts resample runs jointly).
"""
import os, sys, math, json, gzip
from collections import Counter
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inspection_shadow as S

ROOT = S.ROOT
RUNS = os.environ.get('INSPECTION_SHADOW_OUT', os.path.join(ROOT, 'runs', 'inspection_shadow'))
OUTMD = os.environ.get('INSPECTION_SHADOW_MD', os.path.join(ROOT, 'runs', 'inspection-shadow.md'))
OUTJS = OUTMD[:-3] + '.json'
BOOT = 4000
rng_seed = 20261024


def exists(*p):
    return os.path.exists(os.path.join(RUNS, *p))


def chain(arm, c, variant, N):
    f = 'chain_%s_c%g_%s_N%d.json' % (arm, c, variant, N)
    return S.jload(os.path.join(RUNS, f)) if exists(f) else None


def lot(name):
    f = 'lot_%s.json.gz' % name
    return S.jload(os.path.join(RUNS, f)) if exists(f) else None


def direct(arm, c, N, base, ninj, karr):
    f = 'direct_%s_c%g_N%d_%s_inj%d_K%d.json' % (arm, c, N, base, ninj, karr)
    return S.jload(os.path.join(RUNS, f)) if exists(f) else None


def vals(L, key, g):
    out = []
    for r in L['runs']:
        v = r['stats'].get(str(g), {}).get(key)
        out.append(np.nan if v is None else v)
    return np.array(out, float)


def window(L, key, T, N):
    """mean over the checkpoints of the last N generations (every N/10)."""
    out = []
    for r in L['runs']:
        xs = [r['stats'][str(g)].get(key) for g in r['cps'] if T - N <= g <= T and key in r['stats'][str(g)]]
        xs = [x for x in xs if x is not None]
        out.append(np.mean(xs) if xs else np.nan)
    return np.array(out, float)


def boot(x, B=BOOT):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return (np.nan, np.nan, np.nan)
    rng = np.random.default_rng(rng_seed)
    idx = rng.integers(0, len(x), (B, len(x)))
    m = x[idx].mean(1)
    return (float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5)))


def pdiff(a, b, B=BOOT):
    """paired difference a - b over runs (arrays aligned by run), mean and run-clustered CI."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    return boot((a - b)[ok], B)


def fmt(t, d=3):
    if t is None or not np.isfinite(t[0]):
        return 'n/a'
    return '%.*f [%.*f, %.*f]' % (d, t[0], d, t[1], d, t[2])


def lsslope(Ns, ys):
    ok = [(n, y) for n, y in zip(Ns, ys) if y is not None and y > 0]
    if len(ok) < 2:
        return None
    return float(np.polyfit(np.log([n for n, _ in ok]), np.log([y for _, y in ok]), 1)[0])


def main():
    md = ['# The inspection game\'s enforcer and its shadow (run report, 2026-10-24)\n',
          'Spec `specs/2026-10-24-inspection-shadow.md`; predictions `predictions/2026-10-24-inspection-shadow.md`; notes '
          '`notes/inspection-shadow.md`; code `src/inspection_shadow*.py`; rows `runs/inspection_shadow/`. **Chain** = the ε → 0 object '
          '(π over pairs of monomorphic role classes, the whole state space of 157² or 167² pairs, no exploration cap); **lottery** = the '
          'ε = 0 seed lottery at the stated (N, I), mN, horizon 20N, with the declared rain in the rain cells; never π. Payoffs are game payoffs '
          '(gross of the price). Intervals are run-clustered 95% bootstrap (4,000 resamples).\n']
    R = {}
    # ------------------------------------------------------------------ completeness
    jobs = [l.split('|') for l in open(os.path.join(RUNS, 'jobs.txt')) if l.strip()]
    missing = [j[2].strip() for j in jobs if not exists(j[2].strip())]
    R['completeness'] = dict(n_jobs=len(jobs), n_missing=len(missing), missing=missing)
    md.append('## Completeness\n')
    md.append('%d of %d jobs of the job file have an output.%s\n' % (len(jobs) - len(missing), len(jobs), '' if not missing else ' Missing: ' + ', '.join(missing) + '.'))

    # ------------------------------------------------------------------ static and positive controls
    st = S.jload(os.path.join(RUNS, 'static.json')) if exists('static.json') else None
    if st:
        md.append('## Statics: twin relation, sets, prudent class, priors\n')
        for c in ('0', '0.01'):
            d = st['exact_c' + c]
            tw = d['twin']
            md.append('- c = %s: K = %s; |E| = %d, |R| = %d, |R*| = %d pair states. Twins of the net payoff of `N` against `C`: %d classes, mass %.5f '
                      '(`N` %.5f, deterring %.5f, other %.5f). Net payoffs (inspector, inspectee): (CRI, C) = (%.2f, %.2f) with %.0f level charged; (N, C) = (%.2f, %.2f) '
                      'with %.0f.' % (c, d['K'], d['sizes']['E'], d['sizes']['R'], d['sizes']['Rstar'], tw['n_classes'], tw['mass'], tw['mass_N'], tw['mass_deterring'],
                                     tw['mass_nondeterring_other'], tw['u_CRI_C'][0], tw['u_CRI_C'][1], tw['cost_CRI_vs_C'], tw['u_N_C'][0], tw['u_N_C'][1], tw['cost_N_vs_C']))
        d = st['exact_c0']
        md.append('- Prudent class (eight classes, 38 spellings, mass %.6f): ' % d['priors']['boost']['mS'] + '; '.join('`%s` (cost %g vs CRI, %g vs N)' % (x['cls'], x['cost_vs_CRI'], x['cost_vs_N']) for x in d['prudent']) + '.')
        md.append('- Boost x10: m(S) %.6f → %.6f, added mass %.6f taken from all other inspectee classes; control: the same %.6f added to `C` (%.5f → %.5f), taken from all classes outside `C`.\n' % (
            d['priors']['boost']['mS'], d['priors']['boost']['m_new_S'], d['priors']['boost']['delta'], d['priors']['control']['delta'],
            d['priors']['control']['m_new_C'] - d['priors']['control']['delta'], d['priors']['control']['m_new_C']))
        R['static'] = st
        md.append('- `lottery3` equals `mixed2.lottery2` when no rain or arrival is used: **%s**; weighted founders at factor 1 equal the unweighted draw: **%s**.\n' % (st['lottery3_equals_lottery2'], st['founders_factor1_equal']))

    # (the remaining sections are built by the functions below)
    sections = [chain_sections, lottery_sections, remedy_sections, control_sections, verdict_section]
    ctx = dict(md=md, R=R)
    for f in sections:
        f(ctx)
    open(OUTMD, 'w').write('\n'.join(md) + '\n')
    S.jdump(R, OUTJS)
    print('wrote', OUTMD, OUTJS)


def A_m(st, key):
    return float('nan')


CAT_SHORT = {'A_neutral_shadow': 'A neutral shadow', 'B_neutral_other': 'B neutral other', 'C_strict_K': 'C strict K', 'D_strict_other_nonreader': 'D strict non-reading inspectee',
             'E_strict_reader_clean': 'E strict reading inspectee (clean)', 'E_strict_reader_forfeit': 'E strict reading inspectee (forfeit-driven)',
             'F_strict_inspector': 'F strict inspector', 'G_deleterious': 'G deleterious'}
NS = (100, 1000, 10000, 100000)
OLD_CHAIN = {(0.0, 100): -0.777, (0.0, 1000): -0.496, (0.0, 10000): -0.471, (0.01, 1000): -0.632, (0.01, 10000): -0.623}      # RESULTS "Mixed actions in two-role games"


def hz(res, X, cat):
    v = res['exits'][X]['cats'][cat]['hazard']
    return v


def chain_sections(ctx):
    md, R = ctx['md'], ctx['R']
    R['chain'] = {}
    for c in (0.0, 0.01):
        rows = {N: chain('exact', c, 'base', N) for N in NS}
        rows = {N: r for N, r in rows.items() if r is not None}
        if not rows:
            continue
        key = 'c%g' % c
        R['chain'][key] = {}
        md.append('## Chain, exact arm, c = %g (whole state space, ε → 0)\n' % c)
        md.append('| N | π(E) | odds E | π(R) | π(R*) | π(E*) | mean inspector payoff | mean inspectee payoff | inspection prob | cheat prob | forfeit mass in E | peak RSS GB | check vs two-role run |\n|' + '---|' * 13)
        for N, r in rows.items():
            old = OLD_CHAIN.get((c, N))
            md.append('| %d | %.4f | %.4g | %.4f | %.4f | %.4f | %.4f | %.4f | %.3f | %.3f | %.2e | %.1f | %s |' % (
                N, r['pi_sets']['E'], r['odds_E'], r['pi_sets']['R'], r['pi_sets']['Rstar'], r['pi_sets']['Estar'], r['stat']['u0g'], r['stat']['u1g'], r['stat']['p_insp'],
                r['stat']['q_cheat'], r['pi_E_forfeit_mass'], r.get('rss_peak_gb', float('nan')), ('%.3f vs %.3f' % (r['stat']['u0g'], old)) if old is not None else '-'))
            R['chain'][key][str(N)] = dict(pi_E=r['pi_sets']['E'], pi_R=r['pi_sets']['R'], pi_Rstar=r['pi_sets']['Rstar'], pi_Estar=r['pi_sets']['Estar'], odds_E=r['odds_E'],
                                           u0g=r['stat']['u0g'], u1g=r['stat']['u1g'], p=r['stat']['p_insp'], q=r['stat']['q_cheat'])
        Ns = sorted(rows)
        sl = lsslope([N for N in Ns if N >= 1000], [rows[N]['odds_E'] for N in Ns if N >= 1000])
        R['chain'][key]['odds_E_slope_1e3_1e5'] = sl
        md.append('\nOdds of E: least-squares slope of log odds on log N over N ≥ 10³: %s.\n' % ('n/a' if sl is None else '%.3f' % sl))
        for X in ('R', 'E'):
            md.append('**Conditional exit hazard from %s** (per mutation event; flux / π(%s)), by category:\n' % (X, X))
            md.append('| category | ' + ' | '.join('N = %d' % N for N in Ns) + ' | slope (N ≥ 10³) |\n|' + '---|' * (len(Ns) + 2))
            R['chain'][key]['hazard_' + X] = {}
            for cat, nm in CAT_SHORT.items():
                vals_ = [hz(rows[N], X, cat) for N in Ns]
                sl_ = lsslope([N for N in Ns if N >= 1000], [hz(rows[N], X, cat) for N in Ns if N >= 1000])
                md.append('| %s | ' % nm + ' | '.join('%.3e' % v if v else '0' for v in vals_) + ' | %s |' % ('n/a' if sl_ is None else '%.2f' % sl_))
                R['chain'][key]['hazard_' + X][cat] = dict(values={str(N): v for N, v in zip(Ns, vals_)}, slope=sl_)
            tot = [rows[N]['exits'][X]['hazard'] for N in Ns]
            md.append('| **total** | ' + ' | '.join('%.3e' % v for v in tot) + ' | %s |' % ('n/a' if lsslope([N for N in Ns if N >= 1000], [rows[N]['exits'][X]['hazard'] for N in Ns if N >= 1000]) is None else '%.2f' % lsslope([N for N in Ns if N >= 1000], [rows[N]['exits'][X]['hazard'] for N in Ns if N >= 1000])))
            md.append('| largest | ' + ' | '.join(CAT_SHORT[rows[N]['exits'][X]['largest']].split(' ')[0] if rows[N]['exits'][X]['largest'] else '-' for N in Ns) + ' | |')
            md.append('')
            R['chain'][key]['largest_' + X] = {str(N): rows[N]['exits'][X]['largest'] for N in Ns}
        md.append('Strict inspectee flux out of E by the resident inspector (deterring / not deterring K): ' + '; '.join(
            'N = %d: %.2e / %.2e' % (N, rows[N]['exits']['E']['strict_inspectee_from']['deterring_inspector'], rows[N]['exits']['E']['strict_inspectee_from']['nondeterring_inspector']) for N in Ns) + '.\n')
        md.append('**Renewal identities** (exact; mutation events): mean sojourn in R, mean time outside R, mean sojourn in E, mean time outside E:\n')
        md.append('| N | sojourn R | outside R | sojourn E | outside E |\n|---|---|---|---|---|')
        for N in Ns:
            r = rows[N]
            md.append('| %d | %.4g | %.4g | %.4g | %.4g |' % (N, r['renewal_R']['mean_sojourn'], r['renewal_R']['mean_time_outside'], r['renewal_E']['mean_sojourn'], r['renewal_E']['mean_time_outside']))
        md.append('')
        md.append('**Where π sits outside E** (occupancy of the detour categories; exclusive, in this order): ' + '\n')
        md.append('| N | E | ' + ' | '.join(S.OCC_ORDER) + ' |\n|' + '---|' * (len(S.OCC_ORDER) + 2))
        for N in Ns:
            o = rows[N]['occupancy']
            md.append('| %d | %.4f | ' % (N, o['E']) + ' | '.join('%.4f' % o[k] for k in S.OCC_ORDER) + ' |')
        md.append('')
        R['chain'][key]['occupancy'] = {str(N): rows[N]['occupancy'] for N in Ns}
        md.append('**First passage into E and into R** from the named states (exact, same elimination pass; mutation events; P(R) = probability that the first E state entered is in R):\n')
        for N in Ns:
            fp = rows[N].get('first_passage')
            if not fp:
                continue
            md.append('N = %d:' % N)
            md.append('| start | P(first entry in R) | mean time to E | mean time to R | time to E in: shadow excursion / cheater-major / light cheater / committed / mixing / forfeit | visits |\n|---|---|---|---|---|---|')
            for lab, d in fp.items():
                rw = d['reward']
                md.append('| %s | %.4f | %.4g | %s | %.3g / %.3g / %.3g / %.3g / %.3g / %.3g | %.3g |' % (
                    lab, d['P_first_entry_in_R'], d['mean_time_to_E'], ('%.4g' % d['mean_time_to_R']) if 'mean_time_to_R' in d else 'n/a', rw['time_shadow_excursion'], rw['time_cheater_major_other'],
                    rw['time_light_cheater'], rw['time_committed_compliant'], rw['time_mixing'], rw['time_forfeit'], rw['visits']))
            md.append('')
            R['chain'][key].setdefault('first_passage', {})[str(N)] = fp
        # contributors and top states at the middle N
        for N in (10000,):
            if N in rows:
                r = rows[N]
                md.append('Top contributors to the flux out of R at N = %d: ' % N + '; '.join('%s `%s` (%s) %.1f%%' % ('inspector' if t['role'] == 0 else 'inspectee', t['cls'], t['fate'], 100 * t['share']) for t in r['exits']['R']['top'][:8]) + '.')
                md.append('Top contributors to the flux out of E at N = %d: ' % N + '; '.join('%s `%s` (%s) %.1f%%' % ('inspector' if t['role'] == 0 else 'inspectee', t['cls'], t['fate'], 100 * t['share']) for t in r['exits']['E']['top'][:8]) + '.')
                md.append('Top states at N = %d: ' % N + '; '.join('(%s, %s) %.3f%s' % (t['insp'], t['ee'], t['pi'], ' [R]' if t['in_R'] else (' [E]' if t['in_E'] else '')) for t in r['top_states'][:8]) + '.')
                md.append('Support: %d pair states carry 0.99 of π (of %d); balance residual %.1e, circulation index %.3f.\n' % (r['n_states_for_099'], r['S'], r['balance']['max_rel_residual'], r['balance']['circulation']))
        # ratios 1/N and crossover
        Nh = [N for N in Ns if N >= 100]
        md.append('Reference one-state hazards at (CRI, C) (notes §1.2): ' + '; '.join('N = %d: neutral %.2e, strict inspectee %.2e' % (
            N, rows[N]['reference_exits']['(CRI,C)']['inspector']['neutral'], rows[N]['reference_exits']['(CRI,C)']['inspectee']['strict']) for N in Nh) + '.\n')


SIZE_LABEL = {'n100i64': (100, 64), 'n400i16': (400, 16), 'n800i8': (800, 8), 'n400i64': (400, 64)}
SIZE_T = {'n100i64': 2000, 'n400i16': 8000, 'n800i8': 16000, 'n400i64': 8000}


def lab_of(code):
    zp, zq, rd = code // 6, (code % 6) // 2, code % 2
    if zp == 2 and zq == 0:
        return 'R' if rd == 1 else 'C'
    if zp == 0 and zq == 0:
        return 'N'
    if zp == 0 and zq == 2:
        return 'K'
    if zp == 2 and zq == 2:
        return 'IK'
    return 'other'


def phase_summary(L, T, N):
    """label occupancy at the horizon and the switching rate of islands over the last N generations (checkpoints every N/10)."""
    occ = Counter(); sw = 0; obs = 0
    for r in L['runs']:
        cps = r['cps']
        if not r['phases']:
            continue
        ph = np.array(r['phases'])
        labs = np.vectorize(lab_of)(ph)
        occ.update(labs[-1].tolist())
        idx = [i for i, g in enumerate(cps) if T - N <= g <= T]
        for i, j in zip(idx[:-1], idx[1:]):
            sw += int((labs[i] != labs[j]).sum()); obs += labs.shape[1]
    tot = sum(occ.values())
    return dict(occupancy={k: v / tot for k, v in sorted(occ.items())}, switches_per_island_per_N_generations=(sw / obs if obs else None), n_runs=len(L['runs']))


LOT_KEYS = [('isl_efficient', 'efficient islands E'), ('isl_Estar', 'E* islands'), ('isl_eff_resp', 'efficient, responsive inspectors'), ('isl_eff_shadow', 'efficient, shadow'),
            ('isl_commit_comply', 'committed and compliant'), ('isl_light', 'light-cheater islands'), ('isl_cheat_majority', 'cheater-majority'),
            ('u0g', 'inspector payoff'), ('u1g', 'inspectee payoff'), ('p_insp', 'inspection prob'), ('q_cheat', 'cheat prob'), ('f0', 'forfeit (inspector)'), ('f1', 'forfeit (inspectee)'),
            ('sh_0:CRI', 'share cr(THEM(ME)) class'), ('sh_0:N', 'share N'), ('sh_1:K', 'share K'), ('sh_1:C', 'share C'), ('rd1', 'reading inspectees'), ('prud_mass', 'prudent-class mass'),
            ('resp_mass', 'responsive inspector mass')]


def lot_table(md, name, L, T, N, keys=LOT_KEYS):
    out = {}
    md.append('**%s** (%d runs; N = %d, I = %d, horizon %d, mN = %g%s%s): horizon value [95%% CI]; value at generation 2,000; mean over the last N generations\n' % (
        name, len(L['runs']), L['N'], L['I'], T, L['mN'], ', rain %s' % (L['rain'],) if L.get('rain') else '', ', prior %s' % L['variant'] if L.get('variant') not in (None, 'base') else ''))
    md.append('| statistic | horizon | gen 2,000 | last-N window |\n|---|---|---|---|')
    for k, nm in keys:
        v = vals(L, k, T)
        if not np.isfinite(v).any():
            continue
        v2 = vals(L, k, 2000) if T != 2000 else v
        w = window(L, k, T, N)
        out[k] = dict(horizon=boot(v), g2000=boot(v2), window=float(np.nanmean(w)))
        md.append('| %s | %s | %s | %.3f |' % (nm, fmt(boot(v)), fmt(boot(v2)) if np.isfinite(v2).any() else 'n/a', np.nanmean(w)))
    md.append('')
    return out


def traj_row(L, key, grid):
    return [float(np.nanmean(vals(L, key, g))) if str(g) in L['runs'][0]['stats'] else float('nan') for g in grid]


def lottery_sections(ctx):
    md, R = ctx['md'], ctx['R']
    R['lottery'] = {}
    md.append('## Lottery size path (exact arm; ε = 0 seed lottery; mN = 1; horizon 20N)\n')
    summary = []
    for c in (0.0, 0.01):
        for sz, (N, I) in SIZE_LABEL.items():
            L = lot('exact-c%g-%s-base' % (c, sz))
            if L is None:
                continue
            T = SIZE_T[sz]
            key = 'exact_c%g_%s' % (c, sz)
            R['lottery'][key] = lot_table(md, key, L, T, N)
            ph = phase_summary(L, T, N)
            R['lottery'][key]['phases'] = ph
            md.append('Ladder labels at the horizon (R reader+committed, C constants+committed, N lax+compliant, K lax+cheating, IK committed+cheating): ' + ', '.join('%s %.3f' % kv for kv in ph['occupancy'].items()) +
                      '; island label switches per island over the last N generations: %.3f.\n' % (ph['switches_per_island_per_N_generations'] if ph['switches_per_island_per_N_generations'] is not None else float('nan')))
            tgrid = [g for g in (100, 500, 1000, 2000, 4000, 8000, 16000) if g <= T]
            ngrid = [int(round(N * x)) for x in (1, 2, 5, 10, 20)]
            md.append('Efficient islands at common t: ' + ', '.join('t=%d: %.3f' % (g, v) for g, v in zip(tgrid, traj_row(L, 'isl_efficient', tgrid))) + '; at t/N: ' +
                      ', '.join('%d: %.3f' % (g // N, v) for g, v in zip(ngrid, traj_row(L, 'isl_efficient', ngrid))) + '.\n')
            R['lottery'][key]['traj_t'] = dict(zip(map(str, tgrid), traj_row(L, 'isl_efficient', tgrid)))
            R['lottery'][key]['traj_tN'] = dict(zip(['%d' % (g // N) for g in ngrid], traj_row(L, 'isl_efficient', ngrid)))
            summary.append((c, sz, boot(vals(L, 'isl_efficient', T)), boot(vals(L, 'isl_efficient', 2000)), float(np.nanmean(vals(L, 'f0', T))), float(np.nanmean(vals(L, 'f1', T)))))
    md.append('**Efficient islands along the path** (path effects: N, I and the horizon move together; (400, 64) crosses (400, 16) and (100, 64) at fixed I or N):\n')
    md.append('| c | cell | efficient at horizon | efficient at gen 2,000 | forfeit inspector / inspectee at horizon |\n|---|---|---|---|---|')
    for c, sz, h, g2, f0, f1 in summary:
        md.append('| %g | %s | %s | %s | %.3f / %.3f |' % (c, sz, fmt(h), fmt(g2), f0, f1))
    md.append('')
    R['lottery_summary'] = [dict(c=c, cell=sz, horizon=h, g2000=g2, f0=f0, f1=f1) for c, sz, h, g2, f0, f1 in summary]


def remedy_sections(ctx):
    md, R = ctx['md'], ctx['R']
    R['remedies'] = {}
    md.append('## Remedies (lottery cells; rain is ε N = 0.05 mutants per generation per island into the inspectee seat)\n')
    for c in (0.0, 0.01):
        for sz in ('n400i16', 'n100i64'):
            N, I = SIZE_LABEL[sz]; T = SIZE_T[sz]
            Ls = {rem: lot('exact-c%g-%s-%s' % (c, sz, rem)) for rem in ('base', 'rainK', 'rainC', 'boost', 'boostctl')}
            if all(v is None for v in Ls.values()):
                continue
            md.append('**c = %g, %s**: efficient islands E and related statistics at the horizon %d\n' % (c, sz, T))
            md.append('| cell | E | E* | efficient+responsive | efficient+shadow | committed+compliant | light-cheater | inspector payoff | cheat prob | prudent mass |\n|' + '---|' * 10)
            rec = {}
            for rem, L in Ls.items():
                if L is None:
                    continue
                g = lambda k: fmt(boot(vals(L, k, T)))
                md.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (rem, g('isl_efficient'), g('isl_Estar'), g('isl_eff_resp'), g('isl_eff_shadow'),
                                                                                     g('isl_commit_comply'), g('isl_light'), g('u0g'), g('q_cheat'), g('prud_mass')))
                rec[rem] = {k: boot(vals(L, k, T)) for k in ('isl_efficient', 'isl_Estar', 'isl_eff_resp', 'isl_eff_shadow', 'isl_commit_comply', 'isl_light', 'u0g', 'q_cheat')}
            diffs = {}
            for a, b, nm in (('rainK', 'rainC', 'K rain minus matched C rain'), ('boost', 'boostctl', 'prudent x10 minus matched C control'), ('rainK', 'base', 'K rain minus base'), ('rainC', 'base', 'C rain minus base')):
                if Ls.get(a) is not None and Ls.get(b) is not None:
                    d = pdiff(vals(Ls[a], 'isl_efficient', T), vals(Ls[b], 'isl_efficient', T))
                    d2 = pdiff(vals(Ls[a], 'isl_efficient', 2000), vals(Ls[b], 'isl_efficient', 2000)) if T != 2000 else d
                    dr = pdiff(vals(Ls[a], 'isl_eff_resp', T), vals(Ls[b], 'isl_eff_resp', T))
                    diffs[nm] = dict(efficient_horizon=d, efficient_g2000=d2, eff_resp_horizon=dr)
                    md.append('- %s: efficient islands %s (gen 2,000: %s); efficient+responsive %s.' % (nm, fmt(d), fmt(d2), fmt(dr)))
            md.append('')
            R['remedies']['c%g_%s' % (c, sz)] = dict(cells=rec, diffs=diffs)
    md.append('### Chain remedy (prior change, N = 10^4; whole state space)\n')
    md.append('| c | prior | π(E) | π(R) | mean inspector payoff | π(E) minus control |\n|---|---|---|---|---|---|')
    R['remedies']['chain'] = {}
    for c in (0.0, 0.01):
        rows = {v: chain('exact', c, v, 10000) for v in ('base', 'boost', 'control')}
        if rows['boost'] is None and rows['control'] is None:
            continue
        ctl = rows['control']['pi_sets']['E'] if rows['control'] else None
        for v, r in rows.items():
            if r is None:
                continue
            md.append('| %g | %s | %.4f | %.4f | %.4f | %s |' % (c, v, r['pi_sets']['E'], r['pi_sets']['R'], r['stat']['u0g'], ('%.4f' % (r['pi_sets']['E'] - ctl)) if ctl is not None else 'n/a'))
        eff = (rows['boost']['pi_sets']['E'] - rows['control']['pi_sets']['E']) if rows['boost'] and rows['control'] else None
        effR = (rows['boost']['pi_sets']['R'] - rows['control']['pi_sets']['R']) if rows['boost'] and rows['control'] else None
        R['remedies']['chain']['c%g' % c] = dict(effect_E=eff, effect_R=effR, rows={v: (r['pi_sets'] if r else None) for v, r in rows.items()})
    md.append('')


def control_sections(ctx):
    md, R = ctx['md'], ctx['R']
    R['controls'] = {}
    md.append('## Controls\n')
    md.append('### Blind arm (no program reads) and inspector-only reading (`exact_er`) in the lottery\n')
    md.append('| cell | efficient islands (horizon) | efficient (gen 2,000) | inspector payoff | cheat prob | committed+compliant |\n|---|---|---|---|---|---|')
    for arm, cs in (('blind', (0.0,)), ('exact_er', (0.0, 0.01))):
        for c in cs:
            for sz, (N, I) in SIZE_LABEL.items():
                L = lot('%s-c%g-%s-base' % (arm, c, sz))
                if L is None:
                    continue
                T = SIZE_T[sz]
                md.append('| %s c=%g %s | %s | %s | %s | %s | %s |' % (arm, c, sz, fmt(boot(vals(L, 'isl_efficient', T))), fmt(boot(vals(L, 'isl_efficient', 2000))), fmt(boot(vals(L, 'u0g', T))),
                                                                  fmt(boot(vals(L, 'q_cheat', T))), fmt(boot(vals(L, 'isl_commit_comply', T)))))
                R['controls']['%s_c%g_%s' % (arm, c, sz)] = dict(eff=boot(vals(L, 'isl_efficient', T)), u0g=boot(vals(L, 'u0g', T)))
    md.append('')
    md.append('### Chain, inspector-only reading (`exact_er`)\n')
    md.append('| N | π(E) | π(R) | π(R*) | mean inspector payoff | largest exit from R | hazard from R (A neutral shadow / total) |\n|---|---|---|---|---|---|---|')
    for N in (1000, 10000):
        r = chain('exact_er', 0.0, 'base', N)
        if r:
            md.append('| %d | %.4f | %.4f | %.4f | %.4f | %s | %.2e / %.2e |' % (N, r['pi_sets']['E'], r['pi_sets']['R'], r['pi_sets']['Rstar'], r['stat']['u0g'], CAT_SHORT.get(r['exits']['R']['largest'], '-'),
                                                                   r['exits']['R']['cats']['A_neutral_shadow']['hazard'] or 0, r['exits']['R']['hazard']))
            R['controls']['chain_er_N%d' % N] = dict(pi_E=r['pi_sets']['E'], pi_R=r['pi_sets']['R'], u0g=r['stat']['u0g'])
    md.append('')
    md.append('### Migration, mN in {0, 1, 10} at (100, 64)\n')
    md.append('| c | mN | efficient islands | gen 2,000 inspector payoff | committed+compliant | efficient+responsive |\n|---|---|---|---|---|---|')
    for c in (0.0, 0.01):
        for mn, nm_ in ((0, 'mN0'), (1, 'base'), (10, 'mN10')):
            L = lot('exact-c%g-n100i64-%s' % (c, nm_))
            if L is None:
                continue
            md.append('| %g | %d | %s | %s | %s | %s |' % (c, mn, fmt(boot(vals(L, 'isl_efficient', 2000))), fmt(boot(vals(L, 'u0g', 2000))), fmt(boot(vals(L, 'isl_commit_comply', 2000))), fmt(boot(vals(L, 'isl_eff_resp', 2000)))))
            R['controls']['migration_c%g_mN%d' % (c, mn)] = dict(eff=boot(vals(L, 'isl_efficient', 2000)))
    md.append('')
    md.append('### Direct starts (monomorphic islands, no mutation, no migration; one K arrival into every island at generation 100 where K = 1)\n')
    md.append('Base `CRI` = `cr(THEM(ME))`, twin `N` (or the reverse); the injected twin is n copies; fractions are islands (64 per run, 20 runs). `twin fixed` = the injected twin has fixed; `K majority` = K above one half; `recovered` = responsive inspectors hold at least half the seat and K is below 1%. First row of each pair: generation 100 (before the arrival); second: the horizon 20N.\n')
    md.append('| N | base | injected | K arrival | at generation | twin fixed | K majority | efficient | efficient+shadow | recovered |\n|---|---|---|---|---|---|---|---|---|---|')
    R['controls']['direct'] = []
    for N in (100, 400):
        for base in ('CRI', 'N'):
            for ninj in (1, N // 10, N // 2):
                for karr in (0, 1):
                    d = direct('exact', 0.0, N, base, ninj, karr)
                    if d is None:
                        continue
                    for g in (d['cps'][0], d['cps'][-1]):
                        mean = lambda k: float(np.mean([r['at'][str(g)][k] for r in d['runs']]))
                        md.append('| %d | %s | %d | %d | %d | %.3f | %.3f | %.3f | %.3f | %.3f |' % (N, base, ninj, karr, g, mean('twin_fixed'), mean('K_majority'), mean('eff'), mean('shadow_eff'), mean('recovered')))
                        R['controls']['direct'].append(dict(N=N, base=base, ninj=ninj, karr=karr, gen=g, **{k: mean(k) for k in ('twin_fixed', 'K_majority', 'eff', 'shadow_eff', 'recovered')}))
    md.append('')


STRICT_INSPECTEE = ('C_strict_K', 'D_strict_other_nonreader', 'E_strict_reader_clean', 'E_strict_reader_forfeit')


def tag(x, thr, kind):
    """held / partial / failed for an effect size x against the threshold thr."""
    if x is None or not np.isfinite(x):
        return 'not scored (missing)'
    if x >= thr:
        return 'held'
    if x > 0:
        return 'partial'
    return 'failed'


def verdict_section(ctx):
    md, R = ctx['md'], ctx['R']
    V = {}
    md.append('## Verdicts (conventions of predictions/2026-10-24-inspection-shadow.md)\n')
    rows = {N: chain('exact', 0.0, 'base', N) for N in (1000, 10000, 100000)}
    avail = [N for N in rows if rows[N] is not None]
    # ---------------------------------------------------------------- P1
    if len(avail) >= 2:
        per = {}
        fires = 0
        for N in avail:
            r = rows[N]
            lr = r['exits']['R']['largest']; le = r['exits']['E']['largest']
            sf = r['exits']['E']['strict_inspectee_from']
            clauseR = lr == 'A_neutral_shadow'
            clauseE = le in STRICT_INSPECTEE and sf['nondeterring_inspector'] >= sf['deterring_inspector']
            per[N] = dict(largest_R=lr, largest_E=le, clauseR=clauseR, clauseE=clauseE, strict_E_from=sf, hazard_A_R=r['exits']['R']['cats']['A_neutral_shadow']['hazard'],
                          hazard_R=r['exits']['R']['hazard'], hazard_E=r['exits']['E']['hazard'])
            fires += int(not (clauseR and clauseE))
        sl = lsslope(avail, [per[N]['hazard_A_R'] for N in avail])
        slope_ok = sl is not None and -1.2 <= sl <= -0.8
        verdict = 'failed' if (not slope_ok or fires >= 2) else ('partial' if fires == 1 else 'held')
        V['P1'] = dict(verdict=verdict, slope_A_R=sl, slope_ok=slope_ok, falsifier_fired_at=fires, per_N=per, N_used=avail)
        md.append('- **Prediction 1 (mechanism): %s.** Neutral-drift hazard from R has slope %s over N = %s (range −1.2…−0.8: %s). Largest exit from R: %s; largest exit from E: %s (strict inspectee flux from non-deterring / deterring inspectors: %s). Falsifier fired at %d of %d values of N.' % (
            verdict.upper(), 'n/a' if sl is None else '%.3f' % sl, avail, 'yes' if slope_ok else 'no',
            '; '.join('N=%d %s' % (N, CAT_SHORT[per[N]['largest_R']].split(' ')[0]) for N in avail), '; '.join('N=%d %s' % (N, CAT_SHORT[per[N]['largest_E']].split(' ')[0]) for N in avail),
            '; '.join('N=%d %.2e/%.2e' % (N, per[N]['strict_E_from']['nondeterring_inspector'], per[N]['strict_E_from']['deterring_inspector']) for N in avail), fires, len(avail)))
    # ---------------------------------------------------------------- P2 (and counters)
    Nall = [N for N in (1000, 10000, 100000) if rows.get(N)]
    if len(Nall) >= 2:
        odds = [rows[N]['odds_E'] for N in Nall]
        sl = lsslope(Nall, odds)
        rises = all(odds[i + 1] > odds[i] for i in range(len(odds) - 1))
        V['P2'] = dict(verdict='held' if sl < 0.5 else 'failed', odds_slope=sl, N=Nall, pi_E=[rows[N]['pi_sets']['E'] for N in Nall], odds=odds,
                       counter_gpt_held=bool(rises), counter_gemini_held=bool(rises))
        md.append('- **Prediction 2 (scaling): %s.** Odds of E over N = %s: %s; least-squares slope %.3f (held iff < 0.5). P(E) = %s; it rises at every consecutive pair: %s (gpt-6.1-sol and gemini-4-argon counter-predictions: %s).' % (
            V['P2']['verdict'].upper(), Nall, ', '.join('%.4g' % o for o in odds), sl, ', '.join('%.4f' % rows[N]['pi_sets']['E'] for N in Nall), rises, 'held' if rises else 'failed'))
    # ---------------------------------------------------------------- P3
    L8 = lot('exact-c0-n800i8-base'); L1 = lot('exact-c0-n100i64-base')
    if L8 is not None:
        v8 = boot(vals(L8, 'isl_efficient', 16000)); v1 = boot(vals(L1, 'isl_efficient', 2000)) if L1 else (np.nan,) * 3
        verdict = 'held' if (v8[0] < 0.5 and (not np.isfinite(v1[0]) or v8[0] < v1[0])) else ('failed' if v8[0] >= 0.65 else 'partial')
        V['P3'] = dict(verdict=verdict, eff_800_8=v8, eff_100_64=v1, counter_gemini_held=bool(v8[0] >= 0.5))
        md.append('- **Prediction 3 (lottery path): %s.** Efficient islands at (800, 8), c = 0, generation 16,000: %s (generation 2,000: %s); at (100, 64): %s. Gemini-4-argon counter-prediction (stay at or above 0.5): %s.' % (
            verdict.upper(), fmt(v8), fmt(boot(vals(L8, 'isl_efficient', 2000))), fmt(v1), 'held' if v8[0] >= 0.5 else 'failed'))
    # ---------------------------------------------------------------- P4
    LK = lot('exact-c0-n400i16-rainK'); LC = lot('exact-c0-n400i16-rainC')
    if LK is not None and LC is not None:
        d = pdiff(vals(LK, 'isl_efficient', 8000), vals(LC, 'isl_efficient', 8000))
        V['P4'] = dict(verdict=tag(d[0], 0.1, 'effect'), effect=d)
        md.append('- **Prediction 4 (cheater fringe): %s.** K rain minus matched C rain, efficient islands at (400, 16), c = 0, generation 8,000: %s.' % (V['P4']['verdict'].upper(), fmt(d)))
    # ---------------------------------------------------------------- P5, P6
    e0 = R.get('remedies', {}).get('chain', {}).get('c0')
    e1 = R.get('remedies', {}).get('chain', {}).get('c0.01')
    if e0 and e0['effect_E'] is not None:
        V['P5'] = dict(verdict=tag(e0['effect_E'], 0.1, 'effect'), effect=e0['effect_E'], effect_R=e0['effect_R'])
        md.append('- **Prediction 5 (prudent inspectees): %s.** Chain, N = 10^4, c = 0: π(E) boosted minus matched control = %.4f (π(R): %.4f).' % (V['P5']['verdict'].upper(), e0['effect_E'], e0['effect_R']))
        if e1 and e1['effect_E'] is not None:
            if e0['effect_E'] <= 0:
                v6 = 'not scored (no help at c = 0)'
            else:
                v6 = 'held' if e1['effect_E'] < e0['effect_E'] else 'failed'
            V['P6'] = dict(verdict=v6, effect_c0=e0['effect_E'], effect_c001=e1['effect_E'])
            md.append('- **Prediction 6 (price): %s.** Effect at c = 0: %.4f; at c = 0.01: %.4f.' % (v6.upper(), e0['effect_E'], e1['effect_E']))
    # ---------------------------------------------------------------- engineer's expectations
    if len(avail) >= 2:
        la = {N: rows[N]['exits']['R']['largest'] for N in avail}
        e1_ok = la.get(1000) == 'A_neutral_shadow' and all(la[N] != 'A_neutral_shadow' for N in avail if N >= 10000)
        V['E1'] = dict(verdict='held' if e1_ok else 'failed', largest_R=la)
        md.append('- **E1 (crossover between 10^3 and 10^4): %s.** Largest exit from R by N: %s.' % (V['E1']['verdict'].upper(), la))
    if len(Nall) >= 2:
        V['E2'] = dict(verdict='held' if V['P2']['odds_slope'] < 0 else 'failed', slope=V['P2']['odds_slope'])
        md.append('- **E2 (odds slope negative): %s.** Slope %.3f.' % (V['E2']['verdict'].upper(), V['P2']['odds_slope']))
        occ = {N: rows[N]['occupancy'] for N in Nall if N >= 10000}
        if occ:
            e3 = all(o['light_cheater'] > o['shadow_excursion'] for o in occ.values())
            V['E3'] = dict(verdict='held' if e3 else 'failed', occupancy={N: dict(light=o['light_cheater'], shadow=o['shadow_excursion']) for N, o in occ.items()})
            md.append('- **E3 (tolerated light cheaters hold more π than the shadow excursion at N ≥ 10^4): %s.** Light-cheater / shadow-excursion occupancy: %s.' % (
                V['E3']['verdict'].upper(), '; '.join('N=%d %.4f / %.4f' % (N, o['light_cheater'], o['shadow_excursion']) for N, o in occ.items())))
    r001 = {N: chain('exact', 0.01, 'base', N) for N in (1000, 10000, 100000)}
    a001 = [N for N in r001 if r001[N]]
    if len(a001) >= 2:
        h = [r001[N]['exits']['R']['cats']['A_neutral_shadow']['hazard'] + r001[N]['exits']['R']['cats']['F_strict_inspector']['hazard'] for N in a001]
        sl = lsslope(a001, h)
        V['E4'] = dict(verdict='held' if sl is not None and sl > -0.3 else 'failed', slope=sl, N=a001)
        md.append('- **E4 (c = 0.01: leaving R by the shadow is selection, slope above −0.3): %s.** Slope of the (A + F) hazard over N = %s: %.3f.' % (V['E4']['verdict'].upper(), a001, sl))
    if e0 and e0['effect_E'] is not None:
        V['E5'] = dict(verdict='held' if 0 <= e0['effect_E'] < 0.1 else 'failed', effect=e0['effect_E'])
        md.append('- **E5 (prudent boost effect in [0, 0.1)): %s.** Effect %.4f.' % (V['E5']['verdict'].upper(), e0['effect_E']))
    md.append('')
    R['verdicts'] = V


if __name__ == '__main__':
    main()
