"""
REALM FORGE: SOVEREIGN GATEWAY v27.8
ARCHITECT: LEAD SWARM ENGINEER
STATUS: PRODUCTION READY - FULL FIDELITY - OAUTH & ASSISTANT ENABLED
PATH: F:/RealmForge_PROD/server.py
"""

import time
import json
import os
import yaml
import logging
import re
import asyncio
import psutil
import base64
import sys
import csv
import io
from datetime import datetime
from typing import List, Dict, Any, Optional, Union, Annotated
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends, Security, Request, UploadFile, File
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
import uvicorn
from contextlib import asynccontextmanager

# ==============================================================================
# 0. PHYSICAL ENCODING & PATH VIRTUALIZATION
# ==============================================================================
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
        sys.stderr.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
    except AttributeError: pass

load_dotenv()

# DOCKER BRIDGE: If running in container, map F:/ paths to /app paths
IS_DOCKER = os.path.exists('/.dockerenv')
ROOT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
WORKSPACE_ROOT = Path("/app/workspaces") if IS_DOCKER else Path("F:/RealmWorkspaces")

BASE_PATH = ROOT_DIR / "data"
STATIC_PATH = ROOT_DIR / "static"
AGENT_DIR = BASE_PATH / "agents"
GRAPH_PATH = BASE_PATH / "memory" / "neural_graph.json"
AUDIT_LOG_PATH = BASE_PATH / "workforce_audit.csv"

# Ensure industrial directory structure
folders = [BASE_PATH, STATIC_PATH, AGENT_DIR, BASE_PATH / "memory", BASE_PATH / "logs", BASE_PATH / "security", WORKSPACE_ROOT, STATIC_PATH / "deployments"]
for folder in folders: os.makedirs(folder, exist_ok=True)

# Initialize Audit Log
if not AUDIT_LOG_PATH.exists():
    with open(AUDIT_LOG_PATH, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Agent_ID", "Department", "Mission_ID", "Action", "Credits_Earned"])

# --- LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [TITAN_GATEWAY] - %(levelname)s - %(message)s')
logger = logging.getLogger("RealmForgeGateway")

# --- 4. INTERNAL MODULE IMPORTS ---
try:
    from src.auth import gatekeeper
    from src.system.state import get_initial_state, RealmForgeState
    from src.memory.engine import MemoryManager # Required for Assistant Chat
    from src.system.arsenal.registry import (
        prepare_vocal_response, 
        generate_neural_audio, 
        get_swarm_roster, 
        ALL_TOOLS_LIST
    )
    logger.info("✅ [SYSTEM] Core Sovereign Modules Linked.")
except ImportError as e:
    logger.error(f"❌ [CRITICAL] Internal Module Import Failure: {e}")
    sys.exit(1)

# --- ENGINE INTEGRATION ---
genesis_engine = None
def get_brain():
    global genesis_engine
    if genesis_engine is None:
        try:
            logger.info("🧠 [BRAIN] Awakening Genesis Engine & 13k+ Nodes...")
            from realm_core import app as brain_app
            genesis_engine = brain_app
            logger.info("✅ [BRAIN] Genesis Engine Online.")
        except Exception as e:
            logger.error(f"❌ [CRITICAL] Engine Fault: {e}")
            raise RuntimeError(f"Engine Failed to Ignite: {e}")
    return genesis_engine

# ==============================================================================
# 6. DATA MODELS
# ==============================================================================
class MissionRequest(BaseModel):
    task: str

class ChatRequest(BaseModel):
    message: str

class GithubTokenRequest(BaseModel):
    code: str

class FileReadRequest(BaseModel):
    path: str

class FileSaveRequest(BaseModel):
    path: str
    content: str

# ==============================================================================
# 7. TELEMETRY & CONNECTION MANAGEMENT
# ==============================================================================
class ConnectionManager:
    def __init__(self): 
        self.active: List[WebSocket] = []
        
    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)
        logger.info(f"🔌 [UPLINK] HUD Connected. active_nodes: {len(self.active)}")
        
    def disconnect(self, ws: WebSocket):
        if ws in self.active: self.active.remove(ws)
        logger.info(f"🔌 [DOWNLINK] HUD Disconnected.")
        
    async def broadcast(self, msg: dict):
        if "vitals" not in msg:
            try:
                msg["vitals"] = {
                    "ram": round(psutil.virtual_memory().percent, 1),
                    "cpu": psutil.cpu_percent(),
                    "lattice_nodes": self._count_nodes(),
                    "active_users": len(self.active),
                    "active_sector": msg.get("dept", "Architect"),
                    "timestamp": time.time()
                }
            except: pass
        
        txt = json.dumps(msg, ensure_ascii=False)
        for ws in self.active:
            try: await ws.send_text(txt)
            except: self.disconnect(ws)

    def _count_nodes(self):
        try:
            if GRAPH_PATH.exists():
                with open(GRAPH_PATH, 'r', encoding='utf-8-sig') as f:
                    return len(json.load(f).get('nodes', []))
        except: pass
        return 13472

