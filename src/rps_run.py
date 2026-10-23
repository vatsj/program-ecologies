"""Driver for the RPS experiment (spec specs/2026-10-23-rps-mixed.md; notes/rps.md; predictions/2026-10-23-rps.md).

    python3 src/rps_run.py static                                  # tables, validation numbers  -> runs/rps/static.json
    python3 src/rps_run.py chain ARM N [--D 12] [--mu bits|nodes] [--twins 0|1] [--logtheta -32.2]
    python3 src/rps_run.py toy                                     # the eleven-class toy chain at D = 11, 12, 13, 20
    python3 src/rps_run.py lottery ARM CELL [--runs a b]           # CELL in primary | size | cont
    python3 src/rps_run.py sweep                                   # depth sweep on pairs of the classes that matter
Outputs under runs/rps/ (small json / json.gz only).  Every chain number is an eps -> 0 object (pi); every lottery
number is an eps = 0 finite-(N, I, horizon) statistic.
"""
import argparse, gzip, json, math, os, sys, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rps as RP
from chain_log import LogChain, NEG
import solver_audit as SA

ROOT = RP.ROOT
OUT = os.path.join(ROOT, 'runs', 'rps')
os.makedirs(OUT, exist_ok=True)
ARM_LIST = ('pure', 'sample', 'exact', 'matched')
STOCH = ('sample', 'exact', 'matched')
NS_CHAIN = (100, 1000, 10000, 100000)
SWEEP_D = (11, 12, 13, 20)
SENS = ('exact_uniform', 'exact_br')
BENCH = ('constants', 'constx')


def jdump(obj, path, gz=False):
    def default(o):
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, np.ndarray): return o.tolist()
        raise TypeError(type(o))
    data = json.dumps(obj, default=default)
    if gz:
        with gzip.open(path, 'wt') as f: f.write(data)
    else:
        with open(path, 'w') as f: f.write(data)


def jload(path):
    if path.endswith('.gz'):
        with gzip.open(path, 'rt') as f: return json.load(f)
    with open(path) as f: return json.load(f)


# ================================================================ the chain
def state_name(A, ids, x, k=6):
    o = np.argsort(-np.asarray(x))[:k]
    s = ' + '.join('%s:%.3f' % (A.names[ids[i]], x[i]) for i in o)
    return s + (' + ...' if len(ids) > k else '')


