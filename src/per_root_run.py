"""Driver for the per-root run (notes/per-root.md).

  python3 src/per_root_run.py jobs --jobs 'R2_i:0-19,R1_i:0-19' --procs 3            # one job per process
  python3 src/per_root_run.py compare --cell R0_i --parent Ni                          # draw for draw vs stored runs
  python3 src/per_root_run.py static                                                   # reach and validity covers
  python3 src/per_root_run.py traces                                                   # fixed encounter traces
  python3 src/per_root_run.py audit                                                    # realizability (term level)
  python3 src/per_root_run.py replays --cell R2_i --runs 5 --procs 3                   # mediation replays
"""
import os
import sys
import json
import time
import argparse
import itertools
from collections import defaultdict, Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sog_full as F
import sog_full_run as R
import coverage_components as CC
import per_root as PR

OUT = PR.OUT
STORED_FL = os.path.join(PR.ROOT, 'runs', 'founding_legibility')
STORED_CC = os.path.join(PR.ROOT, 'runs', 'coverage_components')


def parse_jobs(spec, extend):
    jl = []
    for item in spec.split(','):
        item = item.strip()
        if not item: continue
        parts = item.split(':')
        nm, rr = parts[0], parts[1]
        ext = int(parts[2]) if len(parts) > 2 else extend
        lo, hi = (int(z) for z in rr.split('-')) if '-' in rr else (int(rr), int(rr))
        for rep in range(lo, hi + 1):
            if not os.path.exists(os.path.join(OUT, 'cell_' + nm, 'rep_%03d.json' % rep)):
                jl.append((nm, rep, ext))
    return jl


def run_pool(jl, procs):
    from multiprocessing import get_context
    print('jobs', len(jl), [j[:2] for j in jl][:200], time.strftime('%H:%M:%S'), flush=True)
    if not jl: return
    with get_context('fork').Pool(min(procs, 3), maxtasksperchild=1) as pool:
        for nm, rep, tm in pool.imap_unordered(PR.cell_job, jl, chunksize=1):
            print(nm, rep, json.dumps({k: round(v, 1) for k, v in tm.items()}), time.strftime('%H:%M:%S'),
                  flush=True)


def jobs(args):
    run_pool(parse_jobs(args.jobs, args.extend), args.procs)


SKIP = {'fills', 'ntypes', 'time', 'ctr'}


def diff(a, b, path=''):
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in set(a) | set(b):
            if k in SKIP: continue
            if k not in a or k not in b:
                out.append(path + '/' + str(k) + ' (missing)'); continue
            out += diff(a[k], b[k], path + '/' + str(k))
        return out
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): return [path + ' (len)']
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out += diff(x, y, path + '[%d]' % i)
        return out
    return [] if a == b else [path]


def compare(args):
    """Every summary field of this run's cell against the stored parent cell, replicate by replicate (counters,
    fills and times excluded; the mark changes counters only)."""
    res = []
    d = os.path.join(OUT, 'cell_' + args.cell)
    src = STORED_FL if args.parent in ('Ni', 'N3', 'N6', 'Heq_i') else STORED_CC
    for f in sorted(os.listdir(d)):
        if not f.endswith('.json') or '.tmp' in f: continue
        a = json.load(open(os.path.join(d, f)))
        pf = os.path.join(src, 'cell_' + args.parent, f)
        if not os.path.exists(pf): continue
        b = json.load(open(pf))
        sa, sb = dict(a['summary']), dict(b['summary'])
        dd = diff(sa, sb) + diff({k: v for k, v in a.get('summary_ext', {}).items() if k != 'ctr'},
                                 {k: v for k, v in b.get('summary_ext', {}).items() if k != 'ctr'}, '/ext')
        dd = [p for p in dd if 'fair_mask_end' not in p]
        res.append(dict(rep=a['rep'], identical=not dd, n_diff=len(dd), first=dd[:8],
                        fair_2000=(a['summary']['h']['persistence'], b['summary']['h']['persistence']),
                        fair_end=(a['summary_ext']['end']['persistence'], b['summary_ext']['end']['persistence'])))
        print(json.dumps(res[-1]), flush=True)
    f = os.path.join(PR.ROOT, 'runs', 'per-root-validate.json')
    old = json.load(open(f)) if os.path.exists(f) else {}
    old['%s_vs_%s' % (args.cell, args.parent)] = res
    json.dump(old, open(f, 'w'), indent=1)


