"""Report for the bridge-less rivals run: runs/bridgeless-rivals.md and runs/bridgeless-rivals.json.
Spec specs/2026-10-05-bridgeless-rivals.md; predictions predictions/2026-10-05-bridgeless-rivals.md."""
import json, math, os, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import bridgeless_rivals as BR
from rival_islands_report import wilson, poisson_ci, km

RUNS = BR.RUNS
OUT_MD = os.path.join(RUNS, 'bridgeless-rivals.md')
OUT_JS = os.path.join(RUNS, 'bridgeless-rivals.json')
MARKS = (100, 1000, 10000, 100000)
VERDICTS = '**Verdicts.**\n\n| # | prediction | outcome |\n|---|---|---|\n| RE 1 | more rivals gain bridges; τ = 0 share falls from n = 9 to 15; τ = 10⁻⁴ ratio in [0.1, 0.5] | **failed, falsifier fired** on 9 → 13 (n = 15 not computable): the τ = 0 share rises 0.214 → 0.252 → 0.253 and no n = 9 bridge-less rival gains a bridge; the τ = 10⁻⁴ clause held (0.425 at n = 13) |\n| RE 2 | dense bridge-less ≥ 0.5, bridged ≤ 0.1; (c) ≥ 0.4; (b) between | **failed, falsifier fired** for S\\* (0.01; bridge-less only at τ ≥ 10⁻⁵ and A-faked); held for P\\* and P\\*′ (0.97), (c) (0.67, +0.55) and (b) (0.54–0.60 between 0.97 and 0.00–0.06); bridged ≤ 0.1 failed narrowly for B₁ (0.12 [0.07, 0.20]), held for H and B₄ |\n| RE 3 | 1–15 of 3,000 at the horizon; bridge-less share ≥ 0.5 | **held** (9; 0.89; the one bridged separation had a dead bridge, sol\'s point) |\n| RE 4 | island P(C,C) ≥ 0.95 per cell; cf ≤ 0.8 in separated runs; \\|Δq\\| ≤ 0.1 | **failed, falsifier fired** on \\|Δq\\| (holder form −0.41 to −0.52 in bridged cells, by absorption after nucleation); island P(C,C) ≥ 0.978 per cell and cf 0.49–0.66 held; q_est within ±0.10 |\n| RE 5 | scaling: bridge-less ≥ 0.5 at (400, 64) and 3·10⁵; bridged faster at (200, 256) | **held** (P\\* 12/12 and 13/13 separated, 0 losses; B₁ 0.00 at (200, 256) against 0.12 at (200, 64)); P\\* cells at 12–13 runs, not 40 |\n| S1 | P\\* family establishes in [0.55, 0.95]; ≥ 0.9 of separations survive | failed, falsifier not fired (establishment 0.98, above the band); survival 0.99 and hazard bound held |\n| S2 | S\\* ≤ 0.1, losses by 2>1 / 2>3 | held (0.01; 151 replacements) |\n| S3 | B₁, B₄ in [0.03, 0.3]; mediation-before-loss ≥ 0.6 | held (0.12, 0.09; 0.80, 0.76) |\n| S4 | H ≤ 0.1 | held (0.01) |\n| S5 | (c) within 0.15 of dense P\\* | failed, falsifier not fired (0.67 vs 0.97, a difference of exactly 0.30; B₁\'s own faker) |\n| S6 | sparse = 1 − (1 − p̂)^16 ± 0.15 | held (0.54 vs 0.54; 0.60 vs 0.54) |\n| S7 | 2–12 natural horizon separations, ≥ half P\\*-family | held (9; 8 of 9) |\n| S8 | island P(C,C) ≥ 0.97 per cell; cf in separated runs [0.45, 0.85] | held (≥ 0.978; 0.49–0.66); two single runs collapsed to all-D by B₁\'s faker |\n\n**Reading.**\n- **The bridge-less obstruction is a fixed fraction of rival mass, not a vanishing one.** On 9 → 13 the hard bridge-less share (no bridge, no mediator, not eaten by A) is 0.21 → 0.26 → 0.26, 0.98–0.99 of it by mass is the P\\* family (`and(BOX1(THEM(·)),not(BOX(THEM(·))))`: cooperate when provable from PA + Con but not from PA; the rest is a tail of light `not(or(BOX(…),BOXD(…)))` classes), and no member present at n = 9 gains a bridge as the language grows. The threshold τ only adds rivals that `BOX1(THEM(ME))` eats, so "literally bridge-less" is the right object and is stable at about a quarter of rival mass.\n- **The mediation-before-loss probability is the bridge\'s scramble survival.** A living bridge resolved every bridged rivalry (0 of 525); separations come only from runs in which the bridge died early, and the bridge\'s death is a per-run scramble lottery whose failure shrinks geometrically in I (≈ 0.19 per run at I = 64 with ≈ 42 seeded islands).\n- **Bridge-less rivals make metapopulation universality fail with probability → 1 along I ≫ N.** Each P\\*-family copy establishes with probability ≈ 0.048 at N = 200 and, once established, holds ≈ 40% of the islands with no measured loss; natural separations occur at μ_bl·N·I·p₁ per run (0.0030 measured, 0.0032 predicted at (200, 64)), so the expected number of independent P\\* establishments grows linearly in I. At fixed N ≥ 200 a patchwork is certain for I ≫ 1/(μ_bl·N·p₁) ≈ 10⁴. Island-level efficiency is untouched (island P(C,C) ≥ 0.978 in every cell, every certified island efficient); what fails is the counterfactual cross-island P(C,C) (≈ 0.6 in separated runs).\n- **Probe-readers carry their own spoilers into the metapopulation.** B₁ without bridges is less permanent than P\\* only because its faker captures it, and in two runs that faker, then D, took the whole archipelago: forcing a fakeable rival everywhere is the one way this run found to lose efficiency at run level.\n- **Holder-form q is the wrong nucleation statistic when bridges are active**; q_est is flat (±0.10) across every forced rival.\n'


