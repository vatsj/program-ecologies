"""Zero-tolerance, suspicious-default and sampling inspectors in the inspection game (spec specs/2026-10-24-zero-tolerance.md; notes
notes/zero-tolerance.md; predictions predictions/2026-10-24-zero-tolerance.md).

Library on top of `mixed2` and `inspection_shadow` (imported, not edited).  The inspection game, n = 8, exact arm, depth D (12 unless
stated).  Added inspector programs, each of the form `op(THEM(ME))`:

    zt     inspect iff the inspectee cheats against me with positive probability (exact read, forfeits on timeout like `cr`)
    crs    `cr` with the suspicious default: the timed-out mass of the read is inspected
    zts    `zt` with the suspicious default
    srK    inspect iff any of K independent simulated draws of the inspectee cheats (stops at the first cheating draw; a timed-out
           draw is a forfeit of the reader, the arm's default); sr1 is the stored sampled responder `if(THEM(ME)=C,N,I)`
    srKs   `srK` with the suspicious default

They are evaluated by the *stored kernel* `mixed2._eval_role` (for the inspectee side, one added inspector at a time) and by a few numpy
lines for the added inspector itself, level by level, so that no stored table is altered; the base program table is `mixed2.evaluate`.
An arm is the base table plus its added inspector rows/columns, collapsed into behavioural classes by `mixed2.collapse` over the arm's
inspector set.  Prior: every arm moves the same total mass m (the class mass of `cr(THEM(ME))`) onto its added program (control: onto
`cr(THEM(ME))` itself; comparator: onto `I`), taken proportionally from the other inspector programs; in the lottery the founders are the
stored draw with each inspector slot replaced, with probability m and independently of the program drawn, by that program.

Every chain number is an eps -> 0 object (pi over pairs of monomorphic role classes, whole state space, no exploration cap); every lottery
number is an eps = 0 finite-(N, I, horizon) statistic, never pi.
"""
import os, sys, math, time, copy, json, tempfile
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mixed2 as M
import inspection_shadow as S

ROOT = M.ROOT
GAME = 'insp'
NMAX = 8
D0 = 12
W = M.W
TOL = 1e-9
EFF = S.EFF
_lrho_stored = M.lrho


def lrho_safe(du, N, w=W):
    """`mixed2.lrho` with the deleterious branch evaluated without overflow: for a = -w du > 30 (payoff differences of 100 or more, which the
    k-fold nested simulation of sr_k reaches at c = 0.01: 8.9e6 levels charged) log(expm1(a)) is replaced by a + log1p(-exp(-a)).  Identical
    to the stored function (to rounding) wherever that one is finite.  Installed as `mixed2.lrho` at import, so the chain classes see it."""
    dw = w * np.asarray(du, float)
    out = _lrho_stored(np.where(-dw > 30.0, 0.0, du), N, w)
    big = -dw > 30.0
    if big.any():
        a = -dw[big]
        out = np.array(out, float)
        out[big] = a + np.log1p(-np.exp(-a)) - N * a - np.log(-np.expm1(-N * a))
    return out


M.lrho = lrho_safe
CACHE = os.environ.get('ZT_CACHE', os.path.join(tempfile.gettempdir(), 'zt_cache'))

# added programs: name -> (operator, k, suspicious, printed source)
ADDED = {
    'cr': ('cr', 0, False, 'cr(THEM(ME))'),                  # the stored exact reader (a self-test of the machinery, not an arm)
    'zt': ('zt', 0, False, 'zt(THEM(ME))'),
    'crs': ('cr', 0, True, 'cr_s(THEM(ME))'),
    'zts': ('zt', 0, True, 'zt_s(THEM(ME))'),
    'sr1': ('sr', 1, False, 'sr1(THEM(ME))'),
    'sr4': ('sr', 4, False, 'sr4(THEM(ME))'),
    'sr16': ('sr', 16, False, 'sr16(THEM(ME))'),
    'sr1s': ('sr', 1, True, 'sr1_s(THEM(ME))'),
    'sr4s': ('sr', 4, True, 'sr4_s(THEM(ME))'),
    'sr16s': ('sr', 16, True, 'sr16_s(THEM(ME))'),
}
# arm -> (added programs, class that receives the matched mass (None = the added program), moves mass at all)
ARMS = {
    'v0': dict(added=[], boost=None, mass=False),            # validation: the stored table
    'ctl': dict(added=[], boost='CRI', mass=True),           # control: the same mass to cr(THEM(ME)) itself
    'unc': dict(added=[], boost='I', mass=True),             # comparator: the same mass to the unconditional inspector
    'zt': dict(added=['zt'], boost=None, mass=True),
    'sus': dict(added=['crs'], boost=None, mass=True),
    'ztsus': dict(added=['zts'], boost=None, mass=True),
    'sr1': dict(added=['sr1'], boost=None, mass=True),
    'sr4': dict(added=['sr4'], boost=None, mass=True),
    'sr16': dict(added=['sr16'], boost=None, mass=True),
    'sr4s': dict(added=['sr4s'], boost=None, mass=True),
    'sr16s': dict(added=['sr16s'], boost=None, mass=True),
}
ARM_ORDER = ('ctl', 'zt', 'sus', 'ztsus', 'sr1', 'sr4', 'sr16', 'unc')


