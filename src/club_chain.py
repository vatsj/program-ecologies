"""The eps->0 chain for specs/2026-10-04-club.md (measure 4) and its controls (measure 5).

Arms: 'club' (the club language at a solved fixed point K), 'free' (modal.build), 'clique' (modal.build_priced with
m = 1 clique spelling at FairBot's mass, c = 0).  PD, w = 0.3, eager_poly=False, theta = 1e-6.

Per cell: P(C,C), pi(K), support, terminal classes, exits from the top K state (strict / neutral / deleterious, inside
and outside K), exits from K as a set, entry rho(club-FairBot | all-D) against rho(FairBot | all-D), hitting time
from all-D into K, the rival share (cert_limN.networks).  Rates are computed in the log domain (closed-form
quadratic exponent, windowed log-sum-exp); a log-domain monomorphic embedded chain (GTH elimination with logaddexp)
gives pi where the linear chain underflows.  Residuals: ||pi P - pi||_1 for the linear chain, the same for the GTH
solution, and the max error of the closed-form log rho against ergodic_islands.log_fixation.

    python3 src/club_chain.py [--workers 3] [--smoke]       # writes runs/club_chain.json
"""
import argparse, json, os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from abm import njit
import modal as M
import club as CL
from chain import Chain
from priced_limN import hitting_time
from cert_limN import networks

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = 0.3
FB = 'BOX(THEM(ME))'
CFB = 'and(BOX(THEM(ME)),CLUB(THEM))'
CT = 'CLUB(THEM)'
KMAX = {}          # (n, mode) -> list of canon names of the fixed point the chain uses (filled by main)


@njit(cache=True)
def log_rho_fast(uqq, uqa, uaq, uaa, N, w):
    """log of the Moran fixation probability (kstar = N) of chain.fixation.  The exponent
    acc_k = w * sum_{j<=k} (pa_j - pq_j) is exactly quadratic in k; the sum of exp(acc_k) is taken over the
    window where acc_k > max - 46 (terms below e^-46 relative are dropped)."""
    c0 = ((N - 1) * uaa - N * uqa + uqq) / (N - 1)
    c1 = (uaq - uaa - uqq + uqa) / (N - 1)
    a = w * (c0 + 0.5 * c1); b = w * 0.5 * c1        # acc_k = a k + b k^2
    K = N - 1
    # candidate maxima over k in [1, K] (and 0 for the leading 1, acc_0 = 0)
    best = 0.0
    cands = np.array([1.0, float(K), 1.0])
    if b < 0:
        v = -a / (2 * b)
        if v < 1: v = 1.0
        if v > K: v = float(K)
        cands[2] = np.floor(v)
    for kk in cands:
        val = a * kk + b * kk * kk
        if val > best: best = val
    thr = best - 46.0
    s = np.exp(-best)                                   # the leading 1 (k = 0)
    # windows: scan outward from each candidate, mark visited ranges to avoid double counting
    lo_done = K + 1; hi_done = 0                        # union of scanned [lo, hi] (contiguous per scan)
    starts = np.array([1, K, int(cands[2])])
    seen_lo = np.full(3, K + 1); seen_hi = np.full(3, 0)
    for si in range(3):
        k0 = starts[si]
        dup = False
        for sj in range(si):
            if seen_lo[sj] <= k0 <= seen_hi[sj]:
                dup = True
        if dup:
            continue
        val0 = a * k0 + b * k0 * k0
        if val0 < thr:
            continue
        lo = k0
        while lo > 1 and a * (lo - 1) + b * (lo - 1) * (lo - 1) >= thr:
            inside = False
            for sj in range(si):
                if seen_lo[sj] <= lo - 1 <= seen_hi[sj]:
                    inside = True
            if inside: break
            lo -= 1
        hi = k0
        while hi < K and a * (hi + 1) + b * (hi + 1) * (hi + 1) >= thr:
            inside = False
            for sj in range(si):
                if seen_lo[sj] <= hi + 1 <= seen_hi[sj]:
                    inside = True
            if inside: break
            hi += 1
        seen_lo[si] = lo; seen_hi[si] = hi
        for k in range(lo, hi + 1):
            s += np.exp(a * k + b * k * k - best)
    return -(best + np.log(s))


@njit(cache=True)
def log_rate_matrix(U, logmu, N, w):
    """LT[a, b] = log mu(b) + log rho(b | all-a) for a != b; -inf on the diagonal."""
    K = U.shape[0]
    LT = np.full((K, K), -np.inf)
    for a in range(K):
        for b in range(K):
            if a != b:
                LT[a, b] = logmu[b] + log_rho_fast(U[b, b], U[b, a], U[a, b], U[a, a], N, w)
    return LT


