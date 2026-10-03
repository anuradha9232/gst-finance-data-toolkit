"""Tests for the individual validation rules (R1-R5)."""

from gst_core import validate_invoice

# A fully correct intra-state invoice (supplier and place of supply both in state 10).
GOOD = {
    "invoice_no": "INV-1",
    "supplier_gstin": "10AABCU9603R1ZM",
    "place_of_supply_code": "10",
    "taxable_value": 10000,
    "gst_rate": 18,
    "cgst": 900,
    "sgst": 900,
    "igst": 0,
    "invoice_total": 11800,
}


def test_good_invoice_has_no_issues():
    assert validate_invoice(GOOD) == []


def test_r1_bad_gstin_flagged():
    inv = dict(GOOD, supplier_gstin="10AABCU9603R1Z")  # 14 chars
    assert any(i.startswith("R1") for i in validate_invoice(inv))


def test_r2_invalid_rate_flagged():
    inv = dict(GOOD, gst_rate=15, cgst=750, sgst=750, invoice_total=11500)
    assert any(i.startswith("R2") for i in validate_invoice(inv))


def test_r3_intra_charged_igst_flagged():
    inv = dict(GOOD, cgst=0, sgst=0, igst=1800, invoice_total=11800)
    assert any(i.startswith("R3") for i in validate_invoice(inv))


def test_r4_wrong_tax_amount_flagged():
    inv = dict(GOOD, cgst=800, sgst=800, invoice_total=11600)
    assert any(i.startswith("R4") for i in validate_invoice(inv))


def test_r5_total_mismatch_flagged():
    inv = dict(GOOD, invoice_total=12000)
    assert any(i.startswith("R5") for i in validate_invoice(inv))


def test_inter_state_invoice_valid():
    inv = {
        "invoice_no": "INV-2",
        "supplier_gstin": "10AABCU9603R1ZM",
        "place_of_supply_code": "27",   # different state -> IGST
        "taxable_value": 50000,
        "gst_rate": 18,
        "cgst": 0,
        "sgst": 0,
        "igst": 9000,
        "invoice_total": 59000,
    }
    assert validate_invoice(inv) == []
