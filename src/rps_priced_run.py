"""Driver for the priced RPS experiment (spec specs/2026-10-23-rps-priced.md; notes/rps-priced.md; predictions/2026-10-23-rps-priced.md).

    python3 src/rps_priced_run.py prep                     # tables (game payoff, depth/work cost, forfeit mass) -> cache outside the repo
    python3 src/rps_priced_run.py static                   # classes, splits, statics, identities -> runs/rps_priced/static.json
    python3 src/rps_priced_run.py toy                      # the eleven-program toy chain, priced
    python3 src/rps_priced_run.py n7work                   # work versus depth at n = 7 on the unpriced class representatives
    python3 src/rps_priced_run.py job ARM --c 0.01 [--kind depth|work|forfeit] [--D 12] [--chains 100 1000 ...]
                                  [--lottery primary size] [--sens] [--runs a b]
Outputs under runs/rps_priced/ (small json / json.gz only).  Every chain number is an eps -> 0 object (pi); every lottery
number is an eps = 0 finite-(N, I, horizon) statistic.
"""
import argparse, gzip, json, math, os, sys, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rps as RP
import rps_priced as PP
import rps_run as RR
from chain_log import LogChain
import solver_audit as SA

ROOT = RP.ROOT
OUT = os.path.join(ROOT, 'runs', 'rps_priced')
os.makedirs(OUT, exist_ok=True)
ARMS = ('pure', 'sample', 'matched', 'exact')
CS = (0.001, 0.01, 0.05)
NS = (100, 1000, 10000, 100000)
jdump, jload = RR.jdump, RR.jload

CELLS = {
    'primary': dict(N=100, I=64, runs=40, horizon=10000),
    'size': dict(N=400, I=16, runs=20, horizon=10000),
    'primary200': dict(N=100, I=64, runs=200, horizon=2000),
}
BASE_CPS = [100, 250, 500, 1000, 1500, 2000, 5000, 10000]
WIN = (1500, 2000)             # the 500-generation window for the resolution rule at the primary reading
WIN_LATE = (9500, 10000)
KEEP_ARR = ['e_prog', 'e_gross', 'e_indiv', 'mix_pop', 'forfeit_plays', 'cost_paid', 'share_readers', 'share_guarded',
            'share_X', 'nclass', 'e_exset', 'homo']


def tag_of(arm, kind, c, D):
    return '%s_%s_c%s_D%d' % (arm, kind, repr(c), D)


