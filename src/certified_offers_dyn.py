"""Step 2 of queue 79 (spec specs/2026-11-15-certified-offers.md): arm T over the 87-program catalogue of certified_offers.py (C1
tables) in queue 74's simulator (majority_tail), mN = 1, Lambda = 100, 100N + 20N, CRN; queue 78's patient_accepter_dyn with this
queue's laws, seeded starts and pacing records (nothing existing is edited).

Laws (family totals; founders and tail alike).  As queues 76/78: the nine constants uniform, exploiters 0.01 delta / 0.09, bullies
beta * delta, of which a share phi is the certified bully Bc (half Bcn, half Bcp) and 1 - phi the simulating bully (half Bn, half Bp);
readers delta split by arm; Rc (or Rcs, R, the 1/3 constants) at gamma * delta taken uniformly out of the nine constants:

  F, FR, FOR   queue 78's arms (phi forced to 0): F = singles 2/3, twos 1/3 of delta; FR adds R; FOR = delta/2 F, delta/2 O, plus R
  Fc           certified firm readers at delta, split like F (the 8 single-fallback Fc 2/3, the 8 two-fallback Fc 1/3)
  FcOc         delta/2 Fc, delta/2 Oc (Ocn, Ocp)
  FcOcRc       delta/2 Fc, delta/2 Oc, Rc at gamma delta (Rcn, Rcp)                       -- the main arm
  FcRc         Fc at delta, Rc at gamma delta
  FcOcRcs      delta/2 Fc, delta/2 Oc, Rcs at gamma delta (Rcsn, Rcsp)
  mix          delta/4 Fc, delta/4 Oc, delta/4 F (2:1), delta/4 O (the eight openers), Rc at gamma delta/2, R (Rnn, Rpn) at gamma delta/2
  FcOcC3       delta/2 Fc, delta/2 Oc, gamma delta to C3 and C0 (Rc with its certificate ablated plays the 1/3 constant)
  Fcs          Fc* : Fc's law on tables where every three-carrier cycle is broken by slot index (slots 0 and 1 pair) -- a comparator
  PcOcRc       delta/2 Pc (the four), delta/2 Oc, Rc at gamma delta

Spec strings:  co:arm=<A>:d=<delta>:b=<beta>:ph=<phi>[:g=<gamma>][:seed=<kind>].  Seeded kinds (every island on the exact triple, its
two rotations on a third of the islands each): unequal (Bn, C3, C8), unequalBc (Bcn, C3, C8), fair (C1, C4, C8), fairC (FcSnzn, FcSpzn, C8).
"""
import os, sys, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import majority_tail as MT
import migration_window as MW
import churn_primary as CP
import certified_offers as CO
from bully_resist_step0 import rho_exact

PFAIL0 = MT.PFAIL
_G = {}
FAMN = CO.FAMC
MCAP = 600000
FAMCODE = {'single': 4, 'two': 5, 'exploit': 6, 'bully': 7, 'junk_f': 8, 'junk_r': 8, 'prudent': 9, 'prudent_a': 10, 'opener': 11,
           'single2': 12, 'accepter': 13, 'c_open': 14, 'c_firm': 15, 'c_acc': 16, 'c_accs': 17, 'c_bully': 18, 'c_prud': 19}


def tabs(cache_dir=None):
    if 'tabs' not in _G:
        _G['tabs'] = CO.TabsCO(cache_dir=cache_dir or os.path.join(ROOT, 'runs', '_cache'), machine='C1')
    return _G['tabs']


def fam_table():
    tb = tabs()
    f = np.zeros(tb.K, np.int64)
    for p in range(tb.K):
        fm = tb.fam[p]
        if fm == 'const':
            a = int(tb.names[p][1:])
            f[p] = 3 if a // 3 == 2 else a % 3
        else:
            f[p] = FAMCODE[fm]
    return np.tile(f, (3, 1))


def ids(fam, tag=None):
    tb = tabs()
    return [i for i in range(tb.K) if tb.fam[i] == fam and (tag is None or tag(tb.names[i]))]


def idx(name):
    return tabs().cat.idx[name]


