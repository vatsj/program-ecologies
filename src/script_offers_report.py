"""Queue 80: step-2 aggregation, tables with bootstrap intervals, and the registered verdicts.

    python3 src/script_offers_report.py OUTDIR      # reads runs/sco_rows/*/rows_*.jsonl, stored queue 75/78 rows; writes
                                                    # OUTDIR/step2.json, OUTDIR/step2_report.md, runs/script-checked-offers.json
"""
import os, sys, json, glob
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DELTAS = [0.1, 0.03, 0.01, 0.003, 0.001]
BULLY = ('s_bully', 'k_bully')


def load(pattern):
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, pattern))):     # sorted: zz_seedfix (the refined route classifier) overrides
        for line in open(f):
            line = line.strip()
            if line:
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                out[r['id']] = r
    return out


def key_of(r):
    kv = dict(p.split('=') for p in r['spec'].split(':')[1:])
    return (kv['arm'], float(kv['b']), float(kv.get('ph', 0.5)), r['N'], float(kv['d']), kv.get('seed'))


def boot(x, B=2000, seed=0):
    x = np.asarray(x, float)
    if len(x) == 0:
        return (None, None)
    rng = np.random.default_rng(seed)
    m = x[rng.integers(0, len(x), (B, len(x)))].mean(1)
    return (round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3))


def dstar(vs):
    """smallest grid delta with V* >= 0.9 there and at every larger delta; None if none."""
    best = None
    for d in DELTAS:
        if vs.get(d) is not None and vs[d] >= 0.9:
            best = d
        else:
            break
    return best


def step(a, b):
    """grid steps from a to b (positive: b smaller delta)."""
    return DELTAS.index(b) - DELTAS.index(a)


def aggregate(rows):
    cells = {}
    for r in rows.values():
        k = key_of(r)
        cells.setdefault(k, []).append(r)
    agg = {}
    for k, rs in cells.items():
        v = [x['vstar'] for x in rs]
        e = dict(n=len(rs), vstar=round(float(np.mean(v)), 4), ci=boot(v), unequal_cons=sum(1 for x in rs if x['cons_modal']['unequal'] >= 0),
                 fair_cons=sum(1 for x in rs if x['cons_modal']['fair_pair'] >= 0),
                 same_class=round(float(np.mean([x['scramble']['same_class'] for x in rs])), 4),
                 charges=round(float(np.mean([x['charges']['120N']['all'] for x in rs])), 5))
        pair_bc = excl_bc = pair_tot = excl_tot = 0
        partner = {}
        hold = {}
        bc23 = sb23 = 0
        isl = 0
        for x in rs:
            o = x['occ120']
            isl += o['fair'] + o['unequal'] + 0
            bc23 += o['bc_on_23']; sb23 += o['sb_on_23']
            for kk, n in o['hold'].items():
                role, fam, sp = kk.split('|')
                hold[kk] = hold.get(kk, 0) + n
                if role == 'pair':
                    pair_tot += n; pair_bc += n if fam in BULLY else 0
                else:
                    excl_tot += n; excl_bc += n if fam in BULLY else 0
            for kk, n in o['bc_pair_partner'].items():
                partner[kk] = partner.get(kk, 0) + n
        nisl = 64 * len(rs)
        e.update(bc_pair_share=round(pair_bc / pair_tot, 4) if pair_tot else None, bc_excl_share=round(excl_bc / excl_tot, 4) if excl_tot else None,
                 bc_pair_partner=partner, bc_on_23_share=round(bc23 / nisl, 4), sb_on_23_share=round(sb23 / nisl, 4), hold=hold,
                 pair_slots=pair_tot)
        if rs[0].get('pacing'):
            P = [x['pacing'] for x in rs]
            e['pacing'] = dict(pred_second=round(sum(p['pred_second'] for p in P), 4), n_second=sum(p['n_second'] for p in P),
                               pred_first=round(sum(p['pred_first'] for p in P), 4), n_first=sum(p['n_first'] for p in P),
                               observed_routes=sum(p['observed_routes'] for p in P), n_UF=sum(p['n_UF'] for p in P),
                               observed_local_cert=sum(p.get('observed_local_cert', 0) for p in P) if all('observed_local_cert' in p for p in P) else None,
                               routes_by_kind={k: sum(p.get('observed_routes_by_kind', {}).get(k, 0) for p in P)
                                               for k in sorted({kk for p in P for kk in p.get('observed_routes_by_kind', {})})},
                               occ_U=sum(p['occ_U'] for p in P), acc_expo=sum(p['acc_expo'] for p in P))
            e['fair240'] = round(float(np.mean([x['snap240']['cls_modal'][0] / 64 for x in rs])), 4)
        agg[k] = e
    return agg


