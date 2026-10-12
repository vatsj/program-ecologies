"""Driver for provenance (predictions/2026-10-12-provenance.md, notes/provenance.md).

    python3 src/provenance_run.py static [--workers 3]   # extend milestone 5's universe for S-k appends (closure)
    python3 src/provenance_run.py osv [--workers 3]      # own-side validity, SPO table, S-nonself closure, Q and R
    python3 src/provenance_run.py validate               # notes §1.11 by code
    python3 src/provenance_run.py lottery --cells ...    # population cells
Raw arrays go to runs/provenance/ (npy/pkl, not committed); summaries to json.
"""
import argparse
import json
import os
import pickle
import sys
import time
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import lt_code as L
import lt_cert as C
import lt_genes as G
import lt_genes_pop as GP
import carrier_populations as CP
import provenance as PV

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'provenance')
M5 = os.path.join(ROOT, 'runs', 'lt_genes')
os.makedirs(OUT, exist_ok=True)
K = 10 ** 6
V = K // 4
PCAP = K // 4
SYNC = os.path.join(OUT, 'sync')


def log(*a):
    print(*a, flush=True)


def base_tables(pool, path=os.path.join(M5, 'static'), sync_dir=SYNC):
    """Milestone 5's universe and tables as a live Tables/Closure (nothing recomputed)."""
    st, meta = GP.load_static(path, mmap=True)
    U = GP.Universe(K, PCAP)
    U.scripts = list(meta['scripts']); U.sid = {k: i for i, k in enumerate(U.scripts)}
    U.sorigin = dict(meta['sorigin'])
    U.units = list(meta['units']); U.uid = {k: i for i, k in enumerate(U.units)}
    n = len(U.units)
    Tb = GP.Tables(U, pool, verbose=True, sync_dir=sync_dir)
    Tb.CH['C'][:n, :n] = st['CHC']; Tb.CH['D'][:n, :n] = st['CHD']; Tb.UVt[:n] = st['UVt']
    Tb.wild = dict(meta['wild']); Tb.prodC = dict(meta['prodC']); Tb.prodD = dict(meta['prodD'])
    Tb.prod_rep = dict(meta['prod_rep'])
    cl = GP.Closure(Tb, verbose=True)
    cl.single = dict(meta['single'])
    for m in ('S', 'C', 'CS', 'H'):
        cl.reach[m] = set(np.asarray(st['reach_' + m]).tolist())
    return st, meta, U, Tb, cl


def sk_missing_units(st, meta, U):
    """Units S-k can create that the lack-rule closure lacks: a candidate written while the list was empty, kept
    after the D step added δ (notes §1.2)."""
    P = np.asarray(st['PRODC']); PD = np.asarray(st['PD']); APP = np.asarray(st['APP'])
    Eu = np.asarray(meta['E_unit'])
    new = []
    for t in range(P.shape[0]):
        e = int(Eu[t]); d0 = int(PD[e])
        if d0 < 0 or d0 == e: continue
        for s in sorted(set(int(x) for x in P[t] if x >= 0)):
            if APP[d0, s] < 0:
                t_, cs, ds = U.units[d0]
                new.append((t, (s,), ds))
    return new


def _exec_prod_job(items):
    """Term-executed productions for new memo keys (cap timeouts of the executable producer)."""
    sys.setrecursionlimit(1000000)
    U = _EX['U']
    out = []
    for tag, key, u, v, rel in items:
        if len(L.CACHE) > 200000: L.CACHE.clear()
        t, cs, ds = U.units[u]
        px = G.Prog('u', U.bodies[t], 'H', [U.scripts[i][1] for i in cs], [U.scripts[i][1] for i in ds])
        if v is None:
            yt = L.PROG_D
        elif rel == 's':
            yt = px.term()
        else:
            t2, cs2, ds2 = U.units[v]
            yt = G.Prog('v', U.bodies[t2], 'C' if rel == 'w' else 'H', [U.scripts[i][1] for i in cs2],
                        [U.scripts[i][1] for i in ds2]).term()
        s, n, oc = G.produce_term(px.term(), yt, 'C' if tag == 'C' else 'D', V, K, PCAP, K)
        out.append((tag, key, oc, n))
    return out


_EX = {}


def _exinit(units, scripts):
    sys.setrecursionlimit(1000000)
    U = GP.Universe(K, PCAP)
    U.scripts = list(scripts); U.sid = {k: i for i, k in enumerate(U.scripts)}
    U.units = list(units); U.uid = {k: i for i, k in enumerate(U.units)}
    _EX['U'] = U


def cmd_static(a):
    t0 = time.time()
    nw = min(3, a.workers)
    with Pool(nw, initializer=GP._winit, initargs=(K, PCAP, SYNC)) as pool:
        st, meta, U, Tb, cl = base_tables(pool)
        n0 = len(U.units)
        old_keys = {('C', k) for k in meta['prodC']} | {('D', k) for k in meta['prodD']}
        new = sk_missing_units(st, meta, U)
        log('S-k units missing from the lack-rule universe:', len(new))
        for key in new:
            u = U.unit(*key)
            cl.reach['S'].add(u)
        Tb._grow()
        rounds = cl.run()
        log('closure converged after %d rounds: units %d (+%d), scripts %d, new checks %d (%.0fs)' % (
            rounds, len(U.units), len(U.units) - n0, len(U.scripts), Tb.n_checks, time.time() - t0))
        st2 = GP.finalize(cl, verbose=True)
        new_keys = [(tag, key) for tag, key in list(Tb.prod_rep.keys()) if (tag, key) not in old_keys]
        log('new production memo keys', len(new_keys))
        GP.save_static(st2, U, Tb, cl, os.path.join(OUT, 'static'))
    # the executable producer on the new keys' representatives
    items = []
    for tag, key in new_keys:
        u, v, rel = Tb.prod_rep[(tag, key)]
        items.append((tag, key, int(u), None if v is None else int(v), rel))
    res = []
    if items:
        with Pool(nw, initializer=_exinit, initargs=(U.units, U.scripts)) as pool:
            for out in pool.imap_unordered(_exec_prod_job, [items[i::nw * 4] for i in range(nw * 4)]):
                res.extend(out)
    ex = json.load(open(os.path.join(M5, 'prod_exec.json')))
    ex += [[tag, list(key), oc] for tag, key, oc, n in res]
    json.dump(ex, open(os.path.join(OUT, 'prod_exec.json'), 'w'))
    rep = dict(n_units_m5=n0, n_new_sk=len(new), n_units=len(U.units), n_scripts=len(U.scripts),
               rounds=rounds, new_checks=int(Tb.n_checks), new_prod_keys=len(new_keys),
               new_prod_cap_timeouts=sum(1 for z in res if z[2] in ('capTO', 'fuelTO')), time_s=time.time() - t0)
    json.dump(rep, open(os.path.join(OUT, 'static_ext.json'), 'w'), indent=1)
    log(json.dumps(rep))


# ------------------------------------------------------------------ own-side validity and the SPO audit
_OS = {}


def _osinit(units, scripts):
    sys.setrecursionlimit(1000000)
    U = GP.Universe(K, PCAP)
    U.scripts = list(scripts); U.sid = {k: i for i, k in enumerate(U.scripts)}
    U.units = list(units); U.uid = {k: i for i, k in enumerate(U.units)}
    _OS['U'] = U
    _OS['chk'] = CP.IdealCheck()
    _OS['terms'] = {}


def _term(key, marker):
    tm = _OS['terms'].get((key, marker))
    if tm is None:
        tm = GP.key_term(_OS['U'], key, marker)
        if len(_OS['terms']) > 50000: _OS['terms'].clear()
        _OS['terms'][(key, marker)] = tm
    return tm


def osv_root(u_key, s, partner, rel):
    """OSV of x' = u + s at the root against the partner (rel 's' self root, 'w' twin of u, 'd' distinct unit)."""
    t, cs, ds = u_key
    xk = (t, tuple(cs) + (s,), ds)                    # the would-be self (cs is empty under a lack rule)
    xt = _term(xk, 'H')
    if rel == 's':
        yt = xt
    elif rel == 'w':
        yt = _term(u_key, 'C')
    else:
        yt = _term(partner, 'H')
    chk = _OS['chk']
    if len(chk.memo) > 300000: chk.clear()
    ok, uS = PV.own_side_valid(chk, xt, yt, V, K)
    return ok


