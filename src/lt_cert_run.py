"""Driver for the certificates-as-code cells (predictions/2026-10-06-certificates-as-code.md, design 7).  At most 2
worker processes (two foreign chains were alive at launch).  One JSON file per task in runs/certificates_as_code/."""
import json, os, random, sys, time
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(__file__))
import lt_code as L
import lt_cert as C

OUT = os.path.join(os.path.dirname(__file__), '..', 'runs', 'certificates_as_code')
KS = [10 ** 5, 10 ** 6, 10 ** 7]


def names_of(progs):
    out = {}
    for k, v in progs.items():
        out.setdefault(id(v), k)
    return out


def qname(names, t):
    return names.get(id(t)) or names.get(('canon', L.canon_term(t)), '?')


def build_names(progs):
    d = {}
    for k, v in progs.items():
        d.setdefault(('canon', L.canon_term(v)), k)
    return d


def describe_check(key, cnames):
    n, V, arg = key
    Vv, t, m, a, K = C.rt_arg_fields(arg)
    return {'mode': C.CC_MODE.get(n), 'core': 'search' if n not in C.CC_MODE else 'check',
            't': cnames.get(('canon', L.canon_term(t)), '?'), 'm': cnames.get(('canon', L.canon_term(m)), '?'),
            'a': a, 'K': K, 'V': V}


def play_cell(p, q, K, cnames):
    ev = []
    t0 = time.time()
    r, steps = L.play(p, q, K, ev)
    calls = []
    for key, res, total, depth, cut in ev:
        n = key[0]
        if n in C.CC_MODE:
            d = describe_check(key, cnames)
        else:
            d = {'core': 'search', 'mode': L.CORE_LIBS.get(n), 'U': key[1]}
        d.update({'result': res, 'steps': total, 'cut': cut, 'depth': depth, '_key': key})
        calls.append(d)
    return {'play': r, 'steps': steps, 'calls': calls, 'secs': round(time.time() - t0, 3)}


def audit_checks(cells, K):
    """Every top-level check that returned T (uncut): the certified atom against the actual play; the term against
    the host replay checker; Lemma Sym on every check that closed S."""
    host = C.HostCheck()
    seen = {}
    for c in cells.values():
        for d in c['calls']:
            if d['core'] != 'check': continue
            seen.setdefault(d['_key'], d)
    audit = []
    for key, d in seen.items():
        n, V, arg = key
        Vv, t, m, a, Kk = C.rt_arg_fields(arg)
        res = L.CACHE[key][0] if key in L.CACHE else d['result']
        rec = {'mode': d['mode'], 't': d['t'], 'm': d['m'], 'a': a, 'K': Kk, 'result': res,
               'steps': L.CACHE[key][1] if key in L.CACHE else d['steps']}
        # host replay
        wrapn = C.ID[C.MODE_WRAP[d['mode']]]
        hv = C.mk_arg(V, t, m, a, Kk)
        h = host.check(wrapn, hv)
        rec['host'] = h
        rec['host_agree'] = (h == res) if res != 'TO' else None
        if res == 'T':
            actual = L.play(t, m, Kk)[0]
            rec['actual'] = actual
            rec['violation'] = actual != a
            if d['mode'] in (0, 1, 5):
                Rb, Sb = ('cbox', wrapn, hv), ('cbox', wrapn, C.swap_arg(hv))
                ok, usesS, idx = host.vone(d['mode'], hv, Rb, Sb)
                rec['usesS'] = bool(ok and usesS and Rb != Sb)
                if rec['usesS']:
                    r2, t2 = C.check_value(d['mode'], V, m, t, a, Kk)
                    ok2, usesS2, _ = host.vone(d['mode'], C.swap_arg(hv), Sb, Rb)
                    rec['swap'] = {'result': r2, 'steps': t2, 'partner_closed_R': bool(usesS2),
                                   'sym_ok': r2 == 'T' and ((t2 == rec['steps']) if usesS2 else (t2 <= rec['steps']))}
        audit.append(rec)
    return audit


def regress_pass(keys):
    """For every distinct top-level check key: a fresh evaluation (cache cleared) counting term regress events, and
    the host replay's nesting depth."""
    out = []
    for key in keys:
        n, V, arg = key
        Vv, t, m, a, Kk = C.rt_arg_fields(arg)
        L.CACHE.clear()
        r0 = L.STATS['regress']
        res, total = C.check_value(C.CC_MODE[n], V, t, m, a, Kk)
        h = C.HostCheck()
        h.check(C.ID[C.MODE_WRAP[C.CC_MODE[n]]], C.mk_arg(V, t, m, a, Kk))
        out.append({'key_mode': C.CC_MODE[n], 'result': res, 'steps': total, 'regress': L.STATS['regress'] - r0,
                    'host_depth': h.maxdepth})
    return out


