# Track-A-Mtaani

**Understand public projects in your community, with sources you can check.**

Track-A-Mtaani is a civic information POC for the Andela hackathon's Transparency & Accountability track. The working browser chat retrieves reviewed local project allocations from official documents. WhatsApp uses the same conversation service; the owner confirmed live Sandbox discovery, details, pagination, and help on September 15, 2026.

> An allocation is not proof of spending or completion. Project facts come from reviewed records, never generated figures.

## Current status

- **Milestone 0 complete:** ten records in Wamagana, Mweiga, and Kabaru, Nyeri County, FY 2026/2027. The project owner reviewed and approved the source records on September 14, 2026.
- **Milestone 1 complete:** responsive web chat, SQLite lookup, exact amounts, official citations, details, pagination, and clear coverage limits.
- **Milestone 1b complete:** the owner confirmed live WhatsApp discovery, `1` for project details and evidence, `MORE` for the remaining Wamagana records, and `HELP` for coverage and privacy on September 15, 2026. Local tests cover signature validation, sender formats, and duplicate handling. WhatsApp is disabled by default and enabled in the private demo configuration.
- **Milestone 2 complete:** reviewed English/Kiswahili glossary and project explanations, session language switching, and shared web/WhatsApp rendering. The owner approved the wording and confirmed the live bilingual WhatsApp checks on September 15, 2026.
- **Milestone 3 complete:** bounded project/amount verification with four evidence-scoped verdicts. The owner approved the wording and confirmed live checks on September 16, including direct `Hakiki` replies in Kiswahili for supported and contradicted claims.
- **Milestone 4:** expanded reviewed dataset and submission materials are not yet implemented.

One repository, one FastAPI application, one SQLite database, and plain HTML/CSS/JavaScript. Browser discovery needs no paid service or API key. The local Git repository is initialized; no GitHub remote, commit, or publication has been created.

## Run locally

