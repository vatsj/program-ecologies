"""Report for hooks Part R: runs/hooks-r.md and runs/hooks-r.json from runs/hooks_r/rows_*.json.gz.

    python3 src/hooks_r_report.py
"""
import gzip
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'hooks_r')
SCOPES = ['none', 'role', 'behaviour', 'history', 'source', 'root']
SOURCES = ['seed', 'write', 'copy', 'contract']


def load(cell):
    p = os.path.join(OUT, 'rows_%s.json.gz' % cell)
    if not os.path.exists(p): return []
    return sorted(json.load(gzip.open(p)), key=lambda r: r['rep'])


def cp_interval(k, n, a=0.05):
    from scipy.stats import beta
    lo = 0.0 if k == 0 else beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(1 - a / 2, k + 1, n - k)
    return lo, hi


def mcnemar(x, y):
    """Exact two-sided McNemar on paired booleans: (b, c, p)."""
    b = sum(1 for u, v in zip(x, y) if u and not v)
    c = sum(1 for u, v in zip(x, y) if v and not u)
    n = b + c
    if n == 0: return b, c, 1.0
    from scipy.stats import binom
    p = min(1.0, 2 * binom.cdf(min(b, c), n, 0.5))
    return b, c, p


def snap(r, g):
    return r['snaps'].get(str(g))


def cell_summary(rows, g):
    S = [snap(r, g) for r in rows]
    S = [s for s in S if s is not None and 'uo' in s]
    if not S: return None
    n = len(S)
    uo = [bool(s['uo']) for s in S]
    out = dict(n=n, g=g, uo=sum(uo), uo_ci=cp_interval(sum(uo), n), uot=sum(bool(s['uot']) for s in S))
    if 'cls' in S[0]:
        I = len(S[0]['cls'])
        out['ident_per_island'] = float(np.mean([s['n_ident'] for s in S]) / I)
        out['rival_per_island'] = float(np.mean([s['n_rival'] for s in S]) / I)
        out['unheld_per_island'] = float(np.mean([s['n_unheld'] for s in S]) / I)
        out['runs_with_identity'] = sum(1 for s in S if s['n_ident'] > 0)
        out['lost'] = sum(1 for s in S if s.get('lost'))
        eff = [np.mean(s['cc']) for s in S if 'cc' in s and not s.get('lost')]
        out['island_pcc'] = float(np.mean(eff)) if eff else None
        out['hooked_holders'] = float(np.mean([np.mean(s['maj_hooked']) for s in S if 'maj_hooked' in s])) \
            if any('maj_hooked' in s for s in S) else None
        out['maj_sp_share'] = float(np.mean([np.mean(s['maj_sp_share']) for s in S if 'maj_sp_share' in s])) \
            if any('maj_sp_share' in s for s in S) else None
        out['open_share'] = float(np.mean([np.mean(s['open_share']) for s in S if 'open_share' in s])) \
            if any('open_share' in s for s in S) else None
        out['target_share'] = float(np.mean([np.mean(s['target_share']) for s in S if 'target_share' in s])) \
            if any('target_share' in s for s in S) else None
    else:
        out['island_pcc'] = float(np.mean([s['pcc'] for s in S]))
    fs = [s.get('fills') for s in S if s.get('fills')]
    if fs:
        held = np.sum([np.array(f['held']) for f in fs], 0)
        out['held_by_scope'] = (held.sum(1) / max(held.sum(), 1)).tolist()
        out['held_by_source'] = (held.sum(0) / max(held.sum(), 1)).tolist()
        out['held_total_per_run'] = float(held.sum() / len(fs))
        out['applicable_by_scope'] = (np.sum([f['applicable'] for f in fs], 0) / len(fs)).tolist()
        out['selected_by_scope'] = (np.sum([f['selected'] for f in fs], 0) / len(fs)).tolist()
        out['inert_held_per_run'] = float(np.mean([f['inert_held'] for f in fs]))
    ex = [np.array(s['scope_ex']) for s in S if 'scope_ex' in s]
    if ex:
        exs = np.sum(ex, 0)
        out['executed_by_scope'] = (exs / max(exs.sum(), 1)).tolist()
        out['executed_by_source'] = (np.sum([s['src_ex'] for s in S], 0) / max(exs.sum(), 1)).tolist()
    ctr = [np.array(s['ctr']) for s in S if 'ctr' in s]
    if ctr:
        import hooks_r_kern as HK
        c = np.mean(ctr, 0)
        out['per_run'] = dict(writes_grudge=c[HK.CT_GRUDGE], writes_thanks=c[HK.CT_THANKS], evictions=c[HK.CT_EVICT],
                              copies=c[HK.CT_COPY_OK], contracts=c[HK.CT_CONTRACT], fill_enc=c[HK.CT_FENC],
                              exec_hook=c[HK.CT_EXEC_HOOK], exec_filled=c[HK.CT_EXEC_FILLED],
                              composite=c[HK.CT_COMPOSITE], uniform=c[HK.CT_UNIFORM], misses=c[HK.CT_MISS_PAIR])
    return out


