"""Behavioural hooks: cells, founders, runs and post-run statistics (spec specs/2026-10-21-behavioural-hooks.md, notes
notes/hooks-beh.md, predictions predictions/2026-10-21-behavioural-hooks.md).  hooks_w2_run's design on hooks_beh_kern.

    python3 src/hooks_beh_run.py validate [REPS]       # `open-max` (legacy keys) against the stored rows -> runs/hooks-beh-validate.json
    python3 src/hooks_beh_run.py time CELL [REPS] [--gens G]   # timing probe on run indices 1000+ (not a counted cell)
    python3 src/hooks_beh_run.py batch CELL[,CELL...] --procs 1
Rows: runs/hooks_beh/CELL.json (one row per run, resumable; gzipped when the cell is complete).
"""
import argparse, json, os, sys, time, gzip
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import hooks_w2 as H
import hooks_w2_run as W2R
import hooks_beh as HB
import hooks_beh_kern as K

ROOT = H.ROOT
OUT = os.path.join(ROOT, 'runs', 'hooks_beh')
STORED = os.path.join(ROOT, 'runs', 'hooks_w2')
SALT = W2R.SALT
W = 0.3
SEG = 1000
COPY_Q = 0.1
CHECKS = W2R.CHECKS
CHECKS_M = list(range(0, 201, 10)) + [300, 500, 750, 1000, 1250, 1500, 1750, 2000]
CLASS_NAMES = ('FairBot', 'PrudentBot', 'CooperateBot-like', 'DefectBot-like', 'TrustingBot-like', 'predator-like', 'other', 'ambiguous')
ORIGIN_NAMES = ('none', 'seeded', 'thanks', 'grudge', 'contract', 'several', 'copied-untracked')
EVENT_NAMES = ('write-thanks', 'write-grudge', 'copy', 'contract', 'birth')

_ALL = np.ones((4, 4), np.bool_)

# cfg indices (hooks_beh_kern doc)
BASECFG = dict(recency=0, grudge=1, thanks=1, contract=1, copy=1, shuffle=0, noinherit=0, enc=1, keep_origin=0,
               write_mode=0, contract_mode=0, strict=1, anc=0, noevict=0, hostile=1, wlo=0, whi=0, log=0)
CELLS = {
    # K1: the stored open-max (legacy keys), same law as hooks_w2_run's (reproduction check)
    'open-max':          dict(write_mode=1, contract_mode=1, gens=500),
    'open-max-stored':   dict(write_mode=1, contract_mode=1, gens=1000, I=64),            # the stored hooks_w2 geometry (reproduction only)
    # K2-K6
    'beh-max':           dict(write_mode=2, contract_mode=2, seed=1, anc=1, log=1, gens=500, nrep=30),
    'beh-max-noA':       dict(write_mode=3, contract_mode=3, seed=2, anc=1, gens=500, nrep=30),
    'beh-max-hostile':   dict(write_mode=2, contract_mode=2, seed=1, anc=1, hostile=10, gens=500, nrep=30),
    'beh-written-only':  dict(write_mode=2, contract_mode=1, seed=0, anc=1, gens=500, nrep=30),
    'ff-beh-max':        dict(write_mode=2, contract_mode=2, seed=1, anc=1, ff=True, gens=400, nrep=10),
    'beh-max-N200':      dict(write_mode=2, contract_mode=2, seed=1, anc=1, gens=600, N=200, I=8, nrep=10),
    # M1 base cells (class logging, ancestry flags)
    'M-open-max':        dict(write_mode=1, contract_mode=1, anc=1, log=1, gens=500),
    'M-thanks-only':     dict(write_mode=1, contract=0, grudge=0, anc=1, log=1, gens=500),
    'M-grudge-only':     dict(write_mode=1, contract=0, thanks=0, anc=1, log=1, gens=500),
    # M3: transmission ablations on thanks-only (primary) and open-max (secondary)
    'M3a-thanks-noinherit': dict(write_mode=1, contract=0, grudge=0, anc=1, noinherit=2, gens=500),
    'M3b-thanks-nocopy':    dict(write_mode=1, contract=0, grudge=0, anc=1, copy=0, gens=500),
    'M3c-thanks-neither':   dict(write_mode=1, contract=0, grudge=0, anc=1, copy=0, noinherit=2, gens=500),
    'M3d-thanks-noevict':   dict(write_mode=1, contract=0, grudge=0, anc=1, noevict=1, gens=500),
    'M3e-thanks-single':    dict(write_mode=1, contract=0, grudge=0, anc=1, single=True, gens=500),
    'M3a-max-noinherit':    dict(write_mode=1, contract_mode=1, anc=1, noinherit=2, gens=500),
    'M3b-max-nocopy':       dict(write_mode=1, contract_mode=1, anc=1, copy=0, gens=500),
    'M3c-max-neither':      dict(write_mode=1, contract_mode=1, anc=1, copy=0, noinherit=2, gens=500),
    'M3d-max-noevict':      dict(write_mode=1, contract_mode=1, anc=1, noevict=1, gens=500),
    'M3e-max-single':       dict(write_mode=1, contract_mode=1, anc=1, single=True, gens=500),
    # M4: timing of writes (open-max)
    'M4-early':          dict(write_mode=1, contract_mode=1, anc=1, wlo=0, whi=51, gens=500),
    'M4-late':           dict(write_mode=1, contract_mode=1, anc=1, wlo=51, whi=10 ** 6, gens=500),
    # M5: sham writes (beh-max with unconditioned, size- and applicability-matched keys)
    'M5-sham':           dict(write_mode=4, contract_mode=2, seed=1, anc=1, gens=500, nrep=30),
}
ISL = dict(N=100, I=16, mN=1.0)                   # reduced from the spec's I = 64 (cost; notes 2): every cell is paired at this geometry
FF = dict(N=100, I=16, mN=1.0, merge=200)
FF_SLOTS = 1600


