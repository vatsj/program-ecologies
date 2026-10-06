# Run: the realizable language, milestone 4: certificates as code (2026-10-06)

Spec `specs/2026-10-06-certificates-as-code.md`; notes `notes/certificates-as-code.md`; predictions `predictions/2026-10-06-certificates-as-code.md`; code `src/lt_cert.py`, `src/lt_cert_run.py`, `src/lt_cert_report.py`, `tests/test_lt_cert.py`; raw tables `runs/certificates_as_code/`. Plays are the actual runs of `p ⌜p⌝ ⌜q⌝` with global fuel K; V = ⌊K/4⌋, k = ⌊K/2⌋. A pair entry "CD" means the row program plays C against the column program and the column program plays D against it.

## 1. Scale guard and costs (K = 10⁷, V = 2.5·10⁶)

| check (reader checks target's script) | result | inner steps W | call cost W + 6 |
|---|---|---|---|
| CB checks CB | T | 8782 | 8788 |
| CB1 checks CB | T | 21541 | 21547 |
| CB checks CB1 | T | 21541 | 21547 |
| CBP checks CB | T | 30491 | 30497 |
| CB checks CBP | T | 30491 | 30497 |
| CBP checks CB1 | T | 37140 | 37146 |
| CB1 checks CBP | T | 37140 | 37146 |
| CBP checks CBP | T | 24388 | 24394 |
| CB1 checks CB1 | T | 12757 | 12763 |
| CBlet checks CB | T | 18166 | 18172 |
| CBwrap checks CB | T | 18526 | 18532 |
| SFc checks CB | T | 25078 | 25084 |
| Ccert checks CB | T | 10827 | 10833 |
| LobC checks CB | T | 17545 | 17551 |
| CBsloppy checks CB | T | 18298 | 18304 |
| CBsloppy checks CBP | T | 31442 | 31448 |
| CBmut checks CB | T | 28507 | 28513 |
| Dcert checks CB | F | 19599 | 19605 |
| CB0 checks CB | F | 8857 | 8863 |

Smallest K (V = K/4, sources rebuilt at each K, bisection to ±4) at which the row pair's check returns T:

| pair (target|reader) | first K |
|---|---|
| CB|CB | 35128 |
| CB|CB1 | 86164 |
| CB|CBP | 121964 |
| CB1|CBP | 148563 |
| CBP|CBP | 97554 |

Certificate lists (production as frozen; expanded size on the root against CB for C scripts and against D for D scripts; storage = term nodes of the whole list; source = term nodes of the program):

| program | a | script | nodes | expanded | list storage | source nodes |
|---|---|---|---|---|---|---|
| CB | C | EvR*; ChkR[EvR*; Ax · Hyp] | 5 | 7 | 65 | 83 |
| CB | D | EvR*; ChkR[RunNeg · EvR*@1; Ax] | 5 | 7 | 65 | 83 |
| CB1 | C | EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Hyp] | 8 | 10 | 83 | 114 |
| CB1 | D | EvR*; ChkR[RunNeg · EvR*@1; Ax] | 5 | 7 | 83 | 114 |
| CBP | C | EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Run] · Hyp] | 8 | 10 | 83 | 117 |
| CBP | D | EvR*; ChkR[RunNeg · EvR*@1; Ax] | 5 | 7 | 83 | 117 |
| CBlet | C | EvR*; ChkR[EvR*; Ax · Hyp] | 5 | 8 | 65 | 86 |
| CBlet | D | EvR*; ChkR[RunNeg · EvR*@1; Ax] | 5 | 8 | 65 | 86 |
| CBwrap | C | EvR*; ChkR[EvR*; Ax · Hyp] | 5 | 8 | 65 | 86 |
| CBwrap | D | EvR*; ChkR[RunNeg · EvR*@1; Ax] | 5 | 8 | 65 | 86 |
| Ccert | C | EvR*; Ax | 2 | 4 | 15 | 20 |
| SFc | C | EvR*; ChkR[EvR*; Ax · Hyp] | 5 | 14 | 47 | 60 |
| SFc | D | EvR*; Ax | 2 | 10 | 47 | 60 |
| LobC | C | EvR*; ChkR[EvR*; Ax · Hyp] | 5 | 7 | 65 | 83 |
| LobC | D | EvR*; ChkR[RunNeg · EvR*@1; Ax] | 5 | 7 | 65 | 83 |
| CBsloppy | C | EvR*; ChkR[EvR*; Ax · Run] | 5 | 7 | 65 | 83 |
| CBsloppy | D | EvR*; ChkR[RunNeg · EvR*@1; Ax] | 5 | 7 | 65 | 83 |
| CBN | C | EvR*; ChkR[EvR*; Ax · Hyp] | 5 | 7 | 65 | 83 |
| CBN | D | EvR*; ChkR[RunNeg · EvR*@1; Ax] | 5 | 7 | 65 | 83 |
| CBS2 | C | EvR*; ChkR[EvR*; Ax · Hyp] | 5 | 7 | 65 | 83 |
| CBS2 | D | EvR*; ChkR[RunNeg · EvR*@1; Ax] | 5 | 7 | 65 | 83 |

Production cost per source (fresh producer; host, not charged to matches):

| source | scripts | tactic nodes | host check emulations | host secs |
|---|---|---|---|---|
| CB | 2 | 20 | 1 | 0.0 |
| CB1 | 2 | 29 | 1 | 0.0 |
| CBP | 2 | 29 | 7 | 0.0 |
| CBlet | 2 | 20 | 1 | 0.0 |
| CBwrap | 2 | 20 | 1 | 0.0 |
| CBlet2 | 2 | 20 | 1 | 0.0 |
| CBw2 | 2 | 20 | 1 | 0.0 |
| CB1h | 2 | 29 | 1 | 0.0 |
| CB1r | 2 | 29 | 1 | 0.0 |
| CBPh | 2 | 29 | 7 | 0.0 |
| CBPr | 2 | 29 | 7 | 0.0 |

## 2.1 Arm S (sound checker) at K = 1e5

