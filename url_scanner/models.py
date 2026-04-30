from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import uuid4


class Verdict(StrEnum):
    SAFE = "Safe"
    SUSPICIOUS = "Suspicious"
    PHISHING = "Phishing"


@dataclass(slots=True)
class DomainContext:
    domain_age_days: int | None = None
    registrar: str | None = None
    dns_record_count: int | None = None
    has_ssl: bool | None = None
    source: str | None = None


@dataclass(slots=True)
class ContentContext:
    claimed_brand: str | None = None
    genuine_url: str | None = None
    html_snippet: str | None = None
    genuine_html_snippet: str | None = None
    text_snippet: str | None = None
    dom_similarity: float | None = None
    tag_similarity: float | None = None
    keyword_similarity: float | None = None
    login_form_detected: bool | None = None


@dataclass(slots=True)
class VisualContext:
    screenshot_similarity: float | None = None
    logo_similarity: float | None = None
    layout_similarity: float | None = None
    theme_similarity: float | None = None
    suspect_screenshot_hash: str | None = None
    genuine_screenshot_hash: str | None = None


@dataclass(slots=True)
class ScanRequestContext:
    domain: DomainContext = field(default_factory=DomainContext)
    content: ContentContext = field(default_factory=ContentContext)
    visual: VisualContext = field(default_factory=VisualContext)


@dataclass(slots=True)
class EngineBreakdown:
    score: int
    reasons: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ScanResult:
    url: str
    verdict: Verdict
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    threat_indicators: list[str] = field(default_factory=list)
    is_cached: bool = False
    phishing_probability: int = 0
    domain_score: int = 0
    content_score: int = 0
    image_score: int = 0
    explanations: list[str] = field(default_factory=list)
    brand_target: str | None = None
    reference_url: str | None = None
    domain_age_days: int | None = None
    registrar: str | None = None
    dns_record_count: int | None = None
    has_ssl: bool | None = None
    domain_location: str | None = None
    scan_id: str = field(default_factory=lambda: str(uuid4()))

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["timestamp"] = self.timestamp.isoformat()
        payload["verdict"] = self.verdict.value
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ScanResult":
        return cls(
            scan_id=payload["scan_id"],
            url=payload["url"],
            verdict=Verdict(payload["verdict"]),
            timestamp=datetime.fromisoformat(payload["timestamp"]),
            threat_indicators=list(payload.get("threat_indicators", [])),
            is_cached=bool(payload.get("is_cached", False)),
            phishing_probability=int(payload.get("phishing_probability", 0)),
            domain_score=int(payload.get("domain_score", 0)),
            content_score=int(payload.get("content_score", 0)),
            image_score=int(payload.get("image_score", 0)),
            explanations=list(payload.get("explanations", [])),
            brand_target=payload.get("brand_target"),
            reference_url=payload.get("reference_url"),
            domain_age_days=payload.get("domain_age_days"),
            registrar=payload.get("registrar"),
            dns_record_count=payload.get("dns_record_count"),
            has_ssl=payload.get("has_ssl"),
            domain_location=payload.get("domain_location"),
        )
