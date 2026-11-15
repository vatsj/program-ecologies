"""V1 of queue 79: the F and FR cells run on the 87-program catalogue reproduce queue 75's (F) and queue 78's (FR) stored rows exactly
(the V* series every N generations and the 120N modal class counts).

    python3 src/certified_offers_v1.py OUT.json
"""
import os, sys, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(pattern):
    out = {}
    for f in glob.glob(os.path.join(ROOT, pattern)):
        for line in open(f):
            line = line.strip()
            if line:
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                out[r['id']] = r
    return out


def main(out):
    mine = load('runs/co_rows/v1/rows_*.jsonl')
    q75 = load('runs/lpt_rows/*/rows_*.jsonl')
    q78 = load('runs/pa_rows/*/rows_*.jsonl')
    res = []
    for jid, r in sorted(mine.items()):
        series, spec, N, I, run, lg = jid.split('|')
        kv = dict(p.split('=') for p in spec.split(':')[1:])
        if kv['arm'] == 'F':
            key = '2a|2a:d=%s:b=%s|%s|%s|%s|0' % (kv['d'], kv['b'], N, I, run)
            ref = q75.get(key)
        else:
            key = 'main|pa:arm=FR:d=%s:b=%s:g=1.0|%s|%s|%s|0' % (kv['d'], kv['b'], N, I, run)
            ref = q78.get(key)
        if ref is None:
            res.append(dict(id=jid, ref=key, found=False)); continue
        same = r['vshare_ts'] == ref['vshare_ts'] and r['snap120']['cls_modal'] == ref['snap120']['cls_modal']
        res.append(dict(id=jid, ref=key, found=True, identical=bool(same), vstar=r['vstar'], ref_vstar=ref.get('vstar')))
    s = dict(n=len(res), found=sum(1 for x in res if x['found']), identical=sum(1 for x in res if x.get('identical')), rows=res)
    json.dump(s, open(out, 'w'), indent=1)
    print(s['n'], s['found'], s['identical'])


if __name__ == '__main__':
    main(sys.argv[1])
