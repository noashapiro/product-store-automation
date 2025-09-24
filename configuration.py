# BASE_URL
BASE_URL = "https://www.demoblaze.com"

# API Configuration
API_BASE_URL = "http://localhost:3000"
PRODUCTS_ENDPOINT = f"{API_BASE_URL}/products"
CART_ENDPOINT = f"{API_BASE_URL}/cart"

# Test Configuration
DEFAULT_TIMEOUT = 10  # seconds for API tests
UI_DEFAULT_TIMEOUT = 10000  # milliseconds for UI tests
NAVIGATION_TIMEOUT = 15000  # milliseconds
ELEMENT_WAIT_TIMEOUT = 10000  # milliseconds

# Test Data Configuration
MIN_PRODUCTS_EXPECTED = 1
MAX_PRODUCTS_EXPECTED = 100
MAX_RESPONSE_TIME = 5.0  # seconds
MAX_PAGE_LOAD_TIME = 5.0  # seconds

# UI Test Configuration
HEADLESS_MODE = True
BROWSER_TYPE = "chromium"  # chromium, firefox, webkit

# Test Categories
SMOKE_TESTS = ["test_demoblaze_homepage_loads", "test_navigation_to_product_details", "test_add_to_cart_functionality"]
REGRESSION_TESTS = ["test_*"]
PERFORMANCE_TESTS = ["*performance*"]

# Retry Configuration
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1  # seconds

# Performance Test Configuration
CONCURRENT_REQUESTS = 10
PERFORMANCE_TEST_DURATION = 30  # seconds
