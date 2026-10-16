"""Report for removing rival networks (notes/removing-rivals.md): Part 0 static tables, B1 cure, A / B2 / B3 cells,
assays, the RS's selected-versus-drift criterion, and verdict inputs.  Writes runs/removing-rivals.json and prints
markdown tables.

    python3 src/removing_rivals_report.py part0
    python3 src/removing_rivals_report.py all
"""
import gzip
import json
import math
import os
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import provenance as PV
import provenance_run as PR
import removing_rivals as RR

ROOT = RR.ROOT
OUT = RR.OUT
RATES = (0.01, 0.1, 1.0)


def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'), float('nan'))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(c - h, 3), round(c + h, 3))


def boot_runs(vals_by_run, B=2000, seed=1):
    """Run-clustered bootstrap of a pooled island fraction: vals_by_run = list of (numerator, denominator)."""
    if not vals_by_run: return (float('nan'), float('nan'))
    rng = np.random.default_rng(seed)
    a = np.array(vals_by_run, float)
    out = []
    for _ in range(B):
        idx = rng.integers(0, len(a), len(a))
        s = a[idx].sum(0)
        out.append(s[0] / s[1] if s[1] > 0 else np.nan)
    return (round(float(np.nanpercentile(out, 2.5)), 3), round(float(np.nanpercentile(out, 97.5)), 3))


def load(name):
    p = os.path.join(OUT, name)
    return json.load(open(p)) if os.path.exists(p) else []


def cellkey(c):
    return c.replace('rs_', '')


