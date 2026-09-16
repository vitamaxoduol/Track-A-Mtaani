# Pitch deck copy

Six-slide draft for the hackathon submission, with an exported [PDF deck](../output/pdf/track-a-mtaani-pitch.pdf). The PDF uses the current fifteen-record coverage, an actual browser screenshot, and visible source limitations. All six rendered pages were visually checked. This Markdown contains the editable copy and presenter notes. The exported PDF matches the submission format; final judge-access details remain to be completed.

## 1. Track-A-Mtaani

Understand approved public-project allocations, with sources you can check.

Understand allocations. Inspect county budget decisions.

Transparency & Accountability · Andela × OSF hackathon

Speaker notes: Introduce the civic-information problem and the motivation for the project. Track-A-Mtaani is an independent individual submission; AI development tools assisted implementation.

## 2. The resident's question

“What was allocated to a project in my ward?”

The pilot's official programme budget spans 433 PDF pages. A resident needs the relevant project row and a clear explanation of what the figure means.

Residents can inspect what the county approved for a project and check allocation claims against the official record. This supports Transparency & Accountability through budget understanding and scrutiny of allocation decisions. An allocation alone cannot establish spending or completion.

Speaker notes: Use the retained official Nyeri programme budget as the concrete example. Resident testing is a planned validation step. Source: https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf

## 3. A working browser and WhatsApp POC

A ward query returns reviewed records with exact amounts and source pages.

English and Kiswahili explanations preserve the evidence.

The resident can open the cited document and inspect the record.

Speaker notes: Show the implemented browser and WhatsApp flows. Both use the same evidence service.

## 4. Evidence for one claim

Kianjogu Karaihu · Wamagana · FY 2026/2027

**KSh 3,000,000 allocated**

The approved programme budget supports this allocation on PDF page 291. A spending or completion claim needs evidence the current dataset does not contain.

Speaker notes: Demonstrate the exact supported query, then a spending claim. The verifier requires an exact project name, ward, financial year, document stage, amount type, and amount. Four verdicts express the evidence boundary; this is not unrestricted fact checking. Source: https://www.nyeri.go.ke/wp-content/uploads/2026/07/APPROVED-PBB-for-FY-2026-27.pdf#page=291

## 5. Access and trust

Text replies and a simple mobile layout keep the interaction small. Opening the full PDF uses more bandwidth.

Browser access needs no account or phone number. Temporary server context expires after 30 minutes of inactivity.

WhatsApp and Twilio process messaging data. No runtime AI provider receives queries or generates figures.

Speaker notes: Refer to docs/privacy.md for application/provider distinctions. Voice, citizen reports, GPS, and accounts are outside this POC. Fixed templates and reviewed records require no paid AI service. Messaging and hosting costs are separate.

## 6. Pilot scope and next validation

Fifteen reviewed allocations in Wamagana, Mweiga, and Kabaru, Nyeri County. One official document supplies project answers; a second PDF is registered as context only.

The prototype demonstrates allocation discovery, explanations, and bounded claim verification. It does not track actual expenditure, accept issue reports, provide public services, or establish project delivery on the ground.

Further development would begin with resident testing and a sustainable source-review process.

Speaker notes: This coverage describes commit `0762d53`; update it if the reviewed dataset changes. Resident testing will assess whether people can find an allocation, understand its limits, and inspect its source. Confirm POC/repository access and the video upload before submission. These future validation steps do not add features to the hackathon scope.
