"""Driver for the core stage-2 run (spec specs/2026-10-21-core-stage2.md).

    python3 src/core_stage2_run.py statics                    # exhaustive statics, order check, skew map and split distribution
    python3 src/core_stage2_run.py list                       # the cell registry
    python3 src/core_stage2_run.py cells --cells NAME ... [--runs 40] [--workers 1] [--chunk 5]
    python3 src/core_stage2_run.py ordercheck --cells NAME ...   # first three runs of each cell under the reverse-order tensor
Outputs go to runs/core_stage2/: statics*.json/csv.gz, cell_<name>.json (summary and series), rows_<name>.csv.gz (per-island end states).
"""
import argparse, gzip, json, os, sys, time, csv, zlib
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core_auction as C
import core_stage2 as S

OUT = S.OUT
os.makedirs(OUT, exist_ok=True)
INSTS = ('threshold', 'asymmetric', 'skew')
SPACES = ('no-overbid', 'unrestricted')


def log(*a):
    print(*a, flush=True)


# ================================================================== statics
def split_class(inst, bA, bB):
    """class of the winners' split (A's payment bA, B's bB) against the references for the instance (two item winners): the Vickrey-nearest payments,
    the equal-surplus payments and the equal-payment payments on the revenue-14 reference edge (skew: A pays 10, 11, 7).  Exact matches on A's payment
    (and the reference total) are 'vn', 'es', 'ep'; else 'other'."""
    v = C.INSTANCES[inst]
    refs = reference_splits(inst)
    for name, (ra, rb) in refs.items():
        if bA == ra and bB == rb:
            return name
    return 'other'


def reference_splits(inst):
    """reference payment pairs (A, B) on the minimum-revenue edge: Vickrey-nearest, equal surplus (equal payoffs u_A = u_B), equal payment."""
    v = C.INSTANCES[inst]
    vP, vA, vB = v
    mr = C.min_revenue(v)
    vn = C.vickrey_nearest(v)
    refs = {'vn': (vn['A'], vn['B'])}
    # equal surplus: vA - pA = vB - pB with pA + pB = mr
    pa = (mr + vA - vB) / 2.0
    refs['es'] = (pa, mr - pa)
    refs['ep'] = (mr / 2.0, mr / 2.0)
    return refs


def static_grid(inst, space):
    """every (t, delta_A, delta_B) facing TX(t): resolved bids, the seller's lottery outcome, and the matched constant c = t's payoff."""
    v = C.INSTANCES[inst]
    caps = C.allowed(inst, space)
    U, X, B = S.build_tensor2(inst, 0)
    mr = C.min_revenue(v)
    rows = []
    for t in range(1, caps[0] + 1):
        kP = S.TX0 + t - 1
        for dA in range(1, 10):
            for dB in range(1, 10):
                kA = S.F0 + dA - 1; kB = S.F0 + dB - 1
                bP, bA, bB = (int(x) for x in B[:, kP, kA, kB])
                uPc = U[0, t, kA, kB]                            # the matched constant c = t against the same pair
                rows.append(dict(t=t, dA=dA, dB=dB, bP=bP, bA=bA, bB=bB, T=bA + bB, txwin=float(X[C.XPRUWIN, kP, kA, kB]),
                                 eff=float(X[C.XEFF, kP, kA, kB]), rev=float(X[C.XREV, kP, kA, kB]), core=float(X[C.XCORE, kP, kA, kB]),
                                 uP=float(U[0, kP, kA, kB]), uA=float(U[1, kP, kA, kB]), uB=float(U[2, kP, kA, kB]), uP_const=float(uPc),
                                 minrev=mr))
    return rows


