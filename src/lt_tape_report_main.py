"""Builds runs/lt-tape.md and runs/lt-tape.json (verdicts, tables) from runs/lt_tape/*.json.gz.  Run after the batches."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lt_tape_report as R
import lt_tape_static as ST
import lt_tape_games as G
import lt_tape_run as RUN

ROOT = os.path.dirname(HERE)
OUT = R.OUT
fmt = R.fmt; stat = R.stat; cn = R.cn


def jload(p):
    with open(p) as f: return json.load(f)


def ratio_boot(num, den, B=4000, seed=7):
    """Run-paired bootstrap of mean(num)/mean(den)."""
    num = np.asarray(num, float); den = np.asarray(den, float)
    ok = ~(np.isnan(num) | np.isnan(den))
    num, den = num[ok], den[ok]
    if len(num) == 0 or den.mean() == 0: return (float('nan'),) * 3
    idx = np.random.default_rng(seed).integers(len(num), size=(B, len(num)))
    r = num[idx].mean(1) / np.maximum(den[idx].mean(1), 1e-12)
    return float(num.mean() / den.mean()), float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5))


def route_share(name, route, g='2000'):
    if route == 'check': return R.rv(name, 'fam1_check', g) + R.rv(name, 'fam1_pcr', g)
    if route == 'enum': return R.rv(name, 'fam1_enum', g)
    if route == 'search_ee': return R.rv(name, 'fam1_prover', g)
    if route == 'search_insp': return R.rv(name, 'fam0_prover', g) + R.rv(name, 'fam0_rim', g)
    raise KeyError(route)


def main():
    V = {}            # verdicts
    J = {}            # json payload
    md = []
    P = md.append
    S = ST.static_checks(); J['static'] = S
    snd = jload(os.path.join(OUT, 'soundness.json')) if os.path.exists(os.path.join(OUT, 'soundness.json')) else None
    J['soundness'] = snd

    P('# A private random tape in the realizable language (run report, 2026-10-24)\n')
    P('Spec `specs/2026-10-24-realizable-randomizer.md`; hand table `notes/lt-tape.md` §1; choices and deviations §2; predictions '
      '`predictions/2026-10-24-realizable-randomizer.md`. Objects: **STATIC** = exact tables (rational over tapes); **LOTTERY** = the ε = 0 '
      'seed lottery at N = 100 (per role in inspection), I = 64 islands, mN = 1, w = 0.3, generation 2,000 unless stated, island '
      'means then run means with run-clustered 95% bootstrap intervals over 40 runs; **CHAIN** = the ε → 0 diagnostic (monomorphic '
      'states); nothing here is π unless labelled CHAIN. K₀ = 10⁴ steps, c₀ = 1.2·10⁻⁵ per step (a forfeit by fuel exhaustion costs 0.12).\n')

    # ---------------------------------------------------------------- P1
    P('## Soundness and statics (STATIC; prediction 1)\n')
    ok_snd = None
    if snd:
        rows = []
        for k in ('insp_full', 'insp_prand', 'rps_full', 'rps_prand'):
            if k in snd:
                s = snd[k]
                rows.append([k, s['queries'], s['found'], s['boxes'], s['sequents'], s['false'], s['skipped'], s['play_checked'], s['play_disagree']])
        P(R.md_table(['catalogue (K0)', 'prove queries', 'derived', 'boxes audited', 'sequents audited', 'false', 'skipped', 'derived atoms replayed', 'play disagrees'], rows))
        ad = snd['adaptive_and_certificates']
        P('Adaptive and nested cases (%d queries, %d derived, %d sequents): false %d, padded-space reference agrees on %d of %d (the branching engine '
          'equals the full enumeration of every invocation\'s m digits). Honest certificates accepted: %d of %d; over-claims rejected: %d of %d; '
          'adversarial certificates rejected: %d of %d (%s).\n' % (
              ad['adaptive']['queries'], ad['adaptive']['found'], ad['adaptive']['sequents'], ad['adaptive']['false'],
              ad['adaptive']['padded_ok'], ad['adaptive']['padded_ref'],
              sum(ad['certs_honest_accepted'].values()), len(ad['certs_honest_accepted']),
              sum(ad['certs_overclaim_rejected'].values()), len(ad['certs_overclaim_rejected']),
              sum(ad['attacks_rejected'].values()), len(ad['attacks_rejected']), ', '.join(sorted(ad['attacks_rejected']))))
        dis = []
        for k in ('insp_full', 'insp_prand', 'rps_full', 'rps_prand'):
            if k in snd and snd[k]['play_disagree']:
                dis += ['%s: %s' % (k, e) for e in snd[k]['play_disagree_examples']]
        if dis: P('Play-vs-atom disagreements (a derived atom whose real play at K = 10⁶ is not the action with probability 1): ' + '; '.join(dis) + '\n')
        nfalse = sum(snd[k]['false'] for k in ('insp_full', 'insp_prand', 'rps_full', 'rps_prand') if k in snd) + ad['adaptive']['false']
        ok_snd = (nfalse == 0 and all(ad['attacks_rejected'].values()) and all(ad['certs_honest_accepted'].values())
                  and ad['adaptive']['padded_ok'] == ad['adaptive']['padded_ref'])
    P('Hash fixtures and mixers (exact): `SIM100` earns **%s** against every `H{j}` (all four defaults; `SIM20R` cannot afford the hash: %s), exactly **%.1f** against `U`; '
      'against the six biased mixers `B(a₁,a₂)` it earns %s (the bias; the best response is %s); `PRR` earns %s against them and %.1f against `U`; `CRR` earns '
      '%s against the carriers and %s against the plain mixers.\n' % (
          sorted(set(round(v, 9) for v in S['sim100_vs_hash'].values())), S['sim20_vs_hash'], S['U_row_max_abs'],
          sorted(set(round(v, 6) for v in S['sim100_vs_B'].values())), sorted(set(round(v, 6) for v in S['best_response_to_B'].values())),
          sorted(set(round(v, 6) for v in S['PRR_vs_B'].values())), S['PRR_vs_U'],
          sorted(set(round(v, 6) for v in S['CRR_vs_CB'].values())), sorted(set(round(v, 6) for v in S['CRR_vs_B'].values()))))
    b_ok = all(abs(v - 1) < 1e-9 for v in S['sim100_vs_hash'].values()) and all(abs(v) < 1e-9 for v in S['sim100_vs_U'].values()) and S['U_row_max_abs'] < 1e-12
    c_ok = all(abs(v - 1 / 3) < 1e-9 for v in S['sim100_vs_B'].values())
    V['P1'] = ('held' if (ok_snd and b_ok and c_ok) else ('failed' if ok_snd is False else 'partial'),
               'soundness %s; hash fixtures %s; bias %s (parenthesis "half the best response" withdrawn: notes §2.5)' % (ok_snd, b_ok, c_ok))

    # ---------------------------------------------------------------- route table (STATIC)
    P('## The two routes, step by step (STATIC; predictions 5 and 6, S1–S3)\n')
    rows = []
    for k, v in S['route_table'].items():
        rows.append([k, '%.0f' % v['PR'], '%.0f' % v['CR'], '%.0f' % v['PR_plain'], '%.2f' % (v['PR'] / v['CR'])])
    P(R.md_table(['committed inspector', 'PR (enumeration) on the carrier', 'CR (check) on the carrier', 'PR on the plain mixer', 'enumeration / check'], rows))
    P('`RI` against `C0` costs %g steps (W = %d); `CR` against a plain mixer costs %g steps and plays K. The responsive inspector\'s refutations cost '
      'W = %s (minimum %s; the success is 8). The hand table matches the code on every entry listed in `tests/test_lt_tape.py` (S1).\n' % (
          S['steps_RI_vs_C0'], S['RI_W']['C0'][0], S['CR_on_plain_steps'],
          ', '.join('%s %d' % (k, w[0]) for k, w in sorted(S['RI_W'].items(), key=lambda kv: kv[1][0])[:8]) + ', ...', S['RI_refuted_W_min']))
    V['S2'] = ('held' if all(v['CR'] < v['PR'] for v in S['route_table'].values()) and S['CR_on_plain_steps'] == 4 else 'failed', 'check < enumeration on every carrier; CR on a plain mixer 4 steps')
    V['S3'] = ('held' if S['RI_refuted_W_min'] is not None and S['RI_refuted_W_min'] > 8 else 'failed', 'min refutation W = %s' % S['RI_refuted_W_min'])

    # ---------------------------------------------------------------- RPS lottery
    P('## RPS (LOTTERY; N = 100, I = 64, 40 runs, generation 2,000)\n')
    rps_keys = ['sh_U', 'tape_mixers', 'fam_sim', 'fam_prover', 'forfeit', 'mix', 'e_prog', 'e_indiv', 'steps']
    rps_lab = ['U share', 'tape mixers', 'simulators', 'PB share', 'forfeited plays', 'individual mixing', 'e_prog (net)', 'e_indiv (net)', 'steps/encounter']
    P(R.lottery_rows('rps', ['full', 'noprover', 'notape', 'prand'], rps_keys, rps_lab))
    P('Renormalized no-tape arm (disabled templates removed):\n')
    P(R.lottery_rows('rps', ['notape'], rps_keys, rps_lab, renorm=True))
    P('Same cells at generation 4,000:\n')
    P(R.lottery_rows('rps', ['full', 'noprover', 'notape', 'prand'], rps_keys, rps_lab, g='4000'))

    # ---------------------------------------------------------------- inspection lottery
    P('## Inspection (LOTTERY; N = 100 per role, I = 64, 40 runs, generation 2,000)\n')
    ik = ['u0g', 'u1g', 'isl_efficient', 'isl_commit_comply', 'p_insp', 'q_cheat', 'fam0_prover', 'fam0_rim', 'fam0_sim', 'fam0_carrier', 'sh1_C0', 'fam1_enum', 'fam1_check', 'fam1_pcr']
    il = ['inspector payoff', 'inspectee payoff', 'efficient islands', 'committed+compliant', 'P(inspect)', 'P(cheat)', 'RI share', 'RIM share', 'SI share', 'carrier share', 'C0 share', 'PR share', 'CR share', 'PCR3 share']
    P(R.lottery_rows('insp', ['full', 'noprover', 'notape', 'prand', 'insp_only', 'ee_only'], ik, il))
    P('Renormalized arms (disabled templates removed, prior renormalized; co-primary where the default shifts a founder share by more than 0.05):\n')
    P(R.lottery_rows('insp', ['noprover', 'notape', 'insp_only', 'ee_only'], ik, il, renorm=True))
    P('Generation 4,000:\n')
    P(R.lottery_rows('insp', ['full', 'noprover', 'notape', 'prand', 'insp_only', 'ee_only'], ik, il, g='4000'))

    # ---------------------------------------------------------------- panels
    P('## Panels (LOTTERY)\n')
    for game, keys, labs, tag in (('insp', ['u0g', 'u1g', 'isl_efficient', 'fam0_prover', 'fam0_rim', 'fam0_sim', 'forfeit0', 'forfeit1'],
                                   ['inspector payoff', 'inspectee payoff', 'efficient islands', 'RI', 'RIM', 'SI', 'inspector forfeits', 'inspectee forfeits'], 'inspection'),
                                  ('rps', ['sh_U', 'tape_mixers', 'fam_sim', 'fam_prover', 'forfeit', 'e_prog', 'e_indiv'],
                                   ['U share', 'tape mixers', 'simulators', 'PB', 'forfeited plays', 'e_prog', 'e_indiv'], 'RPS')):
        rows = []
        for (K, c, lab) in ((1000, 0.12 / 1000, 'c = 0.12/K'), (2000, 0.12 / 2000, 'c = 0.12/K'), (5000, 0.12 / 5000, 'c = 0.12/K'),
                            (5000, 'c0', 'c = c0 fixed'), (5000, '0', 'free'), (RUN.K0, 'c0', 'c = c0'), (RUN.K0, '0', 'free'),
                            (20000, 'c0', 'c = c0 fixed'), (20000, '0', 'free')):
            cs = c if isinstance(c, str) else '%g' % c
            n = cn(game, 'full', cs, 'primary', K=(None if K == RUN.K0 else K))
            if R.load(n) is None: continue
            rows.append(['%d' % K, lab] + [fmt(stat(n, k)) for k in keys])
        P('**Fuel cap and price, %s full arm:**\n' % tag)
        P(R.md_table(['K', 'price'] + labs, rows))
    P('**Size check (400, 16), 20 runs; sampled encounters (10 runs); m = 4:**\n')
    rows = []
    for lab, n in (('size (400,16) free', cn('insp', 'full', '0', 'size')), ('size (400,16) c0', cn('insp', 'full', 'c0', 'size')),
                   ('sampled free (10 runs)', cn('insp', 'full', '0', 'primary', sampled=True)), ('sampled c0 (10 runs)', cn('insp', 'full', 'c0', 'primary', sampled=True)),
                   ('m = 4 free', cn('insp', 'full', '0', 'primary', m=4)), ('m = 4 c0', cn('insp', 'full', 'c0', 'primary', m=4)),
                   ('primary free (reference)', cn('insp', 'full', '0')), ('primary c0 (reference)', cn('insp', 'full', 'c0'))):
        if R.load(n) is None: continue
        rows.append([lab] + [fmt(stat(n, k)) for k in ('u0g', 'u1g', 'isl_efficient', 'isl_commit_comply', 'fam0_prover', 'fam0_rim', 'fam0_sim')])
    P(R.md_table(['cell', 'inspector payoff', 'inspectee payoff', 'efficient', 'committed+compliant', 'RI', 'RIM', 'SI'], rows))
    rows = []
    for lab, n in (('RPS size (400,16) free', cn('rps', 'full', '0', 'size')), ('RPS size (400,16) c0', cn('rps', 'full', 'c0', 'size'))):
        if R.load(n) is None: continue
        rows.append([lab] + [fmt(stat(n, k)) for k in ('sh_U', 'tape_mixers', 'fam_sim', 'forfeit', 'e_prog', 'e_indiv')])
    if rows: P(R.md_table(['cell', 'U share', 'tape mixers', 'simulators', 'forfeits', 'e_prog', 'e_indiv'], rows))

    # ---------------------------------------------------------------- chain (if present)
    chain_files = sorted(f for f in os.listdir(OUT) if f.startswith('chain_') and f.endswith('.json'))
    if chain_files:
        P('## CHAIN (ε → 0 diagnostic, monomorphic states; not the object of the lottery claims)\n')
        rows = []
        for f in chain_files:
            d = jload(os.path.join(OUT, f))
            if d['game'] == 'insp':
                rows.append([f[6:-5], '%.3f' % d['u0g'], '%.3f' % d['u1g'], '%.3f' % d['efficient'], '%.3f' % d['p_insp'], '%.3f' % d['q_cheat'], str(d['top_states'][:3])])
            else:
                rows.append([f[6:-5], 'pi(U) %.3f (prior %.3f)' % (d['pi_U'], d['prior_U']), 'e_indiv %.3f' % d['e_indiv'], 'self-forfeit %.3f' % d['forfeit_self'],
                             'mix %.3f' % d['mix_self'], '', str(d['top_states'][:3])])
        P(R.md_table(['cell', 'a', 'b', 'c', 'd', 'e', 'top states'], rows))

    # ---------------------------------------------------------------- verdicts
    P('## Verdicts\n')
    # P2
    n_rf = cn('rps', 'full', 'c0'); n_rp = cn('rps', 'prand', 'c0')
    u_share = stat(n_rf, 'sh_U'); fo = stat(n_rf, 'forfeit'); tm = stat(n_rf, 'tape_mixers')
    eind = stat(n_rp, 'e_indiv'); eprog = stat(n_rp, 'e_prog')
    a_ok = u_share and u_share[0] >= 0.6 and fo[0] < 0.1
    a_bad = tm and tm[0] < 0.3
    b_ok = eind and eind[0] >= 0.3
    b_bad = eind and eind[0] <= 0.1
    V['P2'] = ('held' if (a_ok and b_ok) else ('failed' if (a_bad or b_bad) else 'partial'),
               'U share %s, tape mixers %s, forfeits %s (full, c0); pseudo-random-only e_indiv %s, e_prog %s' % (fmt(u_share), fmt(tm), fmt(fo), fmt(eind), fmt(eprog)))
    V['P2_gpt'] = ('held' if (eind and eprog and eind[0] >= 0.3 and eprog[0] <= 0.1) else 'failed', 'e_indiv %s, e_prog %s' % (fmt(eind), fmt(eprog)))
    # P3
    n3 = cn('insp', 'full', '0')
    eff = stat(n3, 'isl_efficient')
    isl_eff = R.island_vals(n3, 'isl_efficient'); ri = [np.array(a) + np.array(b) for a, b in zip(R.island_vals(n3, 'sh0_RI'), R.island_vals(n3, 'sh0_RIM'))]
    c0s = R.island_vals(n3, 'sh1_C0')
    fr_ri = []; fr_c = []
    for e, r_, c_ in zip(isl_eff, ri, c0s):
        m_ = e > 0.5
        if m_.sum() > 0:
            fr_ri.append(float((r_[m_] > 0.5).mean())); fr_c.append(float((c_[m_] > 0.5).mean()))
    b3 = (np.mean(fr_ri) >= 0.5 and np.mean(fr_c) >= 0.5) if fr_ri else False
    sim_eff = []
    for e, s_ in zip(isl_eff, R.island_vals(n3, 'fam0_sim')):
        m_ = e > 0.5
        if m_.sum() > 0: sim_eff.append(float((s_[m_] > 0.5).mean()))
    V['P3'] = (('held' if b3 else 'partial') if eff[0] >= 0.3 else ('failed' if eff[0] < 0.1 else 'partial'),
               'efficient islands %s (free, full); on efficient islands RI+RIM majority of inspectors on %.2f of them, C0 majority on %.2f; simulating inspectors majority on %.2f' % (
                   fmt(eff), np.mean(fr_ri) if fr_ri else float('nan'), np.mean(fr_c) if fr_c else float('nan'), np.mean(sim_eff) if sim_eff else float('nan')))
    # P4
    n4 = cn('insp', 'ee_only', '0')
    cc = stat(n4, 'isl_commit_comply')
    cm = R.rv(n4, 'committed_mass'); cmc = R.rv(n4, 'committed_carrier_mass')
    car_share = float(np.nanmean(cmc) / max(np.nanmean(cm), 1e-12)) if len(cm) else float('nan')
    b4 = car_share > 0.5
    V['P4'] = (('held' if b4 else 'partial') if cc[0] >= 0.5 else ('failed' if cc[0] < 0.2 else 'partial'),
               'committed+compliant islands %s (inspectee-only reading, free); carriers hold %.2f of the committed inspector mass; check-route share among inspectees %s' % (
                   fmt(cc), car_share, fmt(boot_sum(n4, ('fam1_check', 'fam1_pcr')))))
    # P5
    n5 = cn('insp', 'full', '0')
    chk_steps = R.rv(n5, 'rs1_check') / np.maximum(R.rv(n5, 'ru1_check'), 1e-12)
    srch_steps = R.rv(n5, 'rs0_search') / np.maximum(R.rv(n5, 'ru0_search'), 1e-12)
    used_c = R.rv(n5, 'ru1_check'); used_s = R.rv(n5, 'ru0_search')
    lot_ratio = float(np.nanmean(np.where(used_c > 1e-9, chk_steps, np.nan)) / np.nanmean(np.where(used_s > 1e-9, srch_steps, np.nan))) if (used_c > 1e-9).any() and (used_s > 1e-9).any() else float('nan')
    st_ratio = S['measured_static_ratio']
    st_ok = 1.125 <= st_ratio <= 4.5
    lot_ok = (1.125 <= lot_ratio <= 4.5) if not np.isnan(lot_ratio) else None
    V['P5'] = (('held' if (st_ok and lot_ok) else ('partial' if st_ok else 'failed')),
               'static check/proof = %.3f (hand 2.25); lottery-weighted (primary, free, generation 2,000) = %s' % (st_ratio, 'n/a (a route unused)' if np.isnan(lot_ratio) else '%.2f' % lot_ratio))
    # P6
    routes = {'search_insp': ('RI', 'RIM'), 'search_ee': ('PE', 'PEC'), 'enum': ('PR2', 'PR3', 'PR4'), 'check': ('CR2', 'CR3', 'CR4', 'PCR3')}
    ins_t, ee_t = G.catalogue_insp(RUN.K0)
    sz0 = {t.name: G.size(t.build('tape')) if hasattr(G, 'size') else 0 for t in ins_t}
    cost = {}
    for rname, members in routes.items():
        cs_ = [S['mean_steps_vs_prior'][m_] for m_ in members]
        cost[rname] = float(np.mean(cs_))
    nf = cn('insp', 'full', '0'); np_ = cn('insp', 'full', 'c0')
    surv = {}
    for rname in routes:
        a = route_share(np_, rname); b = route_share(nf, rname)
        surv[rname] = (float(np.nanmean(b)), float(np.nanmean(a)), ratio_boot(a, b))
    avail = [r_ for r_ in routes if surv[r_][0] > 0.005]
    if len(avail) >= 2:
        cheap = min(avail, key=lambda r_: cost[r_]); dear = max(avail, key=lambda r_: cost[r_])
        ac, bc = route_share(np_, cheap), route_share(nf, cheap)
        ad_, bd_ = route_share(np_, dear), route_share(nf, dear)
        n = min(len(ac), len(ad_))
        diff = []
        rng = np.random.default_rng(11)
        idx = rng.integers(n, size=(4000, n))
        rc = ac[idx].mean(1) / np.maximum(bc[idx].mean(1), 1e-12); rd = ad_[idx].mean(1) / np.maximum(bd_[idx].mean(1), 1e-12)
        d = rc - rd
        lo, hi = np.percentile(d, 2.5), np.percentile(d, 97.5)
        point = (ac.mean() / max(bc.mean(), 1e-12)) - (ad_.mean() / max(bd_.mean(), 1e-12))
        verdict6 = 'held' if lo > 0 else ('failed' if hi < 0 else 'partial')
        V['P6'] = (verdict6, 'cheapest route %s (mean steps %.1f) survival %.2f vs dearest %s (%.1f) survival %.2f; difference %.2f [%.2f, %.2f]' % (
            cheap, cost[cheap], ac.mean() / max(bc.mean(), 1e-12), dear, cost[dear], ad_.mean() / max(bd_.mean(), 1e-12), point, lo, hi))
    else:
        V['P6'] = ('partial', 'fewer than two routes held a share above 0.005 in the free cell: %s' % {k: round(v[0], 4) for k, v in surv.items()})
    J['route_survival'] = {k: dict(share_free=v[0], share_c0=v[1], ratio=v[2]) for k, v in surv.items()}
    J['route_cost'] = cost
    # S4
    dpe = R.paired(cn('insp', 'full', 'c0'), cn('insp', 'full', '0'), 'isl_efficient')
    V['S4'] = ('held' if dpe and abs(dpe[0]) < 0.1 else 'failed', 'efficient islands c0 - free = %s' % fmt(dpe))
    # S5
    f_ = R.rv(cn('rps', 'full', '0'), 'fam_sim') + R.rv(cn('rps', 'full', '0'), 'fam_prover')
    p_ = R.rv(cn('rps', 'prand', '0'), 'fam_sim') + R.rv(cn('rps', 'prand', '0'), 'fam_prover')
    V['S5'] = ('held' if len(f_) and p_.mean() > f_.mean() else 'failed', 'sims+PB share, prand %s vs full %s (free price)' % (fmt(R.boot(p_)), fmt(R.boot(f_))))
    # S6
    pm = G.prior_masses(np.array([G.size(t.build('tape')) for t in ins_t]))
    nm = [t.name for t in ins_t]
    committed = [i for i, t in enumerate(ins_t) if t.meta.get('p', 0) > 0.25]
    car = [i for i in committed if nm[i].startswith('CARR')]
    prior_share = float(pm[car].sum() / pm[committed].sum())
    V['S6'] = ('held' if car_share > prior_share else 'failed', 'carrier share of committed mass %.2f vs prior share among committed templates %.2f' % (car_share, prior_share))

    vt = []
    for k in ('P1', 'P2', 'P2_gpt', 'P3', 'P4', 'P5', 'P6', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6'):
        if k in V: vt.append([k, V[k][0], V[k][1]])
    P(R.md_table(['#', 'verdict', 'numbers'], vt))
    J['verdicts'] = V

    rd = os.path.join(OUT, 'reading.md')
    if os.path.exists(rd):
        P('## Reading\n'); P(open(rd).read())
    with open(os.path.join(ROOT, 'runs', 'lt-tape.md'), 'w') as f: f.write('\n'.join(md))
    with open(os.path.join(ROOT, 'runs', 'lt-tape.json'), 'w') as f: json.dump(J, f, indent=1, default=str)
    print('\n'.join(md)[-6000:])


def boot_sum(name, keys):
    v = sum(R.rv(name, k) for k in keys)
    return R.boot(v)


if __name__ == '__main__':
    main()
