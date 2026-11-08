"""Validations V1 and V2 of queue 75 (spec specs/2026-11-08-length-prior-t.md).

  V1: with delta = 0.09, beta = 0 (law 'main': the stored law, exactly), N = 100 and 200, mN = 1, Lambda = 100, runs 0..39
      reproduce the stored queue-74 rows (runs/majority_tail/rows/T_main_<N>_<r>.jsonl.gz, cell lam = 100, mN = 1) exactly.
      Compared: everything but wall times, the family-indexed arrays (T+ has more families: the extra rows must be zero)
      and the program count K.  Also checks that the 2a law at (0.09, 0) equals the stored law to rounding.
  V2: the bullies behave on the probe set as the DSL bully's definition (reading is bounded: profiles where the read
      completes), and the extended table T+ reproduces the 27-program table on every triple of library programs.

    python3 src/length_prior_t_validate.py v1 N r0 r1 OUT.json
    python3 src/length_prior_t_validate.py v2 OUT.json
"""
import os, sys, json, gzip, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORED = os.path.join(ROOT, 'runs', 'majority_tail', 'rows')
SKIP = ('wall', 'prep_wall', 'fam_names', 'K', 'arm', 'variant')


def stored_cell(N, r):
    path = os.path.join(STORED, 'T_main_%d_%d.jsonl.gz' % (N, r))
    for line in gzip.open(path, 'rt'):
        rec = json.loads(line)
        if rec['lam'] == 100 and rec['mN'] == 1:
            return rec
    raise KeyError((N, r))


def compare(a, b):
    """list of keys that differ between stored a and new b (T+ has nine families, the stored T seven)."""
    bad = []
    for k in a:
        if k in SKIP:
            continue
        if k == 'tail':
            ta, tb_ = a['tail'], b['tail']
            for kk in ('early', 'late'):
                ra, rb = ta[kk], tb_[kk]
                if ra != rb[:len(ra)] or any(any(x) for x in rb[len(ra):]):
                    bad.append('tail.' + kk)
            for kk in ta:
                if kk not in ('early', 'late') and ta[kk] != tb_[kk]:
                    bad.append('tail.' + kk)
            continue
        if a[k] != b[k]:
            bad.append(k)
    return bad


def v1(N, r0, r1, out, cache_dir):
    import length_prior_t as LP
    w = LP.law_main_exact()
    res = []
    for r in range(r0, r1):
        t = time.time()
        old = stored_cell(N, r)
        rec = LP.run_cell(w, w, N, r, 64, long=bool(old.get('long')), cache_dir=cache_dir, slim=False)
        rec = json.loads(json.dumps(rec))     # the stored rows went through JSON (string keys)
        bad = compare(old, rec)
        res.append(dict(N=N, r=r, ok=(not bad), bad=bad, wall=round(time.time() - t, 1)))
        print(N, r, 'OK' if not bad else bad, res[-1]['wall'], flush=True)
    json.dump(res, open(out, 'w'))


def v1_long(N, r, cache_dir):
    """stored long runs (r < 10): re-run long and compare."""
    import length_prior_t as LP
    w = LP.law_main_exact()
    rec = LP.run_cell(w, w, N, r, 64, long=True, cache_dir=cache_dir, slim=False)
    old = stored_cell(N, r)
    return compare(old, rec)


def v2(out, cache_dir):
    import tplus as TP
    import many_islands_t as MT
    tb = TP.TabsPlus(cache_dir=cache_dir)
    old = MT.Tabs(cache_dir=os.path.join(cache_dir, 'old'))
    res = {}
    for a in ('code', 'steps', 'nto', 'fo'):
        res['table_' + a] = bool((getattr(tb, a)[:27, :27, :27] == getattr(old, a)).all())
    res['table_joint'] = bool((tb.JT[:27, :27, :27] == old.JT).all())
    # bully definition on profiles where the read completes (no failed read, no forfeit)
    code = tb.code; nto = tb.nto; fo = tb.fo
    K = tb.K
    ib = {'Bn': tb.names.index('Bn'), 'Bp': tb.names.index('Bp')}
    chk = {}
    for nm, i in ib.items():
        bad = tot = 0
        for b in range(K):
            for c in range(K):
                if nto[i, b, c] == 0 and fo[i, b, c] == 0:
                    tot += 1
                    if nm == 'Bn':      # reads next b, whose own view is (next = c, prev = me)
                        r = code[b, c, i]; exp = 2 if r == 3 else 4
                    else:               # reads prev c, whose view is (next = me, prev = b)
                        r = code[c, i, b]; exp = 5 if r == 0 else 1
                    bad += int(code[i, b, c] != exp)
        chk[nm] = dict(profiles=tot, mismatches=bad)
    res['bully_definition'] = chk
    # junk
    res['Jf'] = dict(code=int(code[tb.names.index('Jf'), 0, 0]), forfeit=int(fo[tb.names.index('Jf'), 0, 0]), failed_reads=int(nto[tb.names.index('Jf'), 0, 0]))
    res['Jr'] = dict(code=int(code[tb.names.index('Jr'), 0, 0]), forfeit=int(fo[tb.names.index('Jr'), 0, 0]), failed_reads=int(nto[tb.names.index('Jr'), 0, 0]))
    # bully game-level: vs the constants the bully's outcome follows the definition (slot-relative table, outcome ids)
    # the 2a law at (0.09, 0) equals the stored law to rounding
    import length_prior_t as LP
    res['law_2a_vs_stored_maxdiff'] = float(np.abs(LP.law_2a(0.09, 0.0) - LP.law_main_exact()).max())
    json.dump(res, open(out, 'w'), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == '__main__':
    cache = os.environ.get('MT_CACHE', os.path.join(ROOT, 'runs', '_cache'))
    if sys.argv[1] == 'v1':
        v1(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], cache)
    elif sys.argv[1] == 'v2':
        v2(sys.argv[2], cache)