def chain_cell(A, N, log_theta=math.log(1e-14), twins=True, max_states=20000, verbose=False, closure_nodes=6000,
               mu_override=None):
    """Closure-seeded log-domain chain (solver audit protocol, IMPLEMENTATION 4) on the class table of A."""
    t0 = time.time()
    U = np.round(A.U, 9)
    mu = A.mass if mu_override is None else mu_override
    K = A.K
    cands, counts = SA.enumerate_candidates_fast(U, mu, keep_all=False)
    S1, n1, comp1 = SA.invasion_closure(U, mu, max_nodes=closure_nodes)
    have = set(tuple(sorted(c['ids'])) for c in cands)
    for c in S1:
        if c['size'] >= 2 and tuple(sorted(c['ids'])) not in have:
            have.add(tuple(sorted(c['ids']))); cands.append(c)
    sel = [c for c in cands if c['status'] == 'stable' and c['size'] > 1]
    n_center = sum(1 for c in cands if c['status'] == 'center')
    seeds = [(list(c['ids']), list(c['x'])) for c in sel]
    layer = [c['n_adv'] == 0 for c in sel]
    prov = RP.ClassProvider(U, mu)
    ch = LogChain(prov, N=N, w=RP.W, Ufull=prov.Ufull if twins else None, twins=twins, theta=1.0, max_states=10 ** 9)
    ch.explore_log(extra_states=seeds, log_theta=log_theta, max_states=max_states + len(seeds), verbose=verbose, layer_mask=layer)
    keys_all, lpi_all, info, out_un, rec = ch.solve_sparse()
    keys = [keys_all[i] for i in rec]
    lpi = lpi_all[rec]
    pi = np.exp(lpi - lpi.max()); pi /= pi.sum()
    nm = RP.named_classes(A)
    Aex = emap = None
    if A.arm in ('pure', 'sample', 'matched', 'exact'):
        Aex = RP.get_arm('exact', A.n, A.D, A.mu_kind)
        emap = RP.embed_classes(A, Aex)
    res = dict(arm=A.arm, N=N, D=A.D, mu_kind=A.mu_kind, twins=twins, K=K, log10_theta=log_theta / math.log(10),
               n_candidates=len(cands), n_seeded=len(seeds), n_center=n_center, closure_nodes=n1, closure_complete=bool(comp1),
               n_expanded=len(ch.trans), n_recurrent=len(keys), closed=info,
               log10_cut=float(ch.log_cut / math.log(10)) if np.isfinite(ch.log_cut) else None, n_cand_left=int(ch.n_cand_left),
               n_twin_moves=int(ch.n_twin_moves), underflow=int(ch.underflow))
    # per-state statistics
    agg = defaultdict(float)
    states = []
    for k, p in zip(keys, pi):
        ids, x, kind = ch.states[k]
        st = RP.state_stats(A, ids, x, nm, Aex, emap)
        for kk, v in st.items():
            if isinstance(v, (int, float)) and not (isinstance(v, float) and math.isnan(v)) and kk not in ('e_prog_arg',):
                agg[kk] += p * v
        states.append((p, ids, x, st))
    res['pi_stat'] = dict(agg)
    res['pi_mass_X'] = agg.get('share_X', 0.0)
    # indeterminate (three-type cycle) events: weight by pi and by prior mass of the mutant
    indet = defaultdict(float); indet_n = defaultdict(int)
    key_pi = dict(zip(keys, pi))
    for (key, q, traj) in ch.indeterminate:
        if key in key_pi:
            sup = tuple(A.names[c] for c in sorted(set(int(c) for c in traj[0][0]))) if traj else ()
            indet[sup] += key_pi[key] * mu[q]; indet_n[sup] += 1
    res['indeterminate_total_events'] = len(ch.indeterminate)
    res['indeterminate_pi_weighted_mutation_mass'] = float(sum(indet.values()))
    res['indeterminate_top'] = [dict(support=list(k)[:6], mass=float(v), events=indet_n[k]) for k, v in sorted(indet.items(), key=lambda kv: -kv[1])[:5]]
    # support: top states
    order = np.argsort(-pi)
    top = []
    for i in order[:12]:
        p, ids, x, st = states[i]
        top.append(dict(pi=float(p), state=state_name(A, ids, x), n_classes=len(ids), e_prog=st['e_prog'], e_act=st['e_act'],
                        mix_pop=st['mix_pop'], forfeit_self=st['forfeit_self'], forfeit_plays=st['forfeit_plays']))
    res['top_states'] = top
    cum = np.cumsum(pi[order])
    res['n_states_for_0.99'] = int(np.searchsorted(cum, 0.99) + 1)
    res['n_states_pi_gt_1e-6'] = int((pi > 1e-6).sum())
    # classes carrying mass: pi-weighted class share
    cls_share = np.zeros(K)
    for p, ids, x, st in states:
        cls_share[list(ids)] += p * np.asarray(x)
    o = np.argsort(-cls_share)
    res['class_share_all'] = [(A.names[c], float(cls_share[c])) for c in o if cls_share[c] > 0]
    res['class_share_top'] = [(A.names[c], float(cls_share[c]), int(A.lang.size[A.rep[c]])) for c in o[:15]]
    res['class_share_cum'] = float(cls_share.sum())
    # transition structure: top exits of the top 3 states (log10 per-event rates) and mutants responsible
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
                ex.append(dict(to=state_name(A, ids, x, 4), log10_rate=float(row[j] / math.log(10)),
                               mutants=[(A.names[int(q)], float(v / math.log(10))) for q, v in muts]))
            ids, x, _ = ch.states[keys[ti]]
            exits.append(dict(state=state_name(A, ids, x, 4), pi=float(pi[ti]), log10_total_exit=tot, top_exits=ex))
        res['top_exits'] = exits
    except Exception as e:      # pragma: no cover
        res['top_exits_error'] = repr(e)
    # pi equivariance under the cyclic relabeling (Prediction 2)
    if A.arm not in BENCH:
        res['pi_equivariance'] = pi_equivariance(A, ch, keys, pi, N)
    res['time_s'] = time.time() - t0
    res['_chain'] = ch if False else None
    return res, (ch, keys, pi, states)


