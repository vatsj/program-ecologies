"""The inspection game's enforcer and its shadow (spec specs/2026-10-24-inspection-shadow.md; notes notes/inspection-shadow.md;
predictions predictions/2026-10-24-inspection-shadow.md).

Library on top of `mixed2` (imported, not edited): the efficient sets E, R, E* on class pairs; the prudent-inspectee class and
the exact boosted / matched-control priors; the whole-state-space eps -> 0 chain with a blocked, subtraction-free GTH solver
that also returns the censored chain on a kept set with reward vectors (first-passage statistics from the same pass); the
exit decomposition (mutant role, class, fate, set crossed); the eps = 0 lottery with rain and scheduled arrivals
(`lottery3`, identical to `mixed2.lottery2` when neither is used); weighted founder draws; direct-start cells.

Every chain number is an eps -> 0 object (pi over pairs of monomorphic role classes, whole state space, no exploration cap);
every lottery number is an eps = 0 finite-(N, I, horizon) statistic, with the declared rain where a remedy has one.
"""
import os, sys, math, time, copy, json, gzip
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mixed2 as M

ROOT = M.ROOT
W = M.W
TOL = 1e-9
EFF = -0.05
NMAX = 8
GAME = 'insp'


# ======================================================================================================== class tables
def get_arm(arm, c):
    """class-level table of the inspection game, n = 8, D = 12 (cached by mixed2; read-only use)."""
    return M.get_arm(GAME, arm, NMAX, c)


def named(A):
    """class indices of the named programs present in the arm (keys I, N, X, CRI, RI, P38 ... for role 0; C, K, X, CRC ... for role 1)."""
    nm = M.named_idx(A)
    return {k.replace(':', ''): v for k, v in nm.items()}       # '0I' '0N' '0CRI' '1C' '1K' ...


def find_class(A, r, name):
    """class index whose representative spelling is `name`."""
    for i, s in enumerate(A.names[r]):
        if s == name:
            return i
    raise KeyError(name)


def class_flags(A):
    """per-class behavioural flags used by the sets and the exit categories."""
    nm = named(A)
    K, C = nm['1K'], nm['1C']
    d = np.maximum(1.0 - A.F0, 1e-300)
    p_pair = A.G0[:, :, 0] / d                       # (K0, K1): P(inspect | acts) of inspector class a against inspectee class b
    d1 = np.maximum(1.0 - A.F1, 1e-300)
    q_pair = (A.G1[:, :, 1] / d1).T                  # (K0, K1): P(cheat | acts)
    fl = dict(pK=p_pair[:, K], pC=p_pair[:, C])
    fl['deter0'] = fl['pK'] > 0.25 + TOL             # deters the constant cheater: K earns less than C against it
    fl['strict0'] = (fl['pK'] >= 1 - TOL) & (fl['pC'] <= TOL)
    fl['reader0'] = A.reader[0].astype(bool)
    fl['reader1'] = A.reader[1].astype(bool)
    fl['isK1'] = np.zeros(A.K[1], bool); fl['isK1'][K] = True
    fl['p'] = np.nan_to_num(p_pair, nan=0.5)
    fl['q'] = np.nan_to_num(q_pair, nan=0.5)
    fl['F0'] = A.F0; fl['F1'] = A.F1.T
    fl['u0'] = A.UAg; fl['u1'] = A.UBg.T
    return fl


def pair_sets(A, fl=None):
    """boolean (K0, K1) masks: E (both game payoffs >= -0.05), R (E with a K-deterring inspector), Rstar (strict responsive inspector),
    Estar (E, no forfeit mass >= 0.05, inspection and cheating probabilities both < 0.05)."""
    fl = fl or class_flags(A)
    E = (fl['u0'] >= EFF - 1e-12) & (fl['u1'] >= EFF - 1e-12)
    R = E & fl['deter0'][:, None]
    Rs = E & fl['strict0'][:, None]
    Es = E & (fl['F0'] < 0.05) & (fl['F1'] < 0.05) & (fl['p'] <= 0.05) & (fl['q'] <= 0.05)
    return dict(E=E, R=R, Rstar=Rs, Estar=Es)


OCC_ORDER = ('forfeit', 'shadow_excursion', 'cheater_major_other', 'light_cheater', 'committed_compliant', 'mixing', 'other')


def occupancy_codes(A, fl=None):
    """(K0, K1) integer code of the (non-E) detour category of every pair, by the exclusive order OCC_ORDER; E pairs get -1."""
    fl = fl or class_flags(A)
    p, q = fl['p'], fl['q']
    E = pair_sets(A, fl)['E']
    code = np.full(E.shape, len(OCC_ORDER) - 1, np.int64)
    mixing = ((p > 0.02) & (p < 0.98)) | ((q > 0.02) & (q < 0.98))
    code[mixing] = 5
    code[(p > 0.25 + 5e-3) & (q < 0.1)] = 4
    code[(q > 0.02) & (q <= 0.25 + 5e-3) & (p <= 0.02)] = 3
    code[q > 0.5] = 2
    code[(q > 0.5) & (~fl['deter0'])[:, None]] = 1
    code[(fl['F0'] > 0.5) | (fl['F1'] > 0.5)] = 0
    code[E] = -1
    return code


# ======================================================================================================== the prudent class and priors
def prudent_classes(A):
    """inspectee classes that play C with probability 1 against `cr(THEM(ME))` and K with probability 1 against `N`, no forfeit."""
    nm = named(A)
    N_, CRI = nm['0N'], nm['0CRI']
    return np.nonzero((A.G1[:, CRI, 0] > 1 - 1e-9) & (A.G1[:, N_, 1] > 1 - 1e-9) & (A.F1[:, CRI] < 1e-9) & (A.F1[:, N_] < 1e-9))[0]


