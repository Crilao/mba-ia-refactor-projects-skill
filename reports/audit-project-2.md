# Architecture Audit Report

Project: ecommerce-api-legacy
Stack: Node.js + Express + sqlite3
Files analyzed: 9
Lines analyzed: ~350
Domain: LMS API with checkout, enrollment, payment, and administrative reporting

## Phase 1 — Architecture Summary

- Entry point: `ecommerce-api-legacy/src/app.js`; the composition root is `src/appFactory.js`.
- HTTP routes are separated from controllers, services, repositories, configuration, and database access.
- SQLite is created in memory and seeded during every application boot.
- `config.js` defines an `ADMIN_TOKEN`, but no route or middleware reads it to authorize administrative actions.

## Summary

CRITICAL: 0 | HIGH: 4 | MEDIUM: 2 | LOW: 2

## Findings

### [HIGH] Destructive user deletion has no authorization middleware
File: `ecommerce-api-legacy/src/routes.js:6`
Description: `DELETE /api/users/:id` invokes `controllers.deleteUser` directly, without authentication or authorization middleware.
Impact: Any client that can reach the API can delete a user.
Recommendation: Add an Express admin-authorization middleware that consumes `config.adminToken`, mount it before `controllers.deleteUser`, and test rejected and authorized requests.

### [HIGH] Financial administration endpoint is public
File: `ecommerce-api-legacy/src/routes.js:5`
Description: `GET /api/admin/financial-report` is exposed directly despite returning administrative revenue and student-payment data.
Impact: Any client can retrieve internal financial information and enrolled students' email addresses.
Recommendation: Confirm the intended access policy and protect the route with the appropriate authentication and authorization middleware.

### [HIGH] Configured administrative token is not enforced
File: `ecommerce-api-legacy/src/config.js:3`; `ecommerce-api-legacy/src/routes.js:3-7`
Description: `config.adminToken` is loaded from `ADMIN_TOKEN`, but the route registration contains no middleware that uses it.
Impact: Setting `ADMIN_TOKEN` gives a false impression that administrative endpoints are protected, while they remain publicly reachable.
Recommendation: Implement one reusable middleware that reads `config.adminToken`, fails closed when it is absent, checks the request credentials, and apply it only to routes requiring this policy.

### [HIGH] Seeded user password is stored in plaintext
File: `ecommerce-api-legacy/src/database.js:89`
Description: The initial user is inserted with the literal password `123`, while newly created checkout users use `hashPassword`.
Impact: The seeded account can be compromised immediately and password storage is inconsistent.
Recommendation: Seed a securely hashed password using the same password-hashing utility used by the application, and avoid documenting or committing a reusable default credential.

### [MEDIUM] Financial report performs N+1 database queries
File: `ecommerce-api-legacy/src/services.js:41-49`; `ecommerce-api-legacy/src/repositories.js:37-46`
Description: The report queries enrollments for each course, then queries a user and payment for every enrollment.
Impact: Database round trips grow with the number of courses and enrollments, degrading reporting performance.
Recommendation: Replace the loop-driven lookups with a joined or aggregated repository query and map the returned rows in the service.

### [MEDIUM] Database state is reset at every boot
File: `ecommerce-api-legacy/src/database.js:5-9`, `85-95`; `ecommerce-api-legacy/src/app.js:5-7`
Description: SQLite uses `:memory:` and the bootstrap always initializes and seeds it.
Impact: Users, enrollments, payments, and audit records disappear on restart, preventing reliable application behavior outside a demo.
Recommendation: Configure a persistent database path and run schema migrations and seeds as explicit operations rather than normal boot work.

### [LOW] Checkout cache is process-global mutable state
File: `ecommerce-api-legacy/src/utils.js:4`, `7-10`; `ecommerce-api-legacy/src/services.js:34`
Description: Checkout data is written to a module-level `globalCache` that is exported through the service module.
Impact: State is shared implicitly across requests, is lost on restart, and is difficult to test or replace.
Recommendation: Encapsulate the cache behind a dedicated dependency or remove it if no consumer requires it.

### [LOW] Dead configuration and export remain in the runtime modules
File: `ecommerce-api-legacy/src/config.js:4`; `ecommerce-api-legacy/src/utils.js:2`, `5`, `18`
Description: `paymentGatewayKey`, `config` in `utils.js`, and `totalRevenue` are defined or exported but not used by the running code.
Impact: Dead code obscures the actual configuration and can mislead maintainers about security and payment behavior.
Recommendation: Remove unused values after confirming they have no external consumers, or wire them into the intended implementation.

## Deprecated APIs

None detected in the project source.

## Total findings

8

Phase 2 complete. No source code was modified. Proceed with refactoring (Phase 3)? [y/n]

## Phase 3 Remediation Verification

The refactor was approved and completed after the Phase 2 report above.

| Original finding | Verification result |
|---|---|
| Destructive user deletion has no authorization middleware | `requireAdmin` now protects `DELETE /api/users/:id`; tests confirm `401` without credentials and a successful deletion with the configured bearer token. |
| Financial administration endpoint is public | `requireAdmin` now protects `GET /api/admin/financial-report`; tests confirm both rejected and authorized requests. |
| Configured administrative token is not enforced | `src/middlewares/requireAdmin.js` consumes `config.adminToken`, uses a timing-safe comparison, and fails closed when the token is absent. |
| Seeded user password is stored in plaintext | `src/seed.js` performs explicit seeding, requires `SEED_USER_PASSWORD`, and stores the scrypt hash generated by `hashPassword`. |
| Financial report performs N+1 database queries | `getFinancialReportRows` fetches courses, enrollments, users, and payments through one joined query. |
| Database state is reset at every boot | The default database path is persistent; schema initialization remains in boot while seeding is an explicit `npm run seed` operation. |
| Checkout cache is process-global mutable state | The global cache and its unused exports were removed. |
| Dead configuration and export remain in runtime modules | Unused payment configuration and stale exports were removed. |

## Post-Refactor Re-audit

CRITICAL: 0 | HIGH: 0 | MEDIUM: 0 | LOW: 0

No findings from the Phase 2 report remain in the current project source.

## Validation

- `npm test`: 3 passing tests, including unauthorized and authorized administrative requests, protected-handler non-execution, seed hashing, and checkout.
- `node --check`: passed for changed runtime and test modules.
- Application boot: passed with a temporary persistent SQLite database on port 31234.
