"""One chain cell of the union game, or the static tables and reduced chains.

    python3 src/union_run.py chain --arm quorum --c 0.5 --N 100
    python3 src/union_run.py static
Writes runs/union/<arm>_c<c>_N<N>.json (chain) and runs/union/static.json.
"""
import argparse, json, os, sys, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import union as U
from union_chain import UChain, dense_chain, log_rho

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'union')
WORK = ['both work', 'one strikes', 'both strike']


def load(arm):
    """Language, classes and named indices (classes cached in runs/union/)."""
    os.makedirs(OUT, exist_ok=True)
    d = U.build(arm=arm)
    f = os.path.join(OUT, 'classes_%s.npz' % arm)
    if os.path.exists(f):
        z = np.load(f)
        C = {k: z[k] for k in z.files}
        for k in ('KcW', 'KcB'): C[k] = int(C[k])
    else:
        C = U.classes(d)
        C.pop('J')
        np.savez(f, **C)
    P = d['P']
    nmw = {k: (int(C['cw'][v]) if v is not None else None) for k, v in U.named(P).items()}
    nmb = {k: int(C['cb'][v]) for k, v in U.named_boss(P).items()}
    return d, C, nmw, nmb


def wsrc(d, C, x):
    return d['P'].src_w(C['repW'][x])


def bsrc(d, C, b):
    return d['P'].src_b(C['repB'][b])


def describe(d, C, b, x, y):
    return '%s | %s | %s' % (bsrc(d, C, b), wsrc(d, C, x), wsrc(d, C, y))


