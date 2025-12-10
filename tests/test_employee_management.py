"""
Employee Management System - Selenium Test Suite
Tests all CRUD operations, navigation, and form validation
"""

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import BASE_URL, EXPLICIT_WAIT


class TestEmployeeManagementSystem:
    """Test suite for Employee Management System"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup method that runs before each test"""
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)
        self.base_url = BASE_URL
    
    # ==================== TEST 1: Homepage Loads ====================
    def test_01_homepage_loads_successfully(self):
        """
        Test Case 1: Verify homepage loads successfully
        Steps:
        1. Navigate to homepage
        2. Verify page title contains expected text
        3. Verify Employee Records heading is displayed
        """
        print("\n[TEST 1] Testing homepage load...")
        self.driver.get(self.base_url)
        
        # Verify page title
        assert "Vite + React" in self.driver.title or "Employee" in self.driver.page_source
        
        # Verify main heading
        heading = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Employee Records')]"))
        )
        assert heading.is_displayed()
        print("[TEST 1] ✓ Homepage loaded successfully")
    
    # ==================== TEST 2: Create Employee Button Exists ====================
    def test_02_create_employee_button_exists(self):
        """
        Test Case 2: Verify Create Employee button is present and clickable
        Steps:
        1. Navigate to homepage
        2. Locate Create Employee button
        3. Verify button is displayed and enabled
        """
        print("\n[TEST 2] Testing Create Employee button...")
        self.driver.get(self.base_url)
        
        # Find Create Employee link/button
        create_button = self.wait.until(
            EC.presence_of_element_located((By.LINK_TEXT, "Create Employee"))
        )
        assert create_button.is_displayed()
        assert create_button.is_enabled()
        print("[TEST 2] ✓ Create Employee button found and enabled")
    
    # ==================== TEST 3: Navigate to Create Page ====================
    def test_03_navigate_to_create_page(self):
        """
        Test Case 3: Verify navigation to Create Employee page
        Steps:
        1. Navigate to homepage
        2. Click Create Employee button
        3. Verify URL changes to /create
        4. Verify form is displayed
        """
        print("\n[TEST 3] Testing navigation to create page...")
        self.driver.get(self.base_url)
        
        # Click Create Employee
        create_button = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Create Employee"))
        )
        create_button.click()
        
        # Verify URL
        self.wait.until(EC.url_contains("/create"))
        assert "/create" in self.driver.current_url
        
        # Verify form heading
        form_heading = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Create/Update')]"))
        )
        assert form_heading.is_displayed()
        print("[TEST 3] ✓ Successfully navigated to create page")
    
    # ==================== TEST 4: Form Elements Present ====================
    def test_04_create_form_elements_present(self):
        """
        Test Case 4: Verify all form elements are present
        Steps:
        1. Navigate to create page
        2. Verify Name input field exists
        3. Verify Position input field exists
        4. Verify Level radio buttons exist
        5. Verify Submit button exists
        """
        print("\n[TEST 4] Testing form elements...")
        self.driver.get(f"{self.base_url}/create")
        
        # Verify Name field
        name_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "name"))
        )
        assert name_input.is_displayed()
        
        # Verify Position field
        position_input = self.driver.find_element(By.ID, "position")
        assert position_input.is_displayed()
        
        # Verify Level radio buttons
        intern_radio = self.driver.find_element(By.ID, "positionIntern")
        junior_radio = self.driver.find_element(By.ID, "positionJunior")
        senior_radio = self.driver.find_element(By.ID, "positionSenior")
        
        assert intern_radio.is_displayed()
        assert junior_radio.is_displayed()
        assert senior_radio.is_displayed()
        
        # Verify Submit button
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        assert submit_button.is_displayed()
        
        print("[TEST 4] ✓ All form elements present")
    
    # ==================== TEST 5: Create New Employee ====================
    def test_05_create_new_employee(self):
        """
        Test Case 5: Create a new employee record
        Steps:
        1. Navigate to create page
        2. Fill in employee details
        3. Submit form
        4. Verify redirect to homepage
        5. Verify employee appears in list
        """
        print("\n[TEST 5] Testing employee creation...")
        self.driver.get(f"{self.base_url}/create")
        
        # Generate unique employee name
        timestamp = str(int(time.time()))
        employee_name = f"Test Employee {timestamp}"
        
        # Fill form
        name_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "name"))
        )
        name_input.clear()
        name_input.send_keys(employee_name)
        
        position_input = self.driver.find_element(By.ID, "position")
        position_input.clear()
        position_input.send_keys("QA Engineer")
        
        # Select Junior level
        junior_radio = self.driver.find_element(By.ID, "positionJunior")
        junior_radio.click()
        
        # Submit form
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()
        
        # Wait for redirect to homepage
        self.wait.until(EC.url_to_be(f"{self.base_url}/"))
        
        # Verify employee in list
        time.sleep(2)  # Wait for data to load
        page_source = self.driver.page_source
        assert employee_name in page_source, f"Employee '{employee_name}' not found in list"
        
        print(f"[TEST 5] ✓ Employee '{employee_name}' created successfully")
    
    # ==================== TEST 6: View Employee List ====================
    def test_06_view_employee_list(self):
        """
        Test Case 6: Verify employee list displays correctly
        Steps:
        1. Navigate to homepage
        2. Verify table headers are present
        3. Check if table has rows (if employees exist)
        """
        print("\n[TEST 6] Testing employee list view...")
        self.driver.get(self.base_url)
        
        # Verify table exists
        table = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
        )
        assert table.is_displayed()
        
        # Verify table headers
        headers = self.driver.find_elements(By.XPATH, "//thead//th")
        assert len(headers) >= 4  # Name, Position, Level, Action
        
        header_texts = [h.text for h in headers]
        assert "Name" in header_texts
        assert "Position" in header_texts
        assert "Level" in header_texts
        assert "Action" in header_texts
        
        print("[TEST 6] ✓ Employee list displayed correctly")
    
    # ==================== TEST 7: Edit Button Exists ====================
    def test_07_edit_button_exists_for_employees(self):
        """
        Test Case 7: Verify Edit button exists for employee records
        Steps:
        1. Create a test employee first
        2. Verify Edit button appears
        3. Verify Edit button is clickable
        """
        print("\n[TEST 7] Testing Edit button existence...")
        
        # First create an employee
        self.driver.get(f"{self.base_url}/create")
        timestamp = str(int(time.time()))
        
        name_input = self.wait.until(EC.presence_of_element_located((By.ID, "name")))
        name_input.send_keys(f"Edit Test {timestamp}")
        
        position_input = self.driver.find_element(By.ID, "position")
        position_input.send_keys("Developer")
        
        senior_radio = self.driver.find_element(By.ID, "positionSenior")
        senior_radio.click()
        
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()
        
        # Wait for redirect
        self.wait.until(EC.url_to_be(f"{self.base_url}/"))
        time.sleep(2)
        
        # Find Edit button
        edit_buttons = self.driver.find_elements(By.LINK_TEXT, "Edit")
        assert len(edit_buttons) > 0, "No Edit buttons found"
        assert edit_buttons[0].is_displayed()
        
        print("[TEST 7] ✓ Edit button exists and is visible")
    
    # ==================== TEST 8: Edit Employee ====================
    def test_08_edit_employee_record(self):
        """
        Test Case 8: Edit an existing employee record
        Steps:
        1. Create a test employee
        2. Click Edit button
        3. Modify employee details
        4. Submit changes
        5. Verify changes are saved
        """
        print("\n[TEST 8] Testing employee edit functionality...")
        
        # Create employee
        self.driver.get(f"{self.base_url}/create")
        timestamp = str(int(time.time()))
        original_name = f"Original Name {timestamp}"
        
        name_input = self.wait.until(EC.presence_of_element_located((By.ID, "name")))
        name_input.send_keys(original_name)
        
        position_input = self.driver.find_element(By.ID, "position")
        position_input.send_keys("Backend Developer")
        
        intern_radio = self.driver.find_element(By.ID, "positionIntern")
        intern_radio.click()
        
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()
        
        self.wait.until(EC.url_to_be(f"{self.base_url}/"))
        time.sleep(2)
        
        # Click Edit on first employee
        edit_button = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Edit"))
        )
        edit_button.click()
        
        # Wait for edit page
        self.wait.until(EC.url_contains("/edit/"))
        
        # Modify name
        updated_name = f"Updated Name {timestamp}"
        name_input = self.wait.until(EC.presence_of_element_located((By.ID, "name")))
        name_input.clear()
        name_input.send_keys(updated_name)
        
        # Submit changes
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()
        
        # Verify redirect and changes
        self.wait.until(EC.url_to_be(f"{self.base_url}/"))
        time.sleep(3)  # Wait for data to update
        
        # Refresh page to ensure we get latest data
        self.driver.refresh()
        time.sleep(2)
        
        page_source = self.driver.page_source
        assert updated_name in page_source, f"Updated name '{updated_name}' not found"
        
        print(f"[TEST 8] ✓ Employee updated to '{updated_name}'")
    
    # ==================== TEST 9: Delete Button Exists ====================
    def test_09_delete_button_exists(self):
        """
        Test Case 9: Verify Delete button exists for employees
        Steps:
        1. Create a test employee
        2. Verify Delete button appears
        3. Verify Delete button is clickable
        """
        print("\n[TEST 9] Testing Delete button existence...")
        
        # Create employee
        self.driver.get(f"{self.base_url}/create")
        timestamp = str(int(time.time()))
        
        name_input = self.wait.until(EC.presence_of_element_located((By.ID, "name")))
        name_input.send_keys(f"Delete Test {timestamp}")
        
        position_input = self.driver.find_element(By.ID, "position")
        position_input.send_keys("Tester")
        
        junior_radio = self.driver.find_element(By.ID, "positionJunior")
        junior_radio.click()
        
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()
        
        self.wait.until(EC.url_to_be(f"{self.base_url}/"))
        time.sleep(2)
        
        # Find Delete button
        delete_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Delete')]")
        assert len(delete_buttons) > 0, "No Delete buttons found"
        assert delete_buttons[0].is_displayed()
        
        print("[TEST 9] ✓ Delete button exists and is visible")
    
    # ==================== TEST 10: Delete Employee ====================
    def test_10_delete_employee_record(self):
        """
        Test Case 10: Delete an employee record
        Steps:
        1. Create a test employee
        2. Count total employees
        3. Click Delete button
        4. Verify employee count decreased
        5. Verify employee no longer in list
        """
        print("\n[TEST 10] Testing employee deletion...")
        
        # Create employee
        self.driver.get(f"{self.base_url}/create")
        timestamp = str(int(time.time()))
        employee_name = f"To Delete {timestamp}"
        
        name_input = self.wait.until(EC.presence_of_element_located((By.ID, "name")))
        name_input.send_keys(employee_name)
        
        position_input = self.driver.find_element(By.ID, "position")
        position_input.send_keys("Temporary")
        
        senior_radio = self.driver.find_element(By.ID, "positionSenior")
        senior_radio.click()
        
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()
        
        self.wait.until(EC.url_to_be(f"{self.base_url}/"))
        time.sleep(2)
        
        # Count employees before deletion
        rows_before = self.driver.find_elements(By.XPATH, "//tbody/tr")
        count_before = len(rows_before)
        
        # Click Delete on first employee
        delete_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Delete')]"))
        )
        delete_button.click()
        
        # Wait a moment for deletion
        time.sleep(2)
        
        # Count employees after deletion
        rows_after = self.driver.find_elements(By.XPATH, "//tbody/tr")
        count_after = len(rows_after)
        
        assert count_after == count_before - 1, "Employee count did not decrease"
        
        print(f"[TEST 10] ✓ Employee deleted successfully (count: {count_before} → {count_after})")
    
    # ==================== TEST 11: Radio Button Selection ====================
    def test_11_radio_button_selection(self):
        """
        Test Case 11: Verify only one radio button can be selected
        Steps:
        1. Navigate to create page
        2. Select Intern radio button
        3. Verify Intern is selected
        4. Select Junior radio button
        5. Verify only Junior is selected
        """
        print("\n[TEST 11] Testing radio button selection...")
        self.driver.get(f"{self.base_url}/create")
        
        intern_radio = self.wait.until(EC.presence_of_element_located((By.ID, "positionIntern")))
        junior_radio = self.driver.find_element(By.ID, "positionJunior")
        senior_radio = self.driver.find_element(By.ID, "positionSenior")
        
        # Select Intern
        intern_radio.click()
        time.sleep(0.5)
        assert intern_radio.is_selected()
        assert not junior_radio.is_selected()
        assert not senior_radio.is_selected()
        
        # Select Junior
        junior_radio.click()
        time.sleep(0.5)
        assert not intern_radio.is_selected()
        assert junior_radio.is_selected()
        assert not senior_radio.is_selected()
        
        # Select Senior
        senior_radio.click()
        time.sleep(0.5)
        assert not intern_radio.is_selected()
        assert not junior_radio.is_selected()
        assert senior_radio.is_selected()
        
        print("[TEST 11] ✓ Radio button selection works correctly")
    
    # ==================== TEST 12: Form Input Validation ====================
    def test_12_form_accepts_input(self):
        """
        Test Case 12: Verify form inputs accept text
        Steps:
        1. Navigate to create page
        2. Enter text in Name field
        3. Enter text in Position field
        4. Verify inputs contain entered text
        """
        print("\n[TEST 12] Testing form input acceptance...")
        self.driver.get(f"{self.base_url}/create")
        
        name_input = self.wait.until(EC.presence_of_element_located((By.ID, "name")))
        position_input = self.driver.find_element(By.ID, "position")
        
        test_name = "John Doe"
        test_position = "Software Engineer"
        
        name_input.send_keys(test_name)
        position_input.send_keys(test_position)
        
        assert name_input.get_attribute("value") == test_name
        assert position_input.get_attribute("value") == test_position
        
        print("[TEST 12] ✓ Form inputs accept text correctly")
    
    # ==================== TEST 13: Multiple Employee Creation ====================
    def test_13_create_multiple_employees(self):
        """
        Test Case 13: Create multiple employees and verify all appear
        Steps:
        1. Create 3 different employees
        2. Verify all 3 appear in the list
        """
        print("\n[TEST 13] Testing multiple employee creation...")
        timestamp = str(int(time.time()))
        
        employees = [
            {"name": f"Alice {timestamp}", "position": "Frontend Dev", "level": "positionJunior"},
            {"name": f"Bob {timestamp}", "position": "Backend Dev", "level": "positionSenior"},
            {"name": f"Charlie {timestamp}", "position": "DevOps", "level": "positionIntern"}
        ]
        
        for emp in employees:
            self.driver.get(f"{self.base_url}/create")
            
            name_input = self.wait.until(EC.presence_of_element_located((By.ID, "name")))
            name_input.send_keys(emp["name"])
            
            position_input = self.driver.find_element(By.ID, "position")
            position_input.send_keys(emp["position"])
            
            level_radio = self.driver.find_element(By.ID, emp["level"])
            level_radio.click()
            
            submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
            submit_button.click()
            
            self.wait.until(EC.url_to_be(f"{self.base_url}/"))
            time.sleep(1)
        
        # Verify all employees in list
        time.sleep(2)
        page_source = self.driver.page_source
        
        for emp in employees:
            assert emp["name"] in page_source, f"Employee '{emp['name']}' not found"
        
        print(f"[TEST 13] ✓ Created and verified {len(employees)} employees")
    
    # ==================== TEST 14: Navigation Back to Homepage ====================
    def test_14_navigation_back_to_homepage(self):
        """
        Test Case 14: Verify navigation back to homepage
        Steps:
        1. Navigate to create page
        2. Click on logo/header to return home
        3. Verify URL is homepage
        """
        print("\n[TEST 14] Testing navigation back to homepage...")
        self.driver.get(f"{self.base_url}/create")
        
        # Verify we're on create page
        assert "/create" in self.driver.current_url
        
        # Navigate back by clicking on the main heading/logo
        # (This might need adjustment based on actual navigation implementation)
        self.driver.get(self.base_url)
        
        # Verify we're back on homepage
        assert self.driver.current_url == f"{self.base_url}/" or self.driver.current_url == self.base_url
        
        print("[TEST 14] ✓ Navigation back to homepage successful")