# ----------------------------------------------------------------------------------------------------------------
# static reach and validity covers (notes §1.1)
# ----------------------------------------------------------------------------------------------------------------
def support_trees(role, reps):
    """{run tree: founder count} over the founders of the given replicates at (100, 64)."""
    g = G()
    r = g.roles[role]
    cum = np.cumsum(g.mass(role))
    out = Counter()
    for rep in reps:
        rng = np.random.default_rng([rep, 100, 64, 20261013])
        uB = rng.random((64, 100)); u1 = rng.random((64, 100)); u2 = rng.random((64, 100))
        for u in ((uB,) if role == 'B' else (u1, u2)):
            sps = np.minimum(np.searchsorted(cum, u * cum[-1]), len(cum) - 1).ravel()
            for s in sps: out[int(r['tau'][s])] += 1
    return out


def roots_of(role, t):
    ats = [a for a in F.dt_atoms(t) if a[0] != 'E']
    if role == 'W':
        idvs = [lambda nm: False]
    else:
        idvs = [(lambda d: (lambda nm: d.get(nm, False)))(dict(zip(('N1', 'N2', 'EQW'), c))) for c in F.BOSS_ID_COMBOS]
    out = []
    for idv in idvs:
        for vb in itertools.product('TF', repeat=len(ats)):
            out.append((idv, dict(zip(ats, vb))))
    return out


def eff_valid(t, role, A, s, idv, val):
    """Valid at the root with every Hyp read as its box's root value (the closure approximated by the root)."""
    u, _ = F.sym_check(t, role, A, s, idv, lambda a: val[a])
    if u is None: return False
    return all(val.get(a) == 'T' for a in u)


def min_cover(sets_by_cand, need):
    """Fewest candidates whose sets cover `need` (brute force up to 5, else greedy, flagged)."""
    cands = [c for c in sets_by_cand if sets_by_cand[c] & need]
    if not need: return 0, True
    for k in range(1, min(5, len(cands)) + 1):
        for comb in itertools.combinations(cands, k):
            u = set()
            for c in comb: u |= sets_by_cand[c]
            if need <= u: return k, True
    left = set(need); n = 0
    while left:
        c = max(cands, key=lambda c: len(sets_by_cand[c] & left)); left -= sets_by_cand[c]; n += 1
    return n, False


def static_tree(role, tk):
    g = G()
    t = g.roles[role]['dts'][tk]
    _, per = g.hlist(role, tk)
    cls = CC.classify(g, role, tk)
    roots = roots_of(role, t)
    rows = {}
    for A in F.FAM[role]:
        S3, ALT = set(), set()
        bundles = []
        for idv, val in roots:
            bv = lambda a: val[a]
            if role == 'W':
                sc, sa, _ = PR.sym_prod3_alt(t, 'W', A, idv, bv)
            else:
                sc, _ = F.sym_prod3(t, role, A, idv, bv); sa = None
            if sc is not None:
                S3.add(per[A].index(sc))
                b = (per[A].index(sc),) + ((per[A].index(sa),) if sa is not None else ())
                bundles.append(b)
            if sa is not None: ALT.add(per[A].index(sa))
        cand = S3 | ALT
        rv = {c: set() for c in cand}; ev_ = {c: set() for c in cand}
        for q, (idv, val) in enumerate(roots):
            for c in cand:
                s = per[A][c]
                u, _ = F.sym_check(t, role, A, s, idv, lambda a: val[a])
                if u is not None: rv[c].add(q)
                if eff_valid(t, role, A, s, idv, val): ev_[c].add(q)
        def cov(sets, cands):
            sb = {c: sets[c] for c in cands}
            need = set().union(*sb.values()) if sb else set()
            return min_cover(sb, need)
        bsets_rv = {b: set().union(*(rv[c] for c in b)) for b in set(bundles)}
        bsets_ev = {b: set().union(*(ev_[c] for c in b)) for b in set(bundles)}
        rows[A] = dict(labels=[r['label'] for r in cls[A]], S3=sorted(S3), ALT=sorted(ALT),
                       cover_root_R1=cov(rv, S3), cover_eff_R1=cov(ev_, S3),
                       cover_root_R2=cov(rv, cand), cover_eff_R2=cov(ev_, cand),
                       bundle_cover_root=min_cover(bsets_rv, set().union(*bsets_rv.values()) if bsets_rv else set()),
                       bundle_cover_eff=min_cover(bsets_ev, set().union(*bsets_ev.values()) if bsets_ev else set()),
                       n=len(per[A]))
    return rows


