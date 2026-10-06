"""Tables for runs/realizable-language.md from runs/realizable_language/*.json (src/lt_run.py)."""
import os, sys, json, glob
from collections import Counter, defaultdict

D = sys.argv[1] if len(sys.argv) > 1 else 'runs/realizable_language'
KS = [10 ** 4, 10 ** 5, 10 ** 6]
NAMES = ['C', 'D', 'FB', 'FB1', 'PB', 'G', 'P*', 'SF', 'SC', 'Vlet', 'Vwrap']
SOUND = ['FB', 'FB1', 'PB', 'Vlet', 'Vwrap']          # readers whose cooperation is backed by a sound box
COND = [n for n in NAMES if n not in ('C', 'D')]


def load(pat):
    out = {}
    for f in sorted(glob.glob(os.path.join(D, pat))):
        d = json.load(open(f))
        if 'error' in d:
            print('ERROR in', f, d['error'][-500:], file=sys.stderr); continue
        out[f] = d
    return out


mains = {d['b']: d for d in load('main_*.json').values()}
B = sorted(mains)
out = []
J = {'b_values': B}
P = out.append


def play(b, x, y, sem='prim'):
    return mains[b]['cells'][x + '|' + y][sem]['play']


def mutual(b, x, y, sem='prim'):
    return play(b, x, y, sem) == 'C' and play(b, y, x, sem) == 'C'


def first_run(pred):
    """(first b with pred, monotone: pred holds at every b >= first)."""
    bs = [b for b in B if pred(b)]
    if not bs: return None, None
    f = bs[0]
    return f, all(pred(b) for b in B if b >= f)


# ---------------------------------------------------------------- thresholds
P('## 1. Self-cooperation thresholds (primitive-assisted)\n')
P('b\\* = first b ∈ {%d..%d} with (C, C) against a copy; "stable" = (C, C) at every larger b on the grid. Certified '
  'minimal size and Λ of the self-play formula at b\\*; W = search work at b\\*.\n' % (B[0], B[-1]))
P('| program | b\\* | stable | minimal size at b\\* | Λ | W at b\\* | certified lower bound if none |')
P('|---|---|---|---|---|---|---|')
J['thresholds'] = {}
for x in NAMES:
    f, mono = first_run(lambda b: mutual(b, x, x))
    row = {'b_star': f, 'stable': mono}
    size = lam = W = '—'
    if f is not None:
        pr = mains[f]['cells'][x + '|' + x]['prim']['proves']
        if pr:
            key = '%s@%d' % (pr[0][0], pr[0][1])
            fm = mains[f]['formulas'].get(key)
            if fm: size, lam, W = fm['size'], fm.get('lam'), fm['W']
    row.update({'size': size, 'lam': lam, 'W': W})
    J['thresholds'][x] = row
    lb = ('> %d (refuted at every b ≤ %d)' % (B[-1], B[-1])) if f is None and x not in ('D',) else ''
    P('| %s | %s | %s | %s | %s | %s | %s |' % (x, f if f is not None else 'none ≤ %d' % B[-1], mono if mono is not None else '—',
                                          size, lam, W, lb))

# ---------------------------------------------------------------- pairwise first mutual cooperation
P('\n## 2. First b of mutual cooperation, every unordered pair (primitive-assisted)\n')
P('Entry: first b with (C, C), "s" if stable above it; "—" none on the grid.\n')
P('| | ' + ' | '.join(NAMES) + ' |')
P('|---' * (len(NAMES) + 1) + '|')
J['first_mutual'] = {}
for x in NAMES:
    row = []
    for y in NAMES:
        f, mono = first_run(lambda b: mutual(b, x, y))
        J['first_mutual'][x + '|' + y] = [f, mono]
        row.append('—' if f is None else ('%d%s' % (f, 's' if mono else '')))
    P('| %s | %s |' % (x, ' | '.join(row)))

# ---------------------------------------------------------------- outcome matrices
for b in [b for b in (8, 16, 25, 32, 64) if b in mains]:
    P('\n### Play of the row program against the column program at b = %d (primitive-assisted; ⊥ = timeout/other)\n' % b)
    P('| row \\ col | ' + ' | '.join(NAMES) + ' |')
    P('|---' * (len(NAMES) + 1) + '|')
    for x in NAMES:
        P('| %s | %s |' % (x, ' | '.join(play(b, x, y).replace('BOT', '⊥') for y in NAMES)))

