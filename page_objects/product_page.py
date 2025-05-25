import allure
from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage
from tests.conftest import logger


class ProductPage(BasePage):
    def __init__(self, browser, base_url, product_id):
        super().__init__(browser, base_url)
        self.path = f"/index.php?route=product/product&product_id={product_id}"

    @allure.step("Открытие страницы товара с ID: {self.path.split('=')[-1]}")
    def open(self):
        logger.info(f"Открытие страницы товара с ID: {self.path.split('=')[-1]}")
        super().open(self.path)

    @allure.step("Добавление товара в корзину")
    def add_to_cart(self):
        logger.info("Добавление товара в корзину.")
        self.wait_for(By.ID, "button-cart").click()

    @allure.step("Получение текста сообщения об успехе добавления товара в корзину")
    def get_alert_text(self):
        alert = self.wait_for(By.CLASS_NAME, "alert-success")
        logger.debug(f"Получено сообщение об успехе: {alert.text}")
        return alert.text
