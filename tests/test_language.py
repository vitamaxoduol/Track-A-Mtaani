from uuid import UUID

import pytest

from src.api.whatsapp import format_whatsapp
from src.models.evidence import ChatRequest
from src.services.explainer import GLOSSARY
from src.services.projects import search_projects
from src.services.translator import ALLOCATION_SW


def ask(client, message='', **kwargs):
    response = client.post('/api/v1/chat', json={'message': message, **kwargs})
    assert response.status_code == 200, response.text
    return response.json()


def test_switch_repeats_same_evidence_without_advancing_page(client):
    first = ask(client, 'Wamagana')
    key = first['session_id']
    sw = ask(client, 'SW', session_id=key)
    assert sw['projects'] == first['projects']
    assert sw['language'] == 'sw' and 'Rekodi 1–3' in sw['message']
    assert sw['disclaimer'] == ALLOCATION_SW
    assert sw['review_notice'] is None
    assert ask(client, 'Mweiga')['language'] == 'en'
    second = ask(client, 'ZAIDI', session_id=key)
    assert second['language'] == 'sw' and '4–6' in second['message']
    detail = ask(client, '1', session_id=key)
    assert detail['projects'] == second['projects'][:1]
    en = ask(client, action='language', language='en', session_id=key)
    assert en['projects'] == detail['projects'] and en['language'] == 'en'
    assert en['review_notice'] is None


def test_coverage_reports_expanded_count_in_both_languages(client):
    en = ask(client, 'HELP')
    sw = ask(client, 'SW', session_id=en['session_id'])
    assert en['coverage']['record_count'] == sw['coverage']['record_count'] == 15
    assert 'fifteen reviewed' in en['message']
    assert 'kumi na tano' in sw['message']
    assert sum(s['used_for_answers'] for s in en['coverage']['sources']) == 1


def test_explanation_uses_same_selected_record_and_survives_switch(client):
    first = ask(client, 'Wamagana')
    key, project = first['session_id'], first['projects'][0]
    en = ask(client, action='explain', project_id=project['id'], session_id=key)
    sw = ask(client, 'SW', session_id=key)
    for result in [en, sw]:
        assert result['kind'] == 'explanation'
        assert result['projects'] == [project]
        assert project['name'] in result['message']
        assert project['observations'][0]['formatted_amount'] in result['message']
        assert '2026/2027' in result['message']
        assert result['review_notice'] is None
    assert 'not proof' in en['message'] and 'si uthibitisho' in sw['message']
    assert ask(client, 'MORE', session_id=key)['kind'] == 'results'


def test_explanation_never_inherits_unknown_scope_or_arbitrary_amounts(client):
    key = ask(client, 'Wamagana')['session_id']
    for text in ['Explain Kianjogu Karaihu in Nairobi', 'Eleza Kianjogu Karaihu katika Nairobi',
                 'Explain Kianjogu Karaihu 2025/2026', 'Explain a fictional project',
                 'Explain KSh 9 million for Wamagana', 'Eleza Kianjogu Karaihu imekamilika']:
        result = ask(client, text, session_id=key)
        assert not result['projects']
        assert ask(client, 'EXPLAIN', session_id=key)['kind'] == 'clarification'
    other = ask(client, 'Mweiga')
    assert ask(client, action='explain', project_id='nyeri-2026-001', session_id=other['session_id'])['kind'] == 'clarification'


@pytest.mark.parametrize('en,sw,kind', [
    ('Show road projects in Mweiga', 'Onyesha miradi ya barabara katika Mweiga', 'results'),
    ('Water projects in Mweiga', 'Miradi ya maji katika Mweiga', 'results'),
    ('Water projects in Kabaru', 'Miradi ya maji katika Kabaru', 'empty'),
    ('Projects in Nairobi near Wamagana', 'Miradi katika Nairobi karibu na Wamagana', 'clarification'),
    ('Wamagana 2025/26', 'Wamagana 2025/26', 'empty'),
    ('Wamagana 2026', 'Wamagana 2026', 'clarification'),
    ('Was Kianjogu Karaihu completed?', 'Kianjogu Karaihu umekamilika?', 'unavailable'),
    ('Verify Wamagana KSh 9000000', 'Hakiki Wamagana KSh 9000000', 'verification'),
])
def test_bilingual_queries_have_same_scope(client, en, sw, kind):
    a, b = ask(client, en), ask(client, sw, language='sw')
    assert a['kind'] == b['kind'] == kind
    assert a['projects'] == b['projects']
    assert a['message'] != b['message']


@pytest.mark.parametrize('term', list(GLOSSARY))
def test_glossary_is_cited_general_and_available_without_ai(client, term, monkeypatch):
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    a = ask(client, 'Explain ' + term)
    b = ask(client, 'SW', session_id=a['session_id'])
    assert a['kind'] == b['kind'] == 'explanation'
    assert not a['projects'] and not b['projects']
    assert a['explanation_sources'] == b['explanation_sources']
    assert a['explanation_sources'][0]['pdf_page'] > 0
    assert a['message'] == GLOSSARY[term]['en'] and b['message'] == GLOSSARY[term]['sw']


def test_expired_language_context_and_unsupported_language(client):
    first = ask(client, 'Wamagana', language='sw')
    service = client.app.state.conversation
    service.sessions[first['session_id']].updated -= 1801
    result = ask(client, action='explain', project_id=first['projects'][0]['id'], session_id=first['session_id'], language='sw')
    assert result['kind'] == 'expired' and 'Muda' in result['message'] and not result['projects']
    assert 'Only English' in ask(client, 'translate to french')['message']
    assert client.post('/api/v1/chat', json={'action':'language'}).status_code == 422


def test_all_pilot_whatsapp_explanations_details_and_pages_fit_limit(client):
    service = client.app.state.conversation
    for language in ['en', 'sw']:
        for ward in service.coverage['wards']:
            result = service.reply(ChatRequest(message=ward, language=language))
            assert len(format_whatsapp(result, first_use=True)) <= 1600
            key = UUID(result.session_id)
            while result.has_more:
                result = service.reply(ChatRequest(action='more', session_id=key))
                assert len(format_whatsapp(result)) <= 1600
        for project in search_projects(service.db_path):
            result = service.reply(ChatRequest(message=project['ward'], language=language))
            key = UUID(result.session_id)
            while project['id'] not in [p['id'] for p in result.projects]:
                assert result.has_more
                result = service.reply(ChatRequest(action='more', session_id=key))
            for action in ['details','explain']:
                result = service.reply(ChatRequest(action=action, project_id=project['id'], session_id=key))
                assert result.projects == [project]
                assert len(format_whatsapp(result, first_use=True)) <= 1600
        for message in ['HELP', 'EXPLAIN allocation', 'EXPLAIN recurrent expenditure', 'EXPLAIN development expenditure']:
            result = service.reply(ChatRequest(message=message, language=language))
            assert len(format_whatsapp(result, first_use=True)) <= 1600
