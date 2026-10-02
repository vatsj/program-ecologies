"""Ergodic islands (THEORY §9.5 (i)): the eps->0 chain over monomorphic
metapopulation states, with mutation re-injected.

Model (as src/islands.py): I islands of N on a regular island graph (complete
or hypercube).  Each event a uniformly random agent dies; with probability
1 - m it is replaced by the offspring of a parent drawn from its own island
with probability proportional to count * exp(w * fitness), with probability m
from a uniformly random neighbouring island (fitness evaluated at the parent's
home).  Fitness is the mean payoff against the other N - 1 agents of the
island.  Mutation: probability eps per birth.

The eps->0 object at fixed (I, N, m): between mutations the metapopulation
absorbs, so the chain runs over monomorphic metapopulation states a with
transition weight mu(q) * Phi(q | a), Phi = probability that one q mutant on a
uniformly random island takes the whole metapopulation.

Two estimates of Phi:
  phi2   rare-migration (m -> 0 after eps -> 0): the mutant fixes on its island
         with the within-island Moran probability rho_N(q|a), then the
         island-level process is a biased walk with ratio r = rho_N(q|a) /
         rho_N(a|q) on every discordant edge of the island graph, so
         Phi = rho_N(q|a) * (1 - 1/r) / (1 - r^-I), on any regular graph
         (neutral: r = 1, Phi = 1/(I N)).
  MC     Monte Carlo to global absorption at fixed m (meta_fix), Wilson
         intervals, for the key edges.

    python3 src/ergodic_islands.py static        # static numbers for the brief
"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from abm import njit
from chain import fixation
from islands import _load, ROOT

W = 0.3


# ------------------------------------------------------------------ static
@njit(cache=True)
def log_fixation(uqq, uqa, uaq, uaa, N, w, kstar):
    """log of chain.fixation (no underflow)."""
    if kstar <= 1:
        return 0.0
    acc = 0.0; lmax = 0.0
    logs = np.empty(kstar - 1)
    for k in range(1, kstar):
        pq = (k - 1) / (N - 1) * uqq + (N - k) / (N - 1) * uqa
        pa = k / (N - 1) * uaq + (N - k - 1) / (N - 1) * uaa
        acc += w * (pa - pq)
        logs[k - 1] = acc
        if acc > lmax: lmax = acc
    ssum = np.exp(-lmax)            # the leading 1
    for k in range(kstar - 1):
        ssum += np.exp(logs[k] - lmax)
    return -(lmax + np.log(ssum))


def _logexpm1(x):
    return x + np.log(-np.expm1(-x)) if x > 30 else np.log(np.expm1(x))


def log_gr(lr, I):
    """log of (1 - 1/r) / (1 - r^-I) with lr = log r: the island-level
    gambler's ruin from one island of I with up/down ratio r (r = 1: 1/I)."""
    if I == 1:
        return 0.0
    if abs(lr) < 1e-12:
        return -np.log(I)
    if lr > 0:
        return np.log(-np.expm1(-lr)) - np.log(-np.expm1(-I * lr))
    a = -lr
    return _logexpm1(a) - _logexpm1(I * a)


def log_rho(U, q, a, N, w=W):
    return log_fixation(U[q, q], U[q, a], U[a, q], U[a, a], N, w, N)


def rho_pair(U, q, a, N, w=W):
    return float(np.exp(log_rho(U, q, a, N, w)))


def log_phi2_game(g, N, I, w=W):
    uqq, uqa, uaq, uaa = g
    lq = log_fixation(uqq, uqa, uaq, uaa, N, w, N)
    la = log_fixation(uaa, uaq, uqa, uqq, N, w, N)
    return lq + log_gr(lq - la, I)


def phi2(U, q, a, N, I, w=W):
    """Rare-migration two-level global fixation probability of one q on all-a."""
    return float(np.exp(log_phi2_game((U[q, q], U[q, a], U[a, q], U[a, a]), N, I, w)))


def phi_matrix(U, N, I, w=W):
    K = U.shape[0]
    L = np.full((K, K), -np.inf)
    for q in range(K):
        for a in range(K):
            if q != a:
                L[q, a] = log_rho(U, q, a, N, w)
    P = np.zeros((K, K))          # P[q, a] = Phi(q | a)
    for q in range(K):
        for a in range(K):
            if q != a:
                P[q, a] = np.exp(L[q, a] + log_gr(L[q, a] - L[a, q], I))
    return P, L


def gth(M):
    """Stationary distribution of the chain with off-diagonal rates M[a, b]
    (Grassmann-Taksar-Heyman; no subtractions, stable for tiny rates)."""
    A = M.astype(float).copy(); np.fill_diagonal(A, 0.0)
    K = A.shape[0]
    for k in range(K - 1, 0, -1):
        s = A[k, :k].sum()
        if s <= 0:
            s = 1e-300
        A[:k, k] /= s
        A[:k, :k] += np.outer(A[:k, k], A[k, :k])
        np.fill_diagonal(A, 0.0)
    pi = np.zeros(K); pi[0] = 1.0
    for k in range(1, K):
        pi[k] = pi[:k] @ A[:k, k]
    return pi / pi.sum()


def stationary(P, mu):
    """Monomorphic chain: from a, mutant q (prob mu_q) takes over with
    Phi(q|a).  Returns pi and the rate matrix M[a, q] = mu_q Phi(q|a)."""
    M = (P * mu[:, None]).T.copy()          # M[a, q]
    np.fill_diagonal(M, 0.0)
    return gth(M), M


