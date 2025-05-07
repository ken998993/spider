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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrape import scrape_video_time
app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    # 呼叫抽取的函數
    result = scrape_video_time()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
