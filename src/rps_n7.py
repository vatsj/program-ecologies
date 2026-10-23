"""Blocked evaluation of the RPS payoff table for n = 7 (17,888 programs in the exact grammar), where the full
(S, S, 4) distribution table (10 GB per buffer) does not fit.

The recursion is closed on rows and columns of a program set Z that contains every program referenced by a lifted
argument (`THEM(^B)`, |B| <= n - 3) plus a block of programs: G_d(a in Z, b in P) reads G_{d-1}(b, a), G_{d-1}(b, b) and
G_{d-1}(b, B); G_d(b in P, a in Z) reads G_{d-1}(a, b), G_{d-1}(a, a) and G_{d-1}(a, B); G_d(b, b) reads G_{d-1}(b, b)
and G_{d-1}(b, B).  So per block we keep R[z, b] = G(Z[z], b), C[b, z] = G(b, Z[z]) and the diagonal.  The payoff rows of the
block's programs against all programs then give the behavioural classes (row hashes, antisymmetric so columns follow).
The class-level table (representatives only) is a second, small pass with P = Z = representatives + lifted arguments.

Equal to rps.evaluate on any n where both fit (tested at n = 6).
"""
import hashlib, os, sys, time
import numpy as np
from numba import njit
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rps as RP


@njit(cache=True, inline='always')
def _step(o, vals, t, c1, c2, appv, cap_uniform, br_mode, tie):
    """Evaluate one non-leaf-or-leaf node into vals[t] (apps use the resolved vector appv)."""
    if o == 0:
        vals[t, 0] = 1.0; vals[t, 1] = 0.0; vals[t, 2] = 0.0; vals[t, 3] = 0.0
    elif o == 1:
        vals[t, 0] = 0.0; vals[t, 1] = 1.0; vals[t, 2] = 0.0; vals[t, 3] = 0.0
    elif o == 2:
        vals[t, 0] = 0.0; vals[t, 1] = 0.0; vals[t, 2] = 1.0; vals[t, 3] = 0.0
    elif o == 3:
        vals[t, 0] = 1.0 / 3; vals[t, 1] = 1.0 / 3; vals[t, 2] = 1.0 / 3; vals[t, 3] = 0.0
    elif o == 4 or o == 5:
        vals[t, 0] = vals[c1, 2]; vals[t, 1] = vals[c1, 0]; vals[t, 2] = vals[c1, 1]; vals[t, 3] = vals[c1, 3]
    elif o == 7:
        for x in range(4):
            vals[t, x] = 0.5 * (vals[c1, x] + vals[c2, x])
    elif o == 6:
        pf = vals[c1, 3]
        if pf >= 1.0 - 1e-15:
            if br_mode == 1:
                vals[t, 0] = 1.0 / 3; vals[t, 1] = 1.0 / 3; vals[t, 2] = 1.0 / 3; vals[t, 3] = 0.0
            else:
                vals[t, 0] = 0.0; vals[t, 1] = 0.0; vals[t, 2] = 0.0; vals[t, 3] = 1.0
        else:
            z = 1.0 - pf
            dr = vals[c1, 0] / z; dp = vals[c1, 1] / z; ds = vals[c1, 2] / z
            u0 = ds - dp; u1 = dr - ds; u2 = dp - dr
            mx = max(u0, max(u1, u2))
            n0 = 1.0 if u0 >= mx - tie else 0.0
            n1 = 1.0 if u1 >= mx - tie else 0.0
            n2 = 1.0 if u2 >= mx - tie else 0.0
            nn = n0 + n1 + n2
            sc = 1.0 if br_mode == 1 else z
            vals[t, 0] = sc * n0 / nn; vals[t, 1] = sc * n1 / nn; vals[t, 2] = sc * n2 / nn
            vals[t, 3] = 0.0 if br_mode == 1 else pf
    else:
        for x in range(4):
            vals[t, x] = appv[x]


@njit(cache=True)
def _row_kernel(t_op, t_l, t_r, t_k, t_len, Z, posZ, Cprev, diagprev, Rout, d, cap_u, br, tie):
    """Rout[z, b] = G_d(Z[z], b) for every b in P."""
    S = t_op.shape[0]; T = t_op.shape[1]
    vals = np.empty((T, 4)); appv = np.empty(4)
    for zi in range(len(Z)):
        a = Z[zi]; L = t_len[a]
        for b in range(S):
            for t in range(L):
                o = t_op[a, t]
                if o == 8:
                    if d == 0:
                        if cap_u == 1:
                            appv[0] = 1.0 / 3; appv[1] = 1.0 / 3; appv[2] = 1.0 / 3; appv[3] = 0.0
                        else:
                            appv[0] = 0.0; appv[1] = 0.0; appv[2] = 0.0; appv[3] = 1.0
                    else:
                        k = t_k[a, t]
                        if k == 0:
                            for x in range(4): appv[x] = Cprev[b, zi, x]
                        elif k == 1:
                            for x in range(4): appv[x] = diagprev[b, x]
                        else:
                            zb = posZ[t_r[a, t]]
                            for x in range(4): appv[x] = Cprev[b, zb, x]
                _step(o, vals, t, t_l[a, t], t_r[a, t], appv, cap_u, br, tie)
            for x in range(4):
                Rout[zi, b, x] = vals[L - 1, x]


