import React, { useState } from 'react';
import { 
  CheckCircle2, AlertTriangle, ShieldCheck, Droplet, 
  ChevronDown, ChevronUp, Plus, Check, Scale, CloudSun, ArrowLeft, RefreshCw, Layers
} from 'lucide-react';

export default function RecommendationResults({ 
  result, 
  onReset, 
  selectedCropsForCompare, 
  onToggleCompare, 
  onOpenComparison,
  lang 
}) {
  const [expandedCropId, setExpandedCropId] = useState(result.recommendations[0]?.crop_id || null);
  const [showFilteredCrops, setShowFilteredCrops] = useState(false);

  const {
    location,
    agro_climatic_zone,
    weather_summary,
    reliability_score_pct,
    data_completeness_pct,
    missing_fields,
    recommendations,
    filtered_crops,
    agricultural_disclaimer
  } = result;

  return (
    <div className="py-8 max-w-5xl mx-auto px-4 sm:px-6 space-y-8">
      {/* Top Banner: Evaluation Diagnostics & Context */}
      <div className="glass-panel rounded-3xl p-6 sm:p-8 relative overflow-hidden border-forest-500/30">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-forest-800/60 pb-6">
          <div>
            <div className="flex items-center space-x-2 text-xs font-mono text-forest-300">
              <span className="w-2 h-2 rounded-full bg-forest-400" />
              <span>Agronomic Evaluation Complete &bull; ID #{result.recommendation_id}</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-1">
              Recommended Crops for {location.district}
            </h2>
            <p className="text-xs sm:text-sm text-slate-300 mt-1">
              Taluk: <strong className="text-white">{location.taluk}</strong> &bull; Zone: <strong className="text-forest-300">{agro_climatic_zone.name} ({agro_climatic_zone.code})</strong>
            </p>
          </div>

          {/* Action: New Evaluation Button */}
          <button
            onClick={onReset}
            className="flex items-center space-x-1.5 px-4 py-2 rounded-xl glass-panel-light hover:bg-forest-800/40 text-slate-200 text-xs font-semibold self-start md:self-auto transition-all"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>New Observation Evaluation</span>
          </button>
        </div>

        {/* Telemetry Strip: Reliability & Weather Source */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-6 text-xs">
          {/* Reliability Score */}
          <div className="p-3.5 rounded-2xl bg-forest-950/60 border border-forest-800/60 flex items-center space-x-3.5">
            <div className="w-10 h-10 rounded-xl bg-forest-900 flex items-center justify-center font-mono font-bold text-forest-300 text-sm">
              {reliability_score_pct}%
            </div>
            <div>
              <div className="font-semibold text-white">Evaluation Reliability</div>
              <div className="text-[11px] text-slate-400">
                {missing_fields.length === 0 ? 'Full field observations' : `${missing_fields.length} unobserved parameters`}
              </div>
            </div>
          </div>

          {/* Weather Ingestion Status */}
          <div className="p-3.5 rounded-2xl bg-forest-950/60 border border-forest-800/60 flex items-center space-x-3.5">
            <div className="w-10 h-10 rounded-xl bg-forest-900 flex items-center justify-center text-cyan-400">
              <CloudSun className="w-5 h-5" />
            </div>
            <div>
              <div className="font-semibold text-white">
                {weather_summary.temperature_c}°C &bull; {weather_summary.condition}
              </div>
              <div className="text-[11px] text-slate-400 truncate max-w-[180px]" title={weather_summary.source}>
                {weather_summary.source}
              </div>
            </div>
          </div>

          {/* Data Completeness */}
          <div className="p-3.5 rounded-2xl bg-forest-950/60 border border-forest-800/60 flex items-center space-x-3.5">
            <div className="w-10 h-10 rounded-xl bg-forest-900 flex items-center justify-center font-mono font-bold text-amber-300 text-sm">
              {data_completeness_pct}%
            </div>
            <div>
              <div className="font-semibold text-white">Data Completeness</div>
              <div className="text-[11px] text-slate-400">
                {data_completeness_pct < 100 ? 'Uncertainty penalty applied' : 'Complete observations'}
              </div>
            </div>
          </div>
        </div>

        {/* Missing Fields Warning Notice */}
        {missing_fields.length > 0 && (
          <div className="mt-4 p-3 rounded-xl bg-amber-950/40 border border-amber-600/30 text-amber-200 text-xs flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 flex-shrink-0 text-amber-400" />
            <span>
              Uncertainty Note: Results computed with missing inputs (<strong>{missing_fields.join(', ')}</strong>). 
              Performing the simple finger-feel soil test will improve recommendation precision.
            </span>
          </div>
        )}
      </div>

      {/* Main Recommendations List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold text-white flex items-center space-x-2">
            <ShieldCheck className="w-5 h-5 text-forest-400" />
            <span>Ranked Suitable Crops ({recommendations.length} Candidates)</span>
          </h3>
          <span className="text-xs text-slate-400">Ranked by 7-dimension weighted score</span>
        </div>

        {recommendations.map((item) => {
          const isExpanded = expandedCropId === item.crop_id;
          const isSelectedForCompare = selectedCropsForCompare.includes(item.crop_id);

          // Tier badge colors
          const tierColor = item.suitability_tier === 'Highly Suitable'
            ? 'bg-emerald-950/80 border-emerald-500/50 text-emerald-300'
            : item.suitability_tier === 'Moderately Suitable'
            ? 'bg-forest-950/80 border-forest-500/50 text-forest-300'
            : 'bg-amber-950/80 border-amber-500/50 text-amber-300';

          return (
            <div 
              key={item.crop_id}
              className={`glass-panel rounded-3xl transition-all duration-200 border ${
                isExpanded ? 'border-forest-400/50 shadow-xl' : 'border-forest-800/60 hover:border-forest-700/80'
              }`}
            >
              {/* Card Header Row */}
              <div 
                className="p-5 sm:p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 cursor-pointer select-none"
                onClick={() => setExpandedCropId(isExpanded ? null : item.crop_id)}
              >
                <div className="flex items-start space-x-3.5">
                  {/* Rank Badge */}
                  <div className="w-10 h-10 rounded-2xl bg-forest-900/90 border border-forest-600/40 flex items-center justify-center font-mono font-extrabold text-forest-300 text-sm flex-shrink-0 shadow-inner">
                    #{item.rank}
                  </div>

                  <div>
                    <div className="flex items-center space-x-2.5">
                      <h4 className="text-lg sm:text-xl font-bold text-white">{item.crop_name}</h4>
                      {item.kannada_name && (
                        <span className="text-base text-forest-300 font-medium">({item.kannada_name})</span>
                      )}
                      <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-semibold border ${tierColor}`}>
                        {item.suitability_tier}
                      </span>
                    </div>

                    <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-slate-300 mt-1">
                      <span>{item.category}</span>
                      <span>&bull;</span>
                      <span className="italic text-slate-400 font-serif">{item.scientific_name}</span>
                      <span>&bull;</span>
                      <span>Duration: {item.duration_days.average || 110} days</span>
                    </div>
                  </div>
                </div>

                {/* Score & Action Column */}
                <div className="flex items-center space-x-4 self-end sm:self-auto">
                  {/* Suitability Score Meter */}
                  <div className="text-right">
                    <div className="text-2xl font-mono font-extrabold text-forest-300">
                      {item.suitability_score}
                      <span className="text-xs text-slate-400 font-sans font-normal ml-0.5">/100</span>
                    </div>
                    <div className="text-[10px] text-slate-400 uppercase tracking-wider">Suitability</div>
                  </div>

                  {/* Add to Compare Button */}
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      onToggleCompare(item.crop_id);
                    }}
                    className={`flex items-center space-x-1 px-3 py-1.5 rounded-xl text-xs font-semibold border transition-all ${
                      isSelectedForCompare
                        ? 'bg-clay-600 border-clay-400 text-white'
                        : 'glass-panel-light border-forest-700/60 text-slate-300 hover:text-white'
                    }`}
                  >
                    {isSelectedForCompare ? <Check className="w-3.5 h-3.5" /> : <Plus className="w-3.5 h-3.5" />}
                    <span>{isSelectedForCompare ? 'Added' : 'Compare'}</span>
                  </button>

                  <div className="text-slate-400">
                    {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                  </div>
                </div>
              </div>

              {/* Expandable Accordion Body */}
              {isExpanded && (
                <div className="px-5 sm:px-6 pb-6 pt-2 border-t border-forest-800/60 space-y-6">
                  {/* 1. Sub-Score Breakdown Visual Bars */}
                  <div>
                    <div className="text-xs font-semibold text-slate-400 mb-2">Evaluation Sub-scores Breakdown</div>
                    <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 text-xs">
                      {[
                        { label: 'Regional Suitability', val: item.sub_scores.regional_score },
                        { label: 'Soil Compatibility', val: item.sub_scores.soil_score },
                        { label: 'Drainage Match', val: item.sub_scores.drainage_score },
                        { label: 'Water Balance', val: item.sub_scores.water_score },
                        { label: 'Seasonal Timing', val: item.sub_scores.season_score },
                      ].map(s => (
                        <div key={s.label} className="p-2.5 rounded-xl bg-forest-950/60 border border-forest-800/50">
                          <div className="flex justify-between text-[11px] mb-1">
                            <span className="text-slate-400 truncate">{s.label}</span>
                            <span className="font-mono font-bold text-forest-300">{Math.round(s.val)}%</span>
                          </div>
                          <div className="w-full h-1.5 bg-forest-900 rounded-full overflow-hidden">
                            <div 
                              className="h-full bg-forest-400 rounded-full"
                              style={{ width: `${Math.min(100, Math.max(0, s.val))}%` }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* 2. Why Recommended & Supporting Soil Observations */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-4 rounded-2xl bg-forest-950/50 border border-forest-800/60 space-y-2">
                      <div className="text-xs font-bold text-forest-300 uppercase tracking-wider flex items-center space-x-1.5">
                        <CheckCircle2 className="w-4 h-4 text-forest-400" />
                        <span>Why This Crop Was Selected</span>
                      </div>
                      <ul className="space-y-1.5 text-xs text-slate-300">
                        {item.reasons_for_selection.map((reason, idx) => (
                          <li key={idx} className="flex items-start space-x-2">
                            <span className="text-forest-400">&bull;</span>
                            <span>{reason}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="p-4 rounded-2xl bg-forest-950/50 border border-forest-800/60 space-y-2">
                      <div className="text-xs font-bold text-forest-300 uppercase tracking-wider flex items-center space-x-1.5">
                        <Layers className="w-4 h-4 text-forest-400" />
                        <span>Supporting Soil Observations</span>
                      </div>
                      <ul className="space-y-1.5 text-xs text-slate-300">
                        {item.supporting_soil_observations.map((soilNote, idx) => (
                          <li key={idx} className="flex items-start space-x-2">
                            <span className="text-forest-400">&bull;</span>
                            <span>{soilNote}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  {/* 3. Water Sufficiency Evaluation */}
                  <div className="p-4 rounded-2xl bg-forest-950/50 border border-forest-800/60 text-xs text-slate-300 leading-relaxed">
                    <div className="font-bold text-forest-300 uppercase tracking-wider text-[11px] mb-1 flex items-center space-x-1.5">
                      <Droplet className="w-3.5 h-3.5 text-cyan-400" />
                      <span>Water Sufficiency Evaluation</span>
                    </div>
                    <p>{item.water_sufficiency_notes}</p>
                    <div className="mt-2 text-slate-400 font-mono text-[11px]">
                      Crop Water Demand: {item.water_requirement_mm.min} - {item.water_requirement_mm.max} mm &bull; Optimal: {item.water_requirement_mm.optimal_min} - {item.water_requirement_mm.optimal_max} mm
                    </div>
                  </div>

                  {/* 4. Agricultural Risks & Package of Practices */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Risks Alert Box */}
                    <div className="p-4 rounded-2xl bg-red-950/30 border border-red-700/30 space-y-2">
                      <div className="text-xs font-bold text-red-300 uppercase tracking-wider flex items-center space-x-1.5">
                        <AlertTriangle className="w-4 h-4 text-red-400" />
                        <span>Critical Agricultural Risks</span>
                      </div>
                      <ul className="space-y-1 text-xs text-slate-300">
                        {item.potential_risks.map((risk, idx) => (
                          <li key={idx} className="flex items-start space-x-2">
                            <span className="text-red-400">&bull;</span>
                            <span>{risk}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Crucial Practices */}
                    <div className="p-4 rounded-2xl bg-forest-950/50 border border-forest-800/60 space-y-2">
                      <div className="text-xs font-bold text-forest-300 uppercase tracking-wider flex items-center space-x-1.5">
                        <ShieldCheck className="w-4 h-4 text-forest-400" />
                        <span>Package of Practices (PoP)</span>
                      </div>
                      <p className="text-xs text-slate-300 leading-relaxed">
                        {item.crucial_practices}
                      </p>
                    </div>
                  </div>

                  {/* 5. Verified Economic Overview */}
                  {item.economics && (
                    <div className="p-4 rounded-2xl bg-clay-950/40 border border-clay-700/40 text-xs space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-clay-300 uppercase tracking-wider text-[11px]">
                          Economic Cost &amp; Benchmark Indicator (CACP / UASB 2024-25)
                        </span>
                        <span className="text-[10px] text-slate-400">Non-guaranteed benchmark</span>
                      </div>
                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center pt-1 font-mono">
                        <div className="p-2 rounded-lg bg-forest-950/70 border border-forest-800/40">
                          <div className="text-slate-400 text-[10px]">Est. Cost / Acre</div>
                          <div className="text-white font-bold">₹{item.economics.total_cost_per_acre_inr?.toLocaleString()}</div>
                        </div>
                        <div className="p-2 rounded-lg bg-forest-950/70 border border-forest-800/40">
                          <div className="text-slate-400 text-[10px]">Yield Range / Acre</div>
                          <div className="text-white font-bold">{item.economics.avg_yield_quintals_per_acre_min} - {item.economics.avg_yield_quintals_per_acre_max} qtl</div>
                        </div>
                        <div className="p-2 rounded-lg bg-forest-950/70 border border-forest-800/40">
                          <div className="text-slate-400 text-[10px]">Official MSP / qtl</div>
                          <div className="text-clay-300 font-bold">₹{item.economics.benchmark_msp_inr_per_quintal?.toLocaleString()}</div>
                        </div>
                        <div className="p-2 rounded-lg bg-forest-950/70 border border-forest-800/40">
                          <div className="text-slate-400 text-[10px]">Benchmark Year</div>
                          <div className="text-slate-200 font-bold">{item.economics.data_year}</div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Transparent Filtered Crops Drawer */}
      {filtered_crops.length > 0 && (
        <div className="glass-panel rounded-3xl p-6 border-forest-900">
          <div 
            className="flex items-center justify-between cursor-pointer"
            onClick={() => setShowFilteredCrops(!showFilteredCrops)}
          >
            <div className="flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5 text-amber-400" />
              <h4 className="font-bold text-white text-base">
                Excluded Unsuitable Crops ({filtered_crops.length} Filtered Out)
              </h4>
            </div>
            <span className="text-xs text-forest-400 font-semibold flex items-center space-x-1">
              <span>{showFilteredCrops ? 'Hide Hard Constraints Log' : 'View Exclusions & Agricultural Reasons'}</span>
              {showFilteredCrops ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </span>
          </div>

          {showFilteredCrops && (
            <div className="mt-4 pt-4 border-t border-forest-800/60 space-y-3">
              <p className="text-xs text-slate-300">
                The recommendation engine strictly enforces agricultural hard constraints so farmers are not advised 
                to grow crops destined for failure (e.g. waterlog-sensitive pulses in stagnant water or rainfed sugarcane in dry zones).
              </p>
              <div className="space-y-2">
                {filtered_crops.map(fc => (
                  <div 
                    key={fc.crop_id}
                    className="p-3.5 rounded-2xl bg-forest-950/80 border border-forest-800/60 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs"
                  >
                    <div>
                      <div className="font-bold text-white flex items-center space-x-2">
                        <span>{fc.crop_name}</span>
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-red-950 text-red-300 border border-red-700/40">
                          {fc.constraint_type}
                        </span>
                      </div>
                      <p className="text-slate-300 mt-0.5">{fc.reason_for_exclusion}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Disclaimer Card */}
      <div className="p-4 rounded-2xl glass-panel-light border-forest-800/50 text-xs text-slate-300 space-y-1">
        <div className="font-bold text-forest-300 flex items-center space-x-1.5">
          <ShieldCheck className="w-4 h-4 text-forest-400" />
          <span>Agricultural Validation &amp; Traceability Note</span>
        </div>
        <p>{agricultural_disclaimer}</p>
      </div>
    </div>
  );
}
