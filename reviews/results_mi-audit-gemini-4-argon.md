# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/results_mi.md` by gemini-4-argon

1. **Unreported statistics and unsupported trajectory numbers.**
   - *Draft sentences:* "The exception is M A = 0, whose symmetric chain peaks at 0.977 and collapses onto unequal pairs (U 0.898 by 1.7·10⁴)." / "The outcome-class flow among fair pairs is restoring (the net flow anticorrelates with the share difference, −0.69 in L A = 0)..." / "...a fair monoculture can later be replaced by an unequal one (an F0-tilted pool: F2 0.78 at 10⁴, U 0.998 by 1.7·10⁴). M A = 0's dip is pool 1 consolidating on an unequal pair (V\* 0.790 → 0.141)..."
   - *Evidence:* In `runs/many-islands.md`, Table 3 reports the M A = 0 symmetric chain only at checkpoints 1,000, 3,000, 10,000, and 30,000 (where V\* is 0.4939, 0.7667, 0.8167, and 0.1003; U is 0.8979 at 30,000). Neither the 0.977 peak nor a 1.7·10⁴ checkpoint appears in the report. Similarly, the −0.69 anticorrelation, the F0-tilted pool's F2 and U shares at 10⁴ and 1.7·10⁴, and M A = 0 pool 1's individual V\* trajectory (0.790 → 0.141) do not appear in `runs/many-islands.md`.
   - *Correction:* Add these trajectory checkpoints, per-pool figures, and the flow-share correlation to `runs/many-islands.md`, or restrict the draft text to numbers present in the report tables (e.g., M A = 0 symmetric chain reaching 0.817 at 10⁴ and U 0.898 by 3·10⁴).

2. **Omission of A = 150 rates in the single-migrant summary.**
   - *Draft sentence:* "Single-migrant rates on fair islands, symmetry-averaged per event: κ (to the donor's pair) 4.5·10⁻⁴ and α (to the third pair) 6.0·10⁻⁵ in L and M, 3.6·10⁻³ and 3.5·10⁻⁴ for readers; α/κ 0.09–0.13, every interval excluding 0."
   - *Evidence:* `runs/many-islands.md` §7 shows that the quoted κ and α values are for A = 0 only (L A = 0: 4.51·10⁻⁴, 5.9·10⁻⁵; M A = 0: 4.55·10⁻⁴, 6.1·10⁻⁵; R A = 0: 3.58·10⁻³, 3.50·10⁻⁴). At A = 150, κ and α are 4.24–4.29·10⁻⁴ and 5.3·10⁻⁵ in L and M, and 2.22·10⁻³ and 2.10·10⁻⁴ in R.
   - *Correction:* Specify "at A = 0" for the point estimates, or state the ranges across both A = 0 and A = 150 (e.g., 2.2–3.6·10⁻³ and 2.1–3.5·10⁻⁴ for readers).

3. **Coefficient of variation range understated.**
   - *Draft sentence:* "...per-recipient exit hazards vary with coefficient of variation 1.5–2.0..."
   - *Evidence:* `runs/many-islands.md` §7 reports CV for F and U across the six cells ranging from 1.48 (F in L A = 0) to 2.29 (U in L A = 150; 2.28 in M A = 150; 2.15 for F in R A = 150).
   - *Correction:* Change "1.5–2.0" to "1.5–2.3" (or specify "1.5–2.0 in L and M at A = 0").

4. **Readers fair-endpoint threshold overstated across A.**
   - *Draft sentence:* "R reaches V\* ≥ 0.999 from every start and 10/10 fair endpoints from I = 1,024..."
   - *Evidence:* `runs/many-islands.md` §4 shows R A = 150 reaches 10/10 fair endpoints already from I = 256 (R A = 0 is 9/10 at I = 256 and 10/10 from I = 1,024).
   - *Correction:* Clarify as "10/10 fair endpoints from I = 1,024 (and from I = 256 at A = 150)".
