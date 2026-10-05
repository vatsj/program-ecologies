# Spec: compatibility among co-seeded establishers, the seed lottery's second condition, 2026-10-05

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-05-compatibility-gpt-6.1-sol.md`) and revised; changes marked [after review]. Committed before launch. To be run by an Opus subagent. Mostly static.

[after review] The asymptotic quantity is the *unresolved incompatibility risk*: the probability that an island co-seeds an incompatible pair, times the probability that selection fails to resolve it. κ alone is not that quantity, and a fixed positive incompatible mass is co-seeded routinely at large N, so the run reports both factors along the (N, I) path and does not claim compatibility is irrelevant from κ.

## Why

NOTATION.md states the seed lottery selects on establishment + *compatibility*: when several establishers are seeded
on one island they must mutually cooperate, or one must win, for the frozen state to be efficient. The one unresolved
island in 1,920 runs (RESULTS "cutoff sensitivity in n") was an anti-coordination rest point between two establishers
that cooperate with each other's class but defect on their own. Compatibility has not been measured as a quantity,
and it is where rival networks would show up on islands.

## Design (static, plus a re-analysis of existing runs)

Over the modal arm at n ∈ {6, 9, 12} (the n = 12 evaluation from `src/seeds_tail.py`):
1. **The establisher compatibility matrix:** for every pair (x, y) of establishers, whether they mutually cooperate,
   mutually defect, or one exploits the other. [after review] Classes are the evaluator's behavioural classes at the
   cutoff (identical rows and columns of the payoff matrix, self-play included), so a within-class encounter plays as
   the diagonal; report within-class and between-class matrices for the heavy set. The **compatibility index**
   κ(n) = P(mutual cooperation | both draws are establishers), with μ_est reported beside it; the exploitation rate on
   the same denominator; and the full pairwise matrix of the heavy establishers (FairBot's pair, the THEM(THEM) pair,
   the probe-readers, PrudentBot), since components are not compatibility (mutual cooperation is not transitive).
2. **Incompatible pairs and their co-seeding probability** [after review: computed, not summed]. List every
   mutually-defecting or exploiting establisher pair; report the missing-edge mass within each component of the
   mutual-cooperation graph; and compute, by 10⁵ multinomial seeds at N = 100 and 400 and by exact calculation where
   feasible, the probability that an island seeds *any* incompatible pair (co-occurrence of both classes), not a sum
   over overlapping pair events. "Non-negligible" is predeclared as a pair co-seeding probability ≥ 0.01 at N = 400.
3. **Anti-coordinators** [after review: object defined]. The observed unresolved island held two *non-establisher*
   classes, each defecting on its own class and cooperating with the other. Identify every pair (x, y) with
   x(y) = y(x) = C and x(x) = y(y) = D (anti-coordinators; by definition not establishers), their mass, and their
   co-seeding probability, as a separate category from establisher incompatibility.
4. **Re-analysis** [after review: selection independent of efficiency]: over the existing seeds-in-n and
   spoiler-conditioned rows (regenerable), select islands by the certification rule alone, and report: unresolved and
   censored counts and the horizon; among certified islands, the fraction with P(C,C) < 0.95 and, separately, the
   fraction not payoff-Pareto-efficient; the fraction whose terminal support holds two or more establisher classes,
   split into mutually-cooperating coexistence and incompatible coexistence; terminal support and extinction order
   for the latter.
5. **Conditioned lottery and pair competitions** [after review]. (a) 400 single islands at N = 400, n = 12, no
   migration, seeded iid from μ conditioned on co-seeding a consequential incompatible pair (co-seeding probability
   ≥ 0.01), with the conditioning-event probability and achieved counts by pair, plus 400 unconditioned iid islands
   as the link to lottery prevalence. (b) For each consequential pair, pair-only competitions (the two classes alone,
   balanced and 3:1 skewed starts, N = 400, 100 runs each) and the same starts embedded in a full-μ background, so
   the interaction pattern (mutually-defecting self-cooperators vs cross-cooperating within-class defectors) is
   tested directly.

## RE predictions (Fable)

1. **κ(n) ≥ 0.9 at every n**, and the heavy establishers form one component except PrudentBot, which defects on the
   probe-readers (they do not provably defect on D's exploiter) and so is mutually defecting with them. *Falsifier:*
   κ(12) < 0.8, or FairBot and a probe-reader in different components.
2. **Incompatible pairs are light, but co-seeding is not negligible** [after review]. The mutually-defecting pair mass
   as a fraction of μ_est² is below 0.05 at every n; the simulated probability that an island of N = 400 co-seeds
   some incompatible establisher pair is 0.1–0.4 (sol is right that N(N−1)/2 opportunities amplify rare pairs; my
   earlier < 0.1 is withdrawn), and it rises with N. *Falsifier:* pair-mass fraction above 0.2, or co-seeding at
   N = 400 above 0.6.
3. **Frozen efficient islands are efficient:** fewer than 1% of frozen cooperative islands in the existing rows have
   P(C,C) < 0.95, and islands with two or more establisher classes in the terminal support have P(C,C) ≥ 0.95 in at
   least 95% of cases. *Falsifier:* more than 5% below 0.95.
4. **Resolution depends on the interaction pattern** [after review: restated]. Mutually-defecting self-cooperators
   have positive frequency dependence: the initially larger class wins in at least 70% of pair-only competitions at
   3:1, and fewer than 10% of conditioned islands freeze polymorphic between them. Cross-cooperating within-class
   defectors (anti-coordinators) have minority advantage and freeze polymorphic in at least 50% of pair-only
   competitions, but they are not establishers and their co-seeding probability is below 0.02 at N = 400. In the
   full-μ background, background programs change the pair-only outcome in fewer than 20% of cases. *Falsifier:* more
   than 25% polymorphic among mutually-defecting establisher pairs in conditioned islands, or the smaller class
   winning at 3:1 in more than 50% of pair-only runs.

**What it would mean.** If 1, 3 and 4 hold, the unresolved incompatibility risk is the product of a co-seeding
probability that grows with N and a resolution-failure probability below 0.1, and it is reported along the (N, I)
path as a bound rather than declared irrelevant; the heavy establishers form one pairwise-compatible network except
PrudentBot. If 1 fails, rival networks exist among establishers at the level of islands, and the I ≫ N path needs a
competition analysis between established islands holding different networks (DEFERRED 1). [after review] High κ may
reflect the grammar, the prior or the free sound oracle rather than a property of realizable readers; the result is
language-relative.

## RS predictions (Jacob)

(Optional.)

## Procedure for the subagent

Follow CLAUDE.md discipline. Commit `predictions/2026-10-05-compatibility.md` carrying the RE predictions before any
computation beyond the published class counts. At most 3 workers; memory is tight, free the n = 12 arrays when not
needed; stop anything projected beyond 2 hours and say so; do not edit RESULTS.md, REJECTED.md, THEORY.md, CLAUDE.md,
DEFERRED.md or NOTATION.md; do not touch `runs/d8dcd7ee9a/row.json`; hand back draft RESULTS, REJECTED, THEORY and
DEFERRED text, at most 5 lines on what matters, and the branch (`git branch --show-current`) and commits.
