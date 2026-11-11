import { useState } from "react";
import { AlertTriangle, FlaskConical, Upload } from "lucide-react";
import { apiClient } from "../api/client";
import { ErrorAlert } from "../components/ErrorAlert";
import { useI18n } from "../i18n";
import type { SoilAnalysisResponse, SoilTypeOption } from "../types";

const SOIL_TYPES: SoilTypeOption[] = ["Red", "Black", "Alluvial", "Laterite", "Sandy", "Loamy", "Clay"];

export function SoilHealthPage() {
  const { lang, t } = useI18n();
  const [soilType, setSoilType] = useState<SoilTypeOption>("Red");
  const [source, setSource] = useState<"soil_test" | "estimate">("soil_test");
  const [ph, setPh] = useState("6.2");
  const [nitrogen, setNitrogen] = useState("50");
  const [phosphorus, setPhosphorus] = useState("30");
  const [potassium, setPotassium] = useState("35");
  const [analysis, setAnalysis] = useState<SoilAnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const parseVal = (v: string) => (v.trim() === "" ? null : Number(v));
      const res = await apiClient.analyzeSoil({
        soil_type: soilType,
        ph: parseVal(ph),
        nitrogen: parseVal(nitrogen),
        phosphorus: parseVal(phosphorus),
        potassium: parseVal(potassium),
        measurement_source: source,
      });
      setAnalysis(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to analyze soil inputs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6 lg:px-8 space-y-8">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-ink sm:text-3xl">{t.soilHealth.pageTitle}</h1>
        <p className="mt-2 max-w-3xl text-sm text-secondary sm:text-base">{t.soilHealth.pageSubtitle}</p>
      </div>

      <div className="grid gap-8 lg:grid-cols-12">
        <form onSubmit={handleAnalyze} className="lg:col-span-5 sk-surface-card rounded-xl p-6 space-y-4 h-fit">
          <div className="flex items-center gap-2 text-base font-semibold text-ink">
            <FlaskConical className="h-5 w-5 text-accent" aria-hidden="true" />
            <h2>Soil Parameter Check</h2>
          </div>

          <div>
            <label htmlFor="sh-soil-type" className="block text-xs font-medium text-secondary mb-1">
              {t.form.soilType}
            </label>
            <select
              id="sh-soil-type"
              className="sk-input"
              value={soilType}
              onChange={(e) => setSoilType(e.target.value as SoilTypeOption)}
            >
              {SOIL_TYPES.map((s) => (
                <option key={s} value={s}>
                  {s} soil
                </option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="sh-source" className="block text-xs font-medium text-secondary mb-1">
              {t.form.soilSource}
            </label>
            <select
              id="sh-source"
              className="sk-input"
              value={source}
              onChange={(e) => setSource(e.target.value as "soil_test" | "estimate")}
            >
              <option value="soil_test">{t.form.soilSourceTest}</option>
              <option value="estimate">{t.form.soilSourceEstimate}</option>
            </select>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label htmlFor="sh-ph" className="block text-xs text-secondary mb-1">
                {t.form.ph}
              </label>
              <input
                id="sh-ph"
                type="number"
                step="0.1"
                min="0"
                max="14"
                className="sk-input font-mono tabular-nums"
                value={ph}
                onChange={(e) => setPh(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="sh-n" className="block text-xs text-secondary mb-1">
                {t.form.nitrogen}
              </label>
              <input
                id="sh-n"
                type="number"
                min="0"
                max="500"
                className="sk-input font-mono tabular-nums"
                value={nitrogen}
                onChange={(e) => setNitrogen(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="sh-p" className="block text-xs text-secondary mb-1">
                {t.form.phosphorus}
              </label>
              <input
                id="sh-p"
                type="number"
                min="0"
                max="500"
                className="sk-input font-mono tabular-nums"
                value={phosphorus}
                onChange={(e) => setPhosphorus(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="sh-k" className="block text-xs text-secondary mb-1">
                {t.form.potassium}
              </label>
              <input
                id="sh-k"
                type="number"
                min="0"
                max="600"
                className="sk-input font-mono tabular-nums"
                value={potassium}
                onChange={(e) => setPotassium(e.target.value)}
              />
            </div>
          </div>

          <button type="submit" disabled={loading} className="sk-btn-primary w-full text-sm">
            {loading ? "Interpreting..." : t.soilHealth.analyzeButton}
          </button>

          {/* Future Soil Health Card Upload notice */}
          <div className="rounded-lg border border-dashed border-white/20 bg-canvas/50 p-4 text-xs space-y-1">
            <div className="flex items-center gap-2 font-medium text-ink">
              <Upload className="h-4 w-4 text-muted" aria-hidden="true" />
              <span>{t.soilHealth.shcFutureTitle}</span>
            </div>
            <p className="text-muted leading-relaxed">{t.soilHealth.shcFutureBody}</p>
          </div>
        </form>

        <div className="lg:col-span-7 space-y-5">
          {error && <ErrorAlert message={error} />}

          {!analysis ? (
            <div className="sk-surface-card rounded-xl p-6 text-sm text-secondary space-y-3">
              <h2 className="text-base font-semibold text-ink">Agronomic Testing Context</h2>
              <p className="leading-relaxed">
                Submit your Soil Health Card pH and NPK readings to view standardized interpretation bands.
                Because different soil laboratories use different extraction methods (such as Olsen-P vs. Bray-P
                or Alkaline KMnO₄-N), SmartKrishi explains reference ranges without prescribing unverified
                fertilizer quantities.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="sk-surface-card rounded-xl p-5">
                <p className="text-sm font-medium text-ink">
                  {lang === "kn" ? analysis.overview_kn : analysis.overview_en}
                </p>
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                {analysis.interpretations.map((item) => (
                  <article key={item.parameter} className="sk-surface-card rounded-xl p-5 space-y-2">
                    <div className="flex items-center justify-between gap-2">
                      <h3 className="text-sm font-semibold text-ink">{item.parameter}</h3>
                      <span className="rounded border border-accent/35 bg-accent/10 px-2 py-0.5 text-xs font-medium text-accent">
                        {item.status}
                      </span>
                    </div>
                    <p className="font-mono text-lg font-semibold text-ink tabular-nums">
                      {item.value !== null ? `${item.value} ${item.unit}` : "Not supplied"}
                    </p>
                    <p className="text-xs leading-relaxed text-secondary">
                      {lang === "kn" ? item.interpretation_kn : item.interpretation_en}
                    </p>
                    <p className="text-[11px] font-mono text-muted">Ref: {item.reference_range}</p>
                  </article>
                ))}
              </div>

              <div className="sk-surface-card rounded-xl p-5 space-y-2">
                <h3 className="text-sm font-semibold text-ink">Soil Management Guidance</h3>
                <ul className="list-disc pl-5 space-y-1.5 text-sm text-secondary">
                  {(lang === "kn" ? analysis.guidance_kn : analysis.guidance_en).map((g, i) => (
                    <li key={i}>{g}</li>
                  ))}
                </ul>
                <div className="mt-3 flex items-start gap-2.5 rounded-lg border border-warning/35 bg-warning/10 p-3 text-xs text-warning">
                  <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
                  <p>{lang === "kn" ? analysis.fertilizer_caution_kn : analysis.fertilizer_caution_en}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