def _osv_job(items):
    U = _OS['U']
    out = []
    for t, code, s, u, v, rel in items:
        ok = osv_root(U.units[u], s, None if v is None else U.units[v], rel)
        out.append((t, code, s, ok))
    return out


def _osv_sample_job(items):
    """OSV on arbitrary (u, v, rel) pairs (validation of the signature reduction)."""
    U = _OS['U']
    out = []
    for t, code, s, u, v, rel in items:
        ok = osv_root(U.units[u], s, None if v is None else U.units[v], rel)
        out.append((t, code, s, u, v, rel, ok))
    return out


WHICH = {'ext': ('static', ''), 'gate': ('static_gate', '_gate')}


def load_ext(which='ext'):
    st, meta = GP.load_static(os.path.join(OUT, WHICH[which][0]))
    return st, meta


def sfx(which, name):
    b, e = os.path.splitext(name)
    return os.path.join(OUT, b + WHICH[which][1] + e)


def patched(st, path=os.path.join(OUT, 'prod_exec.json')):
    PRODC = np.array(st['PRODC']); PD = np.array(st['PD'])
    ex = json.load(open(path))
    capD = set()
    for tag, key, oc in ex:
        if oc not in ('capTO', 'fuelTO'): continue
        if tag == 'C': PRODC[key[0], key[1]] = -3
        else: capD.add((key[0], key[1]))
    utau, code = np.asarray(st['utau']), np.asarray(st['PDCODE'])
    for u in np.nonzero(code >= 0)[0].tolist():
        if (int(utau[u]), int(code[u])) in capD: PD[u] = -3
    return PRODC, PD


def cmd_osv(a):
    t0 = time.time()
    st, meta = load_ext(a.which)
    units, scripts = meta['units'], meta['scripts']
    T = st['PRODC'].shape[0]
    ns = len(scripts)
    P = np.asarray(st['PRODC'])
    BLC = np.asarray(st['BLC']); utau = np.asarray(st['utau'])
    O = np.asarray(st['O'])
    # scripts per run tree: producible, or held by any unit of the tree in the universe
    St = [set() for _ in range(T)]
    for t in range(T):
        St[t] |= set(int(x) for x in P[t] if x >= 0)
    for u, (t, cs, ds) in enumerate(units):
        St[t] |= set(cs)
    codes = {}
    for (t, c), _sid in meta['prodC'].items():
        codes.setdefault(t, []).append(c)
    items = []
    for t in range(T):
        for c in codes.get(t, []):
            u, v, rel = meta['prod_rep'][('C', (t, c))]
            for s in St[t]:
                if scripts[s][0] != 'C': continue
                items.append((t, c, s, int(u), None if v is None else int(v), rel))
    log('OSV computations', len(items))
    OSV = np.full((T, ns, 64), -1, np.int8)
    nw = min(3, a.workers)
    rng = np.random.default_rng(20261012)
    with Pool(nw, initializer=_osinit, initargs=(units, scripts)) as pool:
        chunks = [items[i::nw * 16] for i in range(nw * 16)]
        done = 0
        for out in pool.imap_unordered(_osv_job, chunks):
            for t, c, s, ok in out:
                OSV[t, s, c] = 1 if ok else 0
            done += len(out)
            log('  osv %d / %d (%.0fs)' % (done, len(items), time.time() - t0))
        # validation of the signature reduction: random (u, v) pairs of reachable S units lacking C
        import lt_genes_kern as KN
        lackC = [u for u in st['reach_S'].tolist() if BLC[u, 0] < 0]
        samp = []
        CHD = st['CHD']; UVt = st['UVt']; BLD = st['BLD']
        for _ in range(a.nsample):
            u = int(rng.choice(lackC)); v = int(rng.choice(O))
            rel = 1 if v == u else 0
            if rng.random() < 0.1: v, rel = u, 2
            code = int(KN.sig_code(u, v, rel, st['utau'], st['KIND'], st['NAT'], CHD, UVt, st['BLC'], BLD))
            t = int(utau[u])
            for s in St[t]:
                if scripts[s][0] != 'C': continue
                samp.append((t, code, s, u, v, {0: 'd', 1: 'w', 2: 's'}[rel]))
        mism = []; nchk = 0
        for out in pool.imap_unordered(_osv_sample_job, [samp[i::nw * 4] for i in range(nw * 4)]):
            for t, code, s, u, v, rel, ok in out:
                ref = OSV[t, s, code]
                if ref < 0: continue
                nchk += 1
                if bool(ref) != ok: mism.append([t, code, s, u, v, rel, int(ref), ok])
    log('OSV validation: %d compared, %d mismatches' % (nchk, len(mism)))
    np.save(sfx(a.which, 'OSV.npy'), OSV)
    SPO = PV.spo_table(OSV)
    np.save(sfx(a.which, 'SPO.npy'), SPO)
    # tactic outputs valid at their own codes
    own_bad = []
    for t in range(T):
        for c in codes.get(t, []):
            s = P[t, c]
            if s >= 0 and OSV[t, s, c] != 1: own_bad.append([t, c, int(s)])
    rep = dict(n_osv=len(items), n_validated=nchk, n_mismatch=len(mism), mismatches=mism[:30],
               tactic_not_valid_at_own_code=len(own_bad), own_bad=own_bad[:30], time_s=time.time() - t0)
    json.dump(rep, open(sfx(a.which, 'osv.json'), 'w'), indent=1)
    log(json.dumps({k: v for k, v in rep.items() if k not in ('mismatches', 'own_bad')}))


# ------------------------------------------------------------------ sets: SPO pairs, the S-nonself closure, Q, R
def catalogue():
    cat = CP.Catalogue(7, 'P', K)
    mu = cat.spelling_mass('L')
    return cat, mu / mu.sum()


