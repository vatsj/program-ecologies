"""Agent-based Moran process with standing variance (finite eps*N).

N agents, each holding a behavioural class of the weak-arm language
(n = 6 with ROLE by default).  Each event: one agent reproduces with
probability proportional to exp(w * mean payoff against the other N-1
agents); with probability eps the offspring is a fresh draw from mu over
the classes, otherwise a copy of the parent; a uniformly random agent dies.
A generation is N events.  Statistics per sampled generation: mean payoff,
share of the THEM(^C) class, share of the ALLC class, and whether both are
present at once.

    python3 src/abm.py --game pd --n 6 --N 100 --w 0.3 --epsN 0.1 1 10 --seeds 5
"""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from dsl import Language
from game import Game
from evaluate import square_chunked
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    from numba import njit
except ImportError:  # pragma: no cover
    def njit(*a, **k):
        def deco(f): return f
        return deco if not a or not callable(a[0]) else a[0]


def classes_from_U(lang, ids, U, round_dec=6):
    """Behavioural classes by (row, column) of U; returns (reps, members, mu)."""
    R = np.round(U, round_dec)
    groups = defaultdict(list)
    for a, p in enumerate(ids):
        groups[(R[a].tobytes(), R[:, a].tobytes())].append(a)
    reps, members, mu = [], [], []
    for mem in groups.values():
        rep = min(mem, key=lambda a: (lang.bits[ids[a]], ids[a]))
        reps.append(rep); members.append(mem); mu.append(float(lang.mu[ids[mem]].sum()))
    order = np.argsort(-np.array(mu))
    reps = [reps[o] for o in order]; members = [members[o] for o in order]; mu = np.array([mu[o] for o in order])
    return reps, members, mu / mu.sum()


@njit(cache=True)
def _run(U, mu_cdf, N, w, eps, burn_gens, sample_gens, init_class, seed, iT, iC, K):
    np.random.seed(seed)
    counts = np.zeros(K, np.int64)
    counts[init_class] = N
    fit = np.zeros(K); wts = np.zeros(K)
    n_events = (burn_gens + sample_gens) * N
    S_pay = 0.0; S_T = 0.0; S_C = 0.0; S_both = 0.0; nsamp = 0
    for ev in range(n_events):
        # fitness of present classes: mean payoff against the other N-1 agents
        tot = 0.0
        for i in range(K):
            if counts[i] == 0:
                wts[i] = 0.0; continue
            s = 0.0
            for j in range(K):
                if counts[j] > 0:
                    s += counts[j] * U[i, j]
            s -= U[i, i]
            fit[i] = s / (N - 1)
        m = -1e300
        for i in range(K):
            if counts[i] > 0 and fit[i] > m: m = fit[i]
        for i in range(K):
            if counts[i] > 0:
                wts[i] = counts[i] * np.exp(w * (fit[i] - m)); tot += wts[i]
        # parent
        u = np.random.random() * tot; acc = 0.0; parent = -1
        for i in range(K):
            if counts[i] > 0:
                acc += wts[i]
                if u <= acc:
                    parent = i; break
        if parent < 0: parent = K - 1
        # offspring class
        if np.random.random() < eps:
            u = np.random.random(); child = K - 1
            for i in range(K):
                if u <= mu_cdf[i]:
                    child = i; break
        else:
            child = parent
        # death: uniformly random agent
        u = np.random.random() * N; acc = 0.0; victim = -1
        for i in range(K):
            if counts[i] > 0:
                acc += counts[i]
                if u <= acc:
                    victim = i; break
        if victim < 0: victim = parent
        counts[victim] -= 1; counts[child] += 1
        if ev >= burn_gens * N and (ev + 1) % N == 0:
            mp = 0.0
            for i in range(K):
                if counts[i] > 0: mp += counts[i] * fit[i]
            S_pay += mp / N
            S_T += counts[iT] / N; S_C += counts[iC] / N
            if counts[iT] > 0 and counts[iC] > 0: S_both += 1.0
            nsamp += 1
    return S_pay / nsamp, S_T / nsamp, S_C / nsamp, S_both / nsamp