ARMS = ('F', 'FR', 'FOR', 'Fc', 'FcOc', 'FcOcRc', 'FcRc', 'FcOcRcs', 'mix', 'FcOcC3', 'Fcs', 'PcOcRc')
EXTRA_ARMS = ('FR', 'FOR', 'FcOcRc', 'FcRc', 'FcOcRcs', 'mix', 'FcOcC3', 'PcOcRc')
OLD_ARMS = ('F', 'FR', 'FOR')


def law_arm(arm, delta, beta, phi=0.5, gamma=1.0):
    tb = tabs()
    K = tb.K
    if arm in OLD_ARMS:
        phi = 0.0
    ex = 0.01 * delta / 0.09
    extra = gamma * delta if arm in EXTRA_ARMS else 0.0
    cst = 1.0 - delta - beta * delta - ex - extra
    assert cst > 0, (arm, delta, beta, gamma)
    w = np.zeros(K)
    for i in ids('const'):
        w[i] = cst / 9
    for i in ids('exploit'):
        w[i] = ex / 2
    for i in ids('bully'):
        w[i] = beta * delta * (1 - phi) / 2
    for i in ids('c_bully'):
        w[i] = beta * delta * phi / 2

    def spread(members, tot):
        for i in members:
            w[i] += tot / len(members)
    Fs, Ft, O = ids('single'), ids('two'), ids('opener')
    Fcs = [i for i in ids('c_firm') if tb.names[i][2] == 'S']
    Fct = [i for i in ids('c_firm') if tb.names[i][2] == 'D']
    Oc, Rc, Rcs, Pc = ids('c_open'), ids('c_acc'), ids('c_accs'), ids('c_prud')
    Rm = [idx('Rnn'), idx('Rpn')]
    C13 = [idx('C3'), idx('C0')]
    assert len(Fcs) == 8 and len(Fct) == 8

    def F(tot):
        spread(Fs, tot * 2 / 3); spread(Ft, tot / 3)

    def Fc(tot):
        spread(Fcs, tot * 2 / 3); spread(Fct, tot / 3)
    if arm == 'F':
        F(delta)
    elif arm == 'FR':
        F(delta); spread(Rm, extra)
    elif arm == 'FOR':
        F(delta / 2); spread(O, delta / 2); spread(Rm, extra)
    elif arm in ('Fc', 'Fcs'):
        Fc(delta)
    elif arm == 'FcOc':
        Fc(delta / 2); spread(Oc, delta / 2)
    elif arm == 'FcOcRc':
        Fc(delta / 2); spread(Oc, delta / 2); spread(Rc, extra)
    elif arm == 'FcRc':
        Fc(delta); spread(Rc, extra)
    elif arm == 'FcOcRcs':
        Fc(delta / 2); spread(Oc, delta / 2); spread(Rcs, extra)
    elif arm == 'mix':
        Fc(delta / 4); spread(Oc, delta / 4); F(delta / 4); spread(O, delta / 4); spread(Rc, extra / 2); spread(Rm, extra / 2)
    elif arm == 'FcOcC3':
        Fc(delta / 2); spread(Oc, delta / 2); spread(C13, extra)
    elif arm == 'PcOcRc':
        spread(Pc, delta / 2); spread(Oc, delta / 2); spread(Rc, extra)
    else:
        raise ValueError(arm)
    return w / w.sum()


SEED_TRIPLES = {'unequal': ('Bn', 'C3', 'C8'), 'unequalBc': ('Bcn', 'C3', 'C8'), 'fair': ('C1', 'C4', 'C8'), 'fairC': ('FcSnzn', 'FcSpzn', 'C8')}


def seed_triples(kind):
    a, b, c = SEED_TRIPLES[kind]
    base = (idx(a), idx(b), idx(c))
    return [base, (base[2], base[0], base[1]), (base[1], base[2], base[0])]     # rotation r puts the base's slot s in slot s + r


def seeded_init(kind, I, N):
    tb = tabs(); K = tb.K
    tr = seed_triples(kind)
    init = np.zeros((I, 3, K), np.int64)
    for i in range(I):
        t = tr[i % 3]
        for s in range(3):
            init[i, s, t[s]] = N
    return init


