"""Verdicts of queue 78 (predictions/2026-11-14-patient-accepters.md) from step 0, step 1 and the step-2 report.

    python3 src/patient_accepter_verdicts.py runs/patient-accepters.json runs/patient-accepters.md
"""
import os, sys, json, gzip
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import patient_accepter_report as REP

D = os.path.join(ROOT, 'runs', 'patient_accepter')


def load_step0():
    p = os.path.join(D, 'step0.json')
    if os.path.exists(p):
        return json.load(open(p))
    return json.load(gzip.open(p + '.gz'))


def main(outj, outmd):
    s0 = load_step0()
    routes = json.load(open(os.path.join(D, 'step0_routes.json')))
    s1 = json.load(open(os.path.join(D, 'step1.json')))
    rep = REP.main(os.path.join(D, 'step2_report.json'), os.path.join(D, 'step2_report.md'))
    cs, rows, stored = REP.build()
    V = {}
    # ---------------------------------------------------------------- RE 1
    it1 = s0['item1']
    comp = [r['rhoN'] for r in it1 if r['to'] == 'n' and r['orient'] == 'matched' and r['read'] == 'complete' and not r['offer']]
    to = [r['rhoN'] for r in it1 if r['to'] == 'n' and r['orient'] == 'matched' and r['read'] == 'TO']
    med_c = float(np.median(comp)); med_t = float(np.median(to)); max_t = float(np.max(to))
    V['RE1'] = dict(completed_median=med_c, completed_n=len(comp), completed_share_exactly_1=float(np.mean(np.abs(np.array(comp) - 1) < 1e-9)),
                    completed_min=float(min(comp)), timed_out_median=med_t, timed_out_max=max_t, timed_out_n=len(to),
                    verdict=('holds' if 0.5 <= med_c <= 2 and max_t < 0.1 else ('falsified' if med_c < 0.2 else 'fails, falsifier not fired')))
    # ---------------------------------------------------------------- RE 2
    sel1 = [r['rhoN'] for r in routes if r['R'][2] == 'n' and r['step'].startswith('selected: 1/2')]
    sel2 = [r['rhoN'] for r in routes if r['R'][2] == 'n' and r['step'].startswith('selected: R')]
    f1 = [r['rhoN'] for r in routes if r['R'][2] == 'n' and r['step'].startswith('R first')]
    f2 = [r['rhoN'] for r in routes if r['R'][2] == 'n' and r['step'].startswith('offerer first')]
    ok = min(sel1) >= 5 and min(sel2) >= 5 and all(0.5 <= x <= 2 for x in f1 + f2)
    V['RE2'] = dict(offerer_into_e_with_R=[min(sel1), max(sel1)], R_into_v_with_offerer=[min(sel2), max(sel2)], R_first=[min(f1), max(f1)], offerer_first=[min(f2), max(f2)],
                    verdict='holds' if ok else ('falsified' if min(sel1 + sel2) < 2 else 'fails, falsifier not fired'))
    # ---------------------------------------------------------------- seeded
    sd = rep['seeded']
    g = lambda arm, kind, k='fair120': sd.get('%s|%s' % (arm, kind), {}).get(k)
    fr, forr, f, fc, ro = (g(a, 'unequal') for a in ('FR', 'FOR', 'F', 'FC', 'R'))
    V['RE3'] = dict(FR=fr, FOR=forr, F=f, FC=fc, R=ro,
                    verdict=('holds' if fr is not None and fr >= 0.3 and forr >= fr and f <= 0.05 and fc <= 0.05 else
                             ('falsified' if fr is not None and fr < 0.1 else 'fails, falsifier not fired')))
    # ---------------------------------------------------------------- RE 4
    ds = REP.delta_star(cs, 'FR', 3.0, 200, 64, 1.0)
    V['RE4'] = dict(delta_star=REP.ds_str(ds), means=ds.get('means'), verdict=('holds' if ds['status'] == 'bracket' else 'falsified'))
    fF = {d: (REP.get(cs, 'F', 3.0, 200, 64, d) or {}).get('mean') for d in REP.DELTAS}
    V['RE4']['F_means'] = fF
    # ---------------------------------------------------------------- RE 5
    a = REP.get(cs, 'FR', 0.0, 200, 64, 0.03); b = REP.get(cs, 'F', 0.0, 200, 64, 0.03)
    diff = a['mean'] - b['mean'] if a and b else None
    V['RE5'] = dict(FR=a and a['mean'], F=b and b['mean'], diff=diff,
                    verdict=None if diff is None else ('holds' if abs(diff) <= 0.1 else ('falsified' if diff < -0.2 else 'fails, falsifier not fired')))
    # ---------------------------------------------------------------- RE 6
    r1 = s1['R1']
    gap = r1['shortest_R_n'] - r1['shortest_single']
    V['RE6'] = dict(R1_gap_nodes=gap, R1_ratio_to_bully=r1['ratio_Rn_to_bully'], R0_gap=s1['R0']['shortest_R_n'] - s1['R0']['shortest_single'],
                    verdict=('holds' if gap <= 2 and 0.1 <= r1['ratio_Rn_to_bully'] <= 10 else ('falsified' if gap > 4 else 'fails, falsifier not fired')))
    # ---------------------------------------------------------------- RE 7
    lp = rep['lps']
    mx = max((v['mean'] for v in lp.values()), default=None)
    V['RE7'] = dict(max_cell=mx, n_cells=len(lp), verdict=None if mx is None else ('holds' if mx < 0.9 else 'falsified'))
    # ---------------------------------------------------------------- RE 8
    a = g('FR', 'fair'); b = g('F', 'fair')
    V['RE8'] = dict(FR=a, F=b, diff=(a - b) if a is not None and b is not None else None,
                    verdict=None if a is None or b is None else ('holds' if a >= b - 0.1 else ('falsified' if a < b - 0.25 else 'fails, falsifier not fired')))
    # ---------------------------------------------------------------- counters
    vfr = [REP.get(cs, 'FR', 3.0, 200, 64, d)['mean'] for d in REP.DELTAS]
    vfor = [REP.get(cs, 'FOR', 3.0, 200, 64, d)['mean'] for d in REP.DELTAS]
    V['carbon_a'] = dict(FR_seed_fair120=fr, FR_V_max=max(vfr), FR_threshold=REP.ds_str(ds),
                         verdict='true' if (fr is not None and fr < 0.3 and max(vfr) < 0.5 and ds['status'] != 'bracket') else 'false')
    V['carbon_b'] = dict(FOR_minus_FR_seed=(forr - fr) if fr is not None else None, FOR_minus_FR_V_max=max(x - y for x, y in zip(vfor, vfr)),
                         verdict='true' if (fr is not None and forr - fr <= 0.05 and max(x - y for x, y in zip(vfor, vfr)) <= 0.1) else 'false')
    # exits: carbon (c) and sol on the seeded exit classification (all arms, beta = 3, seed2)
    allex = []
    for k, c in cs.items():
        if c['_rows'] and k[6].startswith(':seed='):
            for r in c['_rows']:
                if r.get('exits', {}).get('version') == 2:
                    for e in r['exits']['exits']:
                        allex.append(dict(arm=k[0], start=k[6][6:], run=r['r'], **e))
    readers = {'single', 'two', 'single2', 'opener'}
    ex_unequal = [e for e in allex if e['start'] == 'unequal']
    withR = [e for e in allex if 'accepter' in e['pair_fams']]
    R_partner_nonhalf = [e for e in withR if not any(v in ('C1', 'C4') for k_, v in e['pair_roles'].items() if not v.startswith('R'))]
    reader_pairs = [e for e in allex if readers & set(e['pair_fams'])]
    carbon_c = len(R_partner_nonhalf) == 0 and len(reader_pairs) == 0
    local = [e for e in allex if e.get('origin') == 'local']
    local_FO = [e for e in local if readers & set(e['pair_fams']) or any(st[4][0] in 'SDOF' for st in e['seq'])]
    imported = [e for e in allex if e.get('origin') == 'imported']
    V['carbon_c'] = dict(exits=len(allex), with_R=len(withR), R_with_non_half_partner=len(R_partner_nonhalf), pairs_with_F_or_O=len(reader_pairs),
                         lasting_pairs_with_F_or_O=sum(1 for e in reader_pairs if e['lasted_to_120N']),
                         verdict=('vacuous (no exits)' if not allex else ('true' if carbon_c else 'false')))
    V['sol'] = dict(local=len(local), local_involving_F_or_O=len(local_FO), imported=len(imported),
                    imported_lasting=sum(1 for e in imported if e['lasted_to_120N']),
                    verdict='true' if (local_FO or imported) else ('false' if allex else 'vacuous'))
    # route table over all seeded exits
    rt = {}
    for e in allex:
        k = '%s|%s|%s|%s' % (e['arm'], e['start'], e['route'], e['origin'])
        x = rt.setdefault(k, [0, 0]); x[0] += 1; x[1] += int(e['lasted_to_120N'])
    V['exit_routes'] = rt
    # ---------------------------------------------------------------- E-predictions (numbers; scored in the md by hand-checked rules)
    E = {}
    E['E1'] = dict(completed_nonoffer_not1=[r['third'] for r in it1 if r['to'] == 'n' and r['orient'] == 'matched' and r['read'] == 'complete' and not r['offer'] and abs(r['rhoN'] - 1) > 1e-6],
                   offering=sorted({round(r['rhoN'], 3) for r in it1 if r['to'] == 'n' and r['orient'] == 'matched' and r['read'] == 'complete' and r['offer']}),
                   timed_out_max=max_t, mismatched_max=max(r['rhoN'] for r in it1 if r['to'] == 'n' and r['orient'] == 'mismatched'))
    it2 = s0['item2']
    rd = [r for r in it2 if r['R'][2] == 'n' and r['xg'] in ('Fs', 'Ft', 'F2', 'O', 'Pz', 'Po')]
    half = [r['rhoN'] for r in it2 if r['R'][2] == 'n' and r['x'] in ('C4', 'C1') and r['out_if_fixed'] == 'F' and r['resident_third'] == 'C8']
    E['E2'] = dict(reader_share_gt3=float(np.mean([r['rhoN'] > 3 for r in rd])), reader_n=len(rd), reader_rest_max=max(r['rhoN'] for r in rd if r['rhoN'] <= 3),
                   half_constant_vs_C8=[min(half), max(half)] if half else None)
    it4a = s0['item4a']
    E['E4'] = dict(bully_into_fair_R_island_max=max(r['rhoN'] for r in it4a if r['xg'] == 'B'),
                   bully_into_fair_R_island_share_gt3=float(np.mean([r['rhoN'] > 3 for r in it4a if r['xg'] == 'B'])),
                   two3_into_out_slot_max=max(r['rhoN'] for r in it4a if r['role'] == 'out' and r['xg'] in ('C2', 'C5', 'C8')),
                   R_into_FI_pair_max=max(r['rhoN'] for r in s0['item4b'] if r['cls'] == 'FI' and r['role'] == 'pair' and r['R'][2] == 'n'),
                   R_into_FI_out_max=max(r['rhoN'] for r in s0['item4b'] if r['cls'] == 'FI' and r['role'] == 'out' and r['R'][2] == 'n'))
    gm = {}
    for arm in ('FR', 'FOR', 'FC'):
        for b in (1.0, 3.0):
            for d in REP.DELTAS:
                x = REP.get(cs, arm, b, 200, 64, d, 0.3); y = REP.get(cs, arm, b, 200, 64, d, 3.0)
                if x and y:
                    gm['%s|%g|%g' % (arm, b, d)] = y['mean'] - x['mean']
    E['E8'] = dict(max_abs=max(abs(v) for v in gm.values()) if gm else None, diffs=gm)
    E['E9'] = {('%g' % d): ((REP.get(cs, 'FR', 0.0, 200, 64, d) or {}).get('mean', np.nan) - (REP.get(cs, 'F', 0.0, 200, 64, d) or {}).get('mean', np.nan)) for d in REP.DELTAS}
    E['E7'] = dict(FR_minus_F_b3_N200={('%g' % d): REP.get(cs, 'FR', 3.0, 200, 64, d)['mean'] - REP.get(cs, 'F', 3.0, 200, 64, d)['mean'] for d in REP.DELTAS},
                   thresholds=[k for k, v in rep['delta_star'].items() if v['status'] == 'bracket'])
    c = REP.get(cs, 'FR', 3.0, 200, 64, 0.03)
    E['E12_E13'] = dict(R_minus_C13=c['R_minus_C13'], n=c['R_minus_C13_n'], R_victim_share=c['R_victim_share'], counts=c['R_victim_counts'])
    E['E14'] = {a: g(a, 'fair') for a in ('F', 'FR', 'FOR', 'FC', 'R')}
    V['E'] = E
    json.dump(dict(verdicts=V, seeded=sd, delta_star=rep['delta_star'], lps=rep['lps'], step1=s1), open(outj, 'w'), indent=1, default=str)
    print(json.dumps({k: (v.get('verdict') if isinstance(v, dict) else None) for k, v in V.items()}, indent=1))
    return V


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
