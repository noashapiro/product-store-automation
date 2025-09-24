from playwright.sync_api import Page, expect

from ui.pages.base_page import BasePage


class HomePage(BasePage):
    """Home page object model for Demoblaze"""

    def __init__(self, page: Page):
        super().__init__(page)

        # Selectors
        self.product_cards = ".col-lg-4.col-md-6.mb-4"
        self.product_name = ".card-title"
        self.product_price = "h5"  # Price is in h5 element
        self.product_image = ".card-img-top"
        self.product_link = ".hrefch"
        self.cart_link = "#cartur"
        self.navbar_brand = ".navbar-brand"

    def navigate(self):
        """Navigate to home page"""
        super().navigate("/")
        # Wait for either navbar or products to be visible
        try:
            self.wait_for_element(self.navbar_brand)
        except:
            # If navbar doesn't load, try waiting for products
            self.wait_for_element(self.product_cards)

    def get_product_cards(self):
        """Get all product cards"""
        return self.page.locator(self.product_cards).all()

    def get_product_count(self) -> int:
        """Get number of products on the page"""
        return self.page.locator(self.product_cards).count()

    def get_product_details(self, index: int = 0) -> dict:
        """Get details of a specific product by index"""
        product_card = self.page.locator(self.product_cards).nth(index)

        name = product_card.locator(self.product_name).text_content()
        price = product_card.locator(self.product_price).text_content()
        image = product_card.locator(self.product_image)
        link = product_card.locator(self.product_link)

        return {
            "name": name.strip() if name else "",
            "price": price.strip() if price else "",
            "image": image,
            "link": link
        }

    def click_product(self, index: int = 0):
        """Click on a product by index"""
        product_card = self.page.locator(self.product_cards).nth(index)
        product_card.locator(self.product_link).click()
        # Wait for page to load with shorter timeout
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
        except:
            self.page.wait_for_load_state("load", timeout=5000)

    def click_cart(self):
        """Click on cart link"""
        self.page.click(self.cart_link)
        # Wait for page to load with shorter timeout
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
        except:
            self.page.wait_for_load_state("load", timeout=5000)

    def validate_product_display(self):
        """Validate that all products are displayed correctly"""
        products = self.get_product_cards()

        for i in range(len(products)):
            product = self.get_product_details(i)

            # Validate product name exists and is not empty
            assert product["name"], f"Product {i} name is empty"
            assert len(product["name"]) > 0, f"Product {i} name is empty"

            # Validate price exists and contains currency symbol
            assert product["price"], f"Product {i} price is empty"
            assert "$" in product["price"], f"Product {i} price doesn't contain $"

            # Validate image is visible
            expect(product["image"]).to_be_visible()

            # Validate link exists
            expect(product["link"]).to_be_visible()

    def is_page_loaded(self) -> bool:
        """Check if home page is loaded"""
        try:
            # Just check if navbar is visible - that's enough to know the page loaded
            navbar_visible = self.page.locator(self.navbar_brand).is_visible()
            return navbar_visible
        except Exception:
            return False

    def get_all_product_names(self) -> list:
        """Get all product names from the page"""
        names = []
        count = self.get_product_count()
        for i in range(count):
            product = self.get_product_details(i)
            names.append(product["name"])
        return names

    def get_all_product_prices(self) -> list:
        """Get all product prices from the page"""
        prices = []
        count = self.get_product_count()
        for i in range(count):
            product = self.get_product_details(i)
            prices.append(product["price"])
        return prices
