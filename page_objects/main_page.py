import random

import allure
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from tests.conftest import logger
from .base_page import BasePage


class MainPage(BasePage):
    path = "/"

    @allure.story("Открытие главной страницы")
    @allure.title("Проверка заголовка главной страницы")
    def open(self, path=None):
        if path is None:
            path = self.path
        logger.info(f"Opening main page with path: {path}")
        super().open(path)

    @allure.step("Получить заголовок страницы")
    def get_title(self):
        title = self.browser.title
        logger.info(f"Page title is: '{title}'")
        return title

    @allure.step("Переключить валюту на '{currency_name}'")
    def switch_currency(self, currency_name):
        logger.info(f"Switching currency to: {currency_name}")
        symbol = currency_name.split()[0]

        self.browser.find_element(By.CSS_SELECTOR, "a.dropdown-toggle").click()
        self.wait_for(By.XPATH, f"//a[contains(text(), '{currency_name}')]" ).click()

        WebDriverWait(self.browser, 10).until(
            lambda driver: symbol in driver.page_source
        )
        logger.info(f"Currency switched successfully to: {currency_name}")

    @allure.step("Получить список цен")
    def get_prices(self):
        prices = [el.text for el in self.browser.find_elements(By.CSS_SELECTOR, ".product-thumb .price")]
        logger.debug(f"Prices found: {prices}")
        return prices

    @allure.step("Проверка наличия элемента: {by}, {locator}")
    def is_element_present(self, by, locator):
        logger.debug(f"Checking presence of element by {by} with locator '{locator}'")
        self.wait_for(by, locator)
        return True

    @allure.step("Получить список всех продуктов на главной странице")
    def get_products(self):
        logger.debug("Getting list of products from the main page")
        products = WebDriverWait(self.browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-thumb"))
        )
        logger.info(f"Found {len(products)} products")
        return products

    @allure.step("Добавить случайный продукт в корзину")
    def add_random_product_to_cart(self):
        logger.info("Attempting to add a random product to the cart")
        products = self.get_products()

        valid_products = [
            p for p in products if not p.find_elements(By.CLASS_NAME, "price-old")
        ]

        if not valid_products:
            logger.warning("No valid (non-discounted) products found to add to cart")
            raise ValueError("No valid products found.")

        product = random.choice(valid_products)
        logger.debug("Random product selected for cart")

        add_to_cart_button = product.find_element(By.CSS_SELECTOR, "button[title='Add to Cart']")
        self.browser.execute_script("arguments[0].click();", add_to_cart_button)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )

        success_message = self.browser.find_element(By.CLASS_NAME, "alert-success").text
        logger.info(f"Product successfully added to cart: {success_message}")
        return success_message
