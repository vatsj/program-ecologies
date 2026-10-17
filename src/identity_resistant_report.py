"""Report for the identity-resistant target (notes/identity-resistant.md): tables, paired comparisons and verdicts.

    python3 src/identity_resistant_report.py            # writes runs/identity-resistant.json and prints the tables
"""
import glob
import gzip
import json
import math
import os
import sys
from collections import Counter, defaultdict

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'identity_resistant')


def load(pattern='cells_*.json.gz'):
    rows = []
    for f in sorted(glob.glob(os.path.join(OUT, pattern))):
        rows += json.load(gzip.open(f))
    seen = {}
    for r in rows: seen[(r['cell'], r['rep'])] = r
    return list(seen.values())


def cp(k, n, a=0.05):
    if n == 0: return (None, None)
    lo = 0.0 if k == 0 else stats.beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(1 - a / 2, k + 1, n - k)
    return (round(float(lo), 3), round(float(hi), 3))


def mcnemar(xa, xb):
    """Paired binary outcomes (lists aligned by replicate): b = a yes & b no ... returns dict with the difference
    (mean b - mean a), discordant counts, exact two-sided p, and the conditional exact interval of the difference."""
    n = len(xa)
    up = sum(1 for p, q in zip(xa, xb) if q and not p)       # b gains
    dn = sum(1 for p, q in zip(xa, xb) if p and not q)
    m = up + dn
    p = 1.0 if m == 0 else float(min(1.0, 2 * stats.binom.cdf(min(up, dn), m, 0.5)))
    if m:
        lo, hi = cp(up, m)
        ci = (round((2 * lo - 1) * m / n, 3), round((2 * hi - 1) * m / n, 3))
    else:
        ci = (0.0, 0.0)
    return dict(n=n, a=int(sum(map(bool, xa))), b=int(sum(map(bool, xb))), diff=round((up - dn) / n, 3), gains=up,
                losses=dn, p=round(p, 4), ci=ci)


def boot_ratio(num_a, den_a, num_b, den_b, B=2000, seed=1):
    """Run-bootstrap (paired by replicate index) of (sum num_b / sum den_b) / (sum num_a / sum den_a)."""
    num_a, den_a, num_b, den_b = map(np.asarray, (num_a, den_a, num_b, den_b))
    n = len(num_a)
    rng = np.random.default_rng(seed)
    ra = num_a.sum() / max(den_a.sum(), 1e-12); rb = num_b.sum() / max(den_b.sum(), 1e-12)
    out = []
    for _ in range(B):
        ix = rng.integers(0, n, n)
        a = num_a[ix].sum() / max(den_a[ix].sum(), 1e-12); b = num_b[ix].sum() / max(den_b[ix].sum(), 1e-12)
        if a > 0: out.append(b / a)
    q = (round(float(np.percentile(out, 2.5)), 3), round(float(np.percentile(out, 97.5)), 3)) if out else (None, None)
    return dict(rate_a=float(ra), rate_b=float(rb), ratio=(float(rb / ra) if ra > 0 else None), ci=q)


# ------------------------------------------------------------------------------------------------ M1 assays
def m1_table():
    rows = []
    for f in sorted(glob.glob(os.path.join(OUT, 'assay_m1_*.json.gz'))):
        rows += json.load(gzip.open(f))
    agg = defaultdict(lambda: dict(n=0, est=0, take=0, fix=0, t_take=[]))
    for r in rows:
        k = (r['lab'], r['inj'], r['N'])
        for (rep, g_est, g_take, g_fix, g_lost, mx, g) in r['rows']:
            a = agg[k]
            took = g_take >= 0 or g_fix >= 0                  # fixation ends the replicate before the 25-generation hold
            a['n'] += 1; a['est'] += int(g_est >= 0); a['take'] += int(took); a['fix'] += int(g_fix >= 0)
            if took: a['t_take'].append(g_take if g_take >= 0 else g_fix)
    out = {}
    for (lab, inj, N), a in sorted(agg.items()):
        out['%s|%s|%d' % (lab, inj, N)] = dict(lab=lab, inj=inj, N=N, n=a['n'], est=a['est'] / a['n'],
                                               take=a['take'] / a['n'], take_ci=cp(a['take'], a['n']),
                                               fix=a['fix'] / a['n'], median_t_take=(float(np.median(a['t_take']))
                                                                                      if a['t_take'] else None))
    return out


