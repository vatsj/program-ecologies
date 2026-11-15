# The social organization game: static acceptable outcomes in program space (2026-11-15)

Motivated by the RS's decision of 2026-11-15 (one target: strong Nash in program space where it exists, the stable
set where it does not). Question: does the fair wage have static backing? Code: `src/sog_static.py`.

**Setup.** Boss picks a wage s ∈ {0, ¼, ½} and whom to whack; each of two workers works or strikes. Payoffs as in
`src/union.py` without tags or the replacement pool (L = 1; c ∈ {0.1, 0.5, 1.5}). Deviation without response: the
others' programs stay as written. Because the reading regress between a rewriting coalition and the fixed text is
not resolved in the theory, two brackets are computed: deviators as constants facing any punishment the fixed text
carries (α-blocking), and deviators that read and move last (β-blocking).

**Prediction, made before the computation (RE):** every wage with both working and no whack is acceptable; the
notion does not select the fair wage. Held.

**Result.**
- The two brackets agree at every c, under strict and weak domination, so the regress does not matter in this game.
- Under weak domination the acceptable outcomes are exactly three: both work, nobody whacked, at s = 0, ¼ or ½.
- Under strict domination (the operating relation) at c = 0.1 and 0.5, four more
  survive: both work at s = 0 or ¼ with one working worker whacked. They are held by the *other* worker's text
  (it strikes if the boss and the victim renegotiate), and the grand coalition cannot strictly improve the bystander.
  They vanish at c = 1.5 and under weak domination; a strict-relation artefact.
- Supporting profiles: zero wage needs no threat (constants suffice: a lone striker gains nothing, strictly). The
  fair wage needs the workers' text to strike below ½; the boss's whack is never needed for any acceptable outcome.

**Reading.** The strong pair is nonempty, so the stable set does not come into play. The static target for this
game is "both work, no whack", with the wage unselected. The fair wage is a member, not the prediction: which wage
holds is a selection question (founding and the tail), which matches the record that the fair state is a
prior-and-seeding property. Not computed: the replacement pool, mixed actions, more wage levels.
