# Spec: coverage of the stable set with islands → ∞ before time, under rare migration and annealed mutation, 2026-10-25

Status: draft by the RE; reviewed by gemini-4-argon (folded [after review]), then gpt-6.1-sol (`--mode amended`, folded
[after second review]); to be run by a Sonnet subagent. Requested by the RS (2026-10-25), after "Churn among the fair pairs in the primary object":

> "I dislike the idea of transient islands because I want a crisp, well-defined notion of limiting behavior. Another
> proposal to save it: send migration to zero alongside mutation (though probably at a slower rate, since migrants are
> from a more benign distribution than mutants)."
>
> "I thought we still needed rare mutation to re-introduce predators to eat a shadow of unconditional cooperators /
> exploitable PD programs. 2 approaches to save coverage of the stable set: 1) disconnected components 2) send num
> islands to infinity first. I think they're related and (2) feels like the sharper choice deriving a stronger
> statement, so I'd run both but shoot for (2) and tell me if and where it fails? Anything needing several migrants is
> EVENTUALLY lost. This is why we decayed mutants - simultaneous mutations are kinda cursed."

Follows RESULTS "Stable sets on islands", "A migration window for stable sets on islands", "Deriving immigrant
rejection, Step 0", "Churn among the fair pairs in the primary object" and "Annealed mutation". REJECTED.md checked: this
partly re-opens "The migration game (the equilibrium set of ρ − ρᵀ over monomorphic island-states) as the island
model's ε-free object". That entry failed because a finite archipelago absorbs before a time average forms and island
states are polymorphic. The new object differs on both counts: it takes I → ∞ before t → ∞, so the island-state
shares follow deterministic dynamics from the founding law rather than a time average, and it works over islands'
actual settled compositions, not monomorphic classes.

## The object

Three-player majority division (`dollar3`, payoffs in sixths, V\* = the three fair pairs), N = 100 per slot, w = 0.3, the
stable-sets island kernel (`stable_sets.kern`, imported). Three time scales, in this order:

1. **Founding** (ε = 0): each island founded from the seed law, as in the stored lottery.
2. **Annealed mutation** (per island, before migration matters): prior arrivals at a decaying rate with a finite total,
   εN(t) = a·(1 + (t − t₁)/t₀)^(−2) as in "Annealed mutation", then a mutation-free chase until the island settles.
   [After second review] Executable endpoint: the total arrival count is drawn as Poisson(A) and the arrival times
   from the normalized intensity, so the last arrival is at a finite time; then the island relaxes fully (below).
   Arms: none (ε = 0 exactly) and annealed with A ∈ {50, 150} expected arrivals per island.
