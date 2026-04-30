from __future__ import annotations

from dataclasses import replace

from .analyzer import Analyzer
from .models import ScanRequestContext, ScanResult
from .storage import ScanStore


class CacheService:
    def __init__(self, analyzer: Analyzer, store: ScanStore, cache_hours: int = 24) -> None:
        self.analyzer = analyzer
        self.store = store
        self.cache_hours = cache_hours

    def scan(
        self,
        url: str,
        force_refresh: bool = False,
        context: ScanRequestContext | None = None,
    ) -> ScanResult:
        if not force_refresh:
            cached = self.store.get_by_url(url, within_hours=self.cache_hours)
            if cached:
                return replace(cached, is_cached=True)

        result = self.analyzer.analyze(url, context=context)
        self.store.save(result)
        return result
