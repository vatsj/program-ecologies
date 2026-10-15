"""Driver for the coverage-components run (notes/coverage-components.md).

  python3 src/coverage_components_run.py static                                   # classification tables, controls
  python3 src/coverage_components_run.py lottery --cells Hfull,minus_a --runs 20 --procs 3
  python3 src/coverage_components_run.py plan --plan "Hfull,minus_a:0:20;plus_a:0:20" --procs 3
  python3 src/coverage_components_run.py compare --cells S3 --parent Ni            # draw for draw vs stored runs
  python3 src/coverage_components_run.py mediate --cells plus_ab --runs 5 --procs 3
"""
import os
import sys
import json
import time
import argparse
from collections import defaultdict, Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sog_full as F
import sog_full_run as R
import coverage_components as CC

OUT = CC.OUT
STORED = os.path.join(CC.ROOT, 'runs', 'founding_legibility')


def lottery(args):
    from multiprocessing import get_context
    names = args.cells.split(',')
    jobs = []
    for nm in names:
        for rep in range(args.start, args.start + args.runs):
            f = os.path.join(OUT, 'cell_' + nm, 'rep_%03d.json' % rep)
            if os.path.exists(f): continue
            jobs.append((nm, rep, bool(args.extend)))
    print('jobs', len(jobs), [j[:2] for j in jobs][:80], time.strftime('%H:%M:%S'), flush=True)
    if not jobs: return
    with get_context('fork').Pool(min(args.procs, 3), maxtasksperchild=args.maxtasks) as pool:
        for nm, rep, tm in pool.imap_unordered(CC.cell_job, jobs, chunksize=1):
            print(nm, rep, json.dumps({k: round(v, 1) for k, v in tm.items()}), time.strftime('%H:%M:%S'), flush=True)


def jobs(args):
    """One pool over an explicit job list: --jobs 'cell:a-b,cell:r,...' (inclusive ranges)."""
    from multiprocessing import get_context
    jl = []
    for item in args.jobs.split(','):
        nm, rr = item.split(':')
        lo, hi = (int(z) for z in rr.split('-')) if '-' in rr else (int(rr), int(rr))
        for rep in range(lo, hi + 1):
            if not os.path.exists(os.path.join(OUT, 'cell_' + nm, 'rep_%03d.json' % rep)):
                jl.append((nm, rep, bool(args.extend)))
    print('jobs', len(jl), [j[:2] for j in jl][:120], time.strftime('%H:%M:%S'), flush=True)
    if not jl: return
    with get_context('fork').Pool(min(args.procs, 3), maxtasksperchild=args.maxtasks) as pool:
        for nm, rep, tm in pool.imap_unordered(CC.cell_job, jl, chunksize=1):
            print(nm, rep, json.dumps({k: round(v, 1) for k, v in tm.items()}), time.strftime('%H:%M:%S'), flush=True)


def plan(args):
    """Sequential segments 'cells:start:runs;...' (each segment one pool of <= 3 processes)."""
    for seg in args.plan.split(';'):
        cells, start, runs = seg.split(':')
        args.cells, args.start, args.runs = cells, int(start), int(runs)
        lottery(args)


SKIP = {'fills', 'ntypes', 'time', 'ctr', 'mark_ext'}


def diff(a, b, path=''):
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in set(a) | set(b):
            if k in SKIP: continue
            if k not in a or k not in b:
                out.append(path + '/' + str(k) + ' (missing)'); continue
            out += diff(a[k], b[k], path + '/' + str(k))
        return out
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): return [path + ' (len)']
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out += diff(x, y, path + '[%d]' % i)
        return out
    return [] if a == b else [path]


