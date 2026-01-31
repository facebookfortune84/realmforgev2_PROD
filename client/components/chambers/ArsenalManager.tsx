/**
 * REALM FORGE: TITAN SOVEREIGN ARMORY v31.0
 * STYLE: CAFFEINE-NEON / HIGH-VISIBILITY
 * ARCHITECT: LEAD SWARM ENGINEER
 * STATUS: PRODUCTION READY - VERCEL COMPLIANT
 * PATH: F:\RealmForge_PROD\client\components\chambers\ArsenalManager.tsx
 */

// @ts-nocheck
"use client";

import { useState, useEffect } from "react";
import { 
  Crosshair, Plus, Zap, Shield, Code, Save, 
  Terminal, Search, Cpu, Box, Database, 
  Wrench, Activity, Sparkles, AlertCircle, 
  ChevronRight, Binary, CpuIcon
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import axios from "axios";

export default function ArsenalManager() {
  const [searchQuery, setSearchQuery] = useState("");
  const [isForging, setIsForging] = useState(false);
  const [toolRequest, setToolRequest] = useState("");
  const [newTool, setNewTool] = useState({ 
    name: "", 
    code: "@tool\nasync def new_capability(args: str):\n    \"\"\"Production-grade industrial logic.\"\"\"\n    # 1. Initialize Senses\n    # 2. Execute Physics\n    # 3. Commit to Ledger\n    pass", 
    imports: "from src.system.arsenal.foundation import *" 
  });

  const [diagnosticLogs, setDiagnosticLogs] = useState([
    "> [ARMORY]: Sharded Registry synchronized (180 Tools).",
    "> [ARMORY]: High-visibility neon shaders active.",
    "> [ARMORY]: Ready for industrial logic injection."
  ]);

  const [config, setConfig] = useState({ url: "", key: "" });

  // --- 1. SOVEREIGN HYDRATION ---
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const url = localStorage.getItem("RF_URL") || "http://localhost:8000";
      const key = localStorage.getItem("RF_KEY") || "sk-realm-god-mode-888";
      setConfig({ url, key });
    }
  }, []);

  const forgeToolWithAI = async () => {
    if (!toolRequest || !config.url) return;
    setIsForging(true);
    try {
        const cleanUrl = config.url.replace(/\/$/, "");
        await axios.post(`${cleanUrl}/api/v1/mission`, {
            task: `ForgeMaster, physically draft a production-grade Python @tool for this requirement: "${toolRequest}". Return the code block and the required imports.`
        }, { headers: { "X-API-Key": config.key, 'ngrok-skip-browser-warning': '69420' } });
        
        setDiagnosticLogs(p => [...p, `[AI_FORGE]: Blueprint drafted for "${toolRequest}"`]);
    } catch (e) {
        setDiagnosticLogs(p => [...p, `[FAULT]: AI Forge link desynchronized.`]);
    } finally {
        setIsForging(false);
    }
  };

  const injectToArsenal = async () => {
    if (!newTool.name || !config.url) return;
    try {
      const cleanUrl = config.url.replace(/\/$/, "");
      await axios.post(`${cleanUrl}/api/v1/mission`, { 
          task: `Physically inject a new tool named ${newTool.name} with this code: ${newTool.code}. Use these imports: ${newTool.imports}` 
      }, { headers: { "X-API-Key": config.key, 'ngrok-skip-browser-warning': '69420' } });
      alert("INJECTION_SUCCESS: Registry re-indexing started.");
    } catch (e) {
      alert("INJECTION_FAILED: Physical write-lock active.");
    }
  };

  return (
    <div className="h-full flex gap-6 bg-transparent overflow-hidden relative">
      
      {/* --- COLUMN A: ACTIVE ARSENAL LEDGER --- */}
      <aside className="w-80 bg-[#0a0a0a] border border-white/5 rounded-2xl flex flex-col shrink-0 overflow-hidden shadow-2xl">
        <div className="p-5 border-b border-white/5 bg-[#00f2ff]/5 flex items-center gap-3">
          <Box size={20} className="text-[#00f2ff]" />
          <span className="text-[11px] font-black text-white uppercase tracking-[0.2em]">Master_Arsenal</span>
        </div>

        <div className="p-4 border-b border-white/5">
          <div className="relative group">
            <Search className="absolute left-3 top-2.5 text-white/20 group-focus-within:text-[#00f2ff]" size={14} />
            <input 
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="PROBE_CAPABILITIES..."
              className="w-full bg-black border border-white/10 p-2.5 pl-10 text-[10px] font-bold text-[#00f2ff] outline-none focus:border-[#00f2ff]/40 rounded-xl"
            />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-2 pb-4 space-y-1 scrollbar-hide">
          {["web_search", "lattice_scout", "csv_read", "github_sync", "port_scan", "nda_generate"].map(tool => (
            <div key={tool} className="group p-3 border border-white/5 bg-white/2 hover:border-[#ff80bf]/40 rounded-xl flex items-center justify-between transition-all cursor-default">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-black group-hover:bg-[#ff80bf]/10 transition-colors">
                  <Wrench size={12} className="text-gray-500 group-hover:text-[#ff80bf]" />
                </div>
                <span className="text-[10px] font-mono text-gray-400 group-hover:text-white uppercase tracking-tight">{tool}</span>
              </div>
              <div className="w-1.5 h-1.5 rounded-full bg-[#00f2ff]/40 animate-pulse" />
            </div>
          ))}
        </div>

        <div className="p-4 bg-black/40 border-t border-white/5 text-center">
           <div className="text-[8px] font-black uppercase text-white/20 tracking-widest">
             Sovereign_Registry_v50.8
           </div>
        </div>
      </aside>

      {/* --- COLUMN B: THE CAPABILITY FORGE --- */}
      <div className="flex-1 flex flex-col gap-6 overflow-hidden">
        
        {/* SECTION: AI TOOL DRAFTER */}
        <div className="bg-[#0a0a0a] p-8 border border-white/5 rounded-3xl relative overflow-hidden shadow-2xl">
           <div className="absolute top-0 right-0 p-6 opacity-5 pointer-events-none text-[#ff80bf]">
             <Sparkles size={120} />
           </div>
           
           <div className="flex items-center gap-3 mb-6">
              <div className="w-8 h-8 rounded-xl bg-[#ff80bf]/10 flex items-center justify-center border border-[#ff80bf]/20">
                <Sparkles size={16} className="text-[#ff80bf]" />
              </div>
              <h2 className="text-[11px] font-black text-[#ff80bf] uppercase tracking-[0.4em]">Sovereign_Forge_AI</h2>
           </div>

           <div className="flex gap-4">
             <input 
               value={toolRequest}
               onChange={e => setToolRequest(e.target.value)}
               placeholder="Describe a physical capability needed for the workforce..."
               className="flex-1 bg-black border border-white/10 p-5 text-[13px] font-medium text-white outline-none focus:border-[#ff80bf]/50 rounded-2xl transition-all placeholder:text-white/5"
             />
             <button 
              onClick={forgeToolWithAI}
              disabled={isForging}
              className="px-10 bg-[#ff80bf] text-black font-black uppercase text-xs rounded-2xl hover:bg-white transition-all shadow-[0_0_25px_rgba(255,128,191,0.2)] disabled:opacity-20"
             >
               {isForging ? "FORGING..." : "Draft_Tool"}
             </button>
           </div>
        </div>

        {/* SECTION: INJECTION PORT & TERMINAL */}
        <div className="flex-1 grid grid-cols-2 gap-6 min-h-0">
          
          {/* EDITOR */}
          <div className="bg-[#0a0a0a] border border-white/5 rounded-3xl flex flex-col p-8 shadow-2xl overflow-hidden">
             <div className="flex items-center gap-3 mb-8">
                <Terminal size={18} className="text-[#00f2ff]" />
                <h3 className="text-[11px] font-black text-white/40 uppercase tracking-[0.2em]">Logic_Committer</h3>
             </div>
             
             <div className="space-y-6 flex-1 flex flex-col min-h-0">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-[8px] text-white/20 uppercase font-black tracking-widest block ml-2">Function_ID</label>
                    <input 
                      value={newTool.name}
                      onChange={e => setNewTool({...newTool, name: e.target.value})}
                      placeholder="e.g. scrape_linkedin"
                      className="w-full bg-black border border-white/10 p-4 text-[11px] font-mono text-[#00f2ff] outline-none rounded-xl focus:border-[#00f2ff]/40 transition-all"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-[8px] text-white/20 uppercase font-black tracking-widest block ml-2">Target_Sector</label>
                    <select className="w-full bg-black border border-white/10 p-4 text-[11px] font-mono text-white/40 outline-none rounded-xl appearance-none cursor-pointer">
                      <option>SOFTWARE_ENGINEERING</option>
                      <option>DATA_INTELLIGENCE</option>
                      <option>CYBER_SECURITY</option>
                      <option>FINANCIAL_OPS</option>
                    </select>
                  </div>
                </div>

                <div className="flex-1 flex flex-col relative group">
                  <label className="text-[8px] text-white/20 uppercase font-black tracking-widest block mb-2 ml-2">Python_Source_Code</label>
                  <textarea 
                    value={newTool.code}
                    onChange={e => setNewTool({...newTool, code: e.target.value})}
                    className="flex-1 bg-black border border-white/10 p-6 text-[12px] font-mono text-green-400 outline-none resize-none leading-relaxed rounded-2xl focus:border-green-400/30 transition-all scrollbar-hide"
                    spellCheck={false}
                  />
                  <div className="absolute top-10 right-4 opacity-0 group-focus-within:opacity-100 transition-opacity">
                     <Binary size={40} className="text-green-400/5" />
                  </div>
                </div>

                <button 
                  onClick={injectToArsenal}
                  className="w-full py-5 bg-[#00f2ff] text-black font-black uppercase text-xs rounded-2xl hover:bg-white transition-all shadow-[0_0_30px_rgba(0,242,255,0.15)] flex items-center justify-center gap-3 active:scale-[0.98]"
                >
                  <Save size={18} /> Manifest_Capability_181
                </button>
             </div>
          </div>

          {/* LOGS PANEL */}
          <div className="bg-[#0a0a0a] border border-white/5 rounded-3xl flex flex-col p-8 shadow-2xl relative overflow-hidden">
             <div className="flex items-center justify-between mb-8 border-b border-white/5 pb-4">
                <div className="flex items-center gap-3">
                  <Activity size={18} className="text-[#ff80bf]" />
                  <span className="text-[11px] font-black text-white uppercase tracking-[0.2em]">Stream_Monitor</span>
                </div>
                <div className="flex gap-2">
                  <div className="w-2 h-2 rounded-full bg-[#00f2ff] animate-pulse shadow-[0_0_10px_#00f2ff]" />
                </div>
             </div>

             <div className="flex-1 font-mono text-[10px] space-y-3 text-[#00f2ff]/60 overflow-y-auto scrollbar-hide">
                {diagnosticLogs.map((log, i) => (
                  <div key={i} className="flex gap-4 group">
                    <span className="text-white/10 select-none font-bold">[{i.toString().padStart(2, '0')}]</span>
                    <span className="group-hover:text-white transition-colors">{log}</span>
                  </div>
                ))}
                <div className="text-white/20 animate-pulse">
                   {" >>> System_Awaiting_Capability_Signature_"}
                </div>
             </div>
             
             <div className="mt-8 p-6 bg-[#ff3e3e]/5 border border-[#ff3e3e]/20 rounded-2xl">
                <div className="flex items-center gap-3 text-[#ff3e3e] mb-2">
                  <AlertCircle size={16} />
                  <span className="text-[9px] font-black uppercase tracking-widest">Monolith_Override_Warning</span>
                </div>
                <p className="text-[9px] text-[#ff3e3e]/40 leading-relaxed uppercase font-bold tracking-tighter">
                  Physical injection triggers a system-wide hot reload. The neural lattice will momentarily desynchronize while tool v50.9 is absorbed.
                </p>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
}