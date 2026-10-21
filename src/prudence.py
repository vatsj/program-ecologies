"""Rewarding prudence: fission-fusion with a light post-merge arrival tail under world K
(spec specs/2026-10-21-prudence-world-k.md, notes notes/prudence.md, predictions predictions/2026-10-21-prudence-world-k.md).

Imports provenance, the Pangaea fission-fusion run (`pg_L_100_128_r100_ff200`), the removing-rivals target and
`src/world_k.py`'s world switch unchanged and adds:
  - the delivered-exposure schedule (notes §1.1): a per-generation arrival probability, t0 = 1,000, normalized on the
    discrete tail generations so that the expected delivered total is exactly 128 A (A per 100 programs, N = 12,800);
  - the arrival prior: the full prior L, or the sucker-depleted prior (spellings whose E-state unit cooperates against
    all five probe units, Q kept; the same syntactic set in both worlds, notes §1.4);
  - the frozen sets (notes §1.2): target T, prudent (guarded) target, PrudentBot's own tree, off-target FairBot variants
    (class CBo at unit level), suckers (certified / uncertified);
  - a run object that is the Pangaea run before the merge and, after it, the arrival kernel with lineage tracking
    (src/prudence_kern.py);
  - the per-checkpoint statistics, the arrival summary, the fixed-list payoff edge (the premium's primary measure).
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import provenance as PV
import provenance_run as PR
import realizable_scaling as RS
import pangaea as PG
import pangaea_kern as PK
import removing_rivals as RR
import world_k as WK
import prudence_kern as PRK

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'prudence')
FF_CELL = 'pg_L_100_128_r100_ff200'
MERGE = 200
TAIL = 10000                       # post-merge generations with arrivals
CHASE = 2000                       # post-tail generations without arrivals
NTOT = 12800
T0 = 1000.0
SALT = 20261021
FCAP = 60000                       # arrival records per run (A = 156 delivers 19,968 in expectation)
G_TAILEND = MERGE + TAIL           # 10,200
G_END = MERGE + TAIL + CHASE       # 12,200
SNAP_T = (0, 50, 100, 500, 1000, 2000, 5000, 10000, 12000)   # heavy snapshots at t = g - MERGE

# arms: name -> (A per 100 programs, sucker-depleted arrival prior)
ARMS = {'A0': (0, False), 'A52': (52, False), 'A156': (156, False), 'SD52': (52, True)}
WORLDS = ('L', 'K')


# ------------------------------------------------------------------------------------------------ schedule (§1.1)
def arrival_weights(tail=TAIL, t0=T0):
    t = np.arange(tail, dtype=float)
    return (1.0 + t / t0) ** -2


def lam(A, tail=TAIL, t0=T0, ntot=NTOT):
    """Expected arrivals in each of the `tail` post-merge generations: normalized so that the sum is exactly A * ntot / 100
    (the delivered total, notes §1.1)."""
    w = arrival_weights(tail, t0)
    return (A * ntot / 100.0) * w / w.sum()


def schedule(A, merge=MERGE, tail=TAIL, t0=T0, ntot=NTOT):
    """Per-Moran-event arrival probability for absolute generation g: zero before the merge and after the tail; the
    array has length merge + tail (the kernel treats g beyond it as 0)."""
    out = np.zeros(merge + tail)
    if A > 0:
        out[merge:] = lam(A, tail, t0, ntot) / ntot
    return out


# ------------------------------------------------------------------------------------------------ world sets (§1.2)
_SETS = {}


def sets(LS):
    """Frozen unit- and spelling-level sets for the world whose static tables are LS (cached per world)."""
    w = LS.get('world', 'L')
    if w in _SETS: return _SETS[w]
    S = RR.static(LS)
    X = PG.statics(LS)
    st = LS['st']
    A = np.asarray(st['A']); sa = np.asarray(st['selfa'])
    BLC = np.asarray(st['BLC'])
    nU = A.shape[0]
    tau, Hu, Eu, mu, names = LS['tau'], LS['Hu'], LS['Eu'], LS['mu'], LS['names']
    cH, dH, cbH, apH, pbH = X['cH'], X['dH'], X['cbH'], X['apH'], X['pbH']
    T = S['T']
    mutFB = (A[:, cbH] == 1) & (A[cbH, :] == 1)
    mutAP = (A[:, apH] == 1) & (A[apH, :] == 1)
    d = dict(
        T=T, uPB=S['uPB'], tPB=S['tPB'], cH=cH, dH=dH, cbH=cbH, apH=apH,
        guard=(A[:, cH] == 0),                      # unit defects against certified CooperateBot
        mutFB=mutFB, mutAP=mutAP,
        sucker=(A[:, dH] == 1), cert=(BLC[:, 0] >= 0),
        ident=np.asarray(LS['ident']), openu=np.asarray(LS['openu']),
        Qsp=np.zeros(len(mu), bool),
    )
    d['Qsp'][LS['Q']] = True
    # the sucker-depleted set (notes §1.4): E-state unit cooperates against all five probe units, Q kept
    uE = Eu[tau]
    allE = np.ones(len(mu), bool)
    for p in (cH, dH, cbH, apH, pbH):
        allE &= (A[uE, p] == 1)
    d['SD'] = allE & ~d['Qsp']
    # spelling-level sets for arrivals (E-state unit = what a fresh founder is; H-state = saturated certificates)
    uH = Hu[tau]
    d['arr_suckerE'] = (A[uE, dH] == 1)
    d['arr_T_H'] = T[uH] & (sa[uH] == 1)
    d['arr_prud_H'] = d['arr_T_H'] & d['guard'][uH]
    d['arr_pbtree'] = (tau == S['tPB'])
    d['arr_CBo'] = (X['cls'] == PG.CLASSES.index('CBo'))
    d['uE'] = uE; d['uH'] = uH
    d['mu'] = mu
    _SETS[w] = d
    return d


def pay_u(A, a, b):
    """Payoff of unit a against unit b (D vs C 2, C vs C 1, D vs D 0, C vs D -1): -A[a, b] + 2 A[b, a]."""
    return -A[a, b].astype(np.int64) + 2 * A[b, a].astype(np.int64)


def depleted_cumL(LS):
    """Cumulative prior with the SD spellings' increments zeroed (arrival draws never select them)."""
    s = sets(LS)
    mu = LS['mu'] * (~s['SD'])
    return np.cumsum(mu).astype(np.float64)


