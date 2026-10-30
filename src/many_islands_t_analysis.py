"""Analyses of the arm-T kernel and laws: charges and timeouts by program class (question 5), per-event rates out of the
dominated classes into V* by migrant program family and the fair-to-fair rates kappa / alpha (question 6), exact class
kernel statistics.  Pure functions of (x, PF, tabs)."""
import os, sys
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from numba import njit
import many_islands_t as M
import many_islands_t_ode as O

NP = M.NP
FAMS = ['const', 'single', 'two', 'exploit']


def fam_index(tabs):
    return np.array([FAMS.index(f) for f in tabs.fam])


def founding_x(tabs, law):
    """the product law of independent slots: x_t = law[a0] law[a1] law[a2]."""
    return (law[:, None, None] * law[None, :, None] * law[None, None, :]).ravel()


def charge_stats(x, tabs):
    """failed reads and forfeits per play by the family of the root program, and the share of triples (encounters) with a
    failed read in some slot.  x: a law over triples."""
    fi = fam_index(tabs)
    out = {}
    nto = tabs.NTO.reshape(NP ** 3, 3).astype(float)
    fo = tabs.FO.reshape(NP ** 3, 3).astype(float)
    steps = tabs.ST.reshape(NP ** 3, 3).astype(float)
    tr = O._TR
    per = {}
    for k, f in enumerate(FAMS):
        num = 0.0; nf = 0.0; den = 0.0; st = 0.0; pto = 0.0
        for s in range(3):
            m = (fi[tr[:, s]] == k)
            w = x * m
            d = w.sum()
            den += d
            num += (w * nto[:, s]).sum()
            nf += (w * fo[:, s]).sum()
            st += (w * steps[:, s]).sum()
            pto += (w * (nto[:, s] > 0)).sum()
        per[f] = dict(mass=float(den / 3.0), failed_reads_per_play=float(num / den) if den > 0 else None,
                      forfeits_per_play=float(nf / den) if den > 0 else None,
                      share_plays_with_timeout=float(pto / den) if den > 0 else None,
                      steps_per_play=float(st / den) if den > 0 else None)
    anyto = float((x * ((nto > 0).any(axis=1))).sum())
    return dict(by_family=per, share_triples_with_timeout=anyto,
                mean_failed_reads_per_play=float((x[:, None] * nto).sum() / 3.0))


@njit(cache=True)
def _conv_rates(x, PF, CL, PAIR, FAM, thr, out_to_F, out_all, nfam):
    """for every recipient class c (0..4) and migrant family f: accumulate sum over recipient triples t in c, slots s and
    migrant programs y of  x_t (1/3) q_s(y) PF[s, t, y] * [new triple's class is F]  into out_to_F[c, f], and the same
    probability of fixing at all into out_all[c, f]; the caller divides by the class mass."""
    n = PF.shape[1]
    q = O._marg(x, n)
    for a0 in range(n):
        for a1 in range(n):
            for a2 in range(n):
                t = (a0 * n + a1) * n + a2
                z = x[t]
                if z < thr:
                    continue
                c = CL[t]
                for y in range(n):
                    if y != a0:
                        p = z * q[0, y] * PF[0, a0, a1, a2, y] / 3.0
                        tn = (y * n + a1) * n + a2
                        out_all[c, FAM[y]] += p
                        if CL[tn] == 0:
                            out_to_F[c, FAM[y]] += p
                    if y != a1:
                        p = z * q[1, y] * PF[1, a0, a1, a2, y] / 3.0
                        tn = (a0 * n + y) * n + a2
                        out_all[c, FAM[y]] += p
                        if CL[tn] == 0:
                            out_to_F[c, FAM[y]] += p
                    if y != a2:
                        p = z * q[2, y] * PF[2, a0, a1, a2, y] / 3.0
                        tn = (a0 * n + a1) * n + y
                        out_all[c, FAM[y]] += p
                        if CL[tn] == 0:
                            out_to_F[c, FAM[y]] += p


def conversion_rates(x, PF, tabs, thr=0.0):
    """per-event rate (per island of the recipient class) at which a recipient of class c becomes a fair-pair island, by
    the migrant's program family; plus the total rate of fixing any migrant."""
    CL = tabs.CL.ravel().astype(np.int64)
    PAIR = tabs.PAIR.ravel().astype(np.int64)
    FAM = fam_index(tabs).astype(np.int64)
    toF = np.zeros((M.NCLS, len(FAMS))); allr = np.zeros((M.NCLS, len(FAMS)))
    _conv_rates(x, PF, CL, PAIR, FAM, float(thr), toF, allr, len(FAMS))
    mass = np.bincount(CL, weights=x, minlength=M.NCLS)
    res = {}
    for c in range(M.NCLS):
        if mass[c] <= 0:
            res[M.CLS[c]] = None
            continue
        res[M.CLS[c]] = dict(mass=float(mass[c]), to_F_by_family={f: float(toF[c, k] / mass[c]) for k, f in enumerate(FAMS)},
                             to_F_total=float(toF[c].sum() / mass[c]),
                             any_fix_by_family={f: float(allr[c, k] / mass[c]) for k, f in enumerate(FAMS)},
                             any_fix_total=float(allr[c].sum() / mass[c]))
    return res


