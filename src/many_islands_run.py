"""Drivers for the many-islands experiment (spec specs/2026-10-25-many-islands.md; notes notes/many-islands.md).

    python3 src/many_islands_run.py validate                  # -> runs/many-islands-validate.json
    python3 src/many_islands_run.py pool ARM A IDX [N_ISL]    # one pool of settled islands -> runs/many_islands/pool_*.npz
    python3 src/many_islands_run.py chain ARM A IDX CAP       # pool Monte Carlo of the jump chain (pool IDX) -> runs/many_islands/chain_*.json
One job per process.  Pools (npz) are not committed; summaries (json) are.
"""
import json, os, sys, time, zlib, math, resource
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import many_islands as MI
import stable_sets as SS

ROOT = MI.ROOT
OUT = os.path.join(ROOT, 'runs', 'many_islands')
os.makedirs(OUT, exist_ok=True)

CHECKPOINTS = (1, 3, 10, 30, 100, 300, 1000)               # the spec's, events per island
EXT = (3000, 10000, 30000, 100000)                          # extension (not in the spec)


def crc(s):
    return zlib.crc32(s.encode()) & 0x7fffffff


def wilson(k, n, z=1.96):
    if n == 0:
        return (float('nan'), float('nan'))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def group_of(arm):
    """L and M share the catalogue and the seed law (paired founders); R and Rw share theirs."""
    return 'LM' if arm in ('L', 'M') else 'R'


# ====================================================================== pools
def pool_path(arm, A, idx):
    return os.path.join(OUT, 'pool_%s_A%d_p%d.npz' % (arm, A, idx))


def build_pool(arm_name, A, idx, n_isl=16384, log=None):
    """n_isl independent islands: founding multinomial per slot (a stream common to arms of one group and to every A,
    by island index), Poisson(A) arrivals (a stream common to arms of one group), relaxation to monomorphism."""
    arm = MI.Arm(arm_name)
    arm.new_cache(24)
    g = group_of(arm_name)
    triples = -np.ones((n_isl, 3), np.int16)
    status = np.zeros(n_isl, np.int8)
    gens = np.zeros(n_isl, np.int64)
    narr = np.zeros(n_isl, np.int32)
    t0 = time.time()
    capped = []
    for i in range(n_isl):
        if i % 128 == 0:
            arm.maybe_flush(0.45)
        rf = np.random.default_rng(crc('mi-found|%s|%d|%d' % (g, idx, i)))
        ra = np.random.default_rng(crc('mi-arr|%s|%d|%d|%d' % (g, A, idx, i)))
        init = np.stack([rf.multinomial(MI.N0, arm.laws[s]) for s in range(3)]).astype(np.int64)
        arr = MI.arrival_times(ra, A)
        H = int(arr[-1] if len(arr) else 0.0) + 20002
        seed = crc('mi-kern|%s|%s|%d|%d|%d' % (arm_name, 'x', A, idx, i)) % (2 ** 31)
        st, gg, counts, na = MI.island_run(arm.ctx(), arm.lc(32 if A == 0 else 64), MI.PAY, init, MI.N0, MI.W, seed, H,
                                          arr, arm.cum, True)
        status[i] = st; gens[i] = gg; narr[i] = na
        if st == 0:
            triples[i] = MI.triple_of(counts)
        else:
            c, e = MI.classify_counts(arm, counts)
            capped.append((i, int(c), float(e)))
        if log and i % 1024 == 1023:
            print('%s A%d p%d: %d islands, %.0f s, capped %d' % (arm_name, A, idx, i + 1, time.time() - t0, len(capped)),
                  file=log, flush=True)
    np.savez_compressed(pool_path(arm_name, A, idx), triples=triples, status=status, gens=gens, narr=narr,
                        capped=np.array(capped, dtype=np.float64).reshape(-1, 3))
    return dict(arm=arm_name, A=A, idx=idx, n=n_isl, wall=time.time() - t0, capped=len(capped),
                max_gen=int(gens.max()), flushes=int(arm.cache['meta'][1]))


