# Engineering Standards

## Shared

- Code must pass formatting, lint, and type checks where applicable.
- Tests must be added for all new or changed critical paths.
- Database changes must be migration-based.
- External dependencies must be isolated behind adapters or clients.

## Web

- Respect design tokens.
- Cover primary flows with Playwright.
- Cover loading, success, empty, and error states.

## Backend

- Respect API contracts.
- Validate request / response DTOs.
- Preserve domain invariants.
- Cover service and integration paths.
