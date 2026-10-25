# Predictions: deriving immigrant rejection for stable sets on islands (2026-10-25)

Spec `specs/2026-10-25-immigrant-rejection.md` (queue 61; reviewed by gemini-4-argon, then gpt-6.1-sol; both folded);
design, definitions, frozen parameters and the engineer's hand numbers in `notes/immigrant-rejection.md` §1 (committed
before this file, in c36ea94). Committed before any code of this experiment and before any counted cell. The
experiment is a finite-size transient experiment at ε = 0 (N = 100, I = 64, one connected component, horizon 10,000
generations for Step 0); nothing here is about π or asymptotic selection.

## The RS's agreement and target

The RS agreed to this experiment on 2026-10-24 (the explainer "Stable Sets on Islands": "a derived immigrant-rejection
guard"), as the follow-up to the migration window ("the next hypothesis ... a derived guard that keeps islands from
adopting a different member, i.e. immigrant rejection"). **Target (RS, 2026-10-24):** "all island outcomes are efficient
and all stable sets show up", in one connected component: *target (as stated)* (every island's modal outcome efficient
and all three fair pairs the modal outcome of at least one island) and *target (V\*)* (every island on a fair pair and
all three present). The RS registered no numeric prediction for this experiment.

## The RE's predictions (verbatim from the spec, falsifiers in brackets)

1. *Step 0.* gV keeps coverage mainly by making mismatched immigrants on a member island lose, through the refusal bit
   carried by residents, not by blocking member-to-member contracts (none exist between members) [the decomposition
   attributes most blocked flips to contract refusal].
2. *Loyalty.* Loyalty meets the stated target in at least 0.8 of runs at mN = 0.1 and 1, N = 100 (gV 1.0 and 0.925)
   [below 0.5 at mN = 0.1]. *Counter-prediction (gemini-4-argon), registered:* one-step loyalty reaches 0.8 at mN = 0.1
   but falls below 0.6 at mN = 1, where immigrant encounters scramble the memory.
3. *Status-quo tie-breaking.* With ε = 0.05 it extends gKR's lifetime by at least 3× at mN = 0.1 but does not reach 0.8
   at mN = 1 [it reaches 0.8 at mN = 1]; with ε = 0 it equals gKR(0.99) within noise (lifetime ratio below 1.2) [above
   1.5].
4. *Conformity.* The conformity reader meets the target as well as gV at every mN (within 0.1) [more than 0.2 below gV
   at any mN]. *Counter-prediction (gpt-6.1-sol), registered:* sampling one encounter is copying, not rejection; it can
   amplify an immigrant's outcome and coarsen like a voter model, losing coverage in a connected component.
5. *Spread.* Every candidate that keeps coverage also rises in frequency under migration (as refusal did), and the
   inert controls do not [a coverage-keeping candidate that falls]. Selection is measured by paired, randomized
   introductions of a rare candidate, and of its inert control, into identical resident islands, recording relative
   reproductive success and establishment, and by the reciprocal rare inert invasion of stabilized islands (the
   within-island frequency change after immigrant arrivals is reported beside). *Counter-prediction (gpt-6.1-sol),
   registered:* a stabilizer can benefit non-carriers equally and stay neutral, so some effective stabilizers will not
   rise when rare.

**Scoring.** Held at or past the stated threshold, failed at the falsifier, partial in between. All contrasts are paired
on founders and kernel seeds, with run-clustered 95% percentile-bootstrap intervals (4,000 resamples); "within 0.1" is
met only if the interval of the difference lies inside ±0.1, failed if it lies outside, undetermined otherwise.
Censored survival curves and member-transition hazards are reported; conclusions are finite-time. Establishment from
uncoordinated founders is reported separately from maintenance of coverage already established. Predictions 2–5 are
scored only if the Step 0 gate passes; otherwise they are recorded as **not run**, with the reason.

## Step 0: the preregistered attribution rule and the gate

**Flips.** Debounced member-to-member (m→m) changes of an island's modal outcome (notes §1.2), counted per run over the
horizon, per mN ∈ {0.01, 0.1, 1}, 40 paired runs. b = mean flips per run in B (baseline, ν = 0), v = in gV. The *flips
that the baseline makes and gV blocks* are max(0, b − v).

