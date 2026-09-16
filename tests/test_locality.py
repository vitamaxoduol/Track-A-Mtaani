from src.services.locality import financial_years, resolve_localities

COVERAGE = {"county": "Nyeri", "wards": ["Wamagana", "Mweiga", "Kabaru"]}


def test_exact_locality_names_case_and_word_boundaries():
    assert resolve_localities("Projects in WAMAGANA ward?", COVERAGE) == ["Wamagana"]
    assert resolve_localities("mweiga and kabaru", COVERAGE) == ["Mweiga", "Kabaru"]
    assert resolve_localities("Kabarux", COVERAGE) == []
    assert resolve_localities("Nairobi", COVERAGE) == []
    assert resolve_localities("my ward", COVERAGE) == []


def test_year_normalization_preserves_requested_year():
    assert financial_years("FY 2026/27") == ["2026/2027"]
    assert financial_years("2025/2026 and 2026-2027") == ["2025/2026", "2026/2027"]
    assert financial_years("2026") == []
