"""Spatial structure: death-birth Moran on a torus, and a complete-graph control.

Lattice: L x L torus, von Neumann neighbourhood (k = 4).  Each event a random
site dies and its 4 neighbours compete to fill it with probability
proportional to exp(w * payoff), payoff being the mean over the neighbour's
own 4 interactions (class-level payoff matrix, role draw averaged); with
probability eps the newborn is a fresh draw from mu over the behavioural
classes, otherwise a copy of the winner.  A generation is N deaths.
Control: the same death-birth rule on the complete graph (every other agent
competes, payoff = mean over all its interactions).

Statistics per sampled generation: P(C,C) and P(exploit) over the graph's
edges, class shares (THEM(^C), ALLC, D, THEM(^D)), mean payoff.  One
snapshot PNG per seed at the end of sampling (class -> colour).

    python3 src/lattice.py --epsN 0.1 1 --seeds 5 --control_epsN 1
"""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from game import Game
from abm import load_or_evaluate, njit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@njit(cache=True)
def _lattice(U, PCC, PEX, mu_cdf, side, w, eps, burn, sample, init_class, seed, track, K):
    np.random.seed(seed)
    N = side * side
    grid = np.full(N, init_class, np.int64)
    nb = np.empty((N, 4), np.int64)
    for s in range(N):
        x = s % side; y = s // side
        nb[s, 0] = y * side + (x + 1) % side
        nb[s, 1] = y * side + (x - 1 + side) % side
        nb[s, 2] = ((y + 1) % side) * side + x
        nb[s, 3] = ((y - 1 + side) % side) * side + x
    T = len(track)
    S_share = np.zeros(T); S_cc = 0.0; S_ex = 0.0; S_pay = 0.0; nsamp = 0
    wts = np.empty(4)
    n_events = (burn + sample) * N
    for ev in range(n_events):
        s = np.random.randint(N)
        tot = 0.0; m = -1e300
        for a in range(4):
            v = nb[s, a]; cv = grid[v]; pay = 0.0
            for b in range(4):
                pay += U[cv, grid[nb[v, b]]]
            wts[a] = pay / 4.0
            if wts[a] > m: m = wts[a]
        for a in range(4):
            wts[a] = np.exp(w * (wts[a] - m)); tot += wts[a]
        u = np.random.random() * tot; acc = 0.0; win = 3
        for a in range(4):
            acc += wts[a]
            if u <= acc:
                win = a; break
        if np.random.random() < eps:
            u = np.random.random(); child = K - 1
            for i in range(K):
                if u <= mu_cdf[i]:
                    child = i; break
        else:
            child = grid[nb[s, win]]
        grid[s] = child
        if ev >= burn * N and (ev + 1) % N == 0:
            cc = 0.0; ex = 0.0; pay = 0.0
            for v in range(N):
                cv = grid[v]
                for b in range(2):                  # right and down: each undirected edge once
                    cu = grid[nb[v, 2 * b]]
                    cc += PCC[cv, cu]; ex += PEX[cv, cu]; pay += U[cv, cu] + U[cu, cv]
            S_cc += cc / (2 * N); S_ex += ex / (2 * N); S_pay += pay / (4 * N)
            for t in range(T):
                c = 0
                for v in range(N):
                    if grid[v] == track[t]: c += 1
                S_share[t] += c / N
            nsamp += 1
    return S_cc / nsamp, S_ex / nsamp, S_pay / nsamp, S_share / nsamp, grid


