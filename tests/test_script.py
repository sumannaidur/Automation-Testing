import logging
import time
import pytest
import os
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json

# Load configuration from environment variable or default to local path
config_path = os.getenv('CONFIG_PATH', 'config/config.json')
try:
    with open(config_path, 'r') as file:
        config = json.load(file)
except FileNotFoundError:
    raise SystemExit(f"Configuration file not found at {config_path}")
except json.JSONDecodeError:
    raise SystemExit(f"Error decoding JSON from the configuration file at {config_path}")

URL = config.get("URL")
EXPECTED_TITLE = config.get("EXPECTED_TITLE")
DELAY = config.get("DELAY", 2)
MOBILE_NUMBER = config.get("MOBILE_NUMBER")
OTP = config.get("OTP")  # Note: OTP should be manually entered by user in a real scenario.
PIN_CODE = config.get("PIN_CODE")

# Clear the log file before running the tests
with open(os.path.join(os.getcwd(), "logs", "test.log"), "w") as file:
    file.write("")

# Setup logging to both console and file
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),  # Log to console
                        logging.FileHandler(os.path.join(os.getcwd(), "logs", "test.log"))  # Log to file
                    ])

# Setup logging to both console and file
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),  # Log to console
                        logging.FileHandler(os.path.join(os.getcwd(), "logs", "test.log"))  # Log to file
                    ])

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def highlight_element(driver, element):
    """Highlights (blinks) a Selenium Webdriver element."""
    driver.execute_script("arguments[0].style.border='5px solid #1BDAE6'", element)
    time.sleep(0.3)
    driver.execute_script("arguments[0].style.border=''", element)

