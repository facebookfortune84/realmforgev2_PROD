"""
REALM FORGE: NVIDIA-TIER ROLE SYNC v3.0
PURPOSE: Aligns 1,113 agents to an industrial corporate hierarchy.
EFFECT: Agents physically gain functional_roles recognized by the Brain.
"""
import os, json, yaml
from pathlib import Path

ROOT = Path("F:/RealmForge_PROD")
AGENT_DIR = ROOT / "data" / "agents"
ROSTER_PATH = ROOT / "data" / "roster.json"

# NVIDIA-SPECIFIC INDUSTRIAL ROLE HIERARCHY
NVIDIA_ROLE_HIERARCHY = {
    "software_engineering": [
        "CUDA_Kernel_Architect", "GPU_Compiler_Engineer", "AI_System_Integrator", 
        "C++_Performance_Specialist", "DirectX_Vulkan_Expert", "Embedded_Software_Lead"
    ],
    "cyber_security": [
        "Product_Security_Architect", "Cloud_Infrastructure_RedTeamer", "Cryptography_Consultant",
        "Zero_Trust_Sentinel", "Forensic_Threat_Analyst", "Compliance_Security_Officer"
    ],
    "data_intelligence": [
        "DL_Dataset_Curator", "NLP_Inference_Scientist", "Big_Data_Pipelines_Manager",
        "RAG_Lattice_Architect", "Generative_AI_Strategist", "Neural_Optimization_Specialist"
    ],
    "research_development": [
        "Computer_Vision_Researcher", "LLM_Training_Engineer", "HPC_Algorithm_Designer",
        "Autonomous_Machine_Scientist", "Tensor_Core_Architect", "Scientific_Computing_Specialist"
    ],
    "financial_ops": [
        "Revenue_Operations_Strategist", "Fiscal_Burn_Analyst", "AIAAS_Pricing_Architect",
        "Monetization_Ledger_Auditor", "Industrial_Contracts_Estimator", "FinTech_Flow_Optimizer"
    ],
    "executive_board": [
        "ForgeMaster_Chief_Orchestrator", "Sector_Strike_Team_Lead", "Operational_Efficiency_VP",
        "Product_Visionary_Director", "Sovereign_OS_Chief_Architect"
    ],
    "marketing_pr": [
        "Technical_Content_Strategist", "Brand_Narrative_WordSmith", "DevRel_Advocate",
        "Industrial_Outreach_Lead", "Product_Communication_Designer", "AIAAS_Market_Evangelist"
    ]
}

def sync_nvidia_roles():
    print("🚀 [ROLE_MASTERY]: Initiating NVIDIA Industrial Pivot for 1,113 Agents...")
    new_roster = []
    
    # 1. Walk every sector folder
    for sector_folder in AGENT_DIR.iterdir():
        if not sector_folder.is_dir(): continue
        
        sector_name = sector_folder.name
        # Find corresponding role pool from NVIDIA map, or default to generalist
        role_pool = NVIDIA_ROLE_HIERARCHY.get(sector_name, [f"{sector_name.capitalize()}_Technical_Specialist"])
        
        agent_files = list(sector_folder.glob("*.yaml"))
        print(f"📦 Sector [{sector_name}]: Syncing {len(agent_files)} agents.")

        for i, f in enumerate(agent_files):
            try:
                # 2. Read Agent DNA
                with open(f, 'r', encoding='utf-8-sig') as stream:
                    dna = yaml.safe_load(stream)
                if not dna: continue

                # 3. Assign Role (Cycling through pool to ensure variety across 1k agents)
                functional_role = role_pool[i % len(role_pool)]
                
                # 4. SURGICAL YAML UPDATE
                dna['professional']['functional_role'] = functional_role
                dna['professional']['department'] = sector_name.upper()
                
                with open(f, 'w', encoding='utf-8-sig') as stream:
                    yaml.dump(dna, stream, sort_keys=False, allow_unicode=True)

                # 5. ROSTER COLLECTION
                new_roster.append({
                    "name": dna['identity'].get('full_name'),
                    "functional_role": functional_role,
                    "dept": sector_name.upper(),
                    "id": dna['identity'].get('employee_id'),
                    "skills": dna['professional'].get('skills', []),
                    "status": "ONLINE"
                })
            except Exception as e:
                print(f"⚠️ Failed to sync {f.name}: {e}")

    # 6. COMMIT ROSTER TO LATTICE
    with open(ROSTER_PATH, 'w', encoding='utf-8-sig') as f:
        json.dump({"roster": new_roster, "alignment": "NVIDIA_CORPORATE_V1"}, f, indent=2)

    print(f"\n💎 [ALIGNMENT_COMPLETE]: {len(new_roster)} Agents now stationed in industrial silos.")
    print("HUD and Brain are now functionally synchronized.")

if __name__ == "__main__":
    sync_nvidia_roles()