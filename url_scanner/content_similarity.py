from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from html.parser import HTMLParser
import re

PHISHING_TERMS = {
    "login",
    "verify",
    "password",
    "otp",
    "signin",
    "secure",
    "bank",
    "wallet",
    "account",
}


class _TagParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.text_parts: list[str] = []
        self.form_inputs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        if tag == "input":
            attr_map = {key: value for key, value in attrs}
            input_type = (attr_map.get("type") or "text").lower()
            self.form_inputs.append(input_type)

    def handle_data(self, data: str) -> None:
        cleaned = data.strip()
        if cleaned:
            self.text_parts.append(cleaned)


@dataclass(slots=True)
class ContentFeatures:
    tags: list[str]
    keywords: set[str]
    dom_signature: str
    login_form_detected: bool


@dataclass(slots=True)
class ContentComparison:
    tag_similarity: float
    keyword_similarity: float
    dom_similarity: float
    login_form_similarity: float
    matched_keywords: list[str]


class ContentSimilarityService:
    def extract_features(self, html: str | None, text: str | None = None) -> ContentFeatures:
        parser = _TagParser()
        sample_html = html or ""
        parser.feed(sample_html)
        combined_text = " ".join([*parser.text_parts, text or ""]).lower()
        keywords = {word for word in re.findall(r"[a-z]{3,}", combined_text) if word in PHISHING_TERMS}
        login_form_detected = "password" in parser.form_inputs or ("form" in parser.tags and "login" in combined_text)
        return ContentFeatures(
            tags=parser.tags,
            keywords=keywords,
            dom_signature=">".join(parser.tags[:80]),
            login_form_detected=login_form_detected,
        )

    def compare(
        self,
        suspect_html: str | None,
        genuine_html: str | None,
        suspect_text: str | None = None,
    ) -> ContentComparison | None:
        if not suspect_html or not genuine_html:
            return None

        suspect = self.extract_features(suspect_html, suspect_text)
        genuine = self.extract_features(genuine_html)

        tag_similarity = self._sequence_similarity(suspect.tags, genuine.tags)
        keyword_similarity = self._set_similarity(suspect.keywords, genuine.keywords)
        dom_similarity = self._string_similarity(suspect.dom_signature, genuine.dom_signature)
        login_form_similarity = 100.0 if suspect.login_form_detected and genuine.login_form_detected else 0.0
        matched_keywords = sorted(suspect.keywords & genuine.keywords)

        return ContentComparison(
            tag_similarity=tag_similarity,
            keyword_similarity=keyword_similarity,
            dom_similarity=dom_similarity,
            login_form_similarity=login_form_similarity,
            matched_keywords=matched_keywords,
        )

    def _sequence_similarity(self, left: list[str], right: list[str]) -> float:
        if not left or not right:
            return 0.0
        return round(SequenceMatcher(a=left, b=right).ratio() * 100, 2)

    def _set_similarity(self, left: set[str], right: set[str]) -> float:
        if not left or not right:
            return 0.0
        return round((len(left & right) / len(left | right)) * 100, 2)

    def _string_similarity(self, left: str, right: str) -> float:
        if not left or not right:
            return 0.0
        return round(SequenceMatcher(a=left, b=right).ratio() * 100, 2)
