# Implementation plan

Fixed scope for the Track-A-Mtaani hackathon POC. Milestones 0–3, including WhatsApp, are complete. M4 covers final demo materials, judge access, and submission. Review approvals and validation results are recorded below.

## Deadline and effort estimate

Budget approximately **35–45 focused hours** for an individual working with AI development tools, including implementation, source review, testing, and submission materials. This is a planning estimate, not a completion guarantee. It assumes usable official PDFs, timely messaging-account access, familiarity with the chosen stack, and access to Kiswahili review. Source extraction and provider setup are the largest schedule uncertainties.

There are seven calendar days from September 14 to the September 21 deadline. Aim to finish and submit on **September 20**, using September 21 only as contingency. The exact deadline cutoff/timezone remains to be confirmed.

| Target date (2026) | Planned work |
| --- | --- |
| September 14 | Milestone 0: choose the pilot/year, collect sources, review the first ten records; check messaging-account access and submission-form requirements |
| September 15–16 | Milestone 1: implement the web chat, structured lookup, source cards, and required tests |
| September 17 | Milestone 1b: connect and test WhatsApp against the same evidence service |
| September 18 | Milestones 2–3: English/Kiswahili explanations and bounded claim verification |
| September 19 | Milestone 4: complete the reviewed dataset, run the full demo, fix failures, and check judge access |
| September 20 | Finish the video, pitch deck, written summary, and GitHub repository; submit |
| September 21 | Official submission deadline; contingency only |

Allow roughly 5–7 focused hours per day through September 20. Prepare submission notes during the build and reserve 6–8 hours of the total estimate for the video, deck, summary, and final packaging. The three-minute demo below is a working format, not a stated organizer duration requirement.

Unmet exit conditions remain open; scope changes require explicit approval.

## Organizer requirements

The selected track is **Transparency & Accountability**. The event asks for a working POC that demonstrates the problem, intended users, operation, and value; production readiness is not required.

The five required submission items are:

1. A working proof of concept.
2. A GitHub repository accessible to the judging team.
3. A short demo video.
4. A pitch deck.
5. A written summary.

These are delivery requirements within milestone 4, not additional product features. The hackathon requires an individual submission, Andela Learning Community membership, being based in Africa, and use of AI development tools. The core idea must be the participant's own; AI can assist development. Work must be original, created for this hackathon, and accessible to judges. Eligibility, registration, and form requirements are part of the submission checklist.

The announcement lists grading on September 22–24, winners on September 25, and the OSF event in Kenya on October 5, 2026.

## Scope and execution rules

- Follow milestones in order: 0 → 1 → 1b → 2 → 3 → 4. Frontend layout with labeled fixtures may proceed during source review.
- Each implementation task must map to a milestone and its exit condition. Complete the required checks before marking that milestone done.
- Build only the agreed web chat, WhatsApp integration, reviewed project lookup and citations, English/Kiswahili explanations, and bounded claim verification.
- Do not add features, stretch goals, new infrastructure, or alternative frameworks during this POC. Audio is excluded from the submission scope.
- Routine implementation choices and fixes needed to meet the existing acceptance criteria remain within scope. Any proposed scope change must wait for explicit approval.
- Use the repository layout in [architecture.md](architecture.md). Create implementation files only when their milestone needs them; a filename in the layout is not a requirement to implement a deferred feature.
- Submission readiness requires completed delivery checks and verified judge access.

## Milestones

| Milestone | Work | Exit condition |
| --- | --- | --- |
| 0. Establish evidence | Select county/wards/year, register official documents, normalize and review ten project records | Each record can be traced to an exact source page; coverage gaps are documented |
| 1. Deliver the first slice | Single-screen web chat, FastAPI chat endpoint, SQLite import, locality resolution, project search/details, deterministic responses, citations | A browser locality question returns reviewed project cards with correct amount types, years, source links, and allocation wording |
| 1b. Connect WhatsApp | Add the messaging adapter to the same conversation service | A validated WhatsApp message returns the same evidence as the browser; duplicate deliveries are handled |
| 2. Explain and translate | Reviewed glossary, English explanations, Kiswahili templates and optional AI adapter, timeout fallback | Both languages preserve facts and citations; reviewed explanations work even when AI is unavailable |
| 3. Verify bounded claims | Resolve claim scope, compare observations, implement verdicts and uncertainty wording | Matching, conflicting, ambiguous, wrong-year, and missing-evidence cases produce justified results |
| 4. Prepare the demo | Maintain 15–30 reviewed records from at least one official project-level document; identify additional documents as answer sources or context only; polish conversations, review privacy behavior, rehearse | The full demo works with authentic sources and its limits are visible |

