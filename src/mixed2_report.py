"""Report for the two-role mixed-action experiment: reads runs/mixed2/ and writes runs/mixed2.md and runs/mixed2.json with the
verdict of every prediction of predictions/2026-10-23-two-role-mixed.md under the scoring conventions fixed there.

    python3 src/mixed2_report.py
"""
import gzip, json, math, os, sys
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs', 'mixed2')
BOOT = 4000
rng = np.random.default_rng(20261023)


def jload(path):
    if path.endswith('.gz'):
        with gzip.open(path, 'rt') as f: return json.load(f)
    with open(path) as f: return json.load(f)


def exists(*parts):
    return os.path.exists(os.path.join(RUNS, *parts))


# ------------------------------------------------------------------ lottery access
_lot = {}


def lot(game, arm, c, cell='primary'):
    """lottery cell (the blind arm pays nothing: its c = 0 file serves both prices); None if missing."""
    if arm == 'blind':
        c = 0.0
    key = (game, arm, c, cell)
    if key not in _lot:
        p = 'lot_%s_%s_c%g_%s.json.gz' % (game, arm, c, cell)
        _lot[key] = jload(os.path.join(RUNS, p)) if exists(p) else None
    return _lot[key]


def vals(L, key, g=2000, runs=None):
    out = []
    for r in L['runs']:
        if runs is not None and r['run'] not in runs:
            continue
        v = r['stats'].get(str(g), {}).get(key)
        out.append(np.nan if v is None else float(v))
    return np.array(out)


def win(L, key, lo=1500, hi=2000):
    out = []
    for r in L['runs']:
        gs = [g for g in r['cps'] if lo <= g <= hi]
        v = [r['stats'][str(g)].get(key) for g in gs]
        v = [x for x in v if x is not None]
        out.append(float(np.mean(v)) if v else np.nan)
    return np.array(out)


def boot(x, B=BOOT):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return (np.nan, np.nan, np.nan)
    idx = rng.integers(0, len(x), size=(B, len(x)))
    m = x[idx].mean(1)
    return (float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5)))


def pdiff(a, b):
    n = min(len(a), len(b))
    return boot(np.asarray(a[:n], float) - np.asarray(b[:n], float))


def mean(x):
    x = np.asarray(x, float)
    return float(np.nanmean(x)) if np.isfinite(x).any() else float('nan')


def fmt(t, d=3):
    if t is None or (isinstance(t, float) and not np.isfinite(t)):
        return 'n/a'
    if isinstance(t, tuple):
        return '%.*f [%.*f, %.*f]' % (d, t[0], d, t[1], d, t[2])
    return '%.*f' % (d, t)


def chain(game, arm, c, capped=False):
    if arm == 'blind':
        c = 0.0
    if exists('chain_%s_%s_c%g_full.json' % (game, arm, c)) and not capped:
        return jload(os.path.join(RUNS, 'chain_%s_%s_c%g_full.json' % (game, arm, c)))
    p = 'chain_%s_%s_c%g.json' % (game, arm, c)
    return jload(os.path.join(RUNS, p)) if exists(p) else None


