import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BRAVE_PATH = r"C:\Users\sarth\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"
CHROMEDRIVER_PATH = r"D:\chromedriver-win64/chromedriver.exe"

# Personal details
FIRST_NAME = "John"
LAST_NAME = "Doe"
PHONE_NUMBER = "9823236221"
PASSWORD = "Test@123"

# Agency details
AGENCY_NAME = "John's Agency"
ROLE_IN_AGENCY = "Manager"
AGENCY_EMAIL = "johnagency@gmail.com"
AGENCY_WEBSITE = "www.johnsagency.com"
AGENCY_ADDRESS = "Kathmandu, Nepal"
OPERATIONAL_REGION = "Nepal"

# Professional experience
YEARS_OF_EXPERIENCE = "5 years"
RECRUITED_STUDENTS = "100"
FOCUS_AREAS = "Visa consulting for Australia"
SUCCESS_METRICS = "75"
SERVICES_PROVIDED = "Visa Processing"

# Business preferences
REG_NO = "123456"
PREFERRED_COUNTRIES = "Australia"
PREFERRED_INSTITUTIONS = "Universities"
CERTIFICATION_DETAILS = "Certified Agent"
COMPANY_REGISTRATION = os.path.join(BASE_DIR, "files", "doc1.png")
EDUCATIONAL_CERTIFICATE = os.path.join(BASE_DIR, "files", "doc2.png")