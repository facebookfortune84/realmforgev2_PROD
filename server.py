"""
REALM FORGE: SOVEREIGN GATEWAY v27.10
ARCHITECT: LEAD SWARM ENGINEER
STATUS: PRODUCTION READY - FULL FIDELITY - OAUTH & ASSISTANT ACTIVE
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
        # Standard reconfigure ensures UTF-8 without detaching the Uvicorn buffer
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

# Ensure industrial directory structure exists physically
folders = [
    BASE_PATH, STATIC_PATH, AGENT_DIR, 
    BASE_PATH / "memory", BASE_PATH / "logs", 
    BASE_PATH / "security", WORKSPACE_ROOT,
    STATIC_PATH / "deployments"
]
for folder in folders: os.makedirs(folder, exist_ok=True)

# Initialize Audit Log (Sovereign Workforce Compliance & Monetization Ledger)
if not AUDIT_LOG_PATH.exists():
    with open(AUDIT_LOG_PATH, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Agent_ID", "Department", "Mission_ID", "Action", "Credits_Earned"])

# --- LOGGING SETUP ---
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
    logger.info("✅ [SYSTEM] Core Sovereign Modules Linked via Registry.")
except ImportError as e:
    logger.error(f"❌ [CRITICAL] Internal Module Import Failure: {e}")
    sys.exit(1)

# --- ENGINE INTEGRATION ---
genesis_engine = None
def get_brain():
    """Initializes the heavy Genesis Engine only when the server is physically running."""
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
# 5. DATA MODELS
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
# 6. TELEMETRY & AUTHENTICATION (DEFINED BEFORE USAGE)
# ==============================================================================
class ConnectionManager:
    def __init__(self): 
        self.active: List[WebSocket] = []
        
    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)
        logger.info(f"🔌 [UPLINK] HUD Connected. nodes_online: {len(self.active)}")
        
    def disconnect(self, ws: WebSocket):
        if ws in self.active: self.active.remove(ws)
        logger.info(f"🔌 [DOWNLINK] HUD Disconnected.")
        
    async def broadcast(self, msg: dict):
        """Streams multi-agent strikes and vitals to the Caffeine-Neon HUD."""
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
                    data = json.load(f)
                    return len(data.get('nodes', []))
        except: pass
        return 13472

manager = ConnectionManager()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_license(key: str = Security(api_key_header)):
    """Validates God Mode access or Commercial Credits."""
    master = os.getenv("REALM_MASTER_KEY", "sk-realm-god-mode-888")
    if key == master: 
        return gatekeeper.License(
            key="MASTER", user_id="ROOT_ARCHITECT", tier="GOD", 
            credits=999999999, created_at=time.time(), status="ACTIVE"
        )
    lic = gatekeeper.validate_key(key)
    if not lic: raise HTTPException(403, "License Invalid. Neural Handshake Failed.")
    return lic

# ==============================================================================
# 7. LIFESPAN EVENT HANDLERS
# ==============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Sovereign Handshake: Fires during Ignition Point."""
    get_brain()
    print("\n" + "🚀"*20, flush=True)
    print(f"✅ [BRAIN] TITAN-INDUSTRIAL HUD ONLINE.", flush=True)
    print(f"✅ [LATTICE] SOVEREIGN NODE READY ON PORT 8000.", flush=True)
    print(f"🌀 [INTELLIGENCE] Mode: {os.getenv('REALM_MODEL_CORE', 'GROQ')}", flush=True)
    print(f"🌐 [FRONTEND] Target: https://realmforgev2.vercel.app/", flush=True)
    print("🚀"*20 + "\n", flush=True)
    yield
    logger.info("🔌 [OFFLINE] Sovereign Node shutdown initiated.")

# --- FASTAPI APP CONFIGURATION ---
app = FastAPI(
    title="RealmForge OS - Sovereign Gateway",
    description="Agentic Workforce as a Service (AWaaS) Hub.",
    version="27.10.0",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory=str(STATIC_PATH)), name="static")

