"""Supplementary b = 0 gate (predictions addendum): only constants are legible from source.

    python3 src/contracts_static_b0.py
Writes runs/contracts_types_b0.npz and runs/contracts_static_b0.json.
"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import contracts as CT

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    C = CT.Contracts(8); C.compute_validity(); C.build_types()
    K = C.K
    t = time.time()
    val, info, aux = C.evaluate(0)
    a = CT.audit(C, val, aux)
    free_sc = np.nonzero(np.diag(C.val0) == 1)[0]
    nc_sc = [p for p in free_sc if val[p, p] == 1]
    named = (CT.FB, CT.PB, CT.PSTAR, 'BOX1(THEM(ME))', 'BOX(THEM(THEM))')
    iF = C.names.index(CT.FB); tF = int(C.cs_type[iF])
    out = dict(info=info, audit=a, time_s=time.time() - t, masked_noncarrier_pairs=int((aux[3][:K, :K] == 0).sum()),
               masked_mu_share=float(C.mu @ (1 - aux[3][:K, :K]) @ C.mu),
               selfcoop_noncarrier={nm: int(val[C.names.index(nm), C.names.index(nm)]) for nm in named},
               n_free_selfcoop=len(free_sc), n_selfcoop_noncarrier=len(nc_sc), mu_free_selfcoop=float(C.mu[free_sc].sum()),
               mu_selfcoop_noncarrier=float(C.mu[nc_sc].sum()), fb_nc_vs_fb_carrier=int(val[iF, tF]), fb_carrier_vs_fb_nc=int(val[tF, iF]),
               top_selfcoop_noncarrier=[(C.names[p], float(C.mu[p])) for p in sorted(nc_sc, key=lambda p: -C.mu[p])[:10]])
    np.savez_compressed(os.path.join(ROOT, 'runs', 'contracts_types_b0.npz'), val_0=val, mask_0=aux[3])
    json.dump(out, open(os.path.join(ROOT, 'runs', 'contracts_static_b0.json'), 'w'), indent=1)
    print(out)


if __name__ == '__main__':
    main()
