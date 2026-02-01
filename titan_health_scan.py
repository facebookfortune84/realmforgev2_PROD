import os
import json
from pathlib import Path

def health_check():
    root = Path("F:/RealmForge_PROD")
    print(f"--- [REALM FORGE HEALTH CHECK] ---")
    
    # 1. Physical Existence
    files_to_check = [
        "server.py",
        "realm_core.py",
        "data/roster.json",
        "src/system/arsenal/registry.py",
        "data/memory/neural_graph.json"
    ]
    
    for f in files_to_check:
        p = root / f
        status = "✅ FOUND" if p.exists() else "❌ MISSING"
        print(f"{f}: {status}")

    # 2. Roster Integrity
    roster_path = root / "data/roster.json"
    if roster_path.exists():
        try:
            with open(roster_path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                agents = data.get("roster", [])
                print(f"Roster Count: {len(agents)} Agents.")
                if len(agents) > 0:
                    print(f"Sample Agent: {agents[0].get('functional_role')} ({agents[0].get('name')})")
        except Exception as e:
            print(f"❌ ROSTER JSON CORRUPT: {e}")

    # 3. Environment Variable Check
    print(f"GITHUB_CLIENT_ID: {'SET' if os.getenv('GITHUB_CLIENT_ID') else 'MISSING'}")
    print(f"REALM_MASTER_KEY: {'SET' if os.getenv('REALM_MASTER_KEY') else 'MISSING'}")

if __name__ == "__main__":
    health_check()