def mass_variant(A, kind, factor=10.0):
    """Inspectee prior (class level) for the remedy: kind 'base', 'boost' (prudent classes x factor, the added mass taken
    proportionally from all inspectee classes outside S) or 'control' (the same added mass given to the class of C, taken
    proportionally from all classes outside C).  Returns (mass, class_factor, info)."""
    m = A.mass[1].copy()
    nm = named(A)
    S = prudent_classes(A)
    mS = m[S].sum()
    delta = (factor - 1.0) * mS
    if kind == 'base':
        new = m
    elif kind == 'boost':
        inS = np.zeros(len(m), bool); inS[S] = True
        new = np.where(inS, m * factor, m * (1.0 - mS - delta) / (1.0 - mS))
    elif kind == 'control':
        C = nm['1C']
        new = m * (1.0 - m[C] - delta) / (1.0 - m[C])
        new[C] = m[C] + delta
    else:
        raise ValueError(kind)
    new = new / new.sum()
    return new, new / m, dict(kind=kind, S=S.tolist(), mS=float(mS), delta=float(delta), m_new_S=float(new[S].sum()), m_new_C=float(new[nm['1C']]))


def variant_arm(A, kind, factor=10.0):
    """shallow copy of the arm with the inspectee prior replaced."""
    mass, fac, info = mass_variant(A, kind, factor)
    B = copy.copy(A)
    B.mass = [A.mass[0], mass]
    B.variant = info
    B.class_factor = fac
    return B


# ======================================================================================================== blocked GTH
@njit(cache=True)
def _panel(A, rew, s, k0, k1):
    """Eliminate states k1-1 .. k0 (GTH, subtraction-free) updating only the panel: the rows of the block (all columns < k) and the
    block columns of the rows below k0.  The trailing block [0,k0) x [0,k0) and its rewards are updated by the caller."""
    nr = rew.shape[1]
    for k in range(k1 - 1, k0 - 1, -1):
        sk = 0.0
        for j in range(k):
            sk += A[k, j]
        if sk <= 0.0:
            sk = 1e-300
        s[k] = sk
        for i in range(k0, k):
            aik = A[i, k]
            if aik == 0.0:
                continue
            f = aik / sk
            for j in range(k):
                A[i, j] += f * A[k, j]
            for r in range(nr):
                rew[i, r] += f * rew[k, r]
        for i in range(k0):
            aik = A[i, k]
            if aik == 0.0:
                continue
            f = aik / sk
            for j in range(k0, k):
                A[i, j] += f * A[k, j]


@njit(cache=True)
def _backsub(A, s):
    n = A.shape[0]
    x = np.zeros(n)
    x[0] = 1.0
    tot = 1.0
    for k in range(1, n):
        v = 0.0
        for i in range(k):
            v += x[i] * A[i, k]
        x[k] = v / s[k]
        tot += x[k]
    return x / tot


def gth_blocked(P, rew, m=0, block=128, chunk=2048):
    """Stationary vector of the jump chain P (row-stochastic, dense, C-contiguous; DESTROYED) by blocked GTH elimination from the last
    index down.  `rew` (n, nr) are state rewards, accumulated through the elimination (expected reward until the next visit of the
    kept set).  If 2 <= m < n, the censored chain on states [0, m) is returned: (x, B, Rw) with B (m, m) row-stochastic (diagonal =
    return probability) and Rw (m, nr) the reward until the next kept visit; otherwise (x, None, None)."""
    n = P.shape[0]
    P[np.diag_indices(n)] = 0.0
    s = np.zeros(n)
    snap = None
    hi = n
    if 2 <= m < n:
        pass
    else:
        m = 0
    while hi > 1:
        lo = max(m, hi - block) if (m and m < hi) else max(1, hi - block)
        lo = max(lo, 1)
        _panel(P, rew, s, lo, hi)
        F = (P[:lo, lo:hi] / s[lo:hi]).astype(P.dtype, copy=False)
        Rows = P[lo:hi, :lo]
        for i0 in range(0, lo, chunk):
            i1 = min(lo, i0 + chunk)
            P[i0:i1, :lo] += F[i0:i1] @ Rows
        rew[:lo] += F.astype(np.float64) @ rew[lo:hi]
        hi = lo
        if m and hi == m:
            snap = (P[:m, :m].copy(), rew[:m].copy())
    x = _backsub(P, s)
    if snap is None:
        return x, None, None
    return x, snap[0], snap[1]


@njit(cache=True)
def _censor(A, rew, nkeep):
    """plain GTH censoring: eliminate states n-1 .. nkeep (in place); rows/rewards of [0, nkeep) become the censored chain."""
    n = A.shape[0]
    nr = rew.shape[1]
    for k in range(n - 1, nkeep - 1, -1):
        sk = 0.0
        for j in range(k):
            sk += A[k, j]
        if sk <= 0.0:
            sk = 1e-300
        for i in range(k):
            aik = A[i, k]
            if aik == 0.0:
                continue
            f = aik / sk
            for j in range(k):
                A[i, j] += f * A[k, j]
            for r in range(nr):
                rew[i, r] += f * rew[k, r]


def censor_to(B, Rw, keep):
    """censored chain of (B, Rw) on the index list `keep` (order kept): returns (B', R') with B' (len(keep), len(keep))."""
    n = B.shape[0]
    keep = list(keep)
    ks = set(keep)
    rest = [i for i in range(n) if i not in ks]
    perm = np.array(keep + rest, np.int64)
    Bp = np.ascontiguousarray(B[np.ix_(perm, perm)])
    Rp = np.ascontiguousarray(Rw[perm])
    _censor(Bp, Rp, len(keep))
    return Bp[:len(keep), :len(keep)].copy(), Rp[:len(keep)].copy()


def first_passage(B, Rw, start, target_mask):
    """From kept state `start` (index into B), the law of the first kept state of `target_mask` (bool over B's indices) and the expected
    reward accumulated before it.  Returns (probs over the target indices dict idx->prob, reward vector)."""
    tgt = [i for i in range(B.shape[0]) if target_mask[i] and i != start]
    Bk, Rk = censor_to(B, Rw, [start] + tgt)
    stay = Bk[0, 0]
    leave = Bk[0, 1:].sum()
    probs = Bk[0, 1:] / leave
    rew = Rk[0] / leave
    return {t: float(p) for t, p in zip(tgt, probs)}, rew, float(stay)


