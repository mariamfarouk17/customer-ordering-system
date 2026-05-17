# e2e/test_customer_order_flow.py
# End-to-end test for the full customer order flow:
#   Menu → Add item → Checkout → Confirmation
#
# Requirements:
#   pip install pytest playwright
#   playwright install chromium
#
# Run with:
#   pytest e2e/test_customer_order_flow.py --headed    (see the browser)
#   pytest e2e/test_customer_order_flow.py             (headless / CI mode)

import os
import pytest
from playwright.sync_api import sync_playwright
from e2e.pages.menu_page import MenuPage


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def page():
    """
    Starts a real Chromium browser, opens a blank page,
    and hands it to the test. Closes everything when the test is done.

    scope="function" means a fresh browser for every test function.
    """
    with sync_playwright() as playwright:
        # Launch a browser. Use the HEADLESS env var to toggle headed/headless.
        headless_env = os.environ.get("HEADLESS", "true").lower()
        headless = not (headless_env in ("0", "false", "no", "n"))
        browser = playwright.chromium.launch(headless=headless)
        context = browser.new_context()
        test_page = context.new_page()

        yield test_page  # the test runs here

        context.close()
        browser.close()


# ── Test ──────────────────────────────────────────────────────────────────────

def test_customer_order_flow(page):
    """
    Full happy-path E2E test:
      1. Open /menu
      2. Add Chicken Shawarma to cart
      3. Click 'Go to Checkout'
      4. Fill in and submit the checkout form
      5. Verify the confirmation page loads
      6. Verify an order code (ORD-XXXXX) is displayed
    """

    # ── Step 1: Open the menu page ──
    menu = MenuPage(page)
    menu.open()

    # ── Step 2: Add Chicken Shawarma to the cart ──
    menu.add_item_to_cart("Chicken Shawarma")

    # Confirm the success message appeared in the notification bar
    notification = menu.get_notification_text()
    assert "added" in notification.lower() or "cart" in notification.lower(), (
        f"Expected a success message after adding item, got: '{notification}'"
    )

    # ── Step 3: Click 'Go to Checkout' ──
    menu.click_go_to_checkout()

    # ── Step 4: Fill in the checkout form ──

    # Select order type: Dine-In
    page.select_option("#order-type", value="Dine-In")

    # The table number field should now be visible — fill it in
    page.wait_for_selector("#field-table-number.visible", timeout=3000)
    page.fill("#table-number", "3")

    # Select payment method: Cash
    page.select_option("#payment-method", value="Cash")

    # Click the Place Order button
    page.locator("#place-order-btn").click()

    # ── Step 5: Wait for the confirmation page to load ──
    # The checkout page redirects to /confirmation/<order_code>
    page.wait_for_url("**/confirmation/**", timeout=10000)

    # ── Step 6: Verify the order code is displayed on the page ──

    # Wait for the order details to load (the JS fetches from the API)
    page.wait_for_selector("#detail-order-code", timeout=8000)

    order_code_text = page.locator("#detail-order-code").inner_text()

    # The order code must follow the ORD-XXXXX format
    assert order_code_text.startswith("ORD-"), (
        f"Expected order code starting with 'ORD-', got: '{order_code_text}'"
    )

    # The confirmation banner should also be visible
    page.wait_for_selector(".success-banner.visible", timeout=5000)
    banner_text = page.locator(".success-banner h2").inner_text()
    assert "confirmed" in banner_text.lower(), (
        f"Expected 'Order Confirmed' banner, got: '{banner_text}'"
    )