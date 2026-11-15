#!/usr/bin/env python3
"""Queue 79: apply the budget cut to job files and to running sandboxes.

The cut (notes/certified-offers.md, Budget): I = 256 (all), the phi in {0, 1} extension to the arms other than FcOcRc and Fc, and the mixed
arm at N = 400.  For a running sandbox the cut jobs of its chunk are pre-locked (the workers skip a job whose lock file exists); for a
chunk not yet launched the job file is rewritten without them.

    python3 tools/co_cut.py files              # rewrite runs/co_jobs/g_*of12.txt of chunks still in the queue
    python3 tools/co_cut.py lock SANDBOX CHUNK # pre-lock the cut jobs of CHUNK inside SANDBOX
"""
import hashlib, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def is_cut(job):
    series, spec = job.split('|')[:2]
    N = int(job.split('|')[2])
    if series == 'i256':
        return True
    if series == 'phi' and not ('arm=FcOcRc:' in spec or 'arm=Fc:' in spec):
        return True
    if series == 'main' and 'arm=mix:' in spec and N == 400:
        return True
    return False


def jobs_of(chunk):
    return [l.strip() for l in open(os.path.join(ROOT, 'runs', 'co_jobs', chunk + '.txt')) if l.strip()]


if __name__ == '__main__':
    if sys.argv[1] == 'files':
        queued = [l.strip() for l in open(os.path.join(ROOT, 'runs', 'co_launch', 'queue.txt')) if l.strip()]
        for c in queued:
            js = jobs_of(c)
            keep = [j for j in js if not is_cut(j)]
            open(os.path.join(ROOT, 'runs', 'co_jobs', c + '.txt'), 'w').write('\n'.join(keep) + '\n')
            print(c, len(js), '->', len(keep))
    elif sys.argv[1] == 'lock':
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import daytona_run as DR
        from daytona import Daytona
        sid, chunk = sys.argv[2], sys.argv[3]
        cut = [j for j in jobs_of(chunk) if is_cut(j)]
        names = ' '.join('lock_' + hashlib.md5(j.encode()).hexdigest() for j in cut)
        d = Daytona()
        sb = [s for s in DR._ours(d) if s.id.startswith(sid)][0]
        r = sb.process.exec('cd %s/runs/co_rows/%s && touch %s && ls lock_* | wc -l' % (DR.REMOTE, chunk, names), timeout=120)
        print(sid, chunk, len(cut), 'cut jobs pre-locked; locks now', r.result.strip())
