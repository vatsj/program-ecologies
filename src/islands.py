"""Island model: migration replaces mutation (THEORY.md §9.5, conjectures A and B').

I islands of N agents on a connected graph (complete or ring).  Each event a
uniformly random agent dies.  With probability 1 - m it is replaced by the
offspring of a parent drawn from its own island with probability
proportional to exp(w * fitness); with probability m by the offspring of a
parent drawn the same way from a uniformly random neighbouring island
(fitness evaluated at home).  Fitness is the mean payoff against the other
N - 1 agents of the parent's own island.  No mutation: every behavioural
class present at the end was seeded at the start.  A generation is I * N
events.

Seedings (every program of L_n appears at least once; programs in one
behavioural class are interchangeable when nothing new is ever drawn, so the
simulation runs on classes with multiplicities):
  programs  - every program once, the remaining slots uniform over programs,
              shuffled across all slots;
  prior     - every program once, the remaining slots from mu, shuffled;
  hostile   - every program once, the remaining slots A_0 (all-D / all-
              Straight), shuffled;
  clustered - as 'programs' but dealt in class order, so each class fills
              as few islands as possible.

Frozen: when every pair of surviving classes has the same payoff the
fitnesses are equal for ever, the outcome can no longer change, and the run
stops.

The rare-migration mean-field object (the migration game): with
monomorphic islands and a complete graph, island-state frequencies follow
replicator dynamics of the antisymmetric game A = rho - rho^T, where
rho[q, a] is the Moran fixation probability of one q migrant on an all-a
island.  Its equilibrium set (A x <= 0) is computed by migration_game().

    python3 src/islands.py --game pd --graphs complete ring --mN 0.1 1 --seedings programs prior hostile clustered --reps 10
"""
import argparse, json, os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from game import Game
from abm import load_or_evaluate, njit
from chain import fixation

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ------------------------------------------------------------------ static
def rho_matrix(U, N, w):
    K = U.shape[0]
    rho = np.zeros((K, K))
    for q in range(K):
        for a in range(K):
            if q != a:
                rho[q, a] = fixation(U[q, q], U[q, a], U[a, q], U[a, a], N, w, N)
    return rho


def migration_game(U, N, w):
    """Equilibrium set of the symmetric zero-sum game A = rho - rho^T:
    one point x* and, per class, the range of x_q over the set."""
    from scipy.optimize import linprog
    K = U.shape[0]
    rho = rho_matrix(U, N, w)
    A = rho - rho.T
    kw = dict(A_ub=A, b_ub=np.full(K, 1e-7), A_eq=np.ones((1, K)), b_eq=[1], bounds=[(0, 1)] * K, method='highs')
    x = linprog(np.zeros(K), **kw).x
    lo = np.zeros(K); hi = np.zeros(K)
    for q in range(K):
        c = np.zeros(K); c[q] = 1
        lo[q] = linprog(c, **kw).fun
        hi[q] = -linprog(-c, **kw).fun
    return rho, x, lo, hi


# ------------------------------------------------------------------ dynamics
@njit(cache=True)
def _sample_parent(counts, paysum, U, pres, npres, isl, N, w):
    m = -1e300
    for t in range(npres[isl]):
        k = pres[isl, t]
        f = (paysum[isl, k] - U[k, k]) / (N - 1)
        if f > m: m = f
    tot = 0.0
    for t in range(npres[isl]):
        k = pres[isl, t]
        f = (paysum[isl, k] - U[k, k]) / (N - 1)
        tot += counts[isl, k] * np.exp(w * (f - m))
    u = np.random.random() * tot; acc = 0.0
    for t in range(npres[isl]):
        k = pres[isl, t]
        f = (paysum[isl, k] - U[k, k]) / (N - 1)
        acc += counts[isl, k] * np.exp(w * (f - m))
        if u <= acc:
            return k
    return pres[isl, npres[isl] - 1]