def classify(U, R, q):
    """Mutant q relative to resident R: shadow (on-path identical), faker
    (earns more against R than R against itself), weak (earns what R earns
    against itself while R is exploited by it) or other."""
    uRR = U[R, R]
    if max(abs(U[q, R] - uRR), abs(U[R, q] - uRR), abs(U[q, q] - uRR)) < 1e-9:
        return 'shadow'
    if U[q, R] > uRR + 1e-9:
        return 'faker'
    if abs(U[q, R] - uRR) < 1e-9 and U[R, q] < uRR - 1e-9:
        return 'weak'
    return 'other'


def block_types(U, PCC, names):
    """Self-cooperating classes split into unconditional (does not punish D),
    unfakeable (punishes D, no strict invader in the language) and fakeable
    (punishes D, has a strict invader)."""
    iD = names.index('D'); K = len(names)
    out = {}
    for c in range(K):
        if PCC[c, c] <= 0.5:
            continue
        if abs(U[iD, c] - U[iD, iD]) > 1e-9:          # D earns more than P against c
            out[c] = 'unconditional'
        elif any(U[q, c] > U[c, c] + 1e-9 for q in range(K) if q != c):
            out[c] = 'fakeable'
        else:
            out[c] = 'unfakeable'
    return out


def analyse(arm, U, PCC, names, mu, N, I, w=W, P=None):
    if P is None:
        P, _ = phi_matrix(U, N, I, w)
    pi, M = stationary(P, mu)
    iD = names.index('D')
    iR = names.index('THEM(^C)') if 'THEM(^C)' in names else names.index('BOX(THEM(ME))')
    pcc = float(pi @ np.diag(PCC))
    ex = dict(shadow=0.0, faker=0.0, weak=0.0, other=0.0)
    for q in range(len(names)):
        if q != iR:
            ex[classify(U, iR, q)] += M[iR, q]
    tot = sum(ex.values())
    coop = np.diag(PCC) > 0.5
    entry_coop = float(sum(M[iD, q] for q in range(len(names)) if coop[q]))
    top = np.argsort(-pi)[:6]
    # the cooperative block: pi by type, and pi-weighted exits to non-cooperative states by mutant type
    bt = block_types(U, PCC, names)
    pib = {t: float(sum(pi[c] for c, tt in bt.items() if tt == t)) for t in ('unconditional', 'unfakeable', 'fakeable')}
    bex = dict(shadow=0.0, faker=0.0, weak=0.0, other=0.0)
    for c in bt:
        for q in range(len(names)):
            if q != c and q not in bt:
                bex[classify(U, c, q)] += pi[c] * M[c, q]
    return dict(arm=arm, N=N, I=I, w=w, pcc=pcc, pi_D=float(pi[iD]), pi_R=float(pi[iR]),
                entry_R=float(M[iD, iR]), entry_coop=entry_coop, exit_R=tot,
                **{'exit_' + k: v for k, v in ex.items()},
                faker_share=ex['faker'] / tot, shadow_share=ex['shadow'] / tot,
                pi_block=pib, block_exit_flow=bex,
                support=[(names[k], float(pi[k])) for k in top])


def coexistence_pairs(U, names, mu, res):
    """Mutants q that invade res while res invades q (a stable interior rest
    point within an island), with their mu weight."""
    a = names.index(res); out = []
    for q in range(len(names)):
        if q != a and U[q, a] > U[a, a] + 1e-9 and U[a, q] > U[q, q] + 1e-9:
            out.append((names[q], float(mu[q])))
    return out


def static_main():
    out = {}
    for arm in ('pd', 'modal6'):
        game, U, PCC, names, sizes, mu = _load(arm, False)
        mu = mu / mu.sum()
        iD = names.index('D'); iC = names.index('C')
        iR = names.index('THEM(^C)') if arm == 'pd' else names.index('BOX(THEM(ME))')
        print('==', arm, 'K', len(names), 'mu(R) %.3e mu(C) %.3e' % (mu[iR], mu[iC]))
        for res in ('D', names[iR]):
            cp = coexistence_pairs(U, names, mu, res)
            print('  coexistence with %s: %d classes, mu %.2e' % (res, len(cp), sum(m for _, m in cp)), cp[:5])
        fk = [(names[q], mu[q], rho_pair(U, q, iR, 100)) for q in range(len(names)) if q != iR and classify(U, iR, q) == 'faker']
        print('  fakers of R: %d, mu %.2e' % (len(fk), sum(f[1] for f in fk)))
        for nm, m_, r_ in sorted(fk, key=lambda f: -f[1] * f[2])[:6]:
            print('    %-28s mu %.2e rho_100 %.3f' % (nm, m_, r_))
        for N in (10, 25, 50, 100, 200, 400, 1000):
            print('  N=%d rho(R|D) %.4f rho(D|R) %.2e rho(C|R) %.4f rho(D|C) %.4f' % (
                N, rho_pair(U, iR, iD, N), rho_pair(U, iD, iR, N), rho_pair(U, iC, iR, N), rho_pair(U, iD, iC, N)), end='')
            if arm == 'pd':
                iF = names.index('THEM(^D)')
                print(' rho(F|R) %.4f rho(R|F) %.2e' % (rho_pair(U, iF, iR, N), rho_pair(U, iR, iF, N)))
            else:
                print()
    return out


