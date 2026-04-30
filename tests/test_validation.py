from url_scanner.validation import validate_url


def test_validate_url_accepts_http_and_https() -> None:
    assert validate_url("http://example.com") == "http://example.com"
    assert validate_url("https://Example.com/login#frag") == "https://example.com/login"


def test_validate_url_rejects_empty_and_malformed_values() -> None:
    assert validate_url("") is None
    assert validate_url("example.com") is None
    assert validate_url("https:///missing-host") is None
    assert validate_url("ftp://example.com") is None
