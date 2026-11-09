"""Step 0 of queue 76 (spec specs/2026-11-08-bully-resistance.md): why bullies beat firm readers (diagnosis), and the new
families in the same assays.  Scoring rules: predictions/2026-11-08-bully-resistance.md.

  python3 src/bully_resist_step0.py assays OUT.json          items 1, 2, 4, 5 (outcome table, exact invasion assays, net payoffs)
  python3 src/bully_resist_step0.py hold OUT.json R0 R1      item 3: rerun of queue 75's beta = 1, 3 cells at N = 200, I = 64 with
                                                             per-island snapshots (holding configurations); checks V* against the stored rows

Exactness.  With the other two slots monomorphic the invader's payoff in the invaded slot is frequency independent, so the
single-island Moran chain (child proportional to count * exp(w * f), victim uniform, w = 0.3) is a birth-death chain whose
embedded jump chain steps up with probability r / (1 + r), r = exp(w * (pi_invader - pi_resident)); the fixation probability from one
copy is rho = (1 - 1/r) / (1 - 1/r^N), 1/N when r = 1.  A Monte Carlo of the jump chain (10^4 trials) is the empirical check; the full
kernel (majority_tail_kern.kern_mt, mN = 0) is the check of the pipeline on non-neutral assays (it stops a run on play identity, so a
neutral invader is only resolved by the walk).
"""
import os, sys, json, itertools, time, gzip, glob
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import bully_resist as BR
import majority_tail as MT
import migration_window as MW
from numba import njit

PFAIL = 0.1
N0 = 200
WSEL = MT.W
CAT = ['F', 'U', 'G', 'W', 'D']


def rho_exact(d, N=N0, w=WSEL):
    """fixation probability of one invader copy; d = net payoff of the invader minus the resident's, in the invaded slot."""
    x = w * d
    if abs(x) < 1e-12:
        return 1.0 / N
    if x > 0:
        return float(-np.expm1(-x) / -np.expm1(-N * x))
    return _rho_neg(x, N)


def _rho_neg(x, N):
    # x < 0: r < 1.  rho = (1 - 1/r)/(1 - 1/r^N) = (r^(N-1) (r - 1)) / (r^N - 1) with r = e^x
    num = np.exp((N - 1) * x) * np.expm1(x)
    den = np.expm1(N * x)
    return float(num / den)


@njit(cache=True)
def _walk(p, N, trials, seed, cap):
    np.random.seed(seed)
    fix = 0; ext = 0; per = 0
    for t in range(trials):
        i = 1; s = 0
        while i > 0 and i < N and s < cap:
            if np.random.random() < p:
                i += 1
            else:
                i -= 1
            s += 1
        if i == N:
            fix += 1
        elif i == 0:
            ext += 1
        else:
            per += 1
    return fix, ext, per


def mc_fixation(d, N=N0, w=WSEL, trials=10000, seed=1):
    r = np.exp(w * d)
    fix, ext, per = _walk(r / (1.0 + r), N, trials, seed, 10 ** 7)
    return fix / trials, int(per)