def ci(k, n):
    if n == 0: return '–'
    lo, hi = wilson(k, n)
    return '%.2f [%.2f, %.2f]' % (k / n, lo, hi)


def e(x, d=2):
    if x is None or (isinstance(x, float) and math.isnan(x)): return '–'
    if x == 0: return '0'
    return ('%.' + str(d - 1) + 'e') % x if (abs(x) < 1e-2 or abs(x) >= 1e4) else ('%.' + str(d + 1) + 'g') % x


def short(name):
    f = BR.forced()
    lab = {f['bridgeless'][0]: 'P*', f['bridgeless'][1]: "P*'", f['bridgeless'][2]: 'S*', f['bridged'][0]: 'B1',
           f['bridged'][1]: 'H', f['bridged'][2]: 'B4'}
    return lab.get(name, name)


def qstat(rows, ref, key='n_loc_end', B=2000):
    rr = {r['rep']: r for r in ref}
    a = np.array([(r[key], rr[r['rep']][key]) for r in rows if r['rep'] in rr], float)
    if len(a) == 0 or a[:, 1].sum() == 0: return float('nan'), (float('nan'), float('nan')), a
    q = a[:, 0].sum() / a[:, 1].sum()
    rng = np.random.default_rng(11); bs = []
    for _ in range(B):
        ix = rng.integers(0, len(a), len(a))
        if a[ix, 1].sum() > 0: bs.append(a[ix, 0].sum() / a[ix, 1].sum())
    return float(q), (float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))), a


def dq(a, b, B=2000):
    """q(a) - q(b) with independent run bootstraps (different initial states)."""
    if len(a) == 0 or len(b) == 0: return float('nan'), (float('nan'), float('nan'))
    d0 = a[:, 0].sum() / a[:, 1].sum() - b[:, 0].sum() / b[:, 1].sum()
    rng = np.random.default_rng(12); bs = []
    for _ in range(B):
        ia = rng.integers(0, len(a), len(a)); ib = rng.integers(0, len(b), len(b))
        if a[ia, 1].sum() > 0 and b[ib, 1].sum() > 0:
            bs.append(a[ia, 0].sum() / a[ia, 1].sum() - b[ib, 0].sum() / b[ib, 1].sum())
    return float(d0), (float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)))


def load_all():
    rows = {}
    for exp in ('iid', 'dense', 'nobridge', 'sparse', 'nat', 'scale'):
        rows[exp] = BR.load(exp); rows[exp + '-m0'] = BR.load(exp, True)
    return rows


