# Predictions: identity-dependent results under world K, 2026-10-18

Spec `specs/2026-10-18-world-k-reruns.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in amended mode; the
amendments supersede the earlier text, the later winning). Notes `notes/world-k.md` §1 (committed before any code).
Written and committed before any code and any counted cell. ε = 0 lottery statistics at finite (N, I, horizon), never
π; the rain cell is a finite-ε diagnostic.

## RE predictions (verbatim from the spec, including the revision and the registered counter-predictions)

1. **Identity cliques vanish under K in this grammar:** identity islands ≤ 0.005 per island in every K cell.
   *Falsifier:* ≥ 0.02 anywhere.
2. **Universality at N ≥ 200 rises to the proportional control's level:** S-nonself under K within 0.1 of the
   L proportional control (0.80–0.95) at (200, 64), (400, 64), (200, 128); the residue is bridge-less non-identity
   rivals. *Falsifier:* K S-nonself ≤ 0.6 at any of them.
3. **The copy-count law weakens** [revised after the second review: non-identity rivals, bridge loss and coverage can
   still depend on founders and geometry]: the K − L gain in universal-open is larger at (200, 128) than at (200, 64).
   *Falsifier:* K universal-open falls by ≥ 0.3 from (200, 64) to (200, 128).
4. **The provenance rule stops mattering:** S-self and S-nonself within 0.1 of each other under K (in L, S-nonself was
   better by removing minted cliques). *Falsifier:* a difference ≥ 0.2.
5. **The Pangaea establishment law strengthens:** with the gentle readers in the network, μ_net rises and all-defect
   Pangaeas fall (at 6,400: ≤ 2 of 20 under K against 5 under L). *Falsifier:* K ≥ L.
6. **Fission–fusion stays universal-open:** 20/20 in K. *Falsifier:* ≤ 17.
8. **Counter-predictions registered (gpt-6.1-sol).** Some copy-count dependence remains under K; the Pangaea
   improvement is smaller than 5 → ≤ 2 of 20, possibly undetectable; near-ceiling universality under S-self and
   S-nonself may hide reproducible differences in establishment time and founder survival.
7. **Counter-predictions registered (gemini-4-argon).** Under K, S-self turns the former TwinD templates into
   self-defectors (a self-play D certificate keyed to the own quote), so S-self and S-nonself differ in mechanism even if
   universality is near ceiling; and the Pangaea all-defect rates under K and L are indistinguishable (within 1–2 runs)
   at 6,400 and 12,800, because the identity mass moved into the network is small.

(Numbering as in the spec: 8 precedes 7 there.)

## Scoring conventions (declared now; they do not change the wording above)

- **Universal-open** is the scaling classifier's (every island held, holders pairwise mutual, every holder open). A
  cell's value is the fraction of its runs universal-open at the stated generation. Scaling and provenance cells are
  scored at **10,000** unless stated (the stored proportional control was scored at 10,000); provenance's (100, 64)
  contrast is also scored at 2,000, its stored primary.
- **Identity islands per island** = (held islands whose holder unit is an identity unit of that world's universe) / I,
  averaged over the cell's runs; scored at 2,000 and 10,000, the larger value counting for a falsifier.
- **"Within x"** (RE 2, RE 4): *held* if the 95% interval of the paired run-level difference lies inside ±x;
  *inconclusive* if the point estimate is inside ±x but the interval is not; *failed* if the point estimate is outside
  ±x. A falsifier fires on the point estimate.
- **RE 2's comparator** is this run's L proportional control at r = 100 (same founders outside the Q slots, same kernel
  seed), not the stored numbers (which ran at r = N/2 at N = 400); the stored values are context.
- **RE 3** compares K − L (S-nonself, paired) at (200, 128) and (200, 64) at 10,000; *held* if the gain is larger at
  (200, 128) by ≥ 1 run, *failed* otherwise; the falsifier is scored on K alone.
- **RE 4** is scored at (100, 64) (2,000 and 10,000) and (200, 64) (10,000), paired on founders and kernel seed; the
  falsifier fires if the S-nonself − S-self difference is ≥ 0.2 in absolute value at any of them.
- **RE 5** compares this run's paired L and K Pangaeas at 6,400 (all-defect = no living cooperator and none reachable,
  the Pangaea run's *lost*); the falsifier fires if K's count ≥ L's.
- **Sol 8**, *copy-count dependence:* there are no identity copies in K, so "copy count" is read as the seeded
  copies of the former TwinD family Q per run (the stored law's regressor). *Held* if, pooled over K S-nonself cells at
  N ≥ 200, universal-open falls with Q copies (logistic slope < 0, one-sided p < 0.05, cell as a stratum), or if K
  universal-open falls by ≥ 0.15 from (200, 64) to (200, 128) or (400, 64); *failed* otherwise. *Pangaea clause:*
  held if the paired K − L all-defect difference at 6,400 is > −3 runs. *Hidden differences:* held if, in a cell where
  both rules are ≥ 0.85 universal-open, median first-establishment time or founder-lineage survival to 200 differs
  between S-self and S-nonself with p < 0.05 (paired Wilcoxon).
- **Gemini 7**, *mechanism:* held if any former TwinD template reaches a self-defecting unit (self-play D) under
  K S-self in any run; *Pangaea:* held if |K − L| all-defect ≤ 2 runs at both 6,400 and 12,800.

## Subagent's own predictions (W1–W16), with falsifiers and outcome regions

Grounded in notes §1: in K the key is the literal ⌜D⌝, so self-certified defection is never live in play; no identity
unit is reachable under S-nonself; the minted C-identity class (10 trees, μ 0.00195) survives under S-self; μ_net is
unchanged (0.0280 → 0.0277); the former TwinD family are certified suckers in the target; Dill → APn moves 0.0126 of
prior mass into the AP network.

**W1 (identity, the static theorem).** Identity islands are exactly 0 at every checkpoint of every run of every K
S-nonself, K proportional and K rain cell. *Falsifier:* any identity island in those cells (it would mean a kernel or
table error). Consequently RE 1 holds in those cells.

**W2 (RE 1 fails in the S-self cells).** K S-self identity islands per island at 2,000 are ≥ 0.03 at (100, 64) and
≥ 0.02 at (200, 64), and ≥ 0.9 of them are held by the 10 minted C-identity trees (none by the former Q). *Regions:*
held if both bounds hold; inconclusive if one; *falsifier:* ≤ 0.01 at both.

**W3 (K S-nonself universal-open at 10,000).** (100, 64) ≥ 34/40; (200, 64) ≥ 16/20; (400, 64) ≥ 15/20; (200, 128)
≥ 14/20; (100, 128) ≥ 15/20; (100, 256) ≥ 14/20. *Regions:* held if every bound holds; failed in a cell that misses its
bound by ≥ 3 runs (*falsifier*); inconclusive in between.

**W4 (K S-nonself against L's proportional control, RE 2's comparison).** The paired difference K − L(prop) is within
±0.15 at every geometry at 10,000 (point estimates), the residue in K is non-identity rivals, and with 20 runs RE 2's
"within 0.1" is scored *inconclusive* at most geometries rather than held. *Falsifier:* |K − L(prop)| ≥ 0.25 at any
geometry.

**W5 (what the former TwinD mass does in K).** K proportional and K S-nonself differ by ≤ 2 runs at every geometry
(the Q mass is 4.6–18 suckers per run that die in the scramble). *Falsifier:* a difference ≥ 4 runs in any cell.

**W6 (the residue's composition in K).** At N ≥ 200, K S-nonself's failing runs end with non-identity rivals or
scramble failures only; AP-network holders (APn or BR class at H) hold at least one rival island in ≥ 1/4 of the
failing runs; rival islands per run in K are ≥ those of L's proportional control at the same geometry (pooled over
N ≥ 200). *Falsifier:* K rival islands per run < 0.5 × L(prop)'s pooled.

**W7 (RE 3).** The K − L gain at (200, 128) exceeds the gain at (200, 64) by ≥ 3 runs (L falls ≈ 11 → 4; K is
near-flat). *Falsifier:* the gain at (200, 128) is not larger.

**W8 (RE 4 fails).** Under K, S-nonself − S-self ≥ +0.1 at (100, 64) at 2,000 and ≥ +0.2 at (200, 64) at 10,000.
*Regions:* held if both; inconclusive if one; *falsifier:* |difference| ≤ 0.1 at both. Mechanism: the minted
C-identity class, not the former TwinD templates.

**W9 (Gemini's mechanism fails).** No former TwinD template reaches a self-defecting unit under K S-self in any run
(by construction: the D step is partner-free); 6 of its 10 spellings, when their first C production is at the self
root, become illegible suckers. *Falsifier:* any self-defecting Q unit.

**W10 (the Pangaea law is unchanged; RE 5 fails).** Paired K − L all-defect counts lie in [−2, +2] at 3,200 and
6,400, and both are ≤ 2 at 12,800 (Gemini's Pangaea clause holds); RE 5's falsifier (K ≥ L at 6,400) fires with
probability about one half. *Falsifier (mine):* |K − L| ≥ 4 runs at 3,200 or 6,400.

**W11 (Pangaea winners).** K Pangaeas at 12,800 are universal-open in ≥ 18/20; the AP network never holds ≥ 0.5 of a K
Pangaea and its maximum share over a run is ≤ 0.2 in every K Pangaea run. *Falsifier:* the AP network wins any K
Pangaea.

**W12 (fission–fusion).** 20/20 universal-open in both worlds (RE 6). *Falsifier:* ≤ 18 in either.

**W13 (paired transitions).** Of L's identity islands at 2,000 in the S-nonself cells with N ≥ 200, their K
counterparts are open in ≥ 0.6 at 2,000 (rival or unheld otherwise), and the K counterpart was established by a local
lineage in ≥ 0.6 of those (conversion at establishment, not by migration). *Falsifier:* ≤ 0.3 open.

**W14 (the former TwinD lineages die in K).** In every K S-nonself run with N·I ≥ 12,800 the Q spellings' global share
at 200 is ≤ 5·10⁻⁴, and their gentle-reader exposure (own-D readers' encounters in which they cooperate and are
defected against) at 200 is at least twice L's; the fraction acting through a matching keyed certificate is exactly 0.
*Falsifier:* Q share > 0.002 at 200 in any such run.

**W15 (rain, paired).** K rain has 0 identity islands (W1) and cures exploitable rivals (exploitable rival islands at
10,000 ≤ 0.5 × the paired ε = 0 count); L rain has more identity islands than L ε = 0 at 10,000 (≥ +0.01 per island,
paired); K rain universal-open ≥ K ε = 0 − 3 runs. *Falsifier:* L rain identity ≤ L ε = 0 identity, or K rain
universal-open < K ε = 0 − 5 runs.

**W16 (production and efficiency).** r = N/2 changes universal-open and all-defect counts by ≤ 3 runs per cell in both
worlds, with K − L of the same sign (or 0) in both arms; excluding scramble failures, mean island P(C,C) ≥ 0.98 in
every cell of both worlds; K and L scramble-failure counts differ by ≤ 2 runs per paired cell. *Falsifier:* a
difference ≥ 5 runs between r arms, or K scramble failures exceeding L's by ≥ 4 in a cell.