# ------------------------------------------------------------------------------------------------ Part 0
def part0():
    ck = load('ckpt_rows.json')
    LS = PR.lot_static(); S = RR.static(LS)
    names = LS['names']
    res = dict(n_runs=len(ck), trace_points=sum(r['trace_compared'] for r in ck),
               trace_bad=sum(r['trace_bad'] for r in ck))
    # per cell
    cells = defaultdict(list)
    for r in ck: cells[r['cell']].append(r)
    tab = []
    for c in sorted(cells):
        rs = cells[c]
        lab = Counter(l for r in rs for l in r['labels'])
        tab.append(dict(cell=cellkey(c), runs=len(rs), uo=sum(r['uo'] for r in rs), uot=sum(r['uot'] for r in rs),
                        split=sum(r['split'] for r in rs), saved=sum(r['saved'] for r in rs),
                        target_isl=lab.get('', 0), identity=lab.get('identity', 0), exploitable=lab.get('exploitable', 0),
                        closed_open=lab.get('closed-open', 0), closed_nonopen=lab.get('closed-nonopen', 0),
                        unheld=lab.get('unheld', 0), islands=sum(len(r['labels']) for r in rs)))
    res['cells'] = tab
    # uo runs on target
    uo = [r for r in ck if r['uo']]
    res['uo_runs'] = len(uo); res['uo_runs_on_target'] = sum(r['uot'] for r in uo)
    # island labels pooled (non-uot runs), and against the stored classifier
    isl = [(r, i, l, r['stored_labels'][i], r['pred_mass'][i]) for r in ck if not r['uot'] for i, l in enumerate(r['labels'])
           if l not in ('', 'unheld')]
    lab = Counter(l for _, _, l, _, _ in isl)
    res['rival_islands'] = dict(lab)
    nonid = [z for z in isl if z[2] != 'identity']
    ex = sum(1 for z in nonid if z[2] == 'exploitable')
    res['re1_target'] = dict(nonid=len(nonid), exploitable=ex, frac=ex / max(1, len(nonid)),
                             ci=boot_runs([(sum(1 for z in nonid if z[0] is r and z[2] == 'exploitable'),
                                            sum(1 for z in nonid if z[0] is r)) for r in ck if not r['uot']]))
    st_rival = [z for z in isl if z[3] == 'rival']
    st_ident = [z for z in isl if z[3] == 'identity']
    res['re1_stored'] = dict(rival=len(st_rival), exploitable=sum(1 for z in st_rival if z[2] == 'exploitable'),
                             labels=dict(Counter(z[2] for z in st_rival)),
                             frac=sum(1 for z in st_rival if z[2] == 'exploitable') / max(1, len(st_rival)))
    res['identity_islands'] = dict(n=lab.get('identity', 0), with_predator=sum(1 for z in isl if z[2] == 'identity' and z[4] > 0),
                                   stored_identity=len(st_ident))
    # stored-classifier "fine" islands that are target-relative rivals
    res['cross'] = dict(Counter('%s|%s' % (z[3] or 'main', z[2]) for z in isl))
    # predator masses
    m = np.array([z[4] for z in isl if z[2] == 'exploitable'])
    res['pred_mass'] = dict(n=int(len(m)), min=float(m.min()) if len(m) else None,
                            q25=float(np.percentile(m, 25)) if len(m) else None,
                            median=float(np.median(m)) if len(m) else None,
                            q75=float(np.percentile(m, 75)) if len(m) else None, max=float(m.max()) if len(m) else None)
    # per distinct rival holder: top predators, constants, certified counts
    hold = {}
    for r in ck:
        for k, v in r['preds'].items():
            cnt = sum(1 for i, l in enumerate(r['labels']) if l not in ('', 'unheld') and '%d|%d' % (r['holder_unit'][i], r['holder_sp'][i]) == k)
            h = hold.setdefault(k, dict(v, islands=0))
            h['islands'] += cnt
    top = sorted(hold.values(), key=lambda v: -v['islands'])[:15]
    res['holders'] = [dict(holder=v['holder'], unit=v['unit'], islands=v['islands'], mass=round(v['mass'], 5),
                           n_sp=v['n_sp'], top=v['top'], constants=v['constants'], cert=v['cert_coop_defect'],
                           cert_pred=v['cert_pred'], fragile=round(v['fragile_mass'], 5),
                           ident=bool(S['ident'][v['unit']]), open=bool(S['openu'][v['unit']])) for v in top]
    res['any_constant_predator'] = sorted(set(c for v in hold.values() for c in v['constants']))
    # expected arrivals and cure probability by rate for the exploitable islands
    res['arrivals'] = {}
    for e in RATES:
        res['arrivals'][str(e)] = dict(mean_arrivals_per_isl_gen=float(e * m.mean()) if len(m) else 0,
                                       expected_cure_10k=float(np.mean(1 - np.exp(-0.26 * e * m * 1e4))) if len(m) else 0)
    # exploitable target members
    tu = Counter()
    tun_by = {}
    for r in ck:
        for i, t in enumerate(r['ontgt']):
            if t:
                tu[(r['holder_unit'][i], r['holder_sp'][i])] += 1
                tun_by.setdefault((r['holder_unit'][i], r['holder_sp'][i]), set()).update(r['tgt_units'])
    em = []
    for (u, s), n in tu.most_common(25):
        Tun = sorted(tun_by[(u, s)] - {u}) or [S['uPB']]
        if u == S['uPB']: Tun = sorted(set(Tun) - {u})
        pt = RR.predator_table(u, s, PV.R_SNON, Tun, LS)
        em.append(dict(holder=names[s], unit=u, islands=n, mass=round(pt['mass'], 5), top=pt['top'][:2]))
    res['target_members'] = em
    tot = sum(x['islands'] for x in em)
    res['target_exploitable_island_share'] = sum(x['islands'] for x in em if x['mass'] > 0) / max(1, tot)
    # stability of 2,000 vs stored final spelling
    res['same_holder_sp_final'] = sum(r['same_as_stored_final'] for r in ck)
    res['time_s'] = sum(r['time_s'] for r in ck)
    return res


