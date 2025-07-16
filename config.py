#!/usr/bin/env python3
"""
Configuration file for Sider AI automation script.
"""

# URLs
SIDER_REFERRAL_URL = "https://sider.ai/invited?c=3eaf48d0e40b6927a29c5db701b17b56"
CHROME_EXTENSION_URL = "https://chromewebstore.google.com/detail/sider-chat-with-all-ai-mo/difoiogjjojoaoomphldepapgpbgkhkb?pli=1"

# Browser settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
DEFAULT_WAIT_TIME = 60
INSTALL_WAIT_TIME = 10
ACCOUNT_DELAY = 30  # Seconds to wait between processing accounts

# PyAutoGUI coordinates for "Add extension" button
# These may need to be adjusted based on your screen resolution
# Run test.py to get the correct coordinates for your setup
ADD_EXTENSION_BUTTON_X = 784
ADD_EXTENSION_BUTTON_Y = 270

# File paths
ACCOUNT_LIST_FILE = "list_account.txt"
LOG_FILE = "sider_automation.log"

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"