def parse_arm(tag):
    """'zt', 'ctl@D11' -> ('zt', 11)."""
    if '@D' in tag:
        a, d = tag.split('@D')
        return a, int(d)
    return tag, D0


# ======================================================================================================== evaluation of added inspectors
_lang = {}
_ev_keep = {}


def base_lang(D):
    if D not in _lang:
        _lang[D] = M.Lang2(GAME, 'exact', NMAX)
    return _lang[D]


def base_eval(D, keep=False):
    """the stored language and the program-level evaluation of the exact arm at depth D (about 12 s; the evaluation is recomputed on
    every call unless keep=True, so that a job holds one copy of it at most)."""
    if D not in _lang:
        _lang[D] = M.Lang2(GAME, 'exact', NMAX)
    lang = _lang[D]
    if D in _ev_keep:
        return lang, _ev_keep[D]
    ev = M.evaluate(lang, D)
    if keep:
        _ev_keep[D] = ev
    return lang, ev


def inspector_step(spec, child, appE, appM):
    """one level of the added inspector against every inspectee program: child (S1, 3) = the inspectee's value (P(C), P(K), P(forfeit))
    against the added inspector at the previous level (or a forfeit at level 0); appE, appM (S1) = cost and serial depth of the read
    (0 at level 0).  Returns value (S1, 3), expected cost E (S1), depth M (S1)."""
    op, k, susp = spec[0], spec[1], spec[2]
    T = M.game_tensors(GAME)[0]
    pc, pk, pf = child[:, 0], child[:, 1], child[:, 2]
    z = 1.0 - pf
    n = len(pc)
    out = np.zeros((n, 3))
    if op in ('cr', 'zt'):
        ok = z > 1e-15
        zz = np.where(ok, z, 1.0)
        if op == 'cr':
            u0 = (pc * T[0, 0, 0, 0, 0] + pk * T[0, 0, 0, 0, 1]) / zz
            u1 = (pc * T[0, 0, 1, 0, 0] + pk * T[0, 0, 1, 0, 1]) / zz
            tie = np.abs(u0 - u1) <= 1e-9
            b = np.where(tie, 0.5, np.where(u0 > u1, 1.0, 0.0))
        else:
            b = np.where(pk / zz > 1e-12, 1.0, 0.0)
        pI = np.where(ok, z * b, 0.0)
        pN = np.where(ok, z * (1.0 - b), 0.0)
        if susp:
            out[:, 0] = np.where(ok, pI + pf, 1.0); out[:, 1] = pN; out[:, 2] = 0.0
        else:
            out[:, 0] = pI; out[:, 1] = pN; out[:, 2] = np.where(ok, pf, 1.0)
        return out, appM.copy(), appM.copy()
    # sampling: k independent draws of the child, stop at the first cheating draw
    full = np.abs(1.0 - pc) < 1e-15
    geo = np.where(full, float(k), (1.0 - pc ** k) / np.where(full, 1.0, 1.0 - pc))
    PI = pk * geo
    PF = pf * geo
    PN = pc ** k
    if susp:
        out[:, 0] = PI + PF; out[:, 1] = PN
    else:
        out[:, 0] = PI; out[:, 1] = PN; out[:, 2] = PF
    return out, geo * appE, k * appM


