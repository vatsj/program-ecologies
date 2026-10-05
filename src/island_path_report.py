"""Report for src/island_path.py: runs/island-path.md and runs/island-path.json."""
import gzip, json, math, os, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import island_path as P
from rival_islands_report import wilson, poisson_ci, km

RUNS = P.RUNS
MARKS = (100, 1000, 10000, 100000)
DIRS = ('2>1', '2>3', '2>0', '1>2', '3>2', '1>3', '3>1', '1>0', '0>1', '0>2', '0>3')


def fci(k, n):
    if n == 0: return '–'
    lo, hi = wilson(k, n)
    return '%.2f [%.2f, %.2f]' % (k / n, lo, hi)


def mci(v):
    v = np.asarray(v, float)
    if len(v) == 0: return '–'
    if len(v) == 1: return '%.3f' % v[0]
    se = v.std(ddof=1) / math.sqrt(len(v))
    return '%.3f ± %.3f' % (v.mean(), 1.96 * se)


def med(v):
    v = [x for x in v if x is not None and x >= 0]
    return ('%.0f' % np.median(v)) if v else '–'


def both(r):
    h = r['held_final']
    return h.get('1', 0) > 0 and h.get('2', 0) > 0


def category(r):
    h = r['held_final']; a, b = h.get('1', 0), h.get('2', 0)
    if a > 0 and b > 0: return 'both'
    if a > 0: return 'A only'
    if b > 0: return 'B only'
    return 'neither'


def resolved(r):
    h = r['held_final']
    return sum(1 for v in h.values() if v > 0) == 1


def hazard(rows):
    k = sum(1 for r in rows if r.get('loss_t') is not None)
    T = sum(r['expo'] for r in rows)
    lo, hi = poisson_ci(k)
    return k, T, (k / T if T > 0 else float('nan')), (lo / T if T > 0 else float('nan')), (hi / T if T > 0 else float('nan'))


def kmS(rows):
    t = [r['loss_t'] if r.get('loss_t') is not None else r['stop_gen'] for r in rows]
    e = [r.get('loss_t') is not None for r in rows]
    s = km(t, e, MARKS)
    return ' / '.join('%.2f' % s[m] for m in MARKS)


def inv_sum(rows):
    c = Counter()
    for r in rows:
        for k, v in r['inv'].items(): c[k] += v
    return c


def qstat(rows, ref, key='n_loc_end_bg', B=2000):
    """Run-paired ratio q = sum(rows[key]) / sum(ref[key]) with a run-pair bootstrap interval."""
    rr = {r['rep']: r for r in ref}
    pairs = [(r[key], rr[r['rep']][key]) for r in rows if r['rep'] in rr]
    if not pairs: return float('nan'), (float('nan'), float('nan')), 0
    a = np.array(pairs, float)
    q = a[:, 0].sum() / a[:, 1].sum()
    rng = np.random.default_rng(11)
    bs = []
    for _ in range(B):
        ix = rng.integers(0, len(a), len(a))
        d = a[ix, 1].sum()
        if d > 0: bs.append(a[ix, 0].sum() / d)
    return float(q), (float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))), len(a)


def by_cell(rows, keys=('N', 'I', 'mN', 'k', 'pair', 'preset')):
    c = defaultdict(list)
    for r in rows: c[tuple(r[k] for k in keys)].append(r)
    return c


def hours(rows):
    return sum(r['time_s'] for r in rows) / 3600


