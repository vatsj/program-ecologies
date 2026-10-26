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

(none yet)
