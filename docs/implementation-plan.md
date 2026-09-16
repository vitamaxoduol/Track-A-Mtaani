# Implementation plan

This is the fixed implementation scope for the Track-A-Mtaani hackathon POC that the project owner will submit to Andela. Milestones 0, 1, 1b, 2, and 3 are complete. The owner approved the glossary and Kiswahili wording and confirmed the live bilingual WhatsApp checks. Milestone 3 verdict wording and live verification checks are owner-approved, including the successful direct-Hakiki reply-language retry. The timeline and submission requirements below come from the hackathon description supplied by the owner on September 14, 2026; they have not been independently verified.

## Deadline and effort estimate

Budget approximately **35–45 focused hours** for an individual working with AI development tools, including implementation, source review, testing, and submission materials. This is a planning estimate, not a completion guarantee. It assumes usable official PDFs, timely messaging-account access, familiarity with the chosen stack, and access to Kiswahili review. Source extraction and provider setup are the largest schedule uncertainties.

There are seven calendar days from September 14 to the September 21 deadline. Aim to finish and submit on **September 20**, using September 21 only as contingency. The supplied announcement does not specify the cutoff time or timezone; the owner should confirm those in the submission form.

| Target date (2026) | Planned work |
| --- | --- |
| September 14 | Milestone 0: choose the pilot/year, collect sources, review the first ten records; check messaging-account access and submission-form requirements |
| September 15–16 | Milestone 1: implement the web chat, structured lookup, source cards, and required tests |
| September 17 | Milestone 1b: connect and test WhatsApp against the same evidence service |
| September 18 | Milestones 2–3: English/Kiswahili explanations and bounded claim verification |
| September 19 | Milestone 4: complete the reviewed dataset, run the full demo, fix failures, and check judge access |
| September 20 | Finish the video, pitch deck, written summary, and GitHub repository; owner submits |
| September 21 | Official submission deadline; contingency only |

Allow roughly 5–7 focused hours per day through September 20. Prepare submission notes during the build and reserve 6–8 hours of the total estimate for the video, deck, summary, and final packaging. The three-minute demo below is our working format, not a stated organizer duration requirement.

If a milestone slips, use the contingency and report the unmet exit condition. Do not silently drop WhatsApp or another agreed requirement, mark incomplete work done, or add features to compensate.

## Organizer requirements supplied by the owner

The selected track is **Transparency & Accountability**. The event asks for a working POC that demonstrates the problem, intended users, operation, and value; production readiness is not required.

The five required submission items are:

1. A working proof of concept.
2. A GitHub repository accessible to the judging team.
3. A short demo video.
4. A pitch deck.
5. A written summary.

These are delivery requirements within milestone 4, not additional product features. The supplied description requires an individual submission, Andela Learning Community membership, being based in Africa, and use of AI development tools. The core idea must be the participant's own; AI can assist development. Work must be original, created for this hackathon, and accessible to judges. The owner confirms eligibility, registration, and form-specific requirements.

The announcement lists grading on September 22–24, winners on September 25, and the OSF event in Kenya on October 5, 2026.

## Scope and execution rules

- Follow milestones in order: 0 → 1 → 1b → 2 → 3 → 4. Frontend layout with labeled fixtures may proceed during source review, as already agreed.
- Each implementation task must map to a milestone and its exit condition. Complete the required checks before marking that milestone done.
- Build only the agreed web chat, WhatsApp integration, reviewed project lookup and citations, English/Kiswahili explanations, and bounded claim verification.
- Do not add features, stretch goals, new infrastructure, or alternative frameworks during this POC. Audio is excluded from the submission scope.
- Routine implementation choices and fixes needed to meet the existing acceptance criteria remain within scope. Any proposed scope change must wait for an explicit request from the project owner.
- Use the repository layout in [architecture.md](architecture.md). Create implementation files only when their milestone needs them; a filename in the layout is not a requirement to implement a deferred feature.
- The project owner handles submission to Andela. Record actual submission requirements when provided; do not invent judging criteria or claim submission readiness before the evidence exists.

## Milestones

