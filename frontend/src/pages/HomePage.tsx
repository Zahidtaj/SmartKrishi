import { Link } from "react-router-dom";
import {
  AlertTriangle,
  ArrowRight,
  BarChart3,
  BookOpen,
  CloudSun,
  Compass,
  Droplets,
  Eye,
  Layers,
  MapPin,
  ShieldAlert,
  Sprout,
} from "lucide-react";
import { useI18n } from "../i18n";

export function HomePage() {
  const { t } = useI18n();

  return (
    <div className="space-y-20 pb-10">
      {/* Hero Section with Bento Decision Preview */}
      <section className="mx-auto max-w-7xl px-4 pt-12 sm:px-6 lg:px-8 lg:pt-16">
        <div className="grid gap-10 lg:grid-cols-12 lg:items-center">
          <div className="lg:col-span-7 space-y-6">
            <h1 className="text-3xl font-semibold tracking-tight text-ink sm:text-4xl lg:text-[2.65rem] lg:leading-[1.14]">
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
              <Link to="/soil-health" className="sk-btn-secondary">
                <Eye className="h-4 w-4 text-accent" aria-hidden="true" />
                <span>{t.home.secondaryCta}</span>
              </Link>
            </div>
          </div>

          {/* Sleek Analytics Bento Preview Card inspired by reference UI */}
          <div className="lg:col-span-5">
            <div className="sk-glass-panel rounded-2xl p-6 space-y-5">
              <div className="flex items-center justify-between border-b border-ink/10 pb-3.5">
                <div className="flex items-center gap-2.5">
                  <Sprout className="h-5 w-5 text-accent" aria-hidden="true" />
                  <h2 className="text-sm font-semibold text-ink">Observation Decision Pipeline</h2>
                </div>
                <span className="rounded-md border border-accent/35 bg-accent/10 px-2.5 py-0.5 font-mono text-xs text-accent">
                  Karnataka · 10 Zones
                </span>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="rounded-xl border border-ink/10 bg-elevated/60 p-3.5">
                  <p className="text-xs text-muted">Taluks Mapped</p>
                  <p className="mt-1 font-mono text-2xl font-semibold text-ink tabular-nums">131</p>
                </div>
                <div className="rounded-xl border border-ink/10 bg-elevated/60 p-3.5">
                  <p className="text-xs text-muted">Lab Test Required</p>
                  <p className="mt-1 text-xl font-semibold text-accent">Optional Only</p>
                </div>
              </div>

              <div className="space-y-2.5">
                <div className="flex items-start gap-3 rounded-xl border border-ink/10 bg-canvas/70 p-3.5">
                  <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-accent" aria-hidden="true" />
                  <div>
                    <p className="text-sm font-medium text-ink">NARP Agro-Climatic Zone Gate</p>
                    <p className="text-xs text-secondary">
                      Auto-links District & Taluk to UAS/ICAR rainfall normals & zone crop calendars.
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3 rounded-xl border border-ink/10 bg-canvas/70 p-3.5">
                  <Droplets className="mt-0.5 h-4 w-4 shrink-0 text-accent" aria-hidden="true" />
                  <div>
                    <p className="text-sm font-medium text-ink">Physical Soil, Drainage & Water Checks</p>
                    <p className="text-xs text-secondary">
                      Filters out waterlogging & scarcity risks using field feel, slope & irrigation reliability.
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-3 rounded-xl border border-ink/10 bg-canvas/70 p-3.5">
                  <CloudSun className="mt-0.5 h-4 w-4 shrink-0 text-accent" aria-hidden="true" />
                  <div>
                    <p className="text-sm font-medium text-ink">Source-Separated Weather Advisory</p>
                    <p className="text-xs text-secondary">
                      Keeps long-term normals distinct from live weather; flags unavailable live feeds honestly.
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
          <article className="sk-surface-card rounded-xl p-6 space-y-2.5">
            <Compass className="h-5 w-5 text-accent" aria-hidden="true" />
            <h3 className="text-base font-semibold text-ink">{t.home.step1Title}</h3>
            <p className="text-sm leading-relaxed text-secondary">{t.home.step1Body}</p>
          </article>
          <article className="sk-surface-card rounded-xl p-6 space-y-2.5">
            <Layers className="h-5 w-5 text-accent" aria-hidden="true" />
            <h3 className="text-base font-semibold text-ink">{t.home.step2Title}</h3>
            <p className="text-sm leading-relaxed text-secondary">{t.home.step2Body}</p>
          </article>
          <article className="sk-surface-card rounded-xl p-6 space-y-2.5">
            <BarChart3 className="h-5 w-5 text-accent" aria-hidden="true" />
            <h3 className="text-base font-semibold text-ink">{t.home.step3Title}</h3>
            <p className="text-sm leading-relaxed text-secondary">{t.home.step3Body}</p>
          </article>
        </div>
      </section>

      {/* Capabilities Grid */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <h2 className="text-2xl font-semibold tracking-tight text-ink">{t.home.capabilitiesTitle}</h2>
        <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <Link to="/recommend" className="sk-choice-card rounded-xl p-6 block">
            <Sprout className="h-5 w-5 text-accent" aria-hidden="true" />
            <h3 className="mt-4 text-base font-semibold text-ink">{t.home.cap1Title}</h3>
            <p className="mt-2 text-sm text-secondary">{t.home.cap1Body}</p>
          </Link>
          <Link to="/knowledge" className="sk-choice-card rounded-xl p-6 block">
            <MapPin className="h-5 w-5 text-accent" aria-hidden="true" />
            <h3 className="mt-4 text-base font-semibold text-ink">{t.home.cap2Title}</h3>
            <p className="mt-2 text-sm text-secondary">{t.home.cap2Body}</p>
          </Link>
          <Link to="/soil-health" className="sk-choice-card rounded-xl p-6 block">
            <CloudSun className="h-5 w-5 text-accent" aria-hidden="true" />
            <h3 className="mt-4 text-base font-semibold text-ink">{t.home.cap3Title}</h3>
            <p className="mt-2 text-sm text-secondary">{t.home.cap3Body}</p>
          </Link>
          <Link to="/compare" className="sk-choice-card rounded-xl p-6 block">
            <BookOpen className="h-5 w-5 text-accent" aria-hidden="true" />
            <h3 className="mt-4 text-base font-semibold text-ink">{t.home.cap4Title}</h3>
            <p className="mt-2 text-sm text-secondary">{t.home.cap4Body}</p>
          </Link>
        </div>
      </section>

      {/* Honest Limitations Banner */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="rounded-xl border border-warning/35 bg-warning/10 p-6 sm:p-8">
          <div className="flex items-start gap-3">
            <ShieldAlert className="mt-0.5 h-5 w-5 shrink-0 text-warning" aria-hidden="true" />
            <div className="space-y-3">
              <h2 className="text-lg font-semibold text-ink">{t.home.limitsTitle}</h2>
              <ul className="space-y-2 text-sm text-secondary">
                {t.home.limitsPoints.map((pt, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-warning" aria-hidden="true" />
                    <span>{pt}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
