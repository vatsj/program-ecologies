"""Driver for the world-K reruns (notes/world-k.md, predictions/2026-10-18-world-k-reruns.md).

    python3 src/world_k_run.py validate [--workers 3]     # reproduction: L vs stored scaling and Pangaea rows, K vs the
                                                          # detectors run's Cis_K0_e0 rows; lineage on/off; K tables
    python3 src/world_k_run.py statics                    # notes §2: static sets, deterministic family dynamics L and K
    python3 src/world_k_run.py probe --jobs ...           # cost probes on a discarded replicate (990)
    python3 src/world_k_run.py cells --part A|B|C|N|D [--workers 3] [--reps 20] [--cells ...]
Rows go to runs/world_k/*.json.gz (not committed if large); summaries to runs/world-k.json.
"""
import argparse
import gzip
import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import world_k as WK

OUT = WK.OUT
os.makedirs(OUT, exist_ok=True)
EXT_ALL, EXT_NONE = 1, 0


def log(*a):
    print(*a, flush=True)


def js(x):
    if isinstance(x, dict): return {str(k): js(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [js(v) for v in x]
    if isinstance(x, np.integer): return int(x)
    if isinstance(x, np.floating): return None if not np.isfinite(x) else float(x)
    if isinstance(x, float): return None if not np.isfinite(x) else x
    if isinstance(x, np.bool_): return bool(x)
    if isinstance(x, np.ndarray): return js(x.tolist())
    return x


def any_job(job):
    """Dispatch: ('I', cell, rep, w, horizon[, track]) island job; ('P', cell, rep, w, gens, ext) Pangaea job."""
    t0 = time.time()
    if job[0] == 'I':
        r = WK.island_job(job[1:])
    else:
        r = WK.pg_job(job[1:])
    r['kind'] = job[0]
    r['time_s'] = time.time() - t0
    return js(r)


def jkey(j):
    return (j[1], j[2], j[3])


def rkey(r):
    return (r['cell'], r['rep'], r['world'])


def run_pool(jobs, path, workers):
    rows = json.load(gzip.open(path)) if os.path.exists(path) else []
    done = {rkey(r) for r in rows}
    todo = [j for j in jobs if jkey(j) not in done]
    log('%s: %d jobs, %d done, %d to run on %d workers (pid %d)' % (os.path.basename(path), len(jobs), len(done),
                                                                    len(todo), workers, os.getpid()))
    if not todo: return rows
    t0 = time.time(); last = time.time()
    with Pool(min(3, workers), maxtasksperchild=6) as pool:
        for r in pool.imap_unordered(any_job, todo):
            rows.append(r)
            log('  %s' % short(r) + ' (%.0fs; total %.0fs)' % (r['time_s'], time.time() - t0))
            if time.time() - last > 60:
                with gzip.open(path + '.tmp', 'wt') as f: json.dump(rows, f)
                os.replace(path + '.tmp', path); last = time.time()
    with gzip.open(path + '.tmp', 'wt') as f: json.dump(rows, f)
    os.replace(path + '.tmp', path)
    return rows


def short(r):
    if r['kind'] == 'I':
        f = r['final']
        s2 = r['snaps'].get('2000', {})
        return '%s %s rep %d: uo2k %s uoEnd %s cls %s pcc %.3f static %s last %d' % (
            r['cell'], r['world'], r['rep'], s2.get('universal_open'), f['universal_open'],
            ''.join(sorted(f['cls'])).replace('o', '')[:20] or '-', f['pcc'], r['static']['label'], r['last_gen'])
    f = r['final']
    return '%s %s rep %d: uo %s M %.3f target %.3f AP %.3f status %s last %d' % (
        r['cell'], r['world'], r['rep'], f.get('uo'), f.get('M', 0), f.get('target', 0), r.get('max_AP', 0),
        f.get('status'), r['last_gen'])


# ------------------------------------------------------------------------------------------------ cells
def jobs_for(part, reps, rep0=0, only=None):
    jobs = []
    W = ('L', 'K')
    if part == 'A':
        for c in WK.CELLS_A:
            N, I = WK.CELLS[c]['N'], WK.CELLS[c]['I']
            nr = 40 if ((N, I) == (100, 64) and WK.CELLS[c]['tag'] == 'Snon') else reps
            for rep in range(rep0, rep0 + nr):
                for w in W:
                    jobs.append(('I', c, rep, w, 10000, N <= 400))
    elif part == 'B':
        for c in WK.CELLS_B:
            N, I = WK.CELLS[c]['N'], WK.CELLS[c]['I']
            nr = 40 if (N, I) == (100, 64) else reps
            for rep in range(rep0, rep0 + nr):
                for w in W:
                    jobs.append(('I', c, rep, w, 10000, True))
    elif part == 'D':
        for rep in range(rep0, rep0 + reps):
            for w in W:
                jobs.append(('I', WK.CELL_RAIN, rep, w, 10000, True))
    elif part == 'C':
        for c in WK.PG_CONT + WK.PG_FF + WK.PG_PANG:
            for rep in range(rep0, rep0 + reps):
                for w in W:
                    jobs.append(('P', c, rep, w, 2000, EXT_ALL))
    elif part == 'N':
        for c in WK.PG_NAT:
            for rep in range(rep0, rep0 + reps):
                for w in W:
                    jobs.append(('P', c, rep, w, 2000, EXT_NONE))
    if only:
        jobs = [j for j in jobs if j[1] in only]
    return jobs


def cost_key(j):
    if j[0] == 'I':
        c = WK.CELLS[j[1]]
        return -(c['N'] * c['I'] * (c['N'] / 100.0) ** 0.5)
    import pangaea as PG
    c = PG.PG[j[1]]
    return -(c['T'] * (c['r'] / 100.0))


def cmd_cells(a):
    jobs = jobs_for(a.part, a.reps, a.rep0, a.cells)
    jobs.sort(key=lambda j: (cost_key(j), j[2], j[3]))
    run_pool(jobs, os.path.join(OUT, 'cells_%s%s.json.gz' % (a.part, a.tag)), a.workers)


def cmd_probe(a):
    out = {}
    for spec in a.jobs:
        kind, cell, w, gens = spec.split(':')
        t0 = time.time()
        if kind == 'I':
            r = WK.island_job((cell, 990, w, int(gens), True))
        else:
            r = WK.pg_job((cell, 990, w, int(gens), EXT_NONE))
        out[spec] = dict(time_s=time.time() - t0, last_gen=r['last_gen'])
        log(spec, '%.1fs' % (time.time() - t0))
    p = os.path.join(OUT, 'probe.json')
    old = json.load(open(p)) if os.path.exists(p) else {}
    old.update(out)
    json.dump(old, open(p, 'w'), indent=1)


# ------------------------------------------------------------------------------------------------ validation
def _val_job(job):
    """Reproduction checks (notes §2): returns compared points and differences."""
    kind, rep = job
    t0 = time.time()
    bad = []; n = 0
    if kind in ('scalL', 'propL'):
        cell = 'wk_Snon_200_64' if kind == 'scalL' else 'wk_prop_200_64'
        sc = 'rs_Snon_200_64_cal' if kind == 'scalL' else 'rs_prop_200_64_cal'
        r = WK.island_job((cell, rep, 'L', 2000, True))
        st = [x for x in json.load(gzip.open(os.path.join(WK.ROOT, 'runs/realizable_scaling/lottery_main.json.gz')))
              if x['cell'] == sc and x['rep'] == rep][0]
        ref = {t[0]: t for t in st['trace']}
        for t in r['trace']:
            if t[0] in ref:
                n += 1
                s = ref[t[0]]
                # stored trace: (g, pcc, islands90, held, identity, open, spo, n_types, uo, isl95)
                if abs(s[1] - t[1]) > 1e-4 or s[7] != t[7] or s[3] != t[2] or s[4] != t[3] or s[8] != t[4]:
                    bad.append((t[0], s[:9], t))
        s2 = st['snaps'].get('2000'); m2 = r['snaps'].get('2000')
        if s2 and m2 and (s2['universal_open'] != m2['universal_open'] or s2['identity_islands'] != m2['identity_islands']):
            bad.append(('snap2000', s2['universal_open'], m2['universal_open']))
    elif kind == 'scalK':
        r = WK.island_job(('wk_Snon_200_64', rep, 'K', 10000, True))
        d = [x for x in json.load(gzip.open(os.path.join(WK.ROOT, 'runs/detectors/cells_C_slim.json.gz')))
             if x['cell'] == 'Cis_K0_e0' and x['rep'] == rep][0]
        ser = {int(x[0]): x[3] for x in d['series']}
        for t in r['trace']:
            if t[0] in ser:
                n += 1
                if abs(ser[t[0]] - t[1]) > 1e-4: bad.append((t[0], ser[t[0]], t[1]))
        fc = [round(x[0], 4) for x in d['final']]
        mc = r['final']['isl']['cc']
        n += 1
        if any(abs(a_ - b_) > 1e-3 for a_, b_ in zip(fc, mc)): bad.append(('final_cc',))
        if bool(d['uo']) != bool(r['final']['universal_open']): bad.append(('uo', d['uo'], r['final']['universal_open']))
    elif kind == 'track':
        ra = WK.island_job(('wk_Snon_100_64', rep, 'K', 500, True))
        rb = WK.island_job(('wk_Snon_100_64', rep, 'K', 500, False))
        for ta, tb in zip(ra['trace'], rb['trace']):
            n += 1
            if ta != tb: bad.append((ta, tb))
    elif kind in ('pgL', 'ffL'):
        import pangaea_run as PGR
        cell = 'pg_L_200_64_r100' if kind == 'pgL' else 'pg_L_100_128_r100_ff200'
        fn = 'lottery_A.json.gz' if kind == 'pgL' else 'lottery_F.json.gz'
        r = WK.pg_job((cell, rep, 'L', 2000, EXT_NONE))
        st = [x for x in json.load(gzip.open(os.path.join(WK.ROOT, 'runs/pangaea', fn)))
              if x['cell'] == cell and x['rep'] == rep][0]
        ref = {t['g']: t for t in st['trace']}
        for t in r['trace']:
            if t['g'] in ref:
                n += 1
                s = ref[t['g']]
                if abs(s['pcc'] - t['pcc']) > 1e-4 or s['nt'] != t['nt'] or s['uo'] != t['uo']:
                    bad.append((t['g'], s['pcc'], t['pcc'], s['nt'], t['nt']))
    return dict(kind=kind, rep=rep, compared=n, n_bad=len(bad), bad=bad[:5], time_s=time.time() - t0)


def cmd_validate(a):
    jobs = [('scalK', 0), ('scalK', 1), ('scalK', 2), ('scalL', 0), ('scalL', 1), ('scalL', 2), ('propL', 0),
            ('propL', 1), ('pgL', 0), ('ffL', 0), ('track', 0), ('track', 1)]
    out = []
    with Pool(min(3, a.workers), maxtasksperchild=2) as pool:
        for r in pool.imap_unordered(_val_job, jobs):
            log('validate %s rep %d: %d compared, %d differ (%.0fs) %s' % (r['kind'], r['rep'], r['compared'], r['n_bad'],
                                                                          r['time_s'], r['bad'][:2]))
            out.append(r)
    out.append(tables_check())
    log(json.dumps(out[-1]))
    json.dump(js(out), open(os.path.join(WK.ROOT, 'runs', 'world-k-validate.json'), 'w'), indent=1)


def tables_check():
    """K tables are the detectors run's: unit counts and the tracked sets summary; the detectors run's statics."""
    import detectors as DT
    LSK = WK.world_ls('K')
    sets = json.load(open(os.path.join(DT.KDIR, 'sets.json')))
    out = dict(units=len(LSK['meta']['units']), sets_units=sets['n_units'], ident_universe=int(np.asarray(LSK['ident']).sum()),
               sets_ident=sets['n_ident_universe'], Q_K=int(len(LSK['Q_K'])), sets_Q=sets['Q_spellings'],
               open_units=int(np.asarray(LSK['openu']).sum()), sets_open=sets['open_units'])
    Wd = DT.world('K')
    out.update(DET_n=int(Wd['DET'].sum()), DET_mass=float(Wd['mu'][Wd['DET']].sum()), PBN_n=int(Wd['PBN'].sum()),
               PBN_mass=float(Wd['mu'][Wd['PBN']].sum()), T_units=int(Wd['T'].sum()))
    st = json.load(open(os.path.join(WK.ROOT, 'runs', 'detectors-static.json')))['K']
    out.update(stored_DET_n=st['DET']['n'], stored_DET_mass=st['DET']['mass'], stored_PBN_n=st['PBN']['n'],
               stored_T_units=st['T_units'])
    out['agree'] = bool(out['units'] == out['sets_units'] and out['ident_universe'] == out['sets_ident'] and
                        out['Q_K'] == out['sets_Q'] == 0 and out['open_units'] == out['sets_open'] and
                        out['DET_n'] == out['stored_DET_n'] and out['PBN_n'] == out['stored_PBN_n'] and
                        out['T_units'] == out['stored_T_units'])
    out['kind'] = 'tables'
    return out


# ------------------------------------------------------------------------------------------------ statics (§2)
def cmd_statics(a):
    import pangaea as PG
    out = {}
    for w in ('L', 'K'):
        LS = WK.use_world(w)
        d = PG.determ(LS, 'L', gens=2000)
        tr = d['traj']
        pick = [t for t in tr if t['g'] in (0, 20, 50, 100, 150, 200, 300, 500, 1000, 2000)]
        out[w] = dict(determ=[dict(g=t['g'], pcc=round(t['pcc'], 4), target=round(t['target'], 4),
                                   open=round(t['open'], 4), APnet=round(t['APnet'], 4), ident=round(t['ident'], 5),
                                   cls={PG.CLASSES[j]: round(x, 4) for j, x in enumerate(t['cls'])}) for t in pick],
                      final_top=d['final_top'], APmax=max(t['APnet'] for t in tr))
        log(w, json.dumps(out[w])[:1500])
    ST = WK.static_sets()
    out['sets'] = dict(effsp_n=int(ST['effsp'].sum()), Q_n=int(ST['Q'].sum()), mint_n=int(ST['mint'].sum()),
                       mint_trees=len(ST['mint_trees']))
    json.dump(js(out), open(os.path.join(WK.ROOT, 'runs', 'world-k-static.json'), 'w'), indent=1)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('validate'); s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('statics')
    s = sub.add_parser('probe'); s.add_argument('--jobs', nargs='+')
    s = sub.add_parser('cells'); s.add_argument('--part', required=True); s.add_argument('--workers', type=int, default=3)
    s.add_argument('--reps', type=int, default=20); s.add_argument('--rep0', type=int, default=0)
    s.add_argument('--cells', nargs='*'); s.add_argument('--tag', default='')
    a = ap.parse_args()
    {'validate': cmd_validate, 'statics': cmd_statics, 'probe': cmd_probe, 'cells': cmd_cells}[a.cmd](a)


if __name__ == '__main__':
    main()