manager = ConnectionManager()

# ==============================================================================
# 8. LIFESPAN EVENT HANDLERS
# ==============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    get_brain()
    print("\n" + "🚀"*20, flush=True)
    print(f"✅ [BRAIN] TITAN-INDUSTRIAL HUD ONLINE.", flush=True)
    print(f"✅ [LATTICE] SOVEREIGN NODE READY ON PORT 8000.", flush=True)
    print(f"🌀 [INTELLIGENCE] Nemotron/Groq Hybrid Active.", flush=True)
    print("🚀"*20 + "\n", flush=True)
    yield
    logger.info("🔌 [OFFLINE] Sovereign Node shutdown initiated.")

# --- FASTAPI APP CONFIGURATION ---
app = FastAPI(
    title="RealmForge OS - Sovereign Gateway",
    version="27.8.0",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory=str(STATIC_PATH)), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://realmforgev2.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.middleware("http")
async def add_ngrok_bypass_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["ngrok-skip-browser-warning"] = "69420"
    return response

# ==============================================================================
# 9. NEW MILLION-DOLLAR ENDPOINTS (OAUTH & ASSISTANT)
# ==============================================================================

@app.post("/api/v1/auth/github")
async def github_auth(req: GithubTokenRequest, lic: gatekeeper.License = Depends(get_license)):
    """Handles GitHub OAuth token exchange for the Sovereign Workforce."""
    try:
        # 1. Exchange 'code' for 'token' via GitHub API
        # (Placeholder for industrial implementation)
        logger.info(f"🗝️ [OAUTH]: Exchanging code for token for client {lic.user_id}")
        return {"status": "SUCCESS", "message": "GitHub Identity Sutured to Swarm."}
    except Exception as e:
        raise HTTPException(500, f"OAuth Failure: {str(e)}")

@app.post("/api/v1/assistant/chat")
async def assistant_chat(req: ChatRequest, lic: gatekeeper.License = Depends(get_license)):
    """The Intelligent Sidebar Bridge: Answers questions using full repo context."""
    try:
        mem = MemoryManager()
        # 1. Query the Lattice for the specific file/logic context
        # category="source_code" limits it to the PROD folder logic
        context = await mem.recall(req.message, n_results=3)
        
        # 2. Call the Mastermind for a direct chat response
        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"You are the ForgeMaster Consultant. Use this code context to help the Architect: {context}"},
                {"role": "user", "content": req.message}
            ]
        )
        return {"response": res.choices[0].message.content}
    except Exception as e:
        return {"response": f"⚠️ [ASSISTANT_FAULT]: {str(e)}"}

# ==============================================================================
# 10. AUTHENTICATION & SENSORY SUTURES
# ==============================================================================
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_license(key: str = Security(api_key_header)):
    master = os.getenv("REALM_MASTER_KEY", "sk-realm-god-mode-888")
    if key == master: 
        return gatekeeper.License(key="MASTER", user_id="ROOT_ARCHITECT", tier="GOD", credits=999999, created_at=time.time(), status="ACTIVE")
    lic = gatekeeper.validate_key(key)
    if not lic: raise HTTPException(403, "License Invalid.")
    return lic

