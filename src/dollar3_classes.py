"""Language sizes and behavioural class counts for the three-player dollar
(static numbers allowed before the predictions commit).

    python3 src/dollar3_classes.py
Writes runs/dollar3_classes.json and runs/dollar3_classes_<arm>.npz (class map).
"""
import json, os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import dollar3 as D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _job(args):
    arm, s, lo, hi = args
    L, S, mu, cnt, size = D.build(arm, 6)
    return lo, D.class_hash(D.ARM[arm], *D.arrays(S), s, lo, hi)


def classes(arm, s, workers=3, chunk=40):
    L, S, mu, cnt, size = D.build(arm, 6)
    jobs = [(arm, s, lo, min(lo + chunk, S.K)) for lo in range(0, S.K, chunk)]
    H = np.zeros((S.K, 4), np.uint64)
    with Pool(workers) as pool:
        for lo, h in pool.imap_unordered(_job, jobs):
            H[lo:lo + len(h)] = h
    def part(cols):
        keys = {}
        cls = np.empty(S.K, np.int64)
        for x in range(S.K):
            k = tuple(int(v) for v in H[x, cols])
            cls[x] = keys.setdefault(k, len(keys))
        return cls
    return part([0, 1]), part([2, 3]), S, mu, cnt, size


def main():
    out = {}
    for lv, name in (((0,), 'PA'), ((0, 1), 'PA+Con')):
        L = D.Lang(10, lv)
        rows = []
        raw = D.raw_counts(12, len(L.atoms))
        for n in range(1, 13):
            row = dict(n=n, programs_of_size=raw[n], programs_upto=int(sum(raw[:n + 1])))
            if n <= 10:
                fs, mu, cnt, size = L.canon(n)
                row.update(canonical=len(fs), mass_constants=float(mu[:9].sum() / mu.sum()))
            rows.append(row)
        out['lang_' + name] = rows
    for arm, slots in [(a, (0,)) for a in sys.argv[1:]] or (('weak', (0, 1)), ('modal', (0,))):
        for s in slots:
            t = time.time()
            ca, cp, S, mu, cnt, size = classes(arm, s)
            out['%s_slot%d' % (arm, s + 1)] = dict(canonical=S.K, action_classes=int(ca.max() + 1), payoff_classes=int(cp.max() + 1), time_s=time.time() - t)
            np.savez(os.path.join(ROOT, 'runs', 'dollar3_classes_%s_slot%d.npz' % (arm, s + 1)), action=ca, payoff=cp)
            print(arm, s, out['%s_slot%d' % (arm, s + 1)], flush=True)
    json.dump(out, open(os.path.join(ROOT, 'runs', 'dollar3_classes%s.json' % ('_' + '_'.join(sys.argv[1:]) if sys.argv[1:] else '')), 'w'), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
