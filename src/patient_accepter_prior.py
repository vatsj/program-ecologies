"""Step 1 of queue 78 (spec specs/2026-11-14-patient-accepters.md): the length-prior mass of the patient accepter R under queue 75's
machines R0 and R1, with queue 75 / 76's machinery (lt_prior, lt_prior_search, lt_prior_enum; nothing existing is edited).

The probe set is unchanged (the 27 library programs and the two bullies); the members are the 59 programs of the extended catalogue
(patient_accepter.CataloguePA), so a table equal to an R's is recognised as that R (exact member).  R answers the constants like no
library family (its default is a 1/3 constant, not a fallback of T's readers), so queue 75's family classifier labels it `other_cond`;
the exact-member label is what this step counts.

    python3 src/patient_accepter_prior.py search R0|R1 OUT.json        targeted grammar search (lt_prior_search.search): lower bounds
    python3 src/patient_accepter_prior.py mc R0|R1 N SEED OUT.json S0  Monte Carlo from the prior with the extended members (upper bound)
    python3 src/patient_accepter_prior.py v3 OUT.json                  V3: R's canonical bodies classify as themselves
    python3 src/patient_accepter_prior.py report OUT.json OUT.md       masses, shortest spellings, ratios, MC bounds, the series' law input
"""
import os, sys, json, glob, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import lt_code as L
import lt_prior as P
import lt_prior_search as S
import patient_accepter as PA

OUTD = os.path.join(ROOT, 'runs', 'patient_accepter')


def extend_probes():
    pr = P.probes()
    if getattr(pr, '_pa', False):
        return pr
    cat = PA.CataloguePA()
    pr.members = cat.names; pr.mterm = cat.terms; pr.mfam = cat.fam
    pr.sig2member = {}
    for i, term in enumerate(cat.terms):
        pr.sig2member.setdefault(pr.signature(pr.table(term)), []).append(i)
    L._compiled.clear()
    pr._pa = True
    return pr


def cmd_search(mach_name, out):
    extend_probes()
    mach = P.MACHINES[mach_name]
    t0 = time.time()
    res = L.run_big(S.search, mach)
    json.dump(dict(machine=mach.name, wall=time.time() - t0, classes=S.pack(res)), open(out, 'w'), default=str)
    print('done', mach_name, time.time() - t0)


def cmd_mc(mach_name, n, seed, out, s0):
    import lt_prior_enum as E
    extend_probes()
    mach = P.MACHINES[mach_name]
    t0 = time.time()
    res = L.run_big(E.mc_run, mach, n, seed, s0, True)
    res.update(machine=mach.name, seed=seed, wall=time.time() - t0)
    json.dump(res, open(out, 'w'))


def canonical_bodies():
    """R's bodies in the two machines' syntax (frame lam me. lam n. lam p.; me = v2, n = v1, p = v0 at depth 0)."""
    out = {}
    for nm in PA.NAMES_R:
        d, to = nm[1], nm[2]
        accv, go, dflt = (4, 1, 3) if d == 'n' else (1, 4, 0)
        r = ('v', 0)
        test = ('eq', r, ('nat', accv))
        if to == 'y':
            test = ('if', test, ('con', 'T'), ('eq', r, ('con', 'TO')))
        F = ('if', test, ('nat', go), ('nat', dflt))
        out[(nm, 'R1')] = ('app', ('lam', F), ('readn',) if d == 'n' else ('readp',))
        x, y, z = (('v', 1), ('v', 0), ('v', 2)) if d == 'n' else (('v', 0), ('v', 2), ('v', 1))
        out[(nm, 'R0')] = ('app', ('lam', F), ('capk', ('nat', 400), ('run', ('nat', 400), x, y), z))
    return out


def cmd_v3(out):
    pr = extend_probes()
    res = {}
    for (nm, mach), body in canonical_bodies().items():
        fam, exact, _ = L.run_big(P.classify_body, body, P.MACHINES[mach], pr)
        L._compiled.clear()
        res['%s|%s' % (nm, mach)] = dict(family=fam, exact=exact, ok=(exact == nm), sexpr=P.to_sexpr(body), nodes=P.node_count(body))
    json.dump(res, open(out, 'w'), indent=1)
    print(json.dumps(res, indent=1))


GROUPS = {'Rn': ('Rnn', 'Rpn'), 'Ry': ('Rny', 'Rpy')}


def search_groups(path):
    """{member: [raw mass, min size, example]} from a search output (exact members only)."""
    d = json.load(open(path))
    mem = {}
    for key, szd in d['classes'].items():
        fam, exact = key.split('|')
        if not exact:
            continue
        for s, forms in szd.items():
            for form, v in forms.items():
                m, c, ex = v[0], v[1], v[2]
                e = mem.setdefault(exact, [0.0, None, None, 0])
                e[0] += m; e[3] += c
                if e[1] is None or int(s) < e[1]:
                    e[1] = int(s); e[2] = ex
    return mem, d


def wilson(k, n, z=1.96):
    if n == 0:
        return 0.0, 1.0
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, c - h), min(1.0, c + h)


