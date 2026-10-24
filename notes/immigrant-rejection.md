# Deriving immigrant rejection for stable sets on islands (notes, 2026-10-25)

Spec `specs/2026-10-25-immigrant-rejection.md` (queue 61; reviewed by gemini-4-argon, then gpt-6.1-sol in `--mode
amended`; the [after review] text is the resolution). Follows `notes/migration-window.md`, RESULTS "A migration window
for stable sets on islands". §1 is written by hand before any code of this experiment and before any counted cell; §2
(deviations, choices where the spec is silent, costs) and §3 (the gV mechanism) are appended as they arise.

## 1. Hand predictions, the candidates' state machines, Step 0's design

### 1.0 Disclosure about order

Before writing this section I ran a few exploratory timing and orientation runs through the existing
`migration_window` kernels (one founder set, run 0 of base `L1`, H ≤ 5,000, mN ∈ {0.01, 0.1, 1}; baseline and gV;
scratch scripts outside the repository; nothing from them is used as a counted cell). They showed one thing that the
spec's narrative does not assume and that shapes Step 0: **under gV, member-to-member transitions of an island's modal
outcome are frequent, not blocked** (on that one run, in 5,000 generations: about 560 debounced member-to-member
changes at mN = 0.1 and 64 at mN = 0.01 against 19 and 2 under the baseline; at mN = 1 about 1,235 in 3,000 generations;
and most contract installs on member islands are fair-to-fair (3, 3) contracts, which gV exempts from its refusal).
The hand predictions below are therefore **informed by one seed** and are not blind; they are stated before the
proper design runs, and the preregistration of the attribution rule (predictions file) is written to cover both
possible readings (gV blocks flips; gV does not).

### 1.1 The object, frozen now

Everything of `src/stable_sets.py` (kernel `kern`, game `dollar3`, tables, seed laws), `src/farsighted_refusal.py`
(kernel `fkern`, guards g0 / gV / gKR(δ), `Setup`, `kr_table` via `farsighted_refusal_run.guard_arrays`),
`src/dominance_contracts.py` and `src/migration_window*.py` (founders, analysis) is imported; nothing is edited.
Step 0 uses a **generated variant of `fkern`** (`src/immigrant_rejection_gen.py` writes
`src/immigrant_rejection_kernels.py`, patching every anchor with an assertion, as `migration_window_gen.py` does) that
adds (i) the migration-window per-generation records, (ii) the freeze vetoes, (iii) the immigrant-fate counters, and
(iv) retention of the contract-event log. With all switches off the variant is tested to reproduce `fkern_mw` draw for
draw, and (at ν = 0, guard g0 only) `kern_mw`.

- **Game, prior, dynamics, founders:** as in the migration-window notes §1.1: `dollar3` in sixths (20 realizable
  outcomes, 3 fair pairs V\*), the length prior L, Moran with w = 0.3, ε = 0 (no mutation), N = 100, I = 64 islands in
  one connected component, mN ∈ {0.01, 0.1, 1}, ν = 0.1 contract events per island per generation in contract arms,
  menu F, public consent, founders base `L1` run r (common to all arms and mN), kernel seed `run_seed('L1', r) % 2^31`.
- **Horizon and runs:** Step 0 runs **10,000 generations** (the migration window's main snapshot; the 20,000-generation
  extension changes none of the statistics below in kind and costs twice as much), **40 runs** per cell.
- **What the kernel is** (read from the code; the spec glosses it). There are no individual encounters: each island has
  three slot populations of N programs; fitness is the exact mean-field expected payoff against the other two
  populations (`_fit_full`); a birth picks a parent with weights exp(w·payoff), replaces a uniformly random member of
  the slot population, and with probability m = mN/N per birth the parent is drawn from another island (a *migrant
  birth*: the child is a newborn offspring of a remote parent that carries the parent's whole genotype, including
  its contract override and guard bit). A genotype is (program k, override o, guard g); a contract that is installed
  rewrites **every** individual of both member slots to the constant play of the contract (override o), which makes the
  slot a single play class.
- **What a "tie" can mean here.** A program is a fixed function of simulated atoms of the opponents' current plays; it has
  no history. The spec's tie is a population-level notion: the excluded slot's offers drift (neutrally) until both other
  slots offer a pivot the same fair split, and the pivot's population then crosses the 50 / 50 point between naming one
  or the other. For *stateful* candidates I define the program-level tie as: **both other slots' base actions name this
  slot as partner with demands that complete a pair at this program's base demand**; the base program then
  chooses its partner, and a candidate rule overrides the partner (never the demand).

### 1.2 Statistics, frozen now

Inherited from the migration-window notes §1.2: modal outcome per island and generation (argmax of the encounter
distribution), target (as stated) and target (V\*) at generation 10,000, the 25-generation debounce.

