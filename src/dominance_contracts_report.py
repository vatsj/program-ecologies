"""Report for the dominance-contracts experiment: runs/dominance-contracts.md and runs/dominance-contracts.json from the
per-cell summaries in runs/dominance_contracts/ (and runs/dominance_contracts/verdicts.md, appended verbatim)."""
import json, os, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dominance_contracts_run as DR

ROOT = DR.ROOT
OUT = DR.OUT
SSDIR = os.path.join(ROOT, 'runs', 'stable_sets')
CATS = ('member', 'unequal', 'wasteful', 'grand', 'disagreement', 'member-mixed', 'other-mixed')
GEN_JUMP = {'member': {'unequal': 1.0},
            'unequal': {'member': 1 / 3, 'unequal': 1 / 3, 'wasteful': 1 / 3},
            'wasteful': {'member': 1 / 4, 'unequal': 1 / 2, 'wasteful': 1 / 4},
            'disagreement': {'member': 3 / 18, 'unequal': 6 / 18, 'wasteful': 9 / 18},
            'grand': {'member': 1.0}}


def load(name):
    f = os.path.join(OUT, name + '.json')
    return json.load(open(f)) if os.path.exists(f) else None


def boot(vals, B=2000, seed=0):
    v = np.asarray(vals, float)
    if len(v) == 0:
        return (float('nan'),) * 3
    rng = np.random.default_rng(seed)
    bs = rng.choice(v, (B, len(v))).mean(1)
    return float(v.mean()), float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975))


def fmt(t, d=3):
    return ('%.' + str(d) + 'f [%.' + str(d) + 'f, %.' + str(d) + 'f]') % t


def horizon_row(c, h):
    runs = [r for r in c['runs'] if str(h) in r['horizons']]
    if not runs:
        return None
    hz = [r['horizons'][str(h)] for r in runs]
    row = dict(n=len(runs))
    row['occupancy'] = boot([x['occupancy'] for x in hz])
    for k in CATS:
        row[k] = float(np.mean([x['cats'].get(k, 0.0) for x in hz]))
    row['support_strict'] = float(np.mean([x['support_strict'] for x in hz]))
    row['support_ss'] = float(np.mean([x['support_ss'] for x in hz]))
    row['coverage'] = float(np.mean([x['coverage'] for x in hz]))
    row['consensus'] = float(np.mean([x['consensus'] for x in hz]))
    row['efficiency'] = float(np.mean([x['efficiency'] for x in hz]))
    row['window_occupancy'] = float(np.mean([x['window_occupancy'] for x in hz]))
    if 'r_mean' in hz[0]:
        row['r_mean'] = float(np.mean([x['r_mean'] for x in hz]))
    return row


_MODAL = {}


def modal_occ(name, nruns, h):
    """fraction of islands whose modal play (argmax of the encounter distribution) is a V* member, from the per-run
    arrays (the RS operationalization's wording); also the mean max-mass of member islands."""
    import stable_sets as SS
    key = (name, h)
    if key in _MODAL:
        return _MODAL[key]
    T = DR.tables(); V = sorted(SS.symmetric_set(T.R, 6))
    p = DR.CELLS[name]; hs = [x for x in DR.HS if x <= p['H']]
    if h not in hs:
        return None
    hi = hs.index(h)
    vals = []
    for r in range(nruns):
        f = os.path.join(OUT, name, 'r%d.npz' % r)
        if not os.path.exists(f):
            continue
        d = np.load(f)['dist'][hi]
        am = d.argmax(1)
        vals.append(float(np.isin(am, V).mean()))
    _MODAL[key] = boot(vals) if vals else None
    return _MODAL[key]


def paired(c, b, h, key='occupancy'):
    if b is None:
        return None
    bb = {r['run']: r for r in b['runs']}
    d = []
    for r in c['runs']:
        if str(h) in r['horizons'] and r['run'] in bb:
            hb = bb[r['run']]['horizons'].get(str(h)) or bb[r['run']]['horizons'][str(max(int(k) for k in bb[r['run']]['horizons']))]
            d.append(r['horizons'][str(h)][key] - hb[key])
    return boot(d) if d else None


