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
          <h2 className="text-base font-semibold text-ink">2. Limitations of Automated Recommendations</h2>
          <p>
            Machine learning predictions and prototype suitability scores depend on simplified regional rules and a
            public benchmark dataset. SmartKrishi is not connected to real-time meteorological feeds, live reservoir
            releases, or live local pest outbreak alerts.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-base font-semibold text-ink">3. Expert Verification Required</h2>
          <p>
            Users must verify crop selection, seed variety choice, chemical/organic nutrient dosages, and plant
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
            Users are responsible for providing accurate soil test measurements where available, respecting local
            irrigation regulations, and using feedback forms respectfully without submitting sensitive personal data.
          </p>
        </section>
      </div>
    </div>
  );
}
