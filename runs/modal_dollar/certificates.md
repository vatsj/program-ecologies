## Certificates (GLS+Def, five-valued definitional constants)

P^a[x,y] reads "x demands S_a against y"; its definition is x's source read against y (a disjunction over the
atom valuations whose table entry is a). An atom BOX_L(THEM = S_b) of x read against y is [](~[]^L F -> P^b[y,x]).
For each encounter: every box atom of each side, its provability (the terminating GL decision procedure of
`src/gl_proofs.py`; "not provable" is the exhaustive search failing, so the atom is false at the stable world),
the certified minimal derivation (size in sequents, Löb steps) of each provable atom, and the evaluator's play.

### P' = `if(BOX(S1),S5,S3)` vs P' = `if(BOX(S1),S5,S3)`: plays (S3, S3); evaluator (S3, S3)

- P''s atom BOX(THEM=S1): not provable
- P''s atom BOX(THEM=S1): not provable

### P' = `if(BOX(S1),S5,S3)` vs A5 = `if(BOX(S5),S1,S3)`: plays (S5, S1); evaluator (S5, S1)

- P''s atom BOX(THEM=S1): **provable**, 6 sequents, 2 Löb step(s)

```
 |- PS1[A5,P']   [UnfR]
   |- []PS5[P',A5]   [GLR]
    []PS5[P',A5] |- PS5[P',A5]   [UnfR]
      []PS5[P',A5] |- []PS1[A5,P']   [GLR]
        PS5[P',A5], []PS1[A5,P'], []PS5[P',A5] |- PS1[A5,P']   [UnfR]
          PS5[P',A5], []PS1[A5,P'], []PS5[P',A5] |- []PS5[P',A5]   [Ax]
```

- A5's atom BOX(THEM=S5): **provable**, 6 sequents, 2 Löb step(s)

```
 |- PS5[P',A5]   [UnfR]
   |- []PS1[A5,P']   [GLR]
    []PS1[A5,P'] |- PS1[A5,P']   [UnfR]
      []PS1[A5,P'] |- []PS5[P',A5]   [GLR]
        PS1[A5,P'], []PS1[A5,P'], []PS5[P',A5] |- PS5[P',A5]   [UnfR]
          PS1[A5,P'], []PS1[A5,P'], []PS5[P',A5] |- []PS1[A5,P']   [Ax]
```


### P' = `if(BOX(S1),S5,S3)` vs P = `{BOX(S1),BOX(S5): TT S5, TF S5, FT S1, FF S3}`: plays (S3, S3); evaluator (S3, S3)

- P''s atom BOX(THEM=S1): not provable
- P's atom BOX(THEM=S1): not provable
- P's atom BOX(THEM=S5): not provable

### P = `{BOX(S1),BOX(S5): TT S5, TF S5, FT S1, FF S3}` vs S5 = `S5`: plays (S1, S5); evaluator (S1, S5)

- P's atom BOX(THEM=S1): not provable
- P's atom BOX(THEM=S5): **provable**, 2 sequents, 0 Löb step(s)

```
 |- PS5[S5,P]   [UnfR]
   |- T   [Ax]
```


### A5 = `if(BOX(S5),S1,S3)` vs S5 = `S5`: plays (S1, S5); evaluator (S1, S5)

- A5's atom BOX(THEM=S5): **provable**, 2 sequents, 0 Löb step(s)

```
 |- PS5[S5,A5]   [UnfR]
   |- T   [Ax]
```


### A5 = `if(BOX(S5),S1,S3)` vs A5 = `if(BOX(S5),S1,S3)`: plays (S3, S3); evaluator (S3, S3)

- A5's atom BOX(THEM=S5): not provable
- A5's atom BOX(THEM=S5): not provable

### P = `{BOX(S1),BOX(S5): TT S5, TF S5, FT S1, FF S3}` vs P = `{BOX(S1),BOX(S5): TT S5, TF S5, FT S1, FF S3}`: plays (S3, S3); evaluator (S3, S3)

