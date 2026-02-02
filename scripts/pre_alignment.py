import os

# PHYSICAL ANCHOR
AGENTS_DIR = "F:/RealmForge_PROD/data/agents"

# Known Department Suffixes to strip (handles single and multi-word suffixes)
DEPT_TAGS = [
    "GLOBAL_SECURITY", "CYBER_SECURITY", "DATA_INTELLIGENCE", "EXECUTIVE_BOARD",
    "PRODUCT_STRATEGY", "OPERATIONS_GENERAL", "FINANCIAL_OPS", "GENERAL_ENGINEERING",
    "LEGAL_COMPLIANCE", "MARKETING_PR", "QUALITY_ASSURANCE", "BACKEND_SYSTEMS",
    "SOFTWARE_ENGINEERING", "FRONTEND_OPS"
]

def cleanse_roles():
    print("--- [REALM FORGE: ATOMIC ROLE MANIFEST] ---")
    
    unique_roles = {} # Role Name: Occurrences

    for root, dirs, files in os.walk(AGENTS_DIR):
        for file in files:
            if not file.endswith((".yaml", ".yml")):
                continue

            # 1. Strip extension
            clean_name = file.replace(".yaml", "").replace(".yml", "")
            
            # 2. Handle "Team" utility files (e.g., global_security_team_bias_auditor)
            if "_team_" in clean_name:
                role = clean_name.split("_team_")[-1]
            
            # 3. Handle standard Agent naming convention
            else:
                parts = clean_name.split("_")
                
                # Identify how many parts are at the end (Department)
                # Note: Most of your depts have 2 parts (CYBER_SECURITY, DATA_INTELLIGENCE)
                end_idx = len(parts)
                for tag in DEPT_TAGS:
                    if clean_name.endswith(tag):
                        tag_parts_count = len(tag.split("_"))
                        end_idx = -tag_parts_count
                        break
                
                # Identify how many parts are at the beginning (Identity)
                # CYB_Apex_Bot (3 parts) vs Aric_Mercer (2 parts)
                start_idx = 0
                if parts[0].isupper() and len(parts[0]) == 3:
                    start_idx = 3 # Code-based ID
                else:
                    start_idx = 2 # Human-based name
                
                # Slice the middle (The Role)
                role_parts = parts[start_idx:end_idx]
                
                if not role_parts:
                    role = clean_name # Fallback for outliers
                else:
                    role = "_".join(role_parts)

            # De-duplicate and count
            unique_roles[role] = unique_roles.get(role, 0) + 1

    # Print results
    for role in sorted(unique_roles.keys()):
        print(f"ROLE: {role.ljust(40)} | COUNT: {unique_roles[role]}")

    print("\n--- [CLEANSE SUMMARY] ---")
    print(f"TOTAL UNIQUE ROLES: {len(unique_roles)}")

if __name__ == "__main__":
    cleanse_roles()