"""Driver for the zero-tolerance experiment (spec specs/2026-10-24-zero-tolerance.md; notes notes/zero-tolerance.md; predictions
predictions/2026-10-24-zero-tolerance.md).  One job per process.

    python3 src/zero_tolerance_run.py static
    python3 src/zero_tolerance_run.py validate                  # arm v0 against the stored chain and lottery (stops the run on failure)
    python3 src/zero_tolerance_run.py chain ARM C N [--f32]     # ARM in ctl zt sus ztsus sr1 sr4 sr16 unc v0, optionally ARM@D11
    python3 src/zero_tolerance_run.py lottery ARM C SIZE        # SIZE in n100i64 | n400i64

Every chain file is an eps -> 0 object (whole state space); every lottery file an eps = 0 finite-(N, I, horizon) statistic.
Outputs under runs/zero_tolerance/ (small json / json.gz only).
"""
import argparse, os, sys, time, resource
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"                    # one core per job: must precede the first numpy import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import mixed2 as M
import inspection_shadow as S
import zero_tolerance as Z

OUT = os.environ.get('ZERO_TOLERANCE_OUT', os.path.join(Z.ROOT, 'runs', 'zero_tolerance'))
os.makedirs(OUT, exist_ok=True)
STORED = os.path.join(Z.ROOT, 'runs', 'inspection_shadow')

SIZES = {
    'n100i64': dict(N=100, I=64, runs=40, T=2000, found='primary'),
    'n400i64': dict(N=400, I=64, runs=20, T=8000, found='n400i64'),
}


def cmd_static(a):
    """static numbers per arm and price: class counts, the added programs' classes and masses, set sizes, the strict invaders of the
    resident (arm inspector, C), and the equality of the validation arm with the stored table."""
    out = {}
    for c in (0.0, 0.01):
        A0 = M.get_arm(Z.GAME, 'exact', Z.NMAX, c)
        for tag in ('v0', 'ctl', 'unc', 'zt', 'sus', 'ztsus', 'sr1', 'sr4', 'sr16', 'sr4s', 'sr16s'):
            A = Z.get_arm_zt(tag, c)
            fl = S.class_flags(A)
            sets = S.pair_sets(A, fl)
            nm = S.named(A)
            d = Z.class_summary(A)
            d['sets'] = {k: int(v.sum()) for k, v in sets.items()}
            d['n_inspector_classes_new'] = A.K[0] - A0.K[0]
            d['n_inspectee_classes_new'] = A.K[1] - A0.K[1]
            d['mass_added_total'] = A.zt['m']
            C_ = nm['1C']
            res = {}
            for lab, a_ in [('CRI', nm['0CRI']), ('N', nm['0N'])] + [(x['name'], x['cls']) for x in A.zt['added']]:
                inv = np.nonzero(A.UB[:, a_] - A.UB[C_, a_] > 1e-9)[0]
                res[lab] = dict(n_strict_invaders=int(len(inv)), mass=float(A.mass[1][inv].sum()),
                                nonreading_mass=float(A.mass[1][[b for b in inv if not A.reader[1][b]]].sum()),
                                reading_mass=float(A.mass[1][[b for b in inv if A.reader[1][b]]].sum()),
                                reading=[(A.names[1][b], float(A.mass[1][b]), float(A.UB[b, a_] - A.UB[C_, a_])) for b in inv if A.reader[1][b]])
            d['strict_invaders_of_(a,C)'] = res
            if tag == 'v0':
                d['equals_stored'] = dict(K=A.K == A0.K, UA=float(np.abs(A.UA - A0.UA).max()), UB=float(np.abs(A.UB - A0.UB).max()),
                                          mass=float(max(np.abs(A.mass[0] - A0.mass[0]).max(), np.abs(A.mass[1] - A0.mass[1]).max())))
            out['%s_c%g' % (tag, c)] = d
    S.jdump(out, os.path.join(OUT, 'static.json'))
    print('wrote static.json')


