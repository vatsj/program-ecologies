"""Report for the symmetric gate: runs/symmetric-gate.md and runs/symmetric-gate.json from
runs/symmetric_gate_rows.json and runs/symmetric_gate_static.json.

    python3 src/symmetric_gate_report.py
"""
import json, math, os, sys
from collections import defaultdict, Counter
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
RULES = ('asym', 'q0.5', 'q0.25', 'sym')


def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'),) * 2
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, c - h), min(1.0, c + h)


def paired(xa, xb):
    """Newcombe (1998, method 10) interval for p_A - p_B on paired binary data; exact McNemar p."""
    xa = np.asarray(xa, int); xb = np.asarray(xb, int); n = len(xa)
    a = int(((xa == 1) & (xb == 1)).sum()); b = int(((xa == 1) & (xb == 0)).sum())
    c = int(((xa == 0) & (xb == 1)).sum()); d = n - a - b - c
    p1 = (a + b) / n; p2 = (a + c) / n
    l1, u1 = wilson(a + b, n); l2, u2 = wilson(a + c, n)
    den = (a + b) * (c + d) * (a + c) * (b + d)
    phi = (a * d - b * c) / math.sqrt(den) if den > 0 else 0.0
    D = p1 - p2
    L = D - math.sqrt(max(0.0, (p1 - l1) ** 2 - 2 * phi * (p1 - l1) * (u2 - p2) + (u2 - p2) ** 2))
    U = D + math.sqrt(max(0.0, (u1 - p1) ** 2 - 2 * phi * (u1 - p1) * (p2 - l2) + (p2 - l2) ** 2))
    m = b + c
    pv = min(1.0, 2 * sum(math.comb(m, i) for i in range(0, min(b, c) + 1)) / 2 ** m) if m > 0 else 1.0
    return dict(diff=D, lo=L, hi=U, only_A=b, only_B=c, mcnemar_p=pv)


def fmt_ci(k, n):
    lo, hi = wilson(k, n)
    return '%d/%d [%.2f, %.2f]' % (k, n, lo, hi)

