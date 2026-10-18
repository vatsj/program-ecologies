import sys, time, cProfile, pstats
sys.path.insert(0, '/Users/jstav/code/program-ecologies/.claude/worktrees/agent-afee96de1999a8256/src')
import numpy as np
import per_root as PR, sog_full_run as R
R.load_costc()
rule = sys.argv[1]
gens = int(sys.argv[2])
I = int(sys.argv[3])
run = PR.make_run(rule, 101, N=100, I=I)
run.prefill()
t0 = time.time()
pr = cProfile.Profile()
pr.enable()
for g in range(10, gens + 1, 10):
    run.run(g)
    print(g, 'wall %.0f' % (time.time() - t0), 'ctr0', run.ctr[0], 'tfill %.0f' % run.t_fill, 'types', len(run.btypes), len(run.wtypes),
          'cls', len(run.bcls), len(run.wcls), 'fills', dict(run.fills), 'PCchg', run.st_[3][14], run.st_[3][46], flush=True)
pr.disable()
pstats.Stats(pr).sort_stats('cumulative').print_stats(25)