def md_part0(p):
    L = []
    L.append('Reconstructed %d stored runs to generation 2,000: %d trace points compared, %d differences.' % (
        p['n_runs'], p['trace_points'], p['trace_bad']))
    L.append('')
    L.append('| cell | runs | universal-open | universal-on-target | split | target isl | identity | exploitable | closed-open | closed-nonopen | unheld |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|')
    for t in p['cells']:
        L.append('| %s | %d | %d | %d | %d | %d | %d | %d | %d | %d | %d |' % (
            t['cell'], t['runs'], t['uo'], t['uot'], t['split'], t['target_isl'], t['identity'], t['exploitable'],
            t['closed_open'], t['closed_nonopen'], t['unheld']))
    L.append('')
    L.append('universal-open runs: %d, of which on target: %d' % (p['uo_runs'], p['uo_runs_on_target']))
    L.append('rival islands (non-uot runs): %s' % p['rival_islands'])
    L.append('RE1 target-relative: %s' % p['re1_target'])
    L.append('RE1 stored-classifier: %s' % p['re1_stored'])
    L.append('identity: %s' % p['identity_islands'])
    L.append('cross (stored|mine): %s' % p['cross'])
    L.append('predator mass over exploitable islands: %s' % p['pred_mass'])
    L.append('constants among predators: %s' % p['any_constant_predator'])
    L.append('arrivals: %s' % p['arrivals'])
    L.append('')
    L.append('| rival holder | unit | islands | identity | open | μ(Pred) | spellings | top predators | certified (coop-defect / pred) | fragile |')
    L.append('|---|---|---|---|---|---|---|---|---|---|')
    for h in p['holders']:
        L.append('| `%s` | %d | %d | %s | %s | %.4f | %d | %s | %d / %d | %.4f |' % (
            h['holder'], h['unit'], h['islands'], h['ident'], h['open'], h['mass'], h['n_sp'],
            '; '.join('`%s` %.1e' % (a, b) for a, b, _ in h['top']), h['cert'], h['cert_pred'], h['fragile']))
    L.append('')
    L.append('target members (most common): ' + '; '.join('`%s` u%d isl %d μ %.4f' % (x['holder'], x['unit'], x['islands'], x['mass']) for x in p['target_members'][:12]))
    L.append('target-island share held by exploitable members: %.3f' % p['target_exploitable_island_share'])
    L.append('same holder spellings at stored final: %d / %d; worker seconds %.0f' % (p['same_holder_sp_final'], p['n_runs'], p['time_s']))
    return '\n'.join(L)


def loss_kinds(L, after=0):
    """Loss records (island, start, length, code, unit, sp) by the new holder: identity / open (a closed-open or other
    open non-target holder, the FairBot-bridged flip) / unheld / other; only episodes starting at or after `after`."""
    S = RR.static(PR.lot_static())
    c = Counter()
    for l in L:
        if l[1] < after: continue
        code, u = l[3], l[4]
        if code == 0: c['unheld'] += 1
        elif S['ident'][u]: c['identity'] += 1
        elif S['openu'][u]: c['open'] += 1
        else: c['other'] += 1
    return dict(c)


