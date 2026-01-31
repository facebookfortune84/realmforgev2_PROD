from langchain.tools import tool
import httpx
from playwright.async_api import async_playwright

@tool("interact_web")
async def interact_web(url: str, action: str = "read"):
    """Headless vision research tool (Playwright)."""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, wait_until="networkidle", timeout=30000)
            text = await page.inner_text("body")
            await browser.close()
            return f"### [RECON]: {url}\n\n{text[:5000]}"
    except Exception as e: return f"[ERROR] [VISION_FAIL]: {e}"

@tool("inspect_api_schema")
async def inspect_api_schema(docs_url: str):
    """Downloads API schemas."""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(docs_url, timeout=15.0)
            return f"### [API_SCHEMA]:\n{resp.text[:3000]}"
    except Exception as e: return f"[ERROR] [SCHEMA_ERROR]: {str(e)}"