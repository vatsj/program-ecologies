"""Two-population attractor chain for a fixed-role game.

Population P plays role 0 (proposer), population R role 1 (responder); each
program only ever meets the other population.  Given the other population's
type, fitness inside a population is frequency-independent, so every
attractor is monomorphic (a neutral tie is split by drift at 1/N) and the
state is a pair (p, q) of class representatives.  A mutation event picks a
population with probability 1/2, draws a mutant m from that population's
mu, and m fixes with the Moran probability at constant fitness ratio
exp(w * (u_m - u_incumbent)).  pi is the stationary distribution over pairs
on the flow-pruned expanded set (reflecting boundary), as in chain.Chain.

Arm (b) fixed-mutual: both populations use the full weak grammar.
Arm (c) fixed-one-sided: R uses the blind grammar (no THEM, no application,
no eq); P sees R.
"""
import numpy as np
import scipy.sparse as sp
from collections import defaultdict
from dsl import Language, CONST, X, ROLE, NOT, AND, OR, APP, EQ, NONE
from evaluate import evaluate, keys_of
from chain import fixation


def map_language(sub, full):
    """Ids in `full` of every program of `sub` (same grammar family, sub a
    restriction), by structural interning; sub.op/lhs/rhs are the term arrays."""
    ids = np.empty(sub.n_enum, np.int64)
    for i in range(sub.n_enum):
        op, l, r, sz = int(sub.op[i]), int(sub.lhs[i]), int(sub.rhs[i]), int(sub.size[i])
        if op in (NOT, AND, OR):
            l = int(ids[l]); r = int(ids[r]) if r >= 0 else r
        elif op in (APP, EQ):
            l = int(ids[l]) if l >= 0 else l; r = int(ids[r]) if r >= 0 else r
        ids[i] = full.intern(op, l, r, sz)
    full._grow()
    return ids


