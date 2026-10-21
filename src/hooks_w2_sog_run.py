"""Hooks, Part W2: union-game cells with union contracts (notes/hooks-w2.md §1.4-§1.7).  A copy of hooks_w_sog_run.py:
founders, fill draws and kernel seeds are Part W's, so `myopic-ref` is Part W's maximal rerun.

    python3 src/hooks_w2_sog_run.py validate [REPS]  # reproduction of Part W's stored sog-maximal rows
    python3 src/hooks_w2_sog_run.py time CELL --gens G --reps R
    python3 src/hooks_w2_sog_run.py batch CELL[,CELL...] --procs 3
Rows: runs/hooks_w2/sog-CELL.json.
"""
import argparse, json, os, sys, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from numba.typed import Dict
from numba import types
import union as U
import hooks_w2_sog as S
import hooks_w2_sog_kern as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'hooks_w2')
STORED = os.path.join(ROOT, 'runs', 'hooks_w')
SALT = 20261018
W = 0.3
GEO = dict(N=int(os.environ.get('HOOKS_SOG_N', 30)), I=16, mN=1.0)
GENS = 1000
CHECKS = [0, 10, 25, 50, 100, 200, 300, 500, 750, 1000, 1250, 1500, 1750, 2000]
COPY_Q = 0.1
TCAP = 60000
LABELS = ['fair', 'intermediate', 'zero wage', 'strike', 'scab split', 'repression:strike', 'repression:source']
_ALL = np.ones((4, 4), np.bool_)


def _act(scope=(), origin=()):
    a = _ALL.copy()
    for s in scope: a[s, :] = False
    for o in origin: a[:, o] = False
    return a


BASECFG = dict(recency=0, grudge=1, thanks=1, contract=1, copy=1, shuffle=0, noinherit=0, enc=1, keep_origin=0,
               union=0, role=0, pboss=0)
CELLS = {
    # Part W's maximal rerun (the paired reference): no union contracts, boss-worker contracts myopic
    'myopic-ref':   dict(active=_ALL),
    # union contracts (notes 1.4): (M) myopic, (C) credible response with the boss's response implemented
    'union-M':      dict(active=_ALL, union=1),
    'union-C':      dict(active=_ALL, union=2, pboss=1),
    'union-C-role': dict(active=_ALL, union=2, pboss=1, role=1),
    # control: Part W's maximal with the (C) protection of the boss's contracted wage, no union contracts
    'bw-only-C':    dict(active=_ALL, pboss=1),
    # validation aliases of Part W's cells
    'maximal':      dict(active=_ALL),
    'inert':        dict(active=np.zeros((4, 4), np.bool_)),
}
ORDER = ['myopic-ref', 'union-M', 'union-C', 'bw-only-C', 'union-C-role']

_LANG = {}


def lang(hooks=True):
    if hooks not in _LANG:
        _LANG[hooks] = S.SogLang(hooks=hooks)
    return _LANG[hooks]


def tables():
    PAY = U.payoff_table(0.5)
    SUMT = np.zeros((36, 2, 2), np.int64)
    for j in range(36):
        for t1 in range(2):
            for t2 in range(2):
                SUMT[j, t1, t2] = U.summary(j, t1, t2)
    return PAY, SUMT


def cfg_of(c):
    d = dict(BASECFG); d.update({k: v for k, v in c.items() if k in BASECFG})
    return np.array([d['recency'], d['grudge'], d['thanks'], d['contract'], d['copy'], d['shuffle'], d['noinherit'],
                     d['enc'], 1, d['keep_origin'], d['union'], d['role'], d['pboss']], np.int64)


def new_tables(cap=TCAP):
    T = (np.zeros(cap, np.int64), np.zeros(cap, np.int64), np.zeros(cap, np.int64), np.zeros((cap, 4), np.int64),
         np.zeros(cap, np.int64), np.zeros(cap, np.int64), np.zeros(cap, np.int64), np.zeros(cap, np.bool_),
         np.zeros((cap, 128), np.int8), np.zeros((cap, 2), np.int64), np.zeros(cap, np.int64), np.zeros(cap, np.int64),
         np.zeros(2, np.int64), np.zeros(cap, np.int64))
    tdict = Dict.empty(key_type=types.UniTuple(types.int64, 3), value_type=types.int64)
    ev = Dict.empty(key_type=types.UniTuple(types.int64, 6), value_type=types.int64)
    return T, tdict, ev