def m1_composite(m1, LS=None):
    """P(takeover | holder) per N, weighted over the Q trees by prior mass; pooled per class (mean over holders)."""
    import provenance_run as PR
    import identity_resistant as IRM
    LS = LS or PR.lot_static()
    reps = IRM.q_reps(LS); w = IRM.q_tree_weights(LS)
    per = {}
    for key, v in m1.items():
        if v['inj'] == 'C': continue
        per.setdefault((v['lab'], v['N']), {})[v['inj']] = v['take']
    comp = {}
    for (lab, N), d in per.items():
        if all(q in d for q in reps):
            comp['%s|%d' % (lab, N)] = float(sum(wi * d[q] for wi, q in zip(w, reps)))
    pooled = {}
    for N in sorted(set(int(k.split('|')[1]) for k in comp)):
        for cls in ('ex', 'res'):
            xs = [v for k, v in comp.items() if k.startswith(cls + '_') and int(k.split('|')[1]) == N]
            if xs: pooled['%s|%d' % (cls, N)] = float(np.mean(xs))
    return comp, pooled


def kappa(rows, pooled):
    """Composite per identity arrival for each run: sum over identity arrivals of P(takeover | holder class)."""
    out = []
    for r in rows:
        k = 0.0
        for q in r['identity_arrivals']:
            if q['status'] != 1: continue
            N = 800                                  # M1 ran at 200 and 800; both rain sizes (800, 1,600) use 800
            k += pooled.get('%s|%d' % (q['x_cls'] or 'res', N), 0.0)
        out.append(k)
    return out


# ------------------------------------------------------------------------------------------------ parts
def part_I(rows):
    cells = defaultdict(list)
    for r in rows:
        if r['part'] == 'I': cells[(r['prior'], r['spon'])].append(r)
    out = {}
    for (prior, spon), rs in sorted(cells.items()):
        rs.sort(key=lambda r: r['rep'])
        f = [r['final'] for r in rs]
        pre = [r['pre'] for r in rs]
        est = defaultdict(lambda: [0, 0, 0])
        for p in pre:
            for k, v in p['est'].items():
                est[k][0] += v['copies']; est[k][1] += v['held_own']; est[k][2] += v['islands_seeded']
        drift_away = [dict(rep=r['rep'], h_sp=r['final']['h_sp'], T=r['final']['T_share']) for r in rs
                      if r['final']['uo'] and not r['final']['uot235']]
        out['%s|%s' % (prior, 'spon' if spon else 'snon')] = dict(
            n=len(rs), reps=[r['rep'] for r in rs],
            uo=sum(x['uo'] for x in f), uot235=sum(x['uot235'] for x in f), uot70=sum(x['uot70'] for x in f),
            lost=sum(x['lost'] for x in f), univ=sum(x['universal'] for x in f),
            uot_neq=sum(1 for x in f if x['uot235'] != x['uot70']),
            ex_share_max=max(x['ex_share'] for x in f), ex_share_mean=float(np.mean([x['ex_share'] for x in f])),
            res_share_mean=float(np.mean([x['res_share'] for x in f])), T_share_mean=float(np.mean([x['T_share'] for x in f])),
            ident_final_max=max(x['ident'] for x in f), max_ident_after=max(r['max_ident_after'] for r in rs),
            pre_identity=sum(p['identity'] for p in pre), pre_tgt_res=sum(p['tgt_res'] for p in pre),
            pre_tgt_ex=sum(p['tgt_ex'] for p in pre), pre_closed_open=sum(p['closed_open'] for p in pre),
            pre_exploitable=sum(p['exploitable'] for p in pre), pre_unheld=sum(p['unheld'] for p in pre),
            pre_islands=sum(len(p['labels']) for p in pre),
            est={k: dict(copies=v[0], held_own=v[1], per_copy=(v[1] / v[0] if v[0] else None),
                         islands_seeded=v[2]) for k, v in est.items()},
            drift_away=drift_away, seeded={k: sum(r['seeded'].get(k, 0) for r in rs) / len(rs)
                                           for k in ('Q', 'E', 'Res', 'UC', 'other')},
            uo_list=[x['uo'] for x in f], uot_list=[x['uot235'] for x in f], uot70_list=[x['uot70'] for x in f])
    return out