def static(args):
    g = G()
    out = {}
    t0 = time.time()
    for role in ('W', 'B'):
        if role == 'W':
            m = g.mass('W')
            wt = Counter()
            for sp, tk in enumerate(g.roles['W']['tau']): wt[int(tk)] += m[sp]
            trees = list(range(len(g.roles['W']['dts'])))
            fw = support_trees('W', range(20))
        else:
            fw = support_trees('B', range(20))
            trees = sorted(fw)
            wt = Counter({tk: c / sum(fw.values()) for tk, c in fw.items()})
        reach = defaultdict(float); tot = defaultdict(float)
        covers = defaultdict(lambda: defaultdict(float))
        exact = True
        for tk in trees:
            rows = static_tree(role, tk)
            w = wt[tk]
            for A, r in rows.items():
                for i, lab in enumerate(r['labels']):
                    k = lab + (':S3' if i in r['S3'] else ':notS3')
                    tot[k] += w
                    if i in r['S3']: reach[('R1', k)] += w
                    if i in r['S3'] or i in r['ALT']: reach[('R2', k)] += w
                for kk in ('cover_root_R1', 'cover_eff_R1', 'cover_root_R2', 'cover_eff_R2', 'bundle_cover_root',
                           'bundle_cover_eff'):
                    n_, ex = r[kk]
                    exact &= ex
                    covers[kk][min(n_, 5)] += w
        nset = len(F.FAM[role])
        out[role] = dict(
            scripts_per_program={k: round(v, 4) for k, v in sorted(tot.items())},
            reach={rule: {k: round(reach[(rule, k)] / tot[k], 4) for k in sorted(tot)} for rule in ('R1', 'R2')},
            covers={kk: {str(n_): round(v / (sum(d.values()) or 1), 4) for n_, v in sorted(d.items())}
                    for kk, d in covers.items()},
            covers_exact=exact, trees=len(trees), weight='prior' if role == 'W' else 'founders 0-19')
        print(role, json.dumps(out[role]), '%.0fs' % (time.time() - t0), flush=True)
    f = os.path.join(PR.ROOT, 'runs', 'per-root-static.json')
    json.dump(out, open(f, 'w'), indent=1)


# ----------------------------------------------------------------------------------------------------------------
# mediation replays (notes §1.0 item 11, as amended in §1.x)
# ----------------------------------------------------------------------------------------------------------------
def replay_jobs(cell, nmax=5, per_script=0, reps=range(20)):
    """For up to nmax regrowing development runs of a cell: one replay barring every second-path pivotal script
    ('perroot' or 'alt') of the run's first nucleus; and, for the first per_script runs, one replay per such script."""
    jl = []
    d = os.path.join(OUT, 'cell_' + cell)
    n = 0
    for rep in reps:
        f = os.path.join(d, 'rep_%03d.json' % rep)
        if not os.path.exists(f): continue
        nu = json.load(open(f))['pr']['nuclei']
        if not nu.get('regrows') or not nu['nuclei']: continue
        piv = [p for p in nu['nuclei'][0].get('pivotal', []) if p['prov'] in ('perroot', 'alt')]
        if not piv: continue
        bars = sorted(set((p['role'], p['tk'], p['set'], p['idx']) for p in piv))
        jl.append((cell, rep, 10000, [list(b) for b in bars], '%s_bar_all' % cell))
        if n < per_script:
            for k, b in enumerate(bars[:3]):
                jl.append((cell, rep, 10000, [list(b)], '%s_bar_%d' % (cell, k)))
        n += 1
        if n >= nmax: break
    return jl


def replays(args):
    jl = []
    for cell in args.cell.split(','):
        jl += replay_jobs(cell, args.runs, per_script=args.per_script)
    jl = [j for j in jl if not os.path.exists(os.path.join(OUT, 'cell_' + j[4], 'rep_%03d.json' % j[1]))]
    run_pool(jl, args.procs)


# ----------------------------------------------------------------------------------------------------------------
# fixed encounter traces (notes §1.0 item 11)
# ----------------------------------------------------------------------------------------------------------------
def founders(rep, I=64, N=100):
    g = G()
    rng = np.random.default_rng([rep, N, I, 20261013])
    uB = rng.random((I, N)); u1 = rng.random((I, N)); u2 = rng.random((I, N))
    cumB = np.cumsum(g.mass('B')); cumW = np.cumsum(g.mass('W'))
    spB = np.minimum(np.searchsorted(cumB, uB * cumB[-1]), len(cumB) - 1)
    sp1 = np.minimum(np.searchsorted(cumW, u1 * cumW[-1]), len(cumW) - 1)
    sp2 = np.minimum(np.searchsorted(cumW, u2 * cumW[-1]), len(cumW) - 1)
    return spB, sp1, sp2


def shadowing(ev, pid, si, vpos, ctxroot):
    """At a validation whose first valid entry (vpos) carries a Hyp node: is a later entry of the set valid at the
    root with no Hyp node (an older primary shadowing a newer alternative)?"""
    pr = ev.reg[pid]
    t = ev.g.roles[pr.role]['dts'][pr.tk]
    A = F.FAM[pr.role][si]
    ents = [sc for A2, sc in pr.entries if A2 == A]
    idv, bv = ctxroot
    u, _ = F.sym_check(t, pr.role, A, ents[vpos], idv, bv)
    if not u: return False
    for sc in ents[vpos + 1:]:
        u2, _ = F.sym_check(t, pr.role, A, sc, idv, bv)
        if u2 == []: return True
    return False


