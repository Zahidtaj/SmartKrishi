import React from 'react';
import { Sprout, MapPin, Scale, CloudSun, BookOpen, Layers, Globe } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, lang, setLang, selectedCropsCount, onOpenComparison }) {
  const navItems = [
    { id: 'wizard', label: lang === 'kn' ? 'ಬೆಳೆ ಸಲಹೆ' : 'Crop Advisor', icon: Sprout },
    { id: 'map', label: lang === 'kn' ? 'ಕರ್ನಾಟಕ ನಕ್ಷೆ' : 'Agro Zones Map', icon: MapPin },
    { id: 'weather', label: lang === 'kn' ? 'ಹವಾಮಾನ ಸಲಹೆ' : 'Weather & Advisories', icon: CloudSun },
    { id: 'soil-guide', label: lang === 'kn' ? 'ಮಣ್ಣಿನ ಮಾರ್ಗದರ್ಶಿ' : 'Soil Guide', icon: Layers },
    { id: 'knowledge', label: lang === 'kn' ? 'ಕೃಷಿ ಮಾಹಿತಿ' : 'Knowledge Base', icon: BookOpen },
  ];

  return (
    <header className="sticky top-0 z-50 w-full glass-panel border-b border-forest-500/20 bg-forest-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Project Title */}
          <div 
            className="flex items-center space-x-3 cursor-pointer group"
            onClick={() => setActiveTab('wizard')}
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-forest-500 to-forest-700 flex items-center justify-center text-white shadow-lg shadow-forest-900/40 group-hover:scale-105 transition-transform">
              <Sprout className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-lg tracking-tight text-white font-sans">
                  Smart<span className="text-forest-400">Krishi</span>
                </span>
                <span className="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded-full bg-forest-900/80 border border-forest-500/30 text-forest-300 font-mono">
                  VTU Project
                </span>
              </div>
              <p className="text-xs text-forest-300/80 hidden sm:block">
                {lang === 'kn' ? 'ವೀಕ್ಷಣೆ ಆಧಾರಿತ ಬೆಳೆ ಶಿಫಾರಸು ವ್ಯವಸ್ಥೆ' : 'Observation-Based Agricultural Decision Support'}
              </p>
            </div>
          </div>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center space-x-1 lg:space-x-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-xs lg:text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-forest-600/30 text-white border border-forest-400/40 shadow-sm'
                      : 'text-slate-300 hover:text-white hover:bg-forest-900/40'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-forest-400' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Right Side: Compare Trigger & Bilingual Toggle */}
          <div className="flex items-center space-x-2 sm:space-x-3">
            {/* Compare Drawer Button */}
            <button
              onClick={onOpenComparison}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
                selectedCropsCount > 0
                  ? 'bg-clay-600/30 border-clay-400 text-clay-200 animate-pulse'
                  : 'bg-forest-900/50 border-forest-700/40 text-slate-300 hover:text-white'
              }`}
            >
              <Scale className="w-3.5 h-3.5 text-clay-400" />
              <span>{lang === 'kn' ? 'ಹೋಲಿಕೆ' : 'Compare'}</span>
              {selectedCropsCount > 0 && (
                <span className="w-4 h-4 rounded-full bg-clay-500 text-white text-[10px] flex items-center justify-center font-bold">
                  {selectedCropsCount}
                </span>
              )}
            </button>

            {/* Language Switcher */}
            <button
              onClick={() => setLang(lang === 'en' ? 'kn' : 'en')}
              className="flex items-center space-x-1 px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-forest-900/60 border border-forest-700/50 text-forest-200 hover:bg-forest-800/60 transition-colors"
              title="Toggle English / Kannada"
            >
              <Globe className="w-3.5 h-3.5 text-forest-400" />
              <span>{lang === 'en' ? 'ಕನ್ನಡ' : 'English'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Secondary Navigation Row */}
      <div className="flex md:hidden overflow-x-auto py-2 px-4 space-x-2 border-t border-forest-800/40 bg-forest-950/90 scrollbar-none">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex items-center space-x-1.5 px-2.5 py-1 rounded-md text-xs whitespace-nowrap font-medium transition-all ${
                isActive
                  ? 'bg-forest-600/40 text-white border border-forest-400/30'
                  : 'text-slate-300 bg-forest-900/40'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>
    </header>
  );
}
