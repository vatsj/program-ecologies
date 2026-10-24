"""Driver for the two-role mixed-action experiment (spec specs/2026-10-23-two-role-mixed.md; notes/mixed2.md;
predictions/2026-10-23-two-role-mixed.md).

    python3 src/mixed2_run.py static                              # tables, audits, validation numbers -> runs/mixed2/static.json
    python3 src/mixed2_run.py chain GAME ARM C [--N 100 1000 10000]
    python3 src/mixed2_run.py lottery GAME ARM C CELL [--runs a b]   # CELL in primary | size
GAME in insp | end; ARM in blind | sample | exact | matched | sr4 | sr16; C the price.  Outputs under runs/mixed2/ (small
json / json.gz only).  Every chain number is an eps -> 0 object (pi over pairs of monomorphic classes); every lottery number
is an eps = 0 finite-(N, I, horizon) statistic.
"""
import argparse, gzip, json, math, os, sys, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mixed2 as M

ROOT = M.ROOT
OUT = os.path.join(ROOT, 'runs', 'mixed2')
os.makedirs(OUT, exist_ok=True)
NMAX = {'insp': 8, 'end': 7}
NS_CHAIN = (100, 1000, 10000)
PRIMARY = dict(N=100, I=64, runs=40, cont=10, gens=2000, cont_gens=10000, m=1.0 / 100)       # mN = 1
SIZE = dict(N=400, I=16, runs=20, cont=0, gens=2000, cont_gens=2000, m=1.0 / 400)


def jdump(obj, path, gz=False):
    def default(o):
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.floating,)): return None if not np.isfinite(o) else float(o)
        if isinstance(o, np.ndarray): return o.tolist()
        if isinstance(o, (np.bool_,)): return bool(o)
        raise TypeError(type(o))
    data = json.dumps(obj, default=default)
    if gz:
        with gzip.open(path, 'wt') as f: f.write(data)
    else:
        with open(path, 'w') as f: f.write(data)


def jload(path):
    if path.endswith('.gz'):
        with gzip.open(path, 'rt') as f: return json.load(f)
    with open(path) as f: return json.load(f)


def log(*a):
    print(*a, flush=True)


# ================================================================ statistics summaries
def summarize(st, game):
    """island means of every scalar statistic, island shares of the conditions the predictions use."""
    out = {}
    for k, v in st.items():
        if k == 'J':
            out['J'] = np.nanmean(v, axis=0).tolist()
        else:
            vv = np.asarray(v, float)
            out[k] = float(np.nanmean(vv)) if np.isfinite(vv).any() else None
    if game == 'insp':
        p = np.nan_to_num(st['p_insp'], nan=0.5); q = np.nan_to_num(st['q_cheat'], nan=0.5)
        out['isl_commit'] = float(np.mean(p > 0.25 + 5e-3))
        out['isl_commit_comply'] = float(np.mean((p > 0.25 + 5e-3) & (q < 0.1)))
        out['isl_lax'] = float(np.mean(p < 0.25 - 5e-3))
        out['isl_reader_majority1'] = float(np.mean(st['rd1'] >= 0.5))
        out['isl_u0_gt_m06'] = float(np.mean(st['u0g'] > -0.6))
        out['isl_efficient'] = float(np.mean((st['u0g'] >= -0.05) & (st['u1g'] >= -0.05)))           # the (N, C) outcome (0, 0)
        out['isl_nashlike'] = float(np.mean((np.abs(p - 0.25) <= 0.1) & (np.abs(q - 0.25) <= 0.1)))
        out['isl_cheat_majority'] = float(np.mean(q > 0.5))
        for qq in (10, 50, 90):
            out['u0g_q%d' % qq] = float(np.percentile(st['u0g'], qq))
    else:
        b = np.nan_to_num(st['bluff'], nan=-9); c = np.nan_to_num(st['call'], nan=-9)
        ob = np.abs(b - 0.25) <= 0.1; oc = np.abs(c - 0.5) <= 0.1
        out['isl_bluff10'] = float(np.mean(ob)); out['isl_call10'] = float(np.mean(oc))
        out['isl_both10'] = float(np.mean(ob & oc)); out['isl_value10'] = float(np.mean(np.abs(st['u0g']) <= 0.1))
        out['isl_all10'] = float(np.mean(ob & oc & (np.abs(st['u0g']) <= 0.1)))
        for qq in (10, 50, 90):
            out['bluff_q%d' % qq] = float(np.percentile(b, qq)); out['call_q%d' % qq] = float(np.percentile(c, qq))
    return out


