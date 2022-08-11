from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from threading import Thread
import helpers as hp
import time

load_dotenv()
BUILD_NAME = "browserstack-build-1"
capabilities = [
    {
        "browserName": "chrome",
        "browserVersion": "103.0",
        "os": "Windows",
        "osVersion": "10",
        "sessionName": "Parallel Test 1",  # test name
        "buildName": BUILD_NAME,
    },
    {
        "browserName": "firefox",
        "browserVersion": "102.0",
        "os": "Windows",
        "osVersion": "10",
        "sessionName": "Parallel Test 2",
        "buildName": BUILD_NAME,
    },
]
def get_browser_option(browser):
    switcher = {
        "chrome": ChromeOptions(),
        "firefox": FirefoxOptions(),
    }
    return switcher.get(browser, ChromeOptions())

def run_session(cap):
    cap["userName"] = os.environ.get("BROWSERSTACK_USERNAME") or "testingforpk_m4AloY"
    cap["accessKey"] = os.environ.get("BROWSERSTACK_ACCESS_KEY") or "ptsT2Zc9sT2iVURoMnQe"
    options = get_browser_option(cap["browserName"].lower())
    options.set_capability("browserName", cap["browserName"].lower())
    options.set_capability("bstack:options", cap)
    driver = webdriver.Remote(
        command_executor="https://hub.browserstack.com/wd/hub", options=options
    )

    driver.get("https://www.amazon.com")
    time.sleep(3)

    print(driver.title)
    assert 'Amazon' in driver.title
    assert driver.title == 'Amazon.com. Spend less. Smile more.'

    print(driver.current_url)
    assert driver.current_url

    try:
        assert (driver.find_element(By.XPATH, "//a[@href='/ref=nav_logo']").get_attribute("href"))
        print('Amazon logo is presented')
    except NoSuchElementException:
        print('Amazon logo is not found')

    wait = WebDriverWait(driver, 6)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='nav-link-accountList']"))).click()

    # email = "testingforpk@gmail.com"
    # password = "testingforpk123"

    driver.find_element(By.XPATH, "//input[@id='ap_email']").send_keys(hp.email)
    driver.find_element(By.XPATH, "//input[@id='continue']").click()
    driver.find_element(By.XPATH, "//input[@id='ap_password']").send_keys(hp.password)

    time.sleep(3)  # waiting before click Sign-In button to avoid additional verification

    driver.find_element(By.XPATH, "//input[@id='signInSubmit']").click()

    try:
        assert (driver.find_element(By.XPATH, "//span[contains(.,'Hello, Testing')]"))
        print('User logged in')
    except NoSuchElementException:
        print('User not logged in')

    driver.quit()
# The Thread function takes run_session function and each set of capability from the caps array as an argument to run each session parallelly
for cap in capabilities:
    Thread(target=run_session, args=(cap,)).start()