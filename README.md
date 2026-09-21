# Track-A-Mtaani

**Understand public projects in your community, with sources you can check.**

Track-A-Mtaani is a civic information POC for the Andela hackathon's Transparency & Accountability track. The working browser chat retrieves reviewed local project allocations from official documents. WhatsApp uses the same conversation service; manual live Sandbox checks passed for discovery, details, pagination, and help on September 15, 2026.

> An allocation is not proof of spending or completion. Project facts come from reviewed records, never generated figures.

## Current status

- **Milestone 0 complete:** ten records in Wamagana, Mweiga, and Kabaru, Nyeri County, FY 2026/2027. Source review completed on September 14, 2026.
- **Milestone 1 complete:** responsive web chat, SQLite lookup, exact amounts, official citations, details, pagination, and clear coverage limits.
- **Milestone 1b complete:** manual live checks passed for discovery, project details, pagination, coverage, and privacy on September 15, 2026. Local tests cover signature validation, sender formats, and duplicate handling. WhatsApp is disabled by default and enabled in the private demo configuration.
- **Milestone 2 complete:** reviewed English/Kiswahili glossary and project explanations, session language switching, and shared web/WhatsApp rendering. Wording review and manual live bilingual checks completed on September 15, 2026.
- **Milestone 3 complete:** bounded project/amount verification with four evidence-scoped verdicts. Wording review and manual live checks completed on September 16, including direct `Hakiki` replies in Kiswahili for supported and contradicted claims.
- **Milestone 4 in progress:** five additional records were reviewed and imported on September 16; demo and submission preparation is tracked in [M4 review](docs/m4-review.md). The active seed contains fifteen reviewed records. Expanded manual live WhatsApp checks passed on September 20, 2026. The demo was converted to MP4 and uploaded September 21, 2026. Playback verification and submission handoff remain open.

