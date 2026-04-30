from __future__ import annotations

from dataclasses import dataclass, replace
from urllib.parse import urlparse

from .models import ContentContext, DomainContext, ScanRequestContext

BRAND_HINTS = {
    "paytm": "Paytm",
    "amazon": "Amazon",
    "sbi": "SBI",
    "google": "Google",
    "microsoft": "Microsoft",
    "bank": "Bank",
}

REGISTRAR_HINTS = {
    "paytm": "Privacy Registrar",
    "secure": "NameCheap Privacy",
    "verify": "LowCost Domains",
    "amazon": "Cloud Registrar",
}

TRUSTED_REFERENCE_DOMAINS = {
    "paytm.com",
    "phonepe.com",
    "google.com",
    "google.co.in",
    "amazon.in",
    "amazon.com",
    "sbi.co.in",
    "microsoft.com",
    "youtube.com",
    "facebook.com",
    "instagram.com",
    "chatgpt.com",
    "reddit.com",
    "wikipedia.org",
    "twitter.com",
    "whatsapp.com",
    "yahoo.com",
    "tiktok.com",
    "duckduckgo.com",
    "bing.com",
    "linkedin.com",
    "apple.com",
    "netflix.com",
    "pinterest.com",
    "flipkart.com",
    "onlinesbi.sbi",
    "icicibank.com",
    "hdfcbank.com",
    "axisbank.com",
    "irctc.co.in",
    "uidai.gov.in",
    "incometax.gov.in",
    "india.gov.in",
    "ebay.com",
    "walmart.com",
    "target.com",
    "bestbuy.com",
    "alibaba.com",
    "aliexpress.com",
    "etsy.com",
    "myntra.com",
    "ajio.com",
    "coursera.org",
    "udemy.com",
    "hotstar.com",
    "sonyliv.com",
    "zee5.com",
    "spotify.com",
    "primevideo.com",
    "khanacademy.org",
    "edx.org",
    "stackoverflow.com",
    "github.com",
    "geeksforgeeks.org",
}


def _is_same_or_subdomain(hostname: str, trusted_domain: str) -> bool:
    return hostname == trusted_domain or hostname.endswith(f".{trusted_domain}")


def _is_trusted_hostname(hostname: str) -> bool:
    return any(_is_same_or_subdomain(hostname, domain) for domain in TRUSTED_REFERENCE_DOMAINS)


@dataclass(slots=True)
class DomainMetadata:
    domain_age_days: int | None = None
    registrar: str | None = None
    dns_record_count: int | None = None
    has_ssl: bool | None = None
    source: str = "heuristic"


class WhoisProvider:
    def lookup(self, hostname: str) -> DomainMetadata:
        raise NotImplementedError


class HeuristicWhoisProvider(WhoisProvider):
    def lookup(self, hostname: str) -> DomainMetadata:
        return DomainMetadata(
            domain_age_days=self._resolve_domain_age(hostname),
            registrar=self._resolve_registrar(hostname),
            dns_record_count=self._resolve_dns_records(hostname),
            has_ssl=self._resolve_ssl(hostname),
            source="heuristic",
        )

    def _resolve_domain_age(self, hostname: str) -> int | None:
        if _is_trusted_hostname(hostname):
            return 3650
        if any(token in hostname for token in ("secure", "verify", "login", "reset")):
            return 3
        if hostname.count("-") >= 2:
            return 7
        return 120

    def _resolve_registrar(self, hostname: str) -> str:
        if _is_trusted_hostname(hostname):
            return "Trusted Registrar"
        for token, registrar in REGISTRAR_HINTS.items():
            if token in hostname:
                return registrar
        return "Trusted Registrar"

    def _resolve_dns_records(self, hostname: str) -> int:
        if _is_trusted_hostname(hostname):
            return 4
        return 0 if any(token in hostname for token in ("secure", "verify")) else 4

    def _resolve_ssl(self, hostname: str) -> bool:
        if _is_trusted_hostname(hostname):
            return True
        return not any(token in hostname for token in ("reset", "wallet"))


class DomainIntelligenceService:
    def __init__(self, provider: WhoisProvider | None = None) -> None:
        self.provider = provider or HeuristicWhoisProvider()

    def extract(self, hostname: str, current: DomainContext | None = None) -> DomainContext:
        base = current or DomainContext()
        metadata = self.provider.lookup(hostname)
        return replace(
            base,
            domain_age_days=base.domain_age_days if base.domain_age_days is not None else metadata.domain_age_days,
            registrar=base.registrar or metadata.registrar,
            dns_record_count=base.dns_record_count if base.dns_record_count is not None else metadata.dns_record_count,
            has_ssl=base.has_ssl if base.has_ssl is not None else metadata.has_ssl,
            source=base.source or metadata.source,
        )


class ContextEnricher:
    def __init__(self, domain_service: DomainIntelligenceService | None = None) -> None:
        self.domain_service = domain_service or DomainIntelligenceService()

    def enrich(self, url: str, context: ScanRequestContext | None = None) -> ScanRequestContext:
        base = context or ScanRequestContext()
        hostname = (urlparse(url).hostname or "").lower()

        domain = self.domain_service.extract(hostname, base.domain)
        content = replace(
            base.content,
            claimed_brand=base.content.claimed_brand or self._infer_brand(hostname),
            genuine_url=base.content.genuine_url or self._infer_reference_url(hostname),
            login_form_detected=self._resolve_login_form(hostname, base.content.login_form_detected, base.content.text_snippet),
        )
        return ScanRequestContext(domain=domain, content=content, visual=base.visual)

    def _infer_brand(self, hostname: str) -> str | None:
        for token, brand in BRAND_HINTS.items():
            if token in hostname:
                return brand
        return None

    def _infer_reference_url(self, hostname: str) -> str | None:
        brand = self._infer_brand(hostname)
        if brand == "Paytm":
            return "https://paytm.com"
        if brand == "Amazon":
            return "https://amazon.in"
        if brand == "SBI":
            return "https://sbi.co.in"
        if brand == "Google":
            return "https://google.com"
        if brand == "Microsoft":
            return "https://microsoft.com"
        return None

    def _resolve_login_form(self, hostname: str, current: bool | None, text_snippet: str | None) -> bool | None:
        if current is not None:
            return current
        sample = f"{hostname} {(text_snippet or '').lower()}"
        if any(token in sample for token in ("login", "signin", "password", "verify", "otp")):
            return True
        return False
