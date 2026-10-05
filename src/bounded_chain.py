"""lim_N under rare mutation for the semantic legibility gate (specs/2026-10-04-bounded-provers.md, item 2 and the
controls of item 4): eps->0 chain, PD, w = 0.3, eager_poly=False.

    python3 src/bounded_chain.py [--workers 3] [--smoke]
Writes runs/bounded-provers-chain.json (rows appended as cells finish; resumable).
"""
import os, sys, json, time, argparse
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import modal as M
from chain import Chain
from bounded import build_arm, BUDGETS, INF, FB, PB, PSTAR, ROOT
from cert_limN import top_exits

OUT = os.path.join(ROOT, 'runs', 'bounded-provers-chain.json')
SUP = 1e-3
NS = (100, 1000, 10000, 100000)


def base_name(s):
    return s.split('@')[0]


def networks(ch, prov, thr=SUP):
    """cert_limN.networks without name lookups: blocks of the mutual-cooperation graph over cooperative
    monomorphic states with pi >= thr, ALLC excluded."""
    names = prov.names; P = prov.PCC
    iC = names.index('C')
    coop = {}
    for key, wgt in zip(ch.keys_list, ch.pi):
        ids, x, kind = ch.states[key]
        if kind == 'poly':
            continue
        q = ids[0]
        if P[q, q] == 1 and q != iC:
            coop[q] = coop.get(q, 0.0) + wgt
    tot = sum(coop.values())
    allq = list(coop)
    pv = np.array([coop[q] for q in allq])
    X = float(pv @ P[np.ix_(allq, allq)] @ pv / tot ** 2) if tot > 0 else float('nan')
    S = [q for q in allq if coop[q] >= thr]
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
    fbs = [i for i, s in enumerate(names) if base_name(s) == FB]
    out = []
    for mem in blocks:
        mass = sum(coop[q] for q in mem)
        top = max(mem, key=lambda q: coop[q])
        out.append(dict(mass=mass, size=len(mem), top=names[top], has_FB=any(q in fbs for q in mem),
                        coops_with_FB=bool(any(P[top, f] == 1 for f in fbs)),
                        members=[(names[q], coop[q]) for q in sorted(mem, key=lambda q: -coop[q])][:6]))
    out.sort(key=lambda b: -b['mass'])
    btot = sum(b['mass'] for b in out)
    for b in out:
        b['share'] = b['mass'] / btot if btot > 0 else float('nan')
    return dict(coop_mass=tot, universality=X, blocks=out, n_blocks=len(out),
                rival_share=1 - out[0]['share'] if out else float('nan'))


