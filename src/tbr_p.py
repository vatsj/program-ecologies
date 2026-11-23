"""Queue 81, arm P: the modal PD at n = 9 with rival networks (bridgeless_rivals' dense and natural cells, N = 200,
I = 64, boundary mN = 1.091).  One population per island.

Reused unchanged: bridgeless_rivals.seeds / build_init / cells (published initial states and seeds), rival_islands
.restrict and ._kern (dynamics), rival_islands.cls(9) (class data; cache built by src/tbr_build_p.py).

Deviation (notes): the analysis runs use lump=False.  Exact lumping merges classes that are payoff-identical on the
current global support only, so a lumped resident or migrant is ambiguous against catalogue variants that are not
present, and migrant regret is undefined under lumping.  The law of the process is unchanged (rival_islands' docstring)
but the random stream is not, so lump=False runs are compared with the published cells statistically; the environment
is checked draw for draw separately (mode `repro`, lump=True, against the stored rows).
Intermediate snapshots (25, 50, 75% of the 10^5-generation horizon) are exact: the kernel is called with the published
seed and the check schedule truncated at the snapshot (checks draw no random numbers and the schedule is a prefix).

Definitions (one-population, amended spec):
  E(p; k)    p' with u(p', p) = u(p, p') = u(p', p') = u(p, p); E_comp: u(p', c) = u(p, c) and u(c, p') = u(c, p) for
             every class c present on island k, and u(p', p') = u(p, p).
  native     max_{p'} u(p', p) - u(p, p) (a rare p' among residents); composition: against the island's mix.
  migrants   holders of the other islands, island-count weights; Delta_q = u(p', q) - u(p, q).
  T_q        exact mean copy-generations of one q in an all-p island (frequency-dependent Moran, parent weight
             exp(w * mean payoff, self excluded), victim uniform, N births per generation) until extinction or N/2.
  prior tier not applicable (the arm has no tail; eps = 0).
  controls   prior-matched (length-prior mass mu over E), founder (E weighted by the run's founder counts); the
             arrival control is unavailable (the kernel does not log per-class arrivals).

    python3 src/tbr_p.py repro [--procs 3]          # lump=True, published seeds, compare with stored rows
    python3 src/tbr_p.py run CELLSET [--procs 3]     # CELLSET in s1, s2
"""
import argparse, gzip, json, math, os, sys, time
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTD = os.path.join(ROOT, 'runs', 'tbr_rows', 'p')
TOL = 1e-9
W = 0.3
GENS = 100000
FRACS = (25, 50, 75, 100)


def _d():
    import rival_islands as R_
    d = R_.cls(9)
    if 'U' not in d:
        V = np.asarray(d['V']).astype(np.int64)
        PDP = np.array([[-1.0, 1.0], [-2.0, 0.0]])
        d['U'] = PDP[V, V.T]
    return d


def kern_run(exp, N, I, mN, rep, gens, rival, preset, lump, upto=None):
    """rival_islands._kern with bridgeless_rivals' published seeds; `upto` truncates the check schedule."""
    import rival_islands as R_
    import bridgeless_rivals as BR
    d = _d()
    rs, ss = BR.seeds(N, I, rep, rival, preset, exp, mN, gens)
    rng = np.random.default_rng(rs)
    init, pre, Rc, removed = BR.build_init(d, N, I, rival, preset, rng)
    A1 = BR.a_ref(d, Rc) if Rc is not None else None
    sup, U, PCC, coop, tag = R_.restrict(d, init, A1, Rc)
    li = np.ascontiguousarray(init[:, sup]); K = len(sup)
    rr = np.random.default_rng(ss); r1 = rr.random(K); r2 = rr.random(K)
    iDl = int(np.searchsorted(sup, d['iD'])) if d['iD'] in set(sup.tolist()) else -1
    ch = R_.checks_schedule(gens)
    if upto is not None:
        ch = ch[ch <= upto]
    o = R_._kern(U, PCC, coop, tag, li, N, W, mN / N, ss, ch, lump, iDl, r1, r2, pre, 1)
    return d, init, sup, tag, o


