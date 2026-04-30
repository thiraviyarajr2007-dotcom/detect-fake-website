from datetime import datetime, timedelta, timezone

from url_scanner.models import ScanResult, Verdict
from url_scanner.storage import ScanStore


def test_save_and_retrieve_round_trip(tmp_path) -> None:
    store = ScanStore(tmp_path / "scanner.db")
    result = ScanResult(
        url="https://example.com",
        verdict=Verdict.SAFE,
        threat_indicators=[],
        phishing_probability=12,
        domain_score=12,
        explanations=["Minimal risk"],
    )
    store.save(result)

    fetched = store.get_by_id(result.scan_id)

    assert fetched is not None
    assert fetched.scan_id == result.scan_id
    assert fetched.url == result.url
    assert fetched.verdict is Verdict.SAFE
    assert fetched.phishing_probability == 12
    assert fetched.explanations == ["Minimal risk"]


def test_history_returns_reverse_chronological_order(tmp_path) -> None:
    store = ScanStore(tmp_path / "scanner.db")
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

    history = store.get_history()

    assert [item.scan_id for item in history] == [newer.scan_id, older.scan_id]


def test_get_by_url_respects_time_window(tmp_path) -> None:
    store = ScanStore(tmp_path / "scanner.db")
    stale = ScanResult(
        url="https://example.com",
        verdict=Verdict.SAFE,
        timestamp=datetime.now(timezone.utc) - timedelta(hours=25),
    )
    store.save(stale)

    assert store.get_by_url("https://example.com", within_hours=24) is None


def test_records_older_than_30_days_are_pruned(tmp_path) -> None:
    store = ScanStore(tmp_path / "scanner.db")
    old_result = ScanResult(
        url="https://old.example.com",
        verdict=Verdict.SAFE,
        timestamp=datetime.now(timezone.utc) - timedelta(days=31),
    )
    fresh_result = ScanResult(
        url="https://fresh.example.com",
        verdict=Verdict.SAFE,
        timestamp=datetime.now(timezone.utc),
    )
    store.save(old_result)
    store.save(fresh_result)

    history = store.get_history()

    assert [item.url for item in history] == ["https://fresh.example.com"]
