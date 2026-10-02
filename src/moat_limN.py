"""eps->0 chain for predictions/2026-10-02-drift-closure.md: the free modal arm, a prior boost (PrudentBot at
FairBot's prior mass) and three background fringes (D, CD, mu), PD, w = 0.3, eager_poly=False.

    python3 src/moat_limN.py [--workers 3] [--smoke]
Writes runs/drift_closure.json and runs/drift_closure.md.
"""
import json, os, sys, time, argparse
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import modal as M
import fringe as F
from chain import Chain
from cert_limN import networks, top_exits
from moat_estimates import family

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = (100, 1000, 10000, 30000, 100000)
WORLDS = [('FB', F.FB), ('FB1', F.FB1), ('PB', F.PB), ('Pstar', F.PSTAR), ('BTT', F.BTT), ('P12b', F.P12B)]


def jobs():
    J = []
    for n in (6, 8):
        for N in NS:
            J.append(('free', n, 0.0, 'D', N))
            for kind in ('D', 'CD'):
                for d in (1e-3, 1e-2):
                    J.append((kind, n, d, kind, N))
            J.append(('mu', n, 1e-2, 'mu', N))
            if n == 8:
                J.append(('boostPB', n, 0.0, 'D', N))
                J.append(('addP12b', n, 0.0, 'D', N))
                J.append(('addP12bsib', n, 0.0, 'D', N))
            if n == 6:
                J.append(('Dpath', n, 10.0 / N, 'D', N))
    # [after review] crossover controls and one larger N (fable 3.1, 3.2; astra)
    for n in (6, 8):
        for N in NS:
            J.append(('mu', n, 1e-3, 'mu', N))
    J.append(('mu', 6, 1e-2, 'mu', 300000)); J.append(('mu', 6, 1e-2, 'mu', 1000000))
    for kind in ('D', 'CD', 'mu'):
        J.append((kind, 8, 1e-2, kind, 300000))
    # [after review] theta sensitivity (astra 3; fable 1.2)
    J.append(('D', 8, 1e-2, 'D', 100000, 1e-8)); J.append(('mu', 8, 1e-2, 'mu', 100000, 1e-8))
    J.append(('free', 9, 0.0, 'D', 100000))       # n-robustness
    for N in (10000, 100000):
        J.append(('D', 9, 1e-2, 'D', N))
        J.append(('mu', 9, 1e-2, 'mu', N))
    return J