def state_info(typ):
    j = typ // 4; t1 = (typ // 2) % 2; t2 = typ % 2
    b = j // 4; a1 = (j // 2) % 2; a2 = j % 2
    return dict(j=j, t1=t1, t2=t2, wage=b // 3, whack=b % 3, work=a1 + a2, summ=U.summary(j, t1, t2))


def exits(ch, code, top=12):
    """Single-mutant moves out of `code` with probability per mutation event."""
    b, x, y = ch.decode(code)
    PAY, Jc, tg = ch.PAY, ch.Jc, ch.tagc
    j0 = Jc[b, x, y]; r = PAY[j0, tg[x], tg[y]]
    out = []
    for s in range(3):
        K = ch.KcB if s == 0 else ch.KcW
        for q in range(K):
            t = [b, x, y]
            if t[s] == q or ch.mass[s, q] == 0: continue
            t[s] = q
            j = Jc[t[0], t[1], t[2]]; u = PAY[j, tg[t[1]], tg[t[2]]]
            du = u[s] - r[s]
            rho = float(np.exp(log_rho(ch.w * du, float(ch.N))))
            same = j == j0 and np.allclose(u, r)
            kind = 'strict' if du > 1e-12 else ('deleterious' if du < -1e-12 else ('neutral-keep' if same else 'neutral-change'))
            out.append(dict(slot=s, cls=q, to=t, mass=ch.mass[s, q] / 3, du=float(du), rho=rho, prob=ch.mass[s, q] / 3 * rho, kind=kind,
                            summ_to=U.SUMM[U.summary(j, tg[t[1]], tg[t[2]])]))
    tot = {k: sum(e['prob'] for e in out if e['kind'] == k) for k in ('strict', 'neutral-change', 'neutral-keep', 'deleterious')}
    out.sort(key=lambda e: -e['prob'])
    return out[:top], tot


def analyse(ch, d, C, nmw, nmb, args):
    codes, pi, pay, typ = ch.codes, ch.pi, ch.pay, ch.typ
    n = len(codes)
    info = [state_info(int(t)) for t in typ]
    summ = np.array([z['summ'] for z in info]); wage = np.array([z['wage'] for z in info])
    whack = np.array([z['whack'] for z in info]); work = np.array([z['work'] for z in info])
    out = dict(arm=args.arm, c=args.c, N=args.N, w=args.w, theta=args.theta, states=n, core=int(ch.is_core.sum()),
               ring=int((~ch.is_core).sum()), cut_flow=ch.cut_flow, rel_cut=ch.rel_cut, rel_cut_change=ch.rel_cut_change,
               rounds=ch.log, KcB=ch.KcB, KcW=ch.KcW)
    out['summary'] = {U.SUMM[k]: float(pi[summ == k].sum()) for k in range(7)}
    # joint (wage, work pattern, whack policy)
    joint = {}
    for si in range(3):
        for wk in range(3):
            for hi in range(3):
                m = float(pi[(wage == si) & (work == wk) & (whack == hi)].sum())
                if m > 0:
                    joint['s=%s, %s, %s' % (U.WNAME[si], WORK[wk], U.HNAME[hi])] = m
    out['joint'] = dict(sorted(joint.items(), key=lambda kv: -kv[1]))
    out['wage_dist'] = {U.WNAME[si]: float(pi[wage == si].sum()) for si in range(3)}
    out['whack_policy_dist'] = {U.HNAME[hi]: float(pi[whack == hi].sum()) for hi in range(3)}
    out['mean_payoff'] = dict(zip(['boss', 'W1', 'W2'], (pi @ pay).tolist()))
    out['efficiency'] = float(pi @ pay.sum(1))                    # max 2
    out['P_both_work_no_whack'] = float(pi[np.isin(summ, [0, 1, 2])].sum())
    out['P_equal_division'] = out['summary']['fair']
    # currents among summaries
    i = ch.src; jdx = ch.dst_idx; f = np.exp(ch.lpi[i] + ch.pr)
    si_, sj_ = summ[i], summ[jdx]
    J = {}
    for A in range(7):
        for B in range(7):
            if A != B:
                v = float(f[(si_ == A) & (sj_ == B)].sum())
                if v > 0: J[U.SUMM[A] + '>' + U.SUMM[B]] = v
    out['currents'] = J
    net = {}
    for A in range(7):
        for B in range(A + 1, 7):
            a = J.get(U.SUMM[A] + '>' + U.SUMM[B], 0.0); b_ = J.get(U.SUMM[B] + '>' + U.SUMM[A], 0.0)
            if a + b_ > 0: net[U.SUMM[A] + '>' + U.SUMM[B]] = a - b_
    out['net_currents'] = net
    dwell = {}; M = np.zeros((7, 7))
    for A in range(7):
        pa = float(pi[summ == A].sum())
        outA = sum(J.get(U.SUMM[A] + '>' + U.SUMM[B], 0.0) for B in range(7) if B != A)
        dwell[U.SUMM[A]] = pa / outA if outA > 0 else (float('inf') if pa > 0 else None)
        for B in range(7):
            if A != B and pa > 0: M[A, B] = J.get(U.SUMM[A] + '>' + U.SUMM[B], 0.0) / pa
        M[A, A] = 1 - M[A].sum()
    out['dwell_events'] = dwell
    live = [A for A in range(7) if pi[summ == A].sum() > 0]
    ev = np.sort(np.abs(np.linalg.eigvals(M[np.ix_(live, live)])))[::-1]
    out['lumped_relaxation_events'] = float(1 / (1 - ev[1])) if len(ev) > 1 and ev[1] < 1 else float('inf')
    # support
    order = np.argsort(-pi)
    dec = [ch.decode(int(cd)) for cd in codes]
    out['support'] = [dict(pi=float(pi[k]), state=describe(d, C, *dec[k]), summary=U.SUMM[summ[k]], pay=np.round(pay[k], 3).tolist())
                      for k in order[:30]]
    out['support_size_99'] = int(np.searchsorted(np.cumsum(pi[order]), 0.99) + 1)
    # mass on states with a conditional program in some slot
    P = d['P']
    condB = np.array([P.nat[0, C['repB'][b]] > 0 for b in range(ch.KcB)])
    condW = np.array([P.nat[1, C['repW'][x]] > 0 for x in range(ch.KcW)])
    isc = np.array([condB[b] or condW[x] or condW[y] for b, x, y in dec])
    out['mass_with_conditional'] = float(pi[isc].sum())
    out['mass_conditional_worker'] = float(pi[np.array([condW[x] or condW[y] for b, x, y in dec])].sum())
    out['mass_conditional_boss'] = float(pi[np.array([condB[b] for b, x, y in dec])].sum())
    # named worker programs: pi mass of states with at least one worker in the class
    nmass = {}
    for k, v in nmw.items():
        if v is None: continue
        nmass[k] = float(pi[np.array([x == v or y == v for b, x, y in dec])].sum())
    out['named_worker_presence'] = nmass
    tagged = np.array([C['tagc'][x] or C['tagc'][y] for b, x, y in dec])
    out['mass_tagged_worker_present'] = float(pi[tagged].sum())
    # transitions out of top states
    trans = []
    for k in order[:10]:
        ex, tot = exits(ch, int(codes[k]), top=6)
        trans.append(dict(state=describe(d, C, *dec[k]), pi=float(pi[k]), summary=U.SUMM[summ[k]], exit_by_kind=tot,
                          top=[dict(p=e['prob'], kind=e['kind'], slot=['B', 'W1', 'W2'][e['slot']],
                                    mutant=(bsrc(d, C, e['cls']) if e['slot'] == 0 else wsrc(d, C, e['cls'])), to=e['summ_to']) for e in ex]))
    out['transitions'] = trans
    # the two drift rates of the race (flows per mutation event, and per unit mass of the source summary)
    dB = np.array([dec[k][0] for k in range(n)]); dX = np.array([dec[k][1] for k in range(n)]); dY = np.array([dec[k][2] for k in range(n)])
    unionlike = set(v for k, v in nmw.items() if k.startswith('union') and v is not None)
    ul = np.array([x in unionlike for x in range(ch.KcW)])
    ent_u = ((ul[dX[jdx]] & ~ul[dX[i]] & (dB[jdx] == dB[i]) & (dY[jdx] == dY[i])) |
             (ul[dY[jdx]] & ~ul[dY[i]] & (dB[jdx] == dB[i]) & (dX[jdx] == dX[i])))
    tagc = C['tagc'].astype(bool)
    ent_t = ((tagc[dX[jdx]] & ~tagc[dX[i]] & (dB[jdx] == dB[i])) | (tagc[dY[jdx]] & ~tagc[dY[i]] & (dB[jdx] == dB[i])))
    bch = dB[jdx] != dB[i]
    ent_src = bch & (whack[jdx] == 2) & (whack[i] != 2)
    ent_stk = bch & (whack[jdx] == 0) & (whack[i] != 0)
    out['drift'] = dict(
        union_like_into_worker_slot=float(f[ent_u].sum()),
        tagged_into_worker_slot=float(f[ent_t].sum()),
        source_targeting_into_boss_slot=float(f[ent_src].sum()),
        strike_targeting_into_boss_slot=float(f[ent_stk].sum()),
        source_targeting_into_boss_from_tagged_states=float(f[ent_src & tagged[i]].sum()),
        total_flow=float(f.sum()))
    # named states: exits
    named_states = {
        'Z: (0,none) scab scab': (nmb['(0,none)'], nmw['scab'], nmw['scab']),
        'I: (1/4,none) scab scab': (nmb['(1/4,none)'], nmw['scab'], nmw['scab']),
        'Fs: (1/2,none) scab scab': (nmb['(1/2,none)'], nmw['scab'], nmw['scab']),
        'Fm: (1/2,none) militant militant': (nmb['(1/2,none)'], nmw['militant'], nmw['militant']),
        'Zm: (0,none) militant scab': (nmb['(0,none)'], nmw['militant'], nmw['scab']),
    }
    if nmw.get('union') is not None:
        named_states.update({
            'F: (1/2,none) union union': (nmb['(1/2,none)'], nmw['union'], nmw['union']),
            'Fu1: (1/2,none) union scab': (nmb['(1/2,none)'], nmw['union'], nmw['scab']),
            'Zu1: (0,none) union scab': (nmb['(0,none)'], nmw['union'], nmw['scab']),
            'S: (0,none) union union': (nmb['(0,none)'], nmw['union'], nmw['union']),
            'Zsrc: (0,source) scab scab': (nmb['(0,source)'], nmw['scab'], nmw['scab'])})
    up = nmw.get("union' (BOX(OTHER=strike))")
    if up is not None:
        named_states["F': (1/2,none) union' union'"] = (nmb['(1/2,none)'], up, up)
    ns = {}
    idx = ch.index
    for name, (b, x, y) in named_states.items():
        cd = ch.code(b, x, y)
        ex, tot = exits(ch, cd, top=6)
        k = idx.get(int(cd))
        ns[name] = dict(pi=float(pi[k]) if k is not None else None, exit_by_kind=tot,
                        top=[dict(p=e['prob'], kind=e['kind'], slot=['B', 'W1', 'W2'][e['slot']],
                                  mutant=(bsrc(d, C, e['cls']) if e['slot'] == 0 else wsrc(d, C, e['cls'])), to=e['summ_to']) for e in ex])
    out['named_states'] = ns
    return out


def seeds(ch, nmw, nmb):
    W = [v for v in nmw.values() if v is not None]
    return [ch.code(b, x, y) for b in nmb.values() for x in W for y in W]


def run_chain(args):
    t = time.time()
    d, C, nmw, nmb = load(args.arm)
    ch = UChain(C, args.c, args.N, w=args.w, theta=args.theta, max_states=args.max_states, core_max=args.core_max,
                promote=args.promote, arm=args.arm, verbose=True)
    ch.max_rounds = args.max_rounds
    ch.explore_hybrid(seeds(ch, nmw, nmb))
    tex = time.time() - t
    print('explored %d states in %.0fs' % (len(ch.codes), tex), flush=True)
    if args.timing:
        return
    out = analyse(ch, d, C, nmw, nmb, args)
    out['time_s'] = time.time() - t; out['explore_s'] = tex
    tag = '%s_c%g_N%d' % (args.arm, args.c, args.N)
    json.dump(out, open(os.path.join(OUT, tag + '.json'), 'w'), indent=1, default=float)
    print(json.dumps({k: out[k] for k in ('arm', 'c', 'N', 'states', 'rel_cut_change', 'summary', 'efficiency', 'mean_payoff', 'dwell_events', 'time_s')}, indent=1, default=float))


# ---------------------------------------------------------------- static tables and reduced chains
def run_static(args):
    out = {}
    d, C, nmw, nmb = load('quorum')
    Jc, tg = C['Jc'], C['tagc']
    names = ['scab', 'militant', 'union']
    W = [nmw[k] for k in names]
    Bn = [U.bname(b) for b in range(U.NB)]
    B = [nmb[k] for k in Bn]
    out['language'] = dict(boss_n=6, worker_n=10, boss_functions=int(d['P'].KB), worker_functions=int(d['P'].KW),
                           boss_classes=int(C['KcB']), worker_classes=int(C['KcW']))
    out['named_mass'] = {k: float(C['massW'][v]) for k, v in nmw.items() if v is not None}
    for c in (0.0, 0.1, 0.5):
        PAY = U.payoff_table(c)
        rows = []
        for bi, b in enumerate(B):
            for xi, x in enumerate(W):
                for yi, y in enumerate(W):
                    if yi < xi: continue          # W1 <-> W2 symmetric
                    j = Jc[b, x, y]; r = PAY[j, tg[x], tg[y]]
                    mov = []
                    for s in range(3):
                        pool = B if s == 0 else W
                        pn = Bn if s == 0 else names
                        for qi, q in enumerate(pool):
                            t = [b, x, y]
                            if t[s] == q: continue
                            t[s] = q
                            j2 = Jc[t[0], t[1], t[2]]; u = PAY[j2, tg[t[1]], tg[t[2]]]
                            du = float(u[s] - r[s])
                            mov.append(dict(slot=['B', 'W1', 'W2'][s], mutant=pn[qi], du=du,
                                            rhoN={str(N): float(np.exp(log_rho(0.3 * du, float(N)))) * N for N in (100, 1000, 10000)},
                                            to=U.joint_name(j2), to_summary=U.SUMM[U.summary(j2, tg[t[1]], tg[t[2]])]))
                    rows.append(dict(boss=Bn[bi], W1=names[xi], W2=names[yi], play=U.joint_name(j),
                                     summary=U.SUMM[U.summary(j, tg[x], tg[y])], pay=r.round(3).tolist(), moves=mov))
        out['c=%g' % c] = rows
        # reduced canonical-strategy chains: uniform prior over the named programs, and the length prior restricted
        red = {}
        for pri in ('uniform', 'mu'):
            mB = np.ones(len(B)) if pri == 'uniform' else C['massB'][B]
            mW = np.ones(len(W)) if pri == 'uniform' else C['massW'][W]
            for N in (100, 1000, 10000):
                st, lpi, A = dense_chain(Jc, tg, PAY, B, W, mB, mW, N, 0.3)
                pi = np.exp(lpi)
                sm = np.zeros(7); top = []
                for k, (b, x, y) in enumerate(st):
                    sm[U.summary(Jc[b, x, y], tg[x], tg[y])] += pi[k]
                for k in np.argsort(-pi)[:8]:
                    b, x, y = st[k]
                    top.append(dict(pi=float(pi[k]), state='%s %s %s' % (Bn[B.index(b)], names[W.index(x)], names[W.index(y)]),
                                    summary=U.SUMM[U.summary(Jc[b, x, y], tg[x], tg[y])]))
                # currents among summaries
                lab = np.array([U.summary(Jc[b, x, y], tg[x], tg[y]) for (b, x, y) in st])
                F = np.exp(lpi[:, None] + A)
                cur = {}
                for a_ in range(7):
                    for b_ in range(7):
                        if a_ != b_:
                            v = float(F[np.ix_(lab == a_, lab == b_)].sum())
                            if v > 0: cur[U.SUMM[a_] + '>' + U.SUMM[b_]] = v
                red['%s_N%d' % (pri, N)] = dict(summary=dict(zip(U.SUMM, sm.tolist())), top=top, currents=cur)
        out['reduced_c=%g' % c] = red
    json.dump(out, open(os.path.join(OUT, 'static.json'), 'w'), indent=1, default=float)
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['chain', 'static'])
    ap.add_argument('--arm', default='quorum', choices=['quorum', 'noquorum', 'blind'])
    ap.add_argument('--c', type=float, default=0.5)
    ap.add_argument('--N', type=float, default=100)
    ap.add_argument('--w', type=float, default=0.3)
    ap.add_argument('--theta', type=float, default=1e-9)
    ap.add_argument('--max_states', type=int, default=400000)
    ap.add_argument('--core_max', type=int, default=2500)
    ap.add_argument('--promote', type=float, default=1e-5)
    ap.add_argument('--max_rounds', type=int, default=40)
    ap.add_argument('--timing', action='store_true')
    args = ap.parse_args()
    if args.what == 'chain':
        run_chain(args)
    else:
        run_static(args)
