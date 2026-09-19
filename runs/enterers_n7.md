# Unfakeable enterers, weak arm L_7 (9426 programs)

Conditions: (i) u(p,D) >= u(D,D) = -1; (ii) u(p,p) > u(D,D); (iii) no q in L_7 invades all-p from rare.
Candidates satisfying (i) and (ii): 98; full (iii) tests after the L_6 prefilter: 0.

## No program in L_7 satisfies all three.

## Shortest satisfying (i)+(ii): `THEM(^C)` (4 nodes, 10.95 bits)

u(p,D) = -1 (u(D,D) = -1), u(p,p) = 0, u(D,p) = -1
(i) True, (ii) True, (iii) False
invaders (shortest): `THEM(^D)` u(q,p)=1 u(q,q)=-1 u(p,q)=-2; `THEM(^X)` u(q,p)=0.5 u(q,q)=-0.5 u(p,q)=-1; `THEM(^not(C))` u(q,p)=1 u(q,q)=-1 u(p,q)=-2; `THEM(^not(X))` u(q,p)=0.5 u(q,q)=-0.5 u(p,q)=-1; `THEM(^not(not(X)))` u(q,p)=0.5 u(q,q)=-0.5 u(p,q)=-1; `THEM(^and(C,D))` u(q,p)=1 u(q,q)=-1 u(p,q)=-2

| N | w | rho(p | all-D) |
|---|---|---|
| 10 | 0.01 | 1.013e-01 |
| 10 | 0.1 | 1.144e-01 |
| 10 | 1 | 5.000e-01 |
| 100 | 0.01 | 1.166e-02 |
| 100 | 0.1 | 2.584e-02 |
| 100 | 1 | 5.000e-01 |

## Shortest satisfying (i)+(iii): `and(X,and(X,THEM(ME)))` (7 nodes, 19.50 bits)

u(p,D) = -1 (u(D,D) = -1), u(p,p) = -1, u(D,p) = -1
(i) True, (ii) False, (iii) True

| N | w | rho(p | all-D) |
|---|---|---|
| 10 | 0.01 | 1.000e-01 |
| 10 | 0.1 | 1.000e-01 |
| 10 | 1 | 1.000e-01 |
| 100 | 0.01 | 1.000e-02 |
| 100 | 0.1 | 1.000e-02 |
| 100 | 1 | 1.000e-02 |

## Shortest satisfying (ii)+(iii): `or(and(X,X),THEM(ME))` (7 nodes, 19.50 bits)

u(p,D) = -1.25 (u(D,D) = -1), u(p,p) = -1.35e-11, u(D,p) = -0.5
(i) False, (ii) True, (iii) True

| N | w | rho(p | all-D) |
|---|---|---|
| 10 | 0.01 | 9.962e-02 |
| 10 | 0.1 | 9.573e-02 |
| 10 | 1 | 4.642e-12 |
| 100 | 0.01 | 9.951e-03 |
| 100 | 0.1 | 8.604e-03 |
| 100 | 1 | 2.047e-99 |

## Extra program: `or(and(and(X,X),THEM(^C)),THEM(ME))` (12 nodes, 32.77 bits)

u(p,D) = -1 (u(D,D) = -1), u(p,p) = -2.4e-11, u(D,p) = -1
(i) True, (ii) True, (iii) True

| N | w | rho(p | all-D) |
|---|---|---|
| 10 | 0.01 | 1.013e-01 |
| 10 | 0.1 | 1.144e-01 |
| 10 | 1 | 5.000e-01 |
| 100 | 0.01 | 1.166e-02 |
| 100 | 0.1 | 2.584e-02 |
| 100 | 1 | 5.000e-01 |

Wall time 51s.
