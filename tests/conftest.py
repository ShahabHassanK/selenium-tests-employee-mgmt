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
    import os
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service
    
    # Set environment variable for headless Firefox
    os.environ['MOZ_HEADLESS'] = '1'
    
    firefox_options = Options()
    
    # Essential options for headless Firefox
    firefox_options.add_argument('-headless')
    
    # Additional preferences for Docker environment
    firefox_options.set_preference('browser.privatebrowsing.autostart', False)
    
    # Set window size using preferences
    width, height = WINDOW_SIZE.split(',')
    firefox_options.set_preference('browser.window.width', int(width))
    firefox_options.set_preference('browser.window.height', int(height))
    
    # Create service with explicit path and log
    service = Service(
        executable_path="/usr/local/bin/geckodriver",
        log_output="/tmp/geckodriver.log"
    )
    
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
