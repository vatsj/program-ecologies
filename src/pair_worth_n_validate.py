"""Validation of the queue-73 machinery (spec Design 2).  python3 src/pair_worth_n_validate.py V1 V2 V6 V7 V8
V1  stored N = 200 rows (C, C+B*, runs 0-2, mN = 1, both Lambda) reproduced exactly
V2  stored N = 400 rows (C+B*, runs 0-1, mN = 1, both Lambda) reproduced exactly
V6  F / F-minus against the play stated before evaluation (exhaustive over the F + constants catalogue; launch gate)
V7  common random numbers: founder arrays and tails of two arms on one run
V8  inoculation founders (exactly k per slot, one split per island, base founders otherwise C's), F/F4 seed law marginals
"""
import gzip, itertools, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pair_worth as PW
import pair_worth_n as PN
import pair_worth_n_run as NR

OUTP = os.path.join(PW.ROOT, 'runs', 'pair_worth_n')
RES = {}
G = PW.get_game('pw13')
ALL = PW.ALL


def report(name, ok, detail):
    RES[name] = dict(ok=bool(ok), detail=detail)
    print(('PASS ' if ok else 'FAIL ') + name + ' ' + str(detail)[:1500], flush=True)


# ============================================================ V1 / V2
SKIP = {'kern_wall', 'prep_wall', 'rss_gb', 'extra_wall', 'chase', 'supply', 'est_grand', 'est_core', 'core_transitions', 'holders'}
# the stored rows' `structure` list was written by an earlier summarize that kept only the first 60 entries (the current one keeps
# 400): compare the stored list as a prefix of the new one (switch_counts / switch_dirs are compared in full)


def stored_index():
    idx = {}
    for l in gzip.open(os.path.join(PW.ROOT, 'runs', 'pair_worth', 'rows.jsonl.gz'), 'rt'):
        r = json.loads(l)
        if r['game'] == 'pw13':
            idx[(r['arm'], r['N'], r['delta'], r['lam'], r['mN'], r['run'])] = r
    return idx


def reproduce(name, N, arms, runs):
    st = stored_index()
    bad = []; n = 0
    for arm in arms:
        for r in runs:
            recs = NR.run_job((arm, N, r, 0.05, [0.0, 10.0], [1.0], 20))
            for rec in recs:
                new = json.loads(json.dumps(rec))
                old = st[(arm, N, 0.05, rec['lam'], rec['mN'], r)]
                n += 1
                new['structure'] = new['structure'][:len(old['structure'])]
                diff = [k for k in old if k not in SKIP and old[k] != new.get(k)]
                if diff:
                    bad.append(dict(arm=arm, run=r, lam=rec['lam'], differing=diff))
                print('  %s %s run %d lam %g: %s (kern %.0fs)' % (name, arm, r, rec['lam'], 'identical' if not diff else 'DIFF ' + str(diff), rec['kern_wall']), flush=True)
    report('%s stored rows reproduced exactly (N = %d, mN = 1, both Lambda)' % (name, N), not bad, dict(records=n, mismatching=bad))


def v1():
    reproduce('V1', 200, ('C', 'CBs'), (0, 1, 2))


def v2():
    reproduce('V2', 400, ('CBs',), (0, 1))


# ============================================================ V6
def A(s, partner, d):
    return G.act(s, ALL if partner == 'ALL' else partner, d)


