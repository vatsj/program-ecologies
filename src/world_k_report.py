"""Report for the world-K reruns: tables, paired contrasts, transitions, verdict inputs (runs/world-k.md, .json).

    python3 src/world_k_report.py
"""
import glob
import gzip
import json
import math
import os
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'world_k')


# ------------------------------------------------------------------------------------------------ statistics
def cp(k, n, a=0.05):
    from scipy.stats import beta
    if n == 0: return (None, None)
    lo = 0.0 if k == 0 else float(beta.ppf(a / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(1 - a / 2, k + 1, n - k))
    return (round(lo, 3), round(hi, 3))


def mcnemar(xk, xl):
    """Paired binary: K − L difference, exact McNemar p, conditional exact 95% interval for the difference."""
    from scipy.stats import binomtest
    xk = np.asarray(xk, bool); xl = np.asarray(xl, bool)
    n = len(xk)
    b = int((xk & ~xl).sum()); c = int((~xk & xl).sum())
    d = (b - c) / n if n else None
    nd = b + c
    if nd == 0:
        return dict(n=n, b=b, c=c, diff=0.0, p=1.0, ci=(0.0, 0.0), ci_note='no discordant pairs')
    p = float(binomtest(b, nd, 0.5).pvalue)
    lo, hi = cp(b, nd)
    f = nd / n
    return dict(n=n, b=b, c=c, diff=round(d, 3), p=round(p, 4), ci=(round(f * (2 * lo - 1), 3), round(f * (2 * hi - 1), 3)))


def equiv(m, x):
    """'within x' scoring: held / inconclusive / failed (predictions' conventions)."""
    if abs(m['diff']) > x: return 'failed'
    if m['ci'][0] >= -x and m['ci'][1] <= x: return 'held'
    return 'inconclusive'


def load(part):
    rows = []
    for p in sorted(glob.glob(os.path.join(OUT, 'cells_%s*.json.gz' % part))):
        rows += json.load(gzip.open(p))
    return rows


# ------------------------------------------------------------------------------------------------ H classes
_HC = {}


def hclass(w):
    """Pangaea's family class of every spelling at H units in world w (identity units 'ID')."""
    if w in _HC: return _HC[w]
    import world_k as WK
    LS = WK.world_ls(w)
    A = np.asarray(LS['st']['A']); sa = np.asarray(LS['st']['selfa'])
    names, tau, Hu = LS['names'], LS['tau'], LS['Hu']
    dH = int(LS['u_d']); cbH = int(LS['u_cb'])
    apH = int(Hu[tau[names.index('if(CHK(them,^D,D),D,C)')]])
    pbH = int(Hu[tau[names.index('if(and(CHK(them,me,C),CHK(them,^D,D)),C,D)')]])
    ident = np.asarray(LS['ident'])
    out = []
    for k in range(len(names)):
        u = int(Hu[tau[k]])
        if ident[u]: c = 'ID'
        elif A[u, dH] == 1: c = 'S' if sa[u] == 1 else 'S-'
        elif sa[u] != 1: c = 'Dill' if A[apH, u] == 1 else 'D'
        else:
            mcb = A[u, cbH] == 1 and A[cbH, u] == 1
            map_ = A[u, apH] == 1 and A[apH, u] == 1
            mpb = A[u, pbH] == 1 and A[pbH, u] == 1
            c = 'BR' if (mcb and map_) else ('PBn' if (mcb and mpb) else ('CBo' if mcb else ('APn' if map_ else 'Eo')))
        out.append(c)
    _HC[w] = out
    return out


# ------------------------------------------------------------------------------------------------ island cells
def snap(r, g):
    s = r['snaps'].get(str(g))
    if s is None and r['last_gen'] < g: s = r['final']
    return s


def uo_at(r, g):
    s = snap(r, g)
    return bool(s['universal_open']) if s else False


def island_cell_summary(rows):
    out = {}
    by = defaultdict(list)
    for r in rows:
        by[(r['cell'], r['world'])].append(r)
    names = None
    for (cell, w), rs in sorted(by.items()):
        rs.sort(key=lambda r: r['rep'])
        n = len(rs); I = rs[0]['I']; N = rs[0]['N']
        u2 = sum(uo_at(r, 2000) for r in rs); u10 = sum(uo_at(r, 10000) for r in rs)
        id2 = np.mean([snap(r, 2000)['identity_islands'] / I for r in rs])
        id10 = np.mean([snap(r, 10000)['identity_islands'] / I for r in rs])
        causes = Counter(r['final']['isl']['cause'] or 'universal' for r in rs)
        scramble = sum(1 for r in rs if r['final']['held'] == 0)
        eff = [np.mean(r['final']['isl']['cc']) for r in rs if r['final']['held'] > 0]
        e95 = [np.mean(np.array(r['final']['isl']['cc']) >= 0.95) for r in rs if r['final']['held'] > 0]
        stat = Counter(r['static']['label'] for r in rs)
        changed_after_2k = sum(1 for r in rs if uo_at(r, 2000) != uo_at(r, 10000))
        rr = [r['final'].get('rr') for r in rs]
        rrc = Counter()
        uot = 0
        if rr[0]:
            for x in rr:
                rrc.update({k: v for k, v in x['counts'].items() if k})
                uot += int(x['uot'])
        rr2 = [snap(r, 2000).get('rr') for r in rs]
        rrc2 = Counter(); uot2 = 0
        if rr2[0]:
            for x in rr2:
                rrc2.update({k: v for k, v in x['counts'].items() if k}); uot2 += int(x['uot'])
        estab = [min([e for e in r['establish'] if e >= 0], default=-1) for r in rs]
        q = [sum(r['seeded']['Q']) for r in rs]
        ex = extra_island(rs, w)
        out['%s|%s' % (cell, w)] = dict(cell=cell, world=w, N=N, I=I, n=n, uo2000=u2, uo10000=u10, extra=ex,
                                       uo10000_ci=cp(u10, n), ident2000=round(float(id2), 4),
                                       ident10000=round(float(id10), 4), causes=dict(causes), scramble=scramble,
                                       mean_isl_pcc_excl_scramble=round(float(np.mean(eff)), 4) if eff else None,
                                       frac_isl95=round(float(np.mean(e95)), 4) if e95 else None, static=dict(stat),
                                       uo_changed_after_2000=changed_after_2k, rr_end=dict(rrc), uot_end=uot,
                                       rr_2000=dict(rrc2), uot_2000=uot2,
                                       first_estab_median=float(np.median([e for e in estab if e >= 0])) if any(e >= 0 for e in estab) else None,
                                       Q_seeded_mean=float(np.mean(q)), time_h=round(sum(r['time_s'] for r in rs) / 3600, 2))
    return out


_UC = {}


def uclass(w, u):
    """The actual holder unit's class: APnet (self-cooperating, mutual with AP-H, not open), open, other."""
    if u is None: return 'unknown'
    if w not in _UC:
        import world_k as WK
        LS = WK.world_ls(w)
        A = np.asarray(LS['st']['A']); sa = np.asarray(LS['st']['selfa'])
        names, tau, Hu = LS['names'], LS['tau'], LS['Hu']
        apH = int(Hu[tau[names.index('if(CHK(them,^D,D),D,C)')]])
        pbH = int(Hu[tau[names.index('if(and(CHK(them,me,C),CHK(them,^D,D)),C,D)')]])
        _UC[w] = (A, sa, np.asarray(LS['openu']), apH, pbH, np.asarray(LS['ident']))
    A, sa, openu, apH, pbH, ident = _UC[w]
    if ident[u]: return 'identity'
    if openu[u]: return 'open-closed' if not (A[u, pbH] == 1 and A[pbH, u] == 1) else 'open-T'
    if A[u, apH] == 1 and A[apH, u] == 1: return 'APnet'
    return 'other'


def extra_island(rs, w):
    """Identity holders by class (minted C-identity trees / former Q / other), rival holders' H classes, exposure,
    S-self budget, minting counts, the former TwinD share at 200."""
    import world_k as WK
    import provenance as PV
    ST = WK.static_sets()
    hc = hclass(w)
    idh = Counter(); rvh = Counter(); rvh2 = Counter()
    for r in rs:
        for g, C_ in (('2000', idh), ):
            s = snap(r, int(g))
            for c_, h in zip(s['cls'], s['holders']):
                if c_ == 'i':
                    C_['mint' if ST['mint'][h] else ('Q' if ST['Q'][h] else 'other')] += 1
        f = r['final']
        lastu = {}
        for c in r['changes']:
            lastu[c[1]] = c[3]
        for i, (c_, h) in enumerate(zip(f['cls'], f['holders'])):
            if c_ == 'r':
                rvh[hc[h]] += 1
                rvh2[uclass(w, lastu.get(i))] += 1
        runs_ap = sum(1 for r in rs if any(c_ == 'r' and hc[h] in ('APn', 'BR') for c_, h in zip(r['final']['cls'], r['final']['holders'])))
    fail_runs = [r for r in rs if not r['final']['universal_open']]
    ap_fail = sum(1 for r in fail_runs if any(c_ == 'r' and hc[h] in ('APn', 'BR') for c_, h in zip(r['final']['cls'], r['final']['holders'])))
    rival_isl_per_run = float(np.mean([sum(1 for c_ in r['final']['cls'] if c_ == 'r') for r in rs]))
    expo = {}
    for g in ('200', '2000', '10000'):
        v = [r['expo'][g] for r in rs if r['expo'].get(g) and r['expo'][g][0] is not None]
        if v:
            tot = sum(x[1] for x in v)
            if tot:
                expo[g] = dict(n_ind=tot, frac=[round(sum(np.array(x[0]) * x[1] for x in v)[j] / tot, 4) for j in range(4)])
    sb = {}
    for g in ('0', '10', '50', '200', '2000'):
        v = [r['selfb'][g] for r in rs if r['selfb'].get(g) and r['selfb'][g]['lacking']]
        if v:
            sb[g] = dict(lacking_mean=float(np.mean([x['lacking'] for x in v])),
                         self_share=round(float(np.average([x['self_share'] for x in v], weights=[x['lacking'] for x in v])), 5))
    mint = [int(np.asarray(r['ctr'])[:, PV.C_IDENT_ENTRY].sum()) for r in rs]
    q200 = [t[6] for r in rs for t in r['trace'] if t[0] == 200]
    return dict(ident_holders_2000=dict(idh), rival_holder_classes_end=dict(rvh), rival_holder_unit_classes_end=dict(rvh2), fail_runs=len(fail_runs),
                fail_runs_with_AP_rival=ap_fail, rival_isl_per_run=round(rival_isl_per_run, 3), expo=expo, selfb=sb,
                ident_entries_mean=float(np.mean(mint)), Q_share_200_max=max(q200) if q200 else None,
                Q_share_200_mean=float(np.mean(q200)) if q200 else None)


def paired(rows, cellK, cellL, wK, wL, g):
    a = {r['rep']: r for r in rows if r['cell'] == cellK and r['world'] == wK}
    b = {r['rep']: r for r in rows if r['cell'] == cellL and r['world'] == wL}
    reps = sorted(set(a) & set(b))
    if not reps: return None
    return mcnemar([uo_at(a[k], g) for k in reps], [uo_at(b[k], g) for k in reps])


def transitions(rows, cell):
    """L × K island-class contingency at 200, 2,000, 10,000 and the attribution of L identity islands."""
    a = {r['rep']: r for r in rows if r['cell'] == cell and r['world'] == 'L'}
    b = {r['rep']: r for r in rows if r['cell'] == cell and r['world'] == 'K'}
    reps = sorted(set(a) & set(b))
    out = {}
    for g in (200, 2000, 10000):
        tab = Counter()
        for k in reps:
            sl, sk = snap(a[k], g), snap(b[k], g)
            for x, y in zip(sl['cls'], sk['cls']):
                tab[x + y] += 1
        out[str(g)] = dict(tab)
    # L identity islands at 2,000: their K counterparts' class and how the K holder came (local or migrant lineage)
    att = Counter()
    for k in reps:
        sl, sk = snap(a[k], 2000), snap(b[k], 2000)
        loc = sk.get('local')
        for i, (x, y) in enumerate(zip(sl['cls'], sk['cls'])):
            if x != 'i': continue
            if y == 'o':
                lsh = loc[i] if loc else None
                att['open_local' if (lsh is not None and lsh >= 0.5) else 'open_migrant'] += 1
            else:
                att['K_' + y] += 1
    # when did the K counterpart first become open, and from what lineage: first change record with class 'o'
    first = []
    for k in reps:
        sl = snap(a[k], 2000)
        ch = defaultdict(list)
        for c in b[k]['changes']:
            ch[c[1]].append(c)
        for i, x in enumerate(sl['cls']):
            if x != 'i': continue
            fo = [c for c in ch[i] if c[4] == 'o']
            if fo:
                first.append((fo[0][0], fo[0][5]))
    out['L_identity_at_2000_K_counterpart'] = dict(att)
    if first:
        out['K_first_open'] = dict(n=len(first), median_gen=float(np.median([f[0] for f in first])),
                                   local_at_first=float(np.mean([(f[1] or 0) >= 0.5 for f in first])))
    return out


# ------------------------------------------------------------------------------------------------ Pangaea cells
def pg_summary(rows):
    out = {}
    by = defaultdict(list)
    for r in rows:
        by[(r['cell'], r['world'])].append(r)
    for (cell, w), rs in sorted(by.items()):
        rs.sort(key=lambda r: r['rep'])
        n = len(rs)
        def at(r, g):
            s = r['snaps'].get(str(g))
            return s if s is not None else r['final']
        uo2 = sum(bool(at(r, 2000).get('uo')) for r in rs)
        uoe = sum(bool(r['final'].get('uo')) for r in rs)
        lost = sum(1 for r in rs if r['first_lost'] >= 0 or r['final'].get('status') == 'lost')
        tgt = sum(1 for r in rs if r['final'].get('target', 0) >= 0.9)
        ident_isl = [r['final'].get('ident_isl') for r in rs]
        out['%s|%s' % (cell, w)] = dict(cell=cell, world=w, n=n, uo2000=uo2, uo_end=uoe, lost=lost, lost_ci=cp(lost, n),
                                       target90=tgt, max_AP=round(max(r['max_AP'] for r in rs), 4),
                                       max_AP_median=round(float(np.median([r['max_AP'] for r in rs])), 4),
                                       max_ident=round(max(r['max_ident'] for r in rs), 4),
                                       max_Q=round(max(r['max_Q'] for r in rs), 5),
                                       ident_isl_mean=(float(np.mean([x for x in ident_isl if x is not None]))
                                                       if any(x is not None for x in ident_isl) else None),
                                       estab_median=float(np.median([r['establish_gen'] for r in rs if r['establish_gen'] >= 0]))
                                       if any(r['establish_gen'] >= 0 for r in rs) else None,
                                       AP_winner=sum(1 for r in rs if r['final'].get('APnet', 0) >= 0.5),
                                       time_h=round(sum(r['time_s'] for r in rs) / 3600, 2))
    return out


def pg_paired_lost(rows, cell):
    a = {r['rep']: r for r in rows if r['cell'] == cell and r['world'] == 'K'}
    b = {r['rep']: r for r in rows if r['cell'] == cell and r['world'] == 'L'}
    reps = sorted(set(a) & set(b))
    lostf = lambda r: r['first_lost'] >= 0 or r['final'].get('status') == 'lost'
    return mcnemar([lostf(a[k]) for k in reps], [lostf(b[k]) for k in reps]) if reps else None


def pg_paired_uo(rows, cell, g=2000):
    a = {r['rep']: r for r in rows if r['cell'] == cell and r['world'] == 'K'}
    b = {r['rep']: r for r in rows if r['cell'] == cell and r['world'] == 'L'}
    reps = sorted(set(a) & set(b))
    at = lambda r: bool((r['snaps'].get(str(g)) or r['final']).get('uo'))
    return mcnemar([at(a[k]) for k in reps], [at(b[k]) for k in reps]) if reps else None


def main():
    A = load('A'); B = load('B'); D = load('D'); C = load('C'); Nn = load('N')
    isl = A + B + D
    rep = dict(island=island_cell_summary(isl), pangaea=pg_summary(C + Nn))
    pairs = {}
    for c in sorted(set(r['cell'] for r in isl)):
        pairs['%s K-L' % c] = dict(g2000=paired(isl, c, c, 'K', 'L', 2000), g10000=paired(isl, c, c, 'K', 'L', 10000))
    for (N, I) in [(100, 64), (200, 64), (400, 64), (100, 128), (200, 128), (100, 256)]:
        cs, cp_ = 'wk_Snon_%d_%d' % (N, I), 'wk_prop_%d_%d' % (N, I)
        pairs['%s K Snon - L prop' % cp_] = dict(g2000=paired(isl, cs, cp_, 'K', 'L', 2000), g10000=paired(isl, cs, cp_, 'K', 'L', 10000))
        pairs['%s K prop - K Snon' % cp_] = dict(g10000=paired(isl, cp_, cs, 'K', 'K', 10000))
    for (N, I) in [(100, 64), (200, 64)]:
        for w in ('L', 'K'):
            pairs['Snon-Sself %d_%d %s' % (N, I, w)] = dict(
                g2000=paired(isl, 'wk_Snon_%d_%d' % (N, I), 'wk_Sself_%d_%d' % (N, I), w, w, 2000),
                g10000=paired(isl, 'wk_Snon_%d_%d' % (N, I), 'wk_Sself_%d_%d' % (N, I), w, w, 10000))
    for w in ('L', 'K'):
        pairs['rain - e0 200_64 %s' % w] = dict(g10000=paired(isl, 'wk_rain_200_64', 'wk_Snon_200_64', w, w, 10000))
    rep['pairs'] = pairs
    rep['transitions'] = {c: transitions(isl, c) for c in sorted(set(r['cell'] for r in isl))}
    rep['pg_pairs'] = {c: dict(lost=pg_paired_lost(C + Nn, c), uo2000=pg_paired_uo(C + Nn, c)) for c in sorted(set(r['cell'] for r in C + Nn))}
    json.dump(rep, open(os.path.join(ROOT, 'runs', 'world-k.json'), 'w'), indent=1, default=str)
    print(json.dumps(rep, indent=1, default=str)[:20000])


if __name__ == '__main__':
    main()
