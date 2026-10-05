"""Agent-based runs for the three-player dollar (finite eps*N; approach rates,
not pi).  N = 100 per slot, eps = 1e-3 per birth, 1e5 generations, 3 seeds,
starts uniform-random and grand coalition, arms modal and weak.

    python3 src/dollar3_abm_run.py [--workers 2]
Writes runs/dollar3/abm.json.
"""
import argparse, json, os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from dollar3_abm import cell

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAIRS = ('P12', 'P13', 'P23')


def summarize(r):
    lab = r['labels']; every = r['every']
    typ = np.array(r['typ'])
    # dwell: runs of a constant dominant label
    runs = []
    cur, start = lab[0], 0
    for k in range(1, len(lab) + 1):
        if k == len(lab) or lab[k] != cur:
            runs.append((cur, (k - start) * every, start == 0, k == len(lab)))
            if k < len(lab): cur, start = lab[k], k
    pair_runs = [d for l, d, first, last in runs if l in PAIRS and not first and not last]
    pair_runs_all = [d for l, d, first, last in runs if l in PAIRS]
    # pair-to-pair turnover: consecutive pair labels (ignoring mixed/other in between)
    seq = [l for l, d, f, la in runs if l != 'mixed']
    p2p = sum(1 for a, b in zip(seq, seq[1:]) if a in PAIRS and b in PAIRS and a != b)
    pairprob = typ[:, 1] + typ[:, 2] + typ[:, 3]
    first_pair = next((k * every for k, v in enumerate(pairprob) if v > 0.5), None)
    frac = {l: sum(d for l2, d, f, la in runs if l2 == l) / (len(lab) * every) for l in ('G', 'P12', 'P13', 'P23', 'X', 'mixed')}
    return dict(arm=r['arm'], start=r['start'], seed=r['seed'], time_s=r['time_s'],
                mean_outcome=dict(zip(['grand', 'fair pair', 'unfair pair', 'wasteful pair', 'disagreement'], typ.mean(0).round(4).tolist())),
                mean_outcome_second_half=dict(zip(['grand', 'fair pair', 'unfair pair', 'wasteful pair', 'disagreement'], typ[len(typ) // 2:].mean(0).round(4).tolist())),
                dominant_label_time=frac, n_pair_runs=len(pair_runs_all), mean_pair_dwell_interior=float(np.mean(pair_runs)) if pair_runs else None,
                median_pair_dwell_interior=float(np.median(pair_runs)) if pair_runs else None,
                pair_to_pair_switches=p2p, first_gen_pair_prob_above_half=first_pair,
                mean_max_share=float(np.mean(np.max(r['pay'], axis=1))) if r['pay'] else None,
                label_runs=[(l, d) for l, d, f, la in runs][:400], dominant_programs_sample=r['dom_src'][:50])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--gens', type=int, default=100000)
    ap.add_argument('--arms', nargs='+', default=['modal', 'weak'])
    a = ap.parse_args()
    jobs = [(arm, start, seed, 100, 1e-3, a.gens, 10, 0.3) for arm in a.arms for start in ('uniform', 'grand') for seed in (1, 2, 3)]
    t = time.time()
    with Pool(a.workers) as pool:
        res = pool.map(cell, jobs, chunksize=1)
    out = [summarize(r) for r in res]
    os.makedirs(os.path.join(ROOT, 'runs', 'dollar3'), exist_ok=True)
    json.dump(dict(jobs=out, time_s=time.time() - t), open(os.path.join(ROOT, 'runs', 'dollar3', 'abm.json'), 'w'), indent=1, default=str)
    for o in out:
        print(o['arm'], o['start'], o['seed'], o['mean_outcome'], 'pair runs', o['n_pair_runs'], 'mean dwell', o['mean_pair_dwell_interior'],
              'p2p', o['pair_to_pair_switches'], 'first pair', o['first_gen_pair_prob_above_half'], flush=True)


if __name__ == '__main__':
    main()
