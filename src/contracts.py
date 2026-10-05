"""Proof-carrying contracts v1 (specs/2026-10-04-proof-carrying-contracts.md).

Sources are modal programs (src/modal.py) at n = 8, one per canonical function
(610).  A *contract* is the signature of a source over the contract alphabet:
the carrier's stable action against a carrier of each contract.  The 'none'
entry is unspecified (a contract says nothing about play against contract-less
opponents), so a question it would answer is read from source.

Contract-level self-reference (resolved as in the certificates-only Löb arm:
contract-level statements are provability atoms).  Reading contracts as bare
truth tables is paradoxical: FairBot's table against the anti-FairBot
BOXD(THEM(ME)) must satisfy T[FB, q] = T[q, FB] and T[q, FB] = not T[FB, q]; the
synchronous all-carrier table iteration from the GL play cycles with period 4
and 58,996 of 372,100 entries varying (measured; see `truth_table_diagnostic`).
So a contract is read through GL: the contract alphabet is the set of
behavioural classes of the free modal game (stable row and column identical,
471 at n = 8), each represented by its shortest source (its canonical proof),
and a box atom answered from contracts is the free GL box over the canonical
representatives' trace: BOX_L(u plays C vs tau) with u, tau carriers is
hc_free[L, rep(c_u), rep(c_tau)] (C at every world >= L), BOXD likewise with
hd.  No gate applies to contract reads (checking is cheap; amortized
verification, THEORY 9.2).

Validity: (p, c) is valid iff for every contract d the evaluator's action of p
carrying c against a carrier of d equals c's stable action against d,
S[c, d].  Carrier-carrier play reads contracts only, so validity depends on
(p, c) alone and is not recursive.  Policy duplicates: 14 stable rows are
shared by two or more classes whose columns differ (others treat them
differently through provability); they stay distinct contracts.

One evaluator over types t = (source p, contract c or -1).  Reader t meets
opponent u; each box atom of p names a target tau: t (THEM(ME)), u (THEM(THEM))
or a literal A (THEM(^A)).  The literal is the carrier (A, class(A)) when u
carries a contract (a question to u's contract) and the bare source (A, none)
otherwise.  If u and tau both carry contracts the atom is the contract-level
box above.  Otherwise it is the GL box over u's actual play toward tau at
earlier worlds, masked by the legibility gate: illegible (v(t, u) = k(u) *
(1 + settle(u, t)) > b) => false.  The gate is a joint fixed point: start from
the ungated play, compute v from the current play's settle worlds, re-evaluate,
until the mask is stable.
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import modal as M
from modal import TM, TT, TL, KC, KD, PD
from abm import njit

INF = 10 ** 9
FB = 'BOX(THEM(ME))'
PSTAR = 'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))'
PB = 'and(BOX(THEM(ME)),BOXD1(THEM(^D)))'


# ------------------------------------------------------------------ GL over types (with contract reads and the gate)
@njit(cache=True)
def _eval_types(nat, ak, al, af, aa, tt, src, con, nc_type, cs_type, rep, BC, BD, mask, max_worlds):
    """src[t], con[t] (-1 = none).  nc_type[canon] = type (canon, none); cs_type[canon] = type
    (canon, class(canon)) or -1 if that pair is not a type.  rep[c] = canonical representative of
    contract c; BC[L, x, y] / BD[L, x, y]: free-GL stable boxes over canonical sources.
    mask[t, u] = 1 iff t may read u's source.  Returns val, worlds, last, hc, hd, ntab, nsrc where
    last[t, u] is the last world at which t's atom values against u changed."""
    NT = src.shape[0]
    hc = np.ones((2, NT, NT), np.bool_)
    hd = np.ones((2, NT, NT), np.bool_)
    val = np.zeros((NT, NT), np.int8)
    prev = -np.ones((NT, NT), np.int64)
    last = np.zeros((NT, NT), np.int64)
    for n in range(max_worlds):
        for t in range(NT):
            p = src[t]
            for u in range(NT):
                idx = 0
                for j in range(nat[p]):
                    f = af[p, j]
                    if f == 0:
                        tg = t
                    elif f == 1:
                        tg = u
                    else:
                        a = aa[p, j]
                        tg = cs_type[a] if con[u] >= 0 else nc_type[a]
                    L = al[p, j]
                    if con[u] >= 0 and con[tg] >= 0:
                        x = rep[con[u]]; y = rep[con[tg]]
                        b = BC[L, x, y] if ak[p, j] == 0 else BD[L, x, y]
                    elif mask[t, u] == 0:
                        b = False
                    else:
                        b = hc[L, u, tg] if ak[p, j] == 0 else hd[L, u, tg]
                    if b: idx |= 1 << j
                if prev[t, u] >= 0 and idx != prev[t, u]:
                    last[t, u] = n
                prev[t, u] = idx
                val[t, u] = (tt[p] >> idx) & 1
        changed = False
        for L in range(2):
            if n < L:
                continue
            for x in range(NT):
                for y in range(NT):
                    c = val[x, y] == 1
                    if hc[L, x, y] and not c:
                        hc[L, x, y] = False; changed = True
                    if hd[L, x, y] and c:
                        hd[L, x, y] = False; changed = True
        if not changed and n >= 2:
            return val, n, last, hc, hd
    return val, -1, last, hc, hd


