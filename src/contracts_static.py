"""Static part of proof-carrying contracts v1: alphabet, compatibility matrix, validity breadth, the gate's joint
fixed point at b in {2, 4, inf}, the certified-implication audit, and the type tables cached for the runs.

    python3 src/contracts_static.py
Writes runs/contracts_static.json and runs/contracts_types.npz.
"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import contracts as CT
from modal import PD

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BS = (CT.INF, 4, 2)


def main():
    t0 = time.time()
    C = CT.Contracts(8)
    V = C.compute_validity()
    NT = C.build_types()
    out = dict(programs=C.L.n_programs, canon=C.K, classes=C.NC, worlds_free=int(C.worlds0), types=NT,
               valid_pairs=int(V.sum()), own_valid=int(V[np.arange(C.K), C.cls].sum()),
               policy_dups=[[C.cname[c] for c in g] for g in C.policy_dups])
    out['truth_table'] = CT.truth_table_diagnostic(C)
    print('truth table', out['truth_table'], flush=True)
    br = V.sum(0); brmu = (C.mu[:, None] * V).sum(0)
    comp = []
    for c in np.argsort(-brmu):
        srcs = np.nonzero(V[:, c])[0]
        comp.append(dict(contract=C.cname[c], id=int(c), n_valid=int(br[c]), mu_valid=float(brmu[c]),
                         mu_own_class=float(C.mu[C.cls == c].sum()), self_coop=int(C.S[c, c]),
                         n_coop_with=int(C.S[c].sum()), sources=[C.names[p] for p in srcs[np.argsort(-C.mu[srcs])][:12]]))
    out['compatibility'] = comp
    out['sources_by_n_valid'] = np.bincount(V.sum(1)).tolist()
    sc = [c for c in range(C.NC) if C.S[c, c] == 1]
    out['selfcoop_contracts'] = len(sc)
    out['breadth_rank_selfcoop'] = [(C.cname[c], int(br[c]), float(brmu[c])) for c in sorted(sc, key=lambda c: (-br[c], -brmu[c]))[:20]]
    tags = [c for c in range(C.NC) if C.S[c, c] == 1 and C.S[c].sum() == 1]
    out['tags'] = [(C.cname[c], int(br[c]), float(brmu[c])) for c in tags]
    pay = np.asarray(PD, float)
    save = dict(tsrc=C.tsrc, tcon=C.tcon, mu=C.mu, cls=C.cls, S=C.S, valid=V, rep=C.rep, k=C.k, cs_type=C.cs_type)
    out['gate'] = {}
    K = C.K
    for b in BS:
        t = time.time()
        val, info, aux = C.evaluate(b)
        a = CT.audit(C, val, aux)
        bl = 'inf' if b >= CT.INF else str(b)
        save['val_' + bl] = val
        save['mask_' + bl] = aux[3]
        named = (CT.FB, CT.PB, CT.PSTAR, 'BOX1(THEM(ME))', 'BOX(THEM(THEM))')
        sc_nc = {nm: int(val[C.names.index(nm), C.names.index(nm)]) for nm in named}
        free_sc = np.nonzero(np.diag(C.val0) == 1)[0]
        nc_sc = [p for p in free_sc if val[p, p] == 1]
        iF = C.names.index(CT.FB); tF = int(C.cs_type[iF])
        out['gate'][bl] = dict(info=info, audit=a, time_s=time.time() - t,
                               masked_noncarrier_pairs=int((aux[3][:K, :K] == 0).sum()),
                               selfcoop_noncarrier=sc_nc, n_free_selfcoop=len(free_sc), n_selfcoop_noncarrier=len(nc_sc),
                               mu_free_selfcoop=float(C.mu[free_sc].sum()), mu_selfcoop_noncarrier=float(C.mu[nc_sc].sum()),
                               fb_nc_vs_fb_carrier=int(val[iF, tF]), fb_carrier_vs_fb_nc=int(val[tF, iF]),
                               noncarrier_equals_free=int((val[:K, :K] == C.val0).all()) if b >= CT.INF else None)
        print(bl, info, a, '%.0fs' % (time.time() - t), flush=True)
    np.savez_compressed(os.path.join(ROOT, 'runs', 'contracts_types.npz'), **save)
    out['names'] = C.names; out['cname'] = C.cname
    json.dump(out, open(os.path.join(ROOT, 'runs', 'contracts_static.json'), 'w'), indent=1)
    print('done %.0fs' % (time.time() - t0))


if __name__ == '__main__':
    main()
