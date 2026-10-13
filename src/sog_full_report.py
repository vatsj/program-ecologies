"""Report for the social organization game, fully realizable (notes/sog-fully-realizable.md): aggregates the cell
outputs (runs/sog_full/cell_*/rep_*.json), the static tables and the assays into runs/sog-fully-realizable.json and
runs/sog-fully-realizable.md, with run-level uncertainty and paired contrasts.

  python3 src/sog_full_report.py
"""
import os
import sys
import json
import math
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RUNS = os.path.join(ROOT, 'runs')
OUT = os.path.join(RUNS, 'sog_full')
B = 2000


def wilson(k, n, z=1.96):
    if n == 0: return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def boot(x, rng, f=np.mean):
    x = np.asarray(x, float)
    if len(x) == 0: return (None, None)
    bs = [f(x[rng.integers(0, len(x), len(x))]) for _ in range(B)]
    return (float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975)))


def mcnemar(a, b):
    """Exact two-sided McNemar p for paired binary outcomes."""
    n01 = sum(1 for x, y in zip(a, b) if x and not y)
    n10 = sum(1 for x, y in zip(a, b) if y and not x)
    n = n01 + n10
    if n == 0: return 1.0
    k = min(n01, n10)
    p = sum(math.comb(n, i) for i in range(0, k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def load_cell(name):
    d = os.path.join(OUT, 'cell_' + name)
    if not os.path.isdir(d): return []
    out = []
    for f in sorted(os.listdir(d)):
        if f.startswith('rep_') and f.endswith('.json'):
            out.append(json.load(open(os.path.join(d, f))))
    return out


def cell_stats(name, reps, rng):
    if not reps: return None
    S = [r['summary'] for r in reps]
    n = len(S)
    est = [s['established'] for s in S]
    eg = [s['est_gen'] for s in S if s['est_gen'] is not None]
    pers = [s['h']['persistence'] for s in S]
    wages = np.array([s['h']['wage'] for s in S])
    prod = [s['h']['prodeff'] for s in S]
    out = dict(n=n, established=sum(est), established_ci=wilson(sum(est), n),
               est_gen_median=float(np.median(eg)) if eg else None, est_gen_by_200=sum(1 for g in eg if g <= 200),
               established_window=sum(1 for s in S if s.get('established_window')),
               est_gen_window_median=float(np.median([s['est_gen_window'] for s in S if s.get('est_gen_window') is not None]))
               if any(s.get('est_gen_window') is not None for s in S) else None,
               fair_at_founding=float(np.mean([s.get('fair_at_founding', 0) for s in S])),
               persistence=float(np.mean(pers)), persistence_ci=boot(pers, rng),
               persistence_runs_ge_half=sum(1 for p in pers if p >= 0.5), persistence_runs_zero=sum(1 for p in pers if p == 0),
               wage_shares=wages.mean(0).tolist(), zero_wage=float(wages[:, 0].mean()), zero_wage_ci=boot(wages[:, 0], rng),
               quarter_wage=float(wages[:, 1].mean()),
               plurality={w: int(sum(1 for row in wages if int(np.argmax(row)) == k)) for k, w in enumerate(('0', '1/4', '1/2'))},
               prodeff=float(np.mean(prod)), prodeff_ci=boot(prod, rng),
               strike_any=float(np.mean([s['h']['strike_any'] for s in S])))
    ext = [r.get('summary_ext') for r in reps if r.get('summary_ext')]
    if ext:
        pe = [e['end']['persistence'] for e in ext]
        out['ext'] = dict(n=len(ext), gen=ext[0]['end']['gen'], persistence=float(np.mean(pe)), persistence_ci=boot(pe, rng),
                          zero_wage=float(np.mean([e['end']['wage'][0] for e in ext])),
                          prodeff=float(np.mean([e['end']['prodeff'] for e in ext])))
    # holders
    H = defaultdict(int); HD = defaultdict(int); GB = defaultdict(int)
    for s in S:
        for k, v in s.get('holders', {}).items(): H[k] += v
        for k, v in s.get('holders_detail', {}).items(): HD[k] += v
        for k, v in s.get('greenbeard_bosses', {}).items(): GB[k] += v
    tot = sum(H.values())
    out['holders'] = {k: v / tot for k, v in H.items()} if tot else {}
    out['holders_detail'] = {k: v / tot for k, v in HD.items()} if tot else {}
    out['fair_islands_counted'] = tot
    out['greenbeard_share'] = (H.get('greenbeard union', 0) + 0.5 * H.get('mixture', 0)) / tot if tot else 0.0
    out['greenbeard_identity_share'] = (HD.get('greenbeard union (identity)', 0) + 0.5 * HD.get('mixture (identity)', 0)) / tot if tot else 0.0
    out['greenbeard_bosses'] = dict(GB)
    hs = defaultdict(int)
    for s in S:
        for k, v in s.get('holder_spellings', {}).items(): hs[k] += v
    out['holder_spellings_top'] = dict(sorted(hs.items(), key=lambda z: -z[1])[:8])
    out['closed_shop_share'] = float(np.mean([s.get('closed_shop_share', 0.0) for s in S]))
    ii = [s['identity_islands'] for s in S if s.get('identity_islands') is not None]
    out['identity_islands'] = float(np.mean(ii)) if ii else None
    BI = defaultdict(int); BT = defaultdict(int)
    for s in S:
        for k, v in s.get('beq_invasion', {}).items(): BI[k] += v
        for k, v in s.get('beq_invasion_T1T1', {}).items(): BT[k] += v
    out['beq_invasion'] = dict(BI); out['beq_invasion_T1T1'] = dict(BT)
    EX = defaultdict(int)
    for s in S:
        for k, v in s.get('exits', {}).items(): EX[k] += v
    ne = sum(EX.values())
    out['exits'] = {k: v / ne for k, v in sorted(EX.items(), key=lambda z: -z[1])} if ne else {}
    out['exits_n'] = ne
    out['cross_fair'] = float(np.mean([s['cross_fair'] for s in S]))
    uc = [s['union_compat'] for s in S if s.get('union_compat') is not None]
    out['union_compat'] = float(np.mean(uc)) if uc else None
    # encounters: timeouts and costs by period; production outcomes; failures by required-cost decile
    enc = {}
    allrows = []
    for g in ('0', '50', '200', '2000'):
        es = [s['encounters'][g] for s in S if g in s['encounters']]
        if not es: continue
        oc = defaultdict(int)
        for e in es:
            for row in e['rows']:
                for o in row[3]: oc[o] += 1
                allrows.append(row)
        no = sum(oc.values())
        enc[g] = dict(todiff=float(np.mean([e['todiff'] for e in es])), play_median=float(np.median([e['play_median'] for e in es])),
                      prod_median=float(np.median([e['prod_median'] for e in es])),
                      total_median=float(np.median([e['total_median'] for e in es])),
                      production_outcomes={k: v / no for k, v in oc.items()} if no else {})
    out['encounters'] = enc
    if allrows:
        req = np.array([r[2] for r in allrows], float)
        play = np.array([r[0] for r in allrows], float); prd = np.array([r[1] for r in allrows], float)
        fail = np.array([sum(1 for o in r[3] if o in ('capTO', 'fuelTO')) for r in allrows], float)
        att = np.array([sum(1 for o in r[3] if o not in ('refused',)) for r in allrows], float)
        q = np.quantile(req, np.linspace(0, 1, 11))
        dec = np.clip(np.searchsorted(q[1:-1], req, side='right'), 0, 9)
        out['failures_by_cost_decile'] = [dict(decile=k + 1, failures=float(fail[dec == k].sum()), attempts=float(att[dec == k].sum()),
                                               share_of_failures=float(fail[dec == k].sum() / max(fail.sum(), 1)))
                                          for k in range(10)]
        out['realized_cost'] = dict(median_play=float(np.median(play)), median_play_plus_prod=float(np.median(play + prd)),
                                    ratio=float(np.median(play + prd) / max(np.median(play), 1)),
                                    mean_play=float(play.mean()), mean_prod=float(prd.mean()),
                                    frac_encounter_with_attempt=float((att > 0).mean()),
                                    failures=float(fail.sum()), attempts=float(att.sum()))
    # production counters (non-quiet islands only; notes §1.13 item 4)
    C = np.array([s['ctr'][:19] for s in S], float).sum(0)
    names = ['encounters', 'boss_attempts', 'boss_found', 'boss_none', 'boss_capTO', 'boss_starved', 'worker_attempts',
             'worker_found', 'worker_none', 'worker_capTO', 'worker_starved', 'gate_refusals', 'boss_replacements',
             'worker_replacements', 'quiet_checks', 'migrations', 'moran_events', 'boss_prod_steps', 'worker_prod_steps']
    out['counters'] = {nm: float(v) for nm, v in zip(names, C)}
    sp = [s['spo_held'] for s in S if 'spo_held' in s]
    if sp:
        out['spo_held'] = dict(individuals=sum(x['individuals'] for x in sp), of=sum(x['of'] for x in sp))
    out['time_s'] = dict(mean=float(np.mean([sum(r['time'].values()) for r in reps])))
    return out


def paired(a_reps, b_reps, key, rng):
    """Paired contrast b - a on persistence (per replicate)."""
    A = {r['rep']: r['summary'] for r in a_reps}; Bm = {r['rep']: r['summary'] for r in b_reps}
    common = sorted(set(A) & set(Bm))
    if not common: return None
    d = [Bm[k]['h'][key] - A[k]['h'][key] for k in common]
    ea = [A[k]['established'] for k in common]; eb = [Bm[k]['established'] for k in common]
    return dict(n=len(common), mean_diff=float(np.mean(d)), ci=boot(d, rng), established_mcnemar_p=mcnemar(ea, eb),
                a_mean=float(np.mean([A[k]['h'][key] for k in common])), b_mean=float(np.mean([Bm[k]['h'][key] for k in common])))


CELLS = ['H_noeq', 'H_eq', 'H_sham', 'H_eqnoT', 'H_noeq_ideal', 'S_noeq', 'S_eq', 'S_sham', 'S_opp', 'S_eq_N200',
         'S_eq_forced_empty', 'S_eq_forced_pre']
PAIRS = [('H_noeq', 'H_eq'), ('H_sham', 'H_eq'), ('H_eqnoT', 'H_eq'), ('S_noeq', 'S_eq'), ('S_sham', 'S_eq'),
         ('H_eq', 'S_eq'), ('H_noeq', 'H_noeq_ideal'), ('S_eq', 'S_opp'), ('S_eq_forced_empty', 'S_eq_forced_pre'),
         ('H_noeq', 'S_noeq')]


def fmt(x, d=3):
    if x is None: return '–'
    if isinstance(x, (tuple, list)) and len(x) == 2:
        if x[0] is None: return '–'
        return '[%s, %s]' % (fmt(x[0], 2), fmt(x[1], 2))
    if isinstance(x, float): return ('%.' + str(d) + 'f') % x
    return str(x)


def main():
    rng = np.random.default_rng(20261013)
    cells = {}
    raw = {}
    for c in CELLS:
        reps = load_cell(c)
        raw[c] = reps
        st = cell_stats(c, reps, rng)
        if st: cells[c] = st
    pairs = {}
    for a, b in PAIRS:
        if raw.get(a) and raw.get(b):
            pairs['%s -> %s' % (a, b)] = paired(raw[a], raw[b], 'persistence', rng)
    out = dict(cells=cells, pairs=pairs)
    for nm in ('sog-full-static.json', 'sog-full-validate.json'):
        f = os.path.join(RUNS, nm)
        if os.path.exists(f): out[nm.replace('.json', '')] = json.load(open(f))
    for nm in ('assay_isolated', 'assay_entrant', 'assay_local'):
        f = os.path.join(OUT, nm + '.json')
        if os.path.exists(f):
            d = json.load(open(f))
            if nm in ('assay_isolated', 'assay_entrant'):
                d = {k: {kk: vv for kk, vv in v.items() if kk != 'rows'} for k, v in d.items()}
            out[nm] = d
    json.dump(out, open(os.path.join(RUNS, 'sog-fully-realizable.json'), 'w'), indent=1, default=str)
    # markdown tables
    L = ['# The social organization game, fully realizable: run report', '',
         'Generated by `src/sog_full_report.py` from `runs/sog_full/`. Lottery: (N, I) = (100, 64) unless stated, mN = 1, '
         'w = 0.3, horizon 2,000 (the 10,000 extension a separate column), 40 runs per main cell; ε = 0 evidence at finite '
         '(N, I, horizon). Intervals: Wilson (runs), bootstrap over runs (island fractions).', '',
         '## Cells', '',
         '| cell | runs | established (first fair check) | median est. gen | established (10-check window) | median window end | persistence (2,000) | runs ≥ ½ / = 0 | zero wage | ¼ wage | plurality 0/¼/½ | prod. eff. | persistence (10,000) |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for c in CELLS:
        s = cells.get(c)
        if not s: continue
        L.append('| %s | %d | %d %s | %s | %d | %s | %s %s | %d / %d | %s | %s | %d/%d/%d | %s | %s |' % (
            c, s['n'], s['established'], fmt(s['established_ci']), fmt(s['est_gen_median'], 0), s['established_window'],
            fmt(s['est_gen_window_median'], 0), fmt(s['persistence']),
            fmt(s['persistence_ci']), s['persistence_runs_ge_half'], s['persistence_runs_zero'], fmt(s['zero_wage']),
            fmt(s['quarter_wage']), s['plurality']['0'], s['plurality']['1/4'], s['plurality']['1/2'], fmt(s['prodeff']),
            fmt(s['ext']['persistence']) + ' (n=%d)' % s['ext']['n'] if 'ext' in s else '–'))
    L += ['', '## Holders of fair islands at 2,000 (fractions of fair islands)', '',
          '| cell | fair islands | open militants | greenbeard union (identity / pact) | mixture (identity / pact) | unconditional | greenbeard share (RE 2) | identity islands | closed-shop share of boss slot |',
          '|---|---|---|---|---|---|---|---|---|']
    for c in CELLS:
        s = cells.get(c)
        if not s: continue
        h, hd = s['holders'], s['holders_detail']
        L.append('| %s | %d | %s | %s (%s / %s) | %s (%s / %s) | %s | %s | %s | %s |' % (
            c, s['fair_islands_counted'], fmt(h.get('open militants', 0.0)), fmt(h.get('greenbeard union', 0.0)),
            fmt(hd.get('greenbeard union (identity)', 0.0)), fmt(hd.get('greenbeard union (pact)', 0.0)),
            fmt(h.get('mixture', 0.0)), fmt(hd.get('mixture (identity)', 0.0)), fmt(hd.get('mixture (pact)', 0.0)),
            fmt(h.get('unconditional', 0.0)), fmt(s['greenbeard_share']), fmt(s['identity_islands']),
            fmt(s['closed_shop_share'], 4)))
    L += ['', '## Exits of fair islands (first exit, fractions), cross-island statistics', '']
    for c in CELLS:
        s = cells.get(c)
        if not s: continue
        L.append('- **%s** (%d exits): %s; cross-island P(fair) %s; union compatibility %s; B_eq invasion at horizon '
                 'modal triples %s (T₁ pairs %s)' % (c, s['exits_n'], ', '.join('%s %.2f' % (k, v) for k, v in s['exits'].items()),
                                                    fmt(s['cross_fair']), fmt(s['union_compat']), s['beq_invasion'], s['beq_invasion_T1T1']))
    L += ['', '## Costs, timeouts and production (sampled realized encounters)', '',
          '| cell | TO-changed 0 / 50 / 200 / 2,000 | median play steps (gen 0) | median play+prod (gen 0) | ratio (pooled) | production outcomes (gen 0) | failures in top cost decile | SPO held |',
          '|---|---|---|---|---|---|---|---|']
    for c in CELLS:
        s = cells.get(c)
        if not s: continue
        e = s['encounters']
        tod = ' / '.join(fmt(e[g]['todiff']) if g in e else '–' for g in ('0', '50', '200', '2000'))
        po = e.get('0', {}).get('production_outcomes', {})
        fb = s.get('failures_by_cost_decile')
        top = fmt(fb[-1]['share_of_failures']) if fb else '–'
        L.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (
            c, tod, fmt(e.get('0', {}).get('play_median'), 0), fmt(e.get('0', {}).get('total_median'), 0),
            fmt(s.get('realized_cost', {}).get('ratio')), ', '.join('%s %.2f' % (k, v) for k, v in sorted(po.items())),
            top, s.get('spo_held', '–')))
    L += ['', '## Paired contrasts (persistence, b − a, same founder streams)', '', '| a → b | n | mean a | mean b | Δ | 95% CI | McNemar p (established) |', '|---|---|---|---|---|---|---|']
    for k, p in pairs.items():
        if p is None: continue
        L.append('| %s | %d | %s | %s | %s | %s | %s |' % (k, p['n'], fmt(p['a_mean']), fmt(p['b_mean']), fmt(p['mean_diff']),
                                                       fmt(p['ci']), fmt(p['established_mcnemar_p'])))
    for nm in ('assay_isolated', 'assay_entrant'):
        if nm in out:
            L += ['', '## ' + nm, '']
            for k, v in out[nm].items():
                L.append('- %s: %s' % (k, json.dumps(v)))
    open(os.path.join(RUNS, 'sog-fully-realizable.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