| row \ col | CB | CB1 | CBP | CBlet | CBwrap | LobC | CBmut | CBsloppy | CBS2 | CBN | CB0 | CBN0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CB | CC | CC | DD | CC | CC | CC | DD | CC | DD | DD | DD | DD |
| CB1 | CC | CC | DD | CC | CC | CC | DD | CC | DD | DD | DD | DD |
| CBP | DD | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DD |
| CBlet | CC | CC | DD | CC | CC | CC | DD | CC | DD | DD | DD | DD |
| CBwrap | CC | CC | DD | CC | CC | CC | DD | CC | DD | DD | DD | DD |
| LobC | CC | CC | CD | CC | CC | CC | CC | CC | CD | CD | CC | CD |
| CBmut | DD | DD | DD | DD | DD | CC | CC | CC | DD | DD | DD | DD |
| CBsloppy | CC | CC | CC | CC | CC | CC | CC | CC | CC | CC | DD | DD |
| CBS2 | DD | DD | DD | DD | DD | DC | DD | CC | CC | DD | DD | DD |
| CBN | DD | DD | DD | DD | DD | DC | DD | CC | DD | CC | DD | DC |
| CB0 | DD | DD | DD | DD | DD | CC | DD | DD | DD | DD | DD | DD |
| CBN0 | DD | DD | DD | DD | DD | DC | DD | DD | DD | CD | DD | DD |
| C | CD | CD | CD | CD | CD | CC | CD | CD | CD | CD | CD | CD |
| D | DD | DD | DD | DD | DD | DC | DD | DD | DD | DD | DD | DD |
| Ccert | CC | CC | CD | CC | CC | CC | CC | CC | CC | CC | CC | CC |
| Dcert | DD | DD | DD | DD | DD | DC | DD | DC | DD | DD | DD | DD |
| CBfake | DD | DD | DD | DD | DD | DC | DD | DC | DD | DD | DD | DD |
| CBdef | CD | CD | CD | CD | CD | DC | CD | DC | CD | CD | CD | CD |
| SF | DD | DD | DD | DD | DD | CC | DD | DD | DD | DD | DD | DD |
| SFc | CC | DD | DD | CC | CC | CC | CC | CC | CC | CC | CC | CC |
| FB_code | DD | DD | DD | DD | DD | DC | DD | DD | DD | DD | DD | DD |
| FB1_code | DD | DD | DD | DD | DD | DC | DD | DD | DD | DD | DD | DD |
| PB_code | DD | DD | DD | DD | DD | DC | DD | DD | DD | DD | DD | DD |
| G_code | CD | CD | CD | CD | CD | CC | CD | CD | CD | CD | CD | CD |

| row \ col | C | D | Ccert | Dcert | CBfake | CBdef | SF | SFc | FB_code | FB1_code | PB_code | G_code |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CB | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| CB1 | DC | DD | CC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| CBP | DC | DD | DC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| CBlet | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| CBwrap | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| LobC | CC | CD | CC | CD | CD | CD | CC | CC | CD | CD | CD | CC |
| CBmut | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| CBsloppy | DC | DD | CC | CD | CD | CD | DD | CC | DD | DD | DD | DC |
| CBS2 | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| CBN | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| CB0 | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| CBN0 | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| C | CC | CD | CC | CD | CD | CC | CC | CC | CC | CD | CD | CD |
| D | DC | DD | DC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| Ccert | CC | CD | CC | CD | CD | CD | CC | CC | CD | CD | CD | CC |
| Dcert | DC | DD | DC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| CBfake | DC | DD | DC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| CBdef | CC | CD | DC | CD | CD | CC | CC | CC | CD | CD | CD | CC |
| SF | CC | DD | CC | DD | DD | CC | DD | DD | DD | DD | DD | CC |
| SFc | CC | DD | CC | DD | DD | CC | DD | DD | DD | DD | DD | CC |
| FB_code | CC | DD | DC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| FB1_code | DC | DD | DC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| PB_code | DC | DD | DC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| G_code | DC | CD | CC | CD | CD | CC | CC | CC | CD | CD | CD | CC |

Held-out sources (carrying the production-set script of their class):

| held-out | CB | CB1 | CBP | CBlet | CBwrap | SFc | CBsloppy | CBlet2 | CBw2 | CB1h | CB1r | CBPh | CBPr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CBlet2 | CC | CC | DD | CC | CC | CC | CC | CC | CC | CC | CC | DD | DD |
| CBw2 | CC | CC | DD | CC | CC | CC | CC | CC | CC | CC | CC | DD | DD |
| CB1h | CC | DD | DD | CC | CC | DD | CC | CC | CC | CC | DD | DD | DD |
| CB1r | CC | DD | DD | CC | CC | DD | CC | CC | CC | DD | CC | DD | DD |
| CBPh | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD | DD | DD | DD |
| CBPr | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD | DD | DD | DD |

## 2.2 Arm S (sound checker) at K = 1e6

| row \ col | CB | CB1 | CBP | CBlet | CBwrap | LobC | CBmut | CBsloppy | CBS2 | CBN | CB0 | CBN0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CB | CC | CC | CC | CC | CC | CC | CC | CC | DD | DD | DD | DD |
| CB1 | CC | CC | CC | CC | CC | CC | CC | CC | DD | DD | DD | DD |
| CBP | CC | CC | CC | CC | CC | DC | DD | CC | DD | DD | DD | DD |
| CBlet | CC | CC | CC | CC | CC | CC | CC | CC | DD | DD | DD | DD |
| CBwrap | CC | CC | CC | CC | CC | CC | CC | CC | DD | DD | DD | DD |
| LobC | CC | CC | CD | CC | CC | CC | CC | CC | CD | CD | CC | CD |
| CBmut | CC | CC | DD | CC | CC | CC | CC | CC | DD | DD | DD | DD |
| CBsloppy | CC | CC | CC | CC | CC | CC | CC | CC | CC | CC | DD | DD |
| CBS2 | DD | DD | DD | DD | DD | DC | DD | CC | CC | DD | DD | DD |
| CBN | DD | DD | DD | DD | DD | DC | DD | CC | DD | CC | DD | DC |
| CB0 | DD | DD | DD | DD | DD | CC | DD | DD | DD | DD | DD | DD |
| CBN0 | DD | DD | DD | DD | DD | DC | DD | DD | DD | CD | DD | DD |
| C | CD | CD | CD | CD | CD | CC | CD | CD | CD | CD | CD | CD |
| D | DD | DD | DD | DD | DD | DC | DD | DD | DD | DD | DD | DD |
| Ccert | CC | CC | CD | CC | CC | CC | CC | CC | CC | CC | CC | CC |
| Dcert | DD | DD | DD | DD | DD | DC | DD | DC | DD | DD | DD | DD |
| CBfake | DD | DD | DD | DD | DD | DC | DD | DC | DD | DD | DD | DD |
| CBdef | CD | CD | CD | CD | CD | DC | CD | DC | CD | CD | CD | CD |
| SF | DD | DD | DD | DD | DD | CC | DD | DD | DD | DD | DD | DD |
| SFc | CC | DD | DD | CC | CC | CC | CC | CC | CC | CC | CC | CC |
| FB_code | DD | DD | DD | DD | DD | DC | DD | DD | DD | DD | DD | DD |
| FB1_code | DD | DD | DD | DD | DD | DC | DD | DD | DD | DD | DD | DD |
| PB_code | DD | DD | DD | DD | DD | DC | DD | DD | DD | DD | DD | DD |
| G_code | CD | CD | CD | CD | CD | CC | CD | CD | CD | CD | CD | CD |