# ================================================================ the chain
def discover(A, att_starts=1000, att_sub=6, closure_nodes=6000, branch=8, pool_cap=None):
    """Candidate stable supports of the priced class table, independent of N: exhaustive pairs and triples, the invasion
    closure (the `branch` strongest invaders at each node; the unrestricted closure explodes once stable polymorphisms
    exist), and a multi-start replicator search for attractors of support up to att_sub."""
    t0 = time.time()
    U = np.round(A.U, 9)
    mu = A.mass
    K = A.K
    pool = None
    if pool_cap is not None and K > pool_cap:
        pool = np.argsort(-mu)[:pool_cap]
    cands, counts = SA.enumerate_candidates_fast(U, mu, pool=pool, keep_all=False)
    S1, n1, comp1 = SA.invasion_closure(U, mu, max_nodes=closure_nodes, branch=branch)
    have = set(tuple(sorted(c['ids'])) for c in cands)
    n_clos_new = 0
    for c in S1:
        if c['size'] >= 2 and tuple(sorted(c['ids'])) not in have:
            have.add(tuple(sorted(c['ids']))); cands.append(c); n_clos_new += 1
    att = SA.attractor_search(U, mu, n_starts=att_starts, seed=1, max_sub=att_sub) if att_starts else []
    n_att_stable = 0; n_att_new = 0
    att_sizes = defaultdict(int)
    for c in att:
        if c['status'] == 'stable':
            att_sizes[min(c['size'], 7)] += 1
        if c['status'] == 'stable' and c['size'] >= 2:
            n_att_stable += 1
            key = tuple(sorted(c['ids']))
            if key not in have:
                have.add(key); cands.append(c); n_att_new += 1
    sel = [c for c in cands if c['status'] == 'stable' and c['size'] > 1]
    n_center = sum(1 for c in cands if c['status'] == 'center')
    d = dict(seeds=[(list(c['ids']), list(c['x'])) for c in sel], layer=[c['n_adv'] == 0 for c in sel],
             info=dict(n_candidates=len(cands), n_seeded=len(sel), n_center=n_center, closure_nodes=n1, closure_complete=bool(comp1),
                       closure_branch=branch, n_closure_new=n_clos_new, n_saturated_closure=len(S1),
                       saturated_closure=[dict(ids=[A.names[i] for i in c['ids']][:6], size=c['size']) for c in S1[:10]],
                       n_attractor_search_rest=len(att), n_attractor_search_stable_poly=n_att_stable, n_attractor_search_new=n_att_new,
                       attractor_stable_sizes={str(k): v for k, v in sorted(att_sizes.items())}, att_starts=att_starts, att_sub=att_sub,
                       enum_counts={k: int(v) for k, v in counts.items()}, n_noadv_candidates=int(sum(1 for c in cands if c['n_adv'] == 0 and c['size'] > 1)),
                       pool_cap=pool_cap, time_s=time.time() - t0))
    return d


