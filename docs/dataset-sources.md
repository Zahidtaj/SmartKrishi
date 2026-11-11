# Dataset Sources, Provenance, and ML Evaluation

## Primary Public Dataset

- **Dataset:** Crop Recommendation Dataset (`datasets/raw/crop_recommendation.csv`)
- **Source URL:** `https://raw.githubusercontent.com/Gladiator07/Harvestify/master/Data-processed/crop_recommendation.csv`
- **Origin & License:** Derived from Indian Chamber of Food and Agriculture / public Kaggle Crop Recommendation dataset (Atharva Ingle), distributed under open CC0 / Public Domain educational terms.
- **Size & Balance:** 2,200 rows across 22 crop labels (100 samples per class), 7 numeric input features (`N`, `P`, `K`, `temperature`, `humidity`, `ph`, `rainfall`).
- **Validation Status:** Verified zero missing/NULL cells, zero out-of-range values, and zero exact duplicate rows (`datasets/processed/dataset_validation_report.json`).

## Reproducible Training & Measured Metrics

Run `python -m ml.train` to reproduce:
1. Stratified 80/20 split (`1,760` training / `440` held-out test, `random_state=42`) performed **before** fitting `StandardScaler` and `LabelEncoder` (`ml/preprocessor.py`).
2. `RandomForestClassifier(n_estimators=150, max_depth=14, min_samples_leaf=2, random_state=42)`.
3. Measured metrics recorded in `ml/artifacts/model_metrics.json`:
   - **Held-out Test Accuracy:** `0.9955` (`99.55%`)
   - **Macro Precision:** `0.9957`
   - **Macro Recall:** `0.9955`
   - **Macro F1 Score:** `0.9955`
   - **5-Fold Stratified CV Macro F1:** `0.9920 +/- 0.0067`
   - **Overfitting Gap (`train - test`):** `0.0045`

## Important Dataset Caveat

The benchmark 99.55% test accuracy reflects the structured, tightly clustered nature of this public dataset rather than noisy real-world farm trial accuracy. It also lacks soil texture, irrigation status, sowing season, and Karnataka dryland staples such as Ragi and Jowar. SmartKrishi mitigates these gaps via its agronomic rule engine and transparent warnings.