| row \ col | C | D | Ccert | Dcert | CBfake | CBdef | SF | SFc | FB_code | FB1_code | PB_code | G_code |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CB | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| CB1 | DC | DD | CC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| CBP | DC | DD | DC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| CBlet | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| CBwrap | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| LobC | CC | CD | CC | CD | CD | CD | CC | CC | CD | CD | CD | CC |
| CBmut | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| CBsloppy | DC | DD | CC | CD | CD | CD | DD | CC | DD | DD | DD | DC |
| CBS2 | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| CBN | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| CB0 | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| CBN0 | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| C | CC | CD | CC | CD | CD | CC | CC | CC | CC | CC | CD | CD |
| D | DC | DD | DC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| Ccert | CC | CD | CC | CD | CD | CD | CC | CC | CC | CC | CD | CD |
| Dcert | DC | DD | DC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| CBfake | DC | DD | DC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| CBdef | CC | CD | DC | CD | CD | CC | CC | CC | CD | CD | CD | CC |
| SF | CC | DD | CC | DD | DD | CC | DD | DD | DD | DD | DD | CC |
| SFc | CC | DD | CC | DD | DD | CC | DD | DD | DD | DD | DD | CC |
| FB_code | CC | DD | CC | DD | DD | DC | DD | DD | CC | DD | DD | DC |
| FB1_code | CC | DD | CC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| PB_code | DC | DD | DC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| G_code | DC | CD | DC | CD | CD | CC | CC | CC | CD | CD | CD | CC |

Held-out sources (carrying the production-set script of their class):

| held-out | CB | CB1 | CBP | CBlet | CBwrap | SFc | CBsloppy | CBlet2 | CBw2 | CB1h | CB1r | CBPh | CBPr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CBlet2 | CC | CC | CC | CC | CC | CC | CC | CC | CC | CC | CC | CC | DD |
| CBw2 | CC | CC | CC | CC | CC | CC | CC | CC | CC | CC | CC | CC | DD |
| CB1h | CC | CC | CC | CC | CC | DD | CC | CC | CC | CC | CC | CC | DD |
| CB1r | CC | CC | CC | CC | CC | DD | CC | CC | CC | CC | CC | CC | DD |
| CBPh | CC | CC | CC | CC | CC | DD | CC | CC | CC | CC | CC | CC | DD |
| CBPr | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD | DD | DD | DD |

## 2.3 Arm S (sound checker) at K = 1e7

| row \ col | CB | CB1 | CBP | CBlet | CBwrap | LobC | CBmut | CBsloppy | CBS2 | CBN | CB0 | CBN0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CB | CC | CC | CC | CC | CC | CC | CC | CC | DD | DD | DD | DD |
| CB1 | CC | CC | CC | CC | CC | CC | CC | CC | DD | DD | DD | DD |
| CBP | CC | CC | CC | CC | CC | DC | DD | CC | DD | DD | DD | DD |
| CBlet | CC | CC | CC | CC | CC | CC | CC | CC | DD | DD | DD | DD |
| CBwrap | CC | CC | CC | CC | CC | CC | CC | CC | DD | DD | DD | DD |
| LobC | CC | CC | CD | CC | CC | CC | CC | CC | CD | CD | CC | CD |
| CBmut | CC | CC | DD | CC | CC | CC | CC | CC | DD | DD | DD | DD |
| CBsloppy | CC | CC | CC | CC | CC | CC | CC | CC | CC | CC | DD | DD |
| CBS2 | DD | DD | DD | DD | DD | DC | DD | CC | CC | DD | DD | DD |
| CBN | DD | DD | DD | DD | DD | DC | DD | CC | DD | CC | DD | DC |
| CB0 | DD | DD | DD | DD | DD | CC | DD | DD | DD | DD | DD | DD |
| CBN0 | DD | DD | DD | DD | DD | DC | DD | DD | DD | CD | DD | DD |
| C | CD | CD | CD | CD | CD | CC | CD | CD | CD | CD | CD | CD |
| D | DD | DD | DD | DD | DD | DC | DD | DD | DD | DD | DD | DD |
| Ccert | CC | CC | CD | CC | CC | CC | CC | CC | CC | CC | CC | CC |
| Dcert | DD | DD | DD | DD | DD | DC | DD | DC | DD | DD | DD | DD |
| CBfake | DD | DD | DD | DD | DD | DC | DD | DC | DD | DD | DD | DD |
| CBdef | CD | CD | CD | CD | CD | DC | CD | DC | CD | CD | CD | CD |
| SF | DD | DD | DD | DD | DD | CC | DD | DD | DD | DD | DD | DD |
| SFc | CC | DD | DD | CC | CC | CC | CC | CC | CC | CC | CC | CC |
| FB_code | DD | DD | DD | DD | DD | DC | DD | DD | DD | DD | DD | DD |
| FB1_code | DD | DD | DD | DD | DD | DC | DD | DD | DD | DD | DD | DD |
| PB_code | DD | DD | DD | DD | DD | DC | DD | DD | DD | DD | DD | DD |
| G_code | CD | CD | CD | CD | CD | CC | CD | CD | CD | CD | CD | CD |

| row \ col | C | D | Ccert | Dcert | CBfake | CBdef | SF | SFc | FB_code | FB1_code | PB_code | G_code |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CB | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| CB1 | DC | DD | CC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| CBP | DC | DD | DC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| CBlet | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| CBwrap | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| LobC | CC | CD | CC | CD | CD | CD | CC | CC | CD | CD | CD | CC |
| CBmut | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| CBsloppy | DC | DD | CC | CD | CD | CD | DD | CC | DD | DD | DD | DC |
| CBS2 | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| CBN | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| CB0 | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| CBN0 | DC | DD | CC | DD | DD | DC | DD | CC | DD | DD | DD | DC |
| C | CC | CD | CC | CD | CD | CC | CC | CC | CC | CC | CD | CD |
| D | DC | DD | DC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| Ccert | CC | CD | CC | CD | CD | CD | CC | CC | CC | CC | CD | CD |
| Dcert | DC | DD | DC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| CBfake | DC | DD | DC | DD | DD | DC | DD | DD | DD | DD | DD | DC |
| CBdef | CC | CD | DC | CD | CD | CC | CC | CC | CD | CD | CD | CC |
| SF | CC | DD | CC | DD | DD | CC | DD | DD | CC | CC | DD | CC |
| SFc | CC | DD | CC | DD | DD | CC | DD | DD | CC | CC | DD | CC |
| FB_code | CC | DD | CC | DD | DD | DC | CC | CC | CC | DD | DD | DC |
| FB1_code | CC | DD | CC | DD | DD | DC | CC | CC | DD | CC | DD | DC |
| PB_code | DC | DD | DC | DD | DD | DC | DD | DD | DD | DD | CC | DC |
| G_code | DC | CD | DC | CD | CD | CC | CC | CC | CD | CD | CD | CC |

