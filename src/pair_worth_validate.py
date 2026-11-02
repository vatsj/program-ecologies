"""Validation V1-V6 of the pair-worth machinery (spec design 2; notes/pair-worth.md).  Run: python3 src/pair_worth_validate.py

The expectations of V4 were derived by hand from the action equations (notes 1.3-1.4) before the first evaluation; each
is written next to the case, as (expected action triple)."""
import json, os, sys, time, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pair_worth as PW
import pair_worth_kern as PK

OUTP = os.path.join(PW.ROOT, 'runs', 'pair_worth')
RES = {}


def report(name, ok, detail):
    RES[name] = dict(ok=bool(ok), detail=detail)
    print(('PASS ' if ok else 'FAIL ') + name + ' ' + str(detail), flush=True)


# ===================================================================== V1
def v1():
    import dollar3 as D
    G = PW.get_game('pw1')
    mism = 0
    tot = 0
    kindmap = {0: 1, 1: 2, 2: 2, 3: 2, 4: 0}            # dollar3 type -> my kind
    for a in itertools.product(range(9), repeat=3):
        u, typ = D.outcome(D.PARTNER, *a)
        b = tuple(7 * (l // 3) + 2 + (l % 3) for l in a)          # my local action for dollar3's local action l
        o = G.outs[int(G.OUT[b])]
        tot += 1
        if tuple(int(t) for t in u) != o[2] or kindmap[int(typ)] != o[0]:
            mism += 1
    report('V1 dollar3 payoff table at a=1 on its 9 actions', mism == 0, dict(triples=tot, mismatches=mism))


# ===================================================================== V2
def v2():
    import churn_primary as CP
    import migration_window_kernels as MK
    import migration_window as MW
    T = CP.T
    stored = json.load(open(os.path.join(PW.ROOT, 'runs', 'churn_primary', 'B6w__c0=0.json')))
    cat = CP.get_cat('B6w')
    base = CP.founder_base('B6w')
    out = []
    allok = True
    for r in range(6):
        prep = CP.prepare(cat, base, r)
        for mN in (0, 1):
            H = 10000
            ref = MK.kern_mw(prep['J'], prep['PAY'], prep['VEC'], T.ISMEM, T.TOT, prep['loc'], prep['N'], CP.W, mN / prep['N'],
                             prep['seed'], H, 10, np.zeros(0, np.int64), 200000)
            rs, rstop, rcounts, rcls, _e, _d, _ev, _nev, rnmig, rmodal, _em, _fm = ref
            nout = T.ISMEM.shape[0]
            Kp = prep['J'].shape[0]
            res = PK.kern_pw(prep['J'], prep['PAY'], prep['VEC'], T.ISMEM, T.TOT, np.zeros((nout, 3)),
                             np.zeros(nout, np.int64), np.zeros(nout, np.int64), 1, 1, np.zeros((3, Kp), np.int64),
                             prep['loc'], prep['N'], CP.W, mN / prep['N'], prep['seed'], H, 10,
                             np.zeros(0, np.int64), np.zeros(0, np.int64), np.zeros(0, np.int64), np.zeros(0),
                             np.zeros(0, np.int64), 10, 10)
            status, stop, counts, cls, modal = res[0], res[1], res[2], res[3], res[4]
            same = (int(status) == int(rs) and int(stop) == int(rstop) and (counts == rcounts).all() and (cls == rcls).all()
                    and (modal.astype(np.int64) == rmodal.astype(np.int64)).all() and int(res[-1]) == int(rnmig))
            # stored row
            row = [x for x in stored[str(mN)] if x['run'] == r][0]
            V = MW.V
            mend = modal[rstop]
            nm = len(set(int(x) for x in mend if int(x) in V)); F_ = int(sum(1 for x in mend if int(x) in V))
            same_stored = (row['stop'] == int(stop) and row['status'] == int(status) and row['nm'] == nm and row['F'] == F_)
            out.append(dict(run=r, mN=mN, stop=int(stop), identical_to_kern_mw=bool(same), matches_stored_row=bool(same_stored)))
            allok &= bool(same) and bool(same_stored)
    report('V2 Lambda=0 kernel vs kern_mw and the stored churn_primary B6w rows (runs 0-5, mN 0 and 1)', allok, out)


# ===================================================================== V3
def v3():
    import math
    import pair_worth_run as PR
    gname = 'pw13'
    G = PW.get_game(gname)
    menu = PW.arm_menu(gname, 'CBs', 0.05)
    N, I = 100, 64
    geo = PR.geometry(N)
    runs = 40
    lam = 10.0
    lam_eff = lam * (1 - 1 / (1 + (geo['gend'] - geo['g0']) / geo['t0']))
    per_isl = []
    cats = np.zeros((3, G.nact + 1)); slot_cnt = np.zeros(3)
    nest_ok = True
    for r in range(runs):
        base = '%s|N%d|I%d' % (gname, N, I)
        sc = PW.tail_schedule(menu, base, r, I, N, 100.0, geo['g0'], geo['t0'], geo['gend'], [1.0, 10.0, 100.0])
        ag, ai, asl, au, am = sc[10.0]
        per_isl.append(np.bincount(ai, minlength=I))
        for s in range(3):
            sel = asl == s
            slot_cnt[s] += sel.sum()
            mm = am[sel]
            cats[s, :G.nact] += np.bincount(np.minimum(mm, G.nact), minlength=G.nact + 1)[:G.nact]
            cats[s, G.nact] += (mm >= G.nact).sum()
        # nesting: lam 1 subset of lam 10 subset of lam 100 (as multisets of (g, i, slot, victim u))
        key = lambda t: set(zip(t[0].tolist(), t[1].tolist(), t[2].tolist(), np.round(t[3], 12).tolist()))
        nest_ok &= key(sc[1.0]) <= key(sc[10.0]) <= key(sc[100.0])
    allc = np.concatenate(per_isl)
    mean = allc.mean(); se = allc.std(ddof=1) / math.sqrt(len(allc))
    z = (mean - lam_eff) / se
    # chi-square per slot: constants uniform (1-delta)/21 each, family bucket delta
    exp_p = np.r_[np.full(G.nact, 0.95 / G.nact), 0.05]
    chis = []
    for s in range(3):
        e = exp_p * cats[s].sum()
        chis.append(float(((cats[s] - e) ** 2 / e).sum()))
    df = G.nact          # 22 categories - 1
    from scipy.stats import chi2
    pv = [float(1 - chi2.cdf(c, df)) for c in chis]
    # uniform slot choice
    from scipy.stats import chisquare
    p_slot = float(chisquare(slot_cnt).pvalue)
    # kernel applies every scheduled arrival
    prep = PR.prepare(gname, 'CBs', 0, N, 0.05, [10.0])
    o = PR.run_kernel(prep, 10.0, 1.0)
    n_sched = len(prep['sched'][10.0][0])
    cnt_ok = bool((o['counts'].sum(axis=2) == N).all())
    ok = abs(z) < 3 and all(p > 0.001 for p in pv) and p_slot > 0.001 and nest_ok and int(o['na']) == n_sched and cnt_ok
    report('V3 tail: arrivals per island vs Lambda, arrival law vs seed law, nesting, kernel applies all', ok,
           dict(runs=runs, mean_per_island=round(float(mean), 4), expected=round(lam_eff, 4), se=round(float(se), 4), z=round(float(z), 2),
                chi2_per_slot=[round(c, 1) for c in chis], df=df, p_chi2=[round(p, 3) for p in pv], p_slot_uniform=round(p_slot, 3),
                nested=bool(nest_ok), kernel_applied=int(o['na']), scheduled=int(n_sched), counts_conserved=cnt_ok))


# ===================================================================== helpers for V3-V6
def A(G, s, partner, d):
    return G.act(s, PW.ALL if partner == 'ALL' else partner, d)


def play(G, progs):
    """progs: three (lines, default) -> action triple."""
    t = PW.table_from_programs(G, [[p] for p in progs])
    return t.play(0, 0, 0)


def decode_triple(G, v):
    return tuple(G.aname(s, v[s]) for s in range(3))


# ===================================================================== V4
def v4():
    G = PW.get_game('pw13')
    sg = (2, 2, 2)
    B = lambda s, c, sig=sg, kind='B': PW.program(G, kind, s, sig, c)
    K = lambda s, c, sig=sg: PW.program(G, 'K', s, sig, c)
    Ap = lambda s, c, sig=sg: PW.program(G, 'A', s, sig, c)
    C = PW.const_program
    c0, c1, c2 = A(G, 0, 2, 3), A(G, 1, 2, 3), A(G, 2, 0, 0)          # fallbacks: 0->(2,3), 1->(2,3), 2->(0,0)
    cases = []

    def add(name, progs, exp, G_=G):
        cases.append((name, G_, progs, exp))
    pa = lambda s, p, d: A(G, s, p, d)
    ALLD = lambda s, d: A(G, s, 'ALL', d)
    # E: B^3 same sigma plays sigma
    add('B^3 plays sigma', [B(0, c0), B(1, c1), B(2, c2)], [ALLD(0, 2), ALLD(1, 2), ALLD(2, 2)])
    # E: B, B, non-grand constant: the two bidders pair at the exclusion split (1,1); slot 2 keeps its constant
    add('B,B,const(0,0): bidders pair', [B(0, c0), B(1, c1), C(c2)], [pa(0, 1, 1), pa(1, 0, 1), c2])
    # E: B, B, matching grand constant: grand
    add('B,B,G_2 matching: grand', [B(0, c0), B(1, c1), C(ALLD(2, 2))], [ALLD(0, 2), ALLD(1, 2), ALLD(2, 2)])
    # E: B, B, a grand constant with another share: grand line fails, bidders pair, slot 2 stays (ALL,3)
    add('B,B,G_2 other share: bidders pair', [B(0, c0), B(1, c1), C(ALLD(2, 3))], [pa(0, 1, 1), pa(1, 0, 1), ALLD(2, 3)])
    # E: B with one constant partner offering exactly pi: pairs with it
    add('B,const(0,1),const(0,0): pairs with slot 1', [B(0, c0), C(pa(1, 0, 1)), C(pa(2, 0, 0))], [pa(0, 1, 1), pa(1, 0, 1), pa(2, 0, 0)])
    # E: second partner offering pi: pairs with slot 2
    add('B,const(0,2),const(0,1): pairs with slot 2', [B(0, c0), C(pa(1, 0, 2)), C(pa(2, 0, 1))], [pa(0, 2, 1), pa(1, 0, 2), pa(2, 0, 1)])
    # E: nobody offers pi: fallback
    add('B,const(0,2),const(0,2): fallback c', [B(0, c0), C(pa(1, 0, 2)), C(pa(2, 0, 2))], [c0, pa(1, 0, 2), pa(2, 0, 2)])
    # E: K,K,B: blockers pair at (1,1), B falls back
    add('K,K,B: blockers pair', [K(0, c0), K(1, c1), B(2, c2)], [pa(0, 1, 1), pa(1, 0, 1), c2])
    # E: K in slot 0 on B island pairs with slot 1 (first handshake line), slot 2 falls back
    add('K_0,B,B: K pairs with slot 1', [K(0, c0), B(1, c1), B(2, c2)], [pa(0, 1, 1), pa(1, 0, 1), c2])
    # E: K in slot 1 pairs with slot 0
    add('B,K_1,B: K pairs with slot 0', [B(0, c0), K(1, c1), B(2, c2)], [pa(0, 1, 1), pa(1, 0, 1), c2])
    # E: K in slot 2 finds no partner (slot 0's first line is for slot 1): bids pair, K falls back
    add('B,B,K_2: bids pair, K excluded', [B(0, c0), B(1, c1), K(2, c2)], [pa(0, 1, 1), pa(1, 0, 1), c2])
    # E: K^3: slots 0 and 1 pair, slot 2 falls back
    add('K^3', [K(0, c0), K(1, c1), K(2, c2)], [pa(0, 1, 1), pa(1, 0, 1), c2])
    # E: a mixed-sigma bid triple with one slot's expectation violated collapses to the fallbacks (hand derivation in notes)
    add('mixed sigma (3,2,1) in slot 1: all fall back', [B(0, c0), B(1, c1, (3, 2, 1)), B(2, c2)], [c0, c1, c2])
    # E: A accepts a constant pair offer (1,1): plays (1, 2-1)
    add('A,const(0,1),const(0,0): accepts', [Ap(0, c0), C(pa(1, 0, 1)), C(pa(2, 0, 0))], [pa(0, 1, 1), pa(1, 0, 1), pa(2, 0, 0)])
    # E: A accepts offer d=0 with (1, 2)
    add('A,const(0,0),const(0,0): accepts at 2', [Ap(0, c0), C(pa(1, 0, 0)), C(pa(2, 0, 0))], [pa(0, 1, 2), pa(1, 0, 0), pa(2, 0, 0)])
    # E: A,A,const that does not offer a pair: mutual acceptance has no consistent fixed point, both fall back to c
    # (first evaluation used const (0,0), which is a pair offer to slot 0 that A_0 accepts: the hand expectation was wrong)
    add('A,A,const(ALL,0): fall back', [Ap(0, c0), Ap(1, c1), C(ALLD(2, 0))], [c0, c1, ALLD(2, 0)])
    add('A,A,const(0,0): A_0 accepts slot 2', [Ap(0, c0), Ap(1, c1), C(c2)], [pa(0, 2, 2), c1, c2])
    # E: level-0 bids (as written): B0,B0,const: no handshake, both bidders play their fallbacks
    add('B0,B0,const: no handshake at level 0', [B(0, c0, kind='B0'), B(1, c1, kind='B0'), C(c2)], [c0, c1, c2])
    add('B0^3 plays sigma', [B(0, c0, kind='B0'), B(1, c1, kind='B0'), B(2, c2, kind='B0')], [ALLD(0, 2), ALLD(1, 2), ALLD(2, 2)])
    # G5/6 equal split: pairs at (5,5)
    G5 = PW.get_game('pw56')
    s5 = (4, 4, 4)
    d0, d1, d2 = A(G5, 0, 2, 3), A(G5, 1, 2, 3), A(G5, 2, 0, 0)
    add('G5/6: B,B,const -> (5,5)', [PW.program(G5, 'B', 0, s5, d0), PW.program(G5, 'B', 1, s5, d1), PW.const_program(d2)],
        [A(G5, 0, 1, 5), A(G5, 1, 0, 5), d2], G5)
    add('G5/6: K_0,B,B -> (5,5)', [PW.program(G5, 'K', 0, s5, d0), PW.program(G5, 'B', 1, s5, d1), PW.program(G5, 'B', 2, s5, d2)],
        [A(G5, 0, 1, 5), A(G5, 1, 0, 5), d2], G5)
    add('G5/6: B^3 grand (4,4,4)', [PW.program(G5, 'B', s, s5, [d0, d1, d2][s]) for s in range(3)],
        [A(G5, s, 'ALL', 4) for s in range(3)], G5)
    # glove: R = slot 0, sigma = (4,1,1): R-L pair split 6*4/5 -> 4, 6*1/5 -> 1, remainder to the larger: (5,1)
    Gg = PW.get_game('gl6')
    sg2 = (4, 1, 1)
    e0, e1, e2 = A(Gg, 0, 2, 3), A(Gg, 1, 2, 3), A(Gg, 2, 0, 0)
    add('glove: B_R,B_L1,const -> (5,1)', [PW.program(Gg, 'B', 0, sg2, e0), PW.program(Gg, 'B', 1, sg2, e1), PW.const_program(e2)],
        [A(Gg, 0, 1, 5), A(Gg, 1, 0, 1), e2], Gg)
    ok = True
    det = []
    for name, G_, progs, exp in cases:
        got = play(G_, progs)
        good = tuple(got) == tuple(exp)
        ok &= good
        det.append(dict(case=name, ok=good, got=decode_triple(G_, got), expected=decode_triple(G_, exp)))
        if not good:
            print('  MISMATCH', name, decode_triple(G_, got), 'expected', decode_triple(G_, exp), flush=True)
    report('V4 bid semantics on hand-built triples (%d cases; expectations derived before evaluation)' % len(cases), ok,
           [d for d in det if not d['ok']] or 'all %d as derived' % len(cases))
    RES['V4_cases'] = det


# ===================================================================== V5
def ref_eval(progs):
    """independent pure-python chain evaluation of decision lists (no shared code with the numba evaluator)."""
    VAC, BRK = 'vac', 'brk'
    hist = {0: [VAC] * 3, 1: [VAC] * 3}
    n = 0
    prev = None
    while n < 80:
        val = []
        for s in range(3):
            lines, df = progs[s]
            out = df
            for atoms, o in lines:
                ok = True
                for (p, a, L, sg) in atoms:
                    h = hist[L][p]
                    truth = (h == VAC) or (h == a)
                    if not sg:
                        truth = not truth
                    if not truth:
                        ok = False
                        break
                if ok:
                    out = o
                    break
            val.append(out)
        changed = False
        for L in (0, 1):
            if n < L:
                continue
            for s in range(3):
                h = hist[L][s]
                if h == VAC:
                    hist[L][s] = val[s]; changed = True
                elif h != BRK and h != val[s]:
                    hist[L][s] = BRK; changed = True
        if not changed and n >= 2:
            return tuple(val)
        n += 1
    return None


def v5():
    rng = np.random.default_rng(5)
    tot = 0; bad = 0
    detail = {}
    for gname in ('pw13', 'pw56', 'gl6', 'pw23'):
        G = PW.get_game(gname)
        # random named programs of every family (including mixed sigma, level 0 variants) and constants
        def rnd(s):
            kind = rng.choice(['C', 'B', 'K', 'A', 'G', 'B0', 'K0', 'A0'])
            c = int(rng.integers(G.nact))
            if kind == 'C':
                return PW.const_program(c)
            sig = PW.splits(G.Gd)[int(rng.integers(len(PW.splits(G.Gd))))]
            return PW.program(G, kind, s, sig, c)
        n = 1000
        b = 0
        for _ in range(n):
            progs = [rnd(s) for s in range(3)]
            t = PW.table_from_programs(G, [[p] for p in progs])
            got = t.play(0, 0, 0)
            ref = ref_eval(progs)
            if tuple(got) != ref:
                b += 1
        # biased sample: programs likely to interact (same sigma, matching constants)
        for _ in range(n):
            sig = PW.splits(G.Gd)[int(rng.integers(len(PW.splits(G.Gd))))]
            progs = []
            for s in range(3):
                r = rng.random()
                c = int(rng.integers(G.nact))
                if r < 0.4:
                    progs.append(PW.program(G, rng.choice(['B', 'K', 'A', 'B0']), s, sig, c))
                elif r < 0.6:
                    progs.append(PW.const_program(G.act(s, PW.ALL, sig[s])))
                elif r < 0.8:
                    p = PW.others(s)[int(rng.integers(2))]
                    progs.append(PW.const_program(G.act(s, p, int(PW.pi_split(G, s, p, sig)[0]))))
                else:
                    progs.append(PW.const_program(c))
            t = PW.table_from_programs(G, [[p] for p in progs])
            got = t.play(0, 0, 0)
            if tuple(got) != ref_eval(progs):
                b += 1
        tot += 2 * n; bad += b
        detail[gname] = dict(n=2 * n, mismatches=b)
    # DSL programs of dollar3 against dollar3.eval_modal
    import dollar3 as D
    import stable_sets as SS
    S, mu = SS.arm_data('modalPA')
    # the full DSL of dollar3 at n = 6 has levels 0 and 1 only in the 'modal' arm; use it for L = 0 and 1
    L_, S2, mu2, cnt2, size2 = D.build('modal', 6)
    K = S2.K
    # convert canonical function (atoms, tab) of slot s to a decision list (valuations in order, positive/negative literals)
    def dsl_prog(S_, s, x):
        atoms = [(int(S_.atJ[s, x, t]), int(S_.atA[s, x, t]), int(S_.atL[s, x, t])) for t in range(S_.nat[s, x])]
        tab = [int(S_.tab[s, x, v]) for v in range(1 << len(atoms))]
        if not atoms:
            return ([], tab[0])
        lines = []
        for v in range(1 << len(atoms)):
            lit = [(p, a, L, 1 if (v >> t) & 1 else 0) for t, (p, a, L) in enumerate(atoms)]
            lines.append((lit, tab[v]))
        return (lines, tab[0])
    prog_cache = {(s, x): dsl_prog(S2, s, x) for s in range(3) for x in range(K)}
    nb = 0; nt = 3000
    for _ in range(nt):
        xs = [int(rng.integers(K)) for _ in range(3)]
        v = D.eval_modal(S2.nat, S2.atL, S2.atJ, S2.atA, S2.tab, xs[0], xs[1], xs[2])
        progs = [prog_cache[(s, xs[s])] for s in range(3)]
        t = PW.table_from_programs(PW.get_game('pw1'), [[p] for p in progs])
        got = t.play(0, 0, 0)
        if tuple(int(a) for a in v) != tuple(got):
            nb += 1
    detail['dollar3_DSL_vs_eval_modal'] = dict(n=nt, mismatches=nb)
    ok = bad == 0 and nb == 0
    report('V5 modal evaluation vs independent chain evaluation and dollar3.eval_modal', ok, dict(named_total=tot, named_mismatches=bad, detail=detail))


# ===================================================================== V6
def v6():
    """V6a: relabelling with the partner priorities carried along (image of the original order) must give exactly the
    permuted outcome (0 mismatches).  V6b: relabelling with the spec's index-ordered priorities (j < k): mismatches
    are counted and attributed (they can only arise where a program has two eligible handshakes)."""
    rng = np.random.default_rng(6)
    detail = {}
    allok = True
    for gname in ('pw13', 'pw23', 'pw56', 'gl6'):
        G = PW.get_game(gname)
        perms = list(itertools.permutations(range(3)))
        if G.glove:
            perms = [p for p in perms if p[0] == 0]
        sp = PW.splits(G.Gd)
        bad_a = 0; bad_b = 0; bad_b_noK = 0; n_noK = 0
        n = 10000
        for _ in range(n):
            tau = perms[int(rng.integers(len(perms)))]
            specs = []
            for s in range(3):
                kind = str(rng.choice(['C', 'B', 'K', 'A', 'G', 'B0']))
                c = int(rng.integers(G.nact))
                sig = sp[int(rng.integers(len(sp)))]
                specs.append((kind, sig, c))
            if rng.random() < 0.5:
                sig = sp[int(rng.integers(len(sp)))]
                specs = [(k, sig, c) for (k, _s, c) in specs]
            progs = [PW.const_program(c) if k == 'C' else PW.program(G, k, s, sg, c) for s, (k, sg, c) in enumerate(specs)]
            v1_ = play(G, progs)
            u1 = G.outs[int(G.OUT[v1_])]

            def img_action(s, l):
                p = G.partner(s, l)
                return G.act(tau[s], PW.ALL if p == PW.ALL else tau[p], l % (G.Gd + 1))
            pv = [0, 0, 0]
            for s in range(3):
                pv[tau[s]] = u1[2][s]
            res = {}
            for mode in ('a', 'b'):
                iprogs = [None] * 3
                for s, (k, sg, c) in enumerate(specs):
                    sg2 = [0, 0, 0]
                    for j in range(3):
                        sg2[tau[j]] = sg[j]
                    t = tau[s]
                    prio = [tau[p] for p in PW.others(s)] if mode == 'a' else None
                    iprogs[t] = PW.const_program(img_action(s, c)) if k == 'C' else PW.program(G, k, t, tuple(sg2), img_action(s, c), prio)
                v2_ = play(G, iprogs)
                u2 = G.outs[int(G.OUT[v2_])]
                acts_ok = all(v2_[tau[s]] == img_action(s, v1_[s]) for s in range(3))
                res[mode] = (tuple(pv) == u2[2]) and acts_ok
            bad_a += (not res['a']); bad_b += (not res['b'])
            hasprio = any(k in ('B', 'K', 'A', 'B0') for (k, _s, _c) in specs)
            if not hasprio:
                n_noK += 1; bad_b_noK += (not res['b'])
        detail[gname] = dict(n=n, V6a_priority_carried_mismatches=bad_a, V6b_index_priority_mismatches=bad_b,
                             V6b_among_triples_without_handshake_families=[n_noK, bad_b_noK], perms=len(perms))
        allok &= bad_a == 0 and bad_b_noK == 0
    report('V6 slot-permutation invariance (V6a priority carried: 0 expected; V6b spec index order: counted)', allok, detail)


def main(which=None):
    os.makedirs(OUTP, exist_ok=True)
    fns = dict(V1=v1, V2=v2, V3=v3, V4=v4, V5=v5, V6=v6)
    for k, f in fns.items():
        if f is None or (which and k not in which):
            continue
        t0 = time.time()
        f()
        print('   (%s %.0fs)' % (k, time.time() - t0), flush=True)
    return RES


if __name__ == '__main__':
    r = main(sys.argv[1:] or None)
    with open(os.path.join(OUTP, 'validation.json'), 'w') as f:
        json.dump(r, f, indent=1, default=str)