def rho_dilute(uqq, uqa, uaq, uaa, N, w, mN, kstar=None):
    """Within-island fixation (reach N) of one q among N - 1 a, with immigrants
    from an all-a sea at m = mN / N per death (the q lineage's own emigrants
    are ignored)."""
    m = mN / N
    kstar = N if kstar is None else kstar
    acc = 0.0; logs = []
    for k in range(1, kstar):
        pq = (k - 1) / (N - 1) * uqq + (N - k) / (N - 1) * uqa
        pa = k / (N - 1) * uaq + (N - k - 1) / (N - 1) * uaa
        fq, fa = np.exp(w * pq), np.exp(w * pa)
        Z = k * fq + (N - k) * fa
        up = (N - k) / N * (1 - m) * k * fq / Z
        dn = k / N * ((1 - m) * (N - k) * fa / Z + m)
        acc += np.log(dn / up); logs.append(acc)
    logs = np.array(logs); mx = max(logs.max(), 0.0)
    return float(np.exp(-mx) / (np.exp(-mx) + np.exp(logs - mx).sum()))


GAMES = {   # 2x2 games of the key edges: (u_qq, u_qa, u_aq, u_aa)
    'entry R|D': (0.0, -1.0, -1.0, -1.0),         # THEM(^C) into all-D = FairBot into all-D
    'faker THEM(^D)|R': (-1.0, 1.0, -2.0, 0.0),   # = D into all-C
    'faker THEM(^X)|R': (-0.5, 0.5, -1.0, 0.0),   # = THEM(^ROLE) into all-R
    'shadow C|R': (0.0, 0.0, 0.0, 0.0),
}


def reduction(arm, N, I, U, names, mu):
    """Three-rate reduction of the two-level chain: entry into all-D by the
    cooperative classes, exits from the reciprocator split by type."""
    iD = names.index('D')
    iR = names.index('THEM(^C)') if arm == 'pd' else names.index('BOX(THEM(ME))')
    entry = mu[iR] * phi2(U, iR, iD, N, I)
    ex = dict(shadow=0.0, faker=0.0, weak=0.0, other=0.0)
    for q in range(len(names)):
        if q != iR:
            ex[classify(U, iR, q)] += mu[q] * phi2(U, q, iR, N, I)
    tot = sum(ex.values())
    return entry, ex, tot


# ------------------------------------------------------------------ Monte Carlo
@njit(cache=True)
def _meta_fix(uqq, uqa, uaq, uaa, nbr, N, w, m, trials, cap_events, seed):
    """One q mutant on a uniformly random island of an all-a metapopulation;
    run to global absorption.  Returns (successes, failures, undecided,
    events used by successes)."""
    np.random.seed(seed)
    I, deg = nbr.shape
    fq = np.empty(N + 1); fa = np.empty(N + 1)
    for k in range(N + 1):
        if k >= 1:
            fq[k] = np.exp(w * ((k - 1) * uqq + (N - k) * uqa) / (N - 1))
        else:
            fq[k] = 0.0
        if k <= N - 1:
            fa[k] = np.exp(w * (k * uaq + (N - k - 1) * uaa) / (N - 1))
        else:
            fa[k] = 0.0
    c = np.zeros(I, np.int64)
    succ = 0; fail = 0; undec = 0; ev_succ = 0
    total_target = I * N
    for t in range(trials):
        for i in range(I): c[i] = 0
        c[np.random.randint(I)] = 1
        tot = 1; ev = 0
        while True:
            i = np.random.randint(I)
            src = i
            if m > 0.0 and np.random.random() < m:
                src = nbr[i, np.random.randint(deg)]
            k = c[src]
            if k == 0:
                child_q = False
            elif k == N:
                child_q = True
            else:
                a = k * fq[k]; b = (N - k) * fa[k]
                child_q = np.random.random() * (a + b) < a
            vict_q = np.random.randint(N) < c[i]
            if child_q and not vict_q:
                c[i] += 1; tot += 1
            elif vict_q and not child_q:
                c[i] -= 1; tot -= 1
            ev += 1
            if tot == 0:
                fail += 1; break
            if tot == total_target:
                succ += 1; ev_succ += ev; break
            if ev >= cap_events:
                undec += 1; break
    return succ, fail, undec, ev_succ


def wilson(k, n, z=1.96):
    if n == 0: return 0.0, 1.0
    p = k / n; d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d; half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, centre - half), min(1.0, centre + half)


def island_graph(kind, I):
    if I == 1:
        return np.zeros((1, 1), np.int64)
    from islands import graph
    return graph(kind, I)[0]


