#!/usr/bin/env python3
"""
Tranzia Receipt Verifier
Usage: python tranzia-verify.py <receipt_file.json>

Exit Code:
  0: Verification PASSED
  1: Verification FAILED or Error
"""
import sys
import json
import hashlib

def canonical_json(obj) -> str:
    """
    Produce stable JSON string for hashing.
    Matches Tranzia Backend: Sorted keys, compact separators (no spaces), UTF-8.
    """
    return json.dumps(
        obj, 
        sort_keys=True, 
        separators=(',', ':'), 
        ensure_ascii=False,
        default=str
    )

def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def verify_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            receipt = json.load(f)
    except Exception as e:
        print(f"ERROR: Could not read file: {e}")
        return False

    # 1. Extract Integrity Block
    integrity = receipt.get("integrity")
    if not integrity:
        print("FAIL: No integrity block found.")
        return False
        
    claimed_hash = integrity.get("canonical_receipt_hash")
    if not claimed_hash:
        print("FAIL: No canonical_receipt_hash found.")
        return False
        
    print(f"Claimed Hash: {claimed_hash}")
    
    # 2. Prepare for Hashing (Blank out the hash field)
    # Important: We must modify a copy or the loaded dict in place effectively
    # to match how the backend computed it (hash = "" inside the obj)
    
    # We assume 'integrity' is a dict inside 'receipt'
    # We must set canonical_receipt_hash to "" (empty string)
    receipt["integrity"]["canonical_receipt_hash"] = ""
    
    # 3. Canonicalize
    canonical_str = canonical_json(receipt)
    
    # 4. Hash
    computed_hash = sha256_hex(canonical_str)
    print(f"Computed Hash: {computed_hash}")
    
    # 5. Compare
    if computed_hash == claimed_hash:
        print("\n✅ VERIFICATION PASSED: Receipt integrity confirmed.")
        return True
    else:
        print("\n❌ VERIFICATION FAILED: Hash mismatch.")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
        
    success = verify_file(sys.argv[1])
    sys.exit(0 if success else 1)
