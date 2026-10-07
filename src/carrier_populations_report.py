"""Report for the carrier-population cells: static diagnostics, chain and lottery tables, verdicts.

    python3 src/carrier_populations_report.py static --arm P
    python3 src/carrier_populations_report.py report
"""
import argparse, json, math, os, sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import carrier_populations as CP
import carrier_populations_run as R

ROOT = R.ROOT
OUT = R.OUT


def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 1.0)
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def leak_test(val):
    """k_at_n8.leak_test: components of mutual cooperation among self-cooperators; closed iff no member cooperates
    with a class that defects on it."""
    K = val.shape[0]
    S = [x for x in range(K) if val[x, x] == 1]
    Sset = set(S)
    mutual = (val == 1) & (val.T == 1)
    comp = {}; comps = []
    for s0 in S:
        if s0 in comp: continue
        stack = [s0]; mem = []; comp[s0] = len(comps)
        while stack:
            a = stack.pop(); mem.append(a)
            for b in np.nonzero(mutual[a])[0]:
                b = int(b)
                if b in Sset and b not in comp:
                    comp[b] = len(comps); stack.append(b)
        comps.append(mem)
    suck = ((val == 1) & (val.T == 0)).any(1)
    closed = [c for c in comps if not suck[c].any()]
    return dict(n_selfcoop=len(S), n_components=len(comps), n_closed=len(closed), closed=closed,
                sizes=sorted((len(c) for c in comps), reverse=True)[:5])