def eval_added(lang, spec, D):
    """rows of one added inspector against all S1 inspectee programs at depth D: dict(G0 (S1,3), G1 (S1,3), E0, E1, F0, F1, U0, U1,
    prevG0, prevG1).  The inspectee side is the stored kernel with a single opponent."""
    T, FI0, FI1, FII0, FII1, FF = M.game_tensors(GAME)
    g = M.GAMES[GAME]
    wts = g['weights']
    S1 = lang.S1
    ta1, tl1 = lang.tape[1]
    G0p = np.zeros((1, S1, 3)); E0p = np.zeros((1, S1)); M0p = np.zeros((1, S1))     # the added inspector, previous level
    G1p = np.zeros((S1, 1, 3)); E1p = np.zeros((S1, 1)); M1p = np.zeros((S1, 1))
    prevG0 = prevG1 = None
    for d in range(0, D + 1):
        G1n = np.zeros((S1, 1, 3)); E1n = np.zeros((S1, 1)); M1n = np.zeros((S1, 1))
        M._eval_role(ta1, tl1, S1, 1, G0p, E0p, M0p, 3, d, G1n, E1n, M1n, 3, T, wts, 0)
        if d == 0:
            child = np.zeros((S1, 3)); child[:, 2] = 1.0
            appE = np.zeros(S1); appM = np.zeros(S1)
        else:
            child = np.ascontiguousarray(G1p[:, 0, :]); appE = 1.0 + E1p[:, 0]; appM = 1.0 + M1p[:, 0]
        v, e, m = inspector_step(spec, child, appE, appM)
        G0n = np.ascontiguousarray(v[None, :, :]); E0n = np.ascontiguousarray(e[None, :]); M0n = np.ascontiguousarray(m[None, :])
        if d == D - 1:
            prevG0 = G0n[0].copy(); prevG1 = G1n[:, 0, :].copy()
        G0p, E0p, M0p, G1p, E1p, M1p = G0n, E0n, M0n, G1n, E1n, M1n
    U0 = np.zeros((1, S1)); U1 = np.zeros((S1, 1)); F0 = np.zeros((1, S1)); F1 = np.zeros((S1, 1))
    M._payoffs(G0p, G1p, 3, wts, g['Pay0'], g['Pay1'], FI0, FI1, FII0, FII1, FF, U0, U1, F0, F1)
    return dict(G0=G0p[0], G1=G1p[:, 0, :], E0=E0p[0], E1=E1p[:, 0], F0=F0[0], F1=F1[:, 0], U0=U0[0], U1=U1[:, 0], prevG0=prevG0, prevG1=prevG1)


_rows = {}


def added_rows(name, D):
    key = (name, D)
    if key not in _rows:
        lang = base_lang(D)
        _rows[key] = eval_added(lang, ADDED[name], D)
    return _rows[key]


# ======================================================================================================== arms
class LangView:
    """the stored language with extra inspector programs appended after the S0 stored ones (node ids len(op) ... ); everything not
    overridden is delegated to the stored language."""

    def __init__(self, base, names, mu0):
        self._b = base
        n = len(names)
        S = len(base.op)
        self.size = np.concatenate([base.size, np.full(n, 4, np.int64)])
        ids = np.arange(S, S + n, dtype=np.int64)
        self.progs = [np.concatenate([base.progs[0], ids]), base.progs[1]]
        self.mu = [mu0, base.mu[1]]
        self.S0 = base.S0 + n
        self.S1 = base.S1
        self.n_added = n
        self.added_names = list(names)
        ex = [ADDED[a][0] in ('cr', 'zt') for a in names]
        sm = [ADDED[a][0] == 'sr' for a in names]
        t = np.ones(n, bool)
        self.has_app = [np.concatenate([base.has_app[0], t]), base.has_app[1]]
        self.has_cr = [np.concatenate([base.has_cr[0], np.array(ex, bool)]), base.has_cr[1]]
        self.has_if = [np.concatenate([base.has_if[0], np.zeros(n, bool)]), base.has_if[1]]
        self.has_sr = [np.concatenate([base.has_sr[0], np.array(sm, bool)]), base.has_sr[1]]
        self._extra = {S + j: ADDED[a][3] for j, a in enumerate(names)}

    def src(self, e):
        if e in self._extra:
            return self._extra[e]
        return self._b.src(e)

    def __getattr__(self, k):
        if k.startswith('__') or k == '_b':
            raise AttributeError(k)
        return getattr(self._b, k)


