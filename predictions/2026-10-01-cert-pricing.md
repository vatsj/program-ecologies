# Predictions: certificate pricing, a free set based on what PA decides about the opponent rather than on sameness, 2026-10-01

Status: reviewed by astra (`reviews/2026-10-01-cert-pricing-gpt-6-astra.md`) and fable
(`reviews/2026-10-01-cert-pricing-fable.md`), then revised; changes are marked [after review]. Committed before the run.

Before the commit only the following were run:
- static single-edge rates, using `Chain.expand` on single states;
- the two-level estimates below;
- two declared driver smoke cells (listed at the end).

## Background

Lazy pricing (RESULTS.md, "Priced arm") makes a check free against constant opponents and against exact copies (the
same canonical function). Against everything else it charges the atoms price c·k(x)·(1 + settle world of x's atoms
against y).

At n = 8 and c = 10⁻² it locked in P* = `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` and two siblings through cost
incumbency:
- a behaviourally neutral newcomer pays c against the residents, while copies are free;
- P* punishes ALLC, so the P* world has no neutral exit.

P* and FairBot defect on each other. The cooperative mass sits in a network that rivals FairBot's instead of
including it.

The question is whether a free set that rewards *being decidable* rather than *being the same* keeps lazy's escape
from the price ladder without the incumbency.

## The arm (`src/cert_priced.py: build_cert`)

The price function is lazy's, unchanged. Only the free set changes.

**Certificate pricing, level ℓ.** x's check of y is free iff y's action toward x is decided in PA + ℓ·Con. That is,
PA (ℓ = 0) or PA + Con(PA) (ℓ = 1) proves "y plays C against x", or proves "y plays D against x". Otherwise x pays
the atoms price.

On the linear GL chain, "decided at level ℓ" means y's value toward x is constant on every world ≥ ℓ. The evaluator
already tracks this as `hc[ℓ, y, x] or hd[ℓ, y, x]` at stabilization. `_evaluate_cert` is `_evaluate_priced`
without cliques, returning hc and hd. Run in modes `lazy` or `atoms`, `build_cert(n, c, ...)` reproduces
`build_priced` exactly: the payoff matrices and class lists are identical at n = 6, 8 and c = 10⁻³, 10⁻² (checked).

[after review, astra] **What "decided in PA" rests on.**
- The agents are pure modal agents of rank 0, and every self-reference is under a box. The joint fixed point is
  therefore a letterless modal sentence (de Jongh–Sambin).
- For letterless sentences, GL proves φ iff φ holds at every world of the linear chain. By Solovay's theorem, GL
  proves φ iff PA proves φ*.
- So "PA decides y's action toward x" is exactly the evaluator's hc[0]/hd[0] test, and "PA + Con(PA) decides it" is
  the hc[1]/hd[1] test.
- That said, this is **semantic certificate eligibility with free provision**, not a certificate market. Nothing
  bounds proof length or models a program withholding its certificate.

[after review, fable] **What cert0 is, syntactically.**
- *Why monotone programs are decided whenever they cooperate:* every box is true at world 0, and box truth only
  falls as the world index rises. A program that is monotone in its box atoms (no effective negation) can therefore
  only switch from C to D, never back. If it cooperates in the end, it cooperated at every world, so PA decides it.
- *How much of the language that covers:* 330 of 610 canonical functions at n = 8 are monotone, carrying 98.7% of
  the prior mass.
- *What cert0 taxes:* almost exclusively cooperation that is conditional on *non*-provability, i.e. a negated box.
  That is P*'s defining feature.
- *The syntactic twin:* call it `mono`. Free iff y is constant, or y is monotone in its atoms and (y cooperates with
  x, or y's world-0 action is D). It differs from cert0 on 65,749 canonical pairs, which carry μ⊗μ weight 3.6·10⁻³
  out of 0.58.
- *So:* the claim this experiment can support is about monotone, box-positive cooperation, which certifies itself.
  "Legibility" is the motivation, not the finding.

**Variants run through the chain.**
- **cert0** (primary): free iff y's action toward x is PA-decided.
- **cert1** (sensitivity, looser): free iff decided in PA + Con(PA).
- **certC** (sensitivity, the literal reading of "cooperation is cheaply certified"): free iff y is a constant, or PA
  proves y cooperates with x. It differs from cert0 only in charging for reading a non-constant, PA-certified
  defector.
- References, rebuilt by the same code:
  - **lazy**;
  - **c = 0**, meaning atoms at c = 0, which is the free modal arm.
- [after review] Controls, n = 8 only:
  - **mono** (fable 3a): the syntactic twin above.
  - **cert0flat** (fable 3b): cert0's free set, with a flat price c for every non-free check (no atom or
    settle-world multiplier). This is the decisive control for *which part* of cert0 removes the P* block.
  - **lazycert0** (astra): the union of the lazy and cert0 free sets. Copies are always free, plus certified
    cross-reads. It keeps P*'s copy subsidy and adds cross-program decidability.
  - **cert0diag** (astra): constants free; copies free only if their self-play is PA-decided; no cross-program
    exemption. It removes P*'s copy subsidy without adding cross-program reads.
