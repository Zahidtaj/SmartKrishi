import React, { useState, useEffect } from 'react';
import { 
  CloudSun, Droplets, Wind, AlertTriangle, ShieldCheck, 
  Calendar, RefreshCw, MapPin, CloudRain, CheckCircle2 
} from 'lucide-react';

export default function WeatherAdvisoryDashboard({ districts, selectedDistrict, lang }) {
  const [district, setDistrict] = useState(selectedDistrict || 'Chitradurga');
  const [weatherData, setWeatherData] = useState(null);
  const [advisories, setAdvisories] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchWeatherAndAdvisories = async (distName) => {
    setIsLoading(true);
    try {
      const [wRes, aRes] = await Promise.all([
        fetch(`/api/weather/${distName}`),
        fetch(`/api/advisories/${distName}`)
      ]);
      if (wRes.ok) {
        const wData = await wRes.json();
        setWeatherData(wData);
      }
      if (aRes.ok) {
        const aData = await aRes.json();
        setAdvisories(aData);
      }
    } catch (err) {
      console.error("Weather/Advisories fetch error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchWeatherAndAdvisories(district);
  }, [district]);

  return (
    <div className="py-8 max-w-6xl mx-auto px-4 sm:px-6 space-y-8">
      {/* Top Header & District Switcher */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-forest-900/60 border border-forest-500/30 text-forest-300 text-xs font-semibold mb-2">
            <CloudSun className="w-3.5 h-3.5 text-cyan-400" />
            <span>Meteorological &amp; Agricultural Advisory</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            {lang === 'kn' ? 'ಹವಾಮಾನ ಮತ್ತು ಕೃಷಿ ಮುನ್ನೆಚ್ಚರಿಕೆಗಳು' : 'Weather Intelligence & Farm Advisories'}
          </h2>
          <p className="text-xs sm:text-sm text-slate-300 mt-1">
            Real-time atmospheric telemetry via Open-Meteo &amp; official IMD district agromet advisories.
          </p>
        </div>

        {/* District Selector Dropdown */}
        <div className="flex items-center space-x-2">
          <select
            value={district}
            onChange={(e) => setDistrict(e.target.value)}
            className="px-4 py-2.5 rounded-xl bg-forest-950/80 border border-forest-700/60 text-white text-xs font-semibold focus:outline-none focus:border-forest-400"
          >
            {districts.map((d) => (
              <option key={d.name} value={d.name}>{d.name}</option>
            ))}
          </select>

          <button
            onClick={() => fetchWeatherAndAdvisories(district)}
            className="p-2.5 rounded-xl glass-panel-light hover:bg-forest-800/40 text-slate-300 hover:text-white transition-colors"
            title="Refresh weather"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {weatherData && (
        <div className="space-y-6">
          {/* Main Current Weather Card */}
          <div className="glass-panel rounded-3xl p-6 sm:p-8 relative overflow-hidden border-forest-500/30">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div>
                <div className="flex items-center space-x-2 text-xs text-forest-300 font-mono mb-1">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                  <span>{weatherData.is_live_data ? 'Live Meteorological Feed' : 'Climatological Normal Baseline'}</span>
                  <span>&bull;</span>
                  <span>{weatherData.retrieval_timestamp}</span>
                </div>
                <h3 className="text-3xl font-extrabold text-white flex items-center space-x-3">
                  <span>{weatherData.location}</span>
                  <span className="text-2xl text-slate-400 font-normal">| {weatherData.condition}</span>
                </h3>
                <p className="text-xs text-slate-400 mt-1">
                  Source: <strong className="text-slate-200">{weatherData.source}</strong>
                </p>
              </div>

              {/* Big Temperature Display */}
              <div className="text-right flex items-baseline space-x-2 self-start md:self-auto">
                <span className="text-5xl font-extrabold font-mono text-white">
                  {weatherData.current_temperature_c}
                </span>
                <span className="text-2xl font-light text-forest-300">°C</span>
              </div>
            </div>

            {/* Weather Metrics Strip */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 pt-6 border-t border-forest-800/60 text-xs">
              <div className="p-3 rounded-xl bg-forest-950/60 border border-forest-800/50">
                <div className="flex items-center space-x-1.5 text-slate-400 mb-1">
                  <Droplets className="w-4 h-4 text-cyan-400" />
                  <span>Relative Humidity</span>
                </div>
                <div className="text-base font-mono font-bold text-white">
                  {weatherData.relative_humidity_pct}%
                </div>
              </div>

              <div className="p-3 rounded-xl bg-forest-950/60 border border-forest-800/50">
                <div className="flex items-center space-x-1.5 text-slate-400 mb-1">
                  <Wind className="w-4 h-4 text-emerald-400" />
                  <span>Wind Speed</span>
                </div>
                <div className="text-base font-mono font-bold text-white">
                  {weatherData.wind_speed_kmh} km/h
                </div>
              </div>

              <div className="p-3 rounded-xl bg-forest-950/60 border border-forest-800/50">
                <div className="flex items-center space-x-1.5 text-slate-400 mb-1">
                  <CloudRain className="w-4 h-4 text-blue-400" />
                  <span>Recent Rain</span>
                </div>
                <div className="text-base font-mono font-bold text-white">
                  {weatherData.recent_precipitation_mm} mm
                </div>
              </div>

              <div className="p-3 rounded-xl bg-forest-950/60 border border-forest-800/50">
                <div className="flex items-center space-x-1.5 text-slate-400 mb-1">
                  <Calendar className="w-4 h-4 text-amber-400" />
                  <span>Dry Days Expected</span>
                </div>
                <div className="text-base font-mono font-bold text-amber-300">
                  {weatherData.consecutive_dry_days_forecast || 0} / 7 days
                </div>
              </div>
            </div>
          </div>

          {/* 7-Day Forecast Strip */}
          {weatherData.forecast_7_day?.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-slate-400 mb-3 uppercase tracking-wider">
                7-Day Precipitation &amp; Temperature Outlook
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-2.5">
                {weatherData.forecast_7_day.map((day, idx) => (
                  <div key={idx} className="glass-panel-light p-3 rounded-2xl text-center space-y-1.5 border border-forest-800/60">
                    <div className="text-[11px] text-slate-400 font-medium">
                      {new Date(day.date).toLocaleDateString('en-US', { weekday: 'short', month: 'numeric', day: 'numeric' })}
                    </div>
                    <div className="text-sm font-mono font-bold text-white">
                      {day.temp_max_c}° / <span className="text-slate-400 text-xs">{day.temp_min_c}°</span>
                    </div>
                    <div className="text-[10px] text-cyan-400 font-medium">
                      {day.expected_rainfall_mm} mm rain
                    </div>
                    <div className="text-[9px] text-slate-400">
                      {day.rain_probability_pct}% prob.
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Agricultural Advisories Feed */}
          <div className="space-y-4">
            <h3 className="text-lg font-bold text-white flex items-center space-x-2">
              <ShieldCheck className="w-5 h-5 text-forest-400" />
              <span>Active Agricultural Advisories ({advisories.length})</span>
            </h3>

            {advisories.length === 0 ? (
              <div className="glass-panel p-6 rounded-2xl text-center text-xs text-slate-400">
                No acute weather alerts for {district} at this time. Standard seasonal practices apply.
              </div>
            ) : (
              <div className="space-y-3">
                {advisories.map((adv) => {
                  const isWarning = adv.severity === 'Warning' || adv.severity === 'Alert';
                  return (
                    <div 
                      key={adv.id}
                      className={`glass-panel p-5 rounded-2xl border-l-4 space-y-2 ${
                        isWarning ? 'border-l-amber-500 bg-amber-950/20' : 'border-l-forest-500 bg-forest-950/40'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                            isWarning ? 'bg-amber-900/60 text-amber-200' : 'bg-forest-900/60 text-forest-200'
                          }`}>
                            {adv.advisory_type}
                          </span>
                          <h4 className="font-bold text-white text-sm">{adv.title}</h4>
                        </div>
                        <span className="text-[11px] text-slate-400">Valid: {adv.valid_until}</span>
                      </div>

                      {adv.kannada_title && (
                        <div className="text-xs text-forest-300 font-medium">{adv.kannada_title}</div>
                      )}

                      <p className="text-xs text-slate-200 leading-relaxed">{adv.message}</p>
                      {adv.kannada_message && (
                        <p className="text-xs text-forest-200/90 leading-relaxed font-sans">{adv.kannada_message}</p>
                      )}

                      <div className="text-[10px] text-slate-400 font-mono pt-1">
                        Source: {adv.source}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
