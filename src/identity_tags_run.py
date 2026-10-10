"""Driver for the identity-and-tags cells (predictions/2026-10-10-identity-and-tags.md).

    python3 src/identity_tags_run.py static [--workers 3]       # catalogue, ideal tables, lumping, families
    python3 src/identity_tags_run.py validate [--workers 3]     # notes §1.12 items 2-9 (before any counted cell)
    python3 src/identity_tags_run.py lottery --cell L --runs 40 [--N 100 --I 64]
    python3 src/identity_tags_run.py chain --N 10000 [--label main|noclosed]

Raw tables go to runs/identity_tags/ (npz and pickles, not committed); summaries to json.
"""
import argparse, json, math, os, pickle, sys, time
from collections import defaultdict, Counter
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import lt_code as L
import lt_cert as C
import carrier_populations as CP
import identity_tags as IT

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'identity_tags')
os.makedirs(OUT, exist_ok=True)
LISTS = os.path.join(OUT, 'lists_n7.pkl')
STATIC = os.path.join(OUT, 'static_n7.npz')
STATIC_JSON = os.path.join(OUT, 'static_n7.json')


# ------------------------------------------------------------------ catalogue cache
def load_catalogue(verbose=False):
    if os.path.exists(LISTS):
        lists = pickle.load(open(LISTS, 'rb'))
        return IT.Catalogue(7, lists=lists, verbose=verbose)
    cat = IT.Catalogue(7, verbose=verbose)
    pickle.dump(cat.lists, open(LISTS, 'wb'))
    return cat


_G = {}


def _init():
    sys.setrecursionlimit(1000000)
    _G['cat'] = load_catalogue()
    _G['chk'] = CP.Checker('ideal', _G['cat'].V, _G['cat'].K)


def _check_job(job):
    """job: (a, rows) rows = [(idx, spelling_t, spelling_m)].  Returns (a, idx array, values int8, n_TO)."""
    a, rows = job
    cat = _G['cat']; chk = _G['chk']
    idx = np.zeros(len(rows), np.int64); vals = np.zeros(len(rows), np.int8); nto = 0
    for r, (i, st, sm) in enumerate(rows):
        idx[r] = i
        if st < 0: continue
        v, _ = chk(0, cat.term(int(st)), cat.term(int(sm)), a)
        vals[r] = 1 if v == 'T' else 0
        nto += v == 'TO'
    return a, idx, vals, nto


def _uv_job(job):
    """Unit values for canonical units: rows [(c, spelling)] -> per row 8 values (self, C, D, CB) x (C, D)."""
    rows = job
    cat = _G['cat']; chk = _G['chk']
    out = []
    QM = {'C': L.PROG_C, 'D': L.PROG_D, 'CB': cat.cb_term}
    for c, s in rows:
        t = cat.term(int(s))
        res = []
        for kind in IT.UV_KINDS:
            for a in 'CD':
                has = cat.u_hasC[c] if a == 'C' else cat.u_hasD[c]
                if not has:
                    res.append(0); continue
                m = t if kind == 'self' else QM[kind]
                v, _ = chk(0, t, m, a)
                res.append(1 if v == 'T' else (2 if v == 'TO' else 0))
        out.append((int(c), res))
    return out


def compute_static(nw):
    t0 = time.time()
    cat = load_catalogue(verbose=True)
    tb = time.time() - t0
    NU = cat.NU
    S, R = IT.asker_masks(cat)
    info = dict(n_bodies=len(cat.sexprs), n_spellings=int(cat.nsp), n_dts=len(cat.dt_list), n_units=int(NU),
                n_lists=len(cat.lists), build_s=tb)
    print(json.dumps(info), flush=True)
    with Pool(nw, initializer=_init) as pool:
        # unit values
        t1 = time.time()
        canon = IT.unit_value_keys(cat)
        cu = np.unique(canon)
        rows = [(int(c), cat.rep(int(c))) for c in cu]
        UVc = {}
        nTO_uv = 0
        for out in pool.imap_unordered(_uv_job, [rows[i:i + 100] for i in range(0, len(rows), 100)]):
            for c, res in out:
                UVc[c] = res
                nTO_uv += sum(1 for v in res if v == 2)
        UV = {}
        j = 0
        for kind in IT.UV_KINDS:
            for a in 'CD':
                UV[(kind, a)] = np.array([1 if UVc[int(canon[u])][j] == 1 else 0 for u in range(NU)], np.int8)
                j += 1
        info['unit_value_checks'] = len(cu) * 8
        info['unit_value_TO'] = nTO_uv
        info['unit_values_s'] = time.time() - t1
        print('unit values', len(cu), time.time() - t1, flush=True)
        # pair checks on reduced keys
        CH = {}
        info['pair'] = {}
        for a in 'CD':
            t1 = time.time()
            keys = IT.needed_keys(cat, a)
            inst = IT.key_instances(cat, keys)
            order = np.argsort(inst[:, 1], kind='stable')          # group by target canonical unit (memo locality)
            jobs = []
            CH_ROWS = 4000
            for s0 in range(0, len(order), CH_ROWS):
                sel = order[s0:s0 + CH_ROWS]
                jobs.append((a, [(int(i), int(inst[i, 2]), int(inst[i, 3])) for i in sel]))
            vals = np.zeros(len(inst), np.int8)
            nto = 0; done = 0
            for (aa, idx, v, nt) in pool.imap_unordered(_check_job, jobs, chunksize=1):
                vals[idx] = v; nto += nt; done += len(idx)
                if done % 1000000 < len(idx):
                    print('  [%s] %d / %d checks (%.0fs)' % (a, done, len(inst), time.time() - t1), flush=True)
            n_noinst = int((inst[:, 2] < 0).sum())
            CH[a] = IT.fill_dense(cat, a, inst[:, 0], vals, S, R)
            info['pair'][a] = dict(keys=int(len(inst)), TO=int(nto), no_instance=n_noinst, T=int(vals.sum()), s=time.time() - t1)
            np.savez_compressed(os.path.join(OUT, 'keys_%s.npz' % a), inst=inst, vals=vals)
            print('pair %s: %d keys, %d T, %d TO (%.0fs)' % (a, len(inst), vals.sum(), nto, time.time() - t1), flush=True)
            del keys, inst, vals
    t1 = time.time()
    A_u, self_u = IT.compose(cat, CH, UV)
    info['compose_s'] = time.time() - t1
    np.savez_compressed(STATIC, A_u=A_u, self_u=self_u, **{'UV_%s_%s' % k: v for k, v in UV.items()})
    del CH
    t1 = time.time()
    w = cat.spelling_weights()
    lp = IT.lump(cat, A_u, self_u, w)
    info['lump_s'] = time.time() - t1
    classes = lp['classes']
    info.update(n_classes=len(classes), n_split_units=lp['n_split_units'], n_split_classes=lp['n_split_classes'])
    print('classes', len(classes), 'split units', lp['n_split_units'], 'split classes', lp['n_split_classes'], flush=True)
    cos = IT.class_of_spelling(classes, cat.nsp)
    with np.load(STATIC) as z:
        d = dict(z)
    d.update(A_class=lp['A'], class_of_spelling=cos, class_rep=np.array([c['rep'] for c in classes]))
    np.savez_compressed(STATIC, **d)
    info['total_s'] = time.time() - t0
    json.dump(info, open(STATIC_JSON, 'w'), indent=1)
    print(json.dumps(info, indent=1), flush=True)


def load_static():
    z = np.load(STATIC)
    return {k: z[k] for k in z.files}