# ---------------------------------------------------------------- minimal sizes at the top budget
bt = B[-1]
P('\n### Certified minimal derivation size (Λ) of each found box of the row program against the column program, b = %d\n' % bt)
P('Entry per prove call in order (PB and P\\* make two); "r" refuted; empty: no prove call.\n')
P('| row \\ col | ' + ' | '.join(NAMES) + ' |')
P('|---' * (len(NAMES) + 1) + '|')
J['sizes_top'] = {}
for x in NAMES:
    row = []
    for y in NAMES:
        ent = []
        for p in mains[bt]['cells'][x + '|' + y]['prim']['proves']:
            fm = mains[bt]['formulas'].get('%s@%d' % (p[0], p[1]))
            if p[2] == 'found' and fm: ent.append('%d(%s)' % (fm['size'], fm.get('lam')))
            else: ent.append('r' if p[2] == 'refuted' else p[2])
        J['sizes_top'][x + '|' + y] = ent
        row.append(' / '.join(ent))
    P('| %s | %s |' % (x, ' | '.join(row)))

# ---------------------------------------------------------------- exploitation
P('\n## 3. Exploitation cells: the row program plays C, the column program plays D or ⊥\n')
J['exploitation'] = {}
for sem in ['prim'] + ['search_%d' % K for K in KS]:
    cnt = Counter(); ex = []
    for b in B:
        for x in NAMES:
            for y in NAMES:
                a, c = play(b, x, y, sem), play(b, y, x, sem)
                if a == 'C' and c in ('D', 'BOT'):
                    cnt[(x, y, c)] += 1
                    ex.append((b, x, y, c))
    J['exploitation'][sem] = [list(e) for e in ex]
    P('**%s:** ' % sem + (', '.join('%s exploited by %s (%s) at %d b' % (x, y, c.replace('BOT', '⊥'), n)
                                     for (x, y, c), n in sorted(cnt.items())) or 'none') + '.\n')
P('Sound readers (%s) on the C side under primitive-assisted charging: %d cells.\n' %
  (', '.join(SOUND), sum(1 for e in J['exploitation']['prim'] if e[1] in SOUND)))

# ---------------------------------------------------------------- trichotomy
P('\n## 4. Prove outcomes: found / refuted / timeout (every prove call of every cell, all b)\n')
P('| semantics | found | refuted | timeout | of which inside a sim | plays ⊥ |')
P('|---|---|---|---|---|---|')
J['trichotomy'] = {}
for sem in ['prim'] + ['search_%d' % K for K in KS] + ['ctrl_prim'] + ['ctrl_search_%d' % K for K in KS]:
    c = Counter(); insim = 0; bot = 0
    for b in B:
        for k, v in mains[b]['cells'].items():
            e = v[sem]
            if e['play'] == 'BOT': bot += 1
            for p in e['proves']:
                c[p[2]] += 1
                if p[2] == 'timeout' and p[4]: insim += 1
    J['trichotomy'][sem] = {'found': c['found'], 'refuted': c['refuted'], 'timeout': c['timeout'], 'timeout_in_sim': insim,
                            'bot_plays': bot}
    P('| %s | %d | %d | %d | %d | %d |' % (sem, c['found'], c['refuted'], c['timeout'], insim, bot))

# ---------------------------------------------------------------- search work and stabilization
P('\n## 5. Search work W and the K at which outcomes stabilize (search-charged)\n')
Wf = []; Wr = []
for b in B:
    for key, fm in mains[b]['formulas'].items():
        (Wf if fm['found'] else Wr).append((fm['W'], b, key))