def coverage_of(ev, pid):
    """Per CC component (canon, (a), (b) split by S3^static, (c), (d)): (held, total) H scripts of the program."""
    pr = ev.reg[pid]
    labs = CC.labels_of(ev.g, pr.role, pr.tk)
    s3 = PR.s3_static(ev.g, pr.role, pr.tk)
    out = defaultdict(lambda: [0, 0])
    for si, ls in enumerate(labs):
        for i, l in enumerate(ls):
            k = l + ('' if l in ('canon', 'c', 'd') else (':S3' if i in s3[si] else ':notS3'))
            out[k][1] += 1
            if i in pr.inv[si]: out[k][0] += 1
    return out


def traces(args):
    rules = args.cell.split(',') if args.cell else ['R0', 'R0alt', 'R1', 'R2', 'R3k2', 'R3k2f']
    Ks = (PR.KI, PR.K3)
    n_enc = args.runs if args.runs > 5 else 2000
    reps, islands = (0, 1, 2), (0, 1, 2, 3)
    out = {}
    t0 = time.time()
    for K in Ks:
        for rule in rules:
            ev = PR.evaluator(rule, K)
            st = Counter()
            cov = defaultdict(lambda: [0.0, 0.0])
            ncov = Counter()
            for rep in reps:
                spB, sp1, sp2 = founders(rep)
                for isl in islands:
                    B = [ev.reg.get('B', int(s), F.empty_inv('B')) for s in spB[isl]]
                    W1 = [ev.reg.get('W', int(s), F.empty_inv('W')) for s in sp1[isl]]
                    W2 = [ev.reg.get('W', int(s), F.empty_inv('W')) for s in sp2[isl]]
                    rng = np.random.default_rng([rep, isl, 20261016])
                    for e in range(n_enc):
                        kb, k1, k2 = (int(z) for z in rng.integers(0, len(B), 3))
                        trip = (B[kb], W1[k1], W2[k2])
                        tr = ev.triple(*trip)
                        prods = ev.productions_full(*trip, tr=tr)
                        for s, (pid, npid, recs) in enumerate(prods):
                            role = 'B' if s == 0 else 'W'
                            if recs and recs[0] == ('refused',):
                                st[role + ':refused'] += 1; continue
                            for r in recs:
                                st[role + ':' + r[0] + ':' + r[2]] += 1
                                if r[0] == 'prod' and r[2] == 'found' and r[5]: st[role + ':prod:alt_written'] += 1
                                if r[0] == 'val' and r[2] == 'valid':
                                    pr = ev.reg[pid]
                                    if pr.role == 'W':
                                        j = s
                                        oex = (tr['wex'][2], tr['wex'][3]) if j == 1 else (tr['wex'][0], tr['wex'][1])
                                        ctx = ev.worker_ctx(pid, j, tr['bex'], oex, bool(tr['rel']))
                                        bex = tr['bex']
                                        bv = (lambda bex, oex: (lambda a: bex[F.BOSS_Q.index(a[1])] if a[0] == 'B' else
                                                                (oex[0] if a[1] == F.A_WORK else oex[1])))(bex, oex)
                                        if shadowing(ev, pid, r[1], ctx[r[1]][3], (lambda nm: False, bv)):
                                            st['W:shadowing'] += 1
                            if npid != pid:
                                if s == 0: B[kb] = npid
                                elif s == 1: W1[k1] = npid
                                else: W2[k2] = npid
                    for role, L_ in (('B', B), ('W', W1 + W2)):
                        for pid in L_:
                            for k, (h, n) in coverage_of(ev, pid).items():
                                if n:
                                    cov[role + ':' + k][0] += h / n; cov[role + ':' + k][1] += 1
                            ncov[role] += 1
                            st[role + ':scripts'] += sum(len(z) for z in ev.reg[pid].inv)
            key = '%s@%s' % (rule, 'ideal' if K == PR.KI else '%.0e' % K)
            out[key] = dict(counts=dict(st), coverage={k: round(v[0] / v[1], 4) for k, v in sorted(cov.items())},
                            scripts_per_program={r_: round(st[r_ + ':scripts'] / ncov[r_], 3) for r_ in ncov},
                            encounters=len(reps) * len(islands) * n_enc)
            print(key, json.dumps(out[key]), '%.0fs' % (time.time() - t0), flush=True)
            ev.maybe_clear(0)
    f = os.path.join(PR.ROOT, 'runs', 'per-root-traces.json')
    json.dump(out, open(f, 'w'), indent=1)


