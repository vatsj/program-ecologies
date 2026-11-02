"""Tests of the annealed-tail machinery (src/annealed_tail*.py): schedules, linearity and mass conservation of the tail field,
dose conservation of the backward-Euler step, the flux attribution against the field.  Fast (tiny supports)."""
import os, sys
import numpy as np
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import many_islands as MI
import unequal_basin as UB
import unequal_basin_validate as UV
import annealed_tail as A
import annealed_tail_attr as AT


def tiny(seed=3, n=6, m=2):
    arm = UB.get_arm('L')
    supp = UV.tiny_support(arm, np.random.default_rng(seed), n)
    obj = UB.Obj('L', 0.0, supp, m)
    rng = np.random.default_rng(seed + 1)
    x = rng.random(obj.n) ** 3
    x = obj.sym(x)
    x /= x.sum()
    return arm, obj, x


def prior_on(arm):
    return arm.laws.copy()


def test_schedule_dose_and_remaining():
    s = A.Sched('anneal', 7.0, 100.0)
    assert abs(s.cum(1e12) - 7.0) < 1e-6
    # eps integrates to the dose
    ts = np.linspace(0, 5000, 200001)
    num = np.trapz([s.eps(t) for t in ts], ts)
    assert abs(num - s.cum(5000)) < 1e-6
    assert abs(s.remaining(100.0) - 3.5) < 1e-12
    c = A.Sched('const', 4.0, T=1e4)
    assert abs(c.cum(2e4) - 4.0) < 1e-12 and abs(c.dose(0, 5e3) - 2.0) < 1e-12


def test_tail_field_linear_and_mass_conserving():
    arm, obj, x = tiny()
    S = A.DSL(obj, prior_on(arm))
    rng = np.random.default_rng(0)
    q1 = np.abs(rng.standard_normal(arm.laws.shape)) * (arm.laws > 0)
    q1 /= q1.sum(axis=1, keepdims=True)
    q2 = obj.marg(x)
    g = S._flux(x, 0.3 * q1 + 1.7 * q2)
    assert np.abs(g - 0.3 * S._flux(x, q1) - 1.7 * S._flux(x, q2)).max() < 1e-12
    for e in (0.0, 1.0, 300.0):
        assert abs((S.F(x) + e * S.G(x)).sum()) < 1e-12 * max(1, e)


def test_tail_field_is_s3_equivariant():
    arm, obj, x = tiny()
    S = A.DSL(obj, prior_on(arm))
    Gx = S.G(x)
    for pi in obj.perm_idx[1:]:
        assert np.abs(Gx[pi] - Gx).max() < 1e-13


def test_be_step_delivers_the_dose():
    # with a tail only (no migration effect), a backward-Euler step with large h and a prescribed dose moves x as the burst does at first order
    arm, obj, x = tiny()
    S = A.DSL(obj, prior_on(arm))
    # small step: BE with dose d on step h equals x + h F + d G to second order
    h, d = 1e-3, 2e-3
    xn, info = A.be_step(S, x, h, d / h)
    ref = x + h * S.F(x) + d * S.G(x)
    assert np.abs(xn - ref).max() < 1e-5 * np.abs(ref).max() + 1e-9
    assert info['resid'] < 1e-8


def test_burst_matches_small_dose_first_order():
    arm, obj, x = tiny()
    S = A.DSL(obj, prior_on(arm))
    d = 1e-4
    xb = A.burst(S, x, d)
    assert np.abs(xb - (x + d * S.G(x))).max() < 1e-6 * np.abs(S.G(x)).max() * 100 + 1e-12
    assert abs(xb.sum() - 1) < 1e-12


def test_flux_attribution_sums_to_class_flux():
    arm, obj, x = tiny()
    cell = type('C', (), {})()
    cell.arm = arm
    cell.isc = obj.isc
    S = A.DSL(obj, prior_on(arm))
    arrs = AT.attr_arrays(cell, obj)
    T = AT.flux_tensor(S, arrs, x, S.p)
    # class-changing flux out of class c minus into c = - d/dt (class share c) under the tail (the unit-rate tail field)
    dsh = np.bincount(obj.cl, weights=S.G(x), minlength=5)
    net = T.sum(axis=(2, 3, 4))           # [from, to]
    for c in range(5):
        assert abs((net[:, c].sum() - net[c, :].sum()) - dsh[c]) < 1e-12
    # the same for migrants
    Tm = AT.flux_tensor(S, arrs, x, obj.marg(x))
    dshm = np.bincount(obj.cl, weights=S.F(x), minlength=5)
    netm = Tm.sum(axis=(2, 3, 4))
    for c in range(5):
        assert abs((netm[:, c].sum() - netm[c, :].sum()) - dshm[c]) < 1e-12


def test_ablation_matched_dose_nulls_events():
    cell = UB.Cell('L', 0.0, 0, (0,))
    p = A.tail_law(cell, 'bully')
    q = A.tail_law(cell, 'full')
    assert p.sum() < q.sum() and abs(q.sum(axis=1) - 1).max() < 1e-12
    pr = A.tail_law(cell, 'bully', renorm=True)
    assert abs(pr.sum(axis=1) - q.sum(axis=1)).max() < 1e-12
