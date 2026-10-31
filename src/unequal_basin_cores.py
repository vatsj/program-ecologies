"""Cores for the core-restricted m = 2 / 3 objects: sets of conditionals (per slot, S3-closed) that are allowed to appear two or
three at a time in an island.  Built from syntactic families and from the donors of saved endpoint states."""
import os, sys, json
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import unequal_basin as UB
import unequal_basin_run as R
import unequal_basin_jobs as J


def close(arm, core):
    """S3-close a core given as per-slot sets."""
    out = [set(c) for c in core]
    for sg, perm in UB.perm_maps(arm):
        for s in range(3):
            for x in core[s]:
                out[sg[s]].add(int(perm[s][x]))
    return out


def core_from(arm, families=(), endpoints=(), qmin=1e-6):
    """families: names for family_mask; endpoints: (obj, x) pairs whose conditional donors with q >= qmin join the core."""
    core = [set() for _ in range(3)]
    for nm in families:
        m = R.family_mask(arm, nm)
        for s in range(3):
            core[s] |= set(int(v) for v in np.nonzero(m[s])[0])
    for obj, x in endpoints:
        q = obj.marg(x)
        for s in range(3):
            for y in np.nonzero(q[s] >= qmin)[0]:
                if not obj.isc[y]:
                    core[s].add(int(y))
    return close(arm, core)