VERDICTS = """
## Verdicts (scored on the preregistered cells: 20 seeds, N = 6,400; N = 25,600 at 10 seeds; the reps 20–99 extension is exploratory)

| # | prediction | outcome |
|---|---|---|
| RE 1 | symmetric post-scramble growth at 10⁻³ in [0, +0.002]; fringe-to-D intervention reproduces it within 0.002 | **Mostly held; range missed narrowly.** Symmetric +0.0026 (post-scramble, ε = 0 background), −0.0007 at the ε = 10⁻³ equilibrium; asymmetric +0.0101 / +0.0093. The intervention gives +0.00256 / −0.00073, the symmetric values within 10⁻⁴; it explains 100.7% of the gap. Of the residual +0.0026, the linear term is +0.0003; the rest is a transient *legibility shield*: `not(BOXD…)` programs (cooperate unless defection is provable) cooperate with illegible carriers and defect on the legible D. Falsifier (> +0.005) not fired |
| RE 2 | symmetric establishment threshold moves to 0.03–0.1 (f₀ = 0.01 < 0.2; 0.03 in 0.2–0.6; 0.1 ≥ 0.8) | **Failed (falsifier not fired).** Symmetric 1/7/16/20 of 20 at f₀ = 0.003/0.01/0.03/0.1 vs asymmetric 4/7/17/20; threshold 0.014 vs 0.014 at 20 seeds. Exploratory 100 seeds: 0.26 vs 0.38 at 0.01, 0.77 vs 0.89 at 0.03; threshold 0.017 vs 0.013 (finite ε), 0.016 vs 0.009 (twins). The fringe is worth 0.10–0.23 of establishment probability, not a factor of 3 in threshold |
| RE 3 | frozen-background growth monotone in q; q = 0.5 within 0.003 of asym | **Held.** Post-scramble 0.0101 / 0.0091 / 0.0054 / 0.0026 for q = 1 / 0.5 / 0.25 / 0; monotone over a 10-point q grid on the post-scramble and ε backgrounds. Growth is linear in the fringe mass assigned to read (38% at q = 0.25, 87% at q = 0.5), not in q. At the μ background it is non-monotone by ≤ 0.0006 (not scored). Full-run success at f₀ = 0.01 is non-monotone (7, 8, 4, 7; reported, not scored) |
| RE 4 | established runs: carrier–carrier P(C,C) 1.00, population ≥ 0.9, no collapse | **Held.** Every established run (all rules, N = 6,400 and 25,600, extension included) has carrier-conditional P(C,C) 1.000 and population P(C,C) 0.985–0.993; no run that reached 50% carriers failed to establish |
| RE 5 | lottery (100, 64): symmetric k = 1 falls to 0.3–0.7; k = 3 ≥ 0.8 | **Failed, falsifier fired.** Symmetric k = 1 is 39/40 (asymmetric 37/40, reproducing the published cell); k = 3 is 40/40 under every rule |
| S1 | only non-carrier → non-constant-carrier entries change at b = 0 | **Failed narrowly:** the block is right (0 changes elsewhere), but 1,352 entries against constant-source carriers holding a non-constant contract also change |
| S2 | b = ∞ tables not exactly equal; differences confined to non-carrier readers; mass < 0.01 | **Partly:** not equal (held), mass 0.0006 (held), but 47,372 carrier → non-carrier entries change too (carriers read the non-carriers' changed play). Population P(C,C) differs by +0.011 (sd 0.039) over 20 paired b = ∞ runs |
| S3 | static: sym growth in [0, 0.002]; sym μ growth below −0.006; intervention ≥ 80% of the gap; q linear in fringe mass | **Mostly held:** range missed as RE 1; −0.0127 at μ; 100.7%; linear in fringe mass to 4·10⁻⁵ |
| S4 | finite-ε success ranges; paired asym − sym at 0.01 positive, interval excluding 0 | **Partly:** all eight ranges held; the paired clause failed at 20 seeds (0.00 [−0.19, +0.19]) and holds in the exploratory extension (+0.12 [+0.03, +0.21]) |
| S5 | symmetric N = 25,600 above its N = 6,400 point, below asymmetric | **Partly:** 5/10 vs 0.35 (held); asymmetric also 5/10 (failed) |
| S6 | symmetric twins 0.2–0.5 at 0.01, ≥ 0.9 at 0.1 | **Partly:** 12/20 = 0.60 (failed); 20/20 (held). At 100 seeds 0.32 |
| S7 | symmetric lottery k = 1 in 0.5–0.85; k = 3 ≥ 0.9 | **Partly:** 0.975 (failed high); 1.00 (held) |
| S8 | D and non-carrier FairBot never fix; ALLC ≤ 5/100 | **Held** under every rule: D and FairBot lineages extinct 100/100; ALLC never fixes, persists neutrally in 17/100 at the freeze (mean share 0.009 ≈ 1/N) |
"""


