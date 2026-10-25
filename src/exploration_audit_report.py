"""Assemble runs/exploration-audit.json and runs/exploration-audit.md from the per-cell stage records in runs/exploration_audit/.

    python3 src/exploration_audit_report.py

Each row is one audited statistic of one inventory group: the published value (from the stored published run record or RESULTS),
the value reproduced at stage (a), and the later stages, with the difference on the scale fixed in
predictions/2026-10-24-exploration-audit.md (absolute for probabilities and shares; payoffs divided by the payoff range).
A missing record is reported as unresolved.
"""
import json, os, sys, glob, math
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
D = os.path.join(ROOT, 'runs', 'exploration_audit')
R = os.path.join(ROOT, 'runs')


def jl(path):
    p = os.path.join(ROOT, path)
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return None


def rec(cell):
    p = os.path.join(D, cell + '.json')
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return {}


def get(cell, stage, *path):
    r = rec(cell).get(stage)
    for k in path:
        if r is None:
            return None
        try:
            r = r[k]
        except (KeyError, IndexError, TypeError):
            return None
    return r


ROWS = []


def add(gid, label, stat, scale, published, stages, note='', kind='prob', repro=None):
    """stages: ordered list of (stage label, value); repro: index of the stage that is the reproduction (a), default 0."""
    ROWS.append(dict(group=gid, cell=label, stat=stat, scale=scale, published=published, stages=stages, note=note, kind=kind, repro=0 if repro is None else repro))


# ------------------------------------------------------------------------------------------------ controls
def rows_controls():
    c = 'm2_insp_exact_c0_N10000'
    rng = 4.0
    pub = dict(c1500=-0.009, c4000=-0.31, c8000=-0.47, full=-0.471)
    add('control+', 'inspection exact c=0 N=1e4 (24,649 states)', 'mean inspector payoff', rng, -0.471,
        [('a: cap 1,500 (published -0.009)', get(c, 'cap1500_published', 'stat', 'u0g')), ('b: cap 4,000 (published -0.31)', get(c, 'cap4000_published', 'stat', 'u0g')),
         ('b: cap 8,000 (published -0.47)', get(c, 'cap8000_published', 'stat', 'u0g')), ('b: cap 15,000 (10x)', get(c, 'cap15000_published', 'stat', 'u0g')),
         ('c: whole space', get(c, 'c_full', 'stat', 'u0g'))],
        note='positive control: capped -0.0093 reproduces the published -0.009 and the whole space -0.4707 the published -0.471; the 4,000-state point does not reproduce (-0.4708 here against -0.31)', kind='payoff', repro=0)
    for N in (100, 10000):
        c = 'm2_insp_blind_c0_N%d' % N
        add('control-', 'inspection blind c=0 N=%d (289 states, complete)' % N, 'mean inspector payoff', rng, -0.93 if N == 100 else -0.92,
            [('a: cap 1,500', get(c, 'cap1500_published', 'stat', 'u0g')), ('c: whole space', get(c, 'c_full', 'stat', 'u0g'))], kind='payoff')
    c = 'm2_insp_sample_c0_N10000'
    add('control-caps', 'inspection sample c=0 N=1e4 (6,889 states): caps and seeds against the whole space', 'mean inspector payoff', rng, get(c, 'c_full', 'stat', 'u0g'),
        [('cap 500', get(c, 'cap500_published', 'stat', 'u0g')), ('cap 1,500 published seeds', get(c, 'cap1500_published', 'stat', 'u0g')),
         ('cap 1,500 random seeds 1', get(c, 'cap1500_random100:1', 'stat', 'u0g')), ('cap 1,500 random seeds 2', get(c, 'cap1500_random100:2', 'stat', 'u0g')),
         ('cap 1,500 random seeds 3', get(c, 'cap1500_random100:3', 'stat', 'u0g')), ('cap 3,000', get(c, 'cap3000_published', 'stat', 'u0g')),
         ('whole space', get(c, 'c_full', 'stat', 'u0g'))], note='published value = the whole-space value here (RESULTS -0.64 / notes)', kind='payoff')
    for nm, cell in (('blind', 'solvercheck_insp_blind_c0_N10000'), ('sample', 'solvercheck_insp_sample_c0_N10000')):
        r = rec(cell).get('solver_check')
        if r:
            add('solver-check', 'jump-chain GTH vs dense generator solve: inspection %s c=0 N=1e4' % nm, 'TV distance', 1.0, 0.0,
                [('TV (full GTH, generator)', r['tv_full_vs_generator'])] + ([('TV (log GTH, jump GTH)', r['tv_full_vs_log_gth'])] if 'tv_full_vs_log_gth' in r else []))


