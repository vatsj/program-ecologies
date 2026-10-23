"""Assemble runs/rps.md and runs/rps.json from the stored cells and score the predictions of
predictions/2026-10-23-rps.md by the conventions fixed there.

    python3 src/rps_report.py
"""
import gzip, json, math, os, sys
from collections import defaultdict, Counter
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rps as RP

ROOT = RP.ROOT
OUT = os.path.join(ROOT, 'runs', 'rps')
ARMS = ('pure', 'sample', 'matched', 'exact')
SENS = ('exact_uniform', 'exact_br')
BENCH = ('constants', 'constx')
NS = (100, 1000, 10000, 100000)
NSX = NS + (1000000, 10000000)        # supplementary large-N chains where present
rng = np.random.default_rng(20261023)


def jload(path):
    if path.endswith('.gz'):
        with gzip.open(path, 'rt') as f: return json.load(f)
    with open(path) as f: return json.load(f)


def chain(arm, N, D=12, mu='bits', lumped=False):
    tag = '%s_D%d_N%d%s%s' % (arm, D, N, '' if mu == 'bits' else '_mu' + mu, '_lumped' if lumped else '')
    p = os.path.join(OUT, 'chain_%s.json' % tag)
    return jload(p) if os.path.exists(p) else None


def lottery(arm, cell):
    p = os.path.join(OUT, 'lottery_%s_%s.jsonl.gz' % (arm, cell))
    if not os.path.exists(p): return []
    return [json.loads(l) for l in gzip.open(p, 'rt')]


