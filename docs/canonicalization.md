# Canonicalization & Hashing Rules

To verify a Tranzia Decision Receipt, you must reproduce the `integrity.canonical_receipt_hash`. This document defines the exact algorithm.

## 1. Zero Out the Hash
The receipt you receive contains the hash itself inside `integrity.canonical_receipt_hash`. 
To verify, you must temporarily set this field to an empty string `""` before hashing.

**Example:**
```json
// Before Hashing
{
  ...
  "integrity": {
    "canonical_receipt_hash": "",
    "hash_alg": "sha256"
  }
}
```

## 2. Canonical JSON Serialization
We use a strict subset of JSON to ensure identical byte streams across languages.

**Rules:**
1. **UTF-8 Encoding**: The output must be valid UTF-8.
2. **Sorted Keys**: Object keys must be sorted methodically (A-Z).
3. **Compact Separators**: 
   - No spaces after colons (`:`).
   - No spaces after commas (`,`).
   - Example: `{"a":1,"b":2}` NOT `{"a": 1, "b": 2}`.
4. **No Float formatting weirdness**: Ideally stick to standard JSON representations.

**Python Implementation:**
```python
import json

def canonical_json(obj) -> str:
    return json.dumps(
        obj, 
        sort_keys=True, 
        separators=(',', ':'), 
        ensure_ascii=False,
        default=str
    )
```

**JavaScript Implementation:**
```javascript
const canonicalJson = (obj) => JSON.stringify(obj, Object.keys(obj).sort()); 
// Note: JS JSON.stringify is usually compact by default, but key sorting requires manual intervention or a library like 'stable-stringify'.
```

## 3. Hashing
Compute the SHA-256 hash of the canonical string. Return as a lowercase hex string.

`hash = sha256_hex(canonical_string)`

## Verification Success
If your computed hash matches the `X-Receipt-Hash` header (or the original `integrity.canonical_receipt_hash` from the receipt), the data is pristine.