def chain_cell_p(A, N, Aex, emap, disc, log_theta=math.log(1e-14), twins=True, max_states=40000, verbose=False):
    """Closure-seeded log-domain chain of the priced class table (seeds from `discover`), with support-size diagnostics
    (rps_run.chain_cell, extended)."""
    t0 = time.time()
    U = np.round(A.U, 9)
    mu = A.mass
    K = A.K
    seeds, layer = disc['seeds'], disc['layer']
    prov = RP.ClassProvider(U, mu)
    ch = LogChain(prov, N=N, w=RP.W, Ufull=prov.Ufull if twins else None, twins=twins, theta=1.0, max_states=10 ** 9)
    ch.explore_log(extra_states=seeds, log_theta=log_theta, max_states=max_states + len(seeds), verbose=verbose, layer_mask=layer)
    keys_all, lpi_all, info, out_un, rec = ch.solve_sparse()
    keys = [keys_all[i] for i in rec]
    lpi = lpi_all[rec]
    pi = np.exp(lpi - lpi.max()); pi /= pi.sum()
    nm = RP.named_classes(A)
    res = dict(arm=A.arm, kind=A.kind, c=A.cprice, N=N, D=A.D, twins=twins, K=K, log10_theta=log_theta / math.log(10),
               discovery=disc['info'], n_expanded=len(ch.trans), n_recurrent=len(keys), closed=info,
               log10_cut=float(ch.log_cut / math.log(10)) if np.isfinite(ch.log_cut) else None, n_cand_left=int(ch.n_cand_left),
               n_twin_moves=int(ch.n_twin_moves), underflow=int(ch.underflow))
    agg = defaultdict(float)
    states = []
    for k, p in zip(keys, pi):
        ids, x, kind = ch.states[k]
        st = PP.state_stats_p(A, ids, x, nm, Aex, emap)
        for kk, v in st.items():
            if isinstance(v, (int, float)) and not (isinstance(v, float) and math.isnan(v)) and kk not in ('e_prog_arg',):
                agg[kk] += p * v
        states.append((p, ids, x, st))
    res['pi_stat'] = dict(agg)
    # support-size distribution and polymorphic mass
    hist = defaultdict(float)
    for p, ids, x, st in states:
        hist[min(len(ids), 7)] += p
    res['pi_support_size'] = {str(k): float(v) for k, v in sorted(hist.items())}
    res['pi_polymorphic_mass'] = float(sum(p for p, ids, x, st in states if len(ids) > 1))
    res['pi_mass_of_states_with_support_gt_3'] = float(sum(p for p, ids, x, st in states if len(ids) > 3))
    key_pi = dict(zip(keys, pi))
    indet = defaultdict(float); indet_n = defaultdict(int)
    for (key, q, traj) in ch.indeterminate:
        if key in key_pi:
            sup = tuple(A.names[c] for c in sorted(set(int(c) for c in traj[0][0]))) if traj else ()
            indet[sup] += key_pi[key] * mu[q]; indet_n[sup] += 1
    res['indeterminate_total_events'] = len(ch.indeterminate)
    res['indeterminate_pi_weighted_mutation_mass'] = float(sum(indet.values()))
    res['indeterminate_top'] = [dict(support=list(k)[:6], mass=float(v), events=indet_n[k]) for k, v in sorted(indet.items(), key=lambda kv: -kv[1])[:5]]
    order = np.argsort(-pi)
    top = []
    for i in order[:12]:
        p, ids, x, st = states[i]
        top.append(dict(pi=float(p), state=RR.state_name(A, ids, x), n_classes=len(ids), e_prog=st['e_prog'], e_gross=st['e_gross'],
                        mix_pop=st['mix_pop'], forfeit_self=st['forfeit_self'], forfeit_plays=st['forfeit_plays'], cost_paid=st['cost_paid']))
    res['top_states'] = top
    cum = np.cumsum(pi[order])
    res['n_states_for_0.99'] = int(np.searchsorted(cum, 0.99) + 1)
    cls_share = np.zeros(K)
    for p, ids, x, st in states:
        cls_share[list(ids)] += p * np.asarray(x)
    o = np.argsort(-cls_share)
    res['class_share_all'] = [(A.names[c], float(cls_share[c])) for c in o if cls_share[c] > 0]
    res['class_share_top'] = [(A.names[c], float(cls_share[c]), int(A.lang.size[A.rep[c]])) for c in o[:15]]
    res['class_share_readers'] = float(cls_share[A.reader].sum())
    res['class_share_guarded'] = float(cls_share[A.guarded].sum())
    res['class_share_X'] = float(cls_share[nm['X']]) if 'X' in nm else 0.0
    res['prior_mass_X'] = float(A.mass[nm['X']]) if 'X' in nm else 0.0
    try:
        LA, _ = ch.log_matrix(keys)
        exits = []
        for ti in order[:3]:
            row = LA[ti]; fin = np.isfinite(row); fin[ti] = False
            tot = float(np.logaddexp.reduce(row[fin]) / math.log(10)) if fin.any() else None
            ex = []
            for j in np.argsort(-np.where(fin, row, -np.inf))[:4]:
                if not fin[j]: break
                ids, x, _ = ch.states[keys[j]]
                muts = sorted(ch.lmut.get((keys[ti], keys[j]), {}).items(), key=lambda kv: -kv[1])[:3]
                ex.append(dict(to=RR.state_name(A, ids, x, 4), log10_rate=float(row[j] / math.log(10)),
                               mutants=[(A.names[int(q)], float(v / math.log(10))) for q, v in muts]))
            ids, x, _ = ch.states[keys[ti]]
            exits.append(dict(state=RR.state_name(A, ids, x, 4), pi=float(pi[ti]), log10_total_exit=tot, top_exits=ex))
        res['top_exits'] = exits
    except Exception as e:      # pragma: no cover
        res['top_exits_error'] = repr(e)
    try:
        res['pi_equivariance'] = RR.pi_equivariance(A, ch, keys, pi, N)
    except AssertionError as e:      # pragma: no cover
        res['pi_equivariance'] = dict(error='relabeling splits a class')
    res['time_s'] = time.time() - t0
    return res