Held-out sources (carrying the production-set script of their class):

| held-out | CB | CB1 | CBP | CBlet | CBwrap | SFc | CBsloppy | CBlet2 | CBw2 | CB1h | CB1r | CBPh | CBPr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CBlet2 | CC | CC | CC | CC | CC | CC | CC | CC | CC | CC | CC | CC | DD |
| CBw2 | CC | CC | CC | CC | CC | CC | CC | CC | CC | CC | CC | CC | DD |
| CB1h | CC | CC | CC | CC | CC | DD | CC | CC | CC | CC | CC | CC | DD |
| CB1r | CC | CC | CC | CC | CC | DD | CC | CC | CC | CC | CC | CC | DD |
| CBPh | CC | CC | CC | CC | CC | DD | CC | CC | CC | CC | CC | CC | DD |
| CBPr | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD | DD | DD | DD |

## 3.O1 Arm O, self-only (Hyp^self only; the RE's guard), K = 1e5

| row \ col | C | D | CB | CB1 | CBP | CBlet | CBwrap | CB0 | Ccert | Dcert | SF | SFc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C | CC | CD | CD | CD | CD | CD | CD | CD | CC | CD | CC | CC |
| D | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| CB | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | CC |
| CB1 | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| CBP | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| CBlet | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | CC |
| CBwrap | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | CC |
| CB0 | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | CC |
| Ccert | CC | CD | CC | CD | CD | CC | CC | CC | CC | CD | CC | CC |
| Dcert | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| SF | CC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |
| SFc | CC | DD | CC | DD | DD | CC | CC | CC | CC | DD | DD | DD |

## 3.O2 Arm O, self-only (Hyp^self only; the RE's guard), K = 1e6

| row \ col | C | D | CB | CB1 | CBP | CBlet | CBwrap | CB0 | Ccert | Dcert | SF | SFc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C | CC | CD | CD | CD | CD | CD | CD | CD | CC | CD | CC | CC |
| D | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| CB | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | CC |
| CB1 | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| CBP | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| CBlet | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | CC |
| CBwrap | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | CC |
| CB0 | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | CC |
| Ccert | CC | CD | CC | CD | CD | CC | CC | CC | CC | CD | CC | CC |
| Dcert | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| SF | CC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |
| SFc | CC | DD | CC | DD | DD | CC | CC | CC | CC | DD | DD | DD |

## 3.O3 Arm O, self-only (Hyp^self only; the RE's guard), K = 1e7

| row \ col | C | D | CB | CB1 | CBP | CBlet | CBwrap | CB0 | Ccert | Dcert | SF | SFc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C | CC | CD | CD | CD | CD | CD | CD | CD | CC | CD | CC | CC |
| D | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| CB | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | CC |
| CB1 | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| CBP | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| CBlet | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | CC |
| CBwrap | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | CC |
| CB0 | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | CC |
| Ccert | CC | CD | CC | CD | CD | CC | CC | CC | CC | CD | CC | CC |
| Dcert | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| SF | CC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |
| SFc | CC | DD | CC | DD | DD | CC | CC | CC | CC | DD | DD | DD |

## 3.X1 Arm X, none (no hypothesis rule; acyclic scripts), K = 1e5

| row \ col | C | D | CB | CB1 | CBP | CBlet | CBwrap | CB0 | Ccert | Dcert | SF | SFc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C | CC | CD | CD | CD | CD | CD | CD | CD | CC | CD | CC | CC |
| D | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| CB | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |
| CB1 | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| CBP | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| CBlet | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |
| CBwrap | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |
| CB0 | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |
| Ccert | CC | CD | CC | CD | CD | CC | CC | CC | CC | CD | CC | CC |
| Dcert | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| SF | CC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |
| SFc | CC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |

## 3.X2 Arm X, none (no hypothesis rule; acyclic scripts), K = 1e6

| row \ col | C | D | CB | CB1 | CBP | CBlet | CBwrap | CB0 | Ccert | Dcert | SF | SFc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C | CC | CD | CD | CD | CD | CD | CD | CD | CC | CD | CC | CC |
| D | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| CB | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |
| CB1 | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| CBP | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| CBlet | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |
| CBwrap | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |
| CB0 | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |
| Ccert | CC | CD | CC | CD | CD | CC | CC | CC | CC | CD | CC | CC |
| Dcert | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| SF | CC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |
| SFc | CC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |

## 3.X3 Arm X, none (no hypothesis rule; acyclic scripts), K = 1e7

| row \ col | C | D | CB | CB1 | CBP | CBlet | CBwrap | CB0 | Ccert | Dcert | SF | SFc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C | CC | CD | CD | CD | CD | CD | CD | CD | CC | CD | CC | CC |
| D | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| CB | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |
| CB1 | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| CBP | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| CBlet | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |
| CBwrap | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |
| CB0 | DC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |
| Ccert | CC | CD | CC | CD | CD | CC | CC | CC | CC | CD | CC | CC |
| Dcert | DC | DD | DD | DD | DD | DD | DD | DD | DC | DD | DD | DD |
| SF | CC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |
| SFc | CC | DD | DD | DD | DD | DD | DD | DD | CC | DD | DD | DD |

## 4. Decomposition: which carrier pairs cooperate in which arm

| K | arm | twins (C,C) | distinct carrier pairs (C,C) | with Ccert | with SFc |
|---|---|---|---|---|---|
| 1e5 | X | 0/5 | 0/10 | 3/5 | 0/5 |
| 1e5 | O | 0/5 | 0/10 | 3/5 | 3/5 |
| 1e5 | S | 5/5 | 6/10 | 4/5 | 3/5 |
| 1e6 | X | 0/5 | 0/10 | 3/5 | 0/5 |
| 1e6 | O | 0/5 | 0/10 | 3/5 | 3/5 |
| 1e6 | S | 5/5 | 10/10 | 4/5 | 3/5 |
| 1e7 | X | 0/5 | 0/10 | 3/5 | 0/5 |
| 1e7 | O | 0/5 | 0/10 | 3/5 | 3/5 |
| 1e7 | S | 5/5 | 10/10 | 4/5 | 3/5 |

