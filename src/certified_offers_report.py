"""Step 2 report of queue 79 (spec specs/2026-11-15-certified-offers.md): aggregates runs/co_rows/* with the stored controls (queue 78's FR and
FOR rows, runs/pa_rows/*; queue 75's F rows, runs/lpt_rows/*) into cells, V* tables, delta*, the phi comparison, controls, seeded starts with
exit classification and pacing, the scramble diagnostic, holders, charges.  All numbers are finite-schedule approach-rate statistics
(mN = 1, Lambda = 100, 120N; seeded starts to 240N), not pi.

    python3 src/certified_offers_report.py OUT.json OUT.md
"""
import os, sys, json, glob
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import certified_offers_run as RR
import certified_offers as CO

DELTAS = [1e-1, 3e-2, 1e-2, 3e-3, 1e-3]
FAMN = CO.FAMC


def is_cut(jid):
    sys.path.insert(0, os.path.join(ROOT, 'tools'))
    import co_cut
    return co_cut.is_cut(jid)


def spec_key(row):
    s = row['spec']; parts = s.split(':')
    kv = {p.split('=')[0]: p.split('=')[1] for p in parts[1:] if '=' in p}
    if parts[0] == '2a':
        return ('F', float(kv['b']), 0.0, float(kv['d']), '')
    if parts[0] == 'pa':
        return (kv['arm'], float(kv['b']), 0.0, float(kv['d']), (':seed=' + kv['seed']) if 'seed' in kv else '')
    if parts[0] == 'co':
        ph = float(kv.get('ph', 0.5))
        if kv['arm'] in ('F', 'FR', 'FOR'):
            ph = 0.0
        return (kv['arm'], float(kv['b']), ph, float(kv['d']), (':seed=' + kv['seed']) if 'seed' in kv else '')
    raise ValueError(s)


def load_dir(pattern):
    rows = {}
    for d in glob.glob(os.path.join(ROOT, pattern)):
        rows.update(RR.load_rows(d))
    return rows


def boot(x, B=2000, seed=0):
    x = np.asarray(x, float)
    if len(x) == 0:
        return (None, None)
    rng = np.random.default_rng(seed)
    m = x[rng.integers(0, len(x), (B, len(x)))].mean(1)
    return (float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5)))


def build():
    mine = load_dir('runs/co_rows/*')
    q78 = load_dir('runs/pa_rows/*')
    q75 = load_dir('runs/lpt_rows/*')
    cells = {}
    src = {}
    for jid, r in mine.items():
        if r['series'] in ('v1', 'pilot') or is_cut(jid):
            continue
        k = spec_key(r)
        key = (k[0], k[1], k[2], r['N'], r['I'], k[3], k[4], bool(r['long']))
        cells.setdefault(key, {})[r['r']] = r; src[key] = 'q79'
    for jid, r in q78.items():
        if r['series'] not in ('main', 'b0', 'i256', 'seed2'):
            continue
        k = spec_key(r)
        if k[0] not in ('FR', 'FOR') or ('g=1.0' not in r['spec'] and 'seed' not in r['spec']):
            continue
        key = (k[0], k[1], 0.0, r['N'], r['I'], k[3], k[4], bool(r['long']))
        if key in src and src[key] == 'q79':
            continue
        cells.setdefault(key, {})[r['r']] = r; src[key] = 'q78'
    for jid, r in q75.items():
        if not jid.startswith('2a|') or ':s1' in r['spec']:
            continue
        k = spec_key(r)
        if k[1] not in (0.0, 1.0, 3.0):
            continue
        key = ('F', k[1], 0.0, r['N'], r['I'], k[3], '', False)
        cells.setdefault(key, {})[r['r']] = r; src[key] = 'q75'
    out = {}
    for key, d in cells.items():
        rs = [d[r] for r in sorted(d) if r < 20]
        out[key] = cell_stats(rs)
        out[key]['_rows'] = rs
        out[key]['src'] = src[key]
    return out


