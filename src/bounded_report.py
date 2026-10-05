"""Collect runs/bounded-provers-{static,chain,lottery}.json into runs/bounded-provers.md and runs/bounded-provers.json.

    python3 src/bounded_report.py
"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from bounded import ROOT, BUDGETS, INF
import almost_all_seeds as AS

RUNS = os.path.join(ROOT, 'runs')
NAMED = ['FairBot', 'FB1', 'BTT', 'BTT1', 'PrudentBot', 'P*']


VERDICTS = """
## Verdicts (cost proxy = semantic stabilization, not measured proof length; finite-language, gate-specific)

**Design deviation.** The spec's joint fixed point (free play → costs → gate → re-evaluate, synchronously) does not
converge: it falls into a period-2 cycle at every finite b at both n (except n = 6, b = 8). The pairs that flip are
mutual readers whose gates close and reopen together. The gate was redefined on the bounded trace, world by world:
at world n, x's boxes reading y are open iff k(y)·(1 + last change world of y's atoms toward x before n) ≤ b. Cost
only grows with n, so each gate closes at most once, box truth is monotone, and the trace settles (worlds 7–11) with no
fixed point to select. At the stable world the gate equals the cost of its own trace in every case; soundness holds on
every pair (0 violations); b = ∞ reproduces the free arm exactly.

| # | prediction | outcome |
|---|---|---|
| 1 | FairBot b* = 2, PrudentBot 4, P* 4; below threshold a prover still cooperates with ALLC | **Failed, falsifier fired.** b* = 1 for FairBot, `BOX1(THEM(ME))`, `BOX(THEM(THEM))` (self-cost 1·(1 + 0)); PrudentBot 2; P* 4 (held). 99.45% of n = 8 prover mass has b* = 1; b* is monotone for all 118 provers. Below threshold, 0.94 (b = 1), 0.68 (b = 2, 3), 1.00 (b = 4, 6) of that mass still cooperates with ALLC; PrudentBot and P* below threshold do not. |
| 2 | first drift-closed classes at b = 4; no legible sibling of a self-cooperator at b = 4 | **Failed, falsifier fired:** no drift-closed class (and no H-closed class) at any b at n = 6 or 8. The sibling clause held: no sibling is legible at any finite b ≤ 8 (cost ratio sibling/self ≥ 2). Closure fails through *cheaper* neighbours: P*'s suckerable mates (μ 3.1·10⁻³) are led by `not(BOX(THEM(ME)))` (k = 1), suckered by D. |
| 3 | FairBot exits neutrally at 1/N at every b, odds ∝ N^½; closed classes at b = 4 parochial | **Held** for FairBot: exit slope −1.00, all into ALLC, odds slope 0.43–0.48 at every b. The closed-class clause is vacuous (none). |
| 4 | π at b = 4 → closed prudent family, exit slope < −1.5, P(C,C) ≥ 0.9 at 10⁴, rival ≥ 0.5; b ≥ 8 within 0.05 of free; controls not closing | **Failed, falsifier fired:** at b = 4, n = 8 the top state is FairBot, exit slope −1.00, P(C,C) 0.620 at 10⁴, rival share 0.10. b ≥ 8 within 0.05: held (b = 8 equals free to 4 decimals). Controls: no slope steeper than −1.00 (held literally), but the random gate at b = 1, 3, 4 locks in P* (P(C,C) 0.98–1.00 at 10⁵) by cutting its cheap mates, which the legibility gate never does. |
| 5 | fixed support: π on the smallest closed b, not the largest | **Falsifier not fired; mechanism failed.** No family is closed. Prover π by b at n = 8, N = 10⁵: 0.235 / 0.223 / 0.189 / 0.184, a weak tilt to small b. Under the length penalty b = 1 dominates by prior (0.53 vs 0.07 / 0.01 / 0.002). |
| 6 | lottery: b ≥ 4 equivalent to free; b = 2 lower by 0.1–0.3 at I = 4, 1.00 at I ≥ 64; b = 1 zero | **Partly.** b ≥ 4: held (paired difference 0.00 at every cell). b = 2 lower: **failed** (+0.05 / −0.05 / 0.00 at I = 4). b = 2 at I ≥ 64 = 1.00: held. b = 1 zero: **failed** (0.20 / 0.53 / 0.80 / 1.00 / 1.00). Falsifier not fired. |
| 7 | budget decides closure under mutation; under seeding only via fragmentation near threshold | **Failed in its first half** (no closure, no parochialism); no fragmentation seen at b = 1–3. Falsifier not fired. |
| S1 | b* = 1 / 2 / 4 for FairBot / PrudentBot / P* | **Held** (also under both phases of the cycling iteration). |
| S2 | soundness by construction; no cycle | **Failed, falsifier fired** (cycle); soundness held. |
| S3 | no legible sibling at b ≤ 4; FairBot's sibling legible at b ≥ 8 | First clause **held**; second **failed** (FairBot's sibling costs 15 at b = 8 on the bounded trace, 9 on the free one). |