def static_summary(arm, n=7, K=10 ** 6):
    z, info = R.load_static(arm, n, K)
    A = z['A_class']
    U, PCC = CP.pay_matrix(A)
    names = R.class_names(info)
    pr = R.class_props(A, info, arm)
    nc = len(names)
    iD = pr['iD']; iC = names.index('Cc')
    cat_dt = [c['dt'] for c in info['classes']]
    out = dict(arm=arm, n_classes=nc, n_tau=info['n_tau'], n_spellings=info['n_spellings'],
               exec_vs_ideal_diff=info['exec_vs_ideal_diff'], exec_check_steps=info['exec_check_steps'])
    masses = {k[5:]: z[k] for k in z.files if k.startswith('mass_')}
    est = pr['est']; selfc = pr['selfc']; allc = pr['allc']
    # S-guarded: from the representative run tree (rebuild from the dt string is awkward: use the catalogue)
    cat = CP.Catalogue(n, arm, K)
    crep = z['class_rep']
    sg = np.array([CP.s_guarded(cat.tau_dt[cat.tau[int(k)]]) for k in crep])
    prudent = est & (A[:, iC] == 0)
    exploited = np.array([bool(((A[e] == 1) & (A[:, e] == 0)).any()) if est[e] else False for e in range(nc)])
    sucker = (A[:, iD] == 1) & (A[:, iC] == 0)
    def m(mask, pr_='L'): return float(masses[pr_][mask].sum())
    for pr_ in masses:
        out['mass_' + pr_] = dict(establishers=m(est, pr_), s_guarded_est=m(est & sg, pr_), prudent_est=m(prudent, pr_),
                                  exploited_est=m(exploited, pr_), self_cooperators=m(selfc, pr_), unconditional_C=m(allc, pr_),
                                  all_D=m((A == 0).all(1), pr_), D_class=float(masses[pr_][iD]), Cc_class=float(masses[pr_][iC]),
                                  sucker_fringe=m(sucker, pr_))
    out['counts'] = dict(establishers=int(est.sum()), s_guarded=int((est & sg).sum()), prudent=int(prudent.sum()),
                         exploited=int(exploited.sum()), self_cooperators=int(selfc.sum()), unconditional_C=int(allc.sum()),
                         sucker_fringe=int(sucker.sum()), split_classes=info['n_split_classes'])
    # compatible establisher pairs
    E = np.nonzero(est)[0]
    comp = [(int(i), int(j)) for ii, i in enumerate(E) for j in E[ii + 1:] if A[i, j] == 1 and A[j, i] == 1]
    out['compatible_est_pairs'] = len(comp)
    out['est_pairs_total'] = len(E) * (len(E) - 1) // 2
    # shadows of each establisher: neutral entrants that are not establishers and cooperate with D
    sh = {}
    for e in E:
        q = np.nonzero((U[:, e] == U[e, e]) & (U[e, :] == U[e, e]) & ~est & (A[:, iD] == 1))[0]
        sh[int(e)] = q
    out['shadow_mass_by_establisher'] = sorted([(names[e], float(masses['L'][q].sum()), int(len(q))) for e, q in sh.items()],
                                              key=lambda t: -masses['L'][names.index(t[0])])[:15]
    # strict invaders of establishers (exploitation reasons)
    expl = []
    for e in E:
        qs = np.nonzero(U[:, e] > U[e, e] + 1e-9)[0]
        if len(qs):
            expl.append(dict(est=names[e], est_mass=float(masses['L'][e]), s_guarded=bool(sg[e]), n_strict=int(len(qs)),
                             strict_mass=float(masses['L'][qs].sum()), examples=[names[q] for q in qs[np.argsort(-masses['L'][qs])][:3]],
                             dt=cat_dt[e]))
    out['exploited_establishers'] = sorted(expl, key=lambda d: -d['est_mass'])
    # top establishers
    out['establishers'] = [dict(name=names[e], mass_L=float(masses['L'][e]), mass_Lstd=float(masses['Lstd'][e]), s_guarded=bool(sg[e]),
                                prudent=bool(prudent[e]), exploited=bool(exploited[e]), entry=str(pr['entry'][e]),
                                n_spellings=info['classes'][e]['n_spellings'], dt=cat_dt[e])
                           for e in sorted(E, key=lambda e: -masses['L'][e])]
    lt = leak_test(A)
    out['leak'] = dict(n_selfcoop=lt['n_selfcoop'], n_components=lt['n_components'], n_closed=lt['n_closed'], sizes=lt['sizes'],
                       closed=[[names[i] for i in c][:6] for c in lt['closed']][:8])
    if arm == 'E':
        e0 = est & (pr['entry'] == '0'); e5 = est & (pr['entry'] == '5')
        br = []
        for q in range(nc):
            c0 = ((A[q] == 1) & (A[:, q] == 1) & e0).any(); c5 = ((A[q] == 1) & (A[:, q] == 1) & e5).any()
            if c0 and c5:
                br.append(q)
        br = np.array(br, int)
        nonsh = [q for q in br if est[q]]
        out['bridges'] = dict(n=int(len(br)), mass_L=float(masses['L'][br].sum()) if len(br) else 0.0,
                              n_establisher_bridges=len(nonsh), mass_est_bridges=float(masses['L'][nonsh].sum()) if nonsh else 0.0,
                              n_unconditional=int(allc[br].sum()) if len(br) else 0,
                              est_bridges=[dict(name=names[q], mass_L=float(masses['L'][q]), s_guarded=bool(sg[q]),
                                                strict_invaders=int((U[:, q] > U[q, q] + 1e-9).sum()), dt=cat_dt[q])
                                           for q in sorted(nonsh, key=lambda q: -masses['L'][q])][:20],
                              entry_mass=dict(e0=float(masses['L'][e0].sum()), e5=float(masses['L'][e5].sum())))
    return out


def cmd_static(a):
    out = static_summary(a.arm, a.n)
    json.dump(out, open(os.path.join(OUT, 'static_summary_%s.json' % a.arm), 'w'), indent=1, default=str)
    print(json.dumps({k: v for k, v in out.items() if k not in ('establishers', 'exploited_establishers')}, indent=1, default=str)[:6000])


def _J(name):
    f = os.path.join(OUT, name)
    return json.load(open(f)) if os.path.exists(f) else None


def fmt(x, d=4):
    if x is None: return '–'
    if isinstance(x, str): return x
    if x == 0: return '0'
    if isinstance(x, int) and abs(x) < 10 ** 6: return str(x)
    if abs(x) < 1e-3 or abs(x) >= 1e5: return '%.2e' % x
    return ('%.' + str(d) + 'f') % x


