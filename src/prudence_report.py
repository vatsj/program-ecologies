"""Tables and summaries for the prudence run (notes/prudence.md, predictions/2026-10-21-prudence-world-k.md).

    python3 src/prudence_report.py [--rows runs/prudence/cells_main.json.gz ...] [--out runs/prudence]

Reads the row files, writes runs/prudence.md (tables) and runs/prudence.json (summaries).  Every number is an ε = 0
seed lottery followed by a finite-(N = 12,800, horizon) re-injection diagnostic, never π.
"""
import argparse
import gzip
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORLDS = ('L', 'K')
ARMS = ('A0', 'A52', 'A156', 'SD52')
TAIL_T, END_T = '10000', '12000'
RNG = np.random.default_rng(20261021)


# ------------------------------------------------------------------------------------------------ io
def load(paths):
    rows = []
    for p in paths:
        rows += json.load(gzip.open(p))
    d = {}
    for r in rows:
        d.setdefault((r['world'], r['arm']), {})[r['rep']] = r
    return d


def reps_common(d, cells):
    s = None
    for c in cells:
        k = set(d.get(c, {}))
        s = k if s is None else (s & k)
    return sorted(s or [])


# ------------------------------------------------------------------------------------------------ per-run endpoints
def snap(row, t):
    return row['snaps'].get(t)


def endpoint(row, t):
    s = snap(row, t)
    if s is None: return None
    lt = s.get('light') or {}
    pcc = s.get('pcc')
    lost = (s.get('status') == 'lost') or (pcc is not None and pcc < 0.1)
    return dict(uo=bool(s.get('universal_open')), pcc=pcc, M=s.get('M'), lost=bool(lost),
                T=lt.get('T'), prud=lt.get('prud'), ung=lt.get('ung'), pb=lt.get('pb'), off=lt.get('off'),
                ident=lt.get('ident'), AP=lt.get('AP'), Q=lt.get('Q'), suck_c=lt.get('suck_c'), suck_u=lt.get('suck_u'),
                uot=(lt.get('T') is not None and lt['T'] >= 0.95),
                prudmaj=(lt.get('prud') is not None and lt['prud'] >= 0.5),
                imm=lt.get('imm'), i_prud=lt.get('i_prud'), i_T=lt.get('i_T'), i_pb=lt.get('i_pb'),
                h_sp=s.get('h_sp'), status=s.get('status'), nt=lt.get('nt'))


def max_over_time(row, key):
    v = [t[key] for t in row['trace'] if t.get(key) is not None]
    return max(v) if v else 0.0


# ------------------------------------------------------------------------------------------------ statistics helpers
def binom_upper(k, n, alpha=0.05):
    """One-sided Clopper-Pearson upper bound for k of n (bisection)."""
    if k >= n: return 1.0
    lo, hi = k / n, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        # P(X <= k | mid)
        p = sum(math.comb(n, i) * mid ** i * (1 - mid) ** (n - i) for i in range(k + 1))
        if p > alpha: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)


def sign_test(x):
    """Exact two-sided sign test on the paired differences x (zeros dropped); returns (n_pos, n_neg, p)."""
    x = np.asarray(x, float)
    pos = int((x > 0).sum()); neg = int((x < 0).sum()); n = pos + neg
    if n == 0: return pos, neg, 1.0
    k = min(pos, neg)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n * 2
    return pos, neg, min(1.0, p)


def boot_mean(x, B=4000):
    x = np.asarray(x, float)
    if len(x) == 0: return (None, None, None)
    m = float(x.mean())
    bs = RNG.choice(x, size=(B, len(x)), replace=True).mean(1)
    return m, float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975))


def mcnemar(a, b):
    """Exact McNemar on paired booleans a, b: (a only, b only, p)."""
    a = np.asarray(a, bool); b = np.asarray(b, bool)
    n01 = int((a & ~b).sum()); n10 = int((~a & b).sum())
    n = n01 + n10
    if n == 0: return n01, n10, 1.0
    k = min(n01, n10)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n * 2
    return n01, n10, min(1.0, p)


def fmt(x, nd=3):
    return '-' if x is None else (('%.' + str(nd) + 'f') % x)


