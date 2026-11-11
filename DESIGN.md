# Design System — SmartKrishi

Documented from the implemented SmartKrishi frontend (`frontend/src/index.css`, `frontend/tailwind.config.js`, and component library).

## Visual Direction & Color Tokens

- **Canvas (`--sk-bg-canvas`):** `#0B0F0D` (deep forest-tinted charcoal)
- **Primary Reading Surface (`--sk-bg-surface`):** `#121815` (opaque dark card/form container ensuring >=7:1 text readability)
- **Elevated Interactive Surface (`--sk-bg-elevated`):** `#18211C`
- **Selective Glassmorphism (`.sk-glass-nav`, `.sk-glass-panel`):** `rgba(14, 20, 17, 0.84)` with `backdrop-filter: blur(14px)` and `1px solid rgba(226, 232, 228, 0.11)`, reserved strictly for the sticky navigation bar, active drawer overlays, and the hero pipeline summary panel.
- **Foreground Ink (`--sk-text-primary`):** `#F2F4F0`
- **Secondary Text (`--sk-text-secondary`):** `#B6C0B9`
- **Muted Metadata:** `#85948A`
- **Primary Accent (`--sk-accent`):** `#52B788` (deep accent `#2D6A4F`) with `#08120D` button ink
- **Semantic Status Colors:** Warning `#D99B4E`, Danger/Conflict `#E06C65`, Info `#68A8B8`

## Typography

- **UI & Multilingual Body:** `"Public Sans"`, `"Noto Sans Kannada"`, `system-ui`, `sans-serif`
- **Tabular Measurements & Numeric Data:** `"JetBrains Mono"` with `font-variant-numeric: tabular-nums` applied strictly to soil pH, NPK, rainfall, duration, scores, and INR comparison ranges.
- **Line Measure & Accessibility:** Prose content constrained to `65-70ch`; visible `2px solid #52B788` focus rings; custom dark scrollbar and text selection styling.

## Components & Motion

- **Buttons:** Rectangular with subtle `6px` radius (`.sk-btn-primary`, `.sk-btn-secondary`), `>=44px` touch target height, restrained hover brighten and `1px` press response. No pill gradients or glowing borders.
- **Icons & Visuals:** Consistent `lucide-react` stroke icons across all controls and navigation; custom botanical SVG brand mark, favicon (`favicon.svg`, `favicon.ico`, `favicon-32x32.png`), and 26 local botanical crop SVG illustrations (`frontend/public/crops/*.svg`).
- **Welcome Animation (`WelcomeAnimation.tsx`):** SVG/CSS botanical growth sequence (circular reveal -> seed -> root -> stem -> 3 leaves -> SmartKrishi wordmark -> fade out) playing once per session with immediate "Skip intro" button and full `prefers-reduced-motion: reduce` bypass.