def cmd_sets(a):
    t0 = time.time()
    st, meta = load_ext(a.which)
    units, scripts = meta['units'], meta['scripts']
    cat, mu = catalogue()
    names = [cat.name(k) for k in range(len(cat.spell))]
    T = cat.T
    tau = cat.tau
    mt = np.bincount(tau, weights=mu, minlength=T)
    A = np.asarray(st['A']); selfa = np.asarray(st['selfa']); O = np.asarray(st['O'])
    OSV = np.load(sfx(a.which, 'OSV.npy')); SPO = np.load(sfx(a.which, 'SPO.npy'))
    PRODC, PD = patched(st, sfx(a.which, 'prod_exec.json'))
    Hu, Eu = np.asarray(meta['H_unit']), np.asarray(meta['E_unit'])
    # identity units over the universe (milestone 5's definition)
    ident = np.zeros(len(units), bool)
    ident[PV.identity_units(set(O.tolist()), A, selfa)] = True
    # S-nonself closure and its identity units
    reach = np.zeros(len(units), np.bool_)
    PV.nonself_closure(Eu.astype(np.int64), O.astype(np.int64), np.asarray(st['utau']), np.asarray(st['KIND']),
                       np.asarray(st['NAT']), np.asarray(st['CHD']), np.asarray(st['UVt']), np.asarray(st['BLC']),
                       np.asarray(st['BLD']), PRODC, PD, np.asarray(st['APP']), reach)
    Rn = set(np.nonzero(reach)[0].tolist())
    idn = PV.identity_units(Rn, A, selfa)
    Qt = sorted(set(int(units[u][0]) for u in idn))
    Q = np.nonzero(np.isin(tau, Qt))[0]
    # receiving set: the prudent open core analogue (H units)
    k_cb = names.index('if(CHK(them,me,C),C,D)'); k_c = names.index('C'); k_d = names.index('D')
    ucb, ucc, ud = int(Hu[tau[k_cb]]), int(Hu[tau[k_c]]), int(Hu[tau[k_d]])
    Rt = []
    for t in range(T):
        u = int(Hu[t])
        if selfa[u] == 1 and A[u, ud] == 0 and A[u, ucb] == 1 and A[ucb, u] == 1 and A[u, ucc] == 0:
            Rt.append(t)
    R = np.nonzero(np.isin(tau, Rt))[0]
    # open units (mutual with CB-H), capable trees (some non-self production)
    openu = np.zeros(len(units), bool)
    openu[O] = (A[O, ucb] == 1) & (A[ucb, O] == 1)
    capable = np.array([any(x >= 0 for x in PRODC[t, :25]) or any(x == -3 for x in PRODC[t, :25]) for t in range(T)])
    only_self = np.array([any(x >= 0 for x in PRODC[t, 25:50]) and not any(x >= 0 for x in PRODC[t, :25]) for t in range(T)])
    # SPO pairs and their trees
    spo_pairs = [(int(t), int(s)) for t, s in zip(*np.nonzero(SPO))]
    spo_trees = sorted(set(t for t, s in spo_pairs))
    # which SPO pairs each rule can write: self codes (S-self etc.) vs non-self codes (S-nonself)
    write_self = sorted({(t, int(PRODC[t, c])) for t in range(T) for c in range(25, 50) if PRODC[t, c] >= 0 and SPO[t, PRODC[t, c]]})
    write_non = sorted({(t, int(PRODC[t, c])) for t in range(T) for c in range(25) if PRODC[t, c] >= 0 and SPO[t, PRODC[t, c]]})
    # units holding an SPO script
    spo_unit = np.zeros(len(units), bool)
    for u, (t, cs, ds) in enumerate(units):
        spo_unit[u] = len(cs) > 0 and all(SPO[t, s] for s in cs)        # only self-play-only C entries
    held_spo_pairs = sorted({(int(units[u][0]), s) for u in O.tolist() for s in units[u][1] if SPO[units[u][0], s]})
    np.savez(sfx(a.which, 'sets.npz'), ident=ident, reach_nonself=reach, Q=Q, R=R, Qt=np.array(Qt), Rt=np.array(Rt),
             openu=openu, capable=capable, only_self=only_self, spo_unit=spo_unit, mu=mu, tau=tau)
    show = lambda ts: [(names[cat.members[t][0]], round(float(mt[t]), 7)) for t in sorted(ts, key=lambda t: -mt[t])]
    rep = dict(
        n_units=len(units), n_ident_universe=int(ident.sum()), nonself_reach=len(Rn), nonself_ident_units=len(idn),
        Q_trees=show(Qt), Q_spellings=len(Q), Q_mass=float(mu[Q].sum()), Q_copies_per_run=float(6400 * mu[Q].sum()),
        R_trees=show(Rt), R_spellings=len(R), R_mass=float(mu[R].sum()),
        spo_pairs=len(spo_pairs), spo_trees=len(spo_trees), spo_tree_mass=float(mt[spo_trees].sum()),
        spo_written_at_self_codes=len(write_self), spo_written_at_nonself_codes=len(write_non),
        spo_written_at_nonself=[(names[cat.members[t][0]], C.show_script(scripts[s][1])) for t, s in write_non[:20]],
        held_spo_pairs_in_universe=len(held_spo_pairs),
        spo_trees_heaviest=show(spo_trees)[:25],
        spo_self_trees_mass=float(mt[sorted(set(t for t, s in write_self))].sum()),
        only_self_trees=int(only_self.sum()), only_self_mass=float(mt[only_self].sum()),
        capable_trees=int(capable.sum()), capable_mass=float(mt[capable].sum()),
        open_units=int(openu.sum()), spo_units=int(spo_unit.sum()), time_s=time.time() - t0)
    json.dump(rep, open(sfx(a.which, 'sets.json'), 'w'), indent=1)
    log(json.dumps(rep, indent=1))


# ------------------------------------------------------------------ the gate cell's universe (notes §1.9)
class GateClosure:
    """Units reachable from the empty units under S-gate alone (the gate = one's own full check against the partner;
    on F or TO, produce against the partner and append a script not yet held; the D step while lacking D), seeded with
    the cached tables so only missing entries are computed."""

    def __init__(self, Tb, cl, Eunits, budget_s):
        self.Tb, self.cl, self.U = Tb, cl, Tb.U
        self.reach = set(int(u) for u in Eunits)
        self.budget_s = budget_s
        self.t0 = time.time()

    def run(self, max_rounds=12):
        Tb, U, cl = self.Tb, self.U, self.cl
        for rnd in range(max_rounds):
            t1 = time.time()
            n_before = len(self.reach)
            O = sorted(self.reach)
            Oa = np.asarray(O, np.int64)
            Tb._grow()
            Tb.ensure_uv(O)
            rowsD = [u for u in O if GP.has_kind(U, u, (1, 1, 0)) and U.has_entry(u, 'D')]
            colsD = [u for u in O if GP.has_kind(U, u, (0, 1, 0))]
            cl._ensure_sub('D', rowsD, colsD, O)
            # gate rows: every unit with a C entry against every reachable unit (the diagonal is the twin)
            rowsC = [u for u in O if U.has_entry(u, 'C')]
            CHC = Tb.CH['C']
            tl, ml = [], []
            for u in rowsC:
                miss = Oa[CHC[u, Oa] < 0]
                if len(miss): tl.append(np.full(len(miss), u, np.int64)); ml.append(miss)
            if tl:
                Tb.ensure_pairs('C', np.concatenate(tl), np.concatenate(ml), label='(gate rows %d)' % len(rowsC))
            if time.time() - self.t0 > self.budget_s:
                raise TimeoutError('gate closure over budget in round %d' % rnd)
            UVA, has = Tb.uv_arrays()
            CHC = Tb.CH['C']
            items = []
            plan = {}
            for u in O:
                t = U.units[u][0]
                vs = np.concatenate([Oa, [u]])
                relc = np.where(vs == u, 1, 0); relc[-1] = 2
                if has['C'][u]:
                    g = CHC[u, vs].astype(np.int64)
                    g[-1] = Tb.UVt[u, GP.UVI[('C', 'self')]]
                    need = g != 1
                else:
                    need = np.ones(len(vs), bool)
                if not need.any():
                    plan[u] = []; continue
                codes = Tb.sig_codes_C(u, vs, relc, UVA, has)
                uc, first = np.unique(codes[need], return_index=True)
                idx = np.nonzero(need)[0][first]
                plan[u] = [int(c) for c in uc]
                for c, j in zip(uc.tolist(), idx.tolist()):
                    rel = 's' if relc[j] == 2 else ('w' if relc[j] == 1 else 'd')
                    items.append((Tb.prodC, (t, c), u, int(vs[j]), rel, 'C'))
            Tb.run_productions(items)
            outs_all = set()
            for u, codes in plan.items():
                t, cs, ds = U.units[u]
                outs = {u}
                for c in codes:
                    s = Tb.prodC[(t, c)]
                    if s >= 0 and s not in cs:
                        if len(cs) >= GP.LMAX: raise RuntimeError('C block over LMAX')
                        outs.add(U.unit(t, cs + (s,), ds))
                outs_all |= outs
            Tb._grow()
            Tb.ensure_uv(sorted(outs_all))
            ditems = []
            for u2 in sorted(outs_all):
                if not U.has_entry(u2, 'D'):
                    ditems.append((Tb.prodD, (U.units[u2][0], Tb.sig_code_D(u2)), u2, None, 'D', 'D'))
            Tb.run_productions(ditems)
            new = set()
            for u2 in outs_all:
                if not U.has_entry(u2, 'D'):
                    s = Tb.prodD[(U.units[u2][0], Tb.sig_code_D(u2))]
                    new.add(U.append(u2, s) if s >= 0 else u2)
                new.add(u2)
            self.reach |= new
            Tb._grow()
            log('  gate closure round %d: reach %d, units %d, scripts %d (%.0fs; total %.0fs)' % (
                rnd, len(self.reach), len(U.units), len(U.scripts), time.time() - t1, time.time() - self.t0))
            if len(self.reach) == n_before:
                return rnd
        raise RuntimeError('gate closure did not converge')