# ------------------------------------------------------------------------------------------------ B1
def b1(rows):
    """Matched branches: per rival island, resolution in the rain branch and in the eps = 0 branch."""
    out = dict(n_ckpt=len(rows))
    per = defaultdict(lambda: defaultdict(list))      # rate -> label -> [(run, resolved, resolved0, path, t, mass)]
    runs = defaultdict(list)                           # rate -> [(uot_end, uot_end0, uo_end)]
    loss = defaultdict(lambda: [0, 0, 0])              # rate -> [losses, target islands at ckpt, transient]
    lk = defaultdict(Counter)
    arr = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    colev = defaultdict(list)
    val = [0, 0]
    tsum = 0.0
    ck = {(r['cell'], r['rep']): r for r in load('ckpt_rows.json')}
    for r in rows:
        tsum += r['time_s']
        br = {b['epsN']: b for b in r['branches']}
        b0 = br.get(0.0)
        if b0 is None: continue
        val[0] += b0['validate']['n']; val[1] += b0['validate']['bad']
        c = ck[(r['cell'], r['rep'])]
        ntgt = sum(c['ontgt'])
        res0 = {x['island']: x for x in b0['islands']}
        for e, b in br.items():
            for x in b['islands']:
                x0 = res0[x['island']]
                per[e][x['label']].append(((r['cell'], r['rep']), bool(x['resolved']), bool(x0['resolved']), x.get('path'),
                                          (x['g'] - b['g0']) if x['resolved'] else None,
                                          c['pred_mass'][x['island']], x.get('elsewhere', False), x.get('pred_seen', False)))
            sn = b['snaps'][str(b['g_end'])]; sn0 = b0['snaps'][str(b0['g_end'])]
            runs[e].append((sn['uot'], sn0['uot'], sn['uo'], r['cell']))
            loss[e][0] += len(b['losses']); loss[e][1] += ntgt; loss[e][2] += b['n_transient']
            for k_, v_ in loss_kinds(b['losses']).items():
                lk[e][k_] += v_
            a = b['arrivals']
            if a.get('n'):
                for k, v in a['by_class'].items():
                    arr[e][k][0] += v[0]; arr[e][k][1] += v[1]
                for ev in a['colonizations']:
                    colev[e].append(dict(ev, cell=r['cell'], rep=r['rep']))
    out['validate'] = dict(points=val[0], bad=val[1])
    out['time_s'] = tsum
    tabs = {}
    for e in sorted(per):
        t = {}
        for lab, xs in per[e].items():
            n = len(xs)
            k = sum(1 for z in xs if z[1]); k0 = sum(1 for z in xs if z[2])
            byrun = defaultdict(lambda: [0, 0, 0])
            for z in xs:
                byrun[z[0]][0] += z[1]; byrun[z[0]][1] += 1; byrun[z[0]][2] += z[2]
            paths = Counter(z[3] for z in xs if z[1])
            ts = [z[4] for z in xs if z[1]]
            t[lab] = dict(n=n, resolved=k, resolved_eps0=k0, frac=k / n if n else None, frac0=k0 / n if n else None,
                          cure=(k - k0) / n if n else None,
                          ci=boot_runs([(v[0] - v[2], v[1]) for v in byrun.values()]),
                          paths=dict(paths), t_median=float(np.median(ts)) if ts else None,
                          elsewhere=sum(1 for z in xs if not z[1] and z[6]), runs=len(byrun))
            if lab == 'exploitable' and n > 3:
                ms = np.array([z[5] for z in xs]); rs_ = np.array([z[1] for z in xs], float)
                from scipy.stats import spearmanr
                rho = spearmanr(ms, rs_).correlation if rs_.std() > 0 and ms.std() > 0 else None
                t[lab]['spearman_mass_cure'] = None if rho is None or np.isnan(rho) else float(rho)
                pred = 1 - np.exp(-0.26 * e * ms * 1e4) if e > 0 else np.zeros(len(ms))
                t[lab]['predicted_cure'] = float(pred.mean())
                bins = [(0, 1e-3), (1e-3, 4e-3), (4e-3, 1e-2), (1e-2, 1)]
                t[lab]['by_mass'] = [dict(lo=lo, hi=hi, n=int(((ms >= lo) & (ms < hi)).sum()),
                                          cured=float(rs_[(ms >= lo) & (ms < hi)].mean()) if ((ms >= lo) & (ms < hi)).any() else None)
                                     for lo, hi in bins]
        rr = runs[e]
        t['_runs'] = dict(n=len(rr), uot=sum(z[0] for z in rr), uot0=sum(z[1] for z in rr), uo=sum(z[2] for z in rr),
                          by_cell={c: [sum(z[0] for z in rr if z[3] == c), sum(z[1] for z in rr if z[3] == c),
                                       sum(1 for z in rr if z[3] == c)] for c in sorted(set(z[3] for z in rr))})
        t['_losses'] = dict(losses=loss[e][0], target_islands=loss[e][1], per_island=loss[e][0] / max(1, loss[e][1]),
                            transient=loss[e][2], kinds=dict(lk[e]))
        t['_arrivals'] = {k: v for k, v in arr[e].items()}
        tabs[str(e)] = t
    out['tabs'] = tabs
    out['colonizations'] = {str(e): v for e, v in colev.items()}
    return out


def drift_stats(colev, arrivals, island_gens):
    """Drift (neutral or deleterious at arrival) colonizations per island-generation; the shadow case (drift on an
    island that was a target island at arrival)."""
    d = [c for c in colev if c['cls'] != 'selected']
    sh = [c for c in d if c['status_at_arrival'] == 1]
    sel = [c for c in colev if c['cls'] == 'selected']
    prob = {}
    for k, v in arrivals.items():
        prob[k] = dict(arrivals=v[0], colonized=v[1], p=v[1] / v[0] if v[0] else None)
    return dict(drift=len(d), drift_per_isl_gen=len(d) / island_gens if island_gens else None, shadow=len(sh),
                shadow_ontarget_after=sum(1 for c in sh if c['on_target_after']), selected=len(sel), by_class=prob)