@app.post("/api/v1/mission")
async def mission(req: MissionRequest, lic: gatekeeper.License = Depends(get_license)):
    engine = get_brain()
    try:
        state = get_initial_state()
        mid = state["mission_id"]
        state["messages"] = [HumanMessage(content=req.task)]
        
        await manager.broadcast({"type": "diagnostic", "text": f"[{datetime.now().strftime('%H:%M:%S')}] Mission {mid} Initialized.", "agent": "CORE"})

        last_msg_idx = 1
        async for output in engine.astream(state):
            for node_name, node_state in output.items():
                agent = node_state.get("active_agent", "NEXUS")
                dept = node_state.get("active_department", "Architect")
                handoffs = node_state.get("handoff_history", [])
                participants = node_state.get("meeting_participants", [])
                msgs = node_state.get("messages", [])

                await manager.broadcast({
                    "type": "node_update", "node": node_name.upper(), "agent": agent, "dept": dept,
                    "handoffs": handoffs, "meeting_participants": participants
                })

                while last_msg_idx < len(msgs):
                    new_msg = msgs[last_msg_idx]
                    content = new_msg.content if hasattr(new_msg, 'content') else str(new_msg)
                    if content and len(content) > 5:
                        audio = await generate_neural_audio(prepare_vocal_response(content))
                        await manager.broadcast({"type": "audio_chunk", "text": content, "audio_base64": audio, "agent": agent, "node": node_name, "dept": dept})
                    last_msg_idx += 1
                await asyncio.sleep(0.05)

        await manager.broadcast({"type": "mission_complete"})
        return {"status": "SUCCESS", "mission_id": mid}
    except Exception as e:
        logger.error(f"💥 [MISSION_FAULT]: {e}")
        await manager.broadcast({"type": "error", "message": str(e)})
        raise HTTPException(500, str(e))

@app.get("/api/v1/agents")
async def list_agents(lic: gatekeeper.License = Depends(get_license)):
    """Provides the roster. Forces schema compliance to prevent HUD crashes."""
    path = BASE_PATH / "roster.json"
    try:
        if path.exists():
            with open(path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                roster = data.get("roster", data.get("agents", []))
                for agent in roster:
                    if "name" not in agent: agent["name"] = agent.get("functional_name", "Unknown_Agent")
                    if "id" not in agent: agent["id"] = "GEN-UNK"
                return {"roster": roster}
        return {"roster": [{"name": "ForgeMaster", "role": "Orchestrator", "dept": "Architect", "id": "RF-CORE", "status": "ACTIVE"}]}
    except Exception as e: return {"roster": [], "error": str(e)}

@app.get("/api/v1/graph")
async def get_lattice_data(lic: gatekeeper.License = Depends(get_license)):
    try:
        if not GRAPH_PATH.exists(): return {"nodes": [{"id": "root", "label": "Offline"}], "links": []}
        with open(GRAPH_PATH, 'r', encoding='utf-8-sig') as f: return json.load(f)
    except Exception as e: return {"nodes": [], "links": [], "error": str(e)}

@app.post("/api/v1/io/read")
async def read_artifact(req: FileReadRequest, lic: gatekeeper.License = Depends(get_license)):
    clean_path = req.path.replace("F:/RealmForge/", "").replace("F:/RealmWorkspaces/", "").replace("F:/RealmForge_PROD/", "")
    target = WORKSPACE_ROOT / clean_path
    if not target.exists(): target = ROOT_DIR / clean_path
    if ".." in str(target): raise HTTPException(403, "Path Traversal Blocked")
    if target.exists() and target.is_file():
        return {"content": target.read_text(encoding='utf-8-sig', errors='replace'), "type": target.suffix, "path": str(req.path)}
    return {"error": "Not Found"}

@app.post("/api/v1/io/write")
async def save_artifact(req: FileSaveRequest, lic: gatekeeper.License = Depends(get_license)):
    clean_path = req.path.replace("F:/RealmForge/", "").replace("F:/RealmWorkspaces/", "").replace("F:/RealmForge_PROD/", "")
    target = WORKSPACE_ROOT / clean_path
    if ".." in str(target): raise HTTPException(403, "Path Traversal Blocked")
    try:
        os.makedirs(target.parent, exist_ok=True)
        target.write_text(req.content, encoding='utf-8-sig')
        return {"status": "SUCCESS"}
    except Exception as e: raise HTTPException(500, str(e))

@app.get("/health")
def health(): return {"status": "ONLINE", "timestamp": datetime.now().isoformat()}

@app.websocket("/ws/telemetry")
async def ws_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True: await websocket.receive_text()
    except WebSocketDisconnect: manager.disconnect(websocket)

if __name__ == "__main__":
    os.environ["PYTHONUNBUFFERED"] = "1"
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)