# ------------------------------------------------------------------ classes, masses, families
class Static:
    """Class-level objects: action table, masses per prior and tilt, names, properties, families."""

    def __init__(self, cat=None):
        self.cat = cat or load_catalogue()
        z = load_static()
        self.A = z['A_class'].astype(np.int8)
        self.cos = z['class_of_spelling']
        self.crep = z['class_rep']
        self.nc = self.A.shape[0]
        self.U, self.PCC = CP.pay_matrix(self.A)
        cat = self.cat
        self.names = [cat.name(int(k)) for k in self.crep]
        self.n_spell = np.bincount(self.cos, minlength=self.nc)
        self.selfc = self.A[np.arange(self.nc), np.arange(self.nc)] == 1
        self.iD = self.class_of(('D',), 0)
        self.est = self.selfc & (self.A[:, self.iD] == 0)
        self.allc = (self.A == 1).all(1)
        self.named = {nm: self.class_of(*IT.NAMED[nm]) for nm in IT.NAMED}
        self.named['TC2^2'] = self.class_of(IT.TC2_X, 2)
        self.w = cat.spelling_weights()

    def class_of(self, x, M):
        return int(self.cos[self.cat.spelling_of(x, M)])

    def mass(self, w_spell):
        m = np.bincount(self.cos, weights=w_spell, minlength=self.nc)
        return m / m.sum()

    def label(self):
        """Family labels of establisher classes (notes §1.10)."""
        A = self.A; mut = (A == 1) & (A.T == 1)
        nm = self.named
        lab = np.array(['-'] * self.nc, dtype=object)
        for i in np.nonzero(self.est)[0]:
            others = mut[i] & self.est
            others[i] = False
            if mut[i, nm['CB']] or i == nm['CB']: lab[i] = 'open'
            elif mut[i, nm['XC']] or i == nm['XC']: lab[i] = 'exclusive'
            elif mut[i, nm['TC1^1']] or i == nm['TC1^1']: lab[i] = 'tag1'
            elif mut[i, nm['TC2^2']] or i == nm['TC2^2']: lab[i] = 'tag2'
            elif not others.any(): lab[i] = 'identity'
            else: lab[i] = 'other'
        return lab

    # -- priors and tilts (spelling level, then classes)
    def spelling_prior(self, cell):
        cat = self.cat
        w = cat.spelling_weights()
        if cell in ('L',) or cell.startswith('L_'):
            return w / w.sum()
        if cell in ('identity', 'tags', 'cbq'):
            w = w * cat.sub_mask(cell)
            return w / w.sum()
        if cell == 'U':
            return None
        Mmass = self.family_mass()
        w = w / w.sum()
        if cell == 'T1a':
            blk = [cat.spelling_of(IT.EQ_X, 0)]
            return self._tilt(w, blk, [Mmass])
        if cell == 'T1b':
            blk = self.heaviest_spellings_of_dt(IT.EQ_X, 10)
            return self._tilt(w, blk, [Mmass / 10] * 10)
        if cell == 'T1c':
            blk = self.heaviest_spellings_of_dt(IT.CB_X, 10)
            fam = self.open_neighbourhood()
            rm = np.isin(self.cos, fam)
            w = w.copy(); w[rm] = 0
            return self._tilt(w, blk, [Mmass / 10] * 10)
        if cell == 'T2':
            return self._tilt(w, [cat.spelling_of(IT.TC1_X, 1)], [Mmass])
        if cell == 'T3':
            return self._tilt(w, [cat.spelling_of(IT.XC_X, 0)], [Mmass])
        raise ValueError(cell)

    @staticmethod
    def _tilt(w, blk, masses):
        w = w.copy()
        w[blk] = 0
        w = w / w.sum() * (1 - sum(masses))
        for k, m in zip(blk, masses): w[k] = m
        return w

    def heaviest_spellings_of_dt(self, x, n):
        cat = self.cat
        d = cat.sx_dt[cat.sx_index[x]]
        ks = np.nonzero(cat.sp_dt == d)[0]
        ks = sorted(ks, key=lambda k: (cat.sp_nodes[k], k))
        return [int(k) for k in ks[:n]]

    def class_prior(self, cell):
        if cell == 'U':
            return np.full(self.nc, 1.0 / self.nc)
        return self.mass(self.spelling_prior(cell))

    def open_neighbourhood(self):
        mut = (self.A == 1) & (self.A.T == 1)
        cb = self.named['CB']
        return np.nonzero(self.est & (mut[cb] | (np.arange(self.nc) == cb)))[0]

    _fam = None

    def families(self):
        if self._fam is None:
            est = np.nonzero(self.est)[0]
            t0 = time.time()
            cl, complete, comps = IT.maximal_cliques(self.A, est)
            self._fam = dict(cliques=cl, complete=complete, comps=comps, s=time.time() - t0)
        return self._fam

    def family_mass(self, prior='L'):
        """M: the pooled L mass of F_CB, the heaviest maximal clique containing CB (cached by `analyze`)."""
        fn = os.path.join(OUT, 'static_analysis.json')
        if os.path.exists(fn):
            return float(json.load(open(fn))['F_CB']['M'])
        mu = self.mass(self.cat.spelling_weights())
        cb = self.named['CB']
        best = 0.0
        for c in self.families()['cliques']:
            if cb in c:
                best = max(best, float(mu[c].sum()))
        return best

    def F_CB(self):
        mu = self.mass(self.cat.spelling_weights())
        cb = self.named['CB']
        best, bc = -1, None
        for c in self.families()['cliques']:
            if cb in c and mu[c].sum() > best:
                best, bc = mu[c].sum(), c
        return bc


