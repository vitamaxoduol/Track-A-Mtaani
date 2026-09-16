"""Validated source records. Money stays exact throughout ingestion and output."""

from datetime import date
from decimal import Decimal
from typing import Annotated, Literal
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SourceDocument(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    title: str = Field(min_length=1)
    publisher: str = Field(min_length=1)
    official_url: str
    local_path: str
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    financial_year: str = Field(pattern=r"^20\d{2}/20\d{2}$")

    @field_validator("official_url")
    @classmethod
    def official_link(cls, value: str) -> str:
        url = urlparse(value)
        if url.scheme != "https" or not url.hostname or not url.hostname.endswith(".go.ke"):
            raise ValueError("Source must be an official Kenyan government HTTPS URL")
        if url.username or url.password or url.fragment:
            raise ValueError("Source URL must not contain credentials or a fragment")
        return value


class Observation(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    amount_kes: str = Field(pattern=r"^\d+\.\d{2}$")
    currency: Literal["KES"]
    amount_kind: Literal["ALLOCATION"]
    original_amount: str = Field(min_length=1)
    original_units: Literal["Kshs."]
    source_amount_heading: str = Field(min_length=1)
    financial_year: str = Field(pattern=r"^20\d{2}/20\d{2}$")
    approval_stage: Literal["APPROVED"]
    implementation_state: None
    source_id: str
    source_pdf_page: int = Field(gt=0)
    source_printed_page_label: str = Field(min_length=1)
    source_excerpt: str = Field(min_length=1)
    review_status: Literal["REVIEWED"]
    reviewer: str = Field(min_length=1)
    reviewed_date: date

    @field_validator("amount_kes")
    @classmethod
    def sqlite_amount_range(cls, value: str) -> str:
        if Decimal(value) * 100 > 9_223_372_036_854_775_807:
            raise ValueError("Amount exceeds SQLite exact integer storage range")
        return value


class Project(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    name: str = Field(min_length=1)
    county: str = Field(min_length=1)
    ward: str = Field(min_length=1)
    department: str = Field(min_length=1)
    spending_unit: str
    observations: Annotated[list[Observation], Field(min_length=1)]


class Dataset(BaseModel):
    schema_version: Literal[1]
    dataset_status: Literal["REVIEWED"]
    sources: list[SourceDocument]
    coverage: dict
    projects: Annotated[list[Project], Field(min_length=1)]
