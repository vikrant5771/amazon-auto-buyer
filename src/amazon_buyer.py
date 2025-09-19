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
        
        # Add user preferences
        if self.config.get('headless', False):
            chrome_options.add_argument('--headless')
            
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Set user agent to avoid detection
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def login_to_amazon(self):
        """Login to Amazon with stored credentials."""
        try:
            logging.info("Navigating to Amazon login page...")
            self.driver.get("https://www.amazon.com/ap/signin")
            
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
                self.driver.get("https://www.amazon.com")
            
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
        """Select the first available product from search results."""
        try:
            logging.info("Selecting first product from search results...")
            
            # Find first product link
            first_product = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-component-type='s-search-result'] h2 a"))
            )
            
            first_product.click()
            
            # Wait for product page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "productTitle"))
            )
            
            product_title = self.driver.find_element(By.ID, "productTitle").text
            logging.info(f"Selected product: {product_title}")
            
            return True
            
        except Exception as e:
            logging.error(f"Product selection failed: {str(e)}")
            return False
    
    def add_to_cart(self):
        """Add the selected product to cart."""
        try:
            logging.info("Adding product to cart...")
            
            # Look for "Add to Cart" button
            add_to_cart_selectors = [
                "#add-to-cart-button",
                "input[name='submit.add-to-cart']",
                "[data-testid='add-to-cart-button']"
            ]
            
            add_to_cart_btn = None
            for selector in add_to_cart_selectors:
                try:
                    add_to_cart_btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if not add_to_cart_btn:
                raise Exception("Could not find Add to Cart button")
            
            add_to_cart_btn.click()
            
            logging.info("Product added to cart successfully")
            time.sleep(2)  # Wait for cart update
            
            return True
            
        except Exception as e:
            logging.error(f"Add to cart failed: {str(e)}")
            return False
    
    def proceed_to_checkout(self):
        """Proceed to checkout process."""
        try:
            logging.info("Proceeding to checkout...")
            
            # Navigate to cart first
            self.driver.get("https://www.amazon.com/gp/cart/view.html")
            
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
    
    def complete_purchase(self, product_name):
        """Complete the entire purchase process."""
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
            if not self.add_to_cart():
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
                input("Press Enter to close the browser...")
                self.driver.quit()


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