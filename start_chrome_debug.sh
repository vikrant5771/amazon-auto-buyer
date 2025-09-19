#!/bin/bash

# Start Chrome with remote debugging enabled
# This allows the Amazon Auto Buyer to connect to an existing Chrome session
# instead of opening a new browser window every time

echo "Starting Chrome with remote debugging enabled..."
echo "The Amazon Auto Buyer will be able to connect to this Chrome session."
echo "Leave this Chrome window open while using the Amazon Auto Buyer."
echo ""
echo "To close this Chrome session later, just close the browser normally."
echo ""

# Check if Chrome is already running on the debug port
if lsof -Pi :9222 -sTCP:LISTEN -t >/dev/null ; then
    echo "Chrome is already running with remote debugging on port 9222"
    echo "You can use the existing session or close it first to start a new one."
    exit 0
fi

# Start Chrome with remote debugging
# Using Google Chrome on macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
    --remote-debugging-port=9222 \
    --user-data-dir=/tmp/chrome-debug-session \
    --disable-web-security \
    --disable-features=VizDisplayCompositor \
    --new-window \
    "https://amazon.in" &

echo "Chrome started with remote debugging on port 9222"
echo "Amazon.in should open automatically"
echo "You can now run the Amazon Auto Buyer script"
echo ""
echo "IMPORTANT: Keep this Chrome window open while using the Auto Buyer"