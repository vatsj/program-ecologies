"""Annealed mutation: a decaying re-injection schedule along the path N*Lambda_N = K/(rho mu_pred)
(spec specs/2026-10-16-annealed-mutation.md, notes notes/annealed.md).

Imports the removing-rivals machinery unchanged (target, founders, predator classifier, run object with lineages) and
adds:
  - the schedules (notes §1.3): annealed eps N(t) = a (1 + (t - 200)/t0)^-2 from generation 200, t0 = N/2, integrated
    exactly per generation, cut at the horizon 10,000; constant rain delivering the same total; eps = 0;
  - the run object with r = 100 production encounters per Moran event, the per-generation rate array and paired
    founder streams (src/annealed_kern.py);
  - the natural cells (arms i-iv, K = 3 and K = 1) and the Part F forced-rival archipelagos.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import provenance as PV
import provenance_run as PR
import realizable_scaling as RS
import removing_rivals as RR
import annealed_kern as AK

ROOT = RR.ROOT
OUT = os.path.join(ROOT, 'runs', 'annealed')
R_FIXED = 100                 # production encounters per Moran event (amendment 3)
ONSET = 200                   # no arrivals before this generation (amendment 2)
HORIZON = 10000               # arrivals stop here
CHASE = 2000                  # mutation-free chase
END = HORIZON + CHASE
RHO = 0.2592                  # exact constant-selection fixation of a predator (notes §1.1)
MU_AP = 0.0741                # anti-punisher class predator mass (notes §1.1)
MU_DET = 0.00568              # detector class
FCAP_ANN = 400000             # arrival records per run
FB_SP = 'if(CHK(them,me,C),C,D)'
FORCED_X = {'AP': (8077, 'if(CHK(them,them,C),D,if(CHK(them,^D,D),D,C))'),
            'DET': (12431, 'if(or(CHK(them,them,D),CHK(me,them,D)),D,C)')}


def arrivals_A(K):
    """Arrivals per island along the path, A = K/(rho mu_AP) (156.2 at K = 3)."""
    return K / (RHO * MU_AP)


def eps_n_annealed(N, A, onset=ONSET, horizon=HORIZON):
    """Per-generation expected arrivals per island (eps N)_g for g < horizon: the exact integral of
    a (1 + (t - onset)/t0)^-2 over [g, g + 1], t0 = N/2, a = A/t0; 0 before the onset."""
    t0 = N / 2.0
    g = np.arange(horizon, dtype=float)
    x = g - onset
    out = np.where(x >= 0, A * (t0 / (t0 + np.maximum(x, 0)) - t0 / (t0 + np.maximum(x, 0) + 1.0)), 0.0)
    return out


def delivered(N, A, onset=ONSET, horizon=HORIZON):
    T = horizon - onset; t0 = N / 2.0
    return A * T / (T + t0)


def eps_n_constant(N, A, onset=ONSET, horizon=HORIZON):
    """Constant rain from the onset to the horizon delivering the annealed schedule's total by the horizon."""
    out = np.zeros(horizon)
    out[onset:] = delivered(N, A, onset, horizon) / (horizon - onset)
    return out


def schedule(kind, N, K):
    """Per-Moran-event probabilities eps_g = (eps N)_g / N, length HORIZON (0 beyond)."""
    if kind == 'zero' or K == 0:
        return np.zeros(1)
    A = arrivals_A(K)
    en = eps_n_annealed(N, A) if kind == 'ann' else eps_n_constant(N, A)
    return (en / N).astype(np.float64)


# ------------------------------------------------------------------------------------------------ cells
CELL = {}                     # name -> dict(N, I, spec, sched, K, arm, cls)


def _reg(name, N, I, spec, sched, K, arm, cls=None):
    RR.register(name, N, I, spec, 0.0, 'cal')
    RS.CELL_INFO[name].update(T_ext=END)
    CELL[name] = dict(N=N, I=I, spec=spec, sched=sched, K=K, arm=arm, cls=cls)
    return name


NS = (200, 400, 800, 1600)
I8 = 8
CELLS_NAT, CELLS_K1, CELLS_F, CELLS_F_K1 = [], [], [], []
for N in NS:
    CELLS_NAT.append(_reg('an_i_%d' % N, N, I8, 'S-nonself', 'ann', 3, 'i'))
    CELLS_NAT.append(_reg('an_ii_%d' % N, N, I8, 'sponsored', 'ann', 3, 'ii'))
    CELLS_NAT.append(_reg('an_iiiS_%d' % N, N, I8, 'S-nonself', 'zero', 0, 'iiiS'))
    CELLS_NAT.append(_reg('an_iiiP_%d' % N, N, I8, 'sponsored', 'zero', 0, 'iiiP'))
    CELLS_NAT.append(_reg('an_iv_%d' % N, N, I8, 'S-nonself', 'const', 3, 'iv'))
for N in (200, 800):
    CELLS_K1.append(_reg('an_i_%d_K1' % N, N, I8, 'S-nonself', 'ann', 1, 'i'))
    CELLS_K1.append(_reg('an_ii_%d_K1' % N, N, I8, 'sponsored', 'ann', 1, 'ii'))


