# Predictions: contracts that form in encounters, with the responders' programs answering (2026-10-25)

Committed before any code of this experiment runs and before any counted cell (notes `notes/encounter-contracts.md` §1,
the hand analysis, was committed first). Spec `specs/2026-10-25-encounter-contracts.md` (reviewed by gemini-4-argon,
then gpt-6.1-sol in `--mode amended`, three addenda each, all folded; the spec is authoritative). Where this file
repeats the spec's wording it does so verbatim. The registered counter-predictions are scored as predictions of
their own authors (held / failed by their own clause).

## The RS's messages (2026-10-25), verbatim from the spec


> "Contracts spawn when they Pareto-improve in aggregate, across the population. Alternatively, they could spawn with
> some rate on individual sets of programs that stand to benefit … it clears up the picture on coalitional deviation,
> since it references an explicit opponent response. To spell it out, coalitions deviate when they Pareto-improve even
> after their opponents respond to their new action profile … This also only makes sense in the extensional wing,
> where response to behavior is defined."
>
> "This is why I want the deviations to be contracts. They trigger on the rare special cases where they apply and don't
> hinder the program elsewhere. [Holders] shouldn't need to [meet each other]. Can we instead only replace the actions
> at that point? In contract language, the responders get to see the contracts mutate into existence, and they only
> actually do if they earn their keep." Best-reply response: "sounds like the right control". Farsighted response: no.

The statement to be tested or refuted (from the engineer's brief): *contracts as situation-keyed overrides that form
in one encounter when every member of the coalition does strictly better after the responders' programs answer make
every island efficient and keep all three fair pairs present under the RS's order of limits (annealed mutation,
rare migration, islands to infinity before time).*

## The spec's predictions and counter-predictions, verbatim

1. *Settled islands go quiet.* On settled fair-pair islands without migrants, in fresh fixed windows after settlement, genesis forms no contract that fires on
   path [a settled fair island keeps forming firing contracts at a rate above 10⁻³ per island-generation].
   *Counter-prediction (gemini-4-argon), registered:* monomorphic settled fair islands go quiet, but polymorphic ones
   keep forming firing contracts above 10⁻³ through drift in silent and committed fills.
2. *Contracts clear some dominated islands.* Under R the settled V\* share is at least 0.15 above arm 0's at the same
   checkpoint [less than 0.05 above].
   *Counter-prediction (gpt-6.1-sol), registered:* gains are heterogeneous with no robust 0.15 uplift across ν and N;
   installations with a positive expected-fitness change, not acceptance counts, predict conversions.
3. *Coordination barrier.* Contracts whose fill needs the other member slot to change as well rarely spread from their
   two signers, because other members of the partner slot do not carry the fill: of contracts formed on dominated
   islands, those that fix in both member slots are under 0.1, and conversions run mostly through partner slots whose
   programs already accept the new action (readers) [at least 0.3 fix in both].
