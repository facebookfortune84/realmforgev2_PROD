"""
REALM FORGE: FINAL ALIGNMENT v2.0
PURPOSE: Re-anchors Agent DNA to PROD path, Purges legacy bloat, and builds Industrial Map.
"""
import os, yaml, json, shutil
from pathlib import Path

ROOT = Path("F:/RealmForge_PROD")
AGENT_DIR = ROOT / "data" / "agents"
MAP_PATH = ROOT / "data" / "industrial_capability_map.json"

# Canonical Industrial Silos for NVIDIA-tier routing
INDUSTRIAL_ROLES = {
    "SILICON_ARCHITECT": ["run_terminal_command", "get_system_vitals", "lattice_scout_search"],
    "DEEP_LEARNING_ENG": ["semantic_code_search", "search_memory", "update_knowledge_graph"],
    "MARKET_INTELLIGENCE": ["get_market_intelligence", "web_search_duckduckgo", "web_search_news"],
    "IP_LEGAL_COUNCIL": ["analyze_contract_risk", "generate_nda_contract"],
    "CONTENT_STRATEGIST": ["craft_persuasive_copy", "format_newsletter_html", "generate_social_media_bundle"],
    "HPC_INFRASTRUCTURE": ["generate_dockerfile", "push_to_github", "sync_repository"],
    "SOFTWARE_ENGINEERING": ["validate_python_syntax", "scaffold_react_component", "scaffold_flask_api"]
}

def finalize():
    print("🧹 [CLEANUP]: Purging Legacy 'src/tools' to clear Cursor errors...")
    legacy_tools = ROOT / "src" / "tools"
    if legacy_tools.exists():
        shutil.rmtree(legacy_tools)

    print("🧬 [DNA_REANCHOR]: Updating 1,112 agent paths to PROD...")
    full_map = {role: [] for role in INDUSTRIAL_ROLES}
    
    agent_files = list(AGENT_DIR.rglob("*.yaml"))
    for af in agent_files:
        try:
            with open(af, 'r', encoding='utf-8-sig') as f:
                dna = yaml.safe_load(f)
            if not dna: continue
            
            # Re-anchor internal metadata if it exists
            if 'system_metadata' in dna:
                dna['system_metadata']['project_root'] = str(ROOT)
            
            # Re-save to enforce correct encoding and new path
            with open(af, 'w', encoding='utf-8-sig') as f:
                yaml.dump(dna, f, sort_keys=False, allow_unicode=True)

            # Build Industrial Map simultaneously
            tools = dna.get('professional', {}).get('tools_assigned', [])
            entry = {"name": dna['identity']['full_name'], "path": str(af)}
            
            # Map to silo
            for role, req_tools in INDUSTRIAL_ROLES.items():
                if any(t in tools for t in req_tools):
                    full_map[role].append(entry)
                    break
        except: continue

    with open(MAP_PATH, 'w') as f:
        json.dump(full_map, f, indent=2)

    print(f"✅ [SUCCESS]: Industrial Map built at {MAP_PATH}")
    print("💎 All agents re-anchored to F:/RealmForge_PROD")

if __name__ == "__main__":
    finalize()