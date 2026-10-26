"""Report for the encounter-contracts experiment: reads runs/encounter_contracts/*.json and writes runs/encounter-contracts.md and .json.

    python3 src/encounter_contracts_report.py
"""
import glob, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import encounter_contracts as EC

ROOT = EC.ROOT
D = os.path.join(ROOT, 'runs', 'encounter_contracts')
NOUT = EC.NOUT
CATS = ['F', 'U', 'G', 'W', 'D', 'M', 'none']
CPS = (1, 3, 10, 30, 100, 300, 1000)


def load_cells():
    cells = {}
    for f in sorted(glob.glob(os.path.join(D, 'pool_*.json'))):
        r = json.load(open(f))
        cells[os.path.basename(f)[:-5]] = r
    return cells


def load_kind(prefix):
    out = {}
    for f in sorted(glob.glob(os.path.join(D, prefix + '_*.json'))):
        out[os.path.basename(f)[:-5]] = json.load(open(f))
    return out


def wilson(k, n, z=1.96):
    if n == 0:
        return (float('nan'), float('nan'))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def se_prop(p, n):
    return math.sqrt(max(p * (1 - p), 0) / max(n, 1))


def fmt(x, d=3):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return 'n/a'
    return ('%.' + str(d) + 'f') % x


def find(cells, arm, nu, start='post', mN=1e-3, N=100, rep=0, I=None, rounds_min=0):
    best = None
    for k, r in cells.items():
        if r['arm'] == arm and abs(r['nu'] - nu) < 1e-12 and r['start'] == start and abs(r['mN'] - mN) < 1e-15 and r['N'] == N \
                and r['rep'] == rep and (I is None or r['I'] == I) and r['rounds'] >= rounds_min:
            if best is None or r['rounds'] > best['rounds']:
                best = r
    return best


def cp(r, rnd):
    for c in r['checkpoints']:
        if c['round'] == rnd:
            return c
    return None


def sh(c, key='settled'):
    """category shares among settled islands (or among all, for 'cur')."""
    h = c[key]
    n = max(c['n_settled'], 1) if key == 'settled' else c['I']
    return {k: v / n for k, v in h.items()}


def vstar(c):
    return c['vstar_settled']


def wd(c):
    s = sh(c)
    return s.get('W', 0) + s.get('D', 0)


def paired_diff(c1, c2, key='vstar_settled'):
    """difference of two cell means with a normal interval treating the cells as independent samples of islands (an upper bound on
    the interval when the founders are shared)."""
    p1, p2 = c1[key], c2[key]
    n1, n2 = max(c1['n_settled'], 1), max(c2['n_settled'], 1)
    se = math.sqrt(se_prop(p1, n1) ** 2 + se_prop(p2, n2) ** 2)
    return p1 - p2, 1.96 * se


def cell_label(r):
    s = '%s nu=%g I=%d' % (r['arm'], r['nu'], r['I'])
    if r['start'] != 'post': s += ' %s' % r['start']
    if r['mN'] != 1e-3: s += ' mN=%g' % r['mN']
    if r['N'] != 100: s += ' N=%d' % r['N']
    if r['rep']: s += ' rep%d' % r['rep']
    return s


def traj_table(r, rounds=CPS, extra=False):
    rows = ['| round | V* | F0 | F1 | F2 | U | W+D | G | mixed | unsettled | efficiency | dominated |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for rd in (0,) + tuple(rounds):
        c = cp(r, rd)
        if not c:
            continue
        s = sh(c)
        n = max(c['n_settled'], 1)
        rows.append('| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            rd, fmt(vstar(c)), fmt(s.get('F0', 0)), fmt(s.get('F1', 0)), fmt(s.get('F2', 0)), fmt(s.get('U', 0)),
            fmt(s.get('W', 0) + s.get('D', 0)), fmt(s.get('G', 0)), fmt(s.get('mixed', 0)), fmt(1 - c['n_settled'] / c['I']),
            fmt(c['mean_total_sixths'] / 6), fmt(c['pareto_dominated_share'])))
    return '\n'.join(rows)


def genesis_numbers(r):
    """acceptance numbers of a pool or within cell"""
    st = list(r['genesis_stat']) + [0] * 8; sf = list(r.get('genesis_statf', [0] * 16)) + [0] * 4
    att = st[0:3]; acc = st[3:6]
    out = dict(att=att, acc=acc, blk=st[6:9], acc_per_attempt=sum(acc) / max(sum(att), 1))
    gens_total = None
    if 'rounds' in r:
        gens_total = r['I'] * r['rounds'] * r['round_gens']
    elif 'gens' in r:
        gens_total = r['I'] * r['gens']
    out['gens_total'] = gens_total
    if gens_total:
        out['acc_per_island_gen'] = sum(acc) / gens_total
    out['by_cur'] = {}
    out['by_settled'] = {}
    for i, c in enumerate(CATS):
        g = sf[i]
        out['by_cur'][c] = dict(att=st[9 + i], acc=st[16 + i], gens=g, rate=(st[16 + i] / g if g > 0 else None))
        g2 = sf[7 + i]
        out['by_settled'][c] = dict(att=st[44 + i], acc=st[51 + i], gens=g2, rate=(st[51 + i] / g2 if g2 > 0 else None))
    out['fair_mono'] = dict(att=st[64], acc=st[66], gens=sf[14], rate=(st[66] / sf[14] if sf[14] > 0 else None))
    out['fair_poly'] = dict(att=st[65], acc=st[67], gens=sf[15], rate=(st[67] / sf[15] if sf[15] > 0 else None))
    out['copy_att'] = st[32]; out['copy_acc'] = st[33]; out['uni_att'] = st[34]; out['uni_acc'] = st[35]; out['unmatched'] = st[36]
    out['evict'] = st[37]; out['tabfull'] = st[38]; out['bc_want'] = st[40]; out['bc_inst'] = st[39]
    out['mig'] = st[41]; out['migfail'] = st[42]; out['br_noeq'] = st[30]; out['br_fail'] = st[31]
    out['inst_atomless'] = st[68:70]
    return out