@njit(cache=True)
def _ka(xr, ir, xd, idr, PF, PAIR, thr, out):
    """out[a, b, c] += (1/3) sum_s PF[s, r, d_s] over recipients r (fair pair a) and donors d (fair pair b) weighted
    x_r x_d, for the new triple's pair c (c = 3: not a fair pair); plus out[a, b, 4] = total weight x_r x_d."""
    n = PF.shape[1]
    for i in range(ir.shape[0]):
        r = ir[i]
        zr = xr[i]
        a0 = r // (n * n); a1 = (r // n) % n; a2 = r % n
        pa = PAIR[r]
        for j in range(idr.shape[0]):
            d = idr[j]
            zd = xd[j]
            pb = PAIR[d]
            w = zr * zd
            out[pa, pb, 4] += w
            d0 = d // (n * n); d1 = (d // n) % n; d2 = d % n
            if d0 != a0:
                pf = PF[0, a0, a1, a2, d0]
                tn = d0 * n * n + a1 * n + a2
                c = PAIR[tn]
                if c < 0:
                    c = 3
                out[pa, pb, c] += w * pf / 3.0
            if d1 != a1:
                pf = PF[1, a0, a1, a2, d1]
                tn = a0 * n * n + d1 * n + a2
                c = PAIR[tn]
                if c < 0:
                    c = 3
                out[pa, pb, c] += w * pf / 3.0
            if d2 != a2:
                pf = PF[2, a0, a1, a2, d2]
                tn = a0 * n * n + a1 * n + d2
                c = PAIR[tn]
                if c < 0:
                    c = 3
                out[pa, pb, c] += w * pf / 3.0


def kappa_alpha(x, PF, tabs, thr=1e-9):
    """fair-to-fair rates over (recipient pair a, donor pair b): K[a, b, c] = probability per event that a recipient in pair
    a hit by a donor in pair b ends in pair c (c = 3: leaves V*); kappa(a, b) = K[a, b, b] (conformist: takes the donor's
    pair), alpha(a, b) = K[a, b, third pair] (the third pair); symmetry-averaged over the rotation orbit of (a, b).
    Pair indices follow V's order; the excluded slot of pair i is EXCL[V[i]]."""
    PAIR = tabs.PAIR.ravel().astype(np.int64)
    idx = np.nonzero((PAIR >= 0) & (x >= thr))[0].astype(np.int64)
    xr = x[idx].copy()
    out = np.zeros((3, 3, 5))
    _ka(xr, idx, xr, idx, PF, PAIR, float(thr), out)
    K = out[:, :, :4] / np.maximum(out[:, :, 4:5], 1e-300)
    exc = np.array([M.EXCL[M.MI.V[i]] for i in range(3)])
    # orbit-average: classify (a, b) by the cyclic offset (exc_b - exc_a) mod 3
    kap = {}; alp = {}; leave = {}
    for off in (0, 1, 2):
        ks = []; as_ = []; ls = []
        for a in range(3):
            for b in range(3):
                if (exc[b] - exc[a]) % 3 != off:
                    continue
                third = [c for c in range(3) if c not in (a, b)]
                ks.append(K[a, b, b])
                as_.append(K[a, b, third[0]] if third else 0.0)
                ls.append(K[a, b, 3])
        kap[off] = float(np.mean(ks)); alp[off] = float(np.mean(as_)); leave[off] = float(np.mean(ls))
    return dict(K=K.tolist(), kappa_by_offset=kap, alpha_by_offset=alp, leave_by_offset=leave,
                n_support=int(len(idx)))


def sum_flux_classes(x, PF, tabs):
    """exact class-to-class event rates under x: R[c, c'] = per event, per island of class c, the probability that the event
    moves it to class c' (rows sum to the exit rate; diagonal excluded)."""
    CL = tabs.CL.ravel().astype(np.int64)
    n = NP
    R = np.zeros((M.NCLS, M.NCLS))
    q = O._marg(x, n)
    tr = O._TR
    for s in range(3):
        for y in range(n):
            pf = PF[s, tr[:, 0], tr[:, 1], tr[:, 2], y]       # (NT,)
            new = tr.copy()
            new[:, s] = y
            tn = (new[:, 0] * n + new[:, 1]) * n + new[:, 2]
            p = x * q[s, y] * pf / 3.0
            np.add.at(R, (CL, CL[tn]), p)
    mass = np.bincount(CL, weights=x, minlength=M.NCLS)
    R = R / np.maximum(mass[:, None], 1e-300)
    np.fill_diagonal(R, 0.0)
    return R
