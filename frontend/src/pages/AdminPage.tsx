import { useEffect, useState } from "react";
import { CheckCircle, LogOut, ShieldCheck } from "lucide-react";
import { apiClient } from "../api/client";
import { ErrorAlert } from "../components/ErrorAlert";
import type { AdminOverview, CropSummary } from "../types";

export function AdminPage() {
  const [token, setToken] = useState<string | null>(() => sessionStorage.getItem("smartkrishi_admin_token"));
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("");
  const [loginNotice, setLoginNotice] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const [overview, setOverview] = useState<AdminOverview | null>(null);
  const [crops, setCrops] = useState<CropSummary[]>([]);

  // New regional rule form
  const [ruleCropId, setRuleCropId] = useState("");
  const [ruleZone, setRuleZone] = useState("KA-Z5");
  const [ruleSeason, setRuleSeason] = useState("Kharif");
  const [ruleLevel, setRuleLevel] = useState("recommended");
  const [ruleNoteEn, setRuleNoteEn] = useState("");
  const [ruleNoteKn, setRuleNoteKn] = useState("");
  const [ruleSource, setRuleSource] = useState("UAS Bengaluru Advisory");
  const [ruleMsg, setRuleMsg] = useState<string | null>(null);

  const loadDashboard = async (activeToken: string) => {
    setLoading(true);
    setError(null);
    try {
      const [ov, cropList] = await Promise.all([
        apiClient.getAdminOverview(activeToken),
        apiClient.getCrops(),
      ]);
      setOverview(ov);
      setCrops(cropList);
      if (cropList.length > 0 && !ruleCropId) {
        setRuleCropId(String(cropList[0].id));
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load admin overview.");
      sessionStorage.removeItem("smartkrishi_admin_token");
      setToken(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (token) {
      void loadDashboard(token);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await apiClient.adminLogin(username, password);
      sessionStorage.setItem("smartkrishi_admin_token", res.access_token);
      setLoginNotice(res.local_dev_notice);
      setToken(res.access_token);
      setPassword("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Authentication failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    sessionStorage.removeItem("smartkrishi_admin_token");
    setToken(null);
    setOverview(null);
  };

  const handleCreateRule = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token || !ruleCropId || ruleNoteEn.trim().length < 5) return;
    try {
      await apiClient.adminCreateRule(token, {
        crop_id: Number(ruleCropId),
        state: "Karnataka",
        agro_climatic_zone: ruleZone,
        season: ruleSeason,
        suitability_level: ruleLevel,
        priority_weight: 1.0,
        rule_notes_en: ruleNoteEn.trim(),
        rule_notes_kn: ruleNoteKn.trim() || ruleNoteEn.trim(),
        source: ruleSource.trim(),
      });
      setRuleMsg("Regional crop rule added.");
      setRuleNoteEn("");
      setRuleNoteKn("");
      await loadDashboard(token);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create rule.");
    }
  };

  const handleReviewFeedback = async (feedbackId: number) => {
    if (!token) return;
    try {
      await apiClient.adminReviewFeedback(token, feedbackId, "reviewed", "Reviewed in Admin Console");
      await loadDashboard(token);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update feedback.");
    }
  };

  if (!token) {
    return (
      <div className="mx-auto max-w-md px-4 py-16">
        <div className="sk-surface-card rounded-xl p-6 sm:p-8 space-y-5">
          <div className="flex items-center gap-2.5">
            <ShieldCheck className="h-6 w-6 text-accent" aria-hidden="true" />
            <h1 className="text-xl font-semibold text-ink">Administration Sign In</h1>
          </div>
          <p className="text-xs leading-relaxed text-secondary">
            Protected local development authentication using salted PBKDF2-HMAC-SHA256 verification and signed
            bearer tokens. Configure credentials via <code className="font-mono text-ink">.env</code> before shared use.
          </p>

          {error && <ErrorAlert message={error} />}

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label htmlFor="admin-user" className="block text-xs font-medium text-secondary mb-1">
                Username
              </label>
              <input
                id="admin-user"
                type="text"
                className="sk-input"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div>
              <label htmlFor="admin-pass" className="block text-xs font-medium text-secondary mb-1">
                Password
              </label>
              <input
                id="admin-pass"
                type="password"
                className="sk-input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit" disabled={loading} className="sk-btn-primary w-full text-sm">
              {loading ? "Signing in..." : "Sign In"}
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8 space-y-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-ink">SmartKrishi Administration Console</h1>
          <p className="text-xs text-secondary mt-1">
            Signed in as <span className="font-mono text-accent">{overview?.admin_username || username}</span>
            {loginNotice ? ` · ${loginNotice}` : ""}
          </p>
        </div>
        <button type="button" onClick={handleLogout} className="sk-btn-secondary text-sm">
          <LogOut className="h-4 w-4" aria-hidden="true" />
          <span>Sign Out</span>
        </button>
      </div>

      {error && <ErrorAlert message={error} />}

      {overview && (
        <div className="space-y-8">
          {/* ML & Dataset Status */}
          <section className="sk-surface-card rounded-xl p-6 space-y-4">
            <h2 className="text-base font-semibold text-ink">ML Model & Dataset Status</h2>
            {overview.ml_metrics && (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 text-sm">
                <div className="rounded-lg border border-ink/10 bg-canvas/70 p-4">
                  <div className="text-xs text-muted">Model</div>
                  <div className="mt-1 font-mono text-ink">{overview.ml_metrics.model_type}</div>
                </div>
                <div className="rounded-lg border border-ink/10 bg-canvas/70 p-4">
                  <div className="text-xs text-muted">Held-out Test Accuracy</div>
                  <div className="mt-1 font-mono text-accent tabular-nums">
                    {(overview.ml_metrics.test_accuracy * 100).toFixed(2)}% ({overview.ml_metrics.test_samples} test rows)
                  </div>
                </div>
                <div className="rounded-lg border border-ink/10 bg-canvas/70 p-4">
                  <div className="text-xs text-muted">Macro F1 / 5-Fold CV F1</div>
                  <div className="mt-1 font-mono text-ink tabular-nums">
                    {overview.ml_metrics.macro_f1.toFixed(4)} / {overview.ml_metrics.cv_macro_f1_mean.toFixed(4)}
                  </div>
                </div>
                <div className="rounded-lg border border-ink/10 bg-canvas/70 p-4">
                  <div className="text-xs text-muted">Active Crops / Rules</div>
                  <div className="mt-1 font-mono text-ink tabular-nums">
                    {crops.length} crops · {overview.regional_rules.length}+ rules shown
                  </div>
                </div>
              </div>
            )}
            <p className="text-xs text-secondary">
              Dataset: {String(overview.dataset_provenance.dataset_name || "")} (
              {String(overview.dataset_provenance.license || "")})
            </p>
          </section>

          {/* Add Regional Crop Rule */}
          <section className="sk-surface-card rounded-xl p-6 space-y-4">
            <h2 className="text-base font-semibold text-ink">Add Regional Crop Rule</h2>
            {ruleMsg && <p className="text-xs text-accent">{ruleMsg}</p>}
            <form onSubmit={handleCreateRule} className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <div>
                <label htmlFor="rule-crop" className="block text-xs text-secondary mb-1">
                  Crop
                </label>
                <select
                  id="rule-crop"
                  className="sk-input"
                  value={ruleCropId}
                  onChange={(e) => setRuleCropId(e.target.value)}
                >
                  {crops.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name_en}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label htmlFor="rule-zone" className="block text-xs text-secondary mb-1">
                  Zone Code
                </label>
                <input
                  id="rule-zone"
                  className="sk-input font-mono"
                  value={ruleZone}
                  onChange={(e) => setRuleZone(e.target.value)}
                />
              </div>
              <div>
                <label htmlFor="rule-season" className="block text-xs text-secondary mb-1">
                  Season
                </label>
                <select
                  id="rule-season"
                  className="sk-input"
                  value={ruleSeason}
                  onChange={(e) => setRuleSeason(e.target.value)}
                >
                  <option value="Kharif">Kharif</option>
                  <option value="Rabi">Rabi</option>
                  <option value="Zaid">Zaid</option>
                  <option value="Perennial">Perennial</option>
                </select>
              </div>
              <div>
                <label htmlFor="rule-level" className="block text-xs text-secondary mb-1">
                  Suitability Level
                </label>
                <select
                  id="rule-level"
                  className="sk-input"
                  value={ruleLevel}
                  onChange={(e) => setRuleLevel(e.target.value)}
                >
                  <option value="recommended">recommended</option>
                  <option value="conditional">conditional</option>
                  <option value="restricted">restricted</option>
                </select>
              </div>
              <div className="sm:col-span-2">
                <label htmlFor="rule-note-en" className="block text-xs text-secondary mb-1">
                  Rule Notes (English)
                </label>
                <input
                  id="rule-note-en"
                  className="sk-input"
                  value={ruleNoteEn}
                  onChange={(e) => setRuleNoteEn(e.target.value)}
                  placeholder="Documented regional constraint or rule..."
                  required
                />
              </div>
              <div>
                <label htmlFor="rule-note-kn" className="block text-xs text-secondary mb-1">
                  Rule Notes (Kannada)
                </label>
                <input
                  id="rule-note-kn"
                  className="sk-input"
                  value={ruleNoteKn}
                  onChange={(e) => setRuleNoteKn(e.target.value)}
                  placeholder="Kannada notes (optional)"
                />
              </div>
              <div>
                <label htmlFor="rule-source" className="block text-xs text-secondary mb-1">
                  Reference Source
                </label>
                <input
                  id="rule-source"
                  className="sk-input"
                  value={ruleSource}
                  onChange={(e) => setRuleSource(e.target.value)}
                  required
                />
              </div>
              <div className="sm:col-span-2 lg:col-span-4 flex justify-end">
                <button type="submit" className="sk-btn-primary text-sm">
                  Save Rule
                </button>
              </div>
            </form>
          </section>

          {/* Feedback Review & Recent Recommendations */}
          <div className="grid gap-6 lg:grid-cols-2">
            <section className="sk-surface-card rounded-xl p-6 space-y-4">
              <h2 className="text-base font-semibold text-ink">User Feedback Queue</h2>
              {overview.feedback.length === 0 ? (
                <p className="text-sm text-secondary">No feedback submitted yet.</p>
              ) : (
                <div className="space-y-3">
                  {overview.feedback.map((fb) => (
                    <div key={fb.id} className="rounded-lg border border-ink/10 bg-canvas/60 p-3.5 text-sm space-y-2">
                      <div className="flex items-center justify-between text-xs text-muted">
                        <span>
                          {fb.category} {fb.district ? `· ${fb.district}` : ""}
                        </span>
                        <span className={fb.review_status === "reviewed" ? "text-accent" : "text-warning"}>
                          {fb.review_status}
                        </span>
                      </div>
                      <p className="text-ink">{fb.comment}</p>
                      {fb.review_status !== "reviewed" && (
                        <button
                          type="button"
                          onClick={() => handleReviewFeedback(fb.id)}
                          className="sk-btn-secondary text-xs min-h-[34px] py-1 px-2.5"
                        >
                          <CheckCircle className="h-3.5 w-3.5 text-accent" aria-hidden="true" />
                          <span>Mark Reviewed</span>
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </section>

            <section className="sk-surface-card rounded-xl p-6 space-y-4">
              <h2 className="text-base font-semibold text-ink">Recent Recommendation Logs</h2>
              {overview.recent_recommendations.length === 0 ? (
                <p className="text-sm text-secondary">No recommendation runs recorded yet.</p>
              ) : (
                <div className="space-y-2.5">
                  {overview.recent_recommendations.map((rec) => (
                    <div
                      key={rec.id}
                      className="flex items-center justify-between rounded-lg border border-ink/10 bg-canvas/60 px-3.5 py-2.5 text-xs"
                    >
                      <div>
                        <span className="font-mono text-ink">#{rec.id}</span> ·{" "}
                        <span className="text-secondary">
                          {rec.district || "Unknown"} ({rec.season || "-"})
                        </span>
                      </div>
                      <span className="font-mono text-accent">{rec.mode_used}</span>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </div>
        </div>
      )}
    </div>
  );
}
