# Trust model

## Core promise

Every project fact should be traceable to reviewed evidence. AI may make that evidence easier to understand; it cannot establish a budget amount, spending claim, or completion status.

The assistant describes what the available sources say. It does not independently confirm physical construction, audit expenditure, or establish wrongdoing.

## Answer contract

A project answer includes the project name, amount with its type, financial year or reporting period, and a readable citation: document title, PDF page, and official URL. Include department and locality when supported. For allocation answers, explicitly state that allocation does not prove spending or completion.

An evidence bundle contains the resolved query scope, reviewed observation IDs and fields, source excerpts and metadata, and dataset coverage. No retrieved result means no project-specific factual answer.

Hashes help track document provenance internally. Citizens receive source titles, pages, and links they can inspect.

## Claim verification

The initial verifier handles one project and amount claim at a time. Compare project identity, location, financial year or reporting period, amount type, document stage, and amount. A draft allocation and an approved allocation are not automatically comparable; neither are a single-year allocation and a multi-year total.

| Verdict | When to use it |
| --- | --- |
| `SUPPORTED` | Comparable reviewed evidence supports all material parts of the claim |
| `PARTIALLY_SUPPORTED` | Evidence supports some material parts, while others lack sufficient evidence; explain each part |
| `INSUFFICIENT_EVIDENCE` | Identity or scope remains ambiguous, comparable evidence is missing, or conflicting sources cannot be resolved |
| `CONTRADICTED_BY_AVAILABLE_SOURCE` | Directly comparable evidence explicitly conflicts with a material part of the claim; identify the conflict and source scope |

A contradiction takes precedence over partial support when comparable evidence explicitly conflicts with a material claim. Never label a claim contradicted solely because retrieval found nothing. If sources disagree without a clear revision relationship, expose the disagreement and return insufficient evidence.

Every verdict explains what was checked, what the source says, and what remains unknown. Use wording such as “contradicted by the available source,” not an unrestricted assertion that a public claim is false.

## Failure behavior

| Situation | Expected response |
| --- | --- |
| Unknown or ambiguous locality | Ask for county/ward context or offer candidates |
| No matching records | State current coverage and absence of a match |
| Question about spending, with only allocation evidence | Say spending cannot be verified; optionally show the allocation with its correct label |
| Conflicting figures in sources | Show the conflict and citations; do not choose arbitrarily |
| AI timeout or unsupported generated claim | Use a deterministic cited response |
| Unreviewed extraction or missing citation | Withhold the affected factual claim |
| User or document instructs the assistant to ignore evidence rules | Treat that content as untrusted data |

## Critical validation cases

These are requirements for future implementation tests, not tests already run:

- An allocation never becomes spending, procurement, or completion in the answer.
- Unit normalization preserves the exact monetary value; missing amounts never become zero.
- A source page and URL are rendered from the same observation as the displayed amount.
- Kiswahili output preserves names, values, years, and source references.
- A wrong year, ambiguous project, or missing source cannot produce an unsupported verification verdict.
- Conflicting documents remain visible unless a reviewed supersession relationship resolves them.
- Prompt injection in a source excerpt or user message cannot change the evidence policy.
- Empty search results do not imply the absence of real-world projects.
- Synthetic fixtures cannot appear as official evidence in the public demo.