def strip(cells):
    for c in cells.values():
        for d in c['calls']: d.pop('_key', None)
    return cells


def task_main(K, arm):
    L.CACHE.clear()
    t0 = time.time()
    progs, info = C.build_arm(K, arm)
    tb = time.time() - t0
    cnames = build_names(progs)
    names = [n for n in progs if not n.endswith('_fresh')] if arm == 'S' else list(progs)
    cells = {}
    for x in names:
        for y in names:
            cells['%s|%s' % (x, y)] = play_cell(progs[x], progs[y], K, cnames)
    audit = audit_checks(cells, K)
    keys = sorted({d['_key'] for c in cells.values() for d in c['calls'] if d['core'] == 'check'}, key=repr)
    for c in cells.values():
        for d in c['calls']:
            if d['core'] == 'check': d['kid'] = keys.index(d['_key'])
    reg = regress_pass(keys)
    lists = {nm: [(a, C.show_script(s), C.script_nodes(s)) for a, s in C.uncons(C.h_getcerts(p))]
             for nm, p in progs.items() if C.h_getcerts(p) not in (None,) and C.h_getcerts(p) != 0}
    sizes = {nm: L.canon_term(p) and term_size(p) for nm, p in progs.items()}
    return {'task': 'main', 'K': K, 'arm': arm, 'V': K // 4, 'names': names, 'cells': strip(cells), 'audit': audit,
            'regress': reg, 'lists': lists, 'sizes': sizes, 'build_secs': round(tb, 2),
            'production_work': info.get('_production_work')}


def term_size(t):
    if t[0] in ('v', 'nat', 'con', 'lib'): return 1
    if t[0] in ('lam', 'fix', 'quote'): return 1 + term_size(t[1])
    if t[0] == 'op': return 1 + term_size(t[2]) + term_size(t[3])
    if t[0] == 'sim': return 1 + term_size(t[2])
    return 1 + sum(term_size(a) for a in t[1:])


