# GST Invoice Validation Rules

The five rules the validator applies to every invoice row. Each one is objective - a row either passes or it doesn't - which is what makes the check reliable and repeatable. These mirror the manual checks I ran on invoice registers while keeping the books.

| Rule | What it checks | Fails when |
|---|---|---|
| **R1 - GSTIN format** | Supplier GSTIN is a valid 15-character GSTIN | Wrong length, or doesn't match the state-code + PAN + entity + Z + checksum pattern |
| **R2 - Valid rate** | GST rate is a real slab | Rate is not one of 0 / 5 / 12 / 18 / 28 |
| **R3 - Tax type** | Intra vs inter-state tax is correct | Intra-state supply charged IGST, or inter-state supply charged CGST/SGST |
| **R4 - Tax amount** | The tax is calculated correctly | Intra: CGST or SGST != taxable x rate / 200. Inter: IGST != taxable x rate / 100 |
| **R5 - Total reconciles** | Invoice total adds up | Total != taxable value + CGST + SGST + IGST |

## The logic behind each rule

- **R1** - A malformed GSTIN means the supplier can't be verified and input tax credit may be denied. The pattern is `^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$`.
- **R2** - A rate like 15% doesn't exist in GST; it's usually a typo for 12% or 18% and will misstate the tax.
- **R3** - Determined by comparing the place-of-supply state code with the supplier's state code (first two digits of the GSTIN). Same state -> CGST+SGST; different state -> IGST. This is the most common real-world error.
- **R4** - Intra-state splits the rate in half across CGST and SGST; inter-state applies the full rate as IGST. A mismatch here means the wrong amount of tax was charged.
- **R5** - The final arithmetic check: the total on the invoice must equal the taxable value plus all tax components. This catches data-entry slips that the other rules miss.

## Result on the sample register

Running [`validate.py`](validate.py) on [`../data/sample_invoice_register.csv`](../data/sample_invoice_register.csv) (15 invoices) flags 5:

| Invoice | Rule(s) | Problem |
|---|---|---|
| INV-006 | R3, R4 | Intra-state supply charged IGST instead of CGST+SGST |
| INV-007 | R4 | CGST/SGST understated (800 each instead of 900) |
| INV-008 | R5 | Total is 34,000 but should be 35,400 |
| INV-009 | R1 | GSTIN is only 14 characters |
| INV-010 | R2 | Rate of 15% is not a valid GST slab |

**Result: 10 clean, 5 flagged.** Each flag points to a specific rule and a specific fix.
