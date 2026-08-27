---
name: refactor-arch
description: Audit and refactor legacy codebases in three phases. Use when you need stack detection, architecture mapping, anti-pattern findings, exact line references, audit reports, or MVC-style backend refactors in Python/Flask, Node/Express, or similar stacks.
---

# Refactor Arch

## Overview

Use this skill to inspect a legacy codebase, produce a reproducible audit, and then refactor the project toward a cleaner MVC structure without breaking observable behavior.

## Phases

### Phase 1 - Analysis

1. Identify language, framework, database, entry point, and application domain.
2. Map the current architecture: routes, controllers, models, services, utilities, and coupling.
3. Record the summary before editing any file.
4. Read `references/project-analysis.md` for heuristics and signals.

### Phase 2 - Audit

1. Cross the code against `references/anti-pattern-catalog.md`.
2. Classify each finding with severity, file, and exact line references.
3. Generate the report using `references/audit-report-template.md`.
4. Stop and ask for explicit confirmation before modifying any file.

### Phase 3 - Refactor

1. Use `references/mvc-guidelines.md` as the structural target.
2. Create a remediation checklist that maps every Phase 2 finding to a concrete change and an observable validation. Keep the finding's severity, file, and line reference in that checklist.
3. Apply the matching transformations in `references/refactor-playbook.md` before any cosmetic cleanup. A finding is not resolved merely because related configuration was added: the running route or execution path must consume it.
4. Preserve endpoints and observable behavior whenever possible; a new security control may intentionally change an unauthorized request from success to `401` or `403`.
5. Validate application boot and the main endpoints after the changes. For every authentication or authorization finding, test both a rejected request without valid credentials and a successful request with valid credentials; verify the protected handler is not called for the rejected request.
6. Re-run the Phase 2 audit after the change set. Do not declare Phase 3 complete while any CRITICAL or HIGH finding from the remediation checklist remains, unless the user explicitly accepts it as deferred and the final report records the reason.

## Decision Rules

- Prioritize findings that affect security, integrity, authentication, sensitive data, or arbitrary execution.
- If two severities are in doubt, choose the higher one when there is risk of leak, data corruption, or access compromise.
- Do not refactor without concrete evidence. If the problem seems possible, confirm it in code before recording it in the report.
- Do not mix report writing and refactoring. Phase 2 must end before any edit.
- Phase 3 must not finish while critical Phase 2 findings still exist in code.
- A configured secret, role, or token does not count as a mitigation until it is enforced by the relevant route, middleware, or service boundary.

## When to Read Resources

- Read `references/project-analysis.md` at the start of any new project.
- Read `references/anti-pattern-catalog.md` to classify severity and detection signals.
- Read `references/audit-report-template.md` to standardize Phase 2 output.
- Read `references/mvc-guidelines.md` before moving code between layers.
- Read `references/refactor-playbook.md` when transforming a specific smell into MVC code.