def cell(job):
    arm, n, delta, kind, N = job[:5]
    theta = job[5] if len(job) > 5 else 1e-6
    t = time.time()
    boost = (F.PB, F.FB) if arm == 'boostPB' else None
    extra = (F.P12B,) if arm == 'addP12b' else ((F.P12B,) + tuple(F.P12B_SIBS) if arm == 'addP12bsib' else ())
    L, prov = F.build_variant(n, delta, kind, boost, extra)
    names = prov.names; P = prov.PCC
    lang = M.ClassLang(prov)
    ch = Chain(prov, N=N, w=0.3, verbose=False, eager_poly=False, theta=theta).explore()
    pcc = 0.0; pis = {}; key_of = {}
    fam = dict(FBfam=0.0, prudent=0.0, rival=0.0, ALLC=0.0)
    for key, wgt in zip(ch.keys_list, ch.pi):
        ids, x, k = ch.states[key]; ids = list(ids); x = np.asarray(x)
        pcc += wgt * float(x @ P[np.ix_(ids, ids)] @ x)
        if k == 'mono':
            q = ids[0]; pis[q] = pis.get(q, 0.0) + wgt; key_of[q] = key
            f = family(P, names, q)
            if f: fam[f] += wgt
    # network exit: stationary flux from cooperative states (self-play P(C,C) > 1/2) to the rest, per unit of
    # cooperative mass and per mutation event; network entry: the reverse flux per unit of non-cooperative mass
    idx = {k: i for i, k in enumerate(ch.keys_list)}
    sp = {}
    for key in ch.keys_list:
        ids, x, k = ch.states[key]; ids = list(ids); x = np.asarray(x)
        sp[key] = float(x @ P[np.ix_(ids, ids)] @ x) > 0.5
    cmass = sum(p for key, p in zip(ch.keys_list, ch.pi) if sp[key])
    fo = sum(p * v for key, p in zip(ch.keys_list, ch.pi) if sp[key] for b, v in ch.trans[key].items() if b in idx and not sp[b])
    fi = sum(p * v for key, p in zip(ch.keys_list, ch.pi) if not sp[key] for b, v in ch.trans[key].items() if b in idx and sp[b])
    net_exit = fo / cmass if cmass > 0 else float('nan')
    net_entry = fi / (1 - cmass) if cmass < 1 else float('nan')
    iD = names.index('D')
    coop_states = [(v, q) for q, v in pis.items() if P[q, q] == 1 and names[q] != 'C']
    v, qtop = max(coop_states)
    # [after review, fable 1.2] kept exit share: for states with pi > 1e-3, the share of their exit flow whose
    # targets were expanded (edges to unexpanded targets are dropped by the reflecting boundary)
    kept = []
    for key, p in zip(ch.keys_list, ch.pi):
        if p > 1e-3:
            ids0 = ch.states[key][0]
            tot = 0.0; kp = 0.0
            # raw transition weights incl. unexpanded targets are not stored after renormalization; use trans (kept)
            # plus the flow recorded into unexpanded targets during exploration
            for b, v in ch.trans[key].items():
                if b == key: continue
                tot += v; kp += v if b in idx else 0.0
            kept.append(kp / tot if tot > 0 else 1.0)
    out = dict(arm=arm, n=n, delta=delta, kind=kind, N=N, theta=theta, kept_exit_share=min(kept) if kept else 1.0,
               n_classes=len(names), pcc=pcc, pi_D=pis.get(iD, 0.0), **fam,
               top_coop=names[qtop], pi_top=v, net_exit=net_exit, net_entry=net_entry, coop_mass_net=cmass,
               cut_flow=ch.cut_flow, indeterminate=len(ch.indeterminate), n_terminal=len(ch.terminal),
               near_closed=int(getattr(ch, 'near_closed', 0)), absorb_error=float(getattr(ch, 'absorb_error', 0.0)),
               n_states=len(ch.trans), poly_flow=ch.poly_flow,
               support=[(ch.describe_state(k, lang), float(p)) for k, p in ch.support(1e-3)][:8])
    out.update(networks(ch, prov))
    out.update(top_exits(ch, prov, key_of[qtop]))
    for lab, s in WORLDS:
        if s in names:
            k = ch.mono(names.index(s)); ch.expand(k)
            e = top_exits(ch, prov, k)
            out.update({'pi_' + lab: pis.get(names.index(s), 0.0), lab + '_exit': e['top_exit'], lab + '_strict': e['top_exit_strict'],
                        lab + '_neutral': e['top_exit_neutral'], lab + '_other': e['top_exit_other'], lab + '_allc': e['allc_share'],
                        lab + '_dest': e['top_dest']})
    out['time_s'] = time.time() - t
    return out


def tag(r):
    return '%s n=%d δ=%.3g N=%d%s' % (r['arm'], r['n'], r['delta'], r['N'], '' if r.get('theta', 1e-6) == 1e-6 else ' θ=%g' % r['theta'])


def slopes(rows):
    """Local log-slopes of the cooperative-to-D odds between consecutive N, per (arm, n, delta-or-path)."""
    from collections import defaultdict
    g = defaultdict(list)
    for r in rows:
        if r.get('theta', 1e-6) != 1e-6: continue
        g[(r['arm'], r['n'], 0.0 if r['arm'] == 'Dpath' else r['delta'])].append(r)
    out = {}
    for key, rs in g.items():
        rs = sorted(rs, key=lambda r: r['N'])
        s = []
        for a, b in zip(rs[:-1], rs[1:]):
            oa = a['pcc'] / max(1 - a['pcc'], 1e-300); ob = b['pcc'] / max(1 - b['pcc'], 1e-300)
            ea, eb = a.get('net_exit', float('nan')), b.get('net_exit', float('nan'))
            se = float(np.log(eb / ea) / np.log(b['N'] / a['N'])) if ea > 0 and eb > 0 else float('nan')
            s.append((a['N'], b['N'], float(np.log(ob / oa) / np.log(b['N'] / a['N'])), se))
        out['%s n=%d δ=%g' % key] = s
    return out


