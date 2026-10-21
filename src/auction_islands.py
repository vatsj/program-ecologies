"""Part B of the coalition-proof auctions run: rings versus police among open-source bidders (spec specs/2026-10-21-coalition-proof-auctions.md).

Roles (one population per role per island): A and B (item bidders, role indices 0 and 1) and P (the package bidder, role 2); the auction
table is the AM family with bidder order (P, A, B).  Bids are integers on 0..40.

Programs (resolution order is fixed: item programs first, conditioned on the partner item program's source class; then P, reading the item
programs' sources and committing to their intended bids; trembles, when used, are realized after all commitments):
  A, B:  T      truthful
         SH     the singleton's best reply to truthful others under the rule in force (ties: closest to truthful, then smaller)
         PAIR   iff the partner item program is PAIR: its half of the pair's best joint report against a truthful P (maximizing the pair's total
                subject to each member gaining individually; ties to the smaller total bid, then lexicographic); otherwise truthful
         PAIRU  its half of that joint report unconditionally
  P:     T      truthful
         POL    reads the item programs, commits to the best reply to their intended bids that is worst for the items' total (spite counts); against
                truthful items it is truthful
         SH     P's best reply to truthful items under the rule
`CONST(c)` (a constant bid) is a mutant class used only in the invasion diagnostics.  The reading audit replaces PAIR and POL by T.

The dynamics: the eps = 0 seed lottery (no mutation), fixed roles, a birth-death process with fitness exp(w * expected payoff) as in
`fixed_role_chicken.sim_two_pop`, extended to three populations per island.  Islands with every present program payoff-equivalent against every
present combination are frozen (absorbed); islands not frozen at the horizon are censored.
"""
import os, sys, math, json, itertools
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auctions as A
from abm import njit

ROOT = A.ROOT
OUT = os.path.join(ROOT, 'runs', 'auctions')
R = 41                       # bids 0..40
W = 0.3
INSTANCES = {'collusion': (20, 5, 5), 'threshold': (20, 15, 15)}     # (vP, vA, vB)
RULES = ('vcg', 'surcharge', 'fp')
ITEM = ('T', 'SH', 'PAIR', 'PAIRU')
PROG_P = ('T', 'POL', 'SH')
K = 4
TOL = 1e-9
_AUC = None


def auc():
    global _AUC
    if _AUC is None:
        _AUC = A.Auction(A.FAMILIES['AM'], R)
    return _AUC