def cmd_report(out, md):
    old = json.load(open(os.path.join(ROOT, 'runs', 'lt_prior', 'lt-prior.json')))
    step2_76 = json.load(open(os.path.join(ROOT, 'runs', 'bully_resist', 'step2.json')))
    rep = {}
    law = dict(machines=['R0', 'R1'], note='queue 76 step2.json masses (conditional on finite trees; exact-member lower bounds) plus accepter = '
                                          'the exact-member lower bound of the n variants of R from this search')
    for mn in ('R0', 'R1'):
        R = old['machines'][mn]
        q = R['finite_mass_q']
        mem, d = search_groups(os.path.join(OUTD, 'search_%s.json' % mn))
        single = sum(v[0] for k, v in mem.items() if k[0] == 'S' and k[2] in 'oz')
        bully = sum(v[0] for k, v in mem.items() if k in ('Bn', 'Bp'))
        rn = sum(mem.get(k, [0.0])[0] for k in GROUPS['Rn']); ry = sum(mem.get(k, [0.0])[0] for k in GROUPS['Ry'])
        c3 = R['const_by_code_cond'][3] * q; c0 = R['const_by_code_cond'][0] * q
        sh_single = min(v[1] for k, v in mem.items() if k[0] == 'S' and k[2] in 'oz' and v[1] is not None)
        sh_bully = min(v[1] for k, v in mem.items() if k in ('Bn', 'Bp'))
        rec = dict(q=q, single_raw_this_search=single, bully_raw_this_search=bully,
                   single_raw_q75=R['combined']['single']['lower_bound_exact_raw'], bully_raw_q75=R['combined']['bully']['lower_bound_exact_raw'],
                   R_n_raw=rn, R_y_raw=ry, R_n_cond=rn / q, R_y_cond=ry / q,
                   members={k: dict(raw=mem[k][0], cond=mem[k][0] / q, min_size=mem[k][1], example=mem[k][2], spellings=mem[k][3]) for k in PA.NAMES_R if k in mem},
                   shortest_R_n=min([mem[k][1] for k in GROUPS['Rn'] if k in mem] or [None]),
                   shortest_R_y=min([mem[k][1] for k in GROUPS['Ry'] if k in mem] or [None]),
                   shortest_single=sh_single, shortest_bully=sh_bully,
                   ratio_Rn_to_single=rn / single if single else None, ratio_Rn_to_bully=rn / bully if bully else None,
                   ratio_Rn_to_C13=rn / (c3 + c0), C3_raw=c3, C0_raw=c0)
        # Monte Carlo upper bound (this queue's draws with the extended members)
        mcs = sorted(glob.glob(os.path.join(OUTD, 'mc*', 'mc_%s_*.json' % mn)))
        if mcs:
            n = 0; hits = {k: 0 for k in PA.NAMES_R}; lost = 0
            for f in mcs:
                m = json.load(open(f))
                n += m['n'] - m['lost']; lost += m['lost']
                for key, v in m['counts'].items():
                    ex = key.split('|')[1] if '|' in key else ''
                    if ex in hits:
                        hits[ex] += v[0] if isinstance(v, list) else v
            kn = hits['Rnn'] + hits['Rpn']; ky = hits['Rny'] + hits['Rpy']
            # counts are over finite draws: the bound is conditional on a finite tree
            rec['mc'] = dict(files=len(mcs), finite_draws=n, hits=hits, upper_cond_Rn=wilson(kn, n)[1], upper_cond_Ry=wilson(ky, n)[1])
        rep[mn] = rec
        s = dict(step2_76[mn])
        s['accepter'] = rn / q
        law[mn] = s
    json.dump(rep, open(out, 'w'), indent=1, default=str)
    json.dump(law, open(os.path.join(OUTD, 'step1_law.json'), 'w'), indent=1)
    Lx = ['## Step 1: length-prior mass of R (conditional on finite trees; exact-member lower bounds from the grammar search)', '',
          '| machine | R (n variants) | R (y variants) | fair single (this search / q75) | bully (this search / q75) | 1/3 constants C3 + C0 | R_n / single | R_n / bully | R_n / (C3 + C0) | shortest R_n / R_y / single / bully | MC 95% upper (R_n) |',
          '|---|---|---|---|---|---|---|---|---|---|---|']
    for mn, r in rep.items():
        q = r['q']
        Lx.append('| %s | %.3g | %.3g | %.3g / %.3g | %.3g / %.3g | %.3g | %.3g | %.3g | %.3g | %s / %s / %s / %s | %s |' % (
            mn, r['R_n_cond'], r['R_y_cond'], r['single_raw_this_search'] / q, r['single_raw_q75'] / q, r['bully_raw_this_search'] / q, r['bully_raw_q75'] / q,
            (r['C3_raw'] + r['C0_raw']) / q, r['ratio_Rn_to_single'], r['ratio_Rn_to_bully'], r['ratio_Rn_to_C13'],
            r['shortest_R_n'], r['shortest_R_y'], r['shortest_single'], r['shortest_bully'],
            ('%.3g (%d finite draws, hits %s)' % (r['mc']['upper_cond_Rn'], r['mc']['finite_draws'], r['mc']['hits'])) if 'mc' in r else '-'))
    Lx.append('')
    for mn, r in rep.items():
        for k, v in r['members'].items():
            Lx.append('- %s %s: %.3g (cond), shortest %s nodes: `%s` (%d spellings counted)' % (mn, k, v['cond'], v['min_size'], v['example'], v['spellings']))
    open(md, 'w').write('\n'.join(Lx) + '\n')
    print('\n'.join(Lx))


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'search':
        cmd_search(sys.argv[2], sys.argv[3])
    elif c == 'mc':
        cmd_mc(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], int(sys.argv[6]))
    elif c == 'v3':
        cmd_v3(sys.argv[2])
    elif c == 'report':
        cmd_report(sys.argv[2], sys.argv[3])
