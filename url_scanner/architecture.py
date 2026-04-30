from __future__ import annotations

from dataclasses import dataclass


DOMAIN_WEIGHT = 0.4
CONTENT_WEIGHT = 0.3
IMAGE_WEIGHT = 0.3


@dataclass(frozen=True, slots=True)
class ScoringWeights:
    domain: float = DOMAIN_WEIGHT
    content: float = CONTENT_WEIGHT
    image: float = IMAGE_WEIGHT


def describe_architecture() -> dict[str, object]:
    return {
        "pipeline": [
            "New Domains (WHOIS)",
            "Feature Extraction",
            "AI/ML Models",
            "Fusion Engine",
            "Phishing Probability Score",
            "Output Dashboard / API",
        ],
        "feature_extraction": [
            "Domain Features",
            "HTML Content",
            "Website Screenshot",
        ],
        "models": [
            "Random Forest (URL + Domain)",
            "NLP Similarity (Content)",
            "CNN / Visual Similarity (Image)",
        ],
        "weights": {
            "domain": DOMAIN_WEIGHT,
            "content": CONTENT_WEIGHT,
            "image": IMAGE_WEIGHT,
        },
        "formula": "0.4 * Domain Score + 0.3 * Content Similarity + 0.3 * Image Similarity",
        "key_features": [
            "Probability score (0-100%)",
            "Fast detection of newly registered domains",
            "Dashboard and API output",
            "Explainable AI evidence for every verdict",
        ],
        "example": {
            "domain": "paytm-secure-login.com",
            "phishing_probability": 91,
            "domain_risk": 85,
            "content_similarity": 92,
            "image_similarity": 95,
            "final_result": "HIGH RISK (Phishing)",
        },
    }
