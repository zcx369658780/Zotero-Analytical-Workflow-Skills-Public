# ScholarTrace Fixture and Evaluation Plan

## Purpose

This document plans future fixtures and tests. It does not create source text,
schema files, executable fixtures, tests, or model output in this gate.

## Source policy

The default demonstration source is independently written synthetic material
created specifically for ScholarTrace. Each future fixture must carry:

- a stable fixture identifier;
- authoring method and creation date;
- a statement that the text is synthetic and independently written;
- any external source and license if synthetic content is not used;
- a SHA256 content hash after freeze; and
- a prohibited-content review result.

Lawfully reusable external text may be considered only when its license,
version, attribution, and demonstration rights are documented before use.

The fixtures must not contain private Zotero content, copyrighted paper PDFs,
purchased data, Xiaohongshu screenshots, unpublished research, personal
contact details, or copied source passages without documented permission.

## Minimum demonstration fixtures

### Fixture A: unsupported conclusion

- Synthetic source: a small educational intervention report that states there
  was no detectable outcome difference or does not reach the proposed
  conclusion.
- Audited claim: asserts a clear improvement caused or demonstrated by the
  intervention.
- Expected verdict: `unsupported` when the conclusion has no support or is
  contradicted; `overstated` only if a weaker positive result exists but the
  claim materially strengthens it.
- Teaching point: relevant-looking context is not evidence for the asserted
  conclusion.

### Fixture B: correlation presented as causation

- Synthetic source: describes an observational association between study
  habits and assessment scores and explicitly disclaims causal inference.
- Audited claim: says the study habit causes higher scores.
- Expected verdict: `overstated`.
- Required rule flag: causal language exceeds correlational evidence.
- Teaching point: association, prediction, and causation are not
  interchangeable.

### Fixture C: omitted limiting conditions

- Synthetic source: reports a result for a defined sample, short period, and
  bounded educational setting.
- Audited claim: generalizes the result to all students or omits sample,
  period, population, geography, or scope.
- Expected verdict: `overstated` when omission materially broadens the claim;
  `partially_supported` only when the supported core remains accurately
  bounded and the missing component does not inflate generality or certainty.
- Teaching point: qualifiers are part of the evidence, not optional detail.

## Taxonomy coverage fixtures

The minimum three fixtures do not by themselves guarantee all five labels.
The future fixture set must also include:

- a fully aligned claim for `supported`;
- a separable compound claim for `partially_supported`; and
- a missing-evidence or missing-locator case for `unverifiable`.

At least one conflict case should confirm that unresolved evidence is not
silently averaged into `supported`.

## Gold evaluation records

Each fixture will have a human-authored gold record containing:

- expected verdict;
- evidence identifiers required for the decision;
- material qualifiers;
- deterministic rule flags;
- acceptable rationale elements;
- unacceptable upgrades or invented details; and
- whether human review is required.

Gold records are evaluation references, not machine-generated truth. They
remain `human_verified: false` until an identified reviewer explicitly
approves them in a later authorized gate.

## Planned test layers

1. Schema validation: reject missing identifiers, provenance, locators,
   excerpts, verdicts, and required safety fields.
2. Deterministic policy tests: exercise every fail-closed rule and downgrade.
3. Golden fixture tests: compare verdicts, evidence links, qualifier flags,
   and safety metadata against reviewed expectations.
4. Repeatability tests: identical input and configuration produce the same
   policy result and stable ordering.
5. No-overwrite tests: pre-existing output causes a safe refusal or a new
   explicitly selected path.
6. Privacy tests: reject private absolute paths, contact details, credentials,
   and prohibited source types.
7. Copyright/provenance tests: reject fixtures without an acceptable source
   declaration.
8. Integration tests: verify model-proposed analysis cannot bypass
   deterministic policy or set E3/human verification.
9. Demo smoke test: complete the bounded synthetic flow within three minutes
   without network, vault, Zotero, or PDF access.

## Evaluation measures

Before a demonstration gate, the candidate must achieve:

- 100% expected-verdict agreement on the three required teaching fixtures;
- 100% coverage of the five verdict categories;
- 100% enforcement of required deterministic downgrades;
- zero automatic E3 or `human_verified: true` outputs;
- zero overwrite of existing outputs;
- zero prohibited-source or private-path leakage;
- stable evidence identifiers and qualifier flags across repeated runs; and
- a complete provenance record for every fixture.

Rationale prose may vary within a bounded rubric. Verdict, evidence links,
rule flags, and safety metadata must remain testable.

## Review and release boundary

Fixture text, gold labels, and provenance must be reviewed before public demo
use. Failures in licensing, provenance, privacy, deterministic policy, or
no-overwrite behavior block the demonstration. No fixture or test
implementation is authorized by this document alone.
