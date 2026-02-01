/**
 * REALM FORGE: TITAN COMMAND CHASSIS v31.0
 * STYLE: CAFFEINE-NEON / HIGH-VISIBILITY
 * ARCHITECT: LEAD SWARM ENGINEER
 * PATH: F:\RealmForge_PROD\client\app\page.tsx
 */
"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  LayoutGrid, Code2, Share2, Wrench, Settings, 
  Power, Mic, MicOff, ShieldCheck, Activity, 
  Terminal, User, Zap, Github, ChevronLeft, 
  ChevronRight, MessageSquare, Send, Binary
} from "lucide-react";
import axios from "axios";

// --- CHAMBER COMPONENTS ---
import WarRoom from "@/components/chambers/WarRoom";
import ArtifactStudio from "@/components/chambers/ArtifactStudio";
import NeuralLattice from "@/components/chambers/NeuralLattice";
import ArsenalManager from "@/components/chambers/ArsenalManager";

export default function TitanForgeHUD() {
  // --- 1. SYSTEM NAVIGATION & LAYOUT ---
  const [activeTab, setActiveTab] = useState("war_room");
  const [isAssistantOpen, setIsAssistantOpen] = useState(true);
  const [status, setStatus] = useState("OFFLINE");
  const [mounted, setMounted] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  
  // --- 2. CONFIGURATION ---
  const [config, setConfig] = useState({ 
    url: "http://localhost:8000", 
    key: "sk-realm-god-mode-888", 
    open: false 
  });

  // --- 3. TELEMETRY & CHAT STATE ---
  const [vitals, setVitals] = useState({ cpu: 0, ram: 0, nodes: 13472, sector: "Architect" });
  const [activeAgent, setActiveAgent] = useState("ForgeMaster");
  const [chatInput, setChatInput] = useState("");
  const [assistantLogs, setAssistantLogs] = useState([
    { id: 1, role: 'assistant', text: "Ready for deployment, Architect. I have access to the full 180-tool arsenal. How shall we begin?" }
  ]);
  
  const [globalLogs, setGlobalLogs] = useState([{
    id: 'init', type: 'system', agent: 'CORE', 
    content: "### [TITAN_OS_v31.0] UPLINK_STABLE.\nFleet aligned to high-visibility neon parameters.",
    timestamp: 'INIT'
  }]);

  // --- 4. SENSORY & COMMUNICATIONS ---
  const audioQueue = useRef([]);
  const isAudioPlaying = useRef(false);
  const audioCtx = useRef(null);
  const [audioUnlocked, setAudioUnlocked] = useState(false);
  const ws = useRef(null);
  const [isListening, setIsListening] = useState(false);

  // --- SENSORY ACTIVATION ---
  const unlockAudio = async () => {
    if (typeof window === 'undefined') return;
    try {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (!audioCtx.current) audioCtx.current = new AudioContextClass();
      if (audioCtx.current.state === 'suspended') await audioCtx.current.resume();
      setAudioUnlocked(true);
    } catch (err) { console.error("Audio Fault", err); }
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
    
    // 1. PHYSICAL UI UPDATE (Move this to the top)
    setGlobalLogs(p => [...p, { 
      id: Date.now(), 
      type: 'user', 
      agent: 'ARCHITECT', 
      content: text, 
      timestamp: new Date().toLocaleTimeString() 
    }]);

    setIsProcessing(true);

    const url = typeof window !== 'undefined' ? (localStorage.getItem("RF_URL") || config.url) : config.url;
    const key = typeof window !== 'undefined' ? (localStorage.getItem("RF_KEY") || config.key) : config.key;

    try {
      await axios.post(`${url.replace(/\/$/, "")}/api/v1/mission`, 
        { task: text }, 
        { headers: { 
            "X-API-Key": key, 
            "ngrok-skip-browser-warning": "69420",
            "Content-Type": "application/json"
          } 
        }
      );
    } catch (err) {
      console.error("MISSION_UPLINK_FAIL:", err);
      setGlobalLogs(p => [...p, { id: 'err', type: 'system', agent: 'FAULT', content: "❌ **UPLINK_ERROR**: Check Ngrok Tunnel and Server Logs." }]);
      setIsProcessing(false);
    }
  }, [config.url, config.key, isProcessing]);

  // --- COMMUNICATIONS (WEBSOCKET) ---
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
      if (data.vitals) setVitals(p => ({ ...p, ...data.vitals }));
      if (data.type === "node_update") {
        setActiveAgent(data.agent);
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
    if (typeof window !== 'undefined') {
      const savedUrl = localStorage.getItem("RF_URL") || config.url;
      const savedKey = localStorage.getItem("RF_KEY") || config.key;
      setConfig(c => ({ ...c, url: savedUrl, key: savedKey }));
      connectToSwarm(savedUrl);
    }
  }, [connectToSwarm]);

  if (!mounted) return null;

  return (
    <div className="flex h-screen w-screen bg-[#050505] text-slate-200 overflow-hidden font-sans">
      
      {/* COLUMN 1: MINIMAL NAV RAIL (CYAN ACCENTS) */}
      <aside className="w-[72px] bg-[#0a0a0a] border-r border-white/5 flex flex-col items-center py-8 gap-10 shrink-0 z-[100]">
        <motion.div whileHover={{ scale: 1.1 }} className="w-10 h-10 bg-[#00f2ff] rounded-xl flex items-center justify-center text-black shadow-[0_0_20px_rgba(0,242,255,0.3)]">
          <Binary size={24} />
        </motion.div>
        
        <nav className="flex flex-col gap-6">
          <NavIcon active={activeTab === "war_room"} onClick={() => setActiveTab("war_room")} icon={<LayoutGrid size={22}/>} label="WAR ROOM" />
          <NavIcon active={activeTab === "artifact_studio"} onClick={() => setActiveTab("artifact_studio")} icon={<Code2 size={22}/>} label="STUDIO" />
          <NavIcon active={activeTab === "neural_lattice"} onClick={() => setActiveTab("neural_lattice")} icon={<Share2 size={22}/>} label="LATTICE" />
          <NavIcon active={activeTab === "arsenal"} onClick={() => setActiveTab("arsenal")} icon={<Wrench size={22}/>} label="ARSENAL" />
        </nav>

        <div className="mt-auto flex flex-col gap-6 pb-4">
           <NavIcon active={false} onClick={() => setConfig({...config, open: true})} icon={<Settings size={22}/>} label="CONFIG" />
           <button onClick={() => window.location.reload()} className="w-10 h-10 flex items-center justify-center rounded-xl text-white/20 hover:text-red-500 hover:bg-red-500/10 transition-all">
             <Power size={20} />
           </button>
        </div>
      </aside>

      {/* COLUMN 2: THE PRIMARY WORKSPACE (CENTER CANVAS) */}
      <main className="flex-1 flex flex-col min-w-0 bg-[#080808] relative">
        <header className="h-14 border-b border-white/5 flex items-center px-8 justify-between bg-[#0a0a0a]/50 backdrop-blur-md">
           <div className="flex items-center gap-6">
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${status === "NOMINAL" ? "bg-[#00f2ff] shadow-[0_0_10px_#00f2ff]" : "bg-red-500"}`} />
                <span className="text-[10px] font-black tracking-[0.2em] uppercase text-white/50">Lattice_{status}</span>
              </div>
              <div className="h-4 w-px bg-white/10" />
              <div className="text-[10px] font-black tracking-[0.2em] uppercase text-[#ff80bf]">Active: {activeAgent}</div>
           </div>
           
           <div className="flex items-center gap-6 text-[10px] font-bold text-white/30 uppercase tracking-widest">
             <div className="flex items-center gap-2"><Activity size={12}/> Load: <span className="text-white">{vitals.cpu}%</span></div>
             <div className="flex items-center gap-2"><Binary size={12}/> Nodes: <span className="text-white">{vitals.nodes}</span></div>
             <button onClick={() => setIsAssistantOpen(!isAssistantOpen)} className={`p-2 rounded-lg transition-all ${isAssistantOpen ? "bg-[#00f2ff]/10 text-[#00f2ff]" : "hover:bg-white/5"}`}>
               <MessageSquare size={18} />
             </button>
           </div>
        </header>

        <div className="flex-1 p-6 relative">
          <AnimatePresence mode="wait">
            <motion.div 
              key={activeTab} 
              initial={{ opacity: 0, y: 10 }} 
              animate={{ opacity: 1, y: 0 }} 
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              className="h-full w-full"
            >
              {activeTab === "war_room" && (
                <WarRoom logs={globalLogs} isProcessing={isProcessing} onSend={executeDirective} audioUnlocked={audioUnlocked} unlockAudio={unlockAudio} />
              )}
              {activeTab === "artifact_studio" && <ArtifactStudio />}
              {activeTab === "neural_lattice" && <NeuralLattice />}
              {activeTab === "arsenal" && <ArsenalManager />}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>

      {/* COLUMN 3: THE INTELLIGENT ASSISTANT (RIGHT SIDEBAR) */}
      <AnimatePresence>
        {isAssistantOpen && (
          <motion.aside 
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: 420, opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            className="bg-[#0a0a0a] border-l border-white/5 flex flex-col shrink-0 overflow-hidden relative"
          >
            {/* OAUTH SECTION */}
            <div className="p-6 border-b border-white/5 bg-[#00f2ff]/5">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-[11px] font-black uppercase tracking-[0.2em] text-[#00f2ff]">Sovereign Context</h3>
                <ShieldCheck size={16} className="text-[#ff80bf]" />
              </div>
              <button className="w-full py-3 bg-white/5 border border-white/10 rounded-xl flex items-center justify-center gap-3 hover:bg-[#00f2ff]/10 hover:border-[#00f2ff]/30 transition-all group">
                <Github size={18} className="group-hover:text-[#00f2ff]" />
                <span className="text-[10px] font-black uppercase tracking-widest group-hover:text-[#00f2ff]">OAuth: Sign in to Repository</span>
              </button>
            </div>

            {/* CHAT LOGS */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-hide">
              {assistantLogs.map(log => (
                <div key={log.id} className="flex flex-col gap-2">
                   <div className="flex items-center gap-2">
                      <div className="w-5 h-5 rounded bg-[#ff80bf]/20 flex items-center justify-center">
                        <User size={12} className="text-[#ff80bf]" />
                      </div>
                      <span className="text-[9px] font-black text-white/30 uppercase">Mastermind</span>
                   </div>
                   <div className="p-4 bg-white/5 rounded-2xl text-[13px] leading-relaxed text-slate-300 border border-white/5 font-mono">
                     {log.text}
                   </div>
                </div>
              ))}
              {isProcessing && (
                <div className="flex items-center gap-2 animate-pulse px-2">
                  <Activity size={10} className="text-[#00f2ff]" />
                  <span className="text-[8px] font-black uppercase text-[#00f2ff]">Analyzing_Lattice_Telemetry...</span>
                </div>
              )}
            </div>

            {/* INPUT PORT */}
            <div className="p-6 border-t border-white/5 bg-black/20">
              <div className="relative">
                <textarea 
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  placeholder="Inquire with ForgeMaster..."
                  className="w-full bg-black border border-white/10 rounded-2xl p-4 pr-12 text-sm font-medium outline-none focus:border-[#ff80bf]/50 h-32 resize-none transition-all"
                />
                <button 
                  onClick={() => { if(chatInput) { setAssistantLogs(p => [...p, { id: Date.now(), role: 'user', text: chatInput }]); setChatInput(""); } }}
                  className="absolute bottom-4 right-4 p-2 bg-[#ff80bf] text-black rounded-lg hover:bg-white transition-all shadow-[0_0_20px_rgba(255,128,191,0.3)]"
                >
                  <Send size={18} fill="currentColor"/>
                </button>
              </div>
            </div>
          </motion.aside>
        )}
      </AnimatePresence>

      {/* CALIBRATION MODAL */}
      <AnimatePresence>
        {config.open && (
          <div className="fixed inset-0 bg-black/90 backdrop-blur-2xl flex items-center justify-center z-[1000]">
            <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="bg-[#111111] border border-[#00f2ff]/30 p-12 rounded-3xl w-full max-w-xl">
               <h2 className="text-3xl font-black text-white mb-10 uppercase italic border-b-4 border-[#00f2ff] inline-block tracking-tighter">Calibration</h2>
               <div className="space-y-8 font-mono">
                  <div className="space-y-2">
                    <label className="text-[10px] uppercase font-black text-[#00f2ff] tracking-widest">Gateway_URL</label>
                    <input value={config.url} onChange={e => setConfig({...config, url: e.target.value})} className="w-full bg-black border border-white/10 p-5 rounded-xl text-[#00f2ff] outline-none" />
                  </div>
                  <div className="space-y-2">
                    <label className="text-[10px] uppercase font-black text-[#ff80bf] tracking-widest">God_Signature</label>
                    <input type="password" value={config.key} onChange={e => setConfig({...config, key: e.target.value})} className="w-full bg-black border border-white/10 p-5 rounded-xl text-[#ff80bf] outline-none" />
                  </div>
                  <button onClick={() => { localStorage.setItem("RF_URL", config.url); localStorage.setItem("RF_KEY", config.key); setConfig({...config, open: false}); window.location.reload(); }} className="w-full py-6 bg-[#00f2ff] text-black font-black uppercase text-lg rounded-2xl hover:bg-white transition-all">Suture Swarm Link</button>
               </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}

// Sub-component for Nav Icons
function NavIcon({ icon, active, onClick, label }) {
  return (
    <button 
      onClick={onClick}
      className={`w-12 h-12 flex items-center justify-center rounded-2xl transition-all relative group ${active ? "bg-[#ff80bf]/10 text-[#ff80bf] shadow-[0_0_15px_rgba(255,128,191,0.1)]" : "text-white/20 hover:text-white hover:bg-white/5"}`}
    >
      {icon}
      <span className="absolute left-20 bg-[#ff80bf] text-black px-2 py-1 text-[9px] font-black uppercase rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none tracking-widest z-[200]">
        {label}
      </span>
    </button>
  );
}