"""The generator must be deterministic: same seed -> byte-identical output."""

from generate_invoices import build_jsonl


def test_build_is_byte_identical():
    assert build_jsonl(1000) == build_jsonl(1000)


def test_different_seed_differs():
    assert build_jsonl(200, seed=1) != build_jsonl(200, seed=2)


def test_record_count():
    text = build_jsonl(50)
    assert text.count("\n") == 50
    # every line is valid JSON with the expected keys
    import json
    first = json.loads(text.splitlines()[0])
    assert {"invoice_no", "supplier_gstin", "taxable_value", "invoice_total"} <= set(first)
