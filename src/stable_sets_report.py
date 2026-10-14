"""Report for the stable-sets-on-islands experiment: aggregates runs/stable_sets/<cell>.json into
runs/stable-sets-on-islands.json and runs/stable-sets-on-islands.md (verdicts appended from
runs/stable_sets/verdicts.md if present).

    python3 src/stable_sets_report.py
"""
import json, math, os, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stable_sets_run as R

ROOT = R.ROOT
OUT = R.OUT
CATS = ['fair', 'unequal', 'wasteful', 'grand-equal', 'grand-unequal', 'grand-wasteful', 'disagreement',
        'member-mixed', 'other-mixed']


def ci(v):
    v = np.asarray(v, float)
    if len(v) == 0:
        return [float('nan')] * 3
    m = v.mean()
    if len(v) < 2:
        return [m, m, m]
    h = 1.96 * v.std(ddof=1) / math.sqrt(len(v))
    return [float(m), float(m - h), float(m + h)]


def wilson(k, n):
    if n == 0:
        return [float('nan')] * 3
    p = k / n; z = 1.96
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [p, max(0.0, c - h), min(1.0, c + h)]


def km_median(pairs):
    """Kaplan-Meier median from (time, censored) pairs; None if not reached."""
    if not pairs:
        return None
    pairs = sorted(pairs)
    n = len(pairs); S = 1.0; i = 0
    while i < n:
        t = pairs[i][0]
        d = sum(1 for tt, c in pairs if tt == t and not c)
        at = sum(1 for tt, c in pairs if tt >= t)
        j = i
        while j < n and pairs[j][0] == t:
            j += 1
        if d:
            S *= 1 - d / at
            if S <= 0.5:
                return t
        i = j
    return None


def load(name):
    f = os.path.join(OUT, name + '.json')
    if not os.path.exists(f):
        return None
    return json.load(open(f))