# ================================================================ chain
def top_pairs(A, m=10):
    o0 = np.argsort(-A.mass[0])[:m]; o1 = np.argsort(-A.mass[1])[:m]
    return [int(a) * A.K[1] + int(b) for a in o0 for b in o1]


def ladder_seeds(A):
    nm = M.named_idx(A)
    pairs = []
    if A.game == 'insp':
        for a, b in (('P38', 'CRC'), ('P38', 'C'), ('N', 'C'), ('N', 'K'), ('I', 'K'), ('I', 'C'), ('X', 'X'), ('P516', 'C'), ('P516', 'CRC'),
                     ('RI', 'C'), ('X', 'C'), ('P14', 'X')):
            if '0:' + a in nm and '1:' + b in nm:
                pairs.append(nm['0:' + a] * A.K[1] + nm['1:' + b])
    else:
        for a, b in (('EQ', 'X'), ('EQ7', 'X'), ('BET', 'CALL'), ('BET', 'FOLD'), ('HON', 'FOLD'), ('HON', 'CALL'), ('XI', 'X'), ('CHECK', 'X'),
                     ('EXP', 'X'), ('EQ', 'CRII'), ('BL', 'X')):
            if '0:' + a in nm and '1:' + b in nm:
                pairs.append(nm['0:' + a] * A.K[1] + nm['1:' + b])
    return pairs


def chain_cell(A, N, classes_info, verbose=False, max_states=1500, max_add=400, full=False):
    t0 = time.time()
    ch = M.TwoPopChain(A, N)
    if full:
        ch.solve_full()
    else:
        seeds = sorted(set(top_pairs(A, 10) + ladder_seeds(A)))
        ch.explore(seeds, log_theta=math.log(1e-10), max_states=max_states, max_add=max_add, verbose=verbose)
    n = len(ch.states)
    lpi = ch.lpi - np.logaddexp.reduce(ch.lpi[np.isfinite(ch.lpi)])
    pi = np.exp(lpi)
    K0, K1 = A.K
    states = np.array(ch.states)
    sa, sb = states // K1, states % K1
    # per-state statistics (one-hot populations, chunked)
    keys = None
    agg = defaultdict(float)
    for lo in range(0, n, 200):
        hi = min(n, lo + 200)
        X0 = np.zeros((hi - lo, K0)); X1 = np.zeros((hi - lo, K1))
        X0[np.arange(hi - lo), sa[lo:hi]] = 1; X1[np.arange(hi - lo), sb[lo:hi]] = 1
        st = M.island_stats(A, X0, X1)
        w = pi[lo:hi]
        for k, v in st.items():
            if k == 'J':
                agg['J'] = agg.get('J', 0.0) + np.tensordot(w, v, axes=(0, 0))
                continue
            vv = np.asarray(v, float)
            ok = np.isfinite(vv)
            agg[k] += float((w * np.where(ok, vv, 0.0)).sum()); agg['_w_' + k] += float((w * ok).sum())
    stat = {}
    for k, v in agg.items():
        if k.startswith('_w_'):
            continue
        if k == 'J':
            stat['J'] = np.asarray(v).tolist(); continue
        wk = agg['_w_' + k]
        stat[k] = v / wk if wk > 0 else None
    # cycle / drift / rest mass (classes of the weakly improving graph over all pairs)
    lab, wcl = classes_info
    kind = {c['label']: c['kind'] for c in wcl}
    mass = defaultdict(float)
    for s, p in zip(ch.states, pi):
        mass[kind.get(int(lab[s]), 'transient')] += p
    # class shares
    sh0 = np.zeros(K0); sh1 = np.zeros(K1)
    np.add.at(sh0, sa, pi); np.add.at(sh1, sb, pi)
    o0 = np.argsort(-sh0)[:12]; o1 = np.argsort(-sh1)[:12]
    order = np.argsort(-pi)[:15]
    cum = np.cumsum(np.sort(pi)[::-1])
    res = dict(N=N, n_states=n, capped=bool(ch.capped), log10_cut=float(ch.log_cut / math.log(10)) if np.isfinite(ch.log_cut) else None,
               log10_unexplored=float(ch.log_unexplored / math.log(10)) if np.isfinite(ch.log_unexplored) else None, circulation=ch.circulation,
               info={k: (v if not isinstance(v, np.ndarray) else v.tolist()) for k, v in ch.info.items()}, full=bool(full),
               stat=stat, pi_cycle=float(mass.get('cycle', 0)), pi_drift=float(mass.get('drift', 0)), pi_rest=float(mass.get('rest', 0)),
               pi_transient=float(mass.get('transient', 0)),
               top_states=[dict(pi=float(pi[i]), s0=A.names[0][sa[i]], s1=A.names[1][sb[i]], kind=kind.get(int(lab[states[i]]), 'transient'),
                                u0g=float(A.UAg[sa[i], sb[i]]), u1g=float(A.UBg[sb[i], sa[i]])) for i in order],
               top0=[(A.names[0][c], float(sh0[c]), int(A.sizes[0][c])) for c in o0 if sh0[c] > 0],
               top1=[(A.names[1][c], float(sh1[c]), int(A.sizes[1][c])) for c in o1 if sh1[c] > 0],
               n_states_for_099=int(np.searchsorted(cum, 0.99) + 1), time_s=time.time() - t0)
    # named class shares under pi and the ladder rates
    nm = M.named_idx(A)
    res['named_share'] = {k: float(sh0[c] if k[0] == '0' else sh1[c]) for k, c in nm.items()}
    res['ladder'] = ladder_rates(A, ch, nm)
    return res


