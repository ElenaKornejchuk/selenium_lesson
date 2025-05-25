import allure
from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage
from tests.conftest import logger


class CartPage(BasePage):
    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)
        self.path = "/index.php?route=checkout/cart"

    @allure.step("Открытие страницы корзины")
    def open(self):
        logger.info("Открытие страницы корзины.")
        super().open(self.path)

    @allure.step("Удаление первого товара из корзины")
    def remove_first_product(self):
        logger.info("Удаление первого товара из корзины.")
        self.wait_for(By.CLASS_NAME, "btn-danger").click()

    @allure.step("Проверка, пуста ли корзина")
    def is_cart_empty(self):
        empty = "Your shopping cart is empty!" in self.browser.page_source
        logger.debug(f"Корзина пуста: {empty}")
        return empty