# Privacy

## Implemented data handling

The initial experience needs a message, a named locality, and a temporary reply destination. It does not require an account, precise GPS coordinates, identity documents, or demographic information.

The messaging provider handles the sender identifier (a number or business-scoped user ID) and message. The backend should use the destination only to reply, keep conversation state short-lived, and avoid persisting raw phone numbers or message bodies in application logs.

The web chat does not require a phone number. It sends messages directly to the application backend, using an opaque temporary session identifier. Keep browser conversation history in page memory, with no persistent chat archive or analytics for the POC. Hosting access logs may contain IP addresses; check their retention before public use. Use the same 30-minute session inactivity limit for both channels.

Implemented session default: expire language preference, result selections, and locality context after 30 minutes of inactivity. Expired context cannot be reused; cleanup runs when another conversation request arrives rather than on a background timer. Process shutdown clears in-memory context. The WhatsApp adapter keeps message IDs and expiry timestamps in SQLite for 24 hours and purges expired IDs on incoming requests. Sender mappings use a keyed SHA-256 digest in memory, expire after 30 minutes, and are bounded to 1,000 entries. These pseudonymous values should still be treated as personal data. Raw phone numbers and messages are not stored in the database. These time limits describe logical expiry, not a guarantee of physical erasure at that exact instant.

The browser uses no AI or messaging provider. The WhatsApp adapter remains disabled by default; the following provider flows apply when it is configured and enabled. Browser and WhatsApp session state contains selected record IDs, query filters, language preference, and the last templated response with its public evidence so a language switch can repeat it. For verification, the last response also includes parsed claim fields (project name, ward, year, stage, amount type, amount, and the supported extra clause) and its verdict; these expire with the same session. It does not retain a raw chat transcript. Use `--no-access-log` in the documented server command; check separate proxy/hosting logs before public use.

## Third-party flows

| Recipient | Intended data |
| --- | --- |
| WhatsApp and messaging provider | Sender/recipient identifiers, incoming messages, outgoing replies |
| ngrok, in the current local demo | Webhook requests and responses passing between Twilio and the app |
| Application host | Incoming request and temporary conversation state |
| AI provider | None enabled; the current POC makes no AI-provider calls |

The private local WhatsApp demo also uses an ngrok tunnel between Twilio and the app. That service handles webhook traffic. Provider retention and logging settings remain to be verified before a public pilot; application retention settings do not control WhatsApp, Twilio, or tunnel-provider storage. An AI adapter would require a separate data-handling review before use.

## First-use notice

The current English first-use WhatsApp notice in `src/api/whatsapp.py` is:

> Track-A-Mtaani is a POC using selected public documents. Messages pass through WhatsApp and Twilio. Avoid personal details. Temporary context expires after 30 minutes. Reply HELP for coverage and privacy.

Kiswahili replies use the manually reviewed translated notice. HELP/MSAADA names WhatsApp, Twilio, and the app, states that no AI provider is used, and explains temporary context and message-ID expiry. Allocation replies separately disclose that allocation is not proof of spending or completion.

The browser's expandable coverage/privacy area is available before the first message. It says browser messages go to this application, with no AI or WhatsApp forwarding, and that conversation history stays in page memory. Reloading starts a new browser conversation; it does not immediately erase the previous server session, which remains subject to the inactivity expiry above.

## Before public use

Verify provider request authentication, log redaction, session expiry, rate limits, actual data flows, and the first-use notice. Review the product with pilot-area users and agree who maintains sources and corrects errors. Public expansion requires fresh decisions about data retention, source updates, support, and applicable obligations.

See [limitations.md](limitations.md) for the POC boundaries.