def cmd_gate_static(a):
    t0 = time.time()
    nw = min(3, a.workers)
    sync = os.path.join(OUT, 'sync_gate')
    with Pool(nw, initializer=GP._winit, initargs=(K, PCAP, sync)) as pool:
        st, meta, U, Tb, cl = base_tables(pool, path=os.path.join(OUT, 'static'), sync_dir=sync)
        n0 = len(U.units)
        old_keys = {('C', k) for k in meta['prodC']} | {('D', k) for k in meta['prodD']}
        gc = GateClosure(Tb, cl, meta['E_unit'], a.budget * 3600)
        try:
            rounds = gc.run()
            ok = True
        except TimeoutError as e:
            log(str(e)); ok = False; rounds = -1
        rep = dict(converged=ok, rounds=rounds, reach=len(gc.reach), units=len(U.units), units_added=len(U.units) - n0,
                   scripts=len(U.scripts), checks=int(Tb.n_checks), check_time_s=Tb.t_checks, time_s=time.time() - t0,
                   multi_C_units=sum(1 for u in gc.reach if len(U.units[u][1]) > 1),
                   max_C_block=max(len(U.units[u][1]) for u in gc.reach))
        log(json.dumps(rep))
        json.dump(rep, open(os.path.join(OUT, 'gate_static.json'), 'w'), indent=1)
        if not ok: return
        cl.reach = {'S': set(gc.reach), 'C': set(), 'CS': set(), 'H': set()}
        st2 = GP.finalize(cl, verbose=True)
        new_keys = [(tag, key) for tag, key in list(Tb.prod_rep.keys()) if (tag, key) not in old_keys]
        GP.save_static(st2, U, Tb, cl, os.path.join(OUT, 'static_gate'))
    items = []
    for tag, key in new_keys:
        u, v, rel = Tb.prod_rep[(tag, key)]
        items.append((tag, key, int(u), None if v is None else int(v), rel))
    res = []
    if items:
        with Pool(nw, initializer=_exinit, initargs=(U.units, U.scripts)) as pool:
            for out in pool.imap_unordered(_exec_prod_job, [items[i::nw * 4] for i in range(nw * 4)]):
                res.extend(out)
    ex = json.load(open(os.path.join(OUT, 'prod_exec.json')))
    ex += [[tag, list(key), oc] for tag, key, oc, n in res]
    json.dump(ex, open(os.path.join(OUT, 'prod_exec_gate.json'), 'w'))
    rep.update(new_prod_keys=len(new_keys), new_prod_cap_timeouts=sum(1 for z in res if z[2] in ('capTO', 'fuelTO')),
               time_s=time.time() - t0)
    json.dump(rep, open(os.path.join(OUT, 'gate_static.json'), 'w'), indent=1)
    log(json.dumps(rep))


# ------------------------------------------------------------------ hand scripts by whole runs of the term (§1.4)
NAMED = {'CB': 'if(CHK(them,me,C),C,D)', 'CB1': 'if(CHK(them,me,C),if(CHK(me,them,C),C,D),D)',
         'AND2': 'if(and(CHK(me,them,C),CHK(them,me,C)),C,D)', 'MM': 'if(and(CHK(me,me,C),CHK(me,them,C)),C,D)',
         'CBP4': 'if(CHK(them,me,C),if(CHK(them,^D,D),C,D),D)', 'CBPr': 'if(CHK(them,^D,D),if(CHK(them,me,C),C,D),D)',
         'TwinD': 'if(or(CHK(me,me,D),CHK(me,them,D)),D,C)'}
TWIN = {'CB': 'if(not(CHK(them,me,C)),D,C)', 'CB1': 'if(and(CHK(them,me,C),CHK(me,them,C)),C,D)',
        'AND2': 'if(CHK(me,them,C),if(CHK(them,me,C),C,D),D)', 'CBP4': 'if(and(CHK(them,me,C),CHK(them,^D,D)),C,D)',
        'CBPr': 'if(and(CHK(them,^D,D),CHK(them,me,C)),C,D)'}
DISTINCT = {'CB': 'CB1'}
_PC = {}


def named_prog(name_or_sexpr, rule):
    """An empty program (no marker: the quote is code + list) of a named spelling."""
    if 'cat' not in _PC:
        cat = CP.Catalogue(7, 'P', K)
        _PC['cat'] = cat
        _PC['idx'] = {cat.name(k): k for k in range(len(cat.spell))}
    cat = _PC['cat']
    s = NAMED.get(name_or_sexpr, name_or_sexpr)
    k = _PC['idx'][s]
    body = CP.body_term(cat.sexprs[cat.spell[k]['i']], V, K)
    return G.Prog(s, body, None, (), ())


def first_partner(cname, ptype):
    if ptype == 'self': return None
    if ptype == 'twin': return named_prog(TWIN[cname], 'S-self') if cname in TWIN else None
    if ptype == 'distinct': return named_prog(DISTINCT.get(cname, 'CB'), 'S-self')
    if ptype == 'C': return named_prog('C', 'S-self')
    if ptype == 'D': return named_prog('D', 'S-self')


def _pairs_job(job):
    """One focal rule on a named carrier against a first-partner type, E encounters (the partner in mode S-self,
    except a self partner, which is the focal's own quote: one production)."""
    sys.setrecursionlimit(1000000)
    rule, cname, ptype, E, shadow = job
    x = named_prog(cname, rule)
    y = first_partner(cname, ptype)
    if ptype != 'self' and y is None:
        return dict(rule=rule, carrier=cname, ptype=ptype, skipped=True)
    sx, sy = PV.TermState(), PV.TermState()
    chk = CP.IdealCheck()
    hist = []
    if rule in ('S-2', 'S-3', 'S-3 strict'):
        # a window needs source-distinct partners: the first-partner type, then a distinct carrier, then D, then C
        seq = [ptype, 'distinct' if ptype != 'distinct' else 'twin', 'D' if ptype != 'D' else 'C', 'C' if ptype != 'C' else 'D']
        for e, pt in enumerate(seq[:E]):
            if len(L.CACHE) > 200000: L.CACHE.clear()
            if pt == 'self':
                r = PV.term_encounter(x, x, rule, rule, sx, sx, K, V, PCAP, self_play=True, chk=chk)
                x = r['nx']
            else:
                y = first_partner(cname, pt) or named_prog('CB1', None)
                r = PV.term_encounter(x, y, rule, 'H', sx, PV.TermState(), K, V, PCAP, chk=chk)
                x = r['nx']
            hist.append(dict(partner=pt, ax=r['ax'], ay=r['ay'], C=[C.show_script(s) for s in x.cseq],
                             D=[C.show_script(s) for s in x.dseq], ev=[list(map(str, z)) for z in r['ex']]))
        return dict(rule=rule, carrier=cname, ptype=ptype, shadow=shadow, hist=hist)
    for e in range(E):
        if len(L.CACHE) > 200000: L.CACHE.clear()
        if ptype == 'self':
            r = PV.term_encounter(x, x, rule, rule, sx, sx, K, V, PCAP, self_play=True, shadow=(shadow, shadow), chk=chk)
            x = r['nx']
        else:
            r = PV.term_encounter(x, y, rule, 'S-self', sx, sy, K, V, PCAP, shadow=(shadow, None), chk=chk)
            x, y = r['nx'], r['ny']
        hist.append(dict(ax=r['ax'], ay=r['ay'], C=[C.show_script(s) for s in x.cseq], D=[C.show_script(s) for s in x.dseq],
                         ev=[list(map(str, z)) for z in r['ex']]))
    return dict(rule=rule, carrier=cname, ptype=ptype, shadow=shadow, hist=hist)


def cmd_pairs(a):
    t0 = time.time()
    rules = ['S-self', 'S-nonself', 'S-self-delayed', 'S-2', 'S-3', 'S-3 strict', 'S-gate+cache']
    jobs = []
    for rule in rules:
        for cname in NAMED:
            for ptype in ('self', 'twin', 'distinct', 'C', 'D'):
                jobs.append((rule, cname, ptype, 4, True if rule == 'S-self-delayed' else None))
    rows = []
    with Pool(min(3, a.workers)) as pool:
        for r in pool.imap_unordered(_pairs_job, jobs):
            rows.append(r)
    rows.sort(key=lambda r: (rules.index(r['rule']), list(NAMED).index(r['carrier']), r['ptype']))
    json.dump(rows, open(os.path.join(OUT, 'pairs.json'), 'w'), indent=1)
    for r in rows:
        if r.get('skipped'): continue
        log('%-15s %-6s %-8s %s' % (r['rule'], r['carrier'], r['ptype'], ' | '.join('%s%s C%s' % (h['ax'], h['ay'], h['C']) for h in r['hist'])))
    log('pairs done (%.0fs)' % (time.time() - t0))


