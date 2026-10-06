"""Driver for the prover-as-code cells (predictions/2026-10-06-prover-as-code.md, design 7).  At most 3 worker
processes; one JSON file per task in runs/prover_as_code/.  Each task also runs the correctness harness on every core
query it produced (term vs host oracle, witness replay, checker term)."""
import json, os, sys, time
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(__file__))
import lt_code as L

OUT = os.path.join(os.path.dirname(__file__), '..', 'runs', 'prover_as_code')
KS = [10 ** 5, 10 ** 6, 10 ** 7]
BS = [8, 12, 16, 24, 32, 64]
LEAK_KS = [10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6]
OUTCOME = {'T': 'found', 'F': 'refuted', 'TO': 'interrupted'}


def qkey(key):
    n, U, (c, (psi, _u)) = key
    return n, U, c, psi


def describe(key, names):
    n, U, c, psi = qkey(key)
    return {'core': L.CORE_LIBS[n], 'c': c, 'U': U, 'formula': L.show_formula(L.rt_to_formula(psi), names)}


def play_cell(p, q, K):
    ev = []
    t0 = time.time()
    r, steps = L.play(p, q, K, ev)
    searches = []
    for key, res, total, depth, cut in ev:
        searches.append({'key': key, 'result': res, 'outcome': 'cut' if cut else OUTCOME[res], 'steps': total,
                         'depth': depth})
    return {'play': r, 'steps': steps, 'searches': searches, 'secs': round(time.time() - t0, 3)}


def top_searches(cell):
    """Program-level searches of the player (those not nested inside another core run: depth 0 or inside SF's sim
    with no enclosing core frame are recorded by the play's event list in order; nested Run runs happen inside clean
    runs and are logged with depth >= 1 within a core frame)."""
    return cell['searches']


def harness(names, max_queries=None):
    """Correctness on every finishing query in the cache: term vs host (outcome, size via witness, work, inst),
    witness replay, checker term.  Returns a list of records."""
    recs = []
    for key, (res, total) in list(L.CACHE.items()):
        n, U, c, psi = qkey(key)
        mode = L.CORE_LIBS[n]
        rec = describe(key, names)
        rec.update({'result': res, 'outcome': OUTCOME[res], 'steps': total})
        if res in ('T', 'F'):
            h = L.host_query(mode, c, psi, U)
            r, w, wi, wsteps = L.core_witness(mode, c, psi, U)
            rec.update({'host_found': h['found'], 'host_size': h['size'], 'host_work': h['work'],
                        'host_inst': h['inst'], 'closure': h['closure'], 'term_work': wi[0], 'term_inst': wi[1],
                        'outcome_agree': h['found'] == (res == 'T') and r == res,
                        'work_agree': tuple(wi) == (h['work'], h['inst'])})
            if res == 'T':
                wt = L.witness_from_rt(w)
                rec['size'] = wt['size']
                st = {}
                try:
                    rec['replay_size'] = L.replay(wt, mode, c, U, L.rt_to_formula(psi), True, st)
                    rec['replay_ok'] = rec['replay_size'] == wt['size'] == h['size']
                except L.ReplayError as e:
                    rec['replay_ok'] = False; rec['replay_err'] = str(e)
                rec['replay_nodes'] = st.get('nodes', 0)
                rec['same_tree'] = wt == h['search'].witness()
                v, csteps = L.term_check(mode, c, psi, U, w)
                rec['check_term'] = v; rec['check_steps'] = csteps
                rec['witness_rules'] = rules_of(wt)
        recs.append(rec)
    return recs


def rules_of(w):
    out = []

    def walk(nd):
        out.append(nd['rule'])
        for p in nd['prem']: walk(p)
    walk(w)
    return out


def names_of(cat):
    return {v: k for k, v in cat.items()}


def strip(cells):
    for c in cells.values():
        for s in c['searches']:
            s['key'] = None
    return cells


def task_main(K, b, mode):
    L.CACHE.clear()
    cat = L.catalogue(K, b, i=mode)
    names = names_of(cat)
    cells = {}
    for x in cat:
        for y in cat:
            c = play_cell(cat[x], cat[y], K)
            for s in c['searches']:
                s.update(describe(s['key'], names))
            cells['%s|%s' % (x, y)] = c
    recs = harness(names)
    return {'task': 'main', 'K': K, 'b': b, 'mode': mode, 'cells': strip(cells), 'queries': recs,
            'regress': L.STATS['regress']}