def compare(args):
    """Draw-for-draw comparison of this run's cell with the stored founding-legibility cell of the same replicates:
    every summary field except counters, fills and times (the mark changes counters only); counters compared too
    when --counters (both runs without the mark)."""
    res = {}
    for nm in args.cells.split(','):
        d = os.path.join(OUT, 'cell_' + nm)
        rows = []
        for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            if not f.endswith('.json') or '.tmp' in f: continue
            a = json.load(open(os.path.join(d, f)))
            pf = os.path.join(STORED, 'cell_' + args.parent, f)
            if not os.path.exists(pf): continue
            b = json.load(open(pf))
            sa, sb = dict(a['summary']), dict(b['summary'])
            for s_ in (sa, sb):          # the extinct-type key 'spo_held' exists only in S runs
                s_.pop('spo_held', None)
            dd = diff(sa, sb) + diff(a.get('summary_ext', {}), b.get('summary_ext', {}), '/ext')
            dd = [p for p in dd if 'fair_mask_end' not in p]
            ctr_eq = None
            if args.counters:
                ca, cb = a['summary']['ctr'], b['summary']['ctr']
                ctr_eq = [x for k, x in enumerate(ca) if k != 14] == [x for k, x in enumerate(cb) if k != 14]
            rows.append(dict(rep=a['rep'], identical=not dd, n_diff=len(dd), first=dd[:6], counters_equal=ctr_eq,
                             persistence=(a['summary']['h']['persistence'], b['summary']['h']['persistence']),
                             end=(a.get('summary_ext', {}).get('end', {}).get('persistence'),
                                  b.get('summary_ext', {}).get('end', {}).get('persistence'))))
        res[nm] = rows
        print(nm, 'vs', args.parent, json.dumps(rows, default=str), flush=True)
    f = os.path.join(CC.ROOT, 'runs', 'coverage-components-validate.json')
    old = json.load(open(f)) if os.path.exists(f) else {}
    old.update({'%s_vs_%s' % (k, args.parent): v for k, v in res.items()})
    json.dump(old, open(f, 'w'), indent=1, default=str)


# ----------------------------------------------------------------------------------------------------------------
# static tables (notes §1.x)
# ----------------------------------------------------------------------------------------------------------------
def founder_tree_weights(g, role, reps):
    r = g.roles[role]
    cum = np.cumsum(g.mass(role))
    wt = defaultdict(float)
    for rep in reps:
        rng = np.random.default_rng([rep, 100, 64, 20261013])
        uB = rng.random((64, 100)); u1 = rng.random((64, 100)); u2 = rng.random((64, 100))
        for u in ((uB,) if role == 'B' else (u1, u2)):
            sps = np.minimum(np.searchsorted(cum, u * cum[-1]), len(cum) - 1).ravel()
            for sp in sps: wt[int(r['tau'][sp])] += 1.0
    return wt


def prior_tree_weights(g, role):
    mu = g.mass(role)
    wt = defaultdict(float)
    for sp, tk in enumerate(g.roles[role]['tau']): wt[int(tk)] += mu[sp]
    return wt


def shares(g, role, wt, masks):
    tot = 0.0; wsum = 0.0
    cnt = Counter(); anyx = Counter(); joint = Counter(); probe = Counter(); ptot = Counter()
    vol = {m.name: 0.0 for m in masks}; ovl = {m.name: 0.0 for m in masks}; want = {m.name: 0.0 for m in masks}
    for tk, w in wt.items():
        if w == 0: continue
        wsum += w
        c = CC.classify(g, role, tk)
        has = set()
        for A in F.FAM[role]:
            for r in c[A]:
                lb = r['label']
                cnt[lb] += w; tot += w; has.add(lb)
                joint[(lb, 'S3' if r['S3'] else ('Sopp' if r['Sopp'] else 'none'), 'idT' if r['idT'] else '-',
                       'live' if r['live'] else 'dead')] += w
                if role == 'W':
                    ptot[lb] += w; probe[lb] += w * bool(r['probe'])
        for lb in has: anyx[lb] += w
        labs = CC.labels_of(g, role, tk)
        for m in masks:
            X = m.comps[0]
            Gs, Xs = m.sets(role, tk)
            d = Gs if m.kind == 'randplus' else Xs
            k = sum(l == X for ls in labs for l in ls)
            vol[m.name] += w * sum(len(z) for z in d)
            want[m.name] += w * k
            ovl[m.name] += w * sum(1 for si, z in enumerate(d) for i in z if labs[si][i] == X)
    return dict(script_share={k: cnt[k] / tot for k in CC.LABELS}, scripts_per_program=tot / wsum,
                any_share={k: anyx[k] / wsum for k in CC.LABELS},
                probe_reachable={k: probe[k] / ptot[k] for k in ptot} if role == 'W' else None,
                joint={'|'.join(k): v / tot for k, v in sorted(joint.items(), key=lambda z: -z[1])},
                controls={m.name: dict(achieved_volume_ratio=vol[m.name] / want[m.name] if want[m.name] else None,
                                       overlap_with_component=ovl[m.name] / vol[m.name] if vol[m.name] else None)
                          for m in masks})


