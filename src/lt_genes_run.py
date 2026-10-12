"""Driver for certificates as genes (predictions/2026-10-11-certificates-as-genes.md).

    python3 src/lt_genes_run.py static [--workers 3]       # unit closure, tables (the scale guard)
    python3 src/lt_genes_run.py validate                     # notes §1.12 validation by code
    python3 src/lt_genes_run.py pairs                        # single-pair tables
    python3 src/lt_genes_run.py graph                        # the transfer compatibility graph
    python3 src/lt_genes_run.py lottery --cells ...          # population cells
Raw arrays go to runs/lt_genes/ (npz/pkl, not committed); summaries to json.
"""
import argparse
import json
import os
import pickle
import subprocess
import sys
import time
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import lt_code as L
import lt_cert as C
import lt_genes as G
import lt_genes_pop as GP
import carrier_populations as CP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'lt_genes')
os.makedirs(OUT, exist_ok=True)
K = 10 ** 6
V = K // 4
PCAP = K // 4


def workers_allowed(req):
    """<= 3, and <= 10 - 3 * (running gene-arm drivers), minimum 1."""
    try:
        out = subprocess.run(['ps', '-eo', 'command'], capture_output=True, text=True).stdout
        n = sum(1 for line in out.splitlines() if 'gene_arm_run' in line and 'grep' not in line)
    except Exception:
        n = 0
    return max(1, min(req, 3, 10 - 3 * n))


def cmd_static(a):
    t0 = time.time()
    nw = workers_allowed(a.workers)
    print('workers', nw, flush=True)
    U = GP.Universe(K, PCAP, verbose=True)
    with Pool(nw, initializer=GP._winit, initargs=(K, PCAP)) as pool:
        Tb = GP.Tables(U, pool, verbose=True)
        cl = GP.Closure(Tb, verbose=True)
        rounds = cl.run()
        print('closure converged after %d rounds: units %d, scripts %d, checks %d (%.0fs check time), total %.0fs' % (
            rounds, len(U.units), len(U.scripts), Tb.n_checks, Tb.t_checks, time.time() - t0), flush=True)
        st = GP.finalize(cl, verbose=True)
    st['time_s'] = time.time() - t0
    GP.save_static(st, U, Tb, cl, os.path.join(OUT, 'static'))
    print('static done (%.0fs)' % (time.time() - t0), flush=True)


# ------------------------------------------------------------------ single-pair tables
CARRIERS = ['CB', 'CB1', 'CBP', 'CBlet', 'CBwrap', 'CB1r', 'CBPh', 'CBPr', 'MC1', 'LobC', 'Cc', 'Dc', 'CBdef', 'SFc']
FAKER_DONORS = ['CBfake', 'CBmut', 'Dcert', 'CBsloppy']
SETTINGS = {           # (x mode, x start, y mode, y start)
    'HH': ('H', 'mode', 'H', 'mode'), 'CH': ('C', 'mode', 'H', 'mode'), 'SH': ('S', 'mode', 'H', 'mode'),
    'CSH': ('CS', 'mode', 'H', 'mode'), 'CC': ('C', 'mode', 'C', 'mode'), 'CC+': ('C', 'mode', 'C', 'host'),
    'SS': ('S', 'mode', 'S', 'mode'), 'CSCS': ('CS', 'mode', 'CS', 'mode'),
}
_CATS = {}


def cat_at(Kc, Vc):
    if (Kc, Vc) not in _CATS:
        _CATS[(Kc, Vc)] = G.named_catalogue(Kc, Vc)
    return _CATS[(Kc, Vc)]


def run_seq(xn, yn, setting, Kc=K, Vc=None, P=None, E=5, alloc='post', reserve=0, negcache=False, rule='lack'):
    Vc = Kc // 4 if Vc is None else Vc
    P = Kc // 4 if P is None else P
    cat = cat_at(Kc, Vc)
    xm, xs, ym, ys = SETTINGS[setting]
    x = G.make_prog(cat, xn, xm, xs)
    y = G.make_prog(cat, yn, ym, ys)
    same = (xn == yn and xm == ym and xs == ys)
    nc = (set(), set()) if negcache else (None, None)
    encs = []
    for e in range(E):
        r = G.encounter(x, y, Kc, Vc, P, alloc=alloc, negcache=nc, self_play=same, reserve=reserve, rule=rule)
        encs.append(dict(
            act=r['ax'] + r['ay'], wx=r['wx'], wy=r['wy'], botx=bool(r['botx']), boty=bool(r['boty']),
            px=dict(r['accx'].steps), py=dict(r['accy'].steps),
            adx=[(a, C.show_script(s), how) for a, s, how in r['accx'].adopted],
            ady=[(a, C.show_script(s), how) for a, s, how in r['accy'].adopted],
            evx=[(k, v, n, d) for k, v, n, d in r['accx'].events], tox=r['accx'].timeouts, toy=r['accy'].timeouts))
        x, y = r['nx'], (r['nx'] if same else r['ny'])
    first_cc = next((e + 1 for e, h in enumerate(encs) if h['act'] == 'CC'), None)
    steady = None
    for e in range(E):
        if all(h['act'] == 'CC' for h in encs[e:]) and all(not h['adx'] and not h['ady'] for h in encs[e:]):
            steady = e + 1; break
    last = encs[-1]
    return dict(x=xn, y=yn, setting=setting, K=Kc, V=Vc, P=P, alloc=alloc, reserve=reserve, negcache=negcache, rule=rule,
                same_quote=same, first_cc=first_cc, steady_cc=steady,
                cost_x_last=last['wx'] + sum(last['px'].values()), cost_y_last=last['wy'] + sum(last['py'].values()),
                prod_x_last=sum(last['px'].values()), play_x_last=last['wx'],
                listx=[[C.show_script(s) for s in x.cseq], [C.show_script(s) for s in x.dseq]], ancx=list(x.anc),
                encs=encs)


def _pairs_job(job):
    sys.setrecursionlimit(1000000)
    return [run_seq(*args, **kw) for args, kw in job]


