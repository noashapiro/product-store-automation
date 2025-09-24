from playwright.sync_api import Page, expect
from .base_page import BasePage


class CartPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        # Selectors
        self.cart_items = ".success"
        self.item_name = "td:nth-child(2)"
        self.item_price = "td:nth-child(3)"
        self.total_price = "#totalp"
        self.delete_button = ".btn-danger"
        self.place_order_button = ".btn-success"
        self.empty_cart_message = ".text-center"

    def get_cart_items(self):
        return self.page.locator(self.cart_items).all()

    def get_cart_item_count(self) -> int:
        return self.page.locator(self.cart_items).count()

    def get_item_details(self, index: int = 0) -> dict:
        item = self.page.locator(self.cart_items).nth(index)

        name = item.locator(self.item_name).text_content()
        price = item.locator(self.item_price).text_content()

        return {
            "name": name.strip() if name else "",
            "price": price.strip() if price else ""
        }

    def get_total_price(self) -> str:
        return self.page.text_content(self.total_price)


    def is_page_loaded(self) -> bool:
        try:
            # Check if cart page is loaded by looking for either items or empty message
            has_items = self.page.locator(self.cart_items).count() > 0
            has_empty_message = self.page.locator(self.empty_cart_message).is_visible()
            return has_items or has_empty_message
        except Exception:
            return False

    def validate_cart_item(self, item_name: str, expected_price: str):
        items = self.get_cart_items()
        found = False

        for i in range(len(items)):
            item = self.get_item_details(i)
            if item["name"] == item_name:
                assert item["price"] == expected_price, f"Price mismatch for {item_name}"
                found = True
                break

        assert found, f"Item {item_name} not found in cart"

    def get_cart_total(self) -> str:
        return self.get_total_price()

    def validate_cart_has_items(self, expected_count: int):
        actual_count = self.get_cart_item_count()
        assert actual_count == expected_count, f"Expected {expected_count} items, got {actual_count}"


    def wait_for_alert(self):
        def handle_dialog(dialog):
            assert "Product added" in dialog.message, f"Unexpected alert message: {dialog.message}"
            dialog.accept()

        self.page.on("dialog", handle_dialog)