"""Small extra analyses for the unequal-basin report: start composition (tilt check, E9), conditional shares, the program counts of
the empirical start, the ladder table (m, core) and the random-knockout summary.   python3 src/unequal_basin_extras.py"""
import os, sys, json, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import unequal_basin as UB
import unequal_basin_run as R
import unequal_basin_jobs as J
import unequal_basin_core as UC

OUT = os.path.join(UC.OUTD, 'extras.json')


def start_composition():
    out = {}
    for cn in ('L0', 'M0'):
        spec = dict(cell=cn, m=3, start='nat', abl=None, core='pilot_L')
        core = J.load_core('pilot_L')
        cell, obj, xn, dropped = R.build_obj_start(spec, None, 'reassign', None, core)
        rows = {}
        for st in ('nat', 'fair', 'uneq', 'wd', 'u:0.3', 'u:0.9'):
            x0, info = R.make_start(obj, xn, st)
            if x0 is None:
                rows[st] = None
                continue
            q = obj.marg(x0)
            cond_share = [float(q[s][~obj.isc].sum()) for s in range(3)]
            # conditional share of each outcome class (slot 0)
            by_class = {}
            for k, nm in enumerate(UB.CLS):
                sel = obj.cl == k
                if x0[sel].sum() > 0:
                    by_class[nm] = float(x0[sel & (~obj.isc[obj.pid[0]])].sum() / x0[sel].sum())
            rows[st] = dict(class_shares=obj.class_shares(x0).tolist(), cond_share_slot0=cond_share[0], cond_share_by_class_slot0=by_class)
        out[cn] = dict(dropped_mass=dropped, rows=rows)
    return out


def ladder():
    rows = []
    for f in sorted(glob.glob(os.path.join(R.ROWS, '*.json'))):
        if os.path.basename(f).startswith('scan_'):
            continue
        r = json.load(open(f))
        sp = r.get('spec')
        if not sp or sp.get('abl') or str(sp['start']) not in ('nat', 'u:0.6') or sp['cell'] not in ('L0', 'M0') or 'records' not in r:
            continue
        if sp.get('raw') or str(sp['start']).startswith('mix'):
            continue
        rows.append(dict(cell=sp['cell'], m=sp['m'], core=sp.get('core') or 'all conditionals', pools=sp.get('pools') or [0, 1, 2], start=sp['start'],
                         states=r['states'], status=r['status'], endpoint=r['endpoint'], final=r['records'][-1]['shares'], t_end=r['t_end'],
                         dropped=r.get('dropped_mass')))
    rows.sort(key=lambda d: (d['cell'], str(d['pools']), d['start'], d['m'], str(d['core'])))
    return rows


def random_knockouts():
    out = []
    for f in sorted(glob.glob(os.path.join(R.ROWS, '*.json'))):
        r = json.load(open(f))
        sp = r.get('spec')
        if not sp or not str(sp.get('abl') or '').startswith('rand:') or 'records' not in r:
            continue
        out.append(dict(cell=sp['cell'], abl=sp['abl'], start=sp['start'], status=r['status'], endpoint=r['endpoint'], final=r['records'][-1]['shares'],
                        states=r['states']))
    return out


if __name__ == '__main__':
    res = dict(start_composition=start_composition(), ladder=ladder(), random_knockouts=random_knockouts())
    json.dump(res, open(OUT, 'w'), indent=1, default=str)
    print(json.dumps(res['start_composition'], indent=1)[:3000])
    for r in res['ladder']:
        print(r['cell'], r['pools'], r['start'], 'm', r['m'], r['core'], r['states'], r['endpoint'], [round(v, 4) for v in r['final']])
    for r in res['random_knockouts']:
        print(r['cell'], r['abl'], r['endpoint'], [round(v, 4) for v in r['final']])
