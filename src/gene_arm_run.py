"""Runner for the gene arm (src/gene_arm.py; notes/gene-arm.md; predictions/2026-10-11-gene-arm.md).

    python3 src/gene_arm_run.py guard                      # scale guard at cap 2 -> runs/gene_arm/guard.json
    python3 src/gene_arm_run.py static                     # static tables (cap 1 SOG, cap 2 chicken) -> runs/gene_arm/static.json
    python3 src/gene_arm_run.py cell ARM KERNEL PRIOR N    # one SOG chain cell -> runs/gene_arm/cell_*.json
    python3 src/gene_arm_run.py cells [--procs 3]          # the planned SOG chain panel
    python3 src/gene_arm_run.py chicken                    # chicken static + chains + lottery -> runs/gene_arm/chicken.json
    python3 src/gene_arm_run.py lottery [--procs 3]        # SOG lottery cells
    python3 src/gene_arm_run.py coalition                  # coalition kernel cell
"""
import argparse, json, math, os, sys, time, zlib
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gene_arm as GA
import union as U

OUT = GA.OUT
CAP = 1
KERNELS = {'prior': 0, 'SG': 1, 'local': 2}
_CACHE = {}


def jdump(obj, name):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), 'w') as f:
        json.dump(obj, f, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))


def sog():
    if 'G' not in _CACHE:
        _CACHE['G'] = GA.SOG(CAP)
    return _CACHE['G']


def tables(rule):
    k = ('T', rule)
    if k not in _CACHE:
        _CACHE[k] = GA.build_tables(sog(), rule, verbose=False)
    return _CACHE[k]


def the_filter():
    """the override filter against the frozen reference catalogue (all cap-1 programs, CC); witnesses weighted by the
    length prior."""
    if 'F' not in _CACHE:
        G = sog()
        f = os.path.join(OUT, 'filter_cap%d.json' % CAP)
        if os.path.exists(f):
            F = json.load(open(f))
            F = {r: {int(k): v for k, v in F[r].items()} for r in F}
        else:
            mB, mW = GA.priors(G)['length']
            F = GA.filter_genes(G, tables('CC'), mB, mW)
            jdump(F, 'filter_cap%d.json' % CAP)
        _CACHE['F'] = F
    return _CACHE['F']


def arm(name):
    return GA.arm_spec(name, sog(), the_filter())


def masses(A, prior):
    """program masses (full-length arrays).  Base arms: the prior over the base list itself; gene arms: the G-all
    prior with filtered programs null (masses preserved)."""
    G = sog()
    if A['name'].startswith('base-'):
        mB = np.zeros(G.KB); mW = np.zeros(G.KW)
        bb = np.array([b for b in range(G.KB) if not G.bprog[b][1]]); ww = np.array([x for x in range(G.KW) if not G.wprog[x][1]])
        if prior == 'length':
            mB[bb] = GA.length_prior(G.bsize[bb]); mW[ww] = GA.length_prior(G.wsize[ww])
        else:
            mB[bb] = 1.0 / len(bb); mW[ww] = 1.0 / len(ww)
        return mB, mW
    if prior == 'uniform':
        return named_uniform(A)
    return GA.priors(G)[prior]


# the named genes of the reduced uniform catalogue (notes §1.17)
NAMED_BGENES = {'whack w1': GA.bgene(0, 3), 'whack w2': GA.bgene(1, 3), 'probe concession': GA.bgene(4, 2),
                'de-escalation': GA.bgene(0, 4), 'wage cut': GA.bgene(2, 0), 'strike concession C1': GA.bgene(0, 2)}
NAMED_WGENES = {'quorum': GA.wgene(7, 1), 'threat accommodation': GA.wgene(3, 0), 'work if fair': GA.wgene(2, 0),
                'solidarity': GA.wgene(6, 1), 'refusal': GA.wgene(0, 1)}


def named_uniform(A):
    """uniform over the named catalogue: every base, alone or with one named gene (the arm's admissible ones);
    filtered named programs are null (mass preserved, 1 / |named catalogue| each)."""
    G = sog()
    nb = [b for b in range(G.KB) if not G.bprog[b][1] or G.bprog[b][1][0] in NAMED_BGENES.values()]
    nw = [x for x in range(G.KW) if not G.wprog[x][1] or G.wprog[x][1][0] in NAMED_WGENES.values()]
    mB = np.zeros(G.KB); mW = np.zeros(G.KW)
    mB[nb] = 1.0 / len(nb); mW[nw] = 1.0 / len(nw)
    return mB, mW


NAMED = {
    'Z': (((0, 1, 0), ()), ((0, 0), ()), ((0, 0), ())),
    'Z_w': (((0, 0, 0), ()), ((0, 0), ()), ((0, 0), ())),
    'S': (((0, 1, 0), ()), ((3, 0), ()), ((3, 0), ())),
    'split': (((0, 1, 0), ()), ((0, 0), ()), ((3, 0), ())),
    'F': (((2, 1, 0), ()), ((2, 0), ()), ((2, 0), ())),
    'F_u': (((2, 1, 0), ()), ((0, 1), ()), ((0, 1), ())),
    'I': (((1, 1, 0), ()), ((1, 0), ()), ((1, 0), ())),
    'F*': (((0, 1, 2), ()), ((2, 0), ()), ((2, 0), ())),
    'Z_D0': (((0, 1, 1), ()), ((0, 0), ()), ((0, 0), ())),
}


def named_progs():
    G = sog()
    return {k: (G.find_b(*v[0]), G.find_w(*v[1]), G.find_w(*v[2])) for k, v in NAMED.items()}


def state_name(G, b, x, y):
    return '%s | %s | %s' % (G.bname(b), G.wname(x), G.wname(y))


# ------------------------------------------------------------------ chain cell
def build_cell(arm_name, kernel, prior):
    G = sog(); A = arm(arm_name)
    Tbl = tables(A['rule'])
    mB, mW = masses(A, prior)
    bsel, wsel = A['bsel'], A['wsel']
    keepB = bsel[mB[bsel] > 0]; keepW = wsel[mW[wsel] > 0]
    A = dict(A, bsel=keepB, wsel=keepW)
    L = GA.lump(Tbl['J'], G.tag, keepB, keepW, mB[keepB], mW[keepW])
    Un = GA.make_units(G, L, A, mB, mW, refine=(kernel != 'prior'))
    rw = keepW[L['repW']]
    QSc = np.ascontiguousarray(Tbl['QS'][np.ix_(rw, rw)])
    return G, A, Tbl, L, Un, QSc, mB, mW


def seeds_for(ch, G, A, L, Un):
    from solver_audit import union_strict_ne
    Km = max(L['KcB'], L['KcW'])
    cm = np.zeros((3, Km)); cm[0, :L['KcB']] = L['massB']; cm[1, :L['KcW']] = L['massW']; cm[2, :L['KcW']] = L['massW']
    ne = union_strict_ne(dict(Jc=L['Jc'], tagc=L['tagc'], KcB=L['KcB'], KcW=L['KcW']), GA.PAY, cm)
    bestB = {}; bestW = {}
    for u in range(Un['KuB']):
        c = int(Un['ucB'][u])
        if c not in bestB or Un['massB'][u] > Un['massB'][bestB[c]]: bestB[c] = u
    for u in range(Un['KuW']):
        c = int(Un['ucW'][u])
        if c not in bestW or Un['massW'][u] > Un['massW'][bestW[c]]: bestW[c] = u
    s = set(ch.code(bestB[b], bestW[x], bestW[y]) for (b, x, y) in ne)
    for k, (b, x, y) in named_progs().items():
        if b in Un['posB'] and x in Un['posW'] and y in Un['posW']:
            s.add(ch.code(Un['posB'][b], Un['posW'][x], Un['posW'][y]))
    # every class triple of constants (as the union run: boss constants x named workers) is cheap and helps
    return sorted(s), ne


