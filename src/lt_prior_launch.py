"""Launcher for the counted step-1 runs of queue 75 (inside a sandbox or locally): shards of the exhaustive enumeration, Monte
Carlo chunks and the targeted search, DAYTONA_CPUS processes at a time.  Outputs go to OUTDIR:
enum_<M>_s<S0>_<shard>of<K>.json, mc_<M>_<seed>.json, search_<M>.json.

    python3 src/lt_prior_launch.py OUTDIR enum  M S0 K SHARDS        # SHARDS like 0,1,2,3
    python3 src/lt_prior_launch.py OUTDIR mc    M NPER NPROC SEED0 S0
    python3 src/lt_prior_launch.py OUTDIR search M
"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))


def pool(cmds, nproc):
    running = []
    fails = 0
    for c in cmds:
        while len(running) >= nproc:
            for p in running:
                if p.poll() is not None:
                    running.remove(p); fails += int(p.returncode != 0)
                    break
            else:
                running[0].wait()
        running.append(subprocess.Popen(c))
    for p in running:
        p.wait(); fails += int(p.returncode != 0)
    return fails


if __name__ == '__main__':
    out, kind, M = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(out, exist_ok=True)
    ncpu = int(os.environ.get('DAYTONA_CPUS', os.cpu_count() or 1))
    py = sys.executable
    if kind == 'enum':
        s0, K = int(sys.argv[4]), int(sys.argv[5])
        shards = [int(x) for x in sys.argv[6].split(',')]
        cmds = [[py, os.path.join(HERE, 'lt_prior_enum.py'), 'enum', M, str(s0), str(sh), str(K),
                 os.path.join(out, 'enum_%s_s%d_%dof%d.json' % (M, s0, sh, K))] for sh in shards]
    elif kind == 'mc':
        nper, nproc, seed0, s0 = int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
        cmds = [[py, os.path.join(HERE, 'lt_prior_enum.py'), 'mc', M, str(nper), str(seed0 + i),
                 os.path.join(out, 'mc_%s_%d.json' % (M, seed0 + i)), str(s0)] for i in range(nproc)]
    else:
        cmds = [[py, os.path.join(HERE, 'lt_prior_search.py'), M, os.path.join(out, 'search_%s.json' % M)]]
    sys.exit(1 if pool(cmds, ncpu) else 0)