# ------------------------------------------------------------------ the eps = 0 lottery
def _lottery_numba():
    from numba import njit
    from almost_all_seeds import _sample_parent, _island_cc

    @njit(cache=True)
    def closure_status(U, selfc, glob, K, res_ids, nres, inZ, queue):
        """Milestone 2's E3 test: Z = closure of the residents under 'a present class q joins if U[q, z] >= U[z, z]';
        1 if every class in Z self-cooperates, 0 if none does, -1 otherwise."""
        for k in range(K): inZ[k] = False
        qn = 0; qh = 0
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
    def majority(counts, pres, npres, i):
        best = -1; bc = -1
        for t in range(npres[i]):
            k = pres[i, t]
            if counts[i, k] > bc or (counts[i, k] == bc and k < best):
                bc = counts[i, k]; best = k
        return best

    @njit(cache=True)
    def run(U, PCC, init, N, w, m, gens_main, gens_ext, every, seed, selfc, track):
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
        res_ids = np.empty(K, np.int64); inZ = np.zeros(K, np.bool_); queue = np.empty(K, np.int64)
        isl_cc = np.zeros(I); maj = np.zeros(I, np.int64); prevmaj = -np.ones(I, np.int64)
        e3_gen = -1; e3_out = -1
        estab = -1; all_estab = -1
        snap_estab = np.zeros(K, np.int64)
        first_sep = -1; n_sep_chk = 0; n_res_events = 0; was_sep = False
        n_flips = 0; sep_isl_chk = 0
        frozen_gen = -1
        nt = track.shape[0]
        track_ext = -np.ones(nt, np.int64); track_maxisl = np.zeros(nt, np.int64)
        track_alive_at_sep = np.zeros(nt, np.bool_)
        # snapshots at gens_main (0) and at the end (1): sep flag, cc mean, maj per island, counts
        snap_counts = np.zeros((2, I, K), np.int64)
        snap_gen = -np.ones(2, np.int64)
        snap_sep = np.zeros(2, np.bool_)
        g_end = gens_ext
        for g in range(gens_ext):
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
            if (g + 1) % every == 0 or g + 1 == gens_main:
                gg = g + 1
                for k in range(K): glob[k] = 0
                allc = True
                for i in range(I):
                    for t in range(npres[i]):
                        glob[pres[i, t]] += counts[i, pres[i, t]]
                    cc, pay = _island_cc(counts, PCC, U, pres, npres, paysum, i, N)
                    isl_cc[i] = cc
                    if cc < 0.9: allc = False
                    if estab < 0 and cc >= 0.9: estab = gg
                    maj[i] = majority(counts, pres, npres, i)
                if all_estab < 0 and allc:
                    all_estab = gg
                    for k in range(K): snap_estab[k] = glob[k]
                # separation: two cooperative islands whose majority classes mutually defect
                sep = False
                for i in range(I):
                    if isl_cc[i] < 0.9: continue
                    for j in range(i + 1, I):
                        if isl_cc[j] < 0.9: continue
                        a = maj[i]; b = maj[j]
                        if a != b and PCC[a, b] == 0.0 and U[a, b] < -0.5 and U[b, a] < -0.5:
                            sep = True; break
                    if sep: break
                if sep:
                    n_sep_chk += 1
                    if first_sep < 0:
                        first_sep = gg
                        for t in range(nt):
                            track_alive_at_sep[t] = glob[track[t]] > 0
                    # flips: an island whose majority changed to a class mutually defecting with the old one
                    for i in range(I):
                        if prevmaj[i] >= 0 and maj[i] != prevmaj[i]:
                            a = prevmaj[i]; b = maj[i]
                            if U[a, b] < -0.5 and U[b, a] < -0.5: n_flips += 1
                    sep_isl_chk += I
                elif was_sep:
                    n_res_events += 1
                was_sep = sep
                for i in range(I): prevmaj[i] = maj[i]
                # tracked classes
                for t in range(nt):
                    k = track[t]
                    if glob[k] == 0 and track_ext[t] < 0: track_ext[t] = gg
                    h = 0
                    for i in range(I):
                        if maj[i] == k and isl_cc[i] >= 0.9: h += 1
                    if h > track_maxisl[t]: track_maxisl[t] = h
                # E3
                if e3_gen < 0:
                    npg = 0; only = -1
                    for k in range(K):
                        if glob[k] > 0:
                            npg += 1; only = k
                    if npg == 1 and not selfc[only]:
                        e3_gen = gg; e3_out = 0
                    else:
                        allres = True; allco = True
                        for i in range(I):
                            for t in range(npres[i]): res_ids[t] = pres[i, t]
                            st = closure_status(U, selfc, glob, K, res_ids, npres[i], inZ, queue)
                            if st < 0:
                                allres = False; break
                            if st == 0: allco = False
                        if allres:
                            e3_gen = gg; e3_out = 1 if allco else 0
                # frozen: U constant on the global support
                npg = 0
                for k in range(K):
                    if glob[k] > 0:
                        res_ids[npg] = k; npg += 1
                frozen = False
                if npg <= 400:
                    u0 = U[res_ids[0], res_ids[0]]
                    frozen = True
                    for x in range(npg):
                        for y in range(npg):
                            if abs(U[res_ids[x], res_ids[y]] - u0) > 1e-9:
                                frozen = False; break
                        if not frozen: break
                stop = False
                if frozen:
                    frozen_gen = gg; stop = True
                if gg == gens_main:
                    snap_gen[0] = gg; snap_sep[0] = sep
                    for i in range(I):
                        for k in range(K): snap_counts[0, i, k] = counts[i, k]
                    if not sep: stop = True
                if stop:
                    g_end = gg
                    break
        for i in range(I):
            for k in range(K): snap_counts[1, i, k] = counts[i, k]
        snap_gen[1] = g_end
        snap_sep[1] = was_sep
        if snap_gen[0] < 0:
            snap_gen[0] = g_end; snap_sep[0] = was_sep
            for i in range(I):
                for k in range(K): snap_counts[0, i, k] = counts[i, k]
        return (e3_gen, e3_out, estab, all_estab, snap_estab, first_sep, n_sep_chk, n_res_events, n_flips, sep_isl_chk,
                frozen_gen, track_ext, track_maxisl, track_alive_at_sep, snap_counts, snap_gen, snap_sep)
    return run


_LOT = {}
SALT = 20261010
CELLS = {   # cell -> (prior cell, N, I)
    'L': ('L', 100, 64), 'L_N200': ('L', 200, 64), 'L_I256': ('L', 100, 256), 'U': ('U', 100, 64),
    'T1a': ('T1a', 100, 64), 'T1b': ('T1b', 100, 64), 'T1c': ('T1c', 100, 64), 'T2': ('T2', 100, 64), 'T3': ('T3', 100, 64),
    'abl_identity': ('identity', 100, 64), 'abl_tags': ('tags', 100, 64), 'abl_cbq': ('cbq', 100, 64),
}


def _lot_static():
    if 'st' not in _LOT:
        st = Static()
        _LOT['st'] = st
        _LOT['lab'] = st.label()
        _LOT['priors'] = {}
        _LOT['run'] = _lottery_numba()
        _LOT['track'] = track_groups(st)
    return _LOT['st']


def track_groups(st):
    """Tracked class groups (bridge fate): marked carriers by marker, or-forms, and-forms, the clubs, EQ."""
    cat = st.cat
    out = defaultdict(set)
    dcb = cat.sx_dt[cat.sx_index[IT.CB_X]]
    dof = cat.sx_dt[cat.sx_index[IT.OF1_X]]
    daf = cat.sx_dt[cat.sx_index[IT.AF1_X]]
    for k in range(cat.nsp):
        c = int(st.cos[k]); M = int(cat.sp_M[k]); d = int(cat.sp_dt[k])
        if d == dcb and (M & 1): out['MC1'].add(c)
        if d == dcb and (M & 2): out['MC2'].add(c)
        if d == dof and (M & 1): out['OF1'].add(c)
        if d == daf and (M & 1): out['AF1'].add(c)
    out['TC1^1'].add(st.named['TC1^1']); out['XC'].add(st.named['XC']); out["XC'"].add(st.named["XC'"])
    out['EQ'].add(st.named['EQ']); out['CB'].add(st.named['CB']); out['TwinD'].add(st.named['TwinD'])
    return {k: sorted(v) for k, v in out.items()}


def cross_pcc(counts, PCC, N):
    I = counts.shape[0]
    cf = counts.astype(float)
    g = cf.sum(0)
    tot = g @ PCC @ g - sum(cf[i] @ PCC @ cf[i] for i in range(I))
    return float(tot / (N * N * I * (I - 1)))


def island_view(counts, U, PCC, N):
    I = counts.shape[0]
    cc = np.zeros(I); maj = np.zeros(I, np.int64)
    for i in range(I):
        c = counts[i].astype(float)
        nz = np.nonzero(c)[0]
        tot = c[nz] @ PCC[np.ix_(nz, nz)] @ c[nz] - (c[nz] * np.diag(PCC)[nz]).sum()
        cc[i] = tot / (N * (N - 1))
        maj[i] = nz[np.argmax(c[nz])]
    return cc, maj


