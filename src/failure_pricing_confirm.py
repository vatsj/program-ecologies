"""Confirming failure pricing (rule A, P_fail = 0.1) as the default compute charge: runner and scores.

Spec specs/2026-10-25-failure-pricing-confirmation.md; hand derivations notes/failure-pricing-confirm.md section 1;
predictions predictions/2026-10-25-failure-pricing-confirm.md.  Imports the merged pricing code (src/pricing_rules*.py) and edits
none of it.  Fresh run indices only: PD reps 200-239, RPS and inspection runs 100-139.

    python3 src/failure_pricing_confirm.py lt <game> <geometry> <level> [<level> ...]      one process, levels in turn
    python3 src/failure_pricing_confirm.py pd <level> [--first 200 --runs 40]               one PD cell, one process

Outputs (small, tracked): runs/failure_pricing_confirm/{rps,insp}_<rule>_<level>_<cell>.json.gz and pd_<rule>_<level>.json.gz.
LOTTERY objects at fixed geometry, never pi.
"""
import gzip
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault('NUMBA_NUM_THREADS', '1')
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'runs', 'failure_pricing_confirm')

FRESH_LT = list(range(100, 140))
FRESH_PD = list(range(200, 240))
STORED_LT = {'primary': list(range(0, 80)), 'size': list(range(0, 20))}
STORED_PD = list(range(0, 40))

TH = dict(rps=0.10, rps_forfeit=0.05, insp=0.60, pd=0.70, pd_charge=0.3, pd_charge_tight=0.03)
RANGE = dict(rps=2.0, insp=5.0, pd=3.0)
TOL = 1e-9
PERSIST = 500
CPS = (500, 1000, 1500, 2000, 4000)


