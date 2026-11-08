"""Exhaustive enumeration of the length prior to size s0 (queue 75, step 1), Monte Carlo from the prior, and the checks.

Enumeration: every term of size s (node count) over the machine's tags except lib / libsrc / sim (whose mass is accounted
exactly and sampled by Monte Carlo), with the leaf variants of lt_prior (de Bruijn indices in scope + one out-of-scope
leaf, five constants, the literal classes of LIT_CLASSES, readn / readp in R1), each term carrying its exact prior mass
(literal classes carry the mass of the block and behave as the block's representative).  Terms whose sure-reached strict
spine is certainly stuck, or whose root is not a number, are junk without evaluation (static_junk); the others are
evaluated: one taint-tracked evaluation decides partner-independence, a 29 x 29 probe table classifies the rest.

    python3 src/lt_prior_enum.py enum R0 5 SHARD K OUT.json      # sizes 1..5, shard SHARD of K
    python3 src/lt_prior_enum.py mc R1 NSAMPLES SEED OUT.json S0
"""
import os, sys, json, math, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import lt_code as L
import lt_prior as P

CONS = L.CONS
OPS = L.OPS


# ====================================================================== the enumerator
class Enumerator:
    def __init__(self, mach, memo_max=3):
        self.mach = mach
        self.pt = 1.0 / mach.T
        self.tags = P.ENUM_TAGS[mach.name]
        self.memo = {}
        self.memo_max = memo_max
        self.leaf_cache = {}

    def leaves(self, d):
        if d in self.leaf_cache:
            return self.leaf_cache[d]
        pt = self.pt
        out = []
        tot = 0.0
        for i in range(d + 3):
            m = P.elias(i); tot += m
            out.append((('v', i), pt * m))
        out.append((('oos',), pt * (1.0 - tot)))
        if 'con' in self.tags:
            for c in CONS:
                out.append((('con', c), pt / 5))
        if 'nat' in self.tags:
            for lab, rep, m in P.LIT_CLASSES:
                out.append((('nat', rep), pt * m))
        for t in ('readn', 'readp'):
            if t in self.tags:
                out.append(((t,), pt))
        self.leaf_cache[d] = out
        return out

    def get(self, size, d):
        """terms of exactly `size` nodes at binder depth d: a list (small sizes, memoized) or a generator."""
        if size <= self.memo_max:
            key = (size, d)
            r = self.memo.get(key)
            if r is None:
                r = list(self.gen(size, d))
                self.memo[key] = r
            return r
        return self.gen(size, d)

    def gen(self, size, d):
        pt = self.pt
        tags = self.tags
        if size == 1:
            yield from self.leaves(d)
            return
        if size >= 2:
            for tg in ('lam', 'fix'):
                if tg in tags:
                    for t, m in self.get(size - 1, d + 1):
                        yield (tg, t), pt * m
            for tg in ('fst', 'snd', 'quote'):
                if tg in tags:
                    for t, m in self.get(size - 1, d):
                        yield (tg, t), pt * m
        if size >= 3:
            for s1 in range(1, size - 1):
                s2 = size - 1 - s1
                for a, ma in self.get(s1, d):
                    for b, mb in self.get(s2, d):
                        mm = pt * ma * mb
                        for tg in ('app', 'pair', 'eq'):
                            if tg in tags:
                                yield (tg, a, b), mm
                        if 'op' in tags:
                            m7 = mm / 7
                            for o in OPS:
                                yield ('op', o, a, b), m7
        if size >= 4:
            for s1 in range(1, size - 2):
                for s2 in range(1, size - 1 - s1):
                    s3 = size - 1 - s1 - s2
                    if s3 < 1:
                        continue
                    for a, ma in self.get(s1, d):
                        for b, mb in self.get(s2, d):
                            mab = pt * ma * mb
                            for c, mc in self.get(s3, d):
                                mm = mab * mc
                                for tg in ('if', 'capk', 'run'):
                                    if tg in tags:
                                        yield (tg, a, b, c), mm


