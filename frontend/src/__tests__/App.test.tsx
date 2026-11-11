import { render, screen, waitFor, within } from "@testing-library/react";
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
            { district: "Bengaluru Rural", agro_climatic_zone: "Eastern Dry Zone", zone_code: "KA-Z5", taluk_count: 4 },
            { district: "Mandya", agro_climatic_zone: "Southern Dry Zone", zone_code: "KA-Z6", taluk_count: 5 },
          ],
        }),
        { status: 200 }
      )
    );
  }
  if (path.includes("/api/locations/taluks")) {
    const isMandya = path.includes("Mandya");
    return Promise.resolve(
      new Response(
        JSON.stringify({
          state: "Karnataka",
          district: isMandya ? "Mandya" : "Bengaluru Rural",
          taluks: [
            {
              id: isMandya ? 2 : 1,
              taluk: isMandya ? "Maddur" : "Devanahalli",
              agro_climatic_zone: isMandya ? "Southern Dry Zone" : "Eastern Dry Zone",
              zone_code: isMandya ? "KA-Z6" : "KA-Z5",
              normal_annual_rainfall_mm: isMandya ? 725 : 790,
              dominant_soil_types: ["Red", "Loamy"],
              data_source: "Karnataka NARP",
            },
          ],
        }),
        { status: 200 }
      )
    );
  }
  if (path.includes("/api/crops/compare")) {
    return Promise.resolve(
      new Response(
        JSON.stringify({
          land_area_acres: 1,
          disclaimer_en: "Illustrative baseline only.",
          disclaimer_kn: "ಮಾದರಿ ಅಂದಾಜು ಮಾತ್ರ.",
          crops: [
            {
              crop_id: 2,
              crop_key: "ragi",
              name_en: "Ragi (Finger Millet)",
              name_kn: "ರಾಗಿ",
              category: "Millet",
              image_asset: "/crops/ragi.svg",
              suitable_soil_types: ["Red", "Loamy"],
              ph_range: "5.0 - 8.0",
              water_requirement_level: "Low",
              water_requirement_mm_range: "350-550 mm",
              suitable_seasons: ["Kharif"],
              growing_duration_days_range: "100-120 days",
              temperature_range_c: "20-34 °C",
              humidity_range_pct: "45-85%",
              rainfall_range_mm: "60-1100 mm",
              seed_rate_kg_per_acre: "4-5 kg/acre",
              economic_data_status: "prototype_demonstration",
              economic_available: true,
              seed_cost_inr_total: 450,
              cultivation_cost_min_total: 9500,
              cultivation_cost_max_total: 14500,
              expected_yield_qtl_min_total: 8,
              expected_yield_qtl_max_total: 13,
              indicative_price_inr_per_qtl: 3800,
              gross_revenue_min_total: 30400,
              gross_revenue_max_total: 49400,
              net_return_min_total: 15900,
              net_return_max_total: 39900,
              assumptions_en: "Baseline assumption for 1 acre dryland Ragi.",
              assumptions_kn: "1 ಎಕರೆ ರಾಗಿ ಮಾದರಿ ಊಹೆ.",
              economic_source: "UAS Bengaluru",
              information_source: "UAS Bengaluru",
            },
          ],
        }),
        { status: 200 }
      )
    );
  }
  if (path.includes("/api/crops")) {
    return Promise.resolve(
      new Response(
        JSON.stringify([
          {
            id: 2,
            crop_key: "ragi",
            name_en: "Ragi (Finger Millet)",
            name_kn: "ರಾಗಿ",
            scientific_name: "Eleusine coracana",
            category: "Millet",
            image_asset: "/crops/ragi.svg",
            growing_duration_days_min: 100,
            growing_duration_days_max: 120,
            water_requirement_level: "Low",
            water_requirement_mm_min: 350,
            water_requirement_mm_max: 550,
            seed_rate_kg_per_acre: "4-5 kg/acre",
            record_status: "verified_reference",
            in_ml_dataset: false,
            suitable_seasons: ["Kharif"],
            suitable_soil_types: ["Red", "Loamy"],
          },
        ]),
        { status: 200 }
      )
    );
  }
  if (path.includes("/api/recommendations") && init?.method === "POST") {
    return Promise.resolve(
      new Response(
        JSON.stringify({
          recommendation_id: 101,
          created_at: new Date().toISOString(),
          mode_used: "hybrid_full",
          confidence_level: "moderate",
          scoring_notice_en: "Illustrative prototype index.",
          scoring_notice_kn: "ಮಾದರಿ ಸೂಚ್ಯಂಕ.",
          disclaimer_en: "Verify with RSK/KVK.",
          disclaimer_kn: "ತಜ್ಞರೊಂದಿಗೆ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.",
          warnings: [],
          insufficient_data_reason: null,
          missing_fields: [],
          location_context: {
            state: "Karnataka",
            district: "Mandya",
            taluk: "Maddur",
            agro_climatic_zone: "Southern Dry Zone",
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
              suitability_category: "Highly Suitable (Prototype Match)",
              illustrative_score: 91.5,
              ml_probability: null,
              dimension_scores: { location: 100, soil: 95, water: 100, seasonal: 100, climatic: 85, nutrient: 80 },
              reasons_en: ["Compatible with Kharif sowing season."],
              reasons_kn: ["ಮುಂಗಾರು ಹಂಗಾಮಿಗೆ ಸೂಕ್ತವಾಗಿದೆ."],
              limitations_en: ["Verify local variety availability."],
              limitations_kn: ["ಸ್ಥಳೀಯ ತಳಿ ಲಭ್ಯತೆ ಪರಿಶೀಲಿಸಿ."],
              conflict_flags: [],
              water_requirement_level: "Low",
              water_requirement_mm_min: 350,
              water_requirement_mm_max: 550,
              suitable_seasons: ["Kharif"],
              growing_duration_days_min: 100,
              growing_duration_days_max: 120,
              cultivation_guidance_en: "Sow with onset of monsoon.",
              cultivation_guidance_kn: "ಮುಂಗಾರು ಆರಂಭದಲ್ಲಿ ಬಿತ್ತನೆ ಮಾಡಿ.",
              information_source: "UAS Bengaluru",
              record_status: "verified_reference",
            },
          ],
        }),
        { status: 201 }
      )
    );
  }
  if (path.includes("/api/knowledge")) {
    return Promise.resolve(
      new Response(
        JSON.stringify([
          {
            id: 1,
            slug: "soil-ph",
            category: "soil",
            title_en: "Understanding Soil pH",
            title_kn: "ಮಣ್ಣಿನ ಪಿಎಚ್ ಮಾಹಿತಿ",
            summary_en: "Summary text",
            summary_kn: "ಸಾರಾಂಶ",
            source_name: "Soil Health Card Portal",
            source_url: "https://soilhealth.dac.gov.in/",
            updated_at: new Date().toISOString(),
          },
        ]),
        { status: 200 }
      )
    );
  }
  return Promise.resolve(new Response(JSON.stringify({}), { status: 200 }));
}