class Ctx:
    def __init__(self, cache_dir=None):
        self.tb = BR.TabsBR(cache_dir=cache_dir or os.path.join(ROOT, 'runs', '_cache'))
        tb = self.tb
        self.names = tb.names; self.idx = {n: i for i, n in enumerate(tb.names)}
        self.NET = tb.payoff(PFAIL, PFAIL)           # (K, K, K, 3)
        self.GROSS = tb.GROSS
        self.OUT = tb.VEC[tb.JT]                      # outcome id of (a, b, c)
        self.CLS = MW.CATMAP[self.OUT]
        fam = tb.fam
        self.FR = [i for i in range(tb.K) if fam[i] in ('single', 'two')]
        self.CST = [i for i in range(tb.K) if fam[i] == 'const']
        self.BUL = [i for i in range(tb.K) if fam[i] == 'bully']
        self.PZ = [i for i in range(tb.K) if fam[i] == 'prudent' and self.names[i][2] == 'z']
        self.PO = [i for i in range(tb.K) if fam[i] == 'prudent' and self.names[i][2] == 'o']
        self.QL = [i for i in range(tb.K) if fam[i] == 'prudent_a']
        self.OP = [i for i in range(tb.K) if fam[i] == 'opener']
        self.third = [self.idx['C0'], self.idx['C3']]          # 1/3-naming constants (a single partner at 1/3)
        self.third_all = self.third + [self.idx['C6']]

    def share(self, t):
        return MW.X[int(self.OUT[t])]

    def pay_in(self, res, s, x, net=True):
        t = list(res); t[s] = x
        a = (self.NET if net else self.GROSS)[t[0], t[1], t[2]]
        return float(a[s])

    def dpi(self, res, s, x):
        return self.pay_in(res, s, x) - self.pay_in(res, s, res[s]), self.pay_in(res, s, x, False) - self.pay_in(res, s, res[s], False)


def role(ctx, res, s):
    """role of slot s in the resident: 'pair' if it has a positive share, else 'out'."""
    sh = ctx.share(tuple(res))
    return 'pair' if sh[s] > 0 else 'out'


# ---------------------------------------------------------------------------------------------------- resident classes
def resident_sets(ctx, fam_ids):
    """named resident triples of the classes of the spec (fam_ids: the reader family F that replaces `firm readers`)."""
    out = {}
    C = ctx.CLS; OUT = ctx.OUT
    FI = [t for t in itertools.product(fam_ids, fam_ids, fam_ids) if C[t] == 0]
    FC = []
    for t in itertools.product(fam_ids + ctx.CST, repeat=3):
        nf = sum(1 for x in t if x in fam_ids); nc = 3 - nf
        if nf == 2 and nc == 1 and C[t] == 0:
            sh = ctx.share(t)
            if all(sh[s] > 0 for s in range(3) if t[s] in fam_ids):      # the two readers form the pair
                FC.append(t)
    UB = []
    for t in itertools.product(ctx.BUL + ctx.CST, repeat=3):
        nb = sum(1 for x in t if x in ctx.BUL)
        if nb == 1 and C[t] == 1:
            sh = ctx.share(t); sb = [s for s in range(3) if t[s] in ctx.BUL][0]
            if sh[sb] == 4 and any(x in ctx.third_all for x in t):
                UB.append(t)
    BF = []
    for t in itertools.product(ctx.BUL + fam_ids + ctx.CST, repeat=3):
        nb = sum(1 for x in t if x in ctx.BUL); nr = sum(1 for x in t if x in fam_ids)
        if nb == 1 and nr >= 1 and C[t] == 0:
            sh = ctx.share(t); sb = [s for s in range(3) if t[s] in ctx.BUL][0]
            if sh[sb] > 0 and any(sh[s] > 0 and t[s] in fam_ids for s in range(3)):
                if all(x in ctx.BUL + fam_ids + ctx.CST for x in t) and sum(1 for x in t if x in ctx.CST) <= 1:
                    BF.append(t)
    return dict(FI=FI, FC=FC, UB=UB, BF=BF)


def assays_for(ctx, residents, invaders, kind):
    rows = []
    for res in residents:
        for s in range(3):
            for x in invaders:
                if x == res[s]:
                    continue
                dn, dg = ctx.dpi(res, s, x)
                rows.append(dict(kind=kind, res=tuple(int(v) for v in res), s=s, x=int(x), role=role(ctx, res, s),
                                 dnet=dn, dgross=dg, rhoN=rho_exact(dn) * N0))
    return rows


def summarize(rows):
    a = np.array([r['rhoN'] for r in rows])
    if len(a) == 0:
        return dict(n=0)
    return dict(n=int(len(a)), median=float(np.median(a)), mean=float(a.mean()), p10=float(np.percentile(a, 10)),
                p90=float(np.percentile(a, 90)), max=float(a.max()), min=float(a.min()),
                share_le_half=float((a < 0.5).mean()), share_neutral=float(((a >= 0.5) & (a <= 3)).mean()),
                share_le_1=float((a <= 1).mean()), share_gt3=float((a > 3).mean()),
                share_exact_neutral=float((np.abs(a - 1.0) < 1e-9).mean()))


