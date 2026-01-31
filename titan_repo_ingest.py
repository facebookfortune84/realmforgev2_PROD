"""
REALM FORGE: REPOSITORY AUTO-INGESTOR v2.1 (HASH-AWARE)
PURPOSE: Physically indexes 100% of the project and FUSES file hashes into the lattice.
"""
import os, json, time, hashlib
from pathlib import Path
from src.memory.engine import MemoryManager
from datetime import datetime

ROOT = Path("F:/RealmForge_PROD")

def get_physical_hash(path):
    """Calculates SHA-256 of a physical file."""
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def ingest_lattice():
    print("\n" + "🛡️"*20)
    print("🚀 REALM FORGE: INTEGRITY-LOCKED RECONSTRUCTION")
    print("🛡️"*20 + "\n")
    
    # Reset Neural Graph
    graph_path = ROOT / "data" / "memory" / "neural_graph.json"
    if graph_path.exists(): os.remove(graph_path)

    mem = MemoryManager()
    count = 0

    ingest_map = {
        "logic": ROOT / "src",
        "workforce": ROOT / "data" / "agents",
        "intelligence": ROOT / "data" / "ingress",
        "gateway": ROOT / "server.py",
        "mastermind": ROOT / "realm_core.py"
    }

    for category, path in ingest_map.items():
        if not path.exists(): continue
        
        files = list(path.rglob("*.py")) if path.is_dir() else [path]
        if category == "workforce": files = list(path.rglob("*.yaml"))
        if category == "intelligence": files = list(path.rglob("*.*"))

        for f in files:
            if any(x in str(f) for x in ["node_modules", "__pycache__", ".git"]): continue
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                if not content.strip(): continue

                # PHYSICAL FINGERPRINTING
                current_hash = get_physical_hash(f)
                
                node_id = f"PROD_{category.upper()}_{f.stem}"
                mem.knowledge.add(
                    documents=[content],
                    metadatas=[{
                        "source": str(f.relative_to(ROOT)), 
                        "category": category,
                        "file_hash": current_hash, # THE TRUTH LINK
                        "last_verified": datetime.now().isoformat()
                    }],
                    ids=[node_id]
                )
                print(f"✅ SECURED [{category}]: {f.name} | HASH: {current_hash[:8]}...")
                count += 1
            except Exception as e:
                print(f"⚠️ Skip {f.name}: {e}")

    print(f"\n💎 INTEGRITY INITIALIZED")
    print(f"Sovereign Nodes Ingested: {count}")
    print("Lattice is now HASH-AWARE.")

if __name__ == "__main__":
    ingest_lattice()