def parse(spec):
    parts = spec.split(':')
    kv = {}
    for p in parts[1:]:
        if '=' in p:
            k, v = p.split('=', 1); kv[k] = v
    assert parts[0] == 'co', spec
    out = dict(pf=float(kv.get('pf', PFAIL0)), seed=kv.get('seed'), arm=kv['arm'])
    d = float(kv['d']); b = float(kv['b']); ph = float(kv.get('ph', 0.5)); g = float(kv.get('g', 1.0))
    out['wf'] = out['wt'] = law_arm(kv['arm'], d, b, ph, g)
    out.update(delta=d, beta=b, phi=ph, gamma=g)
    return out


def _cyclefix(tb, J, PAY, VEC):
    """Fc*: every all-carrier triple whose three carriers name each other in a cycle (all next or all prev at 1/2) is resolved by slot
    index: slot 0 names slot 1 at 1/2, slot 1 names slot 0 at 1/2, slot 2 keeps its action; charges unchanged (the certified branch
    reads no one)."""
    K = tb.K
    car = np.array([tb.cat.meta[i]['cert'] is not None for i in range(K)])
    a, b, c = np.nonzero(car[:, None, None] & car[None, :, None] & car[None, None, :])
    c0 = tb.code[a, b, c]; c1 = tb.code[b, c, a]; c2 = tb.code[c, a, b]
    cyc = ((c0 == 1) & (c1 == 1) & (c2 == 1)) | ((c0 == 4) & (c1 == 4) & (c2 == 4))
    a, b, c, c2 = a[cyc], b[cyc], c[cyc], c2[cyc]
    newjt = (1 * 81 + 1 * 9 + c2.astype(np.int64))
    # the net payoff: the new gross outcome minus the old charges (charges are the A_f read / forfeit terms, unchanged)
    net_old = PAY[J[a, b, c]]
    gross_old = tb.PAYD[tb.JT[a, b, c]]
    charge = gross_old - net_old
    gross_new = tb.PAYD[newjt]
    vec_new = MT.T.VEC[newjt] if hasattr(MT.T, 'VEC') else tb.VEC[newjt]
    newpay = gross_new - charge
    key = np.concatenate([vec_new[:, None].astype(np.float64), np.round(newpay, 12)], axis=1)
    uk, inv = np.unique(key, axis=0, return_inverse=True)
    base = PAY.shape[0]
    PAY2 = np.concatenate([PAY, uk[:, 1:4]], axis=0)
    VEC2 = np.concatenate([VEC, uk[:, 0].astype(np.int64)])
    J2 = J.copy()
    J2[a, b, c] = (base + inv.ravel()).astype(np.int32)
    return J2, PAY2, VEC2, int(cyc.sum())


def tables(pf, arm=None):
    key = ('tables', round(pf, 9), arm == 'Fcs')
    if key not in _G:
        J, PAY, VEC, ISMEM, TOT = tabs().charged_tables(pf, MT.T)
        if arm == 'Fcs':
            J, PAY, VEC, n = _cyclefix(tabs(), J, PAY, VEC)
            _G['cyclefix_n'] = n
        _G[key] = (J, PAY, VEC, ISMEM, TOT)
    return _G[key]


def prepare(wf, wt, N, r, I, pf=PFAIL0, init=None, cache_dir=None, arm=None):
    tb = tabs(cache_dir)
    init0, seed = MT.founders([wf, wf, wf], 'CP-T-main', r, I, N)
    if init is not None:
        init0 = init
    sched = MT.make_schedule(N, r, I, 100.0)
    tl = [wt, wt, wt]
    K = tb.K
    U = [np.arange(K, dtype=np.int64) for _ in range(3)]
    loc = init0[:, :, :K].astype(np.int64)
    J, PAY, VEC, ISMEM, TOT = tables(pf, arm)
    return dict(arm='CO', variant='co', N=N, r=r, I=I, init=init0, seed=seed, sched=sched, tail_laws=tl, U=U, loc=loc,
                J=J, PAY=PAY, VEC=VEC, ISMEM=ISMEM, TOT=TOT, geo=MT.geometry(N))


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


