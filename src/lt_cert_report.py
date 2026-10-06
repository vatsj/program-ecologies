"""Report for the certificates-as-code cells: reads runs/certificates_as_code/*.json, writes
runs/certificates-as-code.md and runs/certificates-as-code.json (summary)."""
import json, os, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(__file__)
IN = os.path.join(HERE, '..', 'runs', 'certificates_as_code')
OUT_MD = os.path.join(HERE, '..', 'runs', 'certificates-as-code.md')
OUT_JS = os.path.join(HERE, '..', 'runs', 'certificates-as-code.json')
KS = [10 ** 5, 10 ** 6, 10 ** 7]
KN = {10 ** 5: '1e5', 10 ** 6: '1e6', 10 ** 7: '1e7'}


def load(tag):
    p = os.path.join(IN, tag + '.json')
    return json.load(open(p)) if os.path.exists(p) else None


def pp(c):
    """Cell play pair string 'x/y' from two cells."""
    return c


def cell(main, x, y):
    c = main['cells'].get('%s|%s' % (x, y))
    return c['play'] if c else '-'


def pair(main, x, y):
    return '%s%s' % (cell(main, x, y)[0], cell(main, y, x)[0])


def checks_of(main, x, y):
    c = main['cells'].get('%s|%s' % (x, y))
    return [d for d in c['calls'] if d['core'] == 'check'] if c else []


def searches_of(main, x, y):
    c = main['cells'].get('%s|%s' % (x, y))
    return [d for d in c['calls'] if d['core'] == 'search'] if c else []


def table(rows, header):
    out = ['| ' + ' | '.join(header) + ' |', '|' + '---|' * len(header)]
    for r in rows: out.append('| ' + ' | '.join(str(x) for x in r) + ' |')
    return '\n'.join(out)


