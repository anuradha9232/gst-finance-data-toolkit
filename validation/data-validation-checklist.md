# Invoice Data Validation Checklist

A manual checklist for reviewing a batch of GST invoices before they're trusted — for filing, for reporting, or as labeled data for a model. The automated rules in [`validation-rules.md`](validation-rules.md) cover the arithmetic; this checklist covers the judgement calls a person still has to make.

## Per-invoice checks

- [ ] **GSTIN present and 15 characters** for the supplier (and customer, if B2B).
- [ ] **GSTIN state code matches** the supplier's registered state.
- [ ] **Invoice number** is present and follows a consistent series (no gaps that suggest a missing invoice).
- [ ] **Invoice date** is valid and within the correct return period.
- [ ] **HSN/SAC code** is present and consistent with the item described.
- [ ] **GST rate** is a valid slab (0 / 5 / 12 / 18 / 28, or a special rate where applicable) and matches the HSN/SAC.
- [ ] **Tax type is correct:** CGST+SGST for intra-state, IGST for inter-state, based on place of supply.
- [ ] **Tax amounts are correct:** each of CGST/SGST = taxable × rate ÷ 200; IGST = taxable × rate ÷ 100.
- [ ] **Invoice total reconciles:** taxable value + all tax components = total.

## Batch-level checks

- [ ] **No duplicate invoice numbers** in the register.
- [ ] **Taxable value totals** match the source system (the control total).
- [ ] **Tax totals by type** (CGST, SGST, IGST) match the summary used for the return.
- [ ] **Place-of-supply distribution** looks reasonable (a sudden spike in one state may indicate a coding error).
- [ ] **Outliers reviewed:** unusually large invoices or unusual rates checked by hand.

## What to do with a flagged invoice

1. **Identify the rule it broke** (R1–R5) and the specific field.
2. **Trace it back to the source document** — the error is usually data entry, not the underlying invoice.
3. **Correct and re-run** the validation so the register is clean end to end.
4. **If the same error recurs**, fix it at the source (the template or process), not just the one row.

That last point is the difference between checking data and *improving* the process that produces it — the same mindset as tightening annotation guidelines when annotators disagree.
