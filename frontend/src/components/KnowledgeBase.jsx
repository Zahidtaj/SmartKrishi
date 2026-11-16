import React, { useState, useEffect } from 'react';
import { BookOpen, Calendar, MapPin, ChevronRight, X, ShieldCheck } from 'lucide-react';

export default function KnowledgeBase({ lang }) {
  const [articles, setArticles] = useState([]);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('ALL');

  useEffect(() => {
    fetch('/api/knowledge')
      .then(res => res.json())
      .then(data => setArticles(data))
      .catch(err => console.error("Knowledge fetch error:", err));
  }, []);

  const categories = ['ALL', 'Soil Observation', 'Water Management', 'Crop Planning', 'Agricultural Advisory'];

  const filteredArticles = selectedCategory === 'ALL'
    ? articles
    : articles.filter(a => a.category === selectedCategory);

  return (
    <div className="py-8 max-w-6xl mx-auto px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div>
        <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-forest-900/60 border border-forest-500/30 text-forest-300 text-xs font-semibold mb-2">
          <BookOpen className="w-3.5 h-3.5 text-forest-400" />
          <span>Verified Agronomic Library</span>
        </div>
        <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          {lang === 'kn' ? 'ಕೃಷಿ ಜ್ಞಾನ ಭಂಡಾರ' : 'Agricultural Knowledge Repository'}
        </h2>
        <p className="text-xs sm:text-sm text-slate-300 max-w-2xl mt-1">
          Evidence-based cultivation guides, in-situ moisture conservation techniques, and crop rotation strategies from UAS Bengaluru, UAS Dharwad &amp; ICAR.
        </p>
      </div>

      {/* Category Pills */}
      <div className="flex flex-wrap gap-2">
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-medium transition-all ${
              selectedCategory === cat
                ? 'bg-forest-600 text-white font-semibold shadow-md'
                : 'glass-panel-light text-slate-300 hover:text-white'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Articles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredArticles.map(art => (
          <div
            key={art.id}
            onClick={() => setSelectedArticle(art)}
            className="glass-panel-interactive p-6 rounded-3xl cursor-pointer flex flex-col justify-between space-y-4"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between text-[11px] text-forest-300">
                <span className="px-2 py-0.5 rounded-md bg-forest-950 font-medium">
                  {art.category}
                </span>
                <span className="text-slate-400">{art.publication_date}</span>
              </div>

              <h3 className="text-base font-bold text-white leading-snug group-hover:text-forest-300 transition-colors">
                {art.title}
              </h3>
              {art.kannada_title && (
                <div className="text-xs text-forest-300/80 font-medium">{art.kannada_title}</div>
              )}

              <p className="text-xs text-slate-300 line-clamp-2 leading-relaxed">
                {art.summary}
              </p>
            </div>

            <div className="flex items-center justify-between text-xs pt-2 border-t border-forest-800/40 text-slate-400">
              <span className="truncate max-w-[240px]" title={art.source}>Source: {art.source}</span>
              <span className="flex items-center text-forest-400 font-semibold space-x-1">
                <span>Read Full</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Article Detail Modal */}
      {selectedArticle && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm overflow-y-auto">
          <div className="glass-panel w-full max-w-3xl rounded-3xl p-6 sm:p-8 space-y-5 max-h-[85vh] overflow-y-auto border-forest-500/40 relative">
            <div className="flex items-start justify-between border-b border-forest-800/60 pb-4">
              <div>
                <span className="text-xs font-semibold px-2 py-0.5 rounded bg-forest-950 text-forest-300">
                  {selectedArticle.category}
                </span>
                <h3 className="text-xl font-bold text-white mt-2 leading-snug">{selectedArticle.title}</h3>
                {selectedArticle.kannada_title && (
                  <div className="text-sm text-forest-300 mt-1">{selectedArticle.kannada_title}</div>
                )}
                <div className="text-[11px] text-slate-400 mt-1">
                  Published: {selectedArticle.publication_date} &bull; Applicability: {selectedArticle.geographic_applicability}
                </div>
              </div>

              <button
                onClick={() => setSelectedArticle(null)}
                className="w-8 h-8 rounded-full glass-panel-light flex items-center justify-center text-slate-400 hover:text-white"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Article Markdown Body */}
            <div className="text-xs sm:text-sm text-slate-200 leading-relaxed space-y-4 whitespace-pre-line font-sans">
              {selectedArticle.content}
            </div>

            {/* Footer Citation */}
            <div className="p-3 rounded-xl bg-forest-950/70 border border-forest-800/60 text-[11px] text-slate-400 flex items-center space-x-2">
              <ShieldCheck className="w-4 h-4 text-forest-400 flex-shrink-0" />
              <span>Verified Scientific Source: {selectedArticle.source}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
