"""Where the arm-T table (P_fail = 0) and the DSL readers arm R's table (churn_primary 'Emin-main-m', modalPA evaluator, and
'Emin-main-w', weak evaluator) differ, triple by triple, on reader-constant and reader-reader triples.  A description only:
fuel decides whether the fallback runs, so a difference is not attributed to the timeout action (spec, second review).

T programs with a DSL counterpart: the nine constants; the single readers S?o?? (DSL Sj / Sk: accept the partner's half offer,
else name the other) and S?z?? (Zj / Zk: null fallback); the two-partner readers D?f?? (R2 .f) and D?z?? (R2 .z); the exploiting
readers have none.  The y / n timeout flag of T has no DSL counterpart: each T variant is compared with the same DSL class.
"""
import os, sys
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dollar3 as D
import churn_primary as CP
import many_islands_t as M
from many_islands_t_common import tabs

NP = M.NP


def dsl_class(cat, T, s, i):
    """class index in the DSL catalogue of arm-T program i placed in slot s, or None."""
    nm = T.names[i]
    fam = T.fam[i]
    nxt = (s + 1) % 3; prv = (s - 1) % 3
    j = D.others(s)[0]
    if fam == 'const':
        code = i
        pc, d = code // 3, code % 3
        ab = nxt if pc == 0 else prv if pc == 1 else D.ALL
        loc = D.local_of(s, ab, d)
        form = D.Lang._reduce([], [loc])
        return cat.S.index[s].get(form)
    if fam == 'single':
        t = nxt if nm[1] == 'n' else prv
        key = ('S' if nm[2] == 'o' else 'Z') + ('j' if t == j else 'k')
        return cat.idx[(s, key)]
    if fam == 'two':
        t = nxt if nm[1] == 'n' else prv
        key = 'R2' + ('j' if t == j else 'k') + nm[2]
        return cat.idx[(s, key)]
    return None


def compare(spec):
    T = tabs()
    cat = CP.get_cat(spec)
    prog = [i for i in range(NP) if T.fam[i] != 'exploit']
    cls = {(s, i): dsl_class(cat, T, s, i) for s in range(3) for i in prog}
    ok = all(v is not None for v in cls.values())
    U = [np.array(sorted(set(cls[(s, i)] for i in prog)), np.int64) for s in range(3)]
    J, PAY, VEC = cat.make_J(U, 0.0)
    pos = [{int(c): k for k, c in enumerate(U[s])} for s in range(3)]
    isr = T.is_reader
    res = {}
    kinds = {'1 reader + 2 constants': 1, '2 readers + 1 constant': 2, '3 readers': 3}
    stats = {k: dict(n=0, differ=0, class_differ=0, by_flag={}, examples=[]) for k in kinds}
    for a, b, c in itertools.product(prog, repeat=3):
        nread = int(isr[a]) + int(isr[b]) + int(isr[c])
        if nread == 0:
            continue
        key = [k for k, v in kinds.items() if v == nread][0]
        o_t = int(T.OUT[a, b, c])
        code = int(J[pos[0][cls[(0, a)]], pos[1][cls[(1, b)]], pos[2][cls[(2, c)]]])
        o_d = int(VEC[code])
        st = stats[key]
        st['n'] += 1
        if o_t != o_d:
            st['differ'] += 1
            if M.CATMAP[o_t] != M.CATMAP[o_d]:
                st['class_differ'] += 1
            flags = ''.join(sorted(set(T.names[x][-1] for x in (a, b, c) if isr[x])))
            st['by_flag'][flags] = st['by_flag'].get(flags, 0) + 1
            if len(st['examples']) < 6 and nread >= 2:
                st['examples'].append((T.names[a], T.names[b], T.names[c], M.MI.OLAB[o_t], M.MI.OLAB[o_d]))
    return dict(spec=spec, all_mapped=bool(ok), stats=stats)


def run():
    return dict(name='dslcmp', modal=compare('Emin-main-m'), weak=compare('Emin-main-w'), **{'pass': True})
