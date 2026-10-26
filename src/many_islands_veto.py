"""Reference arm (extra, outside the registered predictions; RS-approved via the RE): the single-migrant conversion kernel of
fair-pair islands under the hand-written veto gV (nu = 0.1, menu F, public consent, beta = 1), measured with the stored
kernel `migration_window_kernels.fkern_mw` (imported, not edited) as configured by migration_window.run_comp for gV.

Islands: fair-pair islands of the stored L1 founders (64 islands per run), run to settlement without migration (H_SETTLE
generations).  Injection: one migrant program from a donor island on another fair pair into a random member slot, replacing a
random resident individual; the single island is relaxed for H_RELAX generations with contract proposals at nu.  Shams (a
resident copy replaces a resident, no change) estimate the veto's spontaneous flip rate.

    python3 src/many_islands_veto.py N RUNS NINJ       # -> runs/many_islands/veto_N<N>.json
"""
import os, sys, json, time, zlib, math
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stable_sets as SS
import farsighted_refusal as F
import farsighted_refusal_run as FR
import migration_window as MW
import migration_window_kernels as MK

T = MW.T
X = MW.X
V = list(MW.V)
NOUT = MW.NOUT
ROOT = SS.ROOT
OUT = os.path.join(ROOT, 'runs', 'many_islands')
H_SETTLE = 1500
H_RELAX = 1000
BASE = 'L1'


def wilson(k, n, z=1.96):
    if n == 0:
        return [float('nan'), float('nan')]
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [c - h, c + h]


def run_kern(st, ga, tc0, N, seed, H):
    res, modal, effm, fairm = MK.fkern_mw(st.J, T.PAY, T.VEC, T.ISMEM, T.TOT, tc0, st.TK, st.TO, st.TG, st.TPC, st.TMAP, st.ntypes,
                                          st.Kmax, st.NG, N, SS.W, 0.0, int(seed) % (2 ** 31), H, 10, np.zeros(0, np.int64),
                                          float(MW.NU), F.CS_, F.CD_, F.CACT_, F.CX, ga['GKIND'], ga['GTAB'], ga['KRTAB'],
                                          F.PROPM, F.UPAY, float(ga['rdelta']), False, 50, 1000, 100000)
    return res, modal


def settle(N, runs):
    """fair-pair islands after H_SETTLE generations without migration: list of dicts (state counts, setup, pair)."""
    ga = FR.guard_arrays(['g0', 'gV'])
    isl = []
    for r in range(runs):
        init, _ = MW.founders(BASE, r, 64, N)
        loc, U = SS.compress(init)
        st = F.Setup(loc, U, 2, assign=('bit', 1.0, 1), rng=None)
        seed = MW.comp_seed(BASE, r, 0, 64, True)
        res, modal = run_kern(st, ga, st.tc0, N, seed, H_SETTLE)
        tcount = res[2]
        for i in range(64):
            a = int(modal[H_SETTLE, i])
            if a in V and (modal[H_SETTLE - 100:H_SETTLE + 1, i] == a).all():
                isl.append(dict(run=r, i=i, pair=a, tc=tcount[i].copy(), st=st))
    return isl, ga


def donor_program(st, tcrow, s):
    t = int(np.argmax(tcrow[s]))
    return int(st.TK[s, t])