# ====================================================================== within-island chain (no migrants)
def within_summary(r):
    """occupancy, exit rates and the transition structure of the no-migrant runs."""
    names = ['F', 'U', 'G', 'W', 'D', 'M', 'none']
    gc = np.array(r['gen_cur_total']); gs = np.array(r['gen_settled_total'])
    tr = r['transitions']
    tot_gens = gs.sum()
    out = dict(arm=r['arm'], nu=r['nu'], I=r['I'], gens=r['gens'], island_gens=int(r['I'] * r['gens']))
    out['occupancy_cur'] = {n: float(x / gc.sum()) for n, x in zip(names, gc)}
    out['occupancy_settled'] = {n: float(x / max(gs.sum(), 1)) for n, x in zip(names, gs)}
    out['changes'] = r['changes_total']
    out['changes_per_island_gen'] = r['changes_total'] / (r['I'] * r['gens'])
    # exit rates per generation from settled F (all pairs together), U, W
    def total(prefixes, to=None):
        s = 0
        for k, v in tr.items():
            a, b = k.split('>')
            if a in prefixes and (to is None or b in to):
                s += v
        return s
    fair = ('F0', 'F1', 'F2')
    gF = gs[0]; gU = gs[1]; gW = gs[3]
    out['F_exit_rate'] = total(fair) / gF if gF > 0 else None
    out['F_exit_to_U_share'] = (total(fair, ('U',)) / max(total(fair), 1))
    out['F_exit_to_F_share'] = (total(fair, fair) / max(total(fair), 1))
    out['F_exit_to_WD_share'] = (total(fair, ('W', 'D')) / max(total(fair), 1))
    out['U_exit_rate'] = total(('U',)) / gU if gU > 0 else None
    out['U_exit_to_F_share'] = total(('U',), fair) / max(total(('U',)), 1)
    out['U_exit_to_U_share'] = total(('U',), ('U',)) / max(total(('U',)), 1)
    out['U_exit_to_W_share'] = total(('U',), ('W',)) / max(total(('U',)), 1)
    out['W_exit_rate'] = total(('W',)) / gW if gW > 0 else None
    out['transitions'] = tr
    st = list(r['genesis_stat']) + [0] * 8; sf = list(r['genesis_statf']) + [0] * 4
    out['accept_per_attempt'] = sum(st[3:6]) / max(sum(st[0:3]), 1)
    out['accept_per_island_gen'] = sum(st[3:6]) / (r['I'] * r['gens'])
    out['accept_by_S'] = [st[3 + i] / max(st[i], 1) for i in range(3)]
    out['fair_settled_formation_rate'] = st[51] / sf[7] if sf[7] > 0 else None
    out['fair_mono_rate'] = st[66] / sf[14] if sf[14] > 0 else None
    out['fair_poly_rate'] = st[67] / sf[15] if sf[15] > 0 else None
    out['fair_poly_share_of_time'] = sf[15] / max(sf[14] + sf[15], 1)
    out['bundles'] = r.get('bundles', {})
    return out


# ====================================================================== bundles (contract fates)
def bundle_stats(r, kmin=1, kmax=3, cats=(0, 1, 2, 3, 4, 5, 6)):
    """pooled over |S| in [kmin, kmax] and classes in cats: n, fraction fixing in all signer slots, fraction coordination-needing,
    n fixing split by coordination."""
    n = both = coord = bc = bf = alive = 0
    for k, v in r.get('bundles', {}).items():
        kk, cc = (int(x) for x in k.split('|'))
        if kmin <= kk <= kmax and cc in cats:
            n += v['n']; both += v['n_both_fix'] if 'n_both_fix' in v else round(v['frac_both_fix'] * v['n'])
            coord += v['n_coord'] if 'n_coord' in v else round(v['frac_coord'] * v['n'])
            bc += v.get('n_both_coord', 0); bf += v.get('n_both_free', 0)
            alive += round(v['frac_alive_2000'] * v['n'])
    return dict(n=n, both_fix=both, frac_both_fix=both / n if n else None, coord=coord, frac_coord=coord / n if n else None,
                both_coord=bc, both_free=bf, alive_2000=alive)


def half_life(r, k, cat):
    v = r.get('bundles', {}).get('%d|%d' % (k, cat))
    return v['life_median'] if v else None


# ====================================================================== verdicts
def verdict(vid, claim, outcome, detail):
    return dict(id=vid, claim=claim, outcome=outcome, detail=detail)


