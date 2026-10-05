"""Assemble runs/club.md and runs/club.json from the scored outputs of the club arm:
runs/club_static.json (fixed points at n = 6, 7; sanity; composition at the full-set limit), runs/club_lattice.json,
runs/club_maximal.json, runs/club_static_kmax.json and runs/club_chain.json.

    python3 src/club_report.py
"""
import json, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda f: json.load(open(os.path.join(ROOT, 'runs', f)))


def slope(xs, ys):
    return float(np.polyfit(np.log(xs), ys, 1)[0])


def main():
    S = J('club_static.json'); LAT = J('club_lattice.json'); MX = J('club_maximal.json')
    SK = J('club_static_kmax.json'); CH = J('club_chain.json')
    L = ['# The closed club: oracle benchmark for semantic self-recognition (specs/2026-10-04-club.md)', '',
         'Predictions: `predictions/2026-10-04-club.md` (committed 3e20554 before any evaluation). Debugging runs: '
         '`runs/club_debug.md`. Code: `src/club.py` (language, evaluator, F), `src/club_static.py`, `src/club_lattice.py`, '
         '`src/club_maximal.py`, `src/club_chain.py`, this report `src/club_report.py`.', '',
         '`CLUB(THEM)` is a global semantic oracle over the finite universe L_n, not a proof procedure. Nothing here is a '
         'realizability result.', '']
    # ---------------- fixed points
    L += ['## 1. Fixed points of the joint operator F', '',
          'F(K) = {x : x(x) = C under P_K and x plays C against no program of L_n outside K}. F(K) ⊆ K for every K '
          '(prediction S1, a proof), so iteration from any start decreases to a fixed point and cycles cannot occur.', '',
          '### Spec starts at n = 6, 7 (full set, empty set, 20 random sets with inclusion 1/2)', '',
          '| grammar | n | universe | distinct fixed points (spec starts) | all fixed points found (+20 random subsets of K*) | |K*| from full set | cycles | union of found = fixed | all found ⊆ K* | monotonicity violations (50 random nested pairs) |',
          '|---|---|---|---|---|---|---|---|---|---|']
    for r in S['fixed_points']:
        spec = sum(1 for f in r['fixed_points'] if not f['reached_from'][0].startswith('sub'))   # spec starts are recorded first
        L.append('| %s | %d | %d | %d | %d | %d | %s | %s | %s | %d |' % (r['mode'], r['n'], r['universe'], spec, r['n_fixed_points'], r['kstar_size'],
                 'none' if not r['any_cycle'] else 'YES', r['union_is_fixed'], r['all_fixed_points_below_kstar'], r['monotonicity_violations']))
    L += ['', 'K* at n = 7: ' + ', '.join('`%s`' % s for s in [r for r in S['fixed_points'] if r['n'] == 7 and r['mode'] == 'full'][0]['kstar']) + '.', '',
          '### Every subset of K* is a fixed point (`runs/club_lattice.json`)', '',
          '| grammar | n | |K*| | subsets that are fixed points | monotonicity violations (200 random nested pairs) |', '|---|---|---|---|---|']
    for r in LAT:
        L.append('| %s | %d | %d | %d of %d | %d |' % (r['mode'], r['n'], r['kstar'], r['fixed'], r['subsets'], r['mono_violations']))
    L += ['', 'Membership of a guarded program `and(CLUB(THEM),ψ)` is self-fulfilling: in K it cooperates with itself (when ψ '
          'holds of it), out of K it defects on itself. So the fixed points below K* form the full Boolean lattice, and '
          '"the club" is one choice among 2^|K*|; the greatest-fixed-point rule picks all-in.', '',
          '### The limit from the full set is not the greatest fixed point at n ≥ 8 (`runs/club_maximal.json`)', '',
          'F is not monotone at n = 8 (25% of random nested pairs). A program such as `and(CLUB(THEM),BOXD(THEM(^D)))` '
          '(cooperate with members that provably defect on D) self-cooperates when D is outside K and defects on itself '
          'while D is still inside; starting from the full set it is removed at step 1 and never returns. Starts from the '
          'set G of guarded programs, and greedy ascent (add any single program, re-iterate, keep strict growth), find:', '',
          '| grammar | n | guarded programs | |K| from full set | from G | ascended maximum | missed by the full-set start | unguarded members | incomparable fixed points met in ascent |',
          '|---|---|---|---|---|---|---|---|---|']
    for r in MX:
        L.append('| %s | %d | %d | %d | %d | %d | %s | %d | %d |' % (r['mode'], r['n'], r['guarded'], r['K_full'], r['K_G'], r['K_max'],
                 ', '.join('`%s`' % s for s in r['missed_by_full']) or '—', len(r['unguarded_in_max']), r['n_incomparable']))
    L += ['', 'One maximal fixed point was found at every n (no incomparable fixed point met). The chain uses K_max, the '
          'largest found, as the spec defines the club as the largest such set. Every member at every n is guarded.', '']
    # ---------------- sanity
    L += ['## 2. Sanity: the base language', '', '| n | |K| |', '|---|---|']
    for r in S['sanity']:
        L.append('| %d | %d |' % (r['n'], r['K']))
    # ---------------- composition
    def comp_table(rows, title):
        out = ['', title, '', '| grammar | n | canons | programs | behavioural classes | μ(K) | μ(`CLUB(THEM)`) | share of self-coop classes | within-K components (largest) | singletons only | suckerable members (μ) | neutral entrants into all-club-FairBot outside K | excluded unsuckerable μ (×μ(K)) | excluded suckerable μ | old-sense universality |',
               '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
        for o in rows:
            out.append('| %s | %d | %d | %.0f | %d | %.5f | %.5f | %.3f | %d (%d) | %s | %d (%.2g) | %d | %.5f (×%.2f) | %.4f | %.3g |' % (
                o['mode'], o['n'], o['K_canons'], o['K_programs'], o['K_classes'], o['K_mu'], o['mu_CT'] or 0, o['K_share_selfcoop'],
                o['within_K_n_components'], o['within_K_largest'], o['within_K_all_singletons'], o['n_suckerable_members'], o['mu_suckerable_members'],
                len(o['neutral_into_cfb_outside_K']), o['collateral_unsuck_out'], o['collateral_ratio'], o['collateral_suck_out'], o['universality_max']))
        return out
    L += comp_table(S['composition'], '## 3. Composition of K\n\n### At the limit from the full set (first scored pass)')
    L += comp_table(SK['composition'], '### At K_max (the chain\'s fixed point)')
    for o in SK['composition']:
        if o['mode'] != 'full' or o['n'] not in (8, 9): continue
        L += ['', '**Members at n = %d (K_max)**, by μ:' % o['n'], '',
              '| class | μ | canons | programs | suckerable (by) | mutual with `CLUB(THEM)` | mates in K |', '|---|---|---|---|---|---|---|']
        for m in o['members']:
            L.append('| `%s` | %.3g | %d | %.0f | %s | %s | %d |' % (m['name'], m['mu'], m['canons'], m['programs'],
                     ('yes (`%s`)' % m['suckered_by'][0]) if m['suckerable'] else 'no', m['mutual_CT'], m['n_mates']))
        L += ['', 'Within-K mutual-cooperation components: ' + '; '.join('{%s}%s' % (', '.join('`%s`' % s for s in c['members']), ' (complete)' if c['clique'] else '') for c in o['within_K_components']) + '.',
              '', 'Excluded unsuckerable classes (top): ' + ', '.join('`%s` %.2g' % tuple(x) for x in o['collateral_unsuck_out_top'][:6]) + '.',
              '', 'P*-block (mutual cooperators of P* that do not cooperate with FairBot) in the same language: %d classes, μ %.4f. FairBot\'s component: %d classes, μ %.4f.' % (
                  o['pstar_block_classes'], o['pstar_block_mu'], o['KFB_size'], o['KFB_mu'])]
    L += ['', '### Cutoff dependence (K_max, members tracked by source string)', '', '| n → n+1 | members at n | dropped | new members (examples) |', '|---|---|---|---|']
    for r in SK['cutoff']:
        L.append('| %d → %d | %d | %d | %d (%s) |' % (r['n'], r['n1'], r['members'], r['dropped'], r['n_new'], ', '.join('`%s`' % s for s in r['new_examples'][:4])))
    # ---------------- chain
    rows = sorted(CH, key=lambda r: ({'club': 0, 'clique': 1, 'free': 2}[r['arm']], r['n'], r['N']))
    L += ['', '## 4. The ε→0 chain (PD, w = 0.3, `eager_poly=False`, θ = 10⁻⁶) and controls', '',
          'π(K): the chain\'s mass on states made only of K classes (club: K_max; clique: the clique; free: none). GTH: the '
          'log-domain monomorphic embedded chain (single-mutant fixation, no polymorphic routes). Residuals: '
          '‖πP − π‖₁ for the linear chain; max relative balance error for GTH.', '',
          '| arm | n | N | classes | P(C,C) | π(K) | π(K), GTH | log(1 − π(K)), GTH | top K state (π) | log exit rate out of K | cheapest exit (log ρ) | log entry flux into K from all-D | hitting time all-D → K | terminal | polymorphic π | residual lin / GTH | s |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        if r['arm'] == 'free':
            L.append('| free | %d | %d | %d | %.4f | — | — | — | — | — | — | — | — | %d | %.1e | %.0e / %.0e | %.0f |' % (
                r['n'], r['N'], r['n_classes'], r['pcc'], r['n_terminal'], r['poly'], r['residual_linear'], r['gth_residual'], r['time_s']))
            continue
        L.append('| %s | %d | %d | %d | %.4f | %.6f | %.6f | %.1f | `%s` (%.3f) | %.2f | `%s` %.2f | %.2f | %.3g | %d | %.1e | %.0e / %.0e | %.0f |' % (
            r['arm'], r['n'], r['N'], r['n_classes'], r['pcc'], r['pi_K'], r['gth_pi_K'], r['gth_log_1m_pi_K'], r['top_K'], r['pi_top_K'],
            r['K_exit_log'], r['K_exit_best'][0], r['K_exit_best'][1], r['K_entry_log_flux'], r['hit_K'], r['n_terminal'], r['poly'],
            r['residual_linear'], r['gth_residual'], r['time_s']))
    L += ['', '### Exits from the top K state, per mutation event (log domain, single-mutant fixation; last column: transition weights in the linear chain)', '',
          '| arm | n | N | top state | strict in K | neutral in K | weak in K | deleterious in K | deleterious out of K | linear chain: kinds with nonzero weight |', '|---|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        if r['arm'] == 'free': continue
        e = r['top_exits_log']; f = lambda k: ('%.2f' % e[k]) if k in e and np.isfinite(e[k]) else '—'
        lin = ', '.join('%s %.1e' % (k, v) for k, v in r['top_exits_linear'].items() if v > 0)
        L.append('| %s | %d | %d | `%s` | %s | %s | %s | %s | %s | %s |' % (r['arm'], r['n'], r['N'], r['top_K'], f('strict_in'), f('neutral_in'), f('weak_in'),
                 f('deleterious_in'), f('deleterious_out'), lin or '—'))
    # slopes
    L += ['', '### Fitted exit and residence slopes', '', '| arm | n | d log(exit out of K)/dN, N ∈ [10³, 10⁵] | log-log slope of exit out of K, N ∈ [10², 10³] | d log(1−π(K))/dN, N ∈ [10³, 10⁵] |', '|---|---|---|---|---|']
    fits = []
    for arm in ('club', 'clique'):
        for n in (6, 8):
            rr = sorted([r for r in CH if r['arm'] == arm and r['n'] == n], key=lambda r: r['N'])
            Ns = np.array([r['N'] for r in rr], float); ex = np.array([r['K_exit_log'] for r in rr]); res = np.array([r['gth_log_1m_pi_K'] for r in rr])
            big = Ns >= 1000
            s1 = float(np.polyfit(Ns[big], ex[big], 1)[0]); s2 = float((ex[1] - ex[0]) / np.log(Ns[1] / Ns[0])); s3 = float(np.polyfit(Ns[big], res[big], 1)[0])
            fits.append(dict(arm=arm, n=n, exit_per_N=s1, exit_loglog_100_1000=s2, residence_per_N=s3))
            L.append('| %s | %d | %.5f | %.1f | %.5f |' % (arm, n, s1, s2, s3))
    L += ['', 'w/4 = 0.075: the cheapest exit out of K is a symmetric coordination with a non-member self-cooperator (FairBot), '
          'whose fixation is e^(−wN/4 + O(log N)).', '', '### Entry from all-D', '',
          '| arm | n | N | payoff (u(x,x), u(x,D), u(D,x), u(D,D)) of club-FairBot / FairBot / `CLUB(THEM)` | log ρ(club-FairBot) | log ρ(FairBot) | log ρ(`CLUB(THEM)`) | |difference| | K members entering neutrally |',
          '|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        if r['arm'] != 'club': continue
        e = r['entry']; g = lambda s, k: e[s][k] if s in e else None
        cf = 'and(BOX(THEM(ME)),CLUB(THEM))'; fb = 'BOX(THEM(ME))'; ct = 'CLUB(THEM)'
        mats = ' / '.join(str(tuple(e[s]['matrix'])) if s in e else '—' for s in (cf, fb, ct))
        d = abs(g(cf, 'log_rho') - g(fb, 'log_rho')) if cf in e else float('nan')
        L.append('| club | %d | %d | %s | %s | %.6f | %.6f | %.1e | %d |' % (r['n'], r['N'], mats, ('%.6f' % g(cf, 'log_rho')) if cf in e else '— (merged with `CLUB(THEM)`)',
                 g(fb, 'log_rho'), g(ct, 'log_rho'), 0.0 if cf not in e else d, r['K_neutral_entrants_D']))
    L += ['', '### Support (π ≥ 10⁻⁴) and networks', '']
    for r in rows:
        L.append('- %s n=%d N=%d: %s; blocks %d, rival share %.3f' % (r['arm'], r['n'], r['N'], '; '.join('%s %.4f' % tuple(s) for s in r['support'][:5]),
                 r['n_blocks'], r['rival_share']))
    L += ['', '### Top out-of-K destinations from the top state (log rate per mutation event)', '']
    for r in rows:
        if r['arm'] == 'free': continue
        L.append('- %s n=%d N=%d: %s' % (r['arm'], r['n'], r['N'], '; '.join('`%s` %.2f' % (s, v) for s, l, v in r['top_dest_out_log'][:3])))
    if os.path.exists(os.path.join(ROOT, 'runs', 'club_chain_alt.json')):
        A = J('club_chain_alt.json')
        L += ['', '## 5. Extra diagnostic (not predicted): the chain on a smaller fixed point', '',
              "K' = K_max at n = 8 without the four member-exploiting `and(CLUB(THEM),not(BOX...))` members and the four BOXD-guarded ones (which behave as `CLUB(THEM)`): " + ', '.join('`%s`' % s for s in A['K_alt']) + '. '
              "K' is a fixed point (every subset of K* is). Its five members are behaviourally one class, `CLUB(THEM)`.", '',
              "| N | P(C,C) | π(K') | top state (π) | hitting time all-D → K' |", '|---|---|---|---|---|']
        for r in A['rows']:
            L.append('| %d | %.4f | %.6f | `%s` (%.3f) | %.3g |' % (r['N'], r['pcc'], r['pi_K'], r['top_K'], r['pi_top_K'], r['hit_K']))
        L += ['', 'At K_max the stationary mass sits on `and(CLUB(THEM),not(BOX1(THEM(THEM))))` (μ 1.3·10⁻⁶), the unsuckerable end '
              'of a within-club faker ladder; at K\' it sits on `CLUB(THEM)`. Which member holds the club is decided by the '
              'fixed-point selection, not by the dynamics.']
    open(os.path.join(ROOT, 'runs', 'club.md'), 'w').write('\n'.join(L) + '\n')
    json.dump(dict(fixed_points=S['fixed_points'], sanity=S['sanity'], composition_full_start=S['composition'], cutoff_full_start=S['cutoff'],
                   lattice=LAT, maximal=MX, composition_kmax=SK['composition'], cutoff_kmax=SK['cutoff'], chain=CH, fits=fits),
              open(os.path.join(ROOT, 'runs', 'club.json'), 'w'), indent=1, default=str)
    print('\n'.join(L))


if __name__ == '__main__':
    main()
