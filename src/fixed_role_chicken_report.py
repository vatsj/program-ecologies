"""Report for the fixed-role chicken experiment: runs/fixed-role-chicken.md and runs/fixed-role-chicken.json from the
cell outputs in runs/fixed_role_chicken/ (static.json, chain.json, onepop_chain.json, lottery_<set>.json) and the
hand-written verdicts in runs/fixed_role_chicken/verdicts.md.

    python3 src/fixed_role_chicken_report.py
"""
import json, math, os, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixed_role_chicken as F

OUT = F.OUT
ROOT = F.ROOT


def load(name):
    p = os.path.join(OUT, name)
    return json.load(open(p)) if os.path.exists(p) else None


def tci(xs):
    xs = np.asarray(xs, float)
    n = len(xs)
    if n == 0:
        return float('nan'), float('nan')
    m = xs.mean()
    if n < 2:
        return m, float('nan')
    tq = {39: 2.023, 19: 2.093}.get(n - 1, 1.96)
    return float(m), float(tq * xs.std(ddof=1) / math.sqrt(n))


def wilson(k, n, z=1.96):
    if n == 0:
        return (float('nan'), float('nan'))
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def f(x, p=3):
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return '–'
    return ('%.' + str(p) + 'f') % x


def e(x):
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return '–'
    if x == 0:
        return '0'
    return '%.2e' % x


def cell_key(r):
    return (r['kind'], r['arm'], r['game'], r['N'], r['mN'], r.get('bridges', True))


def summarize_cell(rows, mark):
    """two-population cell statistics at a horizon mark."""
    ms = [r['marks'][str(mark)] for r in rows if str(mark) in r['marks']]
    if not ms:
        return None
    I = rows[0]['I']
    est = [m['est_frac'] for m in ms]
    e1 = sum(m['est_R1'] for m in ms); e2 = sum(m['est_R2'] for m in ms)
    cls = Counter()
    for m in ms:
        cls.update(m['counts'])
    tot = sum(cls.values())
    pw = sum(m['patchwork'] for m in ms)
    single = sum(m['single_convention'] for m in ms)
    ever = sum(m['ever_patchwork'] for m in ms)
    res = [m for m in ms if m['resolved']]
    e3res = [m['e3_resolved_gen'] for m in ms if m['e3_resolved_gen'] is not None]
    flips = [fl for r in rows for fl in r.get('flips', []) if fl['gen_after'] <= mark]
    nfl = len(flips)
    rm = sum(fl['reader_mediated'] for fl in flips)
    sf = sum(fl['selection_favoured'] for fl in flips)
    egens = [m['est_gen_median'] for m in ms if m['est_gen_median'] is not None]
    r1r = [m['est_R1'] / (m['est_R1'] + m['est_R2']) for m in ms if m['est_R1'] + m['est_R2'] > 0]
    r1m, r1h = tci(r1r)
    return dict(runs=len(ms), I=I, est=tci(est), r1_share=r1m, r1_ci=(r1m - r1h, r1m + r1h), r1_pooled=(e1 / (e1 + e2) if e1 + e2 else float('nan')),
                cls={k: v / tot for k, v in cls.items()}, patchwork=pw / len(ms), single=single / len(ms), ever_patchwork=ever / len(ms),
                resolved=len(res) / len(ms), res_gen=float(np.median([m['resolution_gen'] for m in res])) if res else None,
                e3_resolved=len(e3res) / len(ms), e3_gen=float(np.median(e3res)) if e3res else None,
                crash_on=tci([m['crash_on_2nd'] for m in ms]), dove_on=tci([m['dove_on_2nd'] for m in ms]),
                crash_end=float(np.mean([m['crash_on_end'] for m in ms])), dove_end=float(np.mean([m['dove_on_end'] for m in ms])),
                loss_on=float(np.mean([m['loss_on'] for m in ms])), loss_cross=tci([m['loss_cross'] for m in ms]),
                crash_cross=float(np.mean([m['crash_cross'] for m in ms])), dove_cross=float(np.mean([m['dove_cross'] for m in ms])),
                flips=nfl / len(ms), reader_mediated=(rm / nfl if nfl else float('nan')), selection_favoured=(sf / nfl if nfl else float('nan')),
                polymorphic=float(np.mean([m['polymorphic'] for m in ms])), bridge_share=[float(np.mean([m['bridge_share'][p] for m in ms])) for p in (0, 1)],
                est_gen=float(np.median(egens)) if egens else None, stop=float(np.median([r['stop_gen'] for r in rows])),
                top=Counter(t[0] for m in ms for p in (0, 1) for t in m['top_classes'][p][:1]).most_common(4),
                per_run_est=est)


