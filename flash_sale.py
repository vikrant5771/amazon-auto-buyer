#!/usr/bin/env python3
"""
Amazon Flash Sale Auto-Buyer
Ultra-fast version optimized for flash sales with sub-second response times.
"""

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from amazon_buyer import AmazonAutoBuyer
import logging

def flash_sale_mode():
    """Run the buyer in ultra-fast flash sale mode."""
    print("🔥 FLASH SALE MODE - MAXIMUM SPEED! 🔥")
    print("=" * 50)
    
    # Get product name
    product_name = input("Enter product name for flash sale: ").strip()
    
    if not product_name:
        print("❌ No product name provided. Exiting...")
        return
    
    print(f"🎯 TARGET: {product_name}")
    print("⚡ Optimizing for speed...")
    print("💡 TIP: Keep Chrome browser already open on Amazon.in for fastest results")
    print()
    
    # Countdown
    for i in range(3, 0, -1):
        print(f"Starting in {i}...")
        time.sleep(1)
    
    print("🚀 LAUNCHING FLASH SALE ATTACK!")
    print("-" * 40)
    
    # Create buyer instance
    buyer = AmazonAutoBuyer()
    
    # Execute flash sale purchase
    start_time = time.time()
    success = buyer.flash_sale_purchase(product_name)
    elapsed = time.time() - start_time
    
    print("-" * 40)
    if success:
        print(f"✅ FLASH SALE SUCCESS in {elapsed:.2f} seconds! 🎉")
        print("🛒 Product added to cart!")
        print("💳 Check your cart to complete purchase manually")
    else:
        print(f"❌ FLASH SALE FAILED after {elapsed:.2f} seconds")
        print("📝 Check logs/amazon_buyer.log for details")
    
    print("=" * 50)

if __name__ == "__main__":
    flash_sale_mode()