Wf.sort(); Wr.sort()
J['W_found_max'] = Wf[-1][:2] if Wf else None
J['W_refuted_max'] = Wr[-1][:2] if Wr else None
P('Distinct prove queries: %d found, %d refuted. Max W of a found box: %s (b = %s, `%s`). Max W of a refutation: %s '
  '(b = %s, `%s`). Found boxes with W > 10⁴ / 10⁵ / 10⁶: %d / %d / %d. Refutations with W > 10⁴ / 10⁵ / 10⁶: %d / %d / %d.\n'
  % (len(Wf), len(Wr), Wf[-1][0], Wf[-1][1], Wf[-1][2], Wr[-1][0], Wr[-1][1], Wr[-1][2],
     sum(w > 1e4 for w, _, _ in Wf), sum(w > 1e5 for w, _, _ in Wf), sum(w > 1e6 for w, _, _ in Wf),
     sum(w > 1e4 for w, _, _ in Wr), sum(w > 1e5 for w, _, _ in Wr), sum(w > 1e6 for w, _, _ in Wr)))
P('| W band | found | refuted |')
P('|---|---|---|')
for lo, hi in [(0, 1e2), (1e2, 1e3), (1e3, 1e4), (1e4, 1e5), (1e5, 1e6), (1e6, 1e9)]:
    P('| [%g, %g) | %d | %d |' % (lo, hi, sum(lo <= w < hi for w, _, _ in Wf), sum(lo <= w < hi for w, _, _ in Wr)))
# stabilization per cell
stab = Counter(); agree = Counter()
for b in B:
    for k, v in mains[b]['cells'].items():
        fin = v['search_%d' % KS[-1]]['play']
        s = next(K for K in KS if all(v['search_%d' % K2]['play'] == fin for K2 in KS if K2 >= K))
        stab[s] += 1
        agree[fin == v['prim']['play']] += 1
J['stabilization'] = {str(k): v for k, v in stab.items()}
J['search_1e6_equals_prim'] = agree[True]; J['search_1e6_differs_prim'] = agree[False]
P('\nCells (all b, %d) by the smallest tested K from which the search-charged play no longer changes: %s. At K = 10⁶ '
  'the search-charged play equals the primitive-assisted play in %d cells and differs in %d.\n' %
  (sum(stab.values()), ', '.join('K = %g: %d' % (k, stab[k]) for k in KS), agree[True], agree[False]))
diff = Counter()
for b in B:
    for k, v in mains[b]['cells'].items():
        if v['search_%d' % KS[-1]]['play'] != v['prim']['play']:
            diff[(k, v['prim']['play'], v['search_%d' % KS[-1]]['play'])] += 1
P('Cells differing at K = 10⁶ (pair, prim → search, number of b): ' +
  (', '.join('%s %s→%s (%d)' % (k, a, c.replace('BOT', '⊥'), n) for (k, a, c), n in sorted(diff.items())) or 'none') + '.\n')
J['differ_1e6'] = [[k, a, c, n] for (k, a, c), n in sorted(diff.items())]

# self-cooperation under search-charged per K
P('\n### Self-cooperation thresholds under search-charged charging\n')
P('| program | ' + ' | '.join('b\\* at K = %g' % K for K in KS) + ' |')
P('|---' * (len(KS) + 1) + '|')
J['thresholds_search'] = {}
for x in NAMES:
    row = []
    for K in KS:
        f, mono = first_run(lambda b: mutual(b, x, x, 'search_%d' % K))
        row.append('none' if f is None else '%d%s' % (f, '' if mono else ' (not stable)'))
        J['thresholds_search'].setdefault(x, {})[str(K)] = [f, mono]
    P('| %s | %s |' % (x, ' | '.join(row)))

# ---------------------------------------------------------------- control
P('\n## 6. JLöb-disabled control K_T⁻ (every cell recomputed)\n')
cc = Counter(); J['control_mutual'] = []
for b in B:
    for x in NAMES:
        for y in NAMES:
            if x < y or x == y:
                if mutual(b, x, y, 'ctrl_prim'):
                    cc[(x, y)] += 1
for (x, y), n in sorted(cc.items()):
    J['control_mutual'].append([x, y, n])