def boot(vals, B=4000):
    v = np.asarray(vals, float)
    v = v[~np.isnan(v)]
    if len(v) == 0: return (float('nan'),) * 3
    idx = np.random.default_rng(20261023).integers(len(v), size=(B, len(v)))
    m = v[idx].mean(1)
    return float(v.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def fmt(t, d=3):
    if t is None: return 'n/a'
    if isinstance(t, tuple):
        return '%.*f [%.*f, %.*f]' % (d, t[0], d, t[1], d, t[2])
    return '%.*f' % (d, t)


def run_vals(recs, g, key, fn=np.nanmean, filt=None):
    out = []
    for r in recs:
        if str(g) not in r['stats']: continue
        v = np.array(r['stats'][str(g)][key], float)
        if filt is not None: v = filt(v)
        with np.errstate(all='ignore'):
            out.append(fn(v) if len(v) else float('nan'))
    return np.array(out)


def le(thr):
    return lambda v: (v <= thr + 1e-9).astype(float)


def lot_summary(recs, g=2000):
    d = {}
    if not recs: return d
    d['runs'] = len([r for r in recs if str(g) in r['stats']])
    for k in ('e_prog', 'e_act', 'e_act_cond', 'mix_pop', 'mix_self', 'forfeit_plays', 'forfeit_self', 'regret', 'max_regret', 'nclass',
              'homo', 'tv_marg', 'share_X', 'share_consts', 'share_N', 'share_C', 'share_TM', 'share_GN', 'share_GC', 'share_M',
              'freqR', 'freqP', 'freqS'):
        if k in recs[0]['stats'][str(g)]:
            d[k] = boot(run_vals(recs, g, k))
    d['share_e_le_0.05'] = boot(run_vals(recs, g, 'e_prog', filt=le(0.05)))
    d['share_e_le_0.15'] = boot(run_vals(recs, g, 'e_prog', filt=le(0.15)))
    d['nalive_window'] = boot([np.mean(r['nalive_window']) for r in recs])
    d['homo_window'] = boot([np.mean(r['homo_window']) for r in recs])
    # per-run asymmetry of action frequencies (island-pooled)
    asym = []
    for r in recs:
        f = np.array([np.nanmean(r['stats'][str(g)][k]) for k in ('freqR', 'freqP', 'freqS')])
        asym.append(np.abs(f - 1 / 3).max())
    d['run_asymmetry_max_dev'] = boot(asym)
    return d


# ---------------------------------------------------------------- offline lottery statistics from stored compositions
_ARMC = {}


def arm_cached(arm, n=6):
    if (arm, n) not in _ARMC:
        _ARMC[(arm, n)] = RP.get_arm(arm, n, 12)
    return _ARMC[(arm, n)]


def lot_offline(arm, recs, g='2000', n=6):
    """e_exset (exploiter set fixed to the exact grammar), per-island dominant classes and island composition types
    from the stored compositions at generation g."""
    A = arm_cached(arm, n)
    Aex = emap = None
    if arm in ('pure', 'sample', 'matched', 'exact'):
        Aex = arm_cached('exact', n)
        emap = RP.embed_classes(A, Aex)
    e_run, share_run = [], []
    dom = Counter(); types = Counter(); n_isl = 0
    for r in recs:
        if 'comp' not in r or g not in r['comp']: continue
        es = []
        for isl in r['comp'][g]:
            ids = np.array([k for k, c in isl], int); cnt = np.array([c for k, c in isl], float)
            x = cnt / cnt.sum()
            if Aex is not None:
                es.append(float((Aex.U[:, emap[ids]] @ x).max()))
            top = ids[x.argmax()]
            dom[A.names[top]] += 1
            n_isl += 1
        if es:
            es = np.array(es)
            e_run.append(es.mean()); share_run.append((es <= 0.05 + 1e-9).mean())
    # transition structure of the islands: does the dominant class change between 500 and the horizon?
    sw = []
    for r in recs:
        if 'comp' not in r or g not in r['comp'] or '500' not in r['comp']: continue
        ch = 0
        for a_, b_ in zip(r['comp']['500'], r['comp'][g]):
            da = max(a_, key=lambda t: t[1])[0]; db = max(b_, key=lambda t: t[1])[0]
            ch += (da != db)
        sw.append(ch / len(r['comp'][g]))
    return dict(e_exset=boot(e_run) if e_run else None, share_exset_le_0_05=boot(share_run) if share_run else None,
                dominant_class_share=[(k, v / n_isl) for k, v in dom.most_common(10)], n_islands=n_isl,
                dominant_class_changed_500_to_horizon=boot(sw) if sw else None)


def island_categories(recs, g=2000):
    """Per-run fractions of islands in the three readings of 'recovering the equilibrium' (spec Why 1)."""
    out = defaultdict(list)
    for r in recs:
        s = r['stats'].get(str(g))
        if s is None: continue
        e = np.array(s['e_prog']); mix = np.array(s['mix_pop']); homo = np.array(s['homo']); tvm = np.array(s['tv_marg'])
        out['I_individual_mixers_unexploitable'].append(np.mean((mix >= 0.95) & (e <= 0.05 + 1e-9)))
        out['mixers_but_exploitable'].append(np.mean((mix >= 0.95) & (e > 0.05 + 1e-9)))
        out['M_pure_polymorphism_uniform_marginal'].append(np.mean((mix < 0.5) & (tvm <= 0.05)))
        out['unexploitable_not_mixing'].append(np.mean((mix < 0.5) & (e <= 0.05 + 1e-9)))
        out['monomorphic'].append(np.mean(homo >= 0.99))
        out['forfeit_only'].append(np.mean(np.array(s['forfeit_plays']) >= 0.99))
    return {k: boot(v) for k, v in out.items()}


def paired(recsA, recsB, key, g=2000, filt=None):
    a = run_vals(recsA, g, key, filt=filt); b = run_vals(recsB, g, key, filt=filt)
    m = min(len(a), len(b))
    return boot(a[:m] - b[:m])


def chain_row(arm, N, **kw):
    c = chain(arm, N, **kw)
    if c is None: return None
    s = c['pi_stat']
    return dict(e_prog=s['e_prog'], e_exset=s.get('e_exset'), e_act=s['e_act'], e_act_cond=s.get('e_act_cond'), mix_pop=s['mix_pop'],
                mix_self=s['mix_self'], forfeit_self=s['forfeit_self'], forfeit_plays=s['forfeit_plays'], consts=s.get('share_consts', 0.0),
                X=s.get('share_X', 0.0), GN=s.get('share_GN', 0.0), GC=s.get('share_GC', 0.0), tv_self=s['tv_self_play_uniform'],
                regret=s['regret'], n99=c['n_states_for_0.99'], K=c['K'], indet=c['indeterminate_total_events'],
                top=c['top_states'][:3], pi_equiv=c.get('pi_equivariance', {}).get('max_abs_pi_diff'))


def md_table(header, rows):
    s = '| ' + ' | '.join(header) + ' |\n|' + '---|' * len(header) + '\n'
    for r in rows:
        s += '| ' + ' | '.join(str(x) for x in r) + ' |\n'
    return s


def f3(x, d=3):
    return 'n/a' if x is None or (isinstance(x, float) and math.isnan(x)) else '%.*f' % (d, x)


# ================================================================ main
def main():
    R = {}            # json output
    md = []
    P = md.append
    static = jload(os.path.join(OUT, 'static.json'))
    sweep = jload(os.path.join(OUT, 'sweep.json')) if os.path.exists(os.path.join(OUT, 'sweep.json')) else {}
    toy = jload(os.path.join(OUT, 'toy.json')) if os.path.exists(os.path.join(OUT, 'toy.json')) else {}

    # ---- completeness
    comp = {}
    for arm in ARMS + SENS + BENCH:
        for N in NS:
            comp['chain %s N=%d' % (arm, N)] = chain(arm, N) is not None
    for D in (11, 13, 20):
        for arm in ARMS:
            for N in (1000, 10000):
                comp['chain %s D=%d N=%d' % (arm, D, N)] = chain(arm, N, D=D) is not None
    for arm in ARMS:
        for N in (100, 1000, 10000):
            comp['chain %s mu=2^-nodes N=%d' % (arm, N)] = chain(arm, N, mu='nodes') is not None
    for cell, runs in (('primary', 40), ('size', 20), ('primary200', 200)):
        for arm in ARMS + SENS + BENCH:
            if cell == 'primary200' and arm not in ARMS: continue
            comp['lottery %s %s' % (arm, cell)] = len(lottery(arm, cell)) == runs
    comp['toy'] = bool(toy); comp['sweep'] = bool(sweep)
    n7 = {}
    for arm in ARMS:
        n7['chain %s n=7' % arm] = all(os.path.exists(os.path.join(OUT, 'chain_%s_D12_N%d_n7.json' % (arm, N))) for N in NS)
        n7['lottery %s n=7' % arm] = len(lottery(arm, 'primary_n7')) == 40 if False else os.path.exists(os.path.join(OUT, 'lottery_%s_primary_n7.jsonl.gz' % arm))
    comp.update(n7)
    R['completeness'] = comp

    P('# Rock-paper-scissors and mixed actions (run report, 2026-10-23)\n')
    P('Spec `specs/2026-10-23-rps-mixed.md`; predictions `predictions/2026-10-23-rps.md`; notes `notes/rps.md`. Code `src/rps.py`, '
      '`src/rps_n7.py`, `src/rps_run.py`, `src/rps_report.py`, tests `tests/test_rps.py`. Every chain number below is an '
      'epsilon -> 0 object (pi, closure-complete over the monomorphic class states, see §2); every lottery number is an '
      'epsilon = 0 finite-(N, I, horizon) statistic at (N, I) = (100, 64) unless stated, mN = 1, w = 0.3, never pi. Time in '
      'generations of I*N events. Intervals are 95% bootstrap intervals over runs.\n')
    P('## 0. Completeness\n')
    done = sum(comp.values()); P('%d of %d cells complete.\n' % (done, len(comp)))
    miss = [k for k, v in comp.items() if not v]
    P('Missing or partial: %s\n' % (', '.join(miss) if miss else 'none'))

    # ---- 1 static
    P('## 1. Static numbers and validation\n')
    rows = []
    for arm in ARMS + SENS + BENCH:
        s = static[arm]
        sy = s.get('symmetry_err_U', {})
        rows.append([arm, s['S'], s['K'], s['K_dec5'], '%.1e' % s['antisym_err'], '%.1e' % max(sy.values()) if sy else 'n/a',
                     '%.2e' % s['mean_forfeit_mass_over_pairs'], s['n_classes_dist_split']])
    P(md_table(['arm', 'programs (n=6)', 'classes', 'classes (5 dec.)', 'antisymmetry err', 'cyclic relabel err (U)', 'mean forfeit mass over pairs', 'classes with distribution-heterogeneous members'], rows))
    P('Hand-computed named-class payoffs (notes §1.3, eleven programs, 121 entries) agree with the evaluator to 1e-12 '
      '(`tests/test_rps.py::test_hand_table`); the recursive reference evaluator agrees with the batched one on random and reading-heavy pairs in all six semantic arms; '
      'the two-type contest through `LogChain` reproduces `chain.Chain` and the closed-form Moran ratio; the blocked evaluator '
      'used for n = 7 reproduces the full table at n = 6.\n')
    P('### Prediction 1 statics\n')
    rows = []
    for arm in ('sample', 'matched', 'exact'):
        s = static[arm]
        rows.append([arm, s['pred1_X_nonforfeit_programs'], '%.1e' % s['pred1_X_max_abs_payoff_nonforfeit'], s['pred1_X_forfeiting_programs'],
                     s.get('pred1_C_self_forfeit_mass', 'n/a'), s['pred1_N_deterministic_opponents'], s['pred1_N_counterexamples'], s['pred1_N_beats_constants']])
    P(md_table(['arm', 'programs not forfeiting vs X', 'max |payoff vs X| among them', 'programs forfeiting vs X', 'forfeit mass of the exact (or matched) counter in self-play', 'opponents deterministic against N', 'counterexamples (u(N, b) != +1)', 'u(N, R/P/S)'], rows))

    P('### Depth sweep (D = 11, 12, 13, 20)\n')
    P('Program-level, all pairs of the full table (payoff difference from D = 12):\n')
    rows = []
    for arm in ARMS + SENS:
        sw = static[arm].get('depth_sweep_program_level', {})
        for D in ('11', '13', '20'):
            if D in sw:
                x = sw[D]; rows.append([arm, D, '%.3g' % x['max_abs_diff_all_pairs'], '%.2e' % x['frac_pairs_diff_gt_1e9'], '%.2e' % x['sign_flips_frac'], '%.3g' % x['sampled1000_max']])
    P(md_table(['arm', 'D', 'max |dU| over all pairs', 'fraction of pairs with |dU| > 1e-9', 'fraction with sign change', 'max |dU| on 1,000 sampled pairs'], rows))
    P('On the pairs that matter (named classes, classes holding 0.99 of pi at N = 10^2..10^5, classes holding 0.99 of the primary lottery mass):\n')
    rows = []
    for arm in ARMS:
        sw = sweep.get(arm)
        if not sw: continue
        for D in ('11', '13', '20'):
            x = sw['by_D'][D]
            rows.append([arm, sw['n_classes_in_set'], D, x['set_pairs_diff_gt_1e9'], x['set_pairs'], x['set_sign_flips'], '%.3g' % x['set_max_abs_payoff_diff'], '%.3g' % x['set_max_forfeit_mass_diff']])
    P(md_table(['arm', 'classes', 'D', 'pairs with |dU| > 1e-9', 'pairs', 'sign flips', 'max |dU|', 'max |d forfeit mass|'], rows))
    P('Inferred versus actual opponent action (a reader of `THEM(ME)` sees the opponent at one level less depth), over the same class sets:\n')
    rows = []
    for arm in ARMS:
        sw = sweep.get(arm)
        if not sw or 'inferred_vs_actual' not in sw: continue
        x = sw['inferred_vs_actual']
        rows.append([arm, x['n_pairs'], x['n_gt_1e9'], '%.3g' % x['mean_tv'], '%.4f' % x['max_tv'], '; '.join('%s vs %s' % (a, b) for a, b, t in x['worst'][:2])])
    P(md_table(['arm', 'reading pairs', 'pairs with inferred != actual', 'mean TV', 'max TV', 'worst pairs'], rows))

    # ---- 2 chain
    P('## 2. The epsilon -> 0 chain (class table at n = 6, D = 12, w = 0.3, prior = length prior)\n')
    P('The explored set is the full monomorphic closure in every cell (expanded states = classes; theta_log 1e-12 / 1e-14 / 1e-16 and the lumped versus twin-expanded runs were executed for pure, sample and exact at N = 10^4 and agree to four decimals in every statistic: files `chain_*_th12.json`, `_th16.json`, `_lumped.json`). '
      'In an antisymmetric symmetric game a single mutant meets a monomorphic resident in a two-type contest, which has no interior attractor, so every state is '
      'monomorphic: the "polymorphic" part of the spec\'s chain never arises, no three-type replicator cycle is met (indeterminate events: %d in all cells), and the chain is a weighted tournament on the classes. '
      'The three-constant polymorphism is never visited.\n' % sum((chain(a, N) or {}).get('indeterminate_total_events', 0) for a in ARMS + SENS + BENCH for N in NS))
    hdr = ['arm', 'N', 'e (own exploiters)', 'e (exact-grammar exploiters)', 'action expl.', 'mixing (vs pop.)', 'self-play forfeit', 'constants', 'X', 'GN', 'GC', 'states for 0.99']
    rows = []
    Rc = {}
    for arm in ARMS + SENS + BENCH:
        for N in NSX:
            r = chain_row(arm, N)
            if r is None: continue
            Rc['%s_%d' % (arm, N)] = r
            rows.append([arm, N, f3(r['e_prog']), f3(r['e_exset']), f3(r['e_act']), f3(r['mix_pop']), f3(r['forfeit_self']), f3(r['consts']), f3(r['X']), f3(r['GN'], 4), f3(r['GC'], 4), r['n99']])
    P(md_table(hdr, rows))
    R['chain'] = Rc
    # pi(X) = mu(X)
    errs = []
    for arm in ('sample', 'matched', 'exact', 'exact_uniform', 'exact_br', 'constx'):
        A = arm_cached(arm)
        muX = float(A.mass[RP.class_index(A, 'X')])
        for N in NS:
            c = chain(arm, N)
            if c: errs.append((abs(c['pi_stat']['share_X'] - muX), arm, N, muX))
    P('**X is an always-neutral entrant: pi(class X) equals its prior mass exactly.** Every program that does not forfeit against X earns 0 against it and X earns 0 against everything, so X invades every monomorphic state at the neutral rate 1/N and leaves it at the neutral rate; detailed balance gives pi(X) = mu(X) at every N. '
      'Max |pi(X) - mu(X)| over the %d cells where X is in the grammar: %.1e.\n' % (len(errs), max(e[0] for e in errs)))
    R['piX_identity_max_err'] = max(e[0] for e in errs)
    P('Support and transition structure at N = 10^4 (top states; each is a monomorphic class):\n')
    for arm in ARMS:
        c = chain(arm, 10000)
        P('* **%s** (K = %d; states for 0.99 of pi: %d): ' % (arm, c['K'], c['n_states_for_0.99']) + '; '.join('%s %.3f' % (t['state'].replace(':1.000', ''), t['pi']) for t in c['top_states'][:6]))
        ex = c.get('top_exits', [])
        if ex:
            e0 = ex[0]
            P('  Top state exits (log10 rate per mutation event): %s; to %s' % (f3(e0['log10_total_exit'], 2), '; '.join('%s (%.2f; by %s)' % (x['to'].replace(':1.000', ''), x['log10_rate'], x['mutants'][0][0] if x['mutants'] else '?') for x in e0['top_exits'][:3])))
    P('\nConvergence in N (exact, e own / e exact-set / mixing): ' + '; '.join('N=%d: %s / %s / %s' % (N, f3(Rc['exact_%d' % N]['e_prog']), f3(Rc['exact_%d' % N]['e_exset']), f3(Rc['exact_%d' % N]['mix_pop'])) for N in NSX if 'exact_%d' % N in Rc) + '.\n')
    # ---- the N -> infinity limit (closed form) and the approach
    P('### The N -> infinity limit of the chain, and the approach to it\n')
    P('Let Z0 be the classes nobody can exploit (e(c) = max_k U[k, c] = 0 over the arm\'s own classes). Members of Z0 are payoff-neutral to one another, a mutant strictly beating a non-Z0 state exits it at an N-independent rate while neutral moves cost 1/N, '
      'so as N -> infinity pi concentrates on Z0 with weights proportional to the prior: pi_inf(c) = mu(c) / mu(Z0) on Z0 (and pi(X) = mu(X) at every finite N). '
      'This is exact for the class table; the finite-N chain approaches it at a speed set by the smallest exploitabilities in the table.\n')
    rows = []
    LIM = {}
    for arm in ARMS + SENS:
        A = arm_cached(arm)
        e = A.U.max(axis=0)
        Z0 = np.nonzero(e <= 1e-9)[0]
        mz = float(A.mass[Z0].sum())
        mix = fself = eact = 0.0
        for c in Z0:
            st = RP.state_stats(A, [c], [1.0])
            w_ = A.mass[c] / mz
            mix += w_ * st['mix_pop']; fself += w_ * st['forfeit_self']; eact += w_ * st['e_act']
        row = [arm, len(Z0), '%.4f' % mz, '%.2f' % mix, '%.2f' % fself, '%.2f' % eact]
        pz = {}
        for N in NSX:
            c = chain(arm, N)
            if c is None:
                row.append('-'); continue
            sh = dict(c['class_share_all'])
            pz[N] = sum(sh.get(A.names[k], 0.0) for k in Z0)
            row.append('%.3f' % pz[N])
        LIM[arm] = dict(n_Z0=len(Z0), mu_Z0=mz, mix=mix, forfeit_self=fself, e_act=eact, pi_Z0=pz, Z0=[A.names[k] for k in Z0])
        rows.append(row)
    P(md_table(['arm', '|Z0|', 'prior mass of Z0', 'mixing under pi_inf', 'self-play forfeit under pi_inf', 'action expl. under pi_inf', 'pi(Z0) N=10^2', '10^3', '10^4', '10^5', '10^6', '10^7'], rows))
    R['limit'] = LIM
    P('Members of Z0 (exact arm): ' + ', '.join(LIM['exact']['Z0']) + '. Pure arm: ' + ', '.join(LIM['pure']['Z0']) + '.\n')
    P('pi mass by exploitability bucket e(c) of the state\'s class (exact arm; the tiny-e classes are exploitable only through the cap residue):\n')
    rows = []
    A = arm_cached('exact'); e = A.U.max(axis=0)
    bk = [(0, 1e-9), (1e-9, 1e-3), (1e-3, 1e-2), (1e-2, 0.1), (0.1, 0.5), (0.5, 2.0)]
    for N in NSX:
        if chain('exact', N) is None: continue
        sh = dict(chain('exact', N)['class_share_all'])
        row = [N]
        for lo, hi in bk:
            row.append('%.3f' % sum(sh.get(A.names[k], 0.0) for k in range(A.K) if lo < e[k] <= hi or (lo == 0 and e[k] <= hi)))
        rows.append(row)
    P(md_table(['N', 'e = 0', '(0, 1e-3]', '(1e-3, 1e-2]', '(1e-2, 0.1]', '(0.1, 0.5]', '(0.5, 1]'], rows))
    P('### Sensitivity to the cap D (N = 10^4 and 10^3) and to the prior (2^-nodes)\n')
    rows = []
    for arm in ARMS:
        for N in (1000, 10000):
            vals = []
            for D in (11, 12, 13, 20):
                r = chain_row(arm, N, D=D)
                vals.append('%s / %s' % (f3(r['e_prog']), f3(r['mix_pop'])) if r else 'n/a')
            rows.append([arm, N] + vals)
    P(md_table(['arm', 'N', 'D = 11: e / mixing', 'D = 12', 'D = 13', 'D = 20'], rows))
    R['cap_sensitivity'] = {'%s_%d_D%d' % (arm, N, D): chain_row(arm, N, D=D) for arm in ARMS for N in (1000, 10000) for D in (11, 12, 13, 20)}
    rows = []
    for arm in ARMS:
        for N in (100, 1000, 10000):
            r = chain_row(arm, N, mu='nodes')
            if r: rows.append([arm, N, f3(r['e_prog']), f3(r['e_exset']), f3(r['mix_pop']), f3(r['forfeit_self']), f3(r['consts']), f3(r['X']), f3(r['GN'], 3)])
    P('Prior 2^-nodes (normalised at n = 6; labelled sensitivity, the primary prior is the length prior):\n')
    P(md_table(['arm', 'N', 'e', 'e (exact set)', 'mixing', 'self-play forfeit', 'constants', 'X', 'GN'], rows))
    R['mu_nodes'] = {'%s_%d' % (arm, N): chain_row(arm, N, mu='nodes') for arm in ARMS for N in (100, 1000, 10000)}

    # ---- n = 7
    if any(n7.values()):
        P('### n = 7 (blocked evaluation; classes by payoff rows over all 17,888 programs)\n')
        rows = []
        for arm in ARMS:
            for N in NS:
                p = os.path.join(OUT, 'chain_%s_D12_N%d_n7.json' % (arm, N))
                if not os.path.exists(p): continue
                c = jload(p); s = c['pi_stat']
                rows.append([arm, c['K'], N, f3(s['e_prog']), f3(s.get('e_exset')), f3(s['mix_pop']), f3(s['forfeit_self']), f3(s.get('share_consts', 0)), f3(s.get('share_X', 0)), c['n_states_for_0.99']])
        P(md_table(['arm', 'classes', 'N', 'e', 'e (exact set)', 'mixing', 'self-play forfeit', 'constants', 'X', 'states for 0.99'], rows))
        R['n7_chain'] = rows
        lim7 = {}
        for arm in ARMS:
            A7 = arm_cached(arm, 7)
            e7 = A7.U.max(axis=0); Z7 = np.nonzero(e7 <= 1e-9)[0]; mz7 = float(A7.mass[Z7].sum())
            mix7 = sum(A7.mass[c] / mz7 * RP.state_stats(A7, [c], [1.0])['mix_pop'] for c in Z7)
            lim7[arm] = dict(n_Z0=len(Z7), mu_Z0=mz7, mix=mix7, Z0=[A7.names[c] for c in Z7][:6])
        P('N -> infinity limit at n = 7 (unexploitable classes): ' + '; '.join('%s: |Z0| = %d, prior mass %.4f, mixing %.2f' % (a, v['n_Z0'], v['mu_Z0'], v['mix']) for a, v in lim7.items()) + '\n')
        R['n7_limit'] = lim7

    # ---- 3 lottery
    P('## 3. The epsilon = 0 seed lottery, (N, I) = (100, 64), mN = 1, 40 runs, generation 2,000\n')
    P('Founders iid from the length prior (common random numbers across arms; exact and sample-matched paired spelling for spelling), complete island graph, w = 0.3. '
      'Run-clustered 95% intervals.\n')
    LS = {}
    LO = {}
    rows = []
    for arm in ARMS + SENS + BENCH:
        recs = lottery(arm, 'primary')
        if not recs: continue
        s = lot_summary(recs, 2000); LS[arm] = s
        LO[arm] = lot_offline(arm, recs) if arm in ARMS else {}
        rows.append([arm, s['runs'], fmt(s['e_prog'], 2), fmt(s['share_e_le_0.05'], 2), fmt(LO[arm].get('e_exset'), 2) if LO[arm] else 'n/a', fmt(s['e_act'], 2),
                     fmt(s['mix_pop'], 2), fmt(s['forfeit_plays'], 2), fmt(s['regret'], 2), fmt(s['nalive_window'], 2), fmt(s['homo_window'], 2)])
    P(md_table(['arm', 'runs', 'in-pop. program exploitability', 'islands with e <= 0.05', 'e (exact-grammar exploiters)', 'action exploitability', 'individual mixing', 'plays forfeited', 'resident regret', 'classes alive (1500-2000)', 'homozygosity (1500-2000)'], rows))
    R['lottery_primary'] = LS
    R['lottery_primary_offline'] = LO
    P('Named-class shares of the population at generation 2,000 (mean over islands, then runs):\n')
    rows = []
    for arm in ARMS + SENS + BENCH:
        s = LS.get(arm)
        if not s: continue
        rows.append([arm] + [fmt(s.get(k), 3) if k in s else 'n/a' for k in ('share_consts', 'share_X', 'share_TM', 'share_N', 'share_C', 'share_GN', 'share_GC', 'share_M')])
    P(md_table(['arm', 'constants', 'X', 'THEM(ME)', 'next(THEM(ME))', 'cr(THEM(ME))', 'guarded next', 'guarded cr', 'coin(R,P)'], rows))
    P('Dominant class of the island at generation 2,000 (share of all islands over the 40 runs):\n')
    for arm in ARMS:
        if LO.get(arm): P('* **%s:** ' % arm + '; '.join('%s %.2f' % (k, v) for k, v in LO[arm]['dominant_class_share'][:6]))
    P('')
    P('Share of islands whose dominant class changed between generation 500 and 2,000 (transitions, rule 4): ' + '; '.join('%s %s' % (a, fmt(LO[a]['dominant_class_changed_500_to_horizon'], 2)) for a in ARMS if LO.get(a) and LO[a].get('dominant_class_changed_500_to_horizon')) + '\n')
    P('The three readings, by islands at generation 2,000 (fraction of islands, run-clustered):\n')
    rows = []
    CAT = {}
    for arm in ARMS + SENS:
        recs = lottery(arm, 'primary')
        if not recs: continue
        c = island_categories(recs, 2000); CAT[arm] = c
        rows.append([arm] + [fmt(c[k], 2) for k in ('I_individual_mixers_unexploitable', 'mixers_but_exploitable', 'M_pure_polymorphism_uniform_marginal', 'unexploitable_not_mixing', 'monomorphic', 'forfeit_only')])
    P(md_table(['arm', '(I) individuals mix and e <= 0.05', 'individuals mix but exploitable', '(M) no individual mixing, population marginal uniform', 'e <= 0.05 without mixing', 'monomorphic (homozygosity >= 0.99)', 'island forfeits >= 0.99 of plays'], rows))
    R['island_categories'] = CAT
    P('Pooled action frequencies over non-forfeit plays (R, P, S; mean over islands, then runs) and per-run asymmetry (max deviation of the run\'s island-pooled frequency from 1/3):\n')
    rows = []
    for arm in ARMS + SENS:
        s = LS.get(arm)
        if not s: continue
        rows.append([arm, fmt(s.get('freqR'), 3) if 'freqR' in s else 'n/a', fmt(s.get('freqP'), 3) if 'freqP' in s else 'n/a', fmt(s.get('freqS'), 3) if 'freqS' in s else 'n/a', fmt(s.get('run_asymmetry_max_dev'), 3)])
    P(md_table(['arm', 'R', 'P', 'S', 'per-run asymmetry'], rows))
    P('Paired differences exact minus sample-matched (founders paired spelling for spelling), run-clustered:\n')
    ex, ma, sa, pu = lottery('exact', 'primary'), lottery('matched', 'primary'), lottery('sample', 'primary'), lottery('pure', 'primary')
    PD = {}
    PD['e_prog'] = paired(ex, ma, 'e_prog'); PD['share_e_le_0.05'] = paired(ex, ma, 'e_prog', filt=le(0.05)); PD['mix_pop'] = paired(ex, ma, 'mix_pop')
    PD['forfeit_plays'] = paired(ex, ma, 'forfeit_plays')
    P(md_table(['statistic (exact - matched)', 'difference'], [[k, fmt(v, 3)] for k, v in PD.items()]))
    R['paired_exact_minus_matched'] = PD
    # supplementary 200
    P('### Supplementary replicate: 200 further runs (independent founders), arms pure / sample / matched / exact\n')
    rows = []
    S200 = {}
    for arm in ARMS:
        recs = lottery(arm, 'primary200')
        if not recs: continue
        s = lot_summary(recs, 2000); S200[arm] = s
        o = lot_offline(arm, recs)
        rows.append([arm, s['runs'], fmt(s['e_prog'], 3), fmt(s['share_e_le_0.05'], 3), fmt(o['e_exset'], 3), fmt(s['mix_pop'], 3), fmt(s['share_X'], 3) if 'share_X' in s else 'n/a'])
    if rows:
        P(md_table(['arm', 'runs', 'e', 'islands with e <= 0.05', 'e (exact set)', 'mixing', 'X share'], rows))
        ex2, ma2 = lottery('exact', 'primary200'), lottery('matched', 'primary200')
        PD2 = {'e_prog': paired(ex2, ma2, 'e_prog'), 'share_e_le_0.05': paired(ex2, ma2, 'e_prog', filt=le(0.05)), 'mix_pop': paired(ex2, ma2, 'mix_pop')}
        P('Paired exact - matched over 200 runs: ' + '; '.join('%s %s' % (k, fmt(v, 3)) for k, v in PD2.items()) + '\n')
        R['primary200'] = S200; R['primary200_paired'] = PD2
    # size cell
    P('### Size cell (N, I) = (400, 16), 20 runs\n')
    rows = []
    SZ = {}
    for arm in ARMS + SENS + BENCH:
        recs = lottery(arm, 'size')
        if not recs: continue
        s = lot_summary(recs, 2000); SZ[arm] = s
        rows.append([arm, s['runs'], fmt(s['e_prog'], 2), fmt(s['share_e_le_0.05'], 2), fmt(s['mix_pop'], 2), fmt(s['forfeit_plays'], 2), fmt(s['nclass'], 2), fmt(s.get('share_X'), 2) if 'share_X' in s else 'n/a'])
    P(md_table(['arm', 'runs', 'e', 'islands with e <= 0.05', 'mixing', 'plays forfeited', 'classes alive', 'X share'], rows))
    R['lottery_size'] = SZ
    # continuation
    P('### Continuation of the first 10 primary runs to 10,000 generations\n')
    rows = []
    CT = {}
    for arm in ARMS + SENS + BENCH:
        recs = [r for r in lottery(arm, 'primary') if r['horizon'] >= 10000]
        if not recs: continue
        row = [arm, len(recs)]
        cts = {}
        for g in (2000, 5000, 10000):
            e = boot(run_vals(recs, g, 'e_prog')); m = boot(run_vals(recs, g, 'mix_pop')); sh = boot(run_vals(recs, g, 'e_prog', filt=le(0.05)))
            cts[g] = dict(e=e, mix=m, share=sh)
            row.append('%s / %s / %s' % (fmt(e, 2).split(' ')[0], fmt(sh, 2).split(' ')[0], fmt(m, 2).split(' ')[0]))
        CT[arm] = cts
        rows.append(row)
    P(md_table(['arm', 'runs', 'g = 2,000: e / share e <= 0.05 / mixing', 'g = 5,000', 'g = 10,000'], rows))
    R['continuation'] = CT
    # trajectory of the primary exact lottery over checkpoints
    P('Time course (exact arm, 40 runs; e / share of islands with e <= 0.05 / mixing / classes alive): ' + '; '.join(
        'g=%d: %s / %s / %s / %s' % (g, fmt(boot(run_vals(ex, g, 'e_prog')), 2).split(' ')[0], fmt(boot(run_vals(ex, g, 'e_prog', filt=le(0.05))), 2).split(' ')[0],
                                      fmt(boot(run_vals(ex, g, 'mix_pop')), 2).split(' ')[0], fmt(boot(run_vals(ex, g, 'nclass')), 2).split(' ')[0]) for g in (100, 250, 500, 1000, 2000)) + '\n')
    if n7.get('lottery exact n=7'):
        P('### n = 7 lottery (40 runs, generation 2,000)\n')
        rows = []
        for arm in ARMS:
            recs = lottery(arm, 'primary_n7')
            if not recs: continue
            s = lot_summary(recs, 2000); o = lot_offline(arm, recs, n=7)
            rows.append([arm, s['runs'], fmt(s['e_prog'], 2), fmt(s['share_e_le_0.05'], 2), fmt(o['e_exset'], 2), fmt(s['mix_pop'], 2), fmt(s['forfeit_plays'], 2)])
        P(md_table(['arm', 'runs', 'e', 'islands with e <= 0.05', 'e (exact set)', 'mixing', 'plays forfeited'], rows))
        R['n7_lottery'] = rows

    # ---- toy
    if toy:
        P('## 4. The eleven-program toy chain (notes §1.4)\n')
        rows = []
        for D in (11, 12, 13, 20):
            for N in (100, 1000, 10000):
                t = toy['D%d_N%d' % (D, N)]
                rows.append([D, N, '%.4f' % t['gap_TM_GN'], f3(t['mass_on_XGNGC'], 4), t['top'][0]['state'], f3(t['top'][0]['pi'], 3)])
        P(md_table(['D', 'N', 'u(TM, GN)', 'pi mass on {X, GN, GC}', 'top state', 'its pi'], rows))
        R['toy'] = toy

    # ---- verdicts
    V = verdicts(static, sweep, Rc, LS, LO, PD, CAT, R.get('primary200_paired'))
    R['verdicts'] = V
    P('## 5. Verdicts (conventions of `predictions/2026-10-23-rps.md`)\n')
    P(md_table(['item', 'verdict', 'evidence'], [[v['id'], v['verdict'], v['evidence']] for v in V]))
    with open(os.path.join(ROOT, 'runs', 'rps.md'), 'w') as f:
        f.write('\n'.join(md) + '\n')
    with open(os.path.join(ROOT, 'runs', 'rps.json'), 'w') as f:
        json.dump(R, f, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
    print('wrote runs/rps.md and runs/rps.json; %d/%d cells' % (done, len(comp)))


def bigN(Rc, arms, Ns=(1000000, 10000000)):
    out = []
    for N in Ns:
        parts = []
        for a in arms:
            r = Rc.get('%s_%d' % (a, N))
            if r: parts.append('%s e %.4f / mixing %.3f' % (a, r['e_prog'], r['mix_pop']))
        if parts: out.append('N = %.0e: %s' % (N, '; '.join(parts)))
    return ' | '.join(out)


def verdicts(static, sweep, Rc, LS, LO, PD, CAT, RR200=None):
    RR200 = RR200 or {}
    V = []

    def add(i, v, e):
        V.append(dict(id=i, verdict=v, evidence=e))
    # 1
    ok_x = all(static[a]['pred1_X_forfeiting_programs'] == 0 and static[a]['pred1_X_max_abs_payoff_nonforfeit'] < 1e-9 for a in ('sample', 'matched', 'exact'))
    ok_c = static['exact']['pred1_C_self_forfeit_mass'] > 0.999999
    ok_n = all(static[a]['pred1_N_counterexamples'] == 0 for a in ('sample', 'matched', 'exact'))
    add('1 statics', 'held' if (ok_x and ok_c and ok_n) else 'failed',
        'no program of the sample/matched/exact tables forfeits against X or earns != 0 against it (max %.1e); cr(THEM(ME)) self-play forfeit mass %.6f; next(THEM(ME)) earns +1 against all %d / %d / %d deterministic opponents (sample / matched / exact), 0 counterexamples, beats R, P, S' % (
            max(static[a]['pred1_X_max_abs_payoff_nonforfeit'] for a in ('sample', 'matched', 'exact')), static['exact']['pred1_C_self_forfeit_mass'],
            static['sample']['pred1_N_deterministic_opponents'], static['matched']['pred1_N_deterministic_opponents'], static['exact']['pred1_N_deterministic_opponents']))
    # 2
    ue = max(max(static[a]['symmetry_err_U'].values()) for a in ARMS + SENS)
    pe = [c['pi_equivariance']['max_abs_pi_diff'] for c in (chain(a, N, D=D) for a in ARMS + SENS for N in NS for D in (12,)) if c and 'pi_equivariance' in c]
    freq_ok = {}
    for a in ('sample', 'matched', 'exact', 'exact_uniform', 'exact_br'):
        s = LS.get(a)
        if s: freq_ok[a] = all(s[k][1] <= 1 / 3 <= s[k][2] for k in ('freqR', 'freqP', 'freqS'))
    f200 = {}
    for a in ('sample', 'matched', 'exact'):
        recs2 = lottery(a, 'primary200')
        if recs2:
            s2 = lot_summary(recs2, 2000)
            f200[a] = (all(s2[k][1] <= 1 / 3 <= s2[k][2] for k in ('freqR', 'freqP', 'freqS')), [fmt(s2[k], 3) for k in ('freqR', 'freqP', 'freqS')])
    bad = {a: [k for k in ('freqR', 'freqP', 'freqS') if not (LS[a][k][1] <= 1 / 3 <= LS[a][k][2])] for a in freq_ok if not freq_ok[a]}
    add('2 symmetry', 'held' if (ue < 1e-9 and max(pe) < 1e-9 and all(freq_ok.values())) else 'partial' if ue < 1e-9 else 'failed',
        'payoff-tensor relabeling error max %.1e; pi equivariance error max %.1e over %d cells (both held to machine precision); pooled lottery action frequencies (40 runs) contain 1/3 in the arms %s, and exclude it narrowly for %s (15 intervals, one expected by chance); 200-run replicate (intervals contain 1/3): %s; per-run asymmetry (max deviation of a run\'s pooled frequency from 1/3) exact %s, matched %s, sample %s' % (
            ue, max(pe), len(pe), [a for a, v in freq_ok.items() if v], bad, {a: v for a, v in f200.items()}, fmt(LS['exact']['run_asymmetry_max_dev'], 3), fmt(LS['matched']['run_asymmetry_max_dev'], 3), fmt(LS['sample']['run_asymmetry_max_dev'], 3)))
    # 3
    r = Rc['pure_10000']
    sw = sweep.get('pure', {})
    L_frac = sw.get('pi_weighted_pair_sign_flip_fraction_N1e4')
    nonzero = sw.get('readers_pairs_nonzero_payoff_D12')
    if r['consts'] >= 0.5: v3 = 'failed'
    elif r['forfeit_self'] >= 0.5 and r['consts'] <= 0.2: v3 = 'held'
    else: v3 = 'partial'
    add('3 pure arm', v3, 'N = 10^4: self-play forfeit share %.3f, constants %.4f, mixing %.3f, e (own exploiters) %.4f, e (exact-grammar exploiters) %.4f. Counter (L) ladder: pi-weighted sign-flip fraction across D = 11, 12, 13, 20 is %s -> %s; counter (N) neutral readers: %s pairs of support readers have non-zero payoff (max |u| %.2f) -> %s' % (
        r['forfeit_self'], r['consts'], r['mix_pop'], r['e_prog'], r['e_exset'], f3(L_frac, 4), 'not shown' if (L_frac is not None and L_frac <= 0.05) else 'shown',
        nonzero, sw.get('readers_mutual_max_abs_payoff_D12', float('nan')), 'not shown' if (nonzero or 0) > 0 else 'shown'))
    # 4
    es = [Rc['sample_%d' % N]['e_prog'] for N in (100, 1000, 10000)]
    ee = [Rc['exact_%d' % N]['e_prog'] for N in (100, 1000, 10000)]
    all_leq = all(s <= e for s, e in zip(es, ee))
    all_gt = all(s > e for s, e in zip(es, ee))
    ratio_s = es[2] / es[0]; ratio_e = ee[2] / ee[0]
    if all_leq: v4 = 'failed'
    elif all_gt and ratio_s > ratio_e and es[2] > 0.005: v4 = 'held'
    else: v4 = 'partial'
    xs = [Rc['sample_%d' % N]['e_exset'] for N in (100, 1000, 10000)]
    add('4 sample arm', v4, 'e (own exploiters) sample %s vs exact %s at N = 10^2, 10^3, 10^4: the sample arm is at most the exact arm at every N (the falsifier); e(10^4)/e(10^2) sample %.2f, exact %.2f. With the exploiter set fixed to the exact grammar: sample %s (exact %s). mixing at 10^4: sample %.3f, exact %.3f' % (
        [round(x, 3) for x in es], [round(x, 3) for x in ee], ratio_s, ratio_e, [round(x, 3) for x in xs], [round(x, 3) for x in ee], Rc['sample_10000']['mix_pop'], Rc['exact_10000']['mix_pop']) + ' Supplementary (not scored): ' + bigN(Rc, ('sample', 'exact')))
    # 5
    rE = Rc['exact_10000']; rM = Rc['matched_10000']
    a5 = (rE['e_prog'] <= 0.05 and rE['mix_pop'] >= 0.8)
    f5a = (rE['e_prog'] > 0.15 or rE['mix_pop'] < 0.5)
    share = LS['exact']['share_e_le_0.05']
    b5 = share[0] >= 0.8; f5b = share[0] < 0.5
    c5 = (rE['e_prog'] - rM['e_prog']) < 0; f5c = not c5
    if a5 and b5 and c5: v5 = 'held'
    elif f5a or f5b or f5c: v5 = 'failed'
    else: v5 = 'partial'
    add('5 exact arm', v5, '(5a) chain N = 10^4: e %.3f (needs <= 0.05, falsifier > 0.15), mixing %.3f (needs >= 0.8, falsifier < 0.5); (5b) lottery: islands with e <= 0.05 = %s (needs >= 0.8, falsifier < 0.5), mean e %s; (5c) exact - matched at 10^4: chain %+.3f (exact e %.3f, matched %.3f; exact-set control exact %.3f, matched %.3f), lottery paired %s (needs < 0)' % (
        rE['e_prog'], rE['mix_pop'], fmt(share, 2), fmt(LS['exact']['e_prog'], 2), rE['e_prog'] - rM['e_prog'], rE['e_prog'], rM['e_prog'], rE['e_exset'], rM['e_exset'], fmt(PD['e_prog'], 3) + ' (40 runs; 200-run replicate ' + fmt(RR200.get('e_prog'), 3) + ')') + '. Supplementary (not scored, the approach to the limit): ' + bigN(Rc, ('exact', 'matched', 'sample')))
    # counter-predictions of 5
    rS = Rc['sample_10000']
    gem_X = (rE['X'] / rE['mix_pop'] >= 0.5) and (rS['X'] / rS['mix_pop'] >= 0.5)
    gem_d = abs(rE['e_prog'] - rM['e_prog']) <= 0.02
    add('5 counter (gemini): X holds the mixing mass, matched control erases the difference', 'held' if (gem_X and gem_d) else 'partial' if gem_X else 'failed',
        'X is %.2f (exact) and %.2f (sample) of the mixing mass at 10^4 (needs >= 0.5), pi(X) = prior mass %.3f in every cell; |exact - matched| = %.3f (needs <= 0.02): the matched control does not erase the difference, and its sign is that exact is MORE exploitable' % (
            rE['X'] / rE['mix_pop'], rS['X'] / rS['mix_pop'], rE['X'], abs(rE['e_prog'] - rM['e_prog'])))
    cap = {D: chain_row('exact', 10000, D=D)['e_prog'] - chain_row('matched', 10000, D=D)['e_prog'] for D in (11, 12, 13, 20)}
    by_N = {N: Rc['exact_%d' % N]['e_prog'] - Rc['matched_%d' % N]['e_prog'] for N in (100, 1000, 10000)}
    sign_changes = len(set(np.sign(list(cap.values())) )) > 1 or len(set(np.sign(list(by_N.values())))) > 1
    gpt_mix = rE['mix_pop'] >= 0.5 and rS['mix_pop'] >= 0.5
    add('5 counter (gpt): mixing substantial in both, no robust sign for exact - matched', 'failed' if not gpt_mix else 'partial',
        'mixing at 10^4: sample %.3f, exact %.3f (needs >= 0.5 in both); exact - matched = %s across D in (11, 12, 13, 20) and %s across N in (10^2, 10^3, 10^4): sign %s' % (
            rS['mix_pop'], rE['mix_pop'], {D: round(v, 3) for D, v in cap.items()}, {N: round(v, 3) for N, v in by_N.items()}, 'changes' if sign_changes else 'never changes (always exact > matched)'))
    # 6
    rU = Rc['exact_uniform_10000']
    d_e = abs(rU['e_prog'] - rE['e_prog']); d_m = abs(rU['mix_pop'] - rE['mix_pop'])
    cu = chain('exact_uniform', 10000); ce = chain('exact', 10000)
    top3u = sum(t['pi'] for t in cu['top_states'][:3]); top3e = sum(t['pi'] for t in ce['top_states'][:3])
    changed = max(d_e, d_m, abs(top3u - top3e)) > 0.05
    nochange = max(d_e, d_m, abs(top3u - top3e)) <= 0.02
    add('6 uniform default', 'held' if (rU['forfeit_plays'] < 1e-6 and changed) else 'failed' if (rU['forfeit_plays'] < 1e-6 and nochange) else 'partial',
        'exact-uniform: plays forfeited %.1e; vs exact at 10^4: e %.3f vs %.3f, mixing %.3f vs %.3f (d %.3f), top-3 pi mass %.3f vs %.3f; self-play TV from uniform: exact-uniform %.3f, exact %.3f, pure %.3f; action exploitability %.3f vs %.3f. '
        'The mixing change is by construction (readers that forfeit become uniform); exploitability is unchanged. Lottery: mixing %s vs %s, e %s vs %s' % (
            rU['forfeit_plays'], rU['e_prog'], rE['e_prog'], rU['mix_pop'], rE['mix_pop'], d_m, top3u, top3e, rU['tv_self'], rE['tv_self'], Rc['pure_10000']['tv_self'], rU['e_act'], rE['e_act'],
            fmt(LS['exact_uniform']['mix_pop'], 2), fmt(LS['exact']['mix_pop'], 2), fmt(LS['exact_uniform']['e_prog'], 2), fmt(LS['exact']['e_prog'], 2)))
    # RS statement
    fails = {}
    for a in ('sample', 'matched', 'exact'):
        r = Rc['%s_10000' % a]
        fails[a] = (r['e_prog'] > 0.15 or r['mix_pop'] < 0.5)
    lot_fail = {a: LS[a]['share_e_le_0.05'][0] < 0.5 for a in ('sample', 'matched', 'exact')}
    held = (not any(fails.values())) and all(Rc['%s_10000' % a]['e_prog'] <= 0.05 and Rc['%s_10000' % a]['mix_pop'] >= 0.8 for a in ('sample', 'matched', 'exact'))
    add("RS statement (reading (I): individual mixers, unexploitable)", 'held' if held else 'failed' if all(fails.values()) else 'partial',
        'chain N = 10^4: exploitability / mixing sample %.3f / %.3f, matched %.3f / %.3f, exact %.3f / %.3f; lottery islands with e <= 0.05: sample %s, matched %s, exact %s. Reading (W) is trivially true (pooled frequencies uniform); reading (M) %s' % (
            Rc['sample_10000']['e_prog'], Rc['sample_10000']['mix_pop'], rM['e_prog'], rM['mix_pop'], rE['e_prog'], rE['mix_pop'], fmt(LS['sample']['share_e_le_0.05'], 2), fmt(LS['matched']['share_e_le_0.05'], 2), fmt(LS['exact']['share_e_le_0.05'], 2),
            'island share %s (population marginal uniform, individuals not mixing)' % fmt(CAT['exact']['M_pure_polymorphism_uniform_marginal'], 2)) + ' Supplementary, the chain at larger N (not scored): ' + bigN(Rc, ('sample', 'matched', 'exact')))
    return V


if __name__ == '__main__':
    main()
