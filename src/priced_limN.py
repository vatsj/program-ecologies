"""Exp 1 and 3 of predictions/2026-10-01-priced-arm.md: eps->0 chain over the
priced modal arm, without and with clique spellings.

    python3 src/priced_limN.py
Writes runs/priced_limN.md/json.
"""
import json, os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import modal as M
from chain import Chain

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def cell(job):
    exp, n, c, m, N = job[:5]
    cm = job[5] if len(job) > 5 else 'per'
    pricing = job[6] if len(job) > 6 else 'atoms'
    L, val, worlds, prov = M.build_priced(n, c, m_cliques=m, clique_mass=cm, pricing=pricing)
    names = prov.names; U = prov.Ufull; P = prov.PCC
    lang = M.ClassLang(prov)
    t = time.time()
    ch = Chain(prov, N=N, w=0.3, verbose=False, eager_poly=False).explore()
    get = lambda s: names.index(s) if s in names else None
    iD, iC, iFB = get('D'), get('C'), get('BOX(THEM(ME))')
    iPB = get('and(BOX(THEM(ME)),BOXD1(THEM(^D)))')
    cliques = [k for k, s in enumerate(names) if s.startswith('CLIQUE')]
    pcc = 0.0; poly = 0.0; pis = {}; key_of = {}
    for key, wgt in zip(ch.keys_list, ch.pi):
        ids, x, kind = ch.states[key]; ids = list(ids); x = np.asarray(x)
        pcc += wgt * float(x @ P[np.ix_(ids, ids)] @ x)
        if len(ids) > 1: poly += wgt
        else: pis[ids[0]] = pis.get(ids[0], 0.0) + wgt; key_of[ids[0]] = key
    pi = lambda k: pis.get(k, 0.0) if k is not None else 0.0
    coop_mass = sum(v for k, v in pis.items() if P[k, k] == 1)
    clique_mass = sum(pi(k) for k in cliques)
    out = dict(exp=exp, n=n, c=c, m=m, N=N, clique_mass_mode=cm, pricing=pricing, pcc=pcc, poly=poly, pi_D=pi(iD), pi_C=pi(iC), pi_FB=pi(iFB), pi_PB=pi(iPB),
               coop_mass=coop_mass, clique_mass=clique_mass, clique_share=clique_mass / coop_mass if coop_mass > 0 else float('nan'),
               cut_flow=ch.cut_flow, indeterminate=len(ch.indeterminate), n_terminal=len(ch.terminal),
               near_closed=int(getattr(ch, 'near_closed', 0)), absorb_error=float(getattr(ch, 'absorb_error', 0.0)),
               hit_clique=hitting_time(ch, key_of.get(iD), [key_of[k] for k in cliques if k in key_of]),
               support=[(ch.describe_state(k, lang), float(p)) for k, p in ch.support(1e-3)][:6])
    # exits from all-FairBot by type
    kFB = key_of.get(iFB)
    ex = dict(strict=0.0, neutral=0.0, other=0.0); dest = {}
    if kFB is not None:
        a = iFB; uaa = U[a, a]
        for b, v in ch.trans.get(kFB, {}).items():
            if b == kFB: continue
            for q, mw in ch.trans_mut[(kFB, b)].items():
                if U[q, a] > uaa + 1e-12: t2 = 'strict'
                elif max(abs(U[q, a] - uaa), abs(U[a, q] - uaa), abs(U[q, q] - uaa)) < 1e-12: t2 = 'neutral'
                else: t2 = 'other'
                ex[t2] += mw; dest[names[q]] = dest.get(names[q], 0.0) + mw
    tot = sum(ex.values())
    out.update(fb_exit=tot, fb_exit_strict=ex['strict'], fb_exit_neutral=ex['neutral'],
               allc_share_fb_exit=dest.get('C', 0.0) / tot if tot else float('nan'),
               time_s=time.time() - t)
    return out


