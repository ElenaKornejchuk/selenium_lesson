from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url

    def open(self, path):
        self.browser.get(self.base_url + path)

    def wait_for(self, by, value, timeout=10):
        WebDriverWait(self.browser, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return self.browser.find_element(by, value)

    def find(self, by, locator):
        return self.browser.find_element(by, locator)

    def find_all(self, by, locator):
        return self.browser.find_elements(by, locator)

    def wait_for_all(self, by, locator, timeout=10):
        return WebDriverWait(self.browser, timeout).until(
            EC.presence_of_all_elements_located((by, locator)))