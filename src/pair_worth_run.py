"""Cells of the pair-worth experiment (spec design 3-5; notes/pair-worth.md).

    python3 src/pair_worth_run.py one GAME ARM RUN [--N 100] [--lams 0,10] [--mNs 1,0] [--delta 0.05]
    python3 src/pair_worth_run.py worker JOBFILE            # claim and run jobs one at a time (a job = one line)
    python3 src/pair_worth_run.py batch JOBFILE --workers 3

A job line:  game|arm|run|N|delta|lams|mNs   e.g.  pw13|CBs|0|100|0.05|0,10|1,0
Rows (one JSON per job) go to $PW_ROWS (default runs/pair_worth/rows).  Importable without side effects.
"""
import argparse, json, os, sys, time, resource, zlib
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pair_worth as PW
import pair_worth_kern as PK

ROWS = os.environ.get('PW_ROWS', os.path.join(PW.ROOT, 'runs', 'pair_worth', 'rows'))
W = 0.3
I_DEFAULT = 64
DEBOUNCE = 25
_TABLES = {}


def game_tables(gname):
    if gname not in _TABLES:
        G = PW.get_game(gname)
        CLA, CLB = G.class_tables()
        _TABLES[gname] = (G, CLA.astype(np.int64), CLB.astype(np.int64))
    return _TABLES[gname]


def geometry(N):
    """tail start, t0, tail end, horizon, chase, last window (scaled with N)."""
    g0 = 2 * N; t0 = N / 2.0; gend = 100 * N; chase = 20 * N
    return dict(g0=g0, t0=t0, gend=gend, H=gend + chase, win=20 * N)


def prepare(gname, arm, r, N, delta, lams, I=I_DEFAULT, menu=None):
    G, CLA, CLB = game_tables(gname)
    menu = menu or PW.arm_menu(gname, arm, delta)
    geo = geometry(N)
    base = '%s|N%d|I%d' % (gname, N, I)
    founders = PW.draw_founders(menu, base, r, I, N)
    sched = PW.tail_schedule(menu, base, r, I, N, 100.0, geo['g0'], geo['t0'], geo['gend'], sorted(set(list(lams) + [100.0])))
    lmax = max(lams) if len(lams) else 0
    sm = sched[float(lmax)] if lmax > 0 else None
    U, loc = PW.build_universe(menu, founders, sm)
    table = PW.ProgTable(menu, U)
    J = table.joint(G)
    seed = PW.seed_int('K', gname, N, r) % (2 ** 31)
    return dict(G=G, CLA=CLA, CLB=CLB, menu=menu, geo=geo, founders=founders, sched=sched, U=U, loc=loc, table=table, J=J,
                seed=seed, N=N, I=I, base=base)


def run_kernel(prep, lam, mN, N=None):
    G = prep['G']; N = prep['N']; geo = prep['geo']
    nout = G.nout
    if lam > 0:
        ag, ai, asl, au, ak = PW.local_arrivals(prep['U'], prep['sched'][float(lam)])
    else:
        ag = np.zeros(0, np.int64); ai = np.zeros(0, np.int64); asl = np.zeros(0, np.int64); au = np.zeros(0); ak = np.zeros(0, np.int64)
    out = PK.kern_pw(prep['J'], G.PAY, np.arange(nout, dtype=np.int64), np.zeros(nout, np.bool_), G.TOT, G.PAY,
                     prep['CLA'], prep['CLB'], 6, 4, prep['table'].FAM, prep['loc'], N, W, mN / N, prep['seed'], geo['H'], 10,
                     ag, ai, asl, au, ak, 2000000, 200000)
    keys = ('status', 'stop', 'counts', 'cls', 'modal', 'majo', 'ptop', 'effm', 'cd', 'payr', 'famr', 'xlog', 'nx', 'alog',
            'na', 'nmig')
    return dict(zip(keys, out))


# ====================================================================== statistics
def flips(series, L=DEBOUNCE):
    """debounced changes of each island's class series: per island a list of (g, from, to)."""
    G1, I = series.shape
    out = []
    for i in range(I):
        s = series[:, i]
        cands = np.nonzero(s[1:] != s[:-1])[0] + 1
        last = s[0]; ch = []; j = 0
        while j < len(cands):
            g = int(cands[j])
            if s[g] != last and (g + L > G1 or (s[g:g + L] == s[g]).all()):
                ch.append((g, int(last), int(s[g])))
                last = s[g]
                j = int(np.searchsorted(cands, g + L))
            else:
                j += 1
        out.append(ch)
    return out


def popcount_slots(bits, fam, thr):
    """number of slots in which family fam (1..4) is present (thr 0: >= 1 individual, 1: >= 10%)."""
    n = 0
    for s in range(3):
        if (bits >> (s * 8 + (fam - 1) * 2 + thr)) & 1:
            n += 1
    return n


