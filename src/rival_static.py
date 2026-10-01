"""Static quantities for predictions/2026-10-01-rival-networks.md (no simulation).

Lazy-priced modal arm, n = 8, PD, w = 0.3.  P* = and(BOX1(THEM(ME)),not(BOX(THEM(ME)))),
FB = BOX(THEM(ME)).  Prints:
  1. the payoff blocks of every requested pair, and which are identical across c;
  2. network membership and prior mass (FB-net, P*-net: mutual cooperators that defect on D);
  3. well-mixed hitting-half and fixation probabilities at the graph sizes;
  4. the first-order flat-border drift on the torus and the biased-random-walk
     estimate of P(FB reaches 3/4 before P* does) from a half split;
  5. the well-mixed birth-death probability of the same event;
  6. a four-state reduced chain {D, ALLC, FB-net, P*-net} with well-mixed rates.

    python3 src/rival_static.py
"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import modal as M
from chain import fixation

W = 0.3
PS = 'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))'
FB = 'BOX(THEM(ME))'
NS = (64, 256, 1024, 4096)


def load(c):
    """Lazy-priced n = 8 provider, with ACT[i, j] = 1 iff class i plays C against class j."""
    L, val, worlds, prov = M.build_priced(8, c, pricing='lazy')
    rep = [m[0] for m in prov.members]
    prov.ACT = val[np.ix_(rep, rep)].astype(np.int64)
    return prov


def networks(prov):
    U, A = prov.Ufull, prov.ACT
    names = prov.names; g = names.index
    iD, iC, iF, iP = g('D'), g('C'), g(FB), g(PS)
    mu = np.array([cl[2] for cl in prov.classes])
    K = len(names)
    mutual = lambda x, y: A[x, y] == 1 and A[y, x] == 1
    lab = np.full(K, 'other', object)
    for x in range(K):
        if A[x, x] == 0:
            lab[x] = 'D-type'                       # defects against a copy of itself
        elif A[x, iD] == 1:
            lab[x] = 'exploitable'                  # self-cooperator that cooperates with D (ALLC and kin)
        elif mutual(x, iF):
            lab[x] = 'FB-net'
        elif mutual(x, iP):
            lab[x] = 'P*-net'
        else:
            lab[x] = 'other-coop'
    return dict(iD=iD, iC=iC, iF=iF, iP=iP, mu=mu, lab=lab)


def block(U, q, r):
    return (U[q, q], U[q, r], U[r, q], U[r, r])


def wm(U, q, r, N, kstar):
    return fixation(U[q, q], U[q, r], U[r, q], U[r, r], N, W, kstar)


def db_complete(U, q, r, N, kstar):
    """Death-birth on the complete graph (the graph kernel's rule, payoffs evaluated before the
    dying site is replaced): P(single q reaches kstar before 0) against resident r."""
    w = W
    def fm(k): return np.exp(w * ((k - 1) / (N - 1) * U[q, q] + (N - k) / (N - 1) * U[q, r]))
    def fr(k): return np.exp(w * (k / (N - 1) * U[r, q] + (N - k - 1) / (N - 1) * U[r, r]))
    logs = [0.0]; acc = 0.0
    for k in range(1, kstar):
        up = (N - k) / N * k * fm(k) / (k * fm(k) + (N - k - 1) * fr(k))
        dn = k / N * (N - k) * fr(k) / ((k - 1) * fm(k) + (N - k) * fr(k))
        acc += np.log(dn) - np.log(up); logs.append(acc)
    logs = np.array(logs)                    # j = 0 .. kstar-1: log prod_{k<=j} dn/up
    m = logs.max()
    return float(np.exp(-m) / np.exp(logs - m).sum())


def bd_hit(U, a, b, N, k0, lo, hi):
    """Well-mixed Moran (birth-death, exp fitness): count k of type a against b.
    P(k reaches hi before lo | k0)."""
    def gam(k):   # f_b / f_a at k copies of a
        pa = (k - 1) / (N - 1) * U[a, a] + (N - k) / (N - 1) * U[a, b]
        pb = k / (N - 1) * U[b, a] + (N - k - 1) / (N - 1) * U[b, b]
        return W * (pb - pa)
    logs = [0.0]; acc = 0.0
    for k in range(lo + 1, hi):
        acc += gam(k); logs.append(acc)
    logs = np.array(logs); m = logs.max()
    num = np.exp(logs[:k0 - lo] - m).sum(); den = np.exp(logs - m).sum()
    return num / den


def flat_border(c):
    """First-order flat-border drift on the torus (death-birth, mean payoff over 4 neighbours).
    Border sites have one cross neighbour.  FB pays (1 + 2c) per P* neighbour, P* pays (1 + 6c)."""
    f, p = -(1 + 2 * c) / 4, -(1 + 6 * c) / 4
    ef, ep = np.exp(W * f), np.exp(W * p)
    p_fb_fills = ef / (ef + 2 * ep + 1)          # a P* border site dies: its FB neighbour wins
    p_ps_fills = ep / (ep + 2 * ef + 1)          # an FB border site dies: its P* neighbour wins
    return p_fb_fills, p_ps_fills


def walk_estimate(c, side):
    """Biased random walk for the FB count from a half split with two straight borders,
    absorbing at N/4 and 3N/4: P(up first) = 1 / (1 + exp(-2 m a / s2))."""
    pf, pp = flat_border(c)
    m = 2 * side * (pf - pp)           # mean count change per generation (two borders)
    s2 = 2 * side * (pf + pp)          # variance per generation
    a = side * side / 4
    x = 2 * m * a / s2
    T = a / m if m > 0 else float('inf')
    return 1 / (1 + np.exp(-x)), (pf - pp), T


def reduced_chain(rates, mu):
    """Four-state chain over D, C, FBnet, PSnet; rates[(r, q)] = per-mutant fixation
    probability of q into all-r; transition weight mu[q] * rates.  Returns pi."""
    S = ['D', 'C', 'FB', 'PS']
    T = np.zeros((4, 4))
    for i, r in enumerate(S):
        for j, q in enumerate(S):
            if i != j:
                T[i, j] = mu[q] * rates.get((r, q), 0.0)
    for i in range(4):
        T[i, i] = 1 - T[i].sum()
    w, v = np.linalg.eig(T.T)
    k = np.argmin(abs(w - 1)); pi = np.real(v[:, k]); pi = pi / pi.sum()
    return dict(zip(S, pi))


def main():
    out = {}
    blocks = {}
    for c in (0.0, 0.01, 0.1):
        prov = load(c); U = prov.Ufull; names = prov.names
        nw = networks(prov); mu = nw['mu']; lab = nw['lab']
        iD, iC, iF, iP = nw['iD'], nw['iC'], nw['iF'], nw['iP']
        print('\n===== c = %g: %d classes' % (c, len(names)))
        pairs = {'P*|FB': (iP, iF), 'FB|P*': (iF, iP), 'ALLC|FB': (iC, iF), 'ALLC|P*': (iC, iP),
                 'D|FB': (iD, iF), 'D|P*': (iD, iP), 'FB|D': (iF, iD), 'P*|D': (iP, iD), 'D|ALLC': (iD, iC)}
        for k, (q, r) in pairs.items():
            b = tuple(np.round(block(U, q, r), 6)); blocks.setdefault(k, {})[c] = b
        # networks
        tot = {}
        for x in range(len(names)):
            tot[lab[x]] = tot.get(lab[x], 0.0) + mu[x]
        cnt = {l: int((lab == l).sum()) for l in set(lab)}
        print('network mass:', {l: '%.4g (%d classes)' % (tot[l], cnt[l]) for l in sorted(tot)})
        ent = (np.abs(U[:, iD] - U[iD, iD]) < 1e-12) & (np.abs(U[iD, :] - U[iD, iD]) < 1e-12) & (np.abs(np.diag(U) - 0) < 1e-12)
        mFB = mu[ent & (lab == 'FB-net')].sum(); mPS = mu[ent & (lab == 'P*-net')].sum(); mOT = mu[ent & (lab == 'other-coop')].sum()
        print('entrants with FB|D block (0,-1,-1,-1): FB-net mu %.4g, P*-net mu %.4g, other-coop mu %.4g' % (mFB, mPS, mOT))
        print('  P*-net entrants:', [(names[x], '%.2e' % mu[x]) for x in np.where(ent & (lab == 'P*-net'))[0]][:10])
        print('  other-coop entrants (top):', [(names[x], '%.2e' % mu[x]) for x in sorted(np.where(ent & (lab == 'other-coop'))[0], key=lambda x: -mu[x])][:6])
        print('mu: D %.4f C %.4f FB %.3e P* %.3e' % (mu[iD], mu[iC], mu[iF], mu[iP]))
        # well-mixed rates
        rows = []
        for k, (q, r) in pairs.items():
            hh = [wm(U, q, r, N, N // 2) for N in NS]; fx = [wm(U, q, r, N, N) for N in NS]
            rows.append((k, hh, fx))
            print('%-8s block %s  well-mixed hit-half %s  fixation %s' % (k, blocks[k][c], ' '.join('%.2e' % v for v in hh), ' '.join('%.2e' % v for v in fx)))
        # flat border + walk
        pf, pp = flat_border(c)
        print('flat border: P(FB fills P* border site) %.6f, P(P* fills FB border site) %.6f, drift %.2e rows/gen' % (pf, pp, pf - pp))
        for side in (16, 32, 64):
            P, v, T = walk_estimate(c, side)
            N = side * side
            print('  torus %d: walk P(FB to 3/4 first) %.3f, time to 3/4 %.0f gen; well-mixed BD P(FB to 3N/4 first) %.3f; initial interface MD-edge fraction %.4f' % (
                side, P, T, bd_hit(U, iF, iP, N, N // 2, N // 4, 3 * N // 4), 1 / side))
        for d in (6, 8, 10):
            N = 1 << d
            print('  hypercube %d: well-mixed BD P(FB to 3N/4 first) %.3f at N = %d; initial interface MD-edge fraction %.4f' % (d, bd_hit(U, iF, iP, N, N // 2, N // 4, 3 * N // 4), N, 1 / d))
        out[c] = dict(mu_FBnet_entry=mFB, mu_PSnet_entry=mPS, mu_other_entry=mOT, mass=tot, counts=cnt,
                      wm=[(k, hh, fx) for k, hh, fx in rows], flat=(pf, pp))
    print('\nblocks identical across c:')
    for k, d in blocks.items():
        print('  %-8s %s %s' % (k, 'identical' if len(set(d.values())) == 1 else 'c-dependent', d))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'runs', 'rival_static.json'), 'w'), indent=1, default=str)


# ---------------------------------------------------------------- network-lumped reduced chain
LABELS = ('D-type', 'FB-net', 'P*-net', 'exploitable', 'other-coop')


def lumped_rates(prov, nw, rho_fn, reps):
    """rates[(r_label, dest_label)] = sum over classes q with label dest of mu(q) * rho_fn(q, rep(r)).
    Moves within a label are not transitions of the lumped chain."""
    mu = nw['mu']; lab = nw['lab']
    R = {}
    for rl, r in reps.items():
        for q in range(len(mu)):
            if q == r or mu[q] == 0 or lab[q] == rl: continue
            R[(rl, lab[q])] = R.get((rl, lab[q]), 0.0) + mu[q] * rho_fn(q, r)
    return R


def gth(Q):
    """Stationary distribution of an irreducible rate matrix (off-diagonal rates) by
    Grassmann-Taksar-Heyman elimination: subtraction-free, accurate for tiny rates."""
    A = np.array(Q, float); n = len(A)
    np.fill_diagonal(A, 0.0)
    for k in range(n - 1, 0, -1):
        s = A[k, :k].sum()
        if s <= 0: s = 1e-300
        A[:k, k] /= s
        for i in range(k):
            if A[i, k] != 0:
                A[i, :k] += A[i, k] * A[k, :k]
        for i in range(k): A[i, i] = 0.0
    pi = np.zeros(n); pi[0] = 1.0
    for k in range(1, n):
        pi[k] = pi[:k] @ A[:k, k]
    return pi / pi.sum()


def lumped_pi(R, labels=LABELS):
    n = len(labels); T = np.zeros((n, n))
    for i, a in enumerate(labels):
        for j, b in enumerate(labels):
            if i != j: T[i, j] = R.get((a, b), 0.0)
    return dict(zip(labels, gth(T)))


def reps_for(prov, nw):
    mu = nw['mu']; lab = nw['lab']
    oc = [x for x in range(len(mu)) if lab[x] == 'other-coop']
    return {'D-type': nw['iD'], 'FB-net': nw['iF'], 'P*-net': nw['iP'], 'exploitable': nw['iC'],
            'other-coop': max(oc, key=lambda x: mu[x])}


def expanded_residents(prov, nw, per_label=(('D-type', 1), ('FB-net', 6), ('P*-net', 4), ('exploitable', 3), ('other-coop', 2))):
    """Resident set for the partially lumped chain: the heaviest members of each label by μ,
    always including the primary representatives."""
    mu = nw['mu']; lab = nw['lab']; reps = reps_for(prov, nw)
    S = []
    for l, k in per_label:
        mem = sorted([x for x in range(len(mu)) if lab[x] == l], key=lambda x: -mu[x])
        sel = [reps[l]] + [x for x in mem if x != reps[l]][:k - 1]
        S += sel
    return S


def partial_rates(prov, nw, rho_fn, S, reps):
    """Rates over the resident set S: a mutant q in S goes to q; any other q goes to the
    primary representative of its label (lumping only outside S)."""
    mu = nw['mu']; lab = nw['lab']
    pos = {s: i for i, s in enumerate(S)}
    Q = np.zeros((len(S), len(S)))
    for i, r in enumerate(S):
        for q in range(len(mu)):
            if q == r or mu[q] == 0: continue
            j = pos.get(q, pos[reps[lab[q]]])
            if j == i: continue
            Q[i, j] += mu[q] * rho_fn(q, r)
    return Q


def partial_pi(prov, nw, rho_fn, S=None):
    reps = reps_for(prov, nw)
    S = S or expanded_residents(prov, nw)
    Q = partial_rates(prov, nw, rho_fn, S, reps)
    p = gth(Q)
    by = {l: 0.0 for l in LABELS}
    for s, v in zip(S, p): by[nw['lab'][s]] += v
    return by, dict(zip([prov.names[s] for s in S], p)), Q, S


def validate():
    """Well-mixed lumped chain vs the published full-chain values (RESULTS.md, 'Priced arm', lazy n = 8;
    c = 0 is the free arm)."""
    known = {0.0: {1000: 0.3707, 10000: 0.6172, 30000: 0.7246}, 0.01: {1000: 0.3790, 10000: 0.9985, 30000: 1.0000}}
    for c in (0.0, 0.01, 0.1):
        prov = load(c); nw = networks(prov); U = prov.Ufull
        reps = reps_for(prov, nw)
        print('c = %g, representatives: %s' % (c, {k: prov.names[v] for k, v in reps.items()}))
        for N in (1000, 4096, 10000, 30000):
            R = lumped_rates(prov, nw, lambda q, r: wm(U, q, r, N, N), reps)
            pi = lumped_pi(R)
            coop = pi['FB-net'] + pi['P*-net'] + pi['exploitable'] + pi['other-coop']
            print('  N=%d lumped pi %s  self-cooperating labels %.4f  full chain P(C,C) %s' % (
                N, {k: '%.4f' % v for k, v in pi.items()}, coop, known.get(c, {}).get(N, '-')))
            by, per, Q, S = partial_pi(prov, nw, lambda q, r: wm(U, q, r, N, N))
            print('        partial (%d residents) %s  self-coop %.4f' % (len(S), {k: '%.4f' % v for k, v in by.items()}, 1 - by['D-type']))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'validate':
        validate()
    else:
        main()