def enum_run(mach, s0, shard=0, K=1, log=None, size_from=1):
    """classify every enumerated term of sizes size_from..s0 (shard `shard` of K by stream index).  Returns
    stats[size][(family, exact)] = [mass, count] and examples."""
    en = Enumerator(mach)
    pr = P.probes()
    stats = {}
    ex = {}
    nev = 0
    ndone = 0
    t0 = time.time()
    for s in range(size_from, s0 + 1):
        st = stats.setdefault(s, {})
        idx = 0
        for term, m in en.get(s, 0):
            idx += 1
            if K > 1 and (idx % K) != shard:
                continue
            fam, exact, ne = P.classify_body(term, mach, pr)
            nev += ne
            ndone += 1
            if ndone % 20000 == 0:
                L._compiled.clear(); L._canon_cache.clear()
            key = (fam, exact)
            e = st.get(key)
            if e is None:
                st[key] = [m, 1]
                ex.setdefault(key, {})[s] = [P.to_sexpr(term)]
            else:
                e[0] += m; e[1] += 1
                lst = ex[key].setdefault(s, [])
                if len(lst) < 3:
                    lst.append(P.to_sexpr(term))
            if idx % 1000000 == 0:
                if log:
                    print('size', s, 'idx', idx, 'elapsed %.0f' % (time.time() - t0), flush=True)
        L._compiled.clear()
        if log:
            print('size', s, 'done', idx, 'terms', 'elapsed %.0f' % (time.time() - t0), flush=True)
    return stats, ex, nev


def pack(stats, ex):
    out = {'stats': {str(s): {'%s|%s' % k: v for k, v in d.items()} for s, d in stats.items()},
           'examples': {'%s|%s' % k: {str(s): v for s, v in d.items()} for k, d in ex.items()}}
    return out


# ====================================================================== Monte Carlo from the prior
class Sampler:
    """draws a body from the prior (all tags, literals exact); trees with more than `cap` pending nodes are lost (a
    supercritical process that still has `cap` open slots is finite with probability q^cap, negligible)."""

    def __init__(self, mach, seed, cap=40):
        self.mach = mach
        self.rng = random.Random(seed)
        self.tags = mach.tags
        self.T = mach.T
        self.cap = cap

    def elias(self):
        r = self.rng
        k = 0
        while r.random() < 0.5:
            k += 1
        # n + 1 in [2^k, 2^(k+1)): mass of the block 2^-(k+1) and uniform inside
        return (1 << k) + r.getrandbits(k) - 1 if k > 0 else 0

    def draw(self):
        """returns (term, size) or (None, size_so_far) if lost."""
        r = self.rng
        tags = self.tags; T = self.T
        size = [0]
        pending = [1]

        def node():
            size[0] += 1
            tg = tags[int(r.random() * T)]
            a = P.ARITY[tg]
            if tg == 'v':
                return ('v', self.elias())
            if tg == 'nat':
                return ('nat', self.elias())
            if tg == 'con':
                return ('con', CONS[int(r.random() * 5)])
            if tg == 'lib':
                return ('lib', int(r.random() * P.NLIB))
            if tg in ('readn', 'readp'):
                return (tg,)
            pending[0] += a - 1
            if pending[0] > self.cap:
                raise OverflowError
            if tg == 'op':
                o = OPS[int(r.random() * 7)]
                x = node(); y = node()
                return ('op', o, x, y)
            if tg == 'sim':
                k = self.elias()
                return ('sim', k, node())
            kids = [node() for _ in range(a)]
            return (tg,) + tuple(kids)
        try:
            t = node()
        except OverflowError:
            return None, size[0]
        return t, size[0]