# ----------------------------------------------------------------------------------------------------------------
# the realizability audit (notes §1.0 item 12)
# ----------------------------------------------------------------------------------------------------------------
def rand_ordered_inv(rng, role, sp, kmax=4):
    """A random acquisition-ordered list per set (R1-R3 shapes: several scripts, any order)."""
    tk = int(G().roles[role]['tau'][sp])
    _, per = G().hlist(role, tk)
    inv = []
    for A in F.FAM[role]:
        k = len(per[A])
        if k and rng.random() < 0.75:
            m = rng.randrange(1, min(k, kmax) + 1)
            inv.append(tuple(rng.sample(range(k), m)))
        else:
            inv.append(())
    return tuple(inv)


def G():
    return R.grammar('id')


def measure_prod3a(slot, prog, A, idctx, forced_atoms):
    import lt_code as L
    L.CACHE.clear()
    enc, j = F.worker_roles('W', slot, prog, idctx)
    boxes = {F.atom_box_arg(a, 'W', enc, j): v for a, v in forced_atoms.items()}
    F.force_boxes(boxes)
    prim, alt, steps, out = PR.term_prod3a(enc, j, A)
    return steps, out, prim, alt


def measure_selfval(role, slot, prog, A, idctx, forced_atoms):
    """The program's own root validation as code (SELFVAL = vone4 on its own box), nested boxes forced at zero cost:
    (own steps of the vone4 window, total steps of the SELFVAL call, valid)."""
    import lt_code as L
    L.CACHE.clear()
    enc, j = F.worker_roles(role, slot, prog, idctx)
    boxes = {F.atom_box_arg(a, role, enc, j): v for a, v in forced_atoms.items()}
    F.force_boxes(boxes)
    ad = F.mk_arg4(F.V_MAIN, enc, j, A, F.K_MAIN)
    tm = ('app', ('lib', L.LIBIDX['SELFVAL']), ad)
    with F.Probe() as pr:
        v, n = L.run_big(L.evaluate, tm, 10 ** 9)
    top = [w for w in pr.windows if w[0] == 'vone']
    w = top[0] if top else None
    return (w[2] - w[3]) if w else None, n, (v != 0)


