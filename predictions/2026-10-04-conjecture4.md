# Predictions: Conjecture 4 and the leak bound, 2026-10-04

Spec: `specs/2026-10-04-conjecture4.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-04-conjecture4-gpt-6.1-sol.md`).
Committed before the extended static runs (n = 12, 13) and before the n ≤ 11 reproduction.

**Done before this commit** (so not predicted):
- the proof attempt in `notes/conjecture4.md`. It gives Theorem 1 (every self-cooperating class has a suckerable
  neighbour in G, in the evaluator semantics with unbounded box levels) through a sibling y = or(x, ψ_K), where ψ_K is
  "your play against DefectBot is undecided at level K" and the faker is z = BOX_K(THEM(^D));
- `src/conj4.py`: an independent trace evaluator and a check of the sibling for every self-cooperating canonical
  function of L_n at n/lmax = 6/1 … 9/1 and 6/2 … 8/2 (0 failures; 0 disagreements with `modal_lv` on 3,000 random
  pairs per language).

So verdict 1 below is decided by the proof, not by a run. It is kept here as Fable wrote it, with its mechanism
clause scored separately.

## Measure (as `src/moat_static.py` computes it)

- *Prior.* Program p of size s has mass 2^(−bits), bits = log2 a(s) + 2 log2 s + 1, where a(s) is the number of
  programs of size s; so each length shell has total mass 1/(2s²). Masses are normalized over L_n (sizes ≤ n).
- *Classes.* Canonical boolean functions of box atoms (exact behavioural equivalence, `modal.ModalLanguage`), then
  merged by identical payoff row and column against all of L_n (`modal.ModalProvider`). So the equivalence relation
  is "plays identically with and against every program of size ≤ n", relative to the cutoff.
- *μ(x)*: the normalized mass of x's class.
- *Direct leak ℓ(x)*: the mass of x's mates (self-cooperating classes in mutual cooperation with x) that are
  suckerable by some class of L_n. *Closure leak*: the mass of all suckerable members of K(x).
- *Shell contribution*: the part of ℓ(x) carried by programs of size exactly s (unnormalized, so shells are
  comparable across n), computed from per-size counts of each canonical function.

## RE predictions (Fable, from the spec)

1. **Conjecture 4 holds** for the full language, through a sibling construction (the bottleneck being closure
   membership). *Falsifier:* a counterexample proved closed against the full language and checked by the evaluator.
   A truncation-closed candidate at n = 12 or 13 is evidence against, not a falsification.
2a. **Lemma 1 and Corollary 1 transfer** to deterministic programs with bounded proof search over source.
   *Falsifier:* a step in either proof that needs the linear chain or full GL.
2b. **The sibling construction transfers only under budget assumptions**, above an explicit threshold to be stated in
   proof lengths. *Falsifier:* a step with no bounded analogue at any budget.
3. **FairBot is leak/μ-optimal at n = 12 and 13,** with direct leak/μ in [85, 105], and the shell contribution to
   its direct leak decays geometrically (ratio of successive shells below 0.7 from n = 10 on). *Falsifier:* another
   unsuckerable class with smaller leak/μ at either n, FairBot's ratio outside the interval, or shell contributions
   that do not decay.
4. **No drift-closed class at n = 12 or 13.**

## Subagent predictions (made after the proof, before the runs)

S1. *Mechanism of 1.* Fable's sibling φ is "a provable-cooperation test". I expect it to be scored **failed as a
   mechanism**: the working ψ is an *undecidedness* test (two negated boxes), non-monotone, and closure membership comes
   from mimicry on finitely many probes, not from Löb. The conclusion of 1 holds.
S2. *2a* holds: Lemma 1 and Corollary 1 use only determinism, distinct PD payoffs and the fixation rule.
S3. *2b* holds in the form "budget-dependent": the mimicry step needs the reader's proof budget to exceed the
   sibling's extra proof cost; a reader with tight budgets can reject every sibling.
S4. *Static map at n = 12 and 13* (if they fit): one component of G, no drift-closed class, max drift distance 1
   (as at n ≤ 11).
S5. *FairBot leak/μ:* 92.0–92.7 at n = 12 and 91.7–92.6 at n = 13 (the n = 6–11 sequence is 96.3, 94.4, 93.5,
   93.1, 92.7). FairBot stays the minimum, but `BOX1(THEM(ME))` stays within 0.1% of it (0.03% at n ≤ 11).
   *Falsifier:* any class below FairBot, or FairBot outside [91.5, 92.8].
S6. *Shells:* the shell contributions to FairBot's direct leak do **not** decay geometrically. Each shell has total
   prior mass 1/(2s²), so if a roughly constant fraction of shell s is a suckerable FairBot mate, successive ratios are
   about (s/(s+1))² ≈ 0.83–0.85 at s = 10–13. I predict ratios in [0.70, 0.98] from s = 10 on, so prediction 3's
   shell clause fails. *Falsifier:* ratios below 0.7 at s = 12 and 13.
S7. *Uniform bound:* leak/μ(FairBot) is bounded uniformly in n for a trivial reason under this prior: leak ≤ Σ 1/(2s²)
   = π²/12 and μ(FairBot) ≥ m(FairBot) = 1/324 (unnormalized), so leak/μ ≤ 27·π² ≈ 266. The question with content
   is the limit value, which the shells bound: the unseen tail adds at most about 162/n to the ratio.