@njit(cache=True)
def _run(U, PCC, init, nbr, nnbr, N, w, m, gens, every, seed, iR, iC, eff, dwl_edges):
    """init: (I, K) counts.  nbr: (I, maxdeg) neighbour lists.  Returns
    traces and summaries (see run_one)."""
    np.random.seed(seed)
    I, K = init.shape
    UT = np.ascontiguousarray(U.T)
    counts = init.copy()
    paysum = np.zeros((I, K))
    pres = np.zeros((I, K), np.int64); npres = np.zeros(I, np.int64); pos = -np.ones((I, K), np.int64)
    for i in range(I):
        for k in range(K):
            if counts[i, k] > 0:
                pres[i, npres[i]] = k; pos[i, k] = npres[i]; npres[i] += 1
                for j in range(K):
                    paysum[i, j] += counts[i, k] * U[j, k]
    nsamp = gens // every
    tr_cc = np.zeros(nsamp); tr_pay = np.zeros(nsamp)
    tr_R = np.zeros(nsamp); tr_C = np.zeros(nsamp); tr_npres = np.zeros(nsamp, np.int64)
    dom_time = np.zeros(K)                  # island-samples with class k dominant (> 1/2), second half
    trans = np.zeros((K, K), np.int64)      # dominant-class changes between samples (any time)
    prev_dom = -np.ones(I, np.int64)
    isl_cc_hist = np.zeros(11)              # island P(C,C) histogram, second half
    nb = dwl_edges.shape[0] - 1
    isl_dwl_hist = np.zeros(nb)             # island deadweight-loss histogram, second half
    ext_R = -1; ext_C = -1; frozen_at = -1
    glob = np.zeros(K, np.int64)
    events_per_gen = I * N
    s = 0
    for g in range(gens):
        for e in range(events_per_gen):
            i = np.random.randint(I)
            src = i
            if np.random.random() < m:
                src = nbr[i, np.random.randint(nnbr[i])]
            child = _sample_parent(counts, paysum, U, pres, npres, src, N, w)
            # victim uniform on island i
            u = np.random.randint(N); acc = 0; victim = pres[i, 0]
            for t in range(npres[i]):
                k = pres[i, t]; acc += counts[i, k]
                if u < acc:
                    victim = k; break
            if victim == child:
                continue
            counts[i, victim] -= 1
            if counts[i, victim] == 0:
                p = pos[i, victim]; last = pres[i, npres[i] - 1]
                pres[i, p] = last; pos[i, last] = p; pos[i, victim] = -1; npres[i] -= 1
            if counts[i, child] == 0:
                pres[i, npres[i]] = child; pos[i, child] = npres[i]; npres[i] += 1
            counts[i, child] += 1
            for j in range(K):
                paysum[i, j] += UT[child, j] - UT[victim, j]
        if (g + 1) % every == 0 and s < nsamp:
            cc_tot = 0.0; pay_tot = 0.0
            for k in range(K): glob[k] = 0
            for i in range(I):
                cc = 0.0; pay = 0.0; dom = -1
                for t in range(npres[i]):
                    a = pres[i, t]; glob[a] += counts[i, a]
                    if 2 * counts[i, a] > N: dom = a
                    pay += counts[i, a] * (paysum[i, a] - U[a, a]) / (N - 1)
                    for t2 in range(npres[i]):
                        b = pres[i, t2]
                        nn = counts[i, a] * counts[i, b] if a != b else counts[i, a] * (counts[i, a] - 1)
                        cc += nn * PCC[a, b]
                cc /= N * (N - 1); pay /= N
                cc_tot += cc; pay_tot += pay
                if 2 * s >= nsamp:
                    if dom >= 0: dom_time[dom] += 1
                    isl_cc_hist[min(10, int(cc * 10))] += 1
                    dwl = eff - pay
                    for b in range(nb):
                        if dwl < dwl_edges[b + 1]:
                            isl_dwl_hist[b] += 1; break
                if dom >= 0:
                    if prev_dom[i] >= 0 and prev_dom[i] != dom:
                        trans[prev_dom[i], dom] += 1
                    prev_dom[i] = dom
            tr_cc[s] = cc_tot / I; tr_pay[s] = pay_tot / I
            tr_R[s] = glob[iR] / (I * N); tr_C[s] = glob[iC] / (I * N)
            npz = 0
            for k in range(K):
                if glob[k] > 0: npz += 1
            tr_npres[s] = npz
            if ext_R < 0 and glob[iR] == 0: ext_R = g + 1
            if ext_C < 0 and glob[iC] == 0: ext_C = g + 1
            # frozen: all surviving classes pairwise payoff-identical
            lo = 1e300; hi = -1e300
            for a in range(K):
                if glob[a] == 0: continue
                for b in range(K):
                    if glob[b] == 0: continue
                    if U[a, b] < lo: lo = U[a, b]
                    if U[a, b] > hi: hi = U[a, b]
            s += 1
            if hi - lo < 1e-12:
                frozen_at = g + 1
                # fill the remaining trace with the frozen values
                for s2 in range(s, nsamp):
                    tr_cc[s2] = tr_cc[s - 1]; tr_pay[s2] = tr_pay[s - 1]
                    tr_R[s2] = tr_R[s - 1]; tr_C[s2] = tr_C[s - 1]; tr_npres[s2] = tr_npres[s - 1]
                break
    return tr_cc, tr_pay, tr_R, tr_C, tr_npres, dom_time, trans, isl_cc_hist, isl_dwl_hist, ext_R, ext_C, frozen_at, counts


