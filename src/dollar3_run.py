"""Run one chain cell of the three-player dollar and write its statistics.

    python3 src/dollar3_run.py --arm modal --N 100 [--theta 1e-9]
arms: constants, weak, modalPA, modal.  Writes runs/dollar3/<arm>_N<N>.json.
"""
import argparse, itertools, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import dollar3 as D
from dollar3_chain import Chain3, log_rho

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COAL = ['G', 'P12', 'P13', 'P23', 'X']        # grand, pairs (1-based slot names), disagreement


def coalition(pay, typ):
    if typ == 4: return 'X'
    if typ == 0: return 'G'
    s = [i for i in range(3) if pay[i] > 0]
    return 'P%d%d' % (s[0] + 1, s[1] + 1)


def load_classes(arm):
    if arm == 'constants':
        arm = 'weak'
    f = np.load(os.path.join(ROOT, 'runs', 'dollar3_classes_%s_slot1.npz' % arm))
    return f['payoff']


def build_chain(arm, N, w, theta, max_states):
    lang_arm = 'weak' if arm == 'constants' else arm
    L, S, mu, cnt, size = D.build(lang_arm, 6)
    cls = load_classes(arm)
    ch = Chain3(lang_arm, S, cls, mu, N, w=w, theta=theta, max_states=max_states, constants_only=(arm == 'constants'))
    return ch, S


def exits_of(ch, code, full=False):
    """Every single-mutant move out of `code`: list of dicts (slot, class, mass,
    du, rho, prob, dest pay, dest typ, kind)."""
    a = ch.decode(code); x = [ch.reps[s, a[s]] for s in range(3)]
    hist = np.empty((2, 3), np.int64); val = np.empty(3, np.int64); u = np.empty(3, np.int64)
    t0 = D.enc_into(ch.ia, *ch.A, x[0], x[1], x[2], hist, val, u); u0 = u.copy()
    out = []
    for s in range(3):
        U, T = D.slot_row(ch.ia, *ch.A, s, x[0], x[1], x[2])
        for q in range(ch.Kc):
            if q == a[s] or ch.mass[s, q] == 0: continue
            r = ch.reps[s, q]
            du = (U[r, s] - u0[s]) / 6.0
            rho = float(np.exp(log_rho(ch.w * du, float(ch.N))))
            same = (U[r] == u0).all() and T[r] == t0
            if du > 1e-12: kind = 'strict'
            elif du < -1e-12: kind = 'deleterious'
            else: kind = 'neutral-keep' if same else 'neutral-change'
            out.append(dict(slot=s, cls=q, mass=ch.mass[s, q] / 3, du=du, rho=rho, prob=ch.mass[s, q] / 3 * rho,
                            pay=U[r].copy(), typ=int(T[r]), kind=kind))
    return out, u0, t0


def bridge_analysis(ch, code, depth3=False):
    """Exit decomposition and neutral-bridge mass of one triple."""
    ex, u0, t0 = exits_of(ch, code)
    dec = {}
    for e in ex:
        d = dec.setdefault(e['kind'], dict(mass=0.0, prob=0.0))
        d['mass'] += e['mass']; d['prob'] += e['prob']
    bridges = 0.0; nbr = 0; examples = []
    a = ch.decode(code)
    for e in ex:
        if e['kind'] != 'neutral-keep': continue
        b = list(a); b[e['slot']] = e['cls']
        code2 = ch.code(*b)
        ex2, _, _ = exits_of(ch, code2)
        opened = [f for f in ex2 if f['kind'] in ('strict', 'neutral-change')]
        strict_new = [f for f in ex2 if f['kind'] == 'strict']
        if strict_new:
            bridges += e['mass']; nbr += 1
            if len(examples) < 3:
                f = max(strict_new, key=lambda f: f['prob'])
                examples.append(dict(entrant=ch.S.src(e['slot'], ch.reps[e['slot'], e['cls']]), slot=e['slot'] + 1,
                                     then=ch.S.src(f['slot'], ch.reps[f['slot'], f['cls']]), then_slot=f['slot'] + 1,
                                     then_rho=f['rho'], then_pay=(f['pay'] / 6).round(3).tolist()))
    closed = (dec.get('strict', {}).get('mass', 0) == 0 and dec.get('neutral-change', {}).get('mass', 0) == 0 and nbr == 0)
    return dict(decomposition=dec, bridge_mass=bridges, n_bridges=nbr, bridge_examples=examples, drift_closed_depth2=closed)