def row(agg, arm, b, ph, N=200, seed=None):
    return {d: (agg.get((arm, b, ph, N, d, seed)) or {}).get('vstar') for d in DELTAS}


def dmean(vs):
    xs = [v for v in vs.values() if v is not None]
    return round(float(np.mean(xs)), 4) if len(xs) == 5 else None


def stored_rows():
    """queue 75's F and queue 78's FR at the old fuel, by (arm, beta, N, delta): mean V* over runs."""
    q75 = load('runs/lpt_rows/*/rows_*.jsonl'); q78 = load('runs/pa_rows/*/rows_*.jsonl')
    out = {}
    for src, arm, pref in ((q75, 'UF', '2a|2a:'), (q78, 'UFR', 'main|pa:arm=FR:')):
        acc = {}
        for jid, r in src.items():
            if not jid.startswith(pref):
                continue
            s = jid.split('|')
            if s[3] != '64' or s[5] != '0':
                continue
            kv = dict(p.split('=') for p in s[1].split(':')[1:])
            if pref.startswith('main') and kv.get('g', '1.0') != '1.0':
                continue
            acc.setdefault((arm, float(kv['b']), int(s[2]), float(kv['d'])), []).append(r['vstar'])
        for k, v in acc.items():
            out[k] = round(float(np.mean(v)), 4)
    return out


def main(outdir):
    rows = load('runs/sco_rows/*/rows_*.jsonl')
    rows = {k: v for k, v in rows.items() if v['series'] not in ('pilot', 'v1')}
    agg = aggregate(rows)
    st = stored_rows()
    os.makedirs(outdir, exist_ok=True)
    json.dump({'|'.join(map(str, k)): v for k, v in agg.items()}, open(os.path.join(outdir, 'step2.json'), 'w'), indent=1)
    return agg, st


def fmtd(d):
    return '–' if d is None else ('%g' % d)