def cell_stats(rs):
    v = np.array([r['vstar'] for r in rs])
    lo, hi = boot(v)
    pairs = np.zeros(3)
    for r in rs:
        pairs += np.array(r['snap120']['pair_modal'], float)
    cls = np.zeros(5)
    for r in rs:
        cls += np.array(r['snap120']['cls_modal'], float)
    fp = [int(r['cons_modal']['fair_pair']) for r in rs]
    un = int(sum(1 for r in rs if r['cons_modal']['unequal'] >= 0))
    hold = {'F': {}, 'U': {}}
    for r in rs:
        for lab in ('F', 'U'):
            for f, n in r['snap120']['hold'][lab].items():
                hold[lab][FAMN[int(f)] if int(f) < len(FAMN) else f] = hold[lab].get(FAMN[int(f)] if int(f) < len(FAMN) else f, 0) + n
    ch = {}
    for r in rs:
        c = (r.get('charges') or {}).get('120N')
        if not c:
            continue
        for f, x in c.items():
            if f != 'all' and x[0] is not None and x[1] > 0:
                ch.setdefault(f, []).append((x[0], x[1]))
    chm = {f: float(sum(a * b for a, b in l) / sum(b for a, b in l)) for f, l in ch.items()}
    scr = [r['scramble'] for r in rs if r.get('scramble')]
    rr = {}
    for r in rs:
        for k, n in (r.get('rroutes') or {}).items():
            rr[k] = rr.get(k, 0) + n
    return dict(n=len(rs), mean=float(v.mean()) if len(v) else None, ci=[lo, hi], all_fair=float((v >= 1.0 - 1e-9).mean()) if len(v) else None,
                fair_pair_islands=(pairs / max(pairs.sum(), 1)).tolist(), cls120=(cls / max(cls.sum(), 1)).tolist(),
                consensus_pairs=[fp.count(i) for i in (0, 1, 2)], unequal_consensus=un, hold=hold, charges=chm,
                scramble_same_class=(float(np.mean([s['same_class'] for s in scr])) if scr else None),
                scramble_n_islands=sum(1 for _ in scr) * 64, rroutes=rr, v_by_run=[float(x) for x in v])


def get(cs, arm, beta, phi, N, I, d, ex='', long=False):
    return cs.get((arm, beta, phi, N, I, d, ex, long))


def delta_star(cs, arm, beta, phi, N, I, deltas=DELTAS, thr=0.9):
    means = {}
    for d in deltas:
        c = get(cs, arm, beta, phi, N, I, d)
        means[d] = c['mean'] if c and c['n'] == 20 else None
    if any(means[d] is None for d in deltas):
        return dict(status='incomplete', means=means)
    passing = [means[d] >= thr for d in deltas]
    k = 0
    while k < len(deltas) and passing[k]:
        k += 1
    iso = [d for d, p in zip(deltas[k:], passing[k:]) if p]
    if k == 0:
        return dict(status='none', means=means, isolated=iso)
    return dict(status='bracket', lower=(deltas[k] if k < len(deltas) else None), upper=deltas[k - 1], means=means, isolated=iso)


def ds_str(ds):
    if ds['status'] == 'none':
        return 'none' + (' (isolated pass at %s)' % ds['isolated'] if ds['isolated'] else '')
    if ds['status'] == 'bracket':
        return '(%s, %g]' % (('%g' % ds['lower']) if ds['lower'] else '< 1e-3', ds['upper'])
    return ds['status']


def fmtc(c):
    if not c:
        return '-'
    s = '%.2f [%.2f, %.2f]' % (c['mean'], c['ci'][0], c['ci'][1])
    if c['n'] < 20:
        s += ' (n=%d)' % c['n']
    return s


def vtable(cs, rows_spec, beta, N, I=64, label=None):
    Lx = ['%s: V\\* at 120N (mean over runs [95%% bootstrap]), by δ' % (label or 'N = %d, I = %d, β = %g' % (N, I, beta)), '',
          '| arm (φ) | ' + ' | '.join('%g' % d for d in DELTAS) + ' | δ\\* |', '|---|' + '---|' * (len(DELTAS) + 1)]
    for arm, phi in rows_spec:
        cells = [get(cs, arm, beta, phi, N, I, d) for d in DELTAS]
        if not any(cells):
            continue
        src = [c['src'] for c in cells if c]
        tag = ' (stored)' if src and src[0] != 'q79' else ''
        Lx.append('| %s (%g)%s | ' % (arm, phi, tag) + ' | '.join(fmtc(c) for c in cells) + ' | %s |' % ds_str(delta_star(cs, arm, beta, phi, N, I)))
    Lx.append('')
    return Lx


