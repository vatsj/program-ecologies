# Predictions: identity and tags in the carrier grammar, the pooling test (2026-10-10)

Spec `specs/2026-10-10-identity-and-tags.md` (reviewed by gpt-6.1-sol; [after review] text is the resolution). Committed
after `notes/identity-tags.md` §1 (commit 78c2618) and before any project code of this experiment, any measurement and
any counted cell (static or dynamic). Every number below is a hand calculation from notes §1 or a guess labelled as
such.

## Frozen design (notes §1)

1. **Language:** milestone 2's carriers (L_T^code, milestone 4's library, sound checker CHK_S, K = 10⁶, V = K/4), PD of
   the modal arm, w = 0.3.
2. **Grammar (n = 7, markers counted):** A ::= C | D | if(B, A, A); B ::= atom | not | and | or; atoms `CHK(p, q, a)`
   (q ∈ {me, them, ⌜C⌝, ⌜D⌝, ⌜CB⌝}), `eq(me, them)`, `tag_1(them)`, `tag_2(them)` (k = 23); marker set M ⊆ {1, 2},
   one node per marker; ⌜CB⌝ = the catalogue's unmarked CB with its list.
3. **Production:** milestone 4's frozen tactic, probes CB, CB1, CBP, CB¹, CB², CB¹², XC (notes §1.3).
4. **Tables:** ideal (host replay, `IdealCheck`) on reduced keys (Lemma R), composed to τ′-units; executable on a class
   sample; identity-aware lumping (rows and columns against every spelling, self and cross-twin cells included).
5. **Priors:** L = 2^−(nodes + |M|); U uniform over classes; tilts T1a/T1b/T1c/T2/T3 at M = F_CB's pooled L mass;
   ablations identity-only / tags-only / named-⌜CB⌝-only.
6. **Lottery:** E3 endpoint, run until frozen or horizon 2,000, separated runs continued to 10,000; L at (100, 64),
   (200, 64), (100, 256); U, tilts, ablations at (100, 64); mN = 1; 40 runs per cell.
7. **Chain (diagnostic):** L, N = 10⁴, closure-seeded; no-clique control at 10³ and 10⁴.
8. **Workers ≤ 3.** Scale guard: if classes exceed 2,500 the full grammar is still run when it is computable; a run
   with the second tag and the `or` connective removed would be a different experiment and would not score any
   prediction below.

## Hand numbers (notes §1)

- Bodies 25,762; spellings 34,968; run trees 8,558 (1,416 with a tag atom, 724 with `eq`); τ′-units 17,305; reduced
  pair-check keys ≤ 1.57·10⁷ per outcome.
- Z = 322.8125. Normalized L weights: `C`, `D` 1.549·10⁻³ each; marked D (D¹ + D² + D¹²) 1.94·10⁻³; **CB 1.936·10⁻⁴
  and EQ 1.936·10⁻⁴ (ratio exactly 1)**; MC¹, TC1¹, EQ′ 9.68·10⁻⁵; TwinD, XC, XC′ 4.84·10⁻⁵; AF¹, OF¹ 2.42·10⁻⁵.
- The eq-clique run tree `eq ? C : D` has 11 spellings (EQ ×4 marker sets, EQ′ ×3, double negation ×3, triple
  negation ×1), total mass 0.2422/Z = **7.50·10⁻⁴**, every pair of them (D, D); CB's run tree `S ? C : D` has the same
  11-spelling structure and the same mass 7.50·10⁻⁴, every pair (C, C).
- Expected seeded count per island at N = 100: CB spelling 0.019, EQ spelling 0.019, MC¹ 0.0097, TC1¹ 0.0097, XC
  0.0048, marked-1 defectors (D¹ + D¹²) 0.116; per run of 64 islands: 1.24 / 1.24 / 0.62 / 0.62 / 0.31 / 7.4.
