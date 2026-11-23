"""Queue 81, stage 1b: frozen natives.  For the ten most common island profiles of an arm's stage-1 worlds (N = 200,
mN = 1 for T and M; arm P at its boundary mN), freeze the natives, take the migrant distribution of the worlds in
which the profile occurs as an exogenous tester field (pooled over occurrences, island-count weights, the island
itself excluded), and simulate fixation from one copy of each member of E(p; k) against the resident.
In arm P (one pool) only tester migrants arrive, at total rate mN * (share of the field that is not p), so that, as
in the focal slot of T and M, migrants of the resident's own program do not dilute the variant.

Members of E are grouped into classes with identical payoffs against every tester triple of the field (they have the
same law in this simulation); one simulation per class.  The island is a real Moran island: in the other slots (arm T,
M) or in the same pool (arm P) migrants arrive at mN per generation, drawn from the field (a draw of the native's own
program is a no-op birth), and live or die under selection (fitness exp(w * expected payoff)).  Migration into the
focal slot is switched off (the variant competes with the resident only).  A replicate ends with the variant fixed,
lost, or a tester type reaching N/2 of its slot (tester established, counted as not fixed).  sigma is P10's,
w * sum mN a_q T_q Delta_q, with T_q the exact single-arrival sojourn.

    python3 src/tbr_1b.py ARM [--reps 40000]
"""
import argparse, gzip, glob, json, math, os, sys, time
from collections import Counter, defaultdict
import numpy as np
from numba import njit
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = 0.3
OUT = os.path.join(ROOT, 'runs', 'tbr_rows')


def asym(s):
    return 1.0 if abs(s) < 1e-12 else s / (1.0 - math.exp(-s))


@njit(cache=True)
def _sim3(P, j, nA, n1, n2, field1, field2, nat1, nat2, N, w, mN, reps, seed):
    """three slots; slot j holds types 0 (resident) and 1 (variant); other slots o1 < o2 hold n1 / n2 types (index 0
    the native).  P[a, b, c, 3] payoffs over (slot-j type, o1 type, o2 type) in slot-j-first order."""
    np.random.seed(seed)
    res = np.zeros(4, np.int64)
    half = N // 2
    pm = mN / N
    c0 = np.zeros(2, np.int64); c1 = np.zeros(n1, np.int64); c2 = np.zeros(n2, np.int64)
    cf1 = np.cumsum(field1); cf2 = np.cumsum(field2)
    f0 = np.zeros(2); fv = np.zeros(max(n1, n2))
    for r in range(reps):
        c0[:] = 0; c1[:] = 0; c2[:] = 0
        c0[0] = N - 1; c0[1] = 1; c1[0] = N; c2[0] = N
        out = -1
        while out < 0:
            sl = np.random.randint(3)
            if sl == 0:
                for a in range(2):
                    v = 0.0
                    for b in range(n1):
                        if c1[b] == 0: continue
                        for c in range(n2):
                            if c2[c] == 0: continue
                            v += c1[b] * c2[c] * P[a, b, c, j]
                    f0[a] = c0[a] * math.exp(w * v / (N * N))
                u = np.random.random() * (f0[0] + f0[1])
                ch = 0 if u < f0[0] else 1
                vi = 0 if np.random.randint(N) < c0[0] else 1
                c0[ch] += 1; c0[vi] -= 1
                if c0[1] == 0: out = 1
                elif c0[1] == N: out = 0
            else:
                if sl == 1:
                    cnt = c1; nn = n1; cf = cf1; o = 1
                else:
                    cnt = c2; nn = n2; cf = cf2; o = 2
                if np.random.random() < pm:
                    u = np.random.random() * cf[nn - 1]
                    ch = 0
                    while ch < nn - 1 and u > cf[ch]:
                        ch += 1
                else:
                    tot = 0.0
                    for t in range(nn):
                        fv[t] = 0.0
                        if cnt[t] == 0: continue
                        v = 0.0
                        for a in range(2):
                            if c0[a] == 0: continue
                            if o == 1:
                                for c in range(n2):
                                    if c2[c] == 0: continue
                                    v += c0[a] * c2[c] * P[a, t, c, 4]
                            else:
                                for b in range(n1):
                                    if c1[b] == 0: continue
                                    v += c0[a] * c1[b] * P[a, b, t, 5]
                        fv[t] = cnt[t] * math.exp(w * v / (N * N))
                        tot += fv[t]
                    u = np.random.random() * tot
                    ch = 0; acc = 0.0
                    for t in range(nn):
                        acc += fv[t]
                        if u <= acc and fv[t] > 0:
                            ch = t; break
                x = np.random.randint(N); acc2 = 0; vi = 0
                for t in range(nn):
                    acc2 += cnt[t]
                    if x < acc2:
                        vi = t; break
                cnt[ch] += 1; cnt[vi] -= 1
                for t in range(1, nn):
                    if cnt[t] >= half:
                        out = 2
        res[out] += 1
    return res


