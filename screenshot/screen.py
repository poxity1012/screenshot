import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image
import firebase_admin
from firebase_admin import credentials, storage

# 初始化 Firebase
cred = credentials.Certificate(r"C:\Users\user\Desktop\screenshot_專題\self-driving-car-17746-firebase-adminsdk-n56sb-4de4a08704.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'self-driving-car-17746.appspot.com'
})


bucket = storage.bucket()

# 設置 Chrome 為無頭模式
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# 初始化 Chrome WebDriver
service = Service(executable_path='chromedriver.exe')  # 替換為 ChromeDriver 的路徑
driver = webdriver.Chrome(service=service, options=chrome_options)

# 打開指定的 URL
driver.get('http://172.20.10.4:8080/')

# 設置截圖範圍 (左上角和右下角的坐標)
left = 450
top = 60
right = 850
bottom = 590

# 指定保存截圖的文件夾路徑
save_folder = r'C:\Users\user\Desktop\screenshot_專題\Android_ai_car_screen_photo'

try:
    while True:
        # 獲取當前系統時間
        timestamp = time.strftime("%Y%m%d_%H%M%S")

        # 截圖並保存為 'screenshot_YYYYMMDD_HHMMSS.png'
        screenshot_name = os.path.join(save_folder, f'screenshot_{timestamp}.png')
        driver.save_screenshot(screenshot_name)
        
        # 打開截圖並裁剪
        image = Image.open(screenshot_name)
        cropped_image = image.crop((left, top, right, bottom))
        cropped_image.save(screenshot_name)
        
        print(f"Screenshot saved as {screenshot_name}")
        
        # 上傳至 Firebase Storage
        remote_file_path = os.path.relpath(screenshot_name, save_folder)
        blob = bucket.blob(remote_file_path)
        blob.upload_from_filename(screenshot_name)
        print(f'File {screenshot_name} uploaded to Firebase Storage.')
        
        # 等待 5 秒
        time.sleep(5)
except KeyboardInterrupt:
    # 捕捉到中斷信號 (Ctrl+C) 後退出循環並關閉瀏覽器
    print("Stopped by user")
finally:
    # 關閉瀏覽器
    driver.quit()