def gth_log(LT):
    """Stationary distribution of the embedded chain with off-diagonal log rates LT (rows need not be normalized:
    the stationary vector of the jump chain with rates is pi_i ~ nu_i / q_i, and GTH on the rate matrix gives
    the stationary vector of the continuous-time chain; here the discrete chain P = rates / row-max with a
    self-loop has the same stationary vector as the CTMC with these rates).  Returns log pi (normalized)."""
    L = LT.copy(); K = L.shape[0]
    np.fill_diagonal(L, -np.inf)
    for k in range(K - 1, 0, -1):
        lS = np.logaddexp.reduce(L[k, :k])
        if not np.isfinite(lS):
            lS = -1e300
        # L[i, j] += L[i, k] * L[k, j] / S for i, j < k
        L[:k, k] = L[:k, k] - lS          # column scaled by 1/S (used again in back substitution)
        add = L[:k, k][:, None] + L[k, :k][None, :]
        L[:k, :k] = np.logaddexp(L[:k, :k], add)
    lp = np.full(K, -np.inf); lp[0] = 0.0
    for k in range(1, K):
        lp[k] = np.logaddexp.reduce(lp[:k] + L[:k, k])
    lp -= np.logaddexp.reduce(lp)
    return lp


def gth_residual(LT, lp):
    """Relative residual of the balance equations sum_i pi_i q_ij = pi_j q_j (log domain), max over j."""
    L = LT.copy(); np.fill_diagonal(L, -np.inf)
    inflow = np.logaddexp.reduce(lp[:, None] + L, axis=0)
    outflow = lp + np.logaddexp.reduce(L, axis=1)
    ok = np.isfinite(outflow) & (lp > lp.max() - 600)
    return float(np.abs(np.expm1(inflow[ok] - outflow[ok])).max())


def lse(xs):
    xs = [x for x in xs if np.isfinite(x)]
    return float(np.logaddexp.reduce(xs)) if xs else float('-inf')


def exit_kind(U, q, a):
    uaa = U[a, a]
    if U[q, a] > uaa + 1e-9: return 'strict'          # faker / strict first-order invader
    if max(abs(U[q, a] - uaa), abs(U[a, q] - uaa), abs(U[q, q] - uaa)) < 1e-9: return 'neutral'
    if abs(U[q, a] - uaa) < 1e-9 and U[q, q] >= U[a, q] - 1e-9: return 'weak'      # neutral at first order, favoured or equal later
    return 'deleterious'


def build(arm, n, mode='full'):
    if arm == 'club':
        c = CL.Club(n, mode=mode)
        K = c.mask([c.names.index(s) for s in KMAX[(n, mode)]])
        F, _ = c.F(K); assert (F == K).all(), 'not a fixed point'
        prov, val = c.provider(K)
        inK = prov.inK
    elif arm == 'free':
        L, val, worlds, prov = M.build(n)
        inK = np.zeros(len(prov.names), bool)
    elif arm == 'clique':
        L, val, worlds, prov = M.build_priced(n, 0.0, m_cliques=1)
        inK = np.array([s.startswith('CLIQUE') for s in prov.names])
    return prov, inK


