"""Queue 73 supplement (RE): which core points the islands end on, interior (every share <= 3/6) against boundary
(a share of 4/6), per cell and pooled by mN.  Reads runs/pair_worth_n/rows.jsonl.gz; writes
runs/pair_worth_n/coverage.json."""
import collections, gzip, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
import pair_worth as PW

ROWS = 'runs/pair_worth_n/rows.jsonl.gz'
OUT = 'runs/pair_worth_n/coverage.json'


def main():
    G = PW.get_game('pw13')
    CLA, _ = G.class_tables()
    vec = lambda o: tuple(int(t) for t in G.VEC[o])
    core = sorted({vec(o) for o in range(G.nout) if CLA[o] == 1})
    interior = [p for p in core if max(p) <= 3]
    rows = [json.loads(l) for l in gzip.open(ROWS, 'rt')]
    cells = collections.defaultdict(list)
    for r in rows:
        if r.get('chase', 20) != 20:
            continue
        cells[(r['arm'], r['N'], r['delta'], r['lam'], r['mN'])].append(r)
    out = {'core': core, 'interior': interior, 'cells': [], 'pooled': {}}
    pooled = {m: collections.Counter() for m in (0.0, 1.0)}
    for (arm, N, d, lam, mN), rs in sorted(cells.items()):
        pts = collections.Counter(); modal = collections.Counter()
        for r in rs:
            c = collections.Counter()
            for k, v in r['end_ids'].items():
                if CLA[int(k)] == 1:
                    c[vec(int(k))] += v
            pts.update(c)
            if c:
                modal[str(max(c, key=c.get))] += 1
        pooled[mN].update(pts)
        tot = sum(pts.values())
        out['cells'].append({'arm': arm, 'N': N, 'delta': d, 'lam': lam, 'mN': mN, 'runs': len(rs),
                             'runs_idx': sorted(r['run'] for r in rs), 'core_islands': tot,
                             'points_held': len(pts), 'boundary_islands': sum(v for p, v in pts.items() if max(p) == 4),
                             'eq_split_share': (pts[(2, 2, 2)] / tot) if tot else None,
                             'modal_point_runs': dict(modal),
                             'by_point': {str(p): pts[p] for p in core}})
    for m, c in pooled.items():
        out['pooled'][str(m)] = {'core_islands': sum(c.values()),
                                 'boundary_islands': sum(v for p, v in c.items() if max(p) == 4),
                                 'by_point': {str(p): c[p] for p in core}}
    json.dump(out, open(OUT, 'w'), indent=1)
    for m, s in out['pooled'].items():
        print('mN', m, 'core islands', s['core_islands'], 'boundary', s['boundary_islands'])


if __name__ == '__main__':
    main()