SEED_KINDS = (('unequal', 0.5), ('unequalBc', 0.5), ('unequalBc', 1.0), ('fair', 0.5), ('fairC', 0.5))


def seeded(cs):
    out = {}
    for arm in ('FR', 'Fc', 'FcOcRc', 'FcRc', 'FcOcRcs'):
        for kind, ph in SEED_KINDS:
            phk = 0.0 if arm == 'FR' else ph
            if arm == 'FR' and ph == 1.0:
                continue
            c = get(cs, arm, 3.0, phk, 200, 64, 0.03, ':seed=%s' % kind, True)
            if not c:
                continue
            rs = c['_rows']
            ex = [r['exits'] for r in rs]
            f30 = np.mean([e['fair30'] for e in ex]); f120 = np.mean([e['fair120'] for e in ex]); f240 = np.mean([e['fair_end'] for e in ex])
            hz = [e['hazard'] for e in ex]
            nUF = sum(h['toend']['n_UF'] for h in hz); occ = sum(h['toend']['occ_U'] for h in hz)
            routes = {}; lasted = {}
            for r in rs:
                for e in r['exits']['exits']:
                    k = '%s|%s' % (e['route'], e.get('origin', '-'))
                    routes[k] = routes.get(k, 0) + 1
                    if e['lasted_to_120N']:
                        lasted[k] = lasted.get(k, 0) + 1
            pc = [r.get('pacing') for r in rs if r.get('pacing')]
            pace = None
            if pc:
                e_arr = {}; v_arr = {}
                for p in pc:
                    for dd, tgt in ((p['e_arr'], e_arr), (p['v_arr'], v_arr)):
                        for k, v in dd.items():
                            t = tgt.setdefault(k, [0, 0.0, 0])
                            t[0] += v['n']; t[1] += v['pred']; t[2] += v['fixed']
                durs = [x for p in pc for x in ([p['fpt_median']] if p['fpt_median'] is not None else [])]
                pace = dict(acc_expo=sum(p['acc_expo'] for p in pc), accR_expo=sum(p['accR_expo'] for p in pc),
                            pred_second=sum(p['pred_second'] for p in pc), n_second=sum(p['n_second'] for p in pc),
                            pred_first=sum(p['pred_first'] for p in pc), n_first=sum(p['n_first'] for p in pc),
                            e_arr=e_arr, v_arr=v_arr, unequal_exits=sum(p['unequal_exits'] for p in pc),
                            unequal_censored=sum(p['unequal_censored'] for p in pc), fpt_median_of_runs=(float(np.median(durs)) if durs else None),
                            n_transitions=sum(p['n_transitions'] for p in pc))
            obs_local_cert = sum(n for k, n in routes.items() if ('|c_acc|cert' in k or '|c_accs|cert' in k) and k.endswith('|local'))
            obs_local_half = sum(n for k, n in routes.items() if ('|c_acc|half' in k or '|c_accs|half' in k or '|accepter|half' in k) and k.endswith('|local'))
            out['%s|%s|ph=%g' % (arm, kind, phk)] = dict(n=len(rs), fair30=float(f30), fair120=float(f120), fair240=float(f240),
                                                       fair120_ci=boot([e['fair120'] for e in ex]), hazard_UF=(nUF / occ if occ else None), n_UF=nUF,
                                                       routes=routes, routes_lasted=lasted, pacing=pace,
                                                       observed_local_Rc_routes_cert=obs_local_cert, observed_local_Rc_routes_half=obs_local_half,
                                                       mlog_overflow=sum(1 for r in rs if r.get('mlog_overflow')), src=c['src'])
    return out


