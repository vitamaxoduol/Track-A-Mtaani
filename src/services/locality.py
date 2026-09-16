"""Resolve only the pilot's reviewed locality names; never infer a home ward."""

import re


def normalize(text: str) -> str:
    return " ".join(text.casefold().split())


def resolve_localities(text: str, coverage: dict) -> list[str]:
    text = normalize(text)
    return [name for name in coverage["wards"] if re.search(r"\b" + re.escape(name.casefold()) + r"\b", text)]


def has_uncovered_location(text: str, coverage: dict) -> bool:
    """Conservatively reject unknown places in explicit 'in/near/around' clauses.

    A familiar project or ward elsewhere in the same sentence must not cause a
    question about an uncovered place to receive a misleading local answer.
    """
    allowed = set(normalize(" ".join([coverage["county"], *coverage["wards"]])).split())
    allowed.update({"and", "ward", "wards", "county", "the", "na", "wadi", "ya", "kaunti"})
    for match in re.finditer(r"\b(?:in|near|around|katika|karibu na)\s+([^?.!;]+)", normalize(text)):
        area = re.split(r"\b(?:for|during|in|near|around|katika|karibu na|fy|financial|kwa|mwaka)\b|\b20\d{2}\b", match.group(1))[0]
        tokens = re.findall(r"[a-z]+", area)
        if any(token not in allowed for token in tokens):
            return True
    return False


def financial_years(text: str) -> list[str]:
    years = []
    for start, end in re.findall(r"\b(20\d{2})\s*[/–-]\s*(20\d{2}|\d{2})\b", text):
        end = end if len(end) == 4 else start[:2] + end
        years.append(f"{start}/{end}")
    return list(dict.fromkeys(years))


def sector_for(text: str) -> str | None:
    for pattern, sector in [
        (r"\b(barabara|roads?|murram\w*|grading)\b", "roads"),
        (r"\b(shule|elimu|school\w*|education|ecde|classroom\w*)\b", "education"),
        (r"\b(taa|umeme|street\s?lights?|energy|electricity)\b", "energy"),
        (r"\b(maji|visima|water|boreholes?)\b", "water"),
        (r"\b(afya|hospital\w*|dispensar\w*)\b", "health"),
    ]:
        if re.search(pattern, text, re.I):
            return sector
    return None
