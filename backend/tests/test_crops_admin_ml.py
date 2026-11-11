"""Tests for crop catalog, comparison, admin auth, and ML pipeline."""

from pathlib import Path
from ml.data_loader import load_crop_dataset
from ml.data_validator import validate_crop_dataset
from ml.preprocessor import split_and_preprocess
from ml.predictor import CropMLPredictor


def test_crops_list_detail_and_comparison(client):
    crops = client.get("/api/crops").json()
    assert len(crops) >= 26

    first_id = crops[0]["id"]
    detail = client.get(f"/api/crops/{first_id}")
    assert detail.status_code == 200
    assert "requirement" in detail.json()

    not_found = client.get("/api/crops/999999")
    assert not_found.status_code == 404

    compare_ids = [c["id"] for c in crops[:3]]
    comp = client.post("/api/crops/compare", json={"crop_ids": compare_ids, "land_area_acres": 2.0})
    assert comp.status_code == 200
    comp_data = comp.json()
    assert comp_data["land_area_acres"] == 2.0
    assert len(comp_data["crops"]) == 3

    bad_comp = client.post("/api/crops/compare", json={"crop_ids": [999999], "land_area_acres": 1.0})
    assert bad_comp.status_code == 404


def test_admin_auth_protection_and_login(client):
    unauth = client.get("/api/admin/overview")
    assert unauth.status_code == 401

    bad_login = client.post("/api/admin/login", json={"username": "admin", "password": "wrong-password"})
    assert bad_login.status_code == 401

    good_login = client.post(
        "/api/admin/login",
        json={"username": "admin", "password": "smartkrishi-local-admin-2026"},
    )
    assert good_login.status_code == 200
    token = good_login.json()["access_token"]

    overview = client.get("/api/admin/overview", headers={"Authorization": f"Bearer {token}"})
    assert overview.status_code == 200
    assert overview.json()["admin_username"] == "admin"
    assert overview.json()["ml_metrics"]["test_accuracy"] > 0.9


def test_ml_pipeline_load_validate_split_and_predict():
    df = load_crop_dataset()
    clean_df, report = validate_crop_dataset(df, save_report_path=None)
    assert report.passed is True
    assert report.valid_rows == 2200

    splits = split_and_preprocess(clean_df)
    assert len(splits.X_train_raw) == 1760
    assert len(splits.X_test_raw) == 440

    predictor = CropMLPredictor()
    predictor.load()
    preds = predictor.predict_probabilities(
        nitrogen=90, phosphorus=42, potassium=43, temperature=21, humidity=82, ph=6.5, rainfall=205
    )
    assert preds[0].crop_key == "rice"