def cmd_chain(A, Aex, emap, a):
    disc = discover(A, pool_cap=a.pool_cap)
    print('discovery %s: %s' % (tag_of(a.arm, a.kind, a.c, a.D), json.dumps(disc['info'])), flush=True)
    for N in a.chains:
        lt0 = a.log10theta * math.log(10)
        variants = [('', lt0, True)]
        if a.sens and N == 10000:
            variants += [('_th%d' % round(-(a.log10theta + 2)), lt0 + 2 * math.log(10), True), ('_th%d' % round(-(a.log10theta - 2)), lt0 - 2 * math.log(10), True),
                         ('_lumped', lt0, False)]
        for sfx, lt, tw in variants:
            t0 = time.time()
            res = chain_cell_p(A, N, Aex, emap, disc, log_theta=lt, twins=tw)
            path = os.path.join(OUT, 'chain_%s_N%d%s.json' % (tag_of(a.arm, a.kind, a.c, a.D), N, sfx))
            jdump(res, path)
            st = res['pi_stat']
            print('chain %s N=%d%s: K=%d rec=%d poly=%.3f  e=%.4f egross=%.4f mix=%.3f fself=%.3f X=%.3f readers=%.3f (%.0fs)' % (
                tag_of(a.arm, a.kind, a.c, a.D), N, sfx, res['K'], res['n_recurrent'], res['pi_polymorphic_mass'], st['e_prog'],
                st['e_gross'], st['mix_pop'], st['forfeit_self'], st.get('share_X', 0), st['share_readers'], time.time() - t0), flush=True)


# ================================================================ the lottery
def one_run(A, cell, r, Aex, emap, nm, tagarm):
    c = CELLS[cell]
    N, I, horizon = c['N'], c['I'], c['horizon']
    cps = set(g for g in BASE_CPS if g <= horizon)
    cps |= set(range(WIN[0], WIN[1] + 1, 10))
    if horizon >= WIN_LATE[1]:
        cps |= set(range(WIN_LATE[0], WIN_LATE[1] + 1, 10))
    cps = np.array(sorted(cps), np.int64)
    seed_f = RP.run_seed('founders|%s' % cell, r)                 # the unpriced run's founder seeds: paired run by run
    init = RP.draw_founders(A.lang, A.cls_of, A.K, I, N, seed_f)
    idx, init_l = RP.compress_run(init)
    Ul = np.ascontiguousarray(A.U[np.ix_(idx, idx)])
    seed_d = RP.run_seed('dynamics|%s|%s' % (cell, A.arm), r)       # the unpriced dynamics seed (exact reproduction at c = 0)
    t0 = time.time()
    out, nalive, homo, nwin = RP.lottery_kernel(Ul, init_l, N, RP.W, 1.0 / N, seed_d, cps, WIN[0], WIN[1], 10)
    wall = time.time() - t0
    rec = dict(arm=A.arm, kind=A.kind, c=A.cprice, D=A.D, cell=cell, run=r, N=N, I=I, K_start=int(len(idx)), wall=wall,
               horizon=int(horizon), nwin=int(nwin), nalive_window=(nalive / max(nwin, 1)).tolist(),
               homo_window=(homo / max(nwin, 1)).tolist(), stats={}, means={}, arr={}, comp={})
    cpl = list(cps)
    full_at = {}
    for ci, g in enumerate(cps):
        if int(g) in BASE_CPS and int(g) <= horizon:
            full = np.zeros((I, A.K), np.int64)
            full[:, idx] = out[ci]
            full_at[int(g)] = full
            st = PP.island_stats_p(A, full, N, nm, Aex, emap)
            rec['means'][str(int(g))] = {k: float(np.mean(v)) for k, v in st.items()}
            rec['means'][str(int(g))]['share_e_le_0.05'] = float(np.mean(st['e_prog'] <= 0.05 + 1e-12))
            if int(g) in (2000, 10000):
                rec['arr'][str(int(g))] = {k: np.round(st[k], 5).tolist() for k in KEEP_ARR if k in st}
            if int(g) in (500, 2000, 10000):
                comp = []
                for i in range(I):
                    nz = np.nonzero(full[i])[0]
                    comp.append([(int(k), int(full[i, k])) for k in nz])
                rec['comp'][str(int(g))] = comp
    # resolution rule on the 500-generation windows (support = classes with share >= 0.05)
    for name, (w0, w1) in (('2000', WIN), ('10000', WIN_LATE)):
        if w1 > horizon:
            continue
        sel = [i for i, g in enumerate(cps) if w0 <= g <= w1]
        seqs = np.zeros((len(sel), I, A.K), np.int64)
        seqs[:, :, idx] = out[sel]
        cls = []; chg = []
        for i in range(I):
            kcls, nch = PP.support_class(seqs[:, i, :], N)
            cls.append(kcls); chg.append(nch)
        rec['resolution_' + name] = dict(resolved=cls.count('resolved'), cycling=cls.count('cycling'), unresolved=cls.count('unresolved'),
                                         mean_support_changes=float(np.mean(chg)), per_island=cls)
    rec['founder_mass_X'] = float(init[:, nm['X']].sum() / (I * N)) if 'X' in nm else 0.0
    return rec


