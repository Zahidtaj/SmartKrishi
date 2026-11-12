import { Link } from "react-router-dom";
import { useI18n } from "../i18n";

export function Footer() {
  const { t } = useI18n();

  return (
    <footer className="border-t border-ink/10 bg-surface/90 mt-16 no-print">
      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="grid gap-8 md:grid-cols-3">
          <div>
            <div className="flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-accent" aria-hidden="true" />
              <span className="text-base font-semibold text-ink">SmartKrishi</span>
            </div>
            <p className="mt-2 max-w-sm text-sm text-secondary">{t.footer.projectNote}</p>
          </div>

          <div>
            <h2 className="text-sm font-semibold text-ink">{t.nav.knowledge}</h2>
            <ul className="mt-2.5 space-y-2 text-sm text-secondary">
              <li>
                <Link to="/recommend" className="hover:text-accent transition-colors">
                  {t.nav.recommend}
                </Link>
              </li>
              <li>
                <Link to="/compare" className="hover:text-accent transition-colors">
                  {t.nav.compare}
                </Link>
              </li>
              <li>
                <Link to="/soil-health" className="hover:text-accent transition-colors">
                  {t.nav.soilHealth}
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h2 className="text-sm font-semibold text-ink">Governance & Legal</h2>
            <ul className="mt-2.5 space-y-2 text-sm text-secondary">
              <li>
                <Link to="/privacy-policy" className="hover:text-accent transition-colors">
                  {t.footer.privacy}
                </Link>
              </li>
              <li>
                <Link to="/terms" className="hover:text-accent transition-colors">
                  {t.footer.terms}
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-8 border-t border-ink/10 pt-6 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between text-xs text-muted">
          <p>{t.footer.disclaimer}</p>
          <p className="shrink-0">© {new Date().getFullYear()} SmartKrishi VTU Community Project</p>
        </div>
      </div>
    </footer>
  );
}
