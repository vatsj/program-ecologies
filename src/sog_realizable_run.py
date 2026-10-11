"""Runs for the social organization game over the realizable language (specs/2026-10-10-sog-realizable.md;
notes/sog-realizable.md; predictions/2026-10-10-sog-realizable.md).

    python3 src/sog_realizable_run.py tables              # catalogue + exact class tables (runs/sog_realizable/, not committed)
    python3 src/sog_realizable_run.py validate [--procs 3] # notes §1.x: code validation of §1 before any counted cell
    python3 src/sog_realizable_run.py static              # notes §1.4: static invasion analysis, masses, coalitions
    python3 src/sog_realizable_run.py costs [--procs 3]    # fuel sweep and cost records (notes §2)
    python3 src/sog_realizable_run.py lottery --cell NAME [--procs 3]
    python3 src/sog_realizable_run.py chain               # the diagnostic chain at N = 10^4

At most 3 worker processes; pool children are terminated by the pool's own context manager.
"""
import argparse
import json
import os
import pickle
import random
import sys
import time

for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import sog_realizable as S

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
OUT = os.path.join(RUNS, 'sog_realizable')
K_MAIN = S.K_MAIN
V_MAIN = K_MAIN // 4

_CAT = {}


def catalogue(K=K_MAIN):
    if K not in _CAT:
        _CAT[K] = S.Catalogue(K=K)
    return _CAT[K]


def tables(force=False):
    os.makedirs(OUT, exist_ok=True)
    f = os.path.join(OUT, 'tables.pkl')
    if os.path.exists(f) and not force:
        return pickle.load(open(f, 'rb'))
    cat = catalogue()
    T = S.build_tables(cat, extra_boss_dts=[S.dt(S.NAMED_B_OUT['D*_2'])])
    pickle.dump(T, open(f, 'wb'), protocol=4)
    return T


# ----------------------------------------------------------------------------------------------------------------
# programs for validation (compiled lazily; picklable tuples)
# ----------------------------------------------------------------------------------------------------------------
def compiled(role, tk, slot, spelling=None, K=K_MAIN):
    cat = catalogue(K)
    return cat.program(role, tk, slot if role == 'W' else 0, V=K // 4, K=K, spelling=spelling)


def named_programs(K=K_MAIN, V=None):
    V = K // 4 if V is None else V

    def build(x, role, slot, naive=False, misorder=False):
        lst, _ = S.produce_lists(S.dt(x), role)
        return S.compile_program(x, role, slot, V, K, lst, naive=naive, misorder=misorder)
    W = {nm: (build(x, 'W', 1), build(x, 'W', 2)) for nm, x in S.NAMED_W.items()}
    B = {nm: build(x, 'B', 0) for nm, x in S.NAMED_B.items()}
    B['D*_2'] = build(S.NAMED_B_OUT['D*_2'], 'B', 0)
    B['C1'] = build(('if', ('A', ('C', 1, S.A_STRIKE)), ('L', 7), ('L', 1)), 'B', 0)
    return W, B, build


# ----------------------------------------------------------------------------------------------------------------
# validation (notes §1.x)
# ----------------------------------------------------------------------------------------------------------------
HAND = [  # (boss, w1, w2) -> expected (boss action, a1, a2): notes §1.3.3 and §1.2.6
    (('D*', 'T1', 'T1'), (7, 'C', 'C')), (('D*', 'T0', 'T0'), (4, 'C', 'C')), (('D*', 'scab', 'scab'), (1, 'C', 'C')),
    (('D*', 'T1', 'scab'), (7, 'C', 'C')), (('D*', 'scab', 'T1'), (1, 'C', 'D')), (('D0', 'T0', 'T0'), (7, 'C', 'C')),
    (('WF', 'T1', 'T1'), (1, 'D', 'D')), (('pay(1/2,none)', 'T1', 'scab'), (7, 'C', 'C')),
    (('pay(0,none)', 'Q', 'Q'), (1, 'D', 'D')), (('pay(1/2,none)', 'Q', 'Q'), (7, 'D', 'D')),
    (('pay(0,none)', 'Q', 'scab'), (1, 'C', 'C')), (('pay(0,none)', 'U', 'U'), (1, 'D', 'D')),
    (('pay(1/2,none)', 'U', 'U'), (7, 'C', 'C')), (('pay(0,none)', 'R', 'R'), (1, 'D', 'D')),
    (('pay(1/2,none)', 'R', 'R'), (7, 'C', 'C')), (('C1', 'T1', 'T1'), (1, 'D', 'D')),
    (('D*_2', 'T1', 'T1'), (7, 'C', 'C')), (('D*_2', 'T1', 'scab'), (1, 'D', 'C')),
]


def _checks_of(enc):
    """Every check a triple's plays and certifications involve: boss wage sets, worker actions, the boss's probes."""
    out = [(enc, 0, A) for A in S.BOSS_Q] + [(enc, j, A) for j in (1, 2) for A in S.WORKER_Q]
    for s in (0, 1):
        pc = S.probe_const(s, V_MAIN, K_MAIN)
        e2 = (pc, enc[1], enc[2])
        out += [(e2, j, A) for j in (1, 2) for A in S.WORKER_Q]
    return out


def _term_vs_host(args):
    """Worker job: (label, enc) -> per check: term value and steps, host value; whole plays; soundness audit."""
    label, enc = args
    res = []
    h = S.HostCheck3()
    play, steps, raw = S.play3(enc[0], enc[1], enc[2], K_MAIN)
    for (e, j, A) in _checks_of(enc):
        tv, ts = S.term_check(e, j, A, V_MAIN, K_MAIN)
        hv = h.check3(e, j, A, V_MAIN, K_MAIN)
        # soundness audit: the actual run of the subject
        sv = None
        if tv == 'T':
            subj = S.conf_term(e, j)
            v, n = S.L.run_big(S.L.evaluate, subj, K_MAIN)
            sv = (v in A)
        res.append(dict(j=j, A=S.ANAME[A], probe=e is not enc, term=tv, steps=int(ts), host=hv, sound=sv))
    return dict(label=label, play=[int(play[0]), play[1], play[2]], steps=[int(x) for x in steps], checks=res)


def validate(args):
    t0 = time.time()
    out = {}
    cat = catalogue()
    T = tables()
    w = cat.roles['W']; b = cat.roles['B']
    rng = random.Random(20261010)
    # V1: production, symbolic vs host tactic
    pp = S.PathProducer()
    mism = []
    for tk, d in enumerate(w['dt']):
        for slot in (1, 2):
            x = w['spellings'][w['members'][tk][0]]
            prog0 = S.compile_program(x, 'W', slot, V_MAIN, K_MAIN, 0)
            lh, _ = S.produce_lists(d, 'W', pp, prog0, slot, V_MAIN, K_MAIN)
            if lh != w['lists'][tk]: mism.append(('W', tk, slot))
    bsample = rng.sample(range(len(b['dt'])), 2000) + [b['tau_of'][S.dt(x)] for x in S.NAMED_B.values()]
    for tk in bsample:
        x = b['spellings'][b['members'][tk][0]]
        prog0 = S.compile_program(x, 'B', 0, V_MAIN, K_MAIN, 0)
        lh, _ = S.produce_lists(b['dt'][tk], 'B', pp, prog0, 0, V_MAIN, K_MAIN)
        if lh != b['lists'][tk]: mism.append(('B', tk))
    # lists as functions of run trees: other spellings of the same tree under the host tactic
    for role, r in (('W', w), ('B', b)):
        multi = [tk for tk in range(len(r['members'])) if len(r['members'][tk]) > 1]
        for tk in rng.sample(multi, min(300, len(multi))):
            k = rng.choice(r['members'][tk][1:])
            prog0 = S.compile_program(r['spellings'][k], role, 1 if role == 'W' else 0, V_MAIN, K_MAIN, 0)
            lh, _ = S.produce_lists(r['dt'][tk], role, pp, prog0, 1 if role == 'W' else 0, V_MAIN, K_MAIN)
            if lh != r['lists'][tk]: mism.append((role, tk, 'spelling', k))
    out['production'] = dict(worker_trees=len(w['dt']), boss_trees_sampled=len(bsample), mismatches=mism)
    print('production: %d mismatches (%.0fs)' % (len(mism), time.time() - t0), flush=True)
    # V2: expanded node counts, formula vs compiled term
    xm = 0
    for role, r in (('W', w), ('B', b)):
        for k in rng.sample(range(len(r['spellings'])), 1000):
            x = r['spellings'][k]
            a = S.expanded_nodes(x, role, V_MAIN, K_MAIN)
            body = S.body_term(x, role, 1 if role == 'W' else 0, V_MAIN, K_MAIN)
            if a != S.term_nodes(body): xm += 1
    out['expanded_nodes'] = dict(sampled=2000, mismatches=xm,
                                 atoms={S.atom_name(at): S.expanded_nodes(('A', at), 'W', V_MAIN, K_MAIN) for at in S.WORKER_ATOMS}
                                 | {S.atom_name(at): S.expanded_nodes(('A', at), 'B', V_MAIN, K_MAIN) for at in S.BOSS_ATOMS},
                                 named={nm: S.expanded_nodes(x, 'W', V_MAIN, K_MAIN) for nm, x in S.NAMED_W.items()}
                                 | {nm: S.expanded_nodes(x, 'B', V_MAIN, K_MAIN) for nm, x in S.NAMED_B.items()})
    print('expanded nodes: %d mismatches' % xm, flush=True)
    # V3: hand plays by whole runs
    Wn, Bn, build = named_programs()
    hand = []
    for (bn, x, y), exp in HAND:
        play, steps, raw = S.play3(Bn[bn], Wn[x][0], Wn[y][1], K_MAIN)
        hand.append(dict(enc='%s | %s | %s' % (bn, x, y), play=[int(play[0]), play[1], play[2]], expected=list(exp),
                         ok=tuple(play) == exp, steps=[int(s) for s in steps]))
    out['hand_plays'] = hand
    print('hand plays: %d/%d as derived' % (sum(h['ok'] for h in hand), len(hand)), flush=True)
    # V4 + V5 + soundness: term vs host on encounters; composition vs whole runs
    jobs = []
    for (bn, x, y), _ in HAND:
        jobs.append(('named %s|%s|%s' % (bn, x, y), (Bn[bn], Wn[x][0], Wn[y][1])))
    nb = len(T['repb']); n1 = len(T['rep1']); n2 = len(T['rep2'])
    trip = []
    for i in range(args.sample):
        bc = rng.randrange(nb); xc = rng.randrange(n1); yc = rng.randrange(n2)
        # a random member tree of each class and a random spelling of it (lumping and tau-symmetry)
        btk = rng.choice(list(np.nonzero(T['clsb'] == bc)[0]))
        xtk = rng.choice(list(np.nonzero(T['cls1'] == xc)[0])); ytk = rng.choice(list(np.nonzero(T['cls2'] == yc)[0]))
        if btk >= T['nb_cat']:
            bprog = Bn['D*_2']
        else:
            bprog = compiled('B', btk, 0, spelling=rng.choice(b['members'][btk]))
        xprog = compiled('W', xtk, 1, spelling=rng.choice(w['members'][xtk]))
        yprog = compiled('W', ytk, 2, spelling=rng.choice(w['members'][ytk]))
        trip.append((bc, xc, yc, btk, xtk, ytk))
        jobs.append(('sample %d' % i, (bprog, xprog, yprog)))
    from multiprocessing import get_context
    with get_context('fork').Pool(args.procs) as pool:
        results = pool.map(_term_vs_host, jobs, chunksize=4)
    nh = len(HAND)
    allc = [c for r in results for c in r['checks']]
    disagree = [(r['label'], c) for r in results for c in r['checks'] if c['term'] != c['host']]
    false_atoms = [(r['label'], c) for r in results for c in r['checks'] if c['sound'] is False]
    steps_T = [c['steps'] for c in allc if c['term'] != 'TO']
    comp_mism = []
    for (bc, xc, yc, btk, xtk, ytk), r in zip(trip, results[nh:]):
        jc = S.joint_code(T, bc, xc, yc)
        want = (jc // 4, 'CD'[(jc // 2) % 2], 'CD'[jc % 2])
        if tuple(r['play']) != want:
            comp_mism.append(dict(label=r['label'], classes=[int(bc), int(xc), int(yc)], trees=[int(btk), int(xtk), int(ytk)],
                                  table=list(want), whole=r['play']))
    out['term_vs_host'] = dict(encounters=len(results), checks=len(allc), disagreements=len(disagree),
                               disagree_examples=disagree[:10], true_checks=sum(1 for c in allc if c['term'] == 'T'),
                               false_atoms=len(false_atoms), false_examples=false_atoms[:5],
                               max_steps_not_TO=max(steps_T), steps_TO=sum(1 for c in allc if c['term'] == 'TO'),
                               median_steps=float(np.median(steps_T)), p99_steps=float(np.percentile(steps_T, 99)))
    out['composition'] = dict(triples=len(trip), mismatches=len(comp_mism), examples=comp_mism[:10])
    print('term vs host: %d checks, %d disagreements, %d false atoms; composition %d/%d mismatches; max steps %d (%.0fs)' % (
        len(allc), len(disagree), len(false_atoms), len(comp_mism), len(trip), max(steps_T), time.time() - t0), flush=True)
    # V6: corrupted instances
    out['corrupted'] = corrupted_instances()
    print('corrupted instances:', json.dumps({k: v.get('ok') for k, v in out['corrupted'].items()}), flush=True)
    # V7: Lemma Sym_3 measured on closures (Q-type pairs)
    out['sym3'] = sym3_measure(rng)
    print('Sym3:', json.dumps(out['sym3'])[:300], flush=True)
    out['time_s'] = time.time() - t0
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(RUNS, 'sog-realizable-validate.json'), 'w'), indent=1, default=str)
    print('validate done %.0fs' % (time.time() - t0))


