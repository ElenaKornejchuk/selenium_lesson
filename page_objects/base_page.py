import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.conftest import logger


class BasePage:
    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url

    @allure.step("Открытие страницы по указанному пути")
    def open(self, path):
        url = self.base_url + path
        logger.info(f"Открытие URL: {url}")
        self.browser.get(url)

    @allure.step("Ожидание элемента")
    def wait_for(self, by, value, timeout=10):
        logger.debug(f"Ожидание элемента: By.{by}, '{value}', timeout={timeout}")
        WebDriverWait(self.browser, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return self.browser.find_element(by, value)

    @allure.step("Поиск одного элемента")
    def find(self, by, locator):
        logger.debug(f"Поиск одного элемента: By.{by}, '{locator}'")
        return self.browser.find_element(by, locator)

    @allure.step("Поиск всех элементов")
    def find_all(self, by, locator):
        logger.debug(f"Поиск всех элементов: By.{by}, '{locator}'")
        return self.browser.find_elements(by, locator)

    @allure.step("Ожидание всех элементов: By.{by}, '{locator}', timeout={timeout}")
    def wait_for_all(self, by, locator, timeout=10):
        logger.debug(f"Ожидание всех элементов: By.{by}, '{locator}', timeout={timeout}")
        return WebDriverWait(self.browser, timeout).until(
            EC.presence_of_all_elements_located((by, locator))
        )