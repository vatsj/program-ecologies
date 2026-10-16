"""The realizable lottery along paths in (N, I, mN) (spec specs/2026-10-14-realizable-scaling.md, notes
notes/realizable-scaling.md).  Imports provenance's machinery unchanged; adds:

  - founders for the proportional control, the crossed TwinD-count panel and dense C-donor (notes §1.3);
  - a run object with a migration rate mN (m = mN/N per Moran event; the coin is event-indexed, so mN arms are
    paired draw for draw);
  - the failure classifier and the static absorbing check (notes §1.6), written over plain arrays so that constructed
    archipelagos can be tested;
  - the exact two-type Moran fixation probability under the kernel's birth-death step.
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import provenance as PV
import provenance_run as PR

SALT = PR.SALT
W = 0.3
_ORIG_FOUNDERS = PR.founders


def mN_cal(N):
    """The calibrated migration rate of the spec: (N/100)^0.7."""
    return (N / 100.0) ** 0.7


def t_ext(N, I):
    """Main cells' extended horizon (amendment 5): 10,000 (I N^0.3)/(64 100^0.3), capped at 40,000."""
    return int(min(40000, round(10000 * I * N ** 0.3 / (64 * 100 ** 0.3))))


# ------------------------------------------------------------------------------------------------ founders (§1.3)
def _base_sp(N, I, rep, LS):
    rng = np.random.default_rng([N, I, rep, SALT])
    return rng.choice(len(LS['mu']), size=(I, N), p=LS['mu'])


def replace_Q_proportional(sp, N, I, rep, LS):
    """Every Q founder redrawn from the non-Q spellings proportional to mu (stream 6)."""
    Q = set(LS['Q'].tolist())
    mu = LS['mu'].copy()
    nonq = np.ones(len(mu), bool); nonq[LS['Q']] = False
    idx = np.nonzero(nonq)[0]
    pr = mu[idx] / mu[idx].sum()
    r = np.random.default_rng([N, I, rep, SALT, 6])
    sp = sp.copy()
    for i in range(I):
        for j in range(N):
            if int(sp[i, j]) in Q:
                sp[i, j] = int(idx[r.choice(len(idx), p=pr)])
    return sp


