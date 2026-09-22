# Milestone 2 wording review

Status: **Approved September 15, 2026.** Review covers the glossary, allocation caution, and browser/WhatsApp wording in English and Kiswahili.

The wording review required by the implementation plan is complete. Draft notices have been removed. No AI provider is configured or required: the same fixed templates work offline with the local source records.

M4 data update, September 16: after approval of five additional source records, the coverage count changed from ten to fifteen (`kumi na tano`) in both languages. Definitions and allocation cautions are unchanged.

## Review-date and follow-up wording

Status: **Approved September 21, 2026.** Manual wording review and live WhatsApp checks passed for these additions. Automated checks cover language switching and preservation of evidence. The September 15 approval applies to the earlier wording.

| English | Kiswahili |
| --- | --- |
| Record reviewed: {date} | Rekodi ilikaguliwa: {date} |
| Review dates describe checks of budget records, not current project progress. | Tarehe za ukaguzi zinahusu rekodi za bajeti, si maendeleo ya sasa ya mradi. |
| Next step: When asking for a project update, cite the project name, ward, financial year, allocation and source page shown. Ask for spending or completion evidence; this budget record alone cannot establish either. | Hatua inayofuata: Unapoulizia maendeleo ya mradi, taja jina la mradi, wadi, mwaka wa fedha, mgao na ukurasa wa chanzo ulioonyeshwa. Omba ushahidi wa matumizi ya fedha au kukamilika kwa kazi; rekodi hii ya bajeti pekee haithibitishi hayo. |

Dates come from individual observations: September 14 for the initial ten records and September 16 for the five additions. They are neither the document's publication date nor an assessment of current implementation. Follow-up guidance appears only with a project's details, explanation, or verification evidence; it does not claim to send a request or identify a verified contact.

## Reviewed definitions

Check that the English wording reflects the linked evidence, the Kiswahili is natural and accurate, and neither language implies that an allocation proves payment or completion. Project names, departments, original source excerpts, document titles, exact amounts, financial years, and source pages stay unchanged.