def part_II(rows):
    cells = defaultdict(list)
    for r in rows:
        if r['part'] == 'II': cells[(r['prior'], r['spon'])].append(r)
    out = {}
    for (prior, spon), rs in sorted(cells.items()):
        rs.sort(key=lambda r: r['rep'])
        d = dict(n=len(rs), reps=[r['rep'] for r in rs])
        for g in ('200', '2000', '10000'):
            s = [r['snaps'].get(g, {}) for r in rs]
            d[g] = dict(uot=sum(bool(x.get('uot')) for x in s), uot70=sum(bool(x.get('uot70')) for x in s),
                        uo=sum(bool(x.get('uo')) for x in s), identity=sum(x.get('identity', 0) for x in s),
                        closed_open=sum(x.get('closed_open', 0) for x in s),
                        exploitable=sum(x.get('exploitable', 0) for x in s),
                        unheld=sum(x.get('unheld', 0) for x in s), tgt_res=sum(x.get('tgt_res', 0) for x in s),
                        tgt_ex=sum(x.get('tgt_ex', 0) for x in s), eff=sum(x.get('eff', 0) for x in s),
                        runs_with_identity=sum(1 for x in s if x.get('identity', 0) > 0),
                        uot_list=[bool(x.get('uot')) for x in s], uo_list=[bool(x.get('uo')) for x in s])
            if g in ('200', '2000'):
                est = defaultdict(lambda: [0, 0, 0])
                for x in s:
                    for k, v in (x.get('est') or {}).items():
                        est[k][0] += v['copies']; est[k][1] += v['held_own']; est[k][2] += v['islands_seeded']
                d[g]['est'] = {k: dict(copies=v[0], held_own=v[1], per_copy=(v[1] / v[0] if v[0] else None))
                               for k, v in est.items()}
        d['identity_takeovers'] = sum(len(r['identity_takeovers']) for r in rs)
        d['drift_away'] = [dict(rep=r['rep'], holders=sorted(set(r['snaps']['10000']['holder_sp'])))
                           for r in rs if r['snaps'].get('10000', {}).get('uo') and not r['snaps']['10000']['uot']]
        out['%s|%s' % (prior, 'spon' if spon else 'snon')] = d
    return out