def by(rows, key):
    out = {}
    for r in rows:
        out.setdefault(key(r), []).append(r)
    return {k: summarize(v) for k, v in out.items()}


def run_assays(out):
    t0 = time.time()
    ctx = Ctx(); nm = ctx.names
    res = {}
    # ---- item 1: outcome table over (bully, firm reader, constant), all slot orders
    tab = []
    cnt = {}
    for b in ctx.BUL:
        for r in ctx.FR:
            for c in ctx.CST:
                for perm in itertools.permutations([b, r, c]):
                    o = int(ctx.OUT[perm]); cl = CAT[int(MW.CATMAP[o])]
                    sh = MW.X[o]
                    key = (nm[b], ctx.tb.fam[r], cl)
                    cnt[key] = cnt.get(key, 0) + 1
                    sb = perm.index(b); sr = perm.index(r); sc = perm.index(c)
                    tab.append(dict(b=nm[b], r=nm[r], c=nm[c], slots=[nm[perm[0]], nm[perm[1]], nm[perm[2]]], cls=cl, shares=list(sh),
                                    bully_share=sh[sb], reader_share=sh[sr], const_share=sh[sc]))
    res['item1_counts'] = {'%s|%s|%s' % k: v for k, v in sorted(cnt.items())}
    unequal_bully = [t for t in tab if t['cls'] == 'U' and t['bully_share'] == 4]
    fair_pair_bully_reader = [t for t in tab if t['cls'] == 'F' and t['bully_share'] > 0 and t['reader_share'] > 0]
    res['item1_unequal_bully_on_2_3'] = dict(n=len(unequal_bully), by_constant_partner={}, examples=unequal_bully[:10])
    cc = {}
    for t in unequal_bully:
        part = t['c'] if t['const_share'] == 2 else ('(reader)' if t['reader_share'] == 2 else '?')
        cc[part] = cc.get(part, 0) + 1
    res['item1_unequal_bully_on_2_3']['by_victim'] = cc
    res['item1_fair_pair_bully_and_reader'] = dict(n=len(fair_pair_bully_reader), by_reader_family={}, examples=fair_pair_bully_reader[:10])
    ff = {}
    for t in fair_pair_bully_reader:
        k = ctx.tb.fam[ctx.idx[t['r']]]
        ff[k] = ff.get(k, 0) + 1
    res['item1_fair_pair_bully_and_reader']['by_reader_family'] = ff
    res['item1_all'] = tab
    # ---- items 2, 4, 5: exact invasion assays
    fams = {'firm': ctx.FR, 'firm_single': [i for i in ctx.FR if ctx.tb.fam[i] == 'single'], 'firm_two': [i for i in ctx.FR if ctx.tb.fam[i] == 'two'],
            'Pz': ctx.PZ, 'Po': ctx.PO, 'Q': ctx.QL, 'O': ctx.OP}
    asy = {}
    summ = {}
    for fn, ids in fams.items():
        rs = resident_sets(ctx, ids)
        a = {}
        a['FI'] = assays_for(ctx, rs['FI'], ctx.BUL, 'FI')                       # bully into fair reader islands
        a['FC'] = assays_for(ctx, rs['FC'], ctx.BUL, 'FC')
        a['UB'] = assays_for(ctx, rs['UB'], ids, 'UB')                           # reader family into bully-held unequal islands
        a['BF'] = assays_for(ctx, rs['BF'], ctx.third_all, 'BF')                 # 1/3 constants into bully-held fair islands
        asy[fn] = a
        summ[fn] = {}
        for k, rows in a.items():
            summ[fn][k] = dict(n_resident=len(rs[k]), all=summarize(rows),
                               by_role=by(rows, lambda r: r['role']),
                               by_slot=by(rows, lambda r: r['s']),
                               by_invader_family=by(rows, lambda r: ('bully' if ctx.tb.fam[r['x']] == 'bully' else ('third_const' if ctx.tb.fam[r['x']] == 'const' else fn))),
                               by_third_const=by(rows, lambda r: nm[r['x']]) if k == 'BF' else None)
        # step 0.4 extra: UB with the 1/3 constant C0/C3 split
    res['item2_summary'] = summ
    # unequal-island: split by the constant type naming the bully at 1/3 (C0 / C3 / C6) for UB and for the firm family
    sp = {}
    for fn in ('firm', 'Pz', 'Po', 'Q', 'O'):
        rows = asy[fn]['UB']
        sp[fn] = by(rows, lambda r: ','.join(nm[x] for x in r['res']) and ('third=' + '+'.join(sorted(nm[x] for x in r['res'] if x in ctx.third_all))))
    res['item2_UB_by_third_constant'] = sp
    # a list of (class, family) -> every assay is stored compactly for the report (res named triples, slot, invader, rho*N)
    res['assays'] = {fn: {k: [(','.join(nm[x] for x in r['res']), r['s'], nm[r['x']], round(r['dnet'], 6), round(r['dgross'], 6), round(r['rhoN'], 6), r['role']) for r in rows]
                         for k, rows in a.items()} for fn, a in asy.items()}
    # ---- Monte Carlo check (10^4 trials) of the exact value, and the neutral twin baseline
    rng = np.random.default_rng(76)
    mc = []
    for fn in ('firm', 'Pz', 'O'):
        for k in ('FI', 'UB', 'BF'):
            rows = asy[fn][k]
            if not rows:
                continue
            for j in rng.choice(len(rows), size=min(60, len(rows)), replace=False):
                r = rows[int(j)]
                f, per = mc_fixation(r['dnet'], trials=10000, seed=int(1000 + j))
                mc.append(dict(fam=fn, cls=k, exact=rho_exact(r['dnet']), mc=f, persisting=per,
                               z=float((f - rho_exact(r['dnet'])) / max(np.sqrt(rho_exact(r['dnet']) * (1 - rho_exact(r['dnet'])) / 10000), 1e-9))))
    twin = [mc_fixation(0.0, trials=10000, seed=7000 + i)[0] for i in range(20)]
    res['mc_check'] = dict(n=len(mc), max_abs_z=float(max(abs(m['z']) for m in mc)), mean_z=float(np.mean([m['z'] for m in mc])),
                           share_abs_z_gt3=float(np.mean([abs(m['z']) > 3 for m in mc])), persisting_total=int(sum(m['persisting'] for m in mc)))
    res['neutral_twin'] = dict(trials=10000, fixation_mean=float(np.mean(twin)), fixation_se=float(np.std(twin) / np.sqrt(len(twin))), one_over_N=1.0 / N0)
    # ---- kernel check on non-neutral assays
    res['kernel_check'] = kernel_check(ctx, asy)
    res['wall'] = round(time.time() - t0, 1)
    json.dump(res, open(out, 'w'))
    print('wall', res['wall'])
    return res