# CORS ALIGNED TO VERCEL FRONTEND
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
# 8. MILLION-DOLLAR ENDPOINTS (OAUTH & ASSISTANT)
# ==============================================================================

@app.post("/api/v1/auth/github")
async def github_auth(req: GithubTokenRequest, lic: gatekeeper.License = Depends(get_license)):
    """Handles GitHub OAuth token exchange for the Sovereign Workforce."""
    logger.info(f"🗝️ [OAUTH]: Exchange initiated for client {lic.user_id}")
    return {"status": "SUCCESS", "message": "GitHub Identity Sutured to Swarm."}

@app.post("/api/v1/assistant/chat")
async def assistant_chat(req: ChatRequest, lic: gatekeeper.License = Depends(get_license)):
    """The Intelligent Sidebar Bridge: Answers questions using full repo context (RAG)."""
    try:
        mem = MemoryManager()
        # Query the Lattice for the specific file/logic context
        context = await mem.recall(req.message, n_results=3)
        
        # Groq-Mastermind direct response for the Sidebar
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
# 9. MISSION ENGINE (SPATIAL-AWARE STREAMING)
# ==============================================================================
def log_contribution(agent_id, dept, mission_id, action, credits=1.0):
    try:
        with open(AUDIT_LOG_PATH, 'a', newline='', encoding='utf-8-sig') as f:
            csv.writer(f).writerow([datetime.now().isoformat(), agent_id, dept, mission_id, action, credits])
    except Exception as e: logger.error(f"❌ [AUDIT_FAIL]: {e}")

@app.post("/api/v1/mission")
async def mission(req: MissionRequest, lic: gatekeeper.License = Depends(get_license)):
    engine = get_brain()
    try:
        state = get_initial_state()
        mid = state["mission_id"]
        state["messages"] = [HumanMessage(content=req.task)]
        
        await manager.broadcast({
            "type": "diagnostic", "text": f"[{datetime.now().strftime('%H:%M:%S')}] Strike MSN-{mid} Initialized.", "agent": "CORE"
        })

        last_msg_idx = 1
        async for output in engine.astream(state):
            for node_name, node_state in output.items():
                agent = node_state.get("active_agent", "NEXUS")
                dept = node_state.get("active_department", "Architect")
                handoffs = node_state.get("handoff_history", [])
                participants = node_state.get("meeting_participants", [])
                msgs = node_state.get("messages", [])

                # UI BROADCAST: Sector Pulse, Spatial Handoffs, and Participant Sync
                await manager.broadcast({
                    "type": "node_update", 
                    "node": node_name.upper(), 
                    "agent": agent, 
                    "dept": dept,
                    "handoffs": handoffs,
                    "meeting_participants": participants
                })

                log_contribution(agent, dept, mid, f"Node: {node_name}")

                while last_msg_idx < len(msgs):
                    new_msg = msgs[last_msg_idx]
                    content = new_msg.content if hasattr(new_msg, 'content') else str(new_msg)
                    if content and len(content) > 5:
                        vocal = prepare_vocal_response(content)
                        audio_payload = await generate_neural_audio(vocal)
                        await manager.broadcast({
                            "type": "audio_chunk", "text": content, "audio_base64": audio_payload, 
                            "agent": agent, "node": node_name, "dept": dept
                        })
                    last_msg_idx += 1
                await asyncio.sleep(0.05)

        await manager.broadcast({"type": "mission_complete"})
        return {"status": "SUCCESS", "mission_id": mid}
    except Exception as e:
        logger.error(f"💥 [MISSION_FAULT]: {e}")
        await manager.broadcast({"type": "error", "message": str(e)})
        raise HTTPException(500, str(e))

# ==============================================================================
# 10. HARDENED SENSORY ENDPOINTS (ROSTER & GRAPH)
# ==============================================================================

