# Testing and Validation Report: 15 Agricultural Scenarios
## Comprehensive Test Suite Results for SmartKrishi Engine

### 1. Test Suite Execution Summary
- **Test Framework**: `pytest 9.2.0` on Python 3.13.14 (Windows x64)
- **Execution Date**: 2026-11-16
- **Total Test Cases**: 15
- **Passed**: 15 (100%)
- **Failed**: 0 (0%)
- **Execution Duration**: 0.63 seconds

---

### 2. Scenario-by-Scenario Validation Matrix

| Test Scenario | Input Observations & Conditions | Expected Agricultural Behavior | Actual Engine Result | Status |
|:---|:---|:---|:---|:---:|
| **1. Red soil, sandy texture, limited irrigation** | Tumakuru, Red soil, Sandy texture, Fast drainage, Limited borewell water | Sandy/drought-hardy crops (Groundnut, Ragi, Sesamum, Horse Gram) rank at top; water-guzzling crops filtered | Groundnut & Ragi ranked #1 and #2 (Score >88); Sugarcane filtered | **PASSED** |
| **2. Dark soil, clayey texture, waterlogging** | Raichur, Dark black clay, "Water remains for 1+ days", Low-lying | Waterlog-sensitive pulses (Groundnut, Red Gram, Chickpea) excluded by hard constraints | Groundnut, Red Gram, Chickpea excluded under "Lethal Drainage Constraint"; Wetland Paddy tolerated | **PASSED** |
| **3. Loamy soil, moderate water availability** | Mandya, Reddish brown loam, Moderate drainage, Canal irrigation | Balanced field crops (Ragi, Maize, Sugarcane, Paddy) thrive | Ragi, Maize, Paddy scored >85 with balanced sub-scores | **PASSED** |
| **4. Shallow soil with rocky land** | Chitradurga, Mixed texture, Shallow (<25cm), Rocky terrain | Deep-taproot crops (Sugarcane, Cotton) excluded; shallow-hardy crops (Horse Gram, Ragi) viable | Sugarcane and Cotton excluded by "Root Depth Restriction"; Horse Gram scored high | **PASSED** |
| **5. Flat land with seasonal rainfall** | Dharwad, Medium black loam, Flat land, Normal rain, Kharif | Prime northern transition portfolio (Soybean, Cotton, Maize, Jowar) selected | Soybean and Maize ranked #1 and #2 with high regional scores | **PASSED** |
| **6. Hilly land with high rainfall** | Kodagu, High rainfall (>2700mm), Steep/hilly slope | Slope incompatibility excludes flat basin crops; terrace/valley agronomy enforced | Sugarcane and Paddy on steep slope flagged with "Topography Incompatibility" | **PASSED** |
| **7. Rainfed cultivation with dry spell** | Vijayapura, Deep black soil, Rainfed, 6 consecutive dry days forecasted | Drought-hardy dryland staples (Jowar, Sunflower, Red Gram) score above water-sensitive crops; advisory generated | Rabi Jowar and Sunflower ranked top; dry spell advisory emitted | **PASSED** |
| **8. Limited irrigation during season** | Gadag, Water available only during certain months | Short-duration crops (Green Gram ~70d, Black Gram ~80d, Sunflower ~90d) favored over long-duration | Green Gram and Black Gram ranked top with high duration scores | **PASSED** |
| **9. Unknown soil colour** | Bengaluru Rural, Soil Colour = "Unknown" | Engine applies uncertainty penalty (-5%) without crashing; generates viable recommendations | Completeness 83.3%, Reliability 95.0%; Missing field explicitly logged | **PASSED** |
| **10. Unknown soil texture** | Kolar, Soil Texture = "Unknown", Drainage = "Unknown" | Engine applies major uncertainty deduction (-25%) and guides farmer on ribbon test | Completeness 66.7%, Reliability 75.0%; Missing fields logged | **PASSED** |
| **11. Missing weather information** | Bagalkote, Live weather offline | Graceful fallback to IMD 30-year climatological normals with transparent flag | `is_live_data = False`, IMD baseline loaded, Reliability penalized -5% | **PASSED** |
| **12. Missing location information** | Unrecognized non-Karnataka district name | Graceful unverified fallback with warning, no server crash | Fallback zone applied, `is_verified = False` | **PASSED** |
| **13. Conflicting agricultural inputs** | Vijayapura (500mm rain, Rainfed) with wetland Paddy | Hard constraint catches conflict; Paddy and Sugarcane excluded | Paddy and Sugarcane disqualified under "Critical Water Deficit Constraint" | **PASSED** |
| **14. Unsupported district** | District query "Jaipur" | Correctly returns `None` and triggers proper 404/fallback | District resolution handled correctly | **PASSED** |
| **15. Crop comparison test** | Comparing Ragi, Jowar, and Groundnut | Returns side-by-side attributes, water needs, and verified CACP economics | 3-way matrix populated with non-guaranteed economic benchmarks | **PASSED** |

---

### 3. Conclusion
The test suite confirms that SmartKrishi behaves strictly as an **evidence-based decision support system**: recommendations dynamically adapt to changes in soil texture, water availability, slope, and climate normals, correctly filtering agronomically lethal scenarios.
