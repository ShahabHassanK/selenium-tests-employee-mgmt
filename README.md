# Selenium Tests for Employee Management System

This directory contains automated Selenium tests for the Employee Management System MERN application.

## 📁 Project Structure

```
selenium-tests/
├── config/
│   ├── __init__.py
│   └── config.py          # Configuration settings
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # Pytest fixtures and setup
│   └── test_employee_management.py  # Main test suite (14 tests)
├── Dockerfile             # Docker image for running tests
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🧪 Test Cases (14 Total)

1. **test_01_homepage_loads_successfully** - Verify homepage loads
2. **test_02_create_employee_button_exists** - Check Create button exists
3. **test_03_navigate_to_create_page** - Test navigation to create page
4. **test_04_create_form_elements_present** - Verify all form elements
5. **test_05_create_new_employee** - Create new employee record
6. **test_06_view_employee_list** - View employee list with table headers
7. **test_07_edit_button_exists_for_employees** - Check Edit button exists
8. **test_08_edit_employee_record** - Edit existing employee
9. **test_09_delete_button_exists** - Check Delete button exists
10. **test_10_delete_employee_record** - Delete employee record
11. **test_11_radio_button_selection** - Test radio button behavior
12. **test_12_form_accepts_input** - Verify form inputs work
13. **test_13_create_multiple_employees** - Create multiple employees
14. **test_14_navigation_back_to_homepage** - Test navigation

## 🚀 Running Tests Locally

### Prerequisites
- Python 3.9+
- Chrome browser installed
- Employee Management System running on http://localhost:5173

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest -v tests/

# Run with HTML report
pytest -v --html=report.html --self-contained-html tests/

# Run specific test
pytest -v tests/test_employee_management.py::TestEmployeeManagementSystem::test_05_create_new_employee
```

## 🐳 Running Tests in Docker

### Build Docker Image
```bash
docker build -t selenium-tests .
```

### Run Tests in Container
```bash
# Make sure your app is accessible from Docker
# Use host.docker.internal instead of localhost in config.py for Docker

docker run --rm --network=host selenium-tests
```

## ⚙️ Configuration

Edit `config/config.py` to change:
- `BASE_URL` - Application URL (default: http://localhost:5173)
- `HEADLESS` - Run in headless mode (default: True)
- `IMPLICIT_WAIT` - Implicit wait timeout (default: 10s)
- `EXPLICIT_WAIT` - Explicit wait timeout (default: 15s)

## 📊 Test Reports

After running tests, check:
- Console output for test results
- `report.html` for detailed HTML report with screenshots

## 🔧 Troubleshooting

### Tests fail with "Connection refused"
- Ensure Employee Management System is running
- Check BASE_URL in config.py matches your app URL

### ChromeDriver version mismatch
- Update webdriver-manager: `pip install --upgrade webdriver-manager`

### Tests timeout
- Increase EXPLICIT_WAIT in config.py
- Check if application is responding slowly

## 📝 Notes for Jenkins

- Tests are configured for headless Chrome
- HTML reports are generated automatically
- Exit code 0 = all tests passed
- Exit code 1 = some tests failed
