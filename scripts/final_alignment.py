import os
import json
import yaml
import math

# --- PHYSICAL ANCHORS ---
ROOT = "F:/RealmForge_PROD"
AGENTS_DIR = f"{ROOT}/data/agents"
OUTPUT_PATH = f"{ROOT}/master_departmental_lattice.json"

SILOS = [
    "Architect", "Data_Intelligence", "Software_Engineering", "DevOps_Infrastructure",
    "Cybersecurity", "Financial_Ops", "Legal_Compliance", "Research_Development",
    "Executive_Board", "Marketing_PR", "Human_Capital", "Quality_Assurance", "Facility_Management"
]

# --- THE INDUSTRIAL ROLE POOLS (Sample of the 100+ roles) ---
ROLE_POOLS = {
    "Architect": ["Sovereign_OS_Architect", "Swarm_Intelligence_Lead", "Lattice_Framework_Engineer", "Core_Systems_Designer"],
    "Data_Intelligence": ["RAG_Optimization_Lead", "Vector_Graph_Scryer", "Neural_Inference_Analyst", "Dataset_Curator"],
    "Software_Engineering": ["CUDA_Kernel_Architect", "GPU_Compiler_Specialist", "DirectX_Vulkan_Expert", "C++_Performance_Lead"],
    "DevOps_Infrastructure": ["Zero_Downtime_Sentinel", "Kubernetes_Orchestrator", "Cloud_Infrastructure_Lead", "SRE_Strike_Team"],
    "Cybersecurity": ["Malware_Forensics_Lead", "Red_Team_Commander", "Zero_Trust_Architect", "Cryptographic_Sentinel"],
    "Financial_Ops": ["AIAAS_Monetization_Lead", "Revenue_Stream_Architect", "Fiscal_Integrity_Auditor", "Burn_Rate_Strategist"],
    "Legal_Compliance": ["IronClad_Policy_Director", "IP_Defense_Counsel", "Compliance_Lattice_Auditor", "Ethics_Framework_Lead"],
    "Research_Development": ["Generative_Persona_Lead", "Experimental_LLM_Engineer", "Simulation_Environment_Designer"],
    "Executive_Board": ["Strike_Team_Commander", "Sector_Roadmap_Director", "Sovereign_Product_Visionary"],
    "Marketing_PR": ["DevRel_Growth_Hacker", "Technical_Narrative_Designer", "SEO_Virality_Strategist"],
    "Human_Capital": ["Workforce_Alignment_Lead", "Empathy_Response_Designer", "Silo_Culture_Curator"],
    "Quality_Assurance": ["Truth_Protocol_Validator", "Autonomous_Healing_Lead", "Regression_Sentinel"],
    "Facility_Management": ["Logistics_Lattice_Director", "Supply_Chain_Architect", "Inventory_Flow_Manager"]
}

# --- 180 TOOL MAPPING (Simplified for this script) ---
# We will assign tools to silos based on the first character to ensure balance
ALL_TOOLS = ["analyze_contract_risk", "analyze_http_security_headers", "analyze_sentiment_advanced", "analyze_seo_tags", "analyze_stock_technicals", "analyze_virality_score", "append_to_file", "apply_text_template", "archive_workspace", "ask_human", "assign_swarm_task", "audit_python_dependencies", "autonomous_readiness_fix", "backup_memory_db", "base64_decode", "base64_encode", "calculate_burn_rate", "calculate_file_hash", "calculate_readability_score", "check_port_availability", "check_robots_txt", "check_server_fingerprint", "check_site_availability", "compare_text_diff", "compress_workspace_assets", "consolidate_memory_dream", "convert_case_style", "convert_csv_to_markdown_table", "convert_currency", "convert_json_to_yaml", "convert_markdown_to_html", "convert_yaml_to_json", "copy_internal_file", "count_tokens_estimate", "count_word_frequency_map", "craft_persuasive_copy", "create_business_card_qr", "create_calendar_event_ics", "create_client_workspace", "create_customer_support_script", "create_investor_deck", "create_qr_code", "create_ticket", "csv_processor_read", "csv_processor_write", "deduplicate_lines", "delete_memory_by_id", "delete_workspace_file", "deobfuscate_sensitive_text", "detect_language_heuristic", "detect_log_anomalies", "detect_pii_in_file", "detect_social_engineering", "discord_voice_broadcast", "dispatch_corporate_email", "dns_lookup_records", "download_file", "duplicate_agent", "extract_code_blocks", "extract_emails_from_text", "extract_keywords_frequency", "extract_mentions_hashtags", "extract_named_entities_heuristic", "format_newsletter_html", "generate_corporate_document", "generate_corporate_invoice", "generate_dockerfile", "generate_hash_wordlist", "generate_industrial_image", "generate_industrial_video", "generate_lorem_ipsum", "generate_mermaid_diagram", "generate_meta_tags", "generate_nda_contract", "generate_negotiation_strategy", "generate_persona_profile", "generate_press_release", "generate_project_budget", "generate_random_user_agent", "generate_security_policy", "generate_sms_alert", "generate_social_media_bundle", "generate_strong_password", "generate_svg_badge", "generate_url_slug", "generate_uuid", "get_crypto_price", "get_directory_tree", "get_domain_whois", "get_env_info", "get_file_metadata", "get_market_intelligence", "get_sector_roster", "get_stock_history_csv", "get_system_vitals", "graph_centrality_analysis", "graph_find_path", "grep_files", "hash_file_integrity", "industrial_data_ingress", "inject_new_capability", "inspect_agent_manifest", "inspect_api_schema", "interact_web", "ip_geolocation", "lattice_scout_search", "list_available_voices", "list_files", "list_workspace_files", "merge_csv_files", "minify_js_css", "mm_add_user_to_channel", "mm_add_user_to_team", "mm_create_channel", "mm_get_channel_history", "mm_get_user_by_name", "mm_join_channel", "move_internal_file", "obfuscate_email_address", "obfuscate_sensitive_text", "optimize_llm_prompt", "parse_log_file", "parse_query_params", "port_scan_local", "push_to_github", "query_knowledge_graph", "read_excel_file", "read_file", "read_from_workspace", "read_json_config", "regex_replace_in_file", "repair_broken_json", "replace_text_in_file", "run_terminal_command", "sanitize_input_text", "scaffold_commercial_website", "scaffold_flask_api", "scaffold_industrial_project", "scaffold_react_component", "scan_code_for_vulnerabilities", "scan_network_ports", "scrape_url_to_markdown", "search_memory", "self_evolve", "semantic_code_search", "send_direct_notification", "send_discord_webhook", "send_slack_webhook", "simulate_conversation_turn", "simulate_phishing_email", "spawn_autonomous_agent", "spawn_ephemeral_agent", "sqlite_create_table_v2", "sqlite_insert", "sqlite_inspect_schema", "sqlite_query", "strip_html_tags", "summarize_text_simple", "sync_repository", "system_auto_heal", "take_website_screenshot", "text_to_ascii_table", "translate_text_simulation", "transmit_workforce_message", "trigger_ingestion", "unzip_file", "update_knowledge_graph", "validate_agent_alignment", "validate_email_list", "validate_jwt_structure", "validate_phone_number", "validate_python_syntax", "verify_ssl_certificate", "web_search_duckduckgo", "web_search_news", "wrap_text_lines", "write_csv_report", "write_file", "write_to_workspace", "zip_directory"]

