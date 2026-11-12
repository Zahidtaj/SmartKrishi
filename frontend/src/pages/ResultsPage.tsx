import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router-dom";
import {
  AlertTriangle,
  ArrowLeft,
  CheckCircle2,
  CloudOff,
  CloudRain,
  CloudSun,
  Compass,
  Droplets,
  HelpCircle,
  Info,
  Printer,
  Scale,
  ShieldCheck,
  Sprout,
  Sun,
} from "lucide-react";
import { apiClient } from "../api/client";
import { ErrorAlert } from "../components/ErrorAlert";
import { useI18n } from "../i18n";
import type { RecommendationResponse } from "../types";

export function ResultsPage() {
  const { id } = useParams();
  const routeLocation = useLocation();
  const navigate = useNavigate();
  const { lang, t } = useI18n();

  const initialState = (routeLocation.state as { recommendation?: RecommendationResponse } | null)?.recommendation || null;
  const [data, setData] = useState<RecommendationResponse | null>(initialState);
  const [loading, setLoading] = useState(!initialState);
  const [error, setError] = useState<string | null>(null);
  const [selectedCompareIds, setSelectedCompareIds] = useState<number[]>([]);

  // Feedback form
  const [rating, setRating] = useState(4);
  const [comment, setComment] = useState("");
  const [fbSent, setFbSent] = useState(false);
  const [fbError, setFbError] = useState<string | null>(null);

  useEffect(() => {
    if (initialState) {
      setSelectedCompareIds(initialState.recommendations.map((r) => r.crop_id));
      return;
    }
    const recId = Number(id);
    if (!recId) {
      setError("Invalid recommendation ID.");
      setLoading(false);
      return;
    }
    setLoading(true);
    apiClient
      .getRecommendation(recId)
      .then((res) => {
        setData(res);
        setSelectedCompareIds(res.recommendations.map((r) => r.crop_id));
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load recommendation."))
      .finally(() => setLoading(false));
  }, [id, initialState]);

  const toggleCompare = (cropId: number) => {
    setSelectedCompareIds((prev) => {
      if (prev.includes(cropId)) return prev.filter((item) => item !== cropId);
      if (prev.length >= 3) return [...prev.slice(1), cropId];
      return [...prev, cropId];
    });
  };

  const handleCompare = () => {
    if (selectedCompareIds.length === 0) return;
    navigate(`/compare?ids=${selectedCompareIds.join(",")}`);
  };

  const handleFeedback = async (e: React.FormEvent) => {
    e.preventDefault();
    if (comment.trim().length < 5) {
      setFbError(lang === "kn" ? "ಕನಿಷ್ಠ 5 ಅಕ್ಷರಗಳ ಅಭಿಪ್ರಾಯ ಬರೆಯಿರಿ." : "Please write at least 5 characters of feedback.");
      return;
    }
    try {
      await apiClient.submitFeedback({
        recommendation_id: data?.recommendation_id,
        category: "recommendation_accuracy",
        rating,
        district: data?.location_context.district,
        comment: comment.trim(),
      });
      setFbSent(true);
      setFbError(null);
    } catch (err) {
      setFbError(err instanceof Error ? err.message : "Could not submit feedback.");
    }
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-6xl px-4 py-16 text-center text-secondary">
        Loading observation advisory...
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-12 space-y-4">
        <ErrorAlert message={error || "Recommendation not found."} />
        <Link to="/recommend" className="sk-btn-secondary inline-flex">
          <ArrowLeft className="h-4 w-4" />
          <span>{t.results.editInputs}</span>
        </Link>
      </div>
    );
  }

  const soil = data.soil_interpretation;
  const weather = data.weather_advisory;
  const advisory = weather.farming_advisory;
  const provenance = data.input_provenance;

  const badgeTone = (cat: string) => {
    if (cat.includes("Highly Suitable")) return "border-accent/40 bg-accent/15 text-accent";
    if (cat.includes("Precautions") || cat.includes("Conditional")) return "border-warning/40 bg-warning/15 text-warning";
    return "border-danger/40 bg-danger/15 text-danger";
  };

  const riskTone = (lvl: string) => {
    if (lvl === "high") return "border-danger/40 bg-danger/10 text-danger";
    if (lvl === "moderate") return "border-warning/40 bg-warning/10 text-warning";
    return "border-accent/40 bg-accent/10 text-accent";
  };

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8 space-y-8">
      {/* Header & Actions */}
      <div className="flex flex-col gap-4 border-b border-ink/10 pb-6 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-ink sm:text-3xl">{t.results.pageTitle}</h1>
          <p className="mt-1.5 text-sm text-secondary">
            {data.location_context.taluk}, {data.location_context.district} · {data.location_context.agro_climatic_zone} (
            <span className="font-mono text-accent">{data.location_context.zone_code}</span>)
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5 no-print">
          <Link to="/recommend" className="sk-btn-secondary text-sm">
            <ArrowLeft className="h-4 w-4" aria-hidden="true" />
            <span>{t.results.editInputs}</span>
          </Link>
          {selectedCompareIds.length > 0 && (
            <button type="button" onClick={handleCompare} className="sk-btn-secondary text-sm">
              <Scale className="h-4 w-4 text-accent" aria-hidden="true" />
              <span>
                {t.results.compareSelected} ({selectedCompareIds.length})
              </span>
            </button>
          )}
          <button type="button" onClick={() => window.print()} className="sk-btn-primary text-sm">
            <Printer className="h-4 w-4" aria-hidden="true" />
            <span>{t.results.printReport}</span>
          </button>
        </div>
      </div>

      {/* Mode & Confidence Strip */}
      <div className="grid gap-4 sm:grid-cols-3">
        <div className="sk-surface-card rounded-xl p-4">
          <p className="text-xs text-muted">{t.results.modeLabel}</p>
          <p className="mt-1 text-sm font-semibold text-ink">Observation & Location Rule Engine</p>
        </div>
        <div className="sk-surface-card rounded-xl p-4">
          <p className="text-xs text-muted">{t.results.confidenceLabel}</p>
          <p className="mt-1 text-sm font-semibold uppercase tracking-wide text-accent">{data.confidence_level}</p>
        </div>
        <div className="sk-surface-card rounded-xl p-4">
          <p className="text-xs text-muted">Normal Zone Rainfall</p>
          <p className="mt-1 font-mono text-sm font-semibold text-ink tabular-nums">
            {data.location_context.normal_annual_rainfall_mm ?? "—"} mm / year
          </p>
        </div>
      </div>

      {/* Warnings & Incomplete Observation Banner */}
      {(data.insufficient_data_reason || data.warnings.length > 0) && (
        <div className="rounded-xl border border-warning/40 bg-warning/10 p-5 space-y-2.5">
          <div className="flex items-center gap-2 font-semibold text-ink">
            <AlertTriangle className="h-5 w-5 text-warning shrink-0" aria-hidden="true" />
            <h2>{t.results.insufficientTitle}</h2>
          </div>
          {data.insufficient_data_reason && <p className="text-sm text-ink">{data.insufficient_data_reason}</p>}
          {data.warnings.length > 0 && (
            <ul className="list-disc pl-5 text-sm text-secondary space-y-1">
              {data.warnings.map((w, idx) => (
                <li key={idx}>{w}</li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* Ranked Recommended Crops */}
      <section className="space-y-6">
        {data.recommendations.map((crop) => {
          const name = lang === "kn" ? crop.name_kn : crop.name_en;
          const reasons = lang === "kn" ? crop.reasons_kn : crop.reasons_en;
          const limitations = lang === "kn" ? crop.limitations_kn : crop.limitations_en;
          const missing = lang === "kn" ? crop.missing_info_kn : crop.missing_info_en;
          const guidance = lang === "kn" ? crop.cultivation_guidance_kn : crop.cultivation_guidance_en;
          const checked = selectedCompareIds.includes(crop.crop_id);

          return (
            <article key={crop.crop_id} className="sk-surface-card rounded-2xl p-6 space-y-6">
              <div className="flex flex-col gap-4 border-b border-ink/10 pb-5 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex items-center gap-4">
                  <div className="relative h-20 w-20 shrink-0 rounded-xl border border-ink/10 bg-elevated/60 p-2">
                    <img src={crop.image_asset} alt={name} className="h-full w-full object-contain" />
                    <span className="absolute -left-2 -top-2 inline-flex h-7 w-7 items-center justify-center rounded-full bg-accent font-mono text-xs font-bold text-[var(--sk-accent-ink)]">
                      #{crop.rank}
                    </span>
                  </div>
                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <h2 className="text-xl font-semibold text-ink">{name}</h2>
                      <span className={`rounded-md border px-2.5 py-0.5 text-xs font-semibold ${badgeTone(crop.suitability_category)}`}>
                        {crop.suitability_category}
                      </span>
                    </div>
                    <p className="mt-0.5 text-xs italic text-muted">
                      {crop.scientific_name} · {crop.category}
                    </p>
                    <p className="mt-2 font-mono text-xs text-secondary tabular-nums">
                      Prototype Index: <strong className="text-ink">{crop.illustrative_score.toFixed(1)}/100</strong>
                    </p>
                  </div>
                </div>

                <label className="no-print inline-flex cursor-pointer items-center gap-2 rounded-lg border border-ink/15 bg-elevated/40 px-3 py-2 text-xs font-medium text-ink hover:border-accent">
                  <input
                    type="checkbox"
                    checked={checked}
                    onChange={() => toggleCompare(crop.crop_id)}
                    className="h-4 w-4 accent-[var(--sk-accent)]"
                  />
                  <span>{t.results.compareSelected}</span>
                </label>
              </div>

              {/* Metadata Pills */}
              <div className="grid gap-3 sm:grid-cols-4">
                <div className="rounded-lg bg-elevated/50 p-3 border border-ink/10">
                  <p className="text-[11px] text-muted">{t.results.waterNeed}</p>
                  <p className="mt-0.5 text-sm font-semibold text-ink">
                    {crop.water_requirement_level} ({crop.water_requirement_mm_min}-{crop.water_requirement_mm_max} mm)
                  </p>
                </div>
                <div className="rounded-lg bg-elevated/50 p-3 border border-ink/10">
                  <p className="text-[11px] text-muted">{t.results.durationLabel}</p>
                  <p className="mt-0.5 font-mono text-sm font-semibold text-ink tabular-nums">
                    {crop.growing_duration_days_min}-{crop.growing_duration_days_max} {t.results.daysUnit}
                  </p>
                </div>
                <div className="rounded-lg bg-elevated/50 p-3 border border-ink/10">
                  <p className="text-[11px] text-muted">{t.results.seasonLabel}</p>
                  <p className="mt-0.5 text-sm font-semibold text-ink">{crop.suitable_seasons.join(", ")}</p>
                </div>
                <div className="rounded-lg bg-elevated/50 p-3 border border-ink/10">
                  <p className="text-[11px] text-muted">{t.results.sourceLabel}</p>
                  <p className="mt-0.5 text-xs font-medium text-secondary">{crop.information_source}</p>
                </div>
              </div>

              {/* Three Explicit Explanation Pillars */}
              <div className="grid gap-5 lg:grid-cols-3">
                <div className="rounded-xl border border-accent/25 bg-accent/5 p-4 space-y-2">
                  <h3 className="flex items-center gap-1.5 text-sm font-semibold text-accent">
                    <CheckCircle2 className="h-4 w-4 shrink-0" aria-hidden="true" />
                    <span>{t.results.reasonsTitle}</span>
                  </h3>
                  <ul className="space-y-1.5 text-xs leading-relaxed text-secondary">
                    {reasons.map((r, i) => (
                      <li key={i}>• {r}</li>
                    ))}
                  </ul>
                </div>

                <div className="rounded-xl border border-warning/25 bg-warning/5 p-4 space-y-2">
                  <h3 className="flex items-center gap-1.5 text-sm font-semibold text-warning">
                    <AlertTriangle className="h-4 w-4 shrink-0" aria-hidden="true" />
                    <span>{t.results.limitationsTitle}</span>
                  </h3>
                  <ul className="space-y-1.5 text-xs leading-relaxed text-secondary">
                    {limitations.map((lim, i) => (
                      <li key={i}>• {lim}</li>
                    ))}
                  </ul>
                </div>

                <div className="rounded-xl border border-info/25 bg-info/5 p-4 space-y-2">
                  <h3 className="flex items-center gap-1.5 text-sm font-semibold text-info">
                    <HelpCircle className="h-4 w-4 shrink-0" aria-hidden="true" />
                    <span>{t.results.missingTitle}</span>
                  </h3>
                  <ul className="space-y-1.5 text-xs leading-relaxed text-secondary">
                    {missing.length > 0 ? (
                      missing.map((m, i) => <li key={i}>• {m}</li>)
                    ) : (
                      <li>• All core observation inputs were provided cleanly.</li>
                    )}
                  </ul>
                </div>
              </div>

              {/* Compatibility Dimension Bars & Cultivation Guidance */}
              <div className="grid gap-6 lg:grid-cols-12 border-t border-ink/10 pt-5">
                <div className="lg:col-span-5 space-y-2.5">
                  <h3 className="text-xs font-semibold uppercase tracking-wider text-muted">{t.results.dimensionsTitle}</h3>
                  {Object.entries(crop.dimension_scores).map(([dim, val]) => (
                    <div key={dim} className="space-y-1">
                      <div className="flex justify-between text-xs">
                        <span className="capitalize text-secondary">{dim.replace("_", " & ")}</span>
                        <span className="font-mono text-ink tabular-nums">{val.toFixed(0)}</span>
                      </div>
                      <div className="h-1.5 w-full overflow-hidden rounded-full bg-ink/10">
                        <div className="h-full rounded-full bg-accent" style={{ width: `${Math.min(100, val)}%` }} />
                      </div>
                    </div>
                  ))}
                </div>

                <div className="lg:col-span-7 rounded-xl border border-ink/10 bg-elevated/40 p-4 space-y-2">
                  <h3 className="flex items-center gap-1.5 text-sm font-semibold text-ink">
                    <Sprout className="h-4 w-4 text-accent" aria-hidden="true" />
                    <span>{t.results.guidanceTitle}</span>
                  </h3>
                  <p className="text-sm leading-relaxed text-secondary">{guidance}</p>
                </div>
              </div>
            </article>
          );
        })}
      </section>

      {/* Physical Soil & Land Synthesis */}
      <section className="sk-surface-card rounded-2xl p-6 space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-ink/10 pb-3">
          <div className="flex items-center gap-2">
            <Compass className="h-5 w-5 text-accent" aria-hidden="true" />
            <h2 className="text-lg font-semibold text-ink">{t.results.soilObsTitle}</h2>
          </div>
          <span className="rounded-md border border-accent/30 bg-accent/10 px-2.5 py-0.5 font-mono text-xs uppercase text-accent">
            Confidence: {soil.observation_confidence}
          </span>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <div className="space-y-2 text-sm text-secondary">
            {(lang === "kn" ? soil.insights_kn : soil.insights_en).map((item, idx) => (
              <p key={idx}>• {item}</p>
            ))}
          </div>
          <div className="space-y-2 text-sm text-secondary">
            {(lang === "kn" ? soil.management_guidance_kn : soil.management_guidance_en).map((item, idx) => (
              <p key={idx}>• {item}</p>
            ))}
          </div>
        </div>

        <div className="rounded-lg border border-warning/30 bg-warning/10 p-3.5 text-xs text-ink flex items-start gap-2">
          <Info className="h-4 w-4 shrink-0 text-warning mt-0.5" aria-hidden="true" />
          <span>{lang === "kn" ? soil.color_disclaimer_kn : soil.color_disclaimer_en}</span>
        </div>
      </section>

      {/* Dedicated Weather and Farming Advisory Section */}
      <section className="sk-surface-card rounded-2xl p-6 space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-ink/10 pb-4">
          <div className="flex items-center gap-2.5">
            <CloudSun className="h-5 w-5 text-accent" aria-hidden="true" />
            <h2 className="text-lg font-semibold text-ink">{t.results.weatherAdvisoryTitle}</h2>
          </div>
          <span
            className={`inline-flex items-center gap-1.5 rounded-md border px-2.5 py-1 text-xs font-semibold ${
              advisory.live_weather_available
                ? "border-accent/40 bg-accent/10 text-accent"
                : "border-warning/40 bg-warning/10 text-warning"
            }`}
          >
            {advisory.live_weather_available ? <Sun className="h-3.5 w-3.5" /> : <CloudOff className="h-3.5 w-3.5" />}
            <span>
              {advisory.live_weather_available
                ? "Live Weather + Zone Normals"
                : "Zone Climate Normals Only (Live Feed Unavailable)"}
            </span>
          </span>
        </div>

        {/* 4-Source Climate vs Weather Separation Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-xl border border-ink/10 bg-elevated/40 p-4 space-y-1.5">
            <p className="text-xs font-semibold text-accent">{t.results.climateNormalsLabel}</p>
            <p className="text-sm font-medium text-ink">
              {weather.long_term_climate.season_normal_temp_c} °C · {weather.long_term_climate.season_normal_rainfall_mm} mm
            </p>
            <p className="text-xs text-secondary">{weather.long_term_climate.typical_rainfall_pattern}</p>
          </div>

          <div className="rounded-xl border border-ink/10 bg-elevated/40 p-4 space-y-1.5">
            <p className="text-xs font-semibold text-info">{t.results.currentWeatherLabel}</p>
            {weather.current_weather.status === "available" ? (
              <p className="text-sm font-medium text-ink">
                {weather.current_weather.temperature_c} °C · Humidity {weather.current_weather.humidity_pct}%
              </p>
            ) : (
              <p className="text-xs font-medium text-warning">Unavailable (Not fabricated)</p>
            )}
            <p className="text-xs text-secondary">
              {weather.current_weather.status === "available"
                ? weather.current_weather.provider
                : lang === "kn"
                  ? weather.current_weather.reason_kn
                  : weather.current_weather.reason_en}
            </p>
          </div>

          <div className="rounded-xl border border-ink/10 bg-elevated/40 p-4 space-y-1.5">
            <p className="text-xs font-semibold text-info">{t.results.forecastLabel}</p>
            {weather.short_term_forecast.status === "available" ? (
              <p className="text-sm font-medium text-ink">
                7d Rain: {weather.short_term_forecast.next_7_days_rain_total_mm} mm (Peak:{" "}
                {weather.short_term_forecast.peak_daily_rain_mm} mm/d)
              </p>
            ) : (
              <p className="text-xs font-medium text-warning">Unavailable offline</p>
            )}
            <p className="text-xs text-secondary">
              {weather.short_term_forecast.status === "available"
                ? weather.short_term_forecast.provider
                : lang === "kn"
                  ? weather.short_term_forecast.reason_kn
                  : weather.short_term_forecast.reason_en}
            </p>
          </div>

          <div className="rounded-xl border border-ink/10 bg-elevated/40 p-4 space-y-1.5">
            <p className="text-xs font-semibold text-secondary">{t.results.seasonalOutlookLabel}</p>
            <p className="text-xs text-ink">
              {lang === "kn"
                ? weather.seasonal_outlook.outlook_summary_kn
                : weather.seasonal_outlook.outlook_summary_en}
            </p>
            <p className="text-[11px] text-muted">
              {lang === "kn" ? weather.seasonal_outlook.limitation_kn : weather.seasonal_outlook.limitation_en}
            </p>
          </div>
        </div>

        {/* 4 Practical Farming Weather Decisions */}
        <div className="grid gap-4 md:grid-cols-2">
          <div className="rounded-xl border border-ink/10 bg-canvas/50 p-4 space-y-1.5">
            <p className="text-xs font-semibold text-ink flex items-center gap-1.5">
              <Sprout className="h-4 w-4 text-accent" />
              <span>{t.results.sowingSuitabilityLabel}</span>
            </p>
            <p className="text-sm text-secondary">
              {lang === "kn" ? advisory.sowing_suitability_kn : advisory.sowing_suitability_en}
            </p>
          </div>

          <div className={`rounded-xl border p-4 space-y-1.5 ${riskTone(advisory.heavy_rainfall_risk_level)}`}>
            <p className="text-xs font-semibold flex items-center gap-1.5">
              <CloudRain className="h-4 w-4" />
              <span>
                {t.results.heavyRainRiskLabel} ({advisory.heavy_rainfall_risk_level.toUpperCase()})
              </span>
            </p>
            <p className="text-sm text-ink">
              {lang === "kn" ? advisory.heavy_rainfall_risk_kn : advisory.heavy_rainfall_risk_en}
            </p>
          </div>

          <div className={`rounded-xl border p-4 space-y-1.5 ${riskTone(advisory.dry_spell_risk_level)}`}>
            <p className="text-xs font-semibold flex items-center gap-1.5">
              <Sun className="h-4 w-4" />
              <span>
                {t.results.drySpellRiskLabel} ({advisory.dry_spell_risk_level.toUpperCase()})
              </span>
            </p>
            <p className="text-sm text-ink">
              {lang === "kn" ? advisory.dry_spell_risk_kn : advisory.dry_spell_risk_en}
            </p>
          </div>

          <div className="rounded-xl border border-ink/10 bg-canvas/50 p-4 space-y-1.5">
            <p className="text-xs font-semibold text-ink flex items-center gap-1.5">
              <Droplets className="h-4 w-4 text-accent" />
              <span>{t.results.irrigationPlanLabel}</span>
            </p>
            <p className="text-sm text-secondary">
              {lang === "kn" ? advisory.irrigation_planning_kn : advisory.irrigation_planning_en}
            </p>
          </div>
        </div>
      </section>

      {/* Transparent Provenance & Disclaimers */}
      <section className="sk-surface-card rounded-2xl p-6 space-y-4">
        <h2 className="flex items-center gap-2 text-base font-semibold text-ink">
          <ShieldCheck className="h-5 w-5 text-accent" aria-hidden="true" />
          <span>{t.results.provenanceTitle}</span>
        </h2>
        <div className="grid gap-4 md:grid-cols-2 text-xs text-secondary">
          <div className="rounded-lg border border-ink/10 bg-elevated/40 p-3.5 space-y-1">
            <p className="font-semibold text-ink">{provenance.farmer_observed.label}</p>
            <p>{provenance.farmer_observed.fields.join(" · ")}</p>
          </div>
          <div className="rounded-lg border border-ink/10 bg-elevated/40 p-3.5 space-y-1">
            <p className="font-semibold text-ink">{provenance.institution_sourced.label}</p>
            <p>{provenance.institution_sourced.sources.join(" · ")}</p>
            <p className="text-[11px] text-muted">
              Status: {provenance.institution_sourced.location_verification_status} · Last updated{" "}
              {provenance.institution_sourced.location_last_updated}
            </p>
          </div>
        </div>
        <p className="text-xs text-muted">{lang === "kn" ? data.disclaimer_kn : data.disclaimer_en}</p>
      </section>

      {/* Farmer Feedback Card */}
      <section className="sk-surface-card rounded-2xl p-6 no-print space-y-4">
        <h2 className="text-base font-semibold text-ink">{t.results.feedbackTitle}</h2>
        <p className="text-sm text-secondary">{t.results.feedbackPrompt}</p>
        {fbError && <ErrorAlert message={fbError} />}
        {fbSent ? (
          <p className="rounded-lg border border-accent/40 bg-accent/10 p-3 text-sm text-accent">
            {t.results.feedbackSuccess}
          </p>
        ) : (
          <form onSubmit={handleFeedback} className="space-y-3">
            <div className="flex items-center gap-2">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  type="button"
                  onClick={() => setRating(star)}
                  className={`h-9 w-9 rounded-lg border text-sm font-semibold transition-colors ${
                    rating >= star
                      ? "border-accent bg-accent text-[var(--sk-accent-ink)]"
                      : "border-ink/15 bg-elevated text-secondary"
                  }`}
                >
                  {star}
                </button>
              ))}
            </div>
            <textarea
              rows={2}
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Share observations from your village..."
              className="sk-input"
            />
            <button type="submit" className="sk-btn-primary text-sm">
              {t.results.feedbackSubmit}
            </button>
          </form>
        )}
      </section>
    </div>
  );
}
