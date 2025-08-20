import pytest
import subprocess
import time
import requests
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def flask_app():
    # Start the Flask app
    process = subprocess.Popen(["python", "run.py"])
    
    # Wait for the app to start
    time.sleep(5)
    
    # Check if the app is running with retries
    max_retries = 5
    retry_delay = 2
    app_started = False
    
    for _ in range(max_retries):
        try:
            response = requests.get("http://localhost:5000")
            if response.status_code == 200:
                app_started = True
                break
        except requests.exceptions.ConnectionError:
            pass
        
        time.sleep(retry_delay)
    
    if not app_started:
        pytest.fail("Flask app did not start properly after multiple retries")
    
    yield process
    
    # Clean up
    process.terminate()
    process.wait()

@pytest.fixture
def browser():
    with sync_playwright() as p:
        
        browser = p.chromium.launch(
            headless=False,  
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-accelerated-2d-canvas",
                "--no-first-run",
                "--no-zygote",
                "--disable-gpu"
            ]
        )
        
       
        context = browser.new_context(
            viewport={"width": 1280, "height": 720}
        )
        

        context.set_default_timeout(10000)
        
        yield context
        
        context.close()
        browser.close()