def graph(kind, I):
    if kind == 'complete':
        nbr = np.array([[j for j in range(I) if j != i] for i in range(I)], np.int64)
    elif kind == 'ring':
        nbr = np.array([[(i - 1) % I, (i + 1) % I] for i in range(I)], np.int64)
    else:
        raise ValueError(kind)
    return nbr, np.full(I, nbr.shape[1], np.int64)


def seed_counts(kind, sizes, mu, iA0, I, N, rng):
    """(I, K) initial counts; every program of the language appears once."""
    K = len(sizes)
    slots = np.repeat(np.arange(K), sizes)
    extra = I * N - len(slots)
    if extra < 0:
        raise ValueError('I*N = %d < %d programs' % (I * N, len(slots)))
    if kind in ('programs', 'clustered'):
        add = rng.choice(K, size=extra, p=sizes / sizes.sum())
    elif kind == 'prior':
        add = rng.choice(K, size=extra, p=mu / mu.sum())
    elif kind == 'hostile':
        add = np.full(extra, iA0)
    else:
        raise ValueError(kind)
    slots = np.concatenate([slots, add])
    if kind == 'clustered':
        slots = np.sort(slots)
    else:
        rng.shuffle(slots)
    init = np.zeros((I, K), np.int64)
    for i in range(I):
        for k in slots[i * N:(i + 1) * N]:
            init[i, k] += 1
    return init


# ------------------------------------------------------------------ driver
TRACE_THIN = 50                 # stored traces keep every 50th sample (one per 1,000 generations at every = 20)
DWL_EDGES = np.array([-1e9, 0.05, 0.1, 0.25, 0.45, 0.55, 0.75, 1.05, 1e9])
_CTX = {}


def _load(game_name, norole):
    key = (game_name, norole)
    if key not in _CTX:
        game = Game.load(os.path.join(ROOT, 'games', game_name + '.yaml'))
        if norole:
            game.role = False; game.nroles = 1
        L, ids, reps, members, mu, U, PCC, PEX, names, div = load_or_evaluate(game, 6, verbose=False)
        _CTX[key] = (game, np.ascontiguousarray(U), np.ascontiguousarray(PCC), names, np.array([len(mm) for mm in members]), mu)
    return _CTX[key]


