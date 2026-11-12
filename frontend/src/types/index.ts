export type Language = "en" | "kn";

export interface HealthStatus {
  status: string;
  service: string;
  engine_mode: string;
  database_connected: boolean;
  ml_model_loaded: boolean;
  ml_model_version: string | null;
  record_counts: Record<string, number>;
}

export interface DistrictItem {
  district: string;
  agro_climatic_zone: string;
  zone_code: string;
  taluk_count: number;
}

export interface TalukItem {
  id: number;
  taluk: string;
  agro_climatic_zone: string;
  zone_code: string;
  normal_annual_rainfall_mm: number | null;
  typical_rainfall_pattern: string;
  dominant_soil_types: string[];
  common_soil_textures: string[];
  major_crops: string[];
  recommended_seasons_summary: Record<string, string>;
  growing_period_info: string;
  regional_references: string[];
  data_source: string;
  verification_status: string;
  last_updated: string;
}

export interface CropSummary {
  id: number;
  crop_key: string;
  name_en: string;
  name_kn: string;
  scientific_name: string;
  category: string;
  image_asset: string;
  growing_duration_days_min: number;
  growing_duration_days_max: number;
  duration_category: string;
  water_requirement_level: string;
  water_requirement_mm_min: number;
  water_requirement_mm_max: number;
  seed_rate_kg_per_acre: string;
  record_status: string;
  verification_status: string;
  last_updated: string;
  in_ml_dataset: boolean;
  suitable_seasons: string[];
  suitable_soil_types: string[];
  suitable_textures: string[];
}

export interface CropEconomic {
  region_scope: string;
  season: string;
  seed_cost_inr_per_acre: number | null;
  cultivation_cost_min_inr_per_acre: number | null;
  cultivation_cost_max_inr_per_acre: number | null;
  expected_yield_qtl_min: number | null;
  expected_yield_qtl_max: number | null;
  indicative_price_inr_per_qtl: number | null;
  assumptions_en: string;
  assumptions_kn: string;
  data_status: string;
  source: string;
}

export interface CropDetail extends CropSummary {
  cultivation_guidance_en: string;
  cultivation_guidance_kn: string;
  information_source: string;
  requirement: {
    suitable_soil_types: string[];
    suitable_textures: string[];
    suitable_drainage: string[];
    moisture_needs: string;
    suitable_land_topography: string[];
    min_soil_depth: string;
    drought_tolerance: string;
    waterlogging_tolerance: string;
    sowing_months: string[];
    temp_min_c: number;
    temp_max_c: number;
    humidity_min_pct: number;
    humidity_max_pct: number;
    rainfall_min_mm: number;
    rainfall_max_mm: number;
    suitable_seasons: string[];
    supported_water_levels: string[];
  };
  economic_data: CropEconomic[];
}

export type SoilTypeOption = "Red" | "Black" | "Alluvial" | "Laterite" | "Sandy" | "Loamy" | "Clay";

export type SoilColorOption =
  | "red"
  | "reddish_brown"
  | "dark_black"
  | "brown"
  | "yellowish"
  | "grey"
  | "sandy_pale"
  | "mixed_uncertain";

export type SoilTextureOption = "sandy" | "clayey" | "loamy" | "silty" | "mixed" | "not_sure";
export type DrainageOption = "very_quickly" | "moderately" | "remains_hours" | "remains_days" | "not_sure";
export type MoistureRetentionOption = "dries_quickly" | "short_period" | "several_days" | "not_sure";
export type LandTopographyOption = "flat" | "slightly_sloping" | "steep_hilly" | "low_lying" | "rocky_stony";
export type SoilDepthOption = "shallow" | "medium" | "deep" | "unknown";
export type VisibleStonesOption = "none_few" | "moderate" | "many_stony" | "not_sure";
export type WaterloggingIssueOption = "none" | "occasional" | "frequent" | "not_sure";
export type ErosionIssueOption = "none" | "mild" | "severe" | "not_sure";
export type WaterSourceOption =
  | "rainfed"
  | "borewell"
  | "open_well"
  | "canal"
  | "pond_reservoir"
  | "drip_irrigation"
  | "multiple_sources";
export type WaterReliabilityOption = "throughout_season" | "certain_months" | "limited" | "uncertain";
export type SeasonOption = "Kharif" | "Rabi" | "Zaid" | "Perennial";
export type DurationPreferenceOption = "short" | "long" | "flexible";
export type FarmingPriorityOption =
  | "low_water"
  | "short_duration"
  | "land_suitability"
  | "household_food"
  | "commercial";

export interface RecommendationPayload {
  state: string;
  district: string;
  taluk: string;
  village?: string | null;