def ladder_rates(A, ch, nm):
    """log10 rate (per mutation event) and N times it, along the predicted inspection ladder, as transitions of the chain."""
    if A.game != 'insp':
        return None
    K1 = A.K[1]
    need = ['0:P38', '1:CRC', '1:C', '0:N', '1:K', '0:I']
    if any(k not in nm for k in need):
        return None
    P38, CRC, C, Nn, K, Ii = (nm[k] for k in need)
    steps = [('(P38,CRC)->(P38,C)', (P38, CRC), (P38, C)), ('(P38,C)->(N,C)', (P38, C), (Nn, C)), ('(N,C)->(N,K)', (Nn, C), (Nn, K)),
             ('(N,K)->(I,K)', (Nn, K), (Ii, K)), ('(I,K)->(I,C)', (Ii, K), (Ii, C)), ('(I,C)->(N,C)', (Ii, C), (Nn, C)),
             ('(P38,C)->(P38,CRC)', (P38, C), (P38, CRC)), ('(N,C)->(P38,C)', (Nn, C), (P38, C)),
             ('(P38,CRC)->(N,CRC)', (P38, CRC), (Nn, CRC)), ('(P38,CRC)->(P38,K)', (P38, CRC), (P38, K))]
    out = {}
    for name, (a, b), (a2, b2) in steps:
        L1, L2 = ch.rates(a * K1 + b)
        if a2 != a:
            lr = L1[a2]
        else:
            lr = L2[b2]
        out[name] = dict(log10_rate=float(lr / math.log(10)), N_rate=float(ch.N * math.exp(lr)) if np.isfinite(lr) else 0.0)
    return out


def cmd_chain(a):
    A = M.get_arm(a.game, a.arm, NMAX[a.game], a.c)
    t0 = time.time()
    if A.K[0] * A.K[1] > 80000:                     # too many pairs for the all-pairs weak graph: not computed (circulation index only)
        classes_info = (np.zeros(A.K[0] * A.K[1], np.int64), [])
    else:
        classes_info = M.weak_graph_classes(A.UA, A.UB)
    cyc = [c for c in classes_info[1]]
    log('[%s %s c=%g] K=%s weak classes: %s (%.0fs)' % (a.game, a.arm, a.c, A.K, [(c['kind'], c['size']) for c in cyc][:10], time.time() - t0))
    out = dict(game=a.game, arm=a.arm, c=a.c, K=A.K, weak_classes=[dict(kind=c['kind'], size=c['size']) for c in cyc], cells={})
    for N in a.N:
        r = chain_cell(A, N, classes_info, verbose=a.verbose, max_states=a.max_states, max_add=a.max_add, full=a.full)
        out['cells'][str(N)] = r
        st = r['stat']
        log('  N=%d states=%d capped=%s cut=%s closed=%s pi_cycle=%.3f pi_drift=%.3f pi_rest=%.3f  u0g=%.4f u1g=%.4f (%.0fs)' % (
            N, r['n_states'], r['capped'], r['log10_cut'], r['info'].get('n_closed'), r['pi_cycle'], r['pi_drift'], r['pi_rest'],
            st['u0g'], st['u1g'], r['time_s']))
        jdump(out, os.path.join(OUT, 'chain_%s_%s_c%g%s.json' % (a.game, a.arm, a.c, a.tag)))