def cell(job):
    arm, n, N, mode = job
    t = time.time()
    prov, inK = build(arm, n, mode)
    names = prov.names; U = prov.Ufull; P = prov.PCC
    mu = np.array([c[2] for c in prov.classes]); logmu = np.log(mu)
    lang = M.ClassLang(prov)
    ch = Chain(prov, N=N, w=W, verbose=False, eager_poly=False).explore()
    get = lambda s: names.index(s) if s in names else None
    iD, iC, iFB, iCFB, iCT = (get(s) for s in ('D', 'C', FB, CFB, CT))
    pcc = 0.0; poly = 0.0; pis = {}; key_of = {}; piK = 0.0; Kkeys = []
    for key, wgt in zip(ch.keys_list, ch.pi):
        ids, x, kind = ch.states[key]; ids = list(ids); x = np.asarray(x)
        pcc += wgt * float(x @ P[np.ix_(ids, ids)] @ x)
        allK = bool(inK[ids].all())
        if allK: piK += wgt; Kkeys.append(key)
        if kind == 'poly': poly += wgt
        else: pis[ids[0]] = pis.get(ids[0], 0.0) + wgt; key_of[ids[0]] = key
    # linear-chain residual
    piv = np.asarray(ch.pi)
    res_lin = float(np.abs(piv @ ch.Pmat - piv).sum())
    out = dict(arm=arm, n=n, N=N, mode=mode, n_classes=len(names), n_K=int(inK.sum()), mu_K=float(mu[inK].sum()),
               pcc=pcc, pi_K=piK, poly=poly, pi_D=pis.get(iD, 0.0), pi_C=pis.get(iC, 0.0), pi_FB=pis.get(iFB, 0.0),
               pi_CFB=pis.get(iCFB, 0.0) if iCFB is not None else None, pi_CT=pis.get(iCT, 0.0) if iCT is not None else None,
               cut_flow=ch.cut_flow, indeterminate=len(ch.indeterminate), n_terminal=len(ch.terminal),
               near_closed=int(getattr(ch, 'near_closed', 0)), absorb_error=float(getattr(ch, 'absorb_error', 0.0)),
               n_states=len(ch.trans), residual_linear=res_lin,
               support=[(ch.describe_state(k, lang), float(p)) for k, p in ch.support(1e-4)][:10])
    # K-state structure in the chain: terminal classes that are all-K
    out['K_states_expanded'] = len(Kkeys)
    # top K state
    monoK = [(v, q) for q, v in pis.items() if inK[q]]
    if inK.any():
        if monoK:
            v, qtop = max(monoK)
        else:
            qtop = int(np.nonzero(inK)[0][np.argmax(mu[inK])]); v = 0.0
        out.update(top_K=names[qtop], pi_top_K=v)
        kt = ch.mono(qtop); ch.expand(kt)
        ex = {}; dest = {}
        for b, vv in ch.trans.get(kt, {}).items():
            if b == kt: continue
            for q, mw in ch.trans_mut[(kt, b)].items():
                lab = exit_kind(U, q, qtop) + ('_in' if inK[q] else '_out')
                ex[lab] = ex.get(lab, 0.0) + mw; dest[(names[q], lab)] = dest.get((names[q], lab), 0.0) + mw
        out['top_exits_linear'] = ex
        out['top_dest_linear'] = [(s, l, w_) for (s, l), w_ in sorted(dest.items(), key=lambda kv: -kv[1])[:6]]
        # log domain, single-mutant fixation (kstar = N) out of the top state
        lr = {}; ldest = {}
        for q in range(len(names)):
            if q == qtop: continue
            r = logmu[q] + log_rho_fast(U[q, q], U[q, qtop], U[qtop, q], U[qtop, qtop], N, W)
            lab = exit_kind(U, q, qtop) + ('_in' if inK[q] else '_out')
            lr.setdefault(lab, []).append(r); ldest[(names[q], lab)] = r
        out['top_exits_log'] = {k: lse(v) for k, v in lr.items()}
        out['top_dest_out_log'] = [(s, l, r) for (s, l), r in sorted(ldest.items(), key=lambda kv: -kv[1]) if l.endswith('_out')][:4]
        # exits from K as a set: every mono K state weighted by its chain pi within K (or mu if pi underflows)
        Kq = [int(q) for q in np.nonzero(inK)[0]]
        wq = np.array([pis.get(q, 0.0) for q in Kq]); wq = wq / wq.sum() if wq.sum() > 0 else mu[Kq] / mu[Kq].sum()
        terms = []; per_state = {}
        notK = [int(q) for q in np.nonzero(~inK)[0]]
        for a, wa in zip(Kq, wq):
            if wa <= 0: continue
            r = lse([logmu[q] + log_rho_fast(U[q, q], U[q, a], U[a, q], U[a, a], N, W) for q in notK])
            per_state[names[a]] = r
            terms.append(np.log(wa) + r)
        out['K_exit_log'] = lse(terms)
        out['K_exit_log_per_state'] = per_state
        # the cheapest way out of K
        a = qtop
        best = max(notK, key=lambda q: logmu[q] + log_rho_fast(U[q, q], U[q, a], U[a, q], U[a, a], N, W))
        out['K_exit_best'] = (names[best], float(log_rho_fast(U[best, best], U[best, a], U[a, best], U[a, a], N, W)), exit_kind(U, best, a))
        # hitting time from all-D into K
        out['hit_K'] = hitting_time(ch, key_of.get(iD, ch.mono(iD)), Kkeys) if Kkeys else float('nan')
        # entry
        ent = {}
        for s in (CFB, FB, CT):
            i = get(s)
            if i is None: continue
            ent[s] = dict(log_rho=float(log_rho_fast(U[i, i], U[i, iD], U[iD, i], U[iD, iD], N, W)),
                          matrix=[float(U[i, i]), float(U[i, iD]), float(U[iD, i]), float(U[iD, iD])])
        out['entry'] = ent
        Kent = [q for q in Kq if abs(U[q, iD] - U[iD, iD]) < 1e-12 and abs(U[iD, q] - U[iD, iD]) < 1e-12]
        out['K_entry_log_flux'] = lse([logmu[q] + log_rho_fast(U[q, q], U[q, iD], U[iD, q], U[iD, iD], N, W) for q in Kq])
        out['K_neutral_entrants_D'] = len(Kent)
    else:
        out['entry'] = {FB: dict(log_rho=float(log_rho_fast(U[iFB, iFB], U[iFB, iD], U[iD, iFB], U[iD, iD], N, W)))}
    # log-domain monomorphic embedded chain
    t2 = time.time()
    LT = log_rate_matrix(np.ascontiguousarray(U, dtype=np.float64), logmu, N, W)
    lp = gth_log(LT)
    pm = np.exp(lp)
    out['gth_pcc'] = float(sum(pm[q] for q in range(len(names)) if P[q, q] == 1))
    out['gth_pi_K'] = float(pm[inK].sum())
    out['gth_log_1m_pi_K'] = lse(lp[~inK].tolist()) if inK.any() else 0.0
    out['gth_pi_D'] = float(pm[iD]); out['gth_pi_FB'] = float(pm[iFB])
    out['gth_residual'] = gth_residual(LT, lp)
    out['gth_top'] = [(names[q], float(pm[q])) for q in np.argsort(-lp)[:6]]
    out['gth_time_s'] = time.time() - t2
    out.update(networks(ch, prov))
    out['blocks'] = out['blocks'][:4]
    out['time_s'] = time.time() - t
    return out


