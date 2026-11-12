export function TermsPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6 lg:px-8 space-y-6">
      <h1 className="text-3xl font-semibold tracking-tight text-ink">Terms & Conditions</h1>
      <p className="text-sm text-muted">SmartKrishi VTU Community Project Prototype</p>

      <div className="sk-surface-card rounded-xl p-6 sm:p-8 space-y-5 text-sm leading-relaxed text-secondary">
        <section className="space-y-2">
          <h2 className="text-base font-semibold text-ink">1. Intended Educational & Decision-Support Use</h2>
          <p>
            SmartKrishi is an agricultural decision-support prototype developed as a VTU Community Project. It helps
            farmers and students explore crop suitability criteria across Karnataka agro-climatic zones.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-base font-semibold text-ink">2. Limitations of Observation-Based Advisories</h2>
          <p>
            Suitability rankings depend on documented Karnataka NARP agro-climatic zone rules and farmer field
            observations (visual colour, feel texture, drainage, slope, and irrigation reliability). Soil colour
            alone cannot establish soil pH or NPK fertility. When live meteorological feeds are disconnected or
            unavailable, SmartKrishi uses only verified zone climate normals without fabricating live forecasts.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-base font-semibold text-ink">3. Expert Verification Required</h2>
          <p>
            Users must verify crop selection, seed variety choice, Soil Health Card nutrient dosages, and plant
            protection measures with certified agricultural officers at their local Raitha Samparka Kendra (RSK) or
            Krishi Vigyan Kendra (KVK) before investing in cultivation.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-base font-semibold text-ink">4. No Yield or Profit Guarantee</h2>
          <p>
            Economic comparison figures displayed by SmartKrishi are clearly labelled illustrative prototype baselines
            derived under documented assumptions. Actual yields, input costs, and market prices fluctuate substantially;
            SmartKrishi makes no guarantee of harvest yield, revenue, or net profit.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-base font-semibold text-ink">5. User Responsibilities</h2>
          <p>
            Users should select "Not sure / Unknown" whenever field conditions are uncertain rather than guessing,
            respect local water regulations, and use feedback forms without submitting sensitive personal data.
          </p>
        </section>
      </div>
    </div>
  );
}
