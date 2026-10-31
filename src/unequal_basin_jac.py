"""Support-aware Jacobian at an endpoint of the unequal-basin object (spec Question 4): three spectra kept apart.

  invariant : S3-symmetric perturbations (P J P on the support)
  transverse: symmetry-breaking perturbations (J (1 - P) on the support)
  full      : the support block without symmetry restriction (union of the two) plus the leak: the flux from the support
              into absent states (invasion by triples absent from the endpoint's support is a forcing, not an eigenvalue:
              the block structure is triangular, the absent states' own eigenvalues being minus their exit rates).
The eigenvectors' class-share projections identify the class-changing directions (a vector with nonzero sum of v over a
class changes that class's share).  Matrix-free ARPACK, dense for small supports."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import unequal_basin as UB


def support_idx(obj, x, thr=1e-9):
    S = x >= thr
    if obj.symmetric:
        S2 = S.copy()
        for pi in obj.perm_idx:
            S2 |= S[pi]
        S = S2
    return np.nonzero(S)[0]


class SupportOp:
    def __init__(self, obj, x, idx, mode):
        self.obj, self.x, self.idx, self.mode = obj, x, idx, mode
        self.q = obj.marg(x)
        self.n = len(idx)
        self.buf = np.zeros(obj.n)

    def mv(self, v):
        o = self.obj
        self.buf[:] = 0.0
        self.buf[self.idx] = v
        w = self.buf
        if self.mode == 'invariant':
            w = o.sym(w)
        elif self.mode == 'transverse':
            w = w - o.sym(w)
        r = UB.jvp(o, self.x, w, self.q, sym=False)
        if self.mode == 'invariant':
            r = o.sym(r)
        elif self.mode == 'transverse':
            r = r - o.sym(r)
        return r[self.idx]


def leading(obj, x, idx, mode, k=12, dense_max=2500):
    from scipy.sparse.linalg import LinearOperator, eigs
    op = SupportOp(obj, x, idx, mode)
    n = op.n
    cl = obj.cl[idx]
    if n <= dense_max:
        J = np.zeros((n, n))
        e = np.zeros(n)
        for j in range(n):
            e[j] = 1.0
            J[:, j] = op.mv(e)
            e[j] = 0.0
        ev, V = np.linalg.eig(J)
    else:
        lo = LinearOperator((n, n), matvec=op.mv, dtype=np.float64)
        ev, V = eigs(lo, k=min(k, n - 2), which='LR', tol=1e-8, maxiter=3000)
    o = np.argsort(-ev.real)
    rows = []
    for i in o[:k]:
        v = V[:, i]
        nv = np.abs(v).sum()
        proj = [float(abs(v[cl == c].sum()) / nv) for c in range(UB.NCLS)]
        rows.append(dict(re=float(ev[i].real), im=float(ev[i].imag), class_proj=proj))
    out = dict(leading=rows, dim=n, dense=bool(n <= dense_max))
    if n <= dense_max:
        nv = np.abs(V).sum(axis=0)
        P = np.array([np.abs(np.array([V[cl == c, j].sum() for c in range(UB.NCLS)])).max() / nv[j] for j in range(n)])
        chg = P > 1e-3
        out['n_neutral_abs_1e-9'] = int((np.abs(ev.real) < 1e-9).sum())
        out['n_positive_re_gt_1e-9'] = int((ev.real > 1e-9).sum())
        out['n_negative_re_lt_-1e-9'] = int((ev.real < -1e-9).sum())
        idx = np.nonzero(chg)[0]
        idx = idx[np.argsort(-ev.real[idx])][:8]
        out['class_changing'] = [dict(re=float(ev[i].real), im=float(ev[i].imag), proj=float(P[i])) for i in idx]
        out['n_class_changing'] = int(chg.sum())
    return out, n


def leak_rate(obj, x, idx):
    """flux per event out of the support into absent states (sum of F over the complement, positive part) and the exit rate of
    the support (sum over the support of x lam)."""
    F = UB.field(obj, x, sym=False)
    mask = np.ones(obj.n, bool)
    mask[idx] = False
    return float(F[mask][F[mask] > 0].sum()), float((x * UB.outflow(obj, x))[idx].sum())