  soil_color: SoilColorOption;
  soil_texture: SoilTextureOption;
  drainage_after_rain: DrainageOption;
  moisture_retention: MoistureRetentionOption;

  land_topography: LandTopographyOption;
  soil_depth: SoilDepthOption;
  visible_stones: VisibleStonesOption;
  waterlogging_issue: WaterloggingIssueOption;
  erosion_issue: ErosionIssueOption;

  water_source: WaterSourceOption;
  water_reliability: WaterReliabilityOption;

  previous_crop?: string | null;
  previous_crop_success?: "yes" | "partial" | "no" | "not_sure" | null;
  drought_history?: "yes" | "no" | "uncertain" | null;
  flood_history?: "yes" | "no" | "uncertain" | null;
  pest_disease_history?: string | null;
  land_area_acres?: number | null;

  season: SeasonOption;
  intended_sowing_month?: string | null;
  duration_preference: DurationPreferenceOption;
  farming_priority: FarmingPriorityOption;
  language: Language;
}

export interface DimensionScores {
  location: number;
  soil_land: number;
  water: number;
  seasonal: number;
  climate: number;
  priority_history: number;
}

export interface RecommendedCropResult {
  rank: number;
  crop_id: number;
  crop_key: string;
  name_en: string;
  name_kn: string;
  scientific_name: string;
  category: string;
  image_asset: string;
  suitability_category: string;
  illustrative_score: number;
  dimension_scores: DimensionScores;
  reasons_en: string[];
  reasons_kn: string[];
  limitations_en: string[];
  limitations_kn: string[];
  missing_info_en: string[];
  missing_info_kn: string[];
  compatibility_badges: Record<string, string>;
  conflict_flags: string[];
  water_requirement_level: string;
  water_requirement_mm_min: number;
  water_requirement_mm_max: number;
  suitable_seasons: string[];
  growing_duration_days_min: number;
  growing_duration_days_max: number;
  cultivation_guidance_en: string;
  cultivation_guidance_kn: string;
  information_source: string;
  record_status: string;
}

export interface SoilObservationResult {
  soil_color: SoilColorOption;
  soil_color_label_en: string;
  soil_color_label_kn: string;
  color_disclaimer_en: string;
  color_disclaimer_kn: string;
  soil_texture: SoilTextureOption;
  effective_drainage: string;
  effective_moisture_retention: string;
  soil_depth: SoilDepthOption;
  visible_stones: VisibleStonesOption;
  waterlogging_issue: WaterloggingIssueOption;
  erosion_issue: ErosionIssueOption;
  observation_confidence: "high" | "moderate" | "low";
  unknown_fields: string[];
  insights_en: string[];
  insights_kn: string[];
  management_guidance_en: string[];
  management_guidance_kn: string[];
  optional_lab_note_en: string;
  optional_lab_note_kn: string;
}

export interface WeatherIntelligence {
  long_term_climate: {
    status: string;
    data_category: string;
    zone_name: string;
    zone_code: string;
    normal_annual_rainfall_mm: number | null;
    typical_rainfall_pattern: string;
    season_reference: string;
    season_normal_temp_c: number;
    season_normal_humidity_pct: number;
    season_normal_rainfall_mm: number;
    growing_period_info: string;
    source: string;
    verification_status: string;
    last_updated: string;
  };
  current_weather: {
    status: "available" | "unavailable";
    data_category: string;
    provider: string;
    observed_at?: string;
    temperature_c: number | null;
    humidity_pct: number | null;
    precipitation_mm: number | null;
    wind_speed_kmh?: number | null;
    reason_en?: string;
    reason_kn?: string;
    disclaimer_en?: string;
    disclaimer_kn?: string;
    official_links?: Array<{ name: string; url: string }>;
  };
  short_term_forecast: {
    status: "available" | "unavailable";
    data_category: string;
    provider: string;
    next_7_days_rain_total_mm: number | null;
    peak_daily_rain_mm: number | null;
    temp_max_c?: number | null;
    temp_min_c?: number | null;
    reason_en?: string;
    reason_kn?: string;
  };
  seasonal_outlook: {
    status: string;
    data_category: string;
    outlook_summary_en: string;
    outlook_summary_kn: string;
    recommended_window_en: string;
    recommended_window_kn: string;
    limitation_en: string;
    limitation_kn: string;
  };
  farming_advisory: {
    advisory_basis: string;
    live_weather_available: boolean;
    sowing_suitability_en: string;
    sowing_suitability_kn: string;
    heavy_rainfall_risk_level: "low" | "moderate" | "high";
    heavy_rainfall_risk_en: string;
    heavy_rainfall_risk_kn: string;
    dry_spell_risk_level: "low" | "moderate" | "high";
    dry_spell_risk_en: string;
    dry_spell_risk_kn: string;
    irrigation_planning_en: string;
    irrigation_planning_kn: string;
  };
}

