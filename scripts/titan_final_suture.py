"""
REALM FORGE: FINAL SOVEREIGN SUTURE v1.1
PURPOSE: Collects missing src/ modules and repairs broken ".." import syntax.
"""
import os
import shutil
import re
from pathlib import Path

# --- CONFIGURATION ---
OLD_ROOT = Path("F:/RealmForge")
NEW_ROOT = Path("F:/RealmForge_PROD")

MISSING_SRC = ["memory", "core", "components", "utils", "tools"]

def final_suture():
    print("🧵 [SUTURE] Starting final logic alignment...")

    # 1. MOVE SCRAGGLER MODULES
    for mod in MISSING_SRC:
        src_path = OLD_ROOT / "src" / mod
        dst_path = NEW_ROOT / "src" / mod
        if src_path.exists() and not dst_path.exists():
            print(f"📦 Moving missing module: src/{mod}")
            shutil.copytree(src_path, dst_path)

    # 2. ENSURE STATE.PY IS ALIGNED
    state_src = OLD_ROOT / "src" / "system" / "state.py"
    state_dst = NEW_ROOT / "src" / "system" / "state.py"
    if state_src.exists() and not state_dst.exists():
        print("📄 Moving src/system/state.py")
        shutil.copy2(state_src, state_dst)

    # 3. SURGICAL IMPORT REPAIR
    print("💉 Repairing broken import syntax...")
    for py_file in NEW_ROOT.rglob("*.py"):
        try:
            content = py_file.read_text(encoding='utf-8', errors='ignore')
            
            # Fix the "Double Dot" disaster
            original = content
            # Pattern 1: from src.memory -> from src.memory
            content = content.replace("from src.memory", "from src.memory")
            # Pattern 2: from src.memory -> from src.memory
            content = content.replace("from src.memory", "from src.memory")
            # Pattern 3: from src.auth -> from src.auth
            content = content.replace("from src.auth", "from src.auth")
            # Pattern 4: General system-relative fix
            content = content.replace("from src.system", "from src.system")
            
            if content != original:
                py_file.write_text(content, encoding='utf-8')
                print(f"✅ Healed imports in: {py_file.relative_to(NEW_ROOT)}")
        except Exception as e:
            print(f"⚠️ Skip {py_file.name}: {e}")

    print("\n" + "="*60)
    print("💎 FINAL SUTURE COMPLETE")
    print("Logic Modules: src/ (memory, core, tools, utils, system) aligned.")
    print("Ready for Gateway Ignition.")
    print("="*60)

if __name__ == "__main__":
    final_suture()