# ------------------------------------------------------------------ reproduction (lump=True)
def repro_job(c):
    exp, N, I, mN, rep, gens, rival, preset = c
    import rival_islands as R_
    d, init, sup, tag, o = kern_run(exp, N, I, mN, rep, gens, rival, preset, True)
    st, sg, counts, isl_cc = o[0], o[1], o[2], o[3]
    hold = np.array([R_.holder(counts[i]) for i in range(I)])
    htag = tag[hold]
    out = dict(exp=exp, rep=rep, rival=rival, status=R_.STATUS[int(st)], stop_gen=int(sg), pcc=float(isl_cc.mean()))
    if rival is not None:
        out['held_end'] = {str(t): int((htag == t).sum()) for t in range(4)}
    return out


def stored(exp):
    import bridgeless_rivals as BR
    return BR.load(exp)


# ------------------------------------------------------------------ analysis
_SJ = {}


def sojourn_fd(N, uqq, uqp, upq, upp):
    key = (N, round(uqq, 12), round(uqp, 12), round(upq, 12), round(upp, 12))
    if key in _SJ:
        return _SJ[key]
    M = N // 2
    j = np.arange(1, M, dtype=float)
    fq = ((j - 1) * uqq + (N - j) * uqp) / (N - 1)
    fp = (j * upq + (N - j - 1) * upp) / (N - 1)
    a = j * np.exp(W * fq); b = (N - j) * np.exp(W * fp)
    up = a / (a + b) * (N - j) / N
    dn = b / (a + b) * j / N
    n = M - 1
    A = np.zeros((n, n)); idx = np.arange(n)
    A[idx, idx] = up + dn
    A[idx[:-1], idx[:-1] + 1] = -up[:-1]
    A[idx[1:], idx[1:] - 1] = -dn[1:]
    e = np.zeros(n); e[0] = 1.0
    G = np.linalg.solve(A.T, e)
    T = float((G * j).sum() / N)
    pr = np.concatenate([[1.0], np.cumprod(dn / up)])
    _SJ[key] = (T, float(1.0 / pr.sum()))
    return _SJ[key]


def fix_fd(N, uqq, uqp, upq, upp):
    """fixation from one copy (frequency-dependent Moran as above, absorbing at N)."""
    j = np.arange(1, N, dtype=float)
    fq = ((j - 1) * uqq + (N - j) * uqp) / (N - 1)
    fp = (j * upq + (N - j - 1) * upp) / (N - 1)
    g = np.exp(W * (fp - fq))
    pr = np.concatenate([[1.0], np.cumprod(g)])
    return float(1.0 / pr.sum())


def analyze_p(d, Gc, N, mN, founders, comp=True, examples=True):
    """Gc: (I, K) global counts."""
    U = d['U']; mu = d['mu']
    I, K = Gc.shape
    hold = Gc.argmax(1); share = Gc.max(1) / N
    pc = Counter(hold.tolist())
    big = [p for p, c in pc.items() if c >= 0.05 * I]
    diverse = len(big) >= 2
    set08 = share >= 0.8; set095 = share >= 0.95
    cache = {}
    cases = []
    for i in range(I):
        p = int(hold[i])
        if p not in cache:
            cache[p] = _pkey(d, p, pc, N, mN, I, examples)
        kd = cache[p]
        E = kd['E']
        cs = dict(i=i, j=0, p=p, smin=float(share[i]), set08=bool(set08[i]), set095=bool(set095[i]), nat=kd['nat'],
                  natpos=bool(kd['nat'] > TOL), nE=int(len(E)), vacE=bool(len(E) == 1), vacA=kd['vacA'], vacT=kd['vacT'],
                  regA=kd['regA_p'], regT=kd['regT_p'], pmA=kd['pmA'], pmT=kd['pmT'])
        fw = founders[E].astype(float)
        cs['fdA'] = _ctl(fw, kd['regA']) if fw.sum() > 0 else None
        cs['fdT'] = _ctl(fw, kd['regT']) if fw.sum() > 0 else None
        if examples and kd.get('ex') is not None:
            cs['ex'] = kd['ex']
        if comp:
            P = np.nonzero(Gc[i])[0]; x = Gc[i, P] / N
            Ec = np.all(U[:, P] == U[p, P][None, :], axis=1) & np.all(U[P, :] == U[P, p][:, None], axis=0) & \
                (np.diagonal(U) == U[p, p])
            ex = U[:, P] @ x
            cs['nEc'] = int(Ec.sum()); cs['natc'] = float(ex.max() - ex[p])
        cases.append(cs)
    w = dict(diverse=bool(diverse), n_profiles=len(pc), big=[[k, v] for k, v in pc.most_common(6)],
             settled08=float(set08.mean()), settled095=float(set095.mean()))
    return w, cases, cache


