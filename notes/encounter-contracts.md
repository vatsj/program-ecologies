# Contracts that form in encounters, with the responders' programs answering (notes, 2026-10-25)

Spec `specs/2026-10-25-encounter-contracts.md` (the RS: contracts are situation-keyed overrides that "trigger on the
rare special cases where they apply", formed when every member of a coalition does strictly better after the
responders' programs answer; reviewed by gemini-4-argon, then gpt-6.1-sol, with three addenda each; the [after review]
text is authoritative). §1 is written by hand before any code of this experiment and before any counted cell; §2
(deviations, choices where the spec is silent, costs) is appended as they arise.

## 1. Hand analysis, before code

### 1.0 Disclosure about order

Nothing of this experiment was run before this section. I read the spec and its eight reviews, the RESULTS sections
named in the brief ("Islands to infinity before time", "Deriving immigrant rejection, Step 0", "Churn among the fair
pairs in the primary object", "Hooks follow-ups in the weak wing", "Every behavioural predicate as a hook key"), and
the sources `src/dollar3.py`, `src/many_islands.py` (kernel, jump chain), and skimmed `src/stable_sets.py`. The numbers
below come from the fixation formula of `notes/many-islands.md` §1.2 (with its §2.1 correction) and from hand
arithmetic on the game; none from a run of contracts.

Notation. Slots 0, 1, 2. An action is (partner, demand), written (j, d) with demand in {⅓, ½, ⅔}; payoffs in sixths
(⅓ = 2, ½ = 3, ⅔ = 4). A pair forms if two slots name each other and the demands sum to at most 1; the fair pair is
(3, 3), the unequal pair (4, 2), the wasteful pairs (2, 2), (2, 3), (3, 2); everyone gets 0 otherwise (disagreement).
Programs in the weak arm are tables over up to two simulation atoms "slot j plays a in this encounter", evaluated as
the least fixed point of the three programs (a slot that stays bottom plays the null action (ALL, ⅔)).

### 1.1 The two-stage evaluation, as I will implement it

An individual is a program together with an ordered list of at most 8 contract entries (key p, fill a), p a full
action profile (a₀, a₁, a₂) of the encounter as the three programs play it without overrides, a a single local action
of the carrier. The type of an individual is (slot, program, entry list); offspring inherit the whole type, so contracts
are heritable and a mutant is an individual whose list changed.

The encounter of three individuals (types t₀, t₁, t₂):

1. *Stage 1.* Play the three programs, ignoring every entry: profile p = (a₀, a₁, a₂) (least fixed point).
2. *Carriers.* Slot s is a carrier if its type has an entry with key p; its fill f_s replaces its action.
3. *Stage 2.* The carriers' actions are fixed at their fills. Every non-carrier slot re-runs its program in which the
   atoms about a carrier read the fill (a behavioural substitution at every depth) and the atoms about the other
   non-carriers are resolved by the least fixed point as in stage 1. The outcome is the stage-2 profile.
4. If there are no carriers stage 2 equals stage 1. Because fills are written into entries whose key was the profile of
   programs, a carrier whose key does not match the encounter's p plays its program. A contract therefore changes the
   outcome only in the situation in which it was written, which is what "doesn't hinder the program elsewhere" asks.

Fitness is exp(w · expected stage-2 payoff of the type against uniformly drawn members of the other two slots), exactly
the kernel of the stored islands; for ν = 0 (no genesis) the type of every individual is its bare program and the
process is arm 0.

Genesis at rate ν per island per generation: draw one individual from each slot (the encounter triple), draw a coalition
S from the seven nonempty subsets, draw a new profile for S uniformly among the 9^|S| − 1 that differ from S's stage-2
actions. Members of S play their proposal; complement members carrying an entry for p play their fills; the remaining
complement members respond (stage 2 against the fixed actions). If every member of S earns strictly more than its
stage-2 payoff with the contracts already in force, each member individual acquires the entry (p, new action), replacing
any entry of its own with key p. Nothing else changes; genesis never touches a whole slot.

The proposal law is not uniform over useful proposals: of the 7 coalitions and 9^|S| − 1 profiles, the share that
Pareto-improves anything is small. That is why the rejection cost matters for the budget (§1.8) and why the examples
below pick the one proposal that is accepted.

### 1.2 Worked genesis, fair island

Residents (all constants): slot 0 (1, ½), slot 1 (0, ½), slot 2 (0, ½). Profile p_F = ((1,½), (0,½), (0,½)), outcome
fair pair {0, 1}, payoffs (3, 3, 0). The excluded slot 2 offers ½ to slot 0, which makes the island a "pivot-ties"
island (notes/many-islands §1.3).

Every coalition and every proposal against constant responders:

- S = {0}: any new action of slot 0 other than (1,½) either does not name slot 1 (then no pair: 0 < 3, except (2,½) which
  pairs with slot 2's (0,½) for exactly (3, 0, 3): slot 0 gets 3, not strictly more) or names slot 1 with a different
  demand ((1,⅓): wasteful pair, 2 < 3; (1,⅔): 4 + 3 = 7 > 6, disagreement, 0). Rejected.
- S = {1}: symmetric; slot 1 cannot improve on 3. Rejected.
- S = {2}: slot 2 earns 0 now; it needs a partner who names it: neither 0 nor 1 does (constants). Rejected.
- S = {0, 1}: the pair is already (3, 3); to give both strictly more than 3 the demands would sum above 6. Rejected.
- S = {0, 2}: (2, ⅔) and (0, ⅓) would give (4, 0, 2) and slot 0 gets 4 > 3, slot 2 gets 2 > 0, but slot 1 as a *constant*
  responder keeps naming 0 and slot 0 no longer names it; there is no problem for the pair {0, 2}: it forms, because
  slot 0 names 2 and slot 2 names 0 with 4 + 2 = 6. ACCEPTED even against constants (slot 1's loss is not tested).
  Contract: key p_F, fills 0 → (2,⅔), 2 → (0,⅓).
- S = {1, 2}: (2, ⅔) and (1, ⅓): likewise accepted, slot 1 gets 4 > 3 and slot 2 gets 2 > 0.
- S = {0, 1, 2}: a grand coalition at thirds gives (2, 2, 2): slot 0 earns 2 < 3. Rejected.

So even a fair island of constants admits (two) accepted contracts, both of the same shape: the excluded slot and one
member of the pair strictly gain at the expense of the other member of the pair, whom nobody asked. The test is the
Pareto improvement of the signers only. A genesis draw picks a coalition with probability 1/7 and one of the 9^|S| − 1
profiles on it (8, 80, 728 for |S| = 1, 2, 3) uniformly, so each of the two accepted proposals has probability
(1/7)(1/80) and a draw finds one with probability 2/560 = 3.6·10⁻³. With ν = 1 an island makes one such discovery
every 280 generations; at ν = 0.1 every 2,800.

What happens to the contract after it forms? Take S = {0, 2} (slot 0 carrier, slot 2 carrier), one individual each.
The individuals' fitnesses, by the expected-payoff rule:

- A slot-0 carrier meets slot 1 (non-carrier, constant (0,½), names 0) and a slot-2 individual. Stage 1 profile is p_F, so
  the carrier fires: it plays (2,⅔). If the slot-2 individual is a carrier it plays (0,⅓): pair {0,2}, 4 + 2 = 6, the
  carrier earns 4. If the slot-2 individual is a non-carrier it plays (0,½): 4 + 3 = 7 > 6, disagreement, 0. With c₂ the
  carrier fraction in slot 2, a slot-0 carrier's payoff is 4 c₂. A slot-0 non-carrier earns 3 whatever slot 2 does
  (the pair {0,1} does not involve slot 2). Slot 1's payoff falls to 3 (1 − c₀) as slot-0 carriers spread (they stop
  naming it).
- A slot-2 carrier plays (0,⅓) against the slot-0 individual: if a carrier, 2; otherwise slot 0 names 1, no pair, 0.
  Its payoff is 2 c₀. A slot-2 non-carrier earns 0.

Hence the two halves are of different kinds: the slot-2 half is weakly advantageous (payoff difference +2 c₀ ≥ 0, neutral
at c₀ = 0); the slot-0 half is *underdominant* (4 c₂ − 3, negative until c₂ > ¾). This is the coordination barrier in
its smallest case (§1.5).

### 1.3 Worked genesis, unequal island

Residents slot 0 (1, ⅔) (dictator), slot 1 (0, ⅓) (victim), slot 2 (0, ½) (excluded, offers ½ to slot 0, which is
ignored). Payoffs (4, 2, 0). Profile p_U.

- S = {1, 2}: slot 1 proposes (2, ½), slot 2 proposes (1, ½): the pair {1, 2} forms fair, payoffs (0, 3, 3); slot 1 gains
  (2 → 3), slot 2 gains (0 → 3); slot 0 as a constant responder keeps naming slot 1 and is simply not matched. ACCEPTED. 
- S = {1}: (2, ½) alone: slot 2 names 0, so no pair: 0 < 2. Rejected. S = {2}: (1, ½) alone: slot 1 names 0: no pair.
  Rejected. S = {0}: gets 4 now, the maximum. Rejected. S = {0, 1} or {0, 2}: slot 0 has nothing to gain. Rejected.
- With a *reader* in slot 2 (name whoever offers me ½; otherwise stay): S = {1}, proposal (2, ½) is accepted even alone:
  the responder re-reads slot 1's fill and answers (1, ½), pair {1, 2} fair (0, 3, 3); slot 1 gains. This is the
  case the RS calls out: the answer is part of the test. Against the constant responder the same proposal needs
  slot 2's cooperation in the contract; against the reader it does not.

Fate of the S = {1, 2} contract: slot-1 carrier earns 3 c₂ (against slot-2 carriers) and 0 otherwise (slot 2 names 0,
slot 0 names 1 but slot 1 names 2, nothing matches), versus the non-carrier's 2: underdominant with threshold c₂ > ⅔.
The slot-2 carrier earns 3 c₁ against a non-carrier's 0: advantage 3 c₁ ≥ 0, neutral at c₁ = 0. Again one neutral
half and one underdominant half. With the reader in slot 2 the slot-1 carrier earns 3 always (singleton-compatible),
advantage +1 sixth, fixation probability about 4.9 % (the table of many-islands §1.2).

### 1.4 Worked genesis, wasteful and disagreement islands

*Wasteful.* Residents slot 0 (1, ⅓), slot 1 (0, ⅓), slot 2 (0, ⅓): pair {0, 1} wasteful, (2, 2, 0).

- S = {0}: (1, ½) vs slot 1's (0, ⅓): 3 + 2 = 5 ≤ 6, wasteful pair (3, 2): slot 0 gains 2 → 3. ACCEPTED alone, against a
  constant responder (slot 1's payoff is not changed: 2 → 2). Also (1, ⅔): 4 + 2 = 6: unequal (4, 2): gains 2 → 4. ACCEPTED.
  Singleton contracts with advantage +1 and +2 sixths at every frequency: fixation probabilities 4.9 % and 9.5 % per carrier.
- S = {1}: (0, ½) or (0, ⅔) likewise accepted (slot 0 constant names 1 at ⅓).
- S = {0, 1}: (1, ½) and (0, ½): fair (3, 3): both gain. ACCEPTED, also reached by two successive singleton steps.
- So wasteful islands are quickly clear of singleton moves: a greedy step has twice the selection of a fair step and both are
  proposed with equal probability, the accommodator ratchet of "Divide-the-dollar" reappears as contracts, towards
  unequal pairs. I expect wasteful islands to convert, and to convert mostly to unequal.

*Disagreement.* Residents slot 0 (1, ⅔), slot 1 (0, ⅔), slot 2 (1, ½): the clash 4 + 4 = 8 > 6 for the pair {0, 1}, no other
match: payoffs (0, 0, 0). Profile p_D.

- S = {0}: (1, ½) vs slot 1's (0, ⅔): 3 + 4 = 7, disagreement. Rejected. (1, ⅓): 2 + 4 = 6 pair {0, 1}: (2, 4): slot 0
  gains 0 → 2 and is accepted alone. S = {1}: (0, ⅓) vs slot 0's (1, ⅔): 4 + 2 = 6: accepted.
- Each of these singleton contracts has advantage +2 sixths for the carrier at every frequency of the other slot's
  carriers (the partner is a constant): 9.5 % fixation.
- So disagreement islands are the easiest to convert: the target of the Pareto test is the zero payoff.
  *Mismatched migrant (the spec's test).* Take the fair island of §1.2 and suppose a migrant constant (2, ½) arrives in
  slot 1 (names slot 2, whose resident names slot 0): every encounter of the migrant has profile p_M = ((1,½), (2,½), (0,½)),
  all earn 0 (nobody matched), and its lineage dies in ≈ 5 generations (Δ = −3, fixation ≈ 5·10⁻⁸). A genesis draw
  samples the migrant with probability 1/N = 1 % (slot 1), selects the coalition S = {1} with probability 1/7 and the
  proposal (0, ½) among the 8 alternatives with probability 1/8: S = {1} playing (0, ½) restores the pair {0, 1},
  payoff 0 → 3, strictly, and is ACCEPTED: the migrant is repaired and becomes neutral (a 1 % lineage). The rate of that per
  generation is ν · 0.01 · (1/7)(1/8) = 1.8·10⁻⁴ ν, so over the migrant's life of ≈ 5 generations the repair probability is
  about 10⁻³ ν. At ν = 0.1 it is 10⁻⁴: unsampled, not impossible; at ν = 1 an order of magnitude more, still rare.
  The spec's remark (ν = 1 separates "cannot form" from "was not sampled") is right, and migrant-encounter genesis has to
  be reported conditionally.

### 1.5 The coordination barrier

*Claim.* A contract that makes its signers better off only if the other signer's slot also carries the fill spreads from
its signers' one copy only if each signer's payoff is non-decreasing in the partner slot's fill frequency and the
signer's alternative payoff is zero; otherwise it is underdominant in its slot and its fixation probability is
exponentially small in N.

*Derivation.* Let a signer i in slot s have, without a contract, payoff u₀ (the island's outcome for that slot). With the
contract, its payoff is u_a (the accepted improvement) when the other signer's slot j plays its fill and u_m when it does
not (the mismatch outcome: the carrier plays the fill, the partner does not follow). With c the fraction of carriers in
slot j (assume the responders' behaviour is the same in both cases), the carrier's advantage over the non-carrier is
Δ(c) = c u_a + (1 − c) u_m − u₀. At c = 1/N, Δ ≈ u_m − u₀ + (u_a − u_m)/N.

- If u_m = u₀ (a zero-payoff signer in both worlds: the excluded slot, or the clash in a disagreement island) then Δ(c) =
  c (u_a − u₀) ≥ 0: neutral at c = 0 and increasing; the half spreads by drift at 1/N and then by selection.
- If u_m < u₀ (a signer who gives up a positive payoff: a pair member moving to a new partner) then Δ < 0 for c below
  the threshold θ = (u₀ − u_m)/(u_a − u_m). For the fair-island contract of §1.2, slot 0's half has u₀ = 3, u_m = 0, u_a = 4:
  θ = ¾. For slot 1's half in §1.3, u₀ = 2, u_m = 0, u_a = 3: θ = ⅔.
- At the observed one-copy start, Δ ≈ −3 sixths (−0.5 dollars), so in the two-type Moran process with ρ = e^(−0.15),
  fixation is ≈ 5·10⁻⁸ (many-islands table); the half dies in about 5 generations. The contract is not the cause
  of its own disappearance: it is the neutral, positive half in the *other* slot that has to drift to c > θ first, with
  probability of order 1/N, and the underdominant half then has to be created *again* by a later genesis event while c is above θ,
  and fixes then with the 4.9 % of a +1 sixth advantage.

*What follows (the predictions' basis).* (i) Contracts formed on dominated islands in which a signer's alternative is 0
(wasteful/disagreement island, the excluded slot) are neutral or advantageous halves and spread; (ii) contracts formed on
V* islands move a pair member off a positive payoff and are selected out, unless the responder's reader accepts the fill
(§1.3, the reader case, where u_m = u_a); so (iii) fair islands go quiet (prediction 1) in monomorphic silence, and the
fills that survive on them are the neutral reservoir of the excluded slot; (iv) conversions of fair islands to a third pair
need the two signers' slots to change together (prediction 4's counter) and arise through the reader route or two coordinated
drift events. The Pareto test of the signers measures the encounter-level gain; the dynamics decide on a different
quantity, the expected payoff against the island's actual composition. That mismatch is what arm S (§1.7) is about.

### 1.6 Two-stage evaluation: separating the arms

- *R:* the responders re-run their programs on the fills (§1.1). *NR:* the coalition is judged against the responders'
  stage-1 actions, i.e. responders do not answer in the test (the installed contract plays the arm's usual semantics, so
  replay can show a different gain). *BR:* the uncommitted responders play a pure best reply to S's new actions, committed
  responders held at their fills; accepted only if every member gains under every such reply, rejected if the remaining
  game has no pure equilibrium. For the examples: against a stubborn constant responder (slot 1 (0, ½) in a fair island)
  and S = {0} proposing (1, ⅔), R rejects (7 > 6, disagreement) while BR accepts (slot 1's best reply is (0, ⅓)); the
  installed contract then earns nothing against the stubborn constant, so BR's acceptance does not deliver (replay
  reports the gain it actually gets). Against an *accommodator* responder ("if slot 0 plays (1, ⅔) then (0, ⅓) else (0, ½)")
  R and BR both accept, NR rejects. Against a generous responder whose reply is not a best reply, R may accept where
  BR rejects. The arms thus separate: NR from R by the responder's answer, BR from R by whether programs best-reply.
- *B (broadcast diagnostic):* a successful genesis also installs the contract on exactly 9 further members of each signing
  slot with the same program, so that the half starts at 10 % instead of 1 %; for the underdominant half of §1.2
  at c₂ = 0.1 and Δ(c₂) = 4 c₂ − 3 = −2.6 sixths nothing changes, but for neutral halves the starting frequency is ten times higher.
  B isolates the responder test from the dilution of a two-individual installation.

### 1.7 The hook grammar (arm H) and the bundle identity (arm C); arm S

*Hook grammar.* The weak grammar of `dollar3` gains the leaf HOOK(t, a₀), tag t ∈ {0, 1}, default a₀ ∈ the nine actions:

    A ::= a | HOOK(t, a₀) | if(B, A, A)

Size 1 per leaf, so the number of size-1 programs goes from 9 to 27, and the length prior, which depends only on the
number of programs of each size, shifts every other size accordingly ("priced like any node"). Behaviour: HOOK(t, a₀) is a
constant a₀. In an encounter the evaluation reaches one leaf (the table entry selected by the atoms' truth values); if it
is a hook, the member *exposes* hook t in that encounter. A contract entry in H is indexed (t, p) with at most one entry
per (t, p), the cap of 8 counting all entries; the fill is written into the hook reached on the member's stage-1 path;
in stage 2 a carrier whose stage-1 path ended at HOOK(t, a₀) and that has an entry for (t, p) plays the fill and
responders substitute it. A member that reaches no hook cannot sign: the proposal is blocked (counted as "blocked", also
for singletons). The canonical form (atoms plus a table over atom valuations) keeps hook and constant entries distinct
(table value ≥ 9 for hooks: 9 + 9 t + a₀), so that two canonical functions with the same behaviour but one hooked are
different programs with a different prior mass (H-inert, the same hooked population with genesis off, isolates the prior).
H-top: the same population, and a member that reaches no hook writes at a free top-level wrapper (tag 2), which is arm R's
fill; a member that reaches a hook writes into the hook. R itself is the grammar without hooks and every program wrapped
at no prior cost.

*Bundle identity (arm C).* A bundle is the content of one accepted genesis: (key p, coalition mask, fill per slot of
the coalition). Every installed entry stores its bundle content, inherited with the fill. Two bundles are the same iff the
content is the same (no separate counter), which makes the identity portable across islands. A copied proposal (a fraction
q = 0.5 of genesis draws in C) picks a bundle by the number of carriers of any of its fills on the island, then draws an
encounter among the island's triples whose stage-1 profile equals the bundle's key (by frequency; if there is none the proposal is
logged as unmatched and the draw is wasted), offers the same coalition the same fills and applies the *same test* as any
proposal. So copying changes the proposal law and never the acceptance rule.

*Arm S.* R with the acceptance test removed: every proposal (from the same proposal law) is installed on its signers.
Selection alone decides. The halves are inherited separately in their own slots. By §1.5 a half with Δ(c) < 0 at the
installed frequency dies and a half with Δ ≥ 0 survives; S keeps what each carrier's fitness likes, which is
the content of prediction 8 (revised).

### 1.8 The object, the clocks, and the budget (what I plan to run)

The order of limits is that of "Islands to infinity before time": annealed mutation, then migration → 0 with islands
relaxed to their attractor between migrants, then the number of islands → ∞ before time. With contracts, the island's
attractor is no longer a program triple: it is a program triple together with a population of contract lists (the
reservoir). I keep the full state (type table and counts) per island and pass a migrant as an individual (program and entries).

*Within-island clock.* Genesis runs at rate ν per generation always; an island is settled when every slot is monomorphic
in programs, all type triples present give the identical outcome (no contract firing on path differs from its absence) and
this has lasted 500 generations with no genesis acceptance that fires on path. Settlement is audited by no-migrant
holdouts (a sample, not every island, see §2).
*Migration clock.* One migrant per event into a settled recipient, the recipient relaxed (with genesis) to settlement
before the next, as before. Spontaneous class changes seen in holdouts are reported as rates per generation and used to
label islands metastable rather than merged with migrant transitions.
*Cost.* The previous experiment moved 10⁶ migrant events per second because the one-migrant chain has a closed form; with
contracts the relaxation must be simulated, ≈ 5 ms to 20 ms per event if the neutral regime is fast-pathed; so the pool is
hundreds of islands, not 16,384, the scale-down is part of the reported deviation, and the I → ∞ statements are
finite-pool statements with symmetrized donors.

Specific expectations from the hand analysis (to be turned into numbers in the predictions file as E1, E2, …):
fair islands go quiet for firing contracts but keep forming and losing reservoir entries (prediction 1's counter holds for
the reservoir, not necessarily for firing); disagreement and wasteful islands convert faster than under arm 0 and to
unequal pairs at least as often as to fair ones; the fair-to-fair conversion κ is raised only through readers; the third-pair
rate α is dominated by reader routes; unequal islands are *not* absorbing for the S = {1, 2}-type contracts because the
excluded slot's half is neutral.

## 2. Deviations, choices where the spec is silent, costs (appended as they arise)

### 2.1 Before any counted cell (code, tests, validation: `src/encounter_contracts*.py`, `tests/test_encounter_contracts.py`)

- **Two hand errors in §1, found by the tests / the first runs and corrected here (§1 is left as written).**
  1. *BR with two uncommitted responders is stricter than §1.6 said.* With S = {0} and both slots 1 and 2 uncommitted, the pure
     equilibria of the remaining 9 × 9 game include the one in which slots 1 and 2 pair with each other, which leaves slot 0
     with nothing; so BR rejects the proposals §1.6 counted as accepted (the stubborn-constant case and the accommodator case).
     BR differs from R in the acceptance of a proposal when exactly one responder is uncommitted (the others being signers or
     carrying an entry for the key); the test `test_br_differs_from_r_on_stubborn_responder` builds that case by committing
     slot 2. The spec's counter-prediction (gpt-6.1-sol: "BR's worst-equilibrium rule can create differences by another
     route") is this route.
  2. *A lone mismatched migrant lives about one generation, not five.* A single individual of a slot is the victim of a given
     slot-event with probability 1/N and a slot has N events per generation, so a deleterious lineage is gone in about a generation
     (the "five generations" of the many-islands notes §1.2 were the lineage's *total* birth count over N ln N, not a lifetime).
     The repair probability in §1.4 is therefore about 2·10⁻⁴ ν per migrant, not 10⁻³ ν.
- **The clock (the spec's two-clock rule, operationalized).** The spec says a class enters the rare-migration limit only if its
  closure is certified from transition support, and otherwise the cell is reported "at an explicit finite migration rate
  (mN = 10⁻³)". Genesis acceptances occur on every fair island at about 3.6·10⁻³ ν per generation (§1.2; confirmed by the
  exhaustive oracle, 2/560 per draw on a fair island of constants), so no fair island is a certified closed class. The pool is therefore run
  in continuous time at the explicit rate: migrants arrive at mN = 10⁻³ per slot per generation (three slots: mean 333 generations
  between migrants to an island), one *round* is 333 generations (mean 1.0 migrants per island), and **the clock is rounds =
  migrant events per island**. The strict m → 0 statements (the within-island chain) are made from no-migrant runs and are labelled
  provisional. The donor state is the donor island's current state (asynchronous, random order per round), a lag of at most one
  round.
- **Settlement (operational).** The spec's literal rule (stage-2 behaviour fixed 500 generations and *no contract formed in that
  window fires on path*) is never met at ν = 1 (acceptances on fair islands every ≈ 280 generations). An island is in outcome
  class c when the stored `_classify` (outcome with at least 0.95 of the encounter mass; member-mixed; other) has been c for 500
  consecutive generations, evaluated at generation boundaries when the state changed; the program composition may drift.
  Transient carriers (one individual, about one generation) do not change the class. The 5,000-generation holdouts of the spec
  are replaced by the no-migrant long runs (`within` jobs, 10⁵–10⁶ generations per island), which also supply the spontaneous
  class-change rates; they are not applied to every island.
- **Founding.** Islands are founded from the stored multinomial seed law (the same generator, N = 100) and relaxed for 2,000
  generations with genesis running and no migrants before event 0 (arm 0: the same 2,000 generations at ν = 0, which settles every
  island to monomorphism, the stored pools' state). No annealed mutation (A = 0) in any cell (A = 150 is not run).
- **Scale.** The earlier pools (16,384 islands, closed-form events) are out of reach for a simulated relaxation, but the engine is
  fast (a quiet monomorphic island is jumped over; 10⁵ generations cost 0.3 s at ν = 1): main cells have I = 1,024 islands, secondary
  arms 512, tilted starts and replicates as listed in the report. The I → ∞ statements are finite-pool statements: the donor
  law is the pool's own (no symmetrization of the donor law; the three fair pairs are compared directly).
- **Eviction.** Entries are kept in installation order and evicted oldest-first past the cap (8; 16 in the cap cell). The spec's
  least-recently-*fired* order is not implemented: firing is not an explicit event in the expected-payoff fitness model (a type's
  fitness is an average over encounters), so recency of firing has no object other than the genesis-sampled encounters. Evictions are
  counted (`ST_EVICT`).
- **Type-table capacity.** At most 160 distinct types per slot per island; a genesis install or a migrant that needs a 161st is
  dropped and counted (`ST_TABFULL`, `ST_MIGFAIL`).
- **Arm B.** The broadcast installs the entry on up to 9 further individuals of the signing slot *with the same program* (any
  entry list), drawn without replacement by type; the realized count is reported (`ST_BC_INST` against `ST_BC_WANT`). The unmatched
  (random-member) broadcast is not run.
- **Arm C.** q = 0.5; a copied proposal picks a surviving bundle by the number of carriers of any of its entries, then an
  encounter among the present type triples whose stage-1 profile is the bundle's key (by frequency); with no such triple it is
  logged as unmatched and no encounter is spent. The bundle code is (key, coalition, fills), so identical contents formed
  independently are one bundle.
- **Arm H.** The grammar gains HOOK(t, a₀) (27 size-1 programs instead of 9; the prior is recomputed; `HookLang`), the hooked
  population has its own founders. A write by a signer that does not reach a hook is blocked (counted by |S|); H-top does not
  block (a member reaching no hook writes at the free top-level wrapper, whose entry has the same semantics: an entry is indexed by the
  key and the stage-1 path fixes the tag, so the entry list needs no tag field). H-inert is H's population at ν = 0.
- **Not run (cut order).** V (the stored aggregate-test veto under this order of limits), the recombination variant of C, the
  unmatched B cell, S-low only if R's acceptance rate is available (it is; run), the A = 150 annealing cell. The N = 200 panel and
  the cap-16 cell are run at I = 256–512.
- **Validation.** `tests/test_encounter_contracts.py` (27 tests): with ν = 0 the engine reproduces `many_islands.island_run`
  draw for draw (counts, generation and status) on founders, and with annealed arrivals; the two-stage evaluation on hand-built
  triples (a carrier that fires, one that does not, a responder that reacts, two responders with nested substitution); BR against R on
  a hand-built case, NR, BR with execution; the genesis examples of §1 (fair, unequal, wasteful, disagreement, mismatched migrant);
  replay of an accepted grand-coalition genesis and of replacement; hook blocking and the hooked prior (18 hooked and 9 unhooked
  constants); copying (an actual surviving bundle, unmatched when none); the S arm installs every proposal; the cap evicts the
  oldest; population, table and cache invariants (cache = direct evaluation, F = full recomputation, neutral flag) along random runs of
  every arm; the Monte Carlo acceptance frequency of the genesis draws against the exhaustive oracle (three islands, 4σ).

### 2.2 Validation run (before any counted cell; `runs/encounter-contracts-validate.json`)

- `nu = 0` against `many_islands.island_run`: 12 of 12 founders and 6 of 6 founders with annealed arrivals identical draw for draw
  (status, generation, final counts).
- The exhaustive oracle against the Monte Carlo acceptance frequency of 30,000 genesis draws on each of 12 islands of the arm-0 pool
  (fair, unequal, wasteful, disagreement, grand classes): all inside 1.9 σ (mean z = +0.22), no island skipped.
- Arm 0 of this engine (continuous-time migrants, 1,024 islands, 1,000 rounds, mN = 10⁻³) against the stored many-islands chain (closed
  form, 49,152 islands, L A = 0): V\* at 1 / 10 / 100 / 300 / 1,000 events 0.254 / 0.265 / 0.329 / 0.403 / 0.469 against 0.280 / 0.289 / 0.348
  / 0.413 / 0.501; the increments agree (+0.215 against +0.221 over the full range) and the level is lower by 0.025 from event 0
  (0.254 against 0.280 post-anneal, 1.9 standard errors of a 1,024-island founding sample; 1.2% of islands are still twin-polymorphic at
  generation 2,000 and count as member-mixed). W + D at 1,000 events: 0.026 against 0.024. The paired comparison with the contract arms is
  between cells that share their founders by island index, so the level offset cancels. The overlap of migrants in time (two within a
  relaxation, a few percent) is the engine's only difference from the stored one-at-a-time chain and is invisible at this resolution.
- This pool is the arm-0 baseline cell of the report (it is also the validation cell and is not selected).

### 2.3 What the counted cells are, cuts and disclosures (written at hand-back)

*Counted cells* (`runs/encounter_contracts/`, report `runs/encounter-contracts.md`): pools of islands at mN = 10⁻³ (one migrant per island per 333-generation
round), founded by the stored multinomial and relaxed 2,000 generations with genesis on, rounds as the clock: arm 0 (1,024 islands, 1,000 rounds; 512 islands to 10⁴
rounds); R at ν = 1 (1,024, 1,000 rounds; replicate 1,024 × 500; 512 to 3,000) and ν = 0.1 (1,024 × 1,000; replicate; 512 to 10⁴); R at ν = 0.01 and 0.001
(512 to 10⁴); the finite-I panel of R at ν = 0.1 (I = 128, 512, 2,048 to 10⁴ rounds) and ν = 1 (I = 128, 1,024 to 3,000); NR, BR, BRx, B, C, H, H-top, R16 at I = 512
(ν = 1 to 300 rounds, ν = 0.1 to 1,000), H-inert, S at ν = 0.1 (512 × 1,000) and S-low at ν = 1 and 0.1 (installation rate equal to R's acceptance rate, 6.26·10⁻³ and
8.47·10⁻⁴ per generation); tilted starts (×6 toward F0 and toward the unequal pairs; R and arm 0); the N panel (50 and 200, ν fixed and ν ∝ N); the migration
panel (mN = 10⁻⁴, 10⁻⁵). No-migrant runs ("within": 200 islands × 3·10⁵ generations at ν = 1; 200 × 3·10⁶ at ν = 0.1; S: 30 islands). Paired migrant / no-migrant
branches (20,000 κ/α events for R, arm 0, NR, BR, BRx, B at ν = 1 and R at ν = 0.1; 6,000 for the other arms at ν = 0.1 and C, H, Htop, R16 at ν = 1, 5,000 / 2,000 general
events).

*Cuts and changes of plan.* (i) **S at ν = 1 was cut**: with one random install per generation no island holds a class for 500 generations (unsettled share 1.0), the
512-island pool ran at 190 s per round (16 h projected for 300 rounds) and was killed after 10 rounds; a 128-island, 30-round pool was run instead (all islands
unsettled, encounter efficiency 0.906, 0.48 of islands Pareto-dominated) and a 30-island 10⁵-generation no-migrant run (no class settles). S at ν = 0.1: 512 islands
× 1,000 rounds (80 min). The paired runs and the within-island chain for S at ν = 1 are therefore absent. (ii) The within-island runs at ν = 0.1 for S were reduced to 30 islands. (iii) V,
the recombination variant of C, the unmatched B cell, the A = 150 cell: not run. (iv) Replicates: R only; single pools for the other arms. (v) Paired runs for
the secondary arms at ν = 0.1 are 6,000 events (not 20,000); the α-resolution budget (2·10⁴ per arm) is met for R at ν = 1 only (and R at ν = 0.1, arm 0, NR, BR, BRx, B).

*Disclosures.*
- The tracked-bundle aggregates (fates, lifetimes, fixation, coordination classes) include the founding relaxation's events (2,000 generations of 3·10⁵–3.3·10⁵ per island,
  under 1% of the tracked contracts at ν = 1; 2% in the 30-island S run). The rate statistics (acceptances per island-generation by class) were reset before the migration phase
  (pools) or before the holdout window (within).
- The first two cells run (R at ν = 1 and ν = 0.1, 1,024 islands) used the engine before the install-site counters, the polymorphism split of the fair-island acceptance
  rate, and the joint (fixed × coordination) counts were added; those cells have zeros in the corresponding fields. Dynamics are unchanged (the counters do not enter the
  state or the random-number order; the tests were rerun).
- The settled class of an island is a class held 500 generations; at ν = 1 about 2% of islands have no settled class at round 0 and 0 from round 10 (R). The
  `settled` shares are among settled islands, `cur` is the instantaneous class.
- Contract fixation ("fix in both member slots") means each signer's half exceeded half of its slot at some check (every 4 generations) within 2,000 generations of
  formation; the tracking table holds 12 bundles per island at a time (the S arm at ν = 1 overflows it).
- "Coordination-needing" bundles are those with a half whose lone-carrier fitness change against the island's current populations is negative at formation;
  "coordination-free" is the complement and includes neutral halves (the excluded slot's), so the coordination-free fixation share is an upper bound on a strict singleton-compatibility share.
- Class-change attribution to migrants uses paired branches on the same random seed (the migrant branch and the control); the in-pool `cev` events are classified only by
  proximity in time (a migrant within 1,500 generations, a fresh contract within 3,000) and are a proxy.
- The founders of arms in one grammar share their random streams by island index (paired); the hooked grammar has its own founders.