def assemble_ev(base_ev, rows):
    """the base program-level evaluation with the added inspectors' rows (role 0) and columns (role 1) appended."""
    n = len(rows)
    S0, S1 = base_ev['U0'].shape
    out = {}
    for k in ('U0', 'E0', 'F0', 'M0'):
        A = np.zeros((S0 + n, S1)); A[:S0] = base_ev[k]
        kk = {'U0': 'U0', 'E0': 'E0', 'F0': 'F0', 'M0': 'E0'}[k]
        for j, r in enumerate(rows):
            A[S0 + j] = r[kk]
        out[k] = A
    for k in ('U1', 'E1', 'F1', 'M1'):
        A = np.zeros((S1, S0 + n)); A[:, :S0] = base_ev[k]
        kk = {'U1': 'U1', 'E1': 'E1', 'F1': 'F1', 'M1': 'E1'}[k]
        for j, r in enumerate(rows):
            A[:, S0 + j] = r[kk]
        out[k] = A
    for k, kk in (('G0', 'G0'), ('prevG0', 'prevG0')):
        A = np.zeros((S0 + n, S1, 3)); A[:S0] = base_ev[k]
        for j, r in enumerate(rows):
            A[S0 + j] = r[kk]
        out[k] = A
    for k, kk in (('G1', 'G1'), ('prevG1', 'prevG1')):
        A = np.zeros((S1, S0 + n, 3)); A[:, :S0] = base_ev[k]
        for j, r in enumerate(rows):
            A[:, S0 + j] = r[kk]
        out[k] = A
    return out


_arms = {}


def get_arm_zt(tag, c):
    """class-level table of one arm (tag 'zt', 'ctl@D11', ...) at price c; the same total prior mass m is moved onto the arm's
    program (see the module docstring).  'exact' (the stored arm) is returned untouched."""
    if tag == 'exact':
        return M.get_arm(GAME, 'exact', NMAX, c)
    key = (tag, c)
    if key in _arms:
        return _arms[key]
    name, D = parse_arm(tag)
    spec = ARMS[name]
    lang, ev = base_eval(D, keep=True)
    A0 = _stored_like(D, c)                                  # the stored arm's classes at this depth and price
    nm0 = S.named(A0)
    m = float(A0.mass[0][nm0['0CRI']]) if spec['mass'] else 0.0
    mu0 = lang.mu[0] * (1.0 - m)
    info = dict(m=m, arm=name, D=D)
    if spec['boost'] is not None and m > 0:
        key0 = '0' + spec['boost']
        members = np.array(A0.members[0][nm0[key0]], np.int64)
        w = lang.mu[0][members]
        mu0[members] += m * w / w.sum()
        info['boost_class'] = A0.names[0][nm0[key0]]
    added = spec['added']
    if added:
        mu0 = np.concatenate([mu0, np.full(len(added), m / len(added))])
    view = LangView(lang, added, mu0) if added else _plain_view(lang, mu0)
    if added:
        rows = [added_rows(a, D) for a in added]
        ev_arm = assemble_ev(ev, rows)
    else:
        ev_arm = ev
    A = M.collapse(view, ev_arm, c)
    A.game, A.arm, A.n, A.D = GAME, tag, NMAX, D
    info['added'] = []
    for j, a in enumerate(added):
        p = lang.S0 + j
        cl = int(A.cls_of[0][p])
        info['added'].append(dict(name=a, src=ADDED[a][3], cls=cl, cls_rep=A.names[0][cl], n_members=len(A.members[0][cl]),
                                  cls_mass=float(A.mass[0][cl]), new_class=bool(len(A.members[0][cl]) == 1)))
    A.zt = info
    A.base_S0 = lang.S0
    del ev_arm
    if not os.environ.get('ZT_KEEP_EV'):
        _ev_keep.pop(D, None)
    _arms[key] = A
    return A


def _plain_view(lang, mu0):
    """the stored language with a replaced inspector prior and no added programs."""
    v = LangView(lang, [], mu0)
    return v


_stored = {}


def _stored_like(D, c):
    """the stored exact arm's class table at depth D (for D = 12 the cached stored table; otherwise rebuilt unchanged)."""
    if (D, c) in _stored:
        return _stored[(D, c)]
    if D == D0:
        A = M.get_arm(GAME, 'exact', NMAX, c)
    else:
        lang, ev = base_eval(D, keep=True)
        A = M.collapse(lang, ev, c)
        A.game, A.arm, A.n, A.D = GAME, 'exact', NMAX, D
    _stored[(D, c)] = A
    return A


