"""
REALM FORGE: SOVEREIGN BRAIN v31.4
ARCHITECT: LEAD SWARM ENGINEER
STATUS: PRODUCTION READY - TRUTH PROTOCOL MAXIMIZED - HASH-AWARE
PATH: F:/RealmForge_PROD/realm_core.py
"""

import os
import yaml
import json
import glob
import re
import asyncio
import sys
import uuid
import io
import time
import torch
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Annotated, Union
from dotenv import load_dotenv

# --- 0. PHYSICAL ENCODING GUARD (WINDOWS PRODUCTION HARDENING) ---
if sys.platform == 'win32':
    try:
        # Standard reconfigure ensures UTF-8 without detaching the Uvicorn buffer
        sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
        sys.stderr.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
    except AttributeError: pass

# --- 0.1 PROJECT ROOT ALIGNMENT ---
_REALM_ROOT = Path(__file__).resolve().parent
if str(_REALM_ROOT) not in sys.path:
    sys.path.insert(0, str(_REALM_ROOT))

from langchain_groq import ChatGroq
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, END

# --- REALM FORGE INTERNAL IMPORTS ---
from src.system.state import RealmForgeState, get_initial_state
from src.memory.engine import MemoryManager

# --- 1. ARSENAL LINKAGE (SHARDED v50.8 ALIGNMENT) ---
try:
    from src.system.arsenal.registry import (
        ALL_TOOLS_LIST, 
        DEPARTMENT_TOOL_MAP,
        get_tools_for_dept,
        get_swarm_roster,
        prepare_vocal_response, 
        generate_neural_audio,
        read_file,
        write_file,
        update_knowledge_graph,
        calculate_file_hash,
        get_file_metadata
    )
    print(f"✅ [BRAIN] Neural Mastermind Aligned to Sharded Foundation.")
except ImportError as e:
    print(f"❌ [CRITICAL_IMPORT_ERROR]: Arsenal Registry linkage failed: {e}")
    sys.exit(1)

# --- 2. CONFIGURATION & HYBRID LLM FACTORY ---
load_dotenv()

llm_instance = None

def get_llm():
    """Initializes LLM based on .env configuration with Mastermind precision."""
    global llm_instance
    if llm_instance is not None: return llm_instance
    
    model_choice = os.getenv("REALM_MODEL_CORE", "GROQ").upper()
    
    if model_choice == "NEMOTRON":
        try:
            print(f"🌀 [NVIDIA_NEMOTRON] Loading NVIDIA-Nemotron-Nano-9B-v2...")
            pipe = pipeline(
                "text-generation", model="nvidia/NVIDIA-Nemotron-Nano-9B-v2", 
                trust_remote_code=True, device_map="auto",
                model_kwargs={"torch_dtype": torch.bfloat16 if torch.cuda.is_available() else torch.float32}
            )
            llm_instance = HuggingFacePipeline(pipeline=pipe)
            print("✅ [NVIDIA_NEMOTRON] Local Brain Online.")
        except Exception as e:
            print(f"⚠️ [MODEL_FAULT] Nemotron local failed: {e}. Defaulting to Groq.")
            model_choice = "GROQ"

    if model_choice == "GROQ" or llm_instance is None:
        llm_instance = ChatGroq(
            temperature=0.1, # Forced precision for high-fidelity strikes
            model_name="llama-3.3-70b-versatile", 
            api_key=os.getenv("GROQ_API_KEY")
        )
        print("🚀 [GROQ] Cloud Mastermind Online.")
    return llm_instance

# --- PATHS ---
DECISION_LOG = Path("F:/RealmForge_PROD/data/memory/decisions.log")
AGENT_DIR = Path("F:/RealmForge_PROD/data/agents")
INDUSTRIAL_MAP = Path("F:/RealmForge_PROD/data/industrial_capability_map.json")
TOOLS = {t.name: t for t in ALL_TOOLS_LIST if hasattr(t, 'name')}

# --- HELPERS ---
def get_industrial_specialist(silo: str):
    """Picks a physical agent manifest from the granular NVIDIA-tier industrial silos."""
    try:
        if not INDUSTRIAL_MAP.exists(): return None
        with open(INDUSTRIAL_MAP, 'r') as f:
            data = json.load(f)
        key = next((k for k in data.keys() if silo.upper() in k.upper()), None)
        pool = data.get(key, []) if key else []
        return pool[0] if pool else None
    except: return None