def charges_by_family(prep, res, pf=PFAIL0):
    tb = tabs()
    N = prep['N']
    ch = pf * (tb.NTO.astype(np.float64) + tb.FO.astype(np.float64))
    fam = fam_table()[0]
    out = {}
    snaps = list(prep['geo']['snaps'])
    nf = len(FAMN)
    for tag, g in (('30N', 30 * N), ('120N', 120 * N)):
        si = snaps.index(g)
        c = res['snapc'][si].astype(np.float64) / N
        num = np.zeros(nf); den = np.zeros(nf)
        for i in range(c.shape[0]):
            q0, q1, q2 = c[i, 0], c[i, 1], c[i, 2]
            e0 = np.einsum('b,c,abc->a', q1, q2, ch[..., 0], optimize=True)
            e1 = np.einsum('a,c,abc->b', q0, q2, ch[..., 1], optimize=True)
            e2 = np.einsum('a,b,abc->c', q0, q1, ch[..., 2], optimize=True)
            for q, e in ((q0, e0), (q1, e1), (q2, e2)):
                np.add.at(num, fam, q * e); np.add.at(den, fam, q)
        tot = den.sum()
        out[tag] = {FAMN[f]: [round(float(num[f] / den[f]), 5) if den[f] > 0 else None, round(float(den[f] / tot), 6)] for f in range(nf)}
        out[tag]['all'] = round(float(num.sum() / tot), 5)
    return out


# ---------------------------------------------------------------- roles and pacing records
RFAM = ('accepter', 'c_acc', 'c_accs')


def roles_of(tb, t):
    """(b, v, e) slots of an unequal majority triple t (b: the 2/3 holder, v: the 1/3 victim, e: excluded), or None."""
    o = int(tb.VEC[tb.JT[t[0], t[1], t[2]]])
    if MW.CATMAP[o] != 1:
        return None
    sh = MW.X[o]
    bs = [s for s in range(3) if sh[s] == 4]; vs = [s for s in range(3) if sh[s] == 2]
    if len(bs) != 1 or len(vs) != 1:
        return None
    return bs[0], vs[0], 3 - bs[0] - vs[0]


def points_at(tb, x, sx, sy):
    """does the program x in slot sx carry a certificate pointing at slot sy?"""
    c = tb.cat.meta[x]['cert']
    if c is None:
        return False
    return (c[0] if (sx + 1) % 3 == sy else c[1]) == 1


def offer_kind(tb, x, se, sv):
    """what kind of offer the program x in the excluded slot se makes to the victim slot sv."""
    if points_at(tb, x, se, sv):
        return 'cert'
    code = int(tb.code[x, 0, 0]) if tb.fam[x] == 'const' else None
    if code is not None and code % 3 == 1 and code // 3 < 2:
        tgt = (se + 1) % 3 if code // 3 == 0 else (se - 1) % 3
        if tgt == sv:
            return 'half'
    return 'none'