# ======================================================================================================== sets, static summaries
def class_summary(A):
    """behavioural-class membership and aggregated prior mass of the added programs of an arm."""
    out = dict(K=A.K, info=A.zt)
    nm = S.named(A)
    out['named_mass'] = {k: float(A.mass[0 if k[0] == '0' else 1][v]) for k, v in nm.items()}
    return out


def resident_exits(A, N, a, b, fl):
    """one-state exit rates (per mutation event) out of the class pair (a, b), by the exit categories of the stationary decomposition
    (neutral shadow, neutral other, strict K, strict non-reading inspectee, strict reading inspectee, strict inspector, deleterious):
    the fixation probabilities and prior-weighted rates of every single mutant are aggregated by category."""
    m0, m1 = A.mass[0], A.mass[1]
    d0 = A.UA[:, b] - A.UA[a, b]; d1 = A.UB[:, a] - A.UB[b, a]
    r0 = np.exp(np.log(0.5 * m0) + M.lrho(d0, N, W)); r0[a] = 0.0
    r1 = np.exp(np.log(0.5 * m1) + M.lrho(d1, N, W)); r1[b] = 0.0
    cats = dict(A_neutral_shadow=0.0, B_neutral_other=0.0, C_strict_K=0.0, D_strict_nonreader=0.0, E_strict_reader=0.0, F_strict_inspector=0.0, G_deleterious=0.0)
    for q in range(len(r0)):
        if r0[q] == 0:
            continue
        if abs(d0[q]) <= TOL:
            cats['A_neutral_shadow' if not fl['deter0'][q] else 'B_neutral_other'] += r0[q]
        elif d0[q] > 0:
            cats['F_strict_inspector'] += r0[q]
        else:
            cats['G_deleterious'] += r0[q]
    for q in range(len(r1)):
        if r1[q] == 0:
            continue
        if abs(d1[q]) <= TOL:
            cats['B_neutral_other'] += r1[q]
        elif d1[q] > 0:
            if fl['isK1'][q]:
                cats['C_strict_K'] += r1[q]
            elif fl['reader1'][q]:
                cats['E_strict_reader'] += r1[q]
            else:
                cats['D_strict_nonreader'] += r1[q]
        else:
            cats['G_deleterious'] += r1[q]
    strict_in = [(float(r1[q]), A.names[1][q], float(d1[q])) for q in np.nonzero(d1 > TOL)[0] if r1[q] > 0]
    strict_in.sort(reverse=True)
    return dict(total=float(sum(cats.values())), cats={k: float(v) for k, v in cats.items()},
                top_strict_inspectee=[dict(cls=n, rate=r, du=du) for r, n, du in strict_in[:6]])


# ======================================================================================================== the whole-space chain
def _embed(pi_src, names_src, names_dst):
    """embed a (K0s, K1s) distribution of one arm into the class index space of another by representative names; mass of classes absent
    from the destination is dropped.  Returns (pi_dst, retained_mass)."""
    out = np.zeros((len(names_dst[0]), len(names_dst[1])))
    i0 = {n: i for i, n in enumerate(names_dst[0])}; i1 = {n: i for i, n in enumerate(names_dst[1])}
    r0 = [i0.get(n, -1) for n in names_src[0]]; r1 = [i1.get(n, -1) for n in names_src[1]]
    for a, ra in enumerate(r0):
        if ra < 0:
            continue
        for b, rb in enumerate(r1):
            if rb >= 0:
                out[ra, rb] = pi_src[a, b]
    return out, float(out.sum())


def pi_path(arm, c, N):
    return os.path.join(CACHE, 'pi_%s_c%g_N%d.npz' % (arm.replace('@', '_'), c, N))