def ref_play(spec):
    """independent pure-python GL chain evaluation written from the action equations (no decision lists).
    spec[s]: ('C', action) | ('F', share, c, fallback) | ('B', sigma, c).  pi = (1, 1) ticks for every pair of G1/3."""
    VAC, BRK = 'vac', 'brk'
    hist = {0: [VAC] * 3, 1: [VAC] * 3}

    def box(L, p, a):
        h = hist[L][p]
        return h == VAC or h == a

    def action(s):
        t = spec[s]
        if t[0] == 'C':
            return t[1]
        j, k = PW.others(s)
        if t[0] == 'F':
            _, share, c, fb = t
            grand = any(box(0, j, A(j, 'ALL', a)) and box(0, k, A(k, 'ALL', b))
                        for a in range(7) for b in range(7) if a + b <= 6 - share)
            if grand:
                return A(s, 'ALL', share)
            if fb and box(1, j, A(j, s, 1)):
                return A(s, j, 1)
            if fb and box(1, k, A(k, s, 1)):
                return A(s, k, 1)
            return c
        _, sig, c = t
        if box(0, j, A(j, 'ALL', sig[j])) and box(0, k, A(k, 'ALL', sig[k])):
            return A(s, 'ALL', sig[s])
        if box(1, j, A(j, s, 1)):
            return A(s, j, 1)
        if box(1, k, A(k, s, 1)):
            return A(s, k, 1)
        return c

    prev = None
    for n in range(80):
        val = [action(s) for s in range(3)]
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
    return None


def prog_of(spec, s):
    t = spec[s]
    if t[0] == 'C':
        return PW.const_program(t[1])
    if t[0] == 'F':
        return PN.F_program(G, s, t[1], t[2], fallback=t[3])
    return PW.program(G, 'B', s, t[1], t[2])