def _tag(game_name, norole, extra):
    suffix = '_norole' if norole and not game_name.endswith('_norole') else ''
    return game_name + suffix + (('_' + extra) if extra else '')


def run_one(job):
    game_name, norole, graph_kind, mN, seeding, rep, I, N, w, gens, every = job
    game, U, PCC, names, sizes, mu = _load(game_name, norole)
    A0, A1 = game.actions[0], game.actions[-1]
    iA0 = names.index(A0); iC = names.index(A1)
    iR = names.index('THEM(^%s)' % A1)
    rng = np.random.default_rng(1000003 * rep + 7919 * ['programs', 'prior', 'hostile', 'clustered'].index(seeding) + 17)
    init = seed_counts(seeding, sizes, mu, iA0, I, N, rng)
    nbr, nnbr = graph(graph_kind, I)
    t = time.time()
    out = _run(U, PCC, init, nbr, nnbr, N, w, mN / N, gens, every, 12345 + rep, iR, iC, game.efficient_symmetric(), DWL_EDGES)
    tr_cc, tr_pay, tr_R, tr_C, tr_npres, dom_time, trans, hist, dwl_hist, ext_R, ext_C, frozen_at, counts = out
    h = len(tr_cc) // 2
    glob = counts.sum(0)
    if frozen_at >= 0:
        # the loop stopped at the freeze; the frozen state holds for every
        # remaining sample, so add it to the second-half island statistics
        nsamp = len(tr_cc); s_frz = frozen_at // every
        missing = nsamp - max(s_frz, h)
        eff = game.efficient_symmetric()
        for i in range(counts.shape[0]):
            c = counts[i].astype(float)
            cc = (c @ PCC @ c - (c * np.diag(PCC)) @ np.ones_like(c)) / (N * (N - 1))
            fit = (U @ c - np.diag(U)) / (N - 1)
            pay = float(c @ fit) / N
            dom = np.nonzero(2 * counts[i] > N)[0]
            if len(dom): dom_time[dom[0]] += missing
            hist[min(10, int(cc * 10))] += missing
            dwl_hist[np.searchsorted(DWL_EDGES, eff - pay, side='right') - 1] += missing
    return dict(game=_tag(game_name, norole, ''), graph=graph_kind, mN=mN, seeding=seeding, rep=rep,
                pcc_2nd=float(tr_cc[h:].mean()), pay_2nd=float(tr_pay[h:].mean()),
                pcc_final=float(tr_cc[-1]), pay_final=float(tr_pay[-1]),
                R_2nd=float(tr_R[h:].mean()), C_2nd=float(tr_C[h:].mean()),
                ext_R=int(ext_R), ext_C=int(ext_C), frozen_at=int(frozen_at),
                npres_final=int(tr_npres[-1]),
                dom_time={names[k]: float(v) for k, v in enumerate(dom_time) if v > 0},
                trans=[(names[a], names[b], int(trans[a, b])) for a, b in zip(*np.nonzero(trans))],
                isl_cc_hist=hist.tolist(), isl_dwl_hist=dwl_hist.tolist(),
                final_classes={names[k]: int(v) for k, v in enumerate(glob) if v > 0},
                trace_every=every * TRACE_THIN, trace_cc=tr_cc[::TRACE_THIN].tolist(), trace_pay=tr_pay[::TRACE_THIN].tolist(),
                trace_R=tr_R[::TRACE_THIN].tolist(), trace_C=tr_C[::TRACE_THIN].tolist(),
                time_s=time.time() - t)


