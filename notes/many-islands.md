# Islands to infinity before time: coverage of the stable set under rare migration and annealed mutation (notes, 2026-10-25)

Spec `specs/2026-10-25-many-islands.md` (the RS: "send num islands to infinity first … shoot for (2) and tell me if and
where it fails"; reviewed by gemini-4-argon, then gpt-6.1-sol in `--mode amended`; the [after review] text is the
resolution). §1 is written by hand, before any code of this experiment and before any counted cell; §2 (deviations,
choices where the spec is silent, costs) is appended as they arise.

## 1. Hand analysis, before code

### 1.0 Disclosure about order

Nothing was run before this section. I read `src/stable_sets.py` (the island kernel `kern`), `src/dollar3.py` (game,
grammar, evaluators), `src/churn_primary.py` (the E-min reader catalogue) and the RESULTS sections named in the
brief. The one structural fact on which everything below rests (§1.2) is derived on paper from the kernel's code, not
from a run; §2 records how it was tested.

### 1.1 The object, as I will implement it

Everything of the stored lottery is imported unchanged: `dollar3` at N = 100 per slot, w = 0.3, Moran birth-death with
fitness exp(w · expected payoff against one uniformly drawn member of each other slot), the realizable outcome list
(20 outcomes), payoffs in dollar units. Three phases, per island, in this order:

1. *Founding* (ε = 0): the three slot populations are multinomial(N, seed law), as in the stored lottery.
2. *Annealing*: Poisson(A) prior arrivals per island, A ∈ {0, 50, 150}; the arrival times are drawn from the normalized
   intensity (1/t₀)(1 + (t − t₁)/t₀)^(−2) on t ≥ t₁ (inverse CDF: t = t₁ + t₀·u/(1 − u)), so the last arrival is at a
   finite time. An arrival picks a slot uniformly, draws a program from that slot's seed law, and replaces a uniformly
   chosen resident. t₁ = 200 generations (founders have mostly closed locally by then), t₀ = 500 generations. These
   two numbers are mine (the spec leaves them open); they are disclosed and not tuned.
3. *Relaxation to settlement*: after the last arrival the island runs, alone, until every slot is monomorphic
   (cap 20,000 generations). The settled state is the program triple. A slot that has not fixed by the cap is a
   quasi-stationary polymorphism: counted, disclosed, never silently settled; the island then stays in the pool as a
   *polymorphic* island and is excluded from the triple-level chain (its share is reported).

Then rare migration, one event at a time: recipient uniform, donor uniform among the other islands of its component,
slot uniform, migrant = the donor's program in that slot (the donor is settled, so one program), placed in place of a
random resident of the recipient's slot; the recipient runs alone until settled; next event.

### 1.2 The key structure: one migrant into a settled island is a constant-fitness two-type Moran process

A settled island has one program a_s in each slot s. The migrant x enters slot s. Then slots j, k ≠ s remain
monomorphic for the whole relaxation: there is no variation in them for selection (or anything else) to act on, and
ε = 0 means nothing new arrives. Slot s holds two types, resident r = a_s and migrant x. The expected payoff of slot s's
type y against the other slots is the constant π_s(y) = PAY[(y, a_j, a_k), s], because the other slots are
monomorphic. So slot s's dynamics is the two-type Moran process with constant fitness ratio ρ = exp(w · (π_s(x) −
π_s(r))): parent chosen with probability proportional to count × exp(w π), victim uniform. Starting from one migrant:

  P_fix(x) = (1 − 1/ρ)/(1 − ρ^(−N))  (ρ ≠ 1),   P_fix = 1/N  (ρ = 1, i.e. equal payoff, N = 100).

If x fixes the island's triple is (a with a_s := x); otherwise it is a. **The island-state chain is therefore exactly
Markov on program triples with a closed-form one-step kernel**; simulating the relaxation is unnecessary for the
one-migrant chain and is used only to validate the formula (against `stable_sets.kern` run as a one-island kernel; a
test) and for the two-migrant probes, where two slots are polymorphic at once and the closed form does not apply.
Values (dollar units, w = 0.3, N = 100), by the payoff change of the migrant relative to the resident, Δ in sixths:

| Δ (sixths) | −3 | −2 | −1 | 0 | +1 | +2 | +3 | +4 |
|---|---|---|---|---|---|---|---|---|
| P_fix | ≈ 3·10⁻⁸ | ≈ 5·10⁻⁶ | ≈ 3.5·10⁻⁴ | 0.01 | ≈ 0.049 | ≈ 0.095 | ≈ 0.139 | ≈ 0.181 |

(hand arithmetic: ρ = e^(0.05Δ); +1: (1 − 1/1.0513)/(1 − 1.0513^(−100)) ≈ 0.0488/0.9933; deleterious values use
ρ^(−N) large). A neutral migrant is 1% (the "voter" move); a strictly better one by one sixth is five times that;
a worse one by one sixth is thirty times *less* than neutral. Mismatched migrants die in about N ln N ≈ 460 births
(about 5 generations) in practice.

Consequences used below: (i) the cost of one event is two cached joint-evaluator lookups plus one uniform draw
(≈ 10⁻⁷ s) against ≈ 10⁻² s for the simulated relaxation (a doomed lineage lives ≈ 5 generations ≈ 1.5·10³ slot-events,
a fixing one ≈ N² = 10⁴ births), a factor of about 10⁵; (ii) the checkpoints of the spec (up to 1,000 events per
island at I = 4,096, i.e. 4·10⁶ events per run, 10 runs per I) cost seconds per cell instead of days, so I will also
extend the clock far beyond the spec's last checkpoint (labelled as an extension, with the spec's checkpoint scored as
registered); (iii) the costly object is the founding/annealing phase, 10⁴–10⁵ islands per cell.

### 1.3 What a single migrant can and cannot convert in `dollar3` (worked examples)

Notation: slot 0, 1, 2; an action is (partner, demand); (1, ½) means "name slot 1, ask for ½". Payoffs in sixths: fair
pair (3, 3), unequal (4, 2), wasteful (2,2), (2,3), (3,2), grand coalition (2,2,2), disagreement (0,0,0). Resident
programs are constants unless stated.

- **Fair → fair (neutral).** Residents (0: (1,½), 1: (0,½), 2: (0,½)), the pair {0,1} with the excluded slot 2 offering
  ½ to slot 0. A migrant constant (2, ½) in slot 0: slot 0 and slot 2 name each other, slot 1 is now excluded:
  pair {0,2} fair, π_0 unchanged (3), so Δ = 0 and P_fix = 1/N = 1%. This is the "pivot crosses a tie" flip (RESULTS
  "Stable sets on islands": 0.90 of member flips are pure drift). It needs the excluded slot to already offer ½ to the
  pivot, which the excluded slot acquires by *neutral* substitution (any excluded program that does not change play
  gets payoff 0 like the resident: Δ = 0, P_fix = 1%). If the excluded slot instead names slot 1 (not 0), the same
  migrant yields disagreement: Δ = −3, never.
- **Fair → unequal (strictly better, if the excluded slot is meek).** Residents as above but slot 2 = (0, ⅓) ("meek").
  A migrant (2, ⅔) in slot 0: 4 + 2 = 6, pair {0,2} unequal (4, 0, 2), π_0 : 3 → 4, Δ = +1, P_fix ≈ 4.9%.
- **Unequal is absorbing against single migrants except through the excluded slot.** (4, 2, 0): slot 0 dictator
  (1, ⅔), slot 1 (0, ⅓). A migrant in the dictator that asks less loses (Δ = −1, −2); one that asks the same is neutral.
  A migrant in the victim asking more (0, ½) makes 4 + 3 = 7 > 6, disagreement (Δ = −2); asking less (0, ⅓) is neutral.
  The only strict escape is for the victim to switch partner: a migrant (2, ½) in slot 1 forms pair {1,2} fair (0, 3, 3)
  if and only if the excluded slot 2 already names slot 1 at ½: then Δ = +1 (4.9%); otherwise disagreement
  (Δ = −2). A migrant in the dictator naming slot 2 at ⅔ forms (4, 0, 2) iff slot 2 names 0 at ⅓ (neutral, Δ = 0).
  So *both* U → F and F → U go through the excluded slot's content, at the same selection strength (one sixth).