class Ctx:
    """one (rule, instance): the table, truthful baselines, the singleton best replies, the pair's joint report."""

    def __init__(self, rule, inst):
        self.rule = rule; self.inst = inst
        self.v = INSTANCES[inst]                      # (vP, vA, vB)
        a = auc(); self.a = a
        self.win, self.pay = a.tables(rule)
        self.truth = self.v
        self.u0 = self.payoffs(self.v)
        vP, vA, vB = self.v
        # singleton best replies to truthful others
        self.sh_A = self.best_reply(1, (vP, None, vB))
        self.sh_B = self.best_reply(2, (vP, vA, None))
        self.sh_P = self.best_reply(0, (None, vA, vB))
        self.pair = self.pair_report()

    def idx(self, b):
        return int(b[0]) + R * int(b[1]) + R * R * int(b[2])

    def payoffs(self, b):
        """(uP, uA, uB) at the bid profile b = (bP, bA, bB)."""
        k = self.idx(b)
        return tuple(self.v[i] * int(self.win[k, i]) - self.pay[k, i] for i in range(3))

    def outcome(self, b):
        k = self.idx(b)
        return dict(win=[int(self.win[k, i]) for i in range(3)], pay=[float(self.pay[k, i]) for i in range(3)],
                    u=[float(self.v[i] * int(self.win[k, i]) - self.pay[k, i]) for i in range(3)])

    def best_reply(self, i, others):
        """best bid for bidder i (0 = P, 1 = A, 2 = B) against the fixed others; ties: closest to truth, then smaller."""
        best = None
        for x in range(R):
            b = list(others); b[i] = x
            u = self.payoffs(tuple(b))[i]
            key = (-u, abs(x - self.v[i]), x)
            if best is None or key < best[0]:
                best = (key, x)
        return best[1]

    def pair_report(self):
        """the pair's best joint report against a truthful P (each member gains individually; total max; ties smaller total bid)."""
        vP, vA, vB = self.v
        u0 = self.u0
        best = None
        for bA in range(R):
            for bB in range(R):
                u = self.payoffs((vP, bA, bB))
                if u[1] > u0[1] + TOL and u[2] > u0[2] + TOL:
                    key = (-(u[1] + u[2]), bA + bB, bA, bB)
                    if best is None or key < best[0]:
                        best = (key, (bA, bB))
        return best[1] if best else (vA, vB)

    # ------------------------------------------------------------ program resolution
    def item_bid(self, role, prog, partner):
        """role 1 = A, 2 = B (bidder index); `prog`, `partner`: names or ('C', c)."""
        v = self.v[role]
        if isinstance(prog, tuple):
            return prog[1]
        if prog == 'T':
            return v
        if prog == 'SH':
            return self.sh_A if role == 1 else self.sh_B
        half = self.pair[0] if role == 1 else self.pair[1]
        if prog == 'PAIRU':
            return half
        if prog == 'PAIR':
            return half if partner == 'PAIR' else v
        raise ValueError(prog)

    def p_bid(self, prog, bA, bB):
        """P's bid given the items' intended bids (P reads the item sources and commits)."""
        vP, vA, vB = self.v
        if isinstance(prog, tuple):
            return prog[1]
        if prog == 'T':
            return vP
        if prog == 'SH':
            return self.sh_P
        if prog == 'POL':
            if (bA, bB) == (vA, vB):
                return vP
            return self.spite_reply(bA, bB)
        raise ValueError(prog)

    def spite_reply(self, bA, bB):
        """P's best reply to the intended item bids that is worst for the items' total payoff (ties: closest to truthful, then smaller)."""
        best = None
        us = [self.payoffs((x, bA, bB)) for x in range(R)]
        m = max(u[0] for u in us)
        for x in range(R):
            if us[x][0] >= m - TOL:
                key = (us[x][1] + us[x][2], abs(x - self.v[0]), x)
                if best is None or key < best[0]:
                    best = (key, x)
        return best[1]

    def bids(self, pa, pb, pp, audit=False):
        if audit:
            pa = 'T' if (isinstance(pa, str) and pa == 'PAIR') else pa
            pb = 'T' if (isinstance(pb, str) and pb == 'PAIR') else pb
            pp = 'T' if (isinstance(pp, str) and pp == 'POL') else pp
        bA = self.item_bid(1, pa, pb)
        bB = self.item_bid(2, pb, pa)
        bP = self.p_bid(pp, bA, bB)
        return (bP, bA, bB)


def tensor(rule, inst, audit=False):
    """UA, UB, UP (K, K, K) payoff arrays indexed [a, b, p] (a, b over ITEM, p over PROG_P), plus a record of each triple."""
    c = Ctx(rule, inst)
    U = np.zeros((3, K, K, K))
    rec = {}
    for a, pa in enumerate(ITEM):
        for b, pb in enumerate(ITEM):
            for p, pp in enumerate(PROG_P):
                bid = c.bids(pa, pb, pp, audit)
                o = c.outcome(bid)
                U[0, a, b, p] = o['u'][1]; U[1, a, b, p] = o['u'][2]; U[2, a, b, p] = o['u'][0]
                joint = (bid[1], bid[2]) == c.pair and c.pair != (c.v[1], c.v[2])
                rec['%s|%s|%s' % (pa, pb, pp)] = dict(bids=list(bid), win=o['win'], pay=o['pay'], u=dict(A=o['u'][1], B=o['u'][2], P=o['u'][0]),
                                                      revenue=sum(o['pay']), joint_deviation=bool(joint),
                                                      efficient=bool(sum(self_v * w for self_v, w in zip(c.v, o['win'])) == int(auc().W[c.idx(c.v)])))
    return U, rec, c