# ------------------------------------------------------------------------------------------------ I-05, I-06 ultimatum
def rows_ult():
    for arm, gname, grp in (('mutual', 'ult', 'I-05'), ('onesided', 'ult', 'I-05'), ('mutual', 'ult_out', 'I-06')):
        c = 'ult_%s_%s_N100' % (gname, arm)
        pub = jl('runs/ult_%s_%s_N100_w0.1.json' % (gname, arm)) or {}
        for stat, key in (('rejection rate', 'reject'), ('proposer share', 'share_P'), ('responder share', 'share_R')):
            add(grp, 'ultimatum %s %s N=100' % (gname, arm), stat, 1.0, pub.get(key),
                [('a: reproduced', get(c, 'stage_a', key)), ('b: theta 1e-10, cap 200k', get(c, 'stage_b', key)), ('c: all pairs (%s)' % get(c, 'stage_c', 'n_pairs'), get(c, 'stage_c', key))])


# ------------------------------------------------------------------------------------------------ I-23 union
def rows_union():
    for N in (1000, 10000):
        c = 'union_quorum_c0.5_N%d' % N
        pub = (jl('runs/union/quorum_c0.5_N%d.json' % N) or {})
        # the published summary lives in the analyse() output of the same file
        ps = None
        d = jl('runs/union/quorum_c0.5_N%d.json' % N)
        if d:
            ps = d.get('summary') or d.get('P_summary')
        for key in ('fair', 'intermediate', 'zero wage'):
            add('I-23', 'union quorum c=0.5 N=%d' % N, key, 1.0, (ps or {}).get(key),
                [('a: theta 1e-9', get(c, 'theta1e-09_core2500', 'summary', key)), ('b: theta 1e-10', get(c, 'theta1e-10_core2500', 'summary', key))],
                note='theta 1e-11 reached 42,007 ring states with relative cut 0.175 after 81 min in round 1 and was stopped (unconverged); theta 1e-12 not run')


# ------------------------------------------------------------------------------------------------ I-24 enforcement part C
def rows_enf():
    for cellname, pubf, label in (('enfC_RR_pool0_c0.5_N1000_whack', 'partC_RR_pool0_c0.5_N1000_whack', 'RR pool0 N=1e3'),
                                  ('enfC_RR_pool0_c0.5_N10000_whack', 'partC_RR_pool0_c0.5_N10000_whack', 'RR pool0 N=1e4'),
                                  ('enfC_RC_pool1_c0.5_N1000_whack', 'partC_RC_pool1_c0.5_N1000_whack', 'RC pool1 N=1e3')):
        pub = (jl('runs/enforcement/%s.json' % pubf) or {}).get('summary', {})
        for key in ('fair', 'intermediate', 'zero wage'):
            add('I-24C', 'enforcement %s' % label, key, 1.0, pub.get(key),
                [('a: theta 1e-11', get(cellname, 'theta1e-11', 'summary', key)), ('b: theta 1e-13', get(cellname, 'theta1e-13', 'summary', key))])
    c = 'enfC_CC_pool0_c0.5_N1000_whack'
    pub = (jl('runs/enforcement/partC_CC_pool0_c0.5_N1000_whack.json') or {}).get('summary', {})
    for key in ('fair', 'intermediate', 'zero wage'):
        add('I-24C', 'enforcement CC pool0 N=1e3', key, 1.0, pub.get(key), [('a: theta 1e-9', get(c, 'theta1e-09', 'summary', key))],
            note='theta 1e-11 reached 42,902 candidates in round 0 and was stopped (not comparable)')


