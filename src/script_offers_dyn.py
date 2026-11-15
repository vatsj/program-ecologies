"""Step 2 of queue 80 (spec specs/2026-11-16-script-checked-offers.md): arm T at (KR', cap') over the world-S (script checker, S1 tables)
and world-K (queue 79's skeleton check CHK, C1) catalogues, in queue 74's simulator with queue 78's kernel (mN = 1, Lambda = 100,
100N + 20N, CRN), with queue 79's law arithmetic.

Laws (family totals; founders and tail alike).  Constants share 1 - delta - beta delta - ex - extra uniformly (nine), exploiters
ex = 0.01 delta / 0.09, bullies beta delta (a share phi certified, Bc), readers delta, accepters gamma delta (gamma = 1) out of the constants.
  U      queue 78's F (singles 2/3, twos 1/3 of delta; phi = 0) and FR (F plus R = Rnn, Rpn at gamma delta); arm strings UF, UFR
  K      world K, canonical skeleton carriers: delta/2 Fc (Snoy, Spoy), delta/2 Oc (n, p), Rc (n, p) at gamma delta, Bc canonical
  K2     world K, each family's mass split evenly over its five spellings (four rejected by CHK)
  A1     world S, canonical spellings: Fc + Oc + Rc, Bc
  A2     world S, each family's mass split over its five spellings
  A3     world S, Fc+ + Oc+ + Rc+ (R = {}), Bc; A2's split
  A4     world S, Pc+ (delta/2) + Oc+ (delta/2) + Rc+ (gamma delta), Bc; A2's split
  A5     world S, Pc+ + OcR+ + RcR+ (everyone requires S_nx), Bc; A2's split
  UF0, UFR0   the U arms at the old fuel on queue 78's 59 programs (V1)

Spec strings: sco:arm=<A>:d=<delta>:b=<beta>:ph=<phi>[:seed=unequal].  Seeded start (unequal): every island on (Bn, C3, C8) and its rotations.
"""
import os, sys, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import majority_tail as MT
import migration_window as MW
import churn_primary as CP
import tplus as TP
import script_offers as S
import script_offers_cat as SC
import script_offers_tables as ST
from bully_resist_step0 import rho_exact

PFAIL0 = MT.PFAIL
_G = {}
MCAP = 600000
XS = np.array(MW.X)
BASEF = ['c_third', 'c_half', 'c_two3', 'c_grand', 'single', 'two', 'exploit', 'bully', 'junk', 'prudent', 'prudent_a', 'opener',
         'single2', 'accepter']
SFAM = list(S.FAM_S)
KFAM = ['k_open', 'k_acc', 'k_firm', 'k_bully']
FAMN = BASEF + SFAM + KFAM
FAMCODE = {f: i for i, f in enumerate(FAMN)}
FAMCODE.update(junk_f=FAMCODE['junk'], junk_r=FAMCODE['junk'])
BULLYF = ('s_bully', 'k_bully')
ACCF = ('accepter', 's_acc', 's_acc+', 's_accR+', 'k_acc')


class Tabs(TP.TabsPlus):
    def __init__(self, cat, code, steps, nto, fo):
        n = cat.Kc
        self.cat = cat
        self.names, self.fam, self.spell, self.K = cat.names[:n], cat.fam[:n], cat.spell[:n], n
        self.meta = cat.meta[:n]
        for m in self.meta:
            if m.get('carrier'):
                m['cert'] = (m['fn'], m['fp'], m['pf'])
            else:
                m['cert'] = None
        self.code, self.steps, self.nto, self.fo = code[:n], steps[:n], nto[:n], fo[:n]
        self._joint()


def world_of(arm):
    if arm in ('UF0', 'UFR0'):
        return 'O'
    if arm in ('K', 'K2'):
        return 'K'
    return 'S'


def tabs(world):
    if world not in _G:
        TP.install_counter(); S.set_regress(True)
        if world == 'S':
            cat, c, s, n, f = ST.get_tables('S', 'S1', forg=False)
        elif world == 'K':
            cat, c, s, n, f = ST.get_tables('K', 'C1')
        else:
            path = os.path.join(ST.CACHE, 'sco_O59.npz')
            cat = SC.Cat('S', cap=400)
            if os.path.exists(path):
                z = np.load(path); c, s, n, f = z['code'], z['steps'], z['nto'], z['fo']
            else:
                cat, c, s, n, f = SC.build_tables('S', machine='S1', cap=400, fuel=1200, rows=list(range(59)), cols=list(range(59)),
                                                  workers=int(os.environ.get('DAYTONA_CPUS', 3)), s1tab={}, regress=True)
                c, s, n, f = c[:59], s[:59], n[:59], f[:59]
                np.savez_compressed(path, code=c, steps=s, nto=n, fo=f)
            cat.Kc = 59
        _G[world] = Tabs(cat, c, s, n, f)
    return _G[world]


