/**
 * REALM FORGE: TITAN NEURAL LATTICE v30.0
 * ARCHITECT: LEAD SWARM ENGINEER
 * STATUS: PRODUCTION READY - SPATIAL CLUSTER ENGINE
 * PATH: F:\RealmForge\client\components\chambers\NeuralLattice.tsx
 */

// @ts-nocheck
"use client";

import React, { useEffect, useRef, useState, useMemo } from "react";
import axios from "axios";
import { 
  Network, Database, Info, Maximize2, RefreshCw, 
  AlertTriangle, ShieldCheck, Filter, Search, 
  Cpu, Zap, Fingerprint, Activity, Layers
} from "lucide-react";
import dynamic from "next/dynamic";
import { motion, AnimatePresence } from "framer-motion";

const ForceGraph2D = dynamic(() => import("react-force-graph-2d"), {
  ssr: false,
  loading: () => (
    <div className="flex-1 flex flex-col items-center justify-center bg-[#05070a] text-[#b5a642] h-full">
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
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState("ALL");
  const [searchQuery, setSearchQuery] = useState("");
  const containerRef = useRef(null);
  const graphRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });

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
    window.addEventListener("resize", updateDimensions);
    fetchGraph();
    return () => window.removeEventListener("resize", updateDimensions);
  }, []);

  const fetchGraph = async () => {
    const url = localStorage.getItem("RF_URL");
    const key = localStorage.getItem("RF_KEY");
    if (!url) return;

    setLoading(true);
    setError(null);
    try {
      const res = await axios.get(`${url.replace(/\/$/, "")}/api/v1/graph`, {
        headers: { "X-API-Key": key, "ngrok-skip-browser-warning": "69420" },
      });

      const rawNodes = res.data.nodes || [];
      const rawLinks = res.data.links || [];

      // --- INDUSTRIAL CATEGORIZATION ---
      const cleanNodes = rawNodes
        .filter(n => n.id && n.id.trim() !== "")
        .map(n => ({
            ...n,
            sector: n.sector || n.department?.toLowerCase() || "general_engineering",
            category: n.type || (n.id.startsWith("ARC-") ? "AGENT" : n.id.startsWith("RF-") ? "TASK" : "ARTIFACT"),
            mastery: Math.floor(Math.random() * 100) // Visual flair for HUD
        }));

      const nodeIds = new Set(cleanNodes.map(n => n.id));
      const cleanLinks = rawLinks.filter(l => nodeIds.has(l.source) && nodeIds.has(l.target));

      setData({ nodes: cleanNodes, links: cleanLinks });
    } catch (e) {
      setError("Uplink failed. Check Forge Gateway.");
    } finally {
      setLoading(false);
    }
  };

  const filteredData = useMemo(() => {
    let nodes = data.nodes;
    if (filter !== "ALL") nodes = nodes.filter(n => n.sector === filter || n.category === filter);
    if (searchQuery) nodes = nodes.filter(n => n.id.toLowerCase().includes(searchQuery.toLowerCase()));
    
    const nodeIds = new Set(nodes.map(n => n.id));
    const links = data.links.filter(l => nodeIds.has(typeof l.source === 'object' ? l.source.id : l.source) && nodeIds.has(typeof l.target === 'object' ? l.target.id : l.target));
    
    return { nodes, links };
  }, [data, filter, searchQuery]);

  const getNodeColor = (node) => {
    if (node.id === selectedNode?.id) return "#ffffff";
    switch (node.category) {
        case "AGENT": return "#b5a642"; // Forge Gold
        case "TASK": return "#00f2ff";  // Kinetic Cyan
        case "ARTIFACT": return "#ff3e3e"; // Cyber Red
        default: return "#4a4a4a";
    }
  };

  return (
    <div className="h-full flex gap-4 bg-black relative p-2 overflow-hidden" ref={containerRef}>
      
      <div className="flex-1 titan-card relative bg-[#05070a] overflow-hidden border-[#b5a642]/10">
        
        {/* --- SPATIAL HUD OVERLAY --- */}
        <div className="absolute top-6 left-6 z-50 flex flex-col gap-3 pointer-events-none">
          <div className="flex gap-2 pointer-events-auto">
            <button 
                type="button"
                onClick={fetchGraph}
                title="Refresh graph"
                aria-label="Refresh graph"
                className="p-3 bg-[#b5a642] text-black hover:bg-white transition-all shadow-[4px_4px_0_#000] rounded-sm"
            >
                <RefreshCw className={loading ? "animate-spin" : ""} size={18} />
            </button>
            <div className="glass-panel px-4 py-2 flex items-center gap-3 border-[#b5a642]/20">
                <ShieldCheck size={14} className="text-[#b5a642]" />
                <span className="text-[10px] font-black text-white uppercase tracking-widest">
                  Lattice_Density: {filteredData.nodes.length} / {data.nodes.length}
                </span>
            </div>
          </div>

          {/* CATEGORY FILTER */}
          <div className="flex gap-2 pointer-events-auto">
            {["ALL", "AGENT", "TASK", "ARTIFACT"].map(cat => (
              <button 
                key={cat}
                onClick={() => setFilter(cat)}
                className={`px-3 py-1 text-[8px] font-black uppercase tracking-widest border transition-all
                ${filter === cat ? "bg-[#b5a642] border-[#b5a642] text-black" : "bg-black/60 border-white/10 text-white/40 hover:text-white"}`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* SECTOR LEGEND (GLASS) */}
          <div className="glass-panel p-4 space-y-2 border-white/5 pointer-events-auto max-h-64 overflow-y-auto scrollbar-hide">
              <div className="text-[8px] font-black text-white/20 uppercase tracking-[0.2em] mb-2">Sector_Distribution</div>
              {CANONICAL_SECTORS.map(s => (
                <div 
                  key={s} 
                  onClick={() => setFilter(s)}
                  className={`flex items-center gap-2 text-[8px] font-black uppercase cursor-pointer transition-all
                  ${filter === s ? "text-[#b5a642]" : "text-white/40 hover:text-white"}`}
                >
                  <Activity size={10} className={filter === s ? "animate-pulse" : ""} />
                  {s.replace(/_/g, " ")}
                </div>
              ))}
          </div>
        </div>

        {/* SEARCH BAR (FLOATING) */}
        <div className="absolute top-6 right-6 z-50 glass-panel border-white/10 p-1 flex items-center gap-2">
            <Search size={14} className="ml-2 text-white/20" />
            <input 
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="PROBE_NODE_ID..." 
              className="bg-transparent border-none outline-none text-[10px] text-[#b5a642] font-black uppercase w-48 p-2 placeholder:text-white/5"
            />
        </div>

        {error ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-red-500 z-40 bg-black/80">
            <AlertTriangle size={48} className="mb-4 animate-bounce" />
            <div className="text-[10px] font-black uppercase tracking-[0.3em]">{error}</div>
            <button onClick={fetchGraph} className="mt-4 px-6 py-2 border border-red-500 text-red-500 text-[9px] font-black uppercase">Retry_Uplink</button>
          </div>
        ) : (
          <ForceGraph2D
            ref={graphRef}
            graphData={filteredData}
            width={dimensions.width}
            height={dimensions.height}
            backgroundColor="#05070a"
            nodeColor={getNodeColor}
            nodeRelSize={5}
            linkColor={() => "rgba(181, 166, 66, 0.03)"}
            linkDirectionalParticles={1}
            linkDirectionalParticleSpeed={0.003}
            linkDirectionalParticleWidth={2}
            linkDirectionalParticleColor={() => "#b5a642"}
            d3AlphaDecay={0.02}
            d3VelocityDecay={0.3}
            onNodeClick={(node) => {
              setSelectedNode(node);
              graphRef.current.centerAt(node.x, node.y, 1000);
              graphRef.current.zoom(3, 1000);
            }}
            nodeCanvasObject={(node, ctx, globalScale) => {
              const label = node.id;
              const fontSize = 14 / globalScale;
              const size = 6 / globalScale + 2;
              
              // Draw Node Core
              ctx.beginPath();
              ctx.arc(node.x, node.y, size, 0, 2 * Math.PI, false);
              ctx.fillStyle = getNodeColor(node);
              ctx.fill();

              // Selection Ring
              if (selectedNode?.id === node.id) {
                ctx.beginPath();
                ctx.arc(node.x, node.y, size + 2, 0, 2 * Math.PI, false);
                ctx.strokeStyle = "#ffffff";
                ctx.lineWidth = 1;
                ctx.stroke();
              }

              // Labels - Only high zoom
              if (globalScale > 2.5) {
                ctx.font = `${fontSize}px "JetBrains Mono", monospace`;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillStyle = 'rgba(255,255,255,0.8)';
                ctx.fillText(label, node.x, node.y + size + 8);
              }
            }}
          />
        )}
      </div>

      {/* --- RIGHT: NEURAL INSPECTOR --- */}
      <aside className="w-96 bg-[#0c0e12]/90 backdrop-blur-xl border-l border-[#b5a642]/20 flex flex-col p-8 shadow-2xl relative">
        <div className="flex items-center gap-4 mb-10 border-b border-[#b5a642]/20 pb-6">
          <Fingerprint className="text-[#b5a642]" size={28} />
          <div>
            <h3 className="text-sm font-black text-white uppercase tracking-[0.2em]">Neural_Inspector</h3>
            <span className="text-[8px] text-white/30 uppercase font-bold tracking-widest">Lattice_Sovereignty_Audit</span>
          </div>
        </div>

        <AnimatePresence mode="wait">
          {selectedNode ? (
            <motion.div 
              key={selectedNode.id}
              initial={{ opacity: 0, x: 20 }} 
              animate={{ opacity: 1, x: 0 }} 
              exit={{ opacity: 0, x: -20 }}
              className="space-y-10 overflow-y-auto pr-2 scrollbar-hide flex-1"
            >
              <section>
                <div className="flex items-center gap-2 mb-2">
                   <Layers size={12} className="text-[#b5a642]" />
                   <h4 className="text-[9px] text-[#b5a642] font-black uppercase tracking-[0.2em]">Entity_ID</h4>
                </div>
                <div className="text-2xl font-black text-white leading-none break-all uppercase tracking-tighter italic">
                  {selectedNode.id}
                </div>
              </section>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white/5 border border-white/10 p-4 rounded-sm">
                  <span className="text-[7px] font-black text-white/20 uppercase block mb-1">Classification</span>
                  <span className="text-[10px] font-black text-[#00f2ff] uppercase">{selectedNode.category}</span>
                </div>
                <div className="bg-white/5 border border-white/10 p-4 rounded-sm">
                  <span className="text-[7px] font-black text-white/20 uppercase block mb-1">Sector_Clearance</span>
                  <span className="text-[10px] font-black text-[#b5a642] uppercase">{selectedNode.sector}</span>
                </div>
              </div>

              <section className="bg-black/50 border border-white/5 p-6 rounded-sm relative group">
                <div className="absolute top-0 right-0 p-2 opacity-10 group-hover:opacity-100 transition-opacity">
                   <Activity size={14} className="text-[#b5a642]" />
                </div>
                <h4 className="text-[9px] text-white/40 font-black uppercase mb-4 flex items-center gap-2 italic">
                  <Cpu size={10} /> Physical_DNA_Sequence
                </h4>
                <div className="space-y-3 font-mono">
                   {Object.entries(selectedNode).map(([key, val]) => {
                     if (["x", "y", "vx", "vy", "index", "id", "category", "sector", "mastery"].includes(key)) return null;
                     return (
                       <div key={key} className="flex flex-col border-b border-white/5 pb-2">
                         <span className="text-[7px] text-[#b5a642] uppercase font-bold">{key}</span>
                         <span className="text-[9px] text-slate-400 break-all">{JSON.stringify(val)}</span>
                       </div>
                     );
                   })}
                </div>
              </section>

              <div className="pt-6 border-t border-white/5">
                 <button 
                  onClick={() => setSelectedNode(null)}
                  className="w-full py-3 bg-white/5 border border-white/10 text-[9px] font-black uppercase text-white/40 hover:text-white hover:bg-[#ff3e3e]/10 hover:border-[#ff3e3e]/50 transition-all"
                 >
                   Terminate_Probe
                 </button>
              </div>
            </motion.div>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-center opacity-10">
              <Zap size={64} className="mb-6" />
              <p className="text-xs font-black uppercase tracking-[0.4em] leading-loose">
                Awaiting_Neural_Selection<br/>Initialize_Lattice_Probe
              </p>
            </div>
          )}
        </AnimatePresence>
      </aside>
    </div>
  );
}