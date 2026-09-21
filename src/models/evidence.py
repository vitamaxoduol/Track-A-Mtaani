"""Small web contract that can also be used by the next WhatsApp adapter."""

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(default="", max_length=1000)
    session_id: UUID | None = None
    action: Literal["more", "details", "coverage", "explain", "language"] | None = None
    project_id: str | None = Field(default=None, max_length=100)
    language: Literal["en", "sw"] | None = None

    @model_validator(mode="after")
    def require_input(self):
        self.message = self.message.strip()
        if not self.message and self.action is None:
            raise ValueError("Enter a question or select an action")
        if self.message and self.action is not None:
            raise ValueError("Send a question or an action, not both")
        if (self.action == "details" and self.project_id is None) or (self.project_id is not None and self.action not in {"details", "explain"}):
            raise ValueError("A project ID is required for details and allowed for explain")
        if self.action == "language" and self.language is None:
            raise ValueError("Choose EN or SW")
        return self


class ChatResponse(BaseModel):
    session_id: str
    kind: Literal["results", "details", "clarification", "empty", "coverage", "unavailable", "expired", "explanation", "language", "verification"]
    message: str
    projects: list[dict] = Field(default_factory=list)
    choices: list[str] = Field(default_factory=list)
    has_more: bool = False
    coverage: dict
    disclaimer: str | None = None

    language: Literal["en", "sw"] = "en"
    explanation_sources: list[dict] = Field(default_factory=list)
    review_notice: str | None = None
    review_context: str | None = None
    next_steps: str | None = None

    verification: dict | None = None
