"""Tests for hybrid crop recommendation engine, hard constraints, validation, and failure modes."""

from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from backend.database import get_db
from backend.main import create_app
from ml.predictor import CropMLPredictor


def _base_payload() -> dict:
    return {
        "state": "Karnataka",
        "district": "Bengaluru Rural",
        "taluk": "Devanahalli",
        "soil_type": "Red",
        "soil_data_available": True,
        "soil_measurement_source": "soil_test",
        "ph": 6.4,
        "nitrogen": 55,
        "phosphorus": 38,
        "potassium": 32,
        "season": "Kharif",
        "irrigation_type": "Rainfed",
        "water_availability": "Rainfed",
        "land_area_acres": 2.5,
        "farming_method": "Integrated (INM/IPM)",
        "temperature": 26.5,
        "humidity": 68.0,
        "rainfall": 750.0,
        "climate_source": "estimate",
        "language": "en",
    }


def test_valid_hybrid_recommendation_persists_and_retrieves(client):
    payload = _base_payload()
    resp = client.post("/api/recommendations", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["mode_used"] == "hybrid_full"
    assert 1 <= len(data["recommendations"]) <= 3
    keys = {c["crop_key"] for c in data["recommendations"]}
    assert "apple" not in keys
    assert "jute" not in keys
    assert "rice" not in keys  # Rainfed Eastern Dry Zone must not suggest high-water paddy

    rec_id = data["recommendation_id"]
    fetched = client.get(f"/api/recommendations/{rec_id}")
    assert fetched.status_code == 200
    assert fetched.json()["recommendation_id"] == rec_id


def test_rabi_black_soil_dharwad_recommends_appropriate_rabi_crops(client):
    payload = _base_payload()
    payload.update(
        {
            "district": "Dharwad",
            "taluk": "Kundgol",
            "soil_type": "Black",
            "season": "Rabi",
            "water_availability": "Limited irrigation",
            "nitrogen": 40,
            "phosphorus": 65,
            "potassium": 78,
            "temperature": 21.0,
            "humidity": 32.0,
            "rainfall": 80.0,
        }
    )
    resp = client.post("/api/recommendations", json=payload)
    assert resp.status_code == 201
    keys = {c["crop_key"] for c in resp.json()["recommendations"]}
    assert keys & {"chickpea", "jowar"}


def test_missing_npk_triggers_reduced_information_mode(client):
    payload = _base_payload()
    payload.update(
        {
            "soil_data_available": False,
            "soil_measurement_source": "unavailable",
            "ph": None,
            "nitrogen": None,
            "phosphorus": None,
            "potassium": None,
        }
    )
    resp = client.post("/api/recommendations", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["mode_used"] == "reduced_information"
    assert data["confidence_level"] == "reduced"
    assert set(["ph", "nitrogen", "phosphorus", "potassium"]).issubset(set(data["missing_fields"]))
    assert len(data["warnings"]) >= 1


def test_invalid_ph_and_invalid_numbers_return_422(client):
    payload = _base_payload()
    payload["ph"] = 18.5
    resp = client.post("/api/recommendations", json=payload)
    assert resp.status_code == 422
    assert resp.json()["code"] == "VALIDATION_ERROR"

    payload2 = _base_payload()
    payload2["nitrogen"] = -15
    resp2 = client.post("/api/recommendations", json=payload2)
    assert resp2.status_code == 422


def test_extreme_non_arable_ph_returns_insufficient_data_without_forcing_crop(client):
    payload = _base_payload()
    payload["ph"] = 2.0
    resp = client.post("/api/recommendations", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["mode_used"] == "insufficient_data"
    assert data["confidence_level"] == "insufficient"
    assert data["recommendations"] == []
    assert data["insufficient_data_reason"] is not None


def test_empty_request_returns_422(client):
    resp = client.post("/api/recommendations", json={})
    assert resp.status_code == 422


def test_unsupported_location_returns_422(client):
    payload = _base_payload()
    payload["state"] = "NonExistentState"
    resp = client.post("/api/recommendations", json=payload)
    assert resp.status_code == 422


def test_model_loading_failure_returns_safe_503(db_session, tmp_path: Path):
    app = create_app()

    def _override_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_db
    with TestClient(app, raise_server_exceptions=False) as tc:
        app.state.predictor = CropMLPredictor(artifacts_dir=tmp_path / "missing_artifacts")
        resp = tc.post("/api/recommendations", json=_base_payload())
        assert resp.status_code == 503
        assert "Recommendation ML engine unavailable" in resp.json()["detail"]


def test_database_failure_returns_safe_500_without_stack_trace(predictor):
    app = create_app()
    app.state.predictor = predictor

    class FailingSession:
        def query(self, *_args, **_kwargs):
            raise SQLAlchemyError("Simulated connection failure")

    def _failing_db():
        yield FailingSession()

    app.dependency_overrides[get_db] = _failing_db
    with TestClient(app, raise_server_exceptions=False) as tc:
        resp = tc.post("/api/recommendations", json=_base_payload())
        assert resp.status_code == 500
        body = resp.json()
        assert body["code"] == "DATABASE_ERROR"
        assert "Simulated connection failure" not in body["detail"]
