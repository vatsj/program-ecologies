"""Hooks, Part W: cells, founders, runs and post-run statistics for the hooked modal PD
(notes/hooks-w.md §1.8-§1.10; predictions/2026-10-18-hooks-w.md).

    python3 src/hooks_w_run.py validate              # stored-row reproduction (baseline) -> runs/hooks-w-validate.json
    python3 src/hooks_w_run.py time CELL [REPS]      # timing probe (not a counted cell; results discarded)
    python3 src/hooks_w_run.py run CELL [--procs 3] [--reps 40]
Rows are written to runs/hooks_w/CELL.json (one row per run, resumable).
"""
import argparse, json, os, sys, time, gzip
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import hooks_w as H
import hooks_w_kern as K

ROOT = H.ROOT
OUT = os.path.join(ROOT, 'runs', 'hooks_w')
SALT = 20261018
W = 0.3
GENS = 2000
SEG = 1000
COPY_Q = 0.1
CHECKS = [0, 10, 25, 50, 100, 200, 300, 500, 750, 1000, 1250, 1500, 1750, 2000]

_ALL = np.ones((4, 4), np.bool_)


def _act(**off):
    a = _ALL.copy()
    for k, v in off.items():
        if k == 'scope':
            for s in v: a[s, :] = False
        if k == 'origin':
            for o in v: a[:, o] = False
    return a


# cfg defaults: recency 0, grudge 1, thanks 1, contracts 1, copying 1, shuffle 0, noinherit 0, encounters 1
BASECFG = dict(recency=0, grudge=1, thanks=1, contract=1, copy=1, shuffle=0, noinherit=0, enc=1, keep_origin=0)
CELLS = {
    # the no-hook baseline: plain grammar, the stored lottery's founders (multinomial over the 51 behavioural classes)
    # and kernel seeds, no encounters; reps 0-19 reproduce runs/almost-all-seeds-islands.json draw for draw
    'baseline':     dict(plain='stored', gens=2000),
    'inert':        dict(active=np.zeros((4, 4), np.bool_), gens=2000),
    'maximal':      dict(active=_ALL, gens=2000),
    'grudge-only':  dict(active=_ALL, thanks=0),
    'no-behaviour':   dict(active=_act(scope=[H.BEH])),
    'no-role':        dict(active=_act(scope=[H.ROLE])),
    'no-history':     dict(active=_act(scope=[H.HIST])),
    'no-behaviour-renorm': dict(active=_act(scope=[H.BEH]), renorm=H.BEH),
    'no-history-renorm':   dict(active=_act(scope=[H.HIST]), renorm=H.HIST),
    'no-seed':        dict(active=_act(origin=[H.SEEDED])),
    'no-writes':      dict(active=_act(origin=[H.WRITTEN])),
    'no-copy':        dict(active=_act(origin=[H.COPIED])),
    'no-contract':    dict(active=_act(origin=[H.CONTRACT])),
    'seeding-only': dict(active=_act(origin=[H.WRITTEN, H.COPIED, H.CONTRACT])),
    'hist-shuffled':  dict(active=_ALL, shuffle=1),
    'hist-noinherit': dict(active=_ALL, noinherit=1),
    'recency':      dict(active=_ALL, recency=1),
    # strict source ablations (added during the run, notes §2.7): copies keep the copied fill's origin, so a disabled
    # source's content cannot re-enter as an active 'copied' fill
    'no-contract-strict': dict(active=_act(origin=[H.CONTRACT]), keep_origin=1),
    'no-writes-strict':   dict(active=_act(origin=[H.WRITTEN]), keep_origin=1),
    'no-seed-strict':     dict(active=_act(origin=[H.SEEDED]), keep_origin=1),
    # fission-fusion (128 x 100, merged into one population at generation 200)
    'ff-baseline':  dict(plain=True, ff=True, gens=600),
    'ff-inert':     dict(active=np.zeros((4, 4), np.bool_), ff=True, gens=600),
    'ff-maximal':   dict(active=_ALL, ff=True, gens=600),
    'ff-grudge-only': dict(active=_ALL, thanks=0, ff=True, gens=600),
}
ISL = dict(N=100, I=64, mN=1.0)
FF = dict(N=100, I=32, mN=1.0, merge=200)
FF_SLOTS = 3200

