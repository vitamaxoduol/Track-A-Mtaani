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

- Audio responses are excluded from this submission; the `speech.py` filename in the supplied layout is reserved only.

## Current implementation status

- Browser discovery is working with ten owner-reviewed records from Nyeri's approved FY 2026/2027 programme budget. Two source PDFs are retained, but only one supplies current project observations.
- The owner confirmed live WhatsApp discovery, detail, pagination, and help replies on September 15, 2026. WhatsApp is disabled by default; the private demo uses a running local app and ngrok tunnel. Custom reply support was confirmed for this account and should not be assumed for every Twilio trial.
- English/Kiswahili templates and glossary explanations are implemented and owner-reviewed. They cover fixed terms and simple query patterns, not unrestricted translation. Names and source excerpts stay in their original language. The owner confirmed successful live bilingual WhatsApp checks on September 15, 2026. Bounded claim verification is implemented; the owner approved verdict wording and live verification checks on September 16. Direct `Hakiki` language selection was corrected and confirmed live for supported and contradicted claims.
- Locality lookup is intentionally limited to the three pilot ward names. Arbitrary geographic names, fuzzy spelling, multiple financial years, and complex questions require clarification or are outside coverage.
- Browser refresh or a server restart clears conversation context. Run one worker. The request limit is a simple application-wide 120 chat/webhook requests per minute for this small demo.
- WhatsApp deduplication retains message IDs for 24 hours, including across restarts. It is not an exactly-once delivery guarantee; loss of a webhook response before provider consumption can lose that reply.
- A temporary ngrok tunnel serves the local demo; no persistent hosting, GitHub publication, pitch deck, video, or written submission summary has been completed. The license remains the owner's decision.
- The full source PDF is approximately 40 MB; opening it requires substantially more bandwidth than reading the text results.

See [privacy.md](privacy.md) for proposed data handling.
