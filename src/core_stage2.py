"""Rediscovering the core, stage 2: certified threats, followers that read certificates, and the sucker supply
(spec specs/2026-10-21-core-stage2.md; notes notes/core-stage2.md; predictions predictions/2026-10-21-core-stage2.md).

Reuses src/core_auction.py by import (instances, seller, `outcome`, core predicates, statistics kernel `_stats`, `_payoff_of`, `_fit`,
`_tri`, sample times, the annealed schedule).  No existing file is edited.

Program indices (one common K = 81 per role; unused indices carry no prior mass and zero payoffs):
  every role      0..40            constants c
  P (role 0)      41 + (t - 1)     TX(t), t = 1..40: "if the winners' total T satisfies T + 1 <= t, bid T + 1, else bid t", with a
                                   certificate that states this policy and is checked against the source (`check_policy`)
  items (1, 2)    41 + (j - 1)     F(d/10), d = j = 1..9: reads the opposing P program (its certified threat t, or its constant c),
                                   R = t + 1 (c + 1), bids floor(d R / 10 + 1/2) = (d R + 5) // 10, raised to at least 1, capped at its value

Resolution: items first (they read P's source or certificate, never P's output), then TX (it reads the items' outputs).  There is no
cycle.  The reverse order evaluates TX first and asks each item for its output afresh (no cached values); the call graph is acyclic
because items read only TX's certificate.  Both orders are implemented twice, in pure python from the program sources (`py_resolve`)
and in numba (`resolve2`), and are compared on every triple (statics and tests).

The island dynamics (`sim2`) is the stage-1 fixed-role seed lottery (`core_auction.sim`) with the arrivals (rain, annealed tail) taken from a
precomputed schedule so that controls can share arrival times, islands, roles and uniform draws with the full rain, and with extra recording
(counts history, fixation times, first-tested generation of every P program, replacement counters, TX-versus-matched-constant payoffs).
"""
import os, sys, math, json
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from abm import njit
import core_auction as C

ROOT = C.ROOT
OUT = os.path.join(ROOT, 'runs', 'core_stage2')
NC = C.NC                    # 41 constants 0..40 in every role
K = 81                       # TX(1..40) occupy 41..80 in role P; followers occupy 41..49 in the item roles
TX0 = NC                     # index of TX(1)
F0 = NC                      # index of F(0.1)
NF = 9
DELTAS = tuple(round(0.1 * (j + 1), 1) for j in range(NF))
TMAX = 80                    # the largest possible winners' total (two bids on 0..40)

# extra statistic channels of the tensor X (the first nine are core_auction's; XPRUWIN here is P(TX wins))
XPW, XAW, XBW = 9, 10, 11
NX2 = 12
NS2 = 6                      # pwin, P threat (count-weighted mean), mean winners' total T, mean bP, TX-minus-matched-constant payoff, spare
S2_PWIN, S2_THREAT, S2_T, S2_BP, S2_DTX = 0, 1, 2, 3, 4


# ================================================================== policy checker (pure python, the ground truth)
# A program source is a nested tuple: ('int', n), ('T',) the winners' total (the sum of the item roles' bids, read from the items' outputs),
# ('add', e, e), ('le', e, e), ('if', cond, e, e).
def tx_source(t):
    return ('if', ('le', ('add', ('T',), ('int', 1)), ('int', t)), ('add', ('T',), ('int', 1)), ('int', t))


def eval_src(src, T):
    op = src[0]
    if op == 'int':
        return src[1]
    if op == 'T':
        return T
    if op == 'add':
        return eval_src(src[1], T) + eval_src(src[2], T)
    if op == 'le':
        return 1 if eval_src(src[1], T) <= eval_src(src[2], T) else 0
    if op == 'if':
        return eval_src(src[2], T) if eval_src(src[1], T) else eval_src(src[3], T)
    raise ValueError(op)


def policy_bid(t, T):
    """the stated policy of a certified threat t: bid T + 1 if T + 1 <= t, else t."""
    return T + 1 if T + 1 <= t else t