def state_exits(ch, code, top=6):
    src, dst, pr = ch.rows(np.array([code]), np.array([code]), np.zeros(1), 0.0, mode=1)[:3]
    b, x, y = ch.decode(code)
    Jc, tg, Un = ch.Jc, ch.tagc, ch.Un
    j0 = Jc[Un['ucB'][b], Un['ucW'][x], Un['ucW'][y]]
    u0 = GA.PAY[j0, tg[Un['ucW'][x]], tg[Un['ucW'][y]]]
    agg = defaultdict(float)
    rows = []
    bydst = defaultdict(float)
    for d, lp in zip(dst, pr):
        bydst[int(d)] = np.logaddexp(bydst.get(int(d), -np.inf), lp)
    for d, lp in bydst.items():
        b2, x2, y2 = ch.decode(d)
        s = [i for i in range(3) if (b, x, y)[i] != (b2, x2, y2)[i]][0]
        cb, cx, cy = Un['ucB'][b2], Un['ucW'][x2], Un['ucW'][y2]
        j = Jc[cb, cx, cy]; u = GA.PAY[j, tg[cx], tg[cy]]
        du = float(u[s] - u0[s])
        kind = 'strict' if du > 1e-12 else ('deleterious' if du < -1e-12 else ('neutral-change' if (j != j0 or np.abs(u - u0).max() > 1e-12) else 'neutral-keep'))
        r = float(np.exp(lp))
        agg[kind] += r
        rows.append(dict(rate=r, slot=['B', 'W1', 'W2'][s], kind=kind, delta=du, N_delta=du * ch.N,
                         to=unit_state_name(ch, d), to_play=U.joint_name(int(j)), to_summary=U.SUMM[U.summary(int(j), int(tg[cx]), int(tg[cy]))]))
    rows.sort(key=lambda e: -e['rate'])
    return dict(exit_total=float(sum(agg.values())), by_kind=dict(agg), top=rows[:top])


def unit_state_name(ch, code):
    G = sog(); b, x, y = ch.decode(code)
    return state_name(G, int(ch.Un['repB'][b]), int(ch.Un['repW'][x]), int(ch.Un['repW'][y]))


