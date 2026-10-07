"""Driver for the carrier-population cells (predictions/2026-10-06-carrier-populations.md).

    python3 src/carrier_populations_run.py static --arm P --n 7 [--workers 2]
    python3 src/carrier_populations_run.py chain --arm P --prior L --N 1000 10000 30000 100000
    python3 src/carrier_populations_run.py lottery --arm P --prior L --runs 40
    python3 src/carrier_populations_run.py ksens --arm P --n 7

Raw tables go to runs/carrier_populations/ (npz, not committed); summaries to json.
"""
import argparse, json, math, os, sys, time
from collections import defaultdict, Counter
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import lt_code as L
import lt_cert as C
import carrier_populations as CP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'carrier_populations')
os.makedirs(OUT, exist_ok=True)
FOREIGN = (74221, 74545)
MAX_STATES = int(os.environ.get('CP_MAX_STATES', 60000))
VERBOSE = bool(int(os.environ.get('CP_VERBOSE', 0)))


def foreign_alive():
    alive = []
    for p in FOREIGN:
        try:
            os.kill(p, 0); alive.append(p)
        except OSError:
            pass
    return alive


def workers_allowed(req):
    return min(req, 2) if foreign_alive() else min(req, 3)


# ------------------------------------------------------------------ worker state
_G = {}


def _init(n, arm, K):
    sys.setrecursionlimit(1000000)
    _G['cat'] = CP.Catalogue(n, arm, K)


def _units(kind, cat, units):
    """units: list of (term_a, term_b) per unit: a = the unit's representative, b = its distinct twin (or itself)."""
    return units


def _pair_job(job):
    """Compute chk_a^md(t, m) for one target unit t against the listed readers m.  job = (kind, md, a, t, ms,
    unit_reps) where unit_reps maps a unit to (spelling index of rep, spelling index of twin)."""
    kind, md, a, t, ms, reps = job
    cat = _G['cat']
    if reps is None:
        reps = _G.setdefault('taureps', {u: (cat.rep(u, 0), cat.rep(u, 1)) for u in range(cat.T)})
    chk = _G.setdefault(('chk', kind), CP.Checker(kind, cat.V, cat.K))
    out = []
    t0 = time.time()
    for m in ms:
        if m == t:
            tt, mm = cat.term(reps[t][0]), cat.term(reps[t][1])
        else:
            tt, mm = cat.term(reps[t][0]), cat.term(reps[m][0])
        v, s = chk(md, tt, mm, a)
        out.append((m, v, -1 if s is None else s))
    return (md, a, t, out, time.time() - t0)


def _unit_job(job):
    kind, keys, us, reps = job
    cat = _G['cat']
    if reps is None:
        reps = _G.setdefault('taureps', {u: (cat.rep(u, 0), cat.rep(u, 1)) for u in range(cat.T)})
    chk = _G.setdefault(('chk', kind), CP.Checker(kind, cat.V, cat.K))
    out = []
    for u in us:
        tm = cat.term(reps[u][0])
        for (k, md, a) in keys:
            m = tm if k == 'self' else (L.PROG_C if k == 'C' else L.PROG_D)
            v, s = chk(md, tm, m, a)
            out.append((u, k, md, a, v, -1 if s is None else s))
    return out


def unit_keys(atoms_by_unit):
    keys = set()
    for ats in atoms_by_unit:
        for (e, p, q, a) in ats:
            md = CP.MODE_OF_ENTRY[e]
            keys.add(('self', md, a))
            if q in ('C', 'D'): keys.add((q, md, a))
    return sorted(keys)


def compute_tables(pool, cat, kind, units_dt, atoms_by_unit, reps, has_entry, chunk=60, verbose=True):
    """Dense pair matrices CH[(md, a)] (n x n int8; -1 = not asked), raw outcomes (TO counted), steps, unit values."""
    n = len(units_dt)
    t0 = time.time()
    keys = unit_keys(atoms_by_unit)
    UV = {k: dict(val=np.zeros(n, np.int8), steps=np.full(n, -1, np.int64), raw=np.zeros(n, np.int8)) for k in keys}
    # unit values (skip targets without an entry for a: F by the code)
    ujobs = []
    us_all = list(range(n))
    for s0 in range(0, n, 200):
        ujobs.append((kind, keys, us_all[s0:s0 + 200], reps))
    for res in pool.imap_unordered(_unit_job, ujobs):
        for (u, k, md, a, v, s) in res:
            UV[(k, md, a)]['val'][u] = 1 if v == 'T' else 0
            UV[(k, md, a)]['raw'][u] = {'T': 1, 'F': 0, 'TO': 2}[v]
            UV[(k, md, a)]['steps'][u] = s
    if verbose: print('  [%s] unit values: %d units x %d keys (%.0fs)' % (kind, n, len(keys), time.time() - t0), flush=True)
    S, R = CP.needed_pairs(atoms_by_unit, n)
    CH = {}
    mods = sorted(set(list(S) + list(R)))
    for k in mods:
        CH[k] = np.zeros((n, n), np.int8)
    jobs = []
    tot = 0
    allm = list(range(n))
    for (md, a) in mods:
        sset = S.get((md, a), [])
        rset = set(R.get((md, a), []))
        for t in range(n):
            if not has_entry(t, a): continue
            ms = allm if t in rset else sset
            if not len(ms): continue
            for s0 in range(0, len(ms), 4000):
                jobs.append((kind, md, a, t, ms[s0:s0 + 4000], reps))
            tot += len(ms)
    if verbose: print('  [%s] pair checks needed: %d in %d jobs' % (kind, tot, len(jobs)), flush=True)
    steps_rec = []
    n_to = {}
    done = 0
    t1 = time.time()
    for (md, a, t, out, dtm) in pool.imap_unordered(_pair_job, jobs, chunksize=1):
        for (m, v, s) in out:
            CH[(md, a)][t, m] = 1 if v == 'T' else 0
            if v == 'TO': n_to[(md, a)] = n_to.get((md, a), 0) + 1
            if s >= 0: steps_rec.append((md, 1 if a == 'C' else 0, t, m, s))
        done += len(out)
        if verbose and done % 200000 < len(out):
            print('    %d / %d pair checks (%.0fs)' % (done, tot, time.time() - t1), flush=True)
    if verbose: print('  [%s] pair checks done: %d (%.0fs)' % (kind, done, time.time() - t1), flush=True)
    return dict(CH=CH, n_to=n_to, UV=UV, steps=steps_rec, n_pair=tot, t_unit=t1 - t0, t_pair=time.time() - t1)


