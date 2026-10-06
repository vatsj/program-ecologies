# Spec: the realizable language, milestone 4: certificates as code: does checking instead of searching restore distinct-source cooperation?, 2026-10-06

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol; to be run by an Opus subagent. Follow-up to
RESULTS "The realizable language, milestone 3" (DEFERRED 2 and 11). This is the RS's proof-carrying-contracts
pitch (2026-10-04) with a realizable rationale.

## Why

With the prover as code, a sound reader cooperates only with exact twins: to certify a distinct source it must run
that source's search, which re-enters the reader's own query, and the regress spends the whole cap. Checking a
derivation costs 1.2·10⁴ steps where searching for it costs 1.1·10⁵ (FairBot) to 9·10⁵ (PrudentBot). So the lever
is a **carried derivation**: a program publishes, beside its code, a derivation of its own cooperation, and readers
*check* it rather than search for it. The milestone-3 obstruction was that a box meant "the opponent's search
finds a proof", a fact about an expensive run; if the opponent's code does not search at all but *checks a carried
certificate*, the fact a reader needs is "the opponent's check returns T", a 10⁴-step deterministic run the reader
can afford to unfold or verify. The questions: (i) is there a sound ex-post rule for *mutual* checks, the
certificate-level FairBot handshake, where each certificate's derivation assumes the other's check succeeds; (ii)
do two distinct sources then cooperate, at what cost, and from what K; (iii) what the fakers are (a certificate
about code that does not use it; a certificate whose check succeeds but whose code defects anyway; a sloppy
checker), and whether soundness ex post rules them out as it ruled out the simulator.

## Design

