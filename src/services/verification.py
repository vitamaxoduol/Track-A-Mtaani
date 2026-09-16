"""Conservative one-project/one-amount comparison. No model or external calls.

Only a complete, bounded claim grammar can reach a factual verdict. Free-form
or additional unsupported clauses receive clarification instead of being ignored.
"""
from copy import deepcopy
from decimal import Decimal, InvalidOperation
import re

from src.services.citations import format_kes
from src.services.locality import normalize

# Explicitly approved by the project owner on 2026-09-16.
WORDING_REVIEWED = True

VERDICT_LABELS = {
    'SUPPORTED': {'en': 'Supported by the available source', 'sw': 'Linaungwa mkono na chanzo kilichopo'},
    'PARTIALLY_SUPPORTED': {'en': 'Partially supported', 'sw': 'Linaungwa mkono kwa sehemu'},
    'INSUFFICIENT_EVIDENCE': {'en': 'Insufficient evidence', 'sw': 'Ushahidi hautoshi'},
    'CONTRADICTED_BY_AVAILABLE_SOURCE': {'en': 'Contradicted by the available source', 'sw': 'Linapingwa na chanzo kilichopo'},
}
REASONS = {
    'format': {
        'en': 'Send one complete claim in this format: Verify Kianjogu Karaihu in Wamagana FY 2026/2027 approved allocation KSh 3,000,000. Use the source project name. You may append "and completed" or "and spent"; other clauses require a separate check.',
        'sw': 'Tuma dai moja kamili kwa muundo huu: Hakiki Kianjogu Karaihu katika Wamagana mwaka wa fedha 2026/2027 iliyoidhinishwa mgao KSh 3,000,000. Tumia jina la mradi katika chanzo. Unaweza kuongeza "na umekamilika" au "na zimetumika"; vifungu vingine vinahitaji uhakiki tofauti.',
    },
    'amount': {'en': 'Use one exact non-negative KSh amount, with valid comma grouping and whole cents. Ranges, estimates, and multiple amounts cannot be compared.', 'sw': 'Tumia kiasi kimoja halisi cha KSh kisicho hasi, chenye koma sahihi na senti kamili. Masafa, makadirio na kiasi zaidi ya kimoja haviwezi kulinganishwa.'},
    'year': {'en': 'Specify one financial year, such as 2026/2027. Multi-year totals cannot be compared with a single-year allocation.', 'sw': 'Taja mwaka mmoja wa fedha, kama 2026/2027. Jumla ya miaka mingi haiwezi kulinganishwa na mgao wa mwaka mmoja.'},
    'identity': {'en': 'The exact project and ward did not resolve to one reviewed record. Check the source name and ward, then resend the full claim. Missing coverage does not mean no project exists.', 'sw': 'Jina halisi la mradi na wadi havikutoa rekodi moja iliyokaguliwa. Angalia jina na wadi katika chanzo, kisha tuma dai lote tena. Kukosekana kwa rekodi hakumaanishi kwamba mradi haupo.'},
    'scope': {'en': 'No reviewed observation matches this financial year and document stage. An approved budget cannot establish a draft figure or a different year. No contradiction has been established.', 'sw': 'Hakuna rekodi iliyokaguliwa inayolingana na mwaka huu wa fedha na hatua ya hati. Bajeti iliyoidhinishwa haiwezi kuthibitisha kiasi cha rasimu au mwaka mwingine. Hakuna upingano uliothibitishwa.'},
    'spending': {'en': 'Only an allocation is available for this scope. It cannot establish the claimed spending or contract value. The allocation below is context, not a comparison of like amounts.', 'sw': 'Mgao wa bajeti pekee unapatikana kwa wigo huu. Hauwezi kuthibitisha matumizi ya fedha au thamani ya mkataba inayodaiwa. Mgao hapa chini ni muktadha, si ulinganisho wa kiasi cha aina moja.'},
    'evidence': {'en': 'The required amount or citation is missing or invalid. No factual comparison can be made.', 'sw': 'Kiasi au rejeleo linalohitajika halipo au si sahihi. Ulinganisho wa ukweli hauwezi kufanywa.'},
    'conflict': {'en': 'Comparable reviewed observations disagree. All are shown below; no reviewed revision relationship resolves them. The claim cannot be settled from these sources.', 'sw': 'Rekodi zilizokaguliwa zinazolinganishwa zinatofautiana. Zote zinaonyeshwa hapa chini; hakuna uhusiano wa marekebisho uliokaguliwa unaotatua tofauti. Dai haliwezi kuamuliwa kwa vyanzo hivi.'},
    'match': {'en': 'The claimed allocation matches the reviewed amount for this project, ward, financial year, and document stage. This supports the allocation claim only.', 'sw': 'Mgao unaodaiwa unalingana na kiasi kilichokaguliwa kwa mradi, wadi, mwaka wa fedha na hatua ya hati. Hii inaunga mkono dai la mgao pekee.'},
    'partial': {'en': 'The allocation matches. The additional spending or completion claim has no supporting observation in this dataset and remains unverified.', 'sw': 'Mgao unalingana. Dai la ziada la matumizi ya fedha au kukamilika kwa kazi halina rekodi inayoliunga mkono katika data hizi na bado halijathibitishwa.'},
    'different': {'en': 'The claimed allocation differs from the directly comparable reviewed amount shown below. Any additional spending or completion claim remains unverified. This conclusion is limited to the cited source.', 'sw': 'Mgao unaodaiwa unatofautiana na kiasi kilichokaguliwa kinacholinganishwa moja kwa moja hapa chini. Dai lolote la ziada la matumizi ya fedha au kukamilika kwa kazi bado halijathibitishwa. Hitimisho hili linahusu chanzo kilichotajwa pekee.'},
}

