from url_scanner.intelligence import ContextEnricher, DomainIntelligenceService, DomainMetadata, WhoisProvider
from url_scanner.models import DomainContext, ScanRequestContext


class StubWhoisProvider(WhoisProvider):
    def lookup(self, hostname: str) -> DomainMetadata:
        return DomainMetadata(
            domain_age_days=2,
            registrar="Demo Registrar",
            dns_record_count=1,
            has_ssl=False,
            source="stub-whois",
        )


def test_context_enricher_infers_brand_and_recent_domain_risk() -> None:
    enriched = ContextEnricher().enrich("https://paytm-secure-login.com", ScanRequestContext())

    assert enriched.domain.domain_age_days == 3
    assert enriched.domain.registrar == "Privacy Registrar"
    assert enriched.domain.dns_record_count == 0
    assert enriched.domain.source == "heuristic"
    assert enriched.content.claimed_brand == "Paytm"
    assert enriched.content.genuine_url == "https://paytm.com"
    assert enriched.content.login_form_detected is True


def test_domain_intelligence_service_uses_provider_metadata() -> None:
    service = DomainIntelligenceService(provider=StubWhoisProvider())

    context = service.extract("example-phish.com", DomainContext())

    assert context.domain_age_days == 2
    assert context.registrar == "Demo Registrar"
    assert context.dns_record_count == 1
    assert context.has_ssl is False
    assert context.source == "stub-whois"