def scope_fix(t, d=0):
    """free de Bruijn indices of the sampled body beyond the binders in scope behave as stuck (they are never bound):
    the evaluator would index past the environment, so replace them by 'oos' (stuck outside quotes)."""
    tag = t[0]
    if tag == 'v':
        return t if t[1] < d + 3 else ('oos',)
    if tag in ('nat', 'con', 'lib', 'readn', 'readp'):
        return t
    if tag in ('lam', 'fix'):
        return (tag, scope_fix(t[1], d + 1))
    if tag == 'quote':
        return t
    if tag == 'sim':
        return ('sim', t[1], scope_fix(t[2], d))
    if tag == 'op':
        return ('op', t[1], scope_fix(t[2], d), scope_fix(t[3], d))
    return (tag,) + tuple(scope_fix(c, d) for c in t[1:])


def has_excluded(t):
    tag = t[0]
    if tag in P.EXCLUDED_ENUM:
        return True
    if tag in ('v', 'nat', 'con', 'lib', 'readn', 'readp', 'oos'):
        return False
    if tag == 'op':
        return has_excluded(t[2]) or has_excluded(t[3])
    if tag == 'sim':
        return True
    return any(has_excluded(c) for c in t[1:])


def mc_run(mach, n, seed, s0=0, log=False):
    """Monte Carlo from the prior.  counts: all finite samples by class; countsM: the samples that the exhaustive
    enumeration to size s0 does not cover (size > s0, or a lib / libsrc / sim tag anywhere)."""
    sm = Sampler(mach, seed)
    pr = P.probes()
    cnt = {}
    cntM = {}
    nlost = 0
    sizes = {}
    ex = {}
    t0 = time.time()
    for i in range(n):
        t, sz = sm.draw()
        if t is None:
            nlost += 1
            continue
        sizes[sz] = sizes.get(sz, 0) + 1
        body = scope_fix(t)
        fam, exact, _ = P.classify_body(body, mach, pr)
        key = (fam, exact)
        c = cnt.get(key)
        if c is None:
            cnt[key] = [1, sz]
            ex[key] = [P.to_sexpr(t)]
        else:
            c[0] += 1
            if sz < c[1]:
                c[1] = sz; ex[key] = [P.to_sexpr(t)]
        if sz > s0 or has_excluded(t):
            cntM[key] = cntM.get(key, 0) + 1
        if i % 5000 == 4999:
            L._compiled.clear()
            if log:
                print('mc', i + 1, 'elapsed %.0f' % (time.time() - t0), flush=True)
    return dict(n=n, lost=nlost, s0=s0, counts={'%s|%s' % k: v for k, v in cnt.items()},
                countsM={'%s|%s' % k: v for k, v in cntM.items()}, sizes=sizes,
                examples={'%s|%s' % k: v for k, v in ex.items()}, internal_errors=P.INTERNAL_ERRORS[0])


def main():
    cmd = sys.argv[1]
    mach = P.MACHINES[sys.argv[2]]
    if cmd == 'enum':
        s0 = int(sys.argv[3]); shard = int(sys.argv[4]); K = int(sys.argv[5]); out = sys.argv[6]
        t0 = time.time()
        stats, ex, nev = L.run_big(enum_run, mach, s0, shard, K, True)
        res = pack(stats, ex)
        res.update(machine=mach.name, s0=s0, shard=shard, K=K, wall=time.time() - t0, evals=nev, internal_errors=P.INTERNAL_ERRORS[0])
        json.dump(res, open(out, 'w'))
    elif cmd == 'mc':
        n = int(sys.argv[3]); seed = int(sys.argv[4]); out = sys.argv[5]
        s0 = int(sys.argv[6]) if len(sys.argv) > 6 else 0
        t0 = time.time()
        res = L.run_big(mc_run, mach, n, seed, s0, True)
        res.update(machine=mach.name, seed=seed, wall=time.time() - t0)
        json.dump(res, open(out, 'w'))


if __name__ == '__main__':
    main()
