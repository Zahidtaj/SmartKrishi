"""Tests for API health, location hierarchy, soil analysis, knowledge, and feedback endpoints."""


def test_health_endpoint(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["database_connected"] is True
    assert data["ml_model_loaded"] is True
    assert data["record_counts"]["crops"] >= 26
    assert data["record_counts"]["locations"] >= 100


def test_location_cascade_states_districts_taluks(client):
    states = client.get("/api/locations/states").json()
    assert "Karnataka" in states["states"]

    districts_resp = client.get("/api/locations/districts", params={"state": "Karnataka"})
    assert districts_resp.status_code == 200
    districts = districts_resp.json()["districts"]
    district_names = {d["district"] for d in districts}
    assert {"Mandya", "Dharwad", "Kodagu", "Dakshina Kannada", "Kalaburagi"}.issubset(district_names)

    taluks_resp = client.get("/api/locations/taluks", params={"state": "Karnataka", "district": "Mandya"})
    assert taluks_resp.status_code == 200
    taluks = taluks_resp.json()["taluks"]
    assert any(t["taluk"] == "Mandya" and t["zone_code"] == "KA-Z6" for t in taluks)


def test_unsupported_district_returns_404(client):
    resp = client.get("/api/locations/taluks", params={"state": "Karnataka", "district": "UnknownDistrict"})
    assert resp.status_code == 404
    assert resp.json()["code"] == "HTTP_404"


def test_soil_analysis_and_fertilizer_caution(client):
    resp = client.post(
        "/api/soil/analyze",
        json={
            "soil_type": "Laterite",
            "ph": 5.1,
            "nitrogen": 45,
            "phosphorus": 18,
            "potassium": 25,
            "measurement_source": "soil_test",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["soil_type"] == "Laterite"
    assert any(i["status"] == "Strongly Acidic" for i in data["interpretations"])
    assert "Soil Health Card" in data["fertilizer_caution_en"]


def test_knowledge_and_feedback_endpoints(client):
    articles = client.get("/api/knowledge").json()
    assert len(articles) >= 7
    detail = client.get(f"/api/knowledge/{articles[0]['id']}")
    assert detail.status_code == 200
    assert detail.json()["source_name"]

    fb = client.post(
        "/api/feedback",
        json={
            "category": "usability",
            "rating": 4,
            "district": "Mandya",
            "comment": "Kannada labels on the soil step are clear and helpful.",
        },
    )
    assert fb.status_code == 201
    assert fb.json()["review_status"] == "pending"