def cell_cfg(c, gen_offset=0):
    d = dict(BASECFG)
    d.update({k: v for k, v in c.items() if k in BASECFG})
    cfg = np.zeros(24, np.int64)
    cfg[:] = [d['recency'], d['grudge'], d['thanks'], d['contract'], d['copy'], d['shuffle'], d['noinherit'], d['enc'], 1, 0,
              d['keep_origin'], d['write_mode'], d['contract_mode'], d['strict'], d['anc'], d['noevict'], d['hostile'],
              d['wlo'], d['whi'], gen_offset, d['log'], 0, 0, 0]
    return cfg


# ------------------------------------------------------------------ the shared setup (language, keys, panel, priors)
class Setup:
    def __init__(self):
        self.B = HB.Beh()
        B = self.B
        self.Lx = B.Lx; self.KT = B.KT
        self.LA = self.Lx.arrays(); self.KA = self.KT.arrays()
        Lx, KT = self.Lx, self.KT
        nb = len(Lx.base)
        # base hook defaults (from the shortest spelling) and the single-hook test
        self.b_def = -np.ones((nb, 2), np.int8)
        for i, nm in enumerate(Lx.names):
            for t in (0, 1):
                hc, hd = ('HOOK(%d,C)' % t) in nm, ('HOOK(%d,D)' % t) in nm
                self.b_def[i, t] = 1 if (hc and not hd) else (0 if (hd and not hc) else -1)
        self.b_multi = np.array([self._multi(c) for c in Lx.base], np.int8)
        N = HB.named_programs(B)
        self.N = N
        order = ['CooperateBot', 'DefectBot', 'FairBot', 'TrustingBot', 'PrudentBot', 'GodelPredator']
        self.PANb = np.array([N[q][0] for q in order], np.int64)
        self.PANs = np.array([N[q][1] for q in order], np.int64)
        self.panel_order = order

        def sig(name):
            bx, sx = N[name]
            s = 0
            for k, q in enumerate(order):
                s |= B.play(bx, sx, *N[q])[0] << k
            s |= B.play(bx, sx, bx, sx)[0] << 6
            return s
        ref_names = ['FairBot', 'PrudentBot', 'CooperateBot', 'DefectBot', 'TrustingBot', 'GodelPredator']
        self.cref = np.array([sig(n) for n in ref_names], np.int64)
        assert len({int(s) & 63 for s in self.cref}) == 6, 'reference signatures collide on the panel'
        self.sig_ref = {n: int(s) for n, s in zip(ref_names, self.cref)}
        self.prior_full = KT.prior_full.copy(); self.prior_noa = KT.prior_noa.copy()
        kid = lambda f: KT.id_of(f, 'full')
        box = lambda f: ('box', f)
        self.hostile = np.array([kid(box(('not', 'a'))), kid(box('a'))], np.int64)
        self.k_fair = kid(box('a'))
        self._sham()
        self.mu = Lx.mu

    def _multi(self, c):
        L = self.Lx.L
        atoms, tt, k = L.funcs[c]
        kinds = [L.atoms[a] for a in atoms]
        for t in (0, 1):
            iA = [j for j, a in enumerate(kinds) if a[0] == H.KA and a[1] == t]
            iV = [j for j, a in enumerate(kinds) if a[0] == H.KV and a[1] == t]
            if not iA and not iV:
                continue
            iA = iA[0] if iA else None; iV = iV[0] if iV else None
            hc_ok = True; hd_ok = True
            for i in range(1 << k):
                if (iA is not None and (i >> iA) & 1) or (iV is not None and (i >> iV) & 1):
                    continue
                g = {}
                for A in (0, 1):
                    for V in (0, 1):
                        j = i | ((A << iA) if iA is not None else 0) | ((V << iV) if iV is not None else 0)
                        g[(A, V)] = (tt >> j) & 1
                if not (g[(0, 0)] == g[(0, 1)] == g[(1, 1)]):
                    hc_ok = False
                if not (g[(0, 0)] == g[(0, 1)] == g[(1, 0)]):
                    hd_ok = False
            if not hc_ok and not hd_ok:
                return 1
        return 0

    def _sham(self):
        """Applicability count of each full-family key: how many of the six named programs make it true for a FairBot reader
        (stabilized); sham groups = keys of the same size and the same count."""
        B, KT = self.B, self.KT
        N = self.N
        fb = N['FairBot']
        nk = len(KT.keys)
        A = np.zeros(nk, np.int64)
        for q in ('FairBot', 'TrustingBot', 'PrudentBot', 'GodelPredator', 'CooperateBot', 'DefectBot'):
            ax, ay, (row, _) = B.play(fb[0], fb[1], N[q][0], N[q][1], full=True)
            for k in KT.full_ids:
                A[k] += int(HB.key_true(k, KT.key_prog, row))
        self.applic = A
        groups = {}
        for k in KT.full_ids:
            groups.setdefault((KT.keys[k]['size'], int(A[k])), []).append(k)
        off = np.zeros(nk + 2, np.int64); lst = []
        full = set(KT.full_ids)
        for k in range(nk + 1):
            off[k] = len(lst)
            if k in full:
                lst.extend(groups[(KT.keys[k]['size'], int(A[k]))])
        off[nk + 1] = len(lst)
        self.sham_off = off; self.sham_list = np.array(lst if lst else [0], np.int64)

    def D(self, hostile_keys=True):
        return (self.prior_full, self.prior_noa, self.sham_off, self.sham_list, self.hostile, self.b_def, self.b_multi,
                self.PANb, self.PANs, self.cref)


