"""Runs for the symmetric gate (specs/2026-10-05-symmetric-gate.md) on the prover_carrier_seed kernel, unchanged.

The access rule enters only through the type tables (src/symmetric_gate.py): each job installs the payoff tables of
its (b, rule) in contracts_abm's data cache, then calls prover_carrier_seed.run_job.  Initial populations and kernel
seeds depend only on (f0, N, I, rep) (or (N, I, k, rep) in the lottery), so the rules are paired.

    python3 src/symmetric_gate_run.py time
    python3 src/symmetric_gate_run.py run --set main twins ... [--procs 3]
"""
import argparse, json, os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import contracts_abm as A
import prover_carrier_seed as P
import symmetric_gate as SG
from symmetric_gate_static import data_from_val

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
OUT = os.path.join(RUNS, 'symmetric_gate_rows.json')
GENS = 20000
_DATA = {}
_LAST = {}
_ORIG_RUN = P._run
_ORIG_LOT = P.lottery_state


def _run_wrap(*a):
    out = _ORIG_RUN(*a)
    _LAST['carr_g'] = out[7]; _LAST['agent_t'] = out[15]; _LAST['anc'] = out[16]
    return out


P._run = _run_wrap


def get_data(b, rule):
    k = (b, rule)
    if k not in _DATA:
        z = np.load(SG.TYPES)
        _DATA[k] = data_from_val(z['val_%s_%s' % (b, rule)], A.data(b))
    return _DATA[k]


def challenge_state(job):
    """99 carriers (establishers ∝ mu, own signature; one draw per rep shared across rules and invaders) + 1 invader."""
    d = A.data(job['b'])
    est = P.establishers(d)
    N = job['N']
    rng = np.random.default_rng([41, N, job['rep'], 20251005])
    pe = d['mu'][est] / d['mu'][est].sum()
    src = est[rng.choice(len(est), size=N, p=pe)]
    car = np.ones(N, bool)
    slot = int(rng.integers(N))
    inv = job['invader']
    if inv == 'D':
        src[slot] = d['iD']; car[slot] = False
    elif inv == 'ALLC':
        src[slot] = d['iC']; car[slot] = False
    elif inv == 'FB_nc':
        src[slot] = d['iFB']; car[slot] = False
    job['_slot'] = slot
    it = np.where(car, d['own_type'][src], d['type_of'][src, 0]).astype(np.int64)
    il = np.where(car, d['cls'][src], -1).astype(np.int64)
    seed = int(rng.integers(1 << 30))
    return d, it, il, seed, src, car


def runs_ge(cg, thr):
    """Longest run of consecutive generations with cg >= thr."""
    best = cur = 0
    for v in (cg >= thr):
        cur = cur + 1 if v else 0
        if cur > best: best = cur
    return best


def run_job(job):
    A._D[job['b']] = get_data(job['b'], job['rule'])
    P.lottery_state = challenge_state if job['set'] == 'challenge' else _ORIG_LOT
    r = P.run_job(dict(job))
    cg = np.asarray(_LAST['carr_g'], np.int64)
    NA = job['N'] * job['I']
    G = len(cg)
    r['rule'] = job['rule']
    r['gens_done'] = G
    if not job['lottery']:
        h = job['gens'] // 2
        r['run50_window'] = int(runs_ge(cg[h:], 0.5 * NA)) if G > h else 0
        r['run50_whole'] = int(runs_ge(cg, 0.5 * NA))
        r['established'] = r['run50_window'] >= 1000
        r['extinct'] = r['carrier_ext_gen'] is not None
        r['censored'] = (not r['established']) and (not r['extinct'])
        r['carrier_traj_fine'] = cg[:2000:5].tolist()
    else:
        r['run50_whole'] = int(runs_ge(cg, 0.5 * NA))
        r['extinct'] = bool(G > 0 and cg[-1] == 0)
        r['carrier_final'] = float(cg[-1] / NA) if G else None
    if job['set'] == 'challenge':
        anc = _LAST['anc']
        r['invader_share'] = float((anc == job['_slot']).mean()) if job['invader'] != 'none' else None
        r['slot'] = job['_slot']
    r.pop('trace', None)
    return r


RULES = SG.RULES
F0 = (0.003, 0.01, 0.03, 0.1)


