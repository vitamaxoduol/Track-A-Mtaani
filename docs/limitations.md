# Limitations

The [implementation plan](implementation-plan.md) defines the fixed POC scope. These limitations must remain visible in the demo and submission.

## Product limits

- Coverage is deliberately small and manually reviewed; results are not a complete county project register.
- Records describe a document and reporting period, not necessarily the current situation on the ground.
- A budget allocation does not establish payment, construction progress, quality, or delivery.
- Claim verification requires the documented full claim format: exact project name, ward, financial year, document stage, amount type, and one amount. It compares only reviewed allocations in the dataset; it is not general fact checking. Missing scope or unrecognized clauses require a complete resubmission. Spending and completion cannot be inferred from an allocation.
- Translation needs human review, especially for financial terms.
- Official source links may move or become unavailable.
- Internet access and messaging-provider availability are required for the WhatsApp experience.
- Incoming attachments, precise location sharing, voice notes, and citizen reports are outside the initial scope. Unsupported input receives a clear text response.

- Audio responses are outside the submission scope.

## Current implementation status

- Browser discovery is working with fifteen manually reviewed records from Nyeri's approved FY 2026/2027 programme budget. Two source PDFs are retained, but only one supplies current project observations.
- Manual live WhatsApp discovery, detail, pagination, and help checks passed September 15, 2026. WhatsApp is disabled by default; the private demo uses a running local app and ngrok tunnel. Custom reply support was confirmed for this account and should not be assumed for every Twilio trial.
- English/Kiswahili templates and glossary explanations are implemented and manually reviewed. They cover fixed terms and simple query patterns, not unrestricted translation. Names and source excerpts stay in their original language. Manual live bilingual WhatsApp checks passed September 15, 2026. Bounded claim verification is implemented; verdict wording was approved and manual live verification checks passed September 16. Direct `Hakiki` language selection was corrected and confirmed live for supported and contradicted claims.
- Locality lookup is intentionally limited to the three pilot ward names. Arbitrary geographic names, fuzzy spelling, multiple financial years, and complex questions require clarification or are outside coverage.
- Browser refresh starts a new conversation; the old server context remains subject to inactivity expiry. A server restart clears in-memory context. Run one worker. The request limit is a simple application-wide 120 chat/webhook requests per minute for this small demo.
- WhatsApp deduplication retains message IDs for 24 hours, including across restarts. It is not an exactly-once delivery guarantee; loss of a webhook response before provider consumption can lose that reply.
- A temporary ngrok tunnel serves the local demo; persistent judge access has not been established. The GitHub repository is private with no open-source license. M4 includes draft submission copy, a six-page PDF pitch deck, and a recording runbook. The source-coverage adjustment was approved September 16: one document supplies project answers and the second remains context only. Expanded manual live WhatsApp checks passed September 20. The demo was converted to MP4 and uploaded September 21. Playback verification, verified judge access, and final submission confirmation remain outstanding.
- The full source PDF is approximately 40 MB; opening it requires substantially more bandwidth than reading the text results.

See [privacy.md](privacy.md) for actual application data handling and outstanding provider checks.