- Named sub-catalogue (notes §1.7): maximal cliques {CB, MC¹, OF¹}, {MC¹, TC1¹, AF¹, OF¹}, {XC, XC′}, {EQ}, {EQ′},
  {TwinD}; bridges between the open set and the tag-1 club: MC¹ (non-exploitable) and OF¹ (exploited by D¹); AF¹ not a
  bridge; XC's set bridge-less by soundness.

## The RE's predictions (verbatim from the spec)

1. **The clique is cheap but cannot pool.** Under L the eq-clique's exact spelling has mass within 4× of CB's
   exact spelling, but its pairwise-compatible set is one class while the open carrier family's pooled mass is
   ≥ 10× any clique's. *Falsifier:* a clique with pooled mass ≥ the open carrier family's; a ratio in (1, 10) is a
   miss of the number.
2. **Families beat cliques by established mass.** At (100, 64) under L the open carrier family holds every island on
   ≥ 0.7 of runs and no run is won globally by an exact-identity clique; the set with the largest *established* mass
   wins in ≥ 0.9 of runs, and it predicts better than the largest raw seeded count (sol's point: placement and
   founder thresholds matter). *Falsifier:* ≥ 0.1 of runs won by a clique, or the largest-established set losing in
   ≥ 0.3 of runs.
3. **Pooling, matched** [revised after review: my first T1 gave one identity the whole family mass, which lets it
   pool within the intervention, so the clique should do well there]: under T1a (one identity at mass M) the clique
   wins a substantial fraction, my bet 0.3–0.7, by counts; under T1b (M over ten incompatible spellings) carriers win
   ≥ 0.8; under T1c (M over ten compatible spellings) carriers win ≥ 0.8. The pooling claim is T1b ≪ T1a for the
   clique. *Falsifier:* the clique winning ≥ 0.3 under T1b, or T1b ≥ T1a for the clique.
4. **Tag clubs resolve through the marked carrier** [revised after review]: under T2 the tag club rivals the carrier
   family on first establishment; the marked carrier is the non-exploitable bridge (the and-form is not a bridge, the
   or-form is exploitable by marked D); where the marked carrier is alive at separation the rivalry resolves (≤ 0.2
   of such runs separated at the horizon), and where only the or-form bridges, marked D exploits it and the patchwork
   persists. *Falsifier:* ≥ 0.4 of runs with a living marked carrier separated at the horizon, or a resolution
   through the and-form.
5. **Exclusive clubs are bridge-less and make permanent patchworks.** Under T3 no bridge exists, ≥ 0.3 of runs end
   separated between the exclusive club and the carrier family, and none resolves by 10,000 generations. *Falsifier:*
   a bridge class, or a separated run resolving.
6. **The (N, I) panel** [revised after review: no monotonicity claim]: the universal fraction at (200, 64) and
   (100, 256) each lie within 0.15 of (100, 64) under L, with the separation hazard per island pair falling in N and
   the resolution hazard rising in I. *Falsifier:* a change of ≥ 0.3 in the universal fraction, or a separation hazard
   rising in N.
7. **The chain is absorbed** by the eq-clique or TwinD at N = 10⁴ in L (diagnostic). *Falsifier:* a non-clique top
   state.

*Scoring conventions (stated now):* "holds every island" / "universal" = universal-open at the horizon (notes §1.10);
"won by a clique" = universal-other with every surviving establisher an identity clique; "the clique wins" under T1a/T1b
= universal-other held by eq-clique spellings; "carriers win" = universal-open. Runs separated at 2,000 are scored at
2,000 and, in a separate column, at 10,000; a prediction about "the horizon" is scored at 2,000 unless it names 10,000.
RE 4's "runs with a living marked carrier" = separated runs in which a marked carrier (CB's run tree with marker 1) is
alive at the first separation.

## The subagent's predictions (numbered S1–S14, each with a falsifier)

**Static and validation**
- **S1.** The 14 × 14 hand table of notes §1.6 is reproduced by whole plays in every cell. *Falsifier:* any mismatch.
- **S2.** Lemma R and Lemma T′: 0 mismatches between whole plays and the composed table on ≥ 2,000 sampled spelling
  pairs (marked pairs, twins, self-plays included). *Falsifier:* any mismatch.
