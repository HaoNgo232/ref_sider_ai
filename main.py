#!/usr/bin/env python3
"""
Sider AI Registration Automation Script
Automates the registration process for Sider AI accounts and Chrome extension installation.
"""

import logging
import os
import tempfile
import shutil
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# Import configuration
from config import *

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL), 
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def setup_chrome_driver(temp_dir):
    """Setup Chrome driver with optimized options."""
    chrome_options = Options()
    chrome_options.add_argument(f'--user-data-dir={temp_dir}')
    chrome_options.add_argument('--remote-allow-origins=*')
    chrome_options.add_argument('--no-first-run')
    chrome_options.add_argument('--no-service-autorun')
    chrome_options.add_argument('--no-default-browser-check')
    chrome_options.add_argument('--homepage=about:blank')
    chrome_options.add_argument('--no-pings')
    chrome_options.add_argument('--password-store=basic')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-breakpad')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-session-crashed-bubble')
    chrome_options.add_argument('--disable-features=IsolateOrigins,site-per-process')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def setup_window(driver):
    """Setup fixed window size and position."""
    try:
        logging.info(f"Setting fixed window size and position ({WINDOW_WIDTH}x{WINDOW_HEIGHT} at 0,0)")
        driver.set_window_position(0, 0)
        driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        time.sleep(1)  # Wait for window to stabilize
    except Exception as e:
        logging.warning(f"Could not set window size/position: {e}")


def click_element(driver, element, description):
    """Helper function to click elements with fallback methods."""
    try:
        driver.execute_script("arguments[0].click();", element)
        logging.info(f"Clicked {description} (JavaScript)")
    except Exception as e:
        logging.warning(f"Click {description} with JavaScript failed: {e}. Trying regular click.")
        try:
            element.click()
            logging.info(f"Clicked {description} (regular)")
        except Exception as e2:
            logging.error(f"All click methods failed for {description}: {e2}")
            raise


def handle_google_login(driver, wait, email, password):
    """Handle Google login process."""
    # Fill email
    email_input = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
    email_input.send_keys(email)
    next_button_email = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Next')]")))
    click_element(driver, next_button_email, "Next after email")
    
    # Fill password
    logging.info("Waiting for password page to load...")
    time.sleep(5)  # Wait for page transition
    logging.info("Looking for password input...")
    password_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
    logging.info("Found password field. Filling...")
    password_input.send_keys(password)
    logging.info("Password filled. Looking for Next button...")
    next_button_password = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Next')]")))
    click_element(driver, next_button_password, "Next after password")


def handle_additional_steps(driver):
    """Handle additional Google verification steps if present."""
    try:
        # Look for "I understand" button
        understand_button_xpath = "//input[@type='submit' and (@value='Tôi hiểu' or @value='I understand')]"
        logging.info(f"Looking for 'I understand' button with XPath: {understand_button_xpath}")
        understand_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, understand_button_xpath))
        )
        click_element(driver, understand_button, "'I understand'")
        
        # Look for Continue button
        logging.info("Looking for 'Continue' button")
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Continue')]"))
        )
        click_element(driver, continue_button, "'Continue'")
    except Exception:
        logging.warning("No additional steps found or not needed")


def get_extension_button_coordinates():
    """Get coordinates for the 'Add extension' button - can be customized per screen."""
    # Coordinates from config - can be updated based on your screen resolution
    # You can run test.py to get the exact coordinates for your setup
    return ADD_EXTENSION_BUTTON_X, ADD_EXTENSION_BUTTON_Y


def install_chrome_extension(driver, wait):
    """Install the Sider Chrome extension."""
    driver.get(CHROME_EXTENSION_URL)
    
    logging.info("Looking for 'Add to Chrome' button")
    add_button_selector = "//button[contains(., 'Add to Chrome')] | //div[contains(., 'Add to Chrome') and @role='button']"
    add_button = wait.until(EC.element_to_be_clickable((By.XPATH, add_button_selector)))
    logging.info("Found 'Add to Chrome' button. Clicking...")
    click_element(driver, add_button, "'Add to Chrome'")
    
    # Use PyAutoGUI to click the browser confirmation dialog
    logging.info("Waiting for browser 'Add extension' dialog to appear...")
    time.sleep(4)  # Wait for dialog to appear
    
    add_extension_button_x, add_extension_button_y = get_extension_button_coordinates()
    
    try:
        logging.info(f"Attempting to click 'Add extension' button at ({add_extension_button_x}, {add_extension_button_y}) using pyautogui")
        pyautogui.click(x=add_extension_button_x, y=add_extension_button_y)
        logging.info("Clicked using pyautogui.")
    except Exception as e:
        logging.error(f"Failed to click using pyautogui: {e}")
    
    # Wait for extension to install
    logging.info(f"Waiting {INSTALL_WAIT_TIME} seconds for extension to install...")