# ------------------------------------------------------------------------------------------------ I-36 concessions
def rows_conc():
    c = 'conc_P01_CC_c0.5_N10000'
    pub = jl('runs/concessions/chain_P01_CC_c0.5_N10000.json') or {}
    cd = jl('runs/concessions/cut_diagnostic.json') or {}
    for key in ('fair', 'intermediate', 'zero wage'):
        add('I-36', 'concessions P01 N=1e4 (explored fair; cut-corrected fair 0.0020)', key, 1.0, (pub.get('summary') or {}).get(key),
            [('a: theta 1e-9 (rel_cut_change 0.094)', get(c, 'theta1e-09', 'summary', key)), ('b: theta 3e-10 (rel_cut_change 0.042)', get(c, 'theta3e-10', 'summary', key))],
            note='published cut-corrected fair: 0.0020; theta 1e-10 and 1e-11 never finished in the original run either')


# ------------------------------------------------------------------------------------------------ I-32 modal fixed-role dollar
def rows_mdfixed():
    for N in (100, 1000):
        c = 'mdfixed_modal_N%d' % N
        pub = (jl('runs/modal_dollar/fixed_modal_n7_N%d_th1e-12.json' % N) or {}).get('ordered_label_mass', {})
        stages_all = [('a: 8,000 states', 'cap8000_th1e-12'), ('b: 16,000 states', 'cap16000_th1e-12_lazy2')]
        for lab, key in (('1/2|1/2', ['1/2|1/2']), ('1/3-type (both orders)', ['1/3|2/3', '2/3|1/3']), ('endpoints (both orders)', ['1/6|5/6', '5/6|1/6']), ('ineff + clash', ['ineff', 'clash'])):
            pv = sum(pub.get(k, 0.0) for k in key) if pub else None
            sv = []
            for sl, sk in stages_all:
                lm = get(c, sk, 'label_mass')
                sv.append((sl, None if lm is None else sum(lm.get(k, 0.0) for k in key)))
            add('I-32', 'modal fixed-role dollar N=%d (space 42,025)' % N, lab, 1.0, pv, sv,
                note='cut 9.8e-4 -> 9.4e-5 (N=100), 5.2e-3 -> 1.0e-6 (N=1000); the whole 42,025-state space does not fit in memory (14 GB)')


# ------------------------------------------------------------------------------------------------ I-29 modal dollar paired chains
def rows_mdlimn():
    pubs = {('modal', 100): 0.986, ('modal', 1000): 0.894, ('modal', 30000): 0.653, ('weak', 100): 0.988, ('weak', 1000): 1.000, ('weak', 30000): 1.000}
    for arm in ('modal', 'weak'):
        for N in (100, 1000, 30000):
            c = 'mdlimn_%s_N%d' % (arm, N)
            r = rec(c)
            st = [(k, v.get('P_efficient')) for k, v in sorted(r.items())]
            if st:
                add('I-29', 'one-population dollar n=7 %s N=%d' % (arm, N), 'P(efficient)', 1.0, pubs[(arm, N)], st)
    for arm, name in (('weak', 'dollar-weak7'),):
        for N in (1000, 10000):
            c = 'sa_%s_N%d' % (name, N)
            add('I-29', 'one-population dollar n=7 weak N=%d (solver-audit pipeline)' % N, 'efficiency', 1.0, 1.0,
                [('d: closure-seeded, lumped', get(c, 'd_lumped', 'resolve_stat', 'eff')), ('e: twin-expanded', get(c, 'd_twins', 'resolve_stat', 'eff'))])


# ------------------------------------------------------------------------------------------------ I-42 one-population chicken
def rows_chk():
    pubs = {}
    for r in (jl('runs/fixed_role_chicken/onepop_chain.json') or []):
        if r['twins'] and abs(r['log10_theta'] + 14) < 1e-6:
            pubs[(r['game'], r['N'])] = r
    for game, N in (('chicken', 100), ('hd3', 1000), ('hd3', 10000), ('hd6', 1000)):
        c = 'chk_modal_%s_N%d' % (game, N)
        p = pubs.get((game, N))
        r = rec(c)
        stg = []
        ks = sorted(r, key=lambda k: (0 if k.startswith('cap3000') else 1, k))
        for k in ks:
            v = r[k]
            stg.append(('%s (%s states, %s candidates left)' % (k, v.get('n_states'), v.get('n_cand_left')), v.get('pay_per_player')))
        has_repro = bool(ks) and ks[0].startswith('cap3000')
        if stg or p:
            add('I-42', 'one-population modal %s N=%d' % (game, N), 'payoff per player', {'chicken': 12.0, 'hd3': 2.5, 'hd6': 4.0}[game],
                None if p is None else p['pay_per_player'], stg, kind='payoff',
                note='published: %s states, %s candidates left, log10 cut %s' % (None if p is None else p['n_states'], None if p is None else p['n_cand_left'], None if p is None else p['log10_cut']), repro=(0 if has_repro else -1))