**Programs with certificates.** A program is a pair (code, cert). The code of a **carrier** reads the opponent's
pair and checks: CB = `λ me them. if CHECK(cert(them), plays(⌜them⌝, ⌜me⌝, C)) then C else D`, where CHECK is the
library checker term of milestone 3 (cost ≈ 10⁴ steps per derivation node count), `cert(them)` is the opponent's
published certificate, and the formula is the fuel-indexed atom of the opponent's actual run against me. A
certificate is a derivation in **K_T^cert** = K_T^code with the search-call rule replaced by a **check-call rule**
ChkR (a CHECK call on a quoted certificate is one evaluation step whose outcome is a fact about a deterministic
10⁴-step run; it carries the static cost of CHECK as its fit condition) and with **JLöb^pair**: a derivation of
"them's code cooperates with me" may take as hypothesis "my own check of them's certificate returns T", since my
check returns T only once that derivation has been checked; the certificate-level handshake is two certificates
each hypothesizing the other's check. The notes (§1) must state every rule of K_T^cert with its semantic obligation
and prove soundness ex post for valid derivations (Theorem S^cert: if both checks return T then both hypotheses
are true), or exhibit where it fails; corrupted instances (a certificate about the wrong code, a certificate whose
root atom names a different fuel, a check call with the fit condition violated, a JLöb^pair hypothesis that is not
the checker's own call) must be rejected by the checker term and the replay checker.

[after review] **Soundness must be unconditional and semantic, and it gates the run.** "If both checks return T then
both hypotheses are true" is a naming fact and proves nothing about the certified atoms. The theorem required
(Theorem S^cert) is: *every certificate accepted by CHECK implies the truth of its exact fuel-indexed execution
atom*, against arbitrary opponents including non-carriers, proved without assuming the checker's soundness inside
the proof (the milestone-3 pattern: size induction on valid derivations, with the ex-post discharge of the pair
hypothesis argued from the order of events in the actual run of both programs, since each code's check finishes
before its branch is taken). If the unrestricted pair rule admits a false certificate, the notes must exhibit it
(a cyclic certificate for a false atom, in particular for `plays(D-code, opp, C)`), state the guard or discharge
condition that excludes it, and re-prove; if no sound rule exists, **stop before the catalogue** and report that as
the result. A certificate's acceptance is syntactic; the theorem is what connects it to behaviour.

[after review] **Identity is the whole behavioural object.** Play depends on (code, certificate list, checker
version, fuel convention), so certificates, lookup keys and the atoms they certify name the complete object, not the
code alone; a program with the same code and a different certificate list is a different program. Self-reference
(a certificate about the pair that contains it) must be represented finitely in the language (the quine/fixed-point
construction of milestone 3, or a hash the library can recompute), never by a host-generated pointer.

[after review] **ChkR charges actual runtime.** A check is not one step: its fit condition must bound the evaluator's
actual run of CHECK on the quoted certificate (quotation, substitution, lookup, nested checks), reported separately
from derivation-node counts, and every summarized check carries a replayable witness (the actual run, re-executed by
the harness) as the milestone-3 Run rule did. If the static bound and the actual run disagree in any cell, that is a
soundness failure to report.

**Certificate production.** Certificates are produced offline by the milestone-3 search (the host oracle or the
library search run once at production, outside any match) for each named program against each named opponent's
*code* (a certificate is specific to the pair of codes, as contracts were specific to sources in RESULTS
"Proof-carrying contracts v1"); the production cost is reported but not charged to the match. A carrier publishes a
list of certificates keyed by opponent code; readers look up their own code (structural `eq`, one step). *Templates:*
whether one certificate can cover a class of opponent codes (all carriers with the same checker and the same
root formula shape) is a static question to answer first; if yes, the catalogue uses template certificates and
the lookup is by template.

[after review] **Production is a frozen procedure, tested on held-out sources.** A pairwise table built with
knowledge of the catalogue demonstrates a curated club, not an extensible class. The production procedure (the
milestone-3 search, its budget, cap and formula shape) is frozen in §1 before the catalogue is fixed; the catalogue
is split into a production set and a **held-out set** of carriers (different spellings, one different checker
wrapping, one FB1-shaped and one PB-shaped source not seen at production), and the report states for each held-out
source whether a certificate produced for the production set covers it, or a fresh production is needed, with
the production cost and the certificate size and count. Report the growth of certificate count, storage and
production cost in the number of sources beside match costs. Literal certificates are source-specific (quoted
sources and fuel-indexed atoms); if templates are to cover a class they are *quantified* templates whose
instantiation is checked (an explicit membership obligation discharged by the checker at match time), and that
instantiation cost is charged.

**Catalogue.** C, D; carriers CB with the sound checker at three code variants (FB-shaped, FB1-shaped, PB-shaped: the
check targets differ as the modal programs' atoms did); the milestone-3 searchers FB_code, FB1_code, PB_code (no
certificate; they search); SF_k; G_code; **fakers:** CBfake (publishes a valid certificate about a *different* code
and its own code defects), CBdef (certificate about its own code, but the code's branch is swapped: the certificate
is then invalid and the checker must reject it, a consistency test), CBsloppy (a sloppy checker that accepts any
derivation whose end sequent matches); and two harmless variants of CB. Fuel K ∈ {10⁵, 10⁶, 10⁷}; certificate
sizes as produced. [after review] Add **Dcert** (code D, carrying a bogus certificate rooted at the atom "D-code
cooperates", with a cyclic pair-rule derivation): the faker that targets CBsloppy and the test of whether the
sound checker rejects cyclic certificates for false atoms; D alone carries nothing and need not trigger CBsloppy.
Add **CBmut**: CB's code with its certificate list mutated (one certificate dropped, one replaced by a certificate
about a different code), the identity control.

**Cells.** Every ordered pair: play (C / D / ⊥), the check's outcome (T / F / interrupted) and its step cost;
distinct-source carrier pairs (FB-shaped vs FB1-shaped vs PB-shaped) at each K; carrier vs searcher (does a
carrier cooperate with a milestone-3 searcher, which has no certificate, and does the searcher certify a
carrier, whose code is a cheap check it can unfold?); carrier vs SF_k; carriers vs fakers; the harmless
variants; the JLöb^pair-disabled control (certificates may not hypothesize the other's check), **measured, not
assumed**: an acyclic carried proof can certify a distinct source whose own code does not read certificates (a
carrier against C, against SF_k, against a searcher's actual run if it fits), so the control's result is the set of
pairs that direct proofs certify under identical accounting, against the set the pair rule adds; **the regress
check**: the deepest nesting of checks in any run and whether any check re-enters its own call; **fuel boundary
cells** at K just above and below each claimed check bound; coverage (finished / interrupted) per cell; the
finite-K plateau.

**Scale guard.** Report the CB–CB check cost and K at which it finishes first; if a carrier's check exceeds 10⁵
steps, reduce the catalogue to C, D, two carriers, one searcher, SF and the fakers. ≤ 3 workers.

## Required outputs

`src/lt_cert.py` (K_T^cert rules in the checker term, certificate production, the carrier programs, the harness),
`tests/test_lt_cert.py`, `notes/certificates-as-code.md` (§1 rules and obligations, Theorem S^cert or its failure,
corrupted instances; §2 costs), `runs/certificates-as-code.md` and `.json`, a predictions file from the spec
committed after §1 and before any counted cell, the usual hand-back (draft RESULTS, REJECTED, THEORY §9.2 and
DEFERRED 2 and 11 edits, NOTATION, ≤ 5 lines, branch from `git branch --show-current`, commits).

## RE predictions (with falsifiers)

1. **JLöb^pair is sound, unconditionally, with one guard** [revised after review]: the unrestricted pair rule
   admits a cyclic certificate for a false atom (Dcert's), and the guard that excludes it is that the hypothesis
   must name *the checking program's own* check call on the certificate being checked (the milestone-3 "root
   call" condition transposed), after which Theorem S^cert goes through by size induction; every corrupted instance
   and Dcert are rejected; 0 violations on every accepted certificate. *Falsifier:* no guard under which the
   theorem holds (stop before the catalogue), or an accepted certificate whose atom is false in any cell.
2. **Distinct-source carriers cooperate, cheaply:** CB(FB-shaped) and CB(FB1-shaped) cooperate at K = 10⁶ with each
   check's actual run ≤ 10⁵ steps, and no check re-enters its own call (regress depth 1). *Falsifier:* a
   distinct-source carrier pair that defects with both checks finished, or an actual check run above 10⁵ steps.
3. **Carriers and searchers both defect** [revised after review: my first version, "the searcher certifies the
   carrier", contradicted soundness, since the carrier defects on a certificate-less searcher and a sound search
   cannot certify a cooperation that does not happen]: CB defects on FB_code (no certificate to check), and FB_code's
   search, where it finishes, refutes or fails to find CB's cooperation; (D, D). *Falsifier:* (C, C) in any
   carrier–searcher cell with both computations finished.
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

The RS is invited to add predictions; the uncertain ones are 1 (whether a guarded pair rule is sound) and 5.
