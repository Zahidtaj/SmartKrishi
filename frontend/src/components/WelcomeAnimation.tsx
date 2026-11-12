import { useEffect, useState } from "react";
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

    const fadeTimer = window.setTimeout(() => setFadingOut(true), 2300);
    const doneTimer = window.setTimeout(() => onComplete(), 2720);
    return () => {
      window.clearTimeout(fadeTimer);
      window.clearTimeout(doneTimer);
    };
  }, [onComplete]);

  return (
    <div
      role="dialog"
      aria-label="SmartKrishi introduction"
      className={`fixed inset-0 z-50 flex flex-col items-center justify-center bg-canvas px-6 transition-opacity duration-500 ${
        fadingOut ? "opacity-0 pointer-events-none" : "opacity-100"
      }`}
    >
      <div className="relative flex max-w-md flex-col items-center text-center">
        {/* Radial subtle ambient glow behind germination canvas */}
        <div
          aria-hidden="true"
          className="pointer-events-none absolute -top-10 h-56 w-56 rounded-full bg-accent/15 blur-3xl"
        />

        <svg
          width="160"
          height="160"
          viewBox="0 0 160 160"
          fill="none"
          aria-hidden="true"
          className="relative mb-6"
        >
          {/* Outer botanical agro-zone concentric rings */}
          <circle
            cx="80"
            cy="80"
            r="68"
            stroke="currentColor"
            strokeOpacity="0.16"
            strokeWidth="1"
            className="text-accent sk-anim-ring"
          />
          <circle
            cx="80"
            cy="80"
            r="56"
            stroke="currentColor"
            strokeOpacity="0.4"
            strokeWidth="1.5"
            strokeDasharray="10 8"
            className="text-accent sk-anim-orbit"
          />
          <circle
            cx="80"
            cy="80"
            r="44"
            fill="currentColor"
            fillOpacity="0.06"
            stroke="currentColor"
            strokeOpacity="0.24"
            strokeWidth="1"
            className="text-accent sk-anim-ring"
          />

          {/* Soil horizon curve */}
          <path
            d="M40 108 Q80 102 120 108"
            stroke="currentColor"
            strokeOpacity="0.45"
            strokeWidth="2"
            strokeLinecap="round"
            className="text-muted"
          />

          {/* Seed */}
          <ellipse cx="80" cy="106" rx="5.5" ry="3.8" fill="#D99B4E" className="sk-anim-seed" />

          {/* Root network drawing downwards */}
          <path
            d="M80 110 C80 118, 75 123, 70 129 M80 111 C83 118, 88 123, 92 128 M80 114 L80 131"
            stroke="#88998F"
            strokeWidth="1.8"
            strokeLinecap="round"
            className="sk-anim-root"
          />

          {/* Central stem drawing upwards */}
          <path
            d="M80 104 C80 86, 80 68, 80 42"
            stroke="currentColor"
            strokeWidth="2.8"
            strokeLinecap="round"
            className="text-accent sk-anim-stem"
          />

          {/* Emerging paired leaves & crown shoot */}
          <path
            d="M80 88 C64 88, 54 79, 52 66 C64 66, 75 74, 80 88 Z"
            fill="currentColor"
            fillOpacity="0.28"
            stroke="currentColor"
            strokeWidth="2.1"
            strokeLinejoin="round"
            className="text-accent sk-anim-leaf-1"
          />
          <path
            d="M80 72 C96 72, 106 63, 108 50 C96 50, 85 58, 80 72 Z"
            fill="currentColor"
            fillOpacity="0.44"
            stroke="currentColor"
            strokeWidth="2.1"
            strokeLinejoin="round"
            className="text-accent sk-anim-leaf-2"
          />
          <path
            d="M80 54 C70 47, 65 37, 68 27 C77 31, 82 40, 80 54 Z"
            fill="currentColor"
            fillOpacity="0.68"
            stroke="currentColor"
            strokeWidth="2.1"
            strokeLinejoin="round"
            className="text-accent sk-anim-leaf-3"
          />
        </svg>

        <div className="sk-anim-wordmark">
          <h1 className="text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
            SmartKrishi
          </h1>
          <p className="mt-2 text-sm text-secondary sm:text-base">{t.welcome.subtitle}</p>
        </div>

        {/* Minimal fluid progress indicator (no skip button) */}
        <div
          aria-hidden="true"
          className="mt-8 h-1 w-44 overflow-hidden rounded-full bg-ink/10"
        >
          <div className="h-full w-full rounded-full bg-accent sk-anim-bar" />
        </div>
      </div>
    </div>
  );
}