# ------------------------------------------------------------------------------------------------ the run object
class PruRun(PG.PGRun):
    """The Pangaea fission-fusion run before the merge; after it, the arrival kernel with lineage tracking."""

    def __init__(self, rep, arm, fcap=FCAP):
        super().__init__(FF_CELL, rep)
        self.arm = arm
        A, depleted = ARMS[arm]
        self.A_exp = A
        self.depleted = depleted
        self.merged = False
        S = RR.static(self.LS)
        self.cumL = depleted_cumL(self.LS) if depleted else S['cumL']
        self.spE = S['spE']
        self.epsg = np.ascontiguousarray(schedule(A), dtype=np.float64)
        self.fseed = int((rep * 1000003 + 7919 + SALT) % (2 ** 62))
        self.lseed = int((rep * 998244353 + 104729 + SALT) % (2 ** 62))
        self.track = A > 0
        self.fcap = fcap
        self.lin = np.zeros((1, 1), np.int64)
        self.nlin = np.zeros(1, np.int64)
        self.fr = np.zeros((1, 6), np.int64); self.frf = np.zeros((1, 3)); self.nfr = np.zeros(1, np.int64)
        self.rcount = np.zeros(1, np.int64)

    def do_merge(self):
        self.merge(PG.kernel_seed_pg(self.N * self.I, 1, self.rep) ^ 0x5DEECE66D)
        self.merged = True
        T = self.N
        self.lin = np.zeros((1, T), np.int64)
        self.nlin = np.zeros(1, np.int64)
        n = self.fcap if self.track else 1
        self.fr = np.zeros((n, 6), np.int64); self.frf = np.zeros((n, 3)); self.nfr = np.zeros(1, np.int64)
        self.rcount = np.zeros(1, np.int64)

    def advance(self, gens):
        if not self.merged:
            return super().advance(gens)
        LS, st = self.LS, self.LS['st']
        self.g = PRK.segment_pru(
            self.g, gens, self.seed, self.N, RS.W, self.mN / self.N, self.r, self.slots, self.counts, self.paysum,
            self.pres, self.npres, self.pos, self.spcount, self.d, self.tunit, self.trule, self.tsp, self.tanc,
            self.ntv, st['utau'], st['BLC'], st['BLD'], st['SINGLE'], st['APP'], LS['PRODC'], LS['PD'], st['KIND'],
            st['NAT'], st['CHC'], st['CHD'], st['UVt'], self.A, self.selfa, LS['OSV'], LS['SPO'], LS['capable'],
            LS['COSTS'], self.ctr, self.steps_rule, self.wn, self.wenc, self.wsp, self.wcode, self.wsid, self.ckey,
            self.cval, self.ncache, self.plog, self.hist_wait, self.hist_acq, self.hist_steps, self.hist_cens,
            self.nprod, LS['ident'], LS['spo_unit'], self.tset, self.uns, self.rulecount, self.enc_exp, self.skip,
            LS['FUT'], self.fcount, self.enc_futile, self.err,
            self.epsg, self.fseed, self.lseed, self.cumL, self.spE, PV.R_SNON, bool(self.track), self.lin,
            self.nlin, self.fr, self.frf, self.nfr, self.rcount)
        if self.err[0] != 0:
            raise RuntimeError('kernel error %d in %s rep %d at generation %d (types %d)' % (
                self.err[0], self.cell, self.rep, self.g, self.ntv[0]))
        if self.track and self.nfr[0] >= self.fr.shape[0]:
            raise RuntimeError('arrival records overflow in %s rep %d' % (self.cell, self.rep))


