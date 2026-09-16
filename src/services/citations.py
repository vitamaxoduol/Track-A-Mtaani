"""Render trusted financial fields without generative rewriting."""

from decimal import Decimal

ALLOCATION_NOTICE = "This is a budget allocation, not proof that money was spent or work completed."


def format_kes(minor_units: int) -> str:
    value = Decimal(minor_units) / 100
    return f"KSh {value:,.0f}" if minor_units % 100 == 0 else f"KSh {value:,.2f}"


def citation(source: dict, observation: dict) -> dict:
    page = observation["source_pdf_page"]
    return {
        "document_title": source["title"], "publisher": source["publisher"],
        "url": source["official_url"], "page_url": f"{source['official_url']}#page={page}",
        "pdf_page": page, "printed_page": observation["source_printed_page_label"],
        "excerpt": observation["source_excerpt"],
        "amount_heading": observation["source_amount_heading"],
        "reviewed_date": observation["reviewed_date"],
    }
