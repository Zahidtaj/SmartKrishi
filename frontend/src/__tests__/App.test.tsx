import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";

function mockFetchImplementation(url: string, init?: RequestInit) {
  const path = url.toString();

  if (path.includes("/api/locations/states")) {
    return Promise.resolve(new Response(JSON.stringify({ states: ["Karnataka"] }), { status: 200 }));
  }
  if (path.includes("/api/locations/districts")) {
    return Promise.resolve(
      new Response(
        JSON.stringify({
          state: "Karnataka",
          districts: [
            { district: "Tumakuru", agro_climatic_zone: "Eastern Dry Zone", zone_code: "KA-Z5", taluk_count: 5 },
            { district: "Mandya", agro_climatic_zone: "Southern Dry Zone", zone_code: "KA-Z6", taluk_count: 5 },
          ],
        }),
        { status: 200 }
      )
    );
  }
  if (path.includes("/api/locations/taluks")) {
    return Promise.resolve(
      new Response(
        JSON.stringify({
          state: "Karnataka",
          district: "Tumakuru",
          taluks: [
            {
              id: 1,
              taluk: "Tumakuru",
              agro_climatic_zone: "Eastern Dry Zone",
              zone_code: "KA-Z5",
              normal_annual_rainfall_mm: 740,
              typical_rainfall_pattern: "Bimodal (~700-850 mm/year)",
              dominant_soil_types: ["Red", "Loamy"],
              common_soil_textures: ["loamy", "sandy"],
              major_crops: ["Ragi (Finger Millet)", "Groundnut", "Maize"],
              recommended_seasons_summary: { Kharif: "June to October" },
              growing_period_info: "115-145 days",
              regional_references: ["UAS Bengaluru Package of Practices"],
              data_source: "Karnataka NARP 10 Zones",
              verification_status: "verified_institutional_reference",
              last_updated: "2026-05-01",
            },
          ],
        }),
        { status: 200 }
      )
    );
  }
  if (path.includes("/api/soil/observe")) {
    return Promise.resolve(
      new Response(
        JSON.stringify({
          soil_color: "red",
          soil_color_label_en: "Red soil appearance",
          soil_color_label_kn: "ಕೆಂಪು ಮಣ್ಣು",
          color_disclaimer_en: "Visual soil colour cannot measure pH or N-P-K nutrients.",
          color_disclaimer_kn: "ಬಣ್ಣದಿಂದ pH ಅಳೆಯಲು ಸಾಧ್ಯವಿಲ್ಲ.",
          soil_texture: "loamy",
          effective_drainage: "well_drained",
          effective_moisture_retention: "moderate_retention",
          soil_depth: "medium",
          visible_stones: "none_few",
          waterlogging_issue: "none",
          erosion_issue: "none",
          observation_confidence: "high",
          unknown_fields: [],
          insights_en: ["Red colour reflects upland iron oxides; texture and drainage govern water handling."],
          insights_kn: ["ಕೆಂಪು ಬಣ್ಣವು ಪ್ರಾಥಮಿಕ ಸೂಚನೆಯಾಗಿದೆ."],
          management_guidance_en: ["Confirm seasonal moisture before sowing."],
          management_guidance_kn: ["ಬಿತ್ತನೆಗೆ ಮುನ್ನ ತೇವಾಂಶ ಗಮನಿಸಿ."],
          optional_lab_note_en: "Soil Health Card optional at RSK/KVK.",
          optional_lab_note_kn: "ಮಣ್ಣು ಆರೋಗ್ಯ ಕಾರ್ಡ್ ಐಚ್ಛಿಕ.",
        }),
        { status: 200 }
      )
    );
  }
  if (path.includes("/api/recommendations") && init?.method === "POST") {
    return Promise.resolve(
      new Response(
        JSON.stringify({
          recommendation_id: 101,
          created_at: "2026-11-12T10:00:00Z",
          mode_used: "observation_rule_based",
          confidence_level: "moderate",
          scoring_notice_en: "Prototype suitability index based on field observations.",
          scoring_notice_kn: "ಕ್ಷೇತ್ರ ವೀಕ್ಷಣೆ ಆಧಾರಿತ ಮಾದರಿ ಸೂಚ್ಯಂಕ.",
          disclaimer_en: "Consult RSK/KVK before investment.",
          disclaimer_kn: "RSK/KVK ಸಂಪರ್ಕಿಸಿ.",
          warnings: [],
          missing_information: ["live_weather_forecast"],
          insufficient_data_reason: null,
          location_context: {
            state: "Karnataka",
            district: "Tumakuru",
            taluk: "Tumakuru",
            agro_climatic_zone: "Eastern Dry Zone",
            zone_code: "KA-Z5",
            normal_annual_rainfall_mm: 740,
            typical_rainfall_pattern: "Bimodal",
            dominant_soil_types: ["Red", "Loamy"],
            common_soil_textures: ["loamy", "sandy"],
            major_crops: ["Ragi", "Groundnut"],
            recommended_seasons_summary: {},
            growing_period_info: "115-145 days",
            regional_references: ["UAS Bengaluru"],
            data_source: "Karnataka NARP",
            verification_status: "verified_institutional_reference",
            last_updated: "2026-05-01",
          },
          soil_interpretation: {
            soil_color: "red",
            soil_color_label_en: "Red soil appearance",
            soil_color_label_kn: "ಕೆಂಪು ಮಣ್ಣು",
            color_disclaimer_en: "Soil colour alone cannot measure pH or NPK.",
            color_disclaimer_kn: "ಬಣ್ಣದಿಂದ pH ಅಳೆಯಲು ಸಾಧ್ಯವಿಲ್ಲ.",
            soil_texture: "loamy",
            effective_drainage: "well_drained",
            effective_moisture_retention: "moderate_retention",
            soil_depth: "medium",
            visible_stones: "none_few",
            waterlogging_issue: "none",
            erosion_issue: "none",
            observation_confidence: "high",
            unknown_fields: [],
            insights_en: ["Loamy soil balances drainage and moisture."],
            insights_kn: ["ಗೋಡು ಮಣ್ಣು ಸಮತೋಲನ ಹೊಂದಿದೆ."],
            management_guidance_en: ["Practice mulching during dry intervals."],
            management_guidance_kn: ["ಹೊದಿಕೆ ಬಳಸಿ."],
            optional_lab_note_en: "SHC optional.",
            optional_lab_note_kn: "SHC ಐಚ್ಛಿಕ.",
          },
          weather_advisory: {
            long_term_climate: {
              status: "available",
              data_category: "institution_sourced",
              zone_name: "Eastern Dry Zone",
              zone_code: "KA-Z5",
              normal_annual_rainfall_mm: 740,
              typical_rainfall_pattern: "Bimodal (~700-850 mm/year)",
              season_reference: "Kharif",
              season_normal_temp_c: 25.5,
              season_normal_humidity_pct: 74,
              season_normal_rainfall_mm: 540,
              growing_period_info: "115-145 days",
              source: "Karnataka NARP",
              verification_status: "verified_institutional_reference",
              last_updated: "2026-05-01",
            },
            current_weather: {
              status: "unavailable",
              data_category: "weather_provider_sourced",
              provider: "IMD Agromet",
              temperature_c: null,
              humidity_pct: null,
              precipitation_mm: null,
              reason_en: "Live weather feed unavailable.",
              reason_kn: "ನೇರ ಹವಾಮಾನ ಲಭ್ಯವಿಲ್ಲ.",
            },
            short_term_forecast: {
              status: "unavailable",
              data_category: "weather_provider_sourced",
              provider: "IMD 5-Day Forecast",
              next_7_days_rain_total_mm: null,
              peak_daily_rain_mm: null,
              reason_en: "Forecast unavailable offline.",
              reason_kn: "ಮುನ್ಸೂಚನೆ ಲಭ್ಯವಿಲ್ಲ.",
            },
            seasonal_outlook: {
              status: "reference_normal",
              data_category: "institution_sourced",
              outlook_summary_en: "Historical bimodal monsoon pattern.",
              outlook_summary_kn: "ದೀರ್ಘಕಾಲೀನ ಮಳೆ ಮಾದರಿ.",
              recommended_window_en: "June to October",
              recommended_window_kn: "ಜೂನ್ - ಅಕ್ಟೋಬರ್",
              limitation_en: "Historical normals only.",
              limitation_kn: "ಸರಾಸರಿ ಮಾಹಿತಿ ಮಾತ್ರ.",
            },
            farming_advisory: {
              advisory_basis: "zone_climate_normals_only_live_unavailable",
              live_weather_available: false,
              sowing_suitability_en: "Confirm top-15cm soil moisture before Kharif sowing.",
              sowing_suitability_kn: "ತೇವಾಂಶ ಖಚಿತಪಡಿಸಿ ಬಿತ್ತನೆ ಮಾಡಿ.",
              heavy_rainfall_risk_level: "low",
              heavy_rainfall_risk_en: "Low flood risk under dry zone normals.",
              heavy_rainfall_risk_kn: "ಅಪಾಯ ಕಡಿಮೆ.",
              dry_spell_risk_level: "moderate",
              dry_spell_risk_en: "Protective moisture conservation helpful.",
              dry_spell_risk_kn: "ತೇವಾಂಶ ರಕ್ಷಣೆ ಅಗತ್ಯ.",
              irrigation_planning_en: "Apply protective irrigation during flowering.",
              irrigation_planning_kn: "ಹೂಬಿಡುವ ಹಂತದಲ್ಲಿ ನೀರಾವರಿ ನೀಡಿ.",
            },
          },
          input_provenance: {
            farmer_observed: { label: "Farmer Observations", fields: ["soil_color=red"] },
            institution_sourced: {
              label: "Verified Institutional Data",
              sources: ["UAS Bengaluru"],
              location_verification_status: "verified_institutional_reference",
              location_last_updated: "2026-05-01",
            },
            weather_provider_sourced: {
              label: "Weather Provider",
              current_weather_status: "unavailable",
              short_term_forecast_status: "unavailable",
              provider: "IMD Agromet",
            },
            demonstration_data: { label: "Demonstration", note: "Prototype scoring index." },
          },
          input_summary: {},
          recommendations: [
            {
              rank: 1,
              crop_id: 2,
              crop_key: "ragi",
              name_en: "Ragi (Finger Millet)",
              name_kn: "ರಾಗಿ",
              scientific_name: "Eleusine coracana",
              category: "Millet",
              image_asset: "/crops/ragi.svg",
              suitability_category: "Highly Suitable (Prototype Fit)",
              illustrative_score: 91.5,
              dimension_scores: {
                location: 100,
                soil_land: 95,
                water: 95,
                seasonal: 100,
                climate: 90,
                priority_history: 82,
              },
              reasons_en: ["Documented crop in Eastern Dry Zone for Kharif season."],
              reasons_kn: ["ಪೂರ್ವ ಒಣ ವಲಯದ ಖರೀಫ್ ಬೆಳೆ."],
              limitations_en: ["Ensure timely weeding at 25 days."],
              limitations_kn: ["25 ದಿನಗಳಲ್ಲಿ ಕಳೆ ತೆಗೆಯಿರಿ."],
              missing_info_en: ["Live 7-day forecast unavailable."],
              missing_info_kn: ["7 ದಿನದ ಮುನ್ಸೂಚನೆ ಲಭ್ಯವಿಲ್ಲ."],
              compatibility_badges: { region: "recommended" },
              conflict_flags: [],
              water_requirement_level: "Low",
              water_requirement_mm_min: 350,
              water_requirement_mm_max: 550,
              suitable_seasons: ["Kharif", "Rabi"],
              growing_duration_days_min: 100,
              growing_duration_days_max: 120,
              cultivation_guidance_en: "Line sow at 22.5-30 cm spacing.",
              cultivation_guidance_kn: "ಸಾಲಿನಲ್ಲಿ ಬಿತ್ತನೆ ಮಾಡಿ.",
              information_source: "UAS Bengaluru",
              record_status: "verified_reference",
            },
          ],
        }),
        { status: 201 }
      )
    );
  }
  return Promise.resolve(new Response(JSON.stringify([]), { status: 200 }));
}

