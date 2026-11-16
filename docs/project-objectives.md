# SmartKrishi: Project Objectives and Problem Statement
## VTU Community Project Technical Report

### 1. Project Background and Context
In Karnataka and across semi-arid India, small and marginal farmers represent over 80% of total agricultural operational holdings. While precision agriculture and decision support tools have advanced rapidly, most modern recommendation engines suffer from a severe foundational flaw: **they presuppose the availability of laboratory soil chemical analysis** (specifically nitrogen, phosphorus, potassium [NPK] in kg/ha and exact soil pH).

In reality:
1. Soil testing laboratories are distant, under-resourced, or take weeks to return results.
2. Less than 15% of dryland farmers possess an active, accurate Soil Health Card.
3. Existing machine-learning crop recommendation demonstrations frequently ask farmers for arbitrary NPK numbers, resulting in farmers inputting guesswork numbers that produce inaccurate recommendations.
4. Conventional models ignore critical land constraints: water stagnation, root asphyxiation, shallow rocky pans, slope erosion, and micro-climatic dry spells.

### 2. Core Problem Statement
How can smallholder farmers make scientifically grounded, crop-selection and planting decisions **without laboratory soil tests**, utilizing only observable physical land characteristics, regional agro-climatic boundaries, reliable meteorological patterns, and verified agronomic package of practices?

---

### 3. Primary Objectives
The SmartKrishi system addresses the following key questions formulated by the Department of Agriculture and VTU Community Project guidelines:

1. **Regional Geographic Suitability**: Which crops are agronomically adapted to the farmer's specific agro-climatic zone and district?
2. **Observable Soil Compatibility**: What crops can thrive in the farmer's observed soil texture (ribbon feel), drainage speed, moisture retention, and depth without chemical lab assays?
3. **Seasonal Window Optimization**: Which crops align with the planned growing season (Kharif, Rabi, Summer/Zaid) and specific sowing months?
4. **Rainfall and Climate Compatibility**: Which crops match the 30-year IMD historical rainfall normal and forecasted precipitation?
5. **Water Budgeting and Risk Mitigation**: Which crops can produce viable economic yields given the farmer's actual irrigation resource (rainfed, borewell, canal, farm pond)?
6. **Land Topography Limitations**: How do slopes, low-lying water accumulation risks, and shallow rocky pans filter out unsuitable crops?
7. **Water-Saving Crop Identification**: Which drought-hardy millets or pulses (e.g. Ragi, Horse Gram, Jowar) can mitigate risk during dry spells?
8. **Agricultural Risk Warning**: What critical insect pests, fungal blights, and terminal droughts must the farmer anticipate for each crop?
9. **Estimated Cultivation Benchmarks**: What are the documented input costs, labor requirements, yield ranges, and official Minimum Support Prices (MSP)?
10. **Pre-Cultivation Actionable Guidance**: What crucial cultural practices (seed treatment, spacing, intercropping) are recommended by state agricultural universities?

---

### 4. Target Geography and Modular Architecture
- **Phase 1 Target**: Karnataka, India (31 Districts, 10 Official Agro-Climatic Zones).
- **Extensibility**: The system architecture isolates geographical parameters, soil matrices, and crop requirements into configurable database schemas and JSON rule sets, enabling seamless extension to neighboring states (e.g. Maharashtra, Tamil Nadu, Andhra Pradesh).

---

### 5. Architectural Principles and Anti-Fabrication Guarantee
- **No Hallucinated Data**: No random numbers or generic generative text. Every score and explanation stems from traceable agricultural equations and verified datasets.
- **Hard Constraints Enforcement**: A high score in rainfall cannot override a lethal condition like waterlogging for root-sensitive pulses (Pigeonpea, Groundnut, Chickpea).
- **Uncertainty Transparency**: When farmer observations or live weather data are incomplete, the system penalizes the reliability index and explicitly reports missing parameters.
