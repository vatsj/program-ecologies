# Spec: identity and tags in the carrier grammar: does the seed lottery reward families over cliques?, 2026-10-10

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol; to be run by an Opus subagent. Follow-up to RESULTS
"The realizable language, milestone 2" and the RS's decision of 2026-10-10 (DEFERRED 1: the seed lottery is the
object; universal cooperation is the target; identity cliques are cooperation but not the target).

## Why

Milestone 2 found that the checker's self-recognition gives a 6-node CliqueBot that absorbs the ε→0 chain, while the
seed lottery was won by FairBot-shaped carriers. The RE's rationale for seeds as the object is a **pooling
argument**: iid seeds draw spellings; a universal family pools its seeded mass across every spelling that cooperates
with the others, while an exact-identity clique cannot, since each of its spellings is a species of its own and they
defect on each other. Two things make this contingent. (i) Milestone 2's grammar had no `eq`, so the clique's mass
(7·10⁻⁴) understates the real language, where `if eq(me, them) then C else D` is as short as FairBot. (ii) Parochial
clubs that recognize a *family* rather than a copy do pool: a tag club ("cooperate iff your source carries tag t")
and an exclusive club ("cooperate iff you certify cooperation with me and certified defection against the open
carrier CB"). Tag clubs should be bridged (a tagged carrier cooperates with both) and bridged rivals resolve;
exclusive clubs are bridge-less by construction (RESULTS "Bridge-less rivals"). The run tests the pooling argument
directly, with the clique made as cheap as FairBot, and measures what pooled clubs do to universality in the lottery.

## Design

**Grammar.** Milestone 2's template grammar (`src/carrier_populations.py`: `C | D | if(B, A, A)` over check atoms
`CHK(p, q, a)` under `not/and/or`, cutoff n = 7, K = 10⁶, V = K/4, public production, entry 0 only) extended by:
- the **identity atom** `eq(me, them)` (one node; structural quote equality, one evaluator step);
- **tag atoms** `tag_t(them)`, t ∈ {1, 2} (one node): true iff the opponent's source carries marker t, where a marker
  is a no-op subterm (`(λx.x) ⌜t⌝` wrapped around the body) that costs one node and changes no play; every program
  may carry 0, 1 or 2 markers;
- the **named quote** ⌜CB⌝ in check atoms (q ∈ {me, them, ⌜C⌝, ⌜D⌝, ⌜CB⌝}), so the exclusive club "cooperate iff
  `CHK(them, me, C)` and `CHK(them, ⌜CB⌝, D)`" is expressible at 7 nodes.