# ------------------------------------------------------------------ validation by code (notes §1.11)
def kernel_one(LS, rule, u, v, rel, shadow_nonself=False, prule=None):
    """One side of one encounter by the kernel's `side` on a two-individual harness.  Returns the new unit."""
    from numba.typed import Dict
    from numba import types
    st = LS['st']
    d = Dict.empty(key_type=types.int64, value_type=types.int64)
    cap = 8
    tunit = np.zeros(cap, np.int64); trule = np.zeros(cap, np.int64); tsp = np.zeros(cap, np.int64)
    tanc = np.zeros(cap, np.int64)
    sp_u = 0
    sp_v = 0 if rel == 2 else (1 if rel == 1 else (0 if st['utau'][u] == st['utau'][v] else 1))
    k, nt = PV.make_type(d, tunit, trule, tsp, tanc, 0, u, rule, sp_u, 0)
    j, nt = PV.make_type(d, tunit, trule, tsp, tanc, nt, v, rule if prule is None else prule, sp_v, 0)
    if rel == 2: j = k
    ntv = np.array([nt], np.int64)
    I, N = 1, 2
    wn = np.zeros((I, N), np.int64); wenc = np.zeros((I, N), np.int64)
    wsp = np.zeros((I, N, 3), np.int64); wcode = np.zeros((I, N, 3), np.int64); wsid = np.zeros((I, N, 3), np.int64)
    ckey = np.zeros((I, N, PV.CACHE_CAP), np.int64); cval = np.zeros((I, N, PV.CACHE_CAP), np.int64)
    ncache = np.zeros((I, N), np.int64); plog = -np.ones((I, N, 5), np.int64)
    ctr = np.zeros((PV.NRULE, PV.NCTR), np.int64); steps = np.zeros(PV.NRULE)
    err = np.zeros(1, np.int64)
    shadow_sp = 7 if shadow_nonself else sp_u
    k2 = PV.side(0, 0, k, j, PV.relation(k, j, tunit, tsp), shadow_sp, d, tunit, trule, tsp, tanc, ntv, cap,
                 st['utau'], st['BLC'], st['BLD'], st['SINGLE'], st['APP'], LS['PRODC'], LS['PD'], st['KIND'],
                 st['NAT'], st['CHC'], st['CHD'], st['UVt'], LS['OSV'], LS['SPO'], LS['COSTS'], ctr, steps, wn, wenc,
                 wsp, wcode, wsid, ckey, cval, ncache, plog, np.zeros(1), err)
    if err[0] != 0:
        return -100 - int(err[0])
    return int(tunit[k2])


def unit_prog_nm(U, u, which=0):
    """Unit u as a marker-free program on its run tree's spelling number `which`."""
    t, cs, ds = U.units[u]
    cat = U.cat
    m = cat.members[t]
    if which >= len(m): return None
    k = m[which]
    body = CP.body_term(cat.sexprs[cat.spell[k]['i']], V, K)
    return G.Prog('u%d' % u, body, None, [U.scripts[i][1] for i in cs], [U.scripts[i][1] for i in ds])


_VA = {}


def _vainit():
    sys.setrecursionlimit(1000000)
    st, meta = load_ext()
    U = GP.Universe(K, PCAP)
    U.scripts = list(meta['scripts']); U.sid = {k: i for i, k in enumerate(U.scripts)}
    U.units = list(meta['units']); U.uid = {k: i for i, k in enumerate(U.units)}
    _VA['U'] = U


def _va_job(items):
    U = _VA['U']
    out = []
    for rule, u, v, rel, shadow in items:
        if len(L.CACHE) > 200000: L.CACHE.clear()
        x = unit_prog_nm(U, u, 0)
        if rel == 2:
            y = x
        elif rel == 1:
            y = unit_prog_nm(U, v, 1)
        else:
            y = unit_prog_nm(U, v, 0)
        if y is None:
            out.append((rule, u, v, rel, shadow, None)); continue
        st_ = PV.TermState()
        nx, ev = PV.term_side(x, y, rule, st_, K, V, PCAP, shadow_nonself=shadow)
        key = (U.units[u][0], tuple(U.sid.get(('C', s), -9) for s in nx.cseq), tuple(U.sid.get(('D', s), -9) for s in nx.dseq))
        out.append((rule, u, v, rel, shadow, [list(key[1]), list(key[2]), [list(map(str, e)) for e in ev]]))
    return out


def cmd_validate(a):
    t0 = time.time()
    LS = lot_static('ext')
    st, meta = LS['st'], LS['meta']
    units = meta['units']
    rng = np.random.default_rng(20261012)
    O = np.asarray(st['O']); BLC = np.asarray(st['BLC'])
    rep = {}
    # 1. the settled-skip is exact (identical trajectories with and without skipping)
    sk = []
    for cell in ('Sself', 'Snon', 'S3', 'S3strict', 'mixed', 'Cdonor', 'Sdel', 'CSnon', 'H', 'ablation'):
        Rs = []
        for skip in (True, False):
            R = Run(cell, 997); R.skip = skip
            R.advance(a.skipgens)
            Rs.append(R)
        same = bool((Rs[0].slots == Rs[1].slots).all() and (Rs[0].tunit[:Rs[0].ntv[0]] == Rs[1].tunit[:Rs[1].ntv[0]]).all())
        sk.append([cell, same, int(Rs[0].ntv[0])])
        log('skip exactness %s: %s' % (cell, same))
    rep['skip_exact'] = sk
    # 2. kernel transitions = term-executed transitions, per rule, on sampled encounters
    lack_S = [u for u in st['reach_S'].tolist() if BLC[u, 0] < 0]
    lack_C = [u for u in st['reach_C'].tolist() if BLC[u, 0] < 0]
    items = []
    for rule in ('S-self', 'S-nonself', 'S-self-delayed', 'CS-nonself', 'C'):
        pool_u = lack_C if rule == 'C' else lack_S
        for z in range(a.nenc):
            u = int(rng.choice(pool_u)); v = int(rng.choice(O)); rel = 0
            r_ = rng.random()
            if r_ < 0.15: v, rel = u, 2
            elif r_ < 0.25: v, rel = u, 1
            shadow = bool(rng.random() < 0.5) if rule == 'S-self-delayed' else None
            items.append((rule, u, v, rel, shadow))
    nw = min(3, a.workers)
    res = []
    with Pool(nw, initializer=_vainit) as pool:
        for out in pool.imap_unordered(_va_job, [items[i::nw * 8] for i in range(nw * 8)]):
            res.extend(out)
    mism = []
    n = 0
    for rule, u, v, rel, shadow, got in res:
        if got is None: continue
        n += 1
        ku = kernel_one(LS, PV.RULE_OF[rule], u, v, rel, bool(shadow))
        kk = units[ku] if ku >= 0 else None
        if kk is None or list(kk[1]) != got[0] or list(kk[2]) != got[1]:
            mism.append([rule, u, v, rel, shadow, None if kk is None else [list(kk[1]), list(kk[2])], got[:2], got[2][:6]])
    rep['transitions'] = dict(n=n, n_mismatch=len(mism), mismatches=mism[:30])
    log('transitions: %d compared, %d mismatches' % (n, len(mism)))
    rep['time_s'] = time.time() - t0
    json.dump(rep, open(os.path.join(OUT, 'validate.json'), 'w'), indent=1, default=str)


def _vagate_init():
    sys.setrecursionlimit(1000000)
    st, meta = load_ext('gate')
    U = GP.Universe(K, PCAP)
    U.scripts = list(meta['scripts']); U.sid = {k: i for i, k in enumerate(U.scripts)}
    U.units = list(meta['units']); U.uid = {k: i for i, k in enumerate(U.units)}
    _VA['U'] = U


def cmd_validate_gate(a):
    """The gate cell's kernel transitions against term-executed gate encounters (fresh caches), on its own tables."""
    t0 = time.time()
    LS = lot_static('gate')
    st, meta = LS['st'], LS['meta']
    units = meta['units']
    rng = np.random.default_rng(20261013)
    O = np.asarray(st['O'])
    items = []
    for z in range(a.nenc):
        u = int(rng.choice(O)); v = int(rng.choice(O)); rel = 0
        r_ = rng.random()
        if r_ < 0.15: v, rel = u, 2
        elif r_ < 0.25: v, rel = u, 1
        items.append(('S-gate+cache', u, v, rel, None))
    nw = min(3, a.workers)
    res = []
    with Pool(nw, initializer=_vagate_init) as pool:
        for out in pool.imap_unordered(_va_job, [items[i::nw * 8] for i in range(nw * 8)]):
            res.extend(out)
    mism = []; n = 0
    for rule, u, v, rel, shadow, got in res:
        if got is None: continue
        n += 1
        ku = kernel_one(LS, PV.R_SGATE, u, v, rel)
        kk = units[ku] if ku >= 0 else None
        if kk is None or list(kk[1]) != got[0] or list(kk[2]) != got[1]:
            mism.append([u, v, rel, None if kk is None else [list(kk[1]), list(kk[2])], got[:2], got[2][:6]])
    rep = dict(n=n, n_mismatch=len(mism), mismatches=mism[:30], time_s=time.time() - t0)
    json.dump(rep, open(os.path.join(OUT, 'validate_gate.json'), 'w'), indent=1, default=str)
    log('gate transitions: %d compared, %d mismatches' % (n, len(mism)))