_LANG = {}


def lang(hooks=True):
    if hooks not in _LANG:
        _LANG[hooks] = H.Lang(6, hooks=hooks)
    return _LANG[hooks]


def cell_cfg(c):
    d = dict(BASECFG); d.update({k: v for k, v in c.items() if k in BASECFG})
    cfg = np.array([d['recency'], d['grudge'], d['thanks'], d['contract'], d['copy'], d['shuffle'], d['noinherit'],
                    d['enc'], 1, 0, d['keep_origin']], np.int64)
    return cfg


# ------------------------------------------------------------------ founders (coupled across cells)
def founders(rep, NI, Lh, renorm=None, ff=False):
    """Base list from stream [SALT, rep, ff]; each founder's fills from its own stream [SALT, rep, ff, j, 1], drawing
    the same random numbers whatever the founder's tags, so every cell of a geometry has identical bases and (except
    the renormalized cells) identical fills."""
    g = 1 if ff else 0
    bases = np.random.default_rng([SALT, rep, g]).choice(len(Lh.mu), size=NI, p=Lh.mu)
    fills = []
    for j in range(NI):
        r = np.random.default_rng([SALT, rep, g, j, 1])
        tg = int(Lh.b_tags[bases[j]])
        tags = [t for t in (0, 1) if (tg >> t) & 1]
        k = int(r.choice(5, p=H.POISSON))
        fl = []
        for _ in range(k):
            ut = int(r.integers(2))
            if renorm is None:
                sc = int(r.integers(4))
            else:
                rest = [s for s in range(4) if s != renorm]
                sc = rest[int(r.integers(3))]
            kh = int(r.integers(NI)); kb = int(r.integers(8))
            a = int(r.integers(2))
            if not tags:
                continue
            t = tags[ut % len(tags)] if len(tags) == 2 else tags[0]
            key = 0 if sc in (H.NONE, H.ROLE) else (kh if sc == H.HIST else kb)
            fl.append(H.fcode(a, t, sc, H.SEEDED, key))
        fills.append(fl)
    return bases, fills


def stored_founders(rep, N, I, mN, Lp, T, tdict):
    """The stored modal lottery's founders: island i is a multinomial draw over the 51 behavioural classes from
    rng [0, N, I, 10 mN, rep]; one type per class (lineage 0), in class order."""
    import modal as M
    import almost_all_seeds as AS
    d = AS.arm_data('modal', 6)
    L, val, worlds, prov = M.build(6)
    reps = [Lp.bidx[min(mem, key=lambda c: (L.bits_canon[c], c))] for mem in prov.members]
    ctype = [H.get_type(T, tdict, Lp.b_tags, np.zeros((4, 4), np.bool_), 0, reps[k], 0, np.zeros(4, np.int64), 0)
             for k in range(len(reps))]
    rng = np.random.default_rng([0, N, I, int(mN * 10), rep])
    tid = []; bases = []
    for i in range(I):
        draw = rng.multinomial(N, d['mu'])
        for k in range(len(reps)):
            tid += [ctype[k]] * int(draw[k]); bases += [reps[k]] * int(draw[k])
    return np.array(bases), tid


def plain_founders(rep, NI, Lp, ff=False):
    g = 1 if ff else 0
    return np.random.default_rng([SALT, rep, g, 7]).choice(len(Lp.mu), size=NI, p=Lp.mu)


# ------------------------------------------------------------------ one run
def _alloc(I, cap, nchk):
    return (np.zeros((I, cap), np.int64), np.zeros((I, cap), np.int64), np.zeros((I, cap)), np.zeros(I, np.int64),
            np.zeros((I, cap, cap), np.int16), np.zeros((nchk, I, K.NREC_I)), np.zeros((nchk, K.NREC_G)))