def hitting_time(ch, start, targets):
    """Expected number of mutation events from `start` until the chain first
    enters a target state, over the expanded states (transient fundamental matrix)."""
    if start is None or not targets:
        return float('nan')
    keys = ch.keys_list; idx = {k: i for i, k in enumerate(keys)}
    T = set(targets)
    rest = [k for k in keys if k not in T]
    pos = {k: i for i, k in enumerate(rest)}
    Q = np.zeros((len(rest), len(rest)))
    for k in rest:
        for b, v in ch.trans.get(k, {}).items():
            if b in pos: Q[pos[k], pos[b]] += v
    try:
        t = np.linalg.solve(np.eye(len(rest)) - Q, np.ones(len(rest)))
    except np.linalg.LinAlgError:
        return float('inf')
    return float(t[pos[start]]) if start in pos else 0.0


def jobs():
    J = []
    for n in (6, 8):
        for N in (100, 1000, 10000, 30000):
            J.append(('exp1', n, 0.0, 0, N, 'per', 'atoms'))
            for c in (1e-3, 1e-2):
                for pricing in ('atoms', 'depth', 'lazy'):
                    J.append(('exp1', n, c, 0, N, 'per', pricing))
        J.append(('exp1', n, 0.1, 0, 100, 'per', 'atoms'))
    for m, cm in ((1, 'per'), (4, 'per'), (4, 'total')):
        for c in (0.0, 1e-2):
            for N in (1000, 10000):
                J.append(('exp3', 8, c, m, N, cm, 'atoms'))
    return J


def main():
    J = sorted(jobs(), key=lambda j: (-j[1], -j[4]))
    rows = []
    with Pool(9) as pool:
        for r in pool.imap_unordered(cell, J):
            rows.append(r)
            print('%s n=%d c=%g m=%d %s N=%d: P(C,C) %.4f pi(D) %.4f pi(FB) %.4f pi(C) %.4f cliques %.4f (share %.2f) FB exit strict %.2e neutral %.2e ALLC share %.2f (%.0fs)' % (
                r['exp'], r['n'], r['c'], r['m'], r['pricing'], r['N'], r['pcc'], r['pi_D'], r['pi_FB'], r['pi_C'], r['clique_mass'], r['clique_share'],
                r['fb_exit_strict'], r['fb_exit_neutral'], r['allc_share_fb_exit'], r['time_s']), flush=True)
            json.dump(rows, open(os.path.join(ROOT, 'runs', 'priced_limN.json'), 'w'), indent=1, default=str)
    rows.sort(key=lambda r: (r['exp'], r['n'], r['m'], r['clique_mass_mode'], r['pricing'], r['c'], r['N']))
    L = ['# Priced modal arm: eps->0 chain (PD, w = 0.3); Exp 1 (no cliques) and Exp 3 (m clique spellings)', '',
         '| exp | n | m (mass) | pricing | c | N | P(C,C) | π(all-D) | π(all-FairBot) | π(all-ALLC) | π(cliques) | clique share of coop | FairBot exits: strict / neutral | ALLC share of FB exits | hitting time to cliques (mutation events) | terminal classes | support (top 4) |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        L.append('| %s | %d | %d (%s) | %s | %g | %d | %.4f | %.4f | %.4f | %.4f | %.4f | %.2f | %.2e / %.2e | %.2f | %.3g | %d | %s |' % (
            r['exp'], r['n'], r['m'], r['clique_mass_mode'], r['pricing'], r['c'], r['N'], r['pcc'], r['pi_D'], r['pi_FB'], r['pi_C'], r['clique_mass'], r['clique_share'],
            r['fb_exit_strict'], r['fb_exit_neutral'], r['allc_share_fb_exit'], r['hit_clique'], r['n_terminal'], '; '.join('%s %.3f' % sp for sp in r['support'][:4])))
    open(os.path.join(ROOT, 'runs', 'priced_limN.md'), 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))


if __name__ == '__main__':
    main()
