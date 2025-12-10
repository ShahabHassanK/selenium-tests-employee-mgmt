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
    Pytest fixture to set up and tear down Chrome WebDriver
    Uses Selenium Grid for reliable headless execution
    """
    import os
    from selenium.webdriver.chrome.options import Options
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(f'--window-size={WINDOW_SIZE}')
    
    # Check if we should use Selenium Grid (remote)
    selenium_remote_url = os.getenv('SELENIUM_REMOTE_URL')
    
    if selenium_remote_url:
        # Use Selenium Grid with retry logic
        import time
        max_retries = 30
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                driver = webdriver.Remote(
                    command_executor=selenium_remote_url,
                    options=chrome_options
                )
                break  # Success!
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Waiting for Selenium Grid... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                else:
                    raise  # Re-raise on final attempt
    else:
        # Fallback to local Chrome (for local testing)
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
