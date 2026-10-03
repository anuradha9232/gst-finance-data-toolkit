#!/usr/bin/env python3
"""
solve.py - command-line GST invoice validator.

Usage:
    python3 solve.py <input.jsonl> <output.jsonl>

Reads a JSONL file of invoices (one JSON object per line), validates each one
against the GST rules in gst_core, and writes a JSONL report (one result per
line): {"invoice_no": ..., "valid": bool, "issues": [...]}.

Exit codes:
    0  ran successfully and every invoice is valid
    1  ran successfully but at least one invoice failed a rule
    2  usage or I/O error
"""

import json
import sys

from gst_core import validate_invoice


def run(input_path, output_path):
    n_total = 0
    n_invalid = 0
    with open(input_path, encoding="utf-8") as fin, \
            open(output_path, "w", encoding="utf-8", newline="\n") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            inv = json.loads(line)
            issues = validate_invoice(inv)
            n_total += 1
            if issues:
                n_invalid += 1
            result = {
                "invoice_no": inv.get("invoice_no"),
                "valid": not issues,
                "issues": issues,
            }
            fout.write(json.dumps(result, sort_keys=True, ensure_ascii=True) + "\n")
    return n_total, n_invalid


def main(argv):
    if len(argv) != 3:
        sys.stderr.write("usage: python3 solve.py <input.jsonl> <output.jsonl>\n")
        return 2
    try:
        n_total, n_invalid = run(argv[1], argv[2])
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 2
    sys.stderr.write(f"validated {n_total} invoices, {n_invalid} invalid\n")
    return 1 if n_invalid else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
