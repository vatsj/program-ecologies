"""Cells of the pair-worth easy case along N (spec specs/2026-11-03-pair-worth-n.md; notes/pair-worth-n.md).

    python3 src/pair_worth_n_run.py one JOBLINE
    python3 src/pair_worth_n_run.py worker JOBFILE        # claim and run jobs in file order (lock file per job)

A job line:  arm|N|run|delta|lams|mNs|chase     e.g.  CF|400|20|0.05|10|1|20
Rows (one JSON per job: a list of (Lambda, mN) records) go to $PWN_ROWS (default runs/pair_worth_n/rows).  Importable without
side effects.
"""
import argparse, json, os, sys, time, resource
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pair_worth as PW
import pair_worth_run as PR
import pair_worth_n as PN

ROWS = os.environ.get('PWN_ROWS', os.path.join(PW.ROOT, 'runs', 'pair_worth_n', 'rows'))
GNAME = 'pw13'
ANC_WINDOW = 200


def prepare_n(arm, N, r, delta, lams, I=64, chase=20):
    menu = PN.arm_menu_n(arm, delta)
    founders = PN.founders_bk(menu, N, r, I, int(arm[3:])) if arm.startswith('CBk') else None
    prep = PR.prepare(GNAME, arm, r, N, delta, lams, I, menu=menu, founders=founders)
    geo = dict(prep['geo']); geo['H'] = geo['gend'] + int(chase) * N
    prep['geo'] = geo
    return prep


def first_run(b, L=PR.DEBOUNCE):
    """first index g (per island column) at which the boolean series b (H+1, I) is True for L consecutive generations; -1 if never."""
    H1, I = b.shape
    cs = np.vstack([np.zeros((1, I), np.int64), np.cumsum(b.astype(np.int64), axis=0)])
    win = cs[L:] - cs[:-L]                     # window sums starting at g = 0..H1-L
    ok = win == L
    out = np.full(I, -1, np.int64)
    anyok = ok.any(0)
    out[anyok] = ok.argmax(0)[anyok]
    return out