The [source adjustment approved September 16, 2026](source-scope-decision.md) replaces the original two-or-three-project-source target. Registered context documents do not count as independent corroboration. The fifteen reviewed records meet the adjusted dataset condition; the remaining M4 delivery checks still apply.

Source citations and factual-integrity checks are part of the first implementation milestone. They should not be postponed until AI is added.

Start frontend work from the [single-screen design](frontend-design.md). Use labeled fixtures to establish the layout while sources are reviewed, then connect the page to the backend. Keep frontend and backend in one repository and deployment. Complete the browser flow before adding the messaging adapter so provider setup does not block the initial demo.

## Progress tracker

Update a row only after its exit condition is met, with the relevant check results or demo evidence.

| Milestone | Status | Completion evidence |
| --- | --- | --- |
| 0. Establish evidence | Complete | Ten source records approved after manual review on September 14; two official source snapshots and checksums in `data/processed/projects.json` |
| 1. Deliver the first slice | Complete | Browser/API flow works against reviewed SQLite data; automated trust checks and desktop/390px/320px Chromium checks pass |
| 1b. Connect WhatsApp | Complete | Manual live checks passed for `Wamagana`, `1`, `MORE`, and `HELP` replies on September 15; records, amounts, source pages, and allocation caveats match the reviewed data. Local tests cover signatures, sender IDs, session isolation, and persistent duplicate handling |
| 2. Explain and translate | Complete | Definitions and Kiswahili wording approved; manual live bilingual WhatsApp checks passed on September 15; 69 automated tests and desktop/390px/320px browser checks pass. Fixed templates preserve facts and citations without an AI service |
| 3. Verify bounded claims | Complete | All four verdicts and comparison boundaries pass automated tests; browser checks pass at 1280px/390px/320px. Wording approved and manual live verdict checks passed on September 16, including the corrected direct-Hakiki Kiswahili replies |
| 4. Prepare the demo | In progress | Branch `m4/demo-submission` starts at `49e01c5`; 124 expanded-dataset tests and desktop/mobile browser checks pass. Fifteen records are reviewed and imported. The approved source adjustment on September 16 completes the dataset condition; expanded manual live WhatsApp checks passed on September 20. The demo was recorded September 20, converted to MP4, and uploaded September 21. Playback verification, judge access, and final submission checks remain open. See [m4-review.md](m4-review.md) |

## Validation record