@njit(cache=True)
def _validity(nat, ak, al, af, aa, tt, cls, rep, BC, BD, S, valid, act):
    """valid[p, c] = 1 iff source p carrying contract c plays S[c, d] against every contract d.
    act[p, c, d] = that action (for the compatibility report)."""
    K = nat.shape[0]; NC = S.shape[0]
    for p in range(K):
        for c in range(NC):
            ok = 1
            for d in range(NC):
                idx = 0
                for j in range(nat[p]):
                    f = af[p, j]
                    if f == 0:
                        tg = c
                    elif f == 1:
                        tg = d
                    else:
                        tg = cls[aa[p, j]]
                    L = al[p, j]
                    x = rep[d]; y = rep[tg]
                    b = BC[L, x, y] if ak[p, j] == 0 else BD[L, x, y]
                    if b: idx |= 1 << j
                a = (tt[p] >> idx) & 1
                act[p, c, d] = a
                if a != S[c, d]:
                    ok = 0
            valid[p, c] = ok


class Contracts:
    """Language, free GL play, contract alphabet, validity matrix, types."""
    def __init__(self, n=8):
        self.L = L = M.ModalLanguage(n)
        self.arr = L.arrays()
        nat, ak, al, af, aa, tt = self.arr
        K = self.K = len(nat)
        self.names = list(L.rep)
        self.mu = L.mu_canon / L.mu_canon.sum()
        self.k = nat.astype(np.int64)
        # free GL over canonical sources (non-carrier types only, no gate)
        src = np.arange(K, dtype=np.int64); con = -np.ones(K, np.int64)
        dummy = np.zeros((2, 1, 1), np.bool_)
        val, worlds, last, hc, hd = _eval_types(nat, ak, al, af, aa, tt, src, con, src, -np.ones(K, np.int64),
                                               np.zeros(1, np.int64), dummy, dummy, np.ones((K, K), np.int8), 200)
        assert worlds >= 0
        v2, w2 = M.evaluate(L)
        assert (v2 == val).all(), 'free GL over types must equal modal.evaluate'
        self.val0 = val; self.worlds0 = worlds; self.last0 = last
        self.BC = hc; self.BD = hd
        # contracts = behavioural classes of the free game
        key = {}; cls = np.zeros(K, np.int64)
        for p in range(K):
            cls[p] = key.setdefault((val[p].tobytes(), val[:, p].tobytes()), len(key))
        self.NC = NC = len(key); self.cls = cls
        rep = np.zeros(NC, np.int64); best = np.full(NC, np.inf)
        for p in range(K):
            if L.bits_canon[p] < best[cls[p]]:
                best[cls[p]] = L.bits_canon[p]; rep[cls[p]] = p
        self.rep = rep
        self.S = val[np.ix_(rep, rep)].astype(np.int8)
        self.cname = ['<%s>' % self.names[rep[c]] for c in range(NC)]
        rows = {}
        for c in range(NC): rows.setdefault(self.S[c].tobytes(), []).append(c)
        self.policy_dups = [v for v in rows.values() if len(v) > 1]
        self.valid = None

    def contract_of(self, src_name):
        return int(self.cls[self.names.index(src_name)])

    def compute_validity(self):
        nat, ak, al, af, aa, tt = self.arr
        valid = np.zeros((self.K, self.NC), np.int8)
        act = np.zeros((self.K, self.NC, self.NC), np.int8)
        _validity(nat, ak, al, af, aa, tt, self.cls, self.rep, self.BC, self.BD, self.S, valid, act)
        self.valid = valid; self.act = act
        return valid

    def build_types(self):
        K = self.K
        src = list(range(K)); con = [-1] * K
        cs_type = -np.ones(K, np.int64)
        for p, c in np.argwhere(self.valid == 1):
            t = len(src); src.append(int(p)); con.append(int(c))
            if c == self.cls[p]:
                cs_type[p] = t
        self.tsrc = np.array(src, np.int64); self.tcon = np.array(con, np.int64)
        self.nc_type = np.arange(K, dtype=np.int64); self.cs_type = cs_type
        self.NT = len(src)
        self.tindex = {(int(s), int(c)): t for t, (s, c) in enumerate(zip(self.tsrc, self.tcon))}
        # literal targets with an invalid own pair: the carrier (A, class(A)) is not a type.  Count them.
        lits = {int(a) for p in range(K) for j in range(self.arr[0][p]) if self.arr[3][p, j] == TL for a in [self.arr[4][p, j]]}
        self.literal_without_own_carrier = sorted(a for a in lits if cs_type[a] < 0)
        return self.NT

    def evaluate(self, b, max_rounds=60):
        """Joint fixed point of the legibility gate at budget b (INF = free box).  Returns val over types and info."""
        nat, ak, al, af, aa, tt = self.arr
        NT = self.NT
        cs = self.cs_type.copy()
        # a literal whose own carrier is not a type: fall back to a carrier of its class via any valid source
        for a in self.literal_without_own_carrier:
            c = self.cls[a]
            alt = [t for t in range(self.K, NT) if self.tcon[t] == c]
            cs[a] = alt[0] if alt else -1
        if (cs[[a for a in self.literal_without_own_carrier]] < 0).any() if self.literal_without_own_carrier else False:
            raise RuntimeError('a literal class has no valid carrier')
        self._cs_eval = cs
        mask = np.ones((NT, NT), np.int8)
        seen = {}; changes = []
        kt = self.k[self.tsrc]
        for r in range(max_rounds):
            val, worlds, last, hc, hd = _eval_types(nat, ak, al, af, aa, tt, self.tsrc, self.tcon, self.nc_type, cs,
                                                     self.rep, self.BC, self.BD, mask, 200)
            if worlds < 0:
                raise RuntimeError('type evaluation did not stabilize')
            if b >= INF:
                return val, dict(rounds=1, cycle=False, worlds=int(worlds), masked=0), (last, hc, hd, mask)
            cost = kt[None, :] * (1 + last.T)          # cost[t, u] = k(u) * (1 + settle(u, t))
            new = (cost <= b).astype(np.int8)
            changes.append(int((new != mask).sum()))
            if (new == mask).all():
                return val, dict(rounds=r + 1, cycle=False, worlds=int(worlds), masked=int((mask == 0).sum()), changes=changes), (last, hc, hd, mask)
            h = new.tobytes()
            if h in seen:
                mask = np.minimum(mask, new)
                val, worlds, last, hc, hd = _eval_types(nat, ak, al, af, aa, tt, self.tsrc, self.tcon, self.nc_type, cs,
                                                         self.rep, self.BC, self.BD, mask, 200)
                return val, dict(rounds=r + 1, cycle=True, worlds=int(worlds), masked=int((mask == 0).sum()), changes=changes), (last, hc, hd, mask)
            seen[h] = r
            mask = new
        raise RuntimeError('gate iteration did not settle')