def extra_stats(prep, o, lam, mN):
    G = prep['G']; J = prep['J']; loc = prep['loc']; menu = prep['menu']; table = prep['table']
    N = prep['N']; I = prep['I']; geo = prep['geo']; H = geo['H']; g0 = geo['g0']; gend = geo['gend']
    U = prep['U']; CLA = prep['CLA']; CLB = prep['CLB']; FAM = table.FAM
    TOT = G.VEC.sum(1); KIND = G.KIND
    ex = {}
    # ---- universe annotations: named split type id, program class (0 other constant, 1 grand constant, 2 bid, 3 F)
    typ = []; kc = []
    for s in range(3):
        t = np.full(table.Kmax, -1, np.int64); c = np.zeros(table.Kmax, np.int64)
        for k, u in enumerate(U[s]):
            fi, si, cc = menu.decode(int(u))
            if fi >= 0:
                t[k] = fi * 1000 + si
            fam = int(FAM[s, k])
            if fam == 1:
                c[k] = 2
            elif fam == 3:
                c[k] = 3
            else:
                lines, df = menu.prog(s, int(u))
                c[k] = 1 if (not lines and G.PARTNER[s, df] == PW.ALL) else 0
        typ.append(t); kc.append(c)
    # ---- supply at founding
    sup_any = np.zeros(I, np.int8); sup_eff = np.zeros(I, np.int8)
    minab_eff = np.zeros(I, np.int64); minab_any = np.zeros(I, np.int64)
    nind_eff = np.zeros(I); nind_named_eff = np.zeros(I); nind_named_any = np.zeros(I)
    sup_named_eff = np.zeros(I, np.int8); minab_named_eff = np.zeros(I, np.int64)
    ntypes = np.zeros((I, 3), np.int64)
    for i in range(I):
        pa = np.nonzero(loc[i, 0])[0]; pb = np.nonzero(loc[i, 1])[0]; pc = np.nonzero(loc[i, 2])[0]
        ca = loc[i, 0, pa]; cb = loc[i, 1, pb]; cc = loc[i, 2, pc]
        sub = J[np.ix_(pa, pb, pc)]
        kd = KIND[sub] == 1
        ef = kd & (TOT[sub] == G.Gd)
        w = ca[:, None, None] * cb[None, :, None] * cc[None, None, :]
        mm = np.minimum(np.minimum(ca[:, None, None], cb[None, :, None]), cc[None, None, :])
        named = (FAM[0, pa] > 0)[:, None, None] & (FAM[1, pb] > 0)[None, :, None] & (FAM[2, pc] > 0)[None, None, :]
        sup_any[i] = kd.any(); sup_eff[i] = ef.any()
        minab_any[i] = int((mm * kd).max()); minab_eff[i] = int((mm * ef).max())
        nind_eff[i] = float((w * ef).sum()); nind_named_eff[i] = float((w * (ef & named)).sum())
        nind_named_any[i] = float((w * (kd & named)).sum())
        sup_named_eff[i] = (ef & named).any(); minab_named_eff[i] = int((mm * (ef & named)).max())
        for s, pp in enumerate((pa, pb, pc)):
            tt = typ[s][pp]
            ntypes[i, s] = len(set(tt[tt >= 0].tolist()))
    cd0 = o['cd'][0]
    ex['supply'] = dict(any=sup_any.tolist(), eff=sup_eff.tolist(), minab_any=minab_any.tolist(), minab_eff=minab_eff.tolist(),
                        nind_eff=[round(x, 1) for x in nind_eff], nind_named_eff=nind_named_eff.tolist(),
                        nind_named_any=nind_named_any.tolist(), ntypes=ntypes.tolist(),
                        named_eff=sup_named_eff.tolist(), minab_named_eff=minab_named_eff.tolist(),
                        p0_grand=[round(float(cd0[i, 6 + 1] + cd0[i, 6 + 2]), 6) for i in range(I)],
                        p0_core=[round(float(cd0[i, 1]), 6) for i in range(I)])
    # ---- establishment
    modal = o['modal'].astype(np.int64)
    A_ser = CLA[modal]; B_ser = CLB[modal]
    ex['est_grand'] = first_run((B_ser == 1) | (B_ser == 2)).tolist()
    ex['est_core'] = first_run(A_ser == 1).tolist()
    # ---- transitions of the core class, by phase, with exposure and ancestry
    core = (A_ser == 1).astype(np.int64)
    fl = PR.flips(core)
    xl = o['xlog']
    xi = xl[:, 1] if len(xl) else np.zeros(0, np.int64)
    byi = []
    for i in range(I):
        m = xi == i
        byi.append(xl[m] if len(xl) else np.zeros((0, 6), np.int64))
    famr = o['famr']
    phases = ('pre', 'tail', 'chase')
    ev = {ph: {'entry': [0, 0, 0], 'exit': [0, 0, 0]} for ph in phases}       # by ancestry: resident, migrant, arrival
    readers_hist = {'entry': [0, 0, 0, 0], 'exit': [0, 0, 0, 0]}
    events = []
    for i, ch in enumerate(fl):
        rows = byi[i]
        for (g, a, b) in ch:
            ph = 'pre' if g < g0 else ('tail' if g < gend else 'chase')
            kind = 'entry' if b == 1 else 'exit'
            anc = 0
            if len(rows):
                sel = rows[(rows[:, 0] <= g) & (rows[:, 0] > g - ANC_WINDOW)]
                if len(sel):
                    anc = 2 if (sel[:, 4] == 1).any() else (1 if (sel[:, 5] >= 0).any() else 0)
            ev[ph][kind][anc] += 1
            bits = int(famr[max(g - 1, 0), i])
            nread = 0
            for s in range(3):
                if ((bits >> (s * 8 + 0 * 2)) & 1) or ((bits >> (s * 8 + 2 * 2)) & 1):      # family 1 (bid) or 3 (F), >= 1 individual
                    nread += 1
            readers_hist[kind][nread] += 1
            if len(events) < 300:
                events.append([int(g), i, kind, anc, nread])
    expo = {ph: dict(in_core=0, out_core=0) for ph in phases}
    for ph, (a, b) in (('pre', (0, g0)), ('tail', (g0, gend)), ('chase', (gend, H + 1))):
        c = int(core[a:b].sum()); expo[ph]['in_core'] = c; expo[ph]['out_core'] = int((b - a) * I - c)
    ex['core_transitions'] = dict(events=ev, exposure=expo, readers_before=readers_hist, first_events=events,
                                  anc_labels=['resident', 'migrant', 'arrival'], window=ANC_WINDOW)
    # ---- who holds the core at the end
    counts = o['counts']
    core_end = np.nonzero(A_ser[H] == 1)[0]
    maj = np.zeros(4, np.int64); share = np.zeros(4); all3gc = 0; anyreader = 0; allreader = 0
    for i in core_end:
        mj = []
        for s in range(3):
            k = int(counts[i, s].argmax()); mj.append(int(kc[s][k]))
            maj[mj[-1]] += 1
            for kk in range(counts.shape[2]):
                if counts[i, s, kk] > 0:
                    share[kc[s][kk]] += counts[i, s, kk] / N
        all3gc += all(m == 1 for m in mj); anyreader += any(m >= 2 for m in mj); allreader += all(m >= 2 for m in mj)
    nci = len(core_end)
    ex['holders'] = dict(n_core_islands=int(nci), majority_program_class=maj.tolist(),
                         pop_share_sum=share.tolist(), all3_grand_constants=int(all3gc), any_reader_majority=int(anyreader),
                         all3_reader_majority=int(allreader), classes=['other-constant', 'grand-constant', 'bid', 'F'])
    return ex


def run_job(job):
    arm, N, r, delta, lams, mNs, chase = job
    t0 = time.time()
    prep = prepare_n(arm, N, r, delta, lams, chase=chase)
    tp = time.time() - t0
    recs = []
    for lam in lams:
        for mN in mNs:
            t1 = time.time()
            o = PR.run_kernel(prep, lam, mN)
            tk = time.time() - t1
            rec = PR.summarize(prep, o, GNAME, lam, mN)
            t2 = time.time()
            rec.update(extra_stats(prep, o, lam, mN))
            rec.update(arm=arm, run=r, N=N, delta=delta, chase=chase, kern_wall=round(tk, 1), prep_wall=round(tp, 1),
                       extra_wall=round(time.time() - t2, 1), rss_gb=round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 2))
            recs.append(rec)
    return recs


def parse_job(line):
    arm, N, r, delta, lams, mNs, chase = line.strip().split('|')
    return (arm, int(N), int(r), float(delta), [float(x) for x in lams.split(',')], [float(x) for x in mNs.split(',')], int(chase))


def job_name(line):
    return line.strip().replace('|', '_').replace(',', '-')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('a', nargs='?')
    args = ap.parse_args()
    os.makedirs(ROWS, exist_ok=True)
    if args.cmd == 'one':
        line = args.a
        recs = run_job(parse_job(line))
        for r in recs:
            print({k: r[k] for k in ('arm', 'N', 'run', 'lam', 'mN', 'endA', 'endB', 'stop', 'kern_wall', 'prep_wall', 'extra_wall', 'rss_gb')}, flush=True)
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