@njit(cache=True)
def _complete(U, PCC, PEX, mu_cdf, N, w, eps, burn, sample, init_class, seed, track, K):
    """Death-birth on the complete graph, class counts."""
    np.random.seed(seed)
    counts = np.zeros(K, np.int64); counts[init_class] = N
    fit = np.zeros(K); wts = np.zeros(K)
    T = len(track)
    S_share = np.zeros(T); S_cc = 0.0; S_ex = 0.0; S_pay = 0.0; nsamp = 0
    n_events = (burn + sample) * N
    for ev in range(n_events):
        # death
        u = np.random.random() * N; acc = 0.0; victim = -1
        for i in range(K):
            if counts[i] > 0:
                acc += counts[i]
                if u <= acc:
                    victim = i; break
        counts[victim] -= 1
        # competitors: the remaining N-1, payoff = mean over their N-2 interactions
        m = -1e300
        for i in range(K):
            if counts[i] == 0:
                wts[i] = 0.0; continue
            s = 0.0
            for j in range(K):
                if counts[j] > 0: s += counts[j] * U[i, j]
            s -= U[i, i]
            fit[i] = s / (N - 2)
            if fit[i] > m: m = fit[i]
        tot = 0.0
        for i in range(K):
            if counts[i] > 0:
                wts[i] = counts[i] * np.exp(w * (fit[i] - m)); tot += wts[i]
        u = np.random.random() * tot; acc = 0.0; parent = -1
        for i in range(K):
            if counts[i] > 0:
                acc += wts[i]
                if u <= acc:
                    parent = i; break
        if np.random.random() < eps:
            u = np.random.random(); child = K - 1
            for i in range(K):
                if u <= mu_cdf[i]:
                    child = i; break
        else:
            child = parent
        counts[child] += 1
        if ev >= burn * N and (ev + 1) % N == 0:
            cc = 0.0; ex = 0.0; pay = 0.0
            for i in range(K):
                if counts[i] == 0: continue
                for j in range(K):
                    if counts[j] == 0: continue
                    nn = counts[i] * counts[j] if i != j else counts[i] * (counts[i] - 1)
                    cc += nn * PCC[i, j]; ex += nn * PEX[i, j]; pay += nn * U[i, j]
            S_cc += cc / (N * (N - 1)); S_ex += ex / (N * (N - 1)); S_pay += pay / (N * (N - 1))
            for t in range(T):
                S_share[t] += counts[track[t]] / N
            nsamp += 1
    return S_cc / nsamp, S_ex / nsamp, S_pay / nsamp, S_share / nsamp, counts


def snapshot(grid, side, names, track_names, path, title):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    palette = {'D': '#222222', 'C': '#2ca02c', 'THEM(^C)': '#1f77b4', 'THEM(^D)': '#d62728', 'X': '#ffdd57'}
    idx = {nm: i for i, nm in enumerate(names)}
    img = np.full(len(grid), 5)
    for nm, col in zip(palette.keys(), range(5)):
        if nm in idx: img[grid == idx[nm]] = col
    cmap = ListedColormap(list(palette.values()) + ['#cccccc'])
    fig, ax = plt.subplots(figsize=(4.4, 4.4))
    ax.imshow(img.reshape(side, side), cmap=cmap, vmin=0, vmax=5, interpolation='nearest')
    ax.set_xticks([]); ax.set_yticks([]); ax.set_title(title, fontsize=9)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=c, label=n) for n, c in palette.items()] + [Patch(color='#cccccc', label='other')],
              loc='upper center', bbox_to_anchor=(0.5, -0.02), ncol=3, fontsize=7, frameon=False)
    fig.tight_layout(); fig.savefig(path, dpi=110); plt.close(fig)


