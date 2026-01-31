import os, yaml, json
from pathlib import Path

def sync():
    root = Path("F:/RealmForge_PROD")
    agent_dir = root / "data" / "agents"
    roster_path = root / "data" / "roster.json"
    
    print("📋 [SYNC] Re-indexing 1,112 Agents into sectors...")
    new_roster = []
    
    # Walk the subfolders we created during the move
    for af in agent_dir.rglob("*.yaml"):
        try:
            with open(af, 'r', encoding='utf-8-sig') as f:
                dna = yaml.safe_load(f)
            if dna:
                new_roster.append({
                    "name": dna['identity'].get('full_name'),
                    "role": dna['professional'].get('role_title'),
                    "dept": dna['professional'].get('department'),
                    "id": dna['identity'].get('employee_id'),
                    "status": "ONLINE"
                })
        except: continue

    with open(roster_path, 'w', encoding='utf-8-sig') as f:
        json.dump({"roster": new_roster}, f, indent=2)
    print(f"✅ [SUCCESS]: {len(new_roster)} agents synced in PROD.")

if __name__ == "__main__":
    sync()