def audit(args):
    import random
    import lt_code as L
    R.load_costc()
    comp, n_old = PR.build_audit_library()
    rng = random.Random(161)
    g = G()
    W = g.roles['W']
    cm = F.CostModel(g, F.live_of('eq'), {})
    out = {}
    # (a)-(b): PROD3A by the term against the symbolic PROD3A and against the cost model
    rows = []
    t0 = time.time()
    while len(rows) < args.runs:
        sp = rng.randrange(len(W['spellings']))
        x = W['spellings'][sp]
        t = F.dt(x)
        tk = int(W['tau'][sp])
        if not any(a[0] == 'O' for a in F.dt_atoms(t)) and rng.random() < 0.7:
            continue                          # oversample trees with co-worker boxes (where alternatives exist)
        inv = rand_ordered_inv(rng, 'W', sp)
        ents = F.inv_entries(g, 'W', tk, inv)
        prog = F.compile_program(x, 'W', F.list_data(ents))
        A = rng.choice(list(F.WORKER_Q))
        forced = {a: rng.choice('TF') for a in F.dt_atoms(t) if a[0] != 'E'}
        idc = {'EQ': False, 'copy': F.compile_program(x, 'W', 0)}
        slot = rng.choice((1, 2))
        steps, oc, prim, alt = measure_prod3a(slot, prog, A, idc, forced)
        s0, o0, sc0 = F.measure_prod('W', slot, prog, A, idc, forced)
        log = []
        sp_, sa_, calls = PR.sym_prod3_alt(t, 'W', A, lambda nm: False, lambda a: forced[a], log)
        log0 = []
        sp0, _ = F.sym_prod3(t, 'W', A, lambda nm: False, lambda a: forced[a], log0)
        ik = F.ident_key('W', t, lambda nm: False)
        tab, dcl = cm.ft_table('W', sp, slot, ik)
        lc = F.list_counts(ents)
        dl = (lc[0] - dcl[0], lc[2] - dcl[2])
        base, f = F.prod_features(log, tab, dl, A, 'W')
        base0, f0 = F.prod_features(log0, tab, dl, A, 'W')
        rows.append(dict(match_primary=(prim == sp_) or (oc != 'found' and sp_ is None),
                         match_alt=(alt == sa_), match_prod3=(sc0 == sp0) or (o0 != 'found' and sp0 is None),
                         has_alt=sa_ is not None, steps_a=steps, steps_0=s0,
                         model_0_on_prod3=F.prod_steps('W', base0, f0, sp0 is not None),
                         model_0_on_log=F.prod_steps('W', base, f, sp_ is not None),
                         base=base, f=f, found=sp_ is not None))
    out['prod3a'] = dict(n=len(rows), primary_match=sum(r['match_primary'] for r in rows),
                         alt_match=sum(r['match_alt'] for r in rows), prod3_match=sum(r['match_prod3'] for r in rows),
                         with_alt=sum(r['has_alt'] for r in rows), time=time.time() - t0)
    # the cost: PROD3 model on PROD3 (sanity), the PROD3 model on PROD3A's log, a refit for PROD3A
    e0 = np.array([abs(r['model_0_on_prod3'] - r['steps_0']) / max(r['steps_0'], 1) for r in rows])
    e1 = np.array([abs(r['model_0_on_log'] - r['steps_a']) / max(r['steps_a'], 1) for r in rows])
    out['prod3a']['rel_err_prod3_model_on_prod3'] = dict(median=float(np.median(e0)), p99=float(np.percentile(e0, 99)))
    out['prod3a']['rel_err_prod3_model_on_prod3a'] = dict(median=float(np.median(e1)), p99=float(np.percentile(e1, 99)))
    ratio = np.array([r['steps_a'] / max(r['steps_0'], 1) for r in rows])
    out['prod3a']['steps_ratio_prod3a_over_prod3'] = dict(median=float(np.median(ratio)),
                                                          with_alt=float(np.median(ratio[[r['has_alt'] for r in rows]])) if any(r['has_alt'] for r in rows) else None,
                                                          without_alt=float(np.median(ratio[[not r['has_alt'] for r in rows]])))
    # refit (least squares on the parent's feature set, half the sample; errors on the other half)
    keys = sorted(set(k for r in rows for k in r['f']) | {'1', 'out_found', 'out_none'})
    def feats(r):
        d = dict(r['f']); d['1'] = 1; d['out_found' if r['found'] else 'out_none'] = 1
        return [d.get(k, 0) for k in keys]
    X = np.array([feats(r) for r in rows], float)
    Y = np.array([r['steps_a'] - r['base'] for r in rows], float)
    half = len(rows) // 2
    coef, *_ = np.linalg.lstsq(X[:half], Y[:half], rcond=None)
    pred = X @ coef + np.array([r['base'] for r in rows])
    err = np.abs(pred - np.array([r['steps_a'] for r in rows])) / np.maximum(np.array([r['steps_a'] for r in rows]), 1)
    out['prod3a']['refit'] = dict(model={k: float(c) for k, c in zip(keys, coef)},
                                  rel_err_train=dict(median=float(np.median(err[:half])), p99=float(np.percentile(err[:half], 99))),
                                  rel_err_test=dict(median=float(np.median(err[half:])), p99=float(np.percentile(err[half:], 99))),
                                  abs_err_test_median=float(np.median(np.abs(pred - np.array([r['steps_a'] for r in rows]))[half:])))
    print('prod3a', json.dumps({k: v for k, v in out['prod3a'].items() if k != 'refit'}), flush=True)
    print('refit', json.dumps({k: v for k, v in out['prod3a']['refit'].items() if k != 'model'}), flush=True)
    # (c) validation as code
    vrows = []
    t0 = time.time()
    ev = PR.evaluator('R2', F.K_MAIN)
    while len(vrows) < args.runs // 2:
        role = 'W' if rng.random() < 0.6 else 'B'
        r_ = g.roles[role]
        sp = rng.randrange(len(r_['spellings']))
        x = r_['spellings'][sp]
        t = F.dt(x)
        tk = int(r_['tau'][sp])
        inv = rand_ordered_inv(rng, role, sp)
        A = rng.choice(list(F.FAM[role]))
        if not inv[F.FAM[role].index(A)]: continue
        ents = F.inv_entries(g, role, tk, inv)
        prog = F.compile_program(x, role, F.list_data(ents))
        forced = {a: rng.choice('TF') for a in F.dt_atoms(t) if a[0] != 'E'}
        if role == 'W':
            idc = {'EQ': False, 'copy': F.compile_program(x, 'W', 0)}; slot = rng.choice((1, 2))
            idv = lambda nm: False
        else:
            c = rng.choice(F.BOSS_ID_COMBOS); idc = dict(zip(('N1', 'N2', 'EQW'), c)); slot = 0
            idv = (lambda d: (lambda nm: d.get(nm, False)))(idc)
        own, tot, ok = measure_selfval(role, slot, prog, A, idc, forced)
        pid = ev.reg.get(role, sp, inv)
        pr = ev.reg[pid]
        ik = F.ident_key(role, t, idv)
        tab, dcl = cm.ft_table(role, sp, slot, ik)
        dl = (pr.dc[0] - dcl[0], pr.dc[2] - dcl[2])
        cid = (lambda a: 0)
        val, vown, vmask, vpos = ev.validate(pr, t, role, A, idv, lambda a: forced[a], cid, tab, dl)
        vrows.append(dict(role=role, match=(val == 1) == ok, own=own, total=tot, model=vown))
    e = np.array([abs(r['model'] - r['own']) / max(r['own'], 1) for r in vrows if r['own'] is not None])
    wrap = np.array([r['total'] - r['own'] for r in vrows if r['own'] is not None])
    out['selfval'] = dict(n=len(vrows), value_match=sum(r['match'] for r in vrows),
                          rel_err=dict(median=float(np.median(e)), p99=float(np.percentile(e, 99)), max=float(e.max())),
                          call_overhead_steps=dict(median=float(np.median(wrap)), max=float(wrap.max())),
                          time=time.time() - t0)
    print('selfval', json.dumps(out['selfval']), flush=True)
    f = os.path.join(PR.ROOT, 'runs', 'per-root-audit.json')
    json.dump(out, open(f, 'w'), indent=1, default=str)