# ------------------------------------------------------------------ the lottery (notes §1.7)
MIX4 = (PV.R_SSELF, PV.R_SNON, PV.R_SK2, PV.R_CSNON)
# cell: (N, I, rule spec, prior, static)
CELLS = {
    'Sself': (100, 64, 'S-self', 'L', 'ext'),
    'Snon': (100, 64, 'S-nonself', 'L', 'ext'),
    'Sdel': (100, 64, 'S-self-delayed', 'L', 'ext'),
    'S2': (100, 64, 'S-2', 'L', 'ext'),
    'S3': (100, 64, 'S-3', 'L', 'ext'),
    'S3strict': (100, 64, 'S-3 strict', 'L', 'ext'),
    'CSnon': (100, 64, 'CS-nonself', 'L', 'ext'),
    'mixed': (100, 64, 'mixed', 'L', 'ext'),
    'Cdonor': (100, 64, 'Cdonor', 'L', 'ext'),
    'H': (100, 64, 'H', 'L', 'ext'),
    'ablation': (100, 64, 'S-nonself', 'ablation', 'ext'),
    'Sgate': (100, 64, 'S-gate+cache', 'L', 'gate'),
    'S2own': (100, 64, 'S-2 own-root', 'L', 'ext'),          # post-hoc diagnostic (not predicted, not scored)
    'S2time': (100, 64, 'S-2 timing', 'L', 'ext'),           # post-hoc diagnostic (not predicted, not scored)
    'SselfDF': (100, 64, 'S-self D-first', 'L', 'ext'),      # post-hoc diagnostic (not predicted, not scored)
    'Sself_N200': (200, 64, 'S-self', 'L', 'ext'),
    'Snon_N200': (200, 64, 'S-nonself', 'L', 'ext'),
    'Cdonor_N200': (200, 64, 'Cdonor', 'L', 'ext'),
    'Sself_I128': (100, 128, 'S-self', 'L', 'ext'),
    'Snon_I128': (100, 128, 'S-nonself', 'L', 'ext'),
    'Cdonor_I128': (100, 128, 'Cdonor', 'L', 'ext'),
    'ablation_N200': (200, 64, 'S-nonself', 'ablation', 'ext'),     # extra, not predicted
    'ablation_I128': (100, 128, 'S-nonself', 'ablation', 'ext'),    # extra, not predicted
}
SALT = 20261012
SNAPS = (10, 50, 200, 1000, 2000, 5000, 10000)
KCAP = 150000
_LS = {}


def lot_static(which='ext'):
    if which in _LS: return _LS[which]
    path = os.path.join(OUT, 'static' if which == 'ext' else 'static_gate')
    st, meta = GP.load_static(path)
    PRODC, PD = patched(st, os.path.join(OUT, 'prod_exec.json' if which == 'ext' else 'prod_exec_gate.json'))
    sets = np.load(os.path.join(OUT, 'sets.npz' if which == 'ext' else 'sets_gate.npz'))
    OSV = np.load(os.path.join(OUT, 'OSV.npy' if which == 'ext' else 'OSV_gate.npy'))
    SPO = np.load(os.path.join(OUT, 'SPO.npy' if which == 'ext' else 'SPO_gate.npy'))
    cat = CP.Catalogue(7, 'P', K)
    mu = cat.spelling_mass('L'); mu = mu / mu.sum()
    names = [cat.name(k) for k in range(len(cat.spell))]
    tau = cat.tau.astype(np.int64)
    Hu, Eu = np.asarray(meta['H_unit']).astype(np.int64), np.asarray(meta['E_unit']).astype(np.int64)
    A, selfa = st['A'], st['selfa']
    O = np.asarray(st['O'])
    k_cb = names.index('if(CHK(them,me,C),C,D)'); k_d = names.index('D')
    u_cb = int(Hu[tau[k_cb]]); u_d = int(Hu[tau[k_d]])
    est = np.zeros(len(meta['units']), bool)
    est[O] = (np.asarray(selfa)[O] == 1) & (np.asarray(A)[O, u_d] == 0)
    hasC = np.asarray(st['BLC'])[:, 0] >= 0
    donor_ok = np.array([est[Hu[tau[k]]] and hasC[Hu[tau[k]]] for k in range(len(names))])
    costs = json.load(open(os.path.join(M5, 'costs.json')))
    COSTS = np.array([costs['ac'] + costs['surgery'], costs['gate'], costs['gate0'], costs['prodC'], costs['prodD'],
                      PCAP + 5], float)
    FUT = np.zeros((PRODC.shape[0], 2), np.int8)
    FUT[:, 0] = ~(PRODC >= 0).any(1)
    FUT[:, 1] = ~(PRODC[:, :25] >= 0).any(1)
    LS = dict(st=st, meta=meta, PRODC=PRODC, PD=PD, OSV=OSV, SPO=SPO, FUT=FUT, cat=cat, mu=mu, names=names, tau=tau,
              Hu=Hu, Eu=Eu, u_cb=u_cb, u_d=u_d, donor_ok=donor_ok, COSTS=COSTS,
              ident=sets['ident'], openu=sets['openu'], spo_unit=sets['spo_unit'], capable=sets['capable'],
              only_self=sets['only_self'], Q=sets['Q'], R=sets['R'])
    _LS[which] = LS
    return LS


def founders(cell, rep, LS):
    N, I, spec, prior, which = CELLS[cell]
    nsp = len(LS['mu'])
    rng = np.random.default_rng([N, I, rep, SALT])
    sp = rng.choice(nsp, size=(I, N), p=LS['mu'])
    if prior == 'ablation':
        Q = set(LS['Q'].tolist()); R = LS['R']
        pr = LS['mu'][R] / LS['mu'][R].sum()
        r_ab = np.random.default_rng([N, I, rep, SALT, 4])
        for i in range(I):
            for j in range(N):
                if int(sp[i, j]) in Q:
                    sp[i, j] = int(r_ab.choice(R, p=pr))
    r_mode = np.random.default_rng([N, I, rep, SALT, 1])
    if spec == 'mixed':
        rule = np.array(MIX4, np.int64)[r_mode.integers(0, 4, size=(I, N))]
    elif spec == 'Cdonor':
        rule = np.full((I, N), PV.R_C, np.int64)
    else:
        rule = np.full((I, N), PV.RULE_OF[spec], np.int64)
    if spec == 'Cdonor':
        r_don = np.random.default_rng([N, I, rep, SALT, 3])
        pd = LS['mu'] * LS['donor_ok']; pd = pd / pd.sum()
        for i in range(I):
            j = int(r_don.integers(N))
            sp[i, j] = int(r_don.choice(nsp, p=pd)); rule[i, j] = PV.R_H
    t = LS['tau'][sp]
    unit = np.where(rule == PV.R_H, LS['Hu'][t], LS['Eu'][t])
    return sp, rule, unit


def kernel_seed(N, I, rep):
    return int((rep * 1000003 + N * 10007 + I * 101 + SALT) % (2 ** 62))


