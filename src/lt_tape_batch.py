"""Batch driver: runs lt_tape_run.py cells as separate processes, at most W at a time, and exits when the batch is done (or
prints STALL and exits if the log has not changed for 2 hours).

    python3 src/lt_tape_batch.py <batch> [workers]
Batches: main (the registered cells), panels (fuel/price/size/sampled/m4 checks), chain (diagnostic, if present).
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'runs', 'lt_tape')
sys.path.insert(0, HERE)
import lt_tape_run as RUN

RPS_ARMS = ['full', 'noprover', 'notape', 'prand']
INSP_ARMS = ['full', 'noprover', 'notape', 'insp_only', 'ee_only', 'prand']
CS = ['0', 'c0']


def cell_args(game, arm, c, cell='primary', K=None, renorm=False, m=3, runs=None, sampled=False):
    a = [game, arm, c, cell]
    if K is not None: a += ['--K', str(K)]
    if renorm: a += ['--renorm']
    if m != 3: a += ['--m', str(m)]
    if runs is not None: a += ['--runs', str(runs)]
    if sampled: a += ['--sampled']
    return a


def out_name(args):
    if args[0] == 'chain':
        return 'chain_%s_%s_%s_N%s' % (args[1], args[2], 'cprice' if args[3] == 'c0' else 'cfree', args[4])
    game, arm, c, cell = args[:4]
    cv = RUN.C0 if c == 'c0' else float(c)
    K = RUN.K0; m = 3; renorm = '--renorm' in args; sampled = '--sampled' in args
    if '--K' in args: K = int(args[args.index('--K') + 1])
    if '--m' in args: m = int(args[args.index('--m') + 1])
    return RUN.cell_name(game, arm, cv, cell, K, renorm, m, sampled)


def batch(name):
    cells = []
    if name == 'main':
        for arm in RPS_ARMS:
            for c in CS: cells.append(cell_args('rps', arm, c))
        for arm in INSP_ARMS:
            for c in CS: cells.append(cell_args('insp', arm, c))
        # renormalized co-primary arms where the default shifts a founder share by more than 0.05 (notes section 2)
        for c in CS:
            cells.append(cell_args('rps', 'notape', c, renorm=True))
        for arm in ('noprover', 'notape', 'insp_only', 'ee_only'):
            for c in CS: cells.append(cell_args('insp', arm, c, renorm=True))
    elif name == 'panels':
        # fuel cap at fixed c0 (and at c = 0), price recalibrated c = 0.12 / K, size check, sampled encounters, m = 4
        for game in ('insp', 'rps'):
            for K in (5000, 20000):
                for c in CS: cells.append(cell_args(game, 'full', c, K=K))
            for K in (1000, 2000, 5000):
                cells.append(cell_args(game, 'full', '%g' % (0.12 / K), K=K))
            if game == 'insp':
                for c in CS: cells.append(cell_args('insp', 'full', c, cell='size'))
                for c in CS: cells.append(cell_args('insp', 'full', c, m=4))
                cells.append(cell_args('insp', 'full', '0', runs=10, sampled=True))
                cells.append(cell_args('insp', 'full', 'c0', runs=10, sampled=True))
            else:
                for c in CS: cells.append(cell_args('rps', 'full', c, cell='size'))
    elif name == 'nosim':
        # post-hoc arm: simulators disabled in place (the registered arms left the responsive prover no room to win against them)
        for game in ('rps', 'insp'):
            for c in CS: cells.append(cell_args(game, 'nosim', c))
    elif name == 'dose':
        # added after the registered cells (labelled in the report): the price dose at the fixed cap K0, c far above the calibrated c0
        for game in ('rps', 'insp'):
            for c in ('0.0001', '0.001', '0.01'):
                cells.append(cell_args(game, 'full', c))
    elif name == 'chain':
        # the epsilon -> 0 diagnostic (the spec's cut order: run last, labelled as a diagnostic)
        for N in (100, 1000, 10000):
            for arm in ('full', 'ee_only', 'nosim'):
                for c in CS: cells.append(['chain', 'insp', arm, c, str(N)])
        for N in (100, 1000, 10000, 100000):
            for arm in ('full', 'nosim', 'noprover'):
                for c in CS: cells.append(['chain', 'rps', arm, c, str(N)])
    elif name == 'dev':
        cells.append(cell_args('rps', 'full', 'c0', runs=2))
    else:
        raise SystemExit('unknown batch')
    return cells


def main():
    name = sys.argv[1]
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    os.makedirs(OUT, exist_ok=True)
    log = os.path.join(OUT, 'batch_%s.log' % name)
    cells = [c for c in batch(name) if not os.path.exists(os.path.join(OUT, out_name(c) + ('.json' if c[0] == 'chain' else '.json.gz')))]
    open(log, 'a').write('%s: %d cells to run\n' % (time.strftime('%H:%M:%S'), len(cells)))
    running = []
    last_change = time.time(); last_size = os.path.getsize(log)
    queue = list(cells)
    while queue or running:
        while queue and len(running) < workers:
            args = queue.pop(0)
            f = open(log, 'a')
            script, sargs = ('lt_tape_chain.py', args[1:]) if args[0] == 'chain' else ('lt_tape_run.py', args)
            p = subprocess.Popen([sys.executable, os.path.join(HERE, script)] + sargs, stdout=f, stderr=subprocess.STDOUT, cwd=ROOT)
            running.append((p, args, f))
            open(log, 'a').write('%s: start %s (pid %d)\n' % (time.strftime('%H:%M:%S'), ' '.join(args), p.pid))
        time.sleep(5)
        for item in list(running):
            p, args, f = item
            if p.poll() is not None:
                running.remove(item); f.close()
                open(log, 'a').write('%s: done %s rc=%d\n' % (time.strftime('%H:%M:%S'), ' '.join(args), p.returncode))
        sz = os.path.getsize(log)
        if sz != last_size: last_size = sz; last_change = time.time()
        if time.time() - last_change > 7200:
            print('STALL', flush=True)
            for p, args, f in running: p.kill()
            return 1
    print('BATCH %s DONE' % name, flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
