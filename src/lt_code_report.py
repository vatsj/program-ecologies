"""Tables for runs/prover-as-code.md and runs/prover-as-code.json from runs/prover_as_code/*.json."""
import glob, json, os, sys
from collections import Counter, defaultdict

D = os.path.join(os.path.dirname(__file__), '..', 'runs', 'prover_as_code')
KS = [10 ** 5, 10 ** 6, 10 ** 7]
BS = [8, 12, 16, 24, 32, 64]
PROGS = ['C', 'D', 'FB', 'FB1', 'PB', 'G', 'P*', 'SF', 'SC', 'Vlet', 'Vwrap', 'FB2', 'FBx']
READERS = ['FB', 'FB1', 'PB', 'Vlet', 'Vwrap', 'FB2', 'FBx']
KN = {10 ** 5: '1e5', 10 ** 6: '1e6', 10 ** 7: '1e7'}


def load(name):
    p = os.path.join(D, name)
    if not os.path.exists(p): return None
    return json.load(open(p))


def ab(play): return {'C': 'C', 'D': 'D', 'BOT': '⊥'}[play]


def outs(searches):
    return ''.join({'found': 'f', 'refuted': 'r', 'interrupted': 'i', 'cut': 'x'}[s['outcome']] for s in searches
                   if s.get('depth', 0) == 0)


def main_tables(mode):
    lines = []
    summ = {}
    for K in KS:
        for b in BS:
            r = load('main_%d_%d_%d.json' % (K, b, mode))
            if r is None: continue
            summ[(K, b)] = r
    if not summ: return lines, summ
    # mutual cooperation table per (K, b): list of unordered pairs with (C, C)
    lines.append('| K | b | mutual (C, C) pairs (unordered, excluding pairs with C) | exploitation of a sound reader (reader C, other not C) | program-level searches: found / refuted / interrupted / cut |')
    lines.append('|---|---|---|---|---|')
    for (K, b), r in sorted(summ.items()):
        cells = r['cells']
        cc = []
        for i, x in enumerate(PROGS):
            for y in PROGS[i:]:
                if 'C' in (x, y): continue
                a, b_ = cells['%s|%s' % (x, y)]['play'], cells['%s|%s' % (y, x)]['play']
                if a == 'C' and b_ == 'C': cc.append('%s–%s' % (x, y))
        ex = []
        for x in READERS + ['G', 'P*']:
            for y in PROGS:
                a, b_ = cells['%s|%s' % (x, y)]['play'], cells['%s|%s' % (y, x)]['play']
                if a == 'C' and b_ != 'C' and x in READERS: ex.append('%s by %s' % (x, y))
        cnt = Counter()
        for c in cells.values():
            for s in c['searches']:
                if s.get('depth', 0) == 0: cnt[s['outcome']] += 1
        lines.append('| %s | %d | %s | %s | %d / %d / %d / %d |' % (KN[K], b, ', '.join(cc) or '—', ', '.join(ex) or '—',
                     cnt['found'], cnt['refuted'], cnt['interrupted'], cnt['cut']))
    return lines, summ


def matrix(r):
    cells = r['cells']
    out = ['| row plays vs column | ' + ' | '.join(PROGS) + ' |', '|---' * (len(PROGS) + 1) + '|']
    for x in PROGS:
        row = []
        for y in PROGS:
            c = cells['%s|%s' % (x, y)]
            o = outs(c['searches'])
            row.append(ab(c['play']) + ('<sub>%s</sub>' % o if o else ''))
        out.append('| **%s** | %s |' % (x, ' | '.join(row)))
    return out


def plateau(summ):
    """Per (pair, b): the smallest tested K from which the play is constant at every larger tested K."""
    res = Counter(); per = {}
    for b in BS:
        for x in PROGS:
            for y in PROGS:
                seq = []
                for K in KS:
                    r = summ.get((K, b))
                    if r is None: break
                    seq.append(r['cells']['%s|%s' % (x, y)]['play'])
                if len(seq) < len(KS): continue
                k0 = len(seq) - 1
                while k0 > 0 and seq[k0 - 1] == seq[-1]: k0 -= 1
                res[KN[KS[k0]]] += 1
                per['%s|%s|%d' % (x, y, b)] = (KN[KS[k0]], seq)
    return res, per