def check_policy(src, claim):
    """the certificate checker: the claim ('policy', t) is admitted iff the source computes, for every possible winners' total T in 0..TMAX, exactly the
    stated policy bid.  The source is a function of T alone, so the finite check over its whole domain is complete.  Returns the certified threat t, or
    None (a false claim is not admitted)."""
    if not (isinstance(claim, tuple) and len(claim) == 2 and claim[0] == 'policy'):
        return None
    t = claim[1]
    for T in range(TMAX + 1):
        if eval_src(src, T) != policy_bid(t, T):
            return None
    return t


_CERT = {}


def certified_threat_of_tx(t):
    """what a follower reads off TX(t): the threat of the certified policy (the certificate is checked against the source once, then cached)."""
    if t not in _CERT:
        _CERT[t] = check_policy(tx_source(t), ('policy', t))
        assert _CERT[t] == t
    return _CERT[t]


# ================================================================== python reference resolver (both orders)
def follower_bid_py(d, R, value):
    x = (d * R + 5) // 10
    x = max(x, 1)
    return min(x, value)


def py_resolve(kP, kA, kB, v, order='items_first'):
    """bids (bP, bA, bB) of the program triple by direct evaluation of the sources.  order 'items_first': items, then TX on their outputs.
    order 'p_first': TX is evaluated first, and asks the item roles for their outputs afresh (no cached values).  Returns (bids, depth) where
    depth is the maximum call depth reached (items never call TX's output, so the depth is 2 at most)."""
    vP, vA, vB = v
    depth = [0]

    def read_P_certificate():
        if kP < NC:
            return kP + 1                              # a constant c: required total c + 1
        return certified_threat_of_tx(kP - TX0 + 1) + 1

    def item_bid(role, k, d0):
        depth[0] = max(depth[0], d0)
        if k < NC:
            return k
        if k >= F0 + NF:
            return 0
        return follower_bid_py(k - F0 + 1, read_P_certificate(), v[role])

    def p_bid(d0, get_T):
        depth[0] = max(depth[0], d0)
        if kP < NC:
            return kP
        return eval_src(tx_source(kP - TX0 + 1), get_T(d0 + 1))

    if order == 'items_first':
        bA = item_bid(1, kA, 1)
        bB = item_bid(2, kB, 1)
        bP = p_bid(1, lambda d0: bA + bB)
    elif order == 'p_first':
        bP = p_bid(1, lambda d0: item_bid(1, kA, d0 + 1) + item_bid(2, kB, d0 + 1))
        bA = item_bid(1, kA, 1)
        bB = item_bid(2, kB, 1)
    else:
        raise ValueError(order)
    return (bP, bA, bB), depth[0]


# ================================================================== numba resolver and tensor
@njit(cache=True)
def f_bid(d, R, value):
    x = (d * R + 5) // 10
    if x < 1:
        x = 1
    if x > value:
        x = value
    return x


@njit(cache=True)
def tx_bid(t, T):
    if T + 1 <= t:
        return T + 1
    return t


@njit(cache=True)
def required_total(kP):
    """what an item reads off the opposing P program: the certified threat plus one (TX), or the constant plus one."""
    if kP < NC:
        return kP + 1
    return (kP - NC + 1) + 1


@njit(cache=True)
def eval_item(k, kP, value):
    if k < NC:
        return k
    if k >= NC + NF:
        return 0
    return f_bid(k - NC + 1, required_total(kP), value)


@njit(cache=True)
def eval_P_fresh(kP, kA, kB, vA, vB):
    """TX evaluated first: asks the items for their outputs afresh."""
    if kP < NC:
        return kP
    T = eval_item(kA, kP, vA) + eval_item(kB, kP, vB)
    return tx_bid(kP - NC + 1, T)


