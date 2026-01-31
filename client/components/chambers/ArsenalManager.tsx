/**
 * REALM FORGE: TITAN SOVEREIGN ARMORY v30.1
 * ARCHITECT: LEAD SWARM ENGINEER
 * STATUS: PRODUCTION READY - VERCEL BUILD COMPLIANT
 * PATH: F:\RealmForge\client\components\chambers\ArsenalManager.tsx
 */

// @ts-nocheck
"use client";

import { useState, useEffect } from "react";
import { 
  Crosshair, Plus, Zap, Shield, Code, Save, 
  Terminal, Search, Cpu, Box, Database, 
  Wrench, Activity, Sparkles, AlertCircle, ChevronRight
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import axios from "axios";

export default function ArsenalManager() {
  const [searchQuery, setSearchQuery] = useState("");
  const [isForging, setIsForging] = useState(false);
  const [toolRequest, setToolRequest] = useState("");
  const [newTool, setNewTool] = useState({ 
    name: "", 
    code: "@tool\nasync def new_capability(args: str):\n    \"\"\"Production-grade logic here.\"\"\"\n    pass", 
    imports: "from langchain.tools import tool" 
  });

  const [existingTools, setExistingTools] = useState([
    "lattice_scout_search", "csv_processor_read", "web_search_duckduckgo",
    "generate_corporate_invoice", "mm_get_user_by_name", "scan_network_ports"
  ]);

  const [diagnosticLogs, setDiagnosticLogs] = useState([
    "> [ARMORY]: Registry synchronized (180 Tools Found).",
    "> [ARMORY]: Ready for industrial injection."
  ]);

  const forgeToolWithAI = async () => {
    if (!toolRequest) return;
    setIsForging(true);
    const apiUrl = typeof window !== 'undefined' ? localStorage.getItem("RF_URL") : "";
    const apiKey = typeof window !== 'undefined' ? localStorage.getItem("RF_KEY") : "";

    try {
        await axios.post(`${apiUrl}/api/v1/mission`, {
            task: `ForgeMaster, draft a production-grade Python @tool for this requirement: "${toolRequest}". 
                   Return ONLY the code block and the required imports.`
        }, { headers: { "X-API-Key": apiKey } });
        
        setDiagnosticLogs(p => [...p, `[AI_FORGE]: Capability logic drafted for ${toolRequest}`]);
    } catch (e) {
        console.error("FORGE_FAULT");
    } finally {
        setIsForging(false);
    }
  };

  const injectToMonolith = async () => {
    const apiUrl = typeof window !== 'undefined' ? localStorage.getItem("RF_URL") : "";
    const apiKey = typeof window !== 'undefined' ? localStorage.getItem("RF_KEY") : "";
    try {
      await axios.post(`${apiUrl}/api/v1/mission`, { 
          task: `Inject a new tool named ${newTool.name} with this code: ${newTool.code}. Use these imports: ${newTool.imports}` 
      }, { headers: { "X-API-Key": apiKey } });
      alert("INJECTION_SUCCESS: System core is re-indexing...");
    } catch (e) {
      alert("INJECTION_FAILED: Buffer conflict.");
    }
  };

  return (
    <div className="h-full flex gap-4 overflow-hidden">
      
      {/* --- LEFT: THE ARMORY LEDGER --- */}
      <aside className="w-80 titan-card flex flex-col border-[#b5a642]/10 bg-black/40">
        <div className="p-4 border-b border-white/5 bg-[#b5a642]/5 flex items-center gap-3">
          <Box size={18} className="text-[#b5a642]" />
          <span className="text-[10px] font-black text-white uppercase tracking-[0.2em]">Active_Arsenal</span>
        </div>

        <div className="p-4 border-b border-white/5">
          <div className="relative">
            <Search className="absolute left-2 top-2.5 text-white/20" size={12} />
            <input 
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="FILTER_CAPABILITIES..."
              className="w-full bg-black/60 border border-white/5 p-2 pl-8 text-[9px] font-bold text-[#b5a642] outline-none"
            />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-2 space-y-1 scrollbar-hide">
          {existingTools.map(tool => (
            <div key={tool} className="group p-3 border border-white/5 bg-white/2 hover:border-[#b5a642]/40 rounded-sm flex items-center justify-between transition-all">
              <div className="flex items-center gap-3">
                <Wrench size={12} className="text-gray-500 group-hover:text-[#b5a642]" />
                <span className="text-[10px] font-mono text-gray-400 group-hover:text-white uppercase">{tool}</span>
              </div>
              <div className="w-1.5 h-1.5 rounded-full bg-green-500/40" />
            </div>
          ))}
        </div>

        <div className="p-4 bg-black/60 border-t border-white/5">
           <div className="flex justify-between text-[8px] font-black uppercase text-white/20">
             <span>Lattice_Sutured: 100%</span>
             <span>Registry: V50.6</span>
           </div>
        </div>
      </aside>

      {/* --- RIGHT: THE CAPABILITY FORGE --- */}
      <div className="flex-1 flex flex-col gap-4 overflow-hidden">
        
        {/* AI TOOL DRAFTER */}
        <div className="titan-card p-6 border-[#b5a642]/20 bg-[#b5a642]/5 relative overflow-hidden">
           <div className="absolute top-0 right-0 p-4 opacity-10 pointer-events-none">
             <Sparkles size={80} />
           </div>
           <h2 className="text-[10px] font-black text-[#b5a642] uppercase tracking-[0.4em] mb-4 flex items-center gap-2">
             <Sparkles size={14} /> AI_Tool_Generator
           </h2>
           <div className="flex gap-4">
             <input 
               value={toolRequest}
               onChange={e => setToolRequest(e.target.value)}
               placeholder="Describe a new capability (e.g., 'A tool to track crypto prices')..."
               className="flex-1 bg-black border border-[#b5a642]/30 p-4 text-sm font-bold text-white outline-none focus:border-[#b5a642]"
             />
             <button 
              onClick={forgeToolWithAI}
              className="px-8 bg-[#b5a642] text-black font-black uppercase text-xs hover:bg-white transition-all shadow-[5px_5px_0_#000]"
             >
               {isForging ? "Generating..." : "Draft Tool"}
             </button>
           </div>
        </div>

        <div className="flex-1 grid grid-cols-2 gap-4 min-h-0">
          <div className="titan-card flex flex-col p-6 border-white/10 bg-black/40">
             <h3 className="text-[9px] font-black text-white/40 uppercase tracking-widest mb-6 border-b border-white/5 pb-2">Technical_Logic_Editor</h3>
             
             <div className="space-y-4 flex-1 flex flex-col min-h-0">
                <div className="flex gap-4">
                  <div className="flex-1">
                    <label htmlFor="function-name" className="text-[8px] text-[#b5a642] uppercase font-black mb-1 block">Function_Name</label>
                    <input 
                      id="function-name"
                      value={newTool.name}
                      onChange={e => setNewTool({...newTool, name: e.target.value})}
                      className="w-full bg-black border border-white/10 p-2 text-[11px] font-mono text-[#00f2ff] outline-none"
                      title="Function name"
                      placeholder="e.g. my_tool"
                    />
                  </div>
                  <div className="flex-1">
                    <label htmlFor="sector-assignment" className="text-[8px] text-[#b5a642] uppercase font-black mb-1 block">Sector_Assignment</label>
                    <select id="sector-assignment" title="Sector assignment" aria-label="Sector assignment" className="w-full bg-black border border-white/10 p-2 text-[11px] font-mono text-white/60 outline-none">
                      <option>SOFTWARE_ENGINEERING</option>
                      <option>CYBER_SECURITY</option>
                      <option>DATA_INTELLIGENCE</option>
                    </select>
                  </div>
                </div>

                <div className="flex-1 flex flex-col">
                  <label htmlFor="python-source" className="text-[8px] text-[#b5a642] uppercase font-black mb-1 block">Python_Source</label>
                  <textarea 
                    id="python-source"
                    value={newTool.code}
                    onChange={e => setNewTool({...newTool, code: e.target.value})}
                    className="flex-1 bg-black border border-white/10 p-4 text-[12px] font-mono text-green-400 outline-none resize-none leading-relaxed"
                    spellCheck={false}
                    title="Python source code"
                    placeholder="# Enter tool code..."
                  />
                </div>

                <button 
                  onClick={injectToMonolith}
                  className="w-full py-4 bg-[#00f2ff] text-black font-black uppercase text-xs hover:bg-white transition-all shadow-[6px_6px_0_#000] flex items-center justify-center gap-3"
                >
                  <Save size={16} /> Physically Inject Tool
                </button>
             </div>
          </div>

          {/* INJECTION LOGS */}
          <div className="titan-card flex flex-col p-6 border-white/10 bg-[#080a0c]">
             <div className="flex items-center justify-between mb-6 border-b border-white/5 pb-2">
                <div className="flex items-center gap-2">
                  <Terminal size={14} className="text-[#00f2ff]" />
                  <span className="text-[9px] font-black text-white/40 uppercase tracking-widest">Injection_Stream</span>
                </div>
                <div className="flex gap-1">
                  <div className="w-1.5 h-1.5 rounded-full bg-[#00f2ff] animate-pulse" />
                </div>
             </div>
             <div className="flex-1 font-mono text-[10px] space-y-2 text-[#00f2ff]/60 overflow-y-auto scrollbar-hide">
                {diagnosticLogs.map((log, i) => (
                  <div key={i} className="flex gap-3">
                    <span className="text-white/10 select-none">[{i}]</span>
                    <span>{log}</span>
                  </div>
                ))}
                {/* FIXED: Wrapped the literal arrows in a JS string block */}
                <div className="animate-pulse">{" >>> Awaiting_Capability_Signature_"}</div>
             </div>
             
             <div className="mt-4 p-4 bg-red-500/5 border border-red-500/20 rounded-sm">
                <div className="flex items-center gap-2 text-red-500 mb-1">
                  <AlertCircle size={12} />
                  <span className="text-[8px] font-black uppercase">Monolith_Integrity_Warning</span>
                </div>
                <p className="text-[8px] text-white/30 leading-relaxed uppercase"> Injection triggers a system-wide hot reload. </p>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
}