@njit(cache=True)
def _sim1(U, n, field, N, w, mN, reps, seed):
    """one population; types 0 resident, 1 variant, 2.. testers; U[a, b] payoffs; fitness exp(w * mean payoff, self
    excluded); a migrant birth (prob mN / N) draws its type from the field (over types, index 0 = resident)."""
    np.random.seed(seed)
    res = np.zeros(4, np.int64)
    half = N // 2; pm = mN / N
    cnt = np.zeros(n, np.int64); fv = np.zeros(n)
    cf = np.cumsum(field)
    for r in range(reps):
        cnt[:] = 0; cnt[0] = N - 1; cnt[1] = 1
        out = -1
        while out < 0:
            if np.random.random() < pm:
                u = np.random.random() * cf[n - 1]
                ch = 0
                while ch < n - 1 and u > cf[ch]:
                    ch += 1
            else:
                tot = 0.0
                for t in range(n):
                    if cnt[t] == 0:
                        fv[t] = 0.0; continue
                    v = 0.0
                    for t2 in range(n):
                        v += cnt[t2] * U[t, t2]
                    v -= U[t, t]
                    fv[t] = cnt[t] * math.exp(w * v / (N - 1))
                    tot += fv[t]
                u = np.random.random() * tot
                ch = 0; acc = 0.0
                for t in range(n):
                    acc += fv[t]
                    if u <= acc and fv[t] > 0:
                        ch = t; break
            x = np.random.randint(N); acc2 = 0; vi = 0
            for t in range(n):
                acc2 += cnt[t]
                if x < acc2:
                    vi = t; break
            cnt[ch] += 1; cnt[vi] -= 1
            # the variant fixes against the resident when the resident is extinct (testers may be present)
            if cnt[1] == 0: out = 1
            elif cnt[0] == 0: out = 0
            else:
                for t in range(2, n):
                    if cnt[t] >= half:
                        out = 2
        res[out] += 1
    return res


def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def run_tm(arm, reps, N=200, mN=1.0, top=10, diverse_only=False):
    import tbr
    A = tbr.Tri(arm)
    files = sorted(glob.glob(os.path.join(ROOT, 'runs', 'tbr_rows', 'tm', '%s_%d_*_100_1.json.gz' % (arm, N))))
    occ = Counter(); fields = defaultdict(lambda: [Counter(), Counter(), Counter()])
    for f in files:
        rec = json.load(gzip.open(f, 'rt'))
        if diverse_only and not rec['snaps']['100']['world']['diverse']:
            continue
        cs = rec['snaps']['100']['cases']
        maj = {}
        for c in cs:
            maj.setdefault(c['i'], [0, 0, 0])[c['j']] = c['p']
        I = len(maj)
        profs = [tuple(maj[i]) for i in range(I)]
        cnt = [Counter(p[s] for p in profs) for s in range(3)]
        for pr in profs:
            occ[pr] += 1
            for s in range(3):
                for q, n in cnt[s].items():
                    fields[pr][s][q] += (n - (1 if q == pr[s] else 0)) / (I - 1)
    rows = []
    for pr, n_occ in occ.most_common(top):
        for j in range(3):
            o1, o2 = tbr.OTHERS[j]
            p = pr[j]
            row = A.pay_slot(j, np.arange(A.K), {o1: [pr[o1]], o2: [pr[o2]]})[:, 0, 0, :]
            E = np.nonzero(np.all(np.abs(row - row[p]) <= 1e-12, axis=1))[0]
            F1 = fields[pr][o1]; F2 = fields[pr][o2]
            Q1 = [pr[o1]] + sorted(q for q in F1 if q != pr[o1] and F1[q] > 0)
            Q2 = [pr[o2]] + sorted(q for q in F2 if q != pr[o2] and F2[q] > 0)
            f1 = np.array([F1.get(q, 0.0) for q in Q1]) / n_occ
            f2 = np.array([F2.get(q, 0.0) for q in Q2]) / n_occ
            Pfull = A.pay_slot(j, E, {o1: Q1, o2: Q2})            # (|E|, n1, n2, 3), axes slot-j-first
            # classes of E with identical payoffs against every tester triple
            keyd = {}
            for x in range(len(E)):
                keyd.setdefault(Pfull[x].round(12).tobytes(), []).append(x)
            ip = int(np.searchsorted(E, p))
            # sigma (P10) per class: testers one at a time against natives
            unat1 = row[p, o1]; unat2 = row[p, o2]
            T1 = np.array([tbr.sojourn(N, math.exp(W * (Pfull[ip, b, 0, o1] - unat1)))[0] for b in range(len(Q1))])
            T2 = np.array([tbr.sojourn(N, math.exp(W * (Pfull[ip, 0, c, o2] - unat2)))[0] for c in range(len(Q2))])
            for key, mem in keyd.items():
                x = mem[0]
                d1 = Pfull[x, :, 0, j] - Pfull[ip, :, 0, j]
                d2 = Pfull[x, 0, :, j] - Pfull[ip, 0, :, j]
                sig = W * mN * ((f1 * T1 * d1)[1:].sum() + (f2 * T2 * d2)[1:].sum())
                # payoff tensor in slot-j-first order with pay index: j own, 4 = o1's payoff, 5 = o2's payoff
                Pp = np.zeros((2, len(Q1), len(Q2), 6))
                for a, xx in enumerate((ip, x)):
                    Pp[a, :, :, :3] = Pfull[xx]
                    Pp[a, :, :, 4] = Pfull[xx][..., o1]
                    Pp[a, :, :, 5] = Pfull[xx][..., o2]
                t0 = time.time()
                seed = (hash((arm, pr, j, x)) & 0x7fffffff)
                o = _sim3(Pp, j, 2, len(Q1), len(Q2), f1, f2, 0, 0, N, W, mN, reps, seed)
                k = int(o[0]); n = int(o.sum()); lo, hi = wilson(k, n)
                rows.append(dict(arm=arm, profile=list(pr), occ=n_occ, j=j, resident=int(p), cls_size=len(mem),
                                 variant=int(E[x]), is_resident=bool(x == ip), sigma=float(sig), Nrho=N * k / n,
                                 Nrho_lo=N * lo, Nrho_hi=N * hi, Nrho_asym=asym(sig), fixed=k, lost=int(o[1]),
                                 tester_est=int(o[2]), reps=n, n_testers=[len(Q1) - 1, len(Q2) - 1],
                                 wall=round(time.time() - t0, 1)))
                print(json.dumps(rows[-1]), flush=True)
    return rows