# ------------------------------------------------------------------ founders (coupled across cells)
def founders(rep, L, N, I, plain=False):
    """bases[i, s, n] and fills per founder; lineage of founder (i, s, n) = (i*3 + s)*N + n.  Bases from stream
    [SALT, rep, 5, s]; fills from [SALT, rep, 5, lineage, 1], the same draws whatever the founder's tags."""
    NL = 3 * N * I
    bases = np.zeros((I, 3, N), np.int64)
    for s in range(3):
        mu = L.muB if s == 0 else L.muW
        bases[:, s, :] = np.random.default_rng([SALT, rep, 5, s, int(plain)]).choice(len(mu), size=(I, N), p=mu)
    fills = {}
    if plain:
        return bases, fills
    for i in range(I):
        for s in range(3):
            nact = 9 if s == 0 else 2
            for n in range(N):
                lin = (i * 3 + s) * N + n
                r = np.random.default_rng([SALT, rep, 5, lin, 1])
                tg = int(L.htags[0 if s == 0 else 1, bases[i, s, n]])
                tags = [t for t in (0, 1) if (tg >> t) & 1]
                k = int(r.choice(5, p=S.POISSON))
                fl = []
                for _ in range(k):
                    ut = int(r.integers(2)); sc = int(r.integers(4)); kh = int(r.integers(NL))
                    kb = int(r.integers(16)); kr = int(r.integers(2)); a = int(r.integers(nact))
                    if not tags:
                        continue
                    t = tags[ut % len(tags)] if len(tags) == 2 else tags[0]
                    key = {S.NONE: 0, S.ROLE: (0 if s == 0 else 1 + kr), S.HIST: kh, S.BEH: kb}[sc]
                    fl.append(S.fcode(a, t, sc, S.SEEDED, key))
                if fl:
                    fills[lin] = fl
    return bases, fills


# ------------------------------------------------------------------ one run
def run_one(cell, rep, gens=GENS):
    c = CELLS[cell]
    if c.get('stored'):
        return stored_run(rep, gens)
    plain = c.get('plain', False)
    L = lang(hooks=not plain)
    PAY, SUMT = tables()
    N, I, mN = GEO['N'], GEO['I'], GEO['mN']
    active = np.zeros((4, 4), np.bool_) if plain else c['active']
    cfg = cfg_of(c)
    if plain:
        cfg[7] = 0
    recency = int(cfg[0])
    T, tdict, ev = new_tables()
    bases, fills = founders(rep, L, N, I, plain)
    pres = np.zeros((I, 3, N), np.int64); cnt = np.zeros((I, 3, N), np.int64); npres = np.zeros((I, 3), np.int64)
    for i in range(I):
        for s in range(3):
            seen = {}
            for n in range(N):
                lin = 0 if plain else (i * 3 + s) * N + n
                fl = fills.get((i * 3 + s) * N + n, [])
                f = np.zeros(4, np.int64); f[:len(fl)] = fl
                t = K.get_type(T, tdict, L.htags, L.wtag, active, recency, s, int(bases[i, s, n]), lin, f, len(fl))
                seen[t] = seen.get(t, 0) + 1
            for t, k in seen.items():
                pres[i, s, npres[i, s]] = t; cnt[i, s, npres[i, s]] = k; npres[i, s] += 1
                T[11][t] += k
    J = np.zeros((I, N, N, N), np.int16); F = np.zeros((I, 3, N))
    chk = np.array([x for x in CHECKS if x <= gens], np.int64)
    rec = np.zeros((len(chk), I, K.NST)); rec_g = np.zeros((len(chk), 4))
    es = np.zeros((3, 4, 4)); thr = np.zeros((3, 4)); ctr = np.zeros(24, np.int64); ustat = np.zeros(40, np.int64)
    seed = (SALT * 11 + 1000003 * rep) % (2 ** 31)
    t0 = time.time()
    nrec = K.kernel(L.arrays(), U.TT, L.htags, L.wtag, PAY, SUMT, T, tdict, ev, active, cfg, COPY_Q, pres, cnt, npres,
                    J, F, N, W, mN / N, gens, seed, chk, rec, rec_g, es, thr, ctr, ustat)
    wall = time.time() - t0
    return summarize(cell, rep, L, T, pres, cnt, npres, chk[:nrec], rec[:nrec], rec_g[:nrec], es, thr, ctr, fills, wall,
                     ustat)


