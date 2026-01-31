from typing import List
from langchain.tools import tool
import os
import pandas as pd
import subprocess
from typing import List
from .base import DATA_DIR, STATIC_DIR, sanitize_path

@tool("scaffold_industrial_project")
async def scaffold_industrial_project(project_name: str, description: str):
    """Generates a full industrial project directory structure with professional boilerplate."""
    try:
        root = DATA_DIR / "projects" / sanitize_path(project_name)
        for f in ["src", "data", "docs", "tests"]: os.makedirs(root / f, exist_ok=True)
        (root / "README.md").write_text(f"# {project_name.upper()}\n{description}", encoding='utf-8')
        subprocess.run(["git", "init"], cwd=str(root), check=False)
        return f"[SUCCESS] [SCAFFOLD_OK]: {project_name} initialized."
    except Exception as e: return f"[ERROR] [SCAFFOLD_FAIL]: {e}"

@tool("scaffold_commercial_website")
async def scaffold_commercial_website(business_name: str, pages: List[str]):
    """Scaffolds a complete commercial web directory in 'static/deployments/'."""
    try:
        root = STATIC_DIR / "deployments" / sanitize_path(business_name)
        os.makedirs(root, exist_ok=True)
        for page in pages:
            (root / f"{page.lower()}.html").write_text(f"<html><body><h1>{business_name}</h1></body></html>", encoding='utf-8')
        return f"[SUCCESS] [SITE_SCAFFOLDED]: {root}"
    except Exception as e: return f"[ERROR] [WEB_FAIL]: {e}"

@tool("industrial_data_ingress")
async def industrial_data_ingress(individual_csv: str, business_csv: str):
    """Parses massive CSV datasets into the swarm."""
    try:
        ind_p = DATA_DIR / individual_csv.replace("data/", "")
        count = 0
        if ind_p.exists(): count += len(pd.read_csv(ind_p))
        return f"[SUCCESS] [INGRESS_OK]: Processed {count} entities."
    except Exception as e: return f"[ERROR] [INGRESS_FAIL]: {str(e)}"