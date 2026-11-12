import { useEffect, useState } from "react";
import { X, Droplets, Calendar, Sprout, BookOpen } from "lucide-react";
import { apiClient } from "../api/client";
import type { CropDetail } from "../types";
import { useI18n } from "../i18n";
import { ErrorAlert } from "./ErrorAlert";

interface CropDetailModalProps {
  cropId: number | null;
  onClose: () => void;
}

export function CropDetailModal({ cropId, onClose }: CropDetailModalProps) {
  const { lang } = useI18n();
  const [detail, setDetail] = useState<CropDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (cropId === null) {
      setDetail(null);
      return;
    }
    let cancelled = false;
    setLoading(true);
    setError(null);
    apiClient
      .getCropDetail(cropId)
      .then((res) => {
        if (!cancelled) setDetail(res);
      })
      .catch((err) => {
        if (!cancelled) setError(err instanceof Error ? err.message : "Failed to load crop profile.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [cropId]);

  if (cropId === null) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label={detail ? detail.name_en : "Crop profile details"}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 p-4 backdrop-blur-sm"
    >
      <div className="sk-surface-card relative max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-lg p-6 shadow-2xl">
        <button
          type="button"
          onClick={onClose}
          aria-label="Close crop details"
          className="absolute right-4 top-4 inline-flex h-10 w-10 items-center justify-center rounded-md border border-ink/15 text-secondary hover:bg-elevated hover:text-ink"
        >
          <X className="h-5 w-5" />
        </button>

        {loading && <p className="py-12 text-center text-sm text-secondary">Loading crop agronomic profile...</p>}
        {error && <ErrorAlert message={error} />}

        {detail && !loading && (
          <div className="space-y-6 pr-2">
            <div className="flex items-center gap-4">
              <img
                src={detail.image_asset}
                alt={detail.name_en}
                className="h-20 w-20 rounded-lg border border-ink/10 bg-canvas p-1"
              />
              <div>
                <h2 className="text-xl font-semibold text-ink">
                  {lang === "kn" ? detail.name_kn : detail.name_en}
                </h2>
                <p className="text-sm text-secondary">
                  {lang === "kn" ? detail.name_en : detail.name_kn} ·{" "}
                  <span className="italic">{detail.scientific_name}</span>
                </p>
                <span className="mt-1.5 inline-block rounded border border-accent/35 bg-accent/10 px-2 py-0.5 text-xs font-medium text-accent">
                  {detail.category}
                </span>
              </div>
            </div>

            <div className="grid gap-3 sm:grid-cols-3">
              <div className="rounded-md border border-ink/10 bg-canvas/70 p-3">
                <div className="flex items-center gap-1.5 text-xs text-muted">
                  <Droplets className="h-3.5 w-3.5 text-accent" aria-hidden="true" />
                  <span>Water Need</span>
                </div>
                <p className="mt-1 font-mono text-sm text-ink tabular-nums">
                  {detail.water_requirement_level} ({detail.water_requirement_mm_min}-{detail.water_requirement_mm_max} mm)
                </p>
              </div>
              <div className="rounded-md border border-ink/10 bg-canvas/70 p-3">
                <div className="flex items-center gap-1.5 text-xs text-muted">
                  <Calendar className="h-3.5 w-3.5 text-accent" aria-hidden="true" />
                  <span>Duration</span>
                </div>
                <p className="mt-1 font-mono text-sm text-ink tabular-nums">
                  {detail.growing_duration_days_min}-{detail.growing_duration_days_max} days
                </p>
              </div>
              <div className="rounded-md border border-ink/10 bg-canvas/70 p-3">
                <div className="flex items-center gap-1.5 text-xs text-muted">
                  <Sprout className="h-3.5 w-3.5 text-accent" aria-hidden="true" />
                  <span>Seed Rate</span>
                </div>
                <p className="mt-1 text-sm text-ink">{detail.seed_rate_kg_per_acre}</p>
              </div>
            </div>

            <div className="space-y-2 text-sm">
              <h3 className="font-semibold text-ink">Documented Field & Climatic Conditions</h3>
              <dl className="grid gap-2 sm:grid-cols-2 rounded-md border border-ink/10 bg-canvas/60 p-4">
                <div>
                  <dt className="text-xs text-muted">Suitable Soils & Textures</dt>
                  <dd className="text-ink">
                    {detail.requirement.suitable_soil_types.join(", ")} ({detail.requirement.suitable_textures.join(", ")})
                  </dd>
                </div>
                <div>
                  <dt className="text-xs text-muted">Drainage & Drought Tolerance</dt>
                  <dd className="text-ink">
                    Depth: {detail.requirement.min_soil_depth} · Drought: {detail.requirement.drought_tolerance}
                  </dd>
                </div>
                <div>
                  <dt className="text-xs text-muted">Seasons</dt>
                  <dd className="text-ink">{detail.requirement.suitable_seasons.join(", ")}</dd>
                </div>
                <div>
                  <dt className="text-xs text-muted">Temperature & Rainfall</dt>
                  <dd className="font-mono text-ink tabular-nums">
                    {detail.requirement.temp_min_c}-{detail.requirement.temp_max_c}°C ·{" "}
                    {detail.requirement.rainfall_min_mm}-{detail.requirement.rainfall_max_mm} mm
                  </dd>
                </div>
              </dl>
            </div>

            <div className="space-y-1.5">
              <h3 className="flex items-center gap-1.5 text-sm font-semibold text-ink">
                <BookOpen className="h-4 w-4 text-accent" aria-hidden="true" />
                <span>Cultivation Guidance</span>
              </h3>
              <p className="text-sm leading-relaxed text-secondary">
                {lang === "kn" ? detail.cultivation_guidance_kn : detail.cultivation_guidance_en}
              </p>
              <p className="text-xs text-muted pt-1">Source: {detail.information_source}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