- **Wasteful is a ratchet.** (2, 2, 0): a migrant in slot 0 asking ½ gives (3, 2): Δ = +1 (4.9%); asking ⅔ gives (4, 2):
  Δ = +2 (9.5%). From (3, 2): slot 1 asking ½ gives (3, 3) fair (Δ = +1), slot 0 asking ⅔ gives (4, 2) (Δ = +1). Among
  constant donors the greedy step has the larger fixation probability and equal prior weight, so wasteful pairs run
  toward unequal pairs more often than toward fair pairs (the accommodator ratchet of the earlier divide-the-dollar work).
- **Grand coalition is absorbing against single migrants.** (2,2,2): a migrant naming a person is unmatched (Δ = −2);
  naming ALL with a bigger demand overshoots 6 (Δ = −2); the same play is neutral.
- **Disagreement is not absorbing.** Demand clashes (0 and 1 both ask ⅔ of each other) are cured by a single lower
  demand (Δ = +2 or +3, 9.5–14%). A cyclic naming (0→1→2→0) is cured by a migrant that closes a pair.
- **Readers.** A reader in a slot changes what a migrant elsewhere does *to its own play*: e.g. the switcher
  `if(BOX(THEM_j = (i,½)), (j,½), (k,½))` (name j iff j provably offers me ½, else k): with residents (reader, (i,½),
  (i,½)) it forms pair {i,j}; a migrant j that names k instead sends the reader to k with no loss to the reader, so a
  single migrant converts fair {i,j} → fair {i,k}: Δ for the migrant equals what j earns at {i,k} (zero, it is the
  excluded one now), against π_j = 3 before: **Δ = −3 for the migrant**, so it does not fix. The reader moves the
  *island* only when the migrant's own payoff is not worse: a reader in the excluded slot k that follows the pivot's
  offer keeps the migrant neutral. This is the mismatch argument behind prediction 5's counter-prediction; whether it
  survives the catalogue is an empirical question, and the chain will answer it exactly because the kernel is exact.

Hand summary: single migrants cannot move grand-coalition islands, cannot move unequal islands except via the excluded
slot's pre-existing content, move fair islands to fair or unequal only via the excluded slot's content, and do move
wasteful and disagreement islands. The excluded slot's content is the hidden state of the system, and it evolves by
neutral substitution at 1% per matched event (the voter move). Class-level Markovianity of the outcome-class chain is
therefore expected to fail.

### 1.4 The symmetry argument for the fair-to-fair block of K

Let σ ∈ S₃ permute the slots. `Slots.permute(σ)` gives the induced bijection of programs, p_s : program x of slot s ↦
program of slot σ(s). Three facts:

1. *The founding/arrival law is S₃-invariant.* Each slot's seed law is the image of slot 0's under a slot permutation
   (`dollar3` module docstring), the grammar is closed under the swap of an owner's two others, and the length prior
   is invariant under that swap (it depends on the number of nodes only). So the prior mass of x in slot s equals that
   of p_s(x) in slot σ(s). The Poisson arrival count and times, the arrival slot (uniform) and the victim (uniform) are
   invariant by construction.
2. *The evaluator and the payoffs are label-free.* The joint play of (x₀,x₁,x₂) equals, relabelled, the joint play of
   (p₀x₀, p₁x₁, p₂x₂) placed in the permuted slots; `outcome` finds the unique mutual pair irrespective of order; the
   weak evaluator's atom order is irrelevant (any bottom atom makes the program bottom). The payoff of slot s's program
   equals the payoff of its image in slot σ(s).
3. *Hence the one-event kernel is S₃-equivariant:* P_fix depends only on the payoff difference, the slot is uniform, the
   donor's program is the corresponding image: K(σa, σb → σc) = K(a, b → c).

Therefore the post-annealing law ν of an island's triple satisfies ν = σν, and in the I → ∞ mean-field equation (a smooth
ODE on the finite triple space reachable from ν's support, with a unique solution) the shares are invariant for all
t: **the three fair-pair classes F₀₁, F₀₂, F₁₂ have equal shares at every time, exactly**, and the symmetrized
antisymmetric part of the fair-to-fair block is zero by construction, not by dynamics. Consequences I want on record:

- Coverage in the I → ∞ limit is then *all or nothing*: either every fair pair has positive share or none does. The
  limit can lose coverage only by losing the fair share altogether (into unequal pairs, or grand coalitions, which are
  absorbing against single migrants).
