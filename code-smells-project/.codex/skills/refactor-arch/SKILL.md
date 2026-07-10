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
2. Turn each Phase 2 finding into a concrete code change before any cosmetic cleanup.
3. Apply the transformations in `references/refactor-playbook.md` for each smell found, including security, sensitive logs, and secure password hashing.
4. Preserve endpoints and observable behavior whenever possible.
5. Validate application boot and the main endpoints after the changes.

## Decision Rules

- Prioritize findings that affect security, integrity, authentication, sensitive data, or arbitrary execution.
- If two severities are in doubt, choose the higher one when there is risk of leak, data corruption, or access compromise.
- Do not refactor without concrete evidence. If the problem seems possible, confirm it in code before recording it in the report.
- Do not mix report writing and refactoring. Phase 2 must end before any edit.
- Phase 3 must not finish while critical Phase 2 findings still exist in code.

## When to Read Resources

- Read `references/project-analysis.md` at the start of any new project.
- Read `references/anti-pattern-catalog.md` to classify severity and detection signals.
- Read `references/audit-report-template.md` to standardize Phase 2 output.
- Read `references/mvc-guidelines.md` before moving code between layers.
- Read `references/refactor-playbook.md` when transforming a specific smell into MVC code.
