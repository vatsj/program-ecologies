# Predictions: the realizable language, milestone 5: certificates as genes (2026-10-11)

Spec `specs/2026-10-11-certificates-as-genes.md` (reviewed by gpt-6.1-sol; the [after review] text is the resolution).
Committed after `notes/certificates-as-genes.md` §1 (commit 529777a) and before any code of this milestone, any
measurement and any counted cell. Numbers are hand calculations from the notes or guesses labelled as such. Lottery
results will be ε = 0, finite-(N, I, horizon) evidence; the chain is a frozen-inventory diagnostic; the two are never
pooled.

## Frozen design (notes §1)

1. L_T^code with milestone 4's library plus one entry PROD/PCORE (the frozen tactic as code); sound checker CHK_S;
   K = 10⁶, V = K/4; production cap P = K/4 in populations, P ∈ {K/8, K/4, K/2} (and K ∈ {10⁵, 10⁶}) in the
   single-pair tables. The quote is (code, mode marker, list); lists are C block then D block, appended.
2. Encounter: play first (fuel K, milestone 4's semantics), then production in the residual of the same K; production
   never changes the play it follows. Pre-play allocation (unsound for the encounter, F0) only in a test; the reserved
   variant only in the single-pair tables.
3. Modes: H (frozen host list, free); S (gate = own check against the partner; if F, PROD(x, y, C); if no D entry,
   PROD(x, ⌜D⌝, D)); C (each donor entry not held: AC = CHK(x_s, q_a, a), q_C = donor, q_D = ⌜D⌝; append on T; one
   adoption per outcome per encounter); CS = C then S. No negative cache in the dynamics.
4. Populations: milestone 2's P grammar at n = 7, prior L; (N, I) = (100, 64), complete island graph, mN = 1, w = 0.3,
   40 runs per arm, horizon 2,000, checkpoints every 10; per Moran event r = 50 encounters (play, then adoption), then
   reproduction with exact inheritance; state keyed by (unit, mode, spelling if split, ancestry tags).
5. Arms and controls as notes §1.10; price arm c ∈ {0.01, 0.1} (+ {1, 10} labelled extras) on production steps only.
6. Workers ≤ 3, and ≤ 10 − 3·(running gene-arm drivers), minimum 1.

## RE predictions (verbatim from the spec)

1. **Copy-and-check restores distinct-source cooperation along verified transfer edges** [revised after review]: a
   distinct pair cooperates under C from the second encounter iff the donor's script is an edge of the measured
   transfer graph for the recipient's code (same call skeleton, script validates against the recipient), and every
   such pair then cooperates at a steady-state per-match cost within 2× of H's; pairs off the graph never do; two
   empty C-carriers never bootstrap each other. *Falsifier:* an on-graph pair that never cooperates under C, an
   off-graph pair that does, or a steady-state cost ≥ 5× H's.
2. **Search alone is twins-only in populations,** as in milestone 3: S-only cooperates only among exact copies within
   P and its lottery success is ≤ 0.2 of H-only's. *Falsifier:* S-only within 0.5 of H-only.
3. **No copied-script faker, under the stated soundness** [revised after review]: CF's copied C-scripts are refused
   against its own code in every cell (0 accepted, by Theorem S^cert plus Lemma A); its fitness is empirical and not
   predicted (refusal may be cheap and CF still earns exploitation payoffs). *Falsifier:* an accepted copied script
   against a code that defects.
4. **H leads during acquisition, then the modes are neutral or inventory-selected** [revised after review]: in the
   mixed-mode population H-carriers establish first (free scripts), C/CS-carriers adopt from them, and by the
   horizon the mode composition of cooperative holders is within 0.2 of the prior's ¼ each among H, C and CS (neutral
   once inventories coincide), with S ≤ 0.1; in the price arm C/CS exceed H. *Falsifier:* H ≥ 0.6 of cooperative
   holders at the horizon in the main cells (a persistent subsidy advantage), or C/CS ≥ 0.8 (my earlier guess of
   systematic dominance).
5. **Seeded C-only establishes later than H-only and persists as H-only; empty C-only never establishes** [revised
   after review]: unconditional establishment under C-only (f₀ = 0.25) is ≥ 0.8 of H-only's with censoring-aware
   establishment times ≥ 2× H-only's; the single-donor cell establishes on ≥ 0.5 of runs; empty C-only 0/40.
   *Falsifier:* seeded C-only establishment ≤ 0.4 of H-only's, or the single-donor cell ≤ 0.2, or empty C-only ≥ 1/40.
