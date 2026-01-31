/**
 * REALM FORGE: TITAN COMMAND DECK v30.0
 * ARCHITECT: LEAD SWARM ENGINEER
 * STATUS: PRODUCTION READY - INDUSTRIAL OVERHAUL
 * PATH: F:\RealmForge\client\app\page.tsx
 */

// @ts-nocheck
"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  LayoutDashboard, Code2, Share2, Crosshair, Settings, Radio, 
  Power, Mic, MicOff, ShieldCheck, Activity, Terminal, 
  Users, Zap, ChevronRight, Binary
} from "lucide-react";
import axios from "axios";

// --- CHAMBER COMPONENTS ---
import WarRoom from "@/components/chambers/WarRoom";
import ArtifactStudio from "@/components/chambers/ArtifactStudio";
import NeuralLattice from "@/components/chambers/NeuralLattice";
import ArsenalManager from "@/components/chambers/ArsenalManager";

// --- 13 CANONICAL SECTORS ---
const SECTORS = [
  "software_engineering", "cyber_security", "data_intelligence", 
  "devops_infrastructure", "financial_ops", "legal_compliance", 
  "research_development", "executive_board", "marketing_pr", 
  "human_capital", "quality_assurance", "facility_management", 
  "general_engineering"
];

export default function TitanForgeHUD() {
  // --- NAVIGATION & CONNECTION ---
  const [activeChamber, setActiveChamber] = useState("war_room");
  const [status, setStatus] = useState("OFFLINE");
  const [mounted, setMounted] = useState(false);
  const [config, setConfig] = useState({ 
    url: "http://localhost:8000", 
    key: "sk-realm-god-mode-888", 
    open: false 
  });

  // --- TITAN-INDUSTRIAL TELEMETRY ---
  const [vitals, setVitals] = useState({ cpu: 0, ram: 0, lattice_nodes: 13472, active_sector: "Architect" });
  const [activeDept, setActiveDept] = useState("Architect");
  const [activeAgent, setActiveAgent] = useState("ForgeMaster");
  const [meetingParticipants, setMeetingParticipants] = useState(["ForgeMaster"]);
  const [handoffHistory, setHandoffHistory] = useState([]);
  const [diagnosticLines, setDiagnosticLines] = useState([
    `[${new Date().toLocaleTimeString()}] RE-INIT: Mastermind Online.`,
    `[${new Date().toLocaleTimeString()}] LATTICE: 13,472 Nodes Synchronized.`
  ]);
  const [isProcessing, setIsProcessing] = useState(false);

  // --- SENSORY REFS ---
  const audioQueue = useRef([]);
  const isAudioPlaying = useRef(false);
  const audioCtx = useRef(null);
  const [audioUnlocked, setAudioUnlocked] = useState(false);
  const ws = useRef(null);
  const mediaRecorder = useRef(null);
  const audioChunks = useRef([]);
  const [isListening, setIsListening] = useState(false);

  const [globalLogs, setGlobalLogs] = useState([{
    id: 'init', type: 'system', agent: 'CORE', 
    content: "### [REALM_FORGE_v30.0] TITAN_HUD_NOMINAL.\nFleet aligned. Standing by for Industrial Directives.",
    timestamp: 'INIT'
  }]);

  // --- SENSORY HANDSHAKE ---
  const unlockAudio = async () => {
    try {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (!audioCtx.current) audioCtx.current = new AudioContextClass();
      if (audioCtx.current.state === 'suspended') await audioCtx.current.resume();
      setAudioUnlocked(true);
      setDiagnosticLines(p => [...p.slice(-49), `[SENSES] Neural vocal link synchronized.`]);
    } catch (err) { console.error("Sensory Fault:", err); }
  };

  const playNextAudio = async () => {
    if (audioQueue.current.length === 0 || !audioUnlocked || !audioCtx.current) {
      isAudioPlaying.current = false;
      return;
    }
    isAudioPlaying.current = true;
    const base64Str = audioQueue.current.shift();
    try {
        const bytes = Uint8Array.from(window.atob(base64Str), c => c.charCodeAt(0));
        const buffer = await audioCtx.current.decodeAudioData(bytes.buffer);
        const source = audioCtx.current.createBufferSource();
        source.buffer = buffer;
        source.connect(audioCtx.current.destination);
        source.onended = () => { isAudioPlaying.current = false; playNextAudio(); };
        source.start(0);
    } catch (e) { isAudioPlaying.current = false; playNextAudio(); }
  };

  // --- MISSION ENGINE ---
  const executeDirective = useCallback(async (text: string) => {
    if (!text || isProcessing) return;
    setIsProcessing(true);
    setGlobalLogs(p => [...p, { id: Date.now(), type: 'user', agent: 'ARCHITECT', content: text, timestamp: new Date().toLocaleTimeString() }]);

    const url = localStorage.getItem("RF_URL") || config.url;
    const key = localStorage.getItem("RF_KEY") || config.key;

    try {
      await axios.post(`${url.replace(/\/$/, "")}/api/v1/mission`, { task: text }, { 
        headers: { "X-API-Key": key, "ngrok-skip-browser-warning": "69420" } 
      });
    } catch (err) {
      setDiagnosticLines(p => [...p.slice(-49), `[FAULT] Mission Crash: Gateway Link Severed.`]);
      setIsProcessing(false);
    }
  }, [config.url, config.key, isProcessing]);

  // --- WEBSOCKET нервная система (NERVOUS SYSTEM) ---
  const connectToSwarm = useCallback((url) => {
    if (typeof window === 'undefined' || !url) return;
    if (ws.current) ws.current.close();

    const base = url.replace("https://", "").replace("http://", "").replace(/\/$/, "");
    const protocol = url.startsWith("https") ? "wss" : "ws";
    const socket = new WebSocket(`${protocol}://${base}/ws/telemetry`);
    ws.current = socket;

    socket.onopen = () => setStatus("NOMINAL");
    socket.onmessage = (e) => {
      const data = JSON.parse(e.data);
      
      if (data.vitals) setVitals(data.vitals);
      
      if (data.type === "node_update") {
        setActiveDept(data.dept);
        setActiveAgent(data.agent);
        if (data.handoffs) setHandoffHistory(data.handoffs);
        if (data.meeting_participants) setMeetingParticipants(data.meeting_participants);
      }

      if (data.type === "diagnostic") {
        setDiagnosticLines(p => [...p.slice(-49), data.text]);
      }

      if (data.type === "audio_chunk") {
        setGlobalLogs(p => [...p, { id: Date.now(), type: 'ai', agent: data.agent, content: data.text, timestamp: new Date().toLocaleTimeString() }]);
        if (data.audio_base64 && audioUnlocked) {
          audioQueue.current.push(data.audio_base64);
          if (!isAudioPlaying.current) playNextAudio();
        }
      }

      if (data.type === "mission_complete") setIsProcessing(false);
    };
    socket.onclose = () => setStatus("OFFLINE");
  }, [audioUnlocked]);

  useEffect(() => {
    setMounted(true);
    const savedUrl = localStorage.getItem("RF_URL") || config.url;
    const savedKey = localStorage.getItem("RF_KEY") || config.key;
    setConfig(c => ({ ...c, url: savedUrl, key: savedKey }));
    connectToSwarm(savedUrl);
  }, [connectToSwarm]);

  if (!mounted) return null;

  return (
    <div className="flex h-screen bg-[#05070a] text-slate-300 font-mono overflow-hidden">
      
      {/* 1. SECTOR SIDEBAR */}
      <aside className="w-80 border-r border-[#b5a642]/20 bg-[#080a0c] flex flex-col shrink-0 z-50">
        <div className="p-6 border-b border-white/5 bg-black/20">
          <div className="flex items-center gap-3 mb-8">
            <div className={`w-3 h-3 rounded-sm ${status === "NOMINAL" ? "bg-[#b5a642] shadow-[0_0_15px_#b5a642] animate-pulse" : "bg-red-500"}`} />
            <h1 className="text-xl font-black text-white italic tracking-tighter uppercase leading-none">Realm_Forge <span className="text-[10px] not-italic font-normal text-white/30 block">Industrial OS v30.0</span></h1>
          </div>
          
          <button 
            onMouseDown={() => { if(!audioCtx.current) unlockAudio(); setIsListening(true); }} 
            onMouseUp={() => setIsListening(false)}
            className={`w-full py-4 border transition-all flex items-center justify-center gap-3 ${isListening ? "bg-[#ff3e3e]/10 border-[#ff3e3e] text-[#ff3e3e]" : "bg-[#b5a642]/5 border-[#b5a642]/30 text-[#b5a642] hover:bg-[#b5a642]/10"}`}
          >
            {isListening ? <Radio size={18} className="animate-spin" /> : <Mic size={18}/>}
            <span className="text-[10px] font-black uppercase tracking-[0.2em]">{isListening ? "Transmitting..." : "Voice Command"}</span>
          </button>
        </div>

        <nav className="flex-1 py-2 overflow-y-auto scrollbar-hide">
          <div className="px-6 py-2 text-[9px] uppercase font-black text-white/20 tracking-[0.2em]">Operational_Chambers</div>
          {[
            { id: "war_room", label: "War Room", icon: <LayoutDashboard size={18}/> },
            { id: "artifact_studio", label: "Artifact Studio", icon: <Code2 size={18}/> },
            { id: "neural_lattice", label: "Neural Lattice", icon: <Share2 size={18}/> },
            { id: "arsenal", label: "Master Arsenal", icon: <Crosshair size={18}/> }
          ].map(ch => (
            <button key={ch.id} onClick={() => setActiveChamber(ch.id)} className={`w-full flex items-center gap-4 px-8 py-4 text-[11px] font-black uppercase tracking-widest transition-all ${activeChamber === ch.id ? "text-[#b5a642] bg-[#b5a642]/10 border-r-4 border-[#b5a642]" : "text-gray-500 hover:text-white hover:bg-white/5"}`}>
              {ch.icon} {ch.label}
            </button>
          ))}

          <div className="mt-8 px-6 py-2 text-[9px] uppercase font-black text-white/20 tracking-[0.2em]">Sector_Activity</div>
          <div className="px-6 grid grid-cols-4 gap-1 opacity-40">
            {SECTORS.map(s => (
              <div key={s} className={`aspect-square border border-white/10 flex items-center justify-center ${vitals.active_sector === s ? "bg-[#b5a642] animate-pulse" : "bg-white/5"}`}>
                <Activity size={10} />
              </div>
            ))}
          </div>
        </nav>

        <div className="p-6 border-t border-white/5 bg-black/40">
          <button onClick={() => setConfig({...config, open: true})} className="w-full py-2 border border-white/10 text-[9px] font-black uppercase text-white/40 hover:text-white flex items-center justify-center gap-2 transition-all">
            <Settings size={12}/> Calibrate Neural Link
          </button>
        </div>
      </aside>

      {/* 2. MAIN HUD AREA */}
      <main className="flex-1 flex flex-col relative bg-[#05070a] border-r border-white/5">
        
        {/* HEADER: ROUND TABLE & VITALS */}
        <header className="h-20 bg-[#080a0c]/80 backdrop-blur-xl border-b border-[#b5a642]/10 flex items-center px-10 justify-between z-40">
          <div className="flex gap-10 items-center">
            <div className="flex -space-x-3">
              {meetingParticipants.map((p, i) => (
                <div key={i} className="w-10 h-10 rounded-full bg-black border-2 border-[#b5a642] flex items-center justify-center text-[10px] font-black text-[#b5a642] shadow-[0_0_15px_rgba(181,166,66,0.2)]">
                  {p.slice(0, 2).toUpperCase()}
                </div>
              ))}
              <div className="w-10 h-10 rounded-full bg-[#b5a642]/10 border-2 border-[#b5a642]/30 flex items-center justify-center text-[12px] text-[#b5a642] hover:bg-[#b5a642] hover:text-black cursor-pointer transition-all">+</div>
            </div>
            <div className="h-8 w-px bg-white/10" />
            <div className="font-mono">
              <span className="text-white/20 text-[9px] block uppercase tracking-widest">Active_Commander</span>
              <span className="text-white font-black text-sm uppercase tracking-tighter italic">{activeAgent}</span>
            </div>
          </div>

          <div className="flex gap-8 text-[10px] font-black uppercase tracking-widest">
            <div className="text-right">
              <span className="text-white/20 block">Lattice_Nodes</span>
              <span className="text-[#00f2ff]">{vitals.lattice_nodes.toLocaleString()}</span>
            </div>
            <div className="text-right">
              <span className="text-white/20 block">System_Load</span>
              <span className="text-[#ff3e3e]">{vitals.cpu}% CPU</span>
            </div>
            <button type="button" onClick={() => window.location.reload()} title="Reload" aria-label="Reload page" className="w-10 h-10 rounded bg-white/5 flex items-center justify-center hover:bg-[#ff3e3e]/20 text-white/40 hover:text-[#ff3e3e] transition-all border border-white/5">
              <Power size={18}/>
            </button>
          </div>
        </header>

        {/* CHAMBER VIEWPORT */}
        <div className="flex-1 relative overflow-hidden">
          <AnimatePresence mode="wait">
            {activeChamber === "war_room" && (
              <motion.div key="war" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="h-full">
                <WarRoom 
                  logs={globalLogs} 
                  activeDept={activeDept} 
                  activeAgent={activeAgent} 
                  isProcessing={isProcessing} 
                  onSend={executeDirective} 
                  unlockAudio={unlockAudio}
                  audioUnlocked={audioUnlocked}
                />
              </motion.div>
            )}
            {activeChamber === "artifact_studio" && <ArtifactStudio />}
            {activeChamber === "neural_lattice" && <NeuralLattice />}
            {activeChamber === "arsenal" && <ArsenalManager />}
          </AnimatePresence>
        </div>

        {/* 3. DIAGNOSTIC FROSTED HUD (THE SHOW-STOPPER) */}
        <div className="absolute bottom-6 right-6 w-96 glass-panel rounded-lg overflow-hidden border border-[#b5a642]/20 shadow-2xl z-50">
          <div className="p-3 bg-[#b5a642]/10 border-b border-[#b5a642]/20 flex items-center justify-between">
            <div className="flex items-center gap-2 text-[9px] font-black uppercase text-[#b5a642] tracking-widest">
              <Terminal size={12} /> System_Diagnostics
            </div>
            <div className="flex gap-1">
              <div className="w-2 h-2 rounded-full bg-[#ff3e3e]/40" />
              <div className="w-2 h-2 rounded-full bg-[#b5a642]/40" />
            </div>
          </div>
          <div className="p-4 h-48 overflow-y-auto font-mono text-[10px] space-y-1 bg-black/40 text-[#b5a642]/80">
             {diagnosticLines.map((line, i) => (
               <div key={i} className="flex gap-2">
                 <span className="text-white/20 select-none">[{i.toString().padStart(2, '0')}]</span>
                 <span>{line}</span>
               </div>
             ))}
             {/* FIXED: Wrapped the literal arrows in strings to satisfy Turbopack build */}
             {isProcessing && <div className="animate-pulse text-[#00f2ff]">{" >>> Processing_Industrial_Directive..."}</div>}
          </div>
        </div>
      </main>

      {/* CALIBRATION OVERLAY */}
      <AnimatePresence>
        {config.open && (
          <div className="fixed inset-0 bg-[#05070a]/95 flex items-center justify-center z-[9999] backdrop-blur-xl">
            <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="bg-[#0c0e12] border-2 border-[#b5a642]/50 p-10 w-full max-w-lg shadow-[0_0_100px_rgba(181,166,66,0.1)]">
               <h2 className="text-3xl font-black text-white mb-8 uppercase italic border-b-4 border-[#b5a642] inline-block tracking-tighter">Calibration</h2>
               <div className="space-y-6 font-mono">
                  <div className="space-y-1">
                    <label htmlFor="config-url" className="text-[9px] uppercase font-black text-white/40 tracking-widest">Node_Endpoint_URL</label>
                    <input id="config-url" value={config.url} onChange={e => setConfig({...config, url: e.target.value})} className="w-full bg-black border border-white/10 p-4 text-sm font-bold text-[#b5a642] outline-none focus:border-[#b5a642]" placeholder="https://..." />
                  </div>
                  <div className="space-y-1">
                    <label htmlFor="config-key" className="text-[9px] uppercase font-black text-white/40 tracking-widest">God_Mode_Signature</label>
                    <input id="config-key" type="password" value={config.key} onChange={e => setConfig({...config, key: e.target.value})} className="w-full bg-black border border-white/10 p-4 text-sm font-bold text-[#b5a642] outline-none focus:border-[#b5a642]" placeholder="Signing key" />
                  </div>
                  <button onClick={() => { localStorage.setItem("RF_URL", config.url); localStorage.setItem("RF_KEY", config.key); setConfig({...config, open: false}); window.location.reload(); }} className="w-full py-4 bg-[#b5a642] text-black font-black uppercase text-sm hover:bg-white transition-all mt-4">Suture Swarm Link</button>
               </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}