def summarize(prep, o, gname, lam, mN):
    G = prep['G']; CLA = prep['CLA']; CLB = prep['CLB']; geo = prep['geo']
    H = geo['H']; win = geo['win']; g0 = geo['g0']; gend = geo['gend']; N = prep['N']; I = prep['I']
    modal = o['modal'].astype(np.int64); majo = o['majo'].astype(np.int64)
    A_ser = CLA[modal]; B_ser = CLB[modal]
    rec = dict(game=gname, lam=lam, mN=mN, status=int(o['status']), stop=int(o['stop']), nmig=int(o['nmig']),
               n_arr_sched=int(len(prep['sched'][float(lam)][0])) if lam > 0 else 0, n_arr_logged=int(o['na']),
               K=[len(u) for u in prep['U']])
    lo = H - win
    # end shares
    rec['endA'] = np.bincount(A_ser[H], minlength=6).tolist()
    rec['endB'] = np.bincount(B_ser[H], minlength=4).tolist()
    rec['endA_maj'] = np.bincount(CLA[majo[H]], minlength=6).tolist()
    rec['endB_maj'] = np.bincount(CLB[majo[H]], minlength=4).tolist()
    # occupancy over the last window: modal one-hot and encounter-weighted
    occA = np.zeros(6); occB = np.zeros(4)
    for c in range(6):
        occA[c] = (A_ser[lo:H + 1] == c).mean()
    for c in range(4):
        occB[c] = (B_ser[lo:H + 1] == c).mean()
    rec['occA'] = occA.round(5).tolist(); rec['occB'] = occB.round(5).tolist()
    cd = o['cd']
    rec['occA_enc'] = cd[lo:H + 1, :, :6].mean(axis=(0, 1)).round(5).tolist()
    rec['occB_enc'] = cd[lo:H + 1, :, 6:].mean(axis=(0, 1)).round(5).tolist()
    rec['endA_enc'] = cd[H, :, :6].mean(0).round(5).tolist()
    rec['endB_enc'] = cd[H, :, 6:].mean(0).round(5).tolist()
    # tail-phase occupancy (200 .. gend) for the grand class etc.
    rec['occA_tail'] = [round(float((A_ser[g0:gend] == c).mean()), 5) for c in range(6)]
    rec['occB_tail'] = [round(float((B_ser[g0:gend] == c).mean()), 5) for c in range(4)]
    # outcome ids at the end and over the window
    ids, cnt = np.unique(modal[H], return_counts=True)
    rec['end_ids'] = {int(a): int(b) for a, b in zip(ids, cnt)}
    ids, cnt = np.unique(modal[lo:H + 1], return_counts=True)
    rec['occ_ids'] = {int(a): int(b) for a, b in zip(ids, cnt)}
    ids, cnt = np.unique(majo[H], return_counts=True)
    rec['end_ids_maj'] = {int(a): int(b) for a, b in zip(ids, cnt)}
    rec['consensus_end'] = bool((modal[H] == modal[H, 0]).all())
    # efficiency and payoffs
    rec['eff_last'] = round(float(o['effm'][lo:H + 1].mean()), 5)
    rec['eff_end'] = round(float(o['effm'][H].mean()), 5)
    rec['pay_last'] = o['payr'][lo:H + 1].mean(axis=(0, 1)).round(5).tolist()
    rec['pay_end'] = o['payr'][H].mean(0).round(5).tolist()
    rec['mixed_time'] = round(float((o['ptop'][lo:H + 1] < 0.95).mean()), 5)
    # genuine majority share per slot at the end (from counts)
    cnts = o['counts']
    rec['maj_share_end'] = [round(float(cnts[:, s, :].max(axis=1).mean() / N), 4) for s in range(3)]
    # mean ptop
    # classes of switching: use kind classes for the hard case and vector classes elsewhere
    ser = B_ser if gname == 'pw56' else A_ser
    fl = flips(ser)
    fam = o['famr']
    sw = dict(tail=0, chase=0)
    dirs = {}
    structure = []
    for i, ch in enumerate(fl):
        for (g, a, b) in ch:
            ph = 'tail' if g0 <= g < gend else ('chase' if g >= gend else 'pre')
            if ph in sw:
                sw[ph] += 1
            key = '%d>%d' % (a, b)
            dirs.setdefault(ph, {}); dirs[ph][key] = dirs[ph].get(key, 0) + 1
            bits = int(fam[max(g - 1, 0), i])
            structure.append((g, a, b, [popcount_slots(bits, f, 0) for f in (1, 2, 3, 4)],
                              [popcount_slots(bits, f, 1) for f in (1, 2, 3, 4)]))
    rec['switch_counts'] = sw
    rec['switch_dirs'] = dirs
    # exposure: island-generations in each phase (for rates per 10^4 generations)
    rec['switch_expo'] = dict(tail=int(I * (gend - g0)), chase=int(I * (H - gend)))
    rec['structure'] = [s for s in structure][:400]
    # bids/blockers present in all three slots at some time
    def allthree(f, thr):
        m = np.ones(fam.shape, bool)
        for s in range(3):
            m &= ((fam >> (s * 8 + (f - 1) * 2 + thr)) & 1).astype(bool)
        return m
    for f, nm in ((1, 'bid'), (2, 'blk'), (3, 'acc'), (4, 'gc')):
        rec['ever3_%s' % nm] = [int(allthree(f, 0).any(0).sum()), int(allthree(f, 1).any(0).sum())]
    # families present (>= 10%) occupancy fraction in last window per slot
    # trajectory (coarse)
    step = max(1, (H + 1) // 60)
    rec['trajA'] = [np.bincount(A_ser[g], minlength=6).tolist() for g in range(0, H + 1, step)]
    rec['trajB'] = [np.bincount(B_ser[g], minlength=4).tolist() for g in range(0, H + 1, step)]
    # tail: arrivals by family; arrivals that fixed; arrivals followed by a class change within 100 gens
    FAMa = prep['table'].FAM
    alog = o['alog']
    arr_fam = {}; arr_applied = {}; arr_change = {}
    if len(alog):
        chA = np.zeros(A_ser.shape, np.int64)
        chA[1:] = (A_ser[1:] != A_ser[:-1])
        csum = np.cumsum(chA, axis=0)
        for row in alog:
            g, i, s, k, vk, ap = [int(x) for x in row[:6]]
            f = int(FAMa[s, k])
            arr_fam[f] = arr_fam.get(f, 0) + 1
            if ap:
                arr_applied[f] = arr_applied.get(f, 0) + 1
                g2 = min(g + 100, H)
                if csum[g2, i] - csum[g, i] > 0:
                    arr_change[f] = arr_change.get(f, 0) + 1
        # baseline: any class change within the next 100 gens, over tail island-generations
        gs = np.arange(g0, gend)
        base_rate = float(((csum[np.minimum(gs + 100, H)] - csum[gs]) > 0).mean())
        rec['arr_change_baseline'] = round(base_rate, 5)
    rec['arr_by_family'] = arr_fam; rec['arr_applied_by_family'] = arr_applied; rec['arr_then_change_100'] = arr_change
    fixed = {}
    for row in o['xlog']:
        g, i, s, k, arrf, introg = [int(x) for x in row]
        if arrf:
            f = int(FAMa[s, k]); fixed[f] = fixed.get(f, 0) + 1
    rec['arr_fixed_by_family'] = fixed
    rec['nx_cross'] = int(o['nx'])
    return rec


def run_job(job):
    gname, arm, r, N, delta, lams, mNs = job
    t0 = time.time()
    prep = prepare(gname, arm, r, N, delta, lams)
    tp = time.time() - t0
    recs = []
    for lam in lams:
        for mN in mNs:
            t1 = time.time()
            o = run_kernel(prep, lam, mN)
            tk = time.time() - t1
            rec = summarize(prep, o, gname, lam, mN)
            rec.update(arm=arm, run=r, N=N, delta=delta, kern_wall=round(tk, 1), prep_wall=round(tp, 1),
                       rss_gb=round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 2))
            recs.append(rec)
    return recs


