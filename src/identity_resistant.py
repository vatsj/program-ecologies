"""An identity-resistant target (spec specs/2026-10-17-identity-resistant-target.md, notes notes/identity-resistant.md).

Imports the removing-rivals, annealed and Pangaea machinery unchanged and adds:
  - the semantic partition of the frozen target 𝒯 (235 units) into members identity can exploit and resistant ones
    (notes §1.2), the challenge set 𝒬 and the syntactic guard test (§1.3);
  - the priors L, R-move (Rm) and R-proportional (Rp) and their maximal coupling as piecewise quantile tables (§1.5);
  - founders for islands, fission-fusion and rain cells under each prior, with or without the sponsored PrudentBot;
  - run objects: Part I (Pangaea's PGRun with the merge), Part II (removing-rivals' RRRun at eps = 0), Part III
    (annealed's AnnRun with the piece-table kernel, src/identity_resistant_kern.py).
"""
import itertools
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import provenance as PV
import provenance_run as PR
import realizable_scaling as RS
import removing_rivals as RR
import annealed as AN
import pangaea as PG                         # patches PR.founders (falls back to removing-rivals' dispatcher)
import identity_resistant_kern as IK

ROOT = RR.ROOT
OUT = os.path.join(ROOT, 'runs', 'identity_resistant')
EXEC_PATH = os.path.join(ROOT, 'runs', 'identity-resistant-exec.json')
PRIORS = ('L', 'Rm', 'Rp')
GUARD = 'them,me,C'
Q_TOP = 'if(or(CHK(me,me,D),CHK(me,them,D)),D,C)'       # the heaviest TwinD spelling (M1 assays)


def q_reps(LS):
    """The heaviest spelling of each TwinD (Q) run tree, in tree order (M1's injected founders)."""
    Q = LS['Q']; tau = LS['tau']; mu = LS['mu']
    out = []
    for t in sorted(set(tau[Q].tolist())):
        m = [q for q in Q.tolist() if tau[q] == t]
        out.append(LS['names'][max(m, key=lambda q: (mu[q], -q))])
    return out


def q_tree_weights(LS):
    """mu(tree) / mu(Q) for each Q tree, aligned with q_reps."""
    Q = LS['Q']; tau = LS['tau']; mu = LS['mu']
    ts = sorted(set(tau[Q].tolist()))
    w = np.array([mu[[q for q in Q.tolist() if tau[q] == t]].sum() for t in ts])
    return w / w.sum()


# ------------------------------------------------------------------------------------------------ the guard (§1.3)
def parse(s):
    """Spelling -> tree: 'C' | 'D' | ('if', cond, e1, e2); cond: ('chk', 'x,y,a') | ('not', c) | ('and'|'or', c1, c2)."""
    pos = [0]

    def tok(t):
        if not s.startswith(t, pos[0]): raise ValueError('parse %s at %d' % (s, pos[0]))
        pos[0] += len(t)

    def expr():
        if s.startswith('if(', pos[0]):
            tok('if('); c = cond(); tok(','); a = expr(); tok(','); b = expr(); tok(')')
            return ('if', c, a, b)
        ch = s[pos[0]]; pos[0] += 1
        if ch not in 'CD': raise ValueError(s)
        return ch

    def cond():
        for op in ('and(', 'or('):
            if s.startswith(op, pos[0]):
                tok(op); x = cond(); tok(','); y = cond(); tok(')')
                return (op[:-1], x, y)
        if s.startswith('not(', pos[0]):
            tok('not('); x = cond(); tok(')')
            return ('not', x)
        tok('CHK('); j = s.index(')', pos[0]); a = s[pos[0]:j]; pos[0] = j + 1
        return ('chk', a)

    e = expr()
    if pos[0] != len(s): raise ValueError(s)
    return e


def _atoms(e, out):
    if isinstance(e, str): return
    if e[0] == 'if':
        _catoms(e[1], out); _atoms(e[2], out); _atoms(e[3], out)


def _catoms(c, out):
    if c[0] == 'chk': out.add(c[1]); return
    for x in c[1:]: _catoms(x, out)


def _evc(c, v):
    if c[0] == 'chk': return v[c[1]]
    if c[0] == 'not': return not _evc(c[1], v)
    if c[0] == 'and': return _evc(c[1], v) and _evc(c[2], v)
    return _evc(c[1], v) or _evc(c[2], v)


def _eve(e, v):
    if isinstance(e, str): return e
    return _eve(e[2], v) if _evc(e[1], v) else _eve(e[3], v)