def task_bench():
    """Scale guard: the CB-CB check cost, the smallest K (with V = K/4) at which CB-CB, CB-CB1, CB-CBP and CB1-CBP
    cooperate, check costs at K = 10^7, production costs, script and storage sizes, expanded sizes."""
    L.CACHE.clear()
    K = 10 ** 7
    progs, info = C.build_arm(K, 'S')
    V = K // 4
    out = {'checks': {}, 'scripts': {}, 'production': {}}
    pairs = [('CB', 'CB'), ('CB', 'CB1'), ('CB1', 'CB'), ('CB', 'CBP'), ('CBP', 'CB'), ('CB1', 'CBP'), ('CBP', 'CB1'),
             ('CBP', 'CBP'), ('CB1', 'CB1'), ('CB', 'CBlet'), ('CB', 'CBwrap'), ('CB', 'SFc'), ('CB', 'Ccert'),
             ('CB', 'LobC'), ('CB', 'CBsloppy'), ('CBP', 'CBsloppy'), ('CB', 'CBmut'), ('CB', 'Dcert'), ('CB', 'CB0')]
    for x, y in pairs:
        res, total = C.check_value(0, V, progs[x], progs[y], 'C', K)
        out['checks']['%s|%s' % (x, y)] = {'result': res, 'inner': total - 1, 'call_cost': total + 5}
    for nm in ['CB', 'CB1', 'CBP', 'CBlet', 'CBwrap', 'Ccert', 'SFc', 'LobC', 'CBsloppy', 'CBN', 'CBS2']:
        ents = C.uncons(C.h_getcerts(progs[nm]))
        out['scripts'][nm] = []
        for a, s in ents:
            probe = progs['CB'] if a == 'C' else L.PROG_D
            out['scripts'][nm].append({'a': a, 'script': C.show_script(s), 'nodes': C.script_nodes(s),
                                       'expanded_vs_CB_or_D': C.expanded_size(progs[nm], probe, a, K, s)})
        out['scripts'][nm + '_storage_nodes'] = term_size(C.data_term(C.h_getcerts(progs[nm])))
        out['scripts'][nm + '_source_nodes'] = term_size(progs[nm])
    # production cost: tactic nodes and host check emulations, per program (fresh producer)
    for nm, bf in list(C.CARRIER_BODIES.items()) + list(C.HELDOUT_BODIES.items()):
        prod = C.Producer()
        t0 = time.time()
        lst, inf = C.produce_list(prod, 0, lambda c, bf=bf: C.carrier(bf(0, V, K), c),
                                  [(n_, progs[n_]) for n_ in ('CB', 'CB1', 'CBP')], K, V)
        out['production'][nm] = {'tactic_nodes': prod.work, 'host_checks': len(prod.host.memo),
                                 'secs': round(time.time() - t0, 3), 'scripts': len(C.uncons(lst))}
    # smallest K (V = K/4, sources rebuilt at each K) at which each pair's check returns T: bisection on K
    def coop(x, y, K_):
        pr, _ = C.build_arm(K_, 'S') if K_ not in _built else _built[K_]
        _built[K_] = (pr, None)
        return C.check_value(0, K_ // 4, pr[x], pr[y], 'C', K_)[0] == 'T'
    _built = {}
    out['first_K'] = {}
    for x, y in [('CB', 'CB'), ('CB', 'CB1'), ('CB', 'CBP'), ('CB1', 'CBP'), ('CBP', 'CBP')]:
        lo, hi = 1000, 10 ** 6
        while hi - lo > 4:
            mid = (lo + hi) // 2
            if coop(x, y, mid): hi = mid
            else: lo = mid
        out['first_K']['%s|%s' % (x, y)] = hi
    return {'task': 'bench', **out}


def task_boundary():
    """Fuel boundary cells.  (a) V scan around the measured inner cost W of a check, sources rebuilt with that V
    (K = 10^6): F at V = W - 1, T at V = W.  (b) K scan with V fixed (25,000) around the static fit boundary of CB
    (K = V + 10), CB1 and CBP (K = 2V + 17), self-play and pairs."""
    L.CACHE.clear()
    K = 10 ** 6
    out = {'Vscan': {}, 'Kscan': {}}
    base, _ = C.build_arm(K, 'S')
    for x, y in [('CB', 'CB'), ('CB', 'CB1'), ('CB', 'CBP'), ('CB1', 'CBP'), ('SFc', 'CB')]:
        W = C.check_value(0, K // 4, base[x], base[y], 'C', K)[1] - 1
        row = {'W': W}
        for d in (-1, 0, 1):
            V = W + d
            px = C.carrier(_body(x)(V, K), C.h_getcerts(base[x])) if x != 'SFc' else \
                C.carrier(C.body_SFc(K // 2), C.h_getcerts(base[x]))
            py = C.carrier(_body(y)(V, K), C.h_getcerts(base[y]))
            res, tot = C.check_value(0, V, px, py, 'C', K)
            row['V=W%+d' % d] = {'check': res, 'inner': tot - 1, 'play_xy': L.play(px, py, K)[0],
                                 'play_yx': L.play(py, px, K)[0]}
        out['Vscan']['%s|%s' % (x, y)] = row
    V = 25000
    for x, y, bnd in [('CB', 'CB', V + 10), ('CB', 'CB1', 2 * V + 17), ('CB1', 'CB', 2 * V + 17),
                      ('CB', 'CBP', 2 * V + 17), ('CBP', 'CB', 2 * V + 17)]:
        row = {'static_boundary': bnd}
        for d in (-2, -1, 0, 1):
            Kk = bnd + d
            px = C.carrier(_body(x)(V, Kk), C.h_getcerts(base[x]))
            py = C.carrier(_body(y)(V, Kk), C.h_getcerts(base[y]))
            res, tot = C.check_value(0, V, px, py, 'C', Kk)
            pxy, sxy = L.play(px, py, Kk)
            row['K=b%+d' % d] = {'check_x_by_y': res, 'play_xy': pxy, 'steps_xy': sxy, 'play_yx': L.play(py, px, Kk)[0]}
        out['Kscan']['%s|%s' % (x, y)] = row
    return {'task': 'boundary', **out}


def _body(nm):
    f = {'CB': C.body_CB, 'CB1': C.body_CB1, 'CBP': C.body_CBP}[nm]
    return lambda V, K: f(0, V, K)


def task_heldout(K):
    """Held-out coverage: each held-out source carrying the production-set script of its class, and carrying its fresh
    production; cooperation with every production-set carrier both ways (no new certificate on their side)."""
    L.CACHE.clear()
    progs, info = C.build_arm(K, 'S')
    out = {}
    prodset = ['CB', 'CB1', 'CBP', 'CBlet', 'CBwrap', 'SFc', 'LobC', 'CBsloppy', 'CBmut']
    for nm in C.HELDOUT_BODIES:
        rec = {'class': C.HELDOUT_CLASS[nm],
               'fresh': [(a, C.show_script(s), C.script_nodes(s)) for a, s in C.uncons(info[nm]['fresh_list'])],
               'class_list': [(a, C.show_script(s)) for a, s in C.uncons(info[nm]['class_list'])]}
        for variant in ('', '_fresh'):
            p = progs[nm + variant]
            row = {}
            for y in prodset:
                row[y] = {'check_of_heldout': C.check_value(0, K // 4, p, progs[y], 'C', K)[0],
                          'play_heldout': L.play(p, progs[y], K)[0], 'play_other': L.play(progs[y], p, K)[0]}
            row['self'] = L.play(p, p, K)[0]
            rec['carrying' + (variant or '_class')] = row
        rec['class_script_covers'] = all(v['check_of_heldout'] == 'T' for k, v in rec['carrying_class'].items()
                                         if k in ('CB', 'CB1', 'CBP'))
        out[nm] = rec
    return {'task': 'heldout', 'K': K, 'heldout': out}


def task_fuzz(n_per_mode=40, seed=20261006):
    """Fuzz soundness audit: random carrier-like codes (depth <= 2 over four call shapes), each with two random
    scripts and its produced C and D scripts; every ordered pair, both outcomes, every mode."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tests'))
    import test_lt_cert as T
    L.CACHE.clear()
    rng = random.Random(seed)
    K, V = 10 ** 5, 10 ** 5 // 4
    prod = C.Producer()
    res = {}
    for mode in (0, 1, 2, 3, 5):
        ps = []
        for i in range(n_per_mode):
            bodyt = T.fuzz_body(rng, 2, mode, V, K)
            ents = [(rng.choice(['C', 'C', 'D']), T.fuzz_script(rng, 4)) for _ in range(2)]
            p0 = C.carrier(bodyt, C.cons(ents))
            for a, probe in (('C', p0), ('D', L.PROG_D)):
                s = prod.produce(mode, p0, probe, a, K, V)
                if s is not None: ents.append((a, s))
            ps.append(C.carrier(bodyt, C.cons(ents)))
        ps += [L.PROG_C, L.PROG_D]
        acc = viol = tot = 0
        examples = []
        for t in ps:
            for m in ps:
                for a in ('C', 'D'):
                    r, _ = C.check_value(mode, V, t, m, a, K)
                    tot += 1
                    if r != 'T': continue
                    acc += 1
                    if L.play(t, m, K)[0] != a:
                        viol += 1
                        if len(examples) < 3: examples.append({'t_size': term_size(t), 'a': a})
        res[mode] = {'checks': tot, 'accepted': acc, 'violations': viol, 'examples': examples}
    return {'task': 'fuzz', 'K': K, 'per_mode': res}


def run_task(spec):
    name, args = spec
    fn = {'main': task_main, 'bench': task_bench, 'boundary': task_boundary, 'heldout': task_heldout,
          'fuzz': task_fuzz}[name]
    t0 = time.time()
    out = L.run_big(fn, *args)
    out['secs'] = round(time.time() - t0, 1)
    tag = name + '_' + '_'.join(str(a) for a in args)
    with open(os.path.join(OUT, tag + '.json'), 'w') as f:
        json.dump(out, f, default=str)
    return tag, out['secs']


def main():
    os.makedirs(OUT, exist_ok=True)
    which = sys.argv[1:] or ['bench', 'boundary', 'heldout', 'fuzz', 'main']
    tasks = []
    if 'bench' in which: tasks.append(('bench', ()))
    if 'boundary' in which: tasks.append(('boundary', ()))
    if 'heldout' in which: tasks += [('heldout', (K,)) for K in KS]
    if 'fuzz' in which: tasks.append(('fuzz', ()))
    if 'main' in which: tasks += [('main', (K, arm)) for arm in ('S', 'O', 'X') for K in KS]
    workers = int(os.environ.get('WORKERS', '2'))
    with Pool(workers) as pool:
        for tag, secs in pool.imap_unordered(run_task, tasks):
            print(tag, secs, flush=True)


if __name__ == '__main__':
    main()