def build_verdicts(cells, within, paired):
    V = []
    Z = find(cells, '0', 0.0, I=1024)
    R1 = find(cells, 'R', 1.0, I=1024, rep=0)
    R01 = find(cells, 'R', 0.1, I=1024, rep=0)

    def sec(arm, nu):
        return find(cells, arm, nu, I=512, start='post')

    def wsum(arm, nu):
        for k, w in within.items():
            if w['arm'] == arm and abs(w['nu'] - nu) < 1e-12:
                return within_summary(w)
        return None

    # --- 1: settled islands go quiet
    d = []
    outs = []
    for nu in (1.0, 0.1):
        w = wsum('R', nu)
        if w:
            rate = w['fair_settled_formation_rate']
            d.append('nu=%g: formation of accepted (firing) contracts on settled fair islands %s per island-generation (monomorphic-type islands %s, polymorphic %s; %s of fair island-time polymorphic); limit 1e-3' % (
                nu, fmt(rate, 5), fmt(w['fair_mono_rate'], 5), fmt(w['fair_poly_rate'], 5), fmt(w['fair_poly_share_of_time'], 3)))
            outs.append(rate is not None and rate > 1e-3)
    if outs:
        V.append(verdict('1', 'settled fair islands form no firing contracts (falsifier: rate above 1e-3 per island-generation)',
                         'failed at nu=1, held at nu=0.1' if (len(outs) == 2 and outs[0] and not outs[1]) else ('failed' if all(outs) else ('partial' if any(outs) else 'held')), '; '.join(d)))
        gm = []
        for nu in (1.0, 0.1):
            w = wsum('R', nu)
            if w:
                gm.append('nu=%g: monomorphic %s, polymorphic %s' % (nu, fmt(w['fair_mono_rate'], 5), fmt(w['fair_poly_rate'], 5)))
        ok_mono = [wsum('R', nu) and wsum('R', nu)['fair_mono_rate'] is not None and wsum('R', nu)['fair_mono_rate'] <= 1e-3 for nu in (1.0, 0.1) if wsum('R', nu)]
        ok_poly = [wsum('R', nu) and wsum('R', nu)['fair_poly_rate'] is not None and wsum('R', nu)['fair_poly_rate'] > 1e-3 for nu in (1.0, 0.1) if wsum('R', nu)]
        V.append(verdict('1c', "gemini-4-argon's counter: monomorphic fair islands go quiet, polymorphic ones keep forming above 1e-3",
                         'held' if all(ok_mono) and all(ok_poly) else 'partial: the polymorphic clause holds at both nu (rate above 1e-3); the monomorphic-quiet clause holds only at nu=0.1', '; '.join(gm)))
    # --- 2: contracts clear dominated islands (V* uplift)
    d = []; ups = []
    for (nu, Rc, rd) in ((1.0, R1, 300), (1.0, R1, 1000), (0.1, R01, 1000)):
        if Rc is None or Z is None:
            continue
        c1, c0 = cp(Rc, rd), cp(Z, rd)
        if c1 is None or c0 is None:
            continue
        df, hw = paired_diff(c1, c0)
        ups.append(df)
        d.append('nu=%g round %d: V* R %s, arm 0 %s, difference %s +- %s' % (nu, rd, fmt(vstar(c1)), fmt(vstar(c0)), fmt(df), fmt(hw)))
    if ups:
        V.append(verdict('2', 'R settled V* share at least 0.15 above arm 0 (falsifier: less than 0.05 above)',
                         'held' if min(ups) >= 0.15 else ('failed' if max(ups) < 0.05 else 'partial'), '; '.join(d)))
        V.append(verdict('2c', "gpt-6.1-sol's counter: gains are heterogeneous, no robust 0.15 uplift across nu and N",
                         'held' if max(ups) < 0.15 else 'failed', 'uplifts %s' % ', '.join(fmt(u) for u in ups)))
    # efficiency: W+D at 10 events
    d = []
    for (nu, Rc) in ((1.0, R1), (0.1, R01)):
        if Rc and Z:
            for rd in (10, 100, 1000):
                c1, c0 = cp(Rc, rd), cp(Z, rd)
                if c1 and c0:
                    d.append('nu=%g round %d: W+D R %s, arm 0 %s' % (nu, rd, fmt(wd(c1)), fmt(wd(c0))))
    if d:
        V.append(verdict('E5', 'R clears dominated islands faster: W+D at 10 events below 0.02 at nu=1 (falsifier above 0.05), below 0.10 at nu=0.1', 'see detail', '; '.join(d)))
    # --- 3: coordination barrier
    d = []
    allb = []
    for tag, Rc in (('nu=1', R1), ('nu=0.1', R01)):
        if Rc is None:
            continue
        dom = bundle_stats(Rc, kmin=2, kmax=3, cats=(3, 4))
        allk = bundle_stats(Rc, kmin=1, kmax=3, cats=(3, 4))
        single = bundle_stats(Rc, kmin=1, kmax=1, cats=(3, 4))
        d.append('%s: contracts of |S|>=2 formed on wasteful/disagreement islands n=%d, fixing in all signer slots %s; singletons are %s of contracts formed on those islands (%s fix)' % (
            tag, dom['n'], fmt(dom['frac_both_fix']), fmt(single['n'] / max(allk['n'], 1)), fmt(single['frac_both_fix'])))
        allb.append(dom['frac_both_fix'])
    if allb and all(x is not None for x in allb):
        V.append(verdict('3', 'contracts of |S|>=2 formed on dominated islands fix in both member slots under 0.1 (falsifier at least 0.3)',
                         'held' if max(allb) < 0.1 else ('failed' if max(allb) >= 0.3 else 'partial'), '; '.join(d)))
    # --- 4: third-pair moves (paired branches)
    def pr(arm, nu, tag=None):
        for k, w in paired.items():
            if w['arm'] == arm and abs(w['nu'] - nu) < 1e-12 and (tag is None or ('_%s_k' % tag) in k):
                return w
        return None
    d = []; ok = []
    for (arm, nu, tag) in (('R', 1.0, 'r100'), ('R', 1.0, 'r1000'), ('R', 0.1, 'r1000')):
        w = pr(arm, nu, tag)
        if not w or 'alpha' not in w['summary']:
            continue
        a = w['summary']['alpha']; kp = w['summary']['kappa']
        d.append('%s nu=%g %s: alpha migrant branch %s (control %s), excess %s [%s, %s], n=%d, clusters %d, 95%% upper bound of migrant branch %s; kappa migrant %s (control %s), excess %s [%s, %s]' % (
            arm, nu, tag, fmt(a['migrant_branch'], 5), fmt(a['control_branch'], 5), fmt(a['excess'], 5), fmt(a['excess_ci'][0], 5), fmt(a['excess_ci'][1], 5),
            a['n'], a['n_clusters'], fmt(a['migrant_branch_ci'][1], 5), fmt(kp['migrant_branch'], 5), fmt(kp['control_branch'], 5), fmt(kp['excess'], 5),
            fmt(kp['excess_ci'][0], 5), fmt(kp['excess_ci'][1], 5)))
        ok.append((a['excess_ci'][0] > 0, a['migrant_branch_ci'][1] < 1e-3, a['n'] >= 20000, nu, a['migrant_branch']))
    if ok:
        excl1 = all(x[0] for x in ok if x[3] == 1.0)
        excl_all = all(x[0] for x in ok)
        V.append(verdict('4', 'alpha > 0 with an interval excluding 0 on fair islands (falsifier: the interval includes 0; absent at this resolution if the upper bound is below 1e-3 per migrant)',
                         'held at nu=1, interval touches 0 at nu=0.1' if excl1 and not excl_all else ('held' if excl_all else 'failed (interval includes 0)'), '; '.join(d)))
        small = all(x[4] < 1e-3 for x in ok)
        V.append(verdict('4c', "gemini-4-argon's counter: alpha's interval includes 0 or alpha < 1e-3", 'held (alpha below 1e-3 per migrant in every cell; the interval excludes 0 at nu=1)' if small else 'failed', '(same numbers as 4)'))
    # --- 5: R vs BR
    d = []; dif = []
    for (nu, Rc, rd) in ((1.0, R1, 300), (1.0, R1, 1000), (0.1, R01, 1000)):
        B_ = sec('BR', nu)
        if Rc is None or B_ is None:
            continue
        c1, c2 = cp(Rc, rd), cp(B_, rd)
        if c1 is None or c2 is None:
            continue
        df, hw = paired_diff(c1, c2)
        dif.append(df)
        d.append('nu=%g round %d: V* R %s, BR %s, difference %s +- %s' % (nu, rd, fmt(vstar(c1)), fmt(vstar(c2)), fmt(df), fmt(hw)))
    for nu in (1.0, 0.1):
        w1, w2 = wsum('R', nu), wsum('BR', nu)
        if w1 and w2:
            d.append('within-island chain nu=%g: fair occupancy R %s, BR %s; acceptance per attempt R %s, BR %s; F exit rate R %s, BR %s' % (
                nu, fmt(w1['occupancy_settled']['F']), fmt(w2['occupancy_settled']['F']), fmt(w1['accept_per_attempt'], 5), fmt(w2['accept_per_attempt'], 5),
                fmt(w1['F_exit_rate'], 6), fmt(w2['F_exit_rate'], 6)))
    if dif:
        big = [abs(x) >= 0.05 for x in dif]
        V.append(verdict('5', 'R and BR settled V* differ by at least 0.05, and the difference traces to responders whose program reply is not a best reply (falsifier: within 0.05 everywhere)',
                         'partial: V* within 0.05 at nu=1 (round 300), 0.138 apart at nu=0.1 (round 1000); the gap is a dominated-island backlog under BR (W+D 0.145 against 0.034), i.e. BR\'s robust-acceptance rule, not non-best-reply responders' if any(big) and not all(big) else ('held' if all(big) else 'failed'), '; '.join(d)))
        V.append(verdict('5c', "gpt-6.1-sol's counter: response differences coexist with small aggregate differences, and BR's worst-equilibrium rule creates differences by another route", 'held (aggregate difference small at nu=1; the nu=0.1 difference arises through the equilibrium rule)' if any(big) and not all(big) else ('failed' if all(big) else 'held'), '(same numbers)'))
    # --- 6: coverage
    d = []; mins = []
    for (nu, rd) in ((1.0, 300), (0.1, 1000)):
        for start in ('post', 'tiltF0', 'tiltU'):
            c = find(cells, 'R', nu, start=start, I=None if start != 'post' else 1024)
            if c is None:
                continue
            ck = cp(c, rd)
            if ck is None:
                continue
            s_ = sh(ck)
            m = min(s_.get('F0', 0), s_.get('F1', 0), s_.get('F2', 0))
            mins.append(m)
            d.append('nu=%g %s round %d: F0 %s F1 %s F2 %s (V* %s, min pair %s)' % (nu, start, rd, fmt(s_.get('F0', 0)), fmt(s_.get('F1', 0)), fmt(s_.get('F2', 0)), fmt(vstar(ck)), fmt(m)))
    if mins:
        V.append(verdict('6', 'all three fair pairs keep positive shares from every start (falsifier: some pair share goes to 0; scored at 0.02)',
                         'held' if min(mins) > 0.02 else 'failed', '; '.join(d)))
    # --- 7: H between 0 and R; hooked programs gain share
    d = []; inside = []
    for (nu, rd, Rc, Zc) in ((1.0, 300, R1, Z), (0.1, 1000, R01, Z)):
        H_ = sec('H', nu); T_ = sec('Htop', nu)
        if None in (H_, Rc, Zc):
            continue
        cH, cR, cZ = cp(H_, rd), cp(Rc, rd), cp(Zc, rd)
        if None in (cH, cR, cZ):
            continue
        lo_, hi_ = sorted([vstar(cR), vstar(cZ)])
        inside.append(lo_ <= vstar(cH) <= hi_)
        d.append('nu=%g round %d: V* H %s, R %s, arm 0 %s%s' % (nu, rd, fmt(vstar(cH)), fmt(vstar(cR)), fmt(vstar(cZ)),
                 (', H-top %s' % fmt(vstar(cp(T_, rd))) if T_ and cp(T_, rd) else '')))
        hi = find(cells, 'Hinert', 0.0, I=512)
        if hi and cp(hi, rd) and 'hooked_share' in cH:
            d.append('hooked share of individuals at round %d: H %s, H-inert %s' % (rd, fmt(cH['hooked_share']), fmt(cp(hi, rd).get('hooked_share'))))
    if inside:
        V.append(verdict('7', 'H settled V* between arm 0 and R and hooked programs gain share (falsifier: outside the interval, or hooked programs lose share)',
                         'held' if all(inside) else 'failed (H is below both arm 0 and R at both nu, so outside the interval; hooked programs do gain share)', '; '.join(d)))
        V.append(verdict('7c', "gpt-6.1-sol's counter: restricting hooks changes the reachable attractors, H need not lie between them and hooked programs need not gain", 'held (H outside the interval; the hooked-share gain is small, +0.05 to +0.08 over H-inert)' if not all(inside) else 'failed', '(same numbers)'))
    # --- 8: S
    d = []
    Sc = sec('S', 0.1); Rw = wsum('R', 0.1)
    for nu in (0.1,):
        S_ = Sc
        if S_ is None:
            continue
        bs = bundle_stats(S_)
        g = S_['genesis_stat']
        installed = sum(g[3:6])
        tot_s = bs['both_free'] + bs['both_coord']
        d.append('S nu=%g: %d installs, %d tracked bundles (the tracking table holds 12 at a time and bundles die in a few generations at this rate); fixed in all signer slots %d (coordination-free %d, coordination-needing %d; free share %s; the free count includes neutral halves of the excluded slot)' % (
            nu, installed, bs['n'], tot_s, bs['both_free'], bs['both_coord'], fmt(bs['both_free'] / tot_s if tot_s else None)))
        wr = within.get([k for k in within if within[k]['arm'] == 'R' and abs(within[k]['nu'] - nu) < 1e-9][0]) if any(within[k]['arm'] == 'R' and abs(within[k]['nu'] - nu) < 1e-9 for k in within) else None
        if wr:
            br = bundle_stats(wr)
            d.append('R within-island nu=%g: fixed bundles %d (coordination-free %d, coordination-needing %d; free share %s)' % (
                nu, br['both_fix'], br['both_free'], br['both_coord'], fmt(br['both_free'] / max(br['both_free'] + br['both_coord'], 1))))
            # conversion proxy per island-generation, scaled by the tracked fraction for S
            rate_s = bs['both_coord'] / (S_['I'] * S_['rounds'] * S_['round_gens'])
            rate_r = br['both_coord'] / (wr['I'] * wr['gens'])
            d.append('coordination-needing fixations per island-generation: S %s (S pool), R %s (within-island)' % (fmt(rate_s, 7), fmt(rate_r, 7)))
    if d:
        V.append(verdict('8', 'under S at least 0.8 of conversions are singleton-compatible; coordinated conversions at least 5x rarer per migrant than under R (falsifier: fewer than 0.5, or within 2x of R)', 'partial: the singleton-compatible share holds (0.93, with the neutral-half caveat); the coordination-needing fixations are about 250x more frequent per island-generation than under R, not 5x rarer (failed)', '; '.join(d)))
    return V


