import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  ArrowRight,
  Calendar,
  Check,
  CloudRain,
  Compass,
  Droplets,
  HelpCircle,
  History,
  Info,
  Loader2,
  MapPin,
  Mountain,
  Sprout,
} from "lucide-react";
import { apiClient, ApiError } from "../api/client";
import { ErrorAlert } from "../components/ErrorAlert";
import { useI18n } from "../i18n";
import type {
  DistrictItem,
  DrainageOption,
  DurationPreferenceOption,
  ErosionIssueOption,
  FarmingPriorityOption,
  LandTopographyOption,
  MoistureRetentionOption,
  RecommendationPayload,
  SeasonOption,
  SoilColorOption,
  SoilDepthOption,
  SoilTextureOption,
  TalukItem,
  VisibleStonesOption,
  WaterloggingIssueOption,
  WaterReliabilityOption,
  WaterSourceOption,
} from "../types";

const TOTAL_STEPS = 8;

const SOIL_COLORS: SoilColorOption[] = [
  "red",
  "reddish_brown",
  "dark_black",
  "brown",
  "yellowish",
  "grey",
  "sandy_pale",
  "mixed_uncertain",
];

const SOIL_TEXTURES: SoilTextureOption[] = ["sandy", "clayey", "loamy", "silty", "mixed", "not_sure"];
const DRAINAGES: DrainageOption[] = ["very_quickly", "moderately", "remains_hours", "remains_days", "not_sure"];
const MOISTURES: MoistureRetentionOption[] = ["dries_quickly", "short_period", "several_days", "not_sure"];
const TOPOGRAPHIES: LandTopographyOption[] = ["flat", "slightly_sloping", "steep_hilly", "low_lying", "rocky_stony"];
const DEPTHS: SoilDepthOption[] = ["shallow", "medium", "deep", "unknown"];
const STONES: VisibleStonesOption[] = ["none_few", "moderate", "many_stony", "not_sure"];
const WATERLOGS: WaterloggingIssueOption[] = ["none", "occasional", "frequent", "not_sure"];
const EROSIONS: ErosionIssueOption[] = ["none", "mild", "severe", "not_sure"];
const WATER_SOURCES: WaterSourceOption[] = [
  "rainfed",
  "borewell",
  "open_well",
  "canal",
  "pond_reservoir",
  "drip_irrigation",
  "multiple_sources",
];
const WATER_RELIABILITIES: WaterReliabilityOption[] = [
  "throughout_season",
  "certain_months",
  "limited",
  "uncertain",
];
const SEASONS: SeasonOption[] = ["Kharif", "Rabi", "Zaid", "Perennial"];
const MONTHS = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];
const DURATIONS: DurationPreferenceOption[] = ["short", "long", "flexible"];
const PRIORITIES: FarmingPriorityOption[] = [
  "low_water",
  "short_duration",
  "land_suitability",
  "household_food",
  "commercial",
];

