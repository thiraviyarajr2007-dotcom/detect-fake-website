from url_scanner.content_similarity import ContentSimilarityService


def test_content_similarity_detects_copied_login_structure() -> None:
    service = ContentSimilarityService()
    suspect_html = """
    <html><body><form><input type="text" /><input type="password" /><button>Login</button></form></body></html>
    """
    genuine_html = """
    <html><body><form><input type="email" /><input type="password" /><button>Login</button></form></body></html>
    """

    comparison = service.compare(suspect_html=suspect_html, genuine_html=genuine_html, suspect_text="login verify password")

    assert comparison is not None
    assert comparison.tag_similarity >= 70
    assert comparison.dom_similarity >= 70
    assert comparison.login_form_similarity == 100
    assert "login" in comparison.matched_keywords