3. **Rare migration**: one migrant at a time. A migration event picks a recipient island uniformly, a donor island
   uniformly (within the recipient's component), a slot uniformly and a program from the donor's slot population; the
   migrant replaces a random resident of that slot; the recipient runs alone until it settles. [After second review, replacing the first fold] Under
   mN → 0 the interarrival time diverges, so every island relaxes fully between events: at ε = 0 a slot is absorbed
   when it is monomorphic, and an island is settled when all three slots are (neutral drift included). Islands are
   relaxed this way after annealing and the recipient after each event; a 20,000-generation cap marks a quasi-stationary
   polymorphism, which is disclosed with its frequency and continued from its state, never treated as settled
   silently. A settled island's state is then a triple of programs, so the island-state chain is exactly Markov. The next event starts
   only after settlement: this is the mN → 0 limit exactly (the jump chain), not a small finite rate.

**Settled state** of an island: its program triple (or, for a capped polymorphism, its compositions); for statistics,
its outcome class (each fair pair, unequal by pair and direction, wasteful, grand, disagreement) and its exact
efficient-outcome frequency.

## Two routes to I → ∞

**(2a) Event-driven archipelagos** at I ∈ {16, 64, 256, 1,024, 4,096}, one component, [after second review] reported at fixed
migration-clock checkpoints (1, 3, 10, 30, 100, 300, 1,000 events per island), 10 runs per I, coverage with Wilson
intervals; a run ends at the last checkpoint or its budget, which is censoring, not convergence; first-loss times are
right-censored there and reported beside the expected time from the occupancy-weighted exit hazards of K. Islands are pre-settled from steps 1–2, drawn
independently, so the founding phase is shared across I by drawing larger archipelagos as supersets (paired by
construction). Report against events per island (the migration clock).

**(2b) The mean-field limit.** [After review, amended after second review] With islands absorbed to program triples,
the I → ∞ dynamics are the triple-level equation below, which is exact for the rare-migration jump chain; its kernel
is estimated over the triples that occur. Where the occurring triples are too many for that, the estimate is the
pool Monte Carlo ((2a)'s dynamics on a pool of at least 16,384 islands, 5 pools), with convergence in pool size shown
at fixed checkpoints (4,096 / 16,384 / 65,536 where affordable) before any long-time statement; a pool's terminal
state is never identified with lim_t lim_I. An outcome-class ODE is a diagnostic summary only; disagreement with the
triple level is reported as evidence that the outcome class is not Markov. Estimate the one-migrant transition kernel K(a, b → c): the probability that a single
migrant from a donor in settled state b moves a recipient in settled state a to settled state c, by injection
experiments on a pool of settled islands (at least 2,000 islands from steps 1–2; at least 200 injections per occupied
(outcome class of a, outcome class of b) cell, more where conversion is rare; report intervals). As the diagnostic, integrate the
island-share dynamics dx_c/dt = Σ_{a≠c, b} x_a x_b K(a, b → c) − x_c Σ_b x_b (1 − K(c, b → c)) (mass conservation and nonnegativity tested) at outcome-class level from
the post-anneal shares of each arm. Before trusting the class-level ODE, check that K depends on the outcome class and not mainly on the
composition within it (the within-class spread of conversion probabilities across sampled recipients; if it is large,
integrate over a pool of sampled compositions instead, a population-dynamics Monte Carlo with I → ∞ by resampling, and
say so).

The headline is (2b) where (2a) converges to it as I grows; (2a) shows how fast.

**(1) Components** (secondary): C ∈ {4, 16, 64} disconnected components of I/C islands each at I = 1,024, the same
event-driven dynamics within components. Report coverage across components and V\* share against (2).

## Arms

- **L**: the stored L seeds (weak arm, the stable-sets lottery's default).
- **modalPA**: the paired modalPA seeds.
- **readers**: the churn experiment's E-min main catalogue (flexible readers at about 9% of the seed), because readers
  raised the V\* share there (0.89–1.00 at mN ≥ 0.1) and single-migrant conversion of dominated islands may need them.
- Each with annealing none / A = 50 / A = 150. Twelve cells for (2a) at the largest I; all I for L and readers at A = 150
  and none.

## Outputs per cell

- Founding and post-anneal shares of outcome classes (efficiency on islands before migration); the migration arms start
  from the post-anneal law.
- K at class level with intervals; the fair-to-fair block and its antisymmetric part (net flows), and the rates out of
  each dominated class into V\*.
- (2b): limiting shares x(∞) from the post-anneal shares; coverage (all three fair pairs with share above 10⁻³) and the V\*
  share; whether the flow converges, cycles, or is neutral (conserved quantities).
- (2a): V\* share and coverage against events per island for each I; the I at which (2a) is within 0.05 of (2b) by the
  final time; time to the first loss of a fair pair, and its growth with I (a voter model predicts about I).
- (1): coverage across components and V\* share.
- [After review] *Excluded-slot drift:* in the injection experiments, how often an event that leaves the outcome class
  unchanged replaces the excluded slot's modal resident, and whether such islands convert more later.
- [After review] *Two-migrant probe* (diagnostic, not part of the object): K₂, the same injections with two migrants from
  one donor into two different slots at once. If single-migrant K leaves dominated islands while K₂ clears them, the
  efficiency failure is the RS's "several migrants are eventually lost". [After second review] Beside it, two migrants
  in sequence, the second after full relaxation, to separate overlap from cumulative hidden change; and injections
  repeated on triples sampled during migration (at the 10 and 100 checkpoints), not only after annealing.
- For the RS, a plain list of where the statement "with islands → ∞ before time, every island ends efficient and all
  three fair pairs are present" fails, and why.

## Predictions (the RE's; falsifiers in brackets)

1. *Fair pairs are neutral among themselves on average.* The symmetry-averaged antisymmetric part of the fair-to-fair
   block of K is zero within its interval for L and modalPA, by the slot symmetry of the grammar (this constrains the
   averaged kernel only; composition-conditioned transitions may be asymmetric) [a net flow outside the interval in either arm]. For
   readers the same, unless the catalogue breaks reflection symmetry (the notes check this first).
2. *Coverage holds in the I → ∞ limit.* In (2b) all three fair pairs keep positive shares in every arm [some pair's share
   → 0 in (2b) in any arm].
3. *Efficiency fails without readers.* Single migrants from fair islands rarely convert unequal, wasteful or disagreement
   islands (a mismatched migrant dies in about 10 generations), so in (2b) under L at A = 0 the V\* share stays below
   0.6 (founding share about 0.28) [V\* share ≥ 0.9].
4. *Annealing helps efficiency but does not finish it.* Under L, A = 150 raises the post-anneal V\* share by at least 0.1
   over A = 0, and the (2b) limit stays below 0.9 [no rise, or ≥ 0.9].
5. *Readers carry conversion.* With readers at A = 150 the (2b) limit has V\* share ≥ 0.9 with coverage [below 0.9]. This
   is the RE's least certain prediction. *Counter-prediction (gemini-4-argon), registered:* a single reader migrant into
   a dominated island is mismatched against the resident coalition and dies, the churn result needed overlapping
   migrants (mN ≥ 0.1), and V\* stays below 0.75 in (2b) even with readers.
6. *Finite I loses coverage slowly.* In (2a) the time to the first loss of a fair pair grows at least linearly in I
   [sublinear growth]; at I = 4,096 coverage is held in at least 0.9 of runs at the final time [below 0.9].
7. *Components and (2) agree on efficiency.* (1) gives the same V\* share as (2) within 0.05 at every C, and coverage
   across components ≥ 0.9 from C = 16 [disagreement beyond 0.05, or lower coverage]. *Counter-prediction (gpt-6.1-sol),
   registered:* smaller components lose rare conversion-carrying programs sooner, so efficiency depends on component
   size wherever readers or bridges are scarce.

## Required outputs

- `src/many_islands.py` (+ runner, report), importing `stable_sets`, `churn_primary`, `annealed_kern` as needed; no
  existing file edited.
- `tests/test_many_islands.py`: the settlement rule on hand-built islands; one migrant event reproducing `stable_sets.kern`
  draw for draw when run as a one-island kernel; the ODE on a hand-built 3-state K with a known solution; with A = 0 and
  no migration the founding shares reproduce the stored L, mN = 0 cell (fair 0.281 at generation 2,000 within noise).
- `notes/many-islands.md` (§1 before code: the hand predictions for K's fair block from the slot symmetry, the
  settlement rule, the expected cost per event; §2 deviations).
- `predictions/2026-10-25-many-islands.md` before any counted cell, with the RS's messages first.
- `runs/many-islands.md` and `.json`, `runs/many_islands/` (small files).
- Hand back RESULTS, REJECTED, THEORY and NOTATION drafts; do not edit the shared docs.

**Budget and scale guard.** Another subagent may be running: check `ps` and free memory before each batch; at most 3
workers, 2 while another subagent is alive. One job per process; no `multiprocessing.Pool`; one background wait per
batch that exits at completion and fires if the log stops changing for 2 hours; never poll periodically. Cut order
(disclose): I = 4,096 in (2a), modalPA beyond (2b), A = 50, components C = 4.
