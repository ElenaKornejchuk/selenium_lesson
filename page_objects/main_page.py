import random
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from .base_page import BasePage


class MainPage(BasePage):
    path = "/"

    def open(self, path=None):
        if path is None:
            path = self.path
        super().open(path)

    def get_title(self):
        return self.browser.title

    def switch_currency(self, currency_name):
        symbol = currency_name.split()[0]  # "£", "€", "$"

        self.browser.find_element(By.CSS_SELECTOR, "a.dropdown-toggle").click()
        self.wait_for(By.XPATH, f"//a[contains(text(), '{currency_name}')]").click()

        WebDriverWait(self.browser, 10).until(
            lambda driver: symbol in driver.page_source
        )

    def get_prices(self):
        return [el.text for el in self.browser.find_elements(By.CSS_SELECTOR, ".product-thumb .price")]

    def is_element_present(self, by, locator):
        self.wait_for(by, locator)
        return True

    def get_products(self):
        return WebDriverWait(self.browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-thumb"))
        )

    def add_random_product_to_cart(self):
        products = self.get_products()

        valid_products = [
            p for p in products if not p.find_elements(By.CLASS_NAME, "price-old")
        ]

        if not valid_products:
            raise ValueError("No valid products found.")

        product = random.choice(valid_products)

        add_to_cart_button = product.find_element(By.CSS_SELECTOR, "button[title='Add to Cart']")
        self.browser.execute_script("arguments[0].click();", add_to_cart_button)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )

        success_message = self.browser.find_element(By.CLASS_NAME, "alert-success").text
        return success_message
