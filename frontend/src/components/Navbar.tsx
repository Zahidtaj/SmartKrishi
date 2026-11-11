import { useState } from "react";
import { NavLink } from "react-router-dom";
import { Globe, Menu, ShieldCheck, X } from "lucide-react";
import { useI18n } from "../i18n";

export function Navbar() {
  const { lang, setLang, t } = useI18n();
  const [mobileOpen, setMobileOpen] = useState(false);

  const navItems = [
    { to: "/", label: t.nav.home, end: true },
    { to: "/recommend", label: t.nav.recommend, end: false },
    { to: "/compare", label: t.nav.compare, end: false },
    { to: "/soil-health", label: t.nav.soilHealth, end: false },
    { to: "/knowledge", label: t.nav.knowledge, end: false },
  ];

  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `inline-flex items-center min-h-[40px] px-3 py-2 rounded-md text-sm font-medium transition-colors ${
      isActive
        ? "bg-elevated text-accent border border-accent/30"
        : "text-secondary hover:text-ink hover:bg-elevated/60"
    }`;

  return (
    <header className="sk-glass-nav sticky top-0 z-40 w-full no-print">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-3 focus:z-50 focus:rounded-md focus:bg-accent focus:px-4 focus:py-2 focus:text-sm focus:font-semibold focus:text-canvas"
      >
        Skip to content
      </a>

      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-4 px-4 sm:px-6 lg:px-8">
        <NavLink to="/" className="flex items-center gap-2.5 text-ink focus-visible:outline-accent">
          <svg width="28" height="28" viewBox="0 0 64 64" fill="none" aria-hidden="true">
            <circle cx="32" cy="32" r="26" stroke="#2D6A4F" strokeWidth="2.5" />
            <path d="M32 48V24" stroke="#52B788" strokeWidth="3.2" strokeLinecap="round" />
            <path d="M32 34C24 34 19 28 19 21C26 21 32 26 32 34Z" fill="#52B788" fillOpacity="0.35" stroke="#52B788" strokeWidth="2.2" />
            <path d="M32 28C40 28 45 22 45 15C38 15 32 20 32 28Z" fill="#52B788" fillOpacity="0.65" stroke="#52B788" strokeWidth="2.2" />
          </svg>
          <span className="text-lg font-semibold tracking-tight text-ink">SmartKrishi</span>
        </NavLink>

        {/* Desktop navigation */}
        <nav aria-label="Primary navigation" className="hidden items-center gap-1 lg:flex">
          {navItems.map((item) => (
            <NavLink key={item.to} to={item.to} end={item.end} className={linkClass}>
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="flex items-center gap-2.5">
          {/* Bilingual switcher */}
          <div
            role="group"
            aria-label={t.nav.languageLabel}
            className="inline-flex items-center rounded-md border border-white/15 bg-surface p-0.5"
          >
            <Globe className="ml-2 mr-1 h-4 w-4 text-muted" aria-hidden="true" />
            <button
              type="button"
              onClick={() => setLang("en")}
              aria-pressed={lang === "en"}
              className={`min-h-[34px] rounded px-2.5 text-xs font-semibold transition-colors ${
                lang === "en" ? "bg-accent text-canvas" : "text-secondary hover:text-ink"
              }`}
            >
              EN
            </button>
            <button
              type="button"
              onClick={() => setLang("kn")}
              aria-pressed={lang === "kn"}
              className={`min-h-[34px] rounded px-2.5 text-xs font-semibold transition-colors ${
                lang === "kn" ? "bg-accent text-canvas" : "text-secondary hover:text-ink"
              }`}
            >
              ಕನ್ನಡ
            </button>
          </div>

          <NavLink
            to="/admin"
            className="hidden sm:inline-flex items-center gap-1.5 min-h-[38px] rounded-md border border-white/15 px-3 py-1.5 text-xs font-medium text-secondary hover:text-ink hover:bg-elevated"
          >
            <ShieldCheck className="h-3.5 w-3.5 text-accent" aria-hidden="true" />
            <span>{t.nav.admin}</span>
          </NavLink>

          <button
            type="button"
            onClick={() => setMobileOpen((prev) => !prev)}
            aria-expanded={mobileOpen}
            aria-label={mobileOpen ? t.nav.closeMenu : t.nav.openMenu}
            className="inline-flex h-11 w-11 items-center justify-center rounded-md border border-white/15 text-ink hover:bg-elevated lg:hidden"
          >
            {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {/* Mobile navigation drawer */}
      {mobileOpen && (
        <nav
          aria-label="Mobile navigation"
          className="border-t border-white/10 bg-canvas px-4 py-4 lg:hidden"
        >
          <div className="flex flex-col gap-1.5">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                onClick={() => setMobileOpen(false)}
                className={linkClass}
              >
                {item.label}
              </NavLink>
            ))}
            <NavLink
              to="/admin"
              onClick={() => setMobileOpen(false)}
              className={linkClass}
            >
              <ShieldCheck className="mr-2 h-4 w-4 text-accent" aria-hidden="true" />
              {t.nav.admin}
            </NavLink>
          </div>
        </nav>
      )}
    </header>
  );
}
