"""Is the net flow between fair pairs a flow toward the larger pair?  For each post-anneal pool the exact class kernel gives the
antisymmetric net flows D_ab; compare their signs with the share differences (x_b - x_a); and on the exactly S3-symmetrized pool
the flows are zero by construction (a check).  Writes runs/many_islands/feedback.json.   python3 src/many_islands_feedback.py"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import many_islands as MI
import many_islands_run as MR
import many_islands_analysis as MA


def run():
    out = {}
    for arm_name in ('L', 'M', 'R'):
        for A in (0, 150):
            if not MR.existing_pools(arm_name, A):
                continue
            arm = MI.Arm(arm_name); arm.new_cache(24)
            rng = np.random.default_rng(1)
            xs = []; ds = []
            for k in MR.existing_pools(arm_name, A):
                tr, _ = MR.load_pool(arm_name, A, k)
                K, npair, x, oc, osl, o = MA.exact_class_kernel(arm, tr, rng)
                flow, D = MA.fair_block(K, x)
                xs.append([x[v] for v in MI.V]); ds.append([D[0, 1], D[0, 2], D[1, 2]])
            xs = np.array(xs); ds = np.array(ds)
            dx = np.stack([xs[:, 1] - xs[:, 0], xs[:, 2] - xs[:, 0], xs[:, 2] - xs[:, 1]], axis=1)      # x_b - x_a for (0,1), (0,2), (1,2)
            agree = int((np.sign(ds) == np.sign(dx)).sum())
            corr = float(np.corrcoef(ds.reshape(-1), dx.reshape(-1))[0, 1])
            # exactly symmetrized pool 0
            tr0, _ = MR.load_pool(arm_name, A, MR.existing_pools(arm_name, A)[0])
            sym = MR.symmetrize(arm, tr0)
            K, npair, x, oc, osl, o = MA.exact_class_kernel(arm, sym, rng, per_class=3000)
            flow, D = MA.fair_block(K, x)
            out['%s A=%d' % (arm_name, A)] = dict(pools=len(xs), sign_agreement=[agree, int(ds.size)], corr=corr,
                                                  D_over_dx=[float(a / b) if b else None for a, b in zip(ds.reshape(-1), dx.reshape(-1))],
                                                  sym_D=[float(D[0, 1]), float(D[0, 2]), float(D[1, 2])], sym_flow=float(flow[~np.eye(3, dtype=bool)].mean()))
            print(arm_name, A, out['%s A=%d' % (arm_name, A)], flush=True)
    with open(os.path.join(MR.OUT, 'feedback.json'), 'w') as f:
        json.dump(out, f)


if __name__ == '__main__':
    run()
