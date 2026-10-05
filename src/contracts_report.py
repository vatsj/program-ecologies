"""Report for proof-carrying contracts v1: runs/proof-carrying-contracts.md and .json.

    python3 src/contracts_report.py
"""
import json, os, sys
from collections import defaultdict
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')


def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'), float('nan'))
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def load(name):
    p = os.path.join(RUNS, name)
    return json.load(open(p)) if os.path.exists(p) else []


def cellkey(r):
    return (r['tag'], r['b'], r['s'], r['f0'], r['sigma'], r['start'], r['N'], r['uniform'])


def f3(x):
    return '%.3f' % x if x == x else 'nan'


def first_cross(tr, thr=0.5, every=1000):
    for i, row in enumerate(tr):
        if row[0] > thr:
            return i * every
    return None


def verdicts(summ, lsum, ssum):
    """Numbers for each prediction; the held/failed call is written by hand in the RESULTS draft from these lines."""
    def g(b, s, f0, sg, start='mu', N=6400, uni=False, tag=None):
        t = tag or ('uniform' if uni else ('grid' if N == 6400 else 'Npath'))
        return summ.get((t, b, s, f0, sg, start, N, uni))
    def pm(c, f='pcc_mean'):
        return f3(c[f]) if c else 'n/a'
    L = ['', '## Numbers for the verdicts (μ seed unless stated)', '']
    # P1
    L.append('- **P1** b = 2, s = 0, f₀ = 0: %s (pred < 0.3). b = 2, f₀ = 1: s = 0/σ = 0 %s, s = 1/σ = 0 %s, s = 0/σ = 1 %s. '
             'Contract baseline b = ∞, f₀ = 1, s = 1, σ = 0: %s; s = 0, σ = 0: %s. Source oracle b = ∞, s = 0, f₀ = 0: %s.' % (
                 pm(g('2', 0, 0.0, 0.0)), pm(g('2', 0, 1.0, 0.0)), pm(g('2', 1, 1.0, 0.0)), pm(g('2', 0, 1.0, 1.0)),
                 pm(g('inf', 1, 1.0, 0.0)), pm(g('inf', 0, 1.0, 0.0)), pm(g('inf', 0, 0.0, 0.0))))
    # P2
    rows = []
    for b in ('2', '4', 'inf'):
        for s in (0, 1):
            for f0 in ((0.01, 1.0) if s == 0 else (0.0, 0.01, 1.0)):
                c = g(b, s, f0, 1.0); u = g(b, s, f0, 1.0, uni=True)
                if c:
                    rows.append('b=%s s=%d f₀=%g: FB-con %s, P*-con %s, top %s; uniform FB-con %s top %s' % (
                        b, s, f0, f3(c['fb_con']), f3(c['ps_con']), c['top_contracts'][0] if c['top_contracts'] else '-',
                        f3(u['fb_con']) if u else 'n/a', (u['top_contracts'][0] if u and u['top_contracts'] else '-')))
    L.append('- **P2** (σ = 1): ' + ' | '.join(rows))
    # P3
    L.append('- **P3** key cell b = 2, s = 0, f₀ = 0.01: σ = 1 %s, σ = 0 %s, σ = 0.1 %s. N path σ = 1: %s; σ = 0: %s.' % (
        pm(g('2', 0, 0.01, 1.0)), pm(g('2', 0, 0.01, 0.0)), pm(g('2', 0, 0.01, 0.1)),
        ' / '.join(pm(g('2', 0, 0.01, 1.0, N=N)) for N in (1600, 6400, 25600)),
        ' / '.join(pm(g('2', 0, 0.01, 0.0, N=N)) for N in (1600, 6400, 25600))))
    # P4
    rows = []
    for k, c in sorted(summ.items()):
        if k[0] == 'grid' and k[5] == 'mu':
            rows.append((k[1], k[2], k[3], k[4], c['src_allc'], c['con_allc']))
    srcl = [r[4] for r in rows] or [float('nan')]
    infl = [r[4] for r in rows if r[0] == 'inf'] or [float('nan')]
    L.append('- **P4** source-ALLC load over μ-seed grid cells: min %.3f, max %.3f, median %.3f; at b = ∞ min %.3f. Contract-ALLC load at f₀ = 1: %s; at f₀ < 1: %s.' % (
        min(srcl), max(srcl), float(np.median(srcl)), min(infl),
        ', '.join('%s/%d/%g: %.2f vs %.2f' % (r[0], r[1], r[3], r[4], r[5]) for r in rows if r[2] == 1.0 and r[0] == 'inf'),
        ', '.join('%s/%d/%g/%g: %.2f vs %.2f' % (r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows if r[2] < 1.0 and r[0] == 'inf')))
    # P5
    if lsum:
        rows = []
        for cell in ((100, 4), (400, 4), (100, 64), (100, 256)):
            fr = lambda b, f0, sg: lsum.get('%d,%d,%s,%g,%g' % (cell[0], cell[1], b, f0, sg), {}).get('frac', float('nan'))
            rows.append('(%d, %d): free %.2f; b=2 f₀=0 %.2f; b=2 f₀=1 σ=0 %.2f / σ=1 %.2f; b=2 f₀=0.01 σ=0 %.2f / σ=1 %.2f; b=∞ f₀=1 σ=0 %.2f' % (
                cell[0], cell[1], fr('inf', 0.0, 0.0), fr('2', 0.0, 0.0), fr('2', 1.0, 0.0), fr('2', 1.0, 1.0), fr('2', 0.01, 0.0), fr('2', 0.01, 1.0), fr('inf', 1.0, 0.0)))
        L.append('- **P5** ' + ' | '.join(rows))
    # P6
    rows = []
    for k, c in sorted(summ.items()):
        if k[4] == 1.0 and k[5] == 'mu' and k[6] == 6400:
            rows.append('%s b=%s s=%d f₀=%g: max label %.2f, FB-label %.2f, FB-con %.2f, max con %.2f' % ('uni' if k[7] else 'pay', k[1], k[2], k[3], c['max_lab'], c['fb_lab'], c['fb_con'], c['max_con']))
    L.append('- **P6** ' + ' | '.join(rows))
    # RS
    anti = [c['anti'] for k, c in summ.items() if k[6] == 6400]
    L.append('- **RS-a** f₀ = 1 vs free (b = ∞, s = 0, f₀ = 0 = %s): %s. **RS-b** anti-prover share max over cells %.4f.' % (
        pm(g('inf', 0, 0.0, 0.0)), '; '.join('b=%s s=%d σ=%g %s' % (b, s, sg, pm(g(b, s, 1.0, sg))) for b in ('2', '4', 'inf') for s in (0, 1) for sg in (0.0, 0.1, 1.0)),
        max(anti) if anti else float('nan')))
    if ssum:
        L.append('- **S1–S4** (b = 0): ' + '; '.join('s=%d f₀=%g σ=%g %.3f' % (k[0], k[1], k[2], v['pcc_mean']) for k, v in sorted(ssum.items())))
    return L


def main():
    st = json.load(open(os.path.join(RUNS, 'contracts_static.json')))
    grid = load('contracts_grid.json'); lot = load('contracts_lottery.json')
    cells = defaultdict(list)
    for r in grid:
        cells[cellkey(r)].append(r)
    summ = {}
    for k, rs in cells.items():
        rs = sorted(rs, key=lambda r: r['rep'])
        def m(f): return float(np.mean([r[f] for r in rs]))
        tops = defaultdict(float)
        for r in rs:
            for c, v in r['top_contracts']: tops[c] += v / len(rs)
        labs = defaultdict(float)
        for r in rs:
            for c, v in r['top_labels']: labs[c] += v / len(rs)
        srcs = defaultdict(float)
        for r in rs:
            for c, v in r['top_sources']: srcs[c] += v / len(rs)
        trans = defaultdict(int)
        for r in rs:
            for a, b, n in r['con_trans']: trans[(a, b)] += n
        sw = defaultdict(int); routes = defaultdict(int); byc = defaultdict(lambda: [0, 0, 0])
        for r in rs:
            for f in ('accepted', 'same', 'rejected', 'donor_none', 'accepted_2nd', 'same_2nd', 'rejected_2nd', 'donor_none_2nd', 'label_changed'):
                sw[f] += r['swaps'][f]
            for a, b, n in r['swaps']['routes']: routes[(a, b)] += n
            for c, x, y, z in r['swaps']['by_contract']:
                byc[c][0] += x; byc[c][1] += y; byc[c][2] += z
        summ[k] = dict(n=len(rs), pcc=[r['pcc'] for r in rs], pcc_mean=m('pcc'), carrier=m('carrier'), coop_mass=m('coop_mass'),
                       src_allc=m('src_allc_load'), con_allc=m('con_allc_load'), anti=m('anti_share'), fb_con=m('fb_con_share'),
                       max_con=m('max_con_share'), ps_con=m('ps_con_share'), fb_lab=m('fb_label_share'), max_lab=m('max_label_share'),
                       labelled=m('labelled'),
                       top_contracts=sorted(tops.items(), key=lambda kv: -kv[1])[:5], top_labels=sorted(labs.items(), key=lambda kv: -kv[1])[:5],
                       top_sources=sorted(srcs.items(), key=lambda kv: -kv[1])[:6],
                       con_trans=sorted(((a, b, n) for (a, b), n in trans.items()), key=lambda t: -t[2])[:8], n_con_trans=sum(trans.values()),
                       swaps=dict(sw), routes=sorted(((a, b, n) for (a, b), n in routes.items()), key=lambda t: -t[2])[:8],
                       swap_by_contract=sorted(((c, *v) for c, v in byc.items()), key=lambda t: -(t[1] + t[2] + t[3]))[:6],
                       first_half_cross=[first_cross(r['trace']) for r in rs],
                       frac_coop_samples=[float(np.mean([row[0] > 0.5 for row in r['trace']])) for r in rs],
                       time_s=sum(r['time_s'] for r in rs))
    L = ['# Proof-carrying contracts v1 (finite-size mechanism results)', '',
         'Spec `specs/2026-10-04-proof-carrying-contracts.md`; predictions `predictions/2026-10-04-proof-carrying-contracts.md`. '
         'Code: `src/contracts.py` (alphabet, validity, evaluator, audit), `src/contracts_static.py`, `src/contracts_abm.py`, this report `src/contracts_report.py`. '
         'Raw: `runs/contracts_static.json`, `runs/contracts_grid.json`, `runs/contracts_lottery.json`, `runs/contracts_types.npz`.', '',
         'Swapping is a second operator outside the ε→0 chain, so nothing here is π or a limit; finite-ε runs are approach rates at fixed N.', '']
    # ---------------- static
    L += ['## Static', '',
          '- Language n = 8: %d programs, %d canonical sources, %d free-game classes, free GL stable by world %d.' % (st['programs'], st['canon'], st['classes'], st['worlds_free']),
          '- Truth-table reading (all carriers, synchronous from the GL play): period %d, %d of %d entries divergent. So contracts are read through GL (predictions, semantics 1).' % (
              st['truth_table']['period'], st['truth_table']['divergent'], st['truth_table']['entries']),
          '- Contract alphabet |C| = %d (behavioural classes); %d policy-duplicate groups (same stable row, different columns).' % (st['classes'], len(st['policy_dups'])),
          '- Validity: %d valid (source, contract) pairs; every source is valid for its own signature (%d / %d). Sources by number of valid contracts: %s (index = count).' % (
              st['valid_pairs'], st['own_valid'], st['canon'], st['sources_by_n_valid']),
          '- Types: %d (610 non-carriers + valid carriers). Self-cooperating contracts: %d. Tags (C against exactly one contract, itself): %d.' % (st['types'], st['selfcoop_contracts'], len(st['tags'])), '',
          '### Compatibility (breadth = number of sources valid for the contract; μ = their prior mass)', '',
          '| contract | breadth | μ of valid sources | μ of own class | self-coop | cooperates with (of 471) | valid sources (top by μ) |', '|---|---|---|---|---|---|---|']
    named = ['<BOX(THEM(ME))>', '<C>', '<D>', '<and(BOX1(THEM(ME)),not(BOX(THEM(ME))))>', '<and(BOX(THEM(ME)),BOXD1(THEM(^D)))>', '<BOX1(THEM(ME))>', '<BOX(THEM(THEM))>', '<BOX1(THEM(THEM))>']
    comp = {c['contract']: c for c in st['compatibility']}
    shown = list(dict.fromkeys([c['contract'] for c in st['compatibility'][:6]] + named))
    for c in shown:
        x = comp[c]
        L.append('| `%s` | %d | %.4g | %.4g | %d | %d | %s |' % (c, x['n_valid'], x['mu_valid'], x['mu_own_class'], x['self_coop'], x['n_coop_with'],
                                                                ', '.join('`%s`' % s for s in x['sources'][:5])))
    L += ['', 'Broadest self-cooperating contracts (breadth, μ): ' + '; '.join('`%s` %d (%.3g)' % (a, b, c) for a, b, c in st['breadth_rank_selfcoop'][:10]) + '.', '',
          '### Gate (joint fixed point) and the certified-implication audit', '',
          '| b | rounds | cycle | masked type pairs | masked non-carrier pairs | self-coop non-carrier classes (of %d free) | μ of those | FB / PrudentBot / P* self-coop as non-carriers | contract reads | box true | violations | source reads (legible / masked) | source violations | carrier pairs off-table |' % st['gate']['inf']['n_free_selfcoop'],
          '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for b in ('inf', '4', '2'):
        g = st['gate'][b]; a = g['audit']; sc = g['selfcoop_noncarrier']
        L.append('| %s | %d | %s | %d | %d | %d | %.5f | %d / %d / %d | %d | %d | %d | %d / %d | %d | %d |' % (
            b, g['info']['rounds'], g['info']['cycle'], g['info']['masked'], g['masked_noncarrier_pairs'], g['n_selfcoop_noncarrier'], g['mu_selfcoop_noncarrier'],
            sc['BOX(THEM(ME))'], sc['and(BOX(THEM(ME)),BOXD1(THEM(^D)))'], sc['and(BOX1(THEM(ME)),not(BOX(THEM(ME))))'],
            a['contract_reads'], a['contract_box_true'], a['contract_violations'], a['source_reads_legible'], a['source_reads_masked'], a['source_violations'],
            a['carrier_pairs_off_table']))
    # ---------------- grid
    def row(k, s):
        tag, b, sv, f0, sg, start, N, uni = k
        return '| %s | %d | %g | %g | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            b, sv, f0, sg, start, ', '.join('%.2f' % x for x in s['pcc']), f3(s['pcc_mean']), f3(s['carrier']), f3(s['fb_con']), f3(s['ps_con']), f3(s['max_con']),
            '`%s` %.2f' % s['top_contracts'][0] if s['top_contracts'] else '-', f3(s['fb_lab']), f3(s['max_lab']), f3(s['src_allc']), f3(s['con_allc']), f3(s['anti']))
    hdr = ['| b | s | f₀ | σ | start | P(C,C) per seed | mean | carrier | FB-con share | P*-con share | max con share | top contract | FB-label share | max label share | src-ALLC load | con-ALLC load | anti-prover share |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    L += ['', '## Finite-ε runs, well-mixed, N = 6,400 (ε = 10⁻³ per birth, w = 0.3, 10⁵ generations, second half)', '']
    for start in ('mu', 'alld'):
        L += ['', '### Start: %s' % ('μ seed' if start == 'mu' else 'all-D with f₀ carriers from μ'), ''] + hdr
        for k in sorted([k for k in summ if k[0] == 'grid' and k[5] == start], key=lambda k: (['2', '4', 'inf'].index(k[1]), k[2], k[3], k[4])):
            L.append(row(k, summ[k]))
    L += ['', '### Uniform-donor control (σ = 1, μ seed)', ''] + hdr
    for k in sorted([k for k in summ if k[0] == 'uniform'], key=lambda k: (['2', '4', 'inf'].index(k[1]), k[2], k[3])):
        L.append(row(k, summ[k]))
    L += ['', '### N path (b = 2, s = 0, f₀ = 0.01, μ seed)', '', '| N | σ | P(C,C) per seed | mean | carrier | FB-con share | max con share | first sample with P(C,C) > 0.5 (gen) |', '|---|---|---|---|---|---|---|---|']
    for N in (1600, 6400, 25600):
        for sg in (0.0, 1.0):
            k = ('Npath' if N != 6400 else 'grid', '2', 0, 0.01, sg, 'mu', N, False)
            if k in summ:
                s = summ[k]
                L.append('| %d | %g | %s | %s | %s | %s | %s | %s |' % (N, sg, ', '.join('%.2f' % x for x in s['pcc']), f3(s['pcc_mean']), f3(s['carrier']), f3(s['fb_con']), f3(s['max_con']), s['first_half_cross']))
    # composition / transitions / swaps for σ > 0 cells
    L += ['', '### Composition, transitions and swap routes (μ seed, σ > 0; pooled over seeds)', '',
          '| b | s | f₀ | σ | donors | top contracts (carrier share) | top sources (population share) | dominant-contract transitions (total; top) | swaps accepted / same / rejected / donor-none | top routes (recipient\'s old → copied) |', '|---|---|---|---|---|---|---|---|---|---|']
    for k in sorted([k for k in summ if k[4] > 0 and k[5] == 'mu' and k[6] == 6400], key=lambda k: (k[7], ['2', '4', 'inf'].index(k[1]), k[2], k[3], k[4])):
        s = summ[k]; sw = s['swaps']
        L.append('| %s | %d | %g | %g | %s | %s | %s | %d; %s | %d / %d / %d / %d | %s |' % (
            k[1], k[2], k[3], k[4], 'uniform' if k[7] else 'payoff', '; '.join('`%s` %.2f' % kv for kv in s['top_contracts'][:3]),
            '; '.join('`%s` %.2f' % kv for kv in s['top_sources'][:4]), s['n_con_trans'], '; '.join('%s→%s %d' % t for t in s['con_trans'][:3]),
            sw['accepted'], sw['same'], sw['rejected'], sw['donor_none'], '; '.join('%s→%s %d' % t for t in s['routes'][:3])))
    # ---------------- lottery
    if lot:
        lc = defaultdict(list)
        for r in lot:
            lc[(r['N'], r['I'], r['b'], r['f0'], r['sigma'])].append(r)
        L += ['', '## ε = 0 seeding lottery (iid μ seeding, complete island graph, mN = 1; efficient = final P(C,C) ≥ 0.95)', '',
              '| (N, I) | b | f₀ | σ | runs | efficient | 95% Wilson | defecting | other | unresolved / metastable | median stop gen |', '|---|---|---|---|---|---|---|---|---|---|---|']
        lsum = {}
        for k in sorted(lc, key=lambda k: (k[1], k[0], ['inf', '2'].index(k[2]), k[3], k[4])):
            rs = lc[k]; n = len(rs)
            e = sum(r['outcome'] == 'efficient' for r in rs); dd = sum(r['outcome'] == 'defecting' for r in rs)
            un = sum(r['status'] in ('unresolved', 'metastable') for r in rs)
            lo, hi = wilson(e, n)
            lsum['%d,%d,%s,%g,%g' % k] = dict(n=n, eff=e, lo=lo, hi=hi, frac=e / n)
            L.append('| (%d, %d) | %s | %g | %g | %d | %.2f | [%.2f, %.2f] | %d | %d | %d | %d |' % (k[0], k[1], k[2], k[3], k[4], n, e / n, lo, hi, dd, n - e - dd - un, un,
                                                                                           int(np.median([r['stop_gen'] for r in rs]))))
    else:
        lsum = {}
    # ---------------- supplementary b = 0
    supp = load('contracts_supp.json'); slot = load('contracts_supplottery.json')
    ssum = {}
    if supp:
        sc = defaultdict(list)
        for r in supp: sc[(r['s'], r['f0'], r['sigma'])].append(r)
        L += ['', '## Supplementary b = 0 arm (only constants legible from source; μ seed, N = 6,400; not in the spec)', '',
              '| s | f₀ | σ | P(C,C) per seed | mean | carrier | FB-con share | max con share | top contract | top sources |', '|---|---|---|---|---|---|---|---|---|---|']
        for k in sorted(sc):
            rs = sc[k]
            m = lambda f: float(np.mean([r[f] for r in rs]))
            tops = defaultdict(float); srcs = defaultdict(float)
            for r in rs:
                for c, v in r['top_contracts']: tops[c] += v / len(rs)
                for c, v in r['top_sources']: srcs[c] += v / len(rs)
            tc = sorted(tops.items(), key=lambda kv: -kv[1]); ts = sorted(srcs.items(), key=lambda kv: -kv[1])
            ssum[k] = dict(pcc=[r['pcc'] for r in rs], pcc_mean=m('pcc'), carrier=m('carrier'), fb_con=m('fb_con_share'), max_con=m('max_con_share'))
            L.append('| %d | %g | %g | %s | %s | %s | %s | %s | %s | %s |' % (k[0], k[1], k[2], ', '.join('%.2f' % r['pcc'] for r in rs), f3(m('pcc')), f3(m('carrier')),
                     f3(m('fb_con_share')), f3(m('max_con_share')), '`%s` %.2f' % tc[0] if tc else '-', '; '.join('`%s` %.2f' % kv for kv in ts[:3])))
    if slot:
        lc = defaultdict(list)
        for r in slot: lc[(r['N'], r['I'], r['f0'], r['sigma'])].append(r)
        L += ['', '### Supplementary lottery at b = 0', '', '| (N, I) | f₀ | σ | runs | efficient | 95% Wilson | unresolved |', '|---|---|---|---|---|---|---|']
        for k in sorted(lc, key=lambda k: (k[1], k[0], k[2], k[3])):
            rs = lc[k]; n = len(rs); e = sum(r['outcome'] == 'efficient' for r in rs); lo, hi = wilson(e, n)
            lsum['%d,%d,0,%g,%g' % (k[0], k[1], k[2], k[3])] = dict(n=n, eff=e, lo=lo, hi=hi, frac=e / n)
            L.append('| (%d, %d) | %g | %g | %d | %.2f | [%.2f, %.2f] | %d |' % (k[0], k[1], k[2], k[3], n, e / n, lo, hi, sum(r['status'] in ('unresolved', 'metastable') for r in rs)))
    L += verdicts(summ, lsum, ssum)
    open(os.path.join(RUNS, 'proof-carrying-contracts.md'), 'w').write('\n'.join(L) + '\n')
    js = dict(static={k: v for k, v in st.items() if k not in ('names', 'cname', 'compatibility')}, compatibility_top=st['compatibility'][:40],
              cells={'|'.join(map(str, k)): v for k, v in summ.items()}, lottery=lsum)
    json.dump(js, open(os.path.join(RUNS, 'proof-carrying-contracts.json'), 'w'), indent=1)
    print('\n'.join(L))


if __name__ == '__main__':
    main()