## 5. Soundness audit, host replay, Lemma Sym, nesting and regress

Distinct top-level checks met in the plays (mode 0 sound, 1 naive, 2 self-only, 3 none, 4 sloppy, 5 sound copy). "violations": T checks whose certified atom the actual play contradicts. "S closed": T checks that closed the swap box; "Sym ok": of those, the swap check is T and costs the same (partner closed R) or no more.

| K | arm | mode | checks | T | F | TO | host agrees | host disagrees | violations | S closed | Sym ok |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1e5 | S | 0 | 453 | 147 | 245 | 61 | 392 | 0 | 0 | 59 | 59 |
| 1e5 | S | 1 | 60 | 7 | 53 | 0 | 60 | 0 | 1 | 1 | 0 |
| 1e5 | S | 4 | 30 | 21 | 9 | 0 | 30 | 0 | 3 | 0 | 0 |
| 1e5 | S | 5 | 30 | 4 | 26 | 0 | 30 | 0 | 0 | 0 | 0 |
| 1e5 | O | 2 | 74 | 10 | 64 | 0 | 74 | 0 | 0 | 0 | 0 |
| 1e5 | X | 3 | 74 | 6 | 68 | 0 | 74 | 0 | 0 | 0 | 0 |
| 1e6 | S | 0 | 458 | 204 | 254 | 0 | 458 | 0 | 0 | 115 | 115 |
| 1e6 | S | 1 | 60 | 7 | 53 | 0 | 60 | 0 | 1 | 1 | 0 |
| 1e6 | S | 4 | 30 | 21 | 9 | 0 | 30 | 0 | 3 | 0 | 0 |
| 1e6 | S | 5 | 30 | 4 | 26 | 0 | 30 | 0 | 0 | 0 | 0 |
| 1e6 | O | 2 | 74 | 10 | 64 | 0 | 74 | 0 | 0 | 0 | 0 |
| 1e6 | X | 3 | 74 | 6 | 68 | 0 | 74 | 0 | 0 | 0 | 0 |
| 1e7 | S | 0 | 458 | 204 | 254 | 0 | 458 | 0 | 0 | 115 | 115 |
| 1e7 | S | 1 | 60 | 7 | 53 | 0 | 60 | 0 | 1 | 1 | 0 |
| 1e7 | S | 4 | 30 | 21 | 9 | 0 | 30 | 0 | 3 | 0 | 0 |
| 1e7 | S | 5 | 30 | 4 | 26 | 0 | 30 | 0 | 0 | 0 | 0 |
| 1e7 | O | 2 | 74 | 10 | 64 | 0 | 74 | 0 | 0 | 0 | 0 |
| 1e7 | X | 3 | 74 | 6 | 68 | 0 | 74 | 0 | 0 | 0 | 0 |

Fresh re-evaluation of every distinct top-level check (cache cleared): host nesting depth of check frames, checks in which the term met a regress (a call re-entering an enclosing check), and the largest inner cost of a check returning T:

| K | arm | checks | nesting depth: count | with regress | regress and T | max inner steps of a T check |
|---|---|---|---|---|---|---|
| 1e5 | S | 573 | {1: 484, 2: 47, 3: 42} | 0 | 0 | 24389 |
| 1e5 | O | 74 | {1: 74} | 0 | 0 | 15108 |
| 1e5 | X | 74 | {1: 74} | 0 | 0 | 2073 |
| 1e6 | S | 578 | {1: 487, 2: 47, 3: 44} | 0 | 0 | 50986 |
| 1e6 | O | 74 | {1: 74} | 0 | 0 | 15108 |
| 1e6 | X | 74 | {1: 74} | 0 | 0 | 2073 |
| 1e7 | S | 578 | {1: 487, 2: 47, 3: 44} | 0 | 0 | 50986 |
| 1e7 | O | 74 | {1: 74} | 0 | 0 | 15108 |
| 1e7 | X | 74 | {1: 74} | 0 | 0 | 2073 |

## 6. Held-out sources

| K | held-out | class | class script validates against CB, CB1, CBP | fresh production | (C,C) with production set, class script | same, fresh script | self-play (class/fresh) |
|---|---|---|---|---|---|---|---|
| 1e5 | CBlet2 | CB | no | C: EvR*; ChkR[EvR*; Ax · Hyp] (5); D: EvR*; ChkR[RunNeg · EvR*@1; Ax] (5) | 7/9 | 7/9 | C/C |
| 1e5 | CBw2 | CB | no | C: EvR*; ChkR[EvR*; Ax · Hyp] (5); D: EvR*; ChkR[RunNeg · EvR*@1; Ax] (5) | 7/9 | 7/9 | C/C |
| 1e5 | CB1h | CB1 | no | C: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Hyp] (8); D: EvR*; ChkR[RunNeg · EvR*@1; Ax] (5) | 5/9 | 5/9 | C/C |
| 1e5 | CB1r | CB1 | no | C: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Hyp] (8); D: EvR*; ChkR[RunNeg · EvR*@1; Ax] (5) | 5/9 | 5/9 | C/C |
| 1e5 | CBPh | CBP | no | C: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Run] · Hyp] (8); D: EvR*; ChkR[RunNeg · EvR*@1; Ax] (5) | 1/9 | 1/9 | D/D |
| 1e5 | CBPr | CBP | no | C: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Run] (8); D: EvR*; ChkR[RunNeg · EvR*@1; Ax] (5) | 1/9 | 1/9 | D/C |
| 1e6 | CBlet2 | CB | yes | C: EvR*; ChkR[EvR*; Ax · Hyp] (5); D: EvR*; ChkR[RunNeg · EvR*@1; Ax] (5) | 9/9 | 9/9 | C/C |
| 1e6 | CBw2 | CB | yes | C: EvR*; ChkR[EvR*; Ax · Hyp] (5); D: EvR*; ChkR[RunNeg · EvR*@1; Ax] (5) | 9/9 | 9/9 | C/C |
| 1e6 | CB1h | CB1 | yes | C: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Hyp] (8); D: EvR*; ChkR[RunNeg · EvR*@1; Ax] (5) | 8/9 | 8/9 | C/C |
| 1e6 | CB1r | CB1 | yes | C: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Hyp] (8); D: EvR*; ChkR[RunNeg · EvR*@1; Ax] (5) | 8/9 | 8/9 | C/C |
| 1e6 | CBPh | CBP | yes | C: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Run] · Hyp] (8); D: EvR*; ChkR[RunNeg · EvR*@1; Ax] (5) | 6/9 | 6/9 | C/C |
| 1e6 | CBPr | CBP | no | C: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Run] (8); D: EvR*; ChkR[RunNeg · EvR*@1; Ax] (5) | 1/9 | 6/9 | D/C |
| 1e7 | CBlet2 | CB | yes | C: EvR*; ChkR[EvR*; Ax · Hyp] (5); D: EvR*; ChkR[RunNeg · EvR*@1; Ax] (5) | 9/9 | 9/9 | C/C |
| 1e7 | CBw2 | CB | yes | C: EvR*; ChkR[EvR*; Ax · Hyp] (5); D: EvR*; ChkR[RunNeg · EvR*@1; Ax] (5) | 9/9 | 9/9 | C/C |
| 1e7 | CB1h | CB1 | yes | C: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Hyp] (8); D: EvR*; ChkR[RunNeg · EvR*@1; Ax] (5) | 8/9 | 8/9 | C/C |
| 1e7 | CB1r | CB1 | yes | C: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Hyp] (8); D: EvR*; ChkR[RunNeg · EvR*@1; Ax] (5) | 8/9 | 8/9 | C/C |
| 1e7 | CBPh | CBP | yes | C: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Run] · Hyp] (8); D: EvR*; ChkR[RunNeg · EvR*@1; Ax] (5) | 6/9 | 6/9 | C/C |
| 1e7 | CBPr | CBP | no | C: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Run] (8); D: EvR*; ChkR[RunNeg · EvR*@1; Ax] (5) | 1/9 | 6/9 | D/C |

