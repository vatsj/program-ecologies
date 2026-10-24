"""Job-file writer for the migration-window batches, in priority order (cut candidates last).

    python3 src/migration_window_jobs.py OUT [stage ...]   # stages: 1 .. 6 (default all)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import migration_window_run as R

STAGES = {
    '1': lambda n, p: n.startswith('M-base-'),
    '2': lambda n, p: n.startswith(('M-gKR-N100', 'M-gV-N100')),
    '3': lambda n, p: n.startswith(('C16-base-', 'Z4-base-', 'Z64-base-')),
    '4': lambda n, p: n.startswith(('C16-gKR-N100', 'Z4-gKR-')) or p['kind'] == 'K',
    '5': lambda n, p: n.startswith(('M-gKR-N200', 'M-gV-N200')),
    '6': lambda n, p: n.startswith(('C16-gKR-N200', 'Z64-gKR-')),
}


def main():
    out = sys.argv[1]
    stages = sys.argv[2:] or sorted(STAGES)
    lines = []
    seen = set()
    for st in stages:
        for n, p in R.CELLS.items():
            if n in seen or n.startswith('VER') or not STAGES[st](n, p):
                continue
            seen.add(n)
            for r in range(p['runs']):
                lines.append('%s %d' % (n, r))
    open(out, 'w').write('\n'.join(lines) + '\n')
    print(len(lines), 'jobs')


if __name__ == '__main__':
    main()
