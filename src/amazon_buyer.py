#!/usr/bin/env python3
"""
Amazon Auto-Buyer
A Python script to automate Amazon product search, selection, and checkout.
"""

import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class AmazonAutoBuyer:
    def __init__(self, config_path='config/config.json'):
        """Initialize the Amazon Auto Buyer with configuration."""
        self.config = self.load_config(config_path)
        self.driver = None
        self.setup_logging()
        
    def load_config(self, config_path):
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Config file not found: {config_path}")
            return {}
    
    def setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/amazon_buyer.log'),
                logging.StreamHandler()
            ]
        )
        
    def setup_driver(self):
        """Set up Chrome WebDriver with options."""
        chrome_options = Options()
        
        # Check if we should reuse existing browser session
        reuse_browser = self.config.get('settings', {}).get('reuse_existing_browser', True)
        
        if reuse_browser:
            # Try to connect to existing Chrome session
            try:
                # Add debugging port to connect to existing Chrome session
                chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
                logging.info("Attempting to connect to existing Chrome session...")
            except Exception as e:
                logging.warning(f"Could not connect to existing session: {e}")
                logging.info("Starting new Chrome session...")
                reuse_browser = False
        
        if not reuse_browser:
            # Add user preferences for new session
            if self.config.get('headless', False):
                chrome_options.add_argument('--headless')
                
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Comprehensive arguments to suppress warnings and improve stability
            chrome_options.add_argument('--disable-background-networking')
            chrome_options.add_argument('--disable-background-timer-throttling')
            chrome_options.add_argument('--disable-renderer-backgrounding')
            chrome_options.add_argument('--disable-backgrounding-occluded-windows')
            chrome_options.add_argument('--disable-client-side-phishing-detection')
            chrome_options.add_argument('--disable-sync')
            chrome_options.add_argument('--disable-default-apps')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--disable-features=TranslateUI')
            chrome_options.add_argument('--disable-ipc-flooding-protection')
            chrome_options.add_argument('--log-level=3')  # Suppress INFO, WARNING and ERROR logs
            
            # Additional arguments to completely disable Google services and GCM
            chrome_options.add_argument('--disable-component-update')
            chrome_options.add_argument('--disable-background-mode')
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            chrome_options.add_argument('--disable-features=UserAgentClientHint')
            chrome_options.add_argument('--disable-sync-preferences')
            chrome_options.add_argument('--disable-component-extensions-with-background-pages')
            chrome_options.add_argument('--disable-background-downloads')
            chrome_options.add_argument('--disable-hang-monitor')
            chrome_options.add_argument('--disable-prompt-on-repost')
            chrome_options.add_argument('--disable-domain-reliability')
            chrome_options.add_argument('--disable-features=OptimizationHints')
            chrome_options.add_argument('--gcm-checkin-url=')
            chrome_options.add_argument('--gcm-mcs-endpoint=')
            chrome_options.add_argument('--gcm-registration-url=')
            chrome_options.add_argument('--disable-cloud-import')
            chrome_options.add_argument('--disable-fetching-hints-at-navigation-start')
            
            # Chrome stability and crash prevention
            chrome_options.add_argument('--disable-gpu-sandbox')
            chrome_options.add_argument('--disable-software-rasterizer')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-first-run')
            chrome_options.add_argument('--no-default-browser-check')
            chrome_options.add_argument('--disable-crash-reporter')
            chrome_options.add_argument('--disable-logging')
            chrome_options.add_argument('--disable-in-process-stack-traces')
            chrome_options.add_argument('--max_old_space_size=1024')
            chrome_options.add_argument('--memory-pressure-off')
            # Note: --single-process removed as it can cause instability on macOS
            
            # Set user agent to avoid detection
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            if not reuse_browser:
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logging.info("WebDriver setup completed successfully")
        except Exception as e:
            if reuse_browser:
                logging.warning(f"Failed to connect to existing Chrome session: {e}")
                logging.info("Falling back to new Chrome session...")
                return self._create_new_chrome_session()
            else:
                raise e
    
    def _create_new_chrome_session(self):
        """Create a new Chrome session with all optimizations."""
        chrome_options = Options()
        if self.config.get('headless', False):
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Comprehensive arguments to suppress warnings and improve stability
        chrome_options.add_argument('--disable-background-networking')
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-client-side-phishing-detection')
        chrome_options.add_argument('--disable-sync')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=TranslateUI')
        chrome_options.add_argument('--disable-ipc-flooding-protection')
        chrome_options.add_argument('--log-level=3')  # Suppress INFO, WARNING and ERROR logs
        
        # Additional arguments to completely disable Google services and GCM
        chrome_options.add_argument('--disable-component-update')
        chrome_options.add_argument('--disable-background-mode')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-features=UserAgentClientHint')
        chrome_options.add_argument('--disable-sync-preferences')
        chrome_options.add_argument('--disable-component-extensions-with-background-pages')
        chrome_options.add_argument('--disable-background-downloads')
        chrome_options.add_argument('--disable-hang-monitor')
        chrome_options.add_argument('--disable-prompt-on-repost')
        chrome_options.add_argument('--disable-domain-reliability')
        chrome_options.add_argument('--disable-features=OptimizationHints')
        chrome_options.add_argument('--gcm-checkin-url=')
        chrome_options.add_argument('--gcm-mcs-endpoint=')
        chrome_options.add_argument('--gcm-registration-url=')
        chrome_options.add_argument('--disable-cloud-import')
        chrome_options.add_argument('--disable-fetching-hints-at-navigation-start')
        
        # Chrome stability and crash prevention
        chrome_options.add_argument('--disable-gpu-sandbox')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--no-default-browser-check')
        chrome_options.add_argument('--disable-crash-reporter')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--disable-in-process-stack-traces')
        chrome_options.add_argument('--max_old_space_size=1024')
        chrome_options.add_argument('--memory-pressure-off')
        # Note: --single-process removed as it can cause instability on macOS
        
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        logging.info("New Chrome session created successfully")
    
    def _recover_driver(self):
        """Attempt to recover from a Chrome crash."""
        try:
            logging.info("Attempting Chrome driver recovery...")
            
            # Close existing driver if possible
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
            
            # Create new session
            self._create_new_chrome_session()
            
            # Verify recovery
            self.driver.get("https://www.amazon.in")
            logging.info("Chrome driver recovery successful")
            
        except Exception as e:
            logging.error(f"Chrome driver recovery failed: {e}")
            raise Exception("Could not recover Chrome session")
        
    def login_to_amazon(self):
        """Login to Amazon with stored credentials."""
        try:
            # First, check if already logged in by visiting Amazon main page
            logging.info("Checking if already logged in to Amazon...")
            self.driver.get("https://www.amazon.in")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "nav-logo"))
            )
            
            # Check if we can find account menu indicating we're logged in
            try:
                account_menu = self.driver.find_element(By.ID, "nav-link-accountList")
                account_text = account_menu.text.lower()
                if "hello" in account_text or "account" in account_text:
                    logging.info("Already logged in to Amazon")
                    return True
            except NoSuchElementException:
                pass
            
            # Not logged in, proceed with login
            logging.info("Not logged in, navigating to Amazon login page...")
            self.driver.get("https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
            
            # Enter email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ap_email"))
            )
            email_field.send_keys(self.config['credentials']['email'])
            
            # Click continue
            continue_btn = self.driver.find_element(By.ID, "continue")
            continue_btn.click()
            
            # Enter password
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ap_password"))
            )
            password_field.send_keys(self.config['credentials']['password'])
            
            # Click sign in
            signin_btn = self.driver.find_element(By.ID, "signInSubmit")
            signin_btn.click()
            
            # Wait for login to complete
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "nav-logo"))
            )
            
            logging.info("Successfully logged in to Amazon")
            return True
            
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            return False
    
    def search_product(self, product_name):
        """Search for a product on Amazon."""
        try:
            logging.info(f"Searching for product: {product_name}")
            
            # Navigate to Amazon main page if not already there
            if "amazon.com" not in self.driver.current_url:
                self.driver.get("https://www.amazon.in")
            
            # Find search box
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
            )
            
            # Clear and enter search term
            search_box.clear()
            search_box.send_keys(product_name)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for search results to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-component-type='s-search-result']"))
            )
            
            logging.info("Search completed successfully")
            return True
            
        except Exception as e:
            logging.error(f"Search failed: {str(e)}")
            return False
    
    def select_first_product(self):
        """Select the first available product from search results with crash recovery."""
        max_retries = 2
        
        for attempt in range(max_retries):
            try:
                logging.info(f"Selecting first product from search results... (attempt {attempt + 1})")
                
                # Check if driver is still responsive
                try:
                    self.driver.current_url
                except Exception as e:
                    logging.error(f"Driver not responsive: {e}")
                    if attempt < max_retries - 1:
                        logging.info("Attempting to recover Chrome session...")
                        self._recover_driver()
                        continue
                    else:
                        raise e
                
                # Multiple selectors to try for product links (Amazon changes these frequently)
                product_selectors = [
                    "[data-component-type='s-search-result'] h2 a",
                    "[data-component-type='s-search-result'] .a-link-normal",
                    ".s-result-item h2 a",
                    ".s-result-item .a-link-normal",
                    ".sg-col-inner .a-link-normal",
                    "[data-asin] h2 a",
                    "[data-asin] .a-link-normal",
                    ".s-search-results .a-link-normal",
                    ".s-main-slot .a-link-normal"
                ]
                
                first_product = None
                selector_used = None
                product_href = None
                
                # Try each selector until one works - OPTIMIZED FOR SPEED
                for selector in product_selectors:
                    try:
                        # Flash sale mode: instant detection (0.3 seconds max)
                        first_product = WebDriverWait(self.driver, 0.3).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        selector_used = selector
                        logging.info(f"Found product: {selector}")
                        break
                    except TimeoutException:
                        continue
                
                if not first_product:
                    logging.error("Could not find any product links with available selectors")
                    # Take a screenshot for debugging
                    try:
                        self.driver.save_screenshot("logs/product_selection_failed.png")
                        logging.info("Screenshot saved to logs/product_selection_failed.png")
                    except:
                        pass
                    return False
                
                # Get product info before clicking for logging
                try:
                    product_href = first_product.get_attribute('href')
                    logging.info(f"Product link: {product_href}")
                except:
                    pass
                
                # Try clicking with multiple methods for stability
                click_success = False
                
                # Method 1: Regular click
                try:
                    first_product.click()
                    click_success = True
                    logging.info("Product clicked successfully (regular click)")
                except Exception as e:
                    logging.warning(f"Regular click failed: {e}")
                
                # Method 2: JavaScript click if regular click fails
                if not click_success:
                    try:
                        self.driver.execute_script("arguments[0].click();", first_product)
                        click_success = True
                        logging.info("Product clicked successfully (JavaScript click)")
                    except Exception as e:
                        logging.warning(f"JavaScript click failed: {e}")
                
                # Method 3: Direct navigation if clicking fails
                if not click_success and product_href:
                    try:
                        self.driver.get(product_href)
                        click_success = True
                        logging.info("Product accessed successfully (direct navigation)")
                    except Exception as e:
                        logging.error(f"Direct navigation failed: {e}")
                
                if not click_success:
                    raise Exception("All click methods failed")
                
                # Wait for product page to load with multiple possible selectors
                product_title_selectors = [
                    "#productTitle",
                    ".product-title",
                    "h1.a-size-large",
                    "[data-feature-name='productTitle']"
                ]
                
                product_title_element = None
                for title_selector in product_title_selectors:
                    try:
                        product_title_element = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, title_selector))
                        )
                        break
                    except TimeoutException:
                        continue
                
                if product_title_element:
                    product_title = product_title_element.text
                    logging.info(f"Selected product: {product_title}")
                else:
                    logging.warning("Could not find product title, but page seems to have loaded")
                    product_title = "Unknown Product"
                
                return True
                
            except Exception as e:
                logging.error(f"Product selection failed (attempt {attempt + 1}): {str(e)}")
                
                # Check if it's a tab crash
                if "tab crashed" in str(e).lower() or "session" in str(e).lower():
                    logging.error("Chrome tab crashed - attempting recovery")
                    if attempt < max_retries - 1:
                        try:
                            self._recover_driver()
                            # Re-search for the product after recovery
                            self.driver.get("https://www.amazon.in")
                            time.sleep(1)
                            continue
                        except Exception as recovery_e:
                            logging.error(f"Driver recovery failed: {recovery_e}")
                
                # Take a screenshot for debugging on final attempt
                if attempt == max_retries - 1:
                    try:
                        self.driver.save_screenshot("logs/product_selection_error.png")
                        logging.info("Error screenshot saved to logs/product_selection_error.png")
                    except:
                        pass
                
                if attempt == max_retries - 1:
                    return False
                else:
                    time.sleep(1)  # Brief pause before retry
        
        return False
    
    def add_to_cart(self, flash_sale_mode=True):
        """Add the selected product to cart - OPTIMIZED FOR FLASH SALES."""
        try:
            logging.info("FLASH SALE: Adding to cart...")
            
            # Extended list of selectors for "Add to Cart" button (Amazon changes these frequently)
            add_to_cart_selectors = [
                "#add-to-cart-button",
                "input[name='submit.add-to-cart']",
                "[data-testid='add-to-cart-button']",
                "input[value='Add to Cart']",
                "button[name='submit.add-to-cart']",
                ".a-button-input[aria-labelledby='submit.add-to-cart-announce']",
                "input[title='Add to Cart']",
                "input[alt='Add to Cart']",
                "#add-to-cart-button-ubb",
                "button[data-action='add-to-cart']",
                ".a-button[data-action='add-to-cart']",
                "input.a-button-input[name='submit.add-to-cart']",
                "input[type='submit'][name*='add-to-cart']",
                "button[type='submit'][name*='add-to-cart']",
                ".add-to-cart-button",
                "[id*='add-to-cart']",
                "[class*='add-to-cart']"
            ]
            
            add_to_cart_btn = None
            selector_used = None
            
            # Try each selector until one works - FLASH SALE OPTIMIZED
            for selector in add_to_cart_selectors:
                try:
                    # Ultra-fast detection: 0.2 seconds max per selector
                    add_to_cart_btn = WebDriverWait(self.driver, 0.2).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    selector_used = selector
                    logging.info(f"Cart btn found: {selector}")
                    break
                except TimeoutException:
                    continue
            
            # FLASH SALE INSTANT FALLBACK: Try to find elements immediately
            if not add_to_cart_btn and flash_sale_mode:
                logging.info("FLASH: Instant fallback...")
                try:
                    # Instant search - no waiting
                    elements = self.driver.find_elements(By.CSS_SELECTOR, "button, input[type='submit'], input[type='button']")
                    for elem in elements:
                        try:
                            text = (elem.text or elem.get_attribute('value') or '').lower()
                            if 'add to cart' in text or 'add to basket' in text:
                                if elem.is_displayed() and elem.is_enabled():
                                    add_to_cart_btn = elem
                                    logging.info(f"FLASH: Found '{text}'")
                                    break
                        except:
                            continue
                    if add_to_cart_btn:
                        selector_used = "flash-instant"
                except Exception:
                    pass
            
            if not add_to_cart_btn:
                logging.error("Could not find Add to Cart button with any known selector")
                if not flash_sale_mode:
                    logging.info("Attempting fallback: searching for buttons with 'add to cart' text...")
                
                # Take a screenshot for debugging
                try:
                    self.driver.save_screenshot("logs/add_to_cart_failed.png")
                    logging.info("Screenshot saved to logs/add_to_cart_failed.png")
                except:
                    pass
                
                # Fallback: find buttons by text content
                try:
                    buttons = self.driver.find_elements(By.TAG_NAME, "button") + self.driver.find_elements(By.TAG_NAME, "input")
                    candidate_buttons = []
                    
                    for btn in buttons:
                        try:
                            # Get all possible text sources for the button
                            btn_text = (
                                btn.get_attribute('value') or 
                                btn.text or 
                                btn.get_attribute('title') or 
                                btn.get_attribute('aria-label') or 
                                btn.get_attribute('alt') or 
                                ''
                            ).strip().lower()
                            
                            # Look for cart-related text
                            cart_phrases = [
                                'add to cart',
                                'add to basket', 
                                'add item',
                                'buy now',
                                'purchase'
                            ]
                            
                            for phrase in cart_phrases:
                                if phrase in btn_text:
                                    # Check if button is visible and clickable
                                    if btn.is_displayed() and btn.is_enabled():
                                        candidate_buttons.append((btn, btn_text, phrase))
                                        logging.info(f"Found clickable cart button: '{btn_text}' (matched: '{phrase}')")
                                        break
                            
                        except Exception as btn_e:
                            continue
                    
                    # Try to use the first viable candidate
                    if candidate_buttons:
                        # Prioritize exact "add to cart" matches
                        best_btn = None
                        for btn, text, phrase in candidate_buttons:
                            if 'add to cart' in phrase:
                                best_btn = btn
                                logging.info(f"Using best match: '{text}'")
                                break
                        
                        if not best_btn:
                            best_btn = candidate_buttons[0][0]
                            logging.info(f"Using first candidate: '{candidate_buttons[0][1]}'")
                        
                        add_to_cart_btn = best_btn
                        selector_used = "text-based fallback"
                    
                except Exception as fallback_e:
                    logging.error(f"Fallback button search failed: {fallback_e}")
                
                if not add_to_cart_btn:
                    raise Exception("Could not find Add to Cart button even with text-based fallback")
            
            # Get button info before clicking for logging
            try:
                btn_text = add_to_cart_btn.get_attribute('value') or add_to_cart_btn.text or add_to_cart_btn.get_attribute('title')
                logging.info(f"Clicking button with text: '{btn_text}'")
            except:
                pass
            
            add_to_cart_btn.click()
            
            logging.info("FLASH: Cart button clicked")
            
            if flash_sale_mode:
                # FLASH SALE: Minimal verification, maximum speed
                time.sleep(0.5)  # Minimal wait
                try:
                    # Quick check for cart count only
                    cart_count = self.driver.find_element(By.CSS_SELECTOR, "#nav-cart-count, .nav-cart-count")
                    if cart_count:
                        logging.info("FLASH: Cart confirmed")
                except:
                    pass  # Don't wait - assume success for speed
            else:
                # Normal mode: Full verification
                time.sleep(3)  # Wait for cart update
                try:
                    cart_indicators = ["#nav-cart-count", ".nav-cart-count", "#sw-atc-confirmation-container", ".a-alert-success"]
                    for indicator in cart_indicators:
                        try:
                            element = WebDriverWait(self.driver, 2).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, indicator))
                            )
                            logging.info(f"Cart update confirmed via: {indicator}")
                            break
                        except TimeoutException:
                            continue
                except:
                    pass
            
            logging.info("Product added to cart successfully")
            return True
            
        except Exception as e:
            logging.error(f"Add to cart failed: {str(e)}")
            # Take a screenshot for debugging
            try:
                self.driver.save_screenshot("logs/add_to_cart_error.png")
                logging.info("Error screenshot saved to logs/add_to_cart_error.png")
            except:
                pass
            return False
    
    def proceed_to_checkout(self):
        """Proceed to checkout process."""
        try:
            logging.info("Proceeding to checkout...")
            
            # Navigate to cart first
            self.driver.get("https://www.amazon.in/gp/cart/view.html")
            
            # Find checkout button
            checkout_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "proceedToRetailCheckout"))
            )
            
            checkout_btn.click()
            
            logging.info("Navigated to checkout page")
            return True
            
        except Exception as e:
            logging.error(f"Checkout navigation failed: {str(e)}")
            return False
    
    def flash_sale_purchase(self, product_name):
        """ULTRA-FAST purchase for flash sales - OPTIMIZED FOR SPEED."""
        start_time = time.time()
        try:
            logging.info(f"FLASH SALE MODE: Starting purchase for '{product_name}'")
            
            # Setup browser (should be pre-connected)
            self.setup_driver()
            
            # Quick login check
            if not self.login_to_amazon():
                return False
            
            # Speed-optimized search
            if not self.search_product(product_name):
                return False
            
            # Store current search for potential recovery
            current_search = product_name
            
            # Instant product selection  
            if not self.select_first_product():
                # If product selection failed due to crash, try to search again
                logging.warning("Product selection failed, attempting search recovery...")
                if self.search_product(current_search):
                    if not self.select_first_product():
                        return False
                else:
                    return False
            
            # Lightning-fast add to cart
            if not self.add_to_cart(flash_sale_mode=True):
                return False
            
            elapsed = time.time() - start_time
            logging.info(f"FLASH SALE COMPLETED in {elapsed:.2f} seconds!")
            
            return True
            
        except Exception as e:
            elapsed = time.time() - start_time
            logging.error(f"FLASH SALE FAILED after {elapsed:.2f} seconds: {str(e)}")
            return False
    
    def complete_purchase(self, product_name):
        """Complete the entire purchase process - NORMAL MODE."""
        try:
            # Setup browser
            self.setup_driver()
            
            # Login
            if not self.login_to_amazon():
                return False
            
            # Search for product
            if not self.search_product(product_name):
                return False
            
            # Select first product
            if not self.select_first_product():
                return False
            
            # Add to cart
            if not self.add_to_cart(flash_sale_mode=False):
                return False
            
            # Proceed to checkout
            if not self.proceed_to_checkout():
                return False
            
            # Note: Actual purchase completion would require payment method selection
            # and final confirmation. This is deliberately left incomplete for safety.
            logging.warning("PURCHASE PROCESS STOPPED AT CHECKOUT FOR SAFETY")
            logging.info("Manual intervention required to complete purchase")
            
            return True
            
        except Exception as e:
            logging.error(f"Purchase process failed: {str(e)}")
            return False
        
        finally:
            if self.driver:
                # Don't close browser if we're reusing an existing session
                reuse_browser = self.config.get('settings', {}).get('reuse_existing_browser', True)
                if not reuse_browser:
                    input("Press Enter to close the browser...")
                    self.driver.quit()
                else:
                    logging.info("Browser session will remain open for reuse")
                    # Just disconnect from the session instead of closing
                    try:
                        self.driver.quit()
                    except:
                        pass  # Ignore errors when disconnecting from existing session


def main():
    """Main function to run the Amazon Auto Buyer."""
    buyer = AmazonAutoBuyer()
    
    # Get product name from user input or config
    product_name = input("Enter the product name to search for: ")
    
    if not product_name.strip():
        print("No product name provided. Exiting...")
        return
    
    # Start the purchase process
    success = buyer.complete_purchase(product_name)
    
    if success:
        print("Process completed successfully!")
    else:
        print("Process failed. Check logs for details.")


if __name__ == "__main__":
    main()