"""Driver of the unequal-basin experiment: cells, starts, ablations, tilt scans (spec specs/2026-10-31-unequal-basin.md).

    python3 src/unequal_basin_run.py prep CELL                       # post-anneal diagnostics of a cell
    python3 src/unequal_basin_run.py ode CELL START [M] [ABL]        # one mean-field run (START nat|fair|uneq|wd|u:<u>)
    python3 src/unequal_basin_run.py scan CELL [M] [ABL]             # tilt scan on U, u*, bisection

Cells (founding charge | migration charge | A):   L0 = L 0|0|0, L01 = L 0.1|0.1|0, M0 = M |0|0, L0x = L 0|0.1|0 (crossed),
L0A = L 0|0|150, M0A = M 0|0|150.  Rows go to runs/unequal_basin/rows/<key>.json, endpoint states and caches to the scratch
directory (not committed).  M is the truncation order (default 1): see notes 1.5 and 2.
"""
import os, sys, json, time, hashlib, itertools
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dollar3 as D
import many_islands as MI
import unequal_basin as UB
import unequal_basin_core as UC

ROWS = os.path.join(UC.OUTD, 'rows')
XS = os.path.join(UC.SCR, 'xstar')
ABLD = os.path.join(UC.SCR, 'abl')
for d in (ROWS, XS, ABLD):
    os.makedirs(d, exist_ok=True)

