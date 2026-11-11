import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router-dom";
import {
  AlertTriangle,
  ArrowLeft,
  Calendar,
  CheckCircle2,
  Droplets,
  Info,
  Printer,
  Scale,
  Send,
} from "lucide-react";
import { apiClient } from "../api/client";
import { CropDetailModal } from "../components/CropDetailModal";
import { ErrorAlert } from "../components/ErrorAlert";
import { useI18n } from "../i18n";
import type { RecommendationResponse } from "../types";

export function ResultsPage() {
  const { id } = useParams<{ id: string }>();
  const location = useLocation();
  const navigate = useNavigate();
  const { lang, t } = useI18n();

  const initialState = (location.state as { result?: RecommendationResponse } | null)?.result ?? null;
  const [data, setData] = useState<RecommendationResponse | null>(initialState);
  const [loading, setLoading] = useState(!initialState);
  const [error, setError] = useState<string | null>(null);
  const [modalCropId, setModalCropId] = useState<number | null>(null);

  const [fbComment, setFbComment] = useState("");
  const [fbRating, setFbRating] = useState("4");
  const [fbSent, setFbSent] = useState(false);
  const [fbError, setFbError] = useState<string | null>(null);

  useEffect(() => {
    if (initialState && String(initialState.recommendation_id) === id) {
      setData(initialState);
      setLoading(false);
      return;
    }
    if (!id) return;
    setLoading(true);
    apiClient
      .getRecommendation(Number(id))
      .then((res) => setData(res))
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load recommendation report."))
      .finally(() => setLoading(false));
  }, [id, initialState]);

  const handleFeedback = async (e: React.FormEvent) => {
    e.preventDefault();
    if (fbComment.trim().length < 5) {
      setFbError("Please enter at least 5 characters.");
      return;
    }
    setFbError(null);
    try {
      await apiClient.submitFeedback({
        recommendation_id: data?.recommendation_id,
        category: "recommendation_accuracy",
        rating: Number(fbRating),
        district: data?.location_context.district,
        comment: fbComment.trim(),
      });
      setFbSent(true);
      setFbComment("");
    } catch (err) {
      setFbError(err instanceof Error ? err.message : "Could not submit feedback.");
    }
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-5xl px-4 py-12 text-center text-sm text-secondary">
        Loading recommendation report...
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-12 space-y-4">
        <ErrorAlert message={error || "Recommendation report unavailable."} />
        <Link to="/recommend" className="sk-btn-secondary">
          <ArrowLeft className="h-4 w-4" aria-hidden="true" />
          <span>{t.results.editInputs}</span>
        </Link>
      </div>
    );
  }

  const compareIds = data.recommendations.map((c) => c.crop_id);

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8 space-y-8">
      {/* Header & Actions */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-ink sm:text-3xl">{t.results.pageTitle}</h1>
          <p className="mt-1.5 text-sm text-secondary">
            {data.location_context.taluk}, {data.location_context.district} ·{" "}
            <span className="text-accent">{data.location_context.agro_climatic_zone}</span>
          </p>
        </div>

        <div className="flex flex-wrap gap-2.5 no-print">
          <Link to="/recommend" className="sk-btn-secondary text-sm">
            <ArrowLeft className="h-4 w-4" aria-hidden="true" />
            <span>{t.results.editInputs}</span>
          </Link>
          {compareIds.length > 0 && (
            <button
              type="button"
              onClick={() => navigate(`/compare?ids=${compareIds.join(",")}`)}
              className="sk-btn-secondary text-sm"
            >
              <Scale className="h-4 w-4 text-accent" aria-hidden="true" />
              <span>{t.results.compareSelected}</span>
            </button>
          )}
          <button type="button" onClick={() => window.print()} className="sk-btn-primary text-sm">
            <Printer className="h-4 w-4" aria-hidden="true" />
            <span>{t.results.printReport}</span>
          </button>
        </div>
      </div>

      {/* Evaluation Mode & Warnings */}
      <div className="sk-surface-card rounded-xl p-5 space-y-4">
        <div className="flex flex-wrap gap-4 text-sm">
          <div>
            <span className="text-muted">{t.results.modeLabel}: </span>
            <span className="font-mono text-ink">{data.mode_used}</span>
          </div>
          <div>
            <span className="text-muted">{t.results.confidenceLabel}: </span>
            <span
              className={`font-semibold ${
                data.confidence_level === "insufficient"
                  ? "text-danger"
                  : data.confidence_level === "reduced"
                  ? "text-warning"
                  : "text-accent"
              }`}
            >
              {data.confidence_level}
            </span>
          </div>
        </div>

        <p className="text-xs leading-relaxed text-secondary">
          {lang === "kn" ? data.scoring_notice_kn : data.scoring_notice_en}
        </p>

        {data.warnings.length > 0 && (
          <ul className="space-y-2 border-t border-white/10 pt-3">
            {data.warnings.map((w, i) => (
              <li key={i} className="flex items-start gap-2.5 text-sm text-warning">
                <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
                <span>{w}</span>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Insufficient data case */}
      {data.recommendations.length === 0 ? (
        <div className="sk-surface-card rounded-xl border-danger/45 p-8 space-y-4">
          <h2 className="text-xl font-semibold text-danger">{t.results.insufficientTitle}</h2>
          <p className="text-sm leading-relaxed text-secondary">{data.insufficient_data_reason}</p>
          <Link to="/recommend" className="sk-btn-primary">
            {t.results.editInputs}
          </Link>
        </div>
      ) : (
        /* Top 3 Recommended Crop Cards */
        <div className="space-y-6">
          {data.recommendations.map((crop) => {
            const reasons = lang === "kn" ? crop.reasons_kn : crop.reasons_en;
            const limits = lang === "kn" ? crop.limitations_kn : crop.limitations_en;
            const guidance = lang === "kn" ? crop.cultivation_guidance_kn : crop.cultivation_guidance_en;

            return (
              <article key={crop.crop_id} className="sk-surface-card rounded-xl p-6 space-y-6">
                <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                  <div className="flex items-center gap-4">
                    <img
                      src={crop.image_asset}
                      alt={crop.name_en}
                      className="h-16 w-16 rounded-lg border border-white/10 bg-canvas p-1"
                    />
                    <div>
                      <div className="flex items-center gap-2.5 flex-wrap">
                        <span className="rounded bg-accent/15 border border-accent/30 px-2 py-0.5 font-mono text-xs font-semibold text-accent">
                          Rank #{crop.rank}
                        </span>
                        <span className="text-xs text-muted">{crop.category}</span>
                      </div>
                      <h2 className="mt-1 text-xl font-semibold text-ink">
                        {lang === "kn" ? crop.name_kn : crop.name_en}
                      </h2>
                      <p className="text-xs text-secondary">
                        {lang === "kn" ? crop.name_en : crop.name_kn} ·{" "}
                        <span className="italic">{crop.scientific_name}</span>
                      </p>
                    </div>
                  </div>

                  <div className="sm:text-right">
                    <div className="font-mono text-2xl font-semibold text-accent tabular-nums">
                      {crop.illustrative_score.toFixed(1)}
                      <span className="text-sm text-muted"> / 100</span>
                    </div>
                    <p className="text-xs text-secondary">{crop.suitability_category}</p>
                    {crop.ml_probability !== null && (
                      <p className="mt-0.5 font-mono text-xs text-muted tabular-nums">
                        {t.results.mlProbabilityLabel}: {(crop.ml_probability * 100).toFixed(1)}%
                      </p>
                    )}
                  </div>
                </div>

                {/* Key specs row */}
                <div className="grid gap-3 sm:grid-cols-3">
                  <div className="rounded-lg border border-white/10 bg-canvas/65 p-3">
                    <div className="flex items-center gap-1.5 text-xs text-muted">
                      <Droplets className="h-3.5 w-3.5 text-accent" aria-hidden="true" />
                      <span>{t.results.waterNeed}</span>
                    </div>
                    <p className="mt-1 font-mono text-sm text-ink tabular-nums">
                      {crop.water_requirement_level} ({crop.water_requirement_mm_min}-{crop.water_requirement_mm_max} mm)
                    </p>
                  </div>
                  <div className="rounded-lg border border-white/10 bg-canvas/65 p-3">
                    <div className="flex items-center gap-1.5 text-xs text-muted">
                      <Calendar className="h-3.5 w-3.5 text-accent" aria-hidden="true" />
                      <span>{t.results.seasonLabel}</span>
                    </div>
                    <p className="mt-1 text-sm text-ink">{crop.suitable_seasons.join(", ")}</p>
                  </div>
                  <div className="rounded-lg border border-white/10 bg-canvas/65 p-3">
                    <div className="flex items-center gap-1.5 text-xs text-muted">
                      <Info className="h-3.5 w-3.5 text-accent" aria-hidden="true" />
                      <span>{t.results.durationLabel}</span>
                    </div>
                    <p className="mt-1 font-mono text-sm text-ink tabular-nums">
                      {crop.growing_duration_days_min}-{crop.growing_duration_days_max} {t.results.daysUnit}
                    </p>
                  </div>
                </div>

                {/* Dimension scores breakdown */}
                <div>
                  <h3 className="text-xs font-semibold uppercase tracking-wide text-muted mb-3">
                    {t.results.dimensionsTitle}
                  </h3>
                  <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-6">
                    {Object.entries(crop.dimension_scores).map(([dim, val]) => (
                      <div key={dim} className="rounded border border-white/10 bg-canvas/50 p-2.5">
                        <div className="flex justify-between text-xs">
                          <span className="capitalize text-secondary">{dim}</span>
                          <span className="font-mono text-ink tabular-nums">{val}%</span>
                        </div>
                        <div className="mt-1.5 h-1.5 w-full rounded-full bg-white/10">
                          <div
                            className="h-1.5 rounded-full bg-accent"
                            style={{ width: `${Math.min(100, Math.max(0, val))}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Reasons & Limitations */}
                <div className="grid gap-6 md:grid-cols-2">
                  <div>
                    <h3 className="text-sm font-semibold text-ink mb-2">{t.results.reasonsTitle}</h3>
                    <ul className="space-y-1.5 text-sm text-secondary">
                      {reasons.map((r, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-accent" aria-hidden="true" />
                          <span>{r}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h3 className="text-sm font-semibold text-ink mb-2">{t.results.limitationsTitle}</h3>
                    <ul className="space-y-1.5 text-sm text-secondary">
                      {limits.map((lim, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-warning" aria-hidden="true" />
                          <span>{lim}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Basic Cultivation Guidance */}
                <div className="border-t border-white/10 pt-4 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
                  <div className="max-w-3xl space-y-1">
                    <h3 className="text-sm font-semibold text-ink">{t.results.guidanceTitle}</h3>
                    <p className="text-sm leading-relaxed text-secondary">{guidance}</p>
                    <p className="text-xs text-muted pt-1">
                      {t.results.sourceLabel}: {crop.information_source}
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={() => setModalCropId(crop.crop_id)}
                    className="sk-btn-secondary shrink-0 text-sm no-print"
                  >
                    {t.results.viewDetails}
                  </button>
                </div>
              </article>
            );
          })}
        </div>
      )}

      {/* Disclaimer */}
      <div className="rounded-lg border border-white/15 bg-surface p-4 text-xs leading-relaxed text-secondary">
        {lang === "kn" ? data.disclaimer_kn : data.disclaimer_en}
      </div>

      {/* Feedback Form */}
      <section className="sk-surface-card rounded-xl p-6 space-y-4 no-print">
        <h2 className="text-base font-semibold text-ink">{t.results.feedbackTitle}</h2>
        <p className="text-sm text-secondary">{t.results.feedbackPrompt}</p>
        {fbSent ? (
          <p className="text-sm font-medium text-accent">{t.results.feedbackSuccess}</p>
        ) : (
          <form onSubmit={handleFeedback} className="space-y-3">
            <div className="grid gap-3 sm:grid-cols-4">
              <div>
                <label htmlFor="fb-rating" className="block text-xs text-muted mb-1">
                  Usefulness (1-5)
                </label>
                <select
                  id="fb-rating"
                  className="sk-input"
                  value={fbRating}
                  onChange={(e) => setFbRating(e.target.value)}
                >
                  <option value="5">5 — Very helpful</option>
                  <option value="4">4 — Helpful</option>
                  <option value="3">3 — Moderate</option>
                  <option value="2">2 — Needs adjustment</option>
                  <option value="1">1 — Not suitable</option>
                </select>
              </div>
              <div className="sm:col-span-3">
                <label htmlFor="fb-comment" className="block text-xs text-muted mb-1">
                  Observations
                </label>
                <input
                  id="fb-comment"
                  type="text"
                  className="sk-input"
                  value={fbComment}
                  onChange={(e) => setFbComment(e.target.value)}
                  placeholder="Share local variety or rainfall notes..."
                />
              </div>
            </div>
            {fbError && <p className="text-xs text-danger">{fbError}</p>}
            <button type="submit" className="sk-btn-secondary text-sm">
              <Send className="h-4 w-4" aria-hidden="true" />
              <span>{t.results.feedbackSubmit}</span>
            </button>
          </form>
        )}
      </section>

      <CropDetailModal cropId={modalCropId} onClose={() => setModalCropId(null)} />
    </div>
  );
}