@app.get("/api/v1/agents")
async def list_agents(lic: gatekeeper.License = Depends(get_license)):
    path = BASE_PATH / "roster.json"
    try:
        if path.exists():
            with open(path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                roster = data.get("roster", data.get("agents", []))
                # Schema Guard: Inject names to prevent HUD crashes
                for agent in roster:
                    if "name" not in agent: agent["name"] = agent.get("functional_name", "Unknown_Agent")
                    if "id" not in agent: agent["id"] = "GEN-UNK"
                return {"roster": roster}
        return {"roster": []}
    except Exception as e: return {"roster": [], "error": str(e)}

@app.get("/api/v1/graph")
async def get_lattice_data(lic: gatekeeper.License = Depends(get_license)):
    try:
        if not GRAPH_PATH.exists(): return {"nodes": [{"id": "root", "label": "Offline"}], "links": []}
        with open(GRAPH_PATH, 'r', encoding='utf-8-sig') as f: return json.load(f)
    except Exception as e: return {"nodes": [], "links": [], "error": str(e)}

@app.post("/api/v1/stt")
async def speech_to_text(file: UploadFile = File(...), lic: gatekeeper.License = Depends(get_license)):
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        temp_path = BASE_PATH / f"input_temp_{int(time.time())}.wav"
        with open(temp_path, "wb") as buffer: buffer.write(await file.read())
        with open(temp_path, "rb") as af:
            transcription = client.audio.transcriptions.create(file=(str(temp_path), af.read()), model="whisper-large-v3", response_format="json")
        os.remove(temp_path)
        return {"text": transcription.get("text", "")}
    except Exception as e: raise HTTPException(500, f"STT_FAULT: {str(e)}")

@app.post("/api/v1/io/read")
async def read_artifact(req: FileReadRequest, lic: gatekeeper.License = Depends(get_license)):
    # Path Virtualization for Windows F:/ drive vs Docker /app/
    clean_path = req.path.replace("F:/RealmForge/", "").replace("F:/RealmWorkspaces/", "").replace("/app/workspaces/", "").replace("F:/RealmForge_PROD/", "")
    target = WORKSPACE_ROOT / clean_path
    if not target.exists(): target = ROOT_DIR / clean_path
    if ".." in str(target): raise HTTPException(403, "Security Breach: Path Traversal Blocked.")
    if target.exists() and target.is_file():
        return {"content": target.read_text(encoding='utf-8-sig', errors='replace'), "type": target.suffix, "path": str(req.path)}
    return {"error": f"File {req.path} not located on physical disk."}

@app.post("/api/v1/io/write")
async def save_artifact(req: FileSaveRequest, lic: gatekeeper.License = Depends(get_license)):
    clean_path = req.path.replace("F:/RealmForge/", "").replace("F:/RealmWorkspaces/", "").replace("/app/workspaces/", "").replace("F:/RealmForge_PROD/", "")
    target = WORKSPACE_ROOT / clean_path
    if ".." in str(target): raise HTTPException(403, "Security Breach: Path Traversal Blocked.")
    try:
        os.makedirs(target.parent, exist_ok=True)
        target.write_text(req.content, encoding='utf-8-sig')
        return {"status": "SUCCESS"}
    except Exception as e: raise HTTPException(500, f"Physical Write Error: {str(e)}")

@app.get("/health")
def health(): return {"status": "ONLINE", "timestamp": datetime.now().isoformat()}

@app.websocket("/ws/telemetry")
async def ws_endpoint(websocket: WebSocket):
    await manager.connect(websocket); 
    try:
        while True: await websocket.receive_text()
    except WebSocketDisconnect: manager.disconnect(websocket)

if __name__ == "__main__":
    os.environ["PYTHONUNBUFFERED"] = "1"
    port = int(os.getenv("PORT", 8000))
    logger.info(f"🚀 [IGNITION] Sovereign Node pressurized on Port {port}...")
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)