"""The PD under rule B-own (per-program memo, `Bo`; `Bow` = pre-warmed memos at generation 0) and the individual-level island
ledger (`Bi`, the like-for-like partner of B-own).  The run object of pricing_rules_pd with the memo kernel
(pricing_rules_pdkern_memo.segment_m).  Lineage tracking is on (a founder is its own lineage; offspring inherit the lineage id);
the memo of a program is the set of (lineage, reader type, partner type) keys paid on its island.
"""
import os
import sys

import numpy as np
from numba import types
from numba.typed import Dict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world_k as WK
import realizable_scaling as RS
import provenance as PV
import pricing_rules_pd as PD
import pricing_rules_pdkern_memo as KM

KC = 200000
LID = 16384


class MemoRun(PD.PricedRun):
    def __init__(self, cell, rep, track=True):
        super().__init__(cell, rep, track=True)
        I, N = self.I, self.N
        self.costind = np.zeros((I, N))
        self.memd = Dict.empty(key_type=types.int64, value_type=types.int64)
        self.spd = Dict.empty(key_type=types.int64, value_type=types.int64)
        self.dirty = np.ones(I, np.int64)
        self.MST = np.zeros(8)
        rule = PD.CFG['rule']
        self.mmode = 2 if rule == 'Bi' else 1
        self.warm0 = 1 if rule == 'Bow' else 0

    def advance(self, gens):
        LS, st = self.LS, self.LS['st']
        self.g = KM.segment_m(
            self.g, gens, self.seed, self.N, RS.W, self.mN / self.N, self.r, self.slots, self.counts, self.paysum,
            self.pres, self.npres, self.pos, self.spcount, self.d, self.tunit, self.trule, self.tsp, self.tanc,
            self.ntv, st['utau'], st['BLC'], st['BLD'], st['SINGLE'], st['APP'], LS['PRODC'], LS['PD'], st['KIND'],
            st['NAT'], st['CHC'], st['CHD'], st['UVt'], self.A, self.selfa, LS['OSV'], LS['SPO'], LS['capable'],
            LS['COSTS'], self.ctr, self.steps_rule, self.wn, self.wenc, self.wsp, self.wcode, self.wsid, self.ckey,
            self.cval, self.ncache, self.plog, self.hist_wait, self.hist_acq, self.hist_steps, self.hist_cens,
            self.nprod, LS['ident'], LS['spo_unit'], self.tset, self.uns, self.rulecount, self.enc_exp, self.skip,
            LS['FUT'], self.fcount, self.enc_futile, self.err,
            self.epsg, self.pairmode, self.fseed, self.cumL, self.spE, PV.R_SNON, bool(self.track), self.lin,
            self.nlin, self.fr, self.frf, self.nfr, self.rcount, self.PX,
            self.costind, self.memd, self.spd, self.dirty, self.MST, self.mmode, self.warm0)
        if self.err[0] != 0:
            raise RuntimeError('kernel error %d in %s rep %d at generation %d (types %d)' % (
                self.err[0], self.cell, self.rep, self.g, self.ntv[0]))

    def memo_stats(self):
        """Sizes of the memos (per program) or of the island ledgers, and the payment counters."""
        grp = {}
        for key in self.memd.keys():
            t = key % KC; rest = key // KC
            k = rest % KC; rest //= KC
            L = rest % LID; i = rest // LID
            grp[(i, L, k)] = grp.get((i, L, k), 0) + 1
        sizes = []
        if self.mmode == 1:
            for i in range(self.I):
                for j in range(self.N):
                    sizes.append(grp.get((i, int(self.lin[i, j]), int(self.slots[i, j])), 0))
        else:
            isl = {}
            for (i, L, k), n in grp.items(): isl[i] = isl.get(i, 0) + n
            sizes = [isl.get(i, 0) for i in range(self.I)]
        M = self.MST
        return dict(mode=int(self.mmode), size_mean=float(np.mean(sizes)), size_max=float(np.max(sizes)),
                    keys=len(self.memd), payments=float(M[0]), pay_steps=float(M[1]), cert_pay=float(M[2]), cert_steps=float(M[3]),
                    first_pay=float(M[4]), first_steps=float(M[5]), groups=float(M[6]), warm_free=float(M[7]))

    def final_logs(self):
        super().final_logs()
        PD.LAST['memo'] = self.memo_stats()


def memo_job(cell, rep, rule, level, horizon=10000, cst=None):
    import time
    PD.CFG.update(rule=rule, level=level, cst=cst)
    WK.IslandRun = MemoRun
    t0 = time.time()
    r = WK.island_job((cell, rep, 'K', horizon, True))
    r['rule'] = rule; r['level'] = level; r['time_total'] = time.time() - t0
    r['ledger'] = PD.LAST.get('ledger')
    r['memo'] = PD.LAST.get('memo')
    return r
