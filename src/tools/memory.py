# ==============================================================================
# 13. COGNITIVE LATTICE & META-EVOLUTION TOOLS
# ==============================================================================

@tool("update_knowledge_graph")
async def update_knowledge_graph(subject: str, relation: str, target: str):
    """
    Maps a relationship edge in the NetworkX Relational Lattice (neural_graph.json).
    Use this to link Agents to Projects, or Missions to Outcomes.
    """
    import networkx as nx
    # Path aligned to Sovereign standard
    graph_path = DATA_DIR / "memory" / "neural_graph.json"
    
    try:
        if graph_path.exists():
            with open(graph_path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                G = nx.node_link_graph(data)
        else:
            G = nx.DiGraph()
            
        # Atomic Update
        G.add_edge(
            subject, 
            target, 
            relation=relation.upper(), 
            timestamp=datetime.now().isoformat()
        )
        
        # Save with Byte-Safe encoding
        with open(graph_path, 'w', encoding='utf-8-sig') as f:
            json.dump(nx.node_link_data(G), f, indent=2)
            
        return f"[SUCCESS] [LATTICE_SYNC]: Relationship created: {subject} --[{relation}]--> {target}"
    except Exception as e:
        logger.error(f"GRAPH_CORE_FAULT: {e}")
        return f"[ERROR] [GRAPH_ERR]: Failed to update lattice: {str(e)}"

@tool("query_knowledge_graph")
async def query_knowledge_graph(entity: str):
    """
    Traverses the neural lattice to find all upstream and downstream connections for an entity.
    Essential for 'Sovereign Colleague' context retrieval before planning.
    """
    import networkx as nx
    graph_path = DATA_DIR / "memory" / "neural_graph.json"
    
    if not graph_path.exists():
        return "⚠️ [LATTICE_EMPTY]: No relational data found on physical disk."
        
    try:
        with open(graph_path, 'r', encoding='utf-8-sig') as f:
            G = nx.node_link_graph(json.load(f))
            
        if not G.has_node(entity):
            return f"ℹ️ [PROBE_RESULT]: Node '{entity}' does not exist in the current lattice."
            
        out_edges = G.edges(entity, data=True)
        in_edges = G.in_edges(entity, data=True)
        
        results = []
        for u, v, d in out_edges:
            results.append(f"   -> [OUT]: {u} --[{d.get('relation')}]--> {v}")
        for u, v, d in in_edges:
            results.append(f"   <- [IN]:  {u} --[{d.get('relation')}]--> {v}")
            
        return f"### [NEURAL_PROBE]: {entity}\n" + "\n".join(results)
    except Exception as e:
        return f"[ERROR] [QUERY_FAIL]: {str(e)}"

@tool("self_evolve")
async def self_evolve(agent_name: str, new_skill: str):
    """
    Augments an agent's YAML manifest with a new capability.
    GOD MODE: This physically modifies the Swarm's DNA.
    """
    # Recursive search for the correct Agent YAML
    files = glob.glob(str(DATA_DIR / "agents" / "**" / "*.yaml"), recursive=True)
    target = next((f for f in files if agent_name.lower() in f.lower()), None)
    
    if not target:
        return f"[ERROR] [EVOLUTION_BLOCKED]: Manifest for {agent_name} not found."
    
    try:
        import yaml
        with open(target, 'r', encoding='utf-8-sig') as f:
            data = yaml.safe_load(f) or {}
            
        # 1. Protect Compliance Block
        prof = data.setdefault('professional', {})
        skills = prof.setdefault('skills', [])
        
        # 2. Suture New Logic
        if new_skill not in skills:
            skills.append(new_skill)
            
            # 3. Non-Destructive Save
            with open(target, 'w', encoding='utf-8-sig') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
                
            return f"[SUCCESS] [EVOLVED]: {agent_name} has mastered '{new_skill}'."
        
        return f"ℹ️ [STASIS]: {agent_name} already possesses the skill '{new_skill}'."
    except Exception as e:
        return f"[ERROR] [DNA_SUTURE_FAIL]: {str(e)}"

@tool("trigger_ingestion")
async def trigger_ingestion(target: str = "ingress"):
    """
    Dispatches a physical memory scan of either the 'ingress' folder or the 'codebase' root.
    Use this after dropping new business plans or refactoring core files.
    """
    # Map target to the v29.0 scripts we just aligned
    script_name = "ingest_knowledge.py" if target == "ingress" else "ingest_codebase.py"
    script_path = ROOT_DIR / "data" / "scripts" / script_name
    
    try:
        import subprocess
        # Async subprocess dispatch
        proc = await asyncio.create_subprocess_shell(
            f"python {script_path}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(ROOT_DIR)
        )
        return f"[SUCCESS] [INGESTION_STRIKE]: {target.upper()} scan triggered. Check Sentinel logs."
    except Exception as e:
        return f"[ERROR] [TRIGGER_FAIL]: {str(e)}"

@tool("search_memory")
async def search_memory(query: str):
    """
    Searches the Swarm's Long-Term Vector Memory (ChromaDB).
    Retrieves both technical 'Facts' and episodic 'History'.
    """
    try:
        # Lazy import to prevent circular dependency with MemoryManager
        from src.memory.engine import MemoryManager
        mem = MemoryManager()
        # Using the v25.0 'recall' logic which handles mission context
        results = await mem.recall(query, n_results=5)
        return f"### [MEMORY_LATTICE_RECALL]: '{query}'\n\n{results}"
    except Exception as e:
        return f"[ERROR] [MEMORY_RETRIEVAL_FAULT]: {str(e)}"

@tool("create_ticket")
async def create_ticket(title: str, priority: str, description: str = ""):
    """
    Logs a high-priority task into 'data/tasks.md'. 
    Forces the 'Titan Loop Controller' to consume the task in the next cycle.
    """
    try:
        # Format aligned with the Titan Loop Controller v28.6 engine
        ts = datetime.now().strftime('%Y-%m-%d %H:%M')
        # Format: | Timestamp | Priority | Type | Description | Status |
        line = f"| {ts} | {priority.upper()} | TASK | {title}: {description} | OPEN |\n"
        
        path = DATA_DIR / "tasks.md"
        
        # Ensure header exists if file is fresh
        if not path.exists():
            with open(path, "w", encoding="utf-8-sig") as f:
                f.write("| Timestamp | Priority | Type | Description | Status |\n")
                f.write("|---|---|---|---|---|\n")
                
        with open(path, "a", encoding="utf-8-sig") as f:
            f.write(line)
            
        return f"[SUCCESS] [TICKET_LOGGED]: {title} at {priority} priority."
    except Exception as e:
        return f"[ERROR] [LOG_FAULT]: {str(e)}"