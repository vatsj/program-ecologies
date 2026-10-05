"""Report for src/rival_islands.py: runs/rival-islands.md and runs/rival-islands.json."""
import gzip, json, math, os, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import rival_islands as R

RUNS = R.RUNS
H = R.GENS
MARKS = (100, 1000, 10000, 100000)


def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'), float('nan'))
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def poisson_ci(k, z=1.96):
    """Exact 95% interval for a Poisson count k (chi-square via scipy)."""
    from scipy.stats import chi2
    lo = 0.0 if k == 0 else chi2.ppf(0.025, 2 * k) / 2
    hi = chi2.ppf(0.975, 2 * k + 2) / 2
    return lo, hi


def diffci(k1, n1, k2, n2):
    p1, p2 = k1 / n1, k2 / n2
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    return p1 - p2, (p1 - p2 - 1.96 * se, p1 - p2 + 1.96 * se)


def fmt_ci(k, n):
    lo, hi = wilson(k, n)
    return '%.2f [%.2f, %.2f]' % (k / n if n else float('nan'), lo, hi)


def km(times, events, marks=MARKS):
    """Kaplan-Meier survival at marks. times: event or censoring time; events: bool."""
    t = np.asarray(times, float); e = np.asarray(events, bool)
    o = np.argsort(t); t = t[o]; e = e[o]
    S = 1.0; out = {}; n = len(t); j = 0; mi = 0
    surv = []
    for idx in range(n):
        surv.append((t[idx], e[idx]))
    at_risk = n
    res = []
    for ti, ei in surv:
        if ei:
            S *= (at_risk - 1) / at_risk
        at_risk -= 1
        res.append((ti, S))
    for mk in marks:
        s = 1.0
        for ti, Si in res:
            if ti <= mk: s = Si
            else: break
        out[mk] = s
    return out


def category(r):
    h = r['held_final']
    a, b = h.get('1', 0), h.get('2', 0)
    # predeclared: unresolved = horizon reached and some island held by a class outside the tagged networks/bridge
    # (transient migrants lowering an island's P(C,C) below 0.95 do not make a run unresolved)
    if r['status'] in ('horizon-certified', 'unresolved') and h.get('0', 0) > 0:
        return 'unresolved'
    if a > 0 and b > 0: return 'both'
    if a > 0: return 'A only'
    if b > 0: return 'B only'
    return 'neither'


def loss_time(r):
    """First network loss (extinction) time and whether it happened; censored at stop_gen (or the horizon if the run
    stopped frozen with both alive, which cannot happen for a mutually-defecting pair)."""
    tA, tB = r['t_ext'][1], r['t_ext'][2]
    ev = [t for t in (tA, tB) if t >= 0]
    if ev:
        return min(ev), True
    return float(H), False


def hazard(rows):
    k = 0; T = 0.0
    for r in rows:
        t, e = loss_time(r)
        k += e; T += t
    lo, hi = poisson_ci(k)
    return k, T, k / T if T > 0 else float('nan'), lo / T if T > 0 else float('nan'), hi / T if T > 0 else float('nan')


def majority(r):
    h = r['held_final']; a, b = h.get('1', 0), h.get('2', 0)
    return 'A' if a > b else ('B' if b > a else 'tie')


def spearman(x, y):
    from scipy.stats import spearmanr
    if len(x) < 3: return float('nan')
    return float(spearmanr(x, y).correlation)


def icc(rows):
    """Intraclass correlation of X_i = local-ancestry establishment across a cell's runs."""
    I = rows[0]['I']
    S = np.array([r['n_local_est'] for r in rows], float)
    nb = rows[0]['n_bg']
    p = S.sum() / (nb * len(rows))
    if p <= 0 or p >= 1 or len(rows) < 3: return float('nan'), p
    v = S.var(ddof=1)
    return (v / (nb * p * (1 - p)) - 1) / (nb - 1), p


