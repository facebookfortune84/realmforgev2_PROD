/**
 * REALM FORGE: TITAN WAR ROOM v30.0
 * ARCHITECT: LEAD SWARM ENGINEER
 * STATUS: PRODUCTION READY - BENTO-GRID INDUSTRIAL REDESIGN
 * PATH: F:\RealmForge\client\components\chambers\WarRoom.tsx
 */

// @ts-nocheck
"use client";

import { useState, useRef, useEffect, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Send, Radio, Activity, Users, Search, Terminal,
  Volume2, VolumeX, Zap, ShieldCheck, BadgeCheck,
  Cpu, Shield, Database, Layout, BarChart, Scale, 
  FlaskConical, Gavel, Megaphone, UserPlus, CheckCircle, 
  Factory, Wrench, ChevronRight
} from "lucide-react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

// --- 13 CANONICAL INDUSTRIAL SECTORS ---
const SECTOR_METADATA = [
  { id: "software_engineering", label: "Software Eng", icon: <Cpu size={16}/> },
  { id: "cyber_security", label: "Cyber Security", icon: <Shield size={16}/> },
  { id: "data_intelligence", label: "Data Intel", icon: <Database size={16}/> },
  { id: "devops_infrastructure", label: "DevOps Infra", icon: <Layout size={16}/> },
  { id: "financial_ops", label: "Financial Ops", icon: <BarChart size={16}/> },
  { id: "legal_compliance", label: "Legal", icon: <Scale size={16}/> },
  { id: "research_development", label: "R&D", icon: <FlaskConical size={16}/> },
  { id: "executive_board", label: "Exec Board", icon: <Gavel size={16}/> },
  { id: "marketing_pr", label: "Marketing", icon: <Megaphone size={16}/> },
  { id: "human_capital", label: "Human Capital", icon: <UserPlus size={16}/> },
  { id: "quality_assurance", label: "QA / Audit", icon: <CheckCircle size={16}/> },
  { id: "facility_management", label: "Facilities", icon: <Factory size={16}/> },
  { id: "general_engineering", label: "General Eng", icon: <Wrench size={16}/> },
];

