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
    chrome_options = Options()
    
    # Essential options for headless Chrome
    if HEADLESS:
        chrome_options.add_argument("--headless")
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Initialize Chrome driver
    # Let Selenium handle ChromeDriver automatically
    driver = webdriver.Chrome(options=chrome_options)
    
    # Set timeouts
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    
    yield driver
    
    # Teardown: quit driver after test
    driver.quit()


def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "Employee Management System - Selenium Test Report"
