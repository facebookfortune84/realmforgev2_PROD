/**
 * REALM FORGE: TITAN NEURAL LATTICE v31.0
 * STYLE: CAFFEINE-NEON / HIGH-VISIBILITY
 * ARCHITECT: LEAD SWARM ENGINEER
 * STATUS: PRODUCTION READY - SPATIAL CLUSTER ENGINE
 * PATH: F:\RealmForge_PROD\client\components\chambers\NeuralLattice.tsx
 */

// @ts-nocheck
"use client";

import React, { useEffect, useRef, useState, useMemo } from "react";
import axios from "axios";
import { 
  Network, Database, Info, RefreshCw, 
  ShieldCheck, Filter, Search, Fingerprint, 
  Activity, Layers, Zap, Trash2, Binary
} from "lucide-react";
import dynamic from "next/dynamic";
import { motion, AnimatePresence } from "framer-motion";

const ForceGraph2D = dynamic(() => import("react-force-graph-2d"), {
  ssr: false,
  loading: () => (
    <div className="flex-1 flex flex-col items-center justify-center bg-[#050505] text-[#00f2ff] h-full">
      <RefreshCw className="animate-spin mb-4" size={48} />
      <span className="text-[10px] font-black uppercase tracking-[0.5em]">Pressurizing_Neural_Lattice</span>
    </div>
  ),
});

const CANONICAL_SECTORS = [
  "software_engineering", "cyber_security", "data_intelligence", 
  "devops_infrastructure", "financial_ops", "legal_compliance", 
  "research_development", "executive_board", "marketing_pr", 
  "human_capital", "quality_assurance", "facility_management", 
  "general_engineering"
];