# ====================================================================== the chain on a pool
PIECE = 20_000_000                                          # events per njit call (the table is flushed between calls)


def load_pool(arm, A, idx):
    z = np.load(pool_path(arm, A, idx))
    tr = z['triples'].astype(np.int64)
    ok = z['status'] == 0
    return tr[ok], dict(n=int(len(ok)), capped=int((~ok).sum()), gens=z['gens'], narr=z['narr'])


def sparse_K(Kc):
    """Kc[ncp, NOUT, NOUT, NOUT] -> list of [interval, a, b, c, count] for nonzero entries."""
    nz = np.argwhere(Kc > 0)
    return [[int(i), int(a), int(b), int(c), int(Kc[i, a, b, c])] for i, a, b, c in nz]


def run_chain(arm, triples, comp, cps_per_island, seed, track_K=False, dump_at=None, dump_n=4000, quiet=True):
    """Pool Monte Carlo of the jump chain on `triples` (I, 3), components of `comp` islands, checkpoints in events per
    island (ascending).  Returns dict(hist, first_loss, drift, Kc, dumps, wall)."""
    pool = np.ascontiguousarray(triples.copy())
    I = len(pool)
    ncp = len(cps_per_island)
    hist = np.zeros((ncp, MI.NOUT), np.int64)
    drift = np.zeros((ncp, MI.NOUT, 3), np.int64)
    Kc = np.zeros((ncp, MI.NOUT, MI.NOUT, MI.NOUT), np.int64) if track_K else None
    first = np.full(3, -1, np.int64)
    fids = np.array(MI.V, np.int64)
    dumps = {}
    prev = 0
    t0 = time.time()
    rseed = seed
    # the state at event 0
    h0 = np.zeros(MI.NOUT, np.int64)
    ctx = arm.ctx()
    for i in range(I):
        h0[MI.VEC[int(MI.jl(ctx, *map(np.int64, pool[i])))]] += 1
    for k, c in enumerate(cps_per_island):
        tgt = int(c) * I
        todo = tgt - prev
        while todo > 0:
            piece = min(PIECE, todo)
            arm.maybe_flush(0.5)
            h = np.zeros((1, MI.NOUT), np.int64)
            Kp = np.zeros((1, MI.NOUT, MI.NOUT, MI.NOUT), np.int64) if track_K else np.zeros((1, 1, 1, 1), np.int64)
            dr = np.zeros((1, MI.NOUT, 3), np.int64)
            fl = np.zeros(3, np.int64)
            rseed = (rseed * 1103515245 + 12345) % (2 ** 31)
            MI.chain_run(arm.ctx(), MI.PAY, MI.VEC, MI.EXCL, pool, comp, piece, np.array([piece], np.int64), rseed, MI.N0, MI.W,
                         h, track_K, Kp, dr, fl, fids)
            hist[k] = h[0]
            drift[k] += dr[0]
            if track_K:
                Kc[k] += Kp[0]
            for q in range(3):
                if first[q] < 0 and fl[q] >= 0:
                    first[q] = (prev + (0 if fl[q] == 0 else fl[q]))
            prev += piece
            todo -= piece
        if dump_at and c in dump_at:
            dumps[int(c)] = pool[:dump_n].copy()
        if not quiet:
            print('  checkpoint %s: %.0f s' % (c, time.time() - t0), flush=True)
    return dict(hist=hist, h0=h0, first_loss=first, drift=drift, Kc=Kc, dumps=dumps, wall=time.time() - t0, I=I)


def summarize_hist(h):
    """class shares of an outcome histogram (NOUT,): dict of fractions."""
    n = h.sum()
    f = h / max(n, 1)
    cat = MI.CATMAP
    d = dict(n=int(n), Vstar=float(f[MI.V].sum()), eff=float(sum(f[k] for k in range(MI.NOUT) if MI.TOT[k] > 0.999)),
             meanTOT=float((f * MI.TOT).sum()))
    for c in range(5):
        d[MI.CATLAB[c]] = float(f[cat == c].sum())
    for i, v in enumerate(MI.V):
        d['F%d' % i] = float(f[v])
    return d


