# Milestone 3 verification review

Status: **Wording approved September 16, 2026.** Manual WhatsApp checks identified a reply-language issue: a `Hakiki` claim received English in an English session. The correction and validation are recorded below.

## Supported claim format

English: `Verify Kianjogu Karaihu in Wamagana FY 2026/2027 approved allocation KSh 3,000,000`

Kiswahili: `Hakiki Kianjogu Karaihu katika Wamagana mwaka wa fedha 2026/2027 iliyoidhinishwa mgao KSh 3,000,000`

Use an exact source project name, its ward, one financial year, document stage, amount type, and one exact KSh/KES amount. A short year such as 2026/27 is normalized. English `million`/`billion` and Kiswahili `milioni`/`bilioni` are supported after the number. Decimal money is compared exactly; invalid grouping and fractions of a cent are rejected.

`approved` / `iliyoidhinishwa` and `draft` / `rasimu` are separate scopes. Current reviewed observations are approved allocations only. Use `spending` / `matumizi` or `contract value` / `thamani ya mkataba` to see that those types lack comparable evidence.

An allocation claim may append `and completed` / `na umekamilika` or `and spent` / `na zimetumika`. These clauses are not established by the allocation data. Other clauses, multiple amounts, missing scope, and unfamiliar wording prompt the user to resend one complete claim. No scope is silently inherited from a previous query. This bounded grammar deliberately does not attempt unrestricted natural-language fact checking.

## Approved verdict wording

| Verdict | English | Kiswahili |
| --- | --- | --- |
| `SUPPORTED` | Supported by the available source | Linaungwa mkono na chanzo kilichopo |
| `PARTIALLY_SUPPORTED` | Partially supported | Linaungwa mkono kwa sehemu |
| `INSUFFICIENT_EVIDENCE` | Insufficient evidence | Ushahidi hautoshi |
| `CONTRADICTED_BY_AVAILABLE_SOURCE` | Contradicted by the available source | Linapingwa na chanzo kilichopo |

## Reasons shown to residents

| Situation | English | Kiswahili |
| --- | --- | --- |
| format | Send one complete claim in this format: Verify Kianjogu Karaihu in Wamagana FY 2026/2027 approved allocation KSh 3,000,000. Use the source project name. You may append "and completed" or "and spent"; other clauses require a separate check. | Tuma dai moja kamili kwa muundo huu: Hakiki Kianjogu Karaihu katika Wamagana mwaka wa fedha 2026/2027 iliyoidhinishwa mgao KSh 3,000,000. Tumia jina la mradi katika chanzo. Unaweza kuongeza "na umekamilika" au "na zimetumika"; vifungu vingine vinahitaji uhakiki tofauti. |
| amount | Use one exact non-negative KSh amount, with valid comma grouping and whole cents. Ranges, estimates, and multiple amounts cannot be compared. | Tumia kiasi kimoja halisi cha KSh kisicho hasi, chenye koma sahihi na senti kamili. Masafa, makadirio na kiasi zaidi ya kimoja haviwezi kulinganishwa. |
| year | Specify one financial year, such as 2026/2027. Multi-year totals cannot be compared with a single-year allocation. | Taja mwaka mmoja wa fedha, kama 2026/2027. Jumla ya miaka mingi haiwezi kulinganishwa na mgao wa mwaka mmoja. |
| identity | The exact project and ward did not resolve to one reviewed record. Check the source name and ward, then resend the full claim. Missing coverage does not mean no project exists. | Jina halisi la mradi na wadi havikutoa rekodi moja iliyokaguliwa. Angalia jina na wadi katika chanzo, kisha tuma dai lote tena. Kukosekana kwa rekodi hakumaanishi kwamba mradi haupo. |
| scope | No reviewed observation matches this financial year and document stage. An approved budget cannot establish a draft figure or a different year. No contradiction has been established. | Hakuna rekodi iliyokaguliwa inayolingana na mwaka huu wa fedha na hatua ya hati. Bajeti iliyoidhinishwa haiwezi kuthibitisha kiasi cha rasimu au mwaka mwingine. Hakuna upingano uliothibitishwa. |
| spending | Only an allocation is available for this scope. It cannot establish the claimed spending or contract value. The allocation below is context, not a comparison of like amounts. | Mgao wa bajeti pekee unapatikana kwa wigo huu. Hauwezi kuthibitisha matumizi ya fedha au thamani ya mkataba inayodaiwa. Mgao hapa chini ni muktadha, si ulinganisho wa kiasi cha aina moja. |
| evidence | The required amount or citation is missing or invalid. No factual comparison can be made. | Kiasi au rejeleo linalohitajika halipo au si sahihi. Ulinganisho wa ukweli hauwezi kufanywa. |
| conflict | Comparable reviewed observations disagree. All are shown below; no reviewed revision relationship resolves them. The claim cannot be settled from these sources. | Rekodi zilizokaguliwa zinazolinganishwa zinatofautiana. Zote zinaonyeshwa hapa chini; hakuna uhusiano wa marekebisho uliokaguliwa unaotatua tofauti. Dai haliwezi kuamuliwa kwa vyanzo hivi. |
| match | The claimed allocation matches the reviewed amount for this project, ward, financial year, and document stage. This supports the allocation claim only. | Mgao unaodaiwa unalingana na kiasi kilichokaguliwa kwa mradi, wadi, mwaka wa fedha na hatua ya hati. Hii inaunga mkono dai la mgao pekee. |
| partial | The allocation matches. The additional spending or completion claim has no supporting observation in this dataset and remains unverified. | Mgao unalingana. Dai la ziada la matumizi ya fedha au kukamilika kwa kazi halina rekodi inayoliunga mkono katika data hizi na bado halijathibitishwa. |
| different | The claimed allocation differs from the directly comparable reviewed amount shown below. Any additional spending or completion claim remains unverified. This conclusion is limited to the cited source. | Mgao unaodaiwa unatofautiana na kiasi kilichokaguliwa kinacholinganishwa moja kwa moja hapa chini. Dai lolote la ziada la matumizi ya fedha au kukamilika kwa kazi bado halijathibitishwa. Hitimisho hili linahusu chanzo kilichotajwa pekee. |