def baseline_identity():
    out = {}
    for mine, theirs in (('B0', 'L0'), ('B1', 'L1'), ('B0-N50', 'L0-N50'), ('B1-N50', 'L1-N50'), ('B0-N200', 'L0-N200'),
                         ('B1-N200', 'L1-N200')):
        a = load(mine)
        f = os.path.join(SSDIR, theirs + '.json')
        if a is None or not os.path.exists(f):
            continue
        b = {r['run']: r for r in json.load(open(f))['runs']}
        same = 0; n = 0
        for r in a['runs']:
            s = b.get(r['run'])
            if s is None:
                continue
            n += 1
            ok = (r['stop_gen'] == s['stop_gen'] and r['status'] == s['status'] and r['nmig'] == s['nmig'] and
                  all(r['horizons'][h]['labels'] == s['horizons'][h]['labels'] for h in s['horizons'] if h in r['horizons']))
            same += ok
        out[mine] = [same, n]
    return out


def agg_counter(c, key):
    tot = Counter()
    for r in c['runs']:
        for k, v in r.get(key, {}).items():
            tot[k] += v
    return tot


def transition_summary(c):
    trig = agg_counter(c, 'triggers')
    entries = agg_counter(c, 'entries_into_V')
    exits = agg_counter(c, 'exits_from_V')
    mex = agg_counter(c, 'member_exit')
    jumps = agg_counter(c, 'jumps')
    trans = agg_counter(c, 'transitions')
    bytrig = defaultdict(Counter)
    for r in c['runs']:
        for t, d in r.get('transitions_by_trigger', {}).items():
            for k, v in d.items():
                bytrig[t][k] += v
    noncon = Counter()
    for t, d in bytrig.items():
        if t != 'contract':
            noncon.update(d)
    sm = np.array([r['same_member_return'] for r in c['runs']]).sum(0)
    cyc = agg_counter(c, 'cycles')
    mg = sum(r['member_gens'] for r in c['runs'])
    guard = agg_counter(c, 'guard')
    counts = agg_counter(c, 'counts')
    # jump matrix rows normalized
    jm = defaultdict(Counter)
    for k, v in jumps.items():
        a, b = k.split('>')
        jm[a][b] += v
    jmn = {a: {b: v / sum(row.values()) for b, v in row.items()} for a, row in jm.items()}
    jmn_n = {a: sum(row.values()) for a, row in jm.items()}
    # net circulation among classes
    circ = {}
    for k, v in trans.items():
        a, b = k.split('>')
        if a < b:
            circ['%s<>%s' % (a, b)] = v - trans.get('%s>%s' % (b, a), 0)
    return dict(triggers=dict(trig), entries=dict(entries), exits=dict(exits), member_exit=dict(mex),
                jump_rows=jmn, jump_n=jmn_n, transitions=dict(trans), noncontract=dict(noncon),
                same_member=[int(sm[0]), int(sm[1])], cycles=dict(cyc.most_common(10)), member_gens=int(mg),
                guard=dict(guard), counts=dict(counts), circulation=circ)


