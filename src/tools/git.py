from langchain.tools import tool

import subprocess

import asyncio

import os

import httpx

from .base import ROOT_DIR, sanitize_path



@tool("sync_repository")

async def sync_repository(commit_message: str = "Swarm State Alignment"):

    """
import jsonAutomated Bidirectional Git Sync."""

    def _run_git():

        try:

            subprocess.run(["git", "add", "."], check=True, cwd=str(ROOT_DIR))

            subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, cwd=str(ROOT_DIR))

            subprocess.run(["git", "pull", "origin", "main", "--rebase", "-Xtheirs"], capture_output=True, cwd=str(ROOT_DIR))

            push_res = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True, cwd=str(ROOT_DIR))

            return push_res

        except Exception as e: return e

    res = await asyncio.to_thread(_run_git)

    return "[SUCCESS] [SYNC_SUCCESS]" if hasattr(res, 'returncode') and res.returncode == 0 else f"[ERROR] [SYNC_FAIL]"



@tool("push_to_github")

async def push_to_github(file_path: str, content: str, commit_message: str):

    """Atomic write to GitHub Cloud."""

    token = os.getenv("GITHUB_TOKEN"); repo = os.getenv("GITHUB_REPO")

    if not token or not repo: return "[ERROR] [AUTH_ERROR]"

    url = f"https://api.github.com/repos/{repo}/contents/{sanitize_path(file_path)}"

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"}

    async with httpx.AsyncClient() as client:

        try:

            resp = await client.get(url, headers=headers)

            sha = resp.json().get("sha") if resp.status_code == 200 else None

            import base64

            payload = {"message": commit_message, "content": base64.b64encode(content.encode()).decode(), "branch": "main"}

            if sha: payload["sha"] = sha

            await client.put(url, headers=headers, json=payload)

            return f"### [CLOUD_SYNC_SUCCESS]: {file_path}"

        except Exception as e: return f"[ERROR] [GITHUB_FAIL]: {str(e)}"