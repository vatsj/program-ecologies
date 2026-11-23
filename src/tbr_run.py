"""Queue 81 driver, arms T and M: regenerate published worlds with saved compositions, then measure tiers.

    python3 src/tbr_run.py one ARM N R LAM MN [--out DIR]      # one run-cell -> DIR/<ARM>_<N>_<R>_<LAM>_<MN>.json.gz
    python3 src/tbr_run.py pool JOBFILE [--procs 3] [--out DIR]   # job lines "ARM N R LAM MN"
    python3 src/tbr_run.py jobs STAGE OUT                        # STAGE in s1, s2

Each run-cell uses majority_tail.prepare(arm, 'main', N, r) (published founders and tail schedule; Lmax = 100, or
1,000 for the Lambda = 1,000 cell, which therefore has its own arrival stream), runs src/tbr_kern.kern_tbr to H = 120 N
with snapshots at 30N, 60N, 90N and 120N, and checks the V* share series (every N generations, modal outcome) against
the stored row of queue 74 where one exists (Lambda in {0, 10, 100}, mN in {0, 0.1, 1}); a mismatch is recorded and the
run-cell is flagged (repro = false).
"""
import argparse, gzip, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTD = os.path.join(ROOT, 'runs', 'tbr_rows', 'tm')
STORED = os.path.join(ROOT, 'runs', 'majority_tail', 'rows')
_A = {}


def arm_obj(arm):
    import tbr
    if arm not in _A:
        _A[arm] = tbr.Tri(arm)
    return _A[arm]


def stored_series(arm, N, r, lam, mN):
    p = os.path.join(STORED, '%s_main_%d_%d.jsonl.gz' % (arm, N, r))
    if not os.path.exists(p):
        return None
    for l in gzip.open(p, 'rt'):
        rec = json.loads(l)
        if rec['lam'] == lam and abs(rec['mN'] - mN) < 1e-12:
            return rec
    return None


def to_glob(arr, U, K, fill=0):
    I = arr.shape[0]
    G = np.full((I, 3, K), fill, arr.dtype)
    for s in range(3):
        G[:, s, U[s]] = arr[:, s, :len(U[s])]
    return G