class TwoPop:
    def __init__(self, game, full, P_ids, R_ids, muP, muR, N, w, theta=1e-6, max_states=20000, max_rounds=60,
                 tol=1e-11, round_dec=9, verbose=False):
        self.g, self.L, self.N, self.w = game, full, N, w
        self.theta, self.max_states, self.max_rounds, self.verbose = theta, max_states, max_rounds, verbose
        P_ids = np.asarray(P_ids); R_ids = np.asarray(R_ids)
        S = full.count
        I = np.repeat(P_ids, len(R_ids)); J = np.tile(R_ids, len(P_ids))
        keys = np.union1d(keys_of(S, I, J, 0), keys_of(S, J, I, 1))
        res = evaluate(full, game, keys, tol=tol)
        self.res = res
        self.div_rate = float(res.div.mean())
        VP = res.V[res.index(I, J, 0)]            # proposer i vs responder j: offer distribution
        VR = res.V[res.index(J, I, 1)]            # responder j vs proposer i: threshold distribution
        nP, nR = len(P_ids), len(R_ids)
        self.UP = np.round(np.einsum('na,ab,nb->n', VP, game.pay[0], VR).reshape(nP, nR), round_dec)   # proposer payoff [i, j]
        self.UR = np.round(np.einsum('nb,ba,na->n', VR, game.pay[1], VP).reshape(nP, nR), round_dec)   # responder payoff [i, j]
        self.REJ = np.einsum('na,ab,nb->n', VP, game.reject, VR).reshape(nP, nR) if game.reject is not None else np.zeros((nP, nR))
        self.VP = VP.reshape(nP, nR, game.k); self.VR = VR.reshape(nP, nR, game.k)
        self.P_ids, self.R_ids = P_ids, R_ids
        # behavioural classes: proposer by (UP[i,:], UR[i,:]); responder by (UP[:,j], UR[:,j])
        self.Pc = self._classes(np.concatenate([np.round(self.UP, 6), np.round(self.UR, 6)], axis=1), P_ids, muP)
        self.Rc = self._classes(np.concatenate([np.round(self.UP, 6).T, np.round(self.UR, 6).T], axis=1), R_ids, muR)
        self.Pi = {int(p): k for k, p in enumerate(P_ids)}; self.Ri = {int(q): k for k, q in enumerate(R_ids)}
        self.states = {}; self.trans = {}; self.trans_mut = defaultdict(dict); self.edge_rho = {}

    def _classes(self, sig, ids, mu):
        groups = defaultdict(list)
        for k in range(len(ids)):
            groups[sig[k].tobytes()].append(int(ids[k]))
        classes = []
        for members in groups.values():
            rep = min(members, key=lambda p: (self.L.bits[p] if p < self.L.n_enum else 1e9, p))
            classes.append((rep, members, float(sum(mu[m] for m in members))))
        classes.sort(key=lambda c: -c[2])
        z = sum(c[2] for c in classes)
        return [(r, m, wgt / z) for r, m, wgt in classes]

    # -- states
    def key(self, p, q):
        k = (int(p), int(q))
        self.states[k] = k
        return k

    def expand(self, key):
        if key in self.trans: return
        p, q = key
        ip, jq = self.Pi[p], self.Ri[q]
        out = defaultdict(float); muts = {}
        N, w = self.N, self.w
        up0 = float(self.UP[ip, jq]); ur0 = float(self.UR[ip, jq])
        stay = 0.0
        for rep, members, m in self.Pc:                       # proposer mutation (prob 1/2)
            if rep == p:
                stay += 0.5 * m; continue
            um = float(self.UP[self.Pi[rep], jq])
            rho = fixation(um, um, up0, up0, N, w, N)
            k2 = self.key(rep, q)
            out[k2] += 0.5 * m * rho; muts[k2] = (rep, 'P', rho, m); stay += 0.5 * m * (1 - rho)
        for rep, members, m in self.Rc:                       # responder mutation (prob 1/2)
            if rep == q:
                stay += 0.5 * m; continue
            um = float(self.UR[ip, self.Ri[rep]])
            rho = fixation(um, um, ur0, ur0, N, w, N)
            k2 = self.key(p, rep)
            out[k2] += 0.5 * m * rho; muts[k2] = (rep, 'R', rho, m); stay += 0.5 * m * (1 - rho)
        out[key] += stay
        self.trans[key] = dict(out)
        for k2, info in muts.items():
            self.trans_mut[(key, k2)] = info

    def explore(self, seeds=None):
        if seeds is None:
            seeds = [(self.key(p, q), mp * mq) for p, _, mp in self.Pc[:12] for q, _, mq in self.Rc[:12]]
        self.seed_weight = dict(seeds)
        queue = [k for k, _ in seeds]
        self.cut_flow = 0.0
        for rnd in range(self.max_rounds):
            while queue and len(self.trans) < self.max_states:
                k = queue.pop()
                if k in self.trans: continue
                self.expand(k)
                row = self.trans[k]
                nonself = [(v, b) for b, v in row.items() if b != k]
                if nonself:
                    top = max(nonself)[1]
                    if top not in self.trans: queue.append(top)
            pi = self.stationary()
            flow = defaultdict(float)
            for k, pk in zip(self.keys_list, pi):
                for b, v in self.trans[k].items():
                    if b not in self.trans: flow[b] += pk * v
            cand = [b for b, f in flow.items() if f > self.theta]
            self.cut_flow = sum(f for b, f in flow.items() if f <= self.theta)
            if self.verbose:
                print('  round %d: %d expanded, %d candidates, cut flow %.2e' % (rnd, len(self.trans), len(cand), self.cut_flow), flush=True)
            if not cand or len(self.trans) >= self.max_states: break
            queue = sorted(cand, key=lambda b: flow[b])
        return self

    def stationary(self):
        keys = list(self.trans); idx = {k: n for n, k in enumerate(keys)}; n = len(keys)
        rows, cols, vals = [], [], []
        for a in keys:
            kept = {b: v for b, v in self.trans[a].items() if b in idx}
            z = sum(kept.values())
            for b, v in kept.items():
                rows.append(idx[a]); cols.append(idx[b]); vals.append(v / z)
        P = sp.csr_matrix((vals, (rows, cols)), shape=(n, n))
        A = (P.T - sp.eye(n)).tolil(); A[n - 1, :] = 1.0
        b = np.zeros(n); b[n - 1] = 1.0
        try:
            pi = sp.linalg.spsolve(A.tocsc(), b)
        except Exception:
            pi = np.linalg.lstsq(A.toarray(), b, rcond=None)[0]
        pi = np.clip(pi, 0, None); pi /= pi.sum()
        self.keys_list, self.pi, self.Pmat = keys, pi, P
        return pi

    # -- stats
    def state_stats(self, key):
        p, q = key; ip, jq = self.Pi[p], self.Ri[q]
        return dict(reject=float(self.REJ[ip, jq]), share_P=float(self.UP[ip, jq]), share_R=float(self.UR[ip, jq]),
                    offer=self.VP[ip, jq].tolist(), threshold=self.VR[ip, jq].tolist())

    def describe(self, key):
        p, q = key
        return '(%s | %s)' % (self.L.src(p), self.L.src(q))

    def support(self, thresh=1e-4):
        order = np.argsort(-self.pi)
        return [(self.keys_list[k], float(self.pi[k])) for k in order if self.pi[k] > thresh]

    def report(self, cfg, top=12):
        pi = dict(zip(self.keys_list, self.pi))
        L = self.L
        lines = ['### %s' % ', '.join('%s=%s' % kv for kv in cfg.items()), '']
        rej = sum(pi[k] * self.state_stats(k)['reject'] for k in pi)
        sP = sum(pi[k] * self.state_stats(k)['share_P'] for k in pi); sR = sum(pi[k] * self.state_stats(k)['share_R'] for k in pi)
        lines.append('proposer programs %d (%d classes), responder programs %d (%d classes), states expanded %d, cut flow %.1e, divergence rate %.4f' % (
            len(self.P_ids), len(self.Pc), len(self.R_ids), len(self.Rc), len(self.trans), self.cut_flow, self.div_rate))
        lines.append('on-path rejection rate %.4f, proposer share %.4f, responder share %.4f (pi-weighted)' % (rej, sP, sR))
        cond = [(k, w_) for k, w_ in self.support(1e-3) if 'THEM' in L.src(k[0]) or 'THEM' in L.src(k[1])]
        lines.append('conditional programs in the support (pi > 1e-3): %s' % (', '.join('%s %.3f' % (self.describe(k), w_) for k, w_ in cond[:8]) if cond else 'none'))
        lines.append(''); lines.append('| pi | proposer | responder | reject | share P | share R | offer dist | threshold dist |'); lines.append('|---|---|---|---|---|---|---|---|')
        for k, w_ in self.support(1e-4)[:top]:
            st = self.state_stats(k)
            lines.append('| %.4f | `%s` | `%s` | %.3f | %.3f | %.3f | %s | %s |' % (w_, L.src(k[0]), L.src(k[1]), st['reject'], st['share_P'], st['share_R'], np.round(st['offer'], 2).tolist(), np.round(st['threshold'], 2).tolist()))
        lines.append(''); lines.append('Transitions out of the top states (P per mutation event; mutant, population, rho, mu):'); lines.append('')
        for k, w_ in self.support(1e-4)[:6]:
            lines.append('- %s' % self.describe(k))
            for b, v in sorted(((v, b) for b, v in self.trans[k].items() if b != k), reverse=True)[:4]:
                pass
            for v, b in sorted(((v, b) for b, v in self.trans[k].items() if b != k), reverse=True)[:4]:
                rep, pop, rho, m = self.trans_mut[(k, b)]
                lines.append('    - %.2e -> %s via `%s` in %s (rho %.2e, mu %.2e)' % (v, self.describe(b), L.src(rep), pop, rho, m))
        lines.append('')
        return '\n'.join(lines), dict(reject=rej, share_P=sP, share_R=sR, n_states=len(self.trans), cut_flow=self.cut_flow,
                                      support=[(self.describe(k), w_) for k, w_ in self.support(1e-4)[:top]], conditional=[(self.describe(k), w_) for k, w_ in cond[:8]])


def build(game, n, arm, N, w, verbose=False, **kw):
    """arm 'mutual': both populations weak; 'onesided': responder blind."""
    full = Language('weak', n, k=game.k, names=game.actions)
    P_ids = full.ids(); muP = {int(p): float(full.mu[p]) for p in P_ids}
    if arm == 'mutual':
        R_ids = P_ids; muR = muP
    else:
        blind = Language('blind', n, k=game.k, names=game.actions)
        R_ids = map_language(blind, full)
        muR = {int(r): float(blind.mu[i]) for i, r in enumerate(R_ids)}
    return TwoPop(game, full, P_ids, R_ids, muP, muR, N, w, verbose=verbose, **kw)