def cmd_pairs(a):
    t0 = time.time()
    specs = []
    for rule in ('lack', 'gate'):
        for st in SETTINGS:
            if rule == 'gate' and st == 'HH': continue
            for xn in CARRIERS:
                for yn in CARRIERS:
                    specs.append(((xn, yn, st), dict(rule=rule)))
        for st in ('CH', 'CSH'):
            for xn in CARRIERS + ['CF']:
                for yn in FAKER_DONORS + CARRIERS:
                    if xn == 'CF' or yn in FAKER_DONORS:
                        specs.append(((xn, yn, st), dict(rule=rule)))
            for xn in CARRIERS:
                for yn in CARRIERS + FAKER_DONORS:
                    specs.append(((xn, yn, st), dict(negcache=True, rule=rule)))
        capset = ['CB', 'CB1', 'CBP', 'CBPr', 'LobC', 'Cc', 'SFc']
        for Kc in (10 ** 5, 10 ** 6):
            for P in (Kc // 8, Kc // 4, Kc // 2):
                for st in ('SH', 'CSH', 'SS'):
                    for xn in capset:
                        for yn in capset:
                            if Kc == K and P == K // 4: continue
                            specs.append(((xn, yn, st), dict(Kc=Kc, P=P, rule=rule)))
            for st in ('SH', 'SS', 'HH'):
                for xn in capset:
                    for yn in capset:
                        specs.append(((xn, yn, st), dict(Kc=Kc // 2, P=Kc // 4, alloc='reserved', reserve=Kc // 2, rule=rule)))
    nw = workers_allowed(a.workers)
    chunks = [specs[i::nw * 8] for i in range(nw * 8)]
    rows = []
    with Pool(nw) as pool:
        for res in pool.imap_unordered(_pairs_job, chunks):
            rows.extend(res)
            print('pairs %d / %d (%.0fs)' % (len(rows), len(specs), time.time() - t0), flush=True)
    json.dump(rows, open(os.path.join(OUT, 'pairs.json'), 'w'))
    print('pairs done: %d sequences (%.0fs)' % (len(rows), time.time() - t0), flush=True)


def cmd_complete(a):
    """After the static: fill CH[C] at (adopted unit, donor) for every C adoption of the closure (the Lemma A
    transfer statistic needs them)."""
    t0 = time.time()
    path = os.path.join(OUT, 'static')
    st, meta = GP.load_static(path, mmap=False)
    U = GP.Universe(K, PCAP)
    U.scripts = list(meta['scripts']); U.sid = {k: i for i, k in enumerate(U.scripts)}
    U.units = list(meta['units']); U.uid = {k: i for i, k in enumerate(U.units)}
    n = len(U.units)
    nw = workers_allowed(a.workers)
    with Pool(nw, initializer=GP._winit, initargs=(K, PCAP)) as pool:
        Tb = GP.Tables(U, pool, verbose=True)
        Tb.CH['C'][:n, :n] = st['CHC']; Tb.CH['D'][:n, :n] = st['CHD']; Tb.UVt[:n] = st['UVt']
        cl = GP.Closure(Tb, verbose=True)
        cl.single = dict(meta['single'])
        for m in ('S', 'C', 'CS', 'H'):
            cl.reach[m] = set(st['reach_' + m].tolist())
        O = cl.O()
        units_c = sorted(cl.reach['C'] | cl.reach['CS'])
        succ = cl.successors_C(units_c, O)
        assert len(U.units) == n, 'closure not closed'
        tl, ml = [], []
        for u, (vs, u2s) in succ.items():
            ncs = len(U.units[u][1])
            for v, u2 in zip(vs.tolist(), u2s.tolist()):
                if len(U.units[u2][1]) > ncs:
                    tl.append(u2); ml.append(v)
        print('transfer pairs', len(tl), flush=True)
        Tb.ensure_pairs('C', np.array(tl), np.array(ml), label='(transfer)')
        np.save(os.path.join(path, 'CHC.npy'), Tb.CH['C'][:n, :n])
    print('complete (%.0fs)' % (time.time() - t0), flush=True)


# ------------------------------------------------------------------ validation and the cost model (before any cell)
def unit_prog(U, u, mode):
    """The Prog of unit u in a mode, on the τ's representative spelling (lt_genes encounter engine)."""
    t, cs, ds = U.units[u]
    return G.Prog('u%d' % u, U.bodies[t], mode, [U.scripts[i][1] for i in cs], [U.scripts[i][1] for i in ds])


def _val_job(job):
    """Term-executed checks of the population tables (validation and costs).  job = (kind, items)."""
    sys.setrecursionlimit(1000000)
    kind, items = job
    LS = _VS
    U = LS['U']
    out = []
    MODES = ('H', 'S', 'C', 'CS')
    for it in items:
        if len(L.CACHE) > 200000: L.CACHE.clear()
        if kind == 'play':
            x, y, rel = it
            px = unit_prog(U, x, 'H'); py = unit_prog(U, y, 'H' if rel == 2 else ('C' if rel == 1 else 'H'))
            if rel == 2: py = px
            ax, nx = L.play(px.term(), py.term(), K)
            ay, ny = L.play(py.term(), px.term(), K)
            out.append((it, ax, ay, nx, ny))
        elif kind == 'check':
            t, m, a, mark_t, mark_m = it
            tt = unit_prog(U, t, mark_t).term(); mm = unit_prog(U, m, mark_m).term()
            v, n = G.check_term(tt, mm, a, V, K, K)
            out.append((it, v, n))
        elif kind == 'prod':
            u, v, rel, a, key = it
            px = unit_prog(U, u, 'H')
            if v is None:
                yt = L.PROG_D
            elif rel == 2:
                yt = px.term()
            else:
                yt = unit_prog(U, v, 'C' if rel == 1 else 'H').term()
            s, n, oc = G.produce_term(px.term(), yt, a, V, K, PCAP, K)
            out.append((it, s, n, oc))
        elif kind == 'enc':
            u, v, mu, mv = it
            px = unit_prog(U, u, MODES[mu]); py = unit_prog(U, v, MODES[mv])
            r = G.encounter(px, py, K, V, PCAP)
            out.append((it, r['ax'], r['ay'], [U.sid.get(('C', s)) for s in r['nx'].cseq], [U.sid.get(('D', s)) for s in r['nx'].dseq],
                        [U.sid.get(('C', s)) for s in r['ny'].cseq], [U.sid.get(('D', s)) for s in r['ny'].dseq],
                        r['accx'].total(), r['accy'].total()))
        elif kind == 'marker':
            k = it
            cat = LS['cat']
            x = cat.sexprs[cat.spell[k]['i']]
            body = CP.body_term(x, V, K)
            cs, ds = G.host_list(body, K, V, mode='S')
            out.append((k, [C.show_script(s) for s in cs], [C.show_script(s) for s in ds], cat.spell[k]['lst']))
    return kind, out


_VS = {}


def _vinit():
    sys.setrecursionlimit(1000000)
    st, meta = GP.load_static(os.path.join(OUT, 'static'))
    U = GP.Universe(K, PCAP)
    U.scripts = list(meta['scripts']); U.sid = {k: i for i, k in enumerate(U.scripts)}
    U.units = list(meta['units']); U.uid = {k: i for i, k in enumerate(U.units)}
    _VS.update(U=U, st=st, meta=meta, cat=U.cat)


def cmd_validate(a):
    """notes §1.12 items 1-4 by code on samples; writes runs/lt_genes/validate.json and costs.json."""
    t0 = time.time()
    _vinit()
    st, meta, U = _VS['st'], _VS['meta'], _VS['U']
    A, selfa, O = st['A'], st['selfa'], st['O']
    rng = np.random.default_rng(20261011)
    n = len(meta['units'])
    reachall = set(O.tolist())
    acquired = [u for u in O.tolist() if u not in set(meta['H_unit'].tolist()) | set(meta['E_unit'].tolist())]
    jobs = []
    # 1. composition against whole actual plays: random pairs, acquired units, twins, self-plays
    pl = [(int(rng.choice(O)), int(rng.choice(O)), 0) for _ in range(600)]
    pl += [(int(rng.choice(acquired)), int(rng.choice(O)), 0) for _ in range(400)] if acquired else []
    pl += [(int(u), int(u), 1) for u in rng.choice(O, 150)] + [(int(u), int(u), 2) for u in rng.choice(O, 150)]
    pl = [(x, y, rel if (x != y or rel) else 1) for x, y, rel in pl]
    # 2. the tactic as code against the host memo: every C production memo entry and every D one
    pr = [(u, v, {'s': 2, 'w': 1, 'd': 0, 'D': 0}[rel], tag, key) for (tag, key), (u, v, rel) in meta['prod_rep'].items()]
    # 3. transitions against direct encounters executed by the term
    MODEI = {'H': 0, 'S': 1, 'C': 2, 'CS': 3}
    en = []
    for m in ('S', 'C', 'CS'):
        R = st['reach_' + m]
        for _ in range(250):
            en.append((int(rng.choice(R)), int(rng.choice(O)), MODEI[m], 0))
    # 4. marker invariance of the H lists
    mk = [int(k) for k in rng.choice(len(U.cat.spell), 300, replace=False)]
    # 5. costs: adoption checks, gates (with and without C entries)
    singles = list(meta['single'].items())
    ac = []
    blc = st['BLC']
    donors = {}
    for u in O.tolist():
        for s_ in U.units[u][1]: donors.setdefault(s_, []).append(u)
    csing = [(k, xs) for k, xs in singles if U.scripts[k[1]][0] == 'C' and donors.get(k[1])]
    for _ in range(400):
        (t, sid), xs = csing[int(rng.integers(len(csing)))]
        ac.append((xs, int(rng.choice(donors[sid])), 'C', 'C', 'H'))
    gates = []
    sr = [u for u in st['reach_S'].tolist() if blc[u, 0] >= 0]
    for _ in range(400):
        gates.append((int(rng.choice(sr)), int(rng.choice(O)), 'C', 'H', 'H'))
    g0 = [u for u in O.tolist() if blc[u, 0] < 0]
    for _ in range(100):
        gates.append((int(rng.choice(g0)), int(rng.choice(O)), 'C', 'H', 'H'))
    nw = workers_allowed(a.workers)
    allj = [('play', pl[i::nw * 4]) for i in range(nw * 4)] + [('prod', pr[i::nw * 8]) for i in range(nw * 8)] + \
           [('enc', en[i::nw * 4]) for i in range(nw * 4)] + [('marker', mk[i::nw * 2]) for i in range(nw * 2)] + \
           [('check', (ac + gates)[i::nw * 4]) for i in range(nw * 4)]
    res = {'play': [], 'prod': [], 'enc': [], 'marker': [], 'check': []}
    with Pool(nw, initializer=_vinit) as pool:
        for kind, out in pool.imap_unordered(_val_job, allj):
            res[kind].extend(out)
    rep = {}
    # plays
    mism = []
    for (x, y, rel), ax, ay, nx, ny in res['play']:
        if rel == 2:
            want = ('C' if selfa[x] == 1 else 'D',) * 2
        else:
            want = ('C' if A[x, y] == 1 else 'D', 'C' if A[y, x] == 1 else 'D')
        got = (ax if ax in ('C', 'D') else 'D', ay if ay in ('C', 'D') else 'D')
        if got != want: mism.append([x, y, rel, want, got])
    rep['plays'] = dict(n=len(res['play']), mismatches=mism[:20], n_mismatch=len(mism))
    # productions
    pm = []
    pcost = {'C': [], 'D': []}
    for (u, v, rel, tag, key), s, nsteps, oc in res['prod']:
        memo = meta['prodC'] if tag == 'C' else meta['prodD']
        sid = memo.get(key)
        want = None if (sid is None or sid < 0) else U.scripts[sid][1]
        if want != s: pm.append([u, v, rel, tag, oc])
        pcost[tag].append(nsteps)
    json.dump([[tag, list(key), oc] for (u, v, rel, tag, key), s_, n_, oc in res['prod']], open(os.path.join(OUT, 'prod_exec.json'), 'w'))
    n_cap = sum(1 for z in res['prod'] if z[3] in ('capTO', 'fuelTO'))
    pm_nocap = [z for z in pm if z[4] not in ('capTO', 'fuelTO')]
    rep['productions'] = dict(n=len(res['prod']), n_mismatch=len(pm), n_cap_timeouts=n_cap, n_mismatch_not_cap=len(pm_nocap), mismatches=pm[:20],
                              cost_C=dict(median=float(np.median(pcost['C'])), max=int(max(pcost['C'])), q90=float(np.quantile(pcost['C'], 0.9))) if pcost['C'] else None,
                              cost_D=dict(median=float(np.median(pcost['D'])), max=int(max(pcost['D']))) if pcost['D'] else None)
    # encounters vs the tables
    em = []
    for (u, v, mu, mv), ax, ay, ncs, nds, ycs, yds, cx, cy in res['enc']:
        rel = 1 if u == v else 0
        # table transition (python mirror of the kernel)
        want = table_transition(st, U, u, v, rel, mu)
        got = U.uid.get((U.units[u][0], tuple(ncs), tuple(nds)))
        if want != got: em.append([u, v, mu, want, got])
    rep['encounters'] = dict(n=len(res['enc']), n_mismatch=len(em), mismatches=em[:20])
    # markers
    mm = []
    for k, cs, ds, lst in res['marker']:
        c0, d0 = G.split_list(lst)
        if cs != [C.show_script(s) for s in c0] or ds != [C.show_script(s) for s in d0]: mm.append(k)
    rep['marker'] = dict(n=len(res['marker']), n_mismatch=len(mm))
    # checks: executable against ideal, and costs
    cm = []
    costs = {'ac': [], 'gate': [], 'gate0': []}
    for (t, m, a_, mt, mm_), v, nsteps in res['check']:
        ideal = st['CHC'][t, m] if t != m else st['CHC'][t, t]
        if ideal >= 0 and (v == 'T') != (ideal == 1): cm.append([t, m, v, int(ideal)])
        kind = 'ac' if mt == 'C' else ('gate' if blc[t, 0] >= 0 else 'gate0')
        costs[kind].append(nsteps + 6)
    rep['checks_exec_vs_ideal'] = dict(n=len(res['check']), n_compared=sum(1 for (t, m, a_, mt, mm_), v, n_ in res['check'] if st['CHC'][t, m] >= 0),
                                       n_mismatch=len(cm), mismatches=cm[:20])
    cj = dict(ac=float(np.median(costs['ac'])), gate=float(np.median(costs['gate'])), gate0=float(np.median(costs['gate0'])),
              prodC=rep['productions']['cost_C']['median'], prodD=rep['productions']['cost_D']['median'],
              surgery=float(np.median([G.data_size(G.canon_list([U.scripts[s][1]], [])) + 5 for (t, s) in meta['single'] if U.scripts[s][0] == 'C'])),
              ac_q90=float(np.quantile(costs['ac'], 0.9)), gate_q90=float(np.quantile(costs['gate'], 0.9)),
              n=dict(ac=len(costs['ac']), gate=len(costs['gate']), gate0=len(costs['gate0'])))
    rep['costs'] = cj
    # identity: for non-split run trees the kernel treats two individuals of one unit and mode as twins; count the
    # units whose S transition differs between self-play and twin play (the approximation's reach)
    utau = st['utau']
    split_tau = set(int(utau[u]) for u in O.tolist() if st['split'][u])
    diff, diff_nonsplit = 0, 0
    for u in sorted(set(st['reach_S'].tolist()) | set(st['reach_CS'].tolist())):
        a1 = table_transition(st, U, u, u, 1, 1); a2 = table_transition(st, U, u, u, 2, 1)
        if a1 != a2:
            diff += 1
            if int(utau[u]) not in split_tau: diff_nonsplit += 1
    rep['identity'] = dict(split_units=int(st['split'][O].sum()), split_tau=len(split_tau), S_self_vs_twin_diff=diff,
                           S_self_vs_twin_diff_nonsplit=diff_nonsplit, tracked_tau=len(tracked_tau(st)))
    rep['time_s'] = time.time() - t0
    json.dump(rep, open(os.path.join(OUT, 'validate.json'), 'w'), indent=1, default=str)
    json.dump(cj, open(os.path.join(OUT, 'costs.json'), 'w'), indent=1)
    print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != 'mismatches'}) for k, v in rep.items()}, indent=1, default=str))