def run_cell(arm, N, r, lam, mN, outdir=OUTD):
    import majority_tail as MT
    import tbr_kern as TK
    import tbr
    path = os.path.join(outdir, '%s_%d_%d_%g_%g.json.gz' % (arm, N, r, lam, mN))
    if os.path.exists(path):
        return path
    t0 = time.time()
    Lmax = 1000.0 if lam > 100 else 100.0
    prep = MT.prepare(arm, 'main', N, r, Lmax=Lmax)
    H = 120 * N
    snapg = np.array([30 * N, 60 * N, 90 * N, 120 * N], np.int64)
    ag, ai, asl, au, lk = MT.local_arrivals(prep, lam)
    o = TK.kern_tbr(prep['J'], prep['PAY'], prep['VEC'], prep['ISMEM'], prep['TOT'], prep['loc'], N, MT.W, mN / N,
                    prep['seed'], H, 10, snapg, ag, ai, asl, au, lk, 400000, 400000)
    (status, stop, counts, modal, majo, snapc, snapd, xlog, nx, alog, na, nmig, lastnew, intro, arrf, t10) = o
    t_kern = time.time() - t0
    # reproduction check against queue 74's stored row
    vs = [round(float(MT.ISFAIR[modal[g]].mean()), 4) for g in range(0, H + 1, N)]
    st = stored_series(arm, N, r, lam, mN) if Lmax == 100.0 else None
    repro = None
    if st is not None:
        repro = bool(st['vshare_ts'][:len(vs)] == vs) and int(st['nmig']) == int(nmig) if not st.get('long') else \
            bool(st['vshare_ts'][:len(vs)] == vs)
    A = arm_obj(arm)
    K = A.K
    U = prep['U']
    tail = [np.asarray(prep['tail_laws'][s][:K], float) for s in range(3)]
    tail = [t / t.sum() for t in tail]
    founders = prep['init'][:, :, :K].sum(0)
    Gs = [to_glob(snapc[k], U, K) for k in range(4)]
    lastg = to_glob(lastnew, U, K, fill=-1)
    t10g = to_glob(t10, U, K, fill=-1)
    rec = dict(arm=arm, N=N, run=r, lam=lam, mN=mN, Lmax=Lmax, status=int(status), stop=int(stop), nmig=int(nmig),
               n_arr=int(len(ag)), arr_late=float((ag > 60 * N).mean()) if len(ag) else None,
               arr_after_gend=float((ag > 100 * N).mean()) if len(ag) else None,
               vstar120=vs[-1], repro=repro, t_kern=round(t_kern, 1))
    snaps = {}
    maj4 = []
    for k, frac in enumerate((25, 50, 75, 100)):
        hz = frac == 100
        if frac == 75:
            maj4.append(Gs[k].argmax(2)); continue
        w, cases, cache = tbr.analyze(A, Gs[k], N, mN, founders, tail, lastnew=lastg if hz else None,
                                      t10g=t10g if hz else None, prior=hz, comp=hz, examples=hz)
        maj4.append(Gs[k].argmax(2))
        if not hz:
            cases = [{x: c[x] for x in ('i', 'j', 'p', 'set08', 'set095', 'natpos', 'vacE', 'vacA', 'vacT', 'regA',
                                        'regT', 'pmA', 'pmT', 'fdA', 'fdT')} for c in cases]
        snaps[str(frac)] = dict(world=w, cases=cases)
        if hz:
            hcache = cache; hcases = cases
    maj4 = [maj4[0], maj4[1], maj4[2], maj4[3]]
    # origin of each horizon holder's presence episode from the crossing log
    origin = {}
    for g, i, s, k, af, it in xlog:
        gk = int(U[s][k])
        origin[(int(i), int(s), gk)] = 'founder' if it == -1 else ('tail' if af == 1 else 'migrant')
    # crossings after 25% by origin (majority changes)
    late = [x for x in xlog if x[0] > 30 * N]
    rec['crossings_after25'] = dict(n=len(late), founder=int(sum(1 for x in late if x[5] == -1)),
                                    tail=int(sum(1 for x in late if x[4] == 1)),
                                    migrant=int(sum(1 for x in late if x[5] != -1 and x[4] != 1)))
    rec['routes'] = tbr.routes(A, maj4, hcases, hcache, origin)
    # founders present per slot (for the 1b / stage-3 supply)
    rec['snaps'] = snaps
    rec['founder_support'] = [np.nonzero(founders[s])[0].tolist() for s in range(3)]
    rec['wall'] = round(time.time() - t0, 1)
    os.makedirs(outdir, exist_ok=True)
    tmp = path + '.tmp'
    with gzip.open(tmp, 'wt') as f:
        json.dump(rec, f, default=_conv)
    os.replace(tmp, path)
    return path


def _conv(o):
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.floating): return float(o)
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return o.tolist()
    raise TypeError(type(o))


def make_jobs(stage):
    jobs = []
    if stage == 's1':
        for arm in ('T', 'M'):
            for N in (100, 200, 400):
                for r in range(20):
                    jobs.append((arm, N, r, 100, 1))
    elif stage == 's2':
        for arm in ('T', 'M'):
            for r in range(20):
                for mN in (0.1, 3, 10):
                    jobs.append((arm, 200, r, 100, mN))
                for lam in (0, 1000):
                    jobs.append((arm, 200, r, lam, 1))
    elif stage == 's3':
        pass
    jobs.sort(key=lambda j: (-j[1], j[0] != 'T'))
    return jobs


def _work(j):
    try:
        t = time.time()
        p = run_cell(*j)
        return '%s done %.0fs' % (j, time.time() - t)
    except Exception as e:
        import traceback
        return 'FAIL %s %r\n%s' % (j, e, traceback.format_exc())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['one', 'pool', 'jobs'])
    ap.add_argument('args', nargs='*')
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--out', default=OUTD)
    a = ap.parse_args()
    if a.cmd == 'one':
        arm, N, r, lam, mN = a.args
        print(run_cell(arm, int(N), int(r), float(lam) if '.' in lam else int(lam), float(mN) if '.' in mN else int(mN), a.out))
    elif a.cmd == 'jobs':
        jobs = make_jobs(a.args[0])
        open(a.args[1], 'w').write('\n'.join(' '.join(str(x) for x in j) for j in jobs) + '\n')
        print(len(jobs))
    else:
        from multiprocessing import Pool
        jobs = []
        for l in open(a.args[0]):
            if l.strip():
                x = l.split()
                jobs.append((x[0], int(x[1]), int(x[2]), int(float(x[3])) if float(x[3]).is_integer() else float(x[3]),
                             int(float(x[4])) if float(x[4]).is_integer() else float(x[4])))
        with Pool(a.procs) as pool:
            for msg in pool.imap_unordered(_work, jobs):
                print(msg, flush=True)


if __name__ == '__main__':
    main()
