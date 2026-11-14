## Step 1: length-prior mass of R (conditional on finite trees; exact-member lower bounds from the grammar search)

| machine | R (n variants) | R (y variants) | fair single (this search / q75) | bully (this search / q75) | 1/3 constants C3 + C0 | R_n / single | R_n / bully | R_n / (C3 + C0) | shortest R_n / R_y / single / bully | MC 95% upper (R_n) |
|---|---|---|---|---|---|---|---|---|---|---|
| R0 | 1.26e-23 | 1.14e-35 | 4.08e-24 / 4.08e-24 | 1.26e-23 / 1.26e-23 | 0.0676 | 3.09 | 1 | 1.86e-22 | 12 / 20 / 12 / 12 | 6.74e-07 (5700481 finite draws, hits {'Rnn': 0, 'Rny': 0, 'Rpn': 0, 'Rpy': 0}) |
| R1 | 9.73e-11 | 3.8e-23 | 3.15e-11 / 3.15e-11 | 9.73e-11 / 9.73e-11 | 0.0428 | 3.09 | 1 | 2.27e-09 | 6 / 14 / 6 / 6 | - |

- R0 Rnn: 7.42e-25 (cond), shortest 12 nodes: `(if (eq (capk 95 (run 95 #1 #0) #2) 4) 1 3)` (120 spellings counted)
- R0 Rny: 6.73e-37 (cond), shortest 20 nodes: `(app (lam (if (if (eq #0 4) T (eq #0 TO)) 1 3)) (capk 95 (run 95 #1 #0) #2))` (30 spellings counted)
- R0 Rpn: 1.19e-23 (cond), shortest 12 nodes: `(if (eq (capk 95 (run 95 #0 #2) #1) 1) 4 0)` (120 spellings counted)
- R0 Rpy: 1.08e-35 (cond), shortest 20 nodes: `(app (lam (if (if (eq #0 1) T (eq #0 TO)) 4 0)) (capk 95 (run 95 #0 #2) #1))` (30 spellings counted)
- R1 Rnn: 5.72e-12 (cond), shortest 6 nodes: `(if (eq readn 4) 1 3)` (8 spellings counted)
- R1 Rny: 2.24e-24 (cond), shortest 14 nodes: `(app (lam (if (if (eq #0 4) T (eq #0 TO)) 1 3)) readn)` (2 spellings counted)
- R1 Rpn: 9.16e-11 (cond), shortest 6 nodes: `(if (eq readp 1) 4 0)` (8 spellings counted)
- R1 Rpy: 3.58e-23 (cond), shortest 14 nodes: `(app (lam (if (if (eq #0 1) T (eq #0 TO)) 4 0)) readp)` (2 spellings counted)
