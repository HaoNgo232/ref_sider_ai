from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains # Import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import tempfile
import shutil
import logging
import pyautogui

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_account(email, password):
    temp_dir = tempfile.mkdtemp()
    try:
        # Thiết lập Chrome options
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

        # Khởi tạo trình duyệt
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 60)

        # --- Cố định kích thước và vị trí cửa sổ ---
        window_width = 1280
        window_height = 720
        try:
            logging.info(f"Setting fixed window size and position ({window_width}x{window_height} at 0,0)")
            driver.set_window_position(0, 0)
            driver.set_window_size(window_width, window_height)
            # Cần import time ở đầu file nếu chưa có
            import time 
            time.sleep(1) # Chờ cửa sổ ổn định
        except Exception as e:
            logging.warning(f"Could not set window size/position: {e}")
        # -----------------------------------------

        # Mở trang Sider
        driver.get("https://sider.ai/invited?c=0cc88d40d1ceb64ef5be3d4d976971b4")
        
        # Click vào Register Now & Claim Rewards
        logging.info("Đang tìm nút 'Register Now & Claim Rewards'")
        try:
            # Thử selector XPATH dựa trên text trước
            register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Register Now & Claim Rewards')]")))
            logging.info("Đã tìm thấy nút Register bằng text")
        except:
            logging.warning("Không tìm thấy nút Register bằng text, thử selector khác...")
            # Thử selector dựa trên class hoặc cấu trúc (cần kiểm tra lại trên trang thực tế)
            # Ví dụ: //button[contains(@class, 'register-button-class')]
            # Hoặc tìm button trong một div cụ thể
            # register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='some-container']//button[contains(., 'Register')]")))
            # Tạm thời dùng lại selector cũ nhưng với contains(., text) để linh hoạt hơn
            register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Register Now & Claim Rewards')]")))

        try:
            register_button.click()
            logging.info("Đã click nút Register (thông thường)")
        except Exception as e:
            logging.warning(f"Click thông thường thất bại: {e}. Thử click bằng JavaScript.")
            driver.execute_script("arguments[0].click();", register_button)
            logging.info("Đã click nút Register (JavaScript)")

        # Tìm và click vào nút Continue with Google
        # Đợi một chút sau khi click Register
        import time
        time.sleep(2) 

        # Tìm và click vào nút Continue with Google
        logging.info("Đang tìm vùng click 'Continue with Google'")
        # Sử dụng selector nhắm vào vùng click chính dựa trên cấu trúc HTML
        google_button_selector = "//div[contains(@class, 'col-[main]') and contains(@style, 'grid-row:1')]"
        google_button = wait.until(EC.element_to_be_clickable((By.XPATH, google_button_selector)))
        logging.info(f"Đã tìm thấy vùng click Google bằng selector: {google_button_selector}")

        try:
            # Thử click bằng ActionChains trước
            actions = ActionChains(driver)
            actions.move_to_element(google_button).click().perform()
            logging.info("Đã thử click vùng Google bằng ActionChains")
        except Exception as e_ac:
            logging.warning(f"Click vùng Google bằng ActionChains thất bại: {e_ac}. Thử click bằng JavaScript.")
            try:
                # Thử click bằng JavaScript
                driver.execute_script("arguments[0].click();", google_button)
                logging.info("Đã click vùng Google (JavaScript)")
            except Exception as e_js:
                logging.warning(f"Click vùng Google bằng JavaScript thất bại: {e_js}. Thử click thông thường.")
                try:
                    google_button.click()
                    logging.info("Đã click vùng Google (thông thường)")
                except Exception as e_click:
                     logging.error(f"Click vùng Google bằng mọi cách đều thất bại: {e_click}")

        # Chuyển sang cửa sổ đăng nhập Google mới
        wait.until(lambda driver: len(driver.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        logging.info("Đã chuyển sang cửa sổ đăng nhập Google")

        # Helper function để click (ưu tiên JS)
        def click_element(element, description):
            try:
                driver.execute_script("arguments[0].click();", element)
                logging.info(f"Đã click {description} (JavaScript)")
            except Exception as e:
                logging.warning(f"Click {description} bằng JavaScript thất bại: {e}. Thử click thông thường.")
                element.click()
                logging.info(f"Đã click {description} (thông thường)")

        # Điền email
        email_input = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
        email_input.send_keys(email)
        next_button_email = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Next')]")))
        click_element(next_button_email, "Next sau email")
        
        # Điền mật khẩu
        # Đợi một chút để trang load sau khi click Next
        logging.info("Đợi trang nhập mật khẩu load...")
        time.sleep(5) # Tăng thời gian chờ lên 5 giây
        logging.info("Đang tìm ô nhập mật khẩu...")
        # Thử dùng element_to_be_clickable và selector CSS linh hoạt hơn
        password_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']"))) 
        # Hoặc giữ lại selector cũ nếu CSS không hoạt động:
        # password_input = wait.until(EC.element_to_be_clickable((By.NAME, "password"))) 
        logging.info("Đã tìm thấy ô mật khẩu. Đang điền...")
        password_input.send_keys(password)
        logging.info("Đã điền mật khẩu. Đang tìm nút Next...")
        next_button_password = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Next')]")))
        click_element(next_button_password, "Next sau password")

        # Xử lý các bước bổ sung nếu có (dùng helper click)
        try:
            # Tìm nút "I understand" / "Tôi hiểu" (là thẻ input)
            understand_button_xpath = "//input[@type='submit' and (@value='Tôi hiểu' or @value='I understand')]"
            logging.info(f"Đang tìm nút 'Tôi hiểu'/'I understand' với XPath: {understand_button_xpath}")
            understand_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, understand_button_xpath))
                # Hoặc thử dùng ID nếu XPath trên không ổn định:
                # EC.element_to_be_clickable((By.ID, "confirm"))
            )
            click_element(understand_button, "'Tôi hiểu'/'I understand'")
            
            # Tìm nút "Continue" (vẫn có thể xuất hiện sau nút "Tôi hiểu")
            logging.info("Đang tìm nút 'Continue'")
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Continue')]"))
            )
            click_element(continue_button, "'Continue'")
        except:
            logging.warning("Không tìm thấy các bước bổ sung hoặc không cần xử lý")

        # Đợi cho đến khi chỉ còn 1 cửa sổ (nghĩa là cửa sổ đăng nhập đã đóng)
        wait.until(lambda driver: len(driver.window_handles) == 1)
        driver.switch_to.window(driver.window_handles[0])
        
        # Chuyển đến trang Chrome Web Store
        driver.get("https://chromewebstore.google.com/detail/sider-chat-with-all-ai-mo/difoiogjjojoaoomphldepapgpbgkhkb?pli=1")
        # Selector cho nút "Add to Chrome" có thể khác nhau, cần kiểm tra
        # Ví dụ: //button[contains(@aria-label, 'Add to Chrome')] hoặc dựa vào text trong button/div
        logging.info("Đang tìm nút 'Add to Chrome'")
        add_button_selector = "//button[contains(., 'Add to Chrome')] | //div[contains(., 'Add to Chrome') and @role='button']"
        add_button = wait.until(EC.element_to_be_clickable((By.XPATH, add_button_selector)))
        logging.info("Đã tìm thấy nút 'Add to Chrome'. Đang click...")
        click_element(add_button, "'Add to Chrome'")
        
        # --- Sử dụng PyAutoGUI để click nút "Add extension" trong hộp thoại ---
        logging.info("Đợi hộp thoại 'Add extension' của trình duyệt xuất hiện...")
        time.sleep(4) # Chờ hộp thoại xuất hiện (điều chỉnh nếu cần)

        # !!! QUAN TRỌNG: Bạn cần thay thế tọa độ X, Y bên dưới !!!
        # Chạy script 1 lần, khi hộp thoại hiện ra, dùng tool/script khác
        # để lấy tọa độ của nút "Add extension" rồi cập nhật vào đây.
        add_extension_button_x = 784
        add_extension_button_y = 270
        
        try:
            logging.info(f"Attempting to click 'Add extension' button at ({add_extension_button_x}, {add_extension_button_y}) using pyautogui")
            pyautogui.click(x=add_extension_button_x, y=add_extension_button_y)
            logging.info("Clicked using pyautogui.")
        except Exception as e:
            logging.error(f"Failed to click using pyautogui: {e}")
        # -------------------------------------------------------------------

        # Đợi một khoảng thời gian để tiện ích cài đặt (sau khi đã click xác nhận)
        install_wait_time = 10 # Giây
        logging.info(f"Đợi {install_wait_time} giây để tiện ích cài đặt...")
        time.sleep(install_wait_time)
        
        logging.info(f"Successfully processed account (đã cố gắng cài tiện ích): {email}")
    except Exception as e:
        logging.error(f"Error processing account {email}: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    with open("list_account.txt", "r") as f:
        accounts = [line.strip().split("|") for line in f]
    for email, password in accounts:
        process_account(email, password)

if __name__ == '__main__':
    main()