def corrupted_instances():
    """notes §1.2.6, by the checker term and the host replay."""
    K, V = K_MAIN, V_MAIN
    Wn, Bn, build = named_programs()
    h = S.HostCheck3()
    out = {}

    def both(enc, j, A, mode=S.MODE3):
        tv, ts = S.term_check(enc, j, A, V, K, mode)
        hv = h.check3(enc, j, A, V, K, mode)
        return tv, hv, int(ts)
    T1a, T1b = Wn['T1']; SCa, SCb = Wn['scab']; DS = Bn['D*']
    # 1. slot-2 ordering
    good = both((DS, T1a, SCb), 0, S.A_EQ12)
    bad = both((DS, SCa, T1b), 0, S.A_EQ12)
    T1mis = build(S.NAMED_W['T1'], 'W', 2, misorder=True)
    play, steps, raw = S.play3(DS, SCa, T1mis, K)
    playc, _, _ = S.play3(DS, SCa, T1b, K)
    out['1_slot2_ordering'] = dict(accepted_in_order=good, same_question_misordered=bad,
                                   misordered_T1_play=[int(play[0]), play[1], play[2]], correct_T1_play=[int(playc[0]), playc[1], playc[2]],
                                   classification='substitution' if (play[0] // 3 < 2 and play[2] == 'C') else 'none',
                                   ok=good[:2] == ('T', 'T') and bad[:2] == ('F', 'F') and play[2] == 'C' and playc[2] == 'D')
    # 2. opponent substitution
    P0 = S.probe_const(0, V, K); P14 = S.probe_const(1, V, K)
    PHALF = S.carrier3(S.N(7), S.constant_list(7))
    a = both((P0, T1a, T1b), 1, S.A_STRIKE); a2 = both((P14, T1a, T1b), 1, S.A_STRIKE)
    bsub = both((PHALF, T1a, T1b), 1, S.A_STRIKE)
    c = both((DS, T1a, T1b), 0, S.A_EQ12); d = both((DS, SCa, SCb), 0, S.A_EQ12)
    out['2_opponent_substitution'] = dict(T1_strike_vs_pay0=a, vs_pay14=a2, vs_actual_pay12=bsub, Dstar_half_T1pair=c,
                                          Dstar_half_scabpair=d,
                                          ok=a[:2] == ('T', 'T') and a2[:2] == ('T', 'T') and bsub[:2] == ('F', 'F') and c[:2] == ('T', 'T') and d[:2] == ('F', 'F'))
    # 3. unequal branches: forged lists for T1
    t1x = S.NAMED_W['T1']
    good_lst, info = S.produce_lists(S.dt(t1x), 'W')
    work_s = info[S.A_WORK][0][0]; strike_s = info[S.A_STRIKE][0][0]
    swapped = S.C.node(S.C.EVS, 0, S.C.node(S.C.CHKR, 0, S.C.node(S.C.RUN, 0), S.C.node(S.C.EVS, 0, S.C.node(S.C.AX, 0))))
    forged = {'premises_exchanged': S.cons([(S.cons(S.A_WORK), swapped)]),
              'F_path_claims_work': S.cons([(S.cons(S.A_WORK), strike_s)]),
              'T_path_claims_strike': S.cons([(S.cons(S.A_STRIKE), work_s)])}
    r3 = {}
    for nm, lst in forged.items():
        F1 = S.compile_program(t1x, 'W', 1, V, K, lst)
        r3[nm] = dict(vs_pay12=both((PHALF, F1, T1b), 1, S.A_WORK if 'work' in nm or 'exchanged' in nm else S.A_STRIKE),
                      vs_pay0=both((P0, F1, T1b), 1, S.A_WORK if 'work' in nm or 'exchanged' in nm else S.A_STRIKE))
    # T-path claim where the box is false: T1's own work script against pay(0)
    r3['T_leaf_box_false'] = both((P0, T1a, T1b), 1, S.A_WORK)
    # (c) unequal mutual pair Q / Qw: every check either F/TO or its atom's truth
    Qa = Wn['Q'][0]; Qwb = Wn['Qw'][1]
    pr, _, _ = S.play3(Bn['pay(0,none)'], Qa, Qwb, K)
    vals = {('x' if j == 1 else 'y', S.ANAME[A]): both((Bn['pay(0,none)'], Qa, Qwb), j, A) for j in (1, 2) for A in S.WORKER_Q}
    acc_false = [k for k, v in vals.items() if v[0] == 'T' and ((k[0] == 'x' and pr[1] != ('C' if k[1] == 'work' else 'D')) or
                                                              (k[0] == 'y' and pr[2] != ('C' if k[1] == 'work' else 'D')))]
    # (d) naive control: QN (naive checker, with list) vs QN0 (same code, no list)
    qx = S.NAMED_W['Q']
    pn = S.PathProducer(naive=True)
    prog0 = S.compile_program(qx, 'W', 1, V, K, 0, naive=True)
    lstN, _ = S.produce_lists(S.dt(qx), 'W', pn, prog0, 1, V, K)
    QN = S.compile_program(qx, 'W', 1, V, K, lstN, naive=True)
    QN0 = S.compile_program(qx, 'W', 2, V, K, 0, naive=True)
    pn_play, _, _ = S.play3(Bn['pay(0,none)'], QN, QN0, K)
    naive_qn_strikes = both((Bn['pay(0,none)'], QN, QN0), 1, S.A_STRIKE, S.MODE3N)
    sound_qn_strikes = both((Bn['pay(0,none)'], QN, QN0), 1, S.A_STRIKE, S.MODE3)
    out['3_unequal_branches'] = dict(forged=r3, mutual_pair_play=[int(pr[0]), pr[1], pr[2]], mutual_pair_checks={'%s %s' % k: v for k, v in vals.items()},
                                     mutual_pair_false_accepted=acc_false,
                                     naive_play=[int(pn_play[0]), pn_play[1], pn_play[2]], naive_accepts_QN_strikes=naive_qn_strikes,
                                     sound_on_same=sound_qn_strikes,
                                     ok=all(v['vs_pay12'][0] != 'T' and v['vs_pay0'][0] != 'T' for k, v in r3.items() if k != 'T_leaf_box_false')
                                     and r3['T_leaf_box_false'][0] == 'F' and not acc_false
                                     and naive_qn_strikes[0] == 'T' and pn_play[1] == 'C' and sound_qn_strikes[0] == 'F')
    # 4. exhausted fuel
    r4 = {}
    Vs = 25000
    fit = {}
    for dK in range(4, 16):
        Kx = Vs + dK
        Wx, Bx, bx = named_programs(K=Kx, V=Vs)
        tv, ts = S.term_check((Bx['pay(1/2,none)'], Wx['T1'][0], Wx['T1'][1]), 1, S.A_WORK, Vs, Kx)
        hv = S.HostCheck3().check3((Bx['pay(1/2,none)'], Wx['T1'][0], Wx['T1'][1]), 1, S.A_WORK, Vs, Kx)
        fit[dK] = (tv, hv)
    r4['fit_boundary'] = {str(k): v for k, v in fit.items()}
    # cap exceeded: D* compiled with a small cap V = 5,000 checked by T1 (same V)
    Ksm = 4 * 5000
    Wx, Bx, bx = named_programs(K=Ksm)
    tv, ts = S.term_check((Bx['D*'], Wx['T1'][0], Wx['T1'][1]), 1, S.A_WORK, Ksm // 4, Ksm)
    playx, stx, _ = S.play3(Bx['D*'], Wx['T1'][0], Wx['T1'][1], Ksm)
    r4['cap_exceeded'] = dict(K=Ksm, check_T1_works=(tv, int(ts)), play=[int(playx[0]), playx[1], playx[2]], steps=[int(s) for s in stx])
    # global timeout: a militant with four wage checks against C1 (each regresses at the cap)
    m4 = ('if', S.B12, ('L', 'W'), ('if', S.B14, ('L', 'S'), ('if', S.BL14, ('L', 'S'), ('if', S.B12, ('L', 'W'), ('L', 'S')))))
    M4a = build(m4, 'W', 1)
    play4, st4, raw4 = S.play3(Bn['C1'], M4a, Wn['T1'][1], K)
    r4['four_checks_vs_C1'] = dict(play=[int(play4[0]), play4[1], play4[2]], raw=[str(v) for v in raw4], steps=[int(s) for s in st4],
                                   classification='timeout' if (raw4[1] == 'BOT' and play4[1] == 'C' and play4[0] // 3 < 2) else 'none')
    # atom asked at fuel below the actual run length
    small = S.HostCheck3()
    r4['fuel_below_run'] = dict(host=small.check(S.ID3['CHK3'], S.mk_arg3(V, (DS, T1a, T1b), 1, S.A_WORK, 40000)),
                                term=S.term_check((DS, T1a, T1b), 1, S.A_WORK, V, 40000)[0])
    out['4_exhausted_fuel'] = r4
    r4['ok'] = (any(v == ('F', 'F') for v in fit.values()) and any(v == ('T', 'T') for v in fit.values())
                and r4['four_checks_vs_C1']['classification'] == 'timeout' and r4['fuel_below_run']['term'] != 'T')
    # 5. mixed closure (Q, Qw): covered by 3(c); record plays
    out['5_mixed_closure'] = dict(play=[int(pr[0]), pr[1], pr[2]], ok=not acc_false)
    # 6. C1 against (T1, T1)
    p6, s6, _ = S.play3(Bn['C1'], T1a, T1b, K)
    out['6_C1'] = dict(play=[int(p6[0]), p6[1], p6[2]], steps=[int(s) for s in s6], ok=(int(p6[0]), p6[1], p6[2]) == (1, 'D', 'D'))
    return out


def sym3_measure(rng, n=200):
    """For checks that used a closure (encounters of tagged workers), every closure member's term check returns T
    with no more steps than the root (Lemma Sym_3)."""
    cat = catalogue()
    w = cat.roles['W']
    tagged = [tk for tk in range(len(w['dt'])) if w['tag'][tk]]
    PH = S.carrier3(S.N(7), S.constant_list(7)); P0 = S.carrier3(S.N(1), S.constant_list(1))
    rows = []
    for _ in range(n):
        x = rng.choice(tagged); y = rng.choice(tagged)
        enc = (rng.choice([PH, P0]), compiled('W', x, 1), compiled('W', y, 2))
        for j in (1, 2):
            for A in S.WORKER_Q:
                h = S.HostCheck3()
                arg = S.mk_arg3(V_MAIN, enc, j, A, K_MAIN)
                used = h._vone3(S.ID3['CHK3'], arg)
                tv, ts = S.term_check(enc, j, A, V_MAIN, K_MAIN)
                if tv == 'T' and used:
                    for u in used:
                        uv, us = _term_from_arg(u)
                        rows.append(dict(root_steps=int(ts), member=uv, member_steps=int(us)))
    bad = [r for r in rows if r['member'] != 'T' or r['member_steps'] > r['root_steps']]
    eq = sum(1 for r in rows if r['member_steps'] == r['root_steps'])
    return dict(closures=len(rows), violations=len(bad), equal_steps=eq, examples=bad[:5])


def _term_from_arg(arg):
    n = S.CORE3[S.MODE3]
    key = (n, V_MAIN, S.L.tval_to_rt(arg))
    rec = S.L.CACHE.get(key)
    if rec is None:
        v, steps = S.L.run_big(S.L.evaluate, ('capk', S.N(V_MAIN), ('lib', n), arg))
        rec = S.L.CACHE.get(key)
        if rec is None: rec = (v, steps - 1)
    return rec


def class_masses(T, prior='L'):
    """Normalized class masses per role: (boss classes incl. extras at mass 0, worker classes (slot 1))."""
    cat = catalogue()
    mt = cat.tau_mass('B', prior)
    mb = np.zeros(len(T['repb']))
    np.add.at(mb, T['clsb'][:len(mt)], mt)
    mw = np.zeros(len(T['rep1']))
    np.add.at(mw, T['cls1'], cat.tau_mass('W', prior))
    return mb / mb.sum(), mw / mw.sum()


def _gap_job(args):
    label, enc, K, want = args
    V = K // 4
    h = S.HostCheck3()
    play, steps, raw = S.play3(enc[0], enc[1], enc[2], K)
    nd = 0; nT = 0; mx = 0; nTO = 0
    for (e, j, A) in _checks_of_K(enc, V, K):
        tv, ts = S.term_check(e, j, A, V, K)
        hv = h.check3(e, j, A, V, K)
        nd += tv != hv; nT += tv == 'T'
        if tv != 'TO': mx = max(mx, int(ts))
        else: nTO += 1
    return dict(label=label, play=[int(play[0]), play[1], play[2]], want=list(want), match=(int(play[0]), play[1], play[2]) == tuple(want),
                disagree=nd, maxsteps=mx, TO=nTO, steps=[int(s) for s in steps])


def _checks_of_K(enc, V, K):
    out = [(enc, 0, A) for A in S.BOSS_Q] + [(enc, j, A) for j in (1, 2) for A in S.WORKER_Q]
    for s in (0, 1):
        pc = S.probe_const(s, V, K)
        out += [((pc, enc[1], enc[2]), j, A) for j in (1, 2) for A in S.WORKER_Q]
    return out


def gap(args):
    """Executable vs ideal on matched samples of class triples at each fuel K (uniform over classes and L-weighted)."""
    T = tables()
    cat = catalogue()
    w = cat.roles['W']; b = cat.roles['B']
    mb, mw = class_masses(T, 'L')
    rng = random.Random(7)
    nb = T['nb_cat']
    nbc = len(T['repb']) - T['n_extra']
    trips = []
    for i in range(args.sample):
        if i % 2 == 0:
            bc, xc, yc = rng.randrange(nbc), rng.randrange(len(T['rep1'])), rng.randrange(len(T['rep2']))
            kind = 'uniform'
        else:
            bc = int(np.searchsorted(np.cumsum(mb), rng.random() * mb.sum()))
            xc = int(np.searchsorted(np.cumsum(mw), rng.random()))
            yc = int(np.searchsorted(np.cumsum(mw), rng.random()))
            bc = min(bc, nbc - 1); xc = min(xc, len(mw) - 1); yc = min(yc, len(mw) - 1)
            kind = 'L'
        btk = int(T['repb'][bc]); xtk = int(T['rep1'][xc]); ytk = int(T['rep2'][yc])
        trips.append((kind, bc, xc, yc, btk, xtk, ytk))
    out = {}
    from multiprocessing import get_context
    for K in args.Ks:
        jobs = []
        for i, (kind, bc, xc, yc, btk, xtk, ytk) in enumerate(trips):
            jc = S.joint_code(T, bc, xc, yc)
            want = (jc // 4, 'CD'[(jc // 2) % 2], 'CD'[jc % 2])
            enc = (compiled('B', btk, 0, K=K), compiled('W', xtk, 1, K=K), compiled('W', ytk, 2, K=K))
            jobs.append(('%s %d' % (kind, i), enc, K, want))
        t0 = time.time()
        with get_context('fork').Pool(args.procs) as pool:
            res = pool.map(_gap_job, jobs, chunksize=4)
        rows = {}
        for kind in ('uniform', 'L'):
            rr = [r for r, t in zip(res, trips) if t[0] == kind]
            rows[kind] = dict(triples=len(rr), play_mismatch=sum(1 for r in rr if not r['match']),
                              checks=15 * len(rr), check_disagree=sum(r['disagree'] for r in rr),
                              term_TO=sum(r['TO'] for r in rr), max_steps_not_TO=max(r['maxsteps'] for r in rr))
        out[str(K)] = dict(rows=rows, mismatches=[r for r in res if not r['match']][:12], time_s=time.time() - t0)
        print(K, json.dumps(rows), '%.0fs' % (time.time() - t0), flush=True)
    json.dump(out, open(os.path.join(RUNS, 'sog-realizable-gap.json'), 'w'), indent=1)


# ----------------------------------------------------------------------------------------------------------------
# static analysis (notes §1.4)
# ----------------------------------------------------------------------------------------------------------------
import union as UN
PAY = UN.payoff_table(0.5)
MODAL = dict(Dstar=9.7e-9, constant=0.1025, militant=1.2e-3, militant_minus=1.2e-3, scab=0.480, striker=0.480)


def named_classes(T):
    cat = catalogue()
    w = cat.roles['W']; b = cat.roles['B']
    nw = {nm: int(T['cls1'][w['tau_of'][S.dt(x)]]) for nm, x in S.NAMED_W.items()}
    nb = {nm: int(T['clsb'][b['tau_of'][S.dt(x)]]) for nm, x in S.NAMED_B.items()}
    nb['D*_2'] = int(T['clsb'][T['nb_cat']])
    return nw, nb


def triple_J(T, bs, x, y):
    """Joint codes of boss classes bs (array) against the class pair (x, y)."""
    c = T['PV'][x, y]
    a = T['FBA'][bs, c].astype(np.int64); be = T['FBB'][bs, c].astype(np.int64)
    return 4 * a + T['EA'][be, x, y].astype(np.int64)


def pay_of(T, J, x, y, s):
    return PAY[J, T['tag1'][x], T['tag2'][y], s]


def code_combos(T, masses):
    """Per realized code: the distinct (action, view) pairs of boss classes and their summed masses (per prior)."""
    nc = len(T['ucodes'])
    out = []
    nm = len(next(iter(masses.values())))
    keyall = T['FBA'][:nm].astype(np.int64) * 64 + T['FBB'][:nm].astype(np.int64)      # (nbc, ncode)
    for c in range(nc):
        k = keyall[:, c]
        u, inv = np.unique(k, return_inverse=True)
        ms = {p: np.bincount(inv, weights=m, minlength=len(u)) for p, m in masses.items()}
        out.append((u // 64, u % 64, ms))
    return out


def static(args):
    t0 = time.time()
    T = tables()
    cat = catalogue()
    w = cat.roles['W']; b = cat.roles['B']
    nw, nb = named_classes(T)
    out = {}
    nB, nW = len(T['repb']), len(T['rep1'])
    assert np.array_equal(T['cls1'], T['cls2'])
    out['counts'] = dict(worker_spellings=len(w['spellings']), worker_run_trees=len(w['dt']), worker_classes=nW,
                         worker_tagged_classes=int(T['tag1'].sum()), boss_spellings=len(b['spellings']),
                         boss_run_trees=len(b['dt']), boss_classes=nB - T['n_extra'], realized_probe_codes=len(T['ucodes']),
                         boss_views=[''.join(v[0] for v in be) for be in T['betas']])
    # ---- masses
    pri = {}
    for p in ('L', 'X'):
        mb, mw = class_masses(T, p)
        pri[p] = (mb, mw)
    nbc = nB - T['n_extra']
    ub = np.zeros(nB); ub[:nbc] = 1.0 / nbc
    uw = np.full(nW, 1.0 / nW)
    pri['U'] = (ub, uw)
    # representative-length masses (shortest spelling of the class)
    rl = {}
    for role, r in (('W', w), ('B', b)):
        nd = cat.tau_repr_nodes(role)
        Z = (2.0 ** (-r['nodes'].astype(float))).sum()
        cls = T['cls1'] if role == 'W' else T['clsb'][:len(nd)]
        best = np.full(cls.max() + 1, 99)
        np.minimum.at(best, cls, nd)
        rl[role] = 2.0 ** (-best.astype(float)) / Z
    mL_b, mL_w = pri['L']
    named_mass = {}
    for nm, c in nb.items():
        named_mass['B ' + nm] = dict(L=float(mL_b[c]), L_repr=float(rl['B'][c]) if c < len(rl['B']) else 0.0,
                                     X=float(pri['X'][0][c]), U=float(ub[c]),
                                     spelling_L=float(2.0 ** -S.nodes(S.NAMED_B.get(nm, S.NAMED_B_OUT.get(nm))) / (2.0 ** (-b['nodes'].astype(float))).sum()))
    for nm, c in nw.items():
        named_mass['W ' + nm] = dict(L=float(mL_w[c]), L_repr=float(rl['W'][c]), X=float(pri['X'][1][c]), U=float(uw[c]),
                                     spelling_L=float(2.0 ** -S.nodes(S.NAMED_W[nm]) / (2.0 ** (-w['nodes'].astype(float))).sum()))
    consts = [nb[S.bname(c)] for c in range(9)]
    cmean = float(np.mean([mL_b[c] for c in consts]))
    out['masses'] = dict(named=named_mass,
                         ratios=dict(Dstar_over_constant_class=float(mL_b[nb['D*']] / cmean),
                                     Dstar_over_constant_class_log2=float(np.log2(mL_b[nb['D*']] / cmean)),
                                     Dstar_over_constant_spelling_log2=-6.0,
                                     T1_over_striker_class=float(mL_w[nw['T1']] / mL_w[nw['striker']]),
                                     T1_over_striker_class_log2=float(np.log2(mL_w[nw['T1']] / mL_w[nw['striker']])),
                                     modal_Dstar_over_constant_log2=float(np.log2(MODAL['Dstar'] / MODAL['constant']))),
                         constant_class_mean_L=cmean, constant_classes_total_L=float(sum(mL_b[c] for c in consts)),
                         boss_constant_classes_total_X=float(sum(pri['X'][0][c] for c in consts)),
                         worker_scab_striker_X=float(pri['X'][1][nw['scab']] + pri['X'][1][nw['striker']]))
    print('masses done %.0fs' % (time.time() - t0), flush=True)
    # ---- the fair state F* and its invaders
    t1, sc = nw['T1'], nw['scab']
    allb = np.arange(nbc)
    allw = np.arange(nW)

    def invaders(bc, x, y):
        J0 = triple_J(T, np.array([bc]), x, y)[0]
        res = {}
        Jb = triple_J(T, allb, x, y)
        ub_ = pay_of(T, Jb, x, y, 0); u0 = pay_of(T, J0, x, y, 0)
        res['B'] = dict(strict_mass=float(mL_b[allb][ub_ > u0 + 1e-12].sum()), neutral_mass=float(mL_b[allb][np.abs(ub_ - u0) <= 1e-12].sum()),
                        strict_n=int((ub_ > u0 + 1e-12).sum()))
        for s, fx in ((1, lambda q: (q, y)), (2, lambda q: (x, q))):
            us = np.array([pay_of(T, triple_J(T, np.array([bc]), *fx(q))[0], *fx(q), s) for q in allw])
            u0s = pay_of(T, J0, x, y, s)
            st = us > u0s + 1e-12; ne = np.abs(us - u0s) <= 1e-12
            res['W%d' % s] = dict(strict_mass=float(mL_w[st].sum()), neutral_mass=float(mL_w[ne].sum()), strict_n=int(st.sum()),
                                  neutral_top=[(S.show_dt(w['dt'][T['rep1'][q]]), float(mL_w[q])) for q in np.argsort(-mL_w * ne)[:5] if ne[q]])
        res['play'] = UN.joint_name(int(J0)); res['summary'] = UN.SUMM[UN.summary(int(J0), int(T['tag1'][x]), int(T['tag2'][y]))]
        return res
    states = {'F* = (D*, T1, T1)': (nb['D*'], t1, t1), '(D*, T1, scab)': (nb['D*'], t1, sc), '(D*, scab, T1)': (nb['D*'], sc, t1),
              '(D*, T0, T0)': (nb['D*'], nw['T0'], nw['T0']), '(D0, T0, T0)': (nb['D0'], nw['T0'], nw['T0']),
              '(D*_2, T1, T1)': (nb['D*_2'], t1, t1), '(pay(1/2,none), T1, T1)': (nb['pay(1/2,none)'], t1, t1),
              '(pay(1/2,none), T1, scab)': (nb['pay(1/2,none)'], t1, sc), '(pay(0,none), T1, scab)': (nb['pay(0,none)'], t1, sc),
              '(WF, T1, T1)': (nb['WF'], t1, t1)}
    out['states'] = {k: invaders(*v) for k, v in states.items()}
    print('states done %.0fs' % (time.time() - t0), flush=True)
    # ---- fakers: every boss class against the militant (T1's class) beside every partner, both slots
    fk = dict(T1_low_wage_work_triples=0, T1_low_wage_work_boss_classes=0)
    bad = set()
    for y in allw:
        for (x_, y_, s) in ((t1, y, 1), (y, t1, 2)):
            J = triple_J(T, allb, x_, y_)
            wage = (J // 4) // 3
            works = ((J // 2) % 2 == 0) if s == 1 else (J % 2 == 0)
            m = (wage < 2) & works
            fk['T1_low_wage_work_triples'] += int(m.sum())
            bad.update(np.nonzero(m)[0].tolist())
    fk['T1_low_wage_work_boss_classes'] = len(bad)
    JW = triple_J(T, allb, t1, t1)
    fk['T1_pair_plays_by_boss_mass_L'] = {}
    for jv in np.unique(JW):
        fk['T1_pair_plays_by_boss_mass_L'][UN.joint_name(int(jv))] = float(mL_b[allb][JW == jv].sum())
    fk['WF_vs_T1_pair'] = UN.joint_name(int(triple_J(T, np.array([nb['WF']]), t1, t1)[0]))
    out['fakers'] = fk
    # ---- low-wage work classification over the prior (L^3), and the coalition masses
    combos = code_combos(T, {p: pri[p][0][:nbc] for p in pri})
    PVa = T['PV']; EA = T['EA']
    rep1 = T['rep1']
    dts = [w['dt'][rep1[x]] for x in range(nW)]

    def truthful(x, act, other_action, slot):
        def val(at):
            if at[0] == 'B': return act in at[1]
            return other_action in at[1]
        return S.LEAFVAL[S.dt_eval(dts[x], val)]
    lw = {p: dict(accepts=0.0, uncertified_default=0.0, total_low_wage_work=0.0) for p in pri}
    coal = {p: 0.0 for p in pri}
    coal_conc = {p: 0.0 for p in pri}
    coal_const = {p: 0.0 for p in pri}
    nfair_pairs = 0
    concession = set()
    # concession bosses: pay 1/2 to the T1 pair and less to the scab pair
    Jt = triple_J(T, allb, t1, t1); Js = triple_J(T, allb, sc, sc)
    conc_mask = ((Jt // 4) // 3 == 2) & ((Js // 4) // 3 < 2)
    const_mask = np.zeros(nbc, bool); const_mask[consts] = True
    for x in range(nW):
        for y in range(nW):
            c = PVa[x, y]
            acts, bes, ms = combos[c]
            J = 4 * acts + EA[bes, x, y]
            a1 = (J // 2) % 2; a2 = J % 2
            wage = (acts // 3)
            ub_ = PAY[J, T['tag1'][x], T['tag2'][y], 0]
            # low-wage work
            for k in range(len(acts)):
                if wage[k] == 2: continue
                for (s, aw, other) in ((1, a1[k], a2[k]), (2, a2[k], a1[k])):
                    if aw != 0: continue
                    q = x if s == 1 else y
                    tr = truthful(q, int(acts[k]), 'CD'[other], s)
                    kind = 'uncertified_default' if tr == 'D' else 'accepts'
                    for p in pri:
                        mm = ms[p][k] * pri[p][1][x] * pri[p][1][y]
                        lw[p][kind] += mm; lw[p]['total_low_wage_work'] += mm
            # coalitions: fair play with no strict boss invader (no worker can exceed 1/2)
            summ = np.array([UN.summary(int(j), int(T['tag1'][x]), int(T['tag2'][y])) for j in J])
            fair = summ == 0
            if not fair.any(): continue
            MB = ub_.max()
            ok = fair & (ub_ >= MB - 1e-12)
            if not ok.any(): continue
            nfair_pairs += 1
            for p in pri:
                coal[p] += ms[p][ok].sum() * pri[p][1][x] * pri[p][1][y]
    out['low_wage_work'] = lw
    # coalition masses split by boss kind (exact per class)
    for x in range(nW):
        for y in range(nW):
            J = triple_J(T, allb, x, y)
            ub_ = pay_of(T, J, x, y, 0)
            summ_fair = (((J // 4) // 3) == 2) & ((J // 2) % 2 == 0) & (J % 2 == 0) & \
                        ~((((J // 4) % 3) == 2) & ((T['tag1'][x] + T['tag2'][y]) > 0))
            if not summ_fair.any(): continue
            ok = summ_fair & (ub_ >= ub_.max() - 1e-12)
            for p in pri:
                wxy = pri[p][1][x] * pri[p][1][y]
                coal_conc[p] += pri[p][0][:nbc][ok & conc_mask].sum() * wxy
                coal_const[p] += pri[p][0][:nbc][ok & const_mask].sum() * wxy
    out['coalitions'] = dict(mass=coal, concession_boss_mass=coal_conc, constant_boss_mass=coal_const, fair_compatible_pairs=nfair_pairs,
                             modal_hand_estimate=3 * MODAL['constant'] * (2 * MODAL['militant_minus'] * MODAL['scab'] + MODAL['militant_minus'] ** 2),
                             concession_classes=int(conc_mask.sum()), concession_mass={p: float(pri[p][0][:nbc][conc_mask].sum()) for p in pri})
    print('coalitions done %.0fs' % (time.time() - t0), flush=True)
    # ---- RR, derived (realizable semantics: probes certify recommendations; wage stage-1; whack -> none)
    def rr_J(J):
        a = J // 4; s = a // 3
        ex = np.where(s > 0, 0, J % 4)
        return 4 * (3 * s + 1) + ex
    rr = {}
    for k, (bc, x, y) in states.items():
        J0 = triple_J(T, np.array([bc]), x, y)[0]
        JR = rr_J(np.array([J0]))[0]
        Jb = rr_J(triple_J(T, allb, x, y))
        ub_ = pay_of(T, Jb, x, y, 0); u0 = pay_of(T, JR, x, y, 0)
        best = np.argmax(ub_)
        rr[k] = dict(play=UN.joint_name(int(JR)), strict_boss_invader_mass=float(mL_b[allb][ub_ > u0 + 1e-12].sum()),
                     best_boss=UN.joint_name(int(Jb[best])), best_boss_payoff=float(ub_[best]))
    c11 = T['ucodes'][T['PV'][t1, t1]]
    rr_probe = {S.atom_name(at): S.VNAME[int(c11[i])] for i, at in enumerate(S.BOSS_ATOMS)}
    out['RR'] = dict(states=rr, T1_pair_probe_code=rr_probe,
                     quarter_probe_certifies_T1_recommendation=rr_probe['P1^1/4:S'] == 'T')
    out['time_s'] = time.time() - t0
    json.dump(out, open(os.path.join(RUNS, 'sog-realizable-static.json'), 'w'), indent=1, default=float)
    print(json.dumps(out['counts']), '\n', json.dumps(out['masses']['ratios']), '\n', json.dumps(out['coalitions']), '\n',
          json.dumps(out['fakers'])[:800], flush=True)


# ----------------------------------------------------------------------------------------------------------------
# the seed lottery (notes §1.3.7)
# ----------------------------------------------------------------------------------------------------------------
import sog_lottery as SL
KEYT = SL.KEYT.astype(np.int64)
GENS = 2000
CHECK_EVERY = 10
FAIR_WINDOW = 10
WFSTAR_MASS = 0.0116            # the modal run's strict faker entry mass at F* (0.0095 + 0.0021, RESULTS "Concessions")
FORCED_PER_ISLAND = 20


def jm_cc():
    return np.arange(36, dtype=np.int64)


def jm_rr():
    jm = np.zeros(36, np.int64)
    for j in range(36):
        b = j // 4; s = b // 3
        jm[j] = 4 * (3 * s + 1) + (0 if s > 0 else j % 4)
    return jm


def rr_exec_tables(T):
    """The modal-matched RR variant: probes read executed actions (at s' = 1/4 every worker executes work, so
    P_j^1/4:W = T and P_j^1/4:S = F); boss views on the modified codes computed by the abstract evaluator."""
    cat = catalogue()
    codes = T['ucodes'].copy()
    mod = codes.copy()
    for k, at in enumerate(S.BOSS_ATOMS):
        if at[2] == 1:
            mod[:, k] = 1 if at[3] == S.A_WORK else 0
    allc, inv = np.unique(np.concatenate([codes, mod]), axis=0, return_inverse=True)
    new_of_old = inv[len(codes):]
    b = cat.roles['B']
    bdt = list(b['dt']) + [S.dt(S.NAMED_B_OUT['D*_2'])]
    bacc = list(b['acc']) + [S.produce_lists(bdt[-1], 'B')[1]]
    saved = (b['dt'], b['acc']); b['dt'], b['acc'] = bdt, bacc
    try:
        act, bet = S.boss_view_table(cat, allc)
    finally:
        b['dt'], b['acc'] = saved
    # class-level arrays on the modified codes (classes as in the main tables: representatives)
    rep_tree = np.concatenate([T['repb'][:len(T['repb']) - T['n_extra']], [len(b['dt'])]])
    bid = np.zeros(bet.shape[:2], np.int64)
    betas = list(T['betas'])
    for r in np.unique(bet.reshape(-1, 3), axis=0):
        be = tuple(S.VNAME[int(v)] for v in r)
        if be not in betas: raise RuntimeError('new view under RR-exec: %s' % (be,))
    for be, i in T['beta_id'].items():
        m = np.all(bet == np.array([S.VCODE[v] for v in be], np.int8), axis=2)
        bid[m] = i
    FBA = act[rep_tree].astype(np.int8); FBB = bid[rep_tree].astype(np.int8)
    PV = new_of_old[T['PV']]
    return dict(FBA=FBA, FBB=FBB, PV=PV)


def cell_config(name, T):
    """Priors (boss classes incl. extras; worker classes), sizes, joint-code map, table overrides."""
    nB = len(T['repb']); nbc = nB - T['n_extra']; nW = len(T['rep1'])
    nw, nb = named_classes(T)
    mbL, mwL = class_masses(T, 'L')
    cfg = dict(name=name, N=100, I=64, mN=1.0, jm=jm_cc(), extra_wf=False, forced=None, runs=40, tables=None)
    pb = mbL.copy(); pw = mwL.copy()
    if name in ('L', 'L200', 'L256', 'RR', 'RRexec', 'L+WF*'):
        pass
    if name == 'L200': cfg['N'] = 200
    if name == 'L256': cfg['I'] = 256
    if name == 'U':
        pb = np.zeros(nB); pb[:nbc] = 1.0 / nbc
        pw = np.full(nW, 1.0 / nW)
    if name == 'X':
        pb, pw = class_masses(T, 'X')
    if name in ('RR', 'RRexec'):
        cfg['jm'] = jm_rr()
    if name == 'RRexec':
        f = os.path.join(OUT, 'rrexec_tables.pkl')
        if not os.path.exists(f):
            pickle.dump(rr_exec_tables(T), open(f, 'wb'))
        cfg['tables'] = pickle.load(open(f, 'rb'))
    if name.startswith('Lmil') or name.startswith('forced'):
        pw = pw.copy(); pw[nw['T1']] += pw[nw['striker']]; pw[nw['striker']] = 0.0
    if name.endswith('+WF*'):
        cfg['extra_wf'] = True
    if name == 'Lmil-ablate':
        Jt = triple_J(T, np.arange(nbc), nw['T1'], nw['T1']); Js = triple_J(T, np.arange(nbc), nw['scab'], nw['scab'])
        conc = ((Jt // 4) // 3 == 2) & ((Js // 4) // 3 < 2)
        pb = pb.copy(); pb[:nbc][conc] = 0.0
        cfg['ablated_mass'] = float(mbL[:nbc][conc].sum()); cfg['ablated_classes'] = int(conc.sum())
    if name == 'forcedD*': cfg['forced'] = nb['D*']
    if name == 'forcedD*2': cfg['forced'] = nb['D*_2']
    pb = pb / pb.sum(); pw = pw / pw.sum()
    cfg['pb'] = pb; cfg['pw'] = pw
    return cfg


def masks(T, cfg, ids):
    """Boss masks (concession, constant 1/2, probe-reading, WF*) over local boss ids; worker masks (militant T1 class,
    scab, striker, tagged)."""
    nw, nb = named_classes(T)
    nB = len(T['repb']); nbc = nB - T['n_extra']
    allb = np.arange(nB)
    Jt = triple_J(T, allb, nw['T1'], nw['T1']); Js = triple_J(T, allb, nw['scab'], nw['scab'])
    conc = ((Jt // 4) // 3 == 2) & ((Js // 4) // 3 < 2)
    half = np.zeros(nB, bool); half[[nb['pay(1/2,%s)' % h] for h in S.HN]] = True
    probe = np.array([len(np.unique(T['FBA'][k])) > 1 for k in range(nB)])
    def pick(arr, wf_value):
        return np.array([wf_value if g < 0 else arr[g] for g in ids])
    MB = np.stack([pick(conc, False), pick(half, False), pick(probe, False), np.array([g < 0 for g in ids])])
    nW = len(T['rep1'])
    MW = np.zeros((4, nW), bool)
    MW[0, nw['T1']] = True; MW[1, nw['scab']] = True; MW[2, nw['striker']] = True; MW[3] = T['tag1'].astype(bool)
    return MB, MW


BMASKS = ['concession', 'constant 1/2', 'probe-reading', 'WF*']
WMASKS = ['militant (T1 class)', 'scab', 'striker', 'tagged']


def local_tables(T, cfg, ids):
    """Class-level arrays restricted to the local boss ids (-1 = WF*), padded to Kmax rows."""
    tb = cfg['tables'] or T
    nW = len(T['rep1'])
    K = max(len(ids), nW)
    nc = tb['FBA'].shape[1]
    FBA = np.zeros((K, nc), np.int64); FBB = np.zeros((K, nc), np.int64)
    half_view = T['beta_id'][S.beta_of_code(7)]
    for k, g in enumerate(ids):
        if g < 0:
            FBA[k] = 1; FBB[k] = half_view
        else:
            FBA[k] = tb['FBA'][g]; FBB[k] = tb['FBB'][g]
    tag = np.zeros(K, np.int64); tag[:nW] = T['tag1']
    return FBA, FBB, tb['PV'].astype(np.int64), T['EA'].astype(np.int64), tag, K


def seed_run(T, cfg, seed):
    """iid seeds: boss classes (and forced copies), worker classes for both slots.  Returns (ids, init counts)."""
    rng = np.random.default_rng(seed)
    I, N = cfg['I'], cfg['N']
    nB = len(cfg['pb'])
    pb = cfg['pb']
    if cfg['extra_wf']:
        pbx = np.concatenate([pb * (1 - WFSTAR_MASS), [WFSTAR_MASS]])
    else:
        pbx = pb
    bdraw = rng.choice(len(pbx), size=(I, N), p=pbx)
    if cfg['extra_wf']:
        bdraw = np.where(bdraw == nB, -1, bdraw)
    w1 = rng.choice(len(cfg['pw']), size=(I, N), p=cfg['pw'])
    w2 = rng.choice(len(cfg['pw']), size=(I, N), p=cfg['pw'])
    if cfg['forced'] is not None:
        pos = np.array([rng.choice(N, FORCED_PER_ISLAND, replace=False) for _ in range(I)])
        for i in range(I):
            bdraw[i, pos[i]] = cfg['forced']
    ids = sorted(set(bdraw.ravel().tolist()))
    loc = {g: k for k, g in enumerate(ids)}
    nW = len(cfg['pw'])
    K = max(len(ids), nW)
    init = np.zeros((I, 3, K), np.int64)
    for i in range(I):
        for g in bdraw[i]: init[i, 0, loc[g]] += 1
        np.add.at(init[i, 1], w1[i], 1)
        np.add.at(init[i, 2], w2[i], 1)
    return ids, init


def fair_flags(stats):
    sm = stats[:, :, :7]
    return sm[:, :, 0] > np.max(sm[:, :, 1:], axis=2) + 1e-12


def island_joint(T, cfg, ids, FBA, FBB, PV, EA, jm, cnt0, cnt1, cnt2):
    """Fair share of the encounter distribution of slot populations (counts over local ids / worker classes)."""
    bs = np.nonzero(cnt0)[0]; xs = np.nonzero(cnt1)[0]; ys = np.nonzero(cnt2)[0]
    c = PV[np.ix_(xs, ys)]
    J = jm[4 * FBA[bs][:, c] + EA[FBB[bs][:, c], xs[None, :, None], ys[None, None, :]]]
    return bs, xs, ys, J


_JOB = {}


def run_cell_job(args):
    name, seed, T_path = args
    if 'T' not in _JOB:
        _JOB['T'] = pickle.load(open(T_path, 'rb'))
    T = _JOB['T']
    if _JOB.get('name') != name:
        _JOB['cfg'] = cell_config(name, T); _JOB['name'] = name
    return run_one(T, _JOB['cfg'], seed)


def run_one(T, cfg, seed, keep_counts=False, checks_upto=None, init_override=None, ids_override=None, m_override=None):
    ids, init = (ids_override, init_override) if init_override is not None else seed_run(T, cfg, seed)
    FBA, FBB, PV, EA, tag, K = local_tables(T, cfg, ids)
    if init.shape[2] < K:
        init = np.concatenate([init, np.zeros(init.shape[:2] + (K - init.shape[2],), np.int64)], axis=2)
    MB, MW = masks(T, cfg, ids)
    MBp = np.zeros((MB.shape[0], K), np.bool_); MBp[:, :MB.shape[1]] = MB
    MWp = np.zeros((MW.shape[0], K), np.bool_); MWp[:, :MW.shape[1]] = MW
    gens = GENS if checks_upto is None else checks_upto
    checks = np.arange(CHECK_EVERY, gens + 1, CHECK_EVERY, dtype=np.int64)
    nstat = 10 + MB.shape[0] + 2 * MW.shape[0]
    N = cfg['N']; m = (cfg['mN'] if m_override is None else m_override) / N
    t0 = time.time()
    status, stop_gen, counts, stats, modal, modalc, nmig, ci = S.kern3(cfg['jm'], FBA, FBB, PV, EA, tag, PAY, KEYT, MBp, MWp,
                                                                    init, N, 0.3, m, seed % (2 ** 31), checks, nstat)
    # frozen after global closure: extend to the horizon
    nck = len(checks) + 1
    if stats.shape[0] < nck:
        pad = nck - stats.shape[0]
        stats = np.concatenate([stats, np.repeat(stats[-1:], pad, axis=0)])
        modal = np.concatenate([modal, np.repeat(modal[-1:], pad, axis=0)])
        modalc = np.concatenate([modalc, np.repeat(modalc[-1:], pad, axis=0)])
    res = dict(seed=seed, status=int(status), stop_gen=int(stop_gen), nmig=int(nmig), time_s=time.time() - t0,
               stats=stats.astype(np.float32), modal=modal, modalc=modalc, ids=np.array(ids), I=cfg['I'], N=N)
    res['init'] = init
    res['counts'] = counts
    return res


def summarize_run(T, cfg, r, compat=None):
    """Per-run outcomes (notes §1.3.7)."""
    st = r['stats']; I = r['I']
    fair = fair_flags(st)                       # (nck, I)
    nck = fair.shape[0]
    gens = np.arange(nck) * CHECK_EVERY
    # windows of FAIR_WINDOW consecutive fair checks
    win_end = np.full(I, -1)
    for i in range(I):
        run = 0
        for c in range(nck):
            run = run + 1 if fair[c, i] else 0
            if run >= FAIR_WINDOW:
                win_end[i] = c; break
    est_islands = win_end >= 0
    est_gen = int(gens[win_end[est_islands].min()]) if est_islands.any() else None
    est_start = int(gens[win_end[est_islands].min() - FAIR_WINDOW + 1]) if est_islands.any() else None
    # residence and exits
    resid = []; exits = []
    nw, nb = named_classes(T)
    mil = nw['T1']
    ids = r['ids']
    half_classes = set(nb['pay(1/2,%s)' % h] for h in S.HN)
    for i in np.nonzero(est_islands)[0]:
        s0 = win_end[i] - FAIR_WINDOW + 1
        after = np.nonzero(~fair[win_end[i]:, i])[0]
        if len(after) == 0:
            resid.append((int((nck - 1 - s0) * CHECK_EVERY), True)); continue
        c = win_end[i] + after[0]
        resid.append((int((c - s0) * CHECK_EVERY), False))
        mb0, mb1 = r['modal'][c - 1, i, 0], r['modal'][c, i, 0]
        w0 = r['modal'][s0:c, i, 1:]; w1n = r['modal'][c, i, 1:]
        boss_change = mb0 != mb1
        wdrift_before = bool((w0 != w0[0]).any() or (w1n != w0[-1]).any())
        mil_lost = bool(((w0[0] == mil) & (w1n != mil)).any())
        if boss_change and wdrift_before:
            kind = 'worker drift then boss change'
        elif boss_change:
            kind = 'boss change'
        elif wdrift_before:
            kind = 'worker drift'
        else:
            kind = 'composition shift (no modal change)'
        exits.append(dict(island=int(i), gen=int(gens[c]), kind=kind, militant_lost=mil_lost))
    fin = st[-1]
    summ = fin[:, :7]
    plural = np.argmax(summ, axis=1)
    pay = fin[:, 7:10]
    tot = pay.sum(1)
    elig = tot > 1e-9
    share_ok = np.where(elig, pay.min(1) / np.where(elig, tot, 1) >= 1 / 6 - 1e-12, False)
    out = dict(seed=r['seed'], status=r['status'], stop_gen=r['stop_gen'], nmig=r['nmig'],
               established=est_gen is not None, est_gen=est_gen, est_start=est_start, n_established_islands=int(est_islands.sum()),
               persistence=float(fair[-1].mean()), persistence10=float(fair[-FAIR_WINDOW:].all(axis=0).mean()),
               plural_frac={UN.SUMM[k]: float((plural == k).mean()) for k in range(7)},
               mean_summary={UN.SUMM[k]: float(summ[:, k].mean()) for k in range(7)},
               mean_payoffs=pay.mean(0).tolist(), three_role=float(share_ok.mean()),
               residence=resid, exits=exits,
               boss_masks_t={BMASKS[z]: st[:, :, 10 + z].mean(1).tolist()[::10] for z in range(len(BMASKS))},
               worker_masks_t={WMASKS[z]: (0.5 * (st[:, :, 10 + len(BMASKS) + 2 * z] + st[:, :, 11 + len(BMASKS) + 2 * z])).mean(1).tolist()[::10]
                               for z in range(len(WMASKS))},
               fair_t=fair.mean(1).tolist()[::10], zero_t=(st[:, :, 2] / np.maximum(st[:, :, :7].sum(2), 1e-12)).mean(1).tolist()[::10],
               repression_t=(st[:, :, 5] + st[:, :, 6]).mean(1).tolist()[::10], time_s=r['time_s'])
    # occupancy at seeding: a compatible founding coalition present on the island
    if compat is not None:
        occ = occupancy(T, cfg, r, compat)
        out['occupied'] = occ.tolist()
        out['est_given_occ'] = [bool(est_islands[i]) for i in range(I)]
    # E3-type endpoint and cross-island P(fair)
    out.update(endpoint_e3(T, cfg, r))
    return out


def occupancy(T, cfg, r, compat):
    """compat: (nW, nW) boss-payoff ceiling ok (max boss payoff over catalogue classes <= 1)."""
    FBA, FBB, PV, EA, tag, K = local_tables(T, cfg, list(r['ids']))
    jm = cfg['jm']
    init = r['init']
    occ = np.zeros(r['I'], bool)
    for i in range(r['I']):
        bs, xs, ys, J = island_joint(T, cfg, r['ids'], FBA, FBB, PV, EA, jm, init[i, 0], init[i, 1], init[i, 2])
        fair = ((J // 4) // 3 == 2) & ((J // 2) % 2 == 0) & (J % 2 == 0) & ~(((J // 4) % 3 == 2) & ((tag[xs][None, :, None] + tag[ys][None, None, :]) > 0))
        ok = fair & compat[np.ix_(xs, ys)][None, :, :]
        occ[i] = bool(ok.any())
    return occ


def endpoint_e3(T, cfg, r):
    """E3-type endpoint per island (closure of entrants among globally present classes) and cross-island P(fair)."""
    FBA, FBB, PV, EA, tag, K = local_tables(T, cfg, list(r['ids']))
    jm = cfg['jm']
    cnt = r['counts']
    I = r['I']; N = r['N']
    glob = [np.nonzero(cnt[:, s].sum(0))[0] for s in range(3)]

    def payoffs(bs, xs, ys):
        c = PV[np.ix_(xs, ys)]
        J = jm[4 * FBA[bs][:, c] + EA[FBB[bs][:, c], xs[None, :, None], ys[None, None, :]]]
        t1 = tag[xs][None, :, None]; t2 = tag[ys][None, None, :]
        return J, PAY[J, np.broadcast_to(t1, J.shape), np.broadcast_to(t2, J.shape)]
    res = []
    for i in range(I):
        Z = [set(np.nonzero(cnt[i, s])[0].tolist()) for s in range(3)]
        changed = True; it = 0
        while changed and it < 50:
            changed = False; it += 1
            for s in range(3):
                zb, zx, zy = (np.array(sorted(Z[0])), np.array(sorted(Z[1])), np.array(sorted(Z[2])))
                for q in glob[s]:
                    if q in Z[s]: continue
                    if s == 0:
                        _, Pq = payoffs(np.array([q]), zx, zy); _, Pz = payoffs(zb, zx, zy)
                        ok = bool((Pq[0, :, :, 0][None] >= Pz[:, :, :, 0] - 1e-12).any())
                    elif s == 1:
                        _, Pq = payoffs(zb, np.array([q]), zy); _, Pz = payoffs(zb, zx, zy)
                        ok = bool((Pq[:, 0:1, :, 1] >= Pz[:, :, :, 1] - 1e-12).any())
                    else:
                        _, Pq = payoffs(zb, zx, np.array([q])); _, Pz = payoffs(zb, zx, zy)
                        ok = bool((Pq[:, :, 0:1, 2] >= Pz[:, :, :, 2] - 1e-12).any())
                    if ok:
                        Z[s].add(int(q)); changed = True
        zb, zx, zy = (np.array(sorted(Z[0])), np.array(sorted(Z[1])), np.array(sorted(Z[2])))
        J, _ = payoffs(zb, zx, zy)
        t1 = tag[zx][None, :, None]; t2 = tag[zy][None, None, :]
        summ = np.vectorize(lambda j, a, b: UN.summary(int(j), int(a), int(b)))(J, np.broadcast_to(t1, J.shape), np.broadcast_to(t2, J.shape))
        u = np.unique(summ)
        res.append(UN.SUMM[int(u[0])] if len(u) == 1 else 'unresolved')
    # cross-island P(fair): boss from island i, workers from island j != i
    cross = []
    for i in range(I):
        bs = np.nonzero(cnt[i, 0])[0]
        for j in range(I):
            if j == i: continue
            xs = np.nonzero(cnt[j, 1])[0]; ys = np.nonzero(cnt[j, 2])[0]
            J, _ = payoffs(bs, xs, ys)
            w = cnt[i, 0, bs][:, None, None] * cnt[j, 1, xs][None, :, None] * cnt[j, 2, ys][None, None, :] / float(N) ** 3
            fair = ((J // 4) // 3 == 2) & ((J // 2) % 2 == 0) & (J % 2 == 0) & ~(((J // 4) % 3 == 2) & ((tag[xs][None, :, None] + tag[ys][None, None, :]) > 0))
            cross.append(float((w * fair).sum()))
        if i > 8: break                          # a sample of source islands (cost), all targets
    e3 = {k: res.count(k) / I for k in set(res)}
    return dict(e3=e3, e3_universal_fair=all(x == 'fair' for x in res), cross_fair=float(np.mean(cross)))


def compat_matrix(T, nbc=None):
    """(nW, nW): the maximum boss payoff against the pair over catalogue boss classes is <= 1 (no strict boss invader of
    a fair play on that pair)."""
    nB = len(T['repb']); nbc = nB - T['n_extra'] if nbc is None else nbc
    nW = len(T['rep1'])
    M = np.zeros((nW, nW), bool)
    allb = np.arange(nbc)
    for x in range(nW):
        for y in range(nW):
            J = triple_J(T, allb, x, y)
            M[x, y] = pay_of(T, J, x, y, 0).max() <= 1 + 1e-12
    return M


def lottery(args):
    T = tables()
    tpath = os.path.join(OUT, 'tables.pkl')
    cpath = os.path.join(OUT, 'compat.npy')
    if not os.path.exists(cpath):
        np.save(cpath, compat_matrix(T))
    compat = np.load(cpath)
    cfg = cell_config(args.cell, T)
    runs = args.runs or cfg['runs']
    seeds = [1000 * (abs(hash(args.cell)) % 1000) + k for k in range(runs)] if args.cell not in ('forcedD*', 'forcedD*2') \
        else [777000 + k for k in range(runs)]          # matched seeds for the forced pair
    if args.cell in ('L', 'L+WF*', 'RR', 'RRexec', 'Lmil', 'Lmil+WF*', 'Lmil-ablate', 'X', 'U'):
        seeds = [500000 + k for k in range(runs)]       # paired seeds across the main controls
    t0 = time.time()
    _JOB['T'] = T; _JOB['cfg'] = cfg; _JOB['name'] = args.cell       # inherited by the forked workers
    from multiprocessing import get_context
    with get_context('fork').Pool(args.procs) as pool:
        res = pool.map(run_cell_job, [(args.cell, s, tpath) for s in seeds], chunksize=1)
    outs = []
    for r in res:
        outs.append(summarize_run(T, cfg, r, compat))
        if args.cell.startswith('forced'):
            np.savez_compressed(os.path.join(OUT, 'final_%s_%d.npz' % (args.cell, r['seed'])), counts=r['counts'], init=r['init'], ids=r['ids'])
    out = dict(cell=args.cell, cfg={k: (v if not isinstance(v, np.ndarray) else None) for k, v in cfg.items() if k not in ('tables',)},
               runs=outs, time_s=time.time() - t0)
    json.dump(out, open(os.path.join(OUT, 'cell_%s.json' % args.cell.replace('*', 'star')), 'w'), default=float)
    est = [o['established'] for o in outs]
    print('%s: %d runs, established %d, persistence %.3f, zero-plural %.3f, %.0fs' % (
        args.cell, len(outs), sum(est), np.mean([o['persistence'] for o in outs]),
        np.mean([o['plural_frac']['zero wage'] for o in outs]), time.time() - t0), flush=True)


# ----------------------------------------------------------------------------------------------------------------
# the diagnostic chain (notes §1.3.7): union_chain.UChain's hybrid explorer with J from the factorized table
# ----------------------------------------------------------------------------------------------------------------
from abm import njit
from dollar3_chain import log_rho
from union_chain import UChain, _bsearch


@njit(cache=True)
def _jf(FBA, FBB, PV, EA, b, x, y):
    c = PV[x, y]
    return 4 * FBA[b, c] + EA[FBB[b, c], x, y]


@njit(cache=True)
def _rows_f(FBA, FBB, PV, EA, tagc, PAY, logm, states, members, KcB, KcW, N, w, pi, theta_edge, mode):
    S_ = states.shape[0]
    cap = S_ * 16 + 1024
    src = np.empty(cap, np.int64); dst = np.empty(cap, np.int64); pr = np.empty(cap, np.float64)
    chg = np.empty(cap, np.bool_)
    out_chg = np.zeros(S_); cut_chg = 0.0
    out_tot = np.zeros(S_); pay = np.zeros((S_, 3)); typ = np.zeros(S_, np.int64)
    ne = 0
    cut = 0.0
    KK = KcW * KcW
    for i in range(S_):
        code = states[i]
        b = code // KK; x = (code // KcW) % KcW; y = code % KcW
        j0 = _jf(FBA, FBB, PV, EA, b, x, y)
        t1 = tagc[x]; t2 = tagc[y]
        r0 = PAY[j0, t1, t2, 0]; r1 = PAY[j0, t1, t2, 1]; r2 = PAY[j0, t1, t2, 2]
        pay[i, 0] = r0; pay[i, 1] = r1; pay[i, 2] = r2; typ[i] = j0 * 4 + t1 * 2 + t2
        for s in range(3):
            Kq = KcB if s == 0 else KcW
            res = b if s == 0 else (x if s == 1 else y)
            ures = r0 if s == 0 else (r1 if s == 1 else r2)
            for q in range(Kq):
                if q == res or logm[s, q] < -1e300:
                    continue
                if s == 0:
                    j = _jf(FBA, FBB, PV, EA, q, x, y); tq1 = t1; tq2 = t2
                    dcode = q * KK + x * KcW + y
                elif s == 1:
                    j = _jf(FBA, FBB, PV, EA, b, q, y); tq1 = tagc[q]; tq2 = t2
                    dcode = b * KK + q * KcW + y
                else:
                    j = _jf(FBA, FBB, PV, EA, b, x, q); tq1 = t1; tq2 = tagc[q]
                    dcode = b * KK + x * KcW + q
                u0 = PAY[j, tq1, tq2, 0]; u1 = PAY[j, tq1, tq2, 1]; u2 = PAY[j, tq1, tq2, 2]
                us = u0 if s == 0 else (u1 if s == 1 else u2)
                dw = w * (us - ures)
                lp = logm[s, q] + log_rho(dw, N)
                ep = np.exp(lp)
                out_tot[i] += ep
                ch = j != j0 or abs(u0 - r0) > 1e-12 or abs(u1 - r1) > 1e-12 or abs(u2 - r2) > 1e-12
                if ch:
                    out_chg[i] += ep
                jx = _bsearch(members, dcode)
                if mode == 0:
                    if jx < 0:
                        continue
                    val_store = lp; d_store = jx
                else:
                    if jx >= 0:
                        continue
                    fl = pi[i] + lp
                    cut += np.exp(fl)
                    if ch:
                        cut_chg += np.exp(fl)
                    if fl <= theta_edge:
                        continue
                    val_store = fl; d_store = dcode
                if ne >= cap:
                    cap2 = cap * 2
                    src2 = np.empty(cap2, np.int64); dst2 = np.empty(cap2, np.int64); pr2 = np.empty(cap2, np.float64)
                    chg2 = np.empty(cap2, np.bool_)
                    src2[:ne] = src[:ne]; dst2[:ne] = dst[:ne]; pr2[:ne] = pr[:ne]; chg2[:ne] = chg[:ne]
                    src, dst, pr, chg, cap = src2, dst2, pr2, chg2, cap2
                src[ne] = i; dst[ne] = d_store; pr[ne] = val_store; chg[ne] = ch; ne += 1
    return src[:ne], dst[:ne], pr[:ne], out_tot, pay, typ, cut, chg[:ne], out_chg, cut_chg


class FChain(UChain):
    def __init__(self, T, mB, mW, N, w=0.3, theta=1e-9, max_states=400000, core_max=2500, promote=1e-6, verbose=True):
        self.arm, self.N, self.w, self.c = 'sog-realizable', N, w, 0.5
        self.theta, self.max_states, self.max_rounds, self.verbose = theta, max_states, 60, verbose
        self.core_max, self.promote, self.drop_rel = core_max, promote, 1e-5
        from dollar3_solve import dense_log_gth
        from dollar3_chain import gth_scaled
        self.gth = dense_log_gth if N > 2000 else gth_scaled
        self.FBA = T['FBA'].astype(np.int64); self.FBB = T['FBB'].astype(np.int64)
        self.PV = T['PV'].astype(np.int64); self.EA = T['EA'].astype(np.int64)
        self.tagc = T['tag1'].astype(np.int64)
        self.KcB, self.KcW = len(mB), len(mW)
        self.Kc = self.KcW
        Km = max(self.KcB, self.KcW)
        mass = np.zeros((3, Km)); mass[0, :self.KcB] = mB; mass[1, :self.KcW] = mW; mass[2, :self.KcW] = mW
        self.mass = mass
        with np.errstate(divide='ignore'):
            self.logm = np.where(mass > 0, np.log(mass) - np.log(3.0), -np.inf)
        self.PAY = PAY

    def J(self, b, x, y):
        return int(_jf(self.FBA, self.FBB, self.PV, self.EA, b, x, y))

    def rows(self, codes, members=None, lpi=None, theta_edge=0.0, mode=0):
        codes = np.asarray(codes, np.int64)
        members = codes if members is None else np.asarray(members, np.int64)
        if lpi is None: lpi = np.zeros(len(codes))
        return _rows_f(self.FBA, self.FBB, self.PV, self.EA, self.tagc, self.PAY, self.logm, codes, members, self.KcB, self.KcW,
                       float(self.N), self.w, lpi, np.log(theta_edge) if theta_edge > 0 else -np.inf, mode)


def fexits(ch, code, top=10):
    b, x, y = ch.decode(code)
    tg = ch.tagc
    j0 = ch.J(b, x, y); r = PAY[j0, tg[x], tg[y]]
    out = []
    for s in range(3):
        K = ch.KcB if s == 0 else ch.KcW
        for q in range(K):
            t = [b, x, y]
            if t[s] == q or ch.mass[s, q] == 0: continue
            t[s] = q
            j = ch.J(*t); u = PAY[j, tg[t[1]], tg[t[2]]]
            du = u[s] - r[s]
            rho = float(np.exp(log_rho(ch.w * du, float(ch.N))))
            same = j == j0 and np.allclose(u, r)
            kind = 'strict' if du > 1e-12 else ('deleterious' if du < -1e-12 else ('neutral-keep' if same else 'neutral-change'))
            out.append(dict(slot=s, cls=q, mass=float(ch.mass[s, q] / 3), du=float(du), rho=rho, prob=float(ch.mass[s, q] / 3 * rho), kind=kind,
                            summ_to=UN.SUMM[UN.summary(j, tg[t[1]], tg[t[2]])]))
    tot = {k: sum(e['prob'] for e in out if e['kind'] == k) for k in ('strict', 'neutral-change', 'neutral-keep', 'deleterious')}
    tot_change = {}
    for e in out:
        if e['summ_to'] != UN.SUMM[UN.summary(j0, tg[x], tg[y])]:
            k = '%s %s' % (['B', 'W1', 'W2'][e['slot']], e['kind'])
            tot_change[k] = tot_change.get(k, 0.0) + e['prob']
    out.sort(key=lambda e: -e['prob'])
    return out[:top], tot, tot_change


def strict_ne(T, mB, mW, tol=1e-9):
    """Strict-NE monomorphic triples (closure seeds): unique best response with a strict margin in every slot."""
    nbc = len(mB); nW = len(mW)
    allb = np.nonzero(mB > 0)[0]
    out = []
    bestb = {}
    for x in range(nW):
        for y in range(nW):
            J = triple_J(T, allb, x, y); u = pay_of(T, J, x, y, 0)
            o = np.argsort(-u)
            if len(o) > 1 and u[o[0]] - u[o[1]] > tol:
                bestb[(x, y)] = int(allb[o[0]])
    for (x, y), b in bestb.items():
        ok = True
        for s in (1, 2):
            us = []
            for q in range(nW):
                xx, yy = (q, y) if s == 1 else (x, q)
                us.append(pay_of(T, triple_J(T, np.array([b]), xx, yy)[0], xx, yy, s))
            us = np.array(us); me = x if s == 1 else y
            o = np.argsort(-us)
            if o[0] != me or us[o[0]] - us[o[1]] <= tol:
                ok = False; break
        if ok: out.append((b, x, y))
    return out


def chain(args):
    t0 = time.time()
    T = tables()
    nw, nb = named_classes(T)
    nbc = len(T['repb']) - T['n_extra']
    mB, mW = class_masses(T, 'L')
    mB = mB[:nbc] / mB[:nbc].sum()
    ch = FChain(T, mB, mW, args.N, theta=args.theta)
    seeds = set()
    nbl = [v for k, v in nb.items() if v < nbc]
    nwl = list(nw.values())
    for b in nbl:
        for x in nwl:
            for y in nwl:
                seeds.add(ch.code(b, x, y))
    ne = strict_ne(T, mB, mW)
    for t in ne: seeds.add(ch.code(*t))
    # lottery endpoints of the main cell (modal triples), if present
    f = os.path.join(OUT, 'cell_L.json')
    print('seeds %d (strict NE %d), %.0fs' % (len(seeds), len(ne), time.time() - t0), flush=True)
    ch.explore_hybrid(sorted(seeds))
    pi = ch.pi; codes = ch.codes; typ = ch.typ
    j = typ // 4; t1 = (typ // 2) % 2; t2 = typ % 2
    summ = np.array([UN.summary(int(j[k]), int(t1[k]), int(t2[k])) for k in range(len(codes))])
    out = dict(N=args.N, theta=args.theta, states=len(codes), core=int(ch.is_core.sum()), strict_ne=len(ne),
               rel_cut=float(ch.rel_cut), rel_cut_change=float(ch.rel_cut_change), rounds=ch.log)
    out['summary'] = {UN.SUMM[k]: float(pi[summ == k].sum()) for k in range(7)}
    wage = (j // 4) // 3
    out['wage_offered'] = {['0', '1/4', '1/2'][s]: float(pi[wage == s].sum()) for s in range(3)}
    order = np.argsort(-pi)
    cat = catalogue(); w = cat.roles['W']; b = cat.roles['B']
    def desc(code):
        bb, x, y = ch.decode(int(code))
        return '%s | %s | %s' % (S.show_dt(b['dt'][T['repb'][bb]]), S.show_dt(w['dt'][T['rep1'][x]]), S.show_dt(w['dt'][T['rep2'][y]]))
    out['support'] = [dict(pi=float(pi[k]), state=desc(codes[k]), play=UN.joint_name(int(j[k])), summary=UN.SUMM[summ[k]]) for k in order[:25]]
    trans = []
    for k in order[:8]:
        ex, tot, tch = fexits(ch, int(codes[k]))
        trans.append(dict(state=desc(codes[k]), pi=float(pi[k]), summary=UN.SUMM[summ[k]], exit_by_kind=tot, outcome_changing=tch,
                          top=[dict(p=e['prob'], kind=e['kind'], slot=['B', 'W1', 'W2'][e['slot']], du=e['du'], to=e['summ_to']) for e in ex[:6]]))
    out['transitions'] = trans
    # fair basin exits
    fi = np.nonzero(summ == 0)[0]
    pf = float(pi[fi].sum())
    ek = {}
    for k in fi[np.argsort(-pi[fi])][:150]:
        ex, tot, tch = fexits(ch, int(codes[k]), top=10 ** 7)
        for kk, v in tch.items():
            ek[kk] = ek.get(kk, 0.0) + pi[k] * v
    out['fair_pi'] = pf
    out['fair_exit_by_slot_kind'] = {kk: v / pf for kk, v in sorted(ek.items(), key=lambda kv: -kv[1])} if pf > 0 else {}
    # cut diagnostic: flows leaving the explored set under the solved pi, by source and destination summary
    r = ch.rows(codes, codes, ch.lpi, 1e-300, mode=1)
    src, dst, fl, chg = r[0], r[1], r[2], r[7]
    f_ = np.exp(fl)
    tot_out = float(np.exp(ch.lpi) @ r[3])
    ssrc = summ[src]
    sdst = np.array([UN.summary(ch.J(*ch.decode(int(d))), int(ch.tagc[ch.decode(int(d))[1]]), int(ch.tagc[ch.decode(int(d))[2]])) for d in dst]) if len(dst) else np.zeros(0, int)
    cut = float(f_.sum())
    out['cut_diagnostic'] = dict(cut_flow=cut, cut_rel_total=cut / tot_out if tot_out > 0 else None, cut_outcome_changing=float(f_[chg].sum()),
                                 dst_summary={UN.SUMM[k]: float(f_[sdst == k].sum() / cut) for k in range(7)} if cut > 0 else {},
                                 src_summary={UN.SUMM[k]: float(f_[ssrc == k].sum() / cut) for k in range(7)} if cut > 0 else {},
                                 out_of_fair=float(f_[(ssrc == 0) & (sdst != 0)].sum()), distinct_destinations=int(len(np.unique(dst))))
    if pf > 0:
        outA = float(f_[(ssrc == 0) & (sdst != 0)].sum())
        esc = sum(v for v in ek.values())
        out['cut_diagnostic']['fair_cut_escape_per_unit'] = outA / pf
    out['time_s'] = time.time() - t0
    json.dump(out, open(os.path.join(RUNS, 'sog-realizable-chain.json'), 'w'), indent=1, default=float)
    print(json.dumps(out['summary']), json.dumps(out['wage_offered']), 'fair exits', json.dumps(out['fair_exit_by_slot_kind'])[:500],
          'cut', json.dumps(out['cut_diagnostic'])[:400], '%.0fs' % (time.time() - t0), flush=True)


# ----------------------------------------------------------------------------------------------------------------
# migration-off residence assays (forced D* vs D*2), the audit of realized encounters at K = 10^6, the fuel sweep
# ----------------------------------------------------------------------------------------------------------------
def _assay_job(args):
    name, seed, T_path, horizon = args
    if 'T' not in _JOB:
        _JOB['T'] = pickle.load(open(T_path, 'rb'))
    T = _JOB['T']
    cfg = cell_config(name, T)
    full = run_one(T, cfg, seed)
    fair = fair_flags(full['stats'])
    nck = fair.shape[0]
    win = {}
    for i in range(full['I']):
        run = 0
        for c in range(nck):
            run = run + 1 if fair[c, i] else 0
            if run >= FAIR_WINDOW:
                win[i] = c; break
    out = []
    by_c = {}
    for i, c in win.items():
        by_c.setdefault(c, []).append(i)
    ids = list(full['ids'])
    for c, isl in sorted(by_c.items()):
        g = int(c * CHECK_EVERY)
        if g == 0:
            snap = full['init']
        else:
            snap = run_one(T, cfg, seed, checks_upto=g)['counts']
        for i in isl:
            init = snap[i:i + 1].copy()
            cfg1 = dict(cfg); cfg1['I'] = 1
            r1 = run_one(T, cfg1, seed + 7919 * (i + 1), init_override=init, ids_override=ids, m_override=0.0,
                         checks_upto=horizon)
            f1 = fair_flags(r1['stats'])[:, 0]
            nf = np.nonzero(~f1)[0]
            res = int(nf[0] * CHECK_EVERY) if len(nf) else None
            # holder at the window end
            bmod = ids[int(np.argmax(init[0, 0]))]
            out.append(dict(island=i, window_end_gen=g, residence=res, censored=res is None, horizon=horizon,
                            boss_holder=int(bmod) if bmod >= 0 else -1, forced_share=float(init[0, 0][ids.index(cfg['forced'])] / cfg['N']) if cfg['forced'] in ids else 0.0))
    return dict(seed=seed, established_islands=len(win), assays=out, persistence=float(fair[-1].mean()))


def assays(args):
    T = tables()
    tpath = os.path.join(OUT, 'tables.pkl')
    _JOB['T'] = T
    out = {}
    from multiprocessing import get_context
    for name in ('forcedD*', 'forcedD*2'):
        seeds = [777000 + k for k in range(args.runs or 40)]
        t0 = time.time()
        with get_context('fork').Pool(args.procs) as pool:
            res = pool.map(_assay_job, [(name, s, tpath, 2000) for s in seeds], chunksize=1)
        a = [x for r in res for x in r['assays']]
        resid = [x['residence'] for x in a if not x['censored']]
        cens = sum(1 for x in a if x['censored'])
        out[name] = dict(runs=len(res), established_islands=len(a), censored_at_2000=cens,
                         residence_median_uncensored=float(np.median(resid)) if resid else None,
                         residence_mean_uncensored=float(np.mean(resid)) if resid else None,
                         residence_lower_bound_mean=float(np.mean([x['residence'] if not x['censored'] else 2000 for x in a])) if a else None,
                         per_run=[dict(seed=r['seed'], established=r['established_islands'], persistence_migration_on=r['persistence']) for r in res],
                         time_s=time.time() - t0)
        print(name, json.dumps({k: v for k, v in out[name].items() if k != 'per_run'}), flush=True)
    json.dump(out, open(os.path.join(RUNS, 'sog-realizable-assays.json'), 'w'), indent=1)


def _audit_job(args):
    label, enc, want = args
    play, steps, raw = S.play3(enc[0], enc[1], enc[2], K_MAIN)
    return dict(label=label, match=(int(play[0]), play[1], play[2]) == tuple(want), steps=[int(s) for s in steps],
                play=[int(play[0]), play[1], play[2]], want=list(want))


def audit(args):
    """Realized encounters of lottery runs, weighted by their frequency on the islands, played whole at K = 10^6
    against the ideal table: the fraction of encounter mass whose executable play differs."""
    T = tables()
    _JOB['T'] = T
    out = {}
    rng = np.random.default_rng(4)
    from multiprocessing import get_context
    for name in ('L', 'Lmil'):
        cfg = cell_config(name, T)
        rows = []
        jobs = []
        for seed in [500000 + k for k in range(4)]:
            for g in (0, 50, 200, 2000):
                r = run_one(T, cfg, seed, checks_upto=g) if g > 0 else None
                cnt = r['counts'] if r is not None else seed_run(T, cfg, seed)[1]
                ids = list(r['ids']) if r is not None else seed_run(T, cfg, seed)[0]
                # sample encounters by frequency
                for k in range(60):
                    i = int(rng.integers(cfg['I']))
                    bs = cnt[i, 0]; xs = cnt[i, 1]; ys = cnt[i, 2]
                    b = int(rng.choice(len(bs), p=bs / bs.sum())); x = int(rng.choice(len(xs), p=xs / xs.sum()))
                    y = int(rng.choice(len(ys), p=ys / ys.sum()))
                    g_b = ids[b]
                    jc = S.joint_code(T, g_b, x, y)
                    want = (jc // 4, 'CD'[(jc // 2) % 2], 'CD'[jc % 2])
                    enc = (compiled('B', int(T['repb'][g_b]), 0) if g_b < T['nb_cat'] else named_programs()[1]['D*_2'],
                           compiled('W', int(T['rep1'][x]), 1), compiled('W', int(T['rep2'][y]), 2))
                    jobs.append(('%s %d %d' % (name, seed, g), enc, want))
                    rows.append((seed, g))
        with get_context('fork').Pool(args.procs) as pool:
            res = pool.map(_audit_job, jobs, chunksize=4)
        by_g = {}
        for (seed, g), r in zip(rows, res):
            by_g.setdefault(g, []).append(r['match'])
        out[name] = {str(g): dict(sampled=len(v), mismatch_frac=float(1 - np.mean(v))) for g, v in sorted(by_g.items())}
        out[name + '_examples'] = [r for r in res if not r['match']][:8]
        print(name, json.dumps(out[name]), flush=True)
    json.dump(out, open(os.path.join(RUNS, 'sog-realizable-audit.json'), 'w'), indent=1)


def _cost_job(args):
    label, enc, K = args
    V = K // 4
    play, steps, raw = S.play3(enc[0], enc[1], enc[2], K)
    chk = []
    for (e, j, A) in _checks_of_K(enc, V, K):
        tv, ts = S.term_check(e, j, A, V, K)
        chk.append(dict(j=j, A=S.ANAME[A], probe=e is not enc, value=tv, steps=int(ts)))
    return dict(label=label, K=K, play=[int(play[0]), play[1], play[2]], raw=[str(v) for v in raw], run_steps=[int(s) for s in steps], checks=chk)


def costs(args):
    """The fuel sweep on the named states and on the most expensive catalogue encounters found in the gap sample;
    production costs."""
    out = {}
    jobs = []
    for K in (300000, 1000000, 3000000):
        Wn, Bn, _ = named_programs(K=K)
        for (bn, x, y), _ in HAND:
            if bn == 'C1': continue
            jobs.append(('%s | %s | %s' % (bn, x, y), (Bn[bn], Wn[x][0], Wn[y][1]), K))
    from multiprocessing import get_context
    with get_context('fork').Pool(args.procs) as pool:
        res = pool.map(_cost_job, jobs, chunksize=2)
    table = {}
    for r in res:
        table.setdefault(r['label'], {})[str(r['K'])] = dict(play=r['play'], run_steps=r['run_steps'],
                                                            max_check=max(c['steps'] for c in r['checks'] if c['value'] != 'TO') if any(c['value'] != 'TO' for c in r['checks']) else None,
                                                            timeouts=[(c['j'], c['A'], c['probe']) for c in r['checks'] if c['value'] == 'TO'])
    out['named'] = table
    # production costs
    cat = catalogue()
    t0 = time.time()
    for role in ('W', 'B'):
        r = cat.roles[role]
        sizes = [S.C.script_nodes(e[1]) for l in r['lists'] for e in S.C.uncons(l)]
        out['lists_' + role] = dict(trees=len(r['dt']), entries_mean=float(np.mean([len(S.C.uncons(l)) for l in r['lists']])),
                                    entries_max=int(max(len(S.C.uncons(l)) for l in r['lists'])),
                                    script_nodes_mean=float(np.mean(sizes)), script_nodes_max=int(max(sizes)))
    pp = S.PathProducer()
    w = cat.roles['W']
    t0 = time.time()
    for tk in range(len(w['dt'])):
        x = w['spellings'][w['members'][tk][0]]
        prog0 = S.compile_program(x, 'W', 1, V_MAIN, K_MAIN, 0)
        S.produce_lists(w['dt'][tk], 'W', pp, prog0, 1, V_MAIN, K_MAIN)
    out['host_production_time_all_worker_trees_s'] = time.time() - t0
    json.dump(out, open(os.path.join(RUNS, 'sog-realizable-costs.json'), 'w'), indent=1)
    for lab, v in table.items():
        print(lab, {k: (vv['play'], vv['max_check'], len(vv['timeouts'])) for k, vv in v.items()}, flush=True)


def modal_coalition(args):
    """The founding-coalition mass of the modal social organization game (the union run's CC language, boss n = 6,
    workers n = 10, length prior), computed exactly as in §1.4: fair triples with no strict boss invader among the
    language's classes (workers cannot exceed 1/2 there either)."""
    C = SL.class_data('CC')
    Jc, tg, mB, mW = C['Jc'], C['tagc'], C['massB'], C['massW']
    KB, KW = C['KcB'], C['KcW']
    tot = 0.0; n_pairs = 0; const_b = C['constB']
    tot_const = 0.0
    fair_boss_payoff = 1.0
    for x in range(KW):
        for y in range(KW):
            J = Jc[:, x, y].astype(np.int64)
            u = PAY[J, tg[x], tg[y], 0]
            fair = np.array([UN.summary(int(j), int(tg[x]), int(tg[y])) == 0 for j in J])
            if not fair.any(): continue
            if u.max() > fair_boss_payoff + 1e-12: continue
            n_pairs += 1
            tot += mB[fair].sum() * mW[x] * mW[y]
            tot_const += mB[fair & const_b].sum() * mW[x] * mW[y]
    out = dict(language='union run CC (boss n = 6, workers n = 10, quorum arm; RESULTS "The union game")', mass=float(tot),
               constant_boss_mass=float(tot_const), compatible_pairs=n_pairs, KcB=int(KB), KcW=int(KW),
               note='the concessions run (P01, n = 11) adds probe bosses of total mass 0.064 and D* at 9.7e-9; not rebuilt here')
    json.dump(out, open(os.path.join(RUNS, 'sog-realizable-modal.json'), 'w'), indent=1)
    print(json.dumps(out), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runs', type=int, default=None)
    ap.add_argument('--N', type=float, default=1e4)
    ap.add_argument('--theta', type=float, default=1e-9)
    ap.add_argument('--Ks', type=int, nargs='*', default=[300000, 1000000, 3000000])
    ap.add_argument('cmd')
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--sample', type=int, default=600)
    ap.add_argument('--cell', default=None)
    args = ap.parse_args()
    assert args.procs <= 3
    if args.cmd == 'tables':
        T = tables(force=True)
        print('classes', len(T['rep1']), len(T['rep2']), len(T['repb']))
    elif args.cmd == 'validate':
        validate(args)
    elif args.cmd == 'gap':
        gap(args)
    elif args.cmd == 'static':
        static(args)
    elif args.cmd == 'lottery':
        lottery(args)
    elif args.cmd == 'chain':
        chain(args)
    elif args.cmd == 'assays':
        assays(args)
    elif args.cmd == 'audit':
        audit(args)
    elif args.cmd == 'costs':
        costs(args)
    elif args.cmd == 'modal':
        modal_coalition(args)
    else:
        raise SystemExit('unknown command')


if __name__ == '__main__':
    main()
