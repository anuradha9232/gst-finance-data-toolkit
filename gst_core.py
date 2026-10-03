"""
gst_core.py - core GST invoice validation logic.

Pure standard library and deterministic. Provides two independent
implementations of the tax calculation (method A: split-first, method B:
total-first) so a test can assert they agree - a cross-validation of the
ground truth from two different decompositions.
"""

import re

VALID_RATES = {0, 5, 12, 18, 28}
GSTIN_RE = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")


def is_intra_state(supplier_gstin, place_of_supply_code):
    """Intra-state when the supplier's state code (first 2 GSTIN chars)
    matches the place-of-supply state code."""
    return str(supplier_gstin)[:2] == str(place_of_supply_code)


def expected_tax_method_a(taxable, rate, intra):
    """Split-first decomposition.
    Intra-state: CGST = SGST = taxable * rate / 200, IGST = 0.
    Inter-state: IGST = taxable * rate / 100.
    """
    if intra:
        half = round(taxable * rate / 200.0, 2)
        return {"cgst": half, "sgst": half, "igst": 0.0}
    return {"cgst": 0.0, "sgst": 0.0, "igst": round(taxable * rate / 100.0, 2)}


def expected_tax_method_b(taxable, rate, intra):
    """Total-first decomposition (independent of method A).
    Compute the total tax first, then halve it across CGST/SGST for intra-state.
    """
    total_tax = round(taxable * rate / 100.0, 2)
    if intra:
        half = round(total_tax / 2.0, 2)
        return {"cgst": half, "sgst": half, "igst": 0.0}
    return {"cgst": 0.0, "sgst": 0.0, "igst": total_tax}


def validate_invoice(inv):
    """Return a list of rule-violation strings for one invoice dict.
    An empty list means the invoice passes all five checks (R1-R5).
    """
    issues = []
    gstin = str(inv.get("supplier_gstin", "")).strip()
    pos = str(inv.get("place_of_supply_code", "")).strip()
    taxable = float(inv.get("taxable_value", 0) or 0)
    rate = float(inv.get("gst_rate", 0) or 0)
    cgst = float(inv.get("cgst", 0) or 0)
    sgst = float(inv.get("sgst", 0) or 0)
    igst = float(inv.get("igst", 0) or 0)
    total = float(inv.get("invoice_total", 0) or 0)
    intra = is_intra_state(gstin, pos) if len(gstin) >= 2 else False

    # R1 - GSTIN format
    if not GSTIN_RE.match(gstin):
        issues.append(f"R1 invalid GSTIN format ({gstin!r})")

    # R2 - valid GST rate
    if rate not in VALID_RATES:
        issues.append(f"R2 invalid GST rate ({rate:g}); allowed 0/5/12/18/28")

    # R3 - intra vs inter-state tax type
    if rate > 0:
        if intra and igst > 0:
            issues.append("R3 intra-state supply charged IGST (should be CGST+SGST)")
        if (not intra) and (cgst > 0 or sgst > 0):
            issues.append("R3 inter-state supply charged CGST/SGST (should be IGST)")

    # R4 - tax amounts correct (method A is the reference)
    exp = expected_tax_method_a(taxable, rate, intra)
    if intra:
        if round(cgst, 2) != exp["cgst"] or round(sgst, 2) != exp["sgst"]:
            issues.append(f"R4 CGST/SGST should each be {exp['cgst']:g} (got {cgst:g}/{sgst:g})")
    else:
        if round(igst, 2) != exp["igst"]:
            issues.append(f"R4 IGST should be {exp['igst']:g} (got {igst:g})")

    # R5 - invoice total reconciles
    expected_total = round(taxable + cgst + sgst + igst, 2)
    if round(total, 2) != expected_total:
        issues.append(f"R5 total should be {expected_total:g} (got {total:g})")

    return issues