def patched(st, path=None):
    """PRODC and PD with the executable producer's cap timeouts (-3), from runs/lt_genes/prod_exec.json (the term run
    of every signature's representative, validate)."""
    PRODC = np.array(st['PRODC']); PD = np.array(st['PD'])
    path = path or os.path.join(OUT, 'prod_exec.json')
    if not os.path.exists(path): return PRODC, PD, 0, 0
    ex = json.load(open(path))
    nC = nD = 0
    capD = set()
    for tag, key, oc in ex:
        if oc != 'capTO' and oc != 'fuelTO': continue
        if tag == 'C':
            PRODC[key[0], key[1]] = -3; nC += 1
        else:
            capD.add((key[0], key[1])); nD += 1
    if capD:
        utau, code = st['utau'], st['PDCODE']
        for u in np.nonzero(code >= 0)[0].tolist():
            if (int(utau[u]), int(code[u])) in capD: PD[u] = -3
    return PRODC, PD, nC, nD


def table_transition(st, U, u, v, rel, mode):
    """Python mirror of the kernel's transition on units (for validation)."""
    import lt_genes_kern as KN
    dctr = np.zeros(KN.NCTR, np.int64)
    cost = np.zeros(1)
    COSTS = np.zeros(6)
    uu, anc = u, 0
    if mode in (2, 3):
        uu, anc = KN.trans_C(uu, v, rel, 0, 0, st['utau'], st['BLC'], st['BLD'], st['SINGLE'], st['APP'], st['CHC'], st['UVt'], dctr, cost, COSTS)
    if mode in (1, 3):
        rel2 = rel if (uu == u or rel == 2) else (1 if uu == v else 0)
        PRODC, PD, _, _ = patched(st)
        uu, anc = KN.trans_S(uu, v, rel2, anc, st['utau'], st['BLC'], st['BLD'], st['APP'], PRODC, PD, st['KIND'], st['NAT'],
                             st['CHC'], st['CHD'], st['UVt'], dctr, cost, COSTS)
    return int(uu)


