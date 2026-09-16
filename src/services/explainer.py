"""Bounded, source-linked explanations with no AI dependency or model output.

Definitions and Kiswahili wording approved by the owner on 2026-09-15.
"""
import re
from src.services.translator import notice

GLOSSARY = {
    'allocation': {
        'aliases': ['allocation', 'budget allocation', 'mgao', 'mgao wa bajeti', 'bajeti'],
        'en': 'A budget allocation is an amount set aside in a budget for a stated purpose. It does not show that cash was released, spent, or that work was completed.',
        'sw': 'Mgao wa bajeti ni kiasi kilichotengwa katika bajeti kwa kusudi lililotajwa. Hauonyeshi kwamba fedha zilitolewa, zilitumika, au kazi ilikamilika.',
        'source': {'title': 'Nyeri County Approved Budget Estimates 2026/2027 — Programme Based Budget', 'url': 'https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf', 'pdf_page': 278, 'note': 'Pilot interpretation of the approved allocation columns; not a spending record.'},
    },
    'recurrent expenditure': {
        'aliases': ['recurrent', 'recurrent expenditure', 'matumizi ya kawaida'],
        'en': 'Recurrent expenditure covers the costs of running government services. This general definition does not show spending on any particular project.',
        'sw': 'Matumizi ya kawaida ni gharama za kuendesha huduma za serikali. Maana hii ya jumla haionyeshi matumizi ya fedha kwa mradi wowote mahsusi.',
    },
    'development expenditure': {
        'aliases': ['development', 'development expenditure', 'matumizi ya maendeleo'],
        'en': 'Development expenditure covers creating or renewing assets. A budget entry in this category does not prove that the asset has been built or renewed.',
        'sw': 'Matumizi ya maendeleo ni gharama za kuunda au kukarabati mali. Rekodi ya bajeti katika kundi hili haithibitishi kwamba mali imejengwa au kukarabatiwa.',
    },
}
for term in ['recurrent expenditure', 'development expenditure']:
    GLOSSARY[term]['source'] = {
        'title': 'National Treasury — Standard Chart of Accounts Manual, March 2026',
        'url': 'https://www.treasury.go.ke/sites/default/files/Latest%20updates/SCOA%20Mar%202026.pdf',
        'pdf_page': 36, 'note': 'Section 6.4; printed page 35. General terminology, not project evidence.',
    }


def glossary_term(text: str) -> str | None:
    # Full question patterns keep an unrelated claim from becoming a definition.
    cleaned = text.strip(' ?.！!')
    cleaned = re.sub(r'^(?:explain|eleza|fafanua|maana ya|what is|what does|meaning of)\s+', '', cleaned)
    cleaned = re.sub(r'\s+(?:mean|ni nini)$', '', cleaned)
    return next((key for key, item in GLOSSARY.items() if cleaned in item['aliases']), None)


def definition(term: str, language: str) -> tuple[str, list[dict]]:
    item = GLOSSARY[term]
    return item[language], [dict(item['source'])]


def explain_project(project: dict, language: str) -> str:
    obs = project['observations'][0]
    amount, year = obs['formatted_amount'], obs['financial_year']
    if language == 'sw':
        text = f"Bajeti iliyoidhinishwa imetenga {amount} kwa {project['name']} katika Wadi ya {project['ward']}, mwaka wa fedha {year}."
    else:
        text = f"The approved budget sets aside {amount} for {project['name']} in {project['ward']} Ward for FY {year}."
    return text + ' ' + notice(language)
