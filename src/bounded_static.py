"""Static map of the semantic legibility gate (specs/2026-10-04-bounded-provers.md, items 1 and 5).

    python3 src/bounded_static.py          (writes runs/bounded-provers-static.json)
"""
import os, sys, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import modal as M
from bounded import (build_arm, lang, cost_matrix, _evaluate_online, _evaluate_gated, BUDGETS, INF, FB, PB, PSTAR, ROOT)

NAMED = [('FairBot', FB), ('FB1', 'BOX1(THEM(ME))'), ('BTT', 'BOX(THEM(THEM))'), ('BTT1', 'BOX1(THEM(THEM))'),
         ('PrudentBot', PB), ('P*', PSTAR)]


def free_context(n):
    import moat_static as MS
    a = build_arm(n, 'global', INF); prov = a['prov']
    sm = MS.static_map(n, prov)
    KFB = []
    for r in sm['classes_rows']:
        if r['in_KFB']:
            KFB += prov.members[prov.names.index(r['name'])]
    allc = prov.members[prov.names.index('C')]
    return dict(KFB=[int(c) for c in KFB], allc=[int(c) for c in allc])


def static_b(n, b, free_ctx):
    import moat_static as MS
    a = build_arm(n, 'global', b); prov = a['prov']; L = lang(n)
    val = a['val']; gate = a['gate']; nat = L.arrays()[0]
    mu = L.mu_canon / L.mu_canon.sum()
    K = len(nat)
    P = (val == 1) & (val.T == 1)
    selfc = np.diag(val) == 1
    iC, iD, iFB = L.rep.index('C'), L.rep.index('D'), L.rep.index(FB)
    U = a['U']
    allc_b = {c for c in range(K) if np.array_equal(U[c], U[iC]) and np.array_equal(U[:, c], U[:, iC])}
    sm = MS.static_map(n, prov)
    cl = MS.closure(prov)
    KFBx = [f for f in free_ctx['KFB'] if f not in set(free_ctx['allc'])]

    def univ_old(x):
        return float(mu[[f for f in KFBx if P[x, f]]].sum() / mu[KFBx].sum())

    def univ_wb(x):
        S = [f for f in range(K) if selfc[f] and f not in allc_b and gate[x, f]]
        m = mu[S].sum()
        return float(mu[[f for f in S if P[x, f]]].sum() / m) if m > 0 else float('nan')
    cost = cost_matrix(nat, a['fp']['last'])
    named = {}
    for lab, s in NAMED:
        if s not in L.rep: continue
        x = L.rep.index(s)
        leg = gate[x]
        named[lab] = dict(self_coop=bool(val[x, x]), self_cost=float(cost[x, x]), coop_ALLC=bool(val[x, iC]), coop_D=bool(val[x, iD]),
                          coop_FB=bool(P[x, iFB]), legible_mu=float(mu[leg].sum()),
                          legible_selfcoop_mu=float(mu[leg & selfc].sum()), selfcoop_mu=float(mu[selfc].sum()),
                          univ_old=univ_old(x), univ_wb=univ_wb(x),
                          legible_named=[l2 for l2, s2 in NAMED if s2 in L.rep and gate[x, L.rep.index(s2)]],
                          coop_named=[l2 for l2, s2 in NAMED if s2 in L.rep and P[x, L.rep.index(s2)]])
    rep_c = {nm: L.rep.index(nm) for nm in prov.names}
    closed_ids = {c['id'] for c in sm['components'] if c['closed']}
    cls_closed = []
    for r in sm['classes_rows']:
        if r['comp'] in closed_ids:
            x = rep_c[r['name']]
            cls_closed.append(dict(name=r['name'], mu=r['mu'], comp=r['comp'], univ_old=univ_old(x), univ_wb=univ_wb(x),
                                   coop_FB=bool(P[x, iFB]), coop_ALLC=bool(val[x, iC]), self_cost=float(cost[x, x]),
                                   members=len(prov.members[prov.names.index(r['name'])])))
    # suckerable / faker structure for named
    return dict(n=n, b=b, classes=len(prov.names), self_coop_classes=sm['self_coop'], mu_self_coop=sm['mu_self_coop'],
                n_components=sm['n_components'], n_closed=sm['n_closed'], mu_closed=sm['mu_closed'],
                closure_H=dict(n_closed=cl['n_closed'], mu_closed=cl['mu_closed'], mu_closed_univ=cl['mu_closed_univ'], FB_closed=cl['FB_closed'],
                               closed=[(r['name'], r['mu'], r['coop_FB']) for r in cl['closed']][:12]),
                closed_components=[dict(id=c['id'], size=c['size'], mu=c['mu'], has_FB=c['has_FB'], has_ALLC=c['has_ALLC'], top=c['top'][:4])
                                   for c in sm['components'] if c['closed']],
                closed_classes=sorted(cls_closed, key=lambda r: -r['mu']),
                KFB_size=sm['KFB_size'], KFB_mu=sm['KFB_mu'], named=named,
                components=[dict(id=c['id'], size=c['size'], mu=c['mu'], closed=c['closed'], has_FB=c['has_FB'], has_ALLC=c['has_ALLC'],
                                 n_suckerable=c['n_suckerable'], top=c['top'][:3]) for c in sm['components'][:8]],
                frontier=sm['frontier'][:10])


