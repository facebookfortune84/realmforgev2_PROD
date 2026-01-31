"""
REALM FORGE: SOVEREIGN MEMORY ENGINE v25.0
ARCHITECT: LEAD SWARM ENGINEER
STATUS: PRODUCTION READY - RAG & LATTICE ENABLED
"""

import os
import json
import uuid
import logging
import asyncio
import re
import networkx as nx
import chromadb
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from chromadb.utils import embedding_functions

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MemoryKernel")

# --- PATH SOVEREIGNTY ---
# Respects the ROOT_DIR established in actions.py to prevent path drift
ROOT_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
DATA_ROOT = ROOT_DIR / "data"
CHROMA_PATH = str(DATA_ROOT / "chroma_db")
GRAPH_PATH = DATA_ROOT / "memory" / "neural_graph.json"

class MemoryManager:
    """
    Sovereign Memory Engine: Manages Vector RAG and Relational Lattice.
    Provides the 'Collective Brain' for 1,107 autonomous agents.
    """

    def __init__(self):
        # Ensure directories exist
        os.makedirs(DATA_ROOT / "memory", exist_ok=True)
        os.makedirs(CHROMA_PATH, exist_ok=True)
        
        # 1. VECTOR DATABASE CLIENT (The 'Deep Memory')
        # Persistent storage for high-dimensional embeddings
        try:
            self.chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
            self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
            
            # COLLECTION A: EPISODIC (Short-term context and workforce logs)
            self.episodic = self.chroma_client.get_or_create_collection(
                name="episodic_memory", 
                embedding_function=self.embedding_fn,
                metadata={"hnsw:space": "cosine"}
            )

            # COLLECTION B: KNOWLEDGE BASE (Long-term corporate intelligence)
            self.knowledge = self.chroma_client.get_or_create_collection(
                name="knowledge_base",
                embedding_function=self.embedding_fn,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            logger.error(f"❌ [VECTOR_INIT_FAIL]: {e}")
            raise

        # 2. RELATIONAL LATTICE (The 'Network Brain')
        # Uses NetworkX to map relationships between 1,107 agents and missions
        self.graph = nx.DiGraph()
        self.graph_lock = asyncio.Lock()
        self._load_graph_sync()

    def _load_graph_sync(self):
        """Loads the graph from physical disk with UTF-8-SIG resilience."""
        if GRAPH_PATH.exists():
            try:
                with open(GRAPH_PATH, 'r', encoding='utf-8-sig') as f:
                    data = json.load(f)
                    # Support both standard node_link and customized swarm schemas
                    self.graph = nx.node_link_graph(data)
                logger.info(f"🕸️ [LATTICE_ACTIVE] Nodes: {self.graph.number_of_nodes()}")
            except Exception as e:
                logger.error(f"⚠️ [LATTICE_RESET]: Corruption detected, re-initializing. {e}")
                self.graph = nx.DiGraph()
        else:
            logger.info("🕸️ [LATTICE_INIT] Creating fresh relational lattice.")
            self.graph = nx.DiGraph()

    async def save_graph(self):
        """Commits the lattice to physical storage."""
        async with self.graph_lock:
            try:
                data = nx.node_link_data(self.graph)
                with open(GRAPH_PATH, 'w', encoding='utf-8-sig') as f:
                    json.dump(data, f, indent=2)
            except Exception as e:
                logger.error(f"❌ [GRAPH_SAVE_FAIL]: {e}")

    # ==============================================================================
    # WORKFORCE PERSISTENCE
    # ==============================================================================

    async def commit_mission_event(self, mission_id: str, agent_id: str, dept: str, action: str, result: str):
        """
        Saves mission outcomes to Episodic Memory.
        Critical for cross-agent collaboration.
        """
        timestamp = datetime.now().isoformat()
        try:
            doc_text = f"MISSION: {mission_id} | AGENT: {agent_id} | DEPT: {dept}\nACTION: {action}\nRESULT: {result[:4000]}"
            
            # 1. Update Vector Store
            self.episodic.add(
                documents=[doc_text],
                metadatas=[{
                    "mission_id": mission_id, 
                    "agent": agent_id, 
                    "dept": dept, 
                    "ts": timestamp, 
                    "type": "work_event"
                }],
                ids=[f"ev_{mission_id}_{uuid.uuid4().hex[:6]}"]
            )

            # 2. Update Relational Lattice
            async with self.graph_lock:
                # Link Agent to the Action
                self.graph.add_node(agent_id, type="AGENT", dept=dept)
                self.graph.add_node(mission_id, type="MISSION", ts=timestamp)
                self.graph.add_edge(agent_id, mission_id, relation="EXECUTED", action=action)
            
            await self.save_graph()
            
        except Exception as e:
            logger.error(f"⚠️ [EPISODIC_FAIL]: {e}")

    async def ingest_knowledge(self, source: str, content: str, category: str = "industrial_data"):
        """
        Absorbs corporate documentation into the long-term knowledge base.
        Used for Business Plans, Tool Manuals, and Regulatory requirements.
        """
        try:
            self.knowledge.add(
                documents=[content],
                metadatas=[{
                    "source": source, 
                    "category": category, 
                    "ingest_ts": datetime.now().isoformat()
                }],
                ids=[f"kn_{uuid.uuid4().hex[:8]}"]
            )
            
            # Record in lattice as an ARTIFACT
            async with self.graph_lock:
                self.graph.add_node(source, type="ARTIFACT", category=category)
                
            logger.info(f"📚 [INGEST] Knowledge lattice expanded with: {source}")
        except Exception as e:
            logger.error(f"❌ [INGEST_FAIL]: {e}")

    # ==============================================================================
    # RETRIEVAL (THE RAG PIPELINE)
    # ==============================================================================

    async def recall(self, query: str, n_results: int = 5) -> str:
        """
        Dual-Core Retrieval: Unified RAG from Facts and History.
        """
        context = []
        
        # 1. Search Knowledge Base (The 'Truth')
        try:
            k_res = self.knowledge.query(query_texts=[query], n_results=n_results)
            if k_res['documents']:
                for doc in k_res['documents'][0]:
                    context.append(f"📚 [KNOWLEDGE_LATTICE]: {doc}")
        except Exception as e:
            logger.warning(f"Knowledge recall hiccup: {e}")

        # 2. Search Episodic Memory (The 'Experience')
        try:
            e_res = self.episodic.query(query_texts=[query], n_results=n_results)
            if e_res['documents']:
                for doc in e_res['documents'][0]:
                    context.append(f"💾 [EPISODIC_LOG]: {doc}")
        except Exception as e:
            logger.warning(f"Episodic recall hiccup: {e}")

        return "\n\n".join(context) if context else "No relevant memory nodes found in the current lattice."

    async def get_node_details(self, entity_id: str) -> Dict[str, Any]:
        """Traverses the lattice for relational metadata."""
        if self.graph.has_node(entity_id):
            return {
                "id": entity_id,
                "metadata": self.graph.nodes[entity_id],
                "connections": list(self.graph.neighbors(entity_id))
            }
        return {"error": "Node not found"}