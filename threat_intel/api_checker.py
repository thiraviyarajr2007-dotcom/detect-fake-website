"""Dummy API checker used to simulate an external threat feed."""

from __future__ import annotations

import random
from urllib.parse import urlparse


def check_with_api(url: str) -> str:
    """Return a simulated API verdict for the given URL."""
    hostname = (urlparse(url).hostname or url).lower()

    # Seed the random generator with the hostname so the demo stays stable
    # for the same URL while still behaving like a simulated API.
    generator = random.Random(hostname)
    return generator.choice(["safe", "phishing"])