_SETUP = {}


def setup():
    if 'S' not in _SETUP:
        _SETUP['S'] = Setup()
    return _SETUP['S']


# ------------------------------------------------------------------ founders (coupled across cells)
class _Mu:
    def __init__(self, mu, b_tags):
        self.mu = mu; self.b_tags = b_tags


def founders(S, rep, NI, c, ff=False):
    """Legacy seeding is hooks_w2_run.founders (identical draws).  Behavioural seeding (cell key 'seed' = 1 full family, 2 a-free)
    replaces the behaviour-scope key (and, under the hostile boost, the joint (key, action)) by a draw from the family prior
    on a separate stream [SALT, rep, g, j, 2]; every other draw is the legacy one."""
    Lh = S.Lx
    mu = S.mu
    if c.get('single'):
        mu = mu * (S.b_multi == 0); mu = mu / mu.sum()
    seed = c.get('seed', 0)
    if seed == 0:
        return W2R.founders(rep, NI, _Mu(mu, Lh.b_tags), None, ff)
    g = 1 if ff else 0
    bases = np.random.default_rng([SALT, rep, g]).choice(len(mu), size=NI, p=mu)
    prior = S.prior_noa if seed == 2 else S.prior_full
    cdf = np.cumsum(prior) / prior.sum()
    boost = float(c.get('hostile', 1))
    fills = []
    hk = set(int(x) for x in S.hostile)
    for j in range(NI):
        r = np.random.default_rng([SALT, rep, g, j, 1])
        r2 = np.random.default_rng([SALT, rep, g, j, 2])
        tg = int(Lh.b_tags[bases[j]])
        tags = [t for t in (0, 1) if (tg >> t) & 1]
        k = int(r.choice(5, p=H.POISSON))
        fl = []
        for _ in range(k):
            ut = int(r.integers(2))
            sc = int(r.integers(4))
            kh = int(r.integers(NI)); kb = int(r.integers(8))
            a = int(r.integers(2))
            u2 = float(r2.random())
            if not tags:
                continue
            t = tags[ut % len(tags)] if len(tags) == 2 else tags[0]
            if sc in (H.NONE, H.ROLE):
                key = 0
            elif sc == H.HIST:
                key = kh
            else:
                if boost > 1.0 and S.b_def[int(bases[j]), t] == 1:
                    w = np.array([prior * np.where(np.isin(np.arange(len(prior)), list(hk)) & (act == 0), boost, 1.0)
                                  for act in (0, 1)])
                    w = (w / w.sum()).ravel()
                    idx = int(np.searchsorted(np.cumsum(w), u2, side='right'))
                    idx = min(idx, len(w) - 1)
                    a = idx // len(prior); key = idx % len(prior)
                else:
                    key = int(np.searchsorted(cdf, u2, side='right'))
                    key = min(key, len(prior) - 1)
                    while prior[key] == 0:                                   # (cdf ties on zero-weight ids)
                        key -= 1
            fl.append(H.fcode(a, t, sc, H.SEEDED, key))
        fills.append(fl)
    return bases, fills