@njit(cache=True)
def resolve2(kP, kA, kB, vA, vB, order):
    """order 0: items first, then TX on their outputs; order 1: TX first (fresh item evaluations), then the items."""
    if order == 0:
        bA = eval_item(kA, kP, vA)
        bB = eval_item(kB, kP, vB)
        if kP < NC:
            bP = kP
        else:
            bP = tx_bid(kP - NC + 1, bA + bB)
    else:
        bP = eval_P_fresh(kP, kA, kB, vA, vB)
        bA = eval_item(kA, kP, vA)
        bB = eval_item(kB, kP, vB)
    return bP, bA, bB


@njit(cache=True)
def _build2(vP, vA, vB, order, U, X, B):
    for kP in range(K):
        for kA in range(NC + NF):
            for kB in range(NC + NF):
                bP, bA, bB = resolve2(kP, kA, kB, vA, vB, order)
                B[0, kP, kA, kB] = bP; B[1, kP, kA, kB] = bA; B[2, kP, kA, kB] = bB
                o = C.outcome(bP, bA, bB, vP, vA, vB)
                U[0, kP, kA, kB] = o[0]; U[1, kP, kA, kB] = o[1]; U[2, kP, kA, kB] = o[2]
                X[C.XREV, kP, kA, kB] = o[3]; X[C.XEFF, kP, kA, kB] = o[4]; X[C.XIR, kP, kA, kB] = o[5]; X[C.XCORE, kP, kA, kB] = o[6]
                X[C.XPRUWIN, kP, kA, kB] = o[7] if kP >= NC else 0.0       # P(TX wins)
                X[C.XCYC, kP, kA, kB] = 0.0
                X[C.XBP, kP, kA, kB] = bP; X[C.XBA, kP, kA, kB] = bA; X[C.XBB, kP, kA, kB] = bB
                X[XPW, kP, kA, kB] = o[7]; X[XAW, kP, kA, kB] = o[8]; X[XBW, kP, kA, kB] = o[9]


_TENS = {}


def build_tensor2(inst, order=0):
    """payoff tensor U (3, K, K, K), statistics tensor X (NX2, K, K, K) float32 and the resolved bids B (3, K, K, K), for the instance.  The bid space
    does not enter the tensor (the prior restricts the allowed programs)."""
    key = (inst, order)
    if key not in _TENS:
        v = C.INSTANCES[inst]
        U = np.zeros((3, K, K, K)); X = np.zeros((NX2, K, K, K), np.float32); B = np.zeros((3, K, K, K), np.int64)
        _build2(v[0], v[1], v[2], order, U, X, B)
        _TENS[key] = (U, X, B)
    return _TENS[key]


# ================================================================== priors
def role_caps(inst, space):
    return C.allowed(inst, space)


def prior2(inst, space, m, ptype='tx', itype='fol'):
    """per-role founding prior (3, K).  P: ptype 'tx' constants (1 - m) uniform on 0..capP plus TX(t) mass m uniform on t = 1..capP; 'const' constants
    only (uniform); 'matched' constants (1 - m) uniform plus the constants c = t at mass m uniform over t = 1..capP.  Items: itype 'fol'
    constants (1 - m) uniform on 0..cap plus followers mass m uniform over the nine deltas; 'const' constants only."""
    caps = role_caps(inst, space)
    p = np.zeros((3, K))
    n = caps[0] + 1
    if ptype == 'tx':
        p[0, :n] = (1 - m) / n
        p[0, TX0:TX0 + caps[0]] = m / caps[0]
    elif ptype == 'const':
        p[0, :n] = 1.0 / n
    elif ptype == 'matched':
        p[0, :n] = (1 - m) / n
        p[0, 1:caps[0] + 1] += m / caps[0]
    else:
        raise ValueError(ptype)
    for r in (1, 2):
        n = caps[r] + 1
        if itype == 'fol':
            p[r, :n] = (1 - m) / n
            p[r, F0:F0 + NF] = m / NF
        elif itype == 'const':
            p[r, :n] = 1.0 / n
        else:
            raise ValueError(itype)
    return p


