"""
REALM FORGE: SOVEREIGN GATEWAY v27.17 (INDUSTRIAL ULTIMATE)
ARCHITECT: LEAD SWARM ENGINEER
STATUS: PRODUCTION READY - FULL FIDELITY - OAUTH BRIDGE & STATE SUTURE
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
import httpx # For GitHub OAuth exchange logic
from datetime import datetime
from typing import List, Dict, Any, Optional, Union, Annotated
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends, Security, Request, UploadFile, File
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
import uvicorn
from contextlib import asynccontextmanager

# ==============================================================================
# 0. PHYSICAL ENCODING & FORCED ENV LOADING
# ==============================================================================
# FORCED PATH: Ensures the server sees your F:/ drive .env even if launched from elsewhere
ROOT_DIR = Path("F:/RealmForge_PROD")
env_path = ROOT_DIR / ".env"

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"✅ [SYSTEM] Physical .env loaded: {env_path}", flush=True)
else:
    print(f"❌ [CRITICAL] .env NOT FOUND at {env_path}. Defaulting to local environment.", flush=True)
    load_dotenv()

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
        sys.stderr.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
    except AttributeError: pass

IS_DOCKER = os.path.exists('/.dockerenv')
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

# Stabilize Lattice Visualization (Fix for the missing neural_graph.json)
if not GRAPH_PATH.exists():
    os.makedirs(GRAPH_PATH.parent, exist_ok=True)
    with open(GRAPH_PATH, 'w', encoding='utf-8') as f:
        json.dump({"nodes": [{"id": "CORE", "label": "NEXUS", "group": "Architect"}], "links": []}, f)

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
    from src.memory.engine import MemoryManager 
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
class MissionRequest(BaseModel): task: str
class ChatRequest(BaseModel): message: str
class GithubTokenRequest(BaseModel): code: str
class FileReadRequest(BaseModel): path: str
class FileSaveRequest(BaseModel): path: str; content: str

# ==============================================================================
# 6. TELEMETRY & AUTHENTICATION
# ==============================================================================
class ConnectionManager:
    def __init__(self): 
        self.active: List[WebSocket] = []
        
    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)
        await self.broadcast({
            "type": "diagnostic", 
            "text": "🤝 [HUD_UPLINK]: Neural Sensory Interface Synchronized."
        })
        logger.info(f"🔌 [UPLINK] Node connection established. active_nodes: {len(self.active)}")
        
    def disconnect(self, ws: WebSocket):
        if ws in self.active: self.active.remove(ws)
        logger.info(f"🔌 [DOWNLINK] Node connection severed.")
        
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
        if self.active:
            tasks = [self._safe_send(ws, txt) for ws in self.active]
            await asyncio.gather(*tasks)

    async def _safe_send(self, ws: WebSocket, text: str):
        try: await ws.send_text(text)
        except Exception: self.disconnect(ws)

    def _count_nodes(self):
        try:
            if GRAPH_PATH.exists():
                with open(GRAPH_PATH, 'r', encoding='utf-8-sig') as f:
                    return len(json.load(f).get('nodes', []))
        except: pass
        return 13472

manager = ConnectionManager()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_license(key: str = Security(api_key_header)):
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
# 7. LIFESPAN & APP CONFIG
# ==============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    get_brain()
    print("\n" + "🚀"*20, flush=True)
    print(f"✅ [BRAIN] TITAN-INDUSTRIAL HUD ONLINE.", flush=True)
    print(f"✅ [LATTICE] SOVEREIGN NODE READY ON PORT 8000.", flush=True)
    print(f"🌀 [INTELLIGENCE] Mode: {os.getenv('REALM_MODEL_CORE', 'GROQ')}", flush=True)
    print("🚀"*20 + "\n", flush=True)
    yield
    logger.info("🔌 [OFFLINE] Sovereign Node shutdown initiated.")

app = FastAPI(title="RealmForge OS - Sovereign Gateway", version="27.17.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(STATIC_PATH)), name="static")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"], expose_headers=["*"]
)

@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str): return {}

# ==============================================================================
# 8. OAUTH & ASSISTANT ENDPOINTS (SUTURED MSN-011)
# ==============================================================================

@app.get("/api/v1/auth/github")
async def github_login():
    """Step 1: Redirect to GitHub. (Ensures ID is pulled from ENV)"""
    client_id = os.getenv("GITHUB_CLIENT_ID")
    if not client_id:
        raise HTTPException(500, "GITHUB_CLIENT_ID not found in .env")
    
    # Callback must be LOCAL to this server
    redirect_uri = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8000/api/v1/auth/github/callback")
    url = f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=repo,user"
    logger.info(f"🗝️ [OAUTH]: Redirecting to GitHub with ID: {client_id}")
    return RedirectResponse(url)

@app.get("/api/v1/auth/github/callback")
async def github_callback(code: str):
    """Step 2: Catch code from GitHub and redirect back to Vercel HUD."""
    frontend_url = "https://realmforgev2-prod.vercel.app/auth-success" 
    logger.info(f"🗝️ [OAUTH]: Handshake code received. Redirecting to HUD.")
    return RedirectResponse(f"{frontend_url}?code={code}")

@app.post("/api/v1/auth/github")
async def github_exchange(req: GithubTokenRequest, lic: gatekeeper.License = Depends(get_license)):
    """Step 3: UI sends code back here for physical token exchange."""
    logger.info(f"🗝️ [OAUTH]: Token exchange for {lic.user_id}")
    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://github.com/login/oauth/access_token",
            params={
                "client_id": os.getenv("GITHUB_CLIENT_ID"),
                "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
                "code": req.code
            },
            headers={"Accept": "application/json"}
        )
        return res.json()

@app.post("/api/v1/assistant/chat")
async def assistant_chat(req: ChatRequest, lic: gatekeeper.License = Depends(get_license)):
    try:
        mem = MemoryManager()
        context = await mem.recall(req.message, n_results=3)
        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"You are the ForgeMaster Consultant. Context: {context}"},
                {"role": "user", "content": req.message}
            ]
        )
        return {"response": res.choices[0].message.content}
    except Exception as e: return {"response": f"⚠️ [ASSISTANT_FAULT]: {str(e)}"}

# ==============================================================================
# 9. MISSION ENGINE (SENSORY-FIXED)
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
        # INITIAL STATE SUTURE: Prevent "None" Agents
        state = {
            "messages": [HumanMessage(content=req.task)],
            "active_agent": "Mastermind",
            "active_department": "Architect",
            "mission_id": f"MSN-{int(time.time())}",
            "handoff_history": [],
            "meeting_participants": ["Mastermind"]
        }
        
        mid = state["mission_id"]
        await manager.broadcast({
            "type": "diagnostic", "text": f"Strike {mid} Initialized.", "agent": "CORE"
        })

        async for output in engine.astream(state):
            for node_name, node_state in output.items():
                agent = node_state.get("active_agent") or node_name.upper()
                dept = node_state.get("active_department", "Architect")
                handoffs = node_state.get("handoff_history", [])
                participants = node_state.get("meeting_participants", [])
                msgs = node_state.get("messages", [])

                await manager.broadcast({
                    "type": "node_update", "node": node_name.upper(), 
                    "agent": agent, "dept": dept, "handoffs": handoffs,
                    "meeting_participants": participants
                })

                log_contribution(agent, dept, mid, f"Node: {node_name}")

                new_msgs = msgs if isinstance(msgs, list) else [msgs]
                for msg in new_msgs:
                    if hasattr(msg, 'content') and msg.content and not isinstance(msg, HumanMessage):
                        content = msg.content
                        vocal = prepare_vocal_response(content)
                        audio = await generate_neural_audio(vocal)
                        await manager.broadcast({
                            "type": "audio_chunk", "text": content, "audio_base64": audio, 
                            "agent": agent, "node": node_name, "dept": dept
                        })

        await manager.broadcast({"type": "mission_complete"})
        return {"status": "SUCCESS", "mission_id": mid}
    except Exception as e:
        logger.error(f"💥 [MISSION_FAULT]: {e}")
        await manager.broadcast({"type": "error", "message": str(e)})
        raise HTTPException(500, str(e))

# ==============================================================================
# 10. HARDENED SENSORY ENDPOINTS (ROSTER & I/O)
# ==============================================================================

@app.get("/api/v1/agents")
async def list_agents(lic: gatekeeper.License = Depends(get_license)):
    path = BASE_PATH / "roster.json"
    try:
        if path.exists():
            with open(path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                roster = data.get("roster", [])
                for agent in roster:
                    f_name = agent.get("functional_role", "Industrial_Specialist")
                    agent["name"] = f_name
                    agent["display_name"] = f"{f_name.replace('_Agent', '').replace('_', ' ')}"
                return {"roster": roster}
        return {"roster": []}
    except Exception as e: return {"roster": [], "error": str(e)}

@app.get("/api/v1/graph")
async def get_lattice_data(lic: gatekeeper.License = Depends(get_license)):
    try:
        if not GRAPH_PATH.exists(): return {"nodes": [{"id": "root", "label": "Offline"}], "links": []}
        with open(GRAPH_PATH, 'r', encoding='utf-8-sig') as f: return json.load(f)
    except Exception as e: return {"nodes": [], "links": [], "error": str(e)}

@app.post("/api/v1/io/read")
async def read_artifact(req: FileReadRequest, lic: gatekeeper.License = Depends(get_license)):
    clean_path = req.path.replace("F:/RealmForge_PROD/", "")
    target = ROOT_DIR / clean_path
    if not target.exists(): target = WORKSPACE_ROOT / clean_path
    if target.exists() and target.is_file():
        return {"content": target.read_text(encoding='utf-8-sig', errors='replace'), "type": target.suffix, "path": str(req.path)}
    return {"error": f"File {req.path} not located on physical disk."}

@app.post("/api/v1/io/write")
async def save_artifact(req: FileSaveRequest, lic: gatekeeper.License = Depends(get_license)):
    clean_path = req.path.replace("F:/RealmForge_PROD/", "")
    target = ROOT_DIR / clean_path
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
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)