def run_one(cell, rep, gens=None, tcap=H.TCAP):
    """One run.  Islands: segments of 1,000 generations (seeds s, s + 1) with a full summary after each; the
    comparison point for every cell is generation 1,000 and the main cells continue to 2,000.  Fission-fusion: 200
    generations on 128 islands, the merge, then one population to generation 1,000."""
    c = CELLS[cell]
    plain = c.get('plain', False)
    ff = c.get('ff', False)
    G = FF if ff else ISL
    if gens is None:
        gens = c.get('gens', SEG)
    N, I, mN = G['N'], G['I'], G['mN']
    NI = N * I
    Lx = lang(hooks=not plain)
    LA = Lx.arrays()
    active = np.zeros((4, 4), np.bool_) if plain else c['active']
    cfg = cell_cfg(c)
    if plain:
        cfg[7] = 0
    T, tdict, ev = H.new_tables(tcap)
    recency = int(cfg[0])
    if plain == 'stored':
        bases, tid = stored_founders(rep, N, I, mN, Lx, T, tdict)
        fills = None
    elif plain:
        bases = plain_founders(rep, NI, Lx, ff)
        tid = [H.get_type(T, tdict, Lx.b_tags, active, recency, int(b), 0, np.zeros(4, np.int64), 0) for b in bases]
        fills = None
    else:
        bases, fills = founders(rep, NI, Lx, c.get('renorm'), ff)
        tid = []
        for j in range(NI):
            f = np.zeros(4, np.int64); f[:len(fills[j])] = fills[j]
            tid.append(H.get_type(T, tdict, Lx.b_tags, active, recency, int(bases[j]), j, f, len(fills[j])))
    seed = (SALT * 7 + 1000003 * rep + (17 if ff else 0)) % (2 ** 31)      # common random numbers across cells
    if plain == 'stored':
        seed = 100003 * rep + 7 * N + I + int(mN * 1000)                     # almost_all_seeds.island_job's seed
    t0 = time.time()
    ts = []; at = {}
    es = np.zeros((4, 4, 4)); ctr = np.zeros(12, np.int64)
    if ff:
        ch1 = [x for x in CHECKS if x <= G['merge']]
        pres, cnt, ps, npres, Cl, rec_i, rec_g = _alloc(I, N, len(ch1))
        _place(pres, cnt, npres, tid, I, N, T)
        nrec = K.kernel(LA, Lx.b_tags, Lx.iC, Lx.iD, Lx.bD, T, tdict, ev, active, cfg, COPY_Q, H.PDPAY, pres, cnt, ps,
                        npres, Cl, N, W, mN / N, G['merge'], seed, np.array(ch1, np.int64), rec_i, rec_g, es, ctr)
        del Cl
        _ts(ts, ch1[:nrec], rec_i, rec_g)
        at[str(G['merge'])] = state_stats(Lx, T, ev, active, recency, pres, cnt, npres, rec_i[nrec - 1])
        comp = {}
        for i in range(I):
            for s_ in range(npres[i]):
                comp[int(pres[i, s_])] = comp.get(int(pres[i, s_]), 0) + int(cnt[i, s_])
        N2 = NI
        ch2 = sorted(set([x - G['merge'] for x in CHECKS if G['merge'] < x <= gens] + [gens - G['merge']]))
        cap2 = min(N2, FF_SLOTS)
        if len(comp) > cap2:
            raise RuntimeError('merged population has %d types > %d slots' % (len(comp), cap2))
        pres2, cnt2, ps2, npres2, Cl2, rec_i2, rec_g2 = _alloc(1, cap2, len(ch2))
        for t_ in sorted(comp):
            pres2[0, npres2[0]] = t_; cnt2[0, npres2[0]] = comp[t_]; npres2[0] += 1
        cfg2 = cfg.copy(); cfg2[8] = 1; cfg2[9] = 1
        nrec2 = K.kernel(LA, Lx.b_tags, Lx.iC, Lx.iD, Lx.bD, T, tdict, ev, active, cfg2, COPY_Q, H.PDPAY, pres2, cnt2,
                         ps2, npres2, Cl2, N2, W, 0.0, gens - G['merge'], seed + 1, np.array(ch2, np.int64), rec_i2,
                         rec_g2, es, ctr)
        _ts(ts, [x + G['merge'] for x in ch2[:nrec2]], rec_i2, rec_g2)
        at[str(gens)] = state_stats(Lx, T, ev, active, recency, pres2, cnt2, npres2, rec_i2[nrec2 - 1])
        conc = rec_i[1:nrec, :, 3].mean(0)
    else:
        pres, cnt, ps, npres, Cl, rec_i, rec_g = _alloc(I, N, len(CHECKS))
        done = 0; k = 0
        _place(pres, cnt, npres, tid, I, N, T)
        concs = []
        while done < gens:
            seg = min(SEG, gens - done)
            chk = [x - done for x in CHECKS if done < x <= done + seg] if done else [x for x in CHECKS if x <= seg]
            if chk[-1] != seg:
                chk.append(seg)
            cfg_k = cfg.copy(); cfg_k[8] = 1 if done == 0 else 0
            ri = np.zeros((len(chk), I, K.NREC_I)); rg = np.zeros((len(chk), K.NREC_G))
            nrec = K.kernel(LA, Lx.b_tags, Lx.iC, Lx.iD, Lx.bD, T, tdict, ev, active, cfg_k, COPY_Q, H.PDPAY, pres, cnt,
                            ps, npres, Cl, N, W, mN / N, seg, seed + k, np.array(chk, np.int64), ri, rg, es, ctr)
            _ts(ts, [x + done for x in chk[:nrec]], ri, rg)
            concs.append(ri[:nrec][[q for q in range(nrec) if chk[q] + done > 0], :, 3])
            done += seg; k += 1
            if nrec < len(chk):
                break
            at[str(done)] = state_stats(Lx, T, ev, active, recency, pres, cnt, npres, ri[nrec - 1])
        conc = np.concatenate(concs).mean(0)
    wall = time.time() - t0
    seeded = np.zeros((4, 2), np.int64)
    if fills is not None:
        for fl in fills:
            for f in fl:
                d = decode_fill(f); seeded[H.SCOPES.index(d['scope']), 1 if d['a'] == 'C' else 0] += 1
    row = dict(cell=cell, rep=rep, wall=round(wall, 1), gens=gens, ntypes=int(T[10][0]),
               live_types=int(T[10][0] - T[10][1]), overflow=int(ctr[8]), island_conc=[round(float(x), 4) for x in conc],
               counters=[int(x) for x in ctr], enc_stats=es.astype(np.int64).tolist(), seeded=seeded.tolist(), ts=ts,
               at=at)
    last = at[max(at, key=int)] if at else {}
    for key in ('eff_islands', 'pcc', 'efficient_run', 'universal_open', 'universal_target', 'universal_current',
                'lineage_closed', 'rival'):
        row[key] = last.get(key)
    return row


