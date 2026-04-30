from __future__ import annotations

from pathlib import Path
import csv
import io
from collections import Counter
from urllib.parse import quote
from urllib.request import Request, urlopen

from fastapi import Cookie, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, Response
from pydantic import BaseModel, Field

from .architecture import describe_architecture
from .analyzer import AnalysisError, Analyzer
from .auth import AuthStore
from .cache import CacheService
from .dashboard import render_dashboard
from .intelligence import ContextEnricher
from .login_page import render_login
from .models import (
    ContentContext,
    DomainContext,
    ScanRequestContext,
    ScanResult,
    Verdict,
    VisualContext,
)
from .monitoring import DomainFeedMonitor
from .storage import ScanStore
from .validation import validate_url


class DomainContextPayload(BaseModel):
    domain_age_days: int | None = Field(default=None, ge=0)
    registrar: str | None = None
    dns_record_count: int | None = Field(default=None, ge=0)
    has_ssl: bool | None = None

    def to_model(self) -> DomainContext:
        return DomainContext(
            domain_age_days=self.domain_age_days,
            registrar=self.registrar,
            dns_record_count=self.dns_record_count,
            has_ssl=self.has_ssl,
        )


class ContentContextPayload(BaseModel):
    claimed_brand: str | None = None
    genuine_url: str | None = None
    html_snippet: str | None = None
    genuine_html_snippet: str | None = None
    text_snippet: str | None = None
    dom_similarity: float | None = Field(default=None, ge=0, le=100)
    tag_similarity: float | None = Field(default=None, ge=0, le=100)
    keyword_similarity: float | None = Field(default=None, ge=0, le=100)
    login_form_detected: bool | None = None

    def to_model(self) -> ContentContext:
        return ContentContext(
            claimed_brand=self.claimed_brand,
            genuine_url=self.genuine_url,
            html_snippet=self.html_snippet,
            genuine_html_snippet=self.genuine_html_snippet,
            text_snippet=self.text_snippet,
            dom_similarity=self.dom_similarity,
            tag_similarity=self.tag_similarity,
            keyword_similarity=self.keyword_similarity,
            login_form_detected=self.login_form_detected,
        )


class VisualContextPayload(BaseModel):
    screenshot_similarity: float | None = Field(default=None, ge=0, le=100)
    logo_similarity: float | None = Field(default=None, ge=0, le=100)
    layout_similarity: float | None = Field(default=None, ge=0, le=100)
    theme_similarity: float | None = Field(default=None, ge=0, le=100)
    suspect_screenshot_hash: str | None = None
    genuine_screenshot_hash: str | None = None

    def to_model(self) -> VisualContext:
        return VisualContext(
            screenshot_similarity=self.screenshot_similarity,
            logo_similarity=self.logo_similarity,
            layout_similarity=self.layout_similarity,
            theme_similarity=self.theme_similarity,
            suspect_screenshot_hash=self.suspect_screenshot_hash,
            genuine_screenshot_hash=self.genuine_screenshot_hash,
        )


class ScanRequest(BaseModel):
    url: str = Field(min_length=1)
    force_refresh: bool = False
    domain: DomainContextPayload = Field(default_factory=DomainContextPayload)
    content: ContentContextPayload = Field(default_factory=ContentContextPayload)
    visual: VisualContextPayload = Field(default_factory=VisualContextPayload)

    def to_context(self) -> ScanRequestContext:
        return ScanRequestContext(
            domain=self.domain.to_model(),
            content=self.content.to_model(),
            visual=self.visual.to_model(),
        )


class MonitorContextPayload(BaseModel):
    domain: DomainContextPayload = Field(default_factory=DomainContextPayload)
    content: ContentContextPayload = Field(default_factory=ContentContextPayload)
    visual: VisualContextPayload = Field(default_factory=VisualContextPayload)

    def to_context(self) -> ScanRequestContext:
        return ScanRequestContext(
            domain=self.domain.to_model(),
            content=self.content.to_model(),
            visual=self.visual.to_model(),
        )


class ScanResultResponse(BaseModel):
    scan_id: str
    url: str
    verdict: Verdict
    timestamp: str
    threat_indicators: list[str]
    is_cached: bool
    phishing_probability: int
    domain_score: int
    content_score: int
    image_score: int
    explanations: list[str]
    brand_target: str | None
    reference_url: str | None
    domain_age_days: int | None
    registrar: str | None
    dns_record_count: int | None
    has_ssl: bool | None
    domain_location: str | None

    @classmethod
    def from_scan_result(cls, result: ScanResult) -> "ScanResultResponse":
        return cls(**result.to_dict())


