"""Main threat detection logic for the phishing detection app."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

from .api_checker import check_with_api
from .config import SUSPICION_THRESHOLD, USE_API_CHECKER
from .feature_extractor import extract_features

MODULE_DIR = Path(__file__).resolve().parent
BLACKLIST_PATH = MODULE_DIR / "blacklist.txt"
THREAT_DB_PATH = MODULE_DIR / "threat_db.json"


def _get_hostname(url: str) -> str:
    """Extract the hostname from a URL."""
    parsed = urlparse(url.strip())
    hostname = parsed.hostname or parsed.path
    return hostname.lower()


def _load_blacklist() -> set[str]:
    """Read all blacklisted domains into a set."""
    if not BLACKLIST_PATH.exists():
        return set()

    with BLACKLIST_PATH.open("r", encoding="utf-8") as file:
        return {
            line.strip().lower()
            for line in file
            if line.strip() and not line.strip().startswith("#")
        }


def _load_threat_db() -> dict[str, str]:
    """Read the local threat database."""
    if not THREAT_DB_PATH.exists():
        return {}

    with THREAT_DB_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return {key.lower(): value.lower() for key, value in data.items()}


def _score_features(features: dict[str, int | bool]) -> int:
    """Turn extracted URL features into a simple suspicion score."""
    score = 0

    # Longer URLs can hide phishing tricks more easily.
    if int(features["url_length"]) > 50:
        score += 1

    # Many dots can suggest deceptive subdomains.
    if int(features["dot_count"]) > 3:
        score += 1

    # Missing HTTPS is suspicious for login-style pages.
    if not bool(features["has_https"]):
        score += 1

    # Special symbols often appear in fake URLs.
    if bool(features["has_at_symbol"]):
        score += 1
    if bool(features["has_dash"]):
        score += 1
    if bool(features["has_underscore"]):
        score += 1

    return score


def detect_url(url: str) -> str:
    """Detect whether a URL is safe or phishing."""
    hostname = _get_hostname(url)
    blacklist = _load_blacklist()
    threat_db = _load_threat_db()

    # Step 1: Block anything already known to be malicious.
    if hostname in blacklist:
        return "PHISHING"

    # Step 2: Check our local domain database.
    if hostname in threat_db:
        if threat_db[hostname] == "phishing":
            return "PHISHING"
        if threat_db[hostname] == "safe":
            return "SAFE"

    # Step 3: Extract basic URL features.
    features = extract_features(url)
    feature_score = _score_features(features)

    # Step 4: Optionally consult a simulated external API.
    api_result = "safe"
    if USE_API_CHECKER:
        api_result = check_with_api(url)

    # Step 5: Combine the results in a simple and readable way.
    if feature_score >= SUSPICION_THRESHOLD:
        return "PHISHING"

    if api_result == "phishing":
        return "PHISHING"

    return "SAFE"