def lottery_rows():
    rows = []
    for s in ('main', 'small', 'controls', 'forced', 'swap', 'onepop'):
        z = load('lottery_%s.json' % s)
        if z:
            for r in z:
                r['_set'] = s
            rows += z
    return rows


def main():
    L = []
    W = L.append
    J = dict()
    static = load('static.json'); chain = load('chain.json'); onepop = load('onepop_chain.json')
    rows = lottery_rows()
    W('# Fixed-role chicken and hawk–dove without `ROLE` (spec `specs/2026-10-11-fixed-role-chicken.md`; notes '
      '`notes/fixed-role-chicken.md`; predictions `predictions/2026-10-11-fixed-role-chicken.md`)')
    W('')
    W('Actions Straight (hawk) = A_0, Swerve (dove) = A_1. Games: `chicken` (St/St −10, St/Sw 2, Sw/St −1, Sw/Sw 0), `hd3` (V = 2, C = 3: −½, 2, 0, 1), '
      '`hd6` (C = 6: −2, 2, 0, 1). Exponential fitness map w = 0.3. Outcome classes by play with tolerance 0.95 (notes §1.6): R1 = role 1 wins '
      '(role 1 Straight, role 2 Swerve), R2 = role 2 wins, crash, dove (mutual swerve/dove), mixed. **The ε→0 chain (rare mutation) and the lottery '
      '(ε = 0, mutation-free absorption) are separate objects and are never pooled; the lottery panel is finite-size evidence.** In the modal arm the '
      'constants are named `D` (= Straight) and `C` (= Swerve); `BOX` reads "provably swerves", `BOXD` "provably goes straight".')
    W('')
    # ---------------- static
    if static:
        W('## Static: catalogues and program-space closure')
        W('')
        W('| arm | programs | classes | Straight / Swerve mass | bridges (classes, mass) | matchers (classes, mass) | X-mixtures | winner-seat neutral mass |')
        W('|---|---|---|---|---|---|---|---|')
        for arm in F.ARMS:
            c = static['catalogues'][arm]; s = static['static']['%s/chicken' % arm]
            tm = s['tag_mass']
            W('| %s | %d | %d | %.3f / %.3f | %d, %s | %d, %s | %s | %.3f |' % (arm, c['n_programs'], c['K'], tm['firm']['mass'], tm['swerver']['mass'],
                                                                      tm['bridge']['n'], f(tm['bridge']['mass'], 5), tm['matcher']['n'], f(tm['matcher']['mass'], 4),
                                                                      f(tm['mixed']['mass'], 3), s['neutral_winner_seat']['mass']))
        W('')
        W('(Firm and swerver masses include the soft commitments that play like constants against constants, e.g. weak `and(THEM(ME),Straight)`.) '
          'Payoff classes equal play classes in every arm and game: %s.' % all(static['payoff_classes_equal_play_classes'].values()))
        W('')
        W('**Closed classes of the Δ ≥ 0 graph on the K² monomorphic pairs** (Lemma F; a closed class with one convention would be a drift-closed '
          'convention), and the shortest escape from (Straight | Swerve):')
        W('')
        W('| arm | game | closed classes | labels in the closed class(es) | escape path from (Straight \\| Swerve) |')
        W('|---|---|---|---|---|')
        for arm in F.ARMS:
            for g in F.GAME_NAMES:
                s = static['static']['%s/%s' % (arm, g)]
                p = s['escape_path']
                ps = ' → '.join('`%s`%s' % (x['state'], ' (%s)' % x['edge'] if x['edge'] else '') for x in p) if p else 'none (no Δ ≥ 0 path)'
                W('| %s | %s | %d | %s | %s |' % (arm, g, s['n_closed'], '; '.join('{' + ', '.join(c) + '}' for c in s['closed_with_convention']), ps))
        W('')
        md = static['matched_play_difference']
        W('Matched pair: the W0 and M0 play matrices differ in %d of %d program pairs (%.2f%%), all between self-referential readers: %s.' % (
            md['pairs'], md['of'], 100 * md['share'], ', '.join('%s %d' % kv for kv in sorted(md['by_tag'].items(), key=lambda kv: -kv[1]))))
        W('')
        W('**Bridges** (conditional straights: swerve against Straight, straight against Swerve) and their self-play:')
        W('')
        for arm in ('weak', 'W0', 'M0', 'modal'):
            s = static['static']['%s/chicken' % arm]
            sp = Counter(b['self_play'] for b in s['bridges'])
            W('- %s: %s; self-play %s.' % (arm, ', '.join('`%s` (%s)' % (b['name'], f(b['mu'], 5)) for b in sorted(s['bridges'], key=lambda b: -b['mu'])[:8]) +
                                           (' and %d more' % (len(s['bridges']) - 8) if len(s['bridges']) > 8 else ''), dict(sp)))
        s = static['static']['weak/chicken']
        names = [b['name'] for b in s['bridges']]
        W('')
        W('Weak bridge–bridge table (row in role 1 against column in role 2; S[row, col] / S[col, row], 1 = swerve) and the outcome class:')
        W('')
        W('| role 1 \\ role 2 | ' + ' | '.join('`%s`' % n for n in names) + ' |')
        W('|---|' + '---|' * len(names))
        for i, n in enumerate(names):
            W('| `%s` | ' % n + ' | '.join('%s %s' % (s['bridge_bridge_S'][i][j], s['bridge_bridge'][i][j]) for j in range(len(names))) + ' |')
        W('')
        W('Bridge–resident (every bridge, every arm, both roles): against the loser\'s Swerve it plays Straight (neutral in the winner\'s seat); against the '
          'winner\'s Straight it plays Swerve (neutral in the loser\'s seat); with a bridge in the winner\'s seat the loser\'s Straight gains T − S '
          '(3 in chicken, 2 in hawk–dove).')
        W('')
        J['static'] = dict(closed={k: v['closed_with_convention'] for k, v in static['static'].items()}, matched=md)
    # ---------------- chain
    if chain:
        W('## The ε→0 chain, two populations (exact K² monomorphic chain; rare mutation)')
        W('')
        W('N per population. π by outcome class; N·exit = N × (flux out of R1 per unit R1 mass, per mutation event); "bridge" = share of that exit flux '
          'leaving from states whose winner is a bridge; feeder = N × rate of the neutral step into bridge-winner states per unit R1 mass; the decisive edge '
          'is the largest exit edge (mutant, role, Δ, N·Δ, N·ρ). Cut = dropped jump flow (edges below 10⁻³⁰ of a row). Check = TV against dense '
          'log-domain GTH on the full generator.')
        W('')
        W('| arm | game | N | π(R1) | π(R2) | dove | crash | mixed | N·exit | bridge share | N·feeder | decisive exit edge | cut | check |')
        W('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        for r in chain:
            p = r['pi_by_class']
            de = r['decisive_exit_edges'][0] if r['decisive_exit_edges'] else None
            ds = ('`%s` → role-%d `%s`, Δ %.2g, NΔ %.3g, Nρ %.3g' % (de['src'], de['role'], de['mutant'], de['Delta'], de['N_Delta'], de['N_rho'])) if de else '–'
            W('| %s | %s | %d | %.4f | %.4f | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                r['arm'], r['game'], r['N'], p['R1'], p['R2'], e(p['dove']), e(p['crash']), e(p['mixed']), e(r['N_exit_R1']),
                f(r['exit_R1_share_bridge_winner']), e(r['N_feeder']), ds, e(r['cut']), e(r.get('check_tv_vs_log_gth'))))
        W('')
        W('**Support and transition structure** (N = 10³, chicken):')
        W('')
        for r in chain:
            if r['N'] == 1000 and r['game'] == 'chicken':
                W('- %s: support %s; lumped flux %s.' % (r['arm'], '; '.join('`%s` %s (%s)' % (x['state'], f(x['pi'], 4), x['label']) for x in r['support'][:5]),
                                                         '; '.join('%s→%s %s' % (x['src'], x['dst'], e(x['flux'])) for x in r['flux'][:6])))
        W('')
        W('Exit edges out of R1 by share (N = 10⁴, chicken):')
        W('')
        for r in chain:
            if r['N'] == 10000 and r['game'] == 'chicken' and r['decisive_exit_edges']:
                W('- %s: %s.' % (r['arm'], '; '.join('`%s` → role-%d `%s` (Δ %.2g, Nρ %.3g) %.3f' % (x['src'], x['role'], x['mutant'], x['Delta'], x['N_rho'], x['share'])
                                                     for x in r['decisive_exit_edges'][:5])))
        W('')
        J['chain'] = [{k: r[k] for k in ('arm', 'game', 'N', 'pi_by_class', 'N_exit_R1', 'exit_R1_share_bridge_winner', 'N_feeder', 'cut', 'efficiency')} for r in chain]
    # ---------------- one population chain
    if onepop:
        W('## The ε→0 chain, one population, modal arm (c) (seeded log-domain solver, twin-expanded and lumped)')
        W('')
        W('| game | N | θ | twins | states | log₁₀ cut | π by class | payoff/player | efficiency | P(St,St) | P(asym) | P(Sw,Sw) | top state (π) | top exit (log₁₀ rate) |')
        W('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        for r in onepop:
            top = r['support'][0] if r['support'] else None
            tx = r['top_exits'][0] if r['top_exits'] else None
            W('| %s | %d | %.0e | %s | %d | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                r['game'], r['N'], r['theta'], r['twins'], r['n_states'], f(r['log10_cut'], 1), ', '.join('%s %.3f' % kv for kv in sorted(r['pi_by_class'].items())),
                f(r['pay_per_player']), f(r['efficiency']), f(r['StSt']), f(r['asym']), f(r['SwSw']),
                ('`%s` (%.3f)' % (top['state'], top['pi'])) if top else '–', ('%s via %s' % (f(tx['log10_rate'], 1), ', '.join('`%s`' % m[0] for m in tx['mutants'][:2]))) if tx else '–'))
        W('')
        J['onepop_chain'] = [{k: r[k] for k in ('game', 'N', 'theta', 'twins', 'pi_by_class', 'pay_per_player', 'efficiency', 'StSt', 'asym', 'SwSw', 'log10_cut', 'n_states')} for r in onepop]
    # ---------------- lottery
    if rows:
        groups = defaultdict(list)
        for r in rows:
            groups[(r['_set'],) + cell_key(r) + (r['swap'],)].append(r)
        W('## The lottery (ε = 0; I = 64; finite-size evidence)')
        W('')
        W('Per-island establishment = share of islands established at a one-sided convention by play (held through the last tenth of the horizon), '
          'mean ± 95% t-interval over runs. R1 share = R1 among established convention islands, per-run fraction averaged over runs with its 95% t-interval (islands within a run are not independent). Patchwork = runs with islands at '
          'both conventions at the mark; resolved = runs that were patchworks at some sample and are not at the mark (median resolution generation); E3 = '
          'runs every island of which is E3-resolved (median generation). Crash/dove on = second-half time average of the islands\' crash/dove '
          'probability. Cross loss = (T + S) − E[u₁ + u₂] for role 1 of island A against role 2 of island B, A ≠ B. Flips: island convention changes per '
          'run, the share reader-mediated (winner bridge share ≥ f* before the flip) and the share selection-favoured.')
        W('')
        hdr = '| set | arm | game | N | mN | mark | runs | establishment | R1 share | R1 / R2 / crash / dove / mixed | patchwork | resolved (gen) | E3 (gen) | crash on | dove on | cross loss | crash cross | flips/run | reader-med. | sel.-fav. | bridge share (r1, r2) | polymorphic |'
        W(hdr)
        W('|' + '---|' * (hdr.count('|') - 1))
        summ = {}
        order = sorted(groups, key=lambda k: (['main', 'small', 'controls', 'forced', 'swap', 'onepop'].index(k[0]), F.ARMS.index(k[2]) if k[2] in F.ARMS else 9,
                                              F.GAME_NAMES.index(k[3]), k[4], k[5], not k[6]))
        for k in order:
            if k[1] == 'onepop':
                continue
            grp = groups[k]
            marks = sorted({int(m) for r in grp for m in r['marks']})
            for mk in marks:
                s = summarize_cell(grp, mk)
                if s is None:
                    continue
                lab = '%s%s' % (k[0], '' if k[0] != 'forced' else (' +bridges' if k[6] else ' −bridges'))
                summ['%s|%s|%s|%d|%g|%d|%s' % (k[0], k[2], k[3], k[4], k[5], mk, 'b' if k[6] else 'nb')] = {kk: v for kk, v in s.items() if kk not in ('top',)}
                cl = s['cls']
                W('| %s | %s | %s | %d | %g | %d | %d | %s ± %s | %s [%s, %s] | %s / %s / %s / %s / %s | %s | %s (%s) | %s (%s) | %s | %s | %s ± %s | %s | %s | %s | %s | %s, %s | %s |' % (
                    lab, k[2], k[3], k[4], k[5], mk, s['runs'], f(s['est'][0]), f(s['est'][1]), f(s['r1_share']), f(s['r1_ci'][0], 2), f(s['r1_ci'][1], 2),
                    f(cl.get('R1', 0), 3), f(cl.get('R2', 0), 3), f(cl.get('crash', 0), 3), f(cl.get('dove', 0), 3), f(cl.get('mixed', 0), 3),
                    f(s['patchwork'], 3), f(s['resolved'], 3), f(s['res_gen'], 0), f(s['e3_resolved'], 3), f(s['e3_gen'], 0),
                    e(s['crash_on'][0]), e(s['dove_on'][0]), f(s['loss_cross'][0]), f(s['loss_cross'][1]), e(s['crash_cross']),
                    f(s['flips'], 1), f(s['reader_mediated'], 2), f(s['selection_favoured'], 2), f(s['bridge_share'][0], 3), f(s['bridge_share'][1], 3), f(s['polymorphic'], 2)))
        W('')
        # one population lottery
        op = [k for k in order if k[1] == 'onepop']
        if op:
            W('**One population (modal arm (c)), lottery:**')
            W('')
            W('| game | mN | mark | runs | island classes | max asym | mean asym | crash end | dove end | crash 2nd half | payoff/player | efficiency | top classes |')
            W('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
            for k in op:
                grp = groups[k]
                for mk in sorted({int(m) for r in grp for m in r['marks']}):
                    ms = [r['marks'][str(mk)] for r in grp if str(mk) in r['marks']]
                    cls = Counter()
                    for m in ms:
                        cls.update(m['counts'])
                    tot = sum(cls.values())
                    top = Counter()
                    for m in ms:
                        for n_, c_ in m['top_classes'][:3]:
                            top[n_] += c_
                    W('| %s | %g | %d | %d | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                        k[3], k[5], mk, len(ms), ', '.join('%s %.3f' % (a, b / tot) for a, b in cls.most_common()), f(max(m['asym_max'] for m in ms)),
                        f(np.mean([m['asym_mean'] for m in ms])), f(np.mean([m['crash_end'] for m in ms])), f(np.mean([m['dove_end'] for m in ms])),
                        f(np.mean([m['crash_2nd'] for m in ms])), f(np.mean([m['pay_per_player'] for m in ms])), f(np.mean([m['efficiency'] for m in ms])),
                        ', '.join('`%s`' % a for a, _ in top.most_common(3))))
                    summ['onepop|modal|%s|100|%g|%d' % (k[3], k[5], mk)] = dict(classes={a: b / tot for a, b in cls.items()},
                                                                                pay=float(np.mean([m['pay_per_player'] for m in ms])),
                                                                                asym_max=float(max(m['asym_max'] for m in ms)))
            W('')
        # matched control paired difference
        pairs = defaultdict(dict)
        for r in rows:
            if r['kind'] == 'paired':
                pairs[(r['game'], r['mN'], r['rep'])][r['arm']] = r
        if pairs:
            W('**Matched control (W0 vs M0, paired seeds):** per-island establishment difference M0 − W0, mean over paired runs ± 95% t-interval:')
            W('')
            W('| game | mN | mark | pairs | W0 | M0 | M0 − W0 | runs with a difference |')
            W('|---|---|---|---|---|---|---|---|')
            for g in F.GAME_NAMES:
                for mN in (0, 1):
                    ks = [k for k in pairs if k[0] == g and k[1] == mN and 'W0' in pairs[k] and 'M0' in pairs[k]]
                    if not ks:
                        continue
                    for mk in sorted({int(m) for k in ks for m in pairs[k]['W0']['marks']}):
                        dw_ = [pairs[k]['W0']['marks'][str(mk)]['est_frac'] for k in ks]
                        dm_ = [pairs[k]['M0']['marks'][str(mk)]['est_frac'] for k in ks]
                        dd = np.array(dm_) - np.array(dw_)
                        m_, h_ = tci(dd)
                        W('| %s | %g | %d | %d | %s | %s | %s ± %s | %d |' % (g, mN, mk, len(ks), f(np.mean(dw_)), f(np.mean(dm_)), f(m_), f(h_), int((np.abs(dd) > 1e-12).sum())))
                        summ['paired|%s|%g|%d' % (g, mN, mk)] = dict(W0=float(np.mean(dw_)), M0=float(np.mean(dm_)), diff=m_, ci=h_)
            W('')
        # flips: classes on flipping islands
        fl = [x for r in rows if r['mN'] > 0 and r['kind'] in ('natural', 'forced') for x in r.get('flips', [])]
        if fl:
            W('**Island flips** (natural and forced cells pooled by arm and game; winner/loser = the dominant classes before the flip):')
            W('')
            by = defaultdict(list)
            for r in rows:
                if r['mN'] > 0 and r['kind'] in ('natural', 'forced'):
                    for x in r.get('flips', []):
                        by[(r['kind'] + ('' if r['kind'] != 'forced' else (' +b' if r.get('bridges', True) else ' −b')), r['arm'], r['game'], r['N'])].append(x)
            W('Frozen rule (notes §1.7): reader-mediated iff the winner seat\'s bridge share at the last convention sample ≥ f*. Post-hoc '
              '(added after the first main-set cells, labelled): the largest winner-seat bridge share over the flip window ≥ f*; bridges present '
              '(> 0) in the winner seat at the last convention sample; flips with no bridge in the winner seat are the demographic candidates.')
            W('')
            W('| cell | arm | game | N | flips | reader-mediated (frozen) | selection-favoured | winner bridge share (median) | post-hoc: window max ≥ f* | bridges present | no bridge | top winner classes before | top loser classes before |')
            W('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
            for k in sorted(by):
                xs = by[k]
                ph = [x['posthoc_bridge_window'] for x in xs if 'posthoc_bridge_window' in x]
                W('| %s | %s | %s | %d | %d | %.3f | %.3f | %.2f | %s | %.3f | %d | %s | %s |' % (k[0], k[1], k[2], k[3], len(xs), np.mean([x['reader_mediated'] for x in xs]),
                                                                    np.mean([x['selection_favoured'] for x in xs]), np.median([x['winner_bridge_share'] for x in xs]),
                                                                    f(np.mean(ph)) if ph else '–', np.mean([x['winner_bridge_share'] > 0 for x in xs]),
                                                                    sum(x['winner_bridge_share'] == 0 for x in xs),
                                                                    ', '.join('`%s` %d' % kv for kv in Counter(x['winner_top'] for x in xs).most_common(3)),
                                                                    ', '.join('`%s` %d' % kv for kv in Counter(x['loser_top'] for x in xs).most_common(3))))
            W('')
        J['lottery'] = summ
    v = os.path.join(OUT, 'verdicts.md')
    if os.path.exists(v):
        L += ['', open(v).read()]
    open(os.path.join(ROOT, 'runs', 'fixed-role-chicken.md'), 'w').write('\n'.join(L) + '\n')
    json.dump(J, open(os.path.join(ROOT, 'runs', 'fixed-role-chicken.json'), 'w'), indent=1, default=lambda o: None)
    print('\n'.join(L[:5]))


if __name__ == '__main__':
    main()
