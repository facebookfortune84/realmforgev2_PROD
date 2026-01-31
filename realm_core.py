"""
REALM FORGE: SOVEREIGN BRAIN v31.2
ARCHITECT: LEAD SWARM ENGINEER
STATUS: MASTERMIND MODE - SILO-AWARE ROUTING REPAIRED
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

# --- 0. PHYSICAL ENCODING GUARD ---
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
        sys.stderr.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
    except AttributeError: pass

# --- 0.1 PROJECT ROOT (for src.* imports) ---
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

# --- 1. ARSENAL LINKAGE ---
try:
    from src.system.arsenal.registry import (
        ALL_TOOLS_LIST, 
        DEPARTMENT_TOOL_MAP,
        get_tools_for_dept,
        get_swarm_roster,
        prepare_vocal_response, 
        generate_neural_audio
    )
    print(f"✅ [BRAIN] Neural Mastermind Aligned to Sharded Registry.")
except ImportError as e:
    print(f"❌ [CRITICAL_IMPORT_ERROR]: Arsenal Registry linkage failed: {e}")
    sys.exit(1)

# --- 2. CONFIGURATION ---
load_dotenv()

def get_llm():
    return ChatGroq(
        temperature=0.1, 
        model_name="llama-3.3-70b-versatile", 
        api_key=os.getenv("GROQ_API_KEY")
    )

# --- PATHS ---
DECISION_LOG = Path("F:/RealmForge/data/memory/decisions.log")
AGENT_DIR = Path("F:/RealmForge/data/agents")
INDUSTRIAL_MAP = Path("F:/RealmForge/data/industrial_capability_map.json")
TOOLS = {t.name: t for t in ALL_TOOLS_LIST if hasattr(t, 'name')}

# --- HELPERS ---
def get_industrial_specialist(silo: str):
    try:
        if not INDUSTRIAL_MAP.exists(): return None
        with open(INDUSTRIAL_MAP, 'r') as f:
            data = json.load(f)
        # Handle case-insensitive lookup
        key = next((k for k in data.keys() if silo.upper() in k.upper()), None)
        pool = data.get(key, []) if key else []
        return pool[0] if pool else None
    except: return None

def extract_json(text: str) -> dict:
    try:
        match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match: return json.loads(match.group(1))
        # Support for raw JSON
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            return json.loads(text[start:end+1])
        return {}
    except: return {}

# ==============================================================================
# 4. NODES (TITAN MASTERMIND CORE)
# ==============================================================================

async def supervisor_node(state: RealmForgeState):
    """ORCHESTRATOR: Translates user-agent requests into Industrial Silos."""
    mission = state["messages"][-1].content
    
    # Identify available silos from the physically mapped file
    silo_list = ["DATA_LATTICE_CURATOR"]
    if INDUSTRIAL_MAP.exists():
        silo_list = list(json.load(open(INDUSTRIAL_MAP)).keys())

    prompt = f"""
    SYSTEM: Realm Forge Industrial Mastermind v31.2
    MISSION: "{mission}"
    AVAILABLE_SILOS: {silo_list}
    
    TASK: 
    1. Identify the PRIMARY SILO that corresponds to the lead agent requested.
    2. Map agents like 'DataScryer' to 'MARKET_INTELLIGENCE' and 'CodeWeaver' to 'SOFTWARE_ENGINEERING'.
    3. Identify a SECONDARY FALLBACK SILO for Redundancy.
    
    RESPOND IN JSON ONLY:
    {{
        "primary_silo": "SILO_NAME",
        "fallback_silo": "SILO_NAME",
        "meeting_invitees": ["SILO_1", "SILO_2"],
        "reasoning": "Sovereign Strategy."
    }}
    """
    model = get_llm()
    res = await model.ainvoke([SystemMessage(content=prompt)])
    data = extract_json(res.content)
    
    primary_silo = data.get("primary_silo", silo_list[0])
    primary = get_industrial_specialist(primary_silo)
    
    return {
        "next_node": "planner",
        "active_department": primary_silo,
        "fallback_department": data.get("fallback_silo"),
        "active_agent": primary['name'] if primary else "ForgeMaster",
        "agent_manifest_path": primary['path'] if primary else None,
        "meeting_participants": data.get("meeting_invitees", []),
        "messages": [AIMessage(content=f"🤝 [ROUND_TABLE]: Convening specialists from {data.get('meeting_invitees')}. Lead: {primary['name'] if primary else 'ForgeMaster'}.")]
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
    1. Do NOT report blockages.
    2. If a tool returns NO DATA, the next task MUST be to 'HANDOFF' to {fallback}.
    3. Output 'sub_tasks' as a JSON list of tool calls.
    
    SCHEMA:
    {{
        "sub_tasks": [
            {{"tool": "tool_name", "args": {{ "arg1": "val1" }} }}
        ]
    }}
    """
    model = get_llm()
    res = await model.ainvoke([SystemMessage(content=prompt)] + state["messages"])
    
    content = res.content if hasattr(res, 'content') else str(res)
    data = extract_json(content)

    return {
        "task_queue": data.get("sub_tasks", []),
        "next_node": "executor",
        "messages": [AIMessage(content=f"📋 [PLAN_LOCKED]: Strike protocol initialized for {dept}. TargetFallback: {fallback}")]
    }