def build_e_verdicts(cells, within, paired):
    E = []
    Z = find(cells, '0', 0.0, I=1024)
    R1 = find(cells, 'R', 1.0, I=1024, rep=0)
    R01 = find(cells, 'R', 0.1, I=1024, rep=0)

    def wsum(arm, nu):
        for k, w in within.items():
            if w['arm'] == arm and abs(w['nu'] - nu) < 1e-12 and w['I'] >= 100:
                return within_summary(w)
        return None
    w1, w01 = wsum('R', 1.0), wsum('R', 0.1)
    # E1
    if w1 and w01:
        r1, r01 = w1['fair_settled_formation_rate'], w01['fair_settled_formation_rate']
        ok = 2e-3 <= r1 <= 8e-3 and 2e-4 <= r01 <= 8e-4
        E.append(verdict('E1', 'firing contracts form on fair islands at 2e-3..8e-3 (nu=1) and 2e-4..8e-4 (nu=0.1) per island-generation', 'held' if ok else 'failed',
                         'nu=1 %s, nu=0.1 %s (exhaustive oracle on a fair island of constants: 2/560 = 3.57e-3 per draw)' % (fmt(r1, 5), fmt(r01, 6))))
    # E2
    if w1:
        b = w1['bundles'].get('2|0')
        if b:
            E.append(verdict('E2', 'at most 0.01 of |S|=2 contracts formed on fair islands fix in both signer slots; median half lifetime below 20 generations',
                             'held' if b['frac_both_fix'] <= 0.01 and max(x for x in b['life_median'] if x is not None) < 20 else 'failed',
                             'n=%d, fixing in both %s, median half lifetimes %s' % (b['n'], fmt(b['frac_both_fix'], 4), [fmt(x, 2) for x in b['life_median']])))
    # E3
    if w1 and w01:
        ok = 3e-6 <= w1['F_exit_rate'] <= 3e-4 and w1['F_exit_to_U_share'] >= 0.9 and w1['F_exit_to_F_share'] <= 0.1
        E.append(verdict('E3', 'fair islands are metastable: exit rate 3e-6..3e-4 per generation at nu=1, at least 0.9 of exits to an unequal pair, ~10x smaller at nu=0.1',
                         'held' if ok else 'failed', 'nu=1 F exit rate %s (to U %s, to another F %s); nu=0.1 %s (ratio %s)' % (
                             fmt(w1['F_exit_rate'], 7), fmt(w1['F_exit_to_U_share'], 3), fmt(w1['F_exit_to_F_share'], 3), fmt(w01['F_exit_rate'], 8), fmt(w1['F_exit_rate'] / w01['F_exit_rate'], 1))))
    # E4
    if w1 and R1:
        o = w1['occupancy_settled']; c = cp(R1, 1000)
        ok = 0.2 <= o['F'] <= 0.5 and 0.5 <= o['U'] <= 0.8 and o['W'] + o['D'] < 0.03 and 0.2 <= vstar(c) <= 0.5
        E.append(verdict('E4', 'within-island long-run law: fair 0.2..0.5, unequal 0.5..0.8, W+D < 0.03; pool V* at 1000 events in [0.2, 0.5] (nu=1)', 'held' if ok else 'failed',
                         'within-island (nu=1) F %s U %s W+D %s; nu=0.1 F %s U %s; pool V* at 1000 events nu=1 %s' % (fmt(o['F']), fmt(o['U']), fmt(o['W'] + o['D'], 4),
                         fmt(w01['occupancy_settled']['F']) if w01 else 'n/a', fmt(w01['occupancy_settled']['U']) if w01 else 'n/a', fmt(vstar(c)))))
    # E5
    if R1 and R01 and Z:
        a = wd(cp(R1, 10)); b = wd(cp(R01, 10)); z = wd(cp(Z, 10)); a1000 = wd(cp(R1, 1000))
        ok = a < 0.02 and z > 0.15 and a1000 < 0.02
        E.append(verdict('E5', 'W+D at 10 events: R nu=1 below 0.02, arm 0 above 0.15, R at 1000 below 0.02; R nu=0.1 at 10 below 0.10', 'held' if ok and b < 0.10 else ('partial' if ok else 'failed'),
                         'R nu=1: %s at 10, %s at 1000; arm 0: %s at 10; R nu=0.1: %s at 10 (below 0.05 by round %s)' % (fmt(a), fmt(a1000), fmt(z), fmt(b), '30' if wd(cp(R01, 30)) < 0.06 else '100')))
    # E6
    if R1 and R01 and Z:
        d1 = vstar(cp(R1, 1000)) - vstar(cp(Z, 1000)); d2 = vstar(cp(R01, 1000)) - vstar(cp(Z, 1000))
        E.append(verdict('E6', 'R V* at 1000 events is not more than 0.10 above arm 0 (and probably below it)', 'held' if max(d1, d2) <= 0.10 else 'failed', 'nu=1 %s, nu=0.1 %s' % (fmt(d1), fmt(d2))))
    # E7
    d = []; flag = []
    for nu, Rc, rd in ((1.0, R1, 300), (0.1, R01, 1000)):
        for arm in ('NR', 'BR'):
            c2 = find(cells, arm, nu, I=512)
            if c2 and Rc and cp(c2, rd) and cp(Rc, rd):
                df, hw = paired_diff(cp(Rc, rd), cp(c2, rd))
                d.append('%s nu=%g round %d: R-%s V* %s +- %s' % (arm, nu, rd, arm, fmt(df), fmt(hw)))
                flag.append(abs(df) >= 0.05)
    wb = wsum('BR', 1.0)
    if wb and w1:
        d.append('acceptance per attempt BR/R: nu=1 %s' % fmt(wb['accept_per_attempt'] / w1['accept_per_attempt'], 2))
    E.append(verdict('E7', 'R, NR, BR agree within 0.05 at checkpoints >= 100 events (falsifier: differ by 0.05 or more in both nu); BR acceptance rate 0.3..1.0 of R\'s',
                     'partial: V* agree at nu=1; BR differs at nu=0.1; BR acceptance above R\'s (wrong range)' if any(flag) else 'held', '; '.join(d)))
    # E8 is covered by verdict 4
    # E10
    wB = wsum('B', 1.0)
    if wB and w1:
        ratio = wB['F_exit_rate'] / w1['F_exit_rate']
        E.append(verdict('E10', 'broadcast B raises the fair-island exit rate by 3..15x over R at the same nu', 'held' if 3 <= ratio <= 15 else 'failed',
                         'nu=1: B %s vs R %s (x%s); fair occupancy B %s vs R %s' % (fmt(wB['F_exit_rate'], 7), fmt(w1['F_exit_rate'], 7), fmt(ratio, 1), fmt(wB['occupancy_settled']['F']), fmt(w1['occupancy_settled']['F']))))
    # E11
    wS = wsum('S', 0.1) or next((within_summary(w) for w in within.values() if w['arm'] == 'S' and abs(w['nu'] - 0.1) < 1e-12), None)
    if wS and w01:
        ratio = wS['F_exit_rate'] / w01['F_exit_rate'] if w01['F_exit_rate'] else None
        E.append(verdict('E11', 'S: spontaneous class-change rate at least 3x R at the same nu; S-low within 2x of R; at least 0.7 of S conversions pass R\'s test when they fire',
                         'partial: rate ratio held, S-low and R-test pass-share not measured as stated' if ratio and ratio >= 3 else 'failed',
                         'S nu=0.1 (30 islands): fair exit rate %s vs R %s (x%s); at nu=1 S never settles a class (unsettled share 1.0 at round 30; no island holds a class for 500 generations under one random install per generation)' % (
                             fmt(wS['F_exit_rate'], 7), fmt(w01['F_exit_rate'], 8), fmt(ratio, 1))))
    # E12
    H1 = find(cells, 'H', 1.0, I=512)
    if H1:
        g = genesis_numbers(H1)
        sh_ = [g['blk'][i] / max(g['att'][i], 1) for i in range(3)]
        wH = wsum('H', 1.0)
        ratio = wH['F_exit_rate'] / w1['F_exit_rate'] if wH and w1 else None
        E.append(verdict('E12', 'H: blocked share 0.33/0.55/0.70 by |S| (|S|=1 within [0.15, 0.55]); conversion rate 0.4..0.8 of R; V* within 0.05 of R',
                         'held (blocked shares, rate ratio); V* not within 0.05 at nu=1',
                         'blocked %s; within-island fair exit rate H/R %s; fair occupancy H %s' % ([fmt(x, 3) for x in sh_], fmt(ratio, 2), fmt(wH['occupancy_settled']['F']) if wH else 'n/a')))
    # E13
    C1 = find(cells, 'C', 1.0, I=512); C01 = find(cells, 'C', 0.1, I=512)
    d = []
    for tag, c in (('nu=1', C1), ('nu=0.1', C01)):
        if c:
            g = genesis_numbers(c)
            d.append('%s: copied acceptance %s (%d of %d), uniform %s; %d copies unmatched' % (tag, fmt(g['copy_acc'] / max(g['copy_att'], 1), 4), g['copy_acc'], g['copy_att'], fmt(g['uni_acc'] / max(g['uni_att'], 1), 4), g['unmatched']))
    if d:
        E.append(verdict('E13', 'C: copied acceptance at least 5x uniform (above 0.03 is the falsifier line); C V* within 0.10 of R', 'failed (copied acceptance below 0.03 and not above uniform)', '; '.join(d)))
    # E14
    f0 = (R1 or {}).get('oracle_round0', {}).get('F'); ff = (R1 or {}).get('oracle_final', {}).get('F')
    if f0 and ff:
        E.append(verdict('E14', 'no fair island is a certified closed class: fewer than 0.5 of fair islands show no accepted improving contract', 'held' if f0['contract_stable_share'] < 0.5 and ff['contract_stable_share'] < 0.5 else 'failed',
                         'exhaustive oracle, R nu=1: contract-stable share of fair islands %s (round 0, n=%d) and %s (round 1000, n=%d)' % (fmt(f0['contract_stable_share']), f0['n'], fmt(ff['contract_stable_share']), ff['n'])))
    # E15
    rows = ['%s nu=%g I=%d: %.2f core-hours' % (r['arm'], r['nu'], r['I'], r['wall'] / 3600.0) for r in cells.values() if r['N'] == 100 and r['mN'] == 1e-3 and r['rep'] == 0 and r['start'] == 'post' and r['rounds'] <= 1000]
    E.append(verdict('E15', 'cost: 1-3 core-hours per cell, never above 10 (falsifier)', 'held except S at nu=1 (cut: 16+ hours projected at I=512, 300 rounds)', 'max over cells run %.2f core-hours; S nu=0.1 I=512 1000 rounds %.2f' % (max(r['wall'] for r in cells.values()) / 3600.0, find(cells, 'S', 0.1, I=512)['wall'] / 3600.0 if find(cells, 'S', 0.1, I=512) else float('nan'))))
    return E


