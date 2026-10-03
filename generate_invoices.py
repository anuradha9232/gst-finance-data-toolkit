"""
generate_invoices.py - deterministic generator for a large invoice dataset.

Produces 2,500 correct GST invoices as JSONL. The generator is pure and
deterministic: a fixed seed, no clock, no network, so re-running it yields a
byte-identical file every time (verified by tests/test_determinism.py).

Run:  python generate_invoices.py          # writes data/invoices.jsonl
      python generate_invoices.py --count 5000 --out data/big.jsonl
"""

import argparse
import json
import os
import random

from gst_core import expected_tax_method_a, is_intra_state

SEED = 20260101
N_DEFAULT = 2500

SUPPLIER_GSTIN = "10AABCU9603R1ZM"          # a Bihar (state code 10) supplier
STATE_CODES = ["10", "27", "07", "29", "06", "24", "33", "09"]
HSN_SAC = ["8471", "6109", "1006", "8517", "9403", "8523", "3304", "9963"]
RATES = [0, 5, 12, 18, 28]


def build_jsonl(count=N_DEFAULT, seed=SEED):
    """Return the dataset as a single JSONL string (deterministic)."""
    rng = random.Random(seed)
    lines = []
    for i in range(1, count + 1):
        pos = rng.choice(STATE_CODES)
        rate = rng.choice(RATES)
        # taxable as a multiple of 1000 keeps both tax decompositions exact
        taxable = rng.randint(1, 500) * 1000
        intra = is_intra_state(SUPPLIER_GSTIN, pos)
        tax = expected_tax_method_a(taxable, rate, intra)
        total = round(taxable + tax["cgst"] + tax["sgst"] + tax["igst"], 2)
        inv = {
            "invoice_no": f"INV-{i:05d}",
            "invoice_date": f"2024-{((i - 1) % 12) + 1:02d}-15",
            "supplier_gstin": SUPPLIER_GSTIN,
            "place_of_supply_code": pos,
            "hsn_sac": rng.choice(HSN_SAC),
            "taxable_value": taxable,
            "gst_rate": rate,
            "cgst": tax["cgst"],
            "sgst": tax["sgst"],
            "igst": tax["igst"],
            "invoice_total": total,
        }
        lines.append(json.dumps(inv, sort_keys=True, ensure_ascii=True))
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Generate a deterministic invoice JSONL dataset.")
    ap.add_argument("--count", type=int, default=N_DEFAULT)
    ap.add_argument("--out", default=os.path.join("data", "invoices.jsonl"))
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    text = build_jsonl(args.count, args.seed)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"Wrote {args.count} invoices to {args.out}")


if __name__ == "__main__":
    main()