6. **Scripts in circulation are few, and their host ancestry is total in the main cells** [revised after review]:
   the number of distinct scripts held at the horizon is ≤ 3× the number of (skeleton, outcome) pairs present (no
   claim on inheritance fraction, which depends on turnover; it is reported with the turnover), and in the C-only
   and mixed cells every held script has a host ancestor, while in CS-only and S-only the host-free fraction is
   positive only among twins. *Falsifier:* ≥ 10× (skeleton, outcome) pairs, or a host-free script held by a
   distinct-source cooperating pair.

*The subagent's expectation on the RE's six (from the notes, before any measurement):* RE 1 holds for C (on-graph =
same skeleton, plus self-trusting readers); RE 2 fails, falsifier expected to fire (S runs the tactic, so S
restores distinct-source cooperation from encounter 2; S-only ≈ H-only); RE 3 holds as a theorem (notes §1.6); RE 4's
S clause fails (S costs nothing in the main cells, so S ≈ CS ≈ H; C lags where no same-skeleton donor exists); RE 5
holds on establishment, its timing clause is uncertain; RE 6's mixed clause fails (S/CS produce host-free scripts
used with distinct sources), falsifier expected to fire.

## Subagent's own predictions (numbered, with falsifiers)

- **S1 (single pairs, C).** Under (C, H) and (C, C⁺), a carrier pair cooperates from encounter 2 iff the recipient and
  the donor's C script share a call skeleton, or the recipient closes the root's R by Hyp^self (LöbC); never
  otherwise; two empty copiers never. *Falsifier:* a distinct-skeleton (C, H) pair that cooperates, or a
  same-skeleton pair that does not by encounter 2.
- **S2 (single pairs, S).** Every carrier pair that cooperates under (H, H) cooperates under (S, H) from encounter 2 and
  under (S, S) by encounter 3 (encounter 3 exactly for CBP against a partner that starts empty). *Falsifier:* an (H, H)
  cooperating carrier pair that is (D, D) at encounter 3 under (S, S) at K = 10⁶.
- **S3 (production cost).** The tactic as code costs 5·10³–3·10⁴ steps per produced script at K = 10⁶ and never more
  than 10⁵; P never binds at K = 10⁶; at K = 10⁵ (V = 25,000, P = 12,500 at K/8) P binds for at least one catalogue
  carrier. *Falsifier:* a produced script costing > 10⁵ at K = 10⁶, or none below 5·10³ (I expect δ and ε near the
  bottom).
- **S4 (steady cost ratios).** Copier against a same-spelling H partner: steady per-match cost / H–H's in [1.6, 2.4]
  (pair check against self-play check); against a distinct spelling in [0.9, 1.1]. S's steady cost includes the gate,
  ratio in [1.6, 2.4] against distinct-spelling H–H. *Falsifier:* a ratio outside its interval for CB, CB1 or CBP.
- **S5 (refusal cost).** CF's refusal of a carrier's C script costs ≤ 3·10³ steps; 0 adoptions of C scripts by CF in
  every cell; CF adopts true D scripts from certificate-carrying defectors. *Falsifier:* a refusal > 10⁴ steps, or a
  C adoption by CF (which would also fire RE 3).
- **S6 (transfer graph).** No C edge between run trees with different C scripts unless the recipient closes R by
  Hyp^self; the D edges are dense (δ accepted by ≥ 50% of the run trees that carry any D script under H).
  *Falsifier:* a cross-skeleton C edge without Hyp^self in the recipient's derivation.
- **S7 (Lemma A in populations).** 0 false atoms in every check; transfer failures (adopted object not certified
  against the donor) are only of type F1 and below 1% of adoptions. *Falsifier:* a false atom, or transfer failures
  ≥ 5% of adoptions in any cell.
- **S8 (S-only).** S-only's unconditional establishment and E3 success are within 0.1 of H-only's (both ≥ 0.9);
  universal-open within 0.15. *Falsifier:* S-only establishment ≤ 0.8 of H-only's.