def part_III(rows, pooled):
    cells = defaultdict(list)
    for r in rows:
        if r['part'] == 'III': cells[(r['sched'], r['prior'], r['N'])].append(r)
    out = {}
    for (sched, prior, N), rs in sorted(cells.items()):
        rs.sort(key=lambda r: r['rep'])
        qa = [q for r in rs for q in r['identity_arrivals']]
        idt = [z for r in rs for z in r['identity_takeovers']]
        tig = Counter(); ds = Counter(); ex = Counter()
        for r in rs:
            tig.update(r['tgt_island_gens']); ds.update(r['drift_split']); ex.update(r['exposure'])
        s_end = [r['snaps'].get(str(r['gens']), {}) for r in rs]
        s_on = [r['snaps'].get('200', {}) for r in rs]
        drift = [sum(1 for c in r['colonizations'] if c['cls'] != 'selected') for r in rs]
        drift_tgt = [sum(1 for c in r['colonizations'] if c['cls'] != 'selected' and c['status_at_arrival'] == 1)
                     for r in rs]
        out['%s|%s|%d' % (sched, prior, N)] = dict(
            n=len(rs), reps=[r['rep'] for r in rs], arrivals=sum(r['arrivals_total'] for r in rs),
            exposure=dict(ex), identity_arrivals=len(qa),
            identity_arrivals_by=dict(Counter('%s|%s|%s' % (q['status'], q['x_cls'], q['cls']) for q in qa)),
            identity_takeovers=len(idt), idt_by=dict(Counter('%s|%s' % (z['attr'], z['holder_cls']) for z in idt)),
            prey=sum(1 for z in idt if z['attr'] == 'prey'), idt_permanent=sum(1 for z in idt if z['permanent']),
            tgt_island_gens=dict(tig), drift_split=dict(ds), drift=sum(drift), drift_tgt=sum(drift_tgt),
            uot=sum(bool(x.get('uot')) for x in s_end), uot70=sum(bool(x.get('uot70')) for x in s_end),
            uo=sum(bool(x.get('uo')) for x in s_end), identity_end=sum(x.get('identity', 0) for x in s_end),
            identity_onset=sum(x.get('identity', 0) for x in s_on),
            tgt_res_end=sum(x.get('tgt_res', 0) for x in s_end), tgt_ex_end=sum(x.get('tgt_ex', 0) for x in s_end),
            unheld_end=sum(x.get('unheld', 0) for x in s_end), eff_end=sum(x.get('eff', 0) for x in s_end),
            islands=sum(r['I'] for r in rs), secondary=sum(len(r['secondary']) for r in rs),
            kappa=float(sum(kappa(rs, pooled))),
            per_run=dict(q=[len(r['identity_arrivals']) for r in rs],
                         prey=[sum(1 for z in r['identity_takeovers'] if z['attr'] == 'prey') for r in rs],
                         idt=[len(r['identity_takeovers']) for r in rs], kappa=kappa(rs, pooled),
                         uot=[bool(x.get('uot')) for x in s_end], drift=drift, drift_tgt=drift_tgt,
                         uc_drift=[sum(v for k, v in r['drift_split'].items() if k.endswith('>UC')) for r in rs],
                         tig=[sum(r['tgt_island_gens'].values()) for r in rs],
                         ident_end=[x.get('identity', 0) for x in s_end]))
    return out