# The order is deliberate: a remaining word cannot silently become a fact.
CLAIM = re.compile(
    r'(?:verify|check|hakiki)\s+(?P<project>.+?)\s+(?:in|katika)\s+(?P<ward>.+?)\s+'
    r'(?:fy|mwaka wa fedha)\s+(?P<year>20[0-9]{2}\s*[/–-]\s*(?:20[0-9]{2}|[0-9]{2}))\s+'
    r'(?P<stage>approved|draft|iliyoidhinishwa|rasimu)\s+'
    r'(?P<kind>allocation|allocated|spending|spent|contract value|mgao(?: wa bajeti)?|imetengwa|matumizi|zimetumika|thamani ya mkataba)\s+'
    r'(?:ksh|kes)\s+(?P<amount>[0-9](?:[0-9,.]*[0-9])?)(?:\s+(?P<unit>million|billion|milioni|bilioni))?'
    r'(?:\s+(?P<extra>and completed|and spent|na umekamilika|na zimetumika))?[?!.]?', re.I,
)
NUMBER = re.compile(r'(?:[0-9]+|[1-9][0-9]{0,2}(?:,[0-9]{3})+)(?:\.[0-9]+)?')


def parse_amount(value: str, unit: str | None) -> int | None:
    if len(value) > 24 or not NUMBER.fullmatch(value):
        return None
    try:
        amount = Decimal(value.replace(',', ''))
        multiplier = {'million': 10**6, 'milioni': 10**6, 'billion': 10**9, 'bilioni': 10**9}.get(unit, 1)
        cents = amount * multiplier * 100
        if not cents.is_finite() or cents != cents.to_integral_value() or not 0 <= cents <= 10**17:
            return None
        return int(cents)
    except InvalidOperation:
        return None


