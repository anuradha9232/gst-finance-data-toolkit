# GST Finance Data Toolkit

A small, practical toolkit for **classifying and validating GST invoice data** in India - built from my own background keeping the books, invoicing, and maintaining GST records for a family business. It pairs a plain-English GST reference with a sample invoice register and an automated validator that catches the errors that matter.

This is here because finance and accounting is a genuine domain I know well, and clean, correctly-classified financial data is exactly what many annotation and model-evaluation projects need a domain expert for.

## What's inside

| File | What it is |
|---|---|
| [`reference/gst-classification-reference.md`](reference/gst-classification-reference.md) | GST slabs, the CGST/SGST/IGST rule, GSTIN structure, HSN/SAC, state codes |
| [`data/sample_invoice_register.csv`](data/sample_invoice_register.csv) | 15 sample invoices - 10 correct, 5 with realistic errors |
| [`validation/validation-rules.md`](validation/validation-rules.md) | The five objective checks applied to every invoice |
| [`validation/validate.py`](validation/validate.py) | Runs the rules and flags every violating row |
| [`validation/data-validation-checklist.md`](validation/data-validation-checklist.md) | The manual review checklist for a batch of invoices |

## The validator in action

```bash
python validation/validate.py
```

On the sample register it correctly flags all five seeded errors and passes the ten clean ones:

```
  INV-006:  intra-state supply charged IGST (should be CGST+SGST); CGST/SGST should each be 1080
  INV-007:  CGST/SGST should each be 900 (got 800/800)
  INV-008:  total should be 35400 (got 34000)
  INV-009:  invalid GSTIN format ('10AABCU9603R1Z', 14 chars)
  INV-010:  invalid GST rate (15%); allowed: 0/5/12/18/28

Summary: 10 clean, 5 flagged out of 15.
```

## The five checks

1. **GSTIN format** - valid 15-character GSTIN.
2. **Valid rate** - one of the real GST slabs.
3. **Tax type** - CGST+SGST for intra-state, IGST for inter-state.
4. **Tax amount** - each tax component calculated correctly.
5. **Total reconciles** - taxable value + all taxes = invoice total.

## What this shows

- Working domain knowledge of Indian GST: rates, place-of-supply rules, GSTIN structure, HSN/SAC.
- Turning domain rules into objective, automatable validation checks.
- Attention to detail and data accuracy on financial records - the core of bookkeeping and of finance-domain data work.

---

*By Anuradha Rani. The invoice data is synthetic sample data created to demonstrate the checks; it contains no real taxpayer information. The GST reference is a general guide - always confirm current rates against CBIC notifications.*
