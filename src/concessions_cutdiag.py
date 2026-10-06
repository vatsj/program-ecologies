import sys, json
sys.path.insert(0, 'src')
import numpy as np
import concessions as K
import union as U
out = {}
cells = [('P01_CC_c0.5_N100', 'P01', 1e2), ('P01_CC_c0.5_N1000', 'P01', 1e3), ('P01_CC_c0.5_N10000', 'P01', 1e4), ('P01_CC_c0.5_N30000', 'P01', 3e4),
         ('P0_CC_c0.5_N1000', 'P0', 1e3), ('P0_CC_c0.5_N10000', 'P0', 1e4), ('ref_CC_c0.5_N1000', 'ref', 1e3), ('ref_CC_c0.5_N10000', 'ref', 1e4),
         ('ref_CC_c0.5_N30000', 'ref', 3e4), ('sham_CC_c0.5_N10000', 'sham', 1e4), ('P01_CC_c0.5_N10000_nofaker', 'P01', 1e4)]
for name, arm, N in cells:
    C = K.build_language(arm, 'CC', 0, 0.5)
    sv = K._Saved(name, C)
    ch = K.make_chain(C, 'CC', 0, 0.5, N)
    codes = np.asarray(sv.codes, np.int64)
    lpi = sv.lpi
    r = ch.rows(codes, codes, lpi, 1e-300, mode=1)
    src, dst, fl = r[0], r[1], r[2]
    chg = r[7]
    f = np.exp(fl)
    tot_out = float(np.exp(lpi) @ r[3])
    def summ_of(code):
        b, x, y = ch.decode(int(code))
        return U.summary(int(C['Jc'][b, x, y]), int(C['tagc'][x]), int(C['tagc'][y]))
    ssrc = np.array([summ_of(codes[i]) for i in src])
    sdst = np.array([summ_of(d) for d in dst])
    cut = float(f.sum()); cutc = float(f[chg].sum())
    d = dict(cut_flow=cut, cut_rel_total=cut / tot_out, cut_outcome_changing=cutc,
             dst_summary={U.SUMM[k]: float(f[sdst == k].sum() / cut) for k in range(7)},
             src_summary={U.SUMM[k]: float(f[ssrc == k].sum() / cut) for k in range(7)},
             into_fair_from_nonfair=float(f[(sdst == 0) & (ssrc != 0)].sum() / cut),
             out_of_fair=float(f[(ssrc == 0) & (sdst != 0)].sum() / cut),
             distinct_destinations=int(len(np.unique(dst))),
             fair_pi=float(np.exp(lpi)[[summ_of(c) == 0 for c in codes]].sum()))
    jj = json.load(open('runs/concessions/chain_%s.json' % name))
    for bname_, bsum in (('fair', 0), ('1/4', 1)):
        br = jj['basin_rates'].get(bname_)
        if br is None: continue
        outA = float(f[(ssrc == bsum) & (sdst != bsum)].sum())
        esc = br['escape_rate']; piA = br['pi']
        cesc = esc + outA / piA
        d['corrected_' + bname_] = dict(explored_escape=esc, cut_escape=outA / piA, corrected_escape=cesc, pi_explored=piA, pi_corrected=piA * esc / cesc)
    out[name] = d
    print(name, json.dumps(d), flush=True)
json.dump(out, open('runs/concessions/cut_diagnostic.json', 'w'), indent=1)