# ------------------------------------------------------------------ tables
INSP_KEYS = [('u0g', 'inspector payoff (game)'), ('u0', 'inspector payoff (net)'), ('u1g', 'inspectee payoff (game)'),
             ('p_insp', 'P(inspect)'), ('q_cheat', 'P(cheat)'), ('m_above', 'inspector mass p>1/4'), ('m_at', 'mass p=1/4'),
             ('m_below', 'mass p<1/4'), ('m_p516', 'mass at 5/16'), ('m_p38', 'mass at 3/8'), ('m_p12', 'mass at 1/2'),
             ('rd1', 'inspectee readers'), ('rdx1', ' exact readers'), ('rds1', ' sampling readers'), ('reads1', ' behavioural readers'),
             ('rd0', 'inspector readers'), ('sh_1:C', 'class C share'), ('sh_1:K', 'class K share'), ('sh_1:X', 'inspectee X share'),
             ('sh_0:N', 'class N share'), ('sh_0:I', 'class I share'), ('q_comply', 'inspectees q<=0.02'), ('q_cheater', 'inspectees q>=0.98'),
             ('f0', 'forfeit (inspector)'), ('f1', 'forfeit (inspectee)'), ('cost0', 'price paid (inspector)'), ('cost1', 'price paid (inspectee)'),
             ('e0', 'best inspector program payoff vs the inspectees (net)'), ('e1', 'best inspectee program payoff vs the inspectors (net)'),
             ('mix0', 'individual mixing (inspector)'), ('mix1', 'individual mixing (inspectee)'), ('homo0', 'homozygosity 0'), ('homo1', 'homozygosity 1'),
             ('sup0', 'support 0'), ('sup1', 'support 1'), ('dis1', 'bounded-cr disagreement (inspectee)'),
             ('isl_commit', 'islands committed'), ('isl_commit_comply', 'islands committed+compliant'), ('isl_efficient', 'islands at (0,0)'),
             ('isl_nashlike', 'islands near Nash'), ('isl_cheat_majority', 'islands cheat prob > 1/2'), ('u0g_q10', 'island inspector payoff q10'),
             ('u0g_q50', 'island inspector payoff median'), ('u0g_q90', 'island inspector payoff q90')]
END_KEYS = [('u0g', 'player I payoff (game)'), ('u1g', 'player II payoff (game)'), ('bluff', 'bluff prob. (loser)'), ('call', 'call prob.'),
            ('winbet', 'winner betting'), ('m_bluff_eq', 'I mass |bluff-1/4|<=0.1'), ('m_call_eq', 'II mass |call-1/2|<=0.1'),
            ('isl_bluff10', 'islands bluff within 0.1'), ('isl_call10', 'islands call within 0.1'), ('isl_both10', 'islands both'),
            ('isl_value10', 'islands |value|<=0.1'), ('isl_all10', 'islands all three'), ('sh_0:EQ', 'class EQ (I)'), ('sh_0:BET', 'class BET'),
            ('sh_0:CHECK', 'class CHECK'), ('sh_0:HON', 'class HON'), ('sh_1:X', 'class X (II)'), ('sh_1:CALL', 'class CALL'), ('sh_1:FOLD', 'class FOLD'),
            ('rd0', 'I readers'), ('rd1', 'II readers'), ('rdx1', 'II exact readers'), ('rds1', 'II sampling readers'), ('reads1', 'II behavioural readers'),
            ('e0', 'exploitability of II: best I program payoff (net)'), ('e1', 'exploitability of I: best II program payoff (net)'),
            ('f0', 'forfeit I'), ('f1', 'forfeit II'), ('cost0', 'price paid I'), ('cost1', 'price paid II'),
            ('bluff_q10', 'island bluff q10'), ('bluff_q50', 'island bluff median'), ('bluff_q90', 'island bluff q90'), ('call_q10', 'island call q10'),
            ('call_q50', 'island call median'), ('call_q90', 'island call q90'),
            ('mix0', 'mixing I'), ('mix1', 'mixing II'), ('sup0', 'support 0'), ('sup1', 'support 1'), ('dis0', 'bounded-cr disagreement (I)'), ('dis1', 'bounded-cr disagreement (II)')]


def lot_table(md, game, arm, c, cell='primary', keys=None):
    L = lot(game, arm, c, cell)
    if L is None:
        md.append('*%s %s c=%g %s: not run*\n' % (game, arm, c, cell))
        return None
    keys = keys or (INSP_KEYS if game == 'insp' else END_KEYS)
    md.append('**%s %s, c = %g, %s (%d runs)**: generation 2,000 mean [95%% run-clustered CI]; window 1,500–2,000 mean\n' % (
        game, arm, c, cell, len(L['runs'])))
    md.append('| statistic | gen 2,000 | window |\n|---|---|---|')
    out = {}
    for k, name in keys:
        v = vals(L, k)
        if not np.isfinite(v).any():
            continue
        w = win(L, k)
        out[k] = dict(g2000=boot(v), window=boot(w))
        md.append('| %s | %s | %.3f |' % (name, fmt(boot(v)), np.nanmean(w)))
    md.append('')
    return out