def _ts(ts, checks, rec_i, rec_g):
    for k, g in enumerate(checks):
        ri = rec_i[k]; rg = rec_g[k]
        ts.append(dict(gen=int(g), pcc=round(float(ri[:, 0].mean()), 5), eff=round(float((ri[:, 0] >= 0.95).mean()), 4),
                       isl_pcc=[round(float(x), 3) for x in ri[:, 0]],
                       lin=round(float(ri[:, 2].mean()), 3), conc=round(float(ri[:, 3].mean()), 5),
                       types=int(rg[66]), gentle=round(float(rg[64]), 5), gentle_holder=round(float(rg[65]), 5),
                       hist_holders=round(float(rg[68]), 5), fills_per=round(float(rg[67]), 4),
                       held=[int(x) for x in rg[:64]]))


def zlib_crc(s):
    import zlib
    return zlib.crc32(s.encode()) % 100003


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


# ------------------------------------------------------------------ post-run statistics
def decode_fill(f):
    f = int(f)
    a = (f - 1) & 1; t = ((f - 1) >> 1) & 1; sc = ((f - 1) >> 2) & 3; og = ((f - 1) >> 4) & 3; key = (f - 1) >> 6
    return dict(a='CD'[1 - a], t=t, scope=H.SCOPES[sc], origin=H.ORIGINS[og], key=int(key))