- [after review] **cert0v** (astra: a verification charge of c/10 on every free check by a program with boxes):
  static only, see below.

Constants are decided at level 0, so a check of C or D is free under every chain variant. Entry into all-D is
neutral, as under lazy pricing; this is condition (i) of THEORY §9.2.

### Why this operationalization

1. **It prices what the reader needs.** To best-reply, x needs only y's action toward x. A PA proof of that action is
   a certificate that can be checked in time linear in its length.
2. **The three suggested bases collapse into two.**
   - *Settle world and proof level are one criterion.* The settle world of the *opponent's value* toward you is
     exactly the least proof level that decides it: the value is constant on worlds ≥ ℓ iff PA + ℓ·Con decides it.
   - *The opponent's own work is a different quantity.* It is its atom count times the settle world of its atoms.
     It is rejected below.
3. **It is not sameness** (static, n = 8). The language has 287 self-cooperating canonical functions and 20,353
   mutually cooperating off-diagonal pairs among them.
   - *Pairs free both ways:* 0 under lazy, 9,267 under cert0, 12,338 under cert1.
   - *Copies that pay:* under cert0, 142 of the 287 pay to read their own copies. Their prior mass is 5.2·10⁻³,
     against 0.38 for all self-cooperators, most of which is ALLC.
   - *Example pairs:*
     - FairBot, `BOX1(THEM(ME))` (FB1), `BOX(THEM(THEM))` (BTT) and `BOX1(THEM(THEM))` (BTT1) decide their mutual
       cooperation at level 0.
     - P*, P*T = `and(BOX1(THEM(THEM)),not(BOX(THEM(THEM))))` and P*M = `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))`
       cooperate with each other only at level 1.