def pure_nash(U, strict=False):
    """pure Nash equilibria of the three-role game over program triples (labels); strict: every unilateral deviation strictly worse."""
    out = []
    for a in range(len(ITEM)):
        for b in range(len(ITEM)):
            for p in range(len(PROG_P)):
                ok = True
                gap = -TOL if strict else TOL
                for a2 in range(len(ITEM)):
                    if a2 != a and (U[0, a2, b, p] > U[0, a, b, p] + TOL if not strict else U[0, a2, b, p] > U[0, a, b, p] - TOL): ok = False
                for b2 in range(len(ITEM)):
                    if b2 != b and (U[1, a, b2, p] > U[1, a, b, p] + TOL if not strict else U[1, a, b2, p] > U[1, a, b, p] - TOL): ok = False
                for p2 in range(len(PROG_P)):
                    if p2 != p and (U[2, a, b, p2] > U[2, a, b, p] + TOL if not strict else U[2, a, b, p2] > U[2, a, b, p] - TOL): ok = False
                if ok:
                    out.append((ITEM[a], ITEM[b], PROG_P[p]))
    return out


# ------------------------------------------------------------------ tremble control and constant-bid invasion diagnostics
def tremble(rule, inst, q=0.05):
    """P's committed bid is computed from the pair's intended bids; each pair member then independently fails to play its half
    with probability q (plays truthful instead).  Expected payoffs of P programs and of the pair members against (PAIR, PAIR)."""
    c = Ctx(rule, inst)
    vP, vA, vB = c.v
    res = {}
    intended = c.bids('PAIR', 'PAIR', 'T')
    bA_i, bB_i = intended[1], intended[2]
    for pp in PROG_P:
        bP = c.p_bid(pp, bA_i, bB_i)          # committed before the trembles
        e = np.zeros(3)
        for fa in (0, 1):
            for fb in (0, 1):
                pr = (q if fa else 1 - q) * (q if fb else 1 - q)
                bA = vA if fa else bA_i; bB = vB if fb else bB_i
                u = c.payoffs((bP, bA, bB))
                e += pr * np.array(u)
        res[pp] = dict(commit_bid=int(bP), E_uP=float(e[0]), E_uA=float(e[1]), E_uB=float(e[2]), E_items=float(e[1] + e[2]))
    # deterministic benchmark (q = 0)
    res0 = {}
    for pp in PROG_P:
        bP = c.p_bid(pp, bA_i, bB_i)
        u = c.payoffs((bP, bA_i, bB_i))
        res0[pp] = dict(commit_bid=int(bP), uP=float(u[0]), uA=float(u[1]), uB=float(u[2]))
    return dict(rule=rule, inst=inst, q=q, intended_pair=[int(bA_i), int(bB_i)], tremble=res, no_tremble=res0)


def invasion(rule, inst, audit=False):
    """for every resident triple and role, every constant bid on 0..40 as a one-program mutant: the best mutant, whether any constant
    invades (strictly outperforms the resident's payoff), and the number of invading constants; also each pair member's individual gain
    over the truthful baseline for the (PAIR, PAIR, p) triples.  The mutant's source class is CONST, so a PAIR partner plays truthful and
    POL reads the constant."""
    c = Ctx(rule, inst)
    out = []
    for pa in ITEM:
        for pb in ITEM:
            for pp in PROG_P:
                if audit and (pa == 'PAIR' or pb == 'PAIR' or pp == 'POL'):
                    continue
                bid = c.bids(pa, pb, pp, audit)
                u_res = c.payoffs(bid)       # (P, A, B)
                row = dict(triple='%s|%s|%s' % (pa, pb, pp), roles={})
                for role, ri in (('A', 1), ('B', 2), ('P', 0)):
                    best = None; inv = []
                    for x in range(R):
                        if role == 'A':
                            mb = c.bids(('C', x), pb, pp, audit)
                        elif role == 'B':
                            mb = c.bids(pa, ('C', x), pp, audit)
                        else:
                            mb = c.bids(pa, pb, ('C', x), audit)
                        mut = c.payoffs(mb)[ri]
                        if mut > u_res[ri] + TOL:
                            inv.append(x)
                        if best is None or mut > best[1] + TOL or (abs(mut - best[1]) <= TOL and abs(x - c.v[ri]) < abs(best[0] - c.v[ri])):
                            best = (x, mut)
                    row['roles'][role] = dict(resident_payoff=float(u_res[ri]), best_constant=int(best[0]), best_constant_payoff=float(best[1]),
                                              n_invading_constants=len(inv), invading=inv)
                if pa == 'PAIR' and pb == 'PAIR' and not audit:
                    row['pair_gain_over_truthful'] = dict(A=float(u_res[1] - c.u0[1]), B=float(u_res[2] - c.u0[2]), P=float(u_res[0] - c.u0[0]))
                out.append(row)
    return out