def cell_stats(rs, ref, qa_ctrl):
    n = len(rs)
    st = dict(n=n)
    st['rival_est'] = sum(r['rival_est'] for r in rs)
    st['ever_sep'] = sum(r['ever_sep_tag'] for r in rs)
    st['sep_end'] = sum(r['sep_end_tag'] for r in rs)
    st['both_end'] = sum(r['both_end'] for r in rs)
    st['gen_sep_end'] = sum(r['n_sep_end'] > 0 for r in rs)
    st['gen_sep_ever'] = sum(r['first_sep'] >= 0 for r in rs)
    st['losses'] = sum(r['loss_t'] >= 0 for r in rs)
    st['loss_A'] = sum(r['loss_net'] == 1 for r in rs); st['loss_R'] = sum(r['loss_net'] == 2 for r in rs)
    st['expo'] = sum(r['expo'] for r in rs)
    lo, hi = poisson_ci(st['losses'])
    T = st['expo']
    st['hazard'] = [st['losses'] / T if T else float('nan'), lo / T if T else float('nan'), hi / T if T else float('nan')]
    inv = Counter()
    for r in rs:
        for k, v in r['inv'].items(): inv[k] += v
    st['inv'] = dict(inv)
    st['rl'] = [inv.get('2>1', 0), inv.get('2>3', 0), inv.get('2>0', 0)]
    st['al'] = [inv.get('1>2', 0), inv.get('1>3', 0), inv.get('1>0', 0)]
    last = Counter(r['last_rival_loss'] for r in rs if r['loss_net'] == 2)
    st['last_loss_R'] = {str(k): v for k, v in last.items()}
    est = [r for r in rs if r['rival_est']]
    st['med_den'] = len(est); st['med'] = sum(r['med_before_end'] for r in est)
    sepd = [r for r in rs if r['ever_sep_tag']]
    st['med_sep_den'] = len(sepd); st['med_sep'] = sum(r['med_before_end'] for r in sepd)
    # per island rival establishment (local ancestry, tag 2) and A's (tag 1)
    I = rs[0]['I']
    st['p_rival_loc'] = sum(r['est_by_tag']['2'][0] for r in rs) / (n * I)
    st['p_rival_cls_loc'] = sum(r['est_rival_cls_local'] for r in rs) / (n * I)
    st['rival_isl_est'] = float(np.mean([sum(r['est_by_tag']['2']) for r in rs]))
    st['A_isl_est'] = float(np.mean([sum(r['est_by_tag']['1']) for r in rs]))
    st['bridge_isl_est'] = float(np.mean([sum(r['est_by_tag']['3']) for r in rs]))
    st['bseed_isl'] = float(np.mean([r['bridge_seed_islands'] for r in rs]))
    st['bseed_cp'] = float(np.mean([r['bridge_seed_copies'] for r in rs]))
    st['b_est_runs'] = sum(r['bridge_est'] > 0 for r in rs)
    st['b_held_end'] = float(np.mean([r['bridge_held_end'] for r in rs]))
    st['b_alive_end'] = sum(r['bridge_alive_end'] for r in rs)
    st['n_med_events'] = sum(r['n_med'] for r in rs)
    st['held_end'] = {t: float(np.mean([r['held_end'][t] for r in rs])) for t in ('0', '1', '2', '3')}
    st['held_R_sep'] = float(np.mean([r['held_end']['2'] for r in rs if r['sep_end_tag']])) if st['sep_end'] else float('nan')
    st['pcc'] = [float(np.mean([r['pcc'] for r in rs])), float(np.min([r['pcc'] for r in rs]))]
    st['cf'] = float(np.mean([r['cf_cross_pcc'] for r in rs]))
    sr = [r for r in rs if r['sep_end_tag']]
    st['cf_sep'] = float(np.mean([r['cf_cross_pcc'] for r in sr])) if sr else float('nan')
    st['pcc_sep'] = float(np.mean([r['pcc'] for r in sr])) if sr else float('nan')
    tl = [r['loss_t'] if r['loss_t'] >= 0 else r['stop_gen'] for r in sepd]
    ev = [r['loss_t'] >= 0 for r in sepd]
    s = km(tl, ev, MARKS) if sepd else {}
    st['km'] = [s.get(m, float('nan')) for m in MARKS]
    st['t_sep_med'] = float(np.median([r['t_sep_tag'] for r in sepd])) if sepd else float('nan')
    st['t_loss_med'] = float(np.median([r['loss_t'] for r in rs if r['loss_t'] >= 0])) if st['losses'] else float('nan')
    st['status'] = dict(Counter(r['status'] for r in rs))
    st['hours'] = sum(r['time_s'] for r in rs) / 3600
    if ref:
        q, qci, a = qstat(rs, ref)
        st['q'] = [q, qci[0], qci[1], len(a)]
        if qa_ctrl is not None and len(a):
            d, dci = dq(a, qa_ctrl[0])
            st['dq'] = [d, dci[0], dci[1]]
        q2, qci2, a2 = qstat(rs, ref, key='n_loc_est')
        st['q_est'] = [q2, qci2[0], qci2[1]]
        if qa_ctrl is not None and len(a2):
            d, dci = dq(a2, qa_ctrl[1])
            st['dq_est'] = [d, dci[0], dci[1]]
    st['run_alld'] = sum(r['pcc'] < 0.05 for r in rs)
    st['run_ineff'] = sum(r['pcc'] < 0.95 for r in rs)
    return st