def lottery_job(job):
    cell, rep, gens, gens_ext = job
    st = _lot_static()
    pcell, N, I = CELLS[cell]
    pri = _LOT['priors'].get(pcell)
    if pri is None:
        pri = st.class_prior(pcell); _LOT['priors'][pcell] = pri
    rng = np.random.default_rng([N, I, rep, SALT])
    init_full = np.zeros((I, st.nc), np.int64)
    for i in range(I):
        init_full[i] = rng.multinomial(N, pri)
    present = np.nonzero(init_full.sum(0))[0]
    K = len(present)
    loc = {int(c): j for j, c in enumerate(present)}
    U = np.ascontiguousarray(st.U[np.ix_(present, present)])
    PCC = np.ascontiguousarray(st.PCC[np.ix_(present, present)])
    selfc = st.selfc[present].astype(np.bool_)
    init = np.ascontiguousarray(init_full[:, present])
    groups = _LOT['track']
    tr = sorted({c for v in groups.values() for c in v if c in loc})
    track = np.array([loc[c] for c in tr], np.int64) if tr else np.zeros(0, np.int64)
    t0 = time.time()
    res = _LOT['run'](U, PCC, init, N, 0.3, 1.0 / N, gens, gens_ext, 10, 7919 * rep + 13 * N + I, selfc, track)
    (e3_gen, e3_out, estab, all_estab, snap_estab, first_sep, n_sep_chk, n_res, n_flips, sep_isl_chk, frozen_gen,
     track_ext, track_maxisl, track_alive_sep, snap_counts, snap_gen, snap_sep) = res
    lab = _LOT['lab']
    names = st.names
    gl = present  # local -> global class
    est_loc = st.est[present]
    mutCB = ((st.A[:, st.named['CB']] == 1) & (st.A[st.named['CB'], :] == 1))[present]
    out = dict(cell=cell, rep=rep, N=N, I=I, K_present=K, gens=gens, gens_ext=gens_ext, time_s=time.time() - t0,
               E3=('success' if e3_out == 1 else 'fail') if e3_gen >= 0 else 'censored', E3_gen=int(e3_gen),
               establish_gen=int(estab), all_established_gen=int(all_estab), first_sep=int(first_sep),
               n_sep_checks=int(n_sep_chk), n_resolutions=int(n_res), n_flips=int(n_flips), sep_island_checks=int(sep_isl_chk),
               frozen_gen=int(frozen_gen))
    # snapshots
    for si, tag in ((0, 'h2000'), (1, 'end')):
        cnt = snap_counts[si]
        cc, maj = island_view(cnt, U, PCC, N)
        glob = cnt.sum(0)
        cross = cross_pcc(cnt, PCC, N)
        occ = float(np.mean([mutCB[m_] for m_ in maj]))
        allco = bool((cc >= 0.9).all())
        alive_est = [int(gl[k]) for k in np.nonzero((glob > 0) & est_loc)[0]]
        maj_lab = Counter(str(lab[gl[m_]]) if st.est[gl[m_]] else ('nonest:' + ('selfc' if st.selfc[gl[m_]] else 'D')) for m_ in maj)
        if allco and cross >= 0.99:
            oc = 'universal-open' if occ == 1.0 else 'universal-other'
        elif allco:
            oc = 'patchwork'
        elif e3_out == 0 and e3_gen >= 0 and e3_gen <= snap_gen[si]:
            oc = 'failed'
        elif glob.sum() > 0 and (glob > 0).sum() == 1 and not selfc[np.nonzero(glob)[0][0]]:
            oc = 'failed'
        else:
            oc = 'unresolved'
        clique_win = oc == 'universal-other' and all(lab[c] == 'identity' for c in alive_est) and len(alive_est) > 0
        out[tag] = dict(gen=int(snap_gen[si]), separated=bool(snap_sep[si]), outcome=oc, cross_pcc=cross, island_pcc=float(cc.mean()),
                        occupancy=occ, labels=dict(maj_lab), clique_win=bool(clique_win),
                        alive_est=alive_est[:50], n_alive_est=len(alive_est),
                        holders=Counter(names[gl[m_]] for m_ in maj).most_common(6))
    # tracked groups
    trk = {}
    for gname, cls in groups.items():
        idx = [j for j, c in enumerate(tr) if c in cls]
        if not idx:
            trk[gname] = dict(seeded=0); continue
        ext = [int(track_ext[j]) for j in idx]
        trk[gname] = dict(seeded=int(sum(init_full[:, c].sum() for c in cls)), extinct_gen=(max(ext) if all(e >= 0 for e in ext) else -1),
                          max_islands=int(max(track_maxisl[j] for j in idx)), alive_at_first_sep=bool(any(track_alive_sep[j] for j in idx)) if first_sep >= 0 else None)
    out['track'] = trk
    # pooling check
    out['pooling'] = pooling_check(st, init_full, present, snap_estab, out, lab)
    out['seeded_labels'] = dict(Counter(str(lab[c]) for c in present for _ in range(1) if st.est[c]))
    out['seeded_label_counts'] = {k: int(v) for k, v in _label_counts(st, init_full, lab).items()}
    return out


def _label_counts(st, init_full, lab):
    g = init_full.sum(0)
    out = Counter()
    for c in np.nonzero(g)[0]:
        out[str(lab[c]) if st.est[c] else ('selfc' if st.selfc[c] else 'nonselfc')] += int(g[c])
    return out


def pooling_check(st, init_full, present, snap_estab, out, lab):
    seeded_est = [int(c) for c in present if st.est[c]]
    if not seeded_est:
        return None
    cl, complete, comps = IT.maximal_cliques(st.A, np.array(seeded_est), limit=20000)
    g = init_full.sum(0)
    loc = {int(c): j for j, c in enumerate(present)}
    estm = np.zeros(st.nc, np.int64)
    if out['all_established_gen'] >= 0:
        for j, c in enumerate(present): estm[c] = snap_estab[j]
    rows = []
    for c in cl:
        seeded = int(g[c].sum())
        per_isl = int(init_full[:, c].sum(1).max())
        em = int(estm[c].sum())
        rows.append((seeded, em, per_isl, c))
    res = {}
    for tag in ('h2000', 'end'):
        alive = set(out[tag]['alive_est'])
        allco = out[tag]['island_pcc'] >= 0.9 and out[tag]['outcome'] in ('universal-open', 'universal-other')
        won = [allco and alive and alive <= set(r[3]) for r in rows]
        ibest_seed = int(np.argmax([r[0] for r in rows]))
        ibest_est = int(np.argmax([r[1] for r in rows])) if out['all_established_gen'] >= 0 else None
        res[tag] = dict(decided=bool(any(won)), best_seed_won=bool(won[ibest_seed]),
                        best_est_won=bool(won[ibest_est]) if ibest_est is not None else None,
                        winner_sizes=[len(rows[i][3]) for i in range(len(rows)) if won[i]][:5])
    top = sorted(rows, key=lambda r: -r[0])[:5]
    return dict(n_sets=len(cl), complete=complete, n_seeded_est=len(seeded_est),
                top_by_seed=[dict(seeded=r[0], est_mass=r[1], max_per_island=r[2], size=len(r[3]),
                                  labels=dict(Counter(str(lab[c]) for c in r[3]))) for r in top],
                **res)


def cmd_lottery(a):
    path = os.path.join(OUT, 'lottery_%s.json' % a.out)
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {(r['cell'], r['rep']) for r in rows}
    jobs = [(c, rep, a.gens, a.gens_ext) for c in a.cells for rep in range(a.runs) if (c, rep) not in done]
    print('lottery jobs', len(jobs), flush=True)
    with Pool(min(a.workers, 3)) as pool:
        for r in pool.imap_unordered(lottery_job, jobs, chunksize=1):
            rows.append(r)
            json.dump(rows, open(path, 'w'), default=str)
            h, e = r['h2000'], r['end']
            print('%s rep %d: E3 %s@%d estab %d sep@%d | 2000: %s cross %.3f occ %.2f | end@%d: %s cross %.3f | %s (%.0fs, K=%d)' % (
                r['cell'], r['rep'], r['E3'], r['E3_gen'], r['establish_gen'], r['first_sep'], h['outcome'], h['cross_pcc'],
                h['occupancy'], e['gen'], e['outcome'], e['cross_pcc'], e['holders'][:2], r['time_s'], r['K_present']), flush=True)