# ======================================================================================================== the whole-space chain
class Whole:
    """The eps -> 0 chain on all K0 x K1 pairs of monomorphic role classes for one (arm, price, prior variant, N)."""

    def __init__(self, A, N):
        self.A, self.N = A, N
        self.ch = M.TwoPopChain(A, N)
        self.K0, self.K1 = A.K
        self.lmu0, self.lmu1 = self.ch.lmu0, self.ch.lmu1

    def log_exit_rates(self):
        K0, K1, N = self.K0, self.K1, self.N
        lR1 = np.empty((K0, K1)); lR2 = np.empty((K0, K1))
        UA, UB = self.A.UA, self.A.UB
        for b in range(K1):
            du = UA[:, b][None, :] - UA[:, b][:, None]
            L = self.lmu0[None, :] + M.lrho(du, N, W)
            np.fill_diagonal(L, -np.inf)
            lR1[:, b] = np.logaddexp.reduce(L, axis=1)
        for a in range(K0):
            du = UB[:, a][None, :] - UB[:, a][:, None]
            L = self.lmu1[None, :] + M.lrho(du, N, W)
            np.fill_diagonal(L, -np.inf)
            lR2[a, :] = np.logaddexp.reduce(L, axis=1)
        return np.logaddexp(lR1, lR2)

    def solve(self, keep_mask=None, rew_fn=None, rel_drop=1e-30, block=128, dtype=np.float64):
        """Stationary log-distribution of the whole chain.  keep_mask (K0, K1) bool: states placed first and returned as the censored
        chain; rew_fn(hold) -> (S, nr) rewards from the holding times hold = 1/R (mutation events).  Returns lpi (S,), snapshot dict."""
        K0, K1, N, A = self.K0, self.K1, self.N, self.A
        S = K0 * K1
        lR = self.log_exit_rates().ravel()
        keep = np.zeros(S, bool) if keep_mask is None else keep_mask.ravel()
        o_keep = np.nonzero(keep)[0]; o_rest = np.nonzero(~keep)[0]
        order = np.concatenate([o_keep[np.argsort(lR[o_keep], kind='stable')], o_rest[np.argsort(lR[o_rest], kind='stable')]])
        inv = np.empty(S, np.int64); inv[order] = np.arange(S)
        P = np.zeros((S, S), dtype=dtype)
        for i in range(S):
            s = int(order[i])
            a, b = divmod(s, K1)
            L1, L2 = self.ch.rates(s)
            t1 = inv[np.arange(K0) * K1 + b]; t2 = inv[a * K1 + np.arange(K1)]
            p1 = np.exp(L1 - lR[s]); p2 = np.exp(L2 - lR[s])
            p1[p1 < rel_drop] = 0.0; p2[p2 < rel_drop] = 0.0
            tot = p1.sum() + p2.sum()
            P[i, t1] = p1 / tot; P[i, t2] += p2 / tot
        hold = np.exp(-lR[order])
        rew = np.zeros((S, 1)) if rew_fn is None else np.ascontiguousarray(rew_fn(hold, order))
        m = len(o_keep)
        x, B, Rw = gth_blocked(P, rew, m=m if (0 < m < S) else 0, block=block)
        del P
        xj = np.empty(S); xj[order] = x
        with np.errstate(divide='ignore'):
            lpi = np.log(np.maximum(xj, 0.0)) - lR
        lpi -= np.logaddexp.reduce(lpi[np.isfinite(lpi)])
        snap = None
        if B is not None:
            snap = dict(B=B, Rw=Rw, kept=o_keep[np.argsort(lR[o_keep], kind='stable')], lR=lR)
        self.lR = lR
        return lpi, snap


# ======================================================================================================== exit decomposition
CATS = ('A_neutral_shadow', 'B_neutral_other', 'C_strict_K', 'D_strict_other_nonreader', 'E_strict_reader_clean', 'E_strict_reader_forfeit',
        'F_strict_inspector', 'G_deleterious')


