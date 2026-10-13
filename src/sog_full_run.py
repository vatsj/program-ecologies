"""Runs for the social organization game, fully realizable (notes/sog-fully-realizable.md): cost calibration,
validation, static tables, lottery cells, assays.

  python3 src/sog_full_run.py calibrate        # fit the cost model's global constants against the term (§1.x)
  python3 src/sog_full_run.py validate         # code validation of notes §1 (before any counted cell)
  ...
"""
import os
import sys
import json
import time
import random
import pickle
import argparse
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import sog_full as F

L, C = F.L, F.C
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RUNS = os.path.join(ROOT, 'runs')
OUT = os.path.join(RUNS, 'sog_full')
COSTC_FILE = os.path.join(RUNS, 'sog-full-costc.json')
os.makedirs(OUT, exist_ok=True)

_G = {}


def grammar(gram):
    if gram not in _G:
        _G[gram] = F.Grammar(gram)
    return _G[gram]


def load_costc():
    if os.path.exists(COSTC_FILE):
        d = json.load(open(COSTC_FILE))
        F.COSTC['VONE'] = {r: tuple(v) for r, v in d['VONE'].items()}
        F.COSTC['BK'] = d['BK']
        for k, v in d.get('extra', {}).items(): F.COSTC[k] = v
        return True
    return False


# ----------------------------------------------------------------------------------------------------------------
# calibration (notes §1.7, §1.x)
# ----------------------------------------------------------------------------------------------------------------
def rand_subinv(rng, g, role, sp, full=False):
    tk = int(g.roles[role]['tau'][sp])
    _, per = g.hlist(role, tk)
    inv = []
    for A in F.FAM[role]:
        k = len(per[A])
        if full:
            inv.append(tuple(range(k)))
        elif k and rng.random() < 0.7:
            # S-type inventories hold at most one script per set; H holds all: mix both shapes
            if rng.random() < 0.5:
                inv.append((rng.randrange(k),))
            else:
                inv.append(tuple(sorted(rng.sample(range(k), rng.randrange(1, k + 1)))))
        else:
            inv.append(())
    return tuple(inv)


def calib_vone(n=1500, seed=11):
    """VONE own steps: forced measurements, linear fit over (1, pairs, C cons, D cons, scanned, attempts, ok, entries)."""
    rng = random.Random(seed)
    g = grammar('id')
    rows = defaultdict(list)
    while sum(len(v) for v in rows.values()) < n:
        role = 'W' if rng.random() < 0.6 else 'B'
        sp = rng.randrange(len(g.roles[role]['spellings']))
        inv = rand_subinv(rng, g, role, sp)
        tk = int(g.roles[role]['tau'][sp])
        ents = F.inv_entries(g, role, tk, inv)
        if not ents: continue
        x = g.roles[role]['spellings'][sp]
        t = F.dt(x)
        A = rng.choice(list(F.FAM[role]))
        prog = F.compile_program(x, role, F.list_data(ents))
        forced = {a: rng.choice('TF') for a in F.dt_atoms(t) if a[0] != 'E'}
        if role == 'W':
            eqv = rng.random() < 0.5
            idc = {'EQ': eqv, 'copy': F.compile_program(x, role, 0)}
            idv = (lambda e: (lambda nm: nm == 'EQ' and e))(eqv)
            slot = rng.choice((1, 2))
        else:
            c = rng.choice(F.BOSS_ID_COMBOS)
            idc = dict(zip(('N1', 'N2', 'EQW'), c))
            idv = (lambda d: (lambda nm: d.get(nm, False)))(idc)
            slot = 0
        meas = F.measure_nodes(role, slot, prog, A, idc, forced)
        att = 0; ok = False; scanned = len(ents)
        for i, (A2, s) in enumerate(ents):
            if A2 != A: continue
            att += 1
            r, calls, nodes_ = F.sym_check_trace(t, role, A, s, idv, lambda a: forced[a])
            if r is not None:
                ok = True; scanned = i + 1; break
        lc = F.list_counts(ents)
        rows[role].append((meas[0][1], (1, lc[0], lc[3], lc[4], scanned, att, int(ok), len(ents))))
    out = {}
    for role in 'WB':
        Y = np.array([r[0] for r in rows[role]], float)
        X = np.array([r[1] for r in rows[role]], float)
        coef, *_ = np.linalg.lstsq(X, Y, rcond=None)
        c = np.round(coef).astype(int)
        err = X @ c - Y
        out[role] = dict(coef=c.tolist(), n=len(Y), max_err=float(abs(err).max()), lstsq=coef.tolist())
    return out


def const_boss(code):
    """A constant boss program pay(code) with its constant list (the path tactic's: EvR*; Ax per set holding it)."""
    return F.carrier4(F.N(code), S_constant_list(code))


def S_constant_list(code):
    return F.S.constant_list(code)


BK_NAMES = ['F0', 'T0', 'F1', 'hit', 'ins', 'ins_cnt', 'ins_len', 'fail', 'fail_cnt', 'cap']


def bk_features(pops, ok):
    f = dict.fromkeys(BK_NAMES, 0)
    if not pops and not ok:
        f['F0'] = 1
        return f
    f['T0' if ok else 'F1'] = 1
    for p in pops:
        if p[0] == 'hit': f['hit'] += 1
        elif p[0] == 'ins': f['ins'] += 1; f['ins_cnt'] += p[1]; f['ins_len'] += p[2]
        elif p[0] == 'fail': f['fail'] += 1; f['fail_cnt'] += p[1]
        else: f['cap'] += 1
    return f


def bk_samples(n, seed):
    """(encounter data, keys, term totals, boss totals) for worker checks beside constant bosses."""
    rng = random.Random(seed)
    g = grammar('id')
    w = g.roles['W']
    tagged = [sp for sp in range(len(w['spellings'])) if F.tagged(w['dts'][w['tau'][sp]])]
    reg = F.Registry(g)
    out = []
    while len(out) < n:
        code = rng.choice([1, 4, 7])
        bprog = const_boss(code)
        bview = tuple('T' if code in A else 'F' for A in F.BOSS_Q)
        sx = rng.choice(tagged)
        sy = sx if rng.random() < 0.3 else (rng.choice(tagged) if rng.random() < 0.7 else rng.randrange(len(w['spellings'])))
        ix = rand_subinv(rng, g, 'W', sx, full=rng.random() < 0.4)
        iy = rand_subinv(rng, g, 'W', sy, full=rng.random() < 0.4)
        px, py = reg.get('W', sx, ix), reg.get('W', sy, iy)
        progx = F.compile_program(w['spellings'][sx], 'W', F.list_data(reg[px].entries))
        progy = F.compile_program(w['spellings'][sy], 'W', F.list_data(reg[py].entries))
        enc_t = (bprog, progx, progy)
        L.CACHE.clear()
        btot = [F.term_check(enc_t, 0, A)[1] for A in F.BOSS_Q]
        terms = {}
        for j in (1, 2):
            for A in F.WORKER_Q:
                terms[(j, A)] = F.term_check(enc_t, j, A)
        out.append((bview, px, py, btot, terms))
    return reg, out


def bk_residuals(reg, samples):
    cm = F.CostModel(reg.g, F.live_of('eq'), {})
    rows = []
    nmis = 0
    for bview, px, py, btot, terms in samples:
        ae = F.AbsEval4(reg, cm, F.live_of('eq'))
        for (j, A), (tv, tt) in terms.items():
            key = (('E', bview, px, py), j, A)
            v = ae.check(key)
            if v != tv: nmis += 1
            if v == 'TO' or tv != v: continue
            cst = ae.cost(key)
            pred = cst[0] + sum(cst[i + 1] * btot[i] for i in range(3))
            pops, ok = ae.pops[key]
            rows.append((tt - pred, bk_features(pops, ok)))
    return rows, nmis


def calib_bk(n=600, seed=12):
    """Closure bookkeeping, fitted on natural term totals of worker checks beside constant bosses (nested checks'
    bookkeeping is part of each prediction, so the fit is iterated to its fixed point)."""
    reg, samples = bk_samples(n, seed)
    params = dict.fromkeys(BK_NAMES, 0)
    hist = []
    for it in range(8):
        F.COSTC['BK'] = dict(params)
        rows, nmis = bk_residuals(reg, samples)
        Y = np.array([r[0] + F.bk_steps_feat(r[1], params) for r in rows], float)
        X = np.array([[r[1][k] for k in BK_NAMES] for r in rows], float)
        used = [i for i in range(len(BK_NAMES)) if X[:, i].any()]
        coef, *_ = np.linalg.lstsq(X[:, used], Y, rcond=None)
        newp = dict.fromkeys(BK_NAMES, 0)
        for i, c in zip(used, coef): newp[BK_NAMES[i]] = int(round(c))
        err = np.array([r[0] for r in rows])
        hist.append(dict(it=it, max_abs_residual=float(abs(err).max()), params=dict(params)))
        if newp == params and abs(err).max() == 0: break
        params = newp
    F.COSTC['BK'] = dict(params)
    rows, nmis = bk_residuals(reg, samples)
    err = np.array([r[0] for r in rows])
    return dict(BK=params, n=len(rows), max_err=float(abs(err).max()), n_nonzero=int((err != 0).sum()),
                value_mismatch=nmis, hist=hist)


def calib_prod(n=1500, seed=21):
    """PROD3 own steps (forced nested calls at zero cost) against the visit-log model: least squares per role."""
    rng = random.Random(seed)
    g = grammar('id')
    cm = F.CostModel(g, F.live_of('eq'), {})
    rows = []
    while len(rows) < n:
        role = 'W' if rng.random() < 0.6 else 'B'
        sp = rng.randrange(len(g.roles[role]['spellings']))
        x = g.roles[role]['spellings'][sp]
        t = F.dt(x)
        inv = rand_subinv(rng, g, role, sp, full=rng.random() < 0.3)
        tk = int(g.roles[role]['tau'][sp])
        ents = F.inv_entries(g, role, tk, inv)
        prog = F.compile_program(x, role, F.list_data(ents))
        A = rng.choice(list(F.FAM[role]))
        forced = {a: rng.choice('TF') for a in F.dt_atoms(t) if a[0] != 'E'}
        if role == 'W':
            eqv = rng.random() < 0.5
            idc = {'EQ': eqv, 'copy': F.compile_program(x, role, 0)}
            idv = (lambda e: (lambda nm: nm == 'EQ' and e))(eqv)
            slot = rng.choice((1, 2))
        else:
            c = rng.choice(F.BOSS_ID_COMBOS)
            idc = dict(zip(('N1', 'N2', 'EQW'), c))
            idv = (lambda d: (lambda nm: d.get(nm, False)))(idc)
            slot = 0
        steps, out, sc = F.measure_prod(role, slot, prog, A, idc, forced)
        log = []
        ss, calls = F.sym_prod3(t, role, A, idv, lambda a: forced[a], log)
        if not ((sc == ss) or (out != 'found' and ss is None)):
            rows.append(('mismatch', role)); continue
        ik = F.ident_key(role, t, idv)
        tab, dcl = cm.ft_table(role, sp, slot, ik)
        lc = F.list_counts(ents)
        base, f = F.prod_features(log, tab, (lc[0] - dcl[0], lc[2] - dcl[2]), A, role)
        f['1'] = 1
        f['out_found' if ss is not None else 'out_none'] = 1
        rows.append((steps - base, f, role))
    out = {}
    nmis = sum(1 for r in rows if r[0] == 'mismatch')
    for role in 'WB':
        R = [r for r in rows if r[0] != 'mismatch' and r[2] == role]
        keys = sorted(set(k for r in R for k in r[1]))
        Y = np.array([r[0] for r in R], float)
        X = np.array([[r[1].get(k, 0) for k in keys] for r in R], float)
        coef, *_ = np.linalg.lstsq(X, Y, rcond=None)
        err = X @ coef - Y
        out[role] = dict(model={k: float(c) for k, c in zip(keys, coef)}, n=len(Y), max_err=float(abs(err).max()),
                         median_err=float(np.median(abs(err))), p99=float(np.percentile(abs(err), 99)))
    out['script_mismatch'] = nmis
    return out


def calib_play(n=400, seed=31):
    """Own run steps of a play (calls forced at zero cost): per (role, calls made, identity atoms evaluated)."""
    rng = random.Random(seed)
    g = grammar('id')
    rows = []
    while len(rows) < n:
        role = 'W' if rng.random() < 0.5 else 'B'
        sp = rng.randrange(len(g.roles[role]['spellings']))
        x = g.roles[role]['spellings'][sp]
        t = F.dt(x)
        prog = F.compile_program(x, role, 0)
        forced = {a: rng.choice('TF') for a in F.dt_atoms(t) if a[0] != 'E'}
        if role == 'W':
            eqv = rng.random() < 0.5
            idc = {'EQ': eqv, 'copy': F.compile_program(x, role, 0)}
            idv = (lambda e: (lambda nm: nm == 'EQ' and e))(eqv)
            slot = rng.choice((1, 2))
        else:
            c = rng.choice(F.BOSS_ID_COMBOS)
            idc = dict(zip(('N1', 'N2', 'EQW'), c))
            idv = (lambda d: (lambda nm: d.get(nm, False)))(idc)
            slot = 0
        steps, v = F.measure_play(role, slot, prog, idc, forced)
        # path statistics
        ncall = 0; nid = 0
        node = t
        while isinstance(node, tuple):
            a = node[0]
            if a[0] == 'E':
                nid += 1; node = node[1] if idv(a[1]) else node[2]
            else:
                ncall += 1; node = node[1] if forced[a] == 'T' else node[2]
        rows.append((steps, role, ncall, nid, F.nodes(x)))
    out = {}
    for role in 'WB':
        R = [r for r in rows if r[1] == role]
        Y = np.array([r[0] for r in R], float)
        X = np.array([[1, r[2], r[3]] for r in R], float)
        coef, *_ = np.linalg.lstsq(X, Y, rcond=None)
        err = X @ coef - Y
        out[role] = dict(coef=coef.tolist(), max_err=float(abs(err).max()), max_steps=float(Y.max()))
    return out


