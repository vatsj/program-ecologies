"""Batch driver for the pricing-rules cells: runs cells as separate processes, at most W at a time, in priority order, skipping
cells whose output exists.  Exits when the batch is done; prints STALL and exits if no log line has appeared for 2 hours.

    python3 src/pricing_rules_batch.py <batch> [workers]

Batches (all levels as in the predictions file; priority order is the spec's cut order read backwards):
  panel     the complete cross-game panel: every rule at c = 1e-4, 1e-3; A at P_fail 0.1, 1; zero price; bridges; toll
  rest      the remaining levels: c = 1e-5 (PD last), A at 0.01 and 10, then c = 1e-2
  big       the larger geometry for the levels listed in runs/pricing_rules/big_levels.json
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'runs', 'pricing_rules')
PY = sys.executable


def lt_cell(game, rule, level, cell='primary'):
    return ('lt', game, rule, level, cell)


def pd_cell(rule, level, cell='wk_Snon_100_64'):
    return ('pd', rule, level, cell)


def out_file(job):
    if job[0] == 'lt':
        _, game, rule, level, cell = job
        return os.path.join(OUT, '%s_%s_%g_%s.json.gz' % (game, rule, level, cell))
    _, rule, level, cell = job
    return os.path.join(OUT, 'pd_%s_%g_%s.json.gz' % (rule, level, cell))


def cmd(job):
    if job[0] == 'lt':
        _, game, rule, level, cell = job
        a = [PY, os.path.join(HERE, 'pricing_rules_lt.py'), game, rule, repr(level), cell]
        if cell == 'size': a += ['--runs', '20']
        return a
    _, rule, level, cell = job
    runs = 20
    return [PY, os.path.join(HERE, 'pricing_rules_pd.py'), rule, repr(level), cell, '--runs', str(runs)]


def lt_rules_at_c(c, games=('rps', 'insp')):
    jobs = []
    for g in games:
        for rule in ('F', 'FA', 'Bw', 'B'):
            jobs.append(lt_cell(g, rule, c))
    return jobs


def batch(name):
    jobs = []
    if name == 'panel':
        for g in ('rps', 'insp'):
            jobs.append(lt_cell(g, 'Z', 0.0))
        for c in (1e-3, 1e-4):
            jobs += lt_rules_at_c(c)
        for g in ('rps', 'insp'):
            for p in (0.1, 1.0):
                jobs.append(lt_cell(g, 'A', p))
            for t in (0.1, 1.0):
                jobs.append(lt_cell(g, 'T', t))
        jobs.append(pd_cell('Z', 0.0))
        for c in (1e-3, 1e-4):
            for rule in ('F', 'FA', 'B'):
                jobs.append(pd_cell(rule, c))
        for p in (0.1, 1.0):
            jobs.append(pd_cell('A', p))
        # sampled-kernel bridges (zero price and F through the sampled kernel), after the panel proper
        for g in ('rps', 'insp'):
            jobs.append(lt_cell(g, 'Zs', 0.0))
            for c in (1e-3, 1e-4):
                jobs.append(lt_cell(g, 'Fs', c))
        for t in (0.1, 1.0):
            jobs.append(pd_cell('T', t))
    elif name == 'rest':
        for p in (0.01, 10.0):
            for g in ('rps', 'insp'):
                jobs.append(lt_cell(g, 'A', p))
            jobs.append(pd_cell('A', p))
        for rule in ('F', 'FA', 'Bw', 'B'):
            for g in ('rps', 'insp'):
                jobs.append(lt_cell(g, rule, 1e-5))
        for c in (1e-2,):
            for rule in ('F', 'FA', 'Bw', 'B'):
                for g in ('rps', 'insp'):
                    jobs.append(lt_cell(g, rule, c))
        for rule in ('F', 'FA', 'B'):
            jobs.append(pd_cell(rule, 1e-2))
        for rule in ('F', 'FA', 'B'):
            jobs.append(pd_cell(rule, 1e-5))
    elif name == 'warm':
        for c in (1e-3, 1e-4):
            for g in ('rps', 'insp'):
                jobs.append(lt_cell(g, 'Bws', c))
    elif name == 'big':
        p = os.path.join(OUT, 'big_levels.json')
        levels = json.load(open(p)) if os.path.exists(p) else []
        for (rule, level) in levels:
            for g in ('rps', 'insp'):
                jobs.append(lt_cell(g, rule, level, 'size'))
            jobs.append(pd_cell(rule, level, 'wk_Snon_200_64'))
    else:
        raise ValueError(name)
    return jobs


def main():
    name = sys.argv[1]
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    os.makedirs(OUT, exist_ok=True)
    todo = [j for j in batch(name) if not os.path.exists(out_file(j))]
    print('%s: %d cells to run, %d workers (pid %d)' % (name, len(todo), workers, os.getpid()), flush=True)
    running = []
    tries = {}
    last = time.time()
    logs = {}
    while todo or running:
        while todo and len(running) < workers:
            job = todo.pop(0)
            logp = os.path.join(OUT, 'log_' + os.path.basename(out_file(job)).replace('.json.gz', '.txt'))
            f = open(logp, 'w')
            p = subprocess.Popen(cmd(job), stdout=f, stderr=subprocess.STDOUT, cwd=ROOT)
            running.append((job, p, f, logp, time.time()))
            print('start', job, 'pid', p.pid, flush=True); last = time.time()
        time.sleep(20)
        for item in list(running):
            job, p, f, logp, t0 = item
            if p.poll() is not None:
                f.close(); running.remove(item)
                print('done', job, 'rc', p.returncode, 'wall %.0fs' % (time.time() - t0), flush=True); last = time.time()
                if p.returncode != 0 and tries.get(job, 0) < 2:
                    tries[job] = tries.get(job, 0) + 1
                    todo.insert(0, job)
                    print('retry', job, flush=True)
        # stall: no output file of a running job has changed for 2 hours
        newest = max([os.path.getmtime(it[3]) for it in running] + [last]) if running else last
        if running and time.time() - newest > 7200:
            print('STALL', flush=True)
            for it in running: it[1].kill()
            return 2
    print('batch %s finished' % name, flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