describe("SmartKrishi Frontend Application", () => {
  beforeEach(() => {
    sessionStorage.setItem("smartkrishi_intro_seen", "1");
    localStorage.setItem("smartkrishi_lang", "en");
    window.history.pushState({}, "", "/");
    vi.spyOn(globalThis, "fetch").mockImplementation((input, init) =>
      mockFetchImplementation(typeof input === "string" ? input : input.toString(), init)
    );
  });

  it("renders home page, switches to Kannada, and navigates to Privacy Policy and Terms", async () => {
    const user = userEvent.setup();
    render(<App />);

    expect(
      screen.getByRole("heading", { name: /Crop selection grounded in soil, water/i })
    ).toBeInTheDocument();

    const primaryNav = screen.getByRole("navigation", { name: /Primary navigation/i });

    // Language switch EN -> KN
    await user.click(screen.getByRole("button", { name: "ಕನ್ನಡ" }));
    expect(within(primaryNav).getByRole("link", { name: "ಬೆಳೆ ಶಿಫಾರಸು" })).toBeInTheDocument();

    // Switch back to EN
    await user.click(screen.getByRole("button", { name: "EN" }));

    // Footer Privacy & Terms links
    await user.click(screen.getByRole("link", { name: "Privacy Policy" }));
    expect(screen.getByRole("heading", { name: "Privacy Policy" })).toBeInTheDocument();

    await user.click(screen.getByRole("link", { name: "Terms & Conditions" }));
    expect(screen.getByRole("heading", { name: "Terms & Conditions" })).toBeInTheDocument();
  });

  it("handles cascading district/taluk dropdowns, inline pH validation, and recommendation submission", async () => {
    const user = userEvent.setup();
    render(<App />);

    const primaryNav = screen.getByRole("navigation", { name: /Primary navigation/i });
    await user.click(within(primaryNav).getByRole("link", { name: "Crop Finder" }));
    await waitFor(() => expect(screen.getByLabelText("District")).toHaveValue("Bengaluru Rural"));

    // Select Mandya -> updates taluk to Maddur & Southern Dry Zone
    await user.selectOptions(screen.getByLabelText("District"), "Mandya");
    await waitFor(() => expect(screen.getByLabelText("Taluk")).toHaveValue("Maddur"));
    expect(screen.getByText(/Southern Dry Zone/i)).toBeInTheDocument();

    // Step 2: Soil Profile -> test invalid pH inline validation
    await user.click(screen.getByRole("button", { name: /Continue/i }));
    const phInput = screen.getByLabelText(/Soil pH/i);
    await user.clear(phInput);
    await user.type(phInput, "19");
    await user.click(screen.getByRole("button", { name: /Continue/i }));
    expect(screen.getByText(/Soil pH must be between 0 and 14/i)).toBeInTheDocument();

    // Fix pH -> continue through Farming -> Climate -> Submit
    await user.clear(phInput);
    await user.type(phInput, "6.4");
    await user.click(screen.getByRole("button", { name: /Continue/i }));
    await user.click(screen.getByRole("button", { name: /Continue/i }));
    await user.click(screen.getByRole("button", { name: /Generate Crop Recommendation/i }));

    await waitFor(() =>
      expect(screen.getByRole("heading", { name: /Crop Recommendation Report/i })).toBeInTheDocument()
    );
    expect(screen.getByText(/Ragi \(Finger Millet\)/i)).toBeInTheDocument();
  });

  it("renders Crop Comparison, Soil Health, Knowledge Centre, and Welcome Animation skip", async () => {
    const user = userEvent.setup();
    sessionStorage.removeItem("smartkrishi_intro_seen");
    render(<App />);

    // Skip welcome animation button works
    const skipBtn = screen.getByRole("button", { name: /Skip intro/i });
    await user.click(skipBtn);
    expect(screen.queryByRole("button", { name: /Skip intro/i })).not.toBeInTheDocument();

    const primaryNav = screen.getByRole("navigation", { name: /Primary navigation/i });
    await user.click(within(primaryNav).getByRole("link", { name: "Compare Crops" }));
    await waitFor(() => expect(screen.getByText(/Baseline assumption for 1 acre/i)).toBeInTheDocument());

    await user.click(within(primaryNav).getByRole("link", { name: "Soil Health" }));
    expect(screen.getByRole("heading", { name: /Soil Health Information/i })).toBeInTheDocument();

    await user.click(within(primaryNav).getByRole("link", { name: "Knowledge Centre" }));
    await waitFor(() => expect(screen.getByText("Understanding Soil pH")).toBeInTheDocument());
  });

  it("bypasses welcome animation automatically under prefers-reduced-motion", () => {
    sessionStorage.removeItem("smartkrishi_intro_seen");
    const origMatchMedia = window.matchMedia;
    window.matchMedia = () =>
      ({
        matches: true,
        media: "(prefers-reduced-motion: reduce)",
        onchange: null,
        addListener: () => {},
        removeListener: () => {},
        addEventListener: () => {},
        removeEventListener: () => {},
        dispatchEvent: () => false,
      }) as MediaQueryList;

    render(<App />);
    expect(screen.queryByRole("button", { name: /Skip intro/i })).not.toBeInTheDocument();
    window.matchMedia = origMatchMedia;
  });
});
