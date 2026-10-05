# Predictions: proof-carrying contracts v1, 2026-10-04

Spec: `specs/2026-10-04-proof-carrying-contracts.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-04-proof-carrying-contracts-gpt-6.1-sol.md`).
Committed before the validity matrix, the certified-implication test and any run. Measured so far: language sizes and the
contract-alphabet size only. Every conclusion is a finite-size mechanism result.

## Measured before commit

- Sources: modal language at n = 8 (all four box kinds), 19,544 programs, 610 canonical functions, 471 behavioural classes
  of the free game, free GL stable by world 7.
- Contract alphabet: |C| = 471 (one contract per behavioural class of the free game; see "Semantics" for why). 14 stable
  rows are shared by 42 classes whose columns differ (policy duplicates); they stay distinct contracts.
- Truth-table reading is paradoxical, measured: iterating the all-carrier table T[p, q] = act_p(T) synchronously from
  the GL play cycles with period 4, and 58,996 of 372,100 entries keep varying. Example: FairBot's table against the
  anti-FairBot `BOXD(THEM(ME))` must satisfy T[FB, q] = T[q, FB] and T[q, FB] = not T[FB, q].

## Semantics fixed before the run (implementation choices the spec leaves open)

1. **A contract is read through GL** (spec: "contract-level statements are provability atoms"). Contracts are the
   behavioural classes of the free game, each represented by its shortest source, which serves as its canonical proof.
   A box atom answered from contracts, BOX_L(u plays C against tau) with u and tau both carriers, is the free-GL stable
   box over the representatives, hc[L, rep(c_u), rep(c_tau)]; BOXD likewise. Contract reads are ungated: checking is
   cheap, which is the α = 1 amortized path (THEORY §9.2). A consequence: among carriers, play is the free modal game
   between canonical representatives, so the premise of prediction 1 ("a signature carries everything a modal reader
   uses") holds by construction for each source's own contract. The content is in mixed encounters, invalid sources,
   validity breadth and the dynamics.
2. **The 'none' entry is unspecified.** A question a contract would answer about play against a contract-less opponent is
   read from the carrier's source, through the gate.
3. **Literal arguments** THEM(^A): when the opponent u carries a contract, the target is the carrier (A, class(A)), a
   question to u's contract; when u carries none, the target is the bare source (A, none). The contract-free world is then
   exactly the bounded source game.
4. **Gate:** v(x, y) = k(y)·(1 + settle(y, x)) from the current play (semantic stabilization, not proof length); bounded
   box = free box masked by v > b; joint fixed point iterated from the ungated play; rounds and cycles reported. Constants
   cost 0. Implemented here from the sibling spec's definition, not from the sibling's code.
5. **Births:** a uniformly random agent dies; the parent is drawn ∝ exp(w·fitness) (fitness = mean payoff against the
   other N − 1). With probability ε the child's source is redrawn from μ (over canonical sources). Its contract is then,
   with probability s, the new source's own signature (if that pair is valid); otherwise the parent's contract if valid
   for the new source, else none. Then, with probability σ, a donor is drawn (∝ exp(w·fitness), or uniformly in the
   uniform-donor control) and its contract is copied if valid for the child's source; a donor with no contract is a
   no-op (counted). Accepted and rejected swaps are counted by contract.
6. **Neutral label:** every agent also carries a label, initialized equal to its contract (or none), inherited with the
   source, set to the new source's own signature with probability s at mutation (no validity filter), and copied from an
   independently drawn donor with the same law at probability σ (no validity filter). It has no behavioural effect. It
   runs inside every run.
7. **Starts.** (a) *all-D start:* every source is D; a fraction f₀ of agents is replaced by carriers whose source is drawn
   from μ (restricted to sources whose own pair is valid) and who carry their own signature. At f₀ = 1 this has no D.
   (b) *μ seed:* every source iid from μ; each agent carries its own signature with probability f₀ (if valid).
8. **Grid:** b ∈ {2, 4, ∞} × s ∈ {0, 1} × f₀ ∈ {0, 0.01, 1} × σ ∈ {0, 0.1, 1}; the cells s = 0, f₀ = 0 are run once (σ = 0)
   per b as the no-contract control. 3 seeds × 2 starts. ε = 10⁻³ per birth, PD, w = 0.3, 10⁵ generations (N births each),
   samples every 20 generations, statistics over the second half. Uniform-donor control: σ = 1, all b, s ∈ {0, 1},
   f₀ ∈ {0.01, 1}, μ seed. N path: (b = 2, s = 0, f₀ = 0.01) at σ ∈ {0, 1}, N ∈ {1,600, 6,400, 25,600}, μ seed.
9. **Definitions.** FairBot-contract = class of `BOX(THEM(ME))`; P*-contract = class of
   `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))`; a *tag* = a contract whose stable action is C against exactly one contract,
   itself. *Carrying mass* of a contract = its share of carriers. *Cooperative mass* = agents whose type self-cooperates.
   *Source-ALLC load* = agents with source C / cooperative mass; *contract-ALLC load* = agents carrying the all-C contract /
   cooperative mass. "Concentration" of contracts or labels = the largest share among carriers (labels: among labelled
   agents), second half.
10. **Lottery:** ε = 0 (s is irrelevant), complete island graph, mN = 1, iid μ seeding with each agent carrying its own
    signature with probability f₀; 40 runs per cell, Wilson intervals; horizon 10⁵ generations; a run stops when every
    type reachable by swapping (present sources × present contracts, valid pairs) is pairwise payoff-identical, or the
    population is monomorphic with every cross-island migrant strictly disadvantaged. Free-arm baseline: b = ∞, f₀ = 0 at
    n = 8 (the n = 6 numbers in RESULTS do not transfer). Bounded no-contract arm b = 2, f₀ = 0 also run.
11. **Censoring:** any cell projected beyond about 2 hours of wall time is stopped and recorded as censored.

## RE predictions (Fable), from the spec, verbatim in substance

1. **Contracts restore legibility, where they are behaviourally matched.** At b = 2 with f₀ = 0, s = 0 (no contracts
   ever) the well-mixed run is below 0.3; with f₀ = 1 it is within 0.1 of the unbounded-reader-with-contracts baseline,
   which is itself within 0.05 of the source oracle (≈ 0.99 from E3). *Falsifier:* b = 2, f₀ = 1 below 0.6, or the
   contract-evaluator baseline more than 0.1 below the source oracle.
2. **Under swapping the FairBot-contract wins, and the uniform-donor control shows whether it is breadth or fitness.**
   With σ = 1 and payoff-weighted donors, the FairBot-contract holds ≥ 0.6 of carrying mass in the second half and the
   P*-contract < 0.1; with uniform donors the FairBot-contract still holds ≥ 0.5 (breadth rather than donor fitness).
   With σ = 0 the composition tracks the prior mass of the carrying sources. *Falsifier:* P*-contract or a tag above the
   FairBot-contract at σ = 1, payoff-weighted.
3. **Swapping spreads a contract from a small seed.** At (b = 2, s = 0, f₀ = 0.01): σ = 1 reaches second-half P(C,C)
   ≥ 0.8 at N = 6,400 and σ = 0 stays below 0.3. Along the N path the σ = 1 value does not fall with N. *Falsifier:*
   σ = 1 below 0.6 at the key cell, or falling by more than 0.2 from N = 1,600 to 25,600.
4. **Source-ALLC and contract-ALLC loads.** Source-ALLC load inside the cooperative mass is 0.2–0.35 at every σ; the
   contract-ALLC load coincides with it when f₀ = 1 and diverges when f₀ < 1. *Falsifier:* source-ALLC load below 0.1 at
   b = ∞.
5. **Seeding lottery:** with f₀ = 1 the efficient fractions at b = 2 are within 0.15 of the free arm's at every cell; with
   f₀ = 0.01, σ = 0 at b = 2 they are at least 0.3 lower at the I = 4 cells; σ = 1 restores them to within 0.15.
   *Falsifier:* f₀ = 1, b = 2 more than 0.15 below the free arm at any cell.
6. **Neutral-label control:** under σ = 1 the neutral label does not concentrate on any label beyond 0.4; the
   FairBot-contract's concentration in 2 exceeds the neutral label's by at least 0.2. *Falsifier:* the neutral label
   concentrating as strongly as the FairBot-contract.

Where the starts differ, predictions 1–4 are scored on the μ seed (the all-D start with s = 0 cannot produce a
cooperative contract except through the f₀ seed); the all-D start is reported beside it.

## RS predictions (Jacob)

From the pitch: with a rich enough contract set this limits to the free-proof case; the one unfit component is the
program that defects on anyone whose cooperation it can prove, and he predicts it does poorly.

Scored as: (RS-a) at f₀ = 1 the contract arm is within 0.05 of the free arm (b = ∞, no contracts) at every b;
(RS-b) the anti-provers, defined as sources with a `BOX(THEM(ME))` or `BOX1(THEM(ME))` atom whose truth table is D
whenever that atom is true (e.g. `not(BOX(THEM(ME)))`), hold < 0.01 of the population in every cell, second half.

## Addendum (subagent, 2026-10-04, after the static map and before any run result): a supplementary b = 0 arm

Reason: the static map shows the gate is nearly inert at b = 2 under the settle proxy as implemented
(v(FairBot, FairBot) = 1·(1 + 0) = 1, since FairBot's atom against itself never changes; the prover network FairBot,
`BOX1(THEM(ME))`, `BOX(THEM(THEM))`, `BOX1(THEM(THEM))` stays mutually legible; masked μ×μ share 0.0005 at b = 4 and 0.018
at b = 2). FairBot first fails to self-cooperate as a non-carrier at b = 0, where only constants are legible (masked share
0.067; the self-cooperating non-carriers are C and `not(BOX…)` programs, whose masked boxes read false). So the question
"do contracts restore cooperation a gate removed" is only posed at b = 0. Supplementary cells, μ seed, 3 seeds, same
settings: s ∈ {0, 1} × f₀ ∈ {0, 0.01, 1} × σ ∈ {0, 1} (s = 0, f₀ = 0 once), and the lottery at b = 0 for the same
(f₀, σ) configurations. These cells are not in the spec and are labelled supplementary.

Subagent predictions for the supplement:
- S1. b = 0, s = 0, f₀ = 0: P(C,C) < 0.3 (no prover can read a prover).
- S2. b = 0, s = 1: within 0.1 of the b = ∞, s = 1 cell with the same f₀ and σ (search gives every mutant prover its
  contract, and contract reads are ungated).
- S3. b = 0, s = 0, f₀ = 1, σ = 0: P(C,C) ≥ 0.8. The carrier sea is kept by inheritance; non-carrier prover mutants are
  illegible to carriers and play D against them, so they are deleterious.
- S4. b = 0, s = 0, f₀ = 0.01 from the μ seed: < 0.3 at both σ = 0 and σ = 1. The seed holds about 64 carriers, of which
  about 1.3 are expected to be provers, so there is almost nothing to copy.
- Falsifier for the reading "contracts restore what the gate removed": S3 below 0.6 or S2 more than 0.2 below its b = ∞ twin.