def harness_summary(files):
    tot = Counter(); bad = []
    by_prog = defaultdict(Counter)
    for f in files:
        r = load(f)
        if r is None: continue
        for q in r.get('queries', []):
            tot['queries'] += 1
            tot[q['outcome']] += 1
            if q['outcome'] in ('found', 'refuted'):
                tot['finishing'] += 1
                if q.get('outcome_agree'): tot['outcome_agree'] += 1
                else: bad.append((f, q))
                if q.get('work_agree'): tot['work_agree'] += 1
                if q['outcome'] == 'found':
                    tot['found_checked'] += 1
                    if q.get('replay_ok'): tot['replay_ok'] += 1
                    else: bad.append((f, q))
                    if q.get('same_tree'): tot['same_tree'] += 1
                    if q.get('check_term') == 'T': tot['check_term_ok'] += 1
                    tot['replay_nodes'] += q.get('replay_nodes', 0)
    return tot, bad


def main():
    md = []
    js = {}
    # benchmarks
    bench = load('bench_.json')
    if bench:
        md.append('## 1. Benchmarks: search vs checking a supplied witness (K = 10⁷, U = 2.5·10⁶)\n')
        md.append('| program | b | result | search steps | expansions | rule instances | closure | witness size | check steps | check steps/node | rules |')
        md.append('|---|---|---|---|---|---|---|---|---|---|---|')
        for k, v in bench['cells'].items():
            x, b = k.split('|')
            md.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                x, b, v['result'], v['search_steps'], v.get('expansions', ''), v.get('instances', ''),
                v.get('closure', ''), v.get('size', ''), v.get('check_steps', ''), v.get('check_steps_per_node', ''),
                ' '.join(v.get('rules', []))))
        js['bench'] = bench['cells']
    th = {K: load('thresholds_%d.json' % K) for K in KS}
    if any(th.values()):
        md.append('\n## 2. Thresholds on b = 2..20 (copies and selected pairs)\n')
        md.append('Entry: first b with (C, C) for the pair (both orders), "—" if none ≤ 20.\n')
        md.append('| pair | ' + ' | '.join('K = %s' % KN[K] for K in KS) + ' |')
        md.append('|---' * 4 + '|')
        pairs = [(x, x) for x in ['FB', 'FB1', 'PB', 'G', 'P*', 'SC', 'Vlet', 'Vwrap', 'FB2', 'FBx']] + \
                [('FB', 'SF'), ('FB', 'FB1'), ('FB', 'PB'), ('FB', 'Vlet'), ('FB', 'Vwrap')]
        jt = {}
        for x, y in pairs:
            row = []
            for K in KS:
                t = th[K]
                if t is None: row.append('n/a'); continue
                first = None
                for b in range(2, 21):
                    a = t['cells'].get('%s|%s|%d' % (x, y, b)); c = t['cells'].get('%s|%s|%d' % (y, x, b))
                    if a and c and a['play'] == 'C' and c['play'] == 'C': first = b; break
                row.append(str(first) if first else '—')
                jt['%s|%s|%d' % (x, y, K)] = first
            md.append('| %s–%s | %s |' % (x, y, ' | '.join(row)))
        js['thresholds'] = jt
    for mode, title in ((0, 'Main catalogue'), (2, 'JLöb-disabled control (CORE_2)')):
        lines, summ = main_tables(mode)
        if not lines: continue
        md.append('\n## %s %s: every (K, b)\n' % ('3.' if mode == 0 else '6.', title))
        md += lines
        if (10 ** 7, 16) in summ:
            md.append('\nPlay matrix at K = 10⁷, b = 16 (row\'s play against column; subscript: the row\'s program-level '
                      'searches, f found, r refuted, i interrupted by the cap, x cut by an outer counter):\n')
            md += matrix(summ[(10 ** 7, 16)])
        if (10 ** 7, 8) in summ and mode == 0:
            md.append('\nPlay matrix at K = 10⁷, b = 8:\n')
            md += matrix(summ[(10 ** 7, 8)])
        pl, per = plateau(summ)
        md.append('\nFinite-K plateau (smallest tested K from which an ordered cell is constant at every larger tested K; '
                  'a plateau, not stabilization): ' + ', '.join('%s: %d' % (k, v) for k, v in sorted(pl.items())))
        js['main_%d' % mode] = {'%d|%d' % k: {c: v['play'] for c, v in r['cells'].items()} for k, r in summ.items()}
        js['plateau_%d' % mode] = per
        # coverage per program and budget
        md.append('\nCoverage of program-level searches by searching program (all K, b):\n')
        md.append('| program | found | refuted | interrupted | cut |')
        md.append('|---|---|---|---|---|')
        cov = defaultdict(Counter)
        for (K, b), r in summ.items():
            for c, v in r['cells'].items():
                x = c.split('|')[0]
                for s in v['searches']:
                    if s.get('depth', 0) == 0: cov[x][s['outcome']] += 1
        for x in PROGS:
            if cov[x]:
                md.append('| %s | %d | %d | %d | %d |' % (x, cov[x]['found'], cov[x]['refuted'], cov[x]['interrupted'], cov[x]['cut']))
        md.append('\nCoverage by (K, b):\n')
        md.append('| K | b | found | refuted | interrupted | cut |')
        md.append('|---|---|---|---|---|---|')
        for (K, b), r in sorted(summ.items()):
            cnt = Counter(s['outcome'] for v in r['cells'].values() for s in v['searches'] if s.get('depth', 0) == 0)
            md.append('| %s | %d | %d | %d | %d | %d |' % (KN[K], b, cnt['found'], cnt['refuted'], cnt['interrupted'], cnt['cut']))
    grid = {K: load('grid_%d.json' % K) for K in KS}
    if any(grid.values()):
        md.append('\n## 4. FairBot distinct-budget grid {8, 12, 16, 32}² (row\'s play / column\'s play, row\'s search outcome)\n')
        for K in KS:
            g = grid[K]
            if g is None: continue
            md.append('\nK = %s:\n' % KN[K])
            md.append('| b_row \\ b_col | 8 | 12 | 16 | 32 |')
            md.append('|---|---|---|---|---|')
            for x in (8, 12, 16, 32):
                row = []
                for y in (8, 12, 16, 32):
                    c1 = g['cells']['%d|%d' % (x, y)]; c2 = g['cells']['%d|%d' % (y, x)]
                    row.append('%s/%s %s' % (ab(c1['play']), ab(c2['play']), outs(c1['searches'])))
                md.append('| %d | %s |' % (x, ' | '.join(row)))
        js['grid'] = {K: {c: v['play'] for c, v in g['cells'].items()} for K, g in grid.items() if g}
    leak = {(K, b): load('leak_%d_%d.json' % (K, b)) for K in KS for b in BS}
    if any(leak.values()):
        md.append('\n## 5. Leak cells: SF_k against every reader\n')
        md.append('Entry per (K, b, k): readers with (reader play / SF play); "matched" = the reader\'s certified target names the fuel SF ran with. Exploitation = reader C, SF not C.\n')
        md.append('| K | b | k | reader/SF plays | matched exploited | mismatched exploited |')
        md.append('|---|---|---|---|---|---|')
        jl = {}
        tot = Counter()
        for (K, b), r in sorted(leak.items()):
            if r is None: continue
            byk = defaultdict(list)
            for name, c in r['cells'].items():
                byk[c['k']].append(c)
                tot['matched' if c['matched'] else 'mismatched'] += 1
                if c['exploited']: tot['exploit_' + ('matched' if c['matched'] else 'mismatched')] += 1
                if c['reader_play'] == 'C' and c['matched']: tot['matched_reader_C'] += 1
                if c['reader_play'] == 'C' and not c['matched']: tot['mismatched_reader_C'] += 1
            for k in sorted(byk):
                cs = byk[k]
                plays = ', '.join('%s %s/%s' % (c['reader'], ab(c['reader_play']), ab(c['sf_play'])) for c in cs)
                em = [c['reader'] for c in cs if c['exploited'] and c['matched']]
                en = [c['reader'] for c in cs if c['exploited'] and not c['matched']]
                kl = ('U%+d' % (k - r['U'])) if abs(k - r['U']) < 100 else str(k)
                md.append('| %s | %d | %s | %s | %s | %s |' % (KN[K], b, kl, plays, ', '.join(em) or '—', ', '.join(en) or '—'))
            jl['%d|%d' % (K, b)] = {n: {kk: c[kk] for kk in ('k', 'reader', 'reader_play', 'sf_play', 'matched', 'exploited', 'target_fuel')}
                                    for n, c in r['cells'].items()}
        md.append('\nTotals: ' + ', '.join('%s %d' % kv for kv in sorted(tot.items())))
        js['leak'] = jl; js['leak_totals'] = dict(tot)
    bd = load('boundary_.json')
    if bd:
        md.append('\n## 7. Fuel-boundary cells\n')
        for k, v in bd['cells'].items():
            md.append('- **%s**: %s' % (k, json.dumps(v)))
        js['boundary'] = bd['cells']
    files = [os.path.basename(f) for f in glob.glob(os.path.join(D, '*.json'))]
    tot, bad = harness_summary(files)
    md.append('\n## 8. Correctness harness (every core query of every task)\n')
    md.append(', '.join('%s %d' % kv for kv in sorted(tot.items())))
    md.append('\nMismatches: %d' % len(bad))
    for f, q in bad[:20]:
        md.append('- %s: %s' % (f, json.dumps(q)[:400]))
    js['harness'] = dict(tot); js['harness_mismatches'] = len(bad)
    print('\n'.join(md))
    with open(os.path.join(D, '..', 'prover-as-code.json'), 'w') as f:
        json.dump(js, f, default=str, indent=0)


if __name__ == '__main__':
    main()