# ================================================================ lottery
def checkpoints(cell, cont):
    cps = set(range(25, 2001, 25)) | set(range(1500, 2001, 10)) | {100, 250, 500, 1000}
    if cont:
        cps |= {3000, 4000, 5000, 7500} | set(range(9500, 10001, 100))
    return sorted(cps)


def lottery_cell(game, arm, c, cell_name, runs, verbose=True):
    cfg = PRIMARY if cell_name == 'primary' else SIZE
    n = NMAX[game]
    A = M.get_arm(game, arm, n, c)
    lang = A.lang
    K0, K1 = A.K
    I, N = cfg['I'], cfg['N']
    res = []
    t0 = time.time()
    for r in runs:
        cont = r < cfg['cont']
        cps = checkpoints(cell_name, cont)
        if not cont:
            cps = [g for g in cps if g <= cfg['gens']]
        f0 = M.draw_founders(lang, 0, A.cls_of[0], K0, I, N, M.run_seed('found|%s|%d|0' % (cell_name, r), 0))
        f1 = M.draw_founders(lang, 1, A.cls_of[1], K1, I, N, M.run_seed('found|%s|%d|1' % (cell_name, r), 0))
        i0 = np.nonzero(f0.sum(0) > 0)[0]; i1 = np.nonzero(f1.sum(0) > 0)[0]
        UA = np.ascontiguousarray(A.UA[np.ix_(i0, i1)]); UB = np.ascontiguousarray(A.UB[np.ix_(i1, i0)])
        o0, o1 = M.lottery2(UA, UB, np.ascontiguousarray(f0[:, i0]), np.ascontiguousarray(f1[:, i1]), N, M.W, cfg['m'],
                            M.run_seed('dyn|%s|%s|%s|%d' % (game, arm, cell_name, r), 0), np.array(cps, np.int64))
        rec = dict(run=r, cps=cps, stats={}, phases=[], founders=dict(n0=int(len(i0)), n1=int(len(i1))))
        phases = []
        for ci, g in enumerate(cps):
            X0 = np.zeros((I, K0)); X1 = np.zeros((I, K1))
            X0[:, i0] = o0[ci] / N; X1[:, i1] = o1[ci] / N
            st = M.island_stats(A, X0, X1)
            rec['stats'][str(g)] = summarize(st, game)
            if g % 25 == 0 and g <= 2000:
                phases.append(M.island_phase(st, game).tolist())
            if g in (2000, 10000):
                sh0 = X0.mean(0); sh1 = X1.mean(0)
                rec['top%d' % g] = dict(
                    r0=[(A.names[0][k], float(sh0[k])) for k in np.argsort(-sh0)[:10] if sh0[k] > 0.005],
                    r1=[(A.names[1][k], float(sh1[k])) for k in np.argsort(-sh1)[:10] if sh1[k] > 0.005])
                # per-island modal classes (the island partition) for the support / resolved statistics
                rec['modal%d' % g] = dict(
                    r0=[int(np.argmax(X0[i])) for i in range(I)], r1=[int(np.argmax(X1[i])) for i in range(I)],
                    h0=[float(X0[i].max()) for i in range(I)], h1=[float(X1[i].max()) for i in range(I)])
        rec['phases'] = phases
        res.append(rec)
        if verbose:
            s2 = rec['stats']['2000']
            if game == 'insp':
                log('  run %d (%.0fs): u0g=%.3f u1g=%.3f p=%.3f q=%.3f rd1=%.2f' % (r, time.time() - t0, s2['u0g'], s2['u1g'], s2['p_insp'] or -1, s2['q_cheat'] or -1, s2['rd1']))
            else:
                log('  run %d (%.0fs): u0g=%.3f bluff=%.3f call=%.3f rd1=%.2f' % (r, time.time() - t0, s2['u0g'], s2['bluff'] or -1, s2['call'] or -1, s2['rd1']))
    return res


