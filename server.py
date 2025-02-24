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

# Install Chromium manually
if not os.path.exists("/usr/bin/chromium-browser"):
    subprocess.run(
        "apt-get update && apt-get install -y chromium-browser",
        shell=True,
        check=True
    )

def get_driver():
    """Set up Selenium with Chromium."""
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium-browser"  # ✅ Use Chromium
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
