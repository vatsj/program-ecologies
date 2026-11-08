"""Step 3 of queue 76 (spec specs/2026-11-08-bully-resistance.md): arm T over the 55-program catalogue of bully_resist.py
(T+ , prudent readers P / Q, openers O, the matched firm control F2) in queue 74's simulator (src/majority_tail.py), mN = 1,
Lambda = 100 from the founding law, 100N + 20N chase, CRN.  Nothing existing is edited.

Laws (family totals over the 55 programs, founders and tail alike).  Constants are uniform over the nine, bullies are beta * delta
(half Bn, half Bp), exploiters are 0.01 * delta / 0.09 (as in queue 75's law 2a), and the reader share delta is split by arm:
  F    singles 2/3, twos 1/3 (queue 75's law 2a exactly; V1)         P    the four P_z (strict probe, fallback z)
  Po   the four P_o                                                     Q    the four lenient-probe readers
  O    the eight openers                                                F2   the four matched controls
  PO   half P_z, half O                                                 FPO  thirds: F (2:1), P_z, O                                           FO   half F (2:1), half O (the RS's addendum)
A spec string is  br:arm=<A>:d=<delta>:b=<beta>[:pf=<P_fail>][:seed=fair|unequal][:fm=..:tm=..]  or
lp:<machine>:<alloc>:d=<delta>  (length-prior-shaped, see law_lp).  `pf=0` suppresses the A_f charges (diagnostic replay: the same
actions and schedule, charges zero).  `tab=ideal` uses the idealized uncapped table of bully_resist_ideal.py (no timeouts, no charges; diagnostic).  `seed=` starts every island on a named triple (see seeded_init) instead of the founding law.
"""
import os, sys, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import majority_tail as MT
import migration_window as MW
import bully_resist as BR
import length_prior_t as LP

PFAIL0 = MT.PFAIL
_G = {}
FAMN = BR.FAMB


def tabs(cache_dir=None):
    if 'tabs' not in _G:
        _G['tabs'] = BR.TabsBR(cache_dir=cache_dir or os.path.join(ROOT, 'runs', '_cache'))
    return _G['tabs']


def fam_table():
    """(3, K) family index (into BR.FAMB) of every program, per slot."""
    tb = tabs()
    f = np.zeros(tb.K, np.int64)
    for p in range(tb.K):
        fm = tb.fam[p]
        if fm == 'const':
            a = int(tb.names[p][1:])
            f[p] = 3 if a // 3 == 2 else a % 3
        else:
            f[p] = {'single': 4, 'two': 5, 'exploit': 6, 'bully': 7, 'junk_f': 8, 'junk_r': 8, 'prudent': 9, 'prudent_a': 10,
                    'opener': 11, 'single2': 12}[fm]
    return np.tile(f, (3, 1))


def ids(fam, tag=None):
    tb = tabs()
    return [i for i in range(tb.K) if tb.fam[i] == fam and (tag is None or tag(tb.names[i]))]


PZ = lambda n: n[2] == 'z'
PO_ = lambda n: n[2] == 'o'


def law_arm(arm, delta, beta):
    tb = tabs()
    K = tb.K
    ex = 0.01 * delta / 0.09
    cst = 1.0 - delta - beta * delta - ex
    assert cst > 0, (arm, delta, beta)
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
    F_single, F_two = ids('single'), ids('two')
    Pz, Po, Q = ids('prudent', PZ), ids('prudent', PO_), ids('prudent_a')
    O, F2 = ids('opener'), ids('single2')
    if arm == 'F':
        spread(F_single, delta * 2 / 3); spread(F_two, delta / 3)
    elif arm == 'P':
        spread(Pz, delta)
    elif arm == 'Po':
        spread(Po, delta)
    elif arm == 'Q':
        spread(Q, delta)
    elif arm == 'O':
        spread(O, delta)
    elif arm == 'F2':
        spread(F2, delta)
    elif arm == 'PO':
        spread(Pz, delta / 2); spread(O, delta / 2)
    elif arm == 'FO':
        spread(F_single, delta / 2 * 2 / 3); spread(F_two, delta / 2 / 3); spread(O, delta / 2)
    elif arm == 'FPO':
        spread(F_single, delta / 3 * 2 / 3); spread(F_two, delta / 3 / 3); spread(Pz, delta / 3); spread(O, delta / 3)
    else:
        raise ValueError(arm)
    return w / w.sum()


