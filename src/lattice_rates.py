"""Per-mutant rates on the torus: the eps -> 0 object of the spatial process.

Death-birth Moran on an L x L torus, von Neumann neighbourhood, fitness
exp(w * mean payoff over the 4 own interactions), no mutation inside a trial.

(a) rho_enter(R): one R in all-D, run until R share >= 1/2 (success) or R
    extinct (failure); trials that decide neither within cap_gens generations
    are reported as undecided.
(b) M_exit(R): from all-R, mutants drawn one at a time from mu over the
    behavioural classes and injected at a random site; each mutant lineage is
    followed until it is extinct or has fixed (or cap_mut generations pass,
    after which the next mutant is drawn with the lineage still present);
    the count of mutants until the R share falls below 1/2 is M_exit.
(c) Shadow pruning: all-R with one ALLC and one D injected at random sites;
    lifetimes in generations of each (censored at cap_gens).

    python3 src/lattice_rates.py --sides 32 64
"""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from game import Game
from abm import load_or_evaluate, njit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@njit(cache=True)
def _neighbours(side):
    N = side * side
    nb = np.empty((N, 4), np.int64)
    for s in range(N):
        x = s % side; y = s // side
        nb[s, 0] = y * side + (x + 1) % side
        nb[s, 1] = y * side + (x - 1 + side) % side
        nb[s, 2] = ((y + 1) % side) * side + x
        nb[s, 3] = ((y - 1 + side) % side) * side + x
    return nb


@njit(cache=True)
def _step(U, grid, nb, w, wts):
    """One death-birth event; returns (site, old class, new class)."""
    N = grid.shape[0]
    s = np.random.randint(N)
    m = -1e300
    for a in range(4):
        v = nb[s, a]; cv = grid[v]; pay = 0.0
        for b in range(4):
            pay += U[cv, grid[nb[v, b]]]
        wts[a] = pay / 4.0
        if wts[a] > m: m = wts[a]
    tot = 0.0
    for a in range(4):
        wts[a] = np.exp(w * (wts[a] - m)); tot += wts[a]
    u = np.random.random() * tot; acc = 0.0; win = 3
    for a in range(4):
        acc += wts[a]
        if u <= acc:
            win = a; break
    old = grid[s]; new = grid[nb[s, win]]
    grid[s] = new
    return s, old, new


@njit(cache=True)
def _enter(U, side, w, iD, iR, trials, cap_gens, seed):
    np.random.seed(seed)
    N = side * side; nb = _neighbours(side); wts = np.empty(4)
    succ = 0; fail = 0; undec = 0; t_succ = 0.0
    for tr in range(trials):
        grid = np.full(N, iD, np.int64)
        grid[np.random.randint(N)] = iR
        cnt = 1; ev = 0; out = -1
        while ev < cap_gens * N:
            s, old, new = _step(U, grid, nb, w, wts)
            if old == iR: cnt -= 1
            if new == iR: cnt += 1
            ev += 1
            if cnt == 0:
                out = 0; break
            if 2 * cnt >= N:
                out = 1; break
        if out == 1:
            succ += 1; t_succ += ev / N
        elif out == 0:
            fail += 1
        else:
            undec += 1
    return succ, fail, undec, (t_succ / succ if succ > 0 else 0.0)


@njit(cache=True)
def _exit(U, mu_cdf, side, w, iR, K, trials, cap_mut, max_mut, seed):
    np.random.seed(seed)
    N = side * side; nb = _neighbours(side); wts = np.empty(4)
    M = np.zeros(trials, np.int64); gens = np.zeros(trials); last = np.zeros(trials, np.int64)
    for tr in range(trials):
        grid = np.full(N, iR, np.int64)
        counts = np.zeros(K, np.int64); counts[iR] = N
        nm = 0; ev_tot = 0; done = False
        while nm < max_mut and not done:
            u = np.random.random(); m = K - 1
            for i in range(K):
                if u <= mu_cdf[i]:
                    m = i; break
            nm += 1
            s = np.random.randint(N)
            counts[grid[s]] -= 1; grid[s] = m; counts[m] += 1
            if 2 * counts[iR] < N:
                done = True; last[tr] = m; break
            if m == iR:
                continue
            ev = 0
            while ev < cap_mut * N:
                s, old, new = _step(U, grid, nb, w, wts)
                counts[old] -= 1; counts[new] += 1
                ev += 1; ev_tot += 1
                if counts[m] == 0 or counts[m] == N:
                    break
                if ev % N == 0 and 2 * counts[iR] < N:
                    done = True; last[tr] = m; break
        M[tr] = nm; gens[tr] = ev_tot / N
    return M, gens, last


@njit(cache=True)
def _prune(U, side, w, iR, iC, iD, trials, cap_gens, seed):
    np.random.seed(seed)
    N = side * side; nb = _neighbours(side); wts = np.empty(4)
    lifeC = np.zeros(trials); lifeD = np.zeros(trials)
    for tr in range(trials):
        grid = np.full(N, iR, np.int64)
        a = np.random.randint(N); b = np.random.randint(N)
        while b == a: b = np.random.randint(N)
        grid[a] = iC; grid[b] = iD
        cC = 1; cD = 1; ev = 0; tC = -1.0; tD = -1.0
        while ev < cap_gens * N and (cC > 0 or cD > 0):
            s, old, new = _step(U, grid, nb, w, wts)
            if old == iC: cC -= 1
            if new == iC: cC += 1
            if old == iD: cD -= 1
            if new == iD: cD += 1
            ev += 1
            if cC == 0 and tC < 0: tC = ev / N
            if cD == 0 and tD < 0: tD = ev / N
        lifeC[tr] = tC if tC >= 0 else cap_gens
        lifeD[tr] = tD if tD >= 0 else cap_gens
    return lifeC, lifeD