export interface RecommendationResponse {
  recommendation_id: number;
  created_at: string;
  mode_used: string;
  confidence_level: string;
  scoring_notice_en: string;
  scoring_notice_kn: string;
  disclaimer_en: string;
  disclaimer_kn: string;
  warnings: string[];
  missing_information: string[];
  insufficient_data_reason: string | null;
  location_context: {
    state: string;
    district: string;
    taluk: string;
    agro_climatic_zone: string;
    zone_code: string;
    normal_annual_rainfall_mm: number | null;
    typical_rainfall_pattern: string;
    dominant_soil_types: string[];
    common_soil_textures: string[];
    major_crops: string[];
    recommended_seasons_summary: Record<string, string>;
    growing_period_info: string;
    regional_references: string[];
    data_source: string;
    verification_status: string;
    last_updated: string;
  };
  soil_interpretation: SoilObservationResult;
  weather_advisory: WeatherIntelligence;
  input_provenance: {
    farmer_observed: { label: string; fields: string[] };
    institution_sourced: { label: string; sources: string[]; location_verification_status: string; location_last_updated: string };
    weather_provider_sourced: { label: string; current_weather_status: string; short_term_forecast_status: string; provider: string };
    demonstration_data: { label: string; note: string };
  };
  input_summary: Record<string, unknown>;
  recommendations: RecommendedCropResult[];
}

export interface ComparedCropItem {
  crop_id: number;
  crop_key: string;
  name_en: string;
  name_kn: string;
  category: string;
  image_asset: string;
  suitable_soil_types: string[];
  ph_range: string;
  water_requirement_level: string;
  water_requirement_mm_range: string;
  suitable_seasons: string[];
  growing_duration_days_range: string;
  temperature_range_c: string;
  humidity_range_pct: string;
  rainfall_range_mm: string;
  seed_rate_kg_per_acre: string;
  economic_data_status: string;
  economic_available: boolean;
  seed_cost_inr_total: number | null;
  cultivation_cost_min_total: number | null;
  cultivation_cost_max_total: number | null;
  expected_yield_qtl_min_total: number | null;
  expected_yield_qtl_max_total: number | null;
  indicative_price_inr_per_qtl: number | null;
  gross_revenue_min_total: number | null;
  gross_revenue_max_total: number | null;
  net_return_min_total: number | null;
  net_return_max_total: number | null;
  assumptions_en: string | null;
  assumptions_kn: string | null;
  economic_source: string | null;
  information_source: string;
}

export interface CompareCropsResponse {
  land_area_acres: number;
  disclaimer_en: string;
  disclaimer_kn: string;
  crops: ComparedCropItem[];
}

export interface SoilAnalysisResponse {
  soil_type: string;
  measurement_source: string;
  overview_en: string;
  overview_kn: string;
  interpretations: Array<{
    parameter: string;
    value: number | null;
    unit: string;
    status: string;
    interpretation_en: string;
    interpretation_kn: string;
    reference_range: string;
  }>;
  guidance_en: string[];
  guidance_kn: string[];
  fertilizer_caution_en: string;
  fertilizer_caution_kn: string;
}

export interface KnowledgeArticleSummary {
  id: number;
  slug: string;
  category: string;
  title_en: string;
  title_kn: string;
  summary_en: string;
  summary_kn: string;
  source_name: string;
  source_url: string | null;
  updated_at: string;
}

export interface KnowledgeArticleDetail extends KnowledgeArticleSummary {
  content_en: string;
  content_kn: string;
}

export interface AdminOverview {
  admin_username: string;
  engine_mode?: string;
  dataset_provenance: Record<string, unknown>;
  dataset_validation: Record<string, unknown>;
  ml_metrics: {
    model_type: string;
    train_samples: number;
    test_samples: number;
    num_classes: number;
    test_accuracy: number;
    macro_precision: number;
    macro_recall: number;
    macro_f1: number;
    cv_macro_f1_mean: number;
    cv_macro_f1_std: number;
    feature_importances: Record<string, number>;
  } | null;
  recent_recommendations: Array<{
    id: number;
    mode_used: string;
    confidence_level: string;
    district: string | null;
    season: string | null;
    created_at: string;
  }>;
  feedback: Array<{
    id: number;
    category: string;
    rating: number | null;
    district: string | null;
    comment: string;
    review_status: string;
    admin_notes: string | null;
    created_at: string;
  }>;
  regional_rules: Array<{
    id: number;
    crop_id: number;
    state: string;
    agro_climatic_zone: string | null;
    season: string;
    suitability_level: string;
    rule_notes_en: string;
    source: string;
    is_active: boolean;
  }>;
}
