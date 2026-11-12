import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

export type ThemeMode = "dark" | "light";

interface ThemeContextValue {
  theme: ThemeMode;
  toggleTheme: (origin?: { clientX: number; clientY: number }) => void;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

const STORAGE_KEY = "smartkrishi_theme";

function applyDomTheme(mode: ThemeMode) {
  const root = document.documentElement;
  root.classList.remove("dark", "light");
  root.classList.add(mode);
  root.style.colorScheme = mode;
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<ThemeMode>(() => {
    if (typeof window === "undefined") return "dark";
    const saved = window.localStorage.getItem(STORAGE_KEY);
    return saved === "light" ? "light" : "dark";
  });

  useEffect(() => {
    applyDomTheme(theme);
    window.localStorage.setItem(STORAGE_KEY, theme);
  }, [theme]);

  const toggleTheme = (origin?: { clientX: number; clientY: number }) => {
    const next: ThemeMode = theme === "dark" ? "light" : "dark";
    const root = document.documentElement;
    if (origin) {
      root.style.setProperty("--theme-x", `${origin.clientX}px`);
      root.style.setProperty("--theme-y", `${origin.clientY}px`);
    } else {
      root.style.setProperty("--theme-x", "90%");
      root.style.setProperty("--theme-y", "28px");
    }

    const prefersReduced =
      typeof window !== "undefined" &&
      typeof window.matchMedia === "function" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const docWithTransition = document as Document & {
      startViewTransition?: (cb: () => void) => { finished: Promise<void> };
    };

    if (!prefersReduced && typeof docWithTransition.startViewTransition === "function") {
      docWithTransition.startViewTransition(() => {
        applyDomTheme(next);
        setTheme(next);
      });
    } else {
      setTheme(next);
    }
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme(): ThemeContextValue {
  const ctx = useContext(ThemeContext);
  if (!ctx) {
    throw new Error("useTheme must be used inside ThemeProvider");
  }
  return ctx;
}