def order_check_all():
    """every program triple of every instance resolved in both orders by independent evaluators: the pure-python source evaluator (both orders) and the
    numba resolver (both orders).  Returns mismatch counts."""
    res = {}
    for inst in INSTS:
        v = C.INSTANCES[inst]
        U0, X0, B0 = S.build_tensor2(inst, 0)
        U1, X1, B1 = S.build_tensor2(inst, 1)
        nb = 0; npy = 0; ntot = 0; maxdepth = 0
        for kP in range(S.K):
            for kA in range(S.F0 + S.NF):
                for kB in range(S.F0 + S.NF):
                    a, d1 = S.py_resolve(kP, kA, kB, v, 'items_first')
                    b, d2 = S.py_resolve(kP, kA, kB, v, 'p_first')
                    maxdepth = max(maxdepth, d1, d2)
                    ntot += 1
                    if a != b:
                        npy += 1
                    if a != tuple(int(x) for x in B0[:, kP, kA, kB]) or a != tuple(int(x) for x in B1[:, kP, kA, kB]):
                        nb += 1
        res[inst] = dict(triples=ntot, python_order_mismatch=npy, numba_vs_python_mismatch=nb, tensor_U_equal=bool((U0 == U1).all()),
                         tensor_X_equal=bool((X0 == X1).all()), tensor_B_equal=bool((B0 == B1).all()), max_call_depth=maxdepth)
    return res


