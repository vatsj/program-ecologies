"""E1: matched control.  W0 = weak arm without X and ROLE (simulation);
M0 = modal arm with the PA box only (provability).  Isomorphic grammars, same
prior; only the meaning of an application differs.  epsilon->0 chain, PD.

    python3 src/matched_control.py
Writes runs/matched_control.md/json.
"""
import json, os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from run import get_language, get_provider, ROOT
from game import Game
from chain import Chain
import modal as M


class Named:
    def __init__(self, names, bits): self.names, self.bits = names, bits
    def src(self, i): return self.names[int(i)]


def build(arm, n):
    if arm == 'M0':
        L, val, worlds, prov = M.build(n, kinds=((0, 0),))
        return prov.Ufull, prov.PCC, prov, Named(prov.names, prov.bits), L.n_programs
    game = Game.load(os.path.join(ROOT, 'games', 'pd.yaml')); game.role = False; game.nroles = 1
    lang = get_language('weak', n, False, False, game)
    prov, div = get_provider(lang, game, 'weak', n, False, 'square', False)
    # chain ids are program ids; class reps
    reps = [c[0] for c in prov.classes]
    U = prov.U(reps)
    # deterministic arm (no X, no ROLE): P(C,C) of a pair = both earn R = 0
    PCC = ((np.abs(U) < 1e-9) & (np.abs(U.T) < 1e-9)).astype(float)
    return U, PCC, prov, lang, len(prov.ids)


def cell(job):
    arm, n, N, w = job
    U, PCC, prov, lang, nprog = build(arm, n)
    reps = [c[0] for c in prov.classes]; pos = {r: k for k, r in enumerate(reps)}
    names = [lang.src(r) for r in reps]
    t = time.time()
    ch = Chain(prov, N=N, w=w, verbose=False, eager_poly=False).explore()
    pcc = 0.0; mono = {}
    for key, wgt in zip(ch.keys_list, ch.pi):
        ids, x, kind = ch.states[key]; ix = [pos[int(p)] for p in ids]; x = np.asarray(x)
        pcc += wgt * float(x @ PCC[np.ix_(ix, ix)] @ x)
        if len(ids) == 1: mono[ix[0]] = (key, wgt)
    iD = names.index('D')
    coop = [(wgt, k, key) for k, (key, wgt) in mono.items() if PCC[k, k] == 1 and k != names.index('C')]
    coop.sort(reverse=True)
    out = dict(arm=arm, n=n, N=N, w=w, programs=nprog, classes=len(reps), pcc=pcc, pi_D=mono.get(iD, (None, 0.0))[1],
               cut_flow=ch.cut_flow, indeterminate=len(ch.indeterminate),
               support=[(ch.describe_state(k, lang), float(p)) for k, p in ch.support(1e-3)][:6])
    if coop:
        wgt, a, key = coop[0]
        uaa = U[a, a]; ex = dict(strict=0.0, neutral=0.0, other=0.0)
        for b, v in ch.trans.get(key, {}).items():
            if b == key: continue
            for q, mw in ch.trans_mut[(key, b)].items():
                qi = pos[int(q)]
                if U[qi, a] > uaa + 1e-9: ex['strict'] += mw
                elif max(abs(U[qi, a] - uaa), abs(U[a, qi] - uaa), abs(U[qi, qi] - uaa)) < 1e-9: ex['neutral'] += mw
                else: ex['other'] += mw
        rho = [v[0] for (s, b, q), v in ch.edge_rho.items() if s == mono.get(iD, (None,))[0] and b == key]
        out.update(top_coop=names[a], pi_top=wgt, rho_enter=float(max(rho)) if rho else 0.0, exits=ex)
    out['time_s'] = time.time() - t
    return out


def main():
    jobs = [(arm, n, N, 0.3) for arm in ('W0', 'M0') for n in (6, 7) for N in (100, 1000, 10000, 30000)]
    for arm, n in {(j[0], j[1]) for j in jobs}:
        build(arm, n)                   # warm the square-evaluation cache before forking
    with Pool(8) as pool:
        rows = pool.map(cell, jobs)
    json.dump(rows, open(os.path.join(ROOT, 'runs', 'matched_control.json'), 'w'), indent=1, default=str)
    L = ['# E1 matched control: W0 (simulation, weak arm without X/ROLE) vs M0 (provability, PA box only); PD, w = 0.3, eps->0 chain', '',
         '| arm | n | N | programs | classes | P(C,C) | π(all-D) | top cooperative state | its π | ρ_enter | exits from it: strict / neutral / other | cut flow |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        ex = r.get('exits', {})
        L.append('| %s | %d | %d | %d | %d | %.4f | %.4f | `%s` | %.4f | %.4f | %.2e / %.2e / %.2e | %.1e |' % (
            r['arm'], r['n'], r['N'], r['programs'], r['classes'], r['pcc'], r['pi_D'], r.get('top_coop', '—'), r.get('pi_top', 0), r.get('rho_enter', 0),
            ex.get('strict', 0), ex.get('neutral', 0), ex.get('other', 0), r['cut_flow']))
    open(os.path.join(ROOT, 'runs', 'matched_control.md'), 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))


if __name__ == '__main__':
    main()
