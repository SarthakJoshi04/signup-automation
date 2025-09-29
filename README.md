# Signup Automation Script

## Overview
This project automates the signup process for the website [https://authorized-partner.netlify.app/login](https://authorized-partner.netlify.app/login) as part of the QA Intern task for Vrit Technologies. The script uses Selenium WebDriver with Python to navigate through the signup flow, fill forms, handle OTP verification via MailSlurp, and submit the registration without manual intervention.

## Environment
- **Operating System**: Windows 10
- **Language**: Python (Version 3.13.3)
- **Library**: Selenium WebDriver
- **Framework**: None
- **Browser**: Brave (Version 1.82.172)
- **Driver**: ChromeDriver (Version 140.0.7339.207)
- **Additional Tool**: MailSlurp

## How to Run the Script
1. **Prerequisites**:
- Install Python, Brave browser and ChromeDriver.
- Get a free MailSlurp API key from [https://www.mailslurp.com/](https://www.mailslurp.com/).
  
2. **Setup**:
- Start the virtual environment using `.venv/Scripts/activate`.
- Install required dependencies using `pip install -r requirements.txt`.
- Update `config.py` with correct paths and test data.
- Create a `.env` file with your MailSlurp API key.
  
3. **Execution**:
- Run the script with `python automation_script.py`.