def run_p(reps, N=200, top=10):
    import tbr_p as TP
    d = TP._d(); U = d['U']; mu = d['mu']
    files = sorted(glob.glob(os.path.join(ROOT, 'runs', 'tbr_rows', 'p', '*_1.09*_*.json.gz')))
    occ = Counter(); fields = defaultdict(Counter); mNs = set()
    for f in files:
        rec = json.load(gzip.open(f, 'rt'))
        mNs.add(rec['mN'])
        hold = [c['p'] for c in rec['snaps']['100']['cases']]
        I = len(hold)
        cnt = Counter(hold)
        for h in hold:
            occ[h] += 1
            for q, n in cnt.items():
                fields[h][q] += (n - (1 if q == h else 0)) / (I - 1)
    mN = float(sorted(mNs)[0])
    rows = []
    for p, n_occ in occ.most_common(top):
        E = np.nonzero((U[:, p] == U[p, p]) & (U[p, :] == U[p, p]) & (np.diagonal(U) == U[p, p]))[0]
        F = fields[p]
        Q = sorted(q for q in F if q != p and F[q] > 0)
        f = np.array([F[q] for q in Q]) / n_occ
        ip = int(np.searchsorted(E, p))
        Tq = np.array([TP.sojourn_fd(N, U[q, q], U[q, p], U[p, q], U[p, p])[0] for q in Q])
        keyd = {}
        for x, e in enumerate(E):
            keyd.setdefault(U[e, Q].tobytes() + U[Q, e].tobytes(), []).append(x)
        for key, mem in keyd.items():
            x = mem[0]; e = int(E[x])
            sig = W * mN * float((f * Tq * (U[e, Q] - U[p, Q])).sum()) if len(Q) else 0.0
            types = [p, e] + Q
            Ut = U[np.ix_(types, types)].astype(float)
            # only tester migrants arrive (as the focal slot of T and M, migrants of the resident's own program are
            # switched off); their total rate is mN * sum(f)
            field = np.concatenate([[0.0], [0.0], f])
            t0 = time.time()
            o = _sim1(Ut, len(types), field, N, W, mN * float(f.sum()), reps, hash((p, e)) & 0x7fffffff)
            k = int(o[0]); n = int(o.sum()); lo, hi = wilson(k, n)
            rows.append(dict(arm='P', profile=d['names'][p], occ=n_occ, resident=p, variant=d['names'][e],
                             cls_size=len(mem), is_resident=bool(e == p), sigma=sig, Nrho=N * k / n, Nrho_lo=N * lo,
                             Nrho_hi=N * hi, Nrho_asym=asym(sig), fixed=k, lost=int(o[1]), tester_est=int(o[2]),
                             reps=n, n_testers=len(Q), wall=round(time.time() - t0, 1)))
            print(json.dumps(rows[-1]), flush=True)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('arm', choices=['T', 'M', 'P'])
    ap.add_argument('--reps', type=int, default=40000)
    ap.add_argument('--diverse', action='store_true', help='exploratory: profiles of diverse worlds only (T, M)')
    a = ap.parse_args()
    rows = run_p(a.reps) if a.arm == 'P' else run_tm(a.arm, a.reps, diverse_only=a.diverse)
    with open(os.path.join(OUT, 'stage1b_%s%s.jsonl' % (a.arm, '_diverse' if a.diverse else '')), 'w') as f:
        for r in rows:
            f.write(json.dumps(r) + '\n')


if __name__ == '__main__':
    main()
