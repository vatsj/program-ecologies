"""Linear stability of the symmetric limit of the arm-T mean-field equation on the rotation-non-invariant sectors.

The group C3 acts on triples by R (a0, a1, a2) = (a2, a0, a1); at a rotation-symmetric x* the Jacobian J commutes
with R, so J splits into the invariant sector (R = 1) and the two non-invariant sectors (R = w, w-bar, w = exp(2 pi i / 3)),
which are conjugates and have the same spectrum up to conjugation.  Support-aware: J is computed (a) restricted to the
support S of x* (rows and columns of triples with x* >= thr, rotation-closed), by the exact directional derivative of the
quadratic field; the flux from S into absent triples is reported separately as a leak rate (an invasion rate, not a
perturbation), and (b) on the full 19,683-dimensional space by Arnoldi (matrix-free) in each sector.
"""
import os, sys
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import many_islands_t as M
import many_islands_t_ode as O

OMEGA = np.exp(2j * np.pi / 3.0)


def support(x, thr=1e-9):
    S = x >= thr
    S = S | S[np.argsort(O.ROT1)] | S[np.argsort(O.ROT2)]          # rotation-closed
    # (S | R S | R^2 S): membership of t in R S means R^-1 t in S, i.e. S[ROT1^-1 ...]; closure checked below
    idx = np.nonzero(S)[0]
    assert S[O.ROT1[idx]].all(), 'support not rotation-closed'
    return idx


def dense_jacobian(x, PF, idx):
    """J restricted to the triples idx (rows and columns): J[:, j] = dF/dx_j, evaluated by the exact directional
    derivative (F quadratic)."""
    m = len(idx)
    q = O._marg(x, O.NP)
    J = np.zeros((m, m))
    e = np.zeros_like(x)
    for jj, j in enumerate(idx):
        e[j] = 1.0
        col = O.jvp(x, e, PF, q, False)
        J[:, jj] = col[idx]
        e[j] = 0.0
    return J


def orbits(idx):
    """orbit representatives (smallest member) of the rotation action restricted to idx, with the 3 members; and the
    fixed triples."""
    inS = {int(t): k for k, t in enumerate(idx)}
    seen = set(); reps3 = []; fixed = []
    for t in idx:
        t = int(t)
        if t in seen:
            continue
        r1 = int(O.ROT1[t]); r2 = int(O.ROT1[r1])
        if r1 == t:
            fixed.append(t); seen.add(t)
        else:
            reps3.append((t, r1, r2)); seen.update((t, r1, r2))
    return reps3, fixed, inS


def sector_matrix(J, idx, reps3, inS, omega):
    """matrix of J on the sector R = omega (omega a cube root of unity, != 1) in the orbit basis
    f(o) = sum_k omega^-k e_{R^k rep(o)}; returns (J_omega, T) with T (m x m3) the basis vectors."""
    m = len(idx)
    m3 = len(reps3)
    T = np.zeros((m, m3), complex)
    for o, (a, b, c) in enumerate(reps3):
        T[inS[a], o] = 1.0
        T[inS[b], o] = omega ** (-1)
        T[inS[c], o] = omega ** (-2)
    JT = J @ T
    rows = np.array([inS[a] for (a, b, c) in reps3])
    return JT[rows, :], T


def invariant_matrix(J, idx, reps3, fixed, inS):
    """J on the invariant sector in the orbit-sum basis g(o) = sum_k e_{R^k rep(o)} (fixed triples: e_t)."""
    m = len(idx)
    cols = []; rows = []
    for (a, b, c) in reps3:
        g = np.zeros(m); g[[inS[a], inS[b], inS[c]]] = 1.0; cols.append(g); rows.append(inS[a])
    for t in fixed:
        g = np.zeros(m); g[inS[t]] = 1.0; cols.append(g); rows.append(inS[t])
    G = np.array(cols).T
    return (J @ G)[np.array(rows), :]


