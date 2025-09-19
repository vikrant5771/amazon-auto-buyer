# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

Project overview
- Purpose: Automate Amazon product search, add-to-cart, and navigate to checkout via Selenium.
- Entrypoint: src/amazon_buyer.py
- Language/runtime: Python 3.7+

Common commands
- Create and activate a virtualenv, then install dependencies
```bash path=null start=null
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

- Run the script (prompts for a product name)
```bash path=null start=null
python src/amazon_buyer.py
```

- Follow logs while running
```bash path=null start=null
tail -f logs/amazon_buyer.log
```

- Edit config (credentials and behavior). The file is git-ignored and required for login.
```bash path=null start=null
# Open for editing
$EDITOR config/config.json
```

Notes on testing/linting/build
- There is no configured test suite or linter in this repo (no pytest/ruff/flake8 config files, no tests/ directory).
- There is no build step (this is a direct-to-Python script workflow).

High-level architecture
- Single module application with one primary class.
  - File: src/amazon_buyer.py
  - Class: AmazonAutoBuyer
    - load_config: Reads JSON from config/config.json
    - setup_logging: Configures logging to logs/amazon_buyer.log and console
    - setup_driver: Creates a Chrome WebDriver with anti-automation flags and a custom user agent
    - login_to_amazon: Performs email/password login (waits for nav logo to confirm)
    - search_product: Navigates to amazon.com, submits a query, waits for results
    - select_first_product: Clicks the first search result and waits for product page
    - add_to_cart: Attempts several selectors for the Add to Cart button with fallbacks
    - proceed_to_checkout: Opens cart and clicks the checkout button
    - complete_purchase: Orchestrates the full flow and intentionally stops at checkout for safety
  - Program flow: main() -> AmazonAutoBuyer() -> prompt for product -> complete_purchase(product)

Configuration model and important discrepancies
- README and config/config.json structure:
  - credentials.email, credentials.password
  - settings.headless, settings.implicit_wait, settings.page_load_timeout, settings.max_retries
  - purchase_limits.max_price, purchase_limits.confirmation_required
  - product_preferences.prime_only, min_rating, verified_seller_only
- Code expectations vs. config:
  - In setup_driver, the code checks self.config.get('headless', False) at the top-level, but README/config place headless under settings.headless. Unless you move headless to the root of config.json, headless will be ignored by the code.
  - Other settings (implicit_wait, page_load_timeout, max_retries), purchase_limits.*, and product_preferences.* are currently not read or enforced in the code.
  - webdriver-manager is listed in requirements but not used in code; the code instantiates webdriver.Chrome directly.

Operational considerations
- Browser requirements: Google Chrome must be installed and compatible with your local chromedriver. Because webdriver-manager is not used in code, ensure your environment has a matching chromedriver available on PATH or adjust the code to use webdriver-manager.
- 2FA/CAPTCHA: If Amazon requires 2FA or shows bot checks, the script expects manual intervention in the visible browser session.
- Safety stop: The purchase flow intentionally stops at checkout and requires manual action to complete a purchase.
- Logs: All major actions are logged to logs/amazon_buyer.log. Use tail -f to monitor.

Repository context highlights (from README)
- Strong disclaimers about legal/ethical use, financial risk, and account security.
- Troubleshooting points include ChromeDriver issues, login failures (2FA), element locators changing, and potential rate limiting.

Warp-specific guidance
- Do not commit credentials. config/config.json is already in .gitignore.
- When modifying behavior that depends on config, reconcile the headless key location or update the code to read settings.headless.
- If you add tests/linting in future iterations, document the exact commands here.