def main():
    md = []
    js = {}
    mains = {(arm, K): load('main_%d_%s' % (K, arm)) for arm in 'SOX' for K in KS}
    bench = load('bench_')
    boundary = load('boundary_')
    held = {K: load('heldout_%d' % K) for K in KS}
    fuzz = load('fuzz_')
    md.append('# Run: the realizable language, milestone 4: certificates as code (2026-10-06)\n')
    md.append('Spec `specs/2026-10-06-certificates-as-code.md`; notes `notes/certificates-as-code.md`; predictions '
              '`predictions/2026-10-06-certificates-as-code.md`; code `src/lt_cert.py`, `src/lt_cert_run.py`, '
              '`src/lt_cert_report.py`, `tests/test_lt_cert.py`; raw tables `runs/certificates_as_code/`. '
              'Plays are the actual runs of `p ⌜p⌝ ⌜q⌝` with global fuel K; V = ⌊K/4⌋, k = ⌊K/2⌋. A pair entry "CD" '
              'means the row program plays C against the column program and the column program plays D against it.\n')

    # ---------------- bench ----------------
    if bench:
        md.append('## 1. Scale guard and costs (K = 10⁷, V = 2.5·10⁶)\n')
        rows = []
        for k, v in bench['checks'].items():
            x, y = k.split('|')
            rows.append([y + ' checks ' + x, v['result'], v['inner'], v['call_cost']])
        md.append(table(rows, ['check (reader checks target\'s script)', 'result', 'inner steps W', 'call cost W + 6']))
        md.append('')
        rows = [[k, v] for k, v in bench['first_K'].items()]
        md.append('Smallest K (V = K/4, sources rebuilt at each K, bisection to ±4) at which the row pair\'s check '
                  'returns T:\n')
        md.append(table(rows, ['pair (target|reader)', 'first K']))
        md.append('')
        rows = []
        for nm, v in bench['scripts'].items():
            if nm.endswith('_storage_nodes') or nm.endswith('_source_nodes'): continue
            for e in v:
                rows.append([nm, e['a'], e['script'], e['nodes'], e['expanded_vs_CB_or_D'],
                             bench['scripts'][nm + '_storage_nodes'], bench['scripts'][nm + '_source_nodes']])
        md.append('Certificate lists (production as frozen; expanded size on the root against CB for C scripts and '
                  'against D for D scripts; storage = term nodes of the whole list; source = term nodes of the program):\n')
        md.append(table(rows, ['program', 'a', 'script', 'nodes', 'expanded', 'list storage', 'source nodes']))
        md.append('')
        rows = [[k, v['scripts'], v['tactic_nodes'], v['host_checks'], v['secs']] for k, v in bench['production'].items()]
        md.append('Production cost per source (fresh producer; host, not charged to matches):\n')
        md.append(table(rows, ['source', 'scripts', 'tactic nodes', 'host check emulations', 'host secs']))
        md.append('')
        js['bench'] = bench

    # ---------------- main arm S ----------------
    carriers = ['CB', 'CB1', 'CBP', 'CBlet', 'CBwrap', 'LobC', 'CBmut', 'CBsloppy', 'CBS2', 'CBN', 'CB0', 'CBN0']
    others = ['C', 'D', 'Ccert', 'Dcert', 'CBfake', 'CBdef', 'SF', 'SFc', 'FB_code', 'FB1_code', 'PB_code', 'G_code']
    for K in KS:
        m = mains[('S', K)]
        if not m: continue
        md.append('## 2.%s Arm S (sound checker) at K = %s\n' % (KS.index(K) + 1, KN[K]))
        cols = carriers
        rows = []
        for x in carriers + others:
            rows.append([x] + [pair(m, x, y) for y in cols])
        md.append(table(rows, ['row \\ col'] + cols))
        md.append('')
        cols2 = others
        rows = []
        for x in carriers + others:
            rows.append([x] + [pair(m, x, y) for y in cols2])
        md.append(table(rows, ['row \\ col'] + cols2))
        md.append('')
        ho = ['CBlet2', 'CBw2', 'CB1h', 'CB1r', 'CBPh', 'CBPr']
        rows = [[x] + [pair(m, x, y) for y in ['CB', 'CB1', 'CBP', 'CBlet', 'CBwrap', 'SFc', 'CBsloppy'] + ho] for x in ho]
        md.append('Held-out sources (carrying the production-set script of their class):\n')
        md.append(table(rows, ['held-out'] + ['CB', 'CB1', 'CBP', 'CBlet', 'CBwrap', 'SFc', 'CBsloppy'] + ho))
        md.append('')

    # ---------------- arms O and X ----------------
    for arm, title in (('O', 'self-only (Hyp^self only; the RE\'s guard)'), ('X', 'none (no hypothesis rule; acyclic scripts)')):
        for K in KS:
            m = mains[(arm, K)]
            if not m: continue
            names = m['names']
            md.append('## 3.%s%s Arm %s, %s, K = %s\n' % ('O' if arm == 'O' else 'X', KS.index(K) + 1, arm, title, KN[K]))
            rows = [[x] + [pair(m, x, y) for y in names] for x in names]
            md.append(table(rows, ['row \\ col'] + names))
            md.append('')

    # ---------------- decomposition ----------------
    md.append('## 4. Decomposition: which carrier pairs cooperate in which arm\n')
    fam = ['CB', 'CB1', 'CBP', 'CBlet', 'CBwrap']
    rows = []
    dec = {}
    for K in KS:
        for arm in 'XOS':
            m = mains[(arm, K)]
            if not m: continue
            twins = sum(1 for x in fam if pair(m, x, x) == 'CC')
            dist = sum(1 for i, x in enumerate(fam) for y in fam[i + 1:] if pair(m, x, y) == 'CC')
            ccert = sum(1 for x in fam if pair(m, x, 'Ccert') == 'CC')
            sfc = sum(1 for x in fam if pair(m, x, 'SFc') == 'CC')
            rows.append([KN[K], arm, '%d/5' % twins, '%d/10' % dist, '%d/5' % ccert, '%d/5' % sfc])
            dec['%s_%s' % (KN[K], arm)] = {'twins': twins, 'distinct': dist, 'Ccert': ccert, 'SFc': sfc}
    md.append(table(rows, ['K', 'arm', 'twins (C,C)', 'distinct carrier pairs (C,C)', 'with Ccert', 'with SFc']))
    md.append('')
    js['decomposition'] = dec

    # ---------------- audit ----------------
    md.append('## 5. Soundness audit, host replay, Lemma Sym, nesting and regress\n')
    rows = []
    audit_tot = {}
    for K in KS:
        for arm in 'SOX':
            m = mains[(arm, K)]
            if not m: continue
            by = defaultdict(Counter)
            for r in m['audit']:
                c = by[r['mode']]
                c['checks'] += 1
                c[r['result']] += 1
                if r.get('host_agree') is True: c['host_agree'] += 1
                if r.get('host_agree') is False: c['host_disagree'] += 1
                if r['result'] == 'T' and r.get('violation'): c['violations'] += 1
                if r.get('usesS'): c['usesS'] += 1
                if r.get('swap'): c['sym_ok'] += int(r['swap']['sym_ok'])
            for mode, c in sorted(by.items()):
                rows.append([KN[K], arm, mode, c['checks'], c['T'], c['F'], c['TO'], c['host_agree'], c['host_disagree'],
                             c['violations'], c['usesS'], c['sym_ok']])
                audit_tot['%s_%s_%s' % (KN[K], arm, mode)] = dict(c)
    md.append('Distinct top-level checks met in the plays (mode 0 sound, 1 naive, 2 self-only, 3 none, 4 sloppy, '
              '5 sound copy). "violations": T checks whose certified atom the actual play contradicts. "S closed": '
              'T checks that closed the swap box; "Sym ok": of those, the swap check is T and costs the same (partner '
              'closed R) or no more.\n')
    md.append(table(rows, ['K', 'arm', 'mode', 'checks', 'T', 'F', 'TO', 'host agrees', 'host disagrees',
                           'violations', 'S closed', 'Sym ok']))
    md.append('')
    js['audit'] = audit_tot
    rows = []
    for K in KS:
        for arm in 'SOX':
            m = mains[(arm, K)]
            if not m: continue
            dep = Counter(r['host_depth'] for r in m['regress'])
            reg = sum(1 for r in m['regress'] if r['regress'] > 0)
            regT = sum(1 for r in m['regress'] if r['regress'] > 0 and r['result'] == 'T')
            rows.append([KN[K], arm, len(m['regress']), dict(sorted(dep.items())), reg, regT,
                         max((r['steps'] for r in m['regress'] if r['result'] == 'T'), default=0)])
    md.append('Fresh re-evaluation of every distinct top-level check (cache cleared): host nesting depth of check '
              'frames, checks in which the term met a regress (a call re-entering an enclosing check), and the largest '
              'inner cost of a check returning T:\n')
    md.append(table(rows, ['K', 'arm', 'checks', 'nesting depth: count', 'with regress', 'regress and T',
                           'max inner steps of a T check']))
    md.append('')

    # ---------------- held-out ----------------
    md.append('## 6. Held-out sources\n')
    rows = []
    for K in KS:
        h = held[K]
        if not h: continue
        for nm, r in h['heldout'].items():
            cc = r['carrying_class']; cf = r['carrying_fresh']
            coop_c = sum(1 for k, v in cc.items() if k != 'self' and v['play_heldout'] == 'C' and v['play_other'] == 'C')
            coop_f = sum(1 for k, v in cf.items() if k != 'self' and v['play_heldout'] == 'C' and v['play_other'] == 'C')
            rows.append([KN[K], nm, r['class'], 'yes' if r['class_script_covers'] else 'no',
                         '; '.join('%s: %s (%d)' % (a, s, n) for a, s, n in r['fresh']), '%d/9' % coop_c, '%d/9' % coop_f,
                         cc['self'] + '/' + cf['self']])
    md.append(table(rows, ['K', 'held-out', 'class', 'class script validates against CB, CB1, CBP', 'fresh production',
                           '(C,C) with production set, class script', 'same, fresh script', 'self-play (class/fresh)']))
    md.append('')
    js['heldout'] = {KN[K]: held[K]['heldout'] for K in KS if held[K]}

    # ---------------- boundary ----------------
    if boundary:
        md.append('## 7. Fuel boundary cells\n')
        rows = []
        for k, r in boundary['Vscan'].items():
            for d in ('V=W-1', 'V=W+0', 'V=W+1'):
                v = r[d]
                rows.append([k, r['W'], d, v['check'], v['inner'], v['play_xy'], v['play_yx']])
        md.append('V scan (K = 10⁶, sources rebuilt with the scanned V; W = the measured inner steps of the check):\n')
        md.append(table(rows, ['target|reader', 'W', 'V', 'check', 'inner steps', 'play target', 'play reader']))
        md.append('')
        rows = []
        for k, r in boundary['Kscan'].items():
            for d in ('K=b-2', 'K=b-1', 'K=b+0', 'K=b+1'):
                v = r[d]
                rows.append([k, r['static_boundary'], d, v['check_x_by_y'], v['play_xy'], v['steps_xy'], v['play_yx']])
        md.append('K scan (V = 25,000 fixed in the sources; b = the static fit boundary: K = V + 10 for CB, 2V + 17 for '
                  'two-call carriers):\n')
        md.append(table(rows, ['x|y', 'static boundary', 'K', 'y checks x', 'play x', 'steps x', 'play y']))
        md.append('')
        js['boundary'] = boundary

    # ---------------- fuzz ----------------
    if fuzz:
        md.append('## 8. Fuzz soundness audit (K = 10⁵)\n')
        rows = [[mode, v['checks'], v['accepted'], v['violations']] for mode, v in sorted(fuzz['per_mode'].items())]
        md.append(table(rows, ['mode', 'checks', 'accepted (T)', 'accepted false atoms']))
        md.append('')
        js['fuzz'] = fuzz['per_mode']

    # ---------------- plateau ----------------
    md.append('## 9. Finite-K plateau (arm S)\n')
    diffs = {}
    for a, b in ((10 ** 5, 10 ** 6), (10 ** 6, 10 ** 7)):
        ma, mb = mains[('S', a)], mains[('S', b)]
        if not (ma and mb): continue
        d = [k for k in ma['cells'] if k in mb['cells'] and ma['cells'][k]['play'] != mb['cells'][k]['play']]
        diffs['%s->%s' % (KN[a], KN[b])] = d
        md.append('- %s → %s: %d ordered cells change: %s' % (KN[a], KN[b], len(d), ', '.join(sorted(d)[:60])))
    md.append('')
    js['plateau'] = diffs

    # ---------------- searchers ----------------
    md.append('## 10. Searchers against carriers (arm S)\n')
    rows = []
    for K in KS:
        m = mains[('S', K)]
        if not m: continue
        oc = Counter()
        for s in ('FB_code', 'FB1_code', 'PB_code', 'G_code'):
            for y in carriers + ['Ccert', 'SFc', 'Dcert']:
                for d in searches_of(m, s, y):
                    oc[(s, d['result'])] += 1
        rows.append([KN[K], ', '.join('%s %s: %d' % (s, r, n) for (s, r), n in sorted(oc.items()))])
    md.append(table(rows, ['K', 'top-level search outcomes of searchers against carriers (T found, F refuted, TO interrupted)']))
    md.append('')

    # ---------------- held-out rows against their class ----------------
    cls = {'CBlet2': 'CB', 'CBw2': 'CB', 'CB1h': 'CB1', 'CB1r': 'CB1', 'CBPh': 'CBP', 'CBPr': 'CBP'}
    md.append('Held-out rows against their class representative (arm S main cells; the held-out source carries the '
              'production-set script of its class): columns where the pair (held-out vs column, column vs held-out) '
              'differs from (class vs column, column vs class):\n')
    rows = []
    for K in KS:
        m = mains[('S', K)]
        if not m: continue
        names = [n for n in m['names'] if n not in cls]
        for h, k in cls.items():
            diff = [y for y in names if (cell(m, h, y), cell(m, y, h)) != (cell(m, k, y), cell(m, y, k))]
            rows.append([KN[K], h, k, ', '.join(diff) or 'none'])
    md.append(table(rows, ['K', 'held-out', 'class', 'differing columns']))
    md.append('')

    # ---------------- supplements ----------------
    extra = load('extra_')
    if extra:
        md.append('## 11. Supplement: cross-checker carriers whose scripts Run the other checker\'s call\n')
        md.append('Run after the main cells. CBrun / CBS2run / CBNrun carry EvR*; ChkR[EvR*; Ax · Run] (Run in place of '
                  'Hyp on the partner\'s call) plus the D script. Term regress events counted on a fresh evaluation.\n')
        rows = []
        for K, rs in extra.items():
            for k, v in rs.items():
                rows.append([K, k, v['result'], v['inner'], v['regress_events'], v['play_x'] + v['play_y']])
        md.append(table(rows, ['K', 'check', 'result', 'inner steps', 'regress events', 'plays (x, y)']))
        md.append('')
        js['extra'] = extra
    sp = load('selfprobe_O')
    if sp:
        md.append('## 12. Supplement: arm O with self-probe production\n')
        md.append('Run after the main cells. The frozen procedure\'s probes are other carriers, so under the self-only '
                  'checker no carrier got a C script and no twin cooperated in §3. Here each carrier\'s C script is '
                  'produced against its own twin and carried.\n')
        fam = ['CB', 'CB1', 'CBP', 'CBlet', 'CBwrap']
        for K, r in sp.items():
            rows = [[x] + [r['cells']['%s|%s' % (x, y)][0] + r['cells']['%s|%s' % (y, x)][0]
                           for y in fam + ['Ccert', 'SFc', 'CB0']] for x in fam]
            md.append('K = %s; scripts: %s\n' % (K, '; '.join('%s: %s' % kv for kv in r['scripts'].items())))
            md.append(table(rows, ['row \\ col'] + fam + ['Ccert', 'SFc', 'CB0']))
            md.append('')
        js['selfprobe_O'] = sp
    vpath = os.path.join(IN, 'verdicts.md')
    if os.path.exists(vpath):
        md.append(open(vpath).read())

    open(OUT_MD, 'w').write('\n'.join(md) + '\n')
    json.dump(js, open(OUT_JS, 'w'), indent=1, default=str)
    print('wrote', OUT_MD)


if __name__ == '__main__':
    main()
