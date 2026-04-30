from __future__ import annotations

from dataclasses import dataclass

from .analyzer import Analyzer
from .intelligence import ContextEnricher
from .models import ScanRequestContext, ScanResult
from .validation import validate_url


@dataclass(slots=True)
class MonitoredDomain:
    raw_value: str
    normalized_url: str
    result: ScanResult


class DomainFeedMonitor:
    def __init__(self, analyzer: Analyzer, enricher: ContextEnricher | None = None) -> None:
        self.analyzer = analyzer
        self.enricher = enricher or ContextEnricher()

    def scan_domains(self, domains: list[str], base_context: ScanRequestContext | None = None) -> list[MonitoredDomain]:
        results: list[MonitoredDomain] = []
        for value in domains:
            normalized = self._normalize_domain(value)
            context = self.enricher.enrich(normalized, base_context)
            result = self.analyzer.analyze(normalized, context=context)
            results.append(MonitoredDomain(raw_value=value, normalized_url=normalized, result=result))
        return results

    def _normalize_domain(self, value: str) -> str:
        trimmed = value.strip()
        normalized = validate_url(trimmed)
        if normalized:
            return normalized
        candidate = validate_url(f"https://{trimmed}")
        if candidate is None:
            raise ValueError(f"Invalid domain in feed: {value}")
        return candidate