## 7. Fuel boundary cells

V scan (K = 10⁶, sources rebuilt with the scanned V; W = the measured inner steps of the check):

| target|reader | W | V | check | inner steps | play target | play reader |
|---|---|---|---|---|---|---|
| CB|CB | 8782 | V=W-1 | TO | 8781 | D | D |
| CB|CB | 8782 | V=W+0 | T | 8782 | C | C |
| CB|CB | 8782 | V=W+1 | T | 8782 | C | C |
| CB|CB1 | 21541 | V=W-1 | TO | 21540 | D | D |
| CB|CB1 | 21541 | V=W+0 | T | 21541 | C | C |
| CB|CB1 | 21541 | V=W+1 | T | 21541 | C | C |
| CB|CBP | 30491 | V=W-1 | TO | 30490 | D | D |
| CB|CBP | 30491 | V=W+0 | T | 30491 | C | C |
| CB|CBP | 30491 | V=W+1 | T | 30491 | C | C |
| CB1|CBP | 37140 | V=W-1 | TO | 37139 | D | D |
| CB1|CBP | 37140 | V=W+0 | T | 37140 | C | C |
| CB1|CBP | 37140 | V=W+1 | T | 37140 | C | C |
| SFc|CB | 16315 | V=W-1 | TO | 16314 | D | D |
| SFc|CB | 16315 | V=W+0 | T | 16315 | C | C |
| SFc|CB | 16315 | V=W+1 | T | 16315 | C | C |

K scan (V = 25,000 fixed in the sources; b = the static fit boundary: K = V + 10 for CB, 2V + 17 for two-call carriers):

| x|y | static boundary | K | y checks x | play x | steps x | play y |
|---|---|---|---|---|---|---|
| CB|CB | 25010 | K=b-2 | F | D | 8256 | D |
| CB|CB | 25010 | K=b-1 | F | D | 8547 | D |
| CB|CB | 25010 | K=b+0 | T | C | 8792 | C |
| CB|CB | 25010 | K=b+1 | T | C | 8792 | C |
| CB|CB1 | 50017 | K=b-2 | F | D | 12162 | D |
| CB|CB1 | 50017 | K=b-1 | F | D | 12461 | D |
| CB|CB1 | 50017 | K=b+0 | T | C | 21551 | C |
| CB|CB1 | 50017 | K=b+1 | T | C | 21551 | C |
| CB1|CB | 50017 | K=b-2 | F | D | 20930 | D |
| CB1|CB | 50017 | K=b-1 | F | D | 21229 | D |
| CB1|CB | 50017 | K=b+0 | T | C | 43099 | C |
| CB1|CB | 50017 | K=b+1 | T | C | 43099 | C |
| CB|CBP | 50017 | K=b-2 | F | D | 12171 | D |
| CB|CBP | 50017 | K=b-1 | F | D | 12470 | D |
| CB|CBP | 50017 | K=b+0 | TO | D | 25010 | D |
| CB|CBP | 50017 | K=b+1 | TO | D | 25010 | D |
| CBP|CB | 50017 | K=b-2 | F | D | 20939 | D |
| CBP|CB | 50017 | K=b-1 | F | D | 21238 | D |
| CBP|CB | 50017 | K=b+0 | TO | D | 25010 | D |
| CBP|CB | 50017 | K=b+1 | TO | D | 25010 | D |

## 8. Fuzz soundness audit (K = 10⁵)

| mode | checks | accepted (T) | accepted false atoms |
|---|---|---|---|
| 0 | 3528 | 591 | 0 |
| 1 | 3528 | 909 | 36 |
| 2 | 3528 | 767 | 0 |
| 3 | 3528 | 715 | 0 |
| 5 | 3528 | 815 | 0 |

## 9. Finite-K plateau (arm S)

- 1e5 → 1e6: 62 ordered cells change: CB1h|CB1, CB1h|CB1r, CB1h|CBP, CB1h|CBPh, CB1h|CBmut, CB1r|CB1, CB1r|CB1h, CB1r|CBP, CB1r|CBPh, CB1r|CBmut, CB1|CB1h, CB1|CB1r, CB1|CBP, CB1|CBPh, CB1|CBmut, CBPh|CB, CBPh|CB1, CBPh|CB1h, CBPh|CB1r, CBPh|CBP, CBPh|CBPh, CBPh|CBlet, CBPh|CBlet2, CBPh|CBw2, CBPh|CBwrap, CBP|CB, CBP|CB1, CBP|CB1h, CBP|CB1r, CBP|CBPh, CBP|CBlet, CBP|CBlet2, CBP|CBw2, CBP|CBwrap, CBlet2|CBP, CBlet2|CBPh, CBlet2|CBmut, CBlet|CBP, CBlet|CBPh, CBlet|CBmut, CBmut|CB, CBmut|CB1, CBmut|CB1h, CBmut|CB1r, CBmut|CBlet, CBmut|CBlet2, CBmut|CBw2, CBmut|CBwrap, CBw2|CBP, CBw2|CBPh, CBw2|CBmut, CBwrap|CBP, CBwrap|CBPh, CBwrap|CBmut, CB|CBP, CB|CBPh, CB|CBmut, FB1_code|C, FB1_code|Ccert, FB_code|Ccert
- 1e6 → 1e7: 10 ordered cells change: FB1_code|FB1_code, FB1_code|SF, FB1_code|SFc, FB_code|SF, FB_code|SFc, PB_code|PB_code, SFc|FB1_code, SFc|FB_code, SF|FB1_code, SF|FB_code