| Milestone | Work | Exit condition |
| --- | --- | --- |
| 0. Establish evidence | Select county/wards/year, register official documents, normalize and review ten project records | Each record can be traced to an exact source page; coverage gaps are documented |
| 1. Deliver the first slice | Single-screen web chat, FastAPI chat endpoint, SQLite import, locality resolution, project search/details, deterministic responses, citations | A browser locality question returns reviewed project cards with correct amount types, years, source links, and allocation wording |
| 1b. Connect WhatsApp | Add the messaging adapter to the same conversation service | A validated WhatsApp message returns the same evidence as the browser; duplicate deliveries are handled |
| 2. Explain and translate | Reviewed glossary, English explanations, Kiswahili templates and optional AI adapter, timeout fallback | Both languages preserve facts and citations; reviewed explanations work even when AI is unavailable |
| 3. Verify bounded claims | Resolve claim scope, compare observations, implement verdicts and uncertainty wording | Matching, conflicting, ambiguous, wrong-year, and missing-evidence cases produce justified results |
| 4. Prepare the demo | Grow to 15–30 records from two or three documents, polish conversations, review privacy behavior, rehearse | The full demo works with authentic sources and its limits are visible |

Source citations and factual-integrity checks are part of the first implementation milestone. They should not be postponed until AI is added.

Start frontend work from the [single-screen design](frontend-design.md). Use labeled fixtures to establish the layout while sources are reviewed, then connect the page to the backend. Keep frontend and backend in one repository and deployment. Complete the browser flow before adding the messaging adapter so provider setup does not block the initial demo.

## Progress tracker

Update a row only after its exit condition is met, with the relevant check results or demo evidence.

| Milestone | Status | Completion evidence |
| --- | --- | --- |
| 0. Establish evidence | Complete | Ten source records approved by the owner on Sept 14; two official source snapshots and checksums in `data/processed/projects.json` |
| 1. Deliver the first slice | Complete | Browser/API flow works against reviewed SQLite data; automated trust checks and desktop/390px/320px Chromium checks pass |
| 1b. Connect WhatsApp | Complete | Owner confirmed live `Wamagana`, `1`, `MORE`, and `HELP` replies on September 15; records, amounts, source pages, and allocation caveats match the reviewed data. Local tests cover signatures, sender IDs, session isolation, and persistent duplicate handling |
| 2. Explain and translate | Complete | Owner approved definitions and Kiswahili wording and confirmed live bilingual WhatsApp checks on September 15; 69 automated tests and desktop/390px/320px browser checks pass. Fixed templates preserve facts and citations without an AI service |
| 3. Verify bounded claims | Complete | All four verdicts and comparison boundaries pass automated tests; browser checks pass at 1280px/390px/320px. Owner approved wording and live verdict checks on September 16, including the corrected direct-Hakiki Kiswahili replies |
| 4. Prepare the demo | Not started | — |

Validation on September 15: **53 automated tests pass**, including sender-ID regression checks, plus earlier desktop and mobile browser checks for the implemented slice. The test stack emits two upstream deprecation warnings; there are no test failures. Local webhook tests use synthetic credentials and make no provider calls. Separately, the owner confirmed a successful live Wamagana reply at 23:18 EAT after fixing the sender-format check: Hubuini, Wamagana, and Karangia ECDE ablution projects, each with KSh 700,000 allocated for FY 2026/2027 and source PDF page 278. At 23:20 EAT, the owner also confirmed `1` returned Hubuini details and its source excerpt; `MORE` returned streetlights (KSh 1,000,000, page 287), Mbaa - ini to Kianderi Rd (KSh 2,000,000, page 291), and Kianjogu Karaihu (KSh 3,000,000, page 291); `HELP` returned coverage, privacy, and source roles. These live results complete milestone 1b. Duplicate delivery handling is validated by local tests, not by a claimed live retry. Milestone 2 implementation now passes **69 automated tests** (including bilingual evidence equality, glossary sources, no-AI operation, language/session isolation, and WhatsApp length checks for all ten projects). Browser language switching, project explanations, exact source links, and failure/retry behavior passed at 1280px, 390px, and 320px. The owner approved the wording in [language-review.md](language-review.md). The owner subsequently confirmed that all requested live bilingual checks worked. Screenshots from 23:36–23:38 EAT show SW discovery with unchanged amounts and source pages, clarification when ELEZA is sent before selecting a project, selection with 1, a cited Kiswahili explanation, ZAIDI pagination, and MSAADA coverage/privacy. Milestone 2 is complete.

