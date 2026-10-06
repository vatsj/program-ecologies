# Predictions: the realizable language, milestone 4: certificates as code (2026-10-06)

Spec `specs/2026-10-06-certificates-as-code.md` (reviewed by gpt-6.1-sol; the [after review] text is the resolution).
Committed after `notes/certificates-as-code.md` §1 (commit 605fb1d) and before any code of this milestone, any
measurement and any counted cell. Every number below is a hand calculation from notes §1 or a guess labelled as such.

## Frozen design (notes §1)

1. **Language:** L_T^code unchanged; library = milestone 3's (indices unchanged) + check wrappers
   `CHK_x = λarg. if eq(capk(fst arg, CC_x, arg), T) then T else F`, arg = (V, (t, (m, (a, K)))), cost ≤ V + 6, and
   check cores CC_x for x ∈ {0 sound, 5 sound copy, 1 naive, 2 self-only, 3 none, 4 sloppy}.
2. **Carriers:** `λme.λthem.(λcerts. BODY) CERTS`, CERTS a literal list of (a, script); scripts are derivation
   skeletons, the checker rebuilds every formula from the root it builds out of the two quotes (Lemma F: explicit
   self-certificates are not finite data). No opponent key: entries for the asked outcome are tried in order.
3. **K_T^cert:** Ax, EvR* (deterministic steps to the next call or value), ChkR (check-call state, fit: every counter
   ≥ V′ + 6, readings ⇓⁺ at the minimal residual), Run/RunNeg (never on R or S; cap ≥ the root's), Hyp^self (closes R),
   Hyp^pair (closes S = the swap of the root; modes 0 and 5 validate the partner's script one level with {R, S}). No
   rule for search calls.
4. **Check:** `ccore(x, arg)` = vone(arg; R, S), then, in modes 0 and 5 when the accepted script closed S ≠ R,
   vone(swap arg; S, R). Mode 4 accepts iff an entry for the outcome exists.
5. **Production (frozen, host, not charged):** the deterministic tactic of notes §1.9 (Ax, Hyp, RunNeg, Run, then the
   first right atom: EvR* or ChkR), bound 64 nodes, probes CB, CB1, CBP (and ⌜D⌝ for D scripts), two passes;
   every produced script re-validated by the checker term.
6. **Catalogue** at K ∈ {10⁵, 10⁶, 10⁷}, V = ⌊K/4⌋, k = ⌊K/2⌋. Arm S (sound): C, D, Ccert, Dcert, CB, CB1, CBP, CBlet,
   CBwrap, CB0 (sound code, empty list), CBfake, CBdef, CBmut, LöbC, CBsloppy, CBN, CBN0, CBS2, SF, SFc, FB_code,
   FB1_code, PB_code, G_code (milestone 3's, b = 16, U = ⌊K/4⌋), and the held-out CBlet2, CBw2, CB1h, CB1r, CBPh,
   CBPr. Arms O (self-only) and X (none): CB, CB1, CBP, CBlet, CBwrap, CB0 with the arm's checker, plus C, D, Ccert,
   Dcert, SF, SFc.
7. **Cells:** every ordered pair per arm and K: play (C / D / ⊥), every top-level check (outcome T / F / TO, steps,
   nesting depth, regress events), every top-level search; held-out coverage; fuel-boundary cells (V around the
   measured check cost; K around the static fit boundary); the soundness audit (every check that returned T: the
   certified atom against the actual play); a fuzz battery of small carrier-like codes with random scripts.
8. **Scale guard:** the CB–CB check cost and the smallest K at which it finishes are reported first; if a carrier's
   check exceeds 10⁵ steps the catalogue is reduced to C, D, CB, CBP, FB_code, SF, SFc and the fakers.
9. Workers ≤ 2 (two foreign chains alive at commit time).

## RE predictions (verbatim from the spec, with falsifiers)

1. **JLöb^pair is sound, unconditionally, with one guard** [revised after review]: the unrestricted pair rule
   admits a cyclic certificate for a false atom (Dcert's), and the guard that excludes it is that the hypothesis
   must name *the checking program's own* check call on the certificate being checked (the milestone-3 "root
   call" condition transposed), after which Theorem S^cert goes through by size induction; every corrupted instance
   and Dcert are rejected; 0 violations on every accepted certificate. *Falsifier:* no guard under which the
   theorem holds (stop before the catalogue), or an accepted certificate whose atom is false in any cell.
2. **Distinct-source carriers cooperate, cheaply:** CB(FB-shaped) and CB(FB1-shaped) cooperate at K = 10⁶ with each
   check's actual run ≤ 10⁵ steps, and no check re-enters its own call (regress depth 1). *Falsifier:* a
   distinct-source carrier pair that defects with both checks finished, or an actual check run above 10⁵ steps.
3. **Carriers and searchers both defect** [revised after review]: CB defects on FB_code (no certificate to check),
   and FB_code's search, where it finishes, refutes or fails to find CB's cooperation; (D, D). *Falsifier:* (C, C) in
   any carrier–searcher cell with both computations finished.
4. **Fakers are rejected by soundness, not by luck:** CBfake's certificate is about another object, so the reader's
   root atom (about CBfake's actual object) does not match and the check returns F; CBdef's certificate fails the
   checker; CBmut is a different object and is cooperated with iff its remaining certificates cover the reader;
   CBsloppy cooperates with Dcert and with every carrier (exploited by Dcert; D alone, carrying nothing, is
   refused), and sound carriers cooperate with CBsloppy iff CBsloppy's own certificate about its object checks.
   *Falsifier:* a sound carrier cooperating with CBfake, CBdef or Dcert.
5. **Literal certificates do not transfer; quantified templates do, at a cost** [revised after review]: a literal
   certificate fails against a same-shape carrier with a different spelling (the quoted source differs); a
   quantified template with a checked membership obligation covers every held-out same-shape carrier, with the
   instantiation adding ≤ 2× to the check's run. *Falsifier:* a held-out same-shape carrier that no template
   covers, or instantiation above 5× the literal check.
6. **The disabled control is not twins-only** [added after review]: acyclic carried proofs certify carrier–C and
   carrier–SF_k cells at the same costs, and the pair rule adds exactly the carrier–carrier cells. *Falsifier:* a
   carrier–carrier cell certified without the pair rule, or a carrier–C cell lost with it.

**How they will be scored** (fixed now, from §1): RE 1's falsifier is about the existence of a sound guard and about
violations; its stated guard (the checker's own call) is scored separately: notes §1.6–1.7 derive that the own-call
guard is sound but certifies twins only (mode 2), that Dcert is not certifiable under any hypothesis rule (its run has
no call), and that the guard that admits distinct sources is partner validation of the swap. RE 4 and RE 6 read "C"
and "SF_k" as the certificate-carrying Ccert and SFc (plain C and SF carry nothing, so no reader can certify them);
"without the pair rule" means arm X (no hypothesis rule), with arm O reported beside it. RE 5's first clause has no
object (Lemma F: there are no literal self-certificates); its second clause is scored on the held-out set, reading
"template" as a production-set script carried by a held-out source, with "same-shape" meaning the same target set
(FB-, FB1- or PB-shaped).

## Static numbers (hand, from notes §1.8)

| script | nodes | expanded size |
|---|---|---|
| CB, CBlet, CBwrap, SFc C script: EvR*; ChkR[EvR*; Ax · Hyp] | 5 | 7 (CB), more for wrappers and SFc |
| CB1 C script: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Hyp] | 8 | 10 |
| CBP C script: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Run] · Hyp] | 8 | 10 |
| D script (all carriers): EvR*; ChkR[RunNeg · EvR*; Ax] | 5 | 7 |
| Ccert: EvR*; Ax | 2 | 4 |

- Check-call cost bound u(V) = V + 6 (to be confirmed exactly by code). CB's static fit boundary: K ≥ V + 10.
- Nesting depth of check frames: 1 for FB-shaped pairs, 3 for pairs involving CBP (check → Run of the partner's D
  script → RunNeg of D's empty check).
- Certificate count: 2 scripts per carrier (C and D), independent of the number of sources; storage per carrier
  ≈ 13–16 script nodes; a new source adds its own 2 scripts and nothing elsewhere.
- Check cost per FB-shaped pair: **guess** 5·10³–3·10⁴ steps; PB-involving ≤ 6·10⁴; all < 10⁵.

## Subagent predictions (with falsifiers)

- **S1 (soundness, measured).** 0 violations: every top-level check by CC_0, CC_2, CC_3, CC_5 that returns T in any
  cell certifies an atom that the actual play confirms; the fuzz battery finds no accepted false atom for these
  modes. *Falsifier:* one accepted false atom.
- **S2 (the guard is load-bearing).** CC_1 (naive) accepts at least one false atom: CBN0 cooperates with CBN while CBN
  defects, at every K where the checks fit; CB0 against CB is (D, D). *Falsifier:* CC_1 accepts no false atom
  anywhere, or CB0 cooperates with CB.
- **S3 (decomposition).** Arm X: carriers cooperate with Ccert and with nobody else (no twin, no SFc, no distinct
  carrier). Arm O: adds twins and SFc against FB-shaped carriers, no distinct carrier pair. Arm S: adds every pair
  among CB, CB1, CBP, CBlet, CBwrap at K ∈ {10⁶, 10⁷}. *Falsifier:* any carrier–carrier cooperation in arm X, a
  distinct pair in arm O, or a distinct sound pair that defects in arm S at K = 10⁷ with both checks finished.
- **S4 (Lemma Sym, measured).** In every cell where a check closed S, the swap check returns T, with an equal step
  count when both scripts close the other's box and a smaller one otherwise. *Falsifier:* a swap check returning F or
  TO, or costing more.
- **S5 (costs).** Every top-level check in arm S costs ≤ 10⁵ steps; CB–CB checks finish at K = 10⁵ (V = 25,000)
  (a guess from the cost estimate). *Falsifier:* a check above 10⁵; CB–CB not finishing at 10⁵.
- **S6 (simulators).** SFc–CB, SFc–CBlet, SFc–CBwrap are (C, C) at K ∈ {10⁶, 10⁷} in arms S and O, and (D, D) in
  arm X; SFc against CB1 and CBP is (D, D) in every arm (two calls do not fit in a K/2 simulation). Plain SF is (D, D)
  with every carrier. *Falsifier:* any of these cells different.
- **S7 (fakers).** CBdef is suckered by every sound carrier (reader D, CBdef C); LöbC cooperates with every program
  including D; CBsloppy is exploited by Dcert and CBfake, cooperates with every carrier, refuses plain D, and every
  sound carrier including CBP cooperates with it (unlike milestone 3, where PB refused SC: here CBsloppy defects on D,
  which carries nothing). CBmut: (C, C) with CB, CB1, CBlet, CBwrap; (D, D) with CBP. *Falsifier:* any of these
  differs.
- **S8 (checkers are conventions).** CB–CBS2 and CB–CBN are (D, D) with a regress event in each check; CBS2 against
  its own twin is (C, C). *Falsifier:* cooperation across different sound checkers, or no regress.
- **S9 (searchers).** Every carrier–searcher cell is (D, D); no searcher query about a carrier is found at any K.
  *Falsifier:* a found query or a (C, C) cell.
- **S10 (held-out).** CBlet2, CBw2, CB1h, CB1r and CBPh validate the production-set script of their shape class;
  CBPr does not and needs a fresh production of the same size (8 nodes); every held-out carrier cooperates with every
  production-set carrier of arm S with no new certificate on the production-set side. *Falsifier:* any held-out
  source covered or not covered otherwise; any production-set carrier needing a new certificate.
- **S11 (static boundaries).** The check-call cost is exactly W + 6 and never exceeds V + 6; the CB–CB fit boundary
  is K = V + 10 statically, and the actual run would succeed at a smaller K: the flip in a K-scan with V fixed is at
  the static boundary. With K fixed and V scanned, a check flips from F to T at V = W (the inner step count).
  *Falsifier:* a check costing more than V + 6, or a flip elsewhere.
- **S12 (plateau).** Every cell of arm S is the same at K = 10⁶ and 10⁷ (nothing depends on K once V ≥ the check
  cost); cells at 10⁵ differ only where a check exceeds 25,000 steps. *Falsifier:* a cell that differs between 10⁶
  and 10⁷.
