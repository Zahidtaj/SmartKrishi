export function PrivacyPolicyPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6 lg:px-8 space-y-6">
      <h1 className="text-3xl font-semibold tracking-tight text-ink">Privacy Policy</h1>
      <p className="text-sm text-muted">SmartKrishi VTU Community Project Prototype</p>

      <div className="sk-surface-card rounded-xl p-6 sm:p-8 space-y-5 text-sm leading-relaxed text-secondary">
        <section className="space-y-2">
          <h2 className="text-base font-semibold text-ink">1. Data This Prototype Collects</h2>
          <p>
            When you submit a crop advisory request, SmartKrishi stores the field observation inputs you
            provide in its local SQLite database: selected state, district, taluk, optional village name,
            observed soil colour, hand-feel soil texture, rainwater drainage and moisture retention, land slope
            and depth observations, water source reliability, optional crop history, and seasonal priorities.
            Laboratory NPK/pH values are NOT required.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-base font-semibold text-ink">2. Personal Information Policy</h2>
          <p>
            SmartKrishi intentionally does NOT request or collect personal identifiers such as phone numbers,
            Aadhaar numbers, GPS coordinates, email addresses, or residential street addresses in farmer workflows.
            Feedback submissions store only the feedback category, optional rating, optional district name, and comment text.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-base font-semibold text-ink">3. Local Browser Storage</h2>
          <p>
            SmartKrishi uses browser <code className="font-mono text-ink">localStorage</code> strictly to remember
            your chosen interface language (English or Kannada) and Light/Dark theme preference, and{" "}
            <code className="font-mono text-ink">sessionStorage</code> to remember whether the welcome animation
            has already played during your current session or to hold a temporary administrator bearer token.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-base font-semibold text-ink">4. No Third-Party Data Sharing</h2>
          <p>
            This local prototype does not transmit user soil records to third-party advertising trackers or external
            analytics networks. Before any future public deployment, hosting security, database backup policies, and
            data-retention controls must be formally reviewed.
          </p>
        </section>
      </div>
    </div>
  );
}
