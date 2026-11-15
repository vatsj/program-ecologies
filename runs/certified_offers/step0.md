# Queue 79 step 0: exact invasion assays (rho * N, N = 200, w = 0.3, A_f charges; 1 = neutral; C1 tables)

Residents: item 1 (simulating-bully unequal) 522, item 2 (Rc / Rcs matched victim) 444; item 4 (Bc unequal) [372, 414]; item 3 fair carrier islands {'Rc,Oc': 354, 'Fc,Fc': 90624, 'Rcs,half': 354, 'Fc,Bc': 11328}; item 3b fair reader islands {'FI': 1728, 'FC': 2385}
Checks: jump chain (10^4 trials, 60 non-neutral assays) max |z| 2.63; kernel (16 assays, 3,000 islands) max |z| 2.17

Rate = rho x the invader's arrival mass under the main law (FcOcRc, delta 0.03, beta 3, phi 1/2).

| group | n | median | min | max | share <= 1 | share > 3 | mean rate per arrival | outcome if fixed |
|---|---|---|---|---|---|---|---|---|
| item1|accepter into v, offerer resident|Rcs|matched|Bc|carrier-active | 12 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 12} |
| item1|accepter into v, offerer resident|Rcs|matched|C1|const-other | 3 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 3} |
| item1|accepter into v, offerer resident|Rcs|matched|C1|half-naming-v | 3 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 3} |
| item1|accepter into v, offerer resident|Rcs|matched|C4|const-other | 3 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 3} |
| item1|accepter into v, offerer resident|Rcs|matched|C4|half-naming-v | 3 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 3} |
| item1|accepter into v, offerer resident|Rcs|matched|Fc|carrier-active | 96 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 96} |
| item1|accepter into v, offerer resident|Rcs|matched|Fs|sim-reader | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item1|accepter into v, offerer resident|Rcs|matched|Ft|sim-reader | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item1|accepter into v, offerer resident|Rcs|matched|Oc|carrier-active | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 6} |
| item1|accepter into v, offerer resident|Rcs|matched|Oc|carrier-inactive | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item1|accepter into v, offerer resident|Rcs|matched|Pc|carrier-active | 24 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 24} |
| item1|accepter into v, offerer resident|Rcs|mismatched|Bc|carrier-active | 12 | 0.007568 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'F': 6, 'W': 6} |
| item1|accepter into v, offerer resident|Rcs|mismatched|C1|const-other | 3 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'F': 3} |
| item1|accepter into v, offerer resident|Rcs|mismatched|C1|half-naming-v | 3 | 0.01514 | 0.0151 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 3} |
| item1|accepter into v, offerer resident|Rcs|mismatched|C4|const-other | 3 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'F': 3} |
| item1|accepter into v, offerer resident|Rcs|mismatched|C4|half-naming-v | 3 | 0.01514 | 0.0151 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 3} |
| item1|accepter into v, offerer resident|Rcs|mismatched|Fc|carrier-active | 96 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 36, 'F': 36, 'D': 24} |
| item1|accepter into v, offerer resident|Rcs|mismatched|Fs|sim-reader | 48 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 18, 'F': 18, 'D': 12} |
| item1|accepter into v, offerer resident|Rcs|mismatched|Ft|sim-reader | 48 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 18, 'D': 12, 'F': 18} |
| item1|accepter into v, offerer resident|Rcs|mismatched|Oc|carrier-active | 6 | 0.01514 | 0.0151 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 6} |
| item1|accepter into v, offerer resident|Rcs|mismatched|Oc|carrier-inactive | 6 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'F': 6} |
| item1|accepter into v, offerer resident|Rcs|mismatched|Pc|carrier-active | 24 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 6, 'D': 18} |
| item1|accepter into v, offerer resident|Rc|matched|Bc|carrier-active | 12 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 12} |
| item1|accepter into v, offerer resident|Rc|matched|C1|const-other | 3 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 3} |
| item1|accepter into v, offerer resident|Rc|matched|C1|half-naming-v | 3 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 3} |
| item1|accepter into v, offerer resident|Rc|matched|C4|const-other | 3 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 3} |
| item1|accepter into v, offerer resident|Rc|matched|C4|half-naming-v | 3 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 3} |
| item1|accepter into v, offerer resident|Rc|matched|Fc|carrier-active | 96 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 96} |
| item1|accepter into v, offerer resident|Rc|matched|Fs|sim-reader | 48 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 48} |
| item1|accepter into v, offerer resident|Rc|matched|Ft|sim-reader | 48 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 48} |
| item1|accepter into v, offerer resident|Rc|matched|Oc|carrier-active | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 6} |
| item1|accepter into v, offerer resident|Rc|matched|Oc|carrier-inactive | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item1|accepter into v, offerer resident|Rc|matched|Pc|carrier-active | 24 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 24} |
| item1|accepter into v, offerer resident|Rc|mismatched|Bc|carrier-active | 12 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6, 'W': 6} |
| item1|accepter into v, offerer resident|Rc|mismatched|C1|const-other | 3 | 4.335e-08 | 4.34e-08 | 4.34e-08 | 1.00 | 0.00 | 3.25e-12 | {'F': 3} |
| item1|accepter into v, offerer resident|Rc|mismatched|C1|half-naming-v | 3 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'W': 3} |
| item1|accepter into v, offerer resident|Rc|mismatched|C4|const-other | 3 | 4.335e-08 | 4.34e-08 | 4.34e-08 | 1.00 | 0.00 | 3.25e-12 | {'F': 3} |
| item1|accepter into v, offerer resident|Rc|mismatched|C4|half-naming-v | 3 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'W': 3} |
| item1|accepter into v, offerer resident|Rc|mismatched|Fc|carrier-active | 96 | 4.335e-08 | 4.34e-08 | 4.34e-08 | 1.00 | 0.00 | 3.25e-12 | {'F': 84, 'D': 12} |
| item1|accepter into v, offerer resident|Rc|mismatched|Fs|sim-reader | 48 | 4.335e-08 | 4.34e-08 | 4.34e-08 | 1.00 | 0.00 | 3.25e-12 | {'F': 36, 'D': 12} |
| item1|accepter into v, offerer resident|Rc|mismatched|Ft|sim-reader | 48 | 4.335e-08 | 4.34e-08 | 4.34e-08 | 1.00 | 0.00 | 3.25e-12 | {'F': 48} |
| item1|accepter into v, offerer resident|Rc|mismatched|Oc|carrier-active | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'W': 6} |
| item1|accepter into v, offerer resident|Rc|mismatched|Oc|carrier-inactive | 6 | 4.335e-08 | 4.34e-08 | 4.34e-08 | 1.00 | 0.00 | 3.25e-12 | {'F': 6} |
| item1|accepter into v, offerer resident|Rc|mismatched|Pc|carrier-active | 24 | 4.335e-08 | 4.34e-08 | 4.34e-08 | 1.00 | 0.00 | 3.25e-12 | {'D': 24} |
| item1|accepter into v, offerer resident|R|matched|Bc|carrier-active | 12 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'F': 6, 'D': 6} |
| item1|accepter into v, offerer resident|R|matched|C1|const-other | 3 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 3} |
| item1|accepter into v, offerer resident|R|matched|C1|half-naming-v | 3 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 3} |
| item1|accepter into v, offerer resident|R|matched|C4|const-other | 3 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 3} |
| item1|accepter into v, offerer resident|R|matched|C4|half-naming-v | 3 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 3} |
| item1|accepter into v, offerer resident|R|matched|Fc|carrier-active | 96 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 60, 'F': 36} |
| item1|accepter into v, offerer resident|R|matched|Fs|sim-reader | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item1|accepter into v, offerer resident|R|matched|Ft|sim-reader | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item1|accepter into v, offerer resident|R|matched|Oc|carrier-active | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 6} |
| item1|accepter into v, offerer resident|R|matched|Oc|carrier-inactive | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item1|accepter into v, offerer resident|R|matched|Pc|carrier-active | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 24} |
| item1|accepter into v, offerer resident|R|mismatched|Bc|carrier-active | 12 | 0.007568 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'F': 6, 'W': 6} |
| item1|accepter into v, offerer resident|R|mismatched|C1|const-other | 3 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'F': 3} |
| item1|accepter into v, offerer resident|R|mismatched|C1|half-naming-v | 3 | 0.01514 | 0.0151 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 3} |
| item1|accepter into v, offerer resident|R|mismatched|C4|const-other | 3 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'F': 3} |
| item1|accepter into v, offerer resident|R|mismatched|C4|half-naming-v | 3 | 0.01514 | 0.0151 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 3} |
| item1|accepter into v, offerer resident|R|mismatched|Fc|carrier-active | 96 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 36, 'F': 36, 'D': 24} |
| item1|accepter into v, offerer resident|R|mismatched|Fs|sim-reader | 48 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 18, 'F': 18, 'D': 12} |
| item1|accepter into v, offerer resident|R|mismatched|Ft|sim-reader | 48 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 18, 'D': 12, 'F': 18} |
| item1|accepter into v, offerer resident|R|mismatched|Oc|carrier-active | 6 | 0.01514 | 0.0151 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 6} |
| item1|accepter into v, offerer resident|R|mismatched|Oc|carrier-inactive | 6 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'F': 6} |
| item1|accepter into v, offerer resident|R|mismatched|Pc|carrier-active | 24 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 6, 'D': 18} |
| item1|accepter into v|Rcs|matched|e=carrier-active | 150 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 150} |
| item1|accepter into v|Rcs|matched|e=carrier-inactive | 18 | 1 | 1.42e-10 | 1 | 1.00 | 0.00 | 0 | {'U': 12, 'D': 6} |
| item1|accepter into v|Rcs|matched|e=const-other | 48 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 48} |
| item1|accepter into v|Rcs|matched|e=half-naming-v | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 6} |
| item1|accepter into v|Rcs|matched|e=other | 12 | 0.5076 | 0.0151 | 1 | 1.00 | 0.00 | 0 | {'U': 12} |
| item1|accepter into v|Rcs|matched|e=sim-reader | 288 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 198, 'F': 84, 'W': 6} |
| item1|accepter into v|Rcs|mismatched|e=carrier-active | 150 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 66, 'F': 42, 'D': 42} |
| item1|accepter into v|Rcs|mismatched|e=carrier-inactive | 18 | 0.01514 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'F': 6, 'W': 12} |
| item1|accepter into v|Rcs|mismatched|e=const-other | 48 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 12, 'U': 6, 'F': 6, 'D': 24} |
| item1|accepter into v|Rcs|mismatched|e=half-naming-v | 6 | 0.01514 | 0.0151 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 6} |
| item1|accepter into v|Rcs|mismatched|e=other | 12 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 12} |
| item1|accepter into v|Rcs|mismatched|e=sim-reader | 288 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 114, 'F': 78, 'D': 96} |
| item1|accepter into v|Rc|matched|e=carrier-active | 150 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 150} |
| item1|accepter into v|Rc|matched|e=carrier-inactive | 18 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 18} |
| item1|accepter into v|Rc|matched|e=const-other | 48 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 48} |
| item1|accepter into v|Rc|matched|e=half-naming-v | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item1|accepter into v|Rc|matched|e=other | 12 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 12} |
| item1|accepter into v|Rc|matched|e=sim-reader | 288 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 288} |
| item1|accepter into v|Rc|mismatched|e=carrier-active | 150 | 4.335e-08 | 4.34e-08 | 1 | 1.00 | 0.00 | 9e-06 | {'W': 24, 'F': 84, 'D': 36, 'U': 6} |
| item1|accepter into v|Rc|mismatched|e=carrier-inactive | 18 | 4.335e-08 | 4.34e-08 | 1 | 1.00 | 0.00 | 2.5e-05 | {'F': 12, 'W': 6} |
| item1|accepter into v|Rc|mismatched|e=const-other | 48 | 4.335e-08 | 4.34e-08 | 1 | 1.00 | 0.00 | 1.88e-05 | {'W': 12, 'U': 6, 'F': 6, 'D': 24} |
| item1|accepter into v|Rc|mismatched|e=half-naming-v | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'W': 6} |
| item1|accepter into v|Rc|mismatched|e=other | 12 | 4.335e-08 | 4.34e-08 | 4.34e-08 | 1.00 | 0.00 | 3.25e-12 | {'D': 12} |
| item1|accepter into v|Rc|mismatched|e=sim-reader | 288 | 4.335e-08 | 4.34e-08 | 1 | 1.00 | 0.00 | 7.81e-06 | {'F': 174, 'D': 72, 'U': 12, 'W': 30} |
| item1|accepter into v|R|matched|e=carrier-active | 150 | 1.419e-10 | 1.42e-10 | 9.75 | 0.96 | 0.04 | 0 | {'F': 48, 'D': 90, 'U': 6, 'W': 6} |
| item1|accepter into v|R|matched|e=carrier-inactive | 18 | 1 | 1.42e-10 | 1 | 1.00 | 0.00 | 0 | {'U': 12, 'D': 6} |
| item1|accepter into v|R|matched|e=const-other | 48 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 48} |
| item1|accepter into v|R|matched|e=half-naming-v | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 6} |
| item1|accepter into v|R|matched|e=other | 12 | 0.5076 | 0.0151 | 1 | 1.00 | 0.00 | 0 | {'U': 12} |
| item1|accepter into v|R|matched|e=sim-reader | 288 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 198, 'F': 84, 'W': 6} |
| item1|accepter into v|R|mismatched|e=carrier-active | 150 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 66, 'F': 42, 'D': 42} |
| item1|accepter into v|R|mismatched|e=carrier-inactive | 18 | 0.01514 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'F': 6, 'W': 12} |
| item1|accepter into v|R|mismatched|e=const-other | 48 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 12, 'U': 6, 'F': 6, 'D': 24} |
| item1|accepter into v|R|mismatched|e=half-naming-v | 6 | 0.01514 | 0.0151 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 6} |
| item1|accepter into v|R|mismatched|e=other | 12 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 12} |
| item1|accepter into v|R|mismatched|e=sim-reader | 288 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 114, 'F': 78, 'D': 96} |
| item1|into e, Rc resident|Bc|carrier-active | 744 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.00315 | {'F': 744} |
| item1|into e, Rc resident|B|sim-reader | 732 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000131 | {'U': 732} |
| item1|into e, Rc resident|C0|const-other | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 366} |
| item1|into e, Rc resident|C1|const-other | 183 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 183} |
| item1|into e, Rc resident|C1|half-naming-v | 183 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 183} |
| item1|into e, Rc resident|C2|const-other | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 366} |
| item1|into e, Rc resident|C3|const-other | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 366} |
| item1|into e, Rc resident|C4|const-other | 183 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 183} |
| item1|into e, Rc resident|C4|half-naming-v | 183 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 183} |
| item1|into e, Rc resident|C5|const-other | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 366} |
| item1|into e, Rc resident|C6|const-other | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 366} |
| item1|into e, Rc resident|C7|const-other | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 366} |
| item1|into e, Rc resident|C8|const-other | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 366} |
| item1|into e, Rc resident|F2|sim-reader | 1464 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 1464} |
| item1|into e, Rc resident|Fc|carrier-active | 5952 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.000131 | {'F': 5952} |
| item1|into e, Rc resident|Fs|sim-reader | 2928 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 2928} |
| item1|into e, Rc resident|Ft|sim-reader | 2928 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 2928} |
| item1|into e, Rc resident|J|other | 732 | 0.01514 | 0.0151 | 1 | 1.00 | 0.00 | 0 | {'U': 732} |
| item1|into e, Rc resident|Oc|carrier-active | 372 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.00105 | {'F': 372} |
| item1|into e, Rc resident|Oc|carrier-inactive | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 4.36e-05 | {'U': 366} |
| item1|into e, Rc resident|O|sim-reader | 2928 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 2928} |
| item1|into e, Rc resident|Pc|carrier-active | 1488 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0 | {'F': 1488} |
| item1|into e, Rc resident|Po|sim-reader | 1464 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 1464} |
| item1|into e, Rc resident|Pz|sim-reader | 1464 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 1464} |
| item1|into e, Rc resident|Q|sim-reader | 1464 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 1464} |
| item1|into e, Rc resident|Rcs|carrier-active | 372 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0 | {'F': 372} |
| item1|into e, Rc resident|Rcs|carrier-inactive | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 366} |
| item1|into e, Rc resident|Rc|carrier-active | 372 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.0021 | {'F': 372} |
| item1|into e, Rc resident|Rc|carrier-inactive | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 8.71e-05 | {'U': 366} |
| item1|into e, Rc resident|R|sim-reader | 1464 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 1464} |
| item1|into e, Rc resident|X|sim-reader | 732 | 1 | 1 | 5.93 | 0.97 | 0.03 | 9.68e-06 | {'U': 732} |
| item1|into e, Rcs resident|Bc|carrier-active | 144 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.00323 | {'F': 144} |
| item1|into e, Rcs resident|B|sim-reader | 144 | 11.81 | 0.0151 | 27.9 | 0.50 | 0.50 | 0.00133 | {'F': 72, 'D': 72} |
| item1|into e, Rcs resident|C0|const-other | 66 | 1 | 1 | 5.93 | 0.82 | 0.18 | 0.000892 | {'U': 66} |
| item1|into e, Rcs resident|C1|const-other | 33 | 1 | 1 | 5.93 | 0.82 | 0.18 | 0.000892 | {'U': 33} |
| item1|into e, Rcs resident|C1|half-naming-v | 36 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.0135 | {'F': 36} |
| item1|into e, Rcs resident|C2|const-other | 66 | 1 | 1 | 5.93 | 0.82 | 0.18 | 0.000892 | {'U': 66} |
| item1|into e, Rcs resident|C3|const-other | 66 | 1 | 1 | 5.93 | 0.82 | 0.18 | 0.000892 | {'U': 66} |
| item1|into e, Rcs resident|C4|const-other | 33 | 1 | 1 | 5.93 | 0.82 | 0.18 | 0.000892 | {'U': 33} |
| item1|into e, Rcs resident|C4|half-naming-v | 36 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.0135 | {'F': 36} |
| item1|into e, Rcs resident|C5|const-other | 66 | 1 | 1 | 5.93 | 0.82 | 0.18 | 0.000892 | {'U': 66} |
| item1|into e, Rcs resident|C6|const-other | 66 | 1 | 1 | 5.93 | 0.82 | 0.18 | 0.000892 | {'U': 66} |
| item1|into e, Rcs resident|C7|const-other | 66 | 1 | 1 | 5.93 | 0.82 | 0.18 | 0.000892 | {'U': 66} |
| item1|into e, Rcs resident|C8|const-other | 66 | 1 | 1 | 5.93 | 0.82 | 0.18 | 0.000892 | {'U': 66} |
| item1|into e, Rcs resident|F2|sim-reader | 288 | 0.01514 | 7.6e-05 | 27.9 | 0.75 | 0.25 | 0 | {'D': 216, 'F': 72} |
| item1|into e, Rcs resident|Fc|carrier-active | 1152 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.000135 | {'F': 1152} |
| item1|into e, Rcs resident|Fs|sim-reader | 576 | 0.01514 | 0.0151 | 27.9 | 0.62 | 0.38 | 0 | {'D': 360, 'F': 216} |
| item1|into e, Rcs resident|Ft|sim-reader | 576 | 0.01514 | 7.6e-05 | 27.9 | 0.62 | 0.38 | 0 | {'D': 360, 'F': 216} |
| item1|into e, Rcs resident|J|other | 132 | 0.01514 | 0.0151 | 1 | 1.00 | 0.00 | 0 | {'U': 132} |
| item1|into e, Rcs resident|Oc|carrier-active | 72 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.00108 | {'F': 72} |
| item1|into e, Rcs resident|Oc|carrier-inactive | 66 | 1 | 1 | 5.93 | 0.82 | 0.18 | 7.11e-05 | {'U': 66} |
| item1|into e, Rcs resident|O|sim-reader | 576 | 7.599e-05 | 7.6e-05 | 22.6 | 0.62 | 0.38 | 0 | {'D': 360, 'F': 216} |
| item1|into e, Rcs resident|Pc|carrier-active | 288 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0 | {'F': 288} |
| item1|into e, Rcs resident|Po|sim-reader | 288 | 9.107 | 0.0151 | 27.9 | 0.50 | 0.50 | 0 | {'F': 144, 'D': 144} |
| item1|into e, Rcs resident|Pz|sim-reader | 288 | 0.01514 | 7.6e-05 | 1 | 1.00 | 0.00 | 0 | {'D': 288} |
| item1|into e, Rcs resident|Q|sim-reader | 288 | 0.01514 | 7.6e-05 | 1 | 1.00 | 0.00 | 0 | {'D': 288} |
| item1|into e, Rcs resident|Rcs|carrier-active | 72 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0 | {'F': 72} |
| item1|into e, Rcs resident|Rcs|carrier-inactive | 72 | 0.01514 | 0.0151 | 1 | 1.00 | 0.00 | 0 | {'D': 72} |
| item1|into e, Rcs resident|Rc|carrier-active | 72 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.00215 | {'F': 72} |
| item1|into e, Rcs resident|Rc|carrier-inactive | 66 | 1 | 1 | 5.93 | 0.82 | 0.18 | 0.000142 | {'U': 66} |
| item1|into e, Rcs resident|R|sim-reader | 288 | 7.261 | 0.0151 | 27.9 | 0.50 | 0.50 | 0 | {'W': 72, 'D': 144, 'F': 72} |
| item1|into e, Rcs resident|X|sim-reader | 144 | 0.01514 | 0.0151 | 1 | 1.00 | 0.00 | 1.49e-06 | {'D': 144} |
| item1|accepter into v (matched)|Rcs|e class B | 12 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'F': 6, 'D': 6} |
| item1|accepter into v (matched)|Rcs|e class Bc | 12 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 12} |
| item1|accepter into v (matched)|Rcs|e class C0 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item1|accepter into v (matched)|Rcs|e class C1 | 6 | 5.377 | 1 | 9.75 | 0.50 | 0.50 | 0 | {'F': 3, 'U': 3} |
| item1|accepter into v (matched)|Rcs|e class C2 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item1|accepter into v (matched)|Rcs|e class C3 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item1|accepter into v (matched)|Rcs|e class C4 | 6 | 5.377 | 1 | 9.75 | 0.50 | 0.50 | 0 | {'U': 3, 'F': 3} |
| item1|accepter into v (matched)|Rcs|e class C5 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item1|accepter into v (matched)|Rcs|e class C6 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item1|accepter into v (matched)|Rcs|e class C7 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item1|accepter into v (matched)|Rcs|e class C8 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item1|accepter into v (matched)|Rcs|e class F2 | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 18, 'F': 6} |
| item1|accepter into v (matched)|Rcs|e class Fc | 96 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 96} |
| item1|accepter into v (matched)|Rcs|e class Fs | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item1|accepter into v (matched)|Rcs|e class Ft | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item1|accepter into v (matched)|Rcs|e class J | 12 | 0.5076 | 0.0151 | 1 | 1.00 | 0.00 | 0 | {'U': 12} |
| item1|accepter into v (matched)|Rcs|e class O | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item1|accepter into v (matched)|Rcs|e class Oc | 12 | 5.377 | 1 | 9.75 | 0.50 | 0.50 | 0 | {'F': 6, 'U': 6} |
| item1|accepter into v (matched)|Rcs|e class Pc | 24 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 24} |
| item1|accepter into v (matched)|Rcs|e class Po | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'F': 12, 'D': 12} |
| item1|accepter into v (matched)|Rcs|e class Pz | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 24} |
| item1|accepter into v (matched)|Rcs|e class Q | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 24} |
| item1|accepter into v (matched)|Rcs|e class R | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'W': 6, 'D': 12, 'F': 6} |
| item1|accepter into v (matched)|Rcs|e class Rc | 12 | 5.377 | 1 | 9.75 | 0.50 | 0.50 | 0 | {'F': 6, 'U': 6} |
| item1|accepter into v (matched)|Rcs|e class Rcs | 12 | 4.877 | 1.42e-10 | 9.75 | 0.50 | 0.50 | 0 | {'F': 6, 'D': 6} |
| item1|accepter into v (matched)|Rcs|e class X | 12 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 12} |
| item1|accepter into v (matched)|Rc|e class B | 12 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 12} |
| item1|accepter into v (matched)|Rc|e class Bc | 12 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 12} |
| item1|accepter into v (matched)|Rc|e class C0 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item1|accepter into v (matched)|Rc|e class C1 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item1|accepter into v (matched)|Rc|e class C2 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item1|accepter into v (matched)|Rc|e class C3 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item1|accepter into v (matched)|Rc|e class C4 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item1|accepter into v (matched)|Rc|e class C5 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item1|accepter into v (matched)|Rc|e class C6 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item1|accepter into v (matched)|Rc|e class C7 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item1|accepter into v (matched)|Rc|e class C8 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item1|accepter into v (matched)|Rc|e class F2 | 24 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 24} |
| item1|accepter into v (matched)|Rc|e class Fc | 96 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 96} |
| item1|accepter into v (matched)|Rc|e class Fs | 48 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 48} |
| item1|accepter into v (matched)|Rc|e class Ft | 48 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 48} |
| item1|accepter into v (matched)|Rc|e class J | 12 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 12} |
| item1|accepter into v (matched)|Rc|e class O | 48 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 48} |
| item1|accepter into v (matched)|Rc|e class Oc | 12 | 5.377 | 1 | 9.75 | 0.50 | 0.50 | 0.000403 | {'F': 6, 'U': 6} |
| item1|accepter into v (matched)|Rc|e class Pc | 24 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 24} |
| item1|accepter into v (matched)|Rc|e class Po | 24 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 24} |
| item1|accepter into v (matched)|Rc|e class Pz | 24 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 24} |
| item1|accepter into v (matched)|Rc|e class Q | 24 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 24} |
| item1|accepter into v (matched)|Rc|e class R | 24 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 24} |
| item1|accepter into v (matched)|Rc|e class Rc | 12 | 5.377 | 1 | 9.75 | 0.50 | 0.50 | 0.000403 | {'F': 6, 'U': 6} |
| item1|accepter into v (matched)|Rc|e class Rcs | 12 | 5.377 | 1 | 9.75 | 0.50 | 0.50 | 0.000403 | {'F': 6, 'U': 6} |
| item1|accepter into v (matched)|Rc|e class X | 12 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 12} |
| item1|accepter into v (matched)|R|e class B | 12 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'F': 6, 'D': 6} |
| item1|accepter into v (matched)|R|e class Bc | 12 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'F': 6, 'D': 6} |
| item1|accepter into v (matched)|R|e class C0 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item1|accepter into v (matched)|R|e class C1 | 6 | 5.377 | 1 | 9.75 | 0.50 | 0.50 | 0 | {'F': 3, 'U': 3} |
| item1|accepter into v (matched)|R|e class C2 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item1|accepter into v (matched)|R|e class C3 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item1|accepter into v (matched)|R|e class C4 | 6 | 5.377 | 1 | 9.75 | 0.50 | 0.50 | 0 | {'U': 3, 'F': 3} |
| item1|accepter into v (matched)|R|e class C5 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item1|accepter into v (matched)|R|e class C6 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item1|accepter into v (matched)|R|e class C7 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item1|accepter into v (matched)|R|e class C8 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item1|accepter into v (matched)|R|e class F2 | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 18, 'F': 6} |
| item1|accepter into v (matched)|R|e class Fc | 96 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 60, 'F': 36} |
| item1|accepter into v (matched)|R|e class Fs | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item1|accepter into v (matched)|R|e class Ft | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item1|accepter into v (matched)|R|e class J | 12 | 0.5076 | 0.0151 | 1 | 1.00 | 0.00 | 0 | {'U': 12} |
| item1|accepter into v (matched)|R|e class O | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item1|accepter into v (matched)|R|e class Oc | 12 | 5.377 | 1 | 9.75 | 0.50 | 0.50 | 0 | {'F': 6, 'U': 6} |
| item1|accepter into v (matched)|R|e class Pc | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 24} |
| item1|accepter into v (matched)|R|e class Po | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'F': 12, 'D': 12} |
| item1|accepter into v (matched)|R|e class Pz | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 24} |
| item1|accepter into v (matched)|R|e class Q | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 24} |
| item1|accepter into v (matched)|R|e class R | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'W': 6, 'D': 12, 'F': 6} |
| item1|accepter into v (matched)|R|e class Rc | 12 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 12} |
| item1|accepter into v (matched)|R|e class Rcs | 12 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'W': 6, 'D': 6} |
| item1|accepter into v (matched)|R|e class X | 12 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 12} |
| item4|accepter into v, offerer resident|Rcs|matched|C1|const-other | 3 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 3} |
| item4|accepter into v, offerer resident|Rcs|matched|C1|half-naming-v | 3 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 3} |
| item4|accepter into v, offerer resident|Rcs|matched|C4|const-other | 3 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 3} |
| item4|accepter into v, offerer resident|Rcs|matched|C4|half-naming-v | 3 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 3} |
| item4|accepter into v, offerer resident|Rcs|matched|Fs|sim-reader | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item4|accepter into v, offerer resident|Rcs|matched|Ft|sim-reader | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item4|accepter into v, offerer resident|Rcs|matched|Oc|carrier-active | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 6} |
| item4|accepter into v, offerer resident|Rcs|mismatched|C1|const-other | 3 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 3} |
| item4|accepter into v, offerer resident|Rcs|mismatched|C1|half-naming-v | 3 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 3} |
| item4|accepter into v, offerer resident|Rcs|mismatched|C4|const-other | 3 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 3} |
| item4|accepter into v, offerer resident|Rcs|mismatched|C4|half-naming-v | 3 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 3} |
| item4|accepter into v, offerer resident|Rcs|mismatched|Fs|sim-reader | 48 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 48} |
| item4|accepter into v, offerer resident|Rcs|mismatched|Ft|sim-reader | 48 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 48} |
| item4|accepter into v, offerer resident|Rcs|mismatched|Oc|carrier-active | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 6} |
| item4|accepter into v, offerer resident|Rc|matched|C1|const-other | 3 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 3} |
| item4|accepter into v, offerer resident|Rc|matched|C1|half-naming-v | 3 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 3} |
| item4|accepter into v, offerer resident|Rc|matched|C4|const-other | 3 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 3} |
| item4|accepter into v, offerer resident|Rc|matched|C4|half-naming-v | 3 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 3} |
| item4|accepter into v, offerer resident|Rc|matched|Fs|sim-reader | 48 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 48} |
| item4|accepter into v, offerer resident|Rc|matched|Ft|sim-reader | 48 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 48} |
| item4|accepter into v, offerer resident|Rc|matched|Oc|carrier-active | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 6} |
| item4|accepter into v, offerer resident|Rc|mismatched|C1|const-other | 3 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 3} |
| item4|accepter into v, offerer resident|Rc|mismatched|C1|half-naming-v | 3 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 3} |
| item4|accepter into v, offerer resident|Rc|mismatched|C4|const-other | 3 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 3} |
| item4|accepter into v, offerer resident|Rc|mismatched|C4|half-naming-v | 3 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 3} |
| item4|accepter into v, offerer resident|Rc|mismatched|Fs|sim-reader | 48 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 48} |
| item4|accepter into v, offerer resident|Rc|mismatched|Ft|sim-reader | 48 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 48} |
| item4|accepter into v, offerer resident|Rc|mismatched|Oc|carrier-active | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 6} |
| item4|accepter into v, offerer resident|R|matched|C1|const-other | 3 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 3} |
| item4|accepter into v, offerer resident|R|matched|C1|half-naming-v | 3 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 3} |
| item4|accepter into v, offerer resident|R|matched|C4|const-other | 3 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 3} |
| item4|accepter into v, offerer resident|R|matched|C4|half-naming-v | 3 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 3} |
| item4|accepter into v, offerer resident|R|matched|Fs|sim-reader | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item4|accepter into v, offerer resident|R|matched|Ft|sim-reader | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item4|accepter into v, offerer resident|R|matched|Oc|carrier-active | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 6} |
| item4|accepter into v, offerer resident|R|mismatched|C1|const-other | 3 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'F': 3} |
| item4|accepter into v, offerer resident|R|mismatched|C1|half-naming-v | 3 | 0.01514 | 0.0151 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 3} |
| item4|accepter into v, offerer resident|R|mismatched|C4|const-other | 3 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'F': 3} |
| item4|accepter into v, offerer resident|R|mismatched|C4|half-naming-v | 3 | 0.01514 | 0.0151 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 3} |
| item4|accepter into v, offerer resident|R|mismatched|Fs|sim-reader | 48 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 18, 'F': 18, 'D': 12} |
| item4|accepter into v, offerer resident|R|mismatched|Ft|sim-reader | 48 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 18, 'D': 12, 'F': 18} |
| item4|accepter into v, offerer resident|R|mismatched|Oc|carrier-active | 6 | 0.01514 | 0.0151 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 6} |
| item4|accepter into v|Rcs|matched|e=carrier-active | 18 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 18} |
| item4|accepter into v|Rcs|matched|e=const-other | 48 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 48} |
| item4|accepter into v|Rcs|matched|e=half-naming-v | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 6} |
| item4|accepter into v|Rcs|matched|e=other | 12 | 0.5076 | 0.0151 | 1 | 1.00 | 0.00 | 0 | {'U': 12} |
| item4|accepter into v|Rcs|matched|e=sim-reader | 288 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 198, 'F': 84, 'W': 6} |
| item4|accepter into v|Rcs|mismatched|e=carrier-active | 18 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 18} |
| item4|accepter into v|Rcs|mismatched|e=const-other | 48 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 48} |
| item4|accepter into v|Rcs|mismatched|e=half-naming-v | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 6} |
| item4|accepter into v|Rcs|mismatched|e=other | 12 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 12} |
| item4|accepter into v|Rcs|mismatched|e=sim-reader | 288 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 288} |
| item4|accepter into v|Rc|matched|e=carrier-active | 18 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 18} |
| item4|accepter into v|Rc|matched|e=const-other | 48 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 48} |
| item4|accepter into v|Rc|matched|e=half-naming-v | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item4|accepter into v|Rc|matched|e=other | 12 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 12} |
| item4|accepter into v|Rc|matched|e=sim-reader | 288 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 288} |
| item4|accepter into v|Rc|mismatched|e=carrier-active | 18 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 18} |
| item4|accepter into v|Rc|mismatched|e=const-other | 48 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 48} |
| item4|accepter into v|Rc|mismatched|e=half-naming-v | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 6} |
| item4|accepter into v|Rc|mismatched|e=other | 12 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 12} |
| item4|accepter into v|Rc|mismatched|e=sim-reader | 288 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 288} |
| item4|accepter into v|R|matched|e=carrier-active | 18 | 1 | 1.42e-10 | 9.75 | 0.67 | 0.33 | 0 | {'F': 6, 'U': 6, 'W': 6} |
| item4|accepter into v|R|matched|e=const-other | 48 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 48} |
| item4|accepter into v|R|matched|e=half-naming-v | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 6} |
| item4|accepter into v|R|matched|e=other | 12 | 0.5076 | 0.0151 | 1 | 1.00 | 0.00 | 0 | {'U': 12} |
| item4|accepter into v|R|matched|e=sim-reader | 288 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 198, 'F': 84, 'W': 6} |
| item4|accepter into v|R|mismatched|e=carrier-active | 18 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 18} |
| item4|accepter into v|R|mismatched|e=const-other | 48 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 12, 'U': 6, 'F': 6, 'D': 24} |
| item4|accepter into v|R|mismatched|e=half-naming-v | 6 | 0.01514 | 0.0151 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 6} |
| item4|accepter into v|R|mismatched|e=other | 12 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 12} |
| item4|accepter into v|R|mismatched|e=sim-reader | 288 | 1.419e-10 | 1.42e-10 | 0.0151 | 1.00 | 0.00 | 0 | {'W': 114, 'F': 78, 'D': 96} |
| item4|into e, Rc resident|Bc|carrier-active | 708 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.00315 | {'F': 708} |
| item4|into e, Rc resident|B|sim-reader | 696 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000132 | {'U': 696} |
| item4|into e, Rc resident|C0|const-other | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'U': 348} |
| item4|into e, Rc resident|C1|const-other | 174 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'U': 174} |
| item4|into e, Rc resident|C1|half-naming-v | 174 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'U': 174} |
| item4|into e, Rc resident|C2|const-other | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'U': 348} |
| item4|into e, Rc resident|C3|const-other | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'U': 348} |
| item4|into e, Rc resident|C4|const-other | 174 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'U': 174} |
| item4|into e, Rc resident|C4|half-naming-v | 174 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'U': 174} |
| item4|into e, Rc resident|C5|const-other | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'U': 348} |
| item4|into e, Rc resident|C6|const-other | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'U': 348} |
| item4|into e, Rc resident|C7|const-other | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'U': 348} |
| item4|into e, Rc resident|C8|const-other | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'U': 348} |
| item4|into e, Rc resident|F2|sim-reader | 1392 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 1392} |
| item4|into e, Rc resident|Fc|carrier-active | 5664 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.000131 | {'F': 5664} |
| item4|into e, Rc resident|Fs|sim-reader | 2784 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 2784} |
| item4|into e, Rc resident|Ft|sim-reader | 2784 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 2784} |
| item4|into e, Rc resident|J|other | 696 | 0.01514 | 0.0151 | 1 | 1.00 | 0.00 | 0 | {'U': 696} |
| item4|into e, Rc resident|Oc|carrier-active | 354 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.00105 | {'F': 354} |
| item4|into e, Rc resident|Oc|carrier-inactive | 354 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.00105 | {'F': 354} |
| item4|into e, Rc resident|O|sim-reader | 2784 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 2784} |
| item4|into e, Rc resident|Pc|carrier-active | 1416 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0 | {'F': 1416} |
| item4|into e, Rc resident|Po|sim-reader | 1392 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 1392} |
| item4|into e, Rc resident|Pz|sim-reader | 1392 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 1392} |
| item4|into e, Rc resident|Q|sim-reader | 1392 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 1392} |
| item4|into e, Rc resident|Rcs|carrier-active | 354 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0 | {'F': 354} |
| item4|into e, Rc resident|Rcs|carrier-inactive | 354 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0 | {'F': 354} |
| item4|into e, Rc resident|Rc|carrier-active | 354 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.0021 | {'F': 354} |
| item4|into e, Rc resident|Rc|carrier-inactive | 354 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.0021 | {'F': 354} |
| item4|into e, Rc resident|R|sim-reader | 1392 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 1392} |
| item4|into e, Rc resident|X|sim-reader | 696 | 1 | 1 | 5.93 | 0.97 | 0.03 | 9.75e-06 | {'U': 696} |
| item4|into e, Rcs resident|Bc|carrier-active | 120 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.00325 | {'F': 120} |
| item4|into e, Rcs resident|B|sim-reader | 120 | 11.81 | 0.0151 | 27.9 | 0.50 | 0.50 | 0.00134 | {'F': 60, 'D': 60} |
| item4|into e, Rcs resident|C0|const-other | 54 | 1 | 1 | 5.93 | 0.78 | 0.22 | 0.000985 | {'U': 54} |
| item4|into e, Rcs resident|C1|const-other | 27 | 1 | 1 | 5.93 | 0.78 | 0.22 | 0.000985 | {'U': 27} |
| item4|into e, Rcs resident|C1|half-naming-v | 30 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.0136 | {'F': 30} |
| item4|into e, Rcs resident|C2|const-other | 54 | 1 | 1 | 5.93 | 0.78 | 0.22 | 0.000985 | {'U': 54} |
| item4|into e, Rcs resident|C3|const-other | 54 | 1 | 1 | 5.93 | 0.78 | 0.22 | 0.000985 | {'U': 54} |
| item4|into e, Rcs resident|C4|const-other | 27 | 1 | 1 | 5.93 | 0.78 | 0.22 | 0.000985 | {'U': 27} |
| item4|into e, Rcs resident|C4|half-naming-v | 30 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.0136 | {'F': 30} |
| item4|into e, Rcs resident|C5|const-other | 54 | 1 | 1 | 5.93 | 0.78 | 0.22 | 0.000985 | {'U': 54} |
| item4|into e, Rcs resident|C6|const-other | 54 | 1 | 1 | 5.93 | 0.78 | 0.22 | 0.000985 | {'U': 54} |
| item4|into e, Rcs resident|C7|const-other | 54 | 1 | 1 | 5.93 | 0.78 | 0.22 | 0.000985 | {'U': 54} |
| item4|into e, Rcs resident|C8|const-other | 54 | 1 | 1 | 5.93 | 0.78 | 0.22 | 0.000985 | {'U': 54} |
| item4|into e, Rcs resident|F2|sim-reader | 240 | 0.01514 | 7.6e-05 | 27.9 | 0.75 | 0.25 | 0 | {'D': 180, 'F': 60} |
| item4|into e, Rcs resident|Fc|carrier-active | 960 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.000135 | {'F': 960} |
| item4|into e, Rcs resident|Fs|sim-reader | 480 | 0.5076 | 0.0151 | 27.9 | 0.62 | 0.38 | 0 | {'D': 300, 'F': 180} |
| item4|into e, Rcs resident|Ft|sim-reader | 480 | 0.01514 | 7.6e-05 | 27.9 | 0.62 | 0.38 | 0 | {'D': 300, 'F': 180} |
| item4|into e, Rcs resident|J|other | 108 | 0.01514 | 0.0151 | 1 | 1.00 | 0.00 | 0 | {'U': 108} |
| item4|into e, Rcs resident|Oc|carrier-active | 60 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.00108 | {'F': 60} |
| item4|into e, Rcs resident|Oc|carrier-inactive | 60 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.00108 | {'F': 60} |
| item4|into e, Rcs resident|O|sim-reader | 480 | 0.007606 | 7.6e-05 | 22.6 | 0.62 | 0.38 | 0 | {'D': 300, 'F': 180} |
| item4|into e, Rcs resident|Pc|carrier-active | 240 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0 | {'F': 240} |
| item4|into e, Rcs resident|Po|sim-reader | 240 | 9.107 | 0.0151 | 27.9 | 0.50 | 0.50 | 0 | {'F': 120, 'D': 120} |
| item4|into e, Rcs resident|Pz|sim-reader | 240 | 0.01514 | 7.6e-05 | 1 | 1.00 | 0.00 | 0 | {'D': 240} |
| item4|into e, Rcs resident|Q|sim-reader | 240 | 0.01514 | 7.6e-05 | 1 | 1.00 | 0.00 | 0 | {'D': 240} |
| item4|into e, Rcs resident|Rcs|carrier-active | 60 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0 | {'F': 60} |
| item4|into e, Rcs resident|Rcs|carrier-inactive | 60 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0 | {'F': 60} |
| item4|into e, Rcs resident|Rc|carrier-active | 60 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.00217 | {'F': 60} |
| item4|into e, Rcs resident|Rc|carrier-inactive | 60 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.00217 | {'F': 60} |
| item4|into e, Rcs resident|R|sim-reader | 240 | 7.261 | 0.0151 | 27.9 | 0.50 | 0.50 | 0 | {'W': 60, 'D': 120, 'F': 60} |
| item4|into e, Rcs resident|X|sim-reader | 120 | 0.01514 | 0.0151 | 1 | 1.00 | 0.00 | 1.77e-06 | {'D': 120} |
| item4|accepter into v (matched)|Rcs|e class B | 12 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'F': 6, 'D': 6} |
| item4|accepter into v (matched)|Rcs|e class C0 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item4|accepter into v (matched)|Rcs|e class C1 | 6 | 5.377 | 1 | 9.75 | 0.50 | 0.50 | 0 | {'F': 3, 'U': 3} |
| item4|accepter into v (matched)|Rcs|e class C2 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item4|accepter into v (matched)|Rcs|e class C3 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item4|accepter into v (matched)|Rcs|e class C4 | 6 | 5.377 | 1 | 9.75 | 0.50 | 0.50 | 0 | {'U': 3, 'F': 3} |
| item4|accepter into v (matched)|Rcs|e class C5 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item4|accepter into v (matched)|Rcs|e class C6 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item4|accepter into v (matched)|Rcs|e class C7 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item4|accepter into v (matched)|Rcs|e class C8 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item4|accepter into v (matched)|Rcs|e class F2 | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 18, 'F': 6} |
| item4|accepter into v (matched)|Rcs|e class Fs | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item4|accepter into v (matched)|Rcs|e class Ft | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item4|accepter into v (matched)|Rcs|e class J | 12 | 0.5076 | 0.0151 | 1 | 1.00 | 0.00 | 0 | {'U': 12} |
| item4|accepter into v (matched)|Rcs|e class O | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item4|accepter into v (matched)|Rcs|e class Oc | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 6} |
| item4|accepter into v (matched)|Rcs|e class Po | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'F': 12, 'D': 12} |
| item4|accepter into v (matched)|Rcs|e class Pz | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 24} |
| item4|accepter into v (matched)|Rcs|e class Q | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 24} |
| item4|accepter into v (matched)|Rcs|e class R | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'W': 6, 'D': 12, 'F': 6} |
| item4|accepter into v (matched)|Rcs|e class Rc | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 6} |
| item4|accepter into v (matched)|Rcs|e class Rcs | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 6} |
| item4|accepter into v (matched)|Rcs|e class X | 12 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 12} |
| item4|accepter into v (matched)|Rc|e class B | 12 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 12} |
| item4|accepter into v (matched)|Rc|e class C0 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item4|accepter into v (matched)|Rc|e class C1 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item4|accepter into v (matched)|Rc|e class C2 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item4|accepter into v (matched)|Rc|e class C3 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item4|accepter into v (matched)|Rc|e class C4 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item4|accepter into v (matched)|Rc|e class C5 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item4|accepter into v (matched)|Rc|e class C6 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item4|accepter into v (matched)|Rc|e class C7 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item4|accepter into v (matched)|Rc|e class C8 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 6} |
| item4|accepter into v (matched)|Rc|e class F2 | 24 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 24} |
| item4|accepter into v (matched)|Rc|e class Fs | 48 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 48} |
| item4|accepter into v (matched)|Rc|e class Ft | 48 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 48} |
| item4|accepter into v (matched)|Rc|e class J | 12 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 12} |
| item4|accepter into v (matched)|Rc|e class O | 48 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 48} |
| item4|accepter into v (matched)|Rc|e class Oc | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 6} |
| item4|accepter into v (matched)|Rc|e class Po | 24 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 24} |
| item4|accepter into v (matched)|Rc|e class Pz | 24 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 24} |
| item4|accepter into v (matched)|Rc|e class Q | 24 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 24} |
| item4|accepter into v (matched)|Rc|e class R | 24 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 24} |
| item4|accepter into v (matched)|Rc|e class Rc | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 6} |
| item4|accepter into v (matched)|Rc|e class Rcs | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0.000732 | {'F': 6} |
| item4|accepter into v (matched)|Rc|e class X | 12 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'U': 12} |
| item4|accepter into v (matched)|R|e class B | 12 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'F': 6, 'D': 6} |
| item4|accepter into v (matched)|R|e class C0 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item4|accepter into v (matched)|R|e class C1 | 6 | 5.377 | 1 | 9.75 | 0.50 | 0.50 | 0 | {'F': 3, 'U': 3} |
| item4|accepter into v (matched)|R|e class C2 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item4|accepter into v (matched)|R|e class C3 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item4|accepter into v (matched)|R|e class C4 | 6 | 5.377 | 1 | 9.75 | 0.50 | 0.50 | 0 | {'U': 3, 'F': 3} |
| item4|accepter into v (matched)|R|e class C5 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item4|accepter into v (matched)|R|e class C6 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item4|accepter into v (matched)|R|e class C7 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item4|accepter into v (matched)|R|e class C8 | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item4|accepter into v (matched)|R|e class F2 | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 18, 'F': 6} |
| item4|accepter into v (matched)|R|e class Fs | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item4|accepter into v (matched)|R|e class Ft | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item4|accepter into v (matched)|R|e class J | 12 | 0.5076 | 0.0151 | 1 | 1.00 | 0.00 | 0 | {'U': 12} |
| item4|accepter into v (matched)|R|e class O | 48 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 30, 'F': 18} |
| item4|accepter into v (matched)|R|e class Oc | 6 | 9.755 | 9.75 | 9.75 | 0.00 | 1.00 | 0 | {'F': 6} |
| item4|accepter into v (matched)|R|e class Po | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'F': 12, 'D': 12} |
| item4|accepter into v (matched)|R|e class Pz | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 24} |
| item4|accepter into v (matched)|R|e class Q | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 24} |
| item4|accepter into v (matched)|R|e class R | 24 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'W': 6, 'D': 12, 'F': 6} |
| item4|accepter into v (matched)|R|e class Rc | 6 | 1 | 1 | 1 | 1.00 | 0.00 | 0 | {'U': 6} |
| item4|accepter into v (matched)|R|e class Rcs | 6 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'W': 6} |
| item4|accepter into v (matched)|R|e class X | 12 | 1.419e-10 | 1.42e-10 | 1.42e-10 | 1.00 | 0.00 | 0 | {'D': 12} |
| item1c|into e, 1/3-constant victim|Bc|carrier-active|points at b=True | 1032 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0.000125 | {'U': 1032} |
| item1c|into e, 1/3-constant victim|B|sim-reader|points at b=False | 1032 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0.000125 | {'U': 1032} |
| item1c|into e, 1/3-constant victim|C0|const-other|points at b=False | 516 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0.000524 | {'U': 516} |
| item1c|into e, 1/3-constant victim|C1|const-other|points at b=False | 258 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0.000524 | {'U': 258} |
| item1c|into e, 1/3-constant victim|C1|half-naming-v|points at b=False | 258 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0.000524 | {'U': 258} |
| item1c|into e, 1/3-constant victim|C2|const-other|points at b=False | 516 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0.000524 | {'U': 516} |
| item1c|into e, 1/3-constant victim|C3|const-other|points at b=False | 516 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0.000524 | {'U': 516} |
| item1c|into e, 1/3-constant victim|C4|const-other|points at b=False | 258 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0.000524 | {'U': 258} |
| item1c|into e, 1/3-constant victim|C4|half-naming-v|points at b=False | 258 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0.000524 | {'U': 258} |
| item1c|into e, 1/3-constant victim|C5|const-other|points at b=False | 516 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0.000524 | {'U': 516} |
| item1c|into e, 1/3-constant victim|C6|const-other|points at b=False | 516 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0.000524 | {'U': 516} |
| item1c|into e, 1/3-constant victim|C7|const-other|points at b=False | 516 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0.000524 | {'U': 516} |
| item1c|into e, 1/3-constant victim|C8|const-other|points at b=False | 516 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0.000524 | {'U': 516} |
| item1c|into e, 1/3-constant victim|F2|sim-reader|points at b=False | 2064 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0 | {'U': 2064} |
| item1c|into e, 1/3-constant victim|Fc|carrier-active|points at b=True | 8256 | 1 | 1 | 5.93 | 0.98 | 0.02 | 5.22e-06 | {'U': 8256} |
| item1c|into e, 1/3-constant victim|Fs|sim-reader|points at b=False | 4128 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0 | {'U': 4128} |
| item1c|into e, 1/3-constant victim|Ft|sim-reader|points at b=False | 4128 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0 | {'U': 4128} |
| item1c|into e, 1/3-constant victim|J|other|points at b=False | 1032 | 0.01514 | 0.0151 | 1 | 1.00 | 0.00 | 0 | {'U': 1032} |
| item1c|into e, 1/3-constant victim|Oc|carrier-active|points at b=False | 516 | 1 | 1 | 5.93 | 0.98 | 0.02 | 4.18e-05 | {'U': 516} |
| item1c|into e, 1/3-constant victim|Oc|carrier-inactive|points at b=True | 516 | 1 | 1 | 5.93 | 0.98 | 0.02 | 4.18e-05 | {'U': 516} |
| item1c|into e, 1/3-constant victim|O|sim-reader|points at b=False | 4128 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0 | {'U': 4128} |
| item1c|into e, 1/3-constant victim|Pc|carrier-active|points at b=True | 2064 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0 | {'U': 2064} |
| item1c|into e, 1/3-constant victim|Po|sim-reader|points at b=False | 2064 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0 | {'U': 2064} |
| item1c|into e, 1/3-constant victim|Pz|sim-reader|points at b=False | 2064 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0 | {'U': 2064} |
| item1c|into e, 1/3-constant victim|Q|sim-reader|points at b=False | 2064 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0 | {'U': 2064} |
| item1c|into e, 1/3-constant victim|Rcs|carrier-active|points at b=False | 516 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0 | {'U': 516} |
| item1c|into e, 1/3-constant victim|Rcs|carrier-inactive|points at b=True | 516 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0 | {'U': 516} |
| item1c|into e, 1/3-constant victim|Rc|carrier-active|points at b=False | 516 | 1 | 1 | 5.93 | 0.98 | 0.02 | 8.36e-05 | {'U': 516} |
| item1c|into e, 1/3-constant victim|Rc|carrier-inactive|points at b=True | 516 | 1 | 1 | 5.93 | 0.98 | 0.02 | 8.36e-05 | {'U': 516} |
| item1c|into e, 1/3-constant victim|R|sim-reader|points at b=False | 2064 | 1 | 1 | 5.93 | 0.98 | 0.02 | 0 | {'U': 2064} |
| item1c|into e, 1/3-constant victim|X|sim-reader|points at b=False | 1032 | 1 | 1 | 5.93 | 0.98 | 0.02 | 9.29e-06 | {'U': 1032} |
| item4c|into e, 1/3-constant victim|Bc|carrier-active|points at b=True | 744 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.00315 | {'F': 744} |
| item4c|into e, 1/3-constant victim|B|sim-reader|points at b=False | 732 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000131 | {'U': 732} |
| item4c|into e, 1/3-constant victim|C0|const-other|points at b=False | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 366} |
| item4c|into e, 1/3-constant victim|C1|const-other|points at b=False | 183 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 183} |
| item4c|into e, 1/3-constant victim|C1|half-naming-v|points at b=False | 183 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 183} |
| item4c|into e, 1/3-constant victim|C2|const-other|points at b=False | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 366} |
| item4c|into e, 1/3-constant victim|C3|const-other|points at b=False | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 366} |
| item4c|into e, 1/3-constant victim|C4|const-other|points at b=False | 183 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 183} |
| item4c|into e, 1/3-constant victim|C4|half-naming-v|points at b=False | 183 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 183} |
| item4c|into e, 1/3-constant victim|C5|const-other|points at b=False | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 366} |
| item4c|into e, 1/3-constant victim|C6|const-other|points at b=False | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 366} |
| item4c|into e, 1/3-constant victim|C7|const-other|points at b=False | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 366} |
| item4c|into e, 1/3-constant victim|C8|const-other|points at b=False | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000546 | {'U': 366} |
| item4c|into e, 1/3-constant victim|F2|sim-reader|points at b=False | 1464 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 1464} |
| item4c|into e, 1/3-constant victim|Fc|carrier-active|points at b=True | 5952 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.000131 | {'F': 5952} |
| item4c|into e, 1/3-constant victim|Fs|sim-reader|points at b=False | 2928 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 2928} |
| item4c|into e, 1/3-constant victim|Ft|sim-reader|points at b=False | 2928 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 2928} |
| item4c|into e, 1/3-constant victim|J|other|points at b=False | 732 | 0.01514 | 0.0151 | 1 | 1.00 | 0.00 | 0 | {'U': 732} |
| item4c|into e, 1/3-constant victim|Oc|carrier-active|points at b=False | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 4.36e-05 | {'U': 366} |
| item4c|into e, 1/3-constant victim|Oc|carrier-inactive|points at b=True | 372 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.00105 | {'F': 372} |
| item4c|into e, 1/3-constant victim|O|sim-reader|points at b=False | 2928 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 2928} |
| item4c|into e, 1/3-constant victim|Pc|carrier-active|points at b=True | 1488 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0 | {'F': 1488} |
| item4c|into e, 1/3-constant victim|Po|sim-reader|points at b=False | 1464 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 1464} |
| item4c|into e, 1/3-constant victim|Pz|sim-reader|points at b=False | 1464 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 1464} |
| item4c|into e, 1/3-constant victim|Q|sim-reader|points at b=False | 1464 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 1464} |
| item4c|into e, 1/3-constant victim|Rcs|carrier-active|points at b=False | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 366} |
| item4c|into e, 1/3-constant victim|Rcs|carrier-inactive|points at b=True | 372 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0 | {'F': 372} |
| item4c|into e, 1/3-constant victim|Rc|carrier-active|points at b=False | 366 | 1 | 1 | 5.93 | 0.97 | 0.03 | 8.71e-05 | {'U': 366} |
| item4c|into e, 1/3-constant victim|Rc|carrier-inactive|points at b=True | 372 | 27.86 | 27.9 | 32.9 | 0.00 | 1.00 | 0.0021 | {'F': 372} |
| item4c|into e, 1/3-constant victim|R|sim-reader|points at b=False | 1464 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0 | {'U': 1464} |
| item4c|into e, 1/3-constant victim|X|sim-reader|points at b=False | 732 | 1 | 1 | 5.93 | 0.97 | 0.03 | 9.68e-06 | {'U': 732} |
| item3b|FC|out|Bc | 4770 | 0.01514 | 0.0151 | 22.6 | 0.66 | 0.34 | 0.000865 | {'F': 3432, 'D': 1338} |
| item3b|FC|out|Fc | 38160 | 0.01514 | 7.6e-05 | 22.6 | 0.75 | 0.25 | 2.63e-05 | {'D': 13944, 'F': 24216} |
| item3b|FC|out|Oc | 4770 | 27.86 | 1 | 27.9 | 0.46 | 0.54 | 0.000578 | {'F': 4770} |
| item3b|FC|out|Pc | 9540 | 0.01514 | 7.6e-05 | 22.6 | 0.99 | 0.01 | 0 | {'D': 5820, 'F': 3720} |
| item3b|FC|out|Rc | 4770 | 1 | 1 | 1 | 1.00 | 0.00 | 7.5e-05 | {'F': 4770} |
| item3b|FC|out|Rcs | 4770 | 0.01514 | 0.0151 | 13.5 | 0.66 | 0.34 | 0 | {'W': 1620, 'D': 1338, 'F': 1812} |
| item3b|FC|pair|Bc | 9540 | 1 | 9.15e-15 | 15.4 | 0.72 | 0.28 | 0.000269 | {'W': 630, 'U': 606, 'F': 4464, 'D': 3840} |
| item3b|FC|pair|Fc | 76320 | 1 | 9.15e-15 | 5.93 | 0.92 | 0.08 | 4.82e-06 | {'F': 48042, 'D': 26850, 'W': 1428} |
| item3b|FC|pair|Oc | 9540 | 1 | 3.03e-12 | 5.93 | 0.70 | 0.30 | 7.75e-05 | {'F': 5232, 'W': 738, 'D': 3570} |
| item3b|FC|pair|Pc | 19080 | 3.029e-12 | 2.69e-17 | 5.93 | 0.98 | 0.02 | 0 | {'F': 3540, 'D': 15228, 'W': 312} |
| item3b|FC|pair|Rc | 9540 | 9.626e-10 | 3.03e-12 | 0.0754 | 1.00 | 0.00 | 8.33e-07 | {'W': 3210, 'F': 396, 'U': 606, 'D': 5328} |
| item3b|FC|pair|Rcs | 9540 | 9.626e-10 | 9.15e-15 | 5.93 | 0.98 | 0.02 | 0 | {'F': 1770, 'W': 2694, 'D': 4638, 'U': 438} |
| item3b|FI|out|Bc | 3456 | 1 | 1 | 5.93 | 0.75 | 0.25 | 0.000251 | {'F': 3456} |
| item3b|FI|out|Fc | 27648 | 1 | 0.0151 | 5.93 | 0.81 | 0.19 | 8.92e-06 | {'F': 27648} |
| item3b|FI|out|Oc | 3456 | 5.926 | 5.93 | 37.9 | 0.00 | 1.00 | 0.000583 | {'F': 3456} |
| item3b|FI|out|Pc | 6912 | 1 | 0.0151 | 5.93 | 0.83 | 0.17 | 0 | {'F': 6912} |
| item3b|FI|out|Rc | 3456 | 5.926 | 5.93 | 11.6 | 0.00 | 1.00 | 0.000552 | {'F': 3456} |
| item3b|FI|out|Rcs | 3456 | 1 | 1 | 5.93 | 0.75 | 0.25 | 0 | {'F': 3456} |
| item3b|FI|pair|Bc | 6912 | 1 | 3.03e-12 | 5.93 | 0.89 | 0.11 | 0.000141 | {'F': 4752, 'D': 2160} |
| item3b|FI|pair|Fc | 55296 | 0.01514 | 9.15e-15 | 5.93 | 0.93 | 0.07 | 3.96e-06 | {'F': 28512, 'D': 26784} |
| item3b|FI|pair|Oc | 6912 | 5.926 | 9.63e-10 | 11.6 | 0.17 | 0.83 | 0.000215 | {'F': 6408, 'D': 504} |
| item3b|FI|pair|Pc | 13824 | 3.029e-12 | 9.15e-15 | 5.93 | 0.99 | 0.01 | 0 | {'F': 792, 'D': 13032} |
| item3b|FI|pair|Rc | 6912 | 9.626e-10 | 9.63e-10 | 2.3 | 0.96 | 0.00 | 7.32e-06 | {'F': 2592, 'D': 2808, 'W': 1512} |
| item3b|FI|pair|Rcs | 6912 | 0.0004656 | 3.03e-12 | 0.0754 | 1.00 | 0.00 | 0 | {'W': 4752, 'D': 2160} |
| item3|Fc,Bc|out|B | 22272 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000132 | {'F': 22272} |
| item3|Fc,Bc|out|Bc | 22656 | 16.89 | 1 | 32.9 | 0.48 | 0.52 | 0.00164 | {'D': 5664, 'F': 16992} |
| item3|Fc,Bc|out|C0 | 11136 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 11136} |
| item3|Fc,Bc|out|C2 | 11136 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 11136} |
| item3|Fc,Bc|out|C3 | 11136 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 11136} |
| item3|Fc,Bc|out|C5 | 11136 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 11136} |
| item3|Fc,Bc|out|C6 | 11136 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 11136} |
| item3|Fc,Bc|out|C8 | 11136 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 11136} |
| item3|Fc,Bc|pair|B | 45312 | 9.149e-15 | 7.73e-20 | 9.75 | 0.99 | 0.01 | 1.6e-05 | {'W': 1320, 'U': 576, 'F': 21564, 'D': 21852} |
| item3|Fc,Bc|pair|Bc | 33984 | 1 | 1 | 1 | 1.00 | 0.00 | 0.000112 | {'F': 33984} |
| item3|Fc,Bc|pair|C0 | 22656 | 3.029e-12 | 3.03e-12 | 0.000466 | 1.00 | 0.00 | 8.21e-08 | {'W': 5376, 'F': 4368, 'D': 9216, 'U': 3696} |
| item3|Fc,Bc|pair|C2 | 22656 | 3.029e-12 | 3.03e-12 | 9.75 | 0.99 | 0.01 | 6.8e-05 | {'D': 15612, 'W': 432, 'F': 5988, 'U': 624} |
| item3|Fc,Bc|pair|C3 | 22656 | 3.029e-12 | 3.03e-12 | 0.000466 | 1.00 | 0.00 | 8.21e-08 | {'W': 5376, 'F': 4368, 'U': 3696, 'D': 9216} |
| item3|Fc,Bc|pair|C5 | 22656 | 3.029e-12 | 3.03e-12 | 9.75 | 0.99 | 0.01 | 6.8e-05 | {'U': 624, 'W': 432, 'D': 15612, 'F': 5988} |
| item3|Fc,Bc|pair|C6 | 22656 | 3.029e-12 | 3.03e-12 | 3.03e-12 | 1.00 | 0.00 | 1.42e-15 | {'D': 15948, 'W': 432, 'F': 5988, 'U': 288} |
| item3|Fc,Bc|pair|C8 | 22656 | 3.029e-12 | 3.03e-12 | 3.03e-12 | 1.00 | 0.00 | 1.42e-15 | {'D': 15948, 'W': 432, 'F': 5988, 'U': 288} |
| item3|Fc,Fc|out|B | 178176 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000132 | {'F': 178176} |
| item3|Fc,Fc|out|Bc | 181248 | 16.89 | 1 | 32.9 | 0.48 | 0.52 | 0.00164 | {'D': 45312, 'F': 135936} |
| item3|Fc,Fc|out|C0 | 89088 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 89088} |
| item3|Fc,Fc|out|C2 | 89088 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 89088} |
| item3|Fc,Fc|out|C3 | 89088 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 89088} |
| item3|Fc,Fc|out|C5 | 89088 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 89088} |
| item3|Fc,Fc|out|C6 | 89088 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 89088} |
| item3|Fc,Fc|out|C8 | 89088 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 89088} |
| item3|Fc,Fc|pair|B | 362496 | 9.149e-15 | 7.73e-20 | 9.75 | 0.99 | 0.01 | 1.74e-05 | {'W': 8832, 'U': 3072, 'F': 165312, 'D': 185280} |
| item3|Fc,Fc|pair|Bc | 362496 | 1 | 1 | 1 | 1.00 | 0.00 | 0.000113 | {'F': 362496} |
| item3|Fc,Fc|pair|C0 | 181248 | 3.029e-12 | 3.03e-12 | 0.000466 | 1.00 | 0.00 | 3.9e-08 | {'W': 29952, 'F': 46848, 'D': 99840, 'U': 4608} |
| item3|Fc,Fc|pair|C2 | 181248 | 3.029e-12 | 3.03e-12 | 9.75 | 0.98 | 0.02 | 7.78e-05 | {'D': 127680, 'W': 2304, 'F': 48192, 'U': 3072} |
| item3|Fc,Fc|pair|C3 | 181248 | 3.029e-12 | 3.03e-12 | 0.000466 | 1.00 | 0.00 | 3.9e-08 | {'W': 29952, 'F': 46848, 'U': 4608, 'D': 99840} |
| item3|Fc,Fc|pair|C5 | 181248 | 3.029e-12 | 3.03e-12 | 9.75 | 0.98 | 0.02 | 7.78e-05 | {'U': 3072, 'W': 2304, 'D': 127680, 'F': 48192} |
| item3|Fc,Fc|pair|C6 | 181248 | 3.029e-12 | 3.03e-12 | 3.03e-12 | 1.00 | 0.00 | 1.42e-15 | {'D': 130752, 'W': 2304, 'F': 48192} |
| item3|Fc,Fc|pair|C8 | 181248 | 3.029e-12 | 3.03e-12 | 3.03e-12 | 1.00 | 0.00 | 1.42e-15 | {'D': 130752, 'W': 2304, 'F': 48192} |
| item3|Rc,Oc|out|B | 696 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000132 | {'F': 696} |
| item3|Rc,Oc|out|Bc | 708 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000131 | {'F': 708} |
| item3|Rc,Oc|out|C0 | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 348} |
| item3|Rc,Oc|out|C2 | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 348} |
| item3|Rc,Oc|out|C3 | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 348} |
| item3|Rc,Oc|out|C5 | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 348} |
| item3|Rc,Oc|out|C6 | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 348} |
| item3|Rc,Oc|out|C8 | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 348} |
| item3|Rc,Oc|pair|B | 1416 | 0.01514 | 9.15e-15 | 9.75 | 0.97 | 0.03 | 7.1e-05 | {'W': 120, 'U': 72, 'F': 702, 'D': 522} |
| item3|Rc,Oc|pair|Bc | 1416 | 1 | 1 | 1 | 1.00 | 0.00 | 0.000112 | {'F': 1416} |
| item3|Rc,Oc|pair|C0 | 708 | 3.029e-12 | 3.03e-12 | 0.000466 | 1.00 | 0.00 | 8.35e-08 | {'W': 327, 'U': 36, 'D': 345} |
| item3|Rc,Oc|pair|C2 | 708 | 3.029e-12 | 3.03e-12 | 9.75 | 0.97 | 0.03 | 0.000117 | {'D': 594, 'W': 78, 'U': 36} |
| item3|Rc,Oc|pair|C3 | 708 | 3.029e-12 | 3.03e-12 | 0.000466 | 1.00 | 0.00 | 8.35e-08 | {'W': 327, 'U': 36, 'D': 345} |
| item3|Rc,Oc|pair|C5 | 708 | 3.029e-12 | 3.03e-12 | 9.75 | 0.97 | 0.03 | 0.000117 | {'U': 36, 'W': 78, 'D': 594} |
| item3|Rc,Oc|pair|C6 | 708 | 3.029e-12 | 3.03e-12 | 3.03e-12 | 1.00 | 0.00 | 1.42e-15 | {'D': 612, 'W': 78, 'U': 18} |
| item3|Rc,Oc|pair|C8 | 708 | 3.029e-12 | 3.03e-12 | 3.03e-12 | 1.00 | 0.00 | 1.42e-15 | {'D': 612, 'W': 78, 'U': 18} |
| item3|Rcs,half|out|B | 696 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000132 | {'F': 696} |
| item3|Rcs,half|out|Bc | 708 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.000131 | {'F': 708} |
| item3|Rcs,half|out|C0 | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 348} |
| item3|Rcs,half|out|C2 | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 348} |
| item3|Rcs,half|out|C3 | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 348} |
| item3|Rcs,half|out|C5 | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 348} |
| item3|Rcs,half|out|C6 | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 348} |
| item3|Rcs,half|out|C8 | 348 | 1 | 1 | 5.93 | 0.97 | 0.03 | 0.00055 | {'F': 348} |
| item3|Rcs,half|pair|B | 1416 | 0.01514 | 9.15e-15 | 9.75 | 0.98 | 0.02 | 5.04e-05 | {'W': 258, 'U': 30, 'F': 666, 'D': 462} |
| item3|Rcs,half|pair|Bc | 1416 | 1 | 3.03e-12 | 9.75 | 0.99 | 0.01 | 9.76e-05 | {'W': 18, 'U': 18, 'F': 1230, 'D': 150} |
| item3|Rcs,half|pair|C0 | 708 | 3.029e-12 | 3.03e-12 | 0.000466 | 1.00 | 0.00 | 8.35e-08 | {'W': 327, 'U': 36, 'D': 345} |
| item3|Rcs,half|pair|C2 | 708 | 3.029e-12 | 3.03e-12 | 9.75 | 0.97 | 0.03 | 0.000117 | {'D': 594, 'W': 78, 'U': 36} |
| item3|Rcs,half|pair|C3 | 708 | 3.029e-12 | 3.03e-12 | 0.000466 | 1.00 | 0.00 | 8.35e-08 | {'W': 327, 'U': 36, 'D': 345} |
| item3|Rcs,half|pair|C5 | 708 | 3.029e-12 | 3.03e-12 | 9.75 | 0.97 | 0.03 | 0.000117 | {'U': 36, 'W': 78, 'D': 594} |
| item3|Rcs,half|pair|C6 | 708 | 3.029e-12 | 3.03e-12 | 3.03e-12 | 1.00 | 0.00 | 1.42e-15 | {'D': 612, 'W': 78, 'U': 18} |
| item3|Rcs,half|pair|C8 | 708 | 3.029e-12 | 3.03e-12 | 3.03e-12 | 1.00 | 0.00 | 1.42e-15 | {'D': 612, 'W': 78, 'U': 18} |