- **S3.** The extended probes change the list of ≤ 1% of milestone-2-shaped spellings. *Falsifier:* > 5% (1–5% is a
  miss of the number).
- **S4.** Classes exceed 2,500 (guess 3,000–8,000) and the full grammar is computable within 3 hours at 3 workers.
  *Falsifier:* not computable (the reduced grammar would then be a different experiment).
- **S5.** M (F_CB's pooled L mass) lies in [0.005, 0.05] (guess 0.015); the heaviest exact-identity clique is EQ
  (1.94·10⁻⁴); the total mass of all exact-identity cliques is ≤ 0.01. *Falsifier:* M outside [0.002, 0.1], or an
  identity clique heavier than 4·10⁻⁴.
- **S6.** There are rival families of the open carrier family with more pooled mass than any identity clique: the
  defection detectors of milestone 2 (e.g. `if(CHK(them,⌜C⌝,D),D,C)`) mutually defect with CB (CB is certified to
  defect against plain C, and they carry no C script valid against CB). *Falsifier:* no establisher outside N(CB) has
  more mass than EQ.

**Lottery**
- **S7.** L (100, 64): E3 success ≥ 0.9; universal-open at 2,000 in ≥ 0.5 of runs (RE says 0.7; I am less sure because
  of S6's detector rivals); separated at 2,000 in ≤ 0.3; no run won by an identity clique. *Falsifier:* universal-open
  < 0.3, or any clique win.
- **S8.** Pooling check: the largest-established-mass set wins in ≥ 0.8 of decided runs and the largest-seeded-count set
  in fewer runs than that (by ≥ 0.1). *Falsifier:* raw count at least as good as established mass.
- **S9.** T1a: eq-clique spellings hold every island in [0.2, 0.6] of runs by 10,000 (guess 0.35); T1b: ≤ 0.1; T1c:
  universal-open ≥ 0.6. *Falsifier:* T1b ≥ T1a, or T1a < 0.1.
- **S10.** T2: TC1¹ establishes on ≥ 1 island in ≥ 0.7 of runs, marked defectors take most of its islands, and the
  marked carrier is alive at the first separation in ≤ 0.3 of separated runs; the tag club holds every island in
  ≤ 0.1 of runs. *Falsifier:* the tag club holds every island in ≥ 0.3 of runs.
- **S11.** T3: XC establishes on ≥ 1 island in ≥ 0.8 of runs; separated at 2,000 in ≥ 0.3 of runs; **at N = 100 with
  mN = 1 some separated runs do resolve by 10,000, by majority without a bridge** (≥ 0.2 of the runs separated at 2,000;
  RESULTS "Rival networks across islands": minority losses at N = 100, mN = 1 within 10³–2·10⁴ generations even without
  a bridge). This contradicts RE 5's "none resolves". *Falsifier:* 0 resolutions among ≥ 5 separated runs.
- **S12.** (N, I) panel: universal-open at (200, 64) within 0.15 of (100, 64); at (100, 256) lower than at (100, 64) by
  ≥ 0.1 (more rival nucleations per run). *Falsifier:* (100, 256) higher than (100, 64).
- **S13.** U: universal-open ≥ 0.4 and identity cliques win ≤ 0.1 (a clique spelling is seeded about once per run under
  U and cannot establish alone). Ablations: each within 0.2 of L on universal-open. *Falsifier:* clique wins > 0.2
  under U.

**Chain**
- **S14.** At N = 10⁴ under L the chain is absorbed by identity cliques with π split roughly by mass, top state EQ;
  in the no-clique control the top state is an open carrier, P(C,C) in [0.4, 0.95], odds slope (10³ → 10⁴) in
  [0.3, 0.7]. *Falsifier:* the top state not an identity clique; the control's slope outside [0.2, 0.8].
