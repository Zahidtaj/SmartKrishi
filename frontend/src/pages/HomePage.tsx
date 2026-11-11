import { Link } from "react-router-dom";
import {
  AlertTriangle,
  ArrowRight,
  BarChart3,
  BookOpen,
  Droplets,
  Layers,
  MapPin,
  Scale,
  ShieldAlert,
  Sprout,
} from "lucide-react";
import { useI18n } from "../i18n";

export function HomePage() {
  const { t } = useI18n();

  return (
    <div className="space-y-20 pb-8">
      {/* Hero Section */}
      <section className="mx-auto max-w-7xl px-4 pt-12 sm:px-6 lg:px-8 lg:pt-16">
        <div className="grid gap-10 lg:grid-cols-12 lg:items-center">
          <div className="lg:col-span-7 space-y-6">
            <h1 className="text-3xl font-semibold tracking-tight text-ink sm:text-4xl lg:text-[2.65rem] lg:leading-[1.15]">
              {t.home.headline}
            </h1>
            <p className="max-w-2xl text-base leading-relaxed text-secondary sm:text-lg">
              {t.home.subheadline}
            </p>
            <div className="flex flex-col gap-3 pt-2 sm:flex-row">
              <Link to="/recommend" className="sk-btn-primary">
                <span>{t.home.primaryCta}</span>
                <ArrowRight className="h-4 w-4" aria-hidden="true" />
              </Link>
              <Link to="/compare" className="sk-btn-secondary">
                <Scale className="h-4 w-4 text-accent" aria-hidden="true" />
                <span>{t.home.secondaryCta}</span>
              </Link>
            </div>
          </div>

          {/* Interactive Decision Flow Preview Panel (no fake stats) */}
          <div className="lg:col-span-5">
            <div className="sk-glass-panel rounded-xl p-6 space-y-5">
              <div className="flex items-center justify-between border-b border-white/10 pb-3">
                <div className="flex items-center gap-2.5">
                  <Sprout className="h-5 w-5 text-accent" aria-hidden="true" />
                  <h2 className="text-sm font-semibold text-ink">Hybrid Decision Pipeline</h2>
                </div>
                <span className="rounded border border-accent/35 bg-accent/10 px-2 py-0.5 font-mono text-xs text-accent">
                  Karnataka Focus
                </span>
              </div>

              <div className="space-y-3">
                <div className="flex items-start gap-3 rounded-lg bg-canvas/80 p-3.5 border border-white/10">
                  <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-accent" aria-hidden="true" />
                  <div>
                    <p className="text-sm font-medium text-ink">NARP Agro-Climatic Zone Gate</p>
                    <p className="text-xs text-secondary">
                      Resolves district & taluk to 10 documented Karnataka agro-climatic zones.
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3 rounded-lg bg-canvas/80 p-3.5 border border-white/10">
                  <Droplets className="mt-0.5 h-4 w-4 shrink-0 text-accent" aria-hidden="true" />
                  <div>
                    <p className="text-sm font-medium text-ink">Hard Water & Season Constraints</p>
                    <p className="text-xs text-secondary">
                      Prevents high-water or mismatched-season crops from overriding rainfed limits.
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3 rounded-lg bg-canvas/80 p-3.5 border border-white/10">
                  <Layers className="mt-0.5 h-4 w-4 shrink-0 text-accent" aria-hidden="true" />
                  <div>
                    <p className="text-sm font-medium text-ink">Random Forest + Scoring Transparency</p>
                    <p className="text-xs text-secondary">
                      Weights 6 compatibility dimensions and returns explicit reasons & limitations.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl">
          <h2 className="text-2xl font-semibold tracking-tight text-ink">{t.home.howTitle}</h2>
          <p className="mt-2.5 text-base text-secondary">{t.home.howIntro}</p>
        </div>

        <div className="mt-8 grid gap-6 md:grid-cols-3">
          <article className="sk-surface-card rounded-lg p-6 space-y-2.5">
            <MapPin className="h-5 w-5 text-accent" aria-hidden="true" />
            <h3 className="text-base font-semibold text-ink">{t.home.step1Title}</h3>
            <p className="text-sm leading-relaxed text-secondary">{t.home.step1Body}</p>
          </article>
          <article className="sk-surface-card rounded-lg p-6 space-y-2.5">
            <Droplets className="h-5 w-5 text-accent" aria-hidden="true" />
            <h3 className="text-base font-semibold text-ink">{t.home.step2Title}</h3>
            <p className="text-sm leading-relaxed text-secondary">{t.home.step2Body}</p>
          </article>
          <article className="sk-surface-card rounded-lg p-6 space-y-2.5">
            <BarChart3 className="h-5 w-5 text-accent" aria-hidden="true" />
            <h3 className="text-base font-semibold text-ink">{t.home.step3Title}</h3>
            <p className="text-sm leading-relaxed text-secondary">{t.home.step3Body}</p>
          </article>
        </div>
      </section>

      {/* Core Capabilities */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <h2 className="text-2xl font-semibold tracking-tight text-ink">{t.home.capabilitiesTitle}</h2>
        <div className="mt-8 grid gap-6 sm:grid-cols-2">
          <Link to="/recommend" className="sk-surface-card rounded-lg p-6 hover:border-accent/45 transition-colors block">
            <div className="flex items-center justify-between">
              <Sprout className="h-5 w-5 text-accent" aria-hidden="true" />
              <ArrowRight className="h-4 w-4 text-muted" aria-hidden="true" />
            </div>
            <h3 className="mt-4 text-base font-semibold text-ink">{t.home.cap1Title}</h3>
            <p className="mt-1.5 text-sm text-secondary leading-relaxed">{t.home.cap1Body}</p>
          </Link>

          <Link to="/compare" className="sk-surface-card rounded-lg p-6 hover:border-accent/45 transition-colors block">
            <div className="flex items-center justify-between">
              <Scale className="h-5 w-5 text-accent" aria-hidden="true" />
              <ArrowRight className="h-4 w-4 text-muted" aria-hidden="true" />
            </div>
            <h3 className="mt-4 text-base font-semibold text-ink">{t.home.cap2Title}</h3>
            <p className="mt-1.5 text-sm text-secondary leading-relaxed">{t.home.cap2Body}</p>
          </Link>

          <Link to="/soil-health" className="sk-surface-card rounded-lg p-6 hover:border-accent/45 transition-colors block">
            <div className="flex items-center justify-between">
              <Layers className="h-5 w-5 text-accent" aria-hidden="true" />
              <ArrowRight className="h-4 w-4 text-muted" aria-hidden="true" />
            </div>
            <h3 className="mt-4 text-base font-semibold text-ink">{t.home.cap3Title}</h3>
            <p className="mt-1.5 text-sm text-secondary leading-relaxed">{t.home.cap3Body}</p>
          </Link>

          <Link to="/knowledge" className="sk-surface-card rounded-lg p-6 hover:border-accent/45 transition-colors block">
            <div className="flex items-center justify-between">
              <BookOpen className="h-5 w-5 text-accent" aria-hidden="true" />
              <ArrowRight className="h-4 w-4 text-muted" aria-hidden="true" />
            </div>
            <h3 className="mt-4 text-base font-semibold text-ink">{t.home.cap4Title}</h3>
            <p className="mt-1.5 text-sm text-secondary leading-relaxed">{t.home.cap4Body}</p>
          </Link>
        </div>
      </section>

      {/* Limitations & Transparency */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="sk-surface-card rounded-xl border-warning/30 p-6 sm:p-8">
          <div className="flex items-center gap-3">
            <ShieldAlert className="h-5 w-5 text-warning shrink-0" aria-hidden="true" />
            <h2 className="text-xl font-semibold text-ink">{t.home.limitsTitle}</h2>
          </div>
          <ul className="mt-4 space-y-2.5 text-sm text-secondary">
            {t.home.limitsPoints.map((point, idx) => (
              <li key={idx} className="flex items-start gap-2.5">
                <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-warning/80" aria-hidden="true" />
                <span>{point}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>
    </div>
  );
}
