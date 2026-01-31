from datetime import datetime
from typing import Optional
from typing import Union
from typing import Dict
from typing import List
from typing import Any
import sqlite3

import secrets

import time

import os

import json

import logging

from pathlib import Path

from datetime import datetime

from pydantic import BaseModel, Field

from typing import Optional, List, Dict, Union, Any



# --- 0. PATH SOVEREIGNTY ---

# Calculates root from src/auth/gatekeeper.py (2 levels up)

ROOT_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

BASE_PATH = ROOT_DIR / "data"

DB_PATH = BASE_PATH / "security" / "licenses.db"



# Ensure the security directory exists physically

os.makedirs(DB_PATH.parent, exist_ok=True)



logger = logging.getLogger("Gatekeeper")



# MASTER ACCESS KEY (God Mode Override)

MASTER_KEY = os.getenv("REALM_MASTER_KEY", "sk-realm-god-mode-888")



# ==============================================================================

# 1. DATA MODELS

# ==============================================================================



class License(BaseModel):

    """
from pydantic import Field
from typing import Union
from typing import Dict
from typing import List
from typing import Any

    Sovereign License Model.

    Standardized for Pydantic v2 validation in FastAPI/Gateway layers.

    """

    key: str

    user_id: str

    tier: str  # "FREE", "PRO", "TITAN", "GOD"

    credits: int

    created_at: float

    status: str = "ACTIVE"

    metadata: Dict[str, Any] = Field(default_factory=dict)



# ==============================================================================

# 2. CORE DATABASE OPERATIONS

# ==============================================================================



def init_auth_db():

    """Initializes the security database with High-Concurrency (WAL) mode."""

    conn = sqlite3.connect(DB_PATH)

    c = conn.cursor()

    

    # Enable WAL mode for multi-agent concurrency

    c.execute("PRAGMA journal_mode=WAL")

    

    # Main License Table

    c.execute('''CREATE TABLE IF NOT EXISTS licenses

                 (key text PRIMARY KEY, 

                  user_id text, 

                  tier text, 

                  credits integer, 

                  created_at real,

                  status text DEFAULT 'ACTIVE',

                  metadata text DEFAULT '{}')''')

    

    # Usage Audit Table: Crucial for Workforce Compliance & Monetization

    c.execute('''CREATE TABLE IF NOT EXISTS usage_logs

                 (id INTEGER PRIMARY KEY AUTOINCREMENT,

                  key text,

                  agent_id text,

                  mission_id text,

                  task_summary text,

                  cost integer,

                  timestamp real)''')

    

    conn.commit()

    conn.close()

    logger.info(f"🔐 [GATEKEEPER] Neural Security Lattice Active (WAL Mode): {DB_PATH}")



def generate_key(user_id: str, tier: str = "FREE", custom_metadata: Dict = None) -> str:

    """Mints a new high-security API Key with tier-based credits."""

    tier = tier.upper()

    prefix = f"rf_{tier.lower()}_"

    api_key = prefix + secrets.token_urlsafe(32)

    

    allotment = {

        "FREE": 50,

        "PRO": 5000,

        "TITAN": 250000,

        "GOD": 999999999

    }

    initial_credits = allotment.get(tier, 50)

    meta_json = json.dumps(custom_metadata or {})

    

    try:

        conn = sqlite3.connect(DB_PATH)

        c = conn.cursor()

        c.execute("""INSERT INTO licenses (key, user_id, tier, credits, created_at, metadata) 

                     VALUES (?, ?, ?, ?, ?, ?)""", 

                  (api_key, user_id, tier, initial_credits, time.time(), meta_json))

        conn.commit()

        conn.close()

        logger.info(f"[NEW] [KEY_GEN] New {tier} key issued for {user_id}")

        return api_key

    except Exception as e:

        logger.error(f"[ERROR] [KEY_GEN_FAULT]: {e}")

        return None



def validate_key(api_key: str) -> Optional[License]:

    """Validates key existence, status, and Master-Key bypass."""

    

    # 1. Master Override (God Mode)

    if api_key == MASTER_KEY:

        return License(

            key=MASTER_KEY,

            user_id="ROOT_ARCHITECT",

            tier="GOD",

            credits=999999999,

            created_at=time.time(),

            status="ACTIVE",

            metadata={"privilege": "UNRESTRICTED"}

        )



    # 2. Database Lookup

    try:

        conn = sqlite3.connect(DB_PATH)

        c = conn.cursor()

        c.execute("""SELECT key, user_id, tier, credits, created_at, status, metadata 

                     FROM licenses WHERE key=?""", (api_key,))

        row = c.fetchone()

        conn.close()

        

        if row:

            try: meta_dict = json.loads(row[6])

            except: meta_dict = {}



            lic = License(

                key=row[0], user_id=row[1], tier=row[2], 

                credits=row[3], created_at=row[4], status=row[5],

                metadata=meta_dict

            )

            

            if lic.status != "ACTIVE":

                logger.warning(f"🚫 [ACCESS_BLOCKED] Key {api_key[:12]}... is INACTIVE")

                return None

            return lic

            

    except Exception as e:

        logger.error(f"[ERROR] [SECURITY_FAULT]: {e}")

    

    return None



def deduct_credit(api_key: str, cost: int = 1, mission_id: str = "MSN-UNK", task_context: str = "Mission", agent_id: str = "NEXUS"):

    """

    Transactional credit deduction with high-concurrency protection.

    Correlates agent contributions with Mission IDs for the workforce ledger.

    """

    if api_key == MASTER_KEY:

        return True



    try:

        conn = sqlite3.connect(DB_PATH, timeout=20)

        c = conn.cursor()

        

        # Atomic deduction

        c.execute("UPDATE licenses SET credits = credits - ? WHERE key = ? AND credits >= ?", 

                  (cost, api_key, cost))

        

        if c.rowcount > 0:

            c.execute("""INSERT INTO usage_logs (key, agent_id, mission_id, task_summary, cost, timestamp) 

                         VALUES (?, ?, ?, ?, ?, ?)""",

                      (api_key, agent_id, mission_id, task_context[:200], cost, time.time()))

            conn.commit()

            conn.close()

            return True

        

        conn.close()

    except Exception as e:

        logger.error(f"[ERROR] [DEDUCTION_FAULT]: {e}")

        

    return False



def get_account_vitals(api_key: str) -> Dict[str, Any]:

    """Retrieves account balance and workforce status for the HUD."""

    lic = validate_key(api_key)

    if not lic:

        return {"status": "INVALID_LICENSE"}

    

    return {

        "user_id": lic.user_id,

        "tier": lic.tier,

        "balance": lic.credits,

        "registration_status": lic.status,

        "metadata": lic.metadata

    }



# BOOTSTRAP SECURITY LAYER ON MODULE LOAD

init_auth_db()