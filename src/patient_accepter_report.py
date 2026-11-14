"""Step 2 report of queue 78 (spec specs/2026-11-14-patient-accepters.md): aggregates runs/pa_rows/* (and queue 75's stored F-arm rows of
runs/lpt_rows/*, the F control) into cells, threshold tables, controls, the seeded starts with their exit classification, the
length-prior-shaped series and the verdict inputs.

    python3 src/patient_accepter_report.py OUT.json OUT.md
"""
import os, sys, json, glob
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import patient_accepter_run as PRR
import length_prior_t_run as LR

DELTAS = [1e-1, 3e-2, 1e-2, 3e-3, 1e-3]
DELTAS_LP = [1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4]
FAMN = None


def spec_key(row):
    s = row['spec']; parts = s.split(':')
    kv = {p.split('=')[0]: p.split('=')[1] for p in parts[1:] if '=' in p}
    if parts[0] == '2a':
        return ('F', float(kv['b']), float(kv['d']), 1.0, '')
    if parts[0] == 'pa':
        g = float(kv.get('g', 1.0))
        ex = ''.join(':%s=%s' % (k, kv[k]) for k in ('seed',) if k in kv)
        return (kv['arm'], float(kv['b']), float(kv['d']), g, ex)
    if parts[0] == 'lp':
        return ('lp:%s:%s' % (parts[1], parts[2]), None, float(kv['d']), 1.0, '')
    raise ValueError(s)


def load():
    rows = {}
    for d in glob.glob(os.path.join(ROOT, 'runs', 'pa_rows', '*')):
        rows.update(PRR.load_rows(d))
    stored = {}
    for d in glob.glob(os.path.join(ROOT, 'runs', 'lpt_rows', '*')):
        stored.update(LR.load_rows(d))
    return rows, stored


def boot(x, B=2000, seed=0):
    x = np.asarray(x, float)
    if len(x) == 0:
        return (None, None)
    rng = np.random.default_rng(seed)
    m = x[rng.integers(0, len(x), (B, len(x)))].mean(1)
    return (float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5)))


def cell_stats(rs):
    v = np.array([r['vstar'] for r in rs])
    lo, hi = boot(v)
    pairs = np.zeros(3)
    for r in rs:
        pairs += np.array(r['snap120']['pair_modal'], float)
    fp = [int(r['cons_modal']['fair_pair']) for r in rs]
    un = int(sum(1 for r in rs if r['cons_modal']['unequal'] >= 0))
    tr = {}
    for win in ('tail|dq', 'chase|dq', 'tail|d25', 'chase|d25'):
        M = np.zeros((5, 5)); occ = np.zeros(5); ff = 0
        for r in rs:
            t = r['trans'].get(win)
            if t is None:
                continue
            M += np.array(t['M']); occ += np.array(t['occ']); ff += t['ff']
        tr[win] = dict(F_to_U=float(M[0, 1] / occ[0]) if occ[0] else None, U_to_F=float(M[1, 0] / occ[1]) if occ[1] else None,
                       n_FU=int(M[0, 1]), n_UF=int(M[1, 0]), occ_F=float(occ[0]), occ_U=float(occ[1]))
    ch = {}
    for r in rs:
        c = (r.get('charges') or {}).get('120N')
        if not c:
            continue
        for f, x in c.items():
            if f != 'all' and x[0] is not None and x[1] > 0:
                ch.setdefault(f, []).append((x[0], x[1]))
    chm = {f: float(sum(a * b for a, b in l) / sum(b for a, b in l)) for f, l in ch.items()}
    hold = {'F': {}, 'U': {}}
    for r in rs:
        for lab in ('F', 'U'):
            for f, n in r['snap120']['hold'][lab].items():
                hold[lab][f] = hold[lab].get(f, 0) + n
    rm = [r['rmeas']['120N'] for r in rs if r.get('rmeas')]
    nU = sum(x['unequal'] for x in rm); nUR = sum(x['unequal_R_victim'] for x in rm)
    dd = [x['mean_R_minus_C13'] for x in rm if x['mean_R_minus_C13'] is not None]
    return dict(n=len(rs), mean=float(v.mean()), ci=[lo, hi], all_fair=float((v >= 1.0 - 1e-9).mean()),
                fair_pair_islands=(pairs / max(pairs.sum(), 1)).tolist(), consensus_pairs=[fp.count(i) for i in (0, 1, 2)], unequal_consensus=un,
                trans=tr, charges=chm, hold=hold, R_victim_share=(nUR / nU if nU else None), R_victim_counts=[nUR, nU],
                R_minus_C13=(float(np.mean(dd)) if dd else None), R_minus_C13_n=len(dd), v_by_run=[float(x) for x in v])


