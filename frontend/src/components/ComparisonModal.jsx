import React, { useState, useEffect } from 'react';
import { X, Scale, Droplet, Clock, Thermometer, Layers, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function ComparisonModal({ isOpen, onClose, cropIds, onRemoveCrop, lang }) {
  const [comparisonData, setComparisonData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (isOpen && cropIds.length >= 2) {
      setIsLoading(true);
      fetch('/api/crops/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ crop_ids: cropIds })
      })
        .then(res => res.json())
        .then(data => {
          setComparisonData(data);
          setIsLoading(false);
        })
        .catch(err => {
          console.error("Comparison fetch error:", err);
          setIsLoading(false);
        });
    }
  }, [isOpen, cropIds]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm overflow-y-auto">
      <div className="glass-panel w-full max-w-5xl rounded-3xl p-6 sm:p-8 space-y-6 max-h-[90vh] overflow-y-auto border-forest-500/40 relative">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-forest-800/60 pb-4">
          <div className="flex items-center space-x-2.5">
            <div className="w-9 h-9 rounded-xl bg-forest-900 border border-forest-600/40 flex items-center justify-center text-forest-300">
              <Scale className="w-5 h-5 text-clay-400" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">
                {lang === 'kn' ? 'ಬೆಳೆ ಹೋಲಿಕೆ ಸ್ಟುಡಿಯೋ' : 'Side-by-Side Crop Comparison'}
              </h3>
              <p className="text-xs text-slate-300">
                Compare agronomic requirements, water demand, and economic benchmarks for up to 3 candidate crops.
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full glass-panel-light flex items-center justify-center text-slate-400 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {cropIds.length < 2 ? (
          <div className="py-12 text-center text-slate-300 text-sm">
            Please select at least 2 crops from the recommendation list to compare.
          </div>
        ) : isLoading ? (
          <div className="py-16 text-center text-forest-300 text-sm animate-pulse">
            Loading comparative agronomic benchmarks...
          </div>
        ) : comparisonData?.crops ? (
          <div className="space-y-6">
            {/* Side-by-Side Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {comparisonData.crops.map((crop) => (
                <div key={crop.crop_id} className="glass-panel-light rounded-2xl p-5 space-y-4 border border-forest-800/60 relative">
                  <div className="flex items-start justify-between">
                    <div>
                      <h4 className="text-lg font-bold text-white">{crop.crop_name}</h4>
                      {crop.kannada_name && (
                        <div className="text-xs text-forest-300 font-medium">{crop.kannada_name}</div>
                      )}
                      <div className="text-[11px] text-slate-400 font-serif italic mt-0.5">{crop.scientific_name}</div>
                    </div>
                    <button
                      onClick={() => onRemoveCrop(crop.crop_id)}
                      className="text-slate-400 hover:text-red-400 text-xs px-2 py-1 rounded-md glass-panel"
                      title="Remove from comparison"
                    >
                      Remove
                    </button>
                  </div>

                  {/* Water Requirements */}
                  <div className="p-3 rounded-xl bg-forest-950/60 text-xs space-y-1">
                    <div className="font-semibold text-cyan-400 flex items-center space-x-1.5">
                      <Droplet className="w-3.5 h-3.5" />
                      <span>Water Requirement (mm)</span>
                    </div>
                    <div className="text-base font-mono font-bold text-white">
                      {crop.water_requirement_mm.min} - {crop.water_requirement_mm.max} mm
                    </div>
                    <div className="text-[11px] text-slate-400">
                      Scarcity Tolerance: <strong>{crop.water_scarcity_tolerance}</strong>
                    </div>
                  </div>

                  {/* Duration & Seasons */}
                  <div className="p-3 rounded-xl bg-forest-950/60 text-xs space-y-1">
                    <div className="font-semibold text-amber-400 flex items-center space-x-1.5">
                      <Clock className="w-3.5 h-3.5" />
                      <span>Growing Duration</span>
                    </div>
                    <div className="text-sm font-semibold text-white">
                      {crop.duration_days.min} - {crop.duration_days.max} days ({crop.duration_days.category})
                    </div>
                    <div className="text-[11px] text-slate-400">
                      Seasons: {crop.suitable_seasons.join(', ')}
                    </div>
                  </div>

                  {/* Soil Texture & Drainage */}
                  <div className="p-3 rounded-xl bg-forest-950/60 text-xs space-y-1">
                    <div className="font-semibold text-forest-300 flex items-center space-x-1.5">
                      <Layers className="w-3.5 h-3.5" />
                      <span>Preferred Soil Texture</span>
                    </div>
                    <div className="text-slate-200">
                      {crop.preferred_soil_textures.join(', ')}
                    </div>
                    <div className="text-[11px] text-slate-400">
                      Drainage: {crop.drainage_preference}
                    </div>
                  </div>

                  {/* Temperature & Rainfall */}
                  <div className="p-3 rounded-xl bg-forest-950/60 text-xs space-y-1">
                    <div className="font-semibold text-slate-300 flex items-center space-x-1.5">
                      <Thermometer className="w-3.5 h-3.5 text-red-400" />
                      <span>Optimal Climate</span>
                    </div>
                    <div className="text-slate-200">Temp: {crop.temperature_range_c}</div>
                    <div className="text-slate-200">Rainfall: {crop.rainfall_range_mm}</div>
                  </div>

                  {/* Economics Indicator */}
                  {crop.economics && (
                    <div className="p-3 rounded-xl bg-clay-950/50 border border-clay-800/40 text-xs space-y-1">
                      <div className="font-semibold text-clay-300">Economic Benchmarks</div>
                      <div className="flex justify-between text-slate-300 font-mono">
                        <span>Est. Cost:</span>
                        <span className="text-white font-bold">₹{crop.economics.total_cost_per_acre_inr?.toLocaleString()} / ac</span>
                      </div>
                      <div className="flex justify-between text-slate-300 font-mono">
                        <span>Avg Yield:</span>
                        <span className="text-white font-bold">{crop.economics.avg_yield_quintals_per_acre_min}-{crop.economics.avg_yield_quintals_per_acre_max} qtl</span>
                      </div>
                      <div className="flex justify-between text-slate-300 font-mono">
                        <span>Official MSP:</span>
                        <span className="text-clay-300 font-bold">₹{crop.economics.benchmark_msp_inr_per_quintal?.toLocaleString()} / qtl</span>
                      </div>
                    </div>
                  )}

                  {/* Risks Alert */}
                  <div className="text-xs text-red-300 bg-red-950/30 p-2.5 rounded-xl border border-red-800/30">
                    <span className="font-semibold block mb-0.5 text-red-400">Key Risk Factor:</span>
                    <span>{crop.key_risks[0] || 'Observe local weather and pests.'}</span>
                  </div>
                </div>
              ))}
            </div>

            {/* Comparison Summary */}
            <div className="p-4 rounded-2xl glass-panel-light text-xs text-slate-300 leading-relaxed border-forest-800">
              <strong className="text-white">Comparative Takeaway: </strong>
              {comparisonData.comparison_summary}
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
