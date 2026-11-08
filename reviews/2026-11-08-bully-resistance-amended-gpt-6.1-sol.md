# Review of `specs/2026-11-08-bully-resistance.md` by gpt-6.1-sol

1. **Errors / unsound mechanisms**
   - **Timeout amendment can defeat prudence.** “P refuses `Bn`/`Bp` and accepts every fair reader” conflicts with “run its timeout-accepting variants as the main arm.” Acceptance after an inconclusive exploitation probe does not establish bully resistance. **Fix:** specify separate timeout rules for the cooperation read and exploitation probe; validate resistance after the gate. Keep strict and accepting variants separately scored, rather than replacing the registered main arm.
   - **Threshold falsifier is incorrect.** “All larger [δ] passing” defines δ*, but RE 2’s falsifier is “no grid δ reaches V* ≥ 0.9.” An isolated passing cell followed by failure satisfies neither verdict. **Fix:** falsify RE 2 whenever no δ meets the complete threshold definition; preregister uncertainty handling.
   - **Mechanism assay is underspecified.** “A firm reader into a homogeneous unequal island held by a bully and each ⅓-naming constant” does not specify the third slot, mutant slot, or what fixes. These choices determine payoffs and neutral fixation probabilities. **Fix:** enumerate resident triples and invasion slots, define slot-specific fixation, and verify the neutral baseline with a neutral-label control.

2. **Design flaws / confounds**
   - **The prior-shaped law is not uniquely defined.** “At their measured masses (exact-member lower bounds; the rest in their measured proportions), scaled so that the reader share … takes the grid values” leaves unclear which nonreader masses change and where unclassified mass goes. Ratios of lower bounds are not bounds on actual ratios. **Fix:** publish the normalized probability vector and transformation for every cell; call these grammar-conditioned projections, and test plausible allocations of unresolved mass.
   - **Runtime costs are observed, not isolated.** “Record mean A_f charges” cannot distinguish strategic failure from timeout-induced changes in behavior: the latter change both actions and charges. **Fix:** add a diagnostic replay using identical capped actions with charges suppressed, plus an idealized uncapped behavioral table. Neither substitutes for the main object.
   - **R2 could change execution as well as description length.** A built-in probe must not obtain cheaper evaluation than its written-out counterpart. **Fix:** verify identical arguments, nested caps, root-fuel accounting, actions, and charges against an explicit implementation.

3. **Predictions likely wrong**
   - **RE 2:** refusing a bully prevents one partnership but supplies no mechanism for replacing an established bully–constant pair. P_z also sacrifices fallback opportunities. I predict no threshold at β = 3 unless P materially improves establishment during founding; distinguish establishment from recovery.
   - **RE 1:** “not that bullies shadow fair readers” is stronger than its falsifier: neutral shadowing near 1/N does not trigger fixation “above 3/N.” Both mechanisms can operate sequentially. I predict a mixture, varying with reader family and slot; score neutrality and unequal-state persistence independently.

4. **Missing controls / cheap additions**
   - Add bully-free P/O rows and matched two-read firm controls to measure generic compatibility costs.
   - Seed matched fair and unequal resident configurations, then apply the same tail; measure entry and exit hazards separately.
   - Report all-islands success and fair-pair frequencies across worlds, not only mean V*: ≥0.9 does not meet “every island.”
   - Extend a small set of boundary cells beyond 120N; bootstrap independent runs, not islands.

5. **Alternative explanations not ruled out**
   - Apparent rescue could reflect founding supply or migration-mediated demographic advantage rather than prudent discrimination.
   - Apparent failure could reflect nested-read incompatibility or slow basin escape rather than absence of a bully-resistant efficient attractor.
   - Length-prior failure could be truncation/classification allocation, not intrinsically insufficient mass on useful readers.
