from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage


class AdminAddProductPage(BasePage):

    def fill_general_tab(self, name, description, meta_title):
        self.browser.find_element(By.ID, "input-name1").send_keys(name)
        self.browser.find_element(By.CLASS_NAME, "note-editable").send_keys(description)
        self.browser.find_element(By.ID, "input-meta-title1").send_keys(meta_title)

    def switch_to_data_tab(self):
        self.browser.find_element(By.LINK_TEXT, "Data").click()

    def fill_data_tab(self, model):
        self.browser.find_element(By.ID, "input-model").send_keys(model)

    def save_product(self):
        self.browser.find_element(By.CSS_SELECTOR, "button[data-original-title='Save']").click()