def describe(ch, code):
    a = ch.decode(code)
    return ' | '.join(ch.S.src(s, ch.reps[s, a[s]]) for s in range(3))


def analyse(ch, args):
    codes, pi, pay, typ = ch.codes, ch.pi, ch.pay, ch.typ
    n = len(codes)
    lab = np.array([coalition(pay[i], typ[i]) for i in range(n)])
    out = dict(arm=args.arm, N=args.N, w=args.w, theta=args.theta, states=n, cut_flow=ch.cut_flow, rounds=ch.log, Kc=ch.Kc)
    # outcome masses
    out['mass_by_type'] = {D.OUT_NAMES[t]: float(pi[typ == t].sum()) for t in range(5)}
    out['mass_by_coalition'] = {c: float(pi[lab == c].sum()) for c in COAL}
    p6 = pay / 6.0
    out['efficiency'] = float(pi @ p6.sum(1))
    out['E_max_share'] = float(pi @ p6.max(1))
    out['P_some_slot_zero'] = float(pi @ (p6.min(1) == 0))
    out['P_pair'] = float(pi[np.isin(typ, [1, 2, 3])].sum())
    out['mean_slot_share'] = (pi @ p6).tolist()
    # currents between coalition states
    i = ch.src; j = ch.dst_idx; f = pi[i] * ch.pr
    J = {}
    for A in COAL:
        for B in COAL:
            if A != B:
                J[A + '>' + B] = float(f[(lab[i] == A) & (lab[j] == B)].sum())
    out['flows'] = J
    C = (J['P12>P13'] - J['P13>P12']) + (J['P13>P23'] - J['P23>P13']) + (J['P23>P12'] - J['P12>P23'])
    pairflow = sum(J[a + '>' + b] for a in ('P12', 'P13', 'P23') for b in ('P12', 'P13', 'P23') if a != b)
    out['circulation'] = dict(C=C, total_pair_to_pair=pairflow)
    # pair-to-pair moves by mover role: the slot that changed is the new member (excluded slot bids in) or the pivot
    roles = dict(excluded_bids_in=0.0, pivot_switches=0.0, dropped_slot_moves=0.0)
    sel = np.isin(lab[i], ['P12', 'P13', 'P23']) & np.isin(lab[j], ['P12', 'P13', 'P23']) & (lab[i] != lab[j])
    for e in np.nonzero(sel)[0]:
        a = ch.decode(codes[i[e]]); b = ch.decode(codes[j[e]])
        mv = [s for s in range(3) if a[s] != b[s]][0]
        before = {int(lab[i[e]][1]) - 1, int(lab[i[e]][2]) - 1}; after = {int(lab[j[e]][1]) - 1, int(lab[j[e]][2]) - 1}
        if mv not in before: roles['excluded_bids_in'] += f[e]
        elif mv in after: roles['pivot_switches'] += f[e]
        else: roles['dropped_slot_moves'] += f[e]
    out['pair_to_pair_by_mover'] = roles
    # dwell per visit (mutation events) and lumped relaxation time
    dwell = {}
    M = np.zeros((5, 5))
    for a_, A in enumerate(COAL):
        pa = float(pi[lab == A].sum())
        outA = sum(J[A + '>' + B] for B in COAL if B != A)
        dwell[A] = pa / outA if outA > 0 else float('inf')
        for b_, B in enumerate(COAL):
            if A != B and pa > 0: M[a_, b_] = J[A + '>' + B] / pa
        M[a_, a_] = 1 - M[a_].sum()
    out['dwell_events'] = dwell
    ev = np.sort(np.abs(np.linalg.eigvals(M)))[::-1]
    out['lumped_relaxation_events'] = float(1 / (1 - ev[1])) if len(ev) > 1 and ev[1] < 1 else float('inf')
    # pi invariance under slot relabeling
    S = ch.S
    perms = list(itertools.permutations(range(3)))
    idx = {int(c): k for k, c in enumerate(codes)}
    worst = 0.0
    for sg in perms:
        P = S.permute(sg)
        cm = [ch.cls[sg[s]][P[s][ch.reps[s]]] for s in range(3)]
        for k in np.argsort(-pi)[:2000]:
            a = ch.decode(codes[k]); b = [0, 0, 0]
            for s in range(3): b[sg[s]] = cm[s][a[s]]
            k2 = idx.get(ch.code(*b))
            pv = pi[k2] if k2 is not None else 0.0
            worst = max(worst, abs(pv - pi[k]) / max(pi[k], 1e-300))
    out['relabel_pi_max_rel_diff_top2000'] = worst
    # support
    order = np.argsort(-pi)
    out['support'] = [dict(pi=float(pi[k]), state=describe(ch, codes[k]), pay=p6[k].round(3).tolist(), type=D.OUT_NAMES[typ[k]],
                           coalition=lab[k]) for k in order[:30]]
    conds = [k for k in order if any(ch.S.nat[s, ch.reps[s, ch.decode(codes[k])[s]]] > 0 for s in range(3))]
    out['mass_with_conditional'] = float(pi[conds].sum()) if conds else 0.0
    out['top_conditional'] = [dict(pi=float(pi[k]), state=describe(ch, codes[k]), type=D.OUT_NAMES[typ[k]]) for k in conds[:15]]
    # entry into each coalition type from disagreement, by mover kind
    entry = {}
    for B in ('G', 'P12', 'P13', 'P23'):
        selB = (lab[i] == 'X') & (lab[j] == B)
        entry[B] = float(f[selB].sum()) / max(float(pi[lab == 'X'].sum()), 1e-300)
    out['entry_rate_from_X'] = entry
    # transitions out of the top states
    trans = []
    for k in order[:8]:
        rows = np.nonzero(ch.src == k)[0]
        top = rows[np.argsort(-ch.pr[rows])[:5]]
        tot = float(ch.out_tot[k])
        trans.append(dict(state=describe(ch, codes[k]), pi=float(pi[k]), total_exit_incl_cut=tot,
                          top=[dict(p=float(ch.pr[r]), to=describe(ch, codes[ch.dst_idx[r]])) for r in top]))
    out['transitions'] = trans
    # efficient triples: exit decomposition, bridges, entry from X
    eff = [k for k in order if typ[k] in (0, 1, 2)]
    tri = []
    t0 = time.time()
    for k in eff[:args.n_eff]:
        ba = bridge_analysis(ch, int(codes[k]))
        selk = (j == k) & (lab[i] == 'X')
        ba.update(state=describe(ch, codes[k]), pi=float(pi[k]), type=D.OUT_NAMES[typ[k]],
                  entry_flux_from_X=float(f[selk].sum()), entry_rate_from_X=float(f[selk].sum()) / max(float(pi[lab == 'X'].sum()), 1e-300))
        tri.append(ba)
    out['efficient_triples'] = tri
    # P1 sweep: efficient states with pi >= 1e-6 plus all efficient constant triples
    sweep = [k for k in eff if pi[k] >= args.p1_min][:args.p1_cap]
    closed = []
    for k in sweep:
        ba = bridge_analysis(ch, int(codes[k]))
        if ba['drift_closed_depth2']:
            closed.append(dict(state=describe(ch, codes[k]), pi=float(pi[k]), type=D.OUT_NAMES[typ[k]]))
    out['p1_sweep'] = dict(checked=len(sweep), closed=closed, closed_mass=float(sum(c['pi'] for c in closed)),
                           checked_mass=float(pi[sweep].sum()), time_s=time.time() - t0)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--arm', required=True, choices=['constants', 'weak', 'modalPA', 'modal'])
    ap.add_argument('--N', type=float, required=True)
    ap.add_argument('--w', type=float, default=0.3)
    ap.add_argument('--theta', type=float, default=1e-9)
    ap.add_argument('--max_states', type=int, default=400000)
    ap.add_argument('--n_eff', type=int, default=12)
    ap.add_argument('--p1_min', type=float, default=1e-6)
    ap.add_argument('--p1_cap', type=int, default=400)
    args = ap.parse_args()
    t = time.time()
    ch, S = build_chain(args.arm, args.N, args.w, args.theta, args.max_states)
    ch.explore()
    out = analyse(ch, args)
    out['time_s'] = time.time() - t
    os.makedirs(os.path.join(ROOT, 'runs', 'dollar3'), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, 'runs', 'dollar3', '%s_N%d.json' % (args.arm, args.N)), 'w'), indent=1, default=float)
    print(json.dumps({k: out[k] for k in ('arm', 'N', 'states', 'cut_flow', 'mass_by_type', 'mass_by_coalition', 'efficiency', 'E_max_share',
                                          'P_some_slot_zero', 'circulation', 'dwell_events', 'time_s')}, indent=1, default=float))


if __name__ == '__main__':
    main()