def chain_cell_zt(arm, c, N, passage=True, verbose=True, dtype=np.float64, ref=None):
    """Whole-space chain for one cell of this module's arms; the structure of `inspection_shadow.chain_cell` plus: the added program's
    classes and masses, resident-specific exits, realized read costs and forfeit (timeout) frequencies, and the hazards from R and E
    under the *reference* arm's stationary weights (embedded by class names), when that arm's pi was saved."""
    t0 = time.time()
    A = get_arm_zt(arm, c)
    if ref is None:
        ref = 'ctl' if A.D == D0 else 'ctl@D%d' % A.D
    fl = S.class_flags(A)
    sets = S.pair_sets(A, fl)
    codes = S.occupancy_codes(A, fl)
    K0, K1 = A.K
    W_ = S.Whole(A, N)
    starts = S.start_states(A) if passage else []
    keep = sets['E'].copy()
    for _, a, b in starts:
        keep[a, b] = True
    lpi, snap = W_.solve(keep_mask=keep if passage else None, rew_fn=S.rewards_factory(codes, fl) if passage else None, dtype=dtype)
    t_solve = time.time() - t0
    pi = np.exp(lpi).reshape(K0, K1)
    pi /= pi.sum()
    res = dict(arm=arm, c=c, N=N, K=[K0, K1], S=K0 * K1, solve_s=t_solve, dtype=np.dtype(dtype).name, vector='chain (eps -> 0, whole state space)',
               added=A.zt)
    u0, u1, p, q = fl['u0'], fl['u1'], fl['p'], fl['q']
    res['stat'] = dict(u0g=float((pi * u0).sum()), u1g=float((pi * u1).sum()), p_insp=float((pi * p).sum()), q_cheat=float((pi * q).sum()),
                       forfeit0=float((pi * fl['F0']).sum()), forfeit1=float((pi * fl['F1']).sum()))
    # realized read costs (levels per round, pi-weighted) and the timeout (forfeit) frequency; the cost mean can be dominated by nested sampling
    cost0 = (pi * A.CA).sum(); cost1 = (pi * A.CB.T).sum()
    flat = np.argsort((A.CA + A.CB.T).ravel())
    cw = np.cumsum(pi.ravel()[flat])
    med = float((A.CA + A.CB.T).ravel()[flat][np.searchsorted(cw, 0.5)])
    res['cost'] = dict(mean_inspector=float(cost0), mean_inspectee=float(cost1), median_total=med,
                       mean_in_E=float((pi * A.CA)[sets['E']].sum() / max(pi[sets['E']].sum(), 1e-300)))
    res['pi_sets'] = {k: float(pi[m].sum()) for k, m in sets.items()}
    res['pi_E_not_R'] = float(pi[sets['E'] & ~sets['R']].sum())
    pe = res['pi_sets']['E']
    res['odds_E'] = pe / max(1.0 - pe, 1e-300)
    res['occupancy'] = {S.OCC_ORDER[k]: float(pi[codes == k].sum()) for k in range(len(S.OCC_ORDER))}
    res['occupancy']['E'] = pe
    sh0 = pi.sum(1); sh1 = pi.sum(0)
    res['top_states'] = []
    for s in np.argsort(-pi.ravel())[:12]:
        a, b = divmod(int(s), K1)
        res['top_states'].append(dict(pi=float(pi[a, b]), insp=A.names[0][a], ee=A.names[1][b], u0g=float(u0[a, b]), u1g=float(u1[a, b]),
                                      in_E=bool(sets['E'][a, b]), in_R=bool(sets['R'][a, b])))
    cs = np.cumsum(np.sort(pi.ravel())[::-1])
    res['n_states_for_099'] = int(np.searchsorted(cs, 0.99) + 1)
    res['top_insp'] = [(A.names[0][i], float(sh0[i])) for i in np.argsort(-sh0)[:8]]
    res['top_ee'] = [(A.names[1][i], float(sh1[i])) for i in np.argsort(-sh1)[:8]]
    nm = S.named(A)
    res['named_share'] = {k: float(sh0[v] if k[0] == '0' else sh1[v]) for k, v in nm.items()}
    res['added_share'] = [float(sh0[a['cls']]) for a in A.zt['added']]
    res['added_share_in_R'] = [float(pi[a['cls']][sets['R'][a['cls']]].sum()) for a in A.zt['added']]
    res['reader_share'] = [float(sh0[fl['reader0']].sum()), float(sh1[fl['reader1']].sum())]
    ex, bal = S.decompose(A, N, pi, sets, fl)
    res['exits'] = ex
    res['balance'] = bal
    for X in ('E', 'R'):
        fX, px = ex[X]['flux'], ex[X]['pi']
        res['renewal_' + X] = dict(mean_sojourn=px / fX if fX > 0 else None, mean_time_outside=(1 - px) / fX if fX > 0 else None, flux_out=fX)
    if passage and snap is not None:
        res['first_passage'] = S.passage_stats(A, snap, sets, fl, starts, K1)
    # resident-specific exits
    refs = {}
    pairs = [('(CRI,C)', nm.get('0CRI'), nm.get('1C')), ('(N,C)', nm.get('0N'), nm.get('1C')), ('(N,K)', nm.get('0N'), nm.get('1K')), ('(I,C)', nm.get('0I'), nm.get('1C'))]
    for j, a in enumerate(A.zt['added']):
        pairs.append(('(%s,C)' % a['name'], a['cls'], nm.get('1C')))
    for lab, a, b in pairs:
        if a is not None and b is not None:
            refs[lab] = resident_exits(A, N, a, b, fl)
            refs[lab]['pair'] = [A.names[0][a], A.names[1][b]]
            refs[lab]['payoffs'] = [float(A.UA[a, b]), float(A.UB[b, a])]
            refs[lab]['cost'] = [float(A.CA[a, b]), float(A.CB[b, a])]
            refs[lab]['in_R'] = bool(sets['R'][a, b])
    res['resident_exits'] = refs
    # hazards under the reference arm's stationary weights
    pp = pi_path(ref, c, N) if ref else None
    if arm != ref and pp and os.path.exists(pp):
        z = np.load(pp, allow_pickle=True)
        pe_, kept = _embed(z['pi'], [list(z['names0']), list(z['names1'])], A.names)
        if kept > 0:
            fx, _ = S.decompose(A, N, pe_ / kept, sets, fl)
            res['fixed_weight'] = dict(ref=ref, retained_mass=kept, R={k: v['hazard'] for k, v in fx['R']['cats'].items()}, R_total=fx['R']['hazard'],
                                       E={k: v['hazard'] for k, v in fx['E']['cats'].items()}, E_total=fx['E']['hazard'], pi_R=fx['R']['pi'], pi_E=fx['E']['pi'])
    if arm == ref:
        os.makedirs(CACHE, exist_ok=True)
        np.savez(pi_path(arm, c, N), pi=pi, names0=np.array(A.names[0], dtype=object), names1=np.array(A.names[1], dtype=object))
    res['time_s'] = time.time() - t0
    if verbose:
        print('  [%s c=%g N=%d] S=%d solve %.0fs total %.0fs  u0g=%.4f u1g=%.4f pi(E)=%.4f pi(R)=%.4f  bal=%.1e' % (
            arm, c, N, K0 * K1, t_solve, res['time_s'], res['stat']['u0g'], res['stat']['u1g'], pe, res['pi_sets']['R'], bal['max_rel_residual']), flush=True)
    return res


