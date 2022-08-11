# 1, Open URL https://www.amazon.com/
# Verify page name and URL
# Verify that Amazon logo presented
# Login into account

from selenium import webdriver

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import helpers as hp
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.amazon.com/")

time.sleep(3)

print(driver.title)
assert 'Amazon' in driver.title
print(driver.current_url)

try:
    assert(driver.find_element(By.XPATH, "//a[@href='/ref=nav_logo']").get_attribute("href"))
    print('Amazon logo is presented')
except NoSuchElementException:
    print('Amazon logo is not found')

wait = WebDriverWait(driver, 6)
element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='nav-link-accountList']"))).click()

#email = "testingforpk@gmail.com"
#password = "testingforpk123"

driver.find_element(By.XPATH, "//input[@id='ap_email']").send_keys(hp.email)
driver.find_element(By.XPATH, "//input[@id='continue']").click()
driver.find_element(By.XPATH, "//input[@id='ap_password']").send_keys(hp.password)

time.sleep(3) # waiting before click Sign-In button to avoid additional verification

driver.find_element(By.XPATH, "//input[@id='signInSubmit']").click()

try:
    assert(driver.find_element(By.XPATH, "//span[contains(.,'Hello, Testing')]"))
    print('User logged in')
except NoSuchElementException:
    print('User not logged in')

driver.quit()
