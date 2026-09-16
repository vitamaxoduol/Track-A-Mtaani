# Data and sources

## Current evidence inventory

Pilot selected: **Nyeri County, FY 2026/2027**, covering selected records in **Wamagana, Mweiga, and Kabaru**. Its approved programme budget provides project descriptions, explicit KES amounts, financial years, and wards in the same table. The owner authorized selecting the county with the clearest official evidence.

Two official PDFs were downloaded on September 14, 2026 from the [county budget index](https://www.nyeri.go.ke/bud/):

| Source | Local snapshot | Use |
| --- | --- | --- |
| [Approved Programme Based Budget 2026/27](https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf) | [county-budget.pdf](../data/raw/county-budget.pdf) | Ten reviewed observations on PDF pages 278, 287, 291, and 292 |
| [Approved Budget Estimates 2026/27](https://www.nyeri.go.ke/wp-content/uploads/2026/07/Approved-UPLOADED-Budget-Estimates-2026-27.pdf) | [nyeri-approved-estimates-2026-27.pdf](../data/raw/nyeri-approved-estimates-2026-27.pdf) | Supporting document registered; no project observations extracted or corroboration claimed |

Checksums and provenance are stored alongside the ten records in [projects.json](../data/processed/projects.json). Codex checked each candidate against rendered source pages. **The project owner confirmed review and approval on September 14, 2026.** All ten observations now have `REVIEWED` status, reviewer attribution, and a review date. The matching [demo seed](../data/seeds/demo_projects.json) supplies the running SQLite dataset; milestone 0 is complete.

The initial Kakamega assembly candidate was not selected because its cover and foreword/footer years conflict. No records from that document or from the original idea's illustrative examples are included in this dataset.

## First ten reviewed records

All amounts below are reviewed **allocations in the approved 2026/27 budget**, not reported spending. The source heading is “Estimated Budget amount (Kshs.)”; no thousands/millions multiplier applies. PDF page numbers and printed page labels agree on these four pages. The source label “New” is retained as text and is not interpreted as proof of construction or completion.

The owner approved these descriptions, wards, amounts, years, and references after the source review request. Any later changes or additional records require the same source check before entering the demo seed.

| Record | Source project description | Ward | KES | PDF page | Row on page |
| --- | --- | --- | ---: | ---: | ---: |
| 001 | Construction of ECDE ablution block at Hubuini ECDE | Wamagana | 700,000 | [278](https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf#page=278) | 2 |
| 002 | Construction of ECDE ablution block at Wamagana ECDE | Wamagana | 700,000 | [278](https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf#page=278) | 3 |
| 003 | Construction of ECDE ablution block at Karangia ECDE | Wamagana | 700,000 | [278](https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf#page=278) | 4 |
| 004 | Installation of streetlights | Wamagana | 1,000,000 | [287](https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf#page=287) | 4 |
| 005 | Mbaa - ini to Kianderi Rd | Wamagana | 2,000,000 | [291](https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf#page=291) | 5 |
| 006 | Kianjogu Karaihu | Wamagana | 3,000,000 | [291](https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf#page=291) | 6 |
| 007 | Installation of streetlights | Mweiga | 4,000,000 | [287](https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf#page=287) | 3 |
| 008 | Grading and Murraming | Mweiga | 4,000,000 | [291](https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf#page=291) | 4 |
| 009 | Installation of streetlights | Kabaru | 2,000,000 | [287](https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf#page=287) | 5 |
| 010 | Grading and Murraming | Kabaru | 2,500,000 | [292](https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf#page=292) | 3 |

Rows count data rows below the table header; the first row on page 278 is the countywide KDSP grant, which is excluded. Countywide projects are never assigned to these wards. Generic project descriptions are preserved; ward and source identifiers distinguish otherwise identical names.

## Select the pilot

Choose a county with accessible official documents that clearly identify projects, financial years, amounts, and locations. Prefer a small area that a team member or local reviewer knows. Record why the chosen documents can support the intended questions.

Target two or three documents and 15–30 reviewed projects across two or three wards. Record whether each document is a plan, draft budget, approved budget, revision, expenditure report, or implementation report. Do not assume these sources support the same claims.

## Ingestion and review

1. Record the official publisher, document title, URL, publication date where available, document type, and retrieval date.
2. Save a local source snapshot and checksum so later changes can be detected.
3. Extract candidate rows, retaining the original excerpt, amount label, and units. OCR output requires visual checking.
4. Normalize amounts without losing the original value. For example, a table expressed in thousands needs an explicit recorded conversion to KES.
5. Check each record against the rendered source page, including row/column headings and any footnotes.
6. Record both the one-based PDF page index and the printed page label when they differ.
7. Check location mapping and duplicate rows. Countywide projects must not be assigned to an individual ward without evidence.
8. Mark the record reviewed with a reviewer identifier and review date. Only reviewed records enter the searchable pilot dataset.

Keep conflicting observations visible for review. A later document does not silently overwrite an earlier record. Mark explicit revisions or supersession when the source supports that relationship.

## Proposed data model

Separate project identity from observations so an allocation, a spending figure, and a completion report cannot overwrite one another.

| Entity | Main fields |
| --- | --- |
| `Locality` | ID, name, administrative type, county ID, reviewed relationships |
| `LocalityAlias` | Alias text, locality ID, normalization rules |
| `SourceDocument` | ID, title, publisher, official URL, document type, publication/retrieval dates, financial year, checksum, local snapshot path |
| `Project` | ID, source name, optional normalized name, county, ward if evidenced, constituency/sub-county where evidenced, department |
| `ProjectObservation` | ID, project ID, observation kind, exact amount if applicable, currency, financial year, reporting period, document approval stage, source ID, PDF page, printed page label, excerpt, original amount/units, review status, reviewer, reviewed date |
| `Coverage` | Included documents, localities, years, review date, known gaps |

Use independent fields for **amount kind** (`ALLOCATION`, `EXPENDITURE`, `CONTRACT_VALUE`), **document approval stage** (`DRAFT`, `APPROVED`, `UNKNOWN`), and any **reported implementation state**. A completed project is not an amount type. Unknown values remain unknown.

Store money exactly using an integer minor-unit representation or validated fixed-decimal text, never binary floating point. Missing amounts are null, not zero. Preserve the reported currency and avoid adding amounts across different types or periods.

Sub-counties and constituencies should be distinct administrative types; do not assume they are interchangeable or impose a single parent chain without checking the pilot's geography.

## Minimum publishable observation

Each financial observation needs a reviewed project identity, amount and units, amount kind, financial year or relevant reporting period, official document title and URL, PDF page, and source excerpt. Preserve uncertainty about location or document approval rather than filling gaps by inference.

If a critical field cannot be checked, keep the observation out of financial answers until reviewed. A source-link outage should be disclosed; a retained snapshot may support inspection but must not be presented as a currently reachable official link.

## Coverage statement

Every discovery or verification flow should make clear that it searches selected documents. “No matching record in our coverage” is different from “no project exists.” Do not present a subtotal of the pilot dataset as a ward's entire budget.