# ------------------------------------------------------------------ the frozen-inventory chain (a diagnostic only)
def chain_job(job):
    """LogChain (FastChain monomorphic fates) over lumped classes with inventories frozen at their founding values:
    'mixedF' = H lists with prior 1/4, certificate-less (S/C/CS founders) 3/4; 'H' = every list produced.  This is
    NOT the ε→0 object of the gene dynamics (a static table cannot carry inherited lists)."""
    import math as _m
    from chain_log import LogChain, NEG
    from dollar_partitions import ClassProvider
    import solver_audit as SA
    import carrier_populations_run as CPR
    cell, N, noclosed = job
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    st, meta = GP.load_static(os.path.join(OUT, 'static'), mmap=False)
    cat = CP.Catalogue(7, 'P', K)
    mu_sp = cat.spelling_mass('L'); mu_sp = mu_sp / mu_sp.sum()
    Hu, Eu = meta['H_unit'], meta['E_unit']
    A, selfa, utau = st['A'], st['selfa'], st['utau']
    split_tau = set(int(utau[u]) for u in st['O'].tolist() if st['split'][u])
    wH = 1.0 if cell == 'H' else 0.25
    cls = {}
    for k in range(len(cat.spell)):
        t = int(cat.tau[k])
        for u, w in ((int(Hu[t]), wH), (int(Eu[t]), 1.0 - wH)):
            if w == 0: continue
            key = (u, k if t in split_tau else -1)
            cls[key] = cls.get(key, 0.0) + w * mu_sp[k]
    keys = sorted(cls)
    n = len(keys)
    us = np.array([k[0] for k in keys]); sps = np.array([k[1] for k in keys])
    Acl = A[np.ix_(us, us)].astype(np.int64)
    for i in range(n):
        Acl[i, i] = selfa[us[i]] if sps[i] >= 0 else A[us[i], us[i]]
    mu = np.array([cls[k] for k in keys])
    # exact lumping on the action pair (rows and columns with the diagonal)
    R = 2 * Acl + Acl.T
    groups = {}
    for i in range(n):
        groups.setdefault((R[i].tobytes(), R[:, i].tobytes()), []).append(i)
    reps = [g[0] for g in groups.values()]
    Ac = Acl[np.ix_(reps, reps)]
    muc = np.array([mu[g].sum() for g in groups.values()])
    names = ['%s|%s' % (cat.name(cat.members[utau[us[i]]][0]), 'H' if us[i] in set(Hu.tolist()) else 'E') for i in reps]
    if noclosed:
        from carrier_populations_report import leak_test
        keep = np.arange(len(reps))
        while True:
            lt = leak_test(Ac[np.ix_(keep, keep)])
            cl = sorted({int(keep[i]) for c in lt['closed'] for i in c})
            if not cl: break
            keep = np.array([k for k in keep if k not in set(cl)])
        Ac = Ac[np.ix_(keep, keep)]; muc = muc[keep]; names = [names[k] for k in keep]
    U, PCC = CP.pay_matrix(Ac)
    muc = muc / muc.sum()
    pool = np.argsort(-muc)[:120]
    cands, counts = SA.enumerate_candidates_fast(U, muc, pool=pool)
    S1, n1, comp1 = SA.invasion_closure(U, muc, max_nodes=6000, branch=3)
    seeds = [(x['ids'], x['x']) for x in cands + S1 if x['size'] > 1 and x['status'] == 'stable']
    CH = CPR.fast_chain_class()
    ch = CH(ClassProvider(U, muc), N=N, w=0.3, Ufull=U, twins=True, theta=1.0, max_states=10 ** 9)
    ch.explore_log(extra_states=[(list(s[0]), list(s[1])) for s in seeds], log_theta=-14 * _m.log(10), max_states=20000)
    keys_all, lpi_all, sinfo, out_un, rec = ch.solve_sparse()
    kk = [keys_all[i] for i in rec]
    pi = np.exp(lpi_all[rec])
    pcc = 0.0
    top = []
    for i in np.argsort(-pi)[:8]:
        ids, x, kind = ch.states[kk[i]]
        c = float(np.asarray(x) @ PCC[np.ix_(list(ids), list(ids))] @ np.asarray(x))
        top.append(dict(state=' + '.join('%s:%.2f' % (names[j], xi) for j, xi in zip(ids, x)), pi=float(pi[i]), coop=c))
    for i, k in enumerate(kk):
        ids, x, kind = ch.states[k]
        pcc += pi[i] * float(np.asarray(x) @ PCC[np.ix_(list(ids), list(ids))] @ np.asarray(x))
    return dict(cell=cell, N=N, noclosed=noclosed, classes_before=n, classes=int(len(muc)), pcc=float(pcc), top=top,
                n_states=len(keys_all), time_s=time.time() - t0)


