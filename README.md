# GST Finance Data Toolkit

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Domain-GST%20(India)-1F4E78?style=flat-square" alt="GST Domain" />
  <img src="https://img.shields.io/badge/Tests-pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white" alt="pytest" />
  <img src="https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://github.com/anuradha9232/gst-finance-data-toolkit/actions/workflows/ci.yml/badge.svg" alt="CI" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License MIT" />
</p>

A small, practical toolkit for **classifying and validating GST invoice data** in India - built from my own background keeping the books, invoicing, and maintaining GST records for a family business. It pairs a plain-English GST reference with sample data and an automated validator that catches the errors that matter.

It comes in two layers:

- a **domain layer** - a GST reference and a CSV invoice register, for reading and manual review;
- an **engineering layer** - a containerized command-line validator with a deterministic data generator, a pytest suite, and continuous integration, so the checks are reproducible and run the same way on any machine.

This is here because finance and accounting is a genuine domain I know well, and clean, correctly-classified financial data - produced and checked by repeatable tooling - is exactly what many annotation and model-evaluation projects need a domain expert for.

## Quick start

```bash
# 1. generate a deterministic dataset of 2,500 correct invoices (JSONL)
python generate_invoices.py                 # writes data/invoices.jsonl

# 2. validate any JSONL invoice file from the command line
python solve.py data/invoices.jsonl report.jsonl
#   exit 0 = every invoice valid, 1 = at least one failed a rule, 2 = usage/IO error

# 3. run the test suite
pip install -r requirements.txt
pytest -q
```

### Run it in Docker

No Python setup needed - the validator ships as a container:

```bash
docker build -t gst-validator .
docker run --rm -v "$PWD/data":/data gst-validator /data/invoices.jsonl /data/report.jsonl
```

## What's inside

| Path | What it is |
|---|---|
| [`gst_core.py`](gst_core.py) | The validation rules and two independent tax calculations |
| [`generate_invoices.py`](generate_invoices.py) | Deterministic JSONL generator (fixed seed, byte-identical output) |
| [`solve.py`](solve.py) | Command-line validator with well-defined exit codes |
| [`Dockerfile`](Dockerfile) | Container image for the validator |
| [`tests/`](tests) | pytest suite: rules, CLI, determinism, cross-validation |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | CI: tests, reproducibility check, and a Docker build on every push |
| [`reference/gst-classification-reference.md`](reference/gst-classification-reference.md) | GST slabs, the CGST/SGST/IGST rule, GSTIN structure, HSN/SAC, state codes |
| [`data/sample_invoice_register.csv`](data/sample_invoice_register.csv) | 15 sample invoices - 10 correct, 5 with realistic errors |
| [`validation/validate.py`](validation/validate.py) | The original CSV validator over the sample register |

## The five checks

1. **GSTIN format** - valid 15-character GSTIN.
2. **Valid rate** - one of the real GST slabs (0 / 5 / 12 / 18 / 28).
3. **Tax type** - CGST+SGST for intra-state, IGST for inter-state.
4. **Tax amount** - each tax component calculated correctly.
5. **Total reconciles** - taxable value + all taxes = invoice total.

## How the ground truth is checked twice

The tax for an invoice can be worked out two different ways: split the rate first
(CGST = SGST = taxable x rate / 200), or compute the total tax first and halve it.
Both must give the same answer. [`gst_core.py`](gst_core.py) implements both, and
[`tests/test_crosscheck.py`](tests/test_crosscheck.py) asserts they agree across
every rate and a wide range of taxable values - an independent cross-validation of
the ground truth, so a mistake in one method can't slip through unnoticed.

## The CSV validator in action

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

## What this shows

- Working domain knowledge of Indian GST: rates, place-of-supply rules, GSTIN structure, HSN/SAC.
- Turning domain rules into objective, automatable validation checks.
- Building those checks into reproducible tooling: a deterministic generator, a tested command-line program, a Docker image, and CI that runs it all on every push.
- Attention to detail and data accuracy on financial records - the core of bookkeeping and of finance-domain data work.

---

*By Anuradha Rani. The invoice data is synthetic sample data created to demonstrate the checks; it contains no real taxpayer information. The GST reference is a general guide - always confirm current rates against CBIC notifications.*