def cell_summary_fills(rows, g):
    S = [snap(r, g) for r in rows]
    fs = [s.get('fills') for s in S if s and s.get('fills')]
    if not fs: return None
    held = np.sum([np.array(f['held']) for f in fs], 0)
    return dict(n=len(fs), held_by_scope=(held.sum(1) / max(held.sum(), 1)).tolist(),
                held_by_source=(held.sum(0) / max(held.sum(), 1)).tolist(), held_total_per_run=float(held.sum() / len(fs)))


def paired(rows_a, rows_b, g):
    A = {r['rep']: snap(r, g) for r in rows_a}; B = {r['rep']: snap(r, g) for r in rows_b}
    reps = sorted(k for k in A if k in B and A[k] is not None and B[k] is not None and 'uo' in A[k] and 'uo' in B[k])
    if not reps: return None
    x = [bool(A[k]['uo']) for k in reps]; y = [bool(B[k]['uo']) for k in reps]
    b, c, p = mcnemar(x, y)
    return dict(n=len(reps), a=sum(x), b=sum(y), diff=(sum(x) - sum(y)) / len(reps), only_a=b, only_b=c, p=p)


def paired2(rows_a, ga, rows_b, gb):
    A = {r['rep']: snap(r, ga) for r in rows_a}; B = {r['rep']: snap(r, gb) for r in rows_b}
    reps = sorted(k for k in A if k in B and A[k] is not None and B[k] is not None and 'uo' in A[k] and 'uo' in B[k])
    if not reps: return None
    x = [bool(A[k]['uo']) for k in reps]; y = [bool(B[k]['uo']) for k in reps]
    b, c, p = mcnemar(x, y)
    return dict(n=len(reps), a=sum(x), b=sum(y), diff=(sum(x) - sum(y)) / len(reps), only_a=b, only_b=c, p=p)


def trajectory(rows):
    """UO runs, mean island P(C,C) and unheld share at each full snapshot; median generation at which P(C,C) >= 0.99."""
    out = {}
    for g in (200, 500, 1000, 2000):
        S = [snap(r, g) for r in rows]; S = [s for s in S if s and 'uo' in s]
        if not S: continue
        out[str(g)] = dict(n=len(S), uo=sum(bool(s['uo']) for s in S), pcc=float(np.mean([np.mean(s['cc']) for s in S])),
                           unheld=float(np.mean([s['n_unheld'] for s in S]) / len(S[0]['cc'])))
    t = []
    for r in rows:
        hit = [g for (g, p, *_) in r['trace'] if p >= 0.99]
        t.append(hit[0] if hit else float('inf'))
    out['t99_median'] = None if np.isinf(np.median(t)) else float(np.median(t))
    out['t99_never'] = int(sum(1 for x in t if np.isinf(x))); out['n'] = len(t)
    return out


