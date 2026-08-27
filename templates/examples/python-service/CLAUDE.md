# CLAUDE.md

<!--
  A WORKED EXAMPLE, not a file to copy. This is what templates/CLAUDE.md.template
  looks like once it is filled in for a real project: a small FastAPI service.

  Note what it does NOT contain: no directory listing, no dependency list, no
  description of what FastAPI is. All of that is either derivable from the code
  or already known. What is left is what Claude would otherwise get wrong.

  73 lines of content. Well inside the budget, and every line earns its place.
-->

Billing API. FastAPI service that reconciles Stripe webhooks against our own subscription records and exposes
invoice history to the dashboard.

## Commands

```bash
uv sync                                        # install
pytest                                         # all tests (~40s)
pytest tests/test_webhooks.py::test_replay     # one test
ruff check . && ruff format .                  # lint and format
mypy src/                                      # typecheck
uvicorn src.billing.main:app --reload          # run locally on :8000
```

**IMPORTANT: run `ruff check . && mypy src/ && pytest` before every commit.** CI runs exactly these three and
nothing else.

## Architecture

Webhooks are the only write path. Everything that mutates subscription state enters through
`src/billing/webhooks/`, is validated, and is written by a service in `src/billing/services/`. Routes never
touch the database directly — a route with a `session.execute(...)` in it is a bug, not a shortcut.

Stripe is the source of truth for payment state; our tables are a cache. When they disagree, Stripe wins and
we log a reconciliation event. Do not add code that "fixes" our records without emitting one.

Webhook handlers must be idempotent. Stripe retries, and it retries more often than you would expect.

## Conventions

- Type annotations on every public function. `mypy` runs in strict mode; `# type: ignore` needs a comment
  saying why.
- Pydantic models for anything crossing a boundary — request bodies, responses, webhook payloads. Plain
  dataclasses internally.
- Raise `BillingError` subclasses from `src/billing/errors.py`; never raise `HTTPException` outside a route.
- Money is `int` cents everywhere. There is no `float` in this codebase and there should never be one.

## Testing

- `pytest` with `tests/` mirroring `src/`.
- Stripe is mocked through `tests/fixtures/stripe.py`. Never mock our own services — if a test needs that,
  the seam is in the wrong place.
- Integration tests need Postgres on `:5433` (`docker compose up -d db`). They are marked `@pytest.mark.integration`
  and excluded by default; run them with `pytest -m integration`.

## Gotchas

- `uv sync` does not regenerate the Stripe type stubs. Run `make stubs` after bumping the `stripe` package or
  `mypy` fails with errors that look unrelated.
- The `subscriptions.status` column is a Postgres enum. Adding a value needs a migration; SQLAlchemy will not
  tell you, it will just fail at runtime in production.
- `TZ=UTC` must be set. Invoice period boundaries are computed in local time if it is not, and the tests pass
  anyway because CI is already UTC.

## Git

- Branches: `feat/<ticket>`, `fix/<ticket>`.
- Conventional commits; the changelog is generated from them.
- Never commit `.env.local` or anything under `fixtures/real/` — both contain live Stripe test keys.