def execute_renormalization():
    print("--- [REALM FORGE: SOVEREIGN RE-NORMALIZATION] ---")
    
    # 1. Collect all existing files
    all_files = []
    for root, _, files in os.walk(AGENTS_DIR):
        for f in files:
            if f.endswith((".yaml", ".yml")):
                all_files.append(os.path.join(root, f))
    
    total_agents = len(all_files)
    agents_per_silo = math.ceil(total_agents / len(SILOS))
    
    lattice = {silo: {"agents": [], "tools": []} for silo in SILOS}
    
    # 2. Assign Tools to Silos for balance
    for i, tool in enumerate(ALL_TOOLS):
        silo_idx = i % len(SILOS)
        lattice[SILOS[silo_idx]]["tools"].append(tool)

    # 3. Physically Move, Rename, and Update Agents
    file_idx = 0
    for silo in SILOS:
        # Create physical directory
        silo_path = os.path.join(AGENTS_DIR, silo.lower())
        os.makedirs(silo_path, exist_ok=True)
        
        for i in range(agents_per_silo):
            if file_idx >= total_agents: break
            
            old_path = all_files[file_idx]
            role = ROLE_POOLS[silo][i % len(ROLE_POOLS[silo])]
            new_filename = f"{silo}_{role}_{file_idx}.yaml"
            new_path = os.path.join(silo_path, new_filename)
            
            # Update Internal YAML
            try:
                with open(old_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or {}
                
                # Standardize Identity & Professional
                if 'identity' not in data: data['identity'] = {}
                if 'professional' not in data: data['professional'] = {}
                
                data['identity']['full_name'] = f"Prime_{silo}_{file_idx}"
                data['professional']['functional_role'] = role
                data['professional']['department'] = silo.upper()
                data['professional']['tools_assigned'] = lattice[silo]["tools"]
                
                # Write back to the NEW path
                with open(new_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f)
                
                # Add to Lattice
                lattice[silo]["agents"].append({
                    "name": data['identity']['full_name'],
                    "role": role,
                    "path": new_path.replace("\\", "/")
                })
                
                # Delete the old file if it was moved/renamed
                if old_path != new_path and os.path.exists(old_path):
                    os.remove(old_path)
                    
            except Exception as e:
                print(f"[!] Error processing {old_path}: {e}")
            
            file_idx += 1

    # 4. Final Save of Lattice JSON
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(lattice, f, indent=4)

    print("\n" + "="*50)
    print(" SOVEREIGN RENORMALIZATION REPORT")
    print("="*50)
    for s in SILOS:
        print(f"{s:<25} | {len(lattice[s]['agents']):<4} Agents | {len(lattice[s]['tools']):<3} Tools")
    print("="*50)
    print(f"TOTAL FILES PROCESSED: {file_idx}")

if __name__ == "__main__":
    execute_renormalization()