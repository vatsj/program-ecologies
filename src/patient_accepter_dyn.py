"""Step 2 of queue 78 (spec specs/2026-11-14-patient-accepters.md): arm T over the 59-program catalogue of patient_accepter.py in
queue 74's simulator (majority_tail), mN = 1, Lambda = 100 from the founding law, 100N + 20N chase, CRN, exactly as queue 76's
bully_resist_dyn (nothing existing is edited).

Laws (family totals over the 59 programs, founders and tail alike).  As queue 76: the nine constants uniform, bullies beta * delta (half
Bn, half Bp), exploiters 0.01 * delta / 0.09, readers delta split by arm; and R at gamma * delta, taken from the constants:

  F     singles 2/3, twos 1/3 of delta (queue 75's law 2a; V1)
  FR    F at delta, R at gamma * delta (half Rnn, half Rpn: the main `n` variants)
  FOR   delta/2 F (2:1), delta/2 openers (eight, uniform), R at gamma * delta
  FC    F at delta, extra 1/3 constants at gamma * delta (half C3, half C0: the constants Rnn and Rpn play on path)
  R     delta = R (half Rnn, half Rpn), no firm readers
  FRs   delta/2 F (2:1), delta/2 R
The donor: in FR, FOR and FC the gamma * delta comes out of the nine constants uniformly (constants total 1 - delta - beta delta - ex -
gamma delta, spread over nine), so FR and FC differ only in the substituted family (same donor mass, same constants, same slots).

Spec strings:  pa:arm=<A>:d=<delta>:b=<beta>[:g=<gamma>][:seed=unequal|fair]   and   lp:<machine>:<alloc>:d=<delta> (length-prior-shaped).
`seed=` starts every island on the spec's exact triple: unequal (Bn, C3, C8), fair (C1, C4, C8), and its two rotations on a third of the
islands each (island i gets rotation i mod 3); founders are identical across arms, which differ only in the tail law.  Seeded cells log
the majority holder of every slot (patient_accepter_kern.kern_pa) and classify every exit from an unequal island.
"""
import os, sys, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import majority_tail as MT
import migration_window as MW
import patient_accepter as PA
import churn_primary as CP

PFAIL0 = MT.PFAIL
_G = {}
FAMN = PA.FAMP
MCAP = 600000


def tabs(cache_dir=None):
    if 'tabs' not in _G:
        _G['tabs'] = PA.TabsPA(cache_dir=cache_dir or os.path.join(ROOT, 'runs', '_cache'))
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
            f[p] = {'single': 4, 'two': 5, 'exploit': 6, 'bully': 7, 'junk_f': 8, 'junk_r': 8, 'prudent': 9, 'prudent_a': 10,
                    'opener': 11, 'single2': 12, 'accepter': 13}[fm]
    return np.tile(f, (3, 1))


def ids(fam, tag=None):
    tb = tabs()
    return [i for i in range(tb.K) if tb.fam[i] == fam and (tag is None or tag(tb.names[i]))]


def idx(name):
    return tabs().names.index(name)


ARMS = ('F', 'FR', 'FOR', 'FC', 'R', 'FRs')