def parse_job(line):
    g, arm, r, N, delta, lams, mNs = line.strip().split('|')
    return (g, arm, int(r), int(N), float(delta), [float(x) for x in lams.split(',')], [float(x) for x in mNs.split(',')])


def job_name(line):
    return line.strip().replace('|', '_').replace(',', '-')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('a', nargs='?')
    ap.add_argument('--workers', type=int, default=3)
    args, rest = ap.parse_known_args()
    os.makedirs(ROWS, exist_ok=True)
    if args.cmd == 'one':
        line = args.a
        recs = run_job(parse_job(line))
        for r in recs:
            print({k: r[k] for k in ('game', 'arm', 'run', 'lam', 'mN', 'endA', 'endB', 'stop', 'kern_wall', 'prep_wall', 'rss_gb')})
        with open(os.path.join(ROWS, job_name(line) + '.json'), 'w') as f:
            json.dump(recs, f)
    elif args.cmd == 'worker':
        jobs = [l.strip() for l in open(args.a) if l.strip() and not l.startswith('#')]
        for line in jobs:
            path = os.path.join(ROWS, job_name(line) + '.json')
            lock = path + '.lock'
            if os.path.exists(path) or os.path.exists(lock):
                continue
            try:
                fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
            except FileExistsError:
                continue
            try:
                t0 = time.time()
                recs = run_job(parse_job(line))
                with open(path + '.tmp', 'w') as f:
                    json.dump(recs, f)
                os.replace(path + '.tmp', path)
                print('done', line, '%.0fs' % (time.time() - t0), flush=True)
            except Exception as e:
                import traceback
                traceback.print_exc()
                print('FAILED', line, repr(e), flush=True)
            finally:
                try:
                    os.remove(lock)
                except OSError:
                    pass
    else:
        raise SystemExit('unknown command')


if __name__ == '__main__':
    main()