def chain_job(arm_name, A, idx, cap=None):
    arm = MI.Arm(arm_name); arm.new_cache(26)
    tr, info = load_pool(arm_name, A, idx)
    cps = list(CHECKPOINTS) + list(EXT)
    if cap is not None:
        cps = [c for c in cps if c <= cap]
    seed = crc('mi-chain|%s|%d|%d' % (arm_name, A, idx))
    r = run_chain(arm, tr, len(tr), cps, seed, track_K=True, dump_at=(10, 100, 1000) if idx == 0 else None, quiet=False)
    out = dict(arm=arm_name, A=A, idx=idx, I=r['I'], capped=info['capped'], cps=cps, wall=r['wall'],
               first_loss=r['first_loss'].tolist(), h0=r['h0'].tolist(), hist=r['hist'].tolist(),
               drift=r['drift'].tolist(), pathK=sparse_K(r['Kc']))
    out['summary0'] = summarize_hist(r['h0'])
    out['summary'] = [summarize_hist(r['hist'][k]) for k in range(len(cps))]
    with open(os.path.join(OUT, 'chain_%s_A%d_p%d.json' % (arm_name, A, idx)), 'w') as f:
        json.dump(out, f)
    if r['dumps']:
        np.savez_compressed(os.path.join(OUT, 'dump_%s_A%d.npz' % (arm_name, A)), **{('t%d' % k): v for k, v in r['dumps'].items()})
    print(json.dumps(dict(arm=arm_name, A=A, idx=idx, wall=r['wall'], final=out['summary'][-1])))
    return out


def union_job(arm_name, A, npools=4, cap=1000):
    """the 65,536-island pool = pools 0..npools-1 concatenated, to `cap` events per island; plus the 4,096-island
    pool (first quarter of pool 0)."""
    arm = MI.Arm(arm_name); arm.new_cache(26)
    cps = [c for c in CHECKPOINTS if c <= cap]
    out = {}
    trs = [load_pool(arm_name, A, k)[0] for k in range(npools)]
    big = np.concatenate(trs)
    for label, tr in (('I%d' % len(big), big), ('I4096', trs[0][:4096])):
        r = run_chain(arm, tr, len(tr), cps, crc('mi-union|%s|%d|%s' % (arm_name, A, label)))
        out[label] = dict(I=len(tr), cps=cps, hist=r['hist'].tolist(), h0=r['h0'].tolist(), wall=r['wall'],
                          summary0=summarize_hist(r['h0']), summary=[summarize_hist(r['hist'][k]) for k in range(len(cps))])
    with open(os.path.join(OUT, 'union_%s_A%d.json' % (arm_name, A)), 'w') as f:
        json.dump(out, f)
    print(json.dumps({k: v['summary'][-1] for k, v in out.items()}))
    return out


IA_I = (16, 64, 256, 1024, 4096)
IA_RUNS = 10


def ia_caps(I):
    return 100000 if I <= 1024 else 10000


def ia_job(arm_name, A, npools=5):
    """(2a): archipelagos of I islands, 10 runs per I, run r using the disjoint block of 4,096 islands r of the master list
    (the first I of the block: supersets, paired by construction)."""
    arm = MI.Arm(arm_name); arm.new_cache(24)
    master = np.concatenate([load_pool(arm_name, A, k)[0] for k in range(npools)])
    assert len(master) >= IA_RUNS * 4096, len(master)
    res = []
    for I in IA_I:
        cps = [c for c in list(CHECKPOINTS) + list(EXT) if c <= ia_caps(I)]
        for r in range(IA_RUNS):
            tr = master[r * 4096: r * 4096 + I]
            o = run_chain(arm, tr, I, cps, crc('mi-ia|%s|%d|%d|%d' % (arm_name, A, I, r)))
            res.append(dict(I=I, run=r, cps=cps, hist=o['hist'].tolist(), h0=o['h0'].tolist(), first_loss=o['first_loss'].tolist(),
                            wall=o['wall']))
        print('ia %s A%d I=%d done' % (arm_name, A, I), flush=True)
    with open(os.path.join(OUT, 'ia_%s_A%d.json' % (arm_name, A)), 'w') as f:
        json.dump(res, f)
    return res


