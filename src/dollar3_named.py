"""Exit decomposition, neutral bridges and N-scaling for named efficient
triples (constant grand coalition, constant fair pair, constant unfair pair),
in every arm, plus the static invasion table by slot.

    python3 src/dollar3_named.py
Writes runs/dollar3/named.json.
"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import json, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import dollar3 as D
from dollar3_run import build_chain, bridge_analysis, exits_of, ROOT

NAMED = {'grand (ALL,1/3)^3': [(D.ALL, 0), (D.ALL, 0), (D.ALL, 0)],
         'fair pair 12, slot 3 (ALL,1/3)': [(1, 1), (0, 1), (D.ALL, 0)],
         'unfair pair 12 (2/3 to slot 1), slot 3 (ALL,1/3)': [(1, 2), (0, 0), (D.ALL, 0)]}


def invasion_table(ch, code):
    ex, u0, t0 = exits_of(ch, code)
    tab = []
    for s in range(3):
        rows = [e for e in ex if e['slot'] == s]
        agg = {}
        for e in rows:
            a = agg.setdefault(e['kind'], dict(mass=0.0, prob=0.0, n=0))
            a['mass'] += e['mass']; a['prob'] += e['prob']; a['n'] += 1
        strict = sorted([e for e in rows if e['kind'] == 'strict'], key=lambda e: -e['prob'])[:3]
        nchg = sorted([e for e in rows if e['kind'] == 'neutral-change'], key=lambda e: -e['prob'])[:2]
        tab.append(dict(slot=s + 1, by_kind=agg,
                        top_strict=[dict(prog=ch.S.src(s, ch.reps[s, e['cls']]), du=e['du'], rho=e['rho'], mass=e['mass'], pay=(e['pay'] / 6).round(3).tolist()) for e in strict],
                        top_neutral_change=[dict(prog=ch.S.src(s, ch.reps[s, e['cls']]), mass=e['mass'], pay=(e['pay'] / 6).round(3).tolist()) for e in nchg]))
    return tab


def main():
    out = {}
    for arm in ('constants', 'weak', 'modalPA', 'modal'):
        for N in (100, 1000, 10000):
            ch, S = build_chain(arm, N, 0.3, 1e-9, 10)
            for name, acts in NAMED.items():
                cl = [ch.const_class[s][D.local_of(s, p, d)] for s, (p, d) in enumerate(acts)]
                code = ch.code(*cl)
                ba = bridge_analysis(ch, code, examples=(N == 100))
                rec = dict(arm=arm, N=N, state=' | '.join(S.src(s, ch.reps[s, cl[s]]) for s in range(3)), **ba)
                if N == 100:
                    rec['invasion_table'] = invasion_table(ch, code)
                out['%s|%d|%s' % (arm, N, name)] = rec
                print(arm, N, name, {k: '%.2e' % v for k, v in ba['exit_rates'].items()}, 'bridge mass %.2e n %d closed %s' % (ba['bridge_mass'], ba['n_bridges'], ba['drift_closed_depth2']), flush=True)
    json.dump(out, open(os.path.join(ROOT, 'runs', 'dollar3', 'named.json'), 'w'), indent=1, default=float)


if __name__ == '__main__':
    main()
