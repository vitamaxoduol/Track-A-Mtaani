# Written submission summary

Submission copy covering the challenge track, information sources, trust and accuracy, and use of AI development tools.

## Track-A-Mtaani

**Track: Transparency & Accountability**

Track-A-Mtaani supports Transparency & Accountability by making approved public-project budget allocations accessible, understandable, and verifiable. Residents can inspect county budget decisions and check allocation claims against official sources. The pilot contains fifteen reviewed records in Wamagana, Mweiga, and Kabaru wards in Nyeri County, Kenya. One official document supplies project answers; a second PDF is registered as context only.

A resident enters a ward in a simple browser chat or sends it through WhatsApp. The POC returns reviewed project records with the allocation, financial year, official source, and PDF page. The resident can inspect a project's evidence and request a plain-language explanation in English or Kiswahili. The same reviewed facts serve both channels and languages.

For a claim about one named project, the verifier compares the stated amount against comparable reviewed evidence. It reports support, contradiction, partial support, or insufficient evidence. It requires the project, ward, year, document stage, amount type, and amount. A matching allocation cannot establish spending or completion.

The POC uses FastAPI, SQLite, and plain HTML, CSS, and JavaScript, with a Twilio WhatsApp adapter. Fixed, reviewed templates provide explanations; no AI service generates financial facts or receives runtime messages. AI development tools assisted implementation and testing of the participant's original idea.

Text replies keep the interaction small, although opening the full source PDF requires more bandwidth. Browser users need no account or phone number. Application conversation context expires after 30 minutes of inactivity; WhatsApp and Twilio also process messaging data.

This is a working prototype with selected reviewed allocations, not a complete project register. It does not track actual expenditure, accept issue reports, provide public services, or establish completion. Expenditure and completion claims require additional evidence. Its value is giving residents evidence they can inspect before making a claim or asking an informed follow-up question. Wider use would require resident testing, maintained source review, and durable hosting.

I developed the original project idea and used Codex to assist with implementation, testing, and documentation. Project answers use reviewed records and fixed templates; no generative AI service processes residents’ queries or generates financial figures.

## Submission details still to complete

Eligibility: Andela Learning Community membership and current residence in Kenya confirmed. Registration and exact deadline cutoff/timezone remain to be confirmed.

| Required item | Current location or status |
| --- | --- |
| Working POC | Local browser app and manually tested WhatsApp Sandbox; arrange judge access |
| GitHub repository | Private: https://github.com/vitamaxoduol/Track-A-Mtaani ; grant and test judge access |
| Short demo video | MP4 conversion and upload completed September 21, 2026. Playback verification remains pending. Accepted formats: MP4/MOV/WebM/AVI, at most 250 MB. See [recording/export notes](demo-runbook.md#submission-requirements) |
| Pitch deck | [Six-page PDF](../output/pdf/track-a-mtaani-pitch.pdf) and [editable copy](pitch-deck.md); PDF upload, maximum 100 MB |
| Written summary | Copy the project summary above into the form; it covers the requested topics and fifteen-record dataset |

Final checks: keep credentials private, verify judge access, upload the deliverables, and retain submission confirmation.