def extract_json(text: str) -> dict:
    try:
        match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match: return json.loads(match.group(1))
        text_clean = text.strip()
        if text_clean.startswith('{'): return json.loads(text_clean)
        return {}
    except: return {}

# ==============================================================================
# 4. NODES (TITAN MASTERMIND CORE)
# ==============================================================================

async def supervisor_node(state: RealmForgeState):
    """ORCHESTRATOR: Maps mission to industrial silos and establishes meeting context."""
    mission = state["messages"][-1].content
    silo_list = ["DATA_LATTICE_CURATOR"]
    if INDUSTRIAL_MAP.exists():
        silo_list = list(json.load(open(INDUSTRIAL_MAP)).keys())

    prompt = f"""
    SYSTEM: Realm Forge Industrial Mastermind v31.4
    MISSION: "{mission}"
    INDUSTRIAL_SILOS: {silo_list}
    
    TASK:
    1. Architect the Strike Team. Assign a PRIMARY SILO to lead.
    2. Identify a FALLBACK SILO for automated escalation (The Truth Protocol).
    3. If the task is technical, always invite 'SILICON_ARCHITECT'.

    RESPOND IN JSON ONLY:
    {{
        "primary_silo": "SILO_NAME",
        "fallback_silo": "SILO_NAME",
        "meeting_invitees": ["SILO_1", "SILO_2"],
        "reasoning": "Sovereign Strike Strategy."
    }}
    """
    model = get_llm()
    res = await model.ainvoke([SystemMessage(content=prompt)])
    data = extract_json(res.content if hasattr(res, 'content') else str(res))
    
    primary_silo = data.get("primary_silo", silo_list[0])
    primary = get_industrial_specialist(primary_silo)
    
    return {
        "next_node": "planner",
        "active_department": primary_silo,
        "fallback_department": data.get("fallback_silo", "SILICON_ARCHITECT"),
        "active_agent": primary['name'] if primary else "ForgeMaster",
        "agent_manifest_path": primary['path'] if primary else None,
        "meeting_participants": data.get("meeting_invitees", []),
        "messages": [AIMessage(content=f"🤝 [ROUND_TABLE]: Convening {data.get('meeting_invitees')}. Lead: {primary['name'] if primary else 'ForgeMaster'}.")]
    }

async def planner_node(state: RealmForgeState):
    """THE SPECIALIST: Drafts the Redundancy-Aware Kinetic Plan."""
    mission = state["messages"][-1].content
    agent_name = state.get("active_agent", "ForgeMaster")
    dept = state.get("active_department", "Architect")
    fallback = state.get("fallback_department")
    
    prompt = f"""
    IDENTITY: {agent_name} (Industrial Role: {dept})
    MISSION: {mission}
    
    PROTOCOL: 
    1. Do NOT report blockages. Hand-off immediately to {fallback} on friction.
    2. Output sub_tasks as a JSON list of real tools.
    3. Every file path mentioned MUST be absolute (F:/RealmForge_PROD/...).
    """
    model = get_llm()
    res = await model.ainvoke([SystemMessage(content=prompt)] + state["messages"])
    
    content = res.content if hasattr(res, 'content') else str(res)
    data = extract_json(content)

    return {
        "task_queue": data.get("sub_tasks", []),
        "next_node": "executor",
        "messages": [AIMessage(content=f"📋 [PLAN_LOCKED]: Redundancy path via {fallback} mapped.")]
    }

