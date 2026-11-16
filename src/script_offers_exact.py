"""Queue 80: exactness of the closure regress key (script_offers.do_capk_keyed).

(1) Old fuel: queue 78's 59-program tables at (KR, KS) = (1,200, 400) rebuilt with the key on must equal the stored tables
    (runs/_cache/pa_*.npz, built by patient_accepter without it) in code, steps, failed reads and forfeits.
(2) New fuel: a stratified sample of profiles of world S at (KR', cap') evaluated with the key on and off must agree exactly.

    python3 src/script_offers_exact.py OUT.json [nsample]
"""
import os, sys, json, glob, time, random
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import lt_code as L
import tplus as TP
import script_offers as S
import script_offers_cat as SC


def old_fuel():
    import patient_accepter as PA
    path = glob.glob(os.path.join(ROOT, 'runs', '_cache', 'pa_*.npz'))
    stored = PA.TabsPA(cache_dir=os.path.join(ROOT, 'runs', '_cache'))
    cat, code, steps, nto, fo = SC.build_tables('S', machine='S1', cap=400, fuel=1200, rows=list(range(59)), cols=list(range(59)),
                                                 workers=3, s1tab={}, regress=True)
    code, steps, nto, fo = code[:59], steps[:59], nto[:59], fo[:59]
    out = dict(stored=[os.path.basename(p) for p in path],
               code_diff=int((code != stored.code).sum()), steps_diff=int((steps != stored.steps.astype(np.int32)).sum()),
               nto_diff=int((nto != stored.nto).sum()), fo_diff=int((fo != stored.fo).sum()), profiles=int(code.size))
    return out


def new_fuel(nsample, seed=7):
    TP.install_counter()
    cat = SC.Cat('S')
    tab = SC.s1_table(cat.terms)
    SC.install_s1(tab)
    S.set_machine('S1')
    rng = random.Random(seed)
    K = cat.K
    heavy = [p for p in range(K) if cat.fam[p] not in ('const', 'junk_f', 'junk_r')]
    prof = [(rng.choice(heavy), rng.randrange(K), rng.randrange(K)) for _ in range(nsample)]
    res = {}
    for on in (True, False):
        S.set_regress(on)
        t0 = time.time()
        r = L.run_big(lambda: [TP.f_eval(cat.terms[a], cat.terms[b], cat.terms[c], S.KRP)[:4] for a, b, c in prof])
        res[on] = (r, time.time() - t0)
    S.set_regress(True)
    diff = [(cat.names[a], cat.names[b], cat.names[c], x, y) for (a, b, c), x, y in zip(prof, res[True][0], res[False][0]) if x != y]
    return dict(n=nsample, differ=len(diff), examples=diff[:10], wall_on=round(res[True][1], 1), wall_off=round(res[False][1], 1))


if __name__ == '__main__':
    out = dict(old_fuel=old_fuel())
    print(out, flush=True)
    out['new_fuel'] = new_fuel(int(sys.argv[2]) if len(sys.argv) > 2 else 300)
    print(out['new_fuel'], flush=True)
    os.makedirs(os.path.dirname(os.path.abspath(sys.argv[1])), exist_ok=True)
    json.dump(out, open(sys.argv[1], 'w'), indent=1)