def thresholds(n):
    """Self-cooperation of every free prover (non-constant, self-cooperating, defects on D) across global budgets."""
    L = lang(n); nat = L.arrays()[0]; mu = L.mu_canon / L.mu_canon.sum()
    iD = L.rep.index('D'); iC = L.rep.index('C')
    free = build_arm(n, 'global', INF)['val']
    provers = [c for c in range(len(nat)) if nat[c] > 0 and free[c, c] == 1 and free[c, iD] == 0]
    vals = {b: build_arm(n, 'global', b)['val'] for b in BUDGETS}
    rows = []; nonmono = 0
    for c in provers:
        seq = [bool(vals[b][c, c]) for b in BUDGETS]
        bstar = next((b for i, b in enumerate(BUDGETS) if all(seq[i:])), None)
        if any(seq[i] and not seq[i + 1] for i in range(len(seq) - 1)): nonmono += 1
        sel = {str(b): bool(vals[b][c, iC]) for b, s in zip(BUDGETS, seq) if not s}
        rows.append(dict(name=L.rep[c], mu=float(mu[c]), bstar=bstar, seq=seq, coop_ALLC_when_not_selfcoop=sel))
    hist = {}
    for r in rows:
        k = str(r['bstar']); hist[k] = hist.get(k, 0.0) + r['mu']
    mp = mu[provers].sum()
    share = {str(b): float(mu[[c for c in provers if vals[b][c, c]]].sum() / mp) for b in BUDGETS}
    sel_share = {}
    for b in BUDGETS:
        below = [c for c in provers if not vals[b][c, c]]
        sel_share[str(b)] = dict(n_below=len(below), mu_below=float(mu[below].sum() / mp),
                                 frac_coop_ALLC=float(mu[[c for c in below if vals[b][c, iC]]].sum() / mu[below].sum()) if below else None)
    return dict(n=n, n_provers=len(provers), mu_provers=float(mp), bstar_mu_hist={k: v / mp for k, v in hist.items()},
                share_selfcoop=share, below_threshold=sel_share, nonmonotone=nonmono, rows=sorted(rows, key=lambda r: -r['mu'])[:40])


def sibling_language(n):
    """L_n (levels 0, 1) plus, for every non-constant canonical x that defects on D, its sibling y = or(x, psi_K) and
    faker z = BOX_K(THEM(^D)) (src/conj4.py), at prior mass 0, whatever their size."""
    import modal_lv as LV, conj4 as C4
    kinds = tuple((k, l) for l in range(2) for k in (M.KC, M.KD))
    L = LV.ModalLanguageLv(n, kinds)
    K0 = len(L.funcs)
    free_val = _evaluate_gated(*L.arrays(), np.ones((K0, K0), np.bool_), 2, 300)[0]
    iD = L.op('D')
    sib = {}
    for c in range(K0):
        if L.funcs[c][2] == 0 or free_val[c, iD] == 1:
            continue
        x = C4.parse(L.rep[c])
        K, y, z = C4.sibling(x)
        sib[c] = (K, C4.to_op(L, y), C4.to_op(L, z), C4.size(y))
    return L, C4.wide_arrays(L), sib, K0