def lottery_table(rows):
    by = defaultdict(list)
    for r in rows: by[(r['arm'], r['prior'])].append(r)
    out = []
    for (arm, prior), R in sorted(by.items()):
        n = len(R)
        d = dict(arm=arm, prior=prior, runs=n)
        for E in ('E1', 'E2', 'E3'):
            k = sum(1 for r in R if r[E] == 'success'); f = sum(1 for r in R if r[E] == 'fail')
            gens = sorted(r[E + '_gen'] for r in R if r[E] != 'censored')
            d[E] = dict(success=k, fail=f, censored=n - k - f, wilson=wilson(k, n),
                        median_gen=float(np.median(gens)) if gens else None)
        est = [r['establish_gen'] for r in R if r['establish_gen'] >= 0]
        d['establish_median'] = float(np.median(est)) if est else None
        d['establish_by_100'] = sum(1 for e in est if e <= 100)
        win = defaultdict(int)
        for r in R:
            if r['E3'] == 'success': win[r['top_final'][0][0]] += 1
        d['winners_E3'] = sorted(win.items(), key=lambda kv: -kv[1])[:6]
        lose = defaultdict(int)
        for r in R:
            if r['E3'] == 'fail': lose[r['top_final'][0][0]] += 1
        d['losers_E3'] = sorted(lose.items(), key=lambda kv: -kv[1])[:4]
        d['pcc_final_mean'] = float(np.mean([r['pcc_final'] for r in R]))
        if arm == 'E':
            d['both_entries_alive_final'] = sum(1 for r in R if r['entries_alive_final']['e0'] and r['entries_alive_final']['e5'])
            d['bridge_alive_final'] = sum(1 for r in R if r['entries_alive_final']['both'])
            d['both_entries_ever'] = sum(1 for r in R if r['both_entries_first'] >= 0)
            d['merges'] = [m for r in R for m in r['merges']]
        out.append(d)
    return out


