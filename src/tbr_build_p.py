"""Queue 81: build arm P's class data (cache/spoiler-n{6,9,12}.npz) with the installed numba.

spoiler_conditioned.build_main calls moat_static_big._traces and seeds_tail's hashing kernels, which are compiled with
parallel=True; numba 0.68 (the only one available for Python 3.13 here; the repo pins 0.57) fails in its parfor pass
on _traces ("unexpected cycle in lookup()").  This driver recompiles the same Python functions with parallel=False
(prange runs as range) and then calls build_main unchanged.  In _traces's parallel loop each thread writes only bit 6
of T[x, y] and reads only bits 0-5, so the serial order computes the identical table.  build_main itself checks the
n = 6 and 9 blocks against seeds_in_n.data.

    python3 src/tbr_build_p.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from numba import njit
import moat_static_big as MB
import seeds_tail as ST


def _serial(mod, name):
    f = getattr(mod, name)
    if hasattr(f, 'py_func'):
        setattr(mod, name, njit(cache=False)(f.py_func))


for _n in ('_traces', '_to_stable'):
    _serial(MB, _n)
for _n in [k for k in dir(MB) if k.startswith('_')]:
    f = getattr(MB, _n)
    if hasattr(f, 'targetoptions') and f.targetoptions.get('parallel'):
        _serial(MB, _n)
for _n in [k for k in dir(ST) if k.startswith('_')]:
    f = getattr(ST, _n)
    if hasattr(f, 'targetoptions') and f.targetoptions.get('parallel'):
        _serial(ST, _n)

if __name__ == '__main__':
    import spoiler_conditioned as SC

    class A:
        procs = 1
    SC.build_main(A())
