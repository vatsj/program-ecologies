"""Queue 81: CPU accounting from the recorded per-cell walls (single-threaded workers)."""
import glob, gzip, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, 'runs', 'tbr_rows')
out = {}
for name, pat in (('T/M stage 1', 'tm/*_100_1.json.gz'), ('T/M stage 2 (all T/M cells)', 'tm/*.json.gz')):
    s = 0.0
    for f in glob.glob(os.path.join(R, pat)):
        s += json.load(gzip.open(f, 'rt'))['wall']
    out[name] = s / 3600
p1 = p2 = 0.0
for f in glob.glob(os.path.join(R, 'p', '*.json.gz')):
    r = json.load(gzip.open(f, 'rt'))
    if abs(r['mN'] - 1.091) < 1e-3:
        p1 += r['wall']
    else:
        p2 += r['wall']
out['P stage 1 (local)'] = p1 / 3600
out['P stage 2 (Daytona, sum of cell walls)'] = p2 / 3600
out['T/M stage 2 only'] = out['T/M stage 2 (all T/M cells)'] - out['T/M stage 1']
for st in ('0a', '0b'):
    out['stage ' + st] = sum(json.loads(l)['wall'] for l in open(os.path.join(R, 'stage%s.jsonl' % st))) / 3600
s = 0.0
for f in glob.glob(os.path.join(R, 'stage1b_*.jsonl')):
    s += sum(json.loads(l)['wall'] for l in open(f))
out['stage 1b (kept runs)'] = s / 3600
for k, v in out.items():
    print('%-40s %6.2f CPU-h' % (k, v))
