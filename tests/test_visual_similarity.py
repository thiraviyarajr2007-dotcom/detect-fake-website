from url_scanner.visual_similarity import VisualSimilarityService


def test_visual_similarity_hash_comparison_returns_high_match_for_nearby_hashes() -> None:
    service = VisualSimilarityService()

    similarity = service.compare_hashes("ffeeddccbbaa9988", "ffeeddccbbab9988")

    assert similarity is not None
    assert similarity >= 80