def canon_state(ids, x, N, perm=None):
    cnt = np.rint(np.asarray(x) * N).astype(int)
    ii = [int(perm[i]) if perm is not None else int(i) for i in ids]
    return tuple(sorted(zip(ii, cnt.tolist())))


def pi_equivariance(A, ch, keys, pi, N):
    out = {}
    sig_cache = A.lang.relabel_map(1)
    perm = RP.class_perm(A, sig_cache)
    d = {}
    for k, p in zip(keys, pi):
        ids, x, kind = ch.states[k]
        d[canon_state(ids, x, N)] = d.get(canon_state(ids, x, N), 0.0) + p
    worst = 0.0; missing = 0.0
    for k, p in zip(keys, pi):
        ids, x, kind = ch.states[k]
        s2 = canon_state(ids, x, N, perm)
        q = d.get(s2)
        if q is None:
            missing += p; worst = max(worst, p)
        else:
            worst = max(worst, abs(p - q))
    out['max_abs_pi_diff'] = float(worst)
    out['pi_mass_of_states_without_image'] = float(missing)
    return out


def cmd_chain(a):
    D = a.D
    A = RP.get_arm(a.arm, a.n, D, a.mu)
    t0 = time.time()
    res, _ = chain_cell(A, a.N, log_theta=a.log10theta * math.log(10), twins=bool(a.twins), verbose=a.verbose)
    res.pop('_chain', None)
    tag = '%s_D%d_N%d%s%s%s%s' % (a.arm, D, a.N, '' if a.n == 6 else '_n%d' % a.n, '' if a.mu == 'bits' else '_mu' + a.mu, '' if a.twins else '_lumped',
                                ('_th%d' % round(-a.log10theta)) if abs(a.log10theta + 14) > 1e-9 else '')
    jdump(res, os.path.join(OUT, 'chain_%s.json' % tag))
    st = res['pi_stat']
    print('%s: K=%d recurrent=%d expanded=%d  e_prog=%.4f e_act=%.4f mix_pop=%.3f forfeit_self=%.3f consts=%.3f X=%.3f (%.0fs)' % (
        tag, res['K'], res['n_recurrent'], res['n_expanded'], st['e_prog'], st['e_act'], st['mix_pop'], st['forfeit_self'],
        st.get('share_consts', 0), st.get('share_X', 0), time.time() - t0), flush=True)


# ================================================================ toy chain (eleven classes)
def cmd_toy(a):
    out = {}
    names = ['R', 'P', 'S', 'X', 'TM', 'N', 'N2', 'C', 'GN', 'GC', 'M']
    for D in (11, 12, 13, 20):
        A = RP.get_arm('exact', 6, D)
        nm = RP.named_classes(A)
        idx = [nm[k] for k in names]
        U = A.U[np.ix_(idx, idx)]
        # the toy class table: classes that coincide in payoff are kept distinct (a list of programs, uniform prior)
        mu = np.ones(len(idx)) / len(idx)
        for N in (100, 1000, 10000):
            prov = RP.ClassProvider(U, mu)
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
                top.append(dict(pi=float(pi[i]), state=' + '.join('%s:%.3f' % (names[c], xi) for c, xi in zip(ids, x))))
            # mass on states whose support lies in {X, GN, GC}
            gset = {names.index(k) for k in ('X', 'GN', 'GC')}
            m_gset = float(sum(p for k, p in zip(keys, pi) if set(ch.states[k][0]) <= gset))
            out['D%d_N%d' % (D, N)] = dict(D=D, N=N, n_states=len(keys), mass_on_XGNGC=m_gset, class_share={k: float(v) for k, v in share.items()},
                                           top=top, gap_TM_GN=float(U[names.index('TM'), names.index('GN')]),
                                           indeterminate=len(ch.indeterminate), closed=info)
            print('toy D=%d N=%d: mass on {X,GN,GC} %.4f  states %d  indeterminate %d  top: %s' % (
                D, N, m_gset, len(keys), len(ch.indeterminate), top[0]['state']), flush=True)
    jdump(out, os.path.join(OUT, 'toy.json'))


