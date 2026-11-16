import React from 'react';
import { Sprout, Compass, ShieldCheck, ArrowRight, Eye, Droplet, Sun, CheckCircle2 } from 'lucide-react';

export default function HeroIntro({ lang, onStartWizard, onExploreMap }) {
  return (
    <section className="relative overflow-hidden py-12 lg:py-16">
      {/* Background Ambient Glows (Forest and Amber Clay, NOT Purple) */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-forest-600/15 rounded-full blur-[120px] pointer-events-none animate-glow" />
      <div className="absolute bottom-0 right-10 w-80 h-80 bg-clay-600/10 rounded-full blur-[100px] pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center max-w-3xl mx-auto space-y-6">
          {/* Eyebrow Pill */}
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-forest-900/60 border border-forest-500/30 text-forest-300 text-xs font-semibold backdrop-blur-md shadow-inner">
            <span className="w-2 h-2 rounded-full bg-forest-400 animate-pulse" />
            <span>VTU Community Project &bull; Karnataka Agriculture</span>
          </div>

          {/* Main Title */}
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white tracking-tight leading-tight">
            {lang === 'kn' ? (
              <>
                ಲ್ಯಾಬ್ ಪರೀಕ್ಷೆಗಳಿಲ್ಲದೆ <span className="text-forest-400 underline decoration-forest-500/50">ವೀಕ್ಷಣೆಯ ಆಧಾರದ ಮೇಲೆ</span> ವೈಜ್ಞಾನಿಕ ಬೆಳೆ ಸಲಹೆ
              </>
            ) : (
              <>
                Crop Recommendations Grounded in <span className="text-transparent bg-clip-text bg-gradient-to-r from-forest-300 to-forest-500">Observable Land Reality</span>
              </>
            )}
          </h1>

          {/* Subtitle */}
          <p className="text-base sm:text-lg text-slate-300 font-normal leading-relaxed">
            {lang === 'kn' ? (
              'ಕರ್ನಾಟಕದ ಸಣ್ಣ ರೈತರಿಗೆ ಮಣ್ಣಿನ NPK ಅಥವಾ pH ಪರೀಕ್ಷೆಯ ಅಗತ್ಯವಿಲ್ಲದೆ, ಮಣ್ಣಿನ ಬಣ್ಣ, ವಿನ್ಯಾಸ, ನೀರು ಇಂಗುವಿಕೆ, ಸ್ಥಳೀಯ ಹವಾಮಾನ ಮತ್ತು ಕೃಷಿ ವಲಯಗಳ ಆಧಾರದ ಮೇಲೆ ನಿಖರ ಬೆಳೆ ಶಿಫಾರಸು.'
            ) : (
              'Empowering Karnataka farmers who lack laboratory soil-testing facilities. We replace artificial NPK assumptions with observable soil texture, drainage behavior, historical weather normals, and verified regional agronomy.'
            )}
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
            <button
              onClick={onStartWizard}
              className="w-full sm:w-auto flex items-center justify-center space-x-2.5 px-6 py-3.5 rounded-xl bg-forest-600 hover:bg-forest-500 text-white font-semibold text-sm shadow-lg shadow-forest-900/50 hover:shadow-forest-600/30 transition-all hover:scale-[1.02] active:scale-[0.98]"
            >
              <Sprout className="w-4 h-4" />
              <span>{lang === 'kn' ? 'ಬೆಳೆ ಶಿಫಾರಸು ಪ್ರಾರಂಭಿಸಿ' : 'Start Crop Evaluation'}</span>
              <ArrowRight className="w-4 h-4 ml-1" />
            </button>

            <button
              onClick={onExploreMap}
              className="w-full sm:w-auto flex items-center justify-center space-x-2 px-5 py-3.5 rounded-xl glass-panel-light hover:bg-forest-800/40 text-slate-200 hover:text-white text-sm font-medium transition-all"
            >
              <Compass className="w-4 h-4 text-forest-400" />
              <span>{lang === 'kn' ? 'ಕರ್ನಾಟಕ ಕೃಷಿ ವಲಯಗಳು' : 'Explore 10 Agro Zones'}</span>
            </button>
          </div>

          {/* Zero Lab NPK Assurance Strip */}
          <div className="pt-4 flex flex-wrap items-center justify-center gap-y-2 gap-x-6 text-xs text-slate-400">
            <span className="flex items-center space-x-1.5 text-forest-300 font-medium">
              <CheckCircle2 className="w-4 h-4 text-forest-400" />
              <span>Zero Lab NPK / pH Needed</span>
            </span>
            <span className="flex items-center space-x-1.5 text-forest-300 font-medium">
              <CheckCircle2 className="w-4 h-4 text-forest-400" />
              <span>UAS Bengaluru &amp; Dharwad PoP</span>
            </span>
            <span className="flex items-center space-x-1.5 text-forest-300 font-medium">
              <CheckCircle2 className="w-4 h-4 text-forest-400" />
              <span>No Fabricated Data</span>
            </span>
          </div>
        </div>

        {/* 4 Feature Value Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-12">
          <div className="glass-panel p-5 rounded-2xl hover:border-forest-500/30 transition-all">
            <div className="w-10 h-10 rounded-xl bg-forest-900/80 border border-forest-600/30 flex items-center justify-center text-forest-400 mb-3">
              <Eye className="w-5 h-5" />
            </div>
            <h3 className="text-white font-semibold text-sm mb-1">
              {lang === 'kn' ? 'ಸ್ಪರ್ಶ ಮತ್ತು ವೀಕ್ಷಣೆ' : 'Farmer Observations'}
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              {lang === 'kn'
                ? 'ಮಣ್ಣಿನ ಬಣ್ಣ, ಬೆರಳಿನ ರಿಬ್ಬನ್ ಪರೀಕ್ಷೆ, ನೀರು ಇಂಗುವಿಕೆ ಮತ್ತು ಆಳದ ಆಧಾರ.'
                : 'Identifies soil texture through finger feel, ribbon length, drainage speed, and profile depth.'}
            </p>
          </div>

          <div className="glass-panel p-5 rounded-2xl hover:border-forest-500/30 transition-all">
            <div className="w-10 h-10 rounded-xl bg-forest-900/80 border border-forest-600/30 flex items-center justify-center text-forest-400 mb-3">
              <Compass className="w-5 h-5" />
            </div>
            <h3 className="text-white font-semibold text-sm mb-1">
              {lang === 'kn' ? '10 ಕೃಷಿ-ಹವಾಮಾನ ವಲಯಗಳು' : 'Karnataka Agro Zones'}
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              {lang === 'kn'
                ? 'ಕರ್ನಾಟಕದ 31 ಜಿಲ್ಲೆಗಳು ಮತ್ತು ತಾಲೂಕುಗಳ ಅಧಿಕೃತ ಕೃಷಿ ವಲಯ ನಕ್ಷೆ.'
                : 'Authoritative mapping across all 31 districts from Northern Dry to Coastal wetlands.'}
            </p>
          </div>

          <div className="glass-panel p-5 rounded-2xl hover:border-forest-500/30 transition-all">
            <div className="w-10 h-10 rounded-xl bg-forest-900/80 border border-forest-600/30 flex items-center justify-center text-forest-400 mb-3">
              <Droplet className="w-5 h-5" />
            </div>
            <h3 className="text-white font-semibold text-sm mb-1">
              {lang === 'kn' ? 'ನೀರು ಮತ್ತು ಹವಾಮಾನ ಬುದ್ಧಿಮತ್ತೆ' : 'Weather & Water Balance'}
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              {lang === 'kn'
                ? 'IMD 30 ವರ್ಷಗಳ ವಾಡಿಕೆ ಮಳೆ, ಮುನ್ಸೂಚನೆ ಮತ್ತು ಒಣ ಹವೆ ಎಚ್ಚರಿಕೆಗಳು.'
                : 'Compares crop water requirements with rainfall normals, irrigation duration, and dry spell forecasts.'}
            </p>
          </div>

          <div className="glass-panel p-5 rounded-2xl hover:border-forest-500/30 transition-all">
            <div className="w-10 h-10 rounded-xl bg-forest-900/80 border border-forest-600/30 flex items-center justify-center text-forest-400 mb-3">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <h3 className="text-white font-semibold text-sm mb-1">
              {lang === 'kn' ? 'ಕಠಿಣ ಕೃಷಿ ನಿಯಮಗಳು' : 'Hard Agricultural Rules'}
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              {lang === 'kn'
                ? 'ನೀರು ನಿಲ್ಲುವ ಜಾಗದಲ್ಲಿ ಕಡಲೆಕಾಯಿ ಅಥವಾ ಒಣ ವಲಯದಲ್ಲಿ ಭತ್ತ ಬೆಳೆಯುವುದನ್ನು ನಿರ್ಬಂಧಿಸುತ್ತದೆ.'
                : 'Prevents catastrophic misplanting (e.g. groundnut in waterlogged clay or rainfed sugarcane).'}
            </p>
          </div>
        </div>

        {/* Numeric Verified Metrics Ribbon */}
        <div className="mt-8 p-4 rounded-xl glass-panel-light flex flex-wrap items-center justify-around gap-4 text-center">
          <div>
            <div className="text-xl sm:text-2xl font-mono font-bold text-forest-300">10</div>
            <div className="text-[11px] text-slate-400 font-medium">Agro-Climatic Zones</div>
          </div>
          <div className="w-px h-8 bg-forest-800 hidden sm:block" />
          <div>
            <div className="text-xl sm:text-2xl font-mono font-bold text-forest-300">31</div>
            <div className="text-[11px] text-slate-400 font-medium">Karnataka Districts</div>
          </div>
          <div className="w-px h-8 bg-forest-800 hidden sm:block" />
          <div>
            <div className="text-xl sm:text-2xl font-mono font-bold text-clay-400">16</div>
            <div className="text-[11px] text-slate-400 font-medium">Verified Field Crops</div>
          </div>
          <div className="w-px h-8 bg-forest-800 hidden sm:block" />
          <div>
            <div className="text-xl sm:text-2xl font-mono font-bold text-emerald-400">0</div>
            <div className="text-[11px] text-slate-400 font-medium">Required Lab Tests</div>
          </div>
        </div>
      </div>
    </section>
  );
}