# ------------------------------------------------------------------------------------------------ statistics (§1.6)
GROUPS = ('T', 'prud', 'ung', 'pb', 'off', 'suck_c', 'suck_u', 'ident', 'AP', 'Q')


def living(R):
    nt = int(R.ntv[0])
    c = R.counts[0, :nt]
    K = np.nonzero(c)[0]
    return K, c[K]


def type_flags(R, S, LS, K):
    """Per living type (indexed like K): self-cooperating, and the group flags of GROUPS (bool arrays)."""
    U = R.tunit[K]; sp = R.tsp[K]
    selfc = np.array([PV.cc_pair(int(k), int(k), R.tunit, R.tsp, R.A, R.selfa) > 0.5 for k in K])
    inT = selfc & S['T'][U]
    f = dict(
        T=inT,
        prud=inT & S['guard'][U],
        ung=inT & ~S['guard'][U],
        pb=(LS['tau'][sp] == S['tPB']),
        off=selfc & ~S['sucker'][U] & S['mutFB'][U] & ~S['T'][U],
        suck_c=S['sucker'][U] & S['cert'][U],
        suck_u=S['sucker'][U] & ~S['cert'][U],
        ident=S['ident'][U],
        AP=selfc & S['mutAP'][U] & ~S['openu'][U],
        Q=S['Qsp'][sp],
    )
    return selfc, f


def light_stats(R, S, LS):
    """One checkpoint: P(C,C), living types, the shares of GROUPS (population fractions), the arrival-descended share
    of each (lineage > 0), the encounter-weighted edge over living suckers, the realized selection advantage of prudent
    over unguarded target members, and the dominant arrival lineage.  Returns a dict of plain numbers."""
    N = R.N
    K, c = living(R)
    selfc, f = type_flags(R, S, LS, K)
    nt = int(R.ntv[0])
    idx = -np.ones(nt, np.int64); idx[K] = np.arange(len(K))
    ind = idx[R.slots[0]]                           # per-individual index into K
    lin = R.lin[0]
    imm = lin > 0
    out = dict(g=int(R.g), nt=int(len(K)), pcc=float(R.island_stats()[0]), coopsh=float(c[selfc].sum() / N),
               imm=float(imm.mean()))
    for name in GROUPS:
        v = f[name]
        out[name] = float(c[v].sum() / N)
        out['i_' + name] = float(((v[ind]) & imm).sum() / N)
    A = np.asarray(R.A)
    U = R.tunit[K]
    e = pay_u(A, S['uPB'], U) - pay_u(A, S['cbH'], U)
    sk = S['sucker'][U]
    out['edge_enc'] = float((c * e * sk).sum() / N)               # edge summed over the sucker mass (population fraction)
    skc = sk & S['cert'][U]
    out['edge_enc_c'] = float((c * e * skc).sum() / N)
    # realized selection advantage of prudent over unguarded target members (payoff in the realized population)
    fk = np.array([(R.paysum[0, k] - PV.pay(int(k), int(k), R.tunit, R.tsp, R.A, R.selfa)) / (N - 1) for k in K])
    def mean_f(mask):
        w = c * mask
        return float((w * fk).sum() / w.sum()) if w.sum() > 0 else None
    fp, fu = mean_f(f['prud']), mean_f(f['ung'])
    out['f_prud'] = fp; out['f_ung'] = fu
    out['sel_adv'] = (fp - fu) if (fp is not None and fu is not None) else None
    # dominant arrival lineage
    if imm.any():
        bc = np.bincount(lin[imm])
        lid = int(np.argmax(bc))
        out['top_lin'] = lid; out['top_lin_sh'] = float(bc[lid] / N)
    else:
        out['top_lin'] = 0; out['top_lin_sh'] = 0.0
    # the plurality type
    kmax = int(K[int(np.argmax(c))])
    ci = int(np.argmax(c))
    out['plur_s'] = int(R.tsp[kmax]); out['plur_sh'] = float(c[ci] / N)
    out['plur'] = dict(sp=LS['names'][int(R.tsp[kmax])], sh=float(c[ci] / N), T=bool(f['T'][ci]), prud=bool(f['prud'][ci]),
                       pb=bool(f['pb'][ci]), rule=int(R.trule[kmax]))
    return out