The claim summary retains the exact amount, year, stage, and amount type. Evidence cards retain original project names, departments, excerpts, titles, and citations. The existing reviewed allocation caution remains visible. The browser's example button adds the label “Compare an allocation” / “Linganisha mgao”.

## Live examples

Send each full message separately:

1. `Verify Kianjogu Karaihu in Wamagana FY 2026/2027 approved allocation KSh 3 million` — supported; the source records KSh 3,000,000 on PDF page 291.
2. Same message with `2 million` — contradicted by the available source, showing both claimed and recorded amounts.
3. Same message with `3 million and completed` — partially supported; the allocation matches but completion remains unverified.
4. Same message using `approved spending KSh 3 million` — insufficient evidence; an allocation cannot establish spending.
5. Same message with `FY 2025/2026` or `draft allocation` — insufficient evidence; no comparison across years or document stages.
6. Send `SW`, then `EN` — the current claim, verdict, and citations remain identical while wording switches.

The test suite also injects conflicting synthetic observations in isolated tests. The verifier returns insufficient evidence and displays both sources. Synthetic data are not imported into the demo dataset. A direct contradiction takes precedence over partial support; missing records alone never establish contradiction.

## Review and completion record

- Review method: manual wording review
- Wording approval date: September 16, 2026
- Manual live WhatsApp verification checks: supported, contradicted, and partially supported verdicts passed; corrected direct-Hakiki language selection passed on September 16 for supported and contradicted replies
- Automated checks: 113 cases validated across the full-suite and targeted runs; all 67 final verification/WhatsApp checks passed
- Browser checks: passed at 1280px, 390px, and 320px (verdicts, language switching, citations, safe text rendering, and layout)

Wording approval is recorded and draft notices are removed. A message beginning with `Hakiki` now selects Kiswahili directly, even in an English session; `EN` still switches back explicitly. Regression checks cover the browser/API and signed WhatsApp path. All 85 targeted verification, WhatsApp, and language tests passed after this correction. The manual live retry passed: Kiswahili supported and contradicted verdicts retain the claimed amount, the KSh 3,000,000 source allocation, and PDF page 291. Milestone 3 is complete.
