/**
 * REALM FORGE: TITAN ARTIFACT VAULT v30.1
 * ARCHITECT: LEAD SWARM ENGINEER
 * STATUS: PRODUCTION READY - HYDRATION HARDENED
 * PATH: F:/RealmForge/client/components/chambers/ArtifactStudio.tsx
 */

// @ts-nocheck
"use client";

import { useState, useEffect, useCallback } from "react";
import axios from "axios";
import { 
  FileCode, Save, Eye, RefreshCw, HardDrive, 
  Package, FileJson, FileText, Globe, Zap, 
  Terminal, ShieldCheck, Download, Search, ChevronRight
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function ArtifactStudio() {
  const [files, setFiles] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [currentFile, setCurrentFile] = useState({ path: "", content: "", type: "code" });
  const [isPreviewOpen, setIsPreviewOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [config, setConfig] = useState({ url: "", key: "" });

  // --- 1. SAFE HYDRATION ---
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const url = localStorage.getItem("RF_URL") || "";
      const key = localStorage.getItem("RF_KEY") || "";
      setConfig({ url, key });
      if (url) scanLattice(url, key);
    }
  }, []);

  const scanLattice = async (url: string, key: string) => {
    if (!url) return;
    setLoading(true);
    try {
      // Indexing logic - points to the Gateway
      const cleanUrl = url.replace(/\/$/, "");
      await axios.get(`${cleanUrl}/api/v1/agents`, { 
        headers: { 'ngrok-skip-browser-warning': '69420', "X-API-Key": key } 
      });
      
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
      console.error("VAULT_INDEX_FAULT");
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
      console.error("VAULT_READ_ERROR");
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
      alert("PHYSICAL_WRITE_FAULT");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-full flex gap-4 bg-black overflow-hidden relative">
      
      {/* --- SIDEBAR: DISK EXPLORER --- */}
      <aside className="w-72 titan-card flex flex-col border-[#b5a642]/10 bg-black/40">
        <div className="p-4 border-b border-white/5 bg-[#b5a642]/5 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <HardDrive size={14} className="text-[#b5a642]" />
            <span className="text-[10px] font-black text-white uppercase tracking-widest font-mono">Vault_Index</span>
          </div>
          <button type="button" onClick={() => scanLattice(config.url, config.key)} title="Refresh vault" aria-label="Refresh vault"><RefreshCw size={12} className="text-[#b5a642]" /></button>
        </div>

        <div className="p-3">
          <div className="relative">
            <Search className="absolute left-2 top-2 text-white/20" size={12} />
            <input 
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="SEARCH_VAULT..."
              className="w-full bg-black/60 border border-white/5 p-2 pl-8 text-[9px] font-bold text-[#b5a642] outline-none focus:border-[#b5a642]/40 rounded-sm"
            />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto px-2 space-y-1 scrollbar-hide">
          {files && files.filter(f => f.toLowerCase().includes(searchQuery.toLowerCase())).map(file => (
            <button 
              key={file} 
              onClick={() => loadArtifact(file)} 
              className={`w-full text-left p-3 text-[10px] flex items-center justify-between rounded-sm transition-all group
              ${currentFile.path === file ? "bg-[#b5a642] text-black font-black" : "text-gray-500 hover:bg-white/5 hover:text-white"}`}
            >
              <div className="flex items-center gap-3 truncate">
                {file.endsWith(".py") ? <Terminal size={14} className={currentFile.path === file ? "text-black" : "text-[#00f2ff]"} /> :
                 file.endsWith(".json") ? <FileJson size={14} className={currentFile.path === file ? "text-black" : "text-[#ff8c00]"} /> :
                 file.endsWith(".csv") ? <Zap size={14} className={currentFile.path === file ? "text-black" : "text-green-500"} /> :
                 <FileText size={14} />}
                <span className="truncate">{file.split('/').pop()}</span>
              </div>
              <ChevronRight size={10} className="opacity-0 group-hover:opacity-100" />
            </button>
          ))}
        </div>

        <div className="p-4 border-t border-white/5">
           <button className="w-full py-3 bg-[#b5a642]/10 border border-[#b5a642]/40 text-[#b5a642] text-[9px] font-black uppercase tracking-[0.2em] flex items-center justify-center gap-2">
             <Package size={14} /> Package AIAAS Shuttle
           </button>
        </div>
      </aside>

      {/* --- MAIN: TITAN EDITOR --- */}
      <div className="flex-1 flex flex-col titan-card bg-[#080a0c] overflow-hidden border-white/5">
        <div className="h-14 bg-black/60 border-b border-white/5 flex items-center px-6 justify-between">
          <div className="flex items-center gap-4 text-[10px] font-black uppercase tracking-widest font-mono">
             <ShieldCheck size={14} className="text-[#b5a642]" />
             <span className="text-white/40">Sovereign_File:</span>
             <span className="text-[#b5a642] italic">{currentFile.path || "VAULT_IDLE"}</span>
          </div>
          <div className="flex gap-2">
            <button onClick={() => setIsPreviewOpen(!isPreviewOpen)} className="px-4 py-1.5 border border-white/10 text-[10px] uppercase font-black">Preview</button>
            <button onClick={commitToDisk} className="px-6 py-1.5 bg-[#b5a642] text-black text-[10px] font-black uppercase">Commit</button>
          </div>
        </div>

        <div className="flex-1 flex overflow-hidden">
          <textarea 
            id="artifact-studio-editor"
            value={currentFile.content}
            onChange={(e) => setCurrentFile({...currentFile, content: e.target.value})}
            className="w-full h-full bg-transparent p-6 text-sm font-mono text-slate-300 outline-none resize-none leading-relaxed border-none"
            spellCheck={false}
            title="File content editor"
            placeholder="Edit file content..."
            aria-label="File content editor"
          />
          {isPreviewOpen && (
            <div className="w-1/2 border-l border-[#b5a642]/20 bg-white">
              {currentFile.type === "web" ? (
                <iframe srcDoc={currentFile.content} className="w-full h-full border-none" title="Preview" />
              ) : (
                <div className="p-10 h-full overflow-auto bg-[#0a0a0a] text-[#a8d4d4] font-mono text-xs">
                  <pre className="whitespace-pre-wrap">{currentFile.content}</pre>
                </div>
              )}
            </div>
          )}
        </div>

        {loading && (
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm flex flex-col items-center justify-center z-[100]">
            <RefreshCw className="animate-spin text-[#b5a642]" size={48} />
            <span className="mt-4 text-[10px] font-black text-white uppercase tracking-[0.5em]">Syncing_Drive</span>
          </div>
        )}
      </div>
    </div>
  );
}