def wait_for_element(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        logging.error(f"Element not found: {value}")
        print(f"ERROR: Element not found: {value}")
        pytest.fail(f"Element not found: {value}")

def wait_for_clickable(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        return element
    except TimeoutException:
        logging.error(f"Element not clickable: {value}")
        print(f"ERROR: Element not clickable: {value}")
        pytest.fail(f"Element not clickable: {value}")

def handle_popup(driver):
    try:
        popup = driver.find_element(By.ID, "wzrk-cancel")
        if popup.is_displayed():
            highlight_element(driver, popup)
            popup.click()
            logging.info("Popup closed successfully")
            print("ACTION: Popup closed successfully")
            time.sleep(1)  # Allow some time for the popup to close
    except NoSuchElementException:
        logging.info("No popup to handle")
        print("INFO: No popup to handle")

@pytest.mark.usefixtures("driver")
def testcase(driver):
    logging.info("Starting Test Case 1: Navigating to home page")
    print("Starting Test Case 1: Navigating to home page")
    driver.get(URL)
    logging.info(f"ACTION: Opened home page: {URL}")
    print(f"ACTION: Opened home page: {URL}")
    
    try:
        handle_popup(driver)  # Ensure popup is handled at the beginning
        wait_for_element(driver, By.TAG_NAME, "body")
        logging.info("SUCCESS: Homepage loaded successfully")
        print("SUCCESS: Homepage loaded successfully")
    except Exception as e:
        logging.error(f"ERROR: Homepage did not load successfully: {e}")
        print(f"ERROR: Homepage did not load successfully: {e}")
        pytest.fail("Test Case 1: Navigating to home page - Failed")
    
    # Title verification
    logging.info("Starting Test Case 2: Tittle verification")
    print("Starting Test Case 2: Tittle verification")
    try:
        handle_popup(driver)  # Ensure popup is handled at the beginning
        assert EXPECTED_TITLE in driver.title
        logging.info(f"SUCCESS: Title verified: {driver.title}")
        print(f"SUCCESS: Title verified: {driver.title}")
    except AssertionError:
        logging.error(f"ERROR: Title verification failed. Expected: {EXPECTED_TITLE}, Found: {driver.title}")
        print(f"ERROR: Title verification failed. Expected: {EXPECTED_TITLE}, Found: {driver.title}")
        pytest.fail(f"Test Case 2: Title verification [{EXPECTED_TITLE}] - Failed")

    handle_popup(driver)
    time.sleep(DELAY)   
    # Test login
    logging.info("Starting Test Case 3: Login process")
    print("Starting Test Case 3: Login process")
    try:
        handle_popup(driver)  # Ensure popup is handled at the beginning

        login_button = wait_for_clickable(driver, By.XPATH, "//li[@class='header__maininfo__list__item dropdown__item' and @tabindex='0' and @aria-label='Login']//span[@class='pb__24 pointer' and @id='RIL_HeaderLoginAndMyAccount' and @role='button' and @tabindex='0']")
        highlight_element(driver, login_button)
        login_button.click()
        logging.info("ACTION: Clicked login button")
        print("ACTION: Clicked login button")
        time.sleep(DELAY)
        handle_popup(driver)
        mobile_input = wait_for_element(driver, By.ID, "lMobileNumber")
        highlight_element(driver, mobile_input)
        mobile_input.send_keys(MOBILE_NUMBER)
        logging.info(f"ACTION: Entered mobile number: {MOBILE_NUMBER}")
        print(f"ACTION: Entered mobile number: {MOBILE_NUMBER}")
        handle_popup(driver)
        proceed_button = wait_for_clickable(driver, By.XPATH, "//button[@aria-label='Proceed']")
        highlight_element(driver, proceed_button)
        proceed_button.click()
        logging.info("ACTION: Clicked proceed button")
        print("ACTION: Clicked proceed button")
        time.sleep(DELAY)
        handle_popup(driver)
        # Wait for manual OTP entry
        otp_input = wait_for_element(driver, By.ID, "l-m-otp")
        highlight_element(driver, otp_input)
        handle_popup(driver)
        otp_entered = False
        while not otp_entered:
            time.sleep(DELAY)
            try:
                otp_value = otp_input.get_attribute('value')
                if otp_value and len(otp_value) == 6:
                    otp_entered = True
                    logging.info("ACTION: OTP entered successfully.")
                    print("ACTION: OTP entered successfully.")
            except Exception as e:
                logging.error("Error while checking OTP entry: %s", e)
                print(f"ERROR: Error while checking OTP entry: {e}")

        login_button_final = wait_for_clickable(driver, By.XPATH, "//button[@aria-label='Login']")
        highlight_element(driver, login_button_final)
        login_button_final.click()
        logging.info("ACTION: Clicked login button")
        print("ACTION: Clicked login button")
        time.sleep(DELAY)

        # Verification of successful login
        try:
            user_profile = wait_for_element(driver, By.XPATH, "//li[@aria-label='Account Details']//span[contains(text(), 'Hi suman')]")
            highlight_element(driver, user_profile)
            logging.info("SUCCESS: Login successful")
            print("SUCCESS: Login successful")
        except TimeoutException:
            logging.error("ERROR: Login not successful")
            print("ERROR: Login not successful")
            pytest.fail("Test Case 3: Login process - Failed")
    except Exception as e:
        logging.error(f"ERROR: Failed during login process: {e}")
        print(f"ERROR: Failed during login process: {e}")
        pytest.fail("Test Case 3: Login process - Failed")

    # Test pin code selection
    logging.info("Starting Test Case 4: Select your pin code")
    print("Starting Test Case 4: Select your pin code")
    try:
        handle_popup(driver)  # Ensure popup is handled at the beginning

        pin_code_button = wait_for_clickable(driver, By.XPATH, "//div[@aria-label='Select your Pin Code']")
        highlight_element(driver, pin_code_button)
        pin_code_button.click()
        logging.info("ACTION: Clicked 'Select your Pin Code' button")
        print("ACTION: Clicked 'Select your Pin Code' button")
        time.sleep(DELAY)

        pin_code_input = wait_for_element(driver, By.ID, "pincode")
        highlight_element(driver, pin_code_input)
        pin_code_input.send_keys(PIN_CODE)
        logging.info(f"ACTION: Entered pin code: {PIN_CODE}")
        print(f"ACTION: Entered pin code: {PIN_CODE}")

        apply_button = wait_for_clickable(driver, By.XPATH, "//button[@aria-label='APPLY']")
        highlight_element(driver, apply_button)
        apply_button.click()
        logging.info("ACTION: Clicked 'APPLY' button")
        print("ACTION: Clicked 'APPLY' button")
        time.sleep(DELAY)

        # Verification of successful pin code update
        try:
            delivery_location = wait_for_element(driver, By.XPATH, f"//span[@aria-label='Deliver to Bangalore 560078']")
            highlight_element(driver, delivery_location)
            logging.info("SUCCESS: Pin code updated successfully")
            print("SUCCESS: Pin code updated successfully")
        except TimeoutException:
            logging.error("ERROR: Pin code not updated successfully")
            print("ERROR: Pin code not updated successfully")
            pytest.fail("Test Case 4: Select your pin code - Failed")
    except Exception as e:
        logging.error(f"ERROR: Failed during pin code selection process: {e}")
        print(f"ERROR: Failed during pin code selection process: {e}")
        pytest.fail("Test Case 4: Select your pin code - Failed")

    # Test find store functionality
    logging.info("Starting Test Case 4: Find a store near me")
    print("Starting Test Case 4: Find a store near me")
    try:
        handle_popup(driver)  # Ensure popup is handled at the beginning

        # Open "Find a store" page in a new tab
        find_store_link = wait_for_clickable(driver, By.XPATH, "//a[@aria-label='Opening Find a store Page in New Tab']")
        driver.execute_script("window.open(arguments[0].href, '_blank');", find_store_link)
        driver.switch_to.window(driver.window_handles[1])
        logging.info("ACTION: Opened 'Find a store' page in a new tab")
        print("ACTION: Opened 'Find a store' page in a new tab")
        time.sleep(DELAY)

        # Enter pin code and find store
        pin_code_input = wait_for_element(driver, By.XPATH, "//input[@aria-label='Enter Pincode / Town / Street']")
        highlight_element(driver, pin_code_input)
        pin_code_input.send_keys(PIN_CODE)
        logging.info(f"ACTION: Entered pin code: {PIN_CODE}")
        print(f"ACTION: Entered pin code: {PIN_CODE}")

        search_result = wait_for_clickable(driver, By.XPATH, "//li[contains(text(), 'Bengaluru, Karnataka 560078')]")
        highlight_element(driver, search_result)
        search_result.click()
        logging.info("ACTION: Clicked on the search result")
        print("ACTION: Clicked on the search result")
        time.sleep(DELAY)

        # Display store details
        store_details = wait_for_element(driver, By.XPATH, "//div[contains(text(), 'Digital Xpress Mini')]")
        store_info = store_details.text
        logging.info(f"SUCCESS: Store details found - {store_info}")
        print(f"SUCCESS: Store details found - {store_info}")

        # Close the new tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        logging.info("ACTION: Closed the new tab")
        print("ACTION: Closed the new tab")
        print("Test Case 5: Find a store near me - Passed")
    except Exception as e:
        logging.error(f"ERROR: Failed during 'Find a store' process: {e}")
        print(f"ERROR: Failed during 'Find a store' process: {e}")
        pytest.fail("Test Case 5: Find a store near me - Failed")

    # Test search functionality
    logging.info("Starting Test Case 6: Search for a product")
    print("Starting Test Case 6: Search for a product")
    try:
        handle_popup(driver)  # Ensure popup is handled at the beginning

        # Locate the search bar
        search_bar = wait_for_element(driver, By.ID, "suggestionBoxEle")
        highlight_element(driver, search_bar)
        search_bar.send_keys("smartphones")
        logging.info("ACTION: Entered 'smartphones' into the search bar")
        print("ACTION: Entered 'smartphones' into the search bar")

        # Simulate pressing Enter key
        search_bar.send_keys(Keys.ENTER)
        logging.info("ACTION: Pressed Enter to search")
        print("ACTION: Pressed Enter to search")

        time.sleep(10)  # Allow time for search results to load
        handle_popup(driver)

        # Verify search results
        search_results_heading = wait_for_element(driver, By.XPATH, "//div[@class='pl__headline']/h1")
        highlight_element(driver, search_results_heading)
        assert "smartphones" in search_results_heading.text.lower()
        logging.info("SUCCESS: Search results loaded successfully with heading 'Smartphones'")
        print("SUCCESS: Search results loaded successfully with heading 'Smartphones'")
        print("Test Case 6: Search functionality - Passed")
    except Exception as e:
        logging.error(f"ERROR: Failed during search functionality: {e}")
        print(f"ERROR: Failed during search functionality: {e}")
        pytest.fail("Test Case 6: Search functionality - Failed")

    # Add to cart after search
    try:
        logging.info("Starting Test Case 7: Add to Cart After Search")
        print("Starting Test Case 7: Add to Cart After Search")
        
        # Step 17.1: Locate and open the specified product link in a new window
        product_link = wait_for_clickable(driver, By.XPATH, "//div[@class='sp grid']//a[@attr-tag='anchor' and contains(., 'Apple iPhone 13 128 GB, Blue')]")
        highlight_element(driver, product_link)
        product_url = product_link.get_attribute("href")
        driver.execute_script(f"window.open('{product_url}', '_blank');")
        logging.info("ACTION: Opened the specified product link in a new window")
        print("ACTION: Opened the specified product link in a new window")
        
        # Switch to the new window
        driver.switch_to.window(driver.window_handles[-1])
        logging.info("ACTION: Switched to the new window")
        print("ACTION: Switched to the new window")
        wait_for_element(driver, By.TAG_NAME, "body")
        logging.info("ACTION: Verified product page loaded successfully")
        print("ACTION: Verified product page loaded successfully")

        # Step 18: Click "ADD TO CART" button
        add_to_cart_button = wait_for_clickable(driver, By.ID, "add_to_cart_main_btn")
        highlight_element(driver, add_to_cart_button)
        add_to_cart_button.click()
        logging.info("ACTION: Clicked 'ADD TO CART' button")
        print("ACTION: Clicked 'ADD TO CART' button")
        time.sleep(DELAY)
        
        print("Test Case 7: Add to Cart After Search - Passed")
    except Exception as e:
        logging.error(f"ERROR: Test Case 7 failed: {e}")
        print(f"ERROR: Test Case 7 failed: {e}")
        pytest.fail(f"Test Case 7: Add to Cart After Search - Failed")

    # Remove from cart
    try:
        logging.info("Starting Test Case 8: Remove from Cart")
        print("Starting Test Case 8: Remove from Cart")
        
        # Step 19.1: Click "Remove" button
        remove_button = wait_for_clickable(driver, By.XPATH, "//button[@aria-label='Remove from Cart' and @id='btn-cab-remove-491997702']")
        highlight_element(driver, remove_button)
        remove_button.click()
        logging.info("ACTION: Clicked 'Remove' button")
        print("ACTION: Clicked 'Remove' button")
        time.sleep(DELAY)
        
        # Step 19.2: Click "Yes" button to confirm removal
        yes_button = wait_for_clickable(driver, By.XPATH, "//button[@aria-label='Yes' and contains(., 'Yes')]")
        highlight_element(driver, yes_button)
        yes_button.click()
        logging.info("ACTION: Clicked 'Yes' button to confirm removal")
        print("ACTION: Clicked 'Yes' button to confirm removal")
        time.sleep(DELAY)
        
        print("Test Case 8: Remove from Cart - Passed")
        # Close the new window and switch back to the original window
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        logging.info("ACTION: Closed the new window and switched back to the original window")
    except Exception as e:
        logging.error(f"ERROR: Test Case 19 failed: {e}")
        print(f"ERROR: Test Case 8 failed: {e}")
        pytest.fail(f"Test Case 8: Remove from Cart - Failed")


    # Filter by price, brand, battery capacity and clear filter
    logging.info("Starting Test Case 9: Filter search results")
    print("Starting Test Case 9: Filter search results")
    try:
        handle_popup(driver)  # Ensure popup is handled at the beginning

        # Test Case 8.1: Apply price filter
        logging.info("ACTION: Applying price filter")
        print("ACTION: Applying price filter")
        
        # Locate and set min price
        min_price_input = wait_for_element(driver, By.XPATH, "//input[@aria-label='Min.']")
        highlight_element(driver, min_price_input)
        min_price_input.clear()
        min_price_input.send_keys("10000")
        logging.info("ACTION: Set minimum price to 10000")
        print("ACTION: Set minimum price to 10000")
        
        # Locate and set max price
        max_price_input = wait_for_element(driver, By.XPATH, "//input[@aria-label='Max.']")
        highlight_element(driver, max_price_input)
        max_price_input.clear()
        max_price_input.send_keys("17000")
        logging.info("ACTION: Set maximum price to 17000")
        print("ACTION: Set maximum price to 17000")

        # Click Go button to apply the filter
        go_button = wait_for_element(driver, By.XPATH, "//button[@aria-label='Go']")
        highlight_element(driver, go_button)
        go_button.click()
        logging.info("ACTION: Clicked 'Go' button to apply price filter")
        print("ACTION: Clicked 'Go' button to apply price filter")
        
        time.sleep(5)  # Allow time for the filter to apply

        # Click to see more brands
        see_more_brands = wait_for_element(driver, By.XPATH, "//span[contains(text(), 'See More')]")
        highlight_element(driver, see_more_brands)
        see_more_brands.click()
        logging.info("ACTION: Clicked 'See More' for brand options")
        print("ACTION: Clicked 'See More' for brand options")

        # Click the 'Xiaomi' brand div
        xiaomi_div = wait_for_element(driver, By.XPATH, "//div[contains(text(), 'Xiaomi') and @class='TextWeb__Text-sc-1cyx778-0 eJjyJG']")
        highlight_element(driver, xiaomi_div)
        xiaomi_div.click()
        logging.info("ACTION: Clicked 'Xiaomi' brand div")
        print("ACTION: Clicked 'Xiaomi' brand div")

        time.sleep(5)  # Allow time for the filter to apply

        # Test Case 8.3: Apply battery capacity filter
        logging.info("ACTION: Applying battery capacity filter")
        print("ACTION: Applying battery capacity filter")

        # Click to expand battery capacity options
        battery_capacity_section = wait_for_element(driver, By.XPATH, "//h4[text()='Battery Capacities']")
        highlight_element(driver, battery_capacity_section)
        battery_capacity_section.click()
        logging.info("ACTION: Clicked to expand battery capacities filter")
        print("ACTION: Clicked to expand battery capacities filter")

        # Click the '6000 mAh & Above' battery capacity div
        battery_div = wait_for_element(driver, By.XPATH, "//div[contains(text(), '6000 mAh & Above') and @class='TextWeb__Text-sc-1cyx778-0 eJjyJG']")
        highlight_element(driver, battery_div)
        battery_div.click()
        logging.info("ACTION: Clicked '6000 mAh & Above' battery capacity div")
        print("ACTION: Clicked '6000 mAh & Above' battery capacity div")

        time.sleep(5)  # Allow time for the filter to apply

        # Test Case 8.4: Clear all filters
        logging.info("ACTION: Clearing all filters")
        print("ACTION: Clearing all filters")

        # Click to clear all filters
        clear_filters_button = wait_for_element(driver, By.XPATH, "//div[contains(text(), 'Clear All')]")
        highlight_element(driver, clear_filters_button)
        clear_filters_button.click()
        logging.info("ACTION: Clicked 'Clear All' to reset all filters")
        print("ACTION: Clicked 'Clear All' to reset all filters")

        time.sleep(5)  # Allow time for filters to clear

        logging.info("SUCCESS: All filters applied and cleared successfully")
        print("SUCCESS: All filters applied and cleared successfully")
        print("Test Case 9: Apply Filters functionality - Passed")

    except Exception as e:
        logging.error(f"ERROR: Failed during filter application: {e}")
        print(f"ERROR: Failed during filter application: {e}")
        pytest.fail("Test Case 9: Apply Filters functionality - Failed")

    # Add to wishlist
    logging.info("Starting Test Case 10: Add to wishlist")
    print("Starting Test Case 10: Add to wishlist")
    try:
        handle_popup(driver)  # Ensure popup is handled at the beginning

        # Test Case 9.1: Click the 'Add to Wishlist' button
        add_to_wishlist_button = wait_for_clickable(driver, By.XPATH, "//button[@aria-label='Add to Wishlist']")
        highlight_element(driver, add_to_wishlist_button)
        add_to_wishlist_button.click()
        logging.info("ACTION: Clicked 'Add to Wishlist' button")
        print("ACTION: Clicked 'Add to Wishlist' button")

        time.sleep(2)  # Allow time for the modal to appear

        # Test Case 9.2: Click the 'should_by' button
        should_by_button = wait_for_clickable(driver, By.XPATH, "//button[@aria-label='should_by']")
        highlight_element(driver, should_by_button)
        should_by_button.click()
        logging.info("ACTION: Clicked 'should_by' button")
        print("ACTION: Clicked 'should_by' button")

        time.sleep(2)  # Allow time for the action to complete

        # Test Case 9.3: Click the final 'Add to Wishlist' button
        final_add_to_wishlist_button = wait_for_clickable(driver, By.XPATH, "//button[@aria-label='Add to Wishlist' and @theme='primary']")
        highlight_element(driver, final_add_to_wishlist_button)
        final_add_to_wishlist_button.click()
        logging.info("ACTION: Clicked final 'Add to Wishlist' button")
        print("ACTION: Clicked final 'Add to Wishlist' button")

        time.sleep(2)  # Allow time for the action to complete

        logging.info("SUCCESS: Item added to wishlist successfully")
        print("SUCCESS: Item added to wishlist successfully")
        print("Test Case 10: Add to Wishlist - Passed")
    except Exception as e:
        logging.error(f"ERROR: Failed during add to wishlist: {e}")
        print(f"ERROR: Failed during add to wishlist: {e}")
        pytest.fail("Test Case 10: Add to Wishlist - Failed")

    # Sort by price (high to low)
    logging.info("Starting Test Case 11: Sort by price (high to low)")
    print("Starting Test Case 11: Sort by price (high to low)")
    try:
        handle_popup(driver)  # Ensure popup is handled at the beginning

        # Click the 'Price (High-Low)' sorting option
        price_high_to_low_option = wait_for_clickable(driver, By.XPATH, "//span[contains(text(), 'Price(High-Low)')]")
        highlight_element(driver, price_high_to_low_option)    
        price_high_to_low_option.click()
        logging.info("ACTION: Clicked 'Price (High-Low)' sorting option")
        print("ACTION: Clicked 'Price (High-Low)' sorting option")

        time.sleep(5)  # Allow time for the sorting to apply

        # Verify the sorting is applied (This can be complex and may require checking the order of product prices)
        sorted_items = driver.find_elements(By.XPATH, "//div[@class='product-price']")
        prices = [float(item.text.replace('₹', '').replace(',', '')) for item in sorted_items if item.text]

        if prices == sorted(prices, reverse=True):
            logging.info("SUCCESS: Items sorted by price from high to low successfully")
            print("SUCCESS: Items sorted by price from high to low successfully")
            print("Test Case 11: Sort by Price (High-Low) - Passed")
        else:
            logging.error("ERROR: Items not sorted by price correctly")
            print("ERROR: Items not sorted by price correctly")
            pytest.fail("Test Case 11: Sort by Price (High-Low) - Failed")
    except Exception as e:
        logging.error(f"ERROR: Failed during sorting by price: {e}")
        print(f"ERROR: Failed during sorting by price: {e}")
        pytest.fail("Test Case 11: Sort by Price (High-Low) - Failed")

    # Remove from wishlist
    logging.info("Starting Test Case 12: Remove from Wishlist")
    print("Starting Test Case 12: Remove from Wishlist")
    try:
        handle_popup(driver)  # Ensure popup is handled at the beginning

        # Step 11.1: Hover over account details
        account_element = wait_for_element(driver, By.CSS_SELECTOR, "span#RIL_HeaderLoginAndMyAccount")
        highlight_element(driver, account_element)
        ActionChains(driver).move_to_element(account_element).perform()
        logging.info("ACTION: Hovered over account details")
        print("ACTION: Hovered over account details")

        # Step 11.2: Click on "My Wishlist"
        wishlist_link = wait_for_clickable(driver, By.CSS_SELECTOR, "a[href='/profile/wishlist'] div#wishlist")
        highlight_element(driver, wishlist_link)
        wishlist_link.click()
        logging.info("ACTION: Clicked on My Wishlist")
        print("ACTION: Clicked on My Wishlist")

        time.sleep(2)  # Wait for the wishlist page to load

        # Step 11.3: Click on the wishlist item
        wishlist_item = wait_for_clickable(driver, By.CSS_SELECTOR, "div.mywishlist__main-container__wishlist__title")
        highlight_element(driver, wishlist_item)
        wishlist_item.click()
        logging.info("ACTION: Clicked on the wishlist item")
        print("ACTION: Clicked on the wishlist item")

        # Step 11.4: Click on the delete icon
        delete_icon = wait_for_clickable(driver, By.CSS_SELECTOR, "div i.fa-trash-o")
        highlight_element(driver, delete_icon)
        delete_icon.click()
        logging.info("ACTION: Clicked on the delete icon")
        print("ACTION: Clicked on the delete icon")

        # Step 11.5: Confirm deletion
        confirm_delete_button = wait_for_clickable(driver, By.CSS_SELECTOR, "button.btn__primary span")
        highlight_element(driver, confirm_delete_button)
        confirm_delete_button.click()
        logging.info("ACTION: Confirmed the deletion")
        print("ACTION: Confirmed the deletion")

        time.sleep(2)  # Wait for the wishlist to update

        # Step 11.6: Verify wishlist is empty and click on "Continue Shopping"
        empty_wishlist_message = wait_for_element(driver, By.CSS_SELECTOR, "div.wishlist-main__noOrder h3")
        assert "Your Wishlist Currently has no Products" in empty_wishlist_message.text
        logging.info("SUCCESS: Verified the wishlist is empty")
        print("SUCCESS: Verified the wishlist is empty")

        continue_shopping_button = wait_for_clickable(driver, By.CSS_SELECTOR, "a.wishlist-main__continueShopping")
        highlight_element(driver, continue_shopping_button)
        continue_shopping_button.click()
        logging.info("ACTION: Clicked on Continue Shopping")
        print("ACTION: Clicked on Continue Shopping")

        print("Test Case 12: Remove from Wishlist - Passed")
    except Exception as e:
        logging.error(f"ERROR: Test Case 12 failed: {e}")
        print(f"ERROR: Test Case 12 failed: {e}")
        pytest.fail(f"Test Case 12: Remove from Wishlist - Failed")


    # Navigate to 'My Credits' page
    try:
        logging.info("Starting Test Case 13: Navigate to 'My Credits' Page")
        print("Starting Test Case 13: Navigate to 'My Credits' Page")

        # Step 1: Hover over account details
        account_element = wait_for_element(driver, By.CSS_SELECTOR, "span#RIL_HeaderLoginAndMyAccount")
        highlight_element(driver, account_element)
        ActionChains(driver).move_to_element(account_element).perform()
        logging.info("ACTION: Hovered over account details")
        print("ACTION: Hovered over account details")

        # Step 2: Select 'My Credits'
        my_credits_link = wait_for_clickable(driver, By.CSS_SELECTOR, "a[href='/profile/storecredit'] div#storecredit")
        highlight_element(driver, my_credits_link)
        my_credits_link.click()
        logging.info("ACTION: Clicked on 'My Credits' link")
        print("ACTION: Clicked on 'My Credits' link")

        time.sleep(2)  # Wait for the My Credits page to load

        # Step 3: Print the available balance
        available_balance = wait_for_element(driver, By.CSS_SELECTOR, "div.mycredit__page__balance__icon__amount")
        highlight_element(driver, available_balance)
        balance_text = available_balance.text.strip()
        logging.info(f"ACTION: Available balance: {balance_text}")
        print(f"ACTION: Available balance: {balance_text}")

        print("Test Case 13: Navigate to 'My Credits' Page - Passed")
    except Exception as e:
        logging.error(f"ERROR: Test Case 13: Navigate to 'My Credits' Page failed: {e}")
        print(f"ERROR: Test Case 13: Navigate to 'My Credits' Page failed: {e}")
        pytest.fail(f"Test Case 13: Navigate to 'My Credits' Page - Failed")

    # Add New Address
    try:
        logging.info("Starting Test Case 14: Add New Address")
        print("Starting Test Case 14: Add New Address")

        # Step 1: Click on 'My Address'
        my_address_link = wait_for_clickable(driver, By.CSS_SELECTOR, "a.left-nav__link-container__myacc[href='/profile/address'] div#address")
        highlight_element(driver, my_address_link)
        my_address_link.click()
        logging.info("ACTION: Clicked on 'My Address' link")
        print("ACTION: Clicked on 'My Address' link")

        time.sleep(2)  # Wait for the address page to load

        # Step 2: Click on 'Add New Shipping Address'
        add_new_address = wait_for_clickable(driver, By.CSS_SELECTOR, "div.myaddress__section__add")
        highlight_element(driver, add_new_address)
        add_new_address.click()
        logging.info("ACTION: Clicked on 'Add New Shipping Address' button")
        print("ACTION: Clicked on 'Add New Shipping Address' button")

        time.sleep(2)  # Wait for the add new address form to load

        logging.info("Starting Test Case 15: fill address form")
        print("Starting Test Case 15: fill address form")

        # Step 3: Verify 'Add a new Address' text appears
        add_new_address_text = wait_for_element(driver, By.CSS_SELECTOR, "div[title='Add a new Address']")
        highlight_element(driver, add_new_address_text)
        assert add_new_address_text.is_displayed(), "Add a new Address text not displayed"
        logging.info("ACTION: Verified 'Add a new Address' text is displayed")
        print("ACTION: Verified 'Add a new Address' text is displayed")

        # Step 4: Enter Pincode
        pincode_field = wait_for_element(driver, By.CSS_SELECTOR, "input#input-address-m-pincode")
        highlight_element(driver, pincode_field)
        pincode_field.send_keys("560078 ")
        logging.info("ACTION: Entered Pincode")
        print("ACTION: Entered Pincode")

        # Step 5: Enter First Name
        first_name_field = wait_for_element(driver, By.CSS_SELECTOR, "input#input-address-w-fname")
        highlight_element(driver, first_name_field)
        first_name_field.send_keys("Suman")
        logging.info("ACTION: Entered First Name")
        print("ACTION: Entered First Name")

        # Step 5.2: Enter Last Name
        last_name_field = wait_for_element(driver, By.CSS_SELECTOR, "input#input-address-w-lname")
        highlight_element(driver, last_name_field)
        last_name_field.send_keys("Naidu R")
        logging.info("ACTION: Entered Last Name")
        print("ACTION: Entered Last Name")

        # Step 6: Enter Address Line 1
        address_line1_field = wait_for_element(driver, By.CSS_SELECTOR, "input#input-address-w-line1")
        highlight_element(driver, address_line1_field)
        address_line1_field.send_keys("no 03")
        logging.info("ACTION: Entered Address Line 1")
        print("ACTION: Entered Address Line 1")

        # Step 8: Enter Address Line 2
        address_line2_field = wait_for_element(driver, By.CSS_SELECTOR, "input#input-address-w-line2")
        highlight_element(driver, address_line2_field)
        address_line2_field.send_keys("vittall nagar")
        logging.info("ACTION: Entered Address Line 2")
        print("ACTION: Entered Address Line 2")

        # Step 9: Enter Landmark
        landmark_field = wait_for_element(driver, By.CSS_SELECTOR, "input#input-address-w-line3")
        highlight_element(driver, landmark_field)
        landmark_field.send_keys("opp national convent school")
        logging.info("ACTION: Entered Landmark")
        print("ACTION: Entered Landmark")

        # Step 10: Enter Mobile Number
        mobile_number_field = wait_for_element(driver, By.CSS_SELECTOR, "input#input-address-w-mobileNumber")
        highlight_element(driver, mobile_number_field)
        mobile_number_field.send_keys("9538998293")
        logging.info("ACTION: Entered Mobile Number")
        print("ACTION: Entered Mobile Number")

        # Step 11: Click on 'Submit' button
        submit_button = wait_for_clickable(driver, By.CSS_SELECTOR, "button.Button__StyledButton-sc-1py7swr-0.jehPGe span.TextWeb__Text-sc-1cyx778-0.cXyRgU")
        highlight_element(driver, submit_button)
        submit_button.click()
        logging.info("ACTION: Clicked 'Submit' button")
        print("ACTION: Clicked 'Submit' button")
        logging.info("Test case 15 passed")
        print("Test case 15 passed")

        time.sleep(2)  # Wait for the address to be added

        # Step 12: Verify the newly added address
        added_address = wait_for_element(driver, By.CSS_SELECTOR, "label.myaddress__section__address__container")
        highlight_element(driver, added_address)
        assert "Suman Naidu R" in added_address.text
        assert "no 03" in added_address.text
        assert "vittall nagar" in added_address.text
        assert "opp national convent school" in added_address.text
        assert "Bangalore-560078, Karnataka" in added_address.text
        assert "+91 9538998293" in added_address.text
        logging.info("ACTION: Verified the newly added address")
        print("ACTION: Verified the newly added address")

        print("Test Case: Add New Address - Passed")
    except Exception as e:
        logging.error(f"ERROR: Test Case 14: Add New Address failed: {e}")
        print(f"ERROR: Test Case 14: Add New Address failed: {e}")
        pytest.fail(f"Test Case 14: Add New Address - Failed")





    # Delete address
    try:
        logging.info("Starting Test Case 16: Delete Address")
        print("Starting Test Case 16: Delete Address")

        # Step 1: Click on 'Delete' button for the address
        delete_button = wait_for_clickable(driver, By.CSS_SELECTOR, "button.Button__StyledButton-sc-1py7swr-0.krSokV span.TextWeb__Text-sc-1cyx778-0.cXyRgU i.fa.fa-trash-o")
        highlight_element(driver, delete_button)
        delete_button.click()
        logging.info("ACTION: Clicked 'Delete' button for the address")
        print("ACTION: Clicked 'Delete' button for the address")

        time.sleep(2)  # Wait for the confirmation dialog to appear

        # Step 2: Click 'Yes' to confirm deletion
        confirm_yes_button = wait_for_clickable(driver, By.CSS_SELECTOR, "button.Button__StyledButton-sc-1py7swr-0.jPTXqT.ripple[aria-label=' Yes '] span.TextWeb__Text-sc-1cyx778-0.cXyRgU")
        highlight_element(driver, confirm_yes_button)
        confirm_yes_button.click()
        logging.info("ACTION: Clicked 'Yes' button to confirm deletion")
        print("ACTION: Clicked 'Yes' button to confirm deletion")

        time.sleep(2)  # Wait for the address to be deleted

        # Verification: Check if the address has been deleted
        try:
            address_container = driver.find_element(By.CSS_SELECTOR, "label.myaddress__section__address__container")
            highlight_element(driver, address_container)
            address_text = address_container.text
            assert "Suman" not in address_text and "no 03" not in address_text and "vittall nagar" not in address_text and "opp national convent school" not in address_text and "Bangalore-560078" not in address_text and "9538998293" not in address_text
            logging.info("VERIFICATION: Address has been deleted")
            print("VERIFICATION: Address has been deleted")
        except NoSuchElementException:
            logging.info("VERIFICATION: Address container not found, assuming address deleted")
            print("VERIFICATION: Address container not found, assuming address deleted")

        print("Test Case: Delete Address - Passed")
    except Exception as e:
        logging.error(f"ERROR: Test Case 16: Delete Address failed: {e}")
        print(f"ERROR: Test Case 16: Delete Address failed: {e}")
        pytest.fail(f"Test Case 16: Delete Address - Failed")

    # Logout
    try:
        logging.info("Starting Test Case 17: Logout")
        print("Starting Test Case 17: Logout")

        # Step 1: Click on 'Logout' button
        logout_button = wait_for_clickable(driver, By.CSS_SELECTOR, "div.left-nav__link-container__myacc.pb__32 i.fa.hidden-xs.fa-sign-out")
        highlight_element(driver, logout_button)
        logout_button.click()
        logging.info("ACTION: Clicked 'Logout' button")
        print("ACTION: Clicked 'Logout' button")

        time.sleep(2)  # Wait for the logout process to complete

        # Verification: Check if the login element is present
        login_element = wait_for_element(driver, By.CSS_SELECTOR, "li.header__maininfo__list__item.dropdown__item[aria-label='Login'] span#RIL_HeaderLoginAndMyAccount")
        highlight_element(driver, login_element)
        assert "Login" in login_element.text
        logging.info("VERIFICATION: Verified 'Login' element is present after logout")
        print("VERIFICATION: Verified 'Login' element is present after logout")

        print("Test Case 17: Logout - Passed")
    except Exception as e:
        logging.error(f"ERROR: Test Case 17: Logout failed: {e}")
        print(f"ERROR: Test Case 17: Logout failed: {e}")
        pytest.fail(f"Test Case 17: Logout - Failed")

    # Test case 18: Invalid login
    logging.info("Starting Test Case 18: Invalid Login")
    print("Starting Test Case 18: Invalid Login")
    try:
        handle_popup(driver)  # Ensure popup is handled at the beginning

        login_button = wait_for_clickable(driver, By.XPATH, "//li[@class='header__maininfo__list__item dropdown__item' and @tabindex='0' and @aria-label='Login']//span[@class='pb__24 pointer' and @id='RIL_HeaderLoginAndMyAccount' and @role='button' and @tabindex='0']")
        highlight_element(driver, login_button)
        login_button.click()
        logging.info("ACTION: Clicked login button")
        print("ACTION: Clicked login button")
        time.sleep(DELAY)
        handle_popup(driver)
        
        mobile_input = wait_for_element(driver, By.ID, "lMobileNumber")
        highlight_element(driver, mobile_input)
        mobile_input.send_keys("0000000000")
        logging.info(f"ACTION: Entered invalid mobile number: 0000000000")
        print(f"ACTION: Entered invalid mobile number: 0000000000")
        handle_popup(driver)
        
        proceed_button = wait_for_clickable(driver, By.XPATH, "//button[@aria-label='Proceed']")
        highlight_element(driver, proceed_button)
        proceed_button.click()
        logging.info("ACTION: Clicked proceed button")
        print("ACTION: Clicked proceed button")
        time.sleep(DELAY)

        # Verification of error message
        error_message = wait_for_element(driver, By.XPATH, "//div[@class='Input__Error-sc-q4csvm-7 hMaMHi']")
        assert error_message.text == "Please enter a valid 10-digit mobile number", "Error message did not match expected"
        logging.info("SUCCESS: Correct error message displayed for invalid mobile number")
        print("SUCCESS: Correct error message displayed for invalid mobile number")

    except Exception as e:
        logging.error(f"ERROR: An error occurred during the invalid login test: {e}")
        print(f"ERROR: An error occurred during the invalid login test: {e}")
