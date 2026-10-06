"""Milestone 1 of the realizable-language spec: every table (specs/2026-10-06-realizable-language.md, "Compute").

Tasks (run with at most 3 worker processes):
  main b     -- the eleven named programs at budget b (SF with k = b): every ordered pair under primitive-assisted
                charging and search-charged charging at K in {1e4, 1e5, 1e6}; prove outcomes found/refuted/timeout with W;
                the JLoeb-disabled control on every cell; soundness check of every found box and every witness sequent;
                independent replay of every witness; independent-evaluator cross-check of every play trace.
  grid       -- FairBot copies vs distinct budgets on {4, 8, 16, 32}^2 and the full {2..40}^2 (primitive-assisted),
                search-charged on {4, 8, 16, 32}^2.
  sweep      -- SF_k against SF_k and against FB_b (b in {16, 32, 64}), k in {5, 10, 20, 64, 200, 1000}.
  brute b    -- the independent brute-force prover on every prove formula of the main table at b (b <= 9).
  memfull b  -- the main table's prove formulas re-decided with Mem = every atom/box content of the root closure.
Usage: python3 src/lt_run.py OUTDIR
"""
import os, sys, json, time
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import lt
from lt import *
import lt_check as LC

KS = [10 ** 4, 10 ** 5, 10 ** 6]
LIMIT = 5 * 10 ** 7
NAMES_ORDER = ['C', 'D', 'FB', 'FB1', 'PB', 'G', 'P*', 'SF', 'SC', 'Vlet', 'Vwrap']


def cell(pr, p, q, K, sem, trace_check=None):
    tr = [] if trace_check is not None else None
    r = run_play(pr, p, q, K, sem, trace=tr)
    if trace_check is not None:
        n, bad = LC.check_trace(tr)
        trace_check[0] += n; trace_check[1] += bad
    return {'play': r['play'], 'steps': r['steps'], 'reason': r['reason'],
            'proves': [[pr.th.show(a)[:120], c, out, W, insim] for (a, c, out, W, insim) in r['proves']]}


def formula_table(pr):
    out = {}
    for (psi, c), r in pr.cache.items():
        key = '%s@%d' % (pr.th.show(psi), c)
        d = {'c': c, 'found': r['found'], 'size': r['size'], 'W': r['W'], 'complete': r['complete'],
             'closure': r['closure'], 'merges': r['merges']}
        if r.get('found'):
            w = pr.witness(psi, c)
            d['lam'] = wlambda(w)
        out[key] = d
    return out


def audits(pr):
    """Soundness check and independent replay of every witness in the prover's cache."""
    t0 = time.time()
    nbox, nseq, bad = soundness_check(pr)
    rep = {'nodes': 0, 'steps': 0, 'jlob': 0}
    nrep = 0; rbad = []
    for (psi, c), r in list(pr.cache.items()):
        if not r.get('found'): continue
        w = pr.witness(psi, c)
        try:
            sz = LC.replay(LC.convert(pr.th, w), rep)
            if sz > c: rbad.append(['size>budget', pr.th.show(psi)[:80], c])
            nrep += 1
        except LC.ReplayError as e:
            rbad.append([str(e), pr.th.show(psi)[:80], c])
    return {'boxes_checked': nbox, 'sequents_checked': nseq, 'violations': [str(x) for x in bad],
            'witnesses_replayed': nrep, 'replay_nodes': rep['nodes'], 'replay_steps': rep['steps'],
            'replay_jlob': rep['jlob'], 'replay_failures': rbad, 'secs': time.time() - t0}


def task_main(b):
    t0 = time.time()
    cat = catalogue(b); register_names(cat)
    pr = Prover(limit=LIMIT)
    ctrl = Prover(th=pr.th, jlob=False, limit=LIMIT)
    tc = [0, 0]
    cells = {}
    for x in NAMES_ORDER:
        for y in NAMES_ORDER:
            d = {'prim': cell(pr, cat[x], cat[y], 10 ** 6, 'prim', tc)}
            for K in KS:
                d['search_%d' % K] = cell(pr, cat[x], cat[y], K, 'search', tc)
            d['ctrl_prim'] = cell(ctrl, cat[x], cat[y], 10 ** 6, 'prim', tc)
            for K in KS:
                d['ctrl_search_%d' % K] = cell(ctrl, cat[x], cat[y], K, 'search')
            cells[x + '|' + y] = d
    out = {'task': 'main', 'b': b, 'cells': cells, 'formulas': formula_table(pr),
           'ctrl_formulas': formula_table(ctrl), 'trace_steps_checked': tc[0], 'trace_disagreements': tc[1]}
    out['audit'] = audits(pr)
    out['ctrl_audit'] = audits(ctrl)
    out['secs'] = time.time() - t0
    return out


