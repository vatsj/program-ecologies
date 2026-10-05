"""Report for src/seeds_in_n.py: writes runs/seeds-in-n.md and runs/seeds-in-n.json."""
import json, os, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import seeds_in_n as S
from almost_all_seeds import wilson
from chain import fixation
from scipy.stats import spearmanr

NS = S.NS
_ENC = {'efficient': 'e', 'defecting': 'd', 'other': 'o', None: 'n'}
_DEC = {v: k for k, v in _ENC.items()}


def ci(k, n):
    lo, hi = wilson(k, n)
    return '%.3f [%.3f, %.3f]' % (k / n if n else float('nan'), lo, hi)


def ci2(k, n):
    lo, hi = wilson(k, n)
    return '%.2f [%.2f, %.2f]' % (k / n if n else float('nan'), lo, hi)


def rho_D(d, k, N):
    U = d['U']; iD = d['iD']
    return fixation(U[k, k], U[k, iD], U[iD, k], U[iD, iD], N, S.W, N)


def main():
    if os.path.exists(S.ROWS):
        rows = json.load(open(S.ROWS))
    else:            # the committed slim file
        rows = json.load(open(os.path.join(S.RUNS, 'seeds-in-n.json')))['rows']
        for r in rows:
            r['isl_out'] = [_DEC[c] for c in r['isl_out']]
    rows.sort(key=S.key)
    st = S.static_rows()
    summ = dict(static=st)
    L = ['# Almost all seeds: cutoff sensitivity in n (2026-10-05)', '',
         'Spec `specs/2026-10-05-seeds-in-n.md`; predictions `predictions/2026-10-05-seeds-in-n.md` (committed before the runs); '
         'code `src/seeds_in_n.py`, `src/seeds_in_n_report.py`. Modal arm (all box kinds), PD, w = 0.3, ε = 0, iid seeding from the '
         'length prior at cutoff n, complete island graph, mN = 1 (a generation = I·N births), checks every 20 generations, common '
         'generation budget 10⁵ in every cell. Paired RNG seeds across n (the multinomial draw differs, so intervals are unpaired). '
         'Wilson 95% intervals throughout. Raw rows: `runs/seeds-in-n.json`.', '']
    # ---------------- static
    L += ['## Static prior masses', '',
          '| n | classes | μ(ALLC) | μ(D) | μ(self-cooperators) | μ(core = unfakeable) | μ(FairBot) | μ(fakeable self-coop) | μ(D-entering self-coop) | core classes / self-cooperators |',
          '|---|---|---|---|---|---|---|---|---|---|']
    mu_est = {}
    for r in st:
        d = S.data(r['n'])
        est = [k for k in d['coop'] if rho_D(d, k, 100) > 1e-3]
        mu_est[r['n']] = float(d['mu'][est].sum())
        r['mu_est'] = mu_est[r['n']]
        L.append('| %d | %d | %.3f | %.3f | %.4f | %.4f | %.4f | %.4f | %.4f | %d / %d |' % (
            r['n'], r['classes'], r['mu_C'], r['mu_D'], r['mu_coop'], r['mu_core'], r['mu_FB'], r['mu_fakeable'], mu_est[r['n']], r['n_core'], r['n_coop']))
    mu_core = {r['n']: r['mu_core'] for r in st}
    L += ['', 'D-entering = a self-cooperator whose single copy fixes on an all-D island of 100 with probability > 10⁻³ (all of them have ρ = 0.0421 there).', '']

    def cell(n, N, I, mN, T0=0):
        return [r for r in rows if (r['n'], r['N'], r['I'], r['mN'], r['T0']) == (n, N, I, mN, T0)]

    # ---------------- administrative censoring
    exp = {(n, N, I, mN, T0): reps for n, N, I, mN, T0, reps in S.cells()}
    missing = {k: v - len(cell(*k)) for k, v in exp.items() if v - len(cell(*k)) > 0}
    L += ['## Censoring', '',
          'Administrative censoring (cells stopped for time): %s. Dynamically unresolved runs (reached 10⁵ generations without certification): %d of %d. '
          'Largest single-run wall time %.1f s; total run exposure %.0f generations.' % (
              'none' if not missing else ', '.join('%s: %d runs not completed' % (k, v) for k, v in missing.items()),
              sum(r['status'] == 'unresolved' for r in rows), len(rows), max(r['time_s'] for r in rows), sum(r['stop_gen'] for r in rows)), '']

    # ---------------- per-island chances
    L += ['## Per-island chance p(N, n) (no-migration control, 100 runs × 4 islands per cell)', '',
          '| n | N | islands | efficient [95%] | defecting | other | not frozen | P(eff \\| no core seed) | P(eff \\| ≥ 1 core seed) | islands with ≥ 1 core seed |',
          '|---|---|---|---|---|---|---|---|---|---|']
    P = {}
    for n in NS:
        for N in (100, 400, 1600):
            s = cell(n, N, 4, 0.0)
            if not s: continue
            outs = [o for r in s for o in r['isl_out']]
            nc = [c for r in s for c in r['seed_n_core']]
            k = sum(o == 'efficient' for o in outs); m = len(outs)
            P[(n, N)] = (k, m)
            e0 = [o == 'efficient' for o, c in zip(outs, nc) if c == 0]; e1 = [o == 'efficient' for o, c in zip(outs, nc) if c > 0]
            nf = sum(r['status'] != 'local-frozen' for r in s)
            L.append('| %d | %d | %d | %s | %.3f | %.3f | %d runs | %s | %s | %.2f |' % (
                n, N, m, ci(k, m), np.mean([o == 'defecting' for o in outs]), np.mean([o == 'other' for o in outs]), nf,
                ci2(sum(e0), len(e0)) if e0 else '-', ci2(sum(e1), len(e1)) if e1 else '-', len(e1) / m))
    summ['p'] = {'%d,%d' % k: dict(k=v[0], m=v[1], p=v[0] / v[1], ci=wilson(*v)) for k, v in P.items()}
    # predictor fits
    def fit(mu, use):
        x = np.array([mu[n] * np.sqrt(N) for n, N in use]); y = np.array([P[(n, N)][0] / P[(n, N)][1] for n, N in use])
        return float((x @ y) / (x @ x))
    fits = {}
    if all((n, N) in P for n in NS for N in (100, 400, 1600)):
        L += ['', 'Predictor p ≈ a·μ·√N. Fits through the origin; residual = (observed − predicted)/predicted; "in CI" = the prediction lies in the observed Wilson interval.', '',
              '| μ used | fit on | a | ' + ' | '.join('n=%d N=%d' % (n, N) for n in NS for N in (100, 400, 1600)) + ' |',
              '|---|---|---|' + '---|' * 12]
        for lab, mu in (('μ_core', mu_core), ('μ_est', mu_est)):
            for flab, use in (('p(100, 6)', [(6, 100)]), ('n = 6, all N', [(6, 100), (6, 400), (6, 1600)])):
                a = fit(mu, use)
                cellsr = []
                for n in NS:
                    for N in (100, 400, 1600):
                        pred = a * mu[n] * np.sqrt(N); k, m = P[(n, N)]; lo, hi = wilson(k, m)
                        cellsr.append('%+.0f%%%s' % (100 * (k / m - pred) / pred, '' if lo <= pred <= hi else ' (out)'))
                fits['%s|%s' % (lab, flab)] = dict(a=a, res=cellsr)
                L.append('| %s | %s | %.3f | %s |' % (lab, flab, a, ' | '.join(cellsr)))
        L += ['', 'Slope of log p on log N (N = 100, 400, 1,600): ' + '; '.join('n = %d: %.2f' % (n, np.polyfit(np.log([100, 400, 1600]), np.log([P[(n, N)][0] / P[(n, N)][1] for N in (100, 400, 1600)]), 1)[0]) for n in NS) + '.']
        # mean absolute residual at n = 7-9
        mar = {}
        for lab, mu in (('μ_core', mu_core), ('μ_est', mu_est)):
            a = fit(mu, [(6, 100)])
            mar[lab] = float(np.mean([abs(P[(n, N)][0] / P[(n, N)][1] - a * mu[n] * np.sqrt(N)) / (a * mu[n] * np.sqrt(N)) for n in (7, 8, 9) for N in (100, 400, 1600)]))
        L += ['', 'Mean absolute relative residual at n = 7–9 (a fitted on p(100, 6)): μ_core %.0f%%, μ_est %.0f%%.' % (100 * mar['μ_core'], 100 * mar['μ_est'])]
        summ['fits'] = fits; summ['mean_abs_resid'] = mar
    L.append('')

    # ---------------- run-level cells
    L += ['## Run-level outcomes with migration (mN = 1)', '',
          'CF / CS / MS / UN = certified frozen / certified separated / metastable / unresolved. Predicted = 1 − (1 − p(N, n))^I with the measured per-island p.', '',
          '| n | N | I | runs | CF / CS / MS / UN | efficient / defecting / other | efficient fraction [95%] | predicted 1−(1−p)^I | median freeze gen | median first certified coop island | median first certified core island | mean final P(C,C) |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|']
    E = {}
    for N, I in ((100, 4), (400, 4), (1600, 4), (100, 64), (100, 256), (400, 16)):
        for n in NS:
            s = cell(n, N, I, 1.0)
            if not s: continue
            m = len(s)
            cat = [sum(r['status'] == c for r in s) for c in ('certified-frozen', 'certified-separated', 'metastable', 'unresolved')]
            oc = [sum(r['outcome'] == o for r in s) for o in ('efficient', 'defecting', 'other')]
            E[(n, N, I)] = (oc[0], m)
            pr = 1 - (1 - P[(n, N)][0] / P[(n, N)][1]) ** I if (n, N) in P else float('nan')
            fc = [r['first_cert'] for r in s if r['first_cert'] >= 0]; fk = [r['first_cert_core'] for r in s if r['first_cert_core'] >= 0]
            L.append('| %d | %d | %d | %d | %d / %d / %d / %d | %d / %d / %d | %s | %.2f | %d | %s | %s | %.3f |' % (
                n, N, I, m, *cat, *oc, ci2(oc[0], m), pr, np.median([r['stop_gen'] for r in s]),
                ('%d (%d runs)' % (np.median(fc), len(fc))) if fc else 'none', ('%d (%d runs)' % (np.median(fk), len(fk))) if fk else 'none',
                np.mean([r['pcc'] for r in s])))
    summ['eff'] = {'%d,%d,%d' % k: dict(k=v[0], m=v[1], ci=wilson(*v)) for k, v in E.items()}
    pool = []
    for N, I in ((100, 4), (400, 4), (1600, 4), (400, 16)):
        k = sum(E[(n, N, I)][0] for n in NS); m = sum(E[(n, N, I)][1] for n in NS)
        pk = sum(P[(n, N)][0] for n in NS); pm = sum(P[(n, N)][1] for n in NS); plo, phi = wilson(pk, pm)
        pool.append('(%d, %d): observed %s, predicted %.2f [%.2f, %.2f]' % (N, I, ci2(k, m), 1 - (1 - pk / pm) ** I, 1 - (1 - plo) ** I, 1 - (1 - phi) ** I))
    L += ['', 'Pooled over n = 6–9 (predicted interval from the Wilson interval of the pooled p): ' + '; '.join(pool) + '.']
    # conditioning on seed
    L += ['', 'Outcome conditioned on the seed (I = 4 cells, pooled over n): efficient fraction by the number of islands seeded with ≥ 1 core program.', '',
          '| N | 0 islands | 1 | 2 | 3–4 |', '|---|---|---|---|---|']
    for N in (100, 400, 1600):
        s = [r for n in NS for r in cell(n, N, 4, 1.0)]
        row = []
        for lo, hi in ((0, 0), (1, 1), (2, 2), (3, 4)):
            t = [r['outcome'] == 'efficient' for r in s if lo <= sum(c > 0 for c in r['seed_n_core']) <= hi]
            row.append(('%d/%d' % (sum(t), len(t))) if t else '-')
        L.append('| %d | %s |' % (N, ' | '.join(row)))
    L += ['', 'Core programs alive (summed over islands) at global ALLC extinction, efficient vs defecting runs, I = 4 (pooled over n): ' +
          '; '.join('N = %d: efficient median %s, defecting median %s, defecting runs with 0 core left %s' % (
              N, (lambda v: '%d' % np.median(v) if v else '-')([r['core_at_extC'] for n in NS for r in cell(n, N, 4, 1.0) if r['outcome'] == 'efficient' and r['core_at_extC'] is not None]),
              (lambda v: '%d' % np.median(v) if v else '-')([r['core_at_extC'] for n in NS for r in cell(n, N, 4, 1.0) if r['outcome'] == 'defecting' and r['core_at_extC'] is not None]),
              (lambda v: '%d/%d' % (sum(x == 0 for x in v), len(v)) if v else '-')([r['coop_at_extC'] for n in NS for r in cell(n, N, 4, 1.0) if r['outcome'] == 'defecting' and r['coop_at_extC'] is not None]))
              for N in (100, 400, 1600)) + ' (the last count uses all self-cooperators).', '']

    # ---------------- nucleation then spread
    L += ['## Nucleation-then-spread control, (100, 64), migration off for the first 2,000 generations', '',
          '| n | runs | certified coop islands at switch: mean [min, max] | of which core-only: mean | frozen non-coop islands: mean | unfrozen islands at switch: mean | runs with 0 certified coop islands | efficient after [95%] | P(eff \\| ≥ 1 certified coop island) | predicted P(≥ 1) = 1−(1−p)^64 | median stop gen |',
          '|---|---|---|---|---|---|---|---|---|---|---|']
    for n in (6, 9):
        s = cell(n, 100, 64, 1.0, 2000)
        if not s: continue
        a = [r['at_T0'] for r in s if r['at_T0'] is not None and r['stop_gen'] >= 2000]
        early = [r for r in s if r['stop_gen'] < 2000]
        cc = [x['cert_coop'] for x in a]
        k = sum(r['outcome'] == 'efficient' for r in s)
        pos = [r for r in s if r['stop_gen'] >= 2000 and r['at_T0']['cert_coop'] > 0]
        p = P[(n, 100)][0] / P[(n, 100)][1] if (n, 100) in P else float('nan')
        L.append('| %d | %d | %.1f [%d, %d] | %.1f | %.1f | %.1f | %d (+%d stopped before the switch: %s) | %s | %s | %.3f | %d |' % (
            n, len(s), np.mean(cc) if cc else 0, min(cc) if cc else 0, max(cc) if cc else 0, np.mean([x['cert_core'] for x in a]) if a else 0,
            np.mean([x['frozen_other'] for x in a]) if a else 0, np.mean([x['not_frozen'] for x in a]) if a else 0,
            sum(c == 0 for c in cc), len(early), ', '.join(r['outcome'] for r in early) or '-', ci2(k, len(s)),
            ci2(sum(r['outcome'] == 'efficient' for r in pos), len(pos)) if pos else '-', 1 - (1 - p) ** 64, np.median([r['stop_gen'] for r in s])))
        summ['nucleation_%d' % n] = dict(cert_coop=cc, eff=k, runs=len(s))
    L += ['', 'Per-island establishment by the switch (certified coop islands / 64) against the no-migration p(100, n): ' +
          '; '.join('n = %d: %.3f vs %.3f' % (n, np.mean([r['at_T0']['cert_coop'] / 64 for r in cell(n, 100, 64, 1.0, 2000) if r['at_T0'] and r['stop_gen'] >= 2000] or [np.nan]),
                                             P[(n, 100)][0] / P[(n, 100)][1]) for n in (6, 9) if (n, 100) in P) + '.', '']

    # ---------------- losses
    L += ['## Cooperative islands lost (≥ 90% → < 50% self-cooperators), mN = 1 cells', '',
          '| n | losses before / after global ALLC extinction | per run (after) [runs] | held by core / fakeable self-coop (after) | strict invasions of monomorphic islands (core-held) | neutral replacements | against selection | mixed-island displacements | runs with losses: efficient |',
          '|---|---|---|---|---|---|---|---|---|']
    LS = {}
    for n in NS:
        s = [r for r in rows if r['n'] == n and r['mN'] == 1.0 and r['T0'] == 0]
        ls = [x for r in s for x in r['losses']]
        aft = [x for x in ls if x['after_allc']]
        LS[n] = ls
        mech = collections.Counter(x['mech'] for x in ls)
        si_core = sum(1 for x in ls if x['mech'].startswith('strict') and x.get('held_core'))
        wl = [r for r in s if r['losses']]
        L.append('| %d | %d / %d | %.3f [%d] | %d / %d | %d (%d) | %d | %d | %d | %s |' % (
            n, sum(not x['after_allc'] for x in ls), len(aft), len(aft) / len(s), len(s),
            sum(1 for x in aft if x.get('held_core')), sum(1 for x in aft if x.get('held_coop') and not x.get('held_core')),
            mech['strict invasion of a monomorphic island'], si_core, mech['neutral replacement'], mech['fixation against selection'],
            mech['displacement from a mixed island'], ci2(sum(r['outcome'] == 'efficient' for r in wl), len(wl)) if wl else '-'))
    L += ['', 'Held class → taker, after global ALLC extinction (all n; count by n = 6/7/8/9):', '']
    c = collections.defaultdict(lambda: [0, 0, 0, 0])
    for j, n in enumerate(NS):
        for x in LS[n]:
            if x['after_allc']:
                c[(x['held'], x['taker'], x['mech'], 'core' if x.get('held_core') else 'fakeable')][j] += 1
    L += ['| held | taker | mechanism | held class | n = 6 / 7 / 8 / 9 |', '|---|---|---|---|---|']
    for kk, v in sorted(c.items(), key=lambda kv: -sum(kv[1]))[:25]:
        L.append('| `%s` | `%s` | %s | %s | %s |' % (kk[0], kk[1], kk[2], kk[3], ' / '.join(map(str, v))))
    L += ['', 'Before global ALLC extinction (all n): ' + ', '.join('`%s` → `%s` (%s) %d' % (k[0], k[1], k[2], v) for k, v in collections.Counter(
        (x['held'], x['taker'], x['mech']) for n in NS for x in LS[n] if not x['after_allc']).most_common(10)) + '.']
    core_l = [(n, x) for n in NS for x in LS[n] if x.get('held_core')]
    if core_l:
        L += ['', 'Core-held losses (%d; first 25): ' % len(core_l) + '; '.join('n %d gen %d (snapshot gen %s) `%s` → `%s`, %s, residents %d, ALLC in snapshot %s, snapshot %s' % (
            n, x['gen'], x.get('snapshot_gen', '?'), x['held'], x['taker'], x['mech'], x['n_residents'], x['allc_in_snapshot'], ', '.join('`%s` %d' % tuple(t) for t in x['snapshot'][:4])) for n, x in core_l[:25])]
    L.append('')
    summ['losses'] = {n: dict(total=len(LS[n]), after=sum(x['after_allc'] for x in LS[n])) for n in NS}
    # probe-fakers: non-self-cooperators that strictly invade some fakeable self-cooperator's monomorphic world
    L += ['', 'Post-ALLC losses held by a fakeable self-cooperator and taken by a probe-faker (a class, not itself a self-cooperator, that strictly invades '
          'some fakeable self-cooperator\'s monomorphic world): ' + '; '.join('n = %d: %s' % (n, (lambda xs, pf: ci2(sum(1 for x in xs if x.get('held_coop') and not x.get('held_core') and x['taker'] in pf), len(xs)) if xs else '-')(
              [x for x in LS[n] if x['after_allc']], {S.data(n)['names'][q] for q in range(len(S.data(n)['names'])) if q not in S.data(n)['coop'] and any(S.data(n)['U'][q, a] > S.data(n)['U'][a, a] + 1e-9 for a in S.data(n)['fakeable'])}))
              for n in NS) + '.']
    L += ['', 'Post-ALLC losses per run by cell (mean; bootstrap 95% over runs):', '', '| N | I | ' + ' | '.join('n = %d' % n for n in NS) + ' |', '|---|---|' + '---|' * len(NS)]
    brng = np.random.default_rng(5)
    for N, I in ((100, 4), (400, 4), (1600, 4), (100, 64), (100, 256), (400, 16)):
        row = []
        for n in NS:
            v = np.array([sum(x['after_allc'] for x in r['losses']) for r in cell(n, N, I, 1.0)], float)
            if not len(v): row.append('-'); continue
            bs = brng.choice(v, (4000, len(v))).mean(1)
            row.append('%.2f [%.2f, %.2f]' % (v.mean(), *np.percentile(bs, [2.5, 97.5])))
        L.append('| %d | %d | %s |' % (N, I, ' | '.join(row)))
    nl = [x for n in (6, 9) for r in cell(n, 100, 64, 1.0, 2000) for x in r['losses']]
    L += ['', 'Nucleation-control runs (reported separately): %d losses, %s.' % (len(nl), ', '.join('`%s` → `%s` (%s)' % (x['held'], x['taker'], x['mech']) for x in nl[:8]) or 'none')]

    # ---------------- frozen compositions
    L += ['## Frozen efficient states: who holds the islands', '',
          'Island holder = largest class on the island at the stop. Shares over islands of efficient runs (mN = 1, all cells pooled) and over efficient islands of the no-migration control. '
          'E_k = μ_k·ρ_k(D, 100). Spearman ρ over all self-cooperators.', '']
    comp = {}
    brng = np.random.default_rng(11)
    for n in NS:
        d = S.data(n); nm = d['names']; mu = d['mu']
        Ek = {nm[k]: mu[k] * rho_D(d, k, 100) for k in d['coop']}
        for lab, sel in (('migration', lambda r: r['mN'] == 1.0 and r['T0'] == 0 and r['outcome'] == 'efficient'), ('no migration', lambda r: r['mN'] == 0.0)):
            h = collections.Counter(); per_run = []
            for r in rows:
                if r['n'] != n or not sel(r): continue
                hr = collections.Counter()
                for hh, o in zip(r['holders'], r['isl_out']):
                    if o == 'efficient' or r['mN'] == 1.0:
                        h[hh] += 1; hr[hh] += 1
                per_run.append(hr)
            tot = sum(h.values())
            if not tot: continue
            core_names = {nm[k] for k in d['coop_unfakeable']}
            fb2 = (h['BOX(THEM(ME))'] + h['BOX1(THEM(ME))']) / tot
            fake = sum(v for k, v in h.items() if k in Ek and k not in core_names) / tot
            keys = list(Ek)
            rs = spearmanr([Ek[k] for k in keys], [h.get(k, 0) / tot for k in keys]).correlation
            ent = [k for k in keys if rho_D(d, nm.index(k), 100) > 1e-3]
            rs_occ = spearmanr([Ek[k] for k in ent], [h.get(k, 0) / tot for k in ent]).correlation
            pE = np.array([Ek[k] for k in keys]); pE = pE / pE.sum(); ob = np.array([h.get(k, 0) / tot for k in keys])
            tv = 0.5 * float(np.abs(pE - ob).sum())
            # run-cluster bootstrap for shares (islands within a migration run are not independent)
            def share(cs, names_):
                a_ = sum(c[x] for c in cs for x in names_); b_ = sum(sum(c.values()) for c in cs)
                return a_ / b_ if b_ else float('nan')
            fakeset = [k for k in Ek if k not in core_names]
            tt = ['BOX(THEM(THEM))', 'BOX1(THEM(THEM))']
            bsf, bsF, bsT = [], [], []
            for _ in range(1000):
                smp = [per_run[j] for j in brng.integers(0, len(per_run), len(per_run))]
                bsf.append(share(smp, ['BOX(THEM(ME))', 'BOX1(THEM(ME))'])); bsF.append(share(smp, fakeset)); bsT.append(share(smp, tt))
            comp[(n, lab)] = dict(tot=tot, fb2=fb2, fake=fake, spearman=rs, spearman_entering=rs_occ, top=h.most_common(6), tv=tv, runs=len(per_run),
                                  boot_fb2=tuple(np.percentile(bsf, [2.5, 97.5])), boot_fake=tuple(np.percentile(bsF, [2.5, 97.5])),
                                  tt=share(per_run, tt), boot_tt=tuple(np.percentile(bsT, [2.5, 97.5])),
                                  ci_fb2=wilson(h['BOX(THEM(ME))'] + h['BOX1(THEM(ME))'], tot),
                                  ci_fake=wilson(sum(v for k, v in h.items() if k in Ek and k not in core_names), tot),
                                  pred={k: Ek[k] / sum(Ek.values()) for k in sorted(Ek, key=lambda k: -Ek[k])[:6]})
    L += ['Intervals are run-cluster bootstrap 95% (islands within a run are not independent; no-migration islands are, so Wilson and bootstrap agree there). '
          'TV = total-variation distance between the holder distribution and E_k normalized.', '',
          '| n | sample | runs / islands | FairBot + `BOX1(THEM(ME))` | fakeable self-coop | `BOX(THEM(THEM))` + `BOX1(THEM(THEM))` | Spearman (all self-coop) | Spearman (D-entering only) | TV to E_k | top holders (share) | E_k-predicted shares (top) |',
          '|---|---|---|---|---|---|---|---|---|---|---|']
    for (n, lab), v in sorted(comp.items()):
        L.append('| %d | %s | %d / %d | %.2f [%.2f, %.2f] | %.2f [%.2f, %.2f] | %.2f [%.2f, %.2f] | %.2f | %.2f | %.2f | %s | %s |' % (
            n, lab, v['runs'], v['tot'], v['fb2'], *v['boot_fb2'], v['fake'], *v['boot_fake'], v['tt'], *v['boot_tt'], v['spearman'], v['spearman_entering'], v['tv'],
            '; '.join('`%s` %.2f' % (k, c / v['tot']) for k, c in v['top']), '; '.join('`%s` %.2f' % kv for kv in list(v['pred'].items())[:4])))
    summ['composition'] = {'%d|%s' % k: {kk: vv for kk, vv in v.items() if kk != 'pred'} for k, v in comp.items()}
    L.append('')

    # ---------------- ALLC extinction
    L += ['## ALLC extinction', '',
          'Island level: exact generation (birth resolution) at which each island\'s ALLC count first reaches 0, pooled over runs. Global: the generation at which the last ALLC dies.', '',
          '| n | N | I | mN | island median [IQR] | island 90th pct | global median / max | ALLC re-entries per run |', '|---|---|---|---|---|---|---|---|']
    EX = {}
    for n, N, I, mN, T0, reps in sorted(S.cells(), key=lambda c: (c[3] == 0, c[4], c[1], c[2], c[0])):
        s = cell(n, N, I, mN, T0)
        if not s: continue
        t = np.array([v for r in s for v in r['tC_first'] if v >= 0]); gl = [r['tC_glob'] for r in s if r['tC_glob'] >= 0]
        if not len(t): continue
        EX[(n, N, I, mN, T0)] = float(np.median(t))
        L.append('| %d | %d | %d | %g%s | %.1f [%.1f, %.1f] | %.1f | %s | %.1f |' % (
            n, N, I, mN, ', T0 2000' if T0 else '', np.median(t), *np.percentile(t, [25, 75]), np.percentile(t, 90),
            ('%.1f / %.1f' % (np.median(gl), max(gl))) if gl else '-', np.mean([r['C_reentries'] for r in s])))
    L += ['', 'Ratio of island-level medians n = 9 / n = 6: ' + '; '.join('(%d, %d, %g) %.2f' % (N, I, mN, EX[(9, N, I, mN, 0)] / EX[(6, N, I, mN, 0)])
                                                                         for (n, N, I, mN, T0) in EX if n == 6 and T0 == 0 and (9, N, I, mN, 0) in EX) + '.', '']
    summ['allc_ext_median'] = {'%d,%d,%d,%g,%d' % k: v for k, v in EX.items()}

    # ---------------- unresolved
    un = [r for r in rows if r['status'] in ('unresolved', 'metastable')]
    L += ['## Unresolved and metastable runs', '']
    if un:
        for r in un:
            L.append('- n %d (%d, %d, mN %g) rep %d: %s, P(C,C) %.3f, support %s; non-identical pairs %s' % (
                r['n'], r['N'], r['I'], r['mN'], r['rep'], r['status'], r['pcc'], ', '.join('`%s` %d' % kv for kv in sorted(r['final'].items(), key=lambda kv: -kv[1])[:6]),
                r.get('unresolved_pairs', [])[:4]))
    else:
        L.append('None.')
    L.append('')
    nfz = [r for r in rows if r['mN'] == 0.0 and r['status'] != 'local-frozen']
    if nfz:
        L += ['No-migration runs with some island unfrozen at the horizon: %d (%s).' % (len(nfz), '; '.join('n %d N %d rep %d' % (r['n'], r['N'], r['rep']) for r in nfz[:10])), '']
    vp = os.path.join(os.path.dirname(__file__), 'seeds_in_n_verdicts.md')
    if os.path.exists(vp):
        L += [open(vp).read()]
    out = '\n'.join(L) + '\n'
    open(os.path.join(S.RUNS, 'seeds-in-n.md'), 'w').write(out)
    slim = []
    for r in rows:
        x = {k: v for k, v in r.items() if k not in ('trace_cc', 'trace_np', 'tC_last')}
        x['isl_out'] = ''.join(_ENC[o] for o in r['isl_out'])
        if r['I'] > 16:
            x.pop('seed_core', None); x.pop('seed_n_C', None)
        slim.append(x)
    json.dump(dict(summary=summ, rows=slim, note='slim rows: isl_out encoded e/d/o; seed_core and seed_n_C dropped for I > 16; traces and tC_last only in the raw rows file (not committed)'), open(os.path.join(S.RUNS, 'seeds-in-n.json'), 'w'), default=float)
    print(out)


if __name__ == '__main__':
    main()
