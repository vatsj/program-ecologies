"""Driver for the founding-legibility run (notes/founding-legibility.md).

  python3 src/founding_legibility_run.py lottery --cells N6 --runs 5 --procs 3 --extend 1
  python3 src/founding_legibility_run.py compare --cells N6,L2_6 --parent S_eq      # bit-identity with stored runs
  python3 src/founding_legibility_run.py static --runs 5                            # generation-0 yield, pass costs
  python3 src/founding_legibility_run.py assay --runs 40                            # isolated (D*, T1, T1), L1 lists
"""
import os
import sys
import json
import time
import argparse
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sog_full as F
import sog_full_kern as KN
import sog_full_run as R
import founding_legibility as FL

OUT = FL.OUT
PARENT = os.path.join(FL.ROOT, 'runs', 'sog_full')


def plan(args):
    """Sequential segments 'cells:start:runs;...' with one pool, optionally after process --waitpid has exited."""
    if args.waitpid:
        while True:
            try:
                os.kill(args.waitpid, 0)
            except OSError:
                break
            time.sleep(30)
    for seg in args.plan.split(';'):
        cells, start, runs = seg.split(':')
        args.cells, args.start, args.runs = cells, int(start), int(runs)
        lottery(args)


def lottery(args):
    from multiprocessing import get_context
    names = args.cells.split(',')
    jobs = []
    for nm in names:
        for rep in range(args.start, args.start + args.runs):
            f = os.path.join(OUT, 'cell_' + nm, 'rep_%03d.json' % rep)
            if os.path.exists(f): continue
            jobs.append((nm, rep, bool(args.extend)))
    print('jobs', len(jobs), [j[:2] for j in jobs][:60], flush=True)
    if not jobs: return
    with get_context('fork').Pool(min(args.procs, 3), maxtasksperchild=args.maxtasks) as pool:
        for nm, rep, tm in pool.imap_unordered(FL.cell_job, jobs, chunksize=1):
            print(nm, rep, json.dumps({k: round(v, 1) for k, v in tm.items()}), time.strftime('%H:%M:%S'), flush=True)


SKIP = {'fills', 'ntypes', 'time'}


def diff(a, b, path=''):
    """Paths where two JSON objects differ."""
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
    """Bit-identity of this run's cells with the parent's stored runs of the same replicates (summary, extension)."""
    res = {}
    for nm in args.cells.split(','):
        d = os.path.join(OUT, 'cell_' + nm)
        par = args.parent
        rows = []
        for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            if not f.endswith('.json'): continue
            a = json.load(open(os.path.join(d, f)))
            pf = os.path.join(PARENT, 'cell_' + par, f)
            if not os.path.exists(pf):
                continue
            b = json.load(open(pf))
            dd = diff(a['summary'], b['summary']) + diff(a.get('summary_ext', {}), b.get('summary_ext', {}), '/ext')
            # ctr[14] counts quiet checks including retries after table misses (table history, not dynamics)
            dd = [p for p in dd if not p.endswith('/ctr[14]')]
            # the mark kernel's extension counters include the mark's attempt accounting: compare the dynamics only
            rows.append(dict(rep=a['rep'], identical=not dd, n_diff=len(dd), first=dd[:6],
                             persistence=(a['summary']['h']['persistence'], b['summary']['h']['persistence']),
                             fair_mask_equal=a['summary']['fair_mask'] == b['summary']['fair_mask'],
                             mark=a.get('fl', {}).get('mark', {}).get('MK')))
        res[nm] = rows
        print(nm, 'vs', par, json.dumps(rows, default=str), flush=True)
    f = os.path.join(OUT, 'compare.json')
    old = json.load(open(f)) if os.path.exists(f) else {}
    old.update({'%s_vs_%s' % (k, args.parent): v for k, v in res.items()})
    json.dump(old, open(f, 'w'), indent=1, default=str)


def is_sprobe_boss(ev, pid):
    t = ev.g.roles['B']['dts'][ev.reg[pid].tk]
    return any(a[0] == 'P' and a[3] == ('D',) for a in F.dt_atoms(t))