- P's atom BOX(THEM=S1): not provable
- P's atom BOX(THEM=S5): not provable
- P's atom BOX(THEM=S1): not provable
- P's atom BOX(THEM=S5): not provable

### P = `{BOX(S1),BOX(S5): TT S5, TF S5, FT S1, FF S3}` vs A5 = `if(BOX(S5),S1,S3)`: plays (S5, S1); evaluator (S5, S1)

- P's atom BOX(THEM=S1): **provable**, 14 sequents, 3 Löb step(s)

```
 |- PS1[A5,P]   [UnfR]
   |- []PS5[P,A5]   [GLR]
    []PS5[P,A5] |- PS5[P,A5]   [UnfR]
      []PS5[P,A5] |- (([]PS1[A5,P] & ~[]PS5[A5,P]) | ([]PS1[A5,P] & []PS5[A5,P]))   [|R]
        []PS5[P,A5] |- ([]PS1[A5,P] & []PS5[A5,P]), ([]PS1[A5,P] & ~[]PS5[A5,P])   [&R]
          []PS5[P,A5] |- ([]PS1[A5,P] & []PS5[A5,P]), []PS1[A5,P]   [GLR]
            PS5[P,A5], []PS1[A5,P], []PS5[P,A5] |- PS1[A5,P]   [UnfR]
              PS5[P,A5], []PS1[A5,P], []PS5[P,A5] |- []PS5[P,A5]   [Ax]
          []PS5[P,A5] |- ([]PS1[A5,P] & []PS5[A5,P]), ~[]PS5[A5,P]   [~R]
            []PS5[A5,P], []PS5[P,A5] |- ([]PS1[A5,P] & []PS5[A5,P])   [&R]
              []PS5[A5,P], []PS5[P,A5] |- []PS1[A5,P]   [GLR]
                PS5[A5,P], PS5[P,A5], []PS1[A5,P], []PS5[A5,P], []PS5[P,A5] |- PS1[A5,P]   [UnfL]
                  F, PS5[P,A5], []PS1[A5,P], []PS5[A5,P], []PS5[P,A5] |- PS1[A5,P]   [Ax]
              []PS5[A5,P], []PS5[P,A5] |- []PS5[A5,P]   [Ax]
```

- P's atom BOX(THEM=S5): not provable
- A5's atom BOX(THEM=S5): **provable**, 20 sequents, 3 Löb step(s)

```
 |- PS5[P,A5]   [UnfR]
   |- (([]PS1[A5,P] & ~[]PS5[A5,P]) | ([]PS1[A5,P] & []PS5[A5,P]))   [|R]
     |- ([]PS1[A5,P] & []PS5[A5,P]), ([]PS1[A5,P] & ~[]PS5[A5,P])   [&R]
       |- ([]PS1[A5,P] & []PS5[A5,P]), []PS1[A5,P]   [GLR]
        []PS1[A5,P] |- PS1[A5,P]   [UnfR]
          []PS1[A5,P] |- []PS5[P,A5]   [GLR]
            PS1[A5,P], []PS1[A5,P], []PS5[P,A5] |- PS5[P,A5]   [UnfR]
              PS1[A5,P], []PS1[A5,P], []PS5[P,A5] |- (([]PS1[A5,P] & ~[]PS5[A5,P]) | ([]PS1[A5,P] & []PS5[A5,P]))   [|R]
                PS1[A5,P], []PS1[A5,P], []PS5[P,A5] |- ([]PS1[A5,P] & []PS5[A5,P]), ([]PS1[A5,P] & ~[]PS5[A5,P])   [&R]
                  PS1[A5,P], []PS1[A5,P], []PS5[P,A5] |- ([]PS1[A5,P] & []PS5[A5,P]), []PS1[A5,P]   [Ax]
                  PS1[A5,P], []PS1[A5,P], []PS5[P,A5] |- ([]PS1[A5,P] & []PS5[A5,P]), ~[]PS5[A5,P]   [~R]
                    PS1[A5,P], []PS1[A5,P], []PS5[A5,P], []PS5[P,A5] |- ([]PS1[A5,P] & []PS5[A5,P])   [&R]
                      PS1[A5,P], []PS1[A5,P], []PS5[A5,P], []PS5[P,A5] |- []PS1[A5,P]   [Ax]
                      PS1[A5,P], []PS1[A5,P], []PS5[A5,P], []PS5[P,A5] |- []PS5[A5,P]   [Ax]
       |- ([]PS1[A5,P] & []PS5[A5,P]), ~[]PS5[A5,P]   [~R]
        []PS5[A5,P] |- ([]PS1[A5,P] & []PS5[A5,P])   [&R]
          []PS5[A5,P] |- []PS1[A5,P]   [GLR]
            PS5[A5,P], []PS1[A5,P], []PS5[A5,P] |- PS1[A5,P]   [UnfL]
              F, []PS1[A5,P], []PS5[A5,P] |- PS1[A5,P]   [Ax]
          []PS5[A5,P] |- []PS5[A5,P]   [Ax]
```