def law_arm(arm, delta, beta, gamma=1.0):
    tb = tabs()
    K = tb.K
    ex = 0.01 * delta / 0.09
    extra = gamma * delta if arm in ('FR', 'FOR', 'FC') else 0.0
    cst = 1.0 - delta - beta * delta - ex - extra
    assert cst > 0, (arm, delta, beta, gamma)
    w = np.zeros(K)
    for i in ids('const'):
        w[i] = cst / 9
    for i in ids('exploit'):
        w[i] = ex / 2
    for i in ids('bully'):
        w[i] = beta * delta / 2

    def spread(members, tot):
        for i in members:
            w[i] += tot / len(members)
    Fs, Ft, O = ids('single'), ids('two'), ids('opener')
    Rm = [idx('Rnn'), idx('Rpn')]
    C13 = [idx('C3'), idx('C0')]
    if arm == 'F':
        spread(Fs, delta * 2 / 3); spread(Ft, delta / 3)
    elif arm == 'FR':
        spread(Fs, delta * 2 / 3); spread(Ft, delta / 3); spread(Rm, extra)
    elif arm == 'FOR':
        spread(Fs, delta / 2 * 2 / 3); spread(Ft, delta / 2 / 3); spread(O, delta / 2); spread(Rm, extra)
    elif arm == 'FC':
        spread(Fs, delta * 2 / 3); spread(Ft, delta / 3); spread(C13, extra)
    elif arm == 'R':
        spread(Rm, delta)
    elif arm == 'FRs':
        spread(Fs, delta / 2 * 2 / 3); spread(Ft, delta / 2 / 3); spread(Rm, delta / 2)
    else:
        raise ValueError(arm)
    return w / w.sum()


def law_lp(step1, mach, alloc, delta):
    """the length-prior-shaped law: step1[mach] holds the measured conditional masses (as queue 76's step2.json: constants by code,
    junk_f, junk_r, exact-member lower bounds of single, two, exploit, bully, prudent_z, prudent_o, opener) plus `accepter` (the exact-member
    lower bound of the `n` variants of R).  The reader share delta = single + two + P_z + P_o + O + R split in the measured ratio, bullies and
    exploiters at their measured ratio to the reader mass, junk at its measured mass; `alloc` decides the unmeasured remainder ('junk': the
    constants keep their measured mass, the rest is junk_f; 'const': junk keeps its mass, the rest goes to the constants in their
    measured proportions).  Queue 76's series with R added to the reader share at its measured mass."""
    m = step1[mach]
    keys = ('single', 'two', 'prudent_z', 'prudent_o', 'opener', 'accepter')
    rd = sum(m[k] for k in keys)
    assert rd > 0
    sh = lambda k: delta * m[k] / rd
    bully = delta * m['bully'] / rd; exploit = delta * m['exploit'] / rd
    cm = np.asarray(m['const'], float)
    readers_tot = sum(sh(k) for k in keys) + bully + exploit
    jf, jr = m['junk_f'], m['junk_r']
    if alloc == 'const':
        rest = 1.0 - readers_tot - jf - jr
        assert rest > 0, (mach, alloc, delta)
        cw = rest * cm / cm.sum()
    elif alloc == 'junk':
        cw = cm.copy()
        jf = 1.0 - readers_tot - cw.sum() - jr
        assert jf > 0, (mach, alloc, delta)
    else:
        raise ValueError(alloc)
    tb = tabs(); K = tb.K
    w = np.zeros(K)
    for k, i in enumerate(ids('const')):
        w[i] = cw[k]
    for i in ids('single'):
        w[i] = sh('single') / 8
    for i in ids('two'):
        w[i] = sh('two') / 8
    for i in ids('exploit'):
        w[i] = exploit / 2
    for i in ids('bully'):
        w[i] = bully / 2
    for i in ids('prudent', lambda n: n[2] == 'z'):
        w[i] = sh('prudent_z') / 4
    for i in ids('prudent', lambda n: n[2] == 'o'):
        w[i] = sh('prudent_o') / 4
    for i in ids('opener'):
        w[i] = sh('opener') / 8
    for nm in ('Rnn', 'Rpn'):
        w[idx(nm)] = sh('accepter') / 2
    w[idx('Jf')] = jf; w[idx('Jr')] = jr
    return w / w.sum()


SEED_TRIPLES = {'unequal': ('Bn', 'C3', 'C8'), 'fair': ('C1', 'C4', 'C8')}


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


