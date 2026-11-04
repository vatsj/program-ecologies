"""Invasion assays along N (spec cell F; notes/pair-worth-n.md 1.5).  python3 src/pair_worth_n_assay.py

Single island, no migration, no tail.  Residents: B*(2,2,2; c = own grand action)^3 and the grand constants (ALL, 2)^3 (equal
split, G1/3).  One individual is introduced into slot s (each s in 0..2): a matching grand constant, a pair offer (a constant
naming each of the two other slots at the exclusion split (1, 1)), B*(sigma'; c = own grand action) on another core split
(sigma' = (3,2,1) rotated so that slot s has share 3).  On G^3 the 'matching grand constant' is the resident program itself
(identity check) and a reading entrant B*(2,2,2) is added.  Fixation probability: 2,000 Monte-Carlo replicates of the kernel's
Moran step (frequency-independent invader, the other two slots monomorphic) and the exact two-type value."""
import json, math, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pair_worth as PW
import pair_worth_assay as PA

OUTP = os.path.join(PW.ROOT, 'runs', 'pair_worth_n')
G = PW.get_game('pw13')
W = 0.3
NS = (100, 200, 400)
REPS = 2000


def A(s, partner, d):
    return G.act(s, PW.ALL if partner == 'ALL' else partner, d)


def rot(sig, s):
    """rotate (3, 2, 1) so that slot s has share 3: slot 0 (3,2,1), slot 1 (1,3,2), slot 2 (2,1,3)."""
    return [(3, 2, 1), (1, 3, 2), (2, 1, 3)][s]


def cases():
    eq = (2, 2, 2)
    out = []
    for res_name in ('B*^3', 'G^3'):
        if res_name == 'B*^3':
            res = [PW.program(G, 'B', s, eq, A(s, 'ALL', 2)) for s in range(3)]
        else:
            res = [PW.const_program(A(s, 'ALL', 2)) for s in range(3)]
        for s in range(3):
            inv = {}
            inv['matching grand constant' if res_name == 'B*^3' else 'identical grand constant (identity check)'] = PW.const_program(A(s, 'ALL', 2))
            if res_name == 'G^3':
                inv['reading entrant B*(equal split)'] = PW.program(G, 'B', s, eq, A(s, 'ALL', 2))
            for p in PW.others(s):
                inv['pair offer to slot %d' % p] = PW.const_program(A(s, p, 1))
            sg = rot(None, s)
            inv['B*(sigma\') on another core split %s' % (sg,)] = PW.program(G, 'B', s, sg, A(s, 'ALL', sg[s]))
            for nm, prog in inv.items():
                out.append((res_name, s, nm, res, prog))
    return out


def main():
    os.makedirs(OUTP, exist_ok=True)
    res = dict(reps=REPS, w=W, rows=[])
    cs = cases()
    seed = 91000          # fresh Monte-Carlo seeds: a smoke run with seed 7300 was discarded before the predictions were committed
    for N in NS:
        for (rn, s, nm, residents, inv) in cs:
            seed += 1
            ures_vec, ores = PA.payoffs(G, residents)
            invl = list(residents); invl[s] = inv
            uinv_vec, oinv = PA.payoffs(G, invl)
            ur, ui = ures_vec[s], uinv_vec[s]
            fx = PA.fix_mc(N, W, ur, ui, REPS, seed)
            pex = PA.fix_exact(N, W, ur, ui)
            p0 = 1.0 / N
            sd0 = math.sqrt(REPS * p0 * (1 - p0))
            res['rows'].append(dict(N=N, resident=rn, slot=s, invader=nm, u_resident=round(ur, 5), u_invader=round(ui, 5),
                                    fixed=int(fx), p_mc=fx / REPS, Np_mc=fx / REPS * N, p_exact=pex, Np_exact=pex * N,
                                    neutral=bool(abs(ur - ui) < 1e-12), z_vs_neutral=(fx - REPS * p0) / sd0,
                                    outcome_resident=str(ores), outcome_invader=str(oinv)))
    json.dump(res, open(os.path.join(OUTP, 'assays.json'), 'w'), indent=1)
    for N in NS:
        print('N =', N)
        for r in res['rows']:
            if r['N'] == N:
                print('  %-5s slot %d %-50s u %.3f -> %.3f  N*p MC %.2f exact %.3f  z(neutral) %+.2f' % (
                    r['resident'], r['slot'], r['invader'], r['u_resident'], r['u_invader'], r['Np_mc'], r['Np_exact'], r['z_vs_neutral']))


if __name__ == '__main__':
    main()
