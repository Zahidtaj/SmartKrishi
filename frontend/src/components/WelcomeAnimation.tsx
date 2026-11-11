import { useEffect, useState } from "react";
import { ArrowRight } from "lucide-react";
import { useI18n } from "../i18n";

interface WelcomeAnimationProps {
  onComplete: () => void;
}

export function WelcomeAnimation({ onComplete }: WelcomeAnimationProps) {
  const { t } = useI18n();
  const [fadingOut, setFadingOut] = useState(false);

  useEffect(() => {
    const prefersReduced =
      typeof window !== "undefined" &&
      typeof window.matchMedia === "function" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (prefersReduced) {
      onComplete();
      return;
    }

    const fadeTimer = window.setTimeout(() => setFadingOut(true), 2350);
    const doneTimer = window.setTimeout(() => onComplete(), 2750);
    return () => {
      window.clearTimeout(fadeTimer);
      window.clearTimeout(doneTimer);
    };
  }, [onComplete]);

  return (
    <div
      role="dialog"
      aria-label="SmartKrishi introduction"
      className={`fixed inset-0 z-50 flex flex-col items-center justify-center bg-canvas px-6 transition-opacity duration-300 ${
        fadingOut ? "opacity-0 pointer-events-none" : "opacity-100"
      }`}
    >
      <div className="relative flex flex-col items-center text-center">
        <svg
          width="128"
          height="128"
          viewBox="0 0 128 128"
          fill="none"
          aria-hidden="true"
          className="mb-6"
        >
          {/* Step 2: Subtle circular visual reveal */}
          <circle
            cx="64"
            cy="64"
            r="52"
            stroke="#2D6A4F"
            strokeOpacity="0.55"
            strokeWidth="1.5"
            className="sk-anim-ring"
          />
          <circle
            cx="64"
            cy="64"
            r="42"
            stroke="#52B788"
            strokeOpacity="0.2"
            strokeWidth="1"
            className="sk-anim-ring"
          />

          {/* Ground horizon */}
          <line x1="34" y1="88" x2="94" y2="88" stroke="#85948A" strokeOpacity="0.5" strokeWidth="1.5" strokeLinecap="round" />

          {/* Step 3: Small seed */}
          <ellipse cx="64" cy="88" rx="4.5" ry="3.2" fill="#D99B4E" className="sk-anim-seed" />

          {/* Step 4: Root develops downward */}
          <path
            d="M64 90 C64 96, 61 101, 57 106 M64 92 C66 98, 69 102, 72 105"
            stroke="#85948A"
            strokeWidth="1.8"
            strokeLinecap="round"
            className="sk-anim-root"
          />

          {/* Step 5: Stem grows upward */}
          <path
            d="M64 87 C64 72, 64 56, 64 38"
            stroke="#52B788"
            strokeWidth="2.6"
            strokeLinecap="round"
            className="sk-anim-stem"
          />

          {/* Step 6: Three leaves emerge */}
          <path
            d="M64 72 C52 72, 44 65, 42 54 C52 54, 60 60, 64 72 Z"
            fill="#52B788"
            fillOpacity="0.32"
            stroke="#52B788"
            strokeWidth="2"
            strokeLinejoin="round"
            className="sk-anim-leaf-1"
          />
          <path
            d="M64 60 C76 60, 84 53, 86 42 C76 42, 68 48, 64 60 Z"
            fill="#52B788"
            fillOpacity="0.5"
            stroke="#52B788"
            strokeWidth="2"
            strokeLinejoin="round"
            className="sk-anim-leaf-2"
          />
          <path
            d="M64 48 C56 43, 52 35, 54 27 C61 30, 65 37, 64 48 Z"
            fill="#52B788"
            fillOpacity="0.72"
            stroke="#52B788"
            strokeWidth="2"
            strokeLinejoin="round"
            className="sk-anim-leaf-3"
          />
        </svg>

        {/* Step 7: SmartKrishi wordmark */}
        <div className="sk-anim-wordmark">
          <h1 className="text-2xl font-semibold tracking-tight text-ink sm:text-3xl">
            SmartKrishi
          </h1>
          <p className="mt-1.5 text-sm text-secondary">{t.welcome.subtitle}</p>
        </div>
      </div>

      <button
        type="button"
        onClick={onComplete}
        className="sk-btn-secondary mt-10 text-sm"
      >
        <span>{t.welcome.skip}</span>
        <ArrowRight className="h-4 w-4" aria-hidden="true" />
      </button>
    </div>
  );
}