def cmd_lottery(A, Aex, emap, a):
    nm = RP.named_classes(A)
    tagarm = tag_of(a.arm, a.kind, a.c, a.D)
    for cell in a.lottery:
        cfg = CELLS[cell]
        r0, r1 = (a.runs if a.runs else (0, cfg['runs']))
        path = os.path.join(OUT, 'lottery_%s_%s.jsonl.gz' % (tagarm, cell))
        rows = []
        done = set()
        if os.path.exists(path):
            rows = [json.loads(l) for l in gzip.open(path, 'rt')]
            done = {r['run'] for r in rows}
        t0 = time.time()
        for r in range(r0, r1):
            if r in done:
                continue
            rec = one_run(A, cell, r, Aex, emap, nm, tagarm)
            rows.append(rec)
            if (r - r0) % 5 == 4 or r == r1 - 1:
                with gzip.open(path + '.tmp', 'wt') as f:
                    for x in rows: f.write(json.dumps(x) + '\n')
                os.replace(path + '.tmp', path)
            g = '2000' if '2000' in rec['means'] else str(rec['horizon'])
            m = rec['means'][g]
            print('lottery %s %s run %d: %.0fs  e %.3f mix %.3f forfeit %.3f nclass %.2f unres %s' % (
                tagarm, cell, r, rec['wall'], m['e_prog'], m['mix_pop'], m['forfeit_plays'], m['nclass'],
                rec.get('resolution_2000', {}).get('unresolved')), flush=True)
        print('done %s %s (%.0fs)' % (tagarm, cell, time.time() - t0), flush=True)


# ================================================================ jobs
def cmd_job(a):
    t0 = time.time()
    b = PP.load_base(a.arm, 6, a.D)
    A = PP.make_arm(b, a.c, a.kind)
    print('job %s: K=%d classes (%.0fs)' % (tag_of(a.arm, a.kind, a.c, a.D), A.K, time.time() - t0), flush=True)
    Aex = emap = None
    if a.arm in ('pure', 'sample', 'matched', 'exact'):
        Aex = PP.get_aex(a.c, a.kind, a.D)
        emap = PP.embed_priced(A, Aex)
    if a.chains:
        cmd_chain(A, Aex, emap, a)
    if a.lottery:
        cmd_lottery(A, Aex, emap, a)
    print('job done %s (%.0fs)' % (tag_of(a.arm, a.kind, a.c, a.D), time.time() - t0), flush=True)


