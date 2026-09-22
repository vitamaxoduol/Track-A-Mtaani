# Judge walkthrough

Track-A-Mtaani is an individual hackathon POC for Transparency & Accountability. This guide describes the fifteen-record pilot at commit `0762d53`. All project answers come from Nyeri's approved FY 2026/2027 programme budget; the second retained budget PDF is registered as context only.

## Access

The [repository](https://github.com/vitamaxoduol/Track-A-Mtaani) is public and can be accessed without an invitation. Follow the setup below to run the browser POC locally; a live hosted demonstration still requires a separate access arrangement.

Browser reproduction needs Python 3.12+ and the dependencies in `requirements.txt`. Follow [README setup](../README.md#run-locally) from the repository root. No `.env`, Twilio credentials, AI key, or paid AI service is needed for the browser demonstration. Startup imports the reviewed seed and checks the retained source snapshots. Internet is needed to install dependencies and open live official links; record lookup itself uses local data.

The WhatsApp demonstration uses a configured Twilio Sandbox. An arranged demonstration requires current Sandbox join instructions and a running backend/tunnel. Credentials remain private. The temporary tunnel is not a persistent deployment.

## Browser walkthrough

| Action | Expected result |
| --- | --- |
| Ask `Wamagana` | First three of nine reviewed Wamagana records, each with source and allocation caution |
| Select **Show more projects** twice | Final page: Kaiguri Gwa Karuga, Kihuro rd, and Kanyamati |
| Expand a project's evidence | Exact source excerpt, amount heading, year, and linked official PDF page |
| Select **Explain this project**, then **SW** | Kiswahili explanation with unchanged amount and citation |
| Ask `Water projects in Mweiga` | Supporting water projects, KSh 2,000,000 allocated, PDF page 282 |
| Ask `Water projects in Kabaru` | Honest no-match response within selected coverage |

To inspect claim verification, switch to EN and send:

```text
Verify Kianjogu Karaihu in Wamagana FY 2026/2027 approved allocation KSh 3,000,000
```

This allocation matches the reviewed source on PDF page 291. Change the amount to `2,000,000` for a contradiction limited to the available source. Append `and completed` to the matching allocation for partial support. Replace `allocation` with `spending` for insufficient evidence.

The complete claim format is intentional: exact project name, ward, financial year, document stage, amount type, and amount. The verifier does not establish arbitrary real-world claims or infer missing information from a prior query.

## Materials and limits

See the [written summary](submission-summary.md), [PDF pitch deck](../output/pdf/track-a-mtaani-pitch.pdf), and [browser rehearsal](../output/video/track-a-mtaani-browser-rehearsal.webm). The rehearsal is a silent browser recording, not live WhatsApp or a production service. The final narrated video is a separate submission-form upload; the silent rehearsal does not replace it. Accepted formats and size limits are recorded in the [demo runbook](demo-runbook.md#submission-requirements).

The pilot covers fifteen selected allocations across Wamagana, Mweiga, and Kabaru, not a full county or ward register. Allocations do not prove spending or completion. English/Kiswahili explanations use fixed reviewed wording; no runtime AI provider generates financial figures. The participant originated the idea and used AI tools to assist software development. See [privacy](privacy.md) and [limitations](limitations.md).