def main():
    out = {}
    md = []
    st = json.load(open(os.path.join(RUNS, 'rival-islands-static.json')))
    out['static'] = st
    sep = R.load('sep'); ctrl = R.load('ctrl'); nat = R.load('nat'); rule = R.load('rule')
    mp = os.path.join(RUNS, 'rival-islands-merge.json.gz')
    merge = json.load(gzip.open(mp, 'rt')) if os.path.exists(mp) else []
    md.append('# Rival networks across islands, and the mN rule (`src/rival_islands.py`)\n')
    md.append('Spec `specs/2026-10-05-rival-islands.md`; predictions `predictions/2026-10-05-rival-islands.md`. '
              'Modal arm, PD, w = 0.3, eps = 0, complete island graph, uniform replacement; generation = I*N births; '
              'horizon 1e5; migration continues after certification. Every run is in every denominator.\n')
    # ---------------------------------------------------------- static
    md.append('## 1. Static\n')
    md.append('| N | rho(DD migrant) | rho(D into FairBot) | rho(establisher into all-D) | P(fix) from k = 5 / 10 / 20 / 40 DD migrants at once |')
    md.append('|---|---|---|---|---|')
    for N, v in st['rho'].items():
        md.append('| %s | %.3g | %.3g | %.4f | %s |' % (N, v['dd_migrant'], v['D_into_FairBot'], v['est_into_D'],
                                                       ' / '.join('%.2g' % v['dd_k'][k] for k in ('5', '10', '20', '40'))))
    for n in ('9', '12'):
        v = st[n]
        md.append('\nn = %s: %d mutually-defecting establisher pairs, pair mass %.3g; rivals of the FairBot pair (cooperative, mutually '
                  'defecting with FairBot or `BOX1(THEM(ME))`): establisher mass %.3g over %d classes; expected rival establisher seeds per run '
                  'at N = 100: %s.' % (n, v['n_dd_pairs'], v['dd_pair_mass'], v['mu_rival_est'], v['n_rival_est'],
                                        ', '.join('I = %s: %.2f' % kv for kv in v['rival_seeds_per_run'].items())))
        md.append('\n| x | y | mu_x | mu_y | co-seed N = 100 |\n|---|---|---|---|---|')
        for p in v['top_pairs'][:8]:
            md.append('| `%s` | `%s` | %.3g | %.3g | %.2e |' % (p['x'], p['y'], p['mu_x'], p['mu_y'], p['co100']))
    md.append('\nItem-2 pairs (n = 9), network masses under the length prior (tag 1 = A\'s network, 2 = B\'s, 3 = bridge):\n')
    md.append('| pair | mu_A | mu_B | A net | B net | bridge | fakers of B | fakers of A |\n|---|---|---|---|---|---|---|---|')
    for i, p in enumerate(st['pairs']):
        nmass = p['net_mass']
        md.append('| %d: `%s` x `%s` | %.3g | %.3g | %.3g | %.3g | %.3g | %.3g | %.3g |' % (
            i + 1, p['A'], p['B'], p['mu_A'], p['mu_B'], nmass['1'], nmass['2'], nmass['3'], p['B_fakers_mass'], p['A_fakers_mass']))
    # ---------------------------------------------------------- item 2
    md.append('\n## 2. Separated seed (n = 9, N = 100; islands 0, 1 all-A, all-B; the rest iid)\n')
    md.append('Categories at the horizon or stop (from island holders): both / A only / B only / neither / unresolved. '
              'Hazard = first network extinctions per generation at risk (exact Poisson 95%). KM = survival of both networks.\n')
    md.append('| pair | I | mN | runs | both | A only | B only | neither | unres. | first-loss hazard [95%] | KM S(1e2) / S(1e3) / S(1e4) / S(1e5) | '
              'median loss gen | A majority | B majority | bridge-held at end | cf cross P(C,C) |')
    md.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    cellrows = defaultdict(list)
    for r in sep:
        cellrows[(r['pair'], r['I'], r['mN'])].append(r)
    item2 = {}
    for key in sorted(cellrows):
        rs = cellrows[key]; n = len(rs)
        cats = Counter(category(r) for r in rs)
        k, T, h, lo, hi = hazard(rs)
        lt = [loss_time(r) for r in rs]
        S = km([t for t, e in lt], [e for t, e in lt])
        med = np.median([t for t, e in lt if e]) if any(e for t, e in lt) else float('nan')
        maj = Counter(majority(r) for r in rs)
        bridge = np.mean([r['held_final'].get('3', 0) / r['I'] for r in rs])
        cf = np.mean([r['cf_cross_pcc'] for r in rs])
        item2[str(key)] = dict(n=n, cats=dict(cats), losses=k, exposure=T, hazard=h, hazard_ci=(lo, hi), km=S, median_loss=med,
                               A_major=maj['A'], B_major=maj['B'], tie=maj['tie'], bridge_share=bridge, cf=cf)
        md.append('| %d | %d | %g | %d | %d | %d | %d | %d | %d | %.2g [%.2g, %.2g] | %s | %s | %d | %d | %.2f | %.3f |' % (
            key[0] + 1, key[1], key[2], n, cats['both'], cats['A only'], cats['B only'], cats['neither'], cats['unresolved'],
            h, lo, hi, ' / '.join('%.2f' % S[m] for m in MARKS), '%.0f' % med if med == med else '-', maj['A'], maj['B'], bridge, cf))
    out['item2'] = item2
    # ancestry / nucleation
    md.append('\nNucleation and ancestry in the background islands (means per run): established locally by A\'s network / B\'s / bridge / '
              'other; established by immigrants (any network); never established; first immigrant-founded establishment (median gen); '
              'run-level: network with more local establishments before it (incl. its pre-seeded island) holds the majority.\n')
    md.append('| pair | I | mN | local A / B / bridge / other | immigrant A / B / bridge | none | first imm. est. | predicted-majority right / wrong / tie |')
    md.append('|---|---|---|---|---|---|---|---|')
    pred2 = Counter()
    for key in sorted(cellrows):
        rs = cellrows[key]
        es = Counter()
        for r in rs:
            for c, v in r['est_summary'].items(): es[c] += v / len(rs)
        fi = [r['first_imm_est'] for r in rs if r['first_imm_est'] >= 0]
        right = wrong = tie = 0
        for r in rs:
            a = 1 + r['local_before_first_imm'].get('tag1', 0); b = 1 + r['local_before_first_imm'].get('tag2', 0)
            m = majority(r)
            if a == b: tie += 1
            elif (a > b and m == 'A') or (b > a and m == 'B'): right += 1
            else: wrong += 1
        pred2['right'] += right; pred2['wrong'] += wrong; pred2['tie'] += tie
        md.append('| %d | %d | %g | %.1f / %.2f / %.1f / %.1f | %.1f / %.2f / %.1f | %.1f | %s | %d / %d / %d |' % (
            key[0] + 1, key[1], key[2], es['tag1/local'], es['tag2/local'], es['tag3/local'], es['other/local'] + es['main/local'] + es['rival/local'],
            es['tag1/imm'], es['tag2/imm'], es['tag3/imm'], es['tag1'] * 0 + sum(v for c, v in es.items() if '/' not in c),
            '%.0f' % np.median(fi) if fi else '-', right, wrong, tie))
    out['pred2_runlevel'] = dict(pred2)
    # ---------------------------------------------------------- controls
    md.append('\n## Controls\n')
    cc = defaultdict(list)
    for r in ctrl:
        cc[(r['preset'], r['pair'], r['I'], r['mN'], r['N'])].append(r)
    md.append('**m = 0 (A and B pre-seeded, iid background):** local establishment per background island, by network.\n')
    md.append('| pair | I | runs | p(A net) | p(B net) | p(bridge) | p(other coop) | p(none) |\n|---|---|---|---|---|---|---|---|')
    m0 = {}
    for key in sorted(k for k in cc if k[0] == 'AB'):
        rs = cc[key]; nb = sum(r['n_bg'] for r in rs)
        es = Counter()
        for r in rs:
            for c, v in r['est_summary'].items(): es[c] += v
        pA = es['tag1/local'] / nb; pB = es['tag2/local'] / nb; pbr = es['tag3/local'] / nb
        poth = sum(v for c, v in es.items() if c.endswith('/local') and c.split('/')[0] in ('other', 'main', 'rival')) / nb
        pnone = sum(v for c, v in es.items() if '/' not in c) / nb
        m0[(key[1], key[2])] = dict(pA=pA, pB=pB, pbr=pbr, nbg=rs[0]['n_bg'])
        md.append('| %d | %d | %d | %.4f | %.5f | %.4f | %.4f | %.3f |' % (key[1] + 1, key[2], len(rs), pA, pB, pbr, poth, pnone))
    out['m0'] = {str(k): v for k, v in m0.items()}
    # prediction 2: majorities vs the measured-rate predictor
    xs, ys, lines = [], [], []
    totA = totB = totT = 0
    for key in sorted(cellrows):
        p, I, mN = key
        if (p, I) not in m0: continue
        v = m0[(p, I)]
        EA = v['pA'] * v['nbg']; EB = v['pB'] * v['nbg']
        pred = (1 + EA) / (2 + EA + EB)
        rs = cellrows[key]; maj = Counter(majority(r) for r in rs)
        xs.append(pred); ys.append(maj['A'] / len(rs))
        totA += maj['A']; totB += maj['B']; totT += maj['tie']
        lines.append('| %d | %d | %g | %.3f | %.2f |' % (p + 1, I, mN, pred, maj['A'] / len(rs)))
    rho_s = spearman(xs, ys)
    ntot = totA + totB + totT
    md.append('\n**Prediction 2.** Predicted A share from the m = 0 measured local-establishment rates, (1 + E_A)/(2 + E_A + E_B), against '
              'the observed fraction of runs with an A majority; Spearman over cells = %.2f. Pooled: A majority %d / %d = %.2f, B majority %d '
              '(%.2f), ties %d. Run level: the network with more local establishments before the first immigrant-founded island held the '
              'majority in %d of %d decided runs (%.2f); %d runs undecided (equal counts).\n' % (
                  rho_s, totA, ntot, totA / ntot, totB, totB / ntot, totT, pred2['right'], pred2['right'] + pred2['wrong'],
                  pred2['right'] / max(1, pred2['right'] + pred2['wrong']), pred2['tie']))
    md.append('| pair | I | mN | predicted A share | observed A-majority fraction |\n|---|---|---|---|---|')
    md += lines
    perpair = {}
    for p in range(3):
        rs = [r for k, v in cellrows.items() if k[0] == p for r in v]
        mj = Counter(majority(r) for r in rs)
        perpair[p + 1] = dict(A=mj['A'], B=mj['B'], tie=mj['tie'], n=len(rs))
    md.append('\nPer pair: ' + '; '.join('pair %d: A %d, B %d, tie %d of %d' % (k, v['A'], v['B'], v['tie'], v['n']) for k, v in perpair.items()))
    out['pred2'] = dict(spearman=rho_s, A=totA, B=totB, tie=totT, perpair=perpair, runlevel=dict(pred2))
    for preset, title in (('A', 'A only pre-seeded (pair 1 tags)'), ('halfAB', 'two homogeneous networks, half/half, no background'),
                          ('minorB', 'one all-B island among I - 1 all-A, no background')):
        md.append('\n**%s.**\n' % title)
        if preset == 'A':
            md.append('| I | mN | runs | A-network-held islands at end (mean share) | bridge-held | rival (any) locally established, runs | '
                      'rival separation at end | ever separated | efficient |')
            md.append('|---|---|---|---|---|---|---|---|---|')
            for key in sorted(k for k in cc if k[0] == 'A'):
                rs = cc[key]
                md.append('| %d | %g | %d | %.2f | %.2f | %d | %d | %d | %d |' % (
                    key[2], key[3], len(rs), np.mean([r['held_final'].get('1', 0) / r['I'] for r in rs]),
                    np.mean([r['held_final'].get('3', 0) / r['I'] for r in rs]),
                    sum(1 for r in rs if r['est_summary'].get('rival/local', 0) > 0), sum(1 for r in rs if r['n_sep_end_pairs']),
                    sum(1 for r in rs if r['first_sep'] >= 0), sum(1 for r in rs if r['outcome'] == 'efficient')))
                out.setdefault('ctrlA', {})[str(key)] = dict(n=len(rs), sep_end=sum(1 for r in rs if r['n_sep_end_pairs']))
            continue
        md.append('| N | I | mN | runs | both | A only | B only | neither | first-loss hazard [95%] | KM S(1e2)/S(1e3)/S(1e4)/S(1e5) | median loss | '
                  'rival separation at end | A majority |')
        md.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        for key in sorted(k for k in cc if k[0] == preset):
            rs = cc[key]; cats = Counter(category(r) for r in rs)
            k, T, h, lo, hi = hazard(rs)
            lt = [loss_time(r) for r in rs]
            S = km([t for t, e in lt], [e for t, e in lt])
            med = np.median([t for t, e in lt if e]) if any(e for t, e in lt) else float('nan')
            maj = Counter(majority(r) for r in rs)
            out.setdefault('ctrl', {})[str(key)] = dict(n=len(rs), cats=dict(cats), losses=k, exposure=T, hazard=h, hazard_ci=(lo, hi), km=S,
                                                        median_loss=med, A_major=maj['A'], sep_end=sum(1 for r in rs if r['n_sep_end_pairs']))
            md.append('| %d | %d | %g | %d | %d | %d | %d | %d | %.2g [%.2g, %.2g] | %s | %s | %d | %d |' % (
                key[4], key[2], key[3], len(rs), cats['both'], cats['A only'], cats['B only'], cats['neither'], h, lo, hi,
                ' / '.join('%.2f' % S[m] for m in MARKS), '%.0f' % med if med == med else '-',
                sum(1 for r in rs if r['n_sep_end_pairs']), maj['A']))
    # S1: minority-island hazard vs mN * rho_DD
    rho = st['rho']['100']['dd_migrant']
    md.append('\nS1 check (one all-B island among I - 1 all-A): hazard of losing B vs the single-migrant prediction mN·rho_DD(100) = %.3g·mN.\n' % rho)
    md.append('| N | I | mN | B losses / runs | hazard of B loss [95%] | predicted mN·rho_DD(N) | ratio | B ever held > 1 island |\n|---|---|---|---|---|---|---|---|')
    for key in sorted(k for k in cc if k[0] == 'minorB'):
        rs = cc[key]
        kB = sum(1 for r in rs if r['t_ext'][2] >= 0); TB = sum(r['t_ext'][2] if r['t_ext'][2] >= 0 else r['stop_gen'] for r in rs)
        lo, hi = poisson_ci(kB)
        grew = sum(1 for r in rs if any(t[4] > 1 for t in r.get('trace', [])))
        rhoN = st['rho'][str(key[4])]['dd_migrant']
        md.append('| %d | %d | %g | %d / %d | %.2g [%.2g, %.2g] | %.2g | %.3g | %d |' % (key[4], key[2], key[3], kB, len(rs), kB / TB, lo / TB, hi / TB,
                                                                                  key[3] * rhoN, kB / TB / (key[3] * rhoN), grew))
    # ---------------------------------------------------------- natural separation
    md.append('\n## 3. Natural separation (iid seeds only, N = 100)\n')
    md.append('Separated = at the end, two certified islands whose cooperative holders mutually defect. p_B = local establishments by a rival '
              'of the FairBot pair per island, measured in these runs; predicted = 1 - (1 - p_B)^I.\n')
    md.append('| n | I | mN | runs | separated at end [95%] | ever separated | p_B (per island) | predicted | rival seeded runs | '
              'efficient | unresolved | composition of separated runs |')
    md.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
    nc = defaultdict(list)
    for r in nat:
        nc[(r['n'], r['I'], r['mN'])].append(r)
    natout = {}
    for key in sorted(nc):
        rs = nc[key]; n = len(rs)
        ks = sum(1 for r in rs if r['n_sep_end_pairs'] > 0)
        ever = sum(1 for r in rs if r['first_sep'] >= 0)
        nb = sum(r['n_bg'] for r in rs)
        rl = sum(r['est_summary'].get('rival/local', 0) for r in rs)
        pB = rl / nb
        pred = 1 - (1 - pB) ** key[1]
        lo, hi = wilson(ks, n)
        comp = Counter()
        for r in rs:
            if r['n_sep_end_pairs'] > 0:
                comp[' + '.join('%s:%d' % (a, b) for a, b in sorted(r['sep_end_holders'], key=lambda t: -t[1])[:3])] += 1
        dn = R.cls(key[0])
        def holds_noncoop(r):
            return r['status'] != 'frozen' and any(not dn['coop'][dn['idx'][nm_]] for nm_, c_ in r['holders'])
        eff = sum(1 for r in rs if r['outcome'] == 'efficient' or (r['status'] != 'frozen' and not holds_noncoop(r)))
        unres = sum(1 for r in rs if holds_noncoop(r))
        rseed = sum(1 for r in rs if r['est_summary'].get('rival/local', 0) + r['est_summary'].get('rival/imm', 0) > 0)
        natout[str(key)] = dict(n=n, sep=ks, ci=(lo, hi), ever=ever, pB=pB, pred=pred, consistent=lo <= pred <= hi, eff=eff, unres=unres,
                                comp=dict(comp))
        md.append('| %d | %d | %g | %d | %s | %d | %.2e | %.3f | %d | %d | %d | %s |' % (
            key[0], key[1], key[2], n, fmt_ci(ks, n), ever, pB, pred, rseed, eff, unres, '; '.join('%s (%d)' % kv for kv in comp.most_common(3))))
    out['nat'] = natout
    # ---------------------------------------------------------- rule
    md.append('\n## 4. The mN rule (n = 9)\n')
    rc = defaultdict(list)
    for r in rule:
        rc[(r['N'], r['I'], r['mN'])].append(r)
    ref = {}
    for N in (100, 400):
        rs = rc.get((N, 16, 0.0), [])
        if rs:
            te = [t for r in rs for t, b in zip(r['t_est'], r['preest']) if t >= 0] if 'preest' in rs[0] else [t for r in rs for t in r['t_est'] if t >= 0]
            nis = sum(r['n_bg'] for r in rs)
            p = len(te) / nis
            ref[N] = dict(T_nuc=float(np.median(te)) if te else float('nan'), p=p, n_islands=nis)
    out['rule_ref'] = {str(k): v for k, v in ref.items()}
    for N, v in ref.items():
        md.append('m = 0 reference, N = %d: per-island establishment p = %.3f (%d islands), T_nuc (median establishment gen) = %.0f.' % (
            N, v['p'], v['n_islands'], v['T_nuc']))
    md.append('\n| N | I | mN | x = mN·T_nuc/N | runs | efficient [95%] | reference 1-(1-p)^I | fall | local-ancestry est. per island | '
              'ICC of local est. | arrivals before est. (mean) | replacement fraction at est. (mean) | median est. gen |')
    md.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    ruleout = {}
    for key in sorted(rc):
        N, I, mN = key
        if mN == 0: continue
        rs = rc[key]; n = len(rs)
        eff = sum(1 for r in rs if r['outcome'] == 'efficient')
        x = mN * ref[N]['T_nuc'] / N if N in ref else float('nan')
        R0 = 1 - (1 - ref[N]['p']) ** I if N in ref else float('nan')
        rho_, pl = icc(rs)
        arrs = [a for r in rs for a, t in zip(r['e_arr'], r['t_est']) if t >= 0]
        imms = [a for r in rs for a, t in zip(r['e_imm'], r['t_est']) if t >= 0]
        tes = [t for r in rs for t in r['t_est'] if t >= 0]
        ruleout[str(key)] = dict(n=n, eff=eff, x=x, ref=R0, fall=R0 - eff / n, icc=rho_, p_local=pl, arr=float(np.mean(arrs)) if arrs else None,
                                 imm=float(np.mean(imms)) if imms else None, t_med=float(np.median(tes)) if tes else None)
        md.append('| %d | %d | %g | %.3f | %d | %s | %.3f | %+.2f | %.3f | %.3f | %.1f | %.3f | %.0f |' % (
            N, I, mN, x, n, fmt_ci(eff, n), R0, R0 - eff / n, pl, rho_, np.mean(arrs) if arrs else float('nan'),
            np.mean(imms) if imms else float('nan'), np.median(tes) if tes else float('nan')))
    out['rule'] = ruleout
    # local nucleation: arrivals and replacement among locally-founded islands; relative local rate q = local/p_N
    md.append('\nLocal nucleation under migration (islands whose winner is local-ancestry). q = local-establishment rate per island / m = 0 p_N; '
              'arrival exposure and replacement fraction averaged over the locally-founded islands only.\n')
    md.append('| N | I | mN | x | mN·T_nuc (expected arrivals) | q | arrivals before local est. (mean) | replacement fraction at local est. (mean) | '
              'median local est. gen |')
    md.append('|---|---|---|---|---|---|---|---|---|')
    qrows = defaultdict(list)
    for key in sorted(rc):
        N, I, mN = key
        if mN == 0 or N not in ref: continue
        rs = rc[key]
        L = [(a, im, t) for r in rs for a, im, t, hl in zip(r['e_arr'], r['e_imm'], r['t_est'], r['e_hloc']) if t >= 0 and hl >= 0.5]
        q = (len(L) / sum(r['n_bg'] for r in rs)) / ref[N]['p']
        x = mN * ref[N]['T_nuc'] / N
        ea = float(np.mean([a for a, im, t in L])) if L else float('nan'); ei = float(np.mean([im for a, im, t in L])) if L else float('nan')
        qrows[N].append((mN, x, mN * ref[N]['T_nuc'], ea, ei, q, len(L)))
        ruleout[str(key)].update(q=q, arr_local=ea, imm_local=ei)
        md.append('| %d | %d | %g | %.3f | %.1f | %.2f | %.1f | %.3f | %s |' % (N, I, mN, x, mN * ref[N]['T_nuc'], q, ea, ei,
                  '%.0f' % np.median([t for a, im, t in L]) if L else '-'))
    # pooled over I per (N, mN), and the crossing point q = 1/2 under each control
    md.append('\nCrossing of q = 1/2 (log-linear interpolation of q pooled over I at each (N, mN)) under each candidate control:\n')
    md.append('| N | mN·T_nuc/N at q = 1/2 | expected arrivals mN·T_nuc at q = 1/2 | measured arrivals before local est. at q = 1/2 | m = mN/N at q = 1/2 |\n|---|---|---|---|---|')
    cross = {}
    for N, L in qrows.items():
        by = defaultdict(list)
        for mN, x, ex, ea, ei, q, nl in L: by[mN].append((x, ex, ea, q, nl))
        pts = []
        for mN in sorted(by):
            v = by[mN]; w = np.array([t[4] for t in v], float)
            pts.append((mN, v[0][0], v[0][1], float(np.nansum([t[2] * t[4] for t in v]) / max(1, w.sum())), float(np.mean([t[3] for t in v]))))
        res = {}
        for j, name in ((1, 'x'), (2, 'expected'), (3, 'measured'), (0, 'm')):
            val = float('nan')
            for a, b in zip(pts, pts[1:]):
                if a[4] >= 0.5 > b[4]:
                    f = (a[4] - 0.5) / (a[4] - b[4])
                    ca, cb = (a[j] / N if name == 'm' else a[j]), (b[j] / N if name == 'm' else b[j])
                    val = float(np.exp(np.log(ca) + f * (np.log(cb) - np.log(ca)))) if ca > 0 and cb > 0 else float('nan')
                    break
            res[name] = val
        cross[N] = res
        md.append('| %d | %.2f | %.0f | %.0f | %.4f |' % (N, res['x'], res['expected'], res['measured'], res['m']))
    out['rule_cross'] = {str(k): v for k, v in cross.items()}
    # collapse comparison
    try:
        md.append('\n' + collapse(rc, ref, out))
    except Exception as e:
        md.append('\n(collapse fit failed: %s)' % e)
    # ---------------------------------------------------------- merge
    md.append('\n## 5. Merge test\n')
    if merge:
        mc = defaultdict(list)
        for m in merge:
            mc[(m['exp'], m['preset'])].append(m)
        md.append('| source | merges | clean two-type | larger won (clean) | minority won (clean) | mixed/unresolved | median gens to freeze (clean) | '
                  'median larger share (clean) | near-ties (share < 0.6) |')
        md.append('|---|---|---|---|---|---|---|---|---|')
        for key in sorted(mc):
            ms = mc[key]; cl = [m for m in ms if m['clean']]
            md.append('| %s %s | %d | %d | %d | %d | %d | %s | %s | %d |' % (
                key[0], key[1], len(ms), len(cl), sum(m['larger_won'] for m in cl), sum(m['minority_won'] for m in cl),
                sum(1 for m in cl if not m['larger_won'] and not m['minority_won']),
                '%.0f' % np.median([m['gens_to_freeze'] for m in cl]) if cl else '-',
                '%.3f' % np.median([m['share_larger'] for m in cl]) if cl else '-', sum(1 for m in cl if m['share_larger'] < 0.6)))
        cl = [m for m in merge if m['clean']]
        out['merge'] = dict(n=len(merge), clean=len(cl), larger=sum(m['larger_won'] for m in cl), minority=sum(m['minority_won'] for m in cl))
    md.append(VERDICTS)
    open(os.path.join(RUNS, 'rival-islands.md'), 'w').write('\n'.join(md) + '\n')
    json.dump(out, open(os.path.join(RUNS, 'rival-islands.json'), 'w'), indent=1, default=float)
    print('\n'.join(md))


