from langchain.tools import tool
import os
from .base import ROOT_DIR, DATA_DIR, STATIC_DIR, sanitize_path

@tool("write_file")
async def write_file(file_path: str, content: str):
    """Writes data to the physical disk using ABSOLUTE PATHS."""
    try:
        clean_path = file_path.replace("data/", "").replace("static/", "").replace("\\", "/")
        
        if file_path.startswith("static/"):
            target = STATIC_DIR / clean_path.replace("deployments/", "")
            target = STATIC_DIR / "deployments" / clean_path.replace("deployments/", "")
        else:
            target = DATA_DIR / clean_path

        os.makedirs(target.parent, exist_ok=True)
        with open(target, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return f"[SUCCESS] [WRITE_SUCCESS]: Saved to {target}"
    except Exception as e: return f"[ERROR] [WRITE_FAIL]: {e}"

@tool("read_file")
async def read_file(file_path: str):
    """Reads a file from disk."""
    try:
        clean_path = file_path.replace("data/", "").replace("static/", "")
        if file_path.startswith("static/"):
             target = STATIC_DIR / "deployments" / clean_path.replace("deployments/", "")
             if not target.exists(): target = STATIC_DIR / clean_path
        else:
            target = DATA_DIR / clean_path
            
        if not target.exists(): return "[ERROR] [FILE_NOT_FOUND]"
        with open(target, 'r', encoding='utf-8') as f: return f.read()
    except Exception as e: return f"[ERROR] [READ_FAIL]: {e}"

@tool("list_files")
async def list_files(directory: str = "."):
    """Provides a manifest of files."""
    try:
        clean_path = directory.replace("data/", "").replace("static/", "")
        target = DATA_DIR / clean_path
        if not target.exists(): return "[ERROR] [DIR_NOT_FOUND]"
        return f"### [MANIFEST]: {directory}\n" + "\n".join(os.listdir(target))
    except Exception as e: return f"[ERROR] [LIST_FAIL]: {e}"

@tool("grep_files")
async def grep_files(pattern: str, directory: str = "."):
    """Regex search across project data."""
    import re
    import asyncio
    def _run():
        res = []
        target = DATA_DIR / str(directory).replace("..", "").replace("data/", "")
        for f in target.rglob('*'):
            if f.is_file():
                try:
                    if re.search(pattern, f.read_text(errors='ignore')): res.append(str(f.relative_to(DATA_DIR)))
                except: continue
        return res
    results = await asyncio.to_thread(_run)
    return f"### [GREP]: {pattern}\n" + "\n".join(results[:10])