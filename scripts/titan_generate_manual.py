"""
REALM FORGE: MASTER MANUAL GENERATOR v1.0
PURPOSE: Physically scans all 180 tools and produces the 'The Book of Tools'.
"""
import os, re
from pathlib import Path

ARSENAL_DIR = Path("F:/RealmForge_PROD/src/system/arsenal")
OUTPUT_PATH = Path("F:/RealmForge_PROD/data/ingress/execution_manual.md")

def generate():
    print("📖 [GENERATOR] Scanning shards for 180 technical signatures...")
    shards = list(ARSENAL_DIR.glob("*.py"))
    
    manual_lines = [
        "# REALM FORGE: SOVEREIGN EXECUTION MANUAL v1.0",
        "## PRIMARY DIRECTIVE: ABSOLUTE TOOL FIDELITY",
        "\n"
    ]

    for shard in shards:
        if shard.name == "foundation.py" or shard.name == "registry.py": continue
        
        content = shard.read_text(encoding='utf-8-sig')
        # Find every tool name and its docstring
        tools = re.findall(r"@tool\('(.*?)'\)\nasync def .*?:\n\s+\"\"\"(.*?)\"\"\"", content, re.DOTALL)
        
        manual_lines.append(f"### SECTOR: {shard.stem.upper()}")
        for name, doc in tools:
            clean_doc = doc.strip().replace('\n', ' ')
            manual_lines.append(f"- **{name}**: {clean_doc}")
        manual_lines.append("\n")

    OUTPUT_PATH.write_text("\n".join(manual_lines), encoding='utf-8-sig')
    print(f"✅ SUCCESS: {OUTPUT_PATH} manifested with exhaustive logic.")

if __name__ == "__main__":
    generate()