def mc_edge(game, kind, I, N, mN, min_succ=150, batch=200, max_trials=400000, time_budget=2400.0, cap_gens=200000, seed=0):
    """Phi_MC with a 95% Wilson interval over decided trials, plus bounds that
    count undecided trials as failures (lo_u) and as successes (hi_u).  Seeds
    differ by edge, graph and mN (no common random numbers across cells)."""
    import zlib
    g = GAMES[game]
    nbr = island_graph(kind, I)
    m = mN / N if I > 1 else 0.0
    base = zlib.crc32(('%s|%s|%d|%d|%g|%d' % (game, kind, I, N, mN, seed)).encode()) % 1000000007
    s = f = u = ev = 0; b = 0; t0 = time.time()
    while s < min_succ and s + f + u < max_trials and time.time() - t0 < time_budget:
        s1, f1, u1, e1 = _meta_fix(*g, nbr, N, W, m, batch, cap_gens * I * N, (base + 7919 * b) % 2147483647)
        s += s1; f += f1; u += u1; ev += e1; b += 1
    stop = 'successes' if s >= min_succ else ('trials' if s + f + u >= max_trials else 'time')
    dec = s + f
    lo, hi = wilson(s, dec)
    lo_u = wilson(s, s + f + u)[0]; hi_u = wilson(s + u, s + f + u)[1]
    rho_N = float(np.exp(log_fixation(*g, N, W, N)))
    return dict(game=game, graph=kind, I=I, N=N, mN=mN, succ=int(s), fail=int(f), undec=int(u), trials=int(s + f + u), stop=stop,
                phi=s / dec if dec else float('nan'), lo=lo, hi=hi, lo_u=lo_u, hi_u=hi_u,
                phi2=float(np.exp(log_phi2_game(g, N, I))), rho_N=rho_N,
                gens_per_success=(ev / s / (I * N)) if s else float('nan'), time_s=time.time() - t0)


def smoke_mc():
    for args in [('entry R|D', 'complete', 1, 25, 0.0), ('shadow C|R', 'complete', 4, 10, 1.0), ('shadow C|R', 'hypercube', 4, 10, 1.0),
                 ('faker THEM(^D)|R', 'complete', 1, 25, 0.0)]:
        r = mc_edge(*args, min_succ=200, batch=500)
        print(args, 'phi %.4f [%.4f, %.4f] phi2 %.4f trials %d undec %d (%.1fs)' % (r['phi'], r['lo'], r['hi'], r['phi2'], r['trials'], r['undec'], r['time_s']))
    r = mc_edge('entry R|D', 'complete', 256, 100, 0.1, min_succ=3, batch=20)
    print('timing I=256 N=100 mN=0.1 entry: phi %.4f, %d trials, gens/success %.0f, %.1fs' % (r['phi'], r['trials'], r['gens_per_success'], r['time_s']))