def pacing(prep, res):
    """pacing-against-scramble records from the majority-holder log and the arrival list:
    - unequal episodes (debounced modal class) and their first-passage times out of unequal;
    - Rc's (and R's) resident exposure in victim seats of unequal majority triples (island-generations);
    - arrivals into e while an accepter holds v (by offer kind), arrivals of accepters into v of unequal islands (by e's offer kind), each
      with the exact birth-death fixation probability of the arrival in its resident majority triple (step 0's formula) and whether it
      took the slot's majority within 10N generations (observed);
    - predicted completions (the sum of those probabilities for the second steps) against the observed local Rc-route completions."""
    tb = tabs()
    N = prep['N']; I = prep['I']
    NET = tb.payoff(PFAIL0, PFAIL0)
    init = prep['init']
    cur = [[int(np.argmax(init[i, s])) for s in range(3)] for i in range(I)]
    mlog = res['mlog']
    rows = sorted([tuple(int(x) for x in r) for r in mlog], key=lambda r: (r[0], r[1], r[2]))
    ag, ai, asl, au, lk = res['arr']
    order = np.argsort(ag, kind='stable')
    fam = tb.fam
    # majority-takeover index for observed fixation: (island, slot, program) -> sorted gens where it became majority by an arrival presence
    took = {}
    for r in rows:
        if r[5] == 1:
            took.setdefault((r[1], r[2], r[4]), []).append(r[0])
    rec = dict(acc_expo=0, accR_expo=0, e_arr=dict(), v_arr=dict(), pred_second=0.0, pred_first=0.0, n_first=0, n_second=0)

    def bump(d, k, p, fixed):
        e = d.setdefault(k, [0, 0.0, 0])
        e[0] += 1; e[1] += p; e[2] += int(fixed)
    j = 0
    state = [None] * I
    last_t = [0] * I

    def classify_island(i):
        t = cur[i]
        ro = roles_of(tb, t)
        if ro is None:
            return None
        b, v, e = ro
        return (b, v, e, fam[t[v]] in ('c_acc', 'c_accs'), fam[t[v]] == 'accepter')

    def settle(i, g):
        st = state[i]
        if st is not None:
            if st[3]:
                rec['acc_expo'] += g - last_t[i]
            if st[4]:
                rec['accR_expo'] += g - last_t[i]
        last_t[i] = g
    for i in range(I):
        state[i] = classify_island(i)
    H = int(res['modal'].shape[0]) - 1
    ri = 0
    na = len(ag)
    events = sorted(set([r[0] for r in rows] + [int(ag[k]) for k in range(na)]))
    for g in events:
        while ri < len(rows) and rows[ri][0] <= g:
            r = rows[ri]
            settle(r[1], r[0])
            cur[r[1]][r[2]] = r[4]; state[r[1]] = classify_island(r[1]); ri += 1
        while j < na and ag[order[j]] <= g:
            k = order[j]; j += 1
            i = int(ai[k]); s = int(asl[k]); x = int(prep['U'][s][lk[k]])
            st = state[i]
            if st is None:
                continue
            b, v, e, accv, accR = st
            t = list(cur[i])
            if x == t[s]:
                continue
            t2 = list(t); t2[s] = x
            d = float(NET[t2[0], t2[1], t2[2]][s] - NET[t[0], t[1], t[2]][s])
            p = rho_exact(d, N)
            gl = took.get((i, s, x), [])
            fixed = any(int(ag[k]) <= gg <= int(ag[k]) + 10 * N for gg in gl)
            if s == e and (accv or accR):
                kind = offer_kind(tb, x, e, v)
                bump(rec['e_arr'], ('Rc|' if accv else 'R|') + kind + '|' + _fg(tb, x), p, fixed)
                if accv and kind == 'cert':
                    rec['pred_second'] += p; rec['n_second'] += 1
            if s == v and fam[x] in ('c_acc', 'c_accs', 'accepter'):
                kind = offer_kind(tb, t[e], e, v)
                bump(rec['v_arr'], fam[x] + '|' + kind, p, fixed)
                if fam[x] in ('c_acc', 'c_accs'):
                    if kind == 'cert':
                        rec['pred_second'] += p; rec['n_second'] += 1
                    else:
                        rec['pred_first'] += p; rec['n_first'] += 1
    for i in range(I):
        settle(i, H)
    for d in ('e_arr', 'v_arr'):
        rec[d] = {k: dict(n=v[0], pred=round(v[1], 6), fixed=v[2]) for k, v in rec[d].items()}
    rec['pred_second'] = round(rec['pred_second'], 6); rec['pred_first'] = round(rec['pred_first'], 6)
    # first-passage times out of unequal (debounced modal class, L = 0.25 N)
    L = max(1, int(round(0.25 * N)))
    cls = MW.CATMAP[res['modal'].astype(np.int64)].astype(np.int64)
    fl = CP.flips(cls, L)
    durs = []; cens = []
    for i in range(I):
        start = 0 if cls[0, i] == 1 else None
        for (g, a, b) in fl[i]:
            if b == 1:
                start = g
            elif a == 1 and start is not None:
                durs.append(g - start); start = None
        if start is not None:
            cens.append(H - start)
    rec['unequal_exits'] = len(durs); rec['unequal_censored'] = len(cens)
    rec['fpt_median'] = float(np.median(durs)) if durs else None
    rec['fpt_q'] = [float(np.percentile(durs, q)) for q in (10, 50, 90)] if durs else None
    rec['n_transitions'] = int(sum(len(f) for f in fl))
    rec['trans_counts'] = {}
    for i in range(I):
        for (g, a, b) in fl[i]:
            kk = '%s>%s' % ('FUGWD'[a], 'FUGWD'[b])
            rec['trans_counts'][kk] = rec['trans_counts'].get(kk, 0) + 1
    return rec


