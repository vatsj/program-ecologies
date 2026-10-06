import sys, json, glob, os
sys.path.insert(0, 'src')
import numpy as np
import concessions as K
import union as U
out = {}
for fn in sorted(glob.glob('runs/concessions/chain_*.npz')):
    name = os.path.basename(fn)[6:-4]
    arm = name.split('_')[0]
    enf = 'RR' if '_RR_' in name else 'CC'
    pool = 1 if 'pool1' in name else 0
    c = 0.1 if 'c0.1' in name else 0.5
    C = K.build_language(arm, enf, pool, c)
    ch = K._Saved(name, C)
    Jc = C['Jc'].astype(np.int64)
    probe = np.array(['(^' in s for s in C['srcB']])
    nw = C['nmw']
    T1, SC = nw['T1 = militant (strike iff s <= 1/4)'], nw['scab']
    Mm = nw['militant- (strike iff not BOX(s = 1/2))']
    conc = np.array([probe[b] and (Jc[b, T1, T1] // 4) // 3 == 2 and Jc[b, T1, T1] % 4 == 0 and (Jc[b, SC, SC] // 4) // 3 == 0
                     for b in range(C['KcB'])])
    pi = ch.pi
    dec = np.array([ch.decode(int(cd)) for cd in ch.codes])
    js = Jc[dec[:, 0], dec[:, 1], dec[:, 2]]
    summ = np.array([U.summary(int(j), int(C['tagc'][x]), int(C['tagc'][y])) for j, (b, x, y) in zip(js, dec)])
    fair = summ == 0
    pf = pi[fair].sum()
    d = dict(fair=float(pf), probe_boss_share_of_fair=float(pi[fair & probe[dec[:, 0]]].sum() / pf) if pf > 0 else None,
             concession_boss_pi=float(pi[conc[dec[:, 0]]].sum()), probe_boss_pi=float(pi[probe[dec[:, 0]]].sum()),
             unfakeable_fair=float(pi[fair & probe[dec[:, 0]] & ((dec[:, 1] == Mm) | (dec[:, 2] == Mm))].sum()),
             militant_in_fair=float(pi[fair & ((dec[:, 1] == T1) | (dec[:, 2] == T1))].sum()),
             quarter_probe_share=float(pi[(summ == 1) & probe[dec[:, 0]]].sum() / max(pi[summ == 1].sum(), 1e-300)))
    out[name] = d
    print(name, {k: (round(v, 5) if isinstance(v, float) else v) for k, v in d.items()}, flush=True)
json.dump(out, open('runs/concessions/fairshare.json', 'w'), indent=1)
