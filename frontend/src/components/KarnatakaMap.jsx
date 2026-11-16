import React, { useState } from 'react';
import { MapPin, Droplets, CloudRain, AlertCircle, ArrowRight, Search, ShieldCheck } from 'lucide-react';

export default function KarnatakaMap({ zones, districts, onSelectDistrictForWizard, lang }) {
  const [selectedDistrictName, setSelectedDistrictName] = useState('Chitradurga');
  const [hoveredDistrictName, setHoveredDistrictName] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [zoneFilter, setZoneFilter] = useState('ALL');

  // Zone colour palette (Earth/Natural Agro Tones, zero neon purple)
  const zoneColors = {
    1: '#d97706', // North Eastern Transition (Amber)
    2: '#ea580c', // North Eastern Dry (Orange Ochre)
    3: '#b45309', // Northern Dry (Terracotta)
    4: '#c2410c', // Central Dry (Rust Clay)
    5: '#65a30d', // Eastern Dry (Olive)
    6: '#16a34a', // Southern Dry (Leaf Green)
    7: '#059669', // Southern Transition (Emerald)
    8: '#0d9488', // Northern Transition (Teal)
    9: '#047857', // Hilly Malnad (Deep Pine)
    10: '#0284c7' // Coastal Zone (Ocean Teal)
  };

  // Geospatial grid positions for Karnataka's 31 districts (scaled for 600x700 SVG canvas)
  const districtMapNodes = [
    // Northern Tip
    { name: 'Bidar', x: 420, y: 50, zone_id: 1 },
    { name: 'Kalaburagi', x: 380, y: 110, zone_id: 2 },
    { name: 'Yadgir', x: 410, y: 170, zone_id: 2 },
    { name: 'Vijayapura', x: 260, y: 110, zone_id: 3 },
    { name: 'Bagalkote', x: 240, y: 170, zone_id: 3 },
    { name: 'Raichur', x: 380, y: 220, zone_id: 2 },
    
    // Northern Transition & Central
    { name: 'Belagavi', x: 150, y: 180, zone_id: 8 },
    { name: 'Dharwad', x: 190, y: 240, zone_id: 8 },
    { name: 'Gadag', x: 250, y: 240, zone_id: 3 },
    { name: 'Koppal', x: 310, y: 230, zone_id: 3 },
    { name: 'Ballari', x: 410, y: 290, zone_id: 3 },
    { name: 'Vijayanagara', x: 330, y: 290, zone_id: 3 },
    { name: 'Haveri', x: 220, y: 310, zone_id: 8 },
    
    // Central Plateau
    { name: 'Uttara Kannada', x: 110, y: 280, zone_id: 10 },
    { name: 'Shivamogga', x: 200, y: 380, zone_id: 7 },
    { name: 'Davanagere', x: 260, y: 350, zone_id: 4 },
    { name: 'Chitradurga', x: 320, y: 380, zone_id: 4 },
    
    // Coastal & Western Ghats
    { name: 'Udupi', x: 110, y: 440, zone_id: 10 },
    { name: 'Chikkamagaluru', x: 200, y: 450, zone_id: 9 },
    { name: 'Dakshina Kannada', x: 130, y: 510, zone_id: 10 },
    { name: 'Hassan', x: 230, y: 510, zone_id: 7 },
    { name: 'Kodagu', x: 170, y: 580, zone_id: 9 },
    
    // Southern & Eastern Dry
    { name: 'Tumakuru', x: 340, y: 470, zone_id: 4 },
    { name: 'Chikkaballapura', x: 440, y: 460, zone_id: 5 },
    { name: 'Kolar', x: 490, y: 510, zone_id: 5 },
    { name: 'Bengaluru Rural', x: 410, y: 520, zone_id: 5 },
    { name: 'Bengaluru Urban', x: 420, y: 550, zone_id: 5 },
    { name: 'Ramanagara', x: 360, y: 560, zone_id: 5 },
    { name: 'Mandya', x: 300, y: 550, zone_id: 6 },
    { name: 'Mysuru', x: 270, y: 610, zone_id: 6 },
    { name: 'Chamarajanagara', x: 340, y: 630, zone_id: 6 },
  ];

  const currentDistrict = districts.find(d => d.name === selectedDistrictName) || districts[0] || {};
  const currentZone = zones.find(z => z.id === currentDistrict.zone_id) || {};

  const filteredDistricts = districts.filter(d => {
    const matchSearch = d.name.toLowerCase().includes(searchTerm.toLowerCase());
    if (zoneFilter === 'ALL') return matchSearch;
    if (zoneFilter === 'DRY') return matchSearch && [2, 3, 4, 5, 6].includes(d.zone_id);
    if (zoneFilter === 'TRANSITION') return matchSearch && [1, 7, 8].includes(d.zone_id);
    if (zoneFilter === 'MALNAD_COASTAL') return matchSearch && [9, 10].includes(d.zone_id);
    return matchSearch;
  });

  return (
    <div className="py-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Section Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
        <div>
          <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-forest-900/60 border border-forest-500/30 text-forest-300 text-xs font-semibold mb-2">
            <MapPin className="w-3.5 h-3.5 text-forest-400" />
            <span>Interactive Geospatial Intelligence</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            {lang === 'kn' ? 'ಕರ್ನಾಟಕ ಕೃಷಿ-ಹವಾಮಾನ ವಲಯಗಳ ನಕ್ಷೆ' : 'Karnataka Agro-Climatic Zones & District Atlas'}
          </h2>
          <p className="text-sm text-slate-300 max-w-2xl mt-1">
            {lang === 'kn'
              ? 'ಕರ್ನಾಟಕದ 10 ಅಧಿಕೃತ ಕೃಷಿ ವಲಯಗಳು ಮತ್ತು 31 ಜಿಲ್ಲೆಗಳು. ಜಿಲ್ಲೆಯನ್ನು ಕ್ಲಿಕ್ ಮಾಡಿ ಆ ವಲಯದ ಹವಾಮಾನ, ಮಣ್ಣು ಮತ್ತು ಶಿಫಾರಸುಗಳನ್ನು ನೋಡಿ.'
              : 'Official ICAR/KSDA delineation of Karnataka’s 10 agro-climatic zones across 31 districts. Select any district to view its agronomic profile.'}
          </p>
        </div>

        {/* Filter Pills */}
        <div className="flex flex-wrap gap-2">
          {[
            { id: 'ALL', label: 'All 31 Districts' },
            { id: 'DRY', label: 'Dry Zones (Zones 2-6)' },
            { id: 'TRANSITION', label: 'Transition (1, 7, 8)' },
            { id: 'MALNAD_COASTAL', label: 'Malnad & Coastal (9, 10)' }
          ].map(f => (
            <button
              key={f.id}
              onClick={() => setZoneFilter(f.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                zoneFilter === f.id
                  ? 'bg-forest-600 text-white font-semibold shadow-md'
                  : 'glass-panel-light text-slate-300 hover:text-white'
              }`}
            >
              {f.label}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left: Interactive Karnataka Map Canvas */}
        <div className="lg:col-span-7 glass-panel rounded-3xl p-6 relative overflow-hidden flex flex-col items-center justify-center">
          <div className="w-full flex items-center justify-between mb-4">
            <span className="text-xs font-mono text-slate-400">
              Interactive SVG Canvas &bull; Karnataka (11.5°N - 18.5°N)
            </span>
            <div className="flex items-center space-x-2 text-[11px] text-slate-400">
              <span className="w-2.5 h-2.5 rounded-full bg-forest-500 inline-block" />
              <span>Click node to select</span>
            </div>
          </div>

          {/* SVG Map of Karnataka */}
          <div className="w-full max-w-[520px] aspect-[520/640] relative">
            <svg
              viewBox="0 0 560 690"
              className="w-full h-full drop-shadow-2xl"
              xmlns="http://www.w3.org/2000/svg"
            >
              {/* Simplified Schematic Karnataka State Boundary Contour */}
              <path
                d="M 390 30 
                   Q 460 40, 440 90 
                   L 460 170 
                   L 440 260 
                   L 470 320 
                   L 460 440 
                   L 520 500 
                   L 490 560 
                   L 450 600 
                   L 370 670 
                   L 310 650 
                   L 250 630 
                   L 150 590 
                   L 110 500 
                   L 80 430 
                   L 90 310 
                   L 120 220 
                   L 160 160 
                   L 230 110 
                   L 290 80 
                   Z"
                fill="#0a261c"
                stroke="rgba(74, 222, 128, 0.25)"
                strokeWidth="2.5"
                strokeDasharray="4 4"
                className="transition-all"
              />

              {/* Coastal Blue Outline Strip */}
              <path
                d="M 120 220 L 90 310 L 80 430 L 110 500 L 150 590"
                fill="none"
                stroke="#0284c7"
                strokeWidth="4"
                strokeLinecap="round"
                opacity="0.6"
              />

              {/* District Connection Rays / Triangulation */}
              {districtMapNodes.map((node, i) => {
                if (i % 3 === 0 && i < districtMapNodes.length - 2) {
                  const nextNode = districtMapNodes[i + 1];
                  return (
                    <line
                      key={`line-${i}`}
                      x1={node.x}
                      y1={node.y}
                      x2={nextNode.x}
                      y2={nextNode.y}
                      stroke="rgba(74, 222, 128, 0.08)"
                      strokeWidth="1"
                    />
                  );
                }
                return null;
              })}

              {/* District Interactive Nodes */}
              {districtMapNodes.map((node) => {
                const isSelected = selectedDistrictName === node.name;
                const isHovered = hoveredDistrictName === node.name;
                const color = zoneColors[node.zone_id] || '#15803d';

                return (
                  <g
                    key={node.name}
                    className="cursor-pointer transition-transform duration-200"
                    onClick={() => setSelectedDistrictName(node.name)}
                    onMouseEnter={() => setHoveredDistrictName(node.name)}
                    onMouseLeave={() => setHoveredDistrictName(null)}
                  >
                    {/* Pulsing ring around selected node */}
                    {isSelected && (
                      <circle
                        cx={node.x}
                        cy={node.y}
                        r="18"
                        fill="none"
                        stroke={color}
                        strokeWidth="2"
                        className="animate-ping opacity-75"
                      />
                    )}

                    {/* Outer Node Halo */}
                    <circle
                      cx={node.x}
                      cy={node.y}
                      r={isSelected ? 14 : isHovered ? 12 : 9}
                      fill={color}
                      fillOpacity={isSelected ? 0.9 : 0.6}
                      stroke="#ffffff"
                      strokeWidth={isSelected ? 2.5 : 1.5}
                      className="transition-all"
                    />

                    {/* District Name Label */}
                    <text
                      x={node.x}
                      y={node.y - 12}
                      textAnchor="middle"
                      fill={isSelected ? '#ffffff' : '#cbd5e1'}
                      fontSize={isSelected ? 11 : 9}
                      fontWeight={isSelected ? 'bold' : '500'}
                      className="pointer-events-none select-none font-sans drop-shadow-md"
                    >
                      {node.name}
                    </text>
                  </g>
                );
              })}
            </svg>
          </div>

          {/* Map Color Legend */}
          <div className="w-full mt-4 pt-4 border-t border-forest-800/60 grid grid-cols-2 sm:grid-cols-5 gap-2 text-[11px] text-slate-300">
            {zones.map(z => (
              <div key={z.id} className="flex items-center space-x-1.5 truncate">
                <span
                  className="w-2.5 h-2.5 rounded-full flex-shrink-0"
                  style={{ backgroundColor: zoneColors[z.id] || '#15803d' }}
                />
                <span className="truncate" title={z.name}>{z.name.replace(' Zone', '')}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Right: Selected District & Agro-Climatic Zone Detailed Profile */}
        <div className="lg:col-span-5 space-y-5">
          {/* District Quick Search Box */}
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder={lang === 'kn' ? 'ಜಿಲ್ಲೆ ಹುಡುಕಿ...' : 'Search Karnataka district...'}
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-forest-950/80 border border-forest-700/50 text-white placeholder-slate-400 text-sm focus:outline-none focus:border-forest-400 transition-colors"
            />
          </div>

          {/* Quick Select District Chips if searching */}
          {searchTerm && (
            <div className="glass-panel p-3 rounded-xl max-h-40 overflow-y-auto space-y-1">
              {filteredDistricts.length === 0 ? (
                <div className="text-xs text-slate-400 p-2">No district matching "{searchTerm}"</div>
              ) : (
                filteredDistricts.map(d => (
                  <button
                    key={d.name}
                    onClick={() => {
                      setSelectedDistrictName(d.name);
                      setSearchTerm('');
                    }}
                    className="w-full text-left px-3 py-1.5 rounded-lg text-xs text-slate-200 hover:bg-forest-800/60 flex items-center justify-between"
                  >
                    <span>{d.name}</span>
                    <span className="text-[10px] text-forest-400">Zone {d.zone_id}</span>
                  </button>
                ))
              )}
            </div>
          )}

          {/* Detailed Selected District Card */}
          <div className="glass-panel p-6 rounded-3xl space-y-5 border-l-4" style={{ borderLeftColor: zoneColors[currentDistrict.zone_id] || '#15803d' }}>
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center space-x-2">
                  <h3 className="text-2xl font-bold text-white">{currentDistrict.name}</h3>
                  {currentDistrict.kannada_name && (
                    <span className="text-base text-forest-300 font-medium">({currentDistrict.kannada_name})</span>
                  )}
                </div>
                <p className="text-xs text-slate-400 mt-0.5">
                  HQ: {currentDistrict.headquarters || currentDistrict.name} &bull; Lat: {currentDistrict.latitude}°N, Lon: {currentDistrict.longitude}°E
                </p>
              </div>

              <div
                className="px-2.5 py-1 rounded-lg text-xs font-bold text-white shadow-sm"
                style={{ backgroundColor: zoneColors[currentDistrict.zone_id] || '#15803d' }}
              >
                Zone {currentDistrict.zone_id}
              </div>
            </div>

            {/* Zone Tag & Overview */}
            <div className="p-3.5 rounded-xl bg-forest-950/60 border border-forest-800/60 space-y-1.5">
              <div className="text-xs font-semibold text-forest-300 flex items-center space-x-1.5">
                <ShieldCheck className="w-4 h-4 text-forest-400" />
                <span>{currentZone.name} ({currentZone.code})</span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">
                {currentZone.climate_description || 'Sub-humid to semi-arid tropical plain with seasonal monsoon.'}
              </p>
            </div>

            {/* Agronomic Telemetry Grid */}
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="p-3 rounded-xl bg-forest-900/40 border border-forest-800/50">
                <div className="flex items-center space-x-1.5 text-slate-400 mb-1">
                  <CloudRain className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Normal Annual Rain</span>
                </div>
                <div className="text-lg font-mono font-bold text-white">
                  {currentDistrict.normal_rainfall_mm} mm
                </div>
              </div>

              <div className="p-3 rounded-xl bg-forest-900/40 border border-forest-800/50">
                <div className="flex items-center space-x-1.5 text-slate-400 mb-1">
                  <AlertCircle className="w-3.5 h-3.5 text-amber-400" />
                  <span>Drought Vulnerability</span>
                </div>
                <div className="text-base font-semibold text-amber-300">
                  {currentDistrict.drought_vulnerability || 'Moderate'}
                </div>
              </div>
            </div>

            {/* Dominant Soils */}
            <div>
              <div className="text-xs font-semibold text-slate-400 mb-2">Dominant Soil Formations</div>
              <div className="flex flex-wrap gap-1.5">
                {(currentDistrict.dominant_soils || []).map((soil, idx) => (
                  <span
                    key={idx}
                    className="px-2.5 py-1 rounded-md bg-forest-900/70 border border-forest-700/50 text-xs text-slate-200"
                  >
                    {soil}
                  </span>
                ))}
              </div>
            </div>

            {/* Primary Crops Cultivated */}
            <div>
              <div className="text-xs font-semibold text-slate-400 mb-2">Primary Documented Crops in Zone</div>
              <div className="flex flex-wrap gap-1.5">
                {(currentZone.primary_crops || []).map((crop, idx) => (
                  <span
                    key={idx}
                    className="px-2.5 py-1 rounded-md bg-clay-950/70 border border-clay-700/40 text-xs text-clay-200"
                  >
                    {crop}
                  </span>
                ))}
              </div>
            </div>

            {/* Action Button: Feed District to Wizard */}
            <button
              onClick={() => onSelectDistrictForWizard(currentDistrict.name)}
              className="w-full flex items-center justify-center space-x-2 py-3 rounded-xl bg-forest-600 hover:bg-forest-500 text-white font-semibold text-sm shadow-md transition-all hover:scale-[1.01]"
            >
              <span>{lang === 'kn' ? 'ಈ ಜಿಲ್ಲೆಗೆ ಬೆಳೆ ಶಿಫಾರಸು ಪರಿಶೀಲಿಸಿ' : `Evaluate Crops for ${currentDistrict.name}`}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
