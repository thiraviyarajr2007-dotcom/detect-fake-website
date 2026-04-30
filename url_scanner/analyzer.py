from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

from .engines import (
    ContentSimilarityEngine,
    DomainIntelligenceEngine,
    FusionEngine,
    VisualSimilarityEngine,
)
from .models import ScanRequestContext, ScanResult, Verdict


class AnalysisError(RuntimeError):
    pass


class AnalysisTimeoutError(AnalysisError):
    pass


class Analyzer:
    def __init__(
        self,
        timeout_seconds: float = 10.0,
        domain_engine: DomainIntelligenceEngine | None = None,
        content_engine: ContentSimilarityEngine | None = None,
        visual_engine: VisualSimilarityEngine | None = None,
        fusion_engine: FusionEngine | None = None,
    ) -> None:
        self.timeout_seconds = timeout_seconds
        self.domain_engine = domain_engine or DomainIntelligenceEngine()
        self.content_engine = content_engine or ContentSimilarityEngine()
        self.visual_engine = visual_engine or VisualSimilarityEngine()
        self.fusion_engine = fusion_engine or FusionEngine()

    def analyze(self, url: str, context: ScanRequestContext | None = None) -> ScanResult:
        request_context = context or ScanRequestContext()
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self._analyze_url, url, request_context)
            try:
                return future.result(timeout=self.timeout_seconds)
            except FutureTimeoutError as exc:
                future.cancel()
                raise AnalysisTimeoutError("URL analysis timed out") from exc
            except AnalysisError:
                raise
            except Exception as exc:  # pragma: no cover - defensive wrapping
                raise AnalysisError("URL analysis failed") from exc

    def _analyze_url(self, url: str, context: ScanRequestContext) -> ScanResult:
        domain_result = self.domain_engine.analyze(url, context.domain)
        content_result = self.content_engine.analyze(url, context.content)
        visual_result = self.visual_engine.analyze(context.visual)
        probability, explanations = self.fusion_engine.combine(url, domain_result, content_result, visual_result)

        if probability >= 70:
            verdict = Verdict.PHISHING
        elif probability >= 30:
            verdict = Verdict.SUSPICIOUS
        else:
            verdict = Verdict.SAFE

        indicators = list(dict.fromkeys(explanations))
        return ScanResult(
            url=url,
            verdict=verdict,
            threat_indicators=indicators,
            phishing_probability=probability,
            domain_score=domain_result.score,
            content_score=content_result.score,
            image_score=visual_result.score,
            explanations=explanations,
            brand_target=context.content.claimed_brand,
            reference_url=context.content.genuine_url,
            domain_age_days=context.domain.domain_age_days,
            registrar=context.domain.registrar,
            dns_record_count=context.domain.dns_record_count,
            has_ssl=context.domain.has_ssl,
            domain_location="Unknown",
        )