export function RecommendPage() {
  const { lang, t } = useI18n();
  const navigate = useNavigate();

  const [step, setStep] = useState(1);
  const [submitting, setSubmitting] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);
  const [stepError, setStepError] = useState<string | null>(null);

  // Location cascade
  const [states, setStates] = useState<string[]>(["Karnataka"]);
  const [stateName, setStateName] = useState("Karnataka");
  const [districts, setDistricts] = useState<DistrictItem[]>([]);
  const [district, setDistrict] = useState("");
  const [taluks, setTaluks] = useState<TalukItem[]>([]);
  const [taluk, setTaluk] = useState("");
  const [village, setVillage] = useState("");

  // Step 2 & 3: Soil Appearance & Texture
  const [soilColor, setSoilColor] = useState<SoilColorOption>("red");
  const [soilTexture, setSoilTexture] = useState<SoilTextureOption>("loamy");
  const [showTextureGuide, setShowTextureGuide] = useState(false);

  // Step 4: Water Drainage & Retention
  const [drainageAfterRain, setDrainageAfterRain] = useState<DrainageOption>("moderately");
  const [moistureRetention, setMoistureRetention] = useState<MoistureRetentionOption>("short_period");

  // Step 5: Land Characteristics
  const [landTopography, setLandTopography] = useState<LandTopographyOption>("flat");
  const [soilDepth, setSoilDepth] = useState<SoilDepthOption>("medium");
  const [visibleStones, setVisibleStones] = useState<VisibleStonesOption>("none_few");
  const [waterloggingIssue, setWaterloggingIssue] = useState<WaterloggingIssueOption>("none");
  const [erosionIssue, setErosionIssue] = useState<ErosionIssueOption>("none");

  // Step 6: Water Availability
  const [waterSource, setWaterSource] = useState<WaterSourceOption>("rainfed");
  const [waterReliability, setWaterReliability] = useState<WaterReliabilityOption>("certain_months");

  // Step 7: Optional Farming History
  const [previousCrop, setPreviousCrop] = useState("");
  const [previousCropSuccess, setPreviousCropSuccess] = useState<"" | "yes" | "partial" | "no" | "not_sure">("");
  const [droughtHistory, setDroughtHistory] = useState<"" | "yes" | "no" | "uncertain">("");
  const [floodHistory, setFloodHistory] = useState<"" | "yes" | "no" | "uncertain">("");
  const [pestHistory, setPestHistory] = useState("");
  const [landAreaAcres, setLandAreaAcres] = useState("");

  // Step 8: Season & Planning
  const [season, setSeason] = useState<SeasonOption>("Kharif");
  const [intendedMonth, setIntendedMonth] = useState("June");
  const [durationPreference, setDurationPreference] = useState<DurationPreferenceOption>("flexible");
  const [farmingPriority, setFarmingPriority] = useState<FarmingPriorityOption>("land_suitability");

  useEffect(() => {
    apiClient
      .getStates()
      .then((res) => {
        if (res.states.length > 0) {
          setStates(res.states);
          setStateName(res.states[0]);
        }
      })
      .catch(() => setStates(["Karnataka"]));
  }, []);

  useEffect(() => {
    if (!stateName) return;
    apiClient
      .getDistricts(stateName)
      .then((res) => {
        setDistricts(res.districts);
        if (res.districts.length > 0) {
          const preferred = res.districts.find((d) => d.district === "Tumakuru") || res.districts[0];
          setDistrict(preferred.district);
        }
      })
      .catch((err) => setApiError(err instanceof Error ? err.message : "Could not load districts."));
  }, [stateName]);

  useEffect(() => {
    if (!stateName || !district) return;
    apiClient
      .getTaluks(stateName, district)
      .then((res) => {
        setTaluks(res.taluks);
        if (res.taluks.length > 0) {
          setTaluk(res.taluks[0].taluk);
        }
      })
      .catch((err) => setApiError(err instanceof Error ? err.message : "Could not load taluks."));
  }, [stateName, district]);

  const selectedTalukObj = taluks.find((item) => item.taluk === taluk) || null;

  const validateCurrentStep = (): boolean => {
    setStepError(null);
    if (step === 1 && (!district || !taluk)) {
      setStepError(lang === "kn" ? "ದಯವಿಟ್ಟು ಜಿಲ್ಲೆ ಮತ್ತು ತಾಲೂಕು ಆಯ್ಕೆಮಾಡಿ." : "Please select both District and Taluk.");
      return false;
    }
    if (step === 7 && landAreaAcres.trim() !== "") {
      const area = Number(landAreaAcres);
      if (Number.isNaN(area) || area <= 0 || area > 1000) {
        setStepError(lang === "kn" ? "ವಿಸ್ತೀರ್ಣ 0.1 ರಿಂದ 1000 ಎಕರೆ ನಡುವೆ ಇರಬೇಕು." : "Land size must be between 0.1 and 1000 acres.");
        return false;
      }
    }
    return true;
  };

  const handleNext = () => {
    if (!validateCurrentStep()) return;
    setStep((s) => Math.min(TOTAL_STEPS, s + 1));
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleBack = () => {
    setStepError(null);
    setStep((s) => Math.max(1, s - 1));
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateCurrentStep()) return;

    setSubmitting(true);
    setApiError(null);

    const payload: RecommendationPayload = {
      state: stateName,
      district,
      taluk,
      village: village.trim() || null,
      soil_color: soilColor,
      soil_texture: soilTexture,
      drainage_after_rain: drainageAfterRain,
      moisture_retention: moistureRetention,
      land_topography: landTopography,
      soil_depth: soilDepth,
      visible_stones: visibleStones,
      waterlogging_issue: waterloggingIssue,
      erosion_issue: erosionIssue,
      water_source: waterSource,
      water_reliability: waterReliability,
      previous_crop: previousCrop.trim() || null,
      previous_crop_success: previousCropSuccess || null,
      drought_history: droughtHistory || null,
      flood_history: floodHistory || null,
      pest_disease_history: pestHistory.trim() || null,
      land_area_acres: landAreaAcres.trim() ? Number(landAreaAcres) : null,
      season,
      intended_sowing_month: intendedMonth || null,
      duration_preference: durationPreference,
      farming_priority: farmingPriority,
      language: lang,
    };

    try {
      const result = await apiClient.createRecommendation(payload);
      navigate(`/results/${result.recommendation_id}`, { state: { recommendation: result } });
    } catch (err) {
      if (err instanceof ApiError) {
        setApiError(err.message);
      } else {
        setApiError("Unable to reach the advisory server. Please check backend connectivity.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  const stepMeta = [
    { key: "location", icon: MapPin, copy: t.wizard.steps.location },
    { key: "soilColor", icon: Compass, copy: t.wizard.steps.soilColor },
    { key: "soilTexture", icon: Sprout, copy: t.wizard.steps.soilTexture },
    { key: "drainage", icon: CloudRain, copy: t.wizard.steps.drainage },
    { key: "land", icon: Mountain, copy: t.wizard.steps.land },
    { key: "water", icon: Droplets, copy: t.wizard.steps.water },
    { key: "history", icon: History, copy: t.wizard.steps.history },
    { key: "season", icon: Calendar, copy: t.wizard.steps.season },
  ][step - 1];

  const StepIcon = stepMeta.icon;
  const pct = Math.round((step / TOTAL_STEPS) * 100);

  return (
    <div className="mx-auto max-w-4xl px-4 py-10 sm:px-6 lg:px-8">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight text-ink sm:text-3xl">{t.wizard.pageTitle}</h1>
        <p className="mt-2 text-sm text-secondary sm:text-base">{t.wizard.pageSubtitle}</p>
      </div>

      {/* Smooth 8-Step Progress Header */}
      <div className="mb-6 rounded-xl border border-ink/10 bg-surface p-4">
        <div className="flex items-center justify-between text-xs font-medium text-secondary">
          <span className="flex items-center gap-2 text-ink">
            <StepIcon className="h-4 w-4 text-accent" aria-hidden="true" />
            {t.wizard.stepOf.replace("{current}", String(step)).replace("{total}", String(TOTAL_STEPS))} —{" "}
            <strong className="font-semibold text-accent">{stepMeta.copy.title}</strong>
          </span>
          <span className="font-mono tabular-nums text-muted">{pct}%</span>
        </div>
        <div className="mt-3 h-2 w-full overflow-hidden rounded-full bg-ink/10">
          <div
            className="h-full rounded-full bg-accent transition-all duration-300 ease-out"
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>

      {apiError && (
        <div className="mb-5">
          <ErrorAlert message={apiError} />
        </div>
      )}
      {stepError && (
        <div className="mb-5">
          <ErrorAlert message={stepError} />
        </div>
      )}

      <form onSubmit={handleSubmit} noValidate className="sk-surface-card rounded-2xl p-6 sm:p-8">
        <div key={step} className="sk-step-enter space-y-6">
          <div className="border-b border-ink/10 pb-4">
            <h2 className="text-lg font-semibold text-ink sm:text-xl">{stepMeta.copy.title}</h2>
            <p className="mt-1 text-sm text-secondary">{stepMeta.copy.subtitle}</p>
          </div>

          {/* STEP 1: LOCATION */}
          {step === 1 && (
            <div className="space-y-6">
              <div className="grid gap-4 sm:grid-cols-2">
                <div>
                  <label htmlFor="state" className="block text-sm font-medium text-ink">
                    {t.wizard.fields.state}
                  </label>
                  <select
                    id="state"
                    value={stateName}
                    onChange={(e) => setStateName(e.target.value)}
                    className="sk-input mt-1.5"
                  >
                    {states.map((st) => (
                      <option key={st} value={st}>
                        {st}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label htmlFor="district" className="block text-sm font-medium text-ink">
                    {t.wizard.fields.district}
                  </label>
                  <select
                    id="district"
                    value={district}
                    onChange={(e) => setDistrict(e.target.value)}
                    className="sk-input mt-1.5"
                  >
                    {districts.map((d) => (
                      <option key={d.district} value={d.district}>
                        {d.district}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label htmlFor="taluk" className="block text-sm font-medium text-ink">
                    {t.wizard.fields.taluk}
                  </label>
                  <select
                    id="taluk"
                    value={taluk}
                    onChange={(e) => setTaluk(e.target.value)}
                    className="sk-input mt-1.5"
                  >
                    {taluks.map((tl) => (
                      <option key={tl.id} value={tl.taluk}>
                        {tl.taluk}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label htmlFor="village" className="block text-sm font-medium text-ink">
                    {t.wizard.fields.village}
                  </label>
                  <input
                    id="village"
                    type="text"
                    value={village}
                    onChange={(e) => setVillage(e.target.value)}
                    placeholder={lang === "kn" ? "ಉದಾ: ಹೆಬ್ಬೂರು" : "e.g., Hebbur"}
                    className="sk-input mt-1.5"
                  />
                </div>
              </div>

              {selectedTalukObj && (
                <div className="rounded-xl border border-accent/30 bg-accent/10 p-5 space-y-3">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div>
                      <p className="text-xs font-medium text-muted">{t.wizard.fields.agroZone}</p>
                      <p className="text-base font-semibold text-ink">
                        {selectedTalukObj.agro_climatic_zone}{" "}
                        <span className="font-mono text-xs text-accent">({selectedTalukObj.zone_code})</span>
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-muted">{t.wizard.fields.zoneRefHint}</p>
                      <p className="font-mono text-sm font-semibold text-ink tabular-nums">
                        {selectedTalukObj.normal_annual_rainfall_mm ?? "—"} mm / yr
                      </p>
                    </div>
                  </div>
                  <p className="text-xs text-secondary">{selectedTalukObj.typical_rainfall_pattern}</p>
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    <span className="text-xs font-medium text-ink mr-1">{t.wizard.fields.majorCropsLabel}:</span>
                    {selectedTalukObj.major_crops.map((c) => (
                      <span
                        key={c}
                        className="rounded-md border border-ink/15 bg-surface px-2 py-0.5 text-xs text-secondary"
                      >
                        {c}
                      </span>
                    ))}
                  </div>
                  <p className="text-[11px] text-muted">
                    {selectedTalukObj.data_source} · Updated {selectedTalukObj.last_updated}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* STEP 2: SOIL APPEARANCE */}
          {step === 2 && (
            <div className="space-y-5">
              <p className="text-base font-medium text-ink">{t.wizard.steps.soilColor.question}</p>
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                {SOIL_COLORS.map((key) => {
                  const selected = soilColor === key;
                  const copy = t.wizard.colors[key];
                  return (
                    <button
                      key={key}
                      type="button"
                      onClick={() => setSoilColor(key)}
                      aria-pressed={selected}
                      className={`sk-choice-card flex flex-col rounded-xl p-3 text-left ${
                        selected ? "border-accent ring-2 ring-accent/40 bg-elevated" : ""
                      }`}
                    >
                      <img
                        src={`/soils/${key}.svg`}
                        alt={copy.label}
                        className="h-20 w-full rounded-lg object-cover border border-ink/10"
                      />
                      <div className="mt-2.5 flex items-center justify-between gap-1">
                        <span className="text-sm font-semibold text-ink">{copy.label}</span>
                        {selected && <Check className="h-4 w-4 text-accent shrink-0" />}
                      </div>
                      {copy.desc && <span className="mt-0.5 text-xs text-secondary">{copy.desc}</span>}
                    </button>
                  );
                })}
              </div>
              <div className="flex items-start gap-2.5 rounded-lg border border-warning/35 bg-warning/10 p-3.5 text-xs text-ink">
                <Info className="mt-0.5 h-4 w-4 shrink-0 text-warning" aria-hidden="true" />
                <span>{t.wizard.steps.soilColor.disclaimer}</span>
              </div>
            </div>
          )}

          {/* STEP 3: SOIL TEXTURE */}
          {step === 3 && (
            <div className="space-y-5">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <p className="text-base font-medium text-ink">{t.wizard.steps.soilTexture.question}</p>
                <button
                  type="button"
                  onClick={() => setShowTextureGuide((prev) => !prev)}
                  className="inline-flex items-center gap-1.5 rounded-lg border border-accent/35 bg-accent/10 px-3 py-1.5 text-xs font-semibold text-accent hover:bg-accent/20 transition-colors"
                >
                  <HelpCircle className="h-3.5 w-3.5" aria-hidden="true" />
                  <span>{t.wizard.steps.soilTexture.guideTitle}</span>
                </button>
              </div>

              {showTextureGuide && (
                <div className="rounded-xl border border-info/35 bg-info/10 p-4 text-xs leading-relaxed text-ink space-y-2">
                  <p className="font-semibold">{t.wizard.steps.soilTexture.guideTitle}</p>
                  <p className="text-secondary">{t.wizard.steps.soilTexture.guideBody}</p>
                </div>
              )}

              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {SOIL_TEXTURES.map((key) => {
                  const selected = soilTexture === key;
                  const copy = t.wizard.textures[key];
                  return (
                    <button
                      key={key}
                      type="button"
                      onClick={() => setSoilTexture(key)}
                      aria-pressed={selected}
                      className={`sk-choice-card flex flex-col items-start rounded-xl p-4 text-left ${
                        selected ? "border-accent ring-2 ring-accent/40 bg-elevated" : ""
                      }`}
                    >
                      <div className="flex w-full items-center justify-between">
                        <span className="text-sm font-semibold text-ink">{copy.label}</span>
                        {selected && <Check className="h-4 w-4 text-accent" />}
                      </div>
                      {copy.desc && <span className="mt-1.5 text-xs text-secondary">{copy.desc}</span>}
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* STEP 4: WATER DRAINAGE & MOISTURE RETENTION */}
          {step === 4 && (
            <div className="space-y-6">
              <div>
                <p className="text-base font-medium text-ink mb-3">{t.wizard.steps.drainage.qRain}</p>
                <div className="grid gap-3 sm:grid-cols-2">
                  {DRAINAGES.map((key) => {
                    const selected = drainageAfterRain === key;
                    const copy = t.wizard.drainages[key];
                    return (
                      <button
                        key={key}
                        type="button"
                        onClick={() => setDrainageAfterRain(key)}
                        aria-pressed={selected}
                        className={`sk-choice-card rounded-xl p-4 text-left ${
                          selected ? "border-accent ring-2 ring-accent/40 bg-elevated" : ""
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-semibold text-ink">{copy.label}</span>
                          {selected && <Check className="h-4 w-4 text-accent shrink-0" />}
                        </div>
                        {copy.desc && <p className="mt-1 text-xs text-secondary">{copy.desc}</p>}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div>
                <p className="text-base font-medium text-ink mb-3">{t.wizard.steps.drainage.qMoisture}</p>
                <div className="grid gap-3 sm:grid-cols-2">
                  {MOISTURES.map((key) => {
                    const selected = moistureRetention === key;
                    const copy = t.wizard.moistures[key];
                    return (
                      <button
                        key={key}
                        type="button"
                        onClick={() => setMoistureRetention(key)}
                        aria-pressed={selected}
                        className={`sk-choice-card rounded-xl p-4 text-left ${
                          selected ? "border-accent ring-2 ring-accent/40 bg-elevated" : ""
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-semibold text-ink">{copy.label}</span>
                          {selected && <Check className="h-4 w-4 text-accent shrink-0" />}
                        </div>
                        {copy.desc && <p className="mt-1 text-xs text-secondary">{copy.desc}</p>}
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {/* STEP 5: LAND CHARACTERISTICS */}
          {step === 5 && (
            <div className="space-y-6">
              <div>
                <p className="text-sm font-semibold text-ink mb-2.5">{t.wizard.steps.land.qTopo}</p>
                <div className="grid gap-2.5 sm:grid-cols-3">
                  {TOPOGRAPHIES.map((key) => {
                    const selected = landTopography === key;
                    return (
                      <button
                        key={key}
                        type="button"
                        onClick={() => setLandTopography(key)}
                        aria-pressed={selected}
                        className={`sk-choice-card flex items-center justify-between rounded-xl px-4 py-3 text-left text-sm font-medium ${
                          selected ? "border-accent ring-2 ring-accent/40 bg-elevated text-ink" : "text-secondary"
                        }`}
                      >
                        <span>{t.wizard.topographies[key].label}</span>
                        {selected && <Check className="h-4 w-4 text-accent shrink-0" />}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="grid gap-5 sm:grid-cols-2">
                <div>
                  <label htmlFor="soilDepth" className="block text-sm font-medium text-ink">
                    {t.wizard.steps.land.qDepth}
                  </label>
                  <select
                    id="soilDepth"
                    value={soilDepth}
                    onChange={(e) => setSoilDepth(e.target.value as SoilDepthOption)}
                    className="sk-input mt-1.5"
                  >
                    {DEPTHS.map((d) => (
                      <option key={d} value={d}>
                        {t.wizard.depths[d].label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label htmlFor="visibleStones" className="block text-sm font-medium text-ink">
                    {t.wizard.steps.land.qStones}
                  </label>
                  <select
                    id="visibleStones"
                    value={visibleStones}
                    onChange={(e) => setVisibleStones(e.target.value as VisibleStonesOption)}
                    className="sk-input mt-1.5"
                  >
                    {STONES.map((s) => (
                      <option key={s} value={s}>
                        {t.wizard.stones[s].label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label htmlFor="waterlogging" className="block text-sm font-medium text-ink">
                    {t.wizard.steps.land.qWaterlog}
                  </label>
                  <select
                    id="waterlogging"
                    value={waterloggingIssue}
                    onChange={(e) => setWaterloggingIssue(e.target.value as WaterloggingIssueOption)}
                    className="sk-input mt-1.5"
                  >
                    {WATERLOGS.map((w) => (
                      <option key={w} value={w}>
                        {t.wizard.waterlogs[w].label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label htmlFor="erosion" className="block text-sm font-medium text-ink">
                    {t.wizard.steps.land.qErosion}
                  </label>
                  <select
                    id="erosion"
                    value={erosionIssue}
                    onChange={(e) => setErosionIssue(e.target.value as ErosionIssueOption)}
                    className="sk-input mt-1.5"
                  >
                    {EROSIONS.map((er) => (
                      <option key={er} value={er}>
                        {t.wizard.erosions[er].label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* STEP 6: WATER AVAILABILITY */}
          {step === 6 && (
            <div className="space-y-6">
              <div>
                <p className="text-base font-medium text-ink mb-3">{t.wizard.steps.water.qSource}</p>
                <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                  {WATER_SOURCES.map((key) => {
                    const selected = waterSource === key;
                    return (
                      <button
                        key={key}
                        type="button"
                        onClick={() => setWaterSource(key)}
                        aria-pressed={selected}
                        className={`sk-choice-card flex items-center justify-between rounded-xl px-4 py-3.5 text-left text-sm font-medium ${
                          selected ? "border-accent ring-2 ring-accent/40 bg-elevated text-ink" : "text-secondary"
                        }`}
                      >
                        <span>{t.wizard.waterSources[key].label}</span>
                        {selected && <Check className="h-4 w-4 text-accent shrink-0" />}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div>
                <p className="text-base font-medium text-ink mb-3">{t.wizard.steps.water.qReliability}</p>
                <div className="grid gap-3 sm:grid-cols-2">
                  {WATER_RELIABILITIES.map((key) => {
                    const selected = waterReliability === key;
                    return (
                      <button
                        key={key}
                        type="button"
                        onClick={() => setWaterReliability(key)}
                        aria-pressed={selected}
                        className={`sk-choice-card flex items-center justify-between rounded-xl px-4 py-3.5 text-left text-sm font-medium ${
                          selected ? "border-accent ring-2 ring-accent/40 bg-elevated text-ink" : "text-secondary"
                        }`}
                      >
                        <span>{t.wizard.waterReliabilities[key].label}</span>
                        {selected && <Check className="h-4 w-4 text-accent shrink-0" />}
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {/* STEP 7: FARMING HISTORY (ALL OPTIONAL) */}
          {step === 7 && (
            <div className="grid gap-5 sm:grid-cols-2">
              <div>
                <label htmlFor="previousCrop" className="block text-sm font-medium text-ink">
                  {t.wizard.steps.history.qPrevCrop}
                </label>
                <input
                  id="previousCrop"
                  type="text"
                  value={previousCrop}
                  onChange={(e) => setPreviousCrop(e.target.value)}
                  placeholder={t.wizard.fields.prevCropPlaceholder}
                  className="sk-input mt-1.5"
                />
              </div>

              <div>
                <label htmlFor="prevSuccess" className="block text-sm font-medium text-ink">
                  {t.wizard.steps.history.qSuccess}
                </label>
                <select
                  id="prevSuccess"
                  value={previousCropSuccess}
                  onChange={(e) => setPreviousCropSuccess(e.target.value as "" | "yes" | "partial" | "no" | "not_sure")}
                  className="sk-input mt-1.5"
                >
                  <option value="">{t.wizard.optionalBadge}</option>
                  {Object.entries(t.wizard.successOptions).map(([val, label]) => (
                    <option key={val} value={val}>
                      {label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="droughtHist" className="block text-sm font-medium text-ink">
                  {t.wizard.steps.history.qDrought}
                </label>
                <select
                  id="droughtHist"
                  value={droughtHistory}
                  onChange={(e) => setDroughtHistory(e.target.value as "" | "yes" | "no" | "uncertain")}
                  className="sk-input mt-1.5"
                >
                  <option value="">{t.wizard.optionalBadge}</option>
                  {Object.entries(t.wizard.yesNoUncertain).map(([val, label]) => (
                    <option key={val} value={val}>
                      {label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="floodHist" className="block text-sm font-medium text-ink">
                  {t.wizard.steps.history.qFlood}
                </label>
                <select
                  id="floodHist"
                  value={floodHistory}
                  onChange={(e) => setFloodHistory(e.target.value as "" | "yes" | "no" | "uncertain")}
                  className="sk-input mt-1.5"
                >
                  <option value="">{t.wizard.optionalBadge}</option>
                  {Object.entries(t.wizard.yesNoUncertain).map(([val, label]) => (
                    <option key={val} value={val}>
                      {label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="pestHistory" className="block text-sm font-medium text-ink">
                  {t.wizard.steps.history.qPests}
                </label>
                <input
                  id="pestHistory"
                  type="text"
                  value={pestHistory}
                  onChange={(e) => setPestHistory(e.target.value)}
                  placeholder={t.wizard.fields.pestPlaceholder}
                  className="sk-input mt-1.5"
                />
              </div>

              <div>
                <label htmlFor="landArea" className="block text-sm font-medium text-ink">
                  {t.wizard.steps.history.qArea}
                </label>
                <input
                  id="landArea"
                  type="number"
                  min={0.1}
                  max={1000}
                  step="0.1"
                  value={landAreaAcres}
                  onChange={(e) => setLandAreaAcres(e.target.value)}
                  placeholder={t.wizard.fields.areaPlaceholder}
                  className="sk-input mt-1.5 font-mono tabular-nums"
                />
              </div>
            </div>
          )}

          {/* STEP 8: SEASON & PLANNING */}
          {step === 8 && (
            <div className="space-y-6">
              <div>
                <p className="text-sm font-semibold text-ink mb-2.5">{t.wizard.steps.season.qSeason}</p>
                <div className="grid gap-3 sm:grid-cols-2">
                  {SEASONS.map((s) => {
                    const selected = season === s;
                    return (
                      <button
                        key={s}
                        type="button"
                        onClick={() => setSeason(s)}
                        aria-pressed={selected}
                        className={`sk-choice-card flex items-center justify-between rounded-xl px-4 py-3 text-left text-sm font-medium ${
                          selected ? "border-accent ring-2 ring-accent/40 bg-elevated text-ink" : "text-secondary"
                        }`}
                      >
                        <span>{t.wizard.seasons[s].label}</span>
                        {selected && <Check className="h-4 w-4 text-accent shrink-0" />}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <div>
                  <label htmlFor="sowingMonth" className="block text-sm font-medium text-ink">
                    {t.wizard.steps.season.qMonth}
                  </label>
                  <select
                    id="sowingMonth"
                    value={intendedMonth}
                    onChange={(e) => setIntendedMonth(e.target.value)}
                    className="sk-input mt-1.5"
                  >
                    <option value="">{t.wizard.fields.monthAny}</option>
                    {MONTHS.map((m) => (
                      <option key={m} value={m}>
                        {m}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label htmlFor="durationPref" className="block text-sm font-medium text-ink">
                    {t.wizard.steps.season.qDuration}
                  </label>
                  <select
                    id="durationPref"
                    value={durationPreference}
                    onChange={(e) => setDurationPreference(e.target.value as DurationPreferenceOption)}
                    className="sk-input mt-1.5"
                  >
                    {DURATIONS.map((d) => (
                      <option key={d} value={d}>
                        {t.wizard.durations[d].label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <p className="text-sm font-semibold text-ink mb-2.5">{t.wizard.steps.season.qPriority}</p>
                <div className="grid gap-3 sm:grid-cols-2">
                  {PRIORITIES.map((key) => {
                    const selected = farmingPriority === key;
                    const copy = t.wizard.priorities[key];
                    return (
                      <button
                        key={key}
                        type="button"
                        onClick={() => setFarmingPriority(key)}
                        aria-pressed={selected}
                        className={`sk-choice-card rounded-xl p-3.5 text-left ${
                          selected ? "border-accent ring-2 ring-accent/40 bg-elevated" : ""
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-semibold text-ink">{copy.label}</span>
                          {selected && <Check className="h-4 w-4 text-accent shrink-0" />}
                        </div>
                        {copy.desc && <p className="mt-1 text-xs text-secondary">{copy.desc}</p>}
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Navigation Buttons */}
        <div className="mt-8 flex items-center justify-between border-t border-ink/10 pt-5">
          {step > 1 ? (
            <button type="button" onClick={handleBack} className="sk-btn-secondary">
              <ArrowLeft className="h-4 w-4" aria-hidden="true" />
              <span>{t.wizard.back}</span>
            </button>
          ) : (
            <div />
          )}

          {step < TOTAL_STEPS ? (
            <button type="button" onClick={handleNext} className="sk-btn-primary">
              <span>{t.wizard.next}</span>
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </button>
          ) : (
            <button type="submit" disabled={submitting} className="sk-btn-primary">
              {submitting ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
                  <span>{t.wizard.submitting}</span>
                </>
              ) : (
                <>
                  <span>{t.wizard.submit}</span>
                  <ArrowRight className="h-4 w-4" aria-hidden="true" />
                </>
              )}
            </button>
          )}
        </div>
      </form>
    </div>
  );
}