# ------------------------------------------------------------------------------------------------ lottery cells
def cell_stats(rows, horizons=(2000, 10000)):
    """Per cell: universal-on-target, universal-open, identity / rival islands, target islands, losses, drift."""
    by = defaultdict(list)
    for r in rows: by[r['cell']].append(r)
    out = {}
    for c, rs in sorted(by.items()):
        d = dict(runs=len(rs), N=rs[0]['N'], I=rs[0]['I'], epsN=rs[0]['epsN'], time_s=sum(r['time_s'] for r in rs))
        for h in horizons:
            sn = [r['snaps'].get(str(h)) for r in rs]
            sn = [x for x in sn if x is not None]
            if not sn: continue
            I = rs[0]['I']; n = len(sn)
            k = sum(x['uot'] for x in sn)
            d[str(h)] = dict(n=n, uot=k, uot_ci=wilson(k, n), uo=sum(x['uo'] for x in sn),
                             split=sum(x['split'] for x in sn),
                             identity=sum(x['identity'] for x in sn) / (n * I),
                             exploitable=sum(x['exploitable'] for x in sn) / (n * I),
                             closed_open=sum(x['closed_open'] for x in sn) / (n * I),
                             closed_nonopen=sum(x['closed_nonopen'] for x in sn) / (n * I),
                             unheld=sum(x['unheld'] for x in sn) / (n * I),
                             target=sum(x['target'] for x in sn) / (n * I),
                             eff=sum(x['eff'] for x in sn) / (n * I), pcc=float(np.mean([x['pcc'] for x in sn])),
                             runs_with_identity=sum(1 for x in sn if x['identity'] > 0),
                             runs_with_closed_open=sum(1 for x in sn if x['closed_open'] > 0),
                             runs_with_exploitable=sum(1 for x in sn if x['exploitable'] > 0),
                             uot_list=[int(x['uot']) for x in sn], reps=[r['rep'] for r in rs if str(h) in r['snaps']])
        d['losses'] = sum(len(r['losses']) for r in rs)
        d['loss_kinds_after2000'] = loss_kinds([l for r in rs for l in r['losses']], 2000)
        d['transient'] = sum(r['n_transient'] for r in rs)
        ig = sum(r['I'] * r['last_gen'] for r in rs)
        d['island_gens'] = ig
        col = [dict(ev, rep=r['rep']) for r in rs for ev in (r['arrivals'].get('colonizations') or [])]
        arr = defaultdict(lambda: [0, 0])
        for r in rs:
            for k_, v in (r['arrivals'].get('by_class') or {}).items():
                arr[k_][0] += v[0]; arr[k_][1] += v[1]
        d['drift'] = drift_stats(col, arr, ig) if rs[0]['epsN'] > 0 else None
        ep = [e for r in rs for e in r['rival_episodes']]
        d['rival_episodes'] = dict(n=len(ep), resolved=sum(1 for e in ep if e['resolved']),
                                   paths=dict(Counter(e.get('path') for e in ep if e['resolved'])))
        out[c] = d
    return out


def paired(rows_a, rows_b, h):
    """Paired difference in universal-on-target at horizon h on common replicates; McNemar-style counts."""
    a = {r['rep']: r['snaps'].get(str(h)) for r in rows_a}
    b = {r['rep']: r['snaps'].get(str(h)) for r in rows_b}
    com = sorted(k for k in a if k in b and a[k] is not None and b[k] is not None)
    ab = sum(1 for k in com if a[k]['uot'] and not b[k]['uot'])
    ba = sum(1 for k in com if b[k]['uot'] and not a[k]['uot'])
    return dict(n=len(com), a_only=ab, b_only=ba, diff=(ab - ba) / len(com) if com else None)


def md_b1(b):
    L = ['B1: %d checkpoints; eps = 0 branch validation %s; worker seconds %.0f' % (b['n_ckpt'], b['validate'], b['time_s'])]
    L.append('')
    L.append('| εN | label | islands (runs) | resolved rain | resolved ε=0 | cure (matched) [run CI] | paths | median t | elsewhere |')
    L.append('|---|---|---|---|---|---|---|---|---|')
    for e, t in b['tabs'].items():
        for lab in ('identity', 'exploitable', 'closed-open', 'closed-nonopen'):
            if lab not in t: continue
            x = t[lab]
            L.append('| %s | %s | %d (%d) | %d (%.2f) | %d | %+.2f %s | %s | %s | %d |' % (
                e, lab, x['n'], x['runs'], x['resolved'], x['frac'], x['resolved_eps0'], x['cure'], x['ci'], x['paths'],
                x['t_median'], x['elsewhere']))
    L.append('')
    for e, t in b['tabs'].items():
        L.append('εN %s runs %s losses %s' % (e, {k: v for k, v in t['_runs'].items()}, t['_losses']))
        if 'exploitable' in t and 'by_mass' in t['exploitable']:
            L.append('   exploitable by mass: %s; predicted %.2f; spearman %s' % (
                t['exploitable']['by_mass'], t['exploitable']['predicted_cure'], t['exploitable'].get('spearman_mass_cure')))
    return '\n'.join(L)