def audit_summary():
    """Identity audit (hooks_r_run.py idaudit): per cell, audited runs with raw 'identity' labels, the raw count,
    and the strict count: islands whose majority type is mutual with none of 300 reference self-cooperating units, no
    panel unit and no living type of another spelling."""
    out = {}
    for tag in ('main', 'ablations', 'mrivals'):
        p = os.path.join(OUT, 'idaudit_%s.json' % tag)
        if not os.path.exists(p): continue
        for x in json.load(open(p)):
            d = out.setdefault(x['cell'], dict(runs=0, raw_i=0, raw_r=0, strict=0, strict_of_i=0, not_reproduced=0, islands=0))
            isl = x['islands']
            st = [i for i in isl if i['ref_mutual'] == 0 and i['panel_mutual'] == 0 and i['living_other_mutual'] == 0]
            d['runs'] += 1; d['raw_i'] += sum(1 for i in isl if i['label'] == 'i'); d['raw_r'] += sum(1 for i in isl if i['label'] == 'r')
            d['strict'] += len(st); d['strict_of_i'] += sum(1 for i in st if i['label'] == 'i')
            d['not_reproduced'] += 0 if x['reproduced'] else 1
            d['islands'] += 64
    return out


STEP_SLOPE = dict(none=224, role=224, behaviour=28866, history=1336, source=1340, root=232)


def cost_model(rows):
    """Modelled verification steps per fill encounter (R15): gene-site checks per fill encounter times steps per check,
    the latter 71 + (fills per holder) x (scope-weighted per-fill slope) from the gate's measured costs (runs/hooks-r-gate.json
    g4_steps: slopes from the 1/2/4-fill checks).  Means over runs, not medians; the lists are priced alike in the inert
    and the live cells (inert fills are held, scanned and never applied)."""
    import hooks_r_kern as HK
    out = {}
    for g in (1000, 2000):
        v = []
        for r in rows:
            s = snap(r, g)
            if not s or 'fills' not in s: continue
            held = np.array(s['fills']['held']).sum(1); tot = held.sum()
            if tot == 0: continue
            w = held / tot
            k = min(4.0, tot / (12800 * 0.95))
            sl = sum(w[i] * STEP_SLOPE[SCOPES[i]] for i in range(6))
            chk = 71 + k * sl
            c = s['ctr']
            v.append((chk, c[HK.CT_EXEC_HOOK] / c[HK.CT_FENC], c[HK.CT_EXEC_FILLED] / max(c[HK.CT_EXEC_HOOK], 1)))
        if v:
            v = np.array(v)
            out[str(g)] = dict(steps_per_check=float(np.median(v[:, 0])), sites_per_encounter=float(np.median(v[:, 1])),
                               steps_per_encounter=float(np.median(v[:, 0] * v[:, 1])), filled_site_share=float(np.mean(v[:, 2])),
                               empty_list_steps_per_encounter=float(71 * np.median(v[:, 1])))
    return out


CELLS_MAIN = ['B', 'I', 'M']
CELLS_ABL = ['M-none', 'M-role', 'M-behaviour', 'M-history', 'M-source', 'M-root', 'seedonly', 'nowrite', 'nocopy',
             'nocontract', 'shuffle', 'noinherit', 'grudgeonly', 'idroutes', 'renorm', 'clone', 'recency']
CELLS_SIZE = ['B-400', 'I-400', 'M-400']