def main(a):
    game = Game.load(os.path.join(ROOT, 'games', a.game + '.yaml'))
    L = Language('weak', a.n, k=game.k, names=game.actions, role=game.role)
    ids = L.ids()
    t0 = time.time()
    U, V, div = square_chunked(L, game, ids, rows=a.rows, verbose=True)
    print('evaluated %d programs (%.0fs), divergence %.4f' % (len(ids), time.time() - t0, div), flush=True)
    reps, members, mu = classes_from_U(L, ids, U)
    K = len(reps)
    Uc = np.ascontiguousarray(U[np.ix_(reps, reps)])
    names = [L.src(ids[r]) for r in reps]
    iT = names.index('THEM(^C)' if game.k == 2 else 'THEM(^%s)' % game.actions[-1])
    iC = names.index(game.actions[-1]); iD = names.index(game.actions[0])
    uDD = float(Uc[iD, iD]); eff = game.efficient_symmetric()
    print('%d classes; mu(C)=%.3f mu(D)=%.3f mu(THEM(^C))=%.2e; u(D,D)=%.3f efficient=%.3f' % (K, mu[iC], mu[iD], mu[iT], uDD, eff), flush=True)
    mu_cdf = np.cumsum(mu)
    rows = []
    for epsN in a.epsN:
        eps = epsN / a.N
        for seed in range(a.seeds):
            t = time.time()
            pay, sT, sC, both = _run(Uc, mu_cdf, a.N, a.w, eps, a.burn, a.sample, iD, seed, iT, iC, K)
            coop = (pay - uDD) / (eff - uDD)
            rows.append(dict(epsN=epsN, eps=eps, seed=seed, mean_payoff=pay, coop_share=coop, themC_share=sT, allc_share=sC, coexist=both, time_s=time.time() - t))
            print('epsN=%g seed=%d: payoff %.4f coop %.4f THEM(^C) %.4f ALLC %.4f coexist %.4f (%.0fs)' % (epsN, seed, pay, coop, sT, sC, both, time.time() - t), flush=True)
    lines = ['# Standing variance: agent-based Moran, %s, weak n=%d with ROLE, N=%d, w=%g, burn-in %d generations, %d sampled, %d seeds' % (
        a.game, a.n, a.N, a.w, a.burn, a.sample, a.seeds), '',
        'Cooperative share = (mean payoff - u(D,D)) / (efficient - u(D,D)); classes = %d behavioural classes of L_%d (%d programs); mutation per birth at eps = epsN/N, mutants from mu over classes.' % (K, a.n, len(ids)), '',
        '| epsN | coop share (mean ± sd over seeds) | THEM(^C) share | ALLC share | P(cooperator & ALLC coexist) |', '|---|---|---|---|---|']
    for epsN in a.epsN:
        sub = [r for r in rows if r['epsN'] == epsN]
        f = lambda key: '%.4f ± %.4f' % (np.mean([r[key] for r in sub]), np.std([r[key] for r in sub]))
        lines.append('| %g | %s | %s | %s | %s |' % (epsN, f('coop_share'), f('themC_share'), f('allc_share'), f('coexist')))
    out = os.path.join(ROOT, 'runs', 'abm_%s_N%d_w%g.md' % (a.game, a.N, a.w))
    open(out, 'w').write('\n'.join(lines) + '\n')
    json.dump(rows, open(out.replace('.md', '.json'), 'w'), indent=1)
    print('\n'.join(lines))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', default='pd')
    ap.add_argument('--n', type=int, default=6)
    ap.add_argument('--N', type=int, default=100)
    ap.add_argument('--w', type=float, default=0.3)
    ap.add_argument('--epsN', type=float, nargs='+', default=[0.1, 1.0, 10.0])
    ap.add_argument('--seeds', type=int, default=5)
    ap.add_argument('--burn', type=int, default=10000)
    ap.add_argument('--sample', type=int, default=100000)
    ap.add_argument('--rows', type=int, default=400)
    main(ap.parse_args())
