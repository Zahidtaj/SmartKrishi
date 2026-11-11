import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { AlertTriangle, Check, Scale } from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { apiClient } from "../api/client";
import { ErrorAlert } from "../components/ErrorAlert";
import { useI18n } from "../i18n";
import type { CompareCropsResponse, CropSummary } from "../types";

export function ComparePage() {
  const { lang, t } = useI18n();
  const [searchParams] = useSearchParams();

  const [allCrops, setAllCrops] = useState<CropSummary[]>([]);
  const [selectedIds, setSelectedIds] = useState<number[]>(() => {
    const raw = searchParams.get("ids");
    if (!raw) return [];
    return raw
      .split(",")
      .map((s) => Number(s.trim()))
      .filter((n) => Number.isFinite(n) && n > 0)
      .slice(0, 3);
  });
  const [landArea, setLandArea] = useState("1");
  const [comparison, setComparison] = useState<CompareCropsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiClient
      .getCrops()
      .then((list) => {
        setAllCrops(list);
        if (selectedIds.length === 0 && list.length >= 1) {
          const defaults = list
            .filter((c) => ["ragi", "maize", "pigeonpeas"].includes(c.crop_key))
            .slice(0, 3)
            .map((c) => c.id);
          const chosen = defaults.length > 0 ? defaults : list.slice(0, 3).map((c) => c.id);
          setSelectedIds(chosen);
          void runCompare(chosen, landArea);
        } else if (selectedIds.length > 0) {
          void runCompare(selectedIds, landArea);
        }
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load crop catalog."));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const runCompare = async (ids = selectedIds, acresStr = landArea) => {
    if (ids.length === 0) {
      setError("Please select at least one crop (up to 3) to compare.");
      return;
    }
    const acres = Number(acresStr);
    if (Number.isNaN(acres) || acres <= 0 || acres > 1000) {
      setError("Land area must be between 0.1 and 1000 acres.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await apiClient.compareCrops(ids, acres);
      setComparison(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to compare selected crops.");
    } finally {
      setLoading(false);
    }
  };

  const toggleCrop = (id: number) => {
    setSelectedIds((prev) => {
      if (prev.includes(id)) return prev.filter((item) => item !== id);
      if (prev.length >= 3) return [...prev.slice(1), id];
      return [...prev, id];
    });
  };

  const chartData =
    comparison?.crops
      .filter((c) => c.economic_available && c.cultivation_cost_min_total !== null && c.gross_revenue_min_total !== null)
      .map((c) => ({
        name: lang === "kn" ? c.name_kn : c.name_en,
        estCostMid: Math.round(((c.cultivation_cost_min_total || 0) + (c.cultivation_cost_max_total || 0)) / 2),
        estRevenueMid: Math.round(((c.gross_revenue_min_total || 0) + (c.gross_revenue_max_total || 0)) / 2),
      })) || [];

  const formatInrRange = (min: number | null, max: number | null) => {
    if (min === null || max === null) return t.compare.unavailableText;
    return `₹${min.toLocaleString("en-IN")} – ₹${max.toLocaleString("en-IN")}`;
  };

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8 space-y-8">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-ink sm:text-3xl">{t.compare.pageTitle}</h1>
        <p className="mt-2 max-w-3xl text-sm text-secondary sm:text-base">{t.compare.pageSubtitle}</p>
      </div>

      {/* Selector Panel */}
      <section className="sk-surface-card rounded-xl p-6 space-y-5">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h2 className="text-sm font-semibold text-ink">{t.compare.selectCrops}</h2>
            <p className="text-xs text-muted mt-0.5">Selected: {selectedIds.length} / 3</p>
          </div>
          <div className="flex items-end gap-3">
            <div>
              <label htmlFor="compare-acres" className="block text-xs text-secondary mb-1">
                {t.compare.landAreaLabel}
              </label>
              <input
                id="compare-acres"
                type="number"
                step="0.5"
                min="0.1"
                max="1000"
                className="sk-input w-32 font-mono tabular-nums"
                value={landArea}
                onChange={(e) => setLandArea(e.target.value)}
              />
            </div>
            <button
              type="button"
              onClick={() => runCompare()}
              disabled={loading || selectedIds.length === 0}
              className="sk-btn-primary text-sm"
            >
              <Scale className="h-4 w-4" aria-hidden="true" />
              <span>{t.compare.runCompare}</span>
            </button>
          </div>
        </div>

        <div className="flex flex-wrap gap-2">
          {allCrops.map((crop) => {
            const active = selectedIds.includes(crop.id);
            return (
              <button
                key={crop.id}
                type="button"
                onClick={() => toggleCrop(crop.id)}
                aria-pressed={active}
                className={`inline-flex items-center gap-1.5 min-h-[38px] rounded-md border px-3 py-1.5 text-xs font-medium transition-colors ${
                  active
                    ? "border-accent bg-accent/15 text-accent"
                    : "border-white/15 bg-canvas/70 text-secondary hover:text-ink hover:border-white/30"
                }`}
              >
                {active && <Check className="h-3.5 w-3.5" aria-hidden="true" />}
                <span>{lang === "kn" ? crop.name_kn : crop.name_en}</span>
              </button>
            );
          })}
        </div>
      </section>

      {error && <ErrorAlert message={error} />}

      {comparison && (
        <>
          {/* Responsive Comparison Table */}
          <section className="sk-surface-card rounded-xl overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full min-w-[680px] text-left text-sm">
                <thead className="border-b border-white/10 bg-canvas/70">
                  <tr>
                    <th className="p-4 font-semibold text-secondary w-52">Parameter</th>
                    {comparison.crops.map((c) => (
                      <th key={c.crop_id} className="p-4 font-semibold text-ink">
                        <div className="flex items-center gap-2.5">
                          <img src={c.image_asset} alt={c.name_en} className="h-9 w-9 rounded border border-white/10" />
                          <div>
                            <div>{lang === "kn" ? c.name_kn : c.name_en}</div>
                            <div className="text-xs font-normal text-muted">{c.category}</div>
                          </div>
                        </div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/10">
                  <tr>
                    <td className="p-4 text-muted">Soil Suitability</td>
                    {comparison.crops.map((c) => (
                      <td key={c.crop_id} className="p-4 text-ink">
                        {c.suitable_soil_types.join(", ")} (pH {c.ph_range})
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-4 text-muted">Water Requirement</td>
                    {comparison.crops.map((c) => (
                      <td key={c.crop_id} className="p-4 font-mono text-ink tabular-nums">
                        {c.water_requirement_level} ({c.water_requirement_mm_range})
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-4 text-muted">Growing Season</td>
                    {comparison.crops.map((c) => (
                      <td key={c.crop_id} className="p-4 text-ink">
                        {c.suitable_seasons.join(", ")}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-4 text-muted">Growing Duration</td>
                    {comparison.crops.map((c) => (
                      <td key={c.crop_id} className="p-4 font-mono text-ink tabular-nums">
                        {c.growing_duration_days_range}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-4 text-muted">Climate Requirements</td>
                    {comparison.crops.map((c) => (
                      <td key={c.crop_id} className="p-4 font-mono text-xs text-secondary tabular-nums">
                        {c.temperature_range_c} · {c.humidity_range_pct} RH · {c.rainfall_range_mm}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-4 text-muted">Seed Rate</td>
                    {comparison.crops.map((c) => (
                      <td key={c.crop_id} className="p-4 text-ink">
                        {c.seed_rate_kg_per_acre}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-4 text-muted">
                      Est. Cultivation Cost ({comparison.land_area_acres} ac)
                      <span className="block text-[11px] text-warning">Illustrative baseline</span>
                    </td>
                    {comparison.crops.map((c) => (
                      <td key={c.crop_id} className="p-4 font-mono text-ink tabular-nums">
                        {formatInrRange(c.cultivation_cost_min_total, c.cultivation_cost_max_total)}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-4 text-muted">Expected Yield ({comparison.land_area_acres} ac)</td>
                    {comparison.crops.map((c) => (
                      <td key={c.crop_id} className="p-4 font-mono text-ink tabular-nums">
                        {c.expected_yield_qtl_min_total !== null && c.expected_yield_qtl_max_total !== null
                          ? `${c.expected_yield_qtl_min_total} – ${c.expected_yield_qtl_max_total} qtl`
                          : t.compare.unavailableText}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-4 text-muted">Potential Gross Revenue</td>
                    {comparison.crops.map((c) => (
                      <td key={c.crop_id} className="p-4 font-mono text-ink tabular-nums">
                        {formatInrRange(c.gross_revenue_min_total, c.gross_revenue_max_total)}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-4 text-muted">Estimated Net Return Range</td>
                    {comparison.crops.map((c) => (
                      <td key={c.crop_id} className="p-4 font-mono text-accent tabular-nums">
                        {formatInrRange(c.net_return_min_total, c.net_return_max_total)}
                      </td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          {/* Chart only when economic comparison data exists */}
          {chartData.length > 0 && (
            <section className="sk-surface-card rounded-xl p-6 space-y-4">
              <div>
                <h2 className="text-base font-semibold text-ink">
                  Illustrative Cost vs. Gross Revenue Midpoint ({comparison.land_area_acres} acre)
                </h2>
                <p className="text-xs text-muted mt-0.5">
                  Midpoint comparison of prototype ranges shown for visual scale only — never a profit guarantee.
                </p>
              </div>
              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData} margin={{ top: 10, right: 20, left: 10, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(226,232,228,0.1)" />
                    <XAxis dataKey="name" stroke="#B6C0B9" fontSize={12} />
                    <YAxis stroke="#B6C0B9" fontSize={12} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#121815",
                        border: "1px solid rgba(226,232,228,0.2)",
                        borderRadius: "6px",
                        color: "#F2F4F0",
                      }}
                    />
                    <Legend />
                    <Bar dataKey="estCostMid" name="Est. Cost Midpoint (INR)" fill="#D99B4E" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="estRevenueMid" name="Potential Gross Revenue Midpoint (INR)" fill="#52B788" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </section>
          )}

          {/* Documented Assumptions */}
          <section className="sk-surface-card rounded-xl p-6 space-y-4">
            <h2 className="text-base font-semibold text-ink">{t.compare.assumptionsTitle}</h2>
            <div className="space-y-3">
              {comparison.crops.map((c) => (
                <div key={c.crop_id} className="rounded-lg border border-white/10 bg-canvas/60 p-4 text-sm space-y-1">
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-semibold text-ink">{lang === "kn" ? c.name_kn : c.name_en}</span>
                    <span className="font-mono text-xs text-warning">{c.economic_data_status}</span>
                  </div>
                  <p className="text-secondary text-xs leading-relaxed">
                    {lang === "kn" ? c.assumptions_kn : c.assumptions_en}
                  </p>
                  <p className="text-xs text-muted">Source: {c.economic_source || c.information_source}</p>
                </div>
              ))}
            </div>
            <div className="flex items-start gap-2.5 text-xs text-warning pt-2">
              <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
              <p>{lang === "kn" ? comparison.disclaimer_kn : comparison.disclaimer_en}</p>
            </div>
          </section>
        </>
      )}
    </div>
  );
}
