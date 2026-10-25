"""Report for the zero-tolerance experiment: reads runs/zero_tolerance/*, scores the predictions of predictions/2026-10-24-zero-tolerance.md
under the conventions fixed there, writes runs/zero-tolerance.md and .json.

    python3 src/zero_tolerance_report.py

Chain numbers are eps -> 0 whole-space objects; lottery numbers are eps = 0 finite-(N, I, horizon) statistics.  Run-clustered 95% intervals:
4,000 bootstrap resamples of runs (paired contrasts resample runs jointly).
"""
import os, sys, math, json
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inspection_shadow as S
from inspection_shadow_report import boot, pdiff, fmt, lsslope

ROOT = S.ROOT
RUNS = os.environ.get('ZERO_TOLERANCE_OUT', os.path.join(ROOT, 'runs', 'zero_tolerance'))
OUTMD = os.environ.get('ZERO_TOLERANCE_MD', os.path.join(ROOT, 'runs', 'zero-tolerance.md'))
OUTJS = OUTMD[:-3] + '.json'
ARMS = ('ctl', 'zt', 'sus', 'ztsus', 'sr1', 'sr4', 'sr16', 'unc')
LABEL = dict(ctl='control', zt='ZT', sus='SUS', ztsus='ZT+SUS', sr1='SR1', sr4='SR4', sr16='SR16', unc='uncond. I')
NS = (1000, 10000, 100000)
STORED_E = {1000: 0.3432, 10000: 0.1570, 100000: 0.0466}          # context only (the stored control, runs/inspection-shadow.md)


def exists(f):
    return os.path.exists(os.path.join(RUNS, f))


def chain(arm, c, N):
    f = 'chain_%s_c%g_N%d.json' % (arm.replace('@', '_'), c, N)
    return S.jload(os.path.join(RUNS, f)) if exists(f) else None


def lot(arm, c, size):
    f = 'lot_%s_c%g_%s.json.gz' % (arm.replace('@', '_'), c, size)
    return S.jload(os.path.join(RUNS, f)) if exists(f) else None


def pE(arm, c, N):
    r = chain(arm, c, N)
    return None if r is None else r['pi_sets']['E']


def cat_hazard(r, X, key):
    """hazard from set X in category `key` ('D' strict non-reading inspectee, 'E' strict reading inspectee (clean + forfeit), 'A' shadow, ...)."""
    if r is None:
        return None
    cats = r['exits'][X]['cats']
    if key == 'D':
        return cats['D_strict_other_nonreader']['hazard']
    if key == 'E':
        return cats['E_strict_reader_clean']['hazard'] + cats['E_strict_reader_forfeit']['hazard']
    if key == 'A':
        return cats['A_neutral_shadow']['hazard']
    if key == 'C':
        return cats['C_strict_K']['hazard']
    if key == 'F':
        return cats['F_strict_inspector']['hazard']
    if key == 'total':
        return r['exits'][X]['hazard']
    if key == 'other':
        tot = r['exits'][X]['hazard']
        return tot - cat_hazard(r, X, 'D') - cat_hazard(r, X, 'E') - cat_hazard(r, X, 'A')
    raise KeyError(key)


def largest(r, X):
    return None if r is None else r['exits'][X]['largest']


def ratio(a, b):
    """a / b with inf for b == 0."""
    if a is None or b is None:
        return None
    if b <= 1e-300:
        return float('inf') if a > 0 else float('nan')
    return a / b


def f3(x, d=3):
    if x is None:
        return 'n/a'
    if isinstance(x, float) and math.isinf(x):
        return 'inf'
    if isinstance(x, float) and math.isnan(x):
        return 'nan'
    return '%.*f' % (d, x)


def fe(x, d=2):
    if x is None:
        return 'n/a'
    if isinstance(x, float) and math.isinf(x):
        return 'inf'
    return '%.*e' % (d, x)


def lvals(L, key, g):
    out = []
    for r in L['runs']:
        v = r['stats'].get(str(g), {}).get(key)
        out.append(np.nan if v is None else v)
    return np.array(out, float)


def verdict(ok, partial=False):
    return 'held' if ok else ('partial' if partial else 'failed')