def cmd_prep(a):
    jobs = [('pure', 12), ('sample', 12), ('matched', 12), ('exact', 12), ('exact_br', 12), ('sample', 8), ('exact', 8), ('sample', 16), ('exact', 16)]
    for arm, D in jobs:
        if not os.path.exists(PP.base_path(arm, 6, D) + '_HW.npy'):
            PP.build_base(arm, 6, D, verbose=True)
    # lite priced exact class tables for the exploiter-set control
    need = [(c, 'depth', 12) for c in CS] + [(0.01, 'forfeit', 12)] + [(0.015, 'depth', 8), (0.0075, 'depth', 16)]
    for c, kind, D in need:
        PP.get_aex(c, kind, D)
        print('aex', c, kind, D, flush=True)


def unpriced_arm(arm, D=12):
    b = PP.load_base(arm, 6, D)
    return PP.make_arm(b, 0.0, 'depth', dec=6)


def hand_check(A):
    """max |priced U - hand value| over the eleven named programs at the arm's price (notes 1.2-1.3, depth price)."""
    return None


def cmd_static(a):
    out = {}
    combos = []
    for arm in ARMS + ('exact_br',):
        for c in (0.0,) + CS:
            combos.append((arm, c, 'depth', 12))
    for arm in ARMS:
        combos.append((arm, 0.01, 'forfeit', 12))
    for arm in ('sample', 'exact'):
        combos += [(arm, 0.015, 'depth', 8), (arm, 0.0075, 'depth', 16)]
    cache_base = {}
    for arm, c, kind, D in combos:
        t0 = time.time()
        key = (arm, D)
        if key not in cache_base:
            cache_base.clear(); cache_base[key] = PP.load_base(arm, 6, D)
        b = cache_base[key]
        A = PP.make_arm(b, c, kind)
        rec = dict(arm=arm, c=c, kind=kind, D=D, S=int(b.lang.S), K=int(A.K), antisym_err_game=A.antisym_err,
                   member_row_dev=A.member_row_dev, H_max=float(np.asarray(b.H).max()), HW_max=float(np.asarray(b.HW).max()),
                   max_abs_work_minus_depth=float(np.abs(np.asarray(b.HW) - np.asarray(b.H)).max()))
        if c > 0:
            U0 = PP.make_arm(b, 0.0, 'depth', dec=6)
            rec['split'] = PP.split_report(A, U0)
        # relabeling equivariance of the priced class table
        try:
            sig = A.lang.relabel_map(1)
            perm = RP.class_perm(A, sig)
            rec['equivariance_err_U'] = float(np.abs(A.U[np.ix_(perm, perm)] - A.U).max())
        except AssertionError:
            rec['equivariance_err_U'] = None
        # Prediction 1 statics at the program level (arms with X)
        L = b.lang
        if arm != 'pure':
            Un = np.asarray(b.U) - PP.price_matrix(b, c, kind)
            xid = L.find('X')
            F = np.asarray(b.F)
            Fself = np.diag(F)
            forf = np.nonzero(Fself > 1e-12)[0]
            cost = PP.price_matrix(b, c, kind)
            rec['pred1'] = dict(
                n_programs=int(L.S), n_self_forfeiting=int(len(forf)), X_min_payoff_vs_any=float(Un[xid].min()),
                X_cost_max=float(cost[xid].max()),
                X_payoff_equals_forfeit_mass_err=float(np.abs(np.asarray(b.U)[xid] - F[:, xid]).max()),
                invade_fail=int((Un[xid, forf] - Un[forf, forf] <= 1e-9).sum()),
                weak_dominance_fail=int((Un[xid, xid] - Un[forf, xid] < -1e-9).sum()),
                min_invade_margin=float((Un[xid, forf] - Un[forf, forf]).min()) if len(forf) else None,
                min_dominance_margin=float((Un[xid, xid] - Un[forf, xid]).min()) if len(forf) else None,
                frac_prior_forfeiting=float(L.mu[forf].sum()))
            # a class dominating X? any program with net payoff against X > 0
            rec['pred1']['programs_earning_gt0_vs_X'] = int((Un[:, xid] > 1e-9).sum())
        out['%s_%s_c%s_D%d' % (arm, kind, repr(c), D)] = rec
        print('static %s: K=%d (%.0fs)' % (tag_of(arm, kind, c, D), A.K, time.time() - t0), flush=True)
    jdump(out, os.path.join(OUT, 'static.json'))