def cmd_validate(a):
    """arm v0 (nothing added, no mass moved) against the stored runs: table equality, chain at N = 10^3 and 10^4 (float32 as stored) and the
    lottery runs 0-2 at (100, 64) bit for bit at generation 2,000 (predictions file: validation tolerance)."""
    res = dict()
    A0 = M.get_arm(Z.GAME, 'exact', Z.NMAX, 0.0)
    V = Z.get_arm_zt('v0', 0.0)
    res['table_max_abs_diff'] = float(max(np.abs(V.UA - A0.UA).max(), np.abs(V.UB - A0.UB).max(), np.abs(V.CA - A0.CA).max()))
    ok = res['table_max_abs_diff'] == 0.0 and V.K == A0.K
    for N, tol in ((1000, 1e-6), (10000, 1e-6)):
        stored = S.jload(os.path.join(STORED, 'chain_exact_c0_base_N%d.json' % N))
        new = Z.chain_cell_zt('v0', 0.0, N, passage=False, dtype=np.float32, verbose=True)
        d = abs(new['pi_sets']['E'] - stored['pi_sets']['E']) / stored['pi_sets']['E']
        res['chain_N%d' % N] = dict(pi_E_new=new['pi_sets']['E'], pi_E_stored=stored['pi_sets']['E'], rel_diff=d, u0g_new=new['stat']['u0g'], u0g_stored=stored['stat']['u0g'])
        ok = ok and d < tol
    lot = S.jload(os.path.join(STORED, 'lot_exact-c0-n100i64-base.json.gz'))
    new = Z.run_lottery_zt('v0', 0.0, 100, 64, 3, 2000, found='primary', verbose=False)
    diffs = []
    for r in range(3):
        for k in ('isl_efficient', 'u0g', 'u1g', 'p_insp', 'q_cheat'):
            diffs.append(abs(new[r]['stats']['2000'][k] - lot['runs'][r]['stats']['2000'][k]))
    res['lottery_max_abs_diff_runs0-2'] = float(max(diffs))
    ok = ok and max(diffs) < 1e-12
    res['passed'] = bool(ok)
    S.jdump(res, os.path.join(OUT, 'validate.json'))
    print('validation', 'PASSED' if ok else 'FAILED', res, flush=True)
    if not ok:
        sys.exit(1)


def cmd_chain(a):
    res = Z.chain_cell_zt(a.arm, a.c, a.N, passage=not a.no_passage, dtype=np.float32 if a.f32 else np.float64)
    res['rss_peak_gb'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
    fn = 'chain_%s_c%g_N%d.json' % (a.arm.replace('@', '_'), a.c, a.N)
    S.jdump(res, os.path.join(OUT, fn))
    print('wrote %s (peak RSS %.1f GB)' % (fn, res['rss_peak_gb']), flush=True)


def cmd_lottery(a):
    z = SIZES[a.size]
    t0 = time.time()
    runs = list(range(a.runs[0], a.runs[1])) if a.runs else None
    res = Z.run_lottery_zt(a.arm, a.c, z['N'], z['I'], z['runs'], z['T'], found=z['found'], run_ids=runs)
    A = Z.get_arm_zt(a.arm, a.c)
    tag = '%s_c%g_%s' % (a.arm.replace('@', '_'), a.c, a.size) + ('_r%d-%d' % tuple(a.runs) if a.runs else '')
    S.jdump(dict(arm=a.arm, c=a.c, N=z['N'], I=z['I'], T=z['T'], mN=1.0, added=A.zt, object='eps = 0 seed lottery (finite N, I, horizon)', runs=res, time_s=time.time() - t0),
            os.path.join(OUT, 'lot_%s.json.gz' % tag), gz=True)
    print('wrote lot_%s.json.gz (%.0fs, peak RSS %.2f GB)' % (tag, time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9), flush=True)


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    s = sp.add_parser('static'); s.set_defaults(f=cmd_static)
    s = sp.add_parser('validate'); s.set_defaults(f=cmd_validate)
    s = sp.add_parser('chain'); s.add_argument('arm'); s.add_argument('c', type=float); s.add_argument('N', type=int)
    s.add_argument('--no-passage', action='store_true'); s.add_argument('--f32', action='store_true'); s.set_defaults(f=cmd_chain)
    s = sp.add_parser('lottery'); s.add_argument('arm'); s.add_argument('c', type=float); s.add_argument('size', choices=sorted(SIZES))
    s.add_argument('--runs', type=int, nargs=2); s.set_defaults(f=cmd_lottery)
    a = ap.parse_args()
    a.f(a)


if __name__ == '__main__':
    main()