Requires Python 3.12+ and `uv` (or Python's `venv` and `pip`). From the repository root:

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --no-access-log
```

Open **http://127.0.0.1:8000**. Startup validates source checksums and reviewed records, then creates/seeds `data/track_mtaani.sqlite3`. No PDF downloads or external API calls occur during startup or browser search. Run a single worker: conversation state is held in memory for this POC.

With standard Python tooling, use `python3 -m venv .venv` and `.venv/bin/python -m pip install -r requirements.txt` before the same server command.

Try:

- `What projects are planned in Wamagana?`
- `Show road projects in Mweiga`
- `How much was allocated to Kianjogu Karaihu?`
- `What water projects are in Kabaru?` — an honest no-match response.
- `How much was spent in Wamagana?` — spending cannot be established from allocation records.

Use **Show more projects**, expand **View details & evidence**, and open the official source. The first row links to PDF page 278. Use **Explain this project** for a selected record or **Understand a budget** for a glossary definition. The **EN / SW** buttons switch the interface and repeat the current reply in the selected language without advancing results. Use **Check a claim** for an editable example with the complete comparison scope.

## Milestone 2: explanations and Kiswahili

No AI key or paid AI provider is needed. Fixed, owner-reviewed templates supply definitions for allocation, recurrent expenditure, and development expenditure. Project explanations use the same reviewed records and citations as discovery. Source names, project names, amounts, years, and excerpts stay verbatim; only surrounding wording changes.

Browser: use **EN / SW**, **Understand a budget**, or **Explain this project**. WhatsApp: send `SW` or `EN`; `1` selects a project; `EXPLAIN` / `ELEZA` explains the selected record; `EXPLAIN 1` / `ELEZA 1` selects and explains a current result. `ZAIDI` means more results and `MSAADA` opens help.

Try `Explain recurrent expenditure`, `Matumizi ya kawaida ni nini?`, `Eleza mgao wa bajeti`, or `Onyesha miradi ya barabara katika Mweiga`. This is a bounded bilingual POC, not unrestricted translation. Unknown terms, unsupported languages, uncovered places, and spending/completion questions receive clarification or an evidence limitation.

The [wording review](docs/language-review.md) records owner approval and source references. The Treasury glossary reference supplies no project observations and does not expand milestone 4's reviewed dataset. Templates run without an AI service, so provider availability cannot interrupt explanations; an optional generative adapter has not been enabled.

## Milestone 3: check one claim

Use the complete format (the order is intentional):

```text
Verify Kianjogu Karaihu in Wamagana FY 2026/2027 approved allocation KSh 3,000,000
```

The source records KSh 3,000,000 on PDF page 291, so this allocation claim is supported. Change the amount to `2,000,000` to see a contradiction limited to that source. Append `and completed` for partial support: the allocation matches, but completion has not been established. Replace `allocation` with `spending` for insufficient evidence. A different year or draft budget also lacks comparable reviewed evidence.

Kiswahili: `Hakiki Kianjogu Karaihu katika Wamagana mwaka wa fedha 2026/2027 iliyoidhinishwa mgao KSh 3,000,000`. Starting a claim with `Hakiki` selects Kiswahili directly. Send `SW` / `EN` to repeat the current verdict in the other language without changing the claim or evidence. Other messages retain the active session language.

The verifier accepts one exact project name, ward, financial year, document stage, amount type, and exact KSh/KES amount. It supports `million` / `milioni`, `billion` / `bilioni`, and one optional spending or completion clause. Unknown wording, omitted scope, multiple projects/amounts, or unsupported qualifiers prompt a complete resubmission. It does not silently ignore clauses or infer scope from the previous query. Conflicting comparable observations are shown together and remain unresolved. See [verification wording and live checklist](docs/verification-review.md).

## Checks

```bash
.venv/bin/python -m pytest -q
node --check frontend/app.js
```

Automated tests exercise record review gates, exact amounts, citations, lookup boundaries, session expiry, request limits, and signed WhatsApp requests using synthetic credentials. They never call Twilio. Desktop and 390px/320px mobile flows have also been checked in Chromium, including pagination, source details, failed-request retry, and safe text rendering.

## WhatsApp setup for milestone 1b

The adapter expects **Twilio Sandbox custom TwiML replies**. Twilio's Sandbox documentation describes free-form replies, while its current trial documentation restricts custom content and direct TwiML responses. Confirm which capabilities your account has before relying on the trial or deciding to upgrade. See [Sandbox replies](https://www.twilio.com/docs/whatsapp/sandbox) and [trial restrictions](https://www.twilio.com/docs/usage/trials/try-out-whatsapp). This implementation does not bypass those restrictions.

1. Confirm the account supports custom Sandbox replies and join the Sandbox from your test phone using the instructions shown by Twilio.
2. Copy `.env.example` to `.env` and fill in the four Twilio values locally. Keep `.env` private; do not paste credentials into chat or commit them.
3. Set `TWILIO_WEBHOOK_URL` to the exact public HTTPS URL ending in `/api/v1/whatsapp/webhook`, with no query string or trailing slash. The app must be reachable by Twilio through your chosen host or tunnel. Localhost alone is insufficient. The private local demo uses ngrok; restart it when needed and update both URL settings if its address changes.
4. Configure that exact URL as the Sandbox's incoming-message webhook using **POST**. Set `TRACK_MTAANI_WHATSAPP_ENABLED=1` only when ready to test on your account.
5. Start the app with the environment file:

```bash
.venv/bin/python -m uvicorn src.main:app --env-file .env --host 127.0.0.1 --port 8000 --no-access-log
```

6. Send `Wamagana` from your joined test phone. Check the amounts, source pages, `1` for details, `MORE`, and `HELP`. Record the real test result before marking milestone 1b complete.

The backend validates Twilio signatures against the configured public URL. It returns a single TwiML reply containing cited results. Duplicate incoming message IDs return an empty response for 24 hours. The owner joined the Sandbox and received a live reply through the local app and ngrok tunnel. Diagnostic provider API access was read-only; the adapter sends replies through TwiML without outbound Messaging REST requests. Actual messaging may incur provider charges.

Incoming senders may be phone numbers or [WhatsApp business-scoped user IDs](https://www.twilio.com/docs/whatsapp/key-concepts). Both formats are accepted after signature validation and hashed for temporary session lookup; raw sender identifiers are not persisted. The first live test revealed this format difference. The corrected adapter passes 69 automated tests, and the owner confirmed successful discovery, detail, pagination, and help replies after the fix.

## Configuration

| Variable | Purpose |
| --- | --- |
| `TRACK_MTAANI_DB_PATH` | Optional SQLite path; defaults to `data/track_mtaani.sqlite3` |
| `TRACK_MTAANI_WHATSAPP_ENABLED` | Defaults to `0`; set to `1` to enable the configured adapter |
| `TWILIO_ACCOUNT_SID` | Account used by the Sandbox |
| `TWILIO_AUTH_TOKEN` | Private signature-validation token |
| `TWILIO_WHATSAPP_NUMBER` | Sandbox destination in `whatsapp:+...` format |
| `TWILIO_WEBHOOK_URL` | Exact public HTTPS callback URL |

`.env` is loaded only when `--env-file .env` is supplied. Keep a single worker and use `--no-access-log` to avoid retaining caller IPs in Uvicorn access logs. Host or proxy logging must be checked separately before a public demo.

## Data and fixed scope

Two official Nyeri PDFs are retained in `data/raw/`. All ten current project observations come from the programme budget; the second document is registered but has not supplied project answers. [Source inventory and review table](docs/data-sources.md) record this distinction. Processed and seed JSON files contain the reviewed facts and provenance. The importer checks the snapshot hashes and rejects unreviewed, uncited, or inconsistent records.

The [implementation plan](docs/implementation-plan.md) is the fixed submission scope. No additional features or audio are planned. The final dataset target remains 15–30 reviewed records from two or three documents; current coverage is deliberately incomplete. The owner will submit the POC, GitHub repository, demo video, pitch deck, and written summary to Andela.

The supplied *Track-A-Viwanda* specification informed this project under the owner's chosen name **Track-A-Mtaani**. Its illustrative figures were not used as data. The owner must choose a license before publication; no license has been assumed.

## Documentation

| Document | Purpose |
| --- | --- |
| [Product requirements](docs/product-requirements.md) | Fixed product scope and acceptance criteria |
| [Frontend design](docs/frontend-design.md) | Screen design and interactions |
| [Architecture](docs/architecture.md) | Components, repository layout, and technical decisions |
| [Verification review](docs/verification-review.md) | Verdict wording, bounded claim format, and live checks |
| [Wording review](docs/language-review.md) | Reviewed English/Kiswahili definitions, wording, and test checklist |
| [Data and sources](docs/data-sources.md) | Pilot evidence, review records, and data model |
| [Trust model](docs/trust-model.md) | Factual integrity and future verification rules |
| [Privacy](docs/privacy.md) | Actual data handling and provider flows |
| [Limitations](docs/limitations.md) | Current gaps and prototype boundaries |
| [Implementation plan](docs/implementation-plan.md) | Milestone status and submission checklist |
