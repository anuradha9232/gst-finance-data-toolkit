"""
validate.py
-----------
Runs the GST data-validation rules (see validation-rules.md) against an invoice
register CSV and reports every row that violates a rule.

Run:  python validation/validate.py

This mirrors the manual checks I used to run on invoice registers while keeping
the books: confirm each row's tax is calculated correctly, the intra/inter-state
tax type is right, the totals reconcile, and the GSTINs are well-formed.
"""

import csv
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "data", "sample_invoice_register.csv")

VALID_RATES = {0, 5, 12, 18, 28}
GSTIN_RE = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")


def check_row(r):
    """Return a list of rule violations for one invoice row."""
    issues = []
    gstin = r["supplier_gstin"].strip()
    pos = r["place_of_supply_code"].strip()
    taxable = float(r["taxable_value"])
    rate = float(r["gst_rate"])
    cgst = float(r["cgst"])
    sgst = float(r["sgst"])
    igst = float(r["igst"])
    total = float(r["invoice_total"])

    supplier_state = gstin[:2]
    is_intra = (pos == supplier_state)

    # R1 - GSTIN format
    if not GSTIN_RE.match(gstin):
        issues.append(f"R1 invalid GSTIN format ({gstin!r}, {len(gstin)} chars)")

    # R2 - valid GST rate
    if rate not in VALID_RATES:
        issues.append(f"R2 invalid GST rate ({rate:g}%); allowed: 0/5/12/18/28")

    # R3 - intra vs inter tax type
    if rate > 0:
        if is_intra and igst > 0:
            issues.append("R3 intra-state supply charged IGST (should be CGST+SGST)")
        if (not is_intra) and (cgst > 0 or sgst > 0):
            issues.append("R3 inter-state supply charged CGST/SGST (should be IGST)")

    # R4 - tax amounts correct
    if is_intra:
        expected = round(taxable * rate / 200, 2)
        if round(cgst, 2) != expected or round(sgst, 2) != expected:
            issues.append(f"R4 CGST/SGST should each be {expected:g} (got {cgst:g}/{sgst:g})")
    else:
        expected = round(taxable * rate / 100, 2)
        if round(igst, 2) != expected:
            issues.append(f"R4 IGST should be {expected:g} (got {igst:g})")

    # R5 - total reconciles
    expected_total = round(taxable + cgst + sgst + igst, 2)
    if round(total, 2) != expected_total:
        issues.append(f"R5 total should be {expected_total:g} (got {total:g})")

    return issues


def main():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    flagged = 0
    print(f"Validating {len(rows)} invoices from sample_invoice_register.csv\n")
    for r in rows:
        issues = check_row(r)
        if issues:
            flagged += 1
            print(f"  {r['invoice_no']}:")
            for i in issues:
                print(f"      - {i}")

    clean = len(rows) - flagged
    print(f"\nSummary: {clean} clean, {flagged} flagged out of {len(rows)}.")


if __name__ == "__main__":
    main()