@njit(cache=True)
def _col_kernel(t_op, t_l, t_r, t_k, t_len, Z, Rprev, diagprev, Cout, d, cap_u, br, tie):
    """Cout[b, z] = G_d(b, Z[z]) for every b in P."""
    S = t_op.shape[0]; T = t_op.shape[1]
    vals = np.empty((T, 4)); appv = np.empty(4)
    for b in range(S):
        L = t_len[b]
        for zi in range(len(Z)):
            a = Z[zi]
            for t in range(L):
                o = t_op[b, t]
                if o == 8:
                    if d == 0:
                        if cap_u == 1:
                            appv[0] = 1.0 / 3; appv[1] = 1.0 / 3; appv[2] = 1.0 / 3; appv[3] = 0.0
                        else:
                            appv[0] = 0.0; appv[1] = 0.0; appv[2] = 0.0; appv[3] = 1.0
                    else:
                        k = t_k[b, t]
                        if k == 0:                      # arg = b (me): opponent a reads G(a, b)
                            for x in range(4): appv[x] = Rprev[zi, b, x]
                        elif k == 1:                    # arg = a (them): G(a, a)
                            for x in range(4): appv[x] = diagprev[a, x]
                        else:                           # arg = B: G(a, B)
                            for x in range(4): appv[x] = Rprev[zi, t_r[b, t], x]
                _step(o, vals, t, t_l[b, t], t_r[b, t], appv, cap_u, br, tie)
            for x in range(4):
                Cout[b, zi, x] = vals[L - 1, x]


@njit(cache=True)
def _diag_kernel(t_op, t_l, t_r, t_k, t_len, posZ, Cprev, diagprev, diagout, d, cap_u, br, tie):
    S = t_op.shape[0]; T = t_op.shape[1]
    vals = np.empty((T, 4)); appv = np.empty(4)
    for b in range(S):
        L = t_len[b]
        for t in range(L):
            o = t_op[b, t]
            if o == 8:
                if d == 0:
                    if cap_u == 1:
                        appv[0] = 1.0 / 3; appv[1] = 1.0 / 3; appv[2] = 1.0 / 3; appv[3] = 0.0
                    else:
                        appv[0] = 0.0; appv[1] = 0.0; appv[2] = 0.0; appv[3] = 1.0
                else:
                    k = t_k[b, t]
                    if k == 0 or k == 1:
                        for x in range(4): appv[x] = diagprev[b, x]
                    else:
                        zb = posZ[t_r[b, t]]
                        for x in range(4): appv[x] = Cprev[b, zb, x]
            _step(o, vals, t, t_l[b, t], t_r[b, t], appv, cap_u, br, tie)
        for x in range(4):
            diagout[b, x] = vals[L - 1, x]


@njit(cache=True)
def _rows_payoff(R, C, pay):
    nz, S = R.shape[0], R.shape[1]
    U = np.empty((nz, S))
    for z in range(nz):
        for b in range(S):
            s = 0.0
            for x in range(4):
                gx = R[z, b, x]
                if gx == 0.0:
                    continue
                for y in range(4):
                    s += gx * C[b, z, y] * pay[x, y]
            U[z, b] = s
    return U