def task_grid(K):
    L.CACHE.clear()
    U = K // 4
    bs = [8, 12, 16, 32]
    progs = {x: L.FB(x, U, K) for x in bs}
    names = {v: 'FB%d' % k for k, v in progs.items()}
    cells = {}
    for x in bs:
        for y in bs:
            c = play_cell(progs[x], progs[y], K)
            for s in c['searches']: s.update(describe(s['key'], names))
            cells['%d|%d' % (x, y)] = c
    return {'task': 'grid', 'K': K, 'cells': strip(cells), 'queries': harness(names)}


def task_leak(K, b):
    """SF_k for k in LEAK_KS and the static boundary k = U + 8, U + 9, against every reader (both orders)."""
    L.CACHE.clear()
    U = K // 4
    cat = L.catalogue(K, b)
    readers = ['FB', 'FB1', 'PB', 'Vlet', 'Vwrap', 'FB2', 'FBx', 'G', 'P*', 'SC']
    ks = LEAK_KS + [U + 8, U + 9]
    cells = {}
    for k in ks:
        sf = L.SF(k)
        names = names_of(cat); names[sf] = 'SF%d' % k
        for r in readers:
            c1 = play_cell(cat[r], sf, K)          # the reader's play against SF
            c2 = play_cell(sf, cat[r], K)          # SF's play against the reader
            for s in c1['searches'] + c2['searches']: s.update(describe(s['key'], names))
            fuel = 10 * K if r == 'FBx' else K
            cells['%s|SF%d' % (r, k)] = {'k': k, 'reader': r, 'reader_play': c1['play'], 'sf_play': c2['play'],
                                         'target_fuel': fuel, 'matched': fuel == K,
                                         'reader_searches': c1['searches'], 'sf_searches': c2['searches'],
                                         'exploited': c1['play'] == 'C' and c2['play'] != 'C'}
    for c in cells.values():
        for s in c['reader_searches'] + c['sf_searches']: s['key'] = None
    return {'task': 'leak', 'K': K, 'b': b, 'U': U, 'cells': cells, 'queries': harness(names_of(cat))}


def task_thresholds(K):
    """Self-play and pairwise first cooperation on b = 2..20 (the exact thresholds behind the coarse b grid)."""
    L.CACHE.clear()
    out = {}
    for b in range(2, 21):
        cat = L.catalogue(K, b)
        for x in ['FB', 'FB1', 'PB', 'G', 'P*', 'SC', 'Vlet', 'Vwrap', 'FB2', 'FBx']:
            c = play_cell(cat[x], cat[x], K)
            out['%s|%s|%d' % (x, x, b)] = {'play': c['play'], 'steps': c['steps'],
                                          'searches': [(s['outcome'], s['steps']) for s in c['searches']]}
        for x, y in [('FB', 'SF'), ('SF', 'FB'), ('FB', 'FB1'), ('FB', 'PB'), ('FB', 'Vlet'), ('FB', 'Vwrap')]:
            c = play_cell(cat[x], cat[y], K)
            out['%s|%s|%d' % (x, y, b)] = {'play': c['play'], 'steps': c['steps'],
                                          'searches': [(s['outcome'], s['steps']) for s in c['searches']]}
    return {'task': 'thresholds', 'K': K, 'cells': out}


def task_boundary():
    """Fuel boundary cells: identical sources at actual K just across the play's needs; SF at the static boundary
    k = U + 8 / U + 9 against FB at b = 16; FB2 (visibility) run length."""
    L.CACHE.clear()
    out = {}
    K0 = 10 ** 6; U = K0 // 4
    for b in (7, 8, 16):
        fb = L.FB(b, U, K0)
        r, need = L.play(fb, fb, 10 ** 8)
        row = {'need': need, 'play_at_need': r}
        for d in (-1, 0, 1):
            row['K=need%+d' % d] = L.play(fb, fb, need + d)[0]
        out['FB%d self, named K0=1e6' % b] = row
    b = 16
    fb = L.FB(b, U, K0)
    for k in (U + 7, U + 8, U + 9, U + 10):
        sf = L.SF(k)
        out['FB16 vs SF k=U%+d' % (k - U)] = {'reader': L.play(fb, sf, K0)[0], 'sf': L.play(sf, fb, K0)[0]}
    # SF's real completion point: smallest k at which SF's own simulation of FB returns a value (not TO), by bisection
    def sim_value(k):
        sf = L.SF(k)
        t = ('run', L.N(k), ('quote', fb), ('quote', sf))
        v, n = L.evaluate(t, 10 ** 8)
        return v
    lo, hi = 1, U + 20
    while lo < hi:
        mid = (lo + hi) // 2
        if sim_value(mid) == 'TO': lo = mid + 1
        else: hi = mid
    out['SF inner completion k*'] = {'k_star': lo, 'value_at_k_star': str(sim_value(lo)), 'U': U,
                                     'static_boundary': U + 9}
    for b in (10, 16):
        fb2 = L.FB2(b, U, K0); fb_ = L.FB(b, U, K0)
        r2, n2 = L.play(fb2, fb2, K0); r1, n1 = L.play(fb_, fb_, K0)
        out['visibility FB2 b=%d' % b] = {'FB2_self': r2, 'FB2_steps': n2, 'FB_self': r1, 'FB_steps': n1}
    return {'task': 'boundary', 'cells': out}