def truth_table_diagnostic(C):
    """Synchronous all-carrier truth-table iteration from the GL play: period and divergent entries."""
    nat, ak, al, af, aa, tt = C.arr
    K = C.K
    T = C.val0.astype(np.int8).copy(); seen = {T.tobytes(): 0}
    for it in range(1, 500):
        out = np.empty_like(T)
        for p in range(K):
            for q in range(K):
                idx = 0
                for j in range(nat[p]):
                    tg = p if af[p, j] == TM else (q if af[p, j] == TT else aa[p, j])
                    v = T[q, tg]
                    if (v == 1) if ak[p, j] == KC else (v == 0): idx |= 1 << j
                out[p, q] = (tt[p] >> idx) & 1
        T = out; h = T.tobytes()
        if h in seen:
            per = it - seen[h]
            lo = T.copy(); hi = T.copy(); w = T.copy()
            for _ in range(per):
                o2 = np.empty_like(w)
                for p in range(K):
                    for q in range(K):
                        idx = 0
                        for j in range(nat[p]):
                            tg = p if af[p, j] == TM else (q if af[p, j] == TT else aa[p, j])
                            v = w[q, tg]
                            if (v == 1) if ak[p, j] == KC else (v == 0): idx |= 1 << j
                        o2[p, q] = (tt[p] >> idx) & 1
                w = o2; lo = np.minimum(lo, w); hi = np.maximum(hi, w)
            return dict(iters=it, period=per, divergent=int((lo != hi).sum()), entries=K * K)
        seen[h] = it
    return None


