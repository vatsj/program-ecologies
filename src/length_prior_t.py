"""Step 2 of queue 75 (spec specs/2026-11-08-length-prior-t.md): arm T of the majority-division simulation
(src/majority_tail.py, queue 74) over the extended library T+ = the 27 programs + Trojan bullies (+ two junk programs
for series 2b) under a two-parameter (and, for 2b, a measured) seed law.  Nothing existing is edited.

Laws (family totals over the 31 programs of tplus.py, every slot, founding and tail alike):
  2a:d=<delta>:b=<beta>[:s1]     constants 1 - d - b*d - 0.01*d/0.09 (uniform over the 9), singles + twos at d (2 : 1 unless
                                 s1: singles only), exploiters 0.01*d/0.09, bullies b*d (half Bn, half Bp)
  2b:<file>:<machine>:d=<delta>:  see law_2b: junk at its measured mass, readers at d with the measured single / two
                                 ratio, bullies at the measured ratio times d, exploiters at the measured ratio times d,
                                 constants in their measured conditional proportions
Founder and tail doses can differ (series 2a slice (ii) and the matched cells): the spec string carries `f=` / `t=`
multipliers on the reader family (founders / tail) mass, see parse_law.
"""
import os, sys, json, gzip, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import majority_tail as MT
import tplus as TP

NAMES = None
FAMP = ['c_third', 'c_half', 'c_two3', 'c_grand', 'single', 'two', 'exploit', 'bully', 'junk']   # 0..8; 0-6 as majority_tail.FAMS_T
BASE = 'CP-T-main'
_G = {}


def tabs(cache_dir=None):
    if 'tabs' not in _G:
        _G['tabs'] = TP.TabsPlus(cache_dir=cache_dir)
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
            f[p] = {'single': 4, 'two': 5, 'exploit': 6, 'bully': 7, 'junk_f': 8, 'junk_r': 8}[fm]
    return np.tile(f, (3, 1))


def _ids(fam):
    tb = tabs()
    return [i for i in range(tb.K) if tb.fam[i] == fam]


def law_main_exact():
    """exactly the stored T-main law (churn_primary_t.TCat.law('main') on 31 programs, then / sum); V1."""
    import churn_primary_t as CT
    tb = tabs()
    w = np.zeros(tb.K)
    for fam, tot in CT.FAMILY_WEIGHT['main'].items():
        ids = _ids(fam)
        for i in ids:
            w[i] = tot / len(ids)
    return w / w.sum()


def law_2a(delta, beta, singles_only=False):
    """series 2a: constants keep T's proportions (uniform over the nine), readers 2 : 1 single : two, exploiters keep their
    ratio to readers, bullies at beta * delta (half Bn, half Bp)."""
    tb = tabs()
    ex = 0.01 * delta / 0.09
    cst = 1.0 - delta - beta * delta - ex
    assert cst > 0, (delta, beta)
    w = np.zeros(tb.K)
    for i in _ids('const'):
        w[i] = cst / 9
    s_tot = delta if singles_only else delta * 2.0 / 3.0
    for i in _ids('single'):
        w[i] = s_tot / 8
    if not singles_only:
        for i in _ids('two'):
            w[i] = delta / 3.0 / 8
    for i in _ids('exploit'):
        w[i] = ex / 2
    for i in _ids('bully'):
        w[i] = beta * delta / 2
    return w / w.sum()


def law_family(const_w, single, two, exploit, bully, junk_f=0.0, junk_r=0.0):
    """law from explicit family totals; const_w: 9 weights (sum 1 - the rest); singles uniform over the 8, twos over the 8,
    exploiters over the 2, bullies over the 2."""
    tb = tabs()
    w = np.zeros(tb.K)
    cids = _ids('const')
    cw = np.asarray(const_w, float)
    for k, i in enumerate(cids):
        w[i] = cw[k]
    for i in _ids('single'):
        w[i] = single / 8
    for i in _ids('two'):
        w[i] = two / 8
    for i in _ids('exploit'):
        w[i] = exploit / 2
    for i in _ids('bully'):
        w[i] = bully / 2
    w[tb.names.index('Jf')] = junk_f
    w[tb.names.index('Jr')] = junk_r
    return w / w.sum()