# ================================================================ static numbers and validation
def cmd_static(a):
    out = {}
    nm_cache = {}
    for arm in ARM_LIST + SENS + BENCH:
        t0 = time.time()
        A = RP.build_arm(arm, 6, 12, sweep=(11, 13, 20))
        RP.get_arm(arm, 6, 12)        # populate the class cache
        rec = dict(arm=arm, S=int(A.lang.S), counts=[int(c) for c in A.lang.counts[1:]], K=int(A.K), K_dec5=int(A.K_dec5),
                   antisym_err=A.antisym_err, diag_err=A.diag_err, mean_forfeit_mass_over_pairs=A.G_full_forfeit_mass,
                   member_dist_dev=A.member_dist_dev, n_classes_dist_split=int(A.n_classes_dist_split),
                   mass_of_top5_classes=[(A.names[c], float(A.mass[c])) for c in range(min(5, A.K))])
        if A.lang.S > 3 and arm not in ('constants', 'constx'):
            errs = {}
            for shift in (1, 2):
                err, sig = RP.symmetry_errors(A, shift)
                errs['shift%d' % shift] = err
            rec['symmetry_err_U'] = errs
            # sensitivity of the payoff table to the cap: sweep at program level
            sw = {}
            rng = np.random.default_rng(11)
            pairs = rng.integers(A.lang.S, size=(1000, 2))
            for d, Ud in A.sweep_U.items():
                diff = np.abs(Ud - A.U_full)
                sw[str(d)] = dict(max_abs_diff_all_pairs=float(diff.max()), frac_pairs_diff_gt_1e3=float((diff > 1e-3).mean()),
                                  frac_pairs_diff_gt_1e9=float((diff > 1e-9).mean()),
                                  sampled1000_max=float(np.abs(Ud[pairs[:, 0], pairs[:, 1]] - A.U_full[pairs[:, 0], pairs[:, 1]]).max()),
                                  sampled1000_frac_gt_1e9=float((np.abs(Ud[pairs[:, 0], pairs[:, 1]] - A.U_full[pairs[:, 0], pairs[:, 1]]) > 1e-9).mean()),
                                  sign_flips_frac=float((np.sign(np.round(Ud, 9)) != np.sign(np.round(A.U_full, 9))).mean()))
            rec['depth_sweep_program_level'] = sw
        # predictions 1 statics (sample and exact arms: all programs; stated for X and C and N)
        if arm in ('sample', 'exact', 'matched', 'exact_br', 'exact_uniform'):
            L = A.lang
            Ux = A.U_full
            G, Gp, _ = RP.evaluate(L, 12)
            xid = L.find('X')
            forf = G[:, xid, 3]
            nonforf = forf < 1e-12
            rec['pred1_X_nonforfeit_programs'] = int(nonforf.sum())
            rec['pred1_X_max_abs_payoff_nonforfeit'] = float(np.abs(Ux[nonforf, xid]).max())
            rec['pred1_X_forfeiting_programs'] = int((~nonforf).sum())
            rec['pred1_X_payoff_equals_minus_forfeit_mass'] = float(np.abs(Ux[:, xid] + forf).max())
            if arm in ('exact', 'matched', 'exact_br', 'exact_uniform'):
                cid = L.find('cr(THEM(ME))') if arm != 'matched' else L.find('next2(THEM(ME))')
                rec['pred1_C_self_forfeit_mass'] = float(G[cid, cid, 3])
            nid = L.find('next(THEM(ME))')
            det = [b for b in range(L.S) if G[b, nid, :3].max() > 1 - 1e-12 and G[b, nid, 3] < 1e-12]
            bad = [b for b in det if abs(Ux[nid, b] - 1.0) > 1e-9]
            rec['pred1_N_deterministic_opponents'] = len(det)
            rec['pred1_N_counterexamples'] = len(bad)
            rec['pred1_N_counterexample_examples'] = [(L.src(b), float(Ux[nid, b])) for b in bad[:8]]
            consts = [L.find(c) for c in 'RPS']
            rec['pred1_N_beats_constants'] = [float(Ux[nid, c]) for c in consts]
            del G, Gp
        out[arm] = rec
        print('static %s: S=%d K=%d (%.1fs)' % (arm, A.lang.S, A.K, time.time() - t0), flush=True)
        del A
    jdump(out, os.path.join(OUT, 'static.json'))


