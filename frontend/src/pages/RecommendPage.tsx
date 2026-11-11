import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, ArrowRight, Check, CloudRain, FlaskConical, MapPin, Tractor, Info } from "lucide-react";
import { apiClient, ApiError } from "../api/client";
import { ErrorAlert } from "../components/ErrorAlert";
import { useI18n } from "../i18n";
import type {
  DistrictItem,
  FarmingMethodOption,
  IrrigationOption,
  RecommendationPayload,
  SeasonOption,
  SoilTypeOption,
  TalukItem,
  WaterAvailabilityOption,
} from "../types";

const SOIL_TYPES: SoilTypeOption[] = ["Red", "Black", "Alluvial", "Laterite", "Sandy", "Loamy", "Clay"];
const SEASONS: SeasonOption[] = ["Kharif", "Rabi", "Zaid", "Perennial"];
const IRRIGATION_TYPES: IrrigationOption[] = [
  "Rainfed",
  "Borewell",
  "Canal",
  "Drip",
  "Sprinkler",
  "Tank / Open Well",
];
const WATER_LEVELS: WaterAvailabilityOption[] = [
  "Rainfed",
  "Limited irrigation",
  "Moderate irrigation",
  "Assured irrigation",
];
const FARMING_METHODS: FarmingMethodOption[] = [
  "Integrated (INM/IPM)",
  "Conventional",
  "Organic / Natural",
  "Mixed / Multi-crop",
];

