"""Static check of the exact simulators at nearby fuel budgets (notes 1.3, "recursive reader pairs at nearby budgets"): the play law and
the failure events of SIMX, SIMX_I and SIMX_E against a spread of opponents (and against each other) at K in {9000, 10000, 11000}.  One
process.  Output: runs/forfeit_pricing/static_K.json.

    python3 src/forfeit_pricing_static.py [K ...]
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lt_tape as T
import lt_tape_games as G
import forfeit_pricing as FP

OUT = FP.OUT
RPS_OPP = ['R0', 'U', 'B_RP', 'H0', 'SIM20R', 'SIM100u', 'PRR', 'CRR', 'PB']
INSP0_OPP = ['C0', 'K0', 'Mc4', 'HE0', 'SE20k', 'SE100c', 'PE', 'CR3', 'PR3', 'PCR3']       # inspectees played by SIMX_I
INSP1_OPP = ['I0', 'N0', 'M4', 'CARR3', 'HI0', 'SI20n', 'SI100i', 'RI', 'RIM']                  # inspectors played by SIMX_E


def row(eng, led, x, y):
    d = eng.dist(x, y); e = led.ledger(x, y)
    ex = FP.x_expectations(e)
    return dict(dist={k: float(v) for k, v in d['dist'].items()}, steps=float(d['steps']), forf=ex['forf'], n_to=ex['n_to'], n_uto=ex['n_uto'],
                ev_A=ex['ev_A'], ev_Af=ex['ev_Af'], unc_fin=ex['unc_fin'], unc_tape=ex['unc_tape'])


def run_K(K):
    out = dict(K=K, rps={}, insp0={}, insp1={})
    cat = G.catalogue_rps(K, 3)[0]
    terms = {t.name: t.build('tape') for t in cat}
    prover = T.TProver(3, limit=3 * max(K, 20000))
    eng = T.Engine(prover, K=K, r=3, m=3); led = FP.LedgerEngineX(prover, K, 3, 3)
    simx = FP.simx_rps(K)
    for nm in RPS_OPP:
        out['rps'][nm] = dict(x=row(eng, led, simx, terms[nm]), y=row(eng, led, terms[nm], simx))
    t = time.time()
    out['rps']['SIMX'] = dict(x=row(eng, led, simx, simx), y=None, wall=time.time() - t)
    ins, ee = G.catalogue_insp(K, 3)
    t0 = {t_.name: t_.build('tape') for t_ in ins}; t1 = {t_.name: t_.build('tape') for t_ in ee}
    prover2 = T.TProver(2, limit=3 * max(K, 20000))
    eng2 = T.Engine(prover2, K=K, r=2, m=3); led2 = FP.LedgerEngineX(prover2, K, 2, 3)
    xi, xe = FP.simx_insp_I(K), FP.simx_insp_E(K)
    for nm in INSP0_OPP:
        out['insp0'][nm] = dict(x=row(eng2, led2, xi, t1[nm]), y=row(eng2, led2, t1[nm], xi))
    for nm in INSP1_OPP:
        out['insp1'][nm] = dict(x=row(eng2, led2, xe, t0[nm]), y=row(eng2, led2, t0[nm], xe))
    t = time.time()
    out['insp0']['SIMX_E'] = dict(x=row(eng2, led2, xi, xe), y=row(eng2, led2, xe, xi), wall=time.time() - t)
    return out


def main(argv):
    Ks = [int(a) for a in argv] or [9000, 10000, 11000]
    path = os.path.join(OUT, 'static_K.json')
    res = json.load(open(path)) if os.path.exists(path) else {}
    for K in Ks:
        if str(K) in res: continue
        t = time.time()
        res[str(K)] = run_K(K)
        print('K', K, 'wall %.0fs' % (time.time() - t), flush=True)
        json.dump(res, open(path, 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1:])