def lab_of(code):
    zp, zq, rd = code // 6, (code % 6) // 2, code % 2
    if zp == 2 and zq == 0:
        return 'R' if rd == 1 else 'C'
    if zp == 0 and zq == 0:
        return 'N'
    if zp == 0 and zq == 2:
        return 'K'
    if zp == 2 and zq == 2:
        return 'IK'
    return 'other'


def phases_summary(L):
    """occupancy and transition counts between ladder labels (R reader+committed, C compliant constants+committed, N lax+compliant,
    K lax+cheating, IK committed+cheating) from the 25-generation island phase snapshots."""
    trans = Counter(); occ = Counter()
    for r in L['runs']:
        ph = np.array(r['phases'])
        if ph.size == 0:
            continue
        labs = np.vectorize(lab_of)(ph)
        occ.update(labs.ravel().tolist())
        for t in range(ph.shape[0] - 1):
            for a, b in zip(labs[t], labs[t + 1]):
                if a != b:
                    trans[(a, b)] += 1
    tot = sum(occ.values())
    return dict(occupancy={k: v / tot for k, v in occ.items()}, transitions={'%s->%s' % k: v for k, v in trans.most_common(14)}, n_obs=tot)


def joint_summary(L, game, g=2000):
    Js = [r['stats'][str(g)].get('J') for r in L['runs']]
    J = np.nanmean(np.array(Js, float), axis=0)
    if game == 'insp':
        px = J.sum(1); py = J.sum(0)
        cov = J[0, 0] - px[0] * py[0]
        corr = cov / math.sqrt(px[0] * (1 - px[0]) * py[0] * (1 - py[0])) if 0 < px[0] < 1 and 0 < py[0] < 1 else float('nan')
        return dict(P_IC=J[0, 0], P_IK=J[0, 1], P_NC=J[1, 0], P_NK=J[1, 1], corr=corr)
    # J[c, x, y]: card, I action (BET, CHECK), II action (CALL, FOLD); P(call | bet) by card
    return dict(P_W_bet_call=J[0, 0, 0], P_W_bet_fold=J[0, 0, 1], P_W_check=J[0, 1].sum(), P_L_bet_call=J[1, 0, 0], P_L_bet_fold=J[1, 0, 1],
                P_L_check=J[1, 1].sum(), P_call_given_bet=(J[0, 0, 0] + J[1, 0, 0]) / max(J[0, 0].sum() + J[1, 0].sum(), 1e-12),
                P_bluff_given_bet=J[1, 0].sum() / max(J[0, 0].sum() + J[1, 0].sum(), 1e-12))


def chain_table(md, ch, title):
    if ch is None:
        md.append('*%s: chain not run*\n' % title)
        return
    md.append('**%s** (chain, pi over pairs of monomorphic classes, K = %s)\n' % (title, ch['K']))
    md.append('| N | states | capped | log10 unexplored flux | circulation | pi cycle | pi drift | pi rest | closed classes | u0 | u1 | p / bluff | q / call | readers (1) | mixing 0 | mixing 1 |\n|' + '---|' * 16)
    for N, r in ch['cells'].items():
        s = r['stat']
        p = s.get('p_insp', s.get('bluff')); q = s.get('q_cheat', s.get('call'))
        md.append('| %s | %d | %s | %s | %s | %.3f | %.3f | %.3f | %s | %.4f | %.4f | %s | %s | %.3f | %.3f | %.3f |' % (
            N, r['n_states'], r['capped'], fmt(r.get('log10_unexplored'), 1), fmt(r.get('circulation')), r['pi_cycle'], r['pi_drift'], r['pi_rest'],
            r['info'].get('n_closed'), s['u0g'], s['u1g'], fmt(p), fmt(q), s['rd1'], s['mix0'], s['mix1']))
    md.append('')


# ------------------------------------------------------------------ verdicts
def verdict(held, failed):
    return 'held' if held else ('failed' if failed else 'partial')


