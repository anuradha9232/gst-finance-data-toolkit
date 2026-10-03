"""Cross-validation: two independent tax decompositions must agree.

method A splits the rate first (CGST = SGST = taxable*rate/200); method B
computes the total tax first and halves it. If they ever disagree, one of them
is wrong - so the ground truth is implemented twice and checked against itself.
"""

from gst_core import expected_tax_method_a, expected_tax_method_b

RATES = [0, 5, 12, 18, 28]


def test_methods_agree_across_the_grid():
    mismatches = []
    for taxable in range(1000, 500001, 1000):   # multiples of 1000
        for rate in RATES:
            for intra in (True, False):
                a = expected_tax_method_a(taxable, rate, intra)
                b = expected_tax_method_b(taxable, rate, intra)
                if a != b:
                    mismatches.append((taxable, rate, intra, a, b))
    assert not mismatches, f"{len(mismatches)} disagreements, e.g. {mismatches[:3]}"


def test_totals_reconcile():
    for taxable in (1000, 25000, 499000):
        for rate in RATES:
            for intra in (True, False):
                t = expected_tax_method_a(taxable, rate, intra)
                assert round(t["cgst"] + t["sgst"] + t["igst"], 2) == round(taxable * rate / 100.0, 2)
