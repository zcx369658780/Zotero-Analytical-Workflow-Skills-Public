# New Work Since 2026-07-13

## Time and provenance boundary

This record uses 2026-07-13 as the competition-period reporting boundary and
the protected tag `pre-build-week-2026-public-baseline` as the immutable
repository-content boundary.

At the start of this gate, the only commits after the protected tag were:

| Commit | Classification |
|---|---|
| `2aa1232293fdfb9763ea2c2734c75e217d715a21` | Task specification for upstream permission and mixed-licensing integration |
| `6c1c6caa93318f08cff666d94de26da42447ef59` | Permission, notice, attribution, and mixed-licensing integration |

## Permission integration is not the judged feature

Commit `6c1c6caa93318f08cff666d94de26da42447ef59` added or updated legal,
notice, confirmation, attribution, and completion-report documentation. It
made the repository's licensing boundary explicit. It did not implement
ScholarTrace and must not be represented as the new Education-track product
feature.

The README change in that commit was also a licensing disclosure, not product
functionality.

## New work created by this planning gate

The competition-period work in this gate is documentation-only:

- a reproducible pre-existing/new-work boundary;
- a frozen ScholarTrace MVP scope;
- a lawful fixture and evaluation plan;
- a Codex and GPT-5.6 responsibility plan;
- a readiness decision; and
- a gate report and governing task file.

These documents define future work but contain no implementation.

## Work not yet performed

As of this scope freeze, none of the following exists as competition-period
implementation:

- ScholarTrace Python code or CLI;
- input/output schema files;
- deterministic verdict engine;
- demonstration fixtures;
- fixture provenance manifest;
- unit, integration, golden, or privacy tests;
- GPT-5.6 invocation or model-generated audit output;
- demo recording, deployment, release, or submission.

## Future judged-work boundary

Future commits may be described as independently developed Build Week work
only when they are created after this scope freeze, remain outside the five
separately licensed upstream-derived counterparts, and are authorized by a
later task.

The next authorized work should begin with synthetic fixture content, explicit
schemas, and a deterministic fail-closed pipeline. Model integration,
submission assets, and deployment require later gates.