def seeded_init(arm, kind, I, N, rng):
    """init counts (I, 3, K) with every island monomorphic on a triple drawn uniformly from
    kind 'fair': fair-pair triples whose pair holds at least one reader of the arm and whose other members are readers of the arm or
    constants (the third slot a constant); kind 'unequal': a bully on 2/3, a 1/3-naming constant (C0 or C3) and a constant."""
    tb = tabs(); K = tb.K
    import itertools
    CAT = MW.CATMAP
    OUT = tb.VEC[tb.JT]
    cst = ids('const'); bul = ids('bully')
    if kind == 'fair':
        arm_readers = {'F': ids('single') + ids('two'), 'P': ids('prudent', PZ), 'Po': ids('prudent', PO_), 'Q': ids('prudent_a'),
                       'O': ids('opener'), 'F2': ids('single2'), 'PO': ids('prudent', PZ) + ids('opener'),
                       'FPO': ids('single') + ids('two') + ids('prudent', PZ) + ids('opener'),
                       'FO': ids('single') + ids('two') + ids('opener')}[arm]
        pool = []
        for t in itertools.product(arm_readers + cst, repeat=3):
            if CAT[OUT[t]] != 0:
                continue
            sh = MW.X[int(OUT[t])]
            if any(sh[s] > 0 and t[s] in arm_readers for s in range(3)) and sum(1 for x in t if x in arm_readers) <= 2 \
                    and all((sh[s] > 0) or (t[s] in cst) for s in range(3)):
                pool.append(t)
    else:
        third = [tb.names.index('C0'), tb.names.index('C3')]
        pool = []
        for t in itertools.product(bul + cst, repeat=3):
            if sum(1 for x in t if x in bul) == 1 and CAT[OUT[t]] == 1:
                sh = MW.X[int(OUT[t])]
                sb = [s for s in range(3) if t[s] in bul][0]
                if sh[sb] == 4 and any(x in third for x in t):
                    pool.append(t)
    assert pool, (arm, kind)
    init = np.zeros((I, 3, K), np.int64)
    pick = rng.integers(0, len(pool), I)
    for i in range(I):
        for s in range(3):
            init[i, s, pool[pick[i]][s]] = N
    return init, len(pool)


def parse(spec, step2=None):
    """spec -> dict(wf, wt, pf, seed, arm)."""
    parts = spec.split(':')
    kv = {}
    for p in parts[1:]:
        if '=' in p:
            k, v = p.split('=', 1); kv[k] = v
    out = dict(pf=float(kv.get('pf', PFAIL0)), seed=kv.get('seed'), arm=kv.get('arm'), tab=kv.get('tab', 'cap'))
    if parts[0] == 'br':
        d = float(kv['d']); b = float(kv['b'])
        fm = float(kv.get('fm', 1.0)); tm = float(kv.get('tm', 1.0))
        out['wf'] = law_arm(kv['arm'], d * fm, b); out['wt'] = law_arm(kv['arm'], d * tm, b)
    elif parts[0] == 'lp':
        out['wf'] = out['wt'] = law_lp(step2, parts[1], parts[2], float(kv['d']))
        out['arm'] = 'lp'
    else:
        raise ValueError(spec)
    return out


def law_lp(step2, mach, alloc, delta):
    """the length-prior-shaped law (series 2c): step2[mach] holds the measured conditional masses -- constants (9 codes), junk_f,
    junk_r, the exact-member lower bounds of the reader groups (single, two, exploit, bully, prudent_z, prudent_o, prudent_a,
    opener).  The reader share delta = single + two + P_z + P_o + O split in the measured ratio, bullies at (bully mass) / (reader
    mass) times delta, exploiters likewise; junk at its measured mass; `alloc` decides the unmeasured remainder:
    'junk' keeps constants at their measured mass and gives the rest to junk_f, 'const' keeps junk and gives the rest to the
    constants in their measured proportions."""
    m = step2[mach]
    rd = m['single'] + m['two'] + m['prudent_z'] + m['prudent_o'] + m['opener']
    assert rd > 0
    sh = lambda k: delta * m[k] / rd
    bully = delta * m['bully'] / rd; exploit = delta * m['exploit'] / rd
    cm = np.asarray(m['const'], float)
    readers_tot = sh('single') + sh('two') + sh('prudent_z') + sh('prudent_o') + sh('opener') + bully + exploit
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
    for i in ids('prudent', PZ):
        w[i] = sh('prudent_z') / 4
    for i in ids('prudent', PO_):
        w[i] = sh('prudent_o') / 4
    for i in ids('opener'):
        w[i] = sh('opener') / 8
    w[tb.names.index('Jf')] = jf; w[tb.names.index('Jr')] = jr
    return w / w.sum()