P('Mutual cooperation cells (unordered pairs, number of b): ' + ', '.join('%s–%s (%d)' % (x, y, n) for (x, y), n in sorted(cc.items())) + '.\n')
lob = [(x, y, n) for (x, y), n in sorted(cc.items()) if x not in ('C', 'SC') and y not in ('C', 'SC')]
P('Mutual cooperation between two programs both outside {C, SC}: %s.\n' % (', '.join('%s–%s (%d)' % t for t in lob) or 'none'))
J['control_lobian'] = lob
cg = Counter()
for b in B:
    for x in NAMES:
        for y in NAMES:
            if play(b, x, y, 'ctrl_prim') != play(b, x, y):
                cg[(x, y, play(b, x, y), play(b, x, y, 'ctrl_prim'))] += 1
P('Cells where the control changes the primitive-assisted play (row vs column, full → control, number of b): ' +
  ', '.join('%s vs %s %s→%s (%d)' % (x, y, a, c, n) for (x, y, a, c), n in sorted(cg.items())) + '.\n')

# ---------------------------------------------------------------- audits
P('\n## 7. Audits\n')
tot = Counter()
for b in B:
    a = mains[b]['audit']; ca = mains[b]['ctrl_audit']
    tot['boxes'] += a['boxes_checked'] + ca['boxes_checked']; tot['seqs'] += a['sequents_checked'] + ca['sequents_checked']
    tot['viol'] += len(a['violations']) + len(ca['violations'])
    tot['rep'] += a['witnesses_replayed'] + ca['witnesses_replayed']; tot['repnodes'] += a['replay_nodes'] + ca['replay_nodes']
    tot['repsteps'] += a['replay_steps'] + ca['replay_steps']; tot['repjlob'] += a['replay_jlob']
    tot['repfail'] += len(a['replay_failures']) + len(ca['replay_failures'])
    tot['trace'] += mains[b]['trace_steps_checked']; tot['tracebad'] += mains[b]['trace_disagreements']
    for key, fm in list(mains[b]['formulas'].items()) + list(mains[b]['ctrl_formulas'].items()):
        tot['merges'] = max(tot['merges'], fm['merges']); tot['incomplete'] += (not fm['complete'])
        tot['closure_max'] = max(tot['closure_max'], fm['closure'])
aux = load('grid_*.json'); aux.update(load('sweep_*.json'))
for f, d in aux.items():
    a = d['audit']
    tot['boxes'] += a['boxes_checked']; tot['seqs'] += a['sequents_checked']; tot['viol'] += len(a['violations'])
    tot['rep'] += a['witnesses_replayed']; tot['repnodes'] += a['replay_nodes']; tot['repsteps'] += a['replay_steps']
    tot['repfail'] += len(a['replay_failures'])
    tot['trace'] += d['trace_steps_checked']; tot['tracebad'] += d['trace_disagreements']
J['audit'] = dict(tot)
P('- Soundness checker: %d found boxes and %d witness sequents evaluated in the standard model (full calculus and control); '
  '**%d violations**.' % (tot['boxes'], tot['seqs'], tot['viol']))
P('- Independent replay (`src/lt_check.py`): %d witnesses, %d nodes, %d evaluation steps re-derived by the independent '
  'evaluator, %d JLöb instances; **%d failures**.' % (tot['rep'], tot['repnodes'], tot['repsteps'], tot['repjlob'], tot['repfail']))
P('- Independent evaluator on every play trace (both charging semantics, every K, full calculus and control under '
  'primitive-assisted): %d steps; **%d disagreements**.' % (tot['trace'], tot['tracebad']))
P('- Merges (states with two deterministic predecessors) in any root closure: max %d (allowed by Lemma U, notes §1.7 as amended). Largest root '
  'closure %d formulas. Searches stopped by the work limit 5·10⁷: %d.' % (tot['merges'], tot['closure_max'], tot['incomplete']))
br = load('brute_*.json')
nb = sum(len(d['rows']) for d in br.values()); ab = sum(r['agree'] for d in br.values() for r in d['rows'])
nc = sum(len(d['ctrl_rows']) for d in br.values()); ac = sum(r['agree'] for d in br.values() for r in d['ctrl_rows'])
J['brute'] = {'b': sorted(d['b'] for d in br.values()), 'rows': nb, 'agree': ab, 'ctrl_rows': nc, 'ctrl_agree': ac}
P('- Independent brute-force prover (no lower bounds; members = whole closure) at b ∈ %s: %d / %d prove queries agree on '
  'found/refuted and the minimal size; control %d / %d.' % (sorted(d['b'] for d in br.values()), ab, nb, ac, nc))