Milestone 3 validation on September 16: **113 test cases validated** across the full-suite and targeted runs; the final verification/WhatsApp run passed all 67 checks. Checks include all four verdicts, contradiction precedence, missing/ambiguous scope, wrong year/stage, unsupported spending, exact decimal money, citation preservation, unresolved source conflicts, inert source instructions, session isolation, and signed WhatsApp replies. The conflict fixture stays in isolated tests, not demo data. Browser checks passed at 1280px, 390px, and 320px for the verdicts, EN/SW switching, source links, safe text rendering, and layout. See [verification-review.md](verification-review.md) for wording review and the live checklist. After the direct-Hakiki language correction, all 85 targeted verification, WhatsApp, and language tests passed. The owner confirmed the live retry on September 16: screenshots at 07:38 and 07:49 EAT show Kiswahili supported and contradicted verdicts, with KSh 3,000,000 retained as the source allocation and PDF page 291 unchanged. Milestone 3 is complete. Milestone 4 remains unstarted.

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

## Decisions to resolve

| Decision | Working proposal | Resolution point |
| --- | --- | --- |
| Pilot county and wards | Nyeri: Wamagana, Mweiga, Kabaru | Selected; initial ten records approved |
| Financial year | 2026/2027 approved budget | Selected and displayed in answers |
| Submission format and deadline | Individual submission; September 21, 2026; five deliverables listed above | Confirm exact cutoff/timezone and form-specific formats before submission |
| Daily availability | Plan assumes roughly 5–7 focused hours per day through September 20 | Confirm against the owner's availability |
| Backend and database | Python/FastAPI and SQLite, as suggested in the supplied specification | Before scaffolding |
| Frontend | Plain HTML/CSS/JavaScript in `frontend/`, served by FastAPI; one responsive chat screen | Working POC design |
| Messaging provider | Custom TwiML discovery, detail, pagination, and help replies confirmed on the owner's Twilio Sandbox account | Resolved for the POC; milestone 1b complete |
| AI provider/model | Reviewed deterministic templates; no AI provider required for milestone 2 | Optional AI adapter not enabled |
| Kiswahili reviewer | Project owner reviewed and approved glossary, cautions, and interface/WhatsApp wording on September 15 | Recorded in language-review.md |
| Hosting and cost limit | Undecided | Before deployment |

## Three-minute demo

1. **0:00–0:25 — The problem:** A resident wants to understand a local project, but the answer is buried in an official document.
2. **0:25–1:00 — Discovery:** Send a covered locality question in the web chat and open one result. Also demonstrate the same query through WhatsApp using the tested milestone 1b flow.
3. **1:00–1:30 — Evidence:** Open the official document at the cited PDF page. Point to the exact amount and its meaning.
4. **1:30–1:55 — Accessibility:** Switch the same result to Kiswahili.
5. **1:55–2:30 — Verification:** Check a simple claim, then show that an unsupported spending claim receives an insufficient-evidence answer.
6. **2:30–3:00 — Vision:** Explain that reviewed records supply the facts, AI assists understanding, and this pilot covers selected documents only.

Use only claims and records checked against the selected documents. If connectivity fails, use a clearly labeled recording of the tested flow or a local replay with the same reviewed dataset. Do not present a replay as a live WhatsApp interaction.

## Completion evidence

Before calling the hackathon prototype complete, retain the source inventory, reviewed dataset, targeted test results, and demo walkthrough. Update the README with real setup instructions and observed limitations as milestones progress.

## Submission handoff to the project owner

- [ ] All milestone exit conditions are met and the progress tracker includes evidence.
- [ ] README setup commands and environment variable names match the implemented app; no credentials are committed.
- [ ] Official source documents and reviewed records support every financial claim shown in the demo.
- [ ] Web and WhatsApp flows, citations, Kiswahili, and claim verification have been demonstrated and the required tests pass.
- [ ] Known gaps are recorded in [limitations.md](limitations.md), and actual data handling is recorded in [privacy.md](privacy.md).
- [ ] The owner has selected the license before the `LICENSE` file is finalized.
- [ ] The working POC and GitHub repository are accessible to judges, and setup has been checked from the documented instructions.
- [ ] A short demo video, pitch deck, and written summary are complete and consistent with the implemented behavior.
- [ ] The owner has confirmed eligibility, signed up, and checked the submission form's exact cutoff/timezone and required formats.
- [ ] The owner has submitted all five deliverables and retained submission confirmation.

Stop feature work once this scope is complete. The owner submits the POC; this document does not claim it has been submitted.
