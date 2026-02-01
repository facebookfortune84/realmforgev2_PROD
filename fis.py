import os
import sys
import importlib.util
from pathlib import Path

def check_syntax(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            compile(f.read(), file_path, 'exec')
        return True, "NOMINAL"
    except Exception as e:
        return False, str(e)

def run_integrity_scan():
    root = Path("F:/RealmForge_PROD")
    critical_files = [
        "server.py", 
        "realm_core.py", 
        "src/system/arsenal/registry.py",
        "src/system/state.py"
    ]
    
    print(f"\n--- [REALM FORGE INTEGRITY SCAN] ---")
    all_clear = True
    
    for f_path in critical_files:
        full_path = root / f_path
        if not full_path.exists():
            print(f"❌ FATAL: {f_path} is MISSING from disk.")
            all_clear = False
            continue
            
        is_valid, msg = check_syntax(full_path)
        if is_valid:
            print(f"✅ {f_path.ljust(30)} | SYNTAX: OK")
        else:
            print(f"💥 {f_path.ljust(30)} | SYNTAX ERROR: {msg}")
            all_clear = False

    # Check Env
    if not (root / ".env").exists():
        print(f"⚠️  WARNING: .env is missing. Server will fail.")
        all_clear = False

    print(f"--- [SCAN COMPLETE: {'READY FOR IGNITION' if all_clear else 'REPAIRS NEEDED'}] ---\n")

if __name__ == "__main__":
    run_integrity_scan()