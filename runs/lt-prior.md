## Machine R0

tags 18, mean arity 1.3333, finite-tree mass q = 0.474810 (lost mass 0.525190); exhaustive enumeration to size s0 = 6

Mass accounting (V3): enumerated 0.249620460 (expected 0.249620460), excluded lib/libsrc/sim 0.164029997, above s0 (finite) 0.061159177, lost 0.525190366; sum 1.000000000000

| class | exhaustive raw (size <= s0) | MC estimate, cond. on finite [95% CI] | hits outside exhaustive | search lower bound beyond s0 (raw) |
|---|---|---|---|---|
| const | 0.05327 | 0.1202 [0.12, 0.12] | 45770 | exact 0 / family 0 |
| junk_f | 0.1963 | 0.8798 [0.879, 0.88] | 2656496 | exact 0 / family 0 |
| junk_r | 0 | 0 [0, 6.74e-07] | 0 | exact 0 / family 0 |
| const_read | 1.735e-08 | 1.724e-05 [1.42e-05, 2.1e-05] | 98 | exact 0 / family 1.15e-15 |
| single | 0 | 0 [0, 6.74e-07] | 0 | exact 1.94e-24 / family 3.71e-21 |
| two | 0 | 0 [0, 6.74e-07] | 0 | exact 0 / family 2.13e-60 |
| bully | 0 | 0 [0, 6.74e-07] | 0 | exact 5.99e-24 / family 9.22e-21 |
| exploit | 0 | 0 [0, 6.74e-07] | 0 | exact 0 / family 0 |
| yielder | 0 | 0 [0, 6.74e-07] | 0 | exact 0 / family 9.91e-19 |
| other_cond | 8.102e-07 | 2.584e-06 [2.08e-06, 3.76e-06] | 5 | exact 0 / family 3.7e-18 |

Headline: constants 0.1202 (cond.); reader lower bound (exact members) raw 1.94e-24, rho_R >= 3.39e-23; (family level) rho_R >= 6.5e-20; bully/reader ratio (exact) 3.090909090911457, (family) 2.482141632380467; junk 0.8798 (forfeit 0.8798, failed-read nan)

Shortest spellings: {"single/exact": {"min_size": 12, "example": "(if (eq (capk 95 (run 95 #1 #0) #2) 4) 1 4)", "counts": {"12": 120, "13": 0, "14": 0}, "masses": {"12": 1.9371837427211986e-24, "13": 0, "14": 0}}, "single/family": {"min_size": 11, "example": "(if (eq (app (run 95 #1 #0) #2) 4) 1 4)", "counts": {"11": 60, "12": 180, "13": 0}, "masses": {"11": 3.709732025541519e-21, "12": 1.2830697516724817e-24, "13": 0}}, "two/family": {"min_size": 29, "example": "(app (lam (if (eq #0 4) 1 (app (lam (if (eq #0 1) 4 1)) (capk 1500 (run 1500 #0 #2) #1)))) (capk 1500 (run 1500 #1 #0) #2))", "counts": {"29": 8, "30": 0, "31": 0}, "masses": {"29": 2.1262339852133427e-60, "30": 0, "31": 0}}, "bully/exact": {"min_size": 12, "example": "(if (eq (capk 95 (run 95 #1 #0) #2) 3) 2 4)", "counts": {"12": 60, "13": 0, "14": 0}, "masses": {"12": 5.9876588411382495e-24, "13": 0, "14": 0}}, "bully/family": {"min_size": 11, "example": "(if (eq (app (run 95 #1 #0) #2) 3) 2 4)", "counts": {"11": 40, "12": 140, "13": 0}, "masses": {"11": 9.208084849111987e-21, "12": 2.005470368160351e-24, "13": 0}}, "yielder/family": {"min_size": 11, "example": "(if (eq (app (run 95 #1 #0) #2) 0) 1 0)", "counts": {"11": 4500, "12": 22500, "13": 0}, "masses": {"11": 9.89739736094492e-19, "12": 8.591490764709191e-22, "13": 0}}}

