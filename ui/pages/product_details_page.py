from playwright.sync_api import Page, expect
from .base_page import BasePage


class ProductDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # Selectors
        self.product_name = ".name"
        self.product_price = "h3"
        self.product_description = ".description"
        self.add_to_cart_button = ".btn-success"
        self.product_image = "img[src*='imgs']"
        self.back_button = "button[onclick='history.back()']"
        self.cart_link = "#cartur"

    def get_product_name(self) -> str:
        return self.page.text_content(self.product_name)

    def get_product_price(self) -> str:
        return self.page.text_content(self.product_price)

    def get_product_description(self) -> str:
        return self.page.text_content(self.product_description)

    def get_product_image(self):
        return self.page.locator(self.product_image)

    def click_add_to_cart(self):
        self.page.click(self.add_to_cart_button)

    def click_back(self):
        self.page.click(self.back_button)
        # Wait for page to load with shorter timeout
        try:
            self.page.wait_for_load_state("domcontentloaded")
        except:
            self.page.wait_for_load_state("load", timeout=5000)

    def click_cart(self):
        self.page.click(self.cart_link)
        # Wait for page to load with shorter timeout
        try:
            self.page.wait_for_load_state("domcontentloaded")
        except:
            self.page.wait_for_load_state("load", timeout=5000)

    def validate_product_details(self):
        # Validate product name exists and is not empty
        name = self.get_product_name()
        assert name, "Product name is empty"
        assert len(name) > 0, "Product name is empty"

        price = self.get_product_price()
        assert price, "Product price is empty"
        assert "$" in price, "Product price doesn't contain $"

        description = self.get_product_description()
        assert description, "Product description is empty"
        assert len(description) > 0, "Product description is empty"

        expect(self.get_product_image()).to_be_visible()

        expect(self.page.locator(self.add_to_cart_button)).to_be_visible()
        expect(self.page.locator(self.add_to_cart_button)).to_be_enabled()

    def is_page_loaded(self) -> bool:
        try:
            # Check if we're on a product details page by looking for the name
            name_visible = self.page.locator(self.product_name).is_visible()
            return name_visible
        except Exception:
            return False


    def get_add_to_cart_button_text(self) -> str:
        return self.page.text_content(self.add_to_cart_button)

    def is_add_to_cart_button_enabled(self) -> bool:
        return self.page.is_enabled(self.add_to_cart_button)