def summarize(cell, rep, L, T, pres, cnt, npres, chk, rec, rec_g, es, thr, ctr, fills, wall, ustat=None):
    fin = rec[-1]
    lab = [int(np.argmax(fin[i, :7])) for i in range(fin.shape[0])]
    share = {LABELS[z]: round(float(np.mean([l == z for l in lab])), 4) for z in range(7)}
    ts = [dict(gen=int(g), labels=[int(np.argmax(rec[k][i, :7])) for i in range(rec.shape[1])],
               fair=round(float(np.mean([np.argmax(rec[k][i, :7]) == 0 for i in range(rec.shape[1])])), 4),
               wage=[round(float(x), 4) for x in rec[k][:, 7:10].mean(0)],
               boss=round(float(rec[k][:, 10].mean()), 4), worker=round(float(rec[k][:, 11].mean()), 4),
               whack=round(float(rec[k][:, 13].mean()), 5), live=int(rec_g[k][0])) for k, g in enumerate(chk)]
    # held fills by slot, scope, origin, threat at the horizon
    held = np.zeros((3, 4, 4, 2), np.int64)
    uheld = np.zeros((3, 2), np.int64)          # individuals holding at least one demand fill, by slot and s
    Tf, Tn = T[3], T[4]
    maj = []
    for i in range(pres.shape[0]):
        m = []
        for s in range(3):
            for q in range(int(npres[i, s])):
                t = int(pres[i, s, q]); k = int(cnt[i, s, q])
                seen_s = set()
                for j in range(int(Tn[t])):
                    f = int(Tf[t, j]); a = S.g_action(f)
                    held[s, S.g_scope(f), S.g_origin(f), int(S.is_threat(s, a))] += k
                    if s > 0 and a >= 2 and ((int(T[5][t]) >> S.g_tag(f)) & 1):
                        seen_s.add(a - 2)
                for a_ in seen_s:
                    uheld[s, a_] += k
            q = int(np.argmax(cnt[i, s, :npres[i, s]]))
            t = int(pres[i, s, q])
            m.append(dict(src=L.src(0 if s == 0 else 1, int(T[1][t])), lin=int(T[2][t]), share=int(cnt[i, s, q]),
                          fills=[_dec(int(Tf[t, j]), s) for j in range(int(Tn[t]))]))
        maj.append(m)
    seeded = np.zeros((3, 4, 2), np.int64)
    for lin, fl in fills.items():
        s = (lin // GEO['N']) % 3
        for f in fl:
            seeded[s, S.g_scope(f), int(S.is_threat(s, S.g_action(f)))] += 1
    return dict(cell=cell, rep=rep, wall=round(wall, 1), labels=lab, shares=share,
                fair=share['fair'], intermediate=share['intermediate'], zero=share['zero wage'],
                wage=[round(float(x), 4) for x in fin[:, 7:10].mean(0)], boss=round(float(fin[:, 10].mean()), 4),
                worker=round(float(fin[:, 11].mean()), 4), whack=round(float(fin[:, 13].mean()), 5),
                counters=[int(x) for x in ctr], enc_stats=es.astype(np.int64).tolist(), threat=thr.astype(np.int64).tolist(),
                held=held.tolist(), union_held=uheld.tolist(), ustat=[int(x) for x in ustat] if ustat is not None else None,
                seeded=seeded.tolist(), ts=ts, majority=maj)


def _dec(f, s):
    a = S.g_action(f)
    an = U.bname(a) if s == 0 else ['work', 'strike', 'demand-1/4', 'demand-1/2'][a]
    return '%s:%s:%s:%d:t%d' % (S.SCOPES[S.g_scope(f)], S.ORIGINS[S.g_origin(f)], an, S.g_key(f), S.g_tag(f))


# ------------------------------------------------------------------ the stored baseline
def stored_run(rep, gens=GENS, cellname='CC-mN1', N=None):
    """sog_lottery's kernel, class tables and seeds of the stored cell CC-mN1 (I = 16, mN = 1), at island size N
    (default: this run's geometry; the stored cell itself has N = 100), run to `gens` generations."""
    import sog_lottery as SL
    p = dict(SL.CELLS[cellname])
    p['N'] = GEO['N'] if N is None else N
    C = SL._cdata(p)
    PAY, T_ = SL.code_tables(p['c'], p['pool'])
    LB, LW = SL.lineage_masks(C)
    pB, pW = SL.seed_dists(C, p['striker'], p['boss'], p.get('swap'))
    seed = SL.run_seed(cellname, rep)
    rng = np.random.default_rng(seed)
    init = SL.init_counts(rng, p['I'], p['N'], pB, pW)
    chk = SL.checks_schedule(gens)
    t0 = time.time()
    status, stop, counts, stats, ts, cum, integ, ext, nmig, ci = SL.kern(
        np.ascontiguousarray(C['Jc']), C['tagc'].astype(np.int64), PAY, T_, SL.KEYT, LB, LW, init, p['N'], SL.W,
        p['mN'] / p['N'], seed % (2 ** 31), chk, 500, gens // 2)
    fin = stats[-1]
    lab = [int(np.argmax(fin[i, :7])) for i in range(p['I'])]
    share = {LABELS[z]: round(float(np.mean([l == z for l in lab])), 4) for z in range(7)}
    return dict(cell='baseline', rep=rep, wall=round(time.time() - t0, 1), status=int(status), stop=int(stop),
                labels=lab, shares=share, fair=share['fair'], intermediate=share['intermediate'], zero=share['zero wage'])


def _stored_rows(cell):
    import gzip
    return {r['rep']: r for r in json.load(gzip.open(os.path.join(STORED, 'sog-%s.json.gz' % cell))) if 'error' not in r}


def validate(nreps=2):
    """Reproduction check: with union contracts and protection off this module's `maximal` cell reproduces Part W's
    stored sog-maximal rows (final island labels, the records at every stored generation, the 11 counters)."""
    stored = _stored_rows('maximal')
    out = []
    for rep in range(nreps):
        row = run_one('maximal', rep)
        st = stored[rep]
        by_gen = {t['gen']: t for t in st['ts']}
        eq_ts = all(t['labels'] == by_gen[t['gen']]['labels'] and t['wage'] == by_gen[t['gen']]['wage'] for t in row['ts']
                    if t['gen'] in by_gen)
        out.append(dict(rep=rep, labels_equal=bool(row['labels'] == st['labels']), records_equal=bool(eq_ts),
                        counters_equal=bool(row['counters'][:11] == st['counters'][:11]), fair=row['fair'], stored_fair=st['fair'],
                        wall=row['wall']))
        print(out[-1], flush=True)
    return out


def _job(args):
    cell, rep = args
    try:
        return run_one(cell, rep)
    except Exception:
        import traceback
        return dict(cell=cell, rep=rep, error=traceback.format_exc())


def run_batch(cells, procs, nrep=40):
    from multiprocessing import Pool
    os.makedirs(OUT, exist_ok=True)
    rows = {}; jobs = []
    for cell in cells:
        path = os.path.join(OUT, 'sog-%s.json' % cell)
        rows[cell] = [r for r in (json.load(open(path)) if os.path.exists(path) else []) if 'error' not in r]
        done = {r['rep'] for r in rows[cell]}
        jobs += [(cell, r) for r in range(nrep) if r not in done]
    print('%d jobs' % len(jobs), flush=True)
    lang(True); lang(False)
    with Pool(procs, maxtasksperchild=8) as pool:
        for row in pool.imap_unordered(_job, jobs):
            cell = row['cell']
            if 'error' in row:
                print('ERROR', cell, row['rep'], row['error'], flush=True)
                continue
            rows[cell].append(row)
            print('sog %s rep %d: fair %.3f int %.3f zero %.3f (%.0fs)' % (cell, row['rep'], row['fair'], row['intermediate'],
                                                                          row['zero'], row['wall']), flush=True)
            json.dump(sorted(rows[cell], key=lambda r: r['rep']), open(os.path.join(OUT, 'sog-%s.json' % cell), 'w'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('cell', nargs='?')
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--gens', type=int, default=GENS)
    ap.add_argument('--reps', type=int, default=1)
    a = ap.parse_args()
    if a.cmd == 'validate':
        out = validate(a.reps)
        json.dump(out, open(os.path.join(ROOT, 'runs', 'hooks-w2-sog-validate.json'), 'w'), indent=1)
    elif a.cmd == 'time':
        for r in range(a.reps):
            t = time.time()
            row = run_one(a.cell, 1000 + r, gens=a.gens)
            print(a.cell, 'probe', 1000 + r, 'gens', a.gens, 'wall %.1f' % (time.time() - t), 'shares', row['shares'],
                  'counters', row.get('counters'), 'threat', row.get('threat'), 'ustat', row.get('ustat'), 'union_held',
                  row.get('union_held'), flush=True)
    elif a.cmd == 'batch':
        cells = ORDER if a.cell == 'sog' else a.cell.split(',')
        run_batch(cells, a.procs)


if __name__ == '__main__':
    main()