class MonitorRequest(BaseModel):
    domains: list[str] = Field(min_length=1)
    context: MonitorContextPayload | None = None


class MonitorItemResponse(BaseModel):
    raw_value: str
    normalized_url: str
    result: ScanResultResponse


class MonitorResponse(BaseModel):
    count: int
    items: list[MonitorItemResponse]


class AnalyticsResponse(BaseModel):
    total_scanned: int
    phishing_found: int
    safe_found: int
    suspicious_found: int
    phishing_vs_safe: dict[str, int]
    top_targeted_brands: list[str]


def create_app(db_path: str | Path = "scan_history.db") -> FastAPI:
    app = FastAPI(title="URL Scanner")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:8000",
            "http://localhost:8000",
            "http://127.0.0.1:5500",
            "http://localhost:5500",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    store = ScanStore(db_path)
    analyzer = Analyzer()
    enricher = ContextEnricher()
    auth_store = AuthStore(db_path)
    app.state.store = store
    app.state.cache_service = CacheService(analyzer=analyzer, store=store)
    app.state.monitor = DomainFeedMonitor(analyzer=analyzer, enricher=enricher)
    app.state.enricher = enricher
    app.state.auth_store = auth_store

    @app.get("/login", response_class=HTMLResponse)
    async def login_page() -> HTMLResponse:
        return HTMLResponse(render_login())

    @app.post("/auth/register")
    async def auth_register(payload: dict) -> JSONResponse:
        username = (payload.get("username") or "").strip()
        email = (payload.get("email") or "").strip()
        password = payload.get("password") or ""
        if not username or not email or len(password) < 6:
            raise HTTPException(status_code=422, detail="Username, email, and password (min 6 chars) are required")
        user = app.state.auth_store.register(username, email, password)
        if user is None:
            raise HTTPException(status_code=409, detail="Username or email already exists")
        return JSONResponse({"message": "Account created", "username": user.username})

    @app.post("/auth/login")
    async def auth_login(payload: dict) -> JSONResponse:
        username = (payload.get("username") or "").strip()
        password = payload.get("password") or ""
        user = app.state.auth_store.authenticate(username, password)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        token = app.state.auth_store.create_session(user.user_id)
        response = JSONResponse({"message": "Login successful", "username": user.username})
        response.set_cookie(key="session_token", value=token, httponly=True, samesite="lax", max_age=72 * 3600)
        return response

    @app.post("/auth/logout")
    async def auth_logout(session_token: str | None = Cookie(default=None)) -> JSONResponse:
        if session_token:
            app.state.auth_store.delete_session(session_token)
        response = JSONResponse({"message": "Logged out"})
        response.delete_cookie("session_token")
        return response

    @app.get("/auth/me")
    async def auth_me(session_token: str | None = Cookie(default=None)) -> JSONResponse:
        if not session_token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        user = app.state.auth_store.get_user_by_session(session_token)
        if user is None:
            raise HTTPException(status_code=401, detail="Session expired")
        return JSONResponse({"username": user.username, "email": user.email})

    @app.get("/", response_class=HTMLResponse)
    async def dashboard(session_token: str | None = Cookie(default=None)) -> Response:
        if not session_token or app.state.auth_store.get_user_by_session(session_token) is None:
            return RedirectResponse(url="/login", status_code=302)
        return HTMLResponse(render_dashboard())

    @app.get("/architecture")
    async def architecture() -> dict[str, object]:
        return describe_architecture()

    @app.get("/preview-image")
    async def preview_image(url: str) -> Response:
        normalized = validate_url(url)
        if normalized is None:
            raise HTTPException(status_code=422, detail="Preview URL must be a valid http or https URL")

        preview_source = f"https://image.thum.io/get/width/1200/crop/760/noanimate/{quote(normalized, safe=':/?&=%#')}"
        request = Request(
            preview_source,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
            },
        )
        try:
            with urlopen(request, timeout=20) as upstream:
                content = upstream.read()
                media_type = upstream.headers.get_content_type() or "image/jpeg"
        except Exception as exc:
            raise HTTPException(status_code=502, detail="Preview image could not be generated") from exc

        return Response(content=content, media_type=media_type, headers={"Cache-Control": "public, max-age=3600"})

    @app.get("/analytics", response_model=AnalyticsResponse)
    async def analytics() -> AnalyticsResponse:
        history = app.state.store.get_history()
        brand_counts = Counter(item.brand_target for item in history if item.brand_target)
        phishing_found = sum(1 for item in history if item.verdict is Verdict.PHISHING)
        safe_found = sum(1 for item in history if item.verdict is Verdict.SAFE)
        suspicious_found = sum(1 for item in history if item.verdict is Verdict.SUSPICIOUS)
        return AnalyticsResponse(
            total_scanned=len(history),
            phishing_found=phishing_found,
            safe_found=safe_found,
            suspicious_found=suspicious_found,
            phishing_vs_safe={
                "phishing": phishing_found,
                "safe": safe_found,
                "suspicious": suspicious_found,
            },
            top_targeted_brands=[brand for brand, _ in brand_counts.most_common(3)],
        )

    @app.post("/scan", response_model=ScanResultResponse)
    async def scan_url(payload: ScanRequest) -> ScanResultResponse:
        normalized = validate_url(payload.url)
        if normalized is None:
            raise HTTPException(status_code=422, detail="URL must be a valid http or https URL with a hostname")

        try:
            enriched_context = app.state.enricher.enrich(normalized, payload.to_context())
            result = app.state.cache_service.scan(
                normalized,
                force_refresh=payload.force_refresh,
                context=enriched_context,
            )
        except AnalysisError as exc:
            raise HTTPException(status_code=503, detail="Analysis service unavailable, please retry shortly") from exc

        return ScanResultResponse.from_scan_result(result)

    @app.post("/monitor/preview", response_model=MonitorResponse)
    async def monitor_preview(payload: MonitorRequest) -> MonitorResponse:
        base_context = payload.context.to_context() if payload.context else None
        try:
            items = app.state.monitor.scan_domains(payload.domains, base_context=base_context)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        except AnalysisError as exc:
            raise HTTPException(status_code=503, detail="Batch monitoring failed, please retry shortly") from exc

        return MonitorResponse(
            count=len(items),
            items=[
                MonitorItemResponse(
                    raw_value=item.raw_value,
                    normalized_url=item.normalized_url,
                    result=ScanResultResponse.from_scan_result(item.result),
                )
                for item in items
            ],
        )

    @app.get("/history", response_model=list[ScanResultResponse])
    async def history() -> list[ScanResultResponse]:
        return [ScanResultResponse.from_scan_result(item) for item in app.state.store.get_history()]

    @app.get("/history/export.csv", response_class=PlainTextResponse)
    async def export_history() -> PlainTextResponse:
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["scan_id", "url", "verdict", "probability", "domain_score", "content_score", "image_score", "timestamp"])
        for item in app.state.store.get_history():
            writer.writerow(
                [
                    item.scan_id,
                    item.url,
                    item.verdict.value,
                    item.phishing_probability,
                    item.domain_score,
                    item.content_score,
                    item.image_score,
                    item.timestamp.isoformat(),
                ]
            )
        return PlainTextResponse(
            buffer.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=phishing-scan-history.csv"},
        )

    @app.get("/history/{scan_id}", response_model=ScanResultResponse)
    async def history_item(scan_id: str) -> ScanResultResponse:
        result = app.state.store.get_by_id(scan_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Scan result not found")
        return ScanResultResponse.from_scan_result(result)

    @app.get("/history/{scan_id}/report.txt", response_class=PlainTextResponse)
    async def history_report(scan_id: str) -> PlainTextResponse:
        result = app.state.store.get_by_id(scan_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Scan result not found")

        lines = [
            "Phishing Detection Report",
            f"Scan ID: {result.scan_id}",
            f"URL: {result.url}",
            f"Verdict: {result.verdict.value}",
            f"Phishing Probability: {result.phishing_probability}%",
            f"Domain Score: {result.domain_score}",
            f"Content Score: {result.content_score}",
            f"Image Score: {result.image_score}",
            f"Timestamp: {result.timestamp.isoformat()}",
            "",
            "Explainable AI Evidence:",
        ]
        if result.explanations:
            lines.extend(f"- {item}" for item in result.explanations)
        else:
            lines.append("- No suspicious evidence detected.")

        return PlainTextResponse(
            "\n".join(lines),
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename=scan-{result.scan_id}.txt"},
        )

    return app


app = create_app()