def type_desc(Lx, T, t):
    Tb, Tl, Tf, Tn = T[0], T[1], T[2], T[3]
    return dict(base=Lx.names[int(Tb[t])], lineage=int(Tl[t]),
                fills=['%s:%s:%s:%d:t%d' % (d['scope'], d['origin'], d['a'], d['key'], d['t']) for d in
                       (decode_fill(Tf[t, j]) for j in range(int(Tn[t])))])


def stranger_code(Lx, T, ev, a, b):
    """Match code of a vs b as strangers (fresh lineages for both: every context is 'no lineage')."""
    Tb, Ts0 = T[0], T[5]
    sa = int(Ts0[a]); sb = int(Ts0[b])
    return int(H.eval_code(Lx.arrays(), ev, Lx.iC, Lx.iD, int(Tb[a]), sa, sa, sa, int(Tb[b]), sb, sb, sb))


def fb_stranger(Lx, T, ev, a):
    Tb, Ts0 = T[0], T[5]
    sa = int(Ts0[a])
    return int(H.eval_code(Lx.arrays(), ev, Lx.iC, Lx.iD, int(Tb[a]), sa, sa, sa, Lx.FB, 0, 0, 0))


def state_stats(Lx, T, ev, active, recency, pres, cnt, npres, rec_i):
    """Island and run statistics of a population state (notes §1.10); rec_i: the record of that state."""
    pcc = rec_i[:, 0]
    eff = pcc >= 0.95
    maj = [int(x) for x in rec_i[:, 4]]
    LA = Lx.arrays()
    umaj = sorted(set(maj))
    comp = {}
    for a in umaj:
        for b in umaj:
            if (b, a) in comp:
                comp[(a, b)] = comp[(b, a)]
                continue
            comp[(a, b)] = (stranger_code(Lx, T, ev, a, b) & 3) == 3
    cur = {}
    for a in umaj:
        for b in umaj:
            cur[(a, b)] = (int(H.match(T, LA, ev, Lx.iC, Lx.iD, active, recency, a, b)) & 3) == 3
    open_all = all(comp[(a, b)] for a in umaj for b in umaj)
    cur_all = all(cur[(a, b)] for a in umaj for b in umaj)
    fbok = {a: (fb_stranger(Lx, T, ev, a) & 3) == 3 for a in umaj}
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
    desc = {str(t): type_desc(Lx, T, t) for t in types_seen}
    trait = {}
    Tf, Tn = T[2], T[3]
    for a in umaj:
        has_contract = any(((int(Tf[a, j]) - 1) >> 4) & 3 == H.CONTRACT for j in range(int(Tn[a])))
        trait[str(a)] = dict(open_self=bool(comp[(a, a)]), cur_self=bool(cur[(a, a)]), fb_mutual=bool(fbok[a]),
                             hooked=bool(Lx.b_tags[int(T[0][a])] > 0), has_contract=bool(has_contract))
    return dict(eff_islands=round(float(eff.mean()), 4), pcc=round(float(pcc.mean()), 5), efficient_run=bool(eff.all()),
                universal_open=bool(eff.all() and open_all),
                universal_target=bool(eff.all() and open_all and all(fbok.values())),
                universal_current=bool(eff.all() and cur_all), lineage_closed=round(float(np.mean(lin_closed)), 4),
                rival=round(float(np.mean(rival)), 4), island_pcc=[round(float(x), 4) for x in pcc],
                island_lin_closed=lin_closed, majority=maj, traits=trait, types=desc, comp=comp_out)


