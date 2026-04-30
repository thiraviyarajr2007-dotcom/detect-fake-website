import time

import pytest

from url_scanner.analyzer import AnalysisTimeoutError, Analyzer
from url_scanner.models import DomainContext, ScanRequestContext, Verdict, VisualContext, ContentContext


def test_known_phishing_domain_returns_phishing() -> None:
    result = Analyzer().analyze("https://secure-login-example.com")
    assert result.verdict is Verdict.PHISHING
    assert result.phishing_probability == 100
    assert any("known phishing domain" in item.lower() for item in result.threat_indicators)


def test_clean_url_returns_safe() -> None:
    result = Analyzer().analyze("https://example.com/about")
    assert result.verdict is Verdict.SAFE
    assert result.threat_indicators == []
    assert result.phishing_probability == 0


def test_multilayer_signals_can_escalate_to_phishing() -> None:
    context = ScanRequestContext(
        domain=DomainContext(domain_age_days=2, has_ssl=False),
        content=ContentContext(
            claimed_brand="Paytm",
            genuine_url="https://paytm.com",
            html_snippet="<form><input type='text' /><input type='password' /><button>Login</button></form>",
            genuine_html_snippet="<form><input type='email' /><input type='password' /><button>Login</button></form>",
            text_snippet="login verify password secure wallet",
            login_form_detected=True,
        ),
        visual=VisualContext(
            logo_similarity=96,
            layout_similarity=93,
            theme_similarity=90,
            suspect_screenshot_hash="ffeeddccbbaa9988",
            genuine_screenshot_hash="ffeeddccbbab9988",
        ),
    )
    result = Analyzer().analyze("https://paytm-secure-login.com", context=context)
    assert result.verdict is Verdict.PHISHING
    assert result.domain_score > 0
    assert result.content_score >= 70
    assert result.image_score >= 80
    assert any("domain registered 2 day" in item.lower() for item in result.explanations)
    assert any("domain intelligence source" in item.lower() for item in result.explanations)


def test_timeout_raises_timeout_error(monkeypatch: pytest.MonkeyPatch) -> None:
    analyzer = Analyzer(timeout_seconds=0.01)

    def slow_analysis(url: str, context):
        time.sleep(0.1)
        return analyzer._analyze_url(url, context)

    monkeypatch.setattr(analyzer, "_analyze_url", slow_analysis)

    with pytest.raises(AnalysisTimeoutError):
        analyzer.analyze("https://example.com")
