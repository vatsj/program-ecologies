"""Driver for the inspection-shadow experiment (spec specs/2026-10-24-inspection-shadow.md; notes notes/inspection-shadow.md;
predictions predictions/2026-10-24-inspection-shadow.md).  One job per process.

    python3 src/inspection_shadow_run.py static
    python3 src/inspection_shadow_run.py chain ARM C N [--variant base|boost|control] [--no-passage]
    python3 src/inspection_shadow_run.py lottery NAME [--runs a b]       # NAME = ARM-cC-SIZE-REMEDY, e.g. exact-c0-n400i16-rainK
    python3 src/inspection_shadow_run.py direct ARM C N BASE NINJ KARR   # BASE in CRI | N, KARR in 0 | 1

SIZE in n100i64 | n400i16 | n800i8 | n400i64; REMEDY in base | rainK | rainC | boost | boostctl | mN0 | mN10.
Every chain file is an eps -> 0 object (whole state space); every lottery file an eps = 0 finite-(N, I, horizon) statistic
(with the declared rain where a remedy has one).  Outputs under runs/inspection_shadow/ (small json / json.gz only).
"""
import argparse, os, sys, time, resource
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"                    # one core per job: must precede the first numpy import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import inspection_shadow as S
import mixed2 as M

OUT = os.environ.get('INSPECTION_SHADOW_OUT', os.path.join(S.ROOT, 'runs', 'inspection_shadow'))
os.makedirs(OUT, exist_ok=True)

SIZES = {
    'n100i64': dict(N=100, I=64, runs=40, T=2000, found='primary'),
    'n400i16': dict(N=400, I=16, runs=20, T=8000, found='size'),
    'n800i8': dict(N=800, I=8, runs=20, T=16000, found='n800i8'),
    'n400i64': dict(N=400, I=64, runs=20, T=8000, found='n400i64'),
}
REMEDIES = ('base', 'rainK', 'rainC', 'boost', 'boostctl', 'mN0', 'mN10')
RAIN_EPS_N = 0.05                # eps N: mutants per generation per island


def parse_lottery(name):
    arm, cs, size, rem = name.split('-')
    c = float(cs[1:])
    z = SIZES[size]
    kw = dict(arm=arm, c=c, N=z['N'], I=z['I'], runs=z['runs'], T=z['T'], mN=1.0, found=z['found'], dyn=z['found'], tag=name)
    if rem == 'base':
        pass
    elif rem in ('rainK', 'rainC'):
        kw['rain'] = (rem[-1], RAIN_EPS_N)
    elif rem == 'boost':
        kw['variant'] = 'boost'
    elif rem == 'boostctl':
        kw['variant'] = 'control'
    elif rem == 'mN0':
        kw['mN'] = 0.0
    elif rem == 'mN10':
        kw['mN'] = 10.0
    else:
        raise ValueError(rem)
    return S.LotCell(**kw)