**Reading.** The gate excludes expensive readers of the resident and keeps cheap ones. Siblings are expensive, so
they are excluded; but the leaks that keep every class open in L_6 and L_8 run through cheap neighbours: ALLC (cost 0)
for FairBot, `BOX(THEM(THEM))` (cost 1) for PrudentBot, `not(BOX(THEM(ME)))` (cost ≤ 2) for P*. A budget can only cut
edges to programs that are costlier than the resident, so it cannot close a class whose suckerable mates are cheaper.
Under mutation the arm is the free arm with the P* block thinned (b ≤ 3 removes it; P(C,C) 0.847 vs 0.814 at
N = 10⁵); under seeding at n = 6 it is the free arm. A realizable prover is not tested here.
"""


def bs(b):
    return 'inf' if b in (None,) or (isinstance(b, float) and not np.isfinite(b)) or str(b) == 'inf' else str(int(float(b))) if b is not None else '-'


def slope(rows, field):
    pts = [(np.log10(r['N']), np.log10(r[field])) for r in rows if r['N'] >= 1000 and r[field] > 0]
    if len(pts) < 2: return float('nan')
    x, y = np.array(pts).T
    return float(np.polyfit(x, y, 1)[0])


def main():
    st = json.load(open(os.path.join(RUNS, 'bounded-provers-static.json')))
    ch = json.load(open(os.path.join(RUNS, 'bounded-provers-chain.json'))) if os.path.exists(os.path.join(RUNS, 'bounded-provers-chain.json')) else []
    lo = json.load(open(os.path.join(RUNS, 'bounded-provers-lottery.json'))) if os.path.exists(os.path.join(RUNS, 'bounded-provers-lottery.json')) else []
    md = ['# A semantic legibility gate (toward bounded provers), 2026-10-04', '',
          'Spec `specs/2026-10-04-bounded-provers.md`; predictions `predictions/2026-10-04-bounded-provers.md`; code `src/bounded*.py`. '
          'The gate is semantic stabilization (essential atoms × settle world), not proof length; all results are finite-language '
          '(n = 6, 8) and specific to this gate. Adopted semantics: the world-indexed (online) gate; the spec\'s synchronous joint '
          'iteration is reported as a diagnostic (it cycles).', '']
    md += VERDICTS.strip().split('\n') + ['']
    summary = dict(static={}, chain=[], lottery={})
    # ---------------- fixed point and soundness
    md += ['## 1. Semantics: joint iteration, online gate, soundness', '',
           '| n | b | joint iteration: rounds / cycle | plays differing, cycle phase vs online | online: worlds | masked share of (k>0, k>0) pairs | final gate = cost of own trace | true open atoms checked | soundness violations | plays differing if the final gate is held fixed from world 0 | classes |',
           '|---|---|---|---|---|---|---|---|---|---|---|']
    for n in ('6', '8'):
        for f in st[n]['fixedpoint']:
            if f['b'] == 'inf-check':
                md.append('| %s | ∞ check | free arm reproduced: plays %s, payoff matrix %s, class names %s | | | | | | | | |' % (n, f['val_equal'], f['U_equal'], f['names_equal']))
                summary['static'].setdefault(n, {})['inf_check'] = f
                continue
            md.append('| %s | %s | %d / %s | %d | %d | %.3f | %s | %d | %d | %d | %d |' % (
                n, bs(f['b']), f['joint_rounds'], 'period 2 from round %d' % f['joint_cycle'][0] if f['joint_cycle'] else 'converged',
                f['joint_play_diff'], f['worlds'], f['masked_rel'], f['gate_consistent'], int(np.sum(f['sound_checked'])),
                int(np.sum(f['sound_bad'])), f['fixed_gate_play_diff'], f['classes']))
    # ---------------- thresholds
    md += ['', '## 2. Thresholds b* (self-cooperation), selective cooperation below threshold', '']
    for n in ('6', '8'):
        T = st[n]['thresholds']
        md.append('- n = %s: %d free provers (self-cooperate, defect on D), μ %.4f. Share of prover mass self-cooperating by b: %s. b* histogram (share of prover mass): %s. Non-monotone in b: %d. Below threshold, share of that mass that still cooperates with ALLC: %s.' % (
            n, T['n_provers'], T['mu_provers'], ', '.join('%s: %.4f' % kv for kv in T['share_selfcoop'].items()),
            ', '.join('%s: %.4f' % kv for kv in sorted(T['bstar_mu_hist'].items())), T['nonmonotone'],
            ', '.join('b=%s: %s (μ %.4f)' % (b, 'none below' if v['frac_coop_ALLC'] is None else '%.2f' % v['frac_coop_ALLC'], v['mu_below']) for b, v in T['below_threshold'].items())))
    md += ['', '| n | b | ' + ' | '.join('%s: self-coop (self-cost), coop ALLC' % x for x in NAMED) + ' |', '|' + '---|' * (2 + len(NAMED))]
    for n in ('6', '8'):
        for b, S in st[n]['static'].items():
            cells = []
            for x in NAMED:
                d = S['named'].get(x)
                cells.append('—' if d is None else '%s (%g), %s' % ('yes' if d['self_coop'] else 'no', d['self_cost'], 'yes' if d['coop_ALLC'] else 'no'))
            md.append('| %s | %s | %s |' % (n, b, ' | '.join(cells)))
    # ---------------- static map
    md += ['', '## 3. Static map: components, drift-closure, universality, legibility', '',
           '| n | b | classes | self-coop classes (μ) | components of G | drift-closed classes (μ) | H-closed (μ) | FairBot old-sense / within-budget universality | PrudentBot old / wb | P* old / wb | legible mass to FairBot / PB / P* |',
           '|---|---|---|---|---|---|---|---|---|---|---|']
    for n in ('6', '8'):
        for b, S in st[n]['static'].items():
            nm = S['named']
            g = lambda x, k: ('%.3f' % nm[x][k]) if x in nm else '—'
            md.append('| %s | %s | %d | %d (%.3f) | %d | %d (%.2g) | %d (%.2g) | %s / %s | %s / %s | %s / %s | %s / %s / %s |' % (
                n, b, S['classes'], S['self_coop_classes'], S['mu_self_coop'], S['n_components'], S['n_closed'], S['mu_closed'],
                S['closure_H']['n_closed'], S['closure_H']['mu_closed'], g('FairBot', 'univ_old'), g('FairBot', 'univ_wb'),
                g('PrudentBot', 'univ_old'), g('PrudentBot', 'univ_wb'), g('P*', 'univ_old'), g('P*', 'univ_wb'),
                g('FairBot', 'legible_mu'), g('PrudentBot', 'legible_mu'), g('P*', 'legible_mu')))
    # ---------------- siblings
    md += ['', '## 4. Siblings beyond n (y = or(x, ψ_K), z = BOX_K(THEM(^D)), built whatever their size)', '',
           '| n | b | provers x (self-coop, defect on D) | sibling legible to x | sibling adjacent to x | adjacent and suckered by z | μ of x with adjacent sibling | min cost(x reads y) / self-cost(x) | FairBot: cost of its sibling | PrudentBot | P* |',
           '|---|---|---|---|---|---|---|---|---|---|---|']
    for n in ('6', '8'):
        for b, S in st[n]['siblings'].items():
            rowd = {r['name']: r for r in S['rows']}
            c = lambda s: ('%g%s' % (rowd[s]['cost_x_reads_y'], ' (legible)' if rowd[s]['legible'] else '')) if s in rowd else '—'
            md.append('| %s | %s | %d | %d | %d | %d | %.2e | %.1f | %s | %s | %s |' % (
                n, b, S['n_x'], S['n_legible'], S['n_adjacent'], S['n_adjacent_suckerable'], S['mu_adjacent'], S['min_cost_ratio'],
                c('BOX(THEM(ME))'), c('and(BOX(THEM(ME)),BOXD1(THEM(^D)))'), c('and(BOX1(THEM(ME)),not(BOX(THEM(ME))))')))
    # ---------------- chain
    if ch:
        md += ['', '## 5. lim_N under rare mutation (ε→0 chain, PD, w = 0.3, eager_poly=False)', '',
               'Exit slope: least-squares slope of log(total exit per mutation event from the top cooperative state) on log N over N = 10³–10⁵ (a fitted slope, not an asymptotic claim). Rival share: 1 − largest block share over cooperative states with π ≥ 10⁻³, ALLC excluded.', '',
               '| arm | n | P(C,C) at N = 10² / 10³ / 10⁴ / 10⁵ | top cooperative state at 10⁵ (π) | top exits at 10⁵: strict / neutral / other | exit slope | rival share at 10³ / 10⁴ / 10⁵ | π(FB, PB, P*) at 10⁵ | classes | terminal / indeterminate / max cut flow |',
               '|---|---|---|---|---|---|---|---|---|---|']
        groups = {}
        for r in ch:
            groups.setdefault((r['kind'], bs(r['b']) if r['b'] is not None else '-', r['n']), []).append(r)
        order = {'global': 0, 'random': 1, 'atom': 2, 'fixed': 3, 'penal': 4, 'clique': 5}
        for (k, b, n), rs in sorted(groups.items(), key=lambda kv: (kv[0][2], order[kv[0][0]], 99 if kv[0][1] in ('inf', '-') else int(kv[0][1]))):
            rs = sorted(rs, key=lambda r: r['N'])
            byN = {r['N']: r for r in rs}
            top = byN.get(100000, rs[-1])
            sl = slope(rs, 'top_exit')
            ent = dict(kind=k, b=b, n=n, pcc={r['N']: r['pcc'] for r in rs}, exit_slope=sl, top=top['top_coop'], pi_top=top['pi_top'],
                       rival={r['N']: r['rival_share'] for r in rs}, fam=top['fam'],
                       exits=dict(strict=top['top_exit_strict'], neutral=top['top_exit_neutral'], other=top['top_exit_other'], dest=top['top_dest']),
                       prover_pi_by_b={r['N']: r.get('prover_pi_by_b') for r in rs}, top_budgets={r['N']: r.get('top_budgets') for r in rs},
                       FB_exit=top.get('FB_exit'), PB_exit=top.get('PB_exit'), Pstar_exit=top.get('Pstar_exit'),
                       blocks=top['blocks'][:3], support=top['support'])
            summary['chain'].append(ent)
            md.append('| %s %s | %d | %s | `%s` (%.3f) | %.1e / %.1e / %.1e | %.2f | %s | %.3f, %.3f, %.3f | %d | %d / %d / %.0e |' % (
                k, b, n, ' / '.join('%.4f' % byN[N]['pcc'] if N in byN else '…' for N in (100, 1000, 10000, 100000)),
                top['top_coop'], top['pi_top'], top['top_exit_strict'], top['top_exit_neutral'], top['top_exit_other'], sl,
                ' / '.join('%.3f' % byN[N]['rival_share'] if N in byN else '…' for N in (1000, 10000, 100000)),
                top['fam']['FB'], top['fam']['PB'], top['fam']['Pstar'], top['n_classes'],
                max(r['n_terminal'] for r in rs), max(r['indeterminate'] for r in rs), max(r['cut_flow'] for r in rs)))
        md += ['', '**Per-program budgets: prover π by budget (μ-weighted within merged classes) and the top state\'s budgets**', '']
        for e in summary['chain']:
            if e['kind'] in ('fixed', 'penal'):
                for N, d in sorted(e['prover_pi_by_b'].items()):
                    if d is None: continue
                    md.append('- %s n=%d N=%d: %s; top state budgets %s' % (e['kind'], e['n'], N, ', '.join('b=%s %.3f' % kv for kv in sorted(d.items())), e['top_budgets'][N]))
        md += ['', '**Support at N = 10⁵ (π ≥ 10⁻³, top 6) and top exit destinations**', '']
        for e in summary['chain']:
            md.append('- %s %s n=%d: %s. Exits: %s' % (e['kind'], e['b'], e['n'], '; '.join('%s %.3f' % tuple(s) for s in e['support'][:6]),
                                                      '; '.join('`%s` (%s) %.1e' % tuple(d) for d in e['exits']['dest'][:3])))
    # ---------------- lottery
    if lo:
        md += ['', '## 6. ε = 0 seeding lottery (n = 6, iid from μ, paired seeds across b)', '',
               'Efficient fraction with Wilson 95% intervals; paired difference against b = ∞ (same seeds) with a bootstrap 95% interval; equivalence margin 0.15. Free-arm reference from "Almost all seeds?" (different seeds): 0.25 / 0.45 / 0.80 at I = 4 (N = 100 / 400 / 1,600); 1.00 at (100, 64) and (100, 256).', '',
               '| arm | cell (N, I, mN) | runs | efficient | defecting | other / unresolved | efficient fraction [95%] | paired diff vs ∞ [95%] | equivalent within 0.15 | median ALLC extinction gen | cooperative-core count at ALLC extinction (median; runs with 0) |',
               '|---|---|---|---|---|---|---|---|---|---|---|']
        import bounded_lottery as BL
        groups = {}
        for r in lo:
            groups.setdefault((r['kind'], bs(r['b']), (r['N'], r['I'], r['mN'])), []).append(r)
        order = {'global': 0, 'random': 1}
        for (k, b, cell), rs in sorted(groups.items(), key=lambda kv: (order[kv[0][0]], 99 if kv[0][1] == 'inf' else int(kv[0][1]), kv[0][2][2] == 0, kv[0][2][1], kv[0][2][0])):
            n = len(rs)
            if cell[2] == 0.0:
                isl = [o for r in rs for o in r['isl_out']]
                ke = sum(o == 'efficient' for o in isl)
                ci = AS.wilson(ke, len(isl))
                md.append('| %s %s | %s | %d | per island: %d / %d | | | per-island %.3f [%.3f, %.3f] | | | | |' % (k, b, cell, n, ke, len(isl), ke / len(isl), ci[0], ci[1]))
                summary['lottery'].setdefault('%s %s' % (k, b), {})[str(cell)] = dict(per_island=ke / len(isl), ci=ci, n_islands=len(isl))
                continue
            ke = sum(r['outcome'] == 'efficient' for r in rs); kd = sum(r['outcome'] == 'defecting' for r in rs)
            ko = n - ke - kd
            ci = AS.wilson(ke, n)
            p = BL.paired(lo, k, int(b) if b != 'inf' else INF, cell) if not (k == 'global' and b == 'inf') else None
            ext = [r['ext_C'] for r in rs if r['ext_C'] >= 0]
            core = [r['core_at_extC'] for r in rs if r['core_at_extC'] is not None]
            md.append('| %s %s | %s | %d | %d | %d | %d | %.2f [%.2f, %.2f] | %s | %s | %s | %s |' % (
                k, b, cell, n, ke, kd, ko, ke / n, ci[0], ci[1],
                '%+.2f [%+.2f, %+.2f] (n=%d)' % (p['diff'], p['lo'], p['hi'], p['n']) if p else '—',
                ('yes' if p['equivalent'] else ('no' if not p['inside_margin'] else 'unresolved')) if p else '—',
                '%d' % np.median(ext) if ext else '—', '%d; %d' % (np.median(core), sum(c == 0 for c in core)) if core else '—'))
            summary['lottery'].setdefault('%s %s' % (k, b), {})[str(cell)] = dict(n=n, eff=ke / n, ci=ci, defect=kd, other=ko, paired=p,
                                                                                  ext_C_median=float(np.median(ext)) if ext else None,
                                                                                  core_zero=sum(c == 0 for c in core) if core else None)
    open(os.path.join(RUNS, 'bounded-provers.md'), 'w').write('\n'.join(md) + '\n')
    summary['static_full'] = {n: dict(thresholds={k: v for k, v in st[n]['thresholds'].items() if k != 'rows'},
                                      static=st[n]['static'], siblings={b: {k: v for k, v in S.items() if k != 'rows'} for b, S in st[n]['siblings'].items()},
                                      fixedpoint=st[n]['fixedpoint']) for n in st}
    json.dump(summary, open(os.path.join(RUNS, 'bounded-provers.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