def guarded(name, exclusive=False):
    """True iff the program outputs D whenever CHK(them,me,C) is false, for every assignment of the other atoms
    (independent; exclusive=True skips assignments with CHK(x,y,C) and CHK(x,y,D) both true)."""
    e = parse(name)
    at = set(); _atoms(e, at)
    others = sorted(at - {GUARD})
    for vals in itertools.product([False, True], repeat=len(others)):
        v = dict(zip(others, vals)); v[GUARD] = False
        if exclusive and any(v[a] and v.get(a[:-1] + ('D' if a[-1] == 'C' else 'C'), False) for a in others):
            continue
        if _eve(e, v) == 'C': return False
    return True


# ------------------------------------------------------------------------------------------------ partition (§1.2)
_P = {}


def partition(LS=None, use_exec=True):
    """Target units, challenge set, exploitable flags (ideal table, union with executed plays when the executed check
    has been written), spelling classes and their masses."""
    key = 'P%d' % int(use_exec)
    if key in _P: return _P[key]
    LS = LS or PR.lot_static()
    S = RR.static(LS)
    A, sa, T = S['A'], S['sa'], S['T']
    utau = np.asarray(LS['st']['utau'])
    tau, mu, names = LS['tau'], LS['mu'], LS['names']
    Tu = np.nonzero(T)[0]
    chal = np.nonzero(np.asarray(LS['ident']))[0]
    ex_ideal = ((A[np.ix_(Tu, chal)] == 1) & (A[np.ix_(chal, Tu)].T == 0)).any(1)
    ex = ex_ideal.copy()
    exec_info = None
    if use_exec and os.path.exists(EXEC_PATH):
        exec_info = json.load(open(EXEC_PATH))
        exe = np.array([bool(exec_info['exploitable_exec'][str(int(u))]) for u in Tu])
        ex = ex_ideal | exe
    exu = np.zeros(A.shape[0], bool); exu[Tu[ex]] = True
    resu = np.zeros(A.shape[0], bool); resu[Tu[~ex]] = True
    ext = set(utau[Tu[ex]].tolist()); rest = set(utau[Tu[~ex]].tolist())
    assert not (ext & rest), 'a run tree with units in both classes'
    sp_E = np.isin(tau, sorted(ext)); sp_Res = np.isin(tau, sorted(rest))
    sp_Q = np.zeros(len(mu), bool); sp_Q[LS['Q']] = True
    Hs = LS['Hu'][tau]
    dH = int(LS['u_d'])
    sp_UC = (A[Hs, dH] == 1) & (sa[Hs] == 1)            # unconditional cooperators (self-coop, cooperate with D-H)
    out = dict(Tu=Tu, chal=chal, ex_ideal=ex_ideal, ex=ex, exu=exu, resu=resu, ext=sorted(ext), rest=sorted(rest),
               sp_E=sp_E, sp_Res=sp_Res, sp_Q=sp_Q, sp_UC=sp_UC, dH=dH, exec_info=exec_info,
               mass=dict(E=float(mu[sp_E].sum()), Res=float(mu[sp_Res].sum()), Q=float(mu[sp_Q].sum())))
    _P[key] = out
    return out


def sp_class(s, P):
    """Rain / founder class of a spelling: Q, E, Res, UC (unconditional cooperator, not in a target tree) or other."""
    if P['sp_Q'][s]: return 'Q'
    if P['sp_E'][s]: return 'E'
    if P['sp_Res'][s]: return 'Res'
    if P['sp_UC'][s]: return 'UC'
    return 'other'


SP_CLASSES = ('Q', 'E', 'Res', 'UC', 'other')


# ------------------------------------------------------------------------------------------------ priors (§1.5)
def prior_mass(prior, LS=None):
    LS = LS or PR.lot_static()
    P = partition(LS)
    mu = LS['mu'].astype(np.float64)
    if prior == 'L': return mu.copy()
    E = P['sp_E']
    W = P['sp_Res'] if prior == 'Rm' else (~E & ~P['sp_Q'])
    out = mu.copy()
    out[E] = 0.0
    out[W] = mu[W] * (1.0 + mu[E].sum() / mu[W].sum())
    return out


_PT = {}


