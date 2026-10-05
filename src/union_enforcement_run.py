"""Runner for the enforcement experiment (specs/2026-10-05-enforcement.md).

    python3 src/union_enforcement_run.py partA
    python3 src/union_enforcement_run.py partB          # reduced chains, 3 workers
    python3 src/union_enforcement_run.py audit          # full-language tensors: stabilization, strikes at s > 0
    python3 src/union_enforcement_run.py partC --arm RC --pool 1 --c 0.5 --N 1000
Writes runs/enforcement/*.json.
"""
import argparse, json, os, sys, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import union as U
import union_enforcement as E

OUT = E.OUT


def run_part_a(args):
    os.makedirs(OUT, exist_ok=True)
    res = {}
    for lev in ((0, 1), (0,)):
        t = time.time()
        res['levels_%s' % ''.join(map(str, lev))] = E.part_a(levels=lev)
        print('part A levels', lev, '%.0fs' % (time.time() - t), flush=True)
    json.dump(res, open(os.path.join(OUT, 'part_a.json'), 'w'), indent=1, default=float)


_BASE = None


def _cell(key):
    global _BASE
    if _BASE is None:
        _BASE = E.make_base()
    arm, pool, c, tie, prior, N = key
    return key, E.reduced_cell(_BASE, arm, pool, c, tie, prior, N)


def run_part_b(args):
    from multiprocessing import Pool
    os.makedirs(OUT, exist_ok=True)
    E.make_base()                      # build the class cache once
    keys = [(arm, pool, c, tie, prior, N) for arm in E.ARMS for pool in (0, 1) for c in (0.1, 0.5) for tie in ('whack', 'nowhack')
            for prior in ('uniform', 'mu') for N in (100, 1000, 10000)]
    with Pool(args.workers) as p:
        res = dict(p.map(_cell, keys))
    out = {'%s|pool%d|c%g|%s|%s|N%d' % k: v for k, v in res.items()}
    base = E.make_base()
    static = {}
    for arm in E.ARMS:
        for pool in (0, 1):
            for c in (0.1, 0.5):
                static['%s|pool%d|c%g' % (arm, pool, c)] = E.reduced_static(base, arm, pool, c, 'whack')
    json.dump(dict(cells=out, static=static,
                   masses=dict(boss={base[2][i]: float(base[5][i]) for i in range(9)}, worker=dict(zip(E.NAMED_W, map(float, base[6]))))),
              open(os.path.join(OUT, 'part_b.json'), 'w'), indent=1, default=float)
    print('part B: %d cells' % len(out))


def run_audit(args):
    """Full-language tensors in every (arm, pool, c, tie): every encounter stabilizes;
    implemented strikes at s > 0 under rational workers (S1)."""
    d, C, nmw, nmb = E.load_base()
    P = d['P']; TAG = P.tag.astype(np.int64)
    out = {}
    for arm, (rb, rw) in E.ARMS.items():
        for pool in (0, 1):
            for c in (0.1, 0.5):
                for tie in ('whack', 'nowhack'):
                    if not pool and tie == 'nowhack':
                        continue
                    t = time.time()
                    J = E.tensor_e(*P.arrays(), U.TT, P.KB, P.KW, TAG, rb, rw, pool, c, E.TIES[tie])
                    b = J // 4; si = b // 3; a1 = (J // 2) % 2; a2 = J % 2
                    out['%s|pool%d|c%g|%s' % (arm, pool, c, tie)] = dict(
                        unstable=int((J < 0).sum()), encounters=int(J.size),
                        strikes_at_positive_wage=int((((a1 == 1) | (a2 == 1)) & (si > 0) & (J >= 0)).sum()),
                        strikes_total=int((((a1 == 1) | (a2 == 1)) & (J >= 0)).sum()),
                        source_targeting_implemented=int(((b % 3) == 2).sum()))
                    print(arm, pool, c, tie, out['%s|pool%d|c%g|%s' % (arm, pool, c, tie)], '%.0fs' % (time.time() - t), flush=True)
    json.dump(out, open(os.path.join(OUT, 'audit_full.json'), 'w'), indent=1)


