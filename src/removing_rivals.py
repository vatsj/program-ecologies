"""Removing rival networks: a sponsored PrudentBot donor (prevention) and seed rain (cure)
(spec specs/2026-10-15-removing-rivals.md, notes notes/removing-rivals.md).

Imports the realizable-scaling machinery unchanged (which imports provenance's) and adds:
  - the target network (notes §1.1): the reference unit u_PB and the target units;
  - founders for the sponsored donor, the empty-list donor control and forced archipelagos;
  - a run object with seed rain and lineage tracking (src/removing_rivals_kern.py), checkpoint save / restore and
    injection;
  - the operational predator classifier (notes §1.2), the island status tracker and the path / loss / colonization
    bookkeeping (notes §1.6, §1.9).
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import provenance as PV
import provenance_run as PR
import realizable_scaling as RS            # patches PR.founders with the scaling founders
import removing_rivals_kern as KR

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'removing_rivals')
SALT = PR.SALT
PB_SP = 'if(CHK(them,me,C),if(CHK(them,^D,D),C,D),D)'     # provenance's named CBP4, run tree 123
FCAP = 2_000_000                                          # arrival records per run
_SC = {}


def static(LS=None):
    """Target units and helpers (cached)."""
    if 'T' in _SC: return _SC
    LS = LS or PR.lot_static()
    st = LS['st']
    A = np.asarray(st['A']); sa = np.asarray(st['selfa'])
    k = LS['names'].index(PB_SP)
    t = int(LS['tau'][k])
    uPB = int(LS['Hu'][t]); ePB = int(LS['Eu'][t])
    T = (sa == 1) & (A[:, uPB] == 1) & (A[uPB, :] == 1)
    cumL = np.cumsum(LS['mu']).astype(np.float64)
    spE = LS['Eu'][LS['tau']].astype(np.int64)
    _SC.update(LS=LS, A=A, sa=sa, T=T, uPB=uPB, ePB=ePB, kPB=k, tPB=t, cumL=cumL, spE=spE,
               openu=np.asarray(LS['openu']), ident=np.asarray(LS['ident']))
    return _SC


# ------------------------------------------------------------------------------------------------ founders
FORCED = {}                                               # cell -> (sp, rule, unit) arrays for forced archipelagos
_PREV_FOUNDERS = PR.founders                              # the scaling run's founders (already patched)


def donor_positions(N, I, rep):
    """C-donor's donor slot per island (provenance's stream [N, I, rep, SALT, 3], first draw integers(N))."""
    r_don = np.random.default_rng([N, I, rep, SALT, 3])
    pos = np.zeros(I, np.int64)
    nsp = len(PR.lot_static()['mu'])
    pd = PR.lot_static()['mu'] * PR.lot_static()['donor_ok']; pd = pd / pd.sum()
    for i in range(I):
        pos[i] = int(r_don.integers(N))
        r_don.choice(nsp, p=pd)                           # consume as C-donor does (keeps the stream aligned)
    return pos


def founders_rr(cell, rep, LS):
    if cell in FORCED:
        sp, rule, unit = FORCED[cell]
        return sp.copy(), rule.copy(), unit.copy()
    N, I, spec, prior, which = PR.CELLS[cell]
    if spec not in ('sponsored', 'pbempty'):
        return _PREV_FOUNDERS(cell, rep, LS)
    S = static(LS)
    sp, rule, unit = _base(N, I, rep, LS)
    pos = donor_positions(N, I, rep)
    for i in range(I):
        j = int(pos[i])
        sp[i, j] = S['kPB']
        if spec == 'sponsored':
            rule[i, j] = PV.R_H; unit[i, j] = S['uPB']
        else:
            rule[i, j] = PV.R_SNON; unit[i, j] = S['ePB']
    return sp, rule, unit


def _base(N, I, rep, LS):
    """S-nonself founders from L (provenance's stream [N, I, rep, SALT])."""
    nsp = len(LS['mu'])
    rng = np.random.default_rng([N, I, rep, SALT])
    sp = rng.choice(nsp, size=(I, N), p=LS['mu'])
    rule = np.full((I, N), PV.R_SNON, np.int64)
    unit = LS['Eu'][LS['tau'][sp]]
    return sp, rule, unit


PR.founders = founders_rr

# ------------------------------------------------------------------------------------------------ cells
CELL_EPSN = {}            # cell -> eps*N


def register(name, N, I, spec, epsN=0.0, arm='cal'):
    PR.CELLS[name] = (N, I, spec, 'L', 'ext')
    RS.CELL_MN[name] = {'m1': 1.0, 'cal': RS.mN_cal(N), 'm0': 0.0}[arm]
    RS.CELL_INFO[name] = dict(rule=spec, N=N, I=I, arm=arm, mN=RS.CELL_MN[name], main=False, T_ext=10000)
    CELL_EPSN[name] = epsN
    return name


def epsN_tag(e):
    return {0.0: '0', 0.01: '001', 0.1: '01', 1.0: '1'}[e]


A_GEOMS = [(200, 64), (400, 64), (200, 128), (100, 256)]
B_GEOMS = [(200, 64), (200, 128)]
RATES = (0.01, 0.1, 1.0)
CELLS_A, CELLS_B2, CELLS_B3 = [], [], []
for (N, I) in A_GEOMS:
    CELLS_A.append(register('rr_spon_%d_%d' % (N, I), N, I, 'sponsored'))
for (N, I) in B_GEOMS:
    CELLS_A.append(register('rr_pbe_%d_%d' % (N, I), N, I, 'pbempty'))
    for e in RATES:
        CELLS_B2.append(register('rr_rain%s_%d_%d' % (epsN_tag(e), N, I), N, I, 'S-nonself', e))
    CELLS_B3.append(register('rr_sponrain01_%d_%d' % (N, I), N, I, 'sponsored', 0.1))
# baselines (S-nonself calibrated at (100, 256) is a stored cell; registered by the scaling module)


# ------------------------------------------------------------------------------------------------ run object
class RRRun(RS.RSRun):
    """The scaling run object with seed rain (eps = epsN/N) and lineage tracking."""

    def __init__(self, cell, rep, epsN=None, track=None):
        super().__init__(cell, rep)
        S = static(self.LS)
        self.epsN = CELL_EPSN.get(cell, 0.0) if epsN is None else epsN
        self.track = (self.epsN > 0) if track is None else bool(track)
        self.cumL, self.spE = S['cumL'], S['spE']
        self.lin = np.zeros((self.I, self.N), np.int64)
        self.nlin = np.zeros(1, np.int64)
        self.fr = np.zeros((FCAP if self.track else 1, 5), np.int64)
        self.frf = np.zeros((FCAP if self.track else 1, 3))
        self.nfr = np.zeros(1, np.int64)
        self.rcount = np.zeros(self.I, np.int64)

    def set_rate(self, epsN, track=None):
        self.epsN = epsN
        self.track = (epsN > 0) if track is None else bool(track)
        if self.track and self.fr.shape[0] < FCAP:
            self.fr = np.zeros((FCAP, 5), np.int64); self.frf = np.zeros((FCAP, 3))

    def advance(self, gens):
        LS, st = self.LS, self.LS['st']
        eps = self.epsN / self.N
        self.g = KR.segment_rain(
            self.g, gens, self.seed, self.N, RS.W, self.mN / self.N, self.r, self.slots, self.counts, self.paysum,
            self.pres, self.npres, self.pos, self.spcount, self.d, self.tunit, self.trule, self.tsp, self.tanc,
            self.ntv, st['utau'], st['BLC'], st['BLD'], st['SINGLE'], st['APP'], LS['PRODC'], LS['PD'], st['KIND'],
            st['NAT'], st['CHC'], st['CHD'], st['UVt'], self.A, self.selfa, LS['OSV'], LS['SPO'], LS['capable'],
            LS['COSTS'], self.ctr, self.steps_rule, self.wn, self.wenc, self.wsp, self.wcode, self.wsid, self.ckey,
            self.cval, self.ncache, self.plog, self.hist_wait, self.hist_acq, self.hist_steps, self.hist_cens,
            self.nprod, LS['ident'], LS['spo_unit'], self.tset, self.uns, self.rulecount, self.enc_exp, self.skip,
            LS['FUT'], self.fcount, self.enc_futile, self.err,
            float(eps), self.cumL, self.spE, PV.R_SNON, bool(self.track), self.lin, self.nlin, self.fr, self.frf,
            self.nfr, self.rcount)
        if self.err[0] != 0:
            raise RuntimeError('kernel error %d in %s rep %d at generation %d (types %d)' % (
                self.err[0], self.cell, self.rep, self.g, self.ntv[0]))

    # -------------------------------------------------------------------------------- checkpoints
    def save_state(self):
        nt = int(self.ntv[0])
        I = self.I
        ps = np.zeros((I, self.N))
        for i in range(I):
            ks = self.pres[i, :self.npres[i]]
            ps[i, :len(ks)] = self.paysum[i, ks]
        return dict(g=self.g, seed=self.seed, nt=nt, slots=self.slots.copy(), pres=self.pres.copy(),
                    npres=self.npres.copy(), paysum_c=ps, tunit=self.tunit[:nt].copy(), trule=self.trule[:nt].copy(),
                    tsp=self.tsp[:nt].copy(), tanc=self.tanc[:nt].copy(), plog=self.plog.copy(), lin=self.lin.copy(),
                    nlin=self.nlin.copy())

    def load_state(self, s):
        nt = int(s['nt'])
        I, N = self.I, self.N
        self.g = int(s['g']); self.seed = int(s['seed'])
        self.tunit[:] = 0; self.trule[:] = 0; self.tsp[:] = 0; self.tanc[:] = 0
        self.tunit[:nt] = s['tunit']; self.trule[:nt] = s['trule']; self.tsp[:nt] = s['tsp']; self.tanc[:nt] = s['tanc']
        self.ntv[0] = nt
        self.d.clear()
        for k in range(nt):
            self.d[int(PV.type_code(int(self.tunit[k]), int(self.trule[k]), int(self.tsp[k]), int(self.tanc[k])))] = k
        self.slots[:] = s['slots']
        self.counts[:] = 0
        for i in range(I):
            np.add.at(self.counts[i], self.slots[i], 1)
        self.pres[:] = s['pres']; self.npres[:] = s['npres']
        self.pos[:] = -1
        self.paysum[:] = 0.0
        for i in range(I):
            ks = self.pres[i, :self.npres[i]]
            assert (self.counts[i, ks] > 0).all() and self.counts[i].sum() == N
            assert len(np.nonzero(self.counts[i])[0]) == self.npres[i]
            self.pos[i, ks] = np.arange(len(ks))
            self.paysum[i, ks] = s['paysum_c'][i, :len(ks)]
        self.spcount[:] = 0
        for i in range(I):
            np.add.at(self.spcount[i], self.tsp[self.slots[i]], 1)
        self.plog[:] = s['plog']
        self.lin[:] = s['lin']; self.nlin[:] = s['nlin']
        self.tset[:] = -1
        self.uns[:] = 0; self.rulecount[:] = 0; self.fcount[:] = 0
        st = self.LS['st']
        PV.init_uns(self.slots, self.tunit, self.trule, self.tset, st['BLC'], st['BLD'], self.LS['PD'], st['utau'],
                    self.LS['FUT'], self.uns, self.rulecount, self.fcount)

    def inject(self, i, j, sp, rule=PV.R_SNON, unit=None):
        """Replace the individual (i, j) by a fresh founder of spelling sp (empty lists unless a unit is given)."""
        st = self.LS['st']
        u = int(self.spE[sp]) if unit is None else int(unit)
        nt = int(self.ntv[0])
        k, nt2 = PV.make_type(self.d, self.tunit, self.trule, self.tsp, self.tanc, nt, u, rule, int(sp), 0)
        self.ntv[0] = nt2
        kv = int(self.slots[i, j])
        if kv == k: return k
        BLC, BLD, PD, utau, FUT = st['BLC'], st['BLD'], self.LS['PD'], st['utau'], self.LS['FUT']
        isS = lambda x: PV.is_settled(x, self.tunit, self.trule, self.tset, BLC, BLD, PD, utau, FUT)
        self.uns[i] += (0 if isS(k) else 1) - (0 if isS(kv) else 1)
        self.fcount[self.trule[k]] += 1 if self.tset[k] == 2 else 0
        self.fcount[self.trule[kv]] -= 1 if self.tset[kv] == 2 else 0
        self.rulecount[self.trule[kv]] -= 1; self.rulecount[self.trule[k]] += 1
        self.spcount[i, self.tsp[kv]] -= 1; self.spcount[i, self.tsp[k]] += 1
        PV.plog_close(i, j, kv, self.tunit, self.trule, utau, BLC, self.LS['capable'], self.plog, self.hist_wait,
                      self.hist_acq, self.hist_steps, self.hist_cens, self.nprod, 1)
        PV.plog_open(i, j, k, self.tunit, self.trule, BLC, self.plog)
        self.slots[i, j] = k
        PV._change(i, kv, k, self.counts, self.paysum, self.pres, self.npres, self.pos, self.tunit, self.tsp, self.A,
                   self.selfa)
        self.nlin[0] += 1
        self.lin[i, j] = self.nlin[0]
        return k


# ------------------------------------------------------------------------------------------------ predators (§1.2)
_DUM = {}


def _dummies():
    if not _DUM:
        _DUM.update(ctr=np.zeros(PV.NCTR, np.int64), steps=np.zeros(1), err=np.zeros(1, np.int64))
    return _DUM


def side_snon(u, sp, v, spv, LS):
    """The kernel's S-nonself side procedure for a unit u of spelling sp against a partner unit v of spelling spv
    (no copy step; production only against another spelling; then the D step).  Returns the new unit."""
    st = LS['st']; D = _dummies()
    BLC = st['BLC']
    if BLC[u, 0] < 0 and spv != sp:
        rel = 0 if u != v else (2 if sp == spv else 1)
        sid, code = PV.c_produce(u, v, rel, st['utau'], st['KIND'], st['NAT'], st['CHD'], st['UVt'], BLC, st['BLD'],
                                 LS['PRODC'], D['ctr'], D['steps'], LS['COSTS'], D['err'])
        if D['err'][0] != 0: raise RuntimeError('c_produce error %d' % D['err'][0])
        if sid >= 0:
            u, _ = PV.c_append(u, sid, 0, st['APP'], BLC, D['err'])
            if D['err'][0] != 0: raise RuntimeError('c_append error')
    u, _ = PV.d_step(u, 0, LS['PD'], st['BLD'], D['ctr'], D['steps'], LS['COSTS'], D['err'])
    if D['err'][0] != 0: raise RuntimeError('d_step error')
    return int(u)


def phenotype(u, sp, v, spv, LS, rule=PV.R_SNON):
    """Repeat the side procedure against the same partner until the unit stops changing."""
    if rule == PV.R_H: return int(u)
    for _ in range(8):
        u2 = side_snon(u, sp, v, spv, LS)
        if u2 == u: return int(u)
        u = u2
    return int(u)


_PH = {}


def phen_cached(s, x, sx, LS):
    """Fresh founder of spelling s against a resident (unit x, spelling sx)."""
    key = (s, x, sx) if s == sx else (int(LS['tau'][s]), x, -1)
    if key not in _PH:
        _PH[key] = phenotype(int(static(LS)['spE'][s]), s, x, sx, LS)
    return _PH[key]


def predator_table(x, sx, xrule, Tun, LS):
    """Accessible predators of a rival holder (unit x, spelling sx, rule xrule) given target units Tun.
    Returns dict(mass, n_sp, top (name, mass, unit) x3, constants among predators, certified counts, fragile mass,
    per-spelling boolean)."""
    S = static(LS)
    A, sa = S['A'], S['sa']
    mu, names, tau = LS['mu'], LS['names'], LS['tau']
    Tun = np.array(sorted(set(int(t) for t in Tun)), np.int64)
    nsp = len(mu)
    is_pred = np.zeros(nsp, bool)
    fragile = np.zeros(nsp, bool)
    phen = np.zeros(nsp, np.int64)
    # per tree (the spelling enters only through "s == sx")
    tree_ph = {}
    for s in range(nsp):
        t = int(tau[s])
        if s == sx:
            p = phenotype(int(S['spE'][s]), s, x, sx, LS)
        else:
            if t not in tree_ph:
                tree_ph[t] = phenotype(int(S['spE'][s]), s, x, sx, LS)
            p = tree_ph[t]
        phen[s] = p
    ok = (A[x, phen] == 1) & (A[phen, x] == 0) & (sa[phen] == 0)
    if len(Tun):
        ok &= (A[np.ix_(Tun, phen)] == 0).all(0)
    is_pred[:] = ok
    # reactions: X's unit after meeting p; p's unit after meeting each target holder (the reference spelling)
    for s in np.nonzero(is_pred)[0].tolist():
        p = int(phen[s])
        x2 = phenotype(x, sx, p, s, LS, xrule)
        bad = not (A[x2, p] == 1 and A[p, x2] == 0)
        for t in Tun.tolist():
            p2 = phenotype(p, s, t, S['kPB'], LS)
            if A[t, p2] != 0 or sa[p2] != 0:
                bad = True; break
        fragile[s] = bad
    m = mu[is_pred]
    order = np.argsort(-mu * is_pred)[:3]
    top = [(names[s], float(mu[s]), int(phen[s])) for s in order.tolist() if is_pred[s]]
    nU = A.shape[0]
    cert = (A[x, :] == 1) & (A[:, x] == 0)
    cert2 = cert & (sa == 0)
    if len(Tun): cert2 &= (A[Tun, :] == 0).all(0)
    consts = [names[s] for s in np.nonzero(is_pred)[0].tolist() if names[s] in ('C', 'D')]
    return dict(mass=float(m.sum()), n_sp=int(is_pred.sum()), top=top, constants=consts,
                cert_coop_defect=int(cert.sum()), cert_pred=int(cert2.sum()),
                fragile_mass=float(mu[is_pred & fragile].sum()), is_pred=is_pred, phen=phen)


def predflag_units(x, Tun, LS):
    """Units with the predator relations against x (unit level, for the predator-step share)."""
    S = static(LS)
    A, sa = S['A'], S['sa']
    f = (A[x, :] == 1) & (A[:, x] == 0) & (sa == 0)
    Tun = np.array(sorted(set(int(t) for t in Tun)), np.int64)
    if len(Tun): f &= (A[Tun, :] == 0).all(0)
    return f


# ------------------------------------------------------------------------------------------------ island status
def holders(R, cc):
    """Per island: majority type, held, on target, holder unit/spelling; run: universal-on-target, universal-open,
    split target, target holder units."""
    S = static(R.LS)
    T, A, sa = S['T'], S['A'], S['sa']
    maj = R.maj_k.copy()
    hu = R.tunit[maj]
    selfc = np.array([PV.cc_pair(int(k), int(k), R.tunit, R.tsp, R.A, R.selfa) > 0.5 for k in maj])
    held = selfc & (cc >= 0.5)
    ontgt = held & T[hu]
    H = sorted(set(int(k) for k in maj.tolist()))
    pair_ok = True
    for a in range(len(H)):
        for b in range(a + 1, len(H)):
            if PV.cc_pair(H[a], H[b], R.tunit, R.tsp, R.A, R.selfa) < 0.5:
                pair_ok = False; break
        if not pair_ok: break
    uot = bool(ontgt.all() and pair_ok)
    split = bool(ontgt.all() and not pair_ok)
    openv = S['openu'][hu]
    uo = bool(held.all() and pair_ok and openv.all())
    ident = S['ident'][hu] & held
    return dict(maj=maj, hu=hu, held=held, ontgt=ontgt, uot=uot, split=split, uo=uo, ident=ident, openv=openv,
                tgt_units=sorted(set(int(u) for u in hu[ontgt].tolist())))


def target_run_units(h, S):
    return sorted(set(h['tgt_units']) | {S['uPB']})


def classify_rivals(R, h, LS, cache=None):
    """Label every held non-target island: identity / exploitable / closed-open / closed-nonopen; unheld islands
    'unheld'; target islands ''."""
    S = static(LS)
    Tun = target_run_units(h, S)
    cache = {} if cache is None else cache
    lab, mass, info = [], [], {}
    for i in range(R.I):
        if not h['held'][i]:
            lab.append('unheld'); mass.append(0.0); continue
        if h['ontgt'][i]:
            lab.append(''); mass.append(0.0); continue
        k = int(h['maj'][i]); x = int(R.tunit[k]); sx = int(R.tsp[k]); xr = int(R.trule[k])
        key = (x, sx, xr, tuple(Tun))
        if key not in cache:
            pt = predator_table(x, sx, xr, Tun, LS)
            cache[key] = {kk: v for kk, v in pt.items() if kk not in ('is_pred', 'phen')}
        pt = cache[key]
        info[key] = pt
        if S['ident'][x]: lab.append('identity')
        elif pt['mass'] > 0: lab.append('exploitable')
        elif S['openu'][x]: lab.append('closed-open')
        else: lab.append('closed-nonopen')
        mass.append(pt['mass'])
    return lab, mass, cache


def island_shares(R, flags_by_island):
    """Share of each island's individuals whose unit has flags_by_island[i] (a bool array over units) set."""
    out = np.zeros(R.I)
    for i, f in flags_by_island.items():
        ks = R.pres[i, :R.npres[i]]
        out[i] = float((R.counts[i, ks] * f[R.tunit[ks]]).sum()) / R.N
    return out


def lineage_majorities(R):
    """Per island: the most common rain lineage id (> 0) and its count."""
    lid = np.zeros(R.I, np.int64); cnt = np.zeros(R.I, np.int64)
    for i in range(R.I):
        v = R.lin[i]
        v = v[v > 0]
        if len(v) == 0: continue
        u, c = np.unique(v, return_counts=True)
        j = int(np.argmax(c))
        lid[i] = u[j]; cnt[i] = c[j]
    return lid, cnt
