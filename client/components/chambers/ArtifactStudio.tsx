/**
 * REALM FORGE: TITAN ARTIFACT VAULT v31.0
 * STYLE: CAFFEINE-NEON / HIGH-VISIBILITY
 * ARCHITECT: LEAD SWARM ENGINEER
 * PATH: F:\RealmForge_PROD\client\components\chambers\ArtifactStudio.tsx
 */

// @ts-nocheck
"use client";

import { useState, useEffect, useCallback } from "react";
import axios from "axios";
import { 
  FileCode, Save, Eye, RefreshCw, HardDrive, 
  Package, FileJson, FileText, Globe, Zap, 
  Terminal, ShieldCheck, Download, Search, 
  ChevronRight, Box, FileEdit
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function ArtifactStudio() {
  const [files, setFiles] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [currentFile, setCurrentFile] = useState({ path: "", content: "", type: "code" });
  const [isPreviewOpen, setIsPreviewOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [config, setConfig] = useState({ url: "", key: "" });

  // --- 1. SOVEREIGN HYDRATION GUARD ---
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const url = localStorage.getItem("RF_URL") || "http://localhost:8000";
      const key = localStorage.getItem("RF_KEY") || "sk-realm-god-mode-888";
      setConfig({ url, key });
      if (url) scanLattice(url, key);
    }
  }, []);

  const scanLattice = async (url: string, key: string) => {
    if (!url) return;
    setLoading(true);
    try {
      const cleanUrl = url.replace(/\/$/, "");
      // Re-fetch agents/files manifest
      await axios.get(`${cleanUrl}/api/v1/agents`, { 
        headers: { 'ngrok-skip-browser-warning': '69420', "X-API-Key": key } 
      });
      
      // Industrial set for primary development
      setFiles([
          "server.py",
          "realm_core.py",
          "src/system/actions.py",
          "data/workforce_audit.csv",
          "data/roster.json",
          "data/memory/neural_graph.json",
          "CLIENT_ONBOARDING.md"
      ]);
    } catch (e) {
      console.error("LATTICE_INDEX_FAULT");
    } finally {
      setLoading(false);
    }
  };

  const loadArtifact = async (path: string) => {
    if (!config.url || !path) return;
    setLoading(true);
    try {
      const cleanUrl = config.url.replace(/\/$/, "");
      const res = await axios.post(`${cleanUrl}/api/v1/io/read`, 
        { path }, 
        { headers: { 'ngrok-skip-browser-warning': '69420', "X-API-Key": config.key } }
      );
      
      if (res.data && res.data.content !== undefined) {
        setCurrentFile({
          path,
          content: res.data.content,
          type: path.endsWith(".html") ? "web" : path.endsWith(".json") ? "json" : "code"
        });
      }
    } catch (e) {
      console.error("ARTIFACT_READ_ERROR");
    } finally {
      setLoading(false);
    }
  };

  const commitToDisk = async () => {
    if (!currentFile.path || !config.url) return;
    setLoading(true);
    try {
      const cleanUrl = config.url.replace(/\/$/, "");
      await axios.post(`${cleanUrl}/api/v1/io/write`, 
        { path: currentFile.path, content: currentFile.content }, 
        { headers: { 'ngrok-skip-browser-warning': '69420', "X-API-Key": config.key } }
      );
    } catch (e) {
      alert("PHYSICAL_COMMIT_FAULT");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-full flex gap-6 bg-transparent overflow-hidden relative">
      
      {/* --- COLUMN A: THE VAULT INDEX --- */}
      <aside className="w-80 bg-[#0a0a0a] border border-white/5 rounded-2xl flex flex-col shrink-0 overflow-hidden shadow-2xl">
        <div className="p-5 border-b border-white/5 bg-[#00f2ff]/5 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <HardDrive size={18} className="text-[#00f2ff]" />
            <span className="text-[11px] font-black text-white uppercase tracking-[0.2em]">Disk_Vault</span>
          </div>
          <button 
            onClick={() => scanLattice(config.url, config.key)}
            className="p-2 hover:bg-white/5 rounded-lg transition-all"
          >
            <RefreshCw size={14} className="text-[#00f2ff]/60" />
          </button>
        </div>

        <div className="p-4">
          <div className="relative group">
            <Search className="absolute left-3 top-2.5 text-white/20 group-focus-within:text-[#00f2ff] transition-colors" size={14} />
            <input 
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="FILTER_VAULT..."
              className="w-full bg-black border border-white/10 p-2.5 pl-10 text-[10px] font-bold text-[#00f2ff] outline-none focus:border-[#00f2ff]/40 rounded-xl transition-all"
            />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto px-2 pb-4 space-y-1 scrollbar-hide">
          {files.filter(f => f.toLowerCase().includes(searchQuery.toLowerCase())).map(file => (
            <button 
              key={file} 
              onClick={() => loadArtifact(file)} 
              className={`w-full text-left px-4 py-3 text-[10px] flex items-center justify-between rounded-xl transition-all group
              ${currentFile.path === file ? "bg-[#00f2ff]/10 border border-[#00f2ff]/30 text-white shadow-[0_0_15px_rgba(0,242,255,0.05)]" : "text-gray-500 hover:bg-white/5 hover:text-white"}`}
            >
              <div className="flex items-center gap-3 truncate">
                {file.endsWith(".py") ? <Terminal size={14} className="text-[#ff80bf]" /> :
                 file.endsWith(".json") ? <Box size={14} className="text-[#00f2ff]" /> :
                 file.endsWith(".csv") ? <Activity size={14} className="text-green-400" /> :
                 <FileText size={14} />}
                <span className="truncate tracking-wide">{file.split('/').pop()}</span>
              </div>
              <ChevronRight size={10} className={`opacity-0 group-hover:opacity-100 ${currentFile.path === file ? 'text-[#00f2ff]' : ''}`} />
            </button>
          ))}
        </div>

        <div className="p-4 border-t border-white/5 bg-black/40">
           <button className="w-full py-3.5 bg-[#ff80bf]/10 border border-[#ff80bf]/30 text-[#ff80bf] text-[10px] font-black uppercase tracking-[0.2em] rounded-xl flex items-center justify-center gap-3 hover:bg-[#ff80bf] hover:text-black transition-all shadow-[0_0_20px_rgba(255,128,191,0.1)]">
             <Package size={16} /> Package Shuttle
           </button>
        </div>
      </aside>

      {/* --- COLUMN B: THE PRODUCTION EDITOR --- */}
      <div className="flex-1 flex flex-col bg-[#0a0a0a] border border-white/5 rounded-2xl overflow-hidden shadow-2xl relative">
        <header className="h-16 bg-black/40 border-b border-white/5 flex items-center px-8 justify-between">
          <div className="flex items-center gap-4">
             <div className="w-10 h-10 rounded-xl bg-[#ff80bf]/10 flex items-center justify-center border border-[#ff80bf]/20">
                <FileEdit size={20} className="text-[#ff80bf]" />
             </div>
             <div>
                <span className="text-[9px] font-black text-white/20 uppercase block tracking-widest leading-none mb-1">Active_Buffer</span>
                <span className="text-[12px] font-black text-[#00f2ff] italic tracking-tight">{currentFile.path || "IDLE_STANDBY"}</span>
             </div>
          </div>
          
          <div className="flex items-center gap-3">
            <button 
                onClick={() => setIsPreviewOpen(!isPreviewOpen)} 
                className={`flex items-center gap-2 px-5 py-2.5 rounded-xl border transition-all text-[11px] font-black uppercase tracking-widest
                ${isPreviewOpen ? "bg-[#ff80bf]/10 border-[#ff80bf] text-[#ff80bf]" : "bg-white/5 border-white/10 text-white/40 hover:border-white/30 hover:text-white"}`}
            >
              <Eye size={16} /> {isPreviewOpen ? "Close_Preview" : "Launch_Preview"}
            </button>
            <button 
                onClick={commitToDisk}
                className="flex items-center gap-2 px-8 py-2.5 bg-[#00f2ff] text-black text-[11px] font-black uppercase rounded-xl hover:bg-white transition-all shadow-[0_0_20px_rgba(0,242,255,0.25)] active:scale-95"
            >
              <Save size={16} /> Commit
            </button>
          </div>
        </header>

        <div className="flex-1 flex overflow-hidden">
          {/* EDITOR AREA */}
          <div className="flex-1 relative bg-black/30 group">
            <div className="absolute left-0 top-0 bottom-0 w-12 bg-black/40 border-r border-white/5 flex flex-col items-center pt-8 text-[9px] font-mono text-white/10 select-none">
              {Array.from({length: 35}).map((_, i) => <div key={i} className="h-[24px]">{i+1}</div>)}
            </div>
            <textarea 
              value={currentFile.content}
              onChange={(e) => setCurrentFile({...currentFile, content: e.target.value})}
              className="w-full h-full bg-transparent p-8 pl-16 text-[14px] font-mono text-slate-300 outline-none resize-none leading-[24px] border-none scrollbar-hide selection:bg-[#ff80bf] selection:text-black"
              placeholder=">>> Awaiting_Industrial_Injection..."
              spellCheck={false}
            />
          </div>

          {/* DUAL VIEW RENDERER (CYAN/PINK STYLE) */}
          <AnimatePresence>
            {isPreviewOpen && (
              <motion.div 
                initial={{ width: 0, opacity: 0 }}
                animate={{ width: "45%", opacity: 1 }}
                exit={{ width: 0, opacity: 0 }}
                transition={{ type: "spring", bounce: 0, duration: 0.4 }}
                className="border-l border-white/5 bg-[#050505] relative shadow-[-20px_0_40px_rgba(0,0,0,0.5)] z-10"
              >
                <div className="absolute top-4 left-6 z-50">
                   <div className="px-3 py-1 bg-[#00f2ff]/10 text-[#00f2ff] text-[9px] font-black uppercase rounded-md border border-[#00f2ff]/20">
                     {currentFile.type === "web" ? "Sandbox_Runtime" : "Logic_Observer"}
                   </div>
                </div>
                
                <div className="h-full w-full pt-12">
                {currentFile.type === "web" ? (
                  <iframe 
                    srcDoc={currentFile.content} 
                    className="w-full h-full border-none bg-white rounded-tl-2xl" 
                    title="Industrial Preview"
                  />
                ) : (
                  <div className="p-8 h-full overflow-auto text-slate-400 font-mono text-[12px] leading-relaxed scrollbar-hide">
                    <div className="mb-6 flex items-center gap-3">
                       <Box size={16} className="text-[#ff80bf]" />
                       <span className="text-[10px] font-black uppercase text-white/20 tracking-widest italic underline underline-offset-4 decoration-[#ff80bf]/40">Inspector_Raw_Feed</span>
                    </div>
                    <pre className="whitespace-pre-wrap">{currentFile.content}</pre>
                  </div>
                )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* LOADING SHIELD */}
        <AnimatePresence>
          {loading && (
            <motion.div 
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="absolute inset-0 bg-black/80 backdrop-blur-md flex flex-col items-center justify-center z-[200]"
            >
              <div className="relative">
                <RefreshCw className="animate-spin text-[#00f2ff]" size={56} />
                <Zap className="absolute inset-0 m-auto text-[#ff80bf] animate-pulse" size={24} />
              </div>
              <span className="mt-6 text-[11px] font-black text-white uppercase tracking-[0.6em] animate-pulse">Sovereign_Sync_In_Progress</span>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}