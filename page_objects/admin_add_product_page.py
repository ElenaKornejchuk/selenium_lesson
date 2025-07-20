import allure
from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage
from tests.conftest import logger


class AdminAddProductPage(BasePage):

    @allure.step("Заполнение вкладки General")
    def fill_general_tab(self, name, description, meta_title):
        logger.info(f"Заполнение вкладки General: name='{name}', meta_title='{meta_title}'")
        self.browser.find_element(By.ID, "input-name1").send_keys(name)
        self.browser.find_element(By.CLASS_NAME, "note-editable").send_keys(description)
        self.browser.find_element(By.ID, "input-meta-title1").send_keys(meta_title)

    @allure.step("Переключение на вкладку Data")
    def switch_to_data_tab(self):
        logger.info("Переключение на вкладку Data")
        self.browser.find_element(By.LINK_TEXT, "Data").click()

    @allure.step("Заполнение вкладки Data")
    def fill_data_tab(self, model):
        logger.info(f"Заполнение вкладки Data: model='{model}'")
        self.browser.find_element(By.ID, "input-model").send_keys(model)

    @allure.step("Сохранение нового продукта")
    def save_product(self):
        logger.info("Сохранение нового продукта")
        self.browser.find_element(By.CSS_SELECTOR, "button[data-original-title='Save']").click()