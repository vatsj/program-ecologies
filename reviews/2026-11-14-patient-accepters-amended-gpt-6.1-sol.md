# Review of `specs/2026-11-14-patient-accepters.md` by gpt-6.1-sol

## 1. Errors, contradictions, unsound mechanisms

- **RE 2 reverses the selected and neutral edges.** “Once any program in the excluded slot names it at ½ … its switch is selected (+⅙)” conflicts with “a ½ constant naming it has ρ·N ≤ 2 … (neutral …) and then R’s switch has ρ·N ≥ 5.” R’s response is executed immediately, not a subsequent heritable mutation. With R resident, the entering half-constant obtains a fair partner immediately; with the half-constant resident, entering R improves its victim-slot payoff from ⅓ to ½. **Fix:** distinguish the two orders explicitly: R-first is neutral entry then selected offerer invasion; offerer-first is neutral offerer entry then selected R invasion. Compute frequency-dependent fixation for each edge; do not invent a separate “switch fixation.”

- **The amended timeout exception contradicts the gate.** “R’s table … equals the ⅓ constant’s wherever the read slot does not name it at ½” conflicts with “both reads time out … both pay P_fail.” Actions may coincide; charged payoffs do not. Moreover, a completed offer and a timeout-default offer need not coincide. **Fix:** gate actions, read status and charges separately, with explicit timeout exceptions. Define offers by the actual bounded evaluation available to R, not an uncharged ideal table.

- **Neutrality remains ambiguous.** “Only prior mass and the A_f charge select against it” conflates arrival supply with selection. Prior mass changes introduction rates, not conditional fixation. **Fix:** report per-mutant fixation separately from prior-weighted establishment rates.

## 2. Design flaws or confounds

- **Seeded states are underspecified.** “Every island on a bully–⅓-constant unequal pair” leaves the excluded program unspecified; “every island on a fair pair” leaves both implementations and excluded programs unspecified. These determine R’s read completion, entry cost and reversibility. **Fix:** specify exact triples, role/orientation allocation and replicate pairing; stratify by excluded-slot class.

- **Treatment changes both responsiveness and supply.** F+R removes unspecified constants, while F/R split removes firm readers. F+C⅓ only isolates responsiveness if exactly the same donor mass and role-specific allocation are used. **Fix:** publish normalized founding and tail laws for every arm; make R/C⅓ substitutions pairwise identical outside the substituted family.

- N = 100–400 at fixed migration and finite horizons cannot establish large-population efficiency. **Fix:** label these approach-rate tests; report N-dependence of prior-weighted entry, return and escape rates without treating 120N occupancy as asymptotic stability.

## 3. Predictions likely wrong

- **RE 2:** the half-constant invasion with resident R should generally be positively selected, not neutral; its exact fixation depends on mixed-population encounters.
- **RE 1:** an unweighted median over an unspecified island class need not be near neutral after timeout classes are included. Predict neutrality conditional on completed reads, suppression conditional on costly failure; score these separately.
- **Carbon’s “every exit … never by F or O” is too absolute.** Mutual reading can block the advertised direct route without excluding indirect exits after intermediate replacements. Predict constants dominate *direct* triggers; distinguish direct from multistep exits.

## 4. Missing controls or cheap additions

- Add F without bullies at the same β = 0 cells; RE 5 otherwise lacks its comparator.
- Log resident triples before/after each successful invasion and transient fair episodes, not merely debounced exits.
- Test both R orientations and all role permutations.

## 5. Alternative explanations

Fair occupancy could rise through altered founding basins, reduced bully-compatible constant supply, or migration-driven recolonization—not local patient-accepter escape. Classify exits by local invasion versus imported replacement and compare founded versus seeded-start effects.