def kernel_check(ctx, asy, n_assay=24, islands=3000, N=N0):
    """invade with the real kernel (mN = 0, no arrivals) and compare with the exact rho; only assays that are not play-identical."""
    import majority_tail_kern as MK
    J, PAY, VEC, ISMEM, TOT = ctx.tb.charged_tables(PFAIL, MT.T)
    rng = np.random.default_rng(5)
    pool = []
    for fn in ('firm', 'Pz', 'O'):
        for k in ('FI', 'UB', 'BF'):
            for r in asy[fn][k]:
                if 0.05 < r['rhoN'] < 12 and abs(r['rhoN'] - 1) > 1e-9:
                    pool.append((fn, k, r))
    out = []
    z0 = np.zeros(0, np.int64)
    for j in rng.choice(len(pool), size=min(n_assay, len(pool)), replace=False):
        fn, k, r = pool[int(j)]
        K = ctx.tb.K
        init = np.zeros((islands, 3, K), np.int64)
        for s in range(3):
            init[:, s, r['res'][s]] = N
        init[:, r['s'], r['res'][r['s']]] = N - 1
        init[:, r['s'], r['x']] = 1
        res = MK.kern_mt(J, PAY, VEC, ISMEM, TOT, init, N, WSEL, 0.0, int(900 + j), 400 * N, 10, np.zeros(0, np.int64), z0, z0, z0,
                         np.zeros(0), z0, 4000, 4000)
        counts = res[2]
        fixed = int((counts[:, r['s'], r['x']] == N).sum())
        persist = int(((counts[:, r['s'], r['x']] > 0) & (counts[:, r['s'], r['x']] < N)).sum())
        p = rho_exact(r['dnet'], N)
        out.append(dict(fam=fn, cls=k, res=[ctx.names[x] for x in r['res']], s=r['s'], x=ctx.names[r['x']], exact=p, kernel=fixed / islands,
                        persisting=persist, status=int(res[0]), z=float((fixed / islands - p) / max(np.sqrt(p * (1 - p) / islands), 1e-9))))
    return dict(n=len(out), max_abs_z=float(max(abs(o['z']) for o in out)), rows=out)