def run_part_c(args):
    """Full chain in one (arm, pool) cell: classes re-lumped under the modified
    evaluator, class masses = sums of the frozen function masses."""
    from union_chain import UChain
    from union_run import analyse, seeds
    t = time.time()
    d, C0, nmw_f, nmb_f = E.load_base()
    P = d['P']; TAG = P.tag.astype(np.int64)
    rb, rw = E.ARMS[args.arm]
    tag = '%s_pool%d_c%g_N%d_%s' % (args.arm, args.pool, args.c, args.N, args.tie)
    J = E.tensor_e(*P.arrays(), U.TT, P.KB, P.KW, TAG, rb, rw, args.pool, args.c, E.TIES[args.tie])
    C = U.classes(d, J=J); C.pop('J')
    nmw = {k: (int(C['cw'][v]) if v is not None else None) for k, v in nmw_f.items()}
    nmb = {k: int(C['cb'][v]) for k, v in nmb_f.items()}
    print('classes: boss %d worker %d (%.0fs)' % (C['KcB'], C['KcW'], time.time() - t), flush=True)
    ch = UChain(C, args.c, args.N, w=0.3, theta=args.theta, arm='quorum', verbose=True)
    PAY, REP = E.payoff_table_e(args.c, args.pool)
    ch.PAY = PAY
    ch.explore_hybrid(seeds(ch, nmw, nmb))
    a = argparse.Namespace(arm=tag, c=args.c, N=args.N, w=0.3, theta=args.theta)
    out = analyse(ch, d, C, nmw, nmb, a)
    # enforcement statistics on the explored chain
    typ = ch.typ; pi = ch.pi
    j = typ // 4; t1 = (typ // 2) % 2; t2 = typ % 2
    b = j // 4; h = b % 3; a1 = (j // 2) % 2; a2 = j % 2
    striker = (a1 == 1) | (a2 == 1)
    wst = ((h == 0) & striker) | ((h == 2) & (((a1 == 1) & (t1 == 1)) | ((a2 == 1) & (t2 == 1))))
    out['strike_incidence'] = float(pi[striker].sum())
    out['repression_given_strike'] = float(pi[wst].sum() / pi[striker].sum()) if pi[striker].sum() > 0 else None
    sur = np.array([E.surplus(int(j[k]), int(t1[k]), int(t2[k]), PAY, REP) for k in range(len(j))])
    out['total_surplus'] = float(pi @ sur)
    out['class_counts'] = dict(boss=int(C['KcB']), worker=int(C['KcW']))
    out['tie'] = args.tie; out['pool'] = args.pool; out['enf_arm'] = args.arm
    out['time_s'] = time.time() - t
    json.dump(out, open(os.path.join(OUT, 'partC_%s.json' % tag), 'w'), indent=1, default=float)
    print(json.dumps({k: out[k] for k in ('states', 'rel_cut_change', 'summary', 'efficiency', 'total_surplus', 'mean_payoff',
                                          'strike_incidence', 'repression_given_strike', 'time_s')}, indent=1, default=float))


SH = ['fair', 'intermediate', 'zero wage', 'strike', 'scab split', 'repression:strike', 'repression:source']


def _f(x, d=3):
    if x is None:
        return '–'
    if x != 0 and abs(x) < 10 ** (-d):
        return '%.1e' % x
    return ('%.' + str(d) + 'f') % x