def main(a):
    game = Game.load(os.path.join(ROOT, 'games', a.game + '.yaml'))
    L, ids, reps, members, mu, Uc, PCC, PEX, names, div = load_or_evaluate(game, a.n, verbose=False)
    K = len(reps); idx = {n: i for i, n in enumerate(names)}
    iD, iC = idx['D'], idx['C']
    Rs = ['THEM(^C)', 'or(X,THEM(ME))', 'THEM(^ROLE)']
    mu_cdf = np.cumsum(mu)
    out = {'enter': [], 'exit': [], 'prune': []}
    lines = ['# Per-mutant rates on the torus (death-birth, von Neumann, weak n=%d with ROLE, %d classes, w=%g, mutation off inside trials)' % (a.n, K, a.w), '']
    lines += ['## (a) rho_enter: one R in all-D, success = R share >= 1/2 (%d trials, cap %d*side generations)' % (a.trials_enter, a.cap_factor), '',
              '| R | side | rho_enter | undecided | mean generations to 1/2 |', '|---|---|---|---|---|']
    for R in Rs:
        for side in a.sides:
            t = time.time()
            succ, fail, undec, tmean = _enter(Uc, side, a.w, iD, idx[R], a.trials_enter, a.cap_factor * side, 1)
            rho = succ / a.trials_enter
            out['enter'].append(dict(R=R, side=side, rho=rho, succ=succ, fail=fail, undecided=undec, t_success=tmean, time_s=time.time() - t))
            lines.append('| `%s` | %d | %.4f (%d/%d) | %d | %.0f |' % (R, side, rho, succ, a.trials_enter, undec, tmean))
            print(lines[-1], flush=True)
    lines += ['', '## (b) M_exit: mutants from mu one at a time until the R share < 1/2 (%d trials; per-mutant cap %d generations)' % (a.trials_exit, a.cap_mut), '',
              '| R | side | M_exit mean ± sd | median | generations mean | last mutant (top 3) |', '|---|---|---|---|---|---|']
    for R in Rs:
        for side in a.sides:
            t = time.time()
            M, gens, last = _exit(Uc, mu_cdf, side, a.w, idx[R], K, a.trials_exit, a.cap_mut, a.max_mut, 2)
            lst = {}
            for m in last: lst[names[int(m)]] = lst.get(names[int(m)], 0) + 1
            top = ', '.join('`%s` %d' % kv for kv in sorted(lst.items(), key=lambda kv: -kv[1])[:3])
            out['exit'].append(dict(R=R, side=side, M=M.tolist(), gens=gens.tolist(), last=[names[int(m)] for m in last], time_s=time.time() - t))
            lines.append('| `%s` | %d | %.1f ± %.1f | %.0f | %.0f | %s |' % (R, side, M.mean(), M.std(), np.median(M), gens.mean(), top))
            print(lines[-1], flush=True)
    lines += ['', '## (c) Shadow pruning: all-R plus one ALLC and one D; lifetimes in generations (%d trials; censored at %d)' % (a.trials_prune, a.cap_prune), '',
              '| R | side | ALLC lifetime mean ± sd | ALLC median | ALLC censored | D lifetime mean ± sd | D median | D censored |', '|---|---|---|---|---|---|---|---|']
    for R in Rs[:2]:
        for side in a.sides:
            t = time.time()
            lifeC, lifeD = _prune(Uc, side, a.w, idx[R], iC, iD, a.trials_prune, a.cap_prune, 3)
            out['prune'].append(dict(R=R, side=side, lifeC=lifeC.tolist(), lifeD=lifeD.tolist(), time_s=time.time() - t))
            lines.append('| `%s` | %d | %.1f ± %.1f | %.1f | %d | %.2f ± %.2f | %.2f | %d |' % (R, side, lifeC.mean(), lifeC.std(), np.median(lifeC), int((lifeC >= a.cap_prune).sum()), lifeD.mean(), lifeD.std(), np.median(lifeD), int((lifeD >= a.cap_prune).sum())))
            print(lines[-1], flush=True)
    path = os.path.join(ROOT, 'runs', 'lattice_rates.md')
    open(path, 'w').write('\n'.join(lines) + '\n')
    json.dump(out, open(path.replace('.md', '.json'), 'w'))
    print('\n'.join(lines))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', default='pd'); ap.add_argument('--n', type=int, default=6); ap.add_argument('--w', type=float, default=0.3)
    ap.add_argument('--sides', type=int, nargs='+', default=[32, 64])
    ap.add_argument('--trials_enter', type=int, default=2000); ap.add_argument('--cap_factor', type=int, default=20)
    ap.add_argument('--trials_exit', type=int, default=50); ap.add_argument('--cap_mut', type=int, default=1000); ap.add_argument('--max_mut', type=int, default=100000)
    ap.add_argument('--trials_prune', type=int, default=500); ap.add_argument('--cap_prune', type=int, default=5000)
    main(ap.parse_args())
