"""lim_N of the attractor chain in the modal arm (PD).

    python3 src/modal_limN.py
Writes runs/modal_limN.md/json.
"""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import modal as M
from chain import Chain

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def cell(n, N, w, built, **chain_kw):
    L, val, worlds, prov = built
    lang = M.ClassLang(prov)
    t = time.time()
    ch = Chain(prov, N=N, w=w, verbose=False, **chain_kw).explore()
    U, P = prov.Ufull, prov.PCC
    def cls(src):
        c = L.rep.index(src)
        for i, m in enumerate(prov.members):
            if c in m: return i
    iD, iFB = cls('D'), cls('BOX(THEM(ME))')
    iPB = cls('and(BOX(THEM(ME)),BOXD1(THEM(^D)))') if n >= 8 else None
    pcc = 0.0; poly = 0.0; key_of = {}; coop_mono = 0.0
    for key, wgt in zip(ch.keys_list, ch.pi):
        ids, x, kind = ch.states[key]; ids = list(ids); x = np.asarray(x)
        pcc += wgt * float(x @ P[np.ix_(ids, ids)] @ x)
        if len(ids) > 1: poly += wgt
        else: key_of[ids[0]] = key
    pi = lambda c: float(ch.pi[ch.keys_list.index(key_of[c])]) if c in key_of and key_of[c] in ch.keys_list else 0.0
    out = dict(n=n, N=N, w=w, chain_kw={k: v for k, v in chain_kw.items()}, pcc=pcc, poly=poly, pi_D=pi(iD), pi_FB=pi(iFB), pi_PB=pi(iPB) if iPB is not None else None,
               indeterminate=len(ch.indeterminate), cut_flow=ch.cut_flow)
    # entry D -> FB, exits from FB by type
    kD, kFB = key_of.get(iD), key_of.get(iFB)
    rho = [v[0] for (a, b, q), v in ch.edge_rho.items() if a == kD and b == kFB]
    out['rho_FB_D'] = float(max(rho)) if rho else 0.0
    ex = dict(neutral=0.0, strict=0.0, other=0.0); dest = {}
    if kFB is not None:
        uaa = U[iFB, iFB]
        for b, wgt in ch.trans.get(kFB, {}).items():
            if b == kFB: continue
            for q, mw in ch.trans_mut[(kFB, b)].items():
                if U[q, iFB] > uaa + 1e-9: t2 = 'strict'
                elif abs(U[q, iFB] - uaa) < 1e-9 and abs(U[iFB, q] - uaa) < 1e-9 and abs(U[q, q] - uaa) < 1e-9: t2 = 'neutral'
                else: t2 = 'other'
                ex[t2] += mw; dest[prov.names[q]] = dest.get(prov.names[q], 0.0) + mw
    tot = sum(ex.values())
    out.update(exit_total=tot, **{'exit_' + k: v for k, v in ex.items()},
               allc_share=dest.get('C', 0.0) / tot if tot else float('nan'),
               top_exits=sorted(dest.items(), key=lambda kv: -kv[1])[:4],
               support=[(ch.describe_state(k, lang), float(p)) for k, p in ch.support(1e-3)][:6],
               time_s=time.time() - t)
    return out


def _job(job):
    n, N, w = job
    return cell(n, N, w, M.build(n))


def main(a):
    from multiprocessing import Pool
    cells = [(9, w) for w in a.w] + [(n, 0.3) for n in a.ns if n != 9]
    jobs = sorted([(n, N, w) for n, w in cells for N in a.N], key=lambda j: -j[1])
    rows = []
    with Pool(a.procs) as pool:
        for r in pool.imap_unordered(_job, jobs):
            rows.append(r)
            print('n=%d w=%g N=%d: P(C,C) %.4f pi(D) %.4f pi(FB) %.4f pi(PB) %s rho(FB|D) %.4f exit %.2e (neutral %.2e strict %.2e other %.2e) ALLC share %.2f poly %.1e (%.0fs)' % (
                r['n'], r['w'], r['N'], r['pcc'], r['pi_D'], r['pi_FB'], 'n/a' if r['pi_PB'] is None else '%.2e' % r['pi_PB'], r['rho_FB_D'], r['exit_total'],
                r['exit_neutral'], r['exit_strict'], r['exit_other'], r['allc_share'], r['poly'], r['time_s']), flush=True)
            json.dump(rows, open(os.path.join(ROOT, 'runs', 'modal_limN.json'), 'w'), indent=1, default=str)
    rows.sort(key=lambda r: (r['n'] != 9, r['n'], r['w'], r['N']))
    L = ['# Modal arm: lim_N of the attractor chain (PD, f = exp(w·payoff))', '',
         '| n | w | N | P(C,C) | π(all-D) | π(all-FairBot) | π(all-PrudentBot) | ρ(FairBot \\| all-D) | exit rate from all-FairBot | of which strict | ALLC share of exits | support (π ≥ 1e-3, top 4) |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        L.append('| %d | %g | %d | %.4f | %.4f | %.4f | %s | %.4f | %.2e | %.2e | %.2f | %s |' % (
            r['n'], r['w'], r['N'], r['pcc'], r['pi_D'], r['pi_FB'], '—' if r['pi_PB'] is None else '%.1e' % r['pi_PB'], r['rho_FB_D'], r['exit_total'], r['exit_strict'],
            r['allc_share'], '; '.join('%s %.3f' % sp for sp in r['support'][:4])))
    open(os.path.join(ROOT, 'runs', 'modal_limN.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--w', type=float, nargs='+', default=[0.1, 0.3, 1.0])
    ap.add_argument('--ns', type=int, nargs='+', default=[6, 8, 9])
    ap.add_argument('--procs', type=int, default=9)
    ap.add_argument('--N', type=int, nargs='+', default=[100, 300, 1000, 3000, 10000, 30000])
    main(ap.parse_args())