def cmd_lottery(a):
    runs = list(range(a.runs[0], a.runs[1])) if a.runs else list(range((PRIMARY if a.cell == 'primary' else SIZE)['runs']))
    res = lottery_cell(a.game, a.arm, a.c, a.cell, runs)
    tag = '%s_%s_c%g_%s' % (a.game, a.arm, a.c, a.cell)
    if a.runs:
        tag += '_r%d-%d' % (a.runs[0], a.runs[1])
    jdump(dict(game=a.game, arm=a.arm, c=a.c, cell=a.cell, runs=res), os.path.join(OUT, 'lot_%s.json.gz' % tag), gz=True)
    log('wrote lot_%s.json.gz' % tag)


# ================================================================ static numbers, audits and validation
def named_table(lang, ev, game):
    tabs = M.NAMED_INSP if game == 'insp' else M.NAMED_END
    rows, cols = [], []
    for k, spec in tabs[0].items():
        try: rows.append((k, M.prog_of(lang, 0, spec)))
        except KeyError: pass
    for k, spec in tabs[1].items():
        try: cols.append((k, M.prog_of(lang, 1, spec)))
        except KeyError: pass
    t = {}
    for rn, a in rows:
        for cn, b in cols:
            t['%s|%s' % (rn, cn)] = dict(u0=float(ev['U0'][a, b]), u1=float(ev['U1'][b, a]), h0=float(ev['E0'][a, b]), h1=float(ev['E1'][b, a]),
                                          f0=float(ev['F0'][a, b]), f1=float(ev['F1'][b, a]))
    return t