def write(rows):
    rows = sorted(rows, key=lambda r: (r['n'], r['arm'], r['delta'] if r['arm'] != 'Dpath' else 0, r['N'], -r.get('theta', 1e-6)))
    sl = slopes(rows)
    json.dump(dict(rows=rows, slopes=sl), open(os.path.join(ROOT, 'runs', 'drift_closure.json'), 'w'), indent=1, default=str)
    L = ['# Drift-closure experiment: eps->0 chain (PD, w = 0.3, eager_poly=False)', '',
         'Predictions: predictions/2026-10-02-drift-closure.md. Families (monomorphic self-cooperating states): FBfam cooperates '
         'with FairBot and ALLC; prudent cooperates with FairBot, defects on ALLC; rival defects on FairBot. Blocks, X and rival '
         'share as in runs/cert_pricing.md (π ≥ 1e-3, ALLC excluded).', '',
         '| cell | P(C,C) | π(D) | FBfam | prudent | rival | π(ALLC) | network exit | network entry | X | blocks | rival share | top coop | its π | top exits s / n / o | ALLC share | terminal | near-closed | absorb err | poly flow | cut flow | s |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        L.append('| %s | %.4f | %.4f | %.4f | %.4f | %.4f | %.1e | %.2e | %.2e | %.3f | %d | %.3f | `%s` | %.4f | %.2e / %.2e / %.2e | %.2f | %d | %d | %.0e | %.1e | %.1e | %.0f |' % (
            tag(r), r['pcc'], r['pi_D'], r['FBfam'], r['prudent'], r['rival'], r['ALLC'], r['net_exit'], r['net_entry'], r['universality'], r['n_blocks'], r['rival_share'],
            r['top_coop'], r['pi_top'], r['top_exit_strict'], r['top_exit_neutral'], r['top_exit_other'], r['allc_share'],
            r['n_terminal'], r['near_closed'], r['absorb_error'], r['poly_flow'], r['cut_flow'], r['time_s']))
    L += ['', '## Exits per mutation event from fixed worlds (total; strict / neutral / other; ALLC share)', '',
          '| cell | ' + ' | '.join(lab for lab, _ in WORLDS) + ' |', '|---|' + '---|' * len(WORLDS)]
    for r in rows:
        L.append('| %s | ' % tag(r) + ' | '.join(
            ('%.2e (%.1e / %.1e / %.1e; %.2f)' % (r[lab + '_exit'], r[lab + '_strict'], r[lab + '_neutral'], r[lab + '_other'], r[lab + '_allc'])
             if lab + '_exit' in r else '—') for lab, _ in WORLDS) + ' |')
    L += ['', '## Local odds slopes d log(P/(1-P)) / d log N', '']
    for k, s in sl.items():
        L.append('- %s: odds %s; network exit %s' % (k, ', '.join('%d→%d %.3f' % t[:3] for t in s), ', '.join('%.2f' % t[3] for t in s)))
    L += ['', '## Support (π ≥ 1e-3, top 8)', '']
    for r in rows:
        L.append('- %s: %s' % (tag(r), '; '.join('%s %.3f' % tuple(s) for s in r['support'])))
    open(os.path.join(ROOT, 'runs', 'drift_closure.md'), 'w').write('\n'.join(L) + '\n')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--workers', type=int, default=3); ap.add_argument('--smoke', action='store_true')
    a = ap.parse_args()
    J = jobs()
    if a.smoke:
        J = [('D', 8, 1e-2, 'D', 10000)]
    J.sort(key=lambda j: (-j[1], -j[4]))
    rows = []
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(cell, J):
            rows.append(r)
            print('%s: P(C,C) %.4f D %.4f FBfam %.4f prudent %.4f rival %.4f X %.3f blocks %d rival %.3f top %s exits s/n/o %.1e/%.1e/%.1e term %d nc %d (%.0fs)' % (
                tag(r), r['pcc'], r['pi_D'], r['FBfam'], r['prudent'], r['rival'], r['universality'], r['n_blocks'], r['rival_share'],
                r['top_coop'], r['top_exit_strict'], r['top_exit_neutral'], r['top_exit_other'], r['n_terminal'], r['near_closed'], r['time_s']), flush=True)
            if not a.smoke:
                write(rows)
    if a.smoke:
        print(json.dumps(rows, indent=1, default=str)[:4000])


if __name__ == '__main__':
    main()
