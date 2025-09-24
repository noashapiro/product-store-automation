from playwright.sync_api import Page, expect
from .base_page import BasePage


class ProductDetailsPage(BasePage):
    """Product details page object model for Demoblaze"""

    def __init__(self, page: Page):
        super().__init__(page)

        # Selectors
        self.product_name = ".name"  # or "h2"
        self.product_price = "h3"  # Price is in h3 element
        self.product_description = ".description"
        self.add_to_cart_button = ".btn-success"
        self.product_image = "img[src*='imgs']"  # More specific selector for product images
        self.back_button = "button[onclick='history.back()']"  # More specific selector
        self.cart_link = "#cartur"

    def get_product_name(self) -> str:
        """Get product name"""
        return self.page.text_content(self.product_name)

    def get_product_price(self) -> str:
        """Get product price"""
        return self.page.text_content(self.product_price)

    def get_product_description(self) -> str:
        """Get product description"""
        return self.page.text_content(self.product_description)

    def get_product_image(self):
        """Get product image element"""
        return self.page.locator(self.product_image)

    def click_add_to_cart(self):
        """Click add to cart button"""
        self.page.click(self.add_to_cart_button)

    def click_back(self):
        """Click back button"""
        self.page.click(self.back_button)
        # Wait for page to load with shorter timeout
        try:
            self.page.wait_for_load_state("domcontentloaded")
        except:
            self.page.wait_for_load_state("load", timeout=5000)

    def click_cart(self):
        """Click cart link"""
        self.page.click(self.cart_link)
        # Wait for page to load with shorter timeout
        try:
            self.page.wait_for_load_state("domcontentloaded")
        except:
            self.page.wait_for_load_state("load", timeout=5000)

    def validate_product_details(self):
        """Validate all product details are present and correct"""
        # Validate product name exists and is not empty
        name = self.get_product_name()
        assert name, "Product name is empty"
        assert len(name) > 0, "Product name is empty"

        # Validate price exists and contains currency symbol
        price = self.get_product_price()
        assert price, "Product price is empty"
        assert "$" in price, "Product price doesn't contain $"

        # Validate description exists and is not empty
        description = self.get_product_description()
        assert description, "Product description is empty"
        assert len(description) > 0, "Product description is empty"

        # Validate image is visible
        expect(self.get_product_image()).to_be_visible()

        # Validate add to cart button is visible and enabled
        expect(self.page.locator(self.add_to_cart_button)).to_be_visible()
        expect(self.page.locator(self.add_to_cart_button)).to_be_enabled()

    def is_page_loaded(self) -> bool:
        """Check if product details page is loaded"""
        try:
            # Check if we're on a product details page by looking for the name
            name_visible = self.page.locator(self.product_name).is_visible()
            return name_visible
        except Exception:
            return False

    def wait_for_alert(self):
        """Wait for alert dialog and handle it"""

        def handle_dialog(dialog):
            assert "Product added" in dialog.message, f"Unexpected alert message: {dialog.message}"
            dialog.accept()

        self.page.on("dialog", handle_dialog)

    def add_to_cart_with_confirmation(self):
        """Add product to cart and wait for confirmation"""
        self.wait_for_alert()
        self.click_add_to_cart()
        # Wait a moment for the alert to be handled
        self.page.wait_for_timeout(1000)

    def get_add_to_cart_button_text(self) -> str:
        """Get add to cart button text"""
        return self.page.text_content(self.add_to_cart_button)

    def is_add_to_cart_button_enabled(self) -> bool:
        """Check if add to cart button is enabled"""
        return self.page.is_enabled(self.add_to_cart_button)
