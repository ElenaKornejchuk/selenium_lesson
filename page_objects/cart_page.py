from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)
        self.path = "/index.php?route=checkout/cart"

    def open(self):
        super().open(self.path)

    def remove_first_product(self):
        self.wait_for(By.CLASS_NAME, "btn-danger").click()

    def is_cart_empty(self):
        return "Your shopping cart is empty!" in self.browser.page_source