def _fg(tb, x):
    f = tb.fam[x]
    if f == 'const':
        return tb.names[x]
    return {'single': 'F', 'two': 'F', 'exploit': 'X', 'bully': 'B', 'junk_f': 'J', 'junk_r': 'J', 'prudent': 'P', 'prudent_a': 'Q',
            'opener': 'O', 'single2': 'F2', 'accepter': 'R', 'c_open': 'Oc', 'c_firm': 'Fc', 'c_acc': 'Rc', 'c_accs': 'Rcs', 'c_bully': 'Bc',
            'c_prud': 'Pc'}[f]


def rc_routes_observed(prep, res):
    """local Rc-route completions observed in any cell (roles from the majority triple just before each exit): the debounced
    unequal->fair flips whose new fair pair is (v, e) of the last unequal majority triple with an accepter (Rc / Rcs / R) in v; split by
    e's offer kind (cert / half / other) and origin (local: some pair holder's presence began with a tail arrival here or at founding)."""
    tb = tabs()
    N = prep['N']; I = prep['I']
    L = max(1, int(round(0.25 * N)))
    modal = res['modal'].astype(np.int64)
    G = modal.shape[0]
    cls = MW.CATMAP[modal].astype(np.int64)
    fl = CP.flips(cls, L)
    per = [[] for _ in range(I)]
    for r in res['mlog']:
        per[int(r[1])].append(tuple(int(x) for x in r))
    init = prep['init']
    out = {}
    for i in range(I):
        m0 = [int(np.argmax(init[i, s])) for s in range(3)]
        for (g, a, b) in fl[i]:
            if not (a == 1 and b == 0):
                continue
            gg = min(g + L, G - 1)
            m = list(m0); hist = []; orig = {s: 'fnd' for s in range(3)}
            for r in per[i]:
                if r[0] > gg:
                    break
                hist.append((r[0], list(m)))
                m[r[2]] = r[4]; orig[r[2]] = 'arr' if r[5] == 1 else ('mig' if r[6] >= 0 else 'fnd')
            prev_u = None
            for (gr, mm) in reversed(hist + [(gg, list(m))]):
                if gr <= g and roles_of(tb, mm) is not None:
                    prev_u = mm; break
            if prev_u is None:
                for (gr, mm) in reversed(hist):
                    if roles_of(tb, mm) is not None:
                        prev_u = mm; break
            o = int(tb.VEC[tb.JT[m[0], m[1], m[2]]]); sh = MW.X[o]
            pair = [s for s in range(3) if sh[s] > 0] if MW.CATMAP[o] == 0 else []
            lab = 'other'
            if prev_u is not None and len(pair) == 2:
                bb, vv, ee = roles_of(tb, prev_u)
                if sorted(pair) == sorted([vv, ee]) and tb.fam[m[vv]] in RFAM:
                    kind = offer_kind(tb, m[ee], ee, vv)
                    lab = 'Rroute|%s|%s' % (tb.fam[m[vv]], kind)
            origin = 'imported' if pair and all(orig[s] == 'mig' for s in pair) else 'local'
            lasted = bool((cls[g:min(120 * N, G - 1) + 1, i] == 0).all()) if g <= 120 * N else False
            key = '%s|%s|%s' % (lab, origin, 'lasting' if lasted else 'transient')
            out[key] = out.get(key, 0) + 1
    return out