def cmd_chain(a):
    jobs = [(c, N, nc) for c in a.cells for N in a.N for nc in (False, True)]
    nw = workers_allowed(a.workers)
    rows = []
    with Pool(nw) as pool:
        for r in pool.imap_unordered(chain_job, jobs):
            rows.append(r)
            print(json.dumps(r)[:1500], flush=True)
            json.dump(rows, open(os.path.join(OUT, 'chain.json'), 'w'), indent=1)


# ------------------------------------------------------------------ the transfer compatibility graph
def cmd_graph(a):
    """notes §1.11: donors = every run tree's H unit; recipients = every run tree in mode C with an empty list."""
    t0 = time.time()
    st, meta = GP.load_static(os.path.join(OUT, 'static'))
    units, scripts = meta['units'], meta['scripts']
    Hu, Eu = meta['H_unit'], meta['E_unit']
    T = len(Hu)
    SINGLE, CHC, UVt, A, selfa = st['SINGLE'], st['CHC'], st['UVt'], st['A'], st['selfa']
    import lt_genes_kern as KN
    cat = CP.Catalogue(7, 'P', K)
    mu = cat.spelling_mass('L'); mu = mu / mu.sum()
    tmass = np.zeros(T); np.add.at(tmass, cat.tau, mu)
    names = [cat.name(k) for k in range(len(cat.spell))]
    u_d = int(Hu[cat.tau[names.index('D')]])
    est = np.array([selfa[Hu[t]] == 1 and A[Hu[t], u_d] == 0 for t in range(T)])
    native_C = [set(units[Hu[t]][1]) for t in range(T)]
    cedge = np.zeros((T, T), bool)       # cedge[y, x]: donor y -> recipient x
    dedge = np.zeros((T, T), bool)
    script_C_recips = {}
    for y in range(T):
        uy = Hu[y]
        cs, ds = units[uy][1], units[uy][2]
        for s in cs:
            xs = SINGLE[:, s]
            ok = xs >= 0
            vals = np.zeros(T, bool)
            vals[ok] = CHC[xs[ok], uy] == 1
            cedge[y] |= vals
            script_C_recips.setdefault(s, set()).update(np.nonzero(vals)[0].tolist())
        for s in ds:
            xs = SINGLE[:, s]
            ok = xs >= 0
            vals = np.zeros(T, bool)
            vals[ok] = UVt[xs[ok], GP.UVI[('D', '^D')]] == 1
            dedge[y] |= vals
    np.fill_diagonal(cedge, cedge.diagonal())   # self edges kept (a copier of the donor's own run tree)
    # cross-skeleton C edges: the recipient's native C scripts do not include the donor's accepted script
    cross = []
    for y in range(T):
        for x in np.nonzero(cedge[y])[0].tolist():
            acc = [s for s in units[Hu[y]][1] if SINGLE[x, s] >= 0 and CHC[SINGLE[x, s], Hu[y]] == 1]
            if not any(s in native_C[x] for s in acc):
                cross.append((y, x, acc))
    # cooperation at encounter 2 under (C, H) against the graph, for establisher pairs that cooperate under (H, H)
    dctr = np.zeros(KN.NCTR, np.int64)
    viol_on, viol_off, n_on, n_off, n_pre = [], [], 0, 0, 0
    for y in np.nonzero(est)[0].tolist():
        uy = Hu[y]
        for x in np.nonzero(est)[0].tolist():
            if x == y: continue
            ux = Hu[x]
            if not (A[ux, uy] == 1 and A[uy, ux] == 1): continue
            u2, _ = KN.trans_C(Eu[x], uy, 0, 0, 0, st['utau'], st['BLC'], st['BLD'], SINGLE, st['APP'], CHC, UVt, dctr,
                               np.zeros(1), np.zeros(5))
            coop = A[u2, uy] == 1 and A[uy, u2] == 1
            coop1 = A[Eu[x], uy] == 1 and A[uy, Eu[x]] == 1
            if coop1:
                n_pre += 1
                continue
            if cedge[y, x]:
                n_on += 1
                if not coop: viol_on.append((y, x))
            else:
                n_off += 1
                if coop: viol_off.append((y, x))
    est_idx = np.nonzero(est)[0]
    indeg = cedge[np.ix_(est_idx, est_idx)].sum(0)
    # components of the C-edge graph on establishers (undirected)
    parent = {int(t): int(t) for t in est_idx}

    def find(z):
        while parent[z] != z:
            parent[z] = parent[parent[z]]; z = parent[z]
        return z
    for y in est_idx.tolist():
        for x in est_idx.tolist():
            if cedge[y, x] and x != y:
                parent[find(y)] = find(x)
    comps = {}
    for t in est_idx.tolist(): comps.setdefault(find(t), []).append(t)
    compsz = sorted([(len(v), float(tmass[v].sum())) for v in comps.values()], reverse=True)
    blocks = {C.show_script(scripts[s][1]): dict(recipients=len(r), recip_mass=float(tmass[list(r)].sum()),
                                                  donors=int(sum(1 for t in range(T) if s in units[Hu[t]][1])))
              for s, r in script_C_recips.items()}
    out = dict(T=T, n_C_edges=int(cedge.sum() - np.trace(cedge)), n_C_self=int(np.trace(cedge)),
               n_D_edges=int(dedge.sum() - np.trace(dedge)), n_est=int(est.sum()), est_mass=float(tmass[est].sum()),
               cross_skeleton_C_edges=len(cross), cross_examples=[(cat.name(cat.members[y][0]), cat.name(cat.members[x][0]),
                                                                  [C.show_script(scripts[s][1]) for s in acc]) for y, x, acc in cross[:25]],
               cross_recipients=sorted({cat.name(cat.members[x][0]) for y, x, acc in cross})[:60],
               est_pairs_HH_coop_already_at_enc1=n_pre, est_pairs_HH_coop_on_graph=n_on, est_pairs_HH_coop_off_graph=n_off,
               violations_on_graph_no_coop=len(viol_on), violations_off_graph_coop=len(viol_off),
               viol_on_examples=[(cat.name(cat.members[y][0]), cat.name(cat.members[x][0])) for y, x in viol_on[:15]],
               viol_off_examples=[(cat.name(cat.members[y][0]), cat.name(cat.members[x][0])) for y, x in viol_off[:15]],
               est_C_indegree=dict(zero=int((indeg == 0).sum()), median=float(np.median(indeg)), max=int(indeg.max())),
               est_components=compsz[:15], n_est_components=len(comps), blocks=blocks,
               d_dense=dict(frac_recipients_of_delta=float(dedge.any(0).mean())), time_s=time.time() - t0)
    json.dump(out, open(os.path.join(OUT, 'graph.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ('blocks', 'cross_examples', 'cross_recipients')}, indent=1))


# ------------------------------------------------------------------ the lottery
CELLS = {
    # name: (N, I, mode spec, start, f0, donor, publish, inherit, price, r)
    'H': (100, 64, 'H', 'mode', 0, False, True, True, 0.0, 50),
    'mixed': (100, 64, 'mix', 'mode', 0, False, True, True, 0.0, 50),
    'S': (100, 64, 'S', 'mode', 0, False, True, True, 0.0, 50),
    'CS': (100, 64, 'CS', 'mode', 0, False, True, True, 0.0, 50),
    'C0': (100, 64, 'C', 'mode', 0, False, True, True, 0.0, 50),
    'C05': (100, 64, 'C', 'mode', 0.05, False, True, True, 0.0, 50),
    'C25': (100, 64, 'C', 'mode', 0.25, False, True, True, 0.0, 50),
    'Cdonor': (100, 64, 'C', 'mode', 0, True, True, True, 0.0, 50),
    'C25pub0': (100, 64, 'C', 'mode', 0.25, False, False, True, 0.0, 50),
    'C25inh0': (100, 64, 'C', 'mode', 0.25, False, True, False, 0.0, 50),
    'mixedH': (100, 64, 'mix', 'host', 0, False, True, True, 0.0, 50),
    'price001': (100, 64, 'mix', 'mode', 0, False, True, True, 0.01, 50),
    'price01': (100, 64, 'mix', 'mode', 0, False, True, True, 0.1, 50),
    'price1': (100, 64, 'mix', 'mode', 0, False, True, True, 1.0, 50),
    'price10': (100, 64, 'mix', 'mode', 0, False, True, True, 10.0, 50),
    'mixed_N50': (50, 64, 'mix', 'mode', 0, False, True, True, 0.0, 25),
    'mixed_N200': (200, 64, 'mix', 'mode', 0, False, True, True, 0.0, 100),
    'C25_N50': (50, 64, 'C', 'mode', 0.25, False, True, True, 0.0, 25),
    'C25_N200': (200, 64, 'C', 'mode', 0.25, False, True, True, 0.0, 100),
    'mixed_r1': (100, 64, 'mix', 'mode', 0, False, True, True, 0.0, 1),
    'C25_r1': (100, 64, 'C', 'mode', 0.25, False, True, True, 0.0, 1),
    'Cdonor_r1': (100, 64, 'C', 'mode', 0, True, True, True, 0.0, 1),
}
SALT = 20261011
SNAPS = (10, 50, 200, 1000, 2000)
_LS = {}


def tracked_tau(st):
    """Run trees whose types keep the spelling: a split unit (twin play != self play) or a unit whose S transition
    differs between self-play and twin play."""
    import lt_genes_kern as KN
    utau = st['utau']
    out = set(int(utau[u]) for u in st['O'].tolist() if st['split'][u])
    PRODC, PD, _, _ = patched(st)
    dctr = np.zeros(KN.NCTR, np.int64)
    for u in sorted(set(st['reach_S'].tolist()) | set(st['reach_CS'].tolist())):
        r = []
        for rel in (1, 2):
            uu, _ = KN.trans_S(u, u, rel, 0, st['utau'], st['BLC'], st['BLD'], st['APP'], PRODC, PD, st['KIND'], st['NAT'],
                               st['CHC'], st['CHD'], st['UVt'], dctr, np.zeros(1), np.zeros(6))
            r.append(uu)
        if r[0] != r[1]: out.add(int(utau[u]))
    return out


def lot_static():
    if 'st' in _LS: return _LS
    import lt_genes_kern as KN
    st, meta = GP.load_static(os.path.join(OUT, 'static'))
    cat = CP.Catalogue(7, 'P', K)
    mu = cat.spelling_mass('L')
    n = len(meta['units'])
    split_unit = st['split']
    utau = st['utau']
    split_tau = np.zeros(cat.T, bool)
    for t in tracked_tau(st):
        split_tau[t] = True
    PRODC, PD, nC, nD = patched(st)
    st = dict(st); st['PRODC'] = PRODC; st['PD'] = PD
    sp_tau = cat.tau.astype(np.int64)
    Hu, Eu = meta['H_unit'].astype(np.int64), meta['E_unit'].astype(np.int64)
    FU = np.stack([Hu, Eu, Eu, Eu]).astype(np.int64)
    A, selfa = st['A'], st['selfa']
    # the D carrier and CB (H units) for establisher and open-family labels
    names = [cat.name(k) for k in range(len(cat.spell))]
    k_cb = names.index('if(CHK(them,me,C),C,D)'); k_d = names.index('D')
    u_cb = int(Hu[sp_tau[k_cb]]); u_d = int(Hu[sp_tau[k_d]])
    O = st['O']
    est_unit = np.zeros(n, bool)
    est_unit[O] = (selfa[O] == 1) & (A[O, u_d] == 0)
    hasC = st['BLC'][:, 0] >= 0
    donor_ok = np.array([est_unit[Hu[sp_tau[k]]] and hasC[Hu[sp_tau[k]]] for k in range(len(names))])
    # identity cliques: self-cooperating units that mutually cooperate with no other reachable unit
    mutual = (A[np.ix_(O, O)] == 1) & (A[np.ix_(O, O)].T == 1)
    np.fill_diagonal(mutual, False)
    ident = np.zeros(n, bool)
    ident[O] = (selfa[O] == 1) & (~mutual.any(1)) & (A[O, O] == 0)
    costs = json.load(open(os.path.join(OUT, 'costs.json')))
    COSTS = np.array([costs['ac'] + costs['surgery'], costs['gate'], costs['gate0'], costs['prodC'], costs['prodD'], PCAP + 5], float)
    _LS.update(st=st, meta=meta, cat=cat, mu=mu / mu.sum(), split_tau=split_tau, sp_tau=sp_tau, FU=FU, u_cb=u_cb,
               u_d=u_d, est_unit=est_unit, donor_ok=donor_ok, ident=ident, COSTS=COSTS, KN=KN, n_units=n)
    return _LS


def lottery_job(job):
    cell, rep, gens = job
    sys.setrecursionlimit(1000000)
    LS = lot_static()
    KN = LS['KN']
    st, meta, cat = LS['st'], LS['meta'], LS['cat']
    N, I, mspec, start, f0, donor, publish, inherit, price, r = CELLS[cell]
    nsp = len(LS['mu'])
    rng = np.random.default_rng([N, I, rep, SALT])
    sp = rng.choice(nsp, size=(I, N), p=LS['mu'])
    r_mode = np.random.default_rng([N, I, rep, SALT, 1])
    r_seed = np.random.default_rng([N, I, rep, SALT, 2])
    r_don = np.random.default_rng([N, I, rep, SALT, 3])
    modes = {'H': 0, 'S': 1, 'C': 2, 'CS': 3}
    if mspec == 'mix':
        mode = r_mode.integers(0, 4, size=(I, N))
    else:
        mode = np.full((I, N), modes[mspec], np.int64)
    seeded = (r_seed.random(size=(I, N)) < f0) if f0 > 0 else np.zeros((I, N), bool)
    if donor:
        pd = LS['mu'] * LS['donor_ok']; pd = pd / pd.sum()
        for i in range(I):
            j = int(r_don.integers(N))
            sp[i, j] = int(r_don.choice(nsp, p=pd)); mode[i, j] = 0
    tau = LS['sp_tau'][sp]
    Hu, Eu = meta['H_unit'], meta['E_unit']
    unit0 = np.where((mode == 0) | (start == 'host') | seeded, Hu[tau], Eu[tau])
    spid = np.where(LS['split_tau'][tau], sp, -1)
    KCAP = 100000
    tunit = np.zeros(KCAP, np.int64); tmode = np.zeros(KCAP, np.int64); tsp = np.zeros(KCAP, np.int64)
    tanc = np.zeros(KCAP, np.int64)
    from numba.typed import Dict
    from numba import types
    d = Dict.empty(key_type=types.int64, value_type=types.int64)
    nt = 0
    slots = np.zeros((I, N), np.int64)
    for i in range(I):
        for j in range(N):
            k, nt = KN.make_type(d, tunit, tmode, tsp, tanc, nt, int(unit0[i, j]), int(mode[i, j]), int(spid[i, j]), 0)
            slots[i, j] = k
    ntv = np.array([nt], np.int64)
    counts = np.zeros((I, KCAP), np.int64)
    for i in range(I):
        np.add.at(counts[i], slots[i], 1)
    pres = np.zeros((I, N), np.int64); npres = np.zeros(I, np.int64); pos = -np.ones((I, KCAP), np.int64)
    paysum = np.zeros((I, KCAP)); pcs = np.zeros((I, KCAP))
    A, selfa = st['A'], st['selfa']
    for i in range(I):
        ks = np.nonzero(counts[i])[0]
        for t, k in enumerate(ks):
            pres[i, t] = k; pos[i, k] = t
        npres[i] = len(ks)
    KN.init_paysum(counts, paysum, pcs, pres, npres, tunit, tmode, tsp, tanc, A, selfa, price, st['utau'], st['BLC'],
                   st['BLD'], st['SINGLE'], st['APP'], st['PRODC'], st['PD'], st['KIND'], st['NAT'], st['CHC'],
                   st['CHD'], st['UVt'], publish, LS['COSTS'])
    ctr = np.zeros((4, KN.NCTR), np.int64)
    steps_mode = np.zeros(4)
    err = np.zeros(1, np.int64)
    KN.seed_rng(int(7919 * rep + 13 * N + I + 100003 * (0 if r == 50 else 1)))
    t0 = time.time()
    every = 10
    trace = []
    snaps = {}
    estab = -1
    e3_gen, e3_out = -1, None
    last_g = gens
    ever90 = np.zeros(I, bool)
    for c in range(gens // every):
        g0 = c * every
        KN.segment(every, N, 0.3, 1.0 / N, r, publish, inherit, price, float(K), slots, counts, paysum, pcs, pres,
                   npres, pos, d, tunit, tmode, tsp, tanc, ntv, LS['FU'], st['utau'], st['BLC'], st['BLD'],
                   st['SINGLE'], st['APP'], st['PRODC'], st['PD'], st['KIND'], st['NAT'], st['CHC'], st['CHD'],
                   st['UVt'], A, selfa, LS['COSTS'], ctr, steps_mode, err)
        if err[0] != 0:
            raise RuntimeError('kernel error %d in %s rep %d at checkpoint %d (types %d)' % (err[0], cell, rep, c, ntv[0]))
        g = g0 + every
        cc, maj, majn = KN.island_stats(counts, pres, npres, N, tunit, tmode, tsp, A, selfa)
        if estab < 0 and (cc >= 0.9).any(): estab = g
        ever90 |= cc >= 0.9
        glob = np.nonzero(counts[:, :ntv[0]].sum(0))[0]
        if e3_gen < 0 and len(glob) <= 3000:
            stt = KN.e3_status(counts, pres, npres, glob.astype(np.int64), len(glob), tunit, tmode, tsp, A, selfa)
            if (stt >= 0).all():
                e3_gen = g; e3_out = 'success' if (stt == 1).all() else 'fail'
        trace.append((g, float(cc.mean()), int((cc >= 0.9).sum()), int(len(glob))))
        if g in SNAPS:
            snaps[g] = snapshot(LS, counts, ntv[0], tunit, tmode, tsp, tanc, cc, maj, majn, N, pres, npres)
        if len(glob) == 1 and g >= 50:
            k = int(glob[0])
            if snapshot_frozen(LS, k, tunit, tmode, tsp, tanc):
                last_g = g
                for gs in SNAPS:
                    if gs > g and gs not in snaps:
                        snaps[gs] = snaps.get(g) or snapshot(LS, counts, ntv[0], tunit, tmode, tsp, tanc, cc, maj, majn, N, pres, npres)
                break
    cc, maj, majn = KN.island_stats(counts, pres, npres, N, tunit, tmode, tsp, A, selfa)
    fin = snaps.get(gens) or snapshot(LS, counts, ntv[0], tunit, tmode, tsp, tanc, cc, maj, majn, N, pres, npres)
    glob = counts[:, :ntv[0]].sum(0)
    top_types = []
    units, scripts = meta['units'], meta['scripts']
    for k in np.argsort(-glob)[:12].tolist():
        if glob[k] == 0: break
        t, cs, ds = units[tunit[k]]
        top_types.append(dict(prog=cat.name(cat.members[t][0]), mode='HSCX'[tmode[k]], n=int(glob[k]),
                              C=[C.show_script(scripts[i][1]) for i in cs], D=[C.show_script(scripts[i][1]) for i in ds],
                              anc=int(tanc[k]), selfc=int(KN.cc_pair(k, k, tunit, tmode, tsp, A, selfa))))
    persist = float((ever90 & (cc >= 0.9)).sum() / ever90.sum()) if ever90.any() else None
    return dict(cell=cell, rep=rep, N=N, I=I, gens=gens, last_gen=last_g, establish_gen=estab, E3_gen=e3_gen,
                ever90=int(ever90.sum()), persistence=persist,
                E3=e3_out if e3_out else 'censored', trace=trace[::5] + [trace[-1]], snaps={str(k): v for k, v in snaps.items()},
                final=fin, top_types=top_types, ctr=ctr.tolist(), steps_mode=steps_mode.tolist(), n_types=int(ntv[0]),
                time_s=time.time() - t0)


def snapshot_frozen(LS, k, tunit, tmode, tsp, tanc):
    """A single global type that its own encounters do not change."""
    st = LS['st']
    if tmode[k] == 0: return True
    KN = LS['KN']
    dctr = np.zeros(KN.NCTR, np.int64)
    u = tunit[k]
    for rel in (1, 2):
        if tmode[k] in (2, 3):
            u2, _ = KN.trans_C(u, u, rel, tanc[k], tanc[k], st['utau'], st['BLC'], st['BLD'], st['SINGLE'], st['APP'],
                               st['CHC'], st['UVt'], dctr, np.zeros(1), LS['COSTS'])
            if u2 != u: return False
        if tmode[k] in (1, 3):
            u2, _ = KN.trans_S(u, u, rel, tanc[k], st['utau'], st['BLC'], st['BLD'], st['APP'], st['PRODC'], st['PD'],
                               st['KIND'], st['NAT'], st['CHC'], st['CHD'], st['UVt'], dctr, np.zeros(1), LS['COSTS'])
            if u2 != u: return False
    return True


def snapshot(LS, counts, nt, tunit, tmode, tsp, tanc, cc, maj, majn, N, pres_g=None, npres_g=None):
    """Holder-based outcome, modes of cooperative holders, scripts held with ancestry, identity islands."""
    st, meta = LS['st'], LS['meta']
    A, selfa = st['A'], st['selfa']
    KN = LS['KN']
    I = counts.shape[0]
    cnt = counts[:, :nt]
    glob = cnt.sum(0)
    present = np.nonzero(glob)[0]
    selfc = np.array([KN.cc_pair(k, k, tunit, tmode, tsp, A, selfa) for k in range(nt)]) if nt else np.zeros(0)
    held = np.array([selfc[maj[i]] > 0.5 and cc[i] >= 0.5 for i in range(I)])
    holders = [int(maj[i]) for i in range(I)]
    univ_pairs = True
    for i in range(I):
        for j in range(i + 1, I):
            if KN.cc_pair(holders[i], holders[j], tunit, tmode, tsp, A, selfa) < 0.5:
                univ_pairs = False; break
        if not univ_pairs: break
    allheld = bool(held.all())
    if allheld and univ_pairs: outcome = 'universal'
    elif allheld: outcome = 'patchwork'
    else: outcome = 'unheld'
    ucb = LS['u_cb']
    open_h = [bool(A[tunit[h], ucb] == 1 and A[ucb, tunit[h]] == 1) for h in holders]
    ident_h = [bool(LS['ident'][tunit[h]]) for h in holders]
    # modes among individuals of self-cooperating holder types... on held islands: every self-cooperating individual
    mode_c = np.zeros(4)
    for i in range(I):
        if not held[i]: continue
        for k in np.nonzero(cnt[i])[0]:
            if selfc[k] > 0.5: mode_c[tmode[k]] += cnt[i, k]
    # scripts held: instances with ancestry
    units = meta['units']
    sc = {}
    inst_host = inst_search = 0
    for k in present.tolist():
        t, cs, ds = units[tunit[k]]
        for pos_, s in enumerate(cs):
            bit = (tanc[k] >> pos_) & 1
            sc.setdefault(s, [0, 0])[bit] += int(glob[k])
        for pos_, s in enumerate(ds):
            bit = (tanc[k] >> (6 + pos_)) & 1
            sc.setdefault(s, [0, 0])[bit] += int(glob[k])
    for s, (h, se) in sc.items():
        inst_host += h; inst_search += se
    # host-free C scripts held by individuals whose type mutually cooperates with a present type of another unit
    hf_distinct = 0 if len(present) <= 1500 else None
    for k in (present.tolist() if len(present) <= 1500 else []):
        t, cs, ds = units[tunit[k]]
        if not any(((tanc[k] >> p) & 1) for p in range(len(cs))): continue
        for j in present.tolist():
            if tunit[j] != tunit[k] and KN.cc_pair(k, j, tunit, tmode, tsp, A, selfa) > 0.5:
                hf_distinct += int(glob[k]); break
    cross = float(KN.cross_pcc(counts, pres_g, npres_g, N, tunit, tmode, tsp, A, selfa)) if pres_g is not None else None
    return dict(pcc=float(cc.mean()), islands90=int((cc >= 0.9).sum()), held=int(held.sum()), outcome=outcome,
                universal_open=bool(outcome == 'universal' and all(open_h)), open_islands=int(sum(open_h[i] and held[i] for i in range(I))),
                identity_islands=int(sum(ident_h[i] and held[i] for i in range(I))), cross_pcc=float(cross),
                mode_coop=(mode_c / max(1, mode_c.sum())).tolist(), mode_all=np.bincount(tmode[present], weights=glob[present], minlength=4).tolist(),
                scripts_held=len(sc), script_inst={str(s): v for s, v in sc.items()},
                inst_host=int(inst_host), inst_search=int(inst_search), hostfree_distinct_coop=int(hf_distinct),
                n_present=int(len(present)))


def cmd_lottery(a):
    path = os.path.join(OUT, 'lottery_%s.json' % a.out)
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {(r['cell'], r['rep']) for r in rows}
    jobs = [(c, rep, a.gens) for c in a.cells for rep in range(a.runs) if (c, rep) not in done]
    nw = workers_allowed(a.workers)
    print('lottery jobs %d, workers %d' % (len(jobs), nw), flush=True)
    t0 = time.time()
    with Pool(nw) as pool:
        for r in pool.imap_unordered(lottery_job, jobs, chunksize=1):
            rows.append(r)
            json.dump(rows, open(path, 'w'))
            f = r['final']
            print('%s rep %d: estab %d E3 %s@%d pcc %.3f held %d %s open %d ident %d modes %s types %d (%.0fs, total %.0fs)' % (
                r['cell'], r['rep'], r['establish_gen'], r['E3'], r['E3_gen'], f['pcc'], f['held'], f['outcome'],
                f['open_islands'], f['identity_islands'], [round(x, 2) for x in f['mode_coop']], r['n_types'],
                r['time_s'], time.time() - t0), flush=True)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('static'); s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('pairs'); s.add_argument('--workers', type=int, default=1)
    s = sub.add_parser('validate'); s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('graph')
    s = sub.add_parser('filltransfer'); s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('chain'); s.add_argument('--cells', nargs='+', default=['mixedF']); s.add_argument('--N', type=int, nargs='+', default=[10000])
    s.add_argument('--workers', type=int, default=2)
    s = sub.add_parser('lottery'); s.add_argument('--cells', nargs='+'); s.add_argument('--runs', type=int, default=40)
    s.add_argument('--gens', type=int, default=2000); s.add_argument('--workers', type=int, default=3)
    s.add_argument('--out', default='main')
    a = ap.parse_args()
    {'static': cmd_static, 'pairs': cmd_pairs, 'lottery': cmd_lottery, 'validate': cmd_validate, 'graph': cmd_graph, 'chain': cmd_chain, 'filltransfer': cmd_complete}[a.cmd](a)


if __name__ == '__main__':
    main()