class Run:
    """The state of one lottery run (numba arrays) and its checkpoint statistics."""

    def __init__(self, cell, rep):
        self.cell, self.rep = cell, rep
        N, I, spec, prior, which = CELLS[cell]
        self.N, self.I, self.r = N, I, N // 2
        LS = self.LS = lot_static(which)
        st = LS['st']
        sp, rule, unit = founders(cell, rep, LS)
        self.sp0, self.rule0 = sp, rule
        from numba.typed import Dict
        from numba import types
        self.d = Dict.empty(key_type=types.int64, value_type=types.int64)
        self.tunit = np.zeros(KCAP, np.int64); self.trule = np.zeros(KCAP, np.int64)
        self.tsp = np.zeros(KCAP, np.int64); self.tanc = np.zeros(KCAP, np.int64)
        nt = 0
        self.slots = np.zeros((I, N), np.int64)
        for i in range(I):
            for j in range(N):
                k, nt = PV.make_type(self.d, self.tunit, self.trule, self.tsp, self.tanc, nt, int(unit[i, j]),
                                     int(rule[i, j]), int(sp[i, j]), 0)
                self.slots[i, j] = k
        self.ntv = np.array([nt], np.int64)
        self.counts = np.zeros((I, KCAP), np.int64)
        for i in range(I):
            np.add.at(self.counts[i], self.slots[i], 1)
        self.pres = np.zeros((I, N), np.int64); self.npres = np.zeros(I, np.int64)
        self.pos = -np.ones((I, KCAP), np.int64)
        for i in range(I):
            ks = np.nonzero(self.counts[i])[0]
            for tt, k in enumerate(ks):
                self.pres[i, tt] = k; self.pos[i, k] = tt
            self.npres[i] = len(ks)
        self.paysum = np.zeros((I, KCAP))
        self.A, self.selfa = st['A'], st['selfa']
        PV.init_paysum(self.counts, self.paysum, self.pres, self.npres, self.tunit, self.tsp, self.A, self.selfa)
        nsp = len(LS['mu'])
        self.spcount = np.zeros((I, nsp), np.int64)
        for i in range(I):
            np.add.at(self.spcount[i], sp[i], 1)
        self.ctr = np.zeros((PV.NRULE, PV.NCTR), np.int64)
        self.steps_rule = np.zeros(PV.NRULE)
        self.wn = np.zeros((I, N), np.int64); self.wenc = np.zeros((I, N), np.int64)
        self.wsp = np.zeros((I, N, 3), np.int64); self.wcode = np.zeros((I, N, 3), np.int64)
        self.wsid = np.zeros((I, N, 3), np.int64)
        self.ckey = np.zeros((I, N, PV.CACHE_CAP), np.int64); self.cval = np.zeros((I, N, PV.CACHE_CAP), np.int64)
        self.ncache = np.zeros((I, N), np.int64)
        self.plog = -np.ones((I, N, 5), np.int64)
        BLC = st['BLC']
        for i in range(I):
            for j in range(N):
                PV.plog_open(i, j, self.slots[i, j], self.tunit, self.trule, BLC, self.plog)
        self.hist_wait = np.zeros((PV.NRULE, 2, 4, PV.NEB), np.int64)
        self.hist_acq = np.zeros((PV.NRULE, 2, PV.NEB), np.int64)
        self.hist_steps = np.zeros((PV.NRULE, PV.NSB), np.int64)
        self.hist_cens = np.zeros((PV.NRULE, 2, 2, PV.NEB), np.int64)
        self.nprod = np.zeros((PV.NRULE, 2, 4), np.int64)
        self.err = np.zeros(1, np.int64)
        self.tset = -np.ones(KCAP, np.int64)
        self.uns = np.zeros(I, np.int64)
        self.rulecount = np.zeros(PV.NRULE, np.int64)
        self.enc_exp = np.zeros(PV.NRULE)
        self.fcount = np.zeros(PV.NRULE, np.int64)
        self.enc_futile = np.zeros(PV.NRULE)
        PV.init_uns(self.slots, self.tunit, self.trule, self.tset, st['BLC'], st['BLD'], LS['PD'], st['utau'], LS['FUT'],
                    self.uns, self.rulecount, self.fcount)
        self.seed = kernel_seed(N, I, rep)
        self.skip = True
        self.g = 0
        self.maj_k = np.zeros(I, np.int64); self.maj_n = np.zeros(I, np.int64)

    def advance(self, gens):
        LS, st = self.LS, self.LS['st']
        g = PV.segment(self.g, gens, self.seed, self.N, 0.3, 1.0 / self.N, self.r, self.slots, self.counts,
                       self.paysum, self.pres, self.npres, self.pos, self.spcount, self.d, self.tunit, self.trule,
                       self.tsp, self.tanc, self.ntv, st['utau'], st['BLC'], st['BLD'], st['SINGLE'], st['APP'],
                       LS['PRODC'], LS['PD'], st['KIND'], st['NAT'], st['CHC'], st['CHD'], st['UVt'], self.A,
                       self.selfa, LS['OSV'], LS['SPO'], LS['capable'], LS['COSTS'], self.ctr, self.steps_rule,
                       self.wn, self.wenc, self.wsp, self.wcode, self.wsid, self.ckey, self.cval, self.ncache,
                       self.plog, self.hist_wait, self.hist_acq, self.hist_steps, self.hist_cens, self.nprod,
                       LS['ident'], LS['spo_unit'], self.tset, self.uns, self.rulecount, self.enc_exp, self.skip,
                       LS['FUT'], self.fcount, self.enc_futile, self.err)
        if self.err[0] != 0:
            raise RuntimeError('kernel error %d in %s rep %d at generation %d (types %d)' % (
                self.err[0], self.cell, self.rep, g, self.ntv[0]))
        self.g = self.g + gens

    def island_stats(self):
        return PV.island_stats(self.counts, self.pres, self.npres, self.N, self.tunit, self.tsp, self.A, self.selfa,
                               self.maj_k, self.maj_n)

    def glob(self):
        return np.nonzero(self.counts[:, :self.ntv[0]].sum(0))[0]

    def e3(self):
        glob = self.glob()
        if len(glob) > 3000: return None
        return PV.e3_status(self.counts, self.pres, self.npres, glob.astype(np.int64), len(glob), self.tunit,
                            self.tsp, self.A, self.selfa)

    def frozen(self):
        """A single global type whose own encounters change nothing."""
        glob = self.glob()
        if len(glob) != 1: return False
        k = int(glob[0])
        st = self.LS['st']
        u = self.tunit[k]; rule = self.trule[k]
        if rule == PV.R_H: return True
        hasC = st['BLC'][u, 0] >= 0; hasD = st['BLD'][u, 0] >= 0
        if rule == PV.R_C: return True                      # copying from one's own quote is skipped
        if rule == PV.R_SGATE: return hasD and hasC and st['UVt'][u, 0] == 1
        return hasC and hasD

    def snapshot(self, cc):
        LS, st = self.LS, self.LS['st']
        A, selfa = self.A, self.selfa
        I, N = self.I, self.N
        nt = int(self.ntv[0])
        tunit, trule, tsp, tanc = self.tunit[:nt], self.trule[:nt], self.tsp[:nt], self.tanc[:nt]
        cnt = self.counts[:, :nt]
        glob = cnt.sum(0)
        present = np.nonzero(glob)[0]
        selfc = np.zeros(nt)
        for k in present.tolist():
            selfc[k] = PV.cc_pair(k, k, self.tunit, self.tsp, A, selfa)
        maj = self.maj_k.copy()
        held = np.array([selfc[maj[i]] > 0.5 and cc[i] >= 0.5 for i in range(I)])
        univ_pairs = True
        for i in range(I):
            for j in range(i + 1, I):
                if PV.cc_pair(maj[i], maj[j], self.tunit, self.tsp, A, selfa) < 0.5:
                    univ_pairs = False; break
            if not univ_pairs: break
        allheld = bool(held.all())
        outcome = 'universal' if (allheld and univ_pairs) else ('patchwork' if allheld else 'unheld')
        ucb = LS['u_cb']
        hu = tunit[maj]
        open_h = (A[hu, ucb] == 1) & (A[ucb, hu] == 1)
        ident_h = LS['ident'][hu]
        spo_h = LS['spo_unit'][hu]
        rule_all = np.bincount(trule[present], weights=glob[present], minlength=PV.NRULE)
        rule_coop = np.zeros(PV.NRULE)
        strat_tree = {}
        strat_sp = {}
        for i in range(I):
            if not held[i]: continue
            for k in np.nonzero(cnt[i])[0]:
                if selfc[k] > 0.5:
                    rule_coop[trule[k]] += cnt[i, k]
                    tt = int(st['utau'][tunit[k]])
                    strat_tree.setdefault(tt, np.zeros(PV.NRULE))[trule[k]] += cnt[i, k]
                    strat_sp.setdefault(int(tsp[k]), np.zeros(PV.NRULE))[trule[k]] += cnt[i, k]
        top_tree = sorted(strat_tree.items(), key=lambda z: -z[1].sum())[:12]
        top_sp = sorted(strat_sp.items(), key=lambda z: -z[1].sum())[:12]
        names = LS['names']; cat = LS['cat']
        units = LS['meta']['units']
        SPO = LS['SPO']
        inst = np.zeros((PV.NRULE, 4))               # C instances, SPO instances, search-tagged, host-tagged
        for k in present.tolist():
            t, cs, ds = units[tunit[k]]
            for p_, s in enumerate(cs):
                inst[trule[k], 0] += glob[k]
                if SPO[t, s]: inst[trule[k], 1] += glob[k]
                if (tanc[k] >> p_) & 1: inst[trule[k], 2] += glob[k]
                else: inst[trule[k], 3] += glob[k]
        quotes = set((int(tunit[k]), int(tsp[k])) for k in present.tolist())
        spells = set(int(tsp[k]) for k in present.tolist())
        cross = float(PV.cross_pcc(self.counts, self.pres, self.npres, N, self.tunit, self.tsp, A, selfa))
        gi = np.zeros(4)                              # individuals in ident units, spo units, open units, total
        for k in present.tolist():
            u = tunit[k]
            gi[0] += glob[k] * LS['ident'][u]; gi[1] += glob[k] * LS['spo_unit'][u]; gi[2] += glob[k] * LS['openu'][u]
        gi[3] = glob.sum()
        holders = {}
        for i in range(I):
            if held[i]:
                key = names[int(tsp[maj[i]])]
                holders[key] = holders.get(key, 0) + 1
        return dict(g=self.g, pcc=float(cc.mean()), islands90=int((cc >= 0.9).sum()), held=int(held.sum()),
                    outcome=outcome, universal_open=bool(outcome == 'universal' and bool(open_h.all())),
                    open_islands=int((open_h & held).sum()), identity_islands=int((ident_h & held).sum()),
                    spo_islands=int((spo_h & held).sum()), cross_pcc=cross,
                    rule_all=rule_all.tolist(), rule_coop=rule_coop.tolist(),
                    strat_tree=[(names[cat.members[t][0]], v.tolist()) for t, v in top_tree],
                    strat_sp=[(names[s_], v.tolist()) for s_, v in top_sp],
                    inst=inst.tolist(), n_quotes=len(quotes), n_spellings=len(spells), n_types=nt,
                    group_ind=gi.tolist(), holders=sorted(holders.items(), key=lambda z: -z[1])[:10])

    def final_logs(self):
        """Censor the producers still lacking at the horizon."""
        st = self.LS['st']
        for i in range(self.I):
            for j in range(self.N):
                PV.plog_close(i, j, self.slots[i, j], self.tunit, self.trule, st['utau'], st['BLC'], self.LS['capable'],
                              self.plog, self.hist_wait, self.hist_acq, self.hist_steps, self.hist_cens, self.nprod, 2)