def siblings(n):
    Ls, arrs, sib, K0 = sibling_language(n)
    nat = arrs[0]
    mu = Ls.mu_canon[:K0] / Ls.mu_canon[:K0].sum()
    iD = Ls.op('D')
    out = {}
    for b in BUDGETS:
        bv = np.full(len(nat), b, float)
        val, w, last, hc, hd, gate, closew = _evaluate_online(*arrs, bv, 3, 300)
        assert w >= 0
        ref = build_arm(n, 'global', b)['val']
        cost = cost_matrix(nat, last)
        rows = []
        for c, (K, cy, cz, ysz) in sib.items():
            if val[c, c] != 1 or val[c, iD] == 1:
                continue
            adj = bool(val[c, cy] == 1 and val[cy, c] == 1 and val[cy, cy] == 1)
            rows.append(dict(name=Ls.rep[c], mu=float(mu[c]), K=int(K), y_size=int(ysz), k_y=int(nat[cy]),
                             cost_x_reads_y=float(cost[c, cy]), self_cost_x=float(cost[c, c]), legible=bool(gate[c, cy]),
                             x_coop_y=bool(val[c, cy]), y_coop_x=bool(val[cy, c]), y_self=bool(val[cy, cy]), adjacent=adj,
                             y_suckered_by_z=bool(val[cy, cz] == 1 and val[cz, cy] == 0)))
        out[str(b)] = dict(b=b, consistent_with_Ln=bool(np.array_equal(val[:K0, :K0], ref)), n_x=len(rows),
                           mu_x=float(sum(r['mu'] for r in rows)), n_legible=sum(r['legible'] for r in rows),
                           n_adjacent=sum(r['adjacent'] for r in rows),
                           n_adjacent_suckerable=sum(r['adjacent'] and r['y_suckered_by_z'] for r in rows),
                           mu_adjacent=float(sum(r['mu'] for r in rows if r['adjacent'])),
                           min_cost_ratio=float(min((r['cost_x_reads_y'] / r['self_cost_x'] for r in rows), default=float('nan'))),
                           rows=sorted(rows, key=lambda r: -r['mu']))
    return out


def fixedpoint_report(n):
    """Joint-iteration diagnostics (the spec's semantics) and the adopted online gate, per b."""
    L = lang(n); nat = L.arrays()[0]
    rel = (nat[:, None] > 0) & (nat[None, :] > 0)
    rows = []
    for b in BUDGETS:
        fp = build_arm(n, 'global', b)['fp']; j = fp['joint']
        rows.append(dict(b=b, worlds=fp['worlds'], masked_rel=float(1 - fp['gate'][rel].mean()), n_masked=int((~fp['gate'] & rel).sum()),
                         gate_consistent=fp['gate_consistent'], fixed_gate_play_diff=fp['fixed_gate_play_diff'],
                         sound_checked=fp['sound_checked'].tolist(), sound_bad=fp['sound_bad'].tolist(),
                         joint_rounds=j['rounds'], joint_cycle=j['cycle'], joint_converged=j['converged'], joint_changes=j['changes'],
                         joint_play_diff=j['play_diff_vs_online'], joint_gate_diff=j['gate_diff_vs_online'],
                         free_gate_diff=j['free_gate_diff_vs_online'], classes=len(build_arm(n, 'global', b)['prov'].names),
                         pairs=int(len(nat) ** 2)))
    # b = inf reproduces the free arm exactly
    L0, val0, w0, prov0 = M.build(n)
    a = build_arm(n, 'global', INF)
    rows.append(dict(b='inf-check', val_equal=bool(np.array_equal(a['val'], val0)),
                     U_equal=bool(np.array_equal(a['prov'].Ufull, prov0.Ufull)), names_equal=a['prov'].names == prov0.names))
    return rows


def main():
    res = {}
    for n in (6, 8):
        t = time.time()
        fc = free_context(n)
        res[str(n)] = dict(fixedpoint=fixedpoint_report(n), thresholds=thresholds(n),
                           static={str(b): static_b(n, b, fc) for b in BUDGETS}, siblings=siblings(n))
        print('n=%d done (%.0fs)' % (n, time.time() - t), flush=True)
    json.dump(res, open(os.path.join(ROOT, 'runs', 'bounded-provers-static.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
