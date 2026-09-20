"""Ultimatum-game runner for the three arms.

  role     : one population, ROLE-symmetrised, the single-population chain
  mutual   : two populations, both with the full weak grammar
  onesided : two populations, blind responders

Writes runs/ult_<game>_<arm>_N<N>_w<w>.md and .json.
"""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from dsl import Language
from game import Game
import run, twopop

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def role_arm(game_path, n, N, w):
    game = Game.load(game_path)
    row, md, ch, prov, L = run.run_cell('weak', n, game_path, N, w=w, verbose=False)
    res = prov.res
    pi = dict(zip(ch.keys_list, ch.pi))

    def pair_stats(p, q):
        vp = res.V[res.index(p, q, 0)]; vq = res.V[res.index(q, p, 1)]      # p proposes to q
        rej = float(vp @ game.reject @ vq) if game.reject is not None else 0.0
        return rej, float(vp @ game.pay[0] @ vq), float(vq @ game.pay[1] @ vp)

    def state_stats(key):
        ids, x, kind = ch.states[key]
        rej = sP = sR = 0.0
        for a, xa in zip(ids, x):
            for b, xb in zip(ids, x):
                r_, sp_, sr_ = pair_stats(a, b)
                rej += xa * xb * r_; sP += xa * xb * sp_; sR += xa * xb * sr_
        return rej, sP, sR
    tot = dict(reject=0.0, share_P=0.0, share_R=0.0)
    for k, p in pi.items():
        r_, sp_, sr_ = state_stats(k)
        tot['reject'] += p * r_; tot['share_P'] += p * sp_; tot['share_R'] += p * sr_
    lines = md.split('\n')
    lines.insert(3, 'on-path rejection rate %.4f, proposer share %.4f, responder share %.4f (pi-weighted, roles drawn)' % (tot['reject'], tot['share_P'], tot['share_R']))
    cond = [(ch.describe_state(k, L), p) for k, p in ch.support(1e-3) if any('THEM' in L.src(i) for i in ch.states[k][0])]
    lines.insert(4, 'conditional programs in the support (pi > 1e-3): %s' % (', '.join('%s %.3f' % c for c in cond[:8]) if cond else 'none'))
    lines.insert(5, '')
    lines.insert(6, '| pi | state | reject | share P | share R |'); lines.insert(7, '|---|---|---|---|---|')
    ins = 8
    for k, p in ch.support(1e-4)[:12]:
        r_, sp_, sr_ = state_stats(k)
        lines.insert(ins, '| %.4f | %s | %.3f | %.3f | %.3f |' % (p, ch.describe_state(k, L), r_, sp_, sr_)); ins += 1
    lines.insert(ins, '')
    stats = dict(tot, support=row['support'], conditional=cond, n_states=row['n_states'], n_classes=row['n_classes'], indeterminate=row['indeterminate'])
    return '\n'.join(lines), stats


def two_pop_arm(game_path, n, N, w, arm, verbose):
    game = Game.load(game_path)
    tp = twopop.build(game, n, arm, N, w, verbose=verbose).explore()
    md, stats = tp.report(dict(game=game.name, arm=arm, n=n, N=N, w=w))
    return md, stats


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--arm', default='role', choices=['role', 'mutual', 'onesided'])
    ap.add_argument('--game', default='ult')
    ap.add_argument('--n', type=int, default=5)
    ap.add_argument('--N', type=int, default=100)
    ap.add_argument('--w', type=float, default=0.1)
    ap.add_argument('--verbose', action='store_true')
    a = ap.parse_args()
    gp = os.path.join(ROOT, 'games', a.game + '.yaml')
    t = time.time()
    if a.arm == 'role':
        md, stats = role_arm(gp, a.n, a.N, a.w)
    else:
        md, stats = two_pop_arm(gp, a.n, a.N, a.w, a.arm, a.verbose)
    stats['time_s'] = time.time() - t
    base = os.path.join(ROOT, 'runs', 'ult_%s_%s_N%d_w%g' % (a.game, a.arm, a.N, a.w))
    open(base + '.md', 'w').write(md + '\n')
    json.dump(stats, open(base + '.json', 'w'), indent=1, default=str)
    print(md)
