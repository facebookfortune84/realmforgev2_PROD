import json
import os
import yaml
from pathlib import Path

def suture_industrial_data():
    root = Path("F:/RealmForge_PROD")
    roster_path = root / "data" / "roster.json"
    map_path = root / "data" / "industrial_capability_map.json"
    agents_dir = root / "data" / "agents"
    
    print("\n" + "⚙️"*30)
    print("--- [REALM FORGE: MASTER DATA SUTURE v2.0] ---")
    print(f"TARGET ROOT: {root}")

    # Canonical 13 Sectors for normalization
    sectors = [
        "software_engineering", "cyber_security", "data_intelligence", 
        "devops_infrastructure", "financial_ops", "legal_compliance", 
        "research_development", "executive_board", "marketing_pr", 
        "human_capital", "quality_assurance", "facility_management", 
        "general_engineering"
    ]

    capability_map = {s.upper(): [] for s in sectors}
    master_roster = []
    total_yaml_processed = 0

    # 1. PHYSICAL YAML CRAWL (The Truth Protocol)
    print(">>> Phase 1: Physical Manifest Ingestion...")
    for sector in sectors:
        sector_dir = agents_dir / sector
        if not sector_dir.exists():
            continue
            
        for yaml_file in sector_dir.glob("*.yaml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    manifest = yaml.safe_load(f)
                
                if not manifest: continue
                
                # Extract Data from YAML Schema v14.3
                identity = manifest.get("identity", {})
                pro = manifest.get("professional", {})
                sys_meta = manifest.get("system_metadata", {})
                
                full_name = identity.get("full_name", "Unknown_Agent")
                f_role = pro.get("functional_role", "Industrial_Specialist")
                assigned_tools = pro.get("tools_assigned", [])
                dept = pro.get("department", sector.upper()).upper()
                
                # Normalize Department for Map
                if dept not in capability_map:
                    dept = next((s.upper() for s in sectors if s.upper() in dept), "GENERAL_ENGINEERING")

                # Physical Entry for industrial_capability_map.json
                agent_entry = {
                    "name": full_name,
                    "functional_role": f_role,
                    "path": str(yaml_file).replace("\\", "/"),
                    "tools": assigned_tools,
                    "god_mode": sys_meta.get("god_mode_enabled", False)
                }
                capability_map[dept].append(agent_entry)

                # Metadata Entry for roster.json (UI Support)
                master_roster.append({
                    "name": f_role, # HUD strictly uses name slot for role mapping
                    "display_name": f_role.replace("_", " "),
                    "real_name": full_name,
                    "dept": dept,
                    "id": identity.get("employee_id", f"GEN-{uuid.uuid4().hex[:4].upper()}"),
                    "skills": pro.get("skills", []),
                    "status": "ONLINE"
                })
                
                total_yaml_processed += 1
            except Exception as e:
                print(f"⚠️  Skip {yaml_file.name}: {e}")

    # 2. ALIAS INJECTION (Brain Routing Support)
    print(">>> Phase 2: Lattice Logic Aliasing...")
    # These keys ensure the supervisor_node in realm_core.py v31.7 always finds a lead
    capability_map["SILICON_ARCHITECT"] = capability_map.get("SOFTWARE_ENGINEERING", [])
    capability_map["DATA_LATTICE_CURATOR"] = capability_map.get("DATA_INTELLIGENCE", [])
    capability_map["ZERO_TRUST_SENTINEL"] = capability_map.get("CYBER_SECURITY", [])

    # 3. PHYSICAL COMMIT: industrial_capability_map.json
    with open(map_path, 'w', encoding='utf-8') as f:
        json.dump(capability_map, f, indent=2)
    print(f"✅ Map Finalized: {len(capability_map)} Sectors Linked.")

    # 4. PHYSICAL COMMIT: roster.json
    with open(roster_path, 'w', encoding='utf-8') as f:
        json.dump({
            "roster": master_roster, 
            "alignment": "NVIDIA_CORPORATE_V1",
            "last_suture": datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"✅ Roster Finalized: {len(master_roster)} Physical Agents Sutured.")
    print(f"Total Physical Shards Processed: {total_yaml_processed}")
    print("--- [SUTURE COMPLETE: LATTICE SYNCHRONIZED] ---")
    print("⚙️"*30 + "\n")

if __name__ == "__main__":
    import uuid
    from datetime import datetime
    suture_industrial_data()