def statics():
    res = dict(hand={}, grid={}, prediction1={}, skew={}, order=order_check_all())
    for inst in INSTS:
        v = C.INSTANCES[inst]
        mr = C.min_revenue(v)
        res['hand'][inst] = dict(v=v, min_revenue=mr, wstar=C.wstar(v), refs=reference_splits(inst))
        for space in SPACES:
            rows = static_grid(inst, space)
            caps = C.allowed(inst, space)
            with gzip.open(os.path.join(OUT, 'static_%s_%s.csv.gz' % (inst, space)), 'wt') as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
            # prediction 1: complementary pairs facing TX(v_P)
            vP = v[0]
            comp = [r for r in rows if r['t'] == vP and r['dA'] + r['dB'] == 10]
            comp_rows = [dict(dA=r['dA'], dB=r['dB'], bA=r['bA'], bB=r['bB'], T=r['T'], bP=r['bP'], eff=r['eff'], txwin=r['txwin'], rev=r['rev'],
                              offset=r['rev'] - mr) for r in comp]
            efficient = [c for c in comp_rows if c['eff'] > 1 - 1e-9]
            res['prediction1']['%s/%s' % (inst, space)] = dict(
                t=vP, min_revenue=mr, complementary=comp_rows, n_efficient=len(efficient),
                max_offset_efficient=max((c['offset'] for c in efficient), default=None),
                n_efficient_more_than_2_off=sum(c['offset'] > 2 + 1e-9 for c in efficient),
                n_tie=sum(1e-9 < c['txwin'] < 1 - 1e-9 for c in comp_rows), n_txwin=sum(c['txwin'] > 1 - 1e-9 for c in comp_rows))
            # all t: efficient complementary offsets
            allc = [r for r in rows if r['dA'] + r['dB'] == 10 and r['eff'] > 1 - 1e-9]
            offs = {}
            for r in allc:
                o = int(round(r['rev'] - mr)); offs[o] = offs.get(o, 0) + 1
            nonc = [r for r in rows if r['dA'] + r['dB'] != 10 and r['eff'] > 1 - 1e-9]
            offn = {}
            for r in nonc:
                o = int(round(r['rev'] - mr)); offn[o] = offn.get(o, 0) + 1
            # TX(t) payoff against the matched constant, over all pairs
            gain = [r['uP'] - r['uP_const'] for r in rows]
            # shadow condition: pairs where the items' total exceeds the threat (TX never wins)
            shadow = [r for r in rows if r['T'] > r['t']]
            res['grid']['%s/%s' % (inst, space)] = dict(
                n=len(rows), ts=caps[0], efficient_complementary_offsets_all_t=dict(sorted(offs.items())),
                efficient_noncomplementary_offsets_all_t=dict(sorted(offn.items())),
                share_items_win_all_t=float(np.mean([r['eff'] > 1 - 1e-9 for r in rows])),
                share_txwin_all_t=float(np.mean([r['txwin'] > 1 - 1e-9 for r in rows])),
                share_tie_all_t=float(np.mean([1e-9 < r['txwin'] < 1 - 1e-9 for r in rows])),
                share_shadow_all_t=len(shadow) / len(rows),
                tx_minus_const_payoff_mean=float(np.mean(gain)), tx_minus_const_payoff_min=float(np.min(gain)),
                tx_minus_const_payoff_max=float(np.max(gain)))
            log(inst, space, 'p1:', res['prediction1']['%s/%s' % (inst, space)]['n_efficient'], 'efficient complementary at t=vP, max offset',
                res['prediction1']['%s/%s' % (inst, space)]['max_offset_efficient'], 'more than 2 off:',
                res['prediction1']['%s/%s' % (inst, space)]['n_efficient_more_than_2_off'])
    # skew: the static map (delta_A, delta_B) -> (bA, bB) at t = 14, and the split distribution before selection
    inst = 'skew'
    v = C.INSTANCES[inst]; mr = C.min_revenue(v)
    U, X, B = S.build_tensor2(inst, 0)
    refs = reference_splits(inst)
    def split_stats(ts, label):
        counts = {}; classes = {'vn': 0, 'es': 0, 'ep': 0, 'other': 0}; dist = []; items_out = 0; ties = 0; n = 0
        for t in ts:
            kP = S.TX0 + t - 1
            for dA in range(1, 10):
                for dB in range(1, 10):
                    kA = S.F0 + dA - 1; kB = S.F0 + dB - 1
                    n += 1
                    bP, bA, bB = (int(x) for x in B[:, kP, kA, kB])
                    tw = float(X[C.XPRUWIN, kP, kA, kB])
                    if tw > 1e-9:
                        ties += int(tw < 1 - 1e-9)
                        continue
                    items_out += 1
                    counts[bA] = counts.get(bA, 0) + 1
                    classes[split_class(inst, bA, bB)] += 1
                    # distance of A's payment (with revenue bA + bB) to the nearest reference payment on the same total: L1 over the pair
                    dist.append(min(abs(bA - ra) + abs(bB - rb) for ra, rb in refs.values()))
        return dict(label=label, n_pairs=n, items_win_outright=items_out, ties=ties, A_payment_counts=dict(sorted(counts.items())),
                    exact_classes=classes, mean_L1_distance_to_nearest_reference=float(np.mean(dist)) if dist else None)
    mp = {}
    kP = S.TX0 + 14 - 1
    for dA in range(1, 10):
        for dB in range(1, 10):
            kA = S.F0 + dA - 1; kB = S.F0 + dB - 1
            bP, bA, bB = (int(x) for x in B[:, kP, kA, kB])
            mp['%d,%d' % (dA, dB)] = dict(bA=bA, bB=bB, T=bA + bB, txwin=float(X[C.XPRUWIN, kP, kA, kB]), rev=float(X[C.XREV, kP, kA, kB]),
                                          cls=split_class(inst, bA, bB))
    res['skew']['static_map_t14'] = mp
    res['skew']['split_distribution_t14'] = split_stats([14], 't = 14 only (uniform delta pairs)')
    res['skew']['split_distribution_t_uniform_1_14'] = split_stats(range(1, 15), 't uniform on 1..14')
    res['skew']['refs'] = refs
    json.dump(res, open(os.path.join(OUT, 'statics.json'), 'w'), indent=1, default=str)
    return res


# ================================================================== the cell registry
CELLS = {}


def reg(name, inst, space, arm, m, ptype='tx', itype='fol', rain_kind='same', rain_roles='all', N=100, group='', runs=None):
    gens = 20000 if arm == 'rain' else 5000
    CELLS[name] = dict(name=name, inst=inst, space=space, arm=arm, m=m, ptype=ptype, itype=itype, rain_kind=rain_kind, rain_roles=rain_roles, N=N,
                       I=64, gens=gens, group=group, runs=runs)


def mtag(m):
    return 'm%02d' % int(round(m * 100))


