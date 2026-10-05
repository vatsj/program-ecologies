"""Divide the dollar with k demand levels: evaluation, classes and partition
statistics (predictions/2026-10-02-dollar-partitions.md).

The game files are games/dollar3.yaml ({1/3, 1/2, 2/3}) and games/dollar5.yaml
({1/6, ..., 5/6}).  Demands that sum to at most 1 are paid; otherwise both get 0.

For every ordered pair of behavioural classes (a, b), JA[a, b] is the k x k
distribution over (a's demand, b's demand) in one match, averaged over the role
draw when ROLE is on.  Actions are independent given the pair, as in the payoff
model.  Partition statistics of a population state come from JA:
  split      unordered pair {d, 1 - d} of a compatible efficient match
  ineff      compatible match with d_i + d_j < 1
  clash      incompatible match (d_i + d_j > 1), both get 0
Deadweight loss per match is 1 - (sum of the two payoffs); per agent it is half that.

The evaluation is cached in runs/dollar_eval_<game>_n<n>[_norole].npz (gitignored).
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from dsl import Language
from game import Game
from evaluate import square_chunked
from abm import classes_from_U

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_game(name, role=True):
    import yaml
    path = os.path.join(ROOT, 'games', name + '.yaml')
    g = Game.load(path)
    cfg = yaml.safe_load(open(path))
    g.values = np.array([cfg['values'][a] for a in g.actions])
    if not role:
        g.role = False; g.nroles = 1
    return g


def joint_actions(game, Vfull):
    """(S, S, k, k): distribution over (i's level, j's level), role-averaged."""
    if game.role:
        A = 0.5 * (np.einsum('ija,jib->ijab', Vfull[:, :, 0], Vfull[:, :, 1])
                   + np.einsum('ija,jib->ijab', Vfull[:, :, 1], Vfull[:, :, 0]))
    else:
        A = np.einsum('ija,jib->ijab', Vfull[:, :, 0], Vfull[:, :, 0])
    return A


def load_or_evaluate(name, n, role=True, rows=300, verbose=True):
    game = load_game(name, role)
    L = Language('weak', n, k=game.k, names=game.actions, role=game.role)
    ids = L.ids()
    path = os.path.join(ROOT, 'runs', 'dollar_eval_%s_n%d%s.npz' % (name, n, '' if role else '_norole'))
    if os.path.exists(path):
        z = np.load(path, allow_pickle=True)
        reps, mu, U, JA = list(z['reps']), z['mu'], z['U'], z['JA']
        members = list(z['members']); div = float(z['div']); selfJA = z['selfJA']
    else:
        t0 = time.time()
        Uf, Vfull, div = square_chunked(L, game, ids, rows=rows, verbose=verbose)
        if verbose:
            print('evaluated %d programs (%.0fs), divergence %.4f' % (len(ids), time.time() - t0, div), flush=True)
        reps, members, mu = classes_from_U(L, ids, Uf)
        r = np.array(reps)
        sub = Vfull[np.ix_(r, r)]
        JA = joint_actions(game, sub)
        U = np.ascontiguousarray(Uf[np.ix_(r, r)])
        # self-play joint action of every member (to check that a class has one self-play partition)
        idx = np.arange(len(ids))
        if game.role:
            selfJA_all = 0.5 * (np.einsum('pa,pb->pab', Vfull[idx, idx, 0], Vfull[idx, idx, 1])
                                + np.einsum('pa,pb->pab', Vfull[idx, idx, 1], Vfull[idx, idx, 0]))
        else:
            selfJA_all = np.einsum('pa,pb->pab', Vfull[idx, idx, 0], Vfull[idx, idx, 0])
        bad = 0
        for c, mem in enumerate(members):
            d = np.abs(selfJA_all[mem] - selfJA_all[mem[0]][None]).max()
            if d > 1e-6:
                bad += 1
        if verbose:
            print('classes with members of different self-play outcome: %d of %d' % (bad, len(members)), flush=True)
        selfJA = np.array([selfJA_all[m[0]] for m in members])
        np.savez(path, reps=r, members=np.array(members, dtype=object), mu=mu, U=U, JA=JA, div=div, selfJA=selfJA,
                 mixed_classes=bad)
        del Vfull
    names = [L.src(ids[p]) for p in reps]
    return dict(game=game, L=L, ids=ids, reps=reps, members=members, mu=np.asarray(mu), U=np.asarray(U),
                JA=np.asarray(JA), names=names, div=div, sizes=np.array([len(m) for m in members], float))


def outcome_masks(game):
    """Masks over (k, k) level pairs: efficient splits by smaller share,
    inefficient-compatible and clash."""
    v = game.values; k = game.k
    S = v[:, None] + v[None, :]
    eff = np.abs(S - 1) < 1e-9
    ineff = S < 1 - 1e-9
    clash = S > 1 + 1e-9
    splits = {}
    for i in range(k):
        for j in range(k):
            if eff[i, j]:
                lo = min(v[i], v[j])
                key = '%s-%s' % (frac(lo), frac(1 - lo))
                splits.setdefault(key, np.zeros((k, k), bool))[i, j] = True
    return splits, ineff, clash


def frac(x):
    from fractions import Fraction
    return str(Fraction(x).limit_denominator(12))


def state_outcomes(JA, game, counts):
    """Outcome distribution of random matching in a population with class
    counts (K,) (without self-matching of an agent).  Returns dict of shares."""
    c = np.asarray(counts, float)
    N = c.sum()
    W = np.outer(c, c) - np.diag(c)
    W /= W.sum()
    D = np.einsum('ab,abij->ij', W, JA)
    splits, ineff, clash = outcome_masks(game)
    out = {s: float(D[m].sum()) for s, m in splits.items()}
    out['ineff'] = float(D[ineff].sum()); out['clash'] = float(D[clash].sum())
    v = game.values
    pay = (v[:, None] + v[None, :]) * (np.abs(v[:, None] + v[None, :]) <= 1 + 1e-9)
    out['dwl'] = float(0.5 * (1 - (D * pay).sum()))           # per agent, against the efficient 1/2
    return out


def eff_matrix(JA, game):
    """P(efficient match) per ordered class pair."""
    splits, ineff, clash = outcome_masks(game)
    m = np.zeros((game.k, game.k), bool)
    for s in splits.values():
        m |= s
    return np.einsum('abij,ij->ab', JA, m.astype(float))


def split_matrix(JA, game, key):
    splits, _, _ = outcome_masks(game)
    return np.einsum('abij,ij->ab', JA, splits[key].astype(float))


def conditions_on_demand(L, ids, members):
    """Does a class contain a program that reads the opponent (THEM)?"""
    return [any('THEM' in L.src(ids[p]) for p in m) for m in members]


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', default='dollar3')
    ap.add_argument('--n', type=int, default=5)
    ap.add_argument('--norole', action='store_true')
    a = ap.parse_args()
    t = time.time()
    E = load_or_evaluate(a.game, a.n, role=not a.norole)
    print('%s n=%d role=%s: %d programs, %d classes, divergence %.4f, %.0fs' % (
        a.game, a.n, not a.norole, len(E['ids']), len(E['reps']), E['div'], time.time() - t))