def v6():
    """Stated play (written before evaluation; derivations in notes 2.2):
    R1  the world-0 triple is a feasible grand triple (every slot plays (ALL, .) at world 0: F plays its own share, a
        constant its action, and the demands sum to at most 6) => the three slots play exactly those world-0 actions
        (the grand coalition), for F and F-minus alike (the grand line holds at every world once the others are steady
        grand with a feasible pair; Loeb: PA |- []phi -> phi);
    R2  otherwise every F leaves its grand line at world 1 together and never returns, so a grand outcome can arise only from the
        fallback actions themselves (an F's pair handshake or c; a grand outcome then equals the outcome of the c / constant triple);
    R3  F with fallback, three F's or two F's in slots 0, 1 and a constant in slot 2, grand infeasible => pair {0, 1} at (1, 1);
    R4  F-minus, grand infeasible => each F-minus plays its c, each constant its action, from world 1 on;
    R5  F with fallback in slot s and constants in the other two slots, grand infeasible => pair with the first other slot p1 if
        its constant is (s, 1), else with the second p2 if its constant is (s, 1), else F plays c_s."""
    # ---- exhaustive catalogue, F and F-minus separately
    nact = G.nact
    stats = dict()
    allok = True
    for fb, arm in ((True, 'CF'), (False, 'CFm')):
        menu = PN.arm_menu_n(arm, 0.05)
        K = menu.total                                   # 21 constants + 147 (share, c)
        U = [np.arange(K, dtype=np.int64) for _ in range(3)]
        t = PW.ProgTable(menu, U)
        J = t.joint(G)[:K, :K, :K]
        # per slot world-0 action and F flags
        ids = np.arange(K)
        isF = ids >= nact
        share = np.where(isF, (ids - nact) // nact, -1)
        cF = np.where(isF, (ids - nact) % nact, -1)
        w0 = np.zeros((3, K), np.int64)
        for s in range(3):
            for x in range(K):
                w0[s, x] = A(s, 'ALL', int(share[x])) if isF[x] else x
        # grand-feasible world-0 triple
        part = np.zeros((3, K), np.int64); dem = np.zeros((3, K), np.int64)
        for s in range(3):
            part[s] = G.PARTNER[s, w0[s]]; dem[s] = G.DEM[w0[s]]
        allALL = (part[0][:, None, None] == ALL) & (part[1][None, :, None] == ALL) & (part[2][None, None, :] == ALL)
        feas = allALL & ((dem[0][:, None, None] + dem[1][None, :, None] + dem[2][None, None, :]) <= 6)
        o_world0 = G.OUT[w0[0][:, None, None], w0[1][None, :, None], w0[2][None, None, :]]
        kind = G.KIND[J]
        m1 = int((feas & (J != o_world0)).sum())                       # R1: exact outcome id
        c0 = np.where(isF, cF, ids)                                    # fallback action of each member (F: its c; constant: itself)
        o_c = G.OUT[c0[:, None, None], c0[None, :, None], c0[None, None, :]]
        m2 = int(((~feas) & (kind == 1) & (J != o_c)).sum())          # R2: a grand outcome without a feasible world-0 triple can only be the fallbacks' own
        # F identity counts
        nF = isF[:, None, None].astype(int) + isF[None, :, None] + isF[None, None, :]
        cnt = dict(total=int(K ** 3), feasible=int(feas.sum()), feasible_with_F=int((feas & (nF > 0)).sum()), infeasible_with_F=int(((~feas) & (nF > 0)).sum()))
        # R3 (fallback) / R4 (no fallback) / R5
        pair01 = G.oid[(2, 0, (1, 1, 0))]
        m3 = m4 = m5 = 0
        n3 = n4 = n5 = 0
        if fb:
            # three F's, and F F const (slot 2)
            sel = (~feas) & isF[:, None, None] & isF[None, :, None]
            m3 = int((sel & (J != pair01)).sum()); n3 = int(sel.sum())
            # R5: F in exactly one slot s, constants elsewhere
            for s in range(3):
                j, k = PW.others(s)
                for x in np.nonzero(isF)[0]:
                    for xj in range(nact):
                        for xk in range(nact):
                            idx = [0, 0, 0]
                            idx[s] = int(x); idx[j] = xj; idx[k] = xk
                            if feas[tuple(idx)]:
                                continue
                            xs = {s: None, j: xj, k: xk}
                            if xs[j] == A(j, s, 1):
                                act = [0, 0, 0]; act[s] = A(s, j, 1); act[j] = xj; act[k] = xk
                            elif xs[k] == A(k, s, 1):
                                act = [0, 0, 0]; act[s] = A(s, k, 1); act[j] = xj; act[k] = xk
                            else:
                                act = [0, 0, 0]; act[s] = int(cF[x]); act[j] = xj; act[k] = xk
                            exp = G.OUT[act[0], act[1], act[2]]
                            n5 += 1
                            m5 += int(J[tuple(idx)] != exp)
        else:
            # R4: every F-minus plays c, constants their action (non-grand)
            sel = (~feas)
            m4 = int((sel & (J != o_c)).sum()); n4 = int(sel.sum())
        # R3 applies to F F const only when the constant is in slot 2 (F F in slots 0 and 1)
        if fb:
            sel2 = (~feas) & isF[:, None, None] & isF[None, :, None] & (~isF)[None, None, :]
            m3b = int((sel2 & (J != pair01)).sum())
            sel3 = (~feas) & isF[:, None, None] & isF[None, :, None] & isF[None, None, :]
            m3c = int((sel3 & (J != pair01)).sum())
            m3 = m3b + m3c; n3 = int(sel2.sum() + sel3.sum())
        stats[arm] = dict(counts=cnt, R1_mismatch=m1, R2_mismatch=m2, R3_checked=n3, R3_mismatch=m3, R4_checked=n4, R4_mismatch=m4,
                          R5_checked=n5, R5_mismatch=m5)
        allok &= (m1 == 0 and m2 == 0 and m3 == 0 and m4 == 0 and m5 == 0)
        print('   V6 exhaustive', arm, stats[arm], flush=True)
    # ---- independent chain (explicit action equations) against the numba evaluator
    rng = np.random.default_rng(66)
    tests = []
    shares = range(7)
    cs = [int(x) for x in rng.integers(0, nact, 6)]
    for fb in (True, False):
        for a, b, c in itertools.product(shares, repeat=3):                        # every F F F share triple
            for cc in cs[:3]:
                tests.append([('F', a, cc, fb), ('F', b, (cc + 5) % nact, fb), ('F', c, (cc + 11) % nact, fb)])
        for pos in itertools.product((0, 1), repeat=3):                             # F / constant mixtures, every share and constant
            nf = sum(pos)
            if nf in (0, 3):
                continue
            for sh in itertools.product(shares, repeat=nf):
                for xs in itertools.product(range(nact), repeat=3 - nf):
                    if nf == 1 and rng.random() > 0.35:
                        continue
                    if nf == 2 and rng.random() > 0.06:
                        continue
                    spec = []; i1 = 0; i2 = 0
                    for s in range(3):
                        if pos[s]:
                            spec.append(('F', sh[i1], int(rng.integers(nact)), fb)); i1 += 1
                        else:
                            spec.append(('C', xs[i2])); i2 += 1
                    tests.append(spec)
    # 1000 random triples: mixed sigma, infeasible sums, constants mimicking F's grand output and handshake offers, F next to B
    sp = PW.splits(6)
    for _ in range(1000):
        spec = []
        for s in range(3):
            r = rng.random()
            c = int(rng.integers(nact))
            if r < 0.30:
                spec.append(('F', int(rng.integers(7)), c, bool(rng.random() < 0.7)))
            elif r < 0.45:
                spec.append(('B', sp[int(rng.integers(28))], c))
            elif r < 0.65:
                spec.append(('C', A(s, 'ALL', int(rng.integers(7)))))
            elif r < 0.80:
                p = PW.others(s)[int(rng.integers(2))]
                spec.append(('C', A(s, p, 1)))
            else:
                spec.append(('C', c))
        tests.append(spec)
    bad = []
    t0 = time.time()
    for spec in tests:
        progs = [prog_of(spec, s) for s in range(3)]
        t = PW.table_from_programs(G, [[p] for p in progs])
        got = t.play(0, 0, 0)
        ref = ref_play(spec)
        if tuple(got) != ref:
            bad.append((spec, got, ref))
    stats['independent_chain'] = dict(tests=len(tests), mismatches=len(bad), first=str(bad[:2]), wall=round(time.time() - t0, 1))
    allok &= not bad
    print('   V6 independent chain', stats['independent_chain'], flush=True)
    report('V6 F / F-minus against stated play (exhaustive) and against an independent chain evaluation (launch gate)', allok, stats)


# ============================================================ V7
def v7():
    N, r, I = 200, 20, 64
    base = '%s|N%d|I%d' % ('pw13', N, I)
    out = {}
    ok = True
    arms = ('C', 'CBs', 'CG', 'CF', 'CB', 'CF4', 'CFm')
    F = {}
    for a in arms:
        m = PN.arm_menu_n(a, 0.05)
        F[a] = (m, PW.draw_founders(m, base, r, I, N))
    rng_u = np.random.default_rng(PW.seed_int('F', base, r))
    u1 = rng_u.random((I, 3, N)); u2 = rng_u.random((I, 3, N))
    named_pos = u2 < 0.05
    for a in arms[1:]:
        m, f = F[a]
        same_off = (f == F['C'][1])
        # outside the named positions the founders are exactly C's; named positions hold named members (>= nact)
        res = dict(unreplaced_equal=bool(same_off[~named_pos].all()), named_positions_hold_named=bool((f[named_pos] >= G.nact).all()),
                   n_named=int(named_pos.sum()))
        ok &= res['unreplaced_equal'] and res['named_positions_hold_named']
        out[a] = res
    # tails identical across arms
    sc = {}
    for a in ('C', 'CBs', 'CF'):
        m = F[a][0]
        sc[a] = PW.tail_schedule(m, base, r, I, N, 100.0, 2 * N, N / 2.0, 100 * N, [10.0])[10.0]
    for a in ('CBs', 'CF'):
        same = all((sc[a][t] == sc['C'][t]).all() for t in range(4))          # (g, island, slot, victim u): identical streams
        ok &= bool(same); out['tail_' + a + '_vs_C_(g,i,slot,u)'] = bool(same)
    # arrivals: the same arrival rows pick named members exactly when u2 < delta (named share of arrivals)
    out['arrival_named_share'] = {a: float((sc[a][4] >= G.nact).mean()) for a in sc}
    # F and B* replace the same positions with the same constant
    mF, fF = F['CF']; mB, fB = F['CBs']
    posn = named_pos
    cF = (fF[posn] - mF.off[0]) % G.nact; cB = (fB[posn] - mB.off[0]) % G.nact
    out['F_and_Bstar_same_c_at_replaced'] = bool((cF == cB).all()); ok &= bool((cF == cB).all())
    # F share marginal at replaced positions against (7 - s)/28
    shF = (fF[posn] - mF.off[0]) // G.nact
    big = PW.arm_menu('pw13', 'CBs', 0.05)
    emp = np.bincount(shF, minlength=7) / len(shF)
    out['F_share_empirical'] = emp.round(3).tolist(); out['F_share_expected'] = [round((7 - s) / 28, 3) for s in range(7)]
    report('V7 common random numbers: arms share unreplaced founders and tails exactly; F and B* replace the same positions with the same c', ok, out)


# ============================================================ V8
def v8():
    ok = True
    out = {}
    N, I = 200, 64
    for k in (1, 4):
        arm = 'CBk%d' % k
        menu = PN.arm_menu_n(arm)
        r = 21
        f = NR.PN.founders_bk(menu, N, r, I, k)
        base = PW.draw_founders(menu, '%s|N%d|I%d' % ('pw13', N, I), r, I, N)
        diffpos = (f != base)
        per_slot = diffpos.sum(2)
        ok_k = bool((per_slot == k).all())
        # one split per island across the three slots
        sig_ok = True
        for i in range(I):
            sigs = set()
            for s in range(3):
                ids = f[i, s][diffpos[i, s]]
                for u in ids:
                    fi, si, c = menu.decode(int(u))
                    sigs.add(menu.fams[fi].sigmas[si])
            sig_ok &= (len(sigs) == 1)
        # c of each copy = the replaced founder's constant
        c_ok = True
        for i in range(I):
            for s in range(3):
                for p in np.nonzero(diffpos[i, s])[0]:
                    fi, si, c = menu.decode(int(f[i, s, p]))
                    c_ok &= (c == int(base[i, s, p]))
        out[arm] = dict(k_per_slot_every_island=ok_k, one_split_per_island=bool(sig_ok), c_is_replaced_constant=bool(c_ok))
        ok &= ok_k and sig_ok and c_ok
    # F4 seed law: shares <= 4 with weights (7 - s)/25
    m = PN.arm_menu_n('CF4', 1.0 - 1e-9)
    rng = np.random.default_rng(8)
    u = [rng.random((4000, 3, 25)) for _ in range(4)]
    d = m.draw(*u)
    sh = (d - m.off[0]) // G.nact
    emp = np.bincount(sh.ravel(), minlength=7) / sh.size
    exp = np.array([(7 - s) / 25 if s <= 4 else 0 for s in range(7)])
    out['F4_share_empirical'] = emp.round(4).tolist(); out['F4_share_expected'] = exp.round(4).tolist()
    ok &= bool(np.abs(emp - exp).max() < 0.005)
    mF = PN.arm_menu_n('CF', 1.0 - 1e-9)
    d = mF.draw(*u)
    sh = (d - mF.off[0]) // G.nact
    emp = np.bincount(sh.ravel(), minlength=7) / sh.size
    exp = np.array([(7 - s) / 28 for s in range(7)])
    out['F_share_empirical'] = emp.round(4).tolist(); out['F_share_expected'] = exp.round(4).tolist()
    ok &= bool(np.abs(emp - exp).max() < 0.005)
    # F program sizes
    out['F_lines'] = {sh: len(PN.F_program(G, 0, sh, 0)[0]) for sh in range(7)}
    report('V8 inoculation founders (k per slot, one split per island, c = replaced constant); F and F4 share laws', ok, out)


def main(which):
    os.makedirs(OUTP, exist_ok=True)
    fns = dict(V1=v1, V2=v2, V6=v6, V7=v7, V8=v8)
    for k in which:
        t0 = time.time()
        fns[k]()
        print('   (%s %.0fs)' % (k, time.time() - t0), flush=True)
        with open(os.path.join(OUTP, 'validation_%s.json' % k), 'w') as f:
            json.dump({n: v for n, v in RES.items() if n.startswith(k)}, f, indent=1, default=str)


if __name__ == '__main__':
    main(sys.argv[1:] or ['V6', 'V7', 'V8'])