def hostile_founded(S, bases, fills, N, I):
    """Per island: does some founder hold a seeded hostile construction (C-default hook, a hostile key, action D)?"""
    hk = set(int(x) for x in S.hostile)
    out = np.zeros(I, bool); cnt = np.zeros(I, np.int64)
    for j, fl in enumerate(fills):
        for f in fl:
            d = H.f_scope(f), H.f_tag(f), H.f_action(f), H.f_key(f)
            if d[0] == H.BEH and d[2] == 0 and (d[3] & 4095) in hk and S.b_def[int(bases[j]), d[1]] == 1 and \
                    (int(S.Lx.b_tags[int(bases[j])]) >> d[1]) & 1:
                out[j // N] = True; cnt[j // N] += 1
    return out, cnt


# ------------------------------------------------------------------ one run
def _alloc(I, cap, nchk):
    return (np.zeros((I, cap), np.int64), np.zeros((I, cap), np.int64), np.zeros((I, cap)), np.zeros(I, np.int64),
            np.zeros((I, cap, cap), np.int16), np.zeros((nchk, I, K.NREC_I)), np.zeros((nchk, K.NREC_G)),
            np.zeros((nchk, I, K.NCLS), np.int64), np.zeros((nchk, K.NCLS, K.NORG, 2), np.int64))


def _place(pres, cnt, npres, tid, I, N, T):
    gcount = T[9]
    for i in range(I):
        seen = {}
        for j in range(i * N, (i + 1) * N):
            t_ = tid[j]
            seen[t_] = seen.get(t_, 0) + 1
        for t_, k in seen.items():
            pres[i, npres[i]] = t_; cnt[i, npres[i]] = k; npres[i] += 1
            gcount[t_] += k


def run_one(cell, rep, gens=None, tcap=K.TCAP):
    S = setup()
    c = CELLS[cell]
    ff = c.get('ff', False)
    G = FF if ff else dict(ISL)
    if 'N' in c:
        G['N'] = c['N']
    if 'I' in c:
        G['I'] = c['I']
    if gens is None:
        gens = c.get('gens', SEG)
    N, I, mN = G['N'], G['I'], G['mN']
    NI = N * I
    LA, KA = S.LA, S.KA
    Lx = S.Lx
    active = _ALL
    cfg = cell_cfg(c)
    recency = int(cfg[0])
    T, tdict, ev, ev2, sdict, tv, smeta = K.new_tables(S.KT, tcap)
    D = S.D()
    bases, fills = founders(S, rep, NI, c, ff)
    tid = []
    for j in range(NI):
        f = np.zeros(4, np.int64); f[:len(fills[j])] = fills[j]
        tid.append(K.get_type(T, tdict, Lx.b_tags, active, recency, int(bases[j]), j, f, len(fills[j])))
    hfounded, hcount = hostile_founded(S, bases, fills, N, I)
    seed = (SALT * 7 + 1000003 * rep + (17 if ff else 0)) % (2 ** 31)
    checks_all = CHECKS_M if cfg[20] == 1 else CHECKS
    t0 = time.time()
    ts = []; at = {}
    es = np.zeros((4, 4, 4)); ctr = np.zeros(32, np.int64); conv = np.zeros((5, 2, 2, K.NCLS, K.NCLS), np.int64)
    args = (LA, KA, Lx.b_tags, Lx.iC, Lx.iD, Lx.bD, T, tdict, ev, ev2, tv, sdict, smeta, D, active)
    if ff:
        ch1 = [x for x in checks_all if x <= G['merge']]
        pres, cnt, ps, npres, Cl, rec_i, rec_g, rec_c, rec_t = _alloc(I, N, len(ch1))
        _place(pres, cnt, npres, tid, I, N, T)
        nrec = K.kernel(*args, cfg, COPY_Q, H.PDPAY, pres, cnt, ps, npres, Cl, N, W, mN / N, G['merge'], seed,
                        np.array(ch1, np.int64), rec_i, rec_g, rec_c, rec_t, es, ctr, conv)
        del Cl
        _ts(ts, ch1[:nrec], rec_i, rec_g, rec_c, rec_t)
        at[str(G['merge'])] = state_stats(S, T, ev, active, recency, pres, cnt, npres, rec_i[nrec - 1])
        comp = {}
        for i in range(I):
            for s_ in range(npres[i]):
                comp[int(pres[i, s_])] = comp.get(int(pres[i, s_]), 0) + int(cnt[i, s_])
        N2 = NI
        ch2 = sorted(set([x - G['merge'] for x in checks_all if G['merge'] < x <= gens] + [gens - G['merge']]))
        cap2 = min(N2, FF_SLOTS)
        if len(comp) > cap2:
            raise RuntimeError('merged population has %d types > %d slots' % (len(comp), cap2))
        pres2, cnt2, ps2, npres2, Cl2, rec_i2, rec_g2, rec_c2, rec_t2 = _alloc(1, cap2, len(ch2))
        for t_ in sorted(comp):
            pres2[0, npres2[0]] = t_; cnt2[0, npres2[0]] = comp[t_]; npres2[0] += 1
        cfg2 = cell_cfg(c, G['merge']); cfg2[8] = 1; cfg2[9] = 1
        nrec2 = K.kernel(*args, cfg2, COPY_Q, H.PDPAY, pres2, cnt2, ps2, npres2, Cl2, N2, W, 0.0, gens - G['merge'], seed + 1,
                         np.array(ch2, np.int64), rec_i2, rec_g2, rec_c2, rec_t2, es, ctr, conv)
        _ts(ts, [x + G['merge'] for x in ch2[:nrec2]], rec_i2, rec_g2, rec_c2, rec_t2)
        last_pres, last_cnt, last_np, last_rec = pres2, cnt2, npres2, rec_i2[nrec2 - 1]
        at[str(gens)] = state_stats(S, T, ev, active, recency, pres2, cnt2, npres2, last_rec)
        conc = rec_i[1:nrec, :, 3].mean(0)
    else:
        pres, cnt, ps, npres, Cl, rec_i, rec_g, rec_c, rec_t = _alloc(I, N, len(checks_all))
        done = 0; k = 0
        _place(pres, cnt, npres, tid, I, N, T)
        concs = []
        while done < gens:
            seg = min(SEG, gens - done)
            chk = [x - done for x in checks_all if done < x <= done + seg] if done else [x for x in checks_all if x <= seg]
            if chk[-1] != seg:
                chk.append(seg)
            cfg_k = cell_cfg(c, done); cfg_k[8] = 1 if done == 0 else 0
            ri = np.zeros((len(chk), I, K.NREC_I)); rg = np.zeros((len(chk), K.NREC_G))
            rc = np.zeros((len(chk), I, K.NCLS), np.int64); rt = np.zeros((len(chk), K.NCLS, K.NORG, 2), np.int64)
            nrec = K.kernel(*args, cfg_k, COPY_Q, H.PDPAY, pres, cnt, ps, npres, Cl, N, W, mN / N, seg, seed + k,
                            np.array(chk, np.int64), ri, rg, rc, rt, es, ctr, conv)
            _ts(ts, [x + done for x in chk[:nrec]], ri, rg, rc, rt)
            concs.append(ri[:nrec][[q for q in range(nrec) if chk[q] + done > 0], :, 3])
            done += seg; k += 1
            if nrec < len(chk):
                break
            at[str(done)] = state_stats(S, T, ev, active, recency, pres, cnt, npres, ri[nrec - 1])
        last_pres, last_cnt, last_np, last_rec = pres, cnt, npres, ri[nrec - 1]
        conc = np.concatenate(concs).mean(0)
    wall = time.time() - t0
    fin = final_stats(S, T, LA, KA, ev, active, recency, last_pres, last_cnt, last_np, last_rec, cfg)
    row = dict(cell=cell, rep=rep, wall=round(wall, 1), gens=gens, N=N, I=I, ntypes=int(T[10][0]), live_types=int(T[10][0] - T[10][1]),
               overflow=int(ctr[8]), ev_size=len(ev), ev2_size=len(ev2), states=int(smeta[0]), state_overflow=int(smeta[1]), max_stab_world=int(smeta[2]), late_stab=int(smeta[3]),
               island_conc=[round(float(x), 4) for x in conc], counters=[int(x) for x in ctr],
               enc_stats=es.astype(np.int64).tolist(), conv=conv.tolist(), ts=ts, at=at, final=fin,
               hostile_founded=[bool(x) for x in hfounded], hostile_founders=[int(x) for x in hcount])
    last = at[max(at, key=int)] if at else {}
    for key in ('eff_islands', 'pcc', 'efficient_run', 'universal_open', 'universal_target', 'universal_current',
                'lineage_closed', 'rival'):
        row[key] = last.get(key)
    return row


def _ts(ts, checks, rec_i, rec_g, rec_c, rec_t):
    for k, g in enumerate(checks):
        ri = rec_i[k]; rg = rec_g[k]
        ts.append(dict(gen=int(g), pcc=round(float(ri[:, 0].mean()), 5), eff=round(float((ri[:, 0] >= 0.95).mean()), 4),
                       isl_pcc=[round(float(x), 3) for x in ri[:, 0]],
                       lin=round(float(ri[:, 2].mean()), 3), conc=round(float(ri[:, 3].mean()), 5),
                       types=int(rg[66]), gentle=round(float(rg[64]), 5), gentle_holder=round(float(rg[65]), 5),
                       hist_holders=round(float(rg[68]), 5), fills_per=round(float(rg[67]), 4),
                       open_holders=[round(float(x), 5) for x in rg[70:74]],
                       held=[int(x) for x in rg[:64]],
                       cls=(rec_c[k].tolist() if rec_c[k].any() else None), tab=(rec_t[k].tolist() if rec_t[k].any() else None)))


# ------------------------------------------------------------------ post-run statistics
def decode_fill(f):
    f = int(f)
    a = (f - 1) & 1; t = ((f - 1) >> 1) & 1; sc = ((f - 1) >> 2) & 3; og = ((f - 1) >> 4) & 3; key = (f - 1) >> 6
    anc = cop = 0
    if sc == 3:
        anc = (key >> 12) & 3; cop = (key >> 14) & 1; key &= 4095
    return dict(a='CD'[1 - a], t=t, scope=('open' if (sc == 3 and key >= 8) else H.SCOPES[sc]), origin=H.ORIGINS[og],
                key=int(key), anc=int(anc), cop=int(cop))


def type_desc(S, T, t):
    Tb, Tl, Tf, Tn = T[0], T[1], T[2], T[3]
    out = []
    for j in range(int(Tn[t])):
        d = decode_fill(Tf[t, j])
        kn = S.KT.keys[d['key']]['name'] if d['scope'] in ('open', 'behaviour') and d['key'] < len(S.KT.keys) else str(d['key'])
        out.append('%s:%s:%s:%s:t%d' % (d['scope'], d['origin'], d['a'], kn, d['t']))
    return dict(base=S.Lx.names[int(Tb[t])], lineage=int(Tl[t]), fills=out)


def stranger_code(S, T, ev, a, b):
    Tb, Ts0 = T[0], T[5]
    sa = int(Ts0[a]); sb = int(Ts0[b])
    return int(K.eval_code(S.LA, S.KA, ev, S.Lx.iC, S.Lx.iD, int(Tb[a]), sa, sa, sa, int(Tb[b]), sb, sb, sb))


def fb_stranger(S, T, ev, a):
    Tb, Ts0 = T[0], T[5]
    sa = int(Ts0[a])
    return int(K.eval_code(S.LA, S.KA, ev, S.Lx.iC, S.Lx.iD, int(Tb[a]), sa, sa, sa, S.Lx.FB, 0, 0, 0))


def state_stats(S, T, ev, active, recency, pres, cnt, npres, rec_i):
    """Island and run statistics of a population state (hooks_w2_run.state_stats on the behavioural evaluator)."""
    Lx = S.Lx
    pcc = rec_i[:, 0]
    eff = pcc >= 0.95
    maj = [int(x) for x in rec_i[:, 4]]
    umaj = sorted(set(maj))
    comp = {}
    for a in umaj:
        for b in umaj:
            if (b, a) in comp:
                comp[(a, b)] = comp[(b, a)]
                continue
            comp[(a, b)] = (stranger_code(S, T, ev, a, b) & 3) == 3
    cur = {}
    for a in umaj:
        for b in umaj:
            cur[(a, b)] = (int(K.match(T, S.LA, S.KA, ev, Lx.iC, Lx.iD, active, recency, a, b)) & 3) == 3
    open_all = all(comp[(a, b)] for a in umaj for b in umaj)
    cur_all = all(cur[(a, b)] for a in umaj for b in umaj)
    fbok = {a: (fb_stranger(S, T, ev, a) & 3) == 3 for a in umaj}
    lin_closed = [bool(eff[i] and cur[(maj[i], maj[i])] and not comp[(maj[i], maj[i])]) for i in range(len(maj))]
    effm = sorted({maj[i] for i in range(len(maj)) if eff[i]})
    parent = {a: a for a in effm}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a in effm:
        for b in effm:
            if a < b and comp[(a, b)]:
                parent[find(a)] = find(b)
    sizes = {}
    for i in range(len(maj)):
        if eff[i]:
            r_ = find(maj[i]); sizes[r_] = sizes.get(r_, 0) + 1
    top = max(sizes, key=sizes.get) if sizes else None
    rival = [bool(eff[i] and find(maj[i]) != top) for i in range(len(maj))]
    comp_out = []
    for i in range(pres.shape[0]):
        items = sorted(((int(cnt[i, s]), int(pres[i, s])) for s in range(int(npres[i]))), reverse=True)
        comp_out.append(items[:4])
    types_seen = sorted({t for isl in comp_out for _, t in isl} | set(umaj))
    desc = {str(t): type_desc(S, T, t) for t in types_seen}
    Tf, Tn = T[2], T[3]
    trait = {}
    for a in umaj:
        has_contract = any(((int(Tf[a, j]) - 1) >> 4) & 3 == H.CONTRACT for j in range(int(Tn[a])))
        trait[str(a)] = dict(open_self=bool(comp[(a, a)]), cur_self=bool(cur[(a, a)]), fb_mutual=bool(fbok[a]),
                             hooked=bool(Lx.b_tags[int(T[0][a])] > 0), has_contract=bool(has_contract))
    # M6: stranger compatibility on winning islands: majority holder against the panel's FairBot stranger and its own stranger copy
    win = [i for i in range(len(maj)) if eff[i]]
    m6 = dict(n_win=len(win), fb_stranger=float(np.mean([fbok[maj[i]] for i in win])) if win else None,
              own_stranger=float(np.mean([comp[(maj[i], maj[i])] for i in win])) if win else None)
    return dict(eff_islands=round(float(eff.mean()), 4), pcc=round(float(pcc.mean()), 5), efficient_run=bool(eff.all()),
                universal_open=bool(eff.all() and open_all),
                universal_target=bool(eff.all() and open_all and all(fbok.values())),
                universal_current=bool(eff.all() and cur_all), lineage_closed=round(float(np.mean(lin_closed)), 4),
                rival=round(float(np.mean(rival)), 4), island_pcc=[round(float(x), 4) for x in pcc],
                island_fb=[bool(fbok[maj[i]]) for i in range(len(maj))],
                island_open_self=[bool(comp[(maj[i], maj[i])]) for i in range(len(maj))],
                island_lin_closed=lin_closed, majority=maj, traits=trait, types=desc, comp=comp_out, m6=m6)


def final_stats(S, T, LA, KA, ev, active, recency, pres, cnt, npres, rec_i, cfg):
    """End-of-run statistics that need the type table: the hostile-construction share, and (when the class machinery is on) the
    (class, deciding origin, copied) table over individuals on winning islands, for prediction 3."""
    Tb, Tl, Tf, Tn, Tg = T[0], T[1], T[2], T[3], T[4]
    hk = set(int(x) for x in S.hostile)
    tot = 0; hos = 0; hos_win = 0; tot_win = 0
    eff = rec_i[:, 0] >= 0.95
    for i in range(pres.shape[0]):
        for s in range(int(npres[i])):
            t = int(pres[i, s]); c = int(cnt[i, s])
            tot += c
            if eff[i]:
                tot_win += c
            h = False
            for j in range(int(Tn[t])):
                f = int(Tf[t, j])
                if H.f_scope(f) == H.BEH and H.f_action(f) == 0 and (H.f_key(f) & 4095) in hk and (int(Tg[t]) >> H.f_tag(f)) & 1 \
                        and S.b_def[int(Tb[t]), H.f_tag(f)] == 1:
                    h = True
            if h:
                hos += c
                if eff[i]:
                    hos_win += c
    out = dict(hostile_share=hos / tot, hostile_share_win=(hos_win / tot_win if tot_win else None))
    tab = np.zeros((K.NCLS, K.NORG, 2), np.int64)
    D = S.D()
    for i in range(pres.shape[0]):
        if not eff[i]:
            continue
        for s in range(int(npres[i])):
            t = int(pres[i, s]); c = int(cnt[i, s])
            k = int(K._class(T, LA, KA, ev, S.Lx.iC, S.Lx.iD, D[7], D[8], D[9], t))
            cat, cp = K._decide_origin(T, LA, KA, ev, S.Lx.iC, S.Lx.iD, D[7], D[8], D[9], active, recency, int(cfg[14]), t)
            tab[k, int(cat), int(cp)] += c
    out['win_tab'] = tab.tolist()
    return out


# ------------------------------------------------------------------ validation and drivers
def _stored_rows(cell):
    path = os.path.join(STORED, '%s.json.gz' % cell)
    return {r['rep']: r for r in json.load(gzip.open(path)) if 'error' not in r}


def validate(nreps=2, cell='open-max-stored', gens=None):
    """Reproduction check: this module's legacy-keys `open-max` cell (anc off) against the stored hooks_w2 rows: island P(C,C),
    present types and held fills at every stored generation, and the final state statistics."""
    stored = _stored_rows('open-max')
    out = []
    for rep in range(nreps):
        row = run_one(cell, rep, gens=gens)
        st = stored[rep]
        by_gen = {t['gen']: t for t in st['ts']}
        gl = max(by_gen) if gens is None else gens
        cmp_ = [t for t in row['ts'] if t['gen'] in by_gen and t['gen'] <= gl]
        eq = {}
        for key in ('isl_pcc', 'types', 'held'):
            eq[key] = all(t[key] == by_gen[t['gen']][key] for t in cmp_)
        eq['n_checked'] = len(cmp_)
        a, b = row['at'].get(str(gl)), st['at'].get(str(gl))
        eq_at = None if (a is None or b is None) else (a['island_pcc'] == b['island_pcc'] and a['majority'] == b['majority'] and
                                                        a['universal_open'] == b['universal_open'] and a['eff_islands'] == b['eff_islands'])
        out.append(dict(rep=rep, cell=cell, gens=gl, records_equal=eq, state_equal=eq_at, eff=row['eff_islands'], wall=row['wall']))
        print(out[-1], flush=True)
    return out


def _job(args):
    cell, rep = args
    try:
        return run_one(cell, rep)
    except Exception:
        import traceback
        return dict(cell=cell, rep=rep, error=traceback.format_exc())


def _path(cell):
    return os.path.join(OUT, '%s.json' % cell), os.path.join(OUT, '%s.json.gz' % cell)


def _load(cell):
    p, pz = _path(cell)
    if os.path.exists(p):
        rows = json.load(open(p))
    elif os.path.exists(pz):
        rows = json.load(gzip.open(pz))
    else:
        rows = []
    return [r for r in rows if 'error' not in r]


def run_batch(cells, procs):
    """All runs of the listed cells through one pool (one job per process), resumable."""
    from multiprocessing import Pool
    os.makedirs(OUT, exist_ok=True)
    rows = {}; jobs = []
    for cell in cells:
        rows[cell] = _load(cell)
        done = {r['rep'] for r in rows[cell]}
        nrep = CELLS[cell].get('nrep', 20 if CELLS[cell].get('ff') else 40)
        jobs += [(cell, r) for r in range(nrep) if r not in done]
    print('%d jobs' % len(jobs), flush=True)
    setup()
    with Pool(procs, maxtasksperchild=1) as pool:
        for row in pool.imap_unordered(_job, jobs):
            cell = row['cell']
            if 'error' in row:
                print('ERROR', cell, row['rep'], row['error'], flush=True)
                continue
            rows[cell].append(row)
            print('%s rep %d: eff %.3f univ-open %s current %s lin-closed %.3f live %d (%.0fs)' % (
                cell, row['rep'], row['eff_islands'], row['universal_open'], row['universal_current'],
                row['lineage_closed'], row['live_types'], row['wall']), flush=True)
            json.dump(sorted(rows[cell], key=lambda r: r['rep']), open(_path(cell)[0], 'w'))
    for cell in cells:                                   # gzip the complete cells
        p, pz = _path(cell)
        nrep = CELLS[cell].get('nrep', 20 if CELLS[cell].get('ff') else 40)
        if os.path.exists(p) and len(rows[cell]) >= nrep:
            with gzip.open(pz, 'wt') as f:
                json.dump(sorted(rows[cell], key=lambda r: r['rep']), f)
            os.remove(p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('cell', nargs='?')
    ap.add_argument('reps', nargs='?', type=int, default=2)
    ap.add_argument('--procs', type=int, default=1)
    ap.add_argument('--gens', type=int, default=None)
    a = ap.parse_args()
    if a.cmd == 'validate':
        out = validate(int(a.cell) if a.cell else 2, gens=a.gens)
        json.dump(out, open(os.path.join(ROOT, 'runs', 'hooks-beh-validate.json'), 'w'), indent=1)
    elif a.cmd == 'time':
        for r in range(a.reps):
            t = time.time()
            row = run_one(a.cell, 1000 + r, gens=a.gens)
            print(a.cell, 'probe rep', 1000 + r, 'gens', a.gens, 'wall %.1f' % (time.time() - t), 'types', row['ntypes'],
                  'states', row['states'], 'eff', row['eff_islands'], 'univ-open', row['universal_open'],
                  'lin-closed', row['lineage_closed'], 'counters', row['counters'][:24], flush=True)
    elif a.cmd == 'batch':
        run_batch(a.cell.split(','), a.procs)


if __name__ == '__main__':
    main()