def control_q(g, reps=range(20)):
    out = {}
    for role in ('W', 'B'):
        wt = founder_tree_weights(g, role, reps)
        n = sum(wt.values())
        out[role] = {}
        for X in CC.COMPS:
            V = P = 0.0
            for tk, w in wt.items():
                labs = CC.labels_of(g, role, tk)
                V += w * sum(l == X for ls in labs for l in ls)
                P += w * sum(l not in ('canon', X) for ls in labs for l in ls)
            out[role][X] = dict(V=V / n, P=P / n, q=min(1.0, V / P) if P else 0.0)
    return out


def static(args):
    g = R.grammar('id')
    masks = [CC.mask_for(c).bind(g) for c in ('rplus_a', 'rplus_b', 'rplus_c', 'rplus_d',
                                               'rminus_a', 'rminus_b', 'rminus_c', 'rminus_d')]
    out = {}
    t0 = time.time()
    for role in ('W', 'B'):
        out[role + '_prior'] = shares(g, role, prior_tree_weights(g, role), masks)
        out[role + '_founders_0_19'] = shares(g, role, founder_tree_weights(g, role, range(20)), masks)
        out[role + '_founders_20_59'] = shares(g, role, founder_tree_weights(g, role, range(20, 60)), masks)
        print(role, 'done', round(time.time() - t0), flush=True)
    named = {}
    for role, nd in (('W', F.NAMED_W), ('B', F.NAMED_B)):
        for nm, x in nd.items():
            if x not in g.roles[role]['spellings']: continue
            sp = g.roles[role]['spellings'].index(x)
            named[role + ':' + nm] = [list(z) for z in CC.labels_of(g, role, int(g.roles[role]['tau'][sp]))]
    out['named'] = named
    out['control_q'] = control_q(g)
    f = os.path.join(CC.ROOT, 'runs', 'coverage-components-static.json')
    json.dump(out, open(f, 'w'), indent=1)
    for k, v in out.items():
        if k == 'named': continue
        print(k, json.dumps(v['script_share']), json.dumps(v['controls']))


VARIANTS = {'H': ('canon', 'a', 'b', 'c', 'd'), 'canon': ('canon',), 'canon+a': ('canon', 'a'),
            'canon+b': ('canon', 'b'), 'canon+c': ('canon', 'c'), 'canon+d': ('canon', 'd'),
            'canon+ab': ('canon', 'a', 'b'), 'canon+cd': ('canon', 'c', 'd'), 'H-a': ('canon', 'b', 'c', 'd'),
            'H-b': ('canon', 'a', 'c', 'd'), 'H-c': ('canon', 'a', 'b', 'd'), 'H-d': ('canon', 'a', 'b', 'c')}


