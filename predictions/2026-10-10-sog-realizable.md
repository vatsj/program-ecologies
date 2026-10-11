# Predictions: the social organization game over the realizable language (2026-10-10)

Spec `specs/2026-10-10-sog-realizable.md` (sol review folded in). Committed after `notes/sog-realizable.md` §1.1–1.3
(the calculus K₃, the grammar, the prior, the frozen conventions) and **before** the static invasion analysis (§1.4),
any table code, and any counted cell. Any prediction added after the static tables is labelled *conditional*.

## The RE's predictions (verbatim from the spec)

1. **The library makes the concession cheap.** Under L, D\*'s mass is within 2⁻⁸ of a constant boss's (my bet 2⁻⁶)
   and the militant T₁'s within 2⁻⁴ of the constant striker's. *Falsifier:* D\* below 2⁻¹² of a constant.
2. **No false-certificate faker** [revised after review]: no boss class gets work from a militant at a wage below
   1/2 through an accepted false atom (0 by soundness), and no class reproduces the modal probe wage faker; low-wage
   work that does occur is by timeout or substitution, and each case is classified. *Falsifier:* a false-certificate
   faker; a substitution faker is a miss of the design (the probe semantics), recorded separately.
3. **Establishment is set by the founding-coalition mass, and the library raises it** [revised after review]: the
   mass of compatible executable founding coalitions under L exceeds the modal run's by ≥ 10³, and establishment
   conditional on co-seeding is ≥ 0.5; the unconditional establishment fraction at (100, 64) is my bet, not a
   derived number: ≥ 0.6 within 200 generations (modal run 0/40), with the expanded-syntax prior at ≤ 0.2 on the
   same dynamics. *Falsifier:* coalition mass within 10× of the modal run's, or establishment conditional on
   co-seeding ≤ 0.2, or the expanded-syntax prior establishing at least as often as L.
4. **The one-slot leak survives, so persistence is partial.** The run-level mean fraction of islands fair at the
   horizon is between 0.2 and 0.6, and the dominant exit of dying fair islands is unread-slot drift followed by a
   boss cut (≥ 0.5 of exits). *Falsifier:* persistence ≥ 0.8 (the leak is gone) or ≤ 0.1, or the dominant exit a
   false certificate.
5. **D\*₂ (both slots), if it fits, lengthens residence** [revised after review]: the migration-off residence time of
   islands held by D\*₂ with militants in both slots is ≥ 5× that of D\* islands on matched seeds, and that state has
   no strict invader; persistence with migration on is higher than D\*'s but need not exceed 0.9. *Falsifier:* a
   strict invader of that state, or residence within 2× of D\*'s.
6. **RR keeps the 1/4 wage,** conditional on the derived RR play table showing that the 1/4 probe certifies no
   rational worker: wage 1/4 on ≥ 0.7 of islands (modal run 0.90). *Falsifier:* fair ≥ 0.3 of islands under RR; if
   the derived table shows the 1/4 probe certifying rational workers, the prediction is void and the table is the
   result.
7. **The chain still says zero wage** (diagnostic): π(fair) at N = 10⁴ ≤ 0.1 under L. *Falsifier:* ≥ 0.3.

