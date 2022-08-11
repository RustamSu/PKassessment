import pytest
import time
import helpers as hp
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver

# Driver initial fixture
@pytest.fixture
def driver_init():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome()
    driver.get("https://www.amazon.com/")
    yield driver
    driver.close()

def test_first():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.amazon.com/")

    # Поиск названия страницы и URL
    wait = WebDriverWait(driver, 6)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@href='/ref=nav_logo']")))
    assert driver.title == 'Amazon.com. Spend less. Smile more.'

    assert driver.current_url == 'https://www.amazon.com/'

    logo = driver.find_element_by_xpath("//a[@href='/ref=nav_logo']")
    assert logo.get_attribute('href') == 'https://www.amazon.com/ref=nav_logo'


    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='nav-link-accountList']"))).click()
    #driver.find_element(By.XPATH, "//span[contains(.,'Hello, Sign in')]").click()

    driver.find_element(By.XPATH, "//input[@id='ap_email']").send_keys(hp.email)
    driver.find_element(By.XPATH, "//input[@id='continue']").click()
    driver.find_element(By.XPATH, "//input[@id='ap_password']").send_keys(hp.password)

    time.sleep(3)
    driver.find_element(By.XPATH, "//input[@id='signInSubmit']").click()

    try:
        assert (driver.find_element(By.XPATH, "//span[contains(.,'Hello, Testing')]"))
        print('User logged in')
    except NoSuchElementException:
        print('User not logged in')

if __name__ == '__main__':
    test_first()