# ------------------------------------------------------------------ static analysis (families, bridges, masses)
def cmd_analyze(a):
    from carrier_populations_report import leak_test
    t0 = time.time()
    st = Static()
    cat = st.cat
    A, U = st.A, st.U
    nc = st.nc
    mu = {'L': st.class_prior('L'), 'U': st.class_prior('U')}
    lab = st.label()
    mut = (A == 1) & (A.T == 1)
    est = st.est
    nm = st.named
    sg = np.array([IT.s_guarded(cat.dt_list[int(cat.sp_dt[int(st.crep[c])])]) for c in range(nc)])
    ninv = np.array([int((U[:, c] > U[c, c] + 1e-9).sum()) for c in range(nc)])
    out = dict(n_classes=nc, n_selfc=int(st.selfc.sum()), n_est=int(est.sum()), n_allc=int(st.allc.sum()))
    out['mass'] = {pr: dict(est=float(mu[pr][est].sum()), selfc=float(mu[pr][st.selfc].sum()), allc=float(mu[pr][st.allc].sum()),
                            D=float(mu[pr][st.iD]), est_sguarded=float(mu[pr][est & sg].sum()),
                            est_exploited=float(mu[pr][est & (ninv > 0)].sum())) for pr in mu}
    out['labels'] = {str(l): dict(n=int((lab == l).sum()), mass_L=float(mu['L'][lab == l].sum()), mass_U=float(mu['U'][lab == l].sum()))
                     for l in sorted(set(lab.tolist()))}
    out['named'] = {n: dict(cls=int(c), name=st.names[c], mass_L=float(mu['L'][c]), n_spellings=int(st.n_spell[c]),
                            label=str(lab[c]), est=bool(est[c]), selfc=bool(st.selfc[c]), s_guarded=bool(sg[c]),
                            n_strict_invaders=int(ninv[c]), strict_invaders=[st.names[q] for q in np.nonzero(U[:, c] > U[c, c] + 1e-9)[0][:6]])
                    for n, c in nm.items()}
    # spelling masses of the two run trees
    w = cat.spelling_weights(); w = w / w.sum()
    for key, x in (('eq_tree', IT.EQ_X), ('cb_tree', IT.CB_X)):
        d = cat.sx_dt[cat.sx_index[x]]
        ks = np.nonzero(cat.sp_dt == d)[0]
        out[key] = dict(n_spellings=int(len(ks)), mass=float(w[ks].sum()), n_classes=len(set(int(st.cos[k]) for k in ks)))
    out['spelling_mass'] = {n: float(w[cat.spelling_of(*IT.NAMED[n])]) for n in IT.NAMED_ORDER}
    # families
    fam = st.families()
    cl = fam['cliques']
    out['cliques'] = dict(n=len(cl), complete=fam['complete'], s=fam['s'], n_components=len(fam['comps']),
                          component_sizes=sorted((len(c) for c in fam['comps']), reverse=True)[:10])
    cm = np.array([mu['L'][c].sum() for c in cl])
    single = [i for i, c in enumerate(cl) if len(c) == 1]
    exact = [i for i in single if st.n_spell[cl[i][0]] == 1]
    FCB = st.F_CB(); M = st.family_mass()
    NCB = st.open_neighbourhood()
    out['F_CB'] = dict(M=M, size=len(FCB), n_spellings=int(st.n_spell[FCB].sum()), labels=dict(Counter(str(lab[c]) for c in FCB)),
                       N_CB_size=int(len(NCB)), N_CB_mass=float(mu['L'][NCB].sum()),
                       n_cliques_with_CB=int(sum(1 for c in cl if nm['CB'] in c)),
                       heaviest_members=[(st.names[c], float(mu['L'][c])) for c in sorted(FCB, key=lambda c: -mu['L'][c])[:10]])
    out['identity_cliques'] = dict(n_singleton_cliques=len(single), n_exact=len(exact),
                                   mass_exact=float(sum(cm[i] for i in exact)),
                                   heaviest=[(st.names[cl[i][0]], float(cm[i])) for i in sorted(exact, key=lambda i: -cm[i])[:10]],
                                   max_mass=float(max([cm[i] for i in exact], default=0.0)))
    out['ratio_M_over_max_identity_clique'] = M / out['identity_cliques']['max_mass'] if out['identity_cliques']['max_mass'] > 0 else None
    # every clique other than those containing CB: the heaviest, i.e. pooled rivals
    order = np.argsort(-cm)
    top = []
    for i in order[:25]:
        c = cl[i]
        rival = bool(((A[np.ix_(c, FCB)] == 0) & (A[np.ix_(FCB, c)].T == 0)).any())
        inter = sorted(set(c) & set(FCB))
        top.append(dict(mass=float(cm[i]), size=len(c), n_spellings=int(st.n_spell[c].sum()), labels=dict(Counter(str(lab[x]) for x in c)),
                        contains_CB=nm['CB'] in c, rival_of_FCB=rival, bridges_with_FCB=len(inter),
                        bridges_nonexploitable=int(sum(1 for x in inter if ninv[x] == 0)),
                        heaviest=[st.names[x] for x in sorted(c, key=lambda x: -mu['L'][x])[:4]]))
    out['top_cliques'] = top
    # the heaviest pooled set that does not contain CB, and the heaviest rival of F_CB
    nocb = [i for i in order if nm['CB'] not in cl[i]]
    out['heaviest_set_without_CB'] = dict(mass=float(cm[nocb[0]]), labels=dict(Counter(str(lab[x]) for x in cl[nocb[0]])),
                                          heaviest=[st.names[x] for x in sorted(cl[nocb[0]], key=lambda x: -mu['L'][x])[:4]]) if nocb else None
    # rivals of CB among establishers: mutual defection with CB
    rivCB = np.nonzero(est & (A[:, nm['CB']] == 0) & (A[nm['CB'], :] == 0))[0]
    out['rivals_of_CB'] = dict(n=int(len(rivCB)), mass=float(mu['L'][rivCB].sum()), labels=dict(Counter(str(lab[c]) for c in rivCB)),
                               heaviest=[(st.names[c], str(lab[c]), float(mu['L'][c]), bool(sg[c]), int(ninv[c])) for c in sorted(rivCB, key=lambda c: -mu['L'][c])[:12]])
    # pairwise bridges of named pairs
    det = st.class_of(('if', IT.A_(('chk', 'them', 'C', 'D')), ('D',), ('C',)), 0)
    pairs = {'CB|TC1^1': (nm['CB'], nm['TC1^1']), 'CB|TC2^2': (nm['CB'], nm['TC2^2']), 'CB|XC': (nm['CB'], nm['XC']),
             'CB|EQ': (nm['CB'], nm['EQ']), 'CB|TwinD': (nm['CB'], nm['TwinD']), 'CB|detector': (nm['CB'], det)}
    out['detector'] = dict(name=st.names[det], mass_L=float(mu['L'][det]), label=str(lab[det]), mutual_with_CB=bool(mut[nm['CB'], det]),
                           A_CB_det=int(A[nm['CB'], det]), A_det_CB=int(A[det, nm['CB']]), n_strict_invaders=int(ninv[det]))
    pb = {}
    for k, (x, y) in pairs.items():
        b = np.nonzero(st.selfc & mut[x] & mut[y])[0]
        b = [c for c in b if c not in (x, y)]
        pb[k] = dict(n=len(b), mass_L=float(mu['L'][b].sum()), n_est=int(sum(est[c] for c in b)),
                     n_nonexploitable=int(sum(1 for c in b if ninv[c] == 0)),
                     nonexploitable=[(st.names[c], float(mu['L'][c])) for c in sorted([c for c in b if ninv[c] == 0], key=lambda c: -mu['L'][c])[:8]],
                     exploitable=[(st.names[c], float(mu['L'][c]), int(ninv[c])) for c in sorted([c for c in b if ninv[c] > 0], key=lambda c: -mu['L'][c])[:6]])
    out['pairwise_bridges'] = pb
    # leak test
    lt = leak_test(A)
    closed = lt['closed']
    out['leak'] = dict(n_selfcoop=lt['n_selfcoop'], n_components=lt['n_components'], n_closed=lt['n_closed'], sizes=lt['sizes'],
                       closed_mass_L=float(sum(mu['L'][c].sum() for c in closed)),
                       closed_labels=dict(Counter(str(lab[x]) if est[x] else 'nonest' for c in closed for x in c)),
                       closed_heaviest=[(st.names[c[0]], float(mu['L'][c].sum()), len(c)) for c in sorted(closed, key=lambda c: -mu['L'][c].sum())[:10]])
    # tilt bookkeeping
    out['tilts'] = {}
    for cell in ('T1a', 'T1b', 'T1c', 'T2', 'T3', 'identity', 'tags', 'cbq'):
        pr = st.class_prior(cell)
        out['tilts'][cell] = dict(open_mass=float(pr[NCB].sum()), EQ=float(pr[nm['EQ']]), TC1=float(pr[nm['TC1^1']]), XC=float(pr[nm['XC']]),
                                  D=float(pr[st.iD]), identity=float(pr[lab == 'identity'].sum()), MC1=float(pr[nm['MC^1']]),
                                  marked_D=float(sum(pr[st.class_of(('D',), M)] for M in (1, 2, 3))))
    out['time_s'] = time.time() - t0
    json.dump(out, open(os.path.join(OUT, 'static_analysis.json'), 'w'), indent=1, default=str)
    print(json.dumps({k: out[k] for k in ('n_classes', 'n_est', 'F_CB', 'identity_cliques', 'cliques', 'ratio_M_over_max_identity_clique')}, default=str, indent=1))