*Notes on scoring, fixed now.* D\*₂ does not fit n = 7 (11 nodes, notes §1.3.3); RE 5 is scored on the forced cells,
where D\*₂ is a named out-of-catalogue class. RE 6's condition is scored on the derived RR table of notes §1.3.4: under
the realizable semantics (certificates are about runs, i.e. recommendations) the 1/4 probe certifies the militant's
*recommendation* to strike, so by the notes' reading the condition fails and RE 6 is void, with the table as the
result; the RR cell is still run and reported, and the modal-matched variant (probes read executed actions), where
the condition holds, is run as a labelled extra and RE 6's number is reported on it beside the void verdict. "Mass"
in RE 1 is scored on aggregated class masses (the spec's "a class's mass is the sum over its sources"), with the
spelling-level ratios reported beside it. "Within 200 generations" in RE 3 is scored on the establishment time
defined in notes §1.3.7 (end of the first 10-check fair window).

## Hand numbers (from notes §1.1–1.3, before any table)

- **Spelling masses under L** (2^−nodes, normalized per role; Z_B = 1,214.44, Z_W = 14.281): each boss constant
  4.12·10⁻⁴; D₀, D14, WF 5.1·10⁻⁵; D14₂ 1.3·10⁻⁵; **D\* 6.43·10⁻⁶ = 2⁻⁶ of a constant** (modal 9.7·10⁻⁹ / 0.1025 =
  2^−23.3: a factor 2^17.3 ≈ 1.6·10⁵ at the spelling level); scab, striker 0.0350; **T₁, T₀, R, Q 4.38·10⁻³ = 2⁻³ of
  the striker**; U 5.5·10⁻⁴.
- **Expanded syntax:** atom sizes B≥¼, B≤¼ 37, B½ 31, O-atoms 27, P^0 60, P^¼ 86; T₁ 34 nodes (2⁻³³ of the
  striker), D\* 151 (2⁻¹⁵⁰ of a constant). The expanded prior is constants-only to within 2⁻³⁰.
- **Aggregated masses, hand estimate:** each constant boss *class* gathers its syntactically constant spellings
  (`if(p, X, X)`, `if(and(p, q), X, X)`, …): ≈ 7.4/Z_B ≈ 6·10⁻³ per constant action (15× its spelling); D\*'s class
  ≈ 1–2 spellings; so the aggregated D\*/constant ratio is ≈ 2⁻⁹ to 2⁻¹⁰, below the spelling ratio. The untagged
  striker class ≈ 0.12, the untagged militant class (wage function S S W: T₁, R and their respellings) ≈ 0.03, so
  T₁/striker ≈ 2⁻².
- **Founding coalitions, hand estimate.** (D\*, T₁, T₁) has no strict invader, but so do (pay(½, h), T₁, T₁) and
  (pay(½, h), T₁, scab) in either slot order (the boss's best payoff against a militant beside anything is 1; no
  worker earns above ½); (pay(½, h), scab, scab) does not (pay(0) earns 2). In the modal run the same shapes with
  militant⁻ are the unfakeable ones (the modal militant T₁ has strict faker invaders): 3 × 0.1025 × (2 × 1.2·10⁻³ ×
  0.48 + (1.2·10⁻³)²) ≈ **3.6·10⁻⁴**, almost all constant fair bosses beside one militant⁻ and a scab. Realizable
  under L: ≈ 3 × 6·10⁻³ × (2 × 0.03 × 0.12 + 0.03²) ≈ **1.4·10⁻⁴**. **The concession is not what founding
  coalitions are made of**, in either language: the constant fair boss beside one militant carries the sum, and
  the template prior dilutes constants (6·10⁻³ against the modal 0.1025) as much as it cheapens D\*.
- **Seeding arithmetic, hand estimate** (islands of 100 per slot, payoffs at seeding with every wage about equally
  likely from the boss soup and a third of bosses strike-targeting): a scab earns ≈ E[s] ≈ ¼; T₀ ≈ ¼ − 0.11 = 0.14;
  the militant ≈ ½·⅓ − ⅔·⅓ = −0.06; the striker ≈ −⅓. Scabs grow first, then bosses that pay 0 to scab pairs.

## The subagent's predictions (numbered S1–S12, each with a falsifier)

S1. **Static, masses.** Aggregated D\*/constant boss class ratio under L is in [2⁻¹¹, 2⁻⁷] (bet 2⁻⁹), so RE 1's D\*
    clause misses its number (≥ 2⁻⁸) but its falsifier (< 2⁻¹²) does not fire; T₁/striker class ratio in [2⁻⁴, 1]
    (bet 2⁻²). *Falsifier:* D\*/constant outside [2⁻¹², 2⁻⁶], or T₁/striker below 2⁻⁵.
S2. **Static, soundness and fakers.** 0 false accepted atoms in every audited check (term and host); 0 boss classes
    get work below ½ from the militant class (Lemma 0₃); WF plays (0; S, S) against the T₁ pair; low-wage work in
    the catalogue occurs only as *uncertified default* (never false certificate, timeout or substitution), and only
    for workers whose work leaf sits on an F-branch, with prior mass of the affected (boss, worker) pairs < 0.01.
    *Falsifier:* any false accepted atom; any low-wage work classified as timeout or substitution inside the
    catalogue.
S3. **Static, the fair state.** F\* = (D\*, T₁, T₁) has no strict invader; its neutral substitutes include the
    scab in slot 2 (the one-slot leak), and after the scab fixes there, pay(0, none) enters neutrally (not
    strictly). *Falsifier:* a strict invader of F\*, or a strict boss cut at (D\*, T₁, scab).
S4. **Coalition mass.** The compatible-founding-coalition mass under L is within a factor 30 of the modal run's
    (bet: 0.1–3×), and concession bosses (classes paying ½ to the T₁ pair and less to the scab pair) carry < 5% of
    it; under U it is larger than under L; under the expanded prior it is the constants-only value. So RE 3's
    first clause (≥ 10³) fails. *Falsifier:* L/modal ratio ≥ 100, or concession share ≥ 0.2.
S5. **Lottery, L main (100, 64).** Establishment (end of a first 10-check fair window) in ≤ 0.35 of runs (bet 0.15);
    run-level mean persistence ≤ 0.1; zero wage the plurality summary on ≥ 0.6 of islands at the horizon. RE 3's
    ≥ 0.6 and RE 4's [0.2, 0.6] therefore fail. *Falsifier:* establishment ≥ 0.6, or persistence ≥ 0.2.
S6. **Lottery, expanded-syntax prior.** Establishment ≤ 0.05 and zero wage ≥ 0.7 of islands: it reproduces the
    modal seed lottery (constant boss, scab and striker seeds). Expanded ≤ L on establishment. *Falsifier:*
    expanded establishment > L's, or ≥ 0.2.
S7. **Lottery, U and the (N, I) panel.** U establishment within 0.25 of L's; L at (200, 64) and (100, 256) within
    0.2 of L at (100, 64) on establishment and persistence. *Falsifier:* a difference ≥ 0.4 in either.
S8. **Militants in numbers** (the striker class's mass moved onto the untagged militant class, L): establishment
    ≥ 0.5 of runs (bet 0.8) and persistence in [0.05, 0.5]; ≥ 0.5 of the surviving fair islands held by a
    concession boss rather than a constant fair boss. *Falsifier:* establishment < 0.3, or persistence > 0.6.
S9. **Exits.** Of fair islands that die (all cells pooled, run-level), the dominant exit is a worker-slot drift
    (scab or other non-militant into a militant slot) before the boss changes, ≥ 0.5 of exits, and no exit is a false
    certificate, timeout or substitution. *Falsifier:* false-certificate/timeout/substitution exits > 0, or worker
    drift < 0.3 of exits.
S10. **Forced D\* vs D\*₂.** On matched seeds (20 forced concession bosses per island, workers from the
    militants-in-numbers prior), D\*₂ islands' migration-off residence is ≥ 3× D\*'s (bet: D\*₂ censored at the assay
    cap on ≥ 0.5 of islands); (D\*₂, T₁, T₁) has no strict invader; with migration on, D\*₂'s persistence exceeds
    D\*'s by ≥ 0.1. *Falsifier:* residence ratio < 2, or a strict invader.
S11. **RR.** Realizable semantics (main): the 1/4 wage is the plurality on ≥ 0.6 of islands and fair ≤ 0.1;
    the modal-matched executed-probe variant: the same within 0.15. *Falsifier:* fair ≥ 0.3 in either.
S12. **Chain (N = 10⁴, L).** π(fair) ≤ 0.05, zero wage ≥ 0.4, and the fair basin's exits are neutral (∝ 1/N), the
    leading one the unread slot; π(fair) under the cut-corrected reading ≤ the explored one. *Falsifier:* π(fair)
    ≥ 0.2, or a strict fair exit carrying ≥ 0.5 of the fair escape.
S13. **Faker re-injection and concession ablation** (controls defined now): (a) a synthetic out-of-language faker
    WF\* (pays 0, plays as if paying ½ against every pair containing an untagged militant: the modal false-certificate
    effect) injected at the modal strict faker mass 0.0116 of the boss prior lowers L-main persistence by < 0.05 in
    absolute terms when persistence is low, and lowers the militants-in-numbers persistence by ≥ 0.1; (b) nulling the
    concession bosses (classes paying ½ to the T₁ pair and less than ½ to the scab pair, mass redistributed
    proportionally) lowers the militants-in-numbers persistence by ≥ 0.1 and leaves its establishment within 0.15.
    *Falsifier:* (a) the re-injection lowering militants-in-numbers persistence by < 0.03, or (b) the ablation
    raising persistence.
S14. **Scale and costs.** Worker classes after lumping 60–250 per slot; boss classes 2,000–30,000; the executable
    D\*-check (T₁ checking D\* in F\*) costs 3·10⁴–1.5·10⁵ steps, below V, and executable = ideal on every named
    encounter at K = 10⁶; at K = 3·10⁵ some named encounter changes. *Falsifier:* the D\*-check above V at K = 10⁶.
