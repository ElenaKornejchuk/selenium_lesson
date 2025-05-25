import allure
from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage
from tests.conftest import logger


class AdminLoginPage(BasePage):
    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)
        self.path = "/administration"

    @allure.step("Открытие страницы логина администратора")
    def open(self):
        logger.info("Открытие страницы логина администратора")
        super().open(self.path)

    @allure.step("Попытка логина с username='{username}'")
    def login(self, username, password):
        logger.info(f"Попытка логина: username='{username}'")
        username_input = self.wait_for(By.ID, "input-username")
        username_input.clear()
        username_input.send_keys(username)

        password_input = self.wait_for(By.ID, "input-password")
        password_input.clear()
        password_input.send_keys(password)

        self.wait_for(By.CSS_SELECTOR, "button[type='submit']").click()
        logger.info("Форма логина отправлена")

    @allure.step("Проверка успешного входа (наличие Dashboard)")
    def is_logged_in(self):
        logger.debug("Проверка успешного входа (наличие Dashboard)")
        self.wait_for(By.XPATH, "//h1[text()='Dashboard']")
        return True

    @allure.step("Выход из админки")
    def logout(self):
        logger.info("Выход из админки")
        self.browser.find_element(By.CSS_SELECTOR, "a[href*='logout']").click()