def _ctl(wt, reg):
    s = wt.sum()
    return [float((wt * (reg <= TOL)).sum() / s), float((wt * reg).sum() / s)]


def _pkey(d, p, pc, N, mN, I, examples):
    U = d['U']; mu = d['mu']
    diag = np.diagonal(U)
    E = np.nonzero((U[:, p] == U[p, p]) & (U[p, :] == U[p, p]) & (diag == U[p, p]))[0]
    ip = int(np.searchsorted(E, p))
    out = dict(E=E, nat=float(U[:, p].max() - U[p, p]))
    Q = np.array(sorted(pc.keys()), np.int64)
    n_q = np.array([pc[q] - (1 if q == p else 0) for q in Q], float)
    a_q = n_q / (I - 1)
    Tq = np.array([sojourn_fd(N, U[q, q], U[q, p], U[p, q], U[p, p])[0] for q in Q])
    uj = U[np.ix_(E, Q)]
    MP = (uj * a_q[None, :]).sum(1)
    dlt = uj - uj[ip][None, :]
    SG = W * (dlt * (mN * a_q * Tq)[None, :]).sum(1)
    regA = MP.max() - MP; regT = SG.max() - SG
    out.update(regA=regA, regT=regT, regA_p=float(regA[ip]), regT_p=float(regT[ip]),
               vacA=bool(MP.max() - MP.min() <= TOL), vacT=bool(SG.max() - SG.min() <= TOL))
    pw = mu[E]
    out['pmA'] = _ctl(pw, regA) if pw.sum() > 0 else None
    out['pmT'] = _ctl(pw, regT) if pw.sum() > 0 else None
    out['ex'] = None
    if examples and regT[ip] > TOL:
        bv = int(np.argmax(SG))
        v = W * mN * a_q * Tq * dlt[bv]
        k = int(np.argmax(v))
        out['ex'] = dict(kind='posreg', resident=d['names'][p], better=d['names'][int(E[bv])], sigma=float(SG[bv]),
                         sep_migrant=d['names'][int(Q[k])], delta=float(dlt[bv, k]), a_q=float(a_q[k]), T_q=float(Tq[k]))
    return out


def routes_p(cases, cache, hold2, founders_isl, tr_log, sup, gens):
    """routes as in tbr.routes, one population: c = the 25% holder is not in E(p; k) (taken over); a = the 25% holder
    is another member of E with positive T-regret; b = the 25% holder is p and no strong-holder transition (a class
    reaching 0.9 of the island, kernel log) to another class happened on the island after 25% of the horizon;
    u = otherwise.  Origin: founder if p was among the island's founders, else migrant (eps = 0)."""
    out = []
    h25, h100 = hold2
    moved = set()
    for g, i, a, b in tr_log:
        if g > gens // 4:
            moved.add((int(i), int(sup[b])))
    for cs in cases:
        if not (cs['set08'] and not cs['vacE'] and not cs['vacT'] and cs['regT'] <= TOL):
            continue
        i, p = cs['i'], cs['p']
        kd = cache[p]; E = kd['E']
        p0 = int(h25[i])
        x = int(np.searchsorted(E, p0)); inE = x < len(E) and E[x] == p0
        if not inE:
            r = 'c'
        elif p0 != p and kd['regT'][x] > TOL:
            r = 'a'
        elif p0 == p and all(q == p for (ii, q) in moved if ii == i):
            r = 'b'
        else:
            r = 'u'
        org = 'founder' if founders_isl[i, p] > 0 else 'migrant'
        out.append(dict(i=i, j=0, p=p, route=r, origin=org, natpos=cs['natpos']))
    return out