def main():
    md = []; out = {}
    calib = json.load(open(P.CALIB)); st = json.load(open(os.path.join(RUNS, 'island-path-static.json')))
    val = json.load(open(os.path.join(RUNS, 'island-path-validate.json')))
    out['calib'] = calib; out['static'] = st; out['validate'] = val
    B = {int(k): v for k, v in calib['mN_boundary'].items()}
    stat = {(c['N'], c['invader'], c['resident'], c['k']): c for c in st['cells']}
    rhoDD = {N: stat[(N, 'A', 'B3', 1)]['exact'] for N in (100, 200, 400)}
    Pk = lambda N, k: stat[(N, 'A', 'B3', k)]['exact']
    cal = P.load('cal')
    md.append('# A path in (N, I, mN): independent nucleation and rival resolution (`src/island_path.py`)\n')
    md.append('Spec `specs/2026-10-05-island-path.md`; predictions `predictions/2026-10-05-island-path.md`. Modal arm, n = 9, PD, '
              'w = 0.3, ε = 0, iid length-prior seeds, complete island graph, generation = I·N births, horizon 10⁵ generations. '
              'Finite-horizon lottery and hazard results, not π. Every run is in every denominator; intervals are Wilson 95% over runs '
              '(islands within a run are not independent), exact Poisson for hazards, run-pair bootstrap for q.\n')
    # ------------------------------------------------------------------ 0
    md.append('## 0. Calibration, statics, validation\n')
    md.append('| N | nucleating islands (m = 0, I = 16, 120 runs) | p | T_nuc median [95%] | 5 / 25 / 75 / 95% | boundary mN |')
    md.append('|---|---|---|---|---|---|')
    for N in (100, 200, 400):
        d = calib['dist'][str(N)]
        md.append('| %d | %d / %d | %.3f | %.0f [%.0f, %.0f] | %.0f / %.0f / %.0f / %.0f | %.3f |' % (
            N, calib['n_nuc'][str(N)][0], calib['n_nuc'][str(N)][1], calib['p'][str(N)], calib['T_nuc'][str(N)], d['median_ci'][0],
            d['median_ci'][1], d['5'], d['25'], d['75'], d['95'], B[N]))
    md.append('\nT_nuc ∝ N^%.2f. Checks every 5 generations (the resolution of T_nuc).\n' % calib['T_nuc_exponent'])
    md.append('**Statics** (exact formula; 10⁴ simulated runs per cell, %d of %d inside the 95%% interval). P(fix) of k invaders arriving at once '
              'on one island:\n' % (sum(c['inside'] for c in st['cells']), len(st['cells'])))
    md.append('| invader → resident | N | k = 1 | k = 10 | k = 30 | k = 60 |')
    md.append('|---|---|---|---|---|---|')
    for (q, r_) in (('A', 'B3'), ('B3', 'A'), ('A', 'B1'), ('bridge', 'A'), ('A', 'bridge'), ('bridge', 'B1'), ('B1', 'bridge'),
                    ('B3', 'bridge'), ('bridge', 'B3')):
        for N in (100, 200, 400):
            md.append('| %s → %s | %d | %s |' % (q, r_, N, ' | '.join('%.3g (%d)' % (stat[(N, q, r_, k)]['exact'], stat[(N, q, r_, k)]['sim'])
                                                                     for k in (1, 10, 30, 60))))
    md.append('\n(simulated fixations of 10⁴ in parentheses.) Classes: %s. B3 → A equals A → B3 and B1 ↔ A equals B3 ↔ A (same symmetric '
              'coordination game).\n' % ', '.join('%s = `%s`' % kv for kv in st['classes'].items()))
    md.append('**Validation.** k = 1 path draw-for-draw identical to the ca3cc7f kernel (48/48, `tests/check_rival_kernel_identity.py`). '
              'Against an unskipped reference with the same stopping rule (N = 50, I = 4, identical initial states, independent streams, '
              '1,000 runs per side per cell): z-scores of kernel − reference:\n')
    md.append('| preset | pair | k | mN | gens | both-present ref / kern | z(both) | z(B count) | z(coop count) | z(n_est) | z(n_local) | z(P(C,C)) |')
    md.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for c in val['propagule']:
        md.append('| %s | %s | %d | %g | %d | %.3f / %.3f | %.2f | %.2f | %.2f | %.2f | %.2f | %.2f |' % (
            c['preset'], c['pair'], c['k'], c['mN'], c['gens'], c['ref']['both'], c['kern']['both'], c['z']['both'], c['z']['gB'],
            c['z']['gcoop'], c['z']['n_est'], c['z']['n_loc'], c['z']['pcc']))
    zs = [abs(v) for c in val['propagule'] for v in c['z'].values() if v != 0]
    md.append('\nmax |z| = %.2f over %d nonzero statistics; %d exceed 2 (≈ %.1f expected under the null). Default kernel vs `seeds_in_n._run`: %s.\n' % (
        max(zs), len(zs), sum(z > 2 for z in zs), 0.0455 * len(zs),
        '; '.join('(%d, %d, mN %g) efficient %.3f vs %.3f (%d runs each)' % (c['N'], c['I'], c['mN'], c['kern']['eff'], c['sn']['eff'], c['sn']['n'])
                  for c in val['default'])))
    # ------------------------------------------------------------------ 1
    path = P.load('path'); pathq = P.load('pathq')
    out['path'] = []
    if path:
        md.append('## 1. The boundary path (pre-seeded A on island 0, B on island 1, rest iid; 40 runs per cell)\n')
        md.append('Both = A and B each hold ≥ 1 island at the horizon or stop (holder rule). Hazard = separation losses per '
                  'minority-island-generation (exposure ∫ min(held_A, held_B) dt). Reference = mN·ρ_DD(N) per recipient island-generation. '
                  'Invasions summed over runs (strong-holder changes; 2>1 = an island held by B taken by A; 2>3 by the bridge; 2>0 by an '
                  'untagged class).\n')
        md.append('| pair | N | I | mN | both [95%] | A only | B only | neither | all islands one tag | B islands at end (mean) | losses / exposure | hazard [95%] | ref. mN·ρ_DD | KM S(10²/10³/10⁴/10⁵) | median loss gen | island P(C,C) | cf cross P(C,C) | worker-h |')
        md.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        C = by_cell(path)
        for pair in (2, 0):
            for N in (100, 200, 400):
                for I in (16, 64):
                    rs = C.get((N, I, B[N], 1, pair, 'AB'), [])
                    if not rs: continue
                    cat = Counter(category(r) for r in rs)
                    k, T, h, lo, hi = hazard(rs)
                    rec = dict(pair=pair, N=N, I=I, mN=B[N], runs=len(rs), both=cat['both'], A_only=cat['A only'], B_only=cat['B only'],
                               neither=cat['neither'], resolved=sum(resolved(r) for r in rs), losses=k, exposure=T, hazard=h, hazard_ci=[lo, hi],
                               ref=B[N] * rhoDD[N], inv=dict(inv_sum(rs)), pcc=float(np.mean([r['pcc'] for r in rs])),
                               cf=float(np.mean([r['cf_cross_pcc'] for r in rs])), heldB=float(np.mean([r['held_final'].get('2', 0) for r in rs])),
                               hours=hours(rs), loss_times=[r.get('loss_t') for r in rs], loss_net=[r.get('loss_net') for r in rs],
                               t_ext=[r['t_ext'][1:3] for r in rs])
                    out['path'].append(rec)
                    md.append('| %s | %d | %d | %.3f | %s | %d | %d | %d | %d | %.1f | %d / %.3g | %.2g [%.2g, %.2g] | %.2g | %s | %s | %s | %s | %.2f |' % (
                        'P*' if pair == 2 else 'bridge', N, I, B[N], fci(cat['both'], len(rs)), cat['A only'], cat['B only'], cat['neither'],
                        rec['resolved'], rec['heldB'], k, T, h, lo, hi, rec['ref'], kmS(rs), med([r.get('loss_t') for r in rs]),
                        mci([r['pcc'] for r in rs]), mci([r['cf_cross_pcc'] for r in rs]), rec['hours']))
        md.append('\n**Invasions by direction** (summed over the 40 runs of each cell):\n')
        md.append('| pair | N | I | ' + ' | '.join(DIRS) + ' | B-island losses: replacement / absorption / capture |')
        md.append('|---|---|---|' + '---|' * len(DIRS) + '---|')
        for rec in out['path']:
            iv = rec['inv']; tot = iv.get('2>1', 0) + iv.get('2>3', 0) + iv.get('2>0', 0)
            md.append('| %s | %d | %d | %s | %s |' % ('P*' if rec['pair'] == 2 else 'bridge', rec['N'], rec['I'],
                                                    ' | '.join(str(iv.get(d, 0)) for d in DIRS),
                                                    ('%d / %d / %d' % (iv.get('2>1', 0), iv.get('2>3', 0), iv.get('2>0', 0))) if tot else '–'))
    if pathq:
        md.append('\n**q on the path** (iid ancestry-tagged runs vs the m = 0 reference with the same initial states):\n')
        md.append('| N | I | mN | x = mN·T_nuc/N | runs | q (holder form) [95%] | q_est (local establishment) [95%] | m = 0 local holders | island P(C,C) | cf cross P(C,C) | worker-h |')
        md.append('|---|---|---|---|---|---|---|---|---|---|---|')
        C = by_cell(pathq); Cr = by_cell(cal)
        out['pathq'] = []
        for N in (100, 200, 400):
            for I in (16, 64):
                rs = C.get((N, I, B[N], 1, None, 'iid'), [])
                ref = Cr.get((N, I, 0.0, 1, None, 'iid'), [])
                if not rs: continue
                q, qci, n = qstat(rs, ref); qe, qeci, _ = qstat(rs, ref, 'n_loc_est_bg')
                den = sum(r['n_loc_end_bg'] for r in ref if r['rep'] in {x['rep'] for x in rs})
                out['pathq'].append(dict(N=N, I=I, mN=B[N], runs=len(rs), q=q, q_ci=qci, q_est=qe, q_est_ci=qeci, den=den,
                                         pcc=float(np.mean([r['pcc'] for r in rs])), cf=float(np.mean([r['cf_cross_pcc'] for r in rs]))))
                md.append('| %d | %d | %.3f | %.2f | %d | %.2f [%.2f, %.2f] | %.2f [%.2f, %.2f] | %d | %s | %s | %.2f |' % (
                    N, I, B[N], B[N] * calib['T_nuc'][str(N)] / N, len(rs), q, qci[0], qci[1], qe, qeci[0], qeci[1], den,
                    mci([r['pcc'] for r in rs]), mci([r['cf_cross_pcc'] for r in rs]), hours(rs)))
    # ------------------------------------------------------------------ 3 natural
    nat = P.load('nat')
    if nat:
        md.append('\n## 3. Natural separation along the path (iid only)\n')
        md.append('Ever = two certified islands with mutually-defecting cooperative holders at some check; horizon = at the end. '
                  'Bridge share = islands at the end held by classes mutually cooperating with both members of the first separated pair '
                  '(ever-separated runs). Colonization time = first immigrant-founded establishment − first establishment; rival interval = '
                  'first establishment of a holder mutually defecting with an earlier holder − first establishment.\n')
        md.append('| N | I | mN | runs | ever separated [95%] | horizon separated [95%] | separations surviving | bridge share (ever-sep. runs) | runs with a rival establishment | rival before first immigrant island | median colonization time | median rival interval | island P(C,C) | cf cross P(C,C) | worker-h |')
        md.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        C = by_cell(nat); out['nat'] = []
        for N in (100, 200):
            for I in (64, 256):
                rs = C.get((N, I, B[N], 1, None, 'iid'), [])
                if not rs: continue
                ev = [r for r in rs if r['first_sep'] >= 0]; hz = [r for r in rs if r['n_sep_end'] > 0]
                riv = [r for r in rs if r['t_rival_est'] >= 0]
                before = [r for r in riv if r['t_first_imm'] < 0 or r['t_rival_est'] < r['t_first_imm']]
                col = [r['t_first_imm'] - r['t_first_est'] for r in rs if r['t_first_imm'] >= 0 and r['t_first_est'] >= 0]
                rint = [r['t_rival_est'] - r['t_first_est'] for r in riv]
                bsh = [r['bridge_share_end'] for r in ev if 'bridge_share_end' in r]
                rec = dict(N=N, I=I, mN=B[N], runs=len(rs), ever=len(ev), horizon=len(hz), rival=len(riv), rival_before_imm=len(before),
                           col_median=float(np.median(col)) if col else None, rival_int_median=float(np.median(rint)) if rint else None,
                           rival_int=rint, bridge_share=bsh, sep_pairs=[r.get('first_sep_pair') for r in ev],
                           hz_pairs=[r.get('sep_end_pair') for r in hz], pcc=float(np.mean([r['pcc'] for r in rs])),
                           cf=float(np.mean([r['cf_cross_pcc'] for r in rs])), hours=hours(rs))
                out['nat'].append(rec)
                md.append('| %d | %d | %.3f | %d | %s | %s | %d / %d | %s | %d | %d / %d | %s | %s | %s | %s | %.2f |' % (
                    N, I, B[N], len(rs), fci(len(ev), len(rs)), fci(len(hz), len(rs)), len(hz), len(ev),
                    ('%.2f' % np.mean(bsh)) if bsh else '–', len(riv), len(before), len(riv),
                    ('%.0f' % rec['col_median']) if col else '–', ('%.0f' % rec['rival_int_median']) if rint else '–',
                    mci([r['pcc'] for r in rs]), mci([r['cf_cross_pcc'] for r in rs]), rec['hours']))
        md.append('\nSeparated pairs (first separated pair in ever-separated runs; horizon pairs marked):\n')
        for rec in out['nat']:
            c = Counter(tuple(p) for p in rec['sep_pairs'] if p); ch = Counter(tuple(p) for p in rec['hz_pairs'] if p)
            if c:
                md.append('- (%d, %d): %s; at the horizon: %s' % (rec['N'], rec['I'], '; '.join('%s × %s (%d)' % (a, b, v) for (a, b), v in c.most_common()),
                                                              '; '.join('%s × %s (%d)' % (a, b, v) for (a, b), v in ch.most_common()) or 'none'))
    # ------------------------------------------------------------------ 2 propagules
    prop = P.load('prop'); propq = P.load('propq')
    if prop:
        md.append('\n## 2. Propagule migration (I = 16, boundary flux mN, mN/k propagule events per island-generation; 40 runs per cell)\n')
        md.append('k = 1 rows are the path cells at I = 16 (same initial states). Reference = (mN/k)·P_k(N), P_k the static A → B probability for '
                  'k at once.\n')
        md.append('| pair | N | k | k/N | both [95%] | A only | B only | B islands at end | losses / exposure | hazard [95%] | ref. (mN/k)·P_k | KM S(10²/10³/10⁴/10⁵) | 2>1 / 1>2 / 2>3 / 2>0 | island P(C,C) | cf cross P(C,C) | worker-h |')
        md.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        C = by_cell(path + prop); out['prop'] = []
        for pair in (2, 0):
            for N, ks in ((200, (1, 10, 30)), (400, (1, 10, 30, 60))):
                for k in ks:
                    rs = C.get((N, 16, B[N], k, pair, 'AB'), [])
                    if not rs: continue
                    cat = Counter(category(r) for r in rs)
                    kk, T, h, lo, hi = hazard(rs); iv = inv_sum(rs)
                    ref = B[N] / k * Pk(N, k)
                    rec = dict(pair=pair, N=N, k=k, runs=len(rs), both=cat['both'], A_only=cat['A only'], B_only=cat['B only'], losses=kk,
                               exposure=T, hazard=h, hazard_ci=[lo, hi], ref=ref, inv=dict(iv), heldB=float(np.mean([r['held_final'].get('2', 0) for r in rs])),
                               pcc=float(np.mean([r['pcc'] for r in rs])), cf=float(np.mean([r['cf_cross_pcc'] for r in rs])), hours=hours(rs))
                    out['prop'].append(rec)
                    md.append('| %s | %d | %d | %.3f | %s | %d | %d | %.1f | %d / %.3g | %.2g [%.2g, %.2g] | %.2g | %s | %d / %d / %d / %d | %s | %s | %.2f |' % (
                        'P*' if pair == 2 else 'bridge', N, k, k / N, fci(cat['both'], len(rs)), cat['A only'], cat['B only'], rec['heldB'], kk, T, h, lo, hi,
                        ref, kmS(rs), iv.get('2>1', 0), iv.get('1>2', 0), iv.get('2>3', 0), iv.get('2>0', 0), mci([r['pcc'] for r in rs]),
                        mci([r['cf_cross_pcc'] for r in rs]), rec['hours']))
    if propq:
        md.append('\n**q under propagules** (iid, I = 16, 120 runs per cell, paired m = 0 reference; Δq against k = 1 on the same initial states):\n')
        md.append('| N | k | q (holder form) [95%] | Δq vs k = 1 [95%] | q_est [95%] | island P(C,C) | cf cross P(C,C) |')
        md.append('|---|---|---|---|---|---|---|')
        C = by_cell(pathq + propq); Cr = by_cell(cal); out['propq'] = []
        for N, ks in ((200, (1, 10, 30)), (400, (1, 10, 30, 60))):
            ref = Cr.get((N, 16, 0.0, 1, None, 'iid'), [])
            base = C.get((N, 16, B[N], 1, None, 'iid'), [])
            for k in ks:
                rs = C.get((N, 16, B[N], k, None, 'iid'), [])
                if not rs: continue
                q, qci, n = qstat(rs, ref); qe, qeci, _ = qstat(rs, ref, 'n_loc_est_bg')
                # paired bootstrap of the difference
                rr = {r['rep']: r for r in ref}; bb = {r['rep']: r for r in base}
                reps = [r['rep'] for r in rs if r['rep'] in rr and r['rep'] in bb]
                a = np.array([({x['rep']: x for x in rs}[p]['n_loc_end_bg'], bb[p]['n_loc_end_bg'], rr[p]['n_loc_end_bg']) for p in reps], float)
                dq = a[:, 0].sum() / a[:, 2].sum() - a[:, 1].sum() / a[:, 2].sum()
                rng = np.random.default_rng(5); bs = []
                for _ in range(2000):
                    ix = rng.integers(0, len(a), len(a)); d = a[ix, 2].sum()
                    if d > 0: bs.append((a[ix, 0].sum() - a[ix, 1].sum()) / d)
                dci = (float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)))
                out['propq'].append(dict(N=N, k=k, q=q, q_ci=qci, dq=float(dq), dq_ci=dci, q_est=qe, q_est_ci=qeci,
                                         pcc=float(np.mean([r['pcc'] for r in rs])), cf=float(np.mean([r['cf_cross_pcc'] for r in rs]))))
                md.append('| %d | %d | %.2f [%.2f, %.2f] | %s | %.2f [%.2f, %.2f] | %s | %s |' % (
                    N, k, q, qci[0], qci[1], ('%+.2f [%+.2f, %+.2f]' % (dq, dci[0], dci[1])) if k > 1 else '–', qe, qeci[0], qeci[1],
                    mci([r['pcc'] for r in rs]), mci([r['cf_cross_pcc'] for r in rs])))
    # ------------------------------------------------------------------ 4 bridge
    br = P.load('bridge')
    if br:
        md.append('\n## 4. The bridge test (N = 100, I = 16, pair 1 tags; 40 runs per cell)\n')
        md.append('Shares are of the 16 islands at the horizon or stop (holder rule). Per-migrant invasion probability = strong-holder changes '
                  'x → y-held / migrant individuals of tag x arriving on islands strongly held by y (static neutral value 1/N = 0.01).\n')
        md.append('| preset | mN | bridge share [95%] | A-net share | B share | bridge majority (> 8 islands) [95%] | bridge holds every island | B present at end | bridge share at 10² / 10³ / 10⁴ / 10⁵ | P(inv) bridge→A-held | A→bridge-held | bridge→B-held | B→bridge-held | island P(C,C) | cf cross P(C,C) |')
        md.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        C = by_cell(br); out['bridge'] = []
        for mN in (0.1, 1.0):
            for preset in ('ABbridge', 'AAbridge', 'bridge'):
                rs = C.get((100, 16, mN, 1, 0, preset), [])
                if not rs: continue
                sh = [r['held_final'].get('3', 0) / 16 for r in rs]
                maj = sum(1 for r in rs if r['held_final'].get('3', 0) > 8)
                allb = sum(1 for r in rs if r['held_final'].get('3', 0) == 16)
                inv = inv_sum(rs); mig = np.sum([np.array(r['mig_ct']) for r in rs], axis=0)
                def pinv(x, y):
                    m = mig[x, y]
                    return ('%.4f (%d/%d)' % (inv.get('%d>%d' % (y, x), 0) / m, inv.get('%d>%d' % (y, x), 0), m)) if m > 0 else '–'
                tr = []
                for mk in MARKS:
                    v = []
                    for r in rs:
                        t = np.array(r['trace'])
                        j = np.searchsorted(t[:, 0], mk, side='right') - 1
                        v.append(t[max(j, 0), 3] / 16 if r['stop_gen'] >= mk else r['held_final'].get('3', 0) / 16)
                    tr.append(np.mean(v))
                rec = dict(preset=preset, mN=mN, runs=len(rs), share=float(np.mean(sh)), share_runs=sh, majority=maj, all=allb,
                           A=float(np.mean([r['held_final'].get('1', 0) / 16 for r in rs])), B=float(np.mean([r['held_final'].get('2', 0) / 16 for r in rs])),
                           Bpresent=sum(1 for r in rs if r['held_final'].get('2', 0) > 0), trace=tr, inv=dict(inv), mig=mig.tolist(),
                           pcc=float(np.mean([r['pcc'] for r in rs])), cf=float(np.mean([r['cf_cross_pcc'] for r in rs])), hours=hours(rs))
                out['bridge'].append(rec)
                md.append('| %s | %g | %s | %.2f | %.2f | %s | %d | %d | %s | %s | %s | %s | %s | %s | %s |' % (
                    {'ABbridge': 'A, B, bridge', 'AAbridge': 'A, A, bridge', 'bridge': 'bridge alone'}[preset], mN, mci(sh), rec['A'], rec['B'],
                    fci(maj, len(rs)), allb, rec['Bpresent'], ' / '.join('%.2f' % v for v in tr), pinv(3, 1), pinv(1, 3), pinv(3, 2), pinv(2, 3),
                    mci([r['pcc'] for r in rs]), mci([r['cf_cross_pcc'] for r in rs])))
    # ------------------------------------------------------------------ merge
    mp = os.path.join(RUNS, 'island-path-merge.json.gz')
    if os.path.exists(mp):
        mg = json.load(gzip.open(mp, 'rt')); out['merge'] = mg
        md.append('\n## Merge test (N = 200 runs of cells 1–2 ending with both present; conditional on survival)\n')
        md.append('| source | merges | clean two-type | larger won (clean) | minority won (clean) | median gens to freeze | median larger share |')
        md.append('|---|---|---|---|---|---|---|')
        C = defaultdict(list)
        for m in mg: C[m['exp']].append(m)
        for e, ms in sorted(C.items()):
            cl = [m for m in ms if m['clean']]
            md.append('| %s | %d | %d | %d | %d | %s | %s |' % (e, len(ms), len(cl), sum(m['larger_won'] for m in cl), sum(m['minority_won'] for m in cl),
                                                      med([m['gens_to_freeze'] for m in cl]), ('%.3f' % np.median([m['share_larger'] for m in cl])) if cl else '–'))
    # per-run compact records
    recs = []
    for e in ('path', 'pathq', 'nat', 'prop', 'propq', 'bridge'):
        for r in P.load(e):
            recs.append({k: r.get(k) for k in ('exp', 'N', 'I', 'mN', 'k', 'pair', 'preset', 'rep', 'status', 'stop_gen', 'pcc', 'cf_cross_pcc',
                                                'held_final', 't_ext', 'held_zero', 'loss_t', 'loss_net', 'expo', 't_first_est', 't_first_imm',
                                                't_rival_est', 'first_sep', 'n_sep_end', 'inv', 'n_loc_est_bg', 'n_loc_end_bg', 'time_s')})
    out['runs'] = recs
    vp = os.path.join(RUNS, 'island-path-verdicts.md')
    if os.path.exists(vp):
        md.append('\n' + open(vp).read())
    open(os.path.join(RUNS, 'island-path.md'), 'w').write('\n'.join(md) + '\n')
    json.dump(out, open(os.path.join(RUNS, 'island-path.json'), 'w'), default=float)
    print('\n'.join(md))


if __name__ == '__main__':
    main()
