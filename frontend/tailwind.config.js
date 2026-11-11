/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Public Sans"', '"Noto Sans Kannada"', "system-ui", "sans-serif"],
        mono: ['"JetBrains Mono"', "ui-monospace", "monospace"],
      },
      colors: {
        canvas: "#0B0F0D",
        surface: "#121815",
        elevated: "#18211C",
        ink: "#F2F4F0",
        secondary: "#B6C0B9",
        muted: "#85948A",
        accent: "#52B788",
        "accent-deep": "#2D6A4F",
        warning: "#D99B4E",
        danger: "#E06C65",
        info: "#68A8B8",
      },
    },
  },
  plugins: [],
};
