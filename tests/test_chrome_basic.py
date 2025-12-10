"""
Basic Chrome test to verify Chrome can start in Docker
"""
import pytest
from selenium import webdriver


def test_chrome_starts(driver):
    """Test that Chrome can start and get a simple page"""
    # Try to access a simple, always-available page
    driver.get("https://www.google.com")
    assert "Google" in driver.title
    print(f"✅ Chrome started successfully! Title: {driver.title}")
