import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Install Chrome if not already installed
CHROME_PATH = "/usr/bin/google-chrome"
if not os.path.exists(CHROME_PATH):
    subprocess.run("curl -o /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb", shell=True)
    subprocess.run("sudo dpkg -i /tmp/chrome.deb || sudo apt-get -f install -y", shell=True)

def get_driver():
    """Set up Selenium Chrome WebDriver with the correct Chrome binary."""
    chrome_options = Options()
    chrome_options.binary_location = CHROME_PATH  # ✅ Set Chrome binary location
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())  
    return webdriver.Chrome(service=service, options=chrome_options)

def extract_video_views(driver, video_url):
    """Extract views from a TikTok video."""
    driver.get(video_url)
    time.sleep(8)  # ✅ Wait for TikTok to load

    page_source = driver.page_source
    try:
        return int(page_source.split('"playCount":')[1].split(",")[0].strip())  
    except:
        return "Not found"

@app.route("/getTikTokViews", methods=["GET"])
def fetch_views():
    video_url = request.args.get("videoUrl")
    if not video_url:
        return jsonify({"error": "Missing videoUrl parameter"}), 400

    driver = get_driver()
    views = extract_video_views(driver, video_url)
    driver.quit()

    return jsonify({"views": views})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