def main():
    res = dict(cells={}, paired={})
    allc = CELLS_MAIN + CELLS_ABL + CELLS_SIZE
    rows = {c: load(c) for c in allc}
    for c in allc:
        if not rows[c]: continue
        res['cells'][c] = {str(g): cell_summary(rows[c], g) for g in (200, 500, 1000, 2000, 5000)}
        res['cells'][c]['time_s'] = float(np.mean([r['time_s'] for r in rows[c]]))
        res['cells'][c]['n_rows'] = len(rows[c])
    for g in (1000, 2000, 5000):
        for a, b in [('I', 'B'), ('M', 'I'), ('M', 'B')]:
            if rows[a] and rows[b]: res['paired']['%s-%s@%d' % (a, b, g)] = paired(rows[a], rows[b], g)
    for c in CELLS_ABL:
        if rows[c] and rows['M']:
            res['paired']['%s-M@1000' % c] = paired(rows[c], rows['M'], 1000)
            res['paired']['%s-I@1000' % c] = paired(rows[c], rows['I'], 1000)
            res['paired']['%s-B@1000' % c] = paired(rows[c], rows['B'], 1000)
            res['paired']['%s@1000-M@2000' % c] = paired2(rows[c], 1000, rows['M'], 2000)
    res['paired']['M@2000-M@1000'] = paired2(rows['M'], 2000, rows['M'], 1000)
    res['traj'] = {c: trajectory(rows[c]) for c in allc if rows[c]}
    res['audit'] = audit_summary()
    res['cost'] = {c: cost_model(rows[c]) for c in ('I', 'M', 'seedonly', 'clone') if rows[c]}
    for a, b in [('M-400', 'I-400'), ('I-400', 'B-400')]:
        if rows[a] and rows[b]: res['paired']['%s-%s@2000' % (a, b)] = paired(rows[a], rows[b], 2000)
    for c in allc:
        if rows[c]:
            res['cells'][c]['0'] = cell_summary_fills(rows[c], 0)
    json.dump(res, open(os.path.join(ROOT, 'runs', 'hooks-r.json'), 'w'), indent=1, default=float)
    open(os.path.join(ROOT, 'runs', 'hooks-r.md'), 'w').write(markdown(res))
    print(json.dumps({k: {g: (v[g]['uo'], v[g]['n'], round(v[g].get('ident_per_island') or 0, 4))
                          for g in v if isinstance(v[g], dict) and v[g] and 'uo' in v[g]} for k, v in res['cells'].items()}, indent=0))
    for k, v in res['paired'].items():
        if v: print(k, v)



def fmt(x, d=3):
    if x is None: return '–'
    if isinstance(x, float): return ('%.' + str(d) + 'f') % x
    return str(x)


