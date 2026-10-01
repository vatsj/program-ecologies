"""Certificate pricing vs lazy pricing vs c = 0: eps->0 chain, PD, w = 0.3
(predictions/2026-10-01-cert-pricing.md).

    python3 src/cert_limN.py [--workers 3]
Writes runs/cert_pricing.md and runs/cert_pricing.json.
"""
import json, os, sys, time, argparse
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import modal as M
import cert_priced as CP
from chain import Chain

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PSTAR = 'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))'
PB = 'and(BOX(THEM(ME)),BOXD1(THEM(^D)))'
FB = 'BOX(THEM(ME))'
SUP = 1e-3          # support threshold on a state's pi


def networks(ch, prov, thr=SUP):
    """Blocks of the mutual-cooperation graph over the cooperative monomorphic support (ALLC excluded and
    reported separately [after review])."""
    names = prov.names; P = prov.PCC
    iC = names.index('C')
    coop = {}; poly_coop = 0.0; poly = 0.0
    for key, wgt in zip(ch.keys_list, ch.pi):
        ids, x, kind = ch.states[key]
        if kind == 'poly':
            poly += wgt
            ids = list(ids); x = np.asarray(x)
            if float(x @ P[np.ix_(ids, ids)] @ x) > 0.5: poly_coop += wgt
            continue
        q = ids[0]
        if P[q, q] == 1 and q != iC:
            coop[q] = coop.get(q, 0.0) + wgt
    tot = sum(coop.values())
    allq = list(coop)
    pv = np.array([coop[q] for q in allq])
    X = float(pv @ P[np.ix_(allq, allq)] @ pv / tot ** 2) if tot > 0 else float('nan')
    S = [q for q in allq if coop[q] >= thr]
    # connected components over S
    comp = {}; blocks = []
    for s in S:
        if s in comp: continue
        stack = [s]; mem = []; comp[s] = len(blocks)
        while stack:
            a = stack.pop(); mem.append(a)
            for b in S:
                if b not in comp and P[a, b] == 1:
                    comp[b] = len(blocks); stack.append(b)
        blocks.append(mem)
    iFB = names.index(FB); iPS = names.index(PSTAR) if PSTAR in names else None
    out = []
    for mem in blocks:
        mass = sum(coop[q] for q in mem)
        clique = all(P[a, b] == 1 for a in mem for b in mem)
        top = max(mem, key=lambda q: coop[q])
        out.append(dict(mass=mass, share=mass / tot if tot > 0 else float('nan'), clique=bool(clique), size=len(mem),
                        top=names[top], has_FB=bool(iFB in mem), coops_with_FB=bool(P[top, iFB] == 1),
                        members=[(names[q], coop[q]) for q in sorted(mem, key=lambda q: -coop[q])][:8]))
    out.sort(key=lambda b: -b['mass'])
    btot = sum(b['mass'] for b in out)
    for b in out:
        b['share'] = b['mass'] / btot if btot > 0 else float('nan')
    # P*-block: cooperative states that mutually cooperate with P* and not with FairBot
    pstar_block = sum(v for q, v in coop.items() if iPS is not None and P[q, iPS] == 1 and P[q, iFB] != 1)
    fb_block = sum(v for q, v in coop.items() if P[q, iFB] == 1)
    return dict(coop_mass=tot, universality=X, blocks=out, n_blocks=len(out), below_thr=tot - sum(coop[q] for q in S),
                rival_share=1 - out[0]['share'] if out else float('nan'),
                fb_block=fb_block, pstar_block=pstar_block, pi_pstar=coop.get(iPS, 0.0) if iPS is not None else 0.0,
                poly=poly, poly_coop=poly_coop)


def top_exits(ch, prov, key):
    U = prov.Ufull; names = prov.names
    a = ch.states[key][0][0]; uaa = U[a, a]
    ex = dict(strict=0.0, neutral=0.0, other=0.0); dest = {}
    for b, v in ch.trans.get(key, {}).items():
        if b == key: continue
        for q, mw in ch.trans_mut[(key, b)].items():
            if U[q, a] > uaa + 1e-12: t = 'strict'
            elif max(abs(U[q, a] - uaa), abs(U[a, q] - uaa), abs(U[q, q] - uaa)) < 1e-12: t = 'neutral'
            else: t = 'other'
            ex[t] += mw
            dest[(names[q], t)] = dest.get((names[q], t), 0.0) + mw
    tot = sum(ex.values())
    return dict(top_exit=tot, top_exit_strict=ex['strict'], top_exit_neutral=ex['neutral'], top_exit_other=ex['other'],
                allc_share=sum(v for (s, t), v in dest.items() if s == 'C') / tot if tot else float('nan'),
                top_dest=[(s, t, v) for (s, t), v in sorted(dest.items(), key=lambda kv: -kv[1])[:4]])