def build():
    rows, stored = load()
    cells = {}
    for src, rr in (('pa', rows), ('q75', stored)):
        for jid, r in rr.items():
            if src == 'q75' and (not jid.startswith('2a|') or ':s1' in r['spec']):
                continue
            if src == 'pa' and r['series'] in ('v1', 'test'):
                continue
            k = spec_key(r)
            if src == 'q75' and k[1] not in (0.0, 1.0, 3.0):
                continue
            key = (k[0], k[1], r['N'], r['I'], k[2], k[3], k[4], bool(r['long']))
            cells.setdefault(key, {})[r['r']] = r
    out = {}
    for key, d in cells.items():
        out[key] = cell_stats([d[r] for r in sorted(d)])
        out[key]['_rows'] = [d[r] for r in sorted(d)]
    return out, rows, stored


def get(cs, arm, beta, N, I, d, g=1.0, ex='', long=False):
    return cs.get((arm, beta, N, I, d, g, ex, long))


def delta_star(cs, arm, beta, N, I, g=1.0, deltas=DELTAS, thr=0.9):
    means = {}
    for d in deltas:
        c = get(cs, arm, beta, N, I, d, g)
        means[d] = c['mean'] if c else None
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
    return '%.2f [%.2f, %.2f]' % (c['mean'], c['ci'][0], c['ci'][1])


def vtable(cs, arms, beta, N, I, g=1.0, deltas=DELTAS, label=None):
    Lx = ['%s: V\\* at 120N (mean over runs [95%% bootstrap]), by δ' % (label or 'N = %d, I = %d, β = %g, γ = %g' % (N, I, beta, g)), '',
          '| arm | ' + ' | '.join('%g' % d for d in deltas) + ' | δ\\* |', '|---|' + '---|' * (len(deltas) + 1)]
    for arm in arms:
        gg = g if arm in ('FR', 'FOR', 'FC') else 1.0
        cells = [get(cs, arm, beta, N, I, d, gg) for d in deltas]
        if not any(cells):
            continue
        Lx.append('| %s | ' % arm + ' | '.join(fmtc(c) for c in cells) + ' | %s |' % ds_str(delta_star(cs, arm, beta, N, I, gg, deltas)))
    Lx.append('')
    return Lx


def seeded(cs, rows):
    """seeded starts: fraction of islands fair at 30N, 120N, 240N (pooled over runs), the unequal exit hazard, exit routes."""
    out = {}
    for arm in ('F', 'FR', 'FOR', 'FC', 'R'):
        for kind in ('unequal', 'fair'):
            g = 1.0
            c = get(cs, arm, 3.0, 200, 64, 0.03, g, ':seed=%s' % kind, True)
            if not c:
                continue
            rs = c['_rows']
            f30 = np.mean([r['exits']['fair30'] for r in rs]); f120 = np.mean([r['exits']['fair120'] for r in rs])
            f240 = np.mean([r['exits']['fair_end'] for r in rs])
            hz = [r['exits']['hazard'] for r in rs]
            nUF = sum(h['toend']['n_UF'] for h in hz); occ = sum(h['toend']['occ_U'] for h in hz)
            nUF120 = sum(h['to120N']['n_UF'] for h in hz); occ120 = sum(h['to120N']['occ_U'] for h in hz)
            routes = {}; lasted = {}; pairs = {}; pairs_lasted = {}
            exl = []
            for r in rs:
                for e in r['exits']['exits']:
                    routes[e['route']] = routes.get(e['route'], 0) + 1
                    k = '+'.join(e['pair_fams']) if e['pair_fams'] else '-'
                    pairs[k] = pairs.get(k, 0) + 1
                    if e['lasted_to_120N']:
                        lasted[e['route']] = lasted.get(e['route'], 0) + 1
                        pairs_lasted[k] = pairs_lasted.get(k, 0) + 1
                        exl.append(dict(run=r['r'], **{x: e[x] for x in ('island', 'g', 'route', 'pair', 'seq', 'unequal_triple', 'fair_triple')}))
            f120_by_run = [r['exits']['fair120'] for r in rs]
            out['%s|%s' % (arm, kind)] = dict(n=len(rs), fair30=float(f30), fair120=float(f120), fair240=float(f240), fair120_ci=boot(f120_by_run),
                                              hazard_UF_toend=(nUF / occ if occ else None), n_UF=nUF, hazard_UF_to120N=(nUF120 / occ120 if occ120 else None),
                                              routes=routes, routes_lasted=lasted, pair_fams=pairs, pair_fams_lasted=pairs_lasted, lasting_exits=exl[:60],
                                              n_lasting=len(exl), mlog_overflow=sum(1 for r in rs if r['exits']['mlog_rows'] > r['exits']['mlog_cap']),
                                              R_victim=c['R_victim_counts'], R_minus_C13=c['R_minus_C13'])
    return out


def lps(cs):
    out = {}
    for key, c in cs.items():
        if not str(key[0]).startswith('lp:'):
            continue
        out['%s|N=%d|d=%g' % (key[0], key[2], key[4])] = dict(mean=c['mean'], ci=c['ci'], all_fair=c['all_fair'], unequal_consensus=c['unequal_consensus'])
    return out