def fam_table(tb):
    f = np.zeros(tb.K, np.int64)
    for p in range(tb.K):
        fm = tb.fam[p]
        if fm == 'const':
            a = int(tb.names[p][1:])
            f[p] = 3 if a // 3 == 2 else a % 3
        else:
            f[p] = FAMCODE[fm]
    return np.tile(f, (3, 1))


def ids(tb, fam, sp=None):
    return [i for i in range(tb.K) if tb.fam[i] == fam and (sp is None or tb.spell[i] == sp)]


ARMS = ('UF', 'UFR', 'K', 'K2', 'A1', 'A2', 'A3', 'A4', 'A5', 'UF0', 'UFR0')
FAMSETS = {   # arm -> (firm family, open family, accepter family, bully family, canonical only)
    'K': ('k_firm', 'k_open', 'k_acc', 'k_bully', True), 'K2': ('k_firm', 'k_open', 'k_acc', 'k_bully', False),
    'A1': ('s_firm', 's_open', 's_acc', 's_bully', True), 'A2': ('s_firm', 's_open', 's_acc', 's_bully', False),
    'A3': ('s_firm+', 's_open+', 's_acc+', 's_bully', False), 'A4': ('s_prud+', 's_open+', 's_acc+', 's_bully', False),
    'A5': ('s_prud+', 's_openR+', 's_accR+', 's_bully', False)}


def law_arm(arm, delta, beta, phi=0.5, gamma=1.0):
    tb = tabs(world_of(arm))
    K = tb.K
    uarm = arm in ('UF', 'UFR', 'UF0', 'UFR0')
    if uarm:
        phi = 0.0
    ex = 0.01 * delta / 0.09
    extra = gamma * delta if arm not in ('UF', 'UF0') else 0.0
    cst = 1.0 - delta - beta * delta - ex - extra
    assert cst > 0
    w = np.zeros(K)

    def spread(members, tot):
        assert members, arm
        for i in members:
            w[i] += tot / len(members)
    spread(ids(tb, 'const'), cst)
    spread(ids(tb, 'exploit'), ex)
    if beta > 0:
        if phi < 1:
            spread(ids(tb, 'bully'), beta * delta * (1 - phi))
    if uarm:
        spread(ids(tb, 'single'), delta * 2 / 3); spread(ids(tb, 'two'), delta / 3)
        if arm in ('UFR', 'UFR0'):
            spread([tb.names.index('Rnn'), tb.names.index('Rpn')], extra)
        assert (w[59:] == 0).all()
        return w / w[:59].sum()
    ff, fo, fa, fb, canon = FAMSETS[arm]
    sp = 'canon' if canon else None

    def fam_split(fam, tot):
        """the family's mass split evenly over its directions / fallbacks (2), and within each over its spellings."""
        mem = ids(tb, fam, sp)
        groups = {}
        for i in mem:
            groups.setdefault(tb.names[i].split('.')[0], []).append(i)
        for g in groups.values():
            spread(g, tot / len(groups))
    if beta > 0 and phi > 0:
        fam_split(fb, beta * delta * phi)
    fam_split(ff, delta / 2); fam_split(fo, delta / 2); fam_split(fa, extra)
    return w / w.sum()


SEED_TRIPLES = {'unequal': ('Bn', 'C3', 'C8')}


def seeded_init(tb, kind, I, N):
    a, b, c = SEED_TRIPLES[kind]
    base = (tb.names.index(a), tb.names.index(b), tb.names.index(c))
    tr = [base, (base[2], base[0], base[1]), (base[1], base[2], base[0])]
    init = np.zeros((I, 3, tb.K), np.int64)
    for i in range(I):
        for s in range(3):
            init[i, s, tr[i % 3][s]] = N
    return init


def parse(spec):
    parts = spec.split(':')
    assert parts[0] == 'sco', spec
    kv = dict(p.split('=', 1) for p in parts[1:] if '=' in p)
    out = dict(pf=float(kv.get('pf', PFAIL0)), seed=kv.get('seed'), arm=kv['arm'])
    d, b, ph = float(kv['d']), float(kv['b']), float(kv.get('ph', 0.5))
    out['w'] = law_arm(kv['arm'], d, b, ph)
    out.update(delta=d, beta=b, phi=ph)
    return out