# ------------------------------------------------------------------ validation (notes §1.12)
def _play_job(job):
    """Whole plays of spelling pairs: rows [(i, x, y)] -> [(i, 'C'|'D'|'BOT')]."""
    cat = _G['cat']
    out = []
    for i, x, y in job:
        L.CACHE.clear()
        out.append((i, L.play(cat.term(int(x)), cat.term(int(y)), cat.K)[0]))
    return out


def _prod_job(ks):
    cat = _G['cat']
    out = []
    for k in ks:
        lst = cat.produce_spelling(int(k))
        u = int(cat.sp_unit[k])
        out.append((int(k), lst == cat.u_list[u]))
    return out


def m2_list_changes(cat):
    """Milestone-2-shaped spellings (no new atom, no marker): does the list under the extended probes equal milestone
    2's production (probes CB, CB1, CBP)?"""
    m2 = CP.Catalogue(7, 'P', cat.K)
    conv = lambda at: ('chk', at[1], at[2], at[3])

    def cv(x):
        t = x[0]
        if t in ('C', 'D'): return x
        if t == 'A': return ('A', conv(x[1]))
        if t == 'not': return ('not', cv(x[1]))
        if t in ('and', 'or'): return (t, cv(x[1]), cv(x[2]))
        return ('if', cv(x[1]), cv(x[2]), cv(x[3]))
    n = 0; changed = []
    for k, s in enumerate(m2.spell):
        x = cv(m2.sexprs[s['i']])
        i = cat.sx_index[x]
        u = cat.unit_key[(int(cat.sx_dt[i]), 0, int(x == IT.CB_X))]
        n += 1
        if cat.u_list[u] != s['lst']:
            changed.append(IT.show(x))
    return dict(n=n, n_changed=len(changed), examples=changed[:12])