export default function NeuralLattice() {
  const [data, setData] = useState({ nodes: [], links: [] });
  const [selectedNode, setSelectedNode] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState("ALL");
  const [searchQuery, setSearchQuery] = useState("");
  const containerRef = useRef(null);
  const graphRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });

  // --- 1. INDUSTRIAL THEME CONSTANTS ---
  const COLORS = {
    CYAN: "#00f2ff",
    BUBBLEGUM: "#ff80bf",
    PINK: "#ff007f",
    SLATE: "#1a1a1a",
    GREY: "#333333"
  };

  useEffect(() => {
    const updateDimensions = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.clientWidth,
          height: containerRef.current.clientHeight,
        });
      }
    };
    updateDimensions();
    if (typeof window !== 'undefined') {
        window.addEventListener("resize", updateDimensions);
        fetchGraph();
    }
    return () => window.removeEventListener("resize", updateDimensions);
  }, []);

  const fetchGraph = async () => {
    if (typeof window === 'undefined') return;
    const url = localStorage.getItem("RF_URL") || "http://localhost:8000";
    const key = localStorage.getItem("RF_KEY") || "sk-realm-god-mode-888";

    setLoading(true);
    try {
      const res = await axios.get(`${url.replace(/\/$/, "")}/api/v1/graph`, {
        headers: { "X-API-Key": key, "ngrok-skip-browser-warning": "69420" },
      });

      const rawNodes = res.data.nodes || [];
      const rawLinks = res.data.links || [];

      // --- KINETIC CLUSTERING LOGIC ---
      const cleanNodes = rawNodes
        .filter(n => n?.id)
        .map(n => ({
            ...n,
            sector: n.sector || n.department?.toLowerCase() || "general_engineering",
            category: n.type || (n.id.startsWith("ARC-") ? "AGENT" : n.id.startsWith("RF-") ? "TASK" : "KNOWLEDGE")
        }));

      const nodeIds = new Set(cleanNodes.map(n => n.id));
      const cleanLinks = rawLinks.filter(l => nodeIds.has(l.source) && nodeIds.has(l.target));

      setData({ nodes: cleanNodes, links: cleanLinks });
    } catch (e) {
      console.error("LATTICE_FAULT");
    } finally {
      setLoading(false);
    }
  };

  const filteredData = useMemo(() => {
    let nodes = data.nodes;
    if (filter !== "ALL") nodes = nodes.filter(n => n.sector === filter || n.category === filter);
    if (searchQuery) nodes = nodes.filter(n => n.id.toLowerCase().includes(searchQuery.toLowerCase()));
    
    const nodeIds = new Set(nodes.map(n => n.id));
    const links = data.links.filter(l => {
      const s = typeof l.source === 'object' ? l.source.id : l.source;
      const t = typeof l.target === 'object' ? l.target.id : l.target;
      return nodeIds.has(s) && nodeIds.has(t);
    });
    
    return { nodes, links };
  }, [data, filter, searchQuery]);

  const getNodeColor = (node) => {
    if (node.id === selectedNode?.id) return "#ffffff";
    switch (node.category) {
        case "AGENT": return COLORS.BUBBLEGUM;
        case "TASK": return COLORS.PINK;
        case "KNOWLEDGE": return COLORS.CYAN;
        default: return COLORS.GREY;
    }
  };

  const handleRebuild = async () => {
    const url = localStorage.getItem("RF_URL");
    const key = localStorage.getItem("RF_KEY");
    alert("🚀 Initiating System Core Re-Ingestion. This will prune orphan nodes...");
    try {
        await axios.post(`${url}/api/v1/mission`, { task: "Trigger a physical codebase ingestion scan." }, { headers: { "X-API-Key": key } });
    } catch (e) {}
  };

  return (
    <div className="h-full flex gap-6 bg-transparent relative overflow-hidden" ref={containerRef}>
      
      {/* --- GRAPH CANVAS --- */}
      <div className="flex-1 bg-[#0a0a0a] border border-white/5 rounded-3xl overflow-hidden relative shadow-2xl">
        
        {/* HUD OVERLAY */}
        <div className="absolute top-6 left-6 z-50 flex flex-col gap-3 pointer-events-none">
          <div className="flex gap-2 pointer-events-auto">
            <button onClick={fetchGraph} className="p-3 bg-[#00f2ff] text-black hover:bg-white transition-all rounded-xl shadow-lg">
                <RefreshCw className={loading ? "animate-spin" : ""} size={18} />
            </button>
            <div className="bg-[#111111]/80 backdrop-blur-xl border border-white/10 px-4 py-2 flex items-center gap-3 rounded-xl">
                <ShieldCheck size={16} className="text-[#ff80bf]" />
                <span className="text-[11px] font-black text-white uppercase tracking-widest">
                  Lattice_Sync: {filteredData.nodes.length} <span className="text-white/20">/</span> {data.nodes.length}
                </span>
            </div>
          </div>

          {/* QUICK CATEGORY FILTER */}
          <div className="flex gap-1 pointer-events-auto bg-black/40 p-1 rounded-xl border border-white/5">
            {["ALL", "AGENT", "TASK", "KNOWLEDGE"].map(cat => (
              <button 
                key={cat} onClick={() => setFilter(cat)}
                className={`px-4 py-1.5 text-[9px] font-black uppercase tracking-widest rounded-lg transition-all
                ${filter === cat ? "bg-[#00f2ff] text-black" : "text-white/40 hover:text-white hover:bg-white/5"}`}
              >
                {cat}
              </button>
            ))}
          </div>
          
          <button 
            onClick={handleRebuild}
            className="pointer-events-auto flex items-center gap-2 px-4 py-2 bg-red-500/10 border border-red-500/20 text-red-500 text-[9px] font-black uppercase rounded-lg hover:bg-red-500 hover:text-white transition-all w-fit"
          >
            <Trash2 size={12} /> Rebuild Neural Roster
          </button>
        </div>

        {/* SEARCH BAR */}
        <div className="absolute top-6 right-6 z-50 pointer-events-auto">
            <div className="bg-[#111111]/80 backdrop-blur-xl border border-white/10 p-1 flex items-center gap-2 rounded-2xl w-64 focus-within:border-[#00f2ff]/40 transition-all">
                <Search size={16} className="ml-3 text-white/20" />
                <input 
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  placeholder="PROBE_LATTICE_ID..." 
                  className="bg-transparent border-none outline-none text-[11px] text-[#00f2ff] font-bold uppercase w-full p-2.5 placeholder:text-white/5"
                />
            </div>
        </div>

        <ForceGraph2D
            ref={graphRef}
            graphData={filteredData}
            width={dimensions.width}
            height={dimensions.height}
            backgroundColor="#0a0a0a"
            nodeColor={getNodeColor}
            nodeRelSize={7}
            linkColor={() => "rgba(0, 242, 255, 0.05)"}
            linkDirectionalParticles={1}
            linkDirectionalParticleSpeed={0.005}
            linkDirectionalParticleWidth={1.5}
            linkDirectionalParticleColor={() => COLORS.CYAN}
            onNodeClick={(node) => {
              setSelectedNode(node);
              graphRef.current.centerAt(node.x, node.y, 800);
              graphRef.current.zoom(4, 800);
            }}
            nodeCanvasObject={(node, ctx, globalScale) => {
              const label = node.id;
              const fontSize = 14 / globalScale;
              const size = 6 / globalScale + 3;
              
              // Draw Outer Glow
              ctx.beginPath();
              ctx.arc(node.x, node.y, size + 1, 0, 2 * Math.PI, false);
              ctx.fillStyle = `${getNodeColor(node)}33`;
              ctx.fill();

              // Draw Node Core
              ctx.beginPath();
              ctx.arc(node.x, node.y, size, 0, 2 * Math.PI, false);
              ctx.fillStyle = getNodeColor(node);
              ctx.fill();

              if (selectedNode?.id === node.id) {
                ctx.beginPath();
                ctx.arc(node.x, node.y, size + 3, 0, 2 * Math.PI, false);
                ctx.strokeStyle = "#ffffff";
                ctx.lineWidth = 1;
                ctx.stroke();
              }

              // Labels at High Zoom
              if (globalScale > 3) {
                ctx.font = `bold ${fontSize}px "Inter", sans-serif`;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillStyle = '#ffffff';
                ctx.fillText(label, node.x, node.y + size + 10);
              }
            }}
          />
      </div>

      {/* --- RIGHT: NEURAL INSPECTOR --- */}
      <aside className="w-[420px] bg-[#0a0a0a] border border-white/5 rounded-3xl flex flex-col p-8 shadow-2xl relative shrink-0">
        <div className="flex items-center gap-4 mb-10 border-b border-white/5 pb-8">
          <div className="w-12 h-12 rounded-2xl bg-[#00f2ff]/10 flex items-center justify-center border border-[#00f2ff]/20 shadow-[0_0_20px_rgba(0,242,255,0.1)]">
            <Fingerprint className="text-[#00f2ff]" size={24} />
          </div>
          <div>
            <h3 className="text-sm font-black text-white uppercase tracking-[0.2em]">Neural_Inspector</h3>
            <span className="text-[9px] text-[#ff80bf] uppercase font-bold tracking-widest">Sovereign_Audit_Link</span>
          </div>
        </div>

        <AnimatePresence mode="wait">
          {selectedNode ? (
            <motion.div 
              key={selectedNode.id}
              initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}
              className="space-y-10 overflow-y-auto pr-2 scrollbar-hide flex-1"
            >
              <section>
                <div className="flex items-center gap-2 mb-2">
                   <Binary size={14} className="text-[#ff80bf]" />
                   <h4 className="text-[10px] text-[#ff80bf] font-black uppercase tracking-[0.2em]">Node_Identity</h4>
                </div>
                <div className="text-2xl font-black text-white leading-tight break-all uppercase tracking-tighter italic selection:bg-white selection:text-black">
                  {selectedNode.id}
                </div>
              </section>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white/5 border border-white/10 p-5 rounded-2xl">
                  <span className="text-[8px] font-black text-white/30 uppercase block mb-1 tracking-widest">Classification</span>
                  <span className="text-[11px] font-black text-[#00f2ff] uppercase">{selectedNode.category}</span>
                </div>
                <div className="bg-white/5 border border-white/10 p-5 rounded-2xl">
                  <span className="text-[8px] font-black text-white/30 uppercase block mb-1 tracking-widest">Sector_Access</span>
                  <span className="text-[11px] font-black text-[#ff80bf] uppercase">{selectedNode.sector}</span>
                </div>
              </div>

              <section className="bg-black/50 border border-white/5 p-6 rounded-2xl relative group">
                <div className="absolute top-4 right-4 p-2 opacity-10 group-hover:opacity-100 transition-opacity">
                   <Activity size={16} className="text-[#00f2ff]" />
                </div>
                <h4 className="text-[10px] text-white/40 font-black uppercase mb-6 flex items-center gap-2">
                  <Layers size={14} className="text-[#00f2ff]" /> RELATIONAL_DNA
                </h4>
                <div className="space-y-4 font-mono">
                   {Object.entries(selectedNode).map(([key, val]) => {
                     if (["x", "y", "vx", "vy", "index", "id", "category", "sector", "mastery"].includes(key)) return null;
                     return (
                       <div key={key} className="flex flex-col border-b border-white/5 pb-3">
                         <span className="text-[8px] text-[#00f2ff] uppercase font-black tracking-widest mb-1">{key}</span>
                         <span className="text-[11px] text-slate-400 break-all leading-relaxed">{JSON.stringify(val)}</span>
                       </div>
                     );
                   })}
                </div>
              </section>

              <div className="pt-6">
                 <button 
                  onClick={() => setSelectedNode(null)}
                  className="w-full py-4 bg-white/5 border border-white/10 text-[10px] font-black uppercase tracking-[0.2em] text-white/30 hover:text-white hover:bg-red-500/20 hover:border-red-500/50 rounded-xl transition-all"
                 >
                   De-link_Neural_Probe
                 </button>
              </div>
            </motion.div>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-center opacity-10">
              <Zap size={64} className="mb-6 text-[#00f2ff]" />
              <p className="text-[10px] font-black uppercase tracking-[0.5em] leading-loose text-[#00f2ff]">
                Awaiting_Lattice_Probe<br/>Select_Neural_Coordinate
              </p>
            </div>
          )}
        </AnimatePresence>
      </aside>
    </div>
  );
}