def rain_prior(pr, kind):
    """the arrival (rain) draw distribution per role (3, K): 'same' as the founding prior; 'fol_only' the item roles draw only followers (uniform over
    the nine deltas), P unchanged (control iv); 'safe' the item roles draw only followers with delta >= 0.5 (control iv'')."""
    q = pr.copy()
    if kind == 'same':
        return q
    for r in (1, 2):
        q[r] = 0.0
        if kind == 'fol_only':
            q[r, F0:F0 + NF] = 1.0 / NF
        elif kind == 'safe':
            q[r, F0 + 4:F0 + NF] = 1.0 / 5          # deltas 0.5..0.9
        else:
            raise ValueError(kind)
    return q


def threat_of(k):
    """threat of a P program: c for a constant, t for TX(t)."""
    return float(k) if k < NC else float(k - NC + 1)


def prior_mean_threat(pr):
    return float(sum(pr[0, k] * threat_of(k) for k in range(K)))


# ================================================================== arrivals (precomputed so controls can be paired)
def make_arrivals(sched, N, I, cdf, seed, roles=(0, 1, 2)):
    """arrival schedule for generations 0..len(sched)-1: for each generation the number of arrivals is Binomial(3 I N, eps_g); each arrival has a slot
    among the 3 I N event slots of the generation, an island, a role, a uniform u0 mapped through the role's cdf to the arriving program, and a
    uniform u1 that picks the victim.  The island, role and uniforms are drawn before any role filtering, so cells with different cdfs or role filters
    share arrival times.  `cdf` is (3, K).  Returns (ptr, pos, island, role, child, u1) with ptr of length gens + 2."""
    rng = np.random.default_rng(seed)
    gens = len(sched)
    ns = rng.binomial(3 * I * N, np.clip(sched, 0.0, 1.0))
    tot = int(ns.sum())
    pos = np.empty(tot, np.int64); isl = np.empty(tot, np.int64); rol = np.empty(tot, np.int64)
    u0 = rng.random(tot); u1 = rng.random(tot)
    ptr = np.zeros(gens + 2, np.int64)
    ptr[1:gens + 1] = np.cumsum(ns)
    ptr[gens + 1] = tot
    for g in range(gens):
        a, b = ptr[g], ptr[g + 1]
        if b > a:
            pos[a:b] = np.sort(rng.integers(0, 3 * I * N, b - a))
            isl[a:b] = rng.integers(0, I, b - a)
            rol[a:b] = rng.integers(0, 3, b - a)
    child = np.empty(tot, np.int64)
    for r in range(3):
        sel = rol == r
        child[sel] = np.minimum(np.searchsorted(cdf[r], u0[sel], side='left'), K - 1)
    keep = np.isin(rol, np.array(roles))
    if not keep.all():
        # drop arrivals of filtered roles, rebuilding the pointer array
        gen_of = np.repeat(np.arange(gens), ns)
        newptr = np.zeros(gens + 2, np.int64)
        cnt = np.bincount(gen_of[keep], minlength=gens)
        newptr[1:gens + 1] = np.cumsum(cnt)
        newptr[gens + 1] = int(keep.sum())
        return newptr, pos[keep], isl[keep], rol[keep], child[keep], u1[keep]
    return ptr, pos, isl, rol, child, u1


# ================================================================== extra statistics (numba)
@njit(cache=True)
def _stats2(U, X, counts, i, N, row2):
    Kk = counts.shape[2]
    row2[:] = 0.0
    pw = 0.0; Ts = 0.0; bps = 0.0
    for a in range(Kk):
        ca = counts[i, 0, a]
        if ca == 0:
            continue
        for b in range(Kk):
            cb = counts[i, 1, b]
            if cb == 0:
                continue
            for c in range(Kk):
                cc = counts[i, 2, c]
                if cc == 0:
                    continue
                p = ca * cb * cc / (N * N * N * 1.0)
                pw += p * X[XPW, a, b, c]
                Ts += p * (X[C.XBA, a, b, c] + X[C.XBB, a, b, c])
                bps += p * X[C.XBP, a, b, c]
    row2[0] = pw; row2[2] = Ts; row2[3] = bps
    th = 0.0
    ntx = 0.0; dsum = 0.0
    for k in range(Kk):
        ck = counts[i, 0, k]
        if ck == 0:
            continue
        if k < NC:
            th += ck * k
        else:
            th += ck * (k - NC + 1)
            t = k - NC + 1
            dsum += ck * (C._payoff_of(U, counts, i, 0, k) - C._payoff_of(U, counts, i, 0, t)) / (N * N * 1.0)
            ntx += ck
    row2[1] = th / N
    row2[4] = dsum / ntx if ntx > 0 else 0.0


