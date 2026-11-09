## Step 2: the length-prior mass of P, Q, O (conditional on finite trees; exact-member lower bounds; R2 = R1 + probn / probp)

| machine | q | fair single (lower bound) | bully | P_z | P_o | Q (y variants) | O | MC 95% upper bound on the reader classes (P, Q); other conditionals (O) |
|---|---|---|---|---|---|---|---|---|
| R0 | 0.4748 | 4.08e-24 | 1.26e-23 | 5.02e-52 | 1.27e-49 | 1.2e-69 | 2.27e-92 | 6.74e-07 (hits 0 of 12000000); other_cond hits 5, upper 2.05e-06 |
| R1 | 0.6667 | 3.15e-11 | 9.73e-11 | 4.96e-38 | 1.25e-35 | 3.72e-56 | 6.82e-63 | 9.6e-07 (hits 0 of 6000000); other_cond hits 7174, upper 0.00184 |
| R2 | 0.6667 | 1.78e-11 | 5.49e-11 | 2.31e-24 | 5.59e-22 | 9.3e-42 | 2.01e-64 | 9.6e-07 (hits 0 of 6000000); other_cond hits 6050, upper 0.00155 |

| machine | shortest fair single | shortest bully | shortest P_z (gap) | shortest P any (gap) | shortest O (gap) | P_z / single | P_z / bully | O / single |
|---|---|---|---|---|---|---|---|---|
| R0 | 12 | 12 | 26 (14) | 26 (14) | 49 (37) | 1.23e-28 | 3.98e-29 | 5.56e-69 |
| R1 | 6 | 6 | 20 (14) | 20 (14) | 37 (31) | 1.57e-27 | 5.09e-28 | 2.17e-52 |
| R2 | 6 | 6 | 12 (6) | 12 (6) | 37 (31) | 1.3e-13 | 4.21e-14 | 1.13e-53 |

R0: shortest P_z `(if (eq (capk 383 (run 383 #1 #0) #2) 4) (if (eq (app (run 383 #1 (quote (lam (lam (lam 3))))) #2) 2) 8 1) 8)`; shortest O `(app (lam (app (lam (if (if (eq #1 2) (eq #0 3) F) 4 (if (if (eq #0 5) (eq #1 0) F) 1 (if (eq #1 4) 1 (if (eq #0 1) 4 1))))) (capk 383 (run 383 #1 #3) #2))) (capk 383 (run 383 #1 #0) #2))`; shortest fair single `(if (eq (capk 95 (run 95 #1 #0) #2) 4) 1 4)`
R1: shortest P_z `(if (eq readn 4) (if (eq (app (run 383 #1 (quote (lam (lam (lam 3))))) #2) 2) 8 1) 8)`; shortest O `(app (lam (app (lam (if (if (eq #1 2) (eq #0 3) F) 4 (if (if (eq #0 5) (eq #1 0) F) 1 (if (eq #1 4) 1 (if (eq #0 1) 4 1))))) readp)) readn)`; shortest fair single `(if (eq readn 4) 1 4)`
R2: shortest P_z `(if (eq readn 4) (if (eq (probn 3) 2) 8 1) 8)`; shortest O `(app (lam (app (lam (if (if (eq #1 2) (eq #0 3) F) 4 (if (if (eq #0 5) (eq #1 0) F) 1 (if (eq #1 4) 1 (if (eq #0 1) 4 1))))) readp)) readn)`; shortest fair single `(if (eq readn 4) 1 4)`
