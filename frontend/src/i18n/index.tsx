import React, { createContext, useContext, useEffect, useState } from "react";
import type { Language } from "../types";
import type { TranslationDictionary } from "./types";
import { en } from "./en";
import { kn } from "./kn";

// Architecture structured for extensible locale dictionaries (future Hindi `hi` support).
const dictionaries: Record<Language, TranslationDictionary> = { en, kn };

interface I18nContextValue {
  lang: Language;
  setLang: (next: Language) => void;
  t: TranslationDictionary;
}

const I18nContext = createContext<I18nContextValue | undefined>(undefined);

export function I18nProvider({ children }: { children: React.ReactNode }) {
  const [lang, setLangState] = useState<Language>(() => {
    const saved = localStorage.getItem("smartkrishi_lang");
    return saved === "kn" ? "kn" : "en";
  });

  const setLang = (next: Language) => {
    setLangState(next);
    localStorage.setItem("smartkrishi_lang", next);
  };

  useEffect(() => {
    document.documentElement.lang = lang;
  }, [lang]);

  return (
    <I18nContext.Provider value={{ lang, setLang, t: dictionaries[lang] }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useI18n(): I18nContextValue {
  const ctx = useContext(I18nContext);
  if (!ctx) {
    throw new Error("useI18n must be used within I18nProvider");
  }
  return ctx;
}