def task_bench():
    """Benchmarks (spec): the FairBot self-proof's search steps, expansions and rule instances by b; checking the
    supplied witness by the checker term; the same for every twin self-proof; closure sizes."""
    L.CACHE.clear()
    K = 10 ** 7; U = K // 4
    out = {}
    for x in ['FB', 'FB1', 'PB', 'Vlet', 'Vwrap', 'FB2', 'SC', 'G', 'P*']:
        for b in [7, 8, 10, 12, 16, 24, 32, 64]:
            cat = L.catalogue(K, b)
            ev = []
            L.play(cat[x], cat[x], K, ev)
            key = [e[0] for e in ev if e[3] == 0][0]          # the program's first search in self-play
            n, _U, (c, (psi, _u)) = key
            mode = L.CORE_LIBS[n]
            t0 = time.time()
            res, total = L.box_truth(mode, b, U, psi)
            rec = {'result': res, 'search_steps': total, 'secs': round(time.time() - t0, 2),
                   'query': L.show_formula(L.rt_to_formula(psi), names_of(cat))}
            if res in ('T', 'F'):
                r, w, wi, wsteps = L.core_witness(mode, b, psi, U)
                h = L.host_query(mode, b, psi, U)
                rec.update({'expansions': wi[0], 'instances': wi[1], 'closure': h['closure'],
                            'host_agree': h['found'] == (res == 'T') and tuple(wi) == (h['work'], h['inst'])})
                if res == 'T':
                    v, csteps = L.term_check(mode, b, psi, U, w)
                    wt = L.witness_from_rt(w)
                    rec.update({'size': wt['size'], 'check_result': v, 'check_steps': csteps,
                                'check_steps_per_node': round(csteps / wt['size'], 1),
                                'search_steps_per_expansion': round(total / max(1, wi[0]), 1),
                                'rules': rules_of(wt)})
            out['%s|%d' % (x, b)] = rec
    return {'task': 'bench', 'cells': out}


def run(task):
    name, args = task
    fn = {'main': task_main, 'grid': task_grid, 'leak': task_leak, 'thresholds': task_thresholds,
          'boundary': task_boundary, 'bench': task_bench}[name]
    t0 = time.time()
    res = L.run_big(fn, *args)
    res['secs'] = round(time.time() - t0, 1)
    fname = '%s_%s.json' % (name, '_'.join(str(a) for a in args))
    with open(os.path.join(OUT, fname), 'w') as f:
        json.dump(res, f, default=str)
    return fname, res['secs']


def tasks(which):
    ts = []
    if 'bench' in which: ts.append(('bench', ()))
    if 'boundary' in which: ts.append(('boundary', ()))
    if 'thresholds' in which: ts += [('thresholds', (K,)) for K in KS]
    if 'grid' in which: ts += [('grid', (K,)) for K in KS]
    if 'main' in which: ts += [('main', (K, b, 0)) for K in KS for b in BS]
    if 'control' in which: ts += [('main', (K, b, 2)) for K in KS for b in BS]
    if 'leak' in which: ts += [('leak', (K, b)) for K in KS for b in BS]
    return ts


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    which = sys.argv[1].split(',')
    ts = tasks(which)
    done = set(os.listdir(OUT)) if '--resume' in sys.argv else set()
    ts = [t for t in ts if '%s_%s.json' % (t[0], '_'.join(str(a) for a in t[1])) not in done]
    print('tasks', len(ts), flush=True)
    with Pool(3) as pool:
        for fname, secs in pool.imap_unordered(run, ts):
            print(fname, secs, flush=True)