def main(a):
    jobs = [(a.game, a.norole, gk, mN, sd, r, a.I, a.N, a.w, a.gens, a.every)
            for gk in a.graphs for mN in a.mN for sd in a.seedings for r in range(a.reps)]
    _load(a.game, a.norole)          # build the evaluation cache once before forking
    tag = _tag(a.game, a.norole, a.tag)
    out = os.path.join(ROOT, 'runs', 'islands_%s.json' % tag)
    rows = []
    with Pool(a.procs) as pool:
        for r in pool.imap_unordered(run_one, jobs):
            rows.append(r)
            print('%s %s mN=%g %s rep %d: P(C,C) 2nd half %.3f final %.3f payoff %.3f R %.4f C %.4f extR %d extC %d frozen %d (%.0fs)' % (
                r['game'], r['graph'], r['mN'], r['seeding'], r['rep'], r['pcc_2nd'], r['pcc_final'], r['pay_2nd'],
                r['R_2nd'], r['C_2nd'], r['ext_R'], r['ext_C'], r['frozen_at'], r['time_s']), flush=True)
            json.dump(rows, open(out, 'w'))
    print('wrote', out)
    report(tag, a.game, a.norole)


# ------------------------------------------------------------------ report
def report(tag, game_name, norole):
    game, U, PCC, names, sizes, mu = _load(game_name, norole)
    rows = json.load(open(os.path.join(ROOT, 'runs', 'islands_%s.json' % tag)))
    A1 = game.actions[-1]
    iR = names.index('THEM(^%s)' % A1); iD = names.index(game.actions[0])
    eff = game.efficient_symmetric()
    cells = sorted({(r['graph'], r['mN'], r['seeding']) for r in rows}, key=lambda c: (c[0], c[1], ['programs', 'prior', 'hostile', 'clustered'].index(c[2])))
    L = ['# Island model: %s, weak L_6%s, I = 64 islands of N = 100, w = 0.3, no mutation' % (game_name, '' if game.role else ' without ROLE'), '',
         'Second-half statistics over a 2e5-generation horizon (frozen runs: the frozen state for the remainder). '
         'P(C,C) is P(%s,%s). DWL = %.3g - island mean payoff. "island-time DWL>0.1" is the fraction of island-samples '
         'with deadweight loss above 0.1. Outcome at freeze: coop = all surviving pairs (C,C); defect = all pairs (D,D); other = '
         'any other frozen outcome; live = not frozen at the horizon.' % (A1, A1, eff), '',
         '| graph | mN | seeding | runs | P(C,C) mean ± sd | payoff | island-time DWL>0.1 | frozen (median gen) | coop / defect / other / live | R extinct | ALLC share at gen 1000 | ALLC extinct |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for c in cells:
        sub = [r for r in rows if (r['graph'], r['mN'], r['seeding']) == c]
        pcc = np.array([r['pcc_2nd'] for r in sub]); pay = np.array([r['pay_2nd'] for r in sub])
        dw = np.array([r['isl_dwl_hist'] for r in sub]).sum(0); dwl_frac = dw[2:].sum() / dw.sum()
        fr = [r['frozen_at'] for r in sub if r['frozen_at'] >= 0]
        oc = dict(coop=0, defect=0, other=0, live=0)
        for r in sub:
            if r['frozen_at'] < 0: oc['live'] += 1
            elif r['pcc_final'] > 1 - 1e-9: oc['coop'] += 1
            elif r['pcc_final'] < 1e-9 and abs(r['pay_final'] - float(U[iD, iD])) < 1e-9: oc['defect'] += 1
            else: oc['other'] += 1
        k1000 = 1000 // sub[0]['trace_every']
        c1000 = np.mean([r['trace_C'][min(k1000, len(r['trace_C']) - 1)] for r in sub])
        L.append('| %s | %g | %s | %d | %.3f ± %.3f | %.3f | %.3f | %d (%s) | %d / %d / %d / %d | %d | %.4f | %d |' % (
            c[0], c[1], c[2], len(sub), pcc.mean(), pcc.std(), pay.mean(), dwl_frac, len(fr),
            '%d' % np.median(fr) if fr else '-', oc['coop'], oc['defect'], oc['other'], oc['live'],
            sum(r['ext_R'] >= 0 for r in sub), c1000, sum(r['ext_C'] >= 0 for r in sub)))
    # dominant classes, second half, pooled per cell
    L += ['', '## Dominant classes (share of second-half island-time with a class above 1/2; top 4 per cell)', '',
          '| graph | mN | seeding | classes (self P(C,C), self payoff): share |', '|---|---|---|---|']
    for c in cells:
        sub = [r for r in rows if (r['graph'], r['mN'], r['seeding']) == c]
        tot = sum(sum(r['isl_cc_hist']) for r in sub)
        agg = {}
        for r in sub:
            for k, v in r['dom_time'].items(): agg[k] = agg.get(k, 0) + v
        top = sorted(agg.items(), key=lambda kv: -kv[1])[:4]
        L.append('| %s | %g | %s | %s |' % (c[0], c[1], c[2], '; '.join('`%s` (%.2f, %.2f): %.3f' % (
            k, PCC[names.index(k), names.index(k)], U[names.index(k), names.index(k)], v / tot) for k, v in top)))
    # spoiler attribution: island transitions out of THEM(^C) dominance
    uRR = U[iR, iR]
    kinds = dict(faker=0, shadow=0, other=0); shadow_then = dict(exploiter=0, other=0)
    to_counts = {}
    for r in rows:
        for a, b, n in r['trans']:
            if a == names[iR]:
                q = names.index(b)
                if U[q, iR] > uRR + 1e-9: kinds['faker'] += n
                elif abs(U[q, iR] - uRR) < 1e-9 and abs(U[iR, q] - uRR) < 1e-9 and abs(U[q, q] - uRR) < 1e-9: kinds['shadow'] += n
                else: kinds['other'] += n
                to_counts[b] = to_counts.get(b, 0) + n
            else:
                qa = names.index(a); qb = names.index(b)
                # a shadow of THEM(^C) (on-path identical against it) taken by a class that exploits the shadow
                if abs(U[qa, iR] - uRR) < 1e-9 and abs(U[iR, qa] - uRR) < 1e-9 and abs(U[qa, qa] - uRR) < 1e-9 and qa != iR:
                    if U[qb, qa] > U[qa, qa] + 1e-9: shadow_then['exploiter'] += n
                    else: shadow_then['other'] += n
    L += ['', '## Exits from `%s` islands (pooled over all runs)' % names[iR], '',
          'Island dominant-class changes out of `%s`, sampled every 20 generations: to a faker (a class earning more against `%s` than it earns against itself) %d, '
          'to an on-path-identical shadow %d, to anything else %d. Shadow islands later taken by a class exploiting the shadow: %d; other exits from shadow islands: %d.' % (
              names[iR], names[iR], kinds['faker'], kinds['shadow'], kinds['other'], shadow_then['exploiter'], shadow_then['other']),
          '', 'Destinations: ' + ', '.join('`%s` %d' % kv for kv in sorted(to_counts.items(), key=lambda kv: -kv[1])[:10]) + '.']
    out = os.path.join(ROOT, 'runs', 'islands_%s.md' % tag)
    open(out, 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', default='pd')
    ap.add_argument('--norole', action='store_true')
    ap.add_argument('--graphs', nargs='+', default=['complete', 'ring'])
    ap.add_argument('--mN', type=float, nargs='+', default=[0.1, 1.0])
    ap.add_argument('--seedings', nargs='+', default=['programs', 'prior', 'hostile', 'clustered'])
    ap.add_argument('--reps', type=int, default=20)
    ap.add_argument('--I', type=int, default=64)
    ap.add_argument('--N', type=int, default=100)
    ap.add_argument('--w', type=float, default=0.3)
    ap.add_argument('--gens', type=int, default=200000)
    ap.add_argument('--every', type=int, default=20)
    ap.add_argument('--procs', type=int, default=9)
    ap.add_argument('--tag', default='')
    ap.add_argument('--report', action='store_true', help='only write the report from runs/islands_<tag>.json')
    a = ap.parse_args()
    if a.report:
        report(_tag(a.game, a.norole, a.tag), a.game, a.norole)
    else:
        main(a)