def main():
    md = ['# Mixed actions in two-role games: the inspection game and Basic Endgame (run report, 2026-10-23)\n',
          'Spec `specs/2026-10-23-two-role-mixed.md`; predictions `predictions/2026-10-23-two-role-mixed.md`; notes `notes/mixed2.md`; code '
          '`src/mixed2*.py`; rows `runs/mixed2/`. Chain = the ε → 0 diagnostic (pi over pairs of monomorphic role classes); lottery = '
          'the ε = 0 seed lottery at (N, I) = (100, 64), mN = 1, 40 runs, generation 2,000 (size cell (400, 16), 20 runs), run-clustered '
          '95% bootstrap intervals (4,000 resamples). Payoffs in verdicts are game payoffs (gross of the price).\n']
    R = {}
    st = jload(os.path.join(RUNS, 'static.json'))
    # ---------------------------------------------------------------- completeness
    md.append('## Completeness\n')
    md.append('| cell | object | runs / Ns |\n|---|---|---|')
    comp = {}
    for game, arms in (('insp', ('blind', 'sample', 'exact', 'matched', 'sr4', 'sr16')), ('end', ('blind', 'sample', 'exact', 'matched'))):
        for arm in arms:
            for c in ((0.0,) if arm == 'blind' else (0.0, 0.01)):
                L = lot(game, arm, c); ch = chain(game, arm, c)
                Ls = lot(game, arm, c, 'size')
                comp['%s_%s_c%g' % (game, arm, c)] = dict(lottery=None if L is None else len(L['runs']), size=None if Ls is None else len(Ls['runs']),
                                                          chain=None if ch is None else sorted(ch['cells'].keys()))
                md.append('| %s %s c=%g | lottery %s; size %s; chain | %s |' % (game, arm, c, 'missing' if L is None else '%d runs' % len(L['runs']),
                                                                       'missing' if Ls is None else '%d runs' % len(Ls['runs']),
                                                                       'missing' if ch is None else ', '.join(sorted(ch['cells'].keys(), key=int))))
    md.append('')
    R['completeness'] = comp

    # ---------------------------------------------------------------- P1
    sys.path.insert(0, os.path.join(ROOT, 'tests'))
    import test_mixed2 as T
    err_i = 0.0; n_i = 0
    tab = st['insp_exact']['table']
    for rn in T.INSP_ROWS:
        for j, cn in enumerate(T.INSP_COLS):
            h0, h1 = T.INSP_TABLE[rn][j]
            e = tab['%s|%s' % (rn, cn)]
            err_i = max(err_i, abs(e['u0'] - float(h0)), abs(e['u1'] - float(h1))); n_i += 2
    err_e = 0.0; n_e = 0
    tab = st['end_exact']['table']
    for rn in T.END_ROWS:
        for j, cn in enumerate(T.END_COLS):
            h = T.END_TABLE[rn][j]
            if h is None or cn == 'SRII':
                continue
            e = tab['%s|%s' % (rn, cn)]
            mutual = (rn == 'CRI' and h == -3)
            err_e = max(err_e, abs(e['u0'] - float(h)), abs(e['u1'] - (-3.0 if mutual else -float(h)))); n_e += 2
    tabm = st['end_matched']['table']
    err_s = 0.0
    for rn in ['BET', 'CHECK', 'XI', 'HON', 'EQ']:
        err_s = max(err_s, abs(tabm['%s|SRII' % rn]['u0'] - float(T.END_TABLE[rn][5])))
    mm = st['end_exact']['minimax']
    g = st['insp_blind']
    x_check = st['end_exact']['table']['CHECK|X']['u1'], st['end_exact']['table']['XI|X']['u1']
    p1_ok = err_i < 1e-9 and err_e < 1e-9 and err_s < 1e-9 and mm['eq_row_min'] > -1e-9 and mm['eq_vs_x_all'] < 1e-9 and mm['x_row_min'] > -1e-9 \
        and x_check[0] > 0.3 and x_check[1] > 0.16 and len(g['grid_p']) == 17
    R['P1'] = dict(verdict='held' if p1_ok else 'failed', insp_table_maxerr=err_i, end_table_maxerr=err_e, end_srii_maxerr=err_s, minimax=mm,
                   x_vs_check_xi=x_check, grid_size=len(g['grid_p']), grid_min_size=g['grid_min_size'],
                   erratum='EXP against CRII/RII/SRII is not a mutual forfeit (notes section 2); hand recursion 473/2187 for CRII, tested')
    md.append('## Prediction 1 (statics)\n')
    md.append('- Inspection hand table (8 × 5, both payoffs): max |evaluator − hand| = %.2e over %d entries.' % (err_i, n_i))
    md.append('- Endgame hand table (exact arm, %d entries) max error %.2e; the SRII column in the matched arm %.2e. One erratum to the notes '
              '(EXP against the reader columns, notes §2): the evaluator was right, the hand entry (−3) was wrong; 473/2187 re-derived by hand.' % (n_e, err_e, err_s))
    md.append('- Minimax: EQ earns between %.1e and %.1e against every II program of the n = 7 table (%d programs); II\'s X earns at least %.1e against every I '
              'program (argmin %s); X gains %.4f against CHECK and %.4f against XI.' % (mm['eq_row_min'], mm['eq_row_max'], st['end_exact']['S'][1], mm['x_row_min'], mm['x_row_argmin'], x_check[0], x_check[1]))
    md.append('- Dyadic grid (blind inspection arm, n = 8): %d distinct inspection probabilities; minimal sizes %s; the smallest above 1/4 is 5/16 (size 7).' % (len(g['grid_p']), g['grid_min_size']))
    md.append('- **Verdict: %s.**\n' % R['P1']['verdict'])

    # ---------------------------------------------------------------- lottery tables
    md.append('## Lottery tables\n')
    R['tables'] = {}
    for game, arm, c, cell in [('insp', 'exact', 0.0, 'primary'), ('insp', 'exact', 0.01, 'primary'), ('insp', 'blind', 0.0, 'primary'),
                               ('insp', 'matched', 0.0, 'primary'), ('insp', 'sr16', 0.0, 'primary'), ('insp', 'sr4', 0.0, 'primary'),
                               ('insp', 'sample', 0.0, 'primary'), ('insp', 'sample', 0.01, 'primary'), ('insp', 'matched', 0.01, 'primary'),
                               ('insp', 'exact', 0.0, 'size'), ('insp', 'exact', 0.01, 'size'),
                               ('insp', 'exact_ee', 0.0, 'primary'), ('insp', 'exact_ee', 0.01, 'primary'), ('insp', 'exact_er', 0.0, 'primary'), ('insp', 'exact_er', 0.01, 'primary'),
                               ('end', 'exact', 0.01, 'primary'), ('end', 'exact', 0.0, 'primary'), ('end', 'blind', 0.0, 'primary'),
                               ('end', 'sample', 0.01, 'primary'), ('end', 'matched', 0.01, 'primary'), ('end', 'sample', 0.0, 'primary'),
                               ('end', 'matched', 0.0, 'primary'), ('end', 'exact_ee', 0.01, 'primary'), ('end', 'exact_er', 0.01, 'primary'),
                               ('end', 'exact_ee', 0.0, 'primary'), ('end', 'exact_er', 0.0, 'primary')]:
        R['tables']['%s_%s_c%g_%s' % (game, arm, c, cell)] = lot_table(md, game, arm, c, cell)

    # ---------------------------------------------------------------- continuation, encounter distributions, phases
    md.append('## Continuation (runs 0–9, generation 10,000 against 2,000), joint actions and ladder transitions\n')
    R['continuation'] = {}
    R['joint'] = {}
    R['phases'] = {}
    for game, arm, c in [('insp', 'exact', 0.0), ('insp', 'exact', 0.01), ('insp', 'blind', 0.0), ('insp', 'matched', 0.0), ('insp', 'sr16', 0.0), ('insp', 'sr4', 0.0),
                         ('end', 'exact', 0.01), ('end', 'exact', 0.0), ('end', 'blind', 0.0), ('end', 'matched', 0.01)]:
        L = lot(game, arm, c)
        if L is None:
            continue
        key = '%s_%s_c%g' % (game, arm, c)
        runs = set(range(10))
        ks = ['u0g', 'u1g', 'rd1'] + (['p_insp', 'q_cheat'] if game == 'insp' else ['bluff', 'call'])
        cont = {}
        for k in ks:
            a = vals(L, k, 2000, runs); b = vals(L, k, 10000, runs)
            if np.isfinite(b).any():
                cont[k] = dict(g2000=boot(a), g10000=boot(b), diff=pdiff(b, a))
        R['continuation'][key] = cont
        R['joint'][key] = joint_summary(L, game)
        if game == 'insp':
            R['phases'][key] = phases_summary(L)
        md.append('- **%s**: ' % key + '; '.join('%s: %s → %s (diff %s)' % (k, fmt(v['g2000']), fmt(v['g10000']), fmt(v['diff'])) for k, v in cont.items()))
        md.append('  joint: ' + ', '.join('%s=%.3f' % (k, v) for k, v in R['joint'][key].items()))
        if game == 'insp':
            ps = R['phases'][key]
            md.append('  ladder labels (R reader+committed, C constants+committed, N lax+compliant, K lax+cheating, IK committed+cheating): occupancy '
                      + ', '.join('%s %.3f' % (k, v) for k, v in sorted(ps['occupancy'].items())) + '; transitions per 25 generations (counts) ' + ', '.join('%s %d' % kv for kv in list(ps['transitions'].items())[:8]))
    md.append('')

    # ---------------------------------------------------------------- chain tables
    md.append('## Chain tables\n')
    R['chain'] = {}
    for game, arm, c in [('insp', 'exact', 0.0), ('insp', 'exact', 0.01), ('insp', 'blind', 0.0), ('insp', 'matched', 0.0), ('insp', 'matched', 0.01), ('insp', 'sample', 0.0),
                         ('insp', 'sample', 0.01), ('insp', 'sr16', 0.0), ('insp', 'sr4', 0.0), ('end', 'exact', 0.01), ('end', 'exact', 0.0), ('end', 'blind', 0.0),
                         ('end', 'sample', 0.01), ('end', 'matched', 0.01)]:
        ch = chain(game, arm, c)
        chain_table(md, ch, '%s %s c=%g%s' % (game, arm, c, ' (whole state space)' if ch is not None and ch.get('full') else ' (exploration-capped, not converged where capped=True)'))
        if ch is not None and ch.get('full'):
            chc = chain(game, arm, c, capped=True)
            if chc is not None and not chc.get('full'):
                chain_table(md, chc, '%s %s c=%g, exploration-capped sensitivity (1,500 states)' % (game, arm, c))
        if ch is not None:
            R['chain']['%s_%s_c%g' % (game, arm, c)] = {N: dict(pi_cycle=r['pi_cycle'], circulation=r.get('circulation'), n_states=r['n_states'], capped=r['capped'],
                                                                 log10_unexplored=r.get('log10_unexplored'), stat={k: v for k, v in r['stat'].items() if k != 'J'},
                                                                 top_states=r['top_states'][:6], ladder=r.get('ladder'), named_share=r.get('named_share')) for N, r in ch['cells'].items()}
            if game == 'insp' and arm == 'exact':
                for N, r in ch['cells'].items():
                    if r.get('ladder'):
                        md.append('Ladder rates (%s c=%g N=%s, log10 rate per mutation event, N × rate): ' % (arm, c, N) + '; '.join(
                            '%s %.2f, %.3g' % (k, v['log10_rate'], v['N_rate']) for k, v in r['ladder'].items()))
                md.append('')

    # ---------------------------------------------------------------- predictions 2-6
    md.append('## Verdicts\n')
    V = {}
    Le0, Le1 = lot('insp', 'exact', 0.0), lot('insp', 'exact', 0.01)
    # --- P2
    if Le0 is not None and Le1 is not None:
        rd = mean(vals(Le0, 'rd1')); m38 = mean(vals(Le0, 'm_p38')); m12 = mean(vals(Le0, 'm_p12')); m516 = mean(vals(Le0, 'm_p516'))
        u0 = mean(vals(Le0, 'u0g')); u1 = mean(vals(Le1, 'u0g'))
        a_held = rd >= 0.5 and m38 > m12 and u0 > -0.6
        a_failed = rd < 0.3 or u0 < -0.8
        d = pdiff(vals(Le1, 'u0g'), vals(Le0, 'u0g'))
        b_held = d[0] <= -0.1
        b_failed = d[0] >= 0
        overall = 'held' if (a_held and b_held) else ('failed' if (a_failed and b_failed) else 'partial')
        sd_rd = float(np.nanstd(vals(Le0, 'rd1')))
        runs10 = set(range(10))
        cont_drop = mean(vals(Le0, 'u0g', 10000, runs10)) - mean(vals(Le0, 'u0g', 2000, runs10))
        gpt = sd_rd >= 0.2 or cont_drop <= -0.1
        rd1_001 = mean(vals(Le1, 'rd1'))
        gem = rd1_001 < 0.5 and u1 < -0.5
        V['P2'] = dict(verdict=overall, part_a=verdict(a_held, a_failed), part_b=verdict(b_held, b_failed), reader_share_c0=boot(vals(Le0, 'rd1')),
                       mass_38=m38, mass_12=m12, mass_516=m516, u0_c0=boot(vals(Le0, 'u0g')), u0_c001=boot(vals(Le1, 'u0g')), drop=d,
                       reader_share_c001=boot(vals(Le1, 'rd1')), gpt=dict(verdict='held' if gpt else 'failed', sd_reader_share=sd_rd, continuation_change_u0=cont_drop),
                       gemini=dict(verdict='held' if gem else 'failed', reader_share=rd1_001, u0=u1))
    # --- P3
    Lb = lot('insp', 'blind', 0.0); chb = chain('insp', 'blind', 0.0)
    if Lb is not None:
        ub = mean(vals(Lb, 'u0g'))
        pc = chb['cells']['10000']['pi_cycle'] if chb is not None and '10000' in chb['cells'] else None
        circ = {N: r.get('circulation') for N, r in chb['cells'].items()} if chb is not None else None
        held = ub <= -0.8 and pc is not None and pc >= 0.5
        failed = ub > -0.5
        V['P3'] = dict(verdict=verdict(held, failed), u0_blind=boot(vals(Lb, 'u0g')), pi_cycle_N1e4=pc, circulation=circ,
                       note='the weakly improving graph over all pairs is one closed class in every arm: the registered cycle criterion cannot separate arms')
    # --- P4
    arms4 = {a: lot('insp', a, 0.0) for a in ('exact', 'sr16', 'sr4', 'matched')}
    if all(v is not None for v in arms4.values()):
        m = {a: mean(vals(v, 'u0g')) for a, v in arms4.items()}
        gap = pdiff(vals(arms4['exact'], 'u0g'), vals(arms4['matched'], 'u0g'))
        order = m['exact'] >= m['sr16'] >= m['sr4'] >= m['matched']
        held = order and gap[0] >= 0.2
        failed = gap[0] <= 0
        graded = m['matched'] <= m['sr4'] <= m['sr16'] <= m['exact']
        V['P4'] = dict(verdict=verdict(held, failed), means=m, gap_exact_minus_matched=gap, ordering_holds=order,
                       gpt=dict(verdict='held' if (gap[0] < 0.2 and graded) else 'failed', graded=graded),
                       gemini=dict(verdict='held' if abs(gap[0]) < 0.1 else 'failed'))
    # --- P5, P6
    Le = lot('end', 'exact', 0.01)
    if Le is not None:
        b10 = mean(vals(Le, 'isl_bluff10')); c10 = mean(vals(Le, 'isl_call10')); both = mean(vals(Le, 'isl_both10'))
        val = boot(vals(Le, 'u0g'))
        held = both >= 0.6 and abs(val[0]) <= 0.1
        failed = b10 < 0.3 or c10 < 0.3
        V['P5'] = dict(verdict=verdict(held, failed), islands_bluff10=b10, islands_call10=c10, islands_both10=both, value=val,
                       bluff=boot(vals(Le, 'bluff')), call=boot(vals(Le, 'call')), winbet=boot(vals(Le, 'winbet')))
        eq = mean(vals(Le, 'sh_0:EQ')); xx = mean(vals(Le, 'sh_1:X')); rd1 = mean(vals(Le, 'rd1'))
        held6 = eq > 0.5 and xx > 0.5 and rd1 <= 0.5
        failed6 = rd1 > 0.5
        V['P6'] = dict(verdict=verdict(held6, failed6), share_EQ=boot(vals(Le, 'sh_0:EQ')), share_X=boot(vals(Le, 'sh_1:X')), II_readers=boot(vals(Le, 'rd1')),
                       II_exact_readers=boot(vals(Le, 'rdx1')))
    # --- ablation (not in the spec): who reads
    abl = {}
    for arm in ('blind', 'exact_ee', 'exact_er', 'exact'):
        for c in ((0.0,) if arm == 'blind' else (0.0, 0.01)):
            L = lot('insp', arm, c)
            if L is not None:
                abl['%s_c%g' % (arm, c)] = {k: boot(vals(L, k)) for k in ('u0g', 'u1g', 'rd0', 'rd1', 'm_above', 'm_p38', 'm_p12', 'isl_efficient', 'isl_commit_comply', 'p_insp', 'q_cheat')}
    R['ablation'] = abl
    md.append('## Ablation (not in the spec): which role reads (inspection, lottery, generation 2,000)\n')
    md.append('| arm | c | inspector payoff | inspectee payoff | inspector readers | inspectee readers | inspector mass p>1/4 | islands at (0,0) | islands committed+compliant |\n|---|---|---|---|---|---|---|---|---|')
    for k, v in abl.items():
        md.append('| %s | %s | %s | %s | %.2f | %.2f | %.2f | %.2f | %.2f |' % (k.split('_c')[0], k.split('_c')[1], fmt(v['u0g']), fmt(v['u1g']), v['rd0'][0], v['rd1'][0], v['m_above'][0], v['isl_efficient'][0], v['isl_commit_comply'][0]))
    md.append('')
    ablE = {}
    for arm in ('blind', 'exact_ee', 'exact_er', 'exact'):
        for c in ((0.0,) if arm == 'blind' else (0.0, 0.01)):
            L = lot('end', arm, c)
            if L is not None:
                ablE['%s_c%g' % (arm, c)] = {k: boot(vals(L, k)) for k in ('u0g', 'bluff', 'call', 'isl_both10', 'sh_0:EQ', 'sh_1:X', 'rd0', 'rd1', 'e0', 'e1')}
    R['ablation_end'] = ablE
    md.append('## Ablation (not in the spec): which role reads (Endgame, lottery, generation 2,000)\n')
    md.append('| arm | c | value to I | bluff | call | islands both within 0.1 | EQ share | X share | I readers | II readers | exploitability of II | of I |\n|' + '---|' * 12)
    for k, v in ablE.items():
        md.append('| %s | %s | %s | %.3f | %.3f | %.2f | %.2f | %.2f | %.2f | %.2f | %.2f | %.2f |' % (k.split('_c')[0], k.split('_c')[1], fmt(v['u0g']), v['bluff'][0], v['call'][0], v['isl_both10'][0], v['sh_0:EQ'][0], v['sh_1:X'][0], v['rd0'][0], v['rd1'][0], v['e0'][0], v['e1'][0]))
    md.append('')
    R['verdicts'] = V
    R['verdicts']['P1'] = dict(verdict=R['P1']['verdict'])
    md.append('| prediction | verdict | key numbers |\n|---|---|---|')
    md.append('| 1 statics | %s | table errors %.1e / %.1e; minimax %.1e |' % (R['P1']['verdict'], err_i, err_e, mm['eq_row_min']))
    for k in ('P2', 'P3', 'P4', 'P5', 'P6'):
        if k in V:
            md.append('| %s | %s | %s |' % (k, V[k]['verdict'], json.dumps({a: (b if not isinstance(b, tuple) else [round(x, 4) for x in b]) for a, b in V[k].items() if a != 'verdict'}, default=lambda o: float(o))[:700]))
        else:
            md.append('| %s | not scored (cell missing) | |' % k)
    md.append('')
    with open(os.path.join(ROOT, 'runs', 'mixed2.md'), 'w') as f:
        f.write('\n'.join(md))
    with open(os.path.join(ROOT, 'runs', 'mixed2.json'), 'w') as f:
        json.dump(R, f, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else (o.tolist() if isinstance(o, np.ndarray) else str(o)))
    print('wrote runs/mixed2.md and runs/mixed2.json')


if __name__ == '__main__':
    main()
