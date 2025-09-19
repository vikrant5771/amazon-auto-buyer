# Amazon Auto-Buyer

An automated Python script that can search for products on Amazon, add them to cart, and navigate to the checkout page using Selenium WebDriver.

## ⚠️ IMPORTANT DISCLAIMERS

**READ CAREFULLY BEFORE USING THIS SOFTWARE:**

1. **Legal and Ethical Considerations**: This software is provided for educational purposes only. Automated purchasing may violate Amazon's Terms of Service.

2. **Financial Risk**: This software can potentially make real purchases with real money. **USE AT YOUR OWN RISK.**

3. **No Warranty**: This software is provided "as is" without any warranty. The authors are not responsible for any unauthorized purchases, financial losses, or account suspensions.

4. **Account Security**: Never share your Amazon credentials. Store them securely and use this software only on trusted devices.

5. **Rate Limiting**: Excessive automation may trigger Amazon's anti-bot measures and could result in account suspension.

## Features

- Automated Amazon login
- Product search functionality
- Automatic product selection (first result)
- Add to cart functionality
- Navigate to checkout page
- Comprehensive logging
- Configurable settings
- Safety stops before final purchase

## Prerequisites

- Python 3.7 or higher
- Chrome web browser
- ChromeDriver (automatically managed by webdriver-manager)
- Valid Amazon account

## Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd amazon-auto-buyer
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your settings**
   ```bash
   cp config/config.json config/config.json.backup
   # Edit config/config.json with your Amazon credentials
   ```

## Configuration

Edit `config/config.json` with your settings:

```json
{
  "credentials": {
    "email": "your-amazon-email@example.com",
    "password": "your-amazon-password"
  },
  "settings": {
    "headless": false,
    "implicit_wait": 10,
    "page_load_timeout": 30,
    "max_retries": 3
  },
  "purchase_limits": {
    "max_price": 100.0,
    "confirmation_required": true
  },
  "product_preferences": {
    "prime_only": false,
    "min_rating": 4.0,
    "verified_seller_only": true
  }
}
```

### Configuration Options

- **credentials**: Your Amazon login credentials
- **headless**: Run browser in headless mode (true/false)
- **reuse_existing_browser**: Connect to existing Chrome session instead of opening new browser (true/false)
- **max_price**: Maximum price limit for purchases
- **confirmation_required**: Require manual confirmation before purchase
- **prime_only**: Only select Prime-eligible products
- **min_rating**: Minimum product rating threshold

## Usage

### Basic Usage

1. **Run the script**
   ```bash
   python src/amazon_buyer.py
   ```

2. **Enter the product name** when prompted

3. **Monitor the process** through the browser window and console logs

### Browser Reuse Feature

By default, the script is configured to reuse an existing Chrome browser session instead of opening a new browser window each time. This is more convenient and efficient.

#### To use browser reuse:

1. **Start Chrome with remote debugging** (first time setup):
   ```bash
   ./start_chrome_debug.sh
   ```
   This will open Chrome with Amazon.in and enable remote debugging.

2. **Run the Amazon Auto Buyer** as normal:
   ```bash
   python src/amazon_buyer.py
   ```
   The script will connect to your existing Chrome session.

3. **Keep the Chrome window open** between runs to reuse the same session.

#### To disable browser reuse:

Set `"reuse_existing_browser": false` in `config/config.json`. This will open a new browser window each time (old behavior).

### Safety Features

- The script **STOPS at checkout** and requires manual intervention to complete purchases
- Comprehensive logging to `logs/amazon_buyer.log`
- Browser window remains open for manual verification
- Price limit checks (if configured)

## Project Structure

```
amazon-auto-buyer/
├── src/
│   └── amazon_buyer.py      # Main automation script
├── config/
│   └── config.json          # Configuration file (not tracked in git)
├── logs/
│   └── amazon_buyer.log     # Log files
├── start_chrome_debug.sh    # Helper script to start Chrome with remote debugging
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Logging

The application creates detailed logs in `logs/amazon_buyer.log` including:

- Login attempts and results
- Product search results
- Cart operations
- Error messages and stack traces
- Timestamps for all operations

## Troubleshooting

### Common Issues

1. **ChromeDriver not found**
   - The webdriver-manager should handle this automatically
   - If issues persist, manually download ChromeDriver

2. **Login failures**
   - Check your credentials in `config/config.json`
   - Amazon may require 2FA - handle manually in browser
   - Account may be temporarily locked due to automation

3. **Element not found errors**
   - Amazon frequently changes their page structure
   - Check logs for specific selectors that failed
   - May need to update selectors in the code

4. **Slow performance**
   - Increase timeout values in configuration
   - Check your internet connection
   - Amazon may be rate-limiting requests

### Debug Mode

To run in debug mode with more verbose output:

1. Set logging level to DEBUG in the script
2. Run with `headless: false` to see browser actions
3. Check `logs/amazon_buyer.log` for detailed information

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use strong passwords** for your Amazon account
3. **Enable 2FA** on your Amazon account
4. **Run only on trusted networks**
5. **Regularly review your Amazon order history**
6. **Use dedicated test account** if possible

## Development

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Add your changes with appropriate tests
4. Update documentation
5. Submit a pull request

### Code Structure

- `AmazonAutoBuyer` class handles all automation logic
- Methods are separated by functionality (login, search, cart, etc.)
- Error handling and logging throughout
- Configuration-driven behavior

## Legal Notice

This software is for educational purposes only. Users are responsible for:

- Complying with Amazon's Terms of Service
- Ensuring legal use in their jurisdiction  
- Any financial transactions made using this software
- Securing their personal and financial information

## Contributing

Contributions are welcome! Please:

1. Read the code of conduct
2. Follow existing code style
3. Add tests for new features
4. Update documentation as needed

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support:

1. Check the troubleshooting section
2. Review existing issues on GitHub
3. Create a new issue with detailed information
4. Include log files (remove sensitive information)

---

**Remember: This software can make real purchases. Always test carefully and use at your own risk.**