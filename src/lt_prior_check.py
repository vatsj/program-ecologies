"""The sampled-interaction check of queue 75 (step 1): a program's assigned family (by the 29 x 29 library probe table) must
reproduce its interactions with other sampled programs, else it is reported as `other`.

Set A: 1,000 non-junk programs drawn from the prior (machine R0 / R1).  Set B: the spelled reader / bully / exploiter
programs of the targeted search (one example per class, size and form).  Partners: the programs of set A.  For each program,
`npairs` random partner pairs (b, c) are run (code, failed reads, forfeit) against the program, and against its family's
references: a constant `const:k` must output k with no charge; an exact member must equal the member's own run on the same
pair; a family-level class is reproduced if some member of the family matches on all pairs.

    python3 src/lt_prior_check.py R0 OUT.json [SEARCH.json] [NPAIRS]
"""
import os, sys, json, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import lt_code as L
import lt_prior as P
import lt_prior_enum as E


def tuplify(t):
    return tuple(tuplify(x) if isinstance(x, list) else x for x in t)


def run3(prog, b, c):
    cd, nt, f, st, raw, _ = P.eval_prog(prog, b, c)
    return (cd, min(nt, 100), f)


def check(mach, seed=7, nA=1000, npairs=40, search=None):
    pr = P.probes()
    sm = E.Sampler(mach, seed)
    rng = random.Random(seed + 1)
    A = []
    tries = 0
    t0 = time.time()
    while len(A) < nA and tries < 20000000:
        tries += 1
        t, sz = sm.draw()
        if t is None:
            continue
        body = E.scope_fix(t)
        fam, exact, _ = P.classify_body(body, mach, pr)
        if P.group_of(fam) in ('junk_f', 'junk_r'):
            continue
        A.append((body, fam, exact))
        if len(A) % 200 == 0:
            L._compiled.clear()
    partners = [P.frame(P.expand(b)) for b, _, _ in A]
    members = pr.mterm
    mfam = pr.mfam

    def pairs():
        return [(rng.randrange(len(partners)), rng.randrange(len(partners))) for _ in range(npairs)]

    def evaluate_set(items, label):
        res = dict(total=0, reproduced=0, other=0, by_group={}, by_kind={}, examples_other=[])
        for body, fam, exact in items:
            g = P.group_of(fam)
            prog = P.frame(P.expand(body))
            pp = pairs()
            got = [run3(prog, partners[i], partners[j]) for i, j in pp]
            ok = False
            kind = 'exact' if exact else 'family'
            if fam.startswith('const:') and not exact:
                k = int(fam.split(':')[1])
                ok = all(x == (k, 0, 0) for x in got)
            elif exact:
                mi = pr.members.index(exact)
                ok = all(run3(members[mi], partners[i], partners[j]) == x for (i, j), x in zip(pp, got))
            elif g in ('single', 'two', 'bully', 'exploit', 'yielder'):
                ok = False
                for mi, mf in enumerate(mfam):
                    nm = pr.members[mi]
                    if (g == 'single' and mf == 'single') or (g == 'two' and mf == 'two') or (g == 'bully' and mf == 'bully') \
                            or (g == 'exploit' and mf == 'exploit'):
                        if all(run3(members[mi], partners[i], partners[j]) == x for (i, j), x in zip(pp, got)):
                            ok = True; break
            else:
                ok = None       # not an assigned reader family (other_cond, const_read, yielder): no reference
            if ok is None:
                continue
            res['total'] += 1
            res['reproduced'] += int(ok); res['other'] += int(not ok)
            bg = res['by_group'].setdefault(g + '/' + kind, [0, 0]); bg[0] += 1; bg[1] += int(ok)
            if not ok and len(res['examples_other']) < 8:
                res['examples_other'].append([P.to_sexpr(body), fam, exact])
        return res
    resA = evaluate_set(A, 'A')
    resA['n_programs'] = len(A); resA['tries'] = tries
    resA['assigned_groups'] = {}
    for _, fam, ex in A:
        g = P.group_of(fam)
        resA['assigned_groups'][g] = resA['assigned_groups'].get(g, 0) + 1
    out = dict(machine=mach.name, npairs=npairs, setA=resA, wall=time.time() - t0)
    if search:
        B = []
        for k, szd in search['classes'].items():
            fam, ex = k.split('|')
            if P.group_of(fam) in ('single', 'two', 'bully', 'exploit'):
                for s, forms in szd.items():
                    for form, v in forms.items():
                        if len(v) > 3 and v[3]:
                            B.append((tuplify(v[3]), fam, ex))
        rng.shuffle(B)
        resB = evaluate_set(B[:600], 'B')
        resB['n_programs'] = min(600, len(B)); resB['candidates'] = len(B)
        out['setB'] = resB
    return out


if __name__ == '__main__':
    mach = P.MACHINES[sys.argv[1]]
    outp = sys.argv[2]
    npairs = int(sys.argv[4]) if len(sys.argv) > 4 else 40
    search = json.load(open(sys.argv[3])) if len(sys.argv) > 3 and sys.argv[3] != '-' else None
    res = L.run_big(check, mach, 7, 1000, npairs, search)
    json.dump(res, open(outp, 'w'), indent=1, default=str)
    print(json.dumps(res['setA'], indent=1, default=str)[:3000])