# ================================================================ depth sweep and inferred-versus-actual reads
def cmd_sweep(a):
    out = {}
    for arm in ARM_LIST:
        A = RP.get_arm(arm, 6, 12)
        L = A.lang
        names = set()
        nm = RP.named_classes(A)
        for k, c in nm.items():
            names.add(A.names[c])
        wchain = {}
        for N in NS_CHAIN:
            r = jload(os.path.join(OUT, 'chain_%s_D12_N%d.json' % (arm, N)))
            cum = 0.0
            for nme, sh in r['class_share_all']:
                if cum >= 0.99: break
                names.add(nme); cum += sh
            if N == 10000:
                wchain = {nme: sh for nme, sh in r['class_share_all']}
        # classes holding 0.99 of the pooled lottery mass (primary cell, horizon 2000)
        p = os.path.join(OUT, 'lottery_%s_primary.jsonl.gz' % arm)
        lot_names = []
        if os.path.exists(p):
            tot = np.zeros(A.K)
            for l in gzip.open(p, 'rt'):
                rec = json.loads(l)
                for isl in rec['comp']['2000']:
                    for k, n in isl: tot[k] += n
            tot /= tot.sum(); cum = 0.0
            for k in np.argsort(-tot):
                if cum >= 0.99: break
                names.add(A.names[k]); lot_names.append(A.names[k]); cum += tot[k]
        names = sorted(names)
        P = np.array([L.find(nme) for nme in names])
        rngp = np.random.default_rng(11)
        pairs = rngp.integers(L.S, size=(1000, 2))
        res = dict(n_classes_in_set=len(names), n_chain_set=len([n for n in names if n in wchain]), n_lottery_set=len(lot_names))
        blocks = {}
        for D in SWEEP_D:
            G, _, Us = RP.evaluate(L, D, keep_prev=False)
            U = Us[D]
            blocks[D] = dict(U=U[np.ix_(P, P)].copy(), F=G[np.ix_(P, P)][:, :, 3].copy(),
                             pu=U[pairs[:, 0], pairs[:, 1]].copy(), pf=G[pairs[:, 0], pairs[:, 1], 3].copy())
            del G, U, Us
        base = blocks[12]
        res['by_D'] = {}
        for D in SWEEP_D:
            if D == 12: continue
            b = blocks[D]
            d = np.abs(b['U'] - base['U'])
            sgn = np.sign(np.round(b['U'], 9)) != np.sign(np.round(base['U'], 9))
            dp = np.abs(b['pu'] - base['pu'])
            res['by_D'][str(D)] = dict(
                set_max_abs_payoff_diff=float(d.max()), set_pairs_diff_gt_1e9=int((d > 1e-9).sum()), set_pairs=int(d.size),
                set_sign_flips=int(sgn.sum()), set_max_forfeit_mass_diff=float(np.abs(b['F'] - base['F']).max()),
                sampled_max_abs_payoff_diff=float(dp.max()), sampled_pairs_diff_gt_1e9=int((dp > 1e-9).sum()),
                sampled_sign_flips=int((np.sign(np.round(b['pu'], 9)) != np.sign(np.round(base['pu'], 9))).sum()),
                sampled_max_forfeit_mass_diff=float(np.abs(b['pf'] - base['pf']).max()))
        res['forfeit_mass_D12_set_mean'] = float(base['F'].mean())
        res['forfeit_mass_D12_set_max_offdiag'] = float((base['F'] - np.diag(np.diag(base['F']))).max())
        # (L): pi-weighted share of ordered pairs of distinct chain-support classes whose payoff sign differs across D
        if wchain:
            idxs = [i for i, nme in enumerate(names) if nme in wchain]
            w = np.array([wchain[names[i]] for i in idxs])
            flip = np.zeros((len(idxs), len(idxs)), bool)
            for D in SWEEP_D:
                if D == 12: continue
                s1 = np.sign(np.round(blocks[D]['U'][np.ix_(idxs, idxs)], 9)); s0 = np.sign(np.round(base['U'][np.ix_(idxs, idxs)], 9))
                flip |= (s1 != s0)
            W2 = np.outer(w, w); np.fill_diagonal(W2, 0.0)
            res['pi_weighted_pair_sign_flip_fraction_N1e4'] = float((W2 * flip).sum() / W2.sum())
            # (N): readers (programs containing an application) in the chain support: all mutual payoffs zero at D = 12?
            rd = [i for i in idxs if (L.t_op[P[i], :L.t_len[P[i]]] == RP.OP_APP).any()]
            sub = base['U'][np.ix_(rd, rd)]
            res['n_reader_classes_in_support'] = len(rd)
            res['readers_mutual_max_abs_payoff_D12'] = float(np.abs(sub).max()) if len(rd) else 0.0
            res['readers_pairs_nonzero_payoff_D12'] = int((np.abs(sub) > 1e-9).sum()) // 2 if len(rd) else 0
            res['constants_pi_mass_N1e4'] = float(sum(wchain.get(n, 0.0) for n in ('R', 'P', 'S')))
        # inferred versus actual: pairs (a, b) where a reads `THEM(ME)`: a's inferred b-action is G_{D-1}(b, a), actual G_D(b, a)
        ia = []
        cl = [A.names.index(nme) for nme in names]
        for i, ca in enumerate(cl):
            if not L.reads_me[A.rep[ca]]: continue
            for j, cb in enumerate(cl):
                inf = A.Gcl_prev[cb, ca]; act = A.Gcl[cb, ca]
                ia.append((names[i], names[j], float(0.5 * np.abs(inf - act).sum())))
        if ia:
            tvs = np.array([t[2] for t in ia])
            res['inferred_vs_actual'] = dict(n_pairs=len(ia), max_tv=float(tvs.max()), mean_tv=float(tvs.mean()), n_gt_1e9=int((tvs > 1e-9).sum()),
                                             worst=sorted(ia, key=lambda t: -t[2])[:8])
        named_rows = []
        for ka in ('TM', 'N', 'C', 'GN', 'GC'):
            if ka not in nm: continue
            for kb in ('R', 'X', 'TM', 'N', 'C', 'GN', 'GC', 'M'):
                if kb not in nm: continue
                inf = A.Gcl_prev[nm[kb], nm[ka]]; act = A.Gcl[nm[kb], nm[ka]]
                named_rows.append(dict(reader=ka, opponent=kb, inferred=[float(v) for v in inf], actual=[float(v) for v in act]))
        res['named_inferred_vs_actual'] = named_rows
        out[arm] = res
        print('sweep %s: set of %d classes; %s' % (arm, len(names), {D: res['by_D'][str(D)]['set_sign_flips'] for D in SWEEP_D if D != 12}), flush=True)
    jdump(out, os.path.join(OUT, 'sweep.json'))