# ================================================================ toy chain
def cmd_toy(a):
    from chain import Chain
    names = ['R', 'P', 'S', 'X', 'TM', 'N', 'N2', 'C', 'GN', 'GC', 'M']
    b = PP.load_base('exact', 6, 12)
    out = {}
    for c in (0.0, 0.001, 0.01, 0.05):
        A = PP.make_arm(b, c, 'depth')
        nm = RP.named_classes(A)
        # the eleven programs as eleven classes (payoff twins kept distinct): rows of the program-level priced table
        L = b.lang
        pid = [L.find(RP.NAMED[k]) for k in names]
        Un = np.asarray(b.U)[np.ix_(pid, pid)] - PP.price_matrix(b, c, 'depth')[np.ix_(pid, pid)]
        mu = np.ones(len(pid)) / len(pid)
        for N in (100, 1000, 10000):
            prov = RP.ClassProvider(Un, mu)
            ch = LogChain(prov, N=N, w=RP.W, Ufull=prov.Ufull, twins=True, theta=1.0, max_states=10 ** 9)
            ch.explore_closure(max_states=20000)
            keys_all, lpi_all, info, out_un, rec = ch.solve_sparse()
            keys = [keys_all[i] for i in rec]; pi = np.exp(lpi_all[rec]); pi /= pi.sum()
            share = defaultdict(float); top = []
            for k, p in zip(keys, pi):
                ids, x, kind = ch.states[k]
                for i, xi in zip(ids, x):
                    share[names[i]] += p * xi
            order = np.argsort(-pi)
            for i in order[:6]:
                ids, x, kind = ch.states[keys[i]]
                top.append(dict(pi=float(pi[i]), state=' + '.join('%s:%.3f' % (names[c_], xi) for c_, xi in zip(ids, x))))
            mono_X = float(sum(p for k, p in zip(keys, pi) if list(ch.states[k][0]) == [names.index('X')]))
            guard = float(sum(p * sum(xi for i, xi in zip(ch.states[k][0], ch.states[k][1]) if names[i] in ('GN', 'GC')) for k, p in zip(keys, pi)))
            # the same contest through chain.Chain (linear weights), compared on pi
            chl = Chain(prov, N=N, w=RP.W, theta=0.0, max_states=20000).explore()
            out['c%s_N%d' % (repr(c), N)] = dict(c=c, N=N, n_states=len(keys), pi_X_mono=mono_X, class_share={k: float(v) for k, v in share.items()},
                                                 guarded_share=guard, top=top, indeterminate=len(ch.indeterminate), closed=info,
                                                 n_states_linear_chain=len(chl.trans))
            print('toy c=%s N=%d: pi(X mono) %.4f  X share %.4f  guarded %.4f  states %d' % (c, N, mono_X, share['X'], guard, len(keys)), flush=True)
    jdump(out, os.path.join(OUT, 'toy.json'))


