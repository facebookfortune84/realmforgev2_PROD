from langchain.tools import tool
import asyncio
from .base import ROOT_DIR

@tool("run_terminal_command")
async def run_terminal_command(command: str, rationale: str):
    """Executes shell commands. RESTRICTED but capable."""
    allowed = ["python", "pip", "ls", "dir", "echo", "mkdir", "del", "rm", "node", "npm", "npx", "git", "move", "copy", "type"]
    
    clean_cmd = command.strip().lower()
    if not any(clean_cmd.startswith(p) for p in allowed):
        return "[ERROR] [SECURITY]: Command not allowed."
    
    if "rm -rf /" in clean_cmd or "format c:" in clean_cmd:
        return "[ERROR] [SECURITY]: Destructive command blocked."
    
    try:
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(ROOT_DIR)
        )
        stdout, stderr = await proc.communicate()
        return f"### [SHELL]: {command}\n{stdout.decode() or stderr.decode()}"
    except Exception as e: return f"[ERROR] [EXEC_ERROR]: {e}"

@tool("ask_human")
async def ask_human(question: str):
    """Stops execution to ask the human Operator for clarification."""
    return f"__HUMAN_INTERACTION_REQUIRED__: {question}"