def main():
    rows = load_all()
    stat = json.load(open(BR.STATIC))
    forced = BR.forced()
    out = dict(static_summary={}, cells={}, nat={}, scale={})
    L = []
    P = L.append
    P('# Bridge-less rivals: prior mass in n, and mediation before loss at N ≥ 200 (`src/bridgeless_rivals.py`)')
    P('')
    P('Spec `specs/2026-10-05-bridgeless-rivals.md`; predictions `predictions/2026-10-05-bridgeless-rivals.md`. Modal arm, PD, '
      'w = 0.3, ε = 0, iid length-prior seeds at n = 9, complete island graph, generation = I·N births, boundary mN = 0.3·N/T_nuc '
      '(1.091 at N = 200, 1.714 at N = 400). Finite-cutoff screening and finite-horizon lottery and hazard results, not π. '
      'Intervals: Wilson 95% over runs (runs are the independent units), exact Poisson for hazards, bootstrap for q.')
    P('')
    P('**What ran.** Everything in the spec\'s priority order: static (n = 9, 12, 13; n = 15 and 14 do not fit), (a) dense 6 × 100, '
      '(d) iid 100, (c) bridge removed 100, (b) sparse 6 × 100 (each with paired m = 0 references), (f) 3,000 natural runs, (e) the '
      'scaling panel with B₁ at the spec\'s 40 runs per cell and P\\* capped at 12–13 runs per cell (declared deviation: the machine '
      'load reached 28 on 10 cores and a P\\* run took 10–15 minutes; every P\\* run sampled was separated with no loss, so the cap '
      'bounds the separation probability below by 0.76 at 95%). *Deviations:* B₂ (B₁\'s twin) replaced by the mass-matched B₄; '
      'kernel tags for S\\* taken against FairBot (S\\* mutually defects only with FairBot).')
    P('')
    # ---------------------------------------------------------------- static
    P('## 1. Static screening (n = 9, 12, 13; n = 15 does not fit)')
    P('')
    P(stat['note_n15'] + ' Classes merged within L_n by identical row and column; the n = 9 and 12 blocks reproduce the existing '
      'caches exactly. Masses in cut units (normalized within the cutoff) unless marked raw (units of the infinite length prior; '
      'inf = raw/(π²/12)). Omitted tail ω(n) = π²/12 − Σ_{s≤n} 1/(2s²) < 1/(2n).')
    P('')
    for key, lab in (('A', 'A = {FairBot, `BOX1(THEM(ME))`}'), ('probe', 'probe-readers {`BOX(THEM(^C))`, `BOX1(THEM(^C))`} (comparison)')):
        P('### Rivals of %s' % lab)
        P('')
        P('| n | classes (canons) | ω(n) | rivals (full) | rival μ cut / raw / inf | union bridge μ | path length 1 / 2 / 3 / none |')
        P('|---|---|---|---|---|---|---|')
        for n in ('9', '12', '13'):
            s = stat[key]['stat'][n]; ph = s['path_hist']
            P('| %s | %s (%s) | %.4f | %d (%d) | %s / %s / %s | %.4f | %s / %s / %s / %s |' % (
                n, format(s['K'], ','), format(s['n_canon'], ','), s['omitted'], s['n_rivals'], s['n_full'], e(s['rival_mu']), e(s['rival_raw']),
                e(s['rival_inf']), s['union_bridge_mu'], ph.get('1', 0), ph.get('2', 0), ph.get('3', 0), ph.get('None', 0)))
        P('')
        P('Bridge-less rivals by threshold τ (heaviest bridge ≤ τ; "total": total bridge mass ≤ τ; "safe": heaviest establisher bridge ≤ τ). '
          'Cells: count, bridge-less fraction of rival μ, bridge-less / bridged ratio, bridge-less raw mass.')
        P('')
        P('| n | variant | τ = 0 | τ = 10⁻⁵ | τ = 10⁻⁴ | τ = 10⁻³ |')
        P('|---|---|---|---|---|---|')
        for n in ('9', '12', '13'):
            g = stat[key]['stat'][n]['agg']
            for var in ('heaviest', 'total', 'safe'):
                cells = []
                for t in ('0', '1e-05', '0.0001', '0.001'):
                    v = g['%s|%s' % (var, t)]
                    cells.append('%d, %.3f, %s, %s' % (v['n_bridgeless'], v['frac'], '%.3f' % v['ratio'] if v['ratio'] is not None else '–', e(v['bridgeless_raw'])))
                P('| %s | %s | %s |' % (n, var, ' | '.join(cells)))
        P('')
        # composition of bridge-less mass
        P('Composition of rival mass (fractions of rival μ): A-faked = some member of the reference pair strictly invades R '
          '(ρ(A_j into R) > 1/N, R a sucker of A_j); mediated = mediator mass > 10⁻⁴; "hard" = bridge-less at τ, neither A-faked nor mediated.')
        P('')
        P('| n | A-faked | τ = 0 bridge-less | τ = 0 hard | τ = 10⁻⁴ bridge-less | of which A-faked | τ = 10⁻⁴ hard (count) |')
        P('|---|---|---|---|---|---|---|')
        comp = {}
        for n in ('9', '12', '13'):
            s = stat[key]['stat'][n]; R = s['rivals']; tot = s['rival_mu']
            fk = lambda r: max(r['rho_into_R']) > 1 / 200
            hard = lambda r: r['mediator_mass'] <= 1e-4 and not fk(r)
            t0 = [r for r in R if r['n_bridges'] == 0]; t4 = [r for r in R if r['heaviest_bridge_mu'] <= 1e-4]
            m = lambda xs: sum(r['mu'] for r in xs) / tot
            comp[n] = dict(afaked=m([r for r in R if fk(r)]), t0=m(t0), t0_hard=m([r for r in t0 if hard(r)]), t4=m(t4),
                           t4_afaked=m([r for r in t4 if fk(r)]), t4_hard=m([r for r in t4 if hard(r)]),
                           n_t4_hard=sum(1 for r in t4 if hard(r)))
            c = comp[n]
            P('| %s | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f (%d) |' % (n, c['afaked'], c['t0'], c['t0_hard'], c['t4'], c['t4_afaked'], c['t4_hard'], c['n_t4_hard']))
        out['static_summary'][key] = comp
        P('')
        P('Cutoff tracking (rivals at the lower cutoff followed by representative canon; rival status is per canon and cutoff-invariant, '
          'so rival raw mass only accumulates; "gained" = bridge-less at the lower cutoff with a bridge at the higher):')
        P('')
        P('| step | rivals | split into ≥ 2 classes | τ = 0 bridge-less | gained a bridge (any part) | μ of gainers | heaviest gained bridge μ |')
        P('|---|---|---|---|---|---|---|')
        for k, tr in stat[key]['track'].items():
            g = [t for t in tr if t['gained_any']]
            P('| %s | %d | %d | %d | %d | %s | %s |' % (k, len(tr), sum(t['split'] > 1 for t in tr), sum(t['hb_lo'] == 0 for t in tr), len(g),
                                                      e(sum(t['mu_lo'] for t in g)), e(max([t['hb_hi'] for t in g], default=0))))
        P('')
    # heavy rival tables
    for n, top in (('9', 20), ('13', 20)):
        P('### The %d heaviest rivals of A at n = %s' % (top, n))
        P('')
        P('| rival | μ | full | bridges (n, mass, safe mass) | heaviest bridge (μ) | prey: A-net / bridges (heaviest) | mediators (n, mass) | path | ρ₂₀₀(R into FB, FB1) | ρ₂₀₀(FB, FB1 into R) |')
        P('|---|---|---|---|---|---|---|---|---|---|')
        for r in stat['A']['stat'][n]['rivals'][:top]:
            P('| `%s` | %s | %s | %d, %s, %s | %s | %s / %s (%s) | %d, %s | %s | %s, %s | %s, %s |' % (
                r['name'], e(r['mu']), 'y' if r['full'] else ('FB only' if r['md'][0] else 'FB1 only'), r['n_bridges'], e(r['bridge_mass']), e(r['safe_mass']),
                ('`%s` (%s)' % (r['heaviest_bridge'], e(r['heaviest_bridge_mu']))) if r['heaviest_bridge'] else 'none',
                e(r['prey_netA_mass']), e(r['prey_bridges_mass']), ('`%s`' % r['prey_bridges_top'][0][0]) if r['prey_bridges_top'] else '–',
                r['n_mediators'], e(r['mediator_mass']), r['path_len'], e(r['rho_R_into'][0]), e(r['rho_R_into'][1]),
                e(r['rho_into_R'][0]), e(r['rho_into_R'][1])))
        P('')
    P('### Forced rivals (n = 9)')
    P('')
    P('| label | class | μ | tags against | bridge mass (static) | heaviest bridge | tag-3 mass (kernel) | tag-2 network mass | mediator mass |')
    P('|---|---|---|---|---|---|---|---|---|')
    for x in forced['six']:
        i = forced['info'][x]
        P('| %s | `%s` | %s | `%s` | %s | %s | %s | %s | %s |' % (short(x), x, e(i['mu']), i['a_ref'], e(i['static_bridge_mass']),
                                                        ('`%s` (%s)' % (i['heaviest'], e(i['hb_mu']))) if i['heaviest'] else 'none',
                                                        e(i['tag3_mass']), e(i['tag2_mass']), e(i['mediator_mass'])))
    P('')
    # ---------------------------------------------------------------- lottery
    P('## 2. Enriched lottery (N = 200, I = 64, mN = 1.091, n = 9, horizon 10⁵, 100 runs per cell)')
    P('')
    ctrl = rows['iid']; ctrl0 = rows['iid-m0']
    qa_ctrl = (qstat(ctrl, ctrl0)[2], qstat(ctrl, ctrl0, key='n_loc_est')[2]) if ctrl and ctrl0 else None
    if ctrl:
        cs = dict(n=len(ctrl), gen_sep_end=sum(r['n_sep_end'] > 0 for r in ctrl), gen_sep_ever=sum(r['first_sep'] >= 0 for r in ctrl),
                  pcc=[float(np.mean([r['pcc'] for r in ctrl])), float(np.min([r['pcc'] for r in ctrl]))],
                  cf=float(np.mean([r['cf_cross_pcc'] for r in ctrl])), hours=sum(r['time_s'] for r in ctrl) / 3600,
                  status=dict(Counter(r['status'] for r in ctrl)))
        if ctrl0:
            q, qci, a = qstat(ctrl, ctrl0); cs['q'] = [q, qci[0], qci[1], len(a)]
            q, qci, a = qstat(ctrl, ctrl0, key='n_loc_est'); cs['q_est'] = [q, qci[0], qci[1], len(a)]
        out['cells']['d iid'] = cs
        P('**(d) iid control:** %d runs; generic separation ever %d, at the horizon %d; island P(C,C) %.3f (min %.3f); cf cross-island %.3f; '
          'q (holder form) %s; q_est (local establishment form) %s; status %s; %.2f worker-h.' % (cs['n'], cs['gen_sep_ever'], cs['gen_sep_end'], cs['pcc'][0], cs['pcc'][1], cs['cf'],
                                                             ('%.2f [%.2f, %.2f] (%d pairs)' % tuple(cs['q'])) if 'q' in cs else '–',
                                                             ('%.2f [%.2f, %.2f]' % tuple(cs['q_est'][:3])) if 'q_est' in cs else '–', cs['status'], cs['hours']))
        P('')
    groups = []
    for exp, lab in (('dense', 'a'), ('nobridge', 'c'), ('sparse', 'b')):
        by = defaultdict(list)
        for r in rows[exp]: by[r['rival']].append(r)
        ref = defaultdict(list)
        for r in rows[exp + '-m0']: ref[r['rival']].append(r)
        for rv in forced['six']:
            if by.get(rv):
                groups.append(('(%s) %s' % (lab, exp), rv, by[rv], ref.get(rv, [])))
    if groups:
        S = {}
        for g, rv, rs, ref in groups:
            S[(g, rv)] = cell_stats(rs, ref, qa_ctrl)
            out['cells']['%s %s' % (g, short(rv))] = S[(g, rv)]
        P('### Separation, loss and mediation')
        P('')
        P('Horizon separated = tags 1 and 2 each hold a certified island at the end; generic = any two certified holders mutually defect at the end. '
          'Hazard = network losses per minority-island-generation after the first separation (exposure ∫ min(held₁, held₂) dt). '
          'Rival-island losses by strong-holder transition: replacement 2>1 / absorption (mediation) 2>3 / capture 2>0. '
          'Mediation-before-loss = runs with a 2>3 event at or before the loss (or horizon) / runs in which the rival established.')
        P('')
        P('| cell | rival | runs | rival established | ever separated | horizon separated | generic sep. end | losses (A / R) / exposure | hazard [95%] | KM S(10²/10³/10⁴/10⁵) | rival-island losses 2>1 / 2>3 / 2>0 | last loss of R by tag | mediation-before-loss | worker-h |')
        P('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        for g, rv, rs, ref in groups:
            s = S[(g, rv)]
            P('| %s | %s | %d | %s | %s | %s | %d | %d (%d / %d) / %s | %s [%s, %s] | %s | %d / %d / %d | %s | %s | %.2f |' % (
                g, short(rv), s['n'], ci(s['rival_est'], s['n']), ci(s['ever_sep'], s['n']), ci(s['sep_end'], s['n']), s['gen_sep_end'],
                s['losses'], s['loss_A'], s['loss_R'], e(s['expo']), e(s['hazard'][0]), e(s['hazard'][1]), e(s['hazard'][2]),
                ' / '.join('%.2f' % v for v in s['km']), s['rl'][0], s['rl'][1], s['rl'][2], s['last_loss_R'] or '–',
                ci(s['med'], s['med_den']), s['hours']))
        P('')
        P('### Establishment, bridge founders, efficiency and q')
        P('')
        P('| cell | rival | per-island local rival establishment (tag 2 / the class R) | islands established by A / rival / bridge (mean per run) | bridge founders: seeded islands, copies (mean) | runs with a bridge establishment | bridge alive at end (runs) | bridge islands at end (mean) | mediation events | islands held at end A / R / bridge / other | island P(C,C) (min) | runs all-D / with island P(C,C) < 0.95 | cf cross P(C,C): all / separated runs | q holder [95%] | Δq holder vs (d) | q_est [95%] | Δq_est vs (d) |')
        P('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        for g, rv, rs, ref in groups:
            s = S[(g, rv)]; h = s['held_end']
            P('| %s | %s | %.4f / %.4f | %.1f / %.2f / %.2f | %.1f, %.1f | %d | %d | %.2f | %d | %.1f / %.1f / %.1f / %.1f | %.3f (%.3f) | %d / %d | %.3f / %s | %s | %s | %s | %s |' % (
                g, short(rv), s['p_rival_loc'], s['p_rival_cls_loc'], s['A_isl_est'], s['rival_isl_est'], s['bridge_isl_est'], s['bseed_isl'], s['bseed_cp'],
                s['b_est_runs'], s['b_alive_end'], s['b_held_end'], s['n_med_events'], h['1'], h['2'], h['3'], h['0'], s['pcc'][0], s['pcc'][1], s['run_alld'], s['run_ineff'], s['cf'],
                '%.3f' % s['cf_sep'] if not math.isnan(s['cf_sep']) else '–',
                ('%.2f [%.2f, %.2f]' % tuple(s['q'][:3])) if 'q' in s else '–', ('%+.2f [%+.2f, %+.2f]' % tuple(s['dq'])) if 'dq' in s else '–',
                ('%.2f [%.2f, %.2f]' % tuple(s['q_est'][:3])) if 'q_est' in s else '–', ('%+.2f [%+.2f, %+.2f]' % tuple(s['dq_est'])) if 'dq_est' in s else '–'))
        P('')
    if groups:
        P('### Separation conditional on the bridge (bridged rivals): bridge established on some island / bridge alive at the end')
        P('')
        P('| cell | rival | runs with a bridge establishment: separated at horizon | without: separated | bridge alive at end: separated | bridge extinct: separated | median bridge extinction gen (extinct runs) |')
        P('|---|---|---|---|---|---|---|')
        for g, rv, rs, ref in groups:
            if rv not in forced['bridged']: continue
            a = [r for r in rs if r['bridge_est'] > 0]; b = [r for r in rs if r['bridge_est'] == 0]
            ae = [r for r in rs if r['bridge_alive_end']]; be = [r for r in rs if not r['bridge_alive_end']]
            te = [r['t_ext'][3] for r in be if r['t_ext'][3] >= 0]
            row = dict(est=[len(a), sum(r['sep_end_tag'] for r in a)], noest=[len(b), sum(r['sep_end_tag'] for r in b)],
                       alive=[len(ae), sum(r['sep_end_tag'] for r in ae)], dead=[len(be), sum(r['sep_end_tag'] for r in be)],
                       t_ext_med=float(np.median(te)) if te else float('nan'))
            out['cells']['%s %s' % (g, short(rv))]['bridge_cond'] = row
            P('| %s | %s | %d / %d | %d / %d | %d / %d | %d / %d | %s |' % (g, short(rv), row['est'][1], row['est'][0], row['noest'][1], row['noest'][0],
                                                               row['alive'][1], row['alive'][0], row['dead'][1], row['dead'][0], e(row['t_ext_med'])))
        P('')
    # ---------------------------------------------------------------- natural
    nat = rows['nat']
    if nat:
        P('## 3. Unconditional natural runs (f): (200, 64), boundary, %d runs' % len(nat))
        P('')
        out['nat'] = natural(nat, stat, P)
    sc = rows['scale']
    if sc:
        P('## 4. Scaling panel (e): dense forced P\\* and B₁')
        P('')
        by = defaultdict(list)
        for r in sc: by[(r['rival'], r['N'], r['I'], r['gens'])].append(r)
        P('| rival | N | I | horizon | runs | rival established | ever separated | horizon separated | losses / exposure | hazard [95%] | rival-island losses 2>1 / 2>3 / 2>0 | mediation-before-loss | island P(C,C) | cf cross (separated) | worker-h |')
        P('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        for k in sorted(by, key=lambda k: (short(k[0]), k[1], k[2], k[3])):
            s = cell_stats(by[k], [], None)
            out['scale']['%s %d %d %d' % (short(k[0]), k[1], k[2], k[3])] = s
            P('| %s | %d | %d | %s | %d | %s | %s | %s | %d / %s | %s [%s, %s] | %d / %d / %d | %s | %.3f | %s | %.2f |' % (
                short(k[0]), k[1], k[2], e(k[3]), s['n'], ci(s['rival_est'], s['n']), ci(s['ever_sep'], s['n']), ci(s['sep_end'], s['n']),
                s['losses'], e(s['expo']), e(s['hazard'][0]), e(s['hazard'][1]), e(s['hazard'][2]), s['rl'][0], s['rl'][1], s['rl'][2],
                ci(s['med'], s['med_den']), s['pcc'][0], '%.3f' % s['cf_sep'] if not math.isnan(s['cf_sep']) else '–', s['hours']))
        P('')
    P('## 5. Verdicts and reading')
    P('')
    P(VERDICTS)
    open(OUT_MD, 'w').write('\n'.join(L) + '\n')
    json.dump(out, open(OUT_JS, 'w'), indent=1, default=float)
    print('\n'.join(L))


def natural(nat, stat, P):
    S9 = {r['name']: r for r in stat['A']['stat']['9']['rivals']}
    n = len(nat)
    ever = [r for r in nat if r['first_sep'] >= 0]; end = [r for r in nat if r['n_sep_end'] > 0]
    res = dict(n=n, ever=len(ever), end=len(end), pcc=float(np.mean([r['pcc'] for r in nat])),
               min_pcc=float(np.min([r['pcc'] for r in nat])), hours=sum(r['time_s'] for r in nat) / 3600)
    P('Ever separated %s; separated at the horizon %s (Wilson 95%%; zero gives the rule-of-three bound 3/n = %.4f). Island P(C,C) mean %.4f, '
      'min %.3f; %.2f worker-h.' % (ci(len(ever), n), ci(len(end), n), 3 / n, res['pcc'], res['min_pcc'], res['hours']))
    P('')

    def rtype(s):
        a, b = s['a'], s['b']
        if s['inA'][0] and not s['inA'][1]: rv = b
        elif s['inA'][1] and not s['inA'][0]: rv = a
        else: return None, 'neither in A'
        r = S9.get(rv)
        if r is None: return rv, 'not a rival of A'
        if r['n_bridges'] == 0: return rv, 'bridge-less (tau = 0)'
        if max(r['rho_into_R']) > 1 / 200: return rv, 'A-faked'
        if r['heaviest_bridge_mu'] <= 1e-4: return rv, 'bridge-less (tau = 1e-4)'
        return rv, 'bridged'
    tab = defaultdict(Counter); lst = []
    for r in nat:
        for s in r.get('seps', []):
            rv, t = rtype(s)
            tab[s['kind']][t] += 1
            lst.append(dict(rep=r['rep'], kind=s['kind'], a=s['a'], b=s['b'], rival=rv, type=t, n_bridge_classes=s['n_bridge_classes'],
                            bridge_seed=s['bridge_seed'], bridge_seed_islands=s['bridge_seed_islands'], bridge_held_end=s['bridge_held_end'],
                            bridge_alive_end=s['bridge_alive_end'], mediations=s['mediations'], held_a=s['held_a'], held_b=s['held_b'],
                            sep_end=r['n_sep_end'] > 0))
    res['types'] = {k: dict(v) for k, v in tab.items()}
    res['list'] = lst
    P('| separation | bridge-less (τ = 0) | bridge-less (τ = 10⁻⁴) | A-faked | bridged | neither in A / not a rival of A |')
    P('|---|---|---|---|---|---|')
    for k in ('first', 'end'):
        c = tab.get(k, Counter())
        P('| %s | %d | %d | %d | %d | %d |' % ('ever (first separated pair)' if k == 'first' else 'at the horizon (every pair)', c['bridge-less (tau = 0)'],
                                          c['bridge-less (tau = 1e-4)'], c['A-faked'], c['bridged'], c['neither in A'] + c['not a rival of A']))
    P('')
    P('Every separation (first separated pair of each ever-separated run, and every pair separated at the end): bridge classes of the pair in the '
      'run\'s support, seeded copies / islands, islands held at the end, alive at the end, mediation transitions (a strong holder of the pair '
      'replaced by a bridge class), islands held at the end by each member.')
    P('')
    P('| rep | kind | pair | rival type | bridge classes | seeded copies / islands | bridge islands at end | bridge alive | mediations | held a / b | separated at end |')
    P('|---|---|---|---|---|---|---|---|---|---|---|')
    for x in lst:
        P('| %d | %s | `%s` × `%s` | %s | %d | %d / %d | %d | %s | %d | %d / %d | %s |' % (x['rep'], x['kind'], x['a'], x['b'], x['type'], x['n_bridge_classes'],
                                                                                x['bridge_seed'], x['bridge_seed_islands'], x['bridge_held_end'],
                                                                                'y' if x['bridge_alive_end'] else 'n', x['mediations'], x['held_a'], x['held_b'],
                                                                                'y' if x['sep_end'] else 'n'))
    P('')
    return res


if __name__ == '__main__':
    main()