def cmd_chain(a):
    res = S.chain_cell(a.arm, a.c, a.N, variant=a.variant, passage=not a.no_passage, dtype=np.float32 if a.f32 else np.float64)
    res['rss_peak_gb'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
    S.jdump(res, os.path.join(OUT, 'chain_%s_c%g_%s_N%d.json' % (a.arm, a.c, a.variant, a.N)))
    print('wrote chain_%s_c%g_%s_N%d.json (peak RSS %.1f GB)' % (a.arm, a.c, a.variant, a.N, res['rss_peak_gb']), flush=True)


def cmd_lottery(a):
    spec = parse_lottery(a.name)
    runs = list(range(a.runs[0], a.runs[1])) if a.runs else None
    t0 = time.time()
    res = S.run_lottery(spec, runs)
    tag = a.name + ('_r%d-%d' % tuple(a.runs) if a.runs else '')
    S.jdump(dict(name=a.name, arm=spec.arm, c=spec.c, N=spec.N, I=spec.I, T=spec.T, mN=spec.mN, rain=spec.rain, variant=spec.variant,
                 object='eps = 0 seed lottery (finite N, I, horizon)', runs=res, time_s=time.time() - t0), os.path.join(OUT, 'lot_%s.json.gz' % tag), gz=True)
    print('wrote lot_%s.json.gz (%.0fs, peak RSS %.2f GB)' % (tag, time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9), flush=True)


def cmd_direct(a):
    res = S.run_direct(a.arm, a.c, a.N, a.base, a.ninj, bool(a.karr))
    S.jdump(res, os.path.join(OUT, 'direct_%s_c%g_N%d_%s_inj%d_K%d.json' % (a.arm, a.c, a.N, a.base, a.ninj, a.karr)))
    print('wrote direct_%s_c%g_N%d_%s_inj%d_K%d.json' % (a.arm, a.c, a.N, a.base, a.ninj, a.karr), flush=True)


def cmd_static(a):
    """static numbers: set sizes, twin relation, prudent classes, boosted priors, the one-state calculations of notes section 1,
    and the equality of lottery3 with mixed2.lottery2 when no rain or arrival is used."""
    out = {}
    for c in (0.0, 0.01):
        A = S.get_arm('exact', c)
        fl = S.class_flags(A)
        sets = S.pair_sets(A, fl)
        nm = S.named(A)
        N_, CRI, C_, K_ = nm['0N'], nm['0CRI'], nm['1C'], nm['1K']
        tw = np.nonzero(np.abs(A.UA[:, C_] - A.UA[CRI, C_]) < 1e-9)[0] if c == 0 else np.nonzero(np.abs(A.UA[:, C_]) < 1e-9)[0]
        d = dict(K=A.K, sizes={k: int(v.sum()) for k, v in sets.items()},
                 twin=dict(n_classes=len(tw), mass=float(A.mass[0][tw].sum()), mass_N=float(A.mass[0][N_]),
                           mass_deterring=float(A.mass[0][tw][fl['deter0'][tw]].sum()), mass_nondeterring_other=float(A.mass[0][tw][~fl['deter0'][tw]].sum() - A.mass[0][N_]),
                           u_CRI_C=[float(A.UA[CRI, C_]), float(A.UB[C_, CRI])], u_N_C=[float(A.UA[N_, C_]), float(A.UB[C_, N_])],
                           cost_CRI_vs_C=float(A.CA[CRI, C_]), cost_N_vs_C=float(A.CA[N_, C_])),
                 priors={})
        S_ = S.prudent_classes(A)
        d['prudent'] = [dict(cls=A.names[1][b], size=int(A.sizes[1][b]), members=len(A.members[1][b]), mass=float(A.mass[1][b]),
                             cost_vs_CRI=float(A.CB[b, CRI]), cost_vs_N=float(A.CB[b, N_]), u_vs_CRI=float(A.UB[b, CRI]), u_vs_N=float(A.UB[b, N_])) for b in S_]
        for kind in ('boost', 'control'):
            mass, fac, info = S.mass_variant(A, kind)
            d['priors'][kind] = info
        if c == 0.0:
            for N in (100, 1000, 10000, 100000):
                d.setdefault('reference_exits', {})[str(N)] = {
                    '(CRI,C)': S.reference_exits(A, N, CRI, C_), '(N,C)': S.reference_exits(A, N, N_, C_), '(N,K)': S.reference_exits(A, N, N_, K_)}
        else:
            for N in (100, 1000, 10000, 100000):
                d.setdefault('reference_exits', {})[str(N)] = {'(CRI,C)': S.reference_exits(A, N, CRI, C_)}
        out['exact_c%g' % c] = d
    # lottery3 == lottery2 without rain and arrivals
    A = S.get_arm('exact', 0.0)
    spec = parse_lottery('exact-c0-n100i64-base')
    lang = A.lang; K0, K1 = A.K
    f0 = M.draw_founders(lang, 0, A.cls_of[0], K0, 8, 100, 11); f1 = M.draw_founders(lang, 1, A.cls_of[1], K1, 8, 100, 12)
    i0 = np.nonzero(f0.sum(0) > 0)[0]; i1 = np.nonzero(f1.sum(0) > 0)[0]
    UA = np.ascontiguousarray(A.UA[np.ix_(i0, i1)]); UB = np.ascontiguousarray(A.UB[np.ix_(i1, i0)])
    z = np.zeros(0, np.int64)
    cps = np.array([10, 40], np.int64)
    a0, a1 = M.lottery2(UA, UB, np.ascontiguousarray(f0[:, i0]), np.ascontiguousarray(f1[:, i1]), 100, M.W, 0.01, 5, cps)
    b0, b1 = S.lottery3(UA, UB, np.ascontiguousarray(f0[:, i0]), np.ascontiguousarray(f1[:, i1]), 100, M.W, 0.01, 5, cps, 0.0, 1, -1, z, z, z, z)
    out['lottery3_equals_lottery2'] = bool((a0 == b0).all() and (a1 == b1).all())
    # weighted founders with factor 1 equal the unweighted draw
    g1 = S.draw_founders_w(lang, 1, A.cls_of[1], K1, 8, 100, 12, np.ones(K1))
    out['founders_factor1_equal'] = bool((g1 == f1).all())
    S.jdump(out, os.path.join(OUT, 'static.json'))
    print('wrote static.json; lottery3==lottery2: %s; founders(factor 1)==unweighted: %s' % (out['lottery3_equals_lottery2'], out['founders_factor1_equal']), flush=True)


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    s = sp.add_parser('static'); s.set_defaults(f=cmd_static)
    s = sp.add_parser('chain'); s.add_argument('arm'); s.add_argument('c', type=float); s.add_argument('N', type=int)
    s.add_argument('--variant', default='base', choices=['base', 'boost', 'control', 'noshadow', 'nolight', 'neither']); s.add_argument('--no-passage', action='store_true'); s.add_argument('--f32', action='store_true'); s.set_defaults(f=cmd_chain)
    s = sp.add_parser('lottery'); s.add_argument('name'); s.add_argument('--runs', type=int, nargs=2); s.set_defaults(f=cmd_lottery)
    s = sp.add_parser('direct'); s.add_argument('arm'); s.add_argument('c', type=float); s.add_argument('N', type=int)
    s.add_argument('base', choices=['CRI', 'N']); s.add_argument('ninj', type=int); s.add_argument('karr', type=int); s.set_defaults(f=cmd_direct)
    a = ap.parse_args()
    a.f(a)


if __name__ == '__main__':
    main()