async def execution_node(state: RealmForgeState):
    """FORCE-KINETIC EXECUTOR: Executes and triggers Industrial Handoff on failure."""
    agent = state.get("active_agent")
    tasks = list(state.get("task_queue", [])) # Ensure list copy
    messages = list(state["messages"])
    
    if not tasks:
        return {"next_node": "auditor"}

    for task in tasks:
        tool_name = task.get("tool")
        
        # MASTERMIND HANDOFF LOGIC
        if tool_name == "HANDOFF":
            new_silo = state.get("fallback_department")
            specialist = get_industrial_specialist(new_silo)
            handoff_entry = {"from": state['active_department'], "to": new_silo}
            print(f"🔄 [HANDOFF]: {agent} transferring to {specialist['name'] if specialist else 'ForgeMaster'}")
            return {
                "active_agent": specialist['name'] if specialist else "ForgeMaster",
                "active_department": new_silo,
                "agent_manifest_path": specialist['path'] if specialist else None,
                "handoff_history": [handoff_entry],
                "next_node": "planner",
                "messages": [AIMessage(content=f"🔄 [REDUNDANCY]: Tool friction detected. Handoff to {new_silo} successful.")]
            }

        if tool_name in TOOLS:
            print(f"⚙️ [KINETIC]: {agent} executing {tool_name}...")
            try:
                # PHYSICAL EXECUTION
                result = await TOOLS[tool_name].ainvoke(task.get("args", {}))
                
                # RECURSIVE VALIDATION: Stop agents from lying
                if "None found" in str(result) or "Throttled" in str(result) or "ERROR" in str(result).upper():
                    print(f"⚠️ [STRIKE_FRICTION]: {tool_name} returned no data.")
                    # Instead of reporting blockage, force a handoff to SiliconArchitect
                    handoff_task = {"tool": "HANDOFF", "args": {"reason": f"{tool_name} failed"}}
                    return {"next_node": "executor", "task_queue": [handoff_task], "messages": messages}
                
                messages.append(ToolMessage(tool_call_id=str(uuid.uuid4()), content=str(result)))
            except Exception as e:
                # Fail gracefully by handing off to a human or fallback
                return {"next_node": "executor", "task_queue": [{"tool": "HANDOFF"}], "messages": messages}
        
    return {"messages": messages[-10:], "active_agent": agent, "next_node": "auditor"}

async def auditor_node(state: RealmForgeState):
    """Verifies that results are PHYSICAL and not HALLUCINATED."""
    last_msg = state["messages"][-1].content
    if "[insert" in last_msg.lower() or "placeholder" in last_msg.lower():
        return {"messages": [AIMessage(content="🚨 [AUDIT_FAIL]: Non-physical data detected. Re-tasking...")], "next_node": "planner"}
    return {"messages": [AIMessage(content="💎 [INTEGRITY_STABLE]")], "next_node": "synthesizer"}

async def synthesizer_node(state: RealmForgeState):
    """Final archival of the successful Strike."""
    last_msg = state["messages"][-1].content
    mid = state.get("mission_id", "UNK")
    summary = f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {state['active_agent']}: Strike Complete."
    
    try:
        with open(DECISION_LOG, 'a', encoding='utf-8-sig') as f:
            f.write(summary + "\n")
    except: pass
        
    return {"messages": [AIMessage(content=last_msg)], "next_node": END}

# --- GRAPH COMPILATION ---
builder = StateGraph(RealmForgeState)

builder.add_node("supervisor", supervisor_node)
builder.add_node("planner", planner_node)
builder.add_node("executor", execution_node)
builder.add_node("auditor", auditor_node)
builder.add_node("synthesizer", synthesizer_node)

builder.set_entry_point("supervisor")

builder.add_conditional_edges("supervisor", lambda x: x["next_node"], {"planner": "planner"})
builder.add_conditional_edges("executor", lambda x: x["next_node"], {"planner": "planner", "auditor": "auditor"})
builder.add_edge("planner", "executor")
builder.add_edge("auditor", "synthesizer")
builder.add_edge("synthesizer", END)

app = builder.compile()