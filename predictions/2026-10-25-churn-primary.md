# Predictions: does churn among the fair pairs happen in the primary object? (2026-10-25)

Committed before any code of this experiment runs and before any counted cell. Spec `specs/2026-10-25-churn-primary.md`
(reviewed by gemini-4-argon, then gpt-6.1-sol); notes `notes/churn-primary.md` §1 (hand predictions, churn-capable
readers and their executable paths, prior masses, arm T's frozen settings, the homogeneous-reader composition), written
before this file.

## The RS's message (2026-10-25)

"I find it especially suspicious that the behavior as stated relies on the veto, which I consider an experimental
artifact rather than a core part of our equilibrium notion. Can we replicate the dynamics in 'the primary object'?
Extensional or Turing-complete would convince me."

The behaviour in question (RESULTS "Deriving immigrant rejection for stable sets on islands, Step 0"): under the
hand-written veto gV (and the weak-consent farsighted table gKRw) islands rotate among the three fair pairs 20-59×
faster than the contract-free baseline, which keeps all three present under migration; the baseline loses coverage and
reaches consensus (0.95 of runs by generation 10,000 at mN = 1).

## Arms and cells (frozen)

Every cell: ε = 0, N = 100, I = 64, one connected component, mN ∈ {0, 0.01, 0.1, 1}, 40 runs, 10,000 generations,
w = 0.3, founders common across mN within a run.

- **B6w** (matched baseline rerun): `weak` arm, n = 6, founders `L1` (the stored contract-free baseline). **B6m**: `modalPA`, n = 6, the same founders.
  **Gate (pre-registered):** B6w must reproduce the stored `M-base-N100` rows' coverage and consensus at generation
  10,000 in all 40 runs for every mN; otherwise stop and report.
- **E (arm E):** `modalPA`, n = 10, length prior. **E′:** `weak`, n = 10, same canonical functions and founders as E.
- **E-min, E′-min:** n ≤ 6 catalogue plus the explicit reader families of notes §1.4, doses lo / main / hi (two-partner
  weight 0.003 / 0.03 / 0.10), modal and weak evaluators.
- **T (arm T):** the 27-program L_T^code library of notes §1.4, doses lo / main / hi, price c = 0; sensitivity at
  c₀ = 1.2·10⁻⁴ per step for main and hi (cut candidate).
- **Probe** and **homogeneous-reader cell**: notes §1.5 and the statistics below.

Cut order if needed (disclosed): the c₀ sensitivity, mN = 0.01, 20,000-generation extensions.

## Statistics and scoring rules (fixed now)

- **Modal outcome** of an island at a generation: argmax of its encounter distribution (the stored statistic). **Fair-pair
  island**: its modal outcome is one of the three fair pairs. **Flip**: a debounced change of an island's modal
  outcome, accepted if the new value lasts 25 generations or to the end of the horizon (the stored `flips`); a
  **member-to-member (m→m) flip** goes from one fair pair to another. Flips per run = count over the horizon and the
  64 islands. **Hazard** = m→m flips divided by the island-generations spent on a fair pair, up to the stop generation
  (runs that close, status 1 or 5, stop being at risk when they close); reported per 10⁴ island-generations with a
  run-bootstrap interval (2,000 resamples).
- **Ratio** R(arm, mN) = mean m→m flips per run of the arm divided by that of B6w at the same mN, with a run-bootstrap
  interval. Where B6w has fewer than 1 flip per run (mN = 0, and possibly 0.01), the rule "within 3×" is replaced by
  "arm mean minus baseline mean is below 3 flips per run".
- **Coverage** at generation g: the three fair pairs are each the modal outcome of at least one island; reported at
  10,000, plus the share of islands on fair pairs ("V\* share"), consensus (every island has the same modal outcome),
  and the time-averaged coverage over generations 5,000-10,000.
- **Probe resolution.** Replicates are closed single islands (I = 1, mN = 0) with a 30N-generation horizon (3,000 at
  N = 100); a run resolves at local closure (status 5) or at the horizon; **switch** = the island's modal outcome in the
  last 25 generations (debounced) is a fair pair different from the initial pair; unresolved runs are counted at their
  final state and flagged. 200 replicates per (resident configuration, immigrant class, slot); Wilson intervals;
  rates are pooled across immigrant classes with equal weight (also reported prior-weighted). Every injection is paired
  with a **sham** (a copy of a resident replaces a resident: no change in classes), with a **naming-preserving
  immigrant** (a class whose play against the three residents equals the replaced resident's) and, for reader
  residents, with a **fallback-disabled twin** (S/D programs with the fallback replaced by "name the first partner anyway").
  Routes by the kernel's event log: **takeover** (a majority-class change in a slot whose new class is the immigrant's
  class), **redirect** (the island's modal outcome changes while no slot's majority class changes), **drift** (a
  majority-class change to a resident class), **other**. Encounter-redirection share = fraction of encounters in
  which the resident reader's partner choice differs from its choice against the residents alone; recorded at the time of
  the switch and at injection.
- **Scoring bands.** Each prediction is scored **held / partial / failed**, by the rules below; a number that lands
  inside a stated "hand" interval of notes §1.6 is "inside". Reports give the interval, never only the point.

## Predictions (the RE's; verbatim from the spec, falsifiers in brackets), with the scoring rule for each

1. **No churn in arm E.** Member-to-member flips per run are within 3× of the stored contract-free baseline at every
   mN (no 20-60× churn), and coverage at mN = 1 is below 0.3 of runs [flips at least 10× the baseline with coverage at
   least 0.5]. Flips and coverage are reported beside the share of islands on V\*, so that islands off the set (dominated
   outcomes, as in the stored runs) are not read as an absence of churn.
   *Rule.* Scored for E (modal) and E′ (weak) separately. **Held** iff R ≤ 3 (or the absolute rule) at every mN ∈
   {0.01, 0.1, 1} and coverage at mN = 1 is below 0.3. **Failed** iff R ≥ 10 at mN = 1 and coverage at mN = 1 is at
   least 0.5 (the spec's falsifier, applied at mN = 1 where the baseline coverage is 0). **Partial** otherwise, labelled:
   (a) 3 ≤ R < 10 with coverage below 0.3, (b) R ≥ 10 with coverage below 0.5, (c) coverage 0.3-0.5 with R ≤ 3. Overall
   P1: held iff both held, failed iff either failed, partial otherwise. **E-min is reported beside it** as the
   dilution control: if E-min (any dose) fails by the same rule while E holds, the E null is attributed to prior
   dilution.
2. **No churn in arm T at c = 0.** The same, in L_T [the same falsifier]. Scored at T-lo and T-main (the library priors
   below the registered 0.05); T-hi reported as the dose.
   *Counter-prediction (gemini-4-argon), registered:* if the template prior gives symmetric two-partner readers
   substantial weight (≥ 0.05), islands establish with them resident, each immigrant in a partner slot redirects the
   readers' encounters to the excluded slot, and arm T churns. *Rule:* **held** iff T-hi has R ≥ 3 at mN = 0.1 or 1 and
   R(T-hi) ≥ 2·R(T-lo) at the same mN; otherwise failed; a route label of the excess (redirect/takeover/drift) is given.
   *Counter-prediction (gpt-6.1-sol), registered:* encounter-level redirection can be common while island flips stay
   rare; any threshold depends on the immigrant fraction and the resident composition. *Rule:* **held** iff in the
   homogeneous-reader cell the mean encounter-redirection share at injection exceeds 0.2 for some immigrant fraction
   while the switching rate is below 0.2 at that fraction in the same cell.
   *Rule for P2 itself:* as P1, applied to T-lo and T-main; both must hold for "held".
3. **Readers do not take fair offers at the island level.** In the probe, an excluded slot's fair offer switches an
   island's pair in under 5% of injections, because a single reader in the member slot changes only its own encounters
   [at least 20%]. *Rule.* The primary statistic is the pooled switching rate in the stratum "member slot i = a
   churn-capable reader (E-A, E-B, E-R2 in the DSL; S*o*, D* in T), member slot j = the constant that offers i a fair
   share, excluded slot k forced to offer i a fair share (stratum a)", immigrants injected one at a time (count 1 of
   100) into slot j, over the library of immigrant classes. **Held** iff the rate is below 5% (point estimate) in both
   grammars; **failed** iff it is at least 20% in either; **partial** otherwise. The stratum with the natural excluded
   composition (b), the sham, the naming-preserving and the fallback-disabled controls are reported beside it and
   decide the attribution (a sham rate above 1% invalidates the pooled number).
4. **Coverage, where present, is founders'.** At mN = 0 and 0.01 coverage is high in both arms (founder diversity),
   and it falls with mN [it does not fall]. *Counter-prediction (gpt-6.1-sol), registered:* coverage depends jointly on
   establishment and island count, with no unconditional monotonicity in mN. *Rule.* **Held** iff in E, E′ and
   T-main coverage at generation 10,000 is at least 0.8 at mN = 0 and 0.01 and coverage at mN = 1 is at least 0.3
   below the coverage at mN = 0.01; **failed** iff coverage at mN = 1 is within 0.05 of coverage at mN = 0.01 in any
   of them; **partial** otherwise. The gpt-6.1-sol counter-prediction is **held** iff some arm's coverage rises with mN
   between adjacent values by more than 0.10.

## The engineer's hand predictions (notes §1.6; scored against the intervals there)

E1. Arm E (modal and weak): flips within 0.7-1.5× of B6w at mN ∈ {0.01, 0.1, 1}; coverage at mN = 1 at most 0.05.
E2. E-min: lo within 0.7-1.5×, main within 1-3×, hi within 1.5-5×; coverage at mN = 1 at most 0.10 in every dose.
E3. Arm T, c = 0: lo within 1-2×, main within 1-3×, hi within 2-6×; coverage at mN = 1 at most 0.10 (hi at most 0.25).
    The c₀ price does not raise flips.
E4. Probe: constant member residents under single-immigrant injections switch under 5%; churn-capable member residents
    5-15% at 1% immigrant share, higher at 5% in the homogeneous-reader cell; sham under 1%; naming-preserving under 3%.
E5. Coverage high (≥ 0.9) at mN = 0 and 0.01 and ≤ 0.1 at mN = 1 in every arm; no arm shows the veto's 20-60× excess
    (largest expected: T-hi, 2-6×).
E6. The matched baseline gate passes (draw-for-draw coverage and consensus at 10,000).
E7. Unresolved: whether a ≥ 10× excess appears in T-hi, E-min hi or the reader-member probe stratum; if it does the
    report must give its route.

## What would change the program

- A churn excess ≥ 10× with coverage ≥ 0.5 in a cell whose reader mass is within the library priors (main, lo) would
  mean the churn is a property of encounter-level reading, and the veto was only a faster route to it.
- A churn excess only in the hi doses or only in the homogeneous-reader cell means the churn is a property of a seeded
  population of flexible readers (a seeding threshold), and the contract layer's churn does not appear in the primary
  object at library priors.
- No excess anywhere means the churn is a property of the contract layer.

## Addendum (2026-10-25, written after the probe code and a few debugging runs, before any counted cell)

Two additions to the registered design, labelled as extensions; no registered prediction above is changed.

1. **Immigrant-fraction scan in the homogeneous-reader cell.** The registered fractions are 1% and 5%. A debugging run
   of the probe showed what any selection-based argument predicts: a single mismatched immigrant is removed within about
   ten generations (it earns 0 against the residents' 3/6), so at 1% and 5% the cell can be expected to switch almost
   never. The cell is therefore also run at 10-90% in steps of 10%, to find the fraction at which the island follows the
   immigrants (the threshold the gpt-6.1-sol counter-prediction refers to). Scored only descriptively (threshold fraction at
   which the switching rate first reaches 0.5).
2. **Balanced start with resident readers** (the primary-object analogue of the migration window's balanced-start
   control). I = 60 islands, 20 on each fair pair, the pair slots held by one program each (the lower slot a reader of the
   kind `const`, `switch` or `two`, its mate a constant that names it), the excluded slot drawn from the catalogue's seed
   law; mN ∈ {0.01, 0.1, 1}, 20 runs, 10,000 generations, in the E-min (modal and weak) and T-main catalogues, with the
   constants-only start in B6w and B6m beside them. It asks directly whether *resident* flexible readers under steady
   migration produce churn that resident constants do not. *Hand prediction (E8):* flips per run of the reader starts are
   within 0.5-3× of the constants start of the same catalogue at mN = 0.1 and 1, and the share of runs with all three
   pairs present at generation 10,000 under mN = 0.1 is at most 0.2 above the constants start's. *Falsifier:* a ratio
   of 10 or more with coverage at least 0.5 at mN = 1.

Cut order is unchanged (the c₀ sensitivity first, then mN = 0.01, then 20,000-generation extensions); the two additions
are cut before the c₀ sensitivity only if the scale guard requires it.

## Addendum 2 (2026-10-25, POST HOC: written after the stage 1-4 lottery, probe and balanced-start results were read; before the ablation cells run)

The counted lottery cells showed a flip excess in every arm with resident flexible readers (E-min, T) and none in arms E and
E′ (n = 10), with no gain in coverage. To say which reader family carries the excess, three ablation cells are added per
catalogue (E-min modal evaluator, and T): one family alone at weight 0.03, the rest constants: **S** (the switchers, fallback
"other slot"; DSL `Sj`, `Sk`; T `S*o*`), **Z** (single-partner readers with the null fallback; DSL `Zj`, `Zk`; T `S*z*`),
**D** (the two-partner readers). 40 runs, four mN. These are post-hoc and carry no scored verdict; the engineer's
expectation, stated now so it can fail: S alone carries most of the excess (flips at least 3× B6w at mN = 0.1, and at least
70% of the main dose's excess), Z alone does not (within 1.5×), D alone carries a smaller part than S.