def place_Q(sp, c, N, I, rep, LS):
    """c TwinD-family copies at uniformly chosen slots (stream 7), spellings proportional to mu restricted to Q
    (stream 8); the displaced founders are overwritten (they were drawn from the non-identity prior)."""
    sp = sp.copy()
    if c <= 0: return sp
    Qs = LS['Q']
    pq = LS['mu'][Qs] / LS['mu'][Qs].sum()
    pos = np.random.default_rng([N, I, rep, SALT, 7]).choice(N * I, size=c, replace=False)
    sq = np.random.default_rng([N, I, rep, SALT, 8]).choice(len(Qs), size=c, p=pq)
    for p_, s_ in zip(pos.tolist(), sq.tolist()):
        sp[p_ // N, p_ % N] = int(Qs[s_])
    return sp


def founders_rs(cell, rep, LS):
    """Provenance's founders for its own priors and specs; this run's priors 'prop' and 'crossC' (C an integer) and
    the spec 'Cdonor_dense'."""
    N, I, spec, prior, which = PR.CELLS[cell]
    if prior in ('L', 'ablation') and spec != 'Cdonor_dense':
        return _ORIG_FOUNDERS(cell, rep, LS)
    nsp = len(LS['mu'])
    sp = _base_sp(N, I, rep, LS)
    if prior == 'ablation':
        raise ValueError('ablation with dense donors is not a cell of this run')
    if prior == 'prop' or prior.startswith('cross'):
        sp = replace_Q_proportional(sp, N, I, rep, LS)
    if prior.startswith('cross'):
        sp = place_Q(sp, int(prior[5:]), N, I, rep, LS)
    if spec == 'Cdonor_dense':
        rule = np.full((I, N), PV.R_C, np.int64)
        k = int(math.ceil(N / 100))
        r_don = np.random.default_rng([N, I, rep, SALT, 5])
        pd = LS['mu'] * LS['donor_ok']; pd = pd / pd.sum()
        for i in range(I):
            js = r_don.choice(N, size=k, replace=False)
            for j in js.tolist():
                sp[i, j] = int(r_don.choice(nsp, p=pd)); rule[i, j] = PV.R_H
    else:
        rule = np.full((I, N), PV.RULE_OF[spec], np.int64)
    t = LS['tau'][sp]
    unit = np.where(rule == PV.R_H, LS['Hu'][t], LS['Eu'][t])
    return sp, rule, unit


PR.founders = founders_rs           # Run.__init__ resolves `founders` in provenance_run's namespace at call time


# ------------------------------------------------------------------------------------------------ cells (§1.4)
CELL_MN = {}                         # cell -> mN
CELL_INFO = {}                       # cell -> dict(rule label, path tags, main flag, T_ext)

RULES = {'Snon': ('S-nonself', 'L'), 'abl': ('S-nonself', 'ablation'), 'Cdon': ('Cdonor', 'L'),
         'prop': ('S-nonself', 'prop'), 'Cdense': ('Cdonor_dense', 'L')}
GEOMS = [(50, 64), (100, 64), (200, 64), (400, 64), (100, 32), (100, 128), (100, 256), (50, 32), (200, 128)]
PANEL_GEOMS = [(100, 64), (200, 64), (100, 128), (200, 128)]
PANEL_C = (0, 4, 8, 16)
MAIN_SNON = [(100, 64), (200, 64), (400, 64), (100, 128), (200, 128), (100, 256)]


def cell_name(rule, N, I, arm):
    return 'rs_%s_%d_%d_%s' % (rule, N, I, arm)


def register(rule, N, I, arm, prior=None):
    """arm: 'm1' (mN = 1), 'cal' (calibrated), 'm0' (no migration, the T_nuc calibration)."""
    spec, pr = RULES[rule] if prior is None else ('S-nonself', prior)
    name = cell_name(rule if prior is None else prior, N, I, arm)
    PR.CELLS[name] = (N, I, spec, pr, 'ext')
    CELL_MN[name] = {'m1': 1.0, 'cal': mN_cal(N), 'm0': 0.0}[arm]
    main = (arm == 'cal' and ((rule == 'Snon' and prior is None and (N, I) in MAIN_SNON) or
                              ((prior is not None and prior.startswith('cross')) or rule == 'prop') and (N, I) in PANEL_GEOMS))
    CELL_INFO[name] = dict(rule=rule if prior is None else prior, N=N, I=I, arm=arm, mN=CELL_MN[name], main=bool(main),
                           T_ext=t_ext(N, I) if main else 10000)
    return name


def all_cells():
    """Blocks A-D of notes §1.4 (duplicates at N = 100 registered once, as the 'cal' arm, mN = 1 there)."""
    out = {'A': [], 'B': [], 'C': [], 'D': []}
    for (N, I) in GEOMS:
        arms = ['cal'] if N == 100 else ['m1', 'cal']
        for arm in arms:
            for rule in ('Snon', 'abl', 'Cdon'):
                out['A'].append(register(rule, N, I, arm))
        out['B'].append(register('prop', N, I, 'cal'))
    for (N, I) in PANEL_GEOMS:
        for c in PANEL_C[1:]:
            out['C'].append(register(None, N, I, 'cal', prior='cross%d' % c))
    for (N, I) in [(200, 64), (400, 64)]:
        for arm in ('m1', 'cal'):
            out['D'].append(register('Cdense', N, I, arm))
    return out


ALL = all_cells()


def calib_cells():
    out = []
    for N in (50, 100, 200, 400):
        for rule in ('Snon', 'abl', 'Cdon'):
            out.append(register(rule, N, 64, 'm0'))
    return out


CALIB = calib_cells()


class RSRun(PR.Run):
    """Provenance's run object with the migration rate of the cell."""

    def __init__(self, cell, rep):
        super().__init__(cell, rep)
        self.mN = CELL_MN.get(cell, 1.0)

    def advance(self, gens):
        LS, st = self.LS, self.LS['st']
        self.g = PV.segment(self.g, gens, self.seed, self.N, W, self.mN / self.N, self.r, self.slots, self.counts,
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


# ------------------------------------------------------------------------------------------------ fixation (§1.6)
def rho_fix(N, a, b, c, d, w=W):
    """Exact fixation probability of one Z in N - 1 X under the kernel's step (birth proportional to count times
    exp(w f), f the mean payoff against the N - 1 others; death uniform).  a = pay(Z,Z), b = pay(Z,X), c = pay(X,Z),
    d = pay(X,X)."""
    j = np.arange(1, N, dtype=float)
    fz = ((j - 1) * a + (N - j) * b) / (N - 1)
    fx = (j * c + (N - j - 1) * d) / (N - 1)
    logs = np.cumsum(w * (fx - fz))
    m = max(0.0, float(logs.max()))
    s = math.exp(-m) + float(np.exp(logs - m).sum())
    return math.exp(-m) / s


# ------------------------------------------------------------------------------------------------ classifier (§1.6)
def classify(holders, held, mutual, openv, ident):
    """holders[i]: the island's holder index (into the type arrays); held[i] bool; mutual[k, j]: mutual cooperation
    of holder types k and j (k == j: self-play); openv[k], ident[k] bool.  Returns dict(universal_open, main (list of
    holder indices in the main network), fail (per island: '' | 'unheld' | 'identity' | 'rival'), cause)."""
    I = len(holders)
    held = np.asarray(held, bool)
    isl_open = np.array([bool(openv[holders[i]]) and held[i] for i in range(I)])
    if isl_open.any():
        cnt = {}
        for i in np.nonzero(isl_open)[0].tolist():
            cnt[holders[i]] = cnt.get(holders[i], 0) + 1
        hstar = sorted(cnt.items(), key=lambda z: (-z[1], z[0]))[0][0]
        main = sorted(k for k in cnt if mutual[k, hstar] and mutual[hstar, k])
    else:
        main = []
    mset = set(main)
    fail = []
    for i in range(I):
        if not held[i]: fail.append('unheld')
        elif holders[i] in mset: fail.append('')
        elif ident[holders[i]]: fail.append('identity')
        else: fail.append('rival')
    pairwise = all(mutual[k, j] for k in main for j in main)
    uo = all(f == '' for f in fail) and pairwise and len(main) > 0
    if uo: cause = None
    elif 'identity' in fail: cause = 'identity'
    elif 'rival' in fail: cause = 'rival'
    elif not pairwise: cause = 'rival'
    else: cause = 'inefficient'
    return dict(universal_open=bool(uo), main=main, fail=fail, cause=cause, pairwise=bool(pairwise))


def static_check(fail, holders, N, mN, Z_ok, Z_mutual_X, Z_rho, Z_share, reach_bridge, horizon_rule=1e6):
    """Notes §1.6.  For each failing island i: living bridges (target-compatible Z mutual with X_i), reachable-only
    bridges (reach_bridge[i]), the hazard h_i = mN sum_Z s_Z rho(Z -> X_i).  Z_ok[z]: target-compatible; Z_mutual_X[z][i]
    bool; Z_rho[z][i]; Z_share[z][i].  Returns (label, per-island list)."""
    per = []
    absorbing = False; only_reach = False; coord = False
    for i, f in enumerate(fail):
        if f == '': continue
        live = [z for z in range(len(Z_ok)) if Z_ok[z] and Z_mutual_X[z][i]]
        h = mN * sum(Z_share[z][i] * Z_rho[z][i] for z in range(len(Z_ok)) if Z_ok[z])
        t = (1.0 / h) if h > 0 else float('inf')
        rb = bool(reach_bridge[i])
        if live: kind = 'bridged'
        elif rb: kind = 'reachable-bridge'; only_reach = True
        elif t > horizon_rule: kind = 'absorbing'; absorbing = True
        else: kind = 'coordination'; coord = True
        per.append(dict(island=i, fail=f, kind=kind, n_living_bridges=len(live), hazard=h, t_res=t))
    if not per: return 'universal', per
    if absorbing: return 'absorbing', per
    if coord: return 'coordination', per
    if only_reach: return 'reachable-bridge', per
    return 'bridged', per