def main():
    md = ["# Zero-tolerance, suspicious and sampling inspectors (run report, 2026-10-24)\n",
          'Spec `specs/2026-10-24-zero-tolerance.md`; predictions `predictions/2026-10-24-zero-tolerance.md`; notes `notes/zero-tolerance.md`; code '
          '`src/zero_tolerance*.py`; rows `runs/zero_tolerance/`. **Chain** = the ε → 0 object (π over pairs of monomorphic role classes, the whole '
          'state space of about 158 × 157 or 168 × 167–173 pairs, no exploration cap, float32 storage as in the previous run); **lottery** = the ε = 0 '
          'seed lottery at the stated (N, I), mN = 1, horizon 20N; never π. Payoffs are game payoffs (gross of the price). "Gain" = an arm\'s π(E) '
          'minus the control\'s at the same (N, c); the control is the newly computed one (the same total mass m = 0.0013517 added to '
          '`cr(THEM(ME))` itself), the stored 0.0466 at N = 10⁵ is context only. Lottery intervals are run-clustered 95% bootstrap (4,000 resamples).\n']
    R = {}
    # ------------------------------------------------------------------ completeness
    jobs = []
    for f in ('jobs.txt', 'jobs_redo.txt', 'jobs_extra.txt'):
        if exists(f):
            jobs += [l.split('|') for l in open(os.path.join(RUNS, f)) if l.strip() and not l.startswith('#')]
    missing = [j[2].strip() for j in jobs if not exists(j[2].strip())]
    R['completeness'] = dict(n_jobs=len(jobs), n_missing=len(missing), missing=missing)
    md.append('## Completeness\n')
    md.append('%d of %d jobs of the job file have an output.%s\n' % (len(jobs) - len(missing), len(jobs), '' if not missing else ' Missing: ' + ', '.join(missing) + '.'))

    # ------------------------------------------------------------------ statics and validation
    st = S.jload(os.path.join(RUNS, 'static.json')) if exists('static.json') else None
    va = S.jload(os.path.join(RUNS, 'validate.json')) if exists('validate.json') else None
    if va:
        md.append('## Validation (before any counted cell)\n')
        md.append('Arm `v0` (nothing added, no mass moved) against the stored runs: class table max |Δ| %.1e; chain π(E) at N = 10³: %.6f vs stored %.6f '
                  '(relative difference %.1e); N = 10⁴: %.6f vs %.6f (%.1e); lottery runs 0–2 at (100, 64), generation 2,000, max |Δ| of five statistics %.1e. '
                  'Passed: **%s**.\n' % (va['table_max_abs_diff'], va['chain_N1000']['pi_E_new'], va['chain_N1000']['pi_E_stored'], va['chain_N1000']['rel_diff'],
                                         va['chain_N10000']['pi_E_new'], va['chain_N10000']['pi_E_stored'], va['chain_N10000']['rel_diff'],
                                         va['lottery_max_abs_diff_runs0-2'], va['passed']))
        R['validation'] = va
    if st:
        md.append('## Statics: classes, added mass, strict invaders of the arm\'s resident\n')
        md.append('| arm, c | K₀ × K₁ | added program: class (members), mass | strict invaders of (inspector, `C`): non-reading mass / reading mass | |E| / |R| |')
        md.append('|---|---|---|---|---|')
        for c in ('0', '0.01'):
            for tag in ('ctl', 'unc', 'zt', 'sus', 'ztsus', 'sr1', 'sr4', 'sr16'):
                d = st.get('%s_c%s' % (tag, c))
                if d is None:
                    continue
                ad = d['info']['added']
                a_s = '; '.join('`%s` → class `%s` (%d), %.6f' % (x['src'], x['cls_rep'], x['n_members'], x['cls_mass']) for x in ad) if ad else ('mass to `%s`' % d['info'].get('boost_class', '-'))
                lab = ad[0]['name'] if ad else 'CRI'
                inv = d['strict_invaders_of_(a,C)'][lab]
                md.append('| %s, c = %s | %d × %d | %s | %.6f / %.6f | %d / %d |' % (LABEL[tag], c, d['K'][0], d['K'][1], a_s, inv['nonreading_mass'], inv['reading_mass'], d['sets']['E'], d['sets']['R']))
        md.append('')
        R['static'] = st

    # ------------------------------------------------------------------ chain: pi(E)
    md.append('## Chain: π(E), gains, odds slopes (ε → 0, whole state space)\n')
    for c in (0.0, 0.01):
        md.append('**c = %g.** π(E) (gain over the control in parentheses); odds slope = least-squares slope of log odds on log N over N ≥ 10³.\n' % c)
        md.append('| arm | N = 10³ | N = 10⁴ | N = 10⁵ | odds slope | π(R), N = 10⁵ | inspector payoff, N = 10⁵ | forfeit mass (insp / ee), N = 10⁵ | π on 0.99 of states, N = 10⁵ |')
        md.append('|---|---|---|---|---|---|---|---|---|')
        base = {N: pE('ctl', c, N) for N in NS}
        for a in ARMS:
            cells = []
            odds = []
            for N in NS:
                v = pE(a, c, N)
                if v is None:
                    cells.append('n/a'); odds.append(None)
                else:
                    g = '' if a == 'ctl' or base[N] is None else ' (%+.3f)' % (v - base[N])
                    cells.append('%.4f%s' % (v, g)); odds.append(v / (1 - v))
            r5 = chain(a, c, 100000)
            sl = lsslope(list(NS), odds) if all(o is not None for o in odds) else None
            md.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                LABEL[a], cells[0], cells[1], cells[2], f3(sl, 2), f3(r5['pi_sets']['R'], 4) if r5 else 'n/a', f3(r5['stat']['u0g'], 3) if r5 else 'n/a',
                ('%.1e / %.1e' % (r5['stat']['forfeit0'], r5['stat']['forfeit1'])) if r5 else 'n/a', str(r5['n_states_for_099']) if r5 else 'n/a'))
        md.append('')
        R['piE_c%g' % c] = {a: {str(N): pE(a, c, N) for N in NS} for a in ARMS}
    md.append('Context only: the stored (unmatched) control gave π(E) = %s at N = 10³ / 10⁴ / 10⁵ (c = 0).\n' % ' / '.join('%.4f' % STORED_E[N] for N in NS))

    # ------------------------------------------------------------------ exits from R
    md.append('## Exit decomposition from R, c = 0 (conditional hazard per mutation event, own stationary weights)\n')
    md.append('Categories: **light cheaters** = D (strict invasion by a non-reading inspectee other than K), **bounded-read exploiters** = E (strict '
              'invasion by a reading inspectee, clean plus forfeit-driven), **shadow** = A (neutral drift of a non-deterring inspector), others = the rest. '
              'R includes the arm\'s added inspector. Ratios are control / arm.\n')
    for c in (0.0, 0.01):
        for N in (10000, 100000):
            rc = chain('ctl', c, N)
            if rc is None:
                continue
            md.append('**c = %g, N = %d.** Largest exit from R; hazards (and the ratio control / arm).\n' % (c, N))
            md.append('| arm | total | D light | E bounded-read | A shadow | other | largest | fixed-weight D / E (control weights) |')
            md.append('|---|---|---|---|---|---|---|---|')
            for a in ARMS:
                r = chain(a, c, N)
                if r is None:
                    continue
                row = [fe(cat_hazard(r, 'R', k)) + ('' if a == 'ctl' else ' (%s×)' % f3(ratio(cat_hazard(rc, 'R', k), cat_hazard(r, 'R', k)), 1)) for k in ('total', 'D', 'E', 'A', 'other')]
                fw = r.get('fixed_weight')
                fws = ('%s / %s' % (fe(fw['R']['D_strict_other_nonreader']), fe(fw['R']['E_strict_reader_clean'] + fw['R']['E_strict_reader_forfeit']))) if fw else '-'
                md.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % ((LABEL[a],) + tuple(row) + (largest(r, 'R').replace('_', ' ') if largest(r, 'R') else 'n/a', fws)))
            md.append('')
    md.append('**Resident-specific one-state rates per mutation event** out of (arm\'s inspector, `C`), c = 0, N = 10⁴ / 10⁵: strict non-reading inspectee (light cheaters), '
              'strict reading inspectee (bounded-read), neutral shadow, strict inspector; and the payoffs and charged levels at the resident.\n')
    md.append('| arm | resident | N | D light | E bounded-read | A shadow | F strict inspector | total |')
    md.append('|---|---|---|---|---|---|---|---|')
    for a in ARMS:
        for N in (10000, 100000):
            r = chain(a, 0.0, N)
            if r is None:
                continue
            lab = [k for k in r['resident_exits'] if k.startswith('(') and k not in ('(N,C)', '(N,K)', '(I,C)')]
            for k in lab:
                x = r['resident_exits'][k]['cats']
                md.append('| %s | %s | %d | %s | %s | %s | %s | %s |' % (LABEL[a], k, N, fe(x['D_strict_nonreader']), fe(x['E_strict_reader']), fe(x['A_neutral_shadow']), fe(x['F_strict_inspector']), fe(r['resident_exits'][k]['total'])))
    md.append('')

    # ------------------------------------------------------------------ occupancy
    md.append('## Where π sits (c = 0; exclusive detour categories of the previous run)\n')
    md.append('| arm | N | E | shadow excursion | cheater majority | light cheater | committed and compliant | mixing | forfeit | share of the added inspector (in R) |')
    md.append('|---|---|---|---|---|---|---|---|---|---|')
    for a in ARMS:
        for N in (10000, 100000):
            r = chain(a, 0.0, N)
            if r is None:
                continue
            o = r['occupancy']
            sa = '%.4f (%.4f)' % (r['added_share'][0], r['added_share_in_R'][0]) if r['added_share'] else '-'
            md.append('| %s | %d | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f | %s |' % (LABEL[a], N, o['E'], o['shadow_excursion'], o['cheater_major_other'], o['light_cheater'], o['committed_compliant'], o['mixing'], o['forfeit'], sa))
    md.append('')

    # ------------------------------------------------------------------ costs and timeouts
    md.append('## Realized read costs and timeouts (π-weighted, per round)\n')
    md.append('| arm | c | N | mean levels charged to the inspector | median levels (inspector + inspectee) | forfeit (timeout) mass, inspector / inspectee |')
    md.append('|---|---|---|---|---|---|')
    for c in (0.0, 0.01):
        for a in ARMS:
            for N in (10000, 100000):
                r = chain(a, c, N)
                if r is None or 'cost' not in r:
                    continue
                md.append('| %s | %g | %d | %s | %s | %.1e / %.1e |' % (LABEL[a], c, N, fe(r['cost']['mean_inspector']), f3(r['cost']['median_total'], 2), r['stat']['forfeit0'], r['stat']['forfeit1']))
    md.append('')

    # ------------------------------------------------------------------ lottery
    LOT = {}
    md.append('## Lottery (ε = 0; (N, I) = (100, 64), mN = 1, horizon 2,000; paired founders)\n')
    for size, T in (('n100i64', 2000), ('n400i64', 8000)):
        for c in (0.0, 0.01):
            cells = {a: lot(a, c, size) for a in ARMS}
            if cells['ctl'] is None:
                continue
            md.append('**%s, c = %g** (%d runs): efficient islands at the horizon, paired difference arm − control [95%% CI], unresolved islands (a role\'s top class below 0.9) at the horizon, share of the added program, efficient with a responsive inspector, inspector payoff, replaced founder slots per run.\n' % (size, c, len(cells['ctl']['runs'])))
            md.append('| arm | efficient | Δ vs control | unresolved | added share | efficient & responsive | efficient & shadow | light-cheater islands | inspector payoff | replaced slots |')
            md.append('|---|---|---|---|---|---|---|---|---|---|')
            ctl_v = lvals(cells['ctl'], 'isl_efficient', T)
            for a in ARMS:
                L = cells[a]
                if L is None:
                    continue
                v = lvals(L, 'isl_efficient', T)
                dif = pdiff(v, ctl_v) if a != 'ctl' else None
                LOT[(size, c, a)] = dict(eff=boot(v), diff=dif)
                nrep = np.mean([r.get('n_replaced', 0) for r in L['runs']])
                md.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %.1f |' % (
                    LABEL[a], fmt(boot(v)), fmt(dif) if dif else '-', fmt(boot(lvals(L, 'unres', T))), fmt(boot(lvals(L, 'sh_add', T)), 4),
                    fmt(boot(lvals(L, 'isl_eff_resp', T))), fmt(boot(lvals(L, 'isl_eff_shadow', T))), fmt(boot(lvals(L, 'isl_light', T))), fmt(boot(lvals(L, 'u0g', T))), nrep))
            md.append('')
    R['lottery'] = {'%s|%g|%s' % k: v for k, v in LOT.items()}
    Lv = lot('v0', 0.0, 'n400i64')
    stp = os.path.join(ROOT, 'runs', 'inspection_shadow', 'lot_exact-c0-n400i64-base.json.gz')
    if Lv is not None and os.path.exists(stp):
        Ls = S.jload(stp)
        d = np.nanmax(np.abs(lvals(Lv, 'isl_efficient', 8000) - lvals(Ls, 'isl_efficient', 8000)))
        md.append('**Validation at (400, 64), c = 0:** the validation arm `v0` against the stored cell of the previous run, efficient islands at generation 8,000 per run: max |Δ| = %.1e (stored mean %.3f, `v0` mean %.3f).\n' % (d, np.nanmean(lvals(Ls, 'isl_efficient', 8000)), np.nanmean(lvals(Lv, 'isl_efficient', 8000))))
        R['validation_400'] = dict(max_abs_diff=float(d))

    # ------------------------------------------------------------------ D-phase extras
    md.append('## D-phase control (extra, outside the spec; notes §1.3): the same arms at depth D = 11 and D = 13, c = 0\n')
    md.append('| D | arm | N = 10⁴ | N = 10⁵ | gain over the same-D control, N = 10⁵ |')
    md.append('|---|---|---|---|---|')
    ph = {}
    for D in (11, 13):
        for a in ('ctl', 'sus', 'ztsus', 'zt', 'sr16'):
            tag = '%s@D%d' % (a, D)
            vs = [pE(tag, 0.0, N) for N in (10000, 100000)]
            if any(v is None for v in vs):
                continue
            cb = pE('ctl@D%d' % D, 0.0, 100000)
            ph[(D, a)] = dict(pE=vs, gain=(vs[1] - cb) if cb is not None and a != 'ctl' else None)
            md.append('| %d | %s | %.4f | %.4f | %s |' % (D, LABEL[a], vs[0], vs[1], f3(ph[(D, a)]['gain'], 3) if a != 'ctl' else '-'))
    md.append('(D = 12 gains over the control at N = 10⁵: %s.)\n' % ', '.join('%s %+.3f' % (LABEL[a], pE(a, 0.0, 100000) - pE('ctl', 0.0, 100000)) for a in ('sus', 'ztsus', 'zt', 'sr16') if pE(a, 0.0, 100000) is not None and pE('ctl', 0.0, 100000) is not None))
    R['phase'] = {'%d|%s' % k: v for k, v in ph.items()}

    # ------------------------------------------------------------------ verdicts
    V = {}
    md.append('## Verdicts\n')
    md.append('Scoring rules are those of the predictions file. Chain numbers are ε → 0 quantities; lottery numbers are finite-horizon.\n')
    md.append('| # | claim | measured | verdict |')
    md.append('|---|---|---|---|')
    # P1
    rc4, rc5 = chain('ctl', 0.0, 10000), chain('ctl', 0.0, 100000)
    rz4, rz5 = chain('zt', 0.0, 10000), chain('zt', 0.0, 100000)
    if rz5 and rc5 and rz4 and rc4:
        r4 = ratio(cat_hazard(rc4, 'R', 'D'), cat_hazard(rz4, 'R', 'D')); r5 = ratio(cat_hazard(rc5, 'R', 'D'), cat_hazard(rz5, 'R', 'D'))
        pz = rz5['pi_sets']['E']
        a_ok = r4 >= 10 and r5 >= 10
        b_ok = pz >= 0.1
        v1 = 'held' if (a_ok and b_ok) else ('failed' if pz < 0.07 else 'partial')
        cp1 = (pz < 0.10) and largest(rz5, 'R') == 'E_strict_reader_clean'
        extra = ''
        if 'resident_exits' in rz5 and '(zt,C)' in rz5['resident_exits']:
            extra = '; resident (zt, C) D hazard %s' % fe(rz5['resident_exits']['(zt,C)']['cats']['D_strict_nonreader'])
        md.append('| 1 | ZT closes the light-cheater exit (≥ 10× at N = 10⁴ and 10⁵) and π(E)(10⁵) ≥ 0.1 [< 0.07] | D-hazard ratio control/ZT %s× (N = 10⁴), %s× (N = 10⁵); π(E)_ZT(10⁵) = %.4f (control %.4f, gain %+.4f); largest exit from R: %s%s | **%s** |' % (
            f3(r4, 1), f3(r5, 1), pz, rc5['pi_sets']['E'], pz - rc5['pi_sets']['E'], (largest(rz5, 'R') or 'n/a').replace('_', ' '), extra, v1))
        md.append('| 1c | counter (gemini-4-argon): the bounded-read exit absorbs the flow, π(E) < 0.10 | π(E)_ZT(10⁵) = %.4f; largest exit from R: %s | **%s** |' % (pz, (largest(rz5, 'R') or 'n/a').replace('_', ' '), 'held' if cp1 else 'failed'))
        V['1'] = dict(verdict=v1, ratio_D=[r4, r5], pE_ZT=pz, counter_held=bool(cp1))
    # P2
    rs5, rzs5, rs4, rzs4 = chain('sus', 0.0, 100000), chain('ztsus', 0.0, 100000), chain('sus', 0.0, 10000), chain('ztsus', 0.0, 10000)
    if rs5 and rzs5 and rc5:
        pzs, ps = rzs5['pi_sets']['E'], rs5['pi_sets']['E']
        v2 = 'held' if (pzs >= 0.5 and ps <= 0.136) else ('failed' if (pzs < 0.3 or ps > 0.2) else 'partial')
        ratE = {}
        for nm_, r4_, r5_ in (('SUS', rs4, rs5), ('ZT+SUS', rzs4, rzs5)):
            ratE[nm_] = [ratio(cat_hazard(rc4, 'R', 'E'), cat_hazard(r4_, 'R', 'E')) if r4_ and rc4 else None, ratio(cat_hazard(rc5, 'R', 'E'), cat_hazard(r5_, 'R', 'E'))]
        cp2 = all(x is not None and x >= 10 for x in ratE['SUS'] + ratE['ZT+SUS']) and pzs < 0.5
        md.append('| 2 | ZT+SUS ≥ 0.5 [< 0.3]; SUS within 0.1 of 0.036, i.e. ≤ 0.136 [> 0.2] (N = 10⁵) | π(E): ZT+SUS %.4f (gain %+.4f), SUS %.4f (gain %+.4f), control %.4f | **%s** |' % (pzs, pzs - rc5['pi_sets']['E'], ps, ps - rc5['pi_sets']['E'], rc5['pi_sets']['E'], v2))
        md.append('| 2c | counter (gpt-6.1-sol): targeted E-hazard falls ≥ 10× at both N in SUS and ZT+SUS but π(E)_ZT+SUS < 0.5 | E-hazard ratios control/arm: SUS %s, ZT+SUS %s; π(E)_ZT+SUS = %.4f | **%s** |' % (
            ' / '.join(f3(x, 1) for x in ratE['SUS']), ' / '.join(f3(x, 1) for x in ratE['ZT+SUS']), pzs, 'held' if cp2 else 'failed'))
        V['2'] = dict(verdict=v2, pE_ZTSUS=pzs, pE_SUS=ps, E_ratios=ratE, counter_held=bool(cp2))
    # P3
    r16, r1 = chain('sr16', 0.0, 100000), chain('sr1', 0.0, 100000)
    if r16 and r1 and rc5:
        g16 = r16['pi_sets']['E'] - rc5['pi_sets']['E']; g1 = r1['pi_sets']['E'] - rc5['pi_sets']['E']
        v3 = 'held' if (g16 >= 0.1 and g1 < 0.1) else ('failed' if g16 < 0.05 else 'partial')
        resD = r16['resident_exits'].get('(sr16,C)', {}).get('cats', {}).get('D_strict_nonreader') if 'resident_exits' in r16 else None
        cp3 = g16 < 0.1 and resD == 0.0
        md.append('| 3 | SR16 gains ≥ 0.1 over the control, SR1 does not [SR16 < 0.05] (N = 10⁵) | gain(SR16) = %+.4f (π(E) %.4f), gain(SR1) = %+.4f (π(E) %.4f); SR16 resident D hazard %s | **%s** |' % (g16, r16['pi_sets']['E'], g1, r1['pi_sets']['E'], fe(resD), v3))
        md.append('| 3c | counter (gpt-6.1-sol): gain depends on the q grid (scored: SR16 gain < 0.1 while its resident has no light-cheater exit) | gain %+.4f; resident D = %s | **%s** |' % (g16, fe(resD), 'held' if cp3 else 'failed'))
        V['3'] = dict(verdict=v3, gain_sr16=g16, gain_sr1=g1, counter_held=bool(cp3))
    # P4
    d4 = {}
    for N in (10000, 100000):
        a, b = pE('zt', 0.01, N), pE('sr16', 0.01, N)
        if a is not None and b is not None:
            d4[N] = a - b
    if d4:
        if len(d4) == 2:
            held = all(v >= 0.02 for v in d4.values()); fail = all(v <= 0 for v in d4.values())
        else:
            held = all(v >= 0.02 for v in d4.values()); fail = all(v <= 0 for v in d4.values())
        v4 = 'held' if held else ('failed' if fail else 'partial')
        md.append('| 4 | at c = 0.01 SR16 loses to ZT: π(E)_ZT − π(E)_SR16 ≥ 0.02 at N = 10⁴ and 10⁵ [≤ 0 at both] | %s | **%s** |' % ('; '.join('N = %d: %+.4f (ZT %.4f, SR16 %.4f)' % (N, d4[N], pE('zt', 0.01, N), pE('sr16', 0.01, N)) for N in d4), v4))
        V['4'] = dict(verdict=v4, diff=d4)
    # P5
    diffs = {}
    for c in (0.0, 0.01):
        L0 = lot('ctl', c, 'n100i64')
        if L0 is None:
            continue
        for a in ARMS[1:]:
            L = lot(a, c, 'n100i64')
            if L is None:
                continue
            d = pdiff(lvals(L, 'isl_efficient', 2000), lvals(L0, 'isl_efficient', 2000))
            diffs['%s|%g' % (a, c)] = d
    if diffs:
        mx = max(abs(d[0]) for d in diffs.values())
        v5 = 'held' if mx < 0.1 else ('failed' if mx > 0.15 else 'partial')
        worst = max(diffs, key=lambda k: abs(diffs[k][0]))
        n_exp = 2 * len(ARMS[1:])
        md.append('| 5 | every arm\'s efficient islands at (100, 64) move by < 0.1 against the control [> 0.15] (both prices) | max |Δ| = %.3f (%s, c = %s; CI %s); %d of %d arm-price cells run | **%s** |' % (
            mx, LABEL[worst.split('|')[0]], worst.split('|')[1], fmt(diffs[worst]), len(diffs), n_exp, v5))
        V['5'] = dict(verdict=v5, max_abs=mx, cells=len(diffs), diffs={k: list(v) for k, v in diffs.items()})
    # engineer's expectations
    # E1
    e1 = {}
    for nm_, a in (('SUS', 'sus'), ('ZT+SUS', 'ztsus')):
        rs = []
        for N in (10000, 100000):
            r_, rc_ = chain(a, 0.0, N), chain('ctl', 0.0, N)
            rs.append(ratio(cat_hazard(rc_, 'R', 'E'), cat_hazard(r_, 'R', 'E')) if r_ and rc_ else None)
        e1[nm_] = rs
    if all(x is not None for v in e1.values() for x in v):
        ok = all(x >= 10 for v in e1.values() for x in v)
        md.append('| E1 | SUS and ZT+SUS cut the bounded-read (E) hazard from R by ≥ 10× at N = 10⁴ and 10⁵ | control/arm: SUS %s, ZT+SUS %s | **%s** |' % (' / '.join(f3(x, 1) for x in e1['SUS']), ' / '.join(f3(x, 1) for x in e1['ZT+SUS']), 'held' if ok else 'failed'))
        V['E1'] = dict(verdict='held' if ok else 'failed', ratios=e1)
    # E2
    if (11, 'sus') in ph and (11, 'ctl') in ph and rs5 and rc5:
        g12 = rs5['pi_sets']['E'] - rc5['pi_sets']['E']; g11 = ph[(11, 'sus')]['gain']
        ok = (g12 - g11) >= 0.2
        fail = abs(g12 - g11) <= 0.1
        md.append('| E2 | the SUS gain at D = 11 is ≥ 0.2 below its D = 12 gain (N = 10⁵) [within 0.1] | gain D = 12: %+.4f; D = 11: %+.4f; D = 13: %s | **%s** |' % (
            g12, g11, f3(ph[(13, 'sus')]['gain'], 4) if (13, 'sus') in ph else 'n/a', 'held' if ok else ('failed' if fail else 'partial')))
        V['E2'] = dict(verdict='held' if ok else ('failed' if fail else 'partial'), gain12=g12, gain11=g11)
    # E2' (post hoc restatement: the arms that gain at D = 12)
    gl = []
    for a in ('ztsus', 'sr16'):
        c12 = pE(a, 0.0, 100000), pE('ctl', 0.0, 100000)
        row = [(c12[0] - c12[1]) if None not in c12 else None]
        for D in (11, 13):
            x, y = pE('%s@D%d' % (a, D), 0.0, 100000), pE('ctl@D%d' % D, 0.0, 100000)
            row.append((x - y) if x is not None and y is not None else None)
        gl.append((a, row))
    if gl:
        md.append("| E2′ (post hoc, not registered) | gain over the same-D control at N = 10⁵, D = 12 / 11 / 13 | %s | descriptive |" % '; '.join('%s: %s' % (LABEL[a], ' / '.join(f3(x, 3) for x in row)) for a, row in gl))
        V["E2'"] = {a: row for a, row in gl}
    # E3
    if rz5 and rc5:
        a_, b_ = rc5['occupancy']['light_cheater'], rz5['occupancy']['light_cheater']
        rr = ratio(a_, b_)
        md.append('| E3 | ZT occupancy of the light-cheater detour at N = 10⁵ ≥ 3× below the control\'s | control %.4f, ZT %.4f (%s×) | **%s** |' % (a_, b_, f3(rr, 1), 'held' if rr >= 3 else 'failed'))
        V['E3'] = dict(verdict='held' if rr >= 3 else 'failed', control=a_, zt=b_)
    # E4
    ru = chain('unc', 0.0, 100000)
    if ru and rc5:
        g = ru['pi_sets']['E'] - rc5['pi_sets']['E']
        md.append('| E4 | the unconditional-inspector comparator gains < 0.05 at N = 10⁵ | gain %+.4f (π(E) %.4f) | **%s** |' % (g, ru['pi_sets']['E'], 'held' if g < 0.05 else 'failed'))
        V['E4'] = dict(verdict='held' if g < 0.05 else 'failed', gain=g)
    # E5
    dd = []
    for N in NS:
        a, b = pE('sr1', 0.0, N), pE('ctl', 0.0, N)
        if a is not None and b is not None:
            dd.append((N, a - b))
    if dd:
        ok = all(abs(d) < 0.03 for _, d in dd)
        md.append('| E5 | the SR1 arm differs from the control by < 0.03 in π(E), N = 10³–10⁵ | %s | **%s** |' % ('; '.join('N = %d: %+.4f' % x for x in dd), 'held' if ok else 'failed'))
        V['E5'] = dict(verdict='held' if ok else 'failed', diffs=dd)
    # E6
    if r16:
        e = cat_hazard(r16, 'R', 'E'); er = r16['resident_exits'].get('(sr16,C)', {}).get('cats', {}).get('E_strict_reader') if 'resident_exits' in r16 else None
        ok = e is not None and e > 1e-12
        md.append('| E6 | SR16 is not immune: its category-E hazard from R is not zero at N = 10⁵ | aggregate E %s; resident (sr16, C) E %s | **%s** |' % (fe(e), fe(er), 'held' if ok else 'failed'))
        V['E6'] = dict(verdict='held' if ok else 'failed', E_hazard=e, resident_E=er)
    md.append('')
    R['verdicts'] = V
    # ------------------------------------------------------------------ support and transitions
    md.append('## Support, transitions and circulation (CLAUDE.md rule 4)\n')
    md.append('| arm | c | N | states carrying 0.99 of π | balance residual | circulation | mean sojourn in R | mean time outside R |')
    md.append('|---|---|---|---|---|---|---|---|')
    for c in (0.0, 0.01):
        for a in ARMS:
            for N in (10000, 100000):
                r = chain(a, c, N)
                if r is None:
                    continue
                md.append('| %s | %g | %d | %d | %.1e | %.3f | %s | %s |' % (LABEL[a], c, N, r['n_states_for_099'], r['balance']['max_rel_residual'], r['balance']['circulation'],
                                                                         fe(r['renewal_R']['mean_sojourn'], 3) if r['renewal_R']['mean_sojourn'] else 'n/a', fe(r['renewal_R']['mean_time_outside'], 3) if r['renewal_R']['mean_time_outside'] else 'n/a'))
    md.append('')
    # first passage: P(first entry in R) from (N, K)
    md.append('Return to R after the shadow-exploited state (first entry into E from (`N`, `K`) lands in R with probability; mean time to R, mutation events), c = 0:\n')
    md.append('| arm | N = 10⁴ | N = 10⁵ |')
    md.append('|---|---|---|')
    for a in ARMS:
        cells = []
        for N in (10000, 100000):
            r = chain(a, 0.0, N)
            fp = r.get('first_passage', {}).get('(N,K)') if r else None
            cells.append('%.4f; %s' % (fp['P_first_entry_in_R'], fe(fp.get('mean_time_to_R'), 2)) if fp else 'n/a')
        md.append('| %s | %s | %s |' % (LABEL[a], cells[0], cells[1]))
    md.append('')
    open(OUTMD, 'w').write('\n'.join(md) + '\n')
    S.jdump(R, OUTJS)
    print('wrote', OUTMD, OUTJS)


if __name__ == '__main__':
    main()
