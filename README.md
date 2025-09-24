# Product Store Automation

Automation test for Product Store website with Mock API Backend tests.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Mock API Server](#running-the-mock-api-server)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [Test Data](#test-data)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.8+** - For running the test framework
- **Node.js** - For json-server (mock API)
- **Git** - For cloning the repository

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd product-store-automation
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
# Install core testing dependencies
pip install pytest requests playwright

# Install Playwright browsers
playwright install
```

### 4. Install JSON Server

```bash
# Install json-server globally (requires Node.js)
npm install -g json-server
```

## Configuration

The project uses environment variables and `configuration.py` for settings:

### Environment Variables

```bash
# For Backend Tests (Mock API) - You are able to set this when running backend tests
export BASE_URL=http://localhost:3000
default - BASE_URL= "http://localhost:3000""
```

### Configuration Settings

- **BASE_URL**: Target application URL
  - **Backend Tests**: Default `http://localhost:3000` (mock API server)
  - **UI Tests**: Default `https://www.demoblaze.com` (live application)
- **UI_DEFAULT_TIMEOUT**: UI test timeout (default: 10000ms)
- **HEADLESS_MODE**: Run browser in headless mode (default: True)
- **BROWSER_TYPE**: Browser to use for UI tests (default: "chromium")

## Running the Mock API Server

**Important**: Backend tests require the mock API server to be running.

### Start the Server

```bash
# Navigate to the mock-api directory
cd be/mock-api

# Start json-server on default port 3000
json-server --watch db.json --port 3000

# Alternative: Start on different port (e.g., 3001)
json-server --watch db.json --port 3001
```

### If Using Different Port

If you change the port, update the BASE_URL environment variable:

```bash
# For port 3001
export BASE_URL=http://localhost:3001
```

**Note**: Keep the server running in a separate terminal while executing backend tests.

## Running Tests

### Backend API Tests

```bash
# Ensure mock server is running first!
# Then run backend tests
source venv/bin/activate
python -m pytest be/tests/ -v

# Run specific test files
python -m pytest be/tests/products/get_products_tests.py -v
python -m pytest be/tests/products/add_to_cart_tests.py -v
python -m pytest be/tests/products/get_cart_tests.py -v
```

### Frontend UI Tests

```bash
# Run all UI tests
source venv/bin/activate
python -m pytest ui/tests/ -v

# Run specific UI test files
python -m pytest ui/tests/product_details_tests.py -v
python -m pytest ui/tests/add_to_cart_tests.py -v

# Run tests with markers
python -m pytest ui/tests/ -m smoke -v
python -m pytest ui/tests/ -m cart -v
```

### Run All Tests

```bash
# Run both backend and frontend tests
source venv/bin/activate
python -m pytest be/tests/ ui/tests/ -v
```

### Test Execution Options

```bash
# Run tests in parallel (if pytest-xdist is installed)
python -m pytest -n auto

# Generate HTML report
python -m pytest --html=report.html

# Run tests with verbose output
python -m pytest -v -s

# Run tests matching a pattern
python -m pytest -k "test_add_to_cart"
```

## Test Data

### Mock API Data Structure

The backend tests use json-server with the following data structure (`be/mock-api/db.json`):

```json
{
  "products": [
    {"id": "1", "name": "Laptop", "price": 1200},
    {"id": "2", "name": "Phone", "price": 800}
  ],
  "cart": [
    {"id": "36df", "product_id": 1, "quantity": 2},
    {"id": "7d8a", "product_id": 2, "quantity": 1}
  ]
}
```

### Available API Endpoints

- `GET /products` - Retrieve all products
- `GET /cart` - Retrieve cart items
- `POST /cart` - Add item to cart

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure virtual environment is activated
   ```bash
   source venv/bin/activate
   ```

2. **Browser Not Found**: Install Playwright browsers
   ```bash
   playwright install
   ```

3. **Mock API Connection Error**: Ensure json-server is running
   ```bash
   cd be/mock-api
   json-server --watch db.json --port 3000
   ```

4. **Port Already in Use**: Change port and update BASE_URL
   ```bash
   json-server --watch db.json --port 3001
   export BASE_URL=http://localhost:3001
   ```

### Debug Mode

```bash
# Run tests with debug output
python -m pytest -v -s --tb=short

# Run specific test with maximum verbosity
python -m pytest be/tests/products/get_products_tests.py::TestGetProduct::test_get_products -v -s
```

### Test Markers

The project uses pytest markers for test categorization:

- `@pytest.mark.smoke`: Critical functionality tests
- `@pytest.mark.cart`: Cart-related functionality
- `@pytest.mark.details`: Product details page tests

## Assumptions and Limitations

### Assumptions

1. **Mock API**: Backend tests require json-server running on localhost:3000
2. **Test Data**: Uses predefined test data from `be/mock-api/db.json`
3. **Browser Support**: Tests are optimized for Chromium browser
4. **Network Stability**: Assumes stable internet connection for UI tests

### Limitations

1. **Browser Dependencies**: UI tests require browser installation via Playwright
2. **Timing Sensitivity**: Some tests may be sensitive to network latency
3. **Browser Compatibility**: Tests are primarily tested on Chromium
4. **Test Data**: Limited to mock data provided in `be/mock-api/db.json`
5. **Concurrent Execution**: UI tests may have limitations with parallel execution

---

This project is for educational and testing purposes.