def cmd_report(a):
    L = []
    J = {}
    W = L.append
    W('# Run: the realizable language, milestone 2: populations of carriers (2026-10-06)')
    W('')
    W('Spec `specs/2026-10-06-carrier-populations.md`; notes `notes/carrier-populations.md`; predictions '
      '`predictions/2026-10-06-carrier-populations.md`; code `src/carrier_populations.py`, `src/carrier_populations_run.py`, '
      '`src/carrier_populations_report.py`, `tests/test_carrier_populations.py`; raw arrays in `runs/carrier_populations/` (npz not '
      'committed). K = 10⁶, V = K/4, PD payoffs of the modal arm, w = 0.3. "Classes" are the exact lumped classes over '
      'spellings (rows and columns against every spelling, self and cross-twin cells included).')
    W('')
    # 1. scale guard
    W('## 1. Scale guard, costs, and the ideal-verification control')
    W('')
    W('| arm | spellings | τ-types | classes (split singletons) | ideal pair checks (s) | executable class checks (s) | exec ≠ ideal cells | exec TO (all at V: regress) | ideal TO | largest non-TO exec check | median |')
    W('|---|---|---|---|---|---|---|---|---|---|---|')
    for arm in ('P', 'O', 'E'):
        st = _J('static_%s_n7_K1000000.json' % arm)
        if not st: continue
        J['static_' + arm] = {k: v for k, v in st.items() if k != 'classes'}
        steps = np.load(os.path.join(OUT, 'exec_steps_%s_n7_K1000000.npy' % arm))
        sv = steps[:, 4] if len(steps) else np.zeros(0)
        below = sv[sv < st['V']]
        W('| %s | %d | %d | %d (%d) | %d (%.0f) | %d (%.0f) | %d | %d | %d | %d | %d |' % (
            arm, st['n_spellings'], st['n_tau'], st['n_classes'], st['n_split_classes'], st['ideal_pair_checks'], st['ideal_s'],
            st['exec_pair_checks'], st['exec_s'], st['exec_vs_ideal_diff'], st['exec_TO'], st['ideal_TO'],
            int(below.max()) if len(below) else 0, int(np.median(sv)) if len(sv) else 0))
    W('')
    W('Executable TO counts are smaller than ideal TO counts only because the executable table is computed on class '
      'representatives and the ideal one on every τ-type pair; on the class cells the two tables are identical, so the '
      'chain and lottery under the ideal table are the same computation (RE 7 / S11).')
    W('')
    ks = _J('ksens_P.json')
    if ks:
        J['ksens'] = ks
        W('**K sensitivity (P, every class cell, sources and lists rebuilt at each K, V = K/4):**')
        W('')
        W('| K | lists equal to K = 10⁶ | cells differing from K = 10⁶ | of which between establishers | checks at the cap | largest check below the cap |')
        W('|---|---|---|---|---|---|')
        for k, v in sorted(ks.items(), key=lambda kv: int(kv[0])):
            W('| %s | %d / %d | %d | %d | %d | %s |' % (fmt(int(k)), v['lists_equal'], v['n_classes'], v['n_diff'], v['n_diff_establisher_pairs'],
                                                       v['n_at_cap'], v['max_below_cap']))
        W('')
    va = _J('validate.json')
    if va:
        J['validate'] = va
        W('**Validation (notes §1.10):** Lemma T / composition sample %d pairs, %d mismatches; class-table sample %d cells, %d '
          'mismatches; empty-selection shortcut %d checks, %d mismatches; n ≤ 5 chain: P(C,C) unlumped / lumped / twin-expanded '
          '%s at N = 10³ and %s at 10⁴.' % (
              va['lemmaT_sample']['n'], va['lemmaT_sample']['mismatches'], va['class_table_sample']['n'], va['class_table_sample']['mismatches'],
              va['empty_selection']['n'], va['empty_selection']['mismatches'],
              ' / '.join('%.9f' % va['small_chain']['rows'][0][k][0] for k in ('unlumped', 'lumped', 'lumped_twins')),
              ' / '.join('%.9f' % va['small_chain']['rows'][1][k][0] for k in ('unlumped', 'lumped', 'lumped_twins'))))
        W('')
    # 2. static
    W('## 2. Static structure')
    W('')
    for arm in ('P', 'O', 'E'):
        ss = _J('static_summary_%s.json' % arm)
        if not ss: continue
        J['static_summary_' + arm] = ss
        W('### Arm %s' % arm)
        W('')
        W('| prior | establishers | S-guarded est. | prudent est. (refuse Cc) | exploited est. | self-cooperators | unconditional C | all-D rows | D class | Cc class | sucker fringe |')
        W('|---|---|---|---|---|---|---|---|---|---|---|')
        for pr_ in ('L', 'U', 'Lstd', 'Leq'):
            m = ss.get('mass_' + pr_)
            if not m: continue
            W('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (pr_, *(fmt(m[k], 3) for k in (
                'establishers', 's_guarded_est', 'prudent_est', 'exploited_est', 'self_cooperators', 'unconditional_C', 'all_D', 'D_class', 'Cc_class', 'sucker_fringe'))))
        c = ss['counts']
        W('')
        W('Counts: %d classes; establishers %d (S-guarded %d, prudent %d, exploited %d); self-cooperators %d; unconditional '
          'cooperators %d; sucker fringe %d; compatible establisher pairs %d of %d. Leak test: %d self-cooperating classes in %d '
          'components (largest %s), **%d closed**: %s.' % (
              ss['n_classes'], c['establishers'], c['s_guarded'], c['prudent'], c['exploited'], c['self_cooperators'], c['unconditional_C'],
              c['sucker_fringe'], ss['compatible_est_pairs'], ss['est_pairs_total'], ss['leak']['n_selfcoop'], ss['leak']['n_components'],
              ss['leak']['sizes'][:3], ss['leak']['n_closed'], '; '.join('`%s`' % x[0] for x in ss['leak']['closed'][:4])))
        W('')
        W('Heaviest establishers (L):')
        W('')
        W('| class | mass L | mass L_std | S-guarded | prudent | exploited | run tree |')
        W('|---|---|---|---|---|---|---|')
        for e in ss['establishers'][:12]:
            W('| `%s` | %s | %s | %s | %s | %s | `%s` |' % (e['name'], fmt(e['mass_L']), fmt(e['mass_Lstd']), e['s_guarded'], e['prudent'], e['exploited'], e['dt']))
        W('')
        W('Exploited establishers, heaviest (strict invaders: count, mass, examples):')
        W('')
        for e in ss['exploited_establishers'][:6]:
            W('- `%s` (mass %s): %d strict invaders of mass %s, e.g. %s' % (e['est'], fmt(e['est_mass']), e['n_strict'], fmt(e['strict_mass'], 3),
                                                                          ', '.join('`%s`' % x for x in e['examples'])))
        W('')
        if 'bridges' in ss:
            b = ss['bridges']
            W('**Bridges (E):** %d classes cooperate mutually with an entry-0 establisher and an entry-5 establisher (mass L %s); '
              '%d of them are establishers (mass %s), %d unconditional cooperators. Establisher mass by entry: entry 0 %s, entry 5 %s.' % (
                  b['n'], fmt(b['mass_L']), b['n_establisher_bridges'], fmt(b['mass_est_bridges']), b['n_unconditional'],
                  fmt(b['entry_mass']['e0']), fmt(b['entry_mass']['e5'])))
            W('')
            for e in b['est_bridges'][:8]:
                W('- `%s` mass %s, S-guarded %s, strict invaders %d' % (e['name'], fmt(e['mass_L']), e['s_guarded'], e['strict_invaders']))
            W('')
    # 3. chain
    ch = _J('chain_main.json') or []
    ch2 = _J('chain_E.json') or []
    ch3 = _J('chain_O.json') or []
    ch4 = (_J('chain_noclosed.json') or []) + (_J('chain_noclosed2.json') or [])
    ch5 = (_J('chain_noclosed_cutdiag.json') or []) + (_J('chain_cutdiag.json') or [])
    rows0 = ch + ch2 + ch3 + ch4 + ch5
    seen = {}
    for r in rows0:                      # later files (with the cut diagnostic) replace earlier rows of the same cell
        seen[(r['arm'], r['prior'], r['N'], r['twins'], r['label'])] = r
    rows = list(seen.values())
    J['chain'] = rows
    W('## 3. The ε→0 chain')
    W('')
    W('| arm | prior | label | twins | N | P(C,C) | π(all-D) | π(coop states) | top cooperative state (π) | its exit per event: total / neutral / strict | entry from all-D (coop share) | states | cut/flow |')
    W('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for r in sorted(rows, key=lambda r: (r['label'], r['arm'], r['prior'], not r['twins'], r['N'])):
        t = r['top_coop'] or {}
        e = r['entry_D'] or {}
        W('| %s | %s | %s | %s | %s | %s | %s | %s | `%s` (%s) | %s / %s / %s | %s (%s) | %d | %s |' % (
            r['arm'], r['prior'], r['label'], 'yes' if r['twins'] else 'no', fmt(r['N']), fmt(r['pcc']), fmt(r['pi_D']), fmt(r['pi_coop']),
            (t.get('state') or '')[:70], fmt(t.get('pi')), fmt(t.get('exit_total')), fmt(t.get('exit_neutral')), fmt(t.get('exit_strict')),
            fmt(e.get('total_rate')), fmt((e.get('coop_rate') or 0) / e['total_rate'] if e.get('total_rate') else None, 3), r['n_recurrent'], fmt(r['cut_rel'])))
    W('')
    cd = [r for r in rows if r.get('cut_rel') and r['cut_rel'] > 0.02]
    if cd:
        W('**Cells with unexplored flow above 2% and their cut diagnostic** (share of the dropped flow by destination and source):')
        W('')
        for r in cd:
            W('- %s × %s, %s, N = %s: cut/flow %s (absolute dropped flow %s per event): %s' % (
                r['arm'], r['prior'], r['label'], fmt(r['N']), fmt(r['cut_rel']), fmt(r['cut_flow']),
                ', '.join('%s %s' % (k, fmt(v, 3)) for k, v in sorted((r.get('cut_diagnostic') or {'not computed': None}).items()))))
        W('')
    # support and transitions for the main cells at 1e4
    for r in rows:
        if r['N'] != 10000 or not r['twins'] or r['prior'] in ('Leq',) or (r['label'] == 'main' and r['arm'] in ('O', 'E')): continue
        W('**Support and transitions, %s × %s, %s, N = 10⁴:**' % (r['arm'], r['prior'], r['label']))
        W('')
        for sp in r['support'][:6]:
            ex = '; '.join('→ %s (10^%.1f; %s)' % (x['to'][:50], x['log10_rate'], ', '.join('%s' % m[0] for m in x['mutants'][:2])) for x in sp['exits'][:3])
            W('- `%s` π %s, P(C,C) %s, log10 exit %s: %s' % (sp['state'][:80], fmt(sp['pi']), fmt(sp['coop'], 2), fmt(sp['log10_exit'], 1), ex))
        t = r['top_coop']
        if t:
            W('- decisive exits of the top cooperative state: ' + '; '.join(
                '`%s` %s (Δ1 %s, Δ2 %s, ρ %s, N·ρ %s, N·Δ1 %s)' % (x['mutant'][:50], x['type'], fmt(x['d1'], 2), fmt(x['d2'], 2), fmt(x['rho']), fmt(x['N_rho'], 2), fmt(x['N_d1'], 1))
                for x in t['exits'][:4]))
        e = r['entry_D']
        if e:
            W('- entry from all-D: ' + '; '.join('`%s` (Δ1 %s, Δ2 %s, ρ %s, N·ρ %s)' % (x['mutant'][:50], fmt(x['d1'], 2), fmt(x['d2'], 2), fmt(x['rho']), fmt(x['N_rho'], 2))
                                                  for x in e['top'][:4]))
        W('')
    # slopes
    W('**Local slopes** of log(π(coop)/π(all-D)) and of log(P(C,C)/(1 − P(C,C))) in log N:')
    W('')
    W('| arm | prior | label | 10³→10⁴ | 10⁴→3·10⁴ | 3·10⁴→10⁵ |')
    W('|---|---|---|---|---|---|')
    grp = defaultdict(dict)
    for r in rows:
        if r['twins']: grp[(r['arm'], r['prior'], r['label'])][r['N']] = r
    slopes = {}
    for k, d in sorted(grp.items()):
        Ns = sorted(d)
        cells = []
        for a_, b_ in zip(Ns, Ns[1:]):
            def lo(r):
                pc, pd = r['pi_coop'], r['pi_D']
                q = r['pcc']
                o1 = math.log(pc / pd) if pc > 0 and pd > 0 else None
                o2 = math.log(q / (1 - q)) if 1e-9 < q < 1 - 1e-9 else None
                return o1, o2
            (x1, y1), (x2, y2) = lo(d[a_]), lo(d[b_])
            dl = math.log(b_ / a_)
            s1 = (x2 - x1) / dl if x1 is not None and x2 is not None else None
            s2 = (y2 - y1) / dl if y1 is not None and y2 is not None else None
            cells.append('%s / %s' % (fmt(s1, 2), fmt(s2, 2)))
        slopes[str(k)] = cells
        W('| %s | %s | %s | %s |' % (k[0], k[1], k[2], ' | '.join(cells)))
    J['slopes'] = slopes
    W('')
    # 4. lottery
    W('## 4. The ε = 0 lottery ((N, I) = (100, 64), mN = 1, horizon 2,000 generations)')
    W('')
    lrows = (_J('lottery_main.json') or []) + (_J('lottery_E.json') or [])
    lt = lottery_table(lrows)
    J['lottery'] = lt
    W('| arm | prior | runs | E1 success / fail / censored [Wilson] | E2 | E3 success / fail / censored [Wilson] | median decision gen (E3) | first island at P(C,C) ≥ 0.9: median gen, by 100 | final P(C,C) | E3 winners (top class) |')
    W('|---|---|---|---|---|---|---|---|---|---|')
    for d in lt:
        def e(E): x = d[E]; return '%d / %d / %d [%.2f, %.2f]' % (x['success'], x['fail'], x['censored'], *x['wilson'])
        W('| %s | %s | %d | %s | %s | %s | %s | %s, %d | %s | %s |' % (d['arm'], d['prior'], d['runs'], e('E1'), e('E2'), e('E3'), fmt(d['E3']['median_gen'], 0),
                                                                fmt(d['establish_median'], 0), d['establish_by_100'], fmt(d['pcc_final_mean'], 3),
                                                                ', '.join('`%s` %d' % (w[0][:45], w[1]) for w in d['winners_E3'][:3])))
    W('')
    for d in lt:
        if d['arm'] == 'E':
            W('E arm: both entries\' establishers alive at the end in %d / %d runs (ever both alive: %d); an establisher bridge alive at the end in %d; '
              'merges (one entry\'s last establisher lost after both were present): %d, at generations %s.' % (
                  d['both_entries_alive_final'], d['runs'], d['both_entries_ever'], d['bridge_alive_final'], len(d['merges']), d['merges'][:20]))
            W('')
    vf = os.path.join(OUT, 'verdicts.md')
    if os.path.exists(vf):
        L.append(open(vf).read())
    open(os.path.join(ROOT, 'runs', 'carrier-populations.md'), 'w').write('\n'.join(L) + '\n')
    json.dump(J, open(os.path.join(ROOT, 'runs', 'carrier-populations.json'), 'w'), indent=1, default=str)
    print('\n'.join(L))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('static'); s.add_argument('--arm', default='P'); s.add_argument('--n', type=int, default=7)
    s = sub.add_parser('report')
    a = ap.parse_args()
    {'static': cmd_static, 'report': cmd_report}[a.cmd](a)
