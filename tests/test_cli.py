"""End-to-end tests for the solve.py command-line validator."""

import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOLVE = os.path.join(REPO, "solve.py")

GOOD = {
    "invoice_no": "INV-1", "supplier_gstin": "10AABCU9603R1ZM",
    "place_of_supply_code": "10", "taxable_value": 10000, "gst_rate": 18,
    "cgst": 900, "sgst": 900, "igst": 0, "invoice_total": 11800,
}
BAD = dict(GOOD, invoice_no="INV-2", invoice_total=12000)   # R5 total mismatch


def _write(path, rows):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    return str(path)


def _read(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def test_cli_all_valid_exit_0(tmp_path):
    inp = _write(tmp_path / "in.jsonl", [GOOD])
    out = str(tmp_path / "out.jsonl")
    r = subprocess.run([sys.executable, SOLVE, inp, out])
    assert r.returncode == 0
    res = _read(out)
    assert res[0]["valid"] is True and res[0]["issues"] == []


def test_cli_flags_invalid_exit_1(tmp_path):
    inp = _write(tmp_path / "in.jsonl", [GOOD, BAD])
    out = str(tmp_path / "out.jsonl")
    r = subprocess.run([sys.executable, SOLVE, inp, out])
    assert r.returncode == 1
    res = _read(out)
    assert res[0]["valid"] is True
    assert res[1]["valid"] is False
    assert any(i.startswith("R5") for i in res[1]["issues"])


def test_cli_usage_error_exit_2():
    r = subprocess.run([sys.executable, SOLVE])
    assert r.returncode == 2
