E2E Tests — Playwright

Quick notes and commands for running the end-to-end tests in this repo.

Selectors used by tests
- Order type select: `#order-type` (values: `Dine-In`, `Takeaway`)
- Payment method select: `#payment-method` (values: `Cash`, `Mock Card`, `Mock Card Fail`)
- Table number container (visible state): `#field-table-number` (has `.visible` when shown)
- Place order button for E2E: `#place-order-btn` (clickable by tests)

Run tests (headless):

```powershell
# From repository root
py -3 -m pytest e2e/test_customer_order_flow.py -q
```

Run tests in headed mode (shows the browser):

```powershell
# Set HEADLESS=false for the test fixture to launch a headed browser
$env:HEADLESS = 'false'
py -3 -m pytest e2e/test_customer_order_flow.py -q
```

Install requirements for Playwright (only once):

```powershell
py -3 -m pip install pytest playwright
py -3 -m playwright install chromium
```

Notes
- The test fixture reads the `HEADLESS` environment variable. Default is `true`.
- The `#place-order-btn` is intentionally shown after the checkout UI renders so automated scripts can reliably trigger the submit action.