def md_cells(cs):
    L = ['| cell | εN | runs | uot 2k [CI] | uot 10k [CI] | uo 10k | identity isl | exploitable | closed-open | closed-nonopen | unheld | eff | losses | transient |']
    L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for c, d in cs.items():
        a = d.get('2000', {}); b = d.get('10000', {})
        L.append('| %s | %s | %d | %s %s | %s %s | %s | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f | %d | %d |' % (
            c, d['epsN'], d['runs'], a.get('uot'), a.get('uot_ci'), b.get('uot'), b.get('uot_ci'), b.get('uo'),
            b.get('identity', float('nan')), b.get('exploitable', float('nan')), b.get('closed_open', float('nan')),
            b.get('closed_nonopen', float('nan')), b.get('unheld', float('nan')), b.get('eff', float('nan')),
            d['losses'], d['transient']))
    for c, d in cs.items():
        if d.get('drift'):
            L.append('%s drift: %s' % (c, {k: v for k, v in d['drift'].items()}))
        L.append('%s rival episodes: %s' % (c, d['rival_episodes']))
    return '\n'.join(L)


def snon_baseline():
    """S-nonself calibrated universal-on-target per replicate at 2,000 (checkpoints) and 10,000 (the B1 eps = 0
    branch's snapshot at generation 10,000; runs on target at 2,000 taken as unchanged); identity islands too."""
    ck = load('ckpt_rows.json')
    br = {(r['cell'], r['rep']): r for r in load('branch_main.json')}
    out = {}
    for r in ck:
        if not r['cell'].startswith('rs_Snon_') or not r['cell'].endswith('_cal'): continue
        N, I = r['N'], r['I']
        key = 'rr_snon_%d_%d' % (N, I)
        d = out.setdefault(key, {})
        ident2 = sum(1 for l in r['labels'] if l == 'identity')
        u10 = None; ident10 = None
        if r['uot']:
            u10 = True; ident10 = 0
        elif (r['cell'], r['rep']) in br:
            b0 = [b for b in br[(r['cell'], r['rep'])]['branches'] if b['epsN'] == 0][0]
            sn = b0['snaps'].get('10000')
            if sn: u10 = sn['uot']; ident10 = sn['identity']
        d[r['rep']] = dict(uot2=r['uot'], uot10=u10, ident2=ident2, ident10=ident10, I=I)
    return out


def a_compare(cells):
    """Sponsored and empty-control cells against S-nonself (paired by replicate) and C-donor bounds."""
    base = snon_baseline()
    rows = load('lottery_A.json') + load('lottery_B.json')
    by = defaultdict(dict)
    for r in rows: by[r['cell']][r['rep']] = r
    cb = json.load(open(os.path.join(OUT, 'cdonor_bounds.json')))
    out = {}
    for c in cells:
        if c not in by: continue
        N, I = by[c][min(by[c])]['N'], by[c][min(by[c])]['I']
        b = base.get('rr_snon_%d_%d' % (N, I), {})
        res = {}
        for h, k in ((2000, 'uot2'), (10000, 'uot10')):
            pairs = [(int(by[c][rep]['snaps'][str(h)]['uot']), int(b[rep][k])) for rep in by[c]
                     if rep in b and b[rep][k] is not None and str(h) in by[c][rep]['snaps']]
            res[str(h)] = dict(n=len(pairs), cell=sum(p[0] for p in pairs), snon=sum(p[1] for p in pairs),
                               cell_only=sum(1 for p in pairs if p[0] and not p[1]),
                               snon_only=sum(1 for p in pairs if p[1] and not p[0]))
        cbk = 'rs_Cdon_%d_%d_cal' % (N, I)
        res['cdonor_2000'] = cb.get(cbk)
        res['snon_identity_2000'] = sum(v['ident2'] for v in b.values()) / max(1, sum(v['I'] for v in b.values()))
        out[c] = res
    return out