def check_log_rho():
    """Residual of the closed form against ergodic_islands.log_fixation on random payoffs."""
    from ergodic_islands import log_fixation
    rng = np.random.default_rng(1); err = 0.0
    vals = [-2.0, -1.0, 0.0, 1.0]
    for N in (100, 1000, 10000):
        for i in range(300):
            u = rng.choice(vals, 4)
            a = log_fixation(u[0], u[1], u[2], u[3], N, W, N); b = log_rho_fast(u[0], u[1], u[2], u[3], N, W)
            err = max(err, abs(a - b) / max(1.0, abs(a)))
    return err


def jobs(cells):
    J = []
    for arm in ('club', 'free', 'clique'):
        for n in (6, 8):
            for N in (100, 1000, 10000, 100000):
                J.append((arm, n, N, 'full'))
    return J


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--workers', type=int, default=3); ap.add_argument('--smoke', action='store_true')
    ap.add_argument('--kmax', default=os.path.join(ROOT, 'runs', 'club_maximal.json')); ap.add_argument('--out', default=os.path.join(ROOT, 'runs', 'club_chain.json'))
    a = ap.parse_args()
    for r in json.load(open(a.kmax)):
        KMAX[(r['n'], r['mode'])] = r['K_max_members']
    print('log rho closed form, max relative error vs ergodic_islands.log_fixation: %.2e' % check_log_rho(), flush=True)
    J = jobs(None)
    if a.smoke:
        J = [('club', 6, 100, 'full'), ('clique', 6, 100, 'full')]
    J.sort(key=lambda j: (-j[1], -j[2]))
    rows = []
    with Pool(a.workers, initializer=_init, initargs=(dict(KMAX),)) as pool:
        for r in pool.imap_unordered(cell, J):
            rows.append(r)
            print('%s n=%d N=%d: P(C,C) %.4f pi(K) %.6f [gth %.6f, log(1-piK) %.1f] top %s %.3f; K exit log %s; hit %.3g; terminal %d; res lin %.1e gth %.1e (%.0fs)' % (
                r['arm'], r['n'], r['N'], r['pcc'], r['pi_K'], r['gth_pi_K'], r['gth_log_1m_pi_K'], r.get('top_K'), r.get('pi_top_K', 0),
                '%.2f' % r['K_exit_log'] if 'K_exit_log' in r else '-', r.get('hit_K', float('nan')), r['n_terminal'],
                r['residual_linear'], r['gth_residual'], r['time_s']), flush=True)
            if not a.smoke:
                json.dump(rows, open(a.out, 'w'), indent=1, default=str)
    if a.smoke:
        print(json.dumps(rows, indent=1, default=str)[:6000])


def _init(k):
    KMAX.update(k)


if __name__ == '__main__':
    main()
