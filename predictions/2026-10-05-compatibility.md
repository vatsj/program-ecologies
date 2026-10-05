# Predictions: compatibility among co-seeded establishers (2026-10-05)

Spec: `specs/2026-10-05-compatibility.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-05-compatibility-gpt-6.1-sol.md`).
Code: `src/compatibility.py`. Committed before any computation beyond the published class counts (51 / 863 / 13,514
classes at n = 6 / 9 / 12). Everything here is finite-cell evidence in the modal arm (free sound oracle) at
n ∈ {6, 9, 12}, N ∈ {100, 400}, w = 0.3, ε = 0; it is language-relative and says nothing directly about realizable
source readers.

## Objects and operational choices (predeclared)

- **Classes:** the class data of `src/spoiler_conditioned.py` (`cdata(n)`): the modal language evaluated once at
  n = 12, classes merged within L_n by identical row and column of the play matrix V (self-play included). A
  within-class encounter plays as the diagonal V[x, x]. Masses μ are cutoff-normalized (seeding units).
- **Establisher:** `cdata(n)['est']`: self-cooperates, defects on D, not ALLC. Every establisher self-cooperates, so
  the within-class matrix is mutual cooperation by construction; the between-class matrix is the object.
- **Pair types** for distinct establisher classes x ≠ y: *mutual cooperation* (V[x,y] = V[y,x] = 1), *mutual
  defection* (both 0), *exploitation* (exactly one is 1). *Incompatible* = mutual defection or exploitation.
- **κ(n)** = P(mutual cooperation | two iid draws from μ are both establishers)
  = Σ_{x,y ∈ E} μ_x μ_y [V[x,y] V[y,x] = 1] / μ_est² (x = y included; it counts as mutual cooperation). Reported with
  μ_est, the mutual-defection and exploitation rates on the same denominator, and κ restricted to x ≠ y.
- **Heavy set:** establishers with μ ≥ 10⁻⁴ at the cutoff (the 8 spoiler-conditioned targets), plus PrudentBot
  `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` wherever it is a class, plus FairBot's pair, the THEM(THEM) pair and the
  probe-readers by name. Full pairwise matrix reported.
- **Components:** connected components of the mutual-cooperation graph on all establishers; missing-edge mass within
  a component C = Σ_{x<y ∈ C, not mutually cooperating} μ_x μ_y, also as a fraction of μ(C)².
