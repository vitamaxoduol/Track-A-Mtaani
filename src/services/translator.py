"""Fixed interface translations; never translate or rewrite evidence fields.

Core wording reviewed on 2026-09-15; additions tracked in docs/language-review.md.
"""
import re

ALLOCATION_SW = 'Huu ni mgao wa bajeti, si uthibitisho kwamba fedha zilitumika au kazi ilikamilika.'

# Record-check dates are provenance, not evidence of current implementation.
REVIEW_CONTEXT = {
    'en': 'Review dates describe checks of budget records, not current project progress.',
    'sw': 'Tarehe za ukaguzi zinahusu rekodi za bajeti, si maendeleo ya sasa ya mradi.',
}
NEXT_STEPS = {
    'en': 'Next step: When asking for a project update, cite the project name, ward, financial year, allocation and source page shown. Ask for spending or completion evidence; this budget record alone cannot establish either.',
    'sw': 'Hatua inayofuata: Unapoulizia maendeleo ya mradi, taja jina la mradi, wadi, mwaka wa fedha, mgao na ukurasa wa chanzo ulioonyeshwa. Omba ushahidi wa matumizi ya fedha au kukamilika kwa kazi; rekodi hii ya bajeti pekee haithibitishi hayo.',
}

# English templates are the keys so every translated response has a fixed source.
MESSAGES = {
    'Your conversation has expired. Select your ward or send your question again.': 'Muda wa mazungumzo umeisha. Chagua wadi yako au tuma swali tena.',
    'The pilot covers fifteen reviewed allocation records in Wamagana, Mweiga, and Kabaru for FY 2026/2027. Only the programme budget supplies project answers; the second document is registered for later review.': 'Jaribio linahusu rekodi kumi na tano za mgao wa bajeti zilizokaguliwa katika Wamagana, Mweiga na Kabaru kwa mwaka wa fedha 2026/2027. Majibu ya miradi yanatoka kwenye bajeti ya programu pekee; hati ya pili imesajiliwa kwa mapitio ya baadaye.',
    'Choose a ward to start a project search.': 'Chagua wadi ili kuanza kutafuta miradi.',
    'You have reached the end of the matching records in our selected documents.': 'Umefika mwisho wa rekodi zinazolingana katika hati tulizochagua.',
    'Select a project from your current results, or search by ward again.': 'Chagua mradi kutoka kwenye matokeo ya sasa, au tafuta kwa wadi tena.',
    'Here is the reviewed project record and its source.': 'Hii ndiyo rekodi ya mradi iliyokaguliwa pamoja na chanzo chake.',
    'Not enough evidence to establish spending or completion. This pilot contains budget allocations only.': 'Hakuna ushahidi wa kutosha kuthibitisha matumizi ya fedha au kukamilika kwa kazi. Jaribio hili lina mgao wa bajeti pekee.',
    'Claim verification is not available in this first milestone. You can inspect an allocation and its official source by asking for projects in a covered ward.': 'Uhakiki wa madai bado haupatikani. Unaweza kuona mgao wa bajeti na chanzo rasmi kwa kuuliza kuhusu miradi katika wadi zinazohusika.',
    'Please ask about one financial year at a time. Current coverage is FY 2026/2027.': 'Uliza kuhusu mwaka mmoja wa fedha kwa wakati mmoja. Rekodi zetu ni za mwaka wa fedha 2026/2027.',
    'Please specify the financial year, such as 2026/2027. A calendar year alone can span two financial years.': 'Taja mwaka wa fedha, kama 2026/2027. Mwaka wa kalenda unaweza kuhusisha miaka miwili ya fedha.',
    'I could not resolve that location within our pilot. Please choose Wamagana, Mweiga, or Kabaru in Nyeri County. Other places are outside current coverage.': 'Eneo hilo halijapatikana katika jaribio hili. Chagua Wamagana, Mweiga au Kabaru katika Kaunti ya Nyeri. Maeneo mengine yako nje ya rekodi zetu.',
    'Please choose one ward for this search.': 'Chagua wadi moja kwa utafutaji huu.',
    'Here is the allocation recorded in the approved FY 2026/2027 budget.': 'Huu ndio mgao uliorekodiwa katika bajeti iliyoidhinishwa ya mwaka wa fedha 2026/2027.',
    'That description appears in more than one ward. Which ward do you mean?': 'Maelezo hayo yanapatikana katika zaidi ya wadi moja. Unamaanisha wadi gani?',
    'I could not identify an exact project from that question. Search by ward and select a project to inspect its recorded allocation.': 'Sikuweza kutambua mradi mahsusi katika swali hilo. Tafuta kwa wadi na uchague mradi ili kuona mgao wake uliorekodiwa.',
    'Which ward in Nyeri County should I search? We cover selected records in Wamagana, Mweiga, and Kabaru only. An area outside this list is outside our current coverage.': 'Nitafute katika wadi gani ya Kaunti ya Nyeri? Tuna rekodi zilizochaguliwa katika Wamagana, Mweiga na Kabaru pekee. Maeneo mengine yako nje ya rekodi zetu.',
    "Try a question such as 'What projects are planned in Wamagana?' This version supports project discovery.": "Jaribu swali kama 'Ni miradi gani imepangwa Wamagana?' Unaweza kutafuta miradi au kuuliza maana ya istilahi ya bajeti.",
    'Choose a budget term: allocation, recurrent expenditure, or development expenditure. Or select a project and send EXPLAIN.': 'Chagua istilahi: mgao wa bajeti, matumizi ya kawaida, au matumizi ya maendeleo. Au chagua mradi na utume ELEZA.',
    'Select a project first, then send EXPLAIN.': 'Chagua mradi kwanza, kisha tuma ELEZA.',
    'That term is not in our glossary. Try allocation, recurrent expenditure, or development expenditure.': 'Istilahi hiyo haipo katika kamusi yetu. Jaribu mgao wa bajeti, matumizi ya kawaida, au matumizi ya maendeleo.',
    'English selected. Your current results are preserved.': 'Kiswahili kimechaguliwa. Matokeo yako ya sasa yamehifadhiwa.',
    'Only English and Kiswahili are supported. Send EN or SW.': 'Kiingereza na Kiswahili pekee vinapatikana. Tuma EN au SW.',
}
DYNAMIC = [
    (r'There are no reviewed records for FY (.+) in our coverage\. We currently cover FY 2026/2027 only\. This does not mean no projects exist\.', 'Hakuna rekodi zilizokaguliwa za mwaka wa fedha {0} katika rekodi zetu. Tuna mwaka wa fedha 2026/2027 pekee. Hii haimaanishi kwamba hakuna miradi.'),
    (r'No matching reviewed records for (.+) in FY 2026/2027 were found in our selected documents\. This does not mean no projects exist\.', 'Hakuna rekodi zilizokaguliwa zinazolingana za {0} kwa mwaka wa fedha 2026/2027 katika hati tulizochagua. Hii haimaanishi kwamba hakuna miradi.'),
    (r'Showing (\d+)–(\d+) of (\d+) matching records for (.+) in the approved FY 2026/2027 budget\.', 'Rekodi {0}–{1} kati ya {2} zinazolingana za {3} katika bajeti iliyoidhinishwa ya mwaka wa fedha 2026/2027.'),
]


def translate(message: str, language: str) -> str:
    if language == 'en':
        return message
    if message in MESSAGES:
        return MESSAGES[message]
    for pattern, template in DYNAMIC:
        match = re.fullmatch(pattern, message)
        if match:
            return template.format(*match.groups())
    # Never attempt machine rewriting of an unfamiliar string.
    return message


def notice(language: str) -> str:
    from src.services.citations import ALLOCATION_NOTICE
    return ALLOCATION_SW if language == 'sw' else ALLOCATION_NOTICE