def heavy_stats(R, S, LS, g):
    cc = R.island_stats()
    dec = PG.decompose(R, cc, closure=True)
    out = {k: (round(v, 6) if isinstance(v, float) else v) for k, v in dec.items()}
    out['g'] = int(g)
    return out


# ------------------------------------------------------------------------------------------------ arrivals (§1.5)
def arrival_summary(R, S, LS, fr=None, frf=None):
    """Aggregates of the realized arrival log: counts by class (static classes of the arriving spelling), the fixed-list
    edge summed over realized arrivals (H-state and E-state units of the arriving spelling), the arrivals' initial
    payoff relative to the population mean, and victims' classes."""
    n = int(R.nfr[0])
    A = np.asarray(R.A)
    out = dict(n=n, rcount=int(R.rcount[0]))
    if n == 0 or not R.track:
        return out
    fr = R.fr[:n]; frf = R.frf[:n]
    s = fr[:, 2]
    uH = S['uH'][s]; uE = S['uE'][s]
    eH = pay_u(A, S['uPB'], uH) - pay_u(A, S['cbH'], uH)
    eE = pay_u(A, S['uPB'], uE) - pay_u(A, S['cbH'], uE)
    cls = dict(suckerE=S['arr_suckerE'][s], SD=S['SD'][s], Q=S['Qsp'][s], T_H=S['arr_T_H'][s],
               prud_H=S['arr_prud_H'][s], pbtree=S['arr_pbtree'][s], CBo=S['arr_CBo'][s])
    out['by_class'] = {k: int(v.sum()) for k, v in cls.items()}
    out['edgeH_sum'] = {k: float(eH[v].sum()) for k, v in cls.items()}
    out['edgeE_sum'] = {k: float(eE[v].sum()) for k, v in cls.items()}
    out['edgeH_all'] = float(eH.sum()); out['edgeE_all'] = float(eE.sum())
    rel = frf[:, 1] - frf[:, 2]
    out['rel_pay_mean'] = float(rel.mean())
    out['n_adv'] = int((rel > 1e-12).sum()); out['n_dis'] = int((rel < -1e-12).sum())
    # victims (type classes at the end: unit and spelling are fixed per type)
    kv = fr[:, 3]
    Uv = R.tunit[kv]; spv = R.tsp[kv]
    out['victims'] = dict(sucker=int(S['sucker'][Uv].sum()), T=int(S['T'][Uv].sum()),
                          prud=int((S['T'][Uv] & S['guard'][Uv]).sum()), Q=int(S['Qsp'][spv].sum()))
    # arrivals by time (cumulative delivered at t = 1000, 5000, 10000)
    t = fr[:, 0] - MERGE
    out['delivered_by'] = {str(x): int((t < x).sum()) for x in (100, 500, 1000, 2000, 5000, 10000)}
    return out


# ------------------------------------------------------------------------------------------------ the fixed-list premium (static)
FIXED_NAMES = ['C', 'if(CHK(me,them,D),D,C)', 'if(CHK(them,me,C),C,D)', 'D']


def static_premium(LS):
    """The premium's primary measure (notes §1.5): edge(x) = payoff(PrudentBot-H vs x) - payoff(FairBot-H vs x) for the
    fixed list of spellings and the prior-weighted sets, on H-state and E-state units of x."""
    S = sets(LS)
    A = np.asarray(LS['st']['A'])
    mu = LS['mu']; names = LS['names']
    uPB, uFB = S['uPB'], S['cbH']
    eH = pay_u(A, uPB, S['uH']) - pay_u(A, uFB, S['uH'])
    eE = pay_u(A, uPB, S['uE']) - pay_u(A, uFB, S['uE'])

    def wmean(e, mask):
        m = mu * mask
        return (float((m * e).sum() / m.sum()) if m.sum() > 0 else None, float(m.sum()))
    out = {}
    for nm in FIXED_NAMES:
        if nm in names:
            k = names.index(nm)
            out['name:' + nm] = dict(H=int(eH[k]), E=int(eE[k]))
    qk = [int(k) for k in LS['Q'].tolist()]
    out['Q'] = dict(H_mean=float(np.mean([eH[k] for k in qk])), E_mean=float(np.mean([eE[k] for k in qk])), n=len(qk))
    for key, mask in (('suckerE', S['arr_suckerE']), ('SD', S['SD']),
                      ('suckerH_cert', (A[S['uH'], S['dH']] == 1) & S['cert'][S['uH']]),
                      ('T_H', S['arr_T_H']), ('prud_H', S['arr_prud_H'])):
        out[key] = dict(H=wmean(eH, mask)[0], E=wmean(eE, mask)[0], mass=wmean(eH, mask)[1])
    return out