def markdown(res):
    L = ['# Hooks, Part R: run report (generated by src/hooks_r_report.py)', '',
         'Every number is an ε = 0 lottery statistic at finite (N, I, horizon) on world K, S-nonself production, '
         'w = 0.3, r = 100, r_f = 2, calibrated mN, (200, 64); classifier as notes §2.5 (mass-based). The identity columns of the first table are the raw mass-classifier '
         'labels, which over-count (a monomorphic rival island is labelled identity); the audited counts are in the identity-audit table.', '']
    C = res['cells']
    L.append('## Cells (universal-open runs of n; per-island rates over all islands of all runs)')
    L.append('')
    L.append('| cell | g | n | UO | UO 95% | UOT | identity (raw label) / island | runs with raw identity label | rival / island | unheld / '
             'island | island P(C,C) | hooked holders | majority-spelling share | open share | target share |')
    L.append('|' + '---|' * 15)
    for c, v in C.items():
        for g in ('1000', '2000'):
            s = v.get(g)
            if not s: continue
            L.append('| %s | %s | %d | %d | [%.2f, %.2f] | %d | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                c, g, s['n'], s['uo'], s['uo_ci'][0], s['uo_ci'][1], s['uot'], fmt(s.get('ident_per_island'), 4),
                fmt(s.get('runs_with_identity')), fmt(s.get('rival_per_island'), 4), fmt(s.get('unheld_per_island'), 4),
                fmt(s.get('island_pcc')), fmt(s.get('hooked_holders'), 2), fmt(s.get('maj_sp_share'), 2),
                fmt(s.get('open_share'), 3), fmt(s.get('target_share'), 3)))
    L.append('')
    L.append('## Paired contrasts (universal-open; exact McNemar)')
    L.append('')
    L.append('| contrast | n | a | b | Δ | only a | only b | p |')
    L.append('|---|---|---|---|---|---|---|---|')
    for k, v in res['paired'].items():
        if v: L.append('| %s | %d | %d | %d | %+.2f | %d | %d | %.3g |' % (k, v['n'], v['a'], v['b'], v['diff'],
                                                                         v['only_a'], v['only_b'], v['p']))
    L.append('')
    L.append('## Fills per hook kind (shares of held fills, individual-weighted, summed over runs)')
    L.append('')
    L.append('| cell | g | held per run | held by scope (' + ', '.join(SCOPES) + ') | held by source (' +
             ', '.join(SOURCES) + ') | executed by scope | executed by source |')
    L.append('|---|---|---|---|---|---|---|')
    for c, v in C.items():
        for g in ('0', '200', '1000', '2000'):
            s = v.get(g)
            if not s or 'held_by_scope' not in s: continue
            L.append('| %s | %s | %.0f | %s | %s | %s | %s |' % (
                c, g, s['held_total_per_run'], ' / '.join('%.2f' % x for x in s['held_by_scope']),
                ' / '.join('%.2f' % x for x in s['held_by_source']),
                ' / '.join('%.3f' % x for x in s.get('executed_by_scope', [])),
                ' / '.join('%.3f' % x for x in s.get('executed_by_source', []))))
    L.append('')
    L.append('## Fill operations per run (cumulative at the cell horizon)')
    L.append('')
    L.append('| cell | g | grudges | thanks | evictions | copies | contracts | fill encounters | gene sites reached | '
             'filled sites | composite pair evals | host misses | time (s) |')
    L.append('|' + '---|' * 13)
    for c, v in C.items():
        for g in ('1000', '2000'):
            s = v.get(g)
            if not s or 'per_run' not in s: continue
            p = s['per_run']
            L.append('| %s | %s | %.0f | %.0f | %.0f | %.0f | %.0f | %.0f | %.0f | %.0f | %.3g | %.3g | %.0f |' % (
                c, g, p['writes_grudge'], p['writes_thanks'], p['evictions'], p['copies'], p['contracts'],
                p['fill_enc'], p['exec_hook'], p['exec_filled'], p['composite'], p['misses'], v['time_s']))
    L.append('')
    L.append('## Trajectories (UO runs / mean island P(C,C) / unheld islands per island at each snapshot; median generation at which '
             'the run mean P(C,C) first reaches 0.99)')
    L.append('')
    L.append('| cell | n | g200 | g500 | g1000 | g2000 | median g(P(C,C) >= 0.99) | runs never reaching it |')
    L.append('|---|---|---|---|---|---|---|---|')
    for c, t in res.get('traj', {}).items():
        cols = []
        for g in ('200', '500', '1000', '2000'):
            x = t.get(g)
            cols.append('%d / %.3f / %.3f' % (x['uo'], x['pcc'], x['unheld']) if x else '–')
        L.append('| %s | %d | %s | %s | %s |' % (c, t['n'], ' | '.join(cols), fmt(t['t99_median'], 0), t['t99_never']))
    L.append('')
    L.append('## Identity audit (post hoc; src/hooks_r_run.py idaudit; strict = mutual with none of 300 reference self-cooperating '
             'units, no panel unit, no living type of another spelling)')
    L.append('')
    L.append('| cell | audited runs | raw identity labels | strict identity | strict among raw-identity | raw rival labels | strict among rival-labelled | not reproduced |')
    L.append('|---|---|---|---|---|---|---|---|')
    for c, d in res.get('audit', {}).items():
        L.append('| %s | %d | %d | %d | %d | %d | %d | %d |' % (c, d['runs'], d['raw_i'], d['strict'], d['strict_of_i'], d['raw_r'],
                                                          d['strict'] - d['strict_of_i'], d['not_reproduced']))
    L.append('')
    L.append('## Modelled verification cost (R15; means over runs, lists priced alike in inert and live cells)')
    L.append('')
    L.append('| cell | g | steps per check | gene-site checks per fill encounter | steps per encounter | share of reached sites with a live fill | steps per encounter if every list were empty |')
    L.append('|---|---|---|---|---|---|---|')
    for c, v in res.get('cost', {}).items():
        for g, x in v.items():
            L.append('| %s | %s | %.0f | %.2f | %.0f | %.2f | %.0f |' % (c, g, x['steps_per_check'], x['sites_per_encounter'],
                                                                    x['steps_per_encounter'], x['filled_site_share'],
                                                                    x['empty_list_steps_per_encounter']))
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    main()