- **Flip.** A *debounced change* of an island's modal outcome from a to b: the first generation g at which the modal
  series differs from its last accepted value and keeps the new value for 25 generations (g .. g + 24), or to the end of
  the horizon. Classes: **member-to-member (m→m)** (a and b distinct fair pairs), member-to-other, other-to-member,
  other-to-other. *Flips per run* is the count over the horizon summed over the 64 islands.
- **Contract-mediated.** A flip on island i is contract-mediated if a contract was installed on i at a generation in
  [g_change − 3, g_change], where g_change is the generation at which the modal series first left a. Contract installs
  are read from the contract-event log (outcome code 2).
- **Install classes.** Installs by the modal outcome class before the install (fair / other) and by whether the contract
  is a (3, 3) fair-to-fair contract (the one class gV exempts from refusal).
- **Immigrant fate** (inside the kernel, on islands whose last generation-boundary modal outcome is a fair pair). A *novel
  arrival* is a birth that makes a play class appear in a slot population where it was absent (count 0 to 1). It is
  described by origin (local birth / migrant birth), role (excluded slot / included slot of the island's pair), and
  match (the arrival's action in the modal context equals the plurality class's action, "matched", or differs,
  "mismatched"). Fate: **lost** (count returns to 0 before a majority), **majority** (count exceeds N / 2; the
  kernel's convention for a dominating class), **overwritten** (a contract installs over the slot), **alive** at the
  horizon. Actions in context are read from the joint table against the other two slots' plurality classes, taken at the
  last generation boundary.
- **Coverage.** The migration-window analysis: target (as stated) and target (V\*) at 10,000, members present, consensus.

### 1.3 Step 0 arms (all paired on founders and kernel seeds)

**Reference arms.**
- **B**: baseline, no contracts (ν = 0).
- **g0**: contracts, every program accepts (D1; the contract walk without refusal).
- **gV**: contracts, universal bit, refusal of every contract that leaves V\* except the (3, 3) fair-to-fair contracts
  (the hand-written veto of the migration-window spec, as stored).
- **gVs** ("strict veto", new): as gV but **also refusing the (3, 3) contracts that leave a fair pair**: every contract is
  refused at a member outcome. It differs from gV only by the exemption.
- **gKRw** ("weak-consent farsighted guard", new, a diagnostic): the default gKR(0.99) table's value function W with
  consent **if not worse** (W_i(x) ≥ W_i(y), strict inequality replaced by indifference-accepts). Not a KR
  equilibrium of anything; a plug-in. Its purpose is to test the reading of gV's mechanism that Step 0 will produce
  (gKR is strict, so every fair-to-fair contract, between which every member's value is equal, is refused).

**Freeze diagnostics (in B; vetoes of births, applied after the child and the victim are drawn so the random stream is
unchanged until the first veto):**
- **FX**: the excluded slot's offers are frozen: a birth in the excluded slot of a member island is discarded if the
  child's action against the island's plurality classes differs from the victim's.
- **FP**: the pivot's tie choice is frozen: a birth in an included slot is discarded if the child's *named partner*
  differs from the victim's (the demand may change).
- **FXP**: both together (the second review's interaction control).
- **FI**: immigrant rejection by fiat: a *migrant* birth at a member island is discarded, in any slot, if the child's
  action differs from the victim's. This is an upper bound for any rule that rejects immigrants.
- **FPL**: FP restricted to *local* births (so immigrants may change the pivot; the pivot's own drift may not).
"Member island" means the island's modal outcome at the last generation boundary is a fair pair; "action against the
plurality classes" is read from the joint table with the other two slots at their plurality play class at that boundary
(an approximation for programs that react to their opponents' plays; exact for constants).

### 1.4 Candidates' state machines (reference implementations; the kernel realization is planned, not built unless the gate passes)

All candidates are **heritable traits** held by programs, with a matched inert control that has the same
memory machinery and never overrides. Tie as in §1.1; "slot" means the position (a role in the island), not a source.

1. **LOYAL-k.** State: the program's last k encounter outcomes, each the partner *slot* it was paired with, or none if
   it was excluded. A newborn (local or migrant: in this kernel a migrant is a newborn offspring) starts with empty
   memory. At a tie: k = 1, keep the last partner if there is one; k = 5, keep the partner held by a strict majority
   of the remembered encounters (ties in the count and empty memory fall to the base choice). Planned kernel realization:
   per-generation memory classes (k, h) whose memory is refreshed from the pairing distribution of the class (one
   encounter per program per generation), the joint table extended by wrapper classes that apply the tie override.
2. **SQ.** Two versions. *SQ-direct*: at a tie keep the partner of the island's current pair (the island's modal outcome at the
   last generation boundary, public information, as gKR's consent already uses), no valuation. *SQ-valued*: gKR(0.99)
   extended from contracts to ties: the chain's value is solved with a cost ε (sixths of the dollar) paid on every change
   of coalition, W^ε_i(y) = u_i(y) + δ Σ_y' P(y' | y) (W^ε_i(y') − ε [coal(y') ≠ coal(y)]); at a tie the program
   chooses the partner j that maximizes Q_i(j | y) = W^ε_i(x_j) − ε [coal(x_j) ≠ coal(y)] where x_j is the outcome that
   follows from pairing with j; remaining ties fall to the base choice. ε ∈ {0, 0.05}; ε = 0 is the control that should
   equal the original transition kernel. This is a preference-modification arm. A third cell would charge the switching
   cost in evolutionary payoffs.
3. **CONF.** Before acting, observe the outcome of one random completed encounter on the island (drawn from the island's
   encounter distribution); if that encounter formed a fair pair containing this slot, play the part (name the partner at
   1/2); otherwise keep the previous choice (the previous action; the base program if none). Planned realization: the
   program's previous choice is an override-like memory class that is resampled each generation from the island's fair-pair
   distribution.

These are specified at the reference level and are the object of `tests/test_immigrant_rejection.py` (the by-hand tie
choices and the inert controls). Whether they are integrated into the kernel depends on the Step 0 gate.

### 1.5 The Step 0 gate

The spec makes Step 0 a gate: if Step 0 falsifies prediction 1 the candidates are revised before the main panel. The
attribution rule is preregistered in the predictions file. The three routes of the spec (immigrant selection, contract
refusal, tie blocking) are given operational forms by the freeze diagnostics and the contract-arm accounting; the
reading in which gV does *not* block baseline flips is covered by a second branch (the contract channel and the
exemption ablation gVs), which the spec's wording does not foresee.

### 1.6 My own predictions (engineer's, by hand, informed by one seed as disclosed in §1.0)

Reasoning inputs: weak selection (w = 0.3, payoffs in [0, 1]) is still strong at N = 100 against a class that gets
payoff 0 where residents get 1/2 (N·s = 14), so a mismatched novel arrival on an *included* slot should fix with
probability well below 1 / N, while arrivals in the *excluded* slot and acting-identically arrivals are neutral; the
standing immigrant load at mN ≥ 0.1 keeps the pivot's mean payoff below 1/2, which is what makes a (3, 3) fair-to-fair
contract "dominating" for the pivot; contracts install on both slots at once, so the contract flip is a restart, not a
drift.

- **E1 (gV churns):** gV makes more member-to-member flips than B at every mN tested: per run over 10,000 generations,
  B about 5–60 (mN = 0.1), 2–20 (0.01), 50–300 (1, before consensus stops the run); gV about 1,000–2,200 (0.1), 100–400
  (0.01), 4,000–9,000 (1). The ratio gV : B exceeds 5 at every mN. gV blocks no flips of the baseline.
- **E2 (contract-mediated):** at least 0.8 of gV's member-to-member flips are contract-mediated at mN ≥ 0.1, and at
  least 0.8 of its installs on member islands are (3, 3) fair-to-fair contracts.
- **E3 (the exemption is the coverage):** the strict veto gVs meets target (as stated) in at most half the share of gV at
  mN = 1 (gV 0.9; gVs 0.2–0.5), because without churn the migration load builds a one-member consensus as in B; at
  mN = 0.01 gVs and gV are within 0.15 (founders carry the diversity).
- **E4 (immigrant fates):** on included slots of member islands, mismatched novel arrivals reach a majority in under 2% of
  cases (migrant or local); matched arrivals and excluded-slot arrivals fix at rates of order 1/N·(the arrival's count) i.e.
  tens of percent of the neutral expectation 1/N; the dominant fate of mismatched included-slot arrivals is "lost" within
  tens of generations.
- **E5 (freezes in B):** at mN = 1 FI removes at least 0.7 of B's m→m flips (immigration carries them); at mN = 0.01 FI
  removes less than 0.4 (local drift carries them); FX removes at least 0.5 at every mN (a tie needs an offer from the
  excluded slot); FXP removes at least 0.9.
- **E6 (gKRw):** the weak-consent version of the derived guard accepts the fair-to-fair contracts and behaves like gV:
  member-to-member flips within a factor 2 of gV's and target (as stated) within 0.15 of gV at mN ∈ {0.1, 1}.
- **E7 (the gate):** prediction 1 is falsified: the mechanism is the contract channel (churn through exempted fair-to-fair
  contracts), not immigrant selection; the gate stops the main panel.
- **Main panel (not run if the gate stops; for the record):** I expect the candidates to *reduce* member switching, which gV
  does not; LOYAL and SQ should lock islands on their founding pair and preserve coverage only as long as the founding
  diversity does (comparable to B at low mN, a modest lift at mN = 0.1, no lift at mN = 1); CONF should coarsen
  (voter-like).
