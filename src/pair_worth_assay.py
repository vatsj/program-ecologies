"""Invasion assays (spec design 2b; notes/pair-worth.md).  Run: python3 src/pair_worth_assay.py

Single islands, no migration, N = 100.  Every invasion is of one individual into a slot of a background in which the other
two slots are monomorphic, so the invader's fitness advantage in its slot is frequency independent: the fixation
probability is the two-type Moran probability with fitness ratio exp(w * (u_inv - u_res)).  Both are reported: the
Monte-Carlo fixation fraction over 2,000 replicates of the same Moran step as the kernel (birth in proportion to count *
exp(w * payoff), uniform death) and the exact value.  The escape hazard is measured with the full kernel (kern_pw, tail
Lambda = 10) from 200 replicate homogeneous grand islands."""
import json, math, os, sys, time
import numpy as np
from numba import njit
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pair_worth as PW
import pair_worth_run as PR

OUTP = os.path.join(PW.ROOT, 'runs', 'pair_worth')
W = 0.3
N = 100


@njit(cache=True)
def fix_mc(N, w, u_res, u_inv, reps, seed):
    np.random.seed(seed)
    fixed = 0
    fr = np.exp(w * u_res); fq = np.exp(w * u_inv)
    for r in range(reps):
        q = 1
        while q > 0 and q < N:
            pq = q * fq / (q * fq + (N - q) * fr)
            birth_q = np.random.random() < pq
            victim_q = np.random.randint(N) < q
            if birth_q and not victim_q:
                q += 1
            elif (not birth_q) and victim_q:
                q -= 1
        if q == N:
            fixed += 1
    return fixed


def fix_exact(N, w, u_res, u_inv):
    d = w * (u_inv - u_res)
    if abs(d) < 1e-12:
        return 1.0 / N
    rho = math.exp(d)
    return (1 - 1 / rho) / (1 - rho ** (-N))


def payoffs(G, progs3):
    """payoff vector (dollars) and outcome of a triple of programs."""
    t = PW.table_from_programs(G, [[p] for p in progs3])
    v = t.play(0, 0, 0)
    o = G.outs[int(G.OUT[v])]
    return [x / G.Gd for x in o[2]], o


def assay(G, name, residents, slot, invader, reps=2000, seed=1):
    """residents: three programs (lines, default); invader replaces one individual of `slot`."""
    ures_vec, ores = payoffs(G, residents)
    inv = list(residents); inv[slot] = invader
    uinv_vec, oinv = payoffs(G, inv)
    ur, ui = ures_vec[slot], uinv_vec[slot]
    fx = fix_mc(N, W, ur, ui, reps, seed)
    return dict(case=name, slot=slot, u_resident=round(ur, 5), u_invader=round(ui, 5), fixed=int(fx), reps=reps,
                p_fix=round(fx / reps, 4), se=round(math.sqrt(max(fx / reps * (1 - fx / reps), 1e-12) / reps), 4),
                p_exact=round(fix_exact(N, W, ur, ui), 5), neutral=bool(abs(ur - ui) < 1e-12), N_p=round(fx / reps * N, 2),
                outcome_resident=str(ores), outcome_invader=str(oinv))