def eval_block(lang, Z, D):
    """Return R (|Z|, S, 4), C (S, |Z|, 4) at depth D for the program set Z."""
    g = lang.g
    cap_u = 1 if g['cap'] == 'uniform' else 0
    br = 1 if g['cr'] == 'br' else 0
    S = lang.S
    Z = np.asarray(Z, np.int64)
    posZ = -np.ones(S, np.int64); posZ[Z] = np.arange(len(Z))
    R0 = np.zeros((len(Z), S, 4)); R1 = np.zeros_like(R0)
    C0 = np.zeros((S, len(Z), 4)); C1 = np.zeros_like(C0)
    d0 = np.zeros((S, 4)); d1 = np.zeros_like(d0)
    args = (lang.t_op, lang.t_l, lang.t_r, lang.t_k, lang.t_len)
    # depth 0
    _row_kernel(*args, Z, posZ, C0, d0, R1, 0, cap_u, br, RP.TIE)
    _col_kernel(*args, Z, R0, d0, C1, 0, cap_u, br, RP.TIE)
    _diag_kernel(*args, posZ, C0, d0, d1, 0, cap_u, br, RP.TIE)
    Rp, Cp, dp = R1, C1, d1
    Rn, Cn, dn = R0, C0, d0
    for d in range(1, D + 1):
        _row_kernel(*args, Z, posZ, Cp, dp, Rn, d, cap_u, br, RP.TIE)
        _col_kernel(*args, Z, Rp, dp, Cn, d, cap_u, br, RP.TIE)
        _diag_kernel(*args, posZ, Cp, dp, dn, d, cap_u, br, RP.TIE)
        Rp, Rn = Rn, Rp; Cp, Cn = Cn, Cp; dp, dn = dn, dp
    return Rp, Cp


def small_programs(lang):
    """programs that can appear as a lifted argument: size <= n - 3."""
    return np.nonzero(lang.size <= lang.n - 3)[0]


def build_arm_blocked(arm, n=7, D=12, block=300, mu_kind='bits', verbose=False, sig_dec=6):
    t0 = time.time()
    lang = RP.Lang(arm, n)
    S = lang.S
    small = small_programs(lang)
    hb = lambda v: hashlib.blake2b(np.ascontiguousarray(v).tobytes(), digest_size=16).digest()
    sig = [None] * S
    maxanti = 0.0
    for s0 in range(0, S, block):
        blk = np.arange(s0, min(S, s0 + block))
        Z = np.unique(np.concatenate([small, blk]))
        R, C = eval_block(lang, Z, D)
        U = _rows_payoff(R, C, RP.PAY)
        pos = {int(z): i for i, z in enumerate(Z)}
        for p in blk:
            row = np.round(U[pos[int(p)]], sig_dec) + 0.0
            sig[p] = hb(row)
        if verbose and (s0 // block) % 10 == 0:
            print('  block %d / %d (%.0fs)' % (s0 // block + 1, (S + block - 1) // block, time.time() - t0), flush=True)
        del R, C, U
    groups = {}
    for p in range(S):
        groups.setdefault(sig[p], []).append(p)
    mu = lang.mu if mu_kind == 'bits' else lang.mu_nodes
    classes = []
    for members in groups.values():
        rep = min(members, key=lambda p: (lang.size[p], p))
        classes.append((rep, members, float(mu[members].sum())))
    classes.sort(key=lambda c: (-c[2], c[0]))
    A = RP.Arm()
    A.arm, A.n, A.D, A.lang, A.mu_kind = arm, n, D, lang, mu_kind
    A.K = len(classes)
    A.rep = np.array([c[0] for c in classes], np.int64)
    A.members = [c[1] for c in classes]
    A.mass = np.array([c[2] for c in classes]); A.mass /= A.mass.sum()
    A.cls_of = np.empty(S, np.int64)
    for c, m in enumerate(A.members):
        A.cls_of[m] = c
    A.names = [lang.src(r) for r in A.rep]
    # class-level pass: P = Z = representatives + lifted arguments (closed set)
    Z = np.unique(np.concatenate([small, A.rep]))
    # the closed pass needs P = Z: restrict the language to Z by evaluating blocks against all programs, then slicing
    R, C = eval_block(lang, Z, D)
    pos = {int(z): i for i, z in enumerate(Z)}
    idx = np.array([pos[int(r)] for r in A.rep])
    Gcl = R[np.ix_(idx, A.rep)].copy()            # G(rep_i, rep_j)
    Gcl_t = C[np.ix_(A.rep, idx)].copy()          # G(rep_i, rep_j) from the column block (consistency)
    A.Gcl = Gcl
    A.antisym_err = 0.0
    A.consistency_err = float(np.abs(Gcl - Gcl_t).max())
    Uc = _rows_payoff(R[idx], C[:, idx], RP.PAY)[:, A.rep]
    A.U = np.round(Uc, 12)
    A.antisym_err = float(np.abs(A.U + A.U.T).max())
    A.diag_err = float(np.abs(np.diag(A.U)).max())
    A.Gcl_prev = None
    A.member_dist_dev = float('nan'); A.n_classes_dist_split = -1
    A.K_dec5 = -1
    A.G_full_forfeit_mass = float('nan')
    A.U_full = None
    A.sweep_U = {}
    A.build_time = time.time() - t0
    return A