| Date | Validation | Result |
| --- | --- | --- |
| September 15 | First-slice automated checks | 53 tests passed, including sender-ID handling; two upstream deprecation warnings |
| September 15 | Manual live WhatsApp discovery | Ward lookup, detail selection, pagination, coverage, and privacy replies passed with correct amounts and citations |
| September 15 | Bilingual validation | 69 automated tests passed; browser checks passed at 1280px, 390px, and 320px; manual live selection, explanation, pagination, and help passed in Kiswahili |
| September 16 | Bounded verification | 113 cases validated across full-suite and targeted runs; all 67 final verification/WhatsApp checks passed; browser verdicts, language switching, citations, and layout passed |
| September 16 | Direct-Hakiki language correction | All 85 targeted verification, WhatsApp, and language tests passed; manual live supported and contradicted replies returned Kiswahili with unchanged source evidence |
| September 16 | Expanded fifteen-record dataset | 124 automated tests and desktop/mobile browser checks passed; see [M4 review](m4-review.md) |
| September 20 | Expanded manual live WhatsApp checks | Passed the [demo checklist](demo-runbook.md#expanded-live-whatsapp-check) |

Automated webhook checks use synthetic credentials and make no provider calls. Duplicate-delivery and conflicting-source cases are tested locally; synthetic observations are never imported into the demo dataset. Wording and live acceptance details are in [language review](language-review.md) and [verification review](verification-review.md).

## First working slice: definition of done

- The app starts and imports at least ten reviewed project records into SQLite.
- A covered ward resolves correctly; an ambiguous place prompts clarification.
- Project search and details return structured observations and citations.
- A browser message returns a concise list and supports expanding project details and opening official sources.
- The page works on mobile and desktop and exposes loading, empty, error, and clarification states.
- Each financial result carries its year, amount type, source title, page, and official URL.
- Allocation replies distinguish allocation from spending and completion.
- Out-of-coverage requests and empty results produce honest, useful responses.
- Targeted data, trust, and chat endpoint integration tests pass.

Milestone 1b additionally requires validated webhook requests, numbered detail selections, duplicate-delivery handling, and webhook integration checks.

## Decisions and remaining checks

| Decision | Working proposal | Resolution point |
| --- | --- | --- |
| Pilot county and wards | Nyeri: Wamagana, Mweiga, Kabaru | Selected; initial ten records approved |
| Financial year | 2026/2027 approved budget | Selected and displayed in answers |
| Submission format and deadline | Individual submission; September 21, 2026; five deliverables listed above | Formats and size limits in [the runbook](demo-runbook.md#submission-requirements); exact cutoff/timezone still unconfirmed |
| Daily availability | Plan assumes roughly 5–7 focused hours per day through September 20 | Original scheduling assumption |
| Backend and database | Python/FastAPI and SQLite | Implemented |
| Frontend | Plain HTML/CSS/JavaScript in `frontend/`, served by FastAPI; one responsive chat screen | Working POC design |
| Messaging provider | Custom TwiML discovery, detail, pagination, and help replies confirmed on the configured Twilio Sandbox account | Resolved for the POC; milestone 1b complete |
| AI provider/model | Reviewed deterministic templates; no AI provider required for milestone 2 | Optional AI adapter not enabled |
| Kiswahili reviewer | Manual review of glossary, cautions, and interface/WhatsApp wording completed September 15 | Recorded in language-review.md |
| Hosting and cost limit | Undecided | Before deployment |

## Three-minute demo

1. **0:00–0:25 — The problem:** A resident wants to understand a local project, but the answer is buried in an official document.
2. **0:25–1:00 — Discovery:** Send a covered locality question in the web chat and open one result. Also demonstrate the same query through WhatsApp using the tested milestone 1b flow.
3. **1:00–1:30 — Evidence:** Open the official document at the cited PDF page. Point to the exact amount and its meaning.
4. **1:30–1:55 — Accessibility:** Switch the same result to Kiswahili.
5. **1:55–2:30 — Verification:** Check a simple claim, then show that an unsupported spending claim receives an insufficient-evidence answer.
6. **2:30–3:00 — Vision:** Explain that reviewed records supply the facts and reviewed templates supply explanations. AI tools assisted development; the running POC uses no AI provider. This pilot covers selected documents only.

Use only claims and records checked against the selected documents. If connectivity fails, use a clearly labeled recording of the tested flow or a local replay with the same reviewed dataset. Do not present a replay as a live WhatsApp interaction.

## Completion evidence

Completion evidence consists of the source inventory, reviewed dataset, test results, demo walkthrough, reproducible setup instructions, and documented limitations.

## Submission checklist

- [ ] All milestone exit conditions are met and the progress tracker includes evidence.
- [ ] README setup commands and environment variable names match the implemented app; no credentials are committed.
- [ ] Official source documents and reviewed records support every financial claim shown in the demo.
- [ ] Web and WhatsApp flows, citations, Kiswahili, and claim verification have been demonstrated and the required tests pass.
- [ ] Known gaps are recorded in [limitations.md](limitations.md), and actual data handling is recorded in [privacy.md](privacy.md).
- [x] Private repository with no open-source license; no `LICENSE` file included.
- [ ] The working POC and GitHub repository are accessible to judges, and setup has been checked from the documented instructions.
- [ ] A short demo video, pitch deck, and written summary are complete and consistent with the implemented behavior.
- [ ] Eligibility, registration, exact deadline cutoff/timezone, and required formats are confirmed.
- [ ] All required deliverables are submitted and confirmation is retained.

Feature work is limited to this scope. Submission remains pending until the checklist is complete and confirmation is recorded.