def cell(job):
    pricing, n, c, N = job[:4]
    theta = job[4] if len(job) > 4 else 1e-6
    t = time.time()
    L, val, worlds, prov, extra = CP.build_cert(n, c, pricing=pricing)
    names = prov.names; P = prov.PCC
    lang = M.ClassLang(prov)
    ch = Chain(prov, N=N, w=0.3, verbose=False, eager_poly=False, theta=theta).explore()
    pcc = 0.0; pis = {}; key_of = {}
    for key, wgt in zip(ch.keys_list, ch.pi):
        ids, x, kind = ch.states[key]; ids = list(ids); x = np.asarray(x)
        pcc += wgt * float(x @ P[np.ix_(ids, ids)] @ x)
        if kind == 'mono':
            pis[ids[0]] = pis.get(ids[0], 0.0) + wgt; key_of[ids[0]] = key
    iD = names.index('D')
    coop_states = [(v, q) for q, v in pis.items() if P[q, q] == 1 and names[q] != 'C']
    v, qtop = max(coop_states)
    get = lambda s: pis.get(names.index(s), 0.0) if s in names else 0.0
    out = dict(pricing=pricing, n=n, c=c, N=N, theta=theta, n_classes=len(names), pcc=pcc, pi_D=pis.get(iD, 0.0),
               pi_C=get('C'), pi_FB=get(FB), pi_FB1=get('BOX1(THEM(ME))'), pi_BTT=get('BOX(THEM(THEM))'), pi_PB=get(PB),
               top_coop=names[qtop], pi_top=v, home_payoff_top=float(prov.Ufull[qtop, qtop]),
               cut_flow=ch.cut_flow, indeterminate=len(ch.indeterminate), n_terminal=len(ch.terminal),
               near_closed=int(getattr(ch, 'near_closed', 0)), absorb_error=float(getattr(ch, 'absorb_error', 0.0)),
               n_states=len(ch.trans),
               support=[(ch.describe_state(k, lang), float(p)) for k, p in ch.support(SUP)][:8])
    out.update(networks(ch, prov))
    nb4 = networks(ch, prov, thr=1e-4)
    out.update(n_blocks_1e4=nb4['n_blocks'], rival_share_1e4=nb4['rival_share'])
    for lab, s in (('btt', 'BOX(THEM(THEM))'), ('nbm', 'not(BOX(THEM(ME)))')):
        if s in names:
            k = ch.mono(names.index(s)); ch.expand(k)
            e = top_exits(ch, prov, k)
            out.update({lab + '_exit_strict': e['top_exit_strict'], lab + '_exit_neutral': e['top_exit_neutral'],
                        lab + '_exit_other': e['top_exit_other'], lab + '_dest': e['top_dest']})
    out.update(top_exits(ch, prov, key_of[qtop]))
    # the P* world's exits (incumbency check), if P* is a class
    if PSTAR in names:
        kP = ch.mono(names.index(PSTAR)); ch.expand(kP)
        e = top_exits(ch, prov, kP)
        out.update(pstar_exit=e['top_exit'], pstar_exit_strict=e['top_exit_strict'], pstar_exit_neutral=e['top_exit_neutral'],
                   pstar_exit_other=e['top_exit_other'], pstar_dest=e['top_dest'])
    out['time_s'] = time.time() - t
    return out


def jobs():
    J = []
    for n in (6, 8):
        for N in (100, 1000, 10000, 30000):
            J.append(('atoms', n, 0.0, N))
            for c in (1e-3, 1e-2):
                for p in ('cert0', 'lazy', 'cert1', 'certC'):
                    J.append((p, n, c, N))
                if n == 8:      # controls [after review]
                    for p in ('mono', 'cert0flat', 'lazycert0', 'cert0diag'):   # cert0v: static only (see predictions)
                        J.append((p, n, c, N))
    for p in ('atoms', 'cert0', 'lazy'):            # one larger N [after review]
        J.append((p, 8, 0.0 if p == 'atoms' else 1e-2, 100000))
    for p in ('cert0', 'lazy'):                      # theta check in the stickiest cells [after review]
        J.append((p, 8, 1e-2, 30000, 1e-7))
    return J


def fmt_blocks(r):
    return '; '.join('%s%s %.3f (%d%s)' % ('FB-block ' if b['has_FB'] else '', b['top'], b['mass'], b['size'], ', clique' if b['clique'] else '')
                     for b in r['blocks'][:3])


ORDER = {'atoms': 0, 'lazy': 1, 'cert0': 2, 'cert1': 3, 'certC': 4, 'mono': 5, 'cert0flat': 6, 'lazycert0': 7, 'cert0diag': 8, 'cert0v': 9}


def tag(r):
    return '%s n=%d c=%g N=%d%s' % (r['pricing'], r['n'], r['c'], r['N'], '' if r.get('theta', 1e-6) == 1e-6 else ' θ=%g' % r['theta'])