# ------------------------------------------------------------------------------------------------ I-22 three-player dollar
def rows_d3():
    for N, th in ((100, 'theta1e-09'),):
        c = 'd3_weak_N%d' % N
        r = rec(c)
        pub = jl('runs/dollar3/weak_N%d.json' % N) or {}
        pm = pub.get('mass_by_coalition', {})
        keys = sorted(r)
        for coal in ('G', 'P12', 'X'):
            add('I-22', 'three-player dollar weak N=%d' % N, 'mass %s' % coal, 1.0, pm.get(coal),
                [('%s (states %s, rel_cut %.4f)' % (k, r[k]['states'], r[k]['rel_cut']), r[k]['mass_by_coalition'].get(coal)) for k in keys])
        add('I-22', 'three-player dollar weak N=%d' % N, 'efficiency', 1.0, pub.get('efficiency'),
            [('%s' % k, r[k]['efficiency']) for k in keys])
    c = 'd3_weak_N1000'
    r = rec(c)
    if r:
        pub = jl('runs/dollar3/weak_N1000.json') or {}
        pm = pub.get('mass_by_coalition', {})
        for coal in ('G', 'P12', 'X'):
            add('I-22', 'three-player dollar weak N=1000', 'mass %s' % coal, 1.0, pm.get(coal),
                [('%s (states %s, rel_cut %.4f)' % (k, r[k]['states'], r[k]['rel_cut']), r[k]['mass_by_coalition'].get(coal)) for k in sorted(r)])


# ------------------------------------------------------------------------------------------------ I-51 mixed2 capped cells
def _capkey(kv):
    import re
    m = re.match(r'(?:cap)?(\d+)', kv[0])
    return (0, int(m.group(1))) if m else (1, 0)


def rows_m2cap():
    rng = 4.0
    for cell, arm, pubf, rng_ in (('m2_insp_sr16_c0_N10000', 'insp sr16 c=0', 'chain_insp_sr16_c0', 4.0), ('m2_insp_sr4_c0_N10000', 'insp sr4 c=0', 'chain_insp_sr4_c0', 4.0),
                                  ('m2_end_matched_c0.01_N10000', 'Endgame matched c=0.01', 'chain_end_matched_c0.01', 6.0)):
        pub = (jl('runs/mixed2/%s.json' % pubf) or {}).get('cells', {}).get('10000', {}).get('stat', {}).get('u0g')
        r = rec(cell)
        add('I-51', '%s N=1e4' % arm, 'mean payoff (player 0)', rng_, pub,
            [(k, v['stat']['u0g']) for k, v in sorted(r.items(), key=_capkey) if isinstance(v, dict) and 'stat' in v], kind='payoff',
            note='frontier mass at the stages: ' + ', '.join('%s %.3f' % (k, v.get('frontier_mass', float('nan'))) for k, v in sorted(r.items(), key=_capkey) if isinstance(v, dict) and 'stat' in v))
    c = 'm2_insp_exact_c0.01_N100'
    pub = (jl('runs/mixed2/chain_insp_exact_c0.01.json') or {}).get('cells', {}).get('100', {}).get('stat', {}).get('u0g')
    r = rec(c)
    add('I-51', 'insp exact c=0.01 N=100 (27,889 states)', 'mean inspector payoff', rng, pub,
        [(k, v['stat']['u0g']) for k, v in sorted(r.items(), key=_capkey) if isinstance(v, dict) and 'stat' in v], kind='payoff')