def verify_claim(text: str, records: list[dict]) -> dict:
    def result(reason, claim=None, projects=None, verdict='INSUFFICIENT_EVIDENCE', compared=None):
        return {'verdict': verdict, 'reason': reason, 'claim': claim,
                'projects': projects or [], 'compared_observation_ids': compared or []}

    match = CLAIM.fullmatch(normalize(text))
    if not match:
        return result('format')
    parts = match.groupdict()
    minor = parse_amount(parts['amount'], parts['unit'])
    if minor is None:
        return result('amount')
    start, end = re.split(r'\s*[/–-]\s*', parts['year'])
    end = end if len(end) == 4 else start[:2] + end
    if int(end) != int(start) + 1:
        return result('year')
    stage = 'APPROVED' if parts['stage'] in {'approved', 'iliyoidhinishwa'} else 'DRAFT'
    kind = ('ALLOCATION' if parts['kind'] in {'allocation', 'allocated', 'mgao', 'mgao wa bajeti', 'imetengwa'}
            else 'CONTRACT_VALUE' if parts['kind'] in {'contract value', 'thamani ya mkataba'} else 'EXPENDITURE')
    extra = ('completion' if parts['extra'] in {'and completed', 'na umekamilika'} else 'spending') if parts['extra'] else None
    claim = {'project_name': parts['project'], 'ward': parts['ward'], 'financial_year': f'{start}/{end}',
             'approval_stage': stage, 'amount_kind': kind, 'amount_kes': f'{Decimal(minor) / 100:.2f}',
             'formatted_amount': format_kes(minor), 'additional_claim': extra}
    projects = [p for p in records if normalize(p['name']) == parts['project'] and normalize(p['ward']) == parts['ward']]
    if len(projects) != 1:
        return result('identity', claim)
    project = deepcopy(projects[0])
    claim['project_name'], claim['ward'] = project['name'], project['ward']
    observations = [o for o in project['observations'] if o['financial_year'] == claim['financial_year'] and o['approval_stage'] == stage and o['amount_kind'] == 'ALLOCATION']
    if not observations:
        return result('scope', claim)
    project['observations'] = observations
    # Seed review gates validate provenance; this boundary also refuses incomplete
    # evidence instead of inventing zero or omitting a citation.
    for obs in observations:
        citation = obs.get('citation', {})
        amount = obs.get('amount_kes')
        if (not isinstance(amount, str) or parse_amount(amount, None) is None
                or not all(citation.get(key) for key in ['document_title', 'url', 'pdf_page', 'excerpt'])):
            return result('evidence', claim)
    if kind != 'ALLOCATION':
        return result('spending', claim, [project])
    amounts = {parse_amount(o['amount_kes'], None) for o in observations}
    ids = [o['id'] for o in observations]
    if len(amounts) != 1:
        return result('conflict', claim, [project], compared=ids)
    if minor not in amounts:
        return result('different', claim, [project], 'CONTRADICTED_BY_AVAILABLE_SOURCE', ids)
    if extra:
        return result('partial', claim, [project], 'PARTIALLY_SUPPORTED', ids)
    return result('match', claim, [project], 'SUPPORTED', ids)


def verification_message(result: dict, language: str) -> str:
    text = VERDICT_LABELS[result['verdict']][language] + '.\n' + REASONS[result['reason']][language]
    claim = result['claim']
    if claim:
        kinds = {'ALLOCATION': ('allocation', 'mgao'), 'EXPENDITURE': ('spending', 'matumizi'), 'CONTRACT_VALUE': ('contract value', 'thamani ya mkataba')}
        stage = ('approved' if claim['approval_stage'] == 'APPROVED' else 'draft') if language == 'en' else ('iliyoidhinishwa' if claim['approval_stage'] == 'APPROVED' else 'rasimu')
        # Identity is already shown in the cited project card when evidence exists.
        identity = '' if result['projects'] else f"{claim['project_name']} | {claim['ward']} | "
        text += '\n' + ('Claim: ' if language == 'en' else 'Dai: ') + identity + f"{claim['financial_year']} | {stage} | {kinds[claim['amount_kind']][language == 'sw']} {claim['formatted_amount']}"
        if claim['additional_claim']:
            text += ' + ' + ({'completion': 'completion', 'spending': 'spending'}[claim['additional_claim']] if language == 'en' else {'completion': 'kukamilika', 'spending': 'matumizi'}[claim['additional_claim']])
    return text
