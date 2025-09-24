from playwright.sync_api import Page, expect
from .base_page import BasePage


class CartPage(BasePage):
    """Cart page object model for Demoblaze"""

    def __init__(self, page: Page):
        super().__init__(page)

        # Selectors
        self.cart_items = ".success"
        self.item_name = "td:nth-child(2)"
        self.item_price = "td:nth-child(3)"
        self.total_price = "#totalp"  # Updated selector
        self.delete_button = ".btn-danger"
        self.place_order_button = ".btn-success"
        self.empty_cart_message = ".text-center"

    def get_cart_items(self):
        """Get all cart items"""
        return self.page.locator(self.cart_items).all()

    def get_cart_item_count(self) -> int:
        """Get number of items in cart"""
        return self.page.locator(self.cart_items).count()

    def get_item_details(self, index: int = 0) -> dict:
        """Get details of a specific cart item by index"""
        item = self.page.locator(self.cart_items).nth(index)

        name = item.locator(self.item_name).text_content()
        price = item.locator(self.item_price).text_content()

        return {
            "name": name.strip() if name else "",
            "price": price.strip() if price else ""
        }

    def get_total_price(self) -> str:
        """Get total price"""
        return self.page.text_content(self.total_price)

    def delete_item(self, index: int = 0):
        """Delete a cart item by index"""
        item = self.page.locator(self.cart_items).nth(index)
        item.locator(self.delete_button).click()
        # Wait for page to load with shorter timeout
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
        except:
            self.page.wait_for_load_state("load", timeout=5000)

    def click_place_order(self):
        """Click place order button"""
        self.page.click(self.place_order_button)

    def is_page_loaded(self) -> bool:
        """Check if cart page is loaded"""
        try:
            # Check if cart page is loaded by looking for either items or empty message
            has_items = self.page.locator(self.cart_items).count() > 0
            has_empty_message = self.page.locator(self.empty_cart_message).is_visible()
            return has_items or has_empty_message
        except Exception:
            return False

    def validate_cart_item(self, item_name: str, expected_price: str):
        """Validate that a specific item exists in cart with correct price"""
        items = self.get_cart_items()
        found = False

        for i in range(len(items)):
            item = self.get_item_details(i)
            if item["name"] == item_name:
                assert item["price"] == expected_price, f"Price mismatch for {item_name}"
                found = True
                break

        assert found, f"Item {item_name} not found in cart"

    def get_all_cart_items(self) -> list:
        """Get all cart items as a list of dictionaries"""
        items = []
        count = self.get_cart_item_count()
        for i in range(count):
            item = self.get_item_details(i)
            items.append(item)
        return items

    def is_cart_empty(self) -> bool:
        """Check if cart is empty"""
        return self.get_cart_item_count() == 0

    def clear_cart(self):
        """Clear all items from cart"""
        while self.get_cart_item_count() > 0:
            self.delete_item(0)

    def get_cart_total(self) -> str:
        """Get cart total price"""
        return self.get_total_price()

    def validate_cart_has_items(self, expected_count: int):
        """Validate that cart has expected number of items"""
        actual_count = self.get_cart_item_count()
        assert actual_count == expected_count, f"Expected {expected_count} items, got {actual_count}"
