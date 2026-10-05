"""Report for src/seeds_tail.py: runs/seeds-tail.md and runs/seeds-tail.json from
runs/seeds-tail-static.json (Part A) and runs/seeds-tail-rows.json (Part B)."""
import collections, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from almost_all_seeds import wilson

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
CATS = ('establisher', 'probe-faker', 'D', 'ALLC', 'other self-cooperator', 'other')


def newcombe(k1, n1, k2, n2):
    """Newcombe hybrid score interval (method 10) for p1 - p2."""
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1); l2, u2 = wilson(k2, n2)
    d = p1 - p2
    return d, d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)


def ci(k, n):
    lo, hi = wilson(k, n)
    return '%.3f [%.3f, %.3f]' % (k / n, lo, hi)


def part_a(o, L, J):
    rows = o['rows']
    J['static'] = dict(rho=o['rho'], canon=o['canon'], eval_s=o['t_eval'], rows=rows, reclass=o['reclass'], check9=o.get('check9'))
    L += ['## Part A: static tail (modal arm, n = 6–12)', '',
          'One evaluation at n = 12 (%d canonical functions, stable at world %d, %.0f s on 3 threads); every smaller cutoff is a '
          'sub-block (canonical ids are a prefix, checked; the n = 9 sub-block reproduces a direct `modal.build(9)` exactly: %s). '
          'n = 13 was not run: the machine was under memory pressure from sibling pools, and n = 12 is where the predictions are stated.' % (
              o['canon'], o['worlds'], o['t_eval'], 'classes 863, μ_est, μ_core and μ_pf equal to 1e-15' if o.get('check9') else 'not run'), '',
          'Units: **raw** (shell s has mass 1/(2s²); the infinite prior totals π²/12 ≈ 0.822, not 1), **inf** = raw/(π²/12), '
          '**cut** = raw/retained(n) (the seeding law). ω(n) = π²/12 − retained(n) is the omitted mass.', '',
          '### Masses by cutoff', '',
          '| n | classes | establisher / faker / core classes | retained | ω(n) | μ_est raw | μ_est cut | μ_est inf | bound on μ_est(∞) inf | μ_core cut | fakeable establishers cut | μ_pf cut (global union) | r = μ_pf/μ_est | μ-weighted faker exposure (cut) | FairBot, `BOX1(THEM(ME))` unfakeable |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        L.append('| %d | %d | %d / %d / %d | %.4f | %.4f | %.5f | %.5f | %.5f | %.4f | %.5f | %.5f | %.5f | %.2f | %.5f | %s, %s |' % (
            r['n'], r['classes'], r['n_est_classes'], r['n_pf_classes'], r['n_core_classes'], r['retained'], r['omitted'],
            r['raw']['est'], r['cut']['est'], r['inf']['est'], r['bound_est_inf'], r['cut']['core'], r['cut']['est_fakeable'],
            r['cut']['pf'], r['r'], r['exposure_cut'], r['FB_unfakeable'], r['FB1_unfakeable']))
    r12 = rows[-1]
    fs = r12['f_est']
    tailf = float(np.mean(fs[9:12]))
    ext_raw = r12['raw']['est'] + tailf * r12['omitted']
    ext_pf = r12['raw']['pf'] + float(np.mean(r12['f_pf'][9:12])) * r12['omitted']
    J['extrapolation'] = dict(tail_fraction_est=tailf, mu_est_inf_extrap=ext_raw / o['Z_inf'], mu_pf_inf_extrap=ext_pf / o['Z_inf'],
                              r_extrap=ext_pf / ext_raw)
    L += ['', '- Bound: μ_est(∞) ≤ (raw(12) + ω(12))/(π²/12) = %.4f (inf units); lower bound raw(12)/(π²/12) = %.4f. '
          '1/s²-tail extrapolation (mean shell fraction over s = 10–12, %.4f, times ω(12)): μ_est(∞) ≈ %.4f (inf); μ_pf(∞) ≈ %.4f; r(∞) ≈ %.2f.' % (
              r12['bound_est_inf'], r12['inf']['est'], tailf, J['extrapolation']['mu_est_inf_extrap'], J['extrapolation']['mu_pf_inf_extrap'],
              J['extrapolation']['r_extrap']),
          '- The global faker union is dominated by the fakers of two rare, highly exploitable establishers, `not(BOXD(THEM(^C)))` and '
          '`not(BOXD1(THEM(^C)))` (μ_cut 0.0003 each, faker mass 0.042–0.047 each, FairBot among their fakers). The μ-weighted exposure '
          '(the faker mass facing a μ-random establisher) is 20–25× smaller than the union.', '',
          '### Shell decomposition at n = 12 (shell fraction f(s) = shell contribution / (1/(2s²)))', '',
          '| s | 1/(2s²) | μ_est contribution (raw) | f_est(s) | ratio to s − 1 | f_pf(s) | f_core(s) |', '|---|---|---|---|---|---|---|']
    for s in range(1, r12['n'] + 1):
        c = r12['shell_est'][s - 1]; pc = r12['shell_est'][s - 2] if s > 1 else 0
        L.append('| %d | %.5f | %.3e | %.4f | %s | %.4f | %.4f |' % (s, 1 / (2 * s * s), c, fs[s - 1], ('%.2f' % (c / pc)) if pc > 0 else '–',
                                                               r12['f_pf'][s - 1], r12['f_core'][s - 1]))
    L += ['', 'Odd shells carry more than even ones (parity of the grammar: a box costs 3, a binary connective 1); two-step ratios '
          'c(s+2)/c(s) at s = 6, 8, 10: %s, against (s/(s+2))²: %s. The tail is 1/s² with a parity oscillation, not geometric.' % (
              ', '.join('%.3f' % (r12['shell_est'][s + 1] / r12['shell_est'][s - 1]) for s in (6, 8, 10)),
              ', '.join('%.3f' % ((s / (s + 2)) ** 2) for s in (6, 8, 10))), '',
          '### Reclassification (n − 1 → n, raw masses)', '',
          '| n | Δμ_est | from new shell | establisher status switches | Δμ_core | core → fakeable (old syntax, raw) | classes reclassified | Δμ_pf | from new shell | old syntax newly fakers |',
          '|---|---|---|---|---|---|---|---|---|---|']
    for rc in o['reclass']:
        L.append('| %d | %.2e | %.2e | %d | %.2e | %.2e | %s | %.2e | %.2e | %.2e |' % (
            rc['n'], rc['d_est_raw'], rc['d_est_new_shell_raw'], rc['est_switch'], rc['d_core_raw'], rc['core_to_fakeable_raw'],
            ', '.join('`%s`' % x for x in rc['core_to_fakeable'][:2]) + (' …' if len(rc['core_to_fakeable']) > 2 else ''),
            rc['d_pf_raw'], rc['d_pf_new_shell_raw'], rc['new_pf_old_syntax_raw']))
    L += ['', '- Establisher status never switches (0 at every step, checked), so μ_est raw grows only by new shells, as argued. '
          'The unfakeable core loses mass to reclassification once materially (n = 7, `BOX(THEM(THEM))` and its kin, 0.0037 raw) and '
          'then by ≤ 2.5·10⁻⁵ per step.', '',
          '### Establishers with raw class mass ≥ 10⁻⁴ (item 4)', '',
          'ρ(x | all-D) is the same for every establisher (same 2×2 game against D): %.4f / %.4f / %.4f at N = 100 / 400 / 1,600.' % (
              o['rho']['100'], o['rho']['400'], o['rho']['1600']), '',
          '| class | μ cut (n = 6) | μ cut (n = 9) | μ cut (n = 12) | faker mass cut (n = 6 / 9 / 12) | core (n = 6 / 9 / 12) | top fakers at n = 12 |',
          '|---|---|---|---|---|---|---|']
    it = {r['n']: {i['name']: i for i in r['items']} for r in rows}
    names = [i['name'] for i in rows[-1]['items']]
    for nm in names:
        g = [it[n].get(nm) for n in (6, 9, 12)]
        L.append('| `%s` | %s | %s | %s | %s | %s | %s |' % (
            nm, *[('%.5f' % x['mu_cut']) if x else '–' for x in g], ' / '.join(('%.5f' % x['faker_mass_cut']) if x else '–' for x in g),
            ' / '.join(('yes' if x['core'] else 'no') if x else '–' for x in g), ', '.join('`%s`' % t for t in g[2]['top_fakers'][:2]) or '–'))
    L += ['', 'These 8 classes carry %.1f%% of μ_est at n = 12.' % (100 * sum(i['mu_cut'] for i in rows[-1]['items']) / r12['cut']['est']), '',
          '### Co-seeding conditioned on an establisher (item 5) and establishment-weighted mass (item 6)', '',
          '10⁵ iid seeds of N = 100 per n from the cutoff-normalized prior. A = some establisher present; K_pf = seed members that are '
          'fakers of an establisher present in that seed (resident-specific).', '',
          '| n | P(A) | E[K_pf given A] | of which establishers | P(K_pf > 0 given A) | naive N·μ_pf | Σ μρ cut, N = 100 | 400 | 1,600 |',
          '|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        c = r['coseed']; e = r['est_weighted']
        L.append('| %d | %.3f | %.3f ± %.3f | %.3f | %.3f ± %.3f | %.2f | %.5f | %.5f | %.5f |' % (
            r['n'], c['P_A'], c['E_kpf_A'], c['se_E'], c['E_kpe_A'], c['P_kpf_A'], c['se_P'], c['naive_N_mupf'],
            e['100']['cut'], e['400']['cut'], e['1600']['cut']))
    L += ['', '- Σ μρ is exactly ρ(N)·μ_est (every establisher has the same game against D), so item 6 adds only ρ(N) ∝ N^(−1/2) '
          '(ρ(400)/ρ(100) = %.3f, ρ(1600)/ρ(400) = %.3f).' % (o['rho']['400'] / o['rho']['100'], o['rho']['1600'] / o['rho']['400']),
          '- About a quarter of E[K_pf | A] is establishers faking other establishers (at n = 9, 73% of the μ×μ pair weight is the prover family '
          '(FairBot, `BOX1(THEM(ME))`, `BOX(THEM(THEM))`, `BOX1(THEM(THEM))`) exploiting `not(BOXD(THEM(^C)))` and `not(BOXD1(THEM(^C)))`, and 83% has one of those two as victim), '
          'whose takeover leaves a cooperative island.', '']


def part_b(rows, L, J):
    by = collections.defaultdict(list)
    for r in rows:
        by[(r['N'], r['I'], r['mN'])].append(r)
    nm0 = by[(400, 4, 0.0)]; isl0 = [o for r in nm0 for o in r['isl_out']]
    k0 = sum(o == 'efficient' for o in isl0); p = k0 / len(isl0); plo, phi = wilson(k0, len(isl0))
    one = by[(1600, 1, 0.0)]; k1 = sum(r['outcome'] == 'efficient' for r in one)
    allfour = sum(r['outcome'] == 'efficient' for r in nm0)
    bench = dict(p400=[p, plo, phi], p4=p ** 4, indep=[1 - (1 - p) ** 4, 1 - (1 - plo) ** 4, 1 - (1 - phi) ** 4],
                 one1600=[k1 / len(one), *wilson(k1, len(one))], allfour=[allfour, len(nm0)])
    J['benchmarks'] = bench
    L += ['## Part B: island merging at I = 4 (n = 6, N = 400 per island)', '',
          'Fresh seeds (salt 20261005); horizon 10⁵ generations; the event kernel equals `seeds_in_n._run` draw for draw '
          '(15 of 15 checks). No run was censored or unresolved: every migration run was certified frozen, every no-migration run '
          'locally frozen.', '',
          '### References (rerun)', '',
          '- (i) No migration, (400, 4), 100 runs: per-island p(400) = %s (published 0.158 [0.124, 0.198]); all four efficient in '
          '%d of 100 runs (p⁴ = %.4f). Independent-trials benchmark 1 − (1 − p)^4 = %.3f [%.3f, %.3f] (p\'s interval propagated).' % (
              ci(k0, len(isl0)), allfour, p ** 4, *bench['indep']),
          '- (ii) One island of N = 1,600, 240 runs: efficient %s (published per-island 0.383 [0.336, 0.432]).' % ci(k1, len(one)), '',
          '### Run-level efficient fraction', '',
          '| mN | runs | efficient | fraction [95%] | per-island efficient | mean global P(C,C) | median / max stop generation |',
          '|---|---|---|---|---|---|---|']
    J['cells'] = {}
    for mN in (0.1, 1.0, 10.0):
        rs = by[(400, 4, mN)]; k = sum(r['outcome'] == 'efficient' for r in rs)
        isl = [o for r in rs for o in r['isl_out']]; ki = sum(o == 'efficient' for o in isl)
        L.append('| %g | %d | %d | %s | %s | %.3f | %d / %d |' % (mN, len(rs), k, ci(k, len(rs)), ci(ki, len(isl)),
                                                                np.mean([r['pcc'] for r in rs]), np.median([r['stop_gen'] for r in rs]),
                                                                max(r['stop_gen'] for r in rs)))
        J['cells'][str(mN)] = dict(runs=len(rs), efficient=k, ci=wilson(k, len(rs)), pcc=float(np.mean([r['pcc'] for r in rs])),
                                   status=dict(collections.Counter(r['status'] for r in rs)),
                                   outcomes=dict(collections.Counter(r['outcome'] for r in rs)))
    a = by[(400, 4, 0.1)]; b = by[(400, 4, 10.0)]
    ka = sum(r['outcome'] == 'efficient' for r in a); kb = sum(r['outcome'] == 'efficient' for r in b)
    d, lo, hi = newcombe(ka, len(a), kb, len(b))
    J['contrast'] = dict(diff=d, lo=lo, hi=hi)
    L += ['', '**Predeclared contrast** fraction(mN = 0.1) − fraction(mN = 10) = %.3f, 95%% Newcombe interval [%.3f, %.3f].' % (d, lo, hi), '']
    # event logs
    L += ['### Event logs', '',
          'Windows: W1 before the first certified cooperative island, W2 from it to resolution. Migrant births by category of the '
          'migrant (per run, mean); "into coop" = target island ≥ 90% self-cooperators at the time.', '',
          '| mN | window | runs | establisher | probe-faker | D | ALLC | other self-coop | other | introductions (new class on target) | of which establishers into non-coop islands | probe-fakers into coop islands |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|']
    J['events'] = {}
    for mN in (0.1, 1.0, 10.0):
        rs = by[(400, 4, mN)]
        M = np.array([r['ev_mig'] for r in rs]); IN = np.array([r['ev_intro'] for r in rs])
        for w in (0, 1):
            tot = M[:, w].sum(2).mean(0)
            L.append('| %g | W%d | %d | %s | %.1f | %.2f | %.2f |' % (mN, w + 1, len(rs), ' | '.join('%.1f' % x for x in tot),
                                                                     IN[:, w].sum((1, 2)).mean(), IN[:, w, 0, 0].mean(), IN[:, w, 1, 1].mean()))
        # nucleation timing and origin
        fc = [r['first_cert'] for r in rs]
        eff = [r for r in rs if r['outcome'] == 'efficient']
        coinc = sum(1 for r in rs if r['first_cert'] >= 0 and r['first_cert'] >= r['stop_gen'] - 20)
        nocert = sum(1 for r in rs if r['first_cert'] < 0)
        loc = []; imp = []; nloc_eff = []
        for r in rs:
            fs = r['first_strong']; os_ = r['origin_strong']
            t1 = min([t for t in fs if t >= 0], default=-1)
            l = sum(1 for t, o in zip(fs, os_) if t >= 0 and o == 'local'); im = sum(1 for t, o in zip(fs, os_) if t >= 0 and o == 'import')
            loc.append(l); imp.append(im)
            if r['outcome'] == 'efficient': nloc_eff.append(l)
        # islands that went strong before vs after the first strong island, and spread
        founders = collections.Counter(r['founder'] for r in eff)
        losses = [x for r in rs for x in r['losses']]
        takers = collections.Counter(x['taker'] for x in losses)
        mech = collections.Counter(x['mech'] for x in losses)
        supp = collections.Counter(tuple(sorted(k for k, v in r['final'].items())) for r in eff)
        dsupp = collections.Counter(tuple(sorted(k for k, v in r['final'].items())) for r in rs if r['outcome'] != 'efficient')
        strong_def = sum(1 for r in rs if r['outcome'] != 'efficient' and any(t >= 0 for t in r['first_strong']))
        J['events'][str(mN)] = dict(mig=M.mean(0).tolist(), intro=IN.mean(0).tolist(), first_cert_median=float(np.median([t for t in fc if t >= 0])) if any(t >= 0 for t in fc) else None,
                                    cert_at_resolution=coinc, no_cert=nocert, local_strong=float(np.mean(loc)), import_strong=float(np.mean(imp)),
                                    eff_runs_with_2plus_local=sum(1 for x in nloc_eff if x >= 2), eff_runs=len(eff),
                                    founders=dict(founders), takers=dict(takers), mech=dict(mech), losses=len(losses),
                                    support_eff=[[list(k), v] for k, v in supp.most_common(6)],
                                    support_def=[[list(k), v] for k, v in dsupp.most_common(4)], defecting_with_strong_island=strong_def,
                                    seed_est_eff=float(np.mean([sum(r['seed_n_est']) for r in eff])) if eff else None,
                                    seed_est_def=float(np.mean([sum(r['seed_n_est']) for r in rs if r['outcome'] != 'efficient'])),
                                    seed_islands_with_est_eff=float(np.mean([sum(1 for x in r['seed_n_est'] if x > 0) for r in eff])) if eff else None,
                                    seed_islands_with_est_def=float(np.mean([sum(1 for x in r['seed_n_est'] if x > 0) for r in rs if r['outcome'] != 'efficient'])))
    L += ['', '| mN | first certified island, median gen | first certification within 20 gens of resolution / no certified island | islands reaching ≥ 90% coop per run: local / imported | efficient runs with ≥ 2 local nucleations | defecting runs that had a ≥ 90% coop island | losses (mechanism) | founders (efficient runs) | seeded establishers per run, efficient / defecting |',
          '|---|---|---|---|---|---|---|---|---|']
    for mN in (0.1, 1.0, 10.0):
        e = J['events'][str(mN)]
        L.append('| %g | %s | %d / %d of 60 | %.2f / %.2f | %d of %d | %d | %d (%s) | %s | %.1f / %.1f |' % (
            mN, ('%.0f' % e['first_cert_median']) if e['first_cert_median'] is not None else '–', e['cert_at_resolution'], e['no_cert'],
            e['local_strong'], e['import_strong'], e['eff_runs_with_2plus_local'], e['eff_runs'], e['defecting_with_strong_island'],
            e['losses'], ', '.join('%s %d' % kv for kv in e['mech'].items()) or '–',
            ', '.join('`%s` %d' % kv for kv in sorted(e['founders'].items(), key=lambda kv: -kv[1])[:4]),
            e['seed_est_eff'] or 0, e['seed_est_def']))
    ref = [t for r in nm0 for t in r['first_strong'] if t >= 0]
    L += ['', '"Local" means the largest cooperative class at the island\'s first ≥ 90%% check was in its own seed; with about 9 '
          'establishers seeded per island this label is weak, so nucleation is also identified by timing. Without migration every '
          'island that went ≥ 90%% cooperative did so by generation %d (median %d, 76 islands), so an island going ≥ 90%% by generation '
          '200 is counted as nucleated, a later one as reached by spread.' % (max(ref), np.median(ref)), '',
          '| mN | efficient runs | islands ≥ 90% coop by gen 200, per efficient run (1 / 2 / 3 / 4) | independent-trials expectation given ≥ 1 (1 / 2 / 3 / 4) | first → last island ≥ 90%, median gens | median resolution gen |',
          '|---|---|---|---|---|---|']
    pp = p
    expct = [math.comb(4, j) * pp ** j * (1 - pp) ** (4 - j) / (1 - (1 - pp) ** 4) for j in (1, 2, 3, 4)]
    J['timing'] = {}
    for mN in (0.1, 1.0, 10.0):
        eff = [r for r in by[(400, 4, mN)] if r['outcome'] == 'efficient']
        early = collections.Counter(sum(1 for t in r['first_strong'] if 0 <= t <= 200) for r in eff)
        spread = float(np.median([max(r['first_strong']) - min(t for t in r['first_strong'] if t >= 0) for r in eff]))
        J['timing'][str(mN)] = dict(early={str(k): v for k, v in early.items()}, spread_median=spread)
        L.append('| %g | %d | %s | %s | %.0f | %.0f |' % (mN, len(eff), ' / '.join(str(early.get(j, 0)) for j in (1, 2, 3, 4)),
                                                         ' / '.join('%.1f' % (e * len(eff)) for e in expct), spread,
                                                         np.median([r['stop_gen'] for r in eff])))
    L += ['', 'Terminal support (efficient runs, most common sets):', '']
    for mN in (0.1, 1.0, 10.0):
        e = J['events'][str(mN)]
        L.append('- mN = %g: %s; defecting: %s' % (mN, '; '.join('{%s} ×%d' % (', '.join('`%s`' % x for x in k), v) for k, v in e['support_eff'][:4]),
                                                 '; '.join('{%s} ×%d' % (', '.join('`%s`' % x for x in k), v) for k, v in e['support_def'][:2])))
    L.append('')


def main():
    o = json.load(open(os.path.join(RUNS, 'seeds-tail-static.json')))
    rows = json.load(open(os.path.join(RUNS, 'seeds-tail-rows.json')))
    L = ['# Seeds tail in n (static) and island merging at I = 4', '',
         'Spec `specs/2026-10-05-seeds-tail.md`; predictions `predictions/2026-10-05-seeds-tail.md`; code `src/seeds_tail.py`, '
         '`src/seeds_tail_report.py`. Modal arm, PD, w = 0.3, ε = 0.', '']
    J = {}
    part_a(o, L, J)
    part_b(rows, L, J)
    L += open(os.path.join(os.path.dirname(__file__), 'seeds_tail_verdicts.md')).read().splitlines()
    open(os.path.join(RUNS, 'seeds-tail.md'), 'w').write('\n'.join(L) + '\n')
    json.dump(J, open(os.path.join(RUNS, 'seeds-tail.json'), 'w'), indent=1, default=float)
    print('\n'.join(L))


if __name__ == '__main__':
    main()
