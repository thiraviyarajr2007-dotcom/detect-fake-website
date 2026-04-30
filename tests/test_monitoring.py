from url_scanner.analyzer import Analyzer
from url_scanner.models import ScanRequestContext
from url_scanner.monitoring import DomainFeedMonitor


def test_monitoring_normalizes_domains_without_scheme() -> None:
    monitor = DomainFeedMonitor(Analyzer())

    results = monitor.scan_domains(["paytm-secure-login.com"], base_context=ScanRequestContext())

    assert results[0].normalized_url == "https://paytm-secure-login.com"
    assert results[0].result.phishing_probability >= 1
