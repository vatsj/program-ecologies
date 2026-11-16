"""Step 1 of queue 80: length-prior mass witnesses for the script carriers (every listed spelling with its script; no search, no Monte Carlo).

Measures (the frame lam^3 is fixed; only the body is drawn; masses conditional on finite trees; queue 75's prior: each node draws its
tag uniformly among the machine's tags, literals and indices Elias-gamma, `lib` uniform over the library, `con` over 5, `op` over 7):
  M1 (CHKS a primitive)  R1's tags plus an arity-1 tag `chks` for (lib CHKS) applied; the script counted as data nodes (pair / nat);
                         other library calls (OFFER, ELIG) are `lib` leaves; reads are R1's `readn` / `readp`
  M1-free                M1 with the script not charged (the packaging's script literal replaced by a 1-node literal)
  M2 (R1 written)        R1's tags; CHKS as a `lib` leaf
  M3 (fully written)     no library: the body's R0 nodes plus every library entry reachable from it (the checker's helpers are
                         recursive through `lib`, so they cannot be inlined as a tree; each reachable entry is counted once, a
                         lower bound on the size of any closed spelling); reported as a node count and log10 mass <= -nodes log10(T_R0)
Comparators: the 6-node fair single reader Snon (if (eq readn 4) 1 4), the bully Bn, the fallbacks, queue 79's skeleton carriers
(its step1.json, R1-written and C1 measures).

    python3 src/script_offers_prior.py OUTDIR
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import lt_code as L
import lt_prior as P
import script_offers as S
import certified_offers_prior as CP

P.ARITY['chks'] = 1
M1 = P.Machine('M1', P.R1.tags + ['chks'])
NLIB = len(L.LIB)


def log10mass(t, mach, nlib=NLIB):
    lt = -math.log10(mach.T)
    tag = t[0]
    if tag == 'lib':
        return lt - math.log10(nlib)
    if tag in ('v', 'nat'):
        return lt + math.log10(P.elias(t[1]))
    if tag == 'con':
        return lt - math.log10(5)
    if tag in ('readn', 'readp'):
        return lt
    if tag == 'op':
        return lt - math.log10(7) + log10mass(t[2], mach, nlib) + log10mass(t[3], mach, nlib)
    return lt + sum(log10mass(c, mach, nlib) for c in t[1:])


def nodes(t):
    tag = t[0]
    if tag in ('v', 'nat', 'con', 'lib', 'readn', 'readp'):
        return 1
    if tag in ('lam', 'fst', 'snd', 'fix', 'quote', 'chks'):
        return 1 + nodes(t[1])
    if tag == 'op':
        return 1 + nodes(t[2]) + nodes(t[3])
    return 1 + sum(nodes(c) for c in t[1:])


def to_chks(t):
    if t[0] == 'app' and t[1] == ('lib', S.ID_CHKS):
        return ('chks', to_chks(t[2]))
    if t[0] in ('v', 'nat', 'con', 'lib', 'readn', 'readp'):
        return t
    if t[0] in ('lam', 'fix', 'fst', 'snd', 'quote'):
        return (t[0], to_chks(t[1]))
    if t[0] == 'op':
        return ('op', t[1], to_chks(t[2]), to_chks(t[3]))
    return (t[0],) + tuple(to_chks(c) for c in t[1:])


def libs_in(t, acc):
    if t[0] == 'lib':
        acc.add(t[1]); return acc
    if t[0] in ('v', 'nat', 'con', 'readn', 'readp'):
        return acc
    if t[0] == 'op':
        libs_in(t[2], acc); libs_in(t[3], acc); return acc
    for c in t[1:]:
        if isinstance(c, tuple):
            libs_in(c, acc)
    return acc


def reachable_lib_nodes(t):
    seen = set(); todo = list(libs_in(t, set()))
    while todo:
        i = todo.pop()
        if i in seen:
            continue
        seen.add(i)
        todo += list(libs_in(L.LIB[i], set()) - seen)
    return seen, sum(P.node_count(L.LIB[i]) for i in seen)


def main(outdir):
    fbR1 = {nm: ('lam', ('lam', ('lam', CP.body_of(nm)))) for nm in ('C1', 'C4', 'C3', 'C0', 'Snoy', 'Spoy', 'Bn', 'Bp')}
    cat = S.s_carriers()
    scripts = {}
    import script_offers_cat as SC
    for nm, f, sp, t, m in SC.library_s():
        if m.get('carrier'):
            scripts[nm] = m['script']
    qM1, qR1, qR0 = M1.extinction(), P.R1.extinction(), P.R0.extinction()
    lq = dict(M1=math.log10(qM1), R1=math.log10(qR1), R0=math.log10(qR0))
    res = dict(T=dict(M1=M1.T, R1=P.R1.T, R0=P.R0.T), q=dict(M1=qM1, R1=qR1, R0=qR0), nlib=NLIB, programs={})
    for nm in ('Snon', 'Snoy', 'Bn'):
        B = CP.body_of(nm)
        res['programs'][nm] = dict(nodes_R1=nodes(B), M1=log10mass(B, M1) - lq['M1'], R1=log10mass(B, P.R1) - lq['R1'])
    for nm, fam, sp, prm in cat:
        body = S.body_spelling(sp, prm['fn'], prm['fp'], prm['pf'], prm['H'], prm['R'], fbR1[prm['fb']])
        scr = scripts[nm]
        full = ('if', ('con', 'T'), body, S.data_term(scr))
        free = ('if', ('con', 'T'), body, ('nat', 0))
        b1 = to_chks(full); b1f = to_chks(free)
        _, libn = reachable_lib_nodes(body)
        r0nodes = P.node_count(P.expand(full, 0)) if True else None
        res['programs'][nm] = dict(fam=fam, sp=sp, script_nodes=S.script_nodes(scr), nodes_M1=nodes(b1), nodes_M1free=nodes(b1f),
                                   nodes_M2=nodes(full), M1=log10mass(b1, M1) - lq['M1'], M1free=log10mass(b1f, M1) - lq['M1'],
                                   M2=log10mass(full, P.R1) - lq['R1'], nodes_M3=r0nodes + libn,
                                   M3_bound=-(r0nodes + libn) * math.log10(P.R0.T) - lq['R0'],
                                   script_share_M1=S.script_nodes(scr) / nodes(b1))
    fr = res['programs']['Snon']
    fams = {}
    for nm, v in res['programs'].items():
        if 'fam' not in v:
            continue
        g = fams.setdefault(v['fam'], dict(members=0))
        g['members'] += 1
        for k in ('M1', 'M1free', 'M2'):
            if k + '_best' not in g or v[k] > g[k + '_best']:
                g[k + '_best'] = v[k]; g[k + '_best_prog'] = nm; g[k + '_best_nodes'] = v['nodes_' + ('M1' if k == 'M1' else ('M1free' if k == 'M1free' else 'M2'))]
            vals = [res['programs'][x][k] for x in res['programs'] if res['programs'][x].get('fam') == v['fam']]
            mx = max(vals)
            g[k + '_total_log10'] = mx + math.log10(sum(10 ** (x - mx) for x in vals))
        g['M3_min_nodes'] = min(g.get('M3_min_nodes', 10 ** 9), v['nodes_M3'])
        g['script_share_min'] = min(g.get('script_share_min', 1.0), v['script_share_M1'])
        g['script_share_max'] = max(g.get('script_share_max', 0.0), v['script_share_M1'])
    for g in fams.values():
        g['M1_best_to_fair_reader_log10'] = g['M1_best'] - fr['M1']
        g['M1free_best_to_fair_reader_log10'] = g['M1free_best'] - fr['M1']
        g['M2_best_to_fair_reader_log10'] = g['M2_best'] - fr['R1']
    res['families'] = fams
    q79 = json.load(open(os.path.join(ROOT, 'runs', 'certified_offers', 'step1.json')))
    res['queue79'] = {k: dict(nodes_C1=v['nodes_C1'], C1=v['C1'], nodes_R1w=v['nodes_R1w'], R1w=v['R1w'])
                      for k, v in q79['programs'].items() if k in ('Ocn', 'Rcn', 'FcSnoy', 'Bcn')}
    os.makedirs(outdir, exist_ok=True)
    json.dump(res, open(os.path.join(outdir, 'step1.json'), 'w'), indent=1)
    Lx = ['# Queue 80 step 1: mass witnesses (log10, conditional on finite trees)', '',
          'Fair single reader Snon (6 nodes): M1 %.2f, R1 %.2f. Bully Bn: M1 %.2f.' % (fr['M1'], fr['R1'], res['programs']['Bn']['M1']), '',
          '| family | best spelling (M1) | nodes | log10 M1 | / fair reader | M1 script free: best, / reader | M2 (R1 written): best, / reader | M3 nodes (min) | script share of M1 nodes |',
          '|---|---|---|---|---|---|---|---|---|']
    for f, g in fams.items():
        Lx.append('| %s | %s | %d | %.1f | %.1f | %.1f, %.1f | %.1f, %.1f | %d | %.2f–%.2f |' % (
            f, g['M1_best_prog'], g['M1_best_nodes'], g['M1_best'], g['M1_best_to_fair_reader_log10'], g['M1free_best'],
            g['M1free_best_to_fair_reader_log10'], g['M2_best'], g['M2_best_to_fair_reader_log10'], g['M3_min_nodes'],
            g['script_share_min'], g['script_share_max']))
    open(os.path.join(outdir, 'step1.md'), 'w').write('\n'.join(Lx) + '\n')
    return res


if __name__ == '__main__':
    main(sys.argv[1])
    print(open(os.path.join(sys.argv[1], 'step1.md')).read())