def main(a):
    game = Game.load(os.path.join(ROOT, 'games', a.game + '.yaml'))
    L, ids, reps, members, mu, Uc, PCC, PEX, names, div = load_or_evaluate(game, a.n)
    K = len(reps)
    C, D = game.actions[-1], game.actions[0]
    track_names = ['THEM(^%s)' % C, C, D, 'THEM(^%s)' % D]
    track = np.array([names.index(t) for t in track_names], np.int64)
    iD = names.index(D)
    mu_cdf = np.cumsum(mu)
    N = a.side * a.side
    os.makedirs(os.path.join(ROOT, 'runs', 'spatial'), exist_ok=True)
    rows = []
    for epsN in a.epsN:
        for seed in range(a.seeds):
            t = time.time()
            cc, ex, pay, sh, grid = _lattice(Uc, PCC, PEX, mu_cdf, a.side, a.w, epsN / N, a.burn, a.sample, iD, seed, track, K)
            png = os.path.join(ROOT, 'runs', 'spatial', 'snap_epsN%g_seed%d.png' % (epsN, seed))
            snapshot(grid, a.side, names, track_names, png, '%dx%d torus, epsN=%g, seed %d, end of sampling' % (a.side, a.side, epsN, seed))
            rows.append(dict(graph='lattice', epsN=epsN, seed=seed, pcc=cc, pexploit=ex, mean_payoff=pay, **{'share_' + n: float(v) for n, v in zip(track_names, sh)}, snapshot=os.path.relpath(png, ROOT), time_s=time.time() - t))
            print('lattice epsN=%g seed=%d: P(C,C) %.4f P(exploit) %.4f payoff %.4f shares %s (%.0fs)' % (epsN, seed, cc, ex, pay, np.round(sh, 4).tolist(), time.time() - t), flush=True)
    for epsN in a.control_epsN:
        for seed in range(a.seeds):
            t = time.time()
            cc, ex, pay, sh, counts = _complete(Uc, PCC, PEX, mu_cdf, N, a.w, epsN / N, a.burn, a.sample, iD, seed, track, K)
            rows.append(dict(graph='complete', epsN=epsN, seed=seed, pcc=cc, pexploit=ex, mean_payoff=pay, **{'share_' + n: float(v) for n, v in zip(track_names, sh)}, time_s=time.time() - t))
            print('complete epsN=%g seed=%d: P(C,C) %.4f P(exploit) %.4f payoff %.4f shares %s (%.0fs)' % (epsN, seed, cc, ex, pay, np.round(sh, 4).tolist(), time.time() - t), flush=True)
    lines = ['# Spatial structure: death-birth Moran, %s, weak n=%d with ROLE (%d classes), w=%g, N=%d, burn-in %d generations, %d sampled, %d seeds' % (
        a.game, a.n, K, a.w, N, a.burn, a.sample, a.seeds), '',
        '| graph | epsN | P(C,C) | P(exploit) | mean payoff | THEM(^C) | ALLC | D | THEM(^D) |', '|---|---|---|---|---|---|---|---|---|']
    for graph in ['lattice', 'complete']:
        for epsN in (a.epsN if graph == 'lattice' else a.control_epsN):
            sub = [r for r in rows if r['graph'] == graph and r['epsN'] == epsN]
            f = lambda key: '%.4f ± %.4f' % (np.mean([r[key] for r in sub]), np.std([r[key] for r in sub]))
            lines.append('| %s | %g | %s | %s | %s | %s | %s | %s | %s |' % (graph, epsN, f('pcc'), f('pexploit'), f('mean_payoff'), f('share_' + track_names[0]), f('share_' + track_names[1]), f('share_' + track_names[2]), f('share_' + track_names[3])))
    lines.append(''); lines.append('Snapshots: ' + ', '.join(r['snapshot'] for r in rows if r['graph'] == 'lattice'))
    out = os.path.join(ROOT, 'runs', 'lattice_%s_w%g.md' % (a.game, a.w))
    open(out, 'w').write('\n'.join(lines) + '\n')
    json.dump(rows, open(out.replace('.md', '.json'), 'w'), indent=1)
    print('\n'.join(lines))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', default='pd')
    ap.add_argument('--n', type=int, default=6)
    ap.add_argument('--side', type=int, default=32)
    ap.add_argument('--w', type=float, default=0.3)
    ap.add_argument('--epsN', type=float, nargs='+', default=[0.1, 1.0])
    ap.add_argument('--control_epsN', type=float, nargs='+', default=[1.0])
    ap.add_argument('--seeds', type=int, default=5)
    ap.add_argument('--burn', type=int, default=10000)
    ap.add_argument('--sample', type=int, default=100000)
    main(ap.parse_args())