def static(args):
    """Notes §1.3 by code: the generation-0 yield of naturally founded coalitions under natural founding and L1; the
    founding pass's cost and coverage, on the founders of replicates 0..runs-1 (paired seeds), at K = 10^6."""
    R.load_costc()
    K = args.K or FL.K6
    evS = R.evaluator_k('eq', 'S', K)
    evH = R.evaluator_k('eq', 'H', K)
    g = evS.g
    consts = R.const_pids(evH)
    W = g.roles['W']; B = g.roles['B']
    fullW = lambda sp: evH.reg.get('W', sp, F.full_inv(g, 'W', int(W['tau'][sp])))
    fullB = lambda sp: evH.reg.get('B', sp, F.full_inv(g, 'B', int(B['tau'][sp])))
    ubc = {}

    def uninvadable(xh, yh):
        k = (xh, yh)
        if k not in ubc:
            t1 = 1 if F.tagged(W['dts'][evH.reg[xh].tk]) else 0
            t2 = 1 if F.tagged(W['dts'][evH.reg[yh].tk]) else 0
            ub = []
            for a in range(9):
                tr = evH.triple(consts[a], xh, yh)
                J = 4 * a + 2 * (tr['a1'] == 'D') + (tr['a2'] == 'D')
                ub.append(R.PAY[J, t1, t2, 0])
            ubc[k] = max(ub) <= 1.0 + 1e-12
        return ubc[k]

    out = dict(K=K, reps=[])
    tot = defaultdict(int)
    t0 = time.time()
    for rep in range(args.runs):
        cfg = dict(FL.cell_cfg('L1_6'), K=K)
        base = R.Run(evS, cfg, rep)
        ft, st = FL.founding_pass(base)
        et = FL.empty_types(base)
        rng = np.random.default_rng([rep, 20261014, 3])
        spB, sp1, sp2 = base.founders
        cnt = defaultdict(int)
        for i in range(base.I):
            for _ in range(args.n):
                kb, k1, k2 = (int(rng.integers(base.N)) for _ in range(3))
                if sp1[i, k1] == sp2[i, k2]: continue
                bh, xh, yh = fullB(int(spB[i, kb])), fullW(int(sp1[i, k1])), fullW(int(sp2[i, k2]))
                if not R.fair_play(evH.triple(bh, xh, yh)): continue
                cnt['H_fair'] += 1
                if not uninvadable(xh, yh): continue
                cnt['coalitions'] += 1
                sprobe = is_sprobe_boss(evS, base.btypes[int(et[0, i, kb])])
                cnt['coalitions_sprobe'] += sprobe
                nat = R.fair_play(evS.triple(base.btypes[int(et[0, i, kb])], base.wtypes[int(et[1, i, k1])],
                                             base.wtypes[int(et[2, i, k2])]))
                l1 = R.fair_play(evS.triple(base.btypes[int(ft[0, i, kb])], base.wtypes[int(ft[1, i, k1])],
                                            base.wtypes[int(ft[2, i, k2])]))
                cnt['fair_natural'] += nat; cnt['fair_L1'] += l1
                cnt['fair_L1_sprobe'] += l1 and sprobe
            evS.maybe_clear(); evH.maybe_clear()
        out['reps'].append(dict(rep=rep, counts=dict(cnt), founding=st))
        for k, v in cnt.items(): tot[k] += v
        print(rep, dict(cnt), st['steps_s0'], st['steps_s1'], st['coverage'], '%.0fs' % (time.time() - t0), flush=True)
    c = tot['coalitions']
    out['total'] = dict(tot)
    out['yield'] = dict(natural=tot['fair_natural'] / max(c, 1), L1=tot['fair_L1'] / max(c, 1),
                        L1_sprobe=tot['fair_L1_sprobe'] / max(tot['coalitions_sprobe'], 1),
                        L1_other=(tot['fair_L1'] - tot['fair_L1_sprobe']) / max(c - tot['coalitions_sprobe'], 1),
                        sprobe_share=tot['coalitions_sprobe'] / max(c, 1), coalitions=c)
    print('yield', json.dumps(out['yield']), flush=True)
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, 'static_yield_K%g.json' % K), 'w'), indent=1, default=str)


def assay(args):
    """The isolated pure coalition (D*, T1, T1), one island, no migration, with L1 founding lists (notes §1.2)."""
    R.load_costc()
    ev = R.evaluator('eq', 'S')
    rows = []
    t0 = time.time()
    co = R.coalition(ev, False)
    for rep in range(args.runs):
        cfg = dict(name='iso', arm='eq', mode='S', N=100, I=1, mN=0.0, forced=co, force_n=100)
        base = R.Run(ev, cfg, 5000 + rep)
        # the founding pass reads the forced founders (every founder of a slot is the coalition member)
        base.founders = tuple(np.full((1, 100), co[s][0], np.int64) for s in range(3))
        ft, st = FL.founding_pass(base)
        base.save_shared()
        seq = FL.founder_seq(base, ft)
        lists = [sorted(set(seq[100 * s + k] for k in range(100))) for s in range(3)]
        assert all(len(z) == 1 for z in lists), lists
        run = R.Run(ev, dict(cfg, forced=tuple(z[0] for z in lists)), 5000 + rep)
        run.prefill()
        run.run(R.HORIZON)
        RS = R.RunStats(run)
        f = RS.fair[:, 0]
        rows.append(dict(fair_end=bool(f[-1]), ever_fair=bool(f.any()), play_end=int(RS.play[-1, 0]),
                         play_0=int(RS.play[0, 0]), founding_lists=[str(z[0]) for z in lists],
                         no_triple_workers=st['no_triple_workers'], founding_ctr=st['ctr'], ctr=run.ctr[:19].tolist()))
    out = dict(n=len(rows), fair_end=sum(r['fair_end'] for r in rows), ever_fair=sum(r['ever_fair'] for r in rows),
               plays_end=dict(sorted(defaultdict(int, {k: sum(1 for r in rows if r['play_end'] == k)
                                                       for k in set(r['play_end'] for r in rows)}).items())),
               time_s=time.time() - t0, rows=rows)
    print(json.dumps({k: v for k, v in out.items() if k != 'rows'}), rows[0]['founding_lists'], flush=True)
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, 'assay_isolated_L1.json'), 'w'), indent=1)


def replay(args):
    """The bare-source replay (notes §1.0 item 4) on natural runs of replicates start..start+runs-1."""
    out = {}
    for rep in range(args.start, args.start + args.runs):
        r = FL.replay_job(rep)
        out[rep] = r
        print(rep, json.dumps(r), flush=True)
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, 'replay.json'), 'w'), indent=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('--cells', default='')
    ap.add_argument('--parent', default='S_eq')
    ap.add_argument('--runs', type=int, default=5)
    ap.add_argument('--start', type=int, default=0)
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--extend', type=int, default=1)
    ap.add_argument('--maxtasks', type=int, default=None)
    ap.add_argument('--n', type=int, default=200)
    ap.add_argument('--K', type=int, default=0)
    ap.add_argument('--plan', default='')
    ap.add_argument('--waitpid', type=int, default=0)
    args = ap.parse_args()
    globals()[args.cmd](args)


if __name__ == '__main__':
    main()