def build_registry():
    for inst in INSTS:                                  # primary grid
        for sp in SPACES:
            for arm in ('zero', 'ann3', 'rain', 'mig'):
                for m in (0.5, 0.2):
                    reg('p_%s_%s_%s_%s' % (inst, sp, arm, mtag(m)), inst, sp, arm, m, group='primary')
    NO = 'no-overbid'
    for arm in ('zero', 'rain', 'mig'):                 # (i) TX without followers, (ii) followers without TX
        reg('i_threshold_%s' % arm, 'threshold', NO, arm, 0.5, itype='const', group='control_i')
        reg('ii_threshold_%s' % arm, 'threshold', NO, arm, 0.5, ptype='const', group='control_ii')
    for inst in ('asymmetric', 'skew'):
        reg('i_%s_zero' % inst, inst, NO, 'zero', 0.5, itype='const', group='control_i')
        reg('ii_%s_zero' % inst, inst, NO, 'zero', 0.5, ptype='const', group='control_ii')
    for inst in INSTS:                                  # (iii) constants-only rain on these seeds
        for sp in SPACES:
            reg('iii_%s_%s_rain' % (inst, sp), inst, sp, 'rain', 0.5, ptype='const', itype='const', group='control_iii')
    for inst in INSTS:                                  # (iv) follower-only rain, (iv'') safe-follower rain
        for m in ((0.5, 0.2) if inst == 'threshold' else (0.5,)):
            reg('iv_%s_%s' % (inst, mtag(m)), inst, NO, 'rain', m, rain_kind='fol_only', group='control_iv')
            reg('ivb_%s_%s' % (inst, mtag(m)), inst, NO, 'rain', m, rain_kind='safe', group='control_ivb')
    for m in (0.5, 0.2):                                # (iv') rain split by role
        reg('ivp_P_threshold_%s' % mtag(m), 'threshold', NO, 'rain', m, rain_roles='P', group='control_ivp')
        reg('ivp_items_threshold_%s' % mtag(m), 'threshold', NO, 'rain', m, rain_roles='items', group='control_ivp')
    for inst in INSTS:                                  # (vi) matched constants
        for sp in SPACES:
            reg('vi_%s_%s_zero' % (inst, sp), inst, sp, 'zero', 0.5, ptype='matched', group='control_vi')
    reg('vi_threshold_rain', 'threshold', NO, 'rain', 0.5, ptype='matched', group='control_vi')
    reg('vi_threshold_zero_m20', 'threshold', NO, 'zero', 0.2, ptype='matched', group='control_vi')
    for N in (50, 200):                                 # (vii) N panel
        reg('vii_threshold_N%d' % N, 'threshold', NO, 'zero', 0.5, N=N, group='npanel')
    for N in (50, 200):
        reg('vii_threshold_unrestricted_N%d' % N, 'threshold', 'unrestricted', 'zero', 0.5, N=N, group='npanel')


build_registry()


def _crc(*parts):
    return zlib.crc32('|'.join(str(p) for p in parts).encode())


def founder_seed(cell, run):
    return [_crc('found', cell['inst'], cell['space'], cell['m'], cell['N'], cell['ptype'], cell['itype']), run, cell['I']]


def arrival_seed(cell, run):
    kind = 'rain' if cell['arm'] == 'rain' else cell['arm']
    return [_crc('arr', cell['inst'], cell['space'], cell['m'], cell['N'], kind), run, cell['I']]


def dyn_seed(cell, run):
    return (_crc('dyn', cell['name']) + 7919 * run) % (2 ** 31 - 1)


_T = {}


def tensors(cell, order=0):
    return S.build_tensor2(cell['inst'], order)


def make_cell_arrivals(cell, pr, run):
    N, I, gens = cell['N'], cell['I'], cell['gens']
    if cell['arm'] in ('zero', 'mig'):
        sched = np.zeros(gens)
    elif cell['arm'] == 'rain':
        sched = C.eps_schedule('rain', N, gens=gens)
    elif cell['arm'] == 'ann3':
        sched = C.eps_schedule('ann', N, A=3.0, gens=gens)
    else:
        raise ValueError(cell['arm'])
    rp = S.rain_prior(pr, cell['rain_kind'])
    roles = {'all': (0, 1, 2), 'P': (0,), 'items': (1, 2)}[cell['rain_roles']]
    return S.make_arrivals(sched, N, I, C.cdf_of(rp), arrival_seed(cell, run), roles=roles)