### P' = `if(BOX(S1),S5,S3)` vs S5 = `S5`: plays (S3, S5); evaluator (S3, S5)

- P''s atom BOX(THEM=S1): not provable

### P' = `if(BOX(S1),S5,S3)` vs C3 = `if(BOX(S3),S3,S1)`: plays (S3, S1); evaluator (S3, S1)

- P''s atom BOX(THEM=S1): not provable
- C3's atom BOX(THEM=S3): not provable

### P'1 = `if(BOX1(S1),S5,S3)` vs A5 = `if(BOX(S5),S1,S3)`: plays (S5, S1); evaluator (S5, S1)

- P'1's atom BOX1(THEM=S1): **provable**, 8 sequents, 2 Löb step(s)

```
 |- (~[]F -> PS1[A5,P'1])   [->R]
   |- PS1[A5,P'1]   [UnfR]
     |- []PS5[P'1,A5]   [GLR]
      []PS5[P'1,A5] |- PS5[P'1,A5]   [UnfR]
        []PS5[P'1,A5] |- [](~[]F -> PS1[A5,P'1])   [GLR]
          PS5[P'1,A5], [](~[]F -> PS1[A5,P'1]), []PS5[P'1,A5] |- (~[]F -> PS1[A5,P'1])   [->R]
            PS5[P'1,A5], [](~[]F -> PS1[A5,P'1]), []PS5[P'1,A5] |- PS1[A5,P'1]   [UnfR]
              PS5[P'1,A5], [](~[]F -> PS1[A5,P'1]), []PS5[P'1,A5] |- []PS5[P'1,A5]   [Ax]
```

- A5's atom BOX(THEM=S5): **provable**, 7 sequents, 2 Löb step(s)

```
 |- PS5[P'1,A5]   [UnfR]
   |- [](~[]F -> PS1[A5,P'1])   [GLR]
    [](~[]F -> PS1[A5,P'1]) |- (~[]F -> PS1[A5,P'1])   [->R]
      [](~[]F -> PS1[A5,P'1]) |- PS1[A5,P'1]   [UnfR]
        [](~[]F -> PS1[A5,P'1]) |- []PS5[P'1,A5]   [GLR]
          (~[]F -> PS1[A5,P'1]), [](~[]F -> PS1[A5,P'1]), []PS5[P'1,A5] |- PS5[P'1,A5]   [UnfR]
            (~[]F -> PS1[A5,P'1]), [](~[]F -> PS1[A5,P'1]), []PS5[P'1,A5] |- [](~[]F -> PS1[A5,P'1])   [Ax]
```


### C3 = `if(BOX(S3),S3,S1)` vs S5 = `S5`: plays (S1, S5); evaluator (S1, S5)

- C3's atom BOX(THEM=S3): not provable

### X = `if(BOX(S1),S1,S4)` vs X = `if(BOX(S1),S1,S4)`: plays (S1, S1); evaluator (S1, S1)

- X's atom BOX(THEM=S1): **provable**, 4 sequents, 1 Löb step(s)

