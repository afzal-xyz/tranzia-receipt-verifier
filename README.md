# Tranzia Receipt Verifier

**Verify Tranzia Decision Receipts offline to prove integrity.**

This repository contains the standalone tools to verify that a "Decision Receipt" issued by the Tranzia B2B Safety Platform has not been tampered with.

## What is this?
Tranzia issues "Defensible Decision Receipts" (audit logs) for every safety risk assessment. These receipts are cryptographically hashed at the time of creation.
This tool allows you to take any exported receipt (JSON) and re-compute its hash to prove:
1. **Integrity**: Detects tampering after issuance (hash mismatch).
2. **Provenance (current)**: Receipts are retrieved from Tranzia over HTTPS/TLS and include a stable hash (ETag / X-Receipt-Hash).
3. **Provenance (future)**: Optional digital signatures will enable offline origin verification independent of transport.
4. **Resilience**: You can verify this forever, even without Tranzia servers.

## Threat Model
This tool detects tampering after export.
It does not prevent a malicious party from fabricating a receipt unless digital signatures are enabled (planned feature).

## Specs
- **Spec version**: Decision Receipt v1.0
- **Verifier release**: v1.0.1

## Quick Start
### 1. Requirements
- Python 3.6+

### 2. Verify an Example
Run the verifier on the included example receipt:
```bash
python tools/tranzia-verify.py examples/receipt_example_v1.json
```

**Expected Output:**
```
Claimed Hash: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
Computed Hash: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

✅ VERIFICATION PASSED: Receipt integrity confirmed.
```

### 3. Verify Your Own Receipt
Export a receipt from the Tranzia API or Dashboard (JSON format) and run:
```bash
python tools/tranzia-verify.py path/to/your_receipt.json
```

## How It Works
See [Canonicalization Rules](docs/canonicalization.md) for the exact hashing specification.

## Schemas
- [Decision Receipt V1 Schema](schemas/decision-receipt-v1.schema.json)