def main(outj, outmd):
    cs = build()
    rep = {}
    Lx = ['# Queue 79 step 2 (approach-rate statistics at finite N, I = 64, 120N; mN = 1, Λ = 100; not π)', '',
          'Stored controls: F (queue 75), FR and FOR (queue 78), all with simulating bullies only (φ = 0 by construction).', '']
    arms_main = [('F', 0.0), ('FR', 0.0), ('FOR', 0.0), ('Fc', 0.5), ('FcOc', 0.5), ('FcOcRc', 0.5), ('FcRc', 0.5), ('mix', 0.5)]
    for N in (100, 200, 400):
        for b in (0.0, 1.0, 3.0):
            Lx += vtable(cs, arms_main + ([('FcOcRcs', 0.5), ('FcOcC3', 0.5), ('Fcs', 0.5), ('PcOcRc', 0.5)] if N == 200 else []), b, N)
    Lx.append('φ comparison (N = 200): FcOcRc and Fc at φ = 0, 1/2, 1 against the stored simulating controls')
    Lx.append('')
    for b in (1.0, 3.0):
        Lx += vtable(cs, [('F', 0.0), ('FOR', 0.0), ('FR', 0.0), ('Fc', 0.0), ('Fc', 0.5), ('Fc', 1.0), ('FcOcRc', 0.0), ('FcOcRc', 0.5), ('FcOcRc', 1.0)], b, 200)
    dst = {}
    for key in sorted({(k[0], k[1], k[2], k[3], k[4]) for k in cs if k[6] == '' and not k[7]}):
        ds = delta_star(cs, *key)
        if ds['status'] != 'incomplete':
            dst['%s|b=%g|ph=%g|N=%d|I=%d' % key] = ds
    rep['delta_star'] = dst
    Lx.append('δ\\* (V\\* ≥ 0.9 at that grid δ and every larger one): ' + '; '.join('%s %s' % (k, ds_str(v)) for k, v in sorted(dst.items())))
    Lx.append('')
    sd = seeded(cs)
    rep['seeded'] = sd
    Lx += ['Seeded starts (N = 200, I = 64, δ = 0.03, β = 3; to 240N; fair share pooled over runs; exits = debounced unequal-to-fair flips, transient included)', '',
           '| arm | start | φ | fair 30N | fair 120N [95%] | fair 240N | U→F hazard (per unequal island-gen) | exits | local Rc routes (cert / ½-const) | routes (top) |',
           '|---|---|---|---|---|---|---|---|---|---|']
    for k, v in sd.items():
        arm, kind, ph = k.split('|')
        top = dict(sorted(v['routes'].items(), key=lambda x: -x[1])[:5])
        Lx.append('| %s | %s | %s | %.3f | %.3f [%s, %s] | %.3f | %s | %d | %d / %d | %s |' % (
            arm, kind, ph[3:], v['fair30'], v['fair120'], *(('%.3f' % x) if x is not None else '-' for x in v['fair120_ci']), v['fair240'],
            ('%.2e' % v['hazard_UF']) if v['hazard_UF'] is not None else '-', v['n_UF'], v['observed_local_Rc_routes_cert'], v['observed_local_Rc_routes_half'], top))
    Lx.append('')
    Lx += ['Pacing against scramble (seeded starts with pacing records; sums over 20 runs × 64 islands):', '',
           '| arm | start | φ | Rc victim-seat exposure (island-gens) | R exposure | Rc into v: arrivals / Σρ / fixed (no active offerer) | second steps: arrivals / Σρ (predicted completions) | observed local Rc routes (cert) | unequal exits / censored | e-arrivals with Rc resident (kind: n / Σρ / fixed) |',
           '|---|---|---|---|---|---|---|---|---|---|']
    for k, v in sd.items():
        p = v['pacing']
        if not p:
            continue
        arm, kind, ph = k.split('|')
        ea = {kk: '%d/%.2f/%d' % tuple(x) for kk, x in sorted(p['e_arr'].items(), key=lambda x: -x[1][0])[:6]}
        first = [x for kk, x in p['v_arr'].items() if kk.startswith(('c_acc|', 'c_accs|')) and not kk.endswith('|cert')]
        fa = [sum(x[0] for x in first), sum(x[1] for x in first), sum(x[2] for x in first)]
        Lx.append('| %s | %s | %s | %d | %d | %d / %.2f / %d | %d / %.2f | %d | %d / %d | %s |' % (
            arm, kind, ph[3:], p['acc_expo'], p['accR_expo'], fa[0], fa[1], fa[2], p['n_second'], p['pred_second'], v['observed_local_Rc_routes_cert'],
            p['unequal_exits'], p['unequal_censored'], ea))
    Lx.append('')
    # main-arm pacing (non-seeded cells): pooled per (beta, N)
    mp = {}
    for key, c in cs.items():
        if key[0] != 'FcOcRc' or key[6] != '' or key[7] or key[2] != 0.5 or key[4] != 64:
            continue
        for r in c['_rows']:
            p = r.get('pacing')
            if not p:
                continue
            e = mp.setdefault('b=%g|N=%d' % (key[1], key[3]), dict(acc_expo=0, pred_second=0.0, n_second=0, pred_first=0.0, n_first=0, rr={}))
            e['acc_expo'] += p['acc_expo']; e['pred_second'] += p['pred_second']; e['n_second'] += p['n_second']
            e['pred_first'] += p['pred_first']; e['n_first'] += p['n_first']
            for kk, n in (r.get('rroutes') or {}).items():
                e['rr'][kk] = e['rr'].get(kk, 0) + n
    for e in mp.values():
        e['observed_local_cert'] = sum(n for kk, n in e['rr'].items() if kk.startswith('Rroute|c_acc|cert|local'))
    rep['main_pacing'] = mp
    Lx += ['Main arm (FcOcRc, φ = 1/2, I = 64) pacing pooled over δ and runs:', '', '| cell | Rc victim exposure | first steps n / Σρ | second steps n / Σρ (predicted) | observed local Rc routes (cert) | all Rc-route exits by kind |', '|---|---|---|---|---|---|']
    for k in sorted(mp):
        e = mp[k]
        Lx.append('| %s | %d | %d / %.2f | %d / %.2f | %d | %s |' % (k, e['acc_expo'], e['n_first'], e['pred_first'], e['n_second'], e['pred_second'], e['observed_local_cert'],
                                                         {kk: n for kk, n in e['rr'].items() if kk.startswith('Rroute')}))
    Lx.append('')
    # scramble
    scr = {}
    for key, c in cs.items():
        if key[6] == '' and not key[7] and key[4] == 64 and key[2] in (0.5, 0.0) and c['scramble_same_class'] is not None:
            scr['%s|b=%g|ph=%g|N=%d|d=%g' % (key[0], key[1], key[2], key[3], key[5])] = c['scramble_same_class']
    rep['scramble_same_class'] = scr
    comp = {}
    for arm in ('FcOcRc', 'Fc'):
        c = get(cs, arm, 3.0, 0.5, 200, 64, 0.03)
        if c:
            cc = {}
            for r in c['_rows']:
                for k, n in r['scramble']['unequal30_holder_victim'].items():
                    cc[k] = cc.get(k, 0) + n
            comp[arm] = dict(same_class=c['scramble_same_class'], unequal30=cc)
    rep['scramble_diag'] = comp
    Lx.append('Scramble diagnostic (β = 3, N = 200, δ = 0.03, φ = 1/2): share of islands whose 120N modal class equals the 30N one, and the '
              '(2/3 holder | victim) composition of unequal islands at 30N: %s' % json.dumps(comp))
    Lx.append('')
    pooled = [v for k, v in scr.items() if k.startswith('FcOcRc|b=3|ph=0.5|')]
    rep['RE8_pooled_main_b3'] = float(np.mean(pooled)) if pooled else None
    Lx.append('Main arm, β = 3, φ = 1/2, all δ and N: mean same-class share %s' % rep['RE8_pooled_main_b3'])
    Lx.append('')
    # holders and charges at the main grid's reference cell
    hc = {}
    for key, c in cs.items():
        if key[6] == '' and not key[7] and key[3] == 200 and key[4] == 64 and key[5] in (0.03, 0.1):
            hc['%s|b=%g|ph=%g|d=%g' % (key[0], key[1], key[2], key[5])] = dict(hold=c['hold'], charges=c['charges'], fair_pair_islands=c['fair_pair_islands'],
                                                                             consensus_pairs=c['consensus_pairs'], unequal_consensus=c['unequal_consensus'])
    rep['holders_charges'] = hc
    rep['cells'] = {json.dumps([str(x) for x in k]): {kk: vv for kk, vv in v.items() if kk != '_rows'} for k, v in cs.items()}
    json.dump(rep, open(outj, 'w'), default=str)
    Lx.append('Holders (120N majority holders per slot, summed over runs), charges and fair-pair distribution at N = 200, δ ∈ {0.03, 0.1}: in the JSON '
              '(`holders_charges`).')
    open(outmd, 'w').write('\n'.join(Lx) + '\n')
    return rep


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
