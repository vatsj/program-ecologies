"""Sweep runner.  One cell = (arm, n, game, N, x_off, role).  Caches the square
evaluation per (arm, n, game, x_off); writes runs/<hash>/report.md and appends to
runs/results.md.
"""
import argparse, hashlib, json, os, pickle, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from dsl import Language
from game import Game
from evaluate import square
from chain import SquareProvider, SparseProvider, Chain
from report import cell_report, write_table

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')


def cell_hash(cfg):
    return hashlib.md5(json.dumps(cfg, sort_keys=True).encode()).hexdigest()[:10]


def get_language(arm, n, x_on, role):
    return Language(arm, n, x_on=x_on, role=role)


def get_provider(lang, game, arm, n, x_on, mode, verbose):
    ecfg = dict(arm=arm, n=n, game=game.name, x_on=x_on, role=game.role, mode=mode)
    path = os.path.join(RUNS, 'eval_' + cell_hash(ecfg) + '.pkl')
    if mode == 'square':
        if os.path.exists(path):
            with open(path, 'rb') as f:
                res = pickle.load(f)
            res.lang, res.game = lang, game
        else:
            t = time.time()
            res = square(lang, game, tol=1e-11)
            if verbose:
                print('square evaluation: %d pairs, %d budgets, %.1fs' % (len(res.keys), res.iters, time.time() - t), flush=True)
            res.lang = res.game = None
            with open(path, 'wb') as f:
                pickle.dump(res, f)
            res.lang, res.game = lang, game
        prov = SquareProvider(lang, res, lang.ids())
        div = float(res.div.mean())
        return prov, div
    prov = SparseProvider(lang, game, lang.ids(), verbose=verbose)
    return prov, None


def run_cell(arm, n, game_path, N, x_on=True, mode=None, verbose=True, seeds_upto=4, max_states=8000, theta=1e-6):
    game = Game.load(game_path)
    if mode is None:
        mode = 'square' if n <= 6 else 'sparse'
    lang = get_language(arm, n, x_on, game.role)
    cfg = dict(arm=arm, n=n, game=game.name, N=N, x_on=x_on, role=game.role, mode=mode)
    if verbose:
        print('== cell', cfg, flush=True)
    prov, div = get_provider(lang, game, arm, n, x_on, mode, verbose)
    seeds = None
    if mode == 'sparse':
        ids = lang.ids(seeds_upto)
        seeds = [(int(p), float(lang.mu[p])) for p in ids]
    t = time.time()
    ch = Chain(prov, N=N, seeds=seeds, verbose=verbose, max_states=max_states, theta=theta).explore()
    if mode == 'sparse':
        div = prov.div_count / max(prov.div_total, 1)
    row, md = cell_report(ch, prov, lang, game, cfg, div)
    row['chain_time_s'] = time.time() - t
    row['cut_flow'] = ch.cut_flow
    row['n_expanded'] = len(ch.trans)
    if mode == 'sparse':
        row['n_pairs_evaluated'] = prov.n_pairs
        row['n_supports'] = len(prov.blocks)
    d = os.path.join(RUNS, cell_hash(cfg))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'report.md'), 'w') as f:
        f.write(md)
    with open(os.path.join(d, 'row.json'), 'w') as f:
        json.dump(row, f, indent=1, default=str)
    if ch.indeterminate:
        with open(os.path.join(d, 'indeterminate.json'), 'w') as f:
            json.dump([(str(k), int(q), [(list(ids), list(map(float, x))) for ids, x in tr][:16]) for k, q, tr in ch.indeterminate[:20]], f)
    if verbose:
        print(md, flush=True)
    return row, md, ch, prov, lang


def collect():
    rows = []
    for d in sorted(os.listdir(RUNS)):
        p = os.path.join(RUNS, d, 'row.json')
        if os.path.exists(p):
            with open(p) as f:
                rows.append(json.load(f))
    rows.sort(key=lambda r: (r['game'], r['arm'], r['n'], r['N']))
    write_table(rows, os.path.join(RUNS, 'results.md'))
    return rows


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--arm', default='weak')
    ap.add_argument('--n', type=int, default=6)
    ap.add_argument('--game', default='pd')
    ap.add_argument('--N', type=int, nargs='+', default=[10, 100, 1000])
    ap.add_argument('--x_off', action='store_true')
    ap.add_argument('--mode', default=None)
    ap.add_argument('--max_states', type=int, default=8000)
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()
    for N in a.N:
        run_cell(a.arm, a.n, os.path.join(ROOT, 'games', a.game + '.yaml'), N, x_on=not a.x_off, mode=a.mode, verbose=not a.quiet, max_states=a.max_states)
    collect()