def lottery_job(job):
    cell, rep, gens, ext = job[:4]
    tmax = job[4] if len(job) > 4 else 0           # wall-clock cap on the extension phase (0: none)
    ext_cut = -1
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    R = Run(cell, rep)
    every = 10
    trace = []
    snaps = {}
    estab = -1
    e3_gen, e3_out = -1, None
    ever90 = np.zeros(R.I, bool)
    group_max = np.zeros(3, np.int64)            # max islands held by ident / spo / open holders
    group_first = [-1, -1, -1]
    est_snap = None
    horizon = gens
    frozen_at = -1
    g = 0
    while g < horizon:
        R.advance(every)
        g = R.g
        cc = R.island_stats()
        if estab < 0 and (cc >= 0.9).any():
            estab = g
        ever90 |= cc >= 0.9
        if e3_gen < 0 and (g <= gens or g in SNAPS or g % 500 == 0):
            # every checkpoint to the 2,000-generation horizon; sparser in an extension (the closure is O(I·types²))
            s3 = R.e3()
            if s3 is not None and (s3 >= 0).all():
                e3_gen = g; e3_out = 'success' if (s3 == 1).all() else 'fail'
        if g in SNAPS or estab == g or g % 50 == 0:
            sn = R.snapshot(cc)
            for z, key in enumerate(('identity_islands', 'spo_islands', 'open_islands')):
                if sn[key] > group_max[z]: group_max[z] = sn[key]
                if sn[key] > 0 and group_first[z] < 0: group_first[z] = g
            if estab == g and est_snap is None: est_snap = sn
            if g in SNAPS: snaps[g] = sn
            trace.append((g, sn['pcc'], sn['islands90'], sn['held'], sn['identity_islands'], sn['open_islands'],
                          sn['spo_islands'], sn['n_types']))
        if g == gens and ext > gens:
            sn = snaps.get(gens)
            if sn is not None and (sn['outcome'] != 'universal' or e3_out is None) and e3_out != 'fail':
                horizon = ext
        if tmax > 0 and g > gens and time.time() - t0 > tmax:
            ext_cut = g                              # the extension is censored at g (budget)
            break
        if g >= 50 and R.frozen():
            frozen_at = g
            sn = R.snapshot(R.island_stats())
            for gs in SNAPS:
                if g < gs <= horizon and gs not in snaps: snaps[gs] = dict(sn, g=gs, frozen_from=g)
            break
    R.final_logs()
    cc = R.island_stats()
    fin = R.snapshot(cc)
    persist = float((ever90 & (cc >= 0.9)).sum() / ever90.sum()) if ever90.any() else None
    LS = R.LS
    sp0 = R.sp0
    seeded_q = int(np.isin(sp0, LS['Q']).sum())
    seeded_only_self = int(LS['only_self'][LS['tau'][sp0]].sum())
    return dict(cell=cell, rep=rep, N=R.N, I=R.I, gens=gens, horizon=horizon, last_gen=R.g, frozen_at=frozen_at,
                ext_cut=ext_cut,
                establish_gen=estab, E3_gen=e3_gen, E3=e3_out if e3_out else 'censored', ever90=int(ever90.sum()),
                persistence=persist, trace=trace, snaps={str(k): v for k, v in snaps.items()}, est_snap=est_snap,
                final=fin, group_max=group_max.tolist(), group_first=group_first,
                seeded_Q=seeded_q, seeded_only_self=seeded_only_self,
                ctr=R.ctr.tolist(), steps_rule=R.steps_rule.tolist(), enc_exp=R.enc_exp.tolist(),
                enc_futile=R.enc_futile.tolist(),
                hist_wait=R.hist_wait.tolist(),
                hist_acq=R.hist_acq.tolist(), hist_steps=R.hist_steps.tolist(), hist_cens=R.hist_cens.tolist(),
                nprod=R.nprod.tolist(), n_types=int(R.ntv[0]), time_s=time.time() - t0)


def cmd_lottery(a):
    path = os.path.join(OUT, 'lottery_%s.json' % a.out)
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {(r['cell'], r['rep']) for r in rows}
    jobs = [(c, rep, a.gens, a.ext, a.tmax) for rep in range(a.rep0, a.rep0 + a.runs) for c in a.cells if (c, rep) not in done]
    log('lottery jobs %d (pid %d)' % (len(jobs), os.getpid()))
    t0 = time.time()
    with Pool(min(3, a.workers)) as pool:
        for r in pool.imap_unordered(lottery_job, jobs):
            rows.append(r)
            tmp = path + '.tmp'
            json.dump(rows, open(tmp, 'w')); os.replace(tmp, path)
            f = r['final']
            log('%s rep %d: estab %d E3 %s@%d pcc %.3f held %d %s open %d ident %d spo %d types %d last %d (%.0fs, total %.0fs)' % (
                r['cell'], r['rep'], r['establish_gen'], r['E3'], r['E3_gen'], f['pcc'], f['held'], f['outcome'],
                f['open_islands'], f['identity_islands'], f['spo_islands'], r['n_types'], r['last_gen'], r['time_s'],
                time.time() - t0))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('static'); s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('osv'); s.add_argument('--workers', type=int, default=3); s.add_argument('--nsample', type=int, default=300)
    s.add_argument('--which', default='ext')
    s = sub.add_parser('sets'); s.add_argument('--which', default='ext')
    s = sub.add_parser('lottery'); s.add_argument('--cells', nargs='+'); s.add_argument('--runs', type=int, default=40)
    s.add_argument('--rep0', type=int, default=0)
    s.add_argument('--gens', type=int, default=2000); s.add_argument('--ext', type=int, default=0)
    s.add_argument('--tmax', type=float, default=0)
    s.add_argument('--workers', type=int, default=3); s.add_argument('--out', default='main')
    s = sub.add_parser('pairs'); s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('validate'); s.add_argument('--workers', type=int, default=3)
    s.add_argument('--nenc', type=int, default=150); s.add_argument('--skipgens', type=int, default=150)
    s = sub.add_parser('gate_static'); s.add_argument('--workers', type=int, default=3)
    s.add_argument('--budget', type=float, default=6.0)
    s = sub.add_parser('validate_gate'); s.add_argument('--workers', type=int, default=3)
    s.add_argument('--nenc', type=int, default=300)
    a = ap.parse_args()
    {'static': cmd_static, 'osv': cmd_osv, 'sets': cmd_sets, 'lottery': cmd_lottery, 'pairs': cmd_pairs,
     'validate': cmd_validate, 'gate_static': cmd_gate_static, 'validate_gate': cmd_validate_gate}[a.cmd](a)


if __name__ == '__main__':
    main()
