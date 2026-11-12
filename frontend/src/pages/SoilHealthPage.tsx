import { useState } from "react";
import { AlertTriangle, CheckCircle2, ChevronDown, ChevronUp, Compass, FlaskConical, Info } from "lucide-react";
import { apiClient } from "../api/client";
import { ErrorAlert } from "../components/ErrorAlert";
import { useI18n } from "../i18n";
import type {
  DrainageOption,
  ErosionIssueOption,
  MoistureRetentionOption,
  SoilAnalysisResponse,
  SoilColorOption,
  SoilDepthOption,
  SoilObservationResult,
  SoilTextureOption,
  SoilTypeOption,
  VisibleStonesOption,
  WaterloggingIssueOption,
} from "../types";

export function SoilHealthPage() {
  const { lang, t } = useI18n();

  // Primary: Field Soil Observation Interpreter
  const [soilColor, setSoilColor] = useState<SoilColorOption>("red");
  const [soilTexture, setSoilTexture] = useState<SoilTextureOption>("loamy");
  const [drainageAfterRain, setDrainageAfterRain] = useState<DrainageOption>("moderately");
  const [moistureRetention, setMoistureRetention] = useState<MoistureRetentionOption>("short_period");
  const [soilDepth, setSoilDepth] = useState<SoilDepthOption>("medium");
  const [visibleStones, setVisibleStones] = useState<VisibleStonesOption>("none_few");
  const [waterloggingIssue, setWaterloggingIssue] = useState<WaterloggingIssueOption>("none");
  const [erosionIssue, setErosionIssue] = useState<ErosionIssueOption>("none");
  const [obsResult, setObsResult] = useState<SoilObservationResult | null>(null);
  const [obsLoading, setObsLoading] = useState(false);
  const [obsError, setObsError] = useState<string | null>(null);

  // Secondary (Collapsed & Strictly Optional): Lab Soil Health Card Interpreter
  const [showOptionalLab, setShowOptionalLab] = useState(false);
  const [soilType, setSoilType] = useState<SoilTypeOption>("Red");
  const [ph, setPh] = useState("6.4");
  const [nitrogen, setNitrogen] = useState("55");
  const [phosphorus, setPhosphorus] = useState("30");
  const [potassium, setPotassium] = useState("40");
  const [labResult, setLabResult] = useState<SoilAnalysisResponse | null>(null);
  const [labError, setLabError] = useState<string | null>(null);

  const handleObserveSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setObsLoading(true);
    setObsError(null);
    try {
      const res = await apiClient.observeSoil({
        soil_color: soilColor,
        soil_texture: soilTexture,
        drainage_after_rain: drainageAfterRain,
        moisture_retention: moistureRetention,
        soil_depth: soilDepth,
        visible_stones: visibleStones,
        waterlogging_issue: waterloggingIssue,
        erosion_issue: erosionIssue,
      });
      setObsResult(res);
    } catch (err) {
      setObsError(err instanceof Error ? err.message : "Failed to interpret soil observations.");
    } finally {
      setObsLoading(false);
    }
  };

  const handleLabSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLabError(null);
    try {
      const res = await apiClient.analyzeSoil({
        soil_type: soilType,
        ph: ph ? Number(ph) : null,
        nitrogen: nitrogen ? Number(nitrogen) : null,
        phosphorus: phosphorus ? Number(phosphorus) : null,
        potassium: potassium ? Number(potassium) : null,
        measurement_source: "soil_test",
      });
      setLabResult(res);
    } catch (err) {
      setLabError(err instanceof Error ? err.message : "Failed to interpret lab values.");
    }
  };

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8 space-y-10">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-ink sm:text-3xl">{t.soilHealth.pageTitle}</h1>
        <p className="mt-2 max-w-3xl text-sm text-secondary sm:text-base">{t.soilHealth.pageSubtitle}</p>
      </div>

      {/* Primary Observation-Based Soil Interpreter */}
      <div className="grid gap-8 lg:grid-cols-12">
        <form onSubmit={handleObserveSubmit} className="sk-surface-card rounded-2xl p-6 space-y-4 lg:col-span-6">
          <div className="flex items-center gap-2 border-b border-ink/10 pb-3">
            <Compass className="h-5 w-5 text-accent" aria-hidden="true" />
            <h2 className="text-base font-semibold text-ink">Physical Field Observations</h2>
          </div>

          {obsError && <ErrorAlert message={obsError} />}

          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="obsColor" className="block text-xs font-medium text-secondary">
                {t.wizard.steps.soilColor.title}
              </label>
              <select
                id="obsColor"
                value={soilColor}
                onChange={(e) => setSoilColor(e.target.value as SoilColorOption)}
                className="sk-input mt-1"
              >
                {Object.entries(t.wizard.colors).map(([k, v]) => (
                  <option key={k} value={k}>
                    {v.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="obsTexture" className="block text-xs font-medium text-secondary">
                {t.wizard.steps.soilTexture.title}
              </label>
              <select
                id="obsTexture"
                value={soilTexture}
                onChange={(e) => setSoilTexture(e.target.value as SoilTextureOption)}
                className="sk-input mt-1"
              >
                {Object.entries(t.wizard.textures).map(([k, v]) => (
                  <option key={k} value={k}>
                    {v.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="obsDrain" className="block text-xs font-medium text-secondary">
                {t.wizard.steps.drainage.qRain}
              </label>
              <select
                id="obsDrain"
                value={drainageAfterRain}
                onChange={(e) => setDrainageAfterRain(e.target.value as DrainageOption)}
                className="sk-input mt-1"
              >
                {Object.entries(t.wizard.drainages).map(([k, v]) => (
                  <option key={k} value={k}>
                    {v.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="obsMoisture" className="block text-xs font-medium text-secondary">
                {t.wizard.steps.drainage.qMoisture}
              </label>
              <select
                id="obsMoisture"
                value={moistureRetention}
                onChange={(e) => setMoistureRetention(e.target.value as MoistureRetentionOption)}
                className="sk-input mt-1"
              >
                {Object.entries(t.wizard.moistures).map(([k, v]) => (
                  <option key={k} value={k}>
                    {v.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="obsDepth" className="block text-xs font-medium text-secondary">
                {t.wizard.steps.land.qDepth}
              </label>
              <select
                id="obsDepth"
                value={soilDepth}
                onChange={(e) => setSoilDepth(e.target.value as SoilDepthOption)}
                className="sk-input mt-1"
              >
                {Object.entries(t.wizard.depths).map(([k, v]) => (
                  <option key={k} value={k}>
                    {v.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="obsStones" className="block text-xs font-medium text-secondary">
                {t.wizard.steps.land.qStones}
              </label>
              <select
                id="obsStones"
                value={visibleStones}
                onChange={(e) => setVisibleStones(e.target.value as VisibleStonesOption)}
                className="sk-input mt-1"
              >
                {Object.entries(t.wizard.stones).map(([k, v]) => (
                  <option key={k} value={k}>
                    {v.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="obsWaterlog" className="block text-xs font-medium text-secondary">
                {t.wizard.steps.land.qWaterlog}
              </label>
              <select
                id="obsWaterlog"
                value={waterloggingIssue}
                onChange={(e) => setWaterloggingIssue(e.target.value as WaterloggingIssueOption)}
                className="sk-input mt-1"
              >
                {Object.entries(t.wizard.waterlogs).map(([k, v]) => (
                  <option key={k} value={k}>
                    {v.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="obsErosion" className="block text-xs font-medium text-secondary">
                {t.wizard.steps.land.qErosion}
              </label>
              <select
                id="obsErosion"
                value={erosionIssue}
                onChange={(e) => setErosionIssue(e.target.value as ErosionIssueOption)}
                className="sk-input mt-1"
              >
                {Object.entries(t.wizard.erosions).map(([k, v]) => (
                  <option key={k} value={k}>
                    {v.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <button type="submit" disabled={obsLoading} className="sk-btn-primary w-full">
            {obsLoading ? "..." : t.soilHealth.observeButton}
          </button>
        </form>

        {/* Observation Interpretation Output */}
        <div className="sk-surface-card rounded-2xl p-6 space-y-4 lg:col-span-6">
          {obsResult ? (
            <>
              <div className="flex items-center justify-between border-b border-ink/10 pb-3">
                <div className="flex items-center gap-2.5">
                  <img src={`/soils/${obsResult.soil_color}.svg`} alt="" className="h-9 w-14 rounded-md object-cover border border-ink/10" />
                  <div>
                    <h3 className="text-base font-semibold text-ink">
                      {lang === "kn" ? obsResult.soil_color_label_kn : obsResult.soil_color_label_en}
                    </h3>
                    <p className="font-mono text-xs text-accent">
                      Drainage: {obsResult.effective_drainage.replace(/_/g, " ")}
                    </p>
                  </div>
                </div>
                <span className="rounded-md border border-accent/35 bg-accent/10 px-2.5 py-0.5 font-mono text-xs uppercase text-accent">
                  {obsResult.observation_confidence}
                </span>
              </div>

              <div className="space-y-2 text-sm text-secondary">
                {(lang === "kn" ? obsResult.insights_kn : obsResult.insights_en).map((line, i) => (
                  <p key={i} className="flex items-start gap-2">
                    <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-accent" />
                    <span>{line}</span>
                  </p>
                ))}
              </div>

              <div className="rounded-xl border border-ink/10 bg-elevated/40 p-4 space-y-2">
                <p className="text-xs font-semibold uppercase tracking-wide text-muted">Practical Field Management</p>
                {(lang === "kn" ? obsResult.management_guidance_kn : obsResult.management_guidance_en).map((m, i) => (
                  <p key={i} className="text-sm text-ink">
                    • {m}
                  </p>
                ))}
              </div>

              <div className="rounded-lg border border-warning/35 bg-warning/10 p-3 text-xs text-ink flex items-start gap-2">
                <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-warning" />
                <span>{lang === "kn" ? obsResult.color_disclaimer_kn : obsResult.color_disclaimer_en}</span>
              </div>
              <p className="text-xs text-muted">{lang === "kn" ? obsResult.optional_lab_note_kn : obsResult.optional_lab_note_en}</p>
            </>
          ) : (
            <div className="flex h-full flex-col justify-center space-y-3 py-8 text-center">
              <Info className="mx-auto h-8 w-8 text-accent" />
              <p className="text-sm font-medium text-ink">{t.soilHealth.shcFutureTitle}</p>
              <p className="mx-auto max-w-md text-xs text-secondary">{t.soilHealth.shcFutureBody}</p>
            </div>
          )}
        </div>
      </div>

      {/* Collapsible Secondary Optional Soil Health Card Lab Interpreter */}
      <section className="sk-surface-card rounded-2xl p-6 space-y-4">
        <button
          type="button"
          onClick={() => setShowOptionalLab((p) => !p)}
          className="flex w-full items-center justify-between text-left"
        >
          <div className="flex items-center gap-2.5">
            <FlaskConical className="h-5 w-5 text-accent" aria-hidden="true" />
            <div>
              <h2 className="text-base font-semibold text-ink">{t.soilHealth.optionalLabTitle}</h2>
              <p className="text-xs text-secondary">{t.soilHealth.optionalLabSubtitle}</p>
            </div>
          </div>
          {showOptionalLab ? <ChevronUp className="h-5 w-5 text-muted" /> : <ChevronDown className="h-5 w-5 text-muted" />}
        </button>

        {showOptionalLab && (
          <div className="border-t border-ink/10 pt-5 grid gap-6 lg:grid-cols-12">
            <form onSubmit={handleLabSubmit} className="lg:col-span-5 space-y-4">
              {labError && <ErrorAlert message={labError} />}
              <div>
                <label className="block text-xs font-medium text-secondary">Soil Group</label>
                <select
                  value={soilType}
                  onChange={(e) => setSoilType(e.target.value as SoilTypeOption)}
                  className="sk-input mt-1"
                >
                  {["Red", "Black", "Alluvial", "Laterite", "Sandy", "Loamy", "Clay"].map((st) => (
                    <option key={st} value={st}>
                      {st}
                    </option>
                  ))}
                </select>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs text-secondary">pH (0-14)</label>
                  <input type="number" step="0.1" value={ph} onChange={(e) => setPh(e.target.value)} className="sk-input mt-1 font-mono" />
                </div>
                <div>
                  <label className="block text-xs text-secondary">N (kg/ha)</label>
                  <input type="number" step="1" value={nitrogen} onChange={(e) => setNitrogen(e.target.value)} className="sk-input mt-1 font-mono" />
                </div>
                <div>
                  <label className="block text-xs text-secondary">P (kg/ha)</label>
                  <input type="number" step="1" value={phosphorus} onChange={(e) => setPhosphorus(e.target.value)} className="sk-input mt-1 font-mono" />
                </div>
                <div>
                  <label className="block text-xs text-secondary">K (kg/ha)</label>
                  <input type="number" step="1" value={potassium} onChange={(e) => setPotassium(e.target.value)} className="sk-input mt-1 font-mono" />
                </div>
              </div>
              <button type="submit" className="sk-btn-secondary w-full">
                {t.soilHealth.analyzeButton}
              </button>
            </form>

            <div className="lg:col-span-7 space-y-3">
              {labResult ? (
                <>
                  <p className="text-sm font-medium text-ink">
                    {lang === "kn" ? labResult.overview_kn : labResult.overview_en}
                  </p>
                  <div className="grid gap-2.5 sm:grid-cols-2">
                    {labResult.interpretations.map((item) => (
                      <div key={item.parameter} className="rounded-lg border border-ink/10 bg-elevated/40 p-3 text-xs">
                        <div className="flex justify-between font-semibold text-ink">
                          <span>{item.parameter}</span>
                          <span className="text-accent">{item.status}</span>
                        </div>
                        <p className="mt-1 text-secondary">
                          {lang === "kn" ? item.interpretation_kn : item.interpretation_en}
                        </p>
                      </div>
                    ))}
                  </div>
                  <p className="text-xs text-muted">
                    {lang === "kn" ? labResult.fertilizer_caution_kn : labResult.fertilizer_caution_en}
                  </p>
                </>
              ) : (
                <p className="text-xs text-muted">
                  Enter optional Soil Health Card laboratory measurements only if you already have a printed lab report.
                </p>
              )}
            </div>
          </div>
        )}
      </section>
    </div>
  );
}
