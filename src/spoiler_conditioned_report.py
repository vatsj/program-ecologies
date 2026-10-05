"""Report for src/spoiler_conditioned.py: runs/spoiler-conditioned.md and runs/spoiler-conditioned.json."""
import gzip, json, math, os, sys
from collections import defaultdict, Counter
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import spoiler_conditioned as S

OUT_MD = os.path.join(S.RUNS, 'spoiler-conditioned.md')
OUT_JS = os.path.join(S.RUNS, 'spoiler-conditioned.json')
B = 2000
CELLS = ('i', 'ii', 'iii', 'iv')
MEAS = (('coop', 'coop_fix'), ('surv', 'target_surv'), ('eff', 'efficient'))
F = {f: i for i, f in enumerate(S.FRC_FIELDS)}


def wilson(k, n, z=1.96):
    if n == 0:
        return (float('nan'),) * 3
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return p, max(0.0, c - h), min(1.0, c + h)


def fmt_w(k, n):
    p, lo, hi = wilson(k, n)
    return '%.3f [%.3f, %.3f] (%d/%d)' % (p, lo, hi, k, n) if n else 'n/a'


def boot_ratio(x1, x0, rng, b=B):
    """ratio mean(x1)/mean(x0), independent resamples; returns point, lo, hi."""
    x1 = np.asarray(x1, float); x0 = np.asarray(x0, float)
    if len(x1) == 0 or len(x0) == 0 or x0.mean() == 0:
        return (float('nan'),) * 3
    r = []
    for _ in range(b):
        a = x1[rng.integers(0, len(x1), len(x1))].mean(); c = x0[rng.integers(0, len(x0), len(x0))].mean()
        r.append(a / c if c > 0 else np.nan)
    r = np.array(r); r = r[np.isfinite(r)]
    return float(x1.mean() / x0.mean()), float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5))


def boot_paired(xa, xb, rng, b=B):
    """paired over backgrounds: difference mean(a) - mean(b) and relative reduction 1 - mean(b)/mean(a)."""
    xa = np.asarray(xa, float); xb = np.asarray(xb, float); n = len(xa)
    d0 = xa.mean() - xb.mean(); r0 = 1 - xb.mean() / xa.mean() if xa.mean() > 0 else float('nan')
    ds, rs = [], []
    for _ in range(b):
        idx = rng.integers(0, n, n)
        a = xa[idx].mean(); c = xb[idx].mean()
        ds.append(a - c)
        if a > 0: rs.append(1 - c / a)
    return (float(d0), float(np.percentile(ds, 2.5)), float(np.percentile(ds, 97.5)),
            float(r0), float(np.percentile(rs, 2.5)) if rs else float('nan'), float(np.percentile(rs, 97.5)) if rs else float('nan'))


def load():
    nat = json.load(gzip.open(S.ROWS_NAT, 'rt'))
    frc = json.load(gzip.open(S.ROWS_FRC, 'rt'))
    T = json.load(open(S.TABLES))
    return nat, frc, T


def next_row(flog, tC):
    """first 20-generation log row strictly after tC (row j is generation 20 j); the last stored row if the log ends."""
    j = int(math.floor(tC / S.EVERY)) + 1
    return flog[min(j, len(flog) - 1)]