def static_report():
    res = dict(instances=INSTANCES, tensors={}, nash={}, tremble={}, invasion={}, pair_report={})
    for inst in INSTANCES:
        for rule in RULES:
            for audit in (False, True):
                key = '%s/%s/%s' % (rule, inst, 'audit' if audit else 'open')
                U, rec, c = tensor(rule, inst, audit)
                res['tensors'][key] = rec
                res['nash'][key] = dict(weak=pure_nash(U), strict=pure_nash(U, True))
                res['pair_report'][key] = dict(pair_joint_report=list(c.pair), SH=dict(A=c.sh_A, B=c.sh_B, P=c.sh_P), truthful_payoffs=dict(P=c.u0[0], A=c.u0[1], B=c.u0[2]))
                res['invasion'][key] = invasion(rule, inst, audit)
            res['tremble']['%s/%s' % (rule, inst)] = tremble(rule, inst)
    return res


# ------------------------------------------------------------------ priors
def prior(kind, noPOL=False):
    """role priors: (pA over ITEM, pB over ITEM, pP over PROG_P).  U uniform; S half on T; M matched-mass (POL mass = f(PAIR)^2)."""
    item = np.full(4, 0.25); pp = np.full(3, 1 / 3)
    if kind == 'S':
        item = np.array([0.5, 1 / 6, 1 / 6, 1 / 6]); pp = np.array([0.5, 0.25, 0.25])
    elif kind == 'M':
        pp = np.array([15 / 32, 1 / 16, 15 / 32])         # POL = (1/4)^2 = 1/16; T and SH split the remaining 15/16
    if noPOL:
        pp = pp.copy(); pp[1] = 0.0; pp = pp / pp.sum()
    return item, item.copy(), pp


def seed_counts(pr, I, N, rng):
    """founders: counts (I, 3, K) for roles A, B, P."""
    out = np.zeros((I, 3, K), np.int64)
    for i in range(I):
        out[i, 0, :4] = rng.multinomial(N, pr[0])
        out[i, 1, :4] = rng.multinomial(N, pr[1])
        out[i, 2, :3] = rng.multinomial(N, pr[2])
    return out


def audit_map(counts):
    """the reading audit on founders: PAIR -> T in A and B, POL -> T in P (mass moves to T)."""
    c = counts.copy()
    for r in (0, 1):
        c[:, r, 0] += c[:, r, 2]; c[:, r, 2] = 0
    c[:, 2, 0] += c[:, 2, 1]; c[:, 2, 1] = 0
    return c


# ------------------------------------------------------------------ the dynamics (numba)
@njit(cache=True)
def _fit(counts, pay, i, r, pres, npres, N, w):
    m = -1e300
    for t in range(npres[i, r]):
        k = pres[i, r, t]
        f = pay[i, r, k] / (N * N)
        if f > m:
            m = f
    tot = 0.0
    for t in range(npres[i, r]):
        k = pres[i, r, t]
        tot += counts[i, r, k] * np.exp(w * (pay[i, r, k] / (N * N) - m))
    u = np.random.random() * tot; acc = 0.0
    for t in range(npres[i, r]):
        k = pres[i, r, t]
        acc += counts[i, r, k] * np.exp(w * (pay[i, r, k] / (N * N) - m))
        if u <= acc:
            return k
    return pres[i, r, npres[i, r] - 1]


@njit(cache=True)
def _island_frozen(counts, U, i):
    """present programs of each role payoff-equivalent against every present combination of the other two roles (island i)."""
    for r in range(3):
        r1 = (r + 1) % 3; r2 = (r + 2) % 3
        k0 = -1
        for k in range(K):
            if counts[i, r, k] == 0:
                continue
            if k0 < 0:
                k0 = k; continue
            for x in range(K):
                if counts[i, r1, x] == 0:
                    continue
                for y in range(K):
                    if counts[i, r2, y] == 0:
                        continue
                    if r == 0:
                        d = U[0, k, x, y] - U[0, k0, x, y]
                    elif r == 1:
                        d = U[1, y, k, x] - U[1, y, k0, x]
                    else:
                        d = U[2, x, y, k] - U[2, x, y, k0]
                    if abs(d) > 1e-9:
                        return False
    return True