def parse(spec, step1=None):
    parts = spec.split(':')
    kv = {}
    for p in parts[1:]:
        if '=' in p:
            k, v = p.split('=', 1); kv[k] = v
    out = dict(pf=float(kv.get('pf', PFAIL0)), seed=kv.get('seed'), arm=kv.get('arm'))
    if parts[0] == 'pa':
        d = float(kv['d']); b = float(kv['b']); g = float(kv.get('g', 1.0))
        out['wf'] = out['wt'] = law_arm(kv['arm'], d, b, g)
        out['gamma'] = g
    elif parts[0] == 'lp':
        out['wf'] = out['wt'] = law_lp(step1, parts[1], parts[2], float(kv['d']))
        out['arm'] = 'lp'
    else:
        raise ValueError(spec)
    return out


def tables(pf):
    key = ('tables', round(pf, 9))
    if key not in _G:
        _G[key] = tabs().charged_tables(pf, MT.T)
    return _G[key]


def prepare(wf, wt, N, r, I, pf=PFAIL0, init=None, cache_dir=None):
    tb = tabs(cache_dir)
    init0, seed = MT.founders([wf, wf, wf], 'CP-T-main', r, I, N)
    if init is not None:
        init0 = init
    sched = MT.make_schedule(N, r, I, 100.0)
    tl = [wt, wt, wt]
    K = tb.K
    U = [np.arange(K, dtype=np.int64) for _ in range(3)]
    loc = init0[:, :, :K].astype(np.int64)
    J, PAY, VEC, ISMEM, TOT = tables(pf)
    return dict(arm='PA', variant='pa', N=N, r=r, I=I, init=init0, seed=seed, sched=sched, tail_laws=tl, U=U, loc=loc,
                J=J, PAY=PAY, VEC=VEC, ISMEM=ISMEM, TOT=TOT, geo=MT.geometry(N))


def run_kernel_pa(prep, lam, mN, H, snapg, mcap):
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
    for tag, g in (('30N', 30 * N), ('120N', 120 * N)):
        si = snaps.index(g)
        c = res['snapc'][si].astype(np.float64) / N
        num = np.zeros(len(FAMN)); den = np.zeros(len(FAMN))
        for i in range(c.shape[0]):
            q0, q1, q2 = c[i, 0], c[i, 1], c[i, 2]
            e0 = np.einsum('b,c,abc->a', q1, q2, ch[..., 0], optimize=True)
            e1 = np.einsum('a,c,abc->b', q0, q2, ch[..., 1], optimize=True)
            e2 = np.einsum('a,b,abc->c', q0, q1, ch[..., 2], optimize=True)
            for q, e in ((q0, e0), (q1, e1), (q2, e2)):
                np.add.at(num, fam, q * e); np.add.at(den, fam, q)
        tot = den.sum()
        out[tag] = {FAMN[f]: [round(float(num[f] / den[f]), 5) if den[f] > 0 else None, round(float(den[f] / tot), 6)] for f in range(len(FAMN))}
        out[tag]['all'] = round(float(num.sum() / tot), 5)
    return out


def r_measures(prep, res):
    """At 120N: (a) the share of unequal islands (majority triple) whose victim's majority program is an R; (b) R's mean per-capita net payoff
    minus the 1/3 constants' (C0, C3) in the same slot, on island-slots where both are present (expected payoffs against the island's other
    two slots); (c) the same with 30N."""
    tb = tabs()
    N = prep['N']
    snaps = list(prep['geo']['snaps'])
    NET = tb.payoff(PFAIL0, PFAIL0)
    OUT = tb.VEC[tb.JT]
    Rids = set(ids('accepter')); C13 = {idx('C0'), idx('C3')}
    out = {}
    for tag, g in (('30N', 30 * N), ('120N', 120 * N)):
        si = snaps.index(g)
        c = res['snapc'][si].astype(np.float64)
        nU = 0; nUR = 0; diffs = []; wts = []
        for i in range(c.shape[0]):
            maj = [int(np.argmax(c[i, s])) for s in range(3)]
            o = int(OUT[maj[0], maj[1], maj[2]])
            if MW.CATMAP[o] == 1:
                sh = MW.X[o]
                nU += 1
                v = [s for s in range(3) if sh[s] == 2]
                if v and maj[v[0]] in Rids:
                    nUR += 1
            q = c[i] / N
            for s in range(3):
                pr = [k for k in Rids if c[i, s, k] > 0]; pc = [k for k in C13 if c[i, s, k] > 0]
                if not pr or not pc:
                    continue
                o1, o2 = [x for x in range(3) if x != s]

                def pay(k):
                    t = [slice(None)] * 3
                    sub = np.take(NET[..., s], k, axis=s)            # (K, K) over the other two slots in order
                    return float(q[o1] @ sub @ q[o2])
                aR = sum(c[i, s, k] * pay(k) for k in pr) / sum(c[i, s, k] for k in pr)
                aC = sum(c[i, s, k] * pay(k) for k in pc) / sum(c[i, s, k] for k in pc)
                diffs.append(aR - aC); wts.append(1.0)
        out[tag] = dict(unequal=nU, unequal_R_victim=nUR, share_R_victim=(nUR / nU if nU else None),
                        n_slots_both=len(diffs), mean_R_minus_C13=(float(np.mean(diffs)) if diffs else None))
    return out