def tables(world, pf):
    key = ('tables', world, round(pf, 9))
    if key not in _G:
        _G[key] = tabs(world).charged_tables(pf, MT.T)
    return _G[key]


def prepare(world, w, N, r, I, pf=PFAIL0, init=None):
    tb = tabs(world)
    init0, seed = MT.founders([w, w, w], 'CP-T-main', r, I, N)
    if init is not None:
        init0 = init
    sched = MT.make_schedule(N, r, I, 100.0)
    K = tb.K
    U = [np.arange(K, dtype=np.int64) for _ in range(3)]
    J, PAY, VEC, ISMEM, TOT = tables(world, pf)
    return dict(arm='SCO', variant='sco', N=N, r=r, I=I, init=init0, seed=seed, sched=sched, tail_laws=[w, w, w], U=U,
                loc=init0[:, :, :K].astype(np.int64), J=J, PAY=PAY, VEC=VEC, ISMEM=ISMEM, TOT=TOT, geo=MT.geometry(N))


def run_kernel_log(prep, lam, mN, H, snapg, mcap):
    import patient_accepter_kern as PK
    ag, ai, asl, au, lk = MT.local_arrivals(prep, lam)
    N = prep['N']
    out = PK.kern_pa(prep['J'], prep['PAY'], prep['VEC'], prep['ISMEM'], prep['TOT'], prep['loc'], N, MT.W, mN / N,
                     prep['seed'], H, 10, np.asarray(snapg, np.int64), ag, ai, asl, au, lk, 400000, 40000, mcap)
    keys = ('status', 'stop', 'counts', 'modal', 'majo', 'snapc', 'snapd', 'xlog', 'nx', 'alog', 'na', 'nmig', 'mlog', 'nm')
    res = dict(zip(keys, out))
    res['arr'] = (ag, ai, asl, au, lk)
    return res


def occupancy(tb, prep, res, g):
    """at snapshot generation g, by the majority triple of each island: fair islands' slots by role (pair / excluded) x family x
    spelling; Bc's paired slots by the partner's family; islands with Bc (or the simulating bully) on 2/3."""
    snaps = list(prep['geo']['snaps']) + ([240 * prep['N']] if g == 240 * prep['N'] else [])
    si = snaps.index(g)
    c = res['snapc'][si]
    out = dict(fair=0, unequal=0, hold={}, bc_pair_partner={}, bc_on_23=0, sb_on_23=0, unequal_holder={})
    for i in range(c.shape[0]):
        t = [int(np.argmax(c[i, s])) for s in range(3)]
        o = int(tb.VEC[tb.JT[t[0], t[1], t[2]]])
        cl = int(MW.CATMAP[o]); sh = XS[o]
        if cl == 0:
            out['fair'] += 1
            pair = [s for s in range(3) if sh[s] == 3]
            for s in range(3):
                role = 'pair' if s in pair else 'excl'
                k = '%s|%s|%s' % (role, tb.fam[t[s]] if tb.fam[t[s]] != 'const' else tb.names[t[s]], tb.spell[t[s]])
                out['hold'][k] = out['hold'].get(k, 0) + 1
            if len(pair) == 2:
                for s in pair:
                    if tb.fam[t[s]] in BULLYF:
                        q = t[[x for x in pair if x != s][0]]
                        pk = tb.fam[q] if tb.fam[q] != 'const' else tb.names[q]
                        out['bc_pair_partner'][pk] = out['bc_pair_partner'].get(pk, 0) + 1
        elif cl == 1:
            out['unequal'] += 1
            b = [s for s in range(3) if sh[s] == 4]
            if len(b) == 1:
                f = tb.fam[t[b[0]]]
                out['bc_on_23'] += int(f in BULLYF); out['sb_on_23'] += int(f == 'bully')
                k = f if f != 'const' else tb.names[t[b[0]]]
                out['unequal_holder'][k] = out['unequal_holder'].get(k, 0) + 1
    return out


def charges(tb, prep, res, pf=PFAIL0):
    N = prep['N']
    ch = pf * (tb.NTO.astype(np.float64) + tb.FO.astype(np.float64))
    fam = fam_table(tb)[0]
    nf = len(FAMN)
    snaps = list(prep['geo']['snaps'])
    out = {}
    for tag, g in (('120N', 120 * N),):
        c = res['snapc'][snaps.index(g)].astype(np.float64) / N
        num = np.zeros(nf); den = np.zeros(nf)
        for i in range(c.shape[0]):
            q0, q1, q2 = c[i, 0], c[i, 1], c[i, 2]
            e0 = np.einsum('b,c,abc->a', q1, q2, ch[..., 0], optimize=True)
            e1 = np.einsum('a,c,abc->b', q0, q2, ch[..., 1], optimize=True)
            e2 = np.einsum('a,b,abc->c', q0, q1, ch[..., 2], optimize=True)
            for q, e in ((q0, e0), (q1, e1), (q2, e2)):
                np.add.at(num, fam, q * e); np.add.at(den, fam, q)
        tot = den.sum()
        out[tag] = {FAMN[f]: [round(float(num[f] / den[f]), 5), round(float(den[f] / tot), 6)] for f in range(nf) if den[f] > 0}
        out[tag]['all'] = round(float(num.sum() / tot), 5)
    return out