CELLS = {
    'L0': dict(arm='L', pf_found=0.0, pf_migr=0.0, A=0),
    'L01': dict(arm='L', pf_found=0.1, pf_migr=0.1, A=0),
    'L0x': dict(arm='L', pf_found=0.0, pf_migr=0.1, A=0),
    'M0': dict(arm='M', pf_found=0.0, pf_migr=0.0, A=0),
    'L0A': dict(arm='L', pf_found=0.0, pf_migr=0.0, A=150),
    'M0A': dict(arm='M', pf_found=0.0, pf_migr=0.0, A=150),
}
SCAN_U = (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
_CELLCACHE = {}


def cell_of(name, pools=(0, 1, 2), symmetrize=True):
    k = (name, tuple(pools), symmetrize)
    if k not in _CELLCACHE:
        c = CELLS[name]
        _CELLCACHE[k] = UB.Cell(c['arm'], c['pf_found'], c['A'], pools, symmetrize)
    return _CELLCACHE[k]


# ====================================================================== program families (syntactic, slot-0-frame features)
def program_features(arm):
    """per program x and slot s: dict of features of a conditional: partner j read, the atom action's target
    ('self', 'third', 'all') and demand index, the true/false branch targets and demands."""
    S = arm.S
    feats = [[None] * len(S.fs) for _ in range(3)]
    for s in range(3):
        for x, f in enumerate(S.fs):
            atoms, tab = f
            if len(atoms) == 0:
                feats[s][x] = None
                continue
            (L, jr, al) = atoms[0]
            j = D.others(s)[jr]
            pa = D.partner_abs(j, al)
            tgt = 'all' if pa == D.ALL else ('self' if pa == s else 'third')
            bt = D.partner_abs(s, tab[1]); bf = D.partner_abs(s, tab[0])
            feats[s][x] = dict(j=j, atom_tgt=tgt, atom_d=al % 3, t_tgt=('all' if bt == D.ALL else ('j' if bt == j else 'k')), t_d=tab[1] % 3,
                               f_tgt=('all' if bf == D.ALL else ('j' if bf == j else 'k')), f_d=tab[0] % 3, tab=tab)
    return feats


def family_mask(arm, name):
    """boolean masks (3, K) of the programs of a syntactic family, S3-closed (defined without reference to slot labels)."""
    feats = program_features(arm)
    K = len(arm.S.fs)
    m = np.zeros((3, K), bool)
    for s in range(3):
        for x in range(K):
            f = feats[s][x]
            if f is None:
                continue
            ok = False
            if name == 'A1':
                ok = True
            elif name == 'read-me':
                ok = f['atom_tgt'] == 'self'
            elif name == 'read-third':
                ok = f['atom_tgt'] == 'third'
            elif name == 'read-all':
                ok = f['atom_tgt'] == 'all'
            elif name == 'yielder':
                ok = f['atom_tgt'] == 'self' and f['atom_d'] == 2 and f['t_tgt'] == 'j' and f['t_d'] == 0
            elif name == 'exploiter':
                ok = f['atom_tgt'] == 'self' and f['atom_d'] == 0 and f['t_tgt'] == 'j' and f['t_d'] == 2
            elif name == 'exploiter-fair':
                ok = (f['atom_tgt'] == 'self' and f['atom_d'] == 0 and f['t_tgt'] == 'j' and f['t_d'] == 2
                      and f['f_tgt'] == 'k' and f['f_d'] == 1)
            elif name == 'fair-reader':
                ok = f['atom_tgt'] == 'self' and f['atom_d'] == 1 and f['t_tgt'] == 'j' and f['t_d'] == 1
            elif name == 'bully-branch':
                ok = (f['t_tgt'] != 'all' and f['t_d'] == 2) or (f['f_tgt'] != 'all' and f['f_d'] == 2)
            elif name == 'true-names-j':
                ok = f['t_tgt'] == 'j'
            else:
                raise ValueError(name)
            m[s, x] = ok
    return m


def orbit_mask(arm, rm):
    """close a (3, K) removal mask under S3 (slot-and-program images)."""
    out = rm.copy()
    for sg, perm in UB.perm_maps(arm):
        for s in range(3):
            xs = np.nonzero(rm[s])[0]
            out[sg[s], perm[s][xs]] = True
    return out


# ====================================================================== ablated start laws
def ablate_law(cell, removed, rule='reassign'):
    """(trip, w, supp) with the programs flagged in removed (3, K) taken out of the symmetrized post-anneal triple law.
    rule 'reassign': a removed program in slot s is replaced by each constant in proportion to the constants' own slot-s
    marginal (the arm-T rule at the triple level); 'drop': the triples are dropped and the law renormalized."""
    isc = cell.isc
    cons = np.array([x for x in range(UB.KP) if isc[x]])
    trip, w = cell.trip.copy(), cell.w.copy()
    q0 = np.zeros((3, UB.KP))
    for s in range(3):
        q0[s] = np.bincount(trip[:, s], weights=w, minlength=UB.KP)
    for s in range(3):
        hit = removed[s][trip[:, s]]
        if not hit.any():
            continue
        if rule == 'drop':
            trip, w = trip[~hit], w[~hit]
            continue
        cm = q0[s, cons] / q0[s, cons].sum()
        kt, kw = trip[~hit], w[~hit]
        ht, hw = trip[hit], w[hit]
        rt = np.repeat(ht, len(cons), axis=0)
        rw = np.repeat(hw, len(cons)) * np.tile(cm, len(ht))
        rt[:, s] = np.tile(cons, len(ht))
        trip = np.concatenate([kt, rt])
        w = np.concatenate([kw, rw])
    k = UB.keys_of(trip)
    uk, inv = np.unique(k, return_inverse=True)
    w2 = np.bincount(inv, weights=w)
    trip2 = UB.decode_keys(uk)
    w2 = w2 / w2.sum()
    supp = []
    for s in range(3):
        sp = set(int(v) for v in np.unique(trip2[:, s])) | set(int(c) for c in cons)
        sp = {v for v in sp if not removed[s][v]}
        supp.append(sorted(sp))
    return trip2, w2, supp


def law_to_state(obj, trip, w):
    pos, ok = obj.index_of(trip)
    x = np.bincount(pos[ok], weights=w[ok], minlength=obj.n)
    dropped = float(w[~ok].sum())
    return x / x.sum(), dropped


# ====================================================================== one run
def key_of(spec):
    s = json.dumps(spec, sort_keys=True, default=str)
    return spec['cell'] + '_m%d_%s_%s_' % (spec['m'], spec['start'].replace(':', ''), spec.get('abl') or 'full') + hashlib.md5(s.encode()).hexdigest()[:8]


def build_obj_start(spec, remove=None, rule='reassign', pools=None, core=None):
    c = CELLS[spec['cell']]
    cell = cell_of(spec['cell'], tuple(pools or spec.get('pools') or (0, 1, 2)), not spec.get('raw', False))
    if remove is not None:
        trip, w, supp = ablate_law(cell, remove, rule)
    else:
        trip, w, supp = cell.trip, cell.w, cell.supp
    obj = UB.Obj(c['arm'], c['pf_migr'], supp, spec['m'], core=core, symmetric=not spec.get('raw', False))
    xn, dropped = law_to_state(obj, trip, w)
    return cell, obj, xn, dropped


def make_start(obj, xn, start):
    if start == 'nat':
        return xn, dict(kind='nat', available=True, after=obj.class_shares(xn).tolist())
    if start in ('fair', 'uneq', 'wd'):
        kind = {'fair': 'fair', 'uneq': 'unequal', 'wd': 'wd'}[start]
        return UB.tilt(obj, xn, kind, 0.6)
    if start.startswith('u:'):
        return UB.tilt(obj, xn, 'unequal', float(start[2:]))
    raise ValueError(start)


def endpoint_diag(obj, x, tail_recs):
    """class shares, pair split, support (programs per slot above 1e-9 donor mass), rare-class growth for the certificate."""
    sh, pairs = obj.class_shares(x, True)
    q = obj.marg(x)
    F = UB.field(obj, x, True)
    d = dict(shares=sh.tolist(), pairs=pairs.tolist(), support=[int((q[s] > 1e-9).sum()) for s in range(3)],
             support12=[int((q[s] > 1e-12).sum()) for s in range(3)])
    # relative growth rate of each (slot, program)'s donor mass
    dq = np.zeros((3, UB.KP))
    for s in range(3):
        dq[s] = np.bincount(obj.pid[s], weights=F, minlength=UB.KP)
    rare = []
    for s in range(3):
        ok = (q[s] > 0) & (q[s] < 1e-3)
        r = np.zeros(UB.KP)
        r[ok] = dq[s][ok] / q[s][ok]
        i = int(np.argmax(r))
        rare.append(dict(slot=s, max_rate=float(r[i]), prog=i, q=float(q[s][i]),
                         t_to_0p01=(float(np.log(1e-2 / q[s][i]) / r[i]) if r[i] > 0 and q[s][i] < 1e-2 else None),
                         n_growing=int((r > 0).sum())))
    d['rare_growth'] = rare
    d['top_donors'] = [[(int(i), float(q[s][i])) for i in np.argsort(-q[s])[:12]] for s in range(3)]
    return d


def run_one(spec, remove=None, rule='reassign', core=None, pools=None, force=False, keep_x=True, verbose=False, tmax=1e7):
    """spec: cell, m, start, abl (label).  Returns the row (and writes it)."""
    key = key_of(spec)
    path = os.path.join(ROWS, key + '.json')
    if os.path.exists(path) and not force:
        return json.load(open(path))
    t0 = time.time()
    cell, obj, xn, dropped = build_obj_start(spec, remove, rule, pools, core)
    x0, tinfo = make_start(obj, xn, spec['start'])
    row = dict(spec=spec, key=key, states=obj.n, dropped_mass=dropped, start_info=tinfo, support_start=[len(s) for s in obj.supp])
    if x0 is None:
        row.update(status='unavailable')
        json.dump(row, open(path, 'w'))
        return row
    recs, xe, status, kept = UB.run_ode(obj, x0, tmax, sym=not spec.get('raw', False), verbose=verbose)
    row['status'] = status
    row['records'] = [dict(t=r['t'], shares=r['shares'], pairs=r['pairs'], resid=r['resid']) for r in recs]
    row['t_end'] = recs[-1]['t']
    row['endpoint'] = UB.classify_endpoint(recs[-1]['shares'])
    row['diag'] = endpoint_diag(obj, xe, recs)
    row['wall'] = time.time() - t0
    if keep_x:
        np.savez_compressed(os.path.join(XS, key + '.npz'), x=xe)
    json.dump(row, open(path, 'w'), default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
    return row


def share_at(row, t):
    best = None
    for r in row['records']:
        if abs(r['t'] - t) <= 1e-9 * max(1, t):
            best = r
    return best['shares'] if best else None


def scan_ustar(spec_base, remove=None, rule='reassign', core=None, us=SCAN_U, refine=0.02, verbose=True):
    """tilt scan on U: endpoint class at each scanned u, bisection of every transition to +-refine.  Returns dict(table,
    ustar, range)."""
    table = {}
    for u in us:
        sp = dict(spec_base, start='u:%g' % u)
        r = run_one(sp, remove, rule, core)
        table[u] = (r['status'], r['endpoint'], r['records'][-1]['shares'] if r.get('records') else None, r['t_end'] if 't_end' in r else None)
        if verbose:
            print('  u=%.2f -> %s %s t=%s' % (u, table[u][1], table[u][0], table[u][3]), flush=True)
    keys = sorted(table)
    refined = []
    for a, b in zip(keys[:-1], keys[1:]):
        if table[a][1] != table[b][1]:
            lo, hi = a, b
            while hi - lo > refine + 1e-12:
                mid = round(0.5 * (lo + hi), 4)
                sp = dict(spec_base, start='u:%g' % mid)
                r = run_one(sp, remove, rule, core)
                table[mid] = (r['status'], r['endpoint'], r['records'][-1]['shares'], r['t_end'])
                if verbose:
                    print('  bisect u=%.3f -> %s' % (mid, table[mid][1]), flush=True)
                if r['endpoint'] == table[lo][1]:
                    lo = mid
                else:
                    hi = mid
            refined.append((lo, hi))
    keys = sorted(table)
    ustar = None
    for u in keys:
        if table[u][1] == 'U':
            ustar = u
            break
    if ustar is not None:
        # first U-dominated crossing: the midpoint of the bracketing refined interval if one ends there
        for lo, hi in refined:
            if table[hi][1] == 'U' and table[lo][1] != 'U' and hi <= ustar + 1e-9:
                ustar = hi
                break
    return dict(table={('%g' % u): [table[u][0], table[u][1], table[u][3]] for u in keys}, ustar=ustar, range=[min(keys), max(keys)],
                refined=refined)


# ====================================================================== post-anneal diagnostics of a cell
def prep(name):
    import unequal_basin_validate as UV
    c = CELLS[name]
    cell = cell_of(name)
    arm = cell.arm
    PAY2, VEC2 = UC.tables2(c['pf_migr'] if name != 'L0x' else c['pf_found'])
    out = dict(cell=name, spec=c, n_islands=cell.n_islands, settled=cell.n_settled,
               capped=[p['capped'] for p in cell.npool], distinct_sym_triples=len(cell.trip))
    # class shares per pool and union (outcome classes of the raw triples)
    def shares(trip, w=None):
        code2 = UB.codes_of(arm, trip.astype(np.int16))
        cl = MI.CATMAP[VEC2[code2]]
        w = np.ones(len(trip)) / len(trip) if w is None else w
        sh = np.bincount(cl, weights=w, minlength=5)
        div = float(w[(code2 // 729) > 0].sum())
        return sh.tolist(), div
    per = []
    off = 0
    for p, info in zip(cell.pools, cell.npool):
        tr, _ = UC.load_pool2(c['arm'], c['pf_found'], c['A'], p)
        sh, dv = shares(tr)
        per.append(dict(pool=p, shares=sh, diverging_mass=dv, n=len(tr)))
    out['per_pool'] = per
    sh, dv = shares(cell.trip, cell.w)
    out['union_shares_sym'] = sh
    out['union_diverging_mass'] = dv
    isc = cell.isc
    out['cond_mass_per_slot'] = [float(sum(cell.w[~isc[cell.trip[:, s]]])) for s in range(3)]
    out['support_per_slot'] = [len(s) for s in cell.supp]
    out['support_cond_per_slot'] = [int(sum(1 for x in s if not isc[x])) for s in cell.supp]
    out['seed_absent_mass'] = cell.seed_absent_mass()
    # single pool supports
    ps = []
    for p in cell.pools:
        tr, _ = UC.load_pool2(c['arm'], c['pf_found'], c['A'], p)
        ps.append([len(np.unique(tr[:, s])) for s in range(3)])
    out['support_single_pool'] = ps
    # lumping
    cc = UV.class_counts(c['arm'], cell.supp, slots=(0,))
    out['classes_slot0'] = cc[0]
    # tilt inflation (E9): conditional share of the U class vs natural, per slot
    cl_all = MI.CATMAP[VEC2[UB.codes_of(arm, cell.trip.astype(np.int16))]]
    infl = []
    for s in range(3):
        cond = (~isc[cell.trip[:, s]])
        tot = cell.w.sum()
        for k, nm in enumerate(UB.CLS):
            sel = cl_all == k
            if cell.w[sel].sum() > 0:
                infl.append(dict(slot=s, cls=nm, cond_share=float(cell.w[sel & cond].sum() / cell.w[sel].sum())))
        infl.append(dict(slot=s, cls='all', cond_share=float(cell.w[cond].sum() / tot)))
    out['cond_share_by_class'] = infl
    with open(os.path.join(UC.OUTD, 'prep-%s.json' % name), 'w') as f:
        json.dump(out, f, indent=1)
    return out


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'prep':
        print(json.dumps(prep(sys.argv[2]), indent=1))
    elif cmd == 'ode':
        cell, start = sys.argv[2], sys.argv[3]
        m = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        r = run_one(dict(cell=cell, m=m, start=start, abl=None), verbose=True, force=True)
        print(json.dumps({k: r[k] for k in ('status', 'endpoint', 't_end', 'wall')}))
    elif cmd == 'scan':
        cell = sys.argv[2]
        m = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        r = scan_ustar(dict(cell=cell, m=m, abl=None))
        print(json.dumps(r, default=str))


