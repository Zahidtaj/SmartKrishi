export interface OptionCopy {
  label: string;
  desc?: string;
}

export interface TranslationDictionary {
  brandName: string;
  brandTagline: string;
  nav: {
    home: string;
    recommend: string;
    compare: string;
    soilHealth: string;
    knowledge: string;
    admin: string;
    languageLabel: string;
    openMenu: string;
    closeMenu: string;
    switchToLight: string;
    switchToDark: string;
  };
  welcome: {
    subtitle: string;
  };
  home: {
    headline: string;
    subheadline: string;
    primaryCta: string;
    secondaryCta: string;
    howTitle: string;
    howIntro: string;
    step1Title: string;
    step1Body: string;
    step2Title: string;
    step2Body: string;
    step3Title: string;
    step3Body: string;
    capabilitiesTitle: string;
    cap1Title: string;
    cap1Body: string;
    cap2Title: string;
    cap2Body: string;
    cap3Title: string;
    cap3Body: string;
    cap4Title: string;
    cap4Body: string;
    limitsTitle: string;
    limitsPoints: string[];
  };
  wizard: {
    pageTitle: string;
    pageSubtitle: string;
    stepOf: string;
    optionalBadge: string;
    next: string;
    back: string;
    submit: string;
    submitting: string;
    selectOption: string;
    steps: {
      location: { title: string; subtitle: string };
      soilColor: { title: string; subtitle: string; question: string; disclaimer: string };
      soilTexture: { title: string; subtitle: string; question: string; guideTitle: string; guideBody: string };
      drainage: { title: string; subtitle: string; qRain: string; qMoisture: string };
      land: { title: string; subtitle: string; qTopo: string; qDepth: string; qStones: string; qWaterlog: string; qErosion: string };
      water: { title: string; subtitle: string; qSource: string; qReliability: string };
      history: { title: string; subtitle: string; qPrevCrop: string; qSuccess: string; qDrought: string; qFlood: string; qPests: string; qArea: string };
      season: { title: string; subtitle: string; qSeason: string; qMonth: string; qDuration: string; qPriority: string };
    };
    fields: {
      state: string;
      district: string;
      taluk: string;
      village: string;
      agroZone: string;
      zoneRefHint: string;
      majorCropsLabel: string;
      prevCropPlaceholder: string;
      pestPlaceholder: string;
      areaPlaceholder: string;
      monthAny: string;
    };
    colors: Record<string, OptionCopy>;
    textures: Record<string, OptionCopy>;
    drainages: Record<string, OptionCopy>;
    moistures: Record<string, OptionCopy>;
    topographies: Record<string, OptionCopy>;
    depths: Record<string, OptionCopy>;
    stones: Record<string, OptionCopy>;
    waterlogs: Record<string, OptionCopy>;
    erosions: Record<string, OptionCopy>;
    waterSources: Record<string, OptionCopy>;
    waterReliabilities: Record<string, OptionCopy>;
    seasons: Record<string, OptionCopy>;
    durations: Record<string, OptionCopy>;
    priorities: Record<string, OptionCopy>;
    yesNoUncertain: Record<string, string>;
    successOptions: Record<string, string>;
  };
  results: {
    pageTitle: string;
    editInputs: string;
    compareSelected: string;
    printReport: string;
    modeLabel: string;
    confidenceLabel: string;
    insufficientTitle: string;
    reasonsTitle: string;
    limitationsTitle: string;
    missingTitle: string;
    guidanceTitle: string;
    dimensionsTitle: string;
    soilObsTitle: string;
    weatherAdvisoryTitle: string;
    climateNormalsLabel: string;
    currentWeatherLabel: string;
    forecastLabel: string;
    seasonalOutlookLabel: string;
    sowingSuitabilityLabel: string;
    heavyRainRiskLabel: string;
    drySpellRiskLabel: string;
    irrigationPlanLabel: string;
    provenanceTitle: string;
    waterNeed: string;
    seasonLabel: string;
    durationLabel: string;
    daysUnit: string;
    sourceLabel: string;
    viewDetails: string;
    feedbackTitle: string;
    feedbackPrompt: string;
    feedbackSubmit: string;
    feedbackSuccess: string;
  };
  compare: {
    pageTitle: string;
    pageSubtitle: string;
    selectCrops: string;
    landAreaLabel: string;
    runCompare: string;
    assumptionsTitle: string;
    unavailableText: string;
  };
  soilHealth: {
    pageTitle: string;
    pageSubtitle: string;
    observeButton: string;
    optionalLabTitle: string;
    optionalLabSubtitle: string;
    analyzeButton: string;
    shcFutureTitle: string;
    shcFutureBody: string;
  };
  knowledge: {
    pageTitle: string;
    pageSubtitle: string;
    searchPlaceholder: string;
    allCategories: string;
    sourceLabel: string;
    readArticle: string;
    backToLibrary: string;
  };
  footer: {
    projectNote: string;
    privacy: string;
    terms: string;
    disclaimer: string;
  };
}
