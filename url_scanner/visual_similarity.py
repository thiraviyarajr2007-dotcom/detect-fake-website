from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class VisualComparison:
    screenshot_similarity: float | None
    logo_similarity: float | None
    layout_similarity: float | None
    theme_similarity: float | None


class VisualSimilarityService:
    def compare_hashes(
        self,
        suspect_hash: str | None,
        genuine_hash: str | None,
    ) -> float | None:
        if not suspect_hash or not genuine_hash or len(suspect_hash) != len(genuine_hash):
            return None
        differing_bits = sum(
            bin(int(left, 16) ^ int(right, 16)).count("1")
            for left, right in zip(suspect_hash.lower(), genuine_hash.lower())
        )
        total_bits = len(suspect_hash) * 4
        similarity = max(0.0, 100.0 - (differing_bits / total_bits) * 100.0)
        return round(similarity, 2)

    def combine(
        self,
        screenshot_similarity: float | None,
        logo_similarity: float | None,
        layout_similarity: float | None,
        theme_similarity: float | None,
    ) -> VisualComparison | None:
        values = [screenshot_similarity, logo_similarity, layout_similarity, theme_similarity]
        if not any(value is not None for value in values):
            return None
        return VisualComparison(
            screenshot_similarity=screenshot_similarity,
            logo_similarity=logo_similarity,
            layout_similarity=layout_similarity,
            theme_similarity=theme_similarity,
        )
