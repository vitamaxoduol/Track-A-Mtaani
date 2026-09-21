# Product requirements

## Vision

Track-A-Mtaani should make local public-budget information understandable and checkable from an ordinary WhatsApp conversation. A resident should be able to find a relevant project, understand the recorded amount, and open the evidence without navigating an entire budget document first.

For the POC, add a browser chat as an accessible demo entry point. It shares the WhatsApp conversation logic and evidence, with clickable project cards in place of numbered replies. Build it in the same repository and deploy it with the backend. The [frontend design](frontend-design.md) defines the single-screen experience.

The working problem hypothesis is that publication alone does not make civic information usable: large documents, technical language, and uncertain location names can make a simple question difficult to answer. Validate this hypothesis with residents of the selected pilot area.

## Who it serves

- Residents seeking information about roads, water, health, and other local projects.
- People who prefer Kiswahili or short mobile messages.
- Community organizers and journalists seeking an initial source reference to inspect.

For the hackathon, prioritize a resident asking about their ward. The broader vision is searchable, source-backed local information across more areas and reporting periods.

## Scope

The [implementation plan](implementation-plan.md) controls the fixed submission scope. This document elaborates existing requirements; it does not authorize additional features.

| Priority | Capability |
| --- | --- |
| First working slice | Responsive web chat, English project discovery and details, county/ward clarification, exact amounts, citations, coverage notice, graceful missing-data responses |
| Hackathon target | WhatsApp connected to the same service, Kiswahili text, explanations using reviewed definitions, verification of a single project/amount claim |
| Outside this POC | Audio responses, nationwide coverage, live expenditure tracking, citizen reports, corruption investigations, user accounts, GPS search, voice-note input, autonomous agents |

The pilot targets one county, two or three wards, and 15–30 reviewed project records from at least one official project-level document. Additional official documents must be registered separately as answer sources or context only; registration alone is not independent corroboration. This [approved adjustment of September 16, 2026](source-scope-decision.md) replaces the original two-or-three-project-source target. Ten reviewed records are sufficient for the first development milestone; the broader record target applies to the final demo.

## User journeys

### Discover a project

1. The resident names an area or asks about “my ward.”
2. The assistant asks for missing county/ward context. It does not infer home location from a phone number.
3. If a name has multiple matches, the assistant offers the matching places for selection.
4. It searches reviewed records for the resolved area and financial year.
5. It returns up to three projects per message, with a next-results option when needed. Each result includes an amount type, financial year, and citation.
6. A numbered reply opens details from the preceding result list. An expired selection asks the user to search again.

If more than one financial year is available and none was requested, ask which year to use. If only one year is covered, state it explicitly.

### Understand the evidence

A resident asks what a term means or requests an explanation of a selected project. The assistant uses a reviewed glossary or retrieved source passage and preserves the project's names, amounts, dates, and references. A general definition must not imply that a particular project has progressed or received funding.

### Switch language

`SW` switches to Kiswahili; `EN` switches to English. This preference lasts for the active session. Both versions use the same underlying evidence and citations. Unsupported language requests receive a short explanation of the available options.

The web interface exposes an English/Kiswahili control for the same action. Project detail buttons replace numbered selections, and suggested questions provide quick entry to Discover, Explain, and Verify without separate pages.

### Check a claim

The resident supplies a claim about one project's amount. The assistant resolves the project, area, year, and whether the claim concerns allocation or spending. It asks for missing context where needed, compares like-for-like evidence, and returns a verdict with its scope and source. See the [trust model](trust-model.md).

## Acceptance criteria

- A resident can discover a project, open its details, and locate the cited evidence in the official document.
- The web chat works on a narrow phone screen and a laptop, supports keyboard interaction, and shows loading, empty, and retry states.
- Web and WhatsApp answers for the same query use the same reviewed observations and verification verdicts.
- Every displayed financial fact matches a reviewed record, including units, year, and amount type.
- Allocation answers explicitly say that an allocation is not proof of spending or completion.
- A query outside the dataset states the coverage limit; it never says no project exists merely because no record was found.
- Ambiguous locations and project names prompt clarification rather than an arbitrary match.
- English and Kiswahili answers preserve identical factual fields; Kiswahili wording is reviewed before the demo.
- Claim verification exposes the evidence used and does not treat missing evidence as contradiction.
- If AI is unavailable or produces an invalid explanation, the resident still receives a deterministic, cited answer where records exist.

## Early validation

Ask a few pilot-area residents to find a project, identify whether the amount means allocation or spending, and open its source. Record where they become confused. These observations should shape message wording before adding more features; they are planned validation, not completed research.