export default function WarRoom({ 
  logs, 
  activeDept, 
  activeAgent, 
  isProcessing, 
  onSend, 
  unlockAudio, 
  audioUnlocked 
}) {
  const [task, setTask] = useState("");
  const [roster, setRoster] = useState([]);
  const [hasMounted, setHasMounted] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    setHasMounted(true);
    fetchRoster();
  }, []);

  useEffect(() => { 
    if (hasMounted && logs) {
      chatEndRef.current?.scrollIntoView({ behavior: "smooth" }); 
    }
  }, [logs, hasMounted]);

  const fetchRoster = async () => {
    const url = localStorage.getItem("RF_URL");
    const key = localStorage.getItem("RF_KEY");
    if (!url) return;
    try {
      const res = await axios.get(`${url.replace(/\/$/, "")}/api/v1/agents`, { 
        headers: { "X-API-Key": key, "ngrok-skip-browser-warning": "69420" } 
      });
      setRoster(res.data.roster || []);
    } catch (e) { console.error("Lattice_Offline: Roster unreachable."); }
  };

  const handleDirective = () => {
    if (!task.trim() || isProcessing) return;
    onSend(task);
    setTask("");
  };

  if (!hasMounted) return null;

  return (
    <div className="h-full flex gap-4 overflow-hidden">
      
      {/* --- LEFT: BENTO SECTOR MATRIX --- */}
      <div className="w-[380px] flex flex-col gap-4 shrink-0 h-full">
        
        {/* SENSORY IGNITION */}
        <div className="titan-card p-1">
          <button 
            onClick={unlockAudio} 
            className={`w-full py-4 rounded-md transition-all font-black text-[10px] uppercase tracking-[0.3em] flex items-center justify-center gap-3
            ${audioUnlocked 
              ? "bg-green-500/10 text-green-500 border border-green-500/50 shadow-[0_0_20px_rgba(34,197,94,0.1)]" 
              : "bg-[#b5a642]/5 text-[#b5a642] border border-[#b5a642]/30 animate-pulse hover:bg-[#b5a642]/10"}`}
          >
            {audioUnlocked ? <Volume2 size={16} className="animate-pulse" /> : <VolumeX size={16}/>}
            {audioUnlocked ? "Vocal_Path: Synchronized" : "Ignite Sensory Link"}
          </button>
        </div>

        {/* 13-SECTOR BENTO GRID */}
        <div className="titan-card p-4 flex-1 flex flex-col overflow-hidden relative border-[#b5a642]/10 bg-black/40">
          <div className="flex items-center justify-between mb-4 border-b border-white/5 pb-2">
            <h3 className="text-[9px] font-black text-white/40 uppercase tracking-[0.3em] flex items-center gap-2">
               <Activity size={12} className="text-[#b5a642]" /> Sector_Status_Matrix
            </h3>
            <span className="text-[8px] font-mono text-[#00f2ff]">{roster.length} EEs</span>
          </div>

          <div className="grid grid-cols-2 gap-2 overflow-y-auto pr-1 scrollbar-hide">
            {SECTOR_METADATA.map((sector) => {
              const isActive = activeDept.toLowerCase().replace(/ /g, "_") === sector.id;
              const agentCount = roster.filter(a => (a.dept || a.sector)?.toLowerCase() === sector.id).length;

              return (
                <motion.div 
                  key={sector.id}
                  animate={isActive ? { scale: 1.02 } : { scale: 1 }}
                  className={`p-3 rounded-md border flex flex-col gap-2 transition-all duration-500 relative overflow-hidden group
                  ${isActive 
                    ? "bg-[#b5a642]/20 border-[#b5a642] shadow-[0_0_25px_rgba(181,166,66,0.15)]" 
                    : "bg-white/5 border-white/5 grayscale opacity-60 hover:grayscale-0 hover:opacity-100 hover:border-white/10"}`}
                >
                  {isActive && (
                    <motion.div 
                      layoutId="activeGlow"
                      className="absolute inset-0 bg-gradient-to-br from-[#b5a642]/10 to-transparent" 
                    />
                  )}
                  
                  <div className="flex items-center justify-between relative z-10">
                    <div className={`${isActive ? "text-[#b5a642]" : "text-white/40"} transition-colors`}>
                      {sector.icon}
                    </div>
                    <span className="text-[7px] font-mono opacity-40">[{agentCount.toString().padStart(3, '0')}]</span>
                  </div>

                  <div className="relative z-10">
                    <div className={`text-[9px] font-black uppercase tracking-tighter ${isActive ? "text-white" : "text-white/30"}`}>
                      {sector.label}
                    </div>
                    {isActive && (
                      <motion.div 
                        initial={{ opacity: 0 }} 
                        animate={{ opacity: 1 }}
                        className="text-[7px] text-[#b5a642] font-bold mt-1 flex items-center gap-1"
                      >
                        <Zap size={8} fill="currentColor" /> COMMAND_ACTIVE
                      </motion.div>
                    )}
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>

      {/* --- RIGHT: KINETIC LOGS & MISSION CONTROL --- */}
      <div className="flex-1 flex flex-col bg-[#080a0c] border border-white/5 relative overflow-hidden rounded-lg">
        
        {/* HEADER: SECTOR PATHWAY */}
        <div className="h-12 bg-black/40 border-b border-white/5 flex items-center px-6 justify-between">
            <div className="flex items-center gap-4 text-[9px] font-black uppercase tracking-[0.2em]">
                <div className="flex items-center gap-2">
                  <Terminal size={12} className="text-[#00f2ff]" />
                  <span className="text-white/40">Mission_Trace</span>
                </div>
                <ChevronRight size={12} className="text-white/10" />
                <span className="text-[#b5a642] italic underline decoration-[#b5a642]/30 underline-offset-4">{activeDept}</span>
            </div>
            <div className="flex items-center gap-2">
               <div className={`w-2 h-2 rounded-full ${isProcessing ? "bg-green-500 animate-pulse" : "bg-white/10"}`} />
               <span className="text-[8px] font-mono opacity-40 uppercase">{status}</span>
            </div>
        </div>

        {/* LOG STREAM: INDUSTRIAL TERMINAL STYLE */}
        <div className="flex-1 overflow-y-auto p-8 space-y-8 scrollbar-hide">
          <AnimatePresence initial={false}>
            {logs.map((log, i) => (
              <motion.div 
                key={log.id || i} 
                initial={{ opacity: 0, y: 10 }} 
                animate={{ opacity: 1, y: 0 }} 
                className="group"
              >
                {/* Meta-Header */}
                <div className={`flex items-center gap-3 mb-3 ${log.agent === 'ARCHITECT' ? 'flex-row-reverse' : ''}`}>
                  <div className={`text-[9px] font-black uppercase tracking-widest px-2 py-0.5 rounded ${log.type === 'user' ? 'bg-[#b5a642] text-black' : 'bg-white/5 text-[#00f2ff]'}`}>
                    {log.agent || 'NEXUS'}
                  </div>
                  <span className="text-[8px] font-mono opacity-20 italic">{log.timestamp}</span>
                </div>

                {/* Content Frame */}
                <div className={`p-6 text-xs leading-relaxed font-mono relative border-l-2 transition-all group-hover:border-l-4
                  ${log.type === 'user' 
                    ? 'bg-[#b5a642]/5 border-[#b5a642] text-slate-100 ml-12' 
                    : 'bg-black/40 border-[#00f2ff]/40 text-[#a8d4d4] mr-12'}`}
                >
                  <ReactMarkdown 
                    remarkPlugins={[remarkGfm]}
                    components={{
                      h1: (p) => <h1 className="text-lg font-black text-white uppercase mb-4 border-b border-white/10 pb-1" {...p} />,
                      h3: (p) => <h3 className="text-[#00f2ff] font-bold uppercase mt-6 mb-2 flex items-center gap-2" {...p} />,
                      code: (p) => <code className="bg-black p-1 text-[#ff8c00] rounded-sm border border-white/5" {...p} />,
                      table: (p) => <div className="overflow-x-auto my-4 border border-white/5"><table className="min-w-full text-[10px]" {...p} /></div>,
                      th: (p) => <th className="bg-white/5 p-2 text-left text-[#b5a642] border border-white/5" {...p} />,
                      td: (p) => <td className="p-2 border border-white/5 opacity-80" {...p} />
                    }}
                  >
                    {log.content}
                  </ReactMarkdown>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
          <div ref={chatEndRef} />
        </div>

        {/* MISSION INPUT PORT */}
        <div className="p-6 bg-black/60 border-t border-white/10 relative">
          <div className="max-w-4xl mx-auto flex gap-4 items-end">
            <div className="flex-1 bg-white/5 border border-white/10 rounded-md p-4 transition-all focus-within:border-[#b5a642]/50">
              <textarea 
                value={task} 
                onChange={(e) => setTask(e.target.value)} 
                onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleDirective()} 
                placeholder="INPUT_INDUSTRIAL_DIRECTIVE..." 
                className="w-full bg-transparent text-[#00f2ff] font-mono text-sm outline-none resize-none placeholder:text-white/5 h-12 scrollbar-hide"
                disabled={isProcessing}
                spellCheck={false}
              />
              <div className="flex justify-between mt-2 text-[8px] uppercase font-black tracking-widest text-white/20">
                <span>Secure_Channel_Uplink</span>
                <span>{task.length} / 2000_Chars</span>
              </div>
            </div>
            
            <button 
              onClick={handleDirective} 
              disabled={isProcessing || !audioUnlocked} 
              className="w-16 h-16 bg-[#b5a642] text-black flex items-center justify-center rounded-md hover:bg-white transition-all disabled:opacity-20 shadow-[5px_5px_0_rgba(181,166,66,0.2)] active:translate-y-1 active:shadow-none"
            >
              {isProcessing ? <Activity className="animate-spin" /> : <Zap size={24} fill="currentColor" />}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}