COMP_C = (1, 4, 16, 64)


def comp_job(arm_name, A, npools=5):
    """(1): the same 1,024 islands (a block of the master list) connected as C disconnected components of 1,024/C islands;
    10 runs (blocks), paired by construction across C."""
    arm = MI.Arm(arm_name); arm.new_cache(24)
    master = np.concatenate([load_pool(arm_name, A, k)[0] for k in range(npools)])
    I = 1024
    res = []
    cps = [c for c in list(CHECKPOINTS) + list(EXT) if c <= 10000]
    for C in COMP_C:
        for r in range(IA_RUNS):
            tr = master[r * 1024: (r + 1) * 1024]
            o = run_chain(arm, tr, I // C, cps, crc('mi-comp|%s|%d|%d|%d' % (arm_name, A, C, r)))
            res.append(dict(C=C, run=r, cps=cps, hist=o['hist'].tolist(), h0=o['h0'].tolist(), first_loss=o['first_loss'].tolist(),
                            wall=o['wall']))
        print('comp %s A%d C=%d done' % (arm_name, A, C), flush=True)
    with open(os.path.join(OUT, 'comp_%s_A%d.json' % (arm_name, A)), 'w') as f:
        json.dump(res, f)
    return res


# ====================================================================== validation
def validate():
    import pytest  # noqa: F401  (tests are run separately; this records the quantities)
    res = {}
    # --- cost
    t = time.time()
    costs = {}
    for name in ('L', 'M', 'R'):
        arm = MI.Arm(name); arm.new_cache(24)
        rng = np.random.default_rng(1)
        MI.build_island(arm, rng, 1, 0)                     # compile / warm
        for A in (0, 150):
            t0 = time.time(); n = 40
            gens = []; narr = []
            for k in range(n):
                r = MI.build_island(arm, rng, 100 + k, A)
                gens.append(r['gen']); narr.append(r['narr'])
                assert r['status'] == 0
            costs['%s_A%d_island_s' % (name, A)] = (time.time() - t0) / n
            costs['%s_A%d_mean_gen' % (name, A)] = float(np.mean(gens))
    res['cost'] = costs
    # --- founding reproduces the stored cells (fair share at generation 2,000)
    found = {}
    for name, stored in (('L', 0.281), ('M', 0.283)):
        arm = MI.Arm(name); arm.new_cache(24)
        n = 2560; nf = 0; mixed = 0
        cls = np.zeros(MI.NOUT + 2, np.int64)
        for k in range(n):
            rf = np.random.default_rng(crc('mi-val-found|%d' % k))        # the same founders for L and M
            init = np.stack([rf.multinomial(MI.N0, arm.laws[s]) for s in range(3)]).astype(np.int64)
            if k % 128 == 0:
                arm.maybe_flush(0.45)
            st, g, counts, na = MI.island_run(arm.ctx(), arm.lc(32), MI.PAY, init, MI.N0, MI.W, 40000 + k, 2000,
                                              np.empty(0), arm.cum, True)
            c, e = MI.classify_counts(arm, counts)
            cls[c] += 1
        fair = int(sum(cls[v] for v in MI.V))
        lo, hi = wilson(fair, n)
        found[name] = dict(n=n, fair=fair / n, ci=[lo, hi], stored=stored, by_class={MI.OLAB[k] if k < MI.NOUT else ('member-mixed' if k == MI.NOUT else 'other'): int(cls[k]) for k in range(MI.NOUT + 2) if cls[k]})
    res['founding_vs_stored'] = found
    # --- formula vs simulation for three event types (simulated relaxation of the stored kernel)
    arm = MI.Arm('L'); arm.new_cache(22)
    ci = SS.const_index(arm.S.fs)

    def cst(s, partner, d):
        return ci[MI.D.local_of(s, partner, d)]
    cases = {
        'selected +1/6 (wasteful (2,2,0), slot 0 asks 1/2)': ((cst(0, 1, 0), cst(1, 0, 0), cst(2, 0, 1)), 0, cst(0, 1, 1), 1500),
        'selected +2/6 (wasteful, slot 0 asks 2/3)': ((cst(0, 1, 0), cst(1, 0, 0), cst(2, 0, 1)), 0, cst(0, 1, 2), 800),
        'neutral (fair pair, excluded slot)': ((cst(0, 1, 1), cst(1, 0, 1), cst(2, 0, 2)), 2, cst(2, 1, 0), 3000),
        'deleterious -2/6 (fair pair, pivot asks 2/3)': ((cst(0, 1, 1), cst(1, 0, 1), cst(2, 0, 2)), 0, cst(0, 1, 2), 400),
    }
    ev = {}
    for name, (tr, s, x, n) in cases.items():
        p, _ = MI.event_prob(arm, tr, s, x)
        fixed = 0
        for k in range(n):
            init = np.zeros((3, arm.K), np.int64)
            for t_ in range(3):
                init[t_, tr[t_]] = MI.N0
            init[s, tr[s]] -= 1; init[s, x] += 1
            st, g, counts, na = MI.island_run(arm.ctx(), arm.lc(32), MI.PAY, init, MI.N0, MI.W, 70000 + k, 8000, np.empty(0),
                                              arm.cum, True)
            assert st == 0
            fixed += MI.triple_of(counts)[s] == x
        lo, hi = wilson(fixed, n)
        ev[name] = dict(n=n, simulated=fixed / n, ci=[lo, hi], formula=p, inside=bool(lo <= p <= hi))
    res['event_formula'] = ev
    # --- evaluator codes are valid on random triples
    mincode = {}
    for name in ('L', 'M', 'R'):
        arm = MI.Arm(name); arm.new_cache(22)
        rng = np.random.default_rng(3)
        ctx = arm.ctx()
        lo_ = 10 ** 9
        for _ in range(20000):
            tr = [int(rng.choice(arm.K, p=arm.laws[s])) for s in range(3)]
            lo_ = min(lo_, int(MI.jl(ctx, *map(np.int64, tr))))
        mincode[name] = lo_
    res['min_joint_code'] = mincode
    res['wall'] = time.time() - t
    res['rss_gb'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
    with open(os.path.join(ROOT, 'runs', 'many-islands-validate.json'), 'w') as f:
        json.dump(res, f, indent=1)
    return res


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'validate':
        r = validate()
        print(json.dumps(r, indent=1))
    elif cmd == 'pool':
        arm, A, idx = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
        n = int(sys.argv[5]) if len(sys.argv) > 5 else 16384
        r = build_pool(arm, A, idx, n, log=sys.stdout)
        with open(os.path.join(OUT, 'pool_%s_A%d_p%d.json' % (arm, A, idx)), 'w') as f:
            json.dump(r, f)
        print(r)
    elif cmd == 'chain':
        arm, A, idx = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
        cap = int(sys.argv[5]) if len(sys.argv) > 5 else None
        chain_job(arm, A, idx, cap)
    elif cmd == 'union':
        union_job(sys.argv[2], int(sys.argv[3]), cap=int(sys.argv[4]) if len(sys.argv) > 4 else 1000)
    elif cmd == 'ia':
        ia_job(sys.argv[2], int(sys.argv[3]))
    elif cmd == 'comp':
        comp_job(sys.argv[2], int(sys.argv[3]))