def forced_founders(N, I, cls, LS):
    """Island 0 all X (the class's holder unit and spelling, S-nonself), islands 1..I-1 all FairBot (unit 3)."""
    x, xs = FORCED_X[cls]
    sx = LS['names'].index(xs)
    sfb = LS['names'].index(FB_SP)
    ufb = int(LS['Hu'][LS['tau'][sfb]])
    sp = np.full((I, N), sfb, np.int64); unit = np.full((I, N), ufb, np.int64)
    rule = np.full((I, N), PV.R_SNON, np.int64)
    sp[0] = sx; unit[0] = x
    return sp, rule, unit


def reg_forced(cls, N, K=3, I=I8, sched='ann', tag=''):
    name = 'anF_%s_%d_K%d%s' % (cls, N, K, tag)
    if name in CELL: return name
    LS = PR.lot_static()
    RR.FORCED[name] = forced_founders(N, I, cls, LS)
    _reg(name, N, I, 'forced', sched, K, 'F', cls)
    return name


for N in NS:
    for cls in ('AP', 'DET'):
        CELLS_F.append(reg_forced(cls, N))
for N in (200, 800):
    for cls in ('AP', 'DET'):
        CELLS_F_K1.append(reg_forced(cls, N, K=1))


def reg_native_r(N=400):
    """The native-r control (r = N/2) at (N, 8), eps = 0, S-nonself."""
    return _reg('an_iiiSnat_%d' % N, N, I8, 'S-nonself', 'zero', 0, 'iiiSnat')


CELL_NAT_R = reg_native_r()


# ------------------------------------------------------------------------------------------------ run object
class AnnRun(RR.RRRun):
    """Removing-rivals' run object with r = 100, a per-generation rate array and paired founder streams."""

    def __init__(self, cell, rep, sched=None, pairmode=1, r=None, track=None, fcap=FCAP_ANN):
        super().__init__(cell, rep, epsN=0.0, track=False)
        info = CELL.get(cell)
        if r is not None: self.r = int(r)
        elif info is not None and info['arm'] == 'iiiSnat': self.r = self.N // 2
        else: self.r = R_FIXED
        if sched is None:
            sched = schedule(info['sched'], self.N, info['K']) if info is not None else np.zeros(1)
        self.epsg = np.ascontiguousarray(sched, dtype=np.float64)
        self.pairmode = int(pairmode)
        self.fseed = int((self.seed * 6364136223846793005 + 1442695040888963407) % (2 ** 62))
        self.track = bool(self.epsg.max() > 0) if track is None else bool(track)
        n = fcap if self.track else 1
        self.fr = np.zeros((n, 5), np.int64); self.frf = np.zeros((n, 3)); self.nfr[0] = 0
        self.epsN = float(self.epsg.max() * self.N)

    def set_rate(self, epsN, track=None):
        raise NotImplementedError('AnnRun uses a schedule array')

    def advance(self, gens):
        LS, st = self.LS, self.LS['st']
        self.g = AK.segment_ann(
            self.g, gens, self.seed, self.N, RS.W, self.mN / self.N, self.r, self.slots, self.counts, self.paysum,
            self.pres, self.npres, self.pos, self.spcount, self.d, self.tunit, self.trule, self.tsp, self.tanc,
            self.ntv, st['utau'], st['BLC'], st['BLD'], st['SINGLE'], st['APP'], LS['PRODC'], LS['PD'], st['KIND'],
            st['NAT'], st['CHC'], st['CHD'], st['UVt'], self.A, self.selfa, LS['OSV'], LS['SPO'], LS['capable'],
            LS['COSTS'], self.ctr, self.steps_rule, self.wn, self.wenc, self.wsp, self.wcode, self.wsid, self.ckey,
            self.cval, self.ncache, self.plog, self.hist_wait, self.hist_acq, self.hist_steps, self.hist_cens,
            self.nprod, LS['ident'], LS['spo_unit'], self.tset, self.uns, self.rulecount, self.enc_exp, self.skip,
            LS['FUT'], self.fcount, self.enc_futile, self.err,
            self.epsg, self.pairmode, self.fseed, self.cumL, self.spE, PV.R_SNON, bool(self.track), self.lin,
            self.nlin, self.fr, self.frf, self.nfr, self.rcount)
        if self.err[0] != 0:
            raise RuntimeError('kernel error %d in %s rep %d at generation %d (types %d)' % (
                self.err[0], self.cell, self.rep, self.g, self.ntv[0]))
        if self.track and self.nfr[0] >= self.fr.shape[0]:
            raise RuntimeError('arrival records overflow in %s rep %d' % (self.cell, self.rep))


def top_predator(cls, LS=None):
    """The top accessible predator spelling of the class's holder against target units {FairBot, u_PB}."""
    LS = LS or PR.lot_static()
    S = RR.static(LS)
    x, xs = FORCED_X[cls]
    sx = LS['names'].index(xs)
    pt = RR.predator_table(x, sx, PV.R_SNON, [3, S['uPB']], LS)
    s = int(np.argmax(LS['mu'] * pt['is_pred']))
    return s, pt