def classify_exits(prep, res, kind):
    """Exit classification on a seeded-start run (version 2: slot roles are the island's SEEDED roles).  The island's seeded triple fixes
    the roles of its slots: b (the seeded bully's slot), v (the seeded victim's slot), e (the seeded excluded slot) (for the fair start
    the roles of the seeded unequal triple at the same rotation are used, as labels only).  Debounced (0.25 N) class series of the modal
    outcome; for every unequal->fair flip the majority triple one debounce window later gives the new fair pair, and the majority-holder
    log gives, for each pair slot, the generation at which its final holder last took it and that presence's origin (tail arrival on this
    island, migrant, founder).
      pair route:   'R+X (v, e)'  R holds v and X holds e: 'R->X' if R took v first, 'X->R' otherwise
                    'bully+X'     the pair is (b, e) with the seeded bully's program class (a bully) in b
                    other labels  '<roles of the pair slots>' with the holder families
      origin:       'local' if some pair holder's presence began with a tail arrival on this island or at founding, 'imported' if every
                    pair holder's presence began with a migrant (the pair came from elsewhere)
    Records the last 16 majority-holder changes (generation, slot, role, old, new, origin) and whether the fair episode lasted to 120N."""
    tb = tabs(); names = tb.names
    N = prep['N']
    L = max(1, int(round(0.25 * N)))
    modal = res['modal'].astype(np.int64)
    G, I = modal.shape
    cls = MW.CATMAP[modal].astype(np.int64)
    fl = CP.flips(cls, L)
    mlog = res['mlog']
    per_isl = [[] for _ in range(I)]
    for row in mlog:
        per_isl[int(row[1])].append(tuple(int(x) for x in row))
    init = prep['init']
    fam = tb.fam
    base = SEED_TRIPLES['unequal']            # roles b, v, e in base slots 0, 1, 2; rotation r puts base slot s in slot s + r
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
                isR = {s: fam[m[s]] == 'accepter' for s in pair}
                origin = 'imported' if all(took[s][1] == 'mig' for s in pair) else 'local'
                if pr == 'ev' and any(isR[s] and roles[s] == 'v' for s in pair):
                    sv = [s for s in pair if roles[s] == 'v'][0]; se = [s for s in pair if roles[s] == 'e'][0]
                    route = 'R->X' if took[sv][0] <= took[se][0] else 'X->R'
                elif pr == 'be' and fam[m[[s for s in pair if roles[s] == 'b'][0]]] == 'bully':
                    route = 'bully+X'
                else:
                    route = 'pair %s: %s' % (pr, '+'.join(sorted(fam[m[s]] for s in pair)))
            sl = [row for row in steps if row[0] <= gg][-16:]
            seq = [(row[0], row[2], roles[row[2]], names[row[3]], names[row[4]], ORIG(row)) for row in sl]
            lasted = bool((cls[g:g120 + 1, i] == 0).all()) if g <= g120 else False
            exits.append(dict(island=i, g=int(g), route=route, origin=origin, pair_roles={roles[s]: names[m[s]] for s in pair},
                              pair_fams=sorted(fam[m[s]] for s in pair), took={roles[s]: list(took[s]) for s in pair},
                              triple=[names[x] for x in m], seq=seq, lasted_to_120N=lasted))
    return dict(version=2, exits=exits, n_exits=len(exits), mlog_rows=int(res['nm']), mlog_cap=MCAP,
                fair30=float(np.mean(cls[30 * N] == 0)), fair120=float(np.mean(cls[min(g120, G - 1)] == 0)), fair_end=float(np.mean(cls[G - 1] == 0)),
                hazard=hazard_u(cls, fl, N))