# ================================================================ the lottery
CELLS = {
    'primary': dict(N=100, I=64, runs=40, horizon=2000, cont_runs=10, cont_horizon=10000),
    'size': dict(N=400, I=16, runs=20, horizon=2000, cont_runs=0, cont_horizon=2000),
    'primary200': dict(N=100, I=64, runs=200, horizon=2000, cont_runs=0, cont_horizon=2000),     # supplementary replicate
}
CPS_BASE = [100, 250, 500, 1000, 1500, 2000]


def one_run(A, cell, r, mN=1.0, tag=''):
    c = CELLS[cell]
    N, I = c['N'], c['I']
    horizon = c['cont_horizon'] if r < c['cont_runs'] else c['horizon']
    cps = [g for g in CPS_BASE if g <= horizon]
    if horizon > 2000:
        cps += [5000, 10000]
    cps = np.array(sorted(set(cps)), np.int64)
    seed_f = RP.run_seed('founders|%s' % cell, r)               # shared by arms: common random numbers
    init = RP.draw_founders(A.lang, A.cls_of, A.K, I, N, seed_f)
    idx, init_l = RP.compress_run(init)
    Ul = np.ascontiguousarray(A.U[np.ix_(idx, idx)])
    seed_d = RP.run_seed('dynamics|%s|%s' % (cell, A.arm), r)
    t0 = time.time()
    out, nalive, homo, nwin = RP.lottery_kernel(Ul, init_l, N, RP.W, mN / N, seed_d, cps, 1500, 2000, 10)
    wall = time.time() - t0
    nm = RP.named_classes(A)
    rec = dict(arm=A.arm, cell=cell, run=r, N=N, I=I, K_start=int(len(idx)), founder_classes=int(len(idx)), wall=wall,
               horizon=int(horizon), cps=[int(g) for g in cps], nwin=int(nwin),
               nalive_window=(nalive / max(nwin, 1)).tolist(), homo_window=(homo / max(nwin, 1)).tolist(), stats={})
    for ci, g in enumerate(cps):
        full = np.zeros((I, A.K), np.int64)
        full[:, idx] = out[ci]
        st = RP.island_stats(A, full, N, nm)
        rec['stats'][str(int(g))] = {k: np.round(v, 6).tolist() for k, v in st.items()}
        if g in (500, 2000, int(cps[-1])):
            # sparse island compositions (class id, count) for support/transition reports
            comp = []
            for i in range(I):
                nz = np.nonzero(full[i])[0]
                comp.append([(int(k), int(full[i, k])) for k in nz])
            rec.setdefault('comp', {})[str(int(g))] = comp
    rec['founder_mass_X'] = float(init[:, nm['X']].sum() / (I * N)) if 'X' in nm else 0.0
    return rec