@njit(cache=True)
def _update_tested(X, counts, pres, npres, first, i, N, g):
    for qi in range(npres[i, 0]):
        k = pres[i, 0, qi]
        if k < NC or first[i, k] >= 0:
            continue
        s = 0.0
        for a in range(npres[i, 1]):
            x = pres[i, 1, a]; cx = counts[i, 1, x]
            for b in range(npres[i, 2]):
                y = pres[i, 2, b]
                s += cx * counts[i, 2, y] * X[C.XPRUWIN, k, x, y]
        if s > 1e-12:
            first[i, k] = g


@njit(cache=True)
def _replace(U, counts, pay, pres, npres, pos, i, r, victim, child):
    """the stage-1 swap victim -> child in role r of island i, with the incremental payoff update."""
    s1 = (r + 1) % 3; s2 = (r + 2) % 3
    for dd in range(2):
        s = s1 if dd == 0 else s2
        t3 = s2 if dd == 0 else s1
        for q in range(npres[i, s]):
            k = pres[i, s, q]
            d = 0.0
            for z in range(npres[i, t3]):
                y = pres[i, t3, z]
                kp, ka, kb = C._tri(r, child, s, k, t3, y)
                kp2, ka2, kb2 = C._tri(r, victim, s, k, t3, y)
                d += counts[i, t3, y] * (U[s, kp, ka, kb] - U[s, kp2, ka2, kb2])
            pay[i, s, k] += d
    counts[i, r, victim] -= 1
    if counts[i, r, victim] == 0:
        q = pos[i, r, victim]; last = pres[i, r, npres[i, r] - 1]
        pres[i, r, q] = last; pos[i, r, last] = q; pos[i, r, victim] = -1; npres[i, r] -= 1
    newp = False
    if counts[i, r, child] == 0:
        pres[i, r, npres[i, r]] = child; pos[i, r, child] = npres[i, r]; npres[i, r] += 1
        newp = True
    counts[i, r, child] += 1
    if newp:
        pay[i, r, child] = C._payoff_of(U, counts, i, r, child)


@njit(cache=True)
def _pick_victim(counts, pres, npres, i, r, u1):
    acc = 0
    victim = pres[i, r, 0]
    for t in range(npres[i, r]):
        k = pres[i, r, t]
        acc += counts[i, r, k]
        if u1 < acc:
            victim = k
            break
    return victim