def run_one(cell, run, order=0):
    inst, space, N, I = cell['inst'], cell['space'], cell['N'], cell['I']
    v = C.INSTANCES[inst]; mr = C.min_revenue(v)
    U, X, Bt = tensors(cell, order)
    pr = S.prior2(inst, space, cell['m'], cell['ptype'], cell['itype'])
    rng = np.random.default_rng(founder_seed(cell, run))
    init = C.seed_counts(pr, I, N, rng)
    arr = make_cell_arrivals(cell, pr, run)
    smp = C.sample_times(cell['gens'])
    t0 = time.time()
    te = 5 if cell['arm'] == 'rain' else 1
    out = S.sim2(U, X, init, N, C.W, 0.01 if cell['arm'] == 'mig' else 0.0, cell['gens'], dyn_seed(cell, run), *arr, smp, mr, te)
    counts, samp, samp2, hist, first_erode, stop_g, pay, fix_items, fix_all, first_tested, rr, rm = out
    dt = time.time() - t0
    return dict(run=run, seconds=dt, counts=counts, samp=samp, samp2=samp2, hist=hist, first_erode=first_erode, stop=int(stop_g), fix_items=fix_items,
                fix_all=fix_all, first_tested=first_tested, rr=rr, rm=rm, smp=smp, init=init, Bt=Bt)


def process(cell, res):
    """per-island end rows and per-run series from a raw run."""
    inst, space, N, I = cell['inst'], cell['space'], cell['N'], cell['I']
    v = C.INSTANCES[inst]; vP = v[0]
    counts, samp, samp2, hist, smp = res['counts'], res['samp'], res['samp2'], res['hist'], res['smp']
    Bt = res['Bt']
    F = C.flags(inst, samp)
    fin = samp[-1]; fin2 = samp2[-1]
    Ff = {k: f[-1] for k, f in F.items()}
    ns = len(smp)
    rows = []
    rb = {'bluff_only': 0}
    for i in range(I):
        modal = [int(np.argmax(counts[i, r])) for r in range(3)]
        shares = [counts[i, r, modal[r]] / N for r in range(3)]
        fixed = [int(shares[r] > 1 - 1e-12) for r in range(3)]
        kP, kA, kB = modal
        bP, bA, bB = (int(x) for x in Bt[:, kP, kA, kB])
        txP = int(kP >= S.NC); folA = int(S.F0 <= kA < S.F0 + S.NF); folB = int(S.F0 <= kB < S.F0 + S.NF)
        tP = (kP - S.NC + 1) if txP else None
        qual = int(txP and fixed[0] and fixed[1] and fixed[2] and folA and folB and (bA + bB) > tP)
        fi = res['fix_items'][i]
        sel = np.arange(ns)
        pre = samp[:, i, 7][smp < fi] if fi >= 0 else samp[:, i, 7]
        post = samp[:, i, 7][smp >= fi] if fi >= 0 else np.array([])
        # bluff accounting on the end P population: TX programs (t > vP are bluffs), tested = first_tested >= 0 for that island
        tx_pop = tested_pop = tb = ub = bluff = 0
        for k in range(S.NC, S.K):
            c = int(counts[i, 0, k])
            if c == 0:
                continue
            t = k - S.NC + 1
            tx_pop += c
            tested = res['first_tested'][i, k] >= 0
            if tested:
                tested_pop += c
            if t > vP:
                bluff += c
                if tested:
                    tb += c
                else:
                    ub += c
        rows.append([res['run'], i, *[round(float(x), 5) for x in fin[i]],
                     txP, folA, folB, int(Ff['eroded'][i]), int(Ff['core'][i]), int(Ff['edge'][i]),
                     round(float(fin2[i, 0]), 5), round(float(fin2[i, 1]), 4), round(float(fin2[i, 2]), 4), round(float(fin2[i, 3]), 4), round(float(fin2[i, 4]), 5),
                     kP, kA, kB, round(shares[0], 3), round(shares[1], 3), round(shares[2], 3), *fixed, bP, bA, bB, bA + bB,
                     int(fi), int(res['fix_all'][i]), int(res['first_erode'][i]), int(res['rr'][-1, i]), int(res['rm'][-1, i]), qual,
                     round(float(pre.mean()), 6) if len(pre) else '', round(float(post.mean()), 6) if len(post) else '',
                     tx_pop, tested_pop, tb, ub, bluff, int(res['first_tested'][i, kP] >= 0) if txP else ''])
    # reorder: fin[i] has 18 entries (uP uA uB rev eff ir core txwin cyc | bmax P A B | bmed P A B | pru share P A B): the header names follow it
    return rows


