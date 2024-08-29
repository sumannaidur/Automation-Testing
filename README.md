# Selenium Automation Testing for Reliance Digital Website

## Description

This project is an automated testing suite developed using Selenium and PyTest for the Reliance Digital website. The test suite is designed to verify the functionality and user experience of the site, ensuring that key features work as expected. The tests simulate user interactions such as navigating the website, logging in, searching for products, managing the shopping cart, applying filters, and more.

## Prerequisites
- **Reliance Digital Account**: Before running the automation tests, ensure that you have created an account on the Reliance Digital website. This is required for testing login functionality, managing the wishlist, adding addresses, and other account-related features.

## Features
- **Automated Navigation**: Tests for loading the home page and verifying the title.
- **Login Automation**: Tests for the login functionality, including OTP verification.
- **Location-Based Testing**: Automated selection of delivery pin codes and verification of serviceability.
- **Search Functionality**: Tests for searching products and verifying search results.
- **Cart Management**: Tests for adding and removing products from the shopping cart.
- **Wishlist Management**: Tests for adding and removing products from the wishlist.
- **Filter Application**: Automated tests for applying and clearing filters like price, brand, and battery capacity.
- **Sorting Functionality**: Tests for sorting products by price (high to low).
- **Address Management**: Automated tests for adding and deleting addresses.
- **Account Management**: Tests for accessing and verifying account details like credits and wishlist.
- **Logout and Error Handling**: Tests for logging out and handling invalid login attempts.

## Technologies Used
- **Python**: Programming language used for scripting.
- **Selenium WebDriver**: For automating web browser interactions.
- **PyTest**: For organizing and running test cases.
- **Logging**: To capture and record the execution process and any errors encountered.
- **JSON**: For configuration management, storing URLs, user credentials, and other necessary data.

## Project Structure
- **project_root/**
- **│**
- **├── config/**
- **│   └── config.json          # Configuration file with URLs, credentials, and other settings**
- **│**
- **├── logs/**
- **│   └── test.log             # Log file generated during test execution**
- **│**
- **├── tests/**
- **│   └── test_script.py       # The main test script using Selenium and PyTest**
- **│**
- **├── requirements.txt         # Dependencies required for the project**
- **│**
- **└── README.md                # Documentation for the project**

## How to Use:
1. Clone the Repository:
    git clone https://github.com/yourusername/your-repository.git
2. Navigate to the Project Directory:
    cd project_root
3. Install Dependencies:
    pip install -r requirements.txt
4. Update the Configuration:
    Modify the config/config.json file with your details (mobile number).
5. Run the Tests:
    pytest tests/test_script.py
6. View Logs:
    Check the logs/test.log file for detailed logs of the test execution.