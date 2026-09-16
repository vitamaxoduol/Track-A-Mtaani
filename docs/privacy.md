# Privacy

## Implemented data handling and planned provider use

The initial experience needs a message, a named locality, and a temporary reply destination. It does not require an account, precise GPS coordinates, identity documents, or demographic information.

The messaging provider handles the sender identifier (a number or business-scoped user ID) and message. The backend should use the destination only to reply, keep conversation state short-lived, and avoid persisting raw phone numbers or message bodies in application logs.

The web chat does not require a phone number. It sends messages directly to the application backend, using an opaque temporary session identifier. Keep browser conversation history in page memory, with no persistent chat archive or analytics for the POC. Hosting access logs may contain IP addresses; check their retention before public use. Use the same 30-minute session inactivity limit for both channels.

Implemented session default: expire language preference, result selections, and locality context after 30 minutes of inactivity. The WhatsApp adapter keeps message IDs and expiry timestamps in SQLite for 24 hours. It purges expired IDs on incoming requests. Sender mappings use a keyed SHA-256 digest in memory, expire after 30 minutes, and are bounded to 1,000 entries. These pseudonymous values should still be treated as personal data. Raw phone numbers and messages are not stored in the database.

The browser uses no AI or messaging provider. The WhatsApp adapter remains disabled by default; the following provider flows apply when it is configured and enabled. Browser and WhatsApp session state contains selected record IDs, query filters, language preference, and the last templated response with its public evidence so a language switch can repeat it. For verification, the last response also includes parsed claim fields (project name, ward, year, stage, amount type, amount, and the supported extra clause) and its verdict; these expire with the same session. It does not retain a raw chat transcript. Use `--no-access-log` in the documented server command; check separate proxy/hosting logs before public use.

## Third-party flows

| Recipient | Intended data |
| --- | --- |
| WhatsApp and messaging provider | Sender/recipient identifiers, incoming messages, outgoing replies |
| Application host | Incoming request and temporary conversation state |
| AI provider, if enabled | Minimal sanitized query and selected public evidence; no phone number or session identifier |

Do not forward raw messages to an AI provider when a structured intent and selected evidence suffice. Provider retention and logging settings remain to be verified before a public pilot. These are proposed engineering choices, not a statement of legal compliance.

## First-use notice

Suggested copy to refine before testing:

> Track-A-Mtaani is a prototype using selected public documents. It cannot confirm that money was spent or work completed unless the cited evidence says so. Messages pass through our messaging service; AI explanations, when enabled, use selected evidence and limited query text. Please avoid sharing sensitive personal information. Reply HELP for coverage and data-handling details.

The implemented HELP response should name the providers actually enabled and explain the actual session retention policy.

For the web chat, adapt the notice to say that messages go to the application backend and, if enabled, limited query text and evidence go to the AI provider. Do not imply browser messages pass through WhatsApp. Make the notice available from the coverage/help area before the first message.

## Before public use

Verify provider request authentication, log redaction, session expiry, rate limits, actual data flows, and the first-use notice. Review the product with pilot-area users and agree who maintains sources and corrects errors. Public expansion requires fresh decisions about data retention, source updates, support, and applicable obligations.

See [limitations.md](limitations.md) for the POC boundaries.