def static_grid():
    rows = []
    for arm in ('pd', 'modal6'):
        game, U, PCC, names, sizes, mu = _load(arm, False)
        mu = mu / mu.sum()
        for N in (10, 25, 50, 100, 200, 400, 1000):
            for I in (1, 4, 16, 64, 256, 1024, 4096):
                e, ex, tot = reduction(arm, N, I, U, names, mu)
                rows.append((arm, N, I, e, ex['faker'], ex['shadow'], ex['other'], e / tot))
                print('%-6s N=%4d I=%4d M=%7d entry_R %.2e exits: faker %.2e shadow %.2e other %.2e  faker share %.2f  R/D odds %.4f' % (
                    arm, N, I, N * I, e, ex['faker'], ex['shadow'], ex['other'], ex['faker'] / tot, e / tot))
    print()
    for name, g in GAMES.items():
        for N in (25, 100, 400):
            print('%-18s N=%d rho_N %.4f' % (name, N, np.exp(log_fixation(*g, N, W, N))), ' '.join('mN=%g: %.4f' % (mN, rho_dilute(*g, N, W, mN, N // 2)) for mN in (0.1, 1, 3, 10)),
                  '| well-mixed IN=64N: %.4f' % np.exp(log_fixation(*g, 64 * N, W, 64 * N)))


def smoke_chain():
    """I = 1 reproduces the well-mixed lim_N chain (RESULTS 'lim_N of the chain')."""
    for arm in ('pd', 'modal6'):
        game, U, PCC, names, sizes, mu = _load(arm, False)
        mu = mu / mu.sum()
        for N in (100, 1000):
            r = analyse(arm, U, PCC, names, mu, N, 1)
            print(arm, N, 'P(C,C) %.4f pi_D %.4f pi_R %.4f faker share %.2f' % (r['pcc'], r['pi_D'], r['pi_R'], r['faker_share']), r['support'][:4])


def patched_row(arm, N, I, mc, graph, mN):
    """Two-level chain with every pair whose 2x2 game equals a game measured
    at (graph, I, N, mN) replaced by Phi_MC (exploratory: the remaining pairs
    keep Phi_2)."""
    game, U, PCC, names, sizes, mu = _load(arm, False)
    mu = mu / mu.sum()
    P, _ = phi_matrix(U, N, I)
    meas = {r['game']: r['phi'] for r in mc if r['graph'] == graph and r['I'] == I and r['N'] == N and r['mN'] == mN and r['succ'] > 0
            and r['game'] != 'shadow C|R'}      # the neutral cell is a code check; its exact value is 1/(IN)
    n_rep = 0
    for gname, ph in meas.items():
        g = np.array(GAMES[gname])
        for q in range(len(names)):
            for a in range(len(names)):
                if q != a and np.abs(np.array([U[q, q], U[q, a], U[a, q], U[a, a]]) - g).max() < 1e-9:
                    P[q, a] = ph; n_rep += 1
    r = chain_row(arm, U, PCC, names, mu, N, I, P=P, top_flows=False)
    r.update(graph=graph, mN=mN, measured=sorted(meas), n_replaced=n_rep)
    return r


# ------------------------------------------------------------------ drivers
ARMS = ('pd', 'modal6')
STATIC_N = (5, 10, 16, 25, 50, 100, 200, 400, 1000)
STATIC_I = (1, 4, 16, 64, 256, 1024, 4096)


def chain_row(arm, U, PCC, names, mu, N, I, P=None, top_flows=True):
    if P is None:
        P, _ = phi_matrix(U, N, I)
    r = analyse(arm, U, PCC, names, mu, N, I, P=P)
    pi, M = stationary(P, mu)
    iR = names.index('THEM(^C)') if arm == 'pd' else names.index('BOX(THEM(ME))')
    iD = names.index('D')
    if top_flows:
        F = pi[:, None] * M                 # probability flow a -> b per mutation event
        np.fill_diagonal(F, 0.0)
        idx = np.dstack(np.unravel_index(np.argsort(-F, axis=None)[:8], F.shape))[0]
        r['top_flows'] = [(names[a], names[b], float(F[a, b])) for a, b in idx]
        r['exit_R_top'] = sorted(((names[q], float(M[iR, q])) for q in range(len(names)) if q != iR), key=lambda kv: -kv[1])[:5]
        r['entry_D_top'] = sorted(((names[q], float(M[iD, q])) for q in range(len(names)) if q != iD and PCC[q, q] > 0.5), key=lambda kv: -kv[1])[:4]
        fk = [q for q in range(len(names)) if q != iR and classify(U, iR, q) == 'faker']
        r['pi_faker_states'] = float(pi[fk].sum()) if fk else 0.0
        wk = [q for q in range(len(names)) if q != iR and classify(U, iR, q) == 'weak']
        r['pi_weak_faker_states'] = float(pi[wk].sum()) if wk else 0.0
        r['pi_C'] = float(pi[names.index('C')])
        coop = np.diag(PCC) > 0.5
        r['pi_coop'] = float(pi[coop].sum())
    return r


def run_static():
    rows = []
    for arm in ARMS:
        game, U, PCC, names, sizes, mu = _load(arm, False)
        mu = mu / mu.sum()
        for N in STATIC_N:
            for I in STATIC_I:
                r = chain_row(arm, U, PCC, names, mu, N, I)
                rows.append(r)
                print('%-6s N=%4d I=%4d P(C,C) %.4f pi_D %.4f pi_R %.4f pi_coop %.4f faker share %.3f' % (
                    arm, N, I, r['pcc'], r['pi_D'], r['pi_R'], r['pi_coop'], r['faker_share']), flush=True)
    json.dump(rows, open(os.path.join(ROOT, 'runs', 'ergodic_islands_static.json'), 'w'), indent=1)
    return rows


def mc_jobs():
    """[after review] Entry is the uncertain edge: >= 150 successes per cell.
    The faker edges are near-theorems (constant selection, T + S = R + P):
    code checks at >= 400 successes on one cell per (graph, mN) plus the
    N = 25 and mN = 10 cells.  A small-m ladder at (I, N) = (16, 25)."""
    E, FD, FX = 'entry R|D', 'faker THEM(^D)|R', 'faker THEM(^X)|R'
    J = []
    for mN in (0.1, 1.0):
        for kind in ('complete', 'hypercube'):
            for I in (4, 16, 64, 256):
                J.append((E, kind, I, 100, mN, 150))
            J.append((FD, kind, 64, 100, mN, 400))
        for N in (25, 400):
            J.append((E, 'complete', 64, N, mN, 150))
        J.append((FX, 'complete', 64, 100, mN, 400))
    J += [(E, 'torus', 64, 100, 1.0, 150), (FD, 'torus', 64, 100, 1.0, 400)]
    J += [(FD, 'complete', 64, 25, 1.0, 400), (FX, 'complete', 64, 25, 1.0, 400)]
    for mN in (3.0, 10.0):
        J.append((E, 'complete', 64, 100, mN, 150))
    J += [(FD, 'complete', 64, 100, 10.0, 400), (FX, 'complete', 64, 100, 10.0, 400)]
    J += [(E, 'complete', 16, 25, mN, 150) for mN in (0.01, 0.1, 1.0, 3.0)]
    J += [('shadow C|R', kind, 16, 25, 1.0, 40) for kind in ('complete', 'hypercube')]
    return J


def _mc_job(j):
    return mc_edge(*j[:5], min_succ=j[5])


def run_mc(procs=3):
    from multiprocessing import Pool
    J = mc_jobs()
    J.sort(key=lambda j: -j[2] * j[3])
    path = os.path.join(ROOT, 'runs', 'ergodic_islands_mc.json')
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {(r['game'], r['graph'], r['I'], r['N'], r['mN']) for r in rows}
    J = [j for j in J if tuple(j[:5]) not in done]
    with Pool(procs) as pool:
        for r in pool.imap_unordered(_mc_job, J):
            rows.append(r)
            print('%-18s %-9s I=%3d N=%3d mN=%4g: Phi %.4f [%.4f, %.4f] phi2 %.4f ratio %.2f (%d/%d/%d, stop %s, %.0f gens/succ, %.0fs)' % (
                r['game'], r['graph'], r['I'], r['N'], r['mN'], r['phi'], r['lo'], r['hi'], r['phi2'], r['phi'] / r['phi2'],
                r['succ'], r['fail'], r['undec'], r['stop'], r['gens_per_success'], r['time_s']), flush=True)
            json.dump(rows, open(path, 'w'), indent=1)
    return rows


ABM = [  # (arm, graph, I, N, mN, epsN, seeding)
    *[('pd', 'complete', I, 100, 1.0, 0.1, 'alld') for I in (16, 64, 256)],
    *[('pd', 'hypercube', I, 100, 1.0, 0.1, 'alld') for I in (64, 256)],
    *[('pd', 'complete', I, 100, 1.0, 0.01, 'alld') for I in (16, 64, 256)],
    *[('pd', 'complete', I, 25, 1.0, 0.1, 'alld') for I in (64, 256)],
    ('pd', 'complete', 64, 100, 0.1, 0.01, 'alld'),
    *[('modal6', 'complete', I, 100, 1.0, e, 'alld') for e in (0.1, 0.01) for I in (16, 64, 256)],
    # [after review] cooperative starts (all-R) as a mixing check
    ('pd', 'complete', 64, 100, 1.0, 0.1, 'allR'),
    ('pd', 'complete', 64, 100, 1.0, 0.01, 'allR'),
    ('modal6', 'complete', 64, 100, 1.0, 0.01, 'allR'),
]


def _abm_job(job):
    from islands import run_one
    arm, kind, I, N, mN, epsN, seeding, rep, gens = job
    r = run_one((arm, False, kind, mN, seeding, rep, I, N, W, gens, 20, epsN, 0.0))
    game, U, PCC, names, sizes, mu = _load(arm, False)
    iR = names.index('THEM(^C)') if arm == 'pd' else names.index('BOX(THEM(ME))')
    t = np.array(r['trace_cc']); h = len(t) // 2
    r['pcc_1st'] = float(t[:h].mean())
    ex = dict(faker=0, shadow=0, weak=0, other=0); ent = {}
    for x, y, n in r['trans']:
        if x == names[iR]:
            ex[classify(U, iR, names.index(y))] += n
        if y == names[iR]:
            ent[x] = ent.get(x, 0) + n
    r['exits_R'] = ex; r['entries_R'] = sorted(ent.items(), key=lambda kv: -kv[1])[:4]
    tot = sum(r['dom_time'].values()) or 1
    r['dom_share'] = {k: v / tot for k, v in sorted(r['dom_time'].items(), key=lambda kv: -kv[1])[:5]}
    r['dom_none'] = 1.0 - tot / max(sum(r['isl_cc_hist']), 1)
    for k in ('trace_pay', 'trans', 'spread_pay_pairs', 'final_classes', 'isl_dwl_hist'):
        r.pop(k, None)
    # [after review] P(C,C) decomposed by island dominant class: R, C, fakers of R, other classes, none
    nis = max(sum(r['isl_cc_hist']), 1)
    dec = dict(R=0.0, C=0.0, faker=0.0, other=0.0, none=0.0)
    for k, v in r['dom_cc'].items():
        if k == '(none)': dec['none'] += v
        elif k == names[iR]: dec['R'] += v
        elif k == 'C': dec['C'] += v
        elif classify(U, iR, names.index(k)) in ('faker', 'weak'): dec['faker'] += v
        else: dec['other'] += v
    r['pcc_by_dom'] = {k: v / nis for k, v in dec.items()}
    r['R_dom_time'] = r['dom_time'].get(names[iR], 0.0) / nis
    ex90 = dict(faker=0, shadow=0, weak=0, other=0, none=0)
    for k, v in r['exits_R90'].items():
        ex90['none' if k == '(none)' else classify(U, iR, names.index(k))] += v
    r['exits_R90_split'] = ex90
    r.update(arm=arm, kind=kind, seeding=seeding)
    return r


def run_abm(procs=3, reps=3, gens=200000):
    from multiprocessing import Pool
    for arm in ARMS:
        _load(arm, False)
    J = [(*c, rep, gens) for c in ABM for rep in range(reps)]
    J.sort(key=lambda j: -j[2] * j[3])
    path = os.path.join(ROOT, 'runs', 'ergodic_islands_abm.json')
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {(r['arm'], r['kind'], r['I'], r['N'], r['mN'], r['epsN'], r['seeding'], r['rep']) for r in rows}
    J = [j for j in J if tuple(j[:8]) not in done]
    with Pool(procs) as pool:
        for r in pool.imap_unordered(_abm_job, J):
            rows.append(r)
            print('%-6s %-9s I=%3d N=%3d mN=%g epsN=%g %s rep %d: P(C,C) 2nd %.3f 1st %.3f R-dom %.3f by-dom %s exits R90 %s (%.0fs)' % (
                r['arm'], r['kind'], r['I'], r['N'], r['mN'], r['epsN'], r['seeding'], r['rep'], r['pcc_2nd'], r['pcc_1st'], r['R_dom_time'],
                {k: round(v, 3) for k, v in r['pcc_by_dom'].items()}, r['exits_R90_split'], r['time_s']), flush=True)
            json.dump(rows, open(path, 'w'), indent=1)
    return rows


# ------------------------------------------------------------------ report
def _load_json(name):
    path = os.path.join(ROOT, 'runs', name)
    return json.load(open(path)) if os.path.exists(path) else []


def conditional_block_exits(arm, N, I):
    """pi-weighted exits from conditional cooperators (unfakeable + fakeable)
    to any class outside that set, by mutant type relative to the resident."""
    game, U, PCC, names, sizes, mu = _load(arm, False)
    mu = mu / mu.sum()
    P, _ = phi_matrix(U, N, I)
    pi, M = stationary(P, mu)
    bt = {c: t for c, t in block_types(U, PCC, names).items() if t != 'unconditional'}
    ex = dict(shadow=0.0, faker=0.0, weak=0.0, other=0.0)
    for c in bt:
        for q in range(len(names)):
            if q != c and q not in bt:
                ex[classify(U, c, q)] += pi[c] * M[c, q]
    tot = sum(ex.values())
    return {k: v / tot for k, v in ex.items()}


def report():
    st = _load_json('ergodic_islands_static.json')
    mc = _load_json('ergodic_islands_mc.json')
    ab = _load_json('ergodic_islands_abm.json')
    L = ['# Ergodic islands: mutation re-injected (predictions/2026-10-02-ergodic-islands.md)', '',
         'PD, w = 0.3. Weak arm L_6 with `ROLE` (R = `THEM(^C)`); modal arm n = 6 (R = FairBot `BOX(THEM(ME))`). '
         'A: eps->0 two-level chain over monomorphic metapopulation states (graph-independent on regular island graphs). '
         'B: Monte Carlo global fixation at fixed mN. C: finite-eps agent-based approach runs (not pi).', '']
    Ns = sorted({r['N'] for r in st}); Is = sorted({r['I'] for r in st})
    for arm, lab in (('pd', 'weak'), ('modal6', 'modal')):
        for key, title in ((('pcc', 'P(C,C)'), ('pi_R', 'pi(all-R)')) if arm == 'pd' else (('pcc', 'P(C,C)'),)):
            L += ['## A. %s arm: %s (rows N, columns I)' % (lab, title), '', '| N \\ I | ' + ' | '.join(map(str, Is)) + ' |', '|---|' + '---|' * len(Is)]
            for N in Ns:
                L.append('| %d | ' % N + ' | '.join('%.4f' % next(r[key] for r in st if r['arm'] == arm and r['N'] == N and r['I'] == I) for I in Is) + ' |')
            L.append('')
    L += ['## A. weak arm: exits from all-R (shares) and sinks', '',
          '| N | I | M | faker | weak | shadow | other | formula f/(f+0.2493/M) | pi(faker states) | pi(weak-faker states) | R share of coop entry | support (top 5) |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in st:
        if r['arm'] != 'pd' or r['I'] not in (1, 16, 64, 256, 4096):
            continue
        t = r['exit_R']; f = r['exit_faker']
        L.append('| %d | %d | %d | %.3f | %.4f | %.3f | %.4f | %.3f | %.1e | %.4f | %.3f | %s |' % (
            r['N'], r['I'], r['N'] * r['I'], f / t, r['exit_weak'] / t, r['shadow_share'], r['exit_other'] / t, f / (f + 0.2493 / (r['N'] * r['I'])),
            r['pi_faker_states'], r['pi_weak_faker_states'], r['entry_R'] / r['entry_coop'],
            '; '.join('`%s` %.4f' % (a, b) for a, b in r['support'][:5])))
    L += ['', '## A. modal arm: cooperative block', '',
          'pi of unfakeable / fakeable / unconditional cooperators; pi-weighted exits from conditional cooperators (unfakeable + fakeable) to classes outside them.', '',
          '| N | I | P(C,C) | odds | pi unfakeable | pi fakeable | fakeable/unfakeable | pi unconditional | exits: strict faker / weak / neutral shadow / other | well-mixed P(C,C) at M = IN |',
          '|---|---|---|---|---|---|---|---|---|---|']
    game, U, PCC, names, sizes, mu = _load('modal6', False); mun = mu / mu.sum()
    wm_cache = {}
    for r in st:
        if r['arm'] != 'modal6' or r['N'] not in (50, 100, 1000) or r['I'] not in (1, 4, 16, 64, 256, 1024):
            continue
        M = r['N'] * r['I']
        if M not in wm_cache:
            wm_cache[M] = analyse('modal6', U, PCC, names, mun, M, 1)['pcc'] if M <= 30000 else float('nan')
        be = conditional_block_exits('modal6', r['N'], r['I']); pb = r['pi_block']
        L.append('| %d | %d | %.4f | %.3f | %.4f | %.4f | %.4f | %.4f | %.2f / %.2f / %.2f / %.2f | %.4f |' % (
            r['N'], r['I'], r['pcc'], r['pcc'] / (1 - r['pcc']), pb['unfakeable'], pb['fakeable'], pb['fakeable'] / pb['unfakeable'], pb['unconditional'],
            be['faker'], be['weak'], be['shadow'], be['other'], wm_cache[M]))
    if mc:
        L += ['', '## B. Monte Carlo global fixation at fixed mN', '',
              'Phi_MC = successes / decided trials, 95% Wilson interval; [lo_u, hi_u] counts undecided trials as failures / successes. '
              'rho_N = within-island Moran fixation; Phi_2 = two-level value.', '',
              '| edge | graph | I | N | mN | Phi_MC [95%] | Phi_MC / rho_N [95%] | Phi_2 | succ / fail / undec | stop | [lo_u, hi_u] | gens per success |',
              '|---|---|---|---|---|---|---|---|---|---|---|---|']
        for r in sorted(mc, key=lambda r: (r['game'], r['N'], r['mN'], r['graph'], r['I'])):
            L.append('| %s | %s | %d | %d | %g | %.4f [%.4f, %.4f] | %.3f [%.3f, %.3f] | %.4f | %d / %d / %d | %s | [%.4f, %.4f] | %.0f |' % (
                r['game'], r['graph'], r['I'], r['N'], r['mN'], r['phi'], r['lo'], r['hi'], r['phi'] / r['rho_N'], r['lo'] / r['rho_N'], r['hi'] / r['rho_N'],
                r['phi2'], r['succ'], r['fail'], r['undec'], r['stop'], r['lo_u'], r['hi_u'], r['gens_per_success']))
        L += ['', '## B. Patched chain (exploratory): two-level chain with the measured 2x2 games replaced by Phi_MC', '',
              '| graph | I | N | mN | measured | P(C,C) patched | pi_R patched | pi_R two-level | ratio | faker share |', '|---|---|---|---|---|---|---|---|---|---|']
        cells = sorted({(r['graph'], r['I'], r['N'], r['mN']) for r in mc if r['game'] == 'entry R|D'})
        pat = []
        gm, Uw, PCw, nmw, szw, muw = _load('pd', False)
        for g, I, N, mN in cells:
            pr = patched_row('pd', N, I, mc, g, mN)
            base = next((r for r in st if r['arm'] == 'pd' and r['N'] == N and r['I'] == I), None)
            if base is None:
                base = analyse('pd', Uw, PCw, nmw, muw / muw.sum(), N, I)
            pr['pi_R_base'] = base['pi_R']; pat.append(pr)
            L.append('| %s | %d | %d | %g | %s | %.4f | %.4f | %.4f | %.2f | %.3f |' % (g, I, N, mN, ', '.join(pr['measured']), pr['pcc'], pr['pi_R'], base['pi_R'], pr['pi_R'] / base['pi_R'], pr['faker_share']))
        json.dump(pat, open(os.path.join(ROOT, 'runs', 'ergodic_islands_patched.json'), 'w'), indent=1)
    if ab:
        L += ['', '## C. Finite-eps agent-based approach runs (w_g = 0; 2e5 generations; second half; approach rates, not pi)', '',
              '| arm | graph | I | N | mN | epsN | start | P(C,C) per rep (2nd half) | mean | 1st half | R-dominant island-time | P(C,C) by island dominant class: R / C / faker / other / none | exits from >=90%-R islands: faker / weak / shadow / other / none | dominance-flip exits from R: faker / weak / shadow / other | dominant classes (rep 0) |',
              '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
        keys = sorted({(r['arm'], r['kind'], r['I'], r['N'], r['mN'], r['epsN'], r['seeding']) for r in ab}, key=lambda k: (k[0] != 'pd', k[5] != 0.1, k[6], k[1], k[3], k[4], k[2]))
        for k in keys:
            sub = sorted([r for r in ab if (r['arm'], r['kind'], r['I'], r['N'], r['mN'], r['epsN'], r['seeding']) == k], key=lambda r: r['rep'])
            p2 = np.array([r['pcc_2nd'] for r in sub]); p1 = np.array([r['pcc_1st'] for r in sub])
            dec = {d: np.mean([r['pcc_by_dom'][d] for r in sub]) for d in ('R', 'C', 'faker', 'other', 'none')}
            e90 = {d: sum(r['exits_R90_split'][d] for r in sub) for d in ('faker', 'weak', 'shadow', 'other', 'none')}
            efl = {d: sum(r['exits_R'].get(d, 0) for r in sub) for d in ('faker', 'weak', 'shadow', 'other')}
            L.append('| %s | %s | %d | %d | %g | %g | %s | %s | %.3f | %.3f | %.3f | %s | %s | %s | %s |' % (
                'weak' if k[0] == 'pd' else 'modal', k[1], k[2], k[3], k[4], k[5], k[6], ', '.join('%.3f' % x for x in p2), p2.mean(), p1.mean(),
                np.mean([r['R_dom_time'] for r in sub]), ' / '.join('%.3f' % dec[d] for d in ('R', 'C', 'faker', 'other', 'none')),
                ' / '.join(str(e90[d]) for d in ('faker', 'weak', 'shadow', 'other', 'none')),
                ' / '.join(str(efl[d]) for d in ('faker', 'weak', 'shadow', 'other')),
                ', '.join('`%s` %.2f' % kv for kv in list(sub[0]['dom_share'].items())[:4])))
    out = os.path.join(ROOT, 'runs', 'ergodic-islands-tables.md')
    open(out, 'w').write('\n'.join(L) + '\n')
    json.dump(dict(static=st, mc=mc, abm=ab, patched=_load_json('ergodic_islands_patched.json')), open(os.path.join(ROOT, 'runs', 'ergodic-islands.json'), 'w'), indent=1)
    print('\n'.join(L))


if __name__ == '__main__':
    if sys.argv[1] == 'static':
        static_main(); static_grid()
    elif sys.argv[1] == 'smoke_chain':
        smoke_chain()
    elif sys.argv[1] == 'smoke_mc':
        smoke_mc()
    elif sys.argv[1] == 'run_static':
        run_static()
    elif sys.argv[1] == 'run_mc':
        run_mc()
    elif sys.argv[1] == 'run_abm':
        run_abm()
    elif sys.argv[1] == 'report':
        report()