# ------------------------------------------------------------------ validation and drivers
def validate(nrep=20):
    """Baseline reproduction: the kernel with the plain grammar, one type per stored class and no encounters
    reproduces the stored modal (100, 64) rows (runs/almost-all-seeds-islands.json) draw for draw."""
    import modal as M
    import almost_all_seeds as AS
    d = AS.arm_data('modal', 6)
    Lp = lang(False)
    L, val, worlds, prov = M.build(6)
    reps = [Lp.bidx[min(mem, key=lambda c: (L.bits_canon[c], c))] for mem in prov.members]
    rows = [r for r in json.load(open(os.path.join(ROOT, 'runs', 'almost-all-seeds-islands.json')))
            if r['arm'] == 'modal' and r['N'] == 100 and r['I'] == 64 and r['mN'] == 1.0]
    rows.sort(key=lambda r: r['rep'])
    out = []
    LA = Lp.arrays()
    for r in rows[:nrep]:
        rep = r['rep']; N = 100; I = 64; mN = 1.0
        rng = np.random.default_rng([0, N, I, int(mN * 10), rep])
        init = np.zeros((I, len(d['mu'])), np.int64)
        for i in range(I):
            init[i] = rng.multinomial(N, d['mu'])
        T, tdict, ev = H.new_tables(10000)
        active = np.zeros((4, 4), np.bool_)
        for k in range(len(reps)):
            H.get_type(T, tdict, Lp.b_tags, active, 0, reps[k], 0, np.zeros(4, np.int64), 0)
        tname = {k: d['names'][k] for k in range(len(reps))}
        pres, cnt, ps, npres, Cl, rec_i, rec_g = _alloc(I, N, 1)
        for i in range(I):
            for k in range(len(reps)):
                if init[i, k] > 0:
                    pres[i, npres[i]] = k; cnt[i, npres[i]] = init[i, k]; npres[i] += 1
                    T[9][k] += init[i, k]
        cfg = np.zeros(11, np.int64); cfg[8] = 1
        seed = 100003 * rep + 7 * N + I + int(mN * 1000)
        es = np.zeros((4, 4, 4)); ctr = np.zeros(12, np.int64)
        K.kernel(LA, Lp.b_tags, Lp.iC, Lp.iD, Lp.bD, T, tdict, ev, active, cfg, 0.0, H.PDPAY, pres, cnt, ps, npres, Cl,
                 N, AS.W, mN / N, r['stop_gen'], seed, np.array([r['stop_gen']], np.int64), rec_i, rec_g, es, ctr)
        # type ids are recycled when a class dies out and comes back; name types by their base program
        glob = {}
        for i in range(I):
            for s in range(npres[i]):
                t_ = int(pres[i, s]); nm = d['names'][reps.index(int(T[0][t_]))]
                glob[nm] = glob.get(nm, 0) + int(cnt[i, s])
        mine = glob
        out.append(dict(rep=rep, stop_gen=r['stop_gen'], equal=mine == r['final'], pcc=float(rec_i[0, :, 0].mean()),
                        stored_pcc=r['pcc']))
        print(out[-1], flush=True)
    return out


def _job(args):
    cell, rep = args
    try:
        return run_one(cell, rep)
    except Exception as e:  # report, do not hide
        import traceback
        return dict(cell=cell, rep=rep, error=traceback.format_exc())