def decompose(A, N, pi, sets, fl, mass=None):
    """Stationary flux and conditional hazards out of each set X in `sets` (dict of (K0,K1) bool masks), by mutant role, class and fate,
    plus the balance residual and circulation index.  pi (K0, K1) sums to 1.  Rates per mutation event (mutant role with probability 1/2,
    class by prior mass, Moran fixation under fitness exp(w du))."""
    K0, K1 = A.K
    m0 = A.mass[0]; m1 = (A.mass[1] if mass is None else mass)
    lmu0 = np.log(0.5 * m0); lmu1 = np.log(0.5 * m1)
    acc = {X: dict(fl0=np.zeros((K0, 3)), fl1=np.zeros((K1, 3)), fl1f=np.zeros((K1, 3)), s1=np.zeros(2)) for X in sets}
    inflow = np.zeros((K0, K1)); outtot = np.zeros((K0, K1))
    circ_num = 0.0; flux_tot = 0.0
    for b in range(K1):
        du = A.UA[:, b][None, :] - A.UA[:, b][:, None]
        rate = np.exp(lmu0[None, :] + M.lrho(du, N, W)); np.fill_diagonal(rate, 0.0)
        Wt = pi[:, b][:, None] * rate
        fate = np.where(du > TOL, 1, np.where(du < -TOL, 2, 0))
        outtot[:, b] += rate.sum(1); inflow[:, b] += Wt.sum(0)
        circ_num += np.abs(Wt - Wt.T).sum(); flux_tot += Wt.sum()
        for X, mk in sets.items():
            WX = Wt * (mk[:, b][:, None] & ~mk[:, b][None, :])
            for f in range(3):
                acc[X]['fl0'][:, f] += (WX * (fate == f)).sum(0)
    for a in range(K0):
        du = A.UB[:, a][None, :] - A.UB[:, a][:, None]
        rate = np.exp(lmu1[None, :] + M.lrho(du, N, W)); np.fill_diagonal(rate, 0.0)
        Wt = pi[a, :][:, None] * rate
        fate = np.where(du > TOL, 1, np.where(du < -TOL, 2, 0))
        ff = ((A.F1[:, a] > 0.05) | (A.F0[a, :] > 0.05))
        outtot[a, :] += rate.sum(1); inflow[a, :] += Wt.sum(0)
        circ_num += np.abs(Wt - Wt.T).sum(); flux_tot += Wt.sum()
        for X, mk in sets.items():
            WX = Wt * (mk[a, :][:, None] & ~mk[a, :][None, :])
            for f in range(3):
                acc[X]['fl1'][:, f] += (WX * (fate == f)).sum(0)
                acc[X]['fl1f'][:, f] += (WX * (fate == f) * ff[None, :]).sum(0)
            acc[X]['s1'][int(fl['deter0'][a])] += (WX * (fate == 1)).sum()      # strict inspectee flux by whether the resident inspector deters K
    out = {}
    typ1 = np.where(fl['isK1'], 0, np.where(fl['reader1'], 1, 2))
    for X, mk in sets.items():
        piX = float(pi[mk].sum())
        a_ = acc[X]
        cats = {k: 0.0 for k in CATS}
        for q in range(K0):
            cats['A_neutral_shadow' if not fl['deter0'][q] else 'B_neutral_other'] += a_['fl0'][q, 0]
            cats['F_strict_inspector'] += a_['fl0'][q, 1]
            cats['G_deleterious'] += a_['fl0'][q, 2]
        for q in range(K1):
            cats['B_neutral_other'] += a_['fl1'][q, 0]
            cats['G_deleterious'] += a_['fl1'][q, 2]
            if typ1[q] == 0:
                cats['C_strict_K'] += a_['fl1'][q, 1]
            elif typ1[q] == 1:
                cats['E_strict_reader_forfeit'] += a_['fl1f'][q, 1]
                cats['E_strict_reader_clean'] += a_['fl1'][q, 1] - a_['fl1f'][q, 1]
            else:
                cats['D_strict_other_nonreader'] += a_['fl1'][q, 1]
        flux = sum(cats.values())
        top = []
        for q in range(K0):
            for f in range(3):
                if a_['fl0'][q, f] > 0:
                    top.append((a_['fl0'][q, f], 0, q, f))
        for q in range(K1):
            for f in range(3):
                if a_['fl1'][q, f] > 0:
                    top.append((a_['fl1'][q, f], 1, q, f))
        top.sort(reverse=True)
        fate_name = ('neutral', 'strict', 'deleterious')
        out[X] = dict(pi=piX, flux=float(flux), hazard=float(flux / piX) if piX > 0 else None,
                      cats={k: dict(flux=float(v), hazard=float(v / piX) if piX > 0 else None, share=float(v / flux) if flux > 0 else None) for k, v in cats.items()},
                      largest=max(cats, key=cats.get) if flux > 0 else None,
                      strict_inspectee_from=dict(nondeterring_inspector=float(a_['s1'][0]), deterring_inspector=float(a_['s1'][1])),
                      top=[dict(role=r, cls=A.names[r][q], fate=fate_name[f], flux=float(v), hazard=float(v / piX), share=float(v / flux)) for v, r, q, f in top[:12]])
    with np.errstate(divide='ignore', invalid='ignore'):
        occ = pi * outtot
        res = np.where(occ > 1e-300, np.abs(inflow - occ) / np.maximum(occ, 1e-300), 0.0)
    bal = dict(max_rel_residual=float(res[occ > 1e-14 * occ.max()].max()), total_flux=float(flux_tot), circulation=float(circ_num / (2 * flux_tot)) if flux_tot > 0 else 0.0,
               sum_abs_resid_over_flux=float(np.abs(inflow - occ).sum() / max(flux_tot, 1e-300)))
    return out, bal


def reference_exits(A, N, a, b, mass=None):
    """rates (per mutation event) out of one class pair by role and fate, with the top targets; the one-state calculation of notes section 1."""
    m1 = A.mass[1] if mass is None else mass
    r0 = np.exp(np.log(0.5 * A.mass[0]) + M.lrho(A.UA[:, b] - A.UA[a, b], N, W)); r0[a] = 0.0
    r1 = np.exp(np.log(0.5 * m1) + M.lrho(A.UB[:, a] - A.UB[b, a], N, W)); r1[b] = 0.0
    d0 = A.UA[:, b] - A.UA[a, b]; d1 = A.UB[:, a] - A.UB[b, a]
    f = lambda r, d: dict(neutral=float(r[np.abs(d) <= TOL].sum()), strict=float(r[d > TOL].sum()), deleterious=float(r[d < -TOL].sum()))
    tops = sorted([(r0[q], 0, q) for q in range(len(r0)) if r0[q] > 0] + [(r1[q], 1, q) for q in range(len(r1)) if r1[q] > 0], reverse=True)[:6]
    return dict(inspector=f(r0, d0), inspectee=f(r1, d1), total=float(r0.sum() + r1.sum()),
                top=[dict(role=r, cls=A.names[r][q], rate=float(v), du=float((d0 if r == 0 else d1)[q])) for v, r, q in tops])


# ======================================================================================================== one chain cell
def rewards_factory(codes, fl):
    """reward columns by holding time: total, forfeit, shadow_excursion, cheater_major_other, light_cheater, committed_compliant, mixing, visits."""
    def fn(hold, order):
        code = codes.ravel()[order]
        R = np.zeros((len(order), 8))
        R[:, 0] = hold
        for c in range(6):
            R[:, 1 + c] = np.where(code == c, hold, 0.0)
        R[:, 7] = 1.0
        return R
    return fn


REWARD_NAMES = ('time_total', 'time_forfeit', 'time_shadow_excursion', 'time_cheater_major_other', 'time_light_cheater',
                'time_committed_compliant', 'time_mixing', 'visits')


def start_states(A):
    """named starting states for the first-passage statistics: (label, inspector class, inspectee class)."""
    nm = named(A)
    out = []
    def add(label, a, b):
        if a is not None and b is not None:
            out.append((label, int(a), int(b)))
    g = lambda k: nm.get(k)
    lc = None
    try:
        lc = find_class(A, 1, 'coin(C,coin(C,X))')
    except KeyError:
        pass
    add('(N,K)', g('0N'), g('1K')); add('(I,K)', g('0I'), g('1K')); add('(I,C)', g('0I'), g('1C'))
    add('(CRI,light1/8)', g('0CRI'), lc); add('(N,light1/8)', g('0N'), lc); add('(P38,C)', g('0P38'), g('1C'))
    return out