- Symmetry does **not** say the symmetric state is stable. The F→F flows are quadratic in the pair's own marginal
  (the pivot must offer to the excluded slot's offer, and both are drawn from slot marginals that a larger F₀₁ share
  inflates), so a finite pool, whose empirical founding law is asymmetric at order I^(−1/2), may amplify the asymmetry.
  The prediction of a voter model (first loss of a pair at a time ∝ I per island) holds only if the F→F flows are
  linear; with quadratic positive feedback the first loss is at a time ∝ log I. This is what (2a) distinguishes.
- The hypothesis in the spec ("this constrains the averaged kernel only") is correct: composition-conditioned
  transitions are asymmetric; only the ensemble average is symmetric.

**Reader catalogue (E-min main), reflection check by construction.** `reader_forms(s)` builds, for slot s with others
(j, k) in increasing order: Sj/Sk (accept j's resp. k's half offer, else name the other), Zj/Zk (the null-fallback
variants), R2jf, R2jz, R2kf, R2kz (two-partner readers, first partner j or k, fallback stay-with-first f or null z).
The swap j ↔ k maps Sj ↔ Sk, Zj ↔ Zk, R2jf ↔ R2kf, R2jz ↔ R2kz (checked on the tables: R2jf's table is `sj if a0 else
(sk if a1 else sj)` and R2kf's is `sk if a1 else (sj if a0 else sk)`, which are each other's images under (a0, sj) ↔ (a1,
sk)). `law(s)` gives S-weight 0.06 split equally between Sj and Sk, Z-weight 0.06 equally between Zj and Zk, D-weight 0.03
equally over the four R2 forms, and the base prior (symmetric by fact 1) on the rest; so the catalogue is
reflection-symmetric in the other two slots and the S₃ argument applies to the readers arm. The test file checks all
of this numerically (prior mass invariance under every p_s, evaluator equivariance on random triples), not only on paper.
Reflection-symmetry caveat: none found. Asymmetries that remain are finite-sample.

### 1.5 The settlement rule and its price

Ruled by the spec (second review): at ε = 0 a slot is absorbed when monomorphic; an island is settled when all three
slots are; neutral drift is included (the stored kernel's "locally closed" test, which stops when play is identical
across the listed classes, is *not* settlement: classes with identical play keep drifting and the drift is exactly the
hidden-state dynamics). After annealing, the cost is dominated by polymorphic slots' neutral drift: a single neutral
type from frequency ½ needs ≈ N²·ln 2 ≈ 7·10³ births per slot (≈ 70 generations); from a single copy ≈ N·ln N·(1 + …)
births. An island with arrivals pays that for every arrival that survives the first few generations; the typical
arrival is deleterious or mismatched and dies in ≈ 5 generations. Costs, estimated now, to be compared with §2:

| step | estimate |
|---|---|
| founding relaxation of one island (L, A = 0) | 0.05–0.2 s (the stored runs: 64 islands in seconds) |
| annealed island, A = 150 | 1–5× the above times the number of surviving arrivals; first guess 0.5–2 s |
| one chain event | ≈ 10⁻⁷ s (two cached lookups, one random number) |
| one simulated injection (validation, two-migrant probes) | ≈ 10⁻² s |
| a 16,384-island pool, A = 0 | ≈ 15–60 min per process |

### 1.6 What I will predict beyond the spec (written in `predictions/…` as E1, E2, …)

Stated here only as hand reasoning from §1.3–1.4; numbers are in the predictions file.

- The unequal pairs hold a large share of the post-founding pool (founding: 0.417 unequal, 0.281 fair, 0.23 wasteful,
  0.07 disagreement at ε = 0, L) and are nearly absorbing under single migrants; wasteful and disagreement islands drain
  mainly into unequal pairs; fair pairs gain from wasteful and from the excluded-slot route and lose to unequal through
  the meek-excluded-slot route. I expect the fair share in the limit to be within a factor 2 of its founding value either
  way, not near 1.
- The class-level chain is not Markov (E-class): conversion probabilities from U and F vary by an order of magnitude
  across recipients of the same class, according to the excluded slot's content.
- The extended clock shows slow drift of the fair share after the spec's last checkpoint; coverage in the pool Monte Carlo
  is symmetric in expectation, and the loss of a pair in finite I is by symmetry breaking whose time grows slowly in I.
