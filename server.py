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

# Define Chrome paths
CHROME_PATH = "/opt/render/project/.google-chrome/google-chrome"
CHROMEDRIVER_PATH = "/opt/render/project/.chromedriver/bin/chromedriver"

# Install Chrome and Chromedriver manually (if not installed)
if not os.path.exists(CHROME_PATH):
    subprocess.run(
        "mkdir -p /opt/render/project/.google-chrome && curl -o /opt/render/project/.google-chrome/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb",
        shell=True,
    )
    subprocess.run(
        "dpkg -x /opt/render/project/.google-chrome/chrome.deb /opt/render/project/.google-chrome/",
        shell=True,
    )
    subprocess.run(
        "mv /opt/render/project/.google-chrome/opt/google/chrome/google-chrome /opt/render/project/.google-chrome/",
        shell=True,
    )

if not os.path.exists(CHROMEDRIVER_PATH):
    subprocess.run(
        "mkdir -p /opt/render/project/.chromedriver/bin && curl -Lo /opt/render/project/.chromedriver/bin/chromedriver https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && unzip /opt/render/project/.chromedriver/bin/chromedriver -d /opt/render/project/.chromedriver/bin && chmod +x /opt/render/project/.chromedriver/bin/chromedriver",
        shell=True,
    )

def get_driver():
    """Set up Selenium Chrome WebDriver with the correct binary paths."""
    chrome_options = Options()
    chrome_options.binary_location = CHROME_PATH  # ✅ Set Chrome binary location
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(CHROMEDRIVER_PATH)  # ✅ Use manually installed Chromedriver
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