# ------------------------------------------------------------------ audit: certified implications vs actual play
@njit(cache=True)
def _audit(nat, ak, al, af, aa, tt, src, con, nc_type, cs_type, rep, BC, BD, mask, hc, hd, val, S):
    """Re-derive every atom at the stable world.  Counts: [contract reads, contract reads whose box is true,
    violations (box true but the opponent's actual play toward the target differs), source reads (legible),
    source reads masked, source boxes true, source violations, carrier pairs, carrier pairs off-table,
    recomputed action != val]."""
    NT = src.shape[0]
    out = np.zeros(10, np.int64)
    for t in range(NT):
        p = src[t]
        for u in range(NT):
            if con[t] >= 0 and con[u] >= 0:
                out[7] += 1
                if val[t, u] != S[con[t], con[u]]:
                    out[8] += 1
            idx = 0
            for j in range(nat[p]):
                f = af[p, j]
                if f == 0:
                    tg = t
                elif f == 1:
                    tg = u
                else:
                    a = aa[p, j]
                    tg = cs_type[a] if con[u] >= 0 else nc_type[a]
                L = al[p, j]
                want = 1 if ak[p, j] == 0 else 0
                if con[u] >= 0 and con[tg] >= 0:
                    x = rep[con[u]]; y = rep[con[tg]]
                    b = BC[L, x, y] if ak[p, j] == 0 else BD[L, x, y]
                    out[0] += 1
                    if b:
                        out[1] += 1
                        if val[u, tg] != want:
                            out[2] += 1
                elif mask[t, u] == 0:
                    b = False
                    out[4] += 1
                else:
                    b = hc[L, u, tg] if ak[p, j] == 0 else hd[L, u, tg]
                    out[3] += 1
                    if b:
                        out[5] += 1
                        if val[u, tg] != want:
                            out[6] += 1
                if b: idx |= 1 << j
            if ((tt[p] >> idx) & 1) != val[t, u]:
                out[9] += 1
    return out


def audit(C, val, aux):
    last, hc, hd, mask = aux
    nat, ak, al, af, aa, tt = C.arr
    o = _audit(nat, ak, al, af, aa, tt, C.tsrc, C.tcon, C.nc_type, C._cs_eval, C.rep, C.BC, C.BD, mask, hc, hd, val, C.S)
    keys = ['contract_reads', 'contract_box_true', 'contract_violations', 'source_reads_legible', 'source_reads_masked',
            'source_box_true', 'source_violations', 'carrier_pairs', 'carrier_pairs_off_table', 'recompute_mismatch']
    return {k: int(v) for k, v in zip(keys, o)}


if __name__ == '__main__':
    import time
    t = time.time()
    C = Contracts(8)
    print('n = 8: programs %d, canonical sources %d, free GL worlds %d' % (C.L.n_programs, C.K, C.worlds0))
    print('contract alphabet |C| = %d behavioural classes; policy duplicates: %d rows shared by %d classes' % (
        C.NC, len(C.policy_dups), sum(len(v) for v in C.policy_dups)))
    print('%.1fs' % (time.time() - t))