mf = load('memfull_*.json')
nm = sum(len(d['rows']) for d in mf.values()); am = sum(r['agree'] for d in mf.values() for r in d['rows'])
J['memfull'] = {'b': sorted(d['b'] for d in mf.values()), 'rows': nm, 'agree': am}
P('- Mem enlarged to every atom and box content of the root closure, b ∈ %s: %d / %d prove queries agree.' %
  (sorted(d['b'] for d in mf.values()), am, nm))

# ---------------------------------------------------------------- grid
g = load('grid_*.json')
if g:
    d = list(g.values())[0]
    P('\n## 8. FairBot budgets: copies vs distinct budgets\n')
    P('Primitive-assisted, then search-charged at K = 10⁴ / 10⁵ / 10⁶ (row FB_x, column FB_y; the row\'s play):\n')
    P('| x \\ y | 4 | 8 | 16 | 32 |')
    P('|---|---|---|---|---|')
    for x in (4, 8, 16, 32):
        row = []
        for y in (4, 8, 16, 32):
            e = d['small']['%d|%d' % (x, y)]
            row.append(('%s / %s' % (e['prim']['play'], ' '.join(e['search_%d' % K]['play'] for K in KS))).replace('BOT', '⊥'))
        P('| %d | %s |' % (x, ' | '.join(row)))
    full = d['full']
    viol = []; asym = []
    for x in range(2, 41):
        for y in range(2, 41):
            want = 'C' if ((x == y and x >= 8) or (x != y and min(x, y) >= 12)) else 'D'
            if full['%d|%d' % (x, y)] != want: viol.append((x, y, full['%d|%d' % (x, y)]))
            if full['%d|%d' % (x, y)] != full['%d|%d' % (y, x)]: asym.append((x, y))
    J['grid_full_violations'] = viol; J['grid_full_asym'] = asym
    P('\nFull grid {2..40}², primitive-assisted: cells violating "C iff (x = y ≥ 8) or (x ≠ y and min(x, y) ≥ 12)": %d; '
      'asymmetric cells: %d.\n' % (len(viol), len(asym)))
    small_ex = []
    for k, e in d['small'].items():
        x, y = k.split('|')
        for sem in ['prim'] + ['search_%d' % K for K in KS]:
            a = e[sem]['play']; c = d['small']['%s|%s' % (y, x)][sem]['play']
            if a == 'C' and c != 'C': small_ex.append((x, y, sem, c))
    J['grid_exploitation'] = small_ex
    P('(C, not-C) cells on the {4, 8, 16, 32}² grid: %s.\n' % (small_ex or 'none'))

# ---------------------------------------------------------------- SF sweep
s = load('sweep_*.json')
if s:
    d = list(s.values())[0]
    P('\n## 9. Simulation FairBot: k sweep\n')
    P('Row program\'s play: primitive-assisted / search-charged at K = 10⁴, 10⁵, 10⁶ (prove outcomes f/r/t).\n')
    pairs = list(next(iter(d['cells'].values())).keys())
    P('| k | ' + ' | '.join(pairs) + ' |')
    P('|---' * (len(pairs) + 1) + '|')
    J['sweep'] = {}
    for k, v in d['cells'].items():
        row = []
        for pnm in pairs:
            e = v[pnm]
            def f(x): return x['play'].replace('BOT', '⊥') + (':' + ''.join(p[2][0] for p in x['proves']) if x['proves'] else '')
            row.append('%s / %s' % (f(e['prim']), ' '.join(f(e['search_%d' % K]) for K in KS)))
            J['sweep']['%s|%s' % (k, pnm)] = row[-1]
        P('| %s | %s |' % (k, ' | '.join(row)))

open(os.path.join(os.path.dirname(D.rstrip('/')), 'realizable-language-tables.md'), 'w').write('\n'.join(out) + '\n')
json.dump(J, open(os.path.join(os.path.dirname(D.rstrip('/')), 'realizable-language.json'), 'w'), indent=1, default=str)
print('\n'.join(out))
