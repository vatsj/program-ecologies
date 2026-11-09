"""Step 2 report of queue 76: the length-prior mass of P, Q, O beside queue 75's classes for the machines R0, R1, R2.

    python3 src/lt_prior_br_report.py OUT_STEP2.json OUT_REPORT.json OUT.md

Inputs: queue 75's runs/lt_prior/lt-prior.json (R0, R1: constants, junk, fair readers, bullies, Monte Carlo, shortest spellings) and
runs/length_prior_t/step1.json; this queue's runs/lt_prior_br/search_<M>.json (P, Q, O lower bounds and spellings; for R2 also the T+
classes) and, for R2, the exhaustive enumeration and the Monte Carlo in runs/lt_prior_br/e_R2 (enum_R2_s4_*.json, mc_R2_*.json).
All masses are conditional on a finite tree (divided by the machine's finite-tree mass q) unless called raw.
"""
import os, sys, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import lt_prior_br as B
import lt_prior as P
import lt_prior_report as RP

OLD = os.path.join(ROOT, 'runs', 'lt_prior')
NEW = os.path.join(ROOT, 'runs', 'lt_prior_br')
PRU = ('prudent_z', 'prudent_o', 'prudent_a', 'opener')


def br_groups(path):
    """{group: [raw mass, count, min size, example, per-member dict]} of the P / Q / O lower bounds, and the probe-bearing spellings of other classes."""
    d = json.load(open(path))
    g = {k: dict(mass=0.0, count=0, min_size=None, example=None, members={}) for k in PRU}
    other = {}
    for key, szd in d['prudent'].items():
        grp, member = key.split('|')
        for s, forms in szd.items():
            for form, v in forms.items():
                m, c, ex = v[0], v[1], v[2]
                if grp in g:
                    x = g[grp]
                    x['mass'] += m; x['count'] += c
                    mm = x['members'].setdefault(member, dict(mass=0.0, min_size=None, example=None))
                    mm['mass'] += m
                    if mm['min_size'] is None or int(s) < mm['min_size']:
                        mm['min_size'] = int(s); mm['example'] = ex
                    if x['min_size'] is None or int(s) < x['min_size']:
                        x['min_size'] = int(s); x['example'] = ex
                else:
                    o = other.setdefault(grp, dict(mass=0.0))
                    o['mass'] += m
    for name, v in d['opener'].items():
        x = g['opener']
        x['mass'] += v['mass']; x['count'] += v['count']
        mm = x['members'].setdefault(name, dict(mass=0.0, min_size=None, example=None))
        mm['mass'] += v['mass']
        if v['shortest']:
            mm['min_size'], mm['example'] = v['shortest'][0], v['shortest'][1]
            if x['min_size'] is None or v['shortest'][0] < x['min_size']:
                x['min_size'] = v['shortest'][0]; x['example'] = v['shortest'][1]
    return g, other, d


def mc_union_upper(R, q):
    """95% Wilson upper bounds (conditional) from the Monte Carlo outside the exhaustive enumeration: for P (and Q), which the queue-75 classifier
    labels as a single-reader family (it answers constants like a single reader), the groups single / two / bully / exploit (all zero hits in
    queue 75's runs, as for the bound on rho_R); for O, which answers constants unlike D and so lands in 'other_cond', that group's hits (not informative:
    other conditionals are most of the finite mass of R1)."""
    mc = R.get('mc')
    if not mc:
        return None
    n = mc['n']
    k = sum(R['estimate'][g]['hits_M'] for g in ('single', 'two', 'bully', 'exploit'))
    ko = R['estimate']['other_cond']['hits_M']
    lo, hi = RP.wilson(k, n)
    lo2, hi2 = RP.wilson(ko, n)
    return dict(n=n, hits=k, upper_raw=hi, upper_cond=hi / q, other_cond_hits=ko, other_cond_upper_cond=hi2 / q)


