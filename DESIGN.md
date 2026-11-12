# Design System — SmartKrishi

Documented from the implemented SmartKrishi frontend (`frontend/src/index.css`, `frontend/tailwind.config.js`, `ThemeContext.tsx`, and component library).

## Visual Direction, Dual Theme & Color Tokens

SmartKrishi supports both **Dark Mode** (`html.dark`, deep forest-emerald inspired analytics palette) and **Light Mode** (`html.light`, warm field-parchment palette), switched smoothly via a circular clip-path `View Transitions API` reveal originating at the navbar toggle button (`--theme-x`, `--theme-y`, `--theme-r`).

### Dark Theme (`html.dark`, default)
- **Canvas (`--sk-bg-canvas`):** `rgb(7 17 13)` (`#07110D`)
- **Primary Reading Surface (`--sk-bg-surface`):** `rgb(12 29 22)` (`#0C1D16`)
- **Elevated Interactive Surface (`--sk-bg-elevated`):** `rgb(19 42 32)` (`#132A20`)
- **Foreground Ink (`--sk-text-primary`):** `rgb(239 246 242)`
- **Secondary Ink (`--sk-text-secondary`):** `rgb(176 196 184)`
- **Muted Metadata:** `rgb(122 146 132)`
- **Primary Accent (`--sk-accent`):** `rgb(45 212 135)` (`#2DD487`) with `#04150D` button ink

### Light Theme (`html.light`)
- **Canvas (`--sk-bg-canvas`):** `rgb(245 247 244)` (`#F5F7F4`)
- **Primary Reading Surface (`--sk-bg-surface`):** `rgb(255 255 255)`
- **Elevated Interactive Surface (`--sk-bg-elevated`):** `rgb(234 242 237)`
- **Foreground Ink (`--sk-text-primary`):** `rgb(15 36 26)`
- **Primary Accent (`--sk-accent`):** `rgb(16 140 84)`

## Typography

- **UI & Multilingual Body:** `"Public Sans"`, `"Noto Sans Kannada"`, `system-ui`, `sans-serif`
- **Tabular Measurements & Numeric Data:** `"JetBrains Mono"` with `font-variant-numeric: tabular-nums` applied strictly to rainfall ranges, growing duration, suitability scores, and INR comparison ranges.
- **Line Measure & Accessibility:** Prose content constrained to `65-70ch`; visible `2px solid rgb(var(--sk-accent))` focus rings.

## Components, Visual Assets & Motion

- **Animated Buttons & Choice Cards (`.sk-btn-primary`, `.sk-btn-secondary`, `.sk-choice-card`):** `>=44px` touch target height, smooth transform/shadow hover states, active press feedback, and step entrance transition (`.sk-step-enter`).
- **Icons & Visuals:** Consistent `lucide-react` stroke icons across navigation and controls; custom botanical SVG brand mark and favicons; 26 local botanical crop SVG illustrations (`frontend/public/crops/*.svg`); and **8 authentic educational soil swatch SVGs** (`frontend/public/soils/*.svg`) for observation-based soil appearance selection.
- **Welcome Animation (`WelcomeAnimation.tsx`):** Botanical seed -> root -> stem -> leaves -> orbit -> SmartKrishi wordmark SVG splash playing once per session with automatic transition (~2.7s), **no "Skip intro" button**, and full `prefers-reduced-motion: reduce` support.