def cmd_static(a):
    import resource
    out = {}
    cells = [('insp', ar) for ar in ('blind', 'sample', 'exact', 'matched', 'sr4', 'sr16')] + [('end', ar) for ar in ('blind', 'sample', 'exact', 'matched')]
    for game, arm in cells:
        t0 = time.time()
        n = NMAX[game]
        arms, ev, lang = M.build_arm(game, arm, n, prices=(0.0, 0.01, 0.001, 0.05), keep_ev=True)
        for pc, A in arms.items():                       # populate the class-table cache (every price of the panel)
            p = M._arm_path(game, arm, n, pc, 12)
            os.makedirs(M.CACHE, exist_ok=True)
            M.save_arm(A, p + '.tmp.npz'); os.replace(p + '.tmp.npz', p)
        rec = dict(game=game, arm=arm, n=n, S=[lang.S0, lang.S1], spellings=[float(lang.a_size[r].sum()) for r in (0, 1)],
                   K={str(pc): A.K for pc, A in arms.items()}, size_counts=[[int((lang.size[lang.progs[r]] == s).sum()) for s in range(1, n + 1)] for r in (0, 1)])
        A0 = arms[0.0]
        rec['reader_prior_mass'] = [float(lang.mu[r][lang.has_app[r]].sum()) for r in (0, 1)]
        rec['exact_reader_prior_mass'] = [float(lang.mu[r][lang.has_cr[r]].sum()) for r in (0, 1)]
        rec['sr_prior_mass'] = [float(lang.mu[r][lang.has_sr[r]].sum()) for r in (0, 1)]
        rec['reader_class_mass'] = [float(A0.mass[r][A0.reader[r]].sum()) for r in (0, 1)]
        rec['top_classes'] = [[(A0.names[r][k], float(A0.mass[r][k]), int(A0.sizes[r][k])) for k in range(min(8, A0.K[r]))] for r in (0, 1)]
        rec['table'] = named_table(lang, ev, game)
        rec['forfeit_mean_over_pairs'] = [float(ev['F0'].mean()), float(ev['F1'].mean())]
        # the bounded-cr audit: a program with `cr` reads the opponent's distribution on D - 1 levels; compare with the actual (D) one
        if arm in ('exact',) :
            d0 = np.abs(ev['prevG1'] - ev['G1']).max(-1) > 1e-9           # (S1, S0): opponent b's distribution against a differs
            d1 = np.abs(ev['prevG0'] - ev['G0']).max(-1) > 1e-9           # (S0, S1)
            m0 = lang.has_cr[0][:, None] & d0.T                           # role-0 cr programs reading b
            m1 = lang.has_cr[1][:, None] & d1.T
            rec['bounded_cr'] = dict(programs_with_cr=[int(lang.has_cr[0].sum()), int(lang.has_cr[1].sum())],
                                     pairs_disagree=[int(m0.sum()), int(m1.sum())], pairs_total=[int(lang.has_cr[0].sum()) * lang.S1, int(lang.has_cr[1].sum()) * lang.S0],
                                     max_abs_diff=[float(np.abs(ev['prevG1'] - ev['G1'])[:, lang.has_cr[0]].max()), float(np.abs(ev['prevG0'] - ev['G0'])[:, lang.has_cr[1]].max())])
            # nested-reader pairs (both programs contain an application) among the cr programs
            nr0 = lang.has_cr[0][:, None] & lang.has_app[1][None, :]
            nr1 = lang.has_cr[1][:, None] & lang.has_app[0][None, :]
            rec['bounded_cr']['nested_pairs'] = [int(nr0.sum()), int(nr1.sum())]
            rec['bounded_cr']['nested_disagree'] = [int((m0 & nr0).sum()), int((m1 & nr1).sum())]
            # work of an exact computation (all branches) against the depth price
            evw = M.evaluate(lang, 12, keep_prev=False, workmode=1)
            for r, (Ed, Ew) in enumerate(((ev['E0'], evw['E0']), (ev['E1'], evw['E1']))):
                mk = lang.has_cr[r]
                rec.setdefault('work_vs_depth', []).append(dict(role=r, mean_depth_cr=float(Ed[mk].mean()), mean_work_cr=float(Ew[mk].mean()),
                                                                max_work_cr=float(Ew[mk].max()), max_depth_cr=float(Ed[mk].max()),
                                                                share_pairs_work_gt_depth=float((Ew[mk] > Ed[mk] + 1e-9).mean())))
            del evw
        # Endgame minimax statics
        if game == 'end':
            def lookup(r, spec):
                try: return M.prog_of(lang, r, spec)
                except KeyError: return None
            eq = lookup(0, M.NAMED_END[0]['EQ']); x2 = lookup(1, 'x')
            rec['minimax'] = dict(eq_row_min=float(ev['U0'][eq].min()), eq_row_max=float(ev['U0'][eq].max()),
                                  x_row_min=float(ev['U1'][x2].min()), x_row_argmin=lang.src(lang.progs[0][int(ev['U1'][x2].argmin())]),
                                  eq_vs_x_all=float(np.abs(ev['U0'][eq]).max()))
            nonread = ~lang.has_app[0]
            wbet = ev['G0'][:, 0, 0]
            rec['minimax']['x_gain_equals_one_minus_w_over_3_maxerr'] = float(np.abs((1 - wbet)[nonread] / 3 - ev['U1'][x2][nonread]).max())
        if game == 'insp' and arm == 'blind':
            p = ev['G0'][:, 0, 0]
            rec['grid_p'] = sorted(set(np.round(p, 12).tolist()))
            sz = lang.size[lang.progs[0]]
            rec['grid_min_size'] = {str(v): int(sz[np.abs(p - v) < 1e-12].min()) for v in (0.25, 3 / 8, 5 / 16, 0.5)}
        # price splits: classes at c = 0 versus c = 0.01
        rec['price_split'] = [A0.K[0], arms[0.01].K[0], A0.K[1], arms[0.01].K[1]]
        rec['peak_rss_mb'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
        rec['time_s'] = time.time() - t0
        out['%s_%s' % (game, arm)] = rec
        log('%s %s: S=%s K(c=0)=%s K(c=.01)=%s rss=%.0fMB (%.0fs)' % (game, arm, rec['S'], A0.K, arms[0.01].K, rec['peak_rss_mb'], rec['time_s']))
        del ev, arms
    jdump(out, os.path.join(OUT, 'static.json'))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd')
    sp.add_parser('static')
    c = sp.add_parser('chain')
    c.add_argument('game'); c.add_argument('arm'); c.add_argument('c', type=float)
    c.add_argument('--N', type=int, nargs='+', default=list(NS_CHAIN)); c.add_argument('--verbose', action='store_true')
    c.add_argument('--max_states', type=int, default=1500); c.add_argument('--max_add', type=int, default=400); c.add_argument('--tag', default=''); c.add_argument('--full', action='store_true')
    l = sp.add_parser('lottery')
    l.add_argument('game'); l.add_argument('arm'); l.add_argument('c', type=float); l.add_argument('cell')
    l.add_argument('--runs', type=int, nargs=2)
    a = ap.parse_args()
    if a.cmd == 'chain': cmd_chain(a)
    elif a.cmd == 'lottery': cmd_lottery(a)
    elif a.cmd == 'static':
        cmd_static(a)


if __name__ == '__main__':
    main()
