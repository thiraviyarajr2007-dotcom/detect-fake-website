from datetime import datetime, timedelta, timezone

from url_scanner.cache import CacheService
from url_scanner.models import ScanRequestContext, ScanResult, Verdict


class StubAnalyzer:
    def __init__(self, result: ScanResult) -> None:
        self.result = result
        self.calls: list[tuple[str, ScanRequestContext | None]] = []

    def analyze(self, url: str, context: ScanRequestContext | None = None) -> ScanResult:
        self.calls.append((url, context))
        return self.result


class StubStore:
    def __init__(self, cached_result: ScanResult | None = None) -> None:
        self.cached_result = cached_result
        self.saved_results: list[ScanResult] = []

    def get_by_url(self, url: str, within_hours: int) -> ScanResult | None:
        return self.cached_result

    def save(self, result: ScanResult) -> None:
        self.saved_results.append(result)


def test_cached_result_is_returned_without_calling_analyzer() -> None:
    cached = ScanResult(
        url="https://example.com",
        verdict=Verdict.SAFE,
        timestamp=datetime.now(timezone.utc) - timedelta(hours=1),
    )
    analyzer = StubAnalyzer(
        ScanResult(url="https://example.com", verdict=Verdict.PHISHING)
    )
    service = CacheService(analyzer=analyzer, store=StubStore(cached))

    result = service.scan("https://example.com")

    assert result.is_cached is True
    assert result.timestamp == cached.timestamp
    assert analyzer.calls == []


def test_analyzer_is_called_when_cache_is_expired() -> None:
    fresh = ScanResult(url="https://example.com", verdict=Verdict.SUSPICIOUS)
    analyzer = StubAnalyzer(fresh)
    store = StubStore(cached_result=None)
    service = CacheService(analyzer=analyzer, store=store)

    result = service.scan("https://example.com")

    assert result is fresh
    assert analyzer.calls == [("https://example.com", None)]
    assert store.saved_results == [fresh]


def test_force_refresh_bypasses_cache() -> None:
    cached = ScanResult(url="https://example.com", verdict=Verdict.SAFE)
    fresh = ScanResult(url="https://example.com", verdict=Verdict.PHISHING)
    analyzer = StubAnalyzer(fresh)
    service = CacheService(analyzer=analyzer, store=StubStore(cached))

    result = service.scan("https://example.com", force_refresh=True)

    assert result is fresh
    assert analyzer.calls == [("https://example.com", None)]