def write(rows):
    rows = sorted(rows, key=lambda r: (r['n'], ORDER[r['pricing']], r['c'], r['N'], -r.get('theta', 1e-6)))
    json.dump(rows, open(os.path.join(ROOT, 'runs', 'cert_pricing.json'), 'w'), indent=1, default=str)
    L = ['# Certificate pricing vs lazy vs c = 0: eps->0 chain (PD, w = 0.3, eager_poly=False)', '',
         'Predictions: predictions/2026-10-01-cert-pricing.md. Blocks: components of the mutual-cooperation graph over '
         'self-cooperating monomorphic states with π ≥ 1e-3, ALLC excluded (π(ALLC) reported). X: threshold-free '
         'π-weighted mutual-cooperation probability over the same states. θ = 1e-6 unless marked.', '',
         '| cell | P(C,C) | π(D) | π(ALLC) | coop mass (excl. ALLC) | X | blocks | rival share | blocks at 1e-4 | rival share at 1e-4 | FB-block π | P*-block π | π(PB) | top coop state | its π | top exits: strict / neutral / other | ALLC share | terminal | near-closed | absorb err | poly π | cut flow | s |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        L.append('| %s | %.4f | %.4f | %.1e | %.4f | %.3f | %d | %.3f | %d | %.3f | %.4f | %.4f | %.4f | `%s` | %.4f | %.2e / %.2e / %.2e | %.2f | %d | %d | %.0e | %.1e | %.1e | %.0f |' % (
            tag(r), r['pcc'], r['pi_D'], r['pi_C'], r['coop_mass'], r['universality'], r['n_blocks'], r['rival_share'],
            r['n_blocks_1e4'], r['rival_share_1e4'], r['fb_block'], r['pstar_block'], r['pi_PB'], r['top_coop'], r['pi_top'],
            r['top_exit_strict'], r['top_exit_neutral'], r['top_exit_other'], r['allc_share'], r['n_terminal'], r['near_closed'],
            r['absorb_error'], r['poly'], r['cut_flow'], r['time_s']))
    L += ['', '## Blocks of the mutual-cooperation graph (top 3 per cell)', '', '| cell | blocks: top member, π mass (size, clique?) |', '|---|---|']
    for r in rows:
        L.append('| %s | %s |' % (tag(r), fmt_blocks(r)))
    L += ['', '## Exits per mutation event from the P* world (`%s`), BTT (`BOX(THEM(THEM))`) and nBM (`not(BOX(THEM(ME)))`)' % PSTAR, '',
          '| cell | P*: strict / neutral / other | P* top destinations | BTT: strict / neutral / other | nBM: strict / neutral / other | nBM top destinations |', '|---|---|---|---|---|---|']
    for r in rows:
        if 'pstar_exit' in r:
            L.append('| %s | %.2e / %.2e / %.2e | %s | %.2e / %.2e / %.2e | %.2e / %.2e / %.2e | %s |' % (
                tag(r), r['pstar_exit_strict'], r['pstar_exit_neutral'], r['pstar_exit_other'],
                '; '.join('`%s` (%s) %.1e' % tuple(d) for d in r['pstar_dest'][:2]),
                r.get('btt_exit_strict', 0), r.get('btt_exit_neutral', 0), r.get('btt_exit_other', 0),
                r.get('nbm_exit_strict', 0), r.get('nbm_exit_neutral', 0), r.get('nbm_exit_other', 0),
                '; '.join('`%s` (%s) %.1e' % tuple(d) for d in r.get('nbm_dest', [])[:2])))
    L += ['', '## Support (π ≥ 1e-3, top 8)', '']
    for r in rows:
        L.append('- %s: %s' % (tag(r), '; '.join('%s %.3f' % tuple(s) for s in r['support'])))
    open(os.path.join(ROOT, 'runs', 'cert_pricing.md'), 'w').write('\n'.join(L) + '\n')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--workers', type=int, default=3); ap.add_argument('--smoke', action='store_true')
    a = ap.parse_args()
    J = jobs()
    if a.smoke:
        J = [('cert0', 6, 1e-2, 100)]
    J.sort(key=lambda j: (-j[1], -j[3]))
    rows = []
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(cell, J):
            rows.append(r)
            print('%s: P(C,C) %.4f X %.3f blocks %d rival %.3f FB-block %.4f P*-block %.4f top %s exits s/n/o %.1e/%.1e/%.1e term %d nc %d (%.0fs)' % (
                tag(r), r['pcc'], r['universality'], r['n_blocks'], r['rival_share'], r['fb_block'], r['pstar_block'],
                r['top_coop'], r['top_exit_strict'], r['top_exit_neutral'], r['top_exit_other'], r['n_terminal'], r['near_closed'], r['time_s']), flush=True)
            if not a.smoke:
                write(rows)
    if a.smoke:
        print(json.dumps(rows, indent=1, default=str)[:3000])


if __name__ == '__main__':
    main()
