# Demo and judge-access runbook

Demo scope: fifteen reviewed records, browser and WhatsApp discovery, English/Kiswahili explanations, official citations, and bounded claim verification. Submission completed September 21, 2026. See [M4 status](m4-review.md) for delivery evidence and subsequent validation.

The [59-second silent browser rehearsal](../output/video/track-a-mtaani-browser-rehearsal.webm) covers the browser flow. The final demo also includes narration, WhatsApp, and source inspection.

## Submission requirements

- Project title, challenge track, current country, and GitHub repository URL.
- Demo video: MP4, MOV, WebM, or AVI, up to **250 MB**.
- Pitch deck: **PDF only**, up to **100 MB**.
- Written summary: cover the track, information sources, approach to trust and accuracy, and use of AI tools.

The three-minute script is a rehearsal target. A maximum video duration and exact deadline cutoff/timezone have not been established. The hackathon also requires a working POC, although the form collects four submission items.

For MKV recordings, export MP4 using **OBS → File → Remux Recordings**. Check video and audio playback before uploading. See the [OBS recording guide](https://obsproject.com/kb/standard-recording-output-guide).

## Before recording

1. Follow the README setup in a clean checkout. Run the tests and JavaScript syntax check. Keep `.env` outside Git.
2. Start a single app worker with access logging disabled. For WhatsApp, keep the configured tunnel running and confirm the exact incoming-message webhook still matches its public URL.
3. Open the browser chat and the official programme budget at PDF pages 278 and 291. Load the large PDF before the recording; disclose if you show a local snapshot during an outage.
4. On the joined test phone, confirm `Wamagana`, `1`, `MORE`, `SW`, and `MSAADA`. Use a fresh browser session for the video.
5. Close credential screens and unrelated chats. Show only the relevant demo conversation. Turn off notifications and confirm microphone/screen capture work.

## Recording script

| Time | Show | Suggested narration |
| --- | --- | --- |
| 0:00–0:25 | App title and coverage | “I built Track-A-Mtaani to help residents understand the public-project allocations recorded for their communities. This pilot uses selected reviewed records from Nyeri County.” |
| 0:25–1:00 | Browser: `Wamagana`; select the first record. Briefly show the same WhatsApp lookup. | “A ward name returns project allocations. Both channels use the same evidence service.” |
| 1:00–1:30 | Hubuini ECDE details and programme budget PDF page 278 | “This record shows KSh 700,000 allocated for FY 2026/2027. The page link lets me check the figure. It does not tell me whether money was spent or work completed.” |
| 1:30–1:55 | Switch to SW and explain the selected project | “Kiswahili changes the explanation while preserving the source names, amount, and citation.” |
| 1:55–2:30 | Switch EN. Paste the supported claim below, then replace `allocation` with `spending`. | “The allocation matches the reviewed source. The spending claim has insufficient evidence. The app makes that limit visible.” |
| 2:30–3:00 | Coverage/help and closing statement | “This is a small, working POC. Reviewed records provide the facts, and fixed reviewed templates explain them. AI tools helped me develop the software. The next validation step is testing the experience with residents.” |

Supported claim:

```text
Verify Kianjogu Karaihu in Wamagana FY 2026/2027 approved allocation KSh 3,000,000
```

Insufficient-evidence claim:

```text
Verify Kianjogu Karaihu in Wamagana FY 2026/2027 approved spending KSh 3,000,000
```

For a longer rehearsal, change the allocation to `2,000,000` for a contradiction, append `and completed` to the matching allocation for partial support, and check the direct Kiswahili query:

```text
Hakiki Kianjogu Karaihu katika Wamagana mwaka wa fedha 2026/2027 iliyoidhinishwa mgao KSh 3,000,000
```

Expected source amount stays KSh 3,000,000, with programme budget PDF page 291. Changing the user's claim must not change the source evidence.

## Expanded live WhatsApp check

Manual live checks passed on September 20, 2026; see [M4 review](m4-review.md). Repeat this sequence after changes to code, data, or messaging configuration.

| Send | Expected result |
| --- | --- |
| `EN`, then `Wamagana`, then `MORE` twice | Third page shows records 7–9 of 9: Kaiguri Gwa Karuga (KSh 1,000,000, page 291), Kihuro rd (KSh 2,000,000, page 292), Kanyamati (KSh 2,400,000, page 292) |
| `1`, then `EXPLAIN` | Kaiguri Gwa Karuga details and explanation preserve the amount, year, citation, and allocation limitation |
| `Mweiga`, then `3`, then `SW`, then `ELEZA` | Supporting water projects: KSh 2,000,000, page 282; Kiswahili explanation preserves the source facts |
| `Hakiki Jambo Zaina Box Culvert katika Kabaru mwaka wa fedha 2026/2027 iliyoidhinishwa mgao KSh 4,000,000` | Supported verdict in Kiswahili, KSh 4,000,000 source allocation, page 296 |
| `MSAADA` | Fifteen reviewed records across three wards, one project-answer source, second document registered only |

Record the test date, device, dataset/commit, and pass/fail result in [M4 review](m4-review.md) after checking the replies. No phone number or private message identifier is needed. Confirm any correction before recording.

## Rehearsal acceptance

For the review-date and follow-up additions, check `Wamagana` → `1` → `SW` → `ELEZA` in WhatsApp and the corresponding browser flow. The record review date should remain `2026-09-14`; the guidance should switch languages without changing evidence. Check `Mweiga` → `3` for the later `2026-09-16` review date. A full verification claim should retain its verdict and show the same guidance when project evidence is available. Manual live checks and wording review for these additions passed September 21, 2026, supplementing the September 20 results. Repeat this sequence after relevant changes.

- Discovery, selection, and pagination work in a desktop browser and at 390px/320px widths.
- English/Kiswahili replies retain amounts, years, and links. No draft-review notice appears for approved wording.
- Unknown places, absent records, unsupported spending, and wrong-year claims disclose limits.
- Each new reviewed record can be opened, explained, and rendered in WhatsApp without losing its citation or exceeding the reply limit.
- HELP/MSAADA states the actual dataset and active source roles after any import.
- Slow/failed browser requests offer a working retry without duplicating results.
- Official page links open. Any fallback to a local PDF snapshot is identified during the demo.

Record the test date, dataset/commit, device, and failures. Track manual live results separately from automated webhook tests. Label recorded fallback segments clearly.

## Judge access and submission

The [GitHub repository](https://github.com/vitamaxoduol/Track-A-Mtaani) is public. Unauthenticated repository access was verified September 22, 2026; judges do not need collaborator invitations. Repository access is separate from access to the running POC.

Document and test the demo access arrangement before delivery. A local app with a temporary tunnel requires the laptop, backend, and tunnel to remain running.

Check file formats, sizes, playback, and judge access before submission. The announced deadline was September 21, 2026; deadline requirements are confirmed in the completed submission checklist. Retain the submission confirmation.