# ================================================================ n = 7: work versus depth
def cmd_n7work(a):
    """Work versus depth where they can differ: exact reading of a coin with two application branches (n >= 7).  On the
    unpriced n = 7 exact class representatives (376 classes; the classes are NOT recomputed under the price here) and the
    lifted arguments they need, the depth and work cost tables are computed by the closed-subset cost kernel and the
    eps -> 0 chain is run at c = 0.01 under each."""
    import rps_n7
    t0 = time.time()
    A7 = RP.get_arm('exact', 7, 12, 'bits')
    L = A7.lang
    Z = np.unique(np.concatenate([rps_n7.small_programs(L), A7.rep]))
    H, _ = PP.cost_table_subset(L, Z, 12, work=False)
    HW, _ = PP.cost_table_subset(L, Z, 12, work=True)
    pos = {int(z): i for i, z in enumerate(Z)}
    idx = np.array([pos[int(r)] for r in A7.rep])
    Hc = H[np.ix_(idx, idx)]; HWc = HW[np.ix_(idx, idx)]
    diff = HWc - Hc
    out = dict(K=int(A7.K), closed_set=int(len(Z)), max_depth=float(Hc.max()), max_work=float(HWc.max()),
               n_pairs_work_gt_depth=int((diff > 1e-9).sum()), n_pairs=int(diff.size), max_work_minus_depth=float(diff.max()),
               min_work_minus_depth=float(diff.min()), time_build=time.time() - t0)
    w = np.argwhere(diff > 1e-9)
    out['examples'] = [(A7.names[i], A7.names[j], float(Hc[i, j]), float(HWc[i, j])) for i, j in w[np.argsort(-diff[tuple(w.T)])][:8]]
    print('n7work: ', json.dumps({k: v for k, v in out.items() if k != 'examples'}), flush=True)
    c = 0.01
    reader = np.array([bool((L.t_op[r, :L.t_len[r]] == RP.OP_APP).any()) for r in A7.rep])
    guarded = np.array([bool((L.t_op[r, :L.t_len[r]] == RP.OP_COIN).any() and (L.t_op[r, :L.t_len[r]] == RP.OP_APP).any()) for r in A7.rep])
    for kind, Hm in (('depth', Hc), ('work', HWc)):
        P = PP.PArm()
        P.arm, P.n, P.D, P.lang, P.mu_kind = 'exact', 7, 12, L, 'bits'
        P.cprice, P.kind = c, kind
        P.K, P.rep, P.members, P.mass, P.cls_of, P.names = A7.K, A7.rep, A7.members, A7.mass, A7.cls_of, A7.names
        P.Ug = A7.U; P.Hc = c * Hm; P.U = np.round(A7.U - c * Hm, 12); P.Gcl = A7.Gcl
        P.reader, P.guarded = reader, guarded
        disc = discover(P, att_starts=400)
        for N in (1000, 10000):
            res = chain_cell_p(P, N, None, None, disc)
            st = res['pi_stat']
            out['%s_N%d' % (kind, N)] = dict(e_prog=st['e_prog'], e_gross=st['e_gross'], mix_pop=st['mix_pop'], forfeit_self=st['forfeit_self'],
                                              forfeit_plays=st['forfeit_plays'], X=st.get('share_X', 0.0), readers=st['share_readers'],
                                              cost_paid=st['cost_paid'], poly=res['pi_polymorphic_mass'], n_recurrent=res['n_recurrent'])
            print('n7work chain %s N=%d: %s' % (kind, N, out['%s_N%d' % (kind, N)]), flush=True)
    jdump(out, os.path.join(OUT, 'n7work.json'))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd')
    sp.add_parser('prep'); sp.add_parser('static'); sp.add_parser('toy'); sp.add_parser('n7work')
    j = sp.add_parser('job'); j.add_argument('arm'); j.add_argument('--c', type=float, required=True)
    j.add_argument('--kind', default='depth'); j.add_argument('--D', type=int, default=12)
    j.add_argument('--chains', type=int, nargs='*', default=[]); j.add_argument('--lottery', nargs='*', default=[])
    j.add_argument('--sens', action='store_true'); j.add_argument('--runs', type=int, nargs=2)
    j.add_argument('--pool-cap', type=int, default=None); j.add_argument('--log10theta', type=float, default=-8.0)
    a = ap.parse_args()
    {'prep': cmd_prep, 'static': cmd_static, 'toy': cmd_toy, 'job': cmd_job, 'n7work': cmd_n7work}[a.cmd](a)


if __name__ == '__main__':
    main()