def tables(pf, tab='cap'):
    key = ('tables', round(pf, 9), tab)
    if key not in _G:
        if tab == 'ideal':
            import bully_resist_ideal as BI
            if 'ideal' not in _G:
                _G['ideal'] = BI.ideal_tabs()[0]
            _G[key] = _G['ideal'].charged_tables(0.0, MT.T)
        else:
            _G[key] = tabs().charged_tables(pf, MT.T)
    return _G[key]


def prepare(wf, wt, N, r, I, pf=PFAIL0, init=None, cache_dir=None, tab='cap'):
    tb = tabs(cache_dir)
    init0, seed = MT.founders([wf, wf, wf], 'CP-T-main', r, I, N)
    if init is not None:
        init0 = init
    sched = MT.make_schedule(N, r, I, 100.0)
    tl = [wt, wt, wt]
    st = MT.map_programs(sched, tl, 100.0)
    K = tb.K
    U = [np.arange(K, dtype=np.int64) for _ in range(3)]
    loc = init0[:, :, :K].astype(np.int64)
    J, PAY, VEC, ISMEM, TOT = tables(pf, tab)
    return dict(arm='BR', variant='br', N=N, r=r, I=I, init=init0, seed=seed, sched=sched, tail_laws=tl, U=U, loc=loc,
                J=J, PAY=PAY, VEC=VEC, ISMEM=ISMEM, TOT=TOT, geo=MT.geometry(N))


def charges_by_family(prep, res, pf=PFAIL0):
    """mean A_f charge per capita and per encounter (the expected charge of a program drawn at random from the island's slot,
    its partners drawn from the island's two other slots) by family, at the 30N and 120N snapshots; shares of capita."""
    tb = tabs()
    N = prep['N']; K = tb.K
    ch = pf * (tb.NTO.astype(np.float64) + tb.FO.astype(np.float64))        # (K, K, K, 3)
    fam = fam_table()[0]
    out = {}
    snaps = list(prep['geo']['snaps'])
    for tag, g in (('30N', 30 * N), ('120N', 120 * N)):
        si = snaps.index(g)
        c = res['snapc'][si].astype(np.float64) / N                          # (I, 3, K)
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


def run_cell(spec, N, r, I, long=False, step2=None, cache_dir=None, charges=True):
    pr = parse(spec, step2)
    tabs(cache_dir)
    init = None
    if pr['seed']:
        rng = np.random.default_rng(76000 + 31 * r + N)
        init, npool = seeded_init(pr['arm'], pr['seed'], I, N, rng)
    prep = prepare(pr['wf'], pr['wt'], N, r, I, pf=pr['pf'], init=init, cache_dir=cache_dir, tab=pr['tab'])
    geo = prep['geo']
    H = geo['Hlong'] if long else geo['H']
    snaps = list(geo['snaps']) + ([240 * N] if long else [])
    t0 = time.time()
    res = MT.run_kernel(prep, 100, 1.0, H, snaps)
    rec = MT.summarize(prep, res, 100, 1.0, fam_table(), long=long)
    rec['wall'] = round(time.time() - t0, 1)
    rec['fam_names'] = FAMN
    for sn in rec['snap'].values():
        sn.pop('fair_enc_isl', None)
    if charges and pr['tab'] == 'cap':
        rec['charges'] = charges_by_family(prep, res, pr['pf'])
    return rec


KEEP = ('vshare_ts', 'cons_modal', 'cons_majo', 'cons_modal_240', 'trans', 'tail', 'nmig', 'status', 'stop', 'wall', 'charges')


def run_job(job, step2, cache_dir):
    series, spec, N, I, r, long = job.split('|')
    N, I, r, long = int(N), int(I), int(r), bool(int(long))
    rec = run_cell(spec, N, r, I, long=long, step2=step2, cache_dir=cache_dir)
    out = dict(id=job, series=series, spec=spec, N=N, I=I, r=r, long=long)
    for k in KEEP:
        if k in rec:
            out[k] = rec[k]
    sn = rec['snap'][str(120 * N)]
    out['snap120'] = dict(cls_modal=sn['cls_modal'], pair_modal=sn['pair_modal'], npairs_modal=sn['npairs_modal'],
                          cls_majo=sn['cls_majo'], hold=sn['hold'], fair_enc=sn['fair_enc'], surplus=sn['surplus'])
    sn30 = rec['snap'][str(30 * N)]
    out['snap30'] = dict(cls_modal=sn30['cls_modal'], cls_majo=sn30['cls_majo'])
    out['vstar'] = rec['vshare_ts'][120]
    return out
