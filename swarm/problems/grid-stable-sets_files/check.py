#!/usr/bin/env python3
"""Reference checker for the grid-stable-sets problem: tests whether a proposed set is a vNM stable set.

Usage:  python3 check.py K "a,b,c a,b,c ..."
Each allocation is three nonnegative integers summing to K (shares in units of 1/K). Prints whether the set is
internally stable, externally stable, and stable; on failure, a witness pair.
"""
import sys
def dominates(x, y):
    return any(x[i] > y[i] and x[j] > y[j] for i, j in ((0, 1), (0, 2), (1, 2)))
def main():
    if len(sys.argv) != 3: print(__doc__); sys.exit(2)
    K = int(sys.argv[1])
    V = [tuple(int(t) for t in s.split(",")) for s in sys.argv[2].split()]
    for v in V:
        if len(v) != 3 or min(v) < 0 or sum(v) != K: raise ValueError(f"not an allocation of {K}: {v}")
    pts = [(a, b, K - a - b) for a in range(K + 1) for b in range(K + 1 - a)]
    internal = [(x, y) for x in V for y in V if dominates(x, y)]
    external = [y for y in pts if y not in V and not any(dominates(x, y) for x in V)]
    print(f"K={K}, |V|={len(set(V))}: internally stable: {'yes' if not internal else 'no, e.g. %s dominates %s' % internal[0]}; "
          f"externally stable: {'yes' if not external else 'no, e.g. %s is undominated' % (external[0],)}; "
          f"stable set: {'YES' if not internal and not external else 'no'}")
if __name__ == "__main__":
    main()
