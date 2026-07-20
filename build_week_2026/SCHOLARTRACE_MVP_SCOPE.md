# ScholarTrace MVP Scope

## Product definition

ScholarTrace / Evidence Gate is an independently developed educational
claim-evidence audit extension. It helps learners see whether a written claim
is actually supported by the evidence supplied with it, which qualifiers were
lost, and when a human must review the result.

It is not a feature that existed at
`pre-build-week-2026-public-baseline`. Existing Zotero and Obsidian workflows
provide context and safety conventions only.

## Target users

Primary users:

- university students learning evidence-based academic writing;
- thesis and capstone students reviewing claims before submission; and
- instructors demonstrating how claim strength changes when evidence,
  causality, sample, period, or scope is misrepresented.

Secondary users are research assistants and educators preparing bounded,
lawfully reusable teaching examples.

## Education-track narrative

The Education-track story is: "turn invisible evidence mistakes into a
teachable audit." A learner supplies a bounded claim set and approved source
excerpts. ScholarTrace produces traceable verdicts and explanations showing
why a claim is supported, incomplete, too strong, unsupported, or impossible
to verify. The learner, not the machine, makes the final academic judgment.

The value is formative feedback and research-literacy training, not automated
grading or authoritative fact checking.

## Input contract

The future MVP must accept a read-only structured case bundle with:

- `case_id` and a schema version;
- a title and short educational scenario;
- source provenance and reuse status;
- one or more supplied source excerpts with stable `source_id` values;
- a locator for each excerpt that does not expose a private path;
- explicit source limitations such as sample, period, geography, population,
  method, and study scope where applicable; and
- one or more claims with stable `claim_id`, claim text, and optional claim
  type.

Inputs must contain only independently written synthetic sources or material
whose reuse is documented as lawful. Raw PDFs, private Zotero records,
unpublished research, purchased data, and real-vault paths are invalid inputs.

## Output contract

The future MVP must emit both structured machine-readable output and a
human-readable audit report. For every claim, output must include:

- `claim_id`;
- exactly one verdict from the frozen taxonomy;
- cited `source_id` values and supplied locators used in the decision;
- a concise rationale;
- missing or altered qualifiers;
- deterministic rule flags;
- unresolved questions and a human-review reason when applicable; and
- `human_verified: false`.

The run-level output must include the input case identifier, schema version,
tool version, read-only/no-overwrite status, and provenance summary. Machine
output must not set E3 or `citation_eligible: true`.

## Frozen verdict taxonomy

| Verdict | Definition |
|---|---|
| `supported` | Every material part of the claim, including strength and limiting conditions, is directly supported by supplied evidence. |
| `partially_supported` | A separable core is supported, but another material component is absent, incomplete, or narrower than stated without making the whole claim affirmatively stronger than the evidence. |
| `unsupported` | Supplied evidence is available and relevant enough to assess, but it provides no support for the claim or contradicts its material conclusion. |
| `overstated` | The claim strengthens certainty, magnitude, causality, generality, or scope beyond what the supplied evidence permits. |
| `unverifiable` | The required evidence, locator, provenance, or context is missing, inaccessible, ambiguous, or insufficient to make a defensible assessment. |

## Deterministic fail-closed rules

The policy layer, not a model preference, controls the final verdict:

1. Missing required source text, provenance, or locator forces
   `unverifiable`.
2. Evidence present but unrelated, silent, or contradictory on the material
   conclusion forces `unsupported`.
3. Causal language supported only by correlational or observational wording
   forces `overstated`.
4. Omission of sample, period, population, geography, or scope is
   `overstated` when it materially broadens applicability or certainty.
5. An incomplete compound claim is `partially_supported` only when supported
   and unsupported components can be separated without disguising stronger
   causal, general, or certainty language.
6. `supported` is allowed only when all material components and qualifiers are
   covered by identified source excerpts.
7. Conflicting evidence or unresolved ambiguity cannot be silently averaged;
   it becomes `unverifiable` with a human-review flag.
8. Model output may propose mappings and rationales but cannot override a
   deterministic downgrade.
9. Every machine result remains `human_verified: false`; no automatic E3
   promotion is allowed.
10. Existing outputs are never overwritten. A repeated run must fail closed or
    write to a new explicitly chosen demonstration output location.

## Human-review boundary

Human review is mandatory before a result is used for grading, publication,
citation approval, E3 promotion, or correction of a real research note. A
reviewer may confirm or revise a verdict, but the review action must be
explicit, attributable, and separate from machine output.

ScholarTrace must present uncertainty and rule triggers. It must not represent
itself as a substitute for reading the source or exercising academic judgment.

## Privacy and copyright

- Demonstrations use independently written synthetic sources by default.
- Lawfully reusable material requires a recorded source, license, version, and
  allowed use.
- No private Zotero data, attachments, local APIs, real Obsidian vaults,
  unpublished research, purchased datasets, copyrighted paper PDFs, or
  Xiaohongshu screenshots may be used.
- No direct writing to a real Obsidian vault is permitted.
- Inputs and outputs must not contain credentials, private paths, or personal
  contact details.

## Three-minute demonstration path

1. `0:00-0:25` - Show the protected pre-existing baseline and identify
   ScholarTrace as new, independently developed work.
2. `0:25-0:50` - Open a synthetic case bundle and point out claims, excerpts,
   provenance, and limitations.
3. `0:50-1:40` - Run the future read-only audit and display all five verdict
   categories, emphasizing deterministic rule flags.
4. `1:40-2:25` - Focus on three teaching moments: unsupported conclusion,
   correlation claimed as causation, and omitted limiting conditions.
5. `2:25-2:50` - Show `human_verified: false`, no E3 promotion, no overwrite,
   and the human-review action boundary.
6. `2:50-3:00` - Close with the Education-track outcome: learners can inspect
   exactly why claim wording exceeds evidence.

## Explicit non-goals

The MVP will not:

- search for or download papers;
- parse PDFs or access Zotero/Obsidian data;
- write to real notes or vaults;
- generate citations or certify publication readiness;
- automatically grade students;
- make legal, medical, or policy decisions;
- infer missing evidence as fact;
- promote evidence to E3;
- provide a general-purpose RAG or literature-review platform;
- support multi-user hosting, deployment, accounts, or billing; or
- create submission, release, video, or Devpost assets in this gate.
