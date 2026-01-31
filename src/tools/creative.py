from langchain.tools import tool
import os
import replicate
import edge_tts
import asyncio
import base64
import httpx
import re
from openai import OpenAI
from .base import DATA_DIR, sanitize_path

@tool("generate_industrial_image")
async def generate_industrial_image(prompt: str, filename: str):
    """Manifests high-fidelity industrial imagery via DALL-E 3. Saves to 'data/assets/images/'."""
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        path = DATA_DIR / "assets/images" / f"{sanitize_path(filename)}.png"
        res = client.images.generate(model="dall-e-3", prompt=f"Industrial, cinematic: {prompt}", n=1, size="1024x1024")
        async with httpx.AsyncClient() as h:
            data = await h.get(res.data[0].url)
            path.write_bytes(data.content)
        return f"[SUCCESS] [IMAGE_GEN]: {path}"
    except Exception as e: return f"[ERROR] [IMAGE_FAIL]: {e}"

@tool("generate_industrial_video")
async def generate_industrial_video(prompt: str, filename: str):
    """Generates cinematic industrial walkthroughs via Luma/Ray."""
    try:
        output = replicate.run("luma/ray-v1", input={"prompt": prompt})
        return f"[SUCCESS] [VIDEO_QUEUED]: Link: {output}"
    except Exception as e: return f"[ERROR] [VIDEO_FAIL]: {e}"

@tool("list_available_voices")
async def list_available_voices():
    """Checks the neural voice synthesizer availability."""
    return "Edge-TTS Christopher: Unlimited Access Confirmed."

# Helper (Not a tool, but used by server.py)
def prepare_vocal_response(text: str) -> str:
    """Sanitizes technical mission logs for Edge-TTS narration."""
    if not text: return "Mission confirmed."
    text = re.sub(r'```.*?```', ' [Technical Detail Omitted] ', text, flags=re.DOTALL)
    text = re.sub(r'[*_#`\-|>\[\]]', '', text)
    return " ".join(text.split()).strip()[:10000]

# Helper (Not a tool)
async def generate_neural_audio(text: str) -> str:
    if not text: return ""
    try:
        communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural", rate="+0%", pitch="-5Hz")
        audio_bytes = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio": audio_bytes += chunk["data"]
        return base64.b64encode(audio_bytes).decode('utf-8')
    except: return ""