def run_cell(cell, reps, procs):
    from multiprocessing import Pool
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, '%s.json' % cell)
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {r['rep'] for r in rows if 'error' not in r}
    rows = [r for r in rows if 'error' not in r]
    jobs = [(cell, r) for r in range(reps) if r not in done]
    print('%s: %d jobs' % (cell, len(jobs)), flush=True)
    lang(True); lang(False)
    with Pool(procs, maxtasksperchild=4) as pool:
        for row in pool.imap_unordered(_job, jobs):
            rows.append(row)
            if 'error' in row:
                print('ERROR', row['cell'], row['rep'], row['error'], flush=True)
            else:
                print('%s rep %d: eff %.3f univ-open %s current %s lin-closed %.3f types %d (%.0fs)' % (
                    row['cell'], row['rep'], row['eff_islands'], row['universal_open'], row['universal_current'],
                    row['lineage_closed'], row['ntypes'], row['wall']), flush=True)
            json.dump(sorted(rows, key=lambda r: r['rep']), open(path, 'w'))


ORDER_PD = ['baseline', 'inert', 'maximal', 'seeding-only', 'grudge-only', 'no-contract', 'no-history', 'no-writes',
            'no-copy', 'no-seed', 'no-behaviour', 'no-role', 'hist-shuffled', 'hist-noinherit', 'no-behaviour-renorm',
            'no-history-renorm', 'recency', 'no-contract-strict', 'no-writes-strict', 'no-seed-strict']
ORDER_FF = ['ff-baseline', 'ff-inert', 'ff-maximal', 'ff-grudge-only']


def run_batch(cells, procs):
    """All runs of the listed cells through one pool (40 runs per island cell, 20 per fission-fusion cell),
    resumable: runs already in runs/hooks_w/CELL.json are skipped."""
    from multiprocessing import Pool
    os.makedirs(OUT, exist_ok=True)
    rows = {}
    jobs = []
    for cell in cells:
        path = os.path.join(OUT, '%s.json' % cell)
        rows[cell] = [r for r in (json.load(open(path)) if os.path.exists(path) else []) if 'error' not in r]
        done = {r['rep'] for r in rows[cell]}
        nrep = 20 if CELLS[cell].get('ff') else 40
        jobs += [(cell, r) for r in range(nrep) if r not in done]
    print('%d jobs' % len(jobs), flush=True)
    lang(True); lang(False)
    with Pool(procs, maxtasksperchild=8) as pool:
        for row in pool.imap_unordered(_job, jobs):
            cell = row['cell']
            if 'error' in row:
                print('ERROR', cell, row['rep'], row['error'], flush=True)
                continue
            rows[cell].append(row)
            print('%s rep %d: eff %.3f univ-open %s current %s lin-closed %.3f live %d (%.0fs)' % (
                cell, row['rep'], row['eff_islands'], row['universal_open'], row['universal_current'],
                row['lineage_closed'], row['live_types'], row['wall']), flush=True)
            json.dump(sorted(rows[cell], key=lambda r: r['rep']), open(os.path.join(OUT, '%s.json' % cell), 'w'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('cell', nargs='?')
    ap.add_argument('reps', nargs='?', type=int, default=40)
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--gens', type=int, default=None)
    a = ap.parse_args()
    if a.cmd == 'validate':
        out = validate()
        json.dump(out, open(os.path.join(ROOT, 'runs', 'hooks-w-validate.json'), 'w'), indent=1)
    elif a.cmd == 'time':
        for r in range(a.reps):
            t = time.time()
            row = run_one(a.cell, 1000 + r, gens=a.gens)
            print(a.cell, 'probe rep', 1000 + r, 'gens', a.gens, 'wall %.1f' % (time.time() - t), 'types', row['ntypes'],
                  'eff', row['eff_islands'], 'lin-closed', row['lineage_closed'], 'counters', row['counters'][:11], flush=True)
    elif a.cmd == 'run':
        run_cell(a.cell, a.reps, a.procs)
    elif a.cmd == 'batch':
        cells = {'pd': ORDER_PD, 'ff': ORDER_FF}.get(a.cell) or a.cell.split(',')
        run_batch(cells, a.procs)


if __name__ == '__main__':
    main()
