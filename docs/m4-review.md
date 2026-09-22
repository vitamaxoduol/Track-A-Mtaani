# Milestone 4 review and delivery

Current branch: `main`, after merging `m4/demo-submission` in `a3f4056`; the initial POC commit is `49e01c5`. Checkpoint `0762d53` contains the reviewed fifteen-record pilot and was pushed to GitHub. M4 submission completed September 21, 2026; confirmation is retained. Subsequent checks are recorded under their actual dates below.

## Additional reviewed records

Manual source review completed September 16, 2026. These five records match the cited original documents. **Approved and imported:** the reviewed dataset now contains fifteen projects. Review-batch provenance is retained in [m4-candidates.json](../data/processed/m4-candidates.json).

All five are allocations in the approved FY 2026/2027 programme budget, in Kshs. with no multiplier. PDF and printed page numbers agree. Row numbers exclude the header. Rendered-page checks and manual approval completed September 16, 2026, following the [source-review process](data-sources.md#ingestion-and-review).


| Candidate | Description as printed    | Ward     | KES allocated | PDF page                                                                                           | Row |
| --------- | ------------------------- | -------- | ------------- | -------------------------------------------------------------------------------------------------- | --- |
| 011       | Kaiguri Gwa Karuga        | Wamagana | 1,000,000     | [291](https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf#page=291) | 7   |
| 012       | Kihuro rd                 | Wamagana | 2,000,000     | [292](https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf#page=292) | 1   |
| 013       | Kanyamati                 | Wamagana | 2,400,000     | [292](https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf#page=292) | 2   |
| 014       | Jambo Zaina Box Culvert   | Kabaru   | 4,000,000     | [296](https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf#page=296) | 1   |
| 015       | Supporting water projects | Mweiga   | 2,000,000     | [282](https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf#page=282) | 7   |


The first four use the source spending unit `Roads Headquarters`; candidate 015 uses `Water Headquarters`. Its description names no individual water scheme: retain that limitation. The source's `New` label is not evidence of construction or completion.

The import preserves the original ten IDs and appends records 011–015. Both languages now report fifteen records. The water filter matches `Water Headquarters`, preserving the original source spending unit. Wamagana has nine reviewed records, Mweiga three, and Kabaru three.

## Approved source coverage

The [source-scope adjustment](source-scope-decision.md), approved September 16, 2026, requires 15–30 reviewed projects from at least one official project-level document, with additional documents explicitly registered as answer sources or context only.

The fifteen reviewed projects satisfy the adjusted dataset condition. This replaces the original two-or-three-project-source target; it does not establish independent corroboration or imply that the context document supplies answers. Submission delivery checks are complete in the [submission checklist](implementation-plan.md#submission-checklist).

The retained [itemized estimates](../data/raw/nyeri-approved-estimates-2026-27.pdf) do not provide a clean second set of ward records in the inspected entries. PDF page 48 combines office repairs across several towns. PDF page 52 names Wamagana Hospital but supplies no ward field; the programme budget labels that allocation Countywide. PDF page 66 combines livestock infrastructure items. Do not infer wards from names or attribute grouped amounts to one project.

The county's [approved Mwananchi budget](https://www.nyeri.go.ke/wp-content/uploads/2026/07/MWANANCHI_BUDGET_FY_2026-27.pdf), found through the [official index](https://www.nyeri.go.ke/bud/) on September 16, summarizes Wamagana Hospital as KSh 26.2 million, whereas the itemized budget reports KSh 26,239,730. A rounded summary is not a conflicting exact amount. It has not been imported or counted as independent project evidence. An annual development plan's estimated costs must likewise not be relabeled as approved budget allocations merely to reach the document target.

## Validation and completed delivery checks

Baseline on September 16: **116 automated tests passed**, with two upstream deprecation warnings and no failures. This run used the original ten-record seed, not the candidates. Earlier manual live WhatsApp checks are recorded in the implementation plan.

Expanded-dataset validation on September 16: **124 automated tests pass**, including exact source citations, water filtering, third-page pagination, bilingual verification for all five additions, and WhatsApp detail/explanation/coverage length checks for all fifteen records. Desktop, 390px, and 320px Chromium checks pass for the expanded coverage, third page, Kiswahili, water explanation, and the Jambo Zaina claim. Expanded manual live WhatsApp checks passed September 20, 2026 using the fifteen-record pilot and [demo checklist](demo-runbook.md#expanded-live-whatsapp-check). This is a manual acceptance result, separate from the September 16 automated run.

- [x] Source records approved and expanded seed imported with reviewer/date attribution.
- [x] Adjusted source scope approved; fifteen reviewed records satisfy it and source roles remain explicit.
- [x] Repeat desktop/mobile browser checks after data changes.
- [x] Manual live WhatsApp rehearsal passed with the fifteen-record dataset (September 20, 2026); review-date and bilingual follow-up additions approved and tested September 21.
- [x] Verify a fresh setup from the README and reconcile privacy documentation with behavior.
- [x] Prepare the written summary and six-page PDF pitch deck with the final reviewed coverage.
- [x] Adapt the summary and deck to any submission-form requirements and final access details.
- [x] Demo recorded (September 20, 2026; MKV outside the repository).
- [x] Convert the demo to MP4 and upload it (September 21, 2026).
- [x] Verify video/audio playback and final submission access.
- [x] Public repository access verified without authentication (September 22, 2026).

- Running POC access is tracked separately in the [submission checklist](implementation-plan.md#submission-checklist).

- [x] Document submission formats and upload limits; see [runbook](demo-runbook.md#submission-requirements).
- [x] Confirm registration and exact deadline cutoff/timezone.
- [x] Submit the required deliverables and retain confirmation.

The repository is public; unauthenticated GitHub access was verified September 22, 2026. No open-source license has been selected. The local server/tunnel is a temporary demo setup, not durable judge access. Submission completed September 21, 2026. Subsequent access checks and validation are recorded separately below.

## Subsequent validation and earlier packaging evidence

September 21 follow-up validation: **134 automated tests pass**. Browser and WhatsApp replies expose the stored record review dates; project details, explanations, and verification with evidence include bilingual guidance for requesting an update and separate spending/completion evidence. Tests preserve the original September 14/16 dates, source amounts, citations, language switching, and all four verification outcomes. Replies without project evidence omit the guidance. All fifteen records remain within the WhatsApp 1,600-character limit in the tested discovery, detail, explanation, and verification flows, including first-use notices.

Chromium checks passed at 1280px, 390px, and 320px for review dates, English/Kiswahili guidance, explanations, partial-support verification, source links, and absence of horizontal overflow or JavaScript errors. Desktop and narrow-mobile screenshots were visually inspected. JavaScript syntax checks and `git diff --check` pass. Manual wording review was approved and live WhatsApp checks passed on September 21 for these additions; see [language review](language-review.md#review-date-and-follow-up-wording) and the [runbook](demo-runbook.md#rehearsal-acceptance). Earlier live acceptance results apply to the previous wording.

On September 16, a fresh local clone of `0762d53` installed the declared requirements into a new environment from the package cache and started with the documented single-worker command, without `.env`. Checks passed for the browser page, fifteen-record import, all three Wamagana result pages, direct Kiswahili verification, API no-store headers, and rejection of requests for `.env` and database files. Judge access is recorded in the completed submission checklist.

The privacy document reflects the implemented first-use notice, provider routes, request-triggered expiry cleanup, and browser-refresh behavior. External providers' retention settings remain unverified. The six-page [PDF pitch deck](../output/pdf/track-a-mtaani-pitch.pdf) now exists and all rendered pages have been checked. It documents the current dataset, source roles, and prototype limitations.

A [59-second silent browser rehearsal](../output/video/track-a-mtaani-browser-rehearsal.webm) records actual replies from the fifteen-record app. Chromium decoded the WebM at 1280 x 900; sampled frames were inspected. The September 20 demo recording is an approximately 20 MB MKV file outside the repository. MP4 conversion and upload completed September 21, 2026. Playback verification is complete in the submission checklist. A [judge walkthrough](judge-guide.md) provides reproducible steps and expected results; repository access is public; running POC access is tracked in the submission checklist.

Pitch PDF review, September 21: all six pages rendered and inspected; content matches the fifteen-record pilot, source roles, allocation limits, and AI-development disclosure. Source-link hit areas were corrected to enclose the full labels on slides 2 and 4, with underlining and an explicit source link added below the screenshot on slide 3. All three HTTPS link targets and label containment checks pass. Track positioning covers budget understanding and scrutiny of allocation decisions; expenditure tracking, issue reporting, and public-service delivery remain outside scope. File size: 143,443 bytes, within the 100 MB submission limit.