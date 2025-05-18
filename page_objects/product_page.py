from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage

class ProductPage(BasePage):
    def __init__(self, browser, base_url, product_id):
        super().__init__(browser, base_url)
        self.path = f"/index.php?route=product/product&product_id={product_id}"

    def open(self):
        super().open(self.path)

    def add_to_cart(self):
        self.wait_for(By.ID, "button-cart").click()

    def get_alert_text(self):
        alert = self.wait_for(By.CLASS_NAME, "alert-success")
        return alert.text

