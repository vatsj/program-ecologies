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

    python3 src/lattice.py --sides 32 64 128 --epsN 0.3 1 3 --epsN_big 1 --control_epsN 1 --seeds 5

Traces (every 100 generations: tracked shares and mean payoff) go to
runs/spatial/trace_<side>_epsN<e>_seed<s>.npy with one overlay plot per
(side, epsN).  A collapse event is the THEM(^C) share crossing 0.5 downward
after having exceeded 0.8; the ALLC share 500 generations before each
crossing is recorded.  Duty cycle = fraction of sampled generations with
THEM(^C) share > 0.5.
"""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from game import Game
from abm import load_or_evaluate, njit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@njit(cache=True)
def _lattice(U, PCC, PEX, mu_cdf, side, w, eps, burn, sample, init_class, seed, track, K, every):
    """Returns (P(C,C), P(exploit), mean payoff, shares, grid, trace, duty):
    trace[g] = (generation, tracked shares..., mean payoff) every `every`
    generations over burn-in and sampling; duty = fraction of sampled
    generations with the first tracked class (THEM(^C)) above 1/2."""
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
    S_share = np.zeros(T); S_cc = 0.0; S_ex = 0.0; S_pay = 0.0; nsamp = 0; duty = 0.0
    ntr = (burn + sample) // every
    trace = np.zeros((ntr, T + 2))
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
        if (ev + 1) % N == 0:
            g = (ev + 1) // N
            sampling = g > burn
            rec = (g % every == 0) and (g // every - 1 < ntr)
            if sampling or rec:
                cc = 0.0; ex = 0.0; pay = 0.0
                for v in range(N):
                    cv = grid[v]
                    for b in range(2):                  # right and down: each undirected edge once
                        cu = grid[nb[v, 2 * b]]
                        cc += PCC[cv, cu]; ex += PEX[cv, cu]; pay += U[cv, cu] + U[cu, cv]
                cnt = np.zeros(T)
                for v in range(N):
                    for t in range(T):
                        if grid[v] == track[t]: cnt[t] += 1
                if sampling:
                    S_cc += cc / (2 * N); S_ex += ex / (2 * N); S_pay += pay / (4 * N)
                    for t in range(T): S_share[t] += cnt[t] / N
                    if cnt[0] > N / 2: duty += 1.0
                    nsamp += 1
                if rec:
                    r = g // every - 1
                    trace[r, 0] = g
                    for t in range(T): trace[r, 1 + t] = cnt[t] / N
                    trace[r, T + 1] = pay / (4 * N)
    return S_cc / nsamp, S_ex / nsamp, S_pay / nsamp, S_share / nsamp, grid, trace, duty / nsamp


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


def collapses(trace, every, lag=500, high=0.8, cross=0.5):
    """Events: THEM(^C) share (column 1) crossing `cross` downward after having
    exceeded `high` since the previous event.  Returns the ALLC share (column 2)
    `lag` generations before each crossing."""
    T = trace[:, 1]; A = trace[:, 2]
    k = max(1, lag // every)
    armed = False; out = []
    for i in range(1, len(T)):
        if T[i] >= high: armed = True
        if armed and T[i] < cross <= T[i - 1]:
            out.append(float(A[i - k]) if i - k >= 0 else float(A[0]))
            armed = False
    return out


def trace_plot(traces, side, epsN, burn, path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 3.2))
    cols = plt.cm.tab10.colors
    for i, tr in enumerate(traces):
        ax.plot(tr[:, 0], tr[:, 1], color=cols[i % 10], lw=0.8, label='seed %d THEM(^C)' % i)
        ax.plot(tr[:, 0], tr[:, 2], color=cols[i % 10], lw=0.8, ls='--', alpha=0.7)
    ax.axvline(burn, color='k', lw=0.5, ls=':')
    ax.set_xlabel('generation (N deaths)'); ax.set_ylabel('share'); ax.set_ylim(0, 1)
    ax.set_title('%dx%d torus, epsN=%g: THEM(^C) (solid) and ALLC (dashed), %d seeds' % (side, side, epsN, len(traces)), fontsize=9)
    ax.legend(fontsize=6, ncol=5, loc='upper left', frameon=False)
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
    os.makedirs(os.path.join(ROOT, 'runs', 'spatial'), exist_ok=True)
    rows = []; cells = []
    for side in a.sides:
        N = side * side
        sample = a.sample if side < 128 else a.sample_128
        for epsN in (a.epsN if side == a.sides[0] else a.epsN_big):
            traces = []; events = []
            for seed in range(a.seeds):
                t = time.time()
                cc, ex, pay, sh, grid, trace, duty = _lattice(Uc, PCC, PEX, mu_cdf, side, a.w, epsN / N, a.burn, sample, iD, seed, track, K, a.every)
                np.save(os.path.join(ROOT, 'runs', 'spatial', 'trace_%d_epsN%g_seed%d.npy' % (side, epsN, seed)), trace)
                traces.append(trace); ev_s = collapses(trace[trace[:, 0] > a.burn], a.every); events += ev_s
                png = os.path.join(ROOT, 'runs', 'spatial', 'snap_%d_epsN%g_seed%d.png' % (side, epsN, seed))
                snapshot(grid, side, names, track_names, png, '%dx%d torus, epsN=%g, seed %d, end of sampling' % (side, side, epsN, seed))
                rows.append(dict(graph='lattice', side=side, N=N, epsN=epsN, seed=seed, pcc=cc, pexploit=ex, mean_payoff=pay, duty=duty, n_collapse=len(ev_s), pre_allc=ev_s,
                                 **{'share_' + n: float(v) for n, v in zip(track_names, sh)}, snapshot=os.path.relpath(png, ROOT), sample=sample, time_s=time.time() - t))
                print('lattice %d epsN=%g seed=%d: P(C,C) %.4f P(exploit) %.4f payoff %.4f duty %.3f collapses %d shares %s (%.0fs)' % (side, epsN, seed, cc, ex, pay, duty, len(ev_s), np.round(sh, 4).tolist(), time.time() - t), flush=True)
            tp = os.path.join(ROOT, 'runs', 'spatial', 'trace_%d_epsN%g.png' % (side, epsN))
            trace_plot(traces, side, epsN, a.burn, tp)
            cells.append((side, epsN, events, os.path.relpath(tp, ROOT)))
    for epsN in a.control_epsN:
        N = a.sides[0] * a.sides[0]
        for seed in range(a.seeds):
            t = time.time()
            cc, ex, pay, sh, counts = _complete(Uc, PCC, PEX, mu_cdf, N, a.w, epsN / N, a.burn, a.sample, iD, seed, track, K)
            rows.append(dict(graph='complete', side=a.sides[0], N=N, epsN=epsN, seed=seed, pcc=cc, pexploit=ex, mean_payoff=pay, **{'share_' + n: float(v) for n, v in zip(track_names, sh)}, time_s=time.time() - t))
            print('complete epsN=%g seed=%d: P(C,C) %.4f P(exploit) %.4f payoff %.4f shares %s (%.0fs)' % (epsN, seed, cc, ex, pay, np.round(sh, 4).tolist(), time.time() - t), flush=True)
    lines = ['# Spatial structure: death-birth Moran, %s, weak n=%d with ROLE (%d classes), w=%g, burn-in %d generations, %d sampled (%d at 128), %d seeds' % (
        a.game, a.n, K, a.w, a.burn, a.sample, a.sample_128, a.seeds), '',
        '| graph | side | N | epsN | P(C,C) | P(exploit) | mean payoff | duty cycle | collapses | pre-collapse ALLC (mean ± sd) | THEM(^C) | ALLC | D | THEM(^D) | trace |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for side, epsN, events, tp in cells:
        sub = [r for r in rows if r['graph'] == 'lattice' and r['side'] == side and r['epsN'] == epsN]
        f = lambda key: '%.4f ± %.4f' % (np.mean([r[key] for r in sub]), np.std([r[key] for r in sub]))
        pre = ('%.3f ± %.3f' % (np.mean(events), np.std(events))) if events else 'n/a'
        lines.append('| lattice | %d | %d | %g | %s | %s | %s | %s | %d | %s | %s | %s | %s | %s | %s |' % (side, side * side, epsN, f('pcc'), f('pexploit'), f('mean_payoff'), f('duty'), len(events), pre,
                     f('share_' + track_names[0]), f('share_' + track_names[1]), f('share_' + track_names[2]), f('share_' + track_names[3]), tp))
    for epsN in a.control_epsN:
        sub = [r for r in rows if r['graph'] == 'complete' and r['epsN'] == epsN]
        f = lambda key: '%.4f ± %.4f' % (np.mean([r[key] for r in sub]), np.std([r[key] for r in sub]))
        lines.append('| complete | — | %d | %g | %s | %s | %s | — | — | — | %s | %s | %s | %s | — |' % (a.sides[0] ** 2, epsN, f('pcc'), f('pexploit'), f('mean_payoff'),
                     f('share_' + track_names[0]), f('share_' + track_names[1]), f('share_' + track_names[2]), f('share_' + track_names[3])))
    lines.append(''); lines.append('Snapshots: ' + ', '.join(r['snapshot'] for r in rows if r['graph'] == 'lattice'))
    out = os.path.join(ROOT, 'runs', 'lattice_%s_w%g.md' % (a.game, a.w))
    open(out, 'w').write('\n'.join(lines) + '\n')
    json.dump(rows, open(out.replace('.md', '.json'), 'w'), indent=1)
    print('\n'.join(lines))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', default='pd')
    ap.add_argument('--n', type=int, default=6)
    ap.add_argument('--sides', type=int, nargs='+', default=[32, 64, 128], help='first side runs every --epsN; the others run --epsN_big')
    ap.add_argument('--epsN_big', type=float, nargs='+', default=[1.0])
    ap.add_argument('--every', type=int, default=100, help='trace record interval in generations')
    ap.add_argument('--sample_128', type=int, default=100000)
    ap.add_argument('--w', type=float, default=0.3)
    ap.add_argument('--epsN', type=float, nargs='+', default=[0.3, 1.0, 3.0])
    ap.add_argument('--control_epsN', type=float, nargs='+', default=[1.0])
    ap.add_argument('--seeds', type=int, default=5)
    ap.add_argument('--burn', type=int, default=10000)
    ap.add_argument('--sample', type=int, default=100000)
    main(ap.parse_args())
