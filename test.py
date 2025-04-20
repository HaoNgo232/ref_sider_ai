import pyautogui
import time
print("Di chuyển chuột đến nút 'Add extension' trong 5 giây...")
time.sleep(5)
x, y = pyautogui.position()
print(f"Tọa độ nút 'Add extension' là: X={x} Y={y}")
print("Bạn có thể đóng cửa sổ này.")