"""
REALM FORGE: LATTICE FUSION ENGINE v3.0 (HASH-AWARE)
ARCHITECT: LEAD SWARM ENGINEER
STATUS: PRODUCTION READY - FULL FIDELITY RECONSTRUCTION
PATH: F:/RealmForge_PROD/ingest_repo.py
"""

import os
import json
import hashlib
import time
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# --- INTERNAL MODULES ---
from src.memory.engine import MemoryManager

# --- CONFIGURATION ---
ROOT = Path("F:/RealmForge_PROD")
GRAPH_PATH = ROOT / "data" / "memory" / "neural_graph.json"
INVENTORY_PATH = ROOT / "data" / "memory" / "inventory_report.json"
EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".next", "dist", "venv", "forge_env"}
EXCLUDE_FILES = {".env", "package-lock.json", "yarn.lock", "licenses.db"}

# --- CATEGORY MAPPING (NEON ALIGNED) ---
EXT_MAP = {
    ".py": "LOGIC",
    ".tsx": "FRONTEND",
    ".ts": "FRONTEND",
    ".css": "STYLE",
    ".yaml": "AGENT",
    ".json": "CONFIG",
    ".md": "DOCS",
    ".csv": "DATA"
}

def get_physical_hash(path: Path) -> str:
    """Calculates SHA-256 of a physical file for IronClad validation."""
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def get_sector(path: Path) -> str:
    """Extracts the industrial sector based on pathing."""
    parts = path.parts
    if "agents" in parts:
        # data/agents/cyber_security/...
        idx = parts.index("agents")
        if len(parts) > idx + 1: return parts[idx+1].upper()
    if "arsenal" in parts: return "ARSENAL"
    return "ARCHITECT"

class LatticeIngestor:
    def __init__(self):
        self.mem = MemoryManager()
        self.nodes = []
        self.links = []
        self.inventory = {}
        self.count = 0

    def run(self):
        print("\n" + "⚡"*30)
        print("🚀 REALM FORGE: LATTICE FUSION INITIALIZED")
        print(f"ANCHOR: {ROOT}")
        print("⚡"*30 + "\n")

        # 1. CLEANUP
        if GRAPH_PATH.exists(): os.remove(GRAPH_PATH)
        
        # 2. PHYSICAL CRAWL
        for path in ROOT.rglob("*"):
            if any(x in path.parts for x in EXCLUDE_DIRS): continue
            if path.name in EXCLUDE_FILES or path.is_dir(): continue
            
            ext = path.suffix.lower()
            if ext not in EXT_MAP: continue

            self.process_file(path)

        # 3. RELATIONSHIP SUTURE (Relational DNA)
        self.build_links()

        # 4. PHYSICAL COMMIT
        self.save_lattice()

    def process_file(self, path: Path):
        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
            if not content.strip(): return

            f_hash = get_physical_hash(path)
            rel_path = str(path.relative_to(ROOT)).replace("\\", "/")
            sector = get_sector(path)
            category = EXT_MAP.get(path.suffix.lower(), "KNOWLEDGE")
            
            # NODE IDENTITY
            node_id = f"RF-{hashlib.md5(rel_path.encode()).hexdigest()[:8]}"
            
            # METADATA FOR BRAIN & IRONCLAD
            metadata = {
                "id": node_id,
                "label": path.name,
                "path": rel_path,
                "category": category,
                "sector": sector,
                "file_hash": f_hash,
                "size": f"{os.path.getsize(path) / 1024:.1f} KB",
                "last_verified": datetime.now().isoformat(),
                "line_count": len(content.splitlines())
            }

            # VECTOR INGESTION (MemoryManager)
            self.mem.knowledge.add(
                documents=[content],
                metadatas=[metadata],
                ids=[node_id]
            )

            # LATTICE GRAPH PREP
            self.nodes.append(metadata)
            self.inventory[rel_path] = f_hash
            
            print(f"✅ FUSED: {rel_path.ljust(50)} | {f_hash[:8]}...")
            self.count += 1

        except Exception as e:
            print(f"❌ FAULT: {path.name} | {e}")

    def build_links(self):
        """Creates Relational DNA between the Brain, Gateway, and Agents."""
        # Find Anchor Nodes
        gateway = next((n for n in self.nodes if "server.py" in n['path']), None)
        brain = next((n for n in self.nodes if "realm_core.py" in n['path']), None)

        if gateway and brain:
            self.links.append({"source": gateway['id'], "target": brain['id'], "type": "NEURAL_LINK"})

        # Link Agents to their Industrial Sectors
        for node in self.nodes:
            if node['category'] == "AGENT":
                # Link Agent to the Brain
                if brain:
                    self.links.append({"source": node['id'], "target": brain['id'], "type": "AUTH_UPLINK"})
            
            if "registry.py" in node['path'] and brain:
                self.links.append({"source": node['id'], "target": brain['id'], "type": "ARSENAL_LOAD"})

    def save_lattice(self):
        # Neural Graph for UI (v31.1 NeuralLattice component)
        with open(GRAPH_PATH, 'w', encoding='utf-8') as f:
            json.dump({"nodes": self.nodes, "links": self.links}, f, indent=2)

        # Inventory Report for Forensic Audits
        with open(INVENTORY_PATH, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "node_count": self.count,
                "inventory": self.inventory,
                "status": "INTEGRITY_LOCKED"
            }, f, indent=2)

        print(f"\n💎 LATTICE FUSION COMPLETE")
        print(f">>> Nodes Secured: {self.count}")
        print(f">>> Relationships Sutured: {len(self.links)}")
        print(f">>> Graph Exported: {GRAPH_PATH}")
        print(f"--- SYSTEM IS NOW HASH-AWARE ---\n")

if __name__ == "__main__":
    ingestor = LatticeIngestor()
    ingestor.run()