def main(out2, outrep, outmd):
    S1 = json.load(open(os.path.join(ROOT, 'runs', 'length_prior_t', 'step1.json')))
    old = json.load(open(os.path.join(OLD, 'lt-prior.json')))
    step2 = dict(machines=['R0', 'R1', 'R2'], note='lower bounds on exact-member class masses (conditional on finite trees); constants and junk are estimates')
    rep = {}
    # ---- R2 base report (enumeration, Monte Carlo, T+ search) in the queue-75 format
    e2 = os.path.join(NEW, 'e_R2')
    r2 = None
    if os.path.exists(os.path.join(NEW, 'search_R2.json')) and glob.glob(os.path.join(e2, 'enum_R2_s4_*.json')):
        s = json.load(open(os.path.join(NEW, 'search_R2.json')))
        json.dump(dict(machine='R2', wall=s['wall'], classes=s['t_plus']), open(os.path.join(e2, 'search_R2.json'), 'w'))
        r2 = RP.report_machine('R2', e2, 4)
    machines = {'R0': old['machines']['R0'], 'R1': old['machines']['R1']}
    if r2:
        machines['R2'] = r2
    for mn in ('R0', 'R1', 'R2'):
        R = machines.get(mn)
        spath = os.path.join(NEW, 'search_%s.json' % mn)
        if R is None or not os.path.exists(spath):
            continue
        q = R['finite_mass_q']
        g, other, sd = br_groups(spath)
        h = R['headline']; c = R['combined']
        single = c['single']['lower_bound_exact_raw']; bully = c['bully']['lower_bound_exact_raw']
        two = c['two']['lower_bound_exact_raw']; expl = c['exploit']['lower_bound_exact_raw']
        sh = R['shortest']
        rec = dict(q=q, single_raw=single, bully_raw=bully, two_raw=two, exploit_raw=expl,
                   shortest_single=sh.get('single/exact', {}).get('min_size'), shortest_single_example=sh.get('single/exact', {}).get('example'),
                   shortest_bully=sh.get('bully/exact', {}).get('min_size'),
                   shortest_two=sh.get('two/exact', {}).get('min_size'))
        for k in PRU:
            x = g[k]
            rec[k] = dict(raw=x['mass'], cond=x['mass'] / q, min_size=x['min_size'], example=x['example'], count=x['count'],
                          ratio_to_single=(x['mass'] / single) if single else None, ratio_to_bully=(x['mass'] / bully) if bully else None,
                          gap_to_shortest_single=(x['min_size'] - rec['shortest_single']) if (x['min_size'] and rec['shortest_single']) else None,
                          members={m: dict(raw=v['mass'], min_size=v['min_size'], example=v['example']) for m, v in x['members'].items()})
        rec['probe_bearing_spellings_of_other_classes_raw'] = {k: v['mass'] for k, v in other.items()}
        rec['prudent_all_min_size'] = min([rec[k]['min_size'] for k in ('prudent_z', 'prudent_o', 'prudent_a') if rec[k]['min_size']] or [None])
        rec['gap_prudent_any'] = rec['prudent_all_min_size'] - rec['shortest_single'] if rec['prudent_all_min_size'] and rec['shortest_single'] else None
        rec['gap_prudent_z'] = rec['prudent_z']['gap_to_shortest_single']
        rec['gap_opener'] = rec['opener']['gap_to_shortest_single']
        rec['mc_upper_bound'] = mc_union_upper(R, q)
        rec['accounting_sum'] = R['accounting']['sum']
        rep[mn] = rec
        # ---- the law input
        s2 = dict(const=(S1[mn]['const'] if mn in S1 else R['const_by_code_cond']),
                  junk_f=(S1[mn]['junk_f'] if mn in S1 else R['estimate']['junk_f']['total_cond']),
                  junk_r=(S1[mn]['junk_r'] if mn in S1 else R['estimate']['junk_r']['total_cond']),
                  single=single / q, two=two / q, exploit=expl / q, bully=bully / q,
                  prudent_z=g['prudent_z']['mass'] / q, prudent_o=g['prudent_o']['mass'] / q, prudent_a=g['prudent_a']['mass'] / q, opener=g['opener']['mass'] / q)
        step2[mn] = s2
    json.dump(step2, open(out2, 'w'), indent=1)
    json.dump(rep, open(outrep, 'w'), indent=1, default=str)
    L = ['## Step 2: the length-prior mass of P, Q, O (conditional on finite trees; exact-member lower bounds; R2 = R1 + probn / probp)', '']
    L.append('| machine | q | fair single (lower bound) | bully | P_z | P_o | Q (y variants) | O | MC 95% upper bound on the reader classes (P, Q); other conditionals (O) |')
    L.append('|---|---|---|---|---|---|---|---|---|')
    for mn, r in rep.items():
        q = r['q']
        mcu = r['mc_upper_bound']
        L.append('| %s | %.4f | %.3g | %.3g | %.3g | %.3g | %.3g | %.3g | %s |' % (mn, q, r['single_raw'] / q, r['bully_raw'] / q, r['prudent_z']['cond'], r['prudent_o']['cond'],
                                                                        r['prudent_a']['cond'], r['opener']['cond'], ('%.3g (hits %d of %d); other_cond hits %d, upper %.3g' % (mcu['upper_cond'], mcu['hits'], mcu['n'], mcu['other_cond_hits'], mcu['other_cond_upper_cond'])) if mcu else '-'))
    L.append('')
    L.append('| machine | shortest fair single | shortest bully | shortest P_z (gap) | shortest P any (gap) | shortest O (gap) | P_z / single | P_z / bully | O / single |')
    L.append('|---|---|---|---|---|---|---|---|---|')
    for mn, r in rep.items():
        L.append('| %s | %s | %s | %s (%s) | %s (%s) | %s (%s) | %.3g | %.3g | %.3g |' % (
            mn, r['shortest_single'], r['shortest_bully'], r['prudent_z']['min_size'], r['gap_prudent_z'], r['prudent_all_min_size'], r['gap_prudent_any'],
            r['opener']['min_size'], r['gap_opener'], r['prudent_z']['ratio_to_single'] or 0, r['prudent_z']['ratio_to_bully'] or 0, r['opener']['ratio_to_single'] or 0))
    L.append('')
    for mn, r in rep.items():
        L.append('%s: shortest P_z `%s`; shortest O `%s`; shortest fair single `%s`' % (mn, r['prudent_z']['example'], r['opener']['example'], r['shortest_single_example']))
    open(outmd, 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main(*sys.argv[1:4])
