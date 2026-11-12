import { useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Footer } from "./components/Footer";
import { Navbar } from "./components/Navbar";
import { WelcomeAnimation } from "./components/WelcomeAnimation";
import { ThemeProvider } from "./context/ThemeContext";
import { I18nProvider } from "./i18n";
import { AdminPage } from "./pages/AdminPage";
import { ComparePage } from "./pages/ComparePage";
import { HomePage } from "./pages/HomePage";
import { KnowledgePage } from "./pages/KnowledgePage";
import { PrivacyPolicyPage } from "./pages/PrivacyPolicyPage";
import { RecommendPage } from "./pages/RecommendPage";
import { ResultsPage } from "./pages/ResultsPage";
import { SoilHealthPage } from "./pages/SoilHealthPage";
import { TermsPage } from "./pages/TermsPage";

export function AppContent() {
  const [showWelcome, setShowWelcome] = useState<boolean>(() => {
    if (typeof window === "undefined") return false;
    return sessionStorage.getItem("smartkrishi_intro_seen") !== "1";
  });

  const handleFinishWelcome = () => {
    sessionStorage.setItem("smartkrishi_intro_seen", "1");
    setShowWelcome(false);
  };

  return (
    <div className="flex min-h-screen flex-col bg-canvas text-ink">
      {showWelcome && <WelcomeAnimation onComplete={handleFinishWelcome} />}
      <Navbar />
      <main id="main-content" className="flex-1">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/recommend" element={<RecommendPage />} />
          <Route path="/results/:id" element={<ResultsPage />} />
          <Route path="/compare" element={<ComparePage />} />
          <Route path="/soil-health" element={<SoilHealthPage />} />
          <Route path="/knowledge" element={<KnowledgePage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="/privacy-policy" element={<PrivacyPolicyPage />} />
          <Route path="/terms" element={<TermsPage />} />
          <Route path="*" element={<HomePage />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <I18nProvider>
        <BrowserRouter>
          <AppContent />
        </BrowserRouter>
      </I18nProvider>
    </ThemeProvider>
  );
}