def main():
    res = {}
    m1 = m1_table()
    comp, pooled = m1_composite(m1) if m1 else ({}, {})
    res['m1'] = m1; res['m1_composite'] = comp; res['m1_pooled'] = pooled
    rows = load()
    res['I'] = part_I(rows)
    res['II'] = part_II(rows)
    res['III'] = part_III(rows, pooled)
    # paired comparisons
    cmp_ = {}
    for part, key in (('I', 'uot_list'), ('I', 'uo_list'), ('I', 'uot70_list')):
        for spon in ('snon', 'spon'):
            a = res['I'].get('L|' + spon)
            for p in ('Rm', 'Rp'):
                b = res['I'].get('%s|%s' % (p, spon))
                if a and b and a['reps'] == b['reps']:
                    cmp_['I|%s|%s|%s' % (key, spon, p)] = mcnemar(a[key], b[key])
        for p in ('L', 'Rm', 'Rp'):
            a = res['I'].get(p + '|snon'); b = res['I'].get(p + '|spon')
            if a and b and a['reps'] == b['reps']:
                cmp_['I|%s|spon-vs-snon|%s' % (key, p)] = mcnemar(a[key], b[key])
    for g in ('2000', '10000'):
        for spon in ('snon', 'spon'):
            a = res['II'].get('L|' + spon)
            for p in ('Rm', 'Rp'):
                b = res['II'].get('%s|%s' % (p, spon))
                if a and b and a['reps'] == b['reps']:
                    cmp_['II|uot%s|%s|%s' % (g, spon, p)] = mcnemar(a[g]['uot_list'], b[g]['uot_list'])
        for p in ('L', 'Rm', 'Rp'):
            a = res['II'].get(p + '|snon'); b = res['II'].get(p + '|spon')
            if a and b and a['reps'] == b['reps']:
                cmp_['II|uot%s|spon-vs-snon|%s' % (g, p)] = mcnemar(a[g]['uot_list'], b[g]['uot_list'])
    for sched in ('ann', 'const'):
        for N in (800, 1600):
            a = res['III'].get('%s|L|%d' % (sched, N))
            for p in ('Rm', 'Rp'):
                b = res['III'].get('%s|%s|%d' % (sched, p, N))
                if a and b and a['reps'] == b['reps']:
                    cmp_['III|uot|%s|%d|%s' % (sched, N, p)] = mcnemar(a['per_run']['uot'], b['per_run']['uot'])
    res['paired'] = cmp_
    # rates (pooled over schedules, and over N where both priors ran)
    rates = {}

    def pool(prior, Ns):
        keys = ['%s|%s|%d' % (s, prior, N) for s in ('ann', 'const') for N in Ns]
        ks = [k for k in keys if k in res['III']]
        pr = defaultdict(list)
        for k in ks:
            for f, v in res['III'][k]['per_run'].items(): pr[f] += v
        return pr, ks

    for Ns, tag in (((800, 1600), 'both'), ((800,), '800'), ((1600,), '1600')):
        L_, kl = pool('L', Ns)
        for p in ('Rm', 'Rp'):
            P_, kp = pool(p, Ns)
            if not P_ or len(P_['q']) != len(L_['q']): continue
            rates['%s|%s' % (tag, p)] = dict(
                prey_per_arrival=boot_ratio(L_['prey'], L_['q'], P_['prey'], P_['q']),
                idt_per_arrival=boot_ratio(L_['idt'], L_['q'], P_['idt'], P_['q']),
                idt_total=dict(L=int(sum(L_['idt'])), X=int(sum(P_['idt']))),
                prey_total=dict(L=int(sum(L_['prey'])), X=int(sum(P_['prey']))),
                kappa=boot_ratio(L_['kappa'], L_['q'], P_['kappa'], P_['q']),
                drift_tgt_per_tig=boot_ratio(L_['drift_tgt'], L_['tig'], P_['drift_tgt'], P_['tig']),
                uc_drift_per_tig=boot_ratio(L_['uc_drift'], L_['tig'], P_['uc_drift'], P_['tig']),
                ident_end=dict(L=int(sum(L_['ident_end'])), X=int(sum(P_['ident_end']))),
                q_arrivals=dict(L=int(sum(L_['q'])), X=int(sum(P_['q']))))
    res['rates'] = rates
    json.dump(res, open(os.path.join(ROOT, 'runs', 'identity-resistant.json'), 'w'), indent=1, default=str)
    show(res)


def show(res):
    print('== M1 composite', json.dumps(res['m1_composite']), json.dumps(res['m1_pooled']))
    for k, v in res['m1'].items():
        print('M1', k, 'n %d est %.3f take %.4f %s fix %.4f t %s' % (v['n'], v['est'], v['take'], v['take_ci'], v['fix'],
                                                                    v['median_t_take']))
    print('== Part I')
    for k, v in res['I'].items():
        print(k, {kk: vv for kk, vv in v.items() if kk not in ('uo_list', 'uot_list', 'uot70_list', 'reps', 'est', 'drift_away')})
        print('   est', {kk: (vv['copies'], vv['held_own'], None if vv['per_copy'] is None else round(vv['per_copy'], 4)) for kk, vv in v['est'].items()})
        print('   drift away', v['drift_away'])
    print('== Part II')
    for k, v in res['II'].items():
        for g in ('200', '2000', '10000'):
            print(k, g, {kk: vv for kk, vv in v[g].items() if kk not in ('uot_list', 'uo_list', 'est')})
            if 'est' in v[g]:
                print('   est', {kk: (vv['copies'], vv['held_own'], None if vv['per_copy'] is None else round(vv['per_copy'], 4)) for kk, vv in v[g]['est'].items()})
        print('  ', k, 'idt', v['identity_takeovers'], 'drift away', v['drift_away'][:5])
    print('== Part III')
    for k, v in res['III'].items():
        print(k, {kk: vv for kk, vv in v.items() if kk not in ('per_run', 'reps')})
    print('== paired')
    for k, v in res['paired'].items(): print(k, v)
    print('== rates')
    for k, v in res['rates'].items(): print(k, json.dumps(v))


if __name__ == '__main__':
    main()