def process_account(email, password):
    """Process a single account for Sider AI registration."""
    temp_dir = tempfile.mkdtemp()
    try:
        # Setup Chrome driver
        driver = setup_chrome_driver(temp_dir)
        wait = WebDriverWait(driver, DEFAULT_WAIT_TIME)
        
        # Setup window
        setup_window(driver)

        # Navigate to Sider registration page
        driver.get(SIDER_REFERRAL_URL)
        
        # Click Register Now & Claim Rewards button
        logging.info("Looking for 'Register Now & Claim Rewards' button")
        try:
            register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Register Now & Claim Rewards')]")))
            logging.info("Found Register button with text")
        except Exception:
            logging.warning("Could not find Register button with text, trying alternative selector...")
            register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Register Now & Claim Rewards')]")))

        try:
            register_button.click()
            logging.info("Clicked Register button (regular)")
        except Exception as e:
            logging.warning(f"Regular click failed: {e}. Trying JavaScript click.")
            driver.execute_script("arguments[0].click();", register_button)
            logging.info("Clicked Register button (JavaScript)")

        # Wait for page transition
        time.sleep(2)

        # Click Continue with Google
        logging.info("Looking for 'Continue with Google' area")
        google_button_selector = "//div[contains(@class, 'col-[main]') and contains(@style, 'grid-row:1')]"
        google_button = wait.until(EC.element_to_be_clickable((By.XPATH, google_button_selector)))
        logging.info(f"Found Google button area with selector: {google_button_selector}")

        try:
            # Try ActionChains first
            actions = ActionChains(driver)
            actions.move_to_element(google_button).click().perform()
            logging.info("Clicked Google area with ActionChains")
        except Exception as e_ac:
            logging.warning(f"ActionChains click failed: {e_ac}. Trying JavaScript.")
            try:
                driver.execute_script("arguments[0].click();", google_button)
                logging.info("Clicked Google area (JavaScript)")
            except Exception as e_js:
                logging.warning(f"JavaScript click failed: {e_js}. Trying regular click.")
                try:
                    google_button.click()
                    logging.info("Clicked Google area (regular)")
                except Exception as e_click:
                    logging.error(f"All click methods failed for Google area: {e_click}")

        # Switch to Google login window
        wait.until(lambda driver: len(driver.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        logging.info("Switched to Google login window")

        # Handle Google login
        handle_google_login(driver, wait, email, password)

        # Handle additional verification steps
        handle_additional_steps(driver)

        # Wait for login window to close
        wait.until(lambda driver: len(driver.window_handles) == 1)
        driver.switch_to.window(driver.window_handles[0])
        
        # Install Chrome extension
        install_chrome_extension(driver, wait)
        
        logging.info(f"Successfully processed account (attempted extension install): {email}")
        
    except Exception as e:
        logging.error(f"Error processing account {email}: {e}")
    finally:
        try:
            driver.quit()
        except Exception:
            pass
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    """Main function to process all accounts from the list."""
    try:
        logging.info("Starting Sider AI automation script")
        
        # Check if account list file exists
        if not os.path.exists(ACCOUNT_LIST_FILE):
            logging.error(f"{ACCOUNT_LIST_FILE} file not found!")
            return
        
        with open(ACCOUNT_LIST_FILE, "r", encoding="utf-8") as f:
            accounts = [line.strip().split("|") for line in f if line.strip()]
        
        logging.info(f"Found {len(accounts)} accounts to process")
        
        for i, (email, password) in enumerate(accounts, 1):
            logging.info(f"Processing account {i}/{len(accounts)}: {email}")
            process_account(email, password)
            
            # Add delay between accounts to avoid rate limiting
            if i < len(accounts):
                logging.info(f"Waiting {ACCOUNT_DELAY} seconds before next account...")
                time.sleep(ACCOUNT_DELAY)
        
        logging.info("All accounts processed successfully")
        
    except Exception as e:
        logging.error(f"Error in main function: {e}")


if __name__ == '__main__':
    main()