def cell(job):
    kind, b, n, N = job
    t = time.time()
    a = build_arm(n, kind, b)
    prov = a['prov']; names = prov.names; P = prov.PCC
    lang = M.ClassLang(prov)
    ch = Chain(prov, N=N, w=0.3, verbose=False, eager_poly=False).explore()
    pcc = 0.0; pis = {}; key_of = {}; poly = 0.0
    for key, wgt in zip(ch.keys_list, ch.pi):
        ids, x, kd = ch.states[key]; ids = list(ids); x = np.asarray(x)
        pcc += wgt * float(x @ P[np.ix_(ids, ids)] @ x)
        if kd == 'mono':
            pis[ids[0]] = pis.get(ids[0], 0.0) + wgt; key_of[ids[0]] = key
        else:
            poly += wgt
    iD = names.index('D'); iC = names.index('C')
    coop_states = [(v, q) for q, v in pis.items() if P[q, q] == 1 and q != iC]
    v, qtop = max(coop_states)
    fam = {}
    for lab, s in (('FB', FB), ('FB1', 'BOX1(THEM(ME))'), ('BTT', 'BOX(THEM(THEM))'), ('BTT1', 'BOX1(THEM(THEM))'), ('PB', PB), ('Pstar', PSTAR)):
        fam[lab] = float(sum(p for q, p in pis.items() if base_name(names[q]) == s))
    out = dict(kind=kind, b=b, n=n, N=N, n_classes=len(names), pcc=pcc, pi_D=pis.get(iD, 0.0), pi_C=pis.get(iC, 0.0), poly=poly,
               top_coop=names[qtop], pi_top=v, fam=fam,
               cut_flow=ch.cut_flow, indeterminate=len(ch.indeterminate), n_terminal=len(ch.terminal),
               near_closed=int(getattr(ch, 'near_closed', 0)), n_states=len(ch.trans),
               support=[(ch.describe_state(k, lang), float(p)) for k, p in ch.support(SUP)][:8])
    out.update(networks(ch, prov))
    out.update(top_exits(ch, prov, key_of[qtop]))
    # exits of named worlds
    for lab, s in (('FB', FB), ('PB', PB), ('Pstar', PSTAR)):
        cands = [i for i, nm in enumerate(names) if base_name(nm) == s]
        if not cands: continue
        q = max(cands, key=lambda i: pis.get(i, 0.0))
        k = ch.mono(q); ch.expand(k)
        e = top_exits(ch, prov, k)
        out[lab + '_exit'] = dict(name=names[q], total=e['top_exit'], strict=e['top_exit_strict'], neutral=e['top_exit_neutral'],
                                  other=e['top_exit_other'], dest=e['top_dest'][:3])
    # per-program arms: prover pi by budget (mu-weighted within a class)
    if kind in ('fixed', 'penal'):
        gb = a['gb']; mu = a['mu']
        byb = {}; amb = 0.0
        for q, p in pis.items():
            if P[q, q] != 1 or q == iC: continue
            mem = prov.members_geno[q]
            bs = [gb[g] for g in mem if np.isfinite(gb[g])]
            if not bs: continue
            if len(set(bs)) > 1: amb += p
            w = np.array([mu[g] for g in mem if np.isfinite(gb[g])]); w = w / w.sum()
            for bb, ww in zip(bs, w):
                byb[str(int(bb))] = byb.get(str(int(bb)), 0.0) + p * ww
        out['prover_pi_by_b'] = byb; out['prover_pi_b_ambiguous'] = amb
        # the top state's budgets
        out['top_budgets'] = sorted({int(gb[g]) for g in prov.members_geno[qtop] if np.isfinite(gb[g])})
    if a.get('fp') is not None and kind in ('global', 'random', 'atom'):
        nat = M.ModalLanguage(n).arrays()[0] if False else None
    out['time_s'] = time.time() - t
    return out


def jobs():
    J = []
    for n in (6, 8):
        for N in NS:
            for b in BUDGETS:
                J.append(('global', b, n, N))
            for b in BUDGETS[:-1]:
                J.append(('random', b, n, N))
            J.append(('atom', 1, n, N))
            J.append(('fixed', None, n, N))
            J.append(('penal', None, n, N))
            J.append(('clique', None, n, N))
    return J


def key(j):
    return '%s|%s|%d|%d' % (j[0], j[1], j[2], j[3])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--workers', type=int, default=3); ap.add_argument('--smoke', action='store_true')
    ap.add_argument('--only', nargs='*')
    a = ap.parse_args()
    rows = json.load(open(OUT)) if os.path.exists(OUT) and not a.smoke else []
    done = {key((r['kind'], r['b'], r['n'], r['N'])) for r in rows}
    J = [j for j in jobs() if key(j) not in done]
    if a.only:
        J = [j for j in J if j[0] in a.only]
    if a.smoke:
        J = [('global', 4, 6, 1000), ('fixed', None, 6, 1000), ('penal', None, 6, 1000), ('clique', None, 6, 1000), ('random', 4, 6, 1000)]
    cost = lambda j: (j[2] == 8) * 10 + (j[0] in ('fixed', 'penal')) * 5 + np.log10(j[3])
    J.sort(key=lambda j: -cost(j))
    print('%d jobs' % len(J), flush=True)
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(cell, J):
            rows.append(r)
            print('%s b=%s n=%d N=%d: P(C,C) %.4f top %s %.3f exits s/n/o %.1e/%.1e/%.1e rival %.3f classes %d (%.0fs)' % (
                r['kind'], r['b'], r['n'], r['N'], r['pcc'], r['top_coop'], r['pi_top'], r['top_exit_strict'], r['top_exit_neutral'],
                r['top_exit_other'], r['rival_share'], r['n_classes'], r['time_s']), flush=True)
            if not a.smoke:
                json.dump(rows, open(OUT, 'w'), indent=1, default=str)
    if a.smoke:
        print(json.dumps(rows, indent=1, default=str)[:4000])


if __name__ == '__main__':
    main()