def series_of(cell, res):
    inst, N, I = cell['inst'], cell['N'], cell['I']
    samp, samp2, hist, smp = res['samp'], res['samp2'], res['hist'], res['smp']
    F = C.flags(inst, samp)
    ser = dict(
        core_enc=samp[:, :, 6].mean(axis=1), core=F['core'].mean(axis=1), edge=F['edge'].mean(axis=1), eroded=F['eroded'].mean(axis=1),
        rev=samp[:, :, 3].mean(axis=1), eff=samp[:, :, 4].mean(axis=1), txwin=samp[:, :, 7].mean(axis=1),
        threat=samp2[:, :, 1].mean(axis=1), tx_share_P=samp[:, :, 15].mean(axis=1), fol_share_A=samp[:, :, 16].mean(axis=1),
        fol_share_B=samp[:, :, 17].mean(axis=1), dTX=samp2[:, :, 4].mean(axis=1), pwin=samp2[:, :, 0].mean(axis=1), meanT=samp2[:, :, 2].mean(axis=1),
        rrain=res['rr'].mean(axis=1), rmig=res['rm'].mean(axis=1))
    npres = (hist > 0).sum(axis=3)                            # (ns, I, 3)
    ser['fixed_items'] = ((npres[:, :, 1] == 1) & (npres[:, :, 2] == 1)).mean(axis=1)
    ser['fixed_all'] = (npres == 1).all(axis=2).mean(axis=1)
    # P threat distribution (mean over islands of the count share at each threat 0..40) at every sample
    thd = np.zeros((len(smp), 41))
    for k in range(S.K):
        th = int(S.threat_of(k))
        thd[:, th] += hist[:, :, 0, k].sum(axis=1) / (N * I)
    return ser, thd


HEAD = ['run', 'island', 'uP', 'uA', 'uB', 'rev', 'eff', 'ir', 'core_enc', 'txwin', 'cyc', 'bmaxP', 'bmaxA', 'bmaxB', 'bmedP', 'bmedA', 'bmedB', 'txshP', 'folshA',
        'folshB', 'txP', 'folA', 'folB', 'eroded', 'core', 'edge', 'pwin', 'threat', 'meanT', 'meanbP', 'dTX', 'kP', 'kA', 'kB', 'shP', 'shA', 'shB', 'fixP', 'fixA',
        'fixB', 'bP', 'bA', 'bB', 'T', 't_fix_items', 't_fix_all', 'first_erode', 'rrain', 'rmig', 'qual', 'txwin_pre', 'txwin_post', 'tx_pop', 'tested_pop',
        'tested_bluff_pop', 'untested_bluff_pop', 'bluff_pop', 'tx_modal_tested']


def _task(args):
    cell, runs = args
    out = []
    for r in runs:
        raw = run_one(cell, r)
        rows = process(cell, raw)
        ser, thd = series_of(cell, raw)
        # end-state P threat histogram (pooled over islands)
        th_end = np.zeros(41)
        for k in range(S.K):
            th_end[int(S.threat_of(k))] += raw['counts'][:, 0, k].sum()
        d = dict(run=r, seconds=raw['seconds'], stop=raw['stop'], rows=rows, ser={k: [float(x) for x in a] for k, a in ser.items()}, thd=thd.tolist(),
                 thd_end=th_end.tolist(), samples=[int(x) for x in raw['smp']])
        if r < 3:                                              # the reverse-order reproduction of the first three runs
            raw2 = run_one(cell, r, order=1)
            d['order_match'] = bool((raw['counts'] == raw2['counts']).all())
        out.append(d)
    return out


