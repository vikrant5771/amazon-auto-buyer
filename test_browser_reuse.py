#!/usr/bin/env python3
"""
Quick test script to verify browser reuse functionality.
This script will test if the browser connection works without running the full automation.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from amazon_buyer import AmazonAutoBuyer
import logging

def test_browser_connection():
    """Test browser connection without running full automation."""
    print("Testing browser reuse functionality...")
    print("=" * 50)
    
    # Create buyer instance
    buyer = AmazonAutoBuyer()
    
    try:
        # Test browser setup
        print("1. Setting up WebDriver connection...")
        buyer.setup_driver()
        
        if buyer.driver:
            print("✅ Successfully connected to browser!")
            print(f"   Current URL: {buyer.driver.current_url}")
            print(f"   Browser title: {buyer.driver.title}")
            
            # Test navigation
            print("\n2. Testing navigation to Amazon...")
            buyer.driver.get("https://amazon.in")
            print(f"✅ Successfully navigated to Amazon")
            print(f"   Page title: {buyer.driver.title}")
            
            print("\n3. Browser connection test completed successfully!")
            print("   The browser session is working and ready to use.")
            
        else:
            print("❌ Failed to connect to browser")
            
    except Exception as e:
        print(f"❌ Error during browser test: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure Chrome is running with remote debugging:")
        print("   ./start_chrome_debug.sh")
        print("2. Check if port 9222 is available:")
        print("   lsof -i :9222")
        print("3. Try setting reuse_existing_browser to false in config.json")
        
    finally:
        if buyer.driver:
            print(f"\n4. Cleaning up connection...")
            try:
                # Don't close the browser, just disconnect
                buyer.driver.quit()
                print("✅ Cleanly disconnected from browser session")
            except:
                pass

if __name__ == "__main__":
    test_browser_connection()