Named classes to track: CB; the eq-clique `if(eq(me,them), C, D)` (4 nodes); TwinD; the tag clubs
`if(tag_t(them), C, D)` with and without own marker; **the marked carrier** (CB with marker t: it carries the tag, so
the tag club cooperates with it, and it checks certificates, so CB cooperates with it and it cooperates with the
tag club through the club's valid "I cooperate with tagged you" script; it is not exploitable by marked D because it
checks) [after review: the bridge candidate; the and-form `if(and(tag_t(them), CHK(them,me,C)), C, D)` is *not* a
bridge, since it defects on the unmarked CB, and the or-form `if(or(tag_t(them), CHK(them,me,C)), C, D)` bridges but
cooperates with marked D, so it is a bridge that is exploitable]; both of those forms are still tracked; the
exclusive club above; the prudent exclusive club `if(and(CHK(them,me,C), CHK(them,⌜C⌝,D), CHK(them,⌜CB⌝,D)), C, D)`
if it fits n = 7, else noted. [after review] **Markers:** a program carries 0, 1 or 2 markers, each costing one node
under L; the marker is part of the source, so it enters quotes, `eq` and certificates (a marked CB's scripts are
produced for its marked source; the tactic is opponent-generic, so a script's validity does not depend on the
opponent's markers). Every named class's reciprocal plays (CB, both tagged forms, the marked carrier, marked and
unmarked tag clubs, marked D, the eq-clique and one respelling of it) are hand-checked in notes §1 before any
bridge is declared non-exploitable.

**Static.** The class catalogue. [after review] **Lumping is identity-aware:** two spellings merge only if no program
in the catalogue distinguishes them, including identity-sensitive and tag-sensitive opponents and their own
within-class plays; spellings of the eq-clique are therefore separate classes (each defects on the others), marked
and unmarked spellings are separate, and the lottery and chain run on these exact identities. **Families** [after
review: mutual cooperation is not transitive, so components would merge the rivals whose separation is measured]:
report (i) the compatibility graph among self-cooperating classes, (ii) its **pairwise-compatible sets** (maximal
cliques of the graph: the pooled families), each with its pooled seed mass and spelling count, (iii) **bridge-mediated
connectivity** (components of the graph) separately, and (iv) for the lottery, the actual occupied supports. A
"clique" in the parochial sense is a pairwise-compatible set of one class. For each pair of pairwise-compatible sets,
whether a **bridge** exists (a class cooperating with every member of both), its mass, and whether it is exploitable
(a strict invader among the classes present). The eq-clique's spelling mass against CB's spelling mass. The leak
test (drift-closed components). [after review] Normalized spelling weights under L are stated explicitly (2^−nodes
over the catalogue including markers).

**Priors.** L (2^−nodes, milestone 2's form) is main; U (uniform over classes) as the control. **Mass tilts**
(seed-composition interventions, as in RESULTS "The social organization game under the seed lottery"), each
renormalizing the rest and run on paired seeds: [after review: the pooling test is a matched comparison of equal
total mass, not one tilt] **(T1a)** the open carrier family's pooled mass M given to *one* identity (the eq-clique's
exact spelling); **(T1b)** the same M spread equally over ten mutually incompatible eq-clique spellings; **(T1c)** the
same M spread equally over ten mutually compatible carrier spellings (CB respellings), the carrier family otherwise
removed; T1a against T1c is the "one identity vs compatible family at equal mass" comparison and T1b against T1c is
the pooling comparison proper. **(T2)** tag club 1 given M; **(T3)** the exclusive club given M. [after review]
**Ablations**, paired seeds: identity-only (no tags, no ⌜CB⌝), tags-only, named-⌜CB⌝-only, each under L at (100, 64).

**Lottery** (primary; `src/islands.py` conventions, endpoint E3 of milestone 2, horizon 2,000, Wilson intervals):
(N, I) ∈ {(100, 64), (200, 64), (100, 256)} at mN = 1 under L; (100, 64) under U and under each tilt; 40 runs per
cell. Report: the fraction of runs in which the open carrier family holds every island (universal), in which the
islands are split between families at the horizon (a patchwork, naming the families and whether a bridge was alive),
in which a clique or club holds every island; establishment generation; for tag clubs the fate of the bridge (its
extinction time where it dies); for the exclusive club the separation hazard and whether any separated run resolved.
[after review] **Universality is measured directly** as cross-island P(C,C) at the horizon (every ordered island pair,
expected play between their holders), beside open-carrier occupancy. **Censoring:** a run not resolved by the horizon
is censored, not scored; separation and resolution hazards are estimated from the separated runs, and separated
runs are extended to a horizon of 10,000 generations (reported as a separate column); the (N, I) panel is finite-size
evidence, labelled so. Also the **pooling check**: for each run, the seeded count of every pairwise-compatible set
*per island* and globally, whether the set with the largest global seeded count won, and whether the set with the
largest *established* mass (founders alive at the first checkpoint after every island is established) won, so that
raw counts and established mass are compared as predictors.

**Chain** (diagnostic only): L at N = 10⁴, closure-seeded `chain_log`, to confirm absorption and name the absorbing
clique; the no-clique control at 10⁴ for the mechanism (odds slope from 10³ and 10⁴ only).

**Scale guard.** Report the catalogue size and class count before any table; if classes exceed 2,500, the run with
the second tag and the or-form removed is a *different experiment*, reported as such and never as confirmation of a
prediction made for the full grammar [after review]. ≤ 3 workers; kill pool children by pid before the driver.

## Required outputs

`src/identity_tags.py` (grammar extension, families, bridges, tilts, the pooling check), `src/identity_tags_run.py`,
`src/identity_tags_report.py`, `tests/test_identity_tags.py` (the eq atom and markers in the evaluator; lumping
exactness; the named classes' hand plays; family extraction on a small catalogue), `notes/identity-tags.md` (§1 the
grammar, the named classes' hand plays, the hand-derived families and bridges, the pooling argument stated as a
calculation before any cell; §2 costs), `runs/identity-tags.md` and `.json`, a predictions file from the spec
committed after §1 and before any counted cell, the usual hand-back (draft RESULTS, REJECTED, THEORY §9.2 and
DEFERRED 1/11 edits, NOTATION, ≤ 5 lines, branch name, commits).

## RE predictions (with falsifiers)

[after review: every prediction has a success range and a falsifier range that meet, so no outcome is unclassified;
an outcome in neither is a miss of the number with the mechanism scored separately.]

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

The RS is invited to add predictions. The uncertain ones are 3 (T1a) and 4 (whether the marked carrier is alive when
the rivalry forms).
