import React, { useState, useEffect } from 'react';
import { 
  MapPin, Layers, Droplets, Calendar, ArrowRight, ArrowLeft, 
  CheckCircle2, Compass, AlertCircle, Sparkles, Navigation, Info
} from 'lucide-react';

export default function RecommendationWizard({ 
  districts, 
  zones, 
  preselectedDistrict, 
  onSubmitWizard, 
  isLoading,
  lang 
}) {
  const [currentStep, setCurrentStep] = useState(1);

  // Form State
  const [formData, setFormData] = useState({
    state: 'Karnataka',
    district: preselectedDistrict || 'Chitradurga',
    taluk: '',
    village: '',
    latitude: null,
    longitude: null,
    soil_observation: {
      soil_colour: 'Red',
      soil_texture: 'Loamy',
      drainage: 'Water drains moderately',
      moisture_retention: 'Soil retains moisture for several days',
      soil_depth: 'Medium',
      presence_of_stones: false,
      rocky_ground: false,
      surface_erosion: false,
      waterlogging_observed: false,
      land_condition_notes: ''
    },
    water_availability: {
      irrigation_source: 'Borewell',
      availability_duration: 'Throughout season',
      has_drip_facility: false
    },
    land_profile: {
      slope_type: 'Flat land',
      approximate_area_acres: 2.0
    },
    farming_history: {
      previous_crop: 'Green gram',
      previous_season: 'Kharif',
      was_successful: true,
      approximate_yield: '',
      drought_affected: false,
      flood_affected: false,
      recurring_pest_problem: '',
      water_shortage_encountered: false
    },
    planned_season: 'Kharif',
    planned_sowing_month: 'July',
    duration_preference: 'Any',
    farming_objective: 'High Yield & Stability'
  });

  // Sync preselected district from Map if changed
  useEffect(() => {
    if (preselectedDistrict) {
      setFormData(prev => ({
        ...prev,
        district: preselectedDistrict,
        taluk: ''
      }));
    }
  }, [preselectedDistrict]);

  // Current District & Taluks list
  const currentDistrictObj = districts.find(d => d.name === formData.district) || districts[0] || {};
  const currentZoneObj = zones.find(z => z.id === currentDistrictObj.zone_id) || {};
  const availableTaluks = currentDistrictObj.taluks || [];

  // Set default taluk when district changes
  useEffect(() => {
    if (availableTaluks.length > 0 && !formData.taluk) {
      setFormData(prev => ({ ...prev, taluk: availableTaluks[0] }));
    }
  }, [formData.district, availableTaluks]);

  // GPS auto-locate
  const [gpsLoading, setGpsLoading] = useState(false);
  const handleDetectGPS = () => {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser.");
      return;
    }
    setGpsLoading(true);
    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;
        try {
          const res = await fetch(`/api/locations/resolve?lat=${lat}&lon=${lon}`);
          if (res.ok) {
            const data = await res.json();
            setFormData(prev => ({
              ...prev,
              district: data.district,
              taluk: data.taluk || '',
              latitude: lat,
              longitude: lon
            }));
          }
        } catch (err) {
          console.error("GPS resolve error:", err);
        } finally {
          setGpsLoading(false);
        }
      },
      (err) => {
        alert("GPS location access was denied or timed out.");
        setGpsLoading(false);
      },
      { timeout: 10000 }
    );
  };

  const steps = [
    { number: 1, title: lang === 'kn' ? 'ಸ್ಥಳ ಮತ್ತು ವಲಯ' : 'Location & Zone', icon: MapPin },
    { number: 2, title: lang === 'kn' ? 'ಮಣ್ಣಿನ ವೀಕ್ಷಣೆ' : 'Soil Observation', icon: Layers },
    { number: 3, title: lang === 'kn' ? 'ನೀರು ಮತ್ತು ಭೂಮಿ' : 'Water & Land', icon: Droplets },
    { number: 4, title: lang === 'kn' ? 'ಋತು ಮತ್ತು ಇತಿಹಾಸ' : 'Season & History', icon: Calendar },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmitWizard(formData);
  };

  return (
    <div className="py-8 max-w-4xl mx-auto px-4 sm:px-6">
      {/* Wizard Header Progress Steps */}
      <div className="mb-8">
        <div className="flex items-center justify-between relative">
          <div className="absolute left-0 top-1/2 -translate-y-1/2 w-full h-1 bg-forest-900 z-0" />
          <div 
            className="absolute left-0 top-1/2 -translate-y-1/2 h-1 bg-forest-500 transition-all duration-300 z-0"
            style={{ width: `${((currentStep - 1) / (steps.length - 1)) * 100}%` }}
          />

          {steps.map((s) => {
            const Icon = s.icon;
            const isCompleted = currentStep > s.number;
            const isCurrent = currentStep === s.number;
            return (
              <div 
                key={s.number}
                className="relative z-10 flex flex-col items-center cursor-pointer"
                onClick={() => setCurrentStep(s.number)}
              >
                <div 
                  className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-xs transition-all ${
                    isCurrent
                      ? 'bg-forest-500 text-white ring-4 ring-forest-500/30 shadow-lg'
                      : isCompleted
                      ? 'bg-forest-700 text-white'
                      : 'bg-forest-950 border border-forest-800 text-slate-400'
                  }`}
                >
                  {isCompleted ? <CheckCircle2 className="w-5 h-5 text-forest-200" /> : <Icon className="w-4 h-4" />}
                </div>
                <span className={`text-[11px] font-medium mt-1.5 hidden sm:block ${isCurrent ? 'text-forest-300 font-semibold' : 'text-slate-400'}`}>
                  {s.title}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Main Wizard Form Card */}
      <form onSubmit={handleSubmit} className="glass-panel rounded-3xl p-6 sm:p-8 space-y-6">
        {/* STEP 1: Location & Agro-Climatic Intelligence */}
        {currentStep === 1 && (
          <div className="space-y-6">
            <div className="border-b border-forest-800/60 pb-4">
              <h3 className="text-xl font-bold text-white flex items-center space-x-2">
                <MapPin className="w-5 h-5 text-forest-400" />
                <span>{lang === 'kn' ? 'ಹಂತ ೧: ಭೌಗೋಳಿಕ ಸ್ಥಳ ಮತ್ತು ಕೃಷಿ ವಲಯ' : 'Step 1: Geographic Location & Agro-Climatic Zone'}</span>
              </h3>
              <p className="text-xs text-slate-300 mt-1">
                {lang === 'kn'
                  ? 'ನಿಮ್ಮ ಜಿಲ್ಲೆ ಮತ್ತು ತಾಲೂಕನ್ನು ಆರಿಸಿ. ವ್ಯವಸ್ಥೆಯು ಅಧಿಕೃತ ಕೃಷಿ-ಹವಾಮಾನ ವಲಯಕ್ಕೆ ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಮ್ಯಾಪ್ ಮಾಡುತ್ತದೆ.'
                  : 'Select your Karnataka district and taluk. The system accurately correlates it to official ICAR agro-climatic zones.'}
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* State (Fixed to Karnataka) */}
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">State</label>
                <input
                  type="text"
                  value="Karnataka"
                  disabled
                  className="w-full px-3.5 py-2.5 rounded-xl bg-forest-950/40 border border-forest-800/60 text-slate-300 text-sm cursor-not-allowed font-medium"
                />
              </div>

              {/* GPS Auto-Detect Button */}
              <div className="flex items-end">
                <button
                  type="button"
                  onClick={handleDetectGPS}
                  disabled={gpsLoading}
                  className="w-full flex items-center justify-center space-x-2 px-4 py-2.5 rounded-xl glass-panel-light hover:bg-forest-800/50 text-forest-300 text-sm font-medium border border-forest-600/30 transition-all"
                >
                  <Navigation className={`w-4 h-4 ${gpsLoading ? 'animate-spin' : ''}`} />
                  <span>{gpsLoading ? 'Detecting GPS...' : 'Auto-Detect via GPS'}</span>
                </button>
              </div>

              {/* District Select */}
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  District <span className="text-red-400">*</span>
                </label>
                <select
                  value={formData.district}
                  onChange={(e) => {
                    const newDist = e.target.value;
                    const dObj = districts.find(d => d.name === newDist);
                    setFormData(prev => ({
                      ...prev,
                      district: newDist,
                      taluk: dObj?.taluks?.[0] || ''
                    }));
                  }}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-forest-950/80 border border-forest-700/60 text-white text-sm focus:outline-none focus:border-forest-400"
                >
                  {districts.map(d => (
                    <option key={d.name} value={d.name}>
                      {d.name} {d.kannada_name ? `(${d.kannada_name})` : ''}
                    </option>
                  ))}
                </select>
              </div>

              {/* Taluk Select */}
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Taluk <span className="text-red-400">*</span>
                </label>
                <select
                  value={formData.taluk}
                  onChange={(e) => setFormData(prev => ({ ...prev, taluk: e.target.value }))}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-forest-950/80 border border-forest-700/60 text-white text-sm focus:outline-none focus:border-forest-400"
                >
                  {availableTaluks.length > 0 ? (
                    availableTaluks.map(t => (
                      <option key={t} value={t}>{t}</option>
                    ))
                  ) : (
                    <option value={formData.district}>{formData.district} (General)</option>
                  )}
                </select>
              </div>
            </div>

            {/* Auto-Resolved Zone Banner */}
            <div className="p-4 rounded-2xl bg-forest-950/70 border border-forest-700/50 flex items-start space-x-3.5">
              <Compass className="w-5 h-5 text-forest-400 mt-0.5 flex-shrink-0" />
              <div>
                <div className="flex items-center space-x-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-forest-400">
                    Mapped Agro-Climatic Zone
                  </span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-forest-800 text-forest-200">
                    Zone {currentDistrictObj.zone_id} &bull; {currentZoneObj.code || 'ZONE'}
                  </span>
                </div>
                <h4 className="text-base font-semibold text-white mt-0.5">
                  {currentZoneObj.name}
                  {currentZoneObj.kannada_name && <span className="text-sm font-normal text-forest-300 ml-2">({currentZoneObj.kannada_name})</span>}
                </h4>
                <p className="text-xs text-slate-300 mt-1 leading-relaxed">
                  {currentZoneObj.climate_description}
                </p>
                <div className="flex flex-wrap gap-4 mt-2.5 text-xs text-slate-300">
                  <span><strong>Normal Rainfall:</strong> {currentDistrictObj.normal_rainfall_mm} mm</span>
                  <span><strong>Drought Risk:</strong> {currentDistrictObj.drought_vulnerability || 'Moderate'}</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* STEP 2: Soil Observation (Without Laboratory Tests) */}
        {currentStep === 2 && (
          <div className="space-y-6">
            <div className="border-b border-forest-800/60 pb-4">
              <h3 className="text-xl font-bold text-white flex items-center space-x-2">
                <Layers className="w-5 h-5 text-forest-400" />
                <span>{lang === 'kn' ? 'ಹಂತ ೨: ಮಣ್ಣಿನ ವೀಕ್ಷಣೆ (ಲ್ಯಾಬ್ ಪರೀಕ್ಷೆಯಿಲ್ಲದೆ)' : 'Step 2: Soil Observation (No Laboratory Tests)'}</span>
              </h3>
              <p className="text-xs text-slate-300 mt-1">
                {lang === 'kn'
                  ? 'ರೈತರು ಕಣ್ಣಿನಿಂದ ನೋಡುವ ಮತ್ತು ಕೈಯಿಂದ ಮುಟ್ಟಿ ತಿಳಿಯುವ ಲಕ್ಷಣಗಳನ್ನು ದಾಖಲಿಸಿ.'
                  : 'Record physical, observable characteristics. No chemical NPK or pH inputs required.'}
              </p>
            </div>

            {/* Soil Colour Selection */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-2">
                Soil Colour <span className="text-slate-400 font-normal">(Mineral indicator, not exact fertility)</span>
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                {[
                  { id: 'Red', label: 'Red Soil', swatch: '#b91c1c' },
                  { id: 'Reddish brown', label: 'Reddish Brown', swatch: '#9a3412' },
                  { id: 'Dark black', label: 'Dark Black (Regur)', swatch: '#1c1917' },
                  { id: 'Brown', label: 'Brown Soil', swatch: '#78350f' },
                  { id: 'Yellowish', label: 'Yellowish', swatch: '#ca8a04' },
                  { id: 'Grey', label: 'Grey Soil', swatch: '#64748b' },
                  { id: 'Light sandy', label: 'Light Sandy', swatch: '#d97706' },
                  { id: 'Mixed', label: 'Mixed / Pebble', swatch: '#57534e' }
                ].map(c => (
                  <button
                    key={c.id}
                    type="button"
                    onClick={() => setFormData(prev => ({
                      ...prev,
                      soil_observation: { ...prev.soil_observation, soil_colour: c.id }
                    }))}
                    className={`p-2.5 rounded-xl flex items-center space-x-2.5 text-xs text-left border transition-all ${
                      formData.soil_observation.soil_colour === c.id
                        ? 'bg-forest-900 border-forest-400 ring-2 ring-forest-500/30 text-white'
                        : 'glass-panel-light border-forest-800/60 text-slate-300 hover:text-white'
                    }`}
                  >
                    <span 
                      className="w-4 h-4 rounded-full border border-white/20 flex-shrink-0"
                      style={{ backgroundColor: c.swatch }}
                    />
                    <span className="font-medium truncate">{c.label}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Soil Texture Selection with Ribbon Test Clues */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-xs font-semibold text-slate-300">
                  Soil Texture <span className="text-forest-400 font-normal">(Determined by Finger Feel &amp; Ribbon Test)</span>
                </label>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {[
                  {
                    id: 'Sandy',
                    title: 'Sandy Soil',
                    kannada: 'ಮರಳು ಮಣ್ಣು',
                    desc: 'Gritty, rough. Crumbles immediately; cannot form a pencil ribbon.',
                    badge: 'Fast Drainage'
                  },
                  {
                    id: 'Loamy',
                    title: 'Loamy Soil',
                    kannada: 'ಗೋಡು ಮಣ್ಣು',
                    desc: 'Smooth yet gritty. Forms flexible ribbon (2.5 - 3.5 cm) before breaking.',
                    badge: 'Ideal Balance'
                  },
                  {
                    id: 'Clayey',
                    title: 'Clayey / Black Cotton',
                    kannada: 'ಜೇಡಿ / ಕಪ್ಪು ಮಣ್ಣು',
                    desc: 'Very sticky and plastic when wet. Forms shiny long ribbon (>5 cm). Deep cracks when dry.',
                    badge: 'High Retention'
                  },
                  {
                    id: 'Silty',
                    title: 'Silty Soil',
                    kannada: 'ಹೂಳು ಮಣ್ಣು',
                    desc: 'Silky, flour-like talcum feel when dry; soapy when wet, non-sticky.',
                    badge: 'Crusting Risk'
                  },
                  {
                    id: 'Mixed',
                    title: 'Mixed / Gravelly Loam',
                    kannada: 'ಮಿಶ್ರ ಮಣ್ಣು',
                    desc: 'Variable mix of pebbles, coarse sand, and clay common on rolling Deccan terrain.',
                    badge: 'Moderate'
                  },
                  {
                    id: 'Unknown',
                    title: 'Not Tested / Unknown',
                    kannada: 'ತಿಳಿದಿಲ್ಲ',
                    desc: 'Applies neutral evaluation with explicit reliability penalty.',
                    badge: 'Penalty -15%'
                  }
                ].map(t => (
                  <button
                    key={t.id}
                    type="button"
                    onClick={() => setFormData(prev => ({
                      ...prev,
                      soil_observation: { ...prev.soil_observation, soil_texture: t.id }
                    }))}
                    className={`p-3.5 rounded-2xl text-left border transition-all ${
                      formData.soil_observation.soil_texture === t.id
                        ? 'bg-forest-900 border-forest-400 ring-2 ring-forest-500/30'
                        : 'glass-panel-light border-forest-800/60 hover:bg-forest-900/40'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-bold text-xs text-white">{t.title}</span>
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-forest-950 text-forest-300 font-mono">
                        {t.badge}
                      </span>
                    </div>
                    <div className="text-[11px] text-forest-400 mb-1">{t.kannada}</div>
                    <p className="text-[11px] text-slate-300 leading-snug">{t.desc}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Drainage Characteristics & Soil Depth */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Water Drainage after Rain
                </label>
                <select
                  value={formData.soil_observation.drainage}
                  onChange={e => setFormData(prev => ({
                    ...prev,
                    soil_observation: { ...prev.soil_observation, drainage: e.target.value }
                  }))}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-forest-950/80 border border-forest-700/60 text-white text-xs focus:outline-none focus:border-forest-400"
                >
                  <option value="Water drains quickly">Water drains quickly (within minutes)</option>
                  <option value="Water drains moderately">Water drains moderately (steady infiltration)</option>
                  <option value="Water remains for several hours">Water remains for several hours (pools briefly)</option>
                  <option value="Water remains for one or more days">Water remains for one or more days (waterlogged)</option>
                  <option value="Unknown">Unknown / Not Observed</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Effective Soil Depth
                </label>
                <select
                  value={formData.soil_observation.soil_depth}
                  onChange={e => setFormData(prev => ({
                    ...prev,
                    soil_observation: { ...prev.soil_observation, soil_depth: e.target.value }
                  }))}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-forest-950/80 border border-forest-700/60 text-white text-xs focus:outline-none focus:border-forest-400"
                >
                  <option value="Shallow">Shallow (&lt;25 cm - rock/gravel layer)</option>
                  <option value="Medium">Medium (25 - 75 cm - workable profile)</option>
                  <option value="Deep">Deep (&gt;75 cm - allows deep taproots)</option>
                  <option value="Unknown">Unknown / Not Measured</option>
                </select>
              </div>
            </div>

            {/* Additional Physical Checks Checkboxes */}
            <div className="p-3.5 rounded-2xl bg-forest-950/50 border border-forest-800/60 space-y-2">
              <span className="text-xs font-semibold text-slate-300 block">Additional Observable Constraints</span>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs text-slate-300">
                <label className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.soil_observation.waterlogging_observed}
                    onChange={e => setFormData(prev => ({
                      ...prev,
                      soil_observation: { ...prev.soil_observation, waterlogging_observed: e.target.checked }
                    }))}
                    className="rounded border-forest-700 text-forest-600 focus:ring-forest-500"
                  />
                  <span>Waterlogging</span>
                </label>

                <label className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.soil_observation.presence_of_stones}
                    onChange={e => setFormData(prev => ({
                      ...prev,
                      soil_observation: { ...prev.soil_observation, presence_of_stones: e.target.checked }
                    }))}
                    className="rounded border-forest-700 text-forest-600 focus:ring-forest-500"
                  />
                  <span>Stony Surface</span>
                </label>

                <label className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.soil_observation.rocky_ground}
                    onChange={e => setFormData(prev => ({
                      ...prev,
                      soil_observation: { ...prev.soil_observation, rocky_ground: e.target.checked }
                    }))}
                    className="rounded border-forest-700 text-forest-600 focus:ring-forest-500"
                  />
                  <span>Rocky Outcrops</span>
                </label>

                <label className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.soil_observation.surface_erosion}
                    onChange={e => setFormData(prev => ({
                      ...prev,
                      soil_observation: { ...prev.soil_observation, surface_erosion: e.target.checked }
                    }))}
                    className="rounded border-forest-700 text-forest-600 focus:ring-forest-500"
                  />
                  <span>Erosion Runoff</span>
                </label>
              </div>
            </div>
          </div>
        )}

        {/* STEP 3: Water Availability & Land Profile */}
        {currentStep === 3 && (
          <div className="space-y-6">
            <div className="border-b border-forest-800/60 pb-4">
              <h3 className="text-xl font-bold text-white flex items-center space-x-2">
                <Droplets className="w-5 h-5 text-forest-400" />
                <span>{lang === 'kn' ? 'ಹಂತ ೩: ನೀರಿನ ಲಭ್ಯತೆ ಮತ್ತು ಭೂಮಿಯ ಲಕ್ಷಣ' : 'Step 3: Water Availability & Land Profile'}</span>
              </h3>
              <p className="text-xs text-slate-300 mt-1">
                {lang === 'kn'
                  ? 'ನಿಮ್ಮ ಜಮೀನಿನ ನೀರಾವರಿ ಮೂಲ ಮತ್ತು ಇಳಿಜಾರಿನ ವಿವರಗಳನ್ನು ನೀಡಿ.'
                  : 'Evaluate your water source duration to prevent overcommitting to water-hungry crops.'}
              </p>
            </div>

            {/* Irrigation Sources Grid */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-2">
                Primary Water Source <span className="text-red-400">*</span>
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                {[
                  'Rainfed farming',
                  'Borewell',
                  'Canal irrigation',
                  'Open well',
                  'Farm pond',
                  'Drip irrigation',
                  'Multiple irrigation sources',
                  'Other'
                ].map(src => (
                  <button
                    key={src}
                    type="button"
                    onClick={() => setFormData(prev => ({
                      ...prev,
                      water_availability: { ...prev.water_availability, irrigation_source: src }
                    }))}
                    className={`p-2.5 rounded-xl text-left text-xs border font-medium transition-all ${
                      formData.water_availability.irrigation_source === src
                        ? 'bg-forest-900 border-forest-400 ring-2 ring-forest-500/30 text-white'
                        : 'glass-panel-light border-forest-800/60 text-slate-300 hover:text-white'
                    }`}
                  >
                    {src}
                  </button>
                ))}
              </div>
            </div>

            {/* Water Duration & Drip */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Water Availability Reliability
                </label>
                <select
                  value={formData.water_availability.availability_duration}
                  onChange={e => setFormData(prev => ({
                    ...prev,
                    water_availability: { ...prev.water_availability, availability_duration: e.target.value }
                  }))}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-forest-950/80 border border-forest-700/60 text-white text-xs focus:outline-none focus:border-forest-400"
                >
                  <option value="Throughout season">Throughout season (Assurred Perennial)</option>
                  <option value="Water available during certain months">Water available during certain months (Seasonal)</option>
                  <option value="Limited water availability">Limited water availability (Protective only)</option>
                  <option value="Uncertain availability">Uncertain / Rain-dependent</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Land Slope / Topography
                </label>
                <select
                  value={formData.land_profile.slope_type}
                  onChange={e => setFormData(prev => ({
                    ...prev,
                    land_profile: { ...prev.land_profile, slope_type: e.target.value }
                  }))}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-forest-950/80 border border-forest-700/60 text-white text-xs focus:outline-none focus:border-forest-400"
                >
                  <option value="Flat land">Flat land (Optimal basin cultivation)</option>
                  <option value="Slightly sloping land">Slightly sloping land (Good runoff)</option>
                  <option value="Steep or hilly land">Steep or hilly land (Requires terracing)</option>
                  <option value="Low-lying land">Low-lying land (Water accumulation prone)</option>
                  <option value="Rocky land">Rocky land</option>
                </select>
              </div>
            </div>

            {/* Cultivated Area (Acres) */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Approximate Field Area (Acres)
                </label>
                <input
                  type="number"
                  step="0.5"
                  min="0.25"
                  max="100"
                  value={formData.land_profile.approximate_area_acres}
                  onChange={e => setFormData(prev => ({
                    ...prev,
                    land_profile: { ...prev.land_profile, approximate_area_acres: parseFloat(e.target.value) || 1.0 }
                  }))}
                  className="w-full px-3.5 py-2 rounded-xl bg-forest-950/80 border border-forest-700/60 text-white text-sm focus:outline-none focus:border-forest-400"
                />
              </div>

              <div className="flex items-center space-x-3 pt-6">
                <label className="flex items-center space-x-2 text-xs text-slate-300 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.water_availability.has_drip_facility}
                    onChange={e => setFormData(prev => ({
                      ...prev,
                      water_availability: { ...prev.water_availability, has_drip_facility: e.target.checked }
                    }))}
                    className="rounded border-forest-700 text-forest-600 focus:ring-forest-500"
                  />
                  <span>Equipped with Drip / Micro-Irrigation</span>
                </label>
              </div>
            </div>
          </div>
        )}

        {/* STEP 4: Season Planning & Farming History */}
        {currentStep === 4 && (
          <div className="space-y-6">
            <div className="border-b border-forest-800/60 pb-4">
              <h3 className="text-xl font-bold text-white flex items-center space-x-2">
                <Calendar className="w-5 h-5 text-forest-400" />
                <span>{lang === 'kn' ? 'ಹಂತ ೪: ಕೃಷಿ ಋತು ಮತ್ತು ಹಿಂದಿನ ಬೆಳೆಯ ಇತಿಹಾಸ' : 'Step 4: Season Planning & Farming History'}</span>
              </h3>
              <p className="text-xs text-slate-300 mt-1">
                {lang === 'kn'
                  ? 'ಬೆಳೆ ಪರಿವರ್ತನೆ (Crop Rotation) ಲಾಭಗಳನ್ನು ಗಣನೆಗೆ ತೆಗೆದುಕೊಳ್ಳಲು ಹಿಂದಿನ ಬೆಳೆ ವಿವರಗಳನ್ನು ನೀಡಿ.'
                  : 'Incorporates crop rotation benefits (e.g. legume following cereal) and avoids consecutive mono-cropping.'}
              </p>
            </div>

            {/* Season Selector */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-2">
                Planned Cultivation Season <span className="text-red-400">*</span>
              </label>
              <div className="grid grid-cols-3 gap-3">
                {[
                  { id: 'Kharif', label: 'Kharif (Monsoon)', months: 'June - Oct', kannada: 'ಮುಂಗಾರು' },
                  { id: 'Rabi', label: 'Rabi (Post-Monsoon)', months: 'Oct - Feb', kannada: 'ಹಿಂಗಾರು' },
                  { id: 'Summer', label: 'Summer / Zaid', months: 'Feb - May', kannada: 'ಬೇಸಿಗೆ' }
                ].map(s => (
                  <button
                    key={s.id}
                    type="button"
                    onClick={() => setFormData(prev => ({ ...prev, planned_season: s.id }))}
                    className={`p-3.5 rounded-2xl text-left border transition-all ${
                      formData.planned_season === s.id
                        ? 'bg-forest-900 border-forest-400 ring-2 ring-forest-500/30'
                        : 'glass-panel-light border-forest-800/60 hover:bg-forest-900/40'
                    }`}
                  >
                    <div className="font-bold text-sm text-white">{s.label}</div>
                    <div className="text-xs text-forest-300">{s.kannada}</div>
                    <div className="text-[10px] text-slate-400 font-mono mt-1">{s.months}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Previous Crop & Sowing Month */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Previous Crop Cultivated <span className="text-slate-400 font-normal">(For rotation analysis)</span>
                </label>
                <select
                  value={formData.farming_history.previous_crop}
                  onChange={e => setFormData(prev => ({
                    ...prev,
                    farming_history: { ...prev.farming_history, previous_crop: e.target.value }
                  }))}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-forest-950/80 border border-forest-700/60 text-white text-xs focus:outline-none focus:border-forest-400"
                >
                  <option value="None / Fallow">None / Fallow Field</option>
                  <option value="Green gram">Green gram (Pulse)</option>
                  <option value="Black gram">Black gram (Pulse)</option>
                  <option value="Red gram">Red gram / Pigeonpea</option>
                  <option value="Chickpea">Bengal gram / Chickpea</option>
                  <option value="Maize">Maize</option>
                  <option value="Jowar">Jowar / Sorghum</option>
                  <option value="Ragi">Ragi / Finger Millet</option>
                  <option value="Paddy">Paddy / Rice</option>
                  <option value="Groundnut">Groundnut</option>
                  <option value="Cotton">Cotton</option>
                  <option value="Sugarcane">Sugarcane</option>
                  <option value="Other">Other Crop</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Planned Sowing Month
                </label>
                <select
                  value={formData.planned_sowing_month}
                  onChange={e => setFormData(prev => ({ ...prev, planned_sowing_month: e.target.value }))}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-forest-950/80 border border-forest-700/60 text-white text-xs focus:outline-none focus:border-forest-400"
                >
                  {['June', 'July', 'August', 'September', 'October', 'November', 'December', 'January', 'February', 'March'].map(m => (
                    <option key={m} value={m}>{m}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Farming Objective */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                Primary Farming Objective
              </label>
              <select
                value={formData.farming_objective}
                onChange={e => setFormData(prev => ({ ...prev, farming_objective: e.target.value }))}
                className="w-full px-3.5 py-2.5 rounded-xl bg-forest-950/80 border border-forest-700/60 text-white text-xs focus:outline-none focus:border-forest-400"
              >
                <option value="High Yield & Stability">High Yield &amp; Stability (Food Security)</option>
                <option value="Low Water Consumption">Low Water Consumption (Drought Coping)</option>
                <option value="High Cash Return">High Cash Return / Commercial Profit</option>
                <option value="Soil Health & Legume Rotation">Soil Health &amp; Nitrogen Fixing</option>
              </select>
            </div>
          </div>
        )}

        {/* Wizard Navigation Footer */}
        <div className="flex items-center justify-between pt-4 border-t border-forest-800/60">
          {currentStep > 1 ? (
            <button
              type="button"
              onClick={() => setCurrentStep(prev => prev - 1)}
              className="flex items-center space-x-1.5 px-4 py-2.5 rounded-xl glass-panel-light hover:bg-forest-800/40 text-slate-200 text-xs font-medium transition-all"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back</span>
            </button>
          ) : <div />}

          {currentStep < 4 ? (
            <button
              type="button"
              onClick={() => setCurrentStep(prev => prev + 1)}
              className="flex items-center space-x-1.5 px-6 py-2.5 rounded-xl bg-forest-600 hover:bg-forest-500 text-white text-xs font-semibold shadow-md transition-all hover:scale-[1.01]"
            >
              <span>Next Step</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          ) : (
            <button
              type="submit"
              disabled={isLoading}
              className="flex items-center space-x-2 px-7 py-3 rounded-xl bg-gradient-to-r from-forest-600 to-forest-500 hover:from-forest-500 hover:to-forest-400 text-white text-sm font-bold shadow-lg shadow-forest-900/60 transition-all hover:scale-[1.02] active:scale-[0.98] disabled:opacity-70"
            >
              <Sparkles className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
              <span>{isLoading ? 'Running Agronomic Rule Engine...' : 'Evaluate & Recommend Crops'}</span>
            </button>
          )}
        </div>
      </form>
    </div>
  );
}