@njit(cache=True)
def _global_frozen(counts, U, I):
    """every present program, over the union of the islands, equivalent against every combination present anywhere."""
    pres = np.zeros((3, K), np.bool_)
    for i in range(I):
        for r in range(3):
            for k in range(K):
                if counts[i, r, k] > 0:
                    pres[r, k] = True
    for r in range(3):
        r1 = (r + 1) % 3; r2 = (r + 2) % 3
        k0 = -1
        for k in range(K):
            if not pres[r, k]:
                continue
            if k0 < 0:
                k0 = k; continue
            for x in range(K):
                if not pres[r1, x]:
                    continue
                for y in range(K):
                    if not pres[r2, y]:
                        continue
                    if r == 0:
                        d = U[0, k, x, y] - U[0, k0, x, y]
                    elif r == 1:
                        d = U[1, y, k, x] - U[1, y, k0, x]
                    else:
                        d = U[2, x, y, k] - U[2, x, y, k0]
                    if abs(d) > 1e-9:
                        return False
    return True


@njit(cache=True)
def _payoff_of(U, r, k, c0, c1, c2, N):
    """unnormalized expected payoff sum_{x,y} c_x c_y U_r[...] of program k in role r given the island's counts."""
    s = 0.0
    if r == 0:
        for x in range(K):
            if c1[x] == 0: continue
            for y in range(K):
                s += c1[x] * c2[y] * U[0, k, x, y]
    elif r == 1:
        for x in range(K):
            if c0[x] == 0: continue
            for y in range(K):
                s += c0[x] * c2[y] * U[1, x, k, y]
    else:
        for x in range(K):
            if c0[x] == 0: continue
            for y in range(K):
                s += c0[x] * c1[y] * U[2, x, y, k]
    return s


@njit(cache=True)
def sim3(U, init, N, w, m, gens, seed, check_every, pol_idx, pairA_idx, pairU_idx, stop_all):
    """Three populations per island.  Returns final counts (I, 3, K), the generation each island became payoff-frozen and the generation it
    became fixed (every role monomorphic; -1: censored), the first
    generation `POL` was the only P program (-1: never), whether (after that) a deviating pair (PAIR in both item roles or PAIRU in both)
    was present at a generation boundary, the stop generation.  With m > 0 the run stops only when globally frozen."""
    np.random.seed(seed)
    I = init.shape[0]
    counts = init.copy()
    pay = np.zeros((I, 3, K))
    pres = np.zeros((I, 3, K), np.int64); npres = np.zeros((I, 3), np.int64); pos = -np.ones((I, 3, K), np.int64)
    for i in range(I):
        for r in range(3):
            for k in range(K):
                if counts[i, r, k] > 0:
                    pres[i, r, npres[i, r]] = k; pos[i, r, k] = npres[i, r]; npres[i, r] += 1
        for r in range(3):
            for k in range(K):
                pay[i, r, k] = _payoff_of(U, r, k, counts[i, 0], counts[i, 1], counts[i, 2], N)
    frozen_gen = -np.ones(I, np.int64)
    fixed_gen = -np.ones(I, np.int64)
    frozen = np.zeros(I, np.bool_)
    fixed = np.zeros(I, np.bool_)
    pol_fix = -np.ones(I, np.int64)
    tested = np.zeros(I, np.int64)
    stop_g = gens
    for g in range(gens + 1):
        # boundary bookkeeping
        for i in range(I):
            if pol_idx >= 0 and pol_fix[i] < 0 and counts[i, 2, pol_idx] == N:
                pol_fix[i] = g
            if pol_fix[i] >= 0 and tested[i] == 0:
                if (counts[i, 0, pairA_idx] > 0 and counts[i, 1, pairA_idx] > 0) or (counts[i, 0, pairU_idx] > 0 and counts[i, 1, pairU_idx] > 0):
                    tested[i] = 1
        allfix = True
        for i in range(I):
            if not fixed[i]:
                if npres[i, 0] == 1 and npres[i, 1] == 1 and npres[i, 2] == 1:
                    fixed[i] = True; fixed_gen[i] = g
                else:
                    allfix = False
        if g % check_every == 0:
            for i in range(I):
                if not frozen[i]:
                    if _island_frozen(counts, U, i):
                        frozen[i] = True; frozen_gen[i] = g
            if m > 0.0:
                if _global_frozen(counts, U, I):
                    stop_g = g
                    break
        if m == 0.0 and allfix and stop_all == 1:
            stop_g = g
            break
        if g == gens:
            break
        for e in range(3 * I * N):
            i = np.random.randint(I)
            r = np.random.randint(3)
            if m == 0.0 and fixed[i]:
                continue
            src = i
            if m > 0.0 and np.random.random() < m:
                src = np.random.randint(I - 1)
                if src >= i: src += 1
            child = _fit(counts, pay, src, r, pres, npres, N, w)
            u = np.random.randint(N); acc = 0; victim = pres[i, r, 0]
            for t in range(npres[i, r]):
                k = pres[i, r, t]; acc += counts[i, r, k]
                if u < acc:
                    victim = k; break
            if victim == child:
                continue
            counts[i, r, victim] -= 1
            if counts[i, r, victim] == 0:
                q = pos[i, r, victim]; last = pres[i, r, npres[i, r] - 1]
                pres[i, r, q] = last; pos[i, r, last] = q; pos[i, r, victim] = -1; npres[i, r] -= 1
            if counts[i, r, child] == 0:
                pres[i, r, npres[i, r]] = child; pos[i, r, child] = npres[i, r]; npres[i, r] += 1
            counts[i, r, child] += 1
            # update the other roles' payoffs: a role-r change alters the payoffs of roles r1 and r2
            for dr in range(1, 3):
                rr = (r + dr) % 3
                for k in range(K):
                    pay[i, rr, k] = _payoff_of(U, rr, k, counts[i, 0], counts[i, 1], counts[i, 2], N)
    return counts, frozen_gen, fixed_gen, pol_fix, tested, stop_g


