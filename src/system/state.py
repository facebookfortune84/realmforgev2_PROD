"""
REALM FORGE: SOVEREIGN STATE BEDROCK v18.0
ARCHITECT: LEAD SWARM ENGINEER
STATUS: PRODUCTION READY - UI REDESIGN ALIGNED
"""

import operator
import uuid
from datetime import datetime
from typing import Annotated, List, Dict, Any, TypedDict, Union, Optional
from langchain_core.messages import BaseMessage

# ==============================================================================
# 0. REDUCER LOGIC (KINETIC STATE SYNCHRONIZATION)
# ==============================================================================

def merge_tasks(existing: List[Dict], new: List[Dict]) -> List[Dict]:
    """Sovereign Task Merger: Ensures the mission backlog is unique and sorted."""
    if not isinstance(existing, list): existing = []
    if not isinstance(new, list): new = []
    
    task_map = {t.get('id'): t for t in existing if t.get('id')}
    
    for t in new:
        if not isinstance(t, dict): continue
        tid = t.get('id') or f"task_{uuid.uuid4().hex[:6]}"
        t['id'] = tid
        
        if tid in task_map:
            task_map[tid] = {**task_map[tid], **t} # Update existing
        else:
            task_map[tid] = t # Append new

    return sorted(
        list(task_map.values()), 
        key=lambda x: (x.get('status', 'OPEN') != 'OPEN', x.get('priority', 'MEDIUM'), x.get('id', ''))
    )

def merge_vitals(existing: Dict, new: Dict) -> Dict:
    """Telemetry Merger: Updates real-time HUD vitals without losing historical keys."""
    if not existing: existing = {}
    if not new: return existing
    return {**existing, **new}

def track_handoffs(existing: List[Dict], new: List[Dict]) -> List[Dict]:
    """Spatial Handoff Reducer: Records the flow of data between industrial sectors."""
    if not existing: existing = []
    if not new: return existing
    return (existing + new)[-10:] # Keep last 10 handoffs for UI visualization

def buffer_diagnostics(existing: List[str], new: List[str]) -> List[str]:
    """Diagnostic Stream Reducer: Manages the 'Glassmorphism' terminal buffer."""
    if not existing: existing = []
    if not new: return existing
    # Maintain a rolling buffer of 50 diagnostic lines
    return (existing + new)[-50:]

def merge_genesis_protocol(existing: Dict[str, bool], new: Dict[str, bool]) -> Dict[str, bool]:
    """Genesis-100 Tracker: Monitors the 100 initialization tasks."""
    if not existing: existing = {}
    if not new: return existing
    return {**existing, **new}

# ==============================================================================
# 1. STATE DEFINITION (THE TITAN-INDUSTRIAL SCHEMA)
# ==============================================================================

class RealmForgeState(TypedDict):
    """
    The Global Sovereign State for RealmForge.
    Engineered for the Grand Finale UI and Multi-Agent Industrial Meetings.
    """
    # --- 1. CORE COMMUNICATION ---
    messages: Annotated[List[BaseMessage], operator.add]
    mission_id: str
    
    # --- 2. IDENTITY & ROUTING ---
    next_node: str 
    active_agent: str      # Current persona in control
    active_department: str # Current active sector (presents as 'Glowing' in UI)
    
    # --- 3. MEETING MODE (THE ROUND TABLE) ---
    meeting_participants: List[str] # List of Agent IDs currently in the thread
    handoff_history: Annotated[List[Dict[str, str]], track_handoffs] # {from: sector, to: sector}
    
    # --- 4. TASK MANAGEMENT ---
    task_queue: Annotated[List[Dict[str, Any]], merge_tasks] 
    genesis_tasks: Annotated[Dict[str, bool], merge_genesis_protocol] # The 100 startup tasks
    
    # --- 5. DATA LATTICE & ARTIFACTS ---
    memory_context: str
    artifacts: Annotated[List[str], lambda x, y: list(set((x or []) + (y or [])))]
    
    # --- 6. TELEMETRY & DIAGNOSTICS ---
    vitals: Annotated[Dict[str, Any], merge_vitals]
    diagnostic_stream: Annotated[List[str], buffer_diagnostics]
    
    # --- 7. METADATA ---
    metadata: Dict[str, Any]

# ==============================================================================
# 2. INITIALIZATION (THE CLEAN SLATE)
# ==============================================================================

def get_initial_state() -> RealmForgeState:
    """
    Titan Factory: Initializes the swarm in 'Architect' mode.
    Pre-populates basic Genesis Protocol placeholders.
    """
    return {
        "messages": [],
        "mission_id": f"MSN-{uuid.uuid4().hex[:8].upper()}",
        "next_node": "supervisor",
        "active_agent": "ForgeMaster",
        "active_department": "Architect", 
        "meeting_participants": ["ForgeMaster"],
        "handoff_history": [],
        "task_queue": [],
        "genesis_tasks": {
            "discord_link_13_sectors": False,
            "workforce_audit_init": True,
            "arsenal_180_verification": True,
            "lattice_node_ingestion": False
        },
        "memory_context": "Neural uplink stable. Awaiting directive.",
        "artifacts": [],
        "vitals": {
            "ram": 0.0, 
            "cpu": 0.0, 
            "latency": 0.0, 
            "lattice_nodes": 13472,
            "active_sector": "Architect"
        },
        "diagnostic_stream": [f"[{datetime.now().strftime('%H:%M:%S')}] System pressurized. Mastermind online."],
        "metadata": {
            "session_id": str(uuid.uuid4()),
            "start_time": datetime.now().isoformat(),
            "version": "18.0.0",
            "ui_theme": "Titan-Industrial"
        }
    }