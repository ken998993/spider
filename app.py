from flask import Flask, jsonify, render_template
from scrape import scrape_video_time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # 回傳首頁 HTML

@app.route('/scrape', methods=['GET'])
def scrape():
    result = scrape_video_time()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
