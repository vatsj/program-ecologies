"""Verdicts of queue 79 (predictions/2026-11-15-certified-offers.md) from the gates, step 0, step 1 and the step-2 report.

    python3 src/certified_offers_verdicts.py runs/certified-offers.json
"""
import os, sys, json, gzip
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'runs', 'certified_offers')
DELTAS = [1e-1, 3e-2, 1e-2, 3e-3, 1e-3]


def load():
    g = json.load(open(os.path.join(D, 'gates.json')))
    s0 = json.load(gzip.open(os.path.join(D, 'step0.json.gz'), 'rt'))
    s1 = json.load(open(os.path.join(D, 'step1.json')))
    rep = json.load(open(os.path.join(D, 'step2.json')))
    return g, s0, s1, rep


def cell(rep, arm, b, ph, N, d, I=64, ex='', long=False):
    k = json.dumps([str(x) for x in (arm, float(b), float(ph), N, I, float(d), ex, long)])
    return rep['cells'].get(k)


def S(s0, key):
    return s0['summary'].get(key)


def verdict(holds, fired, scored=True):
    if not scored:
        return 'unscorable'
    if holds:
        return 'holds'
    return 'falsified' if fired else 'fails, falsifier not fired'


def main(out):
    g, s0, s1, rep = load()
    V = {}
    # RE 1
    pts = [v for k, v in g['G2'].items() if k != 'three_carrier'] + [v for k, v in g['G2_C0'].items() if k != 'three_carrier']
    bad = sum(v['pointing'] - v['fair_pair'] + v['pair_to'] for v in pts)
    V['RE1'] = dict(result='pointing triples %d (C1 and C0), not fair or timed out: %d' % (sum(v['pointing'] for v in pts), bad), verdict=verdict(bad == 0, bad > 0))
    # RE 2
    sm = s0['summary']
    inact = [k for k in sm if k.startswith('item1|accepter into v|Rc|matched|e=') and 'carrier-active' not in k]
    act = 'item1|accepter into v|Rc|matched|e=carrier-active'
    meds = {k.split('e=')[1]: sm[k]['median'] for k in inact}
    mins = min(sm[k]['min'] for k in inact)
    g3 = g['G3']
    bully_to = sum(s['bully_read_to'] for kk in ('Bn|Rcn', 'Bp|Rcp') for s in g3[kk].values())
    rcs_sim = sm.get('item1|accepter into v|Rcs|matched|e=sim-reader', {}).get('median')
    rcs_act = sm.get('item1|accepter into v|Rcs|matched|e=carrier-active', {}).get('median')
    h2 = all(0.5 <= m <= 2 for m in meds.values()) and sm[act]['min'] >= 5 and bully_to == 0 and rcs_sim < 0.1 and rcs_act >= 5
    V['RE2'] = dict(result='Rc inactive medians %s (min %.3g); active median %.3g (min %.3g); bully reads timed out beside Rc: %d; Rcs beside simulating readers '
                           'median %.3g, beside active carriers %.3g' % (meds, mins, sm[act]['median'], sm[act]['min'], bully_to, rcs_sim, rcs_act),
                    verdict=verdict(h2, mins < 0.1 or sm[act]['min'] < 0.1))
    # RE 3
    fc = sm['item1|into e, Rc resident|Fc|carrier-active']; oc = sm['item1|into e, Rc resident|Oc|carrier-active']
    V['RE3'] = dict(result='Fc into e median %.3g (min %.3g); matched Oc %.3g (min %.3g); mismatched Oc %.3g' % (
        fc['median'], fc['min'], oc['median'], oc['min'], sm['item1|into e, Rc resident|Oc|carrier-inactive']['median']),
        verdict=verdict(min(fc['min'], oc['min']) >= 5, min(fc['min'], oc['min']) < 2))
    # RE 4
    a = [sm[k] for k in ('item3|Fc,Fc|pair|Bc', 'item3|Rc,Oc|pair|Bc', 'item3|Fc,Bc|pair|Bc')]
    amax = max(x['max'] for x in a); amin = min(x['min'] for x in a)
    b = [sm['item3|Fc,Bc|out|%s' % c] for c in ('C0', 'C3', 'C6')]
    bmed = max(x['median'] for x in b)
    c1 = {x: (sm.get('item1c|into e, 1/3-constant victim|%s|carrier-active|points at b=True' % x) or sm.get('item1c|into e, 1/3-constant victim|%s|carrier-inactive|points at b=True' % x)) for x in ('Fc', 'Oc')}
    c4 = {x: (sm.get('item4c|into e, 1/3-constant victim|%s|carrier-active|points at b=True' % x) or sm.get('item4c|into e, 1/3-constant victim|%s|carrier-inactive|points at b=True' % x)) for x in ('Fc', 'Oc')}
    cdiff = {x: (c4[x]['median'], c1[x]['median']) for x in ('Fc', 'Oc')}
    clause_c = all(abs(u - v) <= 0.2 for u, v in cdiff.values())
    V['RE4'] = dict(result='(a) Bc into pair slots of fair carrier islands: rho*N in [%.3g, %.3g]; (b) 1/3 constants into the third slot of (Fc, Bc): median %.3g; '
                           '(c) carriers pointing at the bully into e, Bc island vs simulating bully island (medians): %s' % (amin, amax, bmed, cdiff),
                    verdict=('falsified (third clause)' if not clause_c else 'holds') if (amax <= 1.5 and amin >= 0.1 and bmed <= 1.0) else
                    ('falsified' if amin < 0.1 else 'fails, falsifier not fired'))
    V['RE4']['clauses'] = dict(a=amax <= 1.5 and amin >= 0.1, b=bmed <= 1.0, c=clause_c, falsifier_fired=amin < 0.1)
    sd = rep['seeded']
    # RE 5
    x = sd.get('FcOcRc|unequal|ph=0.5', {}).get('fair120')
    V['RE5'] = dict(result='FcOcRc seeded all-unequal (simulating bully) fair at 120N: %s (queue 78 F+R 0.05)' % x,
                    verdict=verdict(x is not None and 0.05 < x < 0.3, x is not None and (x >= 0.3 or x <= 0.05), x is not None))
    if x is not None and x >= 0.3:
        V['RE5']['verdict'] = 'falsified (in the direction of the RS\'s program)'
    elif x is not None and x <= 0.05:
        V['RE5']['verdict'] = 'falsified (no gain)'
    # RE 6
    ds = rep['delta_star']
    cert_arms = ('Fc', 'FcOc', 'FcOcRc', 'FcRc', 'mix', 'FcOcRcs', 'PcOcRc')
    b3 = {k: v['status'] for k, v in ds.items() if k.split('|')[0] in cert_arms and '|b=3|' in k and '|ph=0.5|' in k}
    V['RE6'] = dict(result='delta* status at beta = 3, phi = 1/2: %s' % b3, verdict=verdict(all(s == 'none' for s in b3.values()), any(s == 'bracket' for s in b3.values()), bool(b3)))
    # RE 7
    m = cell(rep, 'FcOcRc', 1, 0.5, 200, 0.1); f = cell(rep, 'FOR', 1, 0.0, 200, 0.1)
    dd = m['mean'] - f['mean'] if m and f else None
    V['RE7'] = dict(result='FcOcRc %.2f vs F+O+R %.2f at beta = 1, N = 200, delta = 0.1: %+.2f' % (m['mean'], f['mean'], dd) if dd is not None else 'missing',
                    verdict=verdict(dd is not None and dd >= 0.15, dd is not None and dd <= 0.05, dd is not None))
    # RE 8
    x = rep.get('RE8_pooled_main_b3')
    V['RE8'] = dict(result='main arm, beta = 3, phi = 1/2: mean share of islands with the 120N class equal to the 30N class %s' % x,
                    verdict=verdict(x is not None and x >= 0.8, x is not None and x < 0.6, x is not None))
    # RE 9
    f0 = cell(rep, 'F', 0, 0.0, 200, 0.03)
    diffs = {}
    for arm in ('Fc', 'FcOc', 'FcOcRc', 'FcRc', 'mix', 'FcOcRcs', 'PcOcRc'):
        c = cell(rep, arm, 0, 0.5, 200, 0.03)
        if c:
            diffs[arm] = round(c['mean'] - f0['mean'], 3)
    V['RE9'] = dict(result='beta = 0, N = 200, delta = 0.03, arm - F (F %.2f): %s' % (f0['mean'], diffs),
                    verdict=verdict(all(abs(v) <= 0.1 or v > 0 for v in diffs.values()), any(v < -0.2 for v in diffs.values()), bool(diffs)))
    V['RE9']['note'] = 'scored as "no arm lower than F by more than 0.1" (arms above F count as within the claim that certification costs nothing)'
    # RE 10
    rows = []
    for b in (1, 3):
        for N in (100, 200):
            for d in DELTAS:
                mx = cell(rep, 'mix', b, 0.5, N, d); c = cell(rep, 'FcOcRc', b, 0.5, N, d); s = cell(rep, 'FOR', b, 0.0, N, d)
                if not (mx and c and s):
                    continue
                lo, hi = min(c['mean'], s['mean']), max(c['mean'], s['mean'])
                dist = (mx['mean'] - hi) if mx['mean'] > hi else ((mx['mean'] - lo) if mx['mean'] < lo else 0.0)
                lower_ci = c['ci'] if c['mean'] <= s['mean'] else s['ci']
                fired = mx['mean'] <= lo - 0.15 and mx['ci'][1] < lower_ci[0]
                rows.append(dict(b=b, N=N, d=d, mix=mx['mean'], cert=c['mean'], sim=s['mean'], dist=round(dist, 3), fired=bool(fired)))
    inside = sum(1 for r in rows if abs(r['dist']) <= 0.05)
    V['RE10'] = dict(result='%d cells; mix within 0.05 of [min, max] of (FcOcRc, F+O+R) in %d; mean signed distance outside %.3f; below the lower by >= 0.15 with '
                            'separated intervals in %d' % (len(rows), inside, float(np.mean([r['dist'] for r in rows])) if rows else float('nan'), sum(r['fired'] for r in rows)),
                     verdict=verdict(rows and inside == len(rows), any(r['fired'] for r in rows), bool(rows)), cells=rows)
    # RE 12
    t3 = g['G2']['three_carrier']['Fc^3']
    fc0 = cell(rep, 'Fc', 0, 0.5, 200, 0.1); f00 = cell(rep, 'F', 0, 0.0, 200, 0.1)
    dd = fc0['mean'] - f00['mean'] if fc0 and f00 else None
    rel = 1 - t3['mean_payoff_per_slot'] / (1 / 3)
    V['RE12'] = dict(result='(Fc)^3 mean payoff per slot %.4f against 1/3 (relative loss %.3f, 2 of 8 orientations cycle); Fc - F at beta = 0, N = 200, delta = 0.1: %s' % (
        t3['mean_payoff_per_slot'], rel, ('%+.2f' % dd) if dd is not None else '-'),
        verdict=verdict(abs(rel - 0.25) < 1e-9 and dd is not None and dd >= -0.1, dd is not None and dd < -0.2, dd is not None))
    # RE 11
    gr = s1['groups']
    gap = max(gr['Oc']['shortest']['C1'], gr['Rc']['shortest']['C1']) - gr['single']['shortest']['R1']
    c0min = min(gr[x]['shortest']['C0w'] for x in ('Oc', 'Rc', 'Rcs', 'Fc', 'Bc'))
    V['RE11'] = dict(result='C1 shortest Oc / Rc %d / %d nodes against the fair reader %d (gap %+d); C0-written shortest carrier %d nodes' % (
        gr['Oc']['shortest']['C1'], gr['Rc']['shortest']['C1'], gr['single']['shortest']['R1'], gap, c0min),
        verdict=verdict(gap <= 4 and c0min > 100, gap > 8))
    # ---------------------------------------------------------------- E
    vals = [sm[k] for k in inact]
    lo_, hi_ = min(v['min'] for v in vals), max(v['max'] for v in vals)
    V['E1'] = dict(result='Rc (matched) beside non-pointing e: rho*N in [%.6g, %.6g] over %d edges' % (lo_, hi_, sum(v['n'] for v in vals)),
                   verdict=verdict(lo_ >= 1 - 1e-6 and hi_ <= 1 + 1e-6, lo_ < 0.99 or hi_ > 1.01))
    rv = sm['item1|accepter into v, offerer resident|Rc|matched|Fc|carrier-active']
    V['E2'] = dict(result='Fc into e %.4g, matched Oc %.4g; Rc into v beside Fc %.4g (min over the second steps %.3g)' % (fc['median'], oc['median'], rv['median'],
                                                                                                                       min(fc['min'], oc['min'], rv['min'])),
                   verdict=verdict(abs(fc['median'] - 27.9) <= 0.2 and abs(oc['median'] - 27.9) <= 0.2 and abs(rv['median'] - 9.75) <= 0.1,
                                   min(fc['min'], oc['min'], rv['min']) < 5))
    e3 = [sm[k] for k in sm if k.startswith('item4c|into e, 1/3-constant victim|') and k.endswith('points at b=True') and k.split('|')[2] in ('Fc', 'Pc', 'Bc', 'Oc', 'Rc')]
    e3min = min(x['min'] for x in e3)
    e3out = set(o for x in e3 for o in x['out_if_fixed'])
    V['E3'] = dict(result='carriers pointing at Bc into e of Bc\'s unequal island (no Rc): min rho*N %.3g, outcomes if fixed %s' % (e3min, sorted(e3out)),
                   verdict=verdict(e3min >= 20 and e3out == {'F'}, e3min < 5))
    e4a = [sm['item3|Fc,Fc|pair|Bc'], sm['item3|Rc,Oc|pair|Bc']]
    e4b = [sm['item3|Fc,Bc|out|%s' % c] for c in ('C0', 'C3', 'C6')]
    lo4 = min(x['min'] for x in e4a + e4b); hi4 = max(x['max'] for x in e4a + e4b)
    V['E4'] = dict(result='Bc into pair slots of (Fc, Fc) / (Rc, Oc): [%.3g, %.3g]; 1/3 constants into the third slot of (Fc, Bc): median %.3g, range [%.3g, %.3g]' % (
        min(x['min'] for x in e4a), max(x['max'] for x in e4a), max(x['median'] for x in e4b), min(x['min'] for x in e4b), max(x['max'] for x in e4b)),
        verdict=verdict(lo4 >= 0.99 and hi4 <= 1.01, lo4 < 0.5 or hi4 > 2))
    bc = {a: sd.get('%s|unequalBc|ph=1' % a, {}).get('fair120') for a in ('Fc', 'FcOcRc', 'FcRc')}
    sim = {a: sd.get('%s|unequal|ph=0.5' % a, {}).get('fair120') for a in ('Fc', 'FcOcRc', 'FcRc')}
    ok = all(v is not None for v in list(bc.values()) + list(sim.values()))
    V['E5'] = dict(result='fair at 120N, Bc start (phi = 1) %s; simulating start (phi = 1/2) %s' % (bc, sim),
                   verdict=verdict(ok and all(v >= 0.5 for v in bc.values()) and all(v <= 0.15 for v in sim.values()),
                                   ok and (any(v < 0.3 for v in bc.values()) or any(v > 0.3 for v in sim.values())), ok))
    p1 = cell(rep, 'FcOcRc', 3, 1.0, 200, 0.1); p0 = cell(rep, 'FcOcRc', 3, 0.0, 200, 0.1)
    dd = p1['mean'] - p0['mean'] if p1 and p0 else None
    V['E6'] = dict(result='FcOcRc beta = 3, N = 200, delta = 0.1: phi = 1 %s, phi = 0 %s, difference %s' % (p1 and round(p1['mean'], 2), p0 and round(p0['mean'], 2),
                                                                                                           ('%+.2f' % dd) if dd is not None else '-'),
                   verdict=verdict(dd is not None and dd >= 0.2, dd is not None and dd < 0.05, dd is not None))
    e7 = {}
    fired = False; held = True
    for a in ('FcOcRc', 'FcRc'):
        v = sd.get('%s|unequal|ph=0.5' % a)
        if not v or not v.get('pacing'):
            held = False; continue
        pred = v['pacing']['pred_second']; obs = v['observed_local_Rc_routes_cert']
        e7[a] = dict(predicted=round(pred, 2), observed=obs, second_step_arrivals=v['pacing']['n_second'])
        ok_ = (obs <= 3 and pred <= 3) or (pred > 0 and 1 / 3 <= obs / pred <= 3)
        held &= ok_
        fired |= obs > 3 * pred and obs > 3
    V['E7'] = dict(result=json.dumps(e7), verdict=verdict(held and len(e7) == 2, fired, len(e7) == 2))
    dif = []
    for d in DELTAS:
        a_ = cell(rep, 'Fc', 0, 0.5, 200, d); b_ = cell(rep, 'F', 0, 0.0, 200, d)
        if a_ and b_:
            dif.append(a_['mean'] - b_['mean'])
    md = float(np.mean(dif)) if len(dif) == 5 else None
    V['E8'] = dict(result='beta = 0, N = 200: mean over delta of V*(Fc) - V*(F) = %s (per delta %s)' % (md, [round(x, 2) for x in dif]),
                   verdict=verdict(md is not None and md >= 0, md is not None and md <= -0.1, md is not None))
    e9 = {}
    for b in (0, 3):
        dl = []
        for d in DELTAS:
            a_ = cell(rep, 'Fcs', b, 0.5, 200, d); b_ = cell(rep, 'Fc', b, 0.5, 200, d)
            if a_ and b_:
                dl.append(a_['mean'] - b_['mean'])
        e9[b] = float(np.mean(dl)) if len(dl) == 5 else None
    ok = all(v is not None for v in e9.values())
    V['E9'] = dict(result='Fc* - Fc, mean over delta at N = 200: %s' % e9, verdict=verdict(ok and all(abs(v) <= 0.05 for v in e9.values()),
                                                                                         ok and any(v >= 0.15 for v in e9.values()), ok))
    a_ = sd.get('FcOcRcs|unequal|ph=0.5', {}).get('fair120'); b_ = sd.get('FcOcRc|unequal|ph=0.5', {}).get('fair120')
    V['E10'] = dict(result='seeded all-unequal fair at 120N: FcOcRcs %s, FcOcRc %s' % (a_, b_),
                    verdict=verdict(a_ is not None and b_ is not None and a_ >= b_ - 0.05, a_ is not None and b_ is not None and b_ - a_ > 0.1, a_ is not None and b_ is not None))
    e11 = []
    fired = False
    for d in DELTAS:
        a_ = cell(rep, 'FcOcC3', 3, 0.5, 200, d); b_ = cell(rep, 'FcOcRc', 3, 0.5, 200, d)
        if a_ and b_:
            e11.append(round(b_['mean'] - a_['mean'], 3))
            fired |= (b_['mean'] - a_['mean'] >= 0.2 and b_['ci'][0] > a_['ci'][1])
    V['E11'] = dict(result='FcOcRc - FcOcC3 at beta = 3, N = 200 by delta: %s' % e11,
                    verdict=verdict(len(e11) == 5 and all(abs(x) <= 0.1 for x in e11), fired, len(e11) == 5))
    oc1 = gr['Oc']['shortest']['C1']; fc1 = gr['Fc']['shortest']['C1']; sg = gr['single']['shortest']['R1']; w = gr['Oc']['shortest']['R1w']
    V['E12'] = dict(result='C1: Oc %d, Fc %d, fair reader %d nodes; R1-written Oc %d (gap %d)' % (oc1, fc1, sg, w, w - sg),
                    verdict=verdict(oc1 <= sg and fc1 - sg <= 6 and w - sg >= 12, oc1 > sg or w - sg < 8))
    json.dump(dict(verdicts=V), open(out, 'w'), indent=1, default=str)
    for k, v in V.items():
        print(k, '|', v['verdict'], '|', v['result'][:300])
    return V


if __name__ == '__main__':
    main(sys.argv[1])