def spectrum_report(x, PF, tabs, thr=1e-9, k_top=8):
    """the support-restricted spectrum on the invariant and the non-invariant sector, the leading eigenvector's content,
    and the leak rate out of the support."""
    idx = support(x, thr)
    J = dense_jacobian(x, PF, idx)
    reps3, fixed, inS = orbits(idx)
    Jw, T = sector_matrix(J, idx, reps3, inS, OMEGA)
    ev, evec = np.linalg.eig(Jw)
    order = np.argsort(-ev.real)
    Ji = invariant_matrix(J, idx, reps3, fixed, inS)
    evi = np.linalg.eigvals(Ji)
    ordi = np.argsort(-evi.real)
    top = []
    cl = tabs.CL.ravel()[idx]
    pr = tabs.PAIR.ravel()[idx]
    for kk in order[:k_top]:
        v = T @ evec[:, kk]
        l1 = np.abs(v).sum()
        cls_l1 = [float(np.abs(v[cl == c]).sum() / l1) for c in range(M.NCLS)]
        pair_sum = [complex(v[pr == i].sum()) for i in range(3)]
        top.append(dict(lam_re=float(ev[kk].real), lam_im=float(ev[kk].imag), class_l1=cls_l1,
                        pair_sum_abs=[abs(p) / l1 for p in pair_sum],
                        pair_sum_phase=[float(np.angle(p)) for p in pair_sum]))
    # leak: flux from S to its complement per event
    F = O.F_of(x, PF, False)
    mask = np.zeros(x.size, bool); mask[idx] = True
    # inflow into absent triples = F on absent triples (their own mass is ~0)
    leak = float(F[~mask].sum())
    return dict(support=int(len(idx)), thr=thr, n_orbits3=len(reps3), n_fixed=len(fixed), mass_in_support=float(x[idx].sum()),
                leak_rate=leak, noninv_top=top, inv_top=[dict(lam_re=float(evi[k].real), lam_im=float(evi[k].imag)) for k in ordi[:k_top]],
                noninv_count_pos=int((ev.real > 1e-12).sum()), noninv_max=float(ev.real.max()),
                noninv_min=float(ev.real.min())), (idx, T, evec, order, ev)


def arnoldi_top(x, PF, k=4, omega=OMEGA, ncv=None, maxiter=800, tol=1e-5, seed=0):
    """leading eigenvalues (largest real part) of J on the sector R = omega of the full 19,683-dimensional space,
    matrix-free (the projection onto the sector is applied before and after the directional derivative)."""
    from scipy.sparse.linalg import LinearOperator, eigs
    n = x.size
    q = O._marg(x, O.NP)

    def proj(v):
        return (v + (omega ** -1) * O.rot_apply(v, 1) + (omega ** -2) * O.rot_apply(v, 2)) / 3.0

    def mv(v):
        v = proj(np.asarray(v, complex).ravel())
        re = O.jvp(x, np.ascontiguousarray(v.real), PF, q, False)
        im = O.jvp(x, np.ascontiguousarray(v.imag), PF, q, False)
        return proj(re + 1j * im)

    A = LinearOperator((n, n), matvec=mv, dtype=complex)
    rng = np.random.default_rng(seed)
    v0 = proj(rng.standard_normal(n) + 1j * rng.standard_normal(n))
    from scipy.sparse.linalg import ArpackNoConvergence
    try:
        ev = eigs(A, k=k, which='LR', ncv=ncv or max(2 * k + 40, 60), maxiter=maxiter, tol=tol, v0=v0, return_eigenvectors=False)
        conv = True
    except ArpackNoConvergence as e:
        ev = e.eigenvalues
        conv = False
    ev = np.asarray(ev)
    order = np.argsort(-ev.real)
    return ev[order], conv


def perturbation(x, idx, vec, eps):
    """x + eps * u with u a real direction on the support, scaled so that max_t |u_t| / x_t = 1 (a relative perturbation of
    size eps in the largest entry), mass-conserving by construction when vec has zero sum."""
    u = np.zeros_like(x)
    u[idx] = vec
    rel = np.abs(u[idx]) / np.maximum(x[idx], 1e-300)
    u = u / rel.max()
    return x + eps * u, u


def nonsym_norm(x):
    return float(np.abs(x - O.symmetrize(x)).sum())