def run_report(args):
    """Markdown tables for runs/enforcement.md (written to runs/enforcement/tables.md)
    and the collected runs/enforcement.json."""
    A = json.load(open(os.path.join(OUT, 'part_a.json')))
    B = json.load(open(os.path.join(OUT, 'part_b.json')))
    cells = B['cells']
    L = []
    # Part A
    for lev, R in A.items():
        L.append('### Part A, boss language %s (%d functions; constants %.3f of μ)\n' % (lev, R['boss_functions'], R['boss_mass']['constants']))
        L.append('Audit: %d encounters, %d violations, %d Lemma 0 counterexamples.\n' % (R['audit']['encounters'], R['audit']['violations'], R['audit']['lemma0_counterexamples']))
        L.append('| self-pair | strikes, s(w0) low | works, s(w0) low | strikes, s(w0) fair | works, s(w0) fair |')
        L.append('|---|---|---|---|---|')
        for k, v in R['self_pair_activation'].items():
            L.append('| %s | %d | %d | %d | %d |' % (k, v['strike_w0low'], v['work_w0low'], v['strike_w0fair'], v['work_w0fair']))
        L.append('')
        L.append('| pair (W1 \\| W2) | low, struck | low, worked (of which fakers: fair at w0) | fair, worked | fair, struck (self-harm) |')
        L.append('|---|---|---|---|---|')
        for k, v in R['pairs'].items():
            g = lambda key: v.get(key, dict(n=0, mass=0.0))
            lw = g('low worked'); lf = g('low worked (faker: fair at world 0)')
            L.append('| %s | %d (%.4f) | %d (%.4f); fakers %d (%.4f) | %d (%.4f) | %d (%.4f) |' % (
                k.replace('|', '\\|'), g('low struck')['n'], g('low struck')['mass'], lw['n'] + lf['n'], lw['mass'] + lf['mass'], lf['n'], lf['mass'],
                g('fair worked')['n'], g('fair worked')['mass'], g('fair struck')['n'], g('fair struck')['mass']))
        L.append('')
    L.append('### Part A traces (levels {0,1}; committed play)\n')
    for k, v in A['levels_01']['traces'].items():
        L.append('- `%s`' % k)
        for line in v[:4]:
            L.append('  - `%s`' % line)
    L.append('')
    # Part B main tables
    def row(k, label):
        v = cells[k]
        return '| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            label, ' | '.join(_f(v['summary'][s]) for s in SH), _f(v['strike_incidence']), _f(v['repression_given_strike']),
            _f(v['realized_repression']), _f(v['mean_payoff']['boss']), _f(v['mean_payoff']['W1']), _f(v['efficiency_slots']),
            _f(v['total_surplus']), _f(v['zero_strike_boss_mass']))
    hdr = ('| cell | fair | interm. | zero | strike | scab split | rep:strike | rep:source | strike inc. | rep \\| strike | realized rep. | boss | worker | eff. (slots) | total surplus | (0,strike) boss |\n'
           '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for prior in ('uniform', 'mu'):
        for c in (0.5, 0.1):
            for N in (1000, 100, 10000):
                L.append('### Reduced chain, %s prior, c = %g, N = %d (tie = whack)\n' % ('uniform' if prior == 'uniform' else 'length', c, N))
                L.append(hdr)
                for arm in ('CC', 'RC', 'CR', 'RR'):
                    for pool in (0, 1):
                        L.append(row('%s|pool%d|c%g|whack|%s|N%d' % (arm, pool, c, prior, N), arm + (' + pool' if pool else '')))
                L.append('')
    mx = 0.0
    for k, v in cells.items():
        if '|whack|' in k:
            v2 = cells[k.replace('|whack|', '|nowhack|')]
            mx = max(mx, max(abs(v['summary'][s] - v2['summary'][s]) for s in SH))
    L.append('Tie rule at 1 − s = c: max |Δ| over all summaries and cells between tie = whack and tie = nowhack: %g.\n' % mx)
    # threats
    L.append('### Committed threats: payoff advantage over the feasible deviation (uniform prior, N = 10³)\n')
    L.append('| c | cell | boss threat untriggered: π mass, value if called | boss whack executed: π mass, advantage | worker strike executed: π mass (each slot), advantage |')
    L.append('|---|---|---|---|---|')
    for c in (0.5, 0.1):
        for arm in ('CC', 'RC', 'CR', 'RR'):
            for pool in (0, 1):
                v = cells['%s|pool%d|c%g|whack|uniform|N1000' % (arm, pool, c)]['threats']
                g = lambda key: ('%s, %s' % (_f(v[key]['mass']), _f(v[key]['mean_adv'], 2))) if key in v else '– (not committed or never)'
                L.append('| %g | %s | %s | %s | %s |' % (c, arm + (' + pool' if pool else ''), g('boss_if_called'), g('boss_exec'), g('w1_exec')))
    L.append('')
    # support and transitions
    for c in (0.5,):
        for arm in ('CC', 'RC', 'CR', 'RR'):
            for pool in (0, 1):
                v = cells['%s|pool%d|c%g|whack|uniform|N1000' % (arm, pool, c)]
                L.append('#### Support and transitions: %s%s, uniform, c = %g, N = 10³ (99%% of π on %d of 81 states)\n' % (arm, ' + pool' if pool else '', c, v['support_size_99']))
                L.append('| π | state (boss, W1, W2) | implemented play | summary |')
                L.append('|---|---|---|---|')
                for s in v['support'][:6]:
                    L.append('| %s | %s | %s | %s |' % (_f(s['pi'], 4), s['state'], s['play'], s['summary']))
                cur = sorted(v['currents'].items(), key=lambda kv: -kv[1])[:6]
                L.append('\nLargest currents between summaries (per mutation event): ' + '; '.join('%s %.1e' % (k, x) for k, x in cur) + '.')
                t = v['transitions'][0]
                L.append('Exits from the top state `%s`: total %.1e per event (strict %.1e, neutral %.1e, deleterious %.1e); top moves: %s.\n' % (
                    t['state'], t['exit_total'], t['by_kind']['strict'], t['by_kind']['neutral'], t['by_kind']['deleterious'],
                    '; '.join('%s → %s (%s, %.1e)' % (e['slot'], e['to'], e['kind'], e['p']) for e in t['top'][:3])))
    # full-language audit
    au = json.load(open(os.path.join(OUT, 'audit_full.json'))) if os.path.exists(os.path.join(OUT, 'audit_full.json')) else {}
    if au:
        L.append('### Full-language tensors (297 boss × 452 × 452 worker functions)\n')
        L.append('| arm \\| pool \\| c \\| tie | unstable | strikes at s > 0 | strikes | implemented source targeting |')
        L.append('|---|---|---|---|---|')
        for k, v in au.items():
            L.append('| %s | %d | %d | %d | %d |' % (k.replace('|', ' \\| '), v['unstable'], v['strikes_at_positive_wage'], v['strikes_total'], v['source_targeting_implemented']))
        L.append('')
    # Part C
    pc = sorted(f for f in os.listdir(OUT) if f.startswith('partC_') and f.endswith('.json'))
    if pc:
        L.append('### Part C, full chain, length prior, N = 10³\n')
        L.append('| cell | θ | states | outcome cut | classes B/W | fair | interm. | zero | strike | scab split | rep:strike | rep:source | strike inc. | rep \\| strike | boss | worker | eff. | total surplus |')
        L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        for f in pc:
            d = json.load(open(os.path.join(OUT, f)))
            L.append('| %s | %g | %d | %s | %d/%d | %s | %s | %s | %s | %s | %s | %s |' % (
                f[6:-5], d['theta'], d['states'], _f(d['rel_cut_change']), d['class_counts']['boss'], d['class_counts']['worker'],
                ' | '.join(_f(d['summary'][s], 4) for s in SH), _f(d['strike_incidence'], 4), _f(d['repression_given_strike']),
                _f(d['mean_payoff']['boss']), _f(d['mean_payoff']['W1'], 4), _f(d['efficiency']), _f(d['total_surplus'])))
        L.append('')
        for f in pc:
            d = json.load(open(os.path.join(OUT, f)))
            L.append('#### Support and transitions: %s\n' % f[6:-5])
            L.append('Whack policy held (implemented): %s; conditional programs hold %s of π; 99%% of π on %d states.\n' % (
                ', '.join('%s %s' % (k, _f(x)) for k, x in d['whack_policy_dist'].items()), _f(d['mass_with_conditional']), d['support_size_99']))
            L.append('| π | state | summary |')
            L.append('|---|---|---|')
            for s in d['support'][:6]:
                L.append('| %s | `%s` | %s |' % (_f(s['pi'], 4), s['state'], s['summary']))
            t = d['transitions'][0]
            L.append('\nExits from `%s`: %s; top: %s. Net currents: %s.\n' % (
                t['state'], ', '.join('%s %.1e' % (k, x) for k, x in t['exit_by_kind'].items()),
                '; '.join('%s %s (%s, %.1e) → %s' % (e['slot'], e['mutant'], e['kind'], e['p'], e['to']) for e in t['top'][:3]),
                '; '.join('%s %.1e' % (k, x) for k, x in sorted(d['net_currents'].items(), key=lambda kv: -abs(kv[1]))[:4])))
    open(os.path.join(OUT, 'tables.md'), 'w').write('\n'.join(L) + '\n')
    # collected json (without the per-state pi dumps)
    slim = {k: {kk: vv for kk, vv in v.items() if kk not in ('pi_all',)} for k, v in cells.items()}
    coll = dict(part_a=A, part_b=dict(cells=slim, masses=B['masses']), audit_full=au,
                part_c={f[6:-5]: json.load(open(os.path.join(OUT, f))) for f in pc})
    json.dump(coll, open(os.path.join(ROOT_RUNS, 'enforcement.json'), 'w'), indent=1, default=float)
    print('wrote tables.md and enforcement.json')


ROOT_RUNS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'runs')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['partA', 'partB', 'audit', 'partC', 'report'])
    ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--arm', default='RC')
    ap.add_argument('--pool', type=int, default=1)
    ap.add_argument('--c', type=float, default=0.5)
    ap.add_argument('--N', type=float, default=1000)
    ap.add_argument('--tie', default='whack')
    ap.add_argument('--theta', type=float, default=1e-9)
    a = ap.parse_args()
    {'partA': run_part_a, 'partB': run_part_b, 'audit': run_audit, 'partC': run_part_c, 'report': run_report}[a.what](a)