def hazard_u(cls, fl, N):
    """unequal-to-fair debounced transitions per unequal island-generation in [0, 120N] and [0, end]."""
    G, I = cls.shape
    out = {}
    for tag, hi in (('to120N', 120 * N), ('toend', G - 1)):
        occ = float((cls[:hi + 1] == 1).sum())
        n = sum(1 for ch in fl for (g, a, b) in ch if g <= hi and a == 1 and b == 0)
        out[tag] = dict(n_UF=int(n), occ_U=occ, rate=(n / occ if occ else None))
    return out


def run_cell(spec, N, r, I, long=False, step1=None, cache_dir=None, charges=True):
    pr = parse(spec, step1)
    tabs(cache_dir)
    init = seeded_init(pr['seed'], I, N) if pr['seed'] else None
    prep = prepare(pr['wf'], pr['wt'], N, r, I, pf=pr['pf'], init=init, cache_dir=cache_dir)
    geo = prep['geo']
    H = geo['Hlong'] if long else geo['H']
    snaps = list(geo['snaps']) + ([240 * N] if long else [])
    t0 = time.time()
    if pr['seed']:
        res = run_kernel_pa(prep, 100, 1.0, H, snaps, MCAP)
    else:
        res = MT.run_kernel(prep, 100, 1.0, H, snaps)
    rec = MT.summarize(prep, res, 100, 1.0, fam_table(), long=long)
    rec['wall'] = round(time.time() - t0, 1)
    rec['fam_names'] = FAMN
    for sn in rec['snap'].values():
        sn.pop('fair_enc_isl', None)
    if charges:
        rec['charges'] = charges_by_family(prep, res, pr['pf'])
    rec['rmeas'] = r_measures(prep, res)
    if pr['seed']:
        rec['exits'] = classify_exits(prep, res, pr['seed'])
    return rec


KEEP = ('vshare_ts', 'cons_modal', 'cons_majo', 'cons_modal_240', 'trans', 'tail', 'nmig', 'status', 'stop', 'wall', 'charges', 'rmeas', 'exits')


def run_job(job, step1, cache_dir):
    series, spec, N, I, r, long = job.split('|')
    N, I, r, long = int(N), int(I), int(r), bool(int(long))
    rec = run_cell(spec, N, r, I, long=long, step1=step1, cache_dir=cache_dir)
    out = dict(id=job, series=series, spec=spec, N=N, I=I, r=r, long=long)
    for k in KEEP:
        if k in rec:
            out[k] = rec[k]
    sn = rec['snap'][str(120 * N)]
    out['snap120'] = dict(cls_modal=sn['cls_modal'], pair_modal=sn['pair_modal'], npairs_modal=sn['npairs_modal'],
                          cls_majo=sn['cls_majo'], hold=sn['hold'], fair_enc=sn['fair_enc'], surplus=sn['surplus'])
    sn30 = rec['snap'][str(30 * N)]
    out['snap30'] = dict(cls_modal=sn30['cls_modal'], cls_majo=sn30['cls_majo'])
    if long:
        sn240 = rec['snap'][str(240 * N)]
        out['snap240'] = dict(cls_modal=sn240['cls_modal'], cls_majo=sn240['cls_majo'])
    out['vstar'] = rec['vshare_ts'][120]
    return out