# ------------------------------------------------------------------------------------------------ M-status cells (solver-audit pipeline, bounded)
SB_PUB = {('pd-kb4', 10000): 0.679, ('pd-kb4', 30000): 0.774, ('pd-kb8', 10000): 0.662, ('pd-kb8', 30000): 0.762,
          ('pd-modal8', 10000): 0.617, ('pd-modal8', 30000): 0.725, ('pd-modal6', 10000): 0.5869,
          ('pd-pr8-lazy-c0.01', 100000): 1.0}


def pub_pcc(name, N):
    """Published PD cooperation (pcc) of a priced / certificate / fringe cell from the stored run records."""
    try:
        if name.startswith('pd-pr') and '-c' in name:
            _, nn, pricing, cc = name.split('-')
            n, c = int(nn[2:]), float(cc[1:])
            for fn in (['priced_recheck.json'] if c == 0.001 else []) + ['priced_limN.json']:
                for r in (jl('runs/' + fn) or []):
                    if r.get('n') == n and r.get('pricing') == pricing and abs(r.get('c', -1) - c) < 1e-12 and r.get('N') == N and r.get('exp', 'exp1') == 'exp1':
                        return r['pcc']
        if name.startswith('pd-cert-'):
            _, _, pricing, nn, cc = name.split('-')
            for r in (jl('runs/cert_pricing.json') or []):
                if r.get('pricing') == pricing and r.get('n') == int(nn[1:]) and abs(r.get('c', -1) - float(cc[1:])) < 1e-12 and r.get('N') == N and r.get('theta', 1e-6) == 1e-6:
                    return r['pcc']
        if name.startswith('pd-fr-'):
            _, _, kind, nn, dd = name.split('-')
            for r in (jl('runs/drift_closure.json') or []):
                if r.get('kind') == kind and r.get('n') == int(nn[1:]) and abs(r.get('delta', -1) - float(dd[1:])) < 1e-12 and r.get('N') == N and r.get('theta', 1e-6) == 1e-6 and r.get('arm') in (kind, 'free'):
                    return r['pcc']
    except Exception:
        return None
    return None


def rows_sb():
    for f in sorted(glob.glob(os.path.join(D, 'sb_*.json')) + glob.glob(os.path.join(D, 'sa_pd-*.json'))):
        base = os.path.basename(f)[:-5]
        r = rec(base)
        for stage, v in sorted(r.items()):
            if not isinstance(v, dict) or 'rerun_stat' not in v:
                continue
            name, N = v['cell'], v['N']
            for stat in v['rerun_stat']:
                pub = SB_PUB.get((name, N))
                if pub is None:
                    pub = pub_pcc(name, N)
                add('M:' + name, '%s N=%d' % (name, N), stat, 1.0, pub,
                    [('a: published construction re-run', v['rerun_stat'][stat]), ('b/d: LogChain %s, %s states, log10 cut %s, %s candidates left' % (stage, v.get('resolve_n_states'), v.get('resolve_log10_cut'), v.get('resolve_n_cand_left')), v['resolve_stat'].get(stat))],
                    note='polymorphic mass %.2e; recurrent polymorphic states %s' % (v.get('resolve_mass_poly') or 0, v.get('resolve_n_recurrent_poly')))


# ------------------------------------------------------------------------------------------------ RPS
def rows_rps():
    for f in sorted(glob.glob(os.path.join(D, 'rps_*.json'))):
        base = os.path.basename(f)[:-5]
        r = rec(base)
        for stat in ('e_prog', 'e_act', 'mix_pop'):
            add('I-48', base, stat, 1.0, None, [(k, v.get(stat)) for k, v in sorted(r.items())])
    for f in sorted(glob.glob(os.path.join(D, 'rpsp_*.json'))):
        base = os.path.basename(f)[:-5]
        r = rec(base)
        for stat in ('e_prog', 'e_gross', 'mix_pop', 'poly_mass'):
            add('I-49', base, stat, 1.0, None, [(k, v.get(stat)) for k, v in sorted(r.items())])


def build():
    for fn in (rows_controls, rows_ult, rows_union, rows_enf, rows_conc, rows_mdfixed, rows_mdlimn, rows_chk, rows_d3, rows_m2cap, rows_sb, rows_rps):
        try:
            fn()
        except Exception as e:                       # a missing or malformed record must not hide the others
            ROWS.append(dict(group='error', cell=fn.__name__, stat=repr(e), scale=1.0, published=None, stages=[], note='', kind='', repro=0))
    return ROWS