def score(agg, st, step0=None, step1=None):
    V = {}
    def R(arm, b, ph, N=200):
        return row(agg, arm, b, ph, N)
    # RE 2
    out = {}
    u = {}
    ok = True; fal = False
    for arm in ('UF', 'UFR'):
        for b in (1.0, 3.0):
            ds = dstar(R(arm, b, 0.0))
            u['%s b%g dstar' % (arm, b)] = ds
            ok &= ds is None
            if b == 3.0 and ds is not None:
                fal = True
        new = dmean(R(arm, 3.0, 0.0))
        old = dmean({d: st.get((arm, 3.0, 200, d)) for d in DELTAS})
        u['%s b3 dmean new / old' % arm] = (new, old)
        ok &= new is not None and old is not None and abs(new - old) < 0.15
    V['RE 2'] = dict(holds=bool(ok), falsifier=fal, detail=u)
    # RE 3
    d = {}
    a0, a5 = dstar(R('A1', 3.0, 0.0)), dstar(R('A1', 3.0, 0.5))
    k0, k5 = dstar(R('K', 3.0, 0.0)), dstar(R('K', 3.0, 0.5))
    d.update(A1_phi0=a0, A1_phi05=a5, K_phi0=k0, K_phi05=k5)
    ok = (a0 is not None and a0 <= 0.03 and a5 is not None and a5 <= 0.01 and k0 is not None and k5 is not None
          and abs(step(a0, k0)) <= 1 and abs(step(a5, k5)) <= 1)
    V['RE 3'] = dict(holds=bool(ok), falsifier=a5 is None, detail=d)
    # RE 4
    d = {}; ok = True; fal = False
    for ph in (0.0, 0.5):
        a1, a2 = dmean(R('A1', 3.0, ph)), dmean(R('A2', 3.0, ph))
        d['phi %g A1 / A2' % ph] = (a1, a2)
        ok &= a1 is not None and a2 is not None and abs(a2 - a1) <= 0.1
        fal |= a1 is not None and a2 is not None and a2 < a1 - 0.2
    V['RE 4'] = dict(holds=bool(ok), falsifier=bool(fal), detail=d)
    # RE 5
    k2, a2 = dmean(R('K2', 3.0, 0.0)), dmean(R('A2', 3.0, 0.0))
    V['RE 5'] = dict(holds=bool(k2 is not None and a2 is not None and k2 <= a2 - 0.2), falsifier=bool(k2 is not None and a2 is not None and abs(k2 - a2) <= 0.1),
                     detail=dict(K2=k2, A2=a2))
    # RE 6
    d = {}; ok = True
    for ph in (0.0, 0.5):
        l, h = dstar(R('A2', 3.0, ph, 100)), dstar(R('A2', 3.0, ph, 400))
        d['phi %g N100 / N400' % ph] = (l, h)
        ok &= l is not None and h is not None and step(l, h) <= 1
    V['RE 6'] = dict(holds=bool(ok), falsifier=None, detail=d)
    # RE 7
    d = {}; ok = True; fal = False
    for b in (1.0, 3.0):
        a3, a2 = dmean(R('A3', b, 0.5)), dmean(R('A2', b, 0.5))
        d['b%g A3 / A2' % b] = (a3, a2)
        ok &= a3 is not None and a2 is not None and abs(a3 - a2) <= 0.1
        fal |= a3 is not None and a2 is not None and a3 < a2 - 0.2
    V['RE 7'] = dict(holds=bool(ok), falsifier=bool(fal), detail=d)
    # RE 8
    def pooled_share(arm):
        num = den = 0
        for dd in DELTAS:
            e = agg.get((arm, 3.0, 0.5, 200, dd, None))
            if e and e['bc_pair_share'] is not None:
                num += e['bc_pair_share'] * e['pair_slots']; den += e['pair_slots']
        return num / den if den else None
    s4, s2 = pooled_share('A4'), pooled_share('A2')
    v4, v2 = R('A4', 3.0, 0.5)[0.003], R('A2', 3.0, 0.5)[0.003]
    c1 = s4 is not None and s2 is not None and s4 <= s2 - 0.15 and s4 > 0.2
    c2 = v4 is not None and v2 is not None and v4 <= v2 - 0.1
    V['RE 8'] = dict(holds=bool(c1 and c2), clause1=bool(c1), clause2=bool(c2),
                     falsifier=bool((s4 is not None and s2 is not None and s4 >= s2) or (v4 is not None and v2 is not None and v4 >= v2)),
                     detail=dict(bc_paired_share_A4=s4, bc_paired_share_A2=s2, vstar_A4_0003=v4, vstar_A2_0003=v2))
    # RE 9
    e = agg.get(('A2', 3.0, 0.5, 200, 0.03, 'unequal'))
    if e:
        f = e['fair240']; p = e['pacing']; pr, ob = p['pred_second'], p['observed_local_cert']
        within = ob is not None and ((pr == 0 and ob == 0) or (pr > 0 and ob > 0 and max(pr / ob, ob / pr) <= 3))
        V['RE 9'] = dict(holds=bool(f <= 0.15 and within), falsifier=bool(f >= 0.3), detail=dict(fair240=f, pred_second=pr, observed=ob, pacing=p))
    # RE 12
    def partner_share(arm):
        tot = bc = 0
        for dd in DELTAS:
            e = agg.get((arm, 3.0, 0.5, 200, dd, None))
            if e:
                for k, n in e['bc_pair_partner'].items():
                    tot += n; bc += n if k in BULLY else 0
        return bc / tot if tot else None
    ps = partner_share('A5')
    c2 = all((agg.get(('A5', 3.0, 0.5, 200, dd, None)) or {}).get('bc_on_23_share', -1) > (agg.get(('A2', 3.0, 0.5, 200, dd, None)) or {}).get('bc_on_23_share', 9)
             for dd in (0.01, 0.003, 0.001))
    V['RE 12'] = dict(holds=bool(ps is not None and ps >= 0.9 and c2), falsifier=bool(ps is not None and ps < 0.6),
                      detail=dict(bc_partnered_share=ps, bc_on_23=[((agg.get(('A5', 3.0, 0.5, 200, dd, None)) or {}).get('bc_on_23_share'),
                                                                     (agg.get(('A2', 3.0, 0.5, 200, dd, None)) or {}).get('bc_on_23_share')) for dd in DELTAS]))
    return V