describe("SmartKrishi Observation-Based UI Tests", () => {
  beforeEach(() => {
    window.localStorage.clear();
    window.sessionStorage.setItem("smartkrishi_intro_seen", "1");
    window.history.pushState({}, "", "/");
    window.scrollTo = vi.fn();
    vi.stubGlobal("fetch", vi.fn(mockFetchImplementation));
  });

  it("renders intro overlay WITHOUT Skip intro button when intro not yet seen", () => {
    window.sessionStorage.removeItem("smartkrishi_intro_seen");
    render(<App />);
    expect(screen.getByRole("dialog", { name: /SmartKrishi introduction/i })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /skip intro/i })).not.toBeInTheDocument();
  });

  it("toggles dark/light theme and switches English <-> Kannada smoothly", async () => {
    const user = userEvent.setup();
    render(<App />);

    const themeBtn = screen.getByRole("button", { name: /switch to light mode/i });
    await user.click(themeBtn);
    expect(document.documentElement.classList.contains("light")).toBe(true);

    const knBtn = screen.getByRole("button", { name: "ಕನ್ನಡ" });
    await user.click(knBtn);
    expect(screen.getAllByRole("link", { name: "ಬೆಳೆ ಸಲಹೆ" })[0]).toBeInTheDocument();

    const enBtn = screen.getByRole("button", { name: "EN" });
    await user.click(enBtn);
    expect(screen.getAllByRole("link", { name: "Crop Advisory" })[0]).toBeInTheDocument();
  });

  it("walks through all 8 observation steps and renders advisory & weather results", async () => {
    const user = userEvent.setup();
    window.history.pushState({}, "", "/recommend");
    render(<App />);

    await waitFor(() => {
      expect(screen.getByDisplayValue("Tumakuru")).toBeInTheDocument();
    });

    // Advance Steps 1 -> 8
    for (let s = 1; s <= 7; s++) {
      await user.click(screen.getByRole("button", { name: /Continue/i }));
    }

    await user.click(screen.getByRole("button", { name: /Generate Crop Advisory/i }));

    await waitFor(() => {
      expect(screen.getByText("Ragi (Finger Millet)")).toBeInTheDocument();
      expect(screen.getByText("Why this crop was recommended")).toBeInTheDocument();
      expect(screen.getByText("Weather and Farming Advisory")).toBeInTheDocument();
    });
  });

  it("runs observation-based soil interpreter on Soil Guide page", async () => {
    const user = userEvent.setup();
    window.history.pushState({}, "", "/soil-health");
    render(<App />);

    await user.click(screen.getByRole("button", { name: /Interpret My Soil Observations/i }));
    await waitFor(() => {
      expect(screen.getByText(/Red soil appearance/i)).toBeInTheDocument();
    });
  });
});