4. **It is not retrospective in the sense the priced-arm reviews flagged.** Whether PA decides y's action toward x is
   a fixed property of the pair. It does not depend on when one evaluation stopped changing.
   - *What is still retrospective:* the price in the non-free case, c·k(x)·(1 + settle world of x's atoms), is
     inherited from lazy so that the comparison isolates the free set.
   - [after review, fable] *Where that price now falls:* by the monotonicity point, it falls almost only on reading
     non-monotone programs.
   - *An idealization:* producing a certificate is free, as recognizing a copy is free under lazy.

### Alternatives rejected

- **Self-decidability.** x is free iff *x's own* action toward y is PA-decided.
  - *Rejected on a static fact:* FairBot's defection against D is decided only at level 1. PA cannot prove that
    FairBot defects on DefectBot without Con(PA).
  - *Consequence:* FairBot would pay against D, and the entry barrier would return.
- **Opponent's work.** x is free iff y's own atoms toward x settle at world 0.
  - *Rejected:* it rests on the atoms' last-change world, the retrospective quantity the priced-arm reviews flagged.
  - *Also:* it prices the opponent's computation, not what the reader must verify.
- **Cooperation-only certification** (certC) and **the looser level** (cert1) are run as sensitivity variants.
- **A verification charge on free checks** (cert0v) is not run through the chain, for two reasons:
  - *It reintroduces the ladder statically.* With FairBot paying c/10 per check and ALLC paying nothing, ALLC
    strictly invades all-FairBot at an N-independent 5.4·10⁻⁵ (c = 10⁻³) and 1.4·10⁻⁴ (c = 10⁻²) per mutation event,
    against 1.6·10⁻⁵ neutral at c = 0 and N = 3·10⁴.
  - *It creates barrier states the chain handles badly.* FairBot entering all-D now faces an unstable interior rest
    point at FairBot share c/10 (10⁻⁴ or 10⁻³). The chain stores these as polymorphic states at (0.999, 0.001):
    the same slow-rest artefact as the priced arm's suspect cell.

  So the exact zero is load-bearing. Any positive verification cost charged only to programs with boxes rebuilds
  the price ladder. This is reported as a static result, not a chain verdict.

### Failure modes

1. **Secretly sameness.** Ruled out statically (point 3 above).
2. **Free against defectors creates a rung.** A rung needs a resident that pays at home and a cheaper on-path
   equivalent. A resident whose self-play is certified pays nothing at home, so nothing can undercut it. Rungs
   therefore exist only below residents whose cooperation is undecided in PA.
   - *Where they lead* (static, n = 8, cert0):
     - P* pays 4c at home.
     - Its cheaper equivalents, `not(BOX(THEM(ME)))` (nBM) and `not(BOX(THEM(THEM)))`, pay 2c. They now invade P*
       strictly; they were neutral exits at c = 0 and deleterious ones under lazy.
     - Both cooperate with D (checked), so D strictly invades them. nBM is also exploited by FairBot.
   - [after review, fable] *This rung is a price-ladder effect, not a free-set effect.* It needs the atom multiplier,
     which makes P* (two atoms, settle world 1) dearer than nBM (one atom). Under a flat price P*'s exits are neutral
     and ∝ 1/N, as at c = 0: statically 3.1·10⁻⁷ at N = 10⁴ for cert0flat, the same as c = 0. cert0flat separates
     the two.
   - [after review, astra] *What D's free check does.* certC charges for reading non-constant certified defectors
     and keeps D free; its static rates equal cert0's. That shows charging for certified non-constant defectors is
     inert. It does not show that the free check of D is inessential. That one is required for neutral entry.
3. **Retrospective cost.** Addressed in point 4 above.

## Static single-edge rates (ε→0 chain transition rates per mutation event, w = 0.3, n = 8 unless stated)

**Entry.** ρ(FairBot | all-D) is the same under every chain variant, since the check of D is free: 0.0421 / 0.0136 /
0.0044 / 0.0025 at N = 10² / 10³ / 10⁴ / 3·10⁴.

**Home payoffs.**
- *FairBot, PrudentBot (PB) and BTT:* 0 under c = 0, lazy, cert0, cert1, certC, mono, cert0flat, lazycert0 and
  cert0diag.
- *P\*:* 0 under c = 0, lazy, cert1 and lazycert0; −4c under cert0, certC, mono and cert0diag; −c under cert0flat.

**Exits from all-FairBot.**
- *c = 0 and cert0, cert1, certC, mono, cert0flat, lazycert0:* no strict exit; neutral 4.9·10⁻³ / 4.9·10⁻⁴ /
  4.9·10⁻⁵ / 1.6·10⁻⁵ at N = 10² / 10³ / 10⁴ / 3·10⁴, of which ALLC is 0.96.
- *Lazy and cert0diag:* the same neutral rate, plus small "other" exits, because FB-family members pay to read
  FairBot.

**Exits from all-BTT** [after review, fable]. A strict exit of 5.1·10⁻⁶ at c = 0 and under every variant, into
nBM-type programs, plus the neutral 1/N rate.

**Exits from the P\* world** (strict / neutral / other).

| variant | c | N = 10² | 10³ | 10⁴ | 3·10⁴ |
|---|---|---|---|---|---|
| c = 0 | 0 | 0 / 3.1e-5 / 3.9e-7 | 0 / 3.1e-6 / ~0 | 0 / 3.1e-7 / 0 | 0 / 1.0e-7 / 0 |
| lazy | 10⁻² | 0 / 0 / 3.1e-5 | 0 / 0 / 2.1e-6 | 0 / 0 / 7.5e-11 | 0 / 0 / 8.9e-20 |
| lazy | 10⁻³ | 0 / 0 / 3.1e-5 | 0 / 0 / 3.1e-6 | 0 / 0 / 2.1e-7 | 0 / 0 / 1.5e-8 |
| cert0 (= certC = mono = cert0diag) | 10⁻² | 4.1e-5 / 1.2e-7 / 8.2e-7 | 1.9e-5 / 1.2e-8 / ~0 | 1.8e-5 / 1.2e-9 / ~0 | 1.8e-5 / 4.1e-10 / ~0 |
| cert0 (= certC = mono = cert0diag) | 10⁻³ | 3.2e-5 / 1.2e-7 / 5.2e-7 | 4.1e-6 / 1.2e-8 / ~0 | 1.9e-6 / 1.2e-9 / ~0 | 1.9e-6 / 4.1e-10 / ~0 |
| cert1, cert0flat | both | as c = 0 | | | |
| lazycert0 | both | as lazy | | | |

**Near-closed cooperative worlds** (N = 10⁴). These are self-cooperating classes with μ ≥ 10⁻⁸ whose total exit is
below 10⁻³/N.
- *Lazy, c = 10⁻²:* four. P* and its two siblings, with exit 7.5·10⁻¹¹, and PrudentBot, with 2.6·10⁻⁸.
- *cert0, cert1 and certC at both c, and c = 0:* none.

**Two-level estimate.** R = Σ_q flux(D → q) / exit(q) over the self-cooperating destinations of all-D, treating every
exit as a return to D, and P(C,C) ≈ R/(1 + R). It reproduces c = 0 at n = 6 (0.700 against the measured 0.707). At
n = 8 it underestimates (0.700 against 0.725), because it ignores moves between cooperative worlds. [after review,
fable] In particular it misses the P* block's inflow: it gives the P* block 4% of the cooperative mass, while the
c = 0 chain had 13–15%.

| n = 8 | N = 10⁴ | 3·10⁴ | FairBot-block share of R at 3·10⁴ |
|---|---|---|---|
| c = 0 | 0.591 | 0.700 | 0.96 |
| lazy 10⁻³ | 0.599 | 0.750 | 0.77 |
| lazy 10⁻² | 0.996 | 1.000 | 0.00 |
| cert0 = certC = mono, both c | 0.581 | 0.691 | 1.00 |
| cert1, both c | 0.591 | 0.701 | 0.96 |
| cert0flat, both c | 0.591 | 0.700 | 0.96 |
| lazycert0 10⁻³ / 10⁻² | 0.595 / 0.996 | 0.745 / 1.000 | 0.77 / 0.00 |
| cert0diag 10⁻³ | 0.586 | 0.699 | 1.00 |
| cert0diag 10⁻² | 0.625 | 1.000 (R = 5·10³, PrudentBot) | 1.00 |

- *cert0diag at c = 10⁻² locks in PrudentBot.* PB's copies are free; every non-copy pays to read PB; and PB punishes
  ALLC.
- *So the lock-in is universal, not parochial:* PB cooperates with FairBot. Its block is connected to FairBot's,
  though not a clique, because PB defects on FB1.

At n = 6 every variant is within 0.002 of c = 0 at every N. n = 6 has no P* (P* has 8 nodes), so it is a control.

## Design

ε→0 chain, PD, w = 0.3, `eager_poly=False`, θ = 10⁻⁶. Driver: `src/cert_limN.py`; outputs `runs/cert_pricing.md` and
`runs/cert_pricing.json`. At most 3 worker processes; 109 cells:
- **Main grid (72 cells):** pricing ∈ {cert0, cert1, certC, lazy} × c ∈ {10⁻³, 10⁻²}, plus c = 0, at n ∈ {6, 8} and
  N ∈ {10², 10³, 10⁴, 3·10⁴}.
- [after review] **Controls (32 cells):** mono, cert0flat, lazycert0 and cert0diag at n = 8, both c, all four N.
- [after review] **One larger N (3 cells):** N = 10⁵ at n = 8 for c = 0, cert0 at 10⁻² and lazy at 10⁻².
- [after review] **θ check (2 cells):** θ = 10⁻⁷ for cert0 and lazy at c = 10⁻², n = 8, N = 3·10⁴.

**Primary statistic: one universal network, or rival ones.** [after review: X first; ALLC excluded; cutoff
sensitivity; "within the enumerated language"]

- **Universality index X** (threshold-free, primary).
  - *Definition:* the π-weighted probability that two programs drawn independently from the cooperative π mass
    cooperate with each other. The mass is taken over monomorphic self-cooperating states, ALLC excluded.
  - *Values:* X is 1 for a single clique, and about Σ (block share)² for mutually defecting blocks.
  - *Status:* the population is monomorphic, so X is counterfactual. It asks whether two typical cooperative worlds
    would cooperate if they met.
- **Blocks** (structure).
  - *Construction:* connected components of the mutual-cooperation graph over those states, at π ≥ 10⁻³ and,
    as a sensitivity check, at π ≥ 10⁻⁴.
  - *Reported per block:* π mass, size, whether it is a clique, and whether its top program cooperates with
    FairBot. The mass below the cutoff is also reported.
  - *Rival share:* 1 − (the largest block's mass / the total block mass).
- **Labels.**
  - *Single network:* rival share < 0.05.
  - *Rival networks:* rival share ≥ 0.05.
  - *Parochial:* the dominant block's top program does not cooperate with FairBot, the reference universal
    cooperator.
- **Scope.** All of this is compatibility within the enumerated language L_8. A self-certifying but incompatible
  family that appears only at n ≥ 9 would not be seen.

**Also reported:**
- P(C,C), π(all-D) and π(ALLC);
- π(PrudentBot) [after review, fable 3c];
- the number of terminal and near-closed classes, the absorption error, polymorphic π and the cut flow;
- exits from the top cooperative state, split into strict, neutral and other, with the ALLC share;
- exits from the P*, BTT and nBM worlds, with their top destinations [after review];
- local log-slopes of the cooperative-to-D ratio [after review].

## Verdicts

1. **The references reproduce.** c = 0 and lazy match `runs/priced_limN.json` to within 10⁻³ in P(C,C) in every
   shared cell. This checks the driver, not the dynamics.
2. **n = 6 is inert.** Every certificate variant is within ±0.005 of c = 0 at every N and c.
3. **cert0 at n = 8 is c = 0 with the P\* block's excursions removed.** [after review, fable: replaces the band]
   - *Monotone:* P(C,C) rises in N at both c.
   - *The renewal identity holds:* P_cert0 = (P_c0 − p)/(1 − p) ± 0.01 at N ≥ 10³, where p is the P* block's π in
     the c = 0 cell at the same N (this run).
   - *Expected values* (c = 0 values in brackets): about 0.58 at N = 10⁴ (0.617) and 0.69 at 3·10⁴ (0.725).
4. **The primary question: cert0 gives one network, and it includes FairBot.**
   - *cert0, n = 8, both c, N ≥ 10⁴:* rival share < 0.02 at both cutoffs; the dominant block's top program cooperates
     with FairBot; X ≥ 0.9.
   - *c = 0, n = 8, N ≥ 10⁴:* rival networks. The P* block makes rival share 0.10–0.20, and X ≤ 0.85.
   - *Lazy 10⁻², n = 8, N ≥ 10⁴:* a single network (rival share < 0.01, X ≥ 0.95), but parochial: its top program is
     in the P* family and defects on FairBot.
   - *Lazy 10⁻³, n = 8, N = 3·10⁴:* rival networks, with rival share in [0.3, 0.55] and X ≤ 0.7.
5. **The P\* block loses its mass under cert0.**
   - *Mass:* π(P* block) < 0.005 at n = 8, c = 10⁻², N = 3·10⁴, and < 0.02 at c = 10⁻³. The references are 0.10–0.11
     at c = 0 and 1.0 under lazy at c = 10⁻².
   - *Exits:* P*'s exits under cert0 are at least 0.95 strict, at N-independent rates of 1.8·10⁻⁵ ± 20% (c = 10⁻²) and
     1.9·10⁻⁶ ± 20% (c = 10⁻³) at N ≥ 10⁴.
   - *Where they go:* the nBM world's exits are at least 0.9 strict, and D takes at least 0.8 of them.
   - [after review] *Classified by transition, not outcome:* the mass leaves through P* → nBM → D, not through a
     neutral drift.
6. **The top cooperative state is unchanged.**
   - Under cert0 it is FairBot or FB1 in every n = 8 cell at N ≥ 10³.
   - It has no strict exits.
   - Its neutral exit is within ±10% of c = 0's 4.9·10⁻⁴ / 4.9·10⁻⁵ / 1.6·10⁻⁵ at N = 10³ / 10⁴ / 3·10⁴.
   - ALLC takes at least 0.9 of its exits. The shadow is untouched.
7. **No absorption lottery, and the numerics are clean.**
   - Every cert0, cert1, certC and mono cell has one terminal class, no near-closed classes and an absorption error
     below 10⁻⁶.
   - The θ = 10⁻⁷ cells match θ = 10⁻⁶ within 10⁻⁴ in P(C,C).
8. **cert1 is the free arm.** Within ±0.01 of c = 0 in P(C,C) and ±0.03 in rival share at every cell. A looser level
   certifies P*'s self-play and restores c = 0's structure, rival P* block included.
9. **certC equals cert0,** within ±0.005 in P(C,C) and ±0.01 in rival share at every cell.
10. [after review] **mono equals cert0,** within 10⁻³ in P(C,C) at every cell.
11. [after review] **cert0flat equals c = 0.**
    - Within ±0.01 in P(C,C), with rival share 0.10–0.20, and P*'s exits neutral and ∝ 1/N.
    - So under a flat price the lock-in is gone (as at c = 0), but the rival P* block survives.
    - What removes the rival block under cert0 is the atom ladder acting only among non-monotone programs.
12. [after review] **lazycert0 equals lazy,** within ±0.01 in P(C,C) at every cell. The copy subsidy alone produces
    the lock-in, whatever the cross-program exemptions.
13. [after review] **cert0diag.**
    - *c = 10⁻³:* within ±0.02 of cert0.
    - *c = 10⁻², N = 3·10⁴:* P(C,C) ≥ 0.95, with PrudentBot holding at least 0.9 of the cooperative mass.
    - *Structure:* a single network that is not parochial, since PB cooperates with FairBot, but not a clique.
    - *At N = 10⁴:* 0.6–0.7.
14. [after review] **N = 10⁵.**
    - *c = 0:* 0.8135 ± 0.001, the same code as the ratchet run.
    - *cert0 at 10⁻²:* follows the renewal identity ± 0.015.
    - *Lazy at 10⁻²:* ≥ 0.999.
    - *Exponents:* from 3·10⁴ to 10⁵, the local log-slope of the cooperative-to-D ratio under cert0 is within ±0.05
      of c = 0's.

## Falsifiers

- *Of "cert0 removes the rival P\* block":* at cert0, n = 8, c = 10⁻², N = 3·10⁴, a block whose top program
  defects on FairBot holds at least 0.05 of the block mass, or π(P* block) is at least 0.05.
- *Of "certification gives no ladder to the monotone block":* at N ≥ 10⁴, strict exits are more than 10% of the
  cert0 top state's exits, or cert0's P(C,C) peaks in N at n = 8.
- *Of the renewal identity:* cert0 differs from (P_c0 − p)/(1 − p) by more than 0.03 at any N ≥ 10³. That would mean
  the P* block's removal reroutes mass, not just deletes excursions.
- *Of the mechanism attribution:* cert0flat loses the P* block (rival share < 0.05). The free set alone would then do
  it, and fable's ladder attribution would be wrong.

## What each outcome would mean

- **If 3–7 and 10–12 hold.**
  - *Lazy's lock-in is the copy subsidy.* Lazy pricing's P(C,C) = 1 was a parochial lock-in bought by the copy
    subsidy (12).
  - *Cross-program exemptions don't matter much:* "PA decides it" exempts nearly the whole monotone block. The
    exemption is equivalent to monotonicity (10), and with a flat price it changes nothing relative to c = 0 (11).
  - *What removes the rival P\* block is the atom ladder,* acting only on non-monotone programs, which pay at home
    while monotone ones do not.
  - *The result is one network that includes FairBot,* with cooperation approaching 1 only at the free arm's rate.
    The cooperative-to-D ratio grows like N^0.44–0.48, and the shadow exits at 1/N.
  - *The comparison, as an evaluation, not a selection:* complete but parochial cooperation (lazy) against universal
    but slower cooperation (cert0).
  - [after review, fable] *Proposed wording for THEORY §9.2's realizable condition:*
    - no price for checking constants or monotone, box-positive cooperation, which certifies itself;
    - no price advantage for the shadow;
    - only cooperation conditional on non-provability pays.

    A compute price can then remove a non-monotone rival network without parochialism. It cannot by itself beat the
    shadow's 1/N drift.
- **If 13 holds.** Copy subsidies lock in whatever ALLC-punishing family they reach: parochial P* under lazy,
  universal PrudentBot under cert0diag. Incumbency is then a tool, and the question becomes which family it reaches
  first. That depends on prior mass and is not a property of the price.
- **If the P\* block survives cert0.** Then removing the copy subsidy is not enough. The open question in §9.2,
  "whether any pricing yields one cooperative network", would lean toward no in the well-mixed ε→0 chain.
- **If the renewal identity fails downward.** Then the new rung drains more than the P* block holds, and pricing
  non-monotone cooperation costs cooperation rather than reassigning it.

## Smoke tests run before commit (declared)

- **cert0, n = 6, c = 10⁻², N = 10²:** P(C,C) 0.1690, against 0.1693 at c = 0. One block, FairBot's (ALLC excluded),
  with X = 0.99. The top state's exits are all neutral, 0.96 ALLC.
- **cert0v, n = 6, c = 10⁻², N = 10²:** run only to check the report writer. P(C,C) 0.1665. Its top state's exits
  were already 96% strict (ALLC), the ladder.
- **Static scripts:** they used `Chain.expand` on single states only.