def calibrate(args):
    t0 = time.time()
    v = calib_vone()
    print('VONE', json.dumps(v), '%.0fs' % (time.time() - t0), flush=True)
    F.COSTC['VONE'] = {r: tuple(v[r]['coef']) for r in 'WB'}
    b = calib_bk()
    print('BK', json.dumps(b)[:400], '%.0fs' % (time.time() - t0), flush=True)
    F.COSTC['BK'] = b['BK']
    pr = calib_prod()
    print('PROD', json.dumps({r: {k: pr[r][k] for k in ('n', 'max_err', 'median_err', 'p99')} for r in 'WB'}),
          'mismatch', pr['script_mismatch'], '%.0fs' % (time.time() - t0), flush=True)
    pl = calib_play()
    print('PLAY', json.dumps(pl), '%.0fs' % (time.time() - t0), flush=True)
    json.dump(dict(VONE={r: v[r]['coef'] for r in 'WB'}, BK=b['BK'],
                   extra=dict(PROD={r: pr[r]['model'] for r in 'WB'},
                              PLAY={r: pl[r]['coef'] for r in 'WB'},
                              PROD_ERR={r: pr[r]['max_err'] for r in 'WB'}),
                   fit=dict(vone=v, bk={k: b[k] for k in b if k != 'hist'}, prod={r: {k: pr[r][k] for k in pr[r] if k != 'model'} for r in 'WB'}, play=pl)),
              open(COSTC_FILE, 'w'), indent=1)


# ----------------------------------------------------------------------------------------------------------------
# whole-encounter replays (notes §1.9): the evaluator against the term
# ----------------------------------------------------------------------------------------------------------------
_EV = {}


def evaluator(arm, mode='S'):
    key = (arm, mode)
    if key not in _EV:
        gram = grammar(F.ARMS[arm][0])
        _EV[key] = F.Evaluator(gram, arm, mode)
    return _EV[key]


def compile_pid(ev, pid):
    pr = ev.reg[pid]
    x = ev.g.roles[pr.role]['spellings'][pr.sp]
    return F.compile_program(x, pr.role, F.list_data(pr.entries), live=ev.live)


def term_encounter(ev, b, x, y, produce=True):
    """The whole encounter by the term: plays (with step counts) and, under S-nonself_3, each participant's PROD3
    attempts in its residual fuel.  Returns dict."""
    progs = [compile_pid(ev, b), compile_pid(ev, x), compile_pid(ev, y)]
    L.CACHE.clear()
    play, steps, raw = F.play3(progs[0], progs[1], progs[2], ev.K)
    out = dict(play=(int(play[0]), play[1], play[2]), steps=tuple(int(v) for v in steps), raw=raw)
    if not produce: return out
    prods = []
    rel = ev.reg[x].sp == ev.reg[y].sp
    for j, pid in ((0, b), (1, x), (2, y)):
        pr = ev.reg[pid]
        if j > 0 and rel:
            prods.append([('refused',)]); continue
        rem = ev.K - steps[j]
        rec = []
        for si, A in enumerate(F.FAM[pr.role]):
            if pr.inv[si]: continue
            if rem <= 0:
                rec.append((si, 'fuelTO', None, 0)); continue
            sc, n, oc = F.term_prod(tuple(progs), j, A, Pcap=ev.P, V=ev.V, K=ev.K, fuel=rem)
            rem -= n
            idx = None
            if oc == 'found':
                _, per = ev.g.hlist(pr.role, pr.tk)
                scd = F._rt_data(sc)
                idx = per[A].index(scd) if scd in per[A] else ('not in H list', scd)
            rec.append((si, oc, idx, n))
        prods.append(rec)
    out['prods'] = prods
    return out


def sample_pid(rng, ev, role, mode, named=None):
    g = ev.g
    r = g.roles[role]
    if named is not None:
        x = named
        sp = r['spellings'].index(x)
    else:
        m = g.mass(role)
        sp = int(np.searchsorted(np.cumsum(m), rng.random()))
        sp = min(sp, len(m) - 1)
    tk = int(r['tau'][sp])
    if mode == 'H':
        inv = F.full_inv(g, role, tk)
    else:
        _, per = g.hlist(role, tk)
        inv = tuple(((rng.randrange(len(per[A])),) if per[A] and rng.random() < 0.6 else ()) for A in F.FAM[role])
    return ev.reg.get(role, sp, inv)


def validate_replays(n=250, seed=41, arms=('eq', 'sham', 'eqnoT', 'noeq')):
    rng = random.Random(seed)
    res = defaultdict(int)
    bad = []
    t0 = time.time()
    for it in range(n):
        arm = arms[it % len(arms)]
        mode = 'S' if rng.random() < 0.7 else 'H'
        ev = evaluator(arm, mode)
        g = ev.g
        named_b = None; named_w = (None, None)
        if rng.random() < 0.3:
            nb = rng.choice(['D*', 'D14', 'B_eq', 'B_id', 'pay(1/2,none)', 'pay(0,none)', 'WF'])
            if arm == 'noeq' and nb in ('B_eq', 'B_id'): nb = 'D*'
            named_b = F.NAMED_B[nb]
            nw = [rng.choice(['T1', 'T0', 'U_eq', 'XM', 'Q', 'U', 'scab', 'T1p']) for _ in range(2)]
            if arm == 'noeq': nw = ['T1' if w in ('U_eq', 'XM') else w for w in nw]
            named_w = (F.NAMED_W[nw[0]], F.NAMED_W[nw[1]])
        b = sample_pid(rng, ev, 'B', mode, named_b)
        x = sample_pid(rng, ev, 'W', mode, named_w[0])
        if rng.random() < 0.3:
            pr = ev.reg[x]
            y = ev.reg.get('W', pr.sp, pr.inv if rng.random() < 0.5 else F.empty_inv('W'))
        else:
            y = sample_pid(rng, ev, 'W', mode, named_w[1])
        tr = ev.triple(b, x, y)
        te = term_encounter(ev, b, x, y, produce=(mode == 'S'))
        pred_play = (tr['boss'], tr['a1'], tr['a2'])
        res['encounters'] += 1
        ok_play = pred_play == te['play']
        res['play_match'] += ok_play
        ok_steps = tuple(tr['steps']) == te['steps']
        res['steps_match'] += ok_steps
        if not (ok_play and ok_steps):
            bad.append(dict(kind='play', arm=arm, mode=mode, pred=pred_play, term=te['play'], psteps=tr['steps'],
                            tsteps=te['steps'], b=F.show(g.roles['B']['spellings'][ev.reg[b].sp]),
                            x=F.show(g.roles['W']['spellings'][ev.reg[x].sp]), y=F.show(g.roles['W']['spellings'][ev.reg[y].sp])))
        if mode == 'S':
            prs = ev.productions(b, x, y, tr)
            for (pid, npid, rec), trec in zip(prs, te['prods']):
                for k, r in enumerate(rec):
                    res['attempts'] += 1
                    if r[0] == 'refused':
                        res['attempt_match'] += trec[0][0] == 'refused'; continue
                    tr_ = trec[k] if k < len(trec) else None
                    pout = r[1]
                    tout = tr_[1] if tr_ else None
                    same_out = (pout == tout) or (pout == 'found' and tout == 'found')
                    if pout == 'found' and tout == 'found':
                        same_out = ev.reg[npid].inv[r[0]] == (tr_[2],)
                    res['attempt_match'] += same_out
                    if tout in ('found', 'none', 'capTO') and pout == tout:
                        d = abs(r[3] - tr_[3]) if tout != 'capTO' else 0
                        res['attempt_steps_absdiff_max'] = max(res['attempt_steps_absdiff_max'], d)
                    if not same_out:
                        bad.append(dict(kind='prod', arm=arm, pred=r, term=tr_, role=ev.reg[pid].role))
    res['time_s'] = time.time() - t0
    return dict(res), bad


def validate(args):
    out = {}
    r, bad = validate_replays(args.n if hasattr(args, 'n') else 250)
    out['replays'] = r
    out['replay_failures'] = bad[:40]
    print(json.dumps(r), flush=True)
    for b in bad[:10]: print(b)
    json.dump(out, open(os.path.join(RUNS, 'sog-full-validate.json'), 'w'), indent=1, default=str)


# ----------------------------------------------------------------------------------------------------------------
# the lottery driver (notes §1.11): founders, type registries, table fills on kernel misses
# ----------------------------------------------------------------------------------------------------------------
import sog_full_kern as KN
from numba import types as NT
from numba.typed import Dict as NDict
import union as UN

