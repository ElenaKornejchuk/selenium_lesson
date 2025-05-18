import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from page_objects.base_page import BasePage

class AdminCatalogPage(BasePage):

    def open_products(self):
        self.wait_for(By.ID, "menu-catalog").click()
        self.wait_for(By.LINK_TEXT, "Products").click()

    def add_new_product(self, name, meta_title, model, seo):
        add_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-primary[aria-label='Add New']"))
        )
        self.browser.execute_script("arguments[0].scrollIntoView(true);", add_button)
        time.sleep(1)
        self.browser.execute_script("arguments[0].click();", add_button)

        WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.ID, "input-name-1"))
        )

        self.browser.find_element(By.ID, "input-name-1").send_keys(name)
        self.browser.find_element(By.ID, "input-meta-title-1").send_keys(meta_title)

        self.browser.find_element(By.LINK_TEXT, "Data").click()
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.ID, "input-model"))
        )
        self.browser.find_element(By.ID, "input-model").send_keys(model)

        self.browser.find_element(By.LINK_TEXT, "SEO").click()
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.ID, "input-keyword-0-1"))
        )
        self.browser.find_element(By.ID, "input-keyword-0-1").send_keys(seo)

        save_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-original-title='Save']"))
        )
        self.browser.execute_script("arguments[0].click();", save_button)

        WebDriverWait(self.browser, 10).until(
            EC.url_contains("route=catalog/product")
        )

    def is_product_added(self, name):
        return name in self.browser.page_source

    def delete_product(self, name):
        search_input = self.wait_for(By.ID, "input-name")
        search_input.clear()
        search_input.send_keys(name)

        self.wait_for(By.ID, "button-filter").click()

        try:
            checkboxes = WebDriverWait(self.browser, 10).until(
                EC.presence_of_all_elements_located((By.NAME, "selected[]"))
            )

            for checkbox in checkboxes:
                if checkbox.is_displayed() and checkbox.is_enabled():
                    checkbox.click()
                    break

            delete_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-original-title='Delete']"))
            )
            delete_button.click()

            self.browser.switch_to.alert.accept()
        except Exception as e:
            print(f"Ошибка при удалении продукта: {e}")


    def is_product_deleted(self, name):
        search_input = self.wait_for(By.ID, "input-name")
        search_input.clear()
        search_input.send_keys(name)
        self.wait_for(By.ID, "button-filter").click()
        return "No results!" in self.browser.page_source
