"""Track-A-Mtaani: one app and shared bilingual conversation service."""

import time
from collections import deque
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from src.api.whatsapp import WhatsAppAdapter, WhatsAppSettings, router as whatsapp_router
from src.db.database import ROOT, default_db_path
from src.db.seed import SEED_PATH, seed_database
from src.models.evidence import ChatRequest, ChatResponse
from src.services.intent import ConversationService
from src.services.projects import get_coverage, search_projects


def create_app(db_path: Path | None = None, seed_path: Path = SEED_PATH,
               whatsapp_settings: WhatsAppSettings | None = None) -> FastAPI:
    path = db_path or default_db_path()

    @asynccontextmanager
    async def lifespan(app):
        seed_database(path, seed_path)
        app.state.conversation = ConversationService(path)
        settings = whatsapp_settings or WhatsAppSettings.from_environment()
        app.state.whatsapp = WhatsAppAdapter(settings, app.state.conversation, path) if settings else None
        yield
        app.state.conversation.sessions.clear()
        if app.state.whatsapp:
            app.state.whatsapp.senders.clear()

    app = FastAPI(title="Track-A-Mtaani", version="0.1.0", lifespan=lifespan)
    recent_requests = deque()

    @app.exception_handler(RequestValidationError)
    async def invalid_request(request, error):
        # Do not echo user inputs, phone numbers, or arbitrary message bodies.
        return JSONResponse(status_code=422, content={"detail": "Invalid request. Use a question of 1–1000 characters or a supported action."})

    @app.middleware("http")
    async def request_limits(request: Request, call_next):
        if request.method == "POST":
            body = bytearray()
            async for chunk in request.stream():
                body.extend(chunk)
                if len(body) > 8192:
                    return JSONResponse(status_code=413, content={"detail": "Message is too large."})
            request._body = bytes(body)
        if request.url.path in {"/api/v1/chat", "/api/v1/whatsapp/webhook"}:
            now = time.monotonic()
            while recent_requests and now - recent_requests[0] >= 60:
                recent_requests.popleft()
            if len(recent_requests) >= 120:
                return JSONResponse(status_code=429, content={"detail": "The demo is busy. Please retry in one minute."}, headers={"Retry-After": "60"})
            recent_requests.append(now)
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store"
        return response

    @app.get("/", include_in_schema=False)
    def index():
        return FileResponse(ROOT / "frontend/index.html")

    @app.get("/health")
    def health():
        return {"status": "ok", "milestone": "3"}

    @app.get("/api/v1/coverage")
    def coverage():
        return get_coverage(path)

    @app.get("/api/v1/projects")
    def projects(county: str | None = Query(None, max_length=80), ward: str | None = Query(None, max_length=80),
                 financial_year: str | None = Query(None, pattern=r"^20\d{2}/20\d{2}$"),
                 sector: Literal["roads", "education", "energy", "water", "health"] | None = None,
                 offset: int = Query(0, ge=0), limit: int = Query(3, ge=1, le=30)):
        results = search_projects(path, county=county, ward=ward, financial_year=financial_year, sector=sector)
        return {"projects": results[offset:offset + limit], "total": len(results), "coverage": get_coverage(path)}

    @app.get("/api/v1/projects/{project_id}")
    def project(project_id: str):
        results = search_projects(path, project_id=project_id)
        if not results:
            raise HTTPException(404, "Project not found in the reviewed pilot dataset.")
        return results[0]

    @app.post("/api/v1/chat", response_model=ChatResponse)
    def chat(body: ChatRequest, request: Request):
        return request.app.state.conversation.reply(body)

    app.include_router(whatsapp_router)
    app.mount("/static", StaticFiles(directory=ROOT / "frontend"), name="static")
    return app


app = create_app()
