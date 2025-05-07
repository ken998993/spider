from flask import Flask, jsonify
from datetime import timedelta
import time
import random
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pickle
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    try:
        # 使用 undetected-chromedriver 啟動 Chrome
        options = uc.ChromeOptions()
        # 禁用 GPU，加速渲染
        options.add_argument('--disable-gpu')

        # 使用 ChromeDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        # 先訪問 Google 網站或你需要的網站
        driver.get("https://www.google.com")

        # 等待頁面載入
        time.sleep(2)

        # 加載 cookies 並將它們添加到當前瀏覽器 session
        cookies = pickle.load(open("google_cookies.pkl", "rb"))
        for cookie in cookies:
            # 確保網域正確
            if 'domain' in cookie and cookie['domain'] == ".google.com":
                driver.add_cookie(cookie)

        driver.get("https://www.google.com")
        time.sleep(2)

        video_url = "https://www.youtube.com/watch?v=E3p-bgAQrXc"
        # 等待頁面加載
        driver.get(video_url)
        time.sleep(5)

        # 取得影片播放時間
        video_time = driver.find_element(By.XPATH, '//*[@id="movie_player"]/div[30]/div[2]/div[1]/div[1]/span[1]/span[4]').text.strip()
        print('video_time', video_time)

        h, m, s = map(int, video_time.split(':'))
        duration = timedelta(hours=h, minutes=m, seconds=s)
        time.sleep(duration.total_seconds() + random.uniform(5, 16))

        # 關閉瀏覽器
        driver.quit()

        return jsonify({"status": "success", "video_time": video_time, "message": "Scraping done!"})

    except Exception as e:
        # 如果發生錯誤，返回錯誤訊息
        return jsonify({"status": "error", "message": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