def piece_table(prior, base='np', LS=None):
    """(boundaries, pmap): u (uniform on [0, total)) -> pmap[searchsorted(boundaries, u, 'right')].
    base 'np': numpy's normalized cumulative sum (founders, = Generator.choice); 'kern': the kernel's cumL
    (removing-rivals' static cumL, rain).  Under L: (base, identity).  Under Rm / Rp: every unchanged interval
    coincides with L's; the union of the exploitable-target intervals is mapped by the recipients' quantile."""
    key = (prior, base)
    if key in _PT: return _PT[key]
    LS = LS or PR.lot_static()
    P = partition(LS)
    mu = LS['mu']
    if base == 'np':
        c = np.asarray(mu, dtype=np.float64).cumsum(); c = c / c[-1]
    else:
        c = np.asarray(RR.static(LS)['cumL'], dtype=np.float64)
    nsp = len(c)
    if prior == 'L':
        _PT[key] = (c.copy(), np.arange(nsp, dtype=np.int64))
        return _PT[key]
    E = P['sp_E']
    W = P['sp_Res'] if prior == 'Rm' else (~E & ~P['sp_Q'])
    width = np.diff(np.concatenate([[0.0], c]))
    widx = np.nonzero(W)[0]
    mE = float(width[E].sum())
    Rb = np.cumsum(width[widx]); Rb = Rb / Rb[-1] * mE          # recipient boundaries on the E-union axis
    bnd, pm = [], []
    eacc = 0.0
    for k in range(nsp):
        if not E[k]:
            bnd.append(c[k]); pm.append(k); continue
        lo = c[k - 1] if k > 0 else 0.0
        start, end = eacc, eacc + width[k]
        r = int(np.searchsorted(Rb, start, side='right'))
        while True:
            r = min(r, len(widx) - 1)
            up = Rb[r]
            if up >= end or r == len(widx) - 1:
                bnd.append(c[k]); pm.append(int(widx[r])); break
            if up > start:
                bnd.append(lo + (up - start)); pm.append(int(widx[r]))
            r += 1
        eacc = end
    b = np.array(bnd, np.float64); p = np.array(pm, np.int64)
    assert (np.diff(b) >= 0).all()
    _PT[key] = (b, p)
    return _PT[key]


def quantile(u, prior, base='np', LS=None):
    b, p = piece_table(prior, base, LS)
    return p[np.searchsorted(b, u * b[-1], side='right')]


def table_mass(prior, base='np', LS=None):
    """Mass each spelling receives under the piece table (validation of the marginals)."""
    LS = LS or PR.lot_static()
    b, p = piece_table(prior, base, LS)
    w = np.diff(np.concatenate([[0.0], b]))
    return np.bincount(p, weights=w, minlength=len(LS['mu'])) / b[-1]


# ------------------------------------------------------------------------------------------------ cells and founders
IR = {}            # cell -> dict(part, prior, spon, N, I, sched, K, ...)


def _sp_unit(sp, LS):
    return LS['Eu'][LS['tau'][sp]]


def founders_ir(cell, rep, LS):
    if cell not in IR:
        return _PREV(cell, rep, LS)
    c = IR[cell]
    S = RR.static(LS)
    if c['part'] == 'I':
        T = 12800
        u = np.random.default_rng([T, rep, PG.SALT_PG]).random(T)
        lst = quantile(u, c['prior'], 'np', LS)
        perm = PG.permutation(T, rep)
        sp = PG.partition(lst, c['N'], c['I'], perm).copy()
    else:
        N, I = c['N'], c['I']
        u = np.random.default_rng([N, I, rep, RR.SALT]).random((I, N))
        sp = quantile(u, c['prior'], 'np', LS)
    N, I = c['N'], c['I']
    rule = np.full((I, N), PV.R_SNON, np.int64)
    unit = _sp_unit(sp, LS).astype(np.int64)
    if c['spon']:
        pos = RR.donor_positions(N, I, rep)
        for i in range(I):
            j = int(pos[i])
            sp[i, j] = S['kPB']; rule[i, j] = PV.R_H; unit[i, j] = S['uPB']
    return sp, rule, unit


_PREV = PR.founders
PR.founders = founders_ir


def _tag(prior, spon):
    return '%s_%s' % (prior, 'spon' if spon else 'snon')


def reg_ff(prior, spon):
    name = 'ir_ff_%s' % _tag(prior, spon)
    PG.PG[name] = dict(T=12800, N=100, I=128, prior='ir:' + prior, r=PG.R_CONST, rarm='c', mN=PG.mN_cal(100),
                       merge_at=200)
    PR.CELLS[name] = (100, 128, 'S-nonself', 'ir:' + prior, 'ext')
    IR[name] = dict(part='I', prior=prior, spon=spon, N=100, I=128, T=12800, merge_at=200, horizon=2200)
    return name


def reg_isl(prior, spon, N=200, I=64):
    name = 'ir_isl_%s_%d_%d' % (_tag(prior, spon), N, I)
    RR.register(name, N, I, 'sponsored' if spon else 'S-nonself', 0.0, 'cal')
    IR[name] = dict(part='II', prior=prior, spon=spon, N=N, I=I, horizon=10000)
    return name


def reg_rain(prior, sched, N, I=8, K=3):
    name = 'ir_rain_%s_%s_%d' % (sched, prior, N)
    AN._reg(name, N, I, 'S-nonself', sched, K, 'i' if sched == 'ann' else 'iv')
    IR[name] = dict(part='III', prior=prior, spon=False, N=N, I=I, sched=sched, K=K, horizon=AN.END)
    return name