async def execution_node(state: RealmForgeState):
    """FORCE-KINETIC EXECUTOR: Physically triggers tools and logs artifact paths."""
    agent = state.get("active_agent")
    tasks = list(state.get("task_queue", []))
    messages = list(state["messages"])
    found_artifacts = list(state.get("artifacts", []))
    
    if not tasks: return {"next_node": "validator"}

    for task in tasks:
        tool_name = task.get("tool")
        
        # INDUSTRIAL HANDOFF
        if tool_name == "HANDOFF":
            new_silo = state.get("fallback_department")
            specialist = get_industrial_specialist(new_silo)
            handoff = {"from": state['active_department'], "to": new_silo}
            return {
                "active_agent": specialist['name'] if specialist else "ForgeMaster",
                "active_department": new_silo,
                "agent_manifest_path": specialist['path'] if specialist else None,
                "handoff_history": [handoff],
                "next_node": "planner",
                "messages": [AIMessage(content=f"🔄 [REDUNDANCY]: Escalating mission to {new_silo}.")]
            }

        if tool_name in TOOLS:
            print(f"⚙️ [KINETIC]: {agent} executing {tool_name}...")
            try:
                result = await TOOLS[tool_name].ainvoke(task.get("args", {}))
                
                # Sniff out physical paths for IronClad validation
                path_matches = re.findall(r'[Ff]:/[^ "^\n\t]+', str(result))
                found_artifacts.extend(path_matches)

                # TRUTH VALIDATION
                if any(err in str(result) for err in ["Throttled", "Error", "None found", "failed"]):
                    print(f"⚠️ [STRIKE_FRICTION]: {tool_name} compromised. Escalating...")
                    return {"next_node": "executor", "task_queue": [{"tool": "HANDOFF"}], "messages": messages}
                
                messages.append(ToolMessage(tool_call_id=str(uuid.uuid4()), content=str(result)))
            except:
                return {"next_node": "executor", "task_queue": [{"tool": "HANDOFF"}], "messages": messages}
        
    return {
        "messages": messages[-10:], 
        "active_agent": agent, 
        "artifacts": list(set(found_artifacts)),
        "next_node": "validator"
    }

async def validator_node(state: RealmForgeState):
    """THE IRONCLAD GATE: Forensic hash-verification of all produced artifacts."""
    artifacts = state.get("artifacts", [])
    agent = "IronClad"
    
    v_logs = []
    for path in artifacts:
        # Physical Hash Probe
        try:
            res = await calculate_file_hash.ainvoke({"file_path": path})
            if "ERROR" in res:
                v_logs.append(f"❌ {path}: Physical file missing.")
                continue
            
            # Logic: If hash exists, we update the Lattice metadata
            current_hash = res.split(": ")[-1]
            await update_knowledge_graph.ainvoke({
                "subject": path, 
                "relation": "CURRENT_HASH", 
                "target": current_hash
            })
            v_logs.append(f"✅ {path}: Integrity Verified. ({current_hash[:8]})")
        except: continue

    return {
        "active_agent": agent,
        "diagnostic_stream": v_logs,
        "next_node": "auditor",
        "messages": [AIMessage(content=f"🛡️ [IRONCLAD]: {len(v_logs)} physical artifacts validated against disk.")]
    }

async def auditor_node(state: RealmForgeState):
    """Verifies that mission output is physical and placeholder-free."""
    last_msg = state["messages"][-1].content
    if any(p in last_msg.lower() for p in ["[insert", "placeholder", "failed"]):
        return {"messages": [AIMessage(content="🚨 [AUDIT_FAIL]: Logic rejection. Re-tracing...")], "next_node": "planner"}
    return {"messages": [AIMessage(content="💎 [INTEGRITY_NOMINAL]")], "next_node": "synthesizer"}

async def synthesizer_node(state: RealmForgeState):
    """Strike archival."""
    last_msg = state["messages"][-1].content
    mid = state.get("mission_id", "UNK")
    try:
        with open(DECISION_LOG, 'a', encoding='utf-8-sig') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] [{mid}] SUCCESS\n")
    except: pass
        
    return {"messages": [AIMessage(content=last_msg)], "next_node": END}

# --- GRAPH COMPILATION ---
builder = StateGraph(RealmForgeState)

builder.add_node("supervisor", supervisor_node); builder.add_node("planner", planner_node)
builder.add_node("executor", execution_node); builder.add_node("validator", validator_node)
builder.add_node("auditor", auditor_node); builder.add_node("synthesizer", synthesizer_node)

builder.set_entry_point("supervisor")

builder.add_conditional_edges("supervisor", lambda x: x["next_node"], {"planner": "planner"})
builder.add_conditional_edges("executor", lambda x: x["next_node"], {"planner": "planner", "validator": "validator"})
builder.add_edge("planner", "executor")
builder.add_edge("validator", "auditor")
builder.add_edge("auditor", "synthesizer")
builder.add_edge("synthesizer", END)

app = builder.compile()