def task_grid():
    t0 = time.time()
    pr = Prover(limit=LIMIT)
    full = {}
    for x in range(2, 41):
        for y in range(2, 41):
            r = run_play(pr, FB(x), FB(y), 10 ** 6, 'prim')
            full['%d|%d' % (x, y)] = r['play']
    small = {}
    tc = [0, 0]
    for x in (4, 8, 16, 32):
        for y in (4, 8, 16, 32):
            d = {'prim': cell(pr, FB(x), FB(y), 10 ** 6, 'prim', tc)}
            for K in KS: d['search_%d' % K] = cell(pr, FB(x), FB(y), K, 'search', tc)
            small['%d|%d' % (x, y)] = d
    return {'task': 'grid', 'full': full, 'small': small, 'trace_steps_checked': tc[0],
            'trace_disagreements': tc[1], 'audit': audits(pr), 'secs': time.time() - t0}


def task_sweep():
    t0 = time.time()
    pr = Prover(limit=LIMIT)
    out = {}
    tc = [0, 0]
    for k in (5, 10, 20, 64, 200, 1000):
        d = {}
        pairs = [('SF', SF(k), 'SF', SF(k))]
        for b in (16, 32, 64):
            pairs += [('SF', SF(k), 'FB%d' % b, FB(b)), ('FB%d' % b, FB(b), 'SF', SF(k))]
        for xn, p, yn, q in pairs:
            e = {'prim': cell(pr, p, q, 10 ** 6, 'prim', tc)}
            for K in KS: e['search_%d' % K] = cell(pr, p, q, K, 'search', tc)
            d[xn + '|' + yn] = e
        out[str(k)] = d
    return {'task': 'sweep', 'cells': out, 'trace_steps_checked': tc[0], 'trace_disagreements': tc[1],
            'audit': audits(pr), 'secs': time.time() - t0}


def _main_formulas(b):
    """The prove formulas of the main table at b (by replaying the primitive-assisted plays)."""
    cat = catalogue(b); register_names(cat)
    pr = Prover(limit=LIMIT)
    for x in NAMES_ORDER:
        for y in NAMES_ORDER:
            run_play(pr, cat[x], cat[y], 10 ** 6, 'prim')
    return pr


def task_brute(b):
    t0 = time.time()
    pr = _main_formulas(b)
    rows = []
    for (psi, c), r in list(pr.cache.items()):
        t1 = time.time()
        br = LC.Brute(root=LC.ideep(pr.th, psi, {}))
        ms = br.minsize(c)
        rows.append({'formula': pr.th.show(psi)[:120], 'c': c, 'lt_found': r['found'], 'lt_size': r['size'],
                     'brute_size': ms, 'agree': (ms == r['size']), 'secs': time.time() - t1})
    ctrl = Prover(th=pr.th, jlob=False, limit=LIMIT)
    crow = []
    for (psi, c) in list(pr.cache.keys()):
        r = ctrl.query(psi, c)
        br = LC.Brute(root=LC.ideep(pr.th, psi, {}), jlob=False)
        ms = br.minsize(c)
        crow.append({'formula': pr.th.show(psi)[:120], 'c': c, 'lt_size': r['size'], 'brute_size': ms,
                     'agree': ms == r['size']})
    return {'task': 'brute', 'b': b, 'rows': rows, 'ctrl_rows': crow, 'secs': time.time() - t0}


def task_memfull(b):
    t0 = time.time()
    pr = _main_formulas(b)
    full = Prover(th=pr.th, mem='full', limit=LIMIT)
    rows = []
    for (psi, c), r in list(pr.cache.items()):
        f = full.query(psi, c)
        rows.append({'formula': pr.th.show(psi)[:120], 'c': c, 'size': r['size'], 'full_size': f['size'],
                     'W': r['W'], 'full_W': f['W'], 'agree': f['size'] == r['size'] and f['found'] == r['found']})
    return {'task': 'memfull', 'b': b, 'rows': rows, 'secs': time.time() - t0}


def run(task):
    kind, arg = task
    try:
        if kind == 'main': return task_main(arg)
        if kind == 'grid': return task_grid()
        if kind == 'sweep': return task_sweep()
        if kind == 'brute': return task_brute(arg)
        if kind == 'memfull': return task_memfull(arg)
    except Exception as e:
        import traceback
        return {'task': kind, 'arg': arg, 'error': traceback.format_exc()}


if __name__ == '__main__':
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    which = sys.argv[2] if len(sys.argv) > 2 else 'all'
    tasks = []
    if which in ('all', 'aux'):
        tasks += [('grid', None), ('sweep', None)] + [('brute', b) for b in range(2, 10)] + \
                 [('memfull', b) for b in (16, 25, 32)]
    if which in ('all', 'main'):
        tasks += [('main', b) for b in range(64, 1, -1)]
    done = set(os.listdir(outdir))
    tasks = [t for t in tasks if '%s_%s.json' % (t[0], t[1]) not in done]
    with Pool(3) as pool:
        for res in pool.imap_unordered(run, tasks):
            name = '%s_%s.json' % (res['task'], res.get('b', res.get('arg')))
            with open(os.path.join(outdir, name), 'w') as fh:
                json.dump(res, fh)
            print(name, res.get('secs', res.get('error', '')[-300:] if 'error' in res else ''), flush=True)
