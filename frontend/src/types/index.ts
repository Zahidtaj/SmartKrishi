export type Language = "en" | "kn";

export interface HealthStatus {
  status: string;
  service: string;
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
  dominant_soil_types: string[];
  data_source: string;
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
  water_requirement_level: string;
  water_requirement_mm_min: number;
  water_requirement_mm_max: number;
  seed_rate_kg_per_acre: string;
  record_status: string;
  in_ml_dataset: boolean;
  suitable_seasons: string[];
  suitable_soil_types: string[];
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
    ph_min: number;
    ph_max: number;
    ph_optimal_min: number;
    ph_optimal_max: number;
    nitrogen_min: number;
    nitrogen_max: number;
    phosphorus_min: number;
    phosphorus_max: number;
    potassium_min: number;
    potassium_max: number;
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
export type SeasonOption = "Kharif" | "Rabi" | "Zaid" | "Perennial";
export type IrrigationOption = "Rainfed" | "Borewell" | "Canal" | "Drip" | "Sprinkler" | "Tank / Open Well";
export type WaterAvailabilityOption = "Rainfed" | "Limited irrigation" | "Moderate irrigation" | "Assured irrigation";
export type FarmingMethodOption = "Conventional" | "Organic / Natural" | "Integrated (INM/IPM)" | "Mixed / Multi-crop";

export interface RecommendationPayload {
  state: string;
  district: string;
  taluk: string;
  village?: string | null;
  agro_climatic_zone?: string | null;
  soil_type: SoilTypeOption;
  soil_data_available: boolean;
  soil_measurement_source: "soil_test" | "estimate" | "unavailable";
  soil_test_date?: string | null;
  ph?: number | null;
  nitrogen?: number | null;
  phosphorus?: number | null;
  potassium?: number | null;
  season: SeasonOption;
  irrigation_type: IrrigationOption;
  water_availability: WaterAvailabilityOption;
  land_area_acres: number;
  farming_method: FarmingMethodOption;
  previous_crop?: string | null;
  temperature?: number | null;
  humidity?: number | null;
  rainfall?: number | null;
  climate_source: "measured" | "estimate" | "reference";
  language: Language;
}

export interface DimensionScores {
  location: number;
  soil: number;
  water: number;
  seasonal: number;
  climatic: number;
  nutrient: number;
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
  ml_probability: number | null;
  dimension_scores: DimensionScores;
  reasons_en: string[];
  reasons_kn: string[];
  limitations_en: string[];
  limitations_kn: string[];
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
  insufficient_data_reason: string | null;
  missing_fields: string[];
  location_context: {
    state: string;
    district: string;
    taluk: string;
    village?: string | null;
    agro_climatic_zone?: string | null;
    zone_code?: string | null;
    normal_annual_rainfall_mm?: number | null;
    dominant_soil_types?: string[];
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
