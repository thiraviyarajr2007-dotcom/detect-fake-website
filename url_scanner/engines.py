from __future__ import annotations

import ipaddress
from dataclasses import dataclass, field
from urllib.parse import urlparse

from .architecture import CONTENT_WEIGHT, DOMAIN_WEIGHT, IMAGE_WEIGHT
from .content_similarity import ContentSimilarityService
from .models import ContentContext, DomainContext, EngineBreakdown, VisualContext
from .visual_similarity import VisualSimilarityService

KNOWN_PHISHING_DOMAINS = {
    "secure-login-example.com",
    "paypa1-alerts.com",
    "account-verification-bad.com",
    "microsoft-reset-live.com",
}

HIGH_RISK_KEYWORDS = {
    "login",
    "verify",
    "update",
    "password",
    "secure",
    "wallet",
    "signin",
    "bank",
    "paytm",
    "amazon",
    "sbi",
}

TRUSTED_BRAND_DOMAINS = {
    "paytm": "paytm.com",
    "amazon": "amazon.in",
    "sbi": "sbi.co.in",
    "google": "google.com",
    "microsoft": "microsoft.com",
}

TRUSTED_REFERENCE_DOMAINS = {
    "google.com",
    "google.co.in",
    "youtube.com",
    "facebook.com",
    "instagram.com",
    "chatgpt.com",
    "reddit.com",
    "wikipedia.org",
    "twitter.com",
    "whatsapp.com",
    "yahoo.com",
    "amazon.com",
    "amazon.in",
    "tiktok.com",
    "duckduckgo.com",
    "bing.com",
    "linkedin.com",
    "microsoft.com",
    "apple.com",
    "netflix.com",
    "pinterest.com",
    "flipkart.com",
    "paytm.com",
    "phonepe.com",
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


def _matches_trusted_domain(hostname: str) -> bool:
    return any(_is_same_or_subdomain(hostname, trusted_domain) for trusted_domain in TRUSTED_REFERENCE_DOMAINS)


def _is_same_or_subdomain(hostname: str, trusted_domain: str) -> bool:
    return hostname == trusted_domain or hostname.endswith(f".{trusted_domain}")


def _clamp_score(score: float) -> int:
    return max(0, min(100, int(round(score))))


@dataclass(slots=True)
class DomainIntelligenceEngine:
    def analyze(self, url: str, context: DomainContext) -> EngineBreakdown:
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        path = parsed.path.lower()
        reasons: list[str] = []
        score = 0.0
        trusted_host = _matches_trusted_domain(hostname.lower())

        if hostname in KNOWN_PHISHING_DOMAINS:
            reasons.append("Domain matches a known phishing domain.")
            return EngineBreakdown(score=100, reasons=reasons)

        if trusted_host:
            return EngineBreakdown(score=0, reasons=[])

        if self._is_ip_hostname(hostname):
            score += 30
            reasons.append("The website uses an IP address instead of a normal domain name.")

        if hostname.count(".") >= 3:
            score += 15
            reasons.append("The domain uses excessive subdomains, a common phishing tactic.")

        if hostname.count("-") >= 2:
            score += 12
            reasons.append("The domain contains multiple hyphens and looks machine-generated.")

        if not trusted_host and any(keyword in hostname.lower() or keyword in path for keyword in HIGH_RISK_KEYWORDS):
            score += 18
            reasons.append("The URL contains high-risk words often seen in phishing pages.")

        if context.domain_age_days is not None:
            if context.domain_age_days <= 7:
                score += 35
                reasons.append(f"Domain registered {context.domain_age_days} day(s) ago.")
            elif context.domain_age_days <= 30:
                score += 20
                reasons.append(f"Domain registered recently ({context.domain_age_days} days old).")

        if context.has_ssl is False:
            score += 20
            reasons.append("SSL certificate is missing.")

        if context.dns_record_count is not None and context.dns_record_count == 0:
            score += 12
            reasons.append("DNS records appear incomplete or missing.")

        if context.registrar:
            registrar = context.registrar.lower()
            if "privacy" in registrar or "cheap" in registrar:
                score += 8
                reasons.append("Registrar metadata suggests low-trust or privacy-shielded registration.")

        if score > 0:
            source = context.source or "user-provided"
            reasons.append(f"Domain intelligence source: {source}.")

        return EngineBreakdown(score=_clamp_score(score), reasons=reasons)

    @staticmethod
    def _is_ip_hostname(hostname: str) -> bool:
        try:
            ipaddress.ip_address(hostname)
            return True
        except ValueError:
            return False


@dataclass(slots=True)
class ContentSimilarityEngine:
    service: ContentSimilarityService = field(default_factory=ContentSimilarityService)

    def analyze(self, url: str, context: ContentContext) -> EngineBreakdown:
        parsed = urlparse(url)
        hostname = (parsed.hostname or "").lower()
        text = " ".join(
            part for part in [context.html_snippet or "", context.text_snippet or "", parsed.path.lower()] if part
        ).lower()
        reasons: list[str] = []
        score = 0.0

        comparison = self.service.compare(
            suspect_html=context.html_snippet,
            genuine_html=context.genuine_html_snippet,
            suspect_text=context.text_snippet,
        )
        tag_similarity = context.tag_similarity
        keyword_similarity = context.keyword_similarity
        dom_similarity = context.dom_similarity
        login_form_detected = context.login_form_detected
        trusted_host = _matches_trusted_domain(hostname)

        if trusted_host:
            return EngineBreakdown(score=0, reasons=[])

        if comparison is not None:
            tag_similarity = tag_similarity if tag_similarity is not None else comparison.tag_similarity
            keyword_similarity = keyword_similarity if keyword_similarity is not None else comparison.keyword_similarity
            dom_similarity = dom_similarity if dom_similarity is not None else comparison.dom_similarity
            if login_form_detected is None:
                login_form_detected = comparison.login_form_similarity >= 100
            if comparison.login_form_similarity >= 100:
                score += 25
                reasons.append("The suspect and genuine pages share a login form structure.")
            if comparison.tag_similarity >= 65:
                score += comparison.tag_similarity * 0.2
                reasons.append(f"HTML tag structure similarity is {int(comparison.tag_similarity)}%.")
            if comparison.keyword_similarity >= 40:
                score += comparison.keyword_similarity * 0.18
                reasons.append(f"Keyword similarity with the genuine page is {int(comparison.keyword_similarity)}%.")
            if comparison.matched_keywords:
                reasons.append(f"Matched phishing-sensitive keywords: {', '.join(comparison.matched_keywords)}.")

        if login_form_detected:
            score += 25
            reasons.append("A login or credential form was detected on the page.")

        keyword_hits = 0 if trusted_host else sum(1 for keyword in HIGH_RISK_KEYWORDS if keyword in text)
        if keyword_hits:
            score += min(30, keyword_hits * 6)
            reasons.append("The page contains phishing-related keywords such as login, verify, or password.")

        if dom_similarity is not None:
            dom_points = max(0.0, min(100.0, dom_similarity))
            score += dom_points * 0.35
            if dom_points >= 70:
                reasons.append(f"DOM structure similarity is high ({int(dom_points)}%).")

        if context.claimed_brand:
            brand = context.claimed_brand.lower()
            trusted_domain = TRUSTED_BRAND_DOMAINS.get(brand)
            if trusted_domain and not _is_same_or_subdomain(hostname, trusted_domain):
                score += 25
                reasons.append(f"The page claims to represent {context.claimed_brand}, but the domain does not match the official brand domain.")

        if context.genuine_url:
            genuine_host = (urlparse(context.genuine_url).hostname or "").lower()
            if genuine_host and not _is_same_or_subdomain(hostname, genuine_host):
                score += 10
                reasons.append("The scanned site differs from the genuine reference domain.")

        return EngineBreakdown(score=_clamp_score(score), reasons=reasons)


@dataclass(slots=True)
class VisualSimilarityEngine:
    service: VisualSimilarityService = field(default_factory=VisualSimilarityService)

    def analyze(self, context: VisualContext) -> EngineBreakdown:
        screenshot_similarity = context.screenshot_similarity
        if screenshot_similarity is None:
            screenshot_similarity = self.service.compare_hashes(
                context.suspect_screenshot_hash,
                context.genuine_screenshot_hash,
            )

        comparison = self.service.combine(
            screenshot_similarity=screenshot_similarity,
            logo_similarity=context.logo_similarity,
            layout_similarity=context.layout_similarity,
            theme_similarity=context.theme_similarity,
        )
        if comparison is None:
            return EngineBreakdown(score=0, reasons=[])

        similarities = [
            ("Screenshot similarity", comparison.screenshot_similarity),
            ("Logo similarity", comparison.logo_similarity),
            ("Layout similarity", comparison.layout_similarity),
            ("Theme similarity", comparison.theme_similarity),
        ]
        present = [(label, value) for label, value in similarities if value is not None]

        average = sum(max(0.0, min(100.0, value)) for _, value in present) / len(present)
        reasons = [f"{label}: {int(value)}%." for label, value in present if value >= 60]

        if average >= 80:
            reasons.append("Visual match is very high and suggests lookalike impersonation.")
        elif average >= 60:
            reasons.append("Visual similarity is notable and may indicate brand imitation.")

        return EngineBreakdown(score=_clamp_score(average), reasons=reasons)


@dataclass(slots=True)
class FusionEngine:
    def combine(
        self,
        url: str,
        domain_result: EngineBreakdown,
        content_result: EngineBreakdown,
        visual_result: EngineBreakdown,
    ) -> tuple[int, list[str]]:
        probability = _clamp_score(
            domain_result.score * DOMAIN_WEIGHT
            + content_result.score * CONTENT_WEIGHT
            + visual_result.score * IMAGE_WEIGHT
        )
        explanations = list(dict.fromkeys(domain_result.reasons + content_result.reasons + visual_result.reasons))
        hostname = (urlparse(url).hostname or "").lower()

        if hostname in KNOWN_PHISHING_DOMAINS:
            probability = 100
            explanations.insert(0, "Known phishing domain triggered an automatic escalation.")
        elif _matches_trusted_domain(hostname):
            probability = min(probability, 10)
            explanations = [item for item in explanations if "high-risk words" not in item.lower() and "privacy-shielded" not in item.lower()]
        elif content_result.score >= 70 and visual_result.score >= 70 and domain_result.score >= 45:
            probability = max(probability, 95)
            explanations.insert(0, "Combined content and visual impersonation signals triggered a phishing escalation.")

        return probability, explanations