def tables_md(agg, st):
    L = ['| arm (phi) | beta | ' + ' | '.join('d=%g' % d for d in DELTAS) + ' | δ* | δ-mean |', '|---|---|' + '---|' * 7]
    order = [('UF', 0.0), ('UFR', 0.0), ('K', 0.0), ('K', 0.5), ('K2', 0.0), ('K2', 0.5), ('A1', 0.0), ('A1', 0.5), ('A2', 0.0), ('A2', 0.5),
             ('A3', 0.5), ('A3', 1.0), ('A4', 0.0), ('A4', 0.5), ('A4', 1.0), ('A5', 0.5)]
    for b in (0.0, 1.0, 3.0):
        for arm, ph in order:
            r = row(agg, arm, b if b else 0.0, ph if b else (0.0 if arm in ('UF', 'UFR') else 0.5))
            if all(v is None for v in r.values()):
                continue
            if b == 0.0 and ph not in ((0.0,) if arm in ('UF', 'UFR') else (0.5,)):
                continue
            cis = [(agg.get((arm, b, ph if b else (0.0 if arm in ('UF', 'UFR') else 0.5), 200, d, None)) or {}).get('ci') for d in DELTAS]
            cells = ['%.2f [%s–%s]' % (r[d], ci[0], ci[1]) if r[d] is not None and ci else '–' for d, ci in zip(DELTAS, cis)]
            L.append('| %s (%g) | %g | %s | %s | %s |' % (arm, ph, b, ' | '.join(cells), fmtd(dstar(r)), dmean(r)))
    for arm in ('UF', 'UFR'):
        for b in (0.0, 1.0, 3.0):
            o = {d: st.get((arm, b, 200, d)) for d in DELTAS}
            L.append('| %s stored old fuel | %g | %s | %s | %s |' % (arm, b, ' | '.join('%.2f' % o[d] if o[d] is not None else '–' for d in DELTAS), fmtd(dstar(o)), dmean(o)))
    for arm in ('A1', 'A2'):
        for N in (100, 400):
            for ph in (0.0, 0.5):
                r = row(agg, arm, 3.0, ph, N)
                if all(v is None for v in r.values()):
                    continue
                L.append('| %s N=%d (%g) | 3 | %s | %s | %s |' % (arm, N, ph, ' | '.join('%.2f' % r[d] if r[d] is not None else '–' for d in DELTAS), fmtd(dstar(r)), dmean(r)))
    return '\n'.join(L)


if __name__ == '__main__':
    agg, st = main(sys.argv[1])
    V = score(agg, st)
    json.dump(V, open(os.path.join(sys.argv[1], 'verdicts_step2.json'), 'w'), indent=1, default=str)
    open(os.path.join(sys.argv[1], 'step2_tables.md'), 'w').write(tables_md(agg, st) + '\n')
    print(len(agg), 'cells'); print(json.dumps(V, indent=1, default=str)[:3000])