4. *Third-pair moves exist.* Under R, α > 0 with an interval excluding 0 on fair islands [α's interval includes 0].
   [Second addendum review] Exposure budget: at least 2·10⁴ migrant events per arm on fair islands; α is reported
   absent at this resolution if its 95% upper bound is below 10⁻³ per migrant, and unresolved otherwise.
   *Counter-prediction (gemini-4-argon), registered:* a third-pair contract needs slots 1 and 3 to change together,
   its two signers are a 1/N minority each, and it dies by drift, so α's interval includes 0 or α < 10⁻³.
5. *R and BR differ where programs do not best-reply.* The two arms' settled V\* shares differ by at least 0.05, and the
   difference traces to responders whose program reply is not a best reply [within 0.05 everywhere].
   *Counter-prediction (gpt-6.1-sol), registered:* encounter-level response differences can coexist with small
   aggregate differences, and BR's worst-equilibrium rule can create differences by another route.
6. *Coverage.* In the I → ∞ dynamics under R, all three fair pairs keep positive shares from every start [some pair's
   share → 0]. *Counter-prediction (gpt-6.1-sol), registered:* symmetric nonlinear pool dynamics can have unstable
   interior coexistence and attracting boundaries, so coverage depends on invasion rates and the start.

### Addendum (the RS's synthesis): arm H, prediction 7

7. *H lies between 0 and R.* H's settled V\* share is between arm 0's and arm R's, and hooked programs gain share on
   islands where contracts fire [H outside the interval spanned by 0 and R, or hooked programs lose share]. Restriction
   and dilution are read separately: H against H-top is the cost of restricting writes, H-inert against 0 the cost of
   hook syntax in the prior.
   *Counter-prediction (gpt-6.1-sol), registered:* restricting hooks changes the reachable attractors and can expose
   holders to exploitation, so H need not lie between them and hooked programs need not gain.

### Addendum 2 (the RS): peer-to-peer spread, arm C (no numbered prediction in the spec)

The RS: "can contracts still spread peer to peer? I don't really see a need nor a suitable mechanism for it but it's in
keeping with the island model." The RE's proposal: copying as a proposal source, not a transfer. In arm **C**, a
fraction q = 0.5 of genesis proposals are drawn from contracts already carried on the island instead of uniformly.
[Addendum C review, amended] Every installed contract keeps its bundle identity (key p, the signing coalition and
each member's fill), inherited with the fills; a copied proposal is an actual surviving bundle drawn by the frequency
of its carriers, offered to the same coalition of slots, and made in an encounter drawn among the island's triples whose situation is
p (by their frequency; if none exists, the copied proposal is logged as unmatched and no encounter is wasted), and it is accepted by exactly the same test (every
member gains after the responders answer). Copying thus changes which deviations are tried, never which survive the
test, so no contract exists that has not earned its keep in the encounter where it was written; migrants carry their
fills between islands as genes already. (Part W's free copying spread fills without a test and leaked disabled fills
back; this avoids both.) Report C against R: genesis attempts and acceptances by source (uniform or copied), settled
shares, κ and α. A recombination variant (one fill per slot drawn by frequency, across bundles) is a separate,
secondary cell if cheap.

### Addendum 3 (the RS): the Pareto clause as selection, arm S, prediction 8 as revised

The RS: "Eventually I'm hoping we can migrate the Pareto improvement clause from a precondition on mutation to an
observed fitness constraint. If the mutation doesn't serve me I'll die and won't pass it to my offspring, losing the
coalition my slot." Arm **S** is R with the acceptance test removed: genesis installs every proposed contract on its
signers (same proposal law, same keys, same two-stage evaluation), and selection alone decides what survives. Each
member's fill is inherited in its own slot, so a bundle is not co-transmitted; its halves are selected separately.
Since S installs every proposal, its genesis rate is set so that installations per island-generation match R's
proposals (not R's acceptances), and a matched S-low cell installs at R's acceptance rate, so S against R separates
removing the filter from changing the input rate.

Outputs for S: survival and fixation of each half and of whole bundles (both halves present above 0.5 in their slots),
split by whether a half is silent (its key not on path) or firing while it rises; settled shares, κ and α against R
and 0; the share of S's conversions that pass R's test at the moment they fire (selection rediscovering the clause).

8. *Selection keeps only what each member wants alone.* [Revised before the run after both reviews of addendum 3, which
   showed the RE's silent-halves mechanism wrong: keys use override-free play, so on a resident island both halves fire
   at once.] Under S, conversions come from fills that raise their holder's fitness without the other signer present
   (singleton-compatible, or the partner slot's programs already accommodate): at least 0.8 of S's conversions are of
   this kind, and conversions that need two signers to coordinate are at least 5× rarer per migrant than under R
   [fewer than 0.5 of this kind, or coordinated conversions within 2× of R]. The original prediction (silent halves
   drifting up neutrally) is kept in the predictions file as withdrawn, with the reviewers' counter-predictions.

**Prediction 8, original text (WITHDRAWN before the run).** The original text was never committed to the spec (the RE
revised it in the same commit that added the addendum, after the reviewers had shown the mechanism wrong); what is on
record is its content, as quoted by the reviewers and the revision note: *under S, conversions out of dominated islands
come from two silent halves drifting up neutrally, with a silent phase in both slots before the contract fires.* It is
withdrawn: keys are override-free profiles, so on a resident island both halves fire at once. It is not scored.
The reviewers' counter-predictions (gemini-4-argon: fewer than 0.5 of S's conversions come from two silent halves
drifting up neutrally, conversions are directly firing singletons or fills where a slot's program already
accommodates; gpt-6.1-sol: successful S conversions disproportionately use immediately firing singleton-compatible
fills, not two silently drifting halves) are the content of revised prediction 8 and are scored under it.

### Further checks (the spec's list; each is an output, scored where it states a threshold)

- A small N panel (N = 50, 100, 200) for genesis and settled shares, at fixed ν per island and at fixed proposal
  exposure per individual (ν ∝ N), reported separately.
- Replay tests: an accepted genesis, replayed after installation, reproduces its predicted outcome, including
  complement contracts, replacements, two responders and the grand coalition.
- A contract cap of 8 per individual with least-recently-fired eviction, fixed in advance, with a cap-16 sensitivity
  cell; eviction is part of the genesis test and of the oracle, and displaced entries are logged with their
  consequences (the locality claim holds only up to eviction).
- [Addendum S review] An execution-consistent BR cell: uncommitted responders actually play the selected equilibrium
  (the worst for S among pure equilibria, ties by a fixed order), so acceptance and execution agree.
- Firing hazards also from fixed-age, unselected post-anneal snapshots, with time to settlement and the never-settled
  mass.
- Efficiency reported three ways: V\* membership of the modal outcome, encounter efficiency, and whether the island's
  expected slot-payoff vector is Pareto-dominated.
- Configuration snapshots and replays include eviction order and bundle provenance; for each sampled configuration,
  paired migrant and no-migrant branches with common random numbers give the migrant's incremental conversion
  probability.
- Establishment stratified by whether each signer's fill raises its fitness without the other signer present.
- On settled V\* islands, the share whose fair play depends on stage-2 overrides on path against those where the
  programs play fair in stage 1 and contracts were only a transient bridge.
- Replay of every accepted installation across all encounter types it affects, with the signers' expected-fitness
  change, not only the founding encounter.
- A no-response arm NR (the coalition is judged against the responders' stage-1 actions), to separate the response
  from encounter-conditioned acceptance; not cuttable.
- [Addendum C review] BR against R at proposal level: for each proposal, the actual reply, whether it is a best reply,
  the worst-equilibrium verdict and the installed payoffs, so non-best-reply behaviour and equilibrium conservatism are
  separated.
- Establishment and conversion stratified by the sign of the signers' expected-fitness change at installation (not
  only founding-encounter gains).
- α's uncertainty clustered by source island and configuration, not treating migrant events as independent.
- Conclusions are finite-N (50–200) and labelled so.
- Matched no-migrant windows beside migrant windows, and contract-lineage attribution, so that third-pair moves are
  not spontaneous genesis events that happened to coincide with a migrant.

## Frozen design choices (made before any code; the spec is silent or leaves a choice)

All of these may be revised in `notes/encounter-contracts.md` §2 if the code shows they are unworkable; every revision
is disclosed there and in the hand-back.

- **Object.** `dollar3`, weak (simulation) arm, the stored L seeds (length prior, n ≤ 6), N = 100 per slot, w = 0.3,
  founding by the stored multinomial, annealed mutation off (A = 0) as the main cell; ν ∈ {0.1, 1} genesis attempts
  per island per generation. Fitness exp(w · expected stage-2 payoff against uniform members of the other two slots).
- **The clock (the two-clock rule, operationalized).** The spec's clause that a class enters the rare-migration limit only
  if its closure is certified, and otherwise the cell is reported "at an explicit finite migration rate
  (mN = 10⁻³)", is the one I can carry out: each island runs in continuous time with genesis at rate ν; migrants arrive
  at rate mN = 10⁻³ per island per generation (mean 1,000 generations between migrants, slot uniform, donor uniform
  among the other islands, the migrant a donor individual drawn by frequency with its full type, program and fills),
  the donor state taken from the snapshot at the start of a 1,000-generation round. **Clock = events per island =
  rounds** (one round is 10³ generations, one migrant per island on average); the spec's checkpoints 1, 3, 10, 30,
  100, 300, 1,000 are rounds. A spontaneous, genesis-driven class change in an island is recorded per generation and is
  never attributed to a migrant (matched no-migrant windows); strict mN → 0 statements are made only from no-migrant
  holdouts and are labelled provisional.
- **Settlement (operational).** The spec's literal rule (stage-2 behaviour fixed 500 generations and no contract formed
  in that window fires on path) is *never* met at ν = 1: the hand analysis (notes §1.2) finds firing contracts forming on
  every fair island at ≈ 3.6·10⁻³ν per island-generation, because the Pareto test counts the signers only. The operational
  rule used for classes and checkpoints: an island is in outcome class c when the classification of its stage-2
  encounter distribution (an outcome with at least 0.95 of the mass; else member-mixed; else other, the stored
  `_classify`) has been c for 500 consecutive generations; the program composition is allowed to drift (twins), and
  firing carriers that are a small minority do not leave the class. This is disclosed as a deviation from the spec's literal rule.
- **"Fires on path."** A contract entry fires on path if its key equals the stage-1 profile of a program triple present
  in the island at positive frequency and it changes the stage-2 outcome of that triple relative to the same triple
  with no entry. A contract "forms" when genesis accepts it. "Fix in both member slots": each signer's half exceeds 0.5 of
  its slot's individuals at some time within 2,000 generations of formation.
- **Arm 0.** The same engine with ν = 0 (no contracts), same clock and mN, not the closed-form chain; the stored chain
  (many-islands) is the reference for its values at the same checkpoints.
- **Efficiency.** Efficient = outcome with total payoff 1 (fair, unequal, grand at thirds); reported
  with the V\* share (fair pairs) and the mean total payoff; "every island efficient" is scored as the W + D share (wasteful
  or disagreement) below 0.02 at the 1,000-event checkpoint and below its arm-0 value at every earlier checkpoint.
  "All three fair pairs present" is scored as every fair pair having share above 0.02 at 1,000 events from every start,
  plus the V\* share itself, which the RS's statement does not require but which is the object's normative target.
- **Scale.** The previous experiment's pool (16,384 islands) is out of reach because the relaxation has to be simulated;
  pools are of the order of 10² islands (hundreds, decided by the measured cost in §2), with tilted starts by resampling
  founders; all statements are labelled finite-pool and finite-N. The 5 pools of the earlier design become independent
  replicates of a smaller pool; intervals are across replicates (t) or Wilson for proportions, clustered by source island
  for α and κ.
- **Scoring words.** *Held*: the falsifier does not trigger and the interval is on the predicted side. *Failed*: the
  falsifier triggers. *Partial*: it does not trigger but the interval straddles the prediction or only part of a
  conjunction holds. A counter-prediction is held if its own clause holds. Cuts and non-measurements are reported as
  "not scored", never as held.

## The engineer's own predictions (E1, E2, …; hand analysis in notes §1; each with its falsifier)

The recurring structural fact behind most of them: **the acceptance test counts only the signers.** On any fair-pair
island the excluded slot e and either pair member m strictly gain from the deal "m demands ⅔ of e, e takes ⅓", whatever
the third programs are; the third member n is a bystander whose loss is not tested. The same holds, with changed
names, on unequal islands (the victim and the excluded slot), and on wasteful and disagreement islands singleton
steps are accepted. The excluded slot's half is neutral (it earns 0 either way), the pair member's half is
underdominant until the excluded slot's fill is common (threshold ¾ on a fair island). So I expect contract genesis to
convert dominated islands to pair outcomes quickly, to *destabilize* fair islands, and to produce a within-island
recurrent chain among pair outcomes, not a crisp settled state.

- **E1 (firing contracts form on fair islands).** At ν = 1, accepted contracts whose key is on path form on settled fair
  islands of constants at about 2/560 = 3.6·10⁻³ per island-generation; across all fair islands of the pool the mean is in
  [2·10⁻³, 8·10⁻³] per island-generation at ν = 1 and in [2·10⁻⁴, 8·10⁻⁴] at ν = 0.1. [Falsifier: the pool mean outside
  these ranges.] Consequence for prediction 1: its falsifier (rate above 10⁻³) is met at ν = 1 and not at ν = 0.1; so I expect prediction 1
  *failed* at ν = 1 and *held* at ν = 0.1, and gemini-4-argon's counter-prediction (polymorphic islands keep forming
  firing contracts above 10⁻³) to hold also for monomorphic islands at ν = 1.
- **E2 (the pair member's half dies; the coordination barrier).** Of contracts that form on fair islands, at most 0.01
  fix in both member slots, and the median lifetime of the pair member's half (time to extinction) is below 20
  generations; the excluded slot's half survives as a neutral reservoir. [Falsifier: more than 0.05 fix in both slots.]
- **E3 (fair islands are metastable, not crisp).** In no-migrant holdouts of 20,000 generations at ν = 1, fair islands show
  spontaneous class changes at a rate in [3·10⁻⁶, 3·10⁻⁴] per island-generation; at least 0.9 of first exits are to an
  unequal pair (never directly to a different fair pair). [Falsifier: rate below 3·10⁻⁷, or a direct fair-to-fair
  exit share above 0.1.] At ν = 0.1 the rate is about 10 times smaller.
- **E4 (within-island recurrent law).** The no-migrant island dynamics at ν > 0 is irreducible among pair outcomes and its long-run
  law puts a fair-pair share in [0.2, 0.5], an unequal share in [0.5, 0.8], W + D below 0.03; by the S₃ symmetry the three
  fair pairs are equally visited. The pool at 1,000 events per island reaches these within ±0.1. [Falsifier: V\* share at
  1,000 events outside [0.2, 0.5] under R at ν = 1.]
- **E5 (efficiency is reached and reached faster).** Under R at ν = 1, W + D at 10 events per island is below 0.02 against
  arm 0's value above 0.15 (the stored chain: wasteful 0.21 → 0.025 over 10³ events); at 1,000 events it is below 0.02. At ν =
  0.1 at 10 events it is below 0.10. [Falsifier: R's W + D at 10 events above 0.05 at ν = 1.]
- **E6 (fairness does not improve).** Prediction 2 fails: R's settled V\* share at 1,000 events is not 0.15 above arm 0's
  and is at most 0.05 above it, and probably below it (E4's one third of pair outcomes against arm 0's 0.5 at 10³ events); contracts raise
  efficiency, not the fair share. [Falsifier: R's V\* share more than 0.10 above arm 0's at 1,000 events.]
  This supports gpt-6.1-sol's counter (no robust 0.15 uplift).
- **E7 (R, NR and BR agree in aggregate).** The acceptance sets that matter are not responder-dependent on constant
  programs, so the settled V\* shares of R, NR and BR agree within 0.05 at each checkpoint; the acceptance rate of BR is
  between 0.3 and 1.0 of R's. Prediction 5 therefore fails (within 0.05 everywhere) and gpt-6.1-sol's counter (aggregate
  differences small) holds. [Falsifier: R and BR (or NR) differ in V\* share by 0.05 or more at a checkpoint at 100 events
  or later, in both ν.]
- **E8 (third-pair moves).** The excess of fair-to-third-fair-pair conversions in migrant windows over matched no-migrant windows
  has an interval including 0 and an upper bound below 10⁻³ per migrant, so α is "absent at this resolution"
  (prediction 4 failed; gemini-4-argon's counter held), because a fair-to-fair' path needs an unequal intermediate
  (no one-step contract from a fair pair gives a different fair pair: the pair member's strict gain needs the 4). A
  few such conversions are spontaneous and not attributed. [Falsifier: an excess with an interval excluding 0 and a
  point estimate above 10⁻³ per migrant.]
- **E9 (coverage).** All three fair pairs keep shares above 0.02 at 1,000 events from the post-anneal start and from the
  tilted starts (prediction 6 held at the pool resolution), because the within-island chain is irreducible; the tilted start converges to within a factor 2 of equal
  shares by 1,000 events. [Falsifier: a fair pair below 0.02 at 1,000 events from some start.] This is coverage in the weak
  sense; with a fair share near one third it is not the normative target.
- **E10 (broadcast B).** Installing the contract on 9 further copies (10% starting frequency) raises the spontaneous
  fair-to-unequal conversion rate by a factor in [3, 15] over R at the same ν, because the excluded slot's neutral
  half then fixes at 10% instead of 1%; the underdominant half is still selected out at 10% (threshold ¾). [Falsifier: factor below 1.5 or above 30.]
- **E11 (S).** The rate of spontaneous class changes under S (every proposal installed) is at least 3 times R's at the
  same ν, S-low is within a factor 2 of R's, and at least 0.7 of S's conversions are of fills that pass R's test at the
  moment they fire (selection rediscovers the clause for the signers that matter). Prediction 8 (revised): at least 0.8 of S's
  conversions are singleton-compatible [falsifier: fewer than 0.5]; coordinated conversions at least 5 times rarer per migrant
  than under R [falsifier: within 2× of R]. Gemini's and sol's counters are consistent with this and are expected to hold.
- **E12 (H).** Hooks are exposed at a third of the leaves reached: the share of genesis attempts blocked because a needed
  member reaches no hook is about 0.33 for |S| = 1, 0.55 for |S| = 2, 0.70 for |S| = 3 [falsifier: the |S| = 1 share outside
  [0.15, 0.55]], H's spontaneous conversion rate is 0.4–0.8 of R's, and H's V\* share at 1,000 events is within 0.05 of R's.
  Prediction 7 (H between 0 and R in V\*) therefore holds only vacuously, if at all; I expect it *failed or
  unresolved* (H, R and 0 within noise on V\*), with gpt-6.1-sol's counter held.
- **E13 (C).** Copying draws proposals from existing bundles: since the bundles that exist are the accepted ones and the accepted
  ones are the useful ones, acceptance among copied proposals is at least 5 times uniform proposals' (above 0.1), but the settled
  V\* share of C is within 0.05 of R's; copies of underdominant halves keep dying. [Falsifier: copied acceptance below 0.03
  or C's V\* share more than 0.10 from R's.]
- **E14 (the strict limit).** In the strict rare-migration limit (no-migrant holdouts) no fair island at ν > 0 is a certified closed
  class for programs of the L catalogue except where the excluded slot cannot be improved (grand coalitions at thirds, and
  islands whose excluded slot already earns as much as it can); so the m → 0 statement of the spec's two-clock rule
  cannot be made for fair islands and the cells are reported at mN = 10⁻³. [Falsifier: more than 0.5 of fair islands
  show no accepted improving contract in the exhaustive oracle.]
- **E15 (cost).** The relaxation with genesis costs 1–30 ms per island per 1,000 generations in the neutral fast path
  and the full cell (hundreds of islands × 1,000 rounds) one to three core-hours. [Falsifier: more than 10 core-hours per cell → the pool size is cut and disclosed.]

## Controls and validation committed before the counted cells

- Replay tests: an accepted genesis replayed after installation reproduces its predicted outcome (complement contracts,
  replacement, two responders, the grand coalition).
- ν = 0 reproduces arm 0 (the stored `island_run`) draw for draw from the same seed on founding states and annealed arrivals.
- BR on a hand-built case where it differs from R (notes §1.6); the two-stage evaluation on hand-built triples; genesis on
  the mismatched migrant and on an unequal island (notes §1.4, §1.3).
- A validation run with a small pool before any counted cell, recorded in `runs/encounter-contracts-validate.json`.