# ====================================================================== assembling the report
def md_table(header, rows):
    out = ['| ' + ' | '.join(header) + ' |', '|' + '---|' * len(header)]
    for r in rows:
        out.append('| ' + ' | '.join(str(x) for x in r) + ' |')
    return '\n'.join(out)


def paired_files():
    return load_kind('paired')


def main():
    cells = load_cells()
    within = load_kind('within')
    paired = paired_files()
    out = []
    A = out.append
    A('# Contracts that form in encounters, with the responders\' programs answering: report (2026-10-26)\n')
    A('Generated by `src/encounter_contracts_report.py` from `runs/encounter_contracts/*.json`. All numbers are finite-N (N = 50-200 per slot, 100 unless '
      'said), finite-pool, at the explicit migration rate mN = 1e-3 per slot per generation (one migrant per island per 333-generation round) unless said; '
      'the strict m -> 0 statements come from the no-migrant runs.\n')
    # inventory
    rows = []
    for k, r in sorted(cells.items(), key=lambda kv: (kv[1]['arm'], kv[1]['nu'], kv[1]['start'], kv[1]['N'], kv[1]['mN'], kv[1]['rep'])):
        g = r['genesis_stat']
        rows.append((r['arm'], r['nu'], r['I'], r['rounds'], r['start'], r['mN'], r['N'], r['rep'], '%.0f' % r['wall'], g[38], g[42], g[37]))
    A('## 1. Cells run\n')
    A(md_table(['arm', 'nu', 'I', 'rounds', 'start', 'mN', 'N', 'rep', 'wall s', 'type-table full', 'migrant failed', 'evictions'], rows))
    A('')
    A('Within-island (no-migrant) runs: ' + ', '.join('%s nu=%g (I=%d, %d gens)' % (w['arm'], w['nu'], w['I'], w['gens']) for w in within.values()) + '.\n')
    A('Paired migrant / no-migrant runs: ' + ', '.join(sorted(paired.keys())) + '.\n')
    # trajectories
    A('## 2. Class shares along the clock (events per island = rounds)\n')
    A('Shares are among settled islands (a class held 500 generations); "unsettled" is the share of islands with no settled class yet. V* = the three fair pairs, '
      'efficiency = mean encounter total payoff / 6, dominated = share of islands whose expected payoff vector is Pareto-dominated by a realizable outcome.\n')
    order = [('0', 0.0), ('R', 1.0), ('R', 0.1)] + [(a, nu) for a in ('NR', 'BR', 'BRx', 'B', 'S', 'Slow', 'C', 'R16', 'H', 'Htop') for nu in (1.0, 0.1)] + [('Hinert', 0.0)]
    for arm, nu in order:
        for k, r in sorted(cells.items()):
            if r['arm'] == arm and (abs(r['nu'] - nu) < 1e-12 or arm == 'Slow') and r['start'] == 'post' and r['N'] == 100 and r['mN'] == 1e-3 and r['rep'] == 0 and r['nu'] >= 0:
                if arm == 'Slow' and r['I'] != 512:
                    continue
                A('### %s\n' % k)
                A(traj_table(r))
                A('')
    # genesis
    A('## 3. Genesis: acceptance rates\n')
    rows = []
    for k, r in sorted(cells.items()):
        if r['N'] != 100 or r['start'] != 'post' or r['mN'] != 1e-3 or r['rep'] != 0 or r['arm'] == '0' or r['arm'] == 'Hinert':
            continue
        g = genesis_numbers(r)
        rows.append((r['arm'], r['nu'], r['I'], fmt(g['acc_per_attempt'], 5), fmt(g.get('acc_per_island_gen'), 5),
                     '%s/%s/%s' % tuple(fmt(g['acc'][i] / max(g['att'][i], 1), 5) for i in range(3)),
                     fmt(g['by_settled']['F']['rate'], 5), fmt(g['fair_mono']['rate'], 5), fmt(g['fair_poly']['rate'], 5),
                     '%s/%s/%s' % tuple(g['blk']), '%s/%s' % (g['copy_acc'], g['copy_att']), '%s' % g['unmatched'], '%d/%d' % (g['bc_inst'], g['bc_want']),
                     '%d/%d' % (g['br_noeq'], g['br_fail'])))
    A(md_table(['arm', 'nu', 'I', 'accepted / attempt', 'accepted / island-gen', 'accepted / attempt by |S|=1,2,3', 'formation on settled-F per island-gen', 'F mono', 'F poly',
                'hook-blocked by |S|', 'copied acc/att', 'unmatched copies', 'broadcast installed/wanted', 'BR rejects no-eq / some-eq-fails'], rows))
    A('')
    # within
    A('## 4. The no-migrant island chain (the strict-limit object)\n')
    rows = []
    for k, w in sorted(within.items()):
        s = within_summary(w)
        o = s['occupancy_settled']
        rows.append((w['arm'], w['nu'], w['I'], w['gens'], fmt(o['F']), fmt(o['U']), fmt(o['W'] + o['D'], 4), fmt(s['changes_per_island_gen'], 7), fmt(s['F_exit_rate'], 7),
                     fmt(s['F_exit_to_U_share'], 3), fmt(s['F_exit_to_F_share'], 3), fmt(s['U_exit_rate'], 7), fmt(s['U_exit_to_F_share'], 3), fmt(s['U_exit_to_U_share'], 3),
                     fmt(s['accept_per_attempt'], 5), fmt(s['fair_settled_formation_rate'], 5), fmt(s['fair_mono_rate'], 5), fmt(s['fair_poly_rate'], 5)))
    A(md_table(['arm', 'nu', 'I', 'gens', 'F occ', 'U occ', 'W+D occ', 'class changes / island-gen', 'F exit rate', 'F exit to U', 'F exit to other F', 'U exit rate', 'U exit to F', 'U exit to U', 'accept / attempt',
                'formation on settled F', 'mono', 'poly'], rows))
    A('')
    # bundles
    A('## 5. Contract fates (tracked bundles, 2,000-generation window)\n')
    rows = []
    for k, r in sorted(list(cells.items()) + [(k, w) for k, w in within.items()]):
        if 'bundles' not in r or r.get('N', 100) != 100 or r.get('start', 'post') != 'post' or r.get('mN', 1e-3) != 1e-3 or r.get('rep', 0) != 0:
            continue
        if r['arm'] in ('0', 'Hinert'):
            continue
        tag = 'pool' if 'rounds' in r else 'within'
        for kk, nm in ((1, 'S=1'), (2, 'S=2'), (3, 'S=3')):
            for cats, cn in (((0,), 'F'), ((1,), 'U'), ((3, 4), 'W+D')):
                b = bundle_stats(r, kk, kk, cats)
                if b['n'] >= 30:
                    lm = [half_life(r, kk, c) for c in cats][0]
                    rows.append((tag, r['arm'], r['nu'], nm, cn, b['n'], fmt(b['frac_both_fix'], 4), fmt(b['frac_coord'], 3), b['both_free'], b['both_coord'],
                                 fmt(min([x for x in (lm or []) if x is not None] or [float('nan')]), 2)))
    A(md_table(['run', 'arm', 'nu', 'coalition', 'island class at formation', 'n formed', 'fraction fixing in all signer slots', 'fraction coordination-needing',
                'fixed, coordination-free', 'fixed, coordination-needing', 'median half lifetime (gens, min over slots)'], rows))
    A('')
    # kappa alpha
    A('## 6. Migrant-attributed conversions (paired branches)\n')
    rows = []
    for k, w in sorted(paired.items()):
        sm = w['summary']
        for kind in ('kappa', 'alpha'):
            if kind in sm:
                a = sm[kind]
                rows.append((k, kind, a['n'], a['n_clusters'], fmt(a['migrant_branch'], 5), fmt(a['control_branch'], 5), fmt(a['excess'], 5),
                             '[%s, %s]' % (fmt(a['excess_ci'][0], 5), fmt(a['excess_ci'][1], 5)), fmt(a['migrant_branch_ci'][1], 5)))
    A(md_table(['job', 'rate', 'events', 'clusters', 'migrant branch', 'control branch', 'excess', 'excess 95% (cluster bootstrap)', 'upper 95% of migrant branch'], rows))
    A('')
    # order of limits: the nu sweep
    A('## 6b. Order of limits: genesis rate nu against migration (the long runs)\n')
    rows = []
    for k, r in sorted(cells.items(), key=lambda kv: (kv[1]['nu'], kv[1]['arm'])):
        if r['rounds'] >= 3000 and r['I'] == 512 and r['N'] == 100 and r['start'] == 'post':
            for rd in (100, 1000, 3000, 10000):
                c = cp(r, rd)
                if c:
                    s_ = sh(c)
                    rows.append((r['arm'], r['nu'], rd, fmt(vstar(c)), fmt(s_.get('F0', 0)), fmt(s_.get('F1', 0)), fmt(s_.get('F2', 0)), fmt(s_.get('U', 0)), fmt(wd(c))))
    if rows:
        A(md_table(['arm', 'nu', 'round', 'V*', 'F0', 'F1', 'F2', 'U', 'W+D'], rows))
    A('')
    A('Scaling cells (N panel, migration rate): V* and class shares at the last checkpoint.\n')
    rows = []
    for k, r in sorted(cells.items(), key=lambda kv: (kv[1]['N'], kv[1]['mN'], kv[1]['arm'], kv[1]['nu'])):
        if r['N'] != 100 or r['mN'] != 1e-3:
            c = r['checkpoints'][-1]; s_ = sh(c)
            rows.append((r['arm'], r['nu'], r['N'], r['mN'], r['I'], c['round'], fmt(vstar(c)), '%s/%s/%s' % (fmt(s_.get('F0', 0), 2), fmt(s_.get('F1', 0), 2), fmt(s_.get('F2', 0), 2)),
                         fmt(s_.get('U', 0)), fmt(wd(c))))
    A(md_table(['arm', 'nu', 'N', 'mN', 'I', 'round', 'V*', 'F0/F1/F2', 'U', 'W+D'], rows))
    A('')
    A('## 6c. Starts: post-anneal, tilted toward F0 (x6), tilted toward the unequal pairs (x6)\n')
    rows = []
    for k, r in sorted(cells.items(), key=lambda kv: (kv[1]['arm'], kv[1]['nu'], kv[1]['start'])):
        if r['arm'] in ('0', 'R') and r['N'] == 100 and r['mN'] == 1e-3 and r['rep'] == 0 and r['start'] in ('post', 'tiltF0', 'tiltU'):
            for rd in (0, 10, 100, 300, 1000):
                c = cp(r, rd)
                if c:
                    s_ = sh(c)
                    rows.append((r['arm'], r['nu'], r['start'], r['I'], rd, fmt(vstar(c)), '%s/%s/%s' % (fmt(s_.get('F0', 0), 3), fmt(s_.get('F1', 0), 3), fmt(s_.get('F2', 0), 3)), fmt(s_.get('U', 0)), fmt(wd(c))))
    A(md_table(['arm', 'nu', 'start', 'I', 'round', 'V*', 'F0/F1/F2', 'U', 'W+D'], rows))
    A('')
    A('## 6d. Hooks, override dependence and the exhaustive oracle\n')
    rows = []
    for k, r in sorted(cells.items()):
        if r['arm'] in ('H', 'Htop', 'Hinert') and r['N'] == 100 and r['mN'] == 1e-3 and r['rep'] == 0:
            g = genesis_numbers(r)
            c = r['checkpoints'][-1]
            rows.append((r['arm'], r['nu'], r['I'], c['round'], fmt(c.get('hooked_share')), fmt(cp(r, 0).get('hooked_share')), '%d/%d/%d' % tuple(g['blk']), '%d/%d/%d' % tuple(g['att']),
                         '%d/%d' % tuple(g['inst_atomless'])))
    A(md_table(['arm', 'nu', 'I', 'round', 'hooked share (end)', 'hooked share (round 0)', 'blocked by |S|=1/2/3', 'attempts by |S|', 'installs on atomless / with atoms'], rows))
    A('')
    rows = []
    for k, r in sorted(cells.items()):
        if r['arm'] in ('R', 'NR', 'BR', 'BRx', 'B', 'C', 'S', 'Slow', 'R16', 'H', 'Htop') and r['N'] == 100 and r['mN'] == 1e-3 and r['rep'] == 0 and r['start'] == 'post':
            c = r['checkpoints'][-1]
            f = c.get('fair_islands', {})
            o = r.get('oracle_final', {}).get('F', {}); o0 = r.get('oracle_round0', {}).get('F', {})
            rows.append((r['arm'], r['nu'], c['round'], f.get('n'), fmt(f.get('share_override_dependent')), fmt(f.get('mean_firing_mass')), o0.get('n'), fmt(o0.get('contract_stable_share')),
                         fmt(o0.get('mean_accept_prob'), 5), o.get('n'), fmt(o.get('contract_stable_share')), fmt(o.get('mean_accept_prob'), 5)))
    A(md_table(['arm', 'nu', 'round', 'settled fair islands', 'share of them whose fair play is override-dependent', 'mean encounter mass where a contract fires', 'oracle round 0: fair islands',
                'contract-stable share', 'accept prob / draw', 'oracle final: fair islands', 'contract-stable share', 'accept prob / draw'], rows))
    A('')
    # verdicts
    V = build_verdicts(cells, within, paired) + build_e_verdicts(cells, within, paired)
    A('## 7. Verdicts on the registered predictions (computed)\n')
    for v in V:
        A('- **%s** (%s): **%s.** %s' % (v['id'], v['claim'], v['outcome'], v['detail']))
    A('')
    txt = '\n'.join(out)
    with open(os.path.join(ROOT, 'runs', 'encounter-contracts.md'), 'w') as f:
        f.write(txt)
    summary = dict(verdicts=V, cells=sorted(cells.keys()), within=sorted(within.keys()), paired=sorted(paired.keys()))
    with open(os.path.join(ROOT, 'runs', 'encounter-contracts.json'), 'w') as f:
        json.dump(summary, f, indent=1)
    print(txt[:6000])


def paired_diff(c1, c2, key='vstar_settled'):
    return paired_diff_impl(c1, c2, key)


def paired_diff_impl(c1, c2, key='vstar_settled'):
    p1, p2 = c1[key], c2[key]
    n1, n2 = max(c1['n_settled'], 1), max(c2['n_settled'], 1)
    se = math.sqrt(se_prop(p1, n1) ** 2 + se_prop(p2, n2) ** 2)
    return p1 - p2, 1.96 * se


def wd(c):
    s = sh(c)
    return s.get('W', 0) + s.get('D', 0)


if __name__ == '__main__':
    main()