def summarize(d):
    runs = d['runs']; n = len(runs)
    I = len(runs[0]['first_member'])
    out = dict(cell=d['cell'], params=d['params'], runs=n, wall=d['wall'], horizons={})
    for h in map(str, R.HS):
        H = [r['horizons'][h] for r in runs]
        s = {}
        for c in CATS:
            s[c] = ci([x['cats'].get(c, 0.0) for x in H])
        s['all_pairs'] = ci([sum(x['cats'].get(c, 0.0) for c in ('fair', 'unequal', 'wasteful')) for x in H])
        s['efficient_pairs'] = ci([sum(x['cats'].get(c, 0.0) for c in ('fair', 'unequal')) for x in H])
        s['unequal_share_of_pair_islands'] = ci([x['cats'].get('unequal', 0) / max(1e-12, x['cats'].get('unequal', 0) + x['cats'].get('fair', 0))
                                                 for x in H if x['cats'].get('unequal', 0) + x['cats'].get('fair', 0) > 0])
        for k in ('coverage', 'rs_strong', 'rs_strong_nomixed', 'rs_weak', 'consensus', 'resolved'):
            s[k] = wilson(sum(bool(x[k]) for x in H), n)
        s['n_members_present'] = ci([x['n_members_present'] for x in H])
        for k in ('efficiency', 'far_not_myopic', 'far_game_not_myopic', 'in_no_stable_set', 'payoff_support_mean_size',
                  'islands_with_nonmember_support', 'grand_islands', 'grand_unequal_islands', 'slot3_at_c_disc'):
            s[k] = ci([x[k] for x in H])
        wc = defaultdict(list)
        for x in H:
            for c in CATS:
                wc[c].append(x['window_cats'].get(c, 0.0))
        s['window'] = {c: float(np.mean(v)) for c, v in wc.items()}
        mp = Counter(); modal = Counter()
        for x in H:
            for k, v in x['member_pairs'].items():
                mp[k] += v
            if x['member_pairs']:
                top = max(x['member_pairs'].values())
                ws = [k for k, v in x['member_pairs'].items() if v == top]
                for k in ws:
                    modal[k] += 1 / len(ws)
        tot = sum(mp.values())
        s['member_pair_shares'] = {k: v / tot for k, v in sorted(mp.items())} if tot else {}
        s['modal_member_runs'] = {k: v / n for k, v in sorted(modal.items())}
        s['slot3_low_rate'] = (sum(x['slot3_low'] for x in H) / max(1, sum(x['slot3_pair_islands'] for x in H)))
        lab = Counter()
        for x in H:
            for k, v in x['labels'].items():
                lab[k] += v
        s['labels_pooled'] = {k: v / (n * I) for k, v in lab.most_common()}
        nsup = Counter(len([l for l in x['support']]) for x in H)
        s['support_size_runs'] = dict(nsup)
        out['horizons'][h] = s
    # transience and dwell
    fm = [t for r in runs for t in r['first_member']]
    reached = [t for t in fm if t >= 0]
    out['first_member'] = dict(frac_ever=len(reached) / len(fm), median_if_reached=float(np.median(reached)) if reached else None,
                               km_median=km_median([(t if t >= 0 else 10 ** 6, t < 0) for t in fm]))
    for key in ('grand', 'wasteful'):
        pairs = [tuple(x) for r in runs for x in r['dwell_first_visit'][key]]
        out['dwell_' + key] = dict(visits_per_run=len(pairs) / n, km_median=km_median(pairs),
                                   censored=sum(c for t, c in pairs) / max(1, len(pairs)),
                                   median_uncensored=float(np.median([t for t, c in pairs if not c])) if any(not c for t, c in pairs) else None)
    if 'flips' in runs[0]:
        F = [r['flips'] for r in runs]
        bt = Counter(); tr = Counter(); tbt = defaultdict(Counter)
        for f in F:
            bt.update(f['by_type']); tr.update(f['triggers'])
            for k, v in f['triggers_by_type'].items():
                tbt[k].update(v)
        mm = sum(f['member_member'] for f in F)
        out['flips'] = dict(per_run=ci([f['n'] for f in F]), by_type=dict(bt.most_common()), triggers=dict(tr.most_common()),
                            triggers_by_type={k: dict(v.most_common()) for k, v in tbt.items()},
                            member_member=mm, member_member_via_outsider=sum(f['member_member_via_outsider'] for f in F),
                            member_member_via_other_mixed=sum(f['member_member_via_other_mixed'] for f in F),
                            steps_out_of_nonmember=sum(f['steps_out_of_nonmember'] for f in F),
                            steps_out_following_arrow=sum(f['steps_out_following_arrow'] for f in F),
                            steps_all=sum(f['steps_all'] for f in F), steps_all_arrow=sum(f['steps_all_arrow'] for f in F),
                            examples=[e for f in F[:3] for e in f['examples'][:6]])
    out['stop_gen'] = dict(median=float(np.median([r['stop_gen'] for r in runs])),
                           resolved=sum(r['status'] in (1, 5) for r in runs),
                           stops=sorted(r['stop_gen'] for r in runs if r['status'] in (1, 5)))
    if 'forced' in runs[0]:
        if d['params']['law'] == 'Fr':
            res = [tuple(x) for r in runs for x in r['forced']['residence']]
            ent = [tuple(x) for r in runs for x in r['forced']['entry']]
            ex = Counter()
            for r in runs:
                ex.update(r['forced']['exits_to'])
            out['forced'] = dict(residence_km_median=km_median(res), residence_censored=sum(c for t, c in res) / len(res),
                                 residence_mean_uncensored=float(np.mean([t for t, c in res if not c])) if any(not c for t, c in res) else None,
                                 entry_km_median=km_median(ent), entry_censored=sum(c for t, c in ent) / len(ent),
                                 exits_to=dict(ex.most_common(8)))
        else:
            out['forced'] = {h: ci([r['forced'][h] for r in runs]) for h in map(str, R.HS)}
    return out


