# e2e/pages/menu_page.py
# Page Object Model for the Menu page.
# Wraps all actions a user can take on /menu so tests stay clean and readable.

class MenuPage:
    """
    Represents the /menu page.
    Each method is one user action (open page, add item, go to checkout).
    """

    def __init__(self, page):
        # Store the Playwright page object so every method can use it
        self.page = page
        self.url  = "http://127.0.0.1:5002/menu"

    # ── Navigation ──

    def open(self):
        """Navigate to the menu page and wait until it has fully loaded."""
        self.page.goto(self.url)
        # Wait for at least one item card to appear before continuing
        self.page.wait_for_selector(".item-card", timeout=10000)

    # ── Cart actions ──

    def add_item_to_cart(self, item_name):
        """
        Find the card for the given item name and click its 'Add to Cart' button.

        Parameters:
            item_name (str): The exact text of the item, e.g. 'Chicken Shawarma'.
        """
        # Locate the card that contains the item name text
        item_card = self.page.locator(".item-card", has=self.page.locator(f"text={item_name}"))

        # Click the 'Add to Cart' button inside that card
        item_card.locator("button.btn-cart").click()

        # Wait for the success notification to confirm the item was added
        self.page.wait_for_selector("#cart-message.success", timeout=5000)

    def click_go_to_checkout(self):
        """Click the 'Go to Checkout' button in the cart sidebar."""
        self.page.locator("#checkout-btn").click()
        # Wait for the checkout page to load
        self.page.wait_for_url("**/checkout", timeout=8000)

    # ── Getters ──

    def get_notification_text(self):
        """Return the text currently shown in the cart notification bar."""
        return self.page.locator("#cart-message").inner_text()