def chain_cell(arm, c, N, variant='base', passage=True, verbose=True, dtype=np.float64):
    """Whole-space chain for one cell; returns a JSON-able dict (no arrays of state size)."""
    t0 = time.time()
    A0 = get_arm(arm, c)
    A = variant_arm(A0, variant) if variant != 'base' else A0
    fl = class_flags(A)
    sets = pair_sets(A, fl)
    codes = occupancy_codes(A, fl)
    K0, K1 = A.K
    W_ = Whole(A, N)
    starts = start_states(A) if passage else []
    keep = sets['E'].copy()
    for _, a, b in starts:
        keep[a, b] = True
    lpi, snap = W_.solve(keep_mask=keep if passage else None, rew_fn=rewards_factory(codes, fl) if passage else None, dtype=dtype)
    t_solve = time.time() - t0
    pi = np.exp(lpi).reshape(K0, K1)
    pi /= pi.sum()
    res = dict(arm=arm, c=c, N=N, variant=variant, K=[K0, K1], S=K0 * K1, solve_s=t_solve, dtype=np.dtype(dtype).name, vector='chain (eps -> 0, whole state space)')
    if variant != 'base':
        res['prior'] = A.variant
    # headline statistics
    u0, u1, p, q = fl['u0'], fl['u1'], fl['p'], fl['q']
    stat = dict(u0g=float((pi * u0).sum()), u1g=float((pi * u1).sum()), p_insp=float((pi * p).sum()), q_cheat=float((pi * q).sum()),
                forfeit0=float((pi * fl['F0']).sum()), forfeit1=float((pi * fl['F1']).sum()))
    res['stat'] = stat
    res['pi_sets'] = {k: float(pi[m].sum()) for k, m in sets.items()}
    res['pi_E_not_R'] = float(pi[sets['E'] & ~sets['R']].sum())
    res['pi_E_forfeit_mass'] = float((pi * fl['F0'])[sets['E']].sum() + (pi * fl['F1'])[sets['E']].sum())
    pe = res['pi_sets']['E']
    res['odds_E'] = pe / max(1.0 - pe, 1e-300)
    res['odds_R'] = res['pi_sets']['R'] / max(1.0 - res['pi_sets']['R'], 1e-300)
    res['occupancy'] = {OCC_ORDER[k]: float(pi[codes == k].sum()) for k in range(len(OCC_ORDER))}
    res['occupancy']['E'] = pe
    # class shares and top states
    sh0 = pi.sum(1); sh1 = pi.sum(0)
    res['top_states'] = []
    flat = np.argsort(-pi.ravel())[:12]
    for s in flat:
        a, b = divmod(int(s), K1)
        res['top_states'].append(dict(pi=float(pi[a, b]), insp=A.names[0][a], ee=A.names[1][b], u0g=float(u0[a, b]), u1g=float(u1[a, b]),
                                      in_E=bool(sets['E'][a, b]), in_R=bool(sets['R'][a, b])))
    cs = np.cumsum(np.sort(pi.ravel())[::-1])
    res['n_states_for_099'] = int(np.searchsorted(cs, 0.99) + 1)
    res['top_insp'] = [(A.names[0][i], float(sh0[i])) for i in np.argsort(-sh0)[:8]]
    res['top_ee'] = [(A.names[1][i], float(sh1[i])) for i in np.argsort(-sh1)[:8]]
    nm = named(A)
    res['named_share'] = {k: float(sh0[v] if k[0] == '0' else sh1[v]) for k, v in nm.items()}
    res['reader_share'] = [float(sh0[fl['reader0']].sum()), float(sh1[fl['reader1']].sum())]
    # exits
    ex, bal = decompose(A, N, pi, sets, fl)
    res['exits'] = ex
    res['balance'] = bal
    # renewal identities (exact): mean sojourn in X and mean time outside X
    for X in ('E', 'R'):
        fX = ex[X]['flux']
        px = ex[X]['pi']
        res['renewal_' + X] = dict(mean_sojourn=px / fX if fX > 0 else None, mean_time_outside=(1 - px) / fX if fX > 0 else None, flux_out=fX)
    # first passage from the named starts
    if passage and snap is not None:
        res['first_passage'] = passage_stats(A, snap, sets, fl, starts, K1)
    # the one-state calculations of the notes
    refs = {}
    for lab, a, b in [('(CRI,C)', nm.get('0CRI'), nm.get('1C')), ('(N,C)', nm.get('0N'), nm.get('1C')), ('(N,K)', nm.get('0N'), nm.get('1K'))]:
        if a is not None and b is not None:
            refs[lab] = reference_exits(A, N, a, b)
    res['reference_exits'] = refs
    res['time_s'] = time.time() - t0
    if verbose:
        print('  [%s c=%g %s N=%d] S=%d solve %.0fs total %.0fs  u0g=%.4f u1g=%.4f pi(E)=%.4f pi(R)=%.4f  bal=%.1e' % (
            arm, c, variant, N, K0 * K1, t_solve, res['time_s'], stat['u0g'], stat['u1g'], pe, res['pi_sets']['R'], bal['max_rel_residual']), flush=True)
    return res