def main():
    nat, frc, T = load()
    rng = np.random.default_rng(20261005)
    md = []; js = dict(tables={}, natural={}, forced={}, heldout={}, logs={})
    P = lambda *a: md.append(' '.join(str(x) for x in a))

    # ---------------------------------------------------------------- payoff tables
    P('# Spoiler-conditioned establishment (`src/spoiler_conditioned.py`)\n')
    P('Spec `specs/2026-10-05-spoiler-conditioned.md`; predictions `predictions/2026-10-05-spoiler-conditioned.md`.')
    P('Modal arm, PD, w = 0.3, ε = 0, single islands, no migration, horizon 10⁵, iid seeds from the length prior at cutoff n.\n')
    P('## 1. Payoff tables and the faker\'s play against D\n')
    P('Rows/columns: target, faker, D, ALLC; entry = row\'s payoff. Profile types: *disadvantaged* (faker cooperates with D), '
      '*neutral* (defects on D and on itself), *advantaged* (defects on D, cooperates with itself = establisher).\n')
    P('| n | targets (μ ≥ 1e-4) | (target, faker) pairs | faker mass: disadvantaged / neutral / advantaged |')
    P('|---|---|---|---|')
    for n in S.NS:
        t = T[str(n)]; fp = t['faker_profile']
        P('| %d | %d | %d | %.4f / %.4f / %.4f |' % (n, t['n_targets'], t['n_pairs'], fp.get('disadvantaged', {}).get('mass', 0),
                                                fp.get('neutral', {}).get('mass', 0), fp.get('advantaged', {}).get('mass', 0)))
        js['tables'][n] = dict(faker_profile=fp, targets=t['targets'], forced=[(r['target'], r['faker'], r['faker_vs_D'], r['table']) for r in t['forced']])
    P('\nForced pairs (same six at every n, plus supplement S):\n')
    for r in S.forced_pairs(12):
        P('- `%s` ← `%s`: %s against D; faker est %s; table %s' % (r['target'], r['faker'], r['faker_vs_D'], r['faker_is_est'], r['table']))

    # ---------------------------------------------------------------- natural seeds
    P('\n## 2. Natural seeds: four disjoint cells (given an establisher present)\n')
    P('Establishment = cooperative fixation unless stated. Wilson 95% intervals; d = (ii)/(i), bootstrap 95% interval.\n')
    for N in S.NS_N:
        for n in S.NS:
            rows = [r for r in nat if r['n'] == n and r['N'] == N]
            cen = [r for r in rows if not r['resolved']]
            res = [r for r in rows if r['resolved']]
            key = '%d,%d' % (n, N)
            out = dict(islands=len(rows), censored=len(cen), cells={})
            cnt = Counter(r['cell'] for r in rows)
            P('### n = %d, N = %d: %d islands, %d censored; P(A) = %.3f; cells %s' % (n, N, len(rows), len(cen),
              1 - cnt['noA'] / len(rows), ', '.join('%s %d' % (c, cnt[c]) for c in ('noA',) + CELLS)))
            P('\n| cell | islands | coop fixation | target survival | efficiency | winner: target / other est / faker / D / other |')
            P('|---|---|---|---|---|---|')
            for c in ('noA',) + CELLS:
                rr = [r for r in res if r['cell'] == c]
                wc = Counter(r['winner_cat'] for r in rr)
                cell = dict(n=len(rr), **{m: sum(r[f] for r in rr) for m, f in MEAS}, winners=dict(wc))
                out['cells'][c] = cell
                P('| %s | %d | %s | %s | %s | %d / %d / %d / %d / %d |' % (c, len(rr), fmt_w(cell['coop'], len(rr)), fmt_w(cell['surv'], len(rr)),
                  fmt_w(cell['eff'], len(rr)), wc['target'], wc['other establisher'], wc['faker'], wc['D'], wc['other'] + wc['ALLC']))
            for m, f in MEAS:
                x1 = [r[f] for r in res if r['cell'] == 'ii']; x0 = [r[f] for r in res if r['cell'] == 'i']
                x3 = [r[f] for r in res if r['cell'] == 'iii']; x4 = [r[f] for r in res if r['cell'] == 'iv']
                out['d_' + m] = boot_ratio(x1, x0, rng)
                out['r3_' + m] = boot_ratio(x3, x0, rng)
                out['r4_' + m] = boot_ratio(x4, x0, rng)
            P('\nd (ii)/(i): coop %.3f [%.3f, %.3f]; survival %.3f [%.3f, %.3f]; efficiency %.3f [%.3f, %.3f]' % (out['d_coop'] + out['d_surv'] + out['d_eff']))
            P('(iii)/(i): coop %.3f [%.3f, %.3f]; survival %.3f [%.3f, %.3f].  (iv)/(i): coop %.3f [%.3f, %.3f]' % (out['r3_coop'] + out['r3_surv'] + out['r4_coop']))
            # cell ii split by faker profile
            sp = {}
            for lab, pred in (('disadvantaged only', lambda r: r['fk_profiles'] == ['disadvantaged']),
                              ('neutral present', lambda r: 'neutral' in r['fk_profiles'])):
                rr = [r for r in res if r['cell'] == 'ii' and pred(r)]
                sp[lab] = dict(n=len(rr), coop=sum(r['coop_fix'] for r in rr), surv=sum(r['target_surv'] for r in rr),
                               d=boot_ratio([r['coop_fix'] for r in rr], [r['coop_fix'] for r in res if r['cell'] == 'i'], rng))
            out['ii_by_profile'] = sp
            P('cell (ii) by faker profile: ' + '; '.join('%s: %d islands, coop %s, d %.3f [%.3f, %.3f]' % (
                k, v['n'], fmt_w(v['coop'], v['n']), *v['d']) for k, v in sp.items()))
            # strata: primary target identity and target count
            strata = defaultdict(lambda: defaultdict(list))
            for r in res:
                if r['cell'] not in ('i', 'ii'): continue
                tgt = max(r['targets'], key=lambda k: r['targets'][k])
                nt = sum(r['targets'].values()); nb = '1' if nt == 1 else ('2' if nt == 2 else '3+')
                strata[(tgt, nb)][r['cell']].append(r['coop_fix'])
            st = []
            for (tgt, nb), v in sorted(strata.items(), key=lambda kv: -len(kv[1]['ii'])):
                if len(v['i']) >= 50 and len(v['ii']) >= 50:
                    st.append((tgt, nb, len(v['i']), float(np.mean(v['i'])), len(v['ii']), float(np.mean(v['ii'])),
                               boot_ratio(v['ii'], v['i'], rng)))
            pooled_i = sum(len(v['i']) for (k, v) in strata.items()); pooled_ii = sum(len(v['ii']) for (k, v) in strata.items())
            out['strata'] = st
            if st:
                P('strata with ≥ 50 islands in both (i) and (ii) (primary target, target copies): ' + '; '.join(
                    '`%s` ×%s: (i) %.3f n=%d, (ii) %.3f n=%d, d %.2f [%.2f, %.2f]' % (s[0], s[1], s[3], s[2], s[5], s[4], *s[6]) for s in st))
            else:
                P('no stratum reaches 50 islands in both (i) and (ii); pooled only')
            # scramble: in cell ii, fakers extinct by ALLC extinction (catC faker count 0)
            rr = [r for r in res if r['cell'] == 'ii' and r['tC'] >= 0]
            for lab, pred in (('disadvantaged only', lambda r: r['fk_profiles'] == ['disadvantaged']),
                              ('neutral present', lambda r: 'neutral' in r['fk_profiles'])):
                q = [r for r in rr if pred(r)]
                if q:
                    k = sum(r['catC'][1] == 0 for r in q)
                    out.setdefault('faker_dead_at_tC', {})[lab] = (k, len(q))
            P('cell (ii): faker extinct by the island\'s ALLC extinction: ' + '; '.join('%s %s' % (k, fmt_w(*v)) for k, v in out.get('faker_dead_at_tC', {}).items()))
            P('')
            js['natural'][key] = out

    # ---------------------------------------------------------------- held-out decomposition
    P('## 3. Held-out decomposition\n')
    P('p = P(noA) P(est | noA) + P(A) Σ_cells P(cell | A) P(est | cell), fitted on reps 0–1,999, compared with the measured p '
      'on reps 2,000–3,999 (censored islands excluded). "transport" uses the held-out cell composition with the fitted rates.\n')
    P('| n | N | measure | fitted p | held-out p | rel. error | transport | rel. error |')
    P('|---|---|---|---|---|---|---|---|')
    for N in S.NS_N:
        for n in S.NS:
            for m, f in MEAS:
                rows = [r for r in nat if r['n'] == n and r['N'] == N and r['resolved']]
                tr = [r for r in rows if r['rep'] < 2000]; te = [r for r in rows if r['rep'] >= 2000]
                rate = {c: (np.mean([r[f] for r in tr if r['cell'] == c]) if any(r['cell'] == c for r in tr) else 0.0) for c in ('noA',) + CELLS}
                comp_tr = {c: np.mean([r['cell'] == c for r in tr]) for c in ('noA',) + CELLS}
                comp_te = {c: np.mean([r['cell'] == c for r in te]) for c in ('noA',) + CELLS}
                pf = sum(comp_tr[c] * rate[c] for c in rate); pt = sum(comp_te[c] * rate[c] for c in rate)
                pm = np.mean([r[f] for r in te])
                js['heldout']['%d,%d,%s' % (n, N, m)] = dict(fit=pf, transport=pt, held=pm, err=pf / pm - 1, err_t=pt / pm - 1)
                P('| %d | %d | %s | %.4f | %.4f | %+.1f%% | %.4f | %+.1f%% |' % (n, N, m, pf, pm, 100 * (pf / pm - 1), pt, 100 * (pt / pm - 1)))

    # ---------------------------------------------------------------- forced seeds
    P('\n## 4. Forced seeds: paired target–faker insertions\n')
    P('(a) target ×k; (b) target ×k + faker ×k; (c) target ×k + k more of the target class; (cD) target ×k + D ×k; (d) faker ×k. '
      'Same background, slots and simulation seed. Relative reduction = 1 − P(b)/P(a); paired bootstrap over 1,000 backgrounds.\n')
    for N in S.NS_N:
        P('### N = %d\n' % N)
        P('| n | pair | type | k | surv a / b / c / cD | coop a / b / cD | (a)−(b) surv | rel. red. surv | rel. red. coop | (a)−(cD) surv | d: faker in support / largest | (b) winner: target / faker / other est / D |')
        P('|---|---|---|---|---|---|---|---|---|---|---|---|')
        for n in S.NS:
            pl = S.forced_pairs(n)
            for pi, pr in enumerate(pl):
                rows = [r for r in frc if r['n'] == n and r['N'] == N and r['pair'] == pi]
                for k in S.DOSES[N]:
                    g = lambda tr, fld: np.array([r['out']['%s%d' % (tr, k)][F[fld]] for r in rows], float)
                    ok = np.ones(len(rows), bool)
                    for tr in S.TREAT: ok &= g(tr, 'resolved') == 1
                    v = {tr: {m: g(tr, fld)[ok] for m, fld in (('surv', 'target_surv'), ('fsurv', 'faker_surv'), ('coop', 'coop_fix'), ('eff', 'efficient'))} for tr in S.TREAT}
                    ab_s = boot_paired(v['a']['surv'], v['b']['surv'], rng)
                    ab_c = boot_paired(v['a']['coop'], v['b']['coop'], rng)
                    acd = boot_paired(v['a']['surv'], v['cD']['surv'], rng)
                    ac = boot_paired(v['a']['surv'], v['c']['surv'], rng)
                    wb = Counter(r['out']['b%d' % k][F['winner_cat']] for r, o in zip(rows, ok) if o)
                    wd = Counter(r['out']['d%d' % k][F['winner_cat']] for r, o in zip(rows, ok) if o)
                    dl = sum(wd[c] for c in ('faker',)) / ok.sum()
                    rec = dict(n=n, N=N, pair=(pr['target'], pr['faker']), type=pr['faker_vs_D'], k=k, backgrounds=int(ok.sum()), censored=int((~ok).sum()),
                               rates={tr: {m: float(x.mean()) for m, x in v[tr].items()} for tr in S.TREAT},
                               ab_surv=ab_s, ab_coop=ab_c, a_cD=acd, a_c=ac, b_winners=dict(wb), d_winners=dict(wd), d_faker_largest=dl)
                    js['forced']['%d,%d,%d,%d' % (n, N, pi, k)] = rec
                    lab = ('S ' if pi == S.NPAIRS else '%d ' % pi) + '`%s` ← `%s`' % (pr['target'], pr['faker'])
                    P('| %d | %s | %s | %d | %.3f / %.3f / %.3f / %.3f | %.3f / %.3f / %.3f | %+.3f [%+.3f, %+.3f] | %.2f [%.2f, %.2f] | %.2f [%.2f, %.2f] | %+.3f [%+.3f, %+.3f] | %.3f / %.3f | %d / %d / %d / %d |' % (
                        n, lab, pr['faker_vs_D'][:5], k, v['a']['surv'].mean(), v['b']['surv'].mean(), v['c']['surv'].mean(), v['cD']['surv'].mean(),
                        v['a']['coop'].mean(), v['b']['coop'].mean(), v['cD']['coop'].mean(),
                        ab_s[0], ab_s[1], ab_s[2], ab_s[3], ab_s[4], ab_s[5], ab_c[3], ab_c[4], ab_c[5], acd[0], acd[1], acd[2],
                        v['d']['fsurv'].mean(), dl, wb['target'], wb['faker'], wb['other establisher'], wb['D']))
        P('')

    # ---------------------------------------------------------------- frequency logs
    P('## 5. Frequency logs around ALLC extinction\n')
    P('(b) islands, k = 1 unless stated. tC = the island\'s first ALLC extinction. "Mechanism" = faker count falls and target count rises '
      'from tC to the next 20-generation row, among islands where the target survives. P(surv | state at tC) splits the target\'s '
      'survival into the scramble (alive at tC) and the post-scramble race.\n')
    P('| n | N | pair type | k | (b) islands | target alive at tC | faker alive at tC | P(surv \\| both alive at tC) | P(surv \\| target alive, faker dead) | (a): P(surv \\| target alive at tC) | mechanism holds / target survives |')
    P('|---|---|---|---|---|---|---|---|---|---|---|')
    for N in S.NS_N:
        for n in S.NS:
            pl = S.forced_pairs(n)
            for typ in ('disadvantaged', 'neutral', 'advantaged'):
                for k in S.DOSES[N]:
                    pis = [i for i, p in enumerate(pl) if p['faker_vs_D'] == typ]
                    rows = [r for r in frc if r['n'] == n and r['N'] == N and r['pair'] in pis]
                    bs = [r['out']['b%d' % k] for r in rows]
                    bs = [b for b in bs if b[F['resolved']] and b[F['tC']] >= 0]
                    as_ = [r['out']['a%d' % k] for r in rows]
                    as_ = [a for a in as_ if a[F['resolved']] and a[F['tC']] >= 0]
                    ta = [b for b in bs if b[F['catC']][0] > 0]
                    both = [b for b in ta if b[F['catC']][1] > 0]
                    only = [b for b in ta if b[F['catC']][1] == 0]
                    a_al = [a for a in as_ if a[F['catC']][0] > 0]
                    sv = [b for b in bs if b[F['target_surv']]]
                    mech = 0
                    for b in sv:
                        row = next_row(b[F['flog']], b[F['tC']])
                        if row[1] < b[F['catC']][1] and row[0] > b[F['catC']][0]:
                            mech += 1
                    rec = dict(islands=len(bs), t_alive=len(ta), both=len(both), surv_both=sum(b[F['target_surv']] for b in both),
                               only=len(only), surv_only=sum(b[F['target_surv']] for b in only), a_alive=len(a_al),
                               a_surv_alive=sum(a[F['target_surv']] for a in a_al), mech=mech, surv=len(sv),
                               fk_at_tC_mean=float(np.mean([b[F['catC']][1] for b in ta])) if ta else None,
                               tg_at_tC_mean=float(np.mean([b[F['catC']][0] for b in ta])) if ta else None)
                    js['logs']['%d,%d,%s,%d' % (n, N, typ, k)] = rec
                    P('| %d | %d | %s | %d | %d | %d (mean %.1f copies) | %d (mean %.1f) | %s | %s | %s | %d / %d |' % (
                        n, N, typ[:5], k, len(bs), len(ta), rec['tg_at_tC_mean'] or 0, len(both), rec['fk_at_tC_mean'] or 0,
                        fmt_w(rec['surv_both'], len(both)), fmt_w(rec['surv_only'], len(only)), fmt_w(rec['a_surv_alive'], len(a_al)), mech, len(sv)))
    # natural cell (ii)/(iii) logs: target and faker counts at tC
    P('\nNatural islands, cells (ii)–(iv): target and faker copies at t = 0 and at tC (means), and target survival given faker alive at tC.\n')
    P('| n | N | cell | islands | target t=0 / tC | faker t=0 / tC | faker alive at tC | P(target surv \\| faker alive at tC, target alive) | P(target surv \\| faker dead, target alive) |')
    P('|---|---|---|---|---|---|---|---|---|')
    for N in S.NS_N:
        for n in S.NS:
            for c in ('ii', 'iii', 'iv'):
                rr = [r for r in nat if r['n'] == n and r['N'] == N and r['cell'] == c and r['resolved'] and r['tC'] >= 0]
                if not rr: continue
                fa = [r for r in rr if r['catC'][1] > 0 and r['catC'][0] > 0]
                fd = [r for r in rr if r['catC'][1] == 0 and r['catC'][0] > 0]
                P('| %d | %d | %s | %d | %.2f / %.2f | %.2f / %.2f | %d | %s | %s |' % (
                    n, N, c, len(rr), np.mean([r['cat0'][0] for r in rr]), np.mean([r['catC'][0] for r in rr]),
                    np.mean([r['cat0'][1] for r in rr]), np.mean([r['catC'][1] for r in rr]), len(fa),
                    fmt_w(sum(r['target_surv'] for r in fa), len(fa)), fmt_w(sum(r['target_surv'] for r in fd), len(fd))))
    extra(nat, frc, rng, md, js)
    open(OUT_MD, 'w').write('\n'.join(md) + '\n')
    json.dump(js, open(OUT_JS, 'w'), indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
    print('\n'.join(md))


def extra(nat, frc, rng, md, js):
    P = lambda *a: md.append(' '.join(str(x) for x in a))
    P('\n## 6. Supplementary analyses (after the run; not predeclared)\n')
    # 6a. scramble profile: the faker's play against ALLC as well as D
    P('### 6a. The faker\'s play against {D, ALLC} (the scramble profile)\n')
    P('A faker that is payoff-identical to D against both D and ALLC ("scramble-neutral": defects on D, ALLC and itself) is the only '
      'non-establisher type that does not lose to D while ALLC is present. Mass of fakers of the 8 targets by (play vs D, play vs ALLC):\n')
    js['scramble'] = {}
    for n in S.NS:
        d = S.cdata(n); V = d['V']; mu = d['mu']; iC = d['iC']; nm = d['names']
        T = np.nonzero(d['est'] & (mu >= S.MU_TARGET))[0]
        out = defaultdict(dict); per_t = {}
        for t in T:
            fq = S.fakers_of(d, t)
            sn = [q for q in fq if S.d_profile(d, q) == 'neutral' and V[q, iC] == 0]
            per_t[nm[t]] = (float(mu[fq].sum()), float(mu[sn].sum()))
            for q in fq:
                out['%s / %s' % (S.d_profile(d, q), 'defects on ALLC' if V[q, iC] == 0 else 'cooperates with ALLC')][int(q)] = float(mu[q])
        js['scramble'][n] = dict(by_type={k: (len(v), sum(v.values())) for k, v in out.items()}, per_target=per_t)
        P('- n = %d: ' % n + '; '.join('%s: %d classes, mass %.5f' % (k, len(v), sum(v.values())) for k, v in sorted(out.items())))
        P('  scramble-neutral faker mass per target: ' + ', '.join('`%s` %.1e (of %.1e)' % (k, v[1], v[0]) for k, v in per_t.items() if v[0] > 0))
    # 6b. target-matched survival in natural cells
    P('\n### 6b. Natural seeds, target-matched survival\n')
    P('For each target class x: P(x survives | x seeded, no faker of any establisher present = cell i) against P(x survives | x seeded '
      'and one of x\'s own fakers seeded, non-establisher fakers only = cell ii, x faked). Pooled over x with ≥ 30 islands in both; '
      'd_x = ratio, bootstrap interval. This removes the target-identity confound of the cell-level survival ratio.\n')
    P('| n | N | target | (i): n, surv | (ii, x faked): n, surv | d_x |')
    P('|---|---|---|---|---|---|')
    js['matched'] = {}
    for N in S.NS_N:
        for n in S.NS:
            rows = [r for r in nat if r['n'] == n and r['N'] == N and r['resolved']]
            names = Counter(x for r in rows if r['cell'] == 'ii' for x in r['targets'])
            for x, _ in names.most_common(4):
                def surv(r):
                    return not any(nm == x for nm, _ in r['ext'])      # x is tracked (a target) in both cells
                i_ = [r for r in rows if r['cell'] == 'i' and x in r['est']]
                ii_ = [r for r in rows if r['cell'] == 'ii' and x in r['targets']]
                si = [surv(r) for r in i_]; sii = [surv(r) for r in ii_]
                si = [int(v) for v in si if v is not None]; sii = [int(v) for v in sii if v is not None]
                if len(si) >= 30 and len(sii) >= 30:
                    b = boot_ratio(sii, si, rng)
                    js['matched']['%d,%d,%s' % (n, N, x)] = dict(i=(len(si), float(np.mean(si))), ii=(len(sii), float(np.mean(sii))), d=b)
                    P('| %d | %d | `%s` | %d, %.3f | %d, %.3f | %.2f [%.2f, %.2f] |' % (n, N, x, len(si), np.mean(si), len(sii), np.mean(sii), *b))
    # 6c. pair-level trend in n, matched by names, k = 1
    P('\n### 6c. Pair-level effect at k = 1 across n (relative reduction of target survival, (a) vs (b))\n')
    P('| N | pair | n = 6 | n = 9 | n = 12 | change 6 → 12 |')
    P('|---|---|---|---|---|---|')
    js['trend'] = {}
    for N in S.NS_N:
        names = [(p['target'], p['faker']) for p in S.forced_pairs(6)]
        for pr in names:
            eff = {}
            for n in S.NS:
                pi = [(p['target'], p['faker']) for p in S.forced_pairs(n)].index(pr)
                eff[n] = js['forced']['%d,%d,%d,1' % (n, N, pi)]['ab_surv'][3:]
            # bootstrap of the change: independent n
            js['trend']['%d,%s<-%s' % (N, pr[0], pr[1])] = eff
            P('| %d | `%s` ← `%s` | %.2f [%.2f, %.2f] | %.2f [%.2f, %.2f] | %.2f [%.2f, %.2f] | %+.2f |' % (
                N, pr[0], pr[1], *eff[6], *eff[9], *eff[12], eff[12][0] - eff[6][0]))
    # 6d. integrated selection through the scramble: per-copy faker survival to tC, and the decomposition
    P('\n### 6d. Integrated selection through the scramble (forced (b), target alive at tC)\n')
    P('q_k = P(faker alive at tC | target alive at tC); per-copy survival s from q_k = 1 − (1 − s)^k; harm h = P(surv | target alive, '
      'faker dead) − P(surv | both alive). Predicted relative reduction ≈ q_k · h / P(surv | target alive at tC), against the measured '
      'relative reduction in survival (which also includes the scramble itself).\n')
    P('| N | type | k | q_k (pooled n) | s | h | predicted rel. red. | measured rel. red. (mean over pairs, n) | alt. mechanism: faker 0 or falling, target rising |')
    P('|---|---|---|---|---|---|---|---|---|')
    F_ = F
    for N in S.NS_N:
        for typ in ('disadvantaged', 'neutral', 'advantaged'):
            for k in S.DOSES[N]:
                ta = both = sb = so = only = 0; alt = sv = 0; meas = []
                for n in S.NS:
                    pl = S.forced_pairs(n)
                    pis = [i for i, p in enumerate(pl) if p['faker_vs_D'] == typ]
                    for pi in pis:
                        meas.append(js['forced']['%d,%d,%d,%d' % (n, N, pi, k)]['ab_surv'][3])
                    for r in frc:
                        if r['n'] != n or r['N'] != N or r['pair'] not in pis: continue
                        b = r['out']['b%d' % k]
                        if not b[F_['resolved']] or b[F_['tC']] < 0: continue
                        if b[F_['target_surv']]:
                            sv += 1
                            row = next_row(b[F_['flog']], b[F_['tC']])
                            if (b[F_['catC']][1] == 0 or row[1] < b[F_['catC']][1]) and row[0] > b[F_['catC']][0]:
                                alt += 1
                        if b[F_['catC']][0] == 0: continue
                        ta += 1
                        if b[F_['catC']][1] > 0:
                            both += 1; sb += b[F_['target_surv']]
                        else:
                            only += 1; so += b[F_['target_surv']]
                q = both / ta; s = 1 - (1 - q) ** (1.0 / k)
                h = so / only - (sb / both if both else 0.0)
                base = (sb + so) / ta
                pred = q * h / (so / only) if only else float('nan')
                js['logs']['decomp,%d,%s,%d' % (N, typ, k)] = dict(q=q, s=s, h=h, pred=pred, meas=float(np.mean(meas)), alt=alt, surv=sv)
                P('| %d | %s | %d | %.3f (%d/%d) | %.3f | %.2f | %.2f | %.2f | %d / %d (%.2f) |' % (N, typ, k, q, both, ta, s, h, pred, np.mean(meas), alt, sv, alt / sv if sv else float('nan')))


if __name__ == '__main__':
    main()