**Branch (a): gV blocks flips** (v ≤ 0.75 b at both mN = 0.1 and 1). Shares of the baseline's flips by route, from the
freeze diagnostics run in B:
- immigrant selection: s_I = 1 − f_FI / b (FI vetoes play-changing migrant births at member islands);
- tie blocking: s_T = 1 − f_FPL / b (FPL vetoes partner changes of the included slots through local births);
- contract refusal: s_R = the fraction of the m→m flips of g0 (contracts accepted) that are contract-mediated and absent
  under gV (absent: the mediated flips of g0 minus those of gV, divided by g0's m→m flips).
The mechanism is the route with share above one half at both mN; if none exceeds one half the mechanism is reported as
**mixed**.

**Branch (b): gV does not block flips** (v > 0.75 b at mN = 0.1 or 1). The quantity to explain becomes gV's lead in
coverage over the baseline:
- c = the fraction of gV's m→m flips that are contract-mediated;
- Δ = (target_gV − target_gVs) / (target_gV − target_B), target (as stated) at generation 10,000, where gVs is the strict
  veto (gV without the exemption of (3, 3) fair-to-fair contracts); if target_gV − target_B ≤ 0.1 at a mN the ratio is
  not evaluated there.
- Mechanism **contract channel** (churn through exempted fair-to-fair contracts) if c > 1/2 and Δ > 1/2 at both
  mN = 0.1 and 1.
- Mechanism **immigrant selection** if Δ ≤ 1/2 at both (the strict veto keeps most of gV's lead) and, in gVs, mismatched
  novel arrivals on included slots of member islands reach a majority in under 5% of cases at both mN.
- Otherwise **mixed**.

**Gate.** Prediction 1 is **held** iff the mechanism is immigrant selection; **failed** iff the mechanism is contract
refusal in branch (a) or the contract channel in branch (b) (this is the spec's falsifier "most to contract refusal" read
for a model in which the contract machinery is the actor); **partial** if tie blocking or mixed. The main panel runs
only if prediction 1 is held or the mechanism is tie blocking (the candidates target immigrants and ties). If the gate
stops the main panel, the hand-back contains the decomposition and a proposed revision of the candidates, and
predictions 2–5 are recorded as not run.

## The engineer's predictions for Step 0 (E1–E7, with falsifiers; informed by one seed as disclosed in notes §1.0)

- **E1 (gV churns).** gV makes more m→m flips than B at every mN; the ratio gV : B exceeds 5 at each mN, gV about
  1,000–2,200 per run at mN = 0.1 [ratio below 2 at mN = 0.1 or 1, or v ≤ 0.75 b anywhere].
- **E2 (contract-mediated).** At least 0.8 of gV's m→m flips are contract-mediated at mN ≥ 0.1, and at least 0.8 of its
  installs on member islands are (3, 3) fair-to-fair [below 0.5].
- **E3 (the exemption is the coverage).** gVs meets target (as stated) at mN = 1 in at most half the share of gV; at
  mN = 0.01 gVs and gV differ by at most 0.15 [gVs within 0.1 of gV at mN = 1].
- **E4 (immigrant fates).** On included slots of member islands, mismatched novel arrivals reach a majority in under 2% of
  cases; excluded-slot and matched arrivals are neutral, reaching a majority with probability within a factor 3 of 1 / N
  per arrival that survives its first generations [mismatched included-slot arrivals above 10%].
- **E5 (freezes in B).** FI removes at least 0.7 of B's m→m flips at mN = 1 and less than 0.4 at mN = 0.01; FX removes at
  least 0.5 at every mN; FXP removes at least 0.9 [FXP below 0.7 anywhere].
- **E6 (gKRw).** The weak-consent version of the derived guard has m→m flips within a factor 2 of gV's and target (as
  stated) within 0.15 of gV at mN ∈ {0.1, 1} [target more than 0.3 below gV at mN = 0.1].
- **E7 (the gate).** Prediction 1 is failed (mechanism: the contract channel) and the gate stops the main panel
  [immigrant selection identified].

Main-panel guesses, for the record only (scored only if the gate passes): LOYAL and SQ preserve coverage only as long as
founding diversity does (modest lift over B at mN = 0.1, none at mN = 1); CONF coarsens; spread: the inert controls are
neutral, the stabilizers are neutral to weakly positive.
