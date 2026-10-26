"""Run a queue of encounter-contracts jobs with at most CONC at a time.

    python3 src/encounter_contracts_queue.py JOBS.json CONC [AFTER_PID]

JOBS.json: a list of {"argv": [...], "env": {...}, "log": path}.  Each job is one process (no multiprocessing pool).  Jobs whose log
file already ends with a line starting with 'done' are skipped (restartable)."""
import json, os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    jobs = json.load(open(sys.argv[1]))
    conc = int(sys.argv[2])
    if len(sys.argv) > 3:                      # optional: wait for another queue's pid to exit first
        pid = int(sys.argv[3])
        while True:
            try:
                os.kill(pid, 0)
            except OSError:
                break
            time.sleep(30)
    running = []
    todo = list(jobs)
    t0 = time.time()
    while todo or running:
        running = [(p, j) for p, j in running if p.poll() is None]
        while todo and len(running) < conc:
            j = todo.pop(0)
            if os.path.exists(j['log']):
                try:
                    tail = open(j['log']).read().strip().split('\n')[-1]
                    if tail.startswith('done'):
                        continue
                except Exception:
                    pass
            env = dict(os.environ)
            env.update(j.get('env', {}))
            f = open(j['log'], 'w')
            p = subprocess.Popen(j['argv'], cwd=ROOT, env=env, stdout=f, stderr=subprocess.STDOUT)
            running.append((p, j))
            print('%.0f s: started %s (pid %d)' % (time.time() - t0, os.path.basename(j['log']), p.pid), flush=True)
        time.sleep(15)
    print('QUEUE FINISHED', flush=True)


if __name__ == '__main__':
    main()
