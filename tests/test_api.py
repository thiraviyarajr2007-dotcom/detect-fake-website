from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from url_scanner.api import create_app
from url_scanner.models import ScanResult, Verdict
from url_scanner.storage import ScanStore


def test_post_scan_with_valid_url_returns_verdict(tmp_path) -> None:
    client = TestClient(create_app(tmp_path / "scanner.db"))

    response = client.post("/scan", json={"url": "https://example.com"})

    assert response.status_code == 200
    body = response.json()
    assert body["url"] == "https://example.com"
    assert body["verdict"] == "Safe"
    assert body["is_cached"] is False
    assert body["phishing_probability"] == 0
    assert body["domain_location"] == "Unknown"


def test_post_scan_with_malformed_url_returns_422(tmp_path) -> None:
    client = TestClient(create_app(tmp_path / "scanner.db"))

    response = client.post("/scan", json={"url": "notaurl"})

    assert response.status_code == 422
    assert "valid http or https URL" in response.json()["detail"]


def test_post_scan_returns_cached_result(tmp_path) -> None:
    db_path = tmp_path / "scanner.db"
    store = ScanStore(db_path)
    store.save(
        ScanResult(
            url="https://example.com",
            verdict=Verdict.SAFE,
            timestamp=datetime.now(timezone.utc) - timedelta(hours=1),
            phishing_probability=0,
        )
    )
    client = TestClient(create_app(db_path))

    response = client.post("/scan", json={"url": "https://example.com"})

    assert response.status_code == 200
    assert response.json()["is_cached"] is True


def test_post_scan_force_refresh_bypasses_cache(tmp_path) -> None:
    db_path = tmp_path / "scanner.db"
    store = ScanStore(db_path)
    cached = ScanResult(url="https://secure-login-example.com", verdict=Verdict.SAFE)
    store.save(cached)
    client = TestClient(create_app(db_path))

    response = client.post(
        "/scan",
        json={
            "url": "https://paytm-secure-login.com",
            "force_refresh": True,
            "domain": {"domain_age_days": 2, "has_ssl": False},
            "content": {
                "claimed_brand": "Paytm",
                "genuine_url": "https://paytm.com",
                "text_snippet": "login verify password",
                "dom_similarity": 90,
                "login_form_detected": True
            },
            "visual": {
                "screenshot_similarity": 94,
                "logo_similarity": 95,
                "theme_similarity": 90
            }
        },
    )

    assert response.status_code == 200
    assert response.json()["verdict"] == "Phishing"
    assert response.json()["is_cached"] is False
    assert response.json()["phishing_probability"] >= 90


def test_get_history_returns_reverse_chronological_order(tmp_path) -> None:
    db_path = tmp_path / "scanner.db"
    store = ScanStore(db_path)
    older = ScanResult(
        url="https://example.com/1",
        verdict=Verdict.SAFE,
        timestamp=datetime.now(timezone.utc) - timedelta(hours=2),
    )
    newer = ScanResult(
        url="https://example.com/2",
        verdict=Verdict.SUSPICIOUS,
        timestamp=datetime.now(timezone.utc) - timedelta(hours=1),
    )
    store.save(older)
    store.save(newer)
    client = TestClient(create_app(db_path))

    response = client.get("/history")

    assert response.status_code == 200
    body = response.json()
    assert [item["scan_id"] for item in body] == [newer.scan_id, older.scan_id]


def test_get_history_item_returns_correct_scan_details(tmp_path) -> None:
    db_path = tmp_path / "scanner.db"
    store = ScanStore(db_path)
    result = ScanResult(url="https://example.com", verdict=Verdict.SAFE)
    store.save(result)
    client = TestClient(create_app(db_path))

    response = client.get(f"/history/{result.scan_id}")

    assert response.status_code == 200
    assert response.json()["scan_id"] == result.scan_id


def test_get_history_item_returns_404_for_missing_scan(tmp_path) -> None:
    client = TestClient(create_app(tmp_path / "scanner.db"))

    response = client.get("/history/missing")

    assert response.status_code == 404


def test_dashboard_route_renders_html(tmp_path) -> None:
    client = TestClient(create_app(tmp_path / "scanner.db"))
    client.post("/auth/register", json={"username": "testuser", "email": "test@example.com", "password": "password123"})
    client.post("/auth/login", json={"username": "testuser", "password": "password123"})

    response = client.get("/")

    assert response.status_code == 200
    assert "PhishGuard AI" in response.text
    assert "Enter Website URL here" in response.text
    assert "Recent Scans" in response.text
    assert "Download Latest Report" in response.text
    assert "Domain Information" in response.text
    assert "Dashboard" in response.text
    assert "Settings" in response.text
    assert "Scanning with AI" in response.text
    assert "Confidence Meter" in response.text
    assert "Home" in response.text


def test_export_history_returns_csv(tmp_path) -> None:
    db_path = tmp_path / "scanner.db"
    store = ScanStore(db_path)
    store.save(ScanResult(url="https://example.com", verdict=Verdict.SAFE, phishing_probability=0))
    client = TestClient(create_app(db_path))

    response = client.get("/history/export.csv")

    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "https://example.com" in response.text


def test_monitor_preview_returns_batch_results(tmp_path) -> None:
    client = TestClient(create_app(tmp_path / "scanner.db"))

    response = client.post(
        "/monitor/preview",
        json={
            "domains": ["paytm-secure-login.com", "example.com"],
            "context": {
                "content": {"text_snippet": "login verify password secure"},
                "visual": {"logo_similarity": 91, "theme_similarity": 84}
            }
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 2
    assert body["items"][0]["normalized_url"] == "https://paytm-secure-login.com"
    assert body["items"][0]["result"]["phishing_probability"] >= 70


def test_architecture_endpoint_returns_weights_and_features(tmp_path) -> None:
    client = TestClient(create_app(tmp_path / "scanner.db"))

    response = client.get("/architecture")

    assert response.status_code == 200
    body = response.json()
    assert body["weights"] == {"domain": 0.4, "content": 0.3, "image": 0.3}
    assert "Explainable AI evidence for every verdict" in body["key_features"]


def test_analytics_endpoint_returns_totals_and_top_brands(tmp_path) -> None:
    db_path = tmp_path / "scanner.db"
    store = ScanStore(db_path)
    store.save(ScanResult(url="https://a.com", verdict=Verdict.PHISHING, brand_target="SBI"))
    store.save(ScanResult(url="https://b.com", verdict=Verdict.SAFE, brand_target="Amazon"))
    store.save(ScanResult(url="https://c.com", verdict=Verdict.PHISHING, brand_target="SBI"))
    client = TestClient(create_app(db_path))

    response = client.get("/analytics")

    assert response.status_code == 200
    body = response.json()
    assert body["total_scanned"] == 3
    assert body["phishing_found"] == 2
    assert body["safe_found"] == 1
    assert body["top_targeted_brands"][0] == "SBI"


def test_history_report_returns_plain_text_summary(tmp_path) -> None:
    db_path = tmp_path / "scanner.db"
    store = ScanStore(db_path)
    result = ScanResult(
        url="https://example.com",
        verdict=Verdict.SUSPICIOUS,
        phishing_probability=42,
        domain_score=50,
        content_score=35,
        image_score=30,
        explanations=["Domain registered recently."],
    )
    store.save(result)
    client = TestClient(create_app(db_path))

    response = client.get(f"/history/{result.scan_id}/report.txt")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "Phishing Detection Report" in response.text
    assert "Domain registered recently." in response.text