CELLS_I = [reg_ff(p, s) for s in (False, True) for p in PRIORS]
CELLS_II = [reg_isl(p, s) for s in (False, True) for p in PRIORS]
CELLS_III = [reg_rain(p, sch, 800) for sch in ('ann', 'const') for p in PRIORS] + \
            [reg_rain(p, sch, 1600) for sch in ('ann', 'const') for p in ('L', 'Rm')]
STORED_I = 'pg_L_100_128_r100_ff200'
STORED_III = {('ann', 800): 'an_i_800', ('const', 800): 'an_iv_800', ('ann', 1600): 'an_i_1600',
              ('const', 1600): 'an_iv_1600'}


# ------------------------------------------------------------------------------------------------ run objects
class IRAnnRun(AN.AnnRun):
    """Annealed's run object with rain drawn through the cell prior's piece table (kernel copy with pmap)."""

    def __init__(self, cell, rep, **kw):
        super().__init__(cell, rep, **kw)
        prior = IR[cell]['prior'] if cell in IR else 'L'
        b, p = piece_table(prior, 'kern', self.LS)
        self.cumV = np.ascontiguousarray(b); self.pmap = np.ascontiguousarray(p)

    def advance(self, gens):
        LS, st = self.LS, self.LS['st']
        self.g = IK.segment_ir(
            self.g, gens, self.seed, self.N, RS.W, self.mN / self.N, self.r, self.slots, self.counts, self.paysum,
            self.pres, self.npres, self.pos, self.spcount, self.d, self.tunit, self.trule, self.tsp, self.tanc,
            self.ntv, st['utau'], st['BLC'], st['BLD'], st['SINGLE'], st['APP'], LS['PRODC'], LS['PD'], st['KIND'],
            st['NAT'], st['CHC'], st['CHD'], st['UVt'], self.A, self.selfa, LS['OSV'], LS['SPO'], LS['capable'],
            LS['COSTS'], self.ctr, self.steps_rule, self.wn, self.wenc, self.wsp, self.wcode, self.wsid, self.ckey,
            self.cval, self.ncache, self.plog, self.hist_wait, self.hist_acq, self.hist_steps, self.hist_cens,
            self.nprod, LS['ident'], LS['spo_unit'], self.tset, self.uns, self.rulecount, self.enc_exp, self.skip,
            LS['FUT'], self.fcount, self.enc_futile, self.err,
            self.epsg, self.pairmode, self.fseed, self.cumV, self.pmap, self.spE, PV.R_SNON, bool(self.track),
            self.lin, self.nlin, self.fr, self.frf, self.nfr, self.rcount)
        if self.err[0] != 0:
            raise RuntimeError('kernel error %d in %s rep %d at generation %d (types %d)' % (
                self.err[0], self.cell, self.rep, self.g, self.ntv[0]))
        if self.track and self.nfr[0] >= self.fr.shape[0]:
            raise RuntimeError('arrival records overflow in %s rep %d' % (self.cell, self.rep))


# ------------------------------------------------------------------------------------------------ statistics helpers
def unit_class(u, P):
    """'res' / 'ex' (target units), '' otherwise."""
    if P['resu'][u]: return 'res'
    if P['exu'][u]: return 'ex'
    return ''


def island_targets(holder_units, labels, P):
    """Counts of target islands held by resistant and exploitable units."""
    res = sum(1 for u, l in zip(holder_units, labels) if l == '' and P['resu'][u])
    ex = sum(1 for u, l in zip(holder_units, labels) if l == '' and P['exu'][u])
    return res, ex


def uot70(snap, P):
    return bool(snap['uot'] and all(P['resu'][u] for u in snap['holder_unit']))


def establishment(sp0, holder_units, labels, LS, P):
    """M2: per class, seeded copies, islands held by a unit of a run tree of that class seeded on that island, and
    islands with the class seeded."""
    tau = LS['tau']; utau = np.asarray(LS['st']['utau'])
    Q_trees = set(tau[LS['Q']].tolist())
    fb_tree = int(tau[LS['names'].index('if(CHK(them,me,C),C,D)')])
    out = {k: dict(copies=0, islands_seeded=0, held_own=0) for k in ('Res', 'E', 'Q', 'FB')}
    res_t = set(P['rest']); ex_t = set(P['ext'])
    for i in range(sp0.shape[0]):
        trees = tau[sp0[i]]
        ht = int(utau[holder_units[i]]) if labels[i] != 'unheld' else -1
        seeded = set(trees.tolist())
        for k, ts in (('Res', res_t), ('E', ex_t), ('Q', Q_trees), ('FB', {fb_tree})):
            n = int(np.isin(trees, list(ts)).sum())
            out[k]['copies'] += n
            out[k]['islands_seeded'] += int(n > 0)
            out[k]['held_own'] += int(ht in ts and ht in seeded)
    return out