@njit(cache=True)
def sim2(U, X, init, N, w, m, gens, seed, arr_ptr, arr_pos, arr_i, arr_r, arr_child, arr_u1, samples, minrev, test_every):
    """The stage-1 island kernel with scheduled arrivals.  Returns (counts, samp (ns, I, NS), samp2 (ns, I, NS2), hist (ns, I, 3, K) int16,
    first_erode (I), stop_g, pay, fix_items (I), fix_all (I), first_tested (I, K), repl_rain (ns, I), repl_mig (ns, I))."""
    np.random.seed(seed)
    I = init.shape[0]; Kk = init.shape[2]
    counts = init.copy()
    pay = np.zeros((I, 3, Kk))
    pres = np.zeros((I, 3, Kk), np.int64); npres = np.zeros((I, 3), np.int64); pos = -np.ones((I, 3, Kk), np.int64)
    for i in range(I):
        for r in range(3):
            for k in range(Kk):
                if counts[i, r, k] > 0:
                    pres[i, r, npres[i, r]] = k; pos[i, r, k] = npres[i, r]; npres[i, r] += 1
        for r in range(3):
            for k in range(Kk):
                if counts[i, r, k] > 0:
                    pay[i, r, k] = C._payoff_of(U, counts, i, r, k)
    ns = samples.shape[0]
    samp = np.zeros((ns, I, C.NS)); samp2 = np.zeros((ns, I, NS2))
    hist = np.zeros((ns, I, 3, Kk), np.int16)
    rr = np.zeros((ns, I), np.int64); rm = np.zeros((ns, I), np.int64)
    first_erode = -np.ones(I, np.int64)
    fix_items = -np.ones(I, np.int64); fix_all = -np.ones(I, np.int64)
    first_tested = -np.ones((I, Kk), np.int64)
    cur_rr = np.zeros(I, np.int64); cur_rm = np.zeros(I, np.int64)
    row = np.zeros(C.NS); row2 = np.zeros(NS2)
    si = 0
    stop_g = gens
    nsched_end = arr_ptr[gens]
    ptr = 0
    for g in range(gens + 1):
        while si < ns and samples[si] <= g:
            for i in range(I):
                C._stats(U, X, counts, i, N, row)
                samp[si, i, :] = row
                _stats2(U, X, counts, i, N, row2)
                samp2[si, i, :] = row2
                for r in range(3):
                    for k in range(Kk):
                        hist[si, i, r, k] = counts[i, r, k]
                rr[si, i] = cur_rr[i]; rm[si, i] = cur_rm[i]
                if first_erode[i] < 0 and row[3] < minrev - 1.0 - 1e-9:
                    first_erode[i] = samples[si]
            si += 1
        allfix = True
        for i in range(I):
            if fix_items[i] < 0 and npres[i, 1] == 1 and npres[i, 2] == 1:
                fix_items[i] = g
            if fix_all[i] < 0 and npres[i, 0] == 1 and npres[i, 1] == 1 and npres[i, 2] == 1:
                fix_all[i] = g
            if npres[i, 0] > 1 or npres[i, 1] > 1 or npres[i, 2] > 1:
                allfix = False
            if g % test_every == 0:
                _update_tested(X, counts, pres, npres, first_tested, i, N, g)
        if g == gens:
            break
        if m == 0.0 and allfix and ptr >= arr_ptr[gens]:
            # frozen for good: no migration, no arrivals left
            stop_g = g
            break
        a_end = arr_ptr[g + 1]
        for e in range(3 * I * N):
            did = False
            while ptr < a_end and arr_pos[ptr] == e:
                i = arr_i[ptr]; r = arr_r[ptr]; child = arr_child[ptr]
                u1 = int(arr_u1[ptr] * N)
                victim = _pick_victim(counts, pres, npres, i, r, u1)
                if victim != child:
                    _replace(U, counts, pay, pres, npres, pos, i, r, victim, child)
                    cur_rr[i] += 1
                ptr += 1
                did = True
            if did:
                continue
            i = np.random.randint(I)
            r = np.random.randint(3)
            if m == 0.0 and npres[i, r] == 1:
                continue
            src = i
            if m > 0.0 and np.random.random() < m:
                src = np.random.randint(I - 1)
                if src >= i:
                    src += 1
            child = C._fit(counts, pay, src, r, pres, npres, N, w)
            u1 = np.random.randint(N)
            victim = _pick_victim(counts, pres, npres, i, r, u1)
            if victim == child:
                continue
            _replace(U, counts, pay, pres, npres, pos, i, r, victim, child)
            if src != i:
                cur_rm[i] += 1
    if stop_g < gens:
        while si < ns:
            for i in range(I):
                C._stats(U, X, counts, i, N, row)
                samp[si, i, :] = row
                _stats2(U, X, counts, i, N, row2)
                samp2[si, i, :] = row2
                for r in range(3):
                    for k in range(Kk):
                        hist[si, i, r, k] = counts[i, r, k]
                rr[si, i] = cur_rr[i]; rm[si, i] = cur_rm[i]
            si += 1
    return counts, samp, samp2, hist, first_erode, stop_g, pay, fix_items, fix_all, first_tested, rr, rm