```
 |- PS1[X,X]   [UnfR]
   |- []PS1[X,X]   [GLR]
    []PS1[X,X] |- PS1[X,X]   [UnfR]
      []PS1[X,X] |- []PS1[X,X]   [Ax]
```

- X's atom BOX(THEM=S1): **provable**, 4 sequents, 1 Löb step(s)

```
 |- PS1[X,X]   [UnfR]
   |- []PS1[X,X]   [GLR]
    []PS1[X,X] |- PS1[X,X]   [UnfR]
      []PS1[X,X] |- []PS1[X,X]   [Ax]
```


### X = `if(BOX(S1),S1,S4)` vs Z = `if(BOX1(S3),S3,S2)`: plays (S4, S2); evaluator (S4, S2)

- X's atom BOX(THEM=S1): not provable
- Z's atom BOX1(THEM=S3): not provable

### X = `if(BOX(S1),S1,S4)` vs V = `if(BOX1(S4),S2,S4)`: plays (S4, S2); evaluator (S4, S2)

- X's atom BOX(THEM=S1): not provable
- V's atom BOX1(THEM=S4): **provable**, 7 sequents, 1 Löb step(s)

```
 |- (~[]F -> PS4[X,V])   [->R]
  ~[]F |- PS4[X,V]   [~L]
     |- PS4[X,V], []F   [UnfR]
       |- []F, ~[]PS1[V,X]   [~R]
        []PS1[V,X] |- []F   [GLR]
          PS1[V,X], []F, []PS1[V,X] |- F   [UnfL]
            F, []F, []PS1[V,X] |- F   [Ax]
```


### Z = `if(BOX1(S3),S3,S2)` vs Z = `if(BOX1(S3),S3,S2)`: plays (S3, S3); evaluator (S3, S3)

- Z's atom BOX1(THEM=S3): **provable**, 6 sequents, 1 Löb step(s)

```
 |- (~[]F -> PS3[Z,Z])   [->R]
   |- PS3[Z,Z]   [UnfR]
     |- [](~[]F -> PS3[Z,Z])   [GLR]
      [](~[]F -> PS3[Z,Z]) |- (~[]F -> PS3[Z,Z])   [->R]
        [](~[]F -> PS3[Z,Z]) |- PS3[Z,Z]   [UnfR]
          [](~[]F -> PS3[Z,Z]) |- [](~[]F -> PS3[Z,Z])   [Ax]
```

- Z's atom BOX1(THEM=S3): **provable**, 6 sequents, 1 Löb step(s)

```
 |- (~[]F -> PS3[Z,Z])   [->R]
   |- PS3[Z,Z]   [UnfR]
     |- [](~[]F -> PS3[Z,Z])   [GLR]
      [](~[]F -> PS3[Z,Z]) |- (~[]F -> PS3[Z,Z])   [->R]
        [](~[]F -> PS3[Z,Z]) |- PS3[Z,Z]   [UnfR]
          [](~[]F -> PS3[Z,Z]) |- [](~[]F -> PS3[Z,Z])   [Ax]
```


### Z = `if(BOX1(S3),S3,S2)` vs V = `if(BOX1(S4),S2,S4)`: plays (S2, S4); evaluator (S2, S4)

- Z's atom BOX1(THEM=S3): not provable
- V's atom BOX1(THEM=S4): not provable

### V = `if(BOX1(S4),S2,S4)` vs V = `if(BOX1(S4),S2,S4)`: plays (S4, S4); evaluator (S4, S4)

- V's atom BOX1(THEM=S4): not provable
- V's atom BOX1(THEM=S4): not provable

### Z = `if(BOX1(S3),S3,S2)` vs S3 = `S3`: plays (S3, S3); evaluator (S3, S3)

- Z's atom BOX1(THEM=S3): **provable**, 3 sequents, 0 Löb step(s)

```
 |- (~[]F -> PS3[S3,Z])   [->R]
   |- PS3[S3,Z]   [UnfR]
     |- T   [Ax]
```


### X = `if(BOX(S1),S1,S4)` vs S4 = `S4`: plays (S4, S4); evaluator (S4, S4)

- X's atom BOX(THEM=S1): not provable