def cmd_validate(a):
    rng = np.random.default_rng(1010)
    out = {}
    st = Static()
    cat = st.cat
    z = load_static()
    A_u, self_u = z['A_u'], z['self_u']
    nw = min(a.workers, 3)
    # 2. compilation: eq, tags, markers
    tg = {}
    for M in IT.MSETS:
        prog = cat.term(cat.spelling_of(IT.CB_X, M))
        for t in (1, 2):
            v, _ = L.evaluate(IT.tag_term(t, ('quote', prog)))
            tg['CB%s tag%d' % (IT.MS_NAME[M], t)] = v
    for nm, p in (('PROG_C', L.PROG_C), ('PROG_D', L.PROG_D)):
        for t in (1, 2):
            tg['%s tag%d' % (nm, t)] = L.evaluate(IT.tag_term(t, ('quote', p)))[0]
    out['tags'] = tg
    out['tags_ok'] = all(tg['CB%s tag%d' % (IT.MS_NAME[M], t)] == ('T' if M & (1 << (t - 1)) else 'F') for M in IT.MSETS for t in (1, 2)) \
        and all(v == 'F' for k, v in tg.items() if k.startswith('PROG'))
    # 3. production
    progs, _ = C.build_arm(cat.K, 'S')
    out['production'] = dict(
        CB_equals_m4=C.h_getcerts(cat.term(cat.spelling_of(IT.CB_X, 0))) == C.h_getcerts(progs['CB']),
        CB1_equals_m4=C.h_getcerts(cat.term(cat.spelling_of(IT.CB1_X, 0))) == C.h_getcerts(progs['CB1']),
        CBP_equals_m4=C.h_getcerts(cat.term(cat.spelling_of(IT.CBP_X, 0))) == C.h_getcerts(progs['CBP']),
        CBquote_is_catalogue_CB=L.canon_term(cat.cb_term) == L.canon_term(cat.term(cat.spelling_of(IT.CB_X, 0))),
        named_lists={nm: [(e[0], C.show_script(e[1])) for e in C.uncons(cat.u_list[int(cat.sp_unit[cat.spelling_of(*IT.NAMED[nm])])])]
                     if cat.u_list[int(cat.sp_unit[cat.spelling_of(*IT.NAMED[nm])])] else [] for nm in IT.NAMED_ORDER})
    out['m2_list_changes'] = m2_list_changes(cat)
    print('production', out['production']['CB_equals_m4'], out['m2_list_changes']['n_changed'], flush=True)
    with Pool(nw, initializer=_init) as pool:
        # lists depend on (dt, M & tags) only: direct production on marked spellings
        ks = rng.choice(np.nonzero(cat.sp_M > 0)[0], a.prod_sample, replace=False)
        res = [r for part in pool.map(_prod_job, [ks[i:i + 25] for i in range(0, len(ks), 25)]) for r in part]
        out['lists_marker_reduction'] = dict(n=len(res), mismatches=sum(1 for _, ok in res if not ok))
        # 4. hand table; 5. Lemma T', R: random pairs; marked pairs; twins; self
        named = {nm: cat.spelling_of(*IT.NAMED[nm]) for nm in IT.NAMED_ORDER}
        pairs = [(named[x], named[y]) for x in IT.NAMED_ORDER for y in IT.NAMED_ORDER]
        nh = len(pairs)
        pairs += [tuple(int(v) for v in rng.integers(0, cat.nsp, 2)) for _ in range(a.sample)]
        mk = np.nonzero(cat.sp_M > 0)[0]
        pairs += [(int(rng.choice(mk)), int(rng.integers(cat.nsp))) for _ in range(a.sample // 4)]
        pairs += [(int(rng.integers(cat.nsp)), int(rng.choice(mk))) for _ in range(a.sample // 4)]
        multi = [u for u in range(cat.NU) if len(cat.members[u]) >= 2]
        for _ in range(a.sample // 4):
            u = multi[rng.integers(len(multi))]; x, y = rng.choice(cat.members[u], 2, replace=False)
            pairs.append((int(x), int(y)))
        # same body, marker sets differing (outside or inside the tags read)
        bodies_m = np.nonzero(cat.sp_M == 1)[0]
        for _ in range(a.sample // 4):
            k = int(rng.choice(bodies_m)); k0 = cat.spelling_of(cat.sexprs[int(cat.sp_sx[k])], 0)
            y = int(rng.integers(cat.nsp))
            pairs.append((k, y) if rng.random() < 0.5 else (y, k)); pairs.append((k0, y))
        for _ in range(a.sample // 8):
            x = int(rng.integers(cat.nsp)); pairs.append((x, x))
        jobs = [[(i, x, y) for i, (x, y) in list(enumerate(pairs))[s0:s0 + 200]] for s0 in range(0, len(pairs), 200)]
        played = dict(r for part in pool.imap_unordered(_play_job, jobs) for r in part)
        bad = []; hand_bad = []
        for i, (x, y) in enumerate(pairs):
            ux, uy = int(cat.sp_unit[x]), int(cat.sp_unit[y])
            pred = self_u[ux] if x == y else A_u[ux, uy]
            r = played[i]
            if (r == 'C') != bool(pred):
                bad.append((cat.name(x), cat.name(y), r, int(pred)))
            if i < nh:
                xn, yn = IT.NAMED_ORDER[i // len(IT.NAMED_ORDER)], IT.NAMED_ORDER[i % len(IT.NAMED_ORDER)]
                if r != IT.HAND[xn][i % len(IT.NAMED_ORDER)]: hand_bad.append((xn, yn, r))
        out['hand_table'] = dict(n=nh, mismatches=len(hand_bad), examples=hand_bad[:10])
        out['lemma_TR_sample'] = dict(n=len(pairs), mismatches=len(bad), examples=bad[:10])
        print('hand', out['hand_table'], 'lemma', out['lemma_TR_sample']['n'], out['lemma_TR_sample']['mismatches'], flush=True)
        # 8. executable = composed ideal on class representatives (whole plays)
        nc = st.nc
        mu = st.class_prior('L')
        heavy = list(np.argsort(-mu)[:a.exec_heavy])
        rnd = list(rng.choice(nc, a.exec_random, replace=False))
        nmc = list(st.named.values())
        sub = sorted(set(int(i) for i in heavy + rnd + nmc))
        cp = [(i, j) for i in sub for j in sub]
        jobs = [[(q, int(st.crep[i]), int(st.crep[j])) for q, (i, j) in list(enumerate(cp))[s0:s0 + 400]] for s0 in range(0, len(cp), 400)]
        t1 = time.time()
        played = dict(r for part in pool.imap_unordered(_play_job, jobs) for r in part)
        badc = [(st.names[i], st.names[j], played[q], int(st.A[i, j])) for q, (i, j) in enumerate(cp)
                if (played[q] == 'C') != bool(st.A[i, j]) and i != j]
        badself = [(st.names[i], played[q]) for q, (i, j) in enumerate(cp) if i == j and (played[q] == 'C') != bool(st.A[i, i])]
        nbot = sum(1 for v in played.values() if v == 'BOT')
        out['exec_vs_ideal'] = dict(n_classes=len(sub), n_cells=len(cp), mismatches=len(badc), self_mismatches=len(badself),
                                    BOT=nbot, examples=badc[:10], s=time.time() - t1)
        print('exec vs ideal', out['exec_vs_ideal'], flush=True)
    # 5b. soundness audit on the ideal keys: every T check against the composed play of its instance
    for aa in 'CD':
        kz = np.load(os.path.join(OUT, 'keys_%s.npz' % aa))
        inst, vals = kz['inst'], kz['vals']
        T = np.nonzero((vals == 1) & (inst[:, 2] >= 0))[0]
        ux = cat.sp_unit[inst[T, 2]]; uy = cat.sp_unit[inst[T, 3]]
        act = A_u[ux, uy]
        want = 1 if aa == 'C' else 0
        out['soundness_%s' % aa] = dict(n_true=int(len(T)), false_atoms=int((act != want).sum()))
    # 6. lumping: eq-clique spellings singletons; marked / unmarked CB separate
    eqd = cat.sx_dt[cat.sx_index[IT.EQ_X]]
    eqs = np.nonzero(cat.sp_dt == eqd)[0]
    out['lumping'] = dict(eq_spellings=len(eqs), eq_classes=len(set(int(st.cos[k]) for k in eqs)),
                          eq_singletons=all(st.n_spell[st.cos[k]] == 1 for k in eqs),
                          CB_marked_classes=[int(st.cos[cat.spelling_of(IT.CB_X, M)]) for M in IT.MSETS],
                          CB_class_size=int(st.n_spell[st.named['CB']]),
                          CB_class_members=[cat.name(int(k)) for k in np.nonzero(st.cos == st.named['CB'])[0][:12]])
    # spelling-level criterion on random merged pairs against a sample of opponents (composed table)
    multi_cls = [c for c in range(st.nc) if st.n_spell[c] >= 2]
    viol = 0; nchk = 0
    for _ in range(300):
        c = multi_cls[rng.integers(len(multi_cls))]
        ks = np.nonzero(st.cos == c)[0]
        x, y = rng.choice(ks, 2, replace=False)
        ux, uy = cat.sp_unit[x], cat.sp_unit[y]
        zs = rng.integers(0, cat.nsp, 200)
        uz = cat.sp_unit[zs]
        nchk += 1
        ok = np.array_equal(A_u[ux, uz], A_u[uy, uz]) and np.array_equal(A_u[uz, ux], A_u[uz, uy]) and self_u[ux] == self_u[uy] \
            and A_u[ux, uy] == self_u[ux] and A_u[uy, ux] == self_u[uy]
        viol += not ok
    out['lumping']['criterion_sample'] = dict(n=nchk, violations=viol)
    # 7. families on the named sub-catalogue
    nmn = ['CB', 'MC^1', 'TC1^1', 'AF^1', 'OF^1', 'EQ', "EQ'", 'TwinD', 'XC', "XC'"]
    idx = np.array([st.named[n] for n in nmn])
    cl, comp, comps = IT.maximal_cliques(st.A, idx)
    inv = {int(st.named[n]): n for n in nmn}
    out['named_families'] = dict(cliques=sorted([sorted(inv[c] for c in q) for q in cl]),
                                 components=sorted([sorted(inv[c] for c in q) for q in comps]),
                                 strict_invaders={n: [st.names[q] for q in IT.strict_invaders(st.U, st.named[n])[:5]] for n in ('MC^1', 'OF^1', 'AF^1', 'TC1^1', 'XC')},
                                 n_strict_invaders={n: int(len(IT.strict_invaders(st.U, st.named[n]))) for n in ('MC^1', 'OF^1', 'AF^1', 'TC1^1', 'XC', 'CB')})
    # 9. the tilts' seed laws
    laws = {}
    for cell in ('T1a', 'T1b', 'T1c', 'T2', 'T3'):
        w = st.spelling_prior(cell)
        Mm = st.family_mass()
        if cell == 'T1a': blk = [cat.spelling_of(IT.EQ_X, 0)]
        elif cell == 'T1b': blk = st.heaviest_spellings_of_dt(IT.EQ_X, 10)
        elif cell == 'T1c': blk = st.heaviest_spellings_of_dt(IT.CB_X, 10)
        elif cell == 'T2': blk = [cat.spelling_of(IT.TC1_X, 1)]
        else: blk = [cat.spelling_of(IT.XC_X, 0)]
        mu = st.mass(w)
        draws = rng.multinomial(200000, mu)
        bc = sorted({int(st.cos[k]) for k in blk})
        laws[cell] = dict(M=Mm, block_mass=float(w[blk].sum()), block_spellings=[cat.name(k) for k in blk],
                          block_classes=len(bc), empirical_block=float(draws[bc].sum() / 200000), total=float(w.sum()))
    out['tilts'] = laws
    json.dump(out, open(os.path.join(OUT, 'validate.json'), 'w'), indent=1, default=str)
    print(json.dumps({k: v for k, v in out.items() if k not in ('production',)}, default=str)[:4000], flush=True)


# ------------------------------------------------------------------ the chain (diagnostic)
def chain_cell(job):
    """milestone 2's chain_cell over this experiment's classes: (label, N, log_theta, fast)."""
    from chain_log import LogChain, NEG
    from dollar_partitions import ClassProvider
    import solver_audit as SA
    import carrier_populations_run as CPR
    from carrier_populations_report import leak_test
    label, N, log_theta, fast = job
    t0 = time.time()
    st = Static()
    A = st.A.copy()
    mu = st.class_prior('L')
    names = list(st.names)
    lab = st.label()
    keep = np.arange(A.shape[0])
    dropped = []
    if label == 'noclosed':
        while True:
            lt = leak_test(A[np.ix_(keep, keep)])
            cl = sorted({int(keep[i]) for c in lt['closed'] for i in c})
            if not cl: break
            dropped += cl
            ks = set(cl)
            keep = np.array([k for k in keep if k not in ks])
    A = A[np.ix_(keep, keep)]; mu = mu[keep]; mu = mu / mu.sum(); names = [names[k] for k in keep]; lab = lab[keep]
    U, PCC = CP.pay_matrix(A)
    nc = len(mu)
    iD = int(np.nonzero(keep == st.iD)[0][0])
    cfn = os.path.join(OUT, 'chain_seeds_%s.json' % label)
    if os.path.exists(cfn):
        seeds = [tuple(s) for s in json.load(open(cfn))]
    else:
        pool = np.argsort(-mu)[:120]
        cands, counts = SA.enumerate_candidates_fast(U, mu, pool=pool)
        S1, n1, comp1 = SA.invasion_closure(U, mu, max_nodes=6000, branch=3)
        seeds = [(x['ids'], x['x']) for x in cands + S1 if x['size'] > 1 and x['status'] == 'stable']
        json.dump([[list(map(int, s[0])), list(map(float, s[1]))] for s in seeds], open(cfn, 'w'))
    CH = CPR.fast_chain_class() if fast else LogChain
    ch = CH(ClassProvider(U, mu), N=N, w=0.3, Ufull=U, twins=True, theta=1.0, max_states=10 ** 9)
    ch.explore_log(extra_states=[(list(s[0]), list(s[1])) for s in seeds], log_theta=log_theta,
                   max_states=int(os.environ.get('IT_MAX_STATES', 60000)), verbose=False)
    keys_all, lpi_all, sinfo, out_un, rec = ch.solve_sparse()
    keys = [keys_all[i] for i in rec]
    pi = np.exp(lpi_all[rec])
    LA, _ = ch.log_matrix(keys)
    pcc = 0.0; piD = 0.0; coop = np.zeros(len(keys))
    for i, k in enumerate(keys):
        ids, x, kind = ch.states[k]; ids = list(ids); x = np.asarray(x)
        c = float(x @ PCC[np.ix_(ids, ids)] @ x); coop[i] = c; pcc += pi[i] * c
        if kind == 'mono' and ids[0] == iD: piD += pi[i]
    tot_flow = 0.0
    for i in range(len(keys)):
        row = LA[i].copy(); row[i] = NEG
        f = row[np.isfinite(row)]
        if len(f): tot_flow += pi[i] * float(np.exp(np.logaddexp.reduce(f)))
    cut = float(sum(float(np.exp(np.logaddexp.reduce([lpi_all[i] + lw for i, lw in lst]))) for k2, lst in out_un.items()))

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
        for j in np.argsort(-np.where(fin, row, -np.inf))[:3]:
            if not fin[j]: break
            muts = sorted(ch.lmut.get((k, keys[j]), {}).items(), key=lambda kv: -kv[1])[:2]
            ex.append(dict(to=desc(keys[j]), log10_rate=float(row[j] / math.log(10)), mutants=[(names[q], float(v / math.log(10))) for q, v in muts]))
        ids = list(ch.states[k][0])
        support.append(dict(state=desc(k), pi=float(pi[i]), coop=float(coop[i]), labels=[str(lab[q]) for q in ids],
                            mass=[float(mu[q]) for q in ids], log10_exit=lex / math.log(10) if np.isfinite(lex) else None, exits=ex))
    top = None
    ci = [i for i in order if coop[i] >= 0.95]
    if ci:
        i = ci[0]; k = keys[i]
        ids, x, kind = ch.states[k]; ids = list(ids); x = np.asarray(x)
        uaa = float(x @ U[np.ix_(ids, ids)] @ x)
        tot = dict(neutral=0.0, strict=0.0, deleterious=0.0); exits = []
        for k2 in ch.ledge.get(k, {}):
            if k2 == k: continue
            for q, lw in ch.lmut.get((k, k2), {}).items():
                d1 = float(U[q, ids] @ x - uaa)
                typ = 'strict' if d1 > 1e-9 else ('neutral' if d1 > -1e-9 else 'deleterious')
                r = ch.edge_rho.get((k, k2, q))
                tot[typ] += math.exp(lw)
                exits.append(dict(mutant=names[q], type=typ, d1=d1, rate=math.exp(lw), N_rho=(N * r[0]) if r else None))
        exits.sort(key=lambda e: -e['rate'])
        top = dict(state=desc(k), pi=float(pi[i]), **{'exit_' + kk: v for kk, v in tot.items()}, exits=exits[:8])
    # pi by family label of the support's classes (cooperative states)
    pi_lab = defaultdict(float)
    for i, k in enumerate(keys):
        ids, x, kind = ch.states[k]
        for q, xi in zip(ids, x): pi_lab[str(lab[q])] += pi[i] * xi
    return dict(label=label, N=N, log10_theta=log_theta / math.log(10), fast=fast, n_classes=nc, n_dropped=len(dropped),
                dropped_labels=dict(Counter(str(st.label()[k]) for k in dropped)), n_seeds=len(seeds),
                n_expanded=len(keys_all), n_recurrent=len(keys), pcc=pcc, pi_D=piD,
                pi_coop=float(pi[coop >= 0.95].sum()), pi_by_label=dict(pi_lab), cut_rel=cut / tot_flow if tot_flow > 0 else None,
                support=support, top_coop=top, time_s=time.time() - t0)


def cmd_chain(a):
    path = os.path.join(OUT, 'chain.json')
    rows = json.load(open(path)) if os.path.exists(path) else []
    jobs = [(lb, N, math.log(a.theta), bool(a.fast)) for lb in a.labels for N in a.N]
    done = {(r['label'], r['N']) for r in rows}
    jobs = [j for j in jobs if (j[0], j[1]) not in done]
    with Pool(min(a.workers, 3, max(1, len(jobs)))) as pool:
        for r in pool.imap_unordered(chain_cell, jobs, chunksize=1):
            rows.append(r)
            json.dump(rows, open(path, 'w'), indent=1, default=str)
            print('%s N=%d: P(C,C) %.4f pi(D) %.4f top %s (%.0fs)' % (r['label'], r['N'], r['pcc'], r['pi_D'],
                  r['support'][0]['state'] if r['support'] else None, r['time_s']), flush=True)


# ------------------------------------------------------------------ main
def cmd_static(a):
    compute_static(min(a.workers, 3))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('static'); s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('lottery')
    s.add_argument('--cells', nargs='+', default=['L']); s.add_argument('--runs', type=int, default=40)
    s.add_argument('--gens', type=int, default=2000); s.add_argument('--gens_ext', type=int, default=10000)
    s.add_argument('--out', default='main'); s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('analyze')
    s = sub.add_parser('validate')
    s.add_argument('--sample', type=int, default=2000); s.add_argument('--prod_sample', type=int, default=200)
    s.add_argument('--exec_heavy', type=int, default=150); s.add_argument('--exec_random', type=int, default=150)
    s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('chain')
    s.add_argument('--labels', nargs='+', default=['main']); s.add_argument('--N', type=int, nargs='+', default=[10000])
    s.add_argument('--theta', type=float, default=1e-14); s.add_argument('--fast', type=int, default=1)
    s.add_argument('--workers', type=int, default=3)
    a = ap.parse_args()
    {'static': cmd_static, 'lottery': cmd_lottery, 'chain': cmd_chain, 'validate': cmd_validate, 'analyze': cmd_analyze}[a.cmd](a)