def cmd_build(a):
    t0 = time.time()
    A = RP.get_arm(a.arm, a.n, 12)
    print('built %s n=%d: S=%d K=%d (%.0fs) antisym %.2e' % (a.arm, a.n, A.lang.S, A.K, time.time() - t0, A.antisym_err), flush=True)


def cmd_lottery(a):
    A = RP.get_arm(a.arm, a.n, 12)
    cell = a.cell
    c = CELLS[cell]
    r0, r1 = (a.runs if a.runs else (0, c['runs']))
    path = os.path.join(OUT, 'lottery_%s_%s%s.jsonl.gz' % (a.arm, cell, '' if a.n == 6 else '_n%d' % a.n))
    done = set()
    rows = []
    if os.path.exists(path):
        rows = [json.loads(l) for l in gzip.open(path, 'rt')]
        done = {r['run'] for r in rows}
    t0 = time.time()
    for r in range(r0, r1):
        if r in done:
            continue
        rec = one_run(A, cell, r)
        rows.append(rec)
        with gzip.open(path + '.tmp', 'wt') as f:
            for x in rows: f.write(json.dumps(x) + '\n')
        os.replace(path + '.tmp', path)
        s = rec['stats'][str(rec['cps'][-1] if rec['horizon'] <= 2000 else 2000)]
        print('lottery %s %s run %d: %.0fs  e_prog %.3f mix %.3f forfeit %.3f nclass %.2f' % (
            a.arm, cell, r, rec['wall'], np.mean(s['e_prog']), np.mean(s['mix_pop']), np.mean(s['forfeit_plays']), np.mean(s['nclass'])), flush=True)
    print('done %s %s (%.0fs)' % (a.arm, cell, time.time() - t0), flush=True)


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd')
    sp.add_parser('static'); sp.add_parser('toy'); sp.add_parser('sweep')
    b7 = sp.add_parser('build'); b7.add_argument('arm'); b7.add_argument('--n', type=int, default=7)
    c = sp.add_parser('chain'); c.add_argument('arm'); c.add_argument('N', type=int)
    c.add_argument('--D', type=int, default=12); c.add_argument('--n', type=int, default=6); c.add_argument('--mu', default='bits'); c.add_argument('--twins', type=int, default=1)
    c.add_argument('--log10theta', type=float, default=-14.0)
    c.add_argument('--verbose', action='store_true')
    l = sp.add_parser('lottery'); l.add_argument('--n', type=int, default=6); l.add_argument('arm'); l.add_argument('cell'); l.add_argument('--runs', type=int, nargs=2)
    a = ap.parse_args()
    {'static': cmd_static, 'toy': cmd_toy, 'sweep': cmd_sweep, 'build': cmd_build, 'chain': cmd_chain, 'lottery': cmd_lottery}[a.cmd](a)


if __name__ == '__main__':
    main()