def chain_numbers():
    out = {}
    for tag in ('', '_stablesets'):
        f = os.path.join(ROOT, 'runs', 'dollar3', 'weak_N100%s.json' % tag)
        if os.path.exists(f):
            d = json.load(open(f))
            out['published' if tag == '' else 'rerun'] = {k: d[k] for k in ('mass_by_type', 'mass_by_coalition', 'E_max_share', 'efficiency',
                                                                             'P_some_slot_zero', 'circulation', 'pair_to_pair_by_mover',
                                                                             'dwell_events', 'lumped_relaxation_events', 'states', 'cut_flow', 'time_s') if k in d}
    return out


def fmt(c, nd=3):
    if c is None:
        return '–'
    if isinstance(c, (list, tuple)):
        if any(isinstance(x, float) and math.isnan(x) for x in c):
            return '–'
        return ('%.' + str(nd) + 'f [%.' + str(nd) + 'f, %.' + str(nd) + 'f]') % tuple(c)
    if isinstance(c, float):
        return ('%.' + str(nd) + 'f') % c
    return str(c)


def main():
    S = {}
    for name in R.ORDER:
        d = load(name)
        if d is not None:
            S[name] = summarize(d)
    chain = chain_numbers()
    static = json.load(open(os.path.join(ROOT, 'runs', 'stable-sets-static.json')))
    json.dump(dict(cells=S, chain=chain), open(os.path.join(ROOT, 'runs', 'stable-sets-on-islands.json'), 'w'), indent=1)
    L = []
    L.append('# Stable sets on islands: run report (2026-10-13)\n')
    L.append('Spec `specs/2026-10-13-stable-sets-on-islands.md`; notes `notes/stable-sets-on-islands.md`; predictions '
             '`predictions/2026-10-13-stable-sets-on-islands.md`; code `src/stable_sets.py`, `src/stable_sets_run.py`, '
             '`src/stable_sets_report.py`. ε = 0 lottery (finite-size evidence); the chain is a separate object. '
             'Intervals: 95% over runs (t for fractions of islands, Wilson for fractions of runs).\n')
    L.append('## Static (enumeration)\n')
    r = static['R']
    L.append('- R (20 realizable outcomes): C = M: %s; singleton commitments dominate: %s; myopic stable sets (M = C): %s; '
             'with game effectiveness: %s; single-slot moves only: %s.' % (r['C_equals_M'], r['singleton_C'], r['M_stable'],
                                                                          r['game_eff_myopic_all'], r['game_eff_myopic_singletons']))
    L.append('- Farsighted (TU): %s; LCS (TU) = all of R: %s. Farsighted (game effectiveness): %s.' % (
        r['farsighted_tu'], len(r['lcs_tu']) == 20, r['farsighted_game']))
    for k in ('G6=', 'G6', 'G8=', 'G8', 'R6x', 'R8x'):
        v = static[k]
        L.append('- %s (%d): stable sets %s; discriminatory sets %s.' % (k, v['n'], v.get('stable', v.get('M_stable')),
                                                                         v.get('discriminatory_sets', 0)))
    L.append('- Chicken under C: %s.\n' % static['chicken']['C_stable'])
    L.append('## Island classes by cell (fraction of islands; mean [95%] over runs)\n')
    for h in ('500', '2000', '10000'):
        L.append('### Horizon %s\n' % h)
        L.append('| cell | runs | fair (V\\*) | unequal | wasteful | grand | disagree | member-mixed | other-mixed | coverage (runs) | RS strong (runs) | consensus | resolved | efficiency |')
        L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        for name, s in S.items():
            x = s['horizons'][h]
            grand = [x['grand-equal'][0] + x['grand-unequal'][0] + x['grand-wasteful'][0]]
            L.append('| %s | %d | %s | %s | %s | %.3f | %.3f | %.3f | %.3f | %s | %s | %.2f | %.2f | %.3f |' % (
                name, s['runs'], fmt(x['fair']), fmt(x['unequal']), fmt(x['wasteful'], 2), grand[0], x['disagreement'][0],
                x['member-mixed'][0], x['other-mixed'][0], fmt(x['coverage'], 2), fmt(x['rs_strong'], 2),
                x['consensus'][0], x['resolved'][0], x['efficiency'][0]))
        L.append('')
    L.append('## Selection, symmetry, farsighted contrast (horizon 2,000)\n')
    L.append('| cell | members present (of 3) | unequal / (fair+unequal) | in no stable set | far (TU) not myopic | far (game) not myopic | member shares P12/P13/P23 | modal member (runs) | slot-3 low rate | islands with non-member support |')
    L.append('|---|---|---|---|---|---|---|---|---|---|')
    for name, s in S.items():
        x = s['horizons']['2000']
        L.append('| %s | %.2f | %s | %.3f | %.3f | %.3f | %s | %s | %.3f | %.3f |' % (
            name, x['n_members_present'][0], fmt(x['unequal_share_of_pair_islands']), x['in_no_stable_set'][0],
            x['far_not_myopic'][0], x['far_game_not_myopic'][0],
            '/'.join('%.2f' % x['member_pair_shares'].get(k, 0) for k in ('P12', 'P13', 'P23')),
            '/'.join('%.2f' % x['modal_member_runs'].get(k, 0) for k in ('P12', 'P13', 'P23')),
            x['slot3_low_rate'], x['islands_with_nonmember_support'][0]))
    L.append('')
    L.append('## Transience and dwell\n')
    L.append('| cell | islands ever on a member | median gen to first member (if reached) | grand: visits/run, KM median dwell, censored | wasteful: visits/run, KM median dwell, censored | stop gen median (resolved runs) |')
    L.append('|---|---|---|---|---|---|')
    for name, s in S.items():
        fm = s['first_member']; g = s['dwell_grand']; w = s['dwell_wasteful']
        L.append('| %s | %.3f | %s | %.1f, %s, %.2f | %.1f, %s, %.2f | %.0f (%d/%d) |' % (
            name, fm['frac_ever'], fm['median_if_reached'], g['visits_per_run'], g['km_median'], g['censored'],
            w['visits_per_run'], w['km_median'], w['censored'], s['stop_gen']['median'], s['stop_gen']['resolved'], s['runs']))
    L.append('')
    L.append('## Flips under migration (mN = 1)\n')
    for name, s in S.items():
        if 'flips' not in s: continue
        f = s['flips']
        L.append('**%s**: flips per run %s; by type %s; triggers %s; member→member %d, via an outsider class %d, via other-mixed %d; '
                 'steps out of a non-member following an M arrow %d/%d; all steps following an arrow %d/%d.' % (
                     name, fmt(f['per_run'], 1), f['by_type'], f['triggers'], f['member_member'], f['member_member_via_outsider'],
                     f['member_member_via_other_mixed'], f['steps_out_following_arrow'], f['steps_out_of_nonmember'],
                     f['steps_all_arrow'], f['steps_all']))
        L.append('  triggers by type: %s\n' % f['triggers_by_type'])
    L.append('## Forced seeds\n')
    for name, s in S.items():
        if 'forced' not in s: continue
        L.append('- %s: %s' % (name, json.dumps(s['forced'])))
    L.append('')
    L.append('## Chain (ε→0, weak arm, N = 100; a separate object)\n')
    for k, v in chain.items():
        L.append('- %s: %s' % (k, json.dumps(v)))
    L.append('')
    vf = os.path.join(OUT, 'verdicts.md')
    if os.path.exists(vf):
        L.append(open(vf).read())
    open(os.path.join(ROOT, 'runs', 'stable-sets-on-islands.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L)[:20000])


if __name__ == '__main__':
    main()