def coalitions(args):
    """Static (notes §1.x): founding coalitions (the parent's definition: a founder triple of distinct worker
    spellings, fair under H lists, with no constant boss earning the boss more) of replicates 0..runs-1, and whether
    each stays fair when every member holds only the classes of a variant (canon plus components, or H minus one)."""
    R.load_costc()
    ev = R.evaluator_k('eq', 'H', CC.KI)
    g = ev.g
    consts = R.const_pids(ev)
    W, B = g.roles['W'], g.roles['B']

    def pid(role, sp, variant):
        r = g.roles[role]
        tk = int(r['tau'][sp])
        labs = CC.labels_of(g, role, tk)
        keep = VARIANTS[variant]
        inv = tuple(tuple(i for i, l in enumerate(ls) if l in keep) for ls in labs)
        return ev.reg.get(role, sp, inv)
    ubc = {}

    def uninvadable(xh, yh):
        k = (xh, yh)
        if k not in ubc:
            t1 = 1 if F.tagged(W['dts'][ev.reg[xh].tk]) else 0
            t2 = 1 if F.tagged(W['dts'][ev.reg[yh].tk]) else 0
            ub = []
            for a in range(9):
                tr = ev.triple(consts[a], xh, yh)
                J = 4 * a + 2 * (tr['a1'] == 'D') + (tr['a2'] == 'D')
                ub.append(R.PAY[J, t1, t2, 0])
            ubc[k] = max(ub) <= 1.0 + 1e-12
        return ubc[k]
    cnt = Counter(); t0 = time.time()
    examples = defaultdict(list)
    for rep in range(args.runs):
        rng = np.random.default_rng([rep, 100, 64, 20261013])
        cumB = np.cumsum(g.mass('B')); cumW = np.cumsum(g.mass('W'))
        uB = rng.random((64, 100)); u1 = rng.random((64, 100)); u2 = rng.random((64, 100))
        spB = np.minimum(np.searchsorted(cumB, uB * cumB[-1]), len(cumB) - 1)
        sp1 = np.minimum(np.searchsorted(cumW, u1 * cumW[-1]), len(cumW) - 1)
        sp2 = np.minimum(np.searchsorted(cumW, u2 * cumW[-1]), len(cumW) - 1)
        r2 = np.random.default_rng([rep, 20261015, 3])
        for i in range(64):
            for _ in range(args.n):
                kb, k1, k2 = (int(r2.integers(100)) for _ in range(3))
                b, x, y = int(spB[i, kb]), int(sp1[i, k1]), int(sp2[i, k2])
                if x == y: continue
                bh, xh, yh = pid('B', b, 'H'), pid('W', x, 'H'), pid('W', y, 'H')
                if not R.fair_play(ev.triple(bh, xh, yh)): continue
                if not uninvadable(xh, yh): continue
                cnt['coalitions'] += 1
                for v in VARIANTS:
                    if v == 'H': continue
                    ok = R.fair_play(ev.triple(pid('B', b, v), pid('W', x, v), pid('W', y, v)))
                    cnt[v] += ok
                    if not ok and len(examples[v]) < 5:
                        examples[v].append([F.show(B['spellings'][b]), F.show(W['spellings'][x]), F.show(W['spellings'][y])])
            ev.maybe_clear()
        print(rep, dict(cnt), '%.0fs' % (time.time() - t0), flush=True)
    c = cnt['coalitions']
    out = dict(coalitions=c, fair_share={v: cnt[v] / max(c, 1) for v in VARIANTS if v != 'H'}, examples=examples)
    print(json.dumps(out['fair_share'], indent=1))
    json.dump(out, open(os.path.join(CC.ROOT, 'runs', 'coverage-components-coalitions.json'), 'w'), indent=1)


# ----------------------------------------------------------------------------------------------------------------
# mediation replays (notes §1.0 item 8)
# ----------------------------------------------------------------------------------------------------------------
def mediate(args):
    from multiprocessing import get_context
    jobs = []
    for nm in args.cells.split(','):
        d = os.path.join(OUT, 'cell_' + nm)
        cand = []
        for f in sorted(os.listdir(d)):
            if not f.endswith('.json') or '.tmp' in f: continue
            a = json.load(open(os.path.join(d, f)))
            rg = a['cc'].get('regrowth', {})
            if not rg.get('regrows') or not rg.get('nuclei'): continue
            nuc = rg['nuclei'][0]
            wh = sorted(set((p['role'], p['tk'], p['set'], p['idx']) for p in nuc.get('pivotal', [])
                            if p['prov'] == 'granted'))
            if not wh: continue
            cand.append((a['rep'], wh))
        for rep, wh in cand[:args.runs]:
            f = os.path.join(OUT, 'cell_%s_med' % nm, 'rep_%03d.json' % rep)
            if os.path.exists(f): continue
            jobs.append((nm, rep, True, [list(w) for w in wh], nm + '_med'))
    print('mediation jobs', [(j[0], j[1], len(j[3])) for j in jobs], flush=True)
    if not jobs: return
    with get_context('fork').Pool(min(args.procs, 3)) as pool:
        for nm, rep, tm in pool.imap_unordered(CC.cell_job, jobs, chunksize=1):
            print(nm, rep, json.dumps({k: round(v, 1) for k, v in tm.items()}), time.strftime('%H:%M:%S'), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('--cells', default='')
    ap.add_argument('--parent', default='Ni')
    ap.add_argument('--runs', type=int, default=20)
    ap.add_argument('--start', type=int, default=0)
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--extend', type=int, default=1)
    ap.add_argument('--maxtasks', type=int, default=None)
    ap.add_argument('--counters', type=int, default=0)
    ap.add_argument('--plan', default='')
    ap.add_argument('--jobs', default='')
    ap.add_argument('--n', type=int, default=200)
    args = ap.parse_args()
    globals()[args.cmd](args)


if __name__ == '__main__':
    main()