- **Pair co-seeding probability** (exact, multinomial, N draws): P(x and y both present)
  = 1 − (1−μ_x)^N − (1−μ_y)^N + (1−μ_x−μ_y)^N. **Consequential** = pair co-seeding probability ≥ 0.01 at N = 400
  (the spec's predeclared "non-negligible").
- **P(any incompatible pair co-seeded):** 10⁵ multinomial seeds at each (n, N), N ∈ {100, 400}, fixed RNG seeds; an
  island counts if two distinct establisher classes present form an incompatible pair. Exact by inclusion–exclusion
  over present subsets, restricted to the heavy set (a lower bound on the full quantity; the simulated restriction to
  the heavy set is reported beside it as a check).
- **Anti-coordinators:** pairs of distinct classes (any classes) with V[x,y] = V[y,x] = 1 and V[x,x] = V[y,y] = 0.
  Reported: count, pair mass Σ μ_x μ_y, the exact pair co-seeding probabilities, and the simulated probability of any
  anti-coordinator pair co-seeded, split by the pair's play against D (both defect on D / otherwise).
- **Re-analysis rows:** `runs/seeds-in-n.json` (1,920 runs, n = 6–9, I ≥ 4), `runs/seeds-tail-rows.json` (520 runs,
  n = 12), `runs/spoiler-conditioned-rows-nat.json.gz` (24,000 single islands, n ∈ {6, 9, 12}, N ∈ {100, 400});
  the natural spoiler rows are regenerated with `spoiler_conditioned.nat_job` (deterministic) where the stored
  top-6 support is incomplete. **Certification rule alone:** an island is *certified* if its run stopped with status
  certified-frozen, certified-separated or local-frozen; *metastable* and *unresolved* are counted and excluded from
  denominators; the horizon is 10⁵ generations. **P(C,C) < 0.95** and **payoff-Pareto inefficiency** are reported
  separately: an island is *Pareto-inefficient* iff some pair of distinct present individuals mutually defects (D,D is
  the only Pareto-dominated outcome of the PD; exploitation is Pareto-efficient but has low P(C,C)). For runs with
  migration the unit is the island, using its terminal support where stored, and the run otherwise.
- **Conditioned lottery (5a):** n = 12, N = 400, single islands, no migration, horizon 10⁵ generations, the
  spoiler-conditioned kernel. Seeds are iid multinomial from μ, accepted iff they co-seed at least one consequential
  incompatible establisher pair (rejection sampling; the acceptance rate is the conditioning-event probability). 400
  accepted islands plus 400 unconditioned islands (separate salt). Per island: certified/unresolved, terminal support,
  the fate of each co-seeded consequential pair (x wins, y wins, both survive, neither), extinction order.
  *Polymorphic between a pair* = both classes in the terminal support.
- **Pair competitions (5b):** for every consequential incompatible establisher pair, every anti-coordinator pair with
  co-seeding ≥ 0.01 at N = 400, and in any case the heaviest anti-coordinator pair and the pair of the observed
  unresolved island (capped at 12 pairs by co-seeding probability, stated if the cap binds). Pair-only: N = 400,
  starts 200:200, 300:100 and 100:300, 100 runs each. Background: 200 slots iid from μ plus the pair at 100:100,
  150:50 and 50:150, 100 runs each. Outcome categories: x only, y only, both, neither. "Background changes the
  outcome" is the total-variation distance between the pair-only and background outcome distributions at the same
  ratio; "changes in fewer than 20% of cases" means TV < 0.2. "Initially larger class wins" = the larger survives and
  the smaller does not.
- **Administrative cap:** any stage projected beyond ~2 hours on 3 workers is stopped and recorded as administratively
  censored.

## RE predictions (Fable, copied from the spec)

1. **κ(n) ≥ 0.9 at every n**, and the heavy establishers form one component except PrudentBot, which defects on the
   probe-readers (they do not provably defect on D's exploiter) and so is mutually defecting with them.
   *Falsifier:* κ(12) < 0.8, or FairBot and a probe-reader in different components. (0.8 ≤ κ(12) < 0.9 at some n is
   inconclusive for the first clause.)
2. **Incompatible pairs are light, but co-seeding is not negligible.** The mutually-defecting pair mass as a fraction
   of μ_est² is below 0.05 at every n; the simulated probability that an island of N = 400 co-seeds some incompatible
   establisher pair is 0.1–0.4, and it rises with N. *Falsifier:* pair-mass fraction above 0.2, or co-seeding at
   N = 400 above 0.6. (Values between the held band and the falsifier are inconclusive.)
3. **Frozen efficient islands are efficient:** fewer than 1% of frozen cooperative islands in the existing rows have
   P(C,C) < 0.95, and islands with two or more establisher classes in the terminal support have P(C,C) ≥ 0.95 in at
   least 95% of cases. *Falsifier:* more than 5% below 0.95. (Judged on certified islands; "frozen cooperative" =
   certified with every present class self-cooperating and not ALLC-only.)
4. **Resolution depends on the interaction pattern.** Mutually-defecting self-cooperators have positive frequency
   dependence: the initially larger class wins in at least 70% of pair-only competitions at 3:1, and fewer than 10% of
   conditioned islands freeze polymorphic between them. Anti-coordinators have minority advantage and freeze
   polymorphic in at least 50% of pair-only competitions, but they are not establishers and their co-seeding
   probability is below 0.02 at N = 400. In the full-μ background, background programs change the pair-only outcome
   in fewer than 20% of cases. *Falsifier:* more than 25% polymorphic among mutually-defecting establisher pairs in
   conditioned islands, or the smaller class winning at 3:1 in more than 50% of pair-only runs.

Clauses are marked separately (held / failed / inconclusive); a numbered prediction holds only if every clause holds.

## RS predictions (Jacob)

None given.