def main():
    rows = json.load(open(os.path.join(RUNS, 'symmetric_gate_rows.json')))
    st = json.load(open(os.path.join(RUNS, 'symmetric_gate_static.json')))
    by = defaultdict(list)
    for r in rows:
        by[r['set']].append(r)
    out = dict(static=st, cells={})
    L = []
    L.append('# Symmetric gate: runs (spec `specs/2026-10-05-symmetric-gate.md`, predictions `predictions/2026-10-05-symmetric-gate.md`)\n')
    L.append('Generated by `src/symmetric_gate_report.py` from `runs/symmetric_gate_rows.json` and `runs/symmetric_gate_static.json`. '
             'Finite sizes; finite-ε cells are approach/establishment results, not π.\n')
    # ------------------------------------------------------------------ static
    L.append('## Static diagnostics (b = 0, identical frozen backgrounds)\n')
    L.append('Changed entries against the asymmetric table: ' + json.dumps(st['changed_entries']) + '\n')
    L.append('b = ∞ baseline: ' + json.dumps(st['b_inf_baseline']) + '\n')
    L.append('Backgrounds: ' + json.dumps(st['backgrounds']) + '; ALLC < 10⁻³ at generation %d.\n' % st['allc_below_1e-3_gen'])
    L.append('### Block tables (mix carrier group vs background; actions are P(C) of the row side)\n')
    L.append('| background | rule | cc action | cc pay | car→bg action | car pay vs bg | bg→car action | bg pay vs car | bg–bg pay | D pay vs car |')
    L.append('|---|---|---|---|---|---|---|---|---|---|')
    for bg, d in st['blocks'].items():
        for r, b in d.items():
            L.append('| %s | %s | %.3f | %.3f | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f |' % (
                bg, r, b['cc_action'], b['cc_pay'], b['car_to_bg_action'], b['car_vs_bg_pay'], b['bg_to_car_action'], b['bg_vs_car_pay'],
                b['bg_bg_pay'], b['D_vs_car_pay']))
    L.append('\n### Rare-carrier growth per generation at f = 10⁻³ (mix group; net of contract stripping at ε = 10⁻³ on the ε background)\n')
    keys = list(next(iter(st['growth'].values())).keys())
    L.append('| rule / intervention | ' + ' | '.join(st['growth'].keys()) + ' | f* (net) per background |')
    L.append('|---|' + '---|' * len(st['growth']) + '---|')
    for r in keys:
        L.append('| %s | %s | %s |' % (r, ' | '.join('%+.5f' % st['growth'][bg][r]['mix']['net'] for bg in st['growth']),
                                      ', '.join(str(st['fstar'][bg][r]['fstar_net']) for bg in st['growth'])))
    L.append('\nFringe: ' + json.dumps(st['fringe']) + '\n')
    L.append('q coverage of fringe mass: ' + json.dumps(st['q_fringe_coverage']) + '\n')
    L.append('Deterministic flow thresholds (smallest f₀ ending > 50% carriers in 4,000 generations): ' +
             json.dumps({k: v['threshold'] for k, v in st['deterministic_flow'].items()}) + '\n')
    # ------------------------------------------------------------------ finite eps
    def cellrows(s, **kw):
        return [r for r in by[s] if all(r.get(k) == v for k, v in kw.items())]
    for s, title, Ns in (('main', 'Finite ε (10⁻³), N = 6,400, 2·10⁴ generations, window = second half', (6400,)),
                         ('n25600', 'Finite ε, N = 25,600, f₀ = 0.01', (25600,)),
                         ('inf_pair', 'b = ∞ pair (added: the b = ∞ tables are not exactly equal), f₀ = 0.01', (6400,))):
        if not by[s]: continue
        L.append('\n## %s\n' % title)
        L.append('| f₀ | rule | established | extinct | censored | median ext gen | median t50 | P(C,C) est. (min–max) | carrier-cond. P(C,C) | carriers (est.) | top sources (est., pooled) |')
        L.append('|---|---|---|---|---|---|---|---|---|---|---|')
        f0s = sorted(set(r['f0'] for r in by[s]))
        for f0 in f0s:
            for rule in RULES:
                rr = sorted(cellrows(s, f0=f0, rule=rule), key=lambda r: r['rep'])
                if not rr: continue
                n = len(rr); e = [r for r in rr if r['established']]
                x = sum(r['extinct'] for r in rr); c = sum(r['censored'] for r in rr)
                eg = [r['carrier_ext_gen'] for r in rr if r['extinct']]
                t5 = [r['t50'] for r in e if r['t50']]
                pc = [r['pcc'] for r in e]; ccp = [r['carrier_pcc'] for r in e if r['carrier_pcc'] is not None]
                src = Counter()
                for r in e:
                    for nm_, v in r['top_sources']: src[nm_] += v / max(len(e), 1)
                cell = dict(n=n, established=len(e), extinct=x, censored=c, wilson=wilson(len(e), n),
                            med_ext=float(np.median(eg)) if eg else None, med_t50=float(np.median(t5)) if t5 else None,
                            pcc_mean=float(np.mean(pc)) if pc else None, pcc_min=float(min(pc)) if pc else None,
                            pcc_max=float(max(pc)) if pc else None, carrier_pcc_min=float(min(ccp)) if ccp else None,
                            carriers=float(np.mean([r['carrier'] for r in e])) if e else None,
                            top_sources=src.most_common(5), whole_run_established=sum(r['run50_whole'] >= 1000 for r in rr),
                            established_reps=[r['rep'] for r in e])
                out['cells']['%s|%g|%s' % (s, f0, rule)] = cell
                L.append('| %g | %s | %s | %d | %d | %s | %s | %s | %s | %s | %s |' % (
                    f0, rule, fmt_ci(len(e), n), x, c, cell['med_ext'], cell['med_t50'],
                    ('%.3f (%.3f–%.3f)' % (cell['pcc_mean'], cell['pcc_min'], cell['pcc_max'])) if pc else '—',
                    ('≥ %.3f' % cell['carrier_pcc_min']) if ccp else '—', ('%.2f' % cell['carriers']) if e else '—',
                    ', '.join('%s %.2f' % (a, b) for a, b in cell['top_sources'][:4])))
        # paired differences
        L.append('\nPaired differences in establishment (Newcombe interval, exact McNemar p; A − B over identical populations):\n')
        L.append('| f₀ | A − B | diff [95%] | A only / B only | McNemar p |')
        L.append('|---|---|---|---|---|')
        for f0 in f0s:
            for A_, B_ in (('asym', 'sym'), ('asym', 'q0.5'), ('q0.5', 'q0.25'), ('q0.25', 'sym')):
                ra = {r['rep']: r for r in cellrows(s, f0=f0, rule=A_)}; rb = {r['rep']: r for r in cellrows(s, f0=f0, rule=B_)}
                reps = sorted(set(ra) & set(rb))
                if not reps: continue
                pdf = paired([ra[k]['established'] for k in reps], [rb[k]['established'] for k in reps])
                out['cells']['%s|%g|%s-%s' % (s, f0, A_, B_)] = pdf
                L.append('| %g | %s − %s | %+.2f [%+.2f, %+.2f] | %d / %d | %.3f |' % (f0, A_, B_, pdf['diff'], pdf['lo'], pdf['hi'],
                                                                                    pdf['only_A'], pdf['only_B'], pdf['mcnemar_p']))
    # ------------------------------------------------------------------ pooled paired differences over f0
    L.append('\nPooled over f₀ ∈ {0.003, 0.01, 0.03} (paired by (f₀, rep)):\n')
    L.append('| set | A − B | diff [95%] | A only / B only | McNemar p |')
    L.append('|---|---|---|---|---|')
    for s, okf in (('main', lambda r: r['established']), ('twins', lambda r: r['outcome'] == 'efficient')):
        for A_, B_ in (('asym', 'sym'), ('asym', 'q0.5'), ('asym', 'q0.25')):
            ra = {(r['f0'], r['rep']): r for r in by[s] if r['rule'] == A_ and r['f0'] < 0.05}
            rb = {(r['f0'], r['rep']): r for r in by[s] if r['rule'] == B_ and r['f0'] < 0.05}
            reps = sorted(set(ra) & set(rb))
            if not reps: continue
            pdf = paired([okf(ra[k]) for k in reps], [okf(rb[k]) for k in reps])
            out['cells']['%s|pooled|%s-%s' % (s, A_, B_)] = pdf
            L.append('| %s | %s − %s | %+.3f [%+.3f, %+.3f] | %d / %d | %.3f |' % (s, A_, B_, pdf['diff'], pdf['lo'], pdf['hi'],
                                                                                 pdf['only_A'], pdf['only_B'], pdf['mcnemar_p']))
    # early survival (all runs, unconditional), main set
    L.append('\nCarrier survival and mean carrier count (unconditional) in the main set, by generation:\n')
    L.append('| f₀ | rule | alive at 25 / 50 / 100 / 200 | mean count at 25 / 100 / 200 (initial) |')
    L.append('|---|---|---|---|')
    for f0 in sorted(set(r['f0'] for r in by['main'])):
        for rule in RULES:
            rr = [r for r in by['main'] if r['f0'] == f0 and r['rule'] == rule]
            if not rr: continue
            def at(r, g):
                tr = r["carrier_traj_fine"]; i = g // 5
                return tr[i] if i < len(tr) else 0
            al = [sum(at(r, g) > 0 for r in rr) for g in (25, 50, 100, 200)]
            mc = [np.mean([at(r, g) for r in rr]) for g in (25, 100, 200)]
            L.append('| %g | %s | %s | %s (%d) |' % (f0, rule, ' / '.join(map(str, al)), ' / '.join('%.0f' % v for v in mc), rr[0]['k0']))
    # ------------------------------------------------------------------ twins
    if by['twins']:
        L.append('\n## ε = 0 twins (same populations, run to the freeze, horizon 10⁵)\n')
        L.append('| f₀ | rule | efficient | extinct carriers | censored (unresolved) | median stop gen | carriers at stop (efficient runs) |')
        L.append('|---|---|---|---|---|---|---|')
        for f0 in sorted(set(r['f0'] for r in by['twins'])):
            for rule in RULES:
                rr = cellrows('twins', f0=f0, rule=rule)
                if not rr: continue
                n = len(rr); ef = [r for r in rr if r['outcome'] == 'efficient']
                cell = dict(n=n, efficient=len(ef), extinct=sum(r['extinct'] for r in rr), censored=sum(r['status'] == 'unresolved' for r in rr),
                            med_stop=float(np.median([r['stop_gen'] for r in rr])),
                            carriers_eff=float(np.mean([r['final_carrier'] for r in ef])) if ef else None,
                            efficient_reps=sorted(r['rep'] for r in ef))
                out['cells']['twins|%g|%s' % (f0, rule)] = cell
                L.append('| %g | %s | %s | %d | %d | %.0f | %s |' % (f0, rule, fmt_ci(len(ef), n), cell['extinct'], cell['censored'],
                                                                     cell['med_stop'], ('%.2f' % cell['carriers_eff']) if ef else '—'))
        L.append('\n| f₀ | A − B | diff [95%] | A only / B only | McNemar p |')
        L.append('|---|---|---|---|---|')
        for f0 in sorted(set(r['f0'] for r in by['twins'])):
            for A_, B_ in (('asym', 'sym'), ('asym', 'q0.5'), ('q0.5', 'q0.25'), ('q0.25', 'sym')):
                ra = {r['rep']: r for r in cellrows('twins', f0=f0, rule=A_)}; rb = {r['rep']: r for r in cellrows('twins', f0=f0, rule=B_)}
                reps = sorted(set(ra) & set(rb))
                if not reps: continue
                pdf = paired([ra[k]['outcome'] == 'efficient' for k in reps], [rb[k]['outcome'] == 'efficient' for k in reps])
                out['cells']['twins|%g|%s-%s' % (f0, A_, B_)] = pdf
                L.append('| %g | %s − %s | %+.2f [%+.2f, %+.2f] | %d / %d | %.3f |' % (f0, A_, B_, pdf['diff'], pdf['lo'], pdf['hi'],
                                                                                    pdf['only_A'], pdf['only_B'], pdf['mcnemar_p']))
    # ------------------------------------------------------------------ lottery
    if by['lottery']:
        L.append('\n## Lottery (100, 64), ε = 0, mN = 1, b = 0, σ = 0\n')
        L.append('| k | rule | efficient | defecting | other | unresolved | median stop gen |')
        L.append('|---|---|---|---|---|---|---|')
        for k in (1, 3):
            for rule in RULES:
                rr = cellrows('lottery', k=k, rule=rule)
                if not rr: continue
                oc = Counter(r['outcome'] for r in rr)
                cell = dict(n=len(rr), outcomes=dict(oc), med_stop=float(np.median([r['stop_gen'] for r in rr])))
                out['cells']['lottery|%d|%s' % (k, rule)] = cell
                L.append('| %d | %s | %s | %d | %d | %d | %.0f |' % (k, rule, fmt_ci(oc['efficient'], len(rr)), oc['defecting'], oc['other'],
                                                                    oc['unresolved'], cell['med_stop']))
            ra = {r['rep']: r for r in cellrows('lottery', k=k, rule='asym')}; rb = {r['rep']: r for r in cellrows('lottery', k=k, rule='sym')}
            reps = sorted(set(ra) & set(rb))
            if reps:
                pdf = paired([ra[q]['outcome'] == 'efficient' for q in reps], [rb[q]['outcome'] == 'efficient' for q in reps])
                out['cells']['lottery|%d|asym-sym' % k] = pdf
                L.append('| %d | asym − sym | %+.2f [%+.2f, %+.2f] (McNemar p %.3f) | | | | |' % (k, pdf['diff'], pdf['lo'], pdf['hi'], pdf['mcnemar_p']))
    # ------------------------------------------------------------------ challenge
    if by['challenge']:
        L.append('\n## Pure-carrier invasion challenge (N = 100, ε = 0; 99 carriers drawn from the establishers ∝ μ + 1 invader)\n')
        L.append('| invader | rule | invader lineage fixed | invader lineage extinct | present at freeze | mean invader share at stop | mean P(C,C) at stop | efficient | median stop gen |')
        L.append('|---|---|---|---|---|---|---|---|---|')
        for inv in ('none', 'D', 'ALLC', 'FB_nc'):
            for rule in RULES:
                rr = [r for r in by['challenge'] if r['invader'] == inv and r['rule'] == rule]
                if not rr: continue
                if inv == 'none':
                    fx = ex = 0; oth = 0
                else:
                    fx = sum(r['invader_share'] >= 1.0 for r in rr); ex = sum(r['invader_share'] == 0.0 for r in rr); oth = len(rr) - fx - ex
                msh = float(np.mean([r['invader_share'] for r in rr])) if inv != 'none' else None
                cell = dict(n=len(rr), fixed=fx, extinct=ex, other=oth, mean_share=msh, pcc=float(np.mean([r['pcc'] for r in rr])),
                            efficient=sum(r['outcome'] == 'efficient' for r in rr), med_stop=float(np.median([r['stop_gen'] for r in rr])))
                out['cells']['challenge|%s|%s' % (inv, rule)] = cell
                L.append('| %s | %s | %s | %d | %d | %s | %.3f | %d | %.0f |' % (inv, rule, fmt_ci(fx, len(rr)) if inv != 'none' else '—', ex, oth,
                                                                           ('%.4f' % msh) if msh is not None else '—', cell['pcc'], cell['efficient'], cell['med_stop']))
    # ------------------------------------------------------------------ inf pair: P(C,C) over all runs
    if by['inf_pair']:
        L.append('\n## b = ∞ pair, population P(C,C) over all runs (finite ε, f₀ = 0.01, 20 seeds)\n')
        L.append('| rule | mean P(C,C) (min–max) | carriers established | mean carrier share (2nd half) |')
        L.append('|---|---|---|---|')
        pp = {}
        for rule in ('asym', 'sym'):
            rr = sorted([r for r in by['inf_pair'] if r['rule'] == rule], key=lambda r: r['rep'])
            pc = [r['pcc'] for r in rr]; pp[rule] = pc
            L.append('| %s | %.4f (%.4f–%.4f) | %d/%d | %.3f |' % (rule, np.mean(pc), min(pc), max(pc), sum(r['established'] for r in rr), len(rr),
                                                                    np.mean([r['carrier'] for r in rr])))
        dd = np.array(pp['asym']) - np.array(pp['sym'])
        out['cells']['inf_pair|pcc_diff'] = dict(mean=float(dd.mean()), sd=float(dd.std(ddof=1)), n=len(dd))
        L.append('\nPaired P(C,C) difference asym − sym: %+.4f (sd %.4f, n %d).\n' % (dd.mean(), dd.std(ddof=1), len(dd)))
    # ------------------------------------------------------------------ post-hoc extension (exploratory)
    if by['main_ext'] or by['twins_ext']:
        L.append('\n## Post-hoc power extension (exploratory; addendum 2): asymmetric vs symmetric, reps 0–99\n')
        L.append('| set | f₀ | asym | sym | asym − sym [95%] | asym only / sym only | McNemar p |')
        L.append('|---|---|---|---|---|---|---|')
        for s0, okf in (('main', lambda r: r['established']), ('twins', lambda r: r['outcome'] == 'efficient')):
            allr = by[s0] + by[s0 + '_ext']
            for f0 in (0.003, 0.01, 0.03, 'pooled'):
                sel = [r for r in allr if (f0 == 'pooled' and r['f0'] < 0.05) or r['f0'] == f0]
                ra = {(r['f0'], r['rep']): r for r in sel if r['rule'] == 'asym'}; rb = {(r['f0'], r['rep']): r for r in sel if r['rule'] == 'sym'}
                reps = sorted(set(ra) & set(rb))
                if not reps: continue
                xa = [okf(ra[k]) for k in reps]; xb = [okf(rb[k]) for k in reps]
                pdf = paired(xa, xb)
                out['cells']['ext|%s|%s' % (s0, f0)] = dict(pdf, n=len(reps), asym=sum(xa), sym=sum(xb))
                L.append('| %s | %s | %s | %s | %+.3f [%+.3f, %+.3f] | %d / %d | %.3f |' % (s0, f0, fmt_ci(sum(xa), len(reps)), fmt_ci(sum(xb), len(reps)),
                                                                                       pdf['diff'], pdf['lo'], pdf['hi'], pdf['only_A'], pdf['only_B'], pdf['mcnemar_p']))
    # ------------------------------------------------------------------ establishment thresholds (log interpolation)
    def thr(pts):
        pts = sorted(pts)
        for (f1, p1), (f2, p2) in zip(pts, pts[1:]):
            if p1 < 0.5 <= p2:
                return float(math.exp(math.log(f1) + (0.5 - p1) / (p2 - p1) * (math.log(f2) - math.log(f1))))
        return None
    L.append('\n## Establishment thresholds (seed frequency at success 0.5, log-interpolated)\n')
    L.append('| object | asym | q0.5 | q0.25 | sym |')
    L.append('|---|---|---|---|---|')
    for s0, okf in (('main', lambda r: r['established']), ('twins', lambda r: r['outcome'] == 'efficient')):
        row = []
        for rule in RULES:
            pts = []
            for f0 in (0.003, 0.01, 0.03, 0.1):
                rr = [r for r in by[s0] if r['rule'] == rule and r['f0'] == f0]
                if rr: pts.append((f0, sum(okf(r) for r in rr) / len(rr)))
            row.append(thr(pts))
        out['cells']['threshold|%s|20seeds' % s0] = dict(zip(RULES, row))
        L.append('| %s, 20 seeds | %s |' % (s0, ' | '.join(('%.4f' % v) if v else '—' for v in row)))
        if by[s0 + '_ext']:
            row = []
            for rule in ('asym', 'sym'):
                pts = []
                for f0 in (0.003, 0.01, 0.03, 0.1):
                    rr = [r for r in by[s0] + by[s0 + '_ext'] if r['rule'] == rule and r['f0'] == f0]
                    if rr: pts.append((f0, sum(okf(r) for r in rr) / len(rr)))
                row.append(thr(pts))
            out['cells']['threshold|%s|100seeds' % s0] = dict(zip(('asym', 'sym'), row))
            L.append('| %s, 100 seeds at f₀ ≤ 0.03 (exploratory) | %.4f | | | %.4f |' % (s0, row[0], row[1]))
    L.append(VERDICTS)
    open(os.path.join(RUNS, 'symmetric-gate.md'), 'w').write('\n'.join(L) + '\n')
    json.dump(out, open(os.path.join(RUNS, 'symmetric-gate.json'), 'w'), indent=1, default=float)
    print('\n'.join(L))


if __name__ == '__main__':
    main()
