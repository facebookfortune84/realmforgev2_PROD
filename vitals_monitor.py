"""
REALM FORGE: SOVEREIGN PERSISTENT MONITOR v2.1
ARCHITECT: LEAD SWARM ENGINEER (MASTERMIND v31.4)
STATUS: PRODUCTION LIVE MONITOR - COLOR CALIBRATED
PATH: F:/RealmForge_PROD/vitals_monitor.py
"""

import os
import json
import sys
import time
import psutil
from pathlib import Path
from datetime import datetime

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.live import Live
    from rich import box
    from rich.layout import Layout
except ImportError:
    print("Please install rich: pip install rich")
    sys.exit(1)

# --- PHYSICAL ANCHORS ---
ROOT_DIR = Path("F:/RealmForge_PROD")
LATTICE_PATH = ROOT_DIR / "master_departmental_lattice.json"
# Neon Palette Calibration
CYAN = "#00f2ff"
MAGENTA = "#ff007f"
BUBBLEGUM = "#ff80bf"

console = Console()

def get_vitals():
    """Real-time system stats."""
    try:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        threads = psutil.Process().num_threads()
    except:
        cpu, ram, threads = 0, 0, 0
        
    return {
        "cpu": cpu,
        "ram": ram,
        "threads": threads,
        "time": datetime.now().strftime("%H:%M:%S")
    }

def generate_dashboard():
    """Generates the high-fidelity UI with ANSI-compliant colors."""
    v = get_vitals()
    
    # Header Panel (Using Magenta instead of Pink)
    header = Panel(
        f"[bold {CYAN}]REALM FORGE COMMAND CENTER[/bold {CYAN}] | [dim]v60.5 SOVEREIGN[/dim]\n"
        f"[bold white]STATUS: ASCENSION ACTIVE[/bold white] | [dim]Local_Time: {v['time']}[/dim]",
        border_style=CYAN, box=box.DOUBLE_EDGE
    )

    # Vitals Table
    v_table = Table(expand=True, box=box.SIMPLE, border_style=CYAN)
    v_table.add_column("METRIC", style=f"bold white")
    v_table.add_column("VALUE", justify="right")
    v_table.add_row("CPU Load", f"{v['cpu']}%")
    v_table.add_row("RAM Usage", f"{v['ram']}%")
    v_table.add_row("Active Threads", str(v['threads']))

    # Silo Integrity Table
    s_table = Table(expand=True, box=box.SIMPLE, border_style=MAGENTA)
    s_table.add_column("SILO_ID", style=f"bold {BUBBLEGUM}")
    s_table.add_column("AGENTS", justify="right")
    s_table.add_column("STATUS", justify="center")

    try:
        if LATTICE_PATH.exists():
            with open(LATTICE_PATH, 'r', encoding='utf-8') as f:
                lattice = json.load(f)
            for silo, data in lattice.items():
                count = len(data.get('agents', []))
                status = "[bold green]ONLINE" if count > 0 else "[bold yellow]EMPTY"
                s_table.add_row(silo, str(count), status)
        else:
            s_table.add_row("LATTICE", "0", "[bold red]FILE_MISSING")
    except Exception as e:
        s_table.add_row("LATTICE", "0", "[bold red]READ_ERROR")

    # Layout Construction
    layout = Layout()
    layout.split_column(
        Layout(header, size=4),
        Layout(name="main", ratio=1)
    )
    layout["main"].split_row(
        Layout(Panel(v_table, title=f"[{CYAN}]System Vitals", border_style=CYAN)),
        Layout(Panel(s_table, title=f"[{MAGENTA}]Industrial Lattice", border_style=MAGENTA))
    )
    
    return layout

def start_monitor():
    """Initializes the live telemetry stream."""
    with Live(generate_dashboard(), refresh_per_second=1, screen=True) as live:
        try:
            while True:
                live.update(generate_dashboard())
                time.sleep(1)
        except KeyboardInterrupt:
            pass # Exit gracefully
        except Exception as e:
            console.print(f"[bold red]Monitor Error: {e}[/bold red]")

if __name__ == "__main__":
    start_monitor()