def scramble(prep, res):
    N = prep['N']
    modal = res['modal'].astype(np.int64)
    c30 = MW.CATMAP[modal[30 * N]]; c120 = MW.CATMAP[modal[120 * N]]
    return dict(same_class=float(np.mean(c30 == c120)), fair30=float(np.mean(c30 == 0)), unequal30=float(np.mean(c30 == 1)))


# ---------------------------------------------------------------- pacing (seeded start), queue 79's records with this queue's families
def points_at(tb, x, sx, sy):
    c = tb.meta[x]['cert'] if tb.meta[x].get('carrier') else None
    if c is None:
        return False
    if tb.fam[x].startswith('k_') and tb.spell[x] != 'canon':
        return False                     # invisible to CHK
    return (c[0] if (sx + 1) % 3 == sy else c[1]) == 1


def offer_kind(tb, x, se, sv):
    if points_at(tb, x, se, sv):
        return 'cert'
    if tb.fam[x] == 'const':
        code = int(tb.code[x, 0, 0])
        if code % 3 == 1 and code // 3 < 2:
            tgt = (se + 1) % 3 if code // 3 == 0 else (se - 1) % 3
            if tgt == sv:
                return 'half'
    return 'none'


def roles_of(tb, t):
    o = int(tb.VEC[tb.JT[t[0], t[1], t[2]]])
    if MW.CATMAP[o] != 1:
        return None
    sh = XS[o]
    bs = [s for s in range(3) if sh[s] == 4]; vs = [s for s in range(3) if sh[s] == 2]
    if len(bs) != 1 or len(vs) != 1:
        return None
    return bs[0], vs[0], 3 - bs[0] - vs[0]


def pacing(tb, prep, res):
    """predicted (exact birth-death fixation of each arrival in its resident majority triple) against observed completions of the
    local accepter route out of bully-held unequal islands: accepters arriving in v (first step) and certified offerers arriving in e
    while an accepter holds v (second step); plus debounced unequal->fair exits and their hazard."""
    N = prep['N']; I = prep['I']
    NET = tb.payoff(PFAIL0, PFAIL0)
    init = prep['init']
    cur = [[int(np.argmax(init[i, s])) for s in range(3)] for i in range(I)]
    rows = sorted([tuple(int(x) for x in r) for r in res['mlog']], key=lambda r: (r[0], r[1], r[2]))
    ag, ai, asl, au, lk = res['arr']
    order = np.argsort(ag, kind='stable')
    took = {}
    for r in rows:
        if r[5] == 1:
            took.setdefault((r[1], r[2], r[4]), []).append(r[0])
    rec = dict(acc_expo=0, n_first=0, pred_first=0.0, n_second=0, pred_second=0.0, fixed_first=0, fixed_second=0)

    def state(i):
        ro = roles_of(tb, cur[i])
        if ro is None:
            return None
        b, v, e = ro
        return b, v, e, tb.fam[cur[i][v]] in ACCF
    st = [state(i) for i in range(I)]
    last = [0] * I
    H = int(res['modal'].shape[0]) - 1
    events = sorted(set([r[0] for r in rows] + [int(x) for x in ag]))
    ri = j = 0
    na = len(ag)
    for g in events:
        while ri < len(rows) and rows[ri][0] <= g:
            r = rows[ri]; i = r[1]
            if st[i] is not None and st[i][3]:
                rec['acc_expo'] += r[0] - last[i]
            last[i] = r[0]
            cur[i][r[2]] = r[4]; st[i] = state(i); ri += 1
        while j < na and ag[order[j]] <= g:
            k = order[j]; j += 1
            i = int(ai[k]); s = int(asl[k]); x = int(prep['U'][s][lk[k]])
            if st[i] is None:
                continue
            b, v, e, accv = st[i]
            t = list(cur[i])
            if x == t[s]:
                continue
            t2 = list(t); t2[s] = x
            p = rho_exact(float(NET[t2[0], t2[1], t2[2]][s] - NET[t[0], t[1], t[2]][s]), N)
            fixed = any(int(ag[k]) <= gg <= int(ag[k]) + 10 * N for gg in took.get((i, s, x), []))
            if s == e and accv and offer_kind(tb, x, e, v) == 'cert':
                rec['n_second'] += 1; rec['pred_second'] += p; rec['fixed_second'] += int(fixed)
            if s == v and tb.fam[x] in ACCF and tb.fam[x] != 'accepter':
                rec['n_first'] += 1; rec['pred_first'] += p; rec['fixed_first'] += int(fixed)
    for i in range(I):
        if st[i] is not None and st[i][3]:
            rec['acc_expo'] += H - last[i]
    rec['pred_first'] = round(rec['pred_first'], 6); rec['pred_second'] = round(rec['pred_second'], 6)
    L = max(1, int(round(0.25 * N)))
    cls = MW.CATMAP[res['modal'].astype(np.int64)].astype(np.int64)
    fl = CP.flips(cls, L)
    n_uf = sum(1 for ch in fl for (g, a, b) in ch if a == 1 and b == 0)
    occ = float((cls == 1).sum())
    rec.update(n_UF=int(n_uf), occ_U=occ, hazard=(n_uf / occ if occ else None))
    # observed local accepter routes: U->F flips whose new pair is (v, e) of the last unequal triple with an accepter in v
    obs = 0
    per = [[] for _ in range(I)]
    for r in rows:
        per[r[1]].append(r)
    for i in range(I):
        for (g, a, b) in fl[i]:
            if not (a == 1 and b == 0):
                continue
            m = [int(np.argmax(init[i, s])) for s in range(3)]
            prev_u = None
            for r in per[i]:
                if r[0] > g + L:
                    break
                if roles_of(tb, m) is not None:
                    prev_u = list(m)
                m[r[2]] = r[4]
            o = int(tb.VEC[tb.JT[m[0], m[1], m[2]]])
            if MW.CATMAP[o] == 0 and prev_u is not None:
                bb, vv, ee = roles_of(tb, prev_u)
                sh = XS[o]
                if sh[vv] == 3 and sh[ee] == 3 and tb.fam[m[vv]] in ACCF:
                    obs += 1
    rec['observed_routes'] = obs
    return rec