def md_table(head, rows):
    out = ['| ' + ' | '.join(head) + ' |', '|' + '|'.join(['---'] * len(head)) + '|']
    for r in rows:
        out.append('| ' + ' | '.join(str(c) for c in r) + ' |')
    return '\n'.join(out)


# ------------------------------------------------------------------------------------------------ the report
def build(d, static=None):
    S = {}
    md = []
    cells = [(w, a) for w in WORLDS for a in ARMS if (w, a) in d]
    nrep = {c: len(d[c]) for c in cells}
    # ---------------------------------------------------------------- delivered exposure
    rows = []
    S['arrivals'] = {}
    for (w, a) in cells:
        rs = [d[(w, a)][k] for k in sorted(d[(w, a)])]
        A = rs[0]['A']
        n = np.array([r['arrivals'].get('n', 0) for r in rs])
        exp = A * 128
        if A > 0:
            by = np.array([[r['arrivals']['delivered_by'][str(x)] for x in (100, 500, 1000, 2000, 5000, 10000)] for r in rs])
            rows.append((w, a, len(rs), exp, '%.0f' % n.mean(), '%d-%d' % (n.min(), n.max()), fmt(n.mean() / exp, 4),
                         fmt(float(np.abs(n / exp - 1).max()), 4), fmt((by[:, 4] / n).mean(), 3),
                         fmt(float(((by[:, 3] / n) if False else (by[:, 2] / n)).mean()), 3)))
            S['arrivals'][w + ':' + a] = dict(mean=float(n.mean()), exp=exp, min=int(n.min()), max=int(n.max()),
                                              max_rel_dev=float(np.abs(n / exp - 1).max()))
    md.append('### Delivered exposure\n\n' + md_table(
        ['world', 'arm', 'runs', 'expected', 'mean realized', 'range', 'ratio', 'max |dev|', 'frac by 5,000', 'frac by 1,000'], rows))
    # ---------------------------------------------------------------- endpoints
    S['endpoints'] = {}
    for tt, label in ((TAIL_T, 'tail end (t = 10,000)'), (END_T, "chase end (t = 12,000)")):
        rows = []
        for (w, a) in cells:
            rs = [d[(w, a)][k] for k in sorted(d[(w, a)])]
            ep = [endpoint(r, tt) for r in rs]
            ep = [e for e in ep if e]
            n = len(ep)
            def cnt(key): return sum(1 for e in ep if e[key])
            def mean(key): return float(np.mean([e[key] for e in ep if e[key] is not None])) if ep else None
            idmax = [max_over_time(r, 'ident') for r in rs]
            row = [w, a, n, cnt('uo'), cnt('uot'), cnt('prudmaj'), cnt('lost'), fmt(mean('pcc')), fmt(mean('T')), fmt(mean('prud')),
                   fmt(mean('ung')), fmt(mean('pb')), fmt(mean('off'), 4), fmt(mean('ident'), 4),
                   sum(1 for x in idmax if x >= 0.05)]
            rows.append(row)
            S['endpoints'][tt + ':' + w + ':' + a] = dict(n=n, uo=cnt('uo'), uot=cnt('uot'), prudmaj=cnt('prudmaj'),
                                                         lost=cnt('lost'), pcc=mean('pcc'), T=mean('T'), prud=mean('prud'),
                                                         ung=mean('ung'), pb=mean('pb'), off=mean('off'),
                                                         ident=mean('ident'), ident_max_ge_05=sum(1 for x in idmax if x >= 0.05))
        md.append('### Endpoints at the %s\n\n' % label + md_table(
            ['world', 'arm', 'runs', 'universal-open', 'T ≥ 0.95', 'prudent ≥ 0.5', 'lost', 'P(C,C)', 'T share', 'prudent share',
             'unguarded share', 'PB own', 'off-target share', 'identity share', 'runs with identity ≥ 0.05 at some time'], rows))
    # ---------------------------------------------------------------- paired differences
    def vec(w, a, f):
        return {k: f(d[(w, a)][k]) for k in d[(w, a)]}
    S['paired'] = {}
    rows = []
    comps = []
    for w in WORLDS:
        comps += [(w, 'A52', 'A0'), (w, 'A156', 'A0'), (w, 'A52', 'SD52'), (w, 'SD52', 'A0'), (w, 'A156', 'A52')]
    for (w, a, b) in comps:
        if (w, a) not in d or (w, b) not in d: continue
        common = reps_common(d, [(w, a), (w, b)])
        for tt in (TAIL_T, END_T):
            for key in ('prud', 'T', 'pb', 'pcc'):
                x = [endpoint(d[(w, a)][k], tt)[key] - endpoint(d[(w, b)][k], tt)[key] for k in common
                     if endpoint(d[(w, a)][k], tt) and endpoint(d[(w, b)][k], tt)]
                if not x: continue
                m, lo, hi = boot_mean(x)
                pos, neg, p = sign_test(x)
                rows.append((w, '%s − %s' % (a, b), 't=%s' % tt, key, len(x), fmt(m), '[%s, %s]' % (fmt(lo), fmt(hi)), pos, neg, fmt(p)))
                S['paired']['%s:%s-%s:%s:%s' % (w, a, b, tt, key)] = dict(n=len(x), mean=m, lo=lo, hi=hi, pos=pos, neg=neg, p=p)
            ua = [endpoint(d[(w, a)][k], tt)['uo'] for k in common if endpoint(d[(w, a)][k], tt) and endpoint(d[(w, b)][k], tt)]
            ub = [endpoint(d[(w, b)][k], tt)['uo'] for k in common if endpoint(d[(w, a)][k], tt) and endpoint(d[(w, b)][k], tt)]
            n01, n10, p = mcnemar(ua, ub)
            rows.append((w, '%s − %s' % (a, b), 't=%s' % tt, 'universal-open (McNemar)', len(ua), fmt(np.mean(ua) - np.mean(ub)), '-', n01, n10, fmt(p)))
            S['paired']['%s:%s-%s:%s:uo' % (w, a, b, tt)] = dict(n=len(ua), diff=float(np.mean(ua) - np.mean(ub)), a_only=n01, b_only=n10, p=p)
    md.append('### Paired differences (same founders and merge seed)\n\n' + md_table(
        ['world', 'contrast', 'time', 'statistic', 'pairs', 'mean diff', '95% bootstrap', '+', '−', 'sign / McNemar p'], rows))
    # K − L
    rows = []
    for a in ARMS:
        if ('L', a) not in d or ('K', a) not in d: continue
        common = reps_common(d, [('L', a), ('K', a)])
        for tt in (TAIL_T, END_T):
            for key in ('prud', 'T', 'pcc'):
                x = [endpoint(d[('K', a)][k], tt)[key] - endpoint(d[('L', a)][k], tt)[key] for k in common
                     if endpoint(d[('K', a)][k], tt) and endpoint(d[('L', a)][k], tt)]
                if not x: continue
                m, lo, hi = boot_mean(x); pos, neg, p = sign_test(x)
                rows.append((a, 't=%s' % tt, key, len(x), fmt(m), '[%s, %s]' % (fmt(lo), fmt(hi)), pos, neg, fmt(p)))
                S['paired']['KL:%s:%s:%s' % (a, tt, key)] = dict(n=len(x), mean=m, lo=lo, hi=hi, p=p)
            ua = [endpoint(d[('K', a)][k], tt)['uo'] for k in common if endpoint(d[('K', a)][k], tt) and endpoint(d[('L', a)][k], tt)]
            ub = [endpoint(d[('L', a)][k], tt)['uo'] for k in common if endpoint(d[('K', a)][k], tt) and endpoint(d[('L', a)][k], tt)]
            n01, n10, p = mcnemar(ua, ub)
            rows.append((a, 't=%s' % tt, 'universal-open (McNemar)', len(ua), fmt(np.mean(ua) - np.mean(ub)), '-', n01, n10, fmt(p)))
            S['paired']['KL:%s:%s:uo' % (a, tt)] = dict(n=len(ua), diff=float(np.mean(ua) - np.mean(ub)), K_only=n01, L_only=n10, p=p)
    md.append('### World K minus world L (paired founders)\n\n' + md_table(
        ['arm', 'time', 'statistic', 'pairs', 'mean diff', '95% bootstrap', 'K>L', 'K<L', 'p'], rows))
    # ---------------------------------------------------------------- outcome regions
    rows = []
    S['regions'] = {}
    for w in WORLDS:
        if (w, 'A0') not in d or (w, 'A52') not in d: continue
        for tt in (TAIL_T, END_T):
            g = {a: np.mean([endpoint(r, tt)['prud'] for r in d[(w, a)].values() if endpoint(r, tt)]) for a in ARMS if (w, a) in d}
            ga0, ga52 = g['A0'], g['A52']
            gsd = g.get('SD52')
            uo52 = np.mean([endpoint(r, tt)['uo'] for r in d[(w, 'A52')].values() if endpoint(r, tt)])
            if uo52 <= 0.75 or ga52 < ga0: reg = 'R-harm'
            elif ga52 >= ga0 + 0.25 and gsd is not None and ga52 >= gsd + 0.20: reg = 'R-reward'
            elif ga52 >= ga0 + 0.25 and gsd is not None and ga52 - gsd < 0.10: reg = 'R-resilience'
            elif abs(ga52 - ga0) < 0.10: reg = 'R-null'
            else: reg = 'intermediate'
            rows.append((w, 't=%s' % tt, fmt(ga0), fmt(ga52), fmt(g.get('A156')), fmt(gsd), fmt(uo52), reg))
            S['regions']['%s:%s' % (w, tt)] = dict(G=g, uo52=float(uo52), region=reg)
    md.append('### Outcome regions (G = mean prudent-target share)\n\n' + md_table(
        ['world', 'time', 'G(A0)', 'G(A52)', 'G(A156)', 'G(SD52)', 'universal-open(A52)', 'region'], rows))
    # ---------------------------------------------------------------- residences
    rows = []
    S['residence'] = {}
    for (w, a) in cells:
        rs = [d[(w, a)][k] for k in sorted(d[(w, a)])]
        row = [w, a]
        for key in ('off', 'suck_c', 'suck_u', 'ident', 'prud'):
            v = np.array([r['res_tail'][key] for r in rs])
            row.append('%s (%d)' % (fmt(v.mean() / 1000, 3), int((v > 0).sum())))
            S['residence']['%s:%s:%s' % (w, a, key)] = dict(mean=float(v.mean()), runs_pos=int((v > 0).sum()), vals=v.tolist())
        rows.append(row)
    md.append('### Residence over the tail (share · 1,000 generations; runs with positive residence in brackets)\n\n' + md_table(
        ['world', 'arm', 'off-target (CBo)', 'certified suckers', 'uncertified suckers', 'identity', 'prudent target'], rows))
    rows = []
    for w in WORLDS:
        for (a, b) in (('A52', 'A0'), ('A52', 'SD52'), ('A156', 'A0')):
            if (w, a) not in d or (w, b) not in d: continue
            common = reps_common(d, [(w, a), (w, b)])
            x = [d[(w, a)][k]['res_tail']['off'] - d[(w, b)][k]['res_tail']['off'] for k in common]
            m, lo, hi = boot_mean(x); pos, neg, p = sign_test(x)
            rows.append((w, '%s − %s' % (a, b), len(x), fmt(m / 1000, 3), '[%s, %s]' % (fmt(lo / 1000, 3), fmt(hi / 1000, 3)), pos, neg, fmt(p)))
            S['paired']['res_off:%s:%s-%s' % (w, a, b)] = dict(n=len(x), mean=m, lo=lo, hi=hi, pos=pos, neg=neg, p=p)
    md.append('### Paired off-target residence difference (share · 1,000 generations)\n\n' + md_table(
        ['world', 'contrast', 'pairs', 'mean', '95% bootstrap', '+', '−', 'sign p'], rows))
    # ---------------------------------------------------------------- premium
    rows = []
    S['premium'] = {}
    for (w, a) in cells:
        if a == 'A0': continue
        rs = [d[(w, a)][k] for k in sorted(d[(w, a)])]
        Aexp = rs[0]['A']
        nsk = np.array([r['arrivals']['by_class']['suckerE'] for r in rs])
        esk = np.array([r['arrivals']['edgeH_sum']['suckerE'] for r in rs])
        nun = np.array([r['arrivals']['by_class']['SD'] for r in rs])
        eun = np.array([r['arrivals']['edgeH_sum']['SD'] for r in rs])
        # encounter-weighted edge integrated over the tail (trapezoid on the trace), per unit A
        ei, eic = [], []
        for r in rs:
            g = np.array([t['g'] for t in r['trace']], float); e = np.array([t['edge_enc'] for t in r['trace']])
            m = (g <= 10200)
            ei.append(float(np.trapz(e[m], g[m]))); eic.append(float(np.trapz(np.array([t['edge_enc_c'] for t in r['trace']])[m], g[m])))
        ei = np.array(ei); eic = np.array(eic)
        rows.append((w, a, fmt(esk.sum() / max(1, nsk.sum()), 4), fmt(nsk.mean(), 0), fmt(esk.mean() / (Aexp * 128 / 100), 3) if Aexp else '-',
                     fmt(eun.sum() / max(1, nun.sum()), 4), fmt(ei.mean() / Aexp, 3), fmt(eic.mean() / Aexp, 3)))
        S['premium'][w + ':' + a] = dict(edge_per_sucker_arrival=float(esk.sum() / max(1, nsk.sum())), n_sucker_arrivals_mean=float(nsk.mean()),
                                         edge_per_SD_arrival=float(eun.sum() / max(1, nun.sum())),
                                         enc_edge_int_per_A=float(ei.mean() / Aexp), enc_edge_cert_int_per_A=float(eic.mean() / Aexp))
    md.append('### The premium: fixed-list edge per arriving sucker (primary), encounter-weighted edge integrated over the tail per A (secondary)\n\n' +
              md_table(['world', 'arm', 'edge per arriving uncertified-sucker founder (H-state)', 'sucker arrivals / run',
                        'edge per 100 programs', 'edge per arriving SD founder', 'encounter edge · generations / A', 'of which certified suckers'], rows))
    if static:
        md.append('Static fixed-list edges (`runs/prudence-static.json`): ' + json.dumps({w: {k: static[w]['premium'][k] for k in ('suckerE', 'SD', 'suckerH_cert', 'Q')} for w in WORLDS}))
    # ---------------------------------------------------------------- ancestry
    rows = []
    S['ancestry'] = {}
    for (w, a) in cells:
        if a == 'A0': continue
        rs = [d[(w, a)][k] for k in sorted(d[(w, a)])]
        up, imm_sh, dimm, dres, n_up = [], [], [], [], 0
        for r in rs:
            tr = r['trace']
            e0 = r['comp']['light']; e2 = snap(r, '2000')
            tend = snap(r, TAIL_T)
            if tend is None: continue
            lt = tend['light']
            gain = lt['prud'] - e0['prud']
            if gain >= 0.25:
                n_up += 1
                imm_sh.append(lt['i_prud'] / lt['prud'] if lt['prud'] > 0 else 0.0)
            if e2 is not None:
                l2 = e2['light']
                dimm.append(l2['i_prud'] - e0['i_prud']); dres.append((l2['prud'] - l2['i_prud']) - (e0['prud'] - e0['i_prud']))
        rows.append((w, a, n_up, fmt(np.mean(imm_sh)) if imm_sh else '-', fmt(np.mean(dimm)) if dimm else '-', fmt(np.mean(dres)) if dres else '-'))
        S['ancestry'][w + ':' + a] = dict(n_gain=n_up, imm_frac=(float(np.mean(imm_sh)) if imm_sh else None),
                                          d_imm_2000=(float(np.mean(dimm)) if dimm else None), d_res_2000=(float(np.mean(dres)) if dres else None))
    md.append('### Ancestry of the prudent share (gain = tail-end prudent share minus its value at the merge ≥ 0.25)\n\n' +
              md_table(['world', 'arm', 'runs with gain ≥ 0.25', 'arrival-descended fraction of the tail-end prudent share',
                        'Δ prudent share from arrivals, t = 0 → 2,000', 'Δ from residents'], rows))
    # ---------------------------------------------------------------- colonizations
    rows = []
    S['colonization'] = {}
    for (w, a) in cells:
        if a == 'A0': continue
        rs = [d[(w, a)][k] for k in sorted(d[(w, a)])]
        col = [c for r in rs for c in r['colonizations']]
        sel = sum(1 for c in col if c['selected'])
        runs = sum(1 for r in rs if r['colonizations'])
        rows.append((w, a, len(col), runs, sel, len(col) - sel, sum(1 for c in col if c['prud_H']), sum(1 for c in col if c['Q']),
                     sum(1 for c in col if c['suckerE'])))
        S['colonization'][w + ':' + a] = dict(n=len(col), runs=runs, selected=sel, drift=len(col) - sel,
                                              prudent_arrival=sum(1 for c in col if c['prud_H']), Q=sum(1 for c in col if c['Q']))
    md.append('### Arrival lineages that reached half of the population\n\n' + md_table(
        ['world', 'arm', 'lineages', 'runs', 'selected (arrival payoff above the mean)', 'drift', 'prudent-target arrivals', 'Q arrivals', 'sucker arrivals'], rows))
    # ---------------------------------------------------------------- composition at the merge
    rows = []
    S['merge'] = {}
    for w in WORLDS:
        if (w, 'A0') not in d: continue
        rs = [d[(w, 'A0')][k] for k in sorted(d[(w, 'A0')])]
        L = [r['comp']['light'] for r in rs]
        row = [w, len(rs)] + [fmt(np.mean([l[k] for l in L])) for k in ('pcc', 'T', 'prud', 'ung', 'pb', 'off', 'suck_c', 'suck_u', 'ident', 'AP')] + \
            [fmt(np.mean([l['nt'] for l in L]), 0)]
        rows.append(row)
        S['merge'][w] = {k: float(np.mean([l[k] for l in L])) for k in ('pcc', 'T', 'prud', 'ung', 'pb', 'off', 'suck_c', 'suck_u', 'ident', 'AP')}
    md.append('### Composition at the merge (generation 200; A0 rows, identical across arms)\n\n' + md_table(
        ['world', 'runs', 'P(C,C)', 'T', 'prudent', 'unguarded', 'PB own', 'off-target', 'certified suckers', 'uncertified suckers', 'identity', 'AP', 'living types'], rows))
    # ---------------------------------------------------------------- winner structure
    rows = []
    S['winner'] = {}
    for (w, a) in cells:
        rs = [d[(w, a)][k] for k in sorted(d[(w, a)])]
        pl = [snap(r, END_T)['light']['plur'] for r in rs if snap(r, END_T) and snap(r, END_T)['light'].get('plur')]
        ch = []
        for r in rs:
            sp = [t.get('plur_s') for t in r['trace'] if t.get('plur_s') is not None]
            ch.append(sum(1 for i in range(1, len(sp)) if sp[i] != sp[i - 1]) if sp else None)
        n = len(pl)
        rows.append((w, a, n, sum(1 for p in pl if p['T']), sum(1 for p in pl if p['prud']), sum(1 for p in pl if p['pb']),
                     fmt(np.mean([c for c in ch if c is not None]), 1) if any(c is not None for c in ch) else '-'))
        S['winner'][w + ':' + a] = dict(n=n, plur_T=sum(1 for p in pl if p['T']), plur_prud=sum(1 for p in pl if p['prud']),
                                        plur_pb=sum(1 for p in pl if p['pb']))
    md.append("### Plurality type at the chase's end, and plurality changes over the tail\n\n" + md_table(
        ['world', 'arm', 'runs', 'plurality in T', 'plurality guarded', 'plurality PB tree', 'mean plurality-spelling changes (samples)'], rows))
    return S, '\n\n'.join(md)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rows', nargs='+', default=[os.path.join(ROOT, 'runs/prudence/cells_main.json.gz')])
    ap.add_argument('--out', default=os.path.join(ROOT, 'runs', 'prudence'))
    a = ap.parse_args()
    d = load(a.rows)
    sp = os.path.join(ROOT, 'runs', 'prudence-static.json')
    static = json.load(open(sp)) if os.path.exists(sp) else None
    S, md = build(d, static)
    head = ('# Prudence under world K: report (generated by src/prudence_report.py from %s)\n\n'
            'Every number is an ε = 0 seed lottery followed by a finite-(N = 12,800, horizon) re-injection diagnostic, never π. '
            'Runs per cell: %s.\n\n' % (', '.join(os.path.basename(p) for p in a.rows),
                                       ', '.join('%s %s: %d' % (w, ar, len(d[(w, ar)])) for (w, ar) in sorted(d))))
    open(a.out + '.md', 'w').write(head + md + '\n')
    json.dump(S, open(a.out + '.json', 'w'), indent=1)
    print(head + md)


if __name__ == '__main__':
    main()