def classify_exits(prep, res, kind):
    """queue 78's exit classifier v2 (roles from the island's seeded triple; unchanged logic), with the route label refined: for a (v, e)
    pair with an accepter in v, the offer kind of e's holder (cert / half / none)."""
    tb = tabs(); names = tb.names
    N = prep['N']
    L = max(1, int(round(0.25 * N)))
    modal = res['modal'].astype(np.int64)
    G, I = modal.shape
    cls = MW.CATMAP[modal].astype(np.int64)
    fl = CP.flips(cls, L)
    per_isl = [[] for _ in range(I)]
    for row in res['mlog']:
        per_isl[int(row[1])].append(tuple(int(x) for x in row))
    init = prep['init']
    fam = tb.fam
    exits = []
    g120 = 120 * N
    ORIG = lambda row: 'arr' if row[5] == 1 else ('mig' if row[6] >= 0 else 'fnd')
    for i in range(I):
        rot = i % 3
        roles = {(s + rot) % 3: 'bve'[s] for s in range(3)}
        maj0 = [int(np.argmax(init[i, s])) for s in range(3)]
        steps = per_isl[i]
        for (g, a, b) in fl[i]:
            if not (a == 1 and b == 0):
                continue
            gg = min(g + L, G - 1)
            m = list(maj0); took = {s: (0, 'fnd') for s in range(3)}
            for row in steps:
                if row[0] > gg:
                    break
                m[row[2]] = row[4]; took[row[2]] = (row[0], ORIG(row))
            o = int(tb.VEC[tb.JT[m[0], m[1], m[2]]]); sh = MW.X[o]
            pair = [s for s in range(3) if sh[s] > 0] if MW.CATMAP[o] == 0 else []
            route = 'unresolved'; origin = '-'
            if len(pair) == 2:
                pr = ''.join(sorted(roles[s] for s in pair))
                isR = {s: fam[m[s]] in RFAM for s in pair}
                origin = 'imported' if all(took[s][1] == 'mig' for s in pair) else 'local'
                if pr == 'ev' and any(isR[s] and roles[s] == 'v' for s in pair):
                    sv = [s for s in pair if roles[s] == 'v'][0]; se = [s for s in pair if roles[s] == 'e'][0]
                    kd = offer_kind(tb, m[se], se, sv)
                    route = ('R->X' if took[sv][0] <= took[se][0] else 'X->R') + '|' + fam[m[sv]] + '|' + kd
                elif pr == 'be' and fam[m[[s for s in pair if roles[s] == 'b'][0]]] in ('bully', 'c_bully'):
                    route = 'bully+X|' + '+'.join(sorted(fam[m[s]] for s in pair))
                else:
                    route = 'pair %s: %s' % (pr, '+'.join(sorted(fam[m[s]] for s in pair)))
            sl = [row for row in steps if row[0] <= gg][-16:]
            seq = [(row[0], row[2], roles[row[2]], names[row[3]], names[row[4]], ORIG(row)) for row in sl]
            lasted = bool((cls[g:g120 + 1, i] == 0).all()) if g <= g120 else False
            exits.append(dict(island=i, g=int(g), route=route, origin=origin, pair_roles={roles[s]: names[m[s]] for s in pair},
                              triple=[names[x] for x in m], seq=seq, lasted_to_120N=lasted))
    return dict(version=2, exits=exits, n_exits=len(exits), mlog_rows=int(res['nm']), mlog_cap=MCAP,
                fair30=float(np.mean(cls[30 * N] == 0)), fair120=float(np.mean(cls[min(g120, G - 1)] == 0)), fair_end=float(np.mean(cls[G - 1] == 0)),
                hazard=hazard_u(cls, fl, N))


def hazard_u(cls, fl, N):
    G, I = cls.shape
    out = {}
    for tag, hi in (('to120N', 120 * N), ('toend', G - 1)):
        occ = float((cls[:hi + 1] == 1).sum())
        n = sum(1 for ch in fl for (g, a, b) in ch if g <= hi and a == 1 and b == 0)
        out[tag] = dict(n_UF=int(n), occ_U=occ, rate=(n / occ if occ else None))
    return out


