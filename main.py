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
        # Điền email
        email_input = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
        email_input.send_keys(email)
        
        # Kiểm tra robot verification sau khi điền email
        handle_robot_verification()
        
        next_button_email = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Next')]")))
        click_element(next_button_email, "Next sau email")
        
        # Điền mật khẩu
        # Đợi một chút để trang load sau khi click Next
        logging.info("Đợi trang nhập mật khẩu load...")
        time.sleep(5) # Tăng thời gian chờ lên 5 giây
        
        # Kiểm tra robot verification trước khi điền password
        handle_robot_verification()
        
        logging.info("Đang tìm ô nhập mật khẩu...")
        # Thử dùng element_to_be_clickable và selector CSS linh hoạt hơn
        password_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']"))) 
        # Hoặc giữ lại selector cũ nếu CSS không hoạt động:
        # password_input = wait.until(EC.element_to_be_clickable((By.NAME, "password"))) 
        logging.info("Đã tìm thấy ô mật khẩu. Đang điền...")
        password_input.send_keys(password)
        logging.info("Đã điền mật khẩu. Đang tìm nút Next...")
        
        # Kiểm tra robot verification sau khi điền password
        handle_robot_verification()
        
        next_button_password = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Next')]")))
        click_element(next_button_password, "Next sau password")

        # Wait for login window to close
        wait.until(lambda driver: len(driver.window_handles) == 1)
        driver.switch_to.window(driver.window_handles[0])
        
        # Install Chrome extension
        install_chrome_extension(driver, wait)
        
        logging.info(f"Successfully processed account (attempted extension install): {email}")
        
        # Chuyển đến trang Chrome Web Store
        driver.get("https://chromewebstore.google.com/detail/sider-chat-with-all-ai-mo/difoiogjjojoaoomphldepapgpbgkhkb?pli=1")
        
        # Kiểm tra robot verification trên trang Chrome Web Store
        handle_robot_verification()
        
        # Selector cho nút "Add to Chrome" có thể khác nhau, cần kiểm tra
        # Ví dụ: //button[contains(@aria-label, 'Add to Chrome')] hoặc dựa vào text trong button/div
        logging.info("Đang tìm nút 'Add to Chrome'")
        add_button_selector = "//button[contains(., 'Add to Chrome')] | //div[contains(., 'Add to Chrome') and @role='button']"
        add_button = wait.until(EC.element_to_be_clickable((By.XPATH, add_button_selector)))
        logging.info("Đã tìm thấy nút 'Add to Chrome'. Đang click...")
        click_element(add_button, "'Add to Chrome'")
        
        # --- Xử lý hộp thoại "Add extension" ---
        def handle_add_extension_dialog():
            logging.info("Đợi hộp thoại 'Add extension' của trình duyệt xuất hiện...")
            max_attempts = 3
            
            for attempt in range(max_attempts):
                time.sleep(3 + attempt)  # Tăng thời gian chờ mỗi lần thử
                
                try:
                    # Thử tìm và click bằng Selenium trước
                    confirm_selectors = [
                        "//button[contains(text(), 'Add extension')]",
                        "//button[contains(text(), 'Thêm tiện ích mở rộng')]",
                        "//*[@role='button' and contains(text(), 'Add extension')]",
                        "//div[contains(@class, 'infobar') or contains(@class, 'dialog')]//button[contains(text(), 'Add')]"
                    ]
                    
                    for selector in confirm_selectors:
                        try:
                            confirm_button = driver.find_element(By.XPATH, selector)
                            if confirm_button.is_displayed():
                                driver.execute_script("arguments[0].click();", confirm_button)
                                logging.info(f"Đã click 'Add extension' bằng Selenium (attempt {attempt + 1})")
                                return True
                        except:
                            continue
                    
                    # Nếu không tìm thấy bằng Selenium, thử PyAutoGUI
                    logging.info(f"Không tìm thấy bằng Selenium, thử PyAutoGUI (attempt {attempt + 1})")
                    add_extension_button_x = 784
                    add_extension_button_y = 270
                    
                    pyautogui.click(x=add_extension_button_x, y=add_extension_button_y)
                    logging.info(f"Đã click bằng PyAutoGUI tại ({add_extension_button_x}, {add_extension_button_y})")
                    return True
                    
                except Exception as e:
                    logging.warning(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == max_attempts - 1:
                        logging.error("Tất cả attempts đều thất bại")
                        return False
            
            return False
        
        # Thực hiện click hộp thoại
        dialog_handled = handle_add_extension_dialog()
        if not dialog_handled:
            logging.error("Không thể xử lý hộp thoại 'Add extension'")
        
        # Kiểm tra robot verification sau khi click "Add extension"
        time.sleep(2)  # Chờ một chút để trang phản ứng
        handle_robot_verification()
        # -------------------------------------------------------------------

        # Đợi và xác nhận tiện ích đã được cài đặt thành công
        def wait_for_extension_installation():
            max_wait_time = 60  # Tối đa 60 giây
            check_interval = 3  # Kiểm tra mỗi 3 giây
            elapsed_time = 0
            
            logging.info("Đang chờ xác nhận tiện ích được cài đặt...")
            original_url = driver.current_url
            
            while elapsed_time < max_wait_time:
                try:
                    # Phương pháp 1: Kiểm tra thông báo thành công trên trang Chrome Web Store
                    if "chromewebstore.google.com" in driver.current_url:
                        success_indicators = [
                            "//div[contains(text(), 'added to Chrome')]",
                            "//div[contains(text(), 'Extension added')]", 
                            "//div[contains(text(), 'successfully')]",
                            "//span[contains(text(), 'added')]",
                            "//*[contains(text(), 'Sider') and contains(text(), 'added')]",
                            "//button[contains(text(), 'Remove from Chrome')]",  # Nút Remove thay vì Add
                            "//button[contains(text(), 'Added to Chrome')]"
                        ]
                        
                        for indicator in success_indicators:
                            try:
                                elements = driver.find_elements(By.XPATH, indicator)
                                for element in elements:
                                    if element.is_displayed():
                                        logging.info(f"Tìm thấy xác nhận cài đặt thành công: {element.text}")
                                        return True
                            except:
                                continue
                    
                    # Phương pháp 2: Kiểm tra extension trong chrome://extensions/
                    try:
                        logging.debug("Kiểm tra trang extensions...")
                        driver.execute_script("window.open('chrome://extensions/', '_blank');")
                        driver.switch_to.window(driver.window_handles[-1])
                        time.sleep(2)
                        
                        # Tìm Sider extension bằng nhiều cách
                        extension_indicators = [
                            "//*[contains(text(), 'Sider')]",
                            "//*[contains(text(), 'Chat with all AI models')]",
                            "//div[@id='items-list']//div[contains(@class, 'extension-list-item-wrapper')]",
                            "//*[contains(text(), 'difoiogjjojoaoomphldepapgpbgkhkb')]"  # Extension ID
                        ]
                        
                        for indicator in extension_indicators:
                            try:
                                elements = driver.find_elements(By.XPATH, indicator)
                                for element in elements:
                                    if element.is_displayed() and ("sider" in element.text.lower() or "chat" in element.text.lower()):
                                        logging.info(f"Tìm thấy Sider extension trong danh sách: {element.text}")
                                        driver.close()  # Đóng tab extensions
                                        driver.switch_to.window(driver.window_handles[0])
                                        return True
                            except:
                                continue
                        
                        # Đóng tab extensions và quay lại tab chính
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        
                    except Exception as e:
                        logging.debug(f"Lỗi khi kiểm tra extensions page: {e}")
                        # Đảm bảo quay lại tab chính
                        try:
                            if len(driver.window_handles) > 1:
                                driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                        except:
                            pass
                    
                    # Phương pháp 3: Kiểm tra popup thông báo
                    try:
                        notification_selectors = [
                            "//div[contains(@class, 'notification')]",
                            "//div[contains(@class, 'infobar')]",
                            "//div[contains(@class, 'toast')]",
                            "//*[@role='alert']"
                        ]
                        
                        for selector in notification_selectors:
                            try:
                                elements = driver.find_elements(By.XPATH, selector)
                                for element in elements:
                                    if (element.is_displayed() and 
                                        ("added" in element.text.lower() or 
                                         "installed" in element.text.lower() or
                                         "success" in element.text.lower())):
                                        logging.info(f"Tìm thấy thông báo cài đặt: {element.text}")
                                        return True
                            except:
                                continue
                    except:
                        pass
                    
                    # Đảm bảo đang ở đúng trang
                    if driver.current_url != original_url:
                        driver.get(original_url)
                        time.sleep(1)
                        
                except Exception as e:
                    logging.debug(f"Lỗi khi kiểm tra cài đặt: {e}")
                
                time.sleep(check_interval)
                elapsed_time += check_interval
                logging.info(f"Đã chờ {elapsed_time}/{max_wait_time} giây...")
            
            logging.warning("Hết thời gian chờ - không thể xác nhận tiện ích đã được cài đặt")
            return False
        
        # Phát hiện và xử lý robot verification
        def handle_robot_verification():
            try:
                logging.info("Kiểm tra robot verification...")
                max_wait_attempts = 5
                
                for attempt in range(max_wait_attempts):
                    time.sleep(2)  # Chờ một chút để trang load
                    
                    # Các selector phổ biến cho CAPTCHA/robot verification
                    captcha_selectors = [
                        "//iframe[contains(@src, 'recaptcha') or contains(@title, 'reCAPTCHA')]",
                        "//*[@id='recaptcha']",
                        "//div[contains(@class, 'recaptcha')]",
                        "//*[contains(text(), 'verify') and contains(text(), 'robot')]",
                        "//*[contains(text(), 'I am not a robot')]",
                        "//*[contains(text(), 'Tôi không phải robot')]",
                        "//input[@type='checkbox' and contains(@aria-label, 'robot')]",
                        "//div[contains(@class, 'g-recaptcha')]",
                        "//*[contains(@class, 'captcha')]",
                        "//iframe[contains(@name, 'a-') and contains(@src, 'google.com')]"
                    ]
                    
                    captcha_found = False
                    for selector in captcha_selectors:
                        try:
                            captcha_elements = driver.find_elements(By.XPATH, selector)
                            for captcha_element in captcha_elements:
                                if captcha_element.is_displayed():
                                    logging.info(f"Phát hiện robot verification (attempt {attempt + 1}): {selector}")
                                    captcha_found = True
                                    
                                    # Xử lý checkbox "I'm not a robot"
                                    if "checkbox" in selector.lower() or "robot" in captcha_element.get_attribute("aria-label") or "":
                                        try:
                                            # Thử click trực tiếp
                                            captcha_element.click()
                                            logging.info("Đã click checkbox 'I'm not a robot' (direct click)")
                                            time.sleep(3)
                                        except:
                                            try:
                                                # Thử click bằng JavaScript
                                                driver.execute_script("arguments[0].click();", captcha_element)
                                                logging.info("Đã click checkbox 'I'm not a robot' (JavaScript)")
                                                time.sleep(3)
                                            except Exception as e:
                                                logging.warning(f"Không thể click checkbox: {e}")
                                    
                                    # Xử lý iframe reCAPTCHA
                                    elif "iframe" in selector.lower() and "recaptcha" in selector.lower():
                                        try:
                                            # Chuyển vào iframe
                                            driver.switch_to.frame(captcha_element)
                                            time.sleep(1)
                                            
                                            # Tìm checkbox trong iframe
                                            checkbox = driver.find_element(By.CSS_SELECTOR, ".recaptcha-checkbox-border")
                                            checkbox.click()
                                            logging.info("Đã click vào reCAPTCHA checkbox trong iframe")
                                            
                                            # Chuyển ra khỏi iframe
                                            driver.switch_to.default_content()
                                            time.sleep(5)
                                        except Exception as e:
                                            logging.warning(f"Không thể xử lý reCAPTCHA iframe: {e}")
                                            driver.switch_to.default_content()
                                    
                                    break
                        except:
                            continue
                    
                    if captcha_found:
                        # Chờ thêm để CAPTCHA được xử lý
                        logging.info("Đã phát hiện CAPTCHA - chờ 10 giây để xử lý...")
                        time.sleep(10)
                        
                        # Kiểm tra xem CAPTCHA đã được giải quyết chưa
                        captcha_still_present = False
                        for selector in captcha_selectors:
                            try:
                                elements = driver.find_elements(By.XPATH, selector)
                                for element in elements:
                                    if element.is_displayed():
                                        captcha_still_present = True
                                        break
                                if captcha_still_present:
                                    break
                            except:
                                continue
                        
                        if not captcha_still_present:
                            logging.info("CAPTCHA đã được giải quyết thành công")
                            return True
                        else:
                            logging.info("CAPTCHA vẫn hiện diện - chờ thêm...")
                            if attempt < max_wait_attempts - 1:
                                time.sleep(15)  # Chờ lâu hơn cho CAPTCHA phức tạp
                            continue
                    else:
                        logging.info(f"Không phát hiện robot verification (attempt {attempt + 1})")
                        return False
                
                logging.warning("Đã hết attempts cho robot verification")
                return False
                
            except Exception as e:
                logging.error(f"Lỗi khi xử lý robot verification: {e}")
                return False
        
        # Xử lý robot verification trước khi chờ cài đặt
        handle_robot_verification()
        
        # Chờ xác nhận cài đặt
        installation_success = wait_for_extension_installation()
        
        if installation_success:
            logging.info(f"Successfully processed account - Extension installed: {email}")
        else:
            logging.warning(f"Processed account but couldn't confirm extension installation: {email}")
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