# ======================================================================================================== the lottery with coupled founders
def slot_programs(lang, r, I, N, seed):
    """program index of every founder slot (the construction of `mixed2.draw_founders`, returning programs instead of class counts)."""
    rng = np.random.default_rng(seed)
    u1 = rng.random(I * N); u2 = rng.random(I * N)
    ps = M.length_prior_sizes(lang, r)
    cdf = np.cumsum(ps)
    sz = np.minimum(np.searchsorted(cdf, u1, side='right'), len(ps) - 1)
    sz = np.where(ps[sz] > 0, sz, np.nonzero(ps)[0][0])
    prog = np.empty(I * N, np.int64)
    ids = lang.progs[r]
    for s in range(1, len(ps)):
        sel = np.nonzero(sz == s)[0]
        if len(sel) == 0:
            continue
        lst = np.nonzero(lang.size[ids] == s)[0]
        cm = np.cumsum(lang.mult[ids[lst]]); cm = cm / cm[-1]
        prog[sel] = lst[np.minimum(np.searchsorted(cm, u2[sel], side='right'), len(lst) - 1)]
    return prog


def replacement_class(A):
    """class index that the replaced founder slots receive in this arm (None if the arm moves no mass)."""
    spec = ARMS[parse_arm(A.arm)[0]]
    if not spec['mass']:
        return None
    if spec['added']:
        return A.zt['added'][0]['cls']
    nm = S.named(A)
    return nm['0' + spec['boost']]