def jobs_for(which, gens=GENS):
    J = []
    base = dict(seed='mix', sigma=0.0, s=0, mN=0.0, ctl='on', I=1)
    if which == 'main':
        for f0 in F0:
            for rep in range(20):
                for rule in RULES:
                    J.append(dict(base, set='main', rule=rule, b='0', f0=f0, N=6400, rep=rep, eps=1e-3, gens=gens, lottery=False))
    if which == 'n25600':
        for rep in range(10):
            for rule in ('asym', 'sym'):
                J.append(dict(base, set='n25600', rule=rule, b='0', f0=0.01, N=25600, rep=rep, eps=1e-3, gens=gens, lottery=False))
    if which == 'twins':
        for f0 in F0:
            for rep in range(20):
                for rule in RULES:
                    J.append(dict(base, set='twins', rule=rule, b='0', f0=f0, N=6400, rep=rep, eps=0.0, gens=100000, lottery=True))
    if which == 'lottery':
        for k in (1, 3):
            for rep in range(40):
                for rule in RULES:
                    J.append(dict(base, set='lottery', rule=rule, b='0', k=k, f0=k / 100, N=100, I=64, rep=rep, mN=1.0, eps=0.0,
                                  gens=100000, lottery=True))
    if which == 'challenge':
        for inv in ('none', 'D', 'ALLC', 'FB_nc'):
            for rep in range(100):
                for rule in RULES:
                    J.append(dict(base, set='challenge', rule=rule, b='0', invader=inv, k=-1, f0=1.0, N=100, I=1, rep=rep, eps=0.0,
                                  gens=100000, lottery=True))
    if which == 'inf_pair':
        for rep in range(20):
            for rule in ('asym', 'sym'):
                J.append(dict(base, set='inf_pair', rule=rule, b='inf', f0=0.01, N=6400, rep=rep, eps=1e-3, gens=gens, lottery=False))
    return J


def key(j):
    return tuple(str(j.get(k)) for k in ('set', 'rule', 'b', 'f0', 'k', 'invader', 'N', 'I', 'rep', 'eps'))


def report_line(r):
    if r['lottery']:
        extra = (' inv %.2f' % r['invader_share']) if r.get('invader_share') is not None else ''
        return '%s %s f0=%g k=%s N=%d I=%d rep %d: %s %s gen %d P(C,C) %.3f carriers %.3f%s (%.0fs)' % (
            r['set'], r['rule'], r['f0'], r.get('k'), r['N'], r['I'], r['rep'], r['status'], r['outcome'], r['stop_gen'], r['pcc'],
            r['final_carrier'], extra, r['time_s'])
    return '%s %s b=%s f0=%g N=%d rep %d: P(C,C) %s carrier %.3f ext %s t50 %s est %s (%.0fs)' % (
        r['set'], r['rule'], r['b'], r['f0'], r['N'], r['rep'], ('%.3f' % r['pcc']) if r['pcc'] is not None else 'extinct',
        r['carrier'], r['carrier_ext_gen'], r['t50'], r['established'], r['time_s'])


def main_run(sets, procs, gens, limit=None):
    rows = json.load(open(OUT)) if os.path.exists(OUT) else []
    done = {key(r) for r in rows}
    jobs = [j for s in sets for j in jobs_for(s, gens) if key(j) not in done]
    if limit: jobs = jobs[:limit]
    print('%d jobs' % len(jobs), flush=True)
    with Pool(procs) as pool:
        for r in pool.imap_unordered(run_job, jobs):
            rows.append(r)
            print(report_line(r), flush=True)
            tmp = OUT + '.tmp'
            json.dump(rows, open(tmp, 'w')); os.replace(tmp, OUT)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('kind', choices=['time', 'run'])
    ap.add_argument('--set', nargs='*', default=['main'])
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--gens', type=int, default=GENS)
    ap.add_argument('--limit', type=int)
    a = ap.parse_args()
    if a.kind == 'time':
        for rule in ('sym', 'asym'):
            j = dict(seed='mix', sigma=0.0, s=0, mN=0.0, ctl='on', I=1, set='time', rule=rule, b='0', f0=0.03, N=6400, rep=0,
                     eps=1e-3, gens=a.gens, lottery=False)
            t = time.time(); r = run_job(j)
            print(report_line(r), 'wall %.1fs' % (time.time() - t), flush=True)
    else:
        main_run(a.set, a.procs, a.gens, a.limit)
