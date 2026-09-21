# Frontend design for the POC

## Decision

This screen is part of the fixed [implementation plan](implementation-plan.md). Keep its existing scope; do not add screens or features for the submission.

Build one responsive web chat in `frontend/`, inside this repository. Serve it from the FastAPI backend. Use plain HTML, CSS, and JavaScript for the initial screen. This keeps the demo to one app, one API, and one deployment.

The browser is the quickest entry point for judges to try the product. WhatsApp is the implemented community channel, using the same conversation service. Neither channel has its own budget or verification logic.

The discovery screen is implemented in `frontend/` and served by FastAPI. Project search, citations, inline evidence, pagination, coverage, and error retry are working. English/Kiswahili switching, reviewed explanations, and bounded claim verification are also implemented. Action buttons on older replies are disabled after a new reply arrives; use the latest project cards. The wireframe below remains the design reference.

## One screen

On first load, show the project name, a short purpose statement, selected-document coverage, three suggested questions, and a message input. Once a question is sent, use that same space for the conversation. Project details expand inline; official sources open in a new tab.

```text
┌────────────────────────────────────────────┐
│ Track-A-Mtaani            [EN / Kiswahili] │
│ Understand projects in your community.    │
│ POC · [County] · [Financial year]          │
│ Selected documents only    [Coverage]     │
├────────────────────────────────────────────┤
│ What would you like to know?              │
│ [Find projects] [Explain a budget term]    │
│ [Check a claim]                           │
│                                          │
│              What is planned in [ward]?   │
│                                          │
│ In our covered documents, I found:        │
│ ┌──────────────────────────────────────┐  │
│ │ [Project name]                      │  │
│ │ KSh [exact amount] · Allocated      │  │
│ │ [Ward] · FY [year]                  │  │
│ │ [Document title] · PDF page [n]     │  │
│ │ [View details] [Open source ↗]      │  │
│ └──────────────────────────────────────┘  │
│ Allocation does not prove spending       │
│ or completion.                           │
│                                          │
│ [Ask about your area…             ] [Send]│
└────────────────────────────────────────────┘
```

All bracketed data in this wireframe are placeholders, not verified records. The coverage control expands a short list of included documents and years in the same page.

## Visual direction

- Warm off-white background (`#F7F8F5`), white cards, dark text (`#18251F`), and deep green primary controls (`#166534`).
- System fonts, a 16px minimum body size, clear amounts, restrained borders, and comfortable spacing.
- One centered conversation column, approximately 760px maximum width on desktop; full width with padding on mobile.
- Text labels for statuses and verdicts. Color supplements meaning; it never carries the verdict alone.
- Visible keyboard focus, labeled form controls, at least 44px touch targets, and announced loading/error updates. Confirm contrast during implementation.

Keep the page light: no large hero image, custom font download, animation framework, or separate dashboard. The evidence cards provide the visual focus.

## Essential interactions

| State or action | Behavior |
| --- | --- |
| Welcome | Show coverage and suggested questions; no fabricated activity or project statistics |
| Suggested question | Fill the input with an editable prompt; the resident sends it |
| Clarification | Show selectable locality/year choices from the backend |
| Loading | Show “Checking available records…” and prevent duplicate submission |
| Results | Show up to three source-backed cards, with “Show more” when available |
| View details | Expand the department, evidence excerpt, and source information inline |
| Check a claim | Show a plain-language verdict, explanation, and citations in the conversation |
| No evidence | State the coverage gap and offer to change area or year |
| Request failure | Preserve the typed question and show a retry action |
| Language switch | Change interface language and subsequent replies; offer the last result in the selected language using the same evidence |
| Expired session | Explain that context expired and ask the resident to select their area again |

Keep chat history in page memory for the POC; reloading starts a new conversation. Use an opaque temporary browser session identifier with the backend's expiry policy. No login or persistent browser chat archive.

## Build boundary

First build the page and its essential states with explicitly labeled fixtures. Then connect it to real reviewed records through the chat endpoint. Finally check the full discovery-to-source flow on mobile and desktop, including keyboard access and long project titles/URLs.

Maps, charts, accounts, an admin dashboard, document uploads, and a full design system are deferred. A later need for multiple complex screens can justify revisiting the frontend stack; the POC does not depend on that decision.
