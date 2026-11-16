import React, { useState } from 'react';
import { Layers, HelpCircle, AlertCircle, CheckCircle2, ArrowRight, Eye, ShieldCheck } from 'lucide-react';

export default function SoilIdentificationGuide({ lang }) {
  const [activeTab, setActiveTab] = useState('ribbon');

  return (
    <div className="py-8 max-w-5xl mx-auto px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div>
        <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-forest-900/60 border border-forest-500/30 text-forest-300 text-xs font-semibold mb-2">
          <Layers className="w-3.5 h-3.5 text-forest-400" />
          <span>Educational Observation Guide</span>
        </div>
        <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          {lang === 'kn' ? 'ಮಣ್ಣಿನ ವೀಕ್ಷಣೆ ಮತ್ತು ಗುರುತಿಸುವಿಕೆ ಕೈಪಿಡಿ' : 'Farmer’s Guide: Identifying Soil Texture & Drainage Without Lab Tests'}
        </h2>
        <p className="text-xs sm:text-sm text-slate-300 max-w-3xl mt-1">
          {lang === 'kn'
            ? 'ಪ್ರಯೋಗಾಲಯಕ್ಕೆ ಹೋಗದೆ ನಿಮ್ಮ ಕೈ ಮತ್ತು ಕಣ್ಣುಗಳಿಂದಲೇ ಮಣ್ಣಿನ ವಿನ್ಯಾಸ, ನೀರು ಇಂಗುವಿಕೆ ಮತ್ತು ಆಳವನ್ನು ಗುರುತಿಸುವ ಸುಲಭ ವಿಧಾನಗಳು.'
            : 'Simple, practical field tests proven by agricultural extension scientists to accurately observe soil physical behavior.'}
        </p>
      </div>

      {/* Warning & Scientific Honesty Banner */}
      <div className="p-4 rounded-2xl bg-amber-950/40 border border-amber-600/30 text-xs text-amber-200 flex items-start space-x-3">
        <AlertTriangle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
        <div className="leading-relaxed">
          <strong className="text-white block mb-0.5">Scientific Clarification on Soil Colour &amp; Laboratory Tests:</strong>
          Soil colour (red, dark black, brown) reflects iron oxides, geological origin, and moisture state, but 
          <strong> does NOT directly measure chemical NPK nutrients or exact soil pH</strong>. 
          SmartKrishi never fabricates exact chemical values from photographs. We rely strictly on physical physical properties that govern root growth, water percolation, and drainage.
        </div>
      </div>

      {/* Guide Tabs */}
      <div className="flex border-b border-forest-800">
        {[
          { id: 'ribbon', label: '1. The Ribbon & Finger Feel Test' },
          { id: 'jar', label: '2. The 24-Hour Jar Settling Test' },
          { id: 'drainage', label: '3. Drainage & Soil Depth Observation' },
        ].map(t => (
          <button
            key={t.id}
            onClick={() => setActiveTab(t.id)}
            className={`pb-3 px-4 text-xs font-semibold border-b-2 transition-all ${
              activeTab === t.id
                ? 'border-forest-400 text-forest-300'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Tab 1: Ribbon & Finger Feel Test */}
      {activeTab === 'ribbon' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="glass-panel p-5 rounded-2xl space-y-3">
              <div className="w-8 h-8 rounded-full bg-forest-900 border border-forest-700 font-mono font-bold text-xs flex items-center justify-center text-forest-300">
                1
              </div>
              <h4 className="font-bold text-white text-sm">Step 1: Ball Formation</h4>
              <p className="text-xs text-slate-300 leading-relaxed">
                Take a small fistful of topsoil (about 25g) from 15 cm depth. Moisten with water drop by drop until it has the consistency of moist putty (not soupy). Squeeze firmly into a ball.
              </p>
              <div className="p-2.5 rounded-xl bg-forest-950/70 text-[11px] text-slate-300">
                <strong className="text-forest-400">If it falls apart immediately:</strong> Sandy Soil.
              </div>
            </div>

            <div className="glass-panel p-5 rounded-2xl space-y-3">
              <div className="w-8 h-8 rounded-full bg-forest-900 border border-forest-700 font-mono font-bold text-xs flex items-center justify-center text-forest-300">
                2
              </div>
              <h4 className="font-bold text-white text-sm">Step 2: Roll the Ribbon</h4>
              <p className="text-xs text-slate-300 leading-relaxed">
                If it holds a ball, roll it between your palms into a roll the thickness of a pencil. Push the soil ribbon between thumb and forefinger, letting it squeeze out over your knuckle until it breaks under its weight.
              </p>
              <div className="p-2.5 rounded-xl bg-forest-950/70 text-[11px] text-slate-300">
                <strong className="text-forest-400">Ribbon Length Breakdown:</strong> See classification matrix below.
              </div>
            </div>

            <div className="glass-panel p-5 rounded-2xl space-y-3">
              <div className="w-8 h-8 rounded-full bg-forest-900 border border-forest-700 font-mono font-bold text-xs flex items-center justify-center text-forest-300">
                3
              </div>
              <h4 className="font-bold text-white text-sm">Step 3: Palm Rub Check</h4>
              <p className="text-xs text-slate-300 leading-relaxed">
                Pinch a small pea-sized portion of moist soil and rub it against the sensitive skin of your palm:
              </p>
              <ul className="text-[11px] text-slate-300 space-y-1">
                <li>&bull; <strong className="text-white">Very gritty/scratchy:</strong> Sand dominates</li>
                <li>&bull; <strong className="text-white">Smooth, floury, talc-like:</strong> Silt dominates</li>
                <li>&bull; <strong className="text-white">Greasy, plastic, sticky:</strong> Clay dominates</li>
              </ul>
            </div>
          </div>

          {/* Ribbon Length Decision Matrix */}
          <div className="glass-panel rounded-2xl p-6 space-y-4">
            <h4 className="font-bold text-white text-sm">Ribbon Length Interpretation Matrix</h4>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
              <div className="p-4 rounded-xl bg-forest-950/60 border border-forest-800/60">
                <div className="font-bold text-white text-sm">Ribbon &lt; 2.5 cm</div>
                <div className="text-forest-400 font-semibold mt-0.5">Loamy Sand / Sandy Loam</div>
                <p className="text-slate-300 mt-2 text-[11px] leading-relaxed">
                  Fast to moderate drainage. Highly suitable for Groundnut, Ragi, Horse Gram, Sesamum.
                </p>
              </div>

              <div className="p-4 rounded-xl bg-forest-950/60 border border-forest-800/60">
                <div className="font-bold text-white text-sm">Ribbon 2.5 cm - 5.0 cm</div>
                <div className="text-forest-400 font-semibold mt-0.5">Loam / Clay Loam</div>
                <p className="text-slate-300 mt-2 text-[11px] leading-relaxed">
                  Optimal balance of water retention and aeration. Ideal benchmark soil for Maize, Red Gram, Sunflower.
                </p>
              </div>

              <div className="p-4 rounded-xl bg-forest-950/60 border border-forest-800/60">
                <div className="font-bold text-white text-sm">Ribbon &gt; 5.0 cm</div>
                <div className="text-forest-400 font-semibold mt-0.5">Heavy Clay / Black Cotton (Vertisol)</div>
                <p className="text-slate-300 mt-2 text-[11px] leading-relaxed">
                  Extremely high moisture retention, deep cracks in summer. Best for Rabi Jowar, Chickpea, Cotton, Paddy.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Jar Settling Test */}
      {activeTab === 'jar' && (
        <div className="glass-panel rounded-2xl p-6 space-y-6">
          <div className="space-y-2">
            <h4 className="font-bold text-white text-base">The 24-Hour Clear Jar Sedimentation Test</h4>
            <p className="text-xs text-slate-300 leading-relaxed max-w-2xl">
              This simple test visually separates sand, silt, and clay into distinct physical layers based on settling velocity.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
            <div className="p-4 rounded-xl bg-forest-950/60 border border-forest-800/60 space-y-2">
              <div className="text-cyan-400 font-bold">1. At 1 Minute</div>
              <div className="text-white font-semibold">Sand Layer Settles</div>
              <p className="text-slate-300 text-[11px]">
                Coarse, heavy sand particles settle right to the bottom within 60 seconds.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-forest-950/60 border border-forest-800/60 space-y-2">
              <div className="text-cyan-400 font-bold">2. At 2 Hours</div>
              <div className="text-white font-semibold">Silt Layer Settles</div>
              <p className="text-slate-300 text-[11px]">
                Medium-weight silt particles settle as a distinct lighter-coloured middle band over the sand.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-forest-950/60 border border-forest-800/60 space-y-2">
              <div className="text-cyan-400 font-bold">3. At 24 to 48 Hours</div>
              <div className="text-white font-semibold">Clay Layer Settles</div>
              <p className="text-slate-300 text-[11px]">
                Fine clay particles settle as the topmost thin crust, leaving the water mostly clear.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Tab 3: Drainage & Depth */}
      {activeTab === 'drainage' && (
        <div className="glass-panel rounded-2xl p-6 space-y-6">
          <div className="space-y-2">
            <h4 className="font-bold text-white text-base">Observing Post-Rain Drainage &amp; Soil Depth</h4>
            <p className="text-xs text-slate-300 leading-relaxed max-w-2xl">
              Water standing time determines whether root-sensitive pulses will survive seasonal monsoons.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div className="p-4 rounded-xl bg-forest-950/60 border border-forest-800/60 space-y-2">
              <div className="text-forest-400 font-bold">The Puddle Duration Test</div>
              <p className="text-slate-300 text-[11px] leading-relaxed">
                After a normal soaking rain of 25-50 mm:
              </p>
              <ul className="space-y-1 text-slate-300 text-[11px]">
                <li>&bull; <strong className="text-white">Water gone in &lt;1 hour:</strong> Rapid drainage (Sandy)</li>
                <li>&bull; <strong className="text-white">Water soaks within 3-6 hours:</strong> Optimal drainage (Loam)</li>
                <li>&bull; <strong className="text-white">Water stands for &gt;24 hours:</strong> Waterlogged (Heavy Clay/Basin)</li>
              </ul>
            </div>

            <div className="p-4 rounded-xl bg-forest-950/60 border border-forest-800/60 space-y-2">
              <div className="text-forest-400 font-bold">The 30 cm Auger/Spade Test</div>
              <p className="text-slate-300 text-[11px] leading-relaxed">
                Dig a simple 30 cm hole in 3 spots across your field with an iron crowbar or spade:
              </p>
              <ul className="space-y-1 text-slate-300 text-[11px]">
                <li>&bull; <strong className="text-white">&lt;25 cm:</strong> Shallow soil (Rocks/Hardpan). Grow Ragi or Horse Gram.</li>
                <li>&bull; <strong className="text-white">25-75 cm:</strong> Medium depth. Suitable for all annual crops.</li>
                <li>&bull; <strong className="text-white">&gt;75 cm:</strong> Deep soil. Ideal for Sugarcane, Cotton, and Red Gram.</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
