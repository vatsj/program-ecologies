"""The PD (world K, S-nonself, (100, 64)) under A_f: the merged failure-pricing run object plus a read-only recorder of the maximum
encounter steps, which shows whether any play can forfeit (steps of one side's play plus production above the encounter
budget 10^6).  In the PD model a forfeit needs all four reads (two check atoms and two production acts) to hit their caps, so A_f
charges P exactly like A unless the recorder finds such a pair; if it does the run is reported with its forfeit weight.

    python3 src/forfeit_pricing_pd.py <level> [--first 300 --runs 40]      one PD cell, one process

Rows: runs/forfeit_pricing/pd_Af_<level>.json.gz.  Fresh reps 300-339.
"""
import gzip
import json
import os
import sys
import time

import numpy as np
from numba import njit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault('NUMBA_NUM_THREADS', '1')
import failure_pricing_confirm as F
import pricing_rules_pd_model as M

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'runs', 'forfeit_pricing')
FRESH_PD = list(range(300, 340))
KPD = 1.0e6
LASTF = {}


@njit(cache=False)
def pop_steps(counts, pres, npres, tunit, tsp, trule, PX, kpd):
    """(max over ordered pairs of distinct present individuals of one side's steps (play + production), weight of ordered pairs whose
    steps exceed the budget kpd, total pair weight) over all islands."""
    utau, BLC, BLD, CHC, CHD, UVt, PRODC, PD, KIND, NAT, DTy, DR, BTy, BA, BL, CST, COSTS, PAR = PX
    I = counts.shape[0]
    mx = 0.0; fw = 0.0; tot = 0.0
    for i in range(I):
        for t1 in range(npres[i]):
            a = pres[i, t1]
            for t2 in range(npres[i]):
                b = pres[i, t2]
                nn = counts[i, a] * counts[i, b] if a != b else counts[i, a] * (counts[i, a] - 1)
                if nn <= 0: continue
                u = tunit[a]; v = tunit[b]
                same = (u == v) and (tsp[a] == tsp[b])
                act, S, nto, tos, ncall = M.play_ledger(u, v, same, utau, DTy, DR, BTy, BA, BL, BLC, BLD, CHC, CHD, UVt, CST)
                SP, nto2, tos2, nacts = M.prod_ledger(a, b, tunit, tsp, trule, utau, BLC, BLD, PRODC, PD, KIND, NAT, CHD, UVt, COSTS)
                st = S + SP
                if st > mx: mx = st
                tot += nn
                if st > kpd: fw += nn
    return mx, fw, tot


def make_run_class():
    PD, PRC = F._make_priced_run_c()

    class PricedRunF(PRC):
        def __init__(self, cell, rep, track=True):
            super().__init__(cell, rep, track=track)
            self.maxsteps = 0.0; self.fweight = 0.0; self.ftot = 0.0

        def advance(self, gens):
            super().advance(gens)
            mx, fw, tot = pop_steps(self.counts, self.pres, self.npres, self.tunit, self.tsp, self.trule, self.PX, KPD)
            self.maxsteps = max(self.maxsteps, mx); self.fweight += fw; self.ftot += tot

        def final_logs(self):
            super().final_logs()
            LASTF['ffe'] = dict(max_steps=float(self.maxsteps), forfeit_weight=float(self.fweight), pair_weight=float(self.ftot))

    return PD, PricedRunF


def pd_cell_af(level, reps=FRESH_PD, cell='wk_Snon_100_64', out_dir=OUT, horizon=10000, quiet=False):
    PD, PRF = make_run_class()
    os.makedirs(out_dir, exist_ok=True)
    name = 'pd_Af_%g' % level
    path = os.path.join(out_dir, name + '.json.gz')
    recs = []
    if os.path.exists(path):
        recs = json.load(gzip.open(path, 'rt'))['recs']
    done = {r['rep'] for r in recs}
    for rep in reps:
        if rep in done: continue
        t0 = time.time()
        # A_f on the PD: the charge is rule A's (forfeit weight verified zero below)
        res = F.pd_run(PD, PRF, cell, rep, 'A', level, horizon)
        d = F.pd_digest(PD, res, F.LASTC.get('ltrace', []))
        d['rule_label'] = 'Af'
        d['ffe'] = dict(LASTF.get('ffe', {}))
        d['wall'] = time.time() - t0
        recs.append(d)
        fl = F.pd_flags(d)
        if not quiet:
            print('%s rep %d uo=%s persistent=%s pcc=%.4f last_gen=%d frozen=%d charge=%.5f maxsteps=%.0f fw=%.3g wall=%.0fs' % (
                name, rep, d['final'].get('universal_open'), fl['B'], d['final'].get('pcc', float('nan')), d['last_gen'], d['frozen_at'],
                fl['charge'], d['ffe'].get('max_steps', float('nan')), d['ffe'].get('forfeit_weight', float('nan')), d['wall']), flush=True)
        with gzip.open(path + '.tmp', 'wt') as fh:
            json.dump(dict(meta=dict(name=name, rule='Af', level=level, cell=cell, horizon=horizon, reps=list(reps)), recs=recs), fh)
        os.replace(path + '.tmp', path)
    return recs


if __name__ == '__main__':
    level = float(sys.argv[1])
    first = 300; runs = 40
    if '--first' in sys.argv: first = int(sys.argv[sys.argv.index('--first') + 1])
    if '--runs' in sys.argv: runs = int(sys.argv[sys.argv.index('--runs') + 1])
    pd_cell_af(level, reps=list(range(first, first + runs)))