def delta(row):
    pub = row['published']
    out = []
    for lab, v in row['stages']:
        out.append((lab, v, (None if v is None or pub is None else (v - pub) / row['scale'])))
    return out


def fmt(v):
    return 'n/a' if v is None else ('%.4g' % v)


def main():
    rows = build()
    js = []
    L = ['# Exploration-cap audit: per-cell table (generated by src/exploration_audit_report.py from runs/exploration_audit/*.json)', '',
         'Difference column: (stage value - published) divided by the scale (1 for probabilities and shares; the payoff range for payoffs).', '',
         '| group | cell | statistic | published | stage values; (difference) |', '|---|---|---|---|---|']
    moved = []
    for r in rows:
        ds = delta(r)
        cells = '; '.join('%s: %s%s' % (lab, fmt(v), '' if d is None else ' (%+.4f)' % d) for lab, v, d in ds)
        L.append('| %s | %s | %s | %s | %s |' % (r['group'], r['cell'], r['stat'], fmt(r['published']), cells))
        mx = max([abs(d) for lab, v, d in ds[r['repro'] + 1:] if d is not None] + [0.0])
        mxa = max([abs(d) for lab, v, d in ds if d is not None] + [0.0])
        js.append(dict(group=r['group'], cell=r['cell'], stat=r['stat'], scale=r['scale'], published=r['published'], note=r['note'],
                       stages=[dict(stage=lab, value=v, diff_scaled=d) for lab, v, d in ds], max_abs_diff_after_repro=mx, max_abs_diff_any=mxa))
        if mxa > 0.02 and not r['group'].startswith('control'):
            moved.append((r['group'], r['cell'], r['stat'], mxa))
    L += ['', '## Cells whose scaled difference from the published value exceeds 0.02 at some stage', '']
    for g, c, s, m in moved:
        L.append('- %s: %s, %s: %.4f' % (g, c, s, m))
    # prediction 2 bookkeeping: one-population DSL cells (PD, dollar, modal arm) re-solved, within 0.02 of the published value
    cellmax = {}
    for r, j in zip(rows, js):
        if r['group'].startswith('control') or r['group'] in ('solver-check', 'error'):
            continue
        ds = delta(r)
        later = [(lab, v, d) for lab, v, d in ds[r['repro'] + 1:] if v is not None]
        if not later:
            continue
        base = r['published']
        if base is None:
            base = ds[0][1]
            if base is None:
                continue
            vals = [abs(v - base) / r['scale'] for lab, v, d in later]
        else:
            vals = [abs(d) for lab, v, d in later if d is not None]
        key = (r['group'], r['cell'])
        cellmax[key] = max(cellmax.get(key, 0.0), max(vals) if vals else 0.0)
    ONE = lambda g: g.startswith('M:') or g in ('I-29', 'I-26', 'I-42')
    one = {k: v for k, v in cellmax.items() if ONE(k[0])}
    multi = {k: v for k, v in cellmax.items() if not ONE(k[0])}
    L += ['', '## Prediction 2 bookkeeping (cells with a stage after the reproduction; largest scaled difference over statistics and stages)', '']
    L.append('- one-population DSL cells re-solved: %d, within 0.02: %d' % (len(one), sum(1 for v in one.values() if v <= 0.02)))
    L.append('- multi-role / fixed-role cells re-solved: %d, within 0.02: %d' % (len(multi), sum(1 for v in multi.values() if v <= 0.02)))
    for k, v in sorted(cellmax.items(), key=lambda kv: -kv[1])[:12]:
        L.append('  - %s: %.4f' % (k, v))
    out_md = os.path.join(R, 'exploration-audit-table.md')
    with open(out_md, 'w') as f:
        f.write('\n'.join(L) + '\n')
    with open(os.path.join(R, 'exploration-audit.json'), 'w') as f:
        json.dump(dict(rows=js, n_rows=len(js), moved_over_0_02=moved), f, indent=1)
    print('\n'.join(L))


if __name__ == '__main__':
    main()
