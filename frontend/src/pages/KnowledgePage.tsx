import { useEffect, useState } from "react";
import { ArrowLeft, BookOpen, ExternalLink, Search } from "lucide-react";
import { apiClient } from "../api/client";
import { ErrorAlert } from "../components/ErrorAlert";
import { useI18n } from "../i18n";
import type { KnowledgeArticleDetail, KnowledgeArticleSummary } from "../types";

const CATEGORIES = [
  { id: "all", labelEn: "All Categories", labelKn: "ಎಲ್ಲಾ ವಿಭಾಗಗಳು" },
  { id: "cultivation", labelEn: "Crop Cultivation", labelKn: "ಬೆಳೆ ಬೇಸಾಯ" },
  { id: "soil", labelEn: "Soil Management", labelKn: "ಮಣ್ಣು ನಿರ್ವಹಣೆ" },
  { id: "water", labelEn: "Water Conservation", labelKn: "ಜಲ ಸಂರಕ್ಷಣೆ" },
  { id: "seasons", labelEn: "Seasons", labelKn: "ಹಂಗಾಮುಗಳು" },
  { id: "sustainability", labelEn: "Sustainable Practices", labelKn: "ಸುಸ್ಥಿರ ಕೃಷಿ" },
  { id: "terminology", labelEn: "Terminology", labelKn: "ಪದಕೋಶ" },
  { id: "government", labelEn: "Official Resources", labelKn: "ಅಧಿಕೃತ ಸಂಪನ್ಮೂಲಗಳು" },
];

export function KnowledgePage() {
  const { lang, t } = useI18n();
  const [category, setCategory] = useState("all");
  const [search, setSearch] = useState("");
  const [articles, setArticles] = useState<KnowledgeArticleSummary[]>([]);
  const [activeArticle, setActiveArticle] = useState<KnowledgeArticleDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    apiClient
      .getKnowledgeArticles(category, search)
      .then(setArticles)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load articles."))
      .finally(() => setLoading(false));
  }, [category, search]);

  const openArticle = async (id: number) => {
    setError(null);
    try {
      const detail = await apiClient.getKnowledgeArticle(id);
      setActiveArticle(detail);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load article.");
    }
  };

  if (activeArticle) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-10 sm:px-6 lg:px-8 space-y-6">
        <button
          type="button"
          onClick={() => setActiveArticle(null)}
          className="sk-btn-secondary text-sm"
        >
          <ArrowLeft className="h-4 w-4" aria-hidden="true" />
          <span>{t.knowledge.backToLibrary}</span>
        </button>

        <article className="sk-surface-card rounded-xl p-6 sm:p-8 space-y-5">
          <span className="inline-block rounded border border-accent/35 bg-accent/10 px-2.5 py-0.5 text-xs font-medium text-accent uppercase">
            {activeArticle.category}
          </span>
          <h1 className="text-2xl font-semibold text-ink sm:text-3xl">
            {lang === "kn" ? activeArticle.title_kn : activeArticle.title_en}
          </h1>
          <p className="text-base text-secondary leading-relaxed">
            {lang === "kn" ? activeArticle.summary_kn : activeArticle.summary_en}
          </p>
          <div className="border-t border-ink/10 pt-5 space-y-4 text-sm leading-relaxed text-ink/90 whitespace-pre-line max-w-[70ch]">
            {lang === "kn" ? activeArticle.content_kn : activeArticle.content_en}
          </div>
          <div className="border-t border-ink/10 pt-4 text-xs text-muted flex flex-wrap items-center gap-2">
            <span>
              {t.knowledge.sourceLabel}: {activeArticle.source_name}
            </span>
            {activeArticle.source_url && (
              <a
                href={activeArticle.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-accent hover:underline"
              >
                <span>Open official portal</span>
                <ExternalLink className="h-3.5 w-3.5" aria-hidden="true" />
              </a>
            )}
          </div>
        </article>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8 space-y-8">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-ink sm:text-3xl">{t.knowledge.pageTitle}</h1>
        <p className="mt-2 max-w-3xl text-sm text-secondary sm:text-base">{t.knowledge.pageSubtitle}</p>
      </div>

      {/* Search & Category Filter */}
      <div className="space-y-4">
        <div className="relative max-w-md">
          <Search className="pointer-events-none absolute left-3 top-3.5 h-4 w-4 text-muted" aria-hidden="true" />
          <input
            type="search"
            className="sk-input pl-10"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder={t.knowledge.searchPlaceholder}
            aria-label={t.knowledge.searchPlaceholder}
          />
        </div>

        <div className="flex flex-wrap gap-2">
          {CATEGORIES.map((cat) => (
            <button
              key={cat.id}
              type="button"
              onClick={() => setCategory(cat.id)}
              aria-pressed={category === cat.id}
              className={`min-h-[38px] rounded-md border px-3 py-1.5 text-xs font-medium transition-colors ${
                category === cat.id
                  ? "border-accent bg-accent/15 text-accent"
                  : "border-ink/15 bg-surface text-secondary hover:text-ink"
              }`}
            >
              {lang === "kn" ? cat.labelKn : cat.labelEn}
            </button>
          ))}
        </div>
      </div>

      {error && <ErrorAlert message={error} />}

      {loading ? (
        <p className="text-sm text-secondary">Loading agricultural guides...</p>
      ) : articles.length === 0 ? (
        <div className="sk-surface-card rounded-xl p-8 text-center text-sm text-secondary">
          No articles matched your filter criteria.
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {articles.map((art) => (
            <article key={art.id} className="sk-surface-card rounded-xl p-6 flex flex-col justify-between gap-4">
              <div className="space-y-2.5">
                <span className="inline-block rounded border border-accent/35 bg-accent/10 px-2 py-0.5 text-[11px] font-medium text-accent uppercase">
                  {art.category}
                </span>
                <h2 className="text-lg font-semibold text-ink">
                  {lang === "kn" ? art.title_kn : art.title_en}
                </h2>
                <p className="text-sm leading-relaxed text-secondary">
                  {lang === "kn" ? art.summary_kn : art.summary_en}
                </p>
              </div>
              <div className="border-t border-ink/10 pt-3 space-y-3">
                <p className="text-xs text-muted">
                  {t.knowledge.sourceLabel}: {art.source_name}
                </p>
                <button
                  type="button"
                  onClick={() => openArticle(art.id)}
                  className="sk-btn-secondary w-full text-sm"
                >
                  <BookOpen className="h-4 w-4 text-accent" aria-hidden="true" />
                  <span>{t.knowledge.readArticle}</span>
                </button>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
