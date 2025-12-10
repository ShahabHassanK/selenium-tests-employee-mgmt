"""
Pytest configuration file for Selenium tests
Sets up Firefox driver with headless mode for CI/CD
"""

import pytest
from selenium import webdriver
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
    Pytest fixture to set up and tear down Firefox WebDriver
    Configured for headless mode to run in Docker/Jenkins
    """
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service
    
    firefox_options = Options()
    
    # Essential options for headless Firefox
    if HEADLESS:
        firefox_options.add_argument("--headless")
    
    # Set window size
    firefox_options.add_argument(f"--width={WINDOW_SIZE.split(',')[0]}")
    firefox_options.add_argument(f"--height={WINDOW_SIZE.split(',')[1]}")
    
    # Create service with explicit path
    service = Service(executable_path="/usr/local/bin/geckodriver")
    
    # Initialize Firefox driver with service
    driver = webdriver.Firefox(service=service, options=firefox_options)
    
    # Set timeouts
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    
    yield driver
    
    # Teardown: quit driver after test
    driver.quit()


def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "Employee Management System - Selenium Test Report"
