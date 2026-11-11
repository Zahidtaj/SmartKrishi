import type {
  AdminOverview,
  CompareCropsResponse,
  CropDetail,
  CropSummary,
  DistrictItem,
  HealthStatus,
  KnowledgeArticleDetail,
  KnowledgeArticleSummary,
  RecommendationPayload,
  RecommendationResponse,
  SoilAnalysisResponse,
  TalukItem,
} from "../types";

export class ApiError extends Error {
  status: number;
  code: string;
  fieldErrors?: Record<string, string>;

  constructor(message: string, status: number, code = "API_ERROR", fieldErrors?: Record<string, string>) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.fieldErrors = fieldErrors;
  }
}

const API_BASE = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");

async function requestJson<T>(url: string, options?: RequestInit): Promise<T> {
  const fullUrl = url.startsWith("http") ? url : `${API_BASE}${url}`;
  const response = await fetch(fullUrl, {
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    },
    ...options,
  });

  const text = await response.text();
  let parsed: Record<string, unknown> | null = null;
  if (text) {
    try {
      parsed = JSON.parse(text) as Record<string, unknown>;
    } catch {
      parsed = null;
    }
  }

  if (!response.ok) {
    const detail =
      (parsed?.detail as string | undefined) ||
      (parsed?.error as string | undefined) ||
      `Request failed with status ${response.status}`;
    const code = (parsed?.code as string | undefined) || `HTTP_${response.status}`;
    const fieldErrors = parsed?.field_errors as Record<string, string> | undefined;
    throw new ApiError(detail, response.status, code, fieldErrors);
  }

  return parsed as T;
}

export const apiClient = {
  getHealth: () => requestJson<HealthStatus>("/api/health"),

  getStates: () => requestJson<{ states: string[] }>("/api/locations/states"),

  getDistricts: (state: string) =>
    requestJson<{ state: string; districts: DistrictItem[] }>(
      `/api/locations/districts?state=${encodeURIComponent(state)}`
    ),

  getTaluks: (state: string, district: string) =>
    requestJson<{ state: string; district: string; taluks: TalukItem[] }>(
      `/api/locations/taluks?state=${encodeURIComponent(state)}&district=${encodeURIComponent(district)}`
    ),

  getCrops: (params?: { category?: string; season?: string; water_level?: string }) => {
    const search = new URLSearchParams();
    if (params?.category) search.set("category", params.category);
    if (params?.season) search.set("season", params.season);
    if (params?.water_level) search.set("water_level", params.water_level);
    const qs = search.toString();
    return requestJson<CropSummary[]>(`/api/crops${qs ? `?${qs}` : ""}`);
  },

  getCropDetail: (cropId: number) => requestJson<CropDetail>(`/api/crops/${cropId}`),

  createRecommendation: (payload: RecommendationPayload) =>
    requestJson<RecommendationResponse>("/api/recommendations", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getRecommendation: (id: number) => requestJson<RecommendationResponse>(`/api/recommendations/${id}`),

  compareCrops: (cropIds: number[], landAreaAcres: number) =>
    requestJson<CompareCropsResponse>("/api/crops/compare", {
      method: "POST",
      body: JSON.stringify({ crop_ids: cropIds, land_area_acres: landAreaAcres }),
    }),

  analyzeSoil: (payload: {
    soil_type: string;
    ph?: number | null;
    nitrogen?: number | null;
    phosphorus?: number | null;
    potassium?: number | null;
    measurement_source: string;
    soil_test_date?: string | null;
  }) =>
    requestJson<SoilAnalysisResponse>("/api/soil/analyze", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getKnowledgeArticles: (category?: string, search?: string) => {
    const params = new URLSearchParams();
    if (category && category !== "all") params.set("category", category);
    if (search) params.set("search", search);
    const qs = params.toString();
    return requestJson<KnowledgeArticleSummary[]>(`/api/knowledge${qs ? `?${qs}` : ""}`);
  },

  getKnowledgeArticle: (id: number) => requestJson<KnowledgeArticleDetail>(`/api/knowledge/${id}`),

  submitFeedback: (payload: {
    recommendation_id?: number | null;
    category: string;
    rating?: number | null;
    district?: string | null;
    comment: string;
  }) =>
    requestJson<{ id: number; review_status: string }>("/api/feedback", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  adminLogin: (username: string, password: string) =>
    requestJson<{
      access_token: string;
      token_type: string;
      username: string;
      role: string;
      local_dev_notice: string;
    }>("/api/admin/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    }),

  getAdminOverview: (token: string) =>
    requestJson<AdminOverview>("/api/admin/overview", {
      headers: { Authorization: `Bearer ${token}` },
    }),

  adminUpdateCrop: (token: string, cropId: number, payload: Record<string, unknown>) =>
    requestJson<{ id: number; name_en: string; is_active: boolean }>(`/api/admin/crops/${cropId}`, {
      method: "PATCH",
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify(payload),
    }),

  adminCreateRule: (token: string, payload: Record<string, unknown>) =>
    requestJson<{ id: number }>("/api/admin/rules", {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify(payload),
    }),

  adminReviewFeedback: (token: string, feedbackId: number, review_status: string, admin_notes?: string) =>
    requestJson<{ id: number; review_status: string }>(`/api/admin/feedback/${feedbackId}`, {
      method: "PATCH",
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify({ review_status, admin_notes }),
    }),
};