def compose(units_dt, tabs):
    n = len(units_dt)
    A = np.zeros((n, n), np.int8)
    selfa = np.zeros(n, np.int8)
    CH, UV = tabs['CH'], tabs['UV']
    for x in range(n):
        A[x] = CP.compose_row(x, units_dt, CH, UV, n)
        selfa[x] = CP.self_action(x, units_dt, UV)
    return A, selfa


# ------------------------------------------------------------------ static
def cmd_static(a):
    t0 = time.time()
    nw = workers_allowed(a.workers)
    print('workers', nw, 'foreign alive', foreign_alive(), flush=True)
    cat = CP.Catalogue(a.n, a.arm, a.K, verbose=True)
    tb = time.time() - t0
    T = cat.T
    reps = {t: (cat.rep(t, 0), cat.rep(t, 1)) for t in range(T)}
    hasE = lambda u, aa: cat.has_entry(u, aa)
    with Pool(nw, initializer=_init, initargs=(a.n, a.arm, a.K)) as pool:
        ckpt = os.path.join(OUT, 'ideal_tau_%s_n%d_K%d.npz' % (a.arm, a.n, a.K))
        if a.resume and os.path.exists(ckpt):
            zz = np.load(ckpt); A_tau, self_tau = zz['A_tau'], zz['self_tau']
            ideal = json.load(open(ckpt.replace('.npz', '.json')))
        else:
            ideal = compute_tables(pool, cat, 'ideal', cat.tau_dt, cat.tau_atoms, None, hasE)
            A_tau, self_tau = compose(cat.tau_dt, ideal)
            ideal = dict(n_pair=ideal['n_pair'], t_unit=ideal['t_unit'], t_pair=ideal['t_pair'],
                         n_TO=int(sum(ideal['n_to'].values()) + sum(int((d['raw'] == 2).sum()) for d in ideal['UV'].values())))
            np.savez_compressed(ckpt, A_tau=A_tau, self_tau=self_tau)
            json.dump(ideal, open(ckpt.replace('.npz', '.json'), 'w'))
        w = cat.spelling_mass('L')
        lp = CP.lump(cat, A_tau, self_tau, w)
        classes = lp['classes']
        nc = len(classes)
        print('lumped: %d classes (%d split types, %d split classes) from %d types' % (nc, lp['n_split_types'], lp['n_split_classes'], T), flush=True)
        # executable table on class representatives
        crep = [c['rep'] for c in classes]
        ct = np.array([cat.tau[k] for k in crep])
        A_id = A_tau[np.ix_(ct, ct)].copy()
        A_id[np.arange(nc), np.arange(nc)] = self_tau[ct]
        # executable table on class representatives (all classes, or a sample when --exec_sample > 0)
        sub = list(range(nc))
        if a.exec_sample > 0:
            rng = np.random.default_rng(5)
            heavy = list(np.argsort(-np.array([cat.spelling_mass('L')[c['spellings']].sum() for c in classes]))[:a.exec_sample // 2])
            sub = sorted(set(int(i) for i in heavy) | set(int(i) for i in rng.choice(nc, a.exec_sample // 2, replace=False)))
        srep = [crep[i] for i in sub]
        cdt = [cat.tau_dt[cat.tau[k]] for k in srep]
        catoms = [cat.tau_atoms[cat.tau[k]] for k in srep]
        creps = {i: (srep[i], srep[i]) for i in range(len(sub))}
        hasC = lambda u, aa: cat.has_entry(int(cat.tau[srep[u]]), aa)
        te = time.time()
        exe = compute_tables(pool, cat, 'exec', cdt, catoms, creps, hasC)
        A_exe, self_exe = compose(cdt, exe)
        t_exec = time.time() - te
        A_exe[np.arange(len(sub)), np.arange(len(sub))] = self_exe
        diff = np.argwhere(A_exe != A_id[np.ix_(sub, sub)])
        if a.exec_sample > 0:
            A_exe2 = A_id.copy()        # the class table is the ideal one; the executable table checked on the sample
        else:
            A_exe2 = A_exe
    # masses per prior
    masses = {}
    for pr in ('L', 'Lstd') + (('Leq',) if a.arm == 'E' else ()):
        ws = cat.spelling_mass(pr)
        masses[pr] = np.array([ws[c['spellings']].sum() for c in classes])
    masses['U'] = np.full(nc, 1.0 / nc)
    tag = '%s_n%d_K%d' % (a.arm, a.n, a.K)
    np.savez_compressed(os.path.join(OUT, 'static_%s.npz' % tag), A_tau=A_tau, self_tau=self_tau, A_class=A_exe2, A_class_ideal=A_id,
                        tau=cat.tau, **{'mass_' + k: v for k, v in masses.items()},
                        class_of_spelling=_class_of_spelling(classes, len(cat.spell)), class_rep=np.array(crep))
    steps = np.array([s[4] for s in exe['steps']]) if exe['steps'] else np.zeros(0)
    info = dict(arm=a.arm, n=a.n, K=a.K, V=cat.V, n_sexprs=len(cat.sexprs), n_spellings=len(cat.spell), n_tau=T,
                n_classes=nc, n_split_types=lp['n_split_types'], n_split_classes=lp['n_split_classes'],
                build_s=tb, ideal_pair_checks=ideal['n_pair'], ideal_s=ideal['t_unit'] + ideal['t_pair'],
                exec_pair_checks=exe['n_pair'], exec_s=t_exec, exec_vs_ideal_diff=int(len(diff)),
                exec_sample_classes=len(sub) if a.exec_sample > 0 else None,
                class_table='ideal (executable checked on a sample of classes)' if a.exec_sample > 0 else 'executable',
                exec_TO=int(sum(exe['n_to'].values()) + sum(int((d['raw'] == 2).sum()) for d in exe['UV'].values())),
                ideal_TO=ideal['n_TO'],
                exec_check_steps=dict(n=int(len(steps)), max=int(steps.max()) if len(steps) else None,
                                      p50=float(np.median(steps)) if len(steps) else None,
                                      p99=float(np.percentile(steps, 99)) if len(steps) else None),
                exec_unit_steps_max=int(max([int(d['steps'].max()) for d in exe['UV'].values()] + [0])),
                classes=[dict(rep=cat.name(c['rep']), n_spellings=len(c['spellings']), n_types=len(c['types']), split=c['split'],
                              mass_L=float(masses['L'][i]), mass_Lstd=float(masses['Lstd'][i]),
                              self_C=int(A_exe2[i, i]), dt=CP.show_dt(cat.tau_dt[cat.tau[c['rep']]]),
                              list=[(e[0], C.show_script(e[1])) for e in C.uncons(cat.tau_list[cat.tau[c['rep']]])] if cat.tau_list[cat.tau[c['rep']]] != 0 else [])
                         for i, c in enumerate(classes)],
                total_s=time.time() - t0)
    json.dump(info, open(os.path.join(OUT, 'static_%s.json' % tag), 'w'), indent=1)
    # the per-check steps (exec) for cost tables
    np.save(os.path.join(OUT, 'exec_steps_%s.npy' % tag), np.array(exe['steps'], dtype=np.int64) if exe['steps'] else np.zeros((0, 5), np.int64))
    print(json.dumps({k: v for k, v in info.items() if k != 'classes'}, indent=1), flush=True)


def load_static(arm, n=7, K=10 ** 6):
    tag = '%s_n%d_K%d' % (arm, n, K)
    z = np.load(os.path.join(OUT, 'static_%s.npz' % tag))
    info = json.load(open(os.path.join(OUT, 'static_%s.json' % tag)))
    return z, info


ALIASES = {'C': 'Cc', 'D': 'Dc', 'if(CHK(them,me,C),C,D)': 'CB', 'if(CHK(them,me,C),if(CHK(me,them,C),C,D),D)': 'CB1',
           'if(CHK(them,me,C),if(CHK(them,^D,D),C,D),D)': 'CBP', 'if(CHK(me,them,C),C,D)': 'LobC',
           'if(CHK(them,me,C),D,C)': 'CBdef'}


def class_names(info):
    return [ALIASES.get(c['rep'], c['rep']) for c in info['classes']]


def class_props(A, info, arm):
    """establisher (self-C and D against D), self-cooperator, unconditional cooperator, entry of a class (E)."""
    nc = A.shape[0]
    names = [c['rep'] for c in info['classes']]
    iD = names.index('D')
    selfc = A[np.arange(nc), np.arange(nc)] == 1
    est = selfc & (A[:, iD] == 0)
    allc = (A == 1).all(1)
    ent = []
    for c in info['classes']:
        d = c['dt']
        e0, e5 = 'CHK(' in d, 'CHK_5(' in d
        ent.append('both' if (e0 and e5) else ('5' if e5 else ('0' if e0 else 'none')))
    return dict(iD=iD, selfc=selfc, est=est, allc=allc, entry=np.array(ent))


def fast_chain_class():
    """LogChain with the two-type replicator fates of a monomorphic state in closed form (the same targets the
    numerical replicator reaches: q fixes unless c > a and b > d, where the stable mixture x* = (c - a) / ((c - a) +
    (b - d)) is the target; a first-order-dying q gets the chain's drift/valley target mono(q)).  Polymorphic states
    use the numerical fates unchanged.  Validated against LogChain on the P arm (notes §2)."""
    from chain_log import LogChain

    class FastChain(LogChain):
        def fates(self, key, ids, x, q, Uq):
            if len(ids) != 1:
                return LogChain.fates(self, key, ids, x, q, Uq)
            a, b, c, d = Uq[0, 0], Uq[0, 1], Uq[1, 0], Uq[1, 1]
            N = self.N
            if c > a + 1e-12 and b > d + 1e-12:
                xs = (c - a) / ((c - a) + (b - d))
                if xs > 1 - 1e-6:
                    return [(1.0, self.mono(q), N)]
                kstar = max(1, int(round(N * xs)))
                return self.targets(np.array([int(ids[0]), int(q)]), np.array([1.0 - xs, xs]), kstar, Uq)
            return [(1.0, self.mono(q), N)]
    return FastChain


def chain_cell(job):
    """One chain cell: (arm, prior, N, twins, log_theta, tag)."""
    from chain_log import LogChain, NEG
    from dollar_partitions import ClassProvider
    import solver_audit as SA
    arm, prior, N, twins, log_theta, label, A_kind = job
    t0 = time.time()
    z, info = load_static(arm)
    A = z['A_class'] if A_kind == 'exec' else z['A_class_ideal']
    mu = z['mass_' + prior].astype(float)
    names = class_names(info)
    names0 = list(names)
    dropped = []
    if label.startswith('noclosed'):
        # control (not preregistered): remove every class in a closed component of the leak test, iterated
        from carrier_populations_report import leak_test
        keep = np.arange(A.shape[0])
        while True:
            lt = leak_test(A[np.ix_(keep, keep)])
            cl = sorted({int(keep[i]) for c in lt['closed'] for i in c})
            if not cl: break
            dropped += cl
            keep = np.array([k for k in keep if k not in set(cl)])
        A = A[np.ix_(keep, keep)]; mu = mu[keep]; names = [names[k] for k in keep]
        info = dict(info, classes=[info['classes'][k] for k in keep])
    dropped_names = [names0[k] for k in dropped]
    U, PCC = CP.pay_matrix(A)
    mu = mu / mu.sum()
    pr = class_props(A, info, arm)
    nc = len(mu)
    # seeds: stable candidates (<= 3 classes; triples on the heaviest 120 classes) and invasion-closure rest points
    cfn = os.path.join(OUT, 'seeds_%s_%s_%s_%s.json' % (arm, prior, A_kind, label.split('_')[0]))
    if os.path.exists(cfn):
        seeds = [tuple(s) for s in json.load(open(cfn))]
    else:
        pool = np.argsort(-mu)[:120]
        cands, counts = SA.enumerate_candidates_fast(U, mu, pool=pool)
        S1, n1, comp1 = SA.invasion_closure(U, mu, max_nodes=6000, branch=3)
        seeds = [(x['ids'], x['x']) for x in cands + S1 if x['size'] > 1 and x['status'] == 'stable']
        json.dump(dict(counts=counts, closure_nodes=n1, closure_complete=comp1, n_saturated=len(S1), n_seeds=len(seeds),
                       saturated=[dict(ids=x['ids'], x=x['x'], deep=bool(x['deep']), status=x['status']) for x in S1]),
                  open(cfn.replace('.json', '_meta.json'), 'w'), default=str)
        json.dump([[list(map(int, s[0])), list(map(float, s[1]))] for s in seeds], open(cfn, 'w'))
    CH = fast_chain_class() if os.environ.get('CP_FAST', '0') == '1' else LogChain
    ch = CH(ClassProvider(U, mu), N=N, w=0.3, Ufull=U if twins else None, twins=twins, theta=1.0, max_states=10 ** 9)
    ch.explore_log(extra_states=[(list(s[0]), list(s[1])) for s in seeds], log_theta=log_theta, max_states=MAX_STATES, verbose=VERBOSE)
    keys_all, lpi_all, sinfo, out_un, rec = ch.solve_sparse()
    keys = [keys_all[i] for i in rec]
    lpi = lpi_all[rec]
    pi = np.exp(lpi)
    LA, _ = ch.log_matrix(keys)
    # stats
    pcc = 0.0; piD = 0.0; coop = np.zeros(len(keys)); stat = []
    for i, k in enumerate(keys):
        ids, x, kind = ch.states[k]; ids = list(ids); x = np.asarray(x)
        c = float(x @ PCC[np.ix_(ids, ids)] @ x)
        coop[i] = c
        pcc += pi[i] * c
        if kind == 'mono' and ids[0] == pr['iD']: piD += pi[i]
    pi_coop = float(pi[coop >= 0.95].sum())
    # entry-level split of cooperative pi (E)
    ent_split = defaultdict(float)
    for i, k in enumerate(keys):
        if coop[i] < 0.95: continue
        ids, x, kind = ch.states[k]
        for j, xi in zip(ids, x):
            ent_split[pr['entry'][j]] += pi[i] * xi
    # cut: total stationary flow into unexplored states vs total transition flow
    tot_flow = 0.0
    for i in range(len(keys)):
        row = LA[i].copy(); row[i] = NEG
        f = row[np.isfinite(row)]
        if len(f): tot_flow += pi[i] * float(np.exp(np.logaddexp.reduce(f)))
    infl = {k2: float(np.exp(np.logaddexp.reduce([lpi_all[i] + lw for i, lw in lst]))) for k2, lst in out_un.items()}
    cut = float(sum(infl.values()))
    # cut diagnostic (concessions_cutdiag pattern): the dropped flow by destination kind / cooperation and by source
    cutdiag = defaultdict(float)
    for k2, lst in out_un.items():
        ids2, x2, kind2 = ch.states[k2]
        c2 = float(np.asarray(x2) @ PCC[np.ix_(list(ids2), list(ids2))] @ np.asarray(x2))
        for i, lw in lst:
            f = float(np.exp(lpi_all[i] + lw))
            ids1, x1, kind1 = ch.states[keys_all[i]]
            c1 = float(np.asarray(x1) @ PCC[np.ix_(list(ids1), list(ids1))] @ np.asarray(x1))
            cutdiag['dst_%s_%s' % (kind2, 'coop' if c2 >= 0.95 else 'noncoop')] += f
            cutdiag['src_%s' % ('coop' if c1 >= 0.95 else 'noncoop')] += f
            if c1 >= 0.95 and c2 < 0.95: cutdiag['coop_to_noncoop'] += f
    cutdiag = {k: v / cut for k, v in cutdiag.items()} if cut > 0 else {}
    cutdiag['n_destinations'] = len(out_un)
    def desc(k):
        ids, x, kind = ch.states[k]
        return ' + '.join('%s:%.3f' % (names[i], xi) for i, xi in zip(ids, x))
    order = np.argsort(-pi)
    support = []
    for i in order[:12]:
        if pi[i] < 1e-4: break
        k = keys[i]
        row = LA[i].copy(); row[i] = NEG
        fin = np.isfinite(row)
        lex = float(np.logaddexp.reduce(row[fin])) if fin.any() else NEG
        ex = []
        for j in np.argsort(-np.where(fin, row, -np.inf))[:4]:
            if not fin[j]: break
            muts = sorted(ch.lmut.get((k, keys[j]), {}).items(), key=lambda kv: -kv[1])[:3]
            ex.append(dict(to=desc(keys[j]), log10_rate=float(row[j] / math.log(10)), mutants=[(names[q], float(v / math.log(10))) for q, v in muts]))
        support.append(dict(state=desc(k), pi=float(pi[i]), coop=float(coop[i]), log10_exit=lex / math.log(10) if np.isfinite(lex) else None, exits=ex))
    # the top cooperative state and its exits by mutant: neutral / strict
    top = None
    ci = [i for i in order if coop[i] >= 0.95]
    if ci:
        i = ci[0]; k = keys[i]
        ids, x, kind = ch.states[k]; ids = list(ids); x = np.asarray(x)
        uaa = float(x @ U[np.ix_(ids, ids)] @ x)
        exits = []
        tot = dict(neutral=0.0, strict=0.0, deleterious=0.0)
        for k2 in ch.ledge.get(k, {}):
            if k2 == k: continue
            for q, lw in ch.lmut.get((k, k2), {}).items():
                d1 = float(U[q, ids] @ x - uaa)
                d2 = float(U[q, q] - U[ids, q] @ x)
                typ = 'strict' if d1 > 1e-9 else ('neutral' if d1 > -1e-9 else 'deleterious')
                r = ch.edge_rho.get((k, k2, q))
                rho = r[0] if r else None
                tot[typ] += math.exp(lw)
                exits.append(dict(mutant=names[q], to=desc(k2), rate=math.exp(lw), type=typ, d1=d1, d2=d2,
                                  rho=rho, N_rho=(N * rho) if rho else None, N_d1=N * d1, mu=float(mu[q])))
        exits.sort(key=lambda e: -e['rate'])
        top = dict(state=desc(k), pi=float(pi[i]), exit_total=sum(tot.values()), **{'exit_' + kk: v for kk, v in tot.items()}, exits=exits[:10])
    # entry into all-D
    entry = None
    kD = ch.mono(pr['iD'])
    if kD in ch.ledge:
        ents = []
        for k2, lw in ch.ledge[kD].items():
            if k2 == kD: continue
            ids, x, kind = ch.states[k2]
            c = float(np.asarray(x) @ PCC[np.ix_(list(ids), list(ids))] @ np.asarray(x))
            for q, lwq in ch.lmut.get((kD, k2), {}).items():
                r = ch.edge_rho.get((kD, k2, q))
                ents.append(dict(mutant=names[q], to=desc(k2), coop=c, rate=math.exp(lwq), rho=r[0] if r else None,
                                 N_rho=N * r[0] if r else None, d1=float(U[q, pr['iD']] - U[pr['iD'], pr['iD']]),
                                 d2=float(U[q, q] - U[pr['iD'], q]), mu=float(mu[q])))
        ents.sort(key=lambda e: -e['rate'])
        entry = dict(total_rate=sum(e['rate'] for e in ents), coop_rate=sum(e['rate'] for e in ents if e['coop'] >= 0.95), top=ents[:8])
    res = dict(arm=arm, prior=prior, N=N, twins=twins, log10_theta=log_theta / math.log(10), label=label, table=A_kind,
               fast=os.environ.get('CP_FAST', '0') == '1',
               n_classes=nc, n_dropped=len(dropped), dropped=dropped_names, n_seeds=len(seeds), n_expanded=len(keys_all), n_recurrent=len(keys), solve=sinfo,
               pcc=pcc, pi_D=piD, pi_coop=pi_coop, poly=float(sum(pi[i] for i, k in enumerate(keys) if ch.states[k][2] == 'poly')),
               entry_split=dict(ent_split), cut_flow=cut, cut_diagnostic=dict(cutdiag), total_flow=tot_flow, cut_rel=cut / tot_flow if tot_flow > 0 else None,
               twin_moves=ch.n_twin_moves, indeterminate=len(ch.indeterminate), support=support, top_coop=top, entry_D=entry,
               time_s=time.time() - t0)
    return res


def cmd_chain(a):
    jobs = []
    for arm, prior in [x.split(':') for x in a.cells]:
        for N in a.N:
            for tw in a.twins:
                jobs.append((arm, prior, N, bool(tw), math.log(a.theta), a.label, a.table))
    path = os.path.join(OUT, 'chain_%s.json' % a.out)
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {(r['arm'], r['prior'], r['N'], r['twins'], round(r['log10_theta'], 3), r['table'], r['label']) for r in rows}
    jobs = [j for j in jobs if (j[0], j[1], j[2], j[3], round(j[4] / math.log(10), 3), j[6], j[5]) not in done]
    jobs.sort(key=lambda j: -j[2])
    nw = workers_allowed(a.workers)
    print('chain jobs', len(jobs), 'workers', nw, 'foreign', foreign_alive(), flush=True)
    with Pool(nw) as pool:
        for r in pool.imap_unordered(chain_cell, jobs, chunksize=1):
            rows.append(r)
            json.dump(rows, open(path, 'w'), indent=1, default=str)
            t = r['top_coop'] or {}
            print('%s %s N=%d tw=%s: P(C,C) %.4f pi(D) %.4f pi(coop) %.4f top %s (%.3f) exit %.2e [n %.2e s %.2e] states %d cut %.1e (%.0fs)' % (
                r['arm'], r['prior'], r['N'], r['twins'], r['pcc'], r['pi_D'], r['pi_coop'], t.get('state'), t.get('pi', 0), t.get('exit_total', 0),
                t.get('exit_neutral', 0), t.get('exit_strict', 0), r['n_recurrent'], r['cut_rel'] or 0, r['time_s']), flush=True)


def small_chain_check(Ns=(1000, 10000)):
    """notes §1.5: on the n <= 5 sub-catalogue, the unlumped chain (every spelling its own class) against the lumped
    chain with and without twin drift: class-aggregated P(C,C), pi(all-D)."""
    from chain_log import LogChain
    from dollar_partitions import ClassProvider
    sys.path.insert(0, os.path.join(ROOT, 'tests'))
    import test_carrier_populations as TT
    c = TT.cat(5)
    A, s = TT._tau_tables(c)['exec']
    n = len(c.spell)
    Asp = CP.spelling_matrix(c, A, s, list(range(n)))
    Usp, Psp = CP.pay_matrix(Asp)
    wsp = c.spelling_mass('L')
    lp = CP.lump(c, A, s, wsp)
    Ac = lp['A']; Uc, Pc = CP.pay_matrix(Ac)
    wc = np.array([wsp[cl['spellings']].sum() for cl in lp['classes']])
    cls_of = _class_of_spelling(lp['classes'], n)
    iDsp = [k for k, sp in enumerate(c.spell) if c.sexprs[sp['i']] == ('D',)][0]
    out = []
    def stats(ch, P, iD):
        keys, lpi, info, _, rec = ch.solve_sparse()
        pcc = 0.0; pd = 0.0
        for i in rec:
            k = keys[i]; ids, x, kind = ch.states[k]; x = np.asarray(x); p = math.exp(lpi[i])
            pcc += p * float(x @ P[np.ix_(list(ids), list(ids))] @ x)
            if kind == 'mono' and ids[0] == iD: pd += p
        return pcc, pd, len(rec)
    for N in Ns:
        r = dict(N=N)
        chu = LogChain(ClassProvider(Usp, wsp), N=N, w=0.3).explore_closure(max_states=20000)
        r['unlumped'] = stats(chu, Psp, iDsp) + (chu.closure_complete,)
        for tw in (False, True):
            chl = LogChain(ClassProvider(Uc, wc), N=N, w=0.3, twins=tw, Ufull=Uc if tw else None).explore_closure(max_states=20000)
            r['lumped_twins' if tw else 'lumped'] = stats(chl, Pc, int(cls_of[iDsp])) + (chl.closure_complete,)
        out.append(r)
        print('n<=5 chain', r, flush=True)
    return dict(n_spellings=n, n_classes=len(wc), rows=out)


def cmd_validate(a):
    """notes §1.10 items 5-9 on the n = 7 static table."""
    rng = np.random.default_rng(11)
    out = {}
    out['small_chain'] = small_chain_check()
    z, info = load_static('P')
    A_tau, self_tau = z['A_tau'], z['self_tau']
    cat = CP.Catalogue(7, 'P', 10 ** 6)
    n = len(cat.spell)
    # Lemma T and composition on a random sample of n = 7 spelling pairs (direct whole plays against the tau table)
    bad = []; nn = 0
    pairs = [tuple(rng.integers(0, n, 2)) for _ in range(a.sample)]
    multi = [t for t in range(cat.T) if len(cat.members[t]) >= 2]
    for _ in range(a.sample // 4):
        t = multi[rng.integers(len(multi))]; x, x2 = rng.choice(cat.members[t], 2, replace=False)
        pairs.append((int(x), int(x2)))
    for _ in range(a.sample // 8):
        x = int(rng.integers(n)); pairs.append((x, x))
    for (x, y) in pairs:
        x, y = int(x), int(y)
        L.CACHE.clear()
        r = L.play(cat.term(x), cat.term(y), cat.K)[0]
        pred = self_tau[cat.tau[x]] if x == y else A_tau[cat.tau[x], cat.tau[y]]
        nn += 1
        if (r == 'C') != bool(pred): bad.append((cat.name(x), cat.name(y), r, int(pred)))
    out['lemmaT_sample'] = dict(n=nn, mismatches=len(bad), examples=bad[:10])
    print('Lemma T sample', out['lemmaT_sample'], flush=True)
    # class table vs whole plays on a sample of class pairs (exec)
    A = z['A_class']; crep = z['class_rep']; nc = len(crep)
    bad = []
    idx = list(range(min(nc, 40))) + list(rng.integers(0, nc, 60))
    for i in idx:
        for j in list(rng.integers(0, nc, 15)) + [i]:
            i, j = int(i), int(j)
            L.CACHE.clear()
            r = L.play(cat.term(int(crep[i])), cat.term(int(crep[j])), cat.K)[0]
            if (r == 'C') != bool(A[i, j]): bad.append((i, j, r, int(A[i, j])))
    out['class_table_sample'] = dict(n=len(idx) * 16, mismatches=len(bad), examples=bad[:10])
    print('class table sample', out['class_table_sample'], flush=True)
    # Lemma G exhaustive; exploited establishers; unconditional cooperators
    U, PCC = CP.pay_matrix(A)
    pr = class_props(A, info, 'P')
    names = class_names(info)
    sg = np.array([CP.s_guarded(_dt_of(cat, int(k))) for k in crep])
    viol = [(names[e], names[q]) for e in np.nonzero(pr['est'] & sg)[0] for q in np.nonzero(U[:, e] > U[e, e] + 1e-9)[0]]
    expl = [(names[e], names[q]) for e in np.nonzero(pr['est'])[0] for q in np.nonzero((A[e] == 1) & (A[:, e] == 0))[0]]
    strict_inv = [(names[e], names[q]) for e in np.nonzero(pr['est'])[0] for q in np.nonzero(U[:, e] > U[e, e] + 1e-9)[0]]
    out['lemmaG'] = dict(n_est=int(pr['est'].sum()), n_est_sguarded=int((pr['est'] & sg).sum()), violations=viol[:20], n_violations=len(viol))
    out['exploited_establishers'] = dict(n_pairs=len(expl), n_est=len({e for e, q in expl}), examples=expl[:20],
                                         n_strict_invaded_est=len({e for e, q in strict_inv}))
    print('Lemma G', out['lemmaG'], 'exploited', out['exploited_establishers']['n_pairs'], flush=True)
    # empty-selection shortcut against the term
    badF = 0; nF = 0
    for _ in range(200):
        k = int(rng.integers(n)); m = int(rng.integers(n))
        for aa in ('C', 'D'):
            if not cat.has_entry(cat.tau[k], aa):
                nF += 1
                badF += C.check_value(0, cat.V, cat.term(k), cat.term(m), aa, cat.K)[0] != 'F'
    out['empty_selection'] = dict(n=nF, mismatches=badF)
    json.dump(out, open(os.path.join(OUT, 'validate.json'), 'w'), indent=1, default=str)
    print(json.dumps(out, default=str)[:3000])


# ------------------------------------------------------------------ the eps = 0 lottery
def _lottery_numba():
    from abm import njit
    from almost_all_seeds import _sample_parent, _island_cc

    @njit(cache=True)
    def closure_status(U, selfc, glob, K, res_ids, nres):
        """Z = closure of the residents under 'a present class q joins if U[q, z] >= U[z, z] for some z in Z';
        returns 1 if every class in Z self-cooperates, 0 if none does, -1 otherwise."""
        inZ = np.zeros(K, np.bool_)
        queue = np.empty(K, np.int64); qn = 0; qh = 0
        for t in range(nres):
            r = res_ids[t]
            if not inZ[r]:
                inZ[r] = True; queue[qn] = r; qn += 1
        while qh < qn:
            z = queue[qh]; qh += 1
            uzz = U[z, z]
            for q in range(K):
                if glob[q] > 0 and not inZ[q] and U[q, z] >= uzz - 1e-9:
                    inZ[q] = True; queue[qn] = q; qn += 1
        ns = 0
        for t in range(qn):
            if selfc[queue[t]]: ns += 1
        if ns == qn: return 1
        if ns == 0: return 0
        return -1

    @njit(cache=True)
    def e2_status(U, selfc, glob, K, a):
        uaa = U[a, a]
        for q in range(K):
            if glob[q] == 0 or q == a: continue
            if U[q, a] > uaa + 1e-9: return -1
            if abs(U[q, a] - uaa) <= 1e-9 and U[q, q] > U[a, q] + 1e-9: return -1
        return 1 if selfc[a] else 0

    @njit(cache=True)
    def run(U, PCC, init, N, w, m, gens, every, seed, selfc, ent):
        np.random.seed(seed)
        I, K = init.shape
        counts = init.copy()
        paysum = np.zeros((I, K))
        pres = np.zeros((I, K), np.int64); npres = np.zeros(I, np.int64); pos = -np.ones((I, K), np.int64)
        for i in range(I):
            for k in range(K):
                if counts[i, k] > 0:
                    pres[i, npres[i]] = k; pos[i, k] = npres[i]; npres[i] += 1
            for t in range(npres[i]):
                j = pres[i, t]
                for t2 in range(npres[i]):
                    k = pres[i, t2]
                    paysum[i, j] += counts[i, k] * U[j, k]
        glob = np.zeros(K, np.int64)
        dec = np.full(3, -1, np.int64)       # decision generation for E1, E2, E3
        outc = np.full(3, -1, np.int64)      # 1 success, 0 fail
        estab = -1                           # first generation with an island at P(C,C) >= 0.9
        both_alive_first = -1; merges = np.zeros(64, np.int64); nmerge = 0
        had0 = False; had5 = False
        nsamp = gens // every
        tr_cc = np.zeros(nsamp); s = 0
        res_ids = np.empty(K, np.int64)
        last_g = gens
        for g in range(gens):
            for e in range(I * N):
                i = np.random.randint(I)
                src = i
                if m > 0.0 and I > 1 and np.random.random() < m:
                    src = np.random.randint(I - 1)
                    if src >= i: src += 1
                child = _sample_parent(counts, paysum, U, pres, npres, src, N, w)
                u = np.random.randint(N); acc = 0; victim = pres[i, 0]
                for t in range(npres[i]):
                    k = pres[i, t]; acc += counts[i, k]
                    if u < acc:
                        victim = k; break
                if victim == child:
                    continue
                counts[i, victim] -= 1
                if counts[i, victim] == 0:
                    p = pos[i, victim]; last = pres[i, npres[i] - 1]
                    pres[i, p] = last; pos[i, last] = p; pos[i, victim] = -1; npres[i] -= 1
                new = counts[i, child] == 0
                if new:
                    pres[i, npres[i]] = child; pos[i, child] = npres[i]; npres[i] += 1
                counts[i, child] += 1
                for t in range(npres[i]):
                    j = pres[i, t]
                    if new and j == child:
                        continue
                    paysum[i, j] += U[j, child] - U[j, victim]
                if new:
                    v = 0.0
                    for t in range(npres[i]):
                        k = pres[i, t]
                        v += counts[i, k] * U[child, k]
                    paysum[i, child] = v
            if (g + 1) % every == 0:
                for k in range(K): glob[k] = 0
                cct = 0.0
                for i in range(I):
                    for t in range(npres[i]):
                        glob[pres[i, t]] += counts[i, pres[i, t]]
                    cc, pay = _island_cc(counts, PCC, U, pres, npres, paysum, i, N)
                    cct += cc
                    if estab < 0 and cc >= 0.9: estab = g + 1
                if s < nsamp:
                    tr_cc[s] = cct / I; s += 1
                # entries (E): establishers alive on entry 0 / entry 5
                a0 = False; a5 = False
                for k in range(K):
                    if glob[k] > 0 and ent[k] == 1: a0 = True
                    if glob[k] > 0 and ent[k] == 2: a5 = True
                if a0 and a5 and both_alive_first < 0: both_alive_first = g + 1
                if (had0 and had5) and not (a0 and a5) and nmerge < 64:
                    merges[nmerge] = g + 1; nmerge += 1
                had0 = a0; had5 = a5
                # global fixation of a non-cooperating class
                npg = 0; only = -1
                for k in range(K):
                    if glob[k] > 0:
                        npg += 1; only = k
                gfail = npg == 1 and not selfc[only]
                # endpoints
                for E in range(3):
                    if dec[E] >= 0: continue
                    if gfail:
                        dec[E] = g + 1; outc[E] = 0; continue
                    allres = True; allcoop = True
                    for i in range(I):
                        if E < 2 and npres[i] != 1:
                            allres = False; break
                        if E == 1:
                            st = e2_status(U, selfc, glob, K, pres[i, 0])
                        else:
                            for t in range(npres[i]): res_ids[t] = pres[i, t]
                            st = closure_status(U, selfc, glob, K, res_ids, npres[i])
                        if st < 0:
                            allres = False; break
                        if st == 0: allcoop = False
                    if allres:
                        dec[E] = g + 1; outc[E] = 1 if allcoop else 0
                if dec[0] >= 0 and dec[1] >= 0 and dec[2] >= 0:
                    last_g = g + 1
                    break
        isl_cc = np.zeros(I)
        for i in range(I):
            isl_cc[i], pay = _island_cc(counts, PCC, U, pres, npres, paysum, i, N)
        return dec, outc, estab, counts, isl_cc, tr_cc[:s], both_alive_first, merges[:nmerge], last_g
    return run


_LOT = {}


def lottery_job(job):
    arm, prior, rep, N, I, mN, gens = job
    if 'run' not in _LOT:
        _LOT['run'] = _lottery_numba()
    z, info = load_static(arm)
    A = z['A_class']
    U, PCC = CP.pay_matrix(A)
    U = np.ascontiguousarray(U); PCC = np.ascontiguousarray(PCC)
    mu = z['mass_' + prior].astype(float); mu /= mu.sum()
    pr = class_props(A, info, arm)
    names = class_names(info)
    K = len(mu)
    ent = np.zeros(K, np.int64)
    for k in range(K):
        if pr['est'][k]:
            ent[k] = {'0': 1, '5': 2, 'both': 3}.get(pr['entry'][k], 0)
    rng = np.random.default_rng([N, I, rep, 20261006, ['P', 'O', 'E'].index(arm[0]), ['L', 'U', 'Lstd', 'Leq'].index(prior)])
    init = np.zeros((I, K), np.int64)
    for i in range(I):
        init[i] = rng.multinomial(N, mu)
    t = time.time()
    dec, outc, estab, counts, isl_cc, tr, baf, merges, last_g = _LOT['run'](
        U, PCC, init, N, 0.3, mN / N, gens, 10, 7919 * rep + 13 * N + I + 1000 * ['L', 'U', 'Lstd', 'Leq'].index(prior) + 100000 * ['P', 'O', 'E'].index(arm[0]),
        pr['selfc'].astype(np.bool_), ent)
    glob = counts.sum(0)
    top = sorted([(names[k], int(v)) for k, v in enumerate(glob) if v > 0], key=lambda kv: -kv[1])[:8]
    est_present = [names[k] for k in range(K) if glob[k] > 0 and pr['est'][k]]
    E = ('E1', 'E2', 'E3')
    return dict(arm=arm, prior=prior, rep=rep, N=N, I=I, mN=mN, gens=gens, last_gen=int(last_g),
                **{E[j] + '_gen': int(dec[j]) for j in range(3)},
                **{E[j]: ('success' if outc[j] == 1 else 'fail') if dec[j] >= 0 else 'censored' for j in range(3)},
                establish_gen=int(estab), pcc_final=float(isl_cc.mean()), islands_coop_final=int((isl_cc >= 0.95).sum()),
                n_present_final=int((glob > 0).sum()), top_final=top, n_est_present=len(est_present),
                winners_carrier=all(pr['est'][k] or not pr['selfc'][k] or pr['allc'][k] for k in range(K) if glob[k] > 0),
                both_entries_first=int(baf), merges=[int(x) for x in merges],
                entries_alive_final=dict(e0=bool(any(glob[k] > 0 and ent[k] == 1 for k in range(K))),
                                         e5=bool(any(glob[k] > 0 and ent[k] == 2 for k in range(K))),
                                         both=bool(any(glob[k] > 0 and ent[k] == 3 for k in range(K)))),
                trace_cc=[float(x) for x in tr[::10]], time_s=time.time() - t)


def cmd_lottery(a):
    jobs = [(arm, prior, rep, a.Nisl, a.I, a.mN, a.gens) for arm, prior in [x.split(':') for x in a.cells] for rep in range(a.runs)]
    path = os.path.join(OUT, 'lottery_%s.json' % a.out)
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {(r['arm'], r['prior'], r['rep']) for r in rows}
    jobs = [j for j in jobs if (j[0], j[1], j[2]) not in done]
    nw = workers_allowed(a.workers)
    print('lottery jobs', len(jobs), 'workers', nw, flush=True)
    with Pool(nw) as pool:
        for r in pool.imap_unordered(lottery_job, jobs, chunksize=1):
            rows.append(r)
            json.dump(rows, open(path, 'w'), indent=1, default=str)
            print('%s %s rep %d: E1 %s@%d E2 %s@%d E3 %s@%d estab %d pcc %.3f top %s (%.0fs)' % (
                r['arm'], r['prior'], r['rep'], r['E1'], r['E1_gen'], r['E2'], r['E2_gen'], r['E3'], r['E3_gen'], r['establish_gen'],
                r['pcc_final'], r['top_final'][:2], r['time_s']), flush=True)


def cmd_ksens(a):
    """K sensitivity (after review): the executable class table recomputed at another K with V/K fixed (sources and
    lists rebuilt at that K; the K = 10^6 classes' representative spellings), compared cell by cell."""
    z, info = load_static(a.arm)
    A0 = z['A_class']; crep = [int(k) for k in z['class_rep']]
    names = class_names(info)
    out = {}
    nw = workers_allowed(a.workers)
    pr = class_props(A0, info, a.arm)
    est = set(np.nonzero(pr['est'])[0].tolist())
    for K2 in a.Ks:
        t0 = time.time()
        cat = CP.Catalogue(7, a.arm, K2)
        nc = len(crep)
        cdt = [cat.tau_dt[cat.tau[k]] for k in crep]
        catoms = [cat.tau_atoms[cat.tau[k]] for k in crep]
        creps = {i: (crep[i], crep[i]) for i in range(nc)}
        hasC = lambda u, aa: cat.has_entry(int(cat.tau[crep[u]]), aa)
        same_lists = sum(1 for i, k in enumerate(crep)
                         if [[e[0], C.show_script(e[1])] for e in (C.uncons(cat.tau_list[cat.tau[k]]) if cat.tau_list[cat.tau[k]] != 0 else [])]
                         == [list(x) for x in info['classes'][i]['list']])
        with Pool(nw, initializer=_init, initargs=(7, a.arm, K2)) as pool:
            exe = compute_tables(pool, cat, 'exec', cdt, catoms, creps, hasC)
        A, sa = compose(cdt, exe)
        A[np.arange(nc), np.arange(nc)] = sa
        diff = np.argwhere(A != A0)
        steps = np.array([x[4] for x in exe['steps']]) if exe['steps'] else np.zeros(0)
        V2 = K2 // 4
        dest = [(int(i), int(j)) for i, j in diff if int(i) in est and int(j) in est]
        out[str(K2)] = dict(K=K2, V=V2, n_classes=nc, lists_equal=same_lists, n_diff=int(len(diff)), n_diff_establisher_pairs=len(dest),
                            diff_examples=[(names[i], names[j], int(A0[i, j]), int(A[i, j])) for i, j in diff[:20]],
                            n_TO=int(sum(exe['n_to'].values())), n_at_cap=int((steps >= V2).sum()),
                            max_below_cap=int(steps[steps < V2].max()) if (steps < V2).any() else None,
                            time_s=time.time() - t0)
        np.save(os.path.join(OUT, 'ksens_A_%s_K%d.npy' % (a.arm, K2)), A)
        print(json.dumps(out[str(K2)])[:2000], flush=True)
    json.dump(out, open(os.path.join(OUT, 'ksens_%s.json' % a.arm), 'w'), indent=1)


def cmd_audit(a):
    """Soundness audit (S1, RE 3(a)): every check that returned T in the executable class table, against the actual
    play it certifies (pair checks against the class table, which is itself validated against whole plays; checks
    against the quotes of plain C and D against whole plays of the representative)."""
    z, info = load_static(a.arm)
    A = z['A_class']; crep = [int(k) for k in z['class_rep']]
    cat = CP.Catalogue(7, a.arm, 10 ** 6)
    nc = len(crep)
    cdt = [cat.tau_dt[cat.tau[k]] for k in crep]
    catoms = [cat.tau_atoms[cat.tau[k]] for k in crep]
    creps = {i: (crep[i], crep[i]) for i in range(nc)}
    hasC = lambda u, aa: cat.has_entry(int(cat.tau[crep[u]]), aa)
    nw = workers_allowed(a.workers)
    out = {}
    for kind in ('exec', 'ideal'):
        with Pool(nw, initializer=_init, initargs=(7, a.arm, 10 ** 6)) as pool:
            tb = compute_tables(pool, cat, kind, cdt, catoms, creps, hasC)
        nT = 0; bad = []
        for (md, aa), M in tb['CH'].items():
            for t, m in np.argwhere(M == 1):
                nT += 1
                want = 1 if aa == 'C' else 0
                act = A[t, m] if t != m else A[t, t]
                if act != want: bad.append(('pair', int(md), aa, int(t), int(m)))
        vsq = {}
        for (k, md, aa), d in tb['UV'].items():
            for t in np.nonzero(d['val'] == 1)[0]:
                nT += 1
                want = 'C' if aa == 'C' else 'D'
                if k == 'self':
                    act = 'C' if A[t, t] else 'D'
                else:
                    key = (int(t), k)
                    if key not in vsq:
                        L.CACHE.clear()
                        vsq[key] = L.play(cat.term(crep[t]), L.PROG_C if k == 'C' else L.PROG_D, cat.K)[0]
                    act = vsq[key]
                if act != want: bad.append((k, int(md), aa, int(t)))
        out[kind] = dict(n_true_checks=nT, false_atoms=len(bad), examples=bad[:10])
        print(kind, out[kind], flush=True)
    json.dump(out, open(os.path.join(OUT, 'audit_%s.json' % a.arm), 'w'), indent=1)


def _dt_of(cat, k):
    return cat.tau_dt[cat.tau[k]]


def _class_of_spelling(classes, n):
    out = np.full(n, -1, np.int64)
    for i, c in enumerate(classes):
        out[c['spellings']] = i
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('static')
    s.add_argument('--arm', default='P'); s.add_argument('--n', type=int, default=7); s.add_argument('--K', type=int, default=10 ** 6)
    s.add_argument('--workers', type=int, default=3)
    s.add_argument('--exec_sample', type=int, default=0); s.add_argument('--resume', type=int, default=0)
    s = sub.add_parser('chain')
    s.add_argument('--cells', nargs='+', default=['P:L'])
    s.add_argument('--N', type=int, nargs='+', default=[1000, 10000, 30000, 100000])
    s.add_argument('--twins', type=int, nargs='+', default=[1])
    s.add_argument('--theta', type=float, default=1e-14)
    s.add_argument('--table', default='exec')
    s.add_argument('--label', default='main')
    s.add_argument('--out', default='main')
    s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('validate')
    s.add_argument('--sample', type=int, default=2000)
    s = sub.add_parser('lottery')
    s.add_argument('--cells', nargs='+', default=['P:L'])
    s.add_argument('--runs', type=int, default=40)
    s.add_argument('--Nisl', type=int, default=100); s.add_argument('--I', type=int, default=64)
    s.add_argument('--mN', type=float, default=1.0); s.add_argument('--gens', type=int, default=2000)
    s.add_argument('--out', default='main')
    s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('audit'); s.add_argument('--arm', default='P'); s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('ksens')
    s.add_argument('--arm', default='P'); s.add_argument('--Ks', type=int, nargs='+', default=[300000, 3000000])
    s.add_argument('--workers', type=int, default=3)
    a = ap.parse_args()
    {'audit': cmd_audit, 'ksens': cmd_ksens, 'static': cmd_static, 'chain': cmd_chain, 'validate': cmd_validate, 'lottery': cmd_lottery}[a.cmd](a)