PAY = UN.payoff_table(0.5)
PAYF = np.array([[PAY[c // 4, (c // 2) % 2, c % 2, s] for s in range(3)] for c in range(144)])
CHECK_EVERY = 10
FORCE_PER_ISLAND = 20
VSTR = {0: 'F', 1: 'T', 2: 'TO'}


def ndict():
    return NDict.empty(key_type=NT.int64, value_type=NT.int64)


class Arr:
    """Growable arrays keyed by name (first axis grows; new space takes the array's fill value)."""

    def __init__(self):
        self.a = {}
        self.fill = {}

    def make(self, name, tail, dtype, cap, fill=0):
        self.a[name] = np.full((cap,) + tuple(tail), fill, dtype)
        self.fill[name] = fill

    def ensure(self, name, n):
        a = self.a[name]
        if n <= a.shape[0]: return
        cap = max(n, 2 * a.shape[0])
        b = np.full((cap,) + a.shape[1:], self.fill[name], a.dtype)
        b[:a.shape[0]] = a
        self.a[name] = b

    def __getitem__(self, k):
        return self.a[k]


def bexvals(bex):
    return tuple(VSTR[(bex // (3 ** A)) % 3] for A in range(3))


def decode_code(code):
    vals = tuple(VSTR[(code // 3 ** k) % 3] for k in range(8))
    ib = code // KN.CODE_ID
    return vals + (bool(ib & 1), bool(ib & 2), bool(ib & 4))


TYPE_W = (('WSP', (), -1), ('WT1', (), 0), ('WCLS', (), -1))
TYPE_B = (('BSP', (), -1), ('BCLS', (), -1))
CLS_W = (('TAG', (), 0), ('WLACK', (), 0), ('WACT', (64,), 0), ('WPLAY', (64, 6), 0))
CLS_B = (('BRA', (3,), -1), ('BRI', (27,), -1), ('PBI', (27,), -1), ('BLACK', (), 0))
ROWS = (('B_ACT', (), 0), ('B_IDL', (3,), 0), ('B_CV', (3, 9), 0), ('B_PLAYOWN', (), 0), ('B_CALLM', (8,), 0),
        ('PB_N', (), 0), ('PB_IDX', (3,), -1), ('PB_OWN', (3,), 0), ('PB_MASK', (3,), 0), ('PB_NEW', (8,), -1),
        ('PW_N', (), 0), ('PW_IDX', (2,), -1), ('PW_OWN', (2,), 0), ('PW_MASK', (2,), 0), ('PW_NEW', (4,), -1))
ROWGROUP = {'PH_V': 'ph', 'PH_C': 'ph', 'WH_I': 'wh', 'WH_CV': 'wh', 'B_ACT': 'br', 'B_IDL': 'br', 'B_CV': 'br',
            'B_PLAYOWN': 'br', 'B_CALLM': 'br', 'PB_N': 'pb', 'PB_IDX': 'pb', 'PB_OWN': 'pb', 'PB_MASK': 'pb',
            'PB_NEW': 'pb', 'PW_N': 'pw', 'PW_IDX': 'pw', 'PW_OWN': 'pw', 'PW_MASK': 'pw', 'PW_NEW': 'pw'}
SHK = KN.SH


_SHARED = {}
SHARED_NAMES = ('btypes', 'bmap', 'wtypes', 'wmap', 'bcls', 'bcmap', 'wcls', 'wcmap', 'A', 'n', 'PRD', 'WCD', 'PWD',
                'TYPB', 'TYPW', 'vs', 'PR_V', 'PR_C', 'WC_V', 'WC_CV', 'NROW', 'CONSTV', 'CONSTC', 'BKA')


class Run:
    """One lottery run: founders, type and class registries, the kernel's tables (filled on misses), snapshots.
    Types are (spelling, inventory); classes (canonical spelling of the run tree, inventory, is T1) carry the tables."""

    def __init__(self, ev, cfg, rep):
        self.ev, self.cfg, self.rep = ev, cfg, rep
        g = ev.g
        I, N = cfg['I'], cfg['N']
        self.I, self.N = I, N
        self.mode_S = 1 if cfg['mode'] == 'S' else 0
        # the tables (types, classes, rows) are a deterministic function of (evaluator, gate) and are shared by the
        # runs of one worker process; the dynamics never depend on type numbering (presence order is founder order)
        self.skey = (id(ev), cfg.get('gate', 'nonself'), self.mode_S)
        if cfg.get('share', True) and self.skey in _SHARED:
            self.__dict__.update(_SHARED[self.skey])
        else:
            self.btypes, self.bmap, self.wtypes, self.wmap = [], {}, [], {}
            self.bcls, self.bcmap, self.wcls, self.wcmap = [], {}, [], {}
            self.A = Arr()
            for nm, tail, fill in TYPE_W + TYPE_B + CLS_W + CLS_B + ROWS:
                self.A.make(nm, tail, np.int64, 4096, fill)
            self.n = defaultdict(int)
            self.PRD, self.WCD, self.PWD, self.TYPB, self.TYPW = ndict(), ndict(), ndict(), ndict(), ndict()
            self.vs = F.VTStore()
            self.PR_V = np.zeros((1 << 19, 8), np.int8); self.PR_C = np.zeros((1 << 19, 8), np.int32)
            self.WC_V = np.zeros((1 << 20, 4), np.int8); self.WC_CV = np.zeros((1 << 20, 4, 4), np.int32)
            self.NROW = np.array([0, 1 << 19, 0, 1 << 20], np.int64)
            self.CONSTV = np.array([[F.v3(v) for v in ev.const_view[sp]] for sp in (0, 1)], np.int64)
            self.CONSTC = np.array([list(ev.const_cost[sp]) for sp in (0, 1)], np.int64)
            self.BKA = F.bk_array()
        self.fills = defaultdict(int)
        self.KM = max(8192, 2 * I * N, 2 * max(len(self.btypes), len(self.wtypes)))
        self.counts = np.zeros((I, 3, self.KM), np.int64)
        rng = np.random.default_rng([rep, N, I, 20261013])
        uB = rng.random((I, N)); u1 = rng.random((I, N)); u2 = rng.random((I, N))
        cumB = np.cumsum(g.mass('B')); cumW = np.cumsum(g.mass('W'))
        spB = np.minimum(np.searchsorted(cumB, uB * cumB[-1]), len(cumB) - 1)
        sp1 = np.minimum(np.searchsorted(cumW, u1 * cumW[-1]), len(cumW) - 1)
        sp2 = np.minimum(np.searchsorted(cumW, u2 * cumW[-1]), len(cumW) - 1)
        self.founders = (spB, sp1, sp2)
        forced = cfg.get('forced')
        fn = cfg.get('force_n', FORCE_PER_ISLAND)
        ent = cfg.get('entrant')
        self.order = [[[] for _ in range(3)] for _ in range(I)]
        for i in range(I):
            for s, arr in ((0, spB), (1, sp1), (2, sp2)):
                role = 'B' if s == 0 else 'W'
                for k in range(N):
                    sp = int(arr[i, k])
                    inv = self.founder_inv(role, sp)
                    if forced is not None and k < fn:
                        sp, inv = forced[s]
                    if ent is not None and i == 0 and s == ent[0] and k == N - 1:
                        sp, inv = ent[1]
                    loc = self.type_id(role, ev.reg.get(role, sp, inv))
                    if self.counts[i, s, loc] == 0:
                        self.order[i][s].append(loc)
                    self.counts[i, s, loc] += 1
        self.pres = np.zeros((I, 3, N + 1), np.int64); self.npres = np.zeros((I, 3), np.int64)
        self.pos = -np.ones((I, 3, self.KM), np.int64)
        for i in range(I):
            for s in range(3):
                for k in self.order[i][s]:
                    self.pres[i, s, self.npres[i, s]] = k; self.pos[i, s, k] = self.npres[i, s]; self.npres[i, s] += 1
        del self.order
        self.F = np.zeros((I, 3, self.KM))
        NU = 3 * I
        self.act = np.arange(NU, dtype=np.int64); self.apos = np.arange(NU, dtype=np.int64)
        self.st = np.zeros(16, np.int64)
        for u in range(NU):
            if self.npres[u // 3, u % 3] > 1:
                KN.setact(u, True, self.act, self.apos, self.st)
        self.quiet = np.full(I, -1 if self.mode_S else 1, np.int8)
        self.nqlist = np.zeros(I, np.int64); self.nqpos = -np.ones(I, np.int64)
        if self.mode_S:
            for i in range(I):
                self.nqlist[i] = i; self.nqpos[i] = i
            self.st[KN.ST_NQ] = I
        self.ctr = np.zeros(KN.NCTR, np.int64)
        self.miss = np.zeros(8, np.int64)
        self.seed = (rep * 1000003 + N * 101 + I) % (2 ** 31)
        self.snap = None
        self.maxiter = 1 << 40
        self.qmax = cfg.get("qmax", 4000)
        self.mbuf = np.zeros((200000, 6), np.int64)
        self.debug = False
        self.t_fill = 0.0
        self.t_run = 0.0
        self.nmiss = 0

    def save_shared(self):
        _SHARED[self.skey] = {nm: getattr(self, nm) for nm in SHARED_NAMES}

    def founder_inv(self, role, sp):
        if self.cfg['mode'] == 'H':
            tk = int(self.ev.g.roles[role]['tau'][sp])
            return F.full_inv(self.ev.g, role, tk)
        return F.empty_inv(role)

    # ---- classes and types
    def class_id(self, role, cpid):
        if role == 'B':
            c = self.bcmap.get(cpid)
            if c is None:
                c = len(self.bcls); self.bcls.append(cpid); self.bcmap[cpid] = c
                for nm, _, _ in CLS_B: self.A.ensure(nm, c + 1)
                pr = self.ev.reg[cpid]
                self.A['BLACK'][c] = (sum(1 << i for i, x in enumerate(pr.inv) if not x) if self.mode_S else 0)
                pi, ii = self.ev.boss_reads(cpid)
                pos_ = list(pi) + list(ii)
                assert len(pos_) <= 3
                self.A['BRA'][c, :] = -1
                self.A['BRA'][c, :len(pos_)] = pos_
            return c
        c = self.wcmap.get(cpid)
        if c is None:
            c = len(self.wcls); self.wcls.append(cpid); self.wcmap[cpid] = c
            for nm, _, _ in CLS_W: self.A.ensure(nm, c + 1)
            self.register_wclass(c, cpid)
            self.vs.add_class(self.ev, c, cpid)
        return c

    def type_id(self, role, pid):
        ev = self.ev
        if role == 'B':
            k = self.bmap.get(pid)
            if k is None:
                k = len(self.btypes); self.btypes.append(pid); self.bmap[pid] = k
                self.ensure_types(k + 1)
                c = self.class_id('B', ev.canon(pid))
                self.A['BSP'][k] = ev.reg[pid].sp; self.A['BCLS'][k] = c
                self.TYPB[(ev.reg[pid].sp << SHK) | c] = k
            return k
        k = self.wmap.get(pid)
        if k is None:
            k = len(self.wtypes); self.wtypes.append(pid); self.wmap[pid] = k
            self.ensure_types(k + 1)
            pr = ev.reg[pid]
            c = self.class_id('W', ev.canon(pid))
            self.A['WSP'][k] = pr.sp; self.A['WT1'][k] = 1 if pr.isT1 else 0; self.A['WCLS'][k] = c
            self.TYPW[(pr.sp << SHK) | c] = k
        return k

    def ensure_types(self, n):
        for nm, _, _ in TYPE_W + TYPE_B:
            self.A.ensure(nm, n)
        if n > self.KM:
            KM = max(n, 2 * self.KM)
            names = ('counts', 'F', 'pos') if hasattr(self, 'F') else ('counts',)
            for nm in names:
                a = getattr(self, nm)
                b = np.full(a.shape[:2] + (KM,), -1 if nm == 'pos' else 0, a.dtype)
                b[:, :, :a.shape[2]] = a
                setattr(self, nm, b)
            self.KM = KM

    def register_wclass(self, c, cpid):
        ev = self.ev
        pr = ev.reg[cpid]
        t = ev.g.roles['W']['dts'][pr.tk]
        A = self.A
        A['TAG'][c] = 1 if F.tagged(t) else 0
        A['WLACK'][c] = (sum(1 << i for i, x in enumerate(pr.inv) if not x) if self.mode_S else 0)
        pc = F.COSTC['PLAY']['W']
        for bits in range(64):
            bt = tuple(bool((bits >> q) & 1) for q in range(6))
            A['WACT'][c, bits] = 0 if ev.worker_act(cpid, bt) == 'C' else 1
            node = t; ncall = 0; nid = 0
            cnt = [0] * 5
            d = {('B', F.A_GE14): (bt[0], 0), ('B', F.A_EQ12): (bt[1], 1), ('B', F.A_LE14): (bt[2], 2),
                 ('O', F.A_STRIKE): (bt[3], 4), ('O', F.A_WORK): (bt[4], 3)}
            while isinstance(node, tuple):
                a = node[0]
                if a[0] == 'E':
                    nid += 1; node = node[1] if bt[5] else node[2]
                else:
                    v, cid = d[a]; cnt[cid] += 1; ncall += 1; node = node[1] if v else node[2]
            A['WPLAY'][c, bits, 0] = int(round(pc[0] + pc[1] * ncall + pc[2] * nid))
            A['WPLAY'][c, bits, 1:] = cnt

    def newrow(self, group):
        r = self.n[group]; self.n[group] += 1
        for nm, _, _ in ROWS:
            if ROWGROUP[nm] == group: self.A.ensure(nm, r + 1)
        return r

    def rel(self, x, y):
        return 1 if self.A['WSP'][x] == self.A['WSP'][y] else 0

    # ---- fills (miss keys carry type ids)
    def fill_brow(self, b, ri, code):
        ev = self.ev
        codet = decode_code(code)
        cb = int(self.A['BCLS'][b])
        cpid = self.bcls[cb]
        act, ideal, cv = ev.boss_row(cpid, codet)
        r = self.newrow('br')
        A = self.A
        A['B_ACT'][r] = act
        A['B_IDL'][r] = [F.v3(v) for v in ideal]
        A['B_CV'][r] = np.array(cv, np.int64)
        pr = ev.reg[cpid]
        t = ev.g.roles['B']['dts'][pr.tk]
        idv = ev.ae.idv_boss(codet)
        vals = dict(zip(F.PROBE_ATOMS, codet[:8]))
        node = t; nid = 0; cnt = [0] * 8; ncall = 0
        while isinstance(node, tuple):
            a = node[0]
            if a[0] == 'E':
                nid += 1; node = node[1] if idv(a[1]) else node[2]
            else:
                cnt[F.PROBE_ATOMS.index(a)] += 1; ncall += 1; node = node[1] if vals[a] == 'T' else node[2]
        pc = F.COSTC['PLAY']['B']
        A['B_PLAYOWN'][r] = int(round(pc[0] + pc[1] * ncall + pc[2] * nid))
        A['B_CALLM'][r] = cnt
        A['BRI'][cb, ri] = r
        self.fills['br'] += 1

    def fill_pb(self, b, ri, code):
        ev = self.ev
        A = self.A
        cb = int(A['BCLS'][b])
        cpid = self.bcls[cb]
        att = ev.prod_boss(cpid, decode_code(code))
        r = self.newrow('pb')
        A['PB_N'][r] = len(att)
        pr = ev.reg[cpid]
        for a, (si, idx, own, calls) in enumerate(att):
            A['PB_IDX'][r, a] = -1 if idx is None else idx
            A['PB_OWN'][r, a] = own
            A['PB_MASK'][r, a] = sum(1 << c for c in set(calls))
        for pat in range(1 << len(att)):
            inv = list(pr.inv)
            for a, (si, idx, own, calls) in enumerate(att):
                if (pat >> a) & 1 and idx is not None:
                    inv[si] = (idx,)
            A['PB_NEW'][r, pat] = self.class_id('B', ev.canon(ev.reg.get('B', pr.sp, tuple(inv))))
        A['PBI'][cb, ri] = r
        self.fills['pb'] += 1

    def fill_pw(self, x, j, bex, oex, rel):
        ev = self.ev
        A = self.A
        cx = int(A['WCLS'][x])
        cpid = self.wcls[cx]
        oexv = (VSTR[oex % 3], VSTR[oex // 3])
        att = ev.prod_worker(cpid, j, bexvals(bex), oexv, bool(rel))
        r = self.newrow('pw')
        A['PW_N'][r] = len(att)
        pr = ev.reg[cpid]
        for a, (si, idx, own, calls) in enumerate(att):
            A['PW_IDX'][r, a] = -1 if idx is None else idx
            A['PW_OWN'][r, a] = own
            A['PW_MASK'][r, a] = sum(1 << c for c in set(calls))
        for pat in range(1 << len(att)):
            inv = list(pr.inv)
            for a, (si, idx, own, calls) in enumerate(att):
                if (pat >> a) & 1 and idx is not None:
                    inv[si] = (idx,)
            A['PW_NEW'][r, pat] = self.class_id('W', ev.canon(ev.reg.get('W', pr.sp, tuple(inv))))
        key = ((((cx * 2 + (j - 1)) * 27 + bex) * 9 + oex) * 2 + rel)
        self.PWD[key] = r
        self.fills['pw'] += 1

    def fill_type(self, role, sp, c):
        cpid = (self.bcls if role == 'B' else self.wcls)[c]
        inv = self.ev.reg[cpid].inv
        self.type_id(role, self.ev.reg.get(role, sp, inv))
        self.fills['type' + role] += 1

    def fill_miss(self, m):
        t0 = time.time()
        kind = int(m[0])
        if kind == KN.MISS_BROW: self.fill_brow(int(m[1]), int(m[2]), int(m[3]))
        elif kind == 8: self.grow_pairs()
        elif kind == KN.MISS_PB: self.fill_pb(int(m[1]), int(m[2]), int(m[3]))
        elif kind == KN.MISS_PW: self.fill_pw(int(m[1]), int(m[2]), int(m[3]), int(m[4]), int(m[5]))
        elif kind == KN.MISS_TB: self.fill_type('B', int(m[1]), int(m[2]))
        elif kind == KN.MISS_TW: self.fill_type('W', int(m[1]), int(m[2]))
        else: raise ValueError(m)
        self.t_fill += time.time() - t0

    def fill_batch(self):
        n = int(self.st[KN.ST_STATUS])
        self.st[KN.ST_STATUS] = 0
        keys = set(tuple(int(v) for v in self.mbuf[k]) for k in range(n))
        self.fills['batches'] += 1
        for key in keys:
            if key[0] == 8:
                self.grow_pairs(); continue
            if self.batch_filled(key): continue
            self.fill_miss(np.array(key + (0, 0), np.int64))

    def batch_filled(self, key):
        A = self.A
        k = key[0]
        if k == KN.MISS_BROW: return A['BRI'][int(A['BCLS'][key[1]]), key[2]] >= 0
        if k == KN.MISS_PB: return A['PBI'][int(A['BCLS'][key[1]]), key[2]] >= 0
        if k == KN.MISS_PW:
            x, j, bex, oex, rel = key[1:6]
            cx = int(A['WCLS'][x])
            return ((((cx * 2 + (j - 1)) * 27 + bex) * 9 + oex) * 2 + rel) in self.PWD
        if k == KN.MISS_TB: return ((key[1] << SHK) | key[2]) in self.TYPB
        if k == KN.MISS_TW: return ((key[1] << SHK) | key[2]) in self.TYPW
        return False

    def grow_pairs(self):
        if self.NROW[0] >= self.NROW[1] - 1:
            cap = 2 * self.NROW[1]
            for nm in ('PR_V', 'PR_C'):
                a = getattr(self, nm); b = np.zeros((cap,) + a.shape[1:], a.dtype); b[:len(a)] = a; setattr(self, nm, b)
            self.NROW[1] = cap
        if self.NROW[2] >= self.NROW[3] - 1:
            cap = 2 * self.NROW[3]
            for nm in ('WC_V', 'WC_CV'):
                a = getattr(self, nm); b = np.zeros((cap,) + a.shape[1:], a.dtype); b[:len(a)] = a; setattr(self, nm, b)
            self.NROW[3] = cap
        self.fills['grow'] += 1

    def filled(self, key):
        if key[0] == KN.MISS_BROW: return self.A['BRI'][int(self.A['BCLS'][key[1]]), key[2]] >= 0
        return False

    def T(self):
        A = self.A
        vs = self.vs
        return (A['WSP'], A['WT1'], A['WCLS'], vs.READS_EQ, vs.VTR, vs.VK, vs.VA, vs.VC, vs.VOK, vs.VSTEPS, vs.VUSED,
                vs.VNU, self.BKA, F.M_CAP, 1 if 'EQ' in self.ev.live else 0,
                self.PRD, self.PR_V, self.PR_C, self.WCD, self.WC_V, self.WC_CV, self.NROW, self.CONSTC, self.CONSTV,
                A['BCLS'], A['BRI'], A['BRA'], A['B_ACT'], A['B_IDL'], A['B_CV'], self.ev.V, F.VPLUS, F.TO_CHARGE)

    def PT(self):
        A = self.A
        return (A['PBI'], A['PB_N'], A['PB_IDX'], A['PB_OWN'], A['PB_MASK'], A['PB_NEW'], A['B_PLAYOWN'],
                A['B_CALLM'], self.PWD, A['PW_N'], A['PW_IDX'], A['PW_OWN'], A['PW_MASK'], A['PW_NEW'], A['WPLAY'],
                A['BCLS'], A['BSP'], A['WCLS'], A['WSP'], self.TYPB, self.TYPW, 0 if self.cfg.get('gate') == 'opp' else 1)

    def prefill(self):
        out = np.zeros((1000000, 6), np.int64)
        while True:
            n = KN.collect_missing(self.I, self.npres, self.pres, self.T(), out, len(out))
            if n < 0:
                self.grow_pairs(); continue
            if n == 0: break
            seen = set()
            for k in range(min(n, len(out))):
                key = tuple(int(v) for v in out[k])
                if key in seen: continue
                seen.add(key)
                if self.filled(key): continue
                self.fill_miss(np.array(key + (0, 0), np.int64))
        live_eq = 1 if 'EQ' in self.ev.live else 0
        if self.mode_S and self.cfg.get('prefill_prod', False):
            # optional: production rows of every present triple (the kernel fills them on demand at little cost)
            while True:
                self.st[KN.ST_STATUS] = 0
                A = self.A
                KN.collect_prod_missing(self.I, self.npres, self.pres, self.T(), self.PT(), A['BLACK'], A['WLACK'],
                                        live_eq, self.ev.K, self.ev.P, F.VPLUS, F.PROD_W, self.mbuf, self.st)
                if self.st[KN.ST_STATUS] == 0: break
                self.fill_batch()
        self.save_shared()
        self.JQ = np.zeros((self.I, self.N + 1, self.N + 1, self.N + 1), np.uint8)
        KN.init_cube_F(self.I, self.counts, self.pres, self.npres, self.pos, self.F, self.JQ, PAYF, self.T(),
                       self.A['WACT'], self.A['TAG'], live_eq)

    def run(self, gens):
        checks = np.arange(CHECK_EVERY, gens + 1, CHECK_EVERY, dtype=np.int64)
        nchk = len(checks)
        I, N = self.I, self.N
        if self.snap is None:
            self.snap = (np.zeros((nchk + 1, I, 3, N + 1), np.int32), np.zeros((nchk + 1, I, 3, N + 1), np.int32),
                         np.zeros((nchk + 1, I, 3), np.int32))
            st, sc, sn = self.snap
            for i in range(I):
                for s in range(3):
                    sn[0, i, s] = self.npres[i, s]
                    for t in range(self.npres[i, s]):
                        k = self.pres[i, s, t]; st[0, i, s, t] = k; sc[0, i, s, t] = self.counts[i, s, k]
        else:
            st, sc, sn = self.snap
            add = nchk + 1 - st.shape[0]
            if add > 0:
                self.snap = (np.concatenate([st, np.zeros((add,) + st.shape[1:], np.int32)]),
                             np.concatenate([sc, np.zeros((add,) + sc.shape[1:], np.int32)]),
                             np.concatenate([sn, np.zeros((add,) + sn.shape[1:], np.int32)]))
        self.checks = checks
        cfg = self.cfg
        m = cfg['mN'] / N
        r_enc = N / 3.0 * cfg.get("r_mult", 1.0)
        live_eq = 1 if 'EQ' in self.ev.live else 0
        t0 = time.time()
        while True:
            A = self.A
            stv, scv, snv = self.snap
            status = KN.run_kernel(self.st, self.seed, I, N, 0.3, m, r_enc, self.checks, self.ev.K, self.ev.P,
                                   live_eq, self.mode_S, self.qmax, F.PROD_W,
                                   self.counts, self.pres, self.npres, self.pos, self.F, self.act, self.apos,
                                   self.quiet, self.nqlist, self.nqpos, self.T(), self.PT(), A['WACT'], A['TAG'],
                                   A['BLACK'], A['WLACK'], self.JQ, PAYF, self.ctr, self.miss, stv, scv, snv,
                                   self.maxiter, self.mbuf)
            if status == 0:
                break
            if status == 5:
                if self.debug: print('iter budget', self.st[:12].tolist(), self.ctr[16], flush=True)
                continue
            if status == 4:
                self.fill_batch()
                continue
            if status == 2:
                self.nmiss += 1
                self.fill_miss(self.miss.copy())
                continue
            raise RuntimeError('kernel status %d' % status)
        self.t_run += time.time() - t0
        self.save_shared()
        return self


# ----------------------------------------------------------------------------------------------------------------
# per-run statistics from snapshots (notes §1.8)
# ----------------------------------------------------------------------------------------------------------------
def play_index(c):
    """Play key index of a (joint code, tags) code c = 4 j + 2 t1 + t2: wage * 16 + a1 * 8 + a2 * 4 + wh1 * 2 + wh2."""
    j, t1, t2 = c // 4, (c // 2) % 2, c % 2
    b = j // 4; a1 = (j // 2) % 2; a2 = j % 2
    w, h = b // 3, b % 3
    wh1 = 1 if ((h == 0 and a1 == 1) or (h == 2 and t1 == 1)) else 0
    wh2 = 1 if ((h == 0 and a2 == 1) or (h == 2 and t2 == 1)) else 0
    return w * 16 + a1 * 8 + a2 * 4 + wh1 * 2 + wh2


PLAYIDX = np.array([play_index(c) for c in range(144)])
FAIR_KEY = 2 * 16
PRODUCTIVE = np.array([1 if ((c // 4) // 2) % 2 == 0 and (c // 4) % 2 == 0 and
                       not (PLAYIDX[c] & 3) else 0 for c in range(144)], float)


def snap_comp(run, ci, i, s):
    st, sc, sn = run.snap
    n = int(sn[ci, i, s])
    return st[ci, i, s, :n].astype(np.int64), sc[ci, i, s, :n].astype(np.int64)


def island_dist(run, ci, i):
    t0, c0 = snap_comp(run, ci, i, 0); t1, c1 = snap_comp(run, ci, i, 1); t2, c2 = snap_comp(run, ci, i, 2)
    out = np.zeros((36, 2, 2))
    while True:
        ok = KN.comp_dist(t0, c0, len(t0), t1, c1, len(t1), t2, c2, len(t2), run.T(), run.A['WACT'], run.A['TAG'],
                          1 if 'EQ' in run.ev.live else 0, out)
        if ok: break
        # a boss row not tabled (a type present only between events): fill and retry
        out[:] = 0
        m = np.zeros(8, np.int64)
        oi = np.zeros(10, np.int64); oc = np.zeros(15, np.int64)
        filled = False
        for b in t0:
            for x in t1:
                for y in t2:
                    if not KN.chain(int(b), int(x), int(y), run.T(), oi, oc, m):
                        if m[0] == 8: run.grow_pairs()
                        else: run.fill_miss(m.copy())
                        filled = True
                        break
                if filled: break
            if filled: break
    return out.reshape(-1)


def modal_type(run, ci, i, s):
    t, c = snap_comp(run, ci, i, s)
    if len(t) == 0: return -1
    return int(t[int(np.argmax(c))])


class RunStats:
    """Island plays per check and the run's statistics."""

    def __init__(self, run):
        self.run = run
        st, sc, sn = run.snap
        self.nck = int(run.st[KN.ST_CI]) + 1
        I = run.I
        self.play = np.zeros((self.nck, I), np.int64)
        self.fair = np.zeros((self.nck, I), bool)
        self.prodeff = np.zeros((self.nck, I))
        self.wage = np.zeros((self.nck, I), np.int64)
        for ci in range(self.nck):
            for i in range(I):
                d = island_dist(run, ci, i)
                pk = np.bincount(PLAYIDX, weights=d, minlength=48)
                k = int(np.argmax(pk))
                self.play[ci, i] = k
                self.fair[ci, i] = (k == FAIR_KEY)
                self.wage[ci, i] = k // 16
                self.prodeff[ci, i] = float((d * PRODUCTIVE).sum())

    def at_gen(self, g):
        return min(g // CHECK_EVERY, self.nck - 1)


def holder_class(run, ev, xpid, cache):
    """'open' (strikes against a certified pay(0, none) beside a scab), 'greenbeard' (strikes beside an exact copy,
    works beside a scab), 'unconditional' (neither)."""
    if xpid in cache: return cache[xpid]
    g = ev.g
    W, B = g.roles['W'], g.roles['B']
    sp0 = B['spellings'].index(F.NAMED_B['pay(0,none)'])
    pay0 = ev.reg.get('B', sp0, F.full_inv(g, 'B', int(B['tau'][sp0])))
    sps = W['spellings'].index(F.NAMED_W['scab'])
    scab = ev.reg.get('W', sps, F.full_inv(g, 'W', int(W['tau'][sps])))
    a_scab = ev.triple(pay0, xpid, scab)['a1']
    a_copy = ev.triple(pay0, xpid, xpid)['a1']
    r = 'open' if a_scab == 'D' else ('greenbeard' if a_copy == 'D' else 'unconditional')
    cache[xpid] = r
    return r


def named_pid(ev, role, name, inv='full'):
    g = ev.g
    r = g.roles[role]
    x = (F.NAMED_W if role == 'W' else F.NAMED_B)[name]
    sp = r['spellings'].index(x)
    tk = int(r['tau'][sp])
    return ev.reg.get(role, sp, F.full_inv(g, role, tk) if inv == 'full' else inv)


def closed_shop(ev, bpid, cache):
    cb = ev.canon(bpid)
    if cb in cache: return cache[cb]
    t1 = named_pid(ev, 'W', 'T1'); t1p = named_pid(ev, 'W', 'T1p')
    w1 = ev.triple(bpid, t1, t1)['boss'] // 3
    w2 = ev.triple(bpid, t1p, t1p)['boss'] // 3
    r = (w1 == 2 and w2 < 2)
    cache[cb] = r
    return r


def fair_play(tr):
    b = tr['boss']
    return b // 3 == 2 and tr['a1'] == 'C' and tr['a2'] == 'C'


_PRODINV = {}


def summarize(run, ev_sham=None, horizon=2000, rng=None):
    """Statistics of one run at the horizon (and at the end of an extension, if any)."""
    rng = rng or np.random.default_rng(run.rep)
    ev = run.ev
    RS = RunStats(run)
    I = run.I
    out = {}
    fairany = RS.fair.any(axis=1)
    est = int(np.argmax(fairany)) if fairany.any() else -1
    out['established'] = bool(fairany.any())
    out['est_gen'] = est * CHECK_EVERY if est >= 0 else None
    for tag, g in (('h', horizon), ('end', (RS.nck - 1) * CHECK_EVERY)):
        ci = RS.at_gen(g)
        out[tag] = dict(gen=ci * CHECK_EVERY, persistence=float(RS.fair[ci].mean()),
                        wage=[float((RS.wage[ci] == w).mean()) for w in range(3)],
                        prodeff=float(RS.prodeff[ci].mean()),
                        strike_any=float(np.mean([(k // 4) % 4 != 0 for k in RS.play[ci]])))
    ci = RS.at_gen(horizon)
    # holders of fair islands, closed shops, identity islands
    hc = {}; cs = {}
    holders = defaultdict(int); holder_sp = defaultdict(int); holders_detail = defaultdict(int)
    gb_boss = defaultdict(int)
    fair_modal = []
    ident = 0; heldfair = 0
    A = run.A
    for i in range(I):
        bt, xt, yt = (modal_type(run, ci, i, s) for s in range(3))
        if bt < 0 or xt < 0 or yt < 0: continue
        bp, xp, yp = run.btypes[bt], run.wtypes[xt], run.wtypes[yt]
        if RS.fair[ci, i]:
            heldfair += 1
            fair_modal.append((ev.reg[bp].sp, ev.reg[bp].inv, ev.reg[xp].sp, ev.reg[xp].inv, ev.reg[yp].sp, ev.reg[yp].inv))
            c1 = holder_class(run, ev, xp, hc); c2 = holder_class(run, ev, yp, hc)
            if c1 == 'greenbeard' and c2 == 'greenbeard' and ev.reg[xp].sp == ev.reg[yp].sp: k = 'greenbeard union'
            elif 'open' in (c1, c2) and 'greenbeard' in (c1, c2): k = 'mixture'
            elif 'open' in (c1, c2): k = 'open militants'
            else: k = 'unconditional'
            holders[k] += 1
            if k in ('greenbeard union', 'mixture'):
                pi_, ii_ = ev.boss_reads(bp)
                gb_boss['%s: boss %s' % (k, 'reads probes' if pi_ else 'reads no worker certificate')] += 1
                gb = xp if c1 == 'greenbeard' else yp
                tgb = ev.g.roles['W']['dts'][ev.reg[gb].tk]
                reads_eq = any(a[0] == 'E' for a in F.dt_atoms(tgb)) and 'EQ' in ev.live
                holders_detail[k + (' (identity)' if reads_eq else ' (pact)')] += 1
            else:
                holders_detail[k] += 1
            holder_sp[(F.show(ev.g.roles['W']['spellings'][ev.reg[xp].sp]),
                       F.show(ev.g.roles['W']['spellings'][ev.reg[yp].sp]))] += 1
            if ev_sham is not None:
                sb = ev_sham.reg.get('B', ev.reg[bp].sp, ev.reg[bp].inv)
                sx = ev_sham.reg.get('W', ev.reg[xp].sp, ev.reg[xp].inv)
                sy = ev_sham.reg.get('W', ev.reg[yp].sp, ev.reg[yp].inv)
                t_ = ev.triple(bp, xp, yp); ts = ev_sham.triple(sb, sx, sy)
                if (t_['boss'], t_['a1'], t_['a2']) != (ts['boss'], ts['a1'], ts['a2']):
                    ident += 1
    out['holders'] = dict(holders)
    out['holders_detail'] = dict(holders_detail)
    out['fair_modal'] = fair_modal
    out['greenbeard_bosses'] = dict(gb_boss)
    # self-play-only scripts held at the horizon (S modes): worker inventories with a script not producible at a
    # non-self root (notes §1.2, Claim N3)
    if run.mode_S:
        spo = 0; nind = 0
        for i in range(I):
            for s_ in (1, 2):
                t, c = snap_comp(run, ci, i, s_)
                for tt, cc in zip(t, c):
                    pr = ev.reg[run.wtypes[int(tt)]]
                    key = pr.tk
                    if key not in _PRODINV: _PRODINV[key] = producible_inv(ev.g, key)
                    pinv = _PRODINV[key]
                    if any(not set(a) <= set(b) for a, b in zip(pr.inv, pinv)):
                        spo += cc
                    nind += cc
        out['spo_held'] = dict(individuals=int(spo), of=int(nind))
    out['holder_spellings'] = {'%s | %s' % k: v for k, v in sorted(holder_sp.items(), key=lambda z: -z[1])[:8]}
    out['identity_islands'] = ident / I if ev_sham is not None else None
    # closed-shop share of the boss slot (pooled individuals)
    tot = 0; csn = 0
    for i in range(I):
        t, c = snap_comp(run, ci, i, 0)
        for tt, cc in zip(t, c):
            tot += cc
            if 'N1' in ev.live and closed_shop(ev, run.btypes[int(tt)], cs): csn += cc
    out['closed_shop_share'] = csn / max(tot, 1)
    # B_eq invasion fitness at the horizon's resident modal triples (unconditional)
    if 'N1' in ev.live or ev.g.gram == 'id':
        beq = named_pid(ev, 'B', 'B_eq', inv='full')
        sig = defaultdict(int)
        sig_t1 = defaultdict(int)
        for i in range(I):
            bt, xt, yt = (modal_type(run, ci, i, s) for s in range(3))
            if min(bt, xt, yt) < 0: continue
            bp, xp, yp = run.btypes[bt], run.wtypes[xt], run.wtypes[yt]
            tr0 = ev.triple(bp, xp, yp); tr1 = ev.triple(beq, xp, yp)
            p0 = PAY[4 * tr0['boss'] + 2 * (tr0['a1'] == 'D') + (tr0['a2'] == 'D'), 0, 0, 0]
            p1 = PAY[4 * tr1['boss'] + 2 * (tr1['a1'] == 'D') + (tr1['a2'] == 'D'), 0, 0, 0]
            sgn = 'pos' if p1 > p0 + 1e-12 else ('neg' if p1 < p0 - 1e-12 else 'zero')
            sig[sgn] += 1
            if ev.reg[xp].isT1 and ev.reg[yp].isT1: sig_t1[sgn] += 1
        out['beq_invasion'] = dict(sig); out['beq_invasion_T1T1'] = dict(sig_t1)
    # exits of fair islands
    exits = defaultdict(int)
    for i in range(I):
        fs = RS.fair[:ci + 1, i]
        if not fs.any(): continue
        c0 = int(np.argmax(fs))
        later = np.nonzero(~fs[c0:])[0]
        if len(later) == 0: continue
        c1 = c0 + int(later[0])
        mb0, mb1 = modal_type(run, c1 - 1, i, 0), modal_type(run, c1, i, 0)
        mw = [(modal_type(run, c0, i, s), modal_type(run, c1 - 1, i, s), modal_type(run, c1, i, s)) for s in (1, 2)]
        drift = any(w[0] != w[1] for w in mw)
        boss_change = mb0 != mb1
        wexit = any(w[1] != w[2] for w in mw)
        inv_only = False
        for s, w in zip((1, 2), mw):
            if w[1] != w[2] and w[1] >= 0 and w[2] >= 0 and ev.reg[run.wtypes[w[1]]].sp == ev.reg[run.wtypes[w[2]]].sp:
                inv_only = True
        if boss_change and drift: k = 'unread-slot drift then boss cut'
        elif boss_change: k = 'boss cut'
        elif inv_only: k = 'inventory change (production)'
        elif wexit or drift: k = 'worker drift'
        else: k = 'composition (non-modal)'
        # executable vs ideal at the exit's modal triple
        bt, xt, yt = mb1, mw[0][2], mw[1][2]
        if min(bt, xt, yt) >= 0:
            tr = ev.triple(run.btypes[bt], run.wtypes[xt], run.wtypes[yt])
            if (tr['boss'], tr['a1'], tr['a2']) != tr['ideal']: k += ' [timeout-changed]'
        exits[k] += 1
    out['exits'] = dict(exits)
    # cross-island P(fair) and union compatibility
    nfair = 0; ns = 600
    for _ in range(ns):
        a, b, c = rng.choice(I, 3, replace=False)
        tb = snap_comp(run, ci, a, 0); t1 = snap_comp(run, ci, b, 1); t2 = snap_comp(run, ci, c, 2)
        bt = int(rng.choice(tb[0], p=tb[1] / tb[1].sum())); xt = int(rng.choice(t1[0], p=t1[1] / t1[1].sum()))
        yt = int(rng.choice(t2[0], p=t2[1] / t2[1].sum()))
        nfair += fair_play(ev.triple(run.btypes[bt], run.wtypes[xt], run.wtypes[yt]))
    out['cross_fair'] = nfair / ns
    fi = np.nonzero(RS.fair[ci])[0]
    comp = []
    for _ in range(min(200, len(fi) * (len(fi) - 1))):
        a, b = rng.choice(fi, 2, replace=False)
        bt = modal_type(run, ci, a, 0); xt = modal_type(run, ci, a, 1); yt = modal_type(run, ci, b, 2)
        comp.append(fair_play(ev.triple(run.btypes[bt], run.wtypes[xt], run.wtypes[yt])))
    out['union_compat'] = float(np.mean(comp)) if comp else None
    # timeouts and costs on sampled encounters at 0, 50, 200 and the horizon
    out['encounters'] = {}
    for g in (0, 50, 200, horizon):
        cj = RS.at_gen(g)
        n_to = 0; rows = []
        for _ in range(300):
            i = int(rng.integers(I))
            tb = snap_comp(run, cj, i, 0); t1 = snap_comp(run, cj, i, 1); t2 = snap_comp(run, cj, i, 2)
            bt = int(rng.choice(tb[0], p=tb[1] / tb[1].sum())); xt = int(rng.choice(t1[0], p=t1[1] / t1[1].sum()))
            yt = int(rng.choice(t2[0], p=t2[1] / t2[1].sum()))
            bp, xp, yp = run.btypes[bt], run.wtypes[xt], run.wtypes[yt]
            tr = ev.triple(bp, xp, yp)
            n_to += tr['todiff']
            play = sum(tr['steps'])
            prod = 0; outc = []
            if run.mode_S:
                for pid, npid, rec in ev.productions(bp, xp, yp, tr, gate=run.cfg.get('gate') != 'opp'):
                    for r in rec:
                        if r[0] == 'refused': outc.append('refused'); continue
                        prod += r[3]; outc.append(r[1])
            req = sum(c for c in tr['bcost'] + tr['wcost'] if c is not None)
            rows.append((play, prod, req, outc))
        out['encounters'][g] = dict(todiff=n_to / 300, play_median=float(np.median([r[0] for r in rows])),
                                    prod_median=float(np.median([r[1] for r in rows])),
                                    total_median=float(np.median([r[0] + r[1] for r in rows])),
                                    rows=[(int(a), int(b), int(c), o) for a, b, c, o in rows])
    out['ctr'] = run.ctr.tolist()
    out['fills'] = dict(run.fills)
    out['ntypes'] = (len(run.btypes), len(run.wtypes))
    out['fair_t'] = RS.fair.mean(axis=1).tolist()
    out['wage_t'] = [[float((RS.wage[c] == w).mean()) for w in range(3)] for c in range(RS.nck)]
    return out, RS


# ----------------------------------------------------------------------------------------------------------------
# cells (notes §1.11, §1.12), forced coalitions, assays
# ----------------------------------------------------------------------------------------------------------------
HORIZON = 2000
EXTEND = 10000
CELLS = {
    'H_noeq': dict(arm='noeq', mode='H'),
    'H_eq': dict(arm='eq', mode='H'),
    'H_sham': dict(arm='sham', mode='H'),
    'H_eqnoT': dict(arm='eqnoT', mode='H'),
    'S_noeq': dict(arm='noeq', mode='S'),
    'S_eq': dict(arm='eq', mode='S'),
    'S_eq_N200': dict(arm='eq', mode='S', N=200, runs=20),
    'S_opp': dict(arm='eq', mode='S', gate='opp', runs=20),
    'S_sham': dict(arm='sham', mode='S', runs=20),
    'S_eq_forced_empty': dict(arm='eq', mode='S', forced='empty', runs=20),
    'S_eq_forced_pre': dict(arm='eq', mode='S', forced='pre', runs=20),
    'H_noeq_ideal': dict(arm='noeq', mode='H', K=10 ** 12, runs=20),
}


def path_script(ev, role, x, A, values, eq=False):
    """The H-list index of the script of template x for set A on the path given by values (atom -> bool)."""
    t = F.dt(x)
    idv = lambda nm: eq if nm == 'EQ' else False
    sc, _ = F.sym_prod3(t, role, A, idv, lambda a: 'T' if values[a] else 'F')
    _, per = F.h_list(t, role)
    return per[A].index(sc)


def coalition(ev, preload):
    """(boss (sp, inv), w1 (sp, inv), w2 (sp, inv)) of the fair coalition (D*, T1, T1), empty or preloaded."""
    g = ev.g
    xb, xw = F.NAMED_B['D*'], F.NAMED_W['T1']
    spb = g.roles['B']['spellings'].index(xb); spw = g.roles['W']['spellings'].index(xw)
    if not preload:
        return (spb, F.empty_inv('B')), (spw, F.empty_inv('W')), (spw, F.empty_inv('W'))
    half = {F.P1_14S[1]: True, F.P1_0S[1]: False}
    zero = {F.P1_14S[1]: False, F.P1_0S[1]: False}
    binv = ((path_script(ev, 'B', xb, F.A_GE14, half),), (path_script(ev, 'B', xb, F.A_EQ12, half),),
            (path_script(ev, 'B', xb, F.A_LE14, zero),))
    winv = ((path_script(ev, 'W', xw, F.A_WORK, {F.B12[1]: True}),),
            (path_script(ev, 'W', xw, F.A_STRIKE, {F.B12[1]: False}),))
    return (spb, binv), (spw, winv), (spw, winv)


def cell_cfg(name):
    c = dict(CELLS[name])
    c.setdefault('N', 100); c.setdefault('I', 64); c.setdefault('mN', 1.0); c.setdefault('runs', 40)
    c['name'] = name
    return c


_EVK = {}


def evaluator_k(arm, mode, K):
    key = (arm, mode, K)
    if key not in _EVK:
        _EVK[key] = F.Evaluator(grammar(F.ARMS[arm][0]), arm, mode, K=K)
    return _EVK[key]


def cell_job(args):
    name, rep, extend = args
    cfg = cell_cfg(name)
    load_costc()
    K = cfg.get('K', F.K_MAIN)
    ev = evaluator_k(cfg['arm'], cfg['mode'], K)
    if cfg.get('forced'):
        cfg['forced'] = coalition(ev, cfg['forced'] == 'pre')
    sham = evaluator_k('sham', cfg['mode'], K) if ev.g.gram == 'id' and cfg['arm'] != 'sham' else None
    t0 = time.time()
    run = Run(ev, cfg, rep)
    run.prefill()
    t1 = time.time()
    run.run(HORIZON)
    t2 = time.time()
    summ, RS = summarize(run, ev_sham=sham, horizon=HORIZON)
    out = dict(cell=name, rep=rep, summary=summ, time=dict(prefill=t1 - t0, run=t2 - t1, summary=time.time() - t2))
    if extend:
        t3 = time.time()
        run.run(EXTEND)
        RS = RunStats(run)
        ci = RS.nck - 1
        end = dict(gen=ci * CHECK_EVERY, persistence=float(RS.fair[ci].mean()),
                   wage=[float((RS.wage[ci] == w).mean()) for w in range(3)], prodeff=float(RS.prodeff[ci].mean()),
                   strike_any=float(np.mean([(k // 4) % 4 != 0 for k in RS.play[ci]])))
        out['summary_ext'] = dict(end=end, fair_t=RS.fair.mean(axis=1)[::10].tolist(),
                                  wage_t=[[float((RS.wage[c] == w).mean()) for w in range(3)] for c in range(0, RS.nck, 10)],
                                  ctr=run.ctr.tolist())
        out['time']['ext'] = time.time() - t3
    d = os.path.join(OUT, 'cell_' + name)
    os.makedirs(d, exist_ok=True)
    json.dump(out, open(os.path.join(d, 'rep_%03d.json' % rep), 'w'), default=str)
    ev.maybe_clear(0)
    return name, rep, out['time']


def lottery(args):
    from multiprocessing import get_context
    names = args.cells.split(',')
    jobs = []
    for nm in names:
        cfg = cell_cfg(nm)
        nruns = args.runs if args.runs else cfg['runs']
        for rep in range(nruns):
            f = os.path.join(OUT, 'cell_' + nm, 'rep_%03d.json' % rep)
            if os.path.exists(f): continue
            jobs.append((nm, rep, bool(args.extend)))
    print('jobs', len(jobs), flush=True)
    with get_context('fork').Pool(args.procs, maxtasksperchild=args.maxtasks) as pool:
        for nm, rep, tm in pool.imap_unordered(cell_job, jobs, chunksize=1):
            print(nm, rep, json.dumps({k: round(v, 1) for k, v in tm.items()}), time.strftime('%H:%M:%S'), flush=True)


# ----------------------------------------------------------------------------------------------------------------
# static tables (notes §1.3, §1.5, §1.6; spec "Static" and "Scale guard"), on the ideal semantics (K = 10^12) unless
# stated; executable plays at K in {3e5, 1e6, 3e6} on the same sampled triples
# ----------------------------------------------------------------------------------------------------------------
ID_POS = {'N1': 8, 'N2': 9, 'EQW': 10}
KBIG = 10 ** 12


def boss_groups(ev):
    """Boss run trees grouped by (read positions in the 11-bit code, action table over the read bits, has identity
    atom): arrays (R (G, 3), TAB (G, 8), MASS (G), HASID (G)).  Identity atoms not live in the arm read False."""
    g = ev.g
    B = g.roles['B']
    m = g.mass('B')
    tkmass = np.bincount(B['tau'], weights=m, minlength=len(B['dts']))
    groups = defaultdict(float)
    live = ev.live
    for tk, t in enumerate(B['dts']):
        ats = F.dt_atoms(t)
        pos = sorted(set(ID_POS[a[1]] if a[0] == 'E' else F.PROBE_ATOMS.index(a) for a in ats))
        assert len(pos) <= 3
        tab = []
        for bits in range(1 << len(pos)):
            vals = {p: (bits >> q) & 1 for q, p in enumerate(pos)}

            def val(a):
                if a[0] == 'E':
                    return bool(vals[ID_POS[a[1]]]) and a[1] in live
                return bool(vals[F.PROBE_ATOMS.index(a)])
            tab.append(int(F.dt_eval(t, val)))
        hasid = any(a[0] == 'E' for a in ats)
        groups[(tuple(pos), tuple(tab), hasid)] += tkmass[tk]
    G = len(groups)
    R = -np.ones((G, 3), np.int64); TAB = np.zeros((G, 8), np.int64); MASS = np.zeros(G); HASID = np.zeros(G, bool)
    for gi, ((pos, tab, hasid), mm) in enumerate(groups.items()):
        R[gi, :len(pos)] = pos; TAB[gi, :len(tab)] = tab; MASS[gi] = mm; HASID[gi] = hasid
    return R, TAB, MASS, HASID


def act_mass(BG, code_bits):
    """Boss prior mass per action (9) at an 11-bit code, all bosses and identity-free bosses."""
    R, TAB, MASS, HASID = BG
    cb = np.append(np.asarray(code_bits, np.int64), 0)          # index -1 -> 0
    idx = cb[R[:, 0]] + 2 * cb[R[:, 1]] + 4 * cb[R[:, 2]]
    act = TAB[np.arange(len(TAB)), idx]
    return np.bincount(act, weights=MASS, minlength=9), np.bincount(act[~HASID], weights=MASS[~HASID], minlength=9)


def code_bits(ev, x, y):
    ev.probe(x, y)
    pv = ev._probe_ideal[(x, y)]
    px, py = ev.reg[x], ev.reg[y]
    return [1 if v == 'T' else 0 for v in pv] + [int(px.isT1), int(py.isT1), int(px.sp == py.sp)]


def const_pids(ev):
    g = ev.g
    B = g.roles['B']
    out = {}
    for sp, x in enumerate(B['spellings']):
        if x[0] == 'L':
            out[int(x[1])] = ev.reg.get('B', sp, F.full_inv(g, 'B', int(B['tau'][sp])))
    assert sorted(out) == list(range(9))
    return out


def producible_inv(g, tk):
    """Worker inventory of every script PROD3 can write at a non-self root (EQ false), over every box assignment."""
    t = g.roles['W']['dts'][tk]
    _, per = g.hlist('W', tk)
    boxes = [a for a in F.dt_atoms(t) if a[0] != 'E']
    inv = []
    for A in F.FAM['W']:
        got = set()
        for bits in range(1 << len(boxes)):
            vals = {a: ('T' if (bits >> q) & 1 else 'F') for q, a in enumerate(boxes)}
            sc, _ = F.sym_prod3(t, 'W', A, lambda n: False, lambda a: vals[a])
            if sc is not None:
                got.add(per[A].index(sc))
        inv.append(tuple(sorted(got)))
    return tuple(inv)


def pair_eval(ev, x, y, consts, BG):
    """Per worker pair: boss mass per action (all / identity-free), worker responses to each constant action, the
    fair actions that are uninvadable (no constant earns the boss more than 1)."""
    cb = code_bits(ev, x, y)
    M, M0 = act_mass(BG, cb)
    g = ev.g
    W = g.roles['W']
    t1 = 1 if F.tagged(W['dts'][ev.reg[x].tk]) else 0
    t2 = 1 if F.tagged(W['dts'][ev.reg[y].tk]) else 0
    ub = np.zeros(9); fair = np.zeros(9, bool)
    for a in range(9):
        tr = ev.triple(consts[a], x, y)
        J = 4 * a + 2 * (tr['a1'] == 'D') + (tr['a2'] == 'D')
        ub[a] = PAY[J, t1, t2, 0]
        fair[a] = UN.summary(int(J), t1, t2) == 0
    ok = fair & (ub.max() <= 1.0 + 1e-12)
    return float(M[ok].sum()), float(M0[ok].sum()), float(M.sum())


def coalition_mass(ev, BG, consts, rng, n, inv_fn=None, no_id_workers=False):
    """Founding-coalition mass (notes §1.5): distinct worker spellings by Monte Carlo (n pairs from mu_W^2 given
    x != y), copies exactly; inv_fn(tk) the worker inventory (default: the full H list)."""
    g = ev.g
    W = g.roles['W']
    mw = g.mass('W')
    cum = np.cumsum(mw)
    hasEQ = np.array([any(a[0] == 'E' for a in F.dt_atoms(W['dts'][W['tau'][s]])) for s in range(len(mw))])
    inv_fn = inv_fn or (lambda tk: F.full_inv(g, 'W', tk))
    pidc = {}

    def wp(sp):
        if sp not in pidc:
            pidc[sp] = ev.reg.get('W', sp, inv_fn(int(W['tau'][sp])))
        return pidc[sp]
    pcopy = float((mw ** 2).sum())
    vals, vals0 = [], []
    k = 0
    while k < n:
        a, b = (min(int(np.searchsorted(cum, rng.random() * cum[-1])), len(mw) - 1) for _ in range(2))
        if a == b: continue
        m, m0, _ = pair_eval(ev, wp(a), wp(b), consts, BG)
        vals.append(m); vals0.append(m0 if not (hasEQ[a] or hasEQ[b]) else 0.0)
        k += 1
    vals, vals0 = np.array(vals), np.array(vals0)
    cop = cop0 = 0.0
    for s in range(len(mw)):
        m, m0, _ = pair_eval(ev, wp(s), wp(s), consts, BG)
        cop += mw[s] ** 2 * m
        if not hasEQ[s]: cop0 += mw[s] ** 2 * m0
    dist = (1 - pcopy) * vals.mean(); dist0 = (1 - pcopy) * vals0.mean()
    se = (1 - pcopy) * vals.std() / np.sqrt(n); se0 = (1 - pcopy) * vals0.std() / np.sqrt(n)
    return dict(total=dist + cop, se=se, distinct=dist, copies=cop, identity_free=dist0 + cop0, identity_free_se=se0,
                copy_prob=pcopy, n_pairs=n, pairs_with_coalition=int((vals > 0).sum()))


def worker_families(ev):
    """Prior mass of open militants, greenbeards and unconditional workers (holder classification, notes §1.8)."""
    g = ev.g
    W = g.roles['W']
    mw = g.mass('W')
    cache = {}
    out = defaultdict(float); n = defaultdict(int)
    for sp in range(len(mw)):
        x = ev.reg.get('W', sp, F.full_inv(g, 'W', int(W['tau'][sp])))
        c = holder_class(None, ev, x, cache)
        out[c] += mw[sp]; n[c] += 1
    return dict(mass=dict(out), spellings=dict(n))


def boss_families(ev, BG):
    t1, t1p, sc = named_pid(ev, 'W', 'T1'), named_pid(ev, 'W', 'T1p'), named_pid(ev, 'W', 'scab')
    R, TAB, MASS, HASID = BG

    def acts(x, y):
        cb = np.append(np.asarray(code_bits(ev, x, y), np.int64), 0)
        idx = cb[R[:, 0]] + 2 * cb[R[:, 1]] + 4 * cb[R[:, 2]]
        return TAB[np.arange(len(TAB)), idx] // 3
    w_t1, w_t1p, w_sc = acts(t1, t1), acts(t1p, t1p), acts(sc, sc)
    closed = (w_t1 == 2) & (w_t1p < 2)
    conc = (w_t1 == 2) & (w_sc < 2)
    return dict(closed_shop=float(MASS[closed].sum()), concession=float(MASS[conc].sum()),
                closed_shop_and_concession=float(MASS[closed & conc].sum()),
                pays_half_to_T1_pair=float(MASS[w_t1 == 2].sum()), groups=len(MASS))


def responds_like_constant(ev, BG, consts, rng, n=300):
    """Check of the static shortcut: a boss's play against (x, y) equals its action's constant's play."""
    g = ev.g
    mw, mb = g.mass('W'), g.mass('B')
    cw, cbm = np.cumsum(mw), np.cumsum(mb)
    W, B = g.roles['W'], g.roles['B']
    agree = 0
    bad = []
    for _ in range(n):
        xs = [min(int(np.searchsorted(cw, rng.random())), len(mw) - 1) for _ in range(2)]
        bs = min(int(np.searchsorted(cbm, rng.random())), len(mb) - 1)
        x, y = (ev.reg.get('W', s, F.full_inv(g, 'W', int(W['tau'][s]))) for s in xs)
        b = ev.reg.get('B', bs, F.full_inv(g, 'B', int(B['tau'][bs])))
        tr = ev.triple(b, x, y)
        tc = ev.triple(consts[tr['boss']], x, y)
        ok = (tr['a1'], tr['a2']) == (tc['a1'], tc['a2'])
        agree += ok
        if not ok and len(bad) < 5:
            bad.append((F.show(B['spellings'][bs]), F.show(W['spellings'][xs[0]]), F.show(W['spellings'][xs[1]]),
                        tr['boss'], tr['a1'], tr['a2'], tc['a1'], tc['a2']))
    return dict(n=n, agree=agree, examples=bad)


def universe(g, rng, nb=3000):
    W, B = g.roles['W'], g.roles['B']
    wtot = 0
    for tk in range(len(W['dts'])):
        _, per = g.hlist('W', tk)
        k = 1
        for A in F.FAM['W']: k *= len(per[A]) + 1
        wtot += k
    sample = rng.sample(range(len(B['dts'])), min(nb, len(B['dts'])))
    bs = []
    for tk in sample:
        _, per = g.hlist('B', tk)
        k = 1
        for A in F.FAM['B']: k *= len(per[A]) + 1
        bs.append(k)
    return dict(worker_types_per_spelling_sum=None, worker_run_tree_inventories=int(wtot),
                boss_run_tree_inventories_est=float(np.mean(bs) * len(B['dts'])),
                boss_inventories_per_run_tree_mean=float(np.mean(bs)), boss_sampled=len(sample))


def cost_sample(rng, n=1500):
    """Per-encounter costs on L-weighted triples (eq grammar, H inventories): required (uncensored) play steps per
    participant (K = 10^12 evaluator), the required production steps of writing each set from an empty inventory at
    the same encounter, and the executable plays at K in {3e5, 1e6, 3e6}."""
    evb = evaluator_k('eq', 'S', KBIG)
    evk = {K: evaluator_k('eq', 'S', K) for K in (3 * 10 ** 5, 10 ** 6, 3 * 10 ** 6)}
    g = evb.g
    W, B = g.roles['W'], g.roles['B']
    mw, mb = g.mass('W'), g.mass('B')
    cw, cbm = np.cumsum(mw), np.cumsum(mb)
    rows = []
    t0 = time.time()
    for it in range(n):
        xs = [min(int(np.searchsorted(cw, rng.random())), len(mw) - 1) for _ in range(2)]
        bs = min(int(np.searchsorted(cbm, rng.random())), len(mb) - 1)
        ids = {}
        for ev in [evb] + list(evk.values()):
            x, y = (ev.reg.get('W', s, F.full_inv(g, 'W', int(W['tau'][s]))) for s in xs)
            b = ev.reg.get('B', bs, F.full_inv(g, 'B', int(B['tau'][bs])))
            ids[id(ev)] = (b, x, y)
        b, x, y = ids[id(evb)]
        tr = evb.triple(b, x, y)
        play = list(tr['steps'])
        # production from empty at this encounter (required steps; the gate refuses workers beside a copy)
        prod = [0, 0, 0]
        be = evb.reg.get('B', bs, F.empty_inv('B'))
        for si, idx, own, calls in evb.prod_boss(be, tr['code']):
            prod[0] += own + sum(tr['pcost'][c] for c in calls)
        if not tr['rel']:
            for jj, s, oc, od in ((1, xs[0], 2, 3), (2, xs[1], 0, 1)):
                we = evb.reg.get('W', s, F.empty_inv('W'))
                oex = (tr['wex'][oc], tr['wex'][od])
                cc = list(tr['bchg']) + [tr['wchg'][oc], tr['wchg'][od]]
                for si, idx, own, calls in evb.prod_worker(we, jj, tr['bex'], oex, bool(tr['rel'])):
                    prod[jj] += own + sum(cc[c] for c in calls)
        ideal = (tr['boss'], tr['a1'], tr['a2'])
        exe = {}
        for K, ev in evk.items():
            tk = ev.triple(*ids[id(ev)])
            exe[K] = (tk['boss'], tk['a1'], tk['a2']) != ideal
        allc = list(tr['bcost']) + list(tr['wcost']) + list(tr['pcost'])
        ito = any(c is None or c >= KBIG // 4 for c in allc)
        maxcheck = max([c for c in allc if c is not None] + [0])
        rows.append(dict(play=play, prod=prod, differs=exe, maxcheck=maxcheck, rel=bool(tr['rel']), ideal_to=ito))
        for ev in [evb] + list(evk.values()): ev.maybe_clear()
    P = np.array([r['play'] for r in rows], float); Q = np.array([r['prod'] for r in rows], float)
    tot = P + Q
    enc_play, enc_tot = P.sum(1), tot.sum(1)
    out = dict(n=n, time_s=time.time() - t0, ideal_regress_triples=int(sum(r['ideal_to'] for r in rows)))
    out['median_encounter_play'] = float(np.median(enc_play)); out['median_encounter_play_plus_prod'] = float(np.median(enc_tot))
    out['median_ratio'] = float(np.median(enc_tot) / max(np.median(enc_play), 1))
    out['quantiles_participant_play'] = {str(q): float(np.quantile(P, q)) for q in (0.5, 0.9, 0.99, 1.0)}
    out['quantiles_participant_prod'] = {str(q): float(np.quantile(Q, q)) for q in (0.5, 0.9, 0.99, 1.0)}
    out['quantiles_encounter_total'] = {str(q): float(np.quantile(enc_tot, q)) for q in (0.5, 0.9, 0.99, 1.0)}
    nr = np.array([not r['ideal_to'] for r in rows])
    out['no_regress'] = dict(
        n=int(nr.sum()),
        median_encounter_play=float(np.median(enc_play[nr])), median_encounter_play_plus_prod=float(np.median(enc_tot[nr])),
        quantiles_participant_play={str(q): float(np.quantile(P[nr], q)) for q in (0.5, 0.9, 0.99, 1.0)},
        quantiles_participant_prod={str(q): float(np.quantile(Q[nr], q)) for q in (0.5, 0.9, 0.99, 1.0)},
        quantiles_encounter_total={str(q): float(np.quantile(enc_tot[nr], q)) for q in (0.5, 0.9, 0.99, 1.0)},
        over_K={str(K): dict(play=float((P[nr] > K).any(1).mean()), play_plus_prod=float((tot[nr] > K).any(1).mean()))
                for K in (3 * 10 ** 5, 10 ** 6, 3 * 10 ** 6)})
    out['rows'] = [(r['play'], r['prod'], r['ideal_to'], {str(k): v for k, v in r['differs'].items()}) for r in rows]
    for K in (3 * 10 ** 5, 10 ** 6, 3 * 10 ** 6):
        out['K=%d' % K] = dict(
            any_participant_play_over_K=float((P > K).any(1).mean()),
            any_participant_play_plus_prod_over_K=float((tot > K).any(1).mean()),
            any_check_over_V=float(np.mean([r['maxcheck'] > K // 4 for r in rows])),
            executable_play_differs_from_ideal=float(np.mean([r['differs'][K] for r in rows])))
    return out, rows


def static_costs(args):
    """The cost sample only (rewrites the 'costs' entry of the static file)."""
    rng = random.Random(20261013)
    f = os.path.join(RUNS, 'sog-full-static.json')
    out = json.load(open(f))
    cs, rows = cost_sample(rng, n=args.n * 5)
    out['costs'] = {k: v for k, v in cs.items() if k != 'rows'}
    json.dump(cs['rows'], open(os.path.join(RUNS, 'sog_full', 'static_cost_rows.json'), 'w'))
    print('costs', json.dumps(out['costs']), flush=True)
    json.dump(out, open(f, 'w'), indent=1, default=str)


def static(args):
    rng = random.Random(20261013)
    out = {}
    t0 = time.time()
    # counts
    for gram in ('noeq', 'id'):
        g = grammar(gram)
        W, B = g.roles['W'], g.roles['B']
        nT1 = 1
        out.setdefault('counts', {})[gram] = dict(
            worker_spellings=len(W['spellings']), worker_run_trees=len(W['dts']), worker_classes=len(W['dts']) + nT1,
            boss_spellings=len(B['spellings']), boss_run_trees=len(B['dts']))
    print('counts', json.dumps(out['counts']), flush=True)
    out['universe'] = {gram: universe(grammar(gram), rng) for gram in ('noeq', 'id')}
    print('universe', json.dumps(out['universe']), '%.0fs' % (time.time() - t0), flush=True)
    # named masses
    nm = {}
    for arm in ('noeq', 'eq'):
        g = grammar(F.ARMS[arm][0])
        mw, mb = g.mass('W'), g.mass('B')
        d = {}
        for name, x in F.NAMED_W.items():
            if x in g.roles['W']['spellings']: d['W:' + name] = float(mw[g.roles['W']['spellings'].index(x)])
        for name, x in F.NAMED_B.items():
            if x in g.roles['B']['spellings']: d['B:' + name] = float(mb[g.roles['B']['spellings'].index(x)])
        nm[arm] = d
    out['named_mass'] = nm
    # families and coalitions per arm (ideal semantics)
    out['families'] = {}; out['coalitions'] = {}; out['like_constant'] = {}
    for arm in ('noeq', 'eq', 'sham', 'eqnoT'):
        ev = evaluator_k(arm, 'H', KBIG)
        BG = boss_groups(ev)
        consts = const_pids(ev)
        wf = worker_families(ev)
        bf = boss_families(ev, BG)
        out['families'][arm] = dict(workers=wf, bosses=bf)
        print(arm, 'families', json.dumps(out['families'][arm]), '%.0fs' % (time.time() - t0), flush=True)
        out['like_constant'][arm] = responds_like_constant(ev, BG, consts, np.random.default_rng(5), n=args.n)
        print(arm, 'like constant', json.dumps(out['like_constant'][arm]), flush=True)
        cm = coalition_mass(ev, BG, consts, np.random.default_rng(7), 3000)
        out['coalitions'][arm] = cm
        print(arm, 'coalitions', json.dumps(cm), '%.0fs' % (time.time() - t0), flush=True)
        if arm == 'eq':
            g = ev.g
            cmd = coalition_mass(ev, BG, consts, np.random.default_rng(7), 3000, inv_fn=lambda tk: producible_inv(g, tk))
            out['coalitions']['eq_producible'] = cmd
            print('eq producible coalitions', json.dumps(cmd), '%.0fs' % (time.time() - t0), flush=True)
        ev.maybe_clear(0)
    json.dump(out, open(os.path.join(RUNS, 'sog-full-static.json'), 'w'), indent=1, default=str)
    cs, rows = cost_sample(rng, n=args.n * 5)
    out['costs'] = {k: v for k, v in cs.items() if k != 'rows'}
    json.dump(cs['rows'], open(os.path.join(RUNS, 'sog_full', 'static_cost_rows.json'), 'w'))
    print('costs', json.dumps(cs), '%.0fs' % (time.time() - t0), flush=True)
    json.dump(out, open(os.path.join(RUNS, 'sog-full-static.json'), 'w'), indent=1, default=str)


# ----------------------------------------------------------------------------------------------------------------
# assays (notes §1.10, §1.12 item 3): isolated islands, the uncertified entrant, local transitions
# ----------------------------------------------------------------------------------------------------------------
def light_run(ev, cfg, rep, gens):
    run = Run(ev, cfg, rep)
    run.prefill()
    run.run(gens)
    RS = RunStats(run)
    return run, RS


def assay_isolated(args):
    """§1.10 (iii): one island (no migration) of the pure coalition (D*, T1, T1), empty vs preloaded inventories,
    S-nonself_3 + eq, 2,000 generations."""
    ev = evaluator('eq', 'S')
    out = {}
    nrep = args.runs or 40
    for pre in (False, True):
        rows = []
        t0 = time.time()
        for rep in range(nrep):
            cfg = dict(name='iso', arm='eq', mode='S', N=100, I=1, mN=0.0, forced=coalition(ev, pre), force_n=100)
            run, RS = light_run(ev, cfg, 5000 + rep, HORIZON)
            f = RS.fair[:, 0]
            rows.append(dict(fair_end=bool(f[-1]), ever_fair=bool(f.any()),
                             first_fair=int(np.argmax(f)) * CHECK_EVERY if f.any() else None,
                             fair_frac=float(f.mean()), play_end=int(RS.play[-1, 0]),
                             ctr=run.ctr[:19].tolist()))
        key = 'preloaded' if pre else 'empty'
        out[key] = dict(n=nrep, fair_end=sum(r['fair_end'] for r in rows), ever_fair=sum(r['ever_fair'] for r in rows),
                        plays_end=dict(sorted(defaultdict(int, {k: sum(1 for r in rows if r['play_end'] == k)
                                                                for k in set(r['play_end'] for r in rows)}).items())),
                        time_s=time.time() - t0, rows=rows)
        print(key, json.dumps({k: v for k, v in out[key].items() if k != 'rows'}), flush=True)
    json.dump(out, open(os.path.join(RUNS, 'sog_full', 'assay_isolated.json'), 'w'), indent=1)


def assay_entrant(args):
    """§1.12 item 3: one uncertified T1 (empty list) entering an island fixed on (D*, T1, T1) with valid preloaded
    certificates, slot 1 or 2, under S-nonself_3 and S-nonself-opp; no migration; 500 generations."""
    ev = evaluator('eq', 'S')
    g = ev.g
    t1sp = g.roles['W']['spellings'].index(F.NAMED_W['T1'])
    nrep = args.runs or 200
    out = {}
    for gate in ('nonself', 'opp'):
        for slot in (1, 2):
            rows = []
            t0 = time.time()
            for rep in range(nrep):
                cfg = dict(name='ent', arm='eq', mode='S', N=100, I=1, mN=0.0, forced=coalition(ev, True),
                           force_n=100, gate=gate, entrant=(slot, (t1sp, F.empty_inv('W'))))
                run = Run(ev, cfg, 7000 + rep)
                run.prefill()
                ent = run.type_id('W', ev.reg.get('W', t1sp, F.empty_inv('W')))
                res = run.type_id('W', ev.reg.get('W', t1sp, coalition(ev, True)[1][1]))
                rel = float(run.F[0, slot, ent] - run.F[0, slot, res]) / (100.0 * 100.0)
                run.run(500)
                st, sc, sn = run.snap
                nck = int(run.st[KN.ST_CI]) + 1
                cnt = []
                for ci in range(nck):
                    n = int(sn[ci, 0, slot]); ts = st[ci, 0, slot, :n]; cs_ = sc[ci, 0, slot, :n]
                    cnt.append(int(cs_[ts != res].sum()) if n else 0)
                lost = next((ci * CHECK_EVERY for ci in range(1, nck) if cnt[ci] == 0), None)
                rows.append(dict(rel_payoff_at_entry=rel, count_end=cnt[-1], lost_gen=lost, max_count=max(cnt),
                                 worker_productions=int(run.ctr[13]), gate_refusals=int(run.ctr[11]),
                                 fixed=cnt[-1] == 100))
            key = '%s_slot%d' % (gate, slot)
            rp = [r['rel_payoff_at_entry'] for r in rows]
            # what the entrant becomes after one encounter beside the residents (its own production, this gate)
            pre = coalition(ev, True)
            st_ = [ev.reg.get('B', *pre[0]), ev.reg.get('W', *pre[1]), ev.reg.get('W', *pre[2])]
            e = ev.reg.get('W', t1sp, F.empty_inv('W'))
            trip = list(st_); trip[slot] = e
            conv = ev.productions(trip[0], trip[1], trip[2], gate=(gate != 'opp'))[slot][1]
            first = dict(becomes_resident_type=conv == st_[slot], inventory=str(ev.reg[conv].inv))
            out[key] = dict(n=nrep, rel_payoff_at_entry=dict(min=min(rp), max=max(rp), mean=float(np.mean(rp))),
                            lost=sum(1 for r in rows if r['count_end'] == 0),
                            fixed=sum(1 for r in rows if r['fixed']),
                            produced=sum(1 for r in rows if r['worker_productions'] > 0),
                            median_lost_gen=float(np.median([r['lost_gen'] for r in rows if r['lost_gen'] is not None]))
                            if any(r['lost_gen'] is not None for r in rows) else None,
                            time_s=time.time() - t0, first_encounter=first, rows=rows)
            print(key, json.dumps({k: v for k, v in out[key].items() if k != 'rows'}), flush=True)
    json.dump(out, open(os.path.join(RUNS, 'sog_full', 'assay_entrant.json'), 'w'), indent=1)


def u_slot(ev, b, x, y, s):
    tr = ev.triple(b, x, y)
    W = ev.g.roles['W']
    t1 = 1 if F.tagged(W['dts'][ev.reg[x].tk]) else 0
    t2 = 1 if F.tagged(W['dts'][ev.reg[y].tk]) else 0
    J = 4 * tr['boss'] + 2 * (tr['a1'] == 'D') + (tr['a2'] == 'D')
    return float(PAY[J, t1, t2, s]), (tr['boss'], tr['a1'], tr['a2'])


def sgn(d):
    return 'strict' if d > 1e-12 else ('deleterious' if d < -1e-12 else 'neutral')


def entrant_versions(ev, pid, state, slot):
    """An entrant's inventories under S: empty, and after one encounter at the state (its own production)."""
    pr = ev.reg[pid]
    e = ev.reg.get(pr.role, pr.sp, F.empty_inv(pr.role))
    b, x, y = list(state)
    trip = [b, x, y]; trip[slot] = e
    out = ev.productions(trip[0], trip[1], trip[2])
    return {'empty': e, 'one encounter': out[slot][1]}


def transitions(ev, state, mode, rng, nsamp=300):
    """Forced one-step transitions at a state (b, x, y) (notes §1.10): the entrant's relative payoff, strict /
    neutral / deleterious, for named entrants and prior samples, and the causal composition substitution -> best boss
    replacement."""
    g = ev.g
    W, B = g.roles['W'], g.roles['B']
    mw, mb = g.mass('W'), g.mass('B')

    def mk(role, name):
        return named_pid(ev, role, name) if mode == 'H' else named_pid(ev, role, name, inv=F.empty_inv(role))

    def versions(pid, slot, st):
        if mode == 'H': return {'H': pid}
        return entrant_versions(ev, pid, st, slot)
    b, x, y = state
    res = dict(play=u_slot(ev, b, x, y, 0)[1])
    # union invasion and named worker entrants, each slot
    named = {}
    for slot in (1, 2):
        for nm in ('scab', 'T1', 'T1p', 'U_eq', 'XM', 'striker'):
            if F.NAMED_W.get(nm) not in W['spellings']: continue
            for vk, e in versions(mk('W', nm), slot, state).items():
                trip = [b, x, y]; trip[slot] = e
                u0 = u_slot(ev, b, x, y, slot)[0]; u1, pl = u_slot(ev, trip[0], trip[1], trip[2], slot)
                named['%s->slot%d [%s]' % (nm, slot, vk)] = (sgn(u1 - u0), round(u1 - u0, 4), pl)
    res['worker_entrants'] = named
    # boss replacement (named and prior samples)
    bn = {}
    for nm in ('pay(0,none)', 'pay(1/4,none)', 'pay(1/2,none)', 'B_eq', 'B_id', 'D*', 'D14'):
        for vk, e in versions(mk('B', nm), 0, state).items():
            u0 = u_slot(ev, b, x, y, 0)[0]; u1, pl = u_slot(ev, e, x, y, 0)
            bn['%s [%s]' % (nm, vk)] = (sgn(u1 - u0), round(u1 - u0, 4), pl)
    res['boss_entrants'] = bn
    cb = np.cumsum(mb)
    agg = defaultdict(float)
    u0 = u_slot(ev, b, x, y, 0)[0]
    for _ in range(nsamp):
        sp = min(int(np.searchsorted(cb, rng.random())), len(mb) - 1)
        e = ev.reg.get('B', sp, F.full_inv(g, 'B', int(B['tau'][sp])) if mode == 'H' else F.empty_inv('B'))
        if mode != 'H':
            e = entrant_versions(ev, e, state, 0)['one encounter']
        agg[sgn(u_slot(ev, e, x, y, 0)[0] - u0)] += 1.0 / nsamp
    res['boss_prior'] = dict(agg)
    # unread-slot substitution by prior samples (slot 2), then the best boss replacement at the substituted state
    cw = np.cumsum(mw)
    aggw = defaultdict(float); seq = defaultdict(float)
    best_bosses = [mk('B', nm) for nm in ('pay(0,none)', 'pay(1/4,none)', 'pay(1/2,none)', 'B_eq', 'D*', 'D14')]
    for _ in range(nsamp):
        sp = min(int(np.searchsorted(cw, rng.random())), len(mw) - 1)
        e = ev.reg.get('W', sp, F.full_inv(g, 'W', int(W['tau'][sp])) if mode == 'H' else F.empty_inv('W'))
        if mode != 'H':
            e = entrant_versions(ev, e, state, 2)['one encounter']
        u0w = u_slot(ev, b, x, y, 2)[0]; u1w = u_slot(ev, b, x, e, 2)[0]
        s1 = sgn(u1w - u0w)
        aggw[s1] += 1.0 / nsamp
        if s1 == 'deleterious': continue
        ub, pl = u_slot(ev, b, x, e, 0)
        cut = 'no'
        for bb in best_bosses:
            be = bb if mode == 'H' else entrant_versions(ev, bb, (b, x, e), 0)['one encounter']
            u1, pl1 = u_slot(ev, be, x, e, 0)
            if pl1[0] // 3 >= pl[0] // 3: continue           # a cut pays a lower wage at the substituted state
            if u1 > ub + 1e-12: cut = 'strict'; break
            if abs(u1 - ub) <= 1e-12: cut = 'neutral'
        seq['%s substitution -> %s cut' % (s1, cut)] += 1.0 / nsamp
    res['slot2_prior'] = dict(aggw)
    res['sequence'] = dict(seq)
    return res


def s_state(ev, names):
    """An S-nonself_3 state: bosses with every script PROD3 can write (bosses are never gated: the H list), workers with
    the scripts producible at non-self roots."""
    g = ev.g
    B, W = g.roles['B'], g.roles['W']
    out = []
    for s, nm in enumerate(names):
        role = 'B' if s == 0 else 'W'
        r = g.roles[role]
        sp = r['spellings'].index((F.NAMED_B if role == 'B' else F.NAMED_W)[nm])
        tk = int(r['tau'][sp])
        inv = F.full_inv(g, role, tk) if role == 'B' else producible_inv(g, tk)
        out.append(ev.reg.get(role, sp, inv))
    return tuple(out)


ASSAY_STATES = [('D*', 'T1', 'T1'), ('B_eq', 'T1', 'T1'), ('pay(1/2,none)', 'U_eq', 'U_eq'), ('B_id', 'U_eq', 'U_eq'),
                ('D*', 'U_eq', 'U_eq'), ('pay(1/2,none)', 'T1', 'T1')]


def assay_local(args):
    out = {}
    rng = np.random.default_rng(11)
    for mode in ('H', 'S'):
        ev = evaluator('eq', mode)
        for names in ASSAY_STATES:
            st = tuple(named_pid(ev, 'B' if s == 0 else 'W', nm) for s, nm in enumerate(names)) if mode == 'H' \
                else s_state(ev, names)
            r = transitions(ev, st, mode, rng, nsamp=args.n)
            out['%s (%s)' % (', '.join(names), mode)] = r
            print(mode, names, json.dumps({k: v for k, v in r.items() if k in ('play', 'boss_prior', 'slot2_prior', 'sequence')}),
                  flush=True)
    # sampled fair islands of the lottery cells at the horizon
    for cell in ('H_eq', 'S_eq'):
        d = os.path.join(OUT, 'cell_' + cell)
        if not os.path.isdir(d): continue
        cfg = cell_cfg(cell)
        ev = evaluator(cfg['arm'], cfg['mode'])
        fm = []
        for f in sorted(os.listdir(d)):
            js = json.load(open(os.path.join(d, f)))
            fm += [tuple(tuple(v) if isinstance(v, list) else v for v in t) for t in js['summary'].get('fair_modal', [])]
        rr = random.Random(3)
        rr.shuffle(fm)
        agg = defaultdict(lambda: defaultdict(float))
        for t in fm[:30]:
            (bsp, binv), (xsp, xinv), (ysp, yinv) = ((t[0], t[1]), (t[2], t[3]), (t[4], t[5]))
            totup = lambda inv: tuple(tuple(z) for z in inv)
            st = (ev.reg.get('B', bsp, totup(binv)), ev.reg.get('W', xsp, totup(xinv)), ev.reg.get('W', ysp, totup(yinv)))
            r = transitions(ev, st, cfg['mode'], rng, nsamp=max(50, args.n // 3))
            for k in ('boss_prior', 'slot2_prior', 'sequence'):
                for kk, v in r[k].items():
                    agg[k][kk] += v / min(30, len(fm))
        out['lottery fair islands ' + cell] = dict(n=min(30, len(fm)), **{k: dict(v) for k, v in agg.items()})
        print(cell, json.dumps(out['lottery fair islands ' + cell]), flush=True)
    json.dump(out, open(os.path.join(RUNS, 'sog_full', 'assay_local.json'), 'w'), indent=1, default=str)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--n', type=int, default=250)
    ap.add_argument('--cells', default='')
    ap.add_argument('--runs', type=int, default=0)
    ap.add_argument('--extend', type=int, default=0)
    ap.add_argument('--maxtasks', type=int, default=None)
    args = ap.parse_args()
    if args.cmd != 'calibrate': load_costc()
    globals()[args.cmd](args)


if __name__ == '__main__':
    main()