# ---------------------------------------------------------------------------------------------------- item 3: holding configurations
def run_hold(out, betas=(1.0, 3.0), deltas=(1e-3, 1e-2, 1e-1), N=200, I=64, runs=20, workers=3, only=None):
    import length_prior_t as LP
    import length_prior_t_run as LR
    import multiprocessing as mp
    rows = {}
    for d in glob.glob(os.path.join(ROOT, 'runs', 'lpt_rows', '*')):
        rows.update(LR.load_rows(d))
    jobs = []
    for b in betas:
        for dl in deltas:
            for r in range(runs):
                spec = '2a:d=%s:b=%s' % (LR.fmt(dl), LR.fmt(b))
                jobs.append(('2a|%s|%d|%d|%d|0' % (spec, N, I, r), spec, r, rows.get('2a|%s|%d|%d|%d|0' % (spec, N, I, r))))
    with mp.Pool(workers) as p:
        res = p.map(_hold_job, [(j[1], N, I, j[2], j[3]) for j in jobs], chunksize=1)
    json.dump(dict(cells=res), open(out, 'w'))
    return res


def _hold_job(arg):
    spec, N, I, r, stored = arg
    import length_prior_t as LP
    wf, wt = LP.parse_law(spec)
    cache = os.path.join(ROOT, 'runs', '_cache')
    LP.tabs(cache)
    prep = LP.prepare_plus(wf, wt, N, r, I, cache_dir=cache)
    geo = prep['geo']
    res = MT.run_kernel(prep, 100, 1.0, geo['H'], list(geo['snaps']))
    modal = res['modal'].astype(np.int64)
    cl = MW.CATMAP[modal]
    snaps = list(geo['snaps'])
    tb = LP.tabs()
    names = tb.names
    isn30 = snaps.index(30 * N); isn120 = snaps.index(120 * N)
    c30 = res['snapc'][isn30]; c120 = res['snapc'][isn120]          # (I, 3, K)
    vstar = float(MW.CATMAP[modal[120 * N]].__eq__(0).mean())
    out = dict(spec=spec, r=r, vstar=vstar, stored_vstar=(stored['vstar'] if stored else None), islands=[])
    for i in range(I):
        c_30 = int(cl[30 * N, i]); c_120 = int(cl[120 * N, i])
        dom30 = [names[int(np.argmax(c30[i, s]))] for s in range(3)]
        dom120 = [names[int(np.argmax(c120[i, s]))] for s in range(3)]
        out['islands'].append((c_30, c_120, dom30, dom120))
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'assays':
        run_assays(sys.argv[2])
    elif sys.argv[1] == 'hold':
        run_hold(sys.argv[2])