def collapse(rc, ref, out):
    """Pooled logistic fits of the run-level efficient indicator, relative to the m = 0 reference, on three candidate
    controls; lower deviance = better collapse of N = 100 and 400."""
    import scipy.optimize as so
    data = []
    for (N, I, mN), rs in rc.items():
        if mN == 0 or N not in ref: continue
        R0 = 1 - (1 - ref[N]['p']) ** I
        arrs = [a for r in rs for a, t in zip(r['e_arr'], r['t_est']) if t >= 0]
        imms = [a for r in rs for a, t in zip(r['e_imm'], r['t_est']) if t >= 0]
        x = mN * ref[N]['T_nuc'] / N
        for r in rs:
            data.append((N, I, R0, x, np.mean(arrs) + 0.01, np.mean(imms) + 1e-3, 1.0 if r['outcome'] == 'efficient' else 0.0))
    D = np.array(data)
    y = D[:, 6]; R0 = np.clip(D[:, 2], 1e-6, 1 - 1e-6)
    lines = ['Collapse test: P(efficient) = R0 * sigmoid(a + b log c) for control c, pooled over all (N, I) cells; deviance (lower is better):\n']
    res = {}
    for j, name in ((3, 'mN·T_nuc/N'), (4, 'arrival exposure'), (5, 'replacement fraction')):
        c = np.log(D[:, j])
        def nll(th):
            q = R0 / (1 + np.exp(-(th[0] + th[1] * c)))
            q = np.clip(q, 1e-9, 1 - 1e-9)
            return -(y * np.log(q) + (1 - y) * np.log(1 - q)).sum()
        best = min((so.minimize(nll, x0, method='Nelder-Mead') for x0 in ([3, -1], [0, -1], [5, -2])), key=lambda o: o.fun)
        res[name] = dict(deviance=2 * best.fun, a=float(best.x[0]), b=float(best.x[1]))
        lines.append('- %s: deviance %.1f (a %.2f, b %.2f)' % (name, 2 * best.fun, best.x[0], best.x[1]))
    out['collapse'] = res
    return '\n'.join(lines)