def run_cell(spec, N, r, I, long=False):
    pr = parse(spec)
    world = world_of(pr['arm'])
    tb = tabs(world)
    init = seeded_init(tb, pr['seed'], I, N) if pr['seed'] else None
    prep = prepare(world, pr['w'], N, r, I, pf=pr['pf'], init=init)
    geo = prep['geo']
    H = geo['Hlong'] if long else geo['H']
    snaps = list(geo['snaps']) + ([240 * N] if long else [])
    t0 = time.time()
    res = run_kernel_log(prep, 100, 1.0, H, snaps, MCAP)
    rec = MT.summarize(prep, res, 100, 1.0, fam_table(tb), long=long)
    rec['wall'] = round(time.time() - t0, 1)
    rec['charges'] = charges(tb, prep, res, pr['pf'])
    rec['scramble'] = scramble(prep, res)
    rec['occ120'] = occupancy(tb, prep, res, 120 * N)
    rec['occ30'] = occupancy(tb, prep, res, 30 * N)
    if long:
        rec['occ240'] = occupancy(tb, prep, res, 240 * N)
    if pr['seed']:
        rec['pacing'] = pacing(tb, prep, res)
    rec['mlog_overflow'] = int(res['nm']) > MCAP
    return rec


KEEP = ('vshare_ts', 'cons_modal', 'cons_majo', 'cons_modal_240', 'status', 'stop', 'wall', 'charges', 'scramble', 'occ120', 'occ30',
        'occ240', 'pacing', 'mlog_overflow', 'nmig')


def run_job(job, cache_dir=None):
    series, spec, N, I, r, long = job.split('|')
    N, I, r, long = int(N), int(I), int(r), bool(int(long))
    rec = run_cell(spec, N, r, I, long=long)
    out = dict(id=job, series=series, spec=spec, N=N, I=I, r=r, long=long)
    for k in KEEP:
        if k in rec:
            out[k] = rec[k]
    sn = rec['snap'][str(120 * N)]
    out['snap120'] = dict(cls_modal=sn['cls_modal'], pair_modal=sn['pair_modal'], cls_majo=sn['cls_majo'], fair_enc=sn['fair_enc'])
    if long:
        out['snap240'] = dict(cls_modal=rec['snap'][str(240 * N)]['cls_modal'])
    out['vstar'] = rec['vshare_ts'][120]
    return out