def passage_stats(A, snap, sets, fl, starts, K1):
    """first entry into E and into R from the named starts, by the censored chain on E + starts (exact; same elimination pass)."""
    B, Rw, kept = snap['B'], snap['Rw'], snap['kept']
    K0 = A.K[0]
    pos = {int(s): i for i, s in enumerate(kept)}
    inE = np.array([bool(sets['E'].ravel()[s]) for s in kept])
    inR = np.array([bool(sets['R'].ravel()[s]) for s in kept])
    out = {}
    for lab, a, b in starts:
        s = a * K1 + b
        if s not in pos:
            continue
        i0 = pos[s]
        tgtE = inE.copy(); tgtE[i0] = False
        if not tgtE.any():
            continue
        probs, rew, stay = first_passage(B, Rw, i0, tgtE)
        pR = sum(p for t, p in probs.items() if inR[t])
        entry = sorted(probs.items(), key=lambda kv: -kv[1])[:5]
        d = dict(P_first_entry_in_R=float(pR), P_first_entry_in_E_not_R=float(1 - pR), mean_time_to_E=float(rew[0]),
                 reward={REWARD_NAMES[j]: float(rew[j]) for j in range(1, len(REWARD_NAMES))},
                 entry_states=[dict(p=float(p), insp=A.names[0][int(kept[t]) // K1], ee=A.names[1][int(kept[t]) % K1]) for t, p in entry])
        # first passage to R: the E-not-R states become transient
        tgtR = inR.copy(); tgtR[i0] = False
        if tgtR.any():
            probsR, rewR, _ = first_passage(B, Rw, i0, tgtR)
            d['mean_time_to_R'] = float(rewR[0])
            d['reward_to_R'] = {REWARD_NAMES[j]: float(rewR[j]) for j in range(1, len(REWARD_NAMES))}
            d['entry_states_R'] = [dict(p=float(p), insp=A.names[0][int(kept[t]) // K1], ee=A.names[1][int(kept[t]) % K1])
                                   for t, p in sorted(probsR.items(), key=lambda kv: -kv[1])[:4]]
        out[lab] = d
    return out


# ======================================================================================================== weighted founders
def draw_founders_w(lang, r, cls_of, K, I, N, seed, cls_factor=None):
    """(I, K) founder class counts for role r.  With cls_factor None this is `mixed2.draw_founders` (same uniforms, same inverse CDFs).
    Otherwise every program is weighted by cls_factor[its class] inside the same size-then-quantile construction (the exact reweighted
    length prior): a size is drawn from the reweighted size distribution, the program within the size by the reweighted spelling mass."""
    if cls_factor is None:
        return M.draw_founders(lang, r, cls_of, K, I, N, seed)
    rng = np.random.default_rng(seed)
    u1 = rng.random(I * N); u2 = rng.random(I * N)
    ids = lang.progs[r]
    sizes = lang.size[ids]
    wprog = cls_factor[cls_of]
    nmax = len(lang.a_size[r])
    ps0 = M.length_prior_sizes(lang, r)
    ps = np.zeros(nmax)
    cm_by = {}
    for s in range(1, nmax):
        lst = np.nonzero(sizes == s)[0]
        if len(lst) == 0 or ps0[s] == 0:
            continue
        w = lang.mult[ids[lst]] * wprog[lst]
        ps[s] = ps0[s] * w.sum() / lang.mult[ids[lst]].sum()
        cm = np.cumsum(w); cm_by[s] = (lst, cm / cm[-1])
    ps = ps / ps.sum()
    cdf = np.cumsum(ps)
    sz = np.minimum(np.searchsorted(cdf, u1, side='right'), len(ps) - 1)
    sz = np.where(ps[sz] > 0, sz, np.nonzero(ps)[0][0])
    prog = np.empty(I * N, np.int64)
    for s in range(1, len(ps)):
        sel = np.nonzero(sz == s)[0]
        if len(sel) == 0:
            continue
        lst, cm = cm_by[s]
        prog[sel] = lst[np.minimum(np.searchsorted(cm, u2[sel], side='right'), len(lst) - 1)]
    cl = cls_of[prog].reshape(I, N)
    init = np.zeros((I, K), np.int64)
    for i in range(I):
        init[i] = np.bincount(cl[i], minlength=K)
    return init


# ======================================================================================================== the lottery with rain and arrivals
@njit(cache=True)
def _apply(counts, pay, pres, npres, pos, i, p, victim, child, UA, UB, K0, K1):
    counts[i, p, victim] -= 1
    if counts[i, p, victim] == 0:
        q = pos[i, p, victim]; last = pres[i, p, npres[i, p] - 1]
        pres[i, p, q] = last; pos[i, p, last] = q; pos[i, p, victim] = -1; npres[i, p] -= 1
    if counts[i, p, child] == 0:
        pres[i, p, npres[i, p]] = child; pos[i, p, child] = npres[i, p]; npres[i, p] += 1
    counts[i, p, child] += 1
    if p == 0:
        for k in range(K1):
            pay[i, 1, k] += UB[k, child] - UB[k, victim]
    else:
        for k in range(K0):
            pay[i, 0, k] += UA[k, child] - UA[k, victim]


@njit(cache=True)
def _victim(counts, pres, npres, i, p, N):
    u = np.random.randint(N); acc = 0; victim = pres[i, p, 0]
    for t in range(npres[i, p]):
        k = pres[i, p, t]
        acc += counts[i, p, k]
        if u < acc:
            victim = k
            break
    return victim


@njit(cache=True)
def lottery3(UA, UB, init0, init1, N, w, m, seed, cps, rain_eps, rain_role, rain_cls, arr_gen, arr_role, arr_cls, arr_n):
    """`mixed2.lottery2` plus (i) rain: with probability rain_eps a birth event of role rain_role produces the class rain_cls instead of a
    sample (rain_eps = 0 changes nothing and consumes no random number), (ii) scheduled arrivals: at the start of generation arr_gen[j],
    every island's population of role arr_role[j] gets arr_n[j] individuals of class arr_cls[j] replacing uniformly chosen victims."""
    np.random.seed(seed)
    I, K0 = init0.shape
    K1 = init1.shape[1]
    KM = max(K0, K1)
    counts = np.zeros((I, 2, KM), np.int64)
    pay = np.zeros((I, 2, KM))
    pres = np.zeros((I, 2, KM), np.int64); npres = np.zeros((I, 2), np.int64); pos = -np.ones((I, 2, KM), np.int64)
    for i in range(I):
        for k in range(K0):
            counts[i, 0, k] = init0[i, k]
        for k in range(K1):
            counts[i, 1, k] = init1[i, k]
        for p in range(2):
            Kp = K0 if p == 0 else K1
            for k in range(Kp):
                if counts[i, p, k] > 0:
                    pres[i, p, npres[i, p]] = k; pos[i, p, k] = npres[i, p]; npres[i, p] += 1
        for k in range(K0):
            s = 0.0
            for j in range(K1):
                s += counts[i, 1, j] * UA[k, j]
            pay[i, 0, k] = s
        for k in range(K1):
            s = 0.0
            for j in range(K0):
                s += counts[i, 0, j] * UB[k, j]
            pay[i, 1, k] = s
    ncp = len(cps)
    out0 = np.zeros((ncp, I, K0), np.int16)
    out1 = np.zeros((ncp, I, K1), np.int16)
    gens = cps[ncp - 1]
    ci = 0
    for g in range(gens):
        for j in range(len(arr_gen)):
            if arr_gen[j] == g:
                p = arr_role[j]
                for i in range(I):
                    for r in range(arr_n[j]):
                        child = arr_cls[j]
                        victim = _victim(counts, pres, npres, i, p, N)
                        if victim != child:
                            _apply(counts, pay, pres, npres, pos, i, p, victim, child, UA, UB, K0, K1)
        for e in range(2 * I * N):
            i = np.random.randint(I)
            p = np.random.randint(2)
            src = i
            if m > 0.0 and np.random.random() < m:
                src = np.random.randint(I - 1)
                if src >= i:
                    src += 1
            if rain_eps > 0.0 and p == rain_role and np.random.random() < rain_eps:
                child = rain_cls
            else:
                child = M._sample2(counts, pay, src, p, pres, npres, N, w)
            victim = _victim(counts, pres, npres, i, p, N)
            if victim == child:
                continue
            _apply(counts, pay, pres, npres, pos, i, p, victim, child, UA, UB, K0, K1)
        gg = g + 1
        while ci < ncp and gg == cps[ci]:
            for i in range(I):
                for k in range(K0):
                    out0[ci, i, k] = counts[i, 0, k]
                for k in range(K1):
                    out1[ci, i, k] = counts[i, 1, k]
            ci += 1
    return out0, out1


def checkpoints(N, T):
    """common-t grid, common t/N grid and the last-N-generations window (every N/10)."""
    g = {25, 50, 100, 200, 300, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000, 12000, 16000}
    g |= {int(round(N * x)) for x in (0.25, 0.5, 1, 2, 3, 5, 7.5, 10, 15, 20)}
    g |= {int(T - N + j * N // 10) for j in range(0, 11)}
    return sorted(x for x in g if 0 < x <= T) + ([T] if T not in g else [])


STORE_KEYS = ('u0g', 'u1g', 'p_insp', 'q_cheat', 'isl_efficient', 'isl_commit_comply', 'isl_nashlike', 'isl_cheat_majority', 'f0', 'f1',
              'rd1', 'rdx0', 'rdx1', 'mix0', 'mix1', 'sh_0:N', 'sh_0:CRI', 'sh_0:I', 'sh_0:P38', 'sh_1:C', 'sh_1:K', 'sh_1:CRC',
              'isl_Estar', 'isl_eff_resp', 'isl_eff_shadow', 'isl_light', 'resp_mass', 'deter_mass', 'prud_mass', 'u0g_q10', 'u0g_q50', 'u0g_q90')


def island_summary(A, X0, X1, extra, fl, sets_flags):
    """island means of the standard statistics (mixed2_run.summarize) plus the E*, responsive-efficient, shadow-efficient, light-cheater
    island shares and class-group masses."""
    import mixed2_run as R2
    st = M.island_stats(A, X0, X1)
    out = R2.summarize(st, GAME)
    u0, u1 = st['u0g'], st['u1g']
    eff = (u0 >= EFF - 1e-12) & (u1 >= EFF - 1e-12)
    p = np.nan_to_num(st['p_insp'], nan=0.5); q = np.nan_to_num(st['q_cheat'], nan=0.5)
    deter = X0 @ fl['deter0'].astype(float)
    resp = X0 @ (fl['pK'] - fl['pC'] >= 0.5).astype(float)
    out['isl_Estar'] = float(np.mean(eff & (st['f0'] < 0.05) & (st['f1'] < 0.05) & (p <= 0.05) & (q <= 0.05)))
    out['isl_eff_resp'] = float(np.mean(eff & (deter >= 0.5)))
    out['isl_eff_shadow'] = float(np.mean(eff & (deter < 0.5)))
    out['isl_light'] = float(np.mean((q > 0.02) & (q <= 0.25 + 5e-3) & (p <= 0.02)))
    out['resp_mass'] = float(resp.mean()); out['deter_mass'] = float(deter.mean())
    if extra.get('S') is not None:
        out['prud_mass'] = float((X1[:, extra['S']].sum(1)).mean())
    return out, M.island_phase(st, GAME).tolist()


def compact(summ):
    return {k: (round(v, 5) if isinstance(v, float) else v) for k, v in summ.items() if k in STORE_KEYS and v is not None}


class LotCell:
    """One lottery cell: arm, price, (N, I), horizon, migration mN, optional rain, optional prior variant for the founders."""

    def __init__(self, arm, c, N, I, runs, T, mN=1.0, found='primary', dyn=None, rain=None, variant='base', tag=''):
        self.arm, self.c, self.N, self.I, self.runs, self.T, self.mN = arm, c, N, I, runs, T, mN
        self.found = found; self.dyn = dyn or found
        self.rain = rain                       # None | ('K'|'C', eps_N) rain of that inspectee class at eps_N mutants per generation
        self.variant = variant
        self.tag = tag


def run_lottery(spec, runs=None, verbose=True):
    """Run a LotCell; returns dict(runs=[...]) with compact checkpoint statistics and final top classes."""
    A0 = get_arm(spec.arm, spec.c)
    A = variant_arm(A0, spec.variant) if spec.variant != 'base' else A0
    fl = class_flags(A)
    lang = A.lang
    K0, K1 = A.K
    N, I, T = spec.N, spec.I, spec.T
    nm = named(A)
    fac = getattr(A, 'class_factor', None)
    S = None
    if spec.arm != 'blind':
        try:
            S = prudent_classes(A0)
        except KeyError:
            S = None
    rain_cls = -1; rain_eps = 0.0
    if spec.rain is not None:
        rain_cls = nm['1K'] if spec.rain[0] == 'K' else nm['1C']
        rain_eps = spec.rain[1] / N
    cps = checkpoints(N, T)
    res = []
    t0 = time.time()
    for r in (runs if runs is not None else range(spec.runs)):
        f0 = draw_founders_w(lang, 0, A.cls_of[0], K0, I, N, M.run_seed('found|%s|%d|0' % (spec.found, r), 0))
        f1 = draw_founders_w(lang, 1, A.cls_of[1], K1, I, N, M.run_seed('found|%s|%d|1' % (spec.found, r), 0), fac)
        i0 = np.nonzero(f0.sum(0) > 0)[0]
        keep1 = f1.sum(0) > 0
        if rain_cls >= 0:
            keep1 = keep1.copy(); keep1[rain_cls] = True
        i1 = np.nonzero(keep1)[0]
        UA = np.ascontiguousarray(A.UA[np.ix_(i0, i1)]); UB = np.ascontiguousarray(A.UB[np.ix_(i1, i0)])
        rc = int(np.searchsorted(i1, rain_cls)) if rain_cls >= 0 else -1
        m = spec.mN / N
        o0, o1 = lottery3(UA, UB, np.ascontiguousarray(f0[:, i0]), np.ascontiguousarray(f1[:, i1]), N, W, m,
                          M.run_seed('dyn|insp|%s|%s|%d' % (spec.arm, spec.dyn, r), 0), np.array(cps, np.int64),
                          rain_eps, 1, rc, np.zeros(0, np.int64), np.zeros(0, np.int64), np.zeros(0, np.int64), np.zeros(0, np.int64))
        rec = dict(run=r, cps=cps, stats={}, phases=[])
        for ci, g in enumerate(cps):
            X0 = np.zeros((I, K0)); X1 = np.zeros((I, K1))
            X0[:, i0] = o0[ci] / N; X1[:, i1] = o1[ci] / N
            summ, ph = island_summary(A, X0, X1, dict(S=S), fl, None)
            rec['stats'][str(g)] = compact(summ)
            rec['phases'].append(ph)
            if g in (T,):
                sh0 = X0.mean(0); sh1 = X1.mean(0)
                rec['top_end'] = dict(r0=[(A.names[0][k], round(float(sh0[k]), 4)) for k in np.argsort(-sh0)[:8] if sh0[k] > 0.005],
                                      r1=[(A.names[1][k], round(float(sh1[k]), 4)) for k in np.argsort(-sh1)[:8] if sh1[k] > 0.005])
        res.append(rec)
        if verbose:
            s = rec['stats'][str(T)]
            print('  run %d (%.0fs): eff=%.3f u0g=%.3f u1g=%.3f p=%.3f q=%.3f' % (r, time.time() - t0, s.get('isl_efficient', -1), s.get('u0g', -1), s.get('u1g', -1),
                                                                                 s.get('p_insp') or -1, s.get('q_cheat') or -1), flush=True)
    return res


# ======================================================================================================== direct starts
def run_direct(arm, c, N, base, n_inj, k_arrival, I=64, nruns=20, T=None, seed_name='direct'):
    """Islands that start monomorphic in `base` ('CRI' or 'N' for the inspectors, C for the inspectees) with n_inj copies of the other
    twin injected, no mutation and no migration; optionally one K arrival into every island's inspectee population at generation 100.
    Records at 100 (before the arrival), 100 + N/2, 100 + 2N and T: the twin's share, K's share, efficient islands, islands where the
    responsive class holds the inspector seat (deter mass >= 0.5)."""
    A = get_arm(arm, c)
    nm = named(A)
    fl = class_flags(A)
    K0, K1 = A.K
    CRI, Nn, Cc, Kk = nm['0CRI'], nm['0N'], nm['1C'], nm['1K']
    T = T or 20 * N
    cps = sorted({100, 100 + N // 2, 100 + 2 * N, T, 100 + N})
    out = []
    for r in range(nruns):
        init0 = np.zeros((I, K0), np.int64); init1 = np.zeros((I, K1), np.int64)
        b_, t_ = (CRI, Nn) if base == 'CRI' else (Nn, CRI)
        init0[:, b_] = N - n_inj; init0[:, t_] = n_inj
        init1[:, Cc] = N
        i0 = np.nonzero(init0.sum(0) > 0)[0]
        i1 = np.nonzero((init1.sum(0) > 0) | (np.arange(K1) == Kk))[0]
        UA = np.ascontiguousarray(A.UA[np.ix_(i0, i1)]); UB = np.ascontiguousarray(A.UB[np.ix_(i1, i0)])
        ag = np.array([100], np.int64) if k_arrival else np.zeros(0, np.int64)
        ar = np.array([1], np.int64) if k_arrival else np.zeros(0, np.int64)
        ac = np.array([int(np.searchsorted(i1, Kk))], np.int64) if k_arrival else np.zeros(0, np.int64)
        an = np.array([1], np.int64) if k_arrival else np.zeros(0, np.int64)
        o0, o1 = lottery3(UA, UB, np.ascontiguousarray(init0[:, i0]), np.ascontiguousarray(init1[:, i1]), N, W, 0.0,
                          M.run_seed('direct|%s|%d|%d|%d' % (seed_name, N, n_inj, r), 0), np.array(cps, np.int64), 0.0, 1, -1, ag, ar, ac, an)
        rec = dict(run=r, at={})
        for ci, g in enumerate(cps):
            X0 = np.zeros((I, K0)); X1 = np.zeros((I, K1))
            X0[:, i0] = o0[ci] / N; X1[:, i1] = o1[ci] / N
            u0 = (X0 * (X1 @ A.UAg.T)).sum(1); u1 = (X1 * (X0 @ A.UBg.T)).sum(1)
            eff = (u0 >= EFF - 1e-12) & (u1 >= EFF - 1e-12)
            deter = X0 @ fl['deter0'].astype(float)
            rec['at'][str(g)] = dict(share_CRI=float(X0[:, CRI].mean()), share_N=float(X0[:, Nn].mean()), share_K=float(X1[:, Kk].mean()),
                                     twin_fixed=float(np.mean(X0[:, t_] > 0.999)), base_fixed=float(np.mean(X0[:, b_] > 0.999)),
                                     K_majority=float(np.mean(X1[:, Kk] > 0.5)), K_fixed=float(np.mean(X1[:, Kk] > 0.999)),
                                     eff=float(eff.mean()), resp_eff=float(np.mean(eff & (deter >= 0.5))), shadow_eff=float(np.mean(eff & (deter < 0.5))),
                                     recovered=float(np.mean((deter >= 0.5) & (X1[:, Kk] < 0.01))))
        out.append(rec)
    return dict(arm=arm, c=c, N=N, base=base, n_inj=n_inj, k_arrival=k_arrival, I=I, nruns=nruns, cps=cps, runs=out)


# ======================================================================================================== json helpers
def jdump(obj, path, gz=False):
    def default(o):
        if isinstance(o, np.integer): return int(o)
        if isinstance(o, np.floating): return None if not np.isfinite(o) else float(o)
        if isinstance(o, np.ndarray): return o.tolist()
        if isinstance(o, np.bool_): return bool(o)
        raise TypeError(type(o))
    data = json.dumps(obj, default=default)
    if gz:
        with gzip.open(path, 'wt') as f: f.write(data)
    else:
        with open(path, 'w') as f: f.write(data)


def jload(path):
    if path.endswith('.gz'):
        with gzip.open(path, 'rt') as f: return json.load(f)
    with open(path) as f: return json.load(f)