def inject(N, runs=6, ninj=2000, seed0=1):
    t0 = time.time()
    isl, ga = settle(N, runs)
    rng = np.random.default_rng(zlib.crc32(('veto|%d' % N).encode()))
    byp = {v: [x for x in isl if x['pair'] == v] for v in V}
    recs = []
    kinds = ['migrant'] * ninj + ['sham'] * ninj
    for n, kind in enumerate(kinds):
        a_isl = isl[int(rng.integers(len(isl)))]
        a = a_isl['pair']; st = a_isl['st']
        s = int(rng.choice([q for q in range(3) if X[a][q] > 0]))
        tc = a_isl['tc'].copy()
        pop = tc[s].astype(float)
        t_r = int(rng.choice(len(pop), p=pop / pop.sum()))
        donor_member = None; b = None
        if kind == 'migrant':
            others = [x for x in isl if x['pair'] != a and x['st'] is st]
            if not others:
                continue
            d = others[int(rng.integers(len(others)))]
            b = d['pair']
            k = donor_program(st, d['tc'], s)
            tm = st.tid(s, k, -1, 1)
            donor_member = bool(X[b][s] > 0)
            if tm == t_r:
                continue
            new_t = tm
        else:
            new_t = t_r
        # state with one resident individual of slot s replaced
        tcn = np.zeros((1, 3, st.Tcap), np.int64)
        tcn[0] = tc
        if kind == 'migrant':
            tcn[0, s, t_r] -= 1; tcn[0, s, new_t] += 1
        res, modal = run_kern(st, ga, tcn, N, 1000003 * seed0 + n, H_RELAX)
        tfin = res[2][0]
        cev = res[9]
        ncev = int(res[10])
        cev = cev[:min(ncev, len(cev))]
        m = modal[:, 0]
        last = int(m[-1])
        stable = bool((m[-100:] == last).all())
        outcome = 'other'
        if stable and last == a:
            outcome = 'same'
        elif stable and last in V:
            outcome = 'kappa' if (b is not None and last == b) else ('alpha' if b is not None and last != b else 'flip_sham')
        inst = cev[cev[:, 3] == 2] if len(cev) else np.zeros((0, 13))
        same_reinstall = int(sum(1 for row in inst if int(F.CX[int(row[2])]) == a))
        other_install = int(sum(1 for row in inst if int(F.CX[int(row[2])]) in V and int(F.CX[int(row[2])]) != a))
        fate = None
        if kind == 'migrant':
            # fraction of slot s carrying the migrant's program at the end
            kmig = int(st.TK[s, new_t])
            fin = sum(int(tfin[s, t]) for t in range(tfin.shape[1]) if tfin[s, t] > 0 and int(st.TK[s, t]) == kmig)
            fate = fin / N
        recs.append(dict(kind=kind, a=a, b=b, s=s, outcome=outcome, same_reinstall=same_reinstall, other_install=other_install,
                         n_inst=len(inst), fate=fate, donor_member=donor_member, flip_any=int(any(
                             int(m[g]) in V and int(m[g]) != a for g in range(0, len(m), 25)))))
    out = dict(N=N, runs=runs, fair_islands=len(isl), by_pair={str(v): len(x) for v, x in byp.items()}, wall=time.time() - t0)
    for kind in ('migrant', 'sham'):
        rs = [r for r in recs if r['kind'] == kind]
        n = len(rs)
        d = dict(n=n)
        for lab in ('same', 'kappa', 'alpha', 'other', 'flip_sham'):
            k = sum(1 for r in rs if r['outcome'] == lab)
            d[lab] = [k, n] + wilson(k, n)
        kflip = sum(1 for r in rs if r['outcome'] in ('kappa', 'alpha', 'flip_sham'))
        d['flip'] = [kflip, n] + wilson(kflip, n)
        k = sum(1 for r in rs if r['same_reinstall'] > 0)
        d['same_reinstall'] = [k, n] + wilson(k, n)
        k = sum(1 for r in rs if r['other_install'] > 0)
        d['other_pair_install'] = [k, n] + wilson(k, n)
        if kind == 'migrant':
            died = [r for r in rs if r['fate'] is not None and r['fate'] < 0.5]
            fixed = [r for r in rs if r['fate'] is not None and r['fate'] >= 0.5]
            d['migrant_fixed'] = [len(fixed), n]
            d['flip_given_fixed'] = [sum(1 for r in fixed if r['outcome'] in ('kappa', 'alpha')), len(fixed)]
            d['flip_given_died'] = [sum(1 for r in died if r['outcome'] in ('kappa', 'alpha')), len(died)]
            for dm in (True, False):
                sub = [r for r in rs if r['donor_member'] is dm]
                d['flip_donor_member_%s' % dm] = [sum(1 for r in sub if r['outcome'] in ('kappa', 'alpha')), len(sub)]
        out[kind] = d
    out['records_head'] = recs[:20]
    with open(os.path.join(OUT, 'veto_N%d.json' % N), 'w') as f:
        json.dump(out, f)
    return out


if __name__ == '__main__':
    N = int(sys.argv[1]); runs = int(sys.argv[2]); ninj = int(sys.argv[3])
    r = inject(N, runs, ninj)
    print(json.dumps({k: r[k] for k in ('N', 'fair_islands', 'wall', 'migrant', 'sham')}, default=str)[:3000])
