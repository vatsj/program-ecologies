"""Follower-value core and its intersection with the leader-value core, from the stored existence sweep
(predictions/2026-11-15-follower-core.md).  v_F(S) = v(S) - FMA(S); 'both' uses max(v, v_F) on proper coalitions."""
import json, sys, os, ast
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from core_sweep import tu_core, proper, full, TOL

def mask(key):
    return sum(1 << i for i in ast.literal_eval(key))

def three(rec, n):
    v = {mask(k): x for k, x in rec['v'].items()}
    fma = {mask(k): x for k, x in rec['fma'].items()}
    if set(fma) != set(proper(n)):
        return None
    F = full(n)
    vf = {S: v[S] - fma[S] for S in fma}; vf[F] = v[F]
    vb = {S: max(v[S], vf[S]) for S in fma}; vb[F] = v[F]
    sc = max(abs(v[F]), 1.0)
    pos = any(x > TOL * sc for x in fma.values()); neg = any(x < -TOL * sc for x in fma.values())
    sign = 'mixed' if pos and neg else 'lead' if pos else 'follow' if neg else 'none'
    return dict(leader=tu_core(v, n)['verdict'], follower=tu_core(vf, n)['verdict'], both=tu_core(vb, n)['verdict'],
                sign=sign)

def main():
    d = json.load(open('runs/core-existence-sweep.json'))
    out = {}
    for fam, recs in d.items():
        if fam == 'catalogue':
            out[fam] = {}
            for g, r in recs.items():
                n = max(len(ast.literal_eval(k)) for k in r['pess']['v'])
                out[fam][g] = {sel: three(r[sel], n) for sel in ('pess', 'opt')}
            continue
        c = Counter(); skipped = 0
        for r in recs:
            t = three(r, r['n'])
            if t is None:
                skipped += 1; continue
            c[(t['sign'], t['leader'], t['follower'], t['both'])] += 1
        out[fam] = dict(skipped=skipped, table=[[*k, n] for k, n in sorted(c.items())])
    json.dump(out, open('runs/follower-core.json', 'w'), indent=1)
    for fam, o in out.items():
        print(fam, json.dumps(o))

if __name__ == '__main__':
    main()
