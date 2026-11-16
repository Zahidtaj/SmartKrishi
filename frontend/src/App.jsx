import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import HeroIntro from './components/HeroIntro';
import KarnatakaMap from './components/KarnatakaMap';
import RecommendationWizard from './components/RecommendationWizard';
import RecommendationResults from './components/RecommendationResults';
import ComparisonModal from './components/ComparisonModal';
import WeatherAdvisoryDashboard from './components/WeatherAdvisoryDashboard';
import SoilIdentificationGuide from './components/SoilIdentificationGuide';
import KnowledgeBase from './components/KnowledgeBase';
import Footer from './components/Footer';

export default function App() {
  const [activeTab, setActiveTab] = useState('wizard');
  const [lang, setLang] = useState('en'); // 'en' or 'kn'

  // Master Data Loaded from Backend
  const [districts, setDistricts] = useState([]);
  const [zones, setZones] = useState([]);
  const [selectedDistrict, setSelectedDistrict] = useState('Chitradurga');

  // Recommendation State
  const [recommendationResult, setRecommendationResult] = useState(null);
  const [isLoadingRecs, setIsLoadingRecs] = useState(false);

  // Comparison State
  const [selectedCropsForCompare, setSelectedCropsForCompare] = useState([]);
  const [isCompareModalOpen, setIsCompareModalOpen] = useState(false);

  // Initial Data Fetch
  useEffect(() => {
    Promise.all([
      fetch('/api/locations/districts').then(r => r.json()),
      fetch('/api/locations/zones').then(r => r.json())
    ])
      .then(([distData, zoneData]) => {
        if (Array.isArray(distData)) setDistricts(distData);
        if (Array.isArray(zoneData)) setZones(zoneData);
      })
      .catch(err => console.error("Initial data load error:", err));
  }, []);

  // Wizard Submit Handler
  const handleWizardSubmit = async (formData) => {
    setIsLoadingRecs(true);
    try {
      const response = await fetch('/api/recommendations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      if (response.ok) {
        const data = await response.json();
        setRecommendationResult(data);
        // Scroll to top of results smoothly
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else {
        const err = await response.json();
        alert(`Evaluation error: ${err.detail || 'Could not generate recommendations'}`);
      }
    } catch (error) {
      console.error("Evaluation request error:", error);
      alert("Failed to connect to recommendation server. Ensure backend is running.");
    } finally {
      setIsLoadingRecs(false);
    }
  };

  // Select District from Map Handler
  const handleSelectDistrictFromMap = (distName) => {
    setSelectedDistrict(distName);
    setRecommendationResult(null);
    setActiveTab('wizard');
    window.scrollTo({ top: 400, behavior: 'smooth' });
  };

  // Toggle Compare
  const handleToggleCompare = (cropId) => {
    setSelectedCropsForCompare(prev => {
      if (prev.includes(cropId)) {
        return prev.filter(id => id !== cropId);
      }
      if (prev.length >= 3) {
        alert("You can compare up to 3 crops simultaneously. Remove one to add another.");
        return prev;
      }
      return [...prev, cropId];
    });
  };

  const handleRemoveCompareCrop = (cropId) => {
    setSelectedCropsForCompare(prev => prev.filter(id => id !== cropId));
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#071711] text-slate-100 font-sans selection:bg-forest-800 selection:text-forest-100">
      {/* Top Navigation */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        lang={lang}
        setLang={setLang}
        selectedCropsCount={selectedCropsForCompare.length}
        onOpenComparison={() => setIsCompareModalOpen(true)}
      />

      {/* Main Tab Routing */}
      <main className="flex-1">
        {activeTab === 'wizard' && (
          <div>
            {!recommendationResult ? (
              <>
                <HeroIntro
                  lang={lang}
                  onStartWizard={() => {
                    const el = document.getElementById('wizard-section');
                    if (el) el.scrollIntoView({ behavior: 'smooth' });
                  }}
                  onExploreMap={() => setActiveTab('map')}
                />
                <div id="wizard-section">
                  <RecommendationWizard
                    districts={districts}
                    zones={zones}
                    preselectedDistrict={selectedDistrict}
                    onSubmitWizard={handleWizardSubmit}
                    isLoading={isLoadingRecs}
                    lang={lang}
                  />
                </div>
              </>
            ) : (
              <RecommendationResults
                result={recommendationResult}
                onReset={() => setRecommendationResult(null)}
                selectedCropsForCompare={selectedCropsForCompare}
                onToggleCompare={handleToggleCompare}
                onOpenComparison={() => setIsCompareModalOpen(true)}
                lang={lang}
              />
            )}
          </div>
        )}

        {activeTab === 'map' && (
          <KarnatakaMap
            zones={zones}
            districts={districts}
            onSelectDistrictForWizard={handleSelectDistrictFromMap}
            lang={lang}
          />
        )}

        {activeTab === 'weather' && (
          <WeatherAdvisoryDashboard
            districts={districts}
            selectedDistrict={selectedDistrict}
            lang={lang}
          />
        )}

        {activeTab === 'soil-guide' && (
          <SoilIdentificationGuide lang={lang} />
        )}

        {activeTab === 'knowledge' && (
          <KnowledgeBase lang={lang} />
        )}
      </main>

      {/* Comparison Drawer / Modal */}
      <ComparisonModal
        isOpen={isCompareModalOpen}
        onClose={() => setIsCompareModalOpen(false)}
        cropIds={selectedCropsForCompare}
        onRemoveCrop={handleRemoveCompareCrop}
        lang={lang}
      />

      {/* Footer */}
      <Footer lang={lang} />
    </div>
  );
}
