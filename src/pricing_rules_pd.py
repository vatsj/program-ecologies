"""The PD (world K, S-nonself, the realizable carrier lottery) under the pricing rules.

Runs the stored island job (world_k.island_job) with the run object replaced by one whose Moran fitness is the pair payoff
net of the rule's charge (pricing_rules_pd_model.pay_net) and whose kernel is the generated copy with that payoff
(pricing_rules_pdkern.segment_p).  Zero price reproduces the stored run draw for draw (a test).

    python3 src/pricing_rules_pd.py <rule> <level> <cell> --runs n [--horizon 10000] [--first 0]

rule in {Z, F, A, FA, B, T}; cell in {wk_Snon_100_64 (primary), wk_Snon_200_64 (larger geometry)}.
Rows: runs/pricing_rules/pd_<rule>_<level>_<cell>.json.gz  (small: one record per run).
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
import world_k as WK
import annealed as AN
import realizable_scaling as RS
import provenance as PV
import pricing_rules_pd_model as M
import pricing_rules_pdkern as KP

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'runs', 'pricing_rules')
CFG = {'rule': 'Z', 'level': 0.0, 'cst': None}
LAST = {}


class PricedRun(WK.IslandRun):
    """The world-K island run with priced fitness."""

    def __init__(self, cell, rep, track=True):
        super().__init__(cell, rep, track=track)
        self.PX = M.make_px(self.LS, CFG['rule'], CFG['level'], CFG['cst'])
        self.paysum[:] = 0.0
        KP.init_paysum_p(self.counts, self.paysum, self.pres, self.npres, self.tunit, self.tsp, self.trule, self.A, self.selfa, self.PX)

    def advance(self, gens):
        LS, st = self.LS, self.LS['st']
        self.g = KP.segment_p(
            self.g, gens, self.seed, self.N, RS.W, self.mN / self.N, self.r, self.slots, self.counts, self.paysum,
            self.pres, self.npres, self.pos, self.spcount, self.d, self.tunit, self.trule, self.tsp, self.tanc,
            self.ntv, st['utau'], st['BLC'], st['BLD'], st['SINGLE'], st['APP'], LS['PRODC'], LS['PD'], st['KIND'],
            st['NAT'], st['CHC'], st['CHD'], st['UVt'], self.A, self.selfa, LS['OSV'], LS['SPO'], LS['capable'],
            LS['COSTS'], self.ctr, self.steps_rule, self.wn, self.wenc, self.wsp, self.wcode, self.wsid, self.ckey,
            self.cval, self.ncache, self.plog, self.hist_wait, self.hist_acq, self.hist_steps, self.hist_cens,
            self.nprod, LS['ident'], LS['spo_unit'], self.tset, self.uns, self.rulecount, self.enc_exp, self.skip,
            LS['FUT'], self.fcount, self.enc_futile, self.err,
            self.epsg, self.pairmode, self.fseed, self.cumL, self.spE, PV.R_SNON, bool(self.track), self.lin,
            self.nlin, self.fr, self.frf, self.nfr, self.rcount, self.PX)
        if self.err[0] != 0:
            raise RuntimeError('kernel error %d in %s rep %d at generation %d (types %d)' % (
                self.err[0], self.cell, self.rep, self.g, self.ntv[0]))

    def final_logs(self):
        super().final_logs()
        L = pop_ledger(self.counts, self.pres, self.npres, self.N, self.tunit, self.tsp, self.trule, self.PX)
        LAST['ledger'] = L.mean(0).tolist()               # steps/play, production steps/play, timeouts/play, charge/play, pairs
        LAST['ledger_isl'] = L[:, 3].tolist()


@njit(cache=False)
def pop_ledger(counts, pres, npres, N, tunit, tsp, trule, PX):
    """Per island: mean per-play steps, production steps, timed-out calls (play + production) per play and the mean
    charge per play, over ordered pairs of distinct individuals, using the ledger functions of the model."""
    utau, BLC, BLD, CHC, CHD, UVt, PRODC, PD, KIND, NAT, DTy, DR, BTy, BA, BL, CST, COSTS, PAR = PX
    I = counts.shape[0]
    out = np.zeros((I, 5))
    for i in range(I):
        tot = 0.0; s = 0.0; sp = 0.0; to = 0.0; ch = 0.0
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
                tot += nn; s += nn * S; sp += nn * SP; to += nn * (nto + nto2); ch += nn * M.charge_pair(a, b, tunit, tsp, trule, PX)
        if tot > 0:
            out[i, 0] = s / tot; out[i, 1] = sp / tot; out[i, 2] = to / tot; out[i, 3] = ch / tot; out[i, 4] = tot
    return out


def _slim(d):
    return d


def pd_job(cell, rep, rule, level, horizon=10000, cst=None):
    if rule in ('Bo', 'Bow', 'Bi'):
        import pricing_rules_pd_memo as PM
        return PM.memo_job(cell, rep, rule, level, horizon, cst)
    CFG.update(rule=rule, level=level, cst=cst)
    WK.IslandRun = PricedRun
    t0 = time.time()
    r = WK.island_job((cell, rep, 'K', horizon, False))
    r['rule'] = rule; r['level'] = level; r['time_total'] = time.time() - t0
    r['ledger'] = LAST.get('ledger')
    return r


KEEP_FINAL = ('g', 'pcc', 'islands90', 'held', 'outcome', 'universal_open', 'open_islands', 'identity_islands')


def digest(r):
    """The small record kept per run."""
    fin = r['final']
    d = dict(cell=r['cell'], rep=r['rep'], rule=r['rule'], level=r['level'], last_gen=r['last_gen'], frozen_at=r['frozen_at'],
             time_s=r['time_s'], n_types=r['n_types'], uo_first=r['uo_first'], uo_last_change=r['uo_last_change'],
             final={k: fin[k] for k in KEEP_FINAL if k in fin}, cls=fin['cls'],
             establish=r['establish'], steps_rule=r['steps_rule'], ledger=r.get('ledger'), memo=r.get('memo'), ctr_enc=int(np.sum(np.array(r['ctr'])[:, 0])) if 'ctr' in r else None)
    d['trace'] = [t for t in r['trace'] if t[0] in (10, 50, 100, 200, 500, 1000, 2000, 5000, 10000)]
    d['mean_pcc_trace'] = [(t[0], t[1]) for t in d['trace']]
    return d


def run_cell(rule, level, cell, runs, horizon=10000, first=0, tag=None):
    os.makedirs(OUT, exist_ok=True)
    name = 'pd_%s_%g_%s%s' % (rule, level, cell, '' if tag is None else '_' + tag)
    path = os.path.join(OUT, name + '.json.gz')
    recs = []
    if os.path.exists(path):
        recs = json.load(gzip.open(path, 'rt'))['recs']
    done = {r['rep'] for r in recs}
    for rep in range(first, first + runs):
        if rep in done: continue
        t0 = time.time()
        res = pd_job(cell, rep, rule, level, horizon)
        d = digest(res)
        # the population's ledger at the end (per island, then the mean)
        d['wall'] = time.time() - t0
        recs.append(d)
        print('%s rep %d uo=%s pcc=%.4f last_gen=%d frozen=%d wall=%.0fs' % (
            name, rep, d['final'].get('universal_open'), d['final'].get('pcc', float('nan')), d['last_gen'], d['frozen_at'], d['wall']), flush=True)
        with gzip.open(path + '.tmp', 'wt') as f:
            json.dump(dict(meta=dict(name=name, rule=rule, level=level, cell=cell, horizon=horizon), recs=recs), f)
        os.replace(path + '.tmp', path)
    return name


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('rule'); ap.add_argument('level', type=float); ap.add_argument('cell')
    ap.add_argument('--runs', type=int, default=20); ap.add_argument('--horizon', type=int, default=10000)
    ap.add_argument('--first', type=int, default=0)
    a = ap.parse_args()
    run_cell(a.rule, a.level, a.cell, a.runs, a.horizon, a.first)