One repository, one FastAPI application, one SQLite database, and plain HTML/CSS/JavaScript. Browser discovery needs no paid service or API key. The [GitHub repository](https://github.com/vitamaxoduol/Track-A-Mtaani) is private; the initial POC commit is `49e01c5`. M4 work is on `m4/demo-submission`.

## Run locally

Requires Python 3.12+ and `uv` (or Python's `venv` and `pip`). From the repository root:

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --no-access-log
```

Open **http://127.0.0.1:8000**. Startup validates source checksums and reviewed records, then creates/seeds `data/track_mtaani.sqlite3`. No PDF downloads or external API calls occur during startup or browser search. Run a single worker: conversation state is held in memory for this POC.

With standard Python tooling, use `python3 -m venv .venv` and `.venv/bin/python -m pip install -r requirements.txt` before the same server command.

For WhatsApp testing after a shutdown or restart, use the [restart checklist](#restart-the-whatsapp-demo-after-a-shutdown) below so the app loads `.env` and the public tunnel is available.

Try:

- `What projects are planned in Wamagana?`
- `Show road projects in Mweiga`
- `How much was allocated to Kianjogu Karaihu?`
- `What water projects are in Kabaru?` — an honest no-match response.
- `How much was spent in Wamagana?` — spending cannot be established from allocation records.

Use **Show more projects**, expand **View details & evidence**, and open the official source. The first row links to PDF page 278. Use **Explain this project** for a selected record or **Understand a budget** for a glossary definition. The **EN / SW** buttons switch the interface and repeat the current reply in the selected language without advancing results. Use **Check a claim** for an editable example with the complete comparison scope.

## Milestone 2: explanations and Kiswahili

No AI key or paid AI provider is needed. Fixed, reviewed templates supply definitions for allocation, recurrent expenditure, and development expenditure. Project explanations use the same reviewed records and citations as discovery. Source names, project names, amounts, years, and excerpts stay verbatim; only surrounding wording changes.

Browser: use **EN / SW**, **Understand a budget**, or **Explain this project**. WhatsApp: send `SW` or `EN`; `1` selects a project; `EXPLAIN` / `ELEZA` explains the selected record; `EXPLAIN 1` / `ELEZA 1` selects and explains a current result. `ZAIDI` means more results and `MSAADA` opens help.

Try `Explain recurrent expenditure`, `Matumizi ya kawaida ni nini?`, `Eleza mgao wa bajeti`, or `Onyesha miradi ya barabara katika Mweiga`. This is a bounded bilingual POC, not unrestricted translation. Unknown terms, unsupported languages, uncovered places, and spending/completion questions receive clarification or an evidence limitation.

The [wording review](docs/language-review.md) records wording approval and source references. The Treasury glossary reference supplies no project observations and does not expand milestone 4's reviewed dataset. Templates run without an AI service, so provider availability cannot interrupt explanations; an optional generative adapter has not been enabled.

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

The backend validates Twilio signatures against the configured public URL. It returns a single TwiML reply containing cited results. Duplicate incoming message IDs return an empty response for 24 hours. The adapter sends replies through TwiML without outbound Messaging REST requests. Actual messaging may incur provider charges.

Incoming senders may be phone numbers or [WhatsApp business-scoped user IDs](https://www.twilio.com/docs/whatsapp/key-concepts). Both formats are accepted after signature validation and hashed for temporary session lookup; raw sender identifiers are not persisted. Both sender formats are covered by automated regression tests; manual live checks passed for discovery, detail, pagination, and help.

## Restart the WhatsApp demo after a shutdown

Shutting down the laptop stops both the backend and the ngrok tunnel. Your saved `.env` remains on disk, but the app must load it again when starting. Follow these steps from the repository root; keep both terminal sessions running during testing and recording.

1. **Start ngrok in the first terminal** (already installed and authenticated for this demo):

   ```bash
   ngrok http 8000 --inspect=false --log=false
   ```

   Note the current HTTPS forwarding address shown by ngrok. It may differ from the previous session. The app becomes reachable after you start the backend below.

2. **Check the local settings.** Keep your existing credentials in `.env` and ensure `TRACK_MTAANI_WHATSAPP_ENABLED=1`. Set `TWILIO_WEBHOOK_URL` to the current ngrok HTTPS address followed by `/api/v1/whatsapp/webhook`. For example, replacing the placeholder host with your actual address:

   ```dotenv
   TRACK_MTAANI_WHATSAPP_ENABLED=1
   TWILIO_WEBHOOK_URL=https://YOUR-CURRENT-HOST.ngrok-free.app/api/v1/whatsapp/webhook
   ```

3. **Match the URL in Twilio.** On the **Try WhatsApp** page, open the **Sandbox settings** tab beside **Sandbox**. Set **When a message comes in** to the exact same full webhook URL, select **POST**, and save. The address must match `.env`, including the path and with no trailing slash. You do not need to send the appointment template in the guided setup.

4. **Start the backend in a second terminal, loading `.env`:**

   ```bash
   .venv/bin/python -m uvicorn src.main:app --env-file .env --host 127.0.0.1 --port 8000 --no-access-log
   ```

   If this app is already running, stop it with `Ctrl+C` in its terminal before restarting. Changes to `.env` take effect when the backend restarts. Using the browser-only command above without `--env-file .env` does not load your saved WhatsApp settings.

5. **Check connectivity and Sandbox membership.** Open `http://127.0.0.1:8000/health`, then the current ngrok HTTPS address with `/health` appended; both should return a JSON response with `"status":"ok"`. If WhatsApp says your number is not connected, send `join <your sandbox code>` using the current code shown in Twilio and wait for confirmation. [Sandbox membership expires after three days](https://www.twilio.com/docs/whatsapp/sandbox); rejoining is separate from restarting the app.

6. **Send a fresh `Kabaru` or `Wamagana` message.** Once project replies return, complete the [expanded live WhatsApp checks](docs/demo-runbook.md#expanded-live-whatsapp-check) before recording.

If the local health check works but the public one fails, check ngrok and its current address. If both work but WhatsApp stays silent, confirm that the Sandbox webhook was saved with POST, both webhook URLs match, and the backend was restarted with `.env` loaded. Health checks establish reachability; the fresh WhatsApp reply confirms the complete messaging flow.

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

Two official Nyeri PDFs are retained in `data/raw/`. All fifteen current project observations come from the programme budget; the second document is registered but has not supplied project answers. [Source inventory and review table](docs/data-sources.md) record this distinction. Processed and seed JSON files contain the reviewed facts and provenance. The importer checks the snapshot hashes and rejects unreviewed, uncited, or inconsistent records.

The [implementation plan](docs/implementation-plan.md) is the fixed submission scope. No additional features or app audio are planned. The [source adjustment approved September 16](docs/source-scope-decision.md) requires 15–30 reviewed records from at least one official project-level document, with additional documents explicitly identified as answer sources or context only. The fifteen reviewed records meet that dataset condition; they remain selected coverage, not a complete ward budget or independently corroborated evidence. M4 delivery checks remain open. Submission includes the working POC, GitHub repository, demo video, pitch deck, and written summary.

The repository is private and has no open-source license selected. Judge access must be arranged before submission.

## Documentation

For judging, start with the **judge walkthrough**, **submission summary**, and **PDF pitch deck**. The design and review documents below retain scope decisions and validation evidence; they are not separate submission uploads. The silent browser rehearsal is a supporting artifact, not the final narrated video.

| Document | Purpose |
| --- | --- |
| [Judge walkthrough](docs/judge-guide.md) | Reproducible demo steps, expected results, and access requirements |
| [Submission artifacts](output/README.md) | PDF deck and clearly labeled silent browser rehearsal |
| [M4 review](docs/m4-review.md) | Candidate source records, validation evidence, and outstanding delivery work |
| [Submission summary](docs/submission-summary.md) | Written summary draft and submission status |
| [Demo runbook](docs/demo-runbook.md) | Recording script, expected results, and judge-access checks |
| [Pitch deck](docs/pitch-deck.md) | Six-page PDF draft with editable slide copy and presenter notes |
| [Product requirements](docs/product-requirements.md) | Fixed product scope and acceptance criteria |
| [Frontend design](docs/frontend-design.md) | Screen design and interactions |
| [Architecture](docs/architecture.md) | Components, repository layout, and technical decisions |
| [Verification review](docs/verification-review.md) | Verdict wording, bounded claim format, and live checks |
| [Wording review](docs/language-review.md) | Reviewed English/Kiswahili definitions, wording, and test checklist |
| [Data and sources](docs/data-sources.md) | Pilot evidence, review records, and data model |
| [Trust model](docs/trust-model.md) | Factual integrity and evidence-scoped verification rules |
| [Privacy](docs/privacy.md) | Actual data handling and provider flows |
| [Limitations](docs/limitations.md) | Current gaps and prototype boundaries |
| [Implementation plan](docs/implementation-plan.md) | Milestone status and submission checklist |