def b1_endstate(rows):
    """Island fractions at the end of each branch, pooled, by rate; losses by kind and median length."""
    S = RR.static(PR.lot_static())
    agg = defaultdict(Counter); lens = defaultdict(list)
    for r in rows:
        for b in r['branches']:
            e = b['epsN']; sn = b['snaps'][str(b['g_end'])]
            agg[e]['I'] += len(sn['labels'])
            for k in ('target', 'identity', 'exploitable', 'closed_open', 'unheld', 'eff'): agg[e][k] += sn[k]
            for l in b['losses']:
                kind = 'unheld' if l[3] == 0 else 'identity' if S['ident'][l[4]] else 'open' if S['openu'][l[4]] else 'other'
                lens['%g|%s' % (e, kind)].append(l[2])
    out = {str(e): {k: a[k] / a['I'] for k in ('target', 'identity', 'exploitable', 'closed_open', 'unheld', 'eff')}
           for e, a in sorted(agg.items())}
    return dict(fractions=out, losses={k: dict(n=len(v), median_len=float(np.median(v))) for k, v in sorted(lens.items())})


def assays():
    ir = load('inject_rows.json'); tr = load('triples_rows.json')
    d = defaultdict(list)
    for r in ir: d['%s|%d|%s' % (r['cell'], r['rep'], r['kind'])].append(r)
    inj = {k: dict(n=len(v), colonized=sum(r['colonized'] for r in v),
                   resolved_after_col=sum(1 for r in v if r['colonized'] and r['path']['resolved']),
                   elsewhere_after_col=sum(1 for r in v if r['colonized'] and not r['path']['resolved']),
                   resolved_any=sum(r['path']['resolved'] for r in v)) for k, v in sorted(d.items())}
    t = defaultdict(list)
    for r in tr: t[r['name']].append(r)
    tri = {k: dict(n=len(v), colonized_own=sum(1 for r in v if 0 in r['colonized']),
                   x_islands_to_target=sum(r['x_to_target'] for r in v), x_islands=4 * len(v),
                   z_lost=sum(r['z_lost'] for r in v)) for k, v in sorted(t.items())}
    return dict(inject=inj, inject_meta=load('inject_meta.json'), triples=tri, triples_meta=load('triples_meta.json'))


def final():
    out = dict(part0=json.load(open(os.path.join(ROOT, 'runs', 'removing-rivals-part0.json'))))
    br = load('branch_main.json')
    out['B1'] = b1(br)
    out['B1'].pop('colonizations', None)
    out['B1_endstate'] = b1_endstate(br)
    rows = load('lottery_A.json') + load('lottery_B.json') + load('lottery_base.json')
    cs = cell_stats(rows)
    for c in cs.values():
        for h in ('2000', '10000'):
            if h in c: c[h].pop('uot_list', None); c[h].pop('reps', None)
        if c.get('drift'): c['drift'].pop('by_class', None)
    out['cells'] = cs
    out['A_compare'] = a_compare([c for c in cs if c.startswith('rr_')])
    out['cdonor_bounds'] = json.load(open(os.path.join(OUT, 'cdonor_bounds.json')))
    out['assays'] = assays()
    for f in ('removing-rivals-drift.json', 'removing-rivals-shadow.json'):
        p = os.path.join(ROOT, 'runs', f)
        if os.path.exists(p): out[f.replace('removing-rivals-', '').replace('.json', '')] = json.load(open(p))
    json.dump(out, open(os.path.join(ROOT, 'runs', 'removing-rivals.json'), 'w'), indent=1, default=str)
    print('wrote runs/removing-rivals.json')
    print(json.dumps(out['B1_endstate'], indent=1))
    print(json.dumps(out['assays']['inject'], indent=0))
    print(json.dumps(out['assays']['triples'], indent=0))


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what == 'part0':
        p = part0()
        json.dump(p, open(os.path.join(ROOT, 'runs', 'removing-rivals-part0.json'), 'w'), indent=1, default=str)
        print(md_part0(p))
    if what == 'final':
        final()
    if what in ('all', 'b1'):
        rows = load('branch_main.json')
        b = b1(rows)
        json.dump(b, open(os.path.join(OUT, 'b1_summary.json'), 'w'), indent=1, default=str)
        print(md_b1(b))
    if what in ('all', 'cells'):
        rows = []
        for f in ('lottery_A.json', 'lottery_B.json', 'lottery_base.json'):
            rows += load(f)
        cs = cell_stats(rows)
        json.dump(cs, open(os.path.join(OUT, 'cells_summary.json'), 'w'), indent=1, default=str)
        print(md_cells(cs))
        ac = a_compare([c for c in cs if c.startswith('rr_')])
        json.dump(ac, open(os.path.join(OUT, 'a_compare.json'), 'w'), indent=1, default=str)
        for c, v in ac.items(): print(c, v)