def run_cell(c, outdir=OUTD):
    exp, N, I, mN, rep, gens, rival, preset = c
    tagr = 'nat' if rival is None else rival.replace('(', '[').replace(')', ']').replace(',', ';')
    path = os.path.join(outdir, '%s_%s_%g_%d.json.gz' % (exp, tagr, mN, rep))
    if os.path.exists(path):
        return path
    t0 = time.time()
    snaps = {}; hold4 = []; G4 = []
    for fr in (25, 100):
        d, init, sup, tag, o = kern_run(exp, N, I, mN, rep, gens, rival, preset, False, upto=gens * fr // 100)
        counts = o[2]
        K = len(d['names'])
        Gc = np.zeros((I, K), np.int64); Gc[:, sup] = counts
        G4.append(Gc); hold4.append(Gc.argmax(1))
        if fr == 100:
            st, sg, isl_cc, tr_log = o[0], o[1], o[3], o[28]
    founders = init.sum(0)
    rec = dict(arm='P', exp=exp, rival=rival, N=N, I=I, mN=mN, run=rep, status=int(st), stop=int(sg),
               pcc=float(isl_cc.mean()), n_tr=int(len(tr_log)))
    for k, fr in enumerate((25, 100)):
        hz = fr == 100
        w, cases, cache = analyze_p(d, G4[k], N, mN, founders, comp=hz, examples=hz)
        if not hz:
            cases = [{x: cs[x] for x in ('i', 'j', 'p', 'set08', 'set095', 'natpos', 'vacE', 'vacA', 'vacT', 'regA',
                                         'regT', 'pmA', 'pmT', 'fdA', 'fdT')} for cs in cases]
        else:
            hcases, hcache = cases, cache
        snaps[str(fr)] = dict(world=w, cases=cases)
    rec['snaps'] = snaps
    rec['routes'] = routes_p(hcases, hcache, hold4, init, tr_log, sup, gens)
    rec['names_used'] = {str(k): d['names'][k] for k in set(int(x) for h in hold4 for x in h)}
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


def cellset(name, nrep=20):
    import bridgeless_rivals as BR
    B = BR.boundary()
    out = []
    if name in ('s1', 'repro'):
        for rv in BR.forced()['six']:
            for rep in range(nrep):
                out.append(('dense', 200, 64, B[200], rep, GENS, rv, 'dense'))
        for rep in range(nrep):
            out.append(('nat', 200, 64, B[200], rep, GENS, None, 'iid'))
    elif name == 's2':
        for mN in (0.1, 3.0, 10.0):
            for rv in BR.forced()['six']:
                for rep in range(nrep):
                    out.append(('dense', 200, 64, mN, rep, GENS, rv, 'dense'))
            for rep in range(nrep):
                out.append(('nat', 200, 64, mN, rep, GENS, None, 'iid'))
    return out


def _w(c):
    try:
        t = time.time(); p = run_cell(c)
        return 'done %s %s %g %d %.0fs' % (c[0], (c[6] or '-')[:30], c[3], c[4], time.time() - t)
    except Exception as e:
        import traceback
        return 'FAIL %s %r\n%s' % (c, e, traceback.format_exc())


def _rw(c):
    return repro_job(c)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['repro', 'run', 'one'])
    ap.add_argument('set', nargs='?', default='s1')
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--nrep', type=int, default=20)
    ap.add_argument('--shard', default='0/1', help='i/k: run cells i, i+k, ... of the sorted cell set')
    a = ap.parse_args()
    from multiprocessing import Pool
    if a.cmd == 'repro':
        cs = cellset('repro', a.nrep)
        with Pool(a.procs) as pool:
            res = pool.map(_rw, cs)
        st = {}
        for exp in ('dense', 'nat'):
            for r in stored(exp):
                st[(exp, r['rival'], r['rep'])] = r
        out = []
        nmatch = 0
        for r in res:
            s = st.get((r['exp'], r['rival'], r['rep']))
            ok = s is not None and s['status'] == r['status'] and s['stop_gen'] == r['stop_gen'] and \
                abs(s['pcc'] - r['pcc']) < 1e-9 and (r['rival'] is None or s['held_end'] == r['held_end'])
            nmatch += ok
            out.append(dict(r, match=bool(ok)))
        os.makedirs(OUTD, exist_ok=True)
        json.dump(dict(n=len(out), matched=nmatch, rows=out), open(os.path.join(OUTD, 'repro.json'), 'w'))
        print('repro: %d of %d match' % (nmatch, len(out)))
    elif a.cmd == 'run':
        cs = cellset(a.set, a.nrep)
        cs.sort(key=lambda c: (c[6] is None, c[4], c[3], c[6] or ''))
        si, sk = (int(x) for x in a.shard.split('/'))
        cs = cs[si::sk]
        with Pool(a.procs) as pool:
            for m in pool.imap_unordered(_w, cs):
                print(m, flush=True)
    else:
        c = cellset('s1', 1)[0]
        print(_w(c))


if __name__ == '__main__':
    main()
