/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Public Sans"', '"Noto Sans Kannada"', "system-ui", "sans-serif"],
        mono: ['"JetBrains Mono"', "ui-monospace", "monospace"],
      },
      colors: {
        canvas: "rgb(var(--sk-canvas-rgb) / <alpha-value>)",
        surface: "rgb(var(--sk-surface-rgb) / <alpha-value>)",
        elevated: "rgb(var(--sk-elevated-rgb) / <alpha-value>)",
        ink: "rgb(var(--sk-ink-rgb) / <alpha-value>)",
        secondary: "rgb(var(--sk-secondary-rgb) / <alpha-value>)",
        muted: "rgb(var(--sk-muted-rgb) / <alpha-value>)",
        accent: "rgb(var(--sk-accent-rgb) / <alpha-value>)",
        "accent-deep": "rgb(var(--sk-accent-deep-rgb) / <alpha-value>)",
        warning: "#D99B4E",
        danger: "#E06C65",
        info: "#4B97AD",
      },
    },
  },
  plugins: [],
};
