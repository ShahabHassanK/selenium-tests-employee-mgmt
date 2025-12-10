"""
Pytest configuration file for Selenium tests
Sets up Chrome driver with headless mode for CI/CD
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import (
    HEADLESS,
    WINDOW_SIZE,
    IMPLICIT_WAIT,
    PAGE_LOAD_TIMEOUT
)


@pytest.fixture(scope="function")
def driver():
    """
    Pytest fixture to set up and tear down Chrome WebDriver
    Configured for headless mode to run in Docker/Jenkins
    """
    from selenium.webdriver.chrome.service import Service
    
    chrome_options = Options()
    
    # Essential options for headless Chrome
    if HEADLESS:
        chrome_options.add_argument("--headless=new")
    
    # Critical options for running in Docker as non-root user
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")
    chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-ipc-flooding-protection")
    
    # Set binary location explicitly
    chrome_options.binary_location = "/usr/bin/google-chrome"
    
    # Create service with explicit path
    service = Service(executable_path="/usr/local/bin/chromedriver")
    
    # Initialize Chrome driver with service
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Set timeouts
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    
    yield driver
    
    # Teardown: quit driver after test
    driver.quit()


def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "Employee Management System - Selenium Test Report"