VERDICTS = r"""
## Verdicts (predictions/2026-10-05-rival-islands.md)

| # | prediction | outcome |
|---|---|---|
| 1 | separation long-lived: hazard < 1e-5 at mN <= 1; both present >= 0.8 at mN <= 1, >= 0.5 at mN = 10 | **Failed, falsifier fired.** Both present at the horizon in 0/40 runs in every mN = 1 and mN = 10 cell; at mN = 0.1, 2/40 to 40/40. First-loss hazard 5e-5 to 7.5e-4 at mN = 1, 5e-3 to 1.4e-2 at mN = 10. "Lifetimes shorten with flux" held, strongly superlinearly |
| 2 | majority set at nucleation; A (FairBot family) majority >= 0.8; falsifier: B majority > 0.3 or Spearman < 0.3 | **Failed, falsifier fired narrowly** (B majority 343/1,080 = 0.32). A majority 0.67; run-level nucleation rule right in 358/511 decided runs (0.70; 569 undecided). Spearman with measured rates 0.70 (that clause held) |
| 3 | natural separation 0.01-0.05 at (100, 256) n = 9, higher at n = 12 and at I = 1,024, consistent with 1 - (1 - p_B)^I, flat in mN <= 1; falsifier: a fall from 256 to 1,024 | **Falsifier not fired; most clauses failed.** Growth in I and n held at mN = 0.1. The band failed (1/300 = 0.003). 1 - (1 - p_B)^I predicts *ever separated* (35/300 vs 0.098; 20/100 vs 0.18), not separated at the horizon (outside the interval at 4 of 6 mN = 0.1 cells). Flatness in mN failed: 0/300 at mN = 1 in every cell |
| 4 | efficient fraction flat while mN·T_nuc/N < 0.1 and falls once > 1; ICC < 0.1 in the flat region; falsifier: a fall > 0.2 while < 0.1 | **Held on the falsifier, the flat clause and ICC** (max fall 0.06; abs(ICC) < 0.03). **Fall clause partly held:** run-level efficiency falls only where independent trials leave room ((100, 16): -0.10 at x = 1.35, -0.17 at x = 4.5; (400, 16) none at x = 1.75; I >= 64 at the ceiling). Island-level local nucleation q has the predicted shape: q = 1/2 at x = 0.75 (N = 100) and 0.86 (N = 400) |
| 5 | larger network wins >= 0.9 of clean two-type merges; falsifier: minority > 0.3 | **Held.** 535/572 clean merges (0.935); 372/372 at larger share >= 0.6; minority wins only near ties (share <= 0.56). All resolved within 115 generations |
| S1 | minority-island hazard = mN·rho_DD(100) within x3 | **Failed** at mN >= 1 (14-18x faster at mN = 1, ~200x at mN = 10); held at mN = 0.1 (ratio 0.27-1.03) |
| S2 | at mN = 10 one network lost within 1e3 generations in >= 0.8 of runs | **Held** (item 2: 360/360; control c: all) |
| S3 | losses dominated by nucleation; both present >= 0.8 at mN = 0.1 in every item-2 cell | **Failed** (415 of 485 losses at mN <= 1 after generation 1e3; pairs 1-2 at I = 64, 256: 2-22 of 40) |
| S4 | N = 200: no loss at mN = 1; at mN = 10 half/half loses >= 0.5, minority <= 0.2 | **Failed on two clauses** (minority preset: 1/40 lost at mN = 1 and 40/40 at mN = 10). The central contrast held: at mN = 1 the hazard falls ~1,000x from N = 100 to 200 |

## Deviations and definitions applied after seeing data

- *Unresolved* at the horizon is assigned by holders, as predeclared: an island held by a class outside the tagged networks. The kernel's
  own "unresolved" status (some island not locally frozen at the last check) is almost always transient migrants and is not used.
- Item 4: the efficient fraction is at its ceiling for I >= 64, so the island-level local-nucleation rate q (relative to m = 0) and its
  q = 1/2 crossing were added as the informative response; the predeclared logistic collapse on the run-level efficient fraction is
  reported but is uninformative (deviances 385-389).
- Item 4's arrival exposure and replacement fraction are reported over locally founded islands (the islands whose nucleation is being
  diluted); means over all established islands are dominated by colonized islands (replacement ~0.9 at every mN).
- The N = 200 control cells (addendum S4) were added after partial item-2 data, predeclared in a committed addendum before they ran.
"""


if __name__ == '__main__':
    main()
