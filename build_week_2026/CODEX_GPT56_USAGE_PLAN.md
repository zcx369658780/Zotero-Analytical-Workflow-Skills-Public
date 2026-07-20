# Codex and GPT-5.6 Usage Plan

## Status

This is a future-use plan only. No GPT-5.6 or API invocation is authorized or
performed in this scope-freeze gate.

## Responsibility split

### GPT-5.6 responsibilities

When a later gate authorizes model use, GPT-5.6 will:

- read only the bounded source excerpts and claims supplied in an approved
  fixture bundle;
- decompose compound claims into auditable material components;
- propose evidence-to-claim mappings using stable source identifiers;
- identify missing qualifiers, causal wording, scope expansion, and unresolved
  ambiguity;
- produce concise rationale candidates and human-review questions; and
- return structured proposals that remain subject to schema validation and
  deterministic policy.

GPT-5.6 will not retrieve private sources, access Zotero or Obsidian, decide
human verification, promote E3, overwrite output, or override deterministic
fail-closed rules.

### Codex responsibilities

In later explicitly authorized development gates, Codex will:

- implement the frozen input/output schemas and validators;
- implement the deterministic verdict and downgrade policy;
- build read-only/no-overwrite CLI behavior;
- create independently written fixtures and provenance records;
- build unit, golden, privacy, copyright, no-overwrite, and integration tests;
- connect model proposals to the deterministic policy boundary;
- keep secrets and local paths outside code, fixtures, logs, and commits;
- inspect diffs and stage only authorized paths;
- run and report reproducible checks; and
- maintain documentation and demonstration instructions.

Codex must not silently broaden product scope or treat model output as an
authoritative academic judgment.

## Decision authority

The responsibility chain is:

1. supplied source excerpts define the available evidence;
2. GPT-5.6 may propose semantic analysis;
3. schema validation rejects malformed or incomplete proposals;
4. deterministic rules apply mandatory verdicts and downgrades;
5. output remains `human_verified: false`; and
6. a human reviewer makes any final academic, grading, citation, or E3
   decision.

Neither GPT-5.6 nor Codex may skip a layer.

## Primary Codex session preservation

The primary Codex session used for the authorized ScholarTrace implementation
must be preserved through the Build Week development sequence so its task
history, decisions, checks, and boundaries remain reviewable.

At implementation start, the owner should record the primary Session ID in a
private run log or other owner-controlled record. It must not be added to the
public repository unless the owner explicitly approves publication.

Before the final feedback step:

- confirm the implementation work remains associated with the primary session;
- capture the `/feedback` Session ID exactly as displayed;
- retain that ID in the owner-controlled submission evidence record;
- do not fabricate or infer a missing ID; and
- do not publish private transcript content merely to prove session use.

## Planned model-use evidence

A later model-use gate should record, without credentials or private prompts:

- model name and invocation date;
- approved fixture identifiers and hashes;
- schema and policy versions;
- whether network access was enabled;
- deterministic rule outcomes;
- human-review status;
- primary Codex Session ID retention status; and
- `/feedback` Session ID retention status.

No API key, token, account detail, private path, or full private transcript may
appear in the repository.

## Failure behavior

If GPT-5.6 is unavailable, returns malformed output, omits evidence links,
introduces unsupported text, or conflicts with deterministic policy, the run
must fail closed. The system may report `unverifiable` or a validation error;
it must not guess, weaken a safety rule, or mark the output human verified.