def refusal_summary(c, H):
    ch = [r['r_change'] for r in c['runs'] if 'r_change' in r]
    fin2000 = [r['horizons']['2000']['r_mean'] for r in c['runs'] if '2000' in r['horizons']]
    out = dict(change=boot(ch), below_half_2000=float(np.mean([v < 0.5 for v in fin2000])) if fin2000 else None,
               rising=float(np.mean([v > 0 for v in ch])) if ch else None)
    trajs = np.array([r['r_traj'] for r in c['runs']])
    out['traj'] = {str(g): round(float(trajs[:, g // 50].mean()), 4) for g in (0, 250, 500, 1000, 2000, 5000, 10000)
                   if g // 50 < trajs.shape[1]}
    # island-level: share vs mean bit, and protection configurations
    for h in ('2000', '10000'):
        xs = []; ys = []; prot = defaultdict(list)
        for r in c['runs']:
            isl = r.get('islands', {}).get(h)
            if not isl:
                continue
            for row in isl:
                xs.append(np.mean(row['bits'])); ys.append(row['share'])
                for kk in ('prot_pub', 'prot_priv'):
                    if row[kk] is not None:
                        prot['%s=%s' % (kk, row[kk])].append(row['share'])
        if xs:
            from scipy.stats import spearmanr
            rho = spearmanr(xs, ys).correlation if np.std(xs) > 0 else float('nan')
            # share by bit count among fully fixed islands
            bins = defaultdict(list)
            for r in c['runs']:
                for row in r.get('islands', {}).get(h, []):
                    if all(b in (0.0, 1.0) for b in row['bits']):
                        bins[int(sum(row['bits']))].append(row['share'])
            out['islands_' + h] = dict(spearman=float(rho), n=len(xs),
                                       share_by_fixed_bits={k: [round(float(np.mean(v)), 3), len(v)] for k, v in sorted(bins.items())},
                                       share_by_protection={k: [round(float(np.mean(v)), 3), len(v)] for k, v in prot.items()})
    return out


def fates(c):
    tot = defaultdict(Counter)
    for r in c['runs']:
        for k, d in r.get('fates', {}).items():
            tot[k].update(d)
    return {k: dict(v) for k, v in tot.items()}


def menus(c):
    sz = np.array([r['menu_size'] for r in c['runs']])
    cov = [r['menu_coverage'] for r in c['runs']]
    L = min(len(x) for x in cov)
    cv = np.array([[np.nan if x[j] is None else x[j] for j in range(L)] for x in cov])
    return dict(size={str(g): round(float(sz[:, g // 50].mean()), 3) for g in (0, 100, 250, 500, 1000, 2000) if g // 50 < sz.shape[1]},
                coverage={str(g): round(float(np.nanmean(cv[:, g // 50])), 3) for g in (0, 100, 250, 500, 1000, 2000) if g // 50 < cv.shape[1]})


def main():
    res = dict(identity=baseline_identity(), cells={})
    names = [n for n in DR.ORDER if load(n) is not None]
    for n in names:
        c = load(n)
        p = c['params']
        mN = p['mN']; N = p.get('N', 100)
        base = load('B%d' % mN if N == 100 else 'B%d-N%d' % (mN, N))
        d = dict(params=p, wall=c['wall'], horizons={})
        for h in DR.HS:
            row = horizon_row(c, h)
            if row is None:
                continue
            row['paired_occupancy'] = paired(c, base, h) if not n.startswith('B') else None
            row['modal_occupancy'] = modal_occ(n, len(c['runs']), h)
            row['paired_efficiency'] = paired(c, base, h, 'efficiency') if not n.startswith('B') else None
            d['horizons'][str(h)] = row
        d['transitions'] = transition_summary(c)
        if p.get('fr', 0) > 0:
            d['refusal'] = refusal_summary(c, p['H'])
        if p.get('beta', 1.0) < 1.0:
            d['fates'] = fates(c)
        if p.get('menu') == 'G':
            d['menus'] = menus(c)
        res['cells'][n] = d
    json.dump(res, open(os.path.join(ROOT, 'runs', 'dominance-contracts.json'), 'w'), indent=1, default=DR._js)
    write_md(res)


def write_md(res):
    L = []
    A = L.append
    A('# Dominance contracts and refusal on islands: run report (2026-10-14)')
    A('')
    A('Spec `specs/2026-10-14-dominance-contracts.md`; notes `notes/dominance-contracts.md`; predictions '
      '`predictions/2026-10-14-dominance-contracts.md`; code `src/dominance_contracts.py`, `src/dominance_contracts_run.py`, '
      '`src/dominance_contracts_report.py`. ε = 0 island lottery, I = 64, w = 0.3, weak arm n = 6, length-prior seeds '
      'shared with the stable-sets L cells (paired founders). Occupancy = fraction of islands classified (≥ 0.95) on a '
      'V\\* member; [95% bootstrap over runs]. Support ⊆ V\\* (strict) = every island on a member or member-mixed; '
      '"ss" = the stable-sets definition (classified islands only).')
    A('')
    A('## Baseline identity (ν = 0 rerun vs the stored stable-sets runs)')
    A('')
    for k, v in res['identity'].items():
        A('- %s: %d/%d runs identical (stop generation, status, migrant births, every horizon\'s class labels)' % (k, v[0], v[1]))
    A('')
    A('## Occupancy and classes')
    A('')
    A('| cell | H | runs | occupancy | modal-play occupancy | paired Δ vs baseline | unequal | wasteful | disagr. | grand | MM | MO | support strict | support ss | coverage | consensus | efficiency | Δ eff |')
    A('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for n, d in res['cells'].items():
        for h, row in d['horizons'].items():
            if h not in ('2000', '10000'):
                continue
            po = row.get('paired_occupancy'); pe = row.get('paired_efficiency')
            mo = row.get('modal_occupancy')
            A('| %s | %s | %d | %s | %s | %s | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f | %.2f | %.2f | %.2f | %.2f | %.3f | %s |' % (
                n, h, row['n'], fmt(row['occupancy']), fmt(mo) if mo else '–', fmt(po) if po else '–', row['unequal'], row['wasteful'],
                row['disagreement'], row['grand'], row['member-mixed'], row['other-mixed'], row['support_strict'],
                row['support_ss'], row['coverage'], row['consensus'], row['efficiency'], ('%+.3f' % pe[0]) if pe else '–'))
    A('')
    A('Occupancy at 500 / 1,000 (main cells):')
    A('')
    for n, d in res['cells'].items():
        if '-N' in n:
            continue
        hs = [h for h in ('500', '1000') if h in d['horizons']]
        A('- %s: %s' % (n, ', '.join('%s: %.3f' % (h, d['horizons'][h]['occupancy'][0]) for h in hs)))
    A('')
    A('## Transition structure')
    A('')
    for n, d in res['cells'].items():
        t = d['transitions']
        A('### %s' % n)
        A('')
        A('- contract counters (all runs): %s' % t['counts'])
        A('- guard: %s' % t['guard'])
        A('- settled transitions by trigger: %s' % t['triggers'])
        A('- entries into V\\* by trigger: %s; exits from V\\*: %s; member-island generations %d' % (t['entries'], t['exits'], t['member_gens']))
        A('- after a member exit, next member same / other: %d / %d' % tuple(t['same_member']))
        A('- contract jump rows (class at the event → class one generation later), with the generator\'s rows:')
        for a, row in sorted(t['jump_rows'].items()):
            g = GEN_JUMP.get(a, {})
            A('  - %s (n = %d): %s | generator %s' % (a, t['jump_n'][a], ', '.join('%s %.3f' % (b, v) for b, v in sorted(row.items())),
                                                  ', '.join('%s %.3f' % (b, v) for b, v in sorted(g.items()))))
        nc = t['noncontract']
        if nc:
            A('- non-contract settled transitions: %s' % dict(sorted(nc.items(), key=lambda kv: -kv[1])[:12]))
        A('- net circulation n(A→B) − n(B→A): %s' % {k: v for k, v in t['circulation'].items() if v})
        A('- most common minimal cycles (settled outcomes, classes M/U/W/D/G): %s' % t['cycles'])
        if 'refusal' in d:
            A('- refusal: %s' % json.dumps(d['refusal'], default=DR._js))
        if 'fates' in d:
            A('- β < 1 fates by edge class: %s' % d['fates'])
        if 'menus' in d:
            A('- menu G: %s' % d['menus'])
        A('')
    A('## Where the bit\'s rise comes from (decomposition added after the R1 cells; no prediction scored on it)')
    A('')
    A('Change of the island mean bit per 50-generation window, summed per run and divided by 64 islands, by the island\'s '
      'state at the window start (classified member or member-mixed vs not) and the window\'s contract events '
      '(`src/dominance_contracts_refusal.py`).')
    A('')
    for cell in ('R1pub-1', 'R1priv-1', 'R1blind-1', 'R1priv-0'):
        f = os.path.join(OUT, 'refusal_%s.json' % cell)
        if os.path.exists(f):
            o = json.load(open(f))
            A('- %s: %s' % (cell, ', '.join('%s %+.3f (%d windows)' % (k, v['sum_per_run_per_island'], v['windows'])
                                            for k, v in o['by_event'].items())))
    A('')
    vf = os.path.join(OUT, 'verdicts.md')
    if os.path.exists(vf):
        A(open(vf).read())
    open(os.path.join(ROOT, 'runs', 'dominance-contracts.md'), 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
