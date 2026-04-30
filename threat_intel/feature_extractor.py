"""Simple URL feature extraction for phishing detection."""

from __future__ import annotations


def extract_features(url: str) -> dict[str, int | bool]:
    """Extract simple beginner-friendly features from a URL."""
    lowered_url = url.strip().lower()

    # Count easy-to-understand URL characteristics.
    features = {
        "url_length": len(lowered_url),
        "dot_count": lowered_url.count("."),
        "has_https": lowered_url.startswith("https://"),
        "has_at_symbol": "@" in lowered_url,
        "has_dash": "-" in lowered_url,
        "has_underscore": "_" in lowered_url,
    }
    return features