def summarize_cell(cell, results):
    results = sorted(results, key=lambda r: r['run'])
    keys = list(results[0]['ser'].keys())
    ser = {k: np.mean([r['ser'][k] for r in results], axis=0).tolist() for k in keys}
    ser_sd = {k: np.std([r['ser'][k] for r in results], axis=0).tolist() for k in keys}
    rows = [row for r in results for row in r['rows']]
    thd = np.mean([r['thd'] for r in results], axis=0).tolist()
    thd_end = np.sum([r['thd_end'] for r in results], axis=0).tolist()
    pr = S.prior2(cell['inst'], cell['space'], cell['m'], cell['ptype'], cell['itype'])
    th_prior = np.zeros(41)
    for k in range(S.K):
        th_prior[int(S.threat_of(k))] += pr[0, k]
    summary = dict(cell=cell, n_runs=len(results), samples=results[0]['samples'], series_mean=ser, series_sd_across_runs=ser_sd, threat_dist_series_mean=thd,
                   threat_dist_end_pooled=thd_end, threat_dist_prior=th_prior.tolist(), prior_mean_threat=S.prior_mean_threat(pr),
                   seconds_total=float(sum(r['seconds'] for r in results)), stops=[r['stop'] for r in results],
                   order_match=[r['order_match'] for r in results if 'order_match' in r])
    with gzip.open(os.path.join(OUT, 'rows_%s.csv.gz' % cell['name']), 'wt') as f:
        w = csv.writer(f); w.writerow(HEAD); w.writerows(rows)
    json.dump(summary, open(os.path.join(OUT, 'cell_%s.json' % cell['name']), 'w'))
    return summary


def pick(names):
    out = []
    for n in names:
        if n in CELLS:
            out.append(n)
        else:
            m = [k for k, c in CELLS.items() if c['group'] == n or k.startswith(n)]
            if not m:
                raise SystemExit('no cell or group %s' % n)
            out.extend(m)
    return list(dict.fromkeys(out))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('--cells', nargs='*', default=[])
    ap.add_argument('--runs', type=int, default=40)
    ap.add_argument('--workers', type=int, default=1)
    ap.add_argument('--chunk', type=int, default=5)
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--tag', default='')
    a = ap.parse_args()
    if a.cmd == 'statics':
        statics()
    elif a.cmd == 'list':
        for k, c in CELLS.items():
            log(k, c['group'], c['inst'], c['space'], c['arm'], c['m'], c['ptype'], c['itype'], c['rain_kind'], c['rain_roles'], c['N'], c['gens'])
    elif a.cmd == 'cells':
        names = pick(a.cells)
        todo = [n for n in names if a.force or not os.path.exists(os.path.join(OUT, 'cell_%s.json' % n))]
        log('cells', todo)
        for n in todo:
            cell = CELLS[n]
            t0 = time.time()
            nr = cell.get('runs') or a.runs
            chunks = [list(range(s, min(s + a.chunk, nr))) for s in range(0, nr, a.chunk)]
            tasks = [(cell, ch) for ch in chunks]
            if a.workers > 1:
                with Pool(a.workers, maxtasksperchild=1) as pool:
                    res = [x for part in pool.imap_unordered(_task, tasks) for x in part]
            else:
                res = [x for t in tasks for x in _task(t)]
            s = summarize_cell(cell, res)
            sm = s['series_mean']
            log('%s done %.0fs  end: core_enc %.3f core %.3f eroded %.3f rev %.2f eff %.3f threat %.2f txwin %.3f ordermatch %s' % (
                n, time.time() - t0, sm['core_enc'][-1], sm['core'][-1], sm['eroded'][-1], sm['rev'][-1], sm['eff'][-1], sm['threat'][-1], sm['txwin'][-1],
                all(s['order_match'])))
