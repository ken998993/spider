from datetime import timedelta
import time
import random
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pickle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_video_time():
    """
    Scrapes the video time from a YouTube video using Selenium and undetected-chromedriver.
    Returns a dictionary containing the status, message, and video time (or error message).
    """
    try:
        # 使用 undetected-chromedriver 啟動 Chrome
        options = uc.ChromeOptions()
        # 禁用 GPU，加速渲染
        options.add_argument('--disable-gpu')

        # 使用 ChromeDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # 先訪問 Google 網站或你需要的網站
        driver.get("https://www.google.com")
        time.sleep(2)  # 等待頁面加載

        # 加載 cookies 並將它們添加到當前瀏覽器 session
        try:
            cookies = pickle.load(open("google_cookies.pkl", "rb"))
            for cookie in cookies:
                # 確保網域正確
                if 'domain' in cookie and cookie['domain'] == ".google.com":
                    driver.add_cookie(cookie)
        except FileNotFoundError:
            return {"status": "error", "message": "Cookies file not found."}
        except Exception as e:
            return {"status": "error", "message": "Failed to load cookies", "error_message": str(e)}

        driver.get("https://www.google.com")
        time.sleep(2)

        video_url = "https://www.youtube.com/watch?v=E3p-bgAQrXc"
        driver.get(video_url)
        
        # 等待影片頁面完全加載並確保元素可見
        try:
            video_time_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="movie_player"]/div[30]/div[2]/div[1]/div[1]/span[1]/span[4]'))
            )
            video_time = video_time_element.text.strip()
            print('video_time', video_time)
        except Exception as e:
            return {"status": "error", "message": "Failed to find video time", "error_message": str(e)}

        # 處理影片時間
        try:
            h, m, s = map(int, video_time.split(':'))
            duration = timedelta(hours=h, minutes=m, seconds=s)
        except ValueError as e:
            return {"status": "error", "message": "Failed to parse video time", "error_message": str(e)}

        # 等待影片播放時間
        time.sleep(duration.total_seconds() + random.uniform(5, 16))

        # 關閉瀏覽器
        driver.quit()

        return {"status": "success", "video_time": video_time, "message": "Scraping done!"}

    except Exception as e:
        # 捕獲整體錯誤並返回具體錯誤訊息
        return {"status": "error", "message": "Scraping failed", "error_message": str(e)}

# 呼叫函數進行測試
if __name__ == "__main__":
    result = scrape_video_time()
    print(result)