## Machine R1

tags 20, mean arity 1.2000, finite-tree mass q = 0.666667 (lost mass 0.333333); exhaustive enumeration to size s0 = 5

Mass accounting (V3): enumerated 0.365507812 (expected 0.365507812), excluded lib/libsrc/sim 0.155616562, above s0 (finite) 0.145542292, lost 0.333333333; sum 1.000000000000

| class | exhaustive raw (size <= s0) | MC estimate, cond. on finite [95% CI] | hits outside exhaustive | search lower bound beyond s0 (raw) |
|---|---|---|---|---|
| const | 0.04751 | 0.07591 [0.0758, 0.076] | 18592 | exact 0 / family 0 |
| junk_f | 0.2012 | 0.719 [0.718, 0.72] | 1668417 | exact 0 / family 0 |
| junk_r | 0 | 0 [0, 9.6e-07] | 0 | exact 0 / family 0 |
| const_read | 0.0158 | 0.04117 [0.041, 0.0413] | 69865 | exact 0 / family 2.1e-08 |
| single | 6.338e-11 | 9.506e-11 [9.51e-11, 9.6e-07] | 0 | exact 2.1e-11 / family 3.05e-11 |
| two | 0 | 0 [0, 9.6e-07] | 0 | exact 5e-29 / family 1.18e-28 |
| bully | 0 | 0 [0, 9.6e-07] | 0 | exact 6.49e-11 / family 7.58e-11 |
| exploit | 0 | 0 [0, 9.6e-07] | 0 | exact 0 / family 0 |
| yielder | 6.143e-05 | 0.0001024 [9.97e-05, 0.000106] | 41 | exact 0 / family 8.14e-09 |
| other_cond | 0.1009 | 0.1531 [0.153, 0.153] | 7174 | exact 0 / family 4.46e-08 |

Headline: constants 0.07591 (cond.); reader lower bound (exact members) raw 2.1e-11, rho_R >= 4.15e-10; (family level) rho_R >= 1.86e-09; bully/reader ratio (exact) 3.0909090909101096, (family) 0.8067926359426746; junk 0.719 (forfeit 0.719, failed-read nan)

Shortest spellings: {"single/exact": {"min_size": 6, "example": "(if (eq readn 4) 1 4)", "counts": {"6": 8, "7": 0, "8": 0}, "masses": {"6": 2.098083496093751e-11, "7": 0, "8": 0}}, "single/family": {"min_size": 5, "example": "(mod 9 (mul 5 readp))", "counts": {"5": 20, "6": 4, "7": 0}, "masses": {"5": 6.337555087342557e-11, "6": 9.536743164062504e-12, "7": 0}}, "two/exact": {"min_size": 17, "example": "(app (lam (if (eq #0 4) 1 (app (lam (if (eq #0 1) 4 1)) readp))) readn)", "counts": {"17": 4, "18": 0, "19": 0}, "masses": {"17": 5.0022208597511104e-29, "18": 0, "19": 0}}, "two/family": {"min_size": 17, "example": "(app (lam (if (eq #0 4) 1 (app (lam (if (eq #0 1) 4 12)) readp))) readn)", "counts": {"17": 4, "18": 0, "19": 0}, "masses": {"17": 6.821210263296968e-29, "18": 0, "19": 0}}, "bully/exact": {"min_size": 6, "example": "(if (eq readn 3) 2 4)", "counts": {"6": 4, "7": 0, "8": 0}, "masses": {"6": 6.484985351562503e-11, "7": 0, "8": 0}}, "bully/family": {"min_size": 6, "example": "(if (le readp 0) 5 1)", "counts": {"6": 4, "7": 0, "8": 0}, "masses": {"6": 1.0899135044642859e-11, "7": 0, "8": 0}}, "yielder/family": {"min_size": 3, "example": "(div 0 readn)", "counts": {"3": 27, "4": 12, "5": 8672}, "masses": {"3": 5.651855468750001e-05, "4": 2.67857142857143e-06, "5": 2.2373076470530718e-06}}}