def main(outj, outmd):
    cs, rows, stored = build()
    rep = {}
    Lx = ['# Queue 78 step 2 (approach-rate statistics at finite N, I, 120N; not π)', '']
    main_arms = ['F', 'FR', 'FOR', 'FC', 'R', 'FRs']
    for N in (100, 200, 400):
        for b in (1.0, 3.0):
            Lx += vtable(cs, main_arms, b, N, 64)
    for g in (0.3, 3.0):
        for b in (1.0, 3.0):
            Lx += vtable(cs, ['F', 'FR', 'FOR', 'FC'], b, 200, 64, g)
    for b in (1.0, 3.0):
        Lx += vtable(cs, ['F', 'FR'], b, 200, 256)
    Lx += vtable(cs, ['F', 'FR'], 0.0, 200, 64)
    # threshold table
    dst = {}
    for arm in main_arms:
        for b in (0.0, 1.0, 3.0):
            for N in (100, 200, 400):
                for I in (64, 256):
                    for g in (0.3, 1.0, 3.0):
                        gg = g if arm in ('FR', 'FOR', 'FC') else 1.0
                        if gg != g:
                            continue
                        ds = delta_star(cs, arm, b, N, I, gg)
                        if ds['status'] != 'incomplete':
                            dst['%s|b=%g|N=%d|I=%d|g=%g' % (arm, b, N, I, gg)] = ds
    rep['delta_star'] = dst
    Lx.append('δ\\* (full definition: V\\* ≥ 0.9 at that grid δ and every larger one): ' + '; '.join('%s %s' % (k, ds_str(v)) for k, v in sorted(dst.items())))
    Lx.append('')
    # seeded starts
    sd = seeded(cs, rows)
    rep['seeded'] = sd
    Lx.append('Seeded starts (N = 200, I = 64, δ = 0.03, β = 3; islands fair, pooled over 20 runs; exits = debounced unequal-to-fair flips, transient included)')
    Lx.append('')
    Lx.append('| arm | start | fair 30N | fair 120N [95%] | fair 240N | U->F hazard (per unequal island-gen, to 240N) | exits (lasting to 120N) | routes | routes of lasting exits | new pair families (lasting) |')
    Lx.append('|---|---|---|---|---|---|---|---|---|---|')
    for k, v in sd.items():
        arm, kind = k.split('|')
        Lx.append('| %s | %s | %.3f | %.3f [%s, %s] | %.3f | %s | %d (%d) | %s | %s | %s |' % (
            arm, kind, v['fair30'], v['fair120'], *(('%.3f' % x) if x is not None else '-' for x in v['fair120_ci']), v['fair240'],
            ('%.2e' % v['hazard_UF_toend']) if v['hazard_UF_toend'] is not None else '-', v['n_UF'], v['n_lasting'], v['routes'], v['routes_lasted'], v['pair_fams_lasted']))
    Lx.append('')
    # R measures and holders on the main grid
    rm = {}
    for key, c in cs.items():
        if key[0] in ('FR', 'FOR', 'R', 'FRs') and key[6] == '' and not key[7]:
            rm['%s|b=%g|N=%d|I=%d|d=%g|g=%g' % (key[0], key[1], key[2], key[3], key[4], key[5])] = dict(R_victim_share=c['R_victim_share'], R_victim_counts=c['R_victim_counts'],
                                                                                                  R_minus_C13=c['R_minus_C13'], n=c['R_minus_C13_n'], charges=c['charges'], hold=c['hold'])
    rep['R_measures'] = rm
    rep['lps'] = lps(cs)
    if rep['lps']:
        Lx.append('Length-prior-shaped series: V\\* at 120N')
        Lx.append('')
        for k in sorted(rep['lps']):
            v = rep['lps'][k]
            Lx.append('- %s: %.2f [%.2f, %.2f]' % (k, v['mean'], v['ci'][0], v['ci'][1]))
        Lx.append('')
    rep['cells'] = {json.dumps([str(x) for x in k]): {kk: vv for kk, vv in v.items() if kk != '_rows'} for k, v in cs.items()}
    json.dump(rep, open(outj, 'w'), default=str)
    open(outmd, 'w').write('\n'.join(Lx) + '\n')
    print('\n'.join(Lx[:12]))
    return rep


def v1_check():
    rows, stored = load()
    n = same = 0; bad = []
    for jid_, r in rows.items():
        if r['series'] != 'v1':
            continue
        spec = r['spec'].replace('pa:arm=F:', '2a:')
        old = stored.get('2a|%s|%d|%d|%d|0' % (spec, r['N'], r['I'], r['r']))
        if old is None:
            continue
        n += 1
        ok = (r['vshare_ts'] == old['vshare_ts'] and r['snap120']['cls_modal'] == old['snap120']['cls_modal'] and r['snap120']['pair_modal'] == old['snap120']['pair_modal']
              and r['cons_modal'] == old['cons_modal'] and r['trans'] == old['trans'])
        same += ok
        if not ok:
            bad.append(jid_)
    return dict(compared=n, identical=same, mismatches=bad[:10])


if __name__ == '__main__':
    if sys.argv[1] == 'v1':
        print(v1_check())
    else:
        main(sys.argv[1], sys.argv[2])