| Term | English | Kiswahili | Reference |
| --- | --- | --- | --- |
| allocation | A budget allocation is an amount set aside in a budget for a stated purpose. It does not show that cash was released, spent, or that work was completed. | Mgao wa bajeti ni kiasi kilichotengwa katika bajeti kwa kusudi lililotajwa. Hauonyeshi kwamba fedha zilitolewa, zilitumika, au kazi ilikamilika. | [Nyeri County Approved Budget Estimates 2026/2027 — Programme Based Budget, PDF page 278](https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf#page=278). Pilot interpretation of the approved allocation columns; not a spending record. |
| recurrent expenditure | Recurrent expenditure covers the costs of running government services. This general definition does not show spending on any particular project. | Matumizi ya kawaida ni gharama za kuendesha huduma za serikali. Maana hii ya jumla haionyeshi matumizi ya fedha kwa mradi wowote mahsusi. | [National Treasury — Standard Chart of Accounts Manual, March 2026, PDF page 36](https://www.treasury.go.ke/sites/default/files/Latest%20updates/SCOA%20Mar%202026.pdf#page=36). Section 6.4; printed page 35. General terminology, not project evidence. |
| development expenditure | Development expenditure covers creating or renewing assets. A budget entry in this category does not prove that the asset has been built or renewed. | Matumizi ya maendeleo ni gharama za kuunda au kukarabati mali. Rekodi ya bajeti katika kundi hili haithibitishi kwamba mali imejengwa au kukarabatiwa. | [National Treasury — Standard Chart of Accounts Manual, March 2026, PDF page 36](https://www.treasury.go.ke/sites/default/files/Latest%20updates/SCOA%20Mar%202026.pdf#page=36). Section 6.4; printed page 35. General terminology, not project evidence. |

The Treasury manual is a glossary reference only. It supplies no project observations and does not expand the reviewed dataset for milestone 4.

## Project explanation and caution

English template: The approved budget sets aside {amount} for {project name} in {ward} Ward for FY {year}.

Kiswahili template: Bajeti iliyoidhinishwa imetenga {amount} kwa {project name} katika Wadi ya {ward}, mwaka wa fedha {year}.

English caution: This is a budget allocation, not proof that money was spent or work completed.

Kiswahili caution: Huu ni mgao wa bajeti, si uthibitisho kwamba fedha zilitumika au kazi ilikamilika.

Both versions display the same project card and its official citation. Explanations never use an unselected or unmatched project. General definitions do not imply any project's implementation status.

## Commands and practical review

1. In the browser, search Wamagana, select SW, and check that the three project cards retain their names, amounts, year, and page 278. Use “Eleza mradi huu”.
2. In WhatsApp, send `Wamagana`, `SW`, `1`, `ELEZA`, `ZAIDI`, `MSAADA`, then `EN`. Switching language repeats the current reply without advancing pagination.
3. Try `Eleza mgao wa bajeti`, `Matumizi ya kawaida ni nini?`, and `Eleza matumizi ya maendeleo`.
4. Try `Miradi ya maji katika Kabaru`, `Miradi katika Nairobi`, and `Kianjogu Karaihu umekamilika?`. The reply must state missing coverage or insufficient evidence.
5. Review [interface wording](../frontend/translations.js) and [WhatsApp labels](../src/api/whatsapp.py). Names and original evidence remain in their source language intentionally.

Only the fixed phrases and simple query patterns are supported. This is not unrestricted machine translation. `EN` and `SW` set an anonymous session preference that expires after inactivity; there is no cross-language identity tracking or account profile.

## Conversation wording

| English | Kiswahili |
| --- | --- |
| Your conversation has expired. Select your ward or send your question again. | Muda wa mazungumzo umeisha. Chagua wadi yako au tuma swali tena. |
| The pilot covers fifteen reviewed allocation records in Wamagana, Mweiga, and Kabaru for FY 2026/2027. Only the programme budget supplies project answers; the second document is registered for later review. | Jaribio linahusu rekodi kumi na tano za mgao wa bajeti zilizokaguliwa katika Wamagana, Mweiga na Kabaru kwa mwaka wa fedha 2026/2027. Majibu ya miradi yanatoka kwenye bajeti ya programu pekee; hati ya pili imesajiliwa kwa mapitio ya baadaye. |
| Choose a ward to start a project search. | Chagua wadi ili kuanza kutafuta miradi. |
| You have reached the end of the matching records in our selected documents. | Umefika mwisho wa rekodi zinazolingana katika hati tulizochagua. |
| Select a project from your current results, or search by ward again. | Chagua mradi kutoka kwenye matokeo ya sasa, au tafuta kwa wadi tena. |
| Here is the reviewed project record and its source. | Hii ndiyo rekodi ya mradi iliyokaguliwa pamoja na chanzo chake. |
| Not enough evidence to establish spending or completion. This pilot contains budget allocations only. | Hakuna ushahidi wa kutosha kuthibitisha matumizi ya fedha au kukamilika kwa kazi. Jaribio hili lina mgao wa bajeti pekee. |
| Claim verification is not available in this first milestone. You can inspect an allocation and its official source by asking for projects in a covered ward. | Uhakiki wa madai bado haupatikani. Unaweza kuona mgao wa bajeti na chanzo rasmi kwa kuuliza kuhusu miradi katika wadi zinazohusika. |
| Please ask about one financial year at a time. Current coverage is FY 2026/2027. | Uliza kuhusu mwaka mmoja wa fedha kwa wakati mmoja. Rekodi zetu ni za mwaka wa fedha 2026/2027. |
| Please specify the financial year, such as 2026/2027. A calendar year alone can span two financial years. | Taja mwaka wa fedha, kama 2026/2027. Mwaka wa kalenda unaweza kuhusisha miaka miwili ya fedha. |
| I could not resolve that location within our pilot. Please choose Wamagana, Mweiga, or Kabaru in Nyeri County. Other places are outside current coverage. | Eneo hilo halijapatikana katika jaribio hili. Chagua Wamagana, Mweiga au Kabaru katika Kaunti ya Nyeri. Maeneo mengine yako nje ya rekodi zetu. |
| Please choose one ward for this search. | Chagua wadi moja kwa utafutaji huu. |
| Here is the allocation recorded in the approved FY 2026/2027 budget. | Huu ndio mgao uliorekodiwa katika bajeti iliyoidhinishwa ya mwaka wa fedha 2026/2027. |
| That description appears in more than one ward. Which ward do you mean? | Maelezo hayo yanapatikana katika zaidi ya wadi moja. Unamaanisha wadi gani? |
| I could not identify an exact project from that question. Search by ward and select a project to inspect its recorded allocation. | Sikuweza kutambua mradi mahsusi katika swali hilo. Tafuta kwa wadi na uchague mradi ili kuona mgao wake uliorekodiwa. |
| Which ward in Nyeri County should I search? We cover selected records in Wamagana, Mweiga, and Kabaru only. An area outside this list is outside our current coverage. | Nitafute katika wadi gani ya Kaunti ya Nyeri? Tuna rekodi zilizochaguliwa katika Wamagana, Mweiga na Kabaru pekee. Maeneo mengine yako nje ya rekodi zetu. |
| Try a question such as 'What projects are planned in Wamagana?' This version supports project discovery. | Jaribu swali kama 'Ni miradi gani imepangwa Wamagana?' Unaweza kutafuta miradi au kuuliza maana ya istilahi ya bajeti. |
| Choose a budget term: allocation, recurrent expenditure, or development expenditure. Or select a project and send EXPLAIN. | Chagua istilahi: mgao wa bajeti, matumizi ya kawaida, au matumizi ya maendeleo. Au chagua mradi na utume ELEZA. |
| Select a project first, then send EXPLAIN. | Chagua mradi kwanza, kisha tuma ELEZA. |
| That term is not in our glossary. Try allocation, recurrent expenditure, or development expenditure. | Istilahi hiyo haipo katika kamusi yetu. Jaribu mgao wa bajeti, matumizi ya kawaida, au matumizi ya maendeleo. |
| English selected. Your current results are preserved. | Kiswahili kimechaguliwa. Matokeo yako ya sasa yamehifadhiwa. |
| Only English and Kiswahili are supported. Send EN or SW. | Kiingereza na Kiswahili pekee vinapatikana. Tuma EN au SW. |

Dynamic result messages preserve the ward, year, and result counts:

- Hakuna rekodi zilizokaguliwa za mwaka wa fedha {0} katika rekodi zetu. Tuna mwaka wa fedha 2026/2027 pekee. Hii haimaanishi kwamba hakuna miradi.
- Hakuna rekodi zilizokaguliwa zinazolingana za {0} kwa mwaka wa fedha 2026/2027 katika hati tulizochagua. Hii haimaanishi kwamba hakuna miradi.
- Rekodi {0}–{1} kati ya {2} zinazolingana za {3} katika bajeti iliyoidhinishwa ya mwaka wa fedha 2026/2027.

## Review record

- Review method: manual wording review
- Review date: September 15, 2026
- English definitions: approved
- Kiswahili meanings, cautions, and interface/WhatsApp wording: approved
- Manual live bilingual WhatsApp checks: passed September 15, 2026

The manual live sequence covered Kiswahili discovery, selection, explanation, pagination, and help. `ELEZA` before project selection correctly requests a selection. Names, allocation amounts, financial years, and source pages remain unchanged. Browser and signed webhook integration checks pass. Milestone 2 is complete.