# ---------------------------------------------------------------------------------------------------------------- statistics
def boot(vals, B=4000, seed=20261025):
    v = np.asarray(vals, float); v = v[~np.isnan(v)]
    if len(v) == 0: return (float('nan'),) * 3
    idx = np.random.default_rng(seed).integers(len(v), size=(B, len(v)))
    m = v[idx].mean(1)
    return float(v.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def boot_paired(a, b, B=4000, seed=20261025):
    """Interval of mean(a - b) over paired runs."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    ok = ~(np.isnan(a) | np.isnan(b))
    return boot((a - b)[ok], B, seed)


def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'),) * 3
    p = k / n
    den = 1 + z * z / n
    ctr = (p + z * z / (2 * n)) / den
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return float(p), float(max(0, ctr - half)), float(min(1, ctr + half))


def status_le(t, th):
    """Target 'value <= th': met if the upper bound is at most th, failed if the lower bound exceeds it."""
    if t is None or np.isnan(t[0]): return 'n/a'
    if t[2] <= th + TOL: return 'met'
    if t[1] > th + TOL: return 'failed'
    return 'undetermined'


def status_ge(t, th):
    """Target 'value >= th': met if the lower bound is at least th, failed if the upper bound is below it."""
    if t is None or np.isnan(t[0]): return 'n/a'
    if t[1] >= th - TOL: return 'met'
    if t[2] < th - TOL: return 'failed'
    return 'undetermined'


_ORDER = {'failed': 0, 'undetermined': 1, 'met': 2}


def worst(*sts):
    sts = [s for s in sts if s in _ORDER]
    if not sts: return 'n/a'
    return min(sts, key=lambda s: _ORDER[s])


def classify(sts):
    """confirmed iff all met; refuted iff any failed; unresolved otherwise (notes 1.3)."""
    sts = list(sts)
    if any(s not in _ORDER for s in sts): return 'incomplete'
    if all(s == 'met' for s in sts): return 'confirmed'
    if any(s == 'failed' for s in sts): return 'refuted'
    return 'unresolved'


def rps_by_mixing(egross, forfeit):
    """By-mixing status from run values: e_gross upper <= 0.10 and forfeit upper <= 0.05 (notes 1.2a)."""
    a = status_le(boot(egross), TH['rps']); b = status_le(boot(forfeit), TH['rps_forfeit'])
    return worst(a, b), a, b


# ---------------------------------------------------------------------------------------------------------------- PD scores
def pd_flags(rec, cap=TH['pd_charge']):
    """Scores of one PD run record (the digest of pricing_rules_pd or this module): end-snapshot universal-open, persistent
    universal-open (frozen, or the last indicator change at least PERSIST generations before the end, or none), late,
    censored (not frozen), and the end-state charge per play and its cap test (notes 1.2b)."""
    uo = bool(rec['final'].get('universal_open'))
    frozen = rec['frozen_at'] >= 0
    ulc = rec['uo_last_change']; last = rec['last_gen']
    persistent = uo and (frozen or ulc < 0 or last - ulc >= PERSIST)
    led = rec.get('ledger')
    charge = float(led[3]) if led else float('nan')
    ok = persistent and (not np.isnan(charge)) and charge <= cap + TOL
    return dict(A=uo, B=persistent, C=bool(ok), late=bool(uo and not persistent), censored=not frozen, charge=charge,
                frozen=frozen)


def pd_counts(recs, cap=TH['pd_charge']):
    fl = [pd_flags(r, cap) for r in recs]
    n = len(fl)
    out = dict(n=n, A=sum(f['A'] for f in fl), B=sum(f['B'] for f in fl), C=sum(f['C'] for f in fl),
               late=sum(f['late'] for f in fl), censored=sum(f['censored'] for f in fl),
               charge_max=float(np.nanmax([f['charge'] for f in fl])) if fl else float('nan'))
    for k in 'ABC':
        out['w' + k] = wilson(out[k], n)
        out['s' + k] = status_ge(out['w' + k], TH['pd'])
    return out


# ---------------------------------------------------------------------------------------------------------------- inspection scores
def insp_island_means(tb, c0, c1, N):
    """Per island: gross and net means of the inspector (0) and inspectee (1), and the gross / net efficient flags
    (both roles >= -0.05; net = gross minus the rule's charge), notes 1.2c."""
    X0 = c0 / float(N); X1 = c1 / float(N)
    u0g = (X0 * (X1 @ tb.UAg.T)).sum(1); u1g = (X1 * (X0 @ tb.UBg.T)).sum(1)
    u0 = (X0 * (X1 @ tb.UA.T)).sum(1); u1 = (X1 * (X0 @ tb.UB.T)).sum(1)
    eg = (u0g >= -0.05 - TOL) & (u1g >= -0.05 - TOL)
    en = (u0 >= -0.05 - TOL) & (u1 >= -0.05 - TOL)
    return dict(u0g=u0g, u1g=u1g, u0=u0, u1=u1, eff_gross=eg.astype(float), eff_net=en.astype(float))


# ---------------------------------------------------------------------------------------------------------------- L_T runner
def depth_arrays(eng, xs, ys):
    """Per ordered pair (x plays against y): expected timed-out calls by position in the call forest: topmost (no timed-out
    ancestor), nested (inside another timed-out call), issued from the opponent's code (the call's issuer is not x)."""
    nx, ny = len(xs), len(ys)
    top = np.zeros((nx, ny)); nested = np.zeros((nx, ny)); opp = np.zeros((nx, ny)); tot = np.zeros((nx, ny))
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            rec = eng.ledger(x, y)
            for (w, out, used, calls, reason) in rec['leaves']:
                w = float(w)
                to = {c[0]: c[5] for c in calls}; par = {c[0]: c[1] for c in calls}
                for c in calls:
                    if not c[5]: continue
                    p = c[1]; nest = False
                    while p != -1:
                        if to.get(p, False): nest = True; break
                        p = par.get(p, -1)
                    tot[i, j] += w
                    if nest: nested[i, j] += w
                    else: top[i, j] += w
                    if eng.key_list[c[3]][0] != x: opp[i, j] += w
    return dict(top=top, nested=nested, opp=opp, tot=tot)


class LTContext:
    """The merged Base of a game plus the depth tables, built once per process."""

    def __init__(self, game):
        import pricing_rules_lt as PL
        self.PL = PL
        self.game = game
        self.base = PL.Base(game)
        b = self.base
        if game == 'rps':
            t = b.tb.terms[0]
            self.depth = [depth_arrays(b.eng, t, t)]
        else:
            t0, t1 = b.tb.terms
            self.depth = [depth_arrays(b.eng, t0, t1), depth_arrays(b.eng, t1, t0)]


def lt_ext_rps(ctx, tb, full, N, I, named):
    import lt_tape_run as R
    b = ctx.base
    names = tb.names[0]
    ext = {}
    st = R.rps_island_stats(full[2000], N, tb, named[0])
    for k in ('e_gross', 'e_prog', 'forfeit', 'mix'):
        ext['isl_' + k] = [round(float(x), 5) for x in st[k]]
    dom = {}; sup = {}
    for g in CPS:
        c = full[g]
        dom[str(g)] = c.argmax(1).tolist()
        sup[str(g)] = [np.nonzero(row / float(N) >= 0.05)[0].tolist() for row in c]
    ext['dom'] = dom
    ext['support2000'] = sup['2000']
    trans = {}
    gl = list(CPS)
    for a, c in zip(gl[:-1], gl[1:]):
        trans['%d-%d' % (a, c)] = dict(modal=float(np.mean([dom[str(a)][i] != dom[str(c)][i] for i in range(I)])),
                                       support=float(np.mean([sup[str(a)][i] != sup[str(c)][i] for i in range(I)])))
    ext['transitions'] = trans
    ext['modal_share'] = {k: float(np.mean([names[d] == k for d in dom['2000']])) for k in ('PRR', 'U', 'PB', 'CRR')}
    ext['to'] = {}
    d = ctx.depth[0]
    for g in (500, 2000):
        X = full[g] / float(N)
        to_prog = (X * np.einsum('ab,ib->ia', b.arrays['n_to'], X)).mean(0)
        ext['to'][str(g)] = dict(play=float(np.einsum('ia,ab,ib->i', X, b.arrays['n_to'], X).mean()),
                                 top=float(np.einsum('ia,ab,ib->i', X, d['top'], X).mean()),
                                 nested=float(np.einsum('ia,ab,ib->i', X, d['nested'], X).mean()),
                                 opp=float(np.einsum('ia,ab,ib->i', X, d['opp'], X).mean()),
                                 by_prog=[round(float(v), 6) for v in to_prog])
    return ext


def lt_ext_insp(ctx, tb, full, N, I, named):
    b = ctx.base
    n0, n1 = tb.names
    ext = {}
    c0, c1 = full[2000]
    m = insp_island_means(tb, c0, c1, N)
    for k in ('u0g', 'u1g', 'u0', 'u1', 'eff_gross', 'eff_net'):
        ext['isl_' + k] = [round(float(x), 5) for x in m[k]]
    dom = {}; sup = {}
    for g in CPS:
        a0, a1 = full[g]
        dom[str(g)] = [a0.argmax(1).tolist(), a1.argmax(1).tolist()]
        sup[str(g)] = [[np.nonzero(r / float(N) >= 0.05)[0].tolist() for r in a0], [np.nonzero(r / float(N) >= 0.05)[0].tolist() for r in a1]]
    ext['dom'] = dom
    ext['support2000'] = sup['2000']
    trans = {}
    gl = list(CPS)
    for a, c in zip(gl[:-1], gl[1:]):
        mod = np.mean([(dom[str(a)][0][i], dom[str(a)][1][i]) != (dom[str(c)][0][i], dom[str(c)][1][i]) for i in range(I)])
        sp = np.mean([(sup[str(a)][0][i], sup[str(a)][1][i]) != (sup[str(c)][0][i], sup[str(c)][1][i]) for i in range(I)])
        trans['%d-%d' % (a, c)] = dict(modal=float(mod), support=float(sp))
    ext['transitions'] = trans
    ext['to'] = {}
    for g in (500, 2000):
        a0, a1 = full[g]
        X0 = a0 / float(N); X1 = a1 / float(N)
        d0, d1 = ctx.depth
        r = dict(
            play=0.5 * (np.einsum('ia,ib,ab->i', X0, X1, b.arr0['n_to']).mean() + np.einsum('ib,ia,ba->i', X1, X0, b.arr1['n_to']).mean()))
        for key in ('top', 'nested', 'opp'):
            r[key] = 0.5 * (np.einsum('ia,ib,ab->i', X0, X1, d0[key]).mean() + np.einsum('ib,ia,ba->i', X1, X0, d1[key]).mean())
        r['role0'] = float(np.einsum('ia,ib,ab->i', X0, X1, b.arr0['n_to']).mean())
        r['role1'] = float(np.einsum('ib,ia,ba->i', X1, X0, b.arr1['n_to']).mean())
        r = {k: float(v) for k, v in r.items()}
        r['by_prog0'] = [round(float(v), 6) for v in (X0 * (X1 @ b.arr0['n_to'].T)).mean(0)]
        r['by_prog1'] = [round(float(v), 6) for v in (X1 * (X0 @ b.arr1['n_to'].T)).mean(0)]
        ext['to'][str(g)] = r
    return ext


def lt_cell(ctx, rule, level, cell, runs=FRESH_LT, out_dir=OUT, quiet=False, no_write=False):
    """One cell: rule in {Z, A}, level, geometry cell ('primary' (100, 64) or 'size' (400, 16)).  Returns the records."""
    import lt_tape_run as R
    PL = ctx.PL
    PL.OUT = out_dir
    game = ctx.game
    base = ctx.base
    tb = base.view(rule, level)
    named = R.named_idx(tb)
    cfg = R.CELLS[cell]
    N, I = cfg['N'], cfg['I']
    label = PL.seed_label(rule, level)
    name = '%s_%s_%g_%s' % (game, rule, level, cell)
    recs = []
    for r in runs:
        t1 = time.time()
        if game == 'rps': full, ex = PL.lottery_rps_exact(tb, cell, r, N, I, label)
        else: full, ex = PL.lottery_insp_exact(tb, cell, r, N, I, label)
        rec = PL.make_record(base, tb, full, N, ex, named, r, time.time() - t1, name)
        rec['ext'] = lt_ext_rps(ctx, tb, full, N, I, named) if game == 'rps' else lt_ext_insp(ctx, tb, full, N, I, named)
        recs.append(rec)
        if not quiet: print('%s run %d wall %.1f' % (name, r, time.time() - t1), flush=True)
    meta = dict(name=name, game=game, rule=rule, level=level, cell=cell, K=base.K, N=N, I=I, runs=list(runs), names=tb.names,
                fam=[f.tolist() for f in tb.fam], mismatch=base.mismatch, label=label)
    if not no_write:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, name + '.json.gz')
        with gzip.open(path + '.tmp', 'wt') as f:
            json.dump(dict(meta=meta, recs=recs), f)
        os.replace(path + '.tmp', path)
    return dict(meta=meta, recs=recs)


# ---------------------------------------------------------------------------------------------------------------- PD runner
LASTC = {}


def _make_priced_run_c():
    import pricing_rules_pd as PD

    class PricedRunC(PD.PricedRun):
        """The priced run with the population ledger recorded after every advance (read-only: the state is untouched, so the
        trajectory equals PricedRun's draw for draw)."""

        def __init__(self, cell, rep, track=True):
            super().__init__(cell, rep, track=track)
            self.ltrace = []
            self._g_prev = 0

        def advance(self, gens):
            super().advance(gens)
            L = PD.pop_ledger(self.counts, self.pres, self.npres, self.N, self.tunit, self.tsp, self.trule, self.PX)
            m = L.mean(0)
            self.ltrace.append((int(self.g), int(self.g - self._g_prev), float(m[0]), float(m[1]), float(m[2]), float(m[3])))
            self._g_prev = int(self.g)

        def final_logs(self):
            super().final_logs()
            LASTC['ltrace'] = list(self.ltrace)

    return PD, PricedRunC


def trace_stats(ltrace, scr=200):
    """Scramble (checkpoints with g <= scr) and cumulative interval-weighted means of steps, timeouts and charge per play."""
    if not ltrace: return dict(scr_charge=float('nan'), cum_charge=float('nan'), scr_to=float('nan'), cum_to=float('nan'))
    t = np.array(ltrace, float)
    w = t[:, 1]
    s = t[:, 0] <= scr

    def avg(col, mask):
        ww = w[mask]
        return float((t[mask, col] * ww).sum() / ww.sum()) if ww.sum() > 0 else float('nan')
    return dict(scr_charge=avg(5, s), cum_charge=avg(5, np.ones(len(t), bool)), scr_to=avg(4, s), cum_to=avg(4, np.ones(len(t), bool)),
                scr_steps=avg(2, s), cum_steps=avg(2, np.ones(len(t), bool)))


def pd_digest(PD, r, ltrace):
    d = PD.digest(r)
    d['holders'] = r['final'].get('holders')
    ch = r.get('changes', [])
    d['n_changes_after500'] = int(sum(1 for c in ch if c[0] > 500))
    d['n_changes'] = int(len(ch))
    d['ltrace_stats'] = trace_stats(ltrace)
    d['ltrace_pts'] = [t for t in ltrace if t[0] in (10, 50, 100, 200, 500, 1000, 2000, 5000, 10000)]
    return d


def pd_run(PD, PRC, cell, rep, rule, level, horizon=10000):
    import world_k as WK
    PD.CFG.update(rule=rule, level=level, cst=None)
    WK.IslandRun = PRC
    t0 = time.time()
    r = WK.island_job((cell, rep, 'K', horizon, False))
    r['rule'] = rule; r['level'] = level; r['time_total'] = time.time() - t0
    r['ledger'] = PD.LAST.get('ledger')
    return r


def pd_cell(rule, level, reps=FRESH_PD, cell='wk_Snon_100_64', out_dir=OUT, horizon=10000, name=None, quiet=False):
    PD, PRC = _make_priced_run_c()
    os.makedirs(out_dir, exist_ok=True)
    name = name or 'pd_%s_%g' % (rule, level)
    path = os.path.join(out_dir, name + '.json.gz')
    recs = []
    if os.path.exists(path):
        recs = json.load(gzip.open(path, 'rt'))['recs']
    done = {r['rep'] for r in recs}
    for rep in reps:
        if rep in done: continue
        t0 = time.time()
        res = pd_run(PD, PRC, cell, rep, rule, level, horizon)
        d = pd_digest(PD, res, LASTC.get('ltrace', []))
        d['wall'] = time.time() - t0
        recs.append(d)
        f = pd_flags(d)
        if not quiet:
            print('%s rep %d uo=%s persistent=%s pcc=%.4f last_gen=%d frozen=%d charge=%.5f scr=%.5f wall=%.0fs' % (
                name, rep, d['final'].get('universal_open'), f['B'], d['final'].get('pcc', float('nan')), d['last_gen'], d['frozen_at'],
                f['charge'], d['ltrace_stats']['scr_charge'], d['wall']), flush=True)
        with gzip.open(path + '.tmp', 'wt') as fh:
            json.dump(dict(meta=dict(name=name, rule=rule, level=level, cell=cell, horizon=horizon, reps=list(reps)), recs=recs), fh)
        os.replace(path + '.tmp', path)
    return recs


# ---------------------------------------------------------------------------------------------------------------- provenance
def _sha(path, chunk=1 << 22):
    import hashlib
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            b = f.read(chunk)
            if not b: break
            h.update(b)
    return h.hexdigest()


def cache_hashes():
    """sha256 of the imported untracked world-K caches (single files; the static directories as one digest over the sorted
    relative paths, sizes and file digests).  Read-only use: pre and post digests must agree (notes 1.6)."""
    import hashlib
    out = {}
    for sub in ('runs/provenance', 'runs/detectors/K'):
        for f in ('sets.npz', 'OSV.npy', 'SPO.npy', 'prod_exec.json', 'grudge.npz'):
            p = os.path.join(ROOT, sub, f)
            if os.path.exists(p): out[sub + '/' + f] = _sha(p)
        d = os.path.join(ROOT, sub, 'static')
        if os.path.isdir(d):
            h = hashlib.sha256()
            n = 0
            for fn in sorted(os.listdir(d)):
                p = os.path.join(d, fn)
                if os.path.isfile(p):
                    h.update(fn.encode()); h.update(str(os.path.getsize(p)).encode()); h.update(_sha(p).encode()); n += 1
            out[sub + '/static'] = '%s (%d files)' % (h.hexdigest(), n)
    return out


def code_hashes():
    import glob
    out = {}
    for p in sorted(glob.glob(os.path.join(HERE, 'pricing_rules*.py')) + glob.glob(os.path.join(HERE, 'failure_pricing_confirm*.py'))):
        out[os.path.relpath(p, ROOT)] = _sha(p)
    for f in ('world_k.py', 'provenance.py', 'provenance_run.py', 'realizable_scaling.py', 'annealed.py', 'lt_tape.py', 'lt_tape_run.py'):
        p = os.path.join(HERE, f)
        if os.path.exists(p): out['src/' + f] = _sha(p)
    return out


# ---------------------------------------------------------------------------------------------------------------- CLI
def main(argv):
    mode = argv[0]
    if mode == 'lt':
        game, geom = argv[1], argv[2]
        cell = {'100_64': 'primary', '400_16': 'size'}[geom]
        specs = argv[3:]
        ctx = LTContext(game)
        for s in specs:
            rule, level = s.split('@') if '@' in s else ('A', s)
            level = float(level)
            if os.path.exists(os.path.join(OUT, '%s_%s_%g_%s.json.gz' % (game, rule, level, cell))): continue
            lt_cell(ctx, rule, level, cell)
    elif mode == 'pd':
        rule = 'Z' if float(argv[1]) == 0.0 else 'A'
        level = float(argv[1])
        first = 200; runs = 40
        if '--first' in argv: first = int(argv[argv.index('--first') + 1])
        if '--runs' in argv: runs = int(argv[argv.index('--runs') + 1])
        pd_cell(rule, level, reps=list(range(first, first + runs)))
    else:
        raise SystemExit('mode?')


if __name__ == '__main__':
    main(sys.argv[1:])