## 10. Searchers against carriers (arm S)

| K | top-level search outcomes of searchers against carriers (T found, F refuted, TO interrupted) |
|---|---|
| 1e5 | FB1_code TO: 15, FB_code TO: 15, G_code TO: 15, PB_code TO: 15 |
| 1e6 | FB1_code T: 1, FB1_code TO: 14, FB_code T: 1, FB_code TO: 14, G_code T: 1, G_code TO: 14, PB_code T: 1, PB_code TO: 15 |
| 1e7 | FB1_code F: 12, FB1_code T: 2, FB1_code TO: 1, FB_code F: 12, FB_code T: 2, FB_code TO: 1, G_code F: 13, G_code T: 1, G_code TO: 1, PB_code F: 14, PB_code T: 1, PB_code TO: 1 |

Held-out rows against their class representative (arm S main cells; the held-out source carries the production-set script of its class): columns where the pair (held-out vs column, column vs held-out) differs from (class vs column, column vs class):

| K | held-out | class | differing columns |
|---|---|---|---|
| 1e5 | CBlet2 | CB | none |
| 1e5 | CBw2 | CB | none |
| 1e5 | CB1h | CB1 | CB1 |
| 1e5 | CB1r | CB1 | CB1 |
| 1e5 | CBPh | CBP | CBP |
| 1e5 | CBPr | CBP | CBP |
| 1e6 | CBlet2 | CB | none |
| 1e6 | CBw2 | CB | none |
| 1e6 | CB1h | CB1 | none |
| 1e6 | CB1r | CB1 | none |
| 1e6 | CBPh | CBP | none |
| 1e6 | CBPr | CBP | CB, CB1, CBP, CBlet, CBwrap |
| 1e7 | CBlet2 | CB | none |
| 1e7 | CBw2 | CB | none |
| 1e7 | CB1h | CB1 | none |
| 1e7 | CB1r | CB1 | none |
| 1e7 | CBPh | CBP | none |
| 1e7 | CBPr | CBP | CB, CB1, CBP, CBlet, CBwrap |

## 11. Supplement: cross-checker carriers whose scripts Run the other checker's call

Run after the main cells. CBrun / CBS2run / CBNrun carry EvR*; ChkR[EvR*; Ax · Run] (Run in place of Hyp on the partner's call) plus the D script. Term regress events counted on a fresh evaluation.

| K | check | result | inner steps | regress events | plays (x, y) |
|---|---|---|---|---|---|
| 1000000 | CB checked by CBS2run | F | 8801 | 0 | DD |
| 1000000 | CBS2run checked by CB | F | 17633 | 0 | DD |
| 1000000 | CBrun checked by CBS2 | F | 17631 | 0 | DD |
| 1000000 | CBrun checked by CBS2run | TO | 250000 | 1 | DD |
| 1000000 | CB checked by CBNrun | F | 8803 | 0 | DD |
| 1000000 | CBNrun checked by CB | F | 17643 | 0 | DD |
| 1000000 | CBrun checked by CBNrun | TO | 250000 | 1 | DD |
| 1000000 | CBS2 checked by CBS2run | F | 17583 | 0 | DD |
| 10000000 | CB checked by CBS2run | F | 8801 | 0 | DD |
| 10000000 | CBS2run checked by CB | F | 17633 | 0 | DD |
| 10000000 | CBrun checked by CBS2 | F | 17631 | 0 | DD |
| 10000000 | CBrun checked by CBS2run | TO | 2500000 | 1 | DD |
| 10000000 | CB checked by CBNrun | F | 8803 | 0 | DD |
| 10000000 | CBNrun checked by CB | F | 17643 | 0 | DD |
| 10000000 | CBrun checked by CBNrun | TO | 2500000 | 1 | DD |
| 10000000 | CBS2 checked by CBS2run | F | 17583 | 0 | DD |

## 12. Supplement: arm O with self-probe production

Run after the main cells. The frozen procedure's probes are other carriers, so under the self-only checker no carrier got a C script and no twin cooperated in §3. Here each carrier's C script is produced against its own twin and carried.

K = 100000; scripts: CB: EvR*; ChkR[EvR*; Ax · Hyp]; CB1: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Ax] · Hyp]; CBP: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Run] · Hyp]; CBlet: EvR*; ChkR[EvR*; Ax · Hyp]; CBwrap: EvR*; ChkR[EvR*; Ax · Hyp]

| row \ col | CB | CB1 | CBP | CBlet | CBwrap | Ccert | SFc | CB0 |
|---|---|---|---|---|---|---|---|---|
| CB | CC | DD | DD | DD | DD | CC | CC | DD |
| CB1 | DD | CC | DD | DD | DD | DC | DD | DD |
| CBP | DD | DD | CC | DD | DD | DC | DD | DD |
| CBlet | DD | DD | DD | CC | DD | CC | CC | DD |
| CBwrap | DD | DD | DD | DD | CC | CC | CC | DD |

K = 1000000; scripts: CB: EvR*; ChkR[EvR*; Ax · Hyp]; CB1: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Ax] · Hyp]; CBP: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Run] · Hyp]; CBlet: EvR*; ChkR[EvR*; Ax · Hyp]; CBwrap: EvR*; ChkR[EvR*; Ax · Hyp]

| row \ col | CB | CB1 | CBP | CBlet | CBwrap | Ccert | SFc | CB0 |
|---|---|---|---|---|---|---|---|---|
| CB | CC | DD | DD | DD | DD | CC | CC | DD |
| CB1 | DD | CC | DD | DD | DD | DC | DD | DD |
| CBP | DD | DD | CC | DD | DD | DC | DD | DD |
| CBlet | DD | DD | DD | CC | DD | CC | CC | DD |
| CBwrap | DD | DD | DD | DD | CC | CC | CC | DD |

K = 10000000; scripts: CB: EvR*; ChkR[EvR*; Ax · Hyp]; CB1: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Ax] · Hyp]; CBP: EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Run] · Hyp]; CBlet: EvR*; ChkR[EvR*; Ax · Hyp]; CBwrap: EvR*; ChkR[EvR*; Ax · Hyp]