# ------------------------------------------------------------------ island end-state classification
def encounter_stats(c, counts_i, audit):
    """for one island (counts (3, K)): probabilities over encounters of the joint deviation, item deviation, P deviation, efficiency, revenue, etc."""
    N = counts_i[0].sum()
    fA = counts_i[0] / N; fB = counts_i[1] / N; fP = counts_i[2] / N
    vP, vA, vB = c.v
    wstar = int(auc().W[c.idx(c.v)])
    st = dict(joint=0.0, items_dev=0.0, p_dev=0.0, truthful=0.0, eff=0.0, rev=0.0, uA=0.0, uB=0.0, uP=0.0, items_win=0.0)
    for a in range(4):
        if fA[a] == 0: continue
        for b in range(4):
            if fB[b] == 0: continue
            for p in range(3):
                pr = fA[a] * fB[b] * fP[p]
                if pr == 0: continue
                bid = c.bids(ITEM[a], ITEM[b], PROG_P[p], audit)
                o = c.outcome(bid)
                joint = (bid[1], bid[2]) == c.pair and c.pair != (vA, vB)
                st['joint'] += pr * joint
                st['items_dev'] += pr * ((bid[1], bid[2]) != (vA, vB))
                st['p_dev'] += pr * (bid[0] != vP)
                st['truthful'] += pr * (bid == c.v)
                st['eff'] += pr * (sum(vv * ww for vv, ww in zip(c.v, o['win'])) == wstar)
                st['rev'] += pr * sum(o['pay'])
                st['uP'] += pr * o['u'][0]; st['uA'] += pr * o['u'][1]; st['uB'] += pr * o['u'][2]
                st['items_win'] += pr * (o['win'][1] and o['win'][2])
    return st


def classify_island(st, counts_i, audit):
    """behavioural class (priority pair, items deviate, P deviates, truthful, mixed) and the overlap flags."""
    if st['joint'] >= 0.5:
        cls = 'pair'
    elif st['items_dev'] >= 0.5:
        cls = 'items_dev'
    elif st['p_dev'] >= 0.5:
        cls = 'p_dev'
    elif st['truthful'] >= 0.5:
        cls = 'truthful'
    else:
        cls = 'mixed'
    pol = bool(counts_i[2, 1] == counts_i[2].sum()) and not audit
    pair_enf = bool(counts_i[0, 2] == counts_i[0].sum() and counts_i[1, 2] == counts_i[1].sum()) and not audit
    pair_unenf = bool(counts_i[0, 3] == counts_i[0].sum() and counts_i[1, 3] == counts_i[1].sum())
    return dict(cls=cls, policed=pol, pair_enforced=pair_enf, pair_unenforced=pair_unenf, items_dev=bool(st['items_dev'] >= 0.5))
