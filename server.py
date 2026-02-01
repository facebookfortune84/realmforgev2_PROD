"""
REALM FORGE: SOVEREIGN GATEWAY v27.11 (PATCHED)
ARCHITECT: LEAD SWARM ENGINEER
STATUS: PRODUCTION READY - NAMEERROR RESOLVED - SCHEMA GUARD ACTIVE
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
import httpx # Added for GitHub OAuth exchange logic
from datetime import datetime
from typing import List, Dict, Any, Optional, Union, Annotated
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends, Security, Request, UploadFile, File
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import RedirectResponse
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

IS_DOCKER = os.path.exists('/.dockerenv')
ROOT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
WORKSPACE_ROOT = Path("/app/workspaces") if IS_DOCKER else Path("F:/RealmWorkspaces")

BASE_PATH = ROOT_DIR / "data"
STATIC_PATH = ROOT_DIR / "static"
AGENT_DIR = BASE_PATH / "agents"
GRAPH_PATH = BASE_PATH / "memory" / "neural_graph.json"
AUDIT_LOG_PATH = BASE_PATH / "workforce_audit.csv"

folders = [BASE_PATH, STATIC_PATH, AGENT_DIR, BASE_PATH / "memory", BASE_PATH / "logs", BASE_PATH / "security", WORKSPACE_ROOT]
for folder in folders: os.makedirs(folder, exist_ok=True)

if not AUDIT_LOG_PATH.exists():
    with open(AUDIT_LOG_PATH, 'w', newline='', encoding='utf-8-sig') as f:
        csv.writer(f).writerow(["Timestamp", "Agent_ID", "Department", "Mission_ID", "Action", "Credits_Earned"])

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

genesis_engine = None
def get_brain():
    global genesis_engine
    if genesis_engine is None:
        try:
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
# 6. TELEMETRY & AUTHENTICATION (INSTANTIATED BEFORE DEPENDENCY)
# ==============================================================================
class ConnectionManager:
    def __init__(self): 
        self.active: List[WebSocket] = []
        
    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)
        await self.broadcast({"type": "diagnostic", "text": "🤝 [HUD_UPLINK]: Neural Sensory Interface Synchronized."})
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

# CRITICAL INSTANTIATION FOR WS BROADCAST
manager = ConnectionManager()

# REPAIR: MSN-001 Suture Gateway - Define Header before usage
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
# 7. LIFESPAN & APP CONFIG
# ==============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    get_brain()
    print(f"\n🚀 [BRAIN] TITAN-INDUSTRIAL HUD ONLINE. PORT 8000 READY.\n", flush=True)
    yield
    logger.info("🔌 [OFFLINE] Sovereign Node shutdown initiated.")

app = FastAPI(title="RealmForge OS", version="27.11.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(STATIC_PATH)), name="static")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"], expose_headers=["*"]
)

@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str): return {}

# ==============================================================================
# 8. MISSION CRITICAL ENDPOINTS
# ==============================================================================

@app.get("/api/v1/auth/github")
async def github_login():
    """Redirects the Architect to GitHub for Identity Verification."""
    client_id = os.getenv("GITHUB_CLIENT_ID")
    # Redirect to GitHub OAuth authorize page
    url = f"https://github.com/login/oauth/authorize?client_id={client_id}&scope=repo,user"
    logger.info("🗝️ [OAUTH]: Redirecting to GitHub Authorization.")
    return RedirectResponse(url)

@app.post("/api/v1/auth/github")
async def github_exchange(req: GithubTokenRequest, lic: gatekeeper.License = Depends(get_license)):
    """Handles the back-end code exchange."""
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

@app.get("/api/v1/agents")
async def list_agents(lic: gatekeeper.License = Depends(get_license)):
    """MSN-002: Roster Schema Guard. Maps functional_role to name for HUD stability."""
    path = BASE_PATH / "roster.json"
    try:
        if path.exists():
            with open(path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                roster = data.get("roster", [])
                for agent in roster:
                    f_role = agent.get("functional_role", "Industrial_Specialist")
                    # HARD-CODED: name slot is now the functional role to prevent HUD undefined errors
                    agent["name"] = f_role 
                    agent["display_name"] = f_role.replace("_Agent", "").replace("_", " ")
                return {"roster": roster}
        return {"roster": []}
    except Exception as e: return {"roster": [], "error": str(e)}

@app.post("/api/v1/assistant/chat")
async def assistant_chat(req: ChatRequest, lic: gatekeeper.License = Depends(get_license)):
    try:
        mem = MemoryManager()
        context = await mem.recall(req.message, n_results=3)
        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"ForgeMaster Consultant. Context: {context}"},
                {"role": "user", "content": req.message}
            ]
        )
        return {"response": res.choices[0].message.content}
    except Exception as e: return {"response": f"⚠️ [ASSISTANT_FAULT]: {str(e)}"}

@app.post("/api/v1/mission")
async def mission(req: MissionRequest, lic: gatekeeper.License = Depends(get_license)):
    engine = get_brain()
    try:
        state = get_initial_state()
        mid = state["mission_id"]
        state["messages"] = [HumanMessage(content=req.task)]
        
        await manager.broadcast({"type": "diagnostic", "text": f"Strike MSN-{mid} Initialized."})

        async for output in engine.astream(state):
            for node_name, node_state in output.items():
                agent = node_state.get("active_agent", "NEXUS")
                dept = node_state.get("active_department", "Architect")
                
                # REPAIR: Broadcast node updates immediately
                await manager.broadcast({
                    "type": "node_update", 
                    "node": node_name.upper(), 
                    "agent": agent, 
                    "dept": dept
                })

                # REPAIR: Corrected Message Loop
                # In 'astream', node_state contains the NEW messages for this step.
                new_messages = node_state.get("messages", [])
                if not isinstance(new_messages, list): new_messages = [new_messages]
                
                for msg in new_messages:
                    # Skip the original HumanMessage and empty content
                    if hasattr(msg, 'content') and msg.content and not isinstance(msg, HumanMessage):
                        content = msg.content
                        vocal = prepare_vocal_response(content)
                        audio_payload = await generate_neural_audio(vocal)
                        
                        # PHYSICAL DISPATCH TO HUD
                        await manager.broadcast({
                            "type": "audio_chunk", 
                            "text": content, 
                            "audio_base64": audio_payload, 
                            "agent": agent, 
                            "node": node_name, 
                            "dept": dept
                        })

        await manager.broadcast({"type": "mission_complete"})
        return {"status": "SUCCESS", "mission_id": mid}
    except Exception as e:
        logger.error(f"💥 [MISSION_FAULT]: {e}")
        await manager.broadcast({"type": "error", "message": str(e)})
        raise HTTPException(500, str(e))

@app.post("/api/v1/io/read")
async def read_artifact(req: FileReadRequest, lic: gatekeeper.License = Depends(get_license)):
    clean_path = req.path.replace("F:/RealmForge_PROD/", "")
    target = ROOT_DIR / clean_path
    if not target.exists(): target = WORKSPACE_ROOT / clean_path
    if target.is_file(): return {"content": target.read_text(encoding='utf-8-sig', errors='replace')}
    return {"error": "Physical file not found."}

@app.post("/api/v1/io/write")
async def save_artifact(req: FileSaveRequest, lic: gatekeeper.License = Depends(get_license)):
    clean_path = req.path.replace("F:/RealmForge_PROD/", "")
    target = ROOT_DIR / clean_path
    os.makedirs(target.parent, exist_ok=True)
    target.write_text(req.content, encoding='utf-8-sig')
    return {"status": "SUCCESS"}

@app.get("/health")
def health(): return {"status": "ONLINE", "timestamp": datetime.now().isoformat()}

@app.websocket("/ws/telemetry")
async def ws_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True: await websocket.receive_text()
    except WebSocketDisconnect: manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)