def case_set(gname):
    G = PW.get_game(gname)
    Gd = G.Gd
    sg = (Gd // 3,) * 3
    pe = PW.pi_split(G, 0, 1, sg)               # equal pair split
    A = lambda s, p, d: G.act(s, PW.ALL if p == 'ALL' else p, d)
    z = A(2, 1, Gd)                              # the excluded slot's inert constant
    Gs = [A(s, 'ALL', sg[s]) for s in range(3)]
    P = lambda kind, s, c: PW.program(G, kind, s, sg, c)
    C = PW.const_program
    out = []
    # (i) pair islands
    pairs = {'equal pair': (A(0, 1, pe[0]), A(1, 0, pe[1]))}
    unequal = (A(0, 1, Gd // 3 + Gd // 6 if Gd == 6 else 7), A(1, 0, 0 if Gd == 6 else 3))
    # Gd = 6 (G1/3 is pair worth 2: demands (2, 0)); Gd = 12 (pair worth 10: (7, 3))
    if gname == 'pw13':
        unequal = (A(0, 1, 2), A(1, 0, 0))
    else:
        unequal = (A(0, 1, 7), A(1, 0, 3))
    pairs['unequal pair'] = unequal
    for pn, (a0, a1) in pairs.items():
        res = [C(a0), C(a1), C(z)]
        for kind in ('B', 'K', 'A'):
            out.append(('(i) %s: %s in pair slot 0' % (pn, kind), res, 0, P(kind, 0, a0)))
            out.append(('(i) %s: %s in pair slot 1' % (pn, kind), res, 1, P(kind, 1, a1)))
        out.append(('(i) %s: B in excluded slot 2' % pn, res, 2, P('B', 2, z)))
        out.append(('(i) %s: matching grand constant in excluded slot' % pn, res, 2, C(Gs[2])))
        # bids fixed in both pair slots
        res2 = [P('B', 0, a0), P('B', 1, a1), C(z)]
        out.append(('(i) %s, B in both pair slots: B in excluded slot 2' % pn, res2, 2, P('B', 2, z)))
        out.append(('(i) %s, B in both pair slots: matching grand constant G in slot 2' % pn, res2, 2, C(Gs[2])))
        out.append(('(i) %s, B in both pair slots: K in slot 2' % pn, res2, 2, P('K', 2, z)))
        out.append(('(i) %s, B in both pair slots: constant in slot 2 (control)' % pn, res2, 2, C(A(2, 0, 0))))
    # (ii) B^3 grand island
    resB = [P('B', s, Gs[s]) for s in range(3)]
    for s in range(3):
        out.append(('(ii) B^3: matching grand constant in slot %d' % s, resB, s, C(Gs[s])))
        out.append(('(ii) B^3: blocker K in slot %d' % s, resB, s, P('K', s, Gs[s])))
        out.append(('(ii) B^3: accept-pair bid A in slot %d' % s, resB, s, P('A', s, Gs[s])))
        out.append(('(ii) B^3: level-0 bid B0 in slot %d' % s, resB, s, P('B0', s, Gs[s])))
        out.append(('(ii) B^3: pair constant in slot %d (control)' % s, resB, s, C(A(s, PW.others(s)[0], pe[0]))))
    # (iii) K^2 and the third slot
    for third in range(3):
        two = [s for s in range(3) if s != third]
        resK = [None] * 3
        for s in two:
            resK[s] = P('K', s, Gs[s])
        resK[third] = P('B', third, Gs[third])
        out.append(('(iii) K in slots %s, B in slot %d: constant (G) invades slot %d' % (two, third, third), resK, third, C(Gs[third])))
        out.append(('(iii) K in slots %s, B in slot %d: pair constant invades slot %d' % (two, third, third), resK, third,
                    C(A(third, PW.others(third)[0], pe[0]))))
        resK2 = list(resK); resK2[third] = C(z if third == 2 else A(third, PW.others(third)[0], Gd))
        out.append(('(iii) K in slots %s, constant in slot %d: B invades slot %d' % (two, third, third), resK2, third, P('B', third, resK2[third][1])))
    return G, out


def escape(gname, arm, delta, reps=200, kind_label=''):
    """homogeneous B^3 grand islands (equal split, c = the slot's grand action) under the tail at Lambda = 10, one island each."""
    G, CLA, CLB = PR.game_tables(gname)
    menu = PW.arm_menu(gname, arm, delta)
    Gd = G.Gd; sg = (Gd // 3,) * 3
    geo = PR.geometry(N)
    ids = [menu.member_id('B', sg, G.act(s, PW.ALL, sg[s])) for s in range(3)]
    res = dict(game=gname, arm=arm, reps=reps)
    exits_tail = 0; expo_tail = 0.0; exits_chase = 0; expo_chase = 0.0
    firsts = []; fams = {}; ended = {}
    t0 = time.time()
    for r in range(reps):
        founders = np.zeros((1, 3, N), np.int64)
        for s in range(3):
            founders[0, s, :] = ids[s]
        prep = PR.prepare(gname, arm, r, N, delta, [10.0], I=1, menu=menu, founders=founders)
        o = PR.run_kernel(prep, 10.0, 0.0)
        ser = (CLB if gname == 'pw56' else CLA)[o['modal'].astype(np.int64)][:, 0]
        grand = 1 if gname == 'pw56' else 1                      # grand-eff (B) / core proper (A)
        # first debounced exit from the grand class at or after g0
        ex = None
        g = 0
        H = geo['H']
        bad = np.nonzero(ser != grand)[0]
        for gi in bad:
            if gi + PR.DEBOUNCE > H or (ser[gi:gi + PR.DEBOUNCE] != grand).all():
                ex = int(gi); break
        g0 = geo['g0']; gend = geo['gend']
        if ex is None:
            expo_tail += gend - g0; expo_chase += H - gend
        elif ex < g0:
            ex = ex       # exit before the tail starts (should not happen: no arrivals before g0)
            expo_tail += 0
            exits_tail += 0
        elif ex < gend:
            exits_tail += 1; expo_tail += ex - g0
            firsts.append(ex)
        else:
            exits_chase += 1; expo_tail += gend - g0; expo_chase += ex - gend
        if ex is not None:
            ended[int(ser[min(ex + PR.DEBOUNCE - 1, H)])] = ended.get(int(ser[min(ex + PR.DEBOUNCE - 1, H)]), 0) + 1
            al = o['alog']
            prev = [row for row in al if row[0] <= ex]
            if prev:
                last = prev[-1]
                f = int(prep['table'].FAM[int(last[2]), int(last[3])])
                fams[f] = fams.get(f, 0) + 1
    res.update(exits_tail=exits_tail, exposure_tail_gens=expo_tail, hazard_tail_per_gen=exits_tail / max(expo_tail, 1),
               exits_chase=exits_chase, exposure_chase_gens=expo_chase, hazard_chase_per_gen=exits_chase / max(expo_chase, 1),
               median_first_exit=float(np.median(firsts)) if firsts else None, last_arrival_family_before_exit=fams,
               class_after_exit=ended, wall=round(time.time() - t0, 1))
    return res


def main():
    os.makedirs(OUTP, exist_ok=True)
    out = dict(fixation={}, escape=[])
    for gname in ('pw13', 'pw56'):
        G, cases = case_set(gname)
        rows = []
        for k, (name, res, slot, inv) in enumerate(cases):
            rows.append(assay(G, name, res, slot, inv, reps=2000, seed=1000 + k))
        out['fixation'][gname] = rows
        print(gname, flush=True)
        for r in rows:
            print('  %-90s u_res %.4f u_inv %.4f  fix %.4f (N*p %.2f) exact N*p %.2f' % (r['case'], r['u_resident'], r['u_invader'],
                                                                                          r['p_fix'], r['N_p'], r['p_exact'] * N), flush=True)
    for gname, arm in (('pw13', 'CBs'), ('pw56', 'CB'), ('pw56', 'CBK')):
        e = escape(gname, arm, 0.05, reps=200)
        out['escape'].append(e)
        print(e, flush=True)
    with open(os.path.join(OUTP, 'assays.json'), 'w') as f:
        json.dump(out, f, indent=1)


if __name__ == '__main__':
    main()