def parse_law(spec, step1=None):
    """spec -> (founding law, tail law) as vectors.  Grammar (':'-separated): 2a:d=..:b=..[:s1][:fm=..][:tm=..] where fm / tm
    multiply the reader and bully mass of the founders / the tail (the removed mass goes to the constants)
    ; main  (the stored law); 2b:<machine>:d=..[:fm=..][:tm=..] with step1 = the measured law data (see law_2b)."""
    parts = spec.split(':')
    kv = {}
    for p in parts[1:]:
        if '=' in p:
            k, v = p.split('=', 1); kv[k] = float(v)
    s1 = 's1' in parts
    if parts[0] == 'main':
        w = law_main_exact()
        return w, w
    if parts[0] == '2a':
        d = kv['d']; b = kv.get('b', 0.0)
        wf = law_2a(d * kv.get('fm', 1.0), b, s1) if True else None
        wt = law_2a(d * kv.get('tm', 1.0), b, s1)
        return wf, wt
    if parts[0] == '2b':
        mach = parts[1]
        d = kv['d']
        return law_2b(step1, mach, d * kv.get('fm', 1.0)), law_2b(step1, mach, d * kv.get('tm', 1.0))
    raise ValueError(spec)


def law_2b(step1, mach, delta):
    """series 2b: the length prior's shape projected onto T+.  step1[mach] holds (measured, conditional on finite terms):
    const (9 masses c0..c8), single, two, exploit, bully, junk_f, junk_r (family masses); delta is the reader share
    (single + two); within-reader ratio single : two, exploit / reader and bully / reader ratios as measured; constants
    take the remainder in their measured conditional proportions."""
    m = step1[mach]
    sg, tw = m['single'], m['two']
    rd = sg + tw
    assert rd > 0
    single = delta * sg / rd; two = delta * tw / rd
    exploit = delta * m['exploit'] / rd; bully = delta * m['bully'] / rd
    jf, jr = m['junk_f'], m['junk_r']
    cm = np.asarray(m['const'], float)
    rest = 1.0 - single - two - exploit - bully - jf - jr
    assert rest > 0, (delta, rest)
    cw = rest * cm / cm.sum()
    return law_family(cw, single, two, exploit, bully, jf, jr)


# ====================================================================== preparation and one cell
def prepare_plus(wf, wt, N, r, I, Lmax=100.0, cache_dir=None):
    tb = tabs(cache_dir)
    init, seed = MT.founders([wf, wf, wf], BASE, r, I, N)
    sched = MT.make_schedule(N, r, I, Lmax)
    tl = [wt, wt, wt]
    st = MT.map_programs(sched, tl, Lmax)
    K = tb.K
    U = [np.arange(K, dtype=np.int64) for _ in range(3)]
    loc = init[:, :, :K].astype(np.int64)
    if 'tables' not in _G:
        _G['tables'] = tb.charged_tables(MT.PFAIL, MT.T)
    J, PAY, VEC, ISMEM, TOT = _G['tables']
    return dict(arm='T+', variant='lp', N=N, r=r, I=I, init=init, seed=seed, sched=sched, tail_laws=tl, U=U, loc=loc,
                J=J, PAY=PAY, VEC=VEC, ISMEM=ISMEM, TOT=TOT, geo=MT.geometry(N))


def run_cell(wf, wt, N, r, I, long=False, lam=100, mN=1.0, cache_dir=None, slim=True):
    prep = prepare_plus(wf, wt, N, r, I, cache_dir=cache_dir)
    geo = prep['geo']
    H = geo['Hlong'] if long else geo['H']
    snaps = list(geo['snaps']) + ([240 * N] if long else [])
    t0 = time.time()
    res = MT.run_kernel(prep, lam, mN, H, snaps)
    rec = MT.summarize(prep, res, lam, mN, fam_table(), long=long)
    rec['wall'] = round(time.time() - t0, 1)
    rec['fam_names'] = FAMP
    if slim:
        for sn in rec['snap'].values():
            sn.pop('fair_enc_isl', None)
    return rec


def vstar_final(rec, N):
    ts = rec['vshare_ts']
    return ts[120] if len(ts) > 120 else ts[-1]