def audit_encounters(args):
    """(d)-(e): whole encounters by the term with lists written by the rules (several bundles per set, alternatives
    first, appends and evictions), against the evaluator; soundness of every term check across list changes."""
    import random
    import lt_code as L
    R.load_costc()
    PR.build_audit_library()
    rng = random.Random(162)
    g = G()
    K = PR.K6           # the programs are compiled at K_MAIN = 10^6 (R.compile_pid), so the term audit runs there
    res = defaultdict(int)
    sd_play, sd_prod = [], []
    bad = []
    t0 = time.time()
    for it in range(args.runs):
        rule = ('R2', 'R3k2', 'R1')[it % 3]
        ev = PR.evaluator(rule, K)
        # a short history: four encounters among a boss and three workers (lists grow, R3 evicts)
        gr = g.roles
        if rng.random() < 0.4:
            bsp = gr['B']['spellings'].index(F.NAMED_B[rng.choice(['D*', 'D14', 'B_eq', 'pay(1/2,none)'])])
        else:
            bsp = ev.reg[R.sample_pid(random.Random(it), ev, 'B', 'S')].sp
        b = ev.reg.get('B', bsp, F.empty_inv('B'))
        ws = []
        otrees = [sp for sp, x in enumerate(gr['W']['spellings']) if any(a[0] == 'O' for a in F.dt_atoms(F.dt(x)))]
        for q in range(3):
            if rng.random() < 0.5:
                wsp = rng.choice(otrees)
            else:
                wsp = ev.reg[R.sample_pid(random.Random(1000 + 7 * it + q), ev, 'W', 'S')].sp
            ws.append(ev.reg.get('W', wsp, F.empty_inv('W')))
        for step in range(5):
            x, y = rng.sample(range(3), 2)
            trip = (b, ws[x], ws[y])
            tr = ev.triple(*trip)
            te = R.term_encounter(ev, trip[0], trip[1], trip[2], produce=False)
            res['encounters'] += 1
            ok_play = (tr['boss'], tr['a1'], tr['a2']) == te['play']
            ok_steps = tuple(tr['steps']) == te['steps']
            res['play_match'] += ok_play
            res['steps_match'] += ok_steps
            sd_play += [abs(a_ - b_) for a_, b_ in zip(tr['steps'], te['steps'])]
            if not (ok_play and ok_steps):
                bad.append(dict(kind='play', rule=rule, pred=(tr['boss'], tr['a1'], tr['a2']), term=te['play'],
                                ps=tr['steps'], ts=te['steps']))
            # soundness: every term check that returns T is a set its subject plays into
            progs = [R.compile_pid(ev, p) for p in trip]
            play = te['play']
            for j, pid in enumerate(trip):
                role = ev.reg[pid].role
                for A in F.FAM[role]:
                    v, n = F.term_check(tuple(progs), j, A, ev.V, ev.K)
                    res['checks'] += 1
                    vv = v if v in ('T', 'F', 'TO') else ('T' if v == F.T_ else ('F' if v == F.F_ else 'TO'))
                    res['checks_' + vv] += 1
                    if vv == 'T':
                        act = play[0] if j == 0 else play[j]
                        if act not in A:
                            res['soundness_violations'] += 1
                            bad.append(dict(kind='unsound', rule=rule, j=j, A=A, act=act))
            # the rules' productions (Python path) against the term's PROD3A / PROD3 for each attempted set
            prods = ev.productions_full(*trip, tr=tr)
            for (pid, npid, recs), j in zip(prods, range(3)):
                if recs and recs[0] == ('refused',): continue
                pr = ev.reg[pid]
                for r in recs:
                    if r[0] != 'prod' or r[2] not in ('found', 'none', 'dup'): continue
                    A = F.FAM[pr.role][r[1]]
                    L.CACHE.clear()
                    progs = [R.compile_pid(ev, p) for p in trip]
                    F.play3(progs[0], progs[1], progs[2], ev.K)
                    if pr.role == 'W' and ev.rule.alt:
                        prim, alt, n, oc = PR.term_prod3a(tuple(progs), j, A, Pcap=ev.P, V=ev.V, K=ev.K)
                    else:
                        sc, n, oc = F.term_prod(tuple(progs), j, A, Pcap=ev.P, V=ev.V, K=ev.K)
                        prim, alt = (F._rt_data(sc) if sc is not None else None), None
                    _, per = g.hlist(pr.role, pr.tk)
                    ctx = (ev.worker_ctx(pid, j, tr['bex'], (tr['wex'][2 if j == 1 else 0], tr['wex'][3 if j == 1 else 1]), bool(tr['rel']))
                           if pr.role == 'W' else ev.boss_ctx(pid, tr['code']))
                    c = ctx[r[1]]
                    want_p = per[A][c[4]] if c[4] >= 0 else None
                    want_a = per[A][c[5]] if c[5] >= 0 else None
                    res['attempts'] += 1
                    same = (prim == want_p) and (alt == want_a)
                    res['attempt_match'] += same
                    res['attempt_steps_absdiff_max'] = max(res['attempt_steps_absdiff_max'], abs(n - r[3]))
                    sd_prod.append(abs(n - r[3]) / max(n, 1))
                    if not same:
                        bad.append(dict(kind='prod', rule=rule, role=pr.role, term=(oc, str(prim)[:60], str(alt)[:60]),
                                        want=(str(want_p)[:60], str(want_a)[:60])))
                if npid != pid:
                    if pr.role == 'B': b = npid
                    else: ws[ws.index(pid)] = npid
    # a located-and-checked alternative, by the term: O:W ? W : (B1/2 ? W : S) beside a striker (never certified to
    # work) and a certified pay(1/2): its [C] list as R2 writes it (alternative first) and in the other order
    ev = PR.evaluator('R2', K)
    _if, _A, _L = F._if, F._A, F._L
    altprog = _if(_A(('O', F.A_WORK)), _L('W'), _if(_A(('B', F.A_EQ12)), _L('W'), _L('S')))
    wsp = g.roles['W']['spellings'].index(altprog)
    bsp = g.roles['B']['spellings'].index(F.NAMED_B['pay(1/2,none)'])
    bfull = ev.reg.get('B', bsp, F.full_inv(g, 'B', int(g.roles['B']['tau'][bsp])))
    stsp = g.roles['W']['spellings'].index(F.NAMED_W['striker'])
    striker = ev.reg.get('W', stsp, F.full_inv(g, 'W', int(g.roles['W']['tau'][stsp])))
    x0 = ev.reg.get('W', wsp, F.empty_inv('W'))
    tr = ev.triple(bfull, x0, striker)
    ctx = ev.worker_ctx(x0, 1, tr['bex'], (tr['wex'][2], tr['wex'][3]), False)
    x1, recs = ev.part(x0, ctx, [10] * 5, 1000)
    inv = ev.reg[x1].inv
    rev = ev.reg.get('W', wsp, (tuple(reversed(inv[0])), inv[1]))
    alt_res = {}
    for tag, x in (('R2 order (alternative first)', x1), ('primary first', rev)):
        progs = [R.compile_pid(ev, p) for p in (bfull, x, striker)]
        L.CACHE.clear()
        play, steps, _ = F.play3(progs[0], progs[1], progs[2], ev.K)
        v, n = F.term_check(tuple(progs), 1, ('C',), ev.V, ev.K)
        alt_res[tag] = dict(list=[list(z) for z in ev.reg[x].inv], term_check_C=v, steps=n,
                            evaluator=ev.triple(bfull, x, striker)['wex'][0], play=list(play))
    res['alt_located'] = alt_res
    print('alt_located', json.dumps(alt_res), flush=True)
    res = dict(res)
    res['play_steps_absdiff'] =dict(median=float(np.median(sd_play)), max=float(max(sd_play)))
    res['prod_steps_reldiff'] = dict(median=float(np.median(sd_prod)), p99=float(np.percentile(sd_prod, 99)))
    res['time_s'] = time.time() - t0
    print('encounters', json.dumps(res), flush=True)
    for x in bad[:10]: print(' bad', x, flush=True)
    f = os.path.join(PR.ROOT, 'runs', 'per-root-audit.json')
    old = json.load(open(f)) if os.path.exists(f) else {}
    old['encounters'] = res
    old['encounters_bad'] = bad[:50]
    json.dump(old, open(f, 'w'), indent=1, default=str)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('--jobs', default='')
    ap.add_argument('--extend', type=int, default=10000)
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--cell', default='')
    ap.add_argument('--parent', default='')
    ap.add_argument('--runs', type=int, default=5)
    ap.add_argument('--per_script', type=int, default=0)
    args = ap.parse_args()
    fn = globals()[args.cmd]
    fn(args)


if __name__ == '__main__':
    main()