export function RecommendPage() {
  const { lang, t } = useI18n();
  const navigate = useNavigate();

  const [step, setStep] = useState(0);

  // Location state
  const [states, setStates] = useState<string[]>(["Karnataka"]);
  const [selectedState, setSelectedState] = useState("Karnataka");
  const [districts, setDistricts] = useState<DistrictItem[]>([]);
  const [selectedDistrict, setSelectedDistrict] = useState("");
  const [taluks, setTaluks] = useState<TalukItem[]>([]);
  const [selectedTaluk, setSelectedTaluk] = useState("");
  const [village, setVillage] = useState("");

  // Soil state
  const [soilType, setSoilType] = useState<SoilTypeOption>("Red");
  const [soilDataAvailable, setSoilDataAvailable] = useState(true);
  const [soilSource, setSoilSource] = useState<"soil_test" | "estimate">("estimate");
  const [soilTestDate, setSoilTestDate] = useState("");
  const [ph, setPh] = useState("6.5");
  const [nitrogen, setNitrogen] = useState("55");
  const [phosphorus, setPhosphorus] = useState("38");
  const [potassium, setPotassium] = useState("35");

  // Farming state
  const [season, setSeason] = useState<SeasonOption>("Kharif");
  const [irrigationType, setIrrigationType] = useState<IrrigationOption>("Rainfed");
  const [waterAvailability, setWaterAvailability] = useState<WaterAvailabilityOption>("Rainfed");
  const [landArea, setLandArea] = useState("2");
  const [farmingMethod, setFarmingMethod] = useState<FarmingMethodOption>("Integrated (INM/IPM)");
  const [previousCrop, setPreviousCrop] = useState("");

  // Climate state
  const [temperature, setTemperature] = useState("26");
  const [humidity, setHumidity] = useState("68");
  const [rainfall, setRainfall] = useState("740");
  const [climateSource, setClimateSource] = useState<"measured" | "estimate" | "reference">("estimate");

  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [loadingLocations, setLoadingLocations] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  // Load states & districts
  useEffect(() => {
    apiClient
      .getStates()
      .then((res) => {
        if (res.states.length > 0) {
          setStates(res.states);
          setSelectedState(res.states[0]);
        }
      })
      .catch(() => {
        // Keep Karnataka default if API call fails transiently; submit will report error clearly
      });
  }, []);

  useEffect(() => {
    if (!selectedState) return;
    setLoadingLocations(true);
    apiClient
      .getDistricts(selectedState)
      .then((res) => {
        setDistricts(res.districts);
        if (res.districts.length > 0) {
          const defaultDist =
            res.districts.find((d) => d.district === "Bengaluru Rural")?.district || res.districts[0].district;
          setSelectedDistrict((prev) =>
            res.districts.some((d) => d.district === prev) ? prev : defaultDist
          );
        } else {
          setSelectedDistrict("");
        }
      })
      .catch((err) => {
        setSubmitError(err instanceof Error ? err.message : "Could not load districts.");
      })
      .finally(() => setLoadingLocations(false));
  }, [selectedState]);

  useEffect(() => {
    if (!selectedState || !selectedDistrict) {
      setTaluks([]);
      setSelectedTaluk("");
      return;
    }
    apiClient
      .getTaluks(selectedState, selectedDistrict)
      .then((res) => {
        setTaluks(res.taluks);
        if (res.taluks.length > 0) {
          setSelectedTaluk((prev) =>
            res.taluks.some((tk) => tk.taluk === prev) ? prev : res.taluks[0].taluk
          );
        } else {
          setSelectedTaluk("");
        }
      })
      .catch(() => {
        setTaluks([]);
        setSelectedTaluk("");
      });
  }, [selectedState, selectedDistrict]);

  const activeTaluk = taluks.find((item) => item.taluk === selectedTaluk);

  const validateStep = (stepIndex: number): boolean => {
    const errors: Record<string, string> = {};

    if (stepIndex === 0) {
      if (!selectedState) errors.state = "Please select a state.";
      if (!selectedDistrict) errors.district = "Please select a district.";
      if (!selectedTaluk) errors.taluk = "Please select a taluk.";
    }

    if (stepIndex === 1 && soilDataAvailable) {
      if (ph.trim() !== "") {
        const val = Number(ph);
        if (Number.isNaN(val) || val < 0 || val > 14) errors.ph = "Soil pH must be between 0 and 14.";
      }
      if (nitrogen.trim() !== "") {
        const val = Number(nitrogen);
        if (Number.isNaN(val) || val < 0 || val > 500) errors.nitrogen = "Nitrogen must be between 0 and 500 kg/ha.";
      }
      if (phosphorus.trim() !== "") {
        const val = Number(phosphorus);
        if (Number.isNaN(val) || val < 0 || val > 500) errors.phosphorus = "Phosphorus must be between 0 and 500 kg/ha.";
      }
      if (potassium.trim() !== "") {
        const val = Number(potassium);
        if (Number.isNaN(val) || val < 0 || val > 600) errors.potassium = "Potassium must be between 0 and 600 kg/ha.";
      }
    }

    if (stepIndex === 2) {
      const area = Number(landArea);
      if (Number.isNaN(area) || area <= 0 || area > 1000) {
        errors.landArea = "Land area must be greater than 0 and up to 1000 acres.";
      }
    }

    if (stepIndex === 3) {
      if (temperature.trim() !== "") {
        const val = Number(temperature);
        if (Number.isNaN(val) || val < -5 || val > 60) errors.temperature = "Temperature must be between -5°C and 60°C.";
      }
      if (humidity.trim() !== "") {
        const val = Number(humidity);
        if (Number.isNaN(val) || val < 0 || val > 100) errors.humidity = "Humidity must be between 0% and 100%.";
      }
      if (rainfall.trim() !== "") {
        const val = Number(rainfall);
        if (Number.isNaN(val) || val < 0 || val > 5000) errors.rainfall = "Rainfall must be between 0 and 5000 mm.";
      }
    }

    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleNext = () => {
    if (validateStep(step)) {
      setStep((s) => Math.min(3, s + 1));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateStep(3)) return;

    setSubmitting(true);
    setSubmitError(null);

    const parseOptNum = (raw: string): number | null => {
      const trimmed = raw.trim();
      return trimmed === "" ? null : Number(trimmed);
    };

    const payload: RecommendationPayload = {
      state: selectedState,
      district: selectedDistrict,
      taluk: selectedTaluk,
      village: village.trim() || null,
      agro_climatic_zone: activeTaluk?.agro_climatic_zone || null,
      soil_type: soilType,
      soil_data_available: soilDataAvailable,
      soil_measurement_source: soilDataAvailable ? soilSource : "unavailable",
      soil_test_date: soilDataAvailable && soilTestDate ? soilTestDate : null,
      ph: soilDataAvailable ? parseOptNum(ph) : null,
      nitrogen: soilDataAvailable ? parseOptNum(nitrogen) : null,
      phosphorus: soilDataAvailable ? parseOptNum(phosphorus) : null,
      potassium: soilDataAvailable ? parseOptNum(potassium) : null,
      season,
      irrigation_type: irrigationType,
      water_availability: waterAvailability,
      land_area_acres: Number(landArea),
      farming_method: farmingMethod,
      previous_crop: previousCrop.trim() || null,
      temperature: parseOptNum(temperature),
      humidity: parseOptNum(humidity),
      rainfall: parseOptNum(rainfall),
      climate_source: climateSource,
      language: lang,
    };

    try {
      const result = await apiClient.createRecommendation(payload);
      sessionStorage.setItem("smartkrishi_latest_rec", JSON.stringify(result));
      navigate(`/results/${result.recommendation_id}`, { state: { result } });
    } catch (err) {
      if (err instanceof ApiError) {
        setSubmitError(err.message);
        if (err.fieldErrors) setFieldErrors(err.fieldErrors);
      } else {
        setSubmitError("Unable to reach the recommendation service. Check that the backend server is running.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  const steps = [
    { label: t.form.stepLocation, icon: MapPin },
    { label: t.form.stepSoil, icon: FlaskConical },
    { label: t.form.stepFarming, icon: Tractor },
    { label: t.form.stepClimate, icon: CloudRain },
  ];

  return (
    <div className="mx-auto max-w-4xl px-4 py-10 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold tracking-tight text-ink sm:text-3xl">{t.form.pageTitle}</h1>
        <p className="mt-2 text-sm text-secondary sm:text-base">{t.form.pageSubtitle}</p>
      </div>

      {/* Stepper indicator */}
      <nav aria-label="Recommendation form sections" className="mb-8 grid grid-cols-2 gap-2.5 sm:grid-cols-4">
        {steps.map((item, idx) => {
          const Icon = item.icon;
          const isCurrent = idx === step;
          const isDone = idx < step;
          return (
            <button
              key={item.label}
              type="button"
              onClick={() => {
                if (idx <= step || validateStep(step)) setStep(idx);
              }}
              aria-current={isCurrent ? "step" : undefined}
              className={`flex items-center gap-2.5 rounded-lg border p-3 text-left text-sm transition-colors min-h-[48px] ${
                isCurrent
                  ? "border-accent bg-elevated text-ink font-semibold"
                  : isDone
                  ? "border-accent/40 bg-surface text-accent"
                  : "border-white/10 bg-surface text-secondary hover:bg-elevated/60"
              }`}
            >
              {isDone ? (
                <Check className="h-4 w-4 shrink-0 text-accent" aria-hidden="true" />
              ) : (
                <Icon className={`h-4 w-4 shrink-0 ${isCurrent ? "text-accent" : "text-muted"}`} aria-hidden="true" />
              )}
              <span className="text-xs sm:text-sm leading-snug">{item.label}</span>
            </button>
          );
        })}
      </nav>

      {submitError && (
        <div className="mb-6">
          <ErrorAlert title="Submission Error" message={submitError} />
        </div>
      )}

      <form onSubmit={handleSubmit} className="sk-surface-card rounded-xl p-6 sm:p-8 space-y-6" noValidate>
        {/* SECTION A: LOCATION */}
        {step === 0 && (
          <div className="space-y-5">
            <h2 className="text-lg font-semibold text-ink">{t.form.stepLocation}</h2>
            <div className="grid gap-5 sm:grid-cols-2">
              <div>
                <label htmlFor="state" className="block text-sm font-medium text-secondary mb-1.5">
                  {t.form.state}
                </label>
                <select
                  id="state"
                  className="sk-input"
                  value={selectedState}
                  onChange={(e) => setSelectedState(e.target.value)}
                  aria-invalid={Boolean(fieldErrors.state)}
                >
                  {states.map((st) => (
                    <option key={st} value={st}>
                      {st}
                    </option>
                  ))}
                </select>
                {fieldErrors.state && <p className="mt-1 text-xs text-danger">{fieldErrors.state}</p>}
              </div>

              <div>
                <label htmlFor="district" className="block text-sm font-medium text-secondary mb-1.5">
                  {t.form.district}
                </label>
                <select
                  id="district"
                  className="sk-input"
                  value={selectedDistrict}
                  disabled={loadingLocations || districts.length === 0}
                  onChange={(e) => setSelectedDistrict(e.target.value)}
                  aria-invalid={Boolean(fieldErrors.district)}
                  aria-describedby={fieldErrors.district ? "district-error" : undefined}
                >
                  {districts.length === 0 && <option value="">{t.form.selectOption}</option>}
                  {districts.map((d) => (
                    <option key={d.district} value={d.district}>
                      {d.district}
                    </option>
                  ))}
                </select>
                {fieldErrors.district && (
                  <p id="district-error" className="mt-1 text-xs text-danger">
                    {fieldErrors.district}
                  </p>
                )}
              </div>

              <div>
                <label htmlFor="taluk" className="block text-sm font-medium text-secondary mb-1.5">
                  {t.form.taluk}
                </label>
                <select
                  id="taluk"
                  className="sk-input"
                  value={selectedTaluk}
                  disabled={taluks.length === 0}
                  onChange={(e) => setSelectedTaluk(e.target.value)}
                  aria-invalid={Boolean(fieldErrors.taluk)}
                  aria-describedby={fieldErrors.taluk ? "taluk-error" : undefined}
                >
                  {taluks.length === 0 && <option value="">{t.form.selectOption}</option>}
                  {taluks.map((tk) => (
                    <option key={tk.id} value={tk.taluk}>
                      {tk.taluk}
                    </option>
                  ))}
                </select>
                {fieldErrors.taluk && (
                  <p id="taluk-error" className="mt-1 text-xs text-danger">
                    {fieldErrors.taluk}
                  </p>
                )}
              </div>

              <div>
                <label htmlFor="village" className="block text-sm font-medium text-secondary mb-1.5">
                  {t.form.village}
                </label>
                <input
                  id="village"
                  type="text"
                  className="sk-input"
                  value={village}
                  onChange={(e) => setVillage(e.target.value)}
                  placeholder="Optional"
                />
              </div>
            </div>

            {activeTaluk && (
              <div className="rounded-lg border border-accent/25 bg-canvas/80 p-4 text-sm space-y-1">
                <p className="text-secondary">
                  <span className="font-medium text-ink">{t.form.agroZone}:</span>{" "}
                  <span className="text-accent font-medium">
                    {activeTaluk.agro_climatic_zone} ({activeTaluk.zone_code})
                  </span>
                </p>
                {activeTaluk.normal_annual_rainfall_mm && (
                  <p className="text-xs text-muted font-mono tabular-nums">
                    {t.form.talukRefHint}: {activeTaluk.normal_annual_rainfall_mm} mm/year · Dominant soils:{" "}
                    {activeTaluk.dominant_soil_types.join(", ")}
                  </p>
                )}
              </div>
            )}
          </div>
        )}

        {/* SECTION B: SOIL INFORMATION */}
        {step === 1 && (
          <div className="space-y-5">
            <h2 className="text-lg font-semibold text-ink">{t.form.stepSoil}</h2>

            <div className="grid gap-5 sm:grid-cols-2">
              <div>
                <label htmlFor="soilType" className="block text-sm font-medium text-secondary mb-1.5">
                  {t.form.soilType}
                </label>
                <select
                  id="soilType"
                  className="sk-input"
                  value={soilType}
                  onChange={(e) => setSoilType(e.target.value as SoilTypeOption)}
                >
                  {SOIL_TYPES.map((st) => (
                    <option key={st} value={st}>
                      {st} soil
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex items-end">
                <label className="flex items-center gap-3 rounded-lg border border-white/15 bg-canvas/70 px-4 py-2.5 min-h-[44px] w-full cursor-pointer">
                  <input
                    type="checkbox"
                    checked={soilDataAvailable}
                    onChange={(e) => setSoilDataAvailable(e.target.checked)}
                    className="h-4 w-4 accent-accent"
                  />
                  <span className="text-sm text-ink">{t.form.soilDataToggle}</span>
                </label>
              </div>
            </div>

            {!soilDataAvailable ? (
              <div className="flex items-start gap-3 rounded-lg border border-warning/35 bg-warning/10 p-4 text-sm text-secondary">
                <Info className="mt-0.5 h-4 w-4 shrink-0 text-warning" aria-hidden="true" />
                <p>{t.form.soilUnavailableNote}</p>
              </div>
            ) : (
              <>
                <div className="grid gap-5 sm:grid-cols-2">
                  <div>
                    <label htmlFor="soilSource" className="block text-sm font-medium text-secondary mb-1.5">
                      {t.form.soilSource}
                    </label>
                    <select
                      id="soilSource"
                      className="sk-input"
                      value={soilSource}
                      onChange={(e) => setSoilSource(e.target.value as "soil_test" | "estimate")}
                    >
                      <option value="soil_test">{t.form.soilSourceTest}</option>
                      <option value="estimate">{t.form.soilSourceEstimate}</option>
                    </select>
                  </div>

                  <div>
                    <label htmlFor="soilTestDate" className="block text-sm font-medium text-secondary mb-1.5">
                      {t.form.soilTestDate}
                    </label>
                    <input
                      id="soilTestDate"
                      type="date"
                      className="sk-input"
                      value={soilTestDate}
                      onChange={(e) => setSoilTestDate(e.target.value)}
                    />
                  </div>
                </div>

                <div className="grid gap-5 sm:grid-cols-2">
                  <div>
                    <label htmlFor="ph" className="block text-sm font-medium text-secondary mb-1.5">
                      {t.form.ph}
                    </label>
                    <input
                      id="ph"
                      type="number"
                      step="0.1"
                      className="sk-input font-mono tabular-nums"
                      value={ph}
                      onChange={(e) => setPh(e.target.value)}
                      aria-invalid={Boolean(fieldErrors.ph)}
                      aria-describedby={fieldErrors.ph ? "ph-error" : undefined}
                    />
                    {fieldErrors.ph && (
                      <p id="ph-error" className="mt-1 text-xs text-danger">
                        {fieldErrors.ph}
                      </p>
                    )}
                  </div>

                  <div>
                    <label htmlFor="nitrogen" className="block text-sm font-medium text-secondary mb-1.5">
                      {t.form.nitrogen}
                    </label>
                    <input
                      id="nitrogen"
                      type="number"
                      step="1"
                      className="sk-input font-mono tabular-nums"
                      value={nitrogen}
                      onChange={(e) => setNitrogen(e.target.value)}
                      aria-invalid={Boolean(fieldErrors.nitrogen)}
                      aria-describedby={fieldErrors.nitrogen ? "nitrogen-error" : undefined}
                    />
                    {fieldErrors.nitrogen && (
                      <p id="nitrogen-error" className="mt-1 text-xs text-danger">
                        {fieldErrors.nitrogen}
                      </p>
                    )}
                  </div>

                  <div>
                    <label htmlFor="phosphorus" className="block text-sm font-medium text-secondary mb-1.5">
                      {t.form.phosphorus}
                    </label>
                    <input
                      id="phosphorus"
                      type="number"
                      step="1"
                      className="sk-input font-mono tabular-nums"
                      value={phosphorus}
                      onChange={(e) => setPhosphorus(e.target.value)}
                      aria-invalid={Boolean(fieldErrors.phosphorus)}
                      aria-describedby={fieldErrors.phosphorus ? "phosphorus-error" : undefined}
                    />
                    {fieldErrors.phosphorus && (
                      <p id="phosphorus-error" className="mt-1 text-xs text-danger">
                        {fieldErrors.phosphorus}
                      </p>
                    )}
                  </div>

                  <div>
                    <label htmlFor="potassium" className="block text-sm font-medium text-secondary mb-1.5">
                      {t.form.potassium}
                    </label>
                    <input
                      id="potassium"
                      type="number"
                      step="1"
                      className="sk-input font-mono tabular-nums"
                      value={potassium}
                      onChange={(e) => setPotassium(e.target.value)}
                      aria-invalid={Boolean(fieldErrors.potassium)}
                      aria-describedby={fieldErrors.potassium ? "potassium-error" : undefined}
                    />
                    {fieldErrors.potassium && (
                      <p id="potassium-error" className="mt-1 text-xs text-danger">
                        {fieldErrors.potassium}
                      </p>
                    )}
                  </div>
                </div>
              </>
            )}
          </div>
        )}

        {/* SECTION C: FARMING CONDITIONS */}
        {step === 2 && (
          <div className="space-y-5">
            <h2 className="text-lg font-semibold text-ink">{t.form.stepFarming}</h2>
            <div className="grid gap-5 sm:grid-cols-2">
              <div>
                <label htmlFor="season" className="block text-sm font-medium text-secondary mb-1.5">
                  {t.form.season}
                </label>
                <select
                  id="season"
                  className="sk-input"
                  value={season}
                  onChange={(e) => setSeason(e.target.value as SeasonOption)}
                >
                  {SEASONS.map((s) => (
                    <option key={s} value={s}>
                      {s}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="waterAvailability" className="block text-sm font-medium text-secondary mb-1.5">
                  {t.form.waterAvailability}
                </label>
                <select
                  id="waterAvailability"
                  className="sk-input"
                  value={waterAvailability}
                  onChange={(e) => setWaterAvailability(e.target.value as WaterAvailabilityOption)}
                >
                  {WATER_LEVELS.map((w) => (
                    <option key={w} value={w}>
                      {w}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="irrigationType" className="block text-sm font-medium text-secondary mb-1.5">
                  {t.form.irrigationType}
                </label>
                <select
                  id="irrigationType"
                  className="sk-input"
                  value={irrigationType}
                  onChange={(e) => setIrrigationType(e.target.value as IrrigationOption)}
                >
                  {IRRIGATION_TYPES.map((ir) => (
                    <option key={ir} value={ir}>
                      {ir}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="landArea" className="block text-sm font-medium text-secondary mb-1.5">
                  {t.form.landArea}
                </label>
                <input
                  id="landArea"
                  type="number"
                  step="0.25"
                  className="sk-input font-mono tabular-nums"
                  value={landArea}
                  onChange={(e) => setLandArea(e.target.value)}
                  aria-invalid={Boolean(fieldErrors.landArea)}
                  aria-describedby={fieldErrors.landArea ? "landArea-error" : undefined}
                />
                {fieldErrors.landArea && (
                  <p id="landArea-error" className="mt-1 text-xs text-danger">
                    {fieldErrors.landArea}
                  </p>
                )}
              </div>

              <div>
                <label htmlFor="farmingMethod" className="block text-sm font-medium text-secondary mb-1.5">
                  {t.form.farmingMethod}
                </label>
                <select
                  id="farmingMethod"
                  className="sk-input"
                  value={farmingMethod}
                  onChange={(e) => setFarmingMethod(e.target.value as FarmingMethodOption)}
                >
                  {FARMING_METHODS.map((fm) => (
                    <option key={fm} value={fm}>
                      {fm}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="previousCrop" className="block text-sm font-medium text-secondary mb-1.5">
                  {t.form.previousCrop}
                </label>
                <input
                  id="previousCrop"
                  type="text"
                  className="sk-input"
                  value={previousCrop}
                  onChange={(e) => setPreviousCrop(e.target.value)}
                  placeholder="e.g., Ragi, Maize, Fallow"
                />
              </div>
            </div>
          </div>
        )}

        {/* SECTION D: CLIMATIC CONDITIONS */}
        {step === 3 && (
          <div className="space-y-5">
            <h2 className="text-lg font-semibold text-ink">{t.form.stepClimate}</h2>

            <div className="flex items-start gap-3 rounded-lg border border-info/30 bg-info/10 p-4 text-sm text-secondary">
              <Info className="mt-0.5 h-4 w-4 shrink-0 text-info" aria-hidden="true" />
              <p>{t.form.climateNoLiveWarning}</p>
            </div>

            <div className="grid gap-5 sm:grid-cols-2">
              <div>
                <label htmlFor="climateSource" className="block text-sm font-medium text-secondary mb-1.5">
                  {t.form.climateSource}
                </label>
                <select
                  id="climateSource"
                  className="sk-input"
                  value={climateSource}
                  onChange={(e) => setClimateSource(e.target.value as "measured" | "estimate" | "reference")}
                >
                  <option value="estimate">{t.form.climateSourceEstimate}</option>
                  <option value="measured">{t.form.climateSourceMeasured}</option>
                  <option value="reference">{t.form.climateSourceReference}</option>
                </select>
              </div>

              <div>
                <label htmlFor="temperature" className="block text-sm font-medium text-secondary mb-1.5">
                  {t.form.temperature}
                </label>
                <input
                  id="temperature"
                  type="number"
                  step="0.5"
                  className="sk-input font-mono tabular-nums"
                  value={temperature}
                  onChange={(e) => setTemperature(e.target.value)}
                  aria-invalid={Boolean(fieldErrors.temperature)}
                  aria-describedby={fieldErrors.temperature ? "temp-error" : undefined}
                />
                {fieldErrors.temperature && (
                  <p id="temp-error" className="mt-1 text-xs text-danger">
                    {fieldErrors.temperature}
                  </p>
                )}
              </div>

              <div>
                <label htmlFor="humidity" className="block text-sm font-medium text-secondary mb-1.5">
                  {t.form.humidity}
                </label>
                <input
                  id="humidity"
                  type="number"
                  step="1"
                  className="sk-input font-mono tabular-nums"
                  value={humidity}
                  onChange={(e) => setHumidity(e.target.value)}
                  aria-invalid={Boolean(fieldErrors.humidity)}
                  aria-describedby={fieldErrors.humidity ? "humidity-error" : undefined}
                />
                {fieldErrors.humidity && (
                  <p id="humidity-error" className="mt-1 text-xs text-danger">
                    {fieldErrors.humidity}
                  </p>
                )}
              </div>

              <div>
                <label htmlFor="rainfall" className="block text-sm font-medium text-secondary mb-1.5">
                  {t.form.rainfall}
                </label>
                <input
                  id="rainfall"
                  type="number"
                  step="10"
                  className="sk-input font-mono tabular-nums"
                  value={rainfall}
                  onChange={(e) => setRainfall(e.target.value)}
                  aria-invalid={Boolean(fieldErrors.rainfall)}
                  aria-describedby={fieldErrors.rainfall ? "rainfall-error" : undefined}
                />
                {fieldErrors.rainfall && (
                  <p id="rainfall-error" className="mt-1 text-xs text-danger">
                    {fieldErrors.rainfall}
                  </p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Navigation controls */}
        <div className="flex flex-col-reverse gap-3 border-t border-white/10 pt-6 sm:flex-row sm:justify-between">
          {step > 0 ? (
            <button
              type="button"
              onClick={() => setStep((s) => Math.max(0, s - 1))}
              className="sk-btn-secondary"
            >
              <ArrowLeft className="h-4 w-4" aria-hidden="true" />
              <span>{t.form.back}</span>
            </button>
          ) : (
            <div />
          )}

          {step < 3 ? (
            <button type="button" onClick={handleNext} className="sk-btn-primary">
              <span>{t.form.next}</span>
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </button>
          ) : (
            <button type="submit" disabled={submitting} className="sk-btn-primary">
              <span>{submitting ? t.form.submitting : t.form.submit}</span>
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </button>
          )}
        </div>
      </form>
    </div>
  );
}
