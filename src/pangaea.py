"""Cliques on a Pangaea (spec specs/2026-10-16-pangaea.md, notes notes/pangaea.md).

Imports provenance's and the realizable-scaling run's machinery unchanged and adds:
  - founders: one list of N*I founders per (total, replicate), cut by a nested uniform partition into every geometry
    (notes §1.2), with the proportional control, C-donor (1 donor or 0.1%) and free certificates (H);
  - a run object with the cell's production rate r (constant 100 or native N/2), its migration rate and the overlap-free
    kernel (src/pangaea_kern.py);
  - the network decomposition of a population (notes §1.5), resolution/loss on the S-nonself closure;
  - the fission-fusion merge of an archipelago into one population;
  - deterministic family dynamics with certificates saturated (H units).
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import provenance as PV
import provenance_run as PR
import realizable_scaling as RS            # registers the scaling cells and patches PR.founders (kept for validation)
import pangaea_kern as PK

SALT_PG = 20261016
W = 0.3
TOTALS = (12800, 6400)
GEOMS = {12800: [(100, 128), (200, 64), (800, 16), (3200, 4), (12800, 1)],
         6400: [(100, 64), (400, 16), (1600, 4), (6400, 1)]}
R_CONST = 100
_RS_FOUNDERS = PR.founders                 # realizable_scaling's dispatcher (provenance's own founders underneath)

AP_NAME = 'if(CHK(them,^D,D),D,C)'
PB_NAME = 'if(and(CHK(them,me,C),CHK(them,^D,D)),C,D)'
CLASSES = ['D', 'Dill', 'S', 'S-', 'PBn', 'CBo', 'BR', 'APn', 'TW', 'Eo']


def mN_cal(N):
    return (N / 100.0) ** 0.7


# ------------------------------------------------------------------------------------------------ founders (§1.2)
def base_list(T, rep, LS):
    return np.random.default_rng([T, rep, SALT_PG]).choice(len(LS['mu']), size=T, p=LS['mu'])


def proportional(lst, T, rep, LS):
    """Every Q entry redrawn from the non-Q spellings proportional to mu, in list order (stream 6)."""
    Q = set(LS['Q'].tolist())
    mu = LS['mu']
    nonq = np.ones(len(mu), bool); nonq[LS['Q']] = False
    idx = np.nonzero(nonq)[0]
    pr = mu[idx] / mu[idx].sum()
    r = np.random.default_rng([T, rep, SALT_PG, 6])
    out = lst.copy()
    for j in range(T):
        if int(out[j]) in Q:
            out[j] = int(idx[r.choice(len(idx), p=pr)])
    return out


def permutation(T, rep):
    return np.random.default_rng([T, rep, SALT_PG, 9]).permutation(T)


def partition(lst, N, I, perm):
    """Nested uniform partition: the permuted list cut into I consecutive blocks of N."""
    assert N * I == len(lst)
    return lst[perm].reshape(I, N)


def donors(T, rep, k, LS):
    """k donor positions (distinct, in list coordinates) and their spellings (stream 3)."""
    r = np.random.default_rng([T, rep, SALT_PG, 3])
    pos = r.choice(T, size=k, replace=False)
    pd = LS['mu'] * LS['donor_ok']; pd = pd / pd.sum()
    sp = r.choice(len(LS['mu']), size=k, p=pd)
    return pos, sp


def founder_list(T, rep, prior, LS):
    """(spellings, rules) over the list coordinates for a prior/spec tag."""
    lst = base_list(T, rep, LS)
    if prior == 'prop':
        lst = proportional(lst, T, rep, LS)
    rule = np.full(T, PV.R_SNON, np.int64)
    if prior == 'H':
        rule[:] = PV.R_H
    elif prior.startswith('Cdon'):
        k = int(prior[4:]) if len(prior) > 4 else 1
        rule[:] = PV.R_C
        pos, sp = donors(T, rep, k, LS)
        lst = lst.copy()
        lst[pos] = sp; rule[pos] = PV.R_H
    return lst, rule


# ------------------------------------------------------------------------------------------------ cells (§1.4)
PG = {}          # cell -> dict(T, N, I, prior, r, mN, merge_at)


def cell_name(prior, N, I, rarm='c', merge_at=0):
    s = 'pg_%s_%d_%d_%s' % (prior, N, I, 'r100' if rarm == 'c' else 'rnat')
    return s + ('_ff%d' % merge_at if merge_at else '')


def register(prior, N, I, rarm='c', merge_at=0):
    T = N * I
    name = cell_name(prior, N, I, rarm, merge_at)
    r = R_CONST if rarm == 'c' else N // 2
    PG[name] = dict(T=T, N=N, I=I, prior=prior, r=r, rarm=rarm, mN=(mN_cal(N) if I > 1 else 0.0), merge_at=merge_at)
    spec = {'H': 'H'}.get(prior, 'Cdonor' if prior.startswith('Cdon') else 'S-nonself')
    PR.CELLS[name] = (N, I, spec, 'pg:' + prior, 'ext')
    return name


def all_cells():
    out = {}
    out['A'] = [register('L', N, I) for T in TOTALS for (N, I) in GEOMS[T]]
    out['B'] = [register('prop', N, I) for (N, I) in GEOMS[12800]] + [register('prop', 6400, 1)]
    out['B2'] = [register('prop', N, I) for (N, I) in [(100, 64), (400, 16), (1600, 4)]]
    out['C'] = [register('L', N, I, 'n') for (N, I) in [(100, 128), (800, 16), (100, 64), (400, 16)]]
    out['D'] = [register('Cdon', 12800, 1), register('Cdon', 6400, 1)]
    out['D2'] = [register('Cdon13', 12800, 1), register('Cdon6', 6400, 1)]
    out['E'] = [register('H', 12800, 1)]
    out['F'] = [register('L', 100, 128, merge_at=200), register('L', 100, 128, merge_at=1000)]
    return out


ALL = all_cells()


def founders_pg(cell, rep, LS):
    if cell not in PG:
        return _RS_FOUNDERS(cell, rep, LS)
    c = PG[cell]
    T, N, I = c['T'], c['N'], c['I']
    lst, rule = founder_list(T, rep, c['prior'], LS)
    perm = permutation(T, rep)
    sp = partition(lst, N, I, perm)
    ru_ = partition(rule, N, I, perm)
    t = LS['tau'][sp]
    unit = np.where(ru_ == PV.R_H, LS['Hu'][t], LS['Eu'][t])
    return sp, ru_, unit


PR.founders = founders_pg


def kernel_seed_pg(N, I, rep):
    return int((rep * 1000003 + N * 10007 + I * 101 + SALT_PG) % (2 ** 62))


class PGRun(PR.Run):
    """Provenance's run object with the cell's r, mN, seed and the overlap-free kernel.  legacy=True keeps the stored
    scaling run's conventions (r = N/2, provenance's seed, RS.CELL_MN) for the draw-for-draw reproduction."""

    def __init__(self, cell, rep, legacy=False):
        super().__init__(cell, rep)
        if legacy or cell not in PG:
            self.mN = RS.CELL_MN.get(cell, 1.0)
            self.r = self.N // 2
        else:
            c = PG[cell]
            self.mN = c['mN']
            self.r = c['r']
            self.seed = kernel_seed_pg(self.N, self.I, rep)

    def advance(self, gens):
        LS, st = self.LS, self.LS['st']
        self.g = PK.segment(self.g, gens, self.seed, self.N, W, self.mN / self.N, self.r, self.slots, self.counts,
                            self.paysum, self.pres, self.npres, self.pos, self.spcount, self.d, self.tunit, self.trule,
                            self.tsp, self.tanc, self.ntv, st['utau'], st['BLC'], st['BLD'], st['SINGLE'], st['APP'],
                            LS['PRODC'], LS['PD'], st['KIND'], st['NAT'], st['CHC'], st['CHD'], st['UVt'], self.A,
                            self.selfa, LS['OSV'], LS['SPO'], LS['capable'], LS['COSTS'], self.ctr, self.steps_rule,
                            self.wn, self.wenc, self.wsp, self.wcode, self.wsid, self.ckey, self.cval, self.ncache,
                            self.plog, self.hist_wait, self.hist_acq, self.hist_steps, self.hist_cens, self.nprod,
                            LS['ident'], LS['spo_unit'], self.tset, self.uns, self.rulecount, self.enc_exp, self.skip,
                            LS['FUT'], self.fcount, self.enc_futile, self.err)
        if self.err[0] != 0:
            raise RuntimeError('kernel error %d in %s rep %d at generation %d' % (self.err[0], self.cell, self.rep,
                                                                                 self.g))

    # -------------------------------------------------------------------------------- fission-fusion (§1.2)
    def merge(self, new_seed):
        """All islands into one population of N*I (types, per-individual logs and counters carried; island-local
        bookkeeping rebuilt).  Event indexing continues from self.g; the seed changes."""
        LS, st = self.LS, self.LS['st']
        I, N = self.I, self.N
        T = I * N
        KCAP = self.tunit.shape[0]
        self.slots = self.slots.reshape(1, T).copy()
        self.N, self.I = T, 1
        self.counts = np.zeros((1, KCAP), np.int64)
        np.add.at(self.counts[0], self.slots[0], 1)
        ks = np.nonzero(self.counts[0])[0]
        self.pres = np.zeros((1, T), np.int64); self.npres = np.array([len(ks)], np.int64)
        self.pos = -np.ones((1, KCAP), np.int64)
        for tt, k in enumerate(ks):
            self.pres[0, tt] = k; self.pos[0, k] = tt
        self.paysum = np.zeros((1, KCAP))
        PV.init_paysum(self.counts, self.paysum, self.pres, self.npres, self.tunit, self.tsp, self.A, self.selfa)
        self.spcount = self.spcount.sum(0, keepdims=True)
        self.wn = np.zeros((1, T), np.int64); self.wenc = np.zeros((1, T), np.int64)
        self.wsp = np.zeros((1, T, 3), np.int64); self.wcode = np.zeros((1, T, 3), np.int64)
        self.wsid = np.zeros((1, T, 3), np.int64)
        self.ckey = np.zeros((1, T, PV.CACHE_CAP), np.int64); self.cval = np.zeros((1, T, PV.CACHE_CAP), np.int64)
        self.ncache = np.zeros((1, T), np.int64)
        self.plog = self.plog.reshape(1, T, 5).copy()
        self.uns = np.zeros(1, np.int64)
        self.rulecount[:] = 0; self.fcount[:] = 0
        PV.init_uns(self.slots, self.tunit, self.trule, self.tset, st['BLC'], st['BLD'], LS['PD'], st['utau'],
                    LS['FUT'], self.uns, self.rulecount, self.fcount)
        self.maj_k = np.zeros(1, np.int64); self.maj_n = np.zeros(1, np.int64)
        self.seed = new_seed
        self.mN = 0.0


# ------------------------------------------------------------------------------------------------ statics
_X = {}


def statics(LS):
    """Reference units and the spelling classes of notes §1.1 (H state)."""
    if 'cls' in _X: return _X
    st = LS['st']
    A = np.asarray(st['A']); selfa = np.asarray(st['selfa'])
    names, tau, Hu = LS['names'], LS['tau'], LS['Hu']
    cH = int(Hu[tau[names.index('C')]]); dH = int(LS['u_d']); cbH = int(LS['u_cb'])
    apH = int(Hu[tau[names.index(AP_NAME)]]); pbH = int(Hu[tau[names.index(PB_NAME)]])
    Q = set(LS['Q'].tolist())
    cls = np.zeros(len(names), np.int64)
    for k in range(len(names)):
        u = int(Hu[tau[k]])
        if k in Q: c = 'TW'
        elif A[u, dH] == 1: c = 'S' if selfa[u] == 1 else 'S-'
        elif selfa[u] != 1: c = 'Dill' if A[apH, u] == 1 else 'D'
        else:
            mcb = A[u, cbH] == 1 and A[cbH, u] == 1
            map_ = A[u, apH] == 1 and A[apH, u] == 1
            mpb = A[u, pbH] == 1 and A[pbH, u] == 1
            if mcb and map_: c = 'BR'
            elif mcb: c = 'PBn' if mpb else 'CBo'
            elif map_: c = 'APn'
            else: c = 'Eo'
        cls[k] = CLASSES.index(c)
    _X.update(cls=cls, cH=cH, dH=dH, cbH=cbH, apH=apH, pbH=pbH,
              R_sp=np.asarray(LS['R'], np.int64), Q_sp=np.asarray(LS['Q'], np.int64),
              BR_sp=np.nonzero(cls == CLASSES.index('BR'))[0])
    return _X


# ------------------------------------------------------------------------------------------------ decomposition (§1.5)
def decompose(R, cc=None, closure=False):
    """Network decomposition of the whole metapopulation (notes §1.5).  cc: island P(C,C) (computed if None)."""
    LS, st = R.LS, R.LS['st']
    X = statics(LS)
    A = np.asarray(R.A); selfa = np.asarray(R.selfa)
    nt = int(R.ntv[0])
    gc = R.counts[:, :nt].sum(0)
    K = np.nonzero(gc)[0].astype(np.int64)
    c = gc[K].astype(float)
    tot = c.sum()
    U = R.tunit[K]
    if cc is None: cc = R.island_stats()
    M = PK.mutual_matrix(K, R.tunit, R.tsp, R.A, R.selfa)
    selfc = np.diag(M).copy()
    S = np.nonzero(selfc)[0]
    out = dict(pcc=float(np.mean(cc)), n_types=int(len(K)), coop=float(c[S].sum() / tot))
    openu = np.asarray(LS['openu']); ident = np.asarray(LS['ident'])
    BLC = np.asarray(st['BLC'])
    certified = BLC[U, 0] >= 0
    if len(S):
        net = PK.dominant_network(M, S.astype(np.int64), c, K)
        inM = np.zeros(len(K), bool); inM[net] = True
        hk = int(K[net[0]]); hu = int(R.tunit[hk])
        out.update(M=float(c[inM].sum() / tot), M_n=int(len(net)), h_sp=LS['names'][int(R.tsp[hk])],
                   h_open=bool(openu[hu]), outside=float(c[S].sum() / tot - c[inM].sum() / tot),
                   M_of_cert=float(c[inM & certified].sum() / max(1.0, c[certified].sum())))
    else:
        inM = np.zeros(len(K), bool)
        out.update(M=0.0, M_n=0, h_sp=None, h_open=False, outside=0.0, M_of_cert=0.0)
    coopv = selfc
    mut = lambda ref: (A[U, ref] == 1) & (A[ref, U] == 1)
    out['target'] = float(c[coopv & mut(X['pbH'])].sum() / tot)
    out['open_coop'] = float(c[coopv & openu[U]].sum() / tot)
    out['ident'] = float(c[ident[U]].sum() / tot)
    out['Q'] = float(c[np.isin(R.tsp[K], X['Q_sp'])].sum() / tot)
    out['APnet'] = float(c[coopv & mut(X['apH']) & ~openu[U]].sum() / tot)
    out['sucker'] = float(c[A[U, X['dH']] == 1].sum() / tot)
    out['uncert_coop'] = float(c[coopv & ~certified].sum() / tot)
    out['cert'] = float(c[certified].sum() / tot)
    cap = np.asarray(LS['capable'])[np.asarray(st['utau'])[U]]
    out['cert_of_capable'] = float(c[certified & cap].sum() / max(1.0, c[cap].sum()))
    cl = X['cls'][R.tsp[K]]
    out['cls'] = [float(c[cl == j].sum() / tot) for j in range(len(CLASSES))]
    out['universal'] = bool(out['M'] >= 0.95)
    out['universal_open'] = bool(out['M'] >= 0.95 and out['h_open'])
    if closure:
        out.update(closure_status(R, K, U, selfc, inM))
    return out


def closure_status(R, K, U, selfc, inM):
    """resolved / lost / unresolved (notes §1.5).  The S-nonself closure of the living units against the living units
    (copying rules: no closure; the label is computed on the living set and flagged)."""
    LS, st = R.LS, R.LS['st']
    A = np.asarray(R.A); sa = np.asarray(R.selfa)
    lu = np.array(sorted(set(U.tolist())), np.int64)
    rules = set(R.trule[K].tolist())
    reach = np.zeros(len(sa), np.bool_)
    if rules <= {PV.R_SNON, PV.R_H}:
        PV.nonself_closure(lu, lu, np.asarray(st['utau']), np.asarray(st['KIND']), np.asarray(st['NAT']),
                           np.asarray(st['CHD']), np.asarray(st['UVt']), np.asarray(st['BLC']), np.asarray(st['BLD']),
                           LS['PRODC'], LS['PD'], np.asarray(st['APP']), reach)
        flag = 'closure'
    else:
        flag = 'living-only'
    reach[lu] = True
    ru_ = np.nonzero(reach & (sa == 1))[0]
    if not selfc.any() and len(ru_) == 0:
        return dict(status='lost', status_flag=flag)
    if not inM.any():
        return dict(status='unresolved', status_flag=flag)
    Mu = np.array(sorted(set(U[inM].tolist())), np.int64)
    outside_living = bool((selfc & ~inM).any())
    ok = np.ones(len(ru_), bool)
    for mu_ in Mu.tolist():
        ok &= (A[ru_, mu_] == 1) & (A[mu_, ru_] == 1)
    ok |= np.isin(ru_, Mu)
    if not outside_living and ok.all():
        return dict(status='resolved', status_flag=flag)
    return dict(status='unresolved', status_flag=flag, n_reach_outside=int((~ok).sum()))


# ------------------------------------------------------------------------------------------------ deterministic control
def determ(LS, prior='L', gens=2000, dt=0.1, every=10):
    """Deterministic family dynamics with certificates saturated (H units, notes §1.8): one infinite well-mixed
    population, Moran mean field dx_k/dt = x_k (exp(w f_k) / mean - 1) per generation, from the prior.  Types are H units,
    except that spellings of units whose twin play differs from self-play are kept apart (identity units)."""
    st = LS['st']
    A = np.asarray(st['A']); selfa = np.asarray(st['selfa'])
    X = statics(LS)
    mu = LS['mu'].copy()
    if prior == 'prop':
        nonq = np.ones(len(mu), bool); nonq[LS['Q']] = False
        mu = np.where(nonq, mu, 0.0); mu = mu / mu.sum()
    tau, Hu = LS['tau'], LS['Hu']
    us = Hu[tau]
    key = {}
    tu, tsp, x = [], [], []
    for k in range(len(mu)):
        if mu[k] <= 0: continue
        u = int(us[k])
        kk = (u, k) if A[u, u] != selfa[u] else (u, -1)
        if kk not in key:
            key[kk] = len(tu); tu.append(u); tsp.append(k); x.append(0.0)
        x[key[kk]] += mu[k]
    tu = np.array(tu); x = np.array(x)
    n = len(tu)
    a = A[np.ix_(tu, tu)].astype(float)
    np.fill_diagonal(a, selfa[tu])
    P = -1.0 + 2.0 * a.T - a                  # P[k, j]: k's payoff against j
    openu = np.asarray(LS['openu'])
    coop = selfa[tu] == 1
    mutpb = (A[tu, X['pbH']] == 1) & (A[X['pbH'], tu] == 1)
    mutap = (A[tu, X['apH']] == 1) & (A[X['apH'], tu] == 1)
    ident = np.asarray(LS['ident'])[tu]
    cls = X['cls'][np.array(tsp)]
    traj = []
    steps = int(round(every / dt))
    g = 0.0
    for blk in range(int(gens / every) + 1):
        if blk > 0:
            for _ in range(steps):
                f = P @ x
                e = np.exp(W * (f - f.max()))
                x = x * np.exp(dt * (e / (x @ e) - 1.0))
                x /= x.sum()
            g += every
        pcc = float(x @ (a * a.T) @ x)
        cs = [float(x[cls == j].sum()) for j in range(len(CLASSES))]
        traj.append(dict(g=g, pcc=pcc, target=float(x[coop & mutpb].sum()), open=float(x[coop & openu[tu]].sum()),
                         APnet=float(x[coop & mutap & ~openu[tu]].sum()), ident=float(x[ident].sum()), cls=cs))
    top = np.argsort(-x)[:10]
    return dict(prior=prior, n_types=n, traj=traj,
                final_top=[(LS['names'][tsp[k]], float(x[k]), bool(openu[tu[k]]), bool(mutpb[k])) for k in top])