def scramble(prep, res):
    """the scramble diagnostic: share of islands whose 120N modal class equals the 30N one; composition of unequal islands at 30N
    (the 2/3 holder's and the victim's family by the majority triple)."""
    tb = tabs()
    N = prep['N']
    modal = res['modal'].astype(np.int64)
    c30 = MW.CATMAP[modal[30 * N]]; c120 = MW.CATMAP[modal[120 * N]]
    out = dict(same_class=float(np.mean(c30 == c120)), same_outcome=float(np.mean(modal[30 * N] == modal[120 * N])))
    snaps = list(prep['geo']['snaps'])
    si = snaps.index(30 * N)
    c = res['snapc'][si]
    comp = {}
    for i in range(c.shape[0]):
        t = [int(np.argmax(c[i, s])) for s in range(3)]
        ro = roles_of(tb, t)
        if ro is None:
            continue
        k = '%s|%s' % (_fg(tb, t[ro[0]]), _fg(tb, t[ro[1]]))
        comp[k] = comp.get(k, 0) + 1
    out['unequal30_holder_victim'] = comp
    return out


def run_cell(spec, N, r, I, long=False, cache_dir=None, charges=True, pace=False):
    pr = parse(spec)
    tabs(cache_dir)
    init = seeded_init(pr['seed'], I, N) if pr['seed'] else None
    prep = prepare(pr['wf'], pr['wt'], N, r, I, pf=pr['pf'], init=init, cache_dir=cache_dir, arm=pr['arm'])
    geo = prep['geo']
    H = geo['Hlong'] if long else geo['H']
    snaps = list(geo['snaps']) + ([240 * N] if long else [])
    t0 = time.time()
    res = run_kernel_log(prep, 100, 1.0, H, snaps, MCAP)
    rec = MT.summarize(prep, res, 100, 1.0, fam_table(), long=long)
    rec['wall'] = round(time.time() - t0, 1)
    rec['fam_names'] = FAMN
    for sn in rec['snap'].values():
        sn.pop('fair_enc_isl', None)
    if charges:
        rec['charges'] = charges_by_family(prep, res, pr['pf'])
    rec['scramble'] = scramble(prep, res)
    rec['rroutes'] = rc_routes_observed(prep, res)
    if pace or pr['seed']:
        rec['pacing'] = pacing(prep, res)
    if pr['seed']:
        rec['exits'] = classify_exits(prep, res, pr['seed'])
    rec['mlog_overflow'] = int(res['nm']) > MCAP
    return rec


KEEP = ('vshare_ts', 'cons_modal', 'cons_majo', 'cons_modal_240', 'trans', 'tail', 'nmig', 'status', 'stop', 'wall', 'charges', 'scramble',
        'rroutes', 'pacing', 'exits', 'mlog_overflow')


def run_job(job, cache_dir):
    series, spec, N, I, r, long = job.split('|')
    N, I, r, long = int(N), int(I), int(r), bool(int(long))
    pace = series in ('main', 'pace') and 'arm=FcOcRc:' in spec
    rec = run_cell(spec, N, r, I, long=long, cache_dir=cache_dir, pace=pace)
    out = dict(id=job, series=series, spec=spec, N=N, I=I, r=r, long=long)
    for k in KEEP:
        if k in rec:
            out[k] = rec[k]
    sn = rec['snap'][str(120 * N)]
    out['snap120'] = dict(cls_modal=sn['cls_modal'], pair_modal=sn['pair_modal'], npairs_modal=sn['npairs_modal'],
                          cls_majo=sn['cls_majo'], hold=sn['hold'], fair_enc=sn['fair_enc'], surplus=sn['surplus'])
    sn30 = rec['snap'][str(30 * N)]
    out['snap30'] = dict(cls_modal=sn30['cls_modal'], cls_majo=sn30['cls_majo'], hold=sn30['hold'])
    if long:
        sn240 = rec['snap'][str(240 * N)]
        out['snap240'] = dict(cls_modal=sn240['cls_modal'], cls_majo=sn240['cls_majo'])
    out['vstar'] = rec['vshare_ts'][120]
    return out