- **S9 (mixed modes at the horizon).** Among individuals of cooperative holder types: H, S, CS each in [0.2, 0.4],
  C ≤ 0.2; at generation 10 H's share is the largest. *Falsifier:* S ≤ 0.1, or H ≥ 0.5 at the horizon.
- **S10 (seeded C-only).** f₀ = 0.25: establishment ≥ 0.9 (guess 1.0); f₀ = 0.05: ≥ 0.75; median establishment
  generation at f₀ = 0.25 between 1× and 3× H-only's. *Falsifier:* f₀ = 0.25 below 0.75.
- **S11 (single donor).** Establishment in [0.5, 0.95] (guess ≈ 0.75): one establisher per island, 64 islands, each a
  near-neutral entrant with a second-order advantage. *Falsifier:* outside [0.3, 1.0].
- **S12 (empty C-only).** 0/40 establishments and island P(C,C) < 0.05 at the horizon in every run (certificate-less
  cooperators lose to defectors). *Falsifier:* any run with an island at P(C,C) ≥ 0.9.
- **S13 (controls).** Publication disabled at f₀ = 0.25: establishment within 0.15 of the published cell (copying
  helps only same-skeleton copiers, which are rare by prior mass); inheritance disabled: establishment ≤ 0.3 (seeded
  lists die with their founders unless copied). Identical inventories: mode shares of cooperative holders within 0.1
  of ¼ each. *Falsifier:* publication-disabled more than 0.3 below the published cell; inheritance-disabled ≥ 0.6.
- **S14 (price arm).** c ∈ {0.01, 0.1}: within lottery noise of the mixed cell (|Δ establishment| ≤ 0.1, mode shares
  within 0.1); the per-match production cost is ≈ 10⁻⁴–10⁻² of the stakes, below drift (N·w·c·steps/K < 0.1 at
  c = 0.1); RE 4's price clause (C/CS exceed H) fails because H is free. *Falsifier:* c = 0.1 moving H's share by
  more than 0.15.
- **S15 (size sweep).** Per-match production cost by mode independent of N within 30% at N ∈ {50, 100, 200} (S pays
  its gate every match and copiers re-pay refusals: realized schedules are α ≈ 0, not α = 1); acquisition cost per
  lineage independent of N within 30%. *Falsifier:* a 2× change of S's per-match cost between N = 50 and 200.
- **S16 (slow transfer, r = 1).** Seeded C-only establishes no earlier than at r = 50; mixed: H's share of cooperative
  holders at generation 50 higher than at r = 50. *Falsifier:* the reverse on both.
- **S17 (scripts).** Distinct scripts held at the horizon ≤ 12 per run in every cell; in S-only, CS-only and mixed,
  host-free scripts are held by distinct-source cooperating pairs (RE 6's falsifier fires). *Falsifier:* > 24
  distinct scripts held in some run.

## Hand numbers (notes §1)

- Scripts: σCB 5 nodes, σCB1 and σCBP 8, δ 5, ε 2 (milestone 4). The P catalogue's H lists: 25 distinct entries, ≤ 1
  C and ≤ 1 D entry per list (scratch count, disclosed in the notes).
- Check costs (milestone 4, K = 10⁷): CB self-play 8,782; CB–CB1 21,541; CB–CBP 30,491; CB1–CBP 37,140; Ccert 2,065;
  distinct-quote same-code pair ≈ 1.8·10⁴ (guess); listless target ≈ 10³ (guess).
- Encounters to steady (C, C) for named pairs: (H, H) 1; (C, H) same skeleton 2; (C, H) distinct skeleton never;
  (S, H) 2; (S, S) 2, CBP against an empty partner 3; (C, C) empty never.
- Prior masses under L (milestone 2): establishers 0.061 (6.1 per island of 100); unconditional cooperators 0.354;
  all-D rows 0.376; CB's run tree 9.7·10⁻⁴ (0.1 per island). Seeded C-only: f₀ = 0.25 gives ≈ 1.5 list-carrying
  establishers per island, f₀ = 0.05 ≈ 0.3.
- Encounters per individual per generation: 2r = 100 at r = 50; 2 at r = 1.
- Price: a production of ≈ 2·10⁴ steps at c = 0.1 costs 0.002 per match; w·Δ = 6·10⁻⁴; N·w·Δ = 0.06 at N = 100.
