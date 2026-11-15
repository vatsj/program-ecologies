"""Queue 80, V1 and V2.

V2: queue 79's Fc+Oc+Rc rows reproduced on 20 cells by queue 79's own machine and historical catalogue (87 programs, 16 fallbacks, C1,
old fuel), with this queue's closure regress key installed (tables rebuilt with the key).
V1: this queue's arm U at the old fuel (UF0 / UFR0, rows produced by script_offers_run stage v1) against queue 75's (F) and queue 78's
(FR) stored rows.

    python3 src/script_offers_v2.py v2 OUT.json
    python3 src/script_offers_v2.py v1 ROWSDIR OUT.json
"""
import os, sys, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

V2_CELLS = [(b, d, r) for b in (1.0, 3.0) for d in (0.1, 0.01) for r in range(5)]


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


def v2(out):
    import script_offers as S
    S.set_regress(True)
    import certified_offers_dyn as CD
    import certified_offers as CO
    cache = os.path.join(ROOT, 'runs', '_cache', 'v2key')       # a separate cache: the tables are rebuilt with the key
    stored = load('runs/co_rows/*/rows_*.jsonl')
    res = []
    for b, d, r in V2_CELLS:
        job = 'main|co:arm=FcOcRc:d=%r:b=%r:ph=0.5|200|64|%d|0' % (d, b, r)
        ref = stored.get(job)
        row = CD.run_job(job, cache)
        same = ref is not None and row['vshare_ts'] == ref['vshare_ts'] and row['snap120']['cls_modal'] == ref['snap120']['cls_modal']
        res.append(dict(id=job, found=ref is not None, identical=bool(same), vstar=row['vstar'], ref_vstar=ref and ref.get('vstar')))
        print(res[-1], flush=True)
    s = dict(n=len(res), found=sum(x['found'] for x in res), identical=sum(x['identical'] for x in res), rows=res)
    json.dump(s, open(out, 'w'), indent=1)


def v1(rowsdir, out):
    mine = load(os.path.relpath(os.path.join(rowsdir, 'rows_*.jsonl'), ROOT))
    q75 = load('runs/lpt_rows/*/rows_*.jsonl')
    q78 = load('runs/pa_rows/*/rows_*.jsonl')
    res = []
    for jid, r in sorted(mine.items()):
        series, spec, N, I, run, lg = jid.split('|')
        if series != 'v1':
            continue
        kv = dict(p.split('=') for p in spec.split(':')[1:])
        if kv['arm'] == 'UF0':
            key = '2a|2a:d=%s:b=%s|%s|%s|%s|0' % (kv['d'], kv['b'], N, I, run); ref = q75.get(key)
        else:
            key = 'main|pa:arm=FR:d=%s:b=%s:g=1.0|%s|%s|%s|0' % (kv['d'], kv['b'], N, I, run); ref = q78.get(key)
        if ref is None:
            res.append(dict(id=jid, ref=key, found=False)); continue
        same = r['vshare_ts'] == ref['vshare_ts'] and r['snap120']['cls_modal'] == ref['snap120']['cls_modal']
        res.append(dict(id=jid, ref=key, found=True, identical=bool(same), vstar=r['vstar'], ref_vstar=ref.get('vstar')))
    s = dict(n=len(res), found=sum(1 for x in res if x['found']), identical=sum(1 for x in res if x.get('identical')), rows=res)
    json.dump(s, open(out, 'w'), indent=1)
    print(s['n'], s['found'], s['identical'])


if __name__ == '__main__':
    if sys.argv[1] == 'v2':
        v2(sys.argv[2])
    else:
        v1(sys.argv[2], sys.argv[3])