| row \ col | CB | CB1 | CBP | CBlet | CBwrap | Ccert | SFc | CB0 |
|---|---|---|---|---|---|---|---|---|
| CB | CC | DD | DD | DD | DD | CC | CC | DD |
| CB1 | DD | CC | DD | DD | DD | DC | DD | DD |
| CBP | DD | DD | CC | DD | DD | DC | DD | DD |
| CBlet | DD | DD | DD | CC | DD | CC | CC | DD |
| CBwrap | DD | DD | DD | DD | CC | CC | CC | DD |

## 13. Verdicts

Scored by the rules fixed in the predictions file before any cell.

| # | prediction | outcome |
|---|---|---|
| RE 1 | the pair rule is sound with one guard (the checker's own call); the unrestricted rule admits Dcert; 0 violations | **Falsifier not fired** (a sound guard exists; 0 accepted false atoms for the sound, copy, self-only and none checkers in every cell, 0 in 3 × 3,528 fuzz checks). **The stated guard and the stated counterexample were wrong** (notes §1.6–1.7, confirmed): the own-call guard (arm O) is sound but certifies twins and SFc only; the guard that admits distinct sources is *partner validation of the swap*; Dcert is uncertifiable under every hypothesis rule (its run has no call) and fools only the sloppy checker; the unguarded rule's false atom is CBN0 accepting CBN (1 per K in the catalogue, 36 of 909 accepted in the naive fuzz) |
| RE 2 | CB and CB1 cooperate at K = 10⁶, each check ≤ 10⁵, no re-entry | **Held.** 21,541 steps per check (first K 86,164); largest check returning T anywhere 50,986; 0 regress events in arm S; nesting depth 1 for FB-shaped pairs, 3 with CBP |
| RE 3 | carriers and searchers (D, D) | **Held** for every reader-carrier at every K (searches about carriers interrupted at 10⁵–10⁶, refuted at 10⁷, never found). Not predicted: SFc, a certificate-carrying simulator, is cooperated with by CB-shaped carriers (certificate) and, at 10⁷, by FB_code and FB1_code (milestone 3's FB–SF mechanism): a bridge between the two worlds, while carriers and searchers still defect on each other |
| RE 4 | fakers rejected by soundness | **Held.** CBfake (its scripts fail on its actual run; there is no carried root to mismatch), CBdef (suckered: reader D, CBdef C), CBmut (cooperated with by FB- and FB1-shaped readers, refused by CBP: no D script), CBsloppy (cooperates with every carrier that has entries, with Dcert, CBfake and CBdef, which exploit it; refuses plain D; every sound carrier, CBP included, cooperates with it) |
| RE 5 | literal certificates fail on respellings; quantified templates cover every held-out same-shape carrier at ≤ 2× | **Failed, falsifier fired.** Clause 1 has no object (Lemma F: no literal self-certificates). Scripts are opponent-generic templates with no instantiation cost, and the production-set script of the class covers CBlet2, CBw2, CB1h, CB1r and CBPh (their rows equal their class representative's in every cell at K ≥ 10⁶), but **not CBPr** (PB-shaped, the two calls in the other order: a different call skeleton). A fresh production fixes it (8 nodes, 29 tactic nodes) and no production-set carrier needs a new certificate |
| RE 6 | the disabled control is not twins-only: acyclic proofs certify carrier–C and carrier–SF at equal cost; the pair rule adds exactly the carrier–carrier cells | **Falsifier not fired; two clauses failed.** Arm X certifies carrier–Ccert at equal cost (2,065 / 2,071 / 2,073 steps in arms S / O / X); no carrier–carrier cell without a hypothesis rule; no Ccert cell lost with it. But SFc is not certified without a hypothesis rule (its certificate needs Hyp^self: the reader's own check runs inside SFc's simulation), and the sound arm adds twins, SFc and CB1–Ccert beside the distinct pairs, not exactly the carrier–carrier cells |
| S1 | 0 violations for modes 0, 2, 3, 5 | **Held** |
| S2 | the naive checker accepts a false atom; CB0–CB (D, D) | **Held** (every K; fuzz 36) |
| S3 | decomposition X ⊂ O ⊂ S | **Falsifier not fired; partly failed.** X: carriers with Ccert only (3/5: CB1 and CBP refuse Ccert, CB1 because its self-audit needs the pair rule, CBP because Ccert has no D script). O: SFc as predicted, **but no twins**: the frozen production never meets a twin, so self-only carriers carry no C script; with self-probe production (§12) twins cooperate and no distinct pair does. S: all 10 distinct pairs at 10⁶ and 10⁷ (6/10 at 10⁵) |
| S4 | Lemma Sym measured | **Held** (115/115 at 10⁶ and 10⁷, 59/59 at 10⁵) |
| S5 | every check ≤ 10⁵; CB–CB at 10⁵ | **Held** (max 50,986; CB–CB from K = 35,128) |
| S6 | simulators | **Held** |
| S7 | fakers | **Held**; also CBdef exploits CBsloppy |
| S8 | cross-checker pairs (D, D) with a regress in each check | **Failed, falsifier fired** on the regress clause: (D, D) as predicted, but with no regress, because the produced scripts name the partner's call as a hypothesis and the check fails there; a regress (and a timeout at the full cap) occurs only when both scripts Run each other's call (§11) |
| S9 | carrier–searcher (D, D); no searcher query about a carrier found | **Failed as worded**: (D, D) for every reader-carrier, but searchers find queries about the certificate-carrying non-readers Ccert (from 10⁶) and SFc (10⁷) |
| S10 | held-out coverage | **Partly failed:** coverage exactly as predicted (CBPr alone uncovered, fresh script 8 nodes); "cooperates with every production-set carrier" was too broad: held-out rows equal their class's, so two-call carriers are (D, D) with SFc and PB-shaped ones refuse LöbC and CBmut, as CB1 and CBP do. No production-set carrier needed a new certificate |
| S11 | static boundaries | **Held** (cost W + 6 ≤ V + 6; V flip at W; K flip at V + 10 and 2V + 17); one clause wrong: "the actual run would succeed below the boundary" — below it the program's own check fails, so the play is D and atom and play agree |
| S12 | every arm-S cell equal at 10⁶ and 10⁷ | **Failed as worded:** every certificate cell is equal; 10 milestone-3 cells change (searchers and simulators: FB_code–SF, FB1_code twins, PB_code twins, SFc–searchers), milestone 3's own plateau |