def analyse_cell(ch, G, A, Tbl, top=12):
    pi = ch.pi; codes = ch.codes; typ = ch.typ
    js = typ // 4; t1 = (typ // 2) % 2; t2 = typ % 2
    sm = np.array([U.summary(int(j), int(a), int(b)) for j, a, b in zip(js, t1, t2)])
    out = dict(states=int(len(codes)), core=int(ch.is_core.sum()), rel_cut=float(ch.rel_cut), rel_cut_change=float(ch.rel_cut_change))
    out['summary'] = {U.SUMM[k]: float(pi[sm == k].sum()) for k in range(7)}
    wi = (js // 4) // 3; hh = (js // 4) % 3
    out['wage'] = {U.WNAME[s]: float(pi[wi == s].sum()) for s in range(3)}
    out['implemented_whack'] = {U.HNAME[h]: float(pi[hh == h].sum()) for h in range(3)}
    pay = ch.pay
    out['payoffs'] = dict(boss=float(pi @ pay[:, 0]), W1=float(pi @ pay[:, 1]), W2=float(pi @ pay[:, 2]), efficiency=float(pi @ pay.sum(1)))
    # committed strike-whacker bosses held (the boss program's policy, base or gene, is "whack strikers")
    reps = [ch.decode(int(c)) for c in codes]
    bprog = np.array([int(ch.Un['repB'][b]) for b, _, _ in reps])
    out['strike_whacker_base'] = float(pi[np.array([G.bh[b] == 0 for b in bprog])].sum())
    out['probe_boss'] = float(pi[np.array([G.bp[b] > 0 or any(G.btr[b, i] >= 4 for i in range(G.bng[b])) for b in bprog])].sum())
    out['gene_carrier_mass'] = dict(boss=float(pi[np.array([G.bng[b] > 0 for b in bprog])].sum()),
                                    workers=float(sum(pi[k] * 0.5 * ((G.wng[int(ch.Un['repW'][x])] > 0) + (G.wng[int(ch.Un['repW'][y])] > 0)) for k, (_, x, y) in enumerate(reps))))
    order = np.argsort(-pi)
    out['support_size_99'] = int(np.searchsorted(np.cumsum(pi[order]), 0.99) + 1)
    sup = []
    for k in order[:top]:
        b, x, y = reps[k]
        pb, px, py = int(ch.Un['repB'][b]), int(ch.Un['repW'][x]), int(ch.Un['repW'][y])
        j = int(js[k])
        gs, wit = GA.gene_stable(G, Tbl, A, pb, px, py)
        gsw, witw = GA.gene_stable(G, Tbl, A, pb, px, py, weak=True)
        u = GA.PAY[j, int(t1[k]), int(t2[k])]
        sup.append(dict(pi=float(pi[k]), state=state_name(G, pb, px, py), play=U.joint_name(j), summary=U.SUMM[sm[k]],
                        pay=[float(v) for v in u], nash=bool(GA.is_nash(j, int(t1[k]), int(t2[k]))), pareto_dominated=bool(GA.pareto_dominated(u)),
                        gene_stable=bool(gs), gene_witness=wit, weak_gene_stable=bool(gsw), weak_witness=witw))
    out['support'] = sup
    out['transitions'] = []
    for k in order[:6]:
        e = state_exits(ch, int(codes[k]))
        e.update(state=unit_state_name(ch, int(codes[k])), pi=float(pi[k]), summary=U.SUMM[sm[k]])
        out['transitions'].append(e)
    out['execution'] = execution_stats(G, A, Tbl, ch, reps, pi, js, t1, t2)
    # proof device on the top states (pi >= 0.01)
    dv = dict(stable=0.0, weak=0.0, dominated=0.0, dominated_stable=0.0, dominated_weak=0.0, nash=0.0, nash_stable=0.0, covered=0.0)
    ex_dom = []
    for k in order[:out['support_size_99']][:3000]:
        b, x, y = reps[k]
        pb, px, py = int(ch.Un['repB'][b]), int(ch.Un['repW'][x]), int(ch.Un['repW'][y])
        j = int(js[k]); u = GA.PAY[j, int(t1[k]), int(t2[k])]
        gs = GA.gene_stable(G, Tbl, A, pb, px, py)[0]; gw = GA.gene_stable(G, Tbl, A, pb, px, py, weak=True)[0]
        dm = GA.pareto_dominated(u); nh = GA.is_nash(j, int(t1[k]), int(t2[k]))
        p = pi[k]; dv['covered'] += p
        dv['stable'] += p * gs; dv['weak'] += p * gw; dv['dominated'] += p * dm; dv['dominated_stable'] += p * (dm and gs)
        dv['dominated_weak'] += p * (dm and gw); dv['nash'] += p * nh; dv['nash_stable'] += p * (nh and gs)
        if dm and gs and len(ex_dom) < 5:
            ex_dom.append(dict(pi=float(p), state=state_name(G, pb, px, py), play=U.joint_name(j)))
    dv['dominated_stable_examples'] = ex_dom
    out['device'] = {k: (float(v) if not isinstance(v, list) else v) for k, v in dv.items()}
    # cut diagnostic: leaving flow by source summary
    src, dst, pr, out_t = ch.rows(codes, codes, ch.lpi, 0.0, mode=1)[:4]
    cutf = np.zeros(7)
    np.add.at(cutf, sm[src], np.exp(pr))
    tot = float(pi @ out_t)
    out['cut_by_source'] = {U.SUMM[k]: float(cutf[k] / tot) if tot > 0 else None for k in range(7) if cutf[k] > 0}
    out['cut_total_rel'] = float(cutf.sum() / tot) if tot > 0 else None
    if out['cut_total_rel'] and out['cut_total_rel'] > 0.02:
        # first-order correction of the fair share: explored exit from fair to non-fair vs dropped flow from fair
        s0, d0, p0 = ch.src, ch.dst_idx, ch.pr
        fairm = sm == 0
        E = float(np.sum(np.exp(ch.lpi[s0] + p0)[fairm[s0] & ~fairm[d0]]))
        Cf = float(cutf[0])
        out['fair_cut_corrected'] = float(out['summary']['fair'] * E / (E + Cf)) if E + Cf > 0 else None
        out['fair_explored_exit'] = E; out['fair_cut_exit'] = Cf
    return out


def execution_stats(G, A, Tbl, ch, reps, pi, js, t1, t2):
    """on-path execution of threat-type genes and base commitments over the explored chain (notes §1.16)."""
    acc = {k: dict(carrier=0.0, executed=0.0, cost=0.0, pay_c=0.0, pay_n=0.0, mass_n=0.0) for k in ('whack', 'quorum strike', 'costly strike')}
    for k, (b, x, y) in enumerate(reps):
        pb, px, py = int(ch.Un['repB'][b]), int(ch.Un['repW'][x]), int(ch.Un['repW'][y])
        j = int(js[k]); bi = j // 4; si, h = bi // 3, bi % 3; a = ((j // 2) % 2, j % 2); tg = (int(t1[k]), int(t2[k]))
        u = GA.PAY[j, tg[0], tg[1]]; p = pi[k]
        # whack (boss)
        car = G.bh[pb] in (0, 2) or any(G.bov[pb, i] in (3, 5) for i in range(G.bng[pb]))
        nwh = sum(int((h == 0 and a[i]) or (h == 2 and tg[i])) for i in range(2))
        r = acc['whack']
        if car:
            r['carrier'] += p; r['pay_c'] += p * u[0]
            if nwh:
                r['executed'] += p; r['cost'] += p * GA.C_WHACK * nwh
        else:
            r['mass_n'] += p; r['pay_n'] += p * u[0]
        for i, xx in ((0, px), (1, py)):
            other = a[1 - i]
            for key in ('quorum strike', 'costly strike'):
                r = acc[key]
                if key == 'quorum strike':
                    car = G.wq[xx] == 1 or any(G.wtr[xx, q] == 7 and G.wov[xx, q] == 1 for q in range(G.wng[xx]))
                    ex = a[i] == 1 and other == 1 and si <= 1
                    cost = U.WAGES[si] + (1.0 if (h == 0 or (h == 2 and tg[i])) else 0.0)
                else:
                    car = G.wt[xx] >= 1 or any(G.wov[xx, q] == 1 for q in range(G.wng[xx]))
                    ex = a[i] == 1 and si >= 1
                    cost = U.WAGES[si] + (1.0 if (h == 0 or (h == 2 and tg[i])) else 0.0)
                if car:
                    r['carrier'] += 0.5 * p; r['pay_c'] += 0.5 * p * u[1 + i]
                    if ex:
                        r['executed'] += 0.5 * p; r['cost'] += 0.5 * p * cost
                else:
                    r['mass_n'] += 0.5 * p; r['pay_n'] += 0.5 * p * u[1 + i]
    out = {}
    for key, r in acc.items():
        out[key] = dict(carrier_mass=r['carrier'], execution_rate=(r['executed'] / r['carrier']) if r['carrier'] > 0 else None,
                        executed_mass=r['executed'], cost_per_execution=(r['cost'] / r['executed']) if r['executed'] > 0 else None,
                        carrier_mean_payoff=(r['pay_c'] / r['carrier']) if r['carrier'] > 0 else None,
                        noncarrier_mean_payoff=(r['pay_n'] / r['mass_n']) if r['mass_n'] > 0 else None)
    return out


def sg_diag(ch, G, A, Tbl, top=8):
    """SG's targeted proposals at the top states (program level, notes §1.10)."""
    pi = ch.pi; order = np.argsort(-pi)
    rec = []
    for k in order[:top]:
        b, x, y = ch.decode(int(ch.codes[k]))
        pb, px, py = int(ch.Un['repB'][b]), int(ch.Un['repW'][x]), int(ch.Un['repW'][y])
        P = GA.sg_proposals(G, Tbl, A, pb, px, py)
        rec.append(dict(pi=float(pi[k]), state=state_name(G, pb, px, py), proposals=P,
                        strict=sum(1 for v in P.values() for p in v if p['kind'] == 'strict'),
                        strict_whack=[p['gene'] for p in P['B'] if p['kind'] == 'strict' and p['whack']],
                        conservative_whack=[p['gene'] for p in P['B'] if p['kind'] == 'conservative' and p['whack']]))
    return rec


def run_cell(arm_name, kernel, prior, N, theta=1e-9, save=True):
    t0 = time.time()
    G, A, Tbl, L, Un, QSc, mB, mW = build_cell(arm_name, kernel, prior)
    if prior == 'uniform':
        # notes §1.17: the named-catalogue uniform prior is diffuse; the full state space is solved exactly
        ch = GA.FullChain(L, Un, QSc, KERNELS[kernel], N, tag='%s/%s/%s' % (arm_name, kernel, prior))
        seeds, ne = seeds_for(ch, G, A, L, Un)
        ch.solve_full()
    else:
        ch = GA.GChain(L, Un, QSc, KERNELS[kernel], N, theta=theta, tag='%s/%s/%s' % (arm_name, kernel, prior),
                       max_states=int(os.environ.get('GA_MAX_STATES', 400000)), verbose=bool(os.environ.get('GA_VERBOSE')))
        ch.max_rounds = int(os.environ.get('GA_MAX_ROUNDS', 60))
        seeds, ne = seeds_for(ch, G, A, L, Un)
        ch.explore_hybrid(seeds)
    res = dict(arm=arm_name, kernel=kernel, prior=prior, N=N, theta=theta, rule=A['rule'],
               caps=dict(max_states=getattr(ch, 'max_states', None), max_rounds=getattr(ch, 'max_rounds', None)), KcB=L['KcB'], KcW=L['KcW'],
               KuB=Un['KuB'], KuW=Un['KuW'], seeds=len(seeds), strict_ne=len(ne),
               strict_ne_states=[state_name(G, int(A['bsel'][L['repB'][b]]), int(A['wsel'][L['repW'][x]]), int(A['wsel'][L['repW'][y]])) for (b, x, y) in ne[:10]],
               null_mass=dict(boss=float(1 - mB[A['bsel']].sum()), worker=float(1 - mW[A['wsel']].sum())),
               explore_log=ch.log)
    res.update(analyse_cell(ch, G, A, Tbl))
    if kernel != 'prior':
        res['sg_diag'] = sg_diag(ch, G, A, Tbl)
    res['time_s'] = time.time() - t0
    if save:
        jdump(res, 'cell_%s_%s_%s_N%d.json' % (arm_name, kernel, prior, N))
    print('%s %s %s N=%g: fair %.4f int %.4f zero %.4f | states %d cut %.3g | %.0fs' % (
        arm_name, kernel, prior, N, res['summary']['fair'], res['summary']['intermediate'], res['summary']['zero wage'],
        res['states'], res['cut_total_rel'] or 0, res['time_s']), flush=True)
    return res


SOG_ARMS = ['base-CC', 'base-RC', 'base-RR', 'G-all', 'G-all-RC', 'G-cred', 'G-cred-ctl', 'G-cred-whole',
            'G-cred-whole-ctl', 'G-asym', 'G-asym-ctl', 'G-recip', 'G-recip-ctl', 'random']


def planned_cells():
    cells = []
    for prior in ('uniform', 'length'):
        for N in (1000, 10000):
            for a in SOG_ARMS:
                cells.append((a, 'prior', prior, N))
            for a in ('G-all', 'G-cred', 'G-cred-whole'):
                for k in ('SG', 'local'):
                    cells.append((a, k, prior, N))
    return cells


def _cell_job(args):
    try:
        return run_cell(*args)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return dict(error=repr(e), cell=args)


def run_cells(procs, only=None):
    from multiprocessing import Pool
    cells = [c for c in planned_cells() if not os.path.exists(os.path.join(OUT, 'cell_%s_%s_%s_N%d.json' % c))]
    if only:
        cells = [c for c in cells if c[0] in only]
    print('%d cells to run' % len(cells), flush=True)
    # warm the caches (tables, filter) before forking
    the_filter(); [tables(r) for r in ('CC', 'RC', 'RR')]
    with Pool(procs) as pl:
        for r in pl.imap_unordered(_cell_job, cells, chunksize=1):
            pass


# ------------------------------------------------------------------ static tables
def static():
    G = sog(); F = the_filter()
    res = dict(cap=CAP, programs=dict(workers=G.KW, bosses=G.KB))
    res['filter'] = F
    res['filter_summary'] = dict(
        worker_admitted=[F['worker'][g]['name'] for g in range(GA.NWG) if F['worker'][g]['admitted']],
        boss_admitted=[F['boss'][g]['name'] for g in range(GA.NBG) if F['boss'][g]['admitted']],
        vacuous=[F[r][g]['name'] for r in ('worker', 'boss') for g in F[r] if F[r][g].get('vacuous')])
    named_genes = {'whack w1': ('boss', GA.bgene(0, 3)), 'whack w2': ('boss', GA.bgene(1, 3)), 'quorum q': ('worker', GA.wgene(7, 1)),
                   'probe concession pi': ('boss', GA.bgene(4, 2)), 'de-escalation': ('boss', GA.bgene(0, 4)),
                   'threat accommodation': ('worker', GA.wgene(3, 0))}
    res['named_gene_verdicts'] = {k: dict(F[r][g], role=r) for k, (r, g) in named_genes.items()}
    # admitted-only iteration
    mB, mW = GA.priors(G)['length']
    Ak = (np.array([F['worker'][g]['admitted'] for g in range(GA.NWG)]), np.array([F['boss'][g]['admitted'] for g in range(GA.NBG)]))
    hist = [(Ak[0].sum(), Ak[1].sum())]
    seen = {(Ak[0].tobytes(), Ak[1].tobytes())}
    status = 'converged'
    for it in range(20):
        wsel = np.array([x for x, (bi, gl) in enumerate(G.wprog) if all(Ak[0][g] for g in gl)])
        bsel = np.array([b for b, (bi, gl) in enumerate(G.bprog) if all(Ak[1][g] for g in gl)])
        F2 = GA.filter_genes(G, tables('CC'), mB, mW, wsel=wsel, bsel=bsel)
        # genes absent from the admitted catalogue are tested as if admitted: they are judged against the admitted catalogue
        nw = np.array([F2['worker'][g]['admitted'] for g in range(GA.NWG)]); nb = np.array([F2['boss'][g]['admitted'] for g in range(GA.NBG)])
        # carriers of a removed gene are absent, so the gene is vacuous in F2; judge it against the admitted catalogue
        for g in range(GA.NWG):
            if not Ak[0][g]:
                Fx = GA.filter_genes(G, tables('CC'), mB, mW, wsel=np.union1d(wsel, [x for x, (bi, gl) in enumerate(G.wprog) if gl == (g,)]), bsel=bsel)
                nw[g] = Fx['worker'][g]['admitted'] and not Fx['worker'][g]['vacuous']
        for g in range(GA.NBG):
            if not Ak[1][g]:
                Fx = GA.filter_genes(G, tables('CC'), mB, mW, wsel=wsel, bsel=np.union1d(bsel, [b for b, (bi, gl) in enumerate(G.bprog) if gl == (g,)]))
                nb[g] = Fx['boss'][g]['admitted'] and not Fx['boss'][g]['vacuous']
        key = (nw.tobytes(), nb.tobytes())
        hist.append((int(nw.sum()), int(nb.sum())))
        if np.array_equal(nw, Ak[0]) and np.array_equal(nb, Ak[1]):
            break
        if key in seen:
            status = 'cycle'; Ak = (nw, nb); break
        seen.add(key); Ak = (nw, nb)
    res['admitted_only'] = dict(status=status, history=[list(map(int, h)) for h in hist],
                                changed_vs_frozen=[GA.wgene_name(g) for g in range(GA.NWG) if Ak[0][g] != F['worker'][g]['admitted']] +
                                [GA.bgene_name(g) for g in range(GA.NBG) if Ak[1][g] != F['boss'][g]['admitted']])
    # arms: composition and class counts
    arms = {}
    for a in SOG_ARMS:
        A = arm(a); Tbl = tables(A['rule'])
        for prior in ('length', 'uniform'):
            mB, mW = masses(A, prior)
            bsel = A['bsel'][mB[A['bsel']] > 0]; wsel = A['wsel'][mW[A['wsel']] > 0]
            if prior == 'length':
                L = GA.lump(Tbl['J'], G.tag, bsel, wsel, mB[bsel], mW[wsel])
                Ur = GA.make_units(G, L, dict(A, bsel=bsel, wsel=wsel), mB, mW, refine=True)
                arms[a] = dict(rule=A['rule'], genes_w=int(A['gw'].sum()), genes_b=int(A['gb'].sum()), programs_b=len(bsel), programs_w=len(wsel),
                               classes_b=L['KcB'], classes_w=L['KcW'], refined_b=Ur['KuB'], refined_w=Ur['KuW'])
            arms[a]['mass_kept_%s' % prior] = dict(boss=float(mB[bsel].sum()), worker=float(mW[wsel].sum()))
    res['arms'] = arms
    res['random_removal'] = dict(worker=[GA.wgene_name(g) for g in range(GA.NWG) if arm('random')['gw'][g]],
                                 boss=[GA.bgene_name(g) for g in range(GA.NBG) if arm('random')['gb'][g]])
    # encoding invariance
    enc = {}
    pairs = {'quorum q on scab vs union base': ('w', G.find_w((0, 0), (GA.wgene(7, 1),)), G.find_w((0, 1))),
             'probe concession on (0,none,0) vs D0': ('b', G.find_b((0, 1, 0), (GA.bgene(4, 2),)), G.find_b((0, 1, 1))),
             'whack w1 on (0,none,0) vs (0,strike,0)': ('b', G.find_b((0, 1, 0), (GA.bgene(0, 3),)), G.find_b((0, 0, 0))),
             'whack w1 on (1/2,none,0) vs (1/2,strike,0)': ('b', G.find_b((2, 1, 0), (GA.bgene(0, 3),)), G.find_b((2, 0, 0)))}
    mB, mW = GA.priors(G)['length']
    for k, (r, p1, p2) in pairs.items():
        row = {}
        for rule in ('CC', 'RR'):
            J = tables(rule)['J']
            if r == 'w':
                d1 = (J[:, p1, :] != J[:, p2, :]); d2 = (J[:, :, p1] != J[:, :, p2])
                m = mB[:, None] * mW[None, :]
                row[rule] = dict(diff_mass_W1=float(m[d1].sum() / m.sum()), diff_mass_W2=float(m[d2].sum() / m.sum()),
                                 tag_equal=bool(G.tag[p1] == G.tag[p2]))
            else:
                d = J[p1] != J[p2]
                m = mW[:, None] * mW[None, :]
                row[rule] = dict(diff_mass=float(m[d].sum() / m.sum()))
        enc[k] = row
    res['encoding_invariance'] = enc
    # named states under each arm
    NP = named_progs()
    nst = {}
    for k, (b, x, y) in NP.items():
        row = {}
        for a in ('G-all', 'G-cred', 'G-cred-whole', 'G-asym', 'G-recip'):
            A = arm(a); Tbl = tables(A['rule'])
            j = int(Tbl['J'][b, x, y]); u = GA.PAY[j, G.tag[x], G.tag[y]]
            gs, wit = GA.gene_stable(G, Tbl, A, b, x, y); gw, witw = GA.gene_stable(G, Tbl, A, b, x, y, weak=True)
            row[a] = dict(play=U.joint_name(j), pay=[float(v) for v in u], nash=bool(GA.is_nash(j, G.tag[x], G.tag[y])),
                          pareto_dominated=bool(GA.pareto_dominated(u)), gene_stable=bool(gs), witness=wit, weak_gene_stable=bool(gw), weak_witness=witw)
        nst[k] = dict(state=state_name(G, b, x, y), arms=row)
    res['named_states'] = nst
    # global scan: gene-stable program triples per arm (strict and weak), Nash and Pareto cross-tab
    ADDB, ADDW = GA.add_tables(G)
    scan = {}
    for a in ('G-all', 'G-cred', 'G-cred-whole', 'G-asym', 'G-recip', 'G-recip-ctl'):
        A = arm(a); Tbl = tables(A['rule'])
        inB = np.zeros(G.KB, bool); inB[A['bsel']] = True; inW = np.zeros(G.KW, bool); inW[A['wsel']] = True
        mBl, mWl = GA.priors(G)['length']
        out_a = {}
        for weak in (0, 1):
            st = np.zeros((len(A['bsel']), len(A['wsel']), len(A['wsel'])), np.int8)
            GA._scan_gene_stable(Tbl['J'], GA.PAY, G.tag, A['bsel'], A['wsel'], inB, inW, ADDB, ADDW, A['gb'], A['gw'], weak, st)
            Js = Tbl['J'][np.ix_(A['bsel'], A['wsel'], A['wsel'])].astype(np.int64)
            T1 = np.broadcast_to(G.tag[A['wsel']][None, :, None], Js.shape); T2 = np.broadcast_to(G.tag[A['wsel']][None, None, :], Js.shape)
            P = GA.PAY[Js, T1, T2]
            dom = np.zeros(Js.shape, bool)
            for f in GA.FRONTIER:
                dom |= (f[None, None, None, :] >= P - 1e-12).all(-1) & (f[None, None, None, :] > P + 1e-12).any(-1)
            nashm = nash_mask(Js, T1, T2)
            stab = st == 1
            wm = mBl[A['bsel']][:, None, None] * mWl[A['wsel']][None, :, None] * mWl[A['wsel']][None, None, :]
            d = dict(triples=int(stab.size), stable=int(stab.sum()), stable_mass=float(wm[stab].sum() / wm.sum()),
                     stable_nash=int((stab & nashm).sum()), stable_not_nash=int((stab & ~nashm).sum()),
                     nash_not_stable=int((~stab & nashm).sum()), stable_dominated=int((stab & dom).sum()),
                     stable_dominated_mass=float(wm[stab & dom].sum() / wm.sum()))
            # wage composition of stable states
            wi = (Js // 4) // 3
            d['stable_by_wage'] = {U.WNAME[s]: int((stab & (wi == s)).sum()) for s in range(3)}
            ex = []
            if (stab & dom).any():
                idx = np.argsort(-np.where(stab & dom, wm, -1).ravel())[:6]
                for f in idx:
                    i, k, l = np.unravel_index(f, Js.shape)
                    b, x, y = int(A['bsel'][i]), int(A['wsel'][k]), int(A['wsel'][l])
                    mv = GA.gene_moves(G, Tbl, A, b, x, y)[2]
                    leave = [m for m in mv if m['du'] >= -1e-12 and any(m['u'][q] > GA.PAY[int(Js[i, k, l]), G.tag[x], G.tag[y]][q] + 1e-12 for q in range(3))]
                    ex.append(dict(state=state_name(G, b, x, y), play=U.joint_name(int(Js[i, k, l])), mass=float(wm[i, k, l] / wm.sum()),
                                   leaving_genes=[(m['slot'], m['gene'], m['du'], m['play']) for m in leave[:4]]))
            d['dominated_examples'] = ex
            out_a['weak' if weak else 'strict'] = d
        scan[a] = out_a
    res['gene_stable_scan'] = scan
    # SG proposals on hand states
    res['sg_hand'] = {k: GA.sg_proposals(G, tables(arm(a)['rule']), arm(a), *NP[k]) for k, a in (('Z_D0', 'G-all'), ('Z', 'G-all'), ('S', 'G-all'), ('F', 'G-cred-whole'))}
    jdump(res, 'static.json')
    return res


def nash_mask(Js, T1, T2):
    b = Js // 4; a1 = (Js // 2) % 2; a2 = Js % 2
    u = GA.PAY[Js, T1, T2]
    ok = np.ones(Js.shape, bool)
    for b2 in range(9):
        ok &= GA.PAY[4 * b2 + 2 * a1 + a2, T1, T2, 0] <= u[..., 0] + 1e-12
    ok &= GA.PAY[4 * b + 2 * (1 - a1) + a2, T1, T2, 1] <= u[..., 1] + 1e-12
    ok &= GA.PAY[4 * b + 2 * a1 + (1 - a2), T1, T2, 2] <= u[..., 2] + 1e-12
    return ok


# ------------------------------------------------------------------ chicken
CH_ARMS = ['const', 'base', 'G-all', 'G-cred', 'G-cred-ctl', 'random']


def chicken_units(C, A, refine):
    sel = A['sel']
    key = {}
    cls = np.empty(len(sel), np.int64)
    for k, a in enumerate(sel):
        kk = (C.A[a, sel].tobytes(), C.A[sel, a].tobytes())
        cls[k] = key.setdefault(kk, len(key))
    if refine:
        un = np.empty(len(sel), np.int64)
        un2 = {}
        for k, a in enumerate(sel):
            bi, gl = C.prog[a]
            un[k] = un2.setdefault((int(cls[k]), bi, gl[:1] if len(gl) == 2 else gl), len(un2))
        return cls, un
    return cls, cls.copy()


def chicken_cell(C, A, prior, kernel, N, mu_prog):
    sel = A['sel']
    cls, un = chicken_units(C, A, kernel != 'prior')
    K = int(un.max() + 1)
    rep = np.full(K, -1, np.int64)
    for k in np.argsort(-mu_prog[sel], kind='stable'):
        if rep[un[k]] < 0: rep[un[k]] = sel[k]
    Uc = C.U[np.ix_(rep, rep)]
    mu = np.bincount(un, weights=mu_prog[sel], minlength=K)
    with np.errstate(divide='ignore'):
        lmu = np.log(mu)
    pos = {int(a): int(un[k]) for k, a in enumerate(sel)}
    local = None
    if kernel != 'prior':
        adm = [g for g in range(GA.NCG) if A['ga'][g]]

        def local(a, b, role):
            r = rep[a] if role == 0 else rep[b]
            opp = rep[b] if role == 0 else rep[a]
            if kernel == 'local':
                ms = [pos.get(C.add_gene(int(r), g), -1) for g in adm]
                ms = [m for m in ms if m >= 0]
                return [(m, -math.log(len(adm))) for m in ms] if adm else []
            # SG: triggers true in the stable play: the opponent's stable action
            them = C.B[r, opp] if role == 0 else C.A[opp, r]
            out = []
            ntrue = 0
            mine = C.A[r, opp] if role == 0 else C.B[opp, r]
            for t in (0, 1):
                if them != t:
                    continue
                best = None
                for o in (0, 1):
                    g = 2 * t + o
                    if g not in adm: continue
                    m = C.add_gene(int(r), g)
                    if m < 0 or m not in pos: continue
                    u = C.U[m, opp] if role == 0 else C.U[m, opp]
                    cons = o == mine
                    if best is None or u > best[0] + 1e-12 or (abs(u - best[0]) <= 1e-12 and cons and not best[1]):
                        best = (u, cons, pos[m])
                if best is not None:
                    ntrue += 1; out.append(best[2])
            return [(m, -math.log(ntrue)) for m in out]
    lpi, LA = GA.chicken_chain_dense(Uc, lmu, lmu, N, local=local)
    pi = np.exp(lpi)
    acts = C.A[np.ix_(rep, rep)]; acts2 = C.B[np.ix_(rep, rep)]
    lab = np.where((acts == 0) & (acts2 == 1), 'R1', np.where((acts == 1) & (acts2 == 0), 'R2', np.where(acts == 0, 'crash', 'dove')))
    res = dict(K=K, summary={k: float(pi[lab == k].sum()) for k in ('R1', 'R2', 'crash', 'dove')})
    order = np.argsort(-pi.ravel())[:8]
    res['support'] = [dict(pi=float(pi.ravel()[f]), state='%s | %s' % (C.name(rep[f // K]), C.name(rep[f % K])), label=str(lab.ravel()[f])) for f in order]
    # exits of the top state
    f = int(order[0]); row = LA[f]
    ex = np.argsort(-row)[:5]
    res['top_exits'] = [dict(rate=float(np.exp(row[d])), to='%s | %s' % (C.name(rep[d // K]), C.name(rep[d % K])), label=str(lab.ravel()[d]),
                             delta=float((Uc[d // K, f % K] - Uc[f // K, f % K]) if d % K == f % K else (Uc[d % K, f // K] - Uc[f % K, f // K])))
                        for d in ex if np.isfinite(row[d])]
    res['exit_total_top'] = float(np.exp(np.logaddexp.reduce(row[np.isfinite(row)])))
    return res


def chicken_lottery(C, A, mu_prog, mN, runs=40, N=100, I=64, gens=4000, seed0=20261011):
    import fixed_role_chicken as FR
    sel = A['sel']
    cls, un = chicken_units(C, A, False)
    K = int(un.max() + 1)
    rep = np.full(K, -1, np.int64)
    for k in np.argsort(-mu_prog[sel], kind='stable'):
        if rep[un[k]] < 0: rep[un[k]] = sel[k]
    Uc = np.ascontiguousarray(C.U[np.ix_(rep, rep)])
    mu = np.bincount(un, weights=mu_prog[sel], minlength=K); mu /= mu.sum()
    acts = C.A[np.ix_(rep, rep)]
    S = (acts == 1).astype(float)          # S[a, b] = P(a swerves vs b) (deterministic)
    Jp = FR.joint(S)
    est = []; patch = []; split = []
    for r in range(runs):
        rng = np.random.default_rng([seed0, int(mN * 10), r, zlib.crc32(A['name'].encode()) % 100000])
        init = np.zeros((I, 2, K), np.int64)
        for i in range(I):
            init[i, 0] = rng.multinomial(N, mu); init[i, 1] = rng.multinomial(N, mu)
        snap, ns, stop_g = FR.sim_two_pop(Uc, Uc, init, N, FR.W, mN / N, gens if mN > 0 else 2000, 50, int(rng.integers(2 ** 31 - 1)), 0, 1)
        X = snap[ns - 1].astype(float) / N
        J = np.einsum('ia,ib,abk->ik', X[:, 0], X[:, 1], Jp)
        lab = FR.classify(J)
        est.append(float(np.isin(lab, (FR.R1, FR.R2)).mean()))
        r1 = (lab == FR.R1).sum(); r2 = (lab == FR.R2).sum()
        split.append(float(r1 / max(r1 + r2, 1)))
        patch.append(bool(r1 > 0 and r2 > 0))
    return dict(mN=mN, runs=runs, per_island_establishment=float(np.mean(est)), est_run_sd=float(np.std(est)),
                role1_share=float(np.mean(split)), patchwork_runs=float(np.mean(patch)))


def chicken():
    C = GA.Chicken(2)
    assert (C.B == C.A.T).all()
    F = C.filter()
    mu_len = GA.length_prior(C.size); mu_uni = np.ones(C.K) / C.K
    res = dict(programs=C.K, filter=F)
    # named states
    nm = {'R1 (St,0)|(Sw,0)': (C.index[(0, ())], C.index[(1, ())]), "R1' (St,1)|(Sw,0)": (C.index[(2, ())], C.index[(1, ())]),
          'crash': (C.index[(0, ())], C.index[(0, ())]), 'dove': (C.index[(1, ())], C.index[(1, ())])}
    nst = {}
    for k, (a, b) in nm.items():
        row = {}
        for an in ('G-all', 'G-cred'):
            A = GA.chicken_arm(C, an, F)
            adm = [g for g in range(GA.NCG) if A['ga'][g]]
            moves = []
            for role, r, opp in ((0, a, b), (1, b, a)):
                u0 = C.U[r, opp]
                for g in adm:
                    m = C.add_gene(r, g)
                    if m < 0 or m == r: continue
                    moves.append((role + 1, GA.cgene_name(g), float(C.U[m, opp] - u0)))
            strict = [mv for mv in moves if mv[2] > 1e-12]
            row[an] = dict(gene_stable=not strict, witness=strict[:2], play=(int(C.A[a, b]), int(C.B[a, b])))
        nst[k] = row
    res['named_states'] = nst
    # encoding invariance: firm gene on (St,1) vs (St,0)
    p1, p2 = C.index[(2, (0,))], C.index[(0, ())]      # (St,1) + firm vs (St,0)
    res['encoding_firm'] = dict(play_identical=bool((C.A[p1] == C.A[p2]).all() and (C.A[:, p1] == C.A[:, p2]).all()))
    cells = {}
    for an in CH_ARMS:
        A = GA.chicken_arm(C, an, F)
        for prior, mu in (('length', mu_len), ('uniform', mu_uni)):
            m = mu.copy()
            if an in ('const', 'base'):
                m = np.zeros(C.K); m[A['sel']] = (GA.length_prior(C.size[A['sel']]) if prior == 'length' else 1.0 / len(A['sel']))
            for N in (1000, 10000):
                for kernel in (('prior', 'SG', 'local') if an in ('G-all', 'G-cred') else ('prior',)):
                    t0 = time.time()
                    r = chicken_cell(C, A, prior, kernel, N, m)
                    r['time_s'] = time.time() - t0
                    cells['%s/%s/%s/%d' % (an, kernel, prior, N)] = r
                    print('chicken', an, kernel, prior, N, r['summary'], '%.0fs' % r['time_s'], flush=True)
            if prior == 'length':
                for mN in (0, 1):
                    r = chicken_lottery(C, A, m, mN)
                    cells['lottery/%s/mN%d' % (an, mN)] = r
                    print('chicken lottery', an, mN, r, flush=True)
    res['cells'] = cells
    jdump(res, 'chicken.json')
    return res


# ------------------------------------------------------------------ SOG lottery
def lottery_cell(arm_name, runs=40, N=100, I=64, mN=1.0, gens=100000, procs=3):
    from multiprocessing import Pool
    jobs = [(arm_name, r, N, I, mN, gens) for r in range(runs)]
    t = time.time()
    with Pool(procs) as pl:
        recs = pl.map(_lottery_job, jobs, chunksize=1)
    out = dict(arm=arm_name, runs=recs, params=dict(N=N, I=I, mN=mN, gens=gens), wall=time.time() - t)
    jdump(out, 'lottery_%s.json' % arm_name)
    return out


def lottery_data(arm_name):
    import sog_lottery as SL
    G = sog(); A = arm(arm_name); Tbl = tables(A['rule'])
    mB, mW = GA.priors(G)['length']
    bsel, wsel = A['bsel'], A['wsel']
    L = GA.lump(Tbl['J'], G.tag, bsel, wsel, mB[bsel], mW[wsel])
    PAYt, T = SL.code_tables(GA.C_WHACK, 0)
    rb = bsel[L['repB']]; rw = wsel[L['repW']]
    LB = np.stack([np.array([G.bh[b] == 0 for b in rb]), np.array([G.bp[b] > 0 or any(G.btr[b, i] >= 4 for i in range(G.bng[b])) for b in rb]),
                   np.array([G.bng[b] > 0 for b in rb])]).astype(np.int64)
    LW = np.stack([np.array([G.wt[x] == 2 for x in rw]), np.array([G.wt[x] == 3 for x in rw]), np.array([G.wng[x] > 0 for x in rw]),
                   np.array([G.tag[x] == 1 for x in rw])]).astype(np.int64)
    pB = L['massB'] / L['massB'].sum(); pW = L['massW'] / L['massW'].sum()
    return L, PAYt, T, LB, LW, pB, pW, rb, rw


def _lottery_job(args):
    import sog_lottery as SL
    import concessions as CO
    arm_name, r, N, I, mN, gens = args
    L, PAYt, T, LB, LW, pB, pW, rb, rw = lottery_data(arm_name)
    G = sog()
    seed = (20261011 + 1009 * (zlib.crc32(arm_name.encode()) % 1000003) + r) % (2 ** 31)
    rng = np.random.default_rng(seed)
    init = SL.init_counts(rng, I, N, pB, pW)
    chk = SL.checks_schedule(gens)
    t0 = time.time()
    status, stop, counts, stats, ts, ff, fnow, nfair, ci = CO.kern_c(
        np.ascontiguousarray(L['Jc']), L['tagc'].astype(np.int64), PAYt, T, SL.KEYT, LB, LW, init, N, SL.W, mN / N,
        seed % (2 ** 31), chk, 1000)
    fin = stats[ci - 1]
    lab = [int(np.argmax(fin[i, :7])) for i in range(I)]
    nlb = LB.shape[0]
    gl = chk[:ci].astype(float); wts = np.diff(np.concatenate([[0.0], gl]))
    st = stats[:ci]
    pos_str = sum(n * st[:, :, 7 + 3 * si + n] for si in (1, 2) for n in (1, 2))
    zero_str = sum(n * st[:, :, 7 + n] for n in (1, 2))
    tavg = lambda arr: float((arr.mean(1) * wts).sum() / wts.sum())
    trajectory = dict(whacks_per_encounter=tavg(st[:, :, 23]), strikes_pos_wage_per_encounter=tavg(pos_str),
                      strikes_zero_wage_per_encounter=tavg(zero_str), first100_whacks=float(st[:100, :, 23].mean()))
    maj = Counter(state_name(G, int(rb[int(np.argmax(counts[i, 0]))]), int(rw[int(np.argmax(counts[i, 1]))]), int(rw[int(np.argmax(counts[i, 2]))])) for i in range(I))
    return dict(run=r, seed=int(seed), status=int(status), stop_gen=int(stop), first_fair=[int(v) for v in ff],
                fair_final=[int(v) for v in fnow], label=lab, label_counts=dict(Counter(U.SUMM[k] for k in lab)),
                strike_whacker_share_final=float(fin[:, 27].mean()), probe_share_final=float(fin[:, 28].mean()),
                whacker_ts={str(g): float(ts[g][:, 1].mean()) for g in (0, 10, 25, 50, 100, 500, 1000) if g < ts.shape[0]},
                majority=maj.most_common(3), trajectory=trajectory, wall=time.time() - t0)


# ------------------------------------------------------------------ coalition kernel
def two_slot_fixation(f1, f2, N, w=GA.W):
    """exact two-slot Moran: f1(k2)[m] -> (payoff of a slot-1 mutant, of a slot-1 resident) given the slot-2 mutant
    count k2; f2(k1) likewise.  Each step picks one of the two slots uniformly.  Returns P(both fix | (1, 1))."""
    import scipy.sparse as sp, scipy.sparse.linalg as spla

    def one_d(fm, fr, k0):
        # constant selection in one slot: fixation from k0 copies with fitness ratio r = e^{w (fm - fr)}
        r = math.exp(w * (fm - fr))
        if abs(r - 1) < 1e-12:
            return k0 / N
        return (1 - r ** (-k0)) / (1 - r ** (-N))
    n = N - 1
    idx = lambda a, b: (a - 1) * n + (b - 1)
    rows = []; cols = []; vals = []; rhs = np.zeros(n * n)
    for a in range(1, N):
        for b in range(1, N):
            i = idx(a, b)
            fm1, fr1 = f1(b); fm2, fr2 = f2(a)
            e1m, e1r = math.exp(w * fm1), math.exp(w * fr1)
            up1 = a * e1m / (a * e1m + (N - a) * e1r) * (N - a) / N
            dn1 = (N - a) * e1r / (a * e1m + (N - a) * e1r) * a / N
            e2m, e2r = math.exp(w * fm2), math.exp(w * fr2)
            up2 = b * e2m / (b * e2m + (N - b) * e2r) * (N - b) / N
            dn2 = (N - b) * e2r / (b * e2m + (N - b) * e2r) * b / N
            stay = 1 - 0.5 * (up1 + dn1 + up2 + dn2)
            rows.append(i); cols.append(i); vals.append(1 - stay)
            for (aa, bb, p) in ((a + 1, b, 0.5 * up1), (a - 1, b, 0.5 * dn1), (a, b + 1, 0.5 * up2), (a, b - 1, 0.5 * dn2)):
                if p == 0: continue
                if 1 <= aa <= N - 1 and 1 <= bb <= N - 1:
                    rows.append(i); cols.append(idx(aa, bb)); vals.append(-p)
                else:
                    if aa == 0 or bb == 0:
                        v = 0.0
                    elif aa == N:
                        fm, fr = f2(N); v = one_d(fm, fr, bb)
                    else:
                        fm, fr = f1(N); v = one_d(fm, fr, aa)
                    rhs[i] += p * v
    M = sp.csr_matrix((vals, (rows, cols)), shape=(n * n, n * n))
    h = spla.spsolve(M.tocsc(), rhs)
    return float(h[idx(1, 1)])


def coalition():
    """the coalition kernel cell (labelled): at the zero-wage named states, two worker mutants enter simultaneously;
    exact two-slot fixation at N = 100, 1000; compared with the sequential neutral path; threshold eps*."""
    G = sog()
    out = {}
    for arm_name in ('G-all', 'G-cred-whole'):
        A = arm(arm_name); Tbl = tables(A['rule']); J = Tbl['J']
        mB, mW = GA.priors(G)['length']
        for st in ('Z', 'Z_D0'):
            b, x0, y0 = named_progs()[st]
            # candidate coalitions: every pair of worker programs (q1, q2) after which the boss has a strict exit to a
            # higher-wage play; keep the heaviest by mu(q1) mu(q2)
            u0 = GA.PAY[int(J[b, x0, y0]), G.tag[x0], G.tag[y0]]
            best = []
            Wl = A['wsel']
            for q1 in Wl:
                for q2 in Wl:
                    j = int(J[b, q1, q2]); u = GA.PAY[j, G.tag[q1], G.tag[q2]]
                    # boss's best strict response among its programs
                    bu = GA.PAY[J[A['bsel'], q1, q2].astype(np.int64), G.tag[q1], G.tag[q2], 0]
                    k = int(np.argmax(bu))
                    jb = int(J[A['bsel'][k], q1, q2])
                    if bu[k] > u[0] + 1e-12 and (jb // 4) // 3 > (int(J[b, x0, y0]) // 4) // 3 and (jb % 4) == 0:
                        best.append((mW[q1] * mW[q2], int(q1), int(q2), int(A['bsel'][k])))
            best.sort(reverse=True)
            if not best:
                out['%s/%s' % (arm_name, st)] = dict(coalition=None)
                continue
            m, q1, q2, bnew = best[0]
            # payoff functions for the two-slot process: payoff to a slot-1 mutant / resident given k2 slot-2 mutants
            def pay(s, a, bb):
                j = int(J[b, a, bb]); return GA.PAY[j, G.tag[a], G.tag[bb]][s]
            res = dict(state=st, coalition=(G.wname(q1), G.wname(q2)), mu_product=m, boss_response=G.bname(bnew),
                       pair_play=U.joint_name(int(J[b, q1, q2])))
            seq_single = {}
            for N in (100, 1000):
                f1 = lambda k2, N=N: ((k2 / N) * pay(1, q1, q2) + (1 - k2 / N) * pay(1, q1, y0), (k2 / N) * pay(1, x0, q2) + (1 - k2 / N) * pay(1, x0, y0))
                f2 = lambda k1, N=N: ((k1 / N) * pay(2, q1, q2) + (1 - k1 / N) * pay(2, x0, q2), (k1 / N) * pay(2, q1, y0) + (1 - k1 / N) * pay(2, x0, y0))
                rho2 = two_slot_fixation(f1, f2, N)
                # sequential: q1 first (constant selection against (b, y0)), then q2 against (b, q1)
                r1 = math.exp(GA._lrho(GA.W * (pay(1, q1, y0) - pay(1, x0, y0)), float(N)))
                r2 = math.exp(GA._lrho(GA.W * (pay(2, q1, q2) - pay(2, q1, y0)), float(N)))
                res['N%d' % N] = dict(rho2=rho2, rho2_times_N2=rho2 * N * N, rho_first=r1, rho_second=r2)
            out['%s/%s' % (arm_name, st)] = res
    jdump(out, 'coalition.json')
    return out


# ------------------------------------------------------------------ SG innovation in the lottery (finite-eps object)
def _sg_lottery_job(args):
    arm_name, r, N, I, mN, gens, inn = args
    G, A, Tbl, L, Un, QSc, mB, mW = build_cell(arm_name, 'SG', 'length')
    pB = Un['massB'] / Un['massB'].sum(); pW = Un['massW'] / Un['massW'].sum()
    K = max(Un['KuB'], Un['KuW'])
    rng = np.random.default_rng([20261011, zlib.crc32(arm_name.encode()) % 100000, r])
    init = np.zeros((I, 3, K), np.int64)
    for i in range(I):
        init[i, 0, :Un['KuB']] = rng.multinomial(N, pB); init[i, 1, :Un['KuW']] = rng.multinomial(N, pW); init[i, 2, :Un['KuW']] = rng.multinomial(N, pW)
    cdfB = np.cumsum(np.concatenate([pB, np.zeros(K - Un['KuB'])])); cdfW = np.cumsum(np.concatenate([pW, np.zeros(K - Un['KuW'])]))
    ucB = np.concatenate([Un['ucB'], np.zeros(K - Un['KuB'], np.int64)]); ucW = np.concatenate([Un['ucW'], np.zeros(K - Un['KuW'], np.int64)])
    LOCB = np.vstack([Un['LOCB'], np.full((K - Un['KuB'], GA.NBG), -2, np.int64)]); LOCW = np.vstack([Un['LOCW'], np.full((K - Un['KuW'], GA.NWG), -2, np.int64)])
    t0 = time.time()
    snap, counts, ninn = GA.kern_sg(L['Jc'], L['tagc'], GA.PAY, ucB, ucW, LOCB, LOCW, QSc, cdfB, cdfW, init, N, GA.W, mN / N,
                                    (1.0 / N ** 2) if inn else 0.0, gens, 50, int(rng.integers(2 ** 31 - 1)))
    js = snap[:, :, 3]
    wage = (js // 4) // 3; both = (js % 4) == 0; noh = ~(((js // 4) % 3 == 0) & ((js % 4) != 0))
    fair = (wage == 2) & both; zero = wage == 0; q = (wage == 1) & both
    h = js.shape[0] // 2
    return dict(arm=arm_name, run=r, innovation=bool(inn), innovations=int(ninn), time_s=time.time() - t0,
                fair_end=float(fair[-1].mean()), quarter_end=float(q[-1].mean()), zero_end=float(zero[-1].mean()),
                fair_2nd=float(fair[h:].mean()), quarter_2nd=float(q[h:].mean()), zero_2nd=float(zero[h:].mean()),
                fair_ts=[float(v) for v in fair.mean(1)[::4]])


def sg_lottery(procs, runs=10, N=100, I=16, mN=1.0, gens=2000):
    from multiprocessing import Pool
    jobs = [(a, r, N, I, mN, gens, inn) for a in ('G-all', 'G-cred') for inn in (1, 0) for r in range(runs)]
    with Pool(procs) as pl:
        recs = pl.map(_sg_lottery_job, jobs, chunksize=1)
    out = dict(params=dict(N=N, I=I, mN=mN, gens=gens, runs=runs, u_inn_per_birth=1.0 / N ** 2), runs=recs)
    summ = {}
    for a in ('G-all', 'G-cred'):
        for inn in (True, False):
            rr = [x for x in recs if x['arm'] == a and x['innovation'] == inn]
            summ['%s/%s' % (a, 'SG-innovation' if inn else 'no-innovation')] = {k: float(np.mean([x[k] for x in rr])) for k in
                                                                              ('fair_end', 'quarter_end', 'zero_end', 'fair_2nd', 'quarter_2nd', 'zero_2nd', 'innovations')}
    out['summary'] = summ
    jdump(out, 'lottery_sg.json')
    print(json.dumps(summ, indent=1))
    return out


def coalition_eps():
    """eps* for the coalition kernel: coalition flux / sequential flux = eps * 3 * e_int * rho2 / (rho1 rho2'), with
    e_int the per-event exit probability of the intermediate state (one mutant in) in the length-prior prior-kernel
    chain; computed for the coalition.json pairs."""
    co = json.load(open(os.path.join(OUT, 'coalition.json')))
    G = sog()
    out = {}
    for key, v in co.items():
        if not v.get('coalition'):
            continue
        arm_name, st = key.split('/')
        b, x0, y0 = named_progs()[st]
        q1 = [x for x in range(G.KW) if G.wname(x) == v['coalition'][0]][0]
        q2 = [x for x in range(G.KW) if G.wname(x) == v['coalition'][1]][0]
        G_, A, Tbl, L, Un, QSc, mB, mW = build_cell(arm_name, 'prior', 'length')
        res = {}
        for N in (1000, 10000):
            ch = GA.GChain(L, Un, QSc, 0, float(N))
            if b not in Un['posB'] or q1 not in Un['posW'] or y0 not in Un['posW']:
                res['N%d' % N] = None; continue
            code = ch.code(Un['posB'][b], Un['posW'][q1], Un['posW'][y0])
            src, dst, lp = ch.rows(np.array([code]), np.array([code]), np.zeros(1), 0.0, mode=1)[:3]
            e_int = float(np.exp(lp).sum())
            m1 = Un['massW'][Un['posW'][q1]] / 3; m2 = Un['massW'][Un['posW'][q2]] / 3
            u = lambda bb, x, y, s: GA.PAY[int(Tbl['J'][bb, x, y]), G.tag[x], G.tag[y]][s]
            r1 = math.exp(GA._lrho(GA.W * (u(b, q1, y0, 1) - u(b, x0, y0, 1)), float(N)))
            r2 = math.exp(GA._lrho(GA.W * (u(b, q1, q2, 2) - u(b, q1, y0, 2)), float(N)))
            rho2 = v['N%d' % N]['rho2'] if ('N%d' % N) in v else r1 * r2
            seq = m1 * r1 * (m2 * r2 / e_int)          # per event of single mutations (eps)
            coal = (1.0 / 3) * (3 * m1) * (3 * m2) * rho2   # per eps^2 (a pair of slots w.p. 1/3, masses unscaled)
            res['N%d' % N] = dict(e_int=e_int, seq_per_eps=seq, coal_per_eps2=coal, eps_star=seq / coal)
        out[key] = res
    json.dump(out, open(os.path.join(OUT, 'coalition_eps.json'), 'w'), indent=1)
    print(json.dumps(out, indent=1))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('args', nargs='*')
    ap.add_argument('--procs', type=int, default=3)
    a = ap.parse_args()
    if a.cmd == 'guard':
        jdump(GA.scale_guard(2, npairs=600, nboss=800), 'guard.json')
    elif a.cmd == 'static':
        static()
    elif a.cmd == 'cell':
        run_cell(a.args[0], a.args[1], a.args[2], float(a.args[3]))
    elif a.cmd == 'cells':
        run_cells(a.procs, only=a.args or None)
    elif a.cmd == 'chicken':
        chicken()
    elif a.cmd == 'lottery':
        for an in (a.args or ['G-all', 'G-cred', 'G-asym', 'G-recip']):
            r = lottery_cell(an, procs=a.procs)
            labs = Counter(l for rr in r['runs'] for l in rr['label'])
            print(an, {U.SUMM[k]: v / (64 * 40) for k, v in labs.items()}, flush=True)
    elif a.cmd == 'lottery_sg':
        sg_lottery(a.procs)
    elif a.cmd == 'coalition_eps':
        coalition_eps()
    elif a.cmd == 'coalition':
        print(json.dumps(coalition(), indent=1, default=str))


if __name__ == '__main__':
    main()