def founders_coupled(A, lang0, I, N, seed0, seed1):
    """inspector founders: the stored size-and-quantile draw with each slot replaced, with probability m and independently of the program
    drawn, by the arm's program; inspectee founders: the stored draw.  Returns (init0 (I, K0), init1 (I, K1), n_replaced)."""
    K0, K1 = A.K
    prog = slot_programs(lang0, 0, I, N, seed0)
    cl = A.cls_of[0][prog].copy()
    m = A.zt['m']
    rc = replacement_class(A)
    nrep = 0
    if rc is not None and m > 0:
        rep = np.random.default_rng([seed0, 7]).random(I * N) < m
        cl[rep] = rc
        nrep = int(rep.sum())
    cl = cl.reshape(I, N)
    init0 = np.zeros((I, K0), np.int64)
    for i in range(I):
        init0[i] = np.bincount(cl[i], minlength=K0)
    init1 = M.draw_founders(lang0, 1, A.cls_of[1], K1, I, N, seed1)
    return init0, init1, nrep


STORE_EXTRA = ('sh_add', 'unres', 'p_deter')


def run_lottery_zt(arm, c, N, I, runs, T, mN=1.0, found='primary', verbose=True, run_ids=None):
    """eps = 0 seed lottery for one arm (the structure of `inspection_shadow.run_lottery`, coupled founders; dynamics seeds are the
    stored cell's, shared by all arms)."""
    A = get_arm_zt(arm, c)
    fl = S.class_flags(A)
    lang0 = base_lang(A.D)
    K0, K1 = A.K
    cps = S.checkpoints(N, T)
    res = []
    t0 = time.time()
    addc = [a['cls'] for a in A.zt['added']]
    rc = replacement_class(A)
    for r in (run_ids if run_ids is not None else range(runs)):
        f0, f1, nrep = founders_coupled(A, lang0, I, N, M.run_seed('found|%s|%d|0' % (found, r), 0), M.run_seed('found|%s|%d|1' % (found, r), 0))
        i0 = np.nonzero(f0.sum(0) > 0)[0]
        i1 = np.nonzero(f1.sum(0) > 0)[0]
        UA = np.ascontiguousarray(A.UA[np.ix_(i0, i1)]); UB = np.ascontiguousarray(A.UB[np.ix_(i1, i0)])
        z = np.zeros(0, np.int64)
        o0, o1 = S.lottery3(UA, UB, np.ascontiguousarray(f0[:, i0]), np.ascontiguousarray(f1[:, i1]), N, W, mN / N,
                            M.run_seed('dyn|insp|exact|%s|%d' % (found, r), 0), np.array(cps, np.int64), 0.0, 1, -1, z, z, z, z)
        rec = dict(run=r, cps=cps, stats={}, phases=[], n_replaced=nrep)
        for ci, g in enumerate(cps):
            X0 = np.zeros((I, K0)); X1 = np.zeros((I, K1))
            X0[:, i0] = o0[ci] / N; X1[:, i1] = o1[ci] / N
            summ, ph = S.island_summary(A, X0, X1, dict(S=None), fl, None)
            st = S.compact(summ)
            st['sh_add'] = round(float(X0[:, addc].sum(1).mean()) if addc else (float(X0[:, rc].mean()) if rc is not None else 0.0), 5)
            st['unres'] = round(float(np.mean((X0.max(1) < 0.9) | (X1.max(1) < 0.9))), 5)
            rec['stats'][str(g)] = st
            rec['phases'].append(ph)
            if g == T:
                sh0 = X0.mean(0); sh1 = X1.mean(0)
                rec['top_end'] = dict(r0=[(A.names[0][k], round(float(sh0[k]), 4)) for k in np.argsort(-sh0)[:8] if sh0[k] > 0.005],
                                      r1=[(A.names[1][k], round(float(sh1[k]), 4)) for k in np.argsort(-sh1)[:8] if sh1[k] > 0.005])
        res.append(rec)
        if verbose:
            s = rec['stats'][str(T)]
            print('  run %d (%.0fs): eff=%.3f u0g=%.3f u1g=%.3f p=%.3f q=%.3f repl=%d' % (r, time.time() - t0, s.get('isl_efficient', -1), s.get('u0g', -1), s.get('u1g', -1),
                                                                                       s.get('p_insp') or -1, s.get('q_cheat') or -1, nrep), flush=True)
    return res
