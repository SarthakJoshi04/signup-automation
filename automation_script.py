from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from mailslurp_client import ApiClient, Configuration, InboxControllerApi, WaitForControllerApi
import re
import logging
import time
import os

from dotenv import load_dotenv
import config as cfg

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    # Brave browser path
    brave_path = cfg.BRAVE_PATH

    # ChromeDriver path
    driver_path = cfg.CHROMEDRIVER_PATH

    # Set Brave as the browser for Selenium
    options = Options()
    options.binary_location = brave_path

    # Start Selenium WebDriver with Brave
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Open the site
    driver.get("https://authorized-partner.netlify.app/login")
    time.sleep(1)

    logging.info("Application opened in Brave with Selenium.")

    # Initialize MailSlurp client
    configuration = Configuration()
    configuration.api_key['x-api-key'] = os.getenv('API_KEY')

    api_client = ApiClient(configuration)
    inbox_controller = InboxControllerApi(api_client)
    wait_for_controller = WaitForControllerApi(api_client)

    logging.info("MailSlurp client initialized.")

    # Setup a MailSlurp inbox
    new_inbox = inbox_controller.create_inbox()
    temp_email = new_inbox.email_address
    inbox_id = new_inbox.id

    logging.info(f"Created temporary email: {temp_email}")

    # Configure wait time
    wait = WebDriverWait(driver, 10)

    # Click Sign Up button to navigate to the registration page
    signup_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign Up")))
    signup_button.click()

    logging.info("Clicked on Sign Up button.")

    # Check the ToS checkbox
    tos_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "remember")))
    tos_checkbox.click()

    logging.info("Checked the Terms of Service checkbox.")

    # Click continue button
    continue_button = driver.find_element(By.XPATH, "//button[contains(@class, 'primary-btn') and contains(text(), 'Continue')]")
    continue_button.click()

    logging.info("Clicked on Continue button.")
    time.sleep(3)

    # Fill personal details
    first_name = wait.until(EC.visibility_of_element_located((By.NAME, "firstName")))
    first_name.send_keys(cfg.FIRST_NAME)

    last_name = driver.find_element(By.NAME, "lastName")
    last_name.send_keys(cfg.LAST_NAME)

    email = driver.find_element(By.NAME, "email")
    email.send_keys(temp_email)

    phone_number = driver.find_element(By.NAME, "phoneNumber")
    phone_number.send_keys(cfg.PHONE_NUMBER)

    password = driver.find_element(By.NAME, "password")
    password.send_keys(cfg.PASSWORD)

    confirm_password = driver.find_element(By.NAME, "confirmPassword")
    confirm_password.send_keys(cfg.PASSWORD)

    logging.info("Filled personal details.")

    next_button = driver.find_element(By.XPATH, "//button[contains(@class, 'primary-btn') and contains(text(), 'Next')]")
    next_button.click()

    logging.info("Clicked on Next button.")

    # Wait for the latest email
    latest_email = wait_for_controller.wait_for_latest_email(inbox_id=inbox_id, timeout=60000, delay=1000)
    email_body = latest_email.body 

    logging.info("OTP email received.")

    # print(email_body)

    # Extract 6-digit code using regex
    otp_match = re.search(r'<p[^>]*>\s*(\d{6})\s*</p>', email_body, re.IGNORECASE)
    if otp_match:
        otp_code = otp_match.group(1)
        logging.info(f"Extracted OTP: {otp_code}")
    else:
        raise Exception("OTP not found.")

    # Confirm verification code
    verification_code = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@data-input-otp='true']")))
    verify_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'primary-btn') and contains(text(), 'Verify') and contains(@type, 'submit')]")
    
    verification_code.send_keys(otp_code)
    verify_btn.click()

    logging.info("Entered OTP and clicked Verify button.")

    # Provide agency details
    agency_name = wait.until(EC.presence_of_element_located((By.NAME, "agency_name")))
    agency_name.send_keys(cfg.AGENCY_NAME)

    role_in_agency = driver.find_element(By.NAME, "role_in_agency")
    role_in_agency.send_keys(cfg.ROLE_IN_AGENCY)

    agency_email = driver.find_element(By.NAME, "agency_email")
    agency_email.send_keys(cfg.AGENCY_EMAIL)

    agency_website = driver.find_element(By.NAME, "agency_website")
    agency_website.send_keys(cfg.AGENCY_WEBSITE)

    agency_address = driver.find_element(By.NAME, "agency_address")
    agency_address.send_keys(cfg.AGENCY_ADDRESS)

    # Click on region dropdown and wait for the options to appear
    region_dropdown = driver.find_element(By.CSS_SELECTOR, 'button[aria-controls^="radix-"]')
    region_dropdown.click()

    # Select the operation region
    country_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div//span[text()='{cfg.OPERATIONAL_REGION}']")))
    country_option.click()

    logging.info("Filled agency details.")

    next_button = driver.find_element(By.XPATH, "//button[contains(@class, 'primary-btn') and contains(text(), 'Next')]")
    next_button.click()

    logging.info("Clicked on Next button.")

    # Enter professional experience details
    experience_select = wait.until(EC.presence_of_element_located((By.TAG_NAME, "select")))
    select = Select(experience_select)
    select.select_by_visible_text(cfg.YEARS_OF_EXPERIENCE)

    recruited_students = driver.find_element(By.NAME, "number_of_students_recruited_annually")
    recruited_students.send_keys(cfg.RECRUITED_STUDENTS)

    focus_areas = driver.find_element(By.NAME, "focus_area")
    focus_areas.send_keys(cfg.FOCUS_AREAS)

    success_metrics = driver.find_element(By.NAME, "success_metrics")
    success_metrics.send_keys(cfg.SUCCESS_METRICS)

    service_checkbox = driver.find_element(By.XPATH, f"//label[text()='{cfg.SERVICES_PROVIDED}']/preceding-sibling::button[@role='checkbox']")
    service_checkbox.click()

    next_button = driver.find_element(By.XPATH, "//button[contains(@class, 'primary-btn') and contains(text(), 'Next')]")
    next_button.click()

    logging.info("Clicked on Next button.")

    # Enter business details and preferences
    reg_no = wait.until(EC.presence_of_element_located((By.NAME, "business_registration_number")))
    reg_no.send_keys(cfg.REG_NO)

    preferred_countries_dropdown = driver.find_element(By.CSS_SELECTOR, 'button[aria-controls^="radix-"]')
    preferred_countries_dropdown.click()

    country_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div//span[text()='{cfg.PREFERRED_COUNTRIES}']")))
    country_option.click()

    preferred_institution_checkbox = driver.find_element(By.XPATH, f"//label[text()='{cfg.PREFERRED_INSTITUTIONS}']/preceding-sibling::button[@role='checkbox']")
    preferred_institution_checkbox.click()

    certification_details = driver.find_element(By.NAME, "certification_details")
    certification_details.send_keys(cfg.CERTIFICATION_DETAILS)

    file_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")

    file_inputs[0].send_keys(cfg.COMPANY_REGISTRATION)
    file_inputs[1].send_keys(cfg.EDUCATIONAL_CERTIFICATE)

    logging.info("Filled business details and preferences.")

    submit_button = driver.find_element(By.XPATH, "//button[contains(@class, 'primary-btn') and contains(text(), 'Submit')]")
    submit_button.click()

    dashboard_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'My Profile')]")))
    logging.info("Registration process completed.")
    time.sleep(1)
except Exception as e:
   logging.warning(f"An error occurred: {e}")
finally:
    if 'driver